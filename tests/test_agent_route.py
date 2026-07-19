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
    # REGISTRY_CSV uses the LEGACY `Provider` header (no Family/Env) — proving a
    # legacy registry reads Provider as Family, byte-identical selection behavior.
    reg, errors = _registry(tmp_path)
    assert errors == []
    m = reg["ANTHROPIC-OPUS-4.8"]
    # The id is a join key; the fields are the machine truth (never parsed out).
    assert m.family == "ANTHROPIC" and m.model == "opus" and m.version == "4.8"
    assert m.env == ""  # no Env column -> ambient environment (today's behavior)
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


def test_select_phase_preference_is_within_tier_and_cooling_falls_through(tmp_path):
    reg, _ = _registry(tmp_path)
    enabled = ["OPENAI-GPT-5.2", "ANTHROPIC-OPUS-4.8", "ANTHROPIC-HAIKU-4"]
    chosen, _ = route.select(
        enabled, reg, "strong", preferred_ids=["ANTHROPIC-OPUS-4.8"]
    )
    assert chosen == "ANTHROPIC-OPUS-4.8"

    cooldowns = {"ANTHROPIC-OPUS-4.8": 200.0}
    fallback, _ = route.select(
        enabled,
        reg,
        "strong",
        now=100.0,
        cooldowns=cooldowns,
        preferred_ids=["ANTHROPIC-OPUS-4.8"],
    )
    assert fallback == "OPENAI-GPT-5.2"

    # A wrong-tier preference never pulls selection down from the requested tier.
    same_tier, _ = route.select(
        enabled, reg, "strong", preferred_ids=["ANTHROPIC-HAIKU-4"]
    )
    assert same_tier == "OPENAI-GPT-5.2"


def test_select_reviewer_heterogeneity_wins_over_phase_preference(tmp_path):
    reg, _ = _registry(tmp_path)
    chosen, reason = route.select(
        ["ANTHROPIC-OPUS-4.8", "OPENAI-GPT-5.2"],
        reg,
        "strong",
        exclude_families=["ANTHROPIC"],
        prefer_different=True,
        preferred_ids=["ANTHROPIC-OPUS-4.8"],
    )
    assert chosen == "OPENAI-GPT-5.2"
    assert "DEGRADED" not in reason


def test_select_prefers_a_different_provider_but_degrades(tmp_path):
    reg, _ = _registry(tmp_path)
    # Two strong models, both same provider as the implementer -> degraded, legal.
    enabled = ["ANTHROPIC-OPUS-4.8"]
    chosen, reason = route.select(
        enabled, reg, "strong", exclude_families=["ANTHROPIC"], prefer_different=True
    )
    assert chosen == "ANTHROPIC-OPUS-4.8"
    assert "DEGRADED" in reason
    # With a different-family option available, it is preferred.
    enabled2 = ["ANTHROPIC-OPUS-4.8", "OPENAI-GPT-5.2"]
    chosen2, reason2 = route.select(
        enabled2, reg, "strong", exclude_families=["ANTHROPIC"], prefer_different=True
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


def test_escalate_shared_failure_tally_rearms_after_dispatch():
    # WI-171: the shared-failure page must not re-fire forever on already-paged
    # strong-tier fails. `fails_since` is the dispatch boundary the coordinator
    # advances each time a page dispatches; only rounds AT/AFTER it count.
    c = route.DEFAULT_CONSTANTS

    def sf():
        return {"verdict": "CHANGES-REQUESTED", "tier": "strong", "margin": 0}

    def ok():
        return {"verdict": "APPROVE", "tier": "strong", "margin": 0}

    rounds = [sf(), sf()]  # two strong-tier fails -> the shared-failure regime
    assert route.escalate(rounds, c)["action"] == "page-human"
    # The coordinator dispatches and advances the boundary to len(rounds); a
    # later clean APPROVE now counts zero fresh fails, so no re-page (the 094
    # design-check bug: a clean APPROVE was still paging).
    boundary = len(rounds)
    rounds.append(ok())
    d = route.escalate(rounds, c, fails_since=boundary)
    assert d["action"] == "continue"
    # But two FRESH strong-tier fails after the boundary re-page (semantics kept).
    rounds.extend([sf(), sf()])
    d = route.escalate(rounds, c, fails_since=boundary)
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


# --- the pair-row registry: Family / Env / version-less resolution (WI-069) --- #
PAIR_CSV = """Id,Family,Model,Version,Tier,CmdTemplate,Env,Notes
# tag-rank: ga>preview>beta>exp
ANTHROPIC-OPUS-4.8,ANTHROPIC,opus,4.8,strong,claude -p {prompt} --model {model},,native
ANTHROPIC-OPUS-4.9,ANTHROPIC,opus,4.9,strong,claude -p {prompt} --model {model},,newer GA
ANTHROPIC-OPUS-5.0-PREVIEW,ANTHROPIC,opus,5.0-preview,strong,claude -p {prompt},,preview
ANTHROPIC-OPUS-4.9-ROUTER,ANTHROPIC,opus,4.9,strong,claude -p {prompt},ANTHROPIC_BASE_URL=https://r.example,router pair
ANTHROPIC-OPUS-4.9-ACCT2,ANTHROPIC,opus,4.9,strong,claude -p {prompt},CLAUDE_CONFIG_DIR=~/.c2,second account
OPENAI-GPT-5.2,OPENAI,gpt-5.2,5.2,strong,codex exec {prompt},,numeric
OPENAI-GPT-5.2-DATED,OPENAI,gpt-5.2,20260101,strong,codex exec {prompt},,dated snapshot
"""


def _pair_registry(tmp_path):
    p = tmp_path / "agents.csv"
    p.write_text(PAIR_CSV, encoding="utf-8")
    reg, errors = route.load_registry(p)
    assert errors == []
    return reg, route.load_tag_rank(p)


def test_family_column_and_env_parse(tmp_path):
    reg, _ = _pair_registry(tmp_path)
    m = reg["ANTHROPIC-OPUS-4.9-ROUTER"]
    assert m.family == "ANTHROPIC" and m.model == "opus" and m.version == "4.9"
    # The Env cell is the declarative route selector.
    assert m.env == "ANTHROPIC_BASE_URL=https://r.example"
    parsed = route.parse_env(m.env)
    assert parsed == {"ANTHROPIC_BASE_URL": "https://r.example"}
    # KEY=value;KEY2=value2, a value may carry '=', an entry without '=' is skipped.
    assert route.parse_env("A=1;B=x=y;bad;=noKey;C=3") == {
        "A": "1",
        "B": "x=y",
        "C": "3",
    }
    assert route.parse_env("") == {}


def test_registry_missing_family_and_provider_is_a_finding(tmp_path):
    p = tmp_path / "agents.csv"
    p.write_text(
        "Id,Model,Version,Tier,CmdTemplate\nX-M-1,m,1,strong,c {prompt}\n",
        encoding="utf-8",
    )
    reg, errors = route.load_registry(p)
    assert reg == {} and any("Family" in e for e in errors)


def test_resolve_exact_id_precedence(tmp_path):
    reg, tr = _pair_registry(tmp_path)
    # An exact id resolves to itself even though a newer version exists.
    rid, reason = route.resolve_token("ANTHROPIC-OPUS-4.8", reg, tr)
    assert rid == "ANTHROPIC-OPUS-4.8" and "exact id" in reason


def test_resolve_versionless_newest_skips_preview(tmp_path):
    reg, tr = _pair_registry(tmp_path)
    # Version-less: newest GA (4.9) wins; the numerically-higher 5.0-preview is
    # SKIPPED (preview), and among the equal-key 4.9 route pairs the FIRST in
    # registry order (the native row) wins.
    rid, _ = route.resolve_token("ANTHROPIC-OPUS", reg, tr)
    assert rid == "ANTHROPIC-OPUS-4.9"


def test_resolve_numeric_dominates_date(tmp_path):
    reg, tr = _pair_registry(tmp_path)
    # GPT-5.2 exists as a numeric row and a dated snapshot; the version-less token
    # is an exact id here, so force the grouping via a non-id token.
    # (OPENAI-GPT-5.2 is BOTH the id and the Family-Model normalization, so the
    #  exact-id path fires; a trailing space defeats it and exercises grouping.)
    rid, _ = route.resolve_token("OPENAI-GPT-5.2 ", reg, tr)
    # numeric 5.2 dominates the 20260101 date-kind row (date is tiebreak-only).
    assert rid == "OPENAI-GPT-5.2"


def test_resolve_tag_rank_override(tmp_path):
    reg, _ = _pair_registry(tmp_path)
    # Invert the vocabulary so preview outranks GA; the preview is no longer
    # skipped only if it's a survivor — but skip is fixed to preview/exp, so it
    # stays skipped. Override affects the TIEBREAK rank, tested directly.
    tr = route.parse_tag_rank("exp>beta>preview>ga")
    assert tr["exp"] > tr["ga"]
    assert route.parse_tag_rank("") == route.DEFAULT_TAG_RANK


def test_resolve_multi_route_survivors_follow_registry_order(tmp_path):
    # Two equal-key 4.9 pairs after the native is removed: the router row precedes
    # the acct2 row in the file, so it wins the tie.
    p = tmp_path / "agents.csv"
    p.write_text(
        "Id,Family,Model,Version,Tier,CmdTemplate,Env,Notes\n"
        "A-OPUS-49-ROUTER,ANTHROPIC,opus,4.9,strong,c {prompt},BASE=1,router\n"
        "A-OPUS-49-ACCT2,ANTHROPIC,opus,4.9,strong,c {prompt},DIR=2,acct2\n",
        encoding="utf-8",
    )
    reg, _ = route.load_registry(p)
    rid, _ = route.resolve_token("ANTHROPIC-OPUS", reg, route.DEFAULT_TAG_RANK)
    assert rid == "A-OPUS-49-ROUTER"  # first in registry order


def test_resolve_token_unresolvable(tmp_path):
    reg, tr = _pair_registry(tmp_path)
    rid, reason = route.resolve_token("GHOST-MODEL", reg, tr)
    assert rid is None and "no exact id and no Family-Model match" in reason
    ids, errors = route.resolve_enabled(["ANTHROPIC-OPUS", "GHOST-MODEL"], reg, tr)
    assert ids == ["ANTHROPIC-OPUS-4.9"]
    assert any("not a row in docs/agents.csv" in e for e in errors)


def test_acct2_row_cools_down_independently(tmp_path):
    # A second account is a second pair row with a distinct id -> its cooldown is
    # independent by construction (ruling 12): cool the primary, the acct2 stays
    # available and select() falls to it.
    reg, _ = _pair_registry(tmp_path)
    enabled = ["ANTHROPIC-OPUS-4.9", "ANTHROPIC-OPUS-4.9-ACCT2"]
    cooldowns = {}
    route.cool(cooldowns, "ANTHROPIC-OPUS-4.9", now=0.0, seconds=300)
    assert route.available(cooldowns, "ANTHROPIC-OPUS-4.9-ACCT2", 10.0)
    chosen, _ = route.select(enabled, reg, "strong", now=10.0, cooldowns=cooldowns)
    assert chosen == "ANTHROPIC-OPUS-4.9-ACCT2"


def test_router_row_is_not_diverse_from_its_native_sibling(tmp_path):
    # Family-keyed heterogeneity: a router-fronted row shares its native sibling's
    # Family, so excluding ANTHROPIC yields the DEGRADED same-family fallback, not
    # a false "different provider" pick.
    reg, _ = _pair_registry(tmp_path)
    enabled = ["ANTHROPIC-OPUS-4.9", "ANTHROPIC-OPUS-4.9-ROUTER"]
    chosen, reason = route.select(
        enabled, reg, "strong", exclude_families=["ANTHROPIC"], prefer_different=True
    )
    assert chosen == "ANTHROPIC-OPUS-4.9" and "DEGRADED" in reason


def test_cli_resolves_versionless_token(tmp_path):
    reg = tmp_path / "agents.csv"
    reg.write_text(PAIR_CSV, encoding="utf-8")
    en = tmp_path / "agents-enabled"
    en.write_text("ANTHROPIC-OPUS\n", encoding="utf-8")  # version-less
    listed = run_py(
        [SCRIPTS / "agent_route.py", "--registry", reg, "--enabled", en, "--list"],
        cwd=tmp_path,
    )
    assert listed.returncode == 0, listed.stdout + listed.stderr
    # The version-less token resolved to the concrete newest-GA id.
    assert "ANTHROPIC-OPUS-4.9" in listed.stdout and "ANTHROPIC" in listed.stdout


def test_pool_context_lists_state_and_notes(tmp_path):
    # WI-109: the page-human banner's per-row pool context — tier/family,
    # cooling-vs-available, and the Notes cell (the declared home for the
    # provider's sign-in/install hint). Lenient on an unknown enabled id.
    p = tmp_path / "agents.csv"
    p.write_text(
        "Id,Family,Model,Version,Tier,CmdTemplate,Env,Notes\n"
        "OPENAI-SOL,OPENAI,gpt-5.6-sol,5.6,strong,opencode run {prompt},,"
        "sign in: opencode auth login\n"
        "ANTHROPIC-OPUS,ANTHROPIC,opus,4.8,strong,claude -p {prompt},,\n",
        encoding="utf-8",
    )
    reg, errors = route.load_registry(p)
    assert errors == []
    now = 1000.0
    ctx = route.pool_context(
        ["OPENAI-SOL", "ANTHROPIC-OPUS", "GHOST-9"],
        reg,
        {"OPENAI-SOL": now + 90.0},  # cooling 90s from `now`
        now,
    )
    assert "enabled pool" in ctx
    # The cooling row carries its remaining seconds AND its Notes hint.
    assert (
        "OPENAI-SOL [strong, OPENAI] cooling ~90s — sign in: opencode auth login" in ctx
    )
    # The available row shows its state; empty Notes adds no dangling dash.
    assert "ANTHROPIC-OPUS [strong, ANTHROPIC] available" in ctx
    assert "available —" not in ctx
    # An enabled id not in the registry renders honestly rather than crashing.
    assert "GHOST-9 (not in docs/agents.csv)" in ctx


# --- the two-hat planner pair + runtime-nonresponse fallback (WI-196, P3) --- #
# docs/agents.csv-shaped fixtures: a two-family pool (ANTHROPIC + OPENAI) and a
# single-family pool. The planner pair is a PURE selection/fallback library
# (no launching); the tests assert the routed families, the recorded reason
# code, and FRESH-session object identity in each degraded case.
PLANNER_TWO_FAMILY_CSV = """Id,Family,Model,Version,Tier,CmdTemplate,Env,Notes
ANTHROPIC-FABLE,ANTHROPIC,claude-fable-5,5,strong,claude -p {prompt} --model {model},,frontier
OPENAI-SOL,OPENAI,gpt-5.6-sol,5.6,strong,codex exec {prompt},,cross-family leg
"""

PLANNER_ONE_FAMILY_CSV = """Id,Family,Model,Version,Tier,CmdTemplate,Env,Notes
ANTHROPIC-FABLE,ANTHROPIC,claude-fable-5,5,strong,claude -p {prompt} --model {model},,frontier
ANTHROPIC-FABLE-ACCT2,ANTHROPIC,claude-fable-5,5,strong,claude -p {prompt},CLAUDE_CONFIG_DIR=~/.c2,second account
"""


def _reg_from(tmp_path, text):
    p = tmp_path / "agents.csv"
    p.write_text(text, encoding="utf-8")
    reg, errors = route.load_registry(p)
    assert errors == []
    return reg


def test_planner_pair_two_family_branch(tmp_path):
    # Two families enabled -> the two hats route to DIFFERENT Family lines, the
    # happy (non-degraded) path with the PAIR_TWO_FAMILY reason recorded as data.
    reg = _reg_from(tmp_path, PLANNER_TWO_FAMILY_CSV)
    enabled = ["ANTHROPIC-FABLE", "OPENAI-SOL"]
    pair = route.planner_pair(enabled, reg, "strong")
    assert pair.reason == route.PAIR_TWO_FAMILY
    assert pair.degraded is False
    a, b = pair.sessions
    assert {a.family, b.family} == {"ANTHROPIC", "OPENAI"}
    assert a.model_id == "ANTHROPIC-FABLE" and b.model_id == "OPENAI-SOL"
    # Two distinct sessions (never the same object).
    assert a is not b


def test_planner_pair_one_family_pool_degrades_at_selection(tmp_path):
    # Only ANTHROPIC enabled -> degraded AT SELECTION: two fresh same-family
    # sessions, the machine-readable reason recorded, fresh-session identity held.
    reg = _reg_from(tmp_path, PLANNER_ONE_FAMILY_CSV)
    enabled = ["ANTHROPIC-FABLE", "ANTHROPIC-FABLE-ACCT2"]
    pair = route.planner_pair(enabled, reg, "strong")
    assert pair.reason == route.PAIR_SINGLE_FAMILY
    assert pair.degraded is True
    a, b = pair.sessions
    assert a.family == b.family == "ANTHROPIC"  # same family (degraded, legal)
    # FRESH-session identity: two distinct objects even in the degraded pair.
    assert a is not b


def test_planner_pair_single_row_pool_yields_two_fresh_same_id_sessions(tmp_path):
    # The narrowest pool: one row, one family. Both hats are fresh same-family
    # sessions of the same model_id (independent runs, weaker corroboration) —
    # still two DISTINCT objects.
    reg = _reg_from(tmp_path, PLANNER_TWO_FAMILY_CSV)
    pair = route.planner_pair(["ANTHROPIC-FABLE"], reg, "strong")
    assert pair.reason == route.PAIR_SINGLE_FAMILY and pair.degraded is True
    a, b = pair.sessions
    assert a.model_id == b.model_id == "ANTHROPIC-FABLE"
    assert a is not b  # fresh identity despite the shared id


def test_planner_pair_no_model_available(tmp_path):
    # Nothing routable at/above tier -> a no-model pair the coordinator pages on.
    reg = _reg_from(tmp_path, PLANNER_TWO_FAMILY_CSV)
    cooldowns = {}
    route.cool(cooldowns, "ANTHROPIC-FABLE", now=0.0, seconds=300)
    route.cool(cooldowns, "OPENAI-SOL", now=0.0, seconds=300)
    pair = route.planner_pair(
        ["ANTHROPIC-FABLE", "OPENAI-SOL"], reg, "strong", now=10.0, cooldowns=cooldowns
    )
    assert pair.reason == route.PAIR_NO_MODEL and pair.sessions == (None, None)


def test_planner_fallback_runtime_nonresponse_branch(tmp_path):
    # Two families were routed; ANTHROPIC proves NONRESPONSIVE at launch. The
    # fallback returns two FRESH same-family sessions from the RESPONDING family
    # (OPENAI), with the degraded-availability reason recorded as data.
    reg = _reg_from(tmp_path, PLANNER_TWO_FAMILY_CSV)
    enabled = ["ANTHROPIC-FABLE", "OPENAI-SOL"]
    pair = route.planner_pair(enabled, reg, "strong")
    failed = pair.sessions[0]  # the ANTHROPIC hat that went dark
    assert failed.family == "ANTHROPIC"

    fb = route.planner_fallback(failed, enabled, reg, "strong")
    assert fb.reason == route.PAIR_RUNTIME_FALLBACK
    assert fb.degraded is True
    a, b = fb.sessions
    # Both fresh sessions come from the responding (OPENAI) family.
    assert a.family == b.family == "OPENAI"
    assert a.model_id == b.model_id == "OPENAI-SOL"
    # FRESH-session identity: neither is the failed object reused, and the two
    # are distinct from each other.
    assert a is not failed and b is not failed and a is not b


def test_planner_fallback_no_responding_family(tmp_path):
    # The other family is also unavailable -> a no-responder pair (page).
    reg = _reg_from(tmp_path, PLANNER_TWO_FAMILY_CSV)
    enabled = ["ANTHROPIC-FABLE", "OPENAI-SOL"]
    failed = route.PlannerSession("A", "ANTHROPIC-FABLE", "ANTHROPIC", "strong")
    cooldowns = {}
    route.cool(cooldowns, "OPENAI-SOL", now=0.0, seconds=300)
    fb = route.planner_fallback(
        failed, enabled, reg, "strong", now=10.0, cooldowns=cooldowns
    )
    assert fb.reason == route.PAIR_NO_RESPONDER and fb.sessions == (None, None)


def test_weak_is_a_legacy_alias_for_quick(tmp_path):
    # WI-113 (owner rename 2026-07-12): the bottom tier is `quick`; the old
    # `weak` vocabulary still loads, validates, and selects — never-breaking
    # (the Provider->Family precedent). REGISTRY_CSV above deliberately still
    # says `weak`, so this doubles as the legacy-registry proof.
    assert route.TIER_ORDER == ("quick", "medium", "strong")
    assert route.normalize_tier("WEAK") == "quick"
    assert route.normalize_tier(" quick ") == "quick"
    reg, errors = _registry(tmp_path)
    assert errors == []
    assert reg["ANTHROPIC-HAIKU-4"].tier == "quick"  # loaded from Tier=weak
    # Selecting BY the legacy token also works (normalized inside select()).
    chosen, reason = route.select(["ANTHROPIC-HAIKU-4"], reg, "weak")
    assert chosen == "ANTHROPIC-HAIKU-4", reason
    # And a legacy tier-map value passes the loop's normalization (phase_tier).
    from conftest import load_script

    agent_loop = load_script("agent_loop")
    assert agent_loop.phase_tier("BUILD", {"BUILD": "weak"}) == "quick"


# --- per-phase draw weights in docs/agents-enabled (WI-236) ---------------- #
# A four-family strong-tier pool: OpenAI + Moonshot(Kimi) + xAI(Grok) reviewers
# and an Anthropic implementer. Weights are declared per phase in agents-enabled
# and drive a DETERMINISTIC weighted rotation keyed on the per-train session
# counter — never randomness, and byte-identical to before when unannotated.
WEIGHT_CSV = """Id,Family,Model,Version,Tier,CmdTemplate,Env,Notes
OPENAI-TERRA,OPENAI,terra,1,strong,codex exec,,openai reviewer
MOONSHOT-KIMI,MOONSHOT,kimi,1,strong,opencode run,,kimi judge
XAI-GROK,XAI,grok,1,strong,opencode run,,grok reviewer
ANTHROPIC-FABLE,ANTHROPIC,claude-fable-5,5,strong,claude -p --model {model},,implementer
"""


def _weight_registry(tmp_path):
    p = tmp_path / "agents.csv"
    p.write_text(WEIGHT_CSV, encoding="utf-8")
    reg, errors = route.load_registry(p)
    assert errors == []
    return reg


def test_weighted_rotation_4to1to1_exact_sequence(tmp_path):
    # Required regression 1: a 4:1:1 REVIEW weighting yields exactly this
    # deterministic rotation over 12 draws with full availability — the SEQUENCE,
    # not just the counts. counter = the durable per-train session number.
    reg = _weight_registry(tmp_path)
    enabled = ["OPENAI-TERRA", "MOONSHOT-KIMI", "XAI-GROK"]
    weights = {"OPENAI-TERRA": 4, "MOONSHOT-KIMI": 1, "XAI-GROK": 1}
    seq = [
        route.select(enabled, reg, "strong", weights=weights, counter=n)[0]
        for n in range(1, 13)
    ]
    T, K, G = "OPENAI-TERRA", "MOONSHOT-KIMI", "XAI-GROK"
    assert seq == [T, T, T, K, G, T, T, T, T, K, G, T]
    # The share holds: 8:2:2 over 12 == 4:1:1.
    assert (seq.count(T), seq.count(K), seq.count(G)) == (8, 2, 2)


def test_weighted_share_renormalizes_over_available_then_returns(tmp_path):
    # Required regression 2: a cooling model's share renormalizes over the
    # available remainder (4:1:1 -> 4:1 over TERRA:GROK) and the model returns
    # to the draw once its cooldown lapses — the SAME counter now lands it.
    reg = _weight_registry(tmp_path)
    enabled = ["OPENAI-TERRA", "MOONSHOT-KIMI", "XAI-GROK"]
    weights = {"OPENAI-TERRA": 4, "MOONSHOT-KIMI": 1, "XAI-GROK": 1}
    cooldowns = {}
    route.cool(cooldowns, "MOONSHOT-KIMI", now=100.0, seconds=60)
    cooling = [
        route.select(
            enabled,
            reg,
            "strong",
            now=100.0,
            cooldowns=cooldowns,
            weights=weights,
            counter=n,
        )[0]
        for n in range(1, 11)
    ]
    assert "MOONSHOT-KIMI" not in cooling  # held out while cooling
    assert "OPENAI-TERRA" in cooling and "XAI-GROK" in cooling  # remainder shares
    # counter 4 lands GROK under the renormalized 4:1, but the very same counter
    # lands the cooled model once it is back (now past the 60s cooldown).
    assert (
        route.select(
            enabled,
            reg,
            "strong",
            now=100.0,
            cooldowns=cooldowns,
            weights=weights,
            counter=4,
        )[0]
        == "XAI-GROK"
    )
    assert (
        route.select(
            enabled,
            reg,
            "strong",
            now=200.0,
            cooldowns=cooldowns,
            weights=weights,
            counter=4,
        )[0]
        == "MOONSHOT-KIMI"
    )


def test_high_critique_weight_concentrates_without_starving_heterogeneity(tmp_path):
    # Required regression 3: CRITIQUE=9 concentrates the judge draws on Kimi, but
    # cannot starve heterogeneity — the same-family implementer (Anthropic) is
    # NEVER drawn even with an absurd weight, and the other cross-family reviewer
    # still earns its 1/10 share.
    reg = _weight_registry(tmp_path)
    enabled = ["MOONSHOT-KIMI", "OPENAI-TERRA", "ANTHROPIC-FABLE"]
    # An absurd weight on the implementer's own family proves weights can never
    # force a same-family review — the exclude wins first.
    weights = {"MOONSHOT-KIMI": 9, "OPENAI-TERRA": 1, "ANTHROPIC-FABLE": 99}
    picks = [
        route.select(
            enabled,
            reg,
            "strong",
            exclude_families=["ANTHROPIC"],
            prefer_different=True,
            weights=weights,
            counter=n,
        )[0]
        for n in range(1, 21)
    ]
    assert "ANTHROPIC-FABLE" not in picks  # heterogeneity is never starved
    assert picks.count("MOONSHOT-KIMI") == 18  # 9/10 of the draws
    assert picks.count("OPENAI-TERRA") == 2  # the cross-family reviewer keeps 1/10


def test_unannotated_and_equal_weights_are_byte_identical_to_today(tmp_path):
    # Required regression 4: an unannotated file (no weights) selects exactly as
    # before — the first enabled id every draw, whatever the counter. An
    # explicitly all-equal annotation is the same: uniform weights == line-order
    # tie-break, no rotation (the byte-identical guarantee).
    reg = _weight_registry(tmp_path)
    enabled = ["OPENAI-TERRA", "MOONSHOT-KIMI", "XAI-GROK"]
    for counter in range(0, 6):
        assert (
            route.select(enabled, reg, "strong", counter=counter)[0] == "OPENAI-TERRA"
        )
        equal = {"OPENAI-TERRA": 2, "MOONSHOT-KIMI": 2, "XAI-GROK": 2}
        assert (
            route.select(enabled, reg, "strong", weights=equal, counter=counter)[0]
            == "OPENAI-TERRA"
        )


def test_malformed_annotation_fails_preflight_naming_the_line(tmp_path):
    # Required regression 5: every malformed annotation shape is a hard error
    # naming the line (the consent surface is never silently ignored). Shapes:
    # unknown phase, non-integer, negative, duplicate phase, missing '='.
    p = tmp_path / "agents-enabled"
    p.write_text(
        "OPENAI-TERRA  REVIEW=4\n"  # a well-formed line resolves clean
        "MOONSHOT-KIMI  BOGUS=2\n"  # unknown phase
        "XAI-GROK  REVIEW=two\n"  # non-integer
        "OPENAI-LUNA  CRITIQUE=-1\n"  # negative
        "ANTHROPIC-FABLE  REVIEW=1 REVIEW=2\n"  # duplicate phase on one line
        "GOOGLE-GEM  REVIEW\n",  # missing '='
        encoding="utf-8",
    )
    entries, errors = route.load_enabled_entries(p)
    # Every id is still captured (presence turns routing on); the errors carry.
    assert [tok for tok, _w in entries] == [
        "OPENAI-TERRA",
        "MOONSHOT-KIMI",
        "XAI-GROK",
        "OPENAI-LUNA",
        "ANTHROPIC-FABLE",
        "GOOGLE-GEM",
    ]
    joined = "\n".join(errors)
    assert "BOGUS" in joined and "unknown phase" in joined
    assert "non-integer weight 'two'" in joined
    assert "negative weight -1" in joined
    assert "duplicate phase REVIEW" in joined
    assert "expected PHASE=int" in joined  # the missing '=' shape
    # Each error names its offending line verbatim (repr of the stripped line).
    assert "'MOONSHOT-KIMI  BOGUS=2'" in joined
    # The clean line contributed no error.
    assert not any("OPENAI-TERRA" in e for e in errors)


def test_prefer_map_pin_wins_its_phase_over_weights(tmp_path):
    # Required regression 6: an AGENT_PREFER_MAP pin still wins its phase outright
    # with weights present — the weighted rotation governs only the UNPINNED
    # remainder. Weights favour Kimi 9:1, but the Terra pin takes every draw.
    reg = _weight_registry(tmp_path)
    enabled = ["OPENAI-TERRA", "MOONSHOT-KIMI"]
    weights = {"MOONSHOT-KIMI": 9, "OPENAI-TERRA": 1}
    for counter in range(0, 8):
        pinned = route.select(
            enabled,
            reg,
            "strong",
            preferred_ids=["OPENAI-TERRA"],
            weights=weights,
            counter=counter,
        )[0]
        assert pinned == "OPENAI-TERRA"
    # Without the pin, the 9:1 weight makes Kimi the dominant draw (contrast).
    unpinned = [
        route.select(enabled, reg, "strong", weights=weights, counter=n)[0]
        for n in range(1, 11)
    ]
    assert unpinned.count("MOONSHOT-KIMI") == 9 and unpinned.count("OPENAI-TERRA") == 1


def test_zero_weight_is_fallback_only(tmp_path):
    # Required regression 7: the ruled zero-weight behavior — PHASE=0 means
    # "never drawn for the phase unless it is the sole legal candidate" (routing
    # never dead-ends). Terra=0 is skipped while Kimi is available, but taken when
    # Kimi cools; all-zero falls back to line order.
    reg = _weight_registry(tmp_path)
    enabled = ["OPENAI-TERRA", "MOONSHOT-KIMI"]
    weights = {"OPENAI-TERRA": 0, "MOONSHOT-KIMI": 1}
    fallback_only = [
        route.select(enabled, reg, "strong", weights=weights, counter=n)[0]
        for n in range(0, 6)
    ]
    assert fallback_only == ["MOONSHOT-KIMI"] * 6  # the 0-weight id is held out
    # Sole legal candidate: cool Kimi, and the 0-weight Terra is taken (never a
    # dead-end).
    cooldowns = {}
    route.cool(cooldowns, "MOONSHOT-KIMI", now=0.0, seconds=300)
    lone = route.select(
        enabled,
        reg,
        "strong",
        now=10.0,
        cooldowns=cooldowns,
        weights=weights,
        counter=3,
    )[0]
    assert lone == "OPENAI-TERRA"
    # All fallback-only -> line order decides (never a dead-end).
    all_zero = {"OPENAI-TERRA": 0, "MOONSHOT-KIMI": 0}
    assert (
        route.select(enabled, reg, "strong", weights=all_zero, counter=5)[0]
        == "OPENAI-TERRA"
    )


def test_enabled_annotations_parse_and_resolve_to_ids(tmp_path):
    # The grammar end-to-end: a well-formed annotated file parses to (token,
    # weights) entries, `load_enabled` strips the annotations to bare ids (so the
    # legacy consumers are unaffected), and `resolved_weights` carries the weights
    # onto the resolved registry ids. REVIEW expands to both reviewer legs.
    p = tmp_path / "agents-enabled"
    p.write_text(
        "# a comment\n"
        "OPENAI-TERRA        REVIEW=4\n"
        "MOONSHOT-KIMI       REVIEW=1  CRITIQUE=9\n"
        "XAI-GROK\n",  # unannotated == weight 1 everywhere
        encoding="utf-8",
    )
    entries, errors = route.load_enabled_entries(p)
    assert errors == []
    assert route.load_enabled(p) == ["OPENAI-TERRA", "MOONSHOT-KIMI", "XAI-GROK"]
    reg = _weight_registry(tmp_path)
    wmap = route.resolved_weights(entries, reg, route.DEFAULT_TAG_RANK)
    # REVIEW expanded to both legs; the unannotated id contributes nothing (== 1).
    assert wmap == {
        "OPENAI-TERRA": {"REVIEW-A": 4, "REVIEW-B": 4},
        "MOONSHOT-KIMI": {"REVIEW-A": 1, "REVIEW-B": 1, "CRITIQUE": 9},
    }
    # phase_weights projects the map onto a concrete phase (BUILD covers '').
    assert route.phase_weights(wmap, "REVIEW-A") == {
        "OPENAI-TERRA": 4,
        "MOONSHOT-KIMI": 1,
    }
    assert route.phase_weights(wmap, "CRITIQUE") == {"MOONSHOT-KIMI": 9}
    assert route.phase_weights(wmap, "BUILD") == {}
    assert route.phase_weights(wmap, "") == {}
