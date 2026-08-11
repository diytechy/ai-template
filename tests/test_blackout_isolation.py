"""WI-428: the suite must not sleep on a policy dial.

`project-trajectory/process.toml.template` declares WI-148's real weekday
blackout window, `blackout = "12:00-19:00"`. A test scaffold seeded from that
template and handed to a session-driving fixture gives `agent_loop` a LIVE
window, which it correctly honors by sleeping — so on a weekday between 12:00
and 19:00 UTC the ten tests of `tests/test_agent_loop_critique.py` did not fail,
they never ran, and the runner reported green on the other 2232. "Full bar
green" was a function of the wall clock; a probe outside the window recorded the
module as "not reproduced ... flaky" on 2026-08-10.

This module guards the fix in both directions:
  - the SHIPPED default is unchanged and still live (so the guard is not
    guarding an already-empty dial — the vacuity trap);
  - no test scaffold a session-driving fixture builds carries a live window, at
    ANY clock time, and the guard that says so REDS on a planted one.

Every assertion here drives an INJECTED clock. A test that read
`datetime.now()` would re-create the defect it exists to prevent.
"""

import datetime

import pytest
from conftest import (
    BOOTSTRAP_IDIOM,
    KIT,
    LOOP_LAUNCH_IDIOM,
    ROOT,
    blackout_is_live,
    disable_blackout,
    live_blackout_scaffolds,
    load_script,
    module_launches_the_loop,
    process_key,
    set_process_key,
)

# This module PLANTS a live window on purpose (the guard's non-vacuity proof),
# so conftest's autouse sweep must not treat it as a session-driving module.
PLANTS_LIVE_BLACKOUT = True

agent_common = load_script("agent_common")

# The window the kit ships, and the one the defect ran on.
OWNER_WINDOW = "12:00-19:00"

# A full week of injected clocks: every weekday and weekend day, every hour,
# three minutes per hour (the edges and the middle). 504 samples — the point is
# that a disabled dial has NO time at which it sleeps, which one spot check
# cannot establish. 2026-07-13 is a Monday, so the range covers Mon..Sun.
WEEK = [
    datetime.datetime(2026, 7, 13 + day, hour, minute)
    for day in range(7)
    for hour in range(24)
    for minute in (0, 30, 59)
]


def sleeps_at(window):
    """Every sampled clock time at which `window` would make a coordinator
    wait, as a list of `(weekday, HH:MM, seconds)`. Empty means the dial can
    never stop this suite."""
    return [
        (now.strftime("%a"), now.strftime("%H:%M"), wake)
        for now in WEEK
        if (wake := agent_common.blackout_wake(window, now))
    ]


def test_the_kit_still_ships_the_owners_live_window():
    # The fix is to the SUITE, not to the policy. WI-148's default is a ruling
    # (the template's own comment forbids re-deciding it inside a refactor), so
    # this test pins that it survived — and it is what stops the rest of this
    # module from being a guard over an already-empty dial.
    text = (KIT / "process.toml.template").read_text(encoding="utf-8")
    assert 'blackout = "{}"'.format(OWNER_WINDOW) in text
    assert blackout_is_live(OWNER_WINDOW)
    # This repo's own declared policy is the same live window, unchanged.
    assert process_key(ROOT, "policies", "blackout") == OWNER_WINDOW
    # And it really does sleep — 35 weekday hours a week, up to 7 h at a time.
    sleeping = sleeps_at(OWNER_WINDOW)
    assert sleeping, "the window under guard must actually block, or this is theatre"
    assert max(wake for _, _, wake in sleeping) == 7 * 3600
    assert {day for day, _, _ in sleeping} == {"Mon", "Tue", "Wed", "Thu", "Fri"}


def test_a_seeded_test_scaffold_never_sleeps_at_any_clock_time(tmp_path):
    # The fix at its seam: conftest's seeding path is where a test scaffold gets
    # its docs/process.toml, and what it hands back must be inert at every hour
    # of every day. `critique_repo` reaches this through exactly this call.
    set_process_key(tmp_path, "policies", "review_rounds", 0)
    window = process_key(tmp_path, "policies", "blackout")
    # Present but disabled, using the dial's own documented disable form — a
    # DELETED key would also be inert, but it would stop testing the parse path
    # a downstream scaffold takes.
    assert window == ""
    assert not blackout_is_live(window)
    assert sleeps_at(window) == []
    # The dial the seeding path did NOT touch is still the template's.
    assert process_key(tmp_path, "policies", "privacy_review") == "require"
    assert live_blackout_scaffolds(tmp_path) == []


def test_the_guard_reds_on_a_planted_live_window(tmp_path):
    # Non-vacuity. Re-enable the dial in a seeded scaffold — the exact state the
    # defect shipped in — and the guard must NAME it; disable it again and the
    # guard must go quiet. A guard that cannot go red is the false green it was
    # written to remove.
    set_process_key(tmp_path, "policies", "review_rounds", 0)
    assert live_blackout_scaffolds(tmp_path) == []  # green

    set_process_key(tmp_path, "policies", "blackout", OWNER_WINDOW)  # planted
    caught = live_blackout_scaffolds(tmp_path)
    assert [(p.relative_to(tmp_path).as_posix(), v) for p, v in caught] == [
        ("docs/process.toml", OWNER_WINDOW)
    ]
    # What the guard caught is a scaffold that would really have slept: this is
    # the measured 2026-08-11 reproduction, on an injected clock (a Tuesday
    # 14:22 UTC), not a string comparison.
    assert (
        agent_common.blackout_wake(caught[0][1], datetime.datetime(2026, 8, 11, 14, 22))
        == 16680
    )

    disable_blackout(tmp_path)  # green again
    assert live_blackout_scaffolds(tmp_path) == []


@pytest.mark.parametrize(
    "value",
    ["", "   ", "00:00-00:00", "12:00-12:00", "not-a-window", "24:00-19:00"],
)
def test_the_documented_disable_forms_are_all_inert(value):
    # The scaffolds opt out through the dial's OWN semantics, so those semantics
    # are what must hold: an empty value and `start == end` disable, and a
    # malformed line is inert too (it warns at the loop's preflight, it does not
    # wait). Injected clocks, all week.
    assert not blackout_is_live(value)
    assert sleeps_at(value) == []


def test_the_guard_is_scoped_to_the_modules_that_launch_the_loop():
    # The autouse sweep in conftest is deliberately NOT suite-wide: a bootstrap
    # test asserting the shipped default carries "12:00-19:00" is checking the
    # right thing and must not be caught. Membership is derived from each
    # module's own source, so a new session-driving module joins by existing —
    # this pins both ends of that discriminator against a live example.
    import test_agent_loop_critique
    import test_bootstrap

    assert module_launches_the_loop(test_agent_loop_critique)
    assert not module_launches_the_loop(test_bootstrap)


def test_every_loop_launching_module_that_bootstraps_disables_the_window():
    # The recurrence mode the seeding fix alone does NOT cover: a fixture that
    # builds its scaffold with `bootstrap.py` gets the shipped live window
    # straight from the template, and conftest's seeding path never runs. Such a
    # module must call `disable_blackout` explicitly. Pre-emptive on purpose —
    # the autouse sweep only fires at teardown, which a sleeping test never
    # reaches.
    offenders = []
    for path in sorted((ROOT / "tests").glob("test_*.py")):
        text = path.read_text(encoding="utf-8")
        if LOOP_LAUNCH_IDIOM not in text or BOOTSTRAP_IDIOM not in text:
            continue
        if "disable_blackout(" not in text:
            offenders.append(path.name)
    assert not offenders, (
        "WI-428: these modules launch agent_loop.py against a scaffold they "
        "bootstrapped from the kit template, which ships a LIVE blackout "
        "window — the loop will sleep instead of running. Call "
        "conftest.disable_blackout(root) on the scaffold: " + ", ".join(offenders)
    )
