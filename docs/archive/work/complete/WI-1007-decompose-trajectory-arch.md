+++
id = "WI-1007"
title = "trajectory_arch.py is split by the checks it holds, each module under the size line, with no change of behaviour"
workstream = "process"
sr_refs = ["SR-159", "SR-165"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
+++

## Deliverable

`trajectory_arch.py` (1,128 SLOC) is split along the checks it held into five
modules beneath it, every one far under the size line, and
`check_trajectory --strict` prints the same findings on this repository.
The spec of record was HANDOFF §12.2
(`docs/plans/2026-11-11-test-tiers/HANDOFF.md`, "Rulings taken on 2026-11-15
and 2026-11-16"); the row's SpecRef cell was cleared at close, as for every
terminal row.

- **Critique dispositions** (`f7af9e4ec`): S4 adopted as
  `planmode = "single"`; S5 adopted, the architectural delta stated in the
  Context and the third Done-when item extended to IF-263, IF-131, the new
  rows, `components.derived.toml` and `docs/kernel-modules-allow`.
- **Plan** (`89c54f960`, `docs/plans/WI-1007/plan.md`): the cuts, and why
  the split stops at five modules. Connectivity asks each arch-map module to
  own an interface row (five ids allotted); containment asks each to be named
  by a design row, so the three checks no design row binds (the armed
  definition gate, seam-TC coverage, the CodeSymbol crosscheck) ride with the
  bound rule of their tier; and `trajectory_arch` keeps the spec-boundary
  rule, whose design row (LLR-068) keeps it in CMP-006.
- **The split** (`dabeb255f`). Every function and constant moved byte for
  byte, 85 named statements with one home each; two docstring phrases that
  said "this module's" now name the module meant.
  - `arch_inputs.py` (114 SLOC): registry paths, the two opt-out dials,
    `load_ifs`, `load_seams`, `load_cmps`, the declared scan profile and
    `arch_inventory`.
  - `arch_interfaces.py` (454): connectivity, the armed definition gate, and
    seam-TC coverage with its migration allowlist.
  - `arch_tags.py` (133): the Implements-tag and CodeSymbol crosscheck and
    `tc_tag_findings`.
  - `arch_seams.py` (156): the seam check (`_classifiable_edges`,
    `_cross_component_scan`), the kernel allowlist, and the one
    `_SCAN_CACHE`, which `trajectory_arch` and `check_trajectory` bind.
  - `arch_components.py` (241): the How-SW top view, the component
    derivation record and `component_findings`.
  - `trajectory_arch.py` (201): IF-263's composer under the same `__all__`,
    and the spec-boundary rule. `check_trajectory.py` does not change, so
    every public name its callers import still resolves.
- **Behaviour unchanged.** `check_trajectory.py --strict` printed 273 lines
  at the base and prints 272 after; the one line gone is this row's own
  SpecRef-staleness warning, which the dispositions commit cleared by
  editing the spec. The base's scripts, run with `--root` against the final
  tree, print output byte-identical to the final scripts'. The existing tests
  pass with only their imports changed: `tests/test_seam_import_forms.py`
  loads `arch_seams` (whose module globals it patches), and TC-080's
  re-export pin loads each rule's new home and names it as the facade's
  `__module__`.
- **Rows** (all in `dabeb255f`). IF-316 to IF-320 are new and `Drafted`, one
  per module, each declared on its owner's `Contracts:` line with a
  `Contract IF-###:` body, and each cited by an existing test case through a
  traced `verifies` cell (TC-080: IF-316, IF-317; TC-409 and TC-410: IF-318;
  TC-067: IF-319; TC-049 and TC-166: IF-320). IF-131's requestors are the
  modules that import `gen_arch_map`. IF-263 keeps its owner, requestor and
  data; its contract body names the composition. LLR-042, LLR-049, LLR-067,
  LLR-172, LLR-365, LLR-366 and LLR-374 name the moved symbols' new modules
  (traced `module` cells; no `code_symbol` changed), and LLR-374's `Drafted`
  detail names `arch_seams.py`. `components.derived.toml` and the interface
  reference regenerated; `docs/kernel-modules-allow` is unchanged. Watermark
  IF 320.
- **Ratchets.** The size baseline's `trajectory_arch.py` entry retires; the
  new modules are under the threshold and need none. The five moved
  functions' complexity entries re-key to their new paths, not re-stamped.
  `tests/test_import_layers.py` finds no new cycle or deferred import.

Left undone:

- **The review bar.** Built on the maintenance branch `maint/wi-1007`,
  outside the lane workflow: no claim and no lane review rounds. The parent
  session reviews the diff and merges it.
- **Accepted prose naming the old home.** LLR-172's detail and TC-166's
  method name `trajectory_arch.component_findings`. The name still resolves
  through the composer, so neither accepted row was amended.
- **One check per module.** The interface tier's three rules share
  `arch_interfaces.py`. A module of their own each needs an interface row
  past the five allotted and a design row binding the two that have none.
- LLR-375 to LLR-380 were allotted and not needed.

## Context

Filed by hand on 2026-11-16 at the operator's ruling (HANDOFF §12.2:
"`trajectory_arch.py` (1,132 code lines): file a work item to decompose it;
not on this branch"). The module passed the line-count ratchet's 1,000-line
threshold while the first-day and conversion fixes landed (989 to 1,012), and
WI-999's component derivation record took it to 1,132. Its own section
comments name seven checks: the armed definition gate, seam-TC coverage and
its migration allowlist, the Implements-tag and CodeSymbol crosscheck, the
How-SW top-view rule, the declared arch-map scan profile, the component
derivation record, and specs acting on declared interface boundaries.

Where the cuts fall is the plan's to find (`docs/plans/WI-1007/plan.md`).
Its scope critique is disposed of below.

The architectural delta. `trajectory_arch` stays the module
`check_trajectory` imports, so IF-263 keeps its owner, its requestor and its
`Contract IF-263:` body, and `check_trajectory.py` does not change. The
checks move into new modules beneath it, each in component CMP-006 as
`trajectory_arch` is today. Every new module is an arch-map module, and the
connectivity rule whose output must not change asks that an interface row
name each one on both sides. So each new module owns one new `Drafted` row
for the surface it hands up (IF-316 to IF-320 are allotted), declared on its
`Contracts:` line with a `Contract IF-###:` body, and each is a requestor on
the row of a module it imports. IF-131 is the one other row that names
`trajectory_arch`: its requestors become the modules that import
`gen_arch_map` after the split. `gen_arch_map` carries two component tags, so
an undeclared edge into it is an advisory. Each new row is cited by the
existing test case that drives its surface, so the seam-TC count and the
migration allowlist do not move. Containment comes from the design rows: each
LLR whose `module` or `code_symbol` binds a moved symbol names the module
that symbol moves to, and that places the module in CMP-006. The interface
reference and `docs/requirements/components.derived.toml` regenerate from the
changed rows. `docs/kernel-modules-allow` names no module this row touches and
does not change.

## Done-when

- [x] `trajectory_arch.py` is split along the checks it holds, and every
      module that results is under the ratchet's threshold. The public names
      callers import still resolve, or every caller moves in the same change.
- [x] Behaviour is unchanged. `check_trajectory.py --strict` prints the same
      findings on this repository before and after. The existing tests pass,
      with only their imports changed.
- [x] Each LLR whose `module` or `code_symbol` binds a moved symbol names
      its new module, and every module that results is named by a design row,
      so each sits in a component. IF-263 keeps its owner, its requestor and
      its contract body in `trajectory_arch`. Each new module owns one
      `Drafted` interface row (from IF-316 to IF-320) with its `Contracts:`
      line and `Contract IF-###:` body, is a requestor on the row of a module
      it imports, and its row is cited by an existing test case. IF-131's
      requestors are the modules that import `gen_arch_map`. The interface
      reference and `docs/requirements/components.derived.toml` regenerate
      clean (`gen_components.py --check`), and `docs/kernel-modules-allow` is
      unchanged. `trace.py --strict` and `check_trajectory.py --strict` are
      clean, and the module-size baseline holds the new modules.

## Critique dispositions

Round 1 (Gemini Argon, attended, 2026-11-19,
`docs/reviews/2026-11-19-scope-critiques/WI-1007.md`): CHANGES-REQUESTED, two
MAJORs.

- **S4, `planmode`: adopted as `planmode = "single"`.** The cuts are the
  plan's to find, and they touch IF-263's seam, so the plan is written and
  committed before any code moves. The Context sentence that defers the cuts
  now points at the plan.
- **S5, the architectural delta: adopted.** Stated in the Context, and the
  third Done-when item now covers each surface the critic named: IF-263 (owner
  `trajectory_arch`, requestor `check_trajectory`, contract body), the new
  interface rows the split needs and their contract bodies, IF-131 (the one
  other row naming `trajectory_arch`), `components.derived.toml` under
  `gen_components.py --check`, `docs/kernel-modules-allow` (it names no module
  of this row), and every LLR `module` or `code_symbol` cell binding a moved
  symbol. `check_trajectory` keeps importing `trajectory_arch`, so it gains no
  edge and no new row names it.
