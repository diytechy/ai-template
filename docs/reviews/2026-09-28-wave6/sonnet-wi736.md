<!-- Claude Sonnet (read-only) review of WI-736, build/wi-736 a0445a80..c4dcc13f. Built by Codex Sol; committed by the coordinator. -->

c4dcc13f SOUND

BLOCKER: none

MAJOR: none

MINOR:
- **The gemini fixture carries `"session_id"`.** In `tests/test_session_service.py::test_gemini_usage_is_recorded_with_unread_values_empty` (about `:166`), the gemini-shaped payload includes `"session_id": "example-session"`. `_claude_usage` (`session_adapters.py:293`) reads it into `gen_ai.conversation.id`, so that column is filled incidentally.
  - The draft's clause enumerates only the runner, the provider name, the raw usage and the token counts, and the test asserts exactly that set. So this is not a spec violation.
  - It is a smell for anyone reusing the fixture. *Coordinator: accepted as recorded.*

**Replacements, verified verbatim** by a programmatic diff of the draft against `a0445a80` and HEAD:
- every "before" string existed and is gone, and every "after" string is present verbatim;
- there are three hunks in all (SR-222, SR-227 and TC-264), and nothing else in either registry moved.

**The prohibitions held:**
- no change under `project-trajectory/`;
- no LLR change;
- SR-222, SR-227 and TC-264 are still Drafted.

**The new test** (`:166-183`) asserts `cli`, `gen_ai.provider.name`, `raw-usage`, the `USAGE_COUNT_KEYS` and `fresh-input-tokens` empty, with the full column set, for a gemini argv under `PlainAdapter`. It would fail if any of those began to fill.

**The texts are true of the code, with one `shall` each:**
- SR-222 matches `PlainAdapter.cli = ""` and the empty unread counts.
- SR-227's whole-write clause matches `store_lock` (`session_keep.py:177`) and `_write_whole` (mkstemp and `os.replace`, `:249-255`). Its keep-warm clause matches the keep-warm machinery.

**Run:** `python -m pytest -q -n 2 tests/test_session_adapters.py tests/test_session_service.py tests/test_session_keep.py -p no:cacheprovider` → **105 passed in 272.95s**.
