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

A run is an autonomous run, marked (review-churn plan revisions 35, "The
coordinator role", and 36, "Headless coordinator legs are marked now"; the
owner's 2026-10-14 split ruling; docs/decisions/coordinator-2026-10-14.toml
D-015 and D-016):
  - the marker. Before the first leg the launcher calls the kit's
    `provenance.mark_loop_process()` once, in its own process, and logs the
    session. That is one session per run (D-016 Q1), inherited by every leg
    and by every process a leg starts, so every commit a leg makes is judged
    by the loop's commit floor and every held status move is refused. A
    well-formed inherited marker is kept and a malformed one is replaced, as
    that function states;
  - the prompt. Each leg's prompt is the newest handoff's session prompt
    (unchanged), then the headless block `headless-leg.md` beside this file
    (read once per run), then the kit's `agent_brief.loop_provenance_note()`,
    which names the session (D-016 Q2). It is piped to the agent CLI on stdin,
    the route the kit's own launches take, and the CLI is resolved on PATH.

A run's trunk is bound once (coordinator-2026-10-18 D-004 and D-005): before
the first leg the launcher reads the trunk's name through the kit's one trunk
reader (`agent_common.trunk_name`) and logs it (`run trunk <name>`). Every leg
in the run is judged against that bound trunk, whatever branch the checkout is
on: the checkout's branch is only compared with it, never read as trunk.

Stops (never retries blindly):
  - before anything else, exit 2 with the reason on stderr and no log
    directory made: the checkout's commit hooks are not on (the kit's
    `commit_hooks.hooks_refusal`);
  - before any leg, exit 2: the headless block is absent, unreadable or
    empty; the provenance note is empty; no `claude` resolves on PATH; the
    trunk reader refuses (the run prints its message);
  - the newest handoff carries the line `Overnight: stop` (queue drained, or
    nothing can move without the owner);
  - exit 3, before a leg: the snapshot does not hold the bound trunk, or the
    checkout is not on it (its HEAD is detached, unreadable or unparseable,
    or names another branch);
  - exit 3, the audit (WI-917's Trust section, as WI-946 amends it): the
    launcher snapshots every local branch immediately before a leg and again
    after it exits, then judges the bound trunk (it must still resolve and
    descend from its pre-leg tip, and every commit the leg added to its
    first-parent line must carry this run's trailer), then `archive/lanes` by
    the same rule, except that it may be created (absent before, it reads
    `absent`, or, created, is judged over the commits no pre-leg branch
    reaches), then every other branch the leg created or moved, over its range
    from trunk, by the merge slot's own lane rule (the claim read through the
    kit's one claim reader, `agent_common.loop_claimed`, then
    `provenance.loop_lane_window`, then the trailer check inside the window,
    which accepts any well-formed session; an attended re-claim closes the
    window as at the slot, read from the same commit records, parents and
    trees included, D-005 C4), then the checkout, which must still be on the
    bound trunk. A refused commit, a claim the reader cannot read, an
    `archive/lanes` that no longer resolves or no longer descends from its
    pre-leg tip, a checkout off the bound trunk, or a git read that fails or
    cannot be parsed, stops the run naming the commit, the pre-leg tip or the
    read; a branch the leg deleted is logged, not judged. Nothing is repaired,
    skipped or re-ordered;
  - a leg exits non-zero, or leaves the coordinator lease held, or adds no
    new handoff (no progress);
  - --max-legs is reached.
A handoff line `Resume-not-before: <ISO local time>` (a Codex plan limit,
say) makes the loop wait until then before the next leg.

**The bound.** The audit judges what the two snapshots can see, and they
cannot see a branch created and deleted inside one leg, or any ref outside
`refs/heads/` (tags, `refs/stash`, notes). Such commits reach a judged ref in
only three ways: as a first-parent commit of trunk or `archive/lanes`, which
the audit judges; as a commit of a branch the leg created or moved, which the
lane rule judges; or as a merge's non-first-parent commits. Those, on trunk's
or `archive/lanes`' first-parent line, are judged by no rule: the archive's
extra parents are lane tips, by the landing recipe, and a lane merged onto
trunk is off procedure while landings are squashes after `check-lane` (once
WI-808 puts landings on the merge slot, its trailer rung judges the lane it
merges). The audit judges provenance only, not which branches a leg may
move: a marked commit on a branch the lane rule reads as a person's (`main`
included) passes it, and the owner-held steps belong to the procedure (the
coordinator-cycle skill's headless-leg section), not to the audit. Until
WI-925 declares the trunk's name, `check-lane` reads trunk at its own run as
the branch the primary checkout is on at that moment, or, when the primary
checkout is detached, as the current branch of the `--repo` checkout, so two
orders escape it. A leg switches the primary checkout, runs `check-lane`, and
switches back before its squash; or a leg detaches the primary checkout and
runs `check-lane` with `--repo` at a lane's worktree, where trunk reads as
the lane itself, the range is empty, and the lane passes. No supported
workflow produces either order (PROCESS.md §6). WI-925's declared name ends
both.

    python overnight_legs.py [--repo <checkout>] [--max-legs 6] [--dry-run]
    python overnight_legs.py check-lane <branch> [--repo <checkout>]

`check-lane` runs the same lane rule over one branch at its tip, from the tip
of the trunk the kit's trunk reader names at its own run, and sets no marker:
exit 0, or 3 printing the first refused commit, the failed read (an
unresolvable branch is a failed read) or the trunk reader's refusal ("cannot
judge"). It reads a re-claim exactly as the merge slot's trailer rung does: an
empty, unmarked commit under the lane's re-claim subject exempts the commits
after it until a loop writer marks the lane again. A headless leg runs it
before it squashes a lane, so a lane holding an unmarked commit is not landed
(the coordinator-cycle skill's headless-leg section).

The checkout defaults to the one holding this script, and the logs go to
`overnight-logs` in its sibling `.wt` folder (`layout.py`).
"""

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from layout import REPO, WTROOT

LOGDIR = WTROOT / "overnight-logs"
HEADLESS_BLOCK = Path(__file__).with_name("headless-leg.md")
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


def read_block(path):
    """(the headless block's text stripped, None), or (None, why it is unusable)."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return None, "absent"
    except UnicodeDecodeError:
        return None, "not UTF-8"
    except OSError as exc:
        return None, "unreadable ({})".format(exc)
    text = text.strip()
    return (text, None) if text else (None, "empty")


def leg_prompt(session_prompt, block, note):
    """A leg's prompt: the handoff's session prompt, then the headless block,
    then the provenance note, which opens with its own blank line."""
    return session_prompt + "\n\n" + block.strip() + note


def prepare_run(repo):
    """Read the block, mark the run, compose the note, resolve the agent CLI
    and bind the run's trunk, in that order; (block, note, claude, session,
    the trunk's ref), or None after logging the stop."""
    block, reason = read_block(HEADLESS_BLOCK)
    if block is None:
        log("stop: the headless block {} is {}".format(HEADLESS_BLOCK, reason))
        return None
    import agent_brief  # the kit's standing trailer instruction
    from kitlib import provenance  # the kit's loop marker

    inherited = provenance.loop_session()
    session = provenance.mark_loop_process()
    log("run session {} ({})".format(session, "inherited" if inherited == session else "new"))
    note = agent_brief.loop_provenance_note()
    if not note.strip():
        log("stop: the loop provenance note is empty under run session {}".format(session))
        return None
    claude = shutil.which("claude")
    if not claude:
        log("stop: no `claude` agent CLI resolves on PATH")
        return None
    trunk = bind_trunk(repo)
    if trunk is None:
        return None
    return block, note, claude, session, trunk


def bind_trunk(repo):
    """The run's trunk, read once through the kit's one trunk reader and
    logged; every leg is judged against it (coordinator-2026-10-18 D-004 and
    D-005 C2). Its ref, or None after logging the reader's refusal."""
    import agent_common  # the kit's trunk reader

    try:
        name = agent_common.trunk_name(repo)
    except ValueError as exc:
        log("stop: trunk: {}".format(exc))
        return None
    log("run trunk {}".format(name))
    return HEADS + name


def run_leg(cmd, prompt, repo, out):
    """Run one leg with its prompt on stdin and its output in `out`; its exit code."""
    with out.open("w", encoding="utf-8") as fh:
        return subprocess.run(
            cmd, cwd=repo, input=prompt, encoding="utf-8", stdout=fh, stderr=subprocess.STDOUT
        ).returncode


# --- the after-leg audit and check-lane ---------------------------------------
# Every git read goes through `run_git` (a module-level callable the in-process
# tests replace) and `read`, which turns a non-zero exit into a stop: a failed
# or unparseable read is never an empty range or an empty snapshot.

HEADS = "refs/heads/"
ARCHIVE = HEADS + "archive/lanes"
SHA = r"[0-9a-f]{40}(?:[0-9a-f]{24})?"
SHA_RE = re.compile(SHA)
SNAPSHOT_LINE = re.compile(r"({}) ({}\S+)".format(SHA, HEADS))


class AuditStop(Exception):
    """A refused commit, or a read the audit could not complete."""


def run_git(repo, args):
    """(exit code, stdout, stderr) of one git command in `repo`."""
    proc = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, encoding="utf-8", errors="replace"
    )
    return proc.returncode, proc.stdout, proc.stderr


def read(repo, *args, answers=(0,)):
    """(exit code, stdout) of a git read whose exit is one of `answers`;
    AuditStop naming the read otherwise."""
    code, out, err = run_git(repo, list(args))
    if code not in answers:
        detail = (err or "").strip().splitlines()
        raise AuditStop("git {} failed (exit {}){}".format(
            " ".join(args), code, ": " + detail[0] if detail else ""))
    return code, out


def log_records(repo, *args):
    """The (sha, message) pairs of a checked `git log`, in git's order."""
    _code, out = read(repo, "log", "--format=%H%x00%B%x1e", *args)
    commits = []
    for record in out.split("\x1e"):
        record = record.lstrip("\r\n")
        if not record.strip():
            continue
        sha, nul, message = record.partition("\x00")
        if not nul or not SHA_RE.fullmatch(sha):
            raise AuditStop("unparseable record {!r} from git log {}".format(record[:60], " ".join(args)))
        commits.append((sha, message))
    return commits


def checkout_refusal(repo, trunk_ref):
    """The checkout must be on the run's trunk (coordinator-2026-10-18 D-005
    C3): its branch is compared with the bound name, never read as trunk.
    AuditStop naming what was read: a detached, unparseable or unreadable
    HEAD, or another branch."""
    code, out = read(repo, "symbolic-ref", "-q", "HEAD", answers=(0, 1))
    ref = out.strip()
    if code == 1:
        raise AuditStop("the checkout's HEAD is detached, not on the run's trunk {}".format(trunk_ref))
    if not ref.startswith(HEADS):
        raise AuditStop("unparseable branch {!r} from git symbolic-ref".format(ref))
    if ref != trunk_ref:
        raise AuditStop("the checkout is on {}, not on the run's trunk {}".format(ref, trunk_ref))


def snapshot(repo):
    """{ref: sha} for every local branch."""
    _code, out = read(repo, "for-each-ref", "--format=%(objectname) %(refname)", HEADS)
    refs = {}
    for line in out.splitlines():
        match = SNAPSHOT_LINE.fullmatch(line.strip())
        if not match:
            raise AuditStop("unparseable line {!r} from git for-each-ref".format(line))
        refs[match.group(2)] = match.group(1)
    return refs


def pre_leg(repo, trunk_ref):
    """The binding read immediately before a leg: the snapshot, which must
    hold the run's trunk, with the checkout on it."""
    refs = snapshot(repo)
    if trunk_ref not in refs:
        raise AuditStop("the run's trunk {} does not resolve before the leg".format(trunk_ref))
    checkout_refusal(repo, trunk_ref)
    return refs


def judge(commits, session, where):
    """Each commit against the run's session; the count judged."""
    from kitlib import provenance

    for sha, message in commits:
        refusal = provenance.loop_trailer_refusal(message, session)
        if refusal:
            raise AuditStop("{} holds {} - {}".format(where, sha[:10], refusal))
    return len(commits)


def judge_descent(repo, ref, pre, post, session, may_create):
    """The rule trunk and `archive/lanes` share (coordinator-2026-10-18 D-004
    and D-005 C5): a ref present before the leg must still resolve after it
    and descend from its pre-leg tip, and every commit the leg added to its
    first-parent line names the run's session. Only the archive `may_create`:
    absent before, it reads `absent`, or, created, is judged over the commits
    no pre-leg branch reaches. A summary of what was judged, or AuditStop."""
    where = ref if may_create else "trunk " + ref
    before, after = pre.get(ref), post.get(ref)
    if before is None:
        if not may_create:
            raise AuditStop("{} does not resolve before the leg".format(where))
        if after is None:
            return "absent"
        span = [after, "--not", *sorted(set(pre.values()))]
    else:
        if after is None:
            raise AuditStop("{} does not resolve after the leg; its pre-leg tip was {}".format(where, before[:10]))
        if after == before:
            return "unmoved"
        code, _out = read(repo, "merge-base", "--is-ancestor", before, after, answers=(0, 1))
        if code == 1:
            raise AuditStop("{} no longer descends from its pre-leg tip {}".format(where, before[:10]))
        span = ["{}..{}".format(before, after)]
    return "{} commit(s)".format(judge(log_records(repo, "--first-parent", *span), session, where))


LANE_FORMAT = "--format=%m%x00%H%x00%P%x00%T%x00%B%x1e"


def lane_records(repo, trunk_tip, branch):
    """The merge slot's lane read: `branch`'s `(sha, message, parents, tree)`
    records from `trunk_tip`, oldest first, and {sha: tree} for each parent
    outside the range (`--boundary`), which the re-claim's empty-tree check
    reads. A record missing a field, with a sha that is not one, or with a
    mark other than `-`, `>` or none stops the audit, naming it."""
    span = "{}..{}{}".format(trunk_tip, HEADS, branch)
    _code, out = read(repo, "log", "--reverse", "--topo-order", "--boundary", LANE_FORMAT, span)
    commits, boundary = [], {}
    for record in out.split("\x1e"):
        record = record.lstrip("\r\n")
        if not record.strip():
            continue
        fields = record.split("\x00", 4)
        if len(fields) != 5 or fields[0] not in ("-", ">", "") or not SHA_RE.fullmatch(fields[1]):
            raise AuditStop("unparseable record {!r} from git log {}".format(record[:60], span))
        mark, sha, parents, tree, message = fields
        if mark == "-":
            boundary[sha] = tree
        else:
            commits.append((sha, message, tuple(parents.split()), tree))
    return commits, boundary


def lane_refusal(repo, branch, trunk_tip):
    """The merge slot's lane rule over `branch`'s range from `trunk_tip`:
    (the first refusal or None, the window's size, None for a person's lane).
    Any well-formed session passes, as at the slot, and an attended re-claim
    closes the window as it does there (D-005 C4). The claim is read through
    the kit's one claim reader, `agent_common.loop_claimed`, the slot's own;
    a claim it cannot read is AuditStop naming the read."""
    import agent_common
    from kitlib import provenance

    commits, boundary = lane_records(repo, trunk_tip, branch)
    claimed, unreadable = agent_common.loop_claimed(repo, branch, trunk_tip)
    if unreadable:
        raise AuditStop(unreadable)
    window = provenance.loop_lane_window(commits, claimed, branch, boundary)
    for sha, message, *_shape in window or ():
        refusal = provenance.loop_trailer_refusal(message)
        if refusal:
            return "lane {} holds {} - {}".format(branch, sha[:10], refusal), len(window)
    return None, None if window is None else len(window)


def audit(repo, trunk_ref, pre, session):
    """Judge what a leg did, from the snapshot before it and one taken now:
    the run's trunk, then `archive/lanes`, then every other branch the leg
    created or moved, then the checkout, which must still be on the run's
    trunk. (A summary line, the post-leg snapshot), or AuditStop at the first
    refusal or failed read."""
    post = snapshot(repo)
    parts = [
        "trunk {}".format(judge_descent(repo, trunk_ref, pre, post, session, may_create=False)),
        "archive/lanes {}".format(judge_descent(repo, ARCHIVE, pre, post, session, may_create=True)),
    ]
    for ref in sorted(post):
        if ref in (trunk_ref, ARCHIVE) or pre.get(ref) == post[ref]:
            continue
        refusal, window = lane_refusal(repo, ref[len(HEADS):], post[trunk_ref])
        if refusal:
            raise AuditStop(refusal)
        parts.append("lane {} window {}".format(ref[len(HEADS):], "none" if window is None else window))
    deleted = sorted(ref[len(HEADS):] for ref in pre if ref not in post)
    if deleted:
        parts.append("deleted, not judged: " + ", ".join(deleted))
    checkout_refusal(repo, trunk_ref)
    return "; ".join(parts), post


def check_lane(repo, branch):
    """`check-lane`: the lane rule over `branch` at its tip now, from the tip
    of the trunk the kit's trunk reader names. 0, or 3 printing the first
    refused commit, the failed read, or the reader's refusal."""
    import agent_common  # the kit's trunk reader

    try:
        try:
            trunk_ref = HEADS + agent_common.trunk_name(repo)
        except ValueError as exc:
            raise AuditStop("trunk: {}".format(exc)) from exc
        _code, tip = read(repo, "rev-parse", "--verify", trunk_ref + "^{commit}")
        read(repo, "rev-parse", "--verify", HEADS + branch + "^{commit}")
        if not SHA_RE.fullmatch(tip.strip()):
            raise AuditStop("unparseable trunk tip {!r} from git rev-parse".format(tip.strip()))
        refusal, window = lane_refusal(repo, branch, tip.strip())
    except AuditStop as exc:
        print("check-lane {}: cannot judge - {}".format(branch, exc))
        return 3
    if refusal:
        print("check-lane {}: refused - {}".format(branch, refusal))
        return 3
    print("check-lane {}: passes (window {})".format(branch, "none, a person's lane" if window is None else window))
    return 0


def check_lane_main(argv):
    ap = argparse.ArgumentParser(prog="overnight_legs.py check-lane")
    ap.add_argument("branch")
    ap.add_argument("--repo", default=str(REPO))
    args = ap.parse_args(argv)
    repo = Path(args.repo).resolve()
    sys.path.insert(0, str(repo / "project-trajectory" / "scripts"))
    return check_lane(repo, args.branch)


def run_and_audit(repo, leg, cmd, prompt, out, session, trunk_ref):
    """Run one leg between the two ref snapshots and audit it against the
    run's trunk; 3 to stop the run, else None. The audit comes first after the
    leg exits, so a refused commit is named whatever else the leg did."""
    try:
        pre = pre_leg(repo, trunk_ref)
    except AuditStop as exc:
        log("stop: before leg {}: {}".format(leg, exc))
        return 3
    code = run_leg(cmd, prompt, repo, out)
    try:
        summary, post = audit(repo, trunk_ref, pre, session)
    except AuditStop as exc:
        log("stop: leg {} audit: {}".format(leg, exc))
        return 3
    log("leg {} audit: {}".format(leg, summary))
    log("leg {} exit {}; trunk {} -> {}".format(leg, code, pre[trunk_ref][:8], post[trunk_ref][:8]))
    if code != 0:
        log("stop: leg {} exited {}".format(leg, code))
        return 3
    return None


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    if argv[:1] == ["check-lane"]:
        return check_lane_main(argv[1:])
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(REPO))
    ap.add_argument("--max-legs", type=int, default=6)
    ap.add_argument("--model", default="claude-opus-5-5")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    repo = Path(args.repo).resolve()
    sys.path.insert(0, str(repo / "project-trajectory" / "scripts"))
    from kitlib import commit_hooks

    # The commit hooks are on before any leg (WI-926), checked before the log
    # directory exists: a refusal goes to stderr, so a first launch refuses
    # cleanly instead of failing to open a log it never made.
    refusal = commit_hooks.hooks_refusal(repo)
    if refusal is not None:
        print("stop: " + refusal, file=sys.stderr)
        return 2
    LOGDIR.mkdir(parents=True, exist_ok=True)
    import coordinator_guard  # the kit's own session-prompt reader

    prepared = prepare_run(repo)
    if prepared is None:
        return 2
    block, note, claude, session, trunk_ref = prepared
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
        prompt = leg_prompt(prompt, block, note)
        cmd = [
            claude, "-p",
            "--model", args.model,
            "--permission-mode", "bypassPermissions",
            "--settings", json.dumps(SETTINGS),
            "--output-format", "text",
        ]
        out = LOGDIR / "leg-{:02d}-{}.log".format(leg, dt.datetime.now().strftime("%Y%m%d-%H%M%S"))
        log("leg {} from {} -> {}".format(leg, handoff.name, out.name))
        if args.dry_run:
            log("dry run: would run {} -p --model {} with <{} chars> on stdin".format(
                claude, args.model, len(prompt)))
            return 0
        stop = run_and_audit(repo, leg, cmd, prompt, out, session, trunk_ref)
        if stop is not None:
            return stop
        after = newest_handoff(repo)
        log("leg {} newest handoff {}".format(leg, after.name if after else None))
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
