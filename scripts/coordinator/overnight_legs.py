#!/usr/bin/env python3
"""overnight_legs.py — run coordinator sessions back to back, unattended, as
headless `claude -p` legs (owner, 2026-10-09: "Headless leg loop").

Why it exists: one coordinator session holds about five rows before the 50%
context guard latches, and the guard's own relaunch fires only when a session
EXITS, which an interactive session never does by itself. A headless leg does
exit when its one turn ends, so this loop is the relaunch: each leg starts
from the newest handoff's session prompt (the kit's own reader,
`coordinator_guard.session_prompt`), works the queue until the latch, closes
out (handoff, status, log, full suite, lease handback) and exits; the next leg
starts from the handoff it wrote.

Probed 2026-10-09 (Claude Code 2.1.289): a `-p` session exits when its turn
ends and KILLS its background tasks, so every leg must work in the foreground;
`--settings '{"env":{"BASH_MAX_TIMEOUT_MS": ...}}'` raises the shell tool's
foreground cap (the plain environment variable is not read).

Stops (never retries blindly):
  - the newest handoff carries the line `Overnight: stop` (queue drained, or
    nothing can move without the owner);
  - a leg exits non-zero, or leaves the coordinator lease held, or adds no
    new handoff (no progress);
  - --max-legs is reached.
A handoff line `Resume-not-before: <ISO local time>` (a Codex plan limit,
say) makes the loop wait until then before the next leg.

    python overnight_legs.py [--repo C:/Projects/ai-template] [--max-legs 6]
                             [--dry-run]
"""

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import time
from pathlib import Path

LOGDIR = Path("C:/Projects/ai-template.wt/overnight-logs")
SETTINGS = {"env": {"BASH_MAX_TIMEOUT_MS": "3600000", "BASH_DEFAULT_TIMEOUT_MS": "600000"}}
STOP_RE = re.compile(r"^\s*Overnight:\s*stop\b", re.M | re.I)
WAIT_RE = re.compile(r"^\s*Resume-not-before:\s*(\S+)", re.M)


def log(msg):
    line = "[{}] {}".format(dt.datetime.now().isoformat(timespec="seconds"), msg)
    print(line, flush=True)
    with (LOGDIR / "loop.log").open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8"
    ).stdout.strip()


def newest_handoff(repo):
    """The handoff most recently ADDED on the checked-out branch."""
    name = git(repo, "log", "-1", "--diff-filter=A", "--format=", "--name-only", "--", "docs/handoff-*.md")
    return (repo / name) if name else None


def lease_holder(repo):
    out = subprocess.run(
        [sys.executable, "project-trajectory/scripts/coordinator_guard.py", "status"],
        cwd=repo, capture_output=True, text=True, encoding="utf-8",
    ).stdout
    try:
        return (json.loads(out).get("lease") or {}).get("holder")
    except ValueError:
        return "unreadable"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="C:/Projects/ai-template")
    ap.add_argument("--max-legs", type=int, default=6)
    ap.add_argument("--model", default="claude-opus-5-5")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    repo = Path(args.repo).resolve()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(repo / "project-trajectory" / "scripts"))
    import coordinator_guard  # the kit's own session-prompt reader

    for leg in range(1, args.max_legs + 1):
        handoff = newest_handoff(repo)
        if handoff is None or not handoff.is_file():
            log("stop: no handoff found")
            return 2
        text = handoff.read_text(encoding="utf-8")
        if STOP_RE.search(text):
            log("stop: {} says Overnight: stop".format(handoff.name))
            return 0
        waited = WAIT_RE.search(text)
        if waited:
            try:
                until = dt.datetime.fromisoformat(waited.group(1))
                if until.tzinfo is None:  # a bare time is local time
                    until = until.astimezone()
                delay = (until - dt.datetime.now().astimezone()).total_seconds()
                if delay > 0:
                    log("waiting {:.0f} s until {} ({})".format(delay, until, handoff.name))
                    if not args.dry_run:
                        time.sleep(delay)
            except ValueError:
                log("ignoring unreadable Resume-not-before: {}".format(waited.group(1)))
        prompt = coordinator_guard.session_prompt(handoff)
        if not prompt:
            log("stop: {} carries no session prompt".format(handoff.name))
            return 2
        holder = lease_holder(repo)
        if holder:
            log("stop: the coordinator lease is held by {} before leg {}".format(holder, leg))
            return 2
        cmd = [
            "claude", "-p", prompt,
            "--model", args.model,
            "--permission-mode", "bypassPermissions",
            "--settings", json.dumps(SETTINGS),
            "--output-format", "text",
        ]
        out = LOGDIR / "leg-{:02d}-{}.log".format(leg, dt.datetime.now().strftime("%Y%m%d-%H%M%S"))
        log("leg {} from {} -> {}".format(leg, handoff.name, out.name))
        if args.dry_run:
            log("dry run: would run claude -p <{} chars> --model {}".format(len(prompt), args.model))
            return 0
        head_before = git(repo, "rev-parse", "HEAD")
        with out.open("w", encoding="utf-8") as fh:
            code = subprocess.call(cmd, cwd=repo, stdout=fh, stderr=subprocess.STDOUT)
        after = newest_handoff(repo)
        log("leg {} exit {}; trunk {} -> {}; newest handoff {}".format(
            leg, code, head_before[:8], git(repo, "rev-parse", "HEAD")[:8], after.name if after else None))
        if code != 0:
            log("stop: leg {} exited {}".format(leg, code))
            return 3
        if lease_holder(repo):
            log("stop: leg {} left the coordinator lease held".format(leg))
            return 3
        if after is None or after == handoff:
            log("stop: leg {} wrote no new handoff".format(leg))
            return 3
    log("stop: --max-legs {} reached".format(args.max_legs))
    return 0


if __name__ == "__main__":
    sys.exit(main())
