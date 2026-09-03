# WI-578 — ADJUDICATE amended-cell meaning/clarity — commit 921f947

One line per amended row. Question judged: did the amendment change the
requirement's MEANING, or only its CLARITY?

**Scope, and why the count is three.** The material handed to me is the whole
drift set of the live registries against `docs/archive/last_approved` (copied
2026-08-30, commit `4824c0ba`) — twenty-nine rows. This row's own generated
`## Context` names **three**: `LLR-158`, `LLR-203`, `LLR-204` (five cells:
`LLR-203` carries three). The other twenty-six are carried by other rows and
are restated below as reading aid, excluded from the counter — the same
correction WI-566's REVIEW-A finding 1 forced and WI-573 applied. The governing
`VERDICT:` line is the last line of this file and it is the only one.

## In-scope amended rows — adjudicated here, counted (3)

- [MEANING] LLR-158 `Detail` -> `split_changed_cells` as the ONE comparison basis: the structural id/Status exclusions, `spine_cell_class` as the shared classifier, `_APPROVED_TEXT` requiring Approved on both sides, the before/after pairs it returns, and needs covered by the whole-file copy rather than a per-need projection. Nothing said about how the readers of that basis get their rows, nor about which registries any of them walk -> the same, PLUS an entire second half: ONE two-tree walk `_spine_row_sides` feeding FOUR named consumers (`staged_spine_amendments`, `staged_approval_acts`, `staged_drafted_rows`, `lane_approval_refusal`); the exempts-vs-reports invariant with its ONE named subtraction (an Approved -> Drafted de-approval moves Status so the amendment reader exempts it, blesses nothing so the approval-act reader does not report it, and `staged_drafted_rows` raises the re-approval it now owes); the per-row judgement stated once in `_approval_act` so the flip arm and the born arm cannot drift apart; and a DECLARED, PARAMETERISED universe — `SPINE_CSVS` (the spine three, the walk's default, read by the amendment and drafted readers), `APPROVAL_ACT_CSVS` (those three plus stakeholder-needs, passed by `staged_approval_acts` so `lane_approval_refusal` refuses a lane signing a NEED), `OUTSIDE_THE_APPROVAL_ACT` (interfaces, external, components), the two lists pinned as one exhaustive disjoint statement `SNAPSHOTTED == APPROVAL_ACT_CSVS + OUTSIDE_THE_APPROVAL_ACT` against `baseline_snapshot.SNAPSHOTTED`'s seven -> a design satisfying the old text — one basis function, each reader doing its own two-tree walk, no declared registry bound and no pinned partition — is correct under the old text and DEFECTIVE under the new one on four independent counts. Obligations added, not restated.
- [MEANING] LLR-203 `Detail` -> a MAPPING row is a source/destination pair plus a prose comment; two of the parent's four finding classes run over it; and, stated as NOT DISCHARGED, "no cell joins an inventoried file to a requirement id", "every arm above walks the DESTINATIONS the inventory declares, NEVER the shipped tree", and "the installer is excluded from its own inventory IN PROSE at its module rather than as a row in the exclusion carrier, so the one exclusion that is load-bearing … is the one no reader can enumerate mechanically" -> a MAPPING row OPTIONALLY carries a third cell naming the requirement, normalized tolerantly by `mapping_entries` to `(source, destination, reference)` with a bare pair surviving as `reference = None`; all four finding classes run; a THIRD arm exists — `delivery_inventory` walks the shipped tree INDEPENDENTLY of the inventory, classifying each physical file as a MAPPING source, a reasoned kit-only exclusion or a conditional materialization and separately enumerating generated outputs that inherit their generator's reference; its exclusion carrier is the mechanically parsed `mapping-source-exclusions`, one `<source> — <reason>` row partitioned on a literal spaced EM DASH, a hyphen row silently skipped and its source resurfacing as a gate-class missing-file finding; the installer is one of those rows; and the NOT DISCHARGED list is a different list (the reference cell mostly unfilled, its consumers owned by no design row) -> three of the old text's own explicit negative claims are now false BY CONSTRUCTION: there IS a requirement-joining cell, there IS an arm walking the shipped tree, and the installer IS a mechanically enumerable row. A checker written to the old text would be wrong about what the inventory is; a reviewer holding the old text would read a delivered mechanism as absent. Verified in the tree: `bootstrap.mapping_entries` (`bootstrap.py:2262`), `_mapping_source_exclusions` partitioning on `" — "` (`:2331`), `delivery_inventory` (`:2346`), the installer row (`mapping-source-exclusions:19`), the four classes at `gen_arch_map.mapping_purpose_findings` (`:2085`).
  - [MEANING] LLR-203 `Title` -> "…**carrying no purpose reference**" -> "…**and its tolerant purpose reference**" — the row's declared subject GAINS a component. A title is the row's scope statement; the old one asserts the absence the new one delivers.
  - [MEANING] LLR-203 `Rationale` -> the row names the inventory rather than a purpose checker, and records THREE gaps (no requirement reference anywhere in the inventory, the join, the widened universe) so a reader cannot mistake the delivered arms for the obligation -> the row names the inventory AND ONLY the inventory, explicitly REFUSING to annex the resolver, the four finding classes and their warn-to-gate table as a decomposition it does not make; records that no design row OWNS those consumers; and states the cell's TOLERANCE as the deliberate design choice (a mandatory reference would force a flag day; a warn class over an optional cell buys the same coverage number as a burn-down) -> what the row claims to own is redrawn, and a NEW positive design constraint appears — the cell must be optional and its class must warn, not gate. A design making the reference mandatory satisfies the old rationale and violates the new one.
- [MEANING] LLR-204 `Detail` -> `backlink_ids` / `scan_backlinks` / `implements_report` / `read_backlink_min` and the warn-to-strict shape, NOT DISCHARGED in two ways (DIRECTION and UNIVERSE), closing with "**the grammar and the dial are what the parent's join and its policy WOULD RIDE**; neither runs for it today" — i.e. this mechanism is the road to SR-163's join, and closing its two gaps is what discharges the parent -> the same mechanism and the same two gaps, PLUS "AND THE PARENT DID NOT COME THIS WAY": the join and its warn-to-gate policy are delivered and ride NEITHER this grammar NOR this dial (the reference is a cell on the shipped-file inventory, its resolution its own function, its classes graded against a separate policy table), so this row's two gaps bound THIS mechanism ONLY and "are no longer the parent's outstanding remainder — what stands here is … useful on its own terms and not on the way to anything" -> the obligation moves in the direction that matters most: a builder acting on the OLD text discharges SR-163 by widening this grammar's universe and inverting its direction; under the NEW text that is wrong work on a mechanism the parent no longer routes through. The two texts send a reader to different code.

All three in-scope rows are MEANING, so §A5.2's "flip back to Approved" arm
does not apply to any of them; each row's `Status` was already `Approved` on
both sides and stays untouched.

### Why this verdict re-anchors where WI-573 refused

WI-573 ruled `LLR-158` MEANING and DECLINED to re-anchor, because the cell's
declared registry bound was FALSE against the tree (it said every reader walks
`SPINE_CSVS`, and named three registries in `OUTSIDE_THE_APPROVAL_ACT`, while
`staged_approval_acts` and `lane_approval_refusal` walk the four-registry
`APPROVAL_ACT_CSVS`). Anchoring is per-registry whole-file
(`baseline_snapshot.copy_live`), so that one false cell held the whole
`low-level-requirements.toml` anchor hostage.

**That finding has been answered.** `4566ca27` ("WI-575: correct LLR-158's
declared registry bound to the shipped partition") rewrote the clause to the
partition that ships, and `33aee707` / `9f8cab1a` (WI-569) corrected three
falsified claims on `LLR-203` and one on `LLR-204`. I re-drove every load-bearing
claim in all three cells against the tree at this commit:

- `SPINE_CSVS` — three registries (`acceptance_record.py:124`);
  `APPROVAL_ACT_CSVS = SPINE_CSVS + (stakeholder-needs,)` — four (`:144`);
  `OUTSIDE_THE_APPROVAL_ACT` — interfaces/external/components, three (`:165`);
  the identity `SNAPSHOTTED == APPROVAL_ACT_CSVS + OUTSIDE_THE_APPROVAL_ACT`
  pinned at `tests/test_acceptance_record.py:233-235` against
  `baseline_snapshot.SNAPSHOTTED`'s seven. `_spine_row_sides(…,
  registries=SPINE_CSVS)` is the parameterised default (`:422`) and
  `staged_approval_acts` passes `APPROVAL_ACT_CSVS` (`:557-558`). The cell now
  describes the shipped partition exactly, and `code_symbol` names
  `APPROVAL_ACT_CSVS` — the omission WI-573 flagged is also closed.
- `LLR-203`'s three arms, the tolerant `(src, dst, ref|None)` normalization, the
  em-dash-partitioned carrier and the installer row: all present as cited above.
- `LLR-204`'s "the parent did not come this way": the delivered join is
  `gen_arch_map.mapping_purpose_findings` over `bootstrap.mapping_entries` +
  `delivery_inventory`, graded by `MAPPING_FINDING_POLICY` — not
  `scan_backlinks`/`read_backlink_min`. The claim holds.

So the new text on all three rows is text I would bless, and the aftermath
below takes the re-anchor. Blessing `low-level-requirements.toml` also carries
the four other Approved rows drifted in that file — `LLR-058`, `LLR-136`,
`LLR-144`, `LLR-198` — each already ruled MEANING (WI-566 for 058/144/198,
WI-573 for 136), each re-read against the tree by WI-573, and none amended
since (`git log 07cbabb..HEAD` on that file shows only the WI-569/WI-575
corrections to 158/203/204). Their re-attest is OWED on this same released
rung, so carrying them is the act completing, not scope creep. `LLR-206` is
`Drafted` on both sides; a Drafted row in the snapshot blesses nothing
(`_APPROVED_TEXT` requires `Approved` on both sides), so its presence in the
copied file is inert and its first approval remains its own act.

No registry CELL was edited by this session, in either commit.

## Restatement, excluded from the count (26)

Reproduced because they are in the drift set I was shown, not because they are
adjudicated here.

**Closed by WI-547 as CLARITY (17)** — SR-024, SR-033, SR-043, SR-052, SR-053,
SR-054, SR-111, SR-112, SR-129, SR-144, SR-146, SR-147, SR-149, SR-167, SR-175,
SR-176, SR-177, all `Rationale`, all the removal (or de-tokenising, at SR-175)
of the `Hat-derived (hat.X)` provenance label and, at SR-111/SR-112, of the
trailing citation-home sentence those cells themselves declared removable. No
obligation moves in any of them; I concur.

**Closed by WI-566 as MEANING (6)** — LLR-058 `Detail`, LLR-144 `Detail`,
LLR-198 `Detail`, TC-138 `Method`, TC-147 `Method`, TC-194 `Method`; all turn
on the WI-553 retirement of the `queued`+`blockref` shape for the terminal
`partial/` move. WI-573 re-read them against the tree and confirmed the amended
text matches what shipped.

**Closed by WI-573 as MEANING (1)** — LLR-136 `Detail`.

**Not amendments of approved text (2)** — TC-199 and TC-200 are `Drafted` in
`docs/test/test-cases.toml`, so they carry no attestation for this rung to
keep. Their `Expected`/`Method` narrowing is not adjudicable here.

**Not in the handed set, noted for the reader (1)** — the LLR registry also
carries `LLR-206`, present live and absent from the snapshot, `Drafted`: a
first-approval act, not an amendment, and not this row's.

VERDICT: MEANING rows=3
