## 2026-11-06 — WI-997: this repository's test files carry their test-case tags, and a strict finding holds tags and evidence cells equal

Deferred open items: none.

A scripted, unshipped seed (`docs/plans/WI-997/seed_tags.py`) wrote 2151 tags
across 216 test files; 21 more were already in the tree. Its checker reads the
seed commit against its parent: 216 files, 0 AST differences with docstrings
stripped, 7720 collected ids before and after with one digest, 0 reader
findings, 0 missing and 0 extra tags, and no complexity row moved. The output
and a 40-tag sample are `docs/plans/WI-997/seed-evidence.txt`.

`check_trajectory.py`, through `trajectory_arch.py`, now reports evidence
without a tag and a tag without evidence: a WARN, an ERROR under `--strict`,
gating from DevStg-Impl. It lands at 0 findings and retires when the evidence
column is generated.

- The spec's 19 stale nodes were 4, plus 15 whitespace-separated cells a
  `;`-only split misread. The 4 are repointed; the 15 were read correctly and
  left alone (wi-997 D-002 to D-006).
- TC-165 and TC-166 name their debt rows through a parenthetical note, under
  OI-127's ruling, and take no tag (D-007).
- TC-333's `expected` had been false since `489678a52`; its sentence is cut to
  what its rows state, blessed at the sitting (D-009, D-010, 005-ADJUDICATE).
- An intent row's `Evidence` cell now holds a note until the tests commit, so a
  test's evidence part arrives with its tag.
