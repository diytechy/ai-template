e7e0117d SOUND

**BLOCKER**

none

**MAJOR**

none

**MINOR**

none

**Verified:** The README change removes the scaffold-breaking link, the template and dogfooded copy match, and `Trigger`, `Rubric` and `MinWorkItems` are explicitly classified as approved. The reference table matches. No spine rows or statuses changed. The RESYNC_PACK entry is anchored at the range’s base commit. The targeted tests passed, and strict trajectory checking exited 0.

**Commands**

- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/build-wi-784 tests/test_check_docs.py::test_an_absent_open_items_registry_is_itself_the_s3_finding tests/test_trajectory_staged.py::test_spine_cell_split_classifies_every_shipped_column tests/test_dogfood_sync.py` — `43 passed, 1 skipped in 3.57s`.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; `check_trajectory: clean (781 work item(s), 705 done (90%), 26 cancelled, graph acyclic).`