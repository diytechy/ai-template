<!-- Claude Sonnet (read-only) review of WI-729, build/wi-729 a20b496a..7a4d1ef9. Built by Codex Sol; committed by the coordinator. -->

7a4d1ef9 SOUND

BLOCKER: none

MAJOR: none

MINOR: none

**Checked against the code:**
- **The adapter provider constants:** Plain `""` (`:217`), Claude `anthropic` (`:349`), Codex `openai` (`:453`); Opencode inherits `""`.
- **`session_keep.keep_for`** (`:524-592`) has three launch cases: mint, resume, and a bounded wait that then runs unretained with a printed reason. These match SR-227's rewritten `shall`.
- **`_classify`:** `joint` iff `any(sid not in disjoint_siblings for sid in siblings)`, a one-line change. A read-only in-memory probe gave:
  - a disjoint-only sibling → `unclassified`, with the advisory;
  - a mixed row → `joint`, with only the disjoint sibling reported.
- **SR-227** is still one row with one `shall launch`. The three sub-cases were already implied by its acceptance and by LLR-270, so there is no tier violation.

**Scope:** exactly the granted files and cells, every numbered item accounted for. The statuses are unchanged: the approved rows stay Approved, and the drafted rows stay Drafted.

**Also verified:**
- No codex `cmd_template` carries `-o`.
- The comment rewrites are standing prose.
- The optional items (LLR-222 title, SR-193 and SR-177 rationales) carry no history.

**Run:** `python -m pytest -q -n 2 tests/test_assumption_rules.py tests/test_session_adapters.py tests/test_session_service.py tests/test_session_keep.py tests/test_cell_classes.py -p no:cacheprovider` → **318 passed in 37.65s**.
