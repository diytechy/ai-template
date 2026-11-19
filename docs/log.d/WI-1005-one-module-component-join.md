## 2026-11-19 — WI-1005: the module-to-component join has one home, kitlib.spine.module_components, which gen_components and trajectory_arch both call

Deferred open items: none.

Built on the maintenance branch `maint/wi-1005`, cut from `refactor_again` at
`10bb4122e`, outside the lane workflow at the operator's direction: no claim,
no lane review rounds, commit hooks on. The parent session reviews and merges.

- **The critique.** Gemini Argon's round 1 asked for three changes, and all
  three were adopted. The input contract is now in the Done-when (S3), and so
  is the home (S5). `planmode = "none"` takes S4's cheap-test exception. The
  critique placed `kitlib/spine.py` on `docs/kernel-modules-allow`. It is not
  there. No edge is owed anyway, since both callers already imported
  `kitlib.spine`.
- **The join.** `kitlib.spine.module_components(llrs)` takes the design rows
  its caller loaded. It skips a `-000` example row and a row whose id does
  not start with `LLR-`, and keeps only the `Component` tokens that start
  with `CMP-`. It splits `Module` with `refs` and normalizes it with
  `norm_module`. It does not filter tags against the component registry.
  `gen_components.build` and `trajectory_arch`'s `component_top_view` and
  `_classifiable_edges` call it. Both copies are deleted, and so is
  `check_trajectory`'s re-export of the second.
- **The three disagreements.** They are the example row, the non-`LLR-` id
  and the non-`CMP-` token. For each, `trajectory_arch`'s narrower answer is
  kept, and a test of the one home pins it. None occurs on a registry
  `trace.py --strict` passes, apart from example rows, which `gen_components`'
  loader already dropped. Measured here, the one home's map equals each
  deleted copy's, and the generator over the trunk-base registries
  reproduces the trunk-base view byte for byte.
- **Rows.** LLR-373 (the join) and TC-435 (the split test, the three arms
  and `gen_components`' call pin) are new and `Drafted`. LLR-049's and
  LLR-199's `code_symbol` (traced) drop `module_components`. TC-436 was not
  needed.
- **The component view** changes only by LLR-373. CMP-006 gains the row,
  SR-169 (now shared with CMP-009) and the UX-ENGINEER hat, and
  `design_rows` goes from 336 to 337. No module or seam moves.
- **Sizes.** `trajectory_arch.py` 1145 -> 1130 SLOC and `check_trajectory.py`
  1660 -> 1659, both pins re-stamped down. `kitlib/spine.py` is 627 SLOC.
- **RESYNC.** "The module-to-component join has one home, in kitlib.spine",
  anchored at `10bb4122e`. Nothing is forced: overwrite `kitlib/spine.py`,
  `gen_components.py`, `trajectory_arch.py` and `check_trajectory.py`
  together. A local caller of a deleted copy calls the one home instead.
