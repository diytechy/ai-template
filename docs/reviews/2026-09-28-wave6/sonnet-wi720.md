<!-- Claude Sonnet (Agent-tool subagent, model "sonnet", read-only) review of WI-720, build/wi-720 4dd6827d..9a7c063d. Built by Codex Sol; committed by the coordinator (the builder's sandbox refused git metadata writes). -->

9a7c063d SOUND

BLOCKER: none

MAJOR: none

MINOR:
- `docs/requirements/system-requirements.toml`, SR-227.rationale. Item 3 asked only that the first clause be restated. The builder also reworded the trailing comparison: "resuming a session by id costs about what a standing process would under the provider's hour-long prompt cache" became "resuming a session by id uses the provider's prompt cache". That drops the "hour-long" figure and the standing-process comparison, neither of which was flagged as history. The new text is still true, just less specific. It is not a spec violation (same in-scope cell). *Coordinator: accepted as still true; the first-approval adjudication judges the row.*

Per-item verification (spec `WI-720`, commit 9a7c063d):

1. **SR-222.requirement / acceptance_criteria:** done, and true against the code:
   - `session_service.py:183` fills `provider` from `row.family` (`:531`);
   - `ClaudeAdapter.provider="anthropic"` (`:349`) and `CodexAdapter.provider="openai"` (`:453`);
   - `OpencodeAdapter` names no provider (`:625`).

   The obligation set, SR-Refs and Verifies are unchanged.
2. **SR-222.rationale:** "was the owner's choice" is gone. The pinned-revision argument is kept.
3. **SR-227.rationale:** done, in present voice, with no "extreme" and no past observation. See the minor finding.
4. **LLR-266.detail / rationale:** match the spec.
5. **LLR-267.rationale:** "34,836%" is gone. Matches the spec exactly.
6. **LLR-268.detail / rationale and the IF-245 docstring** (`session_adapters.py:33-34`):
   - the raw usage is the whole result event line, verbatim, which `_claude_raw` (`:262-269`) returns;
   - the reasoning count and response model match `_claude_usage` / `_claude_model` (`:272-321`);
   - `test_claude_usage_is_mapped_to_the_pinned_otel_names` passed.
7. **LLR-269.rationale:** now the standing consequence of one launch path per role.
8. **TC-262.expected:** true against `CodexAdapter.final_text` (`:440-442`) and `OpencodeAdapter.final_text` (`:592-611`).
9. **TC-264.expected:** the two conditions are stated. Matches the code.
10. **TC-268:** the assertion is pinned to `["keep-warm: skipped (a ping is in flight)"]`. It is deterministic in this fixture (`session_service.py tick()` `:484-499`), and the Method's "says so" now matches its evidence.
11. **LLR-270.rationale:** "exactly a fresh session's". Matches the spec exactly.

**Scope:**
- Only the named cells changed.
- TC-263, TC-265, TC-266 and TC-267 are absent from the diff.
- All ten rows stay Drafted.
- No Hat-Refs, SN-Refs, Boundary-Refs, Verifies, tier or level moved.

**Run:** `python -m pytest -q -n 2 tests/test_session_adapters.py tests/test_session_service.py tests/test_session_keep.py -p no:cacheprovider` → **103 passed in 60.67s**. `trace.py --strict-integrity` was not run by the reviewer. The worktree was clean after the review.
