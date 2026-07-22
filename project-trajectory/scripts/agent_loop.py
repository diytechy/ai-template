#!/usr/bin/env python3
"""Unattended agent entry point: dispatcher, assigned worker, or interactive session.

Implements the walk-away protocol (process-options.md "Unattended operation
(walk-away runs)"). A plain invocation runs the parallel dispatcher: it derives
the ready WI frontier, reserves traincars in Git, launches explicit worker
assignments, and integrates their committed evidence. ``--wi``/``--train`` runs
one dispatcher-assigned worker; ``--interactive`` runs one attached hands-on
session. The retired serial resume loop and its status/run-state input ladder are
not CLI modes. Ported from a field-proven PowerShell coordinator (NotHomeWrecker
trigger.ps1), which this one cross-platform implementation supersedes. Stdlib
only, Python 3.8+.

The agent invocation is a command template — the AGENT_CMD slot in the root
agent-resume.{cmd,sh} launchers (or --agent-cmd / the AGENT_CMD env var).
`{model}` and `{prompt}` placeholders are substituted per session; a template
without `{prompt}` delivers the prompt on the child's STDIN instead (WI-216 —
immune to the OS command-line caps; see build_argv/run_session).
Empty template -> guidance and exit 2 (the launchers ship inert, like run.*).

CONSENT: an unattended run typically wires the agent CLI's permission-bypass
flag into AGENT_CMD — sessions then run with no permission prompts. The human
consents by filling the slot, declaring the gate policy (docs/gate-policy),
and running this; git + CI remain the enforcement floor. The banner restates
this every run.

During worker/review sessions and dispatcher coordination this module:
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
  - honors docs/pause: a graceful-pause request (the file present) stops the
    dispatcher at the next session boundary — the in-flight assignment finishes
    and commits normally, never a mid-session kill; deleting the file resumes;
  - honors docs/blackout: a declared `HH:MM-HH:MM` UTC weekday window inside
    which no new session starts — the in-flight one wraps normally, then the
    loop waits the window out and resumes automatically (a single launch
    survives the blackout). Absent/empty/malformed or start==end = disabled;
    the scaffold ships a 12:00–19:00 default;
  - counts a no-commit worker session toward the stall guard (git HEAD unmoved) —
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
cap; ready spine/gate/attestation WIs cluster into ONE spine-only traincar —
spine packs with spine, never with anything else (WI-204) — which serializes
whole-project with every other lane drained, as does protected;
one spine train at a time), atomically reserves each selected traincar's constituent WIs
(refs/llm/reservations/WI-### — one commit-tree metadata commit + one
update-ref --stdin zero-old-value transaction, all-or-none), leases a linked
worktree per train (../<repo>-trains/<id>), and runs Slice-C workers in
parallel up to the ceiling, rescanning on every worker exit (dynamic refill —
never a static wave). A built train parks ready-to-integrate with its
reservations held for the integrator (Slice F); docs/pause stops new
reservations at the next boundary while in-flight workers finish;
out/dispatch/ is a rebuildable journal/cache, never authority (§11); root
docs/run-state becomes a generated dispatcher outcome. --jobs 1 is the
explicit serial mode. A plain launch IS the dispatcher (WI-210, one engine /
one selection path): absent --jobs/AGENT_JOBS resolves to the §6 default of
two workers — the legacy serial resume driver and its --track lanes are
retired. The two-worker promotion is GATED (WI-186, SR-065): a repo holds at
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

A per-worktree lockfile (out/agent-loop.lock) stops two coordinators grinding
one checkout — the dispatcher, a worker, and an --interactive sitting all take
it (one coordinator per checkout; the OS releases it on process death). The
retired --track lanes' judgment duties are re-homed once in process-options.md
"Unattended operation" (WI-210): intake/triage of new scope belongs to the
human + the gate-stage sessions; drained-queue and NEEDS-HUMAN surfacing are
dispatcher-generated (the end-state banner + root docs/run-state).

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

Contracts: IF-015 — the interface seam this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv). The WI-218 split re-homed IF-041 (agent-CLI invocation) to agent_session.py, IF-037 (declared-surface reads) to agent_common.py, and IF-055 (the schedule seam) to agent_dispatch.py with their code; the split-out layers provide back over IF-064..IF-067.
"""

import argparse
import atexit
import datetime
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Sibling scripts (the S8 routing/scoring half + the WI-218 split-out layers).
# Run as a subprocess the loop's own dir is sys.path[0] so a plain import
# resolves; the guard covers an in-process import (a test) whose sys.path
# doesn't yet carry scripts/ — the same sanctioned-sibling-import idiom
# gen_trajectory uses.
try:
    import agent_common
    import agent_dispatch
    import agent_route
    import agent_session
    import plan_runner
    import schedule
    import score_reviews
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import agent_common
    import agent_dispatch
    import agent_route
    import agent_session
    import plan_runner
    import schedule
    import score_reviews

# The WI-218 split: the session-launch layer (slice B), the shared coordinator
# primitives + the dual-plan runner (slice C), and the parallel dispatcher/
# integrator (slice D) live in their own modules. These bindings keep
# agent_loop's public surface (tests, downstream imports, monkeypatch targets)
# and its internal callers unchanged. Mutable internals (the lock's held
# descriptor) are NOT re-bound — they live only in their home module, so there
# is exactly one lock namespace per process.
split_cmd = agent_session.split_cmd
build_argv = agent_session.build_argv
parse_json_result = agent_session.parse_json_result
summarize_session_line = agent_session.summarize_session_line
echo_session_line = agent_session.echo_session_line
_stdout_is_tty = agent_session._stdout_is_tty
_enable_windows_vt = agent_session._enable_windows_vt
LiveStatus = agent_session.LiveStatus
_codex_lastmsg_setup = agent_session._codex_lastmsg_setup
_codex_lastmsg_read = agent_session._codex_lastmsg_read
run_session = agent_session.run_session

EXIT_DONE = agent_common.EXIT_DONE
EXIT_PREFLIGHT = agent_common.EXIT_PREFLIGHT
EXIT_BLOCKED = agent_common.EXIT_BLOCKED
EXIT_STALL = agent_common.EXIT_STALL
EXIT_WAITING = agent_common.EXIT_WAITING
EXIT_BUDGET = agent_common.EXIT_BUDGET
EXIT_NEEDS_HUMAN = agent_common.EXIT_NEEDS_HUMAN
EXIT_PAUSED = agent_common.EXIT_PAUSED
EXIT_TRAIN_END = agent_common.EXIT_TRAIN_END
END_STATES = agent_common.END_STATES
OWNER_ONLY_PATHS = agent_common.OWNER_ONLY_PATHS
read_declared = agent_common.read_declared
pause_reason = agent_common.pause_reason
parse_blackout = agent_common.parse_blackout
blackout_wake = agent_common.blackout_wake
WI_TOKEN_RE = agent_common.WI_TOKEN_RE
TRAIN_BRANCH_PREFIX = agent_common.TRAIN_BRANCH_PREFIX
sanitize_train = agent_common.sanitize_train
parse_wi_list = agent_common.parse_wi_list
load_wi_registry = agent_common.load_wi_registry
train_evidence = agent_common.train_evidence
_clip = agent_common._clip
_read_csv_rows = agent_common._read_csv_rows
_refs = agent_common._refs
git = agent_common.git
head_sha = agent_common.head_sha
head_sha_full = agent_common.head_sha_full
working_tree_dirty = agent_common.working_tree_dirty
substantive_working_tree_dirty = agent_common.substantive_working_tree_dirty
current_state_excerpt = agent_common.current_state_excerpt
stop_banner = agent_common.stop_banner
_utf8_console = agent_common._utf8_console
acquire_lock = agent_common.acquire_lock
release_lock = agent_common.release_lock
parse_map = agent_common.parse_map
preflight = agent_common.preflight
write_session_log = agent_common.write_session_log
regenerate_index = agent_common.regenerate_index
next_session_number = agent_common.next_session_number
phase_draw_ordinal = agent_common.phase_draw_ordinal
draw_iter_dirs = agent_common.draw_iter_dirs
commit_telemetry = agent_common.commit_telemetry
_write_runstate = agent_common._write_runstate

PLAN_MODE_DUAL = plan_runner.PLAN_MODE_DUAL
wi_plan_mode = plan_runner.wi_plan_mode
run_dual_plan_round = plan_runner.run_dual_plan_round
_dp_routes = plan_runner._dp_routes
_dp_session = plan_runner._dp_session

RESERVATION_NS = agent_dispatch.RESERVATION_NS
DISPATCH_DIR = agent_dispatch.DISPATCH_DIR
TRAIN_RETRY_SECONDS = agent_dispatch.TRAIN_RETRY_SECONDS
FAULT_EXIT = agent_dispatch.FAULT_EXIT
TRAIN_BRANCH_HEADS = agent_dispatch.TRAIN_BRANCH_HEADS
INTEGRATION_REF = agent_dispatch.INTEGRATION_REF
INTEGRATE_BRANCH_PREFIX = agent_dispatch.INTEGRATE_BRANCH_PREFIX
PUBLISH_INTENT_REF = agent_dispatch.PUBLISH_INTENT_REF
STATUS_GENERATED_MARKER = agent_dispatch.STATUS_GENERATED_MARKER
PARALLEL_READY_FILE = agent_dispatch.PARALLEL_READY_FILE
_fault = agent_dispatch._fault
list_reservations = agent_dispatch.list_reservations
reservation_meta = agent_dispatch.reservation_meta
reserve_traincar = agent_dispatch.reserve_traincar
release_reservations = agent_dispatch.release_reservations
train_branch_evidence = agent_dispatch.train_branch_evidence
worktree_root = agent_dispatch.worktree_root
existing_worktrees = agent_dispatch.existing_worktrees
lease_worktree = agent_dispatch.lease_worktree
train_phase_gate = agent_dispatch.train_phase_gate
pack_traincars = agent_dispatch.pack_traincars
_Journal = agent_dispatch._Journal
integration_head = agent_dispatch.integration_head
cas_ref = agent_dispatch.cas_ref
ensure_integration_ref = agent_dispatch.ensure_integration_ref
registry_rows_at = agent_dispatch.registry_rows_at
reviewed_train_head = agent_dispatch.reviewed_train_head
train_verdicts = agent_dispatch.train_verdicts
_staging_worktree = agent_dispatch._staging_worktree
_rewrite_wi_rows = agent_dispatch._rewrite_wi_rows
synth_deliverable = agent_dispatch.synth_deliverable
generate_status = agent_dispatch.generate_status
_run_combined_bar = agent_dispatch._run_combined_bar
integrate_train = agent_dispatch.integrate_train
blocked_disposition = agent_dispatch.blocked_disposition
dual_plan_disposition = agent_dispatch.dual_plan_disposition
_intent_meta = agent_dispatch._intent_meta
publish_integration = agent_dispatch.publish_integration
parse_jobs = agent_dispatch.parse_jobs
assess_migration = agent_dispatch.assess_migration
reconcile_legacy = agent_dispatch.reconcile_legacy
resolve_ceiling = agent_dispatch.resolve_ceiling
dispatch_banner = agent_dispatch.dispatch_banner
telemetry_summary = agent_dispatch.telemetry_summary
dispatch_run = agent_dispatch.dispatch_run


# The limit-hit message a throttled headless run returns, e.g. "You've hit
# your session limit · resets 3:45pm" / "…weekly limit · resets Mon 12:00am".
LIMIT_RE = re.compile(r"limit[^\n]*?resets?\s*[:·|-]?\s*([^\n\"'}]+)", re.I)

# (The resume-from-status.md DEFAULT_PROMPT retired with the serial resume
# driver, WI-210: a session's scope is its worker assignment, a reviewer
# brief, or a critique brief — never "resume from status.md".)

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
    "output; believe nothing you did not observe. Drive the diff's REAL shipped "
    "code paths — construct the scenario and run the actual function or flow it "
    "changes; primitive probes and plausibility reading are supporting evidence, "
    "never the verdict's basis. Before hunting, name the worst failure classes "
    "THIS change admits (silent wrong content, fail-open, data loss) and hunt "
    "those first, severity-ordered. An APPROVE must mean you tried to break it "
    "and failed: map each spec Done-when item to its covering test or call it "
    "UNCOVERED, and where the diff adds a regression test for a fixed defect, "
    "confirm that test fails on the pre-fix behavior. This is an INDEPENDENT parallel "
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


# (read_ask retired with the serial driver, WI-210: the dispatcher composes
# its NEEDS-HUMAN banners from the ask it just generated — the `ask:` line in
# docs/run-state remains the WI-127 contract for humans and launchers.)


# (--track and its docs/tracks/<name>/ lane plumbing retired outright, WI-210:
# the dispatcher's explicit --wi/--train worker assignment is the only lane
# concept; docs/ is the one coordination surface and the integrator owns it.)


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


# (status_size_warning retired with the serial driver, WI-210: no session
# inherits status.md as its resume surface any more — status.md is a
# generated integrator artifact whose size the generator owns.)


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
    guardrails_policy,
    root,
    warned_no_core,
):
    """The session prompt: `body` (the worker assignment, a redacted reviewer
    prompt, or a critique brief — WI-210 retired the resume-from-status
    default) with the vendored guardrails core prepended when
    docs/guardrails-policy selects this session's model (Thread 41). A
    loop-start dirty tree adds the WI-076 reconcile note ahead of the body for
    the first session (resume_reconcile). Returns (prompt, guarded); a
    selected-but-absent core warns once, then runs without it (guardrails
    accelerate quick tiers, they never gate a run). warned_no_core is a shared
    mutable list used as the warn-once flag across calls."""
    base = resume_reconcile + body
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


# A rubric path token as it appears in a TC's Parameters/Method cell.
RUBRIC_PATH_RE = re.compile(r"docs/rubrics/[\w./\-]+\.md")


# --- the critique loop (WI-068) ------------------------------------------------
# A `Verification=Critique` requirement's subjective acceptance is adjudicated by a
# fresh, provider-heterogeneous critic against a written rubric, never the authoring
# session. All of this is gated on managed mode + a real Critique SR, so a repo with
# neither pays nothing (never-breaking).
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


# --- the serial loop's managed-routing / escalation / critique / stall state ---
# (WI-080 Slice C) What were ~24 mutable locals threaded through main() now live
# on one object behind PURE transition methods: each method mutates only this
# object and returns a decision — every print, file-write, telemetry-commit, and
# repo-context call (agent_route.select/failure_action, stop_banner, run-state
# writes) stays with the caller. See the (S8 routing / WI-068 critique / stall
# guard) call sites in main() for how these transitions are wired.
class RoutingState:
    """The serial loop's managed-routing / escalation / critique / stall state
    (S8 + WI-068 + the stall guard) behind pure transition methods (WI-080
    Slice C): methods mutate only this object and return decisions — every
    print/file-write/telemetry-commit stays with the caller."""

    def __init__(
        self, rp_int, cooldown_seconds, critique_srs, critique_max, route_constants
    ):
        self.rp_int = rp_int
        self.cooldown_seconds = cooldown_seconds
        self.route_constants = route_constants
        self.critique_srs = critique_srs
        self.critique_max = critique_max
        # --- managed-routing / reviewer-dispatch state (S8) ---
        self.cooldowns = {}  # model id -> epoch it is available again
        self.review_queue = []  # the pending review phases for the current round
        # The build-vs-design-check phase for the next non-review/non-critique
        # session, held in-process now that docs/run-phase is retired (WI-180).
        self.next_phase = "BUILD"
        self.round_verdicts = []  # (phase, Verdict, provider, model_id) this round
        self.rounds = []  # accumulated round dicts the escalation policy reads
        self.page_fails_since = 0  # WI-171: rounds index the shared-failure tally
        self.last_impl_family = None  # the FAMILY of the build under review
        self.last_impl_wi = ""  # durable rework scope on CHANGES-REQUESTED
        self.last_impl_tier = "medium"  # the tier that build ran at
        self.impl_range = None  # the build's commit range (for the tripwire diff)
        self.swapped = False  # an implementer-family swap has been applied
        self.at_top_tier = False  # the implementer tier has been raised to the top
        self.impl_tier_override = None  # escalation raised the BUILD tier
        self.impl_exclude = set()  # families to avoid for the next BUILD
        # --- critique-loop state (WI-068; vacuous when no Critique SR exists) ---
        self.critique_queue = []  # ["CRITIQUE"] when a critique round is scheduled
        self.critique_scope = set()  # the in-scope Critique SR ids for this loop
        self.critique_rounds = 0  # consecutive CHANGES-REQUESTED critique rounds
        self.critique_limit = None  # None means inf-until-APPROVE for the scope
        self.critique_exhaustion = "move-on"
        # --- stall guard ---
        self.stall = 0
        self.errors = 0  # consecutive ERROR sessions (agent unavailable)

    def pick_phase(self):
        """(phase, is_review, is_critique) for the next session: a queued review
        phase wins, then a queued critique, else the held build/design-check
        default."""
        if self.review_queue:
            return self.review_queue[0], True, False
        if self.critique_queue:
            return "CRITIQUE", False, True
        return self.next_phase, False, False

    def route_intent(self, phase, is_review, is_critique, tier_map, pinned_tier=None):
        """(tier, exclude, prefer_different) for agent_route.select — the S8
        exclude/prefer/tier rules. `pinned_tier` (a normalized valid tier or
        None, computed by the caller from a worker's BuildTier) replaces the
        phase-default BUILD tier when given; an escalation override still wins.
        Returns a FRESH exclude set each call."""
        tier = phase_tier(phase, tier_map)
        exclude = set()
        prefer_different = False
        if is_review:
            prefer_different = True
            if self.last_impl_family:
                exclude.add(self.last_impl_family)
            for _ph, _v, fam, _mid in self.round_verdicts:
                if fam:
                    exclude.add(fam)  # REVIEW-B differs from REVIEW-A too
        elif is_critique:
            prefer_different = True
            if self.last_impl_family:
                exclude.add(self.last_impl_family)
        elif phase == "BUILD" or phase == "":
            if pinned_tier is not None:
                tier = pinned_tier
            if self.impl_tier_override:
                tier = self.impl_tier_override
            if self.impl_exclude:
                exclude = set(self.impl_exclude)
                prefer_different = True
        elif phase == "DESIGN-CHECK":
            prefer_different = True
            if self.last_impl_family:
                exclude.add(self.last_impl_family)
        return tier, exclude, prefer_different

    def note_build_tier(self, tier):
        """Record the tier a BUILD/"" session ran at (the round's implementer
        tier). Called only on the non-review BUILD/"" condition, as today."""
        self.last_impl_tier = tier

    def cool(self, route_id, now, seconds=None):
        """Put a route on cooldown (per-model backoff): the parsed rate-limit
        wait when given, else the configured default."""
        agent_route.cool(
            self.cooldowns,
            route_id,
            now,
            seconds if seconds is not None else self.cooldown_seconds,
        )

    def record_review_verdict(self, phase, verdict, family, model_id):
        """Append one reviewer's verdict to the round and pop the phase it
        consumed off the review queue."""
        self.round_verdicts.append((phase, verdict, family, model_id))
        if self.review_queue:
            self.review_queue.pop(0)

    def round_ready(self):
        """True when the review queue has drained and a verdict was collected —
        the round is complete and ready to merge/escalate."""
        return (not self.review_queue) and bool(self.round_verdicts)

    def complete_round(self, round_info):
        """Record a finished round for the escalation policy and clear the
        per-round verdicts. (main() keeps the append and clear at their original
        distinct positions — see the Slice-C note — because the worker-rework
        handler reads round_verdicts between escalation and the clear.)"""
        self.rounds.append(round_info)
        self.round_verdicts = []

    def escalation(self):
        """The S8 escalation decision dict for the rounds accumulated so far."""
        return agent_route.escalate(
            self.rounds,
            self.route_constants,
            self.swapped,
            self.at_top_tier,
            self.page_fails_since,
        )

    def apply_decision(self, action, merged):
        """The STATE consequences of an escalation decision only — no I/O. The
        caller keeps the prints / failure_action / banners / run-state writes."""
        if action == "page-human":
            # Re-arm the shared-failure tally so already-paged strong-tier fails
            # can't re-page every subsequent round — only NEW fails accumulate.
            self.page_fails_since = len(self.rounds)
        elif action == "swap-implementer":
            if self.last_impl_family:
                self.impl_exclude = {self.last_impl_family}
            self.swapped = True
            self.critique_queue = []  # the artifact will change; re-critique later
            self.next_phase = "BUILD"
        elif action == "tier-up":
            self.impl_tier_override = "strong"
            self.at_top_tier = True
            self.critique_queue = []
            self.next_phase = "BUILD"
        elif merged == "CHANGES-REQUESTED":
            self.critique_queue = []
            self.next_phase = "BUILD"

    def set_design_check(self):
        """Route the next non-review/non-critique session to DESIGN-CHECK (the
        autonomous page path)."""
        self.next_phase = "DESIGN-CHECK"

    def after_design_check(self):
        """The design-check ruling has run; resume building."""
        self.next_phase = "BUILD"

    def on_committed_build(self, family, wi, commits):
        """Record a committing build: its family (the heterogeneity key), its WI
        (the durable rework scope), and its commit range (the tripwire diff)."""
        self.last_impl_family = family
        self.last_impl_wi = wi
        self.impl_range = commits

    def set_train_range(self, rng):
        """Override the impl range with a worker's whole-train diff (base..HEAD)
        — one review scope covers the combined train, not a per-WI slice."""
        self.impl_range = rng

    def schedule_review_round(self):
        """Queue a fresh review round (REVIEW-A, plus REVIEW-B at policy >= 2)
        and return the queue list for the caller's dispatch log. Called only
        when the caller's schedule_review condition holds, as today."""
        self.round_verdicts = []
        self.review_queue = ["REVIEW-A"] + (["REVIEW-B"] if self.rp_int >= 2 else [])
        return list(self.review_queue)

    def schedule_critique(self, in_scope, limit, exhaustion):
        """Queue a critique round for one build scope. A NEW scope starts a fresh
        budget; a rework of the SAME scope preserves the count so the budget
        actually bounds the loop."""
        if in_scope != self.critique_scope:
            self.critique_rounds = 0
        self.critique_limit = limit
        self.critique_exhaustion = exhaustion
        self.critique_scope = set(in_scope)
        self.critique_queue = ["CRITIQUE"]

    def record_critique_verdict(self, merged):
        """Consume the critique round and return the disposition: "rework" (back
        to BUILD), "page" (budget exhausted — the caller pages/design-checks), or
        "approved" (the loop ends). Resets the scope on page/approve."""
        self.critique_queue = []  # this round consumed
        if merged == "CHANGES-REQUESTED":
            self.critique_rounds += 1
            if (
                self.critique_limit is not None
                and self.critique_rounds >= self.critique_limit
            ):
                self.critique_rounds = 0
                self.critique_scope = set()
                return "page"
            self.next_phase = "BUILD"
            return "rework"
        self.critique_rounds = 0
        self.critique_scope = set()
        return "approved"

    def note_session(self, committed, errored):
        """Fold one session's outcome into the stall/error counters: a commit
        resets the stall; an error before work increments the error run."""
        self.stall = 0 if committed else self.stall + 1
        self.errors = self.errors + 1 if errored else 0

    def stall_verdict(self, limit):
        """None (keep going), "agent-error" (the whole stall run errored before
        working — an unavailable agent), or "stall" (a work stall)."""
        if self.stall < limit:
            return None
        return "agent-error" if self.errors >= limit else "stall"


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
        # Plain-text templates: scan only the transcript TAIL (the CLI's own
        # error surface). A full-transcript scan misread echoed prompt/spec
        # sentences like "the token limit resets at 9:00" as a throttle and
        # slept a failed session until then (repo-review 2026-07-21 L-21).
        m = LIMIT_RE.search("\n".join(output.splitlines()[-15:]))
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


def classify_outcome(reset_hint, timed_out, state, committed, data, exit_code):
    """The outcome ladder for one session — a rate limit wins as WAITING, a
    timeout is its own outcome, a declared end-state (run-state) passes through,
    a commit is COMMITTED, an agent error (is_error JSON, or a non-JSON nonzero
    exit — which also covers run_session's OSError sentinel of -1 with no JSON)
    is ERROR, else NO-COMMIT.

    `errored` marks a session that failed *before it could work* — not a rate
    limit (that wins as WAITING) or a timeout (its own outcome): the CLI reported
    an error result (is_error in JSON), or a non-JSON session exited nonzero.
    Distinct from NO-COMMIT (a healthy session that idled), so a fast-dying
    walk-away run — model retired, auth expired, CLI broke — reads as an agent
    error, not a work stall. Mirrors the error signal limit_reset_hint already
    trusts (is_error / nonzero exit), never a substring scan of the transcript.
    Reporting only: it still counts toward the stall guard (no commit), but the
    abort banner names it (Thread 45).

    Returns (outcome, errored)."""
    errored = (
        not reset_hint
        and not timed_out
        and (bool(data.get("is_error")) or (not data and exit_code != 0))
    )
    if reset_hint:
        outcome = "WAITING"
    elif timed_out:
        outcome = "TIMEOUT"
    elif state in END_STATES:
        outcome = state
    elif committed:
        outcome = "COMMITTED"
    elif errored:
        outcome = "ERROR"
    else:
        outcome = "NO-COMMIT"
    return outcome, errored


def worker_endstate(root, worker, review_open, managed, rp_int, allow_block_exit=True):
    """(exit_code, label, detail) when the assignment reached an end state,
    else None — judged ONLY from committed evidence + in-process queues:
    EXIT_BLOCKED when a Blocked-WI trailer names an assigned WI (the
    integrator turns it into the durable disposition, Slice F); EXIT_DONE
    when every assigned WI carries its WI trailer, the tree is clean, and
    no review/critique/rework is pending. A worker never reads run-state.

    Per WI the LATEST trailer wins (train_evidence, WI-239): a resumed worker
    that re-runs green and commits `WI:` supersedes its own earlier
    `Blocked-WI:`, so this reports DONE, not BLOCKED. `allow_block_exit=False`
    (the resumed worker's FIRST session, before it has run) declines to
    short-circuit on a PRE-EXISTING block so the worker gets its one chance to
    cure it; a block that still stands is honored by the post-session check
    (default True) or the next iteration."""
    built, blocked_map = train_evidence(root, worker["base"])
    hit = [w for w in worker["assigned"] if w in blocked_map]
    if hit:
        if not allow_block_exit:
            return None
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
    if review_open or worker["rework"]:
        return None  # built, but the train's review cycle is still open
    if substantive_working_tree_dirty(root):
        return None  # committed evidence only — a dirty tree (owner-only exempt) is not done
    return (
        EXIT_DONE,
        "DONE",
        "every assigned WI ({}) carries its trailer commit on {}{}".format(
            ";".join(worker["assigned"]),
            TRAIN_BRANCH_PREFIX + worker["train"],
            "; review round approved" if managed and rp_int >= 1 else "",
        ),
    )


def worker_exit_banner(worker, end):
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


def parse_args():
    """The whole CLI surface — one home for every flag + its default."""
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
        help="agent command template ({model}/{prompt} placeholders; omit "
        "{prompt} to deliver the prompt via stdin — immune to the OS "
        "command-line caps); "
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
        "--wi",
        default=None,
        help="worker assignment (with --train): the assigned traincar's ordered "
        "constituent WI list, e.g. 'WI-201' or 'WI-201;WI-204'. The worker "
        "builds each in order on the train branch and reports through commit "
        "trailers — no lane status/next/run-state file "
        "(docs/specs/parallel-wi-dispatch.md §6).",
    )
    ap.add_argument(
        "--dual-plan",
        default=None,
        metavar="WI-ID",
        help="run one dual-plan decomposition round for this queued WI (its "
        "registry row must declare PlanMode=dual) and exit: two planner "
        "sessions, the coverage pre-pass, one cross-critique + revision, the "
        "position-swapped arbiter pair, artifacts under docs/plans/DP-NNN-*/ "
        "(process-options.md 'Dual-plan decomposition'; WI-199).",
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
        help="the dispatcher's worker ceiling: an integer (1 = explicit "
        "serial mode) or 'auto' (adaptive up to the AGENT_JOBS_CEILING env, "
        "default 2). A plain launch IS the dispatcher (WI-210): absent "
        "--jobs/AGENT_JOBS resolves to 2, held at 1 until the §14 migration "
        "audits pass (docs/specs/parallel-wi-dispatch.md §4/§14).",
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
    return ap.parse_args()


def map_preflight(
    root,
    template,
    args,
    cmd_map,
    prompt_map,
    tier_map,
    prefer_map,
    managed,
    registry,
    enabled,
    reg_errors,
    enable_errors,
):
    """Assemble every up-front launchability failure (default template,
    cmd-map, prompt-map files, and the managed-routing registry/enable/tier/
    prefer checks) into one list, reading each mapped prompt file once.
    Returns (failures, prompt_templates)."""
    failures = preflight(root, template, args)
    # Every per-phase template must be as launchable as the default one — a
    # broken REVIEW-B entry must fail before iteration 1, not at the first
    # review session mid-run (the preflight contract).
    for ph, tmpl in sorted(cmd_map.items()):
        try:
            argv, _ = build_argv(tmpl, "model", "prompt")
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
                argv, _ = build_argv(m.cmd_template, "model", "prompt")
                exe = argv[0]
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
    return failures, prompt_templates


def build_worker_assignment(args, root):
    """The dispatcher's explicit worker assignment (--wi + --train): parse
    the traincar's WI list, fail closed on an unresolvable --base, and load
    the registry + scheduler views + any --rework findings. Returns
    (None, None) when this is not a worker process, (worker, None) on
    success, or (None, EXIT_PREFLIGHT) after printing its own error."""
    # --- worker assignment mode (WI-181, SR-060) -----------------------------
    # worker != None switches the loop from "resume from the lane" to "build
    # the explicit assignment": no lane status/run-state/pause/next-wi reads or
    # writes, no generated-artifact regeneration, train-scoped collision-safe
    # logs + review evidence, result = committed trailers + the exit code.
    worker = None
    if args.wi and args.train:
        base = (args.base or "").strip() or head_sha(root)
        if not base:
            # An unborn HEAD (zero-commit repo) has no integration base to
            # build evidence against — fail closed, never crash (the
            # dispatcher always assigns from an existing HEAD).
            print(
                "agent_loop: no --base and no HEAD commit to default to — a "
                "worker builds from an integration base; commit first.",
                file=sys.stderr,
            )
            return None, EXIT_PREFLIGHT
        code, _ = git(root, "rev-parse", "--verify", "--quiet", base + "^{commit}")
        if code != 0:
            # A garbage base would make every evidence scan empty and burn the
            # whole iteration budget building "incomplete" work — fail closed.
            print(
                "agent_loop: --base {!r} does not resolve to a commit in this "
                "worktree".format(base),
                file=sys.stderr,
            )
            return None, EXIT_PREFLIGHT
        assigned = parse_wi_list(args.wi)
        rows = load_wi_registry(root)
        # A dual-plan WI never builds as a direct BUILD session (fail-closed,
        # WI-199): the round has its own entry (--dual-plan) and safeguards.
        dual = [w for w in assigned if wi_plan_mode(rows.get(w, {})) == PLAN_MODE_DUAL]
        if dual:
            print(
                "agent_loop: {} declare(s) PlanMode=dual — a dual-plan WI is "
                "never a direct BUILD; run it with --dual-plan {} instead "
                "(process-options.md 'Dual-plan decomposition')".format(
                    ";".join(dual), dual[0]
                ),
                file=sys.stderr,
            )
            return None, EXIT_PREFLIGHT
        worker = {
            "train": sanitize_train(args.train),
            "assigned": assigned,
            "base": base,
            "rows": rows,
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
                return None, EXIT_PREFLIGHT
    return worker, None


def run_interactive(
    args,
    root,
    model_map,
    cmd_map,
    template,
    guardrails_policy,
    warned_no_core,
):
    """Boot exactly one hands-on session (stdio attached) and return its
    exit code — the --interactive early path, no loop. The human at the
    keyboard drives the scope (WI-210 retired the resume-from-status
    default), so the composed prompt is just the guardrails posture."""
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
        "=== one interactive session | phase={} model={} ===".format(
            phase or "—", model or "—"
        )
    )
    argv, stdin_input = build_argv(
        itemplate,
        model,
        compose_session_prompt(
            model,
            "",
            "",
            guardrails_policy,
            root,
            warned_no_core,
        )[0],
    )
    if stdin_input is None:
        # {prompt} rode argv: stdin stays the caller's terminal (hands-on).
        proc = subprocess.run(argv, cwd=str(root))
    else:
        # A no-{prompt} template pipes its prompt in, then the CLI proceeds
        # (stdout/stderr stay attached to the terminal). text=True is
        # load-bearing: a str input on a binary pipe is a TypeError.
        proc = subprocess.run(argv, cwd=str(root), input=stdin_input, text=True)
    return proc.returncode


def print_run_banner(
    root,
    branch,
    worker,
    gate_policy,
    push_policy,
    review_policy,
    managed,
    enabled,
    registry,
    guardrails_policy,
    template,
    cmd_map,
    prompt_map,
    docs,
):
    """The unattended-coordinator launch banner: the run's identity, its
    policies, the routing/guardrails posture, and the privacy warning."""
    print("=== unattended coordinator (scripts/agent_loop.py) ===")
    print("repo: {} | branch: {}".format(root, branch or "(none)"))
    if worker:
        print(
            "worker assignment: train={} wi={} base={} (result = committed "
            "trailers + exit code; no lane files)".format(
                worker["train"], ";".join(worker["assigned"]), worker["base"][:12]
            )
        )
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


class LoopContext:
    """Everything one iteration reads, built once at loop start; the
    per-iteration behavior lives in run_iteration (WI-080 Slice E). A plain
    attribute bag — no logic — so a moved body reads ctx.<name> where it
    used to read the loop-local."""


def route_session(ctx, i, current_wi, session, resume_reconcile, now):
    """Pick the phase + model + prompt for this worker session (managed
    routing or the single-model path; WI-210 — every loop session is a
    dispatcher-assigned worker session). Returns an int exit code to end the
    run (no routable model -> EXIT_NEEDS_HUMAN; a {model} template with no
    model -> EXIT_PREFLIGHT) or a `plan` dict the caller launches."""
    args = ctx.args
    root = ctx.root
    docs = ctx.docs
    status_path = ctx.status_path
    worker = ctx.worker
    managed = ctx.managed
    registry = ctx.registry
    enabled = ctx.enabled
    template = ctx.template
    model_map = ctx.model_map
    cmd_map = ctx.cmd_map
    prompt_templates = ctx.prompt_templates
    tier_map = ctx.tier_map
    prefer_map = ctx.prefer_map
    guardrails_policy = ctx.guardrails_policy
    warned_no_core = ctx.warned_no_core
    reviews_dir = ctx.reviews_dir
    st = ctx.st
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
        phase, is_review, is_critique = st.pick_phase()
        # A worker pins the BUILD tier from its reserved WI row's BuildTier
        # (WI-181 — the per-WI pin that used to ride docs/next-wi); the phase
        # default covers an empty cell, and an escalation override still wins
        # (tier-up-never-down). Computed here (the caller owns the worker row
        # read); route_intent folds it in against the phase default.
        pinned_tier = None
        if (phase == "BUILD" or phase == "") and worker and current_wi:
            row_tier = agent_route.normalize_tier(
                (worker["rows"].get(current_wi, {}).get("BuildTier") or "")
                .strip()
                .lower()
            )
            if row_tier in agent_route.TIER_ORDER:
                pinned_tier = row_tier
        tier, exclude, prefer_different = st.route_intent(
            phase, is_review, is_critique, tier_map, pinned_tier
        )
        # Per-phase draw weights (WI-236) drive a deterministic weighted rotation
        # over the unpinned legal remainder, keyed on the durable PER-PHASE draw
        # ordinal — prior same-phase sessions counted ACROSS trains from the
        # durable aggregate (WI-263, M-31: a per-train count reset to slot 0 on
        # every freshly minted train, so the weights were inert across trains) —
        # NOT the global session counter, which strides across phases and would
        # alias against the weight sum. No randomness, no new durable store.
        route_id, reason = agent_route.select(
            enabled,
            registry,
            tier,
            now,
            st.cooldowns,
            exclude,
            prefer_different,
            [prefer_map[phase]] if phase in prefer_map else (),
            agent_route.phase_weights(ctx.weight_map, phase),
            phase_draw_ordinal(ctx.draw_iter_dirs, phase),
        )
        # Log the routing decision BEFORE launch (the no-silent-swap rule).
        print("route [{}]: {}".format(phase or "—", reason))
        if route_id is None:
            # Every enabled model at the preferred tier-or-stronger is cooling
            # down or none is enabled: page rather than drop to a weaker tier.
            # (A worker never writes run-state — its exit code is the page;
            # the dispatcher generates the root run-state, spec §10.)
            stop_banner(
                status_path,
                "NEEDS-HUMAN — no routable model",
                reason + " (add/enable a model of this tier, or wait for a "
                "cooldown; the loop never silently drops to a weaker tier).\n"
                # Per-row state + the Notes cell — the declared home for the
                # provider's sign-in/install hint (e.g. `opencode auth
                # login`), so the page says what to DO, not just that it
                # paged (WI-109).
                 + agent_route.pool_context(enabled, registry, st.cooldowns, now),
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
            st.note_build_tier(tier)
        # A worker's verdict filename names the exact reviewed code HEAD
        # (SR-060) — the review belongs to (train scope, reviewed commit),
        # never to a mutable branch tip.
        reviewed_sha = ""
        if worker:
            reviewed_sha = (
                st.impl_range.split("..")[1]
                if st.impl_range and ".." in st.impl_range
                else head_sha(root)
            ) or ""
        if is_review:
            verdict_path = reviews_dir / "{}-{}-{}.md".format(
                session, phase, reviewed_sha[:7]
            )
            verdict_path.parent.mkdir(parents=True, exist_ok=True)
            # The path is fully predictable (next session number + the
            # implementer's own HEAD sha), so an UNCOMMITTED file planted here
            # before the reviewer runs would be counted as the verdict whenever
            # the review session errors. The reviewer writes the only file that
            # counts (repo-review 2026-07-21 M-22; committed plants stay
            # defeated by the sha-in-name design).
            if verdict_path.exists():
                verdict_path.unlink()
            body = reviewer_prompt(prompt_templates, phase, verdict_path)
        elif is_critique:
            verdict_path = reviews_dir / "{}-CRITIQUE-{}.md".format(
                session, reviewed_sha[:7]
            )
            verdict_path.parent.mkdir(parents=True, exist_ok=True)
            if verdict_path.exists():  # same pre-plant guard as the review path
                verdict_path.unlink()
            brief = critique_brief(root, docs, st.critique_scope)
            body = critique_prompt(prompt_templates, verdict_path, brief)
        else:
            # Every non-review session builds from the assignment prompt —
            # never a resume-from-status default (retired, WI-210) and never
            # a repo prompt-map template (the assignment is the whole scope).
            body = worker_prompt(
                root,
                worker["rows"],
                current_wi,
                worker["train"],
                worker["base"],
                worker["rework"],
            )
        prompt, guarded = compose_session_prompt(
            model,
            body,
            resume_reconcile,
            guardrails_policy,
            root,
            warned_no_core,
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
            ),
            resume_reconcile,
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
    return {
        "phase": phase,
        "is_review": is_review,
        "is_critique": is_critique,
        "model": model,
        "tmpl": tmpl,
        "prompt": prompt,
        "guarded": guarded,
        "verdict_path": verdict_path,
        "route_id": route_id,
        "route_family": route_family,
        "session_env": session_env,
    }


def session_bookkeeping(
    ctx, plan, outcome, code, commits, after, reset_hint, now, session, wi_label
):
    """The managed-routing / reviewer-dispatch consequences of one session
    (S8): cool+re-route, review-round merge/scoreboard/escalation, critique
    arbitration, committed-build scheduling, design-check reset. Returns None
    (fall through), "reroute" (the managed-WAITING re-route), or an int exit
    code (a page-human)."""
    root = ctx.root
    docs = ctx.docs
    status_path = ctx.status_path
    worker = ctx.worker
    managed = ctx.managed
    registry = ctx.registry
    gate_policy = ctx.gate_policy
    scoreboard = ctx.scoreboard
    rp_int = ctx.rp_int
    st = ctx.st
    phase = plan["phase"]
    is_review = plan["is_review"]
    is_critique = plan["is_critique"]
    verdict_path = plan["verdict_path"]
    route_id = plan["route_id"]
    route_family = plan["route_family"]
    # --- managed routing / reviewer dispatch bookkeeping (S8) -------------
    # All of this is gated on managed mode; the legacy path never enters it.
    if managed and outcome == "WAITING":
        # Generalize the rate-limit backoff PER-MODEL: cool this model and
        # re-route to another available one next iteration. select() pages if
        # none is left rather than dropping to a weaker tier (no silent swap).
        wait = seconds_until_reset(reset_hint) or st.cooldown_seconds
        st.cool(route_id, now, wait)
        print(
            "route: {} rate-limited; cooled ~{}s, re-routing".format(
                route_id, int(wait)
            )
        )
        return "reroute"
    if managed and is_review:
        if verdict_path and Path(verdict_path).exists():
            v = score_reviews.parse_verdict(
                Path(verdict_path).read_text(encoding="utf-8", errors="replace"),
                model=route_family,
            )
            if v.verdict is None:
                # A verdict file with no parseable `VERDICT:` machine line
                # (a routine LLM garble) is neither an approval nor a burnable
                # round: fail closed exactly like a missing file — cool and
                # re-route the same phase (repo-review 2026-07-21 H-1).
                st.cool(route_id, now)
                print(
                    "route: {} review [{}] verdict file has no parseable "
                    "VERDICT line; cooled, re-routing".format(route_id, phase)
                )
            else:
                st.record_review_verdict(phase, v, route_family, route_id)
        else:
            # No verdict file (errored, stalled, or the session simply did not
            # write one): cool the model and re-route the same review phase.
            st.cool(route_id, now)
            print(
                "route: {} review [{}] wrote no verdict ({}); cooled, "
                "re-routing".format(route_id, phase, outcome)
            )
        if st.round_ready():
            verdicts = [v for (_ph, v, _p, _m) in st.round_verdicts]
            merged, contradiction = score_reviews.merge_verdict(verdicts)
            # Substance/corroboration key on Family (who trained it), so a
            # cross-family overlap outweighs a same-family one; the scoreboard
            # tallies by that same Family key.
            family_substance = {}
            subs = []
            for j, (_ph, rv, rfam, _mid) in enumerate(st.round_verdicts):
                peer = (
                    st.round_verdicts[1 - j][1] if len(st.round_verdicts) == 2 else None
                )
                fams = (
                    (rfam, st.round_verdicts[1 - j][2])
                    if len(st.round_verdicts) == 2
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
            if st.impl_range and ".." in st.impl_range:
                _rc, diff_out = git(root, "diff", "--name-only", st.impl_range)
                # The whole-train range (WI-183; the only range now, WI-210)
                # legitimately carries THIS train's own committed verdicts,
                # scoreboard, and session telemetry from earlier rounds — a
                # rework round must not read them as "the implementer touched
                # a review path" (the false-fire this excludes). A gamed
                # verdict is still caught upstream: the integrator verifies
                # verdicts on the exact reviewed head (SR-096).
                own = "docs/reviews/{}/".format(worker["train"])
                changed = [
                    ln
                    for ln in diff_out.splitlines()
                    if ln.strip()
                    and not ln.replace("\\", "/").startswith(own)
                    and not ln.replace("\\", "/").startswith("docs/iteration")
                ]
            fired = score_reviews.fired_tripwires(verdicts, changed_paths=changed)
            round_info = {
                "verdict": merged or "",
                "tier": st.last_impl_tier,
                "margin": margin,
                "primary": primary,
                "tripwire": bool(fired),
                "contradiction": contradiction,
            }
            # Record the round for the escalation policy. Slice-C note: the
            # append and the round_verdicts clear (below) stay at their
            # original distinct positions rather than folding into one
            # st.complete_round() call — the worker-rework handler between
            # escalation() and the clear still reads st.round_verdicts, so a
            # single append+clear would either empty that read or hide the
            # round from escalate(). Behavior (content + console order) is
            # preserved exactly.
            st.rounds.append(round_info)
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
            decision = st.escalation()
            print("escalate: {} — {}".format(decision["action"], decision["reason"]))
            # A worker's rework scope is assignment-scoped in-process state
            # (SR-060) — never the lane's tracked docs/rework-wi pointer,
            # which a train branch must not carry. The verdict text itself
            # is embedded in the next build session's prompt.
            if merged == "CHANGES-REQUESTED":
                worker["rework"] = "\n".join(
                    (rv.text or "").strip()
                    for (_ph, rv, _f, _m) in st.round_verdicts
                    if (rv.text or "").strip()
                )
                worker["rework_wi"] = st.last_impl_wi or ""
                print(
                    "dispatch: CHANGES-REQUESTED -> assignment-scoped "
                    "rework of {}".format(worker["rework_wi"] or "the train")
                )
            elif merged == "APPROVE":
                worker["rework"] = ""
                worker["rework_wi"] = ""
            st.round_verdicts = []
            # (The lane docs/rework-wi pointer retired with the serial driver,
            # WI-210: a worker's rework scope is assignment-scoped in-process
            # state, handled above.)
            # State consequences of the escalation happen ONCE, here (WI-171
            # page re-arm, swap/tier-up/changes-requested); the branch below
            # keeps only the page path's I/O (failure_action / banner /
            # run-state). apply_decision first is safe — failure_action does
            # not read page_fails_since.
            st.apply_decision(decision["action"], merged)
            if decision["action"] == "page-human":
                fa = agent_route.failure_action(gate_policy)
                print("route/failure ({}): {}".format(fa["mode"], fa["note"]))
                if fa["mode"] == "attended":
                    # A worker never writes run-state — its exit code pages
                    # the dispatcher, which generates the root file (§10).
                    stop_banner(
                        status_path,
                        "PAGE-HUMAN — review escalation",
                        decision["reason"] + " | " + fa["note"],
                    )
                    return EXIT_NEEDS_HUMAN
                if fa.get("design_check"):
                    st.set_design_check()
    elif managed and is_critique:
        # The perceptual arbiter (WI-068): read the critic's verdict, iterate
        # BUILD<->CRITIQUE until APPROVE or the budget trips S8 escalation.
        if verdict_path and Path(verdict_path).exists():
            v = score_reviews.parse_verdict(
                Path(verdict_path).read_text(encoding="utf-8", errors="replace"),
                model=route_family,
            )
            merged = (v.verdict or "").upper()
            print(
                "critique [{}]: verdict={} findings={} scope={} ({})".format(
                    route_id,
                    merged or "?",
                    len(v.findings),
                    ",".join(sorted(st.critique_scope)) or "—",
                    verdict_path,
                )
            )
            if not merged:
                # A verdict file with no parseable `VERDICT:` machine line is
                # NOT an approval: fail closed exactly like a missing file
                # (cool + re-critique). Previously the "" fell through to
                # record_critique_verdict's else branch — scope reset, queue
                # cleared, silently approved (repo-review 2026-07-21 H-1; the
                # WI-243 "fail closed" lesson one layer down).
                st.cool(route_id, now)
                print(
                    "critique: {} verdict file has no parseable VERDICT line; "
                    "cooled, re-critiquing".format(route_id)
                )
                return None
            # record_critique_verdict resets critique_rounds on the page path,
            # so capture the exhausted count for the (byte-identical) budget
            # print BEFORE the call — the printed value is the post-increment
            # round count, i.e. pre-call rounds + 1.
            pre_rounds = st.critique_rounds
            action = st.record_critique_verdict(merged)
            if action == "page":
                # Budget exhausted -> the S8 page-the-human semantics, keyed
                # to docs/gate-policy (same failure_action the review round
                # uses). The critic gates iteration; the human owns final
                # acceptance via Attest at gate closure.
                fa = agent_route.failure_action(gate_policy)
                print(
                    "critique/budget ({}): {} CHANGES-REQUESTED round(s) >= "
                    "{} -> page-human: {}".format(
                        fa["mode"], pre_rounds + 1, st.critique_limit, fa["note"]
                    )
                )
                if fa["mode"] == "attended" or st.critique_exhaustion == "block":
                    stop_banner(
                        status_path,
                        "PAGE-HUMAN — critique budget exhausted",
                        "the critique loop hit its {}-round budget still "
                        "CHANGES-REQUESTED | {}".format(st.critique_limit, fa["note"]),
                    )
                    return EXIT_NEEDS_HUMAN
                if fa.get("design_check"):
                    st.set_design_check()
            # action == "rework" (next_phase set to BUILD) / "approved" (the
            # loop ended) need nothing more from the caller.
        else:
            # No verdict written (errored/stalled): cool + re-critique next pass
            # (the stall guard backstops a critic that never writes one).
            st.cool(route_id, now)
            print(
                "critique: {} wrote no verdict ({}); cooled, re-critiquing".format(
                    route_id, outcome
                )
            )
    elif managed and not is_review:
        if outcome in ("ERROR", "TIMEOUT"):
            st.cool(route_id, now)
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
                    int(st.cooldown_seconds),
                    " — " + note if note else "",
                )
            )
        elif outcome == "COMMITTED" and phase not in NON_BUILD_PHASES:
            st.on_committed_build(route_family, wi_label, commits)
            # The review round follows the reviewer dial (S8). A traincar
            # is ONE review scope (WI-183, SR-062): a worker schedules the
            # round only once EVERY assigned WI is built, and the round
            # covers the combined train diff base..HEAD — never a per-WI
            # slice of it. An intermediate constituent commit is
            # accepted-on-train (locally green and committed), not
            # reviewed; the cycle comes once, at the end.
            schedule_review = rp_int >= 1
            if schedule_review:
                built_now, _blk = train_evidence(root, worker["base"])
                schedule_review = all(w in built_now for w in worker["assigned"])
                if schedule_review:
                    st.set_train_range("{}..{}".format(worker["base"], after))
            if schedule_review:
                queued = st.schedule_review_round()
                print(
                    "dispatch: review-policy {} -> scheduling review round {} "
                    "over the whole train diff".format(rp_int, queued)
                )
            # The critique round is INDEPENDENT of the review dial (WI-068): it
            # fires only when this build's WI touches a Critique-verified SR.
            # Vacuous when no Critique SR exists, so a non-adopter pays nothing.
            if st.critique_srs:
                scope_wis = build_scope_wis(root, docs, commits)
                in_scope = build_scope_srs(root, docs, commits) & st.critique_srs
                if in_scope:
                    # A NEW scope starts a fresh budget; a rework of the SAME
                    # scope (a CHANGES-REQUESTED loop) preserves the count, so
                    # the budget actually bounds the loop (schedule_critique
                    # folds that reset in; critique_control does not read the
                    # round count, so the order is identical to before).
                    limit, exhaustion = critique_control(
                        docs, scope_wis, st.critique_max
                    )
                    st.schedule_critique(in_scope, limit, exhaustion)
                    print(
                        "dispatch: build touches Critique SR(s) {} -> scheduling "
                        "CRITIQUE round (budget {}, exhaustion {})".format(
                            ",".join(sorted(in_scope)),
                            "inf" if limit is None else limit,
                            exhaustion,
                        )
                    )
        elif phase == "DESIGN-CHECK":
            # The design-check ruling has run (its verdict is in the commit /
            # log); resume building. Without a tracked run-phase this reset is
            # in-process (WI-180) — the agent no longer advances a phase file.
            st.after_design_check()
    return None


def run_iteration(ctx, i):
    """One worker session end-to-end: guards, routing (route_session),
    launch, telemetry, bookkeeping (session_bookkeeping), and the outcome
    ladder (WI-210 — the loop is the dispatcher-assigned worker engine; the
    serial resume driver and its docs/pause boundary are retired: pause stops
    NEW RESERVATIONS at the dispatcher, spec §12, while an in-flight worker
    finishes its safe boundary). Returns an int exit code to END the run, or
    None to proceed to the next iteration (a `continue` path returns None
    early, so the trailing pause sleep — the last statement — is naturally
    skipped)."""
    args = ctx.args
    root = ctx.root
    lane = ctx.lane
    status_path = ctx.status_path
    worker = ctx.worker
    managed = ctx.managed
    start_dirty = ctx.start_dirty
    raw_dir = ctx.raw_dir
    iter_dir = ctx.iter_dir
    tag = ctx.tag
    use_live = ctx.use_live
    rp_int = ctx.rp_int
    st = ctx.st
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
    # (The WI-209 serial dual-plan quiet-park guard retired with the serial
    # driver, WI-210: the dispatcher auto-runs a dual row's round, so the
    # page-instead-of-idle duty has no second path left to cover.)
    # Inject the reconcile note into the first session's prompt only (see the
    # once-at-start rationale above); every later session's prompt is
    # unchanged from today.
    resume_reconcile = (
        RESUME_RECONCILE_NOTE + "\n\n---\n\n" if (i == 1 and start_dirty) else ""
    )
    # Worker end-state check BEFORE spending a session: a resumed worker
    # whose evidence is already complete (or blocked) exits immediately —
    # recovery reconstructs the same verdict from git alone (spec §11).
    # WI-239: a resumed worker's FIRST session (i == 1) is NOT short-circuited
    # by a pre-existing Blocked-WI trailer — the dispatcher only re-dispatches a
    # blocked train when the base may have been cured, so the worker gets its one
    # chance to supersede the block with a completion; a block still standing
    # after the session exits BLOCKED (the post-session check honors it).
    current_wi = None
    if worker:
        end = worker_endstate(
            root,
            worker,
            bool(st.review_queue or st.critique_queue),
            managed,
            rp_int,
            allow_block_exit=(i > 1),
        )
        if end:
            return worker_exit_banner(worker, end)
        built, _blk = train_evidence(root, worker["base"])
        remaining = [w for w in worker["assigned"] if w not in built]
        current_wi = (
            remaining[0]
            if remaining
            else (worker.get("rework_wi") or worker["assigned"][-1])
        )
        # §7 continuation re-check (WI-183): before the lane takes the next
        # constituent of a MULTI-WI traincar, the classifier must still
        # permit the grouping — a POSITIVE conflict (spine/gate/
        # attestation/protected/high-risk/critique/checkpoint) ends the
        # train EARLY instead of building inside a shared review scope.
        # Missing classification is NOT a newly-visible conflict: the
        # dispatcher already fails closed at packing, and an explicit
        # assignment is dispatcher-authorized. Built evidence stands; the
        # dispatcher releases the unstarted reservations (SR-062).
        # WI-204 (SR-095): a spine-serial constituent inside a
        # HOMOGENEOUS spine-only train is the dispatcher-authorized batch —
        # spine packs with spine, never with anything else — so it is not a
        # newly-visible conflict; only a heterogeneous grouping refuses.
        if remaining and len(worker["assigned"]) > 1:
            sched_wi = worker["sched"].get(current_wi)
            sched_class, reasons = (
                schedule.classify(sched_wi)
                if sched_wi is not None
                else (schedule.SCHED_UNCLASSIFIED, ["unclassified:missing-row"])
            )
            if sched_class == schedule.SCHED_SPINE_SERIAL and all(
                worker["sched"].get(w) is not None
                and schedule.classify(worker["sched"][w])[0]
                == schedule.SCHED_SPINE_SERIAL
                for w in worker["assigned"]
            ):
                # A member with NO sched row keeps the refusal (fail closed).
                sched_class = None  # spine-only batch: authorized, no refusal
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
    session = "{:03d}".format(next_session_number(iter_dir, worker["train"]))
    stamp = time.strftime("%Y%m%d-%H%M%S")
    # The WI this session claims (WI-137) — recorded as a `# wi:` header line
    # + an index column: the assignment's current WI.
    wi_label = current_wi
    before = head_sha(root)
    now = time.time()
    plan = route_session(ctx, i, current_wi, session, resume_reconcile, now)
    if isinstance(plan, int):
        return plan
    phase = plan["phase"]
    model = plan["model"]
    tmpl = plan["tmpl"]
    prompt = plan["prompt"]
    guarded = plan["guarded"]
    session_env = plan["session_env"]
    print(
        "=== session {} [{}] ({}/{}) | phase={} model={} wi={} ===".format(
            session,
            worker["train"],
            i,
            args.max_iterations,
            phase or "—",
            model or "—",
            current_wi,
        )
    )
    argv, stdin_input = build_argv(tmpl, model, prompt)
    # The coordinator's own clock, so a duration exists even when the
    # session dies before emitting JSON (spawn failure, timeout, crash).
    wall_start = time.time()
    live = LiveStatus(worker["train"]) if use_live else None
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
        stdin_input=stdin_input,
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
    if usage.get("input_tokens") is not None or usage.get("output_tokens") is not None:
        tokens = "{}+{}".format(
            usage.get("input_tokens", 0), usage.get("output_tokens", 0)
        )
    cost = data.get("total_cost_usd", "")
    # Where the wall time went: API round-trips vs local tool execution
    # (the gap is the harness running gates/tools). Blank when the CLI
    # reported no JSON result — the wall clock above still stands.
    api_ms = data.get("duration_api_ms")
    api_secs = int(round(api_ms / 1000.0)) if isinstance(api_ms, (int, float)) else ""
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
    # A worker has no lane run-state (spec §10): its state is always RUNNING
    # until its committed evidence says otherwise (worker_endstate).
    ctx.state = "RUNNING"

    # (outcome, errored) via the session-outcome ladder — full semantics
    # (including the "failed before it could work" error rule) live in
    # classify_outcome's docstring (single-source, WI-080 Slice D).
    outcome, errored = classify_outcome(
        reset_hint, timed_out, ctx.state, before != after, data, code
    )

    meta = {
        "session": session,
        "stamp": stamp,
        "date": time.strftime("%Y-%m-%d %H:%M"),
        "train": worker["train"],
        "base": worker["base"][:12],
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
    # Commit the coordinator's own bookkeeping now, in its own telemetry
    # commit — never let it ride the next session's work commit or dangle
    # (WI-137). The review scoreboard is committed at its own write below.
    commit_telemetry(
        root,
        tag + session,
        "{} {}".format(phase or "—", outcome),
        [log_path],
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
    r = session_bookkeeping(
        ctx, plan, outcome, code, commits, after, reset_hint, now, session, wi_label
    )
    if r == "reroute":
        return None
    if r is not None:
        return r
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
            return None
        if args.wait_on_limit and wait and wait <= args.wait_on_limit:
            print(
                "rate limit hit — sleeping {}s until the reset ({}).".format(
                    wait, reset_hint
                )
            )
            time.sleep(wait)
            return None
        stop_banner(
            status_path,
            "WAITING on a rate limit",
            "resume at: {} (re-run agent-resume.* then)".format(reset_hint),
        )
        return EXIT_WAITING
    # (The run-state DONE/BLOCKED/NEEDS-HUMAN ladder retired with the serial
    # driver, WI-210: a worker's state is always RUNNING here — its end
    # states are judged from committed evidence, below, and the dispatcher
    # generates the root run-state.)

    # Worker end-state after the session too — a completed assignment must
    # exit DONE here, not spend the remaining budget re-checking at the top.
    end = worker_endstate(
        root,
        worker,
        bool(st.review_queue or st.critique_queue),
        managed,
        rp_int,
    )
    if end:
        return worker_exit_banner(worker, end)
    st.note_session(before != after, outcome == "ERROR")
    verdict = st.stall_verdict(args.stall_limit)
    if verdict == "agent-error":
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
            "tier.".format(st.errors, iter_dir),
        )
        return EXIT_STALL
    if verdict == "stall":
        stop_banner(
            status_path,
            "STALL",
            "{} consecutive session(s) without a commit — aborting to "
            "protect the budget. See the latest {} "
            "log.".format(st.stall, iter_dir),
        )
        return EXIT_STALL
    if i < args.max_iterations and args.pause:
        time.sleep(args.pause)
    return None


def main():
    _utf8_console()
    args = parse_args()

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

    # One engine, one selection path (WI-210, spec §1.2): a plain launch IS
    # the dispatcher — absent --jobs/AGENT_JOBS resolves to the §6 default of
    # two workers (held at 1 until the §14 migration audits pass, SR-065), and
    # --jobs 1 is the explicit serial-dispatcher escape. A worker assignment,
    # interactive sitting, or --dual-plan round always wins — those are
    # explicit per-process roles the dispatcher itself launches or replaces.
    jobs_opt = (
        args.jobs
        if args.jobs is not None
        else (os.environ.get("AGENT_JOBS", "").strip() or None)
    )
    if not (args.wi or args.train or args.interactive or args.dual_plan):
        args.jobs = jobs_opt if jobs_opt is not None else "2"
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
    # Parse the enable-list WITH its optional per-phase draw-weight annotations
    # (WI-236); a malformed annotation is a preflight failure naming the line
    # (the file is the consent surface — never silently ignored).
    enabled_entries, annot_errors = agent_route.load_enabled_entries(
        docs / "agents-enabled"
    )
    raw_enabled = [token for token, _weights in enabled_entries]
    # The enable-list's PRESENCE (not its resolvability) turns managed routing on
    # — an unresolvable token must fail preflight, not silently fall to legacy.
    managed = bool(raw_enabled)
    # Version-less tokens resolve to concrete pair-row ids (exact-id, else newest
    # in the Family-Model line); unresolvable tokens become preflight failures.
    tag_rank = agent_route.load_tag_rank(docs / "agents.csv")
    enabled, resolve_errors = agent_route.resolve_enabled(
        raw_enabled, registry, tag_rank
    )
    # id -> {phase: weight}, resolved from the annotations (empty when uniform);
    # a conflicting redeclaration of an id is itself a preflight failure.
    weight_map, weight_errors = agent_route.resolved_weights(
        enabled_entries, registry, tag_rank
    )
    # Malformed annotations + unresolvable tokens + weight conflicts all surface
    # as preflight failures under the agents-enabled heading (the consent surface).
    enable_errors = annot_errors + resolve_errors + weight_errors

    failures, prompt_templates = map_preflight(
        root,
        template,
        args,
        cmd_map,
        prompt_map,
        tier_map,
        prefer_map,
        managed,
        registry,
        enabled,
        reg_errors,
        enable_errors,
    )
    if failures:
        print("agent_loop: preflight failed —", file=sys.stderr)
        for f in failures:
            print("  - " + f, file=sys.stderr)
        return EXIT_PREFLIGHT

    # The one coordination surface is docs/ (WI-210: the --track lane
    # redirection is retired; the repo-singular policy files live here too).
    worker, err = build_worker_assignment(args, root)
    if err is not None:
        return err
    lane = docs
    lane.mkdir(parents=True, exist_ok=True)
    status_path = lane / "status.md"

    gate_policy = read_declared(docs / "gate-policy", "attended")
    push_policy = read_declared(docs / "push-policy", "human")
    review_policy = read_declared(docs / "review-policy", "1")
    _, branch = git(root, "branch", "--show-current")

    guardrails_policy = read_declared(docs / "guardrails-policy", "off")
    # Surface a stale/typo'd policy token before the run: if it names a substring
    # that matches none of the models this run could use, the guard is inert.
    possible_models = {m for m in [args.model, *model_map.values()] if m}
    if managed:
        # Under managed routing sessions run the ENABLED registry rows' models,
        # not the env maps — compute the inert check against what will actually
        # run, or the warning is spurious/silent in exactly the managed mode it
        # matters for (repo-review 2026-07-21 L-20).
        possible_models |= {
            (registry[mid].model or mid) for mid in enabled if mid in registry
        }
    if guardrails_inert(guardrails_policy, possible_models):
        print(
            "agent_loop: WARNING - guardrails-policy {!r} would guard none of "
            "the configured models ({}); the guard is inert — fix the token or "
            'the model map (process-options.md "Tier-conditional guardrails").'.format(
                guardrails_policy, ", ".join(sorted(possible_models)) or "none"
            ),
            file=sys.stderr,
        )
    # A malformed declared policy must not silently disable itself — blackout
    # and review-policy are consent surfaces like agents-enabled (repo-review
    # 2026-07-21 M-20). Behavior is unchanged for compat (blackout off /
    # review-policy lenient-parse); the SILENCE was the defect.
    blackout_line = read_declared(docs / "blackout", "")
    if blackout_line and parse_blackout(blackout_line) is None:
        print(
            "agent_loop: WARNING - docs/blackout {!r} is malformed (expected "
            "HH:MM-HH:MM); the blackout window is DISABLED this run.".format(
                blackout_line
            ),
            file=sys.stderr,
        )
    if (review_policy or "").strip() not in ("0", "1", "2"):
        print(
            "agent_loop: WARNING - docs/review-policy {!r} is not 0|1|2; "
            "parsed leniently (unparseable -> 1, out-of-range clamped).".format(
                review_policy
            ),
            file=sys.stderr,
        )
    warned_no_core = []

    # WI-076: snapshot the working tree BEFORE the coordinator creates its own
    # out/agent-loop.lock (and, later, docs/iteration/*.log) — so the check sees
    # genuine interrupted-session residue, never our own artifacts. In a scaffold
    # out/ is gitignored, so the lock would not show anyway; taking the snapshot
    # first is correct regardless of a repo's .gitignore hygiene. Owner-only paths
    # (OWNER_ONLY_PATHS) are dropped so the perpetually-edited scratchpad never
    # reads as residue and fires the reconcile note on every resume (WI-203).
    start_dirty = substantive_working_tree_dirty(root)

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
        return run_interactive(
            args,
            root,
            model_map,
            cmd_map,
            template,
            guardrails_policy,
            warned_no_core,
        )

    if args.dual_plan:
        # The dual-plan round is its own early path (WI-199): one round, then
        # exit — never the resume loop. The trigger lives in the REGISTRY
        # (PlanMode=dual), the flag only names the WI; a non-dual row is
        # refused so the flag can't conscript an ordinary WI into the round.
        import plan_round as _plan_round

        wid = args.dual_plan.strip()
        rows = load_wi_registry(root)
        row = rows.get(wid)
        if row is None:
            print(
                "agent_loop: --dual-plan {}: no such WI in the registry".format(wid),
                file=sys.stderr,
            )
            return EXIT_PREFLIGHT
        if wi_plan_mode(row) != PLAN_MODE_DUAL:
            print(
                "agent_loop: --dual-plan {}: its registry row does not declare "
                "PlanMode=dual (the trigger is declared at filing, never by "
                "flag)".format(wid),
                file=sys.stderr,
            )
            return EXIT_PREFLIGHT
        outcome, detail = run_dual_plan_round(
            root,
            wid,
            row,
            template,
            args.model,
            args.session_timeout or None,
            prompt_map,
        )
        if outcome == "SELECTED":
            print("agent_loop: dual-plan {}: {}".format(wid, detail))
            return EXIT_DONE
        action = _plan_round.page_action(gate_policy)
        print(
            "agent_loop: dual-plan {} PAGED: {} (gate-policy {} -> {})".format(
                wid, detail, gate_policy or "attended", action
            ),
            file=sys.stderr,
        )
        if action == "stop-needs-human":
            _write_runstate(docs, "NEEDS-HUMAN", "dual-plan round: " + detail)
            stop_banner(docs / "status.md", "NEEDS-HUMAN", detail)
        return EXIT_NEEDS_HUMAN

    print_run_banner(
        root,
        branch,
        worker,
        gate_policy,
        push_policy,
        review_policy,
        managed,
        enabled,
        registry,
        guardrails_policy,
        template,
        cmd_map,
        prompt_map,
        docs,
    )

    raw_dir = root / "out" / "run-logs"
    iter_dir = lane / "iteration"
    tag = "{}-".format(worker["train"])
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
    # A worker has no lane run-state (spec §10) — its state is always RUNNING
    # until its committed evidence says otherwise (worker_endstate below).
    state = "RUNNING"

    # --- managed-routing / critique / stall state (S8 + WI-068 + the stall
    # guard) — one RoutingState now holds what were ~24 mutable locals here
    # (WI-080 Slice C). All no-ops when the enable-list is absent, so the legacy
    # path is byte-for-byte unchanged. The parse/env blocks that feed the
    # constructor stay exactly as before. ----------------------------------------
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
    reviews_dir = docs / "reviews" / worker["train"]
    scoreboard = reviews_dir / "scoreboard.txt"
    critique_srs = load_critique_srs(docs) if managed else set()
    try:
        critique_max = int(os.environ.get("AGENT_CRITIQUE_MAX", "3"))
    except ValueError:
        critique_max = 3
    if critique_max < 1:  # a budget is >= 1; a bad value falls back (S8-knob idiom)
        critique_max = 3
    st = RoutingState(
        rp_int, cooldown_seconds, critique_srs, critique_max, route_constants
    )
    if managed and st.critique_srs:
        print(
            "critique: {} Critique-verified SR(s) present -> a build touching one "
            "schedules a rubric-anchored CRITIQUE round (budget {} per scope)".format(
                len(st.critique_srs), st.critique_max
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

    ctx = LoopContext()
    ctx.args = args
    ctx.root = root
    ctx.docs = docs
    ctx.lane = lane
    ctx.status_path = status_path
    ctx.worker = worker
    ctx.managed = managed
    ctx.registry = registry
    ctx.enabled = enabled
    ctx.template = template
    ctx.model_map = model_map
    ctx.cmd_map = cmd_map
    ctx.prompt_templates = prompt_templates
    ctx.tier_map = tier_map
    ctx.prefer_map = prefer_map
    ctx.weight_map = weight_map
    ctx.gate_policy = gate_policy
    ctx.guardrails_policy = guardrails_policy
    ctx.warned_no_core = warned_no_core
    ctx.start_dirty = start_dirty
    ctx.raw_dir = raw_dir
    ctx.iter_dir = iter_dir
    # The weighted-rotation DRAW reads the durable CROSS-train aggregate (the
    # primary worktree's committed docs/iteration) unioned with this worker's
    # local in-flight logs — NOT the train-local iter_dir alone, whose freshly
    # minted history would reset every train's draw to slot 0 (WI-263, M-31).
    # The primary-worktree path is stable for the run, so resolve it once here;
    # the dirs are re-globbed per draw as sibling trains integrate.
    ctx.draw_iter_dirs = draw_iter_dirs(root, iter_dir)
    ctx.tag = tag
    ctx.use_live = use_live
    ctx.reviews_dir = reviews_dir
    ctx.scoreboard = scoreboard
    ctx.rp_int = rp_int
    ctx.st = st
    ctx.state = state

    for i in range(1, args.max_iterations + 1):
        code = run_iteration(ctx, i)
        if code is not None:
            return code

    stop_banner(
        status_path,
        "iteration budget exhausted",
        "{} session(s) run and {} is still {} — raise "
        "--max-iterations deliberately if the run should continue.".format(
            args.max_iterations, lane / "run-state", ctx.state
        ),
    )
    return EXIT_BUDGET


if __name__ == "__main__":
    sys.exit(main())
