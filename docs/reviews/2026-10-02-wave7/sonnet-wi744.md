# Sonnet review — WI-744 (build/wi-744)

Reviewer: Claude Sonnet 5.5 (Agent subagent, read-only). Builder: Codex Sol (gpt-6.1-sol). Range `2e13b2bd..9d19e88d`.

9d19e88d SOUND

**BLOCKER:** none

**MAJOR:** none

**MINOR**
- `project-trajectory/scripts/agent_session.py:72` (`split_cmd`) also runs inside `build_argv`, so the new `except ValueError` in `KeepWarmer.__init__` also skips a row whose template is malformed (an unbalanced quote). Consistent with the commit's "a route that cannot launch cannot be pinged", and the row still fails at its own launch; acceptable, not a defect. (Coordinator: `shlex.split` does raise `ValueError` on an unclosed quote, so the reading holds. Accepted as built; no fix round.)

**Checks**
1. Code change: a pure restructure of the route comprehension into a loop with try/except around `build_argv` only. `build_argv` raises `ValueError` only from `_validate_prompt_transport` (`agent_session.py:152-156`). `adapter_for` and `bounds_one_turn` errors still surface. Prompt-transport check and `bounds_one_turn` unmodified; retention, resume, drain and retirement untouched.
2. Test (`tests/test_session_keep.py:533-551`): monkeypatches the module global `build_argv` looks up at call time (`agent_session.py:184`), so the refusal is forced on every platform and the test is not vacuous. The unfixed failure was reasoned, not run; the builder recorded it red before the fix.
3. Scope: only `session_service.py` (+9/-8) and `tests/test_session_keep.py` (+21). No row cell changed.

**Commands:** `git show 9d19e88d`; `git diff --stat 2e13b2bd 9d19e88d` (2 files, 30+, 8-); in the worktree with `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt`, `pytest -q -n 2 -p no:cacheprovider tests/test_session_keep.py`: `50 passed in 10.80s`.
