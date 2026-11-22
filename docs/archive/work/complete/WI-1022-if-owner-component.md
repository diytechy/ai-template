+++
id = "WI-1022"
title = "Interface rows name components, not files: each owner is a component id or external party; internal call rows retire"
workstream = "process"
sr_refs = ["SR-159", "SR-157"]
specref = ""
needs = ["WI-1021"]
buildtier = "strong"
safety_class = "ordinary"
priority = 2
planmode = "single"
supersedes = "WI-1015"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1022`, cut from `refactor_again` at
`1b15d07fb`, with the commit hooks on. The specref (the pointer rules) is
cleared at close, as a terminal row's is. The plan,
[plan.md](../../../plans/WI-1022/plan.md), carries the mapping rule, the
producing components, the scan surface and the classification of every
`call` row with the quoted rationale of each kept internal one.

- `0b9921e98`: the plan.
- `d8ac920b8`: the migration, the checks, the retirements, the spine rows,
  the documents, the RESYNC entry, the tests and the regenerated views.
- The close-out commit after it: this Deliverable, the move to `complete/`
  and the log fragment.

**The migration** (Done-when 1 and 2). Every row's `owner`, `requestors` and
`consumers` is a live `CMP-###` id or a declared `external:` party, by the
plan's rule (section 1): a file declaring a component becomes it; a
directory or file-channel owner becomes its producing component (below);
`hooks/commit-msg` (no header, outside the census scope) becomes CMP-007
beside its sibling hooks; this repository's own coordinator tooling under the
root `scripts/` (`coordinator/codex_call`, `coordinator-relaunch.cmd` and
`.sh`) becomes CMP-008, the component whose machinery it drives (a deviation:
the plan said `external:coordinator`, below); `tests/test_dogfood_sync.py`
leaves IF-072's far side, a test being no component; repeats in a cell are
dropped. Every `component` cell is deleted and the key leaves the schema
(`kitlib.spine.REGISTRY_KEYS`) and the shipped template. The registry header
states the owner as "a component id or an `external:` party, never a
requirement id", citing revision 35, says an interface row names no file in
an endpoint cell, and declares the seven parties on `# External party:`
lines. IF-312 (`Accepted`) is migrated text only: owner CMP-006, requestor
CMP-007. "IF rows name no file in any cell" is read as the endpoint cells
(plan 1.4): the `data` cell is WI-1025's ("WI-1022 took file names out of the
endpoint cells", its Done-when 6), and file names in `rationale` and `notes`
are WI-1028's.

**The producing components** (Done-when 1; plan 1.1):

| Owner before | Rows | Owner now |
|---|---|---|
| `docs/requirements/`, `docs/requirements` | IF-021, IF-033, IF-034, IF-051, IF-059; IF-103's consumer | CMP-006 |
| `docs/test/` | IF-161 | CMP-006 |
| `docs/work/` | IF-023, IF-024, IF-054, IF-079, IF-159 | CMP-006 |
| `docs/reviews/` | IF-047, IF-160 | CMP-008 |
| `docs/log.d/` | IF-156, IF-168 | CMP-008 |
| `docs/` | IF-030 | CMP-009 |
| `project-trajectory/scripts` | IF-025, IF-026 | CMP-006 |
| `project-trajectory/skills/` | IF-035 | CMP-009 |
| `registries` | IF-039 | CMP-009 |
| the 13 file owners | IF-022, IF-029, IF-031, IF-037, IF-038, IF-045, IF-049, IF-057, IF-068, IF-070, IF-072, IF-073, IF-134, IF-135, IF-162, IF-163 | each file's own header |

**The scan surface** (Done-when 3). `docs/stack.ini` gains `[arch-map]
headers`, the files outside `[paths] src` whose headers the contract scan and
the component census read (one reader, `kitlib.config.declared_headers`; the
template documents the key, commented out). The surface is every file under
`[paths] src` of a type the `Component:` grammar carries, `README.md`
excluded, plus the listed files; nothing else is read, so a body quoted in
`docs/reviews/`, `docs/plans/`, the approval snapshot or an example document
is never counted. This repository lists the 13 file owners and the eight
directory READMEs that state contracts; each README gains the `Component:`
line of its producing component, and the census reads 175 declared files and
0 findings. `docs/reviews/` stays outside, so IF-047's and IF-160's bodies
moved into `score_reviews.py` (CMP-008), the scorer that parses the one and
writes the other. The scan found one interface stated twice:
`dev-setup.template.ps1` repeated IF-292's and IF-293's bodies beside
`dev-setup.template.sh`; the `.sh` keeps them, naming the PowerShell
spellings, and the `.ps1` points at them.
<!-- fig: cmd="arch_inputs.component_headers(root) over the worktree" rev="d8ac920b8" -->

**One body per interface** (Done-when 3; LLR-398, new). At most one file
states each body: zero is valid, two or more is one finding naming every
file. Where a body exists its file's header names the owner, or, for an
`external:`-owned row, a component on the row's far side. A declaration with
no body and a refused header stay findings. The owner-exact reverse warn and
the stray rule retired with the owner's path. `contract_homes(root)` gives
each interface's one body file.

**The stricter cover** (Done-when 4; LLR-067). Only a `call` row owned by
the imported file's component naming the importer's among its requestors
covers an import (`arch_seams._call_cover`); the kernel allowlist and the
one-component exemption are unchanged. **No crossing was left uncovered**:
all 115 non-kernel crossing edges are covered at the component level, and
the one edge this row adds (`check_assumption_gate` into `arch_interfaces`,
CMP-007 to CMP-006) is covered by IF-028, IF-089 and IF-231. No row is
filed.
<!-- fig: cmd="arch_seams._classifiable_edges(root) joined with the migrated call rows (the plan's simulation)" rev="1b15d07fb" -->

**The other readers.** `trace.py` holds every endpoint to the two forms
(LLR-041); the module-owner advisory and the endpoint-class advisory
retired. Connectivity warns judge components (LLR-042). The component view
derives placement: internal to the lowest component enclosing every
endpoint, boundary to every other (LLR-199). The interface-form gate
reaches a requirement through the file stating a boundary row's body
(LLR-244), and, where no source is scanned (`files` mode), through the
design rows placed in the row's owner component, so a non-Python adopter is
not left with every interface-form requirement unreached; the live reach is
unchanged and the step reports 0 findings. The dashboard's How-SW views draw
component nodes and wire them at the layer that shows them (LLR-080). The
intake context block lists the seams of the touched components. The
observation cadence's component trigger drops its interface leg (LLR-293).
A header's `Component:` line is no longer taken for its summary in the
interface reference.

**The `call` rows** (Done-when 5; plan section 3). 134 classified: 80
crossing, 54 internal; of the internal, 25 are kept with the quoted
rationale that earns them and 29 retire. IF-246 and IF-282 became internal
with the coordinator tooling's mapping to CMP-008 and are kept on their
rationales ("Every role that makes a model call needs the same launch,
accounting and record, and a role that keeps its own copy of any of them
drifts"; "The loop and coordinator need one request shape for the retention
plan"). **Retired** (all `Drafted`, so no act; `retire.py` keeps records
for SN, SR, LLR and TC only, so each table is deleted, its id spent under
the watermark):

| Row | Reason |
|---|---|
| IF-044, IF-053, IF-055, IF-065, IF-066, IF-087, IF-090, IF-136, IF-137, IF-173, IF-260, IF-261, IF-262, IF-263, IF-317, IF-318, IF-319, IF-320 | internal; no rationale |
| IF-058, IF-061, IF-097 | internal; no rationale (notes: a `source` marker only) |
| IF-052 | internal; its rationale names the binding and the facade, not a reason for the seam |
| IF-064 | internal; its rationale is the extraction's re-export guarantee, discharged |
| IF-076 | internal; its rationale is the extraction's behaviour-preserving split, discharged |
| IF-099, IF-113 | internal; the rationale states the loader's behaviour, and the notes say the architecture rule no longer demands it |
| IF-100 | internal; no rationale, and the notes say the architecture rule no longer demands it |
| IF-128 | internal; no rationale, the notes recording helper usage |
| IF-302 | internal; its rationale says why not IF-297, not why the seam (a one-caller helper) |
| IF-143 | **crossing, retired at the build** (a deviation): its one requestor, `gen_components`, no longer calls `trace_text.norm_module`, since placement reads component ids |

With them: each owner module's `Contracts:` marker drops the id and the body
stays as plain documentation; each citing TC drops the id from `verifies`;
17 seed entries and the addition IF-173 leave `docs/if-tc-coverage-allow`
(seed count 116 -> 99, its pinned set in `tests/test_trajectory_arch.py`
with it). The registry holds 240 rows.
<!-- fig: cmd="tomllib over docs/requirements/interfaces.toml" rev="d8ac920b8" -->

**Spine rows.** New, `Drafted`, phase 6: LLR-398 (SR-159, CMP-006); TC-462
to TC-467. `trace.py --root . --bump-ids` moved the watermark LLR 397 -> 398,
TC 461 -> 467; IF stays 326. No status moved, and `intake.py snapshot` was
not run.

**Acts owed** (amended `Accepted` rows, text only, drifting for
adjudication; and the new rows' first acceptance):

- LLR-041, LLR-042, LLR-067, LLR-080, LLR-199, LLR-244, LLR-293 (detail; the
  `module` and `code_symbol` cells of LLR-041, LLR-042, LLR-067 and LLR-244
  gain the new symbols, a traced-cell change). Their Hat-Refs are left as
  they are, deliberately: no perspective changes with the endpoint form.
- IF-312 (the migrated endpoints, the `component` cell gone);
- CMP-006 `notes` (its cover sentences: IF-214 is a `file` row and covers no
  import under the stricter cover, so the sentence now names the `call`
  rows that do);
- TC-044, TC-067, TC-080, TC-195, TC-435 (method, expected or evidence made
  untrue);
- the TCs losing a retired id from `verifies`: TC-048, TC-049, TC-067,
  TC-080, TC-148, TC-150, TC-166, TC-167, TC-195, TC-199, TC-266, TC-268,
  TC-374, TC-389, TC-409, TC-410, TC-418, TC-425, TC-428, TC-429;
- first acceptance of LLR-398 and TC-462 to TC-467. LLR-397, TC-458, TC-459
  and TC-460 are `Drafted` and owe none.

Read and left: LLR-153, LLR-187, LLR-373, LLR-374.

**Tests.**

- Red before the code: `tests/test_if_owner_component.py` as first written,
  `15 failed in 2.78s` (each endpoint finding, the party list, zero, one and
  two bodies, the external-body rule, the stricter cover, placement, reach,
  connectivity); green with the code, `15 passed in 2.17s`; then the `files`
  mode reach case added and the module folded to one test per TC to stay
  inside the smoke tier's membership budget, `7 passed in 0.79s`.
  <!-- fig: cmd="python -m pytest tests/test_if_owner_component.py -q" rev="the worktree before the code, then after it, ahead of d8ac920b8" -->
- The modules whose fixtures moved from path owners to component owners,
  each green after its edit: `test_trajectory_arch` `169 passed in 50.24s`;
  `test_component_headers`, `test_gen_components`, `test_seam_resolution`,
  `test_interface_owner_reach`, `test_gen_arch_map`, `test_assumption_gate`,
  `test_if_owner_component` and `test_dogfood_sync` `227 passed, 1 skipped
  in 251.59s`; the ratchets, `test_traj_views`, `test_traj_graph`,
  `test_traj_render` and `test_import_layers` `139 passed in 103.18s`;
  `test_trace_interfaces` `46 passed in 167.60s`.
  <!-- fig: cmd="python -m pytest -q -n auto <each module listed>" rev="the worktree ahead of d8ac920b8" -->
- The full unfiltered suite: `77 failed, 8206 passed, 31 skipped, 18
  warnings in 7631.51s (2:07:11)`. 36 failures were `test_trace_interfaces`
  read mid-run while its fixtures were being reworked (46 passed after); 33
  (`test_dispatch` and `test_loop_provenance`) passed on rerun, a box at
  99% CPU; `test_derive_stage` cleared at the regen; `test_stage_ladder` is
  trunk's red (below); the other six (`test_frame_context`,
  `test_components_registry`, `test_intake`, `test_rejudge`,
  `test_trace_golden`, `test_smoke_budget`) were fixtures of the old shape,
  rewritten (the trace golden regenerated deliberately: the report line and
  the retired endpoint advisory). Those modules with every module touched
  since: `1 failed, 815 passed, 1 skipped in 775.12s (0:12:55)`, the one
  trunk's.
  <!-- fig: cmd="python -m pytest -q -n auto" rev="the worktree ahead of d8ac920b8" -->
- After the cognitive-complexity refactors the commit hook asked for:
  `test_trajectory_arch`, `test_if_owner_component`, `test_assumption_gate`,
  `test_gen_arch_map`, `test_trace_interfaces`, `test_check_complexity`,
  `test_component_headers`, `test_import_layers`, `test_dogfood_sync` `466
  passed, 1 skipped in 103.88s`.
  <!-- fig: cmd="python -m pytest -q -n auto <each module listed>" rev="the worktree ahead of d8ac920b8" -->
- `run_menu.py smoke` over `d8ac920b8`: `trace.py --strict` `orphans=0 integrity=0`, `components=4 component-findings=0 interfaces=240 interface-findings=0`; `check_trajectory.py --strict` clean (`1042 work item(s), 909 done (87%), 35 cancelled, graph acyclic`); `check_resync: OK, 44 shipped path(s) changed; entry anchored at 1b15d07fb`; the tier `1 failed, 3716 passed, 3 skipped, 18 warnings in 106.58s (0:01:46)`, the one failure trunk's (below), under `max-tests = 3720`; the tier's CPU 591.5 s against 540 `cpu-seconds` is the report-only WARN on a loaded box.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="d8ac920b8" -->
- **Trunk's red, not this row's:** `tests/test_stage_ladder.py::
  test_this_repo_is_clean_at_the_ERROR_severity`, `check_vocab --strict`
  flagging the retired tag "G2" at lines 46 and 100 of
  `docs/work/queued/WI-1024-constrains-coverage.md`, from `1b15d07fb`
  (the coordinator's note; it is fixed on trunk and reaches this branch at
  the merge).

**Byte deltas.** `PROCESS.md` 101,950 -> 101,959 (+9, watched);
`PROCESS_OPTIONS.md` 202,304 -> 202,446 (+142, watched); the byte-budget
skill 4,631 -> 4,623 (cap 5,000; its two watched rows re-stamped, three
copies); `RESYNC_PACK.md` 737,613 -> 741,646 (unbudgeted); `EXAMPLE.md`
33,086 -> 33,241 (unbudgeted).

**Deviations from the plan.**

- IF-143 retired (above): 80 crossing rows in the plan, 79 kept.
- The coordinator tooling under the root `scripts/` maps to CMP-008, not
  `external:coordinator`: the frame view holds every `external:` row without
  a crossing to a "No tie-back" note, and two of the four rows open their
  notes with the `source` valve. IF-246 and IF-282 are internal and kept.
- CMP-006's `notes` amended (the plan expected to leave them): IF-214 does
  not cover under the stricter rule.
- TC-435 (`Accepted`), TC-459 and TC-460 (`Drafted`) amended beside the
  plan's list: TC-435 and TC-460 asserted seam placement through membership.
- The interface-form gate gains its `files`-mode reach (LLR-244's text
  says so; TC-466 covers it), which the plan had not foreseen.
- `declared_headers` lives in `kitlib.config`, beside the `stack.ini`
  reader, rather than in `gen_arch_map`, keeping that module under its size
  baseline.
- The ratchets re-stamped down: `trace.py` 3844 -> 3789, `intake.py` 1947 ->
  1939, `gen_arch_map.py` 1657 -> 1654, `check_trajectory.py` 1657 -> 1656
  SLOC; the C901 entries of `interface_findings` and
  `contract_body_findings` deleted (both under the limit); the cognitive
  baseline's six rows this row moved (three deleted, three re-stamped down),
  after `_component_connectivity`, `if_reached_srs`, `scan_contracts` and a
  test translator were decomposed outward. `rendering/traj_views.py` sits at
  999 SLOC, under the 1000 line.

## Context

Variant F's second row (F-2), filed on trunk on 2026-11-21 (queue-drill
HANDOFF §3.3). Ruled in the review-churn plan: F-call 1 (i) and decision 1
(revisions 17 and 18), the OI-67 (a) header amendment (revision 35:
"a component id or an `external:` party, never a requirement id"), ruling 5
(IF rows name no files), and the classification of `call` rows
(revision 20).

Today the 269 interface rows name files: 229 owners are `scripts/<module>`
paths, about 36 are other paths (`docs/requirements/`, `docs/work/`,
`docs/stack.ini`, `docs/process.toml`, templates, directories), and 4 are
`external:` parties. 176 rows carry the optional `component` cell, a
placement; decision 1 found 35 to 39 of them name where the seam sits, not
who produces it. 157 rows list requestors and 112 consumers, as paths.
Seven `external:` parties are in use (`agent CLI`, `coordinator`,
`downstream adopter`, `git`, `run.* launcher templates`, `run.* launchers`,
`upstream docs`). `trajectory_arch`'s owner-exact check and the
contract-body gate's stray-declaration rule (`arch_interfaces._owner_files`,
`_owner_exact_findings`, `_stray_declaration_findings`; OI-67's slices,
tagged LLR-042) and `trace.py`'s refusal of an id-shaped owner (LLR-041) key
on the owner path. 268 rows are `Drafted`, so the migration needs no act;
the one `Accepted` row drifts for adjudication.

**WI-1015's item 1 lands here** (restructured into F, HANDOFF §3.3 N1). The
cross-component rule (LLR-067) counts any interface row naming both files
as cover, on any channel and whoever owns it. Rebinding cover to components
closes that: an import from a file of component X into a file of
component Y (X ≠ Y, Y's file not on the kernel allowlist) is covered only by
a `call` row owned by Y that names X among its requestors. WI-1026 later
reads the requestor from the importing file's role-typed citation; until
then it is the authored component id.

**`call` rows (revision 20).** The 133 `call` rows are classified. One whose
owner and every endpoint resolve to one component is internal: optional
under F (point 3), it retires unless its original rationale earns it,
judged row by row and never by its `kitlib` path or a code-naming `data`
cell. One crossing a boundary stays; its symbol-free typed form is
WI-1025's.

**The component registry's prose.** CMP-006's `notes` cite cover rows
(IF-093, IF-175, IF-214, IF-314, IF-315); this row amends any sentence the
stricter cover or a retirement makes untrue.

**Left to other F rows:** the `data` cell's whole form and the hand-over
(WI-1025); role-typed citations (WI-1026); the `constrains` link that
makes every interface reached by a requirement (WI-1024).

## Scope answers

- **S1.** Two deliverables, in order on one branch: (1) the registry
  migration and the checks that read the migrated cells, which must change
  in one commit or every owner check fails; (2) the `call` classification
  and retirements, which read the migrated endpoints. (2) could land alone;
  it is kept here by choice, so that it lands before WI-1024 populates
  requirements for every live interface and no retiring row gets one.
- **S2.** No: the cells feed existing strict checks; nothing gains
  authority over a hold, an act or a gate.
- **S3.** Each endpoint cell admits exactly a live `CMP-NNN` id or an
  `external:` token from the declared party list (Done-when 1); anything
  else is a finding. A row whose owner and every endpoint are `external:`
  stays refused, as today.
- **S4.** `single`: registry schema, three check families and a migration.
- **S5.** Changes the boundary rule's cover (WI-1015 item 1) and retires
  internal seams. Re-cut LLRs (text only, drifting): LLR-041 (the owner's
  form), LLR-042 (the owner-exact and contract-gate slices), LLR-067 (the
  cover), LLR-199 (placement in the component view); the lane's plan
  completes the list. Each retired row is named in the Deliverable.
- **S6.** `needs` WI-1021: the owner component is the producing file's
  header, and uniqueness checks the body's file header. No new package,
  tool or service.

## Done-when

- [ ] Every interface row's `owner` is a live `CMP-NNN` id or an
      `external:` token; its `consumers` and `requestors` hold only those
      forms. An `external:` token is `external:` followed by a party on the
      list the registry header declares (the seven in use); a new party is
      added to that list by the row that introduces it, and an unlisted
      party is a finding. The `component` cell leaves the schema; its
      placement meaning is derived (the lowest component enclosing every
      endpoint, for the views only). A file-channel or directory owner
      (`docs/reviews/`, `docs/work/`) names its producing component, chosen
      in the lane's plan and listed in the Deliverable.
- [ ] The interface registry's header states the owner as "a component id
      or an `external:` party, never a requirement id", citing revision 35,
      and IF rows name no file in any cell (ruling 5).
- [ ] The stray-declaration rule becomes uniqueness: at most one in-tree
      file states each `Contract IF-NNN:` body. Zero is valid while the
      row's `data` cell is the contract's home (WI-1025 guards the
      transitions); two or more is a finding. Where a body exists: for a
      locally owned interface, its file's `Component:` header names the
      owner; for an `external:`-owned one, its file's header names a
      component the row lists among its `consumers` or `requestors`, and
      any other component is a finding. The scan surface is shipped
      scripts, configuration files and registry headers; the approval
      snapshot, `docs/reviews/`, `docs/plans/` and example documents are
      outside it.
- [ ] The cross-component rule counts as cover only a `call` row owned by
      the imported file's component that names the importer's component
      as a requestor. The kernel allowlist and the one-component exemption
      are unchanged. Every crossing the stricter cover exposes is covered,
      or listed in the Deliverable with the row filed for it.
- [ ] Each `call` row is classified crossing or internal in the lane's
      plan. Internal rows retire unless the plan quotes the rationale that
      earns them; each retirement names the row and its reason.
- [ ] The S5 LLRs and CMP-006's `notes` are amended where this row makes
      them untrue (text only, drifting); the Deliverable lists the acts
      owed for adjudication.
- [ ] `trace.py --strict` and `check_trajectory --strict` are clean; the
      interface reference and the component views regenerate.
- [ ] A RESYNC entry (variant F, after WI-1021's) tells adopters to rewrite
      owners and endpoints to component ids, with the mapping rule.
- [ ] Tests: red-before for each endpoint finding, the party list, zero,
      one and two bodies, the external-body rule and the stricter cover;
      every importer of a changed module runs green.
