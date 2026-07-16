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
  - picks the model per the in-process phase: --model-map
    "PHASE=model,PHASE=model" (or AGENT_MODEL_MAP), falling back to --model /
    AGENT_MODEL — and the COMMAND template the same way: --cmd-map /
    AGENT_CMD_MAP maps a phase to a whole template (first-class cross-provider
    routing; REVIEW-A/REVIEW-B keys are free-form), falling back to AGENT_CMD.
    The phase is runtime state (review/critique queues + the build/design-check
    default), never a tracked docs/run-phase file (retired WI-180). docs/review-
    policy (the reviewer dial, 0|1|2) is surfaced in the banner; the loop never
    enforces it — review dispatch is the managed-mode + status.md convention;
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

--jobs N|auto (or the AGENT_JOBS env) launches the PARALLEL DISPATCHER
(WI-182, SR-061; docs/specs/parallel-wi-dispatch.md §4): reconcile owned
trains -> gate -> build-out. It derives the ready frontier from the WI
registry via schedule.py (declared SafetyClass required — unclassified fails
closed), packs it into traincars (ordinary unary chains cluster up to the
cap; spine/gate/protected serialize whole-project with every other lane
drained), atomically reserves each selected traincar's constituent WIs
(refs/llm/reservations/WI-### — one commit-tree metadata commit + one
update-ref --stdin zero-old-value transaction, all-or-none), leases a linked
worktree per train (../<repo>-trains/<id>), and runs Slice-C workers in
parallel up to the ceiling, rescanning on every worker exit (dynamic refill —
never a static wave). A built train parks ready-to-integrate with its
reservations held for the integrator (Slice F); docs/pause stops new
reservations at the next boundary while in-flight workers finish;
out/dispatch/ is a rebuildable journal/cache, never authority (§11); root
docs/run-state becomes a generated dispatcher outcome. --jobs 1 is the
explicit serial mode. Absent --jobs/AGENT_JOBS keeps today's legacy resume
loop. The two-worker promotion is GATED (WI-186, SR-065): a repo holds at
--jobs 1 until its SafetyClass audit (every open WI classified) AND soft-edge
audit (signed via docs/parallel-ready) pass — a fresh scaffold passes by
construction — and every launch emits reason-coded telemetry (run/train/WI/
session aggregation) + a lanes/frontier/queue/ceiling banner.

--wi/--train run one WORKER ASSIGNMENT (WI-181, SR-060; the parallel-dispatch
contract docs/specs/parallel-wi-dispatch.md §6): an explicit, dispatcher-supplied
traincar — the ordered `--wi "WI-###[;WI-###…]"` list built on train branch
llm/train/<train> in the worktree named by --worktree (default --root), from the
integration base --base. A worker has NO lane files: it never reads or writes
run-state/status.md/pause/next-wi and never regenerates generated root artifacts
(the integrator owns them) — its prompt is assembled from AGENTS.md, the WI row,
its SpecRef, predecessor context, the current train diff, and any --rework
finding, and its RESULT is committed evidence: each WI's final commit carries
`WI:`/`Train:`/`Base:` trailers (a blocker commits `Blocked-WI:` + `BlockRef:`
instead and the worker exits 3). Session logs are collision-safe
(docs/iteration/<train>-NNN-*.log) and review verdicts land at
docs/reviews/<train>/NNN-<PHASE>-<sha7>.md naming the exact reviewed commit, so
parallel workers never collide. A traincar is ONE review scope (WI-183,
SR-062): under managed routing + review-policy >= 1 the round is scheduled
once, after the LAST assigned WI commits, over the combined base..HEAD train
diff — intermediate constituents are accepted-on-train, not reviewed. Before
each successor the §7 continuation conditions are re-checked: a constituent
the classifier no longer permits in a multi-WI grouping ends the train EARLY
(exit 10) — built evidence stands and the dispatcher transactionally releases
the unstarted constituents' reservations. Exit 0 = every assigned WI built
(and its one review cycle approved).

--track <name> drives one parallel development lane (process-options.md
"Parallel tracks"): every coordination file this loop reads or writes —
run-state, status.md (the resume excerpt), the iteration logs and
their index — resolves under docs/tracks/<name>/ instead of docs/, and the
session prompt gains a preamble redirecting the driver to that lane. The
repo-singular policies (gate, gate-policy, push-policy, privacy-check,
guardrails-policy) stay at docs/. A track must run on branch llm/<name> in its
own worktree (preflight enforces it), and a per-worktree lockfile
(out/agent-loop.lock) stops two coordinators grinding one checkout. NO --track
= single-lane operation with docs/ as the lane (the same per-worktree lock
applies there too — one coordinator per checkout). --track is DEPRECATED
(WI-181, one compatibility window): the dispatcher's explicit --wi/--train
worker assignment replaces long-lived tracks; legacy behavior is unchanged
meanwhile and a deprecation warning is printed.

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

Contracts: IF-015, IF-037, IF-041, IF-055 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
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
    import schedule
    import score_reviews
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import agent_route
    import schedule
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
# A worker whose §7 continuation re-check refuses the next constituent ends
# its train EARLY (WI-183, SR-062): built/blocked evidence stands, and the
# dispatcher transactionally releases the unstarted constituents' reservations.
EXIT_TRAIN_END = 10

# The limit-hit message a throttled headless run returns, e.g. "You've hit
# your session limit · resets 3:45pm" / "…weekly limit · resets Mon 12:00am".
LIMIT_RE = re.compile(r"limit[^\n]*?resets?\s*[:·|-]?\s*([^\n\"'}]+)", re.I)

DEFAULT_PROMPT = (
    "You are the driver session launched by the unattended coordinator "
    "(scripts/agent_loop.py) — assume no human is watching. Read AGENTS.md, "
    "then docs/process.md and docs/process-options.md ('Unattended "
    "operation'), and resume from docs/status.md Current State under the "
    "declared docs/gate-policy. Work as far as you can this session — where "
    "docs/plan.md exists, execute the next pending block and only it; if the "
    "plan is exhausted or wrong, re-chunk docs/plan.md against the recent "
    "iteration_index.md rows before continuing (a finding, never a silent "
    "rework). "
    "Honor "
    "docs/push-policy (default: never push, even if asked) and, where the "
    "iteration-branch layer is in use, stay on the llm/ iteration branch and "
    "run its sync ritual at end states. Before stopping: commit your "
    "progress (even a Blocked-register entry is a commit); append session "
    "evidence to docs/log.md and keep docs/status.md holding only the resume "
    "point + open/blocked items; and write docs/run-state — RUNNING while work "
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

# The worker-assignment prompt (WI-181, SR-060). Assembled per session from the
# WI row + SpecRef + predecessor context + train diff + rework finding — NEVER
# from docs/status.md (not a resume surface) or docs/next-wi (retired). The
# format slots are filled by worker_prompt(); the trailer protocol is the
# worker's ONLY result channel (committed evidence, spec §6 — workers have no
# lane-local run-state).
WORKER_PROMPT = (
    "You are a worker session launched by the parallel dispatcher "
    "(scripts/agent_loop.py --wi/--train) — assume no human is watching. You "
    "are assigned ONE work item on ONE train branch; this assignment is your "
    "whole scope. Read AGENTS.md first, then the SpecRef and SR rows below — "
    "they are the spec of record.\n"
    "\n"
    "Assignment:\n"
    "- WI: {wi} — {title}\n"
    "- SR-Refs: {srs} | SpecRef: {specref}\n"
    "- Train: {train} (branch llm/train/{train}; integration base {base})\n"
    "{pred_block}{diff_block}{rework_block}"
    "\n"
    "Rules (the parallel-dispatch worker contract, "
    "docs/specs/parallel-wi-dispatch.md §6):\n"
    "- Work ONLY the assigned WI. Do not resume from docs/status.md and do not "
    "look for docs/next-wi (retired) — the assignment above is authoritative.\n"
    "- Run the declared harness (docs/stack.ini) and keep it green; commit "
    "coherent progress. End your FINAL commit for this WI with the trailers:\n"
    "    WI: {wi}\n"
    "    Train: {train}\n"
    "    Base: {base}\n"
    "- NEVER edit root coordination truth on this branch: docs/status.md, "
    "docs/run-state, docs/log.md, the Status/Deliverable cells of "
    "docs/requirements/work-items.csv, or generated artifacts "
    "(docs/iteration_index.md, dashboards, generated maps). The integrator "
    "regenerates them on the composed tree at integration.\n"
    "- If the WI cannot proceed for a non-predecessor reason, commit the "
    "evidence you have with the trailers `Blocked-WI: {wi}` and `BlockRef: "
    "<OI-N | spec anchor | named external condition>` INSTEAD of the WI "
    "trailer, and stop."
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

# The review-phase names the loop schedules (the in-process phase in {PLAN,
# BUILD, REVIEW-A, REVIEW-B, INTEGRATE}). A committing non-review session
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


# --- WI-181: explicit worker assignment (SR-060) --------------------------------
# A worker is one agent_loop process driving one dispatcher-assigned traincar on
# one llm/train/<id> branch in one worktree. Its inputs are explicit CLI
# arguments (never a lane file) and its result is committed evidence read back
# through git trailers — the durable channel recovery reconstructs from (spec
# §6/§11).

# The branch namespace a train builds on. The dispatcher (Slice D) creates these.
TRAIN_BRANCH_PREFIX = "llm/train/"

WI_TOKEN_RE = re.compile(r"^WI-\d+$")


def sanitize_train(name):
    """A train id becomes a branch segment, a log-file prefix, and a reviews/
    subdirectory, so restrict it to a safe slug (alnum + `.`/`-`/`_`, starts
    alphanumeric) — `--train` can then never traverse the tree. Returns the
    name or raises ValueError (preflight surfaces the message)."""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name or ""):
        raise ValueError(
            "train id {!r} must be a slug matching [A-Za-z0-9][A-Za-z0-9._-]* "
            "(starts alphanumeric; no path separators)".format(name)
        )
    return name


def parse_wi_list(spec):
    """The ordered assigned-WI list from a `;`/`,`/whitespace-joined --wi value.
    Raises ValueError on an empty list, a malformed token, or a duplicate —
    a broken assignment must fail preflight, never half-run."""
    out = []
    for tok in re.split(r"[;,\s]+", (spec or "").strip()):
        if not tok:
            continue
        if not WI_TOKEN_RE.match(tok):
            raise ValueError(
                "--wi token {!r} is not a WI-### id (got --wi {!r})".format(tok, spec)
            )
        if tok in out:
            raise ValueError("--wi names {} twice".format(tok))
        out.append(tok)
    if not out:
        raise ValueError("--wi carries no WI-### id (got {!r})".format(spec))
    return out


def load_wi_registry(root):
    """{WI-ID: raw row dict} from the worktree's tracked WI registry — the
    checked-out copy on the train branch, so a worker reads the same registry
    state its base commit fixed. Malformed/duplicate ids are skipped (the
    validator's finding, not the worker's crash)."""
    rows = _read_csv_rows(root / "docs" / "requirements" / "work-items.csv")
    out = {}
    for r in rows:
        wid = (r.get("WI-ID") or "").strip()
        if WI_TOKEN_RE.match(wid) and wid not in out:
            out[wid] = r
    return out


def train_evidence(root, base):
    """(built, blocked) read from the train branch's committed trailers in
    base..HEAD: `built` is the set of WI ids whose final commit carried the
    `WI:` trailer; `blocked` maps a `Blocked-WI:` id to its `BlockRef:` value
    (empty string when the commit omitted one). This is the worker's one
    result channel — recovery reconstructs the same facts from git alone."""
    # The leading "T" sentinel keeps the first field intact through git()'s
    # stdout .strip() — a commit whose WI field is empty would otherwise lose
    # its leading tab and shift every field left.
    fmt = (
        "T%x09"
        "%(trailers:key=WI,valueonly,separator=;)%x09"
        "%(trailers:key=Blocked-WI,valueonly,separator=;)%x09"
        "%(trailers:key=BlockRef,valueonly,separator=;)"
    )
    code, out = git(root, "log", "--format=" + fmt, "{}..HEAD".format(base))
    built, blocked = set(), {}
    if code != 0:
        return built, blocked
    for line in out.splitlines():
        parts = (line.split("\t")[1:] + ["", "", ""])[:3]
        for tok in parts[0].split(";"):
            tok = tok.strip()
            if WI_TOKEN_RE.match(tok):
                built.add(tok)
        refs = [t.strip() for t in parts[2].split(";")]
        for j, tok in enumerate(t.strip() for t in parts[1].split(";")):
            if WI_TOKEN_RE.match(tok) and tok not in blocked:
                blocked[tok] = refs[j] if j < len(refs) else ""
    return built, blocked


def _clip(text, limit):
    """Bound a prompt block: head lines up to `limit`, with an elision marker."""
    lines = (text or "").splitlines()
    if len(lines) <= limit:
        return "\n".join(lines)
    return "\n".join(lines[:limit] + ["… ({} more lines)".format(len(lines) - limit)])


def worker_prompt(root, wi_rows, wi, train, base, rework_text=""):
    """The per-session worker prompt (SR-060): the WI row + SpecRef +
    predecessor context + the current train diff + any rework finding, slotted
    into WORKER_PROMPT. Reads NOTHING from docs/status.md or docs/next-wi —
    the explicit assignment is the whole scope."""
    row = wi_rows.get(wi, {})

    preds = []
    for tok in re.split(r"[;,\s]+", (row.get("Predecessors") or "").strip()):
        tok = tok.lstrip("~")
        if tok and WI_TOKEN_RE.match(tok):
            p = wi_rows.get(tok)
            if p is not None:
                deliverable = (p.get("Deliverable") or "").strip()
                if len(deliverable) > 200:
                    deliverable = deliverable[:200] + "…"
                preds.append(
                    "  - {} [{}] {}{}".format(
                        tok,
                        (p.get("Status") or "?").strip(),
                        (p.get("Title") or "").strip(),
                        " — " + deliverable if deliverable else "",
                    )
                )
    pred_block = (
        "- Hard predecessors (context, already integrated or accepted on this "
        "train):\n" + "\n".join(preds) + "\n"
        if preds
        else ""
    )

    _c1, log_out = git(
        root, "log", "--oneline", "--no-decorate", "{}..HEAD".format(base)
    )
    _c2, stat_out = git(root, "diff", "--name-status", "{}..HEAD".format(base))
    diff_block = (
        "- Current train diff ({}..HEAD — earlier WIs on this train, accepted "
        "but not yet reviewed/integrated):\n{}\n{}\n".format(
            base[:7], _clip(log_out, 30), _clip(stat_out, 60)
        )
        if log_out.strip()
        else ""
    )

    rework_block = (
        "- REWORK FINDING (address this before anything else):\n{}\n".format(
            _clip(rework_text.strip(), 80)
        )
        if (rework_text or "").strip()
        else ""
    )

    return WORKER_PROMPT.format(
        wi=wi,
        title=(row.get("Title") or "(row missing from the registry)").strip(),
        srs=(row.get("SR-Refs") or "—").strip() or "—",
        specref=(row.get("SpecRef") or "—").strip() or "—",
        train=train,
        base=base,
        pred_block=pred_block,
        diff_block=diff_block,
        rework_block=rework_block,
    )


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


def parse_map(spec):
    """Parse a KEY=value phase map — shared by --model-map/--cmd-map/--prompt-map/
    --tier-map/--prefer-map: "P0=model-a,G3=model-b" -> {"P0": "model-a",
    "G3": "model-b"}."""
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
    """The routing tier for a phase: the declared --tier-map / AGENT_TIER_MAP
    value, else DEFAULT_PHASE_TIER, else `strong` (route an unknown phase UP —
    cheap is not free). Declared values are normalized — legacy `weak` reads as
    `quick` (the tier-rename alias, agent_route.normalize_tier)."""
    if phase in (tier_map or {}):
        return agent_route.normalize_tier(tier_map[phase])
    return DEFAULT_PHASE_TIER.get(phase, "strong")


def reviewer_prompt(prompt_templates, phase, verdict_path):
    """The redacted reviewer prompt for a review phase: the per-phase prompt-map
    template (a FILE the operator wired) if present, else the embedded
    REVIEWER_PROMPT — with {verdict} resolved to the path the reviewer must
    write. Never carries the implementer's self-assessment (redaction by
    construction)."""
    base = prompt_templates.get(phase, REVIEWER_PROMPT)
    return base.replace("{verdict}", str(verdict_path))


def session_model(model_map, default_model):
    """The legacy/interactive route: the tracked docs/run-phase file is retired
    (WI-180), so the phase is '' and the model the ''-keyed map entry, else the
    default."""
    return "", model_map.get("", default_model)


def session_template(cmd_map, default_template, phase):
    """The per-phase command template (AGENT_CMD_MAP), else AGENT_CMD — phase
    keys are free-form, so REVIEW-A/REVIEW-B route providers without any loop
    change."""
    return cmd_map.get(phase, default_template)


def compose_session_prompt(
    model,
    body,
    resume_reconcile,
    track_preamble,
    default_prompt,
    guardrails_policy,
    root,
    warned_no_core,
):
    """The session prompt: the track preamble (when --track redirects the
    driver to a lane) prepended to the base prompt, with the vendored
    guardrails core prepended ahead of both when docs/guardrails-policy
    selects this session's model (Thread 41). `body` overrides the default
    resume prompt (a --prompt-map template, or a redacted reviewer prompt).
    A loop-start dirty tree adds the WI-076 reconcile note ahead of the
    preamble for the first session (resume_reconcile). Returns (prompt,
    guarded); a selected-but-absent core warns once, then runs without it
    (guardrails accelerate quick tiers, they never gate a run). warned_no_core
    is a shared mutable list used as the warn-once flag across calls."""
    base = (
        resume_reconcile + track_preamble + (default_prompt if body is None else body)
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
        "train",
        "base",
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
    # A worker's log name is prefixed with its train id (WI-181): two parallel
    # workers' committed session logs must never collide at integration.
    name = "{}-{}.log".format(meta["session"], meta["stamp"])
    if meta.get("train"):
        name = "{}-{}".format(meta["train"], name)
    path = iter_dir / name
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


def next_session_number(iter_dir, train=None):
    """Next NNN, continuing across coordinator restarts. A worker's numbering
    is scoped to its train prefix (WI-181) — parallel session numbers cannot
    collide because the (train, session) pair is the aggregation key."""
    pattern = re.compile(r"{}-(\d+)-".format(re.escape(train)) if train else r"(\d+)-")
    highest = 0
    if iter_dir.is_dir():
        for log in iter_dir.glob("*.log"):
            m = pattern.match(log.name)
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
    # --- worker assignment preflight (WI-181, SR-060) -----------------------
    wi_spec = getattr(args, "wi", None)
    train = getattr(args, "train", None)
    if bool(wi_spec) != bool(train):
        failures.append(
            "--wi and --train come as a pair (the dispatcher's explicit "
            "assignment); got {}".format(
                "--wi without --train" if wi_spec else "--train without --wi"
            )
        )
    if (wi_spec or train) and getattr(args, "track", None):
        failures.append(
            "--wi/--train (a worker assignment) and --track (a legacy lane) "
            "are mutually exclusive — a worker's lane IS its assignment."
        )
    if (wi_spec or train) and getattr(args, "interactive", False):
        failures.append(
            "--wi/--train is an unattended worker assignment; it cannot be "
            "combined with --interactive."
        )
    if wi_spec and train and not failures:
        try:
            assigned = parse_wi_list(wi_spec)
            sanitize_train(train)
        except ValueError as exc:
            failures.append(str(exc))
        else:
            expected = TRAIN_BRANCH_PREFIX + train
            code, branch = git(root, "branch", "--show-current")
            if code != 0 or not branch:
                # Detached HEAD / unreadable branch: the lane cannot be
                # confirmed, so a worker must fail CLOSED (the track guard's
                # rule) — never build a train from an unverifiable checkout.
                failures.append(
                    "worker assignment for train {!r} requires branch {!r}, "
                    "but this worktree's branch could not be determined "
                    "(detached HEAD, or git older than 2.22).".format(train, expected)
                )
            elif branch != expected:
                failures.append(
                    "worker assignment for train {!r} must run on its train "
                    "branch {!r}, but this worktree is on {!r} — the "
                    "dispatcher creates the branch and leases the worktree "
                    "(docs/specs/parallel-wi-dispatch.md §6).".format(
                        train, expected, branch
                    )
                )
            wi_rows = load_wi_registry(root)
            for wid in assigned:
                row = wi_rows.get(wid)
                if row is None:
                    failures.append(
                        "assigned {} is not in docs/requirements/"
                        "work-items.csv on this branch — a worker never "
                        "builds an untracked WI.".format(wid)
                    )
                elif (row.get("Status") or "").strip().lower() == "done":
                    failures.append(
                        "assigned {} is already integrated done — a stale "
                        "assignment; the dispatcher must re-derive the "
                        "frontier.".format(wid)
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


# =============================================================================
# WI-182: the parallel dispatcher (SR-061; spec §4/§6/§11/§12)
# =============================================================================
# `--jobs N|auto` (or the AGENT_JOBS env the launchers wire at migration)
# switches agent_loop from the legacy resume loop to the DISPATCHER: derive the
# ready frontier from the WI registry via schedule.py, pack it into traincars,
# reserve each selected traincar's constituent WIs atomically in Git, lease a
# linked worktree per train, and run Slice-C workers in parallel up to the
# ceiling — rescanning for dynamic refill on every worker exit. Reservations
# and train branches are the DURABLE state (out/dispatch/ is a rebuildable
# journal/cache, spec §11); a built train parks ready-to-integrate with its
# reservations held until the integrator (Slice F) advances the durable
# disposition, so nothing is double-run even across dispatcher restarts.

RESERVATION_NS = "refs/llm/reservations/"
DISPATCH_DIR = "out/dispatch"
# A worker that rate-limited (exit 5) is retried after this cooldown.
TRAIN_RETRY_SECONDS = 300

# WI-185 (SR-064): the fault-injection hook the crash matrix drives. Setting
# AGENT_FAULT_POINT=<point> hard-kills the dispatcher (os._exit, no cleanup,
# no atexit — a real crash) the first time execution reaches that named
# lifecycle boundary. Production runs never set it; recovery must reconstruct
# from Git alone afterwards.
FAULT_EXIT = 86


def _fault(point):
    if os.environ.get("AGENT_FAULT_POINT", "") == point:
        print("FAULT-INJECTED: {}".format(point), flush=True)
        os._exit(FAULT_EXIT)


def list_reservations(root):
    """{WI-ID: reservation-commit-sha} from refs/llm/reservations/* — the
    durable claims. Empty on error (a broken git surfaces elsewhere)."""
    code, out = git(
        root,
        "for-each-ref",
        "--format=%(refname)%09%(objectname)",
        RESERVATION_NS.rstrip("/"),
    )
    claims = {}
    if code != 0:
        return claims
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) == 2 and parts[0].startswith(RESERVATION_NS):
            wid = parts[0][len(RESERVATION_NS) :]
            if WI_TOKEN_RE.match(wid):
                claims[wid] = parts[1]
    return claims


def reservation_meta(root, sha):
    """The metadata JSON a reservation commit carries ({train, wis, base}), or
    None when unreadable/malformed — the caller quarantines that claim."""
    code, out = git(root, "log", "-1", "--format=%B", sha)
    if code != 0:
        return None
    try:
        meta = json.loads(out)
    except ValueError:
        return None
    if not isinstance(meta, dict) or not meta.get("train") or not meta.get("wis"):
        return None
    return meta


def reserve_traincar(root, train_id, wis, base):
    """Atomically claim a traincar: ONE off-history metadata commit
    (`git commit-tree` — base tree + base parent, message = the {train, wis,
    base} JSON) and ONE `git update-ref --stdin` transaction creating the
    train branch and every constituent reservation ref with zero-old-value
    checks. If ANY WI is already reserved (or the branch exists) the whole
    transaction fails and nothing is created (SR-061 all-or-none). Returns
    None on success, else the failure text."""
    code, tree = git(root, "rev-parse", base + "^{tree}")
    if code != 0:
        return "cannot resolve base tree for {}: {}".format(base, tree)
    meta = json.dumps(
        {"train": train_id, "wis": list(wis), "base": base}, sort_keys=True
    )
    proc = subprocess.run(
        ["git", "-C", str(root), "commit-tree", tree, "-p", base, "-m", meta],
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    if proc.returncode != 0:
        return "commit-tree failed: {}".format(proc.stderr.strip())
    commit = proc.stdout.strip()
    _fault("reserve-pre-txn")
    # `create` = an atomic zero-old-value check: the fixed ref name is the
    # uniqueness claim for that WI, and one stdin transaction makes the branch
    # + every constituent ref all-or-none (spec §6).
    lines = ["start", "create {} {}".format(TRAIN_BRANCH_HEADS + train_id, base)]
    for wid in wis:
        lines.append("create {}{} {}".format(RESERVATION_NS, wid, commit))
    lines += ["prepare", "commit"]
    # Bytes, not text mode: Windows text mode would rewrite \n as \r\n and
    # git update-ref --stdin would read "start\r" as an unknown command.
    proc = subprocess.run(
        ["git", "-C", str(root), "update-ref", "--stdin"],
        input=("\n".join(lines) + "\n").encode("utf-8"),
        capture_output=True,
    )
    if proc.returncode != 0:
        return "reservation transaction failed (already claimed?): {}".format(
            proc.stderr.decode("utf-8", "replace").strip()[:300]
        )
    _fault("reserve-post-txn")
    return None


TRAIN_BRANCH_HEADS = "refs/heads/" + TRAIN_BRANCH_PREFIX


def release_reservations(root, wis):
    """Transactionally delete the reservation refs of `wis` (one update-ref
    --stdin transaction — the release-on-early-end rule, SR-062). Returns None
    on success, else the failure text. A no-op on an empty list."""
    wis = [w for w in wis if WI_TOKEN_RE.match(w)]
    if not wis:
        return None
    lines = ["start"]
    for wid in wis:
        lines.append("delete {}{}".format(RESERVATION_NS, wid))
    lines += ["prepare", "commit"]
    proc = subprocess.run(
        ["git", "-C", str(root), "update-ref", "--stdin"],
        input=("\n".join(lines) + "\n").encode("utf-8"),
        capture_output=True,
    )
    if proc.returncode != 0:
        return "release transaction failed: {}".format(
            proc.stderr.decode("utf-8", "replace").strip()[:300]
        )
    return None


def train_branch_evidence(root, train_id, base):
    """(built, blocked) trailer evidence read off the train BRANCH (not a
    worktree) — usable from the primary checkout for reconcile, the early-end
    release decision, and the blocked-disposition transaction. `built` is a
    set; `blocked` maps WI id -> its committed BlockRef ('' when omitted)."""
    code, tip = git(root, "rev-parse", TRAIN_BRANCH_PREFIX + train_id)
    built, blocked = set(), {}
    if code != 0:
        return built, blocked
    fmt = (
        "T%x09%(trailers:key=WI,valueonly,separator=;)%x09"
        "%(trailers:key=Blocked-WI,valueonly,separator=;)%x09"
        "%(trailers:key=BlockRef,valueonly,separator=;)"
    )
    code, out = git(root, "log", "--format=" + fmt, base + ".." + tip.strip())
    if code != 0:
        return built, blocked
    for line in out.splitlines():
        parts = (line.split("\t")[1:] + ["", "", ""])[:3]
        built.update(
            x.strip() for x in parts[0].split(";") if WI_TOKEN_RE.match(x.strip())
        )
        refs = [t.strip() for t in parts[2].split(";")]
        for j, tok in enumerate(t.strip() for t in parts[1].split(";")):
            if WI_TOKEN_RE.match(tok) and tok not in blocked:
                blocked[tok] = refs[j] if j < len(refs) else ""
    return built, blocked


def worktree_root(root):
    """Where train worktrees live: a sibling directory of the repo
    (`../<repo>-trains/<train-id>`) — outside the repo so a linked worktree
    never nests inside the primary checkout or the disposable out/."""
    root = Path(root).resolve()
    return root.parent / (root.name + "-trains")


def existing_worktrees(root):
    """{branch: worktree-path} parsed from `git worktree list --porcelain`."""
    code, out = git(root, "worktree", "list", "--porcelain")
    trees = {}
    if code != 0:
        return trees
    path = None
    for line in out.splitlines():
        if line.startswith("worktree "):
            path = line[len("worktree ") :].strip()
        elif line.startswith("branch ") and path:
            trees[line[len("branch ") :].strip()] = path
    return trees


def lease_worktree(root, train_id):
    """The linked worktree for a train — reuse the one already checked out on
    its branch (recovery), else `git worktree add`. Returns (path, err)."""
    branch_ref = TRAIN_BRANCH_HEADS + train_id
    trees = existing_worktrees(root)
    if branch_ref in trees:
        return Path(trees[branch_ref]), None
    wt = worktree_root(root) / train_id
    wt.parent.mkdir(parents=True, exist_ok=True)
    code, out = git(root, "worktree", "add", str(wt), TRAIN_BRANCH_PREFIX + train_id)
    if code != 0:
        return None, "worktree add failed for {}: {}".format(train_id, out[:300])
    return wt, None


def train_phase_gate(root, wi_rows, wid):
    """The `{phase}-{gate}` train-id prefix (spec §6): the WI's first SR's
    delivery Phase (or `p0`) + the derived gate cache (or `g0`)."""
    phase = ""
    srs = _refs((wi_rows.get(wid) or {}).get("SR-Refs", ""))
    if srs:
        for r in _read_csv_rows(
            Path(root) / "docs" / "requirements" / "system-requirements.csv"
        ):
            if (r.get("SR-ID") or "").strip() == srs[0]:
                phase = (r.get("Phase") or "").strip()
                break
    gate = read_declared(Path(root) / "docs" / "gate", "").strip().lower() or "g0"
    phase = re.sub(r"[^A-Za-z0-9._-]", "", phase) or "p0"
    return "{}-{}".format(phase, gate)


def pack_traincars(records, wis_by_id, cap=4):
    """Pack the evaluated schedule records into dispatchable traincars —
    resource-constrained list scheduling with conservative clustering (spec
    §7): every ready WI starts its own traincar in the deterministic order;
    an ORDINARY ready WI then absorbs its unary hard-successor chain (each
    successor `ordinary`-classified, all its other hard preds already done,
    single hard successor edge) up to the cap. Spine/gate/attestation/
    protected/single-wi classes never join a multi-WI traincar. Returns a
    list of {wis, sched_class} dicts in dispatch order."""
    by_id = {r["id"]: r for r in records}
    # children[x] = hard successors of x among tracked WIs
    children = {}
    for w in wis_by_id.values():
        for p in w["preds"]:
            children.setdefault(p, []).append(w["id"])
    consumed = set()
    cars = []
    for r in records:
        if r["disposition"] != "ready" or r["id"] in consumed:
            continue
        car = [r["id"]]
        consumed.add(r["id"])
        if r["sched_class"] == schedule.SCHED_ORDINARY:
            cur = r["id"]
            while len(car) < cap:
                succs = children.get(cur, [])
                if len(succs) != 1:
                    break
                nxt = succs[0]
                nrec = by_id.get(nxt)
                nwi = wis_by_id.get(nxt)
                if (
                    nrec is None
                    or nwi is None
                    or nxt in consumed
                    or nrec["sched_class"] != schedule.SCHED_ORDINARY
                    or nrec["disposition"] not in ("waiting", "ready")
                    or nwi["status"] != "queued"
                ):
                    break
                # Every OTHER hard pred of the successor must already be done
                # (accepted-on-train covers only `cur`, which rides this car).
                others = [p for p in nwi["preds"] if p != cur]
                if any(
                    (wis_by_id.get(p) or {}).get("status") != "done" for p in others
                ):
                    break
                # The successor must itself have a single-successor shape to
                # keep the chain unary (a fork ends the train, spec §7).
                car.append(nxt)
                consumed.add(nxt)
                cur = nxt
        cars.append({"wis": car, "sched_class": r["sched_class"]})
    return cars


class _Journal:
    """The out/dispatch/ runtime journal — a CACHE, never authority (§11).
    Events append before the corresponding external action where possible;
    the manifest is rewritten atomically (temp file + os.replace).

    WI-185: every event is stamped with this dispatcher process's `run` id so
    telemetry aggregates by `(run, train, WI, session)` — a parallel session
    number from one worker can never collide with another's across runs
    (SR-065). The id is `<utc-stamp>-<pid>-<rand>`, unique per launch."""

    def __init__(self, root, run_id=None):
        self.dir = Path(root) / DISPATCH_DIR
        self.run_id = run_id or "{}-{}-{:04x}".format(
            time.strftime("%Y%m%dT%H%M%S"),
            os.getpid(),
            int.from_bytes(os.urandom(2), "big"),
        )
        try:
            self.dir.mkdir(parents=True, exist_ok=True)
            (self.dir / "trains").mkdir(exist_ok=True)
        except OSError:
            pass

    def event(self, event, **fields):
        rec = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "run": self.run_id,
            "event": event,
        }
        rec.update(fields)
        try:
            with (self.dir / "events.jsonl").open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, sort_keys=True) + "\n")
        except OSError:
            pass
        detail = " ".join(
            "{}={}".format(k, v) for k, v in sorted(fields.items()) if v != ""
        )
        print("dispatch: {}{}".format(event, " " + detail if detail else ""))

    def manifest(self, data):
        try:
            tmp = self.dir / "manifest.json.tmp"
            tmp.write_text(json.dumps(data, indent=2, sort_keys=True), "utf-8")
            os.replace(str(tmp), str(self.dir / "manifest.json"))
        except OSError:
            pass

    def train(self, train_id, data):
        try:
            tmp = self.dir / "trains" / (train_id + ".json.tmp")
            tmp.write_text(json.dumps(data, indent=2, sort_keys=True), "utf-8")
            os.replace(str(tmp), str(self.dir / "trains" / (train_id + ".json")))
        except OSError:
            pass


# -----------------------------------------------------------------------------
# WI-184: the atomic serialized integrator (SR-063; spec §9)
# -----------------------------------------------------------------------------
# One logical writer against refs/heads/llm/integration. The ref is advanced
# ONLY by compare-and-swap and is never checked out in the user's primary
# worktree: each ready train composes on a temporary staging branch
# llm/integrate/<train-id> in its own worktree, and the development branch is
# a published PROJECTION of the integration ref — synchronized through the
# durable refs/llm/publish-intent protocol, never half-applied.

INTEGRATION_REF = "refs/heads/llm/integration"
INTEGRATE_BRANCH_PREFIX = "llm/integrate/"
PUBLISH_INTENT_REF = "refs/llm/publish-intent"
STATUS_GENERATED_MARKER = "GENERATED by scripts/agent_loop.py integrator"


def integration_head(root):
    """The integration ref's commit, or None when the ref does not exist."""
    code, out = git(root, "rev-parse", "--verify", "--quiet", INTEGRATION_REF)
    return out.strip() if code == 0 and out.strip() else None


def cas_ref(root, ref, new, old):
    """Compare-and-swap `ref` from exactly `old` to `new` (one update-ref
    transaction). `old` = None asserts creation. Returns True on success; a
    False is HARMLESS — the caller recomposes from the ref's new value."""
    if old:
        line = "update {} {} {}".format(ref, new, old)
    else:
        line = "create {} {}".format(ref, new)
    proc = subprocess.run(
        ["git", "-C", str(root), "update-ref", "--stdin"],
        input=("start\n{}\nprepare\ncommit\n".format(line)).encode("utf-8"),
        capture_output=True,
    )
    return proc.returncode == 0


def ensure_integration_ref(root, journal):
    """Create refs/heads/llm/integration from the selected development branch
    on a GENUINE cold start only (spec §11 rule 2): if the ref is absent while
    dispatcher-owned evidence exists (train/integrate branches, reservations,
    a publish intent), something deleted it — fail closed rather than silently
    blessing the development branch. Returns (head, err)."""
    head = integration_head(root)
    if head:
        return head, None
    code, out = git(
        root,
        "for-each-ref",
        "--format=%(refname)",
        "refs/heads/llm/train",
        "refs/heads/llm/integrate",
        RESERVATION_NS.rstrip("/"),
        PUBLISH_INTENT_REF,
    )
    evidence = [ln for ln in out.splitlines() if ln.strip()] if code == 0 else []
    if evidence:
        return None, (
            "refs/heads/llm/integration is absent but dispatcher-owned "
            "evidence exists ({} ref(s)) — a deleted/corrupt integration ref "
            "is reconstructed or fails closed (spec §11), never re-seeded "
            "from the development branch.".format(len(evidence))
        )
    dev = head_sha_full(root)
    if not dev or not cas_ref(root, INTEGRATION_REF, dev, None):
        return None, "cannot initialize the integration ref from HEAD"
    journal.event("integration-ref-init", head=dev[:12])
    return dev, None


def registry_rows_at(root, ref):
    """The WI registry rows as read from `ref` (the integrated disposition),
    falling back to the checkout when unreadable. The integration ref — not
    the development checkout — is the scheduling authority once it exists."""
    proc = subprocess.run(
        ["git", "-C", str(root), "show", ref + ":docs/requirements/work-items.csv"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
    )
    if proc.returncode != 0:
        return None
    import io

    return list(csv.DictReader(io.StringIO(proc.stdout)))


def reviewed_train_head(root, tid, base):
    """The exact code HEAD a train's review must name: the LAST commit in
    base..tip carrying a WI trailer (verdict/telemetry commits come after)."""
    fmt = "%H%x09%(trailers:key=WI,valueonly,separator=;)"
    code, out = git(
        root, "log", "--format=" + fmt, base + ".." + TRAIN_BRANCH_PREFIX + tid
    )
    if code != 0:
        return None
    for line in out.splitlines():  # newest first
        parts = line.split("\t")
        if len(parts) == 2 and any(
            WI_TOKEN_RE.match(x.strip()) for x in parts[1].split(";")
        ):
            return parts[0]
    return None


def train_verdicts(root, tid, reviewed_sha):
    """[(phase, verdict)] parsed from the verdict files committed on the train
    branch that NAME the exact reviewed commit (reviews/<train>/NNN-<PHASE>-
    <sha7>.md). A verdict naming an older head does not count (spec §8)."""
    tip = TRAIN_BRANCH_PREFIX + tid
    prefix = "docs/reviews/{}/".format(tid)
    code, out = git(root, "ls-tree", "-r", "--name-only", tip, prefix)
    results = []
    if code != 0 or not reviewed_sha:
        return results
    want = reviewed_sha[:7]
    for name in out.splitlines():
        m = re.match(r".*/(\d+)-(REVIEW-[AB]|CRITIQUE)-([0-9a-f]+)\.md$", name.strip())
        if not m or m.group(3) != want:
            continue
        code2, text = git(root, "show", "{}:{}".format(tip, name.strip()))
        if code2 != 0:
            continue
        verdict = ""
        for line in text.splitlines():
            vm = re.match(r"\s*VERDICT:\s*(APPROVE|CHANGES-REQUESTED)", line)
            if vm:
                verdict = vm.group(1)
        results.append((m.group(2), verdict))
    return results


def _staging_worktree(root, tid, base):
    """A staging branch llm/integrate/<tid> at `base` checked out in its own
    worktree. Reuses an existing branch/worktree (recovery). Returns
    (worktree_path, err)."""
    branch = INTEGRATE_BRANCH_PREFIX + tid
    trees = existing_worktrees(root)
    ref = "refs/heads/" + branch
    if ref in trees:
        return Path(trees[ref]), None
    code, _ = git(root, "rev-parse", "--verify", "--quiet", ref)
    wt = worktree_root(root) / ("integrate-" + tid)
    wt.parent.mkdir(parents=True, exist_ok=True)
    if code == 0:
        code2, out = git(root, "worktree", "add", str(wt), branch)
    else:
        code2, out = git(root, "worktree", "add", "-b", branch, str(wt), base)
    if code2 != 0:
        return None, "staging worktree failed for {}: {}".format(tid, out[:300])
    return wt, None


def _rewrite_wi_rows(path, updates):
    """Surgically rewrite specific WI rows (Status/Deliverable/BlockRef) in a
    work-items.csv, touching ONLY the named rows so the integrator never
    reflows an adopter's registry. Returns the list of updated ids."""
    with open(str(path), newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.reader(fh))
    if not rows:
        return []
    header = rows[0]
    idx = {h: i for i, h in enumerate(header)}
    done = []
    for r in rows[1:]:
        if not r or r[0] not in updates:
            continue
        for col, val in updates[r[0]].items():
            if col in idx:
                while len(r) <= idx[col]:
                    r.append("")
                r[idx[col]] = val
        done.append(r[0])
    with open(str(path), "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh, lineterminator="\n").writerows(rows)
    return done


def synth_deliverable(root, tid, wid, base):
    """The integrator's Deliverable text for a WI it marks done: the train,
    the exact commit, and the worker's own commit subject — derived facts,
    never invented prose."""
    fmt = "%H%x09%s%x09%(trailers:key=WI,valueonly,separator=;)"
    code, out = git(
        root, "log", "--format=" + fmt, base + ".." + TRAIN_BRANCH_PREFIX + tid
    )
    subject, sha = "", ""
    if code == 0:
        for line in out.splitlines():
            parts = line.split("\t")
            if len(parts) == 3 and wid in [x.strip() for x in parts[2].split(";")]:
                sha, subject = parts[0][:7], parts[1]
                break
    return "Integrated from train {} @ {}: {}".format(tid, sha or "?", subject or wid)


def generate_status(docs, root, last_train=""):
    """The integrator-generated root status snapshot (SR-059's generation
    half; spec §10): derived gate/bar pointers, queue counts, pending human
    items, the last integrated train — links, never copies. Written ONLY when
    docs/status.md is absent or already generated (a hand-authored status is
    the un-migrated state and is left alone until the migration flips it)."""
    path = docs / "status.md"
    try:
        if path.exists() and STATUS_GENERATED_MARKER not in path.read_text(
            encoding="utf-8", errors="replace"
        ):
            return False
    except OSError:
        return False
    rows = registry_rows_at(root, INTEGRATION_REF) or []
    counts = {"queued": 0, "deferred": 0, "blocked": 0, "done": 0}
    for r in rows:
        st = (r.get("Status") or "").strip().lower()
        if st in counts:
            counts[st] += 1
    gate = read_declared(docs / "gate", "(none)")
    reserved = sorted(list_reservations(root))
    lines = [
        "<!-- " + STATUS_GENERATED_MARKER + " — do not hand-edit -->",
        "# Status (generated)",
        "",
        "- **Derived gate:** {} ([docs/gate](gate); the harness is the bar)".format(
            gate
        ),
        "- **Work items:** {queued} queued · {deferred} deferred · "
        "{blocked} blocked · {done} done — the registry "
        "[work-items.csv](requirements/work-items.csv) is the source; the "
        "dashboard is generated from it.".format(**counts),
        "- **Reserved (in flight):** {}".format(", ".join(reserved) or "none"),
        "- **Last integrated train:** {}".format(last_train or "none this run"),
        "- **Needs <human>:** see [open-items.md](open-items.md) if present.",
        "",
        "_Regenerated by the integrator on the integration branch after every"
        " successful integration — never written on a worker branch._",
    ]
    try:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except OSError:
        return False
    return True


def _run_combined_bar(worktree, root):
    """The combined commit bar on the composed tree: the declared stack test
    command (docs/stack.ini [stack] test). Returns (ok, detail); no declared
    command reports ('skipped', True) — a stackless fixture, not a pass."""
    import configparser

    ini = Path(worktree) / "docs" / "stack.ini"
    if not ini.exists():
        return True, "skipped (no docs/stack.ini)"
    cp = configparser.ConfigParser()
    try:
        cp.read(str(ini), encoding="utf-8")
        cmd = (cp.get("stack", "test", fallback="") or "").strip()
    except configparser.Error as exc:
        return False, "stack.ini unreadable: {}".format(exc)
    if not cmd:
        return True, "skipped (no declared test command)"
    try:
        argv = shlex.split(cmd)
    except ValueError as exc:
        return False, "cannot parse test command: {}".format(exc)
    proc = subprocess.run(
        argv,
        cwd=str(worktree),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    tail = ((proc.stdout or "") + (proc.stderr or "")).strip()[-400:]
    return proc.returncode == 0, ("pass" if proc.returncode == 0 else tail)


def integrate_train(root, docs, journal, tid, wis, base, required_verdicts):
    """Compose one ready train into the integration ref (spec §9 steps 1-11).
    Returns (state, detail): 'integrated', 'needs-re-review' (a textual
    conflict — any resolution needs a focused re-review before this train can
    land), 'rework' (verdict missing/stale or the combined bar failed), or
    'error'. The integration ref moves ONLY via the final CAS."""
    old_head = integration_head(root)
    if old_head is None:
        return "error", "integration ref vanished"
    code, tip = git(root, "rev-parse", TRAIN_BRANCH_PREFIX + tid)
    if code != 0:
        return "error", "train branch missing"
    tip = tip.strip()

    # Step 2: verify reservation scope + the exact-head review verdicts.
    claims = list_reservations(root)
    for wid in wis:
        meta = reservation_meta(root, claims.get(wid, ""))
        if not meta or meta.get("train") != tid:
            return "error", "reservation for {} does not name train {}".format(wid, tid)
    reviewed = reviewed_train_head(root, tid, base)
    if required_verdicts:
        verdicts = train_verdicts(root, tid, reviewed)
        approvals = {ph for ph, v in verdicts if v == "APPROVE"}
        if len(approvals) < required_verdicts:
            return "rework", (
                "review verdicts naming {}: {} approval(s) of {} required".format(
                    (reviewed or "?")[:7], len(approvals), required_verdicts
                )
            )

    # Step 1+3+4: compose on the staging branch from the CURRENT integration
    # HEAD. A clean 3-way merge takes the fast path (no re-review); ANY
    # textual conflict aborts composition and demands a focused re-review.
    wt, err = _staging_worktree(root, tid, old_head)
    if err:
        return "error", err
    code, _ = git(wt, "reset", "--hard", old_head)
    if code != 0:
        return "error", "cannot reset staging to the integration HEAD"
    code, out = git(wt, "merge", "--no-ff", "--no-commit", tip)
    if code != 0:
        git(wt, "merge", "--abort")
        journal.event("integration-conflict", train=tid, detail=out[:200])
        return "needs-re-review", "textual conflict against the integrated tree"

    # Steps 6-8: durable disposition + evidence + regenerated artifacts,
    # composed INTO the same integration commit.
    reg = Path(wt) / "docs" / "requirements" / "work-items.csv"
    updates = {
        wid: {
            "Status": "done",
            "Deliverable": synth_deliverable(root, tid, wid, base),
        }
        for wid in wis
    }
    updated = _rewrite_wi_rows(reg, updates) if reg.exists() else []
    stamp = time.strftime("%Y-%m-%d %H:%M")
    log_path = Path(wt) / "docs" / "log.md"
    try:
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(
                "\n## {} — integrated train {} ({})\n\n"
                "Head {} composed onto {} by the serialized integrator; "
                "{} verdict(s) verified on the exact reviewed head; combined "
                "bar ran on the composed tree (result below). WI row(s) {} "
                "-> done.\n".format(
                    stamp,
                    tid,
                    ";".join(wis),
                    tip[:7],
                    old_head[:7],
                    required_verdicts,
                    ";".join(updated) or "(none present)",
                )
            )
    except OSError:
        pass
    regenerate_index(Path(wt) / "docs")
    generate_status(Path(wt) / "docs", root, last_train=tid)

    # Step 9: the combined bar always runs — even after a clean apply.
    ok, bar_detail = _run_combined_bar(wt, root)
    journal.event("integration-bar", train=tid, result=bar_detail[:120])
    if not ok:
        git(wt, "merge", "--abort")  # tolerate failure; then hard-clean below
        git(wt, "reset", "--hard", old_head)
        return "rework", "combined bar failed: {}".format(bar_detail[:300])

    # Step 10: ONE integration commit carrying the trailers.
    git(wt, "add", "-A")
    trailers = "".join("Integrated-WI: {}\n".format(w) for w in wis)
    msg = "integrate: train {} ({})\n\n{}Train-Head: {}\nTrain: {}\n".format(
        tid, ";".join(wis), trailers, tip, tid
    )
    code, out = git(wt, "commit", "-q", "-m", msg)
    if code != 0:
        git(wt, "reset", "--hard", old_head)
        return "error", "integration commit failed: {}".format(out[:200])
    code, new_head = git(wt, "rev-parse", "HEAD")
    new_head = new_head.strip()
    _fault("pre-integration-cas")

    # Step 11: advance the integration ref by CAS. A stale expected-old is
    # HARMLESS — the train re-enters composition from the new HEAD.
    if not cas_ref(root, INTEGRATION_REF, new_head, old_head):
        journal.event("integration-cas-stale", train=tid)
        git(wt, "reset", "--hard", old_head)
        return "recompose", "integration ref moved; recomposing"
    _fault("post-integration-cas")
    journal.event("integrated", train=tid, wis=";".join(wis), head=new_head[:12])
    # Reservation refs release transactionally ONLY after the durable
    # disposition advanced (spec §6).
    err = release_reservations(root, wis)
    if err:
        journal.event("release-failed", train=tid, reason=err[:200])
    return "integrated", new_head


def blocked_disposition(root, docs, journal, tid, wis, base):
    """The smaller serialized blocked-disposition transaction (spec §9): from
    the current integration HEAD change ONLY the blocked WI's row
    (Status=blocked + BlockRef), append the log evidence, commit with
    Blocked-WI/BlockRef/Train trailers, CAS — and only then release the
    blocked WI's reservation (unstarted ones were already released at the
    early end). Built constituents keep theirs (their partial-train re-review
    path hardens in Slice G). Returns (state, detail)."""
    old_head = integration_head(root)
    if old_head is None:
        return "error", "integration ref vanished"
    built, blocked_map = train_branch_evidence(root, tid, base)
    hit = {w: blocked_map[w] for w in wis if w in blocked_map}
    if not hit:
        return "error", "no Blocked-WI trailer evidence on train " + tid
    wt, err = _staging_worktree(root, tid, old_head)
    if err:
        return "error", err
    code, _ = git(wt, "reset", "--hard", old_head)
    if code != 0:
        return "error", "cannot reset staging to the integration HEAD"
    reg = Path(wt) / "docs" / "requirements" / "work-items.csv"
    updates = {
        wid: {"Status": "blocked", "BlockRef": ref or "(uncommitted — a finding)"}
        for wid, ref in hit.items()
    }
    updated = _rewrite_wi_rows(reg, updates) if reg.exists() else []
    try:
        with (Path(wt) / "docs" / "log.md").open("a", encoding="utf-8") as fh:
            fh.write(
                "\n## {} — blocked disposition: {} (train {})\n\n"
                "Worker-reported blocker with committed evidence at {}; "
                "BlockRef: {}.\n".format(
                    time.strftime("%Y-%m-%d %H:%M"),
                    ";".join(sorted(hit)),
                    tid,
                    base[:7],
                    "; ".join(v or "(none)" for v in hit.values()),
                )
            )
    except OSError:
        pass
    generate_status(Path(wt) / "docs", root, last_train="")
    git(wt, "add", "-A")
    trailers = "".join("Blocked-WI: {}\n".format(w) for w in sorted(hit))
    trailers += "".join("BlockRef: {}\n".format(v or "(none)") for v in hit.values())
    msg = "blocked: {} (train {})\n\n{}Train: {}\n".format(
        ";".join(sorted(hit)), tid, trailers, tid
    )
    code, out = git(wt, "commit", "-q", "-m", msg)
    if code != 0:
        git(wt, "reset", "--hard", old_head)
        return "error", "disposition commit failed: {} (rows: {})".format(
            out[:200], ";".join(updated)
        )
    code, new_head = git(wt, "rev-parse", "HEAD")
    if not cas_ref(root, INTEGRATION_REF, new_head.strip(), old_head):
        git(wt, "reset", "--hard", old_head)
        return "recompose", "integration ref moved; recomposing"
    journal.event("blocked-disposition", train=tid, wis=";".join(sorted(hit)))
    err = release_reservations(root, sorted(hit))
    if err:
        journal.event("release-failed", train=tid, reason=err[:200])
    return "integrated", new_head.strip()


def _intent_meta(root):
    """(sha, meta) of the current publish intent, or (None, None). Unreadable
    metadata returns (sha, None) — recovery evidence, never overwritten
    silently."""
    code, sha = git(root, "rev-parse", "--verify", "--quiet", PUBLISH_INTENT_REF)
    if code != 0 or not sha.strip():
        return None, None
    return sha.strip(), reservation_meta(root, sha.strip())


def publish_integration(root, journal, dev_branch):
    """Publish the integration HEAD to the development branch (spec §9): only
    when the primary worktree is CLEAN; guarded by the durable publish-intent
    ref written before the dev-ref CAS and deleted only after the verified
    fast-forward/reset sync. Returns (state, detail) where state is
    'published', 'deferred', 'noop', or 'error'."""
    target = integration_head(root)
    if not target:
        return "noop", "no integration ref"
    dev_ref = "refs/heads/" + dev_branch
    code, dev_head = git(root, "rev-parse", "--verify", "--quiet", dev_ref)
    if code != 0:
        return "error", "development ref {} unreadable".format(dev_ref)
    dev_head = dev_head.strip()
    intent_sha, intent = _intent_meta(root)

    if dev_head == target:
        # Published already (this or a prior attempt): confirm the worktree
        # sync, then drop any completed intent.
        code, porcelain = git(root, "status", "--porcelain")
        tracked_dirty = [
            ln for ln in porcelain.splitlines() if ln and not ln.startswith("??")
        ]
        if tracked_dirty:
            code2, diff_old = (
                git(root, "diff", "--quiet", intent["old"])
                if (intent and intent.get("old"))
                else (1, "")
            )
            if intent and intent.get("old") and code2 == 0:
                # The §11 stale-checkout case: index/worktree still exactly at
                # the intent's expected old hash — mechanically stale, not
                # user dirt. Finish the idempotent sync.
                git(root, "reset", "--hard", target)
            else:
                return "deferred", (
                    "development ref already at the target but the worktree "
                    "diverges — left untouched and reported, never reset"
                )
        if intent_sha:
            git(root, "update-ref", "-d", PUBLISH_INTENT_REF, intent_sha)
            journal.event("publish-intent-cleared", target=target[:12])
        return "noop", "development branch already at the integration head"

    # Dirty-at-outset: defer, report, never stash/reset (spec §9).
    code, porcelain = git(root, "status", "--porcelain")
    tracked_dirty = [
        ln for ln in porcelain.splitlines() if ln and not ln.startswith("??")
    ]
    if tracked_dirty:
        journal.event("publish-deferred", reason="dirty-worktree")
        return "deferred", (
            "primary worktree carries {} uncommitted tracked path(s) — "
            "publication deferred, checkout untouched".format(len(tracked_dirty))
        )

    # The durable intent: {target, old, ref}. Reuse only an EXACT match; a
    # differing intent is replaced by an expected-old-object CAS (a failed
    # prior attempt retained as evidence until this recomposition).
    meta = {
        "train": "publish",
        "wis": ["publish"],
        "base": target,
        "target": target,
        "old": dev_head,
        "ref": dev_ref,
    }
    if intent and (
        intent.get("target") == target
        and intent.get("old") == dev_head
        and intent.get("ref") == dev_ref
    ):
        new_intent = intent_sha  # identical — reuse
    else:
        code, tree = git(root, "rev-parse", target + "^{tree}")
        if code != 0:
            return "error", "cannot resolve the target tree"
        proc = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "commit-tree",
                tree.strip(),
                "-p",
                target,
                "-m",
                json.dumps(meta, sort_keys=True),
            ],
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
        )
        if proc.returncode != 0:
            return "error", "intent commit failed"
        new_intent = proc.stdout.strip()
        if intent_sha:
            ok = cas_ref(root, PUBLISH_INTENT_REF, new_intent, intent_sha)
        else:
            ok = cas_ref(root, PUBLISH_INTENT_REF, new_intent, None)
        if not ok:
            return "deferred", "publish intent raced; retrying next pass"
        journal.event("publish-intent", target=target[:12], old=dev_head[:12])

    _fault("post-intent")
    # Second CAS: the development ref, against the intent's expected old.
    if not cas_ref(root, dev_ref, target, dev_head):
        # Moved to a third hash: no publication occurred; the stale intent is
        # kept as recovery evidence through the next recomposition.
        journal.event("publish-cas-stale", ref=dev_ref)
        return "deferred", "development ref moved; recomposing from its new head"

    _fault("post-dev-cas")
    # Verified sync: a reset fires ONLY with index + tracked tree exactly at
    # the expected old hash (untracked files untouched); divergence defers.
    code1, _ = git(root, "diff", "--quiet", dev_head)
    code2, _ = git(root, "diff", "--cached", "--quiet", dev_head)
    if code1 != 0 or code2 != 0:
        journal.event("publish-sync-deferred", reason="worktree-diverged")
        return "deferred", (
            "edits landed between the CAS and the sync — the intent ref "
            "identifies the pre-publication hash; sync deferred, not reset"
        )
    code, out = git(root, "reset", "--hard", target)
    if code != 0:
        return "error", "sync reset failed: {}".format(out[:200])
    git(root, "update-ref", "-d", PUBLISH_INTENT_REF, new_intent)
    journal.event("published", ref=dev_ref, head=target[:12])
    return "published", target


def parse_jobs(value):
    """The --jobs/AGENT_JOBS value: a positive int, or `auto` (adaptive up to
    the configured ceiling — AGENT_JOBS_CEILING, default 2). Raises ValueError
    on anything else."""
    v = (str(value) or "").strip().lower()
    if v == "auto":
        try:
            ceiling = int(os.environ.get("AGENT_JOBS_CEILING", "2"))
        except ValueError:
            ceiling = 2
        return max(1, ceiling)
    n = int(v)  # ValueError propagates to the caller's preflight
    if n < 1:
        raise ValueError("--jobs must be >= 1, got {}".format(n))
    return n


def _write_runstate(docs, state, ask=""):
    """The dispatcher-generated root run-state (spec §10; SR-059's generation
    half): RUNNING | NEEDS-HUMAN (+ ask) | BLOCKED | DONE. Generated only by
    the dispatcher/integrator — never by a worker."""
    try:
        (docs / "run-state").write_text(
            state + ("\nask: " + ask if ask else "") + "\n", encoding="utf-8"
        )
    except OSError:
        pass


# -----------------------------------------------------------------------------
# WI-186 (SR-065/SR-059; spec §13/§14): telemetry, banner, downstream migration
# -----------------------------------------------------------------------------

PARALLEL_READY_FILE = "parallel-ready"


def assess_migration(root):
    """The two audits that gate the two-worker promotion (spec §14 items 9-10).
    Returns a dict:

    - `safetyclass_ok` — every OPEN WI (queued/blocked/legacy-active) carries a
      resolvable, non-`unclassified` SafetyClass (schedule.classify over the
      declared value). A single unclassified open WI holds the whole repo at
      `--jobs 1` (an unaudited row cannot be promoted, §14.10).
    - `soft_edges` — the `(wi, soft-pred)` pairs the optimistic scheduler would
      treat as safe-to-run-concurrently; each must be human-audited before
      first parallel enable (§14.9).
    - `softedge_ok` — True when there are no soft edges, OR `docs/parallel-ready`
      records the human sign-off (its presence IS the recorded audit).
    - `legacy_active` / `legacy_tracks` — migration residue to reconcile.

    A FRESH scaffold passes by construction: no soft edges, every drafted WI
    classified, no legacy rows — so it runs parallel-by-default with no marker
    (SR-059). A MIGRATED repo holds at 1 until both audits pass."""
    wis = schedule.load_wis(
        schedule.load_rows(root / "docs" / "requirements" / "work-items.csv")
    )
    open_states = ("queued", "blocked", "active", "ready", "reserved")
    unclassified = []
    for w in wis:
        if w["status"] in open_states:
            sched_class, _ = schedule.classify(w)
            if sched_class == schedule.SCHED_UNCLASSIFIED:
                unclassified.append(w["id"])
    soft_edges = [(w["id"], s) for w in wis for s in w["soft"]]
    legacy_active = [w["id"] for w in wis if w["status"] == "active"]
    tracks_dir = root / "docs" / "tracks"
    legacy_tracks = (
        sorted(p.name for p in tracks_dir.iterdir() if p.is_dir())
        if tracks_dir.is_dir()
        else []
    )
    signed = (root / "docs" / PARALLEL_READY_FILE).exists()
    return {
        "safetyclass_ok": not unclassified,
        "unclassified": unclassified,
        "soft_edges": soft_edges,
        "softedge_ok": (not soft_edges) or signed,
        "signed": signed,
        "legacy_active": legacy_active,
        "legacy_tracks": legacy_tracks,
    }


def reconcile_legacy(root, journal, assessment):
    """Reconcile migration residue within the one compatibility window (§14.3-4):
    a legacy `active` WI row returns to `queued` with a logged finding (runtime
    activity is dispatcher state, not a tracked column); `docs/tracks/*` lanes
    stay readable but are flagged (the new dispatcher never schedules from
    them). Returns the count of reconciled active rows."""
    reg = root / "docs" / "requirements" / "work-items.csv"
    reconciled = []
    if assessment["legacy_active"] and reg.exists():
        updates = {w: {"Status": "queued"} for w in assessment["legacy_active"]}
        reconciled = _rewrite_wi_rows(reg, updates)
        if reconciled:
            journal.event(
                "legacy-active-reconciled",
                wis=";".join(reconciled),
                finding="active->queued (runtime activity is dispatcher state)",
            )
    if assessment["legacy_tracks"]:
        journal.event(
            "legacy-tracks-flagged",
            tracks=";".join(assessment["legacy_tracks"]),
            finding="docs/tracks/* readable this window; dispatcher never "
            "schedules from them (declare Priority/edges instead)",
        )
    return len(reconciled)


def resolve_ceiling(root, requested, journal):
    """Apply the migration gate to the requested worker ceiling (SR-065): a
    repo may run >1 worker only once BOTH audits pass. Returns (ceiling,
    assessment). A held repo drops to 1 with a reason-coded event; a repo that
    passes at a ceiling>1 for the first time records the deliberate promotion."""
    assessment = assess_migration(root)
    if requested <= 1:
        return 1, assessment
    if not assessment["safetyclass_ok"]:
        journal.event(
            "migration-hold",
            requested=requested,
            reason="unclassified-open-wi:" + ";".join(assessment["unclassified"]),
        )
        return 1, assessment
    if not assessment["softedge_ok"]:
        journal.event(
            "migration-hold",
            requested=requested,
            reason="soft-edge-audit-unsigned:{}-edge(s); review and create "
            "docs/parallel-ready".format(len(assessment["soft_edges"])),
        )
        return 1, assessment
    # Both audits pass — record the deliberate two-worker promotion once.
    if requested > 1:
        journal.event(
            "parallel-enabled",
            ceiling=requested,
            soft_edges=len(assessment["soft_edges"]),
        )
    return requested, assessment


def dispatch_banner(jobs, active, parked, cars, journal, integrating=0):
    """The one-line dispatcher banner (SR-065): active lanes, ready-frontier
    width, integration-queue depth, and the cost/concurrency ceiling — so
    parallel spend is visible at a glance."""
    ready_frontier = sum(len(c["wis"]) for c in cars)
    queued_to_integrate = sum(
        1
        for p in parked.values()
        if p["state"] in ("ready-to-integrate", "blocked", "train-end")
    )
    print(
        "dispatch banner | lanes {}/{} | frontier {} WI in {} car(s) | "
        "integration-queue {} | ceiling {}".format(
            len(active),
            jobs,
            ready_frontier,
            len(cars),
            queued_to_integrate,
            jobs,
        )
    )


def telemetry_summary(journal):
    """The end-of-run telemetry rollup (spec §13): the required measurements
    derived from the reason-coded event stream, aggregated by `(run, train,
    WI, session)`. Written to out/dispatch/telemetry.json and printed — the
    evidence a downstream adopter tunes capacity from."""
    events = []
    try:
        with (journal.dir / "events.jsonl").open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except ValueError:
                        continue
    except OSError:
        events = []
    run = journal.run_id
    mine = [e for e in events if e.get("run") == run]

    def count(name):
        return sum(1 for e in mine if e.get("event") == name)

    trains = sorted({e["train"] for e in mine if e.get("train")})
    summary = {
        "run": run,
        # ready-frontier decisions + reservation/worker/integration lifecycle
        "reservations": count("reserve"),
        "workers_started": count("worker-start"),
        "workers_done": count("worker-done"),
        "integrations": count("integrated"),
        "blocked_dispositions": count("blocked-disposition"),
        # overlap / conflict / re-review rates (spec §13 required measurements)
        "conflicts": count("integration-conflict"),
        "re_reviews_needed": sum(
            1
            for e in mine
            if e.get("event") == "integration-parked"
            and e.get("state") == "needs-re-review"
        ),
        "rework_parks": sum(
            1
            for e in mine
            if e.get("event") == "integration-parked" and e.get("state") == "rework"
        ),
        # train continuation / early-end reasons
        "train_ends": count("worker-train-end"),
        "released_unstarted": count("release-unstarted"),
        # recovery outcomes
        "reconciles": count("reconcile"),
        "quarantines": count("quarantine"),
        "trains": trains,
        # combined-bar failures after individually-green trains
        "bar_failures": sum(
            1
            for e in mine
            if e.get("event") == "integration-bar"
            and e.get("result")
            not in (
                "pass",
                "skipped (no docs/stack.ini)",
                "skipped (no declared test command)",
            )
        ),
    }
    try:
        (journal.dir / "telemetry.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8"
        )
    except OSError:
        pass
    print(
        "dispatch telemetry | {} reservation(s) -> {} integration(s), "
        "{} conflict(s)/{} re-review(s)/{} rework, {} recovery reconcile(s), "
        "{} quarantine(s), {} bar-failure(s) after green | trains: {}".format(
            summary["reservations"],
            summary["integrations"],
            summary["conflicts"],
            summary["re_reviews_needed"],
            summary["rework_parks"],
            summary["reconciles"],
            summary["quarantines"],
            summary["bar_failures"],
            ", ".join(trains) or "none",
        )
    )
    return summary


def dispatch_run(args, root):
    """The dispatcher/integrator loop (SR-061): reconcile -> gate -> build-out.

    Returns an exit code. Concurrency is bounded by --jobs; every worker exit,
    block, or reservation event triggers a rescan (dynamic refill — never a
    static wave). Spine-class traincars serialize whole-project: one runs with
    every other lane drained, and nothing else dispatches meanwhile."""
    docs = root / "docs"
    journal = _Journal(root)
    try:
        jobs = parse_jobs(args.jobs)
    except ValueError as exc:
        print("agent_loop: --jobs: {}".format(exc), file=sys.stderr)
        return EXIT_PREFLIGHT

    template = (
        args.agent_cmd
        if args.agent_cmd is not None
        else os.environ.get("AGENT_CMD", "")
    )
    failures = preflight(root, template, args)
    if failures:
        print("agent_loop: preflight failed —", file=sys.stderr)
        for f in failures:
            print("  - " + f, file=sys.stderr)
        return EXIT_PREFLIGHT

    # One dispatcher per checkout — the same kernel lock the legacy loop takes,
    # so a legacy coordinator and a dispatcher can never grind one worktree.
    lock_err = acquire_lock(root / "out" / "agent-loop.lock")
    if lock_err:
        print("agent_loop: {}".format(lock_err), file=sys.stderr)
        return EXIT_PREFLIGHT
    atexit.register(release_lock, root / "out" / "agent-loop.lock")

    gate_policy = read_declared(docs / "gate-policy", "attended")
    # The integrator's review requirement: managed routing + the reviewer dial
    # decide how many exact-head APPROVE verdicts a train needs to integrate.
    managed = bool(agent_route.load_enabled(docs / "agents-enabled"))
    try:
        rp_int = max(0, min(2, int(read_declared(docs / "review-policy", "1"))))
    except ValueError:
        rp_int = 1
    required_verdicts = rp_int if managed else 0

    # The selected development branch — the publication target. A detached
    # dispatcher checkout has no publishable projection: fail closed.
    code, dev_branch = git(root, "branch", "--show-current")
    if code != 0 or not dev_branch.strip():
        print(
            "agent_loop: the dispatcher requires a checked-out development "
            "branch (detached HEAD cannot receive publications).",
            file=sys.stderr,
        )
        return EXIT_PREFLIGHT
    dev_branch = dev_branch.strip()

    # The downstream-migration gate (SR-065, spec §14): a repo runs >1 worker
    # only once its soft-edge AND SafetyClass audits pass; until then it holds
    # at --jobs 1. A fresh scaffold passes by construction. Legacy `active`
    # rows + docs/tracks/* reconcile within this one compatibility window.
    requested_jobs = jobs
    jobs, assessment = resolve_ceiling(root, jobs, journal)
    reconcile_legacy(root, journal, assessment)

    print("=== parallel dispatcher (scripts/agent_loop.py --jobs {}) ===".format(jobs))
    if jobs < requested_jobs:
        hold = (
            "unclassified open WI(s): " + ";".join(assessment["unclassified"])
            if not assessment["safetyclass_ok"]
            else "{} unaudited soft edge(s) — sign off by creating "
            "docs/parallel-ready".format(len(assessment["soft_edges"]))
        )
        print(
            "MIGRATION HOLD: requested {} worker(s) but held at 1 until the "
            "migration audits pass ({}). See the downstream-resync skill.".format(
                requested_jobs, hold
            )
        )
    print(
        "repo: {} | gate-policy: {} | dev branch: {} | worktrees: {} | run {}".format(
            root, gate_policy, dev_branch, worktree_root(root), journal.run_id
        )
    )
    print(
        "CONSENT: workers run headless with the wired permission-bypass "
        "template; reservations + train branches are durable Git state."
    )

    # The integration ref is the authoritative integrated disposition (spec
    # §11); create it only on a genuine cold start, else fail closed.
    _ihead, err = ensure_integration_ref(root, journal)
    if err:
        print("agent_loop: {}".format(err), file=sys.stderr)
        return EXIT_PREFLIGHT
    # Reconcile the integration ref against the development branch at launch
    # (spec §9 "creates or reconciles it from the selected development branch").
    # Classify the relationship BEFORE acting so a human's new work is never
    # discarded by a mistaken publish:
    ihead = integration_head(root)
    dhead = head_sha_full(root)
    dev_strictly_ahead = False
    if ihead and dhead and ihead != dhead:
        int_is_anc = git(root, "merge-base", "--is-ancestor", ihead, dhead)[0] == 0
        dev_is_anc = git(root, "merge-base", "--is-ancestor", dhead, ihead)[0] == 0
        if int_is_anc and not dev_is_anc:
            dev_strictly_ahead = True
        elif not int_is_anc and not dev_is_anc:
            journal.event("integration-diverged", ihead=ihead[:12], dhead=dhead[:12])
    if dev_strictly_ahead:
        # Dev is strictly AHEAD of integration: a human added WIs on the
        # development branch. Fast-forward the ref to absorb that new work
        # (never over unpublished integration commits — the divergent case
        # above is logged and left for a human/later rung).
        if cas_ref(root, INTEGRATION_REF, dhead, ihead):
            journal.event("integration-fast-forward", head=dhead[:12])
    else:
        # Integration ahead-or-equal of dev: resume any interrupted publication
        # idempotently (this also finishes a crash-stranded worktree sync when
        # the dev ref already equals the integration head, spec §11).
        state, detail = publish_integration(root, journal, dev_branch)
        if state == "published":
            print(
                "dispatch: resumed an interrupted publication ({})".format(detail[:12])
            )

    # --- stage 1: reconcile owned trains to a clean baseline (spec §4.1) -----
    # Group durable reservation claims into trains; resume the incomplete,
    # park the built (ready-to-integrate, Slice F), quarantine the unreadable.
    active = {}  # train_id -> {proc, wis, base, worktree, spine}
    parked = {}  # train_id -> {"state": ..., "wis": [...]}
    retry_at = {}  # train_id -> epoch when a WAITING train may retry
    quarantined_wis = set()
    claims = list_reservations(root)
    trains = {}
    for wid, sha in sorted(claims.items()):
        meta = reservation_meta(root, sha)
        if meta is None:
            journal.event("quarantine", wi=wid, reason="unreadable-reservation")
            quarantined_wis.add(wid)
            continue
        trains.setdefault(meta["train"], {"wis": [], "base": meta["base"]})
        trains[meta["train"]]["wis"].append(wid)
    for tid, t in sorted(trains.items()):
        code, _ = git(
            root, "rev-parse", "--verify", "--quiet", TRAIN_BRANCH_HEADS + tid
        )
        if code != 0:
            journal.event("quarantine", train=tid, reason="reservation-without-branch")
            quarantined_wis.update(t["wis"])
            continue
        # Read evidence off the branch (works without a worktree).
        built, blocked = train_branch_evidence(root, tid, t["base"])
        # Ownership cross-check (spec §6/§11): a train branch claiming a WI
        # outside its own reservation set is unprovable ownership — quarantine
        # THIS train (fail closed) and let disjoint proven work continue.
        foreign = (built | set(blocked)) - set(t["wis"])
        if foreign:
            journal.event(
                "quarantine",
                train=tid,
                reason="claims-unreserved-wi:" + ";".join(sorted(foreign)),
            )
            quarantined_wis.update(t["wis"])
            parked[tid] = {"state": "quarantined", "wis": t["wis"], "base": t["base"]}
            continue
        # Already-integrated restore (spec §11 table): the durable disposition
        # advanced before a crash could release the reservations — every WI is
        # done on the integration ref, so restore `integrated` and finish the
        # pending release; never re-integrate.
        int_rows = registry_rows_at(root, INTEGRATION_REF) or []
        int_status = {
            (r.get("WI-ID") or "").strip(): (r.get("Status") or "").strip().lower()
            for r in int_rows
        }
        if t["wis"] and all(int_status.get(w) == "done" for w in t["wis"]):
            err = release_reservations(root, t["wis"])
            if err:
                journal.event("release-failed", train=tid, reason=err[:200])
            parked[tid] = {"state": "integrated", "wis": t["wis"], "base": t["base"]}
            journal.event("reconcile", train=tid, state="integrated")
        elif blocked:
            parked[tid] = {"state": "blocked", "wis": t["wis"], "base": t["base"]}
            journal.event("reconcile", train=tid, state="blocked")
        elif set(t["wis"]) <= built:
            parked[tid] = {
                "state": "ready-to-integrate",
                "wis": t["wis"],
                "base": t["base"],
            }
            journal.event("reconcile", train=tid, state="ready-to-integrate")
        else:
            # Incomplete: resume with a fresh worker (its dirty-tree note is
            # the reconcile-first prompt, spec §11).
            parked[tid] = {"state": "resume", "wis": t["wis"], "base": t["base"]}
            journal.event("reconcile", train=tid, state="resume")

    def spawn_worker(tid, wis, base, spine):
        wt, err = lease_worktree(root, tid)
        if err:
            journal.event("quarantine", train=tid, reason=err)
            parked[tid] = {"state": "quarantined", "wis": wis}
            return False
        argv = [
            sys.executable,
            str(Path(__file__).resolve()),
            "--worktree",
            str(wt),
            "--wi",
            ";".join(wis),
            "--train",
            tid,
            "--base",
            base,
            "--max-iterations",
            str(args.worker_iterations),
            "--pause",
            str(args.pause),
            "--no-session-echo",
        ]
        if args.agent_cmd is not None:
            argv += ["--agent-cmd", args.agent_cmd]
        if args.model:
            argv += ["--model", args.model]
        if args.session_timeout:
            argv += ["--session-timeout", str(args.session_timeout)]
        logdir = journal.dir / "logs"
        out_fh = None
        try:
            logdir.mkdir(parents=True, exist_ok=True)
            out_fh = (logdir / (tid + ".out")).open("ab")
        except OSError:
            pass
        proc = subprocess.Popen(
            argv,
            cwd=str(wt),
            stdout=out_fh if out_fh is not None else subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
        )
        active[tid] = {
            "proc": proc,
            "wis": wis,
            "base": base,
            "worktree": str(wt),
            "spine": spine,
            "log_fh": out_fh,
        }
        journal.event(
            "worker-start", train=tid, wis=";".join(wis), pid=proc.pid, spine=spine
        )
        journal.train(tid, {"wis": wis, "base": base, "state": "building"})
        return True

    needs_human_ask = ""

    def handle_exit(tid, code):
        nonlocal needs_human_ask
        info = active.pop(tid)
        if info.get("log_fh") is not None:
            try:
                info["log_fh"].close()
            except OSError:
                pass
        if code == EXIT_DONE:
            parked[tid] = {
                "state": "ready-to-integrate",
                "wis": info["wis"],
                "base": info["base"],
            }
            journal.event("worker-done", train=tid, state="ready-to-integrate")
            journal.train(
                tid,
                {
                    "wis": info["wis"],
                    "base": info["base"],
                    "state": "ready-to-integrate",
                },
            )
            if info["spine"] and gate_policy != "autonomous":
                # Gate/spine work built: under attended/single-ratify the run
                # EXITS FOR RATIFICATION (spec §4.2) — a human closes the gate
                # before build-out continues; `autonomous` continues on the
                # independent-reviewer verdict.
                needs_human_ask = (
                    "spine/gate train {} is built and needs ratification "
                    "(docs/gate-policy: {})".format(tid, gate_policy)
                )
                journal.event("gate-ratification-exit", train=tid)
        elif code in (EXIT_BLOCKED, EXIT_TRAIN_END):
            # A blocked constituent or a refused continuation ends the train
            # early (SR-062): built + blocked constituents KEEP their
            # reservations (evidence for the Slice-F integrator; nothing
            # double-runs), while every UNSTARTED constituent is released in
            # one transaction and the next rescan recomputes the traincar DAG.
            built, blocked_set = train_branch_evidence(root, tid, info["base"])
            unstarted = [
                w for w in info["wis"] if w not in built and w not in blocked_set
            ]
            err = release_reservations(root, unstarted)
            if err:
                journal.event("release-failed", train=tid, reason=err[:200])
            elif unstarted:
                journal.event("release-unstarted", train=tid, wis=";".join(unstarted))
            state = "blocked" if code == EXIT_BLOCKED else "train-end"
            parked[tid] = {
                "state": state,
                "wis": [w for w in info["wis"] if w not in unstarted],
                "base": info["base"],
            }
            journal.event(
                "worker-blocked" if code == EXIT_BLOCKED else "worker-train-end",
                train=tid,
            )
        elif code == EXIT_WAITING:
            retry_at[tid] = time.time() + TRAIN_RETRY_SECONDS
            parked[tid] = {"state": "waiting", "wis": info["wis"], "base": info["base"]}
            journal.event("worker-waiting", train=tid, retry_s=TRAIN_RETRY_SECONDS)
        elif code == EXIT_NEEDS_HUMAN:
            parked[tid] = {
                "state": "needs-human",
                "wis": info["wis"],
                "base": info["base"],
            }
            needs_human_ask = "worker train {} paged (no routable model / escalation) — see {}".format(
                tid, journal.dir / "logs" / (tid + ".out")
            )
            journal.event("worker-needs-human", train=tid)
        else:
            parked[tid] = {
                "state": "quarantined",
                "wis": info["wis"],
                "base": info["base"],
            }
            journal.event("worker-quarantined", train=tid, exit=code)

    # --- stages 2+3: gate-first, then build-out with dynamic refill ----------
    # The lowest-gate-first order (schedule.py) puts spine/gate work at the
    # frontier head; the dispatcher serializes it whole-project by draining
    # every other lane before it runs and dispatching nothing beside it.
    last_banner_sig = None
    while True:
        # Pause: stop NEW reservations at this boundary; in-flight workers
        # finish their safe boundary and stay recoverable (spec §12).
        # Blackout: start no NEW worker inside the window (spec §12); the
        # in-flight ones continue (their own session loop honors it too).
        paused = pause_reason(docs)
        blacked_out = bool(
            blackout_wake(
                read_declared(docs / "blackout", ""), datetime.datetime.utcnow()
            )
        )
        may_dispatch = paused is None and not blacked_out and not needs_human_ask

        spine_active = any(a["spine"] for a in active.values())
        if may_dispatch:
            # Resume reconciled trains first (they already hold reservations).
            for tid, p in sorted(parked.items()):
                if len(active) >= jobs or spine_active:
                    break
                if p.get("state") == "resume" or (
                    p.get("state") == "waiting" and time.time() >= retry_at.get(tid, 0)
                ):
                    del parked[tid]
                    spawn_worker(tid, p["wis"], p["base"], spine=False)

        # Scan the frontier every pass (cheap, and the end-state test below
        # needs it even while paused/blacked out). Once the integration ref
        # exists it is the authoritative integrated disposition (spec §11) —
        # the development checkout is only its published projection.
        reg_rows = registry_rows_at(root, INTEGRATION_REF)
        if reg_rows is None:
            reg_rows = schedule.load_rows(
                root / "docs" / "requirements" / "work-items.csv"
            )
        wi_rows = {}
        for r in reg_rows:
            wid = (r.get("WI-ID") or "").strip()
            if WI_TOKEN_RE.match(wid) and wid not in wi_rows:
                wi_rows[wid] = r
        wis = schedule.load_wis(reg_rows)
        reserved = set(list_reservations(root)) | quarantined_wis
        records = schedule.evaluate(wis, reserved)
        wis_by_id = {w["id"]: w for w in wis}
        cars = pack_traincars(records, wis_by_id)

        if may_dispatch:
            spine_active = any(a["spine"] for a in active.values())
            for car in cars:
                if len(active) >= jobs or spine_active:
                    break
                is_spine = car["sched_class"] in (
                    schedule.SCHED_SPINE_SERIAL,
                    schedule.SCHED_PROTECTED,
                )
                if is_spine and active:
                    break  # spine serializes whole-project: drain lanes first
                first = car["wis"][0]
                tid = "{}-{}-{}".format(
                    train_phase_gate(root, wi_rows, first),
                    first,
                    "%04x" % int.from_bytes(os.urandom(2), "big"),
                )
                # New trains compose from the CURRENT integration HEAD (spec
                # §9) — never from the (possibly stale) development checkout.
                base = integration_head(root) or head_sha_full(root)
                err = reserve_traincar(root, tid, car["wis"], base)
                if err:
                    journal.event("reserve-failed", train=tid, reason=err[:200])
                    continue
                journal.event(
                    "reserve",
                    train=tid,
                    wis=";".join(car["wis"]),
                    cls=car["sched_class"],
                    base=base[:12],
                )
                spawn_worker(tid, car["wis"], base, spine=is_spine)
                if is_spine:
                    break

        # --- the serialized integrator (WI-184, SR-063): one logical writer,
        # deterministic queue order, CAS-advanced. Ready trains compose one at
        # a time; a worker-reported blocker takes the smaller disposition
        # transaction. Each success is followed by a publication attempt and
        # triggers a fresh rescan (the frontier may have grown).
        integrated_any = False
        for tid in sorted(parked):
            if needs_human_ask:
                break  # a pending human act gates integration too (§4.2)
            state_p = parked[tid]["state"]
            if state_p not in ("ready-to-integrate", "blocked"):
                continue
            base_t = parked[tid].get("base") or (
                reservation_meta(
                    root, list_reservations(root).get(parked[tid]["wis"][0], "")
                )
                or {}
            ).get("base", "")
            if state_p == "ready-to-integrate":
                result, detail = integrate_train(
                    root,
                    docs,
                    journal,
                    tid,
                    parked[tid]["wis"],
                    base_t,
                    required_verdicts,
                )
            else:
                result, detail = blocked_disposition(
                    root, docs, journal, tid, parked[tid]["wis"], base_t
                )
            if result == "integrated":
                parked[tid] = {
                    "state": "integrated"
                    if state_p == "ready-to-integrate"
                    else "blocked-done",
                    "wis": parked[tid]["wis"],
                }
                integrated_any = True
            elif result == "recompose":
                integrated_any = True  # ref moved: rescan and retry this train
            else:
                parked[tid] = {
                    "state": result if result != "error" else "quarantined",
                    "wis": parked[tid]["wis"],
                }
                journal.event(
                    "integration-parked", train=tid, state=result, detail=detail[:200]
                )
        if integrated_any:
            state_pub, detail_pub = publish_integration(root, journal, dev_branch)
            if state_pub == "deferred":
                print("dispatch: publication deferred — {}".format(detail_pub))

        journal.manifest(
            {
                "jobs": jobs,
                "run": journal.run_id,
                "active": {t: a["wis"] for t, a in active.items()},
                "parked": {t: p["state"] for t, p in parked.items()},
                "updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }
        )
        # The banner (SR-065) — only when the picture changed, so the poll loop
        # does not spam it every cadence tick.
        banner_sig = (
            len(active),
            tuple(sorted(p["state"] for p in parked.values())),
            sum(len(c["wis"]) for c in cars),
        )
        if banner_sig != last_banner_sig:
            dispatch_banner(jobs, active, parked, cars, journal)
            last_banner_sig = banner_sig
        if integrated_any:
            continue  # the integrated frontier may have unlocked successors

        if not active:
            waiting = [t for t, p in parked.items() if p["state"] == "waiting"]
            resumable = [t for t, p in parked.items() if p["state"] == "resume"]
            dispatchable = bool(cars) or bool(resumable)
            if paused is not None:
                stop_banner(
                    docs / "status.md",
                    "paused (docs/pause present)",
                    "no new reservations; delete docs/pause and relaunch to "
                    "resume ({} in-flight train(s) already wrapped safely).".format(
                        len(parked)
                    ),
                )
                return EXIT_PAUSED
            if needs_human_ask:
                _write_runstate(docs, "NEEDS-HUMAN", needs_human_ask)
                stop_banner(docs / "status.md", "NEEDS-HUMAN", needs_human_ask)
                return EXIT_NEEDS_HUMAN
            if blacked_out and dispatchable:
                # Inside the window with work available: wait it out — a
                # single walk-away launch survives the blackout (spec §12).
                wake = blackout_wake(
                    read_declared(docs / "blackout", ""),
                    datetime.datetime.utcnow(),
                )
                time.sleep(min(wake or 60, 60))
                continue
            if waiting and not dispatchable:
                _write_runstate(docs, "RUNNING")
                stop_banner(
                    docs / "status.md",
                    "WAITING on rate limits",
                    "every dispatchable train is rate-limited; relaunch later.",
                )
                return EXIT_WAITING
            if not dispatchable and not waiting:
                break  # frontier + lanes drained — evaluate the end state

        # Poll workers; every exit is a rescan trigger (dynamic refill).
        exited = [
            (t, a["proc"].poll())
            for t, a in list(active.items())
            if a["proc"].poll() is not None
        ]
        for tid, code in exited:
            handle_exit(tid, code)
        if not exited:
            time.sleep(args.poll_seconds)

    # --- end state (spec §10: run-state is a generated dispatcher outcome) ---
    telemetry_summary(journal)  # the §13 rollup for the completed run
    integrated = [
        t for t, p in parked.items() if p["state"] in ("integrated", "blocked-done")
    ]
    attention = [
        t
        for t, p in parked.items()
        if p["state"] in ("quarantined", "needs-human", "needs-re-review", "rework")
        or (p["state"] == "train-end" and p["wis"])
    ]
    blocked_done = [t for t, p in parked.items() if p["state"] == "blocked-done"]
    # The integrated disposition — not the possibly-stale dev checkout — is
    # what DONE/BLOCKED are judged from.
    reg_rows = registry_rows_at(root, INTEGRATION_REF) or schedule.load_rows(
        root / "docs" / "requirements" / "work-items.csv"
    )
    wis = schedule.load_wis(reg_rows)
    reserved = set(list_reservations(root))
    queued_left = any(w["status"] == "queued" and w["id"] not in reserved for w in wis)
    blocked_rows = any(w["status"] == "blocked" for w in wis)
    summary = (
        "trains: {} integrated ({} blocked-disposition), {} needing attention "
        "(re-review/rework/quarantine/partial); {} unreserved queued WI(s) "
        "remain".format(
            len(integrated),
            len(blocked_done),
            len(attention),
            sum(1 for w in wis if w["status"] == "queued" and w["id"] not in reserved),
        )
    )
    if attention:
        _write_runstate(docs, "RUNNING")
        stop_banner(
            docs / "status.md",
            "trains need attention (re-review / rework / quarantine)",
            summary,
        )
        return EXIT_STALL
    if queued_left:
        _write_runstate(docs, "RUNNING")
        stop_banner(docs / "status.md", "build-out wave complete", summary)
        return EXIT_DONE
    unpublished = integration_head(root)
    if unpublished and unpublished != head_sha_full(root):
        # Everything integrated but the development projection lags (deferred
        # publication — usually a dirty checkout): RUNNING, not DONE; the next
        # launch resumes the publish idempotently.
        _write_runstate(docs, "RUNNING")
        stop_banner(
            docs / "status.md",
            "integration complete; publication deferred",
            summary + " — clean the checkout and relaunch to publish.",
        )
        return EXIT_DONE
    if blocked_rows:
        _write_runstate(docs, "BLOCKED")
        stop_banner(docs / "status.md", "run-state=BLOCKED", summary)
        return EXIT_BLOCKED
    _write_runstate(docs, "DONE")
    stop_banner(docs / "status.md", "run-state=DONE", summary)
    return EXIT_DONE


def head_sha_full(root):
    """Full HEAD sha (reservation bases are exact, never abbreviated)."""
    code, out = git(root, "rev-parse", "HEAD")
    return out if code == 0 else ""


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
        help="DEPRECATED (WI-181; one compatibility window — the dispatcher's "
        "--wi/--train worker assignment replaces tracks): drive one parallel "
        "development lane: every coordination file "
        "(run-state, status.md excerpt, iteration logs + index) "
        "resolves under docs/tracks/<track>/ and the session must be on branch "
        "llm/<track> in its own worktree. Omit for single-lane operation "
        "(default: the AGENT_TRACK env var). See process-options.md "
        "'Parallel tracks'.",
    )
    ap.add_argument(
        "--wi",
        default=None,
        help="worker assignment (with --train): the assigned traincar's ordered "
        "constituent WI list, e.g. 'WI-201' or 'WI-201;WI-204'. The worker "
        "builds each in order on the train branch and reports through commit "
        "trailers — no lane status/next/run-state file "
        "(docs/specs/parallel-wi-dispatch.md §6).",
    )
    ap.add_argument(
        "--train",
        default=None,
        help="worker assignment (with --wi): the train id; the worktree must "
        "be on branch llm/train/<train> (the dispatcher creates it).",
    )
    ap.add_argument(
        "--worktree",
        default=None,
        help="worker assignment: the leased linked worktree to run in "
        "(becomes the effective --root; default: --root itself).",
    )
    ap.add_argument(
        "--base",
        default=None,
        help="worker assignment: the train's integration base commit (from "
        "the reservation metadata). Default: HEAD at worker start.",
    )
    ap.add_argument(
        "--rework",
        default=None,
        help="worker assignment: a findings file (review verdict) to embed in "
        "the worker prompt as the rework scope — assignment-scoped state, "
        "replacing the lane rework-wi pointer.",
    )
    ap.add_argument(
        "--jobs",
        default=None,
        help="launch the PARALLEL DISPATCHER with this worker ceiling: an "
        "integer (1 = explicit serial mode) or 'auto' (adaptive up to the "
        "AGENT_JOBS_CEILING env, default 2). Presence of this flag — or the "
        "AGENT_JOBS env var — selects dispatcher mode; absent keeps the "
        "legacy resume loop (docs/specs/parallel-wi-dispatch.md §4).",
    )
    ap.add_argument(
        "--worker-iterations",
        type=int,
        default=12,
        help="dispatcher mode: per-worker session budget (default 12)",
    )
    ap.add_argument(
        "--poll-seconds",
        type=float,
        default=2.0,
        help="dispatcher mode: worker poll cadence in seconds (default 2)",
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
        "against the in-process phase (default: AGENT_MODEL_MAP env var)",
    )
    ap.add_argument(
        "--cmd-map",
        default=os.environ.get("AGENT_CMD_MAP", ""),
        help='per-phase agent COMMAND template map "REVIEW-B=gemini -p '
        '{prompt},BUILD=claude -p {prompt} --model {model}" matched against '
        "the in-process phase, falling back to the single AGENT_CMD template — "
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

    # A worker runs in its leased linked worktree: --worktree IS the effective
    # root (branch guard, sessions, policy reads all resolve there). WI-181.
    if args.worktree:
        root = Path(args.worktree).resolve()
        if not root.is_dir():
            print(
                "agent_loop: --worktree {} does not exist".format(root),
                file=sys.stderr,
            )
            return EXIT_PREFLIGHT
    else:
        root = Path(args.root).resolve()
    docs = root / "docs"

    # Dispatcher mode (WI-182, SR-061): --jobs (or the AGENT_JOBS env the
    # migrated launchers wire) selects the parallel dispatcher. A worker
    # assignment, legacy track, or interactive sitting always wins — those are
    # explicit per-process roles the dispatcher itself launches or replaces.
    jobs_opt = (
        args.jobs
        if args.jobs is not None
        else (os.environ.get("AGENT_JOBS", "").strip() or None)
    )
    if jobs_opt is not None and not (
        args.wi or args.train or args.track or args.interactive
    ):
        args.jobs = jobs_opt
        return dispatch_run(args, root)
    template = (
        args.agent_cmd
        if args.agent_cmd is not None
        else os.environ.get("AGENT_CMD", "")
    )
    try:
        model_map = parse_map(args.model_map)
        cmd_map = parse_map(args.cmd_map)  # same "KEY=value" syntax
        prompt_map = parse_map(args.prompt_map)  # phase -> prompt-template FILE
        tier_map = parse_map(args.tier_map)  # phase -> tier
        prefer_map = parse_map(args.prefer_map)  # phase -> registry id
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
    # (run-state, status.md, iteration/) under docs/tracks/<track>/;
    # the repo-singular policy files (gate/gate-policy/push-policy/privacy-check/
    # guardrails-policy) always stay at docs/. No track = docs/ itself, so
    # single-lane operation is unchanged (preflight already slug-validated).
    track = sanitize_track(args.track) if args.track else None
    if track:
        # One compatibility window (WI-181): old behavior unchanged, loudly.
        print(
            "agent_loop: WARNING - --track is deprecated (WI-181): the "
            "dispatcher's explicit --wi/--train worker assignment replaces "
            "long-lived tracks. Legacy behavior continues for one "
            "compatibility window (process-options.md 'Parallel tracks').",
            file=sys.stderr,
        )
    # --- worker assignment mode (WI-181, SR-060) -----------------------------
    # worker != None switches the loop from "resume from the lane" to "build
    # the explicit assignment": no lane status/run-state/pause/next-wi reads or
    # writes, no generated-artifact regeneration, train-scoped collision-safe
    # logs + review evidence, result = committed trailers + the exit code.
    worker = None
    if args.wi and args.train:
        base = (args.base or "").strip() or head_sha(root)
        code, _ = git(root, "rev-parse", "--verify", "--quiet", base + "^{commit}")
        if code != 0:
            # A garbage base would make every evidence scan empty and burn the
            # whole iteration budget building "incomplete" work — fail closed.
            print(
                "agent_loop: --base {!r} does not resolve to a commit in this "
                "worktree".format(base),
                file=sys.stderr,
            )
            return EXIT_PREFLIGHT
        worker = {
            "train": sanitize_train(args.train),
            "assigned": parse_wi_list(args.wi),
            "base": base,
            "rows": load_wi_registry(root),
            # The scheduler's view of the same registry, for the §7
            # continuation re-check (classifier eligibility per constituent).
            "sched": {
                w["id"]: w
                for w in schedule.load_wis(
                    schedule.load_rows(
                        root / "docs" / "requirements" / "work-items.csv"
                    )
                )
            },
            "rework": "",  # in-process rework note (a CHANGES-REQUESTED verdict)
        }
        if args.rework:
            rp = Path(args.rework)
            if not rp.is_absolute():
                rp = root / args.rework
            try:
                worker["rework"] = rp.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                print(
                    "agent_loop: cannot read --rework {}: {}".format(rp, exc),
                    file=sys.stderr,
                )
                return EXIT_PREFLIGHT
    lane = lane_dir(docs, track)
    lane.mkdir(parents=True, exist_ok=True)
    status_path = lane / "status.md"
    track_preamble = ""
    if track:
        track_preamble = (
            "You are driving the '{t}' development track. Wherever the "
            "instructions below say docs/status.md, docs/plan.md or "
            "docs/run-state, use the docs/tracks/{t}/ copy instead — that "
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
    # A worker's resume surface is its assignment, not status.md — the size
    # tripwire is the integrator's concern, not the worker's.
    warn = None if worker else status_size_warning(lane / "status.md", warn_bytes)
    if warn:
        print("agent_loop: WARNING - " + warn, file=sys.stderr)

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
        phase, model = session_model(model_map, args.model)
        # Explicit interactive template wins; then the per-phase map; then the
        # default — so a REVIEW-phase interactive sitting uses the same
        # provider routing the unattended leg would.
        itemplate = (
            args.interactive_cmd
            if args.interactive_cmd is not None
            else os.environ.get("AGENT_CMD_INTERACTIVE", "")
            or session_template(cmd_map, template, phase)
        )
        print(
            "=== one interactive session | track={} phase={} model={} ===".format(
                track or "—", phase or "—", model or "—"
            )
        )
        argv = build_argv(
            itemplate,
            model,
            compose_session_prompt(
                model,
                None,
                resume_reconcile,
                track_preamble,
                args.prompt,
                guardrails_policy,
                root,
                warned_no_core,
            )[0],
        )
        proc = subprocess.run(argv, cwd=str(root))
        return proc.returncode

    print("=== unattended coordinator (scripts/agent_loop.py) ===")
    print("repo: {} | branch: {}".format(root, branch or "(none)"))
    if worker:
        print(
            "worker assignment: train={} wi={} base={} (result = committed "
            "trailers + exit code; no lane files)".format(
                worker["train"], ";".join(worker["assigned"]), worker["base"][:12]
            )
        )
    else:
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
    if worker:
        tag = "{}-".format(worker["train"])
    else:
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
    # A worker has no lane run-state (spec §10) — its state is always RUNNING
    # until its committed evidence says otherwise (worker_endstate below).
    state = (
        "RUNNING" if worker else read_declared(lane / "run-state", "RUNNING").upper()
    )

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
    # Worker review evidence is train-scoped and collision-safe (SR-060): two
    # parallel workers' committed verdicts/scoreboards must never collide at
    # integration, so each train gets its own reviews/<train>/ directory.
    reviews_dir = (docs / "reviews" / worker["train"]) if worker else (lane / "reviews")
    scoreboard = reviews_dir / "scoreboard.txt"
    cooldowns = {}  # model id -> epoch it is available again (per-model backoff)
    review_queue = []  # the pending review phases for the current round
    # The build-vs-design-check phase for the next non-review/non-critique
    # session, held in-process now that docs/run-phase is retired (WI-180): the
    # escalation paths set it to DESIGN-CHECK, everything else routes BUILD.
    next_phase = "BUILD"
    round_verdicts = []  # (phase, Verdict, provider, model_id) collected this round
    rounds = []  # accumulated round dicts the escalation policy reads
    page_fails_since = 0  # WI-171: rounds index the shared-failure tally counts
    # from — advanced to len(rounds) each time a page dispatches so an
    # already-paged strong-tier fail can't re-page forever (only NEW fails do).
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

    # --- worker end-state evaluation (WI-181) ---------------------------------
    def worker_endstate():
        """(exit_code, label, detail) when the assignment reached an end state,
        else None — judged ONLY from committed evidence + in-process queues:
        EXIT_BLOCKED when a Blocked-WI trailer names an assigned WI (the
        integrator turns it into the durable disposition, Slice F); EXIT_DONE
        when every assigned WI carries its WI trailer, the tree is clean, and
        no review/critique/rework is pending. A worker never reads run-state."""
        built, blocked_map = train_evidence(root, worker["base"])
        hit = [w for w in worker["assigned"] if w in blocked_map]
        if hit:
            return (
                EXIT_BLOCKED,
                "BLOCKED",
                "\n".join(
                    "{} blocked — BlockRef: {}".format(
                        w, blocked_map[w] or "(none committed — a finding)"
                    )
                    for w in hit
                ),
            )
        remaining = [w for w in worker["assigned"] if w not in built]
        if remaining:
            return None
        if review_queue or critique_queue or worker["rework"]:
            return None  # built, but the train's review cycle is still open
        if working_tree_dirty(root):
            return None  # committed evidence only — a dirty tree is not done
        return (
            EXIT_DONE,
            "DONE",
            "every assigned WI ({}) carries its trailer commit on {}{}".format(
                ";".join(worker["assigned"]),
                TRAIN_BRANCH_PREFIX + worker["train"],
                "; review round approved" if managed and rp_int >= 1 else "",
            ),
        )

    def worker_exit(end):
        """Print the worker's end banner (never a status.md excerpt — a worker
        has no resume surface) and hand the exit code to the dispatcher."""
        code_, label, detail = end
        print(
            "\n=== worker {} [{}]: {} ===".format(
                worker["train"], ";".join(worker["assigned"]), label
            )
        )
        if detail:
            print(detail)
        return code_

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
        # A worker ignores docs/pause: pause stops NEW RESERVATIONS at the
        # dispatcher boundary (spec §12); an in-flight worker finishes its
        # current safe boundary and remains recoverable.
        paused = None if worker else pause_reason(lane)
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
        # Worker end-state check BEFORE spending a session: a resumed worker
        # whose evidence is already complete (or blocked) exits immediately —
        # recovery reconstructs the same verdict from git alone (spec §11).
        current_wi = None
        if worker:
            end = worker_endstate()
            if end:
                return worker_exit(end)
            built, _blk = train_evidence(root, worker["base"])
            remaining = [w for w in worker["assigned"] if w not in built]
            current_wi = (
                remaining[0]
                if remaining
                else (worker.get("rework_wi") or worker["assigned"][-1])
            )
            # §7 continuation re-check (WI-183): before the lane takes the next
            # constituent of a MULTI-WI traincar, the classifier must still
            # permit optimistic grouping — a POSITIVE conflict (spine/gate/
            # attestation/protected/high-risk/critique/checkpoint) ends the
            # train EARLY instead of building inside a shared review scope.
            # Missing classification is NOT a newly-visible conflict: the
            # dispatcher already fails closed at packing, and an explicit
            # assignment is dispatcher-authorized. Built evidence stands; the
            # dispatcher releases the unstarted reservations (SR-062).
            if remaining and len(worker["assigned"]) > 1:
                sched_wi = worker["sched"].get(current_wi)
                sched_class, reasons = (
                    schedule.classify(sched_wi)
                    if sched_wi is not None
                    else (schedule.SCHED_UNCLASSIFIED, ["unclassified:missing-row"])
                )
                if sched_class in (
                    schedule.SCHED_SPINE_SERIAL,
                    schedule.SCHED_PROTECTED,
                    schedule.SCHED_SINGLE_WI,
                ):
                    print(
                        "\n=== worker {} [{}]: TRAIN-END (early) ===".format(
                            worker["train"], ";".join(worker["assigned"])
                        )
                    )
                    print(
                        "continuation refused at {}: {} — built {} stay(s) "
                        "accepted-on-train; the dispatcher releases the "
                        "unstarted constituent(s).".format(
                            current_wi,
                            ";".join(reasons),
                            ";".join(sorted(built)) or "(none)",
                        )
                    )
                    return EXIT_TRAIN_END
        session = "{:03d}".format(
            next_session_number(iter_dir, worker["train"] if worker else None)
        )
        stamp = time.strftime("%Y%m%d-%H%M%S")
        # The WI this session claims (WI-137) — recorded as a `# wi:` header line
        # + an index column. A worker's is its assignment's current WI; otherwise,
        # with docs/next-wi retired (WI-180), the only durable per-session scope
        # pointer is a rework override; empty when neither.
        rework_wi = "" if worker else read_declared(lane / "rework-wi", "")
        wi_label = current_wi if worker else rework_wi
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
                phase = next_phase
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
                # A worker pins the BUILD tier from its reserved WI row's
                # BuildTier (WI-181 — the per-WI pin that used to ride
                # docs/next-wi); the phase default covers an empty cell, and an
                # escalation override still wins (tier-up-never-down).
                if worker and current_wi:
                    row_tier = agent_route.normalize_tier(
                        (worker["rows"].get(current_wi, {}).get("BuildTier") or "")
                        .strip()
                        .lower()
                    )
                    if row_tier in agent_route.TIER_ORDER:
                        tier = row_tier
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
                # (A worker never writes run-state — its exit code is the page.)
                if not worker:
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
            # A worker's verdict filename names the exact reviewed code HEAD
            # (SR-060) — the review belongs to (train scope, reviewed commit),
            # never to a mutable branch tip.
            reviewed_sha = ""
            if worker:
                reviewed_sha = (
                    impl_range.split("..")[1]
                    if impl_range and ".." in impl_range
                    else head_sha(root)
                ) or ""
            if is_review:
                verdict_path = reviews_dir / (
                    "{}-{}-{}.md".format(session, phase, reviewed_sha[:7])
                    if worker
                    else "{}-{}.md".format(session, phase)
                )
                verdict_path.parent.mkdir(parents=True, exist_ok=True)
                body = reviewer_prompt(prompt_templates, phase, verdict_path)
            elif is_critique:
                verdict_path = reviews_dir / (
                    "{}-CRITIQUE-{}.md".format(session, reviewed_sha[:7])
                    if worker
                    else "{}-CRITIQUE.md".format(session)
                )
                verdict_path.parent.mkdir(parents=True, exist_ok=True)
                brief = critique_brief(root, docs, critique_scope)
                body = critique_prompt(prompt_templates, verdict_path, brief)
            elif worker:
                # Every non-review worker session builds from the assignment
                # prompt — never the resume-from-status default and never a
                # repo prompt-map template (the assignment is the whole scope).
                body = worker_prompt(
                    root,
                    worker["rows"],
                    current_wi,
                    worker["train"],
                    worker["base"],
                    worker["rework"],
                )
            elif phase in prompt_templates:
                body = prompt_templates[phase]
            else:
                body = None
            prompt, guarded = compose_session_prompt(
                model,
                body,
                resume_reconcile,
                track_preamble,
                args.prompt,
                guardrails_policy,
                root,
                warned_no_core,
            )
            if (
                rework_wi
                and not is_review
                and not is_critique
                and phase in ("", "BUILD")
            ):
                prompt = (
                    "REWORK OVERRIDE: docs/rework-wi names {}. Rework that reviewed "
                    "scope and its recorded findings before taking new "
                    "work.\n\n---\n\n{}".format(rework_wi, prompt)
                )
        else:
            phase, model = session_model(model_map, args.model)
            tmpl = session_template(cmd_map, template, phase)
            prompt, guarded = compose_session_prompt(
                model,
                worker_prompt(
                    root,
                    worker["rows"],
                    current_wi,
                    worker["train"],
                    worker["base"],
                    worker["rework"],
                )
                if worker
                else None,
                resume_reconcile,
                track_preamble,
                args.prompt,
                guardrails_policy,
                root,
                warned_no_core,
            )
        if not model and "{model}" in tmpl:
            print(
                "agent_loop: the session's command template carries a {model} "
                "placeholder but no model is configured for this phase "
                "(--model / --model-map / AGENT_MODEL).",
                file=sys.stderr,
            )
            return EXIT_PREFLIGHT
        print(
            "=== session {} [{}] ({}/{}) | phase={} model={}{} ===".format(
                session,
                worker["train"] if worker else (track or "single"),
                i,
                args.max_iterations,
                phase or "—",
                model or "—",
                " wi={}".format(current_wi) if worker else "",
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
        state = (
            "RUNNING"
            if worker
            else read_declared(lane / "run-state", "RUNNING").upper()
        )

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
            "train": worker["train"] if worker else "",
            "base": worker["base"][:12] if worker else "",
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
        # A worker never regenerates the iteration index: it is a GENERATED
        # root artifact the integrator rebuilds on the composed tree (spec
        # §5.1) — two workers regenerating it would collide at integration.
        if not worker:
            regenerate_index(lane)
        # Commit the coordinator's own bookkeeping now, in its own telemetry
        # commit — never let it ride the next session's work commit or dangle
        # (WI-137). The review scoreboard is committed at its own write below.
        commit_telemetry(
            root,
            tag + session,
            "{} {}".format(phase or "—", outcome),
            [log_path] if worker else [log_path, lane / "iteration_index.md"],
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
                    rounds, route_constants, swapped, at_top_tier, page_fails_since
                )
                print(
                    "escalate: {} — {}".format(decision["action"], decision["reason"])
                )
                # A worker's rework scope is assignment-scoped in-process state
                # (SR-060) — never the lane's tracked docs/rework-wi pointer,
                # which a train branch must not carry. The verdict text itself
                # is embedded in the next build session's prompt.
                if worker and merged == "CHANGES-REQUESTED":
                    worker["rework"] = "\n".join(
                        (rv.text or "").strip()
                        for (_ph, rv, _f, _m) in round_verdicts
                        if (rv.text or "").strip()
                    )
                    worker["rework_wi"] = last_impl_wi or ""
                    print(
                        "dispatch: CHANGES-REQUESTED -> assignment-scoped "
                        "rework of {}".format(worker["rework_wi"] or "the train")
                    )
                elif worker and merged == "APPROVE":
                    worker["rework"] = ""
                    worker["rework_wi"] = ""
                round_verdicts = []
                if worker:
                    pass  # handled above — no lane rework-wi file in worker mode
                elif merged == "CHANGES-REQUESTED" and last_impl_wi:
                    rework_path = lane / "rework-wi"
                    rework_path.write_text(last_impl_wi + "\n", encoding="utf-8")
                    commit_telemetry(
                        root, session, "review rework scope", [rework_path]
                    )
                    print(
                        "dispatch: CHANGES-REQUESTED -> rework override {} "
                        "takes precedence".format(last_impl_wi)
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
                    # WI-171: this page has now surfaced the current round history
                    # to a human (attended) or a design-check (autonomous). Re-arm
                    # the shared-failure tally so the same already-paged strong-tier
                    # fails can't re-page every subsequent round — only NEW fails
                    # recorded after this dispatch accumulate toward the next page.
                    page_fails_since = len(rounds)
                    fa = agent_route.failure_action(gate_policy)
                    print("route/failure ({}): {}".format(fa["mode"], fa["note"]))
                    if fa["mode"] == "attended":
                        if not worker:
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
                        next_phase = "DESIGN-CHECK"
                elif decision["action"] == "swap-implementer":
                    if last_impl_family:
                        impl_exclude = {last_impl_family}
                    swapped = True
                    critique_queue = []  # the artifact will change; re-critique later
                    next_phase = "BUILD"
                elif decision["action"] == "tier-up":
                    impl_tier_override = "strong"
                    at_top_tier = True
                    critique_queue = []
                    next_phase = "BUILD"
                elif merged == "CHANGES-REQUESTED":
                    critique_queue = []
                    next_phase = "BUILD"
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
                            if not worker:
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
                            next_phase = "DESIGN-CHECK"
                    else:
                        # Rework: back to BUILD; a re-critique schedules after the
                        # reworked build commits.
                        next_phase = "BUILD"
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
                # The review round follows the reviewer dial (S8). A traincar
                # is ONE review scope (WI-183, SR-062): a worker schedules the
                # round only once EVERY assigned WI is built, and the round
                # covers the combined train diff base..HEAD — never a per-WI
                # slice of it. An intermediate constituent commit is
                # accepted-on-train (locally green and committed), not
                # reviewed; the cycle comes once, at the end.
                schedule_review = rp_int >= 1
                if worker and schedule_review:
                    built_now, _blk = train_evidence(root, worker["base"])
                    schedule_review = all(w in built_now for w in worker["assigned"])
                    if schedule_review:
                        impl_range = "{}..{}".format(worker["base"], after)
                if schedule_review:
                    round_verdicts = []
                    review_queue = ["REVIEW-A"] + (["REVIEW-B"] if rp_int >= 2 else [])
                    print(
                        "dispatch: review-policy {} -> scheduling review round "
                        "{}{}".format(
                            rp_int,
                            review_queue,
                            " over the whole train diff" if worker else "",
                        )
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
            elif phase == "DESIGN-CHECK":
                # The design-check ruling has run (its verdict is in the commit /
                # log); resume building. Without a tracked run-phase this reset is
                # in-process (WI-180) — the agent no longer advances a phase file.
                next_phase = "BUILD"

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

        # Worker end-state after the session too — a completed assignment must
        # exit DONE here, not spend the remaining budget re-checking at the top.
        if worker:
            end = worker_endstate()
            if end:
                return worker_exit(end)

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
