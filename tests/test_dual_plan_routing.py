"""Regression tests for the routing-ON dual-plan integration path (WI-215).

Two latent kit defects a downstream (gilbert) hit the first time it actually ran
the routing-ON round with real `--output-format stream-json` templates:

  1. `_dp_routes` and the mid-round planner fallback passed `resolve_enabled`'s
     `(ids, errors)` TUPLE straight into `planner_pair`/`planner_fallback`, which
     iterated it as the pool and crashed (TypeError: unhashable list) *before any
     session launched* — so the routing-ON dual-plan path had never worked.
  2. `_dp_session` returned the RAW json/stream-json event transcript, not the
     session result text, so the round's line-oriented consumers (plan_coverage,
     the {{PLAN}}/{{CRITIQUE}} briefs) parsed garbage and leaked thinking.

The kit's own DP-001 ran a plain-text, routing-off template, so neither fired in
the kit's tests — this file closes that coverage gap.
"""

from conftest import load_script

al = load_script("agent_loop")
# The dual-plan runner lives in plan_runner.py (WI-218 slice C); _dp_session
# resolves run_session in ITS namespace, so the monkeypatch targets pr, not al.
pr = load_script("plan_runner")
pb = load_script("plan_briefs")

# Two strong rows in different families so planner_pair can route a real pair.
REGISTRY_CSV = (
    "Id,Provider,Model,Version,Tier,CmdTemplate,Notes\n"
    "A-STRONG,ANTHROPIC,model-a,1,strong,run {model} {prompt},anthropic strong\n"
    "B-STRONG,OPENAI,model-b,1,strong,run {model} {prompt},openai strong\n"
)


def _routing_repo(tmp_path, enabled_ids):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "agents.csv").write_text(REGISTRY_CSV, encoding="utf-8")
    (docs / "agents-enabled").write_text(
        "\n".join(enabled_ids) + "\n", encoding="utf-8"
    )
    return tmp_path


# --- Bug 1: resolve_enabled tuple unpacking in the dual-plan routing path -----


def test_dp_routes_resolves_a_valid_pool_without_crashing(tmp_path):
    # THE regression: before the fix, resolve_enabled's (ids, errors) tuple was
    # handed to planner_pair, which iterated it and raised TypeError right here.
    root = _routing_repo(tmp_path, ["A-STRONG", "B-STRONG"])
    routes, registry, note = al._dp_routes(root, "strong")
    assert routes is not None, note
    assert registry is not None
    assert {label for label, *_ in routes} == {"A", "B"}


def test_dp_routes_pages_on_unresolvable_id(tmp_path):
    # An unresolvable enable-list id fails loudly (routes None + a naming note),
    # never a crash and never a silent skip.
    root = _routing_repo(tmp_path, ["A-STRONG", "GHOST-ID"])
    routes, registry, note = al._dp_routes(root, "strong")
    assert routes is None
    assert "unresolvable" in note and "GHOST-ID" in note


def test_dp_routes_off_when_no_enable_list(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "agents.csv").write_text(REGISTRY_CSV, encoding="utf-8")
    # No docs/agents-enabled -> routing off (degraded), not a crash.
    routes, registry, note = al._dp_routes(tmp_path, "strong")
    assert routes is None and registry is None and "routing-off" in note


def test_dp_routes_pages_when_enable_list_present_but_registry_broken(tmp_path):
    # Repo-review 2026-07-21 M-30: the enable-list is the consent surface —
    # with it PRESENT, a headerless/missing agents.csv must PAGE (the BUILD
    # workers' preflight posture), never silently drop both hats onto the
    # ambient template. The non-None registry return is the PAGE trigger.
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "agents-enabled").write_text("A-STRONG\n", encoding="utf-8")
    (docs / "agents.csv").write_text("not,a,registry\nheader\n", encoding="utf-8")
    routes, registry, note = al._dp_routes(tmp_path, "strong")
    assert routes is None
    assert registry is not None  # the caller PAGEs on this shape
    assert "agents.csv unreadable/malformed" in note
    # Missing file entirely: same loud outcome.
    (docs / "agents.csv").unlink()
    routes2, registry2, note2 = al._dp_routes(tmp_path, "strong")
    assert routes2 is None and registry2 is not None
    assert "agents.csv unreadable/malformed" in note2


# --- Bug 2: _dp_session reduces a json/stream-json transcript to result text ---


def test_dp_session_reduces_stream_json_to_result_text(tmp_path, monkeypatch):
    transcript = (
        '{"type":"assistant","message":"thinking out loud"}\n'
        '{"type":"result","result":"P1 | the real plan text"}\n'
    )
    monkeypatch.setattr(pr, "run_session", lambda *a, **k: (0, transcript, False))
    ok, output = pr._dp_session("tmpl {prompt}", "m", "prompt", tmp_path, 10)
    assert ok is True
    assert output == "P1 | the real plan text"


def test_dp_session_passes_plain_text_through(tmp_path, monkeypatch):
    monkeypatch.setattr(
        pr, "run_session", lambda *a, **k: (0, "P1 | plan\nP2 | plan\n", False)
    )
    ok, output = pr._dp_session("tmpl {prompt}", "m", "prompt", tmp_path, 10)
    assert ok is True
    assert output == "P1 | plan\nP2 | plan\n"


def test_dp_session_failed_session_is_not_reduced(tmp_path, monkeypatch):
    # A failed session keeps its raw output (ok False); no result reduction.
    monkeypatch.setattr(pr, "run_session", lambda *a, **k: (1, "boom", False))
    ok, output = pr._dp_session("tmpl {prompt}", "m", "prompt", tmp_path, 10)
    assert ok is False
    assert output == "boom"


# --- review-17c M4: the registry's tag-rank override reaches dual-plan routing --


def test_dp_routes_honors_registry_tag_rank_override(tmp_path):
    # A version-less enable token must resolve under the registry's own
    # `# tag-rank:` override — the same rule main() applies — so a dual-plan
    # round routes the same concrete row as every ordinary session. Before the
    # fix, _dp_routes called resolve_enabled without the tag rank and resolved
    # A-GA here (the DEFAULT maturity order) while the main loop resolved
    # A-BETA.
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "agents.csv").write_text(
        "Id,Provider,Model,Version,Tier,CmdTemplate,Notes\n"
        "# tag-rank: beta>ga\n"
        "A-GA,ANTHROPIC,model-a,ga,strong,run {model} {prompt},ga row\n"
        "A-BETA,ANTHROPIC,model-a,beta,strong,run {model} {prompt},beta row\n"
        "B-STRONG,OPENAI,model-b,1,strong,run {model} {prompt},openai strong\n",
        encoding="utf-8",
    )
    (docs / "agents-enabled").write_text(
        "ANTHROPIC-MODEL-A\nB-STRONG\n", encoding="utf-8"
    )
    routes, _registry, note = al._dp_routes(tmp_path, "strong")
    assert routes is not None, note
    ids = {r[4] for r in routes}
    assert "A-BETA" in ids and "A-GA" not in ids


# --- L-28 / WI-265: the mechanical-repair prompt never carries the rival's -----
# coverage. `coverage_fails` holds BOTH plans' `plan_coverage: FAIL - <file>:`
# lines; the repair critique for a plan must be filtered to that plan's OWN file
# lines. When a plan owns no fail line, the payload must NOT fall back to the
# full report (which contains the rival's lines) — the pre-change
# `own_fails or coverage_fails` fallback was that residual leak.

# Only plan-B fails; plan-A owns no FAIL line.
_COVERAGE_FAILS_B_ONLY = (
    "plan_coverage: FAIL - plan-B.md: clause C9 cited but not declared in the goal\n"
    "plan_coverage: FAIL - plan-B.md: Q2 cites undeclared interface IF-999"
)


def test_repair_critique_for_a_omits_rivals_fail_lines():
    # THE regression: A owns no fail line, so its repair critique must carry a
    # generic own-clauses instruction and NONE of plan-B's coverage. Against the
    # old `own_fails or coverage_fails` fallback, B's lines leaked in verbatim.
    crit = pr._repair_critique(_COVERAGE_FAILS_B_ONLY, "plan-A.md")
    assert "plan-B.md" not in crit
    assert "C9" not in crit and "IF-999" not in crit
    assert "MECHANICAL REPAIR ONLY" in crit  # still a valid repair payload


def test_repair_critique_keeps_only_the_owning_plans_lines():
    # With both plans failing, each hat sees ONLY its own file's lines.
    both = (
        "plan_coverage: FAIL - plan-A.md: C1 cited but not delivered\n"
        + _COVERAGE_FAILS_B_ONLY
    )
    crit_a = pr._repair_critique(both, "plan-A.md")
    assert "plan-A.md" in crit_a and "C1" in crit_a
    assert "plan-B.md" not in crit_a and "C9" not in crit_a


def test_repair_prompt_for_a_contains_no_plan_b_content():
    # End-to-end through the real planner template: the assembled A repair
    # prompt (CRITIQUE slot = the filtered payload) contains no plan-B lines,
    # and the planner template declares no COVERAGE_REPORT slot at all.
    crit = pr._repair_critique(_COVERAGE_FAILS_B_ONLY, "plan-A.md")
    planner_tmpl = pb.strip_dispatcher_block(pb.load_template(pb.HAT_PLANNER))
    prompt = pb.assemble(
        pb.HAT_PLANNER,
        {
            "GOAL_BRIEF": "C1: do the thing.",
            "SR_SURFACE": "- SR-001 — one",
            "IF_REGISTRY": "| IF-ID |\n|---|",
            "OWN_PLAN": "| P1 | ... |",
            "CRITIQUE": crit,
        },
        planner_tmpl,
    )
    assert "plan-B.md" not in prompt
    assert "C9" not in prompt and "IF-999" not in prompt


def test_full_coverage_report_reaches_only_critic_and_arbiter_hats():
    # The full report (per-plan sets + the pairwise "only plan-B.md: ..." diff)
    # is a legitimate CRITIQUE/ARBITER input, but the planner template must not
    # even offer a slot for it — so a repair prompt can never carry it (L-28).
    planner_slots = pb._placeholders(pb.load_template(pb.HAT_PLANNER))
    critic_slots = pb._placeholders(pb.load_template(pb.HAT_CRITIC))
    arbiter_slots = pb._placeholders(pb.load_template(pb.HAT_ARBITER))
    assert "COVERAGE_REPORT" not in planner_slots
    assert "COVERAGE_REPORT" in critic_slots
    assert "COVERAGE_REPORT" in arbiter_slots
