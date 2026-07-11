"""The model-routing selector + fixed escalation policy (agent_route.py, WI-059,
process-options.md "Unattended operation" -> routing/escalation). Unit-level:
the pure functions are exercised directly; the loop integration lives in
test_agent_loop.py."""

from conftest import SCRIPTS, load_script, run_py

route = load_script("agent_route")

REGISTRY_CSV = """Id,Provider,Model,Version,Tier,CmdTemplate,Notes
ANTHROPIC-OPUS-4.8,ANTHROPIC,opus,4.8,strong,claude -p {prompt} --model {model},frontier
OPENAI-GPT-5.2,OPENAI,gpt-5.2,5.2,strong,codex exec {prompt},
GOOGLE-GEMINI-3-PRO,GOOGLE,gemini-3-pro,3-pro,medium,gemini -p {prompt},
ANTHROPIC-HAIKU-4,ANTHROPIC,haiku,4,weak,claude -p {prompt} --model {model},
AGENTS-EXAMPLE-000,EXAMPLE,x,0,weak,x {prompt},placeholder ignored
"""


def _registry(tmp_path):
    p = tmp_path / "agents.csv"
    p.write_text(REGISTRY_CSV, encoding="utf-8")
    return route.load_registry(p)


def test_load_registry_parses_columns_not_the_id(tmp_path):
    reg, errors = _registry(tmp_path)
    assert errors == []
    m = reg["ANTHROPIC-OPUS-4.8"]
    # The id is a join key; the fields are the machine truth (never parsed out).
    assert m.provider == "ANTHROPIC" and m.model == "opus" and m.version == "4.8"
    assert m.tier == "strong"
    assert "{model}" in m.cmd_template and "{prompt}" in m.cmd_template
    # The -000 placeholder ships inert like every other registry.
    assert "AGENTS-EXAMPLE-000" not in reg


def test_registry_rejects_bad_id_charset_and_tier(tmp_path):
    p = tmp_path / "agents.csv"
    p.write_text(
        "Id,Provider,Model,Version,Tier,CmdTemplate,Notes\n"
        "anthropic-opus-4.8,ANTHROPIC,opus,4.8,strong,c {prompt},\n"  # lowercase id
        "OPENAI-GPT-5.2,OPENAI,gpt,5.2,superb,codex {prompt},\n",  # bad tier
        encoding="utf-8",
    )
    reg, errors = route.load_registry(p)
    assert reg == {}  # both rows rejected
    joined = " ".join(errors)
    assert "not [A-Z0-9]" in joined  # id charset
    assert "tier" in joined  # vocabulary


def test_duplicate_id_is_a_finding(tmp_path):
    p = tmp_path / "agents.csv"
    p.write_text(
        "Id,Provider,Model,Version,Tier,CmdTemplate,Notes\n"
        "ANTHROPIC-OPUS-4.8,ANTHROPIC,opus,4.8,strong,c {prompt},\n"
        "ANTHROPIC-OPUS-4.8,ANTHROPIC,opus,4.8,strong,c {prompt},\n",
        encoding="utf-8",
    )
    _, errors = route.load_registry(p)
    assert any("duplicate id" in e for e in errors)


def test_absent_registry_and_enable_list_are_empty(tmp_path):
    reg, errors = route.load_registry(tmp_path / "nope.csv")
    assert reg == {} and errors == []
    assert route.load_enabled(tmp_path / "nope-enabled") == []


def test_enable_list_is_ordered_and_skips_comments(tmp_path):
    p = tmp_path / "agents-enabled"
    p.write_text(
        "# preference order, one id per line\nOPENAI-GPT-5.2\n\nANTHROPIC-OPUS-4.8\n",
        encoding="utf-8",
    )
    assert route.load_enabled(p) == ["OPENAI-GPT-5.2", "ANTHROPIC-OPUS-4.8"]


def test_select_honors_preference_order_and_tier(tmp_path):
    reg, _ = _registry(tmp_path)
    enabled = ["OPENAI-GPT-5.2", "ANTHROPIC-OPUS-4.8", "GOOGLE-GEMINI-3-PRO"]
    chosen, reason = route.select(enabled, reg, "strong")
    assert chosen == "OPENAI-GPT-5.2"  # first enabled strong-tier id
    assert "OPENAI-GPT-5.2" in reason


def test_select_prefers_a_different_provider_but_degrades(tmp_path):
    reg, _ = _registry(tmp_path)
    # Two strong models, both same provider as the implementer -> degraded, legal.
    enabled = ["ANTHROPIC-OPUS-4.8"]
    chosen, reason = route.select(
        enabled, reg, "strong", exclude_providers=["ANTHROPIC"], prefer_different=True
    )
    assert chosen == "ANTHROPIC-OPUS-4.8"
    assert "DEGRADED" in reason
    # With a different-provider option available, it is preferred.
    enabled2 = ["ANTHROPIC-OPUS-4.8", "OPENAI-GPT-5.2"]
    chosen2, reason2 = route.select(
        enabled2, reg, "strong", exclude_providers=["ANTHROPIC"], prefer_different=True
    )
    assert chosen2 == "OPENAI-GPT-5.2" and "DEGRADED" not in reason2


def test_select_tiers_up_never_down(tmp_path):
    reg, _ = _registry(tmp_path)
    # Only a strong model enabled; asking for medium bumps UP to strong.
    chosen, reason = route.select(["ANTHROPIC-OPUS-4.8"], reg, "medium")
    assert chosen == "ANTHROPIC-OPUS-4.8"
    assert "bumped up" in reason
    # Only a weak model enabled; asking for medium must NOT drop to weak.
    chosen2, reason2 = route.select(["ANTHROPIC-HAIKU-4"], reg, "medium")
    assert chosen2 is None
    assert "weaker" in reason2


def test_cooldown_excludes_then_reinstates(tmp_path):
    reg, _ = _registry(tmp_path)
    enabled = ["OPENAI-GPT-5.2", "ANTHROPIC-OPUS-4.8"]
    cooldowns = {}
    route.cool(cooldowns, "OPENAI-GPT-5.2", now=100.0, seconds=60)
    # While cooling, the next strong preference is chosen instead.
    chosen, _ = route.select(enabled, reg, "strong", now=100.0, cooldowns=cooldowns)
    assert chosen == "ANTHROPIC-OPUS-4.8"
    # After the cooldown lapses, it is available again (preference order restored).
    chosen2, _ = route.select(enabled, reg, "strong", now=161.0, cooldowns=cooldowns)
    assert chosen2 == "OPENAI-GPT-5.2"


def test_select_none_when_all_cooled(tmp_path):
    reg, _ = _registry(tmp_path)
    cooldowns = {}
    route.cool(cooldowns, "ANTHROPIC-OPUS-4.8", now=0.0, seconds=300)
    chosen, reason = route.select(
        ["ANTHROPIC-OPUS-4.8"], reg, "strong", now=10.0, cooldowns=cooldowns
    )
    assert chosen is None and "cooled down" in reason


# --- the fixed escalation policy ------------------------------------------- #
def test_escalate_continue_and_win_stay():
    c = route.DEFAULT_CONSTANTS
    # A clean approve with a wide margin: win-stay names next round's primary.
    rounds = [
        {"verdict": "APPROVE", "tier": "strong", "margin": 3, "primary": "OPENAI"}
    ]
    d = route.escalate(rounds, c)
    assert d["action"] == "continue" and d["next_primary"] == "OPENAI"
    # A margin below the bar does not move the primary.
    rounds2 = [
        {"verdict": "APPROVE", "tier": "strong", "margin": 1, "primary": "OPENAI"}
    ]
    assert route.escalate(rounds2, c)["next_primary"] is None


def test_escalate_swap_then_tier_up_then_page():
    c = route.DEFAULT_CONSTANTS

    def cr(tier="medium"):
        return {"verdict": "CHANGES-REQUESTED", "tier": tier, "margin": 0}

    # Two consecutive failed gates -> swap the implementer provider.
    d1 = route.escalate([cr(), cr()], c, swapped=False, at_top_tier=False)
    assert d1["action"] == "swap-implementer"
    # Swap already applied and still failing -> raise the tier (only now).
    d2 = route.escalate([cr(), cr()], c, swapped=True, at_top_tier=False)
    assert d2["action"] == "tier-up"
    # Swap + tier-up exhausted at the top tier -> page the human.
    d3 = route.escalate([cr(), cr()], c, swapped=True, at_top_tier=True)
    assert d3["action"] == "page-human"


def test_escalate_pages_on_top_tier_shared_failure():
    c = route.DEFAULT_CONSTANTS
    rounds = [
        {"verdict": "CHANGES-REQUESTED", "tier": "strong", "margin": 0},
        {"verdict": "CHANGES-REQUESTED", "tier": "strong", "margin": 0},
    ]
    d = route.escalate(rounds, c)
    assert d["action"] == "page-human" and "shared-failure" in d["reason"]


def test_escalate_pages_on_tripwire_and_double_contradiction():
    c = route.DEFAULT_CONSTANTS
    assert (
        route.escalate([{"verdict": "APPROVE", "tier": "weak", "tripwire": True}], c)[
            "action"
        ]
        == "page-human"
    )
    two = [
        {"verdict": "CHANGES-REQUESTED", "tier": "weak", "contradiction": True},
        {"verdict": "CHANGES-REQUESTED", "tier": "weak", "contradiction": True},
    ]
    assert route.escalate(two, c)["action"] == "page-human"


def test_constants_overridable_from_env():
    c = route.load_constants(
        {"AGENT_ROUTE_SWAP_AFTER": "3", "AGENT_ROUTE_MARGIN": "bad"}
    )
    assert c["swap_after"] == 3  # overridden
    assert c["margin"] == route.DEFAULT_CONSTANTS["margin"]  # bad value ignored


def test_failure_action_keyed_to_gate_policy():
    assert route.failure_action("attended")["run_state"] == "NEEDS-HUMAN"
    sr = route.failure_action("single-ratify")
    assert sr["run_state"] == "RUNNING" and sr["keep_nondependent"] and sr["pause_wi"]
    au = route.failure_action("autonomous")
    assert au["design_check"] and au["run_state"] == "RUNNING" and au["pause_wi"]
    # Absent/unknown defaults to attended (the safe stop).
    assert route.failure_action("")["mode"] == "attended"


def test_cli_list_select_and_status(tmp_path):
    # The Provides-CLI seam (IF-044): --list the pool, --select the routed id.
    reg = tmp_path / "agents.csv"
    reg.write_text(REGISTRY_CSV, encoding="utf-8")
    en = tmp_path / "agents-enabled"
    en.write_text("OPENAI-GPT-5.2\nANTHROPIC-OPUS-4.8\n", encoding="utf-8")
    listed = run_py(
        [SCRIPTS / "agent_route.py", "--registry", reg, "--enabled", en, "--list"],
        cwd=tmp_path,
    )
    assert listed.returncode == 0, listed.stdout + listed.stderr
    assert "OPENAI-GPT-5.2" in listed.stdout and "strong" in listed.stdout
    sel = run_py(
        [
            SCRIPTS / "agent_route.py",
            "--registry",
            reg,
            "--enabled",
            en,
            "--select",
            "--tier",
            "strong",
        ],
        cwd=tmp_path,
    )
    assert sel.returncode == 0 and "selected" in sel.stdout
    status = run_py(
        [SCRIPTS / "agent_route.py", "--registry", reg, "--enabled", en], cwd=tmp_path
    )
    assert "routing on" in status.stdout
