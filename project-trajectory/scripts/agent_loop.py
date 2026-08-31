#!/usr/bin/env python3
"""Headless session engine: one claimed worker assignment, a reviewer/critique
round, a dual-plan round, or an interactive sitting.

Implements the session half of the walk-away protocol (process-options.md
"Unattended operation (walk-away runs)"). Claiming and merging live in the
sibling integrate.py (the serial integration seam, concurrency-restructure
§1.2/§2.3); the parallel dispatcher this module once fronted retired at Phase 5
of that restructure. A plain invocation (no role flag) runs the serial DRIVE
mode (WI-374, the sibling dispatch.py): claim the next ready WI in build order,
run a worker session on the claimed branch, drain the merge queue, repeat —
the walk-away front end the dispatcher's deletion had removed. The explicit
roles below are unchanged. Ported from a field-proven PowerShell coordinator
(NotHomeWrecker trigger.ps1), which this cross-platform implementation
supersedes. Stdlib only, Python 3.11+.

The agent invocation is a command template — the AGENT_CMD slot in the root
agent-resume.{cmd,sh} launchers (or --agent-cmd / the AGENT_CMD env var).
`{model}` and `{prompt}` placeholders are substituted per session; a template
without `{prompt}` delivers the prompt on the child's STDIN instead (WI-216 —
immune to the OS command-line caps; see build_argv/run_session).
Empty template -> guidance and exit 2 (the launchers ship inert, like run.*).

CONSENT: an unattended run typically wires the agent CLI's permission-bypass
flag into AGENT_CMD — sessions then run with no permission prompts. The human
consents by filling the slot, declaring how far a human approves
(docs/process.toml [attestation]), and running this; git + CI remain the
enforcement floor. The banner restates this every run.

During worker/review sessions this module:
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
  - honors the tracked docs/work/pause (concurrency-restructure §5.6): pause =
    stop claiming/starting, at the next session boundary — the in-flight
    session finishes and commits normally, never a mid-session kill; unpausing
    is a reviewed deletion commit;
  - honors docs/blackout: a declared `HH:MM-HH:MM` UTC WEEKDAY-ONLY window
    (Mon–Fri; weekends are never blacked out, by blackout_wake's contract)
    inside which no new session starts — the in-flight one wraps normally, then
    the agent-resume -> agent_loop path waits the window out and resumes
    automatically (a single launch survives the blackout), printing a banner and
    a periodic countdown so the wait reads as deliberate, not hung. Absent/empty/
    malformed or start==end = disabled, which is what the scaffold ships
    (WI-433: an adopter picks their own hours rather than inheriting the kit
    author's);
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

--wi runs one WORKER ASSIGNMENT (WI-181, LLR-061) on a CLAIMED branch (the
§2.3 model: `integrate.py claim` moves the spec queued/ -> active/<branch>/ on
the trunk and cuts the branch; the ordered `--wi "WI-###[;WI-###…]"` list is
built in the worktree named by --worktree, default --root, from the
integration base --base, default HEAD at start). --train survives as the
optional session TAG scoping logs and review evidence — default: the current
branch name. A worker has NO lane files: it never reads or writes
status.md/next-wi and never regenerates generated root artifacts (the trunk
lane owns them, §5.2) — its prompt is assembled from AGENTS.md, the WI row,
its SpecRef, predecessor context, the current branch diff, and any --rework
finding, and its RESULT is committed evidence: each WI's final commit carries
a `WI:` trailer (a blocker commits `Blocked-WI:` + `BlockRef:` instead and
the worker exits 3). Session logs are collision-safe
(docs/iteration/<tag>-NNN-*.log) and managed review verdicts land under
docs/reviews/<tag>/ naming the exact reviewed commit, so parallel branches
never collide. An assignment is ONE review scope (WI-183, LLR-140): under
managed routing + review-policy >= 1 the round is scheduled once, after the
LAST assigned WI commits, over the combined base..HEAD diff. A multi-WI list is
no longer something the loop packs for itself: session grouping was REMOVED
rather than wired (WI-383, docs/concurrency-v2.md §A6.1 — two lanes beat two
WIs in one session at the same throughput, with better attribution), leaving
one caller, the dispatcher admitting the spine batch, where N WIs genuinely
must share one window and one owner sitting. Exit 0 = every assigned WI built
(and its one review cycle approved).

A per-worktree lockfile (out/agent-loop.lock) stops two coordinators grinding
one checkout — a worker and an --interactive sitting both take it (one
coordinator per checkout; the OS releases it on process death).

Exit codes: 0 DONE · 2 preflight/config failure (incl. the inert unfilled
slot) · 3 BLOCKED · 4 stall abort (work stall or an all-ERROR agent-unavailable
run — the banner distinguishes them) · 5 WAITING on a rate limit · 6 iteration
budget exhausted while still RUNNING · 7 NEEDS-HUMAN (act, then re-run) · 8
paused (the tracked docs/work/pause present — unpause and re-run to resume).

Preflight refuses to start iteration 1 when: the AGENT_CMD executable is
missing (report, never a hang); the working directory is not a git repo; or
docs/privacy-check is enabled and the effective git author email is not in the
exempt allowlist — an unattended run under a private identity is the
history-leak disaster case (process-options.md "Commit identity & privacy").

Contracts: IF-015 — the interface seam this module declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-015: the unattended coordinator's effect on the repository it runs
    in. A plain launch drives the claim / work / merge cycle by COMMITTING to
    its own checkout and never pushing while the declared push policy is
    `human`, which is what ships — advancing the remote stays a human act. A
    per-checkout kernel advisory lock refuses a second coordinator in the same
    worktree rather than letting two of them interleave commits. The stop is
    always named by an exit code: 0 DONE, 2 preflight or config failure, 3
    BLOCKED, 4 stall abort, 5 WAITING on a rate limit, 6 iteration budget
    exhausted while still running, 7 NEEDS-HUMAN, 8 paused on the tracked pause
    file. Preflight refuses to start iteration 1 — rather than hanging or
    committing under a wrong identity — when the agent executable is missing,
    the working directory is not a git repository, or a privacy-checked repo's
    effective author email is not in the exempt allowlist.
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
from dataclasses import dataclass, field
from pathlib import Path

# Sibling: the spine's registry CARRIER — one home for the
# TOML tier tables, the key->column vocabulary and both readers.
try:
    import spine_carrier
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier

# Sibling scripts (the S8 routing/scoring half + the WI-218 split-out layers).
# Run as a subprocess the loop's own dir is sys.path[0] so a plain import
# resolves; the guard covers an in-process import (a test) whose sys.path
# doesn't yet carry scripts/ — the same sanctioned-sibling-import idiom
# gen_trajectory uses.
try:
    import adjudicate_brief
    import adjudicator_session
    import agent_common
    import agent_route
    import agent_session
    import plan_runner
    import prompts
    import score_reviews
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import adjudicate_brief
    import adjudicator_session
    import agent_common
    import agent_route
    import agent_session
    import plan_runner
    import prompts
    import score_reviews

# The WI-218 split: the session-launch layer (slice B), the shared coordinator
# primitives + the dual-plan runner (slice C), and (until Phase 5) the parallel dispatcher/
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
EXIT_REVIEW_OWED = agent_common.EXIT_REVIEW_OWED
END_STATES = agent_common.END_STATES
OWNER_ONLY_PATHS = agent_common.OWNER_ONLY_PATHS
read_declared = agent_common.read_declared
declared_policy = agent_common.declared_policy
process_config = agent_common.process_config
config_conflicts = agent_common.config_conflicts
read_agent_loop_config = agent_common.read_agent_loop_config
resolve_coordinator_dials = agent_common.resolve_coordinator_dials
pause_reason = agent_common.pause_reason
parse_blackout = agent_common.parse_blackout
blackout_wake = agent_common.blackout_wake
blackout_wait = agent_common.blackout_wait
WI_TOKEN_RE = agent_common.WI_TOKEN_RE
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

PLAN_MODE_DUAL = plan_runner.PLAN_MODE_DUAL
wi_plan_mode = plan_runner.wi_plan_mode
run_dual_plan_round = plan_runner.run_dual_plan_round
_dp_routes = plan_runner._dp_routes
_dp_session = plan_runner._dp_session


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


# The three session-engine prompts are FILES now, not string constants
# (plan §8): `project-trajectory/prompts/{worker,reviewer,critique}.template.md`,
# loaded through `prompts.py`. Prompt prose is what steers the sessions this
# loop launches, and it had been reviewable only by reading Python source — so
# it moved to where a diff shows it, under the same machinery the dual-plan
# hats already used.
#
# LOADED LAZILY, never at import: a missing template must be a named PREFLIGHT
# refusal (`map_preflight`), not an ImportError for every consumer of this
# module — dispatch, plan_runner and most of the suite import agent_loop
# without composing a single prompt. The fill idioms are UNCHANGED
# (`WORKER_PROMPT.format(...)`, `.replace("{verdict}", ...)`), because the
# single-brace vocabulary is also every operator override file's contract.


def _kit_prompt(key):
    """One shipped prompt's text, cached per key for the process lifetime.

    Read once and held because `worker_prompt` runs at EVERY claim and the
    reviewer/critique briefs at every review round; the file is kit-owned and
    does not change mid-run. A refusal propagates as `prompts.PromptError`,
    which `route_session`'s callers surface by name."""
    cached = _PROMPT_CACHE.get(key)
    if cached is None:
        cached = _PROMPT_CACHE[key] = prompts.load(key)
    return cached


_PROMPT_CACHE = {}

# The review-phase names the loop schedules (the in-process phase in {PLAN,
# BUILD, REVIEW-A, REVIEW-B, INTEGRATE}). A committing non-review session
# triggers a review round; these phases are the round.
REVIEW_PHASES = ("REVIEW-A", "REVIEW-B")

# Default phase -> tier when routing from docs/agents.toml (AGENT_TIER_MAP /
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
    # SN-026: an adjudicator rules on a CLAIM — was this delivered, did this
    # amendment move meaning, is this queued row a duplicate — and every one of
    # those is a judgement whose cost of being wrong is a wrong approval.
    # Strong by default, like the other two judging phases. The per-row
    # `BuildTier` still pins it down where a disposition estimated cheaper
    # (`intake.tier_signal`), because that estimate is measured; this is the
    # floor for a row that names nothing.
    "ADJUDICATE": "strong",
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
    # SN-026: an adjudication commit changes Status cells and the work
    # registry, which is what its lane runs no product bar for
    # (`integrate.refresh`'s no-bar arm). A review round over it would be a
    # fresh-context reviewer asked to judge a judgement, with no product diff
    # to judge — the corroboration loop the review rounds exist to avoid.
    "ADJUDICATE",
}


# (read_ask retired with the serial driver, WI-210: the engine composes
# its NEEDS-HUMAN banners from the ask it just generated — the `ask:` line in
# docs/run-state remains the WI-127 contract for humans and launchers.)


# (--track and its docs/tracks/<name>/ lane plumbing retired outright, WI-210:
# the explicit --wi worker assignment is the only lane
# concept; docs/ is the one coordination surface and the integrator owns it.)


def worker_prompt(root, wi_rows, wi, train, base, rework_text=""):
    """The per-session worker prompt (LLR-061): the WI row + SpecRef +
    predecessor context + the current branch diff + any rework finding, slotted
    into WORKER_PROMPT (`train` is the session tag = the claim branch name).
    Reads NOTHING from docs/status.md or docs/next-wi — the explicit
    assignment is the whole scope.

    Implements: SR-026, LLR-061
    """
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
        "branch):\n" + "\n".join(preds) + "\n"
        if preds
        else ""
    )

    # The WI-388 context block (consumer 2): computed FRESH at claim for every
    # WI — pure registry joins (cancelled precedent with reasons, pending OIs,
    # the LLR/TC code map, knowledge packs, IF seams, precedent reviews),
    # advisory-never-gating, clipped like the blocks around it. The lazy
    # import keeps this module launchable even where a stripped-down copy
    # ships without the intake sibling.
    try:
        import intake

        # rows=None: the block re-reads the registry from disk, so the joins
        # are as-of the CLAIM, not as-of whenever wi_rows was loaded.
        joins = intake.context_block(root, row)
    except Exception:  # advisory: a missing/broken join is no join
        joins = ""
    context_block = (
        "- Context (advisory registry joins; read the Context refs below "
        "before starting):\n" + "\n".join("  " + ln for ln in joins.splitlines()) + "\n"
        if joins
        else ""
    )

    _c1, log_out = git(
        root, "log", "--oneline", "--no-decorate", "{}..HEAD".format(base)
    )
    _c2, stat_out = git(root, "diff", "--name-status", "{}..HEAD".format(base))
    diff_block = (
        "- Current branch diff ({}..HEAD — earlier work on this branch, accepted "
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

    return _kit_prompt(prompts.WORKER).format(
        wi=wi,
        title=(row.get("Title") or "(row missing from the registry)").strip(),
        srs=(row.get("SR-Refs") or "—").strip() or "—",
        specref=(row.get("SpecRef") or "—").strip() or "—",
        train=train,
        base=base,
        pred_block=pred_block,
        context_block=context_block,
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


def prompt_source(prompt_templates, phase):
    """Which template a phase's session composed from: an operator override's
    declared phase key, else `kit:<PHASE>` for the shipped file.

    Names the SOURCE, not the text — the text's fingerprint is the row's
    `prompt-sha`. Kept deliberately coarse: an override map is keyed by phase,
    so that is the finest distinction this can honestly report."""
    if phase and phase in (prompt_templates or {}):
        return "override:" + phase
    return "kit:" + (phase or "BUILD")


def row_routing(phase, row):
    """`(phase, pinned_tier)` for a claimed WI row — the two routing facts a
    row's own declaration carries.

    THE PHASE RE-KEY COMES FIRST, and must, because it changes what the tier
    default and the heterogeneity rule are: an `adjudication` row is not a
    build (SN-026), and routing it as one drew from the implementer pool at the
    implementer tier — i.e. the judge could be the same family as the party
    whose claim it is judging. THE TIER PIN is WI-181's per-row `BuildTier`,
    normalized and validated against the tier vocabulary; an escalation
    override still wins over it for a BUILD (`route_intent`).

    Only a BUILD-ish phase is re-keyed: a queued review or critique round is
    the round's, not the row's, and must not be renamed by whatever WI happens
    to be claimed."""
    if phase not in ("BUILD", "") or not row:
        return phase, None
    if adjudicating(row):
        phase = "ADJUDICATE"
    tier = agent_route.normalize_tier((row.get("BuildTier") or "").strip().lower())
    return phase, (tier if tier in agent_route.TIER_ORDER else None)


def adjudicating(row):
    """Whether a claimed WI row is an ADJUDICATION row (SN-026).

    Read off the declared `SafetyClass`, which is the same cell
    `schedule.classify` reads to make the row exclusive and rank it — one
    declaration, two consumers, no second vocabulary. A pure function so the
    routing consequence is drivable without a session."""
    return (row.get("SafetyClass") or "").strip().lower() == "adjudication"


def phase_tier(phase, tier_map):
    """The routing tier for a phase: the declared --tier-map / AGENT_TIER_MAP
    value, else DEFAULT_PHASE_TIER, else `strong` (route an unknown phase UP —
    cheap is not free). Declared values are normalized — legacy `weak` reads as
    `quick` (the tier-rename alias, agent_route.normalize_tier)."""
    if phase in (tier_map or {}):
        return agent_route.normalize_tier(tier_map[phase])
    return DEFAULT_PHASE_TIER.get(phase, "strong")


def reviewer_prompt(prompt_templates, phase, verdict_path, root=None, worker=None):
    """The redacted reviewer prompt for a review phase: the per-phase prompt-map
    template (a FILE the operator wired) if present, else the embedded
    REVIEWER_PROMPT — with {verdict} resolved to the path the reviewer must
    write. Never carries the implementer's self-assessment (redaction by
    construction).

    C7 (docs/plans/2026-08-30-stall-guard-plan.md): the brief's reading scope
    renders per repo — `{trunk}` (the primary checkout's branch, the
    integration trunk), `{process_doc}` (docs/process.md where bootstrap
    materialized one; this meta-repo's masters live under project-trajectory/,
    so a literal would be right downstream and wrong here) and `{scripts}`
    (the kit scripts' directory, the same hazard) are SLOTS. An
    operator override file may carry the same slots; one without them renders
    unchanged, and a caller without a root (a bare template read) leaves them
    unrendered rather than guessing.

    Implements: SR-154, LLR-045
    """
    base = prompt_templates.get(phase, _kit_prompt(prompts.REVIEWER))
    text = base.replace("{verdict}", str(verdict_path))
    if root is not None:
        text = text.replace("{process_doc}", process_doc_path(root))
        text = text.replace("{trunk}", trunk_name(root, worker))
        text = text.replace("{scripts}", scripts_dir(root))
    return text


def process_doc_path(root):
    """The path the review brief names for the process doc: `docs/process.md`
    where the scaffold materialized one (every adopter — bootstrap.MAPPING),
    else the kit master `project-trajectory/PROCESS.md` (this meta-repo's
    self-application boundary scaffolds no copy — every reviewer of the
    2026-08-30 run errored on the literal)."""
    return (
        "docs/process.md"
        if (Path(root) / "docs" / "process.md").is_file()
        else "project-trajectory/PROCESS.md"
    )


def scripts_dir(root):
    """The directory the review brief names for the kit scripts: `scripts`
    where the scaffold materialized them (every adopter), else the kit's own
    `project-trajectory/scripts` (this meta-repo — round 2 found every
    reviewer here failing the harness read on the scaffold path)."""
    return (
        "scripts"
        if (Path(root) / "scripts" / "check.py").is_file()
        else "project-trajectory/scripts"
    )


def trunk_name(root, worker=None):
    """The integration trunk's NAME for the review brief: the branch the
    PRIMARY checkout is on (`git worktree list --porcelain`, first block — a
    lane runs in a linked worktree while the primary holds trunk). Falls back
    to the current branch (a repo with no linked worktrees), then to the
    worker's base sha — the slot never renders empty."""
    code, out = git(root, "worktree", "list", "--porcelain")
    if code == 0 and out.strip():
        for line in out.split("\n\n", 1)[0].splitlines():
            if line.startswith("branch refs/heads/"):
                return line[len("branch refs/heads/") :].strip()
    _c, cur = git(root, "branch", "--show-current")
    if cur.strip():
        return cur.strip()
    return (worker or {}).get("base", "") or "HEAD"


def session_body(root, worker, current_wi, session, sha, reviews_dir, templates):
    """`(body, verdict_path, hold, brief)` for a NON-REVIEW session — the one
    fork both routing arms take, so the rule has a single home. `brief` names
    the adjudicator template the body came from ("" for an ordinary
    assignment), which is what arms the ADJUDICATE validation arm downstream.

    An adjudication row is a JUDGEMENT, not a build (SN-026), and gets the
    brief its `Brief` cell declares (WI-424). Routing it to a strong
    cross-family model and then handing it the implementer's assignment was
    the whole defect: the judge was briefed as a builder, and all four
    authored adjudicator briefs were consumed by nothing.

    EVERYTHING ELSE — and any adjudication row whose evidence could not be
    assembled IN FULL — builds from the worker assignment: never a
    resume-from-status default (retired, WI-210) and never a repo prompt-map
    template (the assignment is the whole scope).

    A DECLARED BRIEF THAT CANNOT BE COMPOSED IS A HOLD, NOT A FALLBACK, and
    that is the third value: `(None, None, reason)`. Sending the ordinary
    assignment instead would put the judge back in the builder's chair on a
    ROUTINELY MINTED path — `intake` mints `brief = "amendment"` rows today and
    no assembler can serve them — which is the exact defect this seam exists to
    close. A row that declares a brief the kit cannot produce is a gap in the
    kit, and a gap fails CLOSED.

    A row that declares NO brief keeps the ordinary assignment: that is not a
    claim the kit failed to honour, it is an adjudication class the kit has
    never authored a brief for (the clean-close spot check, a cancellation that
    owes no report), and holding those would page a human for routine work."""
    row = worker["rows"].get(current_wi) if worker and current_wi else None
    brief = adjudicate_brief.declared_brief(row) if row and adjudicating(row) else ""
    if brief:
        verdict_path = fresh_verdict_path(
            reviews_dir, "{}-ADJUDICATE-{}.md".format(session, (sha or "")[:7])
        )
        body, why = adjudicate_brief.compose(root, row, verdict_path, templates)
        if body is None:
            return None, None, why, ""
        return body, verdict_path, None, brief
    return (
        worker_prompt(
            root,
            worker["rows"],
            current_wi,
            worker["train"],
            worker["base"],
            worker["rework"],
        ),
        None,
        None,
        "",
    )


# What a held adjudication row tells the human, appended to the stop banner.
# The exit code is the DURABLE half: `dispatch._lane_close` turns
# EXIT_NEEDS_HUMAN into a `handback.close_partial` — an immutable per-close
# report plus a `blockref` that `schedule._disposition` reads as `blocked` — so
# an unattended run can never re-pick the row until a human clears it. A print
# alone would be gone with the terminal buffer.
ADJUDICATION_HOLD_NOTE = (
    "This row is an ADJUDICATION: it exists to judge a claim, and the brief it "
    "declares is the whole reason it routes to a strong cross-family model. "
    "Dispatching it with the ordinary worker assignment would brief the judge "
    "as a builder, so the loop HOLDS it instead. Either supply the missing "
    "evidence named above, or clear the row's `brief` cell if this class of "
    "judgement is not one the kit briefs."
)


def session_model(model_map, default_model):
    """The legacy/interactive route: the tracked docs/run-phase file is retired
    (WI-180), so the phase is '' and the model the ''-keyed map entry, else the
    default."""
    return "", model_map.get("", default_model)


def session_template(cmd_map, default_template, phase):
    """The per-phase command template (AGENT_CMD_MAP), else AGENT_CMD — phase
    keys are free-form, so REVIEW-A/REVIEW-B route providers without any loop
    change.

    Implements: SR-040, LLR-037
    """
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
    system-requirements.toml). Empty — absent file, or no such row — makes the whole
    critique layer vacuous, exactly like an absent enable-list makes routing off.

    Implements: SR-154, LLR-048
    """
    out = set()
    for r in spine_carrier.load(
        Path(docs) / "requirements" / "system-requirements.toml", "SR-ID"
    ):
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
    """The SR ids delivered by the WI-tagged commits in `commit_range`.

    Reads the registry through `load_wi_registry` (the spec-folder home) —
    the direct-CSV read this carried silently answered EMPTY in a
    folder-registry tree, disarming the critique scope (found while
    classifying its census pair at Phase 5, fixed with item 3).

    Implements: SR-154, LLR-048
    """
    wi_ids = build_scope_wis(root, docs, commit_range)
    srs = set()
    for wid, r in load_wi_registry(Path(docs).parent).items():
        if wid in wi_ids:
            srs.update(_refs(r.get("SR-Refs")))
    return srs


def critique_control(docs, wi_ids, default_max):
    """Resolve the optional per-WI critique control for one build scope.

    A mixed scope uses the most conservative settings: `inf` outranks every
    integer, otherwise the largest budget wins; `block` outranks `move-on`.
    Missing/invalid cells preserve the global default and move-on behavior.
    """
    budgets, disposition = [], "move-on"
    # Through the registry loader, not a raw CSV read — the same Phase 5 item 3
    # re-point as build_scope_srs above.
    for wid, r in load_wi_registry(Path(docs).parent).items():
        if wid not in wi_ids:
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
    implementer's session — redaction by construction.

    Implements: SR-154, LLR-048
    """
    docs = Path(docs)
    sr_by_id = {
        (r.get("SR-ID") or "").strip(): r
        for r in spine_carrier.load(
            docs / "requirements" / "system-requirements.toml", "SR-ID"
        )
    }
    tcs = spine_carrier.load(docs / "test" / "test-cases.toml", "TC-ID")
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
    and {brief} resolved. Never carries the implementer's self-assessment.

    Implements: SR-154, LLR-048
    """
    base = prompt_templates.get("CRITIQUE", _kit_prompt(prompts.CRITIQUE))
    return base.replace("{verdict}", str(verdict_path)).replace("{brief}", brief)


def launcher_exe(cmd_template):
    """`(exe, installed)` for a command template: argv[0], and whether that
    launcher is actually present — on PATH, or an explicit path that exists.

    Stated once (WI-345): the per-phase cmd-map preflight and the agents.toml
    registry preflight both ask "is this model's CLI really here", and a probe
    that answers differently in two places is a preflight that passes for one
    route and fails for another. Raises ValueError/IndexError from `build_argv`
    on an unparseable template — both callers already catch that and report it
    with their own registry's wording."""
    argv, _ = build_argv(cmd_template, "model", "prompt")
    exe = argv[0]
    return exe, bool(shutil.which(exe) or Path(exe).exists())


def fresh_verdict_path(reviews_dir, name):
    """The path a managed session must write its verdict to, guaranteed ABSENT.

    The name is fully predictable (next session number + the implementer's own
    HEAD sha), so an UNCOMMITTED file planted here before the session runs would
    be counted as the verdict whenever that session errors. Clearing it first is
    what makes the reviewer/critic the only writer that counts (repo-review
    2026-07-21 M-22; committed plants stay defeated by the sha-in-name design).

    Stated once (WI-345). The two arms had this in duplicate with the REASON in
    only one of them, so the critique arm's `unlink` read as a stray line — the
    precise failure mode of a copied rule: the copy loses the why."""
    path = reviews_dir / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    return path


def read_verdict(verdict_path, route_family):
    """The parsed verdict at `verdict_path`, or None when the session wrote no
    file (errored, stalled, or simply did not write one).

    Both managed arms read it identically; what they DO about an unparseable
    `VERDICT:` line differs and deliberately stays in the arms — the review arm
    cools and re-routes the phase, the critique arm cools and re-critiques. Only
    the plumbing moves (WI-345)."""
    if not verdict_path or not Path(verdict_path).exists():
        return None
    return score_reviews.parse_verdict(
        Path(verdict_path).read_text(encoding="utf-8", errors="replace"),
        model=route_family,
    )


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
        # WI-264: the win-stay directive from the last escalation — a reviewer
        # FAMILY to prefer as the next review round's primary feedback source
        # when the last round's margin cleared the bar, else None (lose-shift ->
        # the ordinary weighted draw). apply_decision refreshes it every round;
        # the review draw validates it against the live pool (fail-open).
        self.next_primary = None
        # --- critique-loop state (WI-068; vacuous when no Critique SR exists) ---
        self.critique_queue = []  # ["CRITIQUE"] when a critique round is scheduled
        self.critique_scope = set()  # the in-scope Critique SR ids for this loop
        self.critique_rounds = 0  # consecutive CHANGES-REQUESTED critique rounds
        self.critique_limit = None  # None means inf-until-APPROVE for the scope
        self.critique_exhaustion = "move-on"
        # --- stall guard (C1, docs/plans/2026-08-30-stall-guard-plan.md:
        # route-aware — the builder's streak and the reviewer draw's streak
        # are DIFFERENT failures; one counter booked a reviewer outage as the
        # builder not building and closed finished work partial, WI-521) ---
        self.stall = 0  # consecutive non-committing BUILD-side sessions
        self.errors = 0  # consecutive ERROR sessions (agent unavailable)
        self.review_draw_failures = 0  # consecutive failed REVIEW/CRITIQUE draws
        # C4: routes with an unclean history this run (cooled after an
        # ERROR/TIMEOUT/limit/garble) — the pre-dispatch probe list. A route
        # with a clean history is never probed (recovery aid, not a tax).
        self.suspect_routes = set()
        # C5: a relaxed (same-family) reviewer draw served the current round.
        self.round_relaxed = False

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
        if is_review or is_critique or phase in ("ADJUDICATE", "DESIGN-CHECK"):
            # THE JUDGING PHASES, one arm: a reviewer, a critic, an adjudicator
            # and a design-check all rule on work someone else did, and all
            # take the same heterogeneity rule for the same reason — a judge
            # that shares the family of the party it judges corroborates rather
            # than checks. What differs between them is only the tier, which
            # `phase_tier` already answered, plus the two riders below.
            prefer_different = True
            if self.last_impl_family:
                exclude.add(self.last_impl_family)
        if is_review:
            for _ph, _v, fam, _mid in self.round_verdicts:
                if fam:
                    exclude.add(fam)  # REVIEW-B differs from REVIEW-A too
        elif phase == "ADJUDICATE":
            # SN-026. Both HALVES apply, which is why this is its own arm
            # rather than a member of either neighbour's:
            #   * it JUDGES, so it takes the heterogeneity rule the reviewers
            #     and the design-check take — a judge that shares the family of
            #     the party it judges corroborates rather than checks;
            #   * its tier is PINNED by the row, because `intake.tier_signal`
            #     estimated it from measured breadth (rows touched, gate moved,
            #     targets in a red-TC contradiction) and a measured estimate
            #     beats a phase default.
            # The escalation overrides are deliberately NOT read here: they
            # describe the implementer's trouble, and an adjudication row is
            # not the implementer's work.
            if pinned_tier is not None:
                tier = pinned_tier
        elif phase == "BUILD" or phase == "":
            if pinned_tier is not None:
                tier = pinned_tier
            if self.impl_tier_override:
                tier = self.impl_tier_override
            if self.impl_exclude:
                exclude = set(self.impl_exclude)
                prefer_different = True
        return tier, exclude, prefer_different

    def note_build_tier(self, tier):
        """Record the tier a BUILD/"" session ran at (the round's implementer
        tier). Called only on the non-review BUILD/"" condition, as today."""
        self.last_impl_tier = tier

    def cool(self, route_id, now, seconds=None):
        """Put a route on cooldown (per-model backoff): the parsed rate-limit
        wait when given, else the configured default. C4: a cooled route is a
        SUSPECT — before the next real session is spent on it, it must answer
        the pre-dispatch liveness probe (select_with_probe)."""
        if route_id:
            self.suspect_routes.add(route_id)
        agent_route.cool(
            self.cooldowns,
            route_id,
            now,
            seconds if seconds is not None else self.cooldown_seconds,
        )

    def record_review_verdict(self, phase, verdict, family, model_id):
        """Append one reviewer's verdict to the round and pop the phase it
        consumed off the review queue."""
        self.review_draw_failures = 0  # C1: a recorded verdict resets the streak
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

    def apply_decision(self, action, merged, next_primary=None):
        """The STATE consequences of an escalation decision only — no I/O. The
        caller keeps the prints / failure_action / banners / run-state writes.

        `next_primary` (WI-264) is the win-stay directive from the SAME decision:
        the reviewer family to prefer next review round on a win, else None. It is
        stored raw here and validated against the live pool at draw time
        (fail-open), and refreshed every round — a win sets the family, a
        loss/page/swap/tier-up returns None and clears it (lose-shift)."""
        self.next_primary = next_primary
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
        self.round_relaxed = False  # C5: a fresh round starts cross-family
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

    def note_session(self, committed, errored, judging=False):
        """Fold one session's outcome into the stall/error counters: a commit
        resets the stall; an error before work increments the error run.

        C1 (docs/plans/2026-08-30-stall-guard-plan.md): a JUDGING session — a
        review or critique draw — never touches the builder's streak. Its
        failures are counted by `note_review_draw_failure` and bounded by the
        C2 review-owed exit, because a reviewer outage is a reviewer problem:
        booking it here closed finished, committed work `partial` (WI-521).

        Implements: SR-172, LLR-175
        """
        if judging:
            return
        self.stall = 0 if committed else self.stall + 1
        self.errors = self.errors + 1 if errored else 0

    def note_review_family(self, family):
        """C5: record whether this review draw shares the implementer's family
        — the relaxed rung, however the draw got there — and return the fact
        for the verdict filename. Derived from the typed family fact, never a
        reason-string sniff."""
        relaxed = bool(self.last_impl_family and family == self.last_impl_family)
        self.round_relaxed = self.round_relaxed or relaxed
        return relaxed

    def note_review_draw_failure(self):
        """One REVIEW/CRITIQUE draw failed (ERROR, TIMEOUT, no verdict, no
        routable candidate): count it toward the C2 review-owed bound. A
        recorded verdict resets the streak (record_review_verdict)."""
        self.review_draw_failures += 1

    def stall_verdict(self, limit):
        """None (keep going), "agent-error" (the whole stall run errored before
        working — an unavailable agent), or "stall" (a work stall).

        Implements: SR-028, LLR-028
        """
        if self.stall < limit:
            return None
        return "agent-error" if self.errors >= limit else "stall"


def limit_reset_hint(output, data, exit_code):
    """The 'resets <time>' text of a rate-limit message, or None.

    Only an *error* is eligible (the JSON result's is_error, or a nonzero
    session exit for plain-text templates) — a healthy transcript merely
    *mentioning* limits must never read as a throttle.

    Implements: SR-171, LLR-174
    """
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
    enabled) or exits WAITING with the raw hint in the banner.

    Implements: SR-171, LLR-174
    """
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

    Returns (outcome, errored).

    Implements: SR-028, LLR-028
    """
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
    if worker.get("adjudication_owed"):
        # An adjudication row's WI trailer proves a COMMIT, never a
        # RULING. Its brief names a verdict path and a closed-enum line;
        # until both exist this assignment has not delivered what it was
        # routed to a strong cross-family judge to produce.
        return None
    if substantive_working_tree_dirty(root):
        return None  # committed evidence only — a dirty tree (owner-only exempt) is not done
    return (
        EXIT_DONE,
        "DONE",
        "every assigned WI ({}) carries its trailer commit on branch {}{}".format(
            ";".join(worker["assigned"]),
            worker["train"],
            "; review round approved" if managed and rp_int >= 1 else "",
        ),
    )


def worker_exit_banner(worker, end):
    """Print the worker's end banner (never a status.md excerpt — a worker
    has no resume surface) and hand back the exit code."""
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
        help="worker assignment: the session tag scoping logs and review "
        "evidence. Default: the current branch name (the §2.3 claim branch "
        "`integrate.py claim` cut).",
    )
    ap.add_argument(
        "--worktree",
        default=None,
        help="worker assignment: the worktree to run in (becomes the "
        "effective --root; default: --root itself).",
    )
    ap.add_argument(
        "--base",
        default=None,
        help="worker assignment: the integration base commit the branch was "
        "cut from. Default: HEAD at worker start.",
    )
    ap.add_argument(
        "--rework",
        default=None,
        help="worker assignment: a findings file (review verdict) to embed in "
        "the worker prompt as the rework scope — assignment-scoped state, "
        "replacing the lane rework-wi pointer.",
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
        "--lanes",
        type=int,
        default=None,
        help=(
            "worker-lane ceiling for the plain-launch dispatcher (WI-381); "
            "resolves CLI > AGENT_LANES > docs/stack.ini [agent-loop] lanes > "
            "1 — an absent dial means serial"
        ),
    )
    ap.add_argument(
        "--model",
        default=None,
        help="default model tier for {model}; precedence CLI flag > AGENT_MODEL "
        "env > docs/stack.ini [agent-loop] model > '' (IF-068, resolved in main)",
    )
    ap.add_argument(
        "--model-map",
        default=None,
        help='per-phase tier map "P0=strong-model,DevStg-Impl=strong-model" matched '
        "against the in-process phase; precedence CLI flag > AGENT_MODEL_MAP env "
        "> docs/stack.ini [agent-loop] model-map > '' (IF-068, resolved in main)",
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
        "used by the docs/agents.toml router when the enable-list is present; "
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
        "--session-idle-timeout",
        type=int,
        default=None,
        help="kill a session this many seconds after its LAST output line "
        "(C3, the stall-guard plan; default: the AGENT_SESSION_IDLE_TIMEOUT "
        "env slot, else 900; 0 disables) — --session-timeout stays the outer "
        "wall bound",
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
        "keeps the append-only scroll); also enabled by docs/process.toml "
        "[checks] live_status = true. Overridden by --no-session-echo.",
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
    Returns `(failures, prompt_templates, prompt_paths)`: the last mapping is
    the actual file each loaded prompt came from, retained so governing-input
    hashing cannot silently omit or misidentify an adjudication override."""
    failures = preflight(root, template, args)
    # THE SHIPPED PROMPTS (plan §8). Now that the worker / reviewer / critique
    # briefs are files, a missing or unreadable one is a launchability failure
    # exactly like a broken --prompt-map entry — and it must fail HERE, before
    # iteration 1, rather than at the first session that needs that brief. This
    # is the rung that makes the constants-to-files move safe: without it, a
    # scaffold whose prompts/ dir never landed would run, claim, and only then
    # discover it has nothing to send.
    failures.extend(prompts.preflight())
    # Every per-phase template must be as launchable as the default one — a
    # broken REVIEW-B entry must fail before iteration 1, not at the first
    # review session mid-run (the preflight contract).
    for ph, tmpl in sorted(cmd_map.items()):
        try:
            exe, installed = launcher_exe(tmpl)
            if not installed:
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
    prompt_paths = {key: prompts.template_path(key) for key in prompts.KIT_PROMPTS}
    for ph, rel in sorted(prompt_map.items()):
        p = Path(rel)
        if not p.is_absolute():
            p = root / rel
        prompt_paths[ph] = p
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
            failures.append("agents.toml: {}".format(e))
        for e in enable_errors:
            failures.append("agents-enabled: {}".format(e))
        for mid in enabled:
            m = registry[mid]  # resolve_enabled guarantees the id is in the registry
            try:
                exe, installed = launcher_exe(m.cmd_template)
                if not installed:
                    # The row's Notes is the declared install/sign-in hint —
                    # surface it at the earliest failure point (WI-109).
                    failures.append(
                        "agents.toml [{}]: CmdTemplate CLI {!r} is not on "
                        "PATH.{}".format(mid, exe, " — " + m.notes if m.notes else "")
                    )
            except (ValueError, IndexError) as exc:
                failures.append(
                    "agents.toml [{}]: cannot parse CmdTemplate: {}".format(mid, exc)
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
            print("agent_loop: WARNING - agents.toml: {}".format(e), file=sys.stderr)
    return failures, prompt_templates, prompt_paths


def default_base(root):
    """The integration base a worker assumes when --base is not given: the
    merge-base of the lane's HEAD with the TRUNK (the primary checkout's
    branch), else HEAD. It used to be HEAD unconditionally — right for a
    fresh claim (HEAD IS the claim commit) and wrong for every RESUMED
    worker, whose base..HEAD evidence then read empty: the built trailers,
    the owed review round and the resume itself were invisible, which is the
    "resumed session finds nothing to do" pattern of the 2026-08-30 run
    (WI-548 round 3). A repo whose primary checkout is the branch itself
    (a single-checkout attended run, the test fixtures) merges-bases to HEAD
    and keeps the old behaviour exactly."""
    trunk = trunk_name(root)
    code, out = git(root, "merge-base", trunk, "HEAD")
    if code == 0 and out.strip():
        return out.strip()
    return head_sha(root)


def build_worker_assignment(args, root):
    """The explicit worker assignment (--wi, on a claimed branch): parse the
    WI list, fail closed on an unresolvable --base, and load the registry +
    scheduler views + any --rework findings. The session tag (`worker["train"]`,
    scoping logs and review evidence) is --train when given, else the current
    branch name — the §2.3 claim branch. Returns (None, None) when this is not
    a worker process, (worker, None) on success, or (None, EXIT_PREFLIGHT)
    after printing its own error.

    Implements: SR-026, LLR-061
    """
    # --- worker assignment mode (WI-181, LLR-061) -----------------------------
    # worker != None switches the loop from "resume from the lane" to "build
    # the explicit assignment": no lane status/next-wi reads or writes, no
    # generated-artifact regeneration, tag-scoped collision-safe logs + review
    # evidence, result = committed trailers + the exit code.
    worker = None
    if args.wi:
        tag = (args.train or "").strip()
        if not tag:
            code, out = git(root, "symbolic-ref", "--quiet", "--short", "HEAD")
            # A branch name may carry "/" (not a safe path segment for the
            # tag's reviews/<tag>/ and log-prefix roles) — flatten it.
            tag = out.strip().replace("/", "-") if code == 0 else ""
        if not tag:
            print(
                "agent_loop: no --train tag and no current branch (detached "
                "HEAD) — a worker session runs on the claimed branch "
                "(`integrate.py claim`); check one out or pass --train.",
                file=sys.stderr,
            )
            return None, EXIT_PREFLIGHT
        base = (args.base or "").strip() or default_base(root)
        if not base:
            # An unborn HEAD (zero-commit repo) has no integration base to
            # build evidence against — fail closed, never crash (a claim is
            # always cut from an existing HEAD).
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
            "train": sanitize_train(tag),
            "assigned": assigned,
            "base": base,
            "rows": rows,
            # (No scheduler view: the `sched` map existed only to feed the §7
            # continuation re-check, deleted with session grouping — WI-383.)
            "rework": "",  # in-process rework note (a CHANGES-REQUESTED verdict)
            # An ADJUDICATE session whose verdict artifact is missing or
            # untyped: assignment-scoped like `rework`, and read by
            # `worker_endstate` for the same reason — committed evidence
            # alone does not prove a JUDGEMENT was made.
            "adjudication_owed": "",
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


def _subagent_gate_log_count(root):
    """`(decisions, fail_open)` from `out/subagent-gate.log` — one decision per
    line (allow, ask, deny, or a fail-open "gate error, failing open" entry),
    and how many of those lines are the fail-open kind. `(0, 0)` if the file was
    never written, i.e. the gate never fired. `subagent_gate.py`
    writes the file but nothing read it before OI-46 ruled (2a) (2026-08-20):
    a write nobody reads is a record only in name, so `print_run_banner`
    below surfaces this count on every unattended launch (WI-491).

    The filename is a LITERAL, not `subagent_gate.LOG_NAME` — importing that
    sibling for one string would open a new CMP-008 -> CMP-007
    cross-component seam for a fact this small; `tests/test_agent_loop.py`'s
    banner tests and `tests/test_subagent_gate.py`'s own log-path assertions
    both pin the same literal, so a rename on either side breaks a test
    before it breaks silently."""
    path = Path(root) / "out" / "subagent-gate.log"
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            lines = handle.readlines()
    except OSError:
        return 0, 0
    # FAIL-OPEN LINES COUNTED SEPARATELY (2026-08-21 review, m-32). OI-46 (2a)
    # asked for the fail-open allows to be VISIBLE, and a single total cannot
    # do that: a log of 500 routine allows plus one fail-open reads exactly
    # like 501 routine allows. The reason string `subagent_gate.log_decision`
    # writes for that arm is the discriminator — "gate error, failing open".
    return len(lines), sum(1 for ln in lines if "failing open" in ln)


def print_run_banner(
    root,
    branch,
    worker,
    session_hold,
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
    print("=== session engine (scripts/agent_loop.py) ===")
    print("repo: {} | branch: {}".format(root, branch or "(none)"))
    if worker:
        print(
            "worker assignment: branch={} wi={} base={} (result = committed "
            "trailers + exit code; no lane files)".format(
                worker["train"], ";".join(worker["assigned"]), worker["base"][:12]
            )
        )
    print(
        "session-hold: {} | push-policy: {} (the coordinator never pushes "
        "under 'human') | review-policy: {} (docs/process.toml [policies] "
        "review_rounds — the reviewer dial: {})".format(
            session_hold,
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
        "guardrails-policy: {} (docs/process.toml [policies] guardrails — the "
        "vendored core is injected per session when the policy selects that "
        "session's model)".format(guardrails_policy)
    )
    gate_log_count, gate_fail_open = _subagent_gate_log_count(root)
    if gate_log_count:
        print(
            "subagent-gate: {} decision(s) recorded in out/subagent-gate.log, "
            "{} of them FAIL-OPEN (a gate error let the spawn through) — "
            "OI-46 (2a); read the log for those first".format(
                gate_log_count, gate_fail_open
            )
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
    privacy_on = declared_policy(docs, "privacy-check", "false").lower() == "true"
    if privacy_on and not (branch or "").startswith("llm/"):
        print(
            "WARNING: privacy-checked repo (docs/process.toml [policies] "
            "privacy_check) but the current branch {!r} is not an llm/ "
            "iteration branch — see "
            'process-options.md "Agent iteration branch & sync".'.format(
                branch or "(none)"
            )
        )


@dataclass
class LoopRun:
    """The loop's MUTABLE half: the state an iteration is allowed to change.
    Declared separately from `LoopContext` (WI-483 slice 5) so "what a session
    may write" is a three-field record rather than a convention.

    - `state` is the lane run-state a worker reports through (always RUNNING
      until its committed evidence says otherwise — see worker_endstate).
    - `warned_no_core` is the once-per-run guardrails-core warning ledger,
      appended to by route_session.
    - `routing` is the S8 managed-routing / critique / stall cluster
      (RoutingState), which mutates across iterations by design.
    """

    # (An unquoted annotation, deliberately: a STRING annotation sends
    # dataclasses' KW_ONLY probe through sys.modules, which the test harness's
    # load_script import does not populate.)
    routing: RoutingState
    state: str = "RUNNING"
    warned_no_core: list = field(default_factory=list)


@dataclass(frozen=True)
class LoopContext:
    """Everything one iteration reads, resolved ONCE at loop start; the
    per-iteration behavior lives in run_iteration (WI-080 Slice E).

    FROZEN and TOTAL (WI-483 slice 5, program shape item 5 — "typed immutable
    config + explicit mutable runtime state"). This was an empty class
    populated as an attribute bag, which hid three things a declaration makes
    plain: that nothing in the loop ever re-resolves a dial mid-run; that
    `session_hold` was carried for no reader at all (dropped); and that
    `human_held` / `keep_nondependent` were read through
    `getattr(ctx, ..., <default>)`, so a field the constructor forgot would
    have silently become "human-held, don't keep going" instead of failing.
    A total record cannot be missing a field, so those two reads are now
    direct. Everything a session may WRITE lives behind `.run`, the one
    mutable field.
    """

    args: argparse.Namespace
    root: Path
    docs: Path
    lane: Path
    status_path: Path
    worker: dict
    managed: bool
    registry: dict
    enabled: list
    template: str
    model_map: dict
    cmd_map: dict
    prompt_templates: dict
    adjudicator_prompt_paths: tuple
    tier_map: dict
    prefer_map: dict
    weight_map: dict
    guardrails_policy: str
    human_held: bool
    keep_nondependent: bool
    start_dirty: list
    raw_dir: Path
    iter_dir: Path
    draw_iter_dirs: list
    tag: str
    use_live: bool
    reviews_dir: Path
    scoreboard: Path
    rp_int: int
    run: LoopRun


def adjudicator_home_root(root):
    """The dedicated-CLI-home root for retained adjudicator sessions (OI-69 (e1)
    — applied only once the dial is on). `AGENT_ADJUDICATOR_HOME` overrides;
    default `out/adjudicator/home/` under the repo (gitignored). Credentials are
    operator-PROVISIONED there (the owner's (e) answer on record) — the working
    directory, where CLAUDE.md/AGENTS.md/skills live, is never moved."""
    return os.environ.get("AGENT_ADJUDICATOR_HOME") or str(
        Path(root) / "out" / "adjudicator" / "home"
    )


def _adjudicator_resume_record(
    root, cfg, family, current_wi, route_id="", governing_hash_now=""
):
    """The record to RESUME against for this launch, or None to mint fresh (plan
    §3.4, evaluated before every launch). Retires (soft, keeps the generation
    count) and returns None when the session must not be resumed:

    - it is already `retired` (a prior reset);
    - its governing inputs changed and this row is a clear point;
    - `reset_on_same_artifact` is on and this row was already judged in the
      session (the strict rule-3 guard — retire immediately, no drain);
    - it is `draining` and this is a CLEAR POINT — this row does NOT continue a
      chain the session already judged, so retirement need not wait.

    A `draining` session whose next row DOES continue its chain (this row was
    judged before) keeps being resumed, so a review -> worker -> return -> review
    loop is never cut mid-way."""
    record = adjudicator_session.load(root, family, route_id)
    if not isinstance(record, dict):
        return None
    state = record.get("state")
    judged = record.get("judged") or []
    if state == adjudicator_session.STATE_RETIRED:
        return None
    governing_change = adjudicator_session.drain_reason(
        record, "", 0, governing_hash_now, ""
    )
    if governing_change:
        record["state"] = adjudicator_session.STATE_DRAINING
        adjudicator_session.save(root, record)
        state = record["state"]
    if cfg.reset_on_same_artifact and current_wi in judged:
        adjudicator_session.retire(root, record)
        return None
    if state == adjudicator_session.STATE_DRAINING:
        # A row that CONTINUES a chain the session judged is pending chain work
        # (not a clear point) — keep resuming; a row that does not is the clear
        # point that lets the draining session retire now.
        pending = [current_wi] if current_wi in judged else []
        if adjudicator_session.is_clear_point(pending):
            adjudicator_session.retire(root, record)
            return None
    return record


def adjudicator_launch(
    root,
    docs,
    family,
    brief,
    current_wi,
    tmpl,
    session_env,
    route_id="",
    template_paths=(),
):
    """Rewrite an adjudication session's launch for the retention layer (WI-540,
    plan §3.2/§4), returning `(tmpl, session_env, adj)`.

    A STRICT NO-OP when the dial is off or the row is not a retained class:
    `(tmpl, session_env, None)` unchanged — today's one-shot behaviour
    byte-for-byte. When on and the session's `brief` class is in `retain_for`,
    the family's one-shot template becomes its mint-or-resume form and the launch
    env points at the family's dedicated home; `adj` carries what the post-run
    `adjudicator_bookkeeping` needs to update the store (the family, the row, the
    session id it judges under, the id newly minted this launch, and the
    governing-inputs hash the reset rule compares)."""
    cfg = agent_common.adjudicator_config(docs)
    fam = (family or "").upper()
    if not cfg.enabled or not fam or not route_id or brief not in cfg.retain_for:
        return tmpl, session_env, None
    hash_now = adjudicator_session.governing_hash(root, template_paths)
    record = _adjudicator_resume_record(root, cfg, fam, current_wi, route_id, hash_now)
    new_tmpl, mint_id = adjudicator_session.resume_template(fam, tmpl, record)
    home_env = adjudicator_session.dedicated_home_env(
        fam, session_env, adjudicator_home_root(root)
    )
    merged_env = {
        **(session_env if session_env is not None else os.environ),
        **home_env,
    }
    session_id = (record.get("session_id") if record else "") or mint_id
    return (
        new_tmpl,
        merged_env,
        {
            "family": fam,
            "brief": brief,
            "wi": current_wi or "",
            "session_id": session_id,
            "mint_id": mint_id,
            "route_id": route_id,
            "governing_hash": hash_now,
            "resumed": bool(record),
        },
    )


def route_session(ctx, i, current_wi, session, resume_reconcile, now):
    """Pick the phase + model + prompt for this worker session (managed
    routing or the single-model path; WI-210 — every loop session is a
    claimed worker session). Returns an int exit code to end the
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
    warned_no_core = ctx.run.warned_no_core
    reviews_dir = ctx.reviews_dir
    st = ctx.run.routing
    is_review = False
    is_critique = False
    relaxed = False  # C5: a same-family review draw this session (recorded)
    verdict_path = None
    hold = None  # a declared adjudicator brief that could not be composed
    brief_key = ""  # the adjudicator brief this session was composed from
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
        phase, pinned_tier = row_routing(
            phase, worker["rows"].get(current_wi) if worker and current_wi else None
        )
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
        # WI-264 (win-stay/lose-shift, live): on a win the last escalation left
        # st.next_primary set to the winning reviewer FAMILY — prefer that family
        # as THIS review round's primary feedback source, OVERRIDING the WI-263
        # weighted baseline for the draw. A loss/page/swap left it None -> () ->
        # the weighted baseline stands (lose-shift). Gated to review draws because
        # next_primary is defined as the feedback source, not the implementer.
        # Fail-open: an unknown/disabled/cooling family also resolves to () and
        # never wedges the session (and select() drops any off-tier pin).
        winstay_pref = (
            agent_route.winstay_preferred_ids(
                st.next_primary, enabled, registry, st.cooldowns, now
            )
            if is_review
            else ()
        )
        phase_pin = [prefer_map[phase]] if phase in prefer_map else ()
        # Win-stay first -> it takes precedence over the static phase pin; both
        # only pin an id that survives the tier/heterogeneity pool filter.
        preferred_ids = list(winstay_pref) + list(phase_pin)
        route_id, reason, route_stop = draw_session_route(
            ctx, st, phase, tier, exclude, prefer_different, preferred_ids, now
        )
        if route_stop is not None:
            return route_stop
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
        # (LLR-061) — the review belongs to (train scope, reviewed commit),
        # never to a mutable branch tip.
        reviewed_sha = ""
        if worker:
            reviewed_sha = (
                st.impl_range.split("..")[1]
                if st.impl_range and ".." in st.impl_range
                else head_sha(root)
            ) or ""
        if is_review:
            relaxed = st.note_review_family(route_family)
            verdict_path = fresh_verdict_path(
                reviews_dir,
                "{}-{}-{}{}.md".format(
                    session, phase, reviewed_sha[:7], "-relaxed" if relaxed else ""
                ),
            )
            body = reviewer_prompt(
                prompt_templates, phase, verdict_path, root=root, worker=worker
            )
        elif is_critique:
            verdict_path = fresh_verdict_path(
                reviews_dir, "{}-CRITIQUE-{}.md".format(session, reviewed_sha[:7])
            )
            brief = critique_brief(root, docs, st.critique_scope)
            body = critique_prompt(prompt_templates, verdict_path, brief)
        else:
            body, verdict_path, hold, brief_key = session_body(
                root,
                worker,
                current_wi,
                session,
                reviewed_sha,
                reviews_dir,
                prompt_templates,
            )
    else:
        phase, model = session_model(model_map, args.model)
        tmpl = session_template(cmd_map, template, phase)
        # The same fork as the managed arm above: which BRIEF a claimed
        # adjudication row gets is a property of the ROW, not of whether a
        # routing registry happens to be configured.
        body, verdict_path, hold, brief_key = session_body(
            root,
            worker,
            current_wi,
            session,
            head_sha(root) or "",
            reviews_dir,
            prompt_templates,
        )
    if hold:
        # Fail CLOSED (SN-026 x SN-032): never hand a judge the builder's
        # instructions. The exit code is what makes the hold durable.
        stop_banner(
            status_path,
            "NEEDS-HUMAN — adjudication row {} has no usable brief".format(current_wi),
            hold + "\n\n" + ADJUDICATION_HOLD_NOTE,
        )
        return EXIT_NEEDS_HUMAN
    prompt, guarded = compose_session_prompt(
        model,
        body,
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
    # WI-540: the adjudicator session-retention launch rewrite (plan §3.2/§4).
    # A strict no-op when the dial is off or the brief class is not retained —
    # `tmpl`/`session_env` are exactly today's and `adj` is None. The actual
    # loaded adjudication-template paths are carried out of
    # preflight and folded into the governing hash here.
    tmpl, session_env, adj = adjudicator_launch(
        root,
        docs,
        route_family,
        brief_key,
        current_wi,
        tmpl,
        session_env,
        route_id=route_id,
        template_paths=ctx.adjudicator_prompt_paths,
    )
    return {
        "phase": phase,
        "is_review": is_review,
        "is_critique": is_critique,
        "model": model,
        "tmpl": tmpl,
        "prompt": prompt,
        "guarded": guarded,
        "verdict_path": verdict_path,
        # The brief this session was composed from, "" for every other session
        # — the ADJUDICATE validation arm's whole trigger, and a typed field
        # rather than a re-derivation from the phase, which cannot say WHICH.
        "brief": brief_key,
        "route_id": route_id,
        "route_family": route_family,
        "session_env": session_env,
        # C5: this session is a review drawn with heterogeneity relaxed — a
        # typed field for the telemetry header, never a filename re-parse.
        "relaxed": relaxed,
        # WI-540: the adjudicator retention launch metadata (plan §3), None on
        # every session the layer does not retain — the store update and reset
        # rule in session_bookkeeping key on its presence.
        "adjudicator": adj,
    }


def adjudication_bookkeeping(plan, worker, st, managed, route_id, now):
    """Record whether an ADJUDICATE session actually RULED. A no-op for every
    other session (the guard is here rather than at the call site so
    `session_bookkeeping` gains no branch for it).

    The review and critique arms have read their verdict file since they
    existed; an adjudication had no such arm at all. Its session ends through
    `worker_endstate`, which is judged from committed `WI:` trailers — so a
    judge that committed ANYTHING scored DONE, and the loop reported a ruling
    that had never been made. The deliverable of a judgement is the verdict
    artifact the brief named, carrying the closed-enum line the brief demanded;
    nothing else is evidence that a judgement happened.

    Cleared on success, so a re-run that DOES rule can complete: this is a
    per-session judgement, not a latch."""
    if not plan.get("brief"):
        return
    owed = adjudicate_brief.verdict_refusal(plan["brief"], plan["verdict_path"])
    worker["adjudication_owed"] = owed or ""
    if not owed:
        return
    print("adjudicate [{}]: not complete — {}".format(plan["brief"], owed))
    if managed and route_id:
        # The unparseable-review-verdict shape: cool the model and let the next
        # session re-route, rather than re-asking the one that just failed to
        # answer in the required form.
        st.cool(route_id, now)


@dataclass(frozen=True)
class PageConsequence:
    """What a page-human ruling MEANS for this run — the ONE rule both S8 page
    paths (a review escalation, an exhausted critique budget) obey, stated once
    (WI-483 slice 6). `stop` ends the run with EXIT_NEEDS_HUMAN; `design_check`
    re-arms the design-check phase instead, and is only ever true when the run
    is NOT stopping (the stop path returns before that arm, as it always did).
    """

    stop: bool
    design_check: bool


def page_consequence(fa, force_block=False):
    """The pure decision behind a page: SN-029 keys the stop on the MODE the
    ordinal produced, not on the retired enum word. `force_block` is the
    critique arm's declared `exhaustion = block`, which stops the run whatever
    the hold says."""
    stop = (fa["mode"] == "human-held" and not fa["keep_nondependent"]) or force_block
    return PageConsequence(
        stop=stop, design_check=(not stop) and bool(fa.get("design_check"))
    )


def apply_page_consequence(ctx, cons, title, detail):
    """The EFFECT half of a page: a worker has no lane files, so its exit code
    and the stop banner carry the page. Returns EXIT_NEEDS_HUMAN to end the
    run, else None."""
    if cons.stop:
        stop_banner(ctx.status_path, title, detail)
        return EXIT_NEEDS_HUMAN
    if cons.design_check:
        ctx.run.routing.set_design_check()
    return None


def reroute_rate_limited(st, route_id, reset_hint, now):
    """Generalize the rate-limit backoff PER-MODEL: cool this model and
    re-route to another available one next iteration. select() pages if none is
    left rather than dropping to a weaker tier (no silent swap)."""
    wait = seconds_until_reset(reset_hint) or st.cooldown_seconds
    st.cool(route_id, now, wait)
    print("route: {} rate-limited; cooled ~{}s, re-routing".format(route_id, int(wait)))
    return "reroute"


def absorb_review_verdict(st, plan, outcome, now):
    """Take one reviewer session's verdict into the round, or fail CLOSED.
    Both failure arms — no verdict file at all, and a file with no parseable
    `VERDICT:` machine line (a routine LLM garble) — cool the model and
    re-route the SAME review phase; neither is an approval or a burnable round
    (repo-review 2026-07-21 H-1)."""
    phase = plan["phase"]
    route_id = plan["route_id"]
    v = read_verdict(plan["verdict_path"], plan["route_family"])
    if v is None:
        st.cool(route_id, now)
        st.note_review_draw_failure()  # C1/C2: a failed draw, not a build stall
        print(
            "route: {} review [{}] wrote no verdict ({}); cooled, re-routing".format(
                route_id, phase, outcome
            )
        )
        return
    if v.verdict is None:
        st.cool(route_id, now)
        st.note_review_draw_failure()  # C1/C2: a garbled draw, not a build stall
        print(
            "route: {} review [{}] verdict file has no parseable "
            "VERDICT line; cooled, re-routing".format(route_id, phase)
        )
        return
    st.record_review_verdict(phase, v, plan["route_family"], route_id)


@dataclass(frozen=True)
class RoundSubstance:
    """One review round's substance scores, resolved together because they are
    one comparison: `margin` and `primary` are only meaningful across a PAIR.
    Substance/corroboration key on Family (who trained it), so a cross-family
    overlap outweighs a same-family one; the scoreboard tallies by that same
    Family key.

    `primary` is the winning family, or None when the round had a single
    reviewer (no comparison to win) — annotated `object` rather than a lying
    `str`, since this module carries no `typing` import and a STRING annotation
    breaks dataclasses' KW_ONLY probe under the suite's load_script import.
    """

    family_substance: dict
    margin: float
    primary: object


def round_substance(st, root):
    """Score each verdict in the completed round against its peer."""
    family_substance = {}
    subs = []
    for j, (_ph, rv, rfam, _mid) in enumerate(st.round_verdicts):
        peer = st.round_verdicts[1 - j][1] if len(st.round_verdicts) == 2 else None
        fams = (
            (rfam, st.round_verdicts[1 - j][2]) if len(st.round_verdicts) == 2 else None
        )
        s = score_reviews.substance(rv, root, other=peer, providers=fams)
        subs.append((rfam, s))
        if rfam:
            family_substance[rfam] = s
    margin = abs(subs[0][1] - subs[1][1]) if len(subs) == 2 else 0.0
    primary = None
    if len(subs) == 2:
        primary = subs[0][0] if subs[0][1] >= subs[1][1] else subs[1][0]
    return RoundSubstance(
        family_substance=family_substance, margin=margin, primary=primary
    )


def impl_changed_paths(root, st, train):
    """The implementer's own changed paths over the reviewed range, for the
    anti-gaming tripwires. The whole-train range (WI-183; the only range now,
    WI-210) legitimately carries THIS train's own committed verdicts,
    scoreboard, and session telemetry from earlier rounds — a rework round must
    not read them as "the implementer touched a review path" (the false-fire
    this excludes). A gamed verdict is still caught upstream: the integrator
    verifies verdicts on the exact reviewed head (LLR-140)."""
    if not (st.impl_range and ".." in st.impl_range):
        return []
    _rc, diff_out = git(root, "diff", "--name-only", st.impl_range)
    own = "docs/reviews/{}/".format(train)
    return [
        ln
        for ln in diff_out.splitlines()
        if ln.strip()
        and not ln.replace("\\", "/").startswith(own)
        and not ln.replace("\\", "/").startswith("docs/iteration")
    ]


def apply_rework_scope(worker, st, merged):
    """The merged verdict's consequence for the NEXT build session. A worker's
    rework scope is assignment-scoped in-process state (LLR-061) — never the
    lane's tracked docs/rework-wi pointer, which a train branch must not carry
    (and which retired with the serial driver, WI-210). The verdict text itself
    is embedded in the next build session's prompt."""
    if merged == "CHANGES-REQUESTED":
        worker["rework"] = "\n".join(
            (rv.text or "").strip()
            for (_ph, rv, _f, _m) in st.round_verdicts
            if (rv.text or "").strip()
        )
        worker["rework_wi"] = st.last_impl_wi or ""
        print(
            "dispatch: CHANGES-REQUESTED -> assignment-scoped rework of {}".format(
                worker["rework_wi"] or "the train"
            )
        )
    elif merged == "APPROVE":
        worker["rework"] = ""
        worker["rework_wi"] = ""


def complete_review_round(ctx, session):
    """The round is full: merge, score, record, escalate, and apply. Returns an
    int exit code (a page-human) or None."""
    st = ctx.run.routing
    scoreboard = ctx.scoreboard
    # C2: a completed round IS the owed review landing — drop the parked
    # marker so a later resume does not re-schedule a round already served.
    clear_review_owed(ctx.root)
    verdicts = [v for (_ph, v, _p, _m) in st.round_verdicts]
    merged, contradiction = score_reviews.merge_verdict(verdicts)
    sub = round_substance(st, ctx.root)
    fired = score_reviews.fired_tripwires(
        verdicts, changed_paths=impl_changed_paths(ctx.root, st, ctx.worker["train"])
    )
    round_info = {
        "verdict": merged or "",
        "tier": st.last_impl_tier,
        "margin": sub.margin,
        "primary": sub.primary,
        "tripwire": bool(fired),
        "contradiction": contradiction,
    }
    # Record the round for the escalation policy. Slice-C note: the append and
    # the round_verdicts clear (below) stay at their original distinct
    # positions rather than folding into one st.complete_round() call — the
    # worker-rework handler between escalation() and the clear still reads
    # st.round_verdicts, so a single append+clear would either empty that read
    # or hide the round from escalate(). Behavior (content + console order) is
    # preserved exactly.
    st.rounds.append(round_info)
    try:
        score_reviews.record_round(scoreboard, round_info, sub.family_substance)
    except OSError:
        pass
    # The scoreboard is coordinator-written state too — commit it in its own
    # telemetry commit the moment the round records (WI-137), not on the next
    # session's commit.
    commit_telemetry(ctx.root, session, "review scoreboard", [scoreboard])
    print(
        "review round: merged={} margin={:.2f} tripwires={} heterogeneity={} "
        "(advisory scoreboard {})".format(
            merged,
            sub.margin,
            ",".join(fired) or "none",
            "relaxed" if st.round_relaxed else "cross-family",
            scoreboard,
        )
    )
    decision = st.escalation()
    print("escalate: {} — {}".format(decision["action"], decision["reason"]))
    apply_rework_scope(ctx.worker, st, merged)
    st.round_verdicts = []
    # State consequences of the escalation happen ONCE, here (WI-171 page
    # re-arm, swap/tier-up/changes-requested); the page branch below keeps only
    # the I/O (failure_action / banner / run-state). apply_decision first is
    # safe — failure_action does not read page_fails_since.
    st.apply_decision(decision["action"], merged, decision.get("next_primary"))
    if decision["action"] != "page-human":
        return None
    fa = agent_route.failure_action(ctx.human_held, ctx.keep_nondependent)
    print("route/failure ({}): {}".format(fa["mode"], fa["note"]))
    return apply_page_consequence(
        ctx,
        page_consequence(fa),
        "PAGE-HUMAN — review escalation",
        decision["reason"] + " | " + fa["note"],
    )


def review_bookkeeping(ctx, plan, outcome, session, now):
    """A reviewer session's consequences: absorb its verdict, then complete the
    round if this was the last one owed."""
    st = ctx.run.routing
    absorb_review_verdict(st, plan, outcome, now)
    if not st.round_ready():
        return None
    return complete_review_round(ctx, session)


def critique_budget_page(ctx, pre_rounds):
    """The critique budget is spent -> the S8 page-the-human semantics, keyed
    to the session hold (the same failure_action the review round uses). The
    critic gates iteration; the human owns final acceptance via Attest at gate
    closure."""
    st = ctx.run.routing
    fa = agent_route.failure_action(ctx.human_held, ctx.keep_nondependent)
    print(
        "critique/budget ({}): {} CHANGES-REQUESTED round(s) >= "
        "{} -> page-human: {}".format(
            fa["mode"], pre_rounds + 1, st.critique_limit, fa["note"]
        )
    )
    return apply_page_consequence(
        ctx,
        page_consequence(fa, force_block=st.critique_exhaustion == "block"),
        "PAGE-HUMAN — critique budget exhausted",
        "the critique loop hit its {}-round budget still CHANGES-REQUESTED | {}".format(
            st.critique_limit, fa["note"]
        ),
    )


def critique_bookkeeping(ctx, plan, outcome, now):
    """The perceptual arbiter (WI-068): read the critic's verdict, iterate
    BUILD<->CRITIQUE until APPROVE or the budget trips S8 escalation."""
    st = ctx.run.routing
    route_id = plan["route_id"]
    verdict_path = plan["verdict_path"]
    v = read_verdict(verdict_path, plan["route_family"])
    if v is None:
        # No verdict written (errored/stalled): cool + re-critique next pass
        # (the stall guard backstops a critic that never writes one).
        st.cool(route_id, now)
        print(
            "critique: {} wrote no verdict ({}); cooled, re-critiquing".format(
                route_id, outcome
            )
        )
        return None
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
        # A verdict file with no parseable `VERDICT:` machine line is NOT an
        # approval: fail closed exactly like a missing file (cool +
        # re-critique). Previously the "" fell through to
        # record_critique_verdict's else branch — scope reset, queue cleared,
        # silently approved (repo-review 2026-07-21 H-1; the WI-243 "fail
        # closed" lesson one layer down).
        st.cool(route_id, now)
        print(
            "critique: {} verdict file has no parseable VERDICT line; "
            "cooled, re-critiquing".format(route_id)
        )
        return None
    # record_critique_verdict resets critique_rounds on the page path, so
    # capture the exhausted count for the (byte-identical) budget print BEFORE
    # the call — the printed value is the post-increment round count, i.e.
    # pre-call rounds + 1.
    pre_rounds = st.critique_rounds
    if st.record_critique_verdict(merged) != "page":
        # "rework" (next_phase set to BUILD) / "approved" (the loop ended) need
        # nothing more from the caller.
        return None
    return critique_budget_page(ctx, pre_rounds)


def schedule_review_round(ctx, after):
    """The review round follows the reviewer dial (S8). A traincar is ONE
    review scope (WI-183, LLR-140): a worker schedules the round only once
    EVERY assigned WI is built, and the round covers the combined train diff
    base..HEAD — never a per-WI slice of it. An intermediate constituent commit
    is accepted-on-train (locally green and committed), not reviewed; the cycle
    comes once, at the end."""
    st = ctx.run.routing
    worker = ctx.worker
    if ctx.rp_int < 1:
        return
    built_now, _blk = train_evidence(ctx.root, worker["base"])
    if not all(w in built_now for w in worker["assigned"]):
        return
    st.set_train_range("{}..{}".format(worker["base"], after))
    queued = st.schedule_review_round()
    print(
        "dispatch: review-policy {} -> scheduling review round {} "
        "over the whole train diff".format(ctx.rp_int, queued)
    )


def schedule_critique_round(ctx, commits):
    """The critique round is INDEPENDENT of the review dial (WI-068): it fires
    only when this build's WI touches a Critique-verified SR. Vacuous when no
    Critique SR exists, so a non-adopter pays nothing."""
    st = ctx.run.routing
    if not st.critique_srs:
        return
    scope_wis = build_scope_wis(ctx.root, ctx.docs, commits)
    in_scope = build_scope_srs(ctx.root, ctx.docs, commits) & st.critique_srs
    if not in_scope:
        return
    # A NEW scope starts a fresh budget; a rework of the SAME scope (a
    # CHANGES-REQUESTED loop) preserves the count, so the budget actually
    # bounds the loop (schedule_critique folds that reset in; critique_control
    # does not read the round count, so the order is identical to before).
    limit, exhaustion = critique_control(ctx.docs, scope_wis, st.critique_max)
    st.schedule_critique(in_scope, limit, exhaustion)
    print(
        "dispatch: build touches Critique SR(s) {} -> scheduling "
        "CRITIQUE round (budget {}, exhaustion {})".format(
            ",".join(sorted(in_scope)),
            "inf" if limit is None else limit,
            exhaustion,
        )
    )


def report_cooled_model(ctx, route_id, outcome, code):
    """Say WHY the pool is shrinking, at the moment it shrinks — the WAITING/no-verdict siblings already do; this path
    was silent. The row's Notes carries the actionable hint (auth/install), and
    the session log holds the full transcript (WI-109)."""
    note = ctx.registry[route_id].notes
    print(
        "route: {} session outcome={} (exit {}); cooled ~{}s, re-routing{}".format(
            route_id,
            outcome,
            code,
            int(ctx.run.routing.cooldown_seconds),
            " — " + note if note else "",
        )
    )


def build_bookkeeping(ctx, plan, outcome, code, commits, after, wi_label, now):
    """A non-judging session's consequences: cool a broken model, or schedule
    what a committing build owes, or clear the design-check flag."""
    st = ctx.run.routing
    route_id = plan["route_id"]
    phase = plan["phase"]
    if outcome in ("ERROR", "TIMEOUT"):
        st.cool(route_id, now)
        report_cooled_model(ctx, route_id, outcome, code)
        return
    if outcome == "COMMITTED" and phase not in NON_BUILD_PHASES:
        st.on_committed_build(plan["route_family"], wi_label, commits)
        schedule_review_round(ctx, after)
        schedule_critique_round(ctx, commits)
    elif phase == "DESIGN-CHECK":
        # The design-check ruling has run (its verdict is in the commit / log);
        # resume building. Without a tracked run-phase this reset is in-process
        # (WI-180) — the agent no longer advances a phase file.
        st.after_design_check()


def session_bookkeeping(
    ctx, plan, outcome, code, commits, after, reset_hint, now, session, wi_label
):
    """The managed-routing / reviewer-dispatch consequences of one session
    (S8): cool+re-route, review-round merge/scoreboard/escalation, critique
    arbitration, committed-build scheduling, design-check reset. Returns None
    (fall through), "reroute" (the managed-WAITING re-route), or an int exit
    code (a page-human).

    WI-483 slice 6 decomposed this OUTWARD into the four arms below plus the
    decisions each of them makes; what is left is the ladder itself, so a
    reader sees WHICH consequence applies before reading what it does."""
    st = ctx.run.routing
    # The ADJUDICATE validation arm, unconditional (see the function): an
    # adjudication row gets its brief on BOTH routing paths, so it owes its
    # verdict on both — unlike everything below, which is managed-only.
    adjudication_bookkeeping(plan, ctx.worker, st, ctx.managed, plan["route_id"], now)
    # --- managed routing / reviewer dispatch bookkeeping (S8) -------------
    # All of this is gated on managed mode; the legacy path never enters it.
    if not ctx.managed:
        return None
    if outcome == "WAITING":
        return reroute_rate_limited(st, plan["route_id"], reset_hint, now)
    if plan["is_review"]:
        return review_bookkeeping(ctx, plan, outcome, session, now)
    if plan["is_critique"]:
        return critique_bookkeeping(ctx, plan, outcome, now)
    return build_bookkeeping(ctx, plan, outcome, code, commits, after, wi_label, now)


def adjudicator_bookkeeping(ctx, plan, data, timed_out, now, output=""):
    """Update the retained adjudicator session store after one adjudication and
    evaluate the reset rule (plan §3.3/§3.4). Returns the two derived telemetry
    columns `{"session-gen","reset-reason"}` for the log row; a no-op returning
    blanks when the layer did not retain this session (`plan["adjudicator"]` is
    None — the dial-off case, byte-for-byte today's behaviour).

    Called BEFORE `session_meta` (rather than inside `session_bookkeeping`, plan
    §4's nominal home) precisely so its two columns ride the same log row; the
    store MUTATION is the plan's session_bookkeeping step, hoisted."""
    adj = plan.get("adjudicator")
    if not adj:
        return adjudicator_session.empty_bookkeeping()
    cfg = agent_common.adjudicator_config(ctx.docs)
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))
    observation = adjudicator_session.context_telemetry(
        adj["family"],
        data,
        output,
        plan.get("session_env"),
        adj.get("session_id") or "",
    )
    return adjudicator_session.bookkeep(
        ctx.root,
        adj,
        cfg,
        observation,
        timed_out,
        bool(data.get("is_error")),
        stamp,
    )


def wait_out_blackout(lane):
    """WI-148: a declared docs/blackout window pauses NEW sessions on UTC
    weekdays. The in-flight session already wrapped normally (the pause
    semantic), so here we simply wait the window out and then let this
    iteration's session start — no iteration budget is consumed by waiting (we
    sleep inline, never `continue`), so a single walk-away launch survives the
    blackout and resumes automatically. Absent/disabled file => a no-op.

    WI-261: a prominent banner + a periodic countdown heartbeat (vs the old
    one-liner) so a walk-away launch reads as deliberately WAITING, not hung.
    Same wait semantics — total sleep is exactly `wake` seconds."""
    blackout_line = declared_policy(lane, "blackout", "")
    wake = blackout_wake(blackout_line, datetime.datetime.utcnow())
    if not wake:
        return
    resume_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=wake)
    blackout_wait(wake, blackout_line, resume_at, emit=print, sleep=time.sleep)


def current_assignment_wi(root, worker):
    """The WI this session claims (WI-137): the first assigned WI without
    committed evidence, else the rework target (else the last assigned).

    (The §7 continuation re-check retired with session grouping, WI-383 /
    §A6.1. It re-asked, once per successor, whether the classifier still
    permitted a MULTI-WI grouping — a guard that only ever had work to do
    because the dispatcher packed independent WIs into one session. With
    packing deleted, the only multi-WI assignment left is the spine batch the
    dispatcher admits deliberately (§A4), whose constituents are homogeneous by
    construction: the guard's sole non-refusing case. A check that can only
    ever say yes is not a safeguard.)"""
    built, _blk = train_evidence(root, worker["base"])
    remaining = [w for w in worker["assigned"] if w not in built]
    return (
        remaining[0]
        if remaining
        else (worker.get("rework_wi") or worker["assigned"][-1])
    )


def stamp_session_meta(meta, plan, timed_out):
    """C3/C5 telemetry: WHICH deadline killed a TIMEOUT session (`wall` or
    `idle`), and whether a review verdict was drawn with heterogeneity
    relaxed — typed header fields, so neither is a transcript grep later."""
    meta["timeout"] = "idle" if timed_out == "idle" else ("wall" if timed_out else "")
    meta["heterogeneity"] = "relaxed" if plan.get("relaxed") else ""


def resolve_idle_timeout(args):
    """C3: --session-idle-timeout > AGENT_SESSION_IDLE_TIMEOUT > 900 (the
    S8-knob idiom). 0 or negative disables the idle kill; None on the flag
    means "not given"."""
    idle = args.session_idle_timeout
    if idle is None:
        idle = _int_env("AGENT_SESSION_IDLE_TIMEOUT", 900, minimum=0)
    return idle if idle and idle > 0 else None


def launch_session(ctx, argv, stdin_input, session_env):
    """Run one agent session and time it on the COORDINATOR's own clock, so a
    duration exists even when the session dies before emitting JSON (spawn
    failure, timeout, crash). Returns (code, output, timed_out, wall_secs)."""
    args = ctx.args
    wall_start = time.time()
    live = LiveStatus(ctx.worker["train"]) if ctx.use_live else None
    if args.no_session_echo:
        on_line = None
    elif live is not None:
        on_line = live.event
    else:
        on_line = echo_session_line
    code, output, timed_out = run_session(
        argv,
        ctx.root,
        args.session_timeout,
        env=session_env,
        on_line=on_line,
        stdin_input=stdin_input,
        idle_timeout=resolve_idle_timeout(args),
    )
    if live is not None:
        live.finish()
    return code, output, timed_out, int(round(time.time() - wall_start))


def write_raw_stream(raw_dir, name, output):
    """The raw session stream: debug convenience, never load-bearing — so
    every filesystem failure here is swallowed."""
    try:
        raw_dir.mkdir(parents=True, exist_ok=True)
        (raw_dir / name).write_bytes(output.encode("utf-8", "replace"))
    except OSError:
        pass


def family_context_telemetry(family, data):
    """Session id + context occupancy/window/percent, read straight off the
    process's OWN JSON result (WI-535, telemetry first — no mint, no resume,
    no adapter; that's the retention layer, WI-540). Returns
    `(session_id, occupancy, window, pct)`, every field `""` where the
    family's plain one-shot call doesn't carry it today.

    ANTHROPIC's stream-json result already carries `session_id`. Occupancy is
    its four usage counters summed (plan §3.3: input + cache_read +
    cache_creation + output). Window is the unique `modelUsage` entry whose
    same four counters match; absent/ambiguous matches stay blank rather than
    guessed (plan §2). This distinguishes the session's own turn from a
    colliding subagent aside. Duplicate full matches remain ambiguous even if
    their windows agree. OPENAI/OPENCODE's one-shot templates emit none of
    this yet; WI-540's per-family adapter is what adds it."""
    if family != "ANTHROPIC":
        return "", "", "", ""
    return adjudicator_session.anthropic_context_telemetry(data)


def session_meta(
    ctx, plan, data, session, stamp, wi_label, outcome, commits, code, wall_secs
):
    """The session log's row, projected from the agent's JSON result. Stays a
    dict rather than a record because it IS the log's column set — write_session_log
    writes exactly these keys, in this order.

    Where the wall time went: API round-trips vs local tool execution (the gap
    is the harness running gates/tools). Blank when the CLI reported no JSON
    result — the wall clock still stands.

    Session-shape telemetry (WI-124): why a session was slow, not just that it
    was. ttft = boot-to-first-token (the initial context-ingest latency); cache
    read/create = context volume carried per turn / ingested fresh at session
    start; effort + fast-mode name the two per-turn speed dials so their
    experiments are measurable per row; prompt-chars sizes the instruction the
    coordinator composed. All blank when the CLI reported no JSON (the
    effort/prompt pair still stands — the coordinator knows what it launched).
    """
    prompt = plan["prompt"]
    phase = plan["phase"]
    usage = data.get("usage") or {}
    session_id, ctx_used, ctx_window, ctx_pct = (
        adjudicator_session.prefer_retained_context(
            family_context_telemetry(plan.get("route_family") or "", data),
            plan.get("adjudicator_telemetry") or {},
        )
    )
    tokens = ""
    if usage.get("input_tokens") is not None or usage.get("output_tokens") is not None:
        tokens = "{}+{}".format(
            usage.get("input_tokens", 0), usage.get("output_tokens", 0)
        )
    api_ms = data.get("duration_api_ms")
    ttft_ms = data.get("ttft_ms")
    return {
        "session": session,
        "stamp": stamp,
        "date": time.strftime("%Y-%m-%d %H:%M"),
        "train": ctx.worker["train"],
        "base": ctx.worker["base"][:12],
        "phase": phase,
        "wi": wi_label,
        "model": plan["model"],
        "guardrails": "on" if plan["guarded"] else "",
        "outcome": outcome,
        "commits": commits,
        "tokens": tokens,
        "cost-usd": data.get("total_cost_usd", ""),
        "wall-secs": wall_secs,
        "api-secs": int(round(api_ms / 1000.0))
        if isinstance(api_ms, (int, float))
        else "",
        "turns": data.get("num_turns", ""),
        "ttft-secs": int(round(ttft_ms / 1000.0))
        if isinstance(ttft_ms, (int, float))
        else "",
        "cache-read": usage.get("cache_read_input_tokens", ""),
        "cache-create": usage.get("cache_creation_input_tokens", ""),
        "effort": (plan["session_env"] or os.environ).get(
            "CLAUDE_CODE_EFFORT_LEVEL", ""
        ),
        "fast": data.get("fast_mode_state", "") or "",
        "prompt-chars": len(prompt),
        # SN-026: WHICH template, and what it rendered to. The pair is what
        # makes a session's instruction auditable after the fact — the source
        # is a file `prompts/CATALOG.md` lists by digest, the result is this
        # row's own fingerprint, and neither requires keeping rendered prompts
        # on disk. An override path shows HERE rather than only in the launch
        # flags, so a substituted prompt is visible in the telemetry.
        "prompt-template": prompt_source(ctx.prompt_templates, phase),
        "prompt-sha": agent_common.prompt_fingerprint(prompt),
        "exit-code": code,
        # WI-535: the adjudicator-retention plan's telemetry-first step
        # (docs/plans/2026-08-29-adjudicator-session-retention-plan.md §3.3) —
        # what the process already reports about its own context, per family,
        # with the retention dial off. Blank wherever today's one-shot call
        # doesn't carry it (family_context_telemetry).
        "session-id": session_id,
        "context-used": ctx_used,
        "context-window": ctx_window,
        "context-pct": ctx_pct,
        # WI-540: the retention layer's two derived columns (plan §4) — the
        # generation of the retained session this adjudication ran under, and the
        # reset reason if it crested/changed/failed. Blank on every session the
        # layer did not retain (dial off, or a non-adjudication session).
        "session-gen": (plan.get("adjudicator_telemetry") or {}).get("session-gen", ""),
        "reset-reason": (plan.get("adjudicator_telemetry") or {}).get(
            "reset-reason", ""
        ),
    }


@dataclass(frozen=True)
class LimitWait:
    """What a throttled session's reset hint BUYS: either a bounded nap and a
    retry, or nothing — in which case the run stops and the human resumes it
    after the reset. `nap` is the discriminator, so a zero-second wait is not
    mistaken for "no wait" (WI-483 slice 6)."""

    nap: bool
    seconds: int
    message: str


def rate_limit_wait(args, reset_hint):
    """The pure arithmetic behind a rate-limit backoff. A throttled session is
    not progress *or* a stall — never count it toward the stall guard (three
    throttled sessions would otherwise misread as a stall and abort, the NHW
    original's bug); that rule lives at the caller, which never reaches
    note_session on this path."""
    wait = seconds_until_reset(reset_hint)
    if args.wait_on_limit and wait is None:
        # Unrecognized reset wording (locale/format drift): a bounded fallback
        # nap keeps the walk-away run alive, capped at the ceiling the human
        # already consented to waiting.
        wait = min(args.limit_retry_fallback, args.wait_on_limit)
        return LimitWait(
            True,
            wait,
            "rate limit hit — reset time {!r} not recognized; "
            "sleeping {}s (--limit-retry-fallback) and retrying.".format(
                reset_hint, wait
            ),
        )
    if args.wait_on_limit and wait and wait <= args.wait_on_limit:
        return LimitWait(
            True,
            wait,
            "rate limit hit — sleeping {}s until the reset ({}).".format(
                wait, reset_hint
            ),
        )
    return LimitWait(False, 0, "")


# C4: the fixed liveness prompt. One word, so any healthy route of any family
# answers it inside the 30 s wall and a limit/outage page is unmistakable.
PROBE_PROMPT = "Reply with the single word OK"


def probe_route(row, root, wall=30):
    """(ok, transcript) for one C4 liveness probe: the row's CmdTemplate run
    VERBATIM (a template defect must be caught by the probe, not by a burned
    draw — the doubled --dir incident, 2026-08-30) with the fixed prompt and a
    30 s wall. `ok` means the session exited 0 inside the wall and the result
    carries the word OK."""
    try:
        argv, stdin_input = build_argv(row.cmd_template, row.model or "", PROBE_PROMPT)
    except ValueError as exc:
        return False, str(exc)
    row_env = agent_route.parse_env(row.env)
    env = {**os.environ, **row_env} if row_env else None
    code, output, timed_out = run_session(
        argv, root, wall, env=env, stdin_input=stdin_input
    )
    data = parse_json_result(output or "")
    result = str(data.get("result", "")) if data else (output or "")
    ok = code == 0 and not timed_out and re.search(r"\bOK\b", result) is not None
    return ok, (output or "")


def select_with_probe(
    ctx, st, phase, tier, exclude, prefer_different, preferred_ids, now
):
    """agent_route.select + the C4 pre-dispatch probe: a route whose history
    this run is UNCLEAN (it was cooled — ERROR, TIMEOUT, rate limit, garbled
    verdict) must answer a 30 s OK probe on its own CmdTemplate before a real
    session is spent on it; a failing probe cools the route with the reason
    (`limit` when the usage-limit shape matches, else `unreachable`) and the
    draw moves on. A route with a clean history is never probed — the probe
    is a recovery aid, not a tax. Bounded by the pool size."""
    for _ in range(len(ctx.enabled) + 1):
        route_id, reason = agent_route.select(
            ctx.enabled,
            ctx.registry,
            tier,
            now,
            st.cooldowns,
            exclude,
            prefer_different,
            preferred_ids,
            agent_route.phase_weights(ctx.weight_map, phase),
            phase_draw_ordinal(ctx.draw_iter_dirs, phase),
        )
        if route_id is None or route_id not in st.suspect_routes:
            return route_id, reason
        ok, transcript = probe_route(ctx.registry[route_id], ctx.root)
        if ok:
            st.suspect_routes.discard(route_id)
            return route_id, reason + " (probe OK)"
        hit = LIMIT_RE.search("\n".join(transcript.splitlines()[-15:]))
        why = "limit" if hit else "unreachable"
        wait = seconds_until_reset(hit.group(1)) if hit else None
        st.cool(route_id, now, wait)
        print(
            "probe [{}]: {}, cooled ~{}s".format(
                route_id, why, int(wait if wait else st.cooldown_seconds)
            )
        )
    return None, "every candidate failed its liveness probe"


def draw_session_route(
    ctx, st, phase, tier, exclude, prefer_different, preferred_ids, now
):
    """One draw of the session route, with the review ladder's two extra rungs
    (C2/C5, docs/plans/2026-08-30-stall-guard-plan.md): the probing select;
    for a review phase whose cross-family pool is exhausted, the RELAXED retry
    (heterogeneity dropped, recorded by the caller off the typed family fact);
    and, when nothing is routable at all for a worker's review, the REVIEW
    OWED park — never a NEEDS-HUMAN page the dispatcher would turn into a
    handback of finished work. Returns `(route_id, reason, exit_code)`; a
    non-None exit_code ends the run (the banner is already written)."""
    is_review = phase in REVIEW_PHASES
    route_id, reason = select_with_probe(
        ctx, st, phase, tier, exclude, prefer_different, preferred_ids, now
    )
    # Log the routing decision BEFORE launch (the no-silent-swap rule).
    print("route [{}]: {}".format(phase or "—", reason))
    if route_id is None and is_review:
        route_id, reason = select_with_probe(
            ctx, st, phase, tier, set(), False, preferred_ids, now
        )
        if route_id is not None:
            print("route [{}]: heterogeneity RELAXED — {}".format(phase or "—", reason))
    if route_id is None and is_review and ctx.worker:
        st.note_review_draw_failure()
        write_review_owed(
            ctx.root, ctx.worker, st, "no routable reviewer ({})".format(reason)
        )
        stop_banner(
            ctx.status_path,
            "REVIEW OWED — no routable reviewer",
            reason + "; the build is committed, the lane parks with its "
            "work (marker: out/review-owed) and the next cycle resumes "
            "it to draw the round.\n"
            + agent_route.pool_context(ctx.enabled, ctx.registry, st.cooldowns, now),
        )
        return None, reason, EXIT_REVIEW_OWED
    if route_id is None:
        # Every enabled model at the preferred tier-or-stronger is cooling
        # down or none is enabled: page rather than drop to a weaker tier.
        # (A worker never writes run-state — its exit code is the page; the
        # stop banner + exit code carry the outcome. The Notes cell is the
        # declared home for the provider's sign-in/install hint, WI-109.)
        stop_banner(
            ctx.status_path,
            "NEEDS-HUMAN — no routable model",
            reason + " (add/enable a model of this tier, or wait for a "
            "cooldown; the loop never silently drops to a weaker tier).\n"
            + agent_route.pool_context(ctx.enabled, ctx.registry, st.cooldowns, now),
        )
        return None, reason, EXIT_NEEDS_HUMAN
    return route_id, reason, None


def review_owed_marker(root):
    """The C2 parked-state marker: lane-local and gitignored, under out/ so it
    rides the lane worktree across worker restarts (the in-process
    review_queue does not) and is shed at unload with the loop's own
    artifacts (integrate's declared residue)."""
    return Path(root) / "out" / "review-owed"


def write_review_owed(root, worker, st, detail):
    """Persist the owed state's ADVISORY fields (the build's family for C5,
    the detail for the banner). Returns whether the marker was written. The
    marker is deliberately NOT the durable evidence — an untracked file
    whose write can fail is no evidence at all (round 3 finding): a resumed
    worker derives owed-ness from COMMITTED facts (`review_owed_by_evidence`)
    and recovers the family from the build's own session log when the marker
    is gone. A failed write is therefore loud, never silent."""
    path = review_owed_marker(root)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "# review owed (C2) — written by agent_loop; cleared when a round"
            " completes\ntrain = {}\nbase = {}\nfamily = {}\n"
            "draw_failures = {}\ndetail = {}\n".format(
                worker["train"],
                worker["base"],
                st.last_impl_family or "",
                st.review_draw_failures,
                detail,
            ),
            encoding="utf-8",
            newline="\n",
        )
        return True
    except OSError as exc:
        print(
            "agent_loop: WARNING - {} could not be written ({}); the owed round "
            "is still derived from committed evidence at resume".format(path, exc),
            file=sys.stderr,
        )
        return False


def read_review_owed(root):
    """The marker's `key = value` lines as a dict ({} when absent/unreadable).
    The one field a resume MUST restore is `family`: the committed build's
    family is the C5 heterogeneity key, and a fresh process has no memory of
    it — without it the first resumed draw would treat the builder's own
    family as cross-family and write an unmarked verdict (round 2 finding)."""
    try:
        text = review_owed_marker(root).read_text(encoding="utf-8")
    except OSError:
        return {}
    fields = {}
    for line in text.splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, _sep, value = line.partition("=")
            fields[key.strip()] = value.strip()
    return fields


def review_owed_by_evidence(root, worker, reviews_dir):
    """COMMITTED evidence that a review round is owed: every assigned WI
    carries its trailer on the branch, and no round verdict names the
    current HEAD. This is what a resumed worker trusts (a worker reads
    committed facts, never run-state) — the out/review-owed marker only adds
    advisory fields. A verdict for HEAD, of either outcome, means the round
    was served; a rework commit moves HEAD and owes a fresh one."""
    if not worker:
        return False
    built, _blocked = train_evidence(root, worker["base"])
    if not all(w in built for w in worker["assigned"]):
        return False
    head = (head_sha(root) or "")[:7]
    if not head:
        return False
    return not any(Path(reviews_dir).glob("*-REVIEW-?-{}*.md".format(head)))


def last_build_family(iter_dir, registry):
    """The family of the most recent BUILD session recorded in the lane's
    session logs (their `# phase:` / `# model:` headers, joined to the
    registry) — the C5 heterogeneity key when the marker did not survive.
    None when no build log names a registered model."""
    for path in sorted(Path(iter_dir).glob("*.log"), reverse=True):
        try:
            head = path.read_text(encoding="utf-8", errors="replace")[:4000]
        except OSError:
            continue
        phase = re.search(r"^# phase: ?(.*)$", head, re.M)
        model = re.search(r"^# model: ?(.*)$", head, re.M)
        if not (phase and model) or phase.group(1).strip() not in ("BUILD", ""):
            continue
        wanted = model.group(1).strip()
        for row in registry.values():
            if (row.model or row.id) == wanted:
                return row.family
    return None


def resume_owed_round(root, setup, st, rp_int, iter_dir, reviews_dir):
    """C2 resume: a parked review-owed lane owes its ROUND, not another
    build. Owed-ness is decided from committed evidence (the marker alone is
    not trusted — its write can fail); the family comes from the marker when
    it survived, else from the build's own session log, so C5's relaxed audit
    trail survives the restart either way."""
    if not (setup.routing.managed and rp_int >= 1 and setup.worker):
        return
    fields = read_review_owed(root)
    if not fields and not review_owed_by_evidence(root, setup.worker, reviews_dir):
        return
    st.set_train_range("{}..{}".format(setup.worker["base"], head_sha(root)))
    st.last_impl_family = fields.get("family") or last_build_family(
        iter_dir, setup.routing.registry
    )
    queued_round = st.schedule_review_round()
    print(
        "resume: review owed ({}) — scheduling review round {} over the parked "
        "train diff before any build session".format(
            "marker present"
            if fields
            else "committed evidence: built, no verdict for HEAD",
            queued_round,
        )
    )


def clear_review_owed(root):
    try:
        review_owed_marker(root).unlink()
    except OSError:
        pass


def review_owed_stop(ctx):
    """C2 (docs/plans/2026-08-30-stall-guard-plan.md): end the run REVIEW OWED
    when the ladder is exhausted — the build is committed, a round is still
    queued, and `--stall-limit` consecutive draws failed. The exit code is
    deliberately NOT a decided dispatcher outcome: the lane parks with its
    work and the next cycle resumes it to draw the round (owner direction
    2026-08-30 — a reviewer outage never closes finished work partial)."""
    st = ctx.run.routing
    if not st.review_queue or st.review_draw_failures < max(1, ctx.args.stall_limit):
        return None
    families = sorted(
        {ctx.registry[m].family for m in ctx.enabled if m in ctx.registry}
    )
    detail = "{} draw(s) failed on {}".format(
        st.review_draw_failures, ",".join(families) or "(no enabled family)"
    )
    write_review_owed(ctx.root, ctx.worker, st, detail)
    stop_banner(
        ctx.status_path,
        "REVIEW OWED — " + detail,
        "the build is committed and the review round is still queued; the "
        "lane parks with its work (marker: out/review-owed) and the next "
        "cycle resumes it to draw the round. No finished work is handed back "
        "over a reviewer outage.",
    )
    return EXIT_REVIEW_OWED


def stall_stop(ctx, verdict):
    """The stall guard's two stop banners. Returns EXIT_STALL to end the run,
    else None."""
    st = ctx.run.routing
    if verdict == "agent-error":
        # Every session that tripped the guard errored before working —
        # an unavailable agent, not a stuck task. Name it so, and point
        # at the fix (an unsupported model is repointed by hand).
        stop_banner(
            ctx.status_path,
            "STALL — agent error",
            "{} consecutive session(s) errored before doing work "
            "(agent unavailable / CLI or model error) — aborting. Check "
            "the AGENT_CMD model + auth and the latest {} "
            "log (outcome=ERROR, its exit-code); an unsupported model is "
            "fixed by pointing --model / the model map at a live "
            "tier.".format(st.errors, ctx.iter_dir),
        )
        return EXIT_STALL
    if verdict == "stall":
        stop_banner(
            ctx.status_path,
            "STALL",
            "{} consecutive session(s) without a commit — aborting to "
            "protect the budget. See the latest {} "
            "log.".format(st.stall, ctx.iter_dir),
        )
        return EXIT_STALL
    return None


def after_session(ctx, i, outcome, reset_hint, committed, judging=False):
    """What one finished session means for the RUN: the rate-limit nap or stop,
    the post-session worker end state, the stall guard, and the inter-session
    pause. Returns an int exit code to END the run, else None.

    (The run-state DONE/BLOCKED/NEEDS-HUMAN ladder retired with the serial
    driver, WI-210: a worker's state is always RUNNING here — its end states
    are judged from committed evidence, and the coordinator generates the root
    run-state.)"""
    args = ctx.args
    st = ctx.run.routing
    if outcome == "WAITING":
        limit = rate_limit_wait(args, reset_hint)
        if limit.nap:
            print(limit.message)
            time.sleep(limit.seconds)
            return None
        stop_banner(
            ctx.status_path,
            "WAITING on a rate limit",
            "resume at: {} (re-run agent-resume.* then)".format(reset_hint),
        )
        return EXIT_WAITING
    # Worker end-state after the session too — a completed assignment must
    # exit DONE here, not spend the remaining budget re-checking at the top.
    end = worker_endstate(
        ctx.root,
        ctx.worker,
        bool(st.review_queue or st.critique_queue),
        ctx.managed,
        ctx.rp_int,
    )
    if end:
        return worker_exit_banner(ctx.worker, end)
    st.note_session(committed, outcome == "ERROR", judging=judging)
    stop = stall_stop(ctx, st.stall_verdict(args.stall_limit))
    if stop is not None:
        return stop
    stop = review_owed_stop(ctx)
    if stop is not None:
        return stop
    if i < args.max_iterations and args.pause:
        time.sleep(args.pause)
    return None


def run_iteration(ctx, i):
    """One worker session end-to-end: guards, routing (route_session),
    launch, telemetry, bookkeeping (session_bookkeeping), and the outcome
    ladder (after_session) (WI-210 — the loop is the claimed-assignment worker
    engine; the serial resume driver and its docs/pause boundary are retired:
    pause stops NEW CLAIMS at the coordinator (§5.6) while an in-flight worker
    finishes its safe boundary). Returns an int exit code to END the run, or
    None to proceed to the next iteration (a `continue` path returns None
    early, so the trailing pause sleep — the last statement of after_session —
    is naturally skipped)."""
    args = ctx.args
    root = ctx.root
    worker = ctx.worker
    st = ctx.run.routing
    wait_out_blackout(ctx.lane)
    # (The WI-209 serial dual-plan quiet-park guard retired with the serial
    # driver, WI-210: a dual row runs through --dual-plan, so the
    # page-instead-of-idle duty has no second path left to cover.)
    # Inject the reconcile note into the first session's prompt only (see the
    # once-at-start rationale above); every later session's prompt is
    # unchanged from today.
    resume_reconcile = (
        RESUME_RECONCILE_NOTE + "\n\n---\n\n" if (i == 1 and ctx.start_dirty) else ""
    )
    # Worker end-state check BEFORE spending a session: a resumed worker
    # whose evidence is already complete (or blocked) exits immediately —
    # recovery reconstructs the same verdict from git alone (spec §11).
    # WI-239: a resumed worker's FIRST session (i == 1) is NOT short-circuited
    # by a pre-existing Blocked-WI trailer — a coordinator only re-dispatches a
    # blocked train when the base may have been cured, so the worker gets its one
    # chance to supersede the block with a completion; a block still standing
    # after the session exits BLOCKED (the post-session check honors it).
    current_wi = None
    if worker:
        end = worker_endstate(
            root,
            worker,
            bool(st.review_queue or st.critique_queue),
            ctx.managed,
            ctx.rp_int,
            allow_block_exit=(i > 1),
        )
        if end:
            return worker_exit_banner(worker, end)
        current_wi = current_assignment_wi(root, worker)
    session = "{:03d}".format(next_session_number(ctx.iter_dir, worker["train"]))
    stamp = time.strftime("%Y%m%d-%H%M%S")
    wi_label = current_wi
    before = head_sha(root)
    now = time.time()
    plan = route_session(ctx, i, current_wi, session, resume_reconcile, now)
    if isinstance(plan, int):
        return plan
    print(
        "=== session {} [{}] ({}/{}) | phase={} model={} wi={} ===".format(
            session,
            worker["train"],
            i,
            args.max_iterations,
            plan["phase"] or "—",
            plan["model"] or "—",
            current_wi,
        )
    )
    argv, stdin_input = build_argv(plan["tmpl"], plan["model"], plan["prompt"])
    code, output, timed_out, wall_secs = launch_session(
        ctx, argv, stdin_input, plan["session_env"]
    )
    write_raw_stream(ctx.raw_dir, "{}{}-{}.log".format(ctx.tag, session, stamp), output)
    data = parse_json_result(output)
    reset_hint = limit_reset_hint(output, data, code)
    after = head_sha(root)
    committed = before != after
    commits = "{}..{}".format(before or "(root)", after or "?") if committed else ""
    # A worker has no lane run-state (spec §10): its state is always RUNNING
    # until its committed evidence says otherwise (worker_endstate).
    ctx.run.state = "RUNNING"

    # (outcome, errored) via the session-outcome ladder — full semantics
    # (including the "failed before it could work" error rule) live in
    # classify_outcome's docstring (single-source, WI-080 Slice D).
    outcome, errored = classify_outcome(
        reset_hint, timed_out, ctx.run.state, committed, data, code
    )

    # WI-540: update the retained adjudicator session store and evaluate the
    # reset rule (plan §3.3/§3.4). Dial-off is a no-op; derived columns ride the log.
    plan["adjudicator_telemetry"] = adjudicator_bookkeeping(
        ctx, plan, data, timed_out, now, output
    )

    meta = session_meta(
        ctx, plan, data, session, stamp, wi_label, outcome, commits, code, wall_secs
    )
    stamp_session_meta(meta, plan, timed_out)
    log_path = write_session_log(ctx.iter_dir, meta, output)
    # A worker never regenerates the iteration index: it is a GENERATED
    # root artifact the integrator rebuilds on the composed tree (spec
    # §5.1) — two workers regenerating it would collide at integration.
    # Commit the coordinator's own bookkeeping now, in its own telemetry
    # commit — never let it ride the next session's work commit or dangle
    # (WI-137). The review scoreboard is committed at its own write, in
    # complete_review_round.
    commit_telemetry(
        root,
        ctx.tag + session,
        "{} {}".format(plan["phase"] or "—", outcome),
        [log_path],
    )
    print(
        "session {}: outcome={} commits={} wall={}s{}".format(
            session,
            outcome,
            commits or "—",
            wall_secs,
            " api={}s turns={}".format(meta["api-secs"], meta["turns"])
            if meta["turns"] != ""
            else "",
        )
    )
    r = session_bookkeeping(
        ctx, plan, outcome, code, commits, after, reset_hint, now, session, wi_label
    )
    if r == "reroute":
        return None
    if r is not None:
        return r
    judging = plan["is_review"] or plan["is_critique"]
    return after_session(ctx, i, outcome, reset_hint, committed, judging=judging)


def _coordinator_lock(root):
    """Take the per-checkout coordinator lock, registering its release for
    exit. Returns None when held, else the EXIT_PREFLIGHT the caller returns
    — the ONE home of the acquire/report/register sequence, shared by the
    drive mode and the explicit-role path."""
    lock_path = agent_common.dispatch_lock_path(root)
    lock_err = acquire_lock(lock_path)
    if lock_err:
        print("agent_loop: {}".format(lock_err), file=sys.stderr)
        return EXIT_PREFLIGHT
    atexit.register(release_lock, lock_path)
    return None


def _drive_entry(root, args):
    """The plain-launch drive mode (WI-374): coordinator lock, then the
    claim->build->integrate loop in the sibling dispatch.py — the dispatcher,
    renamed from drive.py with lane.py extracted at WI-381
    (docs/concurrency-v2.md §A4.2)."""
    import dispatch

    code = _coordinator_lock(root)
    if code is not None:
        return code
    return dispatch.run(root, args)


# --- loop startup: resolve the run, then run it --------------------------------
# The boundary (WI-483 slice 5): everything that RESOLVES what this run is —
# the effective root, the phase maps, the enable-list, the declared dials — is a
# pure function returning a typed record, and `main` is left with the EFFECTS
# (console, coordinator lock, subprocess) and the mode decisions between them.


def _resolve_root(args):
    """The effective root. A worker runs in its leased linked worktree, so
    --worktree IS the root: the branch guard, sessions and policy reads all
    resolve there (WI-181). Returns (root, None), or (None, EXIT_PREFLIGHT)
    when a named worktree does not exist."""
    if args.worktree:
        root = Path(args.worktree).resolve()
        if not root.is_dir():
            print(
                "agent_loop: --worktree {} does not exist".format(root),
                file=sys.stderr,
            )
            return None, EXIT_PREFLIGHT
        return root, None
    return Path(args.root).resolve(), None


def is_drive_launch(args):
    """A plain launch (no role flag) is the DRIVE mode (WI-374): the serial
    claim->build->integrate front end, restored after the parallel dispatcher's
    Phase 5 deletion took the scheduling front half with it. Any explicit role
    opts out of it."""
    return not (args.wi or args.train or args.interactive or args.dual_plan)


def _parse_session_maps(args):
    """The five "KEY=value" phase maps. They share a syntax and a failure mode,
    so they are parsed as one act: model / command-template / prompt-template
    FILE / tier / preferred registry id, each keyed by phase. Returns
    (maps, None) or (None, EXIT_PREFLIGHT)."""
    try:
        return (
            parse_map(args.model_map),
            parse_map(args.cmd_map),
            parse_map(args.prompt_map),
            parse_map(args.tier_map),
            parse_map(args.prefer_map),
        ), None
    except ValueError as exc:
        print("agent_loop: {}".format(exc), file=sys.stderr)
        return None, EXIT_PREFLIGHT


@dataclass(frozen=True)
class RoutingSetup:
    """What docs/agents.toml + docs/agents-enabled resolve to for this run."""

    registry: dict
    managed: bool
    enabled: list
    weight_map: dict
    reg_errors: list
    enable_errors: list


def resolve_routing_setup(docs):
    """The S8 routing layer (process-options.md "Unattended operation" ->
    routing/escalation). The enable-list's PRESENCE turns managed routing +
    loop-side reviewer dispatch on; ABSENT files keep exactly today's single
    AGENT_CMD/AGENT_MODEL behavior, so a fresh scaffold pays nothing (no silent
    model swap — consent = the enabled set + the declared rules).

    Presence, not resolvability, is the switch: an unresolvable token must fail
    preflight rather than silently fall back to the legacy path. Malformed
    per-phase draw-weight annotations (WI-236), unresolvable tokens and
    conflicting weight redeclarations therefore all come back as errors under
    the agents-enabled heading — the file is the consent surface, never
    silently ignored."""
    registry, reg_errors = agent_route.load_registry(docs / "agents.toml")
    enabled_entries, annot_errors = agent_route.load_enabled_entries(
        docs / "agents-enabled"
    )
    raw_enabled = [token for token, _weights in enabled_entries]
    # Version-less tokens resolve to concrete pair-row ids (exact-id, else newest
    # in the Family-Model line).
    tag_rank = agent_route.load_tag_rank(docs / "agents.toml")
    enabled, resolve_errors = agent_route.resolve_enabled(
        raw_enabled, registry, tag_rank
    )
    # id -> {phase: weight}, resolved from the annotations (empty when uniform);
    # a conflicting redeclaration of an id is itself a preflight failure.
    weight_map, weight_errors = agent_route.resolved_weights(
        enabled_entries, registry, tag_rank
    )
    return RoutingSetup(
        registry=registry,
        managed=bool(raw_enabled),
        enabled=enabled,
        weight_map=weight_map,
        reg_errors=reg_errors,
        enable_errors=annot_errors + resolve_errors + weight_errors,
    )


@dataclass(frozen=True)
class SessionSetup:
    """Everything the CLI flags + the declared routing files resolve to for one
    run: the phase maps, the resolved enable-list, the prompt templates that
    passed preflight, and the worker assignment."""

    template: str
    model_map: dict
    cmd_map: dict
    prompt_map: dict
    tier_map: dict
    prefer_map: dict
    prompt_templates: dict
    adjudicator_prompt_paths: tuple
    routing: RoutingSetup
    worker: dict


def resolve_session_setup(args, root):
    """Resolve the run, or refuse it. Returns (setup, None), or (None, code)
    when a map is malformed, a preflight check fails, or the worker assignment
    is not a legal one — the three refusals that used to be inline arms of
    `main`. Every refusal prints exactly what it printed before."""
    docs = root / "docs"
    template = (
        args.agent_cmd
        if args.agent_cmd is not None
        else os.environ.get("AGENT_CMD", "")
    )
    maps, code = _parse_session_maps(args)
    if code is not None:
        return None, code
    model_map, cmd_map, prompt_map, tier_map, prefer_map = maps
    routing = resolve_routing_setup(docs)
    failures, prompt_templates, prompt_paths = map_preflight(
        root,
        template,
        args,
        cmd_map,
        prompt_map,
        tier_map,
        prefer_map,
        routing.managed,
        routing.registry,
        routing.enabled,
        routing.reg_errors,
        routing.enable_errors,
    )
    if failures:
        print("agent_loop: preflight failed —", file=sys.stderr)
        for f in failures:
            print("  - " + f, file=sys.stderr)
        return None, EXIT_PREFLIGHT
    worker, err = build_worker_assignment(args, root)
    if err is not None:
        return None, err
    return (
        SessionSetup(
            template=template,
            model_map=model_map,
            cmd_map=cmd_map,
            prompt_map=prompt_map,
            tier_map=tier_map,
            prefer_map=prefer_map,
            prompt_templates=prompt_templates,
            adjudicator_prompt_paths=tuple(
                prompt_paths[key] for key in adjudicate_brief.BRIEF_PROMPTS.values()
            ),
            routing=routing,
            worker=worker,
        ),
        None,
    )


@dataclass(frozen=True)
class SessionPolicies:
    """The declared dials this run reads, resolved once through the one policy
    home (docs/process.toml, legacy one-word file as the SN-028 migration
    fallback). SN-029: the three-value gate-authority enum retired for an
    ORDINAL comparison — is the tier the spine is in process at still the
    human's to approve? `human_held` answers it once; `keep_nondependent` is
    the orthogonal dial the enum bundled. WI-437 (OI-25): `session_hold` is the
    derived label — WHO HOLDS this run."""

    human_held: bool
    keep_nondependent: bool
    session_hold: str
    push: str
    review: str
    guardrails: str
    blackout: str


def resolve_session_policies(root, docs):
    human_held = agent_common.human_holds(docs, agent_common.spine_stage_of(root))
    # Spelled as its own statement, not folded into the constructor call below:
    # the WI-437 / OI-25 one-name-one-meaning rule reads this module's SOURCE for
    # the exact `session_hold = <the two derived values>` form, so that the
    # derived hold can be checked to mean one thing across every module that
    # derives it (the rule also forbids the retired enum's name appearing here at
    # all, which is why this comment does not spell the test module either).
    session_hold = "human-held" if human_held else "loop-held"
    return SessionPolicies(
        human_held=human_held,
        keep_nondependent=agent_common.keep_nondependent(docs),
        session_hold=session_hold,
        push=declared_policy(docs, "push-policy", "human"),
        review=declared_policy(docs, "review-policy", "1"),
        guardrails=declared_policy(docs, "guardrails-policy", "off"),
        blackout=declared_policy(docs, "blackout", ""),
    )


def possible_session_models(args, model_map, routing):
    """Every model this run could actually launch. Under managed routing that
    is the ENABLED registry rows' models, not the env maps — compute the inert
    check against what will actually run, or the warning is spurious/silent in
    exactly the managed mode it matters for (repo-review 2026-07-21 L-20)."""
    models = {m for m in [args.model, *model_map.values()] if m}
    if routing.managed:
        models |= {
            (routing.registry[mid].model or mid)
            for mid in routing.enabled
            if mid in routing.registry
        }
    return models


def warn_on_inert_or_malformed_policies(policies, possible_models):
    """Surface a stale/typo'd or malformed declared policy BEFORE the run.

    A guardrails token naming a substring that matches none of the models this
    run could use guards nothing. A malformed blackout window or reviewer dial
    must not silently disable itself either — both are consent surfaces like
    agents-enabled (repo-review 2026-07-21 M-20). Behavior is unchanged for
    compat (blackout off / review-policy lenient-parse); the SILENCE was the
    defect."""
    if guardrails_inert(policies.guardrails, possible_models):
        print(
            "agent_loop: WARNING - guardrails-policy {!r} would guard none of "
            "the configured models ({}); the guard is inert — fix the token or "
            'the model map (process-options.md "Tier-conditional guardrails").'.format(
                policies.guardrails, ", ".join(sorted(possible_models)) or "none"
            ),
            file=sys.stderr,
        )
    if policies.blackout and parse_blackout(policies.blackout) is None:
        print(
            "agent_loop: WARNING - the blackout window {!r} (docs/process.toml "
            "[policies] blackout) is malformed (expected "
            "HH:MM-HH:MM); the blackout window is DISABLED this run.".format(
                policies.blackout
            ),
            file=sys.stderr,
        )
    if (policies.review or "").strip() not in ("0", "1", "2"):
        print(
            "agent_loop: WARNING - the reviewer dial {!r} (docs/process.toml "
            "[policies] review_rounds) is not 0|1|2; "
            "parsed leniently (unparseable -> 1, out-of-range clamped).".format(
                policies.review
            ),
            file=sys.stderr,
        )


def _dual_plan_entry(root, docs, args, setup, policies):
    """The dual-plan round is its own early path (WI-199): one round, then
    exit — never the resume loop. The trigger lives in the REGISTRY
    (PlanMode=dual), the flag only names the WI; a non-dual row is refused so
    the flag can't conscript an ordinary WI into the round."""
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
        setup.template,
        args.model,
        args.session_timeout or None,
        setup.prompt_map,
    )
    if outcome == "SELECTED":
        print("agent_loop: dual-plan {}: {}".format(wid, detail))
        return EXIT_DONE
    action = _plan_round.page_action(policies.human_held, policies.keep_nondependent)
    print(
        "agent_loop: dual-plan {} PAGED: {} (session-hold {} -> {})".format(
            wid, detail, policies.session_hold, action
        ),
        file=sys.stderr,
    )
    if action == "stop-needs-human":
        stop_banner(docs / "status.md", "NEEDS-HUMAN", detail)
        return EXIT_NEEDS_HUMAN
    # Every other action honors the pause-free invariant (WI-204, WI-209):
    # an attention-only outcome lands on EXIT_STALL, never a NEEDS-HUMAN
    # gate. The PAGE evidence is on disk under docs/plans/DP-*; relaunching
    # re-runs the round. (page_action's non-stop-needs-human strings are
    # intent labels.)
    stop_banner(
        docs / "status.md",
        "dual-plan round paged — attention (no human hold on this tier)",
        detail,
    )
    return EXIT_STALL


def _live_console(args, docs):
    """Console rendering (WI-125 scroll / WI-136 live line). --no-session-echo
    silences it; otherwise --live-status (or `[checks] live_status = true`)
    upgrades the scroll to one in-place line per workstream — but only when
    stdout is a TTY with VT enabled, so a pipe / CI log keeps the append-only
    scroll (never-breaking). Decided once: the TTY/VT facts don't change
    mid-run. `declared_policy` reads docs/process.toml first and falls back to
    the legacy docs/live-status for the SN-028 migration window."""
    live_status_on = (
        args.live_status
        or declared_policy(docs, "live-status", "false").lower() == "true"
    )
    return live_status_on and _stdout_is_tty() and _enable_windows_vt()


def _clamped_review_rounds(review_policy):
    """The reviewer dial as an int: unparseable -> 1, out-of-range clamped —
    the lenient parse the startup warning announces."""
    try:
        rp_int = int(review_policy)
    except ValueError:
        rp_int = 1
    return max(0, min(2, rp_int))


def _int_env(name, default, minimum=None):
    """An S8 knob read from the environment: a non-integer — or a value below
    the knob's floor — falls back to the built-in default rather than wedging
    the run (the S8-knob idiom)."""
    try:
        value = int(os.environ.get(name, default))
    except ValueError:
        return default
    if minimum is not None and value < minimum:
        return default
    return value


def build_routing_state(docs, rp_int, managed):
    """The S8 managed-routing / WI-068 critique / stall-guard cluster — one
    RoutingState holding what were ~24 mutable locals of `main` (WI-080 Slice
    C). All no-ops when the enable-list is absent, so the legacy path is
    byte-for-byte unchanged."""
    return RoutingState(
        rp_int,
        _int_env("AGENT_COOLDOWN_SECONDS", DEFAULT_COOLDOWN_SECONDS),
        load_critique_srs(docs) if managed else set(),
        _int_env("AGENT_CRITIQUE_MAX", 3, minimum=1),
        agent_route.load_constants(),
    )


def announce_critique_budget(managed, st):
    """One line when this run can schedule critique rounds at all."""
    if managed and st.critique_srs:
        print(
            "critique: {} Critique-verified SR(s) present -> a build touching one "
            "schedules a rubric-anchored CRITIQUE round (budget {} per scope)".format(
                len(st.critique_srs), st.critique_max
            )
        )


def run_loop(ctx):
    """Iterate until an iteration returns an exit code, or until the declared
    budget runs out — which is itself an exit with a banner, never a silent
    stop."""
    for i in range(1, ctx.args.max_iterations + 1):
        code = run_iteration(ctx, i)
        if code is not None:
            return code
    stop_banner(
        ctx.status_path,
        "iteration budget exhausted",
        "{} session(s) run and {} is still {} — raise "
        "--max-iterations deliberately if the run should continue.".format(
            ctx.args.max_iterations, ctx.lane / "run-state", ctx.run.state
        ),
    )
    return EXIT_BUDGET


# Implements: SR-154, LLR-045, SR-155, LLR-132
def main():
    _utf8_console()
    args = parse_args()
    root, code = _resolve_root(args)
    if code is not None:
        return code
    docs = root / "docs"

    # The session dials, resolved ONCE from the single declared home
    # (docs/stack.ini [agent-loop], IF-068 / WI-274 part B) so they need not be
    # duplicated across the three agent-resume launchers — precedence CLI flag >
    # AGENT_* env > declared file > built-in default. (The jobs dial retired
    # with the parallel dispatcher at concurrency-restructure Phase 5.)
    args.model, args.model_map = resolve_coordinator_dials(args, docs)

    # The drive mode's loop lives in the sibling dispatch.py — ordering only, no
    # new authority; every refusal stays where it already lives. It takes the
    # same per-checkout coordinator lock the explicit roles take below (the
    # worker subprocesses it spawns lock their own worktrees).
    if is_drive_launch(args):
        return _drive_entry(root, args)

    setup, code = resolve_session_setup(args, root)
    if code is not None:
        return code

    # The one coordination surface is docs/ (WI-210: the --track lane
    # redirection is retired; the repo-singular policy files live here too).
    lane = docs
    lane.mkdir(parents=True, exist_ok=True)
    status_path = lane / "status.md"

    policies = resolve_session_policies(root, docs)
    _, branch = git(root, "branch", "--show-current")
    warn_on_inert_or_malformed_policies(
        policies,
        possible_session_models(args, setup.model_map, setup.routing),
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
    code = _coordinator_lock(root)
    if code is not None:
        return code

    if args.interactive:
        return run_interactive(
            args,
            root,
            setup.model_map,
            setup.cmd_map,
            setup.template,
            policies.guardrails,
            warned_no_core,
        )

    if args.dual_plan:
        return _dual_plan_entry(root, docs, args, setup, policies)

    print_run_banner(
        root,
        branch,
        setup.worker,
        policies.session_hold,
        policies.push,
        policies.review,
        setup.routing.managed,
        setup.routing.enabled,
        setup.routing.registry,
        policies.guardrails,
        setup.template,
        setup.cmd_map,
        setup.prompt_map,
        docs,
    )

    iter_dir = lane / "iteration"
    reviews_dir = docs / "reviews" / setup.worker["train"]
    rp_int = _clamped_review_rounds(policies.review)
    st = build_routing_state(docs, rp_int, setup.routing.managed)
    announce_critique_budget(setup.routing.managed, st)

    resume_owed_round(root, setup, st, rp_int, iter_dir, reviews_dir)

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

    return run_loop(
        LoopContext(
            args=args,
            root=root,
            docs=docs,
            lane=lane,
            status_path=status_path,
            worker=setup.worker,
            managed=setup.routing.managed,
            registry=setup.routing.registry,
            enabled=setup.routing.enabled,
            template=setup.template,
            model_map=setup.model_map,
            cmd_map=setup.cmd_map,
            prompt_templates=setup.prompt_templates,
            adjudicator_prompt_paths=setup.adjudicator_prompt_paths,
            tier_map=setup.tier_map,
            prefer_map=setup.prefer_map,
            weight_map=setup.routing.weight_map,
            guardrails_policy=policies.guardrails,
            human_held=policies.human_held,
            keep_nondependent=policies.keep_nondependent,
            start_dirty=start_dirty,
            raw_dir=root / "out" / "run-logs",
            iter_dir=iter_dir,
            # The weighted-rotation DRAW reads the durable CROSS-train aggregate
            # (the primary worktree's committed docs/iteration) unioned with this
            # worker's local in-flight logs — NOT the train-local iter_dir alone,
            # whose freshly minted history would reset every train's draw to slot
            # 0 (WI-263, M-31). The primary-worktree path is stable for the run,
            # so resolve it once here; the dirs are re-globbed per draw as sibling
            # trains integrate.
            draw_iter_dirs=draw_iter_dirs(root, iter_dir),
            tag="{}-".format(setup.worker["train"]),
            use_live=_live_console(args, docs),
            # Worker review evidence is train-scoped and collision-safe
            # (LLR-061): two parallel workers' committed verdicts/scoreboards
            # must never collide at integration, so each train gets its own
            # reviews/<train>/ directory.
            reviews_dir=reviews_dir,
            scoreboard=reviews_dir / "scoreboard.txt",
            rp_int=rp_int,
            run=LoopRun(routing=st, warned_no_core=warned_no_core),
        )
    )


if __name__ == "__main__":
    sys.exit(main())
