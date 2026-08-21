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
consents by filling the slot, declaring how far a human ratifies
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

Contracts: IF-015, IF-068, IF-099, IF-109 — the interface seams this module declares
(process.md §8; rows of record in docs/requirements/interfaces.toml). IF-068
(WI-274 part B) is the coordinator-dial read: main() resolves model/model-map
from docs/stack.ini [agent-loop] (via agent_common.read_agent_loop_config)
with precedence CLI flag > AGENT_* env > declared file > built-in default.
The WI-218 split re-homed IF-041 (agent-CLI invocation) to agent_session.py
and IF-037 (declared-surface reads) to agent_common.py; the split-out layers
provide back over IF-064..IF-067.
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
    import agent_common
    import agent_route
    import agent_session
    import plan_runner
    import prompts
    import score_reviews
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import adjudicate_brief
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
    # those is a judgement whose cost of being wrong is a wrong ratification.
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


def reviewer_prompt(prompt_templates, phase, verdict_path):
    """The redacted reviewer prompt for a review phase: the per-phase prompt-map
    template (a FILE the operator wired) if present, else the embedded
    REVIEWER_PROMPT — with {verdict} resolved to the path the reviewer must
    write. Never carries the implementer's self-assessment (redaction by
    construction).

    Implements: SR-154, LLR-045
    """
    base = prompt_templates.get(phase, _kit_prompt(prompts.REVIEWER))
    return base.replace("{verdict}", str(verdict_path))


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
        resets the stall; an error before work increments the error run.

        Implements: SR-172, LLR-175
        """
        self.stall = 0 if committed else self.stall + 1
        self.errors = self.errors + 1 if errored else 0

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
    Returns (failures, prompt_templates)."""
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
    return failures, prompt_templates


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
        base = (args.base or "").strip() or head_sha(root)
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


class LoopContext:
    """Everything one iteration reads, built once at loop start; the
    per-iteration behavior lives in run_iteration (WI-080 Slice E). A plain
    attribute bag — no logic — so a moved body reads ctx.<name> where it
    used to read the loop-local."""


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
    warned_no_core = ctx.warned_no_core
    reviews_dir = ctx.reviews_dir
    st = ctx.st
    is_review = False
    is_critique = False
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
        route_id, reason = agent_route.select(
            enabled,
            registry,
            tier,
            now,
            st.cooldowns,
            exclude,
            prefer_different,
            preferred_ids,
            agent_route.phase_weights(ctx.weight_map, phase),
            phase_draw_ordinal(ctx.draw_iter_dirs, phase),
        )
        # Log the routing decision BEFORE launch (the no-silent-swap rule).
        print("route [{}]: {}".format(phase or "—", reason))
        if route_id is None:
            # Every enabled model at the preferred tier-or-stronger is cooling
            # down or none is enabled: page rather than drop to a weaker tier.
            # (A worker never writes run-state — its exit code is the page;
            # the stop banner + exit code carry the outcome.)
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
            verdict_path = fresh_verdict_path(
                reviews_dir, "{}-{}-{}.md".format(session, phase, reviewed_sha[:7])
            )
            body = reviewer_prompt(prompt_templates, phase, verdict_path)
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
    human_held = getattr(ctx, "human_held", True)
    keep_going = getattr(ctx, "keep_nondependent", False)
    scoreboard = ctx.scoreboard
    rp_int = ctx.rp_int
    st = ctx.st
    phase = plan["phase"]
    is_review = plan["is_review"]
    is_critique = plan["is_critique"]
    verdict_path = plan["verdict_path"]
    route_id = plan["route_id"]
    route_family = plan["route_family"]
    # The ADJUDICATE validation arm, unconditional (see the function): an
    # adjudication row gets its brief on BOTH routing paths, so it owes its
    # verdict on both — unlike everything below, which is managed-only.
    adjudication_bookkeeping(plan, worker, st, managed, route_id, now)
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
        v = read_verdict(verdict_path, route_family)
        if v is not None:
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
                # verdicts on the exact reviewed head (LLR-140).
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
            # (LLR-061) — never the lane's tracked docs/rework-wi pointer,
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
            st.apply_decision(decision["action"], merged, decision.get("next_primary"))
            if decision["action"] == "page-human":
                fa = agent_route.failure_action(human_held, keep_going)
                print("route/failure ({}): {}".format(fa["mode"], fa["note"]))
                # SN-029: the stop is keyed on the MODE the ordinal produced
                # (), not on the retired enum word .
                if fa["mode"] == "human-held" and not fa["keep_nondependent"]:
                    # A worker has no lane files — its exit code and the
                    # stop banner carry the page.
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
        v = read_verdict(verdict_path, route_family)
        if v is not None:
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
                # Budget exhausted -> the S8 page-the-human semantics, keyed to
                # the session hold (same failure_action the review round uses).
                # The critic gates iteration; the human owns final acceptance
                # via Attest at gate closure.
                fa = agent_route.failure_action(human_held, keep_going)
                print(
                    "critique/budget ({}): {} CHANGES-REQUESTED round(s) >= "
                    "{} -> page-human: {}".format(
                        fa["mode"], pre_rounds + 1, st.critique_limit, fa["note"]
                    )
                )
                if (
                    fa["mode"] == "human-held" and not fa["keep_nondependent"]
                ) or st.critique_exhaustion == "block":
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
            # is ONE review scope (WI-183, LLR-140): a worker schedules the
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
    ladder (WI-210 — the loop is the claimed-assignment worker engine; the
    serial resume driver and its docs/pause boundary are retired: pause stops
    NEW CLAIMS at the coordinator (§5.6) while an in-flight worker
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
    blackout_line = declared_policy(lane, "blackout", "")
    wake = blackout_wake(blackout_line, datetime.datetime.utcnow())
    if wake:
        resume_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=wake)
        # WI-261: a prominent banner + a periodic countdown heartbeat (vs the old
        # one-liner) so a walk-away launch reads as deliberately WAITING, not
        # hung. Same wait semantics — total sleep is exactly `wake` seconds.
        blackout_wait(wake, blackout_line, resume_at, emit=print, sleep=time.sleep)
    # (The WI-209 serial dual-plan quiet-park guard retired with the serial
    # driver, WI-210: a dual row runs through --dual-plan, so the
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
        # (The §7 continuation re-check retired with session grouping, WI-383 /
        # §A6.1. It re-asked, once per successor, whether the classifier still
        # permitted a MULTI-WI grouping — a guard that only ever had work to do
        # because the dispatcher packed independent WIs into one session. With
        # packing deleted, the only multi-WI assignment left is the spine batch
        # the dispatcher admits deliberately (§A4), whose constituents are
        # homogeneous by construction: the guard's sole non-refusing case. A
        # check that can only ever say yes is not a safeguard.)
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
        # SN-026: WHICH template, and what it rendered to. The pair is what
        # makes a session's instruction auditable after the fact — the source
        # is a file `prompts/CATALOG.md` lists by digest, the result is this
        # row's own fingerprint, and neither requires keeping rendered prompts
        # on disk. An override path shows HERE rather than only in the launch
        # flags, so a substituted prompt is visible in the telemetry.
        "prompt-template": prompt_source(ctx.prompt_templates, phase),
        "prompt-sha": agent_common.prompt_fingerprint(prompt),
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
    # states are judged from committed evidence, below, and the coordinator
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


# Implements: SR-154, LLR-045, SR-155, LLR-132
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

    # The session dials, resolved ONCE from the single declared home
    # (docs/stack.ini [agent-loop], IF-068 / WI-274 part B) so they need not be
    # duplicated across the three agent-resume launchers — precedence CLI flag >
    # AGENT_* env > declared file > built-in default. (The jobs dial retired
    # with the parallel dispatcher at concurrency-restructure Phase 5.)
    args.model, args.model_map = resolve_coordinator_dials(args, docs)

    # A plain launch (no role) is the DRIVE mode (WI-374): the serial
    # claim->build->integrate front end, restored after the parallel
    # dispatcher's Phase 5 deletion took the scheduling front half with it.
    # The loop itself lives in the sibling dispatch.py — ordering only, no new
    # authority; every refusal stays where it already lives. It takes the
    # same per-checkout coordinator lock the explicit roles take below (the
    # worker subprocesses it spawns lock their own worktrees).
    if not (args.wi or args.train or args.interactive or args.dual_plan):
        return _drive_entry(root, args)
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
    registry, reg_errors = agent_route.load_registry(docs / "agents.toml")
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
    tag_rank = agent_route.load_tag_rank(docs / "agents.toml")
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

    # SN-028: the four dials now read through the one policy home
    # (docs/process.toml, legacy one-word file as the migration fallback). The
    # four LOCALS stay — `print_run_banner` takes them positionally — so this
    # is a reader swap, not a signature change. SN-029: the three-value
    # gate-authority enum retires for an ORDINAL comparison — is the tier the
    # spine is in process at still the human's to ratify? `human_holds` makes
    # it once; `keep_nondependent` is the orthogonal dial the enum bundled.
    # WI-437 (OI-25): the derived label is `session_hold` — WHO HOLDS this run.
    human_held = agent_common.human_holds(docs, agent_common.spine_stage_of(root))
    keep_going = agent_common.keep_nondependent(docs)
    session_hold = "human-held" if human_held else "loop-held"
    push_policy = declared_policy(docs, "push-policy", "human")
    review_policy = declared_policy(docs, "review-policy", "1")
    _, branch = git(root, "branch", "--show-current")

    guardrails_policy = declared_policy(docs, "guardrails-policy", "off")
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
    blackout_line = declared_policy(docs, "blackout", "")
    if blackout_line and parse_blackout(blackout_line) is None:
        print(
            "agent_loop: WARNING - the blackout window {!r} (docs/process.toml "
            "[policies] blackout) is malformed (expected "
            "HH:MM-HH:MM); the blackout window is DISABLED this run.".format(
                blackout_line
            ),
            file=sys.stderr,
        )
    if (review_policy or "").strip() not in ("0", "1", "2"):
        print(
            "agent_loop: WARNING - the reviewer dial {!r} (docs/process.toml "
            "[policies] review_rounds) is not 0|1|2; "
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
    code = _coordinator_lock(root)
    if code is not None:
        return code

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
        action = _plan_round.page_action(human_held, keep_going)
        print(
            "agent_loop: dual-plan {} PAGED: {} (session-hold {} -> {})".format(
                wid, detail, session_hold, action
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

    print_run_banner(
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
    )

    raw_dir = root / "out" / "run-logs"
    iter_dir = lane / "iteration"
    tag = "{}-".format(worker["train"])
    # Console rendering (WI-125 scroll / WI-136 live line). --no-session-echo
    # silences it; otherwise --live-status (or `[checks] live_status = true`)
    # upgrades the scroll to one in-place line per workstream — but only when
    # stdout is a TTY with VT enabled, so a pipe / CI log keeps the append-only
    # scroll (never-breaking). Decided once: the TTY/VT facts don't change
    # mid-run. `declared_policy` reads docs/process.toml first and falls back to
    # the legacy docs/live-status for the SN-028 migration window.
    live_status_on = (
        args.live_status
        or declared_policy(docs, "live-status", "false").lower() == "true"
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
    # Worker review evidence is train-scoped and collision-safe (LLR-061): two
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
    ctx.session_hold = session_hold
    ctx.human_held = human_held
    ctx.keep_nondependent = keep_going
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
