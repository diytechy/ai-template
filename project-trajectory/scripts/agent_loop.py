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
    AGENT_MODEL — and the COMMAND template the same way: --cmd-map /
    AGENT_CMD_MAP maps a phase to a whole template (first-class cross-provider
    routing; REVIEW-A/REVIEW-B keys are free-form), falling back to AGENT_CMD.
    docs/review-policy (the reviewer dial, 0|1|2) is surfaced in the banner;
    the loop never enforces it — review dispatch is the run-phase + status.md
    convention;
  - runs one fresh headless session (stdin closed; optional
    --session-timeout so a hung session can't wedge the loop);
  - writes the raw transcript to gitignored out/run-logs/ and a size-bounded
    head+tail copy to the tracked docs/iteration/NNN-<stamp>.log, then
    regenerates docs/iteration_index.md from the log metadata (generated,
    never hand-edited);
  - reads docs/run-state: DONE / BLOCKED / NEEDS-HUMAN exit the loop, each
    printing the pending asks from docs/status.md Current State;
  - honors docs/pause: a graceful-pause request (the file present) stops the
    loop at the next session boundary — the in-flight session finishes and
    commits normally, never a mid-session kill; deleting the file resumes;
  - honors docs/blackout: a declared `HH:MM-HH:MM` UTC weekday window inside
    which no new session starts — the in-flight one wraps normally, then the
    loop waits the window out and resumes automatically (a single launch
    survives the blackout). Absent/empty/malformed or start==end = disabled;
    the scaffold ships a 12:00–19:00 default;
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

--track <name> drives one parallel development lane (process-options.md
"Parallel tracks"): every coordination file this loop reads or writes —
run-state, run-phase, status.md (the resume excerpt), the iteration logs and
their index — resolves under docs/tracks/<name>/ instead of docs/, and the
session prompt gains a preamble redirecting the driver to that lane. The
repo-singular policies (gate, gate-policy, push-policy, privacy-check,
guardrails-policy) stay at docs/. A track must run on branch llm/<name> in its
own worktree (preflight enforces it), and a per-worktree lockfile
(out/agent-loop.lock) stops two coordinators grinding one checkout. NO --track
= single-lane operation with docs/ as the lane (the same per-worktree lock
applies there too — one coordinator per checkout).

Exit codes: 0 DONE · 2 preflight/config failure (incl. the inert unfilled
slot) · 3 BLOCKED · 4 stall abort (work stall or an all-ERROR agent-unavailable
run — the banner distinguishes them) · 5 WAITING on a rate limit · 6 iteration
budget exhausted while still RUNNING · 7 NEEDS-HUMAN (act, then re-run) · 8
paused (docs/pause present — delete it and re-run to resume).

Preflight refuses to start iteration 1 when: the AGENT_CMD executable is
missing (report, never a hang); the working directory is not a git repo; or
docs/privacy-check is enabled and the effective git author email is not in the
exempt allowlist — an unattended run under a private identity is the
history-leak disaster case (process-options.md "Commit identity & privacy").

Contracts: IF-015, IF-037, IF-041 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import atexit
import csv
import datetime
import errno
import json
import os
import re
import shlex
import shutil
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

# Sibling scripts (the S8 routing/scoring half). Run as a subprocess the loop's
# own dir is sys.path[0] so a plain import resolves; the guard covers an
# in-process import (a test) whose sys.path doesn't yet carry scripts/ — the
# same sanctioned-sibling-import idiom gen_trajectory uses.
try:
    import agent_route
    import score_reviews
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import agent_route
    import score_reviews

# Size bounds for the tracked per-session log (the Q13d "size-bounded" cap):
# the head shows how the session started, the capped tail how it ended — the
# part that explains the outcome. The raw unbounded stream goes to the
# gitignored out/run-logs/ for local debugging.
LOG_HEAD_LINES = 60
LOG_TAIL_LINES = 400
LOG_MAX_BYTES = 65536

# The end states a driver may write to docs/run-state (one word, tracked like
# docs/gate; anything else — including the file being absent — reads RUNNING).
# NEEDS-HUMAN may carry one `ask: <one-line ask>` line after the state word —
# read_ask() headlines it in the stop banner, so the console names the human
# act instead of burying it in the status excerpt (WI-127). Every state reader
# takes only the first declared line, so the extra line is invisible to them.
END_STATES = ("DONE", "BLOCKED", "NEEDS-HUMAN")

EXIT_DONE = 0
EXIT_PREFLIGHT = 2
EXIT_BLOCKED = 3
EXIT_STALL = 4
EXIT_WAITING = 5
EXIT_BUDGET = 6
EXIT_NEEDS_HUMAN = 7
EXIT_PAUSED = 8

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
    "'Needs <human>' Open item in status.md first, and follow the state word "
    "in docs/run-state with one 'ask: <the one-line ask>' line — the "
    "coordinator headlines it in its stop banner)."
)

# The dirty-tree resume note (WI-076; process-options.md "Unattended
# operation"). Prepended to the FIRST session's prompt when the loop starts on a
# non-empty working tree — residue from a prior interrupted run/session. SURFACE
# only: the loop never stashes, cleans, or blocks (that judgment stays deferred
# as WI-060); the reconcile decision belongs to the session. Kept in ONE place.
RESUME_RECONCILE_NOTE = (
    "The working tree carries uncommitted changes, likely from an interrupted "
    "session. Before starting new work, reconcile them against the open work "
    "item's spec / Done-when: verify and commit what is complete, discard what "
    "is not part of the scoped work, and record which you did in the log."
)

# The redacted reviewer prompt (S8). Ships as the embedded default for the
# REVIEW-A/REVIEW-B phases; a repo overrides it per phase with a prompt-template
# FILE via --prompt-map / AGENT_PROMPT_MAP. Redacted BY CONSTRUCTION: the
# reviewer gets the diff + the requirement surface and NEVER the implementer's
# self-assessment (leaking it collapses finding rates several-fold). No debate
# rounds — independent parallel reviews, mechanically merged. `{verdict}` is
# substituted with the repo path the reviewer must write its verdict to.
REVIEWER_PROMPT = (
    "You are an INDEPENDENT reviewer launched by the unattended coordinator "
    "(scripts/agent_loop.py) — a fresh context that did NOT write this code. "
    "Assume the implementer was careful but missed something, and hunt for it. "
    "Review ONLY (1) the diff of the work under review — run `git log` / `git "
    "diff` yourself to see it — and (2) the requirement surface it must satisfy: "
    "AGENTS.md, docs/process.md, the docs/requirements registries, and the "
    "docs/specs spec-of-record for the open work item. If this diff adds or "
    "changes requirement rows (SN/SR/TC under docs/requirements), also sweep "
    "them against the EXISTING registries — the new rows AND the historical "
    "rows they touch — for any contradiction, overlap, or attribute/limit "
    "conflict, and raise each as a finding (mark it 'for clarity' at MINOR when "
    "it is a wording ambiguity sharper SN/SR/TC language would resolve, not a "
    "defect). If the diff under review is a G1/G2 ratification (a Status-change "
    "commit closing a `[phase]-[g*]` gate), the batch-scoped ratification "
    "hierarchy is a REQUIRED input: generate it with `scripts/trace.py --ratify "
    "<phase>` and confirm the ratified SN->SR->LLR/TC batch — its Requirement/AC, "
    "LLR Detail, TC Method/Expected, and any cited rubric — is coherent and "
    "complete before endorsing the gate. Flag status.md prose that contradicts a "
    "declared policy file's current value as a finding. Do NOT read or trust the "
    "implementer's own session notes or self-assessment — a leaked "
    "self-assessment collapses review finding-rates several-fold. Run the "
    "harness yourself (python scripts/check.py, scripts/trace.py) and quote real "
    "output; believe nothing you did not observe. This is an INDEPENDENT parallel "
    "review — do not debate another reviewer. Write your verdict to {verdict} in "
    "the log.md block format: one `- [BLOCKER|MAJOR|MINOR] <file:line> -> issue "
    "-> the concrete change -> @owner` line per finding, then exactly one machine "
    "line:\n"
    "    VERDICT: APPROVE|CHANGES-REQUESTED findings=N\n"
    "Commit that verdict file (a review is a recorded verdict — its one home) and "
    "stop. Do not edit the code you are reviewing."
)

# The embedded CRITIQUE prompt (WI-068; process-options.md "Critique verification
# & the critique loop"). Ships as the default for the CRITIQUE phase; a repo
# overrides it with a prompt-template FILE via --prompt-map/AGENT_PROMPT_MAP under
# the key `CRITIQUE`. Redacted BY CONSTRUCTION like the reviewer prompt: the critic
# gets the RUBRIC + the SN/SR intent + the artifact recipe — and NEVER the
# implementer's self-assessment (status.md / log.md / session notes). `{brief}` is
# slotted with the rubric+intent+recipe block; `{verdict}` with the verdict path.
CRITIQUE_PROMPT = (
    "You are an INDEPENDENT critic launched by the unattended coordinator "
    "(scripts/agent_loop.py) — a fresh context that did NOT produce this artifact, "
    "wearing a DIFFERENT hat from the implementer. Your job is subjective-quality "
    "judgment: say WHERE and WHY the artifact is or is not good enough, judged "
    "ONLY against the WRITTEN RUBRIC below — never a fresh opinion of your own, and "
    "never a lax test case. Do NOT read or trust the implementer's session notes, "
    "docs/status.md, docs/log.md, or any self-assessment (a leaked self-assessment "
    "collapses a critic's finding rate). Produce the artifact yourself from the "
    "recipe below (agent CLIs read local images/renders natively; if your model "
    "cannot, judge the text/description proxy and SAY SO), inspect it, and score it "
    "against the rubric's numbered anchors.\n\n"
    "--- RUBRIC + SN/SR INTENT + ARTIFACT RECIPE (the only context you get) ---\n"
    "{brief}\n"
    "--- END ---\n\n"
    "Write your verdict to {verdict} in the log.md block format: one "
    "`- [BLOCKER|MAJOR|MINOR] <rubric-anchor> -> where/why it fails -> the concrete "
    "change -> @owner` line per finding, each CITING a rubric anchor id (B1/G2/…) "
    "and locating the region/aspect of the artifact it fails on. A finding that "
    "names a NEW failure mode must propose it as a new `B#` anchor for the rubric "
    "(the accumulation rule). You MAY add `- [TC-HARDEN] ...` lines proposing "
    "measurable sub-criteria — these route through change-intake (process.md §5); "
    "you NEVER edit the spine or the artifact yourself. Then exactly one machine "
    "line:\n"
    "    VERDICT: APPROVE|CHANGES-REQUESTED findings=N\n"
    "Commit that verdict file (a critique is a recorded verdict — its one home) and "
    "stop."
)

# The review-phase names the loop schedules (run-phase in {PLAN, BUILD,
# REVIEW-A, REVIEW-B, INTEGRATE}). A committing non-review session
# triggers a review round; these phases are the round.
REVIEW_PHASES = ("REVIEW-A", "REVIEW-B")

# Default phase -> tier when routing from docs/agents.csv (AGENT_TIER_MAP /
# --tier-map override per phase). Iteration reviewers are cheap-but-heterogeneous
# (the strong-model floor is a GATE-closure rule, not an iteration-loop one), the
# strong tier plans and design-checks, and an unknown phase routes UP — never a
# weaker tier (cheap is not free).
DEFAULT_PHASE_TIER = {
    "PLAN": "strong",
    "BUILD": "medium",
    "REVIEW-A": "medium",
    "REVIEW-B": "medium",
    "DESIGN-CHECK": "strong",
    # Perceptual judgment is exactly where model capability + multimodal support
    # matter (WI-068), so a critic routes strong by default (tier-up-never-down).
    "CRITIQUE": "strong",
}

# A model whose session fails to start / stalls goes on cooldown this long (its
# limit is probably exhausted) — the generalized rate-limit backoff, per-model.
# AGENT_COOLDOWN_SECONDS overrides; a bad value falls back to this default.
DEFAULT_COOLDOWN_SECONDS = 900

# Phases that are NOT build work, so a commit in them never triggers a review
# round (a reviewer's own commit, a planner, an integrator, a design-check, a
# critic writing its verdict).
NON_BUILD_PHASES = frozenset(REVIEW_PHASES) | {
    "PLAN",
    "INTEGRATE",
    "DESIGN-CHECK",
    "CRITIQUE",
}


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


def read_ask(path):
    """The optional `ask: <one-line ask>` line a driver leaves in docs/run-state
    below the NEEDS-HUMAN state word — the concrete human act the stop banner
    must headline (WI-127: a long status.md Current State can push the
    Needs-<human> items past the banner excerpt's line cap, so the ask gets its
    own dedicated line). Returns "" when absent — the legacy one-word file."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return ""
    for ln in lines:
        ln = ln.strip()
        if ln.lower().startswith("ask:"):
            return ln[4:].strip()
    return ""


def pause_reason(lane):
    """A declared **graceful-pause** request (WI-147): the `docs/pause` file
    present = pause the loop at the next session boundary. Returns the free-form
    reason (the file's first non-comment line, `""` when it carries none) or
    `None` when the file is absent. The file is the whole contract — presence
    pauses, deleting it resumes — so `run-state` is deliberately left untouched
    (a resume is one act: delete the file and re-launch). Per-lane like
    run-state, so a track pauses only its own coordinator."""
    path = lane / "pause"
    if not path.is_file():
        return None
    return read_declared(path, "")


# --- WI-148: weekday blackout window ------------------------------------------
# A declared `docs/blackout` policy: first non-comment line `HH:MM-HH:MM` (UTC),
# active Mon–Fri. Inside the window the coordinator starts no new session (the
# in-flight one already wrapped, the same graceful semantic as docs/pause) — it
# waits out the window, then resumes automatically, so a single walk-away launch
# survives the blackout. An absent/empty/malformed file, or `start == end`,
# disables it (byte-identical to a repo that never had the file — never-breaking);
# a fresh scaffold ships the 12:00–19:00 default so the owner's "always on"
# blackout is honored by the scaffold, not a hidden built-in.
BLACKOUT_RE = re.compile(r"^\s*(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})\s*$")


def parse_blackout(line):
    """Parse a `HH:MM-HH:MM` blackout line into `(start_min, end_min)` — minutes
    past UTC midnight — or `None` when absent/empty/malformed (an out-of-range
    hour or minute is malformed). Deliberately does NOT apply the `start == end`
    disable rule; the caller (blackout_wake) does, so the parse and the policy
    stay separately testable."""
    m = BLACKOUT_RE.match(line or "")
    if not m:
        return None
    sh, sm, eh, em = (int(g) for g in m.groups())
    if sh > 23 or eh > 23 or sm > 59 or em > 59:
        return None
    return (sh * 60 + sm, eh * 60 + em)


def blackout_wake(line, now):
    """Seconds until the current UTC weekday blackout window ends, or `None` when
    a new session is NOT blacked out at `now` — the file is absent/empty/
    malformed, the window is disabled (`start == end`), it is the weekend (the
    window is Mon–Fri only), or `now` falls outside the window. The window is
    half-open `[start, end)`: a session starting exactly at `end` is already
    clear (so 12:00–19:00 blocks 12:00 through 18:59 and releases at 19:00). A
    window whose start is after its end wraps past UTC midnight, honored on its
    start weekday. `now` is a naive UTC datetime (datetime.utcnow())."""
    win = parse_blackout(line)
    if win is None:
        return None
    start, end = win
    if start == end:
        return None  # the disable form
    if now.weekday() >= 5:  # Sat/Sun — the window is weekdays only
        return None
    minute = now.hour * 60 + now.minute
    inside = start <= minute < end if start < end else (minute >= start or minute < end)
    if not inside:
        return None
    wake = now.replace(hour=end // 60, minute=end % 60, second=0, microsecond=0)
    if wake <= now:  # a wrap window's end is tomorrow morning
        wake += datetime.timedelta(days=1)
    return int((wake - now).total_seconds())


def sanitize_track(name):
    """A track name becomes a lane directory segment, so restrict it to a safe
    slug — `--track` can then never traverse the tree. Returns the name or
    raises ValueError (the preflight and main both surface the message)."""
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name or ""):
        raise ValueError(
            "track name {!r} must be a lowercase slug matching "
            "[a-z0-9][a-z0-9-]* (starts alphanumeric)".format(name)
        )
    return name


def lane_dir(docs, track):
    """The coordination lane for a track: docs/tracks/<track> when a track is
    named, else docs itself — so single-lane operation uses docs/ exactly as
    before (the repo-singular policy files always stay at docs/)."""
    return (docs / "tracks" / track) if track else docs


# The per-worktree coordinator lock is a kernel ADVISORY lock (fcntl.flock on
# POSIX, msvcrt.locking on Windows) held on out/agent-loop.lock for this
# process's lifetime. The OS releases it automatically when the process exits —
# INCLUDING a crash or SIGKILL — so there is no stale-pid file to reason about
# and no PID-reuse hazard: the freed lock is simply available to the next run.
# The pid/host/stamp written into the file are human-readable DIAGNOSTICS only,
# never the liveness signal. The held descriptor lives in a module global so it
# (and thus the lock) stays open until release_lock / process exit.
_LOCK_FD = None


def _host():
    """This machine's name, for the lock file's human-readable diagnostics."""
    try:
        return socket.gethostname()
    except OSError:
        return ""


# On Windows the CRT lock is MANDATORY — it blocks other processes from reading
# the locked bytes — so we lock a single byte far beyond any real content. The
# human-readable diagnostics in bytes 0..N stay readable (e.g. git staging this
# file if a repo forgot to gitignore out/), while two coordinators still contend
# on the same byte range. POSIX flock is advisory and whole-descriptor, so it
# needs no offset games.
_WIN_LOCK_OFFSET = 1 << 40


def _take_os_lock(fd):
    """Take a non-blocking exclusive advisory lock on `fd`, raising OSError when
    another process already holds it. Platform-split, stdlib only."""
    if os.name == "nt":
        import msvcrt

        os.lseek(fd, _WIN_LOCK_OFFSET, os.SEEK_SET)
        try:
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        finally:
            os.lseek(fd, 0, os.SEEK_SET)
    else:
        import fcntl

        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)


# Errnos that mean "this filesystem cannot do advisory locks" (a network / exotic
# mount — flock returns these) as opposed to "the lock is held" (EWOULDBLOCK /
# EAGAIN / EACCES). On these we degrade to a warning instead of failing closed;
# every other error stays a refusal, so an unknown failure never silently drops
# the guard (fail-safe). Built via getattr so a name absent on a platform is just
# skipped.
_UNSUPPORTED_LOCK_ERRNOS = frozenset(
    getattr(errno, name)
    for name in ("ENOLCK", "ENOSYS", "EOPNOTSUPP", "ENOTSUP")
    if hasattr(errno, name)
)


def _read_holder(lock_path):
    """The holder's diagnostic line (pid host stamp) for an error message, or ''
    — best-effort; a mandatory Windows lock may block the read, which is fine."""
    try:
        return lock_path.read_text(encoding="utf-8").strip().replace("\n", " ")
    except OSError:
        return ""


def acquire_lock(lock_path):
    """Take the per-worktree coordinator lock, or return an error string.

    Prevents two coordinators grinding the same checkout — a double-launch or a
    cron overlap — the one collision the branch guard can't catch (both would
    sit on the same llm/<track> branch in one worktree). The lock is a kernel
    advisory lock the OS grants atomically and releases on exit *or crash*, so a
    dead run never wedges the next one (no pid reasoning, no timer). Cross-host
    on a shared filesystem is best-effort only: flock over NFS is unreliable, so
    this guards one checkout on one host — the common and important case. A
    filesystem that cannot lock at all (ENOLCK/ENOTSUP) degrades to a warning and
    runs unguarded rather than fail-closed on a legitimate run."""
    global _LOCK_FD
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_RDWR | os.O_CREAT
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY  # keep the diagnostic newlines untranslated on Windows
    fd = os.open(str(lock_path), flags, 0o644)
    try:
        _take_os_lock(fd)
    except OSError as exc:
        if os.name != "nt" and exc.errno in _UNSUPPORTED_LOCK_ERRNOS:
            # This filesystem cannot do advisory locks (a network / exotic mount).
            # Degrade to a warning and proceed WITHOUT the guard rather than block
            # a legitimate run: the single-checkout guarantee is only lost on a
            # mount that never supported it, and the branch guard + git history
            # still backstop. Keep fd open (diagnostics written below) so the file
            # still records who is here.
            print(
                "agent_loop: WARNING - {} is on a filesystem that does not "
                "support advisory locks (errno {}); running WITHOUT the "
                "one-coordinator-per-checkout guard.".format(lock_path, exc.errno),
                file=sys.stderr,
            )
        else:
            os.close(fd)
            return (
                "another coordinator holds {} — refusing to run two in one "
                "worktree (held by: {}). It clears itself when that run exits; "
                "wait for it, or delete the file only if you are sure that run "
                "is gone.".format(lock_path, _read_holder(lock_path) or "unknown")
            )
    # We hold the lock: overwrite the diagnostics (a crashed predecessor may have
    # left its own). Best-effort — the OS lock, not this content, is the guard.
    try:
        os.ftruncate(fd, 0)
        os.write(
            fd,
            "{}\n{}\n{}\n".format(
                os.getpid(), _host(), time.strftime("%Y-%m-%d %H:%M:%S")
            ).encode("utf-8"),
        )
    except OSError:
        pass
    _LOCK_FD = fd
    return None


def release_lock(lock_path=None):
    """Drop the coordinator lock: closing the descriptor releases the OS lock.
    Idempotent, and a no-op if we never held it; the OS would release on exit
    regardless (the crash path relies on exactly that). `lock_path` is accepted
    for the atexit call signature but unused — the held descriptor is the
    authority, so a reclaimed-then-exited predecessor never disturbs a successor."""
    global _LOCK_FD
    if _LOCK_FD is not None:
        try:
            os.close(_LOCK_FD)
        except OSError:
            pass
        _LOCK_FD = None


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
                                   newly added quick tier is guarded automatically.
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
    """The always-on core to prepend to a quick-tier session's prompt, or None.
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


def status_size_warning(status_path, limit):
    """A warn-only message when the resume surface outgrew one screen, or None.

    Every session inherits the lane's status.md; a bloated one is the
    file-world analogue of a full context window. Advisory
    only — the integrator's prune charter is the fix; limit <= 0 disables."""
    try:
        size = status_path.stat().st_size
    except OSError:
        return None  # no surface yet — nothing to warn about
    if limit <= 0 or size <= limit:
        return None
    return (
        "{} is {} bytes (> {}): every session inherits this resume surface — "
        "prune it to one screen (the integrator charter; evidence belongs in "
        "log.md / the iteration logs). AGENT_STATUS_WARN_BYTES tunes or "
        "silences (0) this warning.".format(status_path, size, limit)
    )


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


def phase_tier(phase, tier_map):
    """The routing tier for a run-phase: the declared --tier-map / AGENT_TIER_MAP
    value, else DEFAULT_PHASE_TIER, else `strong` (route an unknown phase UP —
    cheap is not free). Declared values are normalized — legacy `weak` reads as
    `quick` (the tier-rename alias, agent_route.normalize_tier)."""
    if phase in (tier_map or {}):
        return agent_route.normalize_tier(tier_map[phase])
    return DEFAULT_PHASE_TIER.get(phase, "strong")


def _next_wi_ids(next_wi_path):
    """The ordered WI id(s) declared in `docs/next-wi`: the value line split on
    `;` (the registry join convention) — one id is the WI-126 form, several are
    a dev-slice batch (WI-133). Empty/absent file => []."""
    line = read_declared(next_wi_path, "")
    return [w.strip() for w in line.split(";") if w.strip()]


def build_tier_pin(next_wi_path, work_items_path):
    """The per-WI starting-tier pin (WI-126). `docs/next-wi` (the declared-file
    idiom, driver-maintained alongside status.md's Next action) names the WI the
    coordinator expects to pick up next — or a `;`-joined ordered dev-slice
    BATCH (WI-133); that WI's `BuildTier` column in
    docs/requirements/work-items.csv, when set to a valid tier, is the BUILD
    session's STARTING tier in place of the phase default — the escalation
    override (tier-up-never-down) still wins AFTER it, so a pin never caps
    escalation. A batch pins the STRONGEST member BuildTier (route up, never
    down); members with no row or an empty/invalid BuildTier contribute no pin
    and are named in the loud line. Returns (tier, note): a tier to apply plus
    the loud line to log; (None, None) when nothing is pinned (absent/empty
    file, no matching row, or an empty BuildTier = the phase default,
    byte-identical to today); (None, warning) for a bad pin — an unknown WI id,
    or a BuildTier that does not normalize to a known tier — LOUD but never
    fatal, the caller falls back to the phase default."""
    ids = _next_wi_ids(next_wi_path)
    if not ids:
        return None, None
    rows = {
        (row.get("WI-ID") or "").strip(): row for row in _read_csv_rows(work_items_path)
    }
    if len(ids) == 1:
        # The WI-126 single-id contract, byte-identical (strings pinned by tests).
        wi = ids[0]
        row = rows.get(wi)
        if row is None:
            return None, (
                "docs/next-wi names {} but no such WI-ID row in "
                "docs/requirements/work-items.csv — ignoring, using the phase "
                "default".format(wi)
            )
        raw = (row.get("BuildTier") or "").strip()
        if not raw:
            return None, None  # empty BuildTier = phase default (no pin)
        tier = agent_route.normalize_tier(raw)
        if tier in agent_route.TIER_ORDER:
            return tier, (
                "BuildTier pin {} -> starting tier {} (docs/next-wi)".format(wi, tier)
            )
        return None, (
            "docs/next-wi pins {} whose BuildTier {!r} is not one of {} — "
            "ignoring, using the phase default".format(
                wi, raw, "|".join(agent_route.TIER_ORDER)
            )
        )
    # A dev-slice batch (WI-133): strongest member pin, problems named loudly.
    issues = []
    unknown = [w for w in ids if w not in rows]
    if unknown:
        issues.append("unknown WI id(s) {} ignored".format(";".join(unknown)))
    best = None  # (TIER_ORDER index, tier)
    for wi in ids:
        row = rows.get(wi)
        if row is None:
            continue
        raw = (row.get("BuildTier") or "").strip()
        if not raw:
            continue
        tier = agent_route.normalize_tier(raw)
        if tier not in agent_route.TIER_ORDER:
            issues.append("BuildTier {!r} on {} ignored".format(raw, wi))
            continue
        rank = agent_route.TIER_ORDER.index(tier)
        if best is None or rank > best[0]:
            best = (rank, tier)
    suffix = " — " + "; ".join(issues) if issues else ""
    if best:
        return best[1], (
            "BuildTier batch pin {} -> starting tier {} (strongest member; "
            "docs/next-wi){}".format(";".join(ids), best[1], suffix)
        )
    if issues:
        return None, (
            "docs/next-wi batch {}: no usable BuildTier pin — using the phase "
            "default{}".format(";".join(ids), suffix)
        )
    return None, None  # a batch with no pins = the phase default, silently


def batch_advisories(next_wi_path, work_items_path):
    """Dev-slice batch eligibility advisories (WI-133) — a batch should hold
    only INDEPENDENT, OFF-SPINE slices, but the rule is advisory: one loud line
    per violation, never fatal, never blocking (the WI-126 pin's failure
    style). Flags a spine-touching member (non-empty SR-Refs — spine slices
    review per-slice, 'series for dev') and a member hard-depending on another
    member (a mid-batch failure would strand it). Empty for a single id."""
    ids = _next_wi_ids(next_wi_path)
    if len(ids) < 2:
        return []
    rows = {
        (row.get("WI-ID") or "").strip(): row for row in _read_csv_rows(work_items_path)
    }
    idset = set(ids)
    advisories = []
    for wi in ids:
        row = rows.get(wi)
        if row is None:
            continue
        if (row.get("SR-Refs") or "").strip():
            advisories.append(
                "dev-batch advisory: {} carries SR-Refs (spine-touching) — "
                "spine slices review per-slice; split it from the batch".format(wi)
            )
        hard = [
            p.strip()
            for p in (row.get("Predecessors") or "").split(";")
            if p.strip() and not p.strip().startswith("~")
        ]
        inside = sorted(set(hard) & idset)
        if inside:
            advisories.append(
                "dev-batch advisory: {} hard-depends on batch member(s) {} — "
                "a mid-batch failure strands it; keep the order or split".format(
                    wi, ";".join(inside)
                )
            )
    return advisories


def reviewer_prompt(prompt_templates, phase, verdict_path):
    """The redacted reviewer prompt for a review phase: the per-phase prompt-map
    template (a FILE the operator wired) if present, else the embedded
    REVIEWER_PROMPT — with {verdict} resolved to the path the reviewer must
    write. Never carries the implementer's self-assessment (redaction by
    construction)."""
    base = prompt_templates.get(phase, REVIEWER_PROMPT)
    return base.replace("{verdict}", str(verdict_path))


# --- the critique loop (WI-068) ------------------------------------------------
# A `Verification=Critique` requirement's subjective acceptance is adjudicated by a
# fresh, provider-heterogeneous critic against a written rubric, never the authoring
# session. All of this is gated on managed mode + a real Critique SR, so a repo with
# neither pays nothing (never-breaking).
_SPLIT_RE = re.compile(r"[;,\s]+")
# A rubric path token as it appears in a TC's Parameters/Method cell.
RUBRIC_PATH_RE = re.compile(r"docs/rubrics/[\w./\-]+\.md")


def _read_csv_rows(path):
    """CSV rows of `path` as dicts, or [] (absent/unreadable). errors=replace so a
    stray byte degrades, never crashes (the declared-reader idiom)."""
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    return list(csv.DictReader(text.splitlines()))


def _refs(cell):
    return [t for t in _SPLIT_RE.split((cell or "").strip()) if t]


def load_critique_srs(docs):
    """The SR ids whose Verification is `Critique` (docs/requirements/
    system-requirements.csv). Empty — absent file, or no such row — makes the whole
    critique layer vacuous, exactly like an absent enable-list makes routing off."""
    out = set()
    for r in _read_csv_rows(Path(docs) / "requirements" / "system-requirements.csv"):
        sid = (r.get("SR-ID") or "").strip()
        if (
            sid
            and not sid.endswith("-000")
            and (r.get("Verification") or "").strip() == "Critique"
        ):
            out.add(sid)
    return out


def build_scope_wis(root, docs, commit_range):
    """The WI ids named in `commit_range`'s commit subjects; empty when there is
    no range or no WI-tagged subject."""
    if not commit_range or ".." not in commit_range:
        return set()
    code, subjects = git(root, "log", "--format=%s", commit_range)
    if code != 0:
        return set()
    return set(re.findall(r"WI-\d+", subjects))


def build_scope_srs(root, docs, commit_range):
    """The SR ids delivered by the WI-tagged commits in `commit_range`."""
    wi_ids = build_scope_wis(root, docs, commit_range)
    srs = set()
    for r in _read_csv_rows(Path(docs) / "requirements" / "work-items.csv"):
        if (r.get("WI-ID") or "").strip() in wi_ids:
            srs.update(_refs(r.get("SR-Refs")))
    return srs


def critique_control(docs, wi_ids, default_max):
    """Resolve the optional per-WI critique control for one build scope.

    A mixed scope uses the most conservative settings: `inf` outranks every
    integer, otherwise the largest budget wins; `block` outranks `move-on`.
    Missing/invalid cells preserve the global default and move-on behavior.
    """
    budgets, disposition = [], "move-on"
    for r in _read_csv_rows(Path(docs) / "requirements" / "work-items.csv"):
        if (r.get("WI-ID") or "").strip() not in wi_ids:
            continue
        raw = (r.get("CritiqueBudget") or "").strip().lower()
        if raw == "inf":
            budgets.append(None)
        else:
            try:
                value = int(raw)
            except ValueError:
                value = 0
            if value >= 1:
                budgets.append(value)
        if (r.get("CritiqueExhaustion") or "").strip().lower() == "block":
            disposition = "block"
    if any(value is None for value in budgets):
        return None, disposition
    return max(budgets or [default_max]), disposition


def critique_brief(root, docs, scope_srs):
    """The redacted critique brief: for each in-scope Critique SR, its intent (the
    Requirement/Rationale/AcceptanceCriteria — the SN/SR intent, never the TC), the
    verifying TC's artifact recipe (its Parameters cell), and the full text of every
    rubric the TC names. Carries rubric + intent + recipe and NOTHING from the
    implementer's session — redaction by construction."""
    docs = Path(docs)
    sr_by_id = {
        (r.get("SR-ID") or "").strip(): r
        for r in _read_csv_rows(docs / "requirements" / "system-requirements.csv")
    }
    tcs = _read_csv_rows(docs / "test" / "test-cases.csv")
    lines, rubric_paths = [], set()
    for sid in sorted(scope_srs):
        r = sr_by_id.get(sid)
        if not r:
            continue
        lines.append("### {} — {}".format(sid, (r.get("Title") or "").strip()))
        lines.append(
            "Intent (requirement): {}".format((r.get("Requirement") or "").strip())
        )
        if (r.get("Rationale") or "").strip():
            lines.append(
                "Intent (rationale / SN link): {}".format(r["Rationale"].strip())
            )
        if (r.get("AcceptanceCriteria") or "").strip():
            lines.append(
                "Acceptance intent: {}".format(r["AcceptanceCriteria"].strip())
            )
        for t in tcs:
            if sid in _refs(t.get("Verifies")):
                params = (t.get("Parameters") or "").strip()
                if params:
                    lines.append(
                        "Artifact recipe ({}): {}".format(
                            (t.get("TC-ID") or "").strip(), params
                        )
                    )
                for cell in (params, t.get("Method") or ""):
                    rubric_paths.update(RUBRIC_PATH_RE.findall(cell.replace("\\", "/")))
        lines.append("")
    for rp in sorted(rubric_paths):
        try:
            body = (
                (Path(root) / rp).read_text(encoding="utf-8", errors="replace").strip()
            )
        except OSError:
            body = "(rubric file {} is missing — write it from the SN/SR intent above)".format(
                rp
            )
        lines += ["### Rubric: {}".format(rp), body, ""]
    return "\n".join(lines).strip()


def critique_prompt(prompt_templates, verdict_path, brief):
    """The redacted critique prompt: the CRITIQUE prompt-map template (a FILE the
    operator wired) if present, else the embedded CRITIQUE_PROMPT — with {verdict}
    and {brief} resolved. Never carries the implementer's self-assessment."""
    base = prompt_templates.get("CRITIQUE", CRITIQUE_PROMPT)
    return base.replace("{verdict}", str(verdict_path)).replace("{brief}", brief)


def git(root, *args):
    """Run git in the repo; returns (returncode, stdout-stripped)."""
    proc = subprocess.run(
        ["git", "-C", str(root)] + list(args),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
    )
    return proc.returncode, (proc.stdout or "").strip()


def head_sha(root):
    """Short HEAD sha, or None on a zero-commit repo (guarded rev-parse)."""
    code, out = git(root, "rev-parse", "--short", "HEAD")
    return out if code == 0 and out else None


def working_tree_dirty(root):
    """The `git status --porcelain` lines — one per uncommitted path (a rename is
    a single 'R  old -> new' entry, an untracked file a single '?? path' entry),
    or [] on a clean tree or a non-repo. Read through git() (text,
    errors=replace) so an odd byte in a path degrades rather than crashes (the
    sibling encoding-safe idiom). Used once at loop start to surface
    interrupted-session residue (WI-076)."""
    code, out = git(root, "status", "--porcelain")
    if code != 0:
        return []
    return [ln for ln in out.splitlines() if ln.strip()]


def current_state_excerpt(status_path, max_lines=40):
    """The '## Current State' section of a status.md — the root dispatcher's or
    a track lane's own — the pending asks a stopping coordinator must surface in
    its exit banner."""
    try:
        lines = status_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return "({} not found — no asks to surface)".format(status_path)
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
        return "({} has no '## Current State' section)".format(status_path)
    section = [ln for ln in section if ln.strip()][:max_lines]
    return "\n".join(section)


def parse_json_result(output):
    """Best-effort parse of a --output-format json / stream-json run: the last
    line (or the whole output) that loads as a JSON object, preferring a
    `type: result` event — so a stream-json transcript whose tail carries a
    non-result event (a killed stream, trailing diagnostics) never shadows the
    session result. Returns {} when nothing parses."""
    candidates = [ln for ln in output.splitlines() if ln.strip()][-3:]
    dicts = []
    for text in reversed(candidates + [output.strip()]):
        try:
            data = json.loads(text)
        except ValueError:
            continue
        if isinstance(data, dict):
            dicts.append(data)
    for data in dicts:
        if data.get("type") == "result":
            return data
    return dicts[0] if dicts else {}


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
        # A named weekday is a weekly reset: if that day/time has already passed
        # today (ahead == 0, time in the past), the true reset is next week's
        # same weekday — advance by whole weeks, not one day (which would land
        # on a different weekday).
        while target <= now:
            target += datetime.timedelta(days=7)
    else:
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
        "wi",
        "model",
        "guardrails",
        "outcome",
        "commits",
        "tokens",
        "cost-usd",
        "wall-secs",
        "api-secs",
        "turns",
        "ttft-secs",
        "cache-read",
        "cache-create",
        "effort",
        "fast",
        "prompt-chars",
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
            for _ in range(32):
                line = fh.readline()
                if not line or line.startswith("# ---"):
                    break
                m = re.match(r"#\s*([\w-]+):\s*(.*)", line)
                if m:
                    meta[m.group(1)] = m.group(2).strip()
    except OSError:
        pass
    return meta


def per_turn_pace(meta):
    """API seconds per turn from a log's header meta — the like-for-like speed
    number across sessions of different lengths (a 100-turn build and a
    25-turn review compare honestly here, not on wall time). Empty when either
    field is absent (pre-WI-119 logs, errored sessions)."""
    try:
        api, turns = float(meta.get("api-secs", "")), float(meta.get("turns", ""))
    except ValueError:
        return ""
    return "{:.1f}".format(api / turns) if turns else ""


def per_turn_context(meta):
    """Average context carried per turn (cache-read tokens / turns, humanized
    to k) — the "how much is it re-reading every step" complexity number the
    per-session totals hide. Empty when the fields are absent."""
    try:
        read, turns = float(meta.get("cache-read", "")), float(meta.get("turns", ""))
    except ValueError:
        return ""
    return "{:.0f}k".format(read / turns / 1000.0) if turns else ""


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
            "| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} "
            "| [{}](iteration/{}) |".format(
                meta.get("session", ""),
                meta.get("date", ""),
                meta.get("phase", "") or "—",
                meta.get("wi", "") or "—",
                meta.get("model", "") or "—",
                meta.get("outcome", ""),
                meta.get("commits", "") or "—",
                meta.get("tokens", "") or "—",
                meta.get("cost-usd", "") or "—",
                meta.get("wall-secs", "") or "—",
                meta.get("api-secs", "") or "—",
                meta.get("turns", "") or "—",
                per_turn_pace(meta) or "—",
                per_turn_context(meta) or "—",
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
        "| # | Date | Phase | WI | Model | Outcome | Commits | Tokens | Cost USD "
        "| Wall s | API s | Turns | s/turn | Ctx/turn | Log |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n"
        + "\n".join(rows)
        + "\n"
    )
    (docs_dir / "iteration_index.md").write_text(text, encoding="utf-8")


def commit_telemetry(root, session, label, paths):
    """Commit the coordinator's own bookkeeping in its own `telemetry:` commit,
    right after it is written — so it never rides the next session's work commit
    or dangles in the tree (WI-137, the session-021 defect-shape). Stages only
    the named bookkeeping paths (the iteration log + regenerated index, the
    review scoreboard); the reviewer's verdict files commit themselves. Honors
    the hooks and is best-effort: nothing staged, or a hook veto, leaves the
    files in the tree exactly as before — never fatal, so the fix can only help
    (a walk-away run that today dangles telemetry keeps working either way)."""
    rels = []
    for p in paths:
        try:
            rels.append(os.path.relpath(str(p), str(root)))
        except ValueError:
            continue  # a path on another drive (Windows) — skip, never crash
    if not rels:
        return
    code, out = git(root, "status", "--porcelain", "--", *rels)
    if code != 0 or not out.strip():
        return  # unchanged bookkeeping — no empty commit
    code, staged = git(root, "diff", "--cached", "--name-only", "--", *rels)
    pre_staged = set(staged.splitlines()) if code == 0 else set()
    git(root, "add", "--", *rels)
    msg = "telemetry: session {} {}".format(session, label)
    code, out = git(root, "commit", "-q", "-m", msg, "--", *rels)
    if code != 0:
        # "Exactly as before" covers the index too: a veto must not leave the
        # bookkeeping staged for the next session's work commit to swallow.
        # Unstage only what this add staged; anything already staged stays.
        fresh = [r for r in rels if r.replace(os.sep, "/") not in pre_staged]
        if fresh:
            git(root, "reset", "-q", "--", *fresh)
        print(
            "agent_loop: telemetry commit skipped (session {}): {}".format(
                session, (out or "").strip()[:200] or "hook veto or nothing staged"
            ),
            file=sys.stderr,
        )


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
    track = getattr(args, "track", None)
    if track:
        try:
            sanitize_track(track)
        except ValueError as exc:
            failures.append(str(exc))
        else:
            code, branch = git(root, "branch", "--show-current")
            expected = "llm/{}".format(track)
            if code != 0 or not branch:
                # Empty/failed = detached HEAD (or git < 2.22). We cannot confirm
                # the lane, so a track run must fail CLOSED — never fall through
                # and write from an unverifiable checkout.
                failures.append(
                    "track {!r} requires branch {!r}, but this worktree's branch "
                    "could not be determined (detached HEAD, or git older than "
                    "2.22). A track drives one llm/<track> iteration branch in "
                    "one worktree (process-options.md 'Parallel tracks'); check "
                    "out that branch, or drop --track.".format(track, expected)
                )
            elif branch != expected:
                failures.append(
                    "track {!r} must run on its own branch {!r}, but this "
                    "worktree is on {!r}. A track drives one llm/<track> "
                    "iteration branch in one worktree (process-options.md "
                    "'Parallel tracks'); `git worktree add` that branch and run "
                    "there, or drop --track.".format(track, expected, branch)
                )
    return failures


def summarize_session_line(line):
    """Parse one line of session output into zero or more compact console
    summaries (WI-125) — shared by the scrolling echo (echo_session_line) and
    the in-place live line (LiveStatus, WI-136). stream-json events render as
    `  > <assistant text>` / `  * <tool name>`; result/system/user events are
    suppressed (the coordinator prints its own outcome line, and tool results
    re-echo file contents). A line that isn't a JSON event — a plain-text CLI
    like opencode — passes through as one truncated summary. Every summary is
    truncated for console hygiene; the FULL stream is still captured for the
    session log + out/run-logs regardless."""
    s = line.rstrip()
    if not s:
        return []
    if s.startswith("{"):
        try:
            evt = json.loads(s)
        except ValueError:
            evt = None
        if isinstance(evt, dict):
            out = []
            if evt.get("type") == "assistant":
                for block in (evt.get("message") or {}).get("content") or []:
                    if block.get("type") == "text" and block.get("text", "").strip():
                        txt = " ".join(block["text"].split())
                        out.append(
                            "  > {}".format(
                                txt[:240] + ("..." if len(txt) > 240 else "")
                            )
                        )
                    elif block.get("type") == "tool_use":
                        out.append("  * {}".format(block.get("name", "tool")))
            return out  # every other event type is log detail, not progress
    return [s[:240] + ("..." if len(s) > 240 else "")]


def echo_session_line(line):
    """Scrolling live echo (WI-125): print each compact summary of one output
    line so a walk-away console shows progress instead of silent minutes."""
    for summary in summarize_session_line(line):
        print(summary)


def _stdout_is_tty():
    """True only when the coordinator console is an interactive terminal — the
    gate for the in-place live line (WI-136). A pipe / redirect / CI log is not
    a TTY, so it keeps the append-only scroll (CI logs must stay append-only)."""
    try:
        return bool(sys.stdout.isatty())
    except Exception:
        return False


def _enable_windows_vt():
    """Best-effort enable of ANSI/VT escape processing for the current Windows
    console (modern conhost + Windows Terminal support it, but the flag can be
    off). stdlib-only via ctypes — no curses / colorama dependency. Returns True
    when VT is usable (always so on a non-Windows OS), False when it could not be
    turned on, so the caller falls back to the plain scroll rather than emit raw
    escape bytes (never-breaking)."""
    if os.name != "nt":
        return True
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        if not handle or handle == -1:
            return False
        mode = ctypes.c_uint()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        enable_vt = 0x0004  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
        if mode.value & enable_vt:
            return True
        return bool(kernel32.SetConsoleMode(handle, mode.value | enable_vt))
    except Exception:
        return False


class LiveStatus:
    """One in-place console status line for a workstream (WI-136). Opt-in
    (--live-status / docs/live-status) and used only when stdout is a TTY with
    VT enabled — a non-TTY keeps the scrolling echo. Each streamed event
    rewrites a single line (carriage-return + clear-to-EOL) instead of
    scrolling, so a long walk-away session shows its current step rather than
    30 silent minutes. The FULL stream is still captured for the session log +
    out/run-logs; this only changes what the console shows."""

    def __init__(self, label):
        self.label = label
        self.active = False

    def event(self, line):
        for summary in summarize_session_line(line):
            self._render(summary)

    def _render(self, summary):
        prefix = "  [{}] ".format(self.label)
        width = shutil.get_terminal_size((80, 24)).columns
        text = (prefix + " ".join(summary.split()))[: max(1, width - 1)]
        # \r to column 0, \x1b[2K to clear the whole line, then rewrite it.
        sys.stdout.write("\r\x1b[2K" + text)
        sys.stdout.flush()
        self.active = True

    def finish(self):
        """Close the live line with a newline so the next scrolling print starts
        clean — a no-op when nothing was ever rendered (an idle/errored session)."""
        if self.active:
            sys.stdout.write("\n")
            sys.stdout.flush()
            self.active = False


def run_session(argv, root, timeout, env=None, on_line=None):
    """One fresh headless driver session. Returns (exit_code, output,
    timed_out). stdin is closed so a CLI that would wait on it can't hang.

    `env` is the merged environment for a pair row that declares one (the
    registry `Env` column, already merged over os.environ by the caller); None
    means inherit the ambient environment exactly — today's call, byte for
    byte. `on_line`, when given, is called with each output line as it arrives —
    the console renderer (echo_session_line's scroll, WI-125, or LiveStatus's
    in-place line, WI-136); the returned output is the full captured stream
    either way."""
    if os.name == "nt":
        # CreateProcess resolves a bare argv[0] only to .exe/.com — never the
        # PATHEXT script shims (.cmd/.bat) npm-style CLIs install on Windows —
        # while preflight's shutil.which honors PATHEXT, so a shim-only CLI
        # passes preflight then dies here with [WinError 2] (WI-120). Hand
        # CreateProcess the which-resolved path (an explicit .cmd runs fine);
        # a miss, or a .ps1-only resolution (no CreateProcess interposition),
        # falls through unchanged to the OSError sentinel below.
        resolved = shutil.which(argv[0], path=(env or os.environ).get("PATH"))
        if resolved and not resolved.lower().endswith(".ps1"):
            argv = [resolved] + argv[1:]
    try:
        proc = subprocess.Popen(
            argv,
            cwd=str(root),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )
    except OSError as exc:
        return -1, "coordinator: session error: {}".format(exc), False
    # A reader thread pumps the pipe so the child can never block on a full
    # buffer while the main thread waits — the same shape subprocess.run uses
    # internally, opened up so each line can be echoed as it arrives.
    lines = []

    def _pump():
        for line in proc.stdout:
            lines.append(line)
            if on_line is not None:
                on_line(line)
        proc.stdout.close()

    pump = threading.Thread(target=_pump, daemon=True)
    pump.start()
    try:
        proc.wait(timeout=timeout or None)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        pump.join(5)
        return (
            -1,
            "".join(lines)
            + "\ncoordinator: session timed out after {}s".format(timeout),
            True,
        )
    pump.join(5)
    return proc.returncode, "".join(lines), False


def stop_banner(status_path, label, detail=""):
    print("\n=== coordinator stopping: {} ===".format(label))
    if detail:
        print(detail)
    print("--- pending state ({} Current State) ---".format(status_path))
    print(current_state_excerpt(status_path))
    print(
        "--- end-of-run evidence: {0} | {1} | {2} ---".format(
            status_path,
            status_path.parent / "log.md",
            status_path.parent / "iteration_index.md",
        )
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
        "--track",
        default=os.environ.get("AGENT_TRACK", "") or None,
        help="drive one parallel development lane: every coordination file "
        "(run-state, run-phase, status.md excerpt, iteration logs + index) "
        "resolves under docs/tracks/<track>/ and the session must be on branch "
        "llm/<track> in its own worktree. Omit for single-lane operation "
        "(default: the AGENT_TRACK env var). See process-options.md "
        "'Parallel tracks'.",
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
        "--cmd-map",
        default=os.environ.get("AGENT_CMD_MAP", ""),
        help='per-phase agent COMMAND template map "REVIEW-B=gemini -p '
        '{prompt},BUILD=claude -p {prompt} --model {model}" matched against '
        "docs/run-phase, falling back to the single AGENT_CMD template — "
        "first-class cross-provider routing (cross-provider "
        "dual review is the recommended review-policy 2 pairing). Same "
        "syntax/parser as --model-map, so a template must not itself contain "
        "',' or ';' — for one that does, use a thin dispatcher wrapper "
        "instead (default: AGENT_CMD_MAP env var)",
    )
    ap.add_argument(
        "--prompt-map",
        default=os.environ.get("AGENT_PROMPT_MAP", ""),
        help='per-phase prompt-template map "REVIEW-A=docs/prompts/review.md" '
        "(same KEY=value syntax as --model-map); each value is a FILE path whose "
        "content is that phase's prompt. Reviewer phases (REVIEW-A/REVIEW-B) fall "
        "back to the embedded redacted reviewer prompt when unmapped; a {verdict} "
        "slot in a reviewer template is filled with the verdict-file path. Every "
        "referenced file is preflighted before iteration 1 (default: "
        "AGENT_PROMPT_MAP env var)",
    )
    ap.add_argument(
        "--tier-map",
        default=os.environ.get("AGENT_TIER_MAP", ""),
        help='per-phase tier map "BUILD=medium,PLAN=strong" (strong|medium|quick; '
        "legacy `weak` reads as quick) "
        "used by the docs/agents.csv router when the enable-list is present; "
        "falls back to the built-in phase->tier defaults (default: AGENT_TIER_MAP "
        "env var)",
    )
    ap.add_argument(
        "--prefer-map",
        default=os.environ.get("AGENT_PREFER_MAP", ""),
        help='per-phase within-tier preference map "BUILD=OPENAI-SOL"; the '
        "preferred id is tried before docs/agents-enabled order without changing "
        "tier, and unknown/cooling ids fall through (default: AGENT_PREFER_MAP "
        "env var)",
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
        "--no-session-echo",
        action="store_true",
        help="silence the live echo of session output on the coordinator "
        "console (WI-125; the full stream is still captured to the session "
        "log and out/run-logs either way)",
    )
    ap.add_argument(
        "--live-status",
        action="store_true",
        help="upgrade the scrolling session echo to one in-place status line "
        "per workstream (WI-136) — only when stdout is a TTY (a pipe / CI log "
        "keeps the append-only scroll); also enabled by a docs/live-status "
        "file reading 'true'. Overridden by --no-session-echo.",
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
        cmd_map = parse_model_map(args.cmd_map)  # same "KEY=value" syntax
        prompt_map = parse_model_map(args.prompt_map)  # phase -> prompt-template FILE
        tier_map = parse_model_map(args.tier_map)  # phase -> tier
        prefer_map = parse_model_map(args.prefer_map)  # phase -> registry id
    except ValueError as exc:
        print("agent_loop: {}".format(exc), file=sys.stderr)
        return EXIT_PREFLIGHT

    # The S8 routing layer (process-options.md "Unattended operation" ->
    # routing/escalation). The enable-list's PRESENCE turns managed routing +
    # loop-side reviewer dispatch on; ABSENT files keep exactly today's single
    # AGENT_CMD/AGENT_MODEL behavior, so a fresh scaffold pays nothing (no silent
    # model swap — consent = the enabled set + the declared rules).
    registry, reg_errors = agent_route.load_registry(docs / "agents.csv")
    raw_enabled = agent_route.load_enabled(docs / "agents-enabled")
    # The enable-list's PRESENCE (not its resolvability) turns managed routing on
    # — an unresolvable token must fail preflight, not silently fall to legacy.
    managed = bool(raw_enabled)
    # Version-less tokens resolve to concrete pair-row ids (exact-id, else newest
    # in the Family-Model line); unresolvable tokens become preflight failures.
    tag_rank = agent_route.load_tag_rank(docs / "agents.csv")
    enabled, enable_errors = agent_route.resolve_enabled(
        raw_enabled, registry, tag_rank
    )

    failures = preflight(root, template, args)
    # Every per-phase template must be as launchable as the default one — a
    # broken REVIEW-B entry must fail before iteration 1, not at the first
    # review session mid-run (the preflight contract).
    for ph, tmpl in sorted(cmd_map.items()):
        try:
            argv = build_argv(tmpl, "model", "prompt")
            exe = argv[0]
            if not (shutil.which(exe) or Path(exe).exists()):
                failures.append(
                    "cmd-map [{}]: agent CLI not found: {!r} is not on PATH.".format(
                        ph, exe
                    )
                )
        except (ValueError, IndexError) as exc:
            failures.append("cmd-map [{}]: cannot parse template: {}".format(ph, exc))

    # Every --prompt-map entry names a prompt-template FILE that must exist and
    # be readable before iteration 1 (the preflight contract — a broken reviewer
    # prompt must fail up front, never mid-run). Read them once, here.
    prompt_templates = {}
    for ph, rel in sorted(prompt_map.items()):
        p = Path(rel)
        if not p.is_absolute():
            p = root / rel
        try:
            prompt_templates[ph] = p.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            failures.append("prompt-map [{}]: cannot read {}: {}".format(ph, p, exc))

    # Managed routing preflight (only when the enable-list opts in): the registry
    # must parse, every enabled id must resolve to a real registry row, each
    # row's CmdTemplate executable must be launchable, and any --tier-map value
    # must be a valid tier — all up front, like cmd-map.
    if managed:
        for e in reg_errors:
            failures.append("agents.csv: {}".format(e))
        for e in enable_errors:
            failures.append("agents-enabled: {}".format(e))
        for mid in enabled:
            m = registry[mid]  # resolve_enabled guarantees the id is in the registry
            try:
                exe = build_argv(m.cmd_template, "model", "prompt")[0]
                if not (shutil.which(exe) or Path(exe).exists()):
                    # The row's Notes is the declared install/sign-in hint —
                    # surface it at the earliest failure point (WI-109).
                    failures.append(
                        "agents.csv [{}]: CmdTemplate CLI {!r} is not on "
                        "PATH.{}".format(mid, exe, " — " + m.notes if m.notes else "")
                    )
            except (ValueError, IndexError) as exc:
                failures.append(
                    "agents.csv [{}]: cannot parse CmdTemplate: {}".format(mid, exc)
                )
        for ph, tier in sorted(tier_map.items()):
            # normalize_tier: the legacy `weak` value stays a valid tier-map entry.
            if agent_route.normalize_tier(tier) not in agent_route.TIER_ORDER:
                failures.append(
                    "tier-map [{}]: {!r} is not one of {}".format(
                        ph, tier, "|".join(agent_route.TIER_ORDER)
                    )
                )
        for ph, mid in sorted(prefer_map.items()):
            if not ph or not mid or not agent_route.ID_RE.match(mid):
                failures.append(
                    "prefer-map [{}]: {!r} is not a valid agent id".format(ph, mid)
                )
    elif reg_errors:
        # A malformed registry in a repo NOT using routing is only a warning —
        # the layer is off, so it changes nothing (never-breaking).
        for e in reg_errors:
            print("agent_loop: WARNING - agents.csv: {}".format(e), file=sys.stderr)

    if failures:
        print("agent_loop: preflight failed —", file=sys.stderr)
        for f in failures:
            print("  - " + f, file=sys.stderr)
        return EXIT_PREFLIGHT

    # Resolve the coordination lane. --track redirects the per-track files
    # (run-state, run-phase, status.md, iteration/) under docs/tracks/<track>/;
    # the repo-singular policy files (gate/gate-policy/push-policy/privacy-check/
    # guardrails-policy) always stay at docs/. No track = docs/ itself, so
    # single-lane operation is unchanged (preflight already slug-validated).
    track = sanitize_track(args.track) if args.track else None
    lane = lane_dir(docs, track)
    lane.mkdir(parents=True, exist_ok=True)
    status_path = lane / "status.md"
    track_preamble = ""
    if track:
        track_preamble = (
            "You are driving the '{t}' development track. Wherever the "
            "instructions below say docs/status.md, docs/plan.md, docs/run-state "
            "or docs/run-phase, use the docs/tracks/{t}/ copy instead — that "
            "lane is your resume surface and coordinator contract. Append this "
            "session's evidence to docs/tracks/{t}/log.md. Do NOT write the root "
            "docs/status.md (the cross-track dispatcher, integrator-only) or any "
            "other track's lane. The requirement registries "
            "(docs/requirements/*), docs/gate, and the root docs/log.md gate "
            "sign-offs are repo-singular and shared: propose registry changes as "
            "off-spine scope drafts for the integrator to land — never edit "
            "another lane. Stay on the llm/{t} branch (process-options.md "
            "'Parallel tracks').\n\n---\n\n"
        ).format(t=track)

    gate_policy = read_declared(docs / "gate-policy", "attended")
    push_policy = read_declared(docs / "push-policy", "human")
    review_policy = read_declared(docs / "review-policy", "1")
    _, branch = git(root, "branch", "--show-current")

    # The resume-surface size preflight (warn-only): every
    # session inherits the lane's status.md, so a bloated one is the file-world
    # version of a full context window. The integrator's charter is to prune it
    # to one screen; this is the cheap tripwire, never a gate.
    # A misconfigured AGENT_STATUS_WARN_BYTES must never crash the run this
    # warning exists to help — fall back to the default.
    try:
        warn_bytes = int(os.environ.get("AGENT_STATUS_WARN_BYTES", "8192"))
    except ValueError:
        warn_bytes = 8192
    warn = status_size_warning(lane / "status.md", warn_bytes)
    if warn:
        print("agent_loop: WARNING - " + warn, file=sys.stderr)

    def session_model():
        phase = read_declared(lane / "run-phase", "")
        return phase, model_map.get(phase, args.model)

    def session_template(phase):
        """The per-phase command template (AGENT_CMD_MAP), else AGENT_CMD —
        run-phase keys are free-form, so REVIEW-A/REVIEW-B route providers
        without any loop change."""
        return cmd_map.get(phase, template)

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
    # WI-076: set to the reconcile note (+ separator) for the FIRST session only
    # when the loop starts on a dirty tree; "" otherwise, so every other session's
    # prompt is byte-for-byte today's. The interactive path (early return above)
    # leaves this "" — a human at the keyboard already sees the tree.
    resume_reconcile = ""

    def session_prompt(model, body=None):
        """The session prompt: the track preamble (when --track redirects the
        driver to a lane) prepended to the base prompt, with the vendored
        guardrails core prepended ahead of both when docs/guardrails-policy
        selects this session's model (Thread 41). `body` overrides the default
        resume prompt (a --prompt-map template, or a redacted reviewer prompt).
        A loop-start dirty tree adds the WI-076 reconcile note ahead of the
        preamble for the first session (resume_reconcile). Returns (prompt,
        guarded); a selected-but-absent core warns once, then runs without it
        (guardrails accelerate quick tiers, they never gate a run)."""
        base = (
            resume_reconcile + track_preamble + (args.prompt if body is None else body)
        )
        if not guardrails_apply(guardrails_policy, model):
            return base, False
        core = guardrails_core(root)
        if core:
            return core + "\n\n---\n\n" + base, True
        if not warned_no_core:
            warned_no_core.append(True)
            print(
                "agent_loop: guardrails-policy={!r} selects model {!r} but "
                "docs/guardrails/core.md is absent — running without the "
                "guardrails core (vendor it per process-options.md "
                '"Tier-conditional guardrails").'.format(guardrails_policy, model),
                file=sys.stderr,
            )
        return base, False

    # WI-076: snapshot the working tree BEFORE the coordinator creates its own
    # out/agent-loop.lock (and, later, docs/iteration/*.log) — so the check sees
    # genuine interrupted-session residue, never our own artifacts. In a scaffold
    # out/ is gitignored, so the lock would not show anyway; taking the snapshot
    # first is correct regardless of a repo's .gitignore hygiene.
    start_dirty = working_tree_dirty(root)

    # One coordinator per worktree (a double-launch or cron overlap is the
    # collision the branch guard can't catch — same branch, same checkout).
    # Both the loop and a single interactive session take it; atexit drops it.
    lock_path = root / "out" / "agent-loop.lock"
    lock_err = acquire_lock(lock_path)
    if lock_err:
        print("agent_loop: {}".format(lock_err), file=sys.stderr)
        return EXIT_PREFLIGHT
    atexit.register(release_lock, lock_path)

    if args.interactive:
        phase, model = session_model()
        # Explicit interactive template wins; then the per-phase map; then the
        # default — so a REVIEW-phase interactive sitting uses the same
        # provider routing the unattended leg would.
        itemplate = (
            args.interactive_cmd
            if args.interactive_cmd is not None
            else os.environ.get("AGENT_CMD_INTERACTIVE", "") or session_template(phase)
        )
        print(
            "=== one interactive session | track={} phase={} model={} ===".format(
                track or "—", phase or "—", model or "—"
            )
        )
        argv = build_argv(itemplate, model, session_prompt(model)[0])
        proc = subprocess.run(argv, cwd=str(root))
        return proc.returncode

    print("=== unattended coordinator (scripts/agent_loop.py) ===")
    print("repo: {} | branch: {}".format(root, branch or "(none)"))
    print("track: {} | lane: {}".format(track or "(single-lane)", lane))
    print(
        "gate-policy: {} | push-policy: {} (the coordinator never pushes "
        "under 'human') | review-policy: {} (docs/review-policy — the reviewer "
        "dial: {})".format(
            gate_policy,
            push_policy,
            review_policy,
            "LOOP-ENFORCED (managed routing on) — a committing build schedules "
            "the reviewer round(s)"
            if managed
            else "surfaced here, enforced by the integrator convention, never "
            "by the loop",
        )
    )
    if managed:
        print(
            "routing: docs/agents-enabled present -> managed model selection from "
            "{} enabled of {} registry models (tier + heterogeneity + cooldown + "
            "tier-up-never-down); every selection logged before launch".format(
                len(enabled), len(registry)
            )
        )
    print(
        "guardrails-policy: {} (docs/guardrails-policy — the vendored core is "
        "injected per session when the policy selects that session's "
        "model)".format(guardrails_policy)
    )
    print("agent command: {}".format(template))
    for ph in sorted(cmd_map):
        print("  cmd-map [{}]: {}".format(ph, cmd_map[ph]))
    for ph in sorted(prompt_map):
        print("  prompt-map [{}]: {}".format(ph, prompt_map[ph]))
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
    iter_dir = lane / "iteration"
    tag = "{}-".format(track) if track else ""
    # Console rendering (WI-125 scroll / WI-136 live line). --no-session-echo
    # silences it; otherwise --live-status (or a docs/live-status file) upgrades
    # the scroll to one in-place line per workstream — but only when stdout is a
    # TTY with VT enabled, so a pipe / CI log keeps the append-only scroll
    # (never-breaking). Decided once: the TTY/VT facts don't change mid-run.
    live_status_on = (
        args.live_status
        or read_declared(docs / "live-status", "false").lower() == "true"
    )
    use_live = live_status_on and _stdout_is_tty() and _enable_windows_vt()
    stall = 0
    errors = 0  # consecutive ERROR sessions (agent unavailable, not a work stall)
    state = read_declared(lane / "run-state", "RUNNING").upper()

    # --- managed-routing / reviewer-dispatch state (S8; all no-ops when the
    # enable-list is absent, so the legacy path is byte-for-byte unchanged) ----
    try:
        rp_int = int(review_policy)
    except ValueError:
        rp_int = 1
    rp_int = max(0, min(2, rp_int))
    try:
        cooldown_seconds = int(
            os.environ.get("AGENT_COOLDOWN_SECONDS", DEFAULT_COOLDOWN_SECONDS)
        )
    except ValueError:
        cooldown_seconds = DEFAULT_COOLDOWN_SECONDS
    route_constants = agent_route.load_constants()
    scoreboard = lane / "reviews" / "scoreboard.txt"
    cooldowns = {}  # model id -> epoch it is available again (per-model backoff)
    review_queue = []  # the pending review phases for the current round
    round_verdicts = []  # (phase, Verdict, provider, model_id) collected this round
    rounds = []  # accumulated round dicts the escalation policy reads
    last_impl_family = None  # the FAMILY of the build under review (heterogeneity key)
    last_impl_wi = ""  # durable rework scope if that build's review requests changes
    last_impl_tier = "medium"  # the tier that build ran at
    impl_range = None  # the build's commit range (for the tripwire diff)
    swapped = False  # an implementer-family swap has been applied
    at_top_tier = False  # the implementer tier has been raised to the top
    impl_tier_override = None  # escalation raised the BUILD tier
    impl_exclude = set()  # families to avoid for the next BUILD (after a swap)

    # --- critique-loop state (WI-068; vacuous when no Critique SR exists) ------
    critique_srs = load_critique_srs(docs) if managed else set()
    critique_queue = []  # ["CRITIQUE"] when a critique round is scheduled
    critique_scope = set()  # the in-scope Critique SR ids for the current loop
    critique_rounds = 0  # consecutive CHANGES-REQUESTED critique rounds this scope
    critique_limit = None  # None means inf-until-APPROVE for the active scope
    critique_exhaustion = "move-on"
    try:
        critique_max = int(os.environ.get("AGENT_CRITIQUE_MAX", "3"))
    except ValueError:
        critique_max = 3
    if critique_max < 1:  # a budget is >= 1; a bad value falls back (S8-knob idiom)
        critique_max = 3
    if managed and critique_srs:
        print(
            "critique: {} Critique-verified SR(s) present -> a build touching one "
            "schedules a rubric-anchored CRITIQUE round (budget {} per scope)".format(
                len(critique_srs), critique_max
            )
        )

    # --- WI-076: surface the loop-start dirty tree (ONCE) --------------------
    # start_dirty was snapshotted before the lock (above). A non-empty tree here
    # is residue from a prior interrupted run/session: a fresh coordinator has
    # not yet written this run's own docs/iteration bookkeeping (the tracked,
    # one-session-lagging *.log + index a committing session picks up), so the
    # tree purely reflects the outside world. Per-iteration re-checking would
    # false-positive every pass on exactly that lagging bookkeeping, so
    # once-at-start is the honest scope. Surface only — one log line + a reconcile
    # note into the first session's prompt (below) — never stash/clean/block
    # (that judgment stays deferred as WI-060).
    if start_dirty:
        print(
            "agent_loop: working tree carries {} uncommitted path(s) — likely "
            "an interrupted session".format(len(start_dirty)),
            file=sys.stderr,
        )

    for i in range(1, args.max_iterations + 1):
        # WI-147: a graceful-pause request (docs/pause) stops the loop at a
        # session *boundary* — never mid-session. Checked at the top of every
        # iteration, so iteration 1 is the launch-time refusal (no session starts
        # while the file is present) and a mid-run request takes effect only after
        # the in-flight session has already finished and committed. run-state is
        # left as-is; deleting docs/pause and re-launching resumes.
        paused = pause_reason(lane)
        if paused is not None:
            because = " — reason: {}".format(paused) if paused else ""
            stop_banner(
                status_path,
                "paused (docs/pause present)",
                "a graceful-pause request is in effect{}. No new session will "
                "start; delete {} and re-run agent-resume.* to resume.".format(
                    because, lane / "pause"
                ),
            )
            return EXIT_PAUSED
        # WI-148: a declared docs/blackout window pauses NEW sessions on UTC
        # weekdays. The in-flight session already wrapped normally (the pause
        # semantic), so here we simply wait the window out and then let this
        # iteration's session start — no iteration budget is consumed by waiting
        # (we sleep inline, never `continue`), so a single walk-away launch
        # survives the blackout and resumes automatically. Absent/disabled file
        # => a no-op (byte-identical to today).
        wake = blackout_wake(
            read_declared(lane / "blackout", ""), datetime.datetime.utcnow()
        )
        if wake:
            resume_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=wake)
            print(
                "agent_loop: inside the docs/blackout window — starting no new "
                "session until {} UTC (~{}s); waiting.".format(
                    resume_at.strftime("%H:%M"), wake
                )
            )
            time.sleep(wake)
        # Inject the reconcile note into the first session's prompt only (see the
        # once-at-start rationale above); every later session's prompt is
        # unchanged from today.
        resume_reconcile = (
            RESUME_RECONCILE_NOTE + "\n\n---\n\n" if (i == 1 and start_dirty) else ""
        )
        session = "{:03d}".format(next_session_number(iter_dir))
        stamp = time.strftime("%Y%m%d-%H%M%S")
        # The WI this session claims (WI-137) — captured BEFORE the session runs,
        # since a BUILD that closes its WI rewrites docs/next-wi to the next one;
        # recorded as a `# wi:` header line + an index column. A `;`-batch value
        # (WI-133) is kept verbatim; empty when docs/next-wi is absent.
        queued_wi = read_declared(lane / "next-wi", "")
        rework_wi = read_declared(lane / "rework-wi", "")
        wi_label = rework_wi or queued_wi
        before = head_sha(root)
        now = time.time()
        is_review = False
        is_critique = False
        verdict_path = None
        route_id = None  # the selected registry id (managed mode)
        route_family = None  # the selected pair row's Family (identity, not route)
        # The launch environment: None = inherit the ambient env (today's exact
        # call); a pair row's Env is merged over os.environ below. This is how a
        # router (ANTHROPIC_BASE_URL), a second account (CLAUDE_CONFIG_DIR /
        # CODEX_HOME), or an API key (GEMINI_API_KEY) is selected declaratively.
        session_env = None
        if managed:
            if review_queue:
                phase = review_queue[0]
                is_review = True
            elif critique_queue:
                # Reviews (if any) drain first; then the perceptual critique runs
                # before the next build (WI-068).
                phase = "CRITIQUE"
                is_critique = True
            else:
                phase = read_declared(lane / "run-phase", "")
            tier = phase_tier(phase, tier_map)
            exclude = set()
            prefer_different = False
            if is_review:
                prefer_different = True
                if last_impl_family:
                    exclude.add(last_impl_family)
                for _ph, _v, fam, _mid in round_verdicts:
                    if fam:
                        exclude.add(fam)  # REVIEW-B differs from REVIEW-A too
            elif is_critique:
                # A critic wears a different hat: prefer a different FAMILY from
                # the implementer (fresh context is the invariant; degraded legal).
                prefer_different = True
                if last_impl_family:
                    exclude.add(last_impl_family)
            elif phase == "BUILD" or phase == "":
                # WI-126: a per-WI BuildTier pin (docs/next-wi -> the named WI's
                # row) sets the STARTING tier, replacing the phase default; the
                # escalation override below still wins after it (tier-up-never-
                # down), so a pin never caps escalation. A bad pin logs loud and
                # falls back to the phase default (never fatal, never silent).
                scope_pointer = lane / ("rework-wi" if rework_wi else "next-wi")
                pinned, pin_note = build_tier_pin(
                    scope_pointer, docs / "requirements" / "work-items.csv"
                )
                if pin_note:
                    print("route [{}]: {}".format(phase or "—", pin_note))
                # WI-133: dev-slice batch eligibility is advisory — loud, never
                # fatal (a spine-touching member / an intra-batch hard edge).
                for adv in batch_advisories(
                    lane / "next-wi", docs / "requirements" / "work-items.csv"
                ):
                    print("route [{}]: {}".format(phase or "—", adv))
                if pinned:
                    tier = pinned
                if impl_tier_override:
                    tier = impl_tier_override
                if impl_exclude:
                    exclude = set(impl_exclude)
                    prefer_different = True
            elif phase == "DESIGN-CHECK":
                # The autonomous page-the-human path: a fresh strong-tier session
                # from a DIFFERENT family rules grind-through vs redesign.
                prefer_different = True
                if last_impl_family:
                    exclude.add(last_impl_family)
            route_id, reason = agent_route.select(
                enabled,
                registry,
                tier,
                now,
                cooldowns,
                exclude,
                prefer_different,
                [prefer_map[phase]] if phase in prefer_map else (),
            )
            # Log the routing decision BEFORE launch (the no-silent-swap rule).
            print("route [{}]: {}".format(phase or "—", reason))
            if route_id is None:
                # Every enabled model at the preferred tier-or-stronger is cooling
                # down or none is enabled: page rather than drop to a weaker tier.
                (lane / "run-state").write_text(
                    "NEEDS-HUMAN\nask: no routable model — add/enable a model "
                    "of the required tier in docs/agents.csv, or wait out the "
                    "cooldown\n",
                    encoding="utf-8",
                )
                stop_banner(
                    status_path,
                    "NEEDS-HUMAN — no routable model",
                    reason + " (add/enable a model of this tier, or wait for a "
                    "cooldown; the loop never silently drops to a weaker tier).\n"
                    # Per-row state + the Notes cell — the declared home for the
                    # provider's sign-in/install hint (e.g. `opencode auth
                    # login`), so the page says what to DO, not just that it
                    # paged (WI-109).
                     + agent_route.pool_context(enabled, registry, cooldowns, now),
                )
                return EXIT_NEEDS_HUMAN
            m = registry[route_id]
            model = m.model or route_id
            route_family = m.family
            tmpl = m.cmd_template or template
            row_env = agent_route.parse_env(m.env)
            if row_env:
                # Only a declared Env changes the launch env — an empty Env keeps
                # the inherited environment exactly (session_env stays None).
                session_env = {**os.environ, **row_env}
            if not is_review and (phase == "BUILD" or phase == ""):
                last_impl_tier = tier
            if is_review:
                verdict_path = lane / "reviews" / "{}-{}.md".format(session, phase)
                verdict_path.parent.mkdir(parents=True, exist_ok=True)
                body = reviewer_prompt(prompt_templates, phase, verdict_path)
            elif is_critique:
                verdict_path = lane / "reviews" / "{}-CRITIQUE.md".format(session)
                verdict_path.parent.mkdir(parents=True, exist_ok=True)
                brief = critique_brief(root, docs, critique_scope)
                body = critique_prompt(prompt_templates, verdict_path, brief)
            elif phase in prompt_templates:
                body = prompt_templates[phase]
            else:
                body = None
            prompt, guarded = session_prompt(model, body=body)
            if (
                rework_wi
                and not is_review
                and not is_critique
                and phase in ("", "BUILD")
            ):
                prompt = (
                    "REWORK OVERRIDE: docs/rework-wi names {}. Rework that reviewed "
                    "scope and its recorded findings before docs/next-wi; do not advance "
                    "the backlog pointer.\n\n---\n\n{}".format(rework_wi, prompt)
                )
        else:
            phase, model = session_model()
            tmpl = session_template(phase)
            prompt, guarded = session_prompt(model)
        if not model and "{model}" in tmpl:
            print(
                "agent_loop: the session's command template carries a {model} "
                "placeholder but no model is configured for this phase "
                "(--model / --model-map / AGENT_MODEL).",
                file=sys.stderr,
            )
            return EXIT_PREFLIGHT
        print(
            "=== session {} [{}] ({}/{}) | phase={} model={} ===".format(
                session,
                track or "single",
                i,
                args.max_iterations,
                phase or "—",
                model or "—",
            )
        )
        argv = build_argv(tmpl, model, prompt)
        # The coordinator's own clock, so a duration exists even when the
        # session dies before emitting JSON (spawn failure, timeout, crash).
        wall_start = time.time()
        live = LiveStatus(track or "single") if use_live else None
        if args.no_session_echo:
            on_line = None
        elif live is not None:
            on_line = live.event
        else:
            on_line = echo_session_line
        code, output, timed_out = run_session(
            argv,
            root,
            args.session_timeout,
            env=session_env,
            on_line=on_line,
        )
        if live is not None:
            live.finish()
        wall_secs = int(round(time.time() - wall_start))

        try:
            raw_dir.mkdir(parents=True, exist_ok=True)
            (raw_dir / "{}{}-{}.log".format(tag, session, stamp)).write_bytes(
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
        # Where the wall time went: API round-trips vs local tool execution
        # (the gap is the harness running gates/tools). Blank when the CLI
        # reported no JSON result — the wall clock above still stands.
        api_ms = data.get("duration_api_ms")
        api_secs = (
            int(round(api_ms / 1000.0)) if isinstance(api_ms, (int, float)) else ""
        )
        turns = data.get("num_turns", "")
        # Session-shape telemetry (WI-124): why a session was slow, not just
        # that it was. ttft = boot-to-first-token (the initial context-ingest
        # latency); cache read/create = context volume carried per turn /
        # ingested fresh at session start; effort + fast-mode name the two
        # per-turn speed dials so their experiments are measurable per row;
        # prompt-chars sizes the instruction the coordinator composed. All
        # blank when the CLI reported no JSON (the effort/prompt pair still
        # stands — the coordinator knows what it launched).
        ttft_ms = data.get("ttft_ms")
        ttft_secs = (
            int(round(ttft_ms / 1000.0)) if isinstance(ttft_ms, (int, float)) else ""
        )
        cache_read = usage.get("cache_read_input_tokens", "")
        cache_create = usage.get("cache_creation_input_tokens", "")
        fast = data.get("fast_mode_state", "") or ""
        effort = (session_env or os.environ).get("CLAUDE_CODE_EFFORT_LEVEL", "")

        reset_hint = limit_reset_hint(output, data, code)
        after = head_sha(root)
        commits = ""
        if before != after:
            commits = "{}..{}".format(before or "(root)", after or "?")
        state = read_declared(lane / "run-state", "RUNNING").upper()

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
            "wi": wi_label,
            "model": model,
            "guardrails": "on" if guarded else "",
            "outcome": outcome,
            "commits": commits,
            "tokens": tokens,
            "cost-usd": cost,
            "wall-secs": wall_secs,
            "api-secs": api_secs,
            "turns": turns,
            "ttft-secs": ttft_secs,
            "cache-read": cache_read,
            "cache-create": cache_create,
            "effort": effort,
            "fast": fast,
            "prompt-chars": len(prompt),
            "exit-code": code,
        }
        log_path = write_session_log(iter_dir, meta, output)
        regenerate_index(lane)
        # Commit the coordinator's own bookkeeping now, in its own telemetry
        # commit — never let it ride the next session's work commit or dangle
        # (WI-137). The review scoreboard is committed at its own write below.
        commit_telemetry(
            root,
            session,
            "{} {}".format(phase or "—", outcome),
            [log_path, lane / "iteration_index.md"],
        )
        print(
            "session {}: outcome={} commits={} wall={}s{}".format(
                session,
                outcome,
                commits or "—",
                wall_secs,
                " api={}s turns={}".format(api_secs, turns) if turns != "" else "",
            )
        )

        # --- managed routing / reviewer dispatch bookkeeping (S8) -------------
        # All of this is gated on managed mode; the legacy path never enters it.
        if managed and outcome == "WAITING":
            # Generalize the rate-limit backoff PER-MODEL: cool this model and
            # re-route to another available one next iteration. select() pages if
            # none is left rather than dropping to a weaker tier (no silent swap).
            wait = seconds_until_reset(reset_hint) or cooldown_seconds
            agent_route.cool(cooldowns, route_id, now, wait)
            print(
                "route: {} rate-limited; cooled ~{}s, re-routing".format(
                    route_id, int(wait)
                )
            )
            continue
        if managed and is_review:
            if verdict_path and Path(verdict_path).exists():
                v = score_reviews.parse_verdict(
                    Path(verdict_path).read_text(encoding="utf-8", errors="replace"),
                    model=route_family,
                )
                round_verdicts.append((phase, v, route_family, route_id))
                if review_queue:
                    review_queue.pop(0)
            else:
                # No verdict file (errored, stalled, or the session simply did not
                # write one): cool the model and re-route the same review phase.
                agent_route.cool(cooldowns, route_id, now, cooldown_seconds)
                print(
                    "route: {} review [{}] wrote no verdict ({}); cooled, "
                    "re-routing".format(route_id, phase, outcome)
                )
            if not review_queue and round_verdicts:
                verdicts = [v for (_ph, v, _p, _m) in round_verdicts]
                merged, contradiction = score_reviews.merge_verdict(verdicts)
                # Substance/corroboration key on Family (who trained it), so a
                # cross-family overlap outweighs a same-family one; the scoreboard
                # tallies by that same Family key.
                family_substance = {}
                subs = []
                for j, (_ph, rv, rfam, _mid) in enumerate(round_verdicts):
                    peer = (
                        round_verdicts[1 - j][1] if len(round_verdicts) == 2 else None
                    )
                    fams = (
                        (rfam, round_verdicts[1 - j][2])
                        if len(round_verdicts) == 2
                        else None
                    )
                    s = score_reviews.substance(rv, root, other=peer, providers=fams)
                    subs.append((rfam, s))
                    if rfam:
                        family_substance[rfam] = s
                margin = abs(subs[0][1] - subs[1][1]) if len(subs) == 2 else 0.0
                primary = None
                if len(subs) == 2:
                    primary = subs[0][0] if subs[0][1] >= subs[1][1] else subs[1][0]
                changed = []
                if impl_range and ".." in impl_range:
                    _rc, diff_out = git(root, "diff", "--name-only", impl_range)
                    changed = [ln for ln in diff_out.splitlines() if ln.strip()]
                fired = score_reviews.fired_tripwires(verdicts, changed_paths=changed)
                round_info = {
                    "verdict": merged or "",
                    "tier": last_impl_tier,
                    "margin": margin,
                    "primary": primary,
                    "tripwire": bool(fired),
                    "contradiction": contradiction,
                }
                rounds.append(round_info)
                try:
                    score_reviews.record_round(scoreboard, round_info, family_substance)
                except OSError:
                    pass
                # The scoreboard is coordinator-written state too — commit it in
                # its own telemetry commit the moment the round records (WI-137),
                # not on the next session's commit.
                commit_telemetry(root, session, "review scoreboard", [scoreboard])
                print(
                    "review round: merged={} margin={:.2f} tripwires={} "
                    "(advisory scoreboard {})".format(
                        merged, margin, ",".join(fired) or "none", scoreboard
                    )
                )
                decision = agent_route.escalate(
                    rounds, route_constants, swapped, at_top_tier
                )
                print(
                    "escalate: {} — {}".format(decision["action"], decision["reason"])
                )
                round_verdicts = []
                if merged == "CHANGES-REQUESTED" and last_impl_wi:
                    rework_path = lane / "rework-wi"
                    rework_path.write_text(last_impl_wi + "\n", encoding="utf-8")
                    commit_telemetry(
                        root, session, "review rework scope", [rework_path]
                    )
                    print(
                        "dispatch: CHANGES-REQUESTED -> rework override {} "
                        "outranks docs/next-wi".format(last_impl_wi)
                    )
                elif merged == "APPROVE":
                    rework_path = lane / "rework-wi"
                    if (
                        last_impl_wi
                        and rework_path.exists()
                        and read_declared(rework_path, "") == last_impl_wi
                    ):
                        rework_path.unlink()
                        commit_telemetry(
                            root, session, "review rework scope cleared", [rework_path]
                        )
                        print(
                            "dispatch: APPROVE -> cleared rework override {}".format(
                                last_impl_wi
                            )
                        )
                if decision["action"] == "page-human":
                    fa = agent_route.failure_action(gate_policy)
                    print("route/failure ({}): {}".format(fa["mode"], fa["note"]))
                    if fa["mode"] == "attended":
                        (lane / "run-state").write_text(
                            "NEEDS-HUMAN\nask: review escalation — "
                            + decision["reason"]
                            + "\n",
                            encoding="utf-8",
                        )
                        stop_banner(
                            status_path,
                            "PAGE-HUMAN — review escalation",
                            decision["reason"] + " | " + fa["note"],
                        )
                        return EXIT_NEEDS_HUMAN
                    if fa.get("design_check"):
                        (lane / "run-phase").write_text(
                            "DESIGN-CHECK\n", encoding="utf-8"
                        )
                elif decision["action"] == "swap-implementer":
                    if last_impl_family:
                        impl_exclude = {last_impl_family}
                    swapped = True
                    critique_queue = []  # the artifact will change; re-critique later
                    (lane / "run-phase").write_text("BUILD\n", encoding="utf-8")
                elif decision["action"] == "tier-up":
                    impl_tier_override = "strong"
                    at_top_tier = True
                    critique_queue = []
                    (lane / "run-phase").write_text("BUILD\n", encoding="utf-8")
                elif merged == "CHANGES-REQUESTED":
                    critique_queue = []
                    (lane / "run-phase").write_text("BUILD\n", encoding="utf-8")
        elif managed and is_critique:
            # The perceptual arbiter (WI-068): read the critic's verdict, iterate
            # BUILD<->CRITIQUE until APPROVE or the budget trips S8 escalation.
            if verdict_path and Path(verdict_path).exists():
                v = score_reviews.parse_verdict(
                    Path(verdict_path).read_text(encoding="utf-8", errors="replace"),
                    model=route_family,
                )
                critique_queue = []  # this round consumed
                merged = (v.verdict or "").upper()
                print(
                    "critique [{}]: verdict={} findings={} scope={} ({})".format(
                        route_id,
                        merged or "?",
                        len(v.findings),
                        ",".join(sorted(critique_scope)) or "—",
                        verdict_path,
                    )
                )
                if merged == "CHANGES-REQUESTED":
                    critique_rounds += 1
                    if critique_limit is not None and critique_rounds >= critique_limit:
                        # Budget exhausted -> the S8 page-the-human semantics, keyed
                        # to docs/gate-policy (same failure_action the review round
                        # uses). The critic gates iteration; the human owns final
                        # acceptance via Attest at gate closure.
                        fa = agent_route.failure_action(gate_policy)
                        print(
                            "critique/budget ({}): {} CHANGES-REQUESTED round(s) >= "
                            "{} -> page-human: {}".format(
                                fa["mode"], critique_rounds, critique_limit, fa["note"]
                            )
                        )
                        critique_rounds = 0
                        critique_scope = set()
                        if fa["mode"] == "attended" or critique_exhaustion == "block":
                            (lane / "run-state").write_text(
                                "NEEDS-HUMAN\nask: critique budget exhausted "
                                "still CHANGES-REQUESTED — review the findings "
                                "and rule\n",
                                encoding="utf-8",
                            )
                            stop_banner(
                                status_path,
                                "PAGE-HUMAN — critique budget exhausted",
                                "the critique loop hit its {}-round budget still "
                                "CHANGES-REQUESTED | {}".format(
                                    critique_limit, fa["note"]
                                ),
                            )
                            return EXIT_NEEDS_HUMAN
                        if fa.get("design_check"):
                            (lane / "run-phase").write_text(
                                "DESIGN-CHECK\n", encoding="utf-8"
                            )
                    else:
                        # Rework: back to BUILD; a re-critique schedules after the
                        # reworked build commits.
                        (lane / "run-phase").write_text("BUILD\n", encoding="utf-8")
                else:  # APPROVE (or no parseable request) -> the critique loop ends
                    critique_rounds = 0
                    critique_scope = set()
            else:
                # No verdict written (errored/stalled): cool + re-critique next pass
                # (the stall guard backstops a critic that never writes one).
                agent_route.cool(cooldowns, route_id, now, cooldown_seconds)
                print(
                    "critique: {} wrote no verdict ({}); cooled, re-critiquing".format(
                        route_id, outcome
                    )
                )
        elif managed and not is_review:
            if outcome in ("ERROR", "TIMEOUT"):
                agent_route.cool(cooldowns, route_id, now, cooldown_seconds)
                # Say WHY the pool is shrinking, at the moment it shrinks — the
                # WAITING/no-verdict siblings already do; this path was silent.
                # The row's Notes carries the actionable hint (auth/install),
                # and the session log holds the full transcript (WI-109).
                note = registry[route_id].notes
                print(
                    "route: {} session outcome={} (exit {}); cooled ~{}s, "
                    "re-routing{}".format(
                        route_id,
                        outcome,
                        code,
                        int(cooldown_seconds),
                        " — " + note if note else "",
                    )
                )
            elif outcome == "COMMITTED" and phase not in NON_BUILD_PHASES:
                last_impl_family = route_family
                last_impl_wi = wi_label
                impl_range = commits
                # The review round follows the reviewer dial (S8).
                if rp_int >= 1:
                    round_verdicts = []
                    review_queue = ["REVIEW-A"] + (["REVIEW-B"] if rp_int >= 2 else [])
                    print(
                        "dispatch: review-policy {} -> scheduling review round "
                        "{}".format(rp_int, review_queue)
                    )
                # The critique round is INDEPENDENT of the review dial (WI-068): it
                # fires only when this build's WI touches a Critique-verified SR.
                # Vacuous when no Critique SR exists, so a non-adopter pays nothing.
                if critique_srs:
                    scope_wis = build_scope_wis(root, docs, commits)
                    in_scope = build_scope_srs(root, docs, commits) & critique_srs
                    if in_scope:
                        # A NEW scope starts a fresh budget; a rework of the SAME
                        # scope (a CHANGES-REQUESTED loop) preserves the count, so
                        # the budget actually bounds the loop.
                        if in_scope != critique_scope:
                            critique_rounds = 0
                        critique_limit, critique_exhaustion = critique_control(
                            docs, scope_wis, critique_max
                        )
                        critique_scope = in_scope
                        critique_queue = ["CRITIQUE"]
                        print(
                            "dispatch: build touches Critique SR(s) {} -> scheduling "
                            "CRITIQUE round (budget {}, exhaustion {})".format(
                                ",".join(sorted(in_scope)),
                                "inf" if critique_limit is None else critique_limit,
                                critique_exhaustion,
                            )
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
                status_path,
                "WAITING on a rate limit",
                "resume at: {} (re-run agent-resume.* then)".format(reset_hint),
            )
            return EXIT_WAITING

        if outcome == "DONE":
            stop_banner(status_path, "run-state=DONE")
            return EXIT_DONE
        if outcome == "BLOCKED":
            stop_banner(
                status_path,
                "run-state=BLOCKED",
                "everything remaining is in the Blocked register.",
            )
            return EXIT_BLOCKED
        if outcome == "NEEDS-HUMAN":
            # Headline the driver's own ask line (WI-127): the status excerpt
            # below is capped, and on a long Current State the Needs-<human>
            # items land past the cap — the ask must never scroll away.
            ask = read_ask(lane / "run-state")
            stop_banner(
                status_path,
                "run-state=NEEDS-HUMAN",
                (("ask: " + ask + "\n") if ask else "")
                + "the next step requires a human act — the asks below; "
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
                    status_path,
                    "STALL — agent error",
                    "{} consecutive session(s) errored before doing work "
                    "(agent unavailable / CLI or model error) — aborting. Check "
                    "the AGENT_CMD model + auth and the latest {} "
                    "log (outcome=ERROR, its exit-code); an unsupported model is "
                    "fixed by pointing --model / the model map at a live "
                    "tier.".format(errors, iter_dir),
                )
                return EXIT_STALL
            stop_banner(
                status_path,
                "STALL",
                "{} consecutive session(s) without a commit — aborting to "
                "protect the budget. See the latest {} "
                "log.".format(stall, iter_dir),
            )
            return EXIT_STALL

        if i < args.max_iterations and args.pause:
            time.sleep(args.pause)

    stop_banner(
        status_path,
        "iteration budget exhausted",
        "{} session(s) run and {} is still {} — raise "
        "--max-iterations deliberately if the run should continue.".format(
            args.max_iterations, lane / "run-state", state
        ),
    )
    return EXIT_BUDGET


if __name__ == "__main__":
    sys.exit(main())
