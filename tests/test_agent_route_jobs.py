"""agent_route.draw_for_job — the config-driven job-pool draw (SR-154/LLR-181,
TC-175).

TC-175 permutations: full-pool | unavailable-route | no-capable-route |
adjudicator | arbiter.

The requirement is an ORDER of operations, so the refusals carry most of the
proof: a pool with no capable route has to refuse rather than downgrade, and —
the case the order exists for — a route going unavailable must never let the
fallback buy a route past the capability bar or below the strength floor. Those
two are tested at least as hard as the happy path. The draw itself is seeded, so
every assertion here is exact rather than sampled.

The other half of the module (the docs/agents.csv registry x enable-list path)
is test_agent_route.py's; the last test in this file guards that this slice
added a path beside it rather than rewiring it.
"""

import random

import pytest
from conftest import SCRIPTS, load_script, run_py

route = load_script("agent_route")
config = load_script("config")

ALL_CAPS = (
    '["planning", "critique", "arbitration", "implementation", "review", '
    '"adjudication"]'
)

# Four routes spanning both axes the draw reasons over: two families x three
# declared strengths. Every one declares every capability, so a test that wants
# the capability bar to bite says so explicitly rather than inheriting it.
ROUTES = """schema = 1

[routing]
enabled = true

[[routes]]
id = "ANTHROPIC-STRONG"
family = "ANTHROPIC"
model = "opus"
strength = 3
capabilities = {caps}

[[routes]]
id = "OPENAI-STRONG"
family = "OPENAI"
model = "gpt-sol"
strength = 3
capabilities = {caps}

[[routes]]
id = "ANTHROPIC-MEDIUM"
family = "ANTHROPIC"
model = "opus"
strength = 2
capabilities = {caps}

[[routes]]
id = "OPENAI-QUICK"
family = "OPENAI"
model = "gpt-luna"
strength = 1
capabilities = {caps}
""".format(caps=ALL_CAPS)


def write_config(root, text):
    """Put `text` at <root>/docs/config.toml and return root."""
    docs = root / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "config.toml").write_text(text, encoding="utf-8", newline="\n")
    return root


def with_job(root, body, routes=ROUTES):
    """A repo whose config declares ROUTES plus one `[jobs.*]` table."""
    return write_config(root, routes + "\n" + body)


class ScriptedRandom:
    """A `random.Random` stand-in whose `randrange` returns declared slots, so
    the cumulative-range arithmetic can be asserted exactly instead of sampled.
    It also records the totals it was asked for — the denominator IS the sum of
    the declared weights, and a test that never checks it would pass just as
    happily against a uniform draw."""

    def __init__(self, slots):
        self.slots = list(slots)
        self.totals = []

    def randrange(self, total):
        self.totals.append(total)
        return self.slots.pop(0)


def draw_ids(root, job, n=60, seed=20260808, **kw):
    """The set of route ids `n` seeded draws produce — the shape most of these
    assertions want, since "which routes are reachable" is the property under
    test rather than which one a particular slot hit."""
    rng = random.Random(seed)
    return {route.draw_for_job(root, job, rng=rng, **kw).route.id for _ in range(n)}


# --- the declared vocabulary -------------------------------------------------


def test_every_declared_job_has_a_capability_and_the_roles_are_pinned():
    # config.JOBS is the closed vocabulary; a job added there with no capability
    # here would refuse at the FIRST draw in production instead of failing now.
    assert set(route.JOB_CAPABILITY) == set(config.JOBS)
    # The two roles whose independence is not the adopter's to switch off.
    assert route.CROSS_FAMILY_JOBS == frozenset({"reviewer", "adjudicator"})
    assert "arbiter" not in route.CROSS_FAMILY_JOBS  # its preference is the dial


def test_a_declared_requires_capability_is_read_not_ignored(tmp_path):
    """The DECLARED bar wins over the role default — SR-154's word "declared".

    This was read with `getattr(cfg.jobs, job)` on a plain dict, so it answered
    None for every job name and the role default ALWAYS won. Both directions are
    driven here because the two failures are opposite and only one of them looks
    like a failure: a tightened bar failed OPEN (a route the adopter excluded got
    the job, and the reason line asserted a capability it had not been checked
    for), and a loosened one refused for a capability nobody asked about.
    """
    # (a) Fails open without the fix: the reviewer must clear `adjudication`,
    # the only pool route declares `review`, and the draw must REFUSE.
    routes = ROUTES.replace(ALL_CAPS, '["review"]')
    strict = with_job(
        tmp_path,
        '[jobs.reviewer]\nrequires_capability = "adjudication"\n'
        'pool = [ { route = "ANTHROPIC-STRONG", weight = 1 } ]\n',
        routes=routes,
    )
    drawn = route.draw_for_job(strict, "reviewer", rng=random.Random(1))
    assert drawn.capability == "adjudication", "the declared bar was not read"
    assert drawn.route is None
    (finding,) = drawn.findings
    assert finding.key == "jobs.reviewer.pool"
    assert "'adjudication' capability" in finding.reason

    # (b) Refuses without the fix: the adopter widened the reviewer to plain
    # `text`, and a text-only route is exactly what they said may serve it.
    text_only = with_job(
        tmp_path / "text-only",
        '[jobs.reviewer]\nrequires_capability = "text"\n'
        'pool = [ { route = "ANTHROPIC-STRONG", weight = 1 } ]\n',
        routes=ROUTES.replace(ALL_CAPS, '["text"]'),
    )
    drawn = route.draw_for_job(text_only, "reviewer", rng=random.Random(1))
    assert drawn.findings == ()
    assert drawn.route.id == "ANTHROPIC-STRONG"
    assert drawn.capability == "text"
    # The no-silent-swap line has to name the bar actually cleared, not a
    # role default the draw never applied.
    assert "declares text" in drawn.reason


def test_an_undeclared_requires_capability_still_falls_back_to_the_role(tmp_path):
    # The fix must be behaviour-preserving for every config that never set it:
    # an unset job resolves its role default exactly as before.
    root = with_job(
        tmp_path,
        '[jobs.planner]\npool = [ { route = "ANTHROPIC-STRONG", weight = 1 } ]\n',
    )
    assert route.draw_for_job(root, "planner", rng=random.Random(1)).capability == (
        "planning"
    )


def test_strength_and_tier_are_one_ladder_read_from_both_ends():
    assert [route.strength_tier(s) for s in (1, 2, 3)] == list(route.TIER_ORDER)
    assert [route.tier_strength(t) for t in route.TIER_ORDER] == [1, 2, 3]
    assert route.tier_strength("weak") == 1  # the legacy alias still reads
    assert route.strength_tier(4) is None and route.tier_strength("superb") is None


# --- permutation: full-pool --------------------------------------------------


def test_full_pool_draws_in_declared_proportion(tmp_path):
    root = with_job(
        tmp_path,
        '[jobs.implementer]\npool = [ { route = "ANTHROPIC-STRONG", weight = 3 },\n'
        '         { route = "OPENAI-STRONG", weight = 1 } ]\n',
    )
    # Exact: the slot indexes the cumulative ranges over the DECLARED weights.
    scripted = ScriptedRandom([0, 1, 2, 3])
    picked = [
        route.draw_for_job(root, "implementer", rng=scripted).route.id for _ in range(4)
    ]
    assert picked == ["ANTHROPIC-STRONG"] * 3 + ["OPENAI-STRONG"]
    assert scripted.totals == [4, 4, 4, 4]  # the denominator is the weight sum

    # And over a seeded run the share follows the declaration (3:1 -> 0.75).
    # 600 draws, not 6000: the arithmetic is already pinned exactly above, so
    # this only has to corroborate it over the real public path, and every draw
    # re-reads docs/config.toml (a per-session cost in production, a per-loop one
    # here). The seed makes the measured share a constant, so the band is a
    # readability aid rather than a flake budget.
    rng = random.Random(7)
    draws = [
        route.draw_for_job(root, "implementer", rng=rng).route.id for _ in range(600)
    ]
    share = draws.count("ANTHROPIC-STRONG") / len(draws)
    assert 0.72 <= share <= 0.78, share


def test_full_pool_reports_the_route_it_drew(tmp_path):
    root = with_job(
        tmp_path,
        '[jobs.planner]\npool = [ { route = "ANTHROPIC-STRONG", weight = 1 } ]\n',
    )
    drawn = route.draw_for_job(root, "planner", rng=random.Random(1))
    assert drawn.route.id == "ANTHROPIC-STRONG"
    assert drawn.findings == () and drawn.degraded is False
    assert drawn.capability == "planning"
    # The reason is the line the coordinator LOGS before launch: it has to name
    # the route, its tier vocabulary, its family and the bar it cleared.
    for token in ("ANTHROPIC-STRONG", "strong", "ANTHROPIC", "planner", "planning"):
        assert token in drawn.reason, drawn.reason


def test_zero_weight_is_fallback_only_and_never_dead_ends(tmp_path):
    root = with_job(
        tmp_path,
        '[jobs.implementer]\npool = [ { route = "ANTHROPIC-STRONG", weight = 0 },\n'
        '         { route = "OPENAI-STRONG", weight = 1 } ]\n',
    )
    assert draw_ids(root, "implementer") == {"OPENAI-STRONG"}
    # Sole legal candidate: the 0-weight route is taken rather than refused.
    assert draw_ids(root, "implementer", exclude=("OPENAI-STRONG",)) == {
        "ANTHROPIC-STRONG"
    }


def test_capability_filter_beats_a_much_larger_weight(tmp_path):
    routes = ROUTES.replace(
        '[[routes]]\nid = "OPENAI-STRONG"\nfamily = "OPENAI"\nmodel = "gpt-sol"\n'
        "strength = 3\ncapabilities = " + ALL_CAPS,
        '[[routes]]\nid = "OPENAI-STRONG"\nfamily = "OPENAI"\nmodel = "gpt-sol"\n'
        'strength = 3\ncapabilities = ["planning"]',
    )
    root = with_job(
        tmp_path,
        '[jobs.reviewer]\npool = [ { route = "ANTHROPIC-STRONG", weight = 1 },\n'
        '         { route = "OPENAI-STRONG", weight = 500 } ]\n',
        routes=routes,
    )
    # The heavy route cannot review, so weight never gets a vote on the bar.
    assert draw_ids(root, "reviewer", n=200) == {"ANTHROPIC-STRONG"}


def test_declared_capability_case_is_folded(tmp_path):
    routes = ROUTES.replace(ALL_CAPS, '["Review", "IMPLEMENTATION"]')
    root = with_job(
        tmp_path,
        '[jobs.reviewer]\npool = [ { route = "ANTHROPIC-STRONG", weight = 1 } ]\n',
        routes=routes,
    )
    assert route.draw_for_job(root, "reviewer", rng=random.Random(1)).route is not None


# --- permutation: unavailable-route -----------------------------------------


def test_unavailable_route_falls_back_to_an_equal_or_stronger_one(tmp_path):
    root = with_job(
        tmp_path,
        "[jobs.implementer]\nminimum_strength = 2\n"
        'pool = [ { route = "ANTHROPIC-MEDIUM", weight = 1 },\n'
        '         { route = "ANTHROPIC-STRONG", weight = 1 },\n'
        '         { route = "OPENAI-QUICK", weight = 50 } ]\n',
    )
    # The floor holds even unexcluded: the heavily-weighted quick route is below
    # minimum_strength, so it is never in the draw at all.
    assert draw_ids(root, "implementer", n=200) == {
        "ANTHROPIC-MEDIUM",
        "ANTHROPIC-STRONG",
    }
    # The medium route goes unavailable -> the draw goes UP, never down.
    assert draw_ids(root, "implementer", n=200, exclude=("ANTHROPIC-MEDIUM",)) == {
        "ANTHROPIC-STRONG"
    }


def test_no_survivor_above_the_floor_refuses_instead_of_downgrading(tmp_path):
    root = with_job(
        tmp_path,
        "[jobs.implementer]\nminimum_strength = 2\n"
        'pool = [ { route = "ANTHROPIC-MEDIUM", weight = 1 },\n'
        '         { route = "ANTHROPIC-STRONG", weight = 1 },\n'
        '         { route = "OPENAI-QUICK", weight = 1 } ]\n',
    )
    drawn = route.draw_for_job(
        root, "implementer", exclude=("ANTHROPIC-MEDIUM", "ANTHROPIC-STRONG")
    )
    assert drawn.route is None  # OPENAI-QUICK is present, drawable and REFUSED
    (finding,) = drawn.findings
    assert finding.key == "jobs.implementer.pool"
    assert "no drawable route" in finding.reason
    assert "ANTHROPIC-MEDIUM, ANTHROPIC-STRONG" in finding.reason


def test_a_fallback_never_buys_a_route_past_the_capability_bar(tmp_path):
    # The order of operations, stated as a test: the only available route is the
    # one that cannot do the job, so the draw refuses rather than falling to it.
    routes = ROUTES.replace(
        '[[routes]]\nid = "OPENAI-STRONG"\nfamily = "OPENAI"\nmodel = "gpt-sol"\n'
        "strength = 3\ncapabilities = " + ALL_CAPS,
        '[[routes]]\nid = "OPENAI-STRONG"\nfamily = "OPENAI"\nmodel = "gpt-sol"\n'
        'strength = 3\ncapabilities = ["planning"]',
    )
    root = with_job(
        tmp_path,
        '[jobs.reviewer]\npool = [ { route = "ANTHROPIC-STRONG", weight = 1 },\n'
        '         { route = "OPENAI-STRONG", weight = 1 } ]\n',
        routes=routes,
    )
    drawn = route.draw_for_job(root, "reviewer", exclude=("ANTHROPIC-STRONG",))
    assert drawn.route is None
    assert "no drawable route" in drawn.findings[0].reason


def test_minimum_strength_above_the_pool_names_the_dial(tmp_path):
    root = with_job(
        tmp_path,
        "[jobs.reviewer]\nminimum_strength = 3\n"
        'pool = [ { route = "ANTHROPIC-MEDIUM", weight = 1 },\n'
        '         { route = "OPENAI-QUICK", weight = 1 } ]\n',
    )
    drawn = route.draw_for_job(root, "reviewer")
    assert drawn.route is None
    (finding,) = drawn.findings
    assert finding.key == "jobs.reviewer.minimum_strength"
    assert "is 3 but the strongest review-capable route in the pool is 2" in (
        finding.reason
    )


def test_an_exclusion_outside_the_pool_is_a_no_op(tmp_path):
    root = with_job(
        tmp_path,
        '[jobs.critic]\npool = [ { route = "ANTHROPIC-STRONG", weight = 1 } ]\n',
    )
    drawn = route.draw_for_job(
        root, "critic", exclude=("NOT-A-ROUTE",), rng=random.Random(3)
    )
    assert drawn.route.id == "ANTHROPIC-STRONG" and drawn.degraded is False


# --- permutation: no-capable-route ------------------------------------------


def test_pool_with_no_capable_route_refuses_rather_than_downgrading(tmp_path):
    # The just-converted state contracts §1 describes: docs/agents.csv had no
    # capability column, so every converted route arrives with an empty list.
    routes = ROUTES.replace(ALL_CAPS, "[]")
    root = with_job(
        tmp_path,
        '[jobs.reviewer]\npool = [ { route = "ANTHROPIC-STRONG", weight = 1 },\n'
        '         { route = "OPENAI-STRONG", weight = 1 } ]\n',
        routes=routes,
    )
    drawn = route.draw_for_job(root, "reviewer", rng=random.Random(1))
    assert drawn.route is None and drawn.capability == "review"
    (finding,) = drawn.findings
    assert finding.key == "jobs.reviewer.pool"
    assert "'review' capability" in finding.reason
    # The message shows what each route DOES declare, so the fix is visible in it.
    assert "ANTHROPIC-STRONG=[]" in finding.reason
    assert "OPENAI-STRONG=[]" in finding.reason
    assert "refuses rather than downgrading" in finding.reason


def test_a_pool_naming_undeclared_routes_reports_every_one(tmp_path):
    root = with_job(
        tmp_path,
        '[jobs.reviewer]\npool = [ { route = "GHOST-ONE", weight = 1 },\n'
        '         { route = "GHOST-TWO", weight = 1 } ]\n',
    )
    drawn = route.draw_for_job(root, "reviewer")
    assert drawn.route is None
    keys = [f.key for f in drawn.findings]
    assert keys == ["jobs.reviewer.pool[0].route", "jobs.reviewer.pool[1].route"]
    assert "GHOST-TWO" in drawn.findings[1].reason


def test_an_empty_pool_and_an_undeclared_job_each_name_themselves(tmp_path):
    root = with_job(tmp_path, "[jobs.reviewer]\nminimum_strength = 2\n")
    empty = route.draw_for_job(root, "reviewer")
    assert empty.route is None
    assert empty.findings[0].key == "jobs.reviewer.pool"
    assert "is empty" in empty.findings[0].reason

    typo = route.draw_for_job(root, "reviewr")
    assert typo.route is None and typo.capability is None
    assert typo.findings[0].key == "jobs.reviewr"
    assert "not a declared job" in typo.findings[0].reason
    assert "adjudicator" in typo.findings[0].reason  # the expected set is shown


def test_routing_off_and_an_absent_config_refuse_naming_the_consent_key(tmp_path):
    off = with_job(
        tmp_path,
        '[jobs.reviewer]\npool = [ { route = "ANTHROPIC-STRONG", weight = 1 } ]\n',
        routes=ROUTES.replace("enabled = true", "enabled = false"),
    )
    drawn = route.draw_for_job(off, "reviewer")
    assert drawn.route is None
    assert [f.key for f in drawn.findings] == ["routing.enabled"]
    assert "opt-in" in drawn.findings[0].reason

    # An absent document is not a finding of its own — it is the declared
    # default, and the default for managed routing is off. It leaves the repo
    # with TWO honest problems (no consent, no pool) and both are reported: one
    # run has to teach the adopter everything wrong, not the first thing wrong.
    bare = route.draw_for_job(tmp_path / "nothing-here", "reviewer")
    assert bare.route is None
    assert [f.key for f in bare.findings] == ["routing.enabled", "jobs.reviewer"]
    assert "declares no pool in docs/config.toml" in bare.findings[1].reason


def test_a_malformed_config_refuses_with_the_loaders_own_findings(tmp_path):
    root = with_job(
        tmp_path,
        '[jobs.reviewer]\npool = [ { route = "ANTHROPIC-STRONG", weight = 1 } ]\n',
        routes=ROUTES.replace("[routing]", "[policy]\nreview_rounds = 9\n\n[routing]"),
    )
    drawn = route.draw_for_job(root, "reviewer")
    assert drawn.route is None
    assert "policy.review_rounds" in [f.key for f in drawn.findings]


def test_refusals_carry_the_programs_one_message_shape(tmp_path):
    routes = ROUTES.replace(ALL_CAPS, "[]")
    root = with_job(
        tmp_path,
        '[jobs.reviewer]\npool = [ { route = "ANTHROPIC-STRONG", weight = 1 } ]\n',
        routes=routes,
    )
    (line,) = route.draw_for_job(root, "reviewer").refusals
    assert line.startswith("agent_route: REFUSED - jobs.reviewer.pool (")
    assert line.endswith(")")


# --- permutations: adjudicator + arbiter ------------------------------------


@pytest.mark.parametrize("job", ["reviewer", "adjudicator"])
def test_judging_roles_prefer_a_cross_family_route_without_being_told(tmp_path, job):
    # No prefer_cross_family dial in the table: the preference is pinned by the
    # role, because a judge drawn from the judged party's family shares its
    # blind spots. The adjudicator resolves through the reviewer's path exactly.
    root = with_job(
        tmp_path,
        '[jobs.{}]\npool = [ {{ route = "ANTHROPIC-STRONG", weight = 20 }},\n'
        '         {{ route = "OPENAI-STRONG", weight = 1 }} ]\n'.format(job),
    )
    # Unconstrained, the heavy route wins its share of the draws.
    assert "ANTHROPIC-STRONG" in draw_ids(root, job, n=100)
    # With the implementer's route excluded, its whole FAMILY is preferred
    # against — even though the same-family medium route is not excluded by id.
    drawn = route.draw_for_job(
        root, job, exclude=("ANTHROPIC-STRONG",), rng=random.Random(5)
    )
    assert drawn.route.id == "OPENAI-STRONG" and drawn.degraded is False
    assert draw_ids(root, job, n=100, exclude=("ANTHROPIC-STRONG",)) == {
        "OPENAI-STRONG"
    }


@pytest.mark.parametrize("job", ["reviewer", "adjudicator"])
def test_a_declared_false_cannot_switch_a_judging_roles_independence_off(tmp_path, job):
    root = with_job(
        tmp_path,
        "[jobs.{}]\nprefer_cross_family = false\n"
        'pool = [ {{ route = "ANTHROPIC-MEDIUM", weight = 1 }},\n'
        '         {{ route = "OPENAI-STRONG", weight = 1 }} ]\n'.format(job),
    )
    assert draw_ids(root, job, n=100, exclude=("ANTHROPIC-MEDIUM",)) == {
        "OPENAI-STRONG"
    }


@pytest.mark.parametrize("job", ["reviewer", "adjudicator"])
def test_the_degraded_same_family_draw_stays_legal_and_is_recorded(tmp_path, job):
    # Only one family is routable. The documented degraded mode: a same-family
    # second opinion corroborates weakly, but SKIPPING it corroborates not at
    # all — so the draw succeeds, flagged, rather than refusing.
    root = with_job(
        tmp_path,
        '[jobs.{}]\npool = [ {{ route = "ANTHROPIC-STRONG", weight = 1 }},\n'
        '         {{ route = "ANTHROPIC-MEDIUM", weight = 1 }} ]\n'.format(job),
    )
    drawn = route.draw_for_job(
        root, job, exclude=("ANTHROPIC-STRONG",), rng=random.Random(2)
    )
    assert drawn.route.id == "ANTHROPIC-MEDIUM"
    assert drawn.degraded is True
    assert "DEGRADED" in drawn.reason and "weaker corroboration" in drawn.reason


def test_the_arbiter_resolves_through_the_same_path_on_its_own_capability(tmp_path):
    root = with_job(
        tmp_path,
        "[jobs.arbiter]\nminimum_strength = 2\n"
        'pool = [ { route = "ANTHROPIC-STRONG", weight = 1 },\n'
        '         { route = "OPENAI-QUICK", weight = 40 } ]\n',
    )
    drawn = route.draw_for_job(root, "arbiter", rng=random.Random(11))
    assert drawn.capability == "arbitration"
    assert drawn.route.id == "ANTHROPIC-STRONG"  # the quick route is under the floor
    routes = ROUTES.replace('"arbitration", ', "")
    bare = with_job(
        tmp_path / "no-arb",
        '[jobs.arbiter]\npool = [ { route = "ANTHROPIC-STRONG", weight = 1 } ]\n',
        routes=routes,
    )
    assert route.draw_for_job(bare, "arbiter").route is None


def test_the_arbiters_cross_family_preference_is_its_dial_not_its_role(tmp_path):
    pool = (
        'pool = [ {{ route = "ANTHROPIC-STRONG", weight = 1 }},\n'
        '         {{ route = "ANTHROPIC-MEDIUM", weight = 1 }},\n'
        '         {{ route = "OPENAI-STRONG", weight = 1 }} ]\n'
    )
    undialled = with_job(tmp_path, "[jobs.arbiter]\n" + pool.format())
    dialled = with_job(
        tmp_path / "dialled",
        "[jobs.arbiter]\nprefer_cross_family = true\n" + pool.format(),
    )
    excl = ("ANTHROPIC-STRONG",)
    # Undialled, the same-family medium route stays reachable (plan_runner
    # already records a shared-family arbiter as a mitigated degraded case).
    assert draw_ids(undialled, "arbiter", n=100, exclude=excl) == {
        "ANTHROPIC-MEDIUM",
        "OPENAI-STRONG",
    }
    # Dialled, the declared preference narrows it the way the roles are pinned.
    assert draw_ids(dialled, "arbiter", n=100, exclude=excl) == {"OPENAI-STRONG"}


# --- the CLI seam and the untouched registry path ---------------------------


def test_cli_job_arm_prints_the_draw_and_exits_nonzero_on_a_refusal(tmp_path):
    root = with_job(
        tmp_path,
        '[jobs.reviewer]\npool = [ { route = "ANTHROPIC-STRONG", weight = 1 } ]\n',
    )
    ok = run_py(
        [SCRIPTS / "agent_route.py", "--job", "reviewer", "--seed", "3"], cwd=root
    )
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert "drew ANTHROPIC-STRONG" in ok.stdout

    write_config(
        root,
        ROUTES.replace(ALL_CAPS, "[]")
        + '\n[jobs.reviewer]\npool = [ { route = "ANTHROPIC-STRONG", weight = 1 } ]\n',
    )
    bad = run_py([SCRIPTS / "agent_route.py", "--job", "reviewer"], cwd=root)
    assert bad.returncode == 1
    assert "agent_route: REFUSED - jobs.reviewer.pool" in bad.stderr


def test_the_job_layer_sits_beside_the_registry_path_not_on_top_of_it(tmp_path):
    # The cutover is a later slice: a repo with only agents.csv still routes by
    # phase, and a repo with only config.toml still draws by job. Neither path
    # reads the other's file.
    registry_csv = (
        "Id,Family,Model,Version,Tier,CmdTemplate,Env,Notes\n"
        "ANTHROPIC-OPUS-4.8,ANTHROPIC,opus,4.8,strong,claude -p {prompt},,\n"
        "OPENAI-GPT-5.2,OPENAI,gpt-5.2,5.2,strong,codex exec {prompt},,\n"
    )
    (tmp_path / "agents.csv").write_text(registry_csv, encoding="utf-8", newline="\n")
    registry, errors = route.load_registry(tmp_path / "agents.csv")
    assert errors == []
    chosen, _reason = route.select(
        ["OPENAI-GPT-5.2", "ANTHROPIC-OPUS-4.8"], registry, "strong"
    )
    assert chosen == "OPENAI-GPT-5.2"  # enable-list order, exactly as before

    # The job draw sees none of those ids — it reads docs/config.toml only.
    root = with_job(
        tmp_path,
        '[jobs.reviewer]\npool = [ { route = "ANTHROPIC-STRONG", weight = 1 } ]\n',
    )
    assert route.draw_for_job(root, "reviewer", rng=random.Random(1)).route.id == (
        "ANTHROPIC-STRONG"
    )
