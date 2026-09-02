# WI-573 — ADJUDICATE amended-cell meaning/clarity — commit 07cbabb

One line per amended row. Question judged: did the amendment change the
requirement's MEANING, or only its CLARITY?

**Scope, and why the count is two.** The material I was handed is the whole
drift set of the live registries against `docs/archive/last_approved` (copied
2026-08-30, commit `4824c0ba`) — twenty-seven rows. This row's own generated
`## Context` names **two**: `LLR-136` and `LLR-158`. The other twenty-five are
carried by other rows and are reproduced below as reading aid, excluded from the
counter — the same correction WI-566's REVIEW-A finding 1 forced on its first
issue (it had re-counted seventeen SR rows WI-547 had already closed). The
governing `VERDICT:` line is the last line of this file and it is the only one.

## In-scope amended rows — adjudicated here, counted (2)

- [MEANING] LLR-136 `Detail` -> the converter's write side, its round-trip `--verify`, `write_spec_file` as the single writer, and its four refusals; nothing said about where the READ side takes its population from or about the schema constant's twin -> the same, PLUS two new binding statements: `read_specs` takes its population from `spec_paths` (the `kitlib.registry.spec_files` re-export) rather than from a second folder walk, so a tracked non-spec file under a status directory is residue to BOTH sides; and `COLUMNS` is pinned equal to its read-side twin `kitlib.registry.WI_COLUMNS` -> a design conforming to the old text could carry its own read-side folder walk and its own unpinned column list and be correct; under the new text both are defects. Two obligations were added to the row, not restated. (Verified present in the tree: `wi_convert.py:513` `spec_paths = _kitregistry.spec_files`, `wi_convert.py:632` the walk, and the pin asserted at `tests/test_wi_convert.py:648` — the added text is accurate, which is why it is blessable in principle; see the aftermath below for why it is not re-anchored.)
- [MEANING] LLR-158 `Detail` -> `split_changed_cells` as the one comparison basis: the structural id/Status exclusions, `spine_cell_class` as the shared classifier, `_APPROVED_TEXT`, the before/after pairs, and needs covered by the whole-file copy -> the same, PLUS an entire second half: ONE two-tree walk `_spine_row_sides` feeding FOUR named consumers (`staged_spine_amendments`, `staged_approval_acts`, `staged_drafted_rows`, `lane_approval_refusal`), the exempts-vs-reports invariant with the de-approval subtraction, the per-row judgement stated once in `_approval_act`, and a declared registry bound (`SPINE_CSVS` / `OUTSIDE_THE_APPROVAL_ACT`, pinned exhaustive and disjoint against `baseline_snapshot.SNAPSHOTTED`) -> the old text obliges one function; the new text obliges a shared walk, four readers, an invariant between two of them, and a closed registry partition. An implementation satisfying the old text (one basis function, each reader walking the tree itself) fails the new one outright.

Both in-scope rows are MEANING, so §A5.2's "flip back to Approved" arm does not
apply to either.

### The finding that governs the aftermath (LLR-158)

`LLR-158`'s new final clause does not describe the code the row owns. It says
*"every reader here walks `SPINE_CSVS`, the three spine registries … the four
other registries a snapshot anchors are listed in `OUTSIDE_THE_APPROVAL_ACT`,
and the two lists are pinned as one exhaustive, disjoint statement against
`baseline_snapshot.SNAPSHOTTED`."* In the tree at this commit:

- `acceptance_record.APPROVAL_ACT_CSVS` — **four** registries, the spine three
  PLUS `stakeholder-needs.toml` — is what `staged_approval_acts` and
  `lane_approval_refusal` walk (`acceptance_record.py:144`, docstring at :541,
  test docstring at `tests/test_acceptance_record.py:216`). Two of the four
  readers therefore do NOT walk `SPINE_CSVS`.
- `OUTSIDE_THE_APPROVAL_ACT` lists **three** registries, not four
  (`acceptance_record.py:165`).
- The pinned identity is `SNAPSHOTTED == APPROVAL_ACT_CSVS +
  OUTSIDE_THE_APPROVAL_ACT` (`acceptance_record.py:162`,
  `tests/test_acceptance_record.py:234-235`) — not `SPINE_CSVS + OUTSIDE…`.

This is a stale cell, not a disagreement about design: the cell was written at
`d5b3e124` ("close round 7") and the widening landed later at `94b77a26`
("REVIEW-A round 028 rework … the merge refusal extended to the
stakeholder-needs tier"), which moved `stakeholder-needs.toml` out of
`OUTSIDE_THE_APPROVAL_ACT` and into the act's own set. `d5b3e124` is an ancestor
of `94b77a26`; the Detail cell was never re-read against the rework it now
misdescribes. The row's `code_symbol` cell names `OUTSIDE_THE_APPROVAL_ACT` and
omits `APPROVAL_ACT_CSVS`, consistent with the same miss.

**Consequence: this session does NOT re-anchor.** The rung is released to the
loop, so a MEANING verdict here would ordinarily be re-attested by me in a
second commit. `LLR-158`'s new text is not text I would bless — a design row
stating a false bound is worse than a drifted one, because the bound is the very
claim the row exists to make checkable. Anchoring is per-registry
(`baseline_snapshot.copy_live` mirrors whole registry files), so I cannot bless
`LLR-136` without also blessing `LLR-158` out of the same file. Both stay
drifted and keep surfacing on the owner's re-attestation brief; the correction is
drafted in this spec's `## Dispositions`. No `Status` cell and no registry cell
was touched by this session.

## Restatement, excluded from the count (25)

Reproduced because they are in the drift set I was shown, not because they are
adjudicated here.

**Closed by WI-566 as MEANING (6)** — `docs/reviews/wi-566-adjudicate-llr-058-llr-144/001-ADJUDICATE-05fb6a3.md`, `VERDICT: MEANING rows=6`: LLR-058 `Detail`, LLR-144 `Detail`, LLR-198 `Detail`, TC-138 `Method`, TC-147 `Method`, TC-194 `Method`. All six turn on the WI-553 retirement of the `queued`+`blockref` shape for the terminal `partial/` move; I re-read them against the tree and the amended text matches what shipped (`schedule.py:654-714`, `handback.py:331`, `pending.py:13`, `traj_status.py:57-63`).

**Closed by WI-547 as CLARITY (17)** — SR-024, SR-033, SR-043, SR-052, SR-053, SR-054, SR-111, SR-112, SR-129, SR-144, SR-146, SR-147, SR-149, SR-167, SR-175, SR-176, SR-177, all `Rationale`, all the removal (or de-tokenising, at SR-175) of the `Hat-derived (hat.X)` provenance label and, at SR-111/SR-112, of the trailing citation-home sentence those cells themselves declared removable. No obligation moves in any of them; I concur with the WI-547 reading and add nothing to it.

**Not amendments of approved text (2)** — TC-199 and TC-200 are `Drafted` in `docs/test/test-cases.toml`, so they carry no attestation for this rung to keep. Their `Expected`/`Method` narrowing is in the WI-569 spine-reseal scope drafted by WI-568's `## Dispositions`, not here.

VERDICT: MEANING rows=2
