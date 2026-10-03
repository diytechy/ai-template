# Sonnet review — WI-748, fix round 1 (build/wi-748 at 630150c3)

Reviewer: Claude Sonnet 5.5 (read-only). Range `72b035e5..630150c3`, and the lane `83db9d75..630150c3` as the landing candidate.

630150c3 SOUND

**BLOCKER:** none. **MAJOR:** none; both round-1 majors resolved.
- MAJOR 1: `_observe_compaction` (`session_keep.py:719-748`) infers only from `observation["prompts"]` (rollout per-request counts); exec totals are only stored; no readable rollout means no inference. `test_codex_multi_request_exec_turn_then_smaller_turn_cannot_infer` (15154+15224, then +15717, no rollout) asserts nothing inferred; traced by hand to fail on 72b035e5.
- MAJOR 2: `pair = [previous] + prompts[cursor:]`, `inferred = any(cur < prior ...)` (`session_keep.py:728-731`); cursor `record["rollout_requests"] = len(prompts)`. 35911 -> 15717 -> 18200 infers; a pure rise infers nothing; a legacy record learns without rechecking. Rotation/truncation (empty slice, cursor reset), new thread/reset (fresh record, no cursor), legacy record and unreadable rollout all hold.

**MINOR**
1. `session_keep.py:35-37` store docstring omits the new `rollout_requests` cursor.
2. `input_total` (`session_keep.py:739`) is now write-only (LLR-290 says so honestly; dead state).
3. A first fresh call with no readable rollout leaves no cursor, so the next call takes the legacy learn path and its own drop goes unchecked: a missed inference, never a false one, per the legacy rule.

Round-1 minors: fresh clamped `max(0, total - cached - written)`, LLR-268/TC-264 hedge cache-write inclusion "not yet verified live", a `write=4000` clamp test; `compaction()` gets `os.environ if env is None else env` (`session_service.py:283-289`), tested. Cells: LLR-268 detail and TC-264 method (Approved) match the code; LLR-290 and TC-303 (Drafted) match; no other attesting cell changed over the lane; RESYNC updated.

**Commands:** `pytest -q -n 2 tests/test_session_adapters.py tests/test_session_service.py tests/test_session_keep.py`: `123 passed in 28.82s`; git log/diff reads.
