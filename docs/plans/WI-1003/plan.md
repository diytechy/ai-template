# WI-1003 plan: one resolver for the import token, so the seam check sees dotted and relative imports

Planned on the maintenance branch `maint/wi-1003`, base `121473dec`, against
the spec as its critique dispositions left it (`10204665b`). Figures marked
measured were taken at the base by a scratch script over `arch_inventory`.

## The construction

1. **`gen_arch_map.resolve_import(token, importer, modules)`** returns the one
   inventory module `token` names from `importer`, or None. `modules` is the
   collection of module paths in the map's grammar (`scripts/kitlib/spine`).
   Two helpers keep each arm short:
   - `_resolve_absolute(token, modules)`: the dotted prefixes, longest first,
     each matched as a path equal to the candidate or ending in `/` plus it.
     The first prefix with a match decides: one match is the answer, several
     are None.
   - `_resolve_relative(token, importer, modules)`: the package is the
     importer when an inventory module sits under `importer + "/"`, else its
     parent. Each dot past the first climbs one level, and a climb past the top
     is None. Then exact matches of the package plus the tail, trimming the
     tail down to the package itself.

     *Corrected at review:* guessing package-ness from the modules under the
     importer misses a package's `__init__.py` with nothing inventoried under
     it. The built rule reads it from the files: `package_paths(src_roots)`
     gives the module paths whose file is an `__init__.py`, and
     `resolve_import` takes them as a fourth argument.

   The diagram's `_resolve_import` is deleted and `build_dependency_diagram`
   calls `resolve_import`. The diagram changes in two places only, both in the
   direction of the seam check: several modules ending in the same path now
   draw no arrow instead of the first one's, and a relative import in a
   package's `__init__.py` now draws its arrow. Measured with a prototype of the
   new resolver: over this repository's scan root both resolvers draw the same
   557 import arrows (no committed document splices the diagram, so this is a
   check, not a regeneration).

2. **`trajectory_arch._classifiable_edges`** drops its last-segment index and
   resolves each token with `gen_arch_map.resolve_import` against the
   normalized inventory, with the normalized importer. IF-131 promises that
   every `gen_arch_map` entry point is optional at the call site, so an older
   `gen_arch_map` without `resolve_import` makes the rule silent, the posture
   `arch_inventory` already takes when the module is missing. No local join is
   reintroduced: membership stays `kitlib.spine.module_components`.

## The declarations (Done-when 2), measured at the base

| Finding-tier edge | Declared by |
|---|---|
| `agent_common`, `check_privacy` -> `kitlib/secret_classes` | IF-314, new: `kitlib/secret_classes`'s `SECRET_CLASSES` table as a call |
| `check_perf`, `check_test_first` -> `kitlib/spine` | `docs/kernel-modules-allow` entry for `kitlib/spine.py` |
| `rejudge` -> `kitlib/observation` | IF-214 gains `scripts/rejudge` as a consumer (it reads the records through `read_records`, `latest`, `parse_utc` and `OBSERVATIONS_DIR`) |
| `coordinator_guard`, `kitlib/guard_hooks` -> `kitlib/observation` | IF-315, new: `write_atomic` as a call (neither writes an observation record) |

Why a kernel entry for `kitlib/spine.py` and interface rows for the rest:
`spine.py` is imported by 43 modules across all four components. OI-48 ruled
that re-declaring such a module edge by edge restates "everyone imports the
shared helper" once per caller. CMP-006's accepted note already says this
module's consumption is recorded on the kernel surface. `secret_classes.py`
has two consumers, and `observation.py` three outside its component, so a row
names them. That is the kernel file's own precedent for `kitlib/station.py`,
kept off the surface because its consumer set is narrow.

Each new row gets a `Contracts:` declaration and a `Contract IF-###:` body in
its owner's docstring. Each needs a TC citing it, or the seam-TC rule fails
`--strict`. Each is cited from the existing TC that already drives it, by a
traced `verifies` cell: TC-201 (drives `check_privacy` and `agent_common`
against the shared table) cites IF-314, and TC-229 (drives `write_atomic`'s
bounded retries) cites IF-315.

The advisory tier, measured: the fix surfaces 55 multi-membership advisories
beside the base's 25, and the `spine.py` kernel entry clears 41 of them.
*Corrected after the build, re-measured on the final tree:* IF-315's endpoint
pairing also covers `coordinator_guard` to `kitlib/guard_hooks`, so 42 of the
55 are cleared and 13 remain. IF-131's new requestor covers one of the 25 base
advisories (`trajectory_arch` to `gen_arch_map`), so 24 remain. That gives 37
in all. The 13 are reported and not declared (the spec's second Done-when
item).

## Registry rows

- LLR-374 (`Drafted`, SR-159, CMP-006): the resolution rule. `module` names
  `gen_arch_map.py` and `trajectory_arch.py`, and `code_symbol` names
  `resolve_import/_classifiable_edges`; both carry `Implements: SR-159,
  LLR-374`. Test refs TC-436.
- TC-436 (`Drafted`): verifies SR-159 and LLR-374; evidence
  `tests/test_seam_import_forms.py`.
- IF-314, IF-315 (`Drafted`), as above. IF-214 and IF-131 amended (IF-131's
  `data` cell and its contract body name `resolve_import`).
- CMP-006's note rewritten to what the check sees (an amendment: the row stays
  `Accepted`).
- TC-437 is allotted and not needed.

## The arms the tests pin (`tests/test_seam_import_forms.py`, TC-436)

One fixture tree, scan root `scripts`: a package `kitlib` with `spine.py` and a
nested package `deep`, a top-level `helper.py`, two `util.py` in two packages,
and an empty `blank.py`. Each case adds one importer tagged CMP-001, with every
other module CMP-002, and runs `cross_component_findings` in process. A resolved
case asserts the finding naming its importer and target. A skipped case asserts
no finding names its importer.

- Resolved: `import kitlib.spine`; `import kitlib.spine as s`;
  `from kitlib import spine`; `from kitlib.spine import go`;
  `from kitlib.spine import helper` (a name sharing a module's stem falls back
  to the module it is imported from); `from .spine import go`;
  `from . import spine`; `from .. import spine` from `kitlib/deep/`;
  `from . import spine` in `kitlib/__init__.py`; the bare stem `import helper`.
- Skipped: the ambiguous bare stem `import util`; the ambiguous dotted
  `import pkg.util` (two modules end in `pkg/util`); the unknown `import blank`
  (an empty module, scanned but not in the inventory); and a relative climb
  past the top.
- One case runs the rule with `resolve_import` removed from `gen_arch_map` and
  asserts silence (the IF-131 posture).
- One case draws the dependency diagram for the `__init__.py` relative import,
  the arrow the deleted resolver missed, so the diagram is pinned to the one
  resolver.

Red first: the dotted, relative and fallback cases fail on the base (the rule
sees no edge) and `resolve_import` does not exist. The bare-stem, ambiguous and
unknown cases pass on the base, which is the point: they pin today's answer.

## Files

`project-trajectory/scripts/gen_arch_map.py`,
`project-trajectory/scripts/trajectory_arch.py`,
`project-trajectory/scripts/kitlib/secret_classes.py` and
`project-trajectory/scripts/kitlib/observation.py` (docstrings only),
`tests/test_seam_import_forms.py`, `tests/test_module_size_ratchet.py`
(re-stamps), `docs/requirements/{interfaces,components,low-level-requirements}.toml`,
`docs/test/test-cases.toml`, `docs/kernel-modules-allow`,
`project-trajectory/RESYNC_PACK.md`, and the regenerated views.
