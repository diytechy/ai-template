## 2026-11-19 — WI-1003: the seam check resolves dotted and relative imports through one resolver, gen_arch_map.resolve_import, and the seven edges it surfaced are declared

Deferred open items: none.

Built on the maintenance branch `maint/wi-1003`, cut from `refactor_again` at
`121473dec`, outside the lane workflow at the operator's direction: no claim,
no lane review rounds, commit hooks on. The parent session reviews and merges.

- **The critique.** Gemini Argon's round 1 raised four MAJORs, and all four
  were adopted:
  - S3: the Done-when closes the import-form space over `ast.Import` and
    `ast.ImportFrom` as `internal_imports` tokenizes them, with the default
    (skip what resolves to no module, or to several) and the bound (the static
    imports of the scanned tree).
  - S4: `planmode = "single"`.
  - S5: the Context states the delta. `gen_arch_map` never lost the dotted
    name. Of the 559 tokens at the base, 244 are dotted and 37 relative;
    `_classifiable_edges` lost them by looking each token up by its last path
    segment.
  - B2: the successor-row escape is gone, and the finding-tier edges are
    declared in the row.
- **The resolver.** `gen_arch_map.resolve_import` tries an absolute token's
  dotted prefixes longest first, as paths matched exactly or by suffix. The
  first prefix that matches decides, and two matches are ambiguous. A relative
  token starts from the importer's package, where a package's `__init__` is
  its own package. It climbs one level per extra dot and matches exactly. The
  dependency diagram's `_resolve_import`, which took the first of several
  matches and anchored an `__init__`'s relative import one level too high, is
  deleted, and the diagram calls the one resolver. Over this repository both
  draw the same 557 arrows.
- **The rule.** `_classifiable_edges` resolves through it and skips an edge
  from a module to itself. With a `gen_arch_map` that lacks the resolver, the
  rule is silent (IF-131's optional entry points).
- **What it surfaced.** At the base the rule reported 0 findings and 25
  advisories. With the resolver it reports 7 findings and 80 advisories.
- **The declarations.**
  - IF-314 (new) covers `kitlib/secret_classes` for `check_privacy` and
    `agent_common`.
  - IF-315 (new) covers `kitlib/observation`'s `write_atomic` for
    `coordinator_guard` and `kitlib/guard_hooks`.
  - IF-214 gains `rejudge` as a consumer.
  - `kitlib/spine.py` joins `docs/kernel-modules-allow`. It is imported by 43
    modules across all four components, and CMP-006's accepted note already
    placed it there.
  - IF-131 gains `resolve_import` and its real requestor, `trajectory_arch`.

  After them: 0 findings and 37 advisories. 13 of the 37 are edges the fix
  surfaced into modules that carry several components' tags. Those belong to
  the record's defect 1, not to a seam row.
- **Rows.** IF-314, IF-315, LLR-374 and TC-436 are new and `Drafted`. TC-201
  and TC-229 cite the two new seams (traced `verifies`). CMP-006's note is
  amended to what the check sees and stays `Accepted`, waiting on the
  operator's re-accept. TC-437 was not needed.
- **Sizes.** `gen_arch_map.py` 1581 to 1593 SLOC (a reviewed bump: the
  resolver) and `trajectory_arch.py` 1130 to 1124 (re-stamped down).
  `_classifiable_edges` leaves the complexity baseline.
- **RESYNC.** "The seam check resolves dotted and relative imports",
  anchored at `121473dec`. An adopter with packages may see new findings
  under `--strict`. For each, they declare the row, retag, or add a kernel
  entry, and they overwrite `gen_arch_map.py` and `trajectory_arch.py`
  together.
- **A test hazard, found and contained.** `trajectory_arch` caches its
  cross-component scan per root path for the process. Under this repository's
  `tmp_path_retention_policy = failed`, pytest hands a passed test's directory
  name to the next test, so an in-process test of the rule reads a stale
  scan. The new test module resets the cache per test. The cache itself is
  unchanged.
