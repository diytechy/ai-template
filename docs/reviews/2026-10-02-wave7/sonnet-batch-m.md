# Sonnet cross-review — spine-acts batch M (WI-762, WI-763; build/batch-m at 8415796a)

Reviewer: Claude Sonnet 5.5 (read-only). Adjudicator: an independent Claude Opus 5.5 session, one sitting over two kit-composed briefs, one combined act (seq 20). Commits `fafb0ff2..8415796a`.

8415796a SOUND

**BLOCKER:** none. **MAJOR:** none.

**MINOR**
1. SR-006 is a thin anchor for LLR-291. For the reading: SR-006 requires running "the required steps of the gate" (`system-requirements.toml:6,8`); a path trigger only adds runs, and `resolve_plan` keeps the rung test (`check.py:1470`). Against: its acceptance says "a tier selection runs exactly the declared step subset" for "the gate that must next be passed", and never mentions change-based selection or the hook's `--path-triggered` bar. Recommendation: amend SR-006 with one clause ("a step may also declare changed-path triggers that select it below its rung") or give LLR-291 its own SR parent. Not blocking: the owner ruled the placement 2026-10-02. (Coordinator: surfaced to the owner; requirement-tier text is the owner's to approve.)
2. `tests/test_step_path_trigger.py:11-18` never exercises comma-separated patterns (`kitlib/config.py:266`) or a wrong-case path proving case-sensitivity (`fnmatchcase`, `check.py:1466`).

**Clean:** both MEANING rulings right; LLR-195/LLR-206 text true of `check.py:1441-1467`, `kitlib/config.py:254`, `docs/stack.ini` (dupes-census `paths` line 1001, complexity line 1024), and the template (commented examples only; complexity report-only downstream). LLR-291 true of the code (`check.py:2307-2315`). The act: exactly two status flips; `acts.toml` seq 20 (`approved = ["LLR-291","TC-304"]`, `reattested = ["LLR-195","LLR-206"]`); LLR and TC snapshots byte-identical to live.

**Commands:** `pytest -q -n 2 tests/test_step_path_trigger.py tests/test_check_complexity.py`: `72 passed in 0.71s`; `trace.py --strict-integrity`: orphans=0 integrity=0 drafts=2; git diff / cmp / acts.toml reads.
