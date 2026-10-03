# Sonnet review — WI-657's path trigger (build/wi-657 at 9c472f7b)

Reviewer: Claude Sonnet 5.5 (read-only). Builder: Codex Sol (gpt-6.1-sol). Range `83db9d75..9c472f7b`. (The coordinator stopped the first, uncommitted build before review: the hook would have refused every script commit on trunk's red ratchet, and it ran smoke at commit time; the fix round answered both.)

9c472f7b SOUND

**BLOCKER:** none. **MAJOR:** none.

**MINOR**
- `check.py` ~1296-1307: the comment block introducing `RETIRED_STAGE_ALIASES` remains though the table moved to `kitlib/config.py`; dead prose.
- Import ordering/style in `check.py` (`_LEGACY_GATES_WARNED` re-export, `import fnmatch` placement) and `kitlib/config.py` (`from . import ladder`).
- The hook runs `--path-triggered` on every commit here; complexity and readability are rung-selected at DevStg-Impl, so they run even with no declared path changed (~3.6 s): the owner's "rung OR path" ruling, not a defect.
- dupes-census reads 5/5/52 against 0/0/0 on this lane; warn-only, never blocks.

**1. Selection:** rung OR path in `resolve_plan` / `_path_matches` (~1465-1485); unknown change (git failure, empty staged diff off a lane, empty lane-base diff, unresolvable base) runs the step; `--no-renames` yields both rename sides; deletions kept; a step without paths is rung-only and never reads changes; the lane base (`agent_common.default_base`) can only over-include, so it fails toward running.
**2. Hook:** only complexity, dupes-census and readability; smoke excluded and tested; `set -e` blocks only on a real failing step (dupes-census always 0); an adopter with no declared paths gets a no-op (pinned); the shipped template arms nothing new.
**3. Baseline:** 8 rows re-pointed with unchanged numbers; 5 new + 2 growth rows each with a dated reason naming the introducing WI; no other row changed; enforce OK; the deferred-import window 29 -> 30 honest (`check.py` imports `agent_common` lazily to keep its kitlib-only floor).
**4. Rows/docs:** LLR-195 and LLR-206 amendments match the code, the ARMED wording is the owner's ruling; IF-267/LLR-291/TC-304 well formed, TC-304 drives the real functions; rule stated once in PROCESS.md and PROCESS_OPTIONS.md; RESYNC entry present.

**Commands:** `pytest -q -n 2 tests/test_step_path_trigger.py tests/test_complexity_ratchet.py tests/test_import_layers.py tests/test_dogfood_sync.py tests/test_check_harness.py`: `112 passed, 2 skipped in 53.22s`; `check_complexity --mode enforce`: OK (208); `check.py --path-triggered`: PASS (3.6 s); `check.py --run-steps approval-fresh,approval-immutable,held-status,derived-stage,registry-integrity`: PASS.
