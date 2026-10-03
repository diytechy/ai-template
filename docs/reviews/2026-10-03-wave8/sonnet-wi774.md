# Sonnet review — WI-774 (build/wi-774 at cca8c710)

Reviewer: Claude Sonnet 5.5 (read-only). Builder: Codex Sol (gpt-6.1-sol). Range
`f2bc66c1..cca8c710`. The spec is WI-773's exact adjudicator draft (spine-acts batch
O, revised at 83c2f292).

cca8c710 SOUND

**MINOR**
1. `gen_release_checklist.py:98`: a bare `import assumption_rules`, with no try/except
   fallback, unlike its neighbours. It works because `scripts/` is already on the
   path, and it matches `rejudge.py`, `observation_cadence.py` and `traj_parse.py`.
2. TC-055 `expected` moved from a `"""` string to a `"` string; the parsed value is
   identical.
3. The lane commit carries regenerated artifacts; deliberate, per the commit message.
4. The expected WARNs (an amended-SR citation, the trailer reconcile) clear at close.

**Verified**
- Exactness. A script compared every registry table across the range. Only the
  granted cells differ, and each equals the draft:
  - TC-055 `expected` (one clause);
  - TC-306, TC-309 and TC-310;
  - LLR-296 `detail`;
  - SR-215 `rationale`;
  - IF-200 `requestors` only.
  No Status changed, and the protected rows are untouched.
- Code. The production change reuses `is_observation_tc`, and
  `check_trajectory --strict` is clean with no cross-component finding.
- Tests. The new tests are real:
  - a zero floor;
  - three distinct ValueErrors;
  - an uncommitted policy change moving nothing;
  - both composer refusals;
  - the observation-only method;
  - no section when every row is omitted.
- The RESYNC entry is correct and anchored at the parent.

**Commands:** `pytest -q -n 2 tests/test_release_assumptions.py tests/test_rejudge.py
tests/test_assumption_observation_briefs.py tests/test_gen_release_checklist.py`:
`74 passed in 58.05s`; `check_trajectory.py --strict`: clean; `trace.py --strict`:
only LLR-292's `minimal`.
