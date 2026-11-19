+++
id = "WI-1003"
title = "The seam check resolves dotted and relative imports, so edges into kitlib/* and rendering/* are checked"
workstream = "process"
sr_refs = ["SR-159"]
specref = "docs/plans/2026-11-11-oi130-rescore/README.md#defects-in-the-live-partition"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
planmode = "single"
+++

## Context

Filed by hand on 2026-11-15 (attended, at the owner's request) from defect 2
of the OI-130 re-score record, the first of the three rows the 2026-11-11a
handoff left unfiled (its owner item 3). Its scope critique is owed before a
claim.

`trajectory_arch._classifiable_edges` resolves each `Imports (internal):`
entry by its bare stem against the inventory, so `kitlib.spine` never matches
`scripts/kitlib/spine`. Every import into `kitlib/*` or `rendering/*` is
skipped, and SR-159's "cross-component import no declared interface covers"
goes unreported for those edges. The record counts 10 such edges with no
interface row; three of them are `check_perf` to `kitlib/spine`,
`check_privacy` to `kitlib/secret_classes` and `rejudge` to
`kitlib/observation`. CMP-006's note says the edges into `kitlib/station` and
`kitlib/verdict` are "policed as an interface row"; this check cannot see
them.

Where the fix sits is the plan's to find: `gen_arch_map` emits the import
lines `_classifiable_edges` reads, so the dotted name may already be lost
there.

**The architectural delta** (measured at base `121473dec`). The dotted name is
not lost in `gen_arch_map`. `internal_imports` already emits the import as
written: of the 559 tokens `scan_inventory` hands over for this tree, 278 are
bare stems, 244 are dotted (`kitlib.spine`, `rendering.traj_graph`) and 37
are relative (`.registry`). The name is lost in `_classifiable_edges`, which
looks the whole token up in an index keyed by each module's last path
segment, so any token holding a dot misses. `scan_inventory`'s record shape
and its `imports` value domain do not change, so IF-028 (`check_doc_refs`'s
`sym:` oracle) and IF-132 (the dashboard's module source) are untouched, as is
IF-263 (`trajectory_arch`'s rule surface to `check_trajectory`), whose
findings change in content but not in shape.

The fix is one resolver for the token grammar, in the module that defines the
grammar: `gen_arch_map.resolve_import`, which `_classifiable_edges` calls.
`gen_arch_map` already holds a resolver of the same tokens, the dependency
diagram's `_resolve_import`, which takes the first match when several modules
end in the same path and resolves a relative import written in a package's
`__init__.py` one level too high. A second resolver beside it would be the
two-homes defect the re-score records as defect 3, so the diagram calls the
new one and `_resolve_import` is deleted. The call adds no import edge:
`trajectory_arch` imports `gen_arch_map` today. IF-131 (the call surface the
spine checks read from `gen_arch_map`) gains `resolve_import` in its `data`
cell and its `Contract IF-131:` body. The interface reference and
`components.derived.toml` regenerate from the changed registry rows.

## Done-when

- [ ] A dotted import (`import kitlib.spine`, `from kitlib import spine`,
      `from kitlib.spine import x`) and a relative import inside a package
      resolve to their inventory module, and the cross-component rule
      classifies the edge. A bare stem resolves as today; an unknown or
      ambiguous name is still skipped. The form space is closed:
      - **In scope:** every `ast.Import` and `ast.ImportFrom` node in a
        scanned module, at module level or inside a function, as
        `gen_arch_map.internal_imports` turns it into a token. That function
        is unchanged. `import a.b.c` and `import a.b.c as x` give `a.b.c`.
        `from a.b import n` gives `a.b.n` when `n` is a scanned module or
        package name other than `b`, and `a.b` otherwise. A relative import
        (`level` 1 or more, with `module` present or `None`) gives the same
        shape behind `level` dots: `.m.n`, `.m`, `.n`, `.`.
      - **Absolute token:** try its dotted prefixes longest first, each as a
        path (`kitlib.spine` as `kitlib/spine`), against the inventory's
        normalized module paths, matching a path equal to it or ending in
        `/` plus it. The first prefix that matches decides: one module is the
        target; more than one is ambiguous and the edge is skipped. No match
        at any prefix is unknown and the edge is skipped. A one-segment token
        is today's bare-stem rule exactly. The fallback is why
        `from kitlib.spine import x` lands on `kitlib/spine`, and why
        `from traj_parse import schedule` (a function that shares a module's
        stem) lands on `traj_parse`, not on `schedule`.
      - **Relative token:** the importer's package is the importer itself
        when it is a package (an inventory module sits under its path), and
        its parent otherwise. Each dot past the first climbs one more level,
        and a climb past the scan root's top is skipped. The target is the
        package path plus the token's segments, matched exactly (no suffix
        match), dropping trailing segments down to the package itself. No
        exact match is unknown and the edge is skipped.
      - **Outside the bound:** an import naming no scanned module or package
        (`gen_arch_map` emits no token for it), `importlib` or `__import__`
        calls, `sys.path` changes, and a name that reaches a module only
        through an alias assigned at run time. None of these is an edge.
- [ ] Each edge this makes visible to the cross-component finding tier (its
      endpoints' component sets disjoint, the edges the record counts under
      defect 2) is declared in this row and none is deferred: by an interface
      row (a new row is `Drafted`), or, for a destination imported from every
      component by design, by a reasoned `docs/kernel-modules-allow` entry,
      the reuse provision OI-48 ruled. An edge this makes visible to the
      multi-membership advisory tier (the component sets overlap and an
      endpoint carries several tags) is reported warn-only, as the rule
      already does, and the Deliverable gives the count. Those edges are the
      record's defect 1 ("194 cross-component edges reach only the warn-only
      advisory"), a question about the partition rather than a missing seam.
      The resolver, the declarations and the CMP-006 note land together, and
      the row lands with `trace.py --strict` and `check_trajectory.py
      --strict` clean.
- [ ] CMP-006's note matches what the check now sees.
- [ ] Regressions name each import form above, and the unchanged bare-stem,
      unknown and ambiguous cases.

## Critique dispositions

Round 1 (Gemini Argon, attended, 2026-11-19,
`docs/reviews/2026-11-19-scope-critiques/WI-1003.md`): CHANGES-REQUESTED, four
MAJORs.

- **S3, the import-form space: adopted.** The first Done-when item now closes
  the space over `ast.Import` and `ast.ImportFrom` as `internal_imports`
  tokenizes them, states the resolution of an absolute token and of a relative
  one (`level` 1 or more, with `module` present or `None`), and states the
  default: a token that resolves to no inventory module, or to more than one,
  is skipped. Each case the critic named has its answer there. A relative
  import with `module = None` is `.n` or `.`. A climb of more than one level
  drops one segment per extra dot, and a climb past the top is skipped. An
  alias changes nothing, since the token is the module path. A symbol leaf
  falls back to its module. The bound is the static `import` statements of
  the scanned tree; a dynamic import, a `sys.path` change and an alias bound
  at run time are outside it. `gen_arch_map` and `trajectory_arch` cannot
  disagree on the token, because one function resolves it for both the seam
  check and the dependency diagram.
- **S4, `planmode`: adopted as `planmode = "single"`.** The row promises
  behaviour over an input space and touches two modules joined by an
  interface row, plus the registries.
- **S5, the architectural delta: adopted.** Stated in the Context. The
  `imports` value domain and the record shape do not change, so IF-028 and
  IF-132 are untouched. IF-131's surface gains `resolve_import`. The dotted
  name is lost in `_classifiable_edges`, not in `gen_arch_map`'s import lines.
  The interface reference and `components.derived.toml` regenerate. Measured
  at base `121473dec`, the fix surfaces 7 finding-tier edges (the record
  counted 10 on its 2026-11-11 tree): `agent_common` and `check_privacy` to
  `kitlib/secret_classes`; `check_perf` and `check_test_first` to
  `kitlib/spine`; and `rejudge`, `coordinator_guard` and `kitlib/guard_hooks`
  to `kitlib/observation`. All 7 are declared in this row. No refactor row is
  owed on trunk first.
- **B2, the deferral escape: adopted.** "or is named in the Deliverable with
  the successor row filed for it" is gone from the second Done-when item, so
  every finding-tier edge the fix surfaces is declared in scope. The item now
  records the S1 keep-together: the resolver, the declarations and the
  CMP-006 note land as one deliverable, which `--strict` needs. The item also
  says how an edge is declared: an interface row, or a reasoned kernel entry
  for a destination imported from every component, the path the critic's own
  S5 text offers. The advisory tier is named rather than left to inference,
  and is sent to the record's defect 1, whose count it already is. This does
  not narrow the row: the record counts defect 2's edges as the live
  single-tag cross edges, which is the finding tier.
