"""WI-122 — the meta commit-bar smoke tier stays honest.

The per-commit bar runs `-m smoke`; the full suite runs at slice/phase close
and in CI. These guard the two ways that split could silently rot into a false
green: a test landing outside both tiers, or a SLOW_MODULES entry going stale.
"""

from conftest import ROOT, SLOW_MODULES, smoke_tier_for


def test_tiering_is_total_smoke_or_slow():
    # smoke_tier_for maps ANY module stem to exactly one tier, so the collection
    # hook marks every collected test smoke-or-slow and never neither — the
    # "a new test is in the commit bar by default" invariant. The "in" examples
    # are in-process unit modules WI-281 keeps in the bar.
    assert smoke_tier_for("test_agent_common_harness") == "smoke"  # in
    assert smoke_tier_for("test_schedule") == "smoke"
    assert smoke_tier_for("test_brand_new_module_nobody_marked") == "smoke"
    assert smoke_tier_for("test_pre_push_hook") == "slow"  # heavy e2e: out
    assert smoke_tier_for("test_gen_trajectory") == "slow"  # WI-281 subprocess: out
    for stem in SLOW_MODULES:
        assert smoke_tier_for(stem) == "slow"


def test_wi277_split_modules_stay_slow():
    # The WI-277 guard. Splitting a slow monolith mints NEW module stems, and
    # `smoke_tier_for` defaults an unlisted stem to smoke — so a split that
    # forgets its SLOW_MODULES entry silently pulls a subprocess-heavy module
    # back into the per-commit bar (the WI-281 budget breaks quietly, since the
    # ratchet is blind to a single omission). Each stem below inherits its
    # parent's tier because it inherits its parent's cost class; a deliberate
    # re-tier of a genuinely in-process half is a separate measured decision
    # that must also update this list.
    for stem in (
        "test_trajectory_staged",
        "test_trajectory_arch",
        "test_trajectory_specs",
        "test_trace_rules",
        "test_trace_briefs",
        "test_agent_loop_routing",
        "test_agent_loop_policy",
        "test_traj_status",
        "test_traj_panels",
        "test_traj_views",
        "test_traj_render",
        "test_traj_render_sweeps",
    ):
        assert smoke_tier_for(stem) == "slow", stem

    # The literal above is hand-maintained, so it goes stale the next time the
    # gen_trajectory family gains a module. This half is DERIVED and needs no
    # editing: every `test_traj_*.py` on disk must be slow, because every one of
    # them drives the real gen_trajectory.py through run_py — the #1 cost in the
    # suite. (Kept inside this test rather than beside it so the WI-277 slice
    # guard "collected-test count is unchanged" stays a clean signal.)
    stems = sorted(p.stem for p in (ROOT / "tests").glob("test_traj_*.py"))
    assert stems, "vacuous — the traj split modules are gone"
    for stem in stems:
        assert smoke_tier_for(stem) == "slow", stem


def test_slow_modules_are_real_test_files():
    # A renamed/removed file must not leave a dead SLOW_MODULES entry silently
    # shrinking the slow set (slowing the commit bar back down unnoticed), and
    # nothing outside tests/ can be listed.
    for stem in SLOW_MODULES:
        assert (ROOT / "tests" / (stem + ".py")).is_file(), stem
