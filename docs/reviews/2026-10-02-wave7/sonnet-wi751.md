# Sonnet cross-review — WI-751 first-approval act (build/wi-751 at da8c3f13)

Reviewer: Claude Sonnet 5.5 (read-only). Adjudicator: an independent Claude Opus 5.5 session. Commits `83db9d75..da8c3f13` (verdict `79a638cc`, act `da8c3f13`).

da8c3f13 SOUND

**BLOCKER:** none. **MAJOR:** none.

**MINOR**
- The Dispositions draft's added assert (after `path.unlink()` in `test_examples_and_absent_registry_are_inert`) looks like a duplicate of the existing one before it, but is the only one covering the ABSENT registry; correct as drafted.
- The adjudicator's note that IF-265's "refusing unreadable data" is `spine_carrier.load`'s existing behaviour was not checked; it does not change the verdict.

**Checks.** LLR-288 true of `schedule.py` (`load_wis` ~305-340 attaches pending gates only, skips `-000`, sorts by id; `hard_preds_satisfied` 481 refuses a gated queued row; `_disposition` 777 reports `blocked:open-item-pending:<id>` per gate; a ruled gate drops out with no row edit), under approved SR-148. LLR-289 true of `check_trajectory.py:927` (`open_item_wi_ref_findings` skips `-000`, checks every status, resolves against live and archive rows via `kitlib/registry.py:419`; wired at 3312). TC-301's evidence exists and passes. TC-302's return: both gaps real (Method at `test-cases.toml:3037` omits archive resolution; no checker call with the registry absent); the draft quotes the old text byte for byte and adds the right archived-work test. The act: exactly three `status` lines flipped (LLR-288, LLR-289, TC-301), TC-302 Drafted, `acts.toml` seq 15 well-formed, no other attesting cell edited. The two uncounted observations are not findings for this act.

**Commands:** `check_trajectory.py --strict`: clean (748 WIs); `trace.py --strict-integrity`: orphans=0 integrity=0 drafts=3; `pytest -q -n 2 tests/test_open_item_readiness.py tests/test_schedule.py tests/test_baseline_snapshot.py`: `182 passed in 135.16s`.
