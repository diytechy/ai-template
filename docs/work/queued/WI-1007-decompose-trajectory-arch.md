+++
id = "WI-1007"
title = "trajectory_arch.py is split by the checks it holds, each module under the size line, with no change of behaviour"
workstream = "process"
sr_refs = ["SR-159", "SR-165"]
specref = "docs/plans/2026-11-11-test-tiers/HANDOFF.md#122-rulings-taken-on-2026-11-15-and-2026-11-16"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
+++

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

- [ ] `trajectory_arch.py` is split along the checks it holds, and every
      module that results is under the ratchet's threshold. The public names
      callers import still resolve, or every caller moves in the same change.
- [ ] Behaviour is unchanged. `check_trajectory.py --strict` prints the same
      findings on this repository before and after. The existing tests pass,
      with only their imports changed.
- [ ] Each LLR whose `module` or `code_symbol` binds a moved symbol names
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
