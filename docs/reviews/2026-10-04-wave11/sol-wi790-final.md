6f67736b NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. `project-trajectory/scripts/acceptance_record.py:1919` and `project-trajectory/scripts/acceptance_record.py:1959` — **Unreadable parent blobs still bypass synchronization.** With the parent commit and trees readable, removing its open-items registry blob changes an unchanged-Done-when ruling from refused to `[]`; the merge sync check changes from a refusal to `None`. The staged check also returns `[]`. An unreadable parent citing-spec blob likewise silently removes that row from the citing set. Failed reads become absent registries or skipped malformed specs. This violates A1’s no-skip rule; round-1 MAJOR 1 is only partially resolved.

**MINOR**

1. `docs/requirements/interfaces.toml:1031` — **Round-1 MINOR 1 remains partly unresolved.** For a row citing OI-5 and OI-6, ruling OI-5 while OI-6 remains pending permits retaining the registry SpecRef. IF-073 still says SpecRef becomes real “after the item is ruled.” LLR-153 and TC-147’s intake qualifications are corrected. The adjudicator carried this IF-073 discrepancy as a nonblocking observation.

**Verified**

Round-1 MAJOR 2–5 and MINOR 2–3 are resolved in code and cells. Reviewed both fix rounds and verdicts 001–004. The act changes exactly four Status cells and no other live registry cell; seq 30 names exactly four approvals, twelve amendments and two retirements. All three written snapshots match their live registries byte-for-byte, both on disk and in HEAD. The record attributes the act to the independent adjudicator; no script gained approval authority. `needs` remains the sole relationship edge, and synchronization compares each commit with its parent. Default and Node scaffolds pass. The worktree remains clean.

**Commands**

All pytest runs used `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 0 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-790-final`, with the specified Git ceiling and bytecode writing disabled.

- Five requested test modules — **120 passed in 13.00s**.
- `tests/test_profile.py::test_default_scaffold_is_fully_green_including_warnings` and `tests/test_profile.py::test_the_scaffolded_oi3_is_filed_with_its_queued_placeholder` — **2 passed in 6.29s**.
- Two open-item intake cases plus `tests/test_decision_record.py` — **91 passed in 3.60s**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — **exit 0**, advisory warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -B C:/Projects/ai-template.wt/review-tmp/wi-790-final-probes.py` — reproduced the unreadable-blob bypasses.
- Git log/diff reads, parsed act-cell comparison, snapshot byte/hash comparisons, IF Data-length audit and final `git status --porcelain=v1` — completed.