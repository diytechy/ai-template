#!/usr/bin/env python3
"""The dual-plan round RUNNER: the coordinator fan-in over the WI-194..WI-198
modules, extracted VERBATIM from agent_loop.py (WI-218 slice C — a file split,
not a rewrite; behaviors and WI history unchanged).

A queued WI whose registry row declares `PlanMode=dual` is run as a dual-plan
round — two planner sessions, the coverage pre-pass, one cross-critique +
revision, the position-swapped arbiter pair — never as a direct BUILD (the
worker path refuses a dual row, fail-closed). Sessions launch through the
split-out headless layer (agent_session.build_argv/run_session), so each
inherits the S8 per-session limits; routing (agent_route.planner_pair /
planner_fallback, with the registry's tag-rank override) is used when the
enable-list opts it in, else one template drives every hat as the recorded
routing-off degraded mode. The protocol, its caps, and every safeguard live in
plan_round/plan_briefs/plan_coverage_step/plan_artifacts — this runner only
drives them through the session machinery and writes the artifacts.
agent_loop re-exports `wi_plan_mode`/`PLAN_MODE_DUAL`/`run_dual_plan_round`
(and the `_dp_*` helpers) so its public surface is unchanged.

Stdlib only, Python 3.11+, Windows/POSIX.

Contracts: IF-066 — the interface seam this module declares (process.md §8; row of record in docs/requirements/interfaces.toml).

Contract IF-066: agent_loop imports two names from this module and re-exports
    them, so its own public surface is unchanged. `wi_plan_mode(row)` returns
    the work item's declared PlanMode as a lowered token — only `dual` fires a
    round, and an absent column, an empty cell or an unknown word are ordinary
    BUILD dispatch, never an error. `run_dual_plan_round(root, wi, row,
    template, model, timeout, prompt_map)` drives the whole round — two planner
    sessions, the coverage pre-pass, one cross-critique and revision, the
    position-swapped arbiter pair — through the headless session layer and
    returns `(outcome, detail)` where outcome is `SELECTED` (verdict recorded,
    the chosen plan's rows filed as queued work items) or `PAGE` (the reason,
    for the caller to map onto its approval level). Every refusal on the way in
    — no resolvable goal brief, no rubric, an unreadable hat template, an
    unusable roster, nothing routable — returns PAGE with its reason rather
    than falling through to a direct build. Routing-on
    resolves planner pairs tag-rank-aware with one runtime-nonresponse
    fallback; routing-off drives every hat from the one template, the recorded
    degraded mode. Every session launched inherits the declared per-session
    limits; nothing here writes the spine.
"""

import os
import re
import sys
from pathlib import Path

# Sibling scripts (the WI-218 split): the headless session layer. The guard
# covers an in-process import (a test) whose sys.path doesn't yet carry
# scripts/ — the same sanctioned-sibling-import idiom agent_loop uses.
try:
    import agent_common
    import agent_session as agent_session
    from agent_session import build_argv, parse_json_result, run_session
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import agent_common
    import agent_session as agent_session
    from agent_session import build_argv, parse_json_result, run_session
# --- the dual-plan decomposition round (WI-199; DP-001 selected plan P6) -------
# The coordinator fan-in over the WI-194..WI-198 modules: a queued WI whose
# registry row declares `PlanMode=dual` is run as a dual-plan round — two
# planner sessions, the coverage pre-pass, one cross-critique + revision, the
# position-swapped arbiter pair — never as a direct BUILD (the worker path
# refuses a dual row, fail-closed). Sessions launch through the existing
# headless invocation path (build_argv/run_session), so each inherits the S8
# per-session limits; routing (agent_route.planner_pair/planner_fallback) is
# used when the enable-list opts it in, else one template drives every hat as
# the recorded routing-off degraded mode. Frontier AUTO-dispatch under --jobs
# is wired (WI-209): schedule.classify derives the single-WI-traincar class
# from the PlanMode signal itself and the dispatcher runs the round as a
# serialized disposition (dual_plan_disposition) instead of a BUILD worker.
# Residual honesty: sessions run in the repo cwd like every S8 hat (redaction
# rides the brief's allowlist construction, plan_briefs); the manual
# protocol's empty-cwd isolation is stronger.
PLAN_MODE_COLUMN = "PlanMode"


PLAN_MODE_DUAL = "dual"


DUALPLAN_BUDGET_ENV = "AGENT_DUALPLAN_BUDGET"


PLAN_RUBRIC = "docs/rubrics/plan-decomposition.md"


_CRITIC_VERDICT_RE = re.compile(r"VERDICT:\s*(APPROVE|CHANGES-REQUESTED)")


_ARBITER_VERDICT_RE = re.compile(r"VERDICT:\s*SELECT\s+([AB])\b(?:\s+ports=(\d+))?")


_EMPTY_SLOT = "(empty - first round)"


def wi_plan_mode(row):
    """The WI row's declared plan mode: `dual` fires the round; anything else
    (absent column, empty cell, unknown token) is ordinary BUILD dispatch."""
    return (row.get(PLAN_MODE_COLUMN) or "").strip().lower()


def _dp_routes(root, tier):
    """The two planner hat routes as `[(label, model, template, env, note)]`.
    With routing opted in (docs/agents-enabled + agents.toml), the pair comes
    from agent_route.planner_pair (different families where the pool allows,
    else the recorded degraded reason); with routing off, both hats ride the
    ambient template/model — the recorded routing-off degraded mode. Returns
    (routes, registry, note); registry is None when routing is off."""
    import agent_route

    enabled = agent_route.load_enabled(root / "docs" / "agents-enabled")
    registry, reg_errors = agent_route.load_registry(root / "docs" / "agents.toml")
    if not enabled:
        return None, None, "routing-off: one template drives every hat (degraded)"
    if not registry or reg_errors:
        # The enable-list is the consent surface: with it PRESENT, a missing/
        # headerless/all-malformed agents.toml must PAGE loudly (the posture
        # map_preflight already takes for BUILD workers), never silently drop
        # both hats onto the ambient template — and a partially-malformed
        # registry must not silently shrink the pool either (repo-review
        # 2026-07-21 M-30). The non-None registry return is what makes the
        # caller PAGE (routing was opted in).
        return (
            None,
            registry,
            "routing: agents.toml unreadable/malformed with agents-enabled "
            "present: {}".format("; ".join(reg_errors) or "no parseable rows"),
        )
    # resolve_enabled returns (ids, errors) — unpack it, or planner_pair iterates
    # the whole tuple as the pool and crashes (TypeError: unhashable list) before
    # any session launches. This routing-ON dual-plan path was never exercised
    # (the kit's own DP-001 ran routing-off), so the defect stayed latent until it
    # surfaced downstream in gilbert. Unresolvable ids PAGE loudly, never a silent
    # skip (the main dispatcher path unpacks correctly; only these helpers did not).
    # The registry's declared tag-rank override rides along (as main() does) so
    # version-less token resolution is identical in every engine path.
    tag_rank = agent_route.load_tag_rank(root / "docs" / "agents.toml")
    pool, resolve_errors = agent_route.resolve_enabled(enabled, registry, tag_rank)
    if resolve_errors:
        return (
            None,
            registry,
            "routing: unresolvable agents-enabled id(s): {}".format(
                "; ".join(resolve_errors)
            ),
        )
    pair = agent_route.planner_pair(pool, registry, tier)
    if pair.sessions[0] is None:
        return None, registry, "routing: no routable model ({})".format(pair.detail)
    routes = []
    for label, sess in zip(("A", "B"), pair.sessions):
        m = registry[sess.model_id]
        routes.append((label, m.model, m.cmd_template, m.env, sess.model_id))
    return routes, registry, "{} ({})".format(pair.reason, pair.detail)


def _dp_session(
    template, model, prompt, root, timeout, env_cell="", *, attribution=None
):
    """One round session through the existing headless path. Returns
    (ok, output). A pair row's Env cell is merged over the ambient env
    (agent_route.parse_env), matching the loop's session launch."""
    env = None
    if env_cell:
        import agent_route

        env = dict(os.environ)
        env.update(agent_route.parse_env(env_cell))
    argv, stdin_input = build_argv(template, model, prompt)
    metrics = dict(attribution or {})
    metrics.setdefault("role", "PLAN")
    metrics.setdefault("source-event", "dual-plan")
    metrics["requested-model"] = model
    code, output, timed_out = agent_common.invoke_and_persist(
        root,
        argv,
        timeout,
        metrics=metrics,
        runner=run_session,
        env=env,
        stdin_input=stdin_input,
    )
    ok = code == 0 and not timed_out
    # A --output-format json/stream-json template (what the real agents.toml rows
    # use) captures the whole event transcript, but the round's consumers need the
    # SESSION RESULT TEXT: plan_coverage's line-oriented parser finds zero rows in
    # a one-line JSON transcript, and the {{PLAN}}/{{CRITIQUE}} brief slots must
    # carry artifacts, not conversations (a raw transcript leaks thinking + model
    # names into the redacted briefs). Reduce to the result event's text when one
    # parses; a plain-text template yields no JSON and passes through unchanged.
    # Latent kit defect surfaced downstream in gilbert (the kit's own DP-001 ran a
    # plain-text template, so it never fired).
    if ok:
        data = parse_json_result(output)
        if data.get("type") == "result":
            output = str(data.get("result") or output)
    return ok, output


def _repair_critique(coverage_fails, plan_name):
    """The mechanical-repair CRITIQUE payload for ONE plan: ONLY the coverage
    FAIL lines that name this plan's own file (each line is
    `plan_coverage: FAIL - <planfile>: ...`). The RIVAL plan's fail lines must
    NEVER enter this hat's context — anchoring a planner on the other plan's
    coverage biases the build toward convergence, defeating two-planner
    independence at the cheapest gaming point (repo-review 2026-07-21 L-28 /
    WI-265). When this plan owns no fail line the payload is a generic
    repair-your-own-clauses instruction — NEVER a fallback to the full
    `coverage_fails`, which carries the rival's lines. The full coverage report
    (per-plan sets + the pairwise diff) rides only the CRITIQUE/ARBITER briefs,
    whose templates alone declare a {{COVERAGE_REPORT}} slot."""
    own_fails = "\n".join(ln for ln in coverage_fails.splitlines() if plan_name in ln)
    body = own_fails or (
        "(no coverage FAIL line names your plan) — repair only your own failing "
        "clauses; do not add coverage the pre-pass did not flag."
    )
    return "MECHANICAL REPAIR ONLY - the coverage pre-pass found:\n" + body


def _hat_slots(root, row, planner_tmpl):
    """The `{{HAT_QUESTIONS}}` fill for this decomposition (SN-036 / OI-19), or
    `{}` when the planner template does not declare the slot.

    THE GUARD IS WHY THIS IS CONDITIONAL: `plan_briefs.assemble` rejects a slot
    key the template does not declare, so filling it unconditionally would stop
    every operator `--prompt-map` override authored before the slot existed
    from composing at all. Raises `HatsError` on a roster or declared scope
    reference that is unusable — the caller pages on it."""
    import plan_briefs

    if not plan_briefs.declares_slot(planner_tmpl, plan_briefs.HAT_QUESTIONS_SLOT):
        # A legacy template composes fine WITHOUT hats — but if a roster
        # EXISTS, the operator declared perspectives this round will not face,
        # and silence here would be the miss SN-036 exists to surface (review
        # finding). Warn-only: breaking every pre-slot --prompt-map override
        # would be the worse failure.
        if (root / "docs" / "requirements" / "hats.toml").exists():
            print(
                "plan_runner: WARN - a hats roster is declared but the planner "
                "template carries no {{HAT_QUESTIONS}} slot — this "
                "decomposition faces NO declared perspective; add the slot to "
                "the override or drop the override",
                file=sys.stderr,
            )
        return {}
    return plan_briefs.hat_surface_for_work_item(root, row)


def _dp_attribution(root, wi, round_dir, step, registry, route_id=""):
    """Attribute a plan role to its existing round and selected roster row."""
    kind, plan = step["step"], step.get("plan")
    route = (registry or {}).get(route_id)
    return {
        "wi": wi,
        "attempt-id": round_dir.relative_to(root).as_posix(),
        "source-event": "{}:{}:{}".format(
            round_dir.name, kind, plan or step.get("run", "")
        ),
        "role": kind,
        "provider": route.family if route else "",
        "tier": route.tier if route else "",
        "roster-row": route_id if route else "",
    }


def run_dual_plan_round(root, wi, row, template, model, timeout, prompt_map=None):
    """Run one dual-plan decomposition round for `wi` unattended and return
    `(outcome, detail)` — outcome `SELECTED` (verdict recorded, the selected
    plan's rows filed as queued WIs) or `PAGE` (the round's page reason;
    the caller maps it onto the declared approval level's failure semantics via
    plan_round.page_action). The protocol, its caps, and every safeguard live
    in the WI-194..WI-198 modules — this runner only drives them through the
    existing session machinery and writes the artifacts."""
    import plan_artifacts
    import plan_briefs
    import plan_coverage_step
    import plan_round

    prompt_map = prompt_map or {}

    spec_ref = (row.get("SpecRef") or "").split("#")[0].strip()
    goal_path = root / spec_ref if spec_ref else None
    if goal_path is None or not goal_path.exists():
        return "PAGE", "dual-plan WI {} has no resolvable SpecRef goal brief".format(wi)
    rubric_path = root / PLAN_RUBRIC
    if not rubric_path.exists():
        return "PAGE", "no plan rubric on file ({})".format(PLAN_RUBRIC)
    goal_text = goal_path.read_text(encoding="utf-8", errors="replace")
    rubric_text = rubric_path.read_text(encoding="utf-8", errors="replace")

    def hat_template(hat):
        return plan_briefs.strip_dispatcher_block(
            plan_briefs.load_template(hat, override=prompt_map.get(hat))
        )

    try:
        surface = plan_briefs.build_surface(root)
        planner_tmpl = hat_template(plan_briefs.HAT_PLANNER)
        critic_tmpl = hat_template(plan_briefs.HAT_CRITIC)
        arbiter_tmpl = hat_template(plan_briefs.HAT_ARBITER)
        hat_slots = _hat_slots(root, row, planner_tmpl)
    except OSError as exc:
        return "PAGE", "dual-plan hat template unreadable: {}".format(exc)
    except (plan_briefs.HatsError, SystemExit) as exc:
        # Malformed declared context PAGES with the reader's reason. An absent
        # roster opts out before the optional parent carriers are read.
        return "PAGE", "the planning context is unusable: {}".format(exc)

    routes, _registry, route_note = _dp_routes(root, "strong")
    if routes is None and _registry is not None:
        return "PAGE", route_note  # routing opted in but nothing routable
    if routes is None:
        routes = [
            ("A", model, template, "", "ambient"),
            ("B", model, template, "", "ambient"),
        ]
    route_of = {r[0]: r for r in routes}
    # Cross-critique: each plan is judged by the OTHER hat's route (cross-family
    # exactly when the pair is). The arbiter rides the ambient template/model —
    # a shared-family arbiter is the recorded degraded case (position-swap x2 +
    # anonymized labels are the mitigations, enforced below).
    critic_route_of = {"A": route_of["B"], "B": route_of["A"]}

    budget = plan_round.DEFAULT_ROUND_BUDGET
    try:
        budget = int(os.environ.get(DUALPLAN_BUDGET_ENV, "") or budget)
    except ValueError:
        pass
    slug = wi.lower()
    round_dir = plan_artifacts.allocate_round_dir(root, slug)
    plan_artifacts.write_stage(round_dir, "goal.md", goal_text)
    state = plan_round.new_round(slug, budget=budget)

    plan_text = {}  # true key -> current text
    plan_path = {}  # true key -> current artifact path
    critique_text = {}
    coverage_report = ""  # the clean report (the critic/arbiter brief payload)
    coverage_fails = ""  # the raw FAIL lines (the mechanical-repair payload)
    fell_back = False
    arbiter_notes = []

    def dispatch(step):
        nonlocal coverage_report, coverage_fails, fell_back
        nonlocal routes, route_of, critic_route_of
        kind, plan = step["step"], step.get("plan")

        if kind == plan_round.STEP_PLAN or kind in (
            plan_round.STEP_REPAIR,
            plan_round.STEP_REVISE,
        ):
            own = plan_text.get(plan, _EMPTY_SLOT)
            if kind == plan_round.STEP_PLAN:
                crit = _EMPTY_SLOT
            elif kind == plan_round.STEP_REPAIR:
                # ONLY this plan's own FAIL lines (the line names the plan
                # file); the rival's failures are never this hat's business,
                # and an empty own-fail set must NOT fall back to the full
                # coverage_fails — that leaked the rival's lines (L-28 / WI-265).
                crit = _repair_critique(coverage_fails, plan_path[plan].name)
            else:
                crit = critique_text.get(plan, "")
            prompt = plan_briefs.assemble(
                plan_briefs.HAT_PLANNER,
                dict(
                    hat_slots,
                    GOAL_BRIEF=goal_text,
                    SR_SURFACE=surface["SR_SURFACE"],
                    IF_REGISTRY=surface["IF_REGISTRY"],
                    OWN_PLAN=own if kind != plan_round.STEP_PLAN else _EMPTY_SLOT,
                    CRITIQUE=crit,
                ),
                planner_tmpl,
            )
            _label, m, tmpl, env_cell, note = route_of[plan]
            ok, output = _dp_session(
                tmpl,
                m,
                prompt,
                root,
                timeout,
                env_cell,
                attribution=_dp_attribution(root, wi, round_dir, step, _registry, note),
            )
            if not ok:
                if _registry is not None and not fell_back:
                    # One runtime-nonresponse fallback (WI-196), then page.
                    import agent_route

                    failed = type("S", (), {"family": ""})()
                    for sess_id, mm in _registry.items():
                        if mm.model == m:
                            failed.family = mm.family
                            break
                    # resolve_enabled returns (ids, errors) — unpack (the same
                    # latent tuple bug fixed in _dp_routes); the tag-rank
                    # override rides along like every other resolution site.
                    pool, _pool_errors = agent_route.resolve_enabled(
                        agent_route.load_enabled(root / "docs" / "agents-enabled"),
                        _registry,
                        agent_route.load_tag_rank(root / "docs" / "agents.toml"),
                    )
                    pair = agent_route.planner_fallback(
                        failed, pool, _registry, "strong"
                    )
                    if pair.sessions[0] is not None:
                        fell_back = True
                        routes = [
                            (
                                lbl,
                                _registry[s.model_id].model,
                                _registry[s.model_id].cmd_template,
                                _registry[s.model_id].env,
                                s.model_id,
                            )
                            for lbl, s in zip(("A", "B"), pair.sessions)
                        ]
                        route_of.update({r[0]: r for r in routes})
                        critic_route_of.update({"A": route_of["B"], "B": route_of["A"]})
                        arbiter_notes.append(
                            "runtime fallback: {} ({})".format(pair.reason, pair.detail)
                        )
                        return dispatch(step)  # relaunch this hat once, rerouted
                return None, "session failed at {} {}".format(kind, plan or "")
            suffix = {"PLAN": "", "REPAIR": "-repair", "REVISE": "-rev"}[kind]
            path = plan_artifacts.write_stage(
                round_dir, "plan-{}{}.md".format(plan, suffix), output
            )
            plan_text[plan], plan_path[plan] = output, path
            return {"ok": True}, None
        if kind == plan_round.STEP_COVERAGE:
            stage = step["stage"]
            result = plan_coverage_step.run_coverage(
                goal_path,
                [plan_path["A"], plan_path["B"]],
                root,
                round_dir / "coverage-{}.md".format(stage),
                {plan_path["A"].name: "A", plan_path["B"].name: "B"}.get,
            )
            coverage_report = result["report"]
            # FAIL lines only: the checker's full stdout also prints both
            # plans' covered/uncovered sets and the pairwise "only A / only B"
            # diff — handing that to a planner inside the "mechanical repair"
            # prompt leaks the rival plan's coverage at the cheapest gaming
            # point (repo-review 2026-07-21 L-28; independence is the design).
            raw_out = result.get("stdout") or result["report"] or ""
            coverage_fails = "\n".join(
                ln
                for ln in raw_out.splitlines()
                if ln.startswith("plan_coverage: FAIL")
            )
            kwargs = plan_coverage_step.to_record_kwargs(result)
            kwargs["stage"] = stage
            return kwargs, None
        if kind == plan_round.STEP_CRITIQUE:
            prompt = plan_briefs.assemble(
                plan_briefs.HAT_CRITIC,
                {
                    "GOAL_BRIEF": goal_text,
                    "SR_SURFACE": surface["SR_SURFACE"],
                    "IF_REGISTRY": surface["IF_REGISTRY"],
                    "RUBRIC": rubric_text,
                    "COVERAGE_REPORT": coverage_report,
                    "PLAN": plan_text[plan],
                },
                critic_tmpl,
            )
            _label, m, tmpl, env_cell, note = critic_route_of[plan]
            ok, output = _dp_session(
                tmpl,
                m,
                prompt,
                root,
                timeout,
                env_cell,
                attribution=_dp_attribution(root, wi, round_dir, step, _registry, note),
            )
            if not ok:
                return None, "session failed at CRITIQUE {}".format(plan)
            mm = _CRITIC_VERDICT_RE.search(output)
            if not mm:
                return None, "unparseable critique verdict for plan {}".format(plan)
            critique_text[plan] = output
            plan_artifacts.write_stage(
                round_dir, "critique-of-{}.md".format(plan), output
            )
            return {"verdict": mm.group(1)}, None
        if kind == plan_round.STEP_ARBITER:
            run = step["run"]
            # Position swap x2: run 1 labels the plans as-is, run 2 swaps —
            # the labels carry no provenance either way (anonymized by
            # construction: the arbiter sees only "Plan A"/"Plan B").
            label_to_true = {"A": "A", "B": "B"} if run == "1" else {"A": "B", "B": "A"}
            prompt = plan_briefs.assemble(
                plan_briefs.HAT_ARBITER,
                {
                    "OWNER_PROMPT": (row.get("Title") or wi).strip(),
                    "GOAL_BRIEF": goal_text,
                    "RUBRIC": rubric_text,
                    "COVERAGE_REPORT": coverage_report,
                    "PLAN_A": plan_text[label_to_true["A"]],
                    "PLAN_B": plan_text[label_to_true["B"]],
                },
                arbiter_tmpl,
            )
            ok, output = _dp_session(
                template,
                model,
                prompt,
                root,
                timeout,
                attribution=_dp_attribution(root, wi, round_dir, step, _registry),
            )
            if not ok:
                return None, "session failed at ARBITER run {}".format(run)
            mm = _ARBITER_VERDICT_RE.search(output)
            if not mm:
                return None, "unparseable arbiter verdict (run {})".format(run)
            plan_artifacts.write_stage(
                round_dir, "verdict-run{}.md".format(run), output
            )
            true_key = label_to_true[mm.group(1)]
            arbiter_notes.append(
                "run {}: labels A={}/B={} -> SELECT {} = plan {}".format(
                    run,
                    label_to_true["A"],
                    label_to_true["B"],
                    mm.group(1),
                    true_key,
                )
            )
            return {
                "selection": true_key,
                "ports": int(mm.group(2) or 0),
            }, None
        return None, "unknown step {!r}".format(kind)

    while True:
        steps = plan_round.ready_steps(state)
        if not steps:
            break
        step = steps[0]
        result, err = dispatch(step)
        if err:
            state["page_reason"] = err
            break
        disp = plan_round.record(
            state,
            step["step"],
            plan=step.get("plan"),
            stage=result.pop("stage", step.get("stage")),
            run=step.get("run"),
            **result,
        )
        if disp != plan_round.DISP_CONTINUE:
            break

    if state["selected"]:
        winner = state["selected"]
        rel_plan = plan_path[winner].relative_to(root).as_posix()
        try:
            mapping = plan_artifacts.file_selected_wis(
                root,
                plan_text[winner],
                rel_plan,
                (row.get("Workstream") or "unattended").strip() or "unattended",
                wi,
            )
        except ValueError as exc:
            # The filer fails closed on damaged plan tables (L-29); a PAGE is
            # the round's honest outcome, never an uncaught crash.
            return "PAGE", "selected plan not fileable: {}".format(exc)
        verdict = (
            "# {} verdict - dual-plan round for {} (unattended)\n\n"
            "VERDICT: SELECT plan {} ports={} (both position-swapped runs "
            "agree)\n\n- route: {}\n- {}\n- filed: {}\n"
            "- budget: {}/{} sessions\n".format(
                round_dir.name,
                wi,
                winner,
                state["ports"] or 0,
                route_note,
                "\n- ".join(arbiter_notes),
                ", ".join("{} -> {}".format(k, v) for k, v in sorted(mapping.items()))
                or "(no rows)",
                state["spent"],
                state["budget"],
            )
        )
        plan_artifacts.write_stage(round_dir, "verdict.md", verdict)
        plan_artifacts.append_log_summary(
            root,
            "## dual-plan round {} ({}): SELECT plan {}, ports={}\n\n"
            "Artifacts: {}/. Filed: {}. Route: {}. Acceptance follows the "
            "declared approval level in docs/process.toml (the "
            "recorded-verdict rules).".format(
                round_dir.name,
                wi,
                winner,
                state["ports"] or 0,
                round_dir.relative_to(root).as_posix(),
                ", ".join(sorted(mapping.values())) or "(none)",
                route_note,
            ),
        )
        return "SELECTED", "round {}: SELECT plan {} -> {}".format(
            round_dir.name, winner, ", ".join(sorted(mapping.values())) or "-"
        )

    reason = state["page_reason"] or "round ended without a selection"
    plan_artifacts.write_stage(
        round_dir,
        "verdict.md",
        "# {} - PAGE\n\n{}\n\nroute: {}\n{}\n".format(
            round_dir.name,
            reason,
            route_note,
            "\n".join(arbiter_notes),
        ),
    )
    return "PAGE", reason
