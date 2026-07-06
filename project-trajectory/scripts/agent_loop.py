#!/usr/bin/env python3
"""Unattended coordinator: loop fresh agent driver sessions until done.

Implements the walk-away protocol (process-options.md "Unattended operation
(walk-away runs)"): loop fresh headless driver sessions — repo text is the
only memory; each resumes from docs/status.md — until docs/run-state reaches
an end state, a stall guard trips (consecutive sessions without a commit), or
the iteration budget ceiling hits. Ported from a field-proven PowerShell
coordinator (NotHomeWrecker trigger.ps1), which this one implementation for
every platform supersedes. Stdlib only, Python 3.8+.

The agent invocation is a command template — the AGENT_CMD slot in the root
agent-resume.{cmd,sh} launchers (or --agent-cmd / the AGENT_CMD env var).
`{model}` and `{prompt}` placeholders are substituted per session; a template
without `{prompt}` gets the resume prompt appended as its final argument.
Empty template -> guidance and exit 2 (the launchers ship inert, like run.*).

CONSENT: an unattended run typically wires the agent CLI's permission-bypass
flag into AGENT_CMD — sessions then run with no permission prompts. The human
consents by filling the slot, declaring the gate policy (docs/gate-policy),
and running this; git + CI remain the enforcement floor. The banner restates
this every run.

Per session the coordinator:
  - reads docs/run-phase (optional) and picks the model: --model-map
    "PHASE=model,PHASE=model" (or AGENT_MODEL_MAP), falling back to --model /
    AGENT_MODEL;
  - runs one fresh headless session (stdin closed; optional
    --session-timeout so a hung session can't wedge the loop);
  - writes the raw transcript to gitignored out/run-logs/ and a size-bounded
    head+tail copy to the tracked docs/iteration/NNN-<stamp>.log, then
    regenerates docs/iteration_index.md from the log metadata (generated,
    never hand-edited);
  - reads docs/run-state: DONE / BLOCKED / NEEDS-HUMAN exit the loop, each
    printing the pending asks from docs/status.md Current State;
  - counts a no-commit session toward the stall guard (git HEAD unmoved) —
    except limit-hit sessions (below), which never count as a stall. A session
    that errored *before it could work* (the CLI reported is_error, or it could
    not be launched) — and is not a rate limit — is logged as ERROR rather than
    NO-COMMIT; it still counts toward the guard, but when a whole stall run was
    ERRORs the abort banner names an unavailable agent, not a work stall (an
    unsupported model is repointed by hand: --model / the model map).

Rate limits are handled reactively (plan-usage state is not scriptable): a
session whose output matches the "…limit … resets <time>" message backs off —
with --wait-on-limit N the loop sleeps until the parsed reset (when <= N
seconds) and continues; otherwise it exits with a WAITING banner naming the
resume time. Both am/pm and 24-hour reset clocks parse (the wording is
region-dependent); a hint in any other format doesn't kill a walk-away run —
with --wait-on-limit set, the loop sleeps --limit-retry-fallback seconds
(default 3600, capped at the --wait-on-limit ceiling) and retries.

--interactive boots exactly one hands-on session (stdio attached, no loop,
no capture) at the mapped tier — the "grind from a single point" entry for a
human sitting down. The template comes from --interactive-cmd / the
AGENT_CMD_INTERACTIVE env var, falling back to AGENT_CMD.

Exit codes: 0 DONE · 2 preflight/config failure (incl. the inert unfilled
slot) · 3 BLOCKED · 4 stall abort (work stall or an all-ERROR agent-unavailable
run — the banner distinguishes them) · 5 WAITING on a rate limit · 6 iteration
budget exhausted while still RUNNING · 7 NEEDS-HUMAN (act, then re-run).

Preflight refuses to start iteration 1 when: the AGENT_CMD executable is
missing (report, never a hang); the working directory is not a git repo; or
docs/privacy-check is enabled and the effective git author email is not in the
exempt allowlist — an unattended run under a private identity is the
history-leak disaster case (process-options.md "Commit identity & privacy").
"""

import argparse
import datetime
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Size bounds for the tracked per-session log (the Q13d "size-bounded" cap):
# the head shows how the session started, the capped tail how it ended — the
# part that explains the outcome. The raw unbounded stream goes to the
# gitignored out/run-logs/ for local debugging.
LOG_HEAD_LINES = 60
LOG_TAIL_LINES = 400
LOG_MAX_BYTES = 65536

# The end states a driver may write to docs/run-state (one word, tracked like
# docs/gate; anything else — including the file being absent — reads RUNNING).
END_STATES = ("DONE", "BLOCKED", "NEEDS-HUMAN")

EXIT_DONE = 0
EXIT_PREFLIGHT = 2
EXIT_BLOCKED = 3
EXIT_STALL = 4
EXIT_WAITING = 5
EXIT_BUDGET = 6
EXIT_NEEDS_HUMAN = 7

# The limit-hit message a throttled headless run returns, e.g. "You've hit
# your session limit · resets 3:45pm" / "…weekly limit · resets Mon 12:00am".
LIMIT_RE = re.compile(r"limit[^\n]*?resets?\s*[:·|-]?\s*([^\n\"'}]+)", re.I)

DEFAULT_PROMPT = (
    "You are the driver session launched by the unattended coordinator "
    "(scripts/agent_loop.py) — assume no human is watching. Read AGENTS.md, "
    "then docs/process.md and docs/process-options.md ('Unattended "
    "operation'), and resume from docs/status.md Current State under the "
    "declared docs/gate-policy. Work as far as you can this session — but "
    "where docs/plan.md exists, follow the plan/build cadence "
    "(process-options.md): in BUILD, execute the next pending block and only "
    "it; if the plan is exhausted or wrong (a finding, never a silent "
    "rework), set docs/run-phase to PLAN and stop; in PLAN, re-chunk "
    "docs/plan.md against the recent iteration_index.md rows, set run-phase "
    "to BUILD, and — budget allowing — continue straight into the first "
    "block: the bounce governs who plans, not how much one session does. "
    "Honor "
    "docs/push-policy (default: never push, even if asked) and, where the "
    "iteration-branch layer is in use, stay on the llm/ iteration branch and "
    "run its sync ritual at end states. Before stopping: commit your "
    "progress (even a Blocked-register entry is a commit); append session "
    "evidence to docs/log.md and keep docs/status.md holding only the resume "
    "point + open/blocked items; update docs/run-phase to the phase the next "
    "session should drive; and write docs/run-state — RUNNING while work "
    "remains, DONE only at the declared end state (a wrong DONE is a false "
    "green), BLOCKED when everything remaining is in the Blocked register, "
    "NEEDS-HUMAN when the next step requires a human act (state the ask as a "
    "'Needs <human>' Open item in status.md first)."
)


def read_declared(path, default):
    """Read a one-word declared-policy file (docs/gate, docs/run-state, …):
    the first non-empty, non-comment line — the same rule the git hooks and
    check_privacy.py apply — or `default` when absent/empty."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return default
    for ln in lines:
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            return ln
    return default


# The always-on guardrails core is vendored verbatim as docs/guardrails/core.md
# (the upstream CLAUDE.md); its BEGIN/END KIT CORE block is what gets injected.
KIT_CORE_RE = re.compile(
    r"<!--\s*BEGIN KIT CORE.*?<!--\s*END KIT CORE[^>]*-->", re.S | re.I
)


def guardrails_apply(policy, model):
    """Whether to inject the guardrails core for a session on `model`, under
    docs/guardrails-policy (case-insensitive). The grammar:
      - `off` / absent          -> never.
      - `all`                   -> every session.
      - `all except <sub> ...`  -> every session EXCEPT models matching a listed
                                   substring — name your frontier model(s), so a
                                   newly added weak tier is guarded automatically.
      - `<sub> [<sub> ...]`     -> an allowlist: guard when the model matches ANY
                                   listed substring (e.g. `opus sonnet`).
    See process-options.md "Tier-conditional guardrails"."""
    p = (policy or "").strip().lower()
    if p in ("", "off"):
        return False
    m = (model or "").lower()
    toks = p.split()
    if toks[0] == "all":
        excepts = toks[2:] if len(toks) >= 2 and toks[1] == "except" else []
        return not any(x in m for x in excepts)
    return any(t in m for t in toks)


def guardrails_core(root):
    """The always-on core to prepend to a weak-tier session's prompt, or None.
    Vendored verbatim as docs/guardrails/core.md; the BEGIN/END KIT CORE block is
    extracted when present, else the whole file. Absent -> None (the caller warns
    once and runs without it — guardrails accelerate, they are not a gate)."""
    try:
        text = (root / "docs" / "guardrails" / "core.md").read_text(encoding="utf-8")
    except OSError:
        return None
    m = KIT_CORE_RE.search(text)
    return (m.group(0) if m else text).strip()


def guardrails_inert(policy, models):
    """True when a *guarding* policy (not off / bare all) would guard none of the
    models a run could use — a stale/mistyped allowlist, or an `all except` that
    excludes every configured model. Used only to warn; off/`all` never inert."""
    p = (policy or "").strip().lower()
    if p in ("", "off", "all"):
        return False
    return not any(guardrails_apply(policy, m) for m in models)


def split_cmd(template):
    """Split a command template into tokens, quote-aware but with backslash
    escaping disabled so Windows paths survive (shlex's posix escape rules
    would eat C:\\path separators)."""
    lex = shlex.shlex(template, posix=True)
    lex.whitespace_split = True
    lex.escape = ""
    lex.commenters = ""
    return list(lex)


def build_argv(template, model, prompt):
    """Substitute {model}/{prompt} per token (never through a shell, so the
    multi-line prompt needs no quoting); append the prompt when the template
    carries no {prompt} placeholder."""
    argv = []
    saw_prompt = False
    for tok in split_cmd(template):
        if "{prompt}" in tok:
            saw_prompt = True
        argv.append(tok.replace("{model}", model).replace("{prompt}", prompt))
    if not saw_prompt:
        argv.append(prompt)
    return argv


def parse_model_map(spec):
    """ "P0=model-a,G3=model-b" -> {"P0": "model-a", "G3": "model-b"}."""
    mapping = {}
    for pair in (spec or "").replace(";", ",").split(","):
        pair = pair.strip()
        if not pair:
            continue
        if "=" not in pair:
            raise ValueError("--model-map entry without '=': {}".format(pair))
        phase, _, model = pair.partition("=")
        mapping[phase.strip()] = model.strip()
    return mapping


def git(root, *args):
    """Run git in the repo; returns (returncode, stdout-stripped)."""
    proc = subprocess.run(
        ["git", "-C", str(root)] + list(args),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    return proc.returncode, (proc.stdout or "").strip()


def head_sha(root):
    """Short HEAD sha, or None on a zero-commit repo (guarded rev-parse)."""
    code, out = git(root, "rev-parse", "--short", "HEAD")
    return out if code == 0 and out else None


def current_state_excerpt(root, max_lines=40):
    """The '## Current State' section of docs/status.md — the pending asks a
    stopping coordinator must surface in its exit banner."""
    status = root / "docs" / "status.md"
    try:
        lines = status.read_text(encoding="utf-8").splitlines()
    except OSError:
        return "(docs/status.md not found — no asks to surface)"
    section, collecting = [], False
    for ln in lines:
        if ln.startswith("## "):
            if collecting:
                break
            collecting = ln.strip().lower().startswith("## current state")
            continue
        if collecting:
            section.append(ln)
    if not section:
        return "(docs/status.md has no '## Current State' section)"
    section = [ln for ln in section if ln.strip()][:max_lines]
    return "\n".join(section)


def parse_json_result(output):
    """Best-effort parse of a --output-format json run: the last line (or the
    whole output) that loads as a JSON object. Returns {} when none does."""
    candidates = [ln for ln in output.splitlines() if ln.strip()][-3:]
    for text in reversed(candidates + [output.strip()]):
        try:
            data = json.loads(text)
        except ValueError:
            continue
        if isinstance(data, dict):
            return data
    return {}


def limit_reset_hint(output, data, exit_code):
    """The 'resets <time>' text of a rate-limit message, or None.

    Only an *error* is eligible (the JSON result's is_error, or a nonzero
    session exit for plain-text templates) — a healthy transcript merely
    *mentioning* limits must never read as a throttle."""
    if data:
        if not data.get("is_error"):
            return None
        m = LIMIT_RE.search(str(data.get("result", ""))) or LIMIT_RE.search(output)
    elif exit_code != 0:
        m = LIMIT_RE.search(output)
    else:
        return None
    return m.group(1).strip().rstrip(".") if m else None


def seconds_until_reset(hint, now=None):
    """Best-effort seconds until a reset hint like '3:45pm', '10am',
    'Mon 12:00am', '14:30' or 'Tue 09:00' — both am/pm and 24-hour clocks,
    since the message wording is locale-dependent. None when unparseable —
    the caller then sleeps the --limit-retry-fallback (when waiting is
    enabled) or exits WAITING with the raw hint in the banner."""
    if not hint:
        return None
    now = now or datetime.datetime.now()
    m = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b", hint, re.I)
    if m:
        hour, minute = int(m.group(1)) % 12, int(m.group(2) or 0)
        if m.group(3).lower() == "pm":
            hour += 12
    else:
        m = re.search(r"\b(\d{1,2}):(\d{2})(?::\d{2})?\b", hint)
        if not m:
            return None
        hour, minute = int(m.group(1)), int(m.group(2))
        if hour > 23 or minute > 59:
            return None
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    days = re.search(r"\b(mon|tue|wed|thu|fri|sat|sun)", hint, re.I)
    if days:
        wanted = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"].index(
            days.group(1).lower()
        )
        ahead = (wanted - target.weekday()) % 7
        target += datetime.timedelta(days=ahead)
    while target <= now:
        target += datetime.timedelta(days=1)
    return int((target - now).total_seconds())


def bounded_transcript(output):
    """Head + capped tail of a session transcript (the tracked-log bound)."""
    lines = output.splitlines()
    if len(lines) > LOG_HEAD_LINES + LOG_TAIL_LINES:
        elided = len(lines) - LOG_HEAD_LINES - LOG_TAIL_LINES
        lines = (
            lines[:LOG_HEAD_LINES]
            + [
                "",
                "[... {} line(s) elided — full stream in out/run-logs/ ...]".format(
                    elided
                ),
                "",
            ]
            + lines[-LOG_TAIL_LINES:]
        )
    text = "\n".join(lines)
    encoded = text.encode("utf-8", "replace")
    if len(encoded) > LOG_MAX_BYTES:
        keep = LOG_MAX_BYTES // 2
        text = (
            encoded[:keep].decode("utf-8", "ignore")
            + "\n[... byte cap hit — full stream in out/run-logs/ ...]\n"
            + encoded[-keep:].decode("utf-8", "ignore")
        )
    return text


def write_session_log(iter_dir, meta, transcript):
    """Write the tracked, size-bounded per-session log: a `# key: value`
    metadata header (what the index is regenerated from) + the transcript."""
    iter_dir.mkdir(parents=True, exist_ok=True)
    header = ["# agent-loop session log — written by scripts/agent_loop.py"]
    for key in (
        "session",
        "date",
        "phase",
        "model",
        "guardrails",
        "outcome",
        "commits",
        "tokens",
        "cost-usd",
        "exit-code",
    ):
        header.append("# {}: {}".format(key, meta.get(key, "")))
    header.append("# ---")
    path = iter_dir / "{}-{}.log".format(meta["session"], meta["stamp"])
    path.write_text(
        "\n".join(header) + "\n" + bounded_transcript(transcript) + "\n",
        encoding="utf-8",
    )
    return path


def read_log_meta(path):
    """Parse the `# key: value` metadata header of one session log."""
    meta = {}
    try:
        with open(str(path), encoding="utf-8", errors="replace") as fh:
            for _ in range(16):
                line = fh.readline()
                if not line or line.startswith("# ---"):
                    break
                m = re.match(r"#\s*([\w-]+):\s*(.*)", line)
                if m:
                    meta[m.group(1)] = m.group(2).strip()
    except OSError:
        pass
    return meta


def regenerate_index(docs_dir):
    """Rebuild docs/iteration_index.md from the docs/iteration/*.log metadata
    headers — generated, never hand-maintained (the kit's standing rule), so
    it survives manual log pruning and answers "which session did this"."""
    iter_dir = docs_dir / "iteration"
    rows = []
    for log in sorted(iter_dir.glob("*.log")):
        meta = read_log_meta(log)
        if not meta.get("session"):
            continue
        rows.append(
            "| {} | {} | {} | {} | {} | {} | {} | {} | [{}](iteration/{}) |".format(
                meta.get("session", ""),
                meta.get("date", ""),
                meta.get("phase", "") or "—",
                meta.get("model", "") or "—",
                meta.get("outcome", ""),
                meta.get("commits", "") or "—",
                meta.get("tokens", "") or "—",
                meta.get("cost-usd", "") or "—",
                log.name,
                log.name,
            )
        )
    text = (
        "# Iteration index\n\n"
        "_Generated by `scripts/agent_loop.py` from the `docs/iteration/*.log`\n"
        "metadata headers — regenerated every session, never hand-edited. The\n"
        "collated human-review record is `log.md`; this index is the quick\n"
        '"which session did this" pointer (process-options.md "Unattended\n'
        'operation")._\n\n'
        "| # | Date | Phase | Model | Outcome | Commits | Tokens | Cost USD | Log |\n"
        "|---|---|---|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n"
    )
    (docs_dir / "iteration_index.md").write_text(text, encoding="utf-8")


def next_session_number(iter_dir):
    """Next NNN, continuing across coordinator restarts."""
    highest = 0
    if iter_dir.is_dir():
        for log in iter_dir.glob("*.log"):
            m = re.match(r"(\d+)-", log.name)
            if m:
                highest = max(highest, int(m.group(1)))
    return highest + 1


def preflight(root, template, args):
    """Refuse to start iteration 1 on a broken footing. Returns the list of
    failures (empty = go)."""
    failures = []
    if not template.strip():
        failures.append(
            "no agent command wired yet: fill the AGENT_CMD slot in "
            "agent-resume.cmd + agent-resume.sh (or pass --agent-cmd / set "
            "the AGENT_CMD env var). Example:\n"
            "    claude -p {prompt} --model {model} --output-format json "
            "--dangerously-skip-permissions\n"
            "  The permission-bypass flag is YOUR consent to unattended "
            "edits; leave it out to be prompted."
        )
        return failures  # nothing else is checkable without a command
    try:
        argv = build_argv(template, "model", "prompt")
    except ValueError as exc:
        failures.append("cannot parse AGENT_CMD: {}".format(exc))
        return failures
    exe = argv[0]
    if not (shutil.which(exe) or Path(exe).exists()):
        failures.append(
            "agent CLI not found: {!r} is not on PATH. Install it (or fix "
            "AGENT_CMD), then re-run.".format(exe)
        )
    code, _ = git(root, "rev-parse", "--git-dir")
    if code != 0:
        failures.append(
            "{} is not a git repository — the loop reads commits as its "
            "progress signal.".format(root)
        )
    else:
        enabled = (
            read_declared(root / "docs" / "privacy-check", "false").lower() == "true"
        )
        if enabled:
            # Single-source the exempt allowlist: let check_privacy.py judge the
            # author email (it self-skips when the gate is off, so this fails
            # only on a genuinely private author on a privacy-checked repo).
            proc = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).resolve().parent / "check_privacy.py"),
                    "--root",
                    str(root),
                    "--author",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            if proc.returncode != 0:
                failures.append(
                    "privacy-check author identity violated: an unattended run "
                    "would commit every session under a private identity. "
                    + (proc.stderr or proc.stdout or "").strip()
                )
    return failures


def run_session(argv, root, timeout):
    """One fresh headless driver session. Returns (exit_code, output,
    timed_out). stdin is closed so a CLI that would wait on it can't hang."""
    try:
        proc = subprocess.run(
            argv,
            cwd=str(root),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            timeout=timeout or None,
        )
        return proc.returncode, proc.stdout or "", False
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or ""
        if isinstance(out, bytes):
            out = out.decode("utf-8", "replace")
        return (
            -1,
            out + "\ncoordinator: session timed out after {}s".format(timeout),
            True,
        )
    except OSError as exc:
        return -1, "coordinator: session error: {}".format(exc), False


def stop_banner(root, label, detail=""):
    print("\n=== coordinator stopping: {} ===".format(label))
    if detail:
        print(detail)
    print("--- pending state (docs/status.md Current State) ---")
    print(current_state_excerpt(root))
    print(
        "--- end-of-run evidence: docs/status.md | docs/log.md | docs/iteration_index.md ---"
    )


def _utf8_console():
    """Emit UTF-8 whatever the OS console codepage is (bootstrap.py's guard):
    session transcripts echoed into findings can carry any characters."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--root",
        default=str(Path(__file__).resolve().parent.parent),
        help="repo root (default: this script's parent's parent)",
    )
    ap.add_argument(
        "--agent-cmd",
        default=None,
        help="agent command template ({model}/{prompt} placeholders); "
        "default: the AGENT_CMD env var (set by the agent-resume launchers)",
    )
    ap.add_argument(
        "--interactive",
        action="store_true",
        help="boot exactly one hands-on session (stdio attached) instead of "
        "the unattended loop",
    )
    ap.add_argument(
        "--interactive-cmd",
        default=None,
        help="command template for --interactive; default: the "
        "AGENT_CMD_INTERACTIVE env var, else AGENT_CMD",
    )
    ap.add_argument(
        "--max-iterations",
        type=int,
        default=40,
        help="hard budget ceiling; raise deliberately (default 40)",
    )
    ap.add_argument(
        "--stall-limit",
        type=int,
        default=3,
        help="consecutive no-commit sessions before abort (default 3)",
    )
    ap.add_argument(
        "--model",
        default=os.environ.get("AGENT_MODEL", ""),
        help="default model tier for {model} (default: AGENT_MODEL env var)",
    )
    ap.add_argument(
        "--model-map",
        default=os.environ.get("AGENT_MODEL_MAP", ""),
        help='per-phase tier map "P0=strong-model,G3=strong-model" matched '
        "against docs/run-phase (default: AGENT_MODEL_MAP env var)",
    )
    ap.add_argument(
        "--prompt",
        default=DEFAULT_PROMPT,
        help="resume prompt passed to each session (default: the kit's "
        "resume-from-status.md prompt)",
    )
    ap.add_argument(
        "--session-timeout",
        type=int,
        default=0,
        help="per-session timeout in seconds so a hung session can't wedge "
        "the loop (0 = none)",
    )
    ap.add_argument(
        "--pause",
        type=int,
        default=10,
        help="seconds between sessions (default 10)",
    )
    ap.add_argument(
        "--wait-on-limit",
        type=int,
        default=0,
        help="on a rate-limit hit, sleep until the parsed reset when it is "
        "<= this many seconds and continue; otherwise (and by default) exit "
        "with a WAITING banner naming the resume time",
    )
    ap.add_argument(
        "--limit-retry-fallback",
        type=int,
        default=3600,
        help="with --wait-on-limit: when the reset time can't be parsed "
        "(am/pm and 24-hour clocks are recognized; other wordings are not), "
        "sleep this many seconds and retry instead of exiting — capped at "
        "the --wait-on-limit ceiling (default 3600)",
    )
    args = ap.parse_args()

    root = Path(args.root).resolve()
    docs = root / "docs"
    template = (
        args.agent_cmd
        if args.agent_cmd is not None
        else os.environ.get("AGENT_CMD", "")
    )
    try:
        model_map = parse_model_map(args.model_map)
    except ValueError as exc:
        print("agent_loop: {}".format(exc), file=sys.stderr)
        return EXIT_PREFLIGHT

    failures = preflight(root, template, args)
    if failures:
        print("agent_loop: preflight failed —", file=sys.stderr)
        for f in failures:
            print("  - " + f, file=sys.stderr)
        return EXIT_PREFLIGHT

    gate_policy = read_declared(docs / "gate-policy", "attended")
    push_policy = read_declared(docs / "push-policy", "human")
    _, branch = git(root, "branch", "--show-current")

    def session_model():
        phase = read_declared(docs / "run-phase", "")
        return phase, model_map.get(phase, args.model)

    guardrails_policy = read_declared(docs / "guardrails-policy", "off")
    # Surface a stale/typo'd policy token before the run: if it names a substring
    # that matches none of the models this run could use, the guard is inert.
    possible_models = {m for m in [args.model, *model_map.values()] if m}
    if guardrails_inert(guardrails_policy, possible_models):
        print(
            "agent_loop: WARNING - guardrails-policy {!r} would guard none of "
            "the configured models ({}); the guard is inert — fix the token or "
            'the model map (process-options.md "Tier-conditional guardrails").'.format(
                guardrails_policy, ", ".join(sorted(possible_models)) or "none"
            ),
            file=sys.stderr,
        )
    warned_no_core = []

    def session_prompt(model):
        """The session prompt, with the vendored guardrails core prepended when
        docs/guardrails-policy selects this session's model (Thread 41). Returns
        (prompt, guarded); a selected-but-absent core warns once, then runs
        without it (guardrails accelerate weak tiers, they never gate a run)."""
        if not guardrails_apply(guardrails_policy, model):
            return args.prompt, False
        core = guardrails_core(root)
        if core:
            return core + "\n\n---\n\n" + args.prompt, True
        if not warned_no_core:
            warned_no_core.append(True)
            print(
                "agent_loop: guardrails-policy={!r} selects model {!r} but "
                "docs/guardrails/core.md is absent — running without the "
                "guardrails core (vendor it per process-options.md "
                '"Tier-conditional guardrails").'.format(guardrails_policy, model),
                file=sys.stderr,
            )
        return args.prompt, False

    if args.interactive:
        itemplate = (
            args.interactive_cmd
            if args.interactive_cmd is not None
            else os.environ.get("AGENT_CMD_INTERACTIVE", "") or template
        )
        phase, model = session_model()
        print(
            "=== one interactive session | phase={} model={} ===".format(
                phase or "—", model or "—"
            )
        )
        argv = build_argv(itemplate, model, session_prompt(model)[0])
        proc = subprocess.run(argv, cwd=str(root))
        return proc.returncode

    print("=== unattended coordinator (scripts/agent_loop.py) ===")
    print("repo: {} | branch: {}".format(root, branch or "(none)"))
    print(
        "gate-policy: {} | push-policy: {} (the coordinator never pushes "
        "under 'human')".format(gate_policy, push_policy)
    )
    print(
        "guardrails-policy: {} (docs/guardrails-policy — the vendored core is "
        "injected per session when the policy selects that session's "
        "model)".format(guardrails_policy)
    )
    print("agent command: {}".format(template))
    print(
        "CONSENT: sessions run headless; a permission-bypass flag in "
        "AGENT_CMD means unattended edits without prompts — you consented by "
        "wiring it and running this. Ctrl+C is safe; re-running resumes."
    )
    privacy_on = read_declared(docs / "privacy-check", "false").lower() == "true"
    if privacy_on and not (branch or "").startswith("llm/"):
        print(
            "WARNING: privacy-checked repo (docs/privacy-check) but the "
            "current branch {!r} is not an llm/ iteration branch — see "
            'process-options.md "Agent iteration branch & sync".'.format(
                branch or "(none)"
            )
        )

    raw_dir = root / "out" / "run-logs"
    iter_dir = docs / "iteration"
    stall = 0
    errors = 0  # consecutive ERROR sessions (agent unavailable, not a work stall)
    state = read_declared(docs / "run-state", "RUNNING").upper()
    for i in range(1, args.max_iterations + 1):
        session = "{:03d}".format(next_session_number(iter_dir))
        stamp = time.strftime("%Y%m%d-%H%M%S")
        before = head_sha(root)
        phase, model = session_model()
        if not model and "{model}" in template:
            print(
                "agent_loop: AGENT_CMD carries a {model} placeholder but no "
                "model is configured for this phase (--model / --model-map / "
                "AGENT_MODEL).",
                file=sys.stderr,
            )
            return EXIT_PREFLIGHT
        print(
            "=== session {} ({}/{}) | phase={} model={} ===".format(
                session, i, args.max_iterations, phase or "—", model or "—"
            )
        )
        prompt, guarded = session_prompt(model)
        argv = build_argv(template, model, prompt)
        code, output, timed_out = run_session(argv, root, args.session_timeout)

        try:
            raw_dir.mkdir(parents=True, exist_ok=True)
            (raw_dir / "{}-{}.log".format(session, stamp)).write_bytes(
                output.encode("utf-8", "replace")
            )
        except OSError:
            pass  # the raw stream is debug convenience, never load-bearing

        data = parse_json_result(output)
        tokens = ""
        usage = data.get("usage") or {}
        if (
            usage.get("input_tokens") is not None
            or usage.get("output_tokens") is not None
        ):
            tokens = "{}+{}".format(
                usage.get("input_tokens", 0), usage.get("output_tokens", 0)
            )
        cost = data.get("total_cost_usd", "")

        reset_hint = limit_reset_hint(output, data, code)
        after = head_sha(root)
        commits = ""
        if before != after:
            commits = "{}..{}".format(before or "(root)", after or "?")
        state = read_declared(docs / "run-state", "RUNNING").upper()

        # A session that failed *before it could work* — and is not a rate limit
        # (that wins as WAITING) or a timeout (its own outcome): the CLI reported
        # an error result (is_error in JSON), or a non-JSON session exited nonzero
        # — which also covers run_session's OSError sentinel (-1, no JSON) when it
        # could not launch at all. Distinct from NO-COMMIT (a healthy session that
        # idled), so a fast-dying walk-away run — model retired, auth expired, CLI
        # broke — reads as an agent error, not a work stall. Mirrors the error
        # signal limit_reset_hint already trusts (is_error / nonzero exit), never
        # a substring scan of the transcript. Reporting only: it still counts
        # toward the stall guard (no commit), but the abort banner names it
        # (Thread 45).
        errored = (
            not reset_hint
            and not timed_out
            and (bool(data.get("is_error")) or (not data and code != 0))
        )

        if reset_hint:
            outcome = "WAITING"
        elif timed_out:
            outcome = "TIMEOUT"
        elif state in END_STATES:
            outcome = state
        elif before != after:
            outcome = "COMMITTED"
        elif errored:
            outcome = "ERROR"
        else:
            outcome = "NO-COMMIT"

        meta = {
            "session": session,
            "stamp": stamp,
            "date": time.strftime("%Y-%m-%d %H:%M"),
            "phase": phase,
            "model": model,
            "guardrails": "on" if guarded else "",
            "outcome": outcome,
            "commits": commits,
            "tokens": tokens,
            "cost-usd": cost,
            "exit-code": code,
        }
        write_session_log(iter_dir, meta, output)
        regenerate_index(docs)
        print(
            "session {}: outcome={} commits={}".format(session, outcome, commits or "—")
        )

        if outcome == "WAITING":
            # A throttled session is not progress *or* a stall — never count
            # it toward the stall guard (three throttled sessions would
            # otherwise misread as a stall and abort, the NHW original's bug).
            wait = seconds_until_reset(reset_hint)
            if args.wait_on_limit and wait is None:
                # Unrecognized reset wording (locale/format drift): a bounded
                # fallback nap keeps the walk-away run alive, capped at the
                # ceiling the human already consented to waiting.
                wait = min(args.limit_retry_fallback, args.wait_on_limit)
                print(
                    "rate limit hit — reset time {!r} not recognized; "
                    "sleeping {}s (--limit-retry-fallback) and retrying.".format(
                        reset_hint, wait
                    )
                )
                time.sleep(wait)
                continue
            if args.wait_on_limit and wait and wait <= args.wait_on_limit:
                print(
                    "rate limit hit — sleeping {}s until the reset ({}).".format(
                        wait, reset_hint
                    )
                )
                time.sleep(wait)
                continue
            stop_banner(
                root,
                "WAITING on a rate limit",
                "resume at: {} (re-run agent-resume.* then)".format(reset_hint),
            )
            return EXIT_WAITING

        if outcome == "DONE":
            stop_banner(root, "run-state=DONE")
            return EXIT_DONE
        if outcome == "BLOCKED":
            stop_banner(
                root,
                "run-state=BLOCKED",
                "everything remaining is in the Blocked register.",
            )
            return EXIT_BLOCKED
        if outcome == "NEEDS-HUMAN":
            stop_banner(
                root,
                "run-state=NEEDS-HUMAN",
                "the next step requires a human act — the asks below; "
                "re-run agent-resume.* after acting.",
            )
            return EXIT_NEEDS_HUMAN

        if before == after:
            stall += 1
        else:
            stall = 0
        errors = errors + 1 if outcome == "ERROR" else 0
        if stall >= args.stall_limit:
            if errors >= args.stall_limit:
                # Every session that tripped the guard errored before working —
                # an unavailable agent, not a stuck task. Name it so, and point
                # at the fix (an unsupported model is repointed by hand).
                stop_banner(
                    root,
                    "STALL — agent error",
                    "{} consecutive session(s) errored before doing work "
                    "(agent unavailable / CLI or model error) — aborting. Check "
                    "the AGENT_CMD model + auth and the latest docs/iteration/ "
                    "log (outcome=ERROR, its exit-code); an unsupported model is "
                    "fixed by pointing --model / the model map at a live "
                    "tier.".format(errors),
                )
                return EXIT_STALL
            stop_banner(
                root,
                "STALL",
                "{} consecutive session(s) without a commit — aborting to "
                "protect the budget. See the latest docs/iteration/ "
                "log.".format(stall),
            )
            return EXIT_STALL

        if i < args.max_iterations and args.pause:
            time.sleep(args.pause)

    stop_banner(
        root,
        "iteration budget exhausted",
        "{} session(s) run and docs/run-state is still {} — raise "
        "--max-iterations deliberately if the run should continue.".format(
            args.max_iterations, state
        ),
    )
    return EXIT_BUDGET


if __name__ == "__main__":
    sys.exit(main())
