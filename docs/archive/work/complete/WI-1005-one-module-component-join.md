+++
id = "WI-1005"
title = "The module to component join has one home, which gen_components and trajectory_arch both call"
workstream = "process"
sr_refs = ["SR-159", "SR-169"]
specref = ""
buildtier = "quick"
safety_class = "ordinary"
priority = 3
planmode = "none"
+++

## Deliverable

`kitlib.spine.module_components(llrs)` is the module-to-component join's one
home. `gen_components.build` passes it the design rows its loader returned.
`trajectory_arch`'s `component_top_view` and `_classifiable_edges` pass it
`spine_carrier.load` of the LLR registry. Both copies are deleted, and so is
`check_trajectory`'s re-export of the second. Both callers already imported
the package, so no import edge, interface row or boundary is added. The spec
of record is defect 3 under "Defects in the live partition" in
[`docs/plans/2026-11-11-oi130-rescore/README.md`](../../../plans/2026-11-11-oi130-rescore/README.md).
The row's SpecRef cell was cleared at close, as R-F asks of a terminal row.

The two copies disagreed on three inputs. The kept answer for each is
`trajectory_arch`'s:

- **A `-000` example row.** `gen_components`' copy joined one if handed it,
  though its own loader never handed it one; `trajectory_arch`'s skipped it.
  Kept: skipped. The shipped template's `LLR-000` row is the live instance:
  the old `gen_components` copy, handed the template's rows unfiltered, mapped
  `path/to/module` to `CMP-000`.
- **A row whose id does not start with `LLR-`.** `gen_components`' copy joined
  it; `trajectory_arch`'s skipped it. Kept: skipped.
- **A `Component` token that does not start with `CMP-`.** `gen_components`'
  copy kept it; `trajectory_arch`'s dropped it. Kept: dropped.

Why the narrower answer: a placeholder row, or a token that cannot name a
component, should not make a membership that the gate-bearing containment and
cross-component rules read. That copy was also the one with a test. No caller
wanted the wider answer, since each intersects the map with the ids it
declares. `test_the_join_keeps_the_narrower_answer_where_its_two_copies_disagreed`
pins all three, one case each, beside a control row whose well-formed dangling
tag is kept.

A registry `trace.py --strict` passes carries none of the three, apart from
`-000` rows, which `gen_components`' loader already drops, so each caller's
output on it is unchanged. Measured on this repository: the one home's map
equals each deleted copy's, each fed the rows its caller fed it, and the
current generator over the trunk-base registries reproduces the trunk-base
component view byte for byte.

- **Critique dispositions** (7a88dba75): S3, S5 and S4 adopted. The
  Done-when states the input contract, the three disagreements, the kept
  answer and the home. `planmode = "none"`.
- **Regressions** (5a4f2e201), red before the code in all five cases: four on
  the missing `kitlib.spine.module_components`, one on `gen_components`'
  copy still bound. The WI-429 split test now drives the one home over the
  rows `spine_carrier` loads, and the three disagreement arms sit beside it in
  `tests/test_components_registry.py`.
  `tests/test_gen_components.py::test_seam_placement_reads_membership_from_the_one_join`
  pins three things: the generator binds no copy, it hands the one home its
  loaded design rows once, and it places seams by the answer. A stubbed empty
  map leaves all three seams unplaced.
- **Code** (8abc17fc8): the function in `kitlib/spine.py` and the two
  callers' calls. The ratchet re-stamps down: `trajectory_arch.py` from 1145
  to 1130 SLOC and `check_trajectory.py` from 1660 to 1659.
  `kitlib/spine.py` is 627 SLOC, under the threshold. RESYNC entry "The
  module-to-component join has one home, in kitlib.spine": nothing forced;
  overwrite the four files together. The OI-130 re-score's `live.py` calls
  the one home, so its README re-run recipe still runs.
- **Registry rows** (5f3245c7b): LLR-373 and TC-435, both new and `Drafted`.
  LLR-049's and LLR-199's `code_symbol` (traced) drop `module_components`,
  which neither module defines now. Watermark LLR 373, TC 435.
- **The component view** changes only by the new row. CMP-006 gains LLR-373
  and SR-169 (now shared with CMP-009, so it enters both `sr_shared_refs`),
  and gains the UX-ENGINEER hat SR-169 carries. `design_rows` goes from 336
  to 337. No module or seam moves. The stage, status, open-items,
  acceptance-brief and `PROJECT_STATE` views were regenerated for the two
  new `Drafted` rows.

Left undone:

- **The review bar.** Built on the maintenance branch `maint/wi-1005`,
  outside the lane workflow: no claim and no lane review rounds. The parent
  session reviews the diff and merges it.
- **TC-436** was allotted and not minted: one case verifies LLR-373, the
  call pin included.
- **The re-score's other two defects** (membership drift and the seam check's
  blindness to dotted imports) are their own rows. `kitlib/spine.py` stays
  tagged into CMP-006, CMP-008 and CMP-009. LLR-373 tags CMP-006, where the
  module already was, so it adds no tag.

## Context

Filed by hand on 2026-11-15 (attended, at the owner's request) from defect 3
of the OI-130 re-score record, the third of the three rows the 2026-11-11a
handoff left unfiled (its owner item 3). Its scope critique is owed before a
claim.

`gen_components.module_components(llrs)` and
`trajectory_arch.module_components(root)` each join the LLR `Component` tags
on `LLR.Module`. Both split with `kitlib.spine.refs` and normalize with
`kitlib.spine.norm_module`, but `trajectory_arch` loads its own rows, drops
example and non-`LLR-` ids and keeps only `CMP-` tags, while `gen_components`
takes the rows it is given and keeps every tag. Only the `trajectory_arch`
copy has a test. `gen_components`' own docstring says a second reconciliation
"would be a second answer waiting to disagree".

The review-churn plan's variant F (phase 3) moves membership onto the
realization. If that lands first it may absorb this row; the critique checks.
It found that it does not: variant F's migration runs last, and this row does
not wait on it (S6, clean).

The architectural delta. The join moves into `kitlib/spine.py`, the shared
package's cell-and-row vocabulary, beside the other joins over design rows it
already holds (`resolve_modules`, `module_tests`, `llrs_under`). Both callers
already import `kitlib.spine`, so the change adds no import edge, no interface
row and no boundary. `check_trajectory` stops re-exporting the deleted
`trajectory_arch.module_components`. A new design row states the join
(`Drafted`), with one test case verifying it.

## Done-when

- [x] One function owns the join: `kitlib.spine.module_components(llrs)`.
      `gen_components` (CMP-009) and `trajectory_arch` (CMP-006) both call it,
      both copies are deleted, and so is `check_trajectory`'s re-export of the
      second.
- [x] The join's input contract is closed:
      - It takes the LLR rows its caller loaded and loads nothing.
        `gen_components` passes its own `_load` rows (examples dropped), and
        `trajectory_arch` passes `spine_carrier.load(<llr registry>, "LLR-ID")`.
      - It skips a row whose id is a `-000` example or does not start with
        `LLR-`.
      - Of a row's `Component` tokens it keeps those that start with `CMP-`.
      - It splits `Module` with `kitlib.spine.refs` and normalizes each part
        with `kitlib.spine.norm_module`, skipping an empty key.
      - It does not filter tags against the component registry: every caller
        intersects with the ids it declares, and a tag naming no row is
        `trace.py`'s finding.
- [x] The two copies disagreed on three inputs, and the kept answer for each
      is `trajectory_arch`'s, named in the Deliverable and pinned by a test of
      the one home:
      - a `-000` example row is skipped;
      - a row whose id does not start with `LLR-` is skipped;
      - a `Component` token that does not start with `CMP-` is dropped.

      The declared bound is the rows `spine_carrier.load` returns. A registry
      `trace.py --strict` passes carries none of the three, apart from `-000`
      rows, which `gen_components`' loader already drops. On such a registry,
      each caller's output is unchanged.
- [x] The existing test covers the one home, and `gen_components` keeps a pin
      that it calls it.
- [x] `trace.py --strict` and `check_trajectory.py --strict` are clean, and
      the component view regenerates unchanged or its changes are explained
      in the Deliverable.

## Critique dispositions

Round 1 (Gemini Argon, attended, 2026-11-19,
`docs/reviews/2026-11-19-scope-critiques/WI-1005.md`): CHANGES-REQUESTED, two
MAJORs and one MINOR.

- **S3, the input contract: adopted.** The second Done-when item states the
  contract: rows in, nothing loaded, the id rule, the tag rule, the split and
  the normalizer, and no filter against the registry. The third item names
  the three disagreements, the kept answer for each and the declared bound.
  The kept answer is `trajectory_arch`'s narrower one. A template row, or a
  token that cannot be a component id, should not make a membership that the
  gate-bearing rules read (`component_findings`, the cross-component scan).
  That copy is also the one with a test. The wider answer has no reader: every
  caller of either copy intersects the result with the ids it declares.
- **S5, the owning module: adopted.** The first Done-when item names
  `kitlib.spine` as the home, and the Context states the delta. The critique
  said `kitlib/spine.py` is on `docs/kernel-modules-allow`. It is not. The
  move still adds no edge to declare: `gen_components` and `trajectory_arch`
  each import `kitlib.spine` today, and `kitlib/spine.py`'s design rows tag it
  into both their components, CMP-006 and CMP-009. So no `IF-###` row and no
  `interfaces.toml` change is owed. A home in `trajectory_arch` would have
  made `gen_components` import a CMP-006 checker for one function, which this
  avoids.
- **S4, `planmode`: adopted as `planmode = "none"`.** With S3 and S5 settled
  in the Done-when, the diff is fully specified by cheap tests: one function
  moved, two call-site changes and a deleted re-export, pinned by the three
  disagreement arms, the existing split test and one call pin. That is S4's
  cheap-test exception, which the finding itself offers.
