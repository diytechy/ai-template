#!/usr/bin/env python3
"""Session brief construction and assignment-facing evidence.

This module decides what a worker, reviewer, critic, or adjudicator session is
told. Runtime scheduling and bookkeeping stay in ``agent_loop``; prompt text,
route-neutral brief assembly, guardrails payload selection, and the lane facts
those briefs render live here together.

Contracts: IF-260 — the interface seam this file declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-260: ``agent_loop`` imports the brief constructors, prompt-routing
helpers, and assignment evidence readers from this module and re-exports their
historical names. Inputs are repository paths, registry rows, routing values,
and prompt templates; outputs are prompt text or the small derived facts used
to build it. The module launches no session and commits nothing.
"""

import re
import shutil
import sys
from pathlib import Path

try:
    import agent_common
    import agent_route
    import agent_session
    import prompts
    import spine_carrier
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import agent_common
    import agent_route
    import agent_session
    import prompts
    import spine_carrier

from kitlib import decisions as kdecisions
from kitlib import done_when as kdone
from kitlib import provenance as kprovenance
from kitlib import verdict as kverdict

build_argv = agent_session.build_argv
WI_TOKEN_RE = agent_common.WI_TOKEN_RE
_clip = agent_common._clip
git = agent_common.git
trunk_name = agent_common.trunk_name
load_wi_registry = agent_common.load_wi_registry
_refs = agent_common._refs
train_evidence = agent_common.train_evidence

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
# BUILD, REVIEW-A, REVIEW-B, INTEGRATE}) are `kverdict.REVIEW_PHASES`, and this
# module deliberately keeps NO copy of them: IF-175 declares ONE definition of
# the verdict, and the span the merge slot demands is half of it, so a second
# tuple here is drift made representable rather than detected (LLR-182). A
# committing non-review session triggers a review round; those phases are it.

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
# round through the BUILD arm (a reviewer's own commit, a planner, an
# integrator, a critic writing its verdict). DESIGN-CHECK stays in the set
# because it is not a build for TIER/routing purposes, but a committing one
# arms the round through its own arm in `build_bookkeeping` — it did the
# rework, and a BUILD session that exists only to re-arm the round is waste.
NON_BUILD_PHASES = frozenset(kverdict.REVIEW_PHASES) | {
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


def assignment_block(root, wi_rows, wi, base, assigned):
    """The WI-580 batch block: EVERY row this lane was claimed with, each with
    its evidence state, or `""` for the ordinary one-row lane.

    The dispatcher admits a spine batch as ONE lane (`--wi 'A;B'`, §A4) and
    `current_assignment_wi` walks it a row per session — but the brief rendered
    the walked row alone, under an opening sentence that called it the whole
    scope. Measured 2026-09-02 on `wi-569-…`: the human saw `wi=WI-569;WI-575`
    in the launch banner and the session that took WI-569 never learned WI-575
    was on its lane.

    THE ONE-ROW LANE RENDERS NOTHING, which is what keeps this safe to add: the
    `- WI:`/`- SR-Refs:`/`- Branch:` lines already carry every fact this block
    would repeat, so only a batch can observe the difference.

    The state vocabulary is the walk's own, not a fourth opinion about
    doneness: `this session's focus` is whatever `current_assignment_wi`
    returned, and the rest split on the SAME two-part predicate that walk reads
    (`lane_completion`). A row that is `built` here is one the walk has already
    stepped past — trailer committed AND spec out of `active/<branch>/`. A row
    with only the trailer reads `started, not closed`, because that is a row
    the walk WILL come back to and telling its next session `built` is the
    silent-completion miss this block was measured against.

    Implements: SR-026, LLR-061
    """
    if len(assigned) < 2:
        return ""
    built, done = lane_completion(root, base)
    # `done` wins over `built` where a row is both — the trailer-only rows are
    # what is left, and a row in neither set was never touched.
    state = dict.fromkeys(built, "started, not closed") | dict.fromkeys(done, "built")
    return (
        "- The WHOLE assignment ({} rows claimed on this lane, one row per "
        "session — a sibling row is this lane's later work, not another "
        "lane's):\n".format(len(assigned))
        + "".join(
            "  - {} [{}] {} — SpecRef: {}\n".format(
                tok,
                "this session's focus" if tok == wi else state.get(tok, "not started"),
                _row_title(wi_rows, tok),
                (wi_rows.get(tok, {}).get("SpecRef") or "—").strip() or "—",
            )
            for tok in assigned
        )
    )


def _row_title(wi_rows, tok):
    """A WI's Title for a prompt block, with the placeholder both blocks show
    for a row the registry does not carry — an empty cell there would read as a
    row with no scope rather than as a row the reader cannot look up."""
    return (
        wi_rows.get(tok, {}).get("Title") or "(row missing from the registry)"
    ).strip()


def _predecessor_lines(wi_rows, row):
    """The hard-predecessor lines of a worker brief: one `  - <id> [Status]
    Title — Deliverable…` line per `Predecessors` token that names a live row
    (a `~` soft-edge prefix is stripped; an unknown id is skipped; a long
    Deliverable is clipped at 200 characters). Extracted from `worker_prompt`
    when the assignment block (WI-580) pushed it over the cognitive ceiling —
    outward, the census's own remedy, never a baseline bump.

    Implements: SR-026, LLR-061
    """
    preds = []
    for tok in re.split(r"[;,\s]+", (row.get("Predecessors") or "").strip()):
        tok = tok.lstrip("~")
        p = wi_rows.get(tok) if tok and WI_TOKEN_RE.match(tok) else None
        if p is None:
            continue
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
    return preds


def worker_prompt(root, wi_rows, wi, train, base, rework_text="", assigned=None):
    """The per-session worker prompt (LLR-061): the WI row + SpecRef +
    predecessor context + the current branch diff + any rework finding, slotted
    into WORKER_PROMPT (`train` is the session tag = the claim branch name).
    `{scripts}` resolves at this sole composition boundary so the meta-repo and
    a scaffold use their respective runtime script directories.
    Reads NOTHING from docs/status.md or docs/next-wi — the explicit
    assignment is the whole scope.

    `assigned` is the lane's WHOLE claim (WI-580); `wi` is the row this session
    walked to. Defaulting it to `[wi]` keeps every in-process caller that only
    knows one row rendering exactly what it rendered before.

    Implements: SR-026, LLR-061
    """
    import schedule

    held = next(
        (
            r
            for r in schedule.evaluate(schedule._load(root))
            if r["id"] == wi and r["disposition"] == "blocked"
        ),
        None,
    )
    if held:
        gates = "; ".join(
            "{} — {}".format(o["id"], o["title"]) for o in held["open_items"]
        )
        return "BLOCKED {}: {}. See docs/open-items.html; no worker assignment.".format(
            wi, gates
        )
    row = wi_rows.get(wi, {})

    preds = _predecessor_lines(wi_rows, row)
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
        scripts=scripts_dir(root),
        assignment_block=assignment_block(
            root, wi_rows, wi, base, list(assigned) if assigned else [wi]
        ),
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


def guardrails_core(root, model=""):
    """The always-on core to prepend to a quick-tier session's prompt, or None.
    Vendored verbatim as docs/guardrails/core.md; the BEGIN/END KIT CORE block is
    extracted when present, else the whole file. Absent -> None (the caller warns
    once and runs without it — guardrails accelerate, they are not a gate).

    A repo may vendor one payload per model substring beside it,
    `core.<substring>.md`, for a model that wants a different posture: the
    payload whose substring `model` contains replaces core.md, chosen by the
    policy's own matcher, the longest substring winning so a narrower payload
    beats a broader one. The substrings are the repo's file names, so the kit
    names no model.

    Implements: SR-223, LLR-280
    """
    gdir = root / "docs" / "guardrails"
    stems = sorted(
        (p.name[len("core.") : -len(".md")] for p in gdir.glob("core.?*.md")),
        key=lambda sub: (-len(sub), sub),
    )
    chosen = next((sub for sub in stems if guardrails_apply(sub, model)), None)
    name = "core.{}.md".format(chosen) if chosen else "core.md"
    try:
        text = (gdir / name).read_text(encoding="utf-8")
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

    WI-580 adds `{wis}` — the rows under review, id + title. The brief named no
    work item at all, so a round had to infer its scope from the diff before it
    could map a spec's Done-when items to coverage. Unlike the three C7 slots
    this one renders even with no worker (an attended round), because the
    honest fallback is a sentence saying the scope was not declared; leaving a
    literal `{wis}` in a brief that was actually SENT would be worse than
    either. An override file without the slot still renders unchanged —
    `str.replace` on an absent needle is a no-op.

    Implements: SR-154, LLR-045
    """
    base = prompt_templates.get(phase, _kit_prompt(prompts.REVIEWER))
    text = base.replace("{verdict}", str(verdict_path)).replace(
        "{wis}", reviewed_rows_block(worker)
    )
    if root is not None:
        text = text.replace("{process_doc}", process_doc_path(root))
        text = text.replace("{trunk}", trunk_name(root, worker))
        text = text.replace("{scripts}", scripts_dir(root))
        text += done_when_flag_block(root, worker)
    return text


def done_when_flag_block(root, worker):
    """The brief's DONE-WHEN CHANGED SINCE CLAIM block, or "" when the lane
    left every assigned row's Done-when as claimed (ticks and evidence aside).

    S13's reviewer half: a round maps each Done-when item to its covering test,
    so a builder that rewords an item has moved the checklist its own reviewer
    reads. The claim-time text is the spec under `active/<train>/` at the lane's
    base; the current one is this tree's (`lane_spec_text`).

    Implements: SR-154, SR-156, LLR-262
    """
    lines = []
    for wi in (worker or {}).get("assigned") or []:
        claimed = kdone.claimed_text(root, worker["base"], worker["train"], wi)
        current = lane_spec_text(root, wi)
        found = kdone.changes(claimed, current) if claimed and current else []
        if found:
            lines += ["  " + wi + ":"] + ["    " + ln for ln in kdone.describe(found)]
    if not lines:
        return ""
    return (
        "\n\nDONE-WHEN CHANGED SINCE CLAIM — this lane's own diff changed the "
        "checklist you map coverage against. Judge the work against the "
        "claim-time items, and raise each change as a finding unless it only "
        "clarifies:\n" + "\n".join(lines)
    )


def reviewed_rows_block(worker):
    """The `{wis}` block: the claimed rows a review round covers, `  - <id> —
    <title>` a line, in assignment order.

    A round reviews the LANE, so every assigned row is in scope — not just the
    row whatever session happened to trigger the round. With no worker (an
    attended round, or a caller that has no assignment to name) the block says
    so in one line rather than rendering an empty bullet list, which would read
    as "this diff covers nothing"."""
    assigned = [w for w in (worker or {}).get("assigned") or [] if w]
    if not assigned:
        return "  - (not declared for this round — infer the scope from the diff)"
    rows = (worker or {}).get("rows") or {}
    return "\n".join("  - {} — {}".format(w, _row_title(rows, w)) for w in assigned)


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


def decision_record_note(root, worker):
    """The delegated-decisions note for this lane's session, or "" when the
    repository's `[attestation] decision_recording` dial is `off` or there is no
    lane. Appended at the one fork every build and adjudication session takes,
    so both altitudes that close a lane are told where the record the merge
    slot asks for belongs, and a reviewer, which closes nothing, is not."""
    if not worker:
        return ""
    mode = agent_common.decision_recording(Path(root) / "docs")
    return kdecisions.session_note(mode, worker["train"])


# What a held adjudication row tells the human, appended to the stop banner.
# The exit code is the DURABLE half: `dispatch._lane_close` turns
# EXIT_NEEDS_HUMAN into a `handback.close_partial` — an immutable per-close
# report and a move to the TERMINAL partial/, which `schedule._disposition`
# reads as `partial` (never ready) — so an unattended run can never re-pick the
# row until a successor is minted. A print alone would be gone with the terminal
# buffer.
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
    base = resume_reconcile + body + loop_provenance_note()
    if not guardrails_apply(guardrails_policy, model):
        return base, False
    core = guardrails_core(root, model)
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


def loop_provenance_note():
    """The standing instruction a session under the loop marker owes every
    commit, or "" for a session nobody marked (an interactive one).

    A session is a process the loop started, so every commit it makes is the
    loop's and must carry the `Loop-Session` trailer (SR-209): the commit-msg
    hook refuses one without it where hooks are enabled, and the merge slot
    re-checks every commit of the lane whether or not they are. Nothing in git
    can add a trailer to `git commit -m` by itself, so the session is told the
    exact line - value included - and where it goes: inside the final trailer
    block, beside `WI:`, since git reads trailers from the last paragraph only
    and a blank line between them would hide the `WI:` trailer."""
    session = kprovenance.loop_session()
    if session is None:
        return ""
    return (
        "\n\nLOOP PROVENANCE: this session runs under the unattended loop. End "
        "EVERY commit message with the trailer line `{}`, in the same final "
        "trailer block as any `WI:` trailer (no blank line between them). A "
        "commit without it is refused where the loop's commit floor runs, and "
        "the lane will not merge.".format(kprovenance.format_loop_trailer(session))
    )


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


def lane_spec_text(root, wi):
    """`wi`'s spec as THIS LANE'S OWN TREE holds it, or None when unreadable.

    Searched across `agent_common.SPEC_HOMES` because a session that ran its
    close ritual has already moved the spec out of `active/`; WHICH copy wins
    when the tree carries both is `agent_common.authoritative_spec`'s to say,
    shared with the merge slot so the two cannot read different copies."""
    found = {}
    for home in agent_common.SPEC_HOMES:
        for hit in (Path(root) / home).rglob(wi + "-*.md"):
            found[hit.relative_to(Path(root)).as_posix()] = hit
    chosen = agent_common.authoritative_spec(found)
    if chosen is None:
        return None
    try:
        return found[chosen].read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def claimed_on_branch(root):
    """The assigned rows this lane has NOT closed: the WI ids whose spec is
    still in `active/<current branch>/` on the branch's committed tree.

    Only the branch resolution is the loop's; the tree read itself is
    `integrate.claimed_ids_on_branch`, beside the `finished_branches` that asks
    the same tree the same question — two answers to "has this row left
    `active/`?" is exactly how the walk and the integrator came apart. Scoped to
    `<branch>` because a lane worktree inherits trunk's whole `active/`, other
    lanes' claims included. An empty answer (a detached HEAD, git silent) leaves
    the caller's behaviour exactly as it was before this read existed.
    """
    import integrate  # a sibling reader; deferred so a non-worker run pays nothing

    code, out = git(root, "symbolic-ref", "--quiet", "--short", "HEAD")
    branch = out.strip() if code == 0 else ""
    return (branch and integrate.claimed_ids_on_branch(root, branch)) or set()


def lane_completion(root, base):
    """`(built, done)` for a lane, the ONE completion predicate its two readers
    share: `built` is the rows carrying a committed `WI:` trailer, `done` the
    rows a session is finished with — trailer AND spec gone from
    `active/<branch>/`.

    Both facts in one read because both readers need the distinction and
    neither may invent its own (WI-580 review A): the walk
    (`current_assignment_wi`) and the brief (`assignment_block`) had each
    derived doneness separately, and the brief's half-predicate labelled a row
    `built` on its trailer alone — so a batch with a trailer committed but the
    close ritual unrun told the next session its still-active row was complete,
    the exact miss `current_assignment_wi`'s two-part test exists to prevent."""
    built, _blocked = train_evidence(root, base)
    return built, built - claimed_on_branch(root)


__all__ = (
    "_kit_prompt",
    "_PROMPT_CACHE",
    "DEFAULT_PHASE_TIER",
    "DEFAULT_COOLDOWN_SECONDS",
    "NON_BUILD_PHASES",
    "assignment_block",
    "_row_title",
    "_predecessor_lines",
    "worker_prompt",
    "KIT_CORE_RE",
    "guardrails_apply",
    "guardrails_core",
    "guardrails_inert",
    "prompt_source",
    "row_routing",
    "adjudicating",
    "phase_tier",
    "reviewer_prompt",
    "done_when_flag_block",
    "reviewed_rows_block",
    "process_doc_path",
    "scripts_dir",
    "decision_record_note",
    "ADJUDICATION_HOLD_NOTE",
    "session_model",
    "session_template",
    "compose_session_prompt",
    "loop_provenance_note",
    "RUBRIC_PATH_RE",
    "load_critique_srs",
    "build_scope_wis",
    "build_scope_srs",
    "critique_control",
    "critique_brief",
    "critique_prompt",
    "launcher_exe",
    "fresh_verdict_path",
    "lane_spec_text",
    "claimed_on_branch",
    "lane_completion",
)
