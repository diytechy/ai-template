9c39bab2 NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. **Missing parent history silently passes the sync check.** `project-trajectory/scripts/acceptance_record.py:2028` returns `[]` whenever `rev^1` cannot resolve, treating a shallow boundary as a root commit. Reproduced the same unchanged-Done-when ruling in a full repository and at a Git shallow boundary: the full repository refused it; the shallow repository returned no findings despite the commit object carrying a parent. This violates A1’s explicit “never skips for missing history” rule.

2. **CSV-carrier rulings bypass synchronization.** `project-trajectory/scripts/acceptance_record.py:1974` checks only `docs/requirements/open-items.toml`. For the supported CSV carrier, changing OI-5 from pending to ruled without updating its citer returned `[]` from both staged and committed checks. `project-trajectory/scripts/check_trajectory.py:975` likewise compares SpecRef against only the TOML spelling. Existing CSV adopters therefore receive incomplete enforcement.

3. **A malformed decision record crashes the owner surface.** `project-trajectory/scripts/kitlib/decisions.py:221` constructs `set(hoist)` without validating its elements. With `high_risk = [["D-001"]]`, `record_findings` correctly reports malformed data, but `review_queue` and `gen_open_items.render` raise `TypeError: unhashable type: 'list'`. The owner page cannot display the finding or the remaining decisions.

4. **A substantive Done-when update can be refused as unchanged.** `project-trajectory/scripts/acceptance_record.py:1951` uses the claim-time evidence-stripping comparator. Reproduced a ruling that changes `- OI-5 is ruled.` to `- OI-5 is ruled. — Use scripts/export.py as the canonical export entry.` The added criterion contains a path, so the comparator discards it as evidence and refuses the commit. The sync rule must not mistake added criteria for completion evidence; A1 leaves their substance to independent review.

5. **LLR-299 promises an anchor check that does not exist.** `docs/requirements/low-level-requirements.toml:3150` requires a placeholder’s SpecRef to name its cited pending item. A queued WI citing pending OI-5 but pointing at ruled OI-6 passes both `open_item_specref_findings` and R-E resolution. TC-314’s evidence checks a correctly authored placeholder, but never tests this mismatch. The row and its test coverage overstate the implemented rule.

**MINOR**

1. **Several amended cells overstate when SpecRef changes.** `docs/requirements/low-level-requirements.toml:1538` and `docs/test/test-cases.toml:1459` say an open-item successor receives the registry SpecRef. Intake preserves an existing real SpecRef; the amended intake test explicitly asserts that preservation. These cells need the “when absent” qualification. Similarly, `docs/requirements/interfaces.toml:1031` says SpecRef becomes real after an item is ruled, while the spec and tested code permit the registry reference until all cited items leave pending.

2. **Four amended IF Data cells exceed PROCESS.md’s 160-character limit.** Locations and measured lengths: `docs/requirements/interfaces.toml:719` — 206; `:920` — 163; `:1037` — 225; `:2248` — 259. They previously fitted the limit. IF-256 also describes `review_queue(text) -> [entry]`, although it returns `(entries, reviewed_count)`. A caller following that cell receives a different shape.

3. **The new traced rules lack their LLR back-links.** Examples: `project-trajectory/scripts/acceptance_record.py:1964` names only SR-148 despite LLR-298 now existing; `project-trajectory/scripts/check_trajectory.py:935` and `project-trajectory/scripts/kitlib/spine.py:267` omit LLR-299. The new functions’ declarations therefore do not reach the design rows authored for them.

**Verified**

Reviewed both commits, the complete WI spec, OI-102, both reports, and amended spine cells. The `needs` token is the sole relationship edge; historical `wi_refs` does not drive readiness, context selection, validation, or rendering. Blocking, mixed-edge reasons, queue projections, reviewed-value cases, and normal synchronization cases pass. No existing row changes Status, and no new script approves anything. The Node scaffold passes its strict checker and remains paired after resync. Five selected new tests fail against `15874031` for the expected missing behavior. RESYNC_PACK is anchored at trunk commit `15874031`. The worktree remained clean.

**Commands**

All pytest runs used the stated Python executable, `-q -p no:cacheprovider -n 0`, and the literal `--basetemp C:/Projects/ai-template.wt/review-tmp/wi-790`. Bytecode writing was disabled.

- `git status --short`, `git log --oneline 15874031..9c39bab2`, and file-scoped `git diff 15874031..9c39bab2` reads — clean worktree; both commits inspected.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 0 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-790 tests/test_open_item_readiness.py tests/test_open_item_queue.py tests/test_ruling_sync.py tests/test_decisions_to_review.py tests/test_schedule.py` — **104 passed in 9.00s**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — **exit 0; clean**, with advisory warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 0 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-790 tests/test_profile.py::test_the_scaffolded_oi3_is_filed_with_its_queued_placeholder tests/test_intake.py tests/test_decision_record.py tests/test_trace.py::test_an_unreadable_allow_line_reds_the_integrity_floor tests/test_trace.py::test_an_unresolved_allow_entry_reds_the_integrity_floor` — **192 passed in 97.38s**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/wi-790-red-setup.py` — exported the baseline kit and current selected tests into scratch.
- Baseline pytest selecting the cited-pending, uncited-pending, citing-card, untouched-Done-when, and scaffold-placeholder tests — **5 expected failures in 6.78s**. The initial selection also included the decisions module, which could not collect because the baseline lacks `pending._kitdecisions`.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/wi-790-probes.py` — final run **exit 0**; reproduced the five major findings. Earlier scratch attempts encountered a blocked Git transport and corrected fixture formatting.
- Inline Python TOML/AST/byte audits — **no Status flips**; confirmed IF lengths and byte deltas: PROCESS.md **+124**, byte-budget skill **+2**.