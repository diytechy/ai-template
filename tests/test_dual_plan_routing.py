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


# --- Bug 2: _dp_session reduces a json/stream-json transcript to result text ---


def test_dp_session_reduces_stream_json_to_result_text(tmp_path, monkeypatch):
    transcript = (
        '{"type":"assistant","message":"thinking out loud"}\n'
        '{"type":"result","result":"P1 | the real plan text"}\n'
    )
    monkeypatch.setattr(al, "run_session", lambda *a, **k: (0, transcript, False))
    ok, output = al._dp_session("tmpl {prompt}", "m", "prompt", tmp_path, 10)
    assert ok is True
    assert output == "P1 | the real plan text"


def test_dp_session_passes_plain_text_through(tmp_path, monkeypatch):
    monkeypatch.setattr(
        al, "run_session", lambda *a, **k: (0, "P1 | plan\nP2 | plan\n", False)
    )
    ok, output = al._dp_session("tmpl {prompt}", "m", "prompt", tmp_path, 10)
    assert ok is True
    assert output == "P1 | plan\nP2 | plan\n"


def test_dp_session_failed_session_is_not_reduced(tmp_path, monkeypatch):
    # A failed session keeps its raw output (ok False); no result reduction.
    monkeypatch.setattr(al, "run_session", lambda *a, **k: (1, "boom", False))
    ok, output = al._dp_session("tmpl {prompt}", "m", "prompt", tmp_path, 10)
    assert ok is False
    assert output == "boom"
