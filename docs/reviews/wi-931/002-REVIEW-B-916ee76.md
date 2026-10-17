Reviewed: 916ee762f86596c6e06add264caa40f1b7c1e39c

**Verified.** Reading scope: the brief's range diff (2b2350add...916ee762f, excluding records and generated views), WI-931's spec, the cited registry rows (SR-238, LLR-026, TC-026, plus the LLR-270/TC-268 rows that name `TreeNotEnded`), and the rubric `docs/rubrics/kit-change-review.md`. Failure classes I hunted first, worst first: (1) fail-open, meaning a failed tree end, now an `OSError`, gets caught by an ordinary handler and turned into a continuing run or a session result; (2) silent wrong content, meaning spine cells that no longer match the code; (3) a regression in the kept ordinary kill (containment refusal, grandchild kill, the 10 s bound, unopenable member).
- **(1) No fail-open found.** `run_session`'s `except (OSError, ValueError)` launch conversion wraps only `_validate_prompt_transport` and `_spawn_session`. `_spawn_session` now catches `OSError` only, kills and reaps the never-run child through `with proc`, and re-raises. Nothing inside that `try` raises `TreeNotEnded` any more. The `finally` that calls `_kill_tree` sits outside it.
- **I re-checked the plan's P4 handler census myself.** I swept every `except` in `session_service`, `agent_loop`, `dispatch`, `plan_runner` and `coordinator_adjudicate`, plus every module that imports `agent_session` or `session_service`, and grepped for `Thread(`/`Executor`/`submit(`. Results:
  - `session_service.act` re-raises (bare `raise` after accounting).
  - `KeepWarmer._ping` still catches `TreeNotEnded` before its `BaseException` clause, so the carrier still works.
  - `coordinator_adjudicate` catches only `SigninRefused` and `BlackoutRefused` around `call`.
  - `plan_runner`'s `except OSError` (L311) wraps only the hat-template build.
  - Every other `OSError` handler in `agent_loop` and `dispatch` wraps file I/O, not a session.
  - The only thread that runs a session is the keep-warm ping's.
  - The census verdict ("none converts") holds.
- **The new assertion fails before the change.** I archived trunk 2b2350add into my scratch area, overlaid the lane's `tests/test_session_stdin.py`, and ran it. `test_a_tree_not_ended_within_the_bound_raises` FAILS on the new `isinstance(raised.value, OSError)` assertion (MRO `TreeNotEnded, BaseException, object`). The other 28 tests in the module pass there, so the kept tests pass both before and after on Windows.
- **I drove the real kill path through `run_session`.** A session child that spawns a python grandchild every 10 ms was run under a 2 s wall deadline, 5 times. Each run returned `(-1, timed_out=True)` in about 2.2 to 2.5 s with no `TreeNotEnded`. So dropping the late-spawn close and the PID-reuse check does not make the ordinary deadline kill flaky under processes joining the job during the kill.
- **Deletions confirmed.** A grep at base vs tip for `_end_launch` 2/0, `_end_suspended` 2/0, `_close_job` 2/0, `_JobBasicLimit` 2/0, `SetInformationJobObject` 4/0, and `except BaseException` 1/0. `_in_job`, `IsProcessInJob` and the query bit in `_MEMBER_ACCESS` are gone too. None of the six deleted tests or five deleted helpers is referenced anywhere live, TC-026's Method/Evidence included. Every remaining TC-026 Evidence test exists.
- **K1 (requirement text true and the right way round):**
  - SR-238's amended AcceptanceCriteria and Rationale equal the spec's text and match the code. A process that joins between the member snapshot and `TerminateJobObject` is terminated but not held, which is the stated millisecond residue. An interruption before `run_session`'s supervising `try` is outside the kill.
  - LLR-026's Detail substitutions are accurate. Its retained clause "an ordinary launch error still returns the session error" (lane D-004) is true and is what TC-026's Expected asserts.
  - TC-026's Expected matches the kept tests.
- **K2 and K3:**
  - K2: no SR cell gained an implementation carrier.
  - K3: every `Implements: … LLR-026` symbol in `agent_session.py` is in LLR-026's `code_symbol`. Every `code_symbol` entry exists in the module or `session_adapters.py` (`_codex_lastmsg_setup`, pre-existing). No Status flipped.
- **Requirement-row sweep.** I swept SR-238/LLR-026/TC-026 against the other rows that name the session job, process group or `TreeNotEnded` (LLR-270, TC-268). No contradiction: LLR-270 names the class, not its base.
- **Lint.** `ruff check` and `ruff format --check` on both changed Python files are clean.

**Done-when map:**
- No `_end_launch`/`_end_suspended`/`_close_job`/`_JobBasicLimit`/`SetInformationJobObject`/`except BaseException`; each present before: COVERED (grep base vs tip, above).
- The `OSError` assertion, failing before the change: COVERED (fails at 2b2350add, passes at tip).
- The kept ordinary-kill, idle/wall and WI-895 keep-warm tests pass unchanged: COVERED on Windows (258 passed across the three modules at tip; 28 others pass at base). POSIX: I did not observe it; lane D-002 routes it to a WSL run and to CI after push.
- Six tests and five helpers gone, TC-026 names none; `trace.py --strict-integrity` and `check_trajectory.py --strict` clean: COVERED (grep; both commands clean, below).
- The handler census recorded with a verdict per handler: COVERED (plan.md P4, re-checked above).
- SR-238/LLR-026/TC-026 carry the amendments: COVERED. Their blessing or approval at the checkpoint sitting, with its acts: PENDING. That sitting follows the counted rounds (lane D-001), so this diff carries no act. It is not a lane defect, but the landing must not proceed without it.
- `RESYNC_PACK.md` carries the entry: COVERED (see the MINOR on its anchor).
- Commit bar within its smoke budget, and REVIEW-A: not run by me (the brief forbids the smoke tier and the full suite here).

**Commands:**
- `git rev-parse HEAD` -> `916ee762f86596c6e06add264caa40f1b7c1e39c`
- `python lowprio.py python -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-17-coord/wi-931/r1-opus/wi-931 tests/test_session_stdin.py tests/test_session_keep.py tests/test_agent_loop.py` -> `258 passed in 142.11s (0:02:22)` (posix-shell gate unsatisfied, 0 tests skipped by it)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (935 work item(s), 815 done (87%), 30 cancelled, graph acyclic).` (pre-existing overlap WARNs only)
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=303 TC=317 orphans=0 integrity=0 … interface-findings=0 ac-advisories=1 paraphrase-advisories=3.` (the rewritten `docs/test/report.md` was byte-identical; `git status` clean afterwards)
- Pre-fix red check: `git archive 2b2350add` into `r1-opus/prefix`, overlay of the tip's `tests/test_session_stdin.py`, then `pytest -q tests/test_session_stdin.py` -> `1 failed, 28 passed` (FAILED `test_a_tree_not_ended_within_the_bound_raises`, AssertionError on the `OSError` isinstance)
- Real-path probe `r1-opus/probe/spawn_probe.py` (`run_session` over a child spawning a grandchild every 10 ms, 2 s wall, 5 runs) -> `ok 5`, each run `-1 True` in about 2.2 to 2.5 s
- `ruff check` / `ruff format --check` on `project-trajectory/scripts/agent_session.py` and `tests/test_session_stdin.py` -> `All checks passed!` / `2 files already formatted`

**Notes (no severity).**
- `_contain_in_job`'s docstring (project-trajectory/scripts/agent_session.py:318-320) still stresses that the job is published "BEFORE the resume". Its only reader for that order, the launch cleanup, is deleted, so the ordering is now harmless but unexplained. A one-line reason, or dropping the emphasis, would stop a reader hunting for its consumer.
- The new SR-238 AcceptanceCriteria narrows to "while the coordinator supervises a launched session". The unchanged Requirement cell still reads "When a declared deadline or coordinator interruption ends a session". That is the same refinement pattern the pre-change AcceptanceCriteria used, so it is not raised.

**Findings:**
- [MINOR] project-trajectory/scripts/agent_session.py:825 -> the edited comment was not reflowed: one line runs to 104 characters inside a block wrapped at about 79, against every other comment in the module (rubric: none; readability) -> rewrap the three-line comment block at the module's width -> @owner
- [MINOR] project-trajectory/RESYNC_PACK.md:8580 -> K4: the entry is anchored `[since 61ee4e165]`, the lane's previous base. Trunk has since moved to 2b2350add (D-005's rebase), and the pack's rule is that an entry applies when its `since` SHA is IN the adopter's range. So an adopter stamped at 8c72559ed, a4691ac23 or 2b2350add, none of which carries this change, would skip the entry and its `except OSError` advice -> re-anchor at the landing's parent when the lane lands (coordinator-cycle recipes "RESYNC: anchor the entry at the landing's parent"), today 2b2350add -> @owner

VERDICT: APPROVE findings=2
