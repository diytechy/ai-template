+++
id = "WI-1005"
title = "The module to component join has one home, which gen_components and trajectory_arch both call"
workstream = "process"
sr_refs = ["SR-159", "SR-169"]
specref = "docs/plans/2026-11-11-oi130-rescore/README.md#defects-in-the-live-partition"
buildtier = "quick"
safety_class = "ordinary"
priority = 3
planmode = "none"
+++

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

- [ ] One function owns the join: `kitlib.spine.module_components(llrs)`.
      `gen_components` (CMP-009) and `trajectory_arch` (CMP-006) both call it,
      both copies are deleted, and so is `check_trajectory`'s re-export of the
      second.
- [ ] The join's input contract is closed:
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
- [ ] The two copies disagreed on three inputs, and the kept answer for each
      is `trajectory_arch`'s, named in the Deliverable and pinned by a test of
      the one home:
      - a `-000` example row is skipped;
      - a row whose id does not start with `LLR-` is skipped;
      - a `Component` token that does not start with `CMP-` is dropped.

      The declared bound is the rows `spine_carrier.load` returns. A registry
      `trace.py --strict` passes carries none of the three, apart from `-000`
      rows, which `gen_components`' loader already drops. On such a registry,
      each caller's output is unchanged.
- [ ] The existing test covers the one home, and `gen_components` keeps a pin
      that it calls it.
- [ ] `trace.py --strict` and `check_trajectory.py --strict` are clean, and
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
