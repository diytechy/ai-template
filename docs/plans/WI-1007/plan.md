# WI-1007 plan: trajectory_arch.py split by the checks it holds

Planned on the maintenance branch `maint/wi-1007`, base `af1dec169`, against
the spec as its critique dispositions left it (`f7af9e4ec`). Sizes are code
lines (SLOC) as `check_complexity.module_sloc` counts them, measured at the
base by a scratch script over the module's top-level statements.

## What bounds the cut

`trajectory_arch.py` is 1,128 SLOC. Three rules this row must leave silent
decide how far it can be cut, because `check_trajectory.py --strict` must
print the same findings after the move:

- **Connectivity** (`interface_findings`): every arch-map module must be
  named by an interface row, as the owner of one (it provides) and on the far
  side of one (it consumes). Each new module therefore owns one new row.
  Five ids are allotted (IF-316 to IF-320), so the split makes at most five
  new modules.
- **Containment** (`component_findings`, the knowledge coupling arm): this
  repository holds knowledge packs, so a module in no component is a
  `--strict` finding. A module joins a component through a design row whose
  `module` cell names it. Three of the checks are bound by no design row (the
  armed definition gate, seam-TC coverage and its allowlist, and the
  CodeSymbol crosscheck), and the kernel allowlist is part of LLR-067's
  cross-component rule. Each of these rides with the bound rule of its tier,
  as it does inside `trajectory_arch` today. No design row is minted: a new
  `Drafted` row under SR-159 would be design written for a refactor.
- **Seam coverage** (`if_tc_coverage_findings`): a new interface row cited
  by no test case is a `--strict` finding, and an allowlist entry would move
  the allowlist's growth count. Each new row is cited by the existing test
  case that drives its surface (a traced `verifies` cell).

`trajectory_arch` must stay the module `check_trajectory` imports: removing
it would add an import and a row per new module to `check_trajectory.py`,
which the size ratchet pins at 1,659. It must also stay in a component, so it
keeps the one rule whose design row does not move: the spec-boundary rule
(LLR-068).

## The cuts

Every function and constant moves verbatim; only the imports at the top of
each module are new. Section comments move with the code they head.

| Module | Holds | SLOC (est.) | Bound by |
|---|---|---|---|
| `arch_inputs.py` (new) | the registry paths, `IF_ID_RE`, `CMP_ID_RE`, the `kitlib` aliases, the two opt-out dials, `load_ifs`, `load_seams`, `load_cmps`, the declared arch-map scan profile (`_stack_ini_get`, `_arch_scan_profile`) and `arch_inventory` | 130 | LLR-042, LLR-067 (`arch_inventory`), LLR-049 (`load_cmps`) |
| `arch_interfaces.py` (new) | connectivity (`interface_findings`, `_owner_files`, the contracts grammar and owner-exact arms), the armed definition gate (`contract_body_findings` and its helpers, `unchecked_contract_rows`), and seam-TC coverage with its migration allowlist (`IF_TC_ALLOW` .. `if_tc_allow_parse_findings`) | 440 | LLR-042 (`interface_findings`) |
| `arch_tags.py` (new) | the Implements-tag and CodeSymbol crosscheck, and the test-file tag rule (`_tag_evidence_findings`, `_undeclared_case_findings`, `tc_tag_findings`) | 130 | LLR-365, LLR-366 |
| `arch_seams.py` (new) | the cross-component seam check: `_declared_seam_pairs`, `_norm_endpoints`, the kernel allowlist (`KERNEL_ALLOW` .. `kernel_allow_parse_findings`), `_classifiable_edges`, `_SCAN_CACHE`, `_cross_component_scan`, `cross_component_findings`, `cross_component_advisories` | 145 | LLR-067, LLR-374 |
| `arch_components.py` (new) | the How-SW top view (`TOP_VIEW_MAX`, `_cmp_roots`, `component_top_view`, `knowledge_packs`), the component derivation record, and `component_findings`, which composes them with the seam check | 240 | LLR-049, LLR-172 |
| `trajectory_arch.py` | IF-263's composer: it imports the five modules' names and re-exports them under the same `__all__`, and keeps the spec-boundary rule (`spec_interface_findings` and its helpers) | 220 | LLR-068 |

Import direction, all acyclic and all inside CMP-006: `arch_inputs` imports
`kitlib`, `spine_carrier` and `gen_arch_map`; `arch_interfaces`, `arch_tags`
and `arch_seams` import `arch_inputs`; `arch_components` imports
`arch_inputs` and `arch_seams`; `trajectory_arch` imports all five.
`check_trajectory.py` does not change. Every module stays far under the
1,000-line threshold.

One home for each shared name: the registry paths, dials, loaders, scan
profile and inventory live only in `arch_inputs`; each rule module imports
them. `_SCAN_CACHE` lives only in `arch_seams`; `trajectory_arch` and
`check_trajectory` bind the same dict, so the process keeps one cache. The
optional `gen_arch_map` import keeps its fallback in each module that calls
it (`arch_inputs`, `arch_interfaces`, `arch_tags`, `arch_seams`).

## Interface and design rows

- **IF-263**: owner, requestor and data unchanged. Its `Contract IF-263:`
  body stays in `trajectory_arch` and says the surface is composed from the
  five modules.
- **IF-316** `arch_inputs` -> `trajectory_arch`, `arch_interfaces`,
  `arch_tags`, `arch_seams`, `arch_components`; **IF-317** `arch_interfaces`
  -> `trajectory_arch`; **IF-318** `arch_tags` -> `trajectory_arch`;
  **IF-319** `arch_seams` -> `trajectory_arch`, `arch_components`;
  **IF-320** `arch_components` -> `trajectory_arch`. Each `Drafted`, channel
  `call`, CMP-006, with its `Contracts:` line and `Contract IF-###:` body in
  the owner's docstring.
- **IF-131**: requestors become `check_trajectory`, `arch_inputs`,
  `arch_interfaces`, `arch_tags` and `arch_seams`, the modules that import
  `gen_arch_map`; `trajectory_arch` no longer does.
- **Test cases** (`verifies`, traced): TC-080 cites IF-316 and IF-317;
  TC-409 and TC-410 cite IF-318; TC-067 cites IF-319; TC-049 and TC-166 cite
  IF-320.
- **Design rows** (`module`, traced): LLR-042 names `arch_interfaces.py` and
  `arch_inputs.py`; LLR-049 `arch_components.py` and `arch_inputs.py`;
  LLR-067 `arch_seams.py` and `arch_inputs.py`; LLR-172 `arch_components.py`;
  LLR-365 `gen_arch_map.py` and `arch_tags.py`; LLR-366 `arch_tags.py`;
  LLR-374 `gen_arch_map.py` and `arch_seams.py`. LLR-068 is unchanged.
  `code_symbol` cells name no module and do not change.

## The arms the tests pin

No behaviour changes, so no regression test is written. The proof is the
before/after comparison and the existing tests:

- `check_trajectory.py --strict` on this repository, captured at the base and
  after the change, diffed; and the base's scripts run against the final tree
  (`--root`) beside the final scripts, which must print identical output.
- The existing tests, with only their imports changed:
  `tests/test_seam_import_forms.py` loads `arch_seams` (it patches that
  module's `_SCAN_CACHE` and `gen_arch_map`), and
  `tests/test_trajectory_arch.py::test_architecture_rules_are_reexported_from_their_behavior_module`
  (TC-080) loads each rule's new home and asserts the facade's `__module__`
  names it.
- The ratchets: `tests/test_module_size_ratchet.py` deletes the
  `trajectory_arch.py` entry (now under the threshold) and needs none for the
  new modules; `tests/test_complexity_ratchet.py` and
  `docs/complexity-baseline` re-key the five moved functions to their new
  paths without re-stamping; `tests/test_import_layers.py` must find no new
  cycle and no new deferred import.

## Files

New: `project-trajectory/scripts/arch_{inputs,interfaces,tags,seams,components}.py`.
Changed: `project-trajectory/scripts/trajectory_arch.py`,
`project-trajectory/scripts/kitlib/bootstrap_manifest.py` (the five modules
ship), `project-trajectory/scripts/gen_arch_map.py` and
`project-trajectory/scripts/kitlib/spine.py` (comments naming the moved
functions' homes), `tests/test_seam_import_forms.py`,
`tests/test_trajectory_arch.py`, `tests/test_module_size_ratchet.py`,
`tests/test_complexity_ratchet.py`, `docs/complexity-baseline`,
`docs/requirements/{interfaces,low-level-requirements}.toml`,
`docs/test/test-cases.toml`, `project-trajectory/README.md`,
`project-trajectory/RESYNC_PACK.md`, and the regenerated views.
