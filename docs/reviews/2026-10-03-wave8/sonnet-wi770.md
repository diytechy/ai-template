# Sonnet review — WI-770 (build/wi-770 at 719dcaeb)

Reviewer: Claude Sonnet 5.5 (read-only). Builder: Codex Sol (gpt-6.1-sol). Range
`f3f188a2..719dcaeb`. The spec is WI-766's exact adjudicator draft, cross-reviewed
as batch N r1/r2.

719dcaeb SOUND

**MINOR**
- `tests/test_rejudge.py:241-253`: the two new assertions call `checkpoint_drafts`
  twice more, and the trigger one reads `not trigger or X in ...`. A local `ctx`
  would be clearer. Not a defect.
- `RESYNC_PACK.md:6675`: the anchor `[since f3f188a2]` follows the convention.
  Trunk has since gained `00467fc7`, which touches no kit file; re-anchor at the
  landing if wanted. *(Re-anchored at the landing.)*
- Expect conflicts in the generated `docs/id-watermark`, `docs/stage` and
  `PROJECT_STATE.html` at the merge.

**Verified:**
- Only the draft's 19 cells and the new TC-311 row changed.
- TC-036, TC-055, TC-209, TC-210, TC-211, TC-279, TC-307, TC-261 and LLR-265
  are md5-identical.
- No Status flipped (the only `status` line is TC-311's `Drafted`), and no
  production code changed.
- TC-247's assertions match `rejudge.py`'s `_context` and `explain()`. The
  rubric one has a real red ("(not declared)").
- The `cadence_repo` change is limited to TC-002's `Rubric`.
- The doc pin reads the skill body. Its "required" occurs only in the new
  paragraph.
- The skill paragraph is placed and worded exactly as drafted, and the mirrors
  are byte-identical.
- The RESYNC entry is new, last and actionable.
- TC-311 is true of its test (Integration/Full/Yes; LLR-294, IF-269).
- The reworked rows read true against the code.
- `trace.py --strict` no longer prints SR-215's CRITIQUE-instrument advisory.

**Commands:** `pytest -q -n 2 tests/test_rejudge.py tests/test_skills_index.py
tests/test_intake.py`: `162 passed in 88.39s`; `check_trajectory.py --strict`:
clean (767 work items).
