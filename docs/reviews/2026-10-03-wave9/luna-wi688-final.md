0b6bb6a5 NOT YET SOUND

### BLOCKER

none

### MAJOR

docs/test/test-cases.toml:2182 — TC-211’s inputs omit the decomposition record and its SR-161 perspective record, though the procedure requires both to be read. If either file changes, the observation digest remains unchanged, so the `pass` can still appear fresh for a sample the judge did not inspect. Add the inspected records to the case’s declared inputs.

### MINOR

none

### Verified

- The earlier `recorded_by`/`recorded_on` MAJOR is closed: first writes without `--by` and records missing either field are refused, with tests at tests/test_hats_record.py:189 and tests/test_hats_record.py:209.
- LLR-297’s detail and TC-312’s method match the code. The round-two registry changes are limited to those two cells; act 26 later approves them. Three single-point mutations on scratch copies—removing authorship validation, merging sibling tag contexts, and bypassing atomic replacement—were each caught by tests.
- Both archived registry copies are byte-identical to live. Act 26 lists approved `LLR-297` and `TC-312`, re-attested `LLR-183`, and its README stamp matches. Each blessed row has a corresponding ruling: docs/reviews/wi-688-re-judge-tc-211-no-result-rec/002-ADJUDICATE-FIRSTAPPROVAL-6d76936.md:169, docs/reviews/wi-688-re-judge-tc-211-no-result-rec/003-ADJUDICATE-AMENDMENT-6d76936.md:32.
- TC-211’s current `pass` follows its Method: the judge recorded the paraphrasing child as a finding, read the complete sample and SR-161 record, and validated that record with no findings. The Method was not weakened. The observation is well-formed and its digest matches its declared inputs, but those inputs omit the inspected records.
- The judges recorded verdicts; the lane builder made the fixes. The worktree is clean.
- `check_trajectory.py --strict` exited 0. `trace.py --strict` reported only the pre-existing LLR-292 “minimal” finding. The hats record check reported no findings.

### Commands

- Focused hats tests: `116 passed`.
- `check_trajectory.py --strict`: exit 0.
- `trace.py --strict`: exit 1 for the single LLR-292 finding.
- `hats.py --root . record docs/ai-template-redesign-2026-09-05-codex/DECOMPOSITION-AMENDMENTS.perspectives.toml --check --strict`: no findings.
- Three scratch-copy mutation runs: all three mutants killed by tests.