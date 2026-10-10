# WI-881 amendment adjudication: 009 at b025047

Anchor: `docs/archive/last_approved` (system-requirements.toml at 04956829; low-level-requirements.toml at b3cfae9b; test-cases.toml at 04eaa891). I read the lane's rounds 4 and 5 (`b31c3d2a`, in which the launch owns the child until it hands it over; `eb81debd`, `TreeNotEnded`), decisions D-006 and D-007, the code of `agent_session._spawn_session`, `_end_launch`, `_end_suspended` and `TreeNotEnded`, and the reconciled rows in `b0250473`.

The code is sound. On Windows, any exception after `Popen` returns ends what the launch owns: the suspended child, or the job once it is published. A cleanup that cannot end the tree raises `TreeNotEnded`, a `BaseException` that no `except OSError` or `except Exception` converts into a session result. `session_service._launch`'s caller records it and re-raises. The one sibling that swallows it, the keep-warm `_ping` thread, is filed as WI-895 (D-007). `tests/test_session_stdin.py` gave 36 passed here, no skips.

The findings below are about the TEXT. Round 4 recorded a residual, but only in SR-238's Rationale, and three cells that state the guarantee still contradict it.

- [MEANING] SR-238 Rationale -> the rationale argued the bounded guarantee and its recorded exclusions (a descendant that leaves the group, a service-started process outside the job, a non-reaping PID 1, a member denying SYNCHRONIZE) -> the same, PLUS why stopping is SN-006's cannot-proceed case, and a new exclusion: "An interruption inside platform process creation, before the child reaches the coordinator, is not covered" -> not the same. The cell is a rationale, but its new sentence removes a case from what the row guarantees. A reader acting on the old row would expect an interruption at any point to leave no session child alive. The new row says one window is outside the guarantee: on POSIX a running child is lost (D-006). NOT BLESSED. The exclusion is honest and its cost argument (D-006) is sound, but SR-238's own AcceptanceCriteria, unchanged, still promises that at a coordinator interruption "the direct session child ... ha[s] ended". The earlier exclusions sat inside the AC's stated domain ("every process still in the session process group ... or session job"), so they did not contradict it. This one removes the direct child, which the AC names outright. The row now states a guarantee in one cell and withdraws part of it in another, and only the Rationale is true.
- [MEANING] LLR-026 Detail -> the bounded tree kill: on a deadline or an interruption, every process in the group or job ends; the Windows close, hold and terminate order; the 10 s raise; an uncontainable child as a session error -> the same, PLUS: a failure to end the tree, or to show that it ended, raises `TreeNotEnded`, which no ordinary handler converts into a session result, while an ordinary launch error still returns the session error -> not the same: a new error contract. A correct old implementation could return a cleanup failure as a session result. NOT BLESSED this sitting, though the new clause itself is right and true of the code. The Detail still says, unqualified, that "an interruption ... ends every process in the session process group on POSIX or session job on Windows". It does not state the launch-window residual the row's parent now records, in which a POSIX child interrupted inside `Popen`'s exec handshake is lost. The Detail is where the design boundary belongs ("the launch owns the child from when `Popen` returns"), and that is the gap the lane has to close.
- [MEANING] TC-026 Expected + Method -> the bounded descendants have ended with no grace period, an interruption ends them as a deadline does, plus the remaining kill conditions -> the same, PLUS: "an interruption during launch or supervision setup ends the child as one during the wait does", and a failure to end or verify the tree raises `TreeNotEnded` rather than returning a session result, while an ordinary launch error still does. The Method adds six tests -> not the same: new acceptance conditions and verification. NOT BLESSED this sitting. The six new tests are well aimed, and each passes here. But "an interruption during launch ... ends the child" is unqualified, and the recorded residual is an interruption during launch, inside platform process creation, that does NOT end the child. The tests drive only the kit's side of the boundary (before the job, after the resume, in supervision), which is correct; the Expected cell claims more than they show.

VERDICT: MEANING rows=3

Aftermath: no row is blessed, so nothing is re-attested. All three rows change together, and the drift stays visible until the lane answers the Dispositions below.

### Answered in the lane

The return below was answered in the lane: Terra carried the launch-window residual into SR-238's AcceptanceCriteria, LLR-026's Detail and TC-026's Expected (`d90ac640`), re-sat at sitting 010, which blessed all three rows.

WI-881 is an ordinary work lane, and intake mints drafts only from adjudication-kind specs. This draft is therefore the lane's to answer before its merge, written in the shape intake reads:

```toml
title = "WI-881 return: the launch-window residual is stated only in SR-238's Rationale; its AC, LLR-026 and TC-026 still claim the case"
safety_class = "ordinary"
sr_refs = ["SR-238"]
```

Carry D-006's residual into every cell that states the guarantee, so the four agree. No code changes:
- **SR-238 AcceptanceCriteria:** bound the interruption arm to a child the launch has handed to the coordinator, for example "at a coordinator interruption once the platform's process creation has returned the child". Keep the Rationale's sentence as the argued exclusion.
- **LLR-026 Detail:** state where ownership starts. The launch owns the child from when `Popen` returns; an interruption inside `Popen` is outside the kill, and on POSIX a child interrupted there is lost.
- **TC-026 Expected:** change "an interruption during launch or supervision setup ends the child" to the kit-side windows the tests actually drive: before containment, after the resume, and during I/O setup or the deadline handoff.

Then re-submit SR-238, LLR-026 and TC-026 together. The `TreeNotEnded` clauses, the SN-006 sentence and the six new tests need no change.
