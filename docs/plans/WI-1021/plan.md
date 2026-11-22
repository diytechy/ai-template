# WI-1021 plan: each file declares its one component, and membership is read from the declarations

Planned on branch `maint/wi-1021` at `1aa6c439a`, cut from `refactor_again`
at the same commit. A maintenance-branch build (`planmode = "single"`): no
plan critique or pass record. The one-component table the operator rules is
its own file, [component-table.md](component-table.md); the lane builds on
its picks and does not wait for the ruling.

## What reads membership today, from the code

`kitlib.spine.module_components(llrs)` joins each design row's `module` cell
to its `component` cell (LLR-373). Its callers:

- `arch_components.component_top_view`: the How-SW top view, its bound and
  the knowledge-pack coupling (LLR-049), which `check_trajectory` and the
  dashboard (`traj_views`, through `trajectory_arch`) both read;
- `arch_seams._classifiable_edges`: the cross-component rule (LLR-067,
  LLR-374) and its multi-membership advisory (WI-440);
- `gen_components.build`: seam placement in the derived component view
  (LLR-199). The view's `modules` list is a second membership read, from the
  member design rows' `module` cells.

**`derive_stage` reads no membership.** The DevStg-Arch rung
(`spine_rules.arch_incomplete`) reads the component rows' `status` and
`standing` only; neither `derive_stage` nor `spine_rules` calls
`module_components` or reads a file's component. The membership-bearing
checks at DevStg-Arch are the component rules above, which `check_trajectory
--strict` runs. So the spec's "the DevStg-Arch derivation" has nothing to
switch, and `derive_stage.py` is not changed; LLR-172 (the derivation
record, read off the component rows alone) states no membership source and
is not amended.

## The design

**The grammar and its one reader** (`gen_arch_map`, beside
`module_contracts` and `header_lines`):

- `COMPONENT_RE`: a line, stripped, reading exactly `Component: CMP-NNN`,
  the digits as the CMP id space spells them (`CMP-\d+`, `trace.py`'s
  pattern).
- `component_declaration(lines)` returns `(component, problem)`. A stripped
  line opening `component:` in any case that is not exactly the form is
  malformed; two exact lines are doubled; none is absent. A malformed line
  beside an exact one leaves the file undeclared: a file with a bad line has
  no trustworthy declaration.
- `file_component(path)` is the one reader: a `.py` file's module docstring
  (read with `tokenize`, the first statement's string literal, so the reader
  costs one token pass rather than a full parse), any other file's
  `header_lines`, the existing carrier reader the `Contracts:` grammar uses.
  That reader already strips `#` (`.sh`, `.command`, `.ps1`, `.toml`,
  `.ini`, `.csv`, suffixless), `REM` and `::` (`.cmd`), `<# #>` (`.ps1`) and
  the opening `<!-- -->` (`.md`), and skips a shebang or `@echo off`.
- `COMPONENT_TYPES`: the grammar's file types, closed: `.py`, `.sh`,
  `.command`, `.ps1`, `.toml`, `.ini`, `.csv`, `.cmd`, `.md` and no suffix.

**The scope and its census** (`arch_inputs.component_headers(root)`, the
architecture rules' input home):

- The scope, closed: every file under `[paths] src` (hidden parts and
  `__pycache__` skipped) of a grammar type, `README.md` excluded; and every
  non-directory file owner `gen_arch_map.owner_files` reads from the
  interface registry (13 today; a directory owner is read through its
  `README.md`, which is documentation).
- It returns `(declared, findings)`: `{repository-relative path: CMP id}`
  for each in-scope file with a valid declaration naming a live component
  row (`load_cmps`), and one finding per in-scope file that is absent,
  doubled, malformed or names an id no live row has. A file of another type
  under `[paths] src` is outside the rule unless its header states a
  `Contract IF-NNN:` body, which is then a finding naming its type.
- Vacuous, `({}, [])`, with no live component row: a project below
  DevStg-Arch has no partition to declare into. A file outside the scope may
  carry a declaration; `file_component` judges it by the same grammar
  wherever it is read, and the census does not walk for it.
- The findings join `component_findings`: WARN at a plain run, ERROR under
  `--strict`, the `[checks] components_check` opt-out, exactly as the
  cross-component rule they feed. In this repository `check_trajectory
  --strict` runs at every commit's checks; an adopter's gate adds `--strict`
  at its own rung (`check.py`).

**The membership home** stays `kitlib.spine.module_components`, its input
changed: `module_components(declared)` takes the census's `{path: CMP id}`
pairs and returns `{normalized key: {CMP ids}}`, keyed by `norm_module`
exactly as before, so every caller's lookups are unchanged. It still reads
no file itself (it is on the shared kernel and may not import upward), and
still drops a token not starting `CMP-`.

**The consumers, under the Trust ruling** (a file whose declaration is
absent or invalid belongs to no component):

- `component_top_view` reads `module_components(component_headers(root)[0])`;
  an undeclared module is uncontained.
- `_classifiable_edges` yields every resolved internal edge, membership or
  not; `_cross_component_scan` classifies: an edge with an endpoint in no
  component is a finding naming it as unclassified, before cover and the
  kernel are consulted (never internal, never exempt); otherwise a covered
  pair or a kernel destination is silent; an edge is internal only when
  both endpoints are in the same one component; anything else is the
  existing finding. So a key two files share (`norm_module` strips the
  suffix: `check.py` and `check.sh` meet on one key) can never silence an
  edge the way a second tag did.
- **The multi-membership advisory retires** with its cause:
  `cross_component_advisories`, its re-export in `trajectory_arch`, its
  line in `check_trajectory`'s warn loop, and IF-319's `data` and body
  mention.
- `gen_components.build` takes the declarations: seam placement and each
  component's `modules` read them. The design rows' `component` cell still
  places design rows and their requirements in the view (`llr_refs`,
  `sr_refs`, `hat_refs`) until WI-1023 derives placement; no check compares
  a cell with a header. `gen_components` reaching `arch_inputs` is a new
  edge from CMP-009 into CMP-006, covered by adding `gen_components` to
  IF-316's requestors (a `Drafted` row, the rule surface's input seam).

## The headers written (the migration)

167 files, each picked in [component-table.md](component-table.md). A
scratch script (not shipped) inserts one line per file, preserving each
file's line endings and byte-order mark:

- a Python module: a `Component: CMP-NNN` paragraph immediately before the
  paragraph holding the `Contracts:` marker, else as the docstring's last
  paragraph (blank lines either side, so no contract body swallows it);
- a `#` header: `# Component: CMP-NNN` as the header's first line (after a
  shebang), followed by a bare `#`;
- a `.cmd` file: `REM Component: CMP-NNN` as line 2, after `@echo off` and
  before `setlocal`, which is where `header_lines` reads the block;
- `gen_arch_map.reference.ps1`: `# Component: CMP-006` above its `<#` help
  block, so the help block keeps opening with `.SYNOPSIS`;
- a Markdown file: the first line inside the opening `<!--`, then a blank.

The kernel allowlist is unchanged.

## No new silence

The lane's simulation of the new rule over the live import graph at
`1aa6c439a` (every file's pick, the declared seams, the kernel) finds three
edges the picks turn into uncovered crossings. Each is covered:

- `acceptance_record` -> `kitlib/done_when` reads the private digest width
  `_DIGEST_CHARS`, so the record's text digest and the Done-when digest are
  one width. No row states it: a new `Drafted` `call` row, **IF-326**, owner
  `scripts/kitlib/done_when`, requestor `scripts/acceptance_record`, with its
  `Contract IF-326:` body in `done_when`'s header and **TC-461** citing it.
- `agent_policy` -> `kitlib/authority`: IF-195 (`Drafted`) states exactly
  the surface called; `agent_policy` joins its requestors. A second row for
  the same call would duplicate IF-195 in intent.
- `id_carrier` -> `kitlib/provenance` (`with_loop_trailer`): IF-194
  (`Drafted`) names the symbol; `id_carrier` joins its requestors.

The edges the multi-membership advisory listed (37 at `1aa6c439a`) all
become internal or one of these three. `trace.py --strict` and
`check_trajectory --strict` stay clean.

## Spine rows

New, `Drafted`, phase 6, `component = "CMP-006"`, under SR-159
("Declared-architecture connectivity gaps are reported"):

- **LLR-396**, the declaration's grammar and its one reader: the line, the
  carriers by type, the three per-file classes the reader returns.
- **LLR-397**, the scope and the census: the closed scope, the four finding
  classes and the other-type finding, vacuity, severity and the opt-out.
- **TC-457** (LLR-396): each carrier syntax read, each problem class.
- **TC-458** (LLR-397): the scope's edges, each finding red before the code
  and named, vacuity, WARN plain and ERROR under `--strict`.
- **TC-459** (LLR-373, LLR-067): membership from the declarations through
  the one join, and the Trust ruling: an edge touching an undeclared module
  is reported as unclassified, before cover and the kernel; a shared key
  silences nothing.
- **TC-460** (LLR-199): the component view's `modules` and seam placement
  read the declarations.
- **TC-461** (LLR-359, IF-326): the record's digest and the Done-when
  digest are one width.
- **IF-326**, above.

Amended `Accepted` rows, text only, each drifting for automated
adjudication:

- **LLR-373**: the join's input is the declarations, not the design rows.
- **LLR-067**: membership from the declarations; the unclassified edge; an
  edge is internal only inside one component.
- **LLR-199**: the view's `modules` and seam placement read the
  declarations.
- **TC-435**: its method and evidence follow the join's new input.
- **TC-067**: its method drops the advisory, and its evidence drops the
  retired advisory test.
- **TC-195**: "membership comes from the design tier's Component tag ...
  and the modules follow" becomes the declarations.
- **CMP-006** `notes`: the sentences describing membership by design-row
  tags and the multi-membership advisories are rewritten (Done-when 5);
  the file names it carries stay for WI-1028.

Read and left unamended, because no sentence of theirs names the membership
source: **LLR-374** (import resolution; its "skips an import that resolves
to None or to the importing module itself" stays true), **LLR-049** (the
bound and its vacuity), **LLR-172** (the derivation record), **TC-049** and
**TC-436** (whose "tag one importer into one component" the header does).
`Drafted` rows edited, no act: IF-194, IF-195, IF-316, IF-319.

Ids: LLR-396 and LLR-397, TC-457 to TC-461, IF-326, then `trace.py --root .
--bump-ids`.

## Documents

- `PROCESS.md` §8, once: the header that holds a file's `Contracts:`
  marker also names its one component, `Component: CMP-NNN`, and from
  DevStg-Arch every source file and file owner carries it.
- `PROCESS_OPTIONS.md` "Component layer": software membership is the file's
  header; the unclassified edge; the advisory retired; "uncontained" is a
  module with no valid declaration. Byte deltas reported, both watched rows
  re-stamped.
- A RESYNC entry, the first of variant F's: the grammar, headers owed from
  DevStg-Arch, the advisory gone, and that the kit's own shipped files carry
  the kit's ids (as their `Contracts:` markers already do).

## Tests, red first

`tests/test_component_headers.py` (new, in-process): each carrier, each
reader class, each census finding, the scope's edges, vacuity, the
other-type finding, the unclassified edge and membership from headers.
Then the existing fixtures move from design-row tags to headers:
`test_trajectory_arch.py` (top view, coupling, containment, cross-component,
kernel, the overlap block retired), `test_components_registry.py` (the
join), `test_gen_components.py`, `test_seam_import_forms.py`,
`test_traj_views.py`. Every module importing a changed module runs, plus
`test_import_layers.py`, `test_module_size_ratchet.py`,
`test_dogfood_sync.py`, `test_bootstrap.py` and `run_menu.py smoke`.

## Order of work

1. This plan and the table, committed.
2. Red tests for the reader, the census and the edge rule; then the code.
3. The headers, the interface and spine rows, the documents, the regenerated
   views.
4. The close: Deliverable, spec moved, log fragment. Review waits for the
   operator's ruling on the table, recorded in the spec's Context.
