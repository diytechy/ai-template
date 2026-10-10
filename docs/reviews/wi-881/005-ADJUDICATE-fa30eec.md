# WI-881 amendment adjudication: 005 at fa30eec

Anchor: `docs/archive/last_approved` (test-cases.toml at ad91c7b4). Read with sitting 004 (`004-ADJUDICATE-0020593.md`), which returned TC-026 for one defect: its rewritten Expected had dropped SR-026's outcome. The lane's answer, `fa30eece`, changes only TC-026's Expected, restoring "Satisfies SR-026 AcceptanceCriteria" at the head of the cell. The rest of the row is byte-identical to what sitting 004 judged.

- [MEANING] TC-026 Expected + Method -> Expected: "Satisfies SR-026 AcceptanceCriteria"; Method: the agent-loop suite, headless resume without blocking, a stdin-delivered prompt and a large prompt untruncated -> Expected: SR-026's acceptance, PLUS that the bounded descendants have ended when the coordinator continues with no grace period, an interruption ends them as a deadline does, an uncontainable child errors before it runs, no process enters the job once the kill begins, and an unopenable member or an overrun past 10 s raises. Method: the same SR-026 cases, PLUS seven named real-process tests (deadline, interruption, containment refusal, overrun, a member spawned during the kill, an unopenable member, and the idle bound) -> not the same: new acceptance conditions and new verification owed, for SR-238 and LLR-026's new arm. BLESSED.
  - **SR-026's outcome is back.** Expected again carries the pointer sitting 004 named as sufficient, so every requirement in `Verifies` (SR-026, SR-238, LLR-026) has its observable outcome in Expected. That was the one finding.
  - **Every SR-238 and LLR-026 clause is covered by a named test.** Sitting 004 confirmed each clause against the code, and `tests/test_session_stdin.py` gave 29 passed on this Windows box.
  - **The chain above is settled.** Sitting 004 blessed LLR-026 (act at `b3cfae9b`) and approved SR-238 (`04956829`), so nothing above this row is open.

VERDICT: MEANING rows=1

Aftermath: the TC rung is released and the row is blessed, so the act re-attests TC-026 in its own commit.
