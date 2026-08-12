"""WI-428/WI-433: the suite must not sleep on a policy dial.

`project-trajectory/process.toml.template` used to declare WI-148's real weekday
window, `blackout = "12:00-19:00"`. A test scaffold seeded from that template and
handed to a session-driving fixture gave `agent_loop` a LIVE window, which it
correctly honors by sleeping — so on a weekday between 12:00 and 19:00 UTC the
ten tests of `tests/test_agent_loop_critique.py` did not fail, they never ran,
and the runner reported green on the other 2232. "Full bar green" was a function
of the wall clock; a probe outside the window recorded the module as "not
reproduced ... flaky" on 2026-08-10.

WI-433 removed the source: the owner ruled the template SHIPS DISABLED
(`"12:00-12:00"`, `start == end`), keeping the shape so an adopter can see what
a window looks like without inheriting one. That moves this module's job, and
the move is where the vacuity trap lives — a guard whose subject no longer
exists passes for the wrong reason. So the guard now holds four things, and the
last two are what keep it honest:

  - the SHIPPED default is disabled, and the disabling is REAL: no wait at any
    hour of any day across a full week of injected clocks;
  - the shipped value still PARSES as a window, so the form stayed legible;
  - a POPULATED window really does block — 35 weekday hours a week, up to 7 h at
    a stretch — so the machinery under test is proven live, not merely unused;
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

# The window the defect ran on — the kit author's own, and the value the
# template shipped until WI-433. It is no longer what a scaffold receives; it is
# kept here as the POPULATED window every non-vacuity probe in this module is
# driven against.
OWNER_WINDOW = "12:00-19:00"

# What the template ships now: a window whose start equals its end, i.e. the
# dial's own documented disable form, written in window SHAPE rather than as an
# empty string so an adopter reads the format off the line they are editing.
SHIPPED_WINDOW = "12:00-12:00"

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


def test_the_kit_ships_the_dial_disabled_and_the_disabling_is_real():
    # WI-433, half one: what a fresh scaffold receives. A string comparison
    # alone would be the vacuity trap in a new costume — "the template says
    # 12:00-12:00" is not the claim; "an adopter who never touches this line is
    # never stopped by it" is. So the value is read off the shipped file and
    # then DRIVEN, at every hour of every day of a week.
    text = (KIT / "process.toml.template").read_text(encoding="utf-8")
    assert 'blackout = "{}"'.format(SHIPPED_WINDOW) in text
    assert not blackout_is_live(SHIPPED_WINDOW)
    assert sleeps_at(SHIPPED_WINDOW) == []
    # The SHAPE survived the disabling: it still parses as a window, which is
    # the whole reason it is not simply `""`. An adopter reads the format off
    # the line they are about to edit.
    assert agent_common.parse_blackout(SHIPPED_WINDOW) == (720, 720)


def test_a_populated_window_still_blocks_so_the_machinery_is_proven_live():
    # WI-433, half two, and the load-bearing half. Once the shipped dial is
    # inert, every other assertion in this module could pass over machinery that
    # had quietly stopped working. This is the one test that would notice: the
    # window the defect actually ran on must still stop a coordinator — 35
    # weekday hours a week, up to 7 h at a stretch, and never at a weekend.
    assert blackout_is_live(OWNER_WINDOW)
    sleeping = sleeps_at(OWNER_WINDOW)
    assert sleeping, "the window under guard must actually block, or this is theatre"
    assert max(wake for _, _, wake in sleeping) == 7 * 3600
    assert {day for day, _, _ in sleeping} == {"Mon", "Tue", "Wed", "Thu", "Fri"}
    assert len(sleeping) == 5 * 7 * 3  # five weekdays x seven hours x three samples


def test_this_repos_own_dial_is_deliberately_not_pinned_to_a_value():
    # The template stopped carrying the owner's window; this repo still declares
    # one, and it is the OWNER'S to set — WI-433 was explicitly scoped out of
    # docs/process.toml. So this pins the two things that are the kit's business
    # and not the owner's: the key EXISTS (a deleted key reads as disabled with
    # nothing saying so), and whatever it holds is a value the shipped parser
    # understands.
    value = process_key(ROOT, "policies", "blackout")
    assert isinstance(value, str), "docs/process.toml must still declare the dial"
    assert value == "" or agent_common.parse_blackout(value) is not None


def test_the_shipped_comment_offers_the_window_without_claiming_a_vendor_fact():
    # The wording constraint the ruling attached to this change, mechanized so
    # it cannot erode. The 12:00-19:00 hours may be OFFERED to an adopter — they
    # are the kit author's operating observation — but the kit has no source for
    # any vendor's aggregate load and must not read as asserting one.
    text = (KIT / "process.toml.template").read_text(encoding="utf-8")
    block = text.split("[policies]", 1)[1].split('blackout = "', 1)[0]
    assert "the kit's author observes" in block, (
        "the offered window must be framed as one person's observation"
    )
    assert "NOT a measurement of any vendor's load" in block
    for vendor_claim in ("Anthropic", "Claude models see", "usage peaks"):
        assert vendor_claim not in block, (
            "the shipped comment must not assert a vendor-load fact: " + vendor_claim
        )


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
    # builds its scaffold with `bootstrap.py` copies whatever the template
    # declares, and conftest's seeding path never runs. Such a module must call
    # `disable_blackout` explicitly. Pre-emptive on purpose — the autouse sweep
    # only fires at teardown, which a sleeping test never reaches.
    #
    # WI-433 made the template's window inert, so this is now the SECOND line of
    # defence rather than the first. It is kept, not dropped: it is the rule that
    # holds if the shipped default is ever repopulated, and the day that happens
    # is exactly the day nobody is looking at this file.
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
