# WI-1022 plan: interface rows name components, and internal `call` rows retire

Planned on branch `maint/wi-1022` at `1b15d07fb`, cut from `refactor_again`
at the same commit. A maintenance-branch build (`planmode = "single"`): no
plan critique or pass record. Counts below are read from the tree at
`1b15d07fb`: 270 interface rows (269 `Drafted`, IF-312 `Accepted`), 134 of
them `call` rows; the spec's 269 and 133 predate IF-326.

## 1. The migration rule (Done-when 1 and 2)

Every endpoint cell (`owner`, `requestors`, `consumers`) is rewritten once,
by this rule, and the `component` cell is deleted from every row:

1. An `external:<party>` endpoint stays as written.
2. A path naming a file that declares a live component in its `Component:`
   header (WI-1021) becomes that component. The registry spells modules
   without the kit prefix and suffix (`scripts/check` is
   `project-trajectory/scripts/check.py`; `hooks/pre-commit` is
   `project-trajectory/hooks/pre-commit`). A generated file was already owned
   by the module that writes it, so its row takes the writer's component.
3. A directory or file-channel owner with no header of its own becomes its
   producing component (table 1.1). A hand-edited file is owned by the
   component its own header declares (pointer rules), so the 13 file owners
   take their headers' components.
4. A file outside every component's scope is mapped as table 1.2 says.
5. A cell's entries are de-duplicated, first occurrence kept. The far side's
   key (`requestors` or `consumers`) is unchanged, so every row keeps its
   direction.

### 1.1 The producing components (directory and file-channel owners)

| Owner today | Rows | Producing component | Why |
|---|---|---|---|
| `docs/requirements/`, `docs/requirements` | IF-021, IF-033, IF-034, IF-051, IF-059 (and IF-103's consumer) | CMP-006 | the spine registries; their reader, `spine_carrier`, and the rules that decide whether they hold are CMP-006. IF-059's `component = CMP-008` was a placement (the planner reads it), not a producer |
| `docs/test/` | IF-161 | CMP-006 | the test-case tier is a spine registry, read through the same carrier |
| `docs/work/` | IF-023, IF-024, IF-054, IF-079, IF-159 | CMP-006 | `wi_convert`, the format's single writer (IF-159's own body), and `kitlib/registry`, its reader, declare CMP-006 |
| `docs/reviews/` | IF-047, IF-160 | CMP-008 | the review machinery that writes and scores the records (`score_reviews`, the scoreboard's single writer; `kitlib/verdict`; `review_brief`) declares CMP-008 |
| `docs/log.d/` | IF-156, IF-168 | CMP-008 | `trunk_step`, which compiles and removes the fragments a session adds, declares CMP-008 |
| `docs/` | IF-030 | CMP-009 | the hand-written documentation tree, "everything a person reads" (CMP-009's notes) |
| `project-trajectory/scripts` | IF-025, IF-026 | CMP-006 | the source root as the inventory surface, whose walk (`gen_arch_map`) decides the architecture rules |
| `project-trajectory/skills/` | IF-035 | CMP-009 | the skills an adopter receives; both readers (`bootstrap`, `gen_skills_index`) declare CMP-009 |
| `registries` | IF-039 | CMP-009 | the blank templates a scaffold copies; `bootstrap` declares CMP-009 |
| the 13 file owners | IF-022, IF-029, IF-031, IF-037, IF-038, IF-045, IF-049, IF-057, IF-068, IF-070, IF-072, IF-073, IF-134, IF-135, IF-162, IF-163 | each file's header | `docs/stack.ini`, `docs/coverage-floors`, `docs/declared-absences` and the two hooks CMP-007; `docs/process.toml`, `docs/agents.toml`, `docs/agents-enabled` and `docs/status.md` CMP-008; `docs/runtime-flows.md` CMP-009; the three registry files CMP-006 |

### 1.2 Endpoints outside every component's scope

| Endpoint | Rows | Becomes | Why |
|---|---|---|---|
| `hooks/commit-msg` | IF-197, IF-298 | CMP-007 | a shipped hook outside the census scope (it is no file owner); its two sibling hooks declare CMP-007, and CMP-007's notes name the shipped hooks |
| `scripts/coordinator/codex_call`, `scripts/coordinator-relaunch.cmd`, `scripts/coordinator-relaunch.sh` | IF-246, IF-282, IF-278, IF-279 | `external:coordinator` | this repository's own coordinator tooling under the root `scripts/`, outside the shipped kit and every component's scope; the coordinator is already a declared party |
| `tests/test_dogfood_sync.py` | IF-072 | dropped | a test file is evidence, not a component; the row keeps its two kit consumers. The rationale naming the test file is WI-1028's (row text) |

### 1.3 The party list

The registry header declares the closed list, one line per party, reading
exactly `# External party: <name>`: the seven in use (`agent CLI`,
`coordinator`, `downstream adopter`, `git`, `run.* launcher templates`,
`run.* launchers`, `upstream docs`). `trace.py` reads the lines of the
registry's leading comment block; the shipped template documents the line
and declares none.

### 1.4 What "no file in any cell" covers

Done-when 2's "IF rows name no file in any cell (ruling 5)" is read as the
endpoint cells and the retired `component` cell, which this row rewrites.
The `data` cell's form is WI-1025's ("A form names no file ... WI-1022 took
file names out of the endpoint cells", its Done-when 6), and file and code
names in `rationale` and `notes` are WI-1028's commit check and rewrite. The
endpoint rule makes a path in an endpoint cell a finding.

### 1.5 The accepted row

IF-312 (`Accepted`) is a crossing `call` row (CMP-006 owner, CMP-007
requestor) and stays; its owner, requestor and `component` cells change, text
only, and it drifts for adjudication.

## 2. The checks

### 2.1 The endpoint form (`trace.py`, LLR-041)

`interface_findings` holds every endpoint to exactly one of two forms: a
`CMP-###` id that a real row of the component registry has, or `external:`
followed by a party the header declares. Each other endpoint is a strict
finding naming the row, the cell and the reason: a requirement or design id
(revision 35's "never a requirement id", kept as its own message), an id no
component row has, a bare or undeclared party, or anything else (a path or a
module). The owner stays one endpoint, the row with no in-tree endpoint (all
`external:`) stays refused, and the direction advisory stays. The retired
`component` cell joins the retired-cell finding (key presence). Retired as
untrue under component owners: the module-owner advisory (`_implementing_modules`),
`if_endpoint_class_advisories` and `trace_text`'s `module_endpoints` and
`_module_shaped`, their only caller. The party list rides `Registries`
(`if_parties`), so `analyze` stays free of I/O. The two pure predicates
(`declared_parties`, `endpoint_problem`) live in `trace_text`, beside
`EXTERNAL_ENDPOINT_PREFIX`.

### 2.2 The scan surface, one list for two rules (LLR-397, LLR-398)

Today the contract scan reads the modules under `[paths] src` plus the file
owners the registry names, and the component census scope takes the same
file owners. Owners stop being files, so the files outside the source walk
are declared instead: `docs/stack.ini` `[arch-map] headers`, a
whitespace-separated list of repository-relative paths, beside `[arch-map]
mode` (the scan profile's home). The template documents it, commented out;
absent means none. One reader, `gen_arch_map.declared_headers(root)`.

The surface is: every file under `[paths] src` of a type the `Component:`
grammar has a carrier for (`README.md` excluded, hidden parts and bytecode
caches skipped) plus each listed file. The census scope and the contract
scan both read exactly that set. A listed path that does not exist is a
census finding. The approval snapshot, `docs/reviews/`, `docs/plans/` and the
example documents are outside it because nothing outside `[paths] src` is
read unless listed. This repository lists the 13 file owners and the
README files that state contracts for the directory owners kept in place
(below).

### 2.3 One body per interface (`arch_interfaces`, new LLR-398)

`contract_body_findings` becomes:

- **Uniqueness.** At most one file on the surface states each
  `Contract IF-NNN:` body. Zero is valid (the row's `data` cell is the
  contract's home until WI-1025's hand-over). Two or more is one finding
  naming every file.
- **Where a body exists, its file's header.** For a locally owned row, the
  file's `Component:` header names the owner. For an `external:`-owned row,
  it names a component the row lists among its `consumers` or `requestors`;
  any other component, or none, is a finding.
- **Kept:** a file whose `Contracts:` marker declares an id it states no body
  for ("declared, not stated"), and a header the grammar refuses (its rows
  unstated, the scan continuing).
- **Retired:** the owner-exact reverse warn (`_owner_exact_findings`) and the
  stray-declaration rule, both keyed on the owner's path; the "no far-side
  module states it" finding, since zero bodies is valid. A `Contracts:` id
  naming no row stays the connectivity warn's.

The scan keys each site by its repository path and reads its component from
the census's declarations, so a file with no valid header is "no component".
Private names follow the semantics: `_owner_files` becomes `_header_files`,
`_file_owner_declarations` becomes `_header_declarations`,
`_stray_declaration_findings` becomes `_uniqueness_findings`; the re-exports
in `trajectory_arch` and `check_trajectory` follow.

**Two bodies today.** `scripts/dev-setup.template.ps1` states IF-292 and
IF-293 beside `scripts/dev-setup.template.sh`, unseen until now because only
the owner file was scanned. The `.sh` keeps the bodies, which gain the
PowerShell spellings; the `.ps1` header points at them in prose.

**Directory owners' bodies.** The README files stay the bodies' homes and
each gains the `Component:` line of its producing component (table 1.1):
`docs/README.md` CMP-009, `docs/log.d/README.md` CMP-008,
`docs/requirements/README.md` CMP-006, `docs/test/README.md` CMP-006,
`docs/work/README.md` CMP-006, `project-trajectory/registries/README.md`
CMP-009, `project-trajectory/skills/README.md` CMP-009,
`project-trajectory/scripts/README.md` CMP-006; each is listed in `[arch-map]
headers`. `docs/reviews/` is outside the surface, so IF-047's body moves into
`kitlib/verdict.py` (CMP-008, the verdict record's parser) and IF-160's into
`score_reviews.py` (CMP-008, the scoreboard's single writer); the README
keeps its prose and points at them. No other file's component changes.

### 2.4 Connectivity warns read components (`arch_interfaces`, LLR-042)

`interface_findings`' per-module warns keyed on module paths. They now judge
each component that holds at least one inventory module by header: no row
names it, it owns no row (no Provides), it is on no row's far side (no
Consumes), with the `source` and `sink` valves unchanged. The uncited-seam
line, the marker-grammar findings and the dangling `Contracts:` citations
are unchanged.

### 2.5 The stricter cover (`arch_seams`, LLR-067)

`_declared_seam_pairs` (every pair of any row's endpoints, both ways, any
channel) becomes `_call_cover`: the `(requestor, owner)` component pairs of
the `call` rows. An import from a file of component X into a file of
component Y, X not Y and Y's file not on the kernel allowlist, is silent
only when `(X, Y)` is in it. The kernel allowlist, the unclassified edge and
the one-component exemption are unchanged. WI-1026 later reads the
requestor from the importing file's citation.

**Crossings exposed.** None. Simulated over the live import graph with the
migrated rows (and the retirements below, which are internal and cover no
crossing pair), all 115 non-kernel crossing edges are covered: every pair
they make (CMP-006 to CMP-007 and CMP-008, CMP-007 to CMP-006 and CMP-008,
CMP-008 to CMP-006 and CMP-009, CMP-009 to CMP-006 and CMP-008) has a
`call` row owned by the imported side naming the importer. The one new edge
this row adds, `check_assumption_gate` (CMP-007) into `arch_interfaces`
(CMP-006), is covered the same way (IF-028, IF-089, IF-231). So no row is
filed for Done-when 4.

### 2.6 Placement in the views (`gen_components`, LLR-199)

`seam_placement` reads the endpoint cells: a row is placed at each local
component it names, internal to the lowest component enclosing every
endpoint (through `part_of`; none when an endpoint is `external:` or no
component encloses them all) and boundary to every other. The `component`
cell's union retires with the cell.

### 2.7 The other readers of the migrated cells

- **The interface-form gate's reach** (`assumption_rules`,
  `check_assumption_gate`, LLR-244). `if_reached_srs` went owner path to
  module to the design rows naming it. It now goes through the file stating
  the row's body (the owner's declaration site today): `arch_interfaces`
  gains `contract_homes(root)` (`{IF id: path}`, unique bodies only), the
  step passes it in, and the rule stays pure. The reach over this tree is
  unchanged (each reaching row's body sits in the module that owned it).
- **The dashboard's How-SW views** (`traj_views`, LLR-080). `_sw_node`
  classifies a `CMP-###` endpoint as a component node; the drill wires a
  component endpoint to its component's block at the layer that shows it,
  so the top view keeps its component-to-component and component-to-party
  wires. Inside a component the module-level seam wires go: the rows no
  longer name modules. `gen_arch_map`'s dependency diagram draws no seam
  edge for the same reason (vacuous, not removed).
- **The intake context block** (`intake._seam_lines`, LLR-153 unchanged in
  substance). "Interface seams via the touched modules" matched file stems
  in the endpoint cells; it now lists the rows naming a component the touched
  design rows carry, as the knowledge-pack line already reads them.
- **The observation cadence's component trigger** (`observation_cadence`,
  LLR-293). Its interface leg read the owner paths of rows whose `component`
  cell named the component; the cell retires and owners are not paths, so the
  leg goes. The design rows' module leg stays until WI-1023.
- Read and unchanged: `gen_release_checklist` (an `external:` test only),
  `traj_parse` (the `external:` endpoints of untied rows), `plan_briefs` (the
  cells shown as written), `coherence.component_membership_findings` (its IF
  leg reads a cell no row carries; a row that still does is the retired-cell
  finding).

## 3. The `call` rows (Done-when 5)

Classified on the migrated endpoints: a row whose owner and every endpoint
are one component is internal; any other is crossing. **80 crossing rows
stay** (their symbol-free form is WI-1025's). **54 internal rows**: each is
judged on its original rationale (its `rationale` cell, or, on a row older
than that cell, the `notes` sentence saying why it was declared), never on
its `kitlib` path or a code-naming `data` cell. The test for "earns": the
rationale argues for the seam itself, what breaks without it (the header's
own definition of the cell): several callers sharing one reading, sequence
or primitive so they cannot disagree, a pure layer kept apart from I/O, or
an obligation recorded nowhere else. A row with no rationale, or whose
rationale states an extraction's guarantee, the owner's behaviour (an LLR's
matter) or that the cross-component rule or the retired advisory demanded
it, retires. **25 are kept, 29 retire.**

### 3.1 Crossing (80, stay)

| Row | Owner | Far side | Status |
|---|---|---|---|
| IF-028 | CMP-006 | CMP-007 | Drafted |
| IF-046 | CMP-008 | CMP-008, CMP-009, CMP-006 | Drafted |
| IF-056 | CMP-006 | CMP-009 | Drafted |
| IF-071 | CMP-008 | CMP-009 | Drafted |
| IF-075 | CMP-006 | CMP-009, CMP-008 | Drafted |
| IF-077 | CMP-007 | CMP-006 | Drafted |
| IF-078 | CMP-006 | CMP-008 | Drafted |
| IF-082 | CMP-006 | CMP-009 | Drafted |
| IF-083 | CMP-006 | CMP-009 | Drafted |
| IF-084 | CMP-006 | CMP-009 | Drafted |
| IF-085 | CMP-008 | CMP-009 | Drafted |
| IF-088 | CMP-009 | CMP-008 | Drafted |
| IF-089 | CMP-006 | CMP-008, CMP-007 | Drafted |
| IF-091 | CMP-006 | CMP-008 | Drafted |
| IF-092 | CMP-006 | CMP-008 | Drafted |
| IF-093 | CMP-008 | CMP-009 | Drafted |
| IF-094 | CMP-008 | CMP-009 | Drafted |
| IF-098 | CMP-008 | CMP-009 | Drafted |
| IF-101 | CMP-006 | CMP-008, CMP-007 | Drafted |
| IF-102 | CMP-006 | CMP-006, CMP-008, CMP-009, CMP-007 | Drafted |
| IF-104 | CMP-006 | CMP-007 | Drafted |
| IF-105 | CMP-006 | CMP-007 | Drafted |
| IF-106 | CMP-006 | CMP-009 | Drafted |
| IF-107 | CMP-006 | CMP-009 | Drafted |
| IF-108 | CMP-006 | CMP-008 | Drafted |
| IF-109 | CMP-006 | CMP-008 | Drafted |
| IF-110 | CMP-006 | CMP-008 | Drafted |
| IF-111 | CMP-006 | CMP-009 | Drafted |
| IF-112 | CMP-006 | CMP-007 | Drafted |
| IF-114 | CMP-006 | CMP-008 | Drafted |
| IF-117 | CMP-006 | CMP-007 | Drafted |
| IF-118 | CMP-006 | CMP-009 | Drafted |
| IF-119 | CMP-006 | CMP-008 | Drafted |
| IF-120 | CMP-006 | CMP-008 | Drafted |
| IF-122 | CMP-006 | CMP-007 | Drafted |
| IF-123 | CMP-006 | CMP-008 | Drafted |
| IF-124 | CMP-006 | CMP-008 | Drafted |
| IF-125 | CMP-006 | CMP-009 | Drafted |
| IF-126 | CMP-006 | CMP-009 | Drafted |
| IF-129 | CMP-006 | CMP-006, CMP-008 | Drafted |
| IF-132 | CMP-006 | CMP-009 | Drafted |
| IF-133 | CMP-006 | CMP-008 | Drafted |
| IF-141 | CMP-006 | CMP-009 | Drafted |
| IF-142 | CMP-006 | CMP-009 | Drafted |
| IF-143 | CMP-006 | CMP-009 | Drafted |
| IF-175 | CMP-008 | CMP-008, CMP-009, CMP-006 | Drafted |
| IF-176 | CMP-006 | CMP-008 | Drafted |
| IF-177 | CMP-006 | CMP-008 | Drafted |
| IF-178 | CMP-006 | CMP-008 | Drafted |
| IF-179 | CMP-008 | CMP-009 | Drafted |
| IF-189 | CMP-008 | CMP-007 | Drafted |
| IF-190 | CMP-006 | CMP-006, CMP-009 | Drafted |
| IF-194 | CMP-008 | CMP-008, CMP-007, CMP-006 | Drafted |
| IF-195 | CMP-006 | CMP-006, CMP-008, CMP-007 | Drafted |
| IF-196 | CMP-006 | CMP-008, CMP-007, CMP-006 | Drafted |
| IF-199 | CMP-006 | CMP-007 | Drafted |
| IF-200 | CMP-006 | CMP-006, CMP-008, CMP-009 | Drafted |
| IF-201 | CMP-006 | CMP-006, CMP-008 | Drafted |
| IF-224 | CMP-008 | CMP-006, CMP-008 | Drafted |
| IF-228 | CMP-008 | CMP-008, CMP-009 | Drafted |
| IF-231 | CMP-006 | CMP-007 | Drafted |
| IF-242 | CMP-008 | CMP-008, CMP-006 | Drafted |
| IF-246 | CMP-008 | CMP-008, external:coordinator | Drafted |
| IF-256 | CMP-008 | CMP-006, CMP-008, CMP-009 | Drafted |
| IF-264 | CMP-008 | CMP-009, CMP-008 | Drafted |
| IF-265 | CMP-006 | CMP-008 | Drafted |
| IF-269 | CMP-008 | CMP-008, CMP-006 | Drafted |
| IF-270 | CMP-006 | CMP-009 | Drafted |
| IF-282 | CMP-008 | CMP-008, external:coordinator | Drafted |
| IF-287 | CMP-008 | CMP-008, CMP-006 | Drafted |
| IF-290 | CMP-008 | CMP-008, CMP-006 | Drafted |
| IF-308 | CMP-006 | CMP-007, CMP-008 | Drafted |
| IF-310 | CMP-006 | CMP-008 | Drafted |
| IF-311 | CMP-006 | CMP-008 | Drafted |
| IF-312 | CMP-006 | CMP-007 | Accepted |
| IF-314 | CMP-006 | CMP-007, CMP-008 | Drafted |
| IF-315 | CMP-006 | CMP-008, CMP-009 | Drafted |
| IF-316 | CMP-006 | CMP-006, CMP-009 | Drafted |
| IF-325 | CMP-006 | CMP-009 | Drafted |
| IF-326 | CMP-008 | CMP-006 | Drafted |

The far side is the migrated `requestors` (or, for IF-264 and IF-265,
`consumers`), de-duplicated, in first-occurrence order.

### 3.2 Internal (54): kept with the rationale that earns them, or retired

| Row | Component | Disposition |
|---|---|---|
| IF-044 | CMP-008 | retires: no rationale |
| IF-052 | CMP-009 | retires: the rationale names the binding and the facade, not a reason for the seam |
| IF-053 | CMP-008 | retires: no rationale |
| IF-055 | CMP-008 | retires: no rationale |
| IF-058 | CMP-008 | retires: no rationale (notes: a `source` marker only) |
| IF-061 | CMP-008 | retires: no rationale (notes: a `source` marker only) |
| IF-064 | CMP-008 | retires: the rationale is the extraction's re-export guarantee, discharged |
| IF-065 | CMP-008 | retires: no rationale |
| IF-066 | CMP-008 | retires: no rationale |
| IF-076 | CMP-006 | retires: the rationale is the extraction's behaviour-preserving split, discharged |
| IF-087 | CMP-007 | retires: no rationale |
| IF-090 | CMP-008 | retires: no rationale |
| IF-097 | CMP-008 | retires: no rationale (notes: a `source` marker only) |
| IF-099 | CMP-008 | retires: the rationale states the loader's behaviour; notes: the architecture rule no longer demands it |
| IF-100 | CMP-008 | retires: no rationale; notes: the architecture rule no longer demands it |
| IF-113 | CMP-008 | retires: the rationale states the loader's strict fill, a behaviour; notes: the architecture rule no longer demands it |
| IF-115 | CMP-008 | kept: notes: "declared because the fail-closed obligation lives on the CALLER and would otherwise be recorded nowhere" (no LLR states the caller's hold, so it is still true) |
| IF-128 | CMP-006 | retires: no rationale; notes: declared because the module consumes it (helper usage) |
| IF-131 | CMP-006 | kept: "One walk, one grammar: the module keys and import names are exactly what the map rendered, so every downstream join (import resolution, CMP membership) is unchanged." |
| IF-136 | CMP-008 | retires: no rationale |
| IF-137 | CMP-008 | retires: no rationale |
| IF-173 | CMP-008 | retires: no rationale |
| IF-180 | CMP-006 | kept: "drawing the seam here keeps the checker growing by composition lines alone while the rules stay testable on in-memory rows" |
| IF-186 | CMP-008 | kept: "One helper owning the whole write sequence ... keeps both callers from sweeping in, overwriting or discarding an edit of the operator's ... instead of two copies of a whole-tree sequence each guarded separately." |
| IF-188 | CMP-007 | kept: "a function the report calls worse is one the complexity step calls worse; a second copy of any of them would be a second answer waiting to disagree." |
| IF-208 | CMP-006 | kept: "Keeping both in the pure rule module, beside the rows they read, lets the checker compose each into its own class by one line, and keeps the rules testable on in-memory rows." |
| IF-216 | CMP-006 | kept: "the checker reads every file and every commit these rules need and hands them in, so the rules stay testable on in-memory rows and the checker grows by composition lines alone." |
| IF-217 | CMP-006 | kept: "the module that writes the record is the one that reads it back, so the reading follows the record's own format and the pure rule compares texts it never has to find." |
| IF-226 | CMP-006 | kept: "Gathering that chain in the pure join layer that judges the tier keeps the acceptor reading the same rows, joined the same way, as the checker judges" |
| IF-227 | CMP-009 | kept: "Deriving the view from the registries in the dashboard's source layer, through the same classification rule the checker applies, keeps it from going stale ... and keeps the page and the checker agreeing." |
| IF-239 | CMP-007 | kept: "a module the report calls worse is one the count's own report calls worse; a second copy of any of them would be a second answer waiting to disagree." |
| IF-245 | CMP-008 | kept: "Scattered through the launching roles those differences drift apart, so one module answers them per runner and the session layer imports it." |
| IF-248 | CMP-008 | kept: "a copy of any rule in the service would let the launch side and the bookkeeping side disagree about when a session resets; one module owns them and the service imports it." |
| IF-252 | CMP-006 | kept: "drawing the seam here keeps the checker growing by composition lines alone while the rule stays testable on in-memory rows" |
| IF-260 | CMP-008 | retires: no rationale |
| IF-261 | CMP-008 | retires: no rationale |
| IF-262 | CMP-009 | retires: no rationale |
| IF-263 | CMP-006 | retires: no rationale |
| IF-266 | CMP-008 | kept: "Keep provider event shapes in the adapter while retained bookkeeping owns comparisons across calls and resets." |
| IF-271 | CMP-008 | kept: "The integrator must ask one guard-owned admission question, so every non-dispatcher route receives the same lease and drain decision." |
| IF-272 | CMP-008 | kept: "Coordinator and retained-session state must resolve the same primary checkout, or a lane worktree can split their runtime state." |
| IF-273 | CMP-008 | kept: "One exclusive-file lock primitive keeps coordinator lease updates and other runtime-store updates from growing incompatible lock behavior." |
| IF-286 | CMP-008 | kept: "Dispatch, close, merge and brief composition need one reading of whether a changed Done-when has the exact blessing it owes; separate readers could release a different text" |
| IF-291 | CMP-008 | kept: "Every pause consumer needs one boundary interpretation, because separate parsing would disagree over wrapping weekdays, end instants or the interval" |
| IF-294 | CMP-008 | kept: "The close, sweep and commit check need one pure interpretation of an adoption request and record, so they cannot disagree" |
| IF-296 | CMP-008 | kept: "The coordinator needs one fail-closed derivation of the later act so it cannot construct a partial brief, reinterpret a committed verdict, or act on held text" |
| IF-297 | CMP-008 | kept: "Every agent route needs the same answer before it can begin governed work; one owner prevents route-specific meanings of an active commit floor." |
| IF-302 | CMP-008 | retires: the rationale says why not IF-297, not why the seam (a one-caller helper) |
| IF-303 | CMP-008 | kept: "The close and commit rule need one owner for validation at a named revision, so both bind an adoption record to the same parent-tree result." |
| IF-309 | CMP-008 | kept: "The three consumers need one derivation so a recorded, drawn, or rendered review cannot disagree about its test set or refusal." |
| IF-317 | CMP-006 | retires: no rationale |
| IF-318 | CMP-006 | retires: no rationale |
| IF-319 | CMP-006 | retires: no rationale |
| IF-320 | CMP-006 | retires: no rationale |

### 3.3 How a row retires

Every retiring row is `Drafted`, so no act is owed for the deletion.
`retire.py` writes records for the four spine tiers only (SN, SR, LLR, TC);
an interface row retires by deleting its table, its id staying spent under
the watermark, and its reason is the table above and the Deliverable. With
it, in the same build commit:

- its owner module's `Contracts:` marker drops the id and the
  `Contract IF-NNN:` opener goes, the body's sentences kept as the module's
  own documentation;
- each test case citing it drops the id from `verifies`: Accepted TC-048,
  TC-049, TC-067, TC-080, TC-148, TC-150, TC-166, TC-167, TC-199, TC-266,
  TC-268, TC-374, TC-389, TC-409, TC-410, TC-418, TC-425, TC-428, TC-429
  (each drifts), and Drafted TC-459;
- its `docs/if-tc-coverage-allow` entry is pruned (the seed count and the
  pinned seed set in `tests/test_trajectory_arch.py` move with it).

Historical mentions (open items, archived specs, the log) stay.

## 4. Spine rows

New, `Drafted`, phase 6, ids from the lane's ranges:

- **LLR-398** (SR-159, CMP-006): one body per interface, over the declared
  surface (2.2, 2.3).
- **TC-462** (LLR-041): each endpoint form and its finding, the party list,
  the all-`external:` refusal and the retired `component` cell.
- **TC-463** (LLR-398): zero, one and two bodies; the local and external
  header rules; declared, not stated; the surface's edges.
- **TC-464** (LLR-067): the stricter cover.
- **TC-465** (LLR-199): derived placement.
- **TC-466** (LLR-244): reach through the body's file.
- **TC-467** (LLR-042): connectivity warns over components.

Re-cut LLRs (amended, text only; each `Accepted` one drifts for
adjudication), completing S5's list from the code:

- **LLR-041**: the owner's form and the far side's, the party list, the
  retired cell and advisories (2.1).
- **LLR-042**: connectivity over components; the owner-exact reverse warn
  retires, the body rule being LLR-398's (2.4).
- **LLR-067**: the cover is the `call` rows' component pairs (2.5).
- **LLR-199**: placement derived from the endpoints (2.6).
- **LLR-244**: reach through the file stating the body (2.7).
- **LLR-080**: the dashboard wires seams between the components and parties
  the rows name; the architecture map's diagram draws none (2.7).
- **LLR-293**: the component trigger's interface leg goes (2.7).
- **LLR-397** (`Drafted`, no act): the scope's second half is `[arch-map]
  headers`, not the registry's file owners (2.2).

Read and left: LLR-153 ("IF seams" among the context block's joins stays
true), LLR-187 (the IF entries in the required-field tables), LLR-373 and
LLR-374 (membership and import resolution, unchanged).

Test cases amended where their text becomes untrue: TC-044 (the endpoint
advisory becomes the endpoint finding), TC-067 (the cover), TC-080 (the
connectivity cases), TC-195 (the seam placement), TC-458 (`Drafted`: the
scope's second half); each `Accepted` one drifts.

CMP-006's `notes`: its "Their cross-component edges are covered as interface
rows" sentences hold under the stricter cover (each cited row is a crossing
`call` row owned by the imported component naming the importer) and are
kept; nothing it says is made untrue by a retirement, so it is read and left
unamended unless the build finds otherwise.

Then `trace.py --root . --bump-ids` (LLR 397 to 398, TC 461 to 467).

## 5. Documents

- The registry header (Done-when 2): the owner is "a component id or an
  `external:` party, never a requirement id" (revision 35); the far side's
  forms; the party list; `component` gone; the definition gate's paragraph as
  2.3; IF rows name no file in an endpoint cell. The shipped template's
  header and example row follow.
- `PROCESS.md` §8 and `PROCESS_OPTIONS.md` "Component layer": the owner's
  form and the cover, each stated once (byte deltas reported).
- `docs/registry-machinery-reference.md`: the interface row of the table.
- `RESYNC_PACK.md`: variant F's entry after WI-1021's, anchored at
  `1b15d07fb`, with the mapping rule (section 1) for adopters.

## 6. Tests

Red before the code, in one new module (`tests/test_if_owner_component.py`):
each endpoint finding, the party list, zero, one and two bodies, the external
body rule, the stricter cover and placement. Then every test module
importing a changed module, fixtures moved from path owners to component
owners, the whole-tree tests and `run_menu.py smoke`.

## 7. Acts owed (for the Deliverable)

Amendments of `Accepted` rows, drifting: LLR-041, LLR-042, LLR-067,
LLR-080, LLR-199, LLR-244, LLR-293; IF-312; TC-044, TC-067, TC-080, TC-195
and the 19 TCs losing a retired id. First acceptance: LLR-398, TC-462 to
TC-467. None taken here.
