+++
id = "WI-428"
title = "The full-suite bar is a function of the wall clock: tests/test_agent_loop_critique.py (10 tests) does not RUN on a weekday between 12:00 and 19:00 UTC — it SLEEPS. conftest.set_process_key(seed=True) seeds a test scaffold's docs/process.toml from project-trajectory/process.toml.template, which declares blackout = \"12:00-19:00\"; critique_repo is the session-driving fixture that calls it, so the agent_loop under test correctly honors a LIVE policy window and waits it out (measured blackout_wake(\"12:00-19:00\", 14:22Z) = 16650 s). The suite therefore reports green as a function of time-of-day, and it has already misled this program once — docs/repo-lock.md §5 records this module as 'not reproduced, 2026-08-10 ... environmental or flaky'. It is not flaky; it is deterministic in UTC time-of-day. Make the kit's own test scaffolds immune (a seeded session-driving scaffold carries a DISABLED blackout, per the dial's own documented semantics), find EVERY fixture with this exposure rather than assuming critique_repo is alone, and add a GUARD that reds if a session-driving scaffold ever inherits an enabled window again. The blackout dial's own behavior must still be really tested, fast, on an injected clock. DO NOT change blackout = \"12:00-19:00\" in process.toml.template or docs/process.toml — WI-148's default is a ruling, and re-deciding it is the owner's call, tabled separately. This row makes the SUITE honest, not the policy different."
workstream = "scripts"
specref = ""
buildtier = "medium"
safety_class = "ordinary"
+++

## Context

WI-427 surfaced this as its finding 1 and deliberately did not fix it: *"a bar
that silently blocks for a third of the day teaches people to skip it."* Its
2227/5 figure was measured with this module **excluded**, so the program's
headline suite number currently describes 2232 of 2242 collected tests.

**The class matters more than the ten tests.** This repo exists to eliminate
false greens (SN-008: a green must not hide a skipped check). A suite whose
membership depends on the wall clock is the purest form of that failure —
nothing errors, nothing is reported skipped, the ten tests simply never run and
the runner reports success on the other 2232. The earlier "not reproduced"
verdict is the predictable consequence: a probe outside 12:00–19:00 UTC passes.

**The boundary is the point.** The template's `blackout = "12:00-19:00"` is
WI-148's deliberate default, recorded in the template's own comment as a MOVE
that is not an occasion to re-decide the value. A test scaffold inheriting a
live operational policy is a *test-harness* defect, not a policy question. The
fix belongs in the seeding path, and the dial's own semantics already supply the
disable form (empty value, or `start == end`) — so the scaffolds opt out using
the documented contract rather than a special case.

**A seeding change alone is a one-off.** The durable deliverable is the guard:
a test that reds when a session-driving scaffold carries an enabled window,
proven non-vacuous against a planted defect.
