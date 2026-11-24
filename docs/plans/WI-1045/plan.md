# WI-1045 plan, revision 1: the landing rules leave the acceptance record for a CMP-008 module

Written in the worktree `D:/ai-template-wt-wi1045`, branch `maint/wi-1045`,
cut from `refactor_again` at `9e8eb6e57`. `planmode = "single"`: this commit
carries the plan alone, and nothing else changes until the coordinator's
go-ahead.

Read in full: the spec `docs/work/queued/WI-1045-acceptance-record-split.md`;
its scope critique `docs/reviews/2026-11-21-scope-critiques/WI-1045.md`; the
queue-drill hand-off `docs/plans/2026-11-21-queue-drill/HANDOFF.md` sections
3.3 (N3) and 3.5 (R2); WI-1021's component table
(`docs/plans/WI-1021/component-table.md`); WI-1022's and WI-1023's specs;
WI-1069's `## Trust`. Code read: `acceptance_record.py` (whole), the call
sites in every importer (`adjudicate_act`, `adoption_record`,
`amendment_brief`, `baseline_snapshot`, `check`, `check_test_first`,
`check_trajectory`, `held_status`, `intake`, `integrate`, `text_then_act`),
`arch_seams.py` (the cover rule), `kitlib/bootstrap_manifest.py`, and the
docstrings of `kitlib/git.py`, `kitlib/decisions.py` and `kitlib/sitting.py`.
Rows read: LLR-153, LLR-158, LLR-178, LLR-202, LLR-220, LLR-222, LLR-225,
LLR-278, LLR-298, LLR-302, LLR-358, LLR-359, LLR-364, LLR-420, LLR-042,
LLR-067, LLR-398; TC-147, TC-313, TC-397, TC-398, TC-403, TC-461; IF-091,
IF-102, IF-129, IF-175, IF-196, IF-220, IF-256, IF-287, IF-308, IF-326;
CMP-006 to CMP-009.

## Ids

None minted. IF-327 to IF-336, LLR-511 to LLR-515 and TC-606 to TC-612 stay
unminted unless the coordinator takes D5's alternative (IF-327 and TC-606).
No SR, DA, SUR or WI id.

## Measured (the base, `9e8eb6e57`)

Measured read-only with the worktree's Python 3.11.

- **`acceptance_record.py`**: 2,455 lines, **989 SLOC**
  (`check_complexity.module_sloc`), 76 functions and 30 module-level
  assignments.
- **What moves** (section 1): 27 functions and 6 assignments, **296 SLOC**:
  the ruling sync 131, the parent-first judgement 73, the mint's acceptance
  arms 92. So `acceptance_record.py` falls to about 693 SLOC and the new
  module is about 320 (296 plus its imports and three aliases).
- **Importers**: 11 scripts (`adjudicate_act`, `adoption_record`,
  `amendment_brief`, `baseline_snapshot`, `check`, `check_test_first`,
  `check_trajectory`, `held_status`, `intake`, `integrate`, `text_then_act`)
  and 25 test modules holding 1,192 tests; 4 more test modules name the file
  (`test_bootstrap`, `test_import_layers`, `test_module_size_ratchet`,
  `test_complexity_ratchet`).
- **The cover at the base**: `trace.py --root . --strict` exits 0 with
  `component-findings=0 interface-findings=0`; `check_trajectory.py --root .
  --strict` exits 0 (`clean`). Over 612 internal import edges, 121 cross a
  component outside the shared kernel and `arch_seams.cross_component_findings`
  reports none uncovered. `acceptance_record` has 4 crossing edges out (into
  `kitlib/decisions`, `kitlib/done_when`, `kitlib/sitting`, `kitlib/verdict`,
  all CMP-006 to CMP-008) and 8 in (`adjudicate_act`, `adoption_record`,
  `amendment_brief`, `intake`, `integrate`, `text_then_act` from CMP-008;
  `check`, `check_test_first` from CMP-007).
- **Placement** (`components.derived.toml`): LLR-153, LLR-158, LLR-278,
  LLR-359 and LLR-364 are placed in CMP-006 and CMP-008; LLR-358 in CMP-006
  only (through TC-397's IF-308); LLR-298 is unplaced (TC-313 names no
  interface).
- **Ratchets**: deferred function-body imports 46, the top of the stamped
  window 14..46 (`tests/test_import_layers.py`); no cycle. Smoke tier 3,959
  tests against `max-tests` 4,060. Neither complexity sensor has a row for
  `acceptance_record.py` (`tests/test_complexity_ratchet.py`, ruff C901 at
  10: the file passes; `docs/complexity-baseline`, cognitive at 15: the moved
  functions' highest is `settled_amendments` at 13). The module-size ratchet
  has **no `BASELINE` entry** for `acceptance_record.py`: it is under the
  1,000-SLOC `THRESHOLD`. Entries that a changed importer sits at: `intake.py`
  1,946, `integrate.py` 1,788, `check.py` 1,339.

## 1. What moves and what stays (Done-when 1)

### 1.1 The new module

One new module, **`project-trajectory/scripts/landing_rules.py`**, header
**`Component: CMP-008`**, **`Contracts: IF-308`**. Its boundary sentence:
*the rules the coordinator's landing runs on top of the acceptance record —
the pre-commit hook's and the merge slot's per-commit refusals (the ruling
sync, the parent-first judgement) and the trunk mint's acceptance arms (the
settled-amendment filter, the held-act arms) — each reading two git trees
and the record through `acceptance_record`'s readers, never the working
tree.* It joins the `assumption_rules`, `frame_rules`, `spine_rules` naming.
One module rather than one per rule family: every family reads the record
through the same readers, so one module keeps one seam (D1).

Every moved definition moves **verbatim**: its body, docstring and
`Implements:` tag byte-identical, checked in Phase 2 by comparing each moved
definition's source segment against the base. Only the import block and the
three aliases below are new text in it. `acceptance_record` keeps **no second
name** for any of them (no re-export).

The module's imports, the `text_then_act` idiom (a sibling fallback under
`try`/`except ImportError`): `spine_carrier`; from `acceptance_record` the
ten names section 1.3 lists; `kitlib.decisions`, `kitlib.git`,
`kitlib.registry`, `kitlib.sitting`, `kitlib.spine`. Its aliases:
`_git = _kitgit.git_out`, `_spine_carriers = spine_carrier.carriers`,
`_tier_carriers = spine_carrier.tier_carriers` (the same objects
`acceptance_record` aliases, so no second body).

### 1.2 What moves (33 definitions)

| Definition | Design row | Side |
|---|---|---|
| `OPEN_ITEMS_REGISTRY`, `WORK_DIR`, `ARCHIVE_WORK_DIR`, `_PENDING`, `_git_paths`, `_show` | LLR-298 | CMP-008: the ruling sync's constants and its two git reads |
| `_tree_specs`, `_registry_states`, `_ruled_items`, `_citing_rows`, `_sync_gap`, `_raw_done_when`, `ruling_sync_lines`, `_judged_lines`, `_sync_lines`, `staged_ruling_sync_lines`, `commit_ruling_sync_lines` | LLR-298 | CMP-008: the ruling-to-citer sync, its staged form (the hook's `ruling-sync` step) and commit form (the merge slot's lane-commit walk) |
| `parent_first_tiers`, `_parent_first_names`, `_status_moved`, `_parent_statuses`, `parent_first_lines`, `staged_parent_first_lines`, `commit_parent_first_lines` | LLR-358 | CMP-008: the parent-first commit judgement and its two forms |
| `_latest_reaccept`, `_no_later_writer`, `_row_settled`, `_routed_unmoved`, `_tier_sides`, `_settled_row`, `settled_amendments` | LLR-364 | CMP-008: the trunk mint's settled-amendment filter |
| `unanchored_rows`, `text_as_bound` | LLR-153 | CMP-008: the mint's held-act arms (trigger (f)) |

`ARCHIVE_WORK_DIR` has no reader at the base; it moves verbatim with its
siblings and is surfaced, not deleted (D10).

### 1.3 What stays in `acceptance_record.py` (73 definitions), and why

The two-tree comparison, under `Component: CMP-006`, its header and its
`Contracts: IF-091, IF-129` (IF-308 leaves).

| Definition | Design row | Why it stays |
|---|---|---|
| `SPINE_CSVS`, `ACCEPTANCE_ACT_CSVS`, `AMENDMENT_CSVS`, `OUTSIDE_THE_ACCEPTANCE_ACT` | LLR-158, LLR-220 | the walk's universes |
| `SPINE_TABLE`, `SPINE_COLUMN`, `_spine_stem`, `_spine_carriers`, `_tier_carriers`, `_git` | LLR-158 | the carrier vocabulary and the git degrade the comparison reads |
| `_spine_rows_at`, `rows_at`, `_spine_revs`, `_spine_row_sides` | LLR-158 | the one two-tree walk and its row reader |
| `_tier_reads` | LLR-358 (tag) | the one carrier loop under `_spine_rows_at` (LLR-158); `held_status` and `_snapshot_copy_rows` read it too. Its tag stays: it serves the parent-first tiers as well |
| `SPINE_TRACED_CELLS`, `SPINE_ACCEPTED_CELLS`, `OFFSPINE_TRACED_CELLS` | LLR-222, LLR-225, LLR-420 | the cell split |
| `spine_cell_class`, `traced_cells`, `_ACCEPTED_TEXT`, `split_changed_cells` | LLR-158, LLR-202 | the one comparison basis (IF-129) |
| `accepted_text_digest` | LLR-359 | the judged-text identity; see 1.4 |
| `_claims_acceptance`, `_acceptance_act`, `staged_acceptance_acts`, `acceptance_acts_between`, `staged_drafted_rows`, `staged_spine_amendments`, `_amended_cells`, `staged_spine_findings` | LLR-158 | the acceptance-act and amendment readers over the walk |
| `HAT_REFS_CELL`, `staged_hat_refs_findings` | LLR-202 | the Hat-Refs arm |
| `_SNAPSHOT_ACT`, `_snapshot_acts`, `acceptance_delta`, `first_acceptance_scope`, `_registry_identity`, `lane_acted_set`, `_copy_lines`, `adjudication_acceptance_refusal`, `merge_acceptance_refusal`, `amendment_scope`, `_ledger_acts`, `_reaccepted_ids`, `reaccepted_between`, `_wrote_ledger`, `reaccept_scope_refusal`, `_added_acts`, `added_ledger_entries` | LLR-278 | the merge-time acceptance-act refusal, its re-acceptance scope bound included (D2) |
| `backed_act_refusal`, `lane_acceptance_refusal` | LLR-158 | the same refusal's actor test and wording |
| `_tier_of` | LLR-278 | a row id's tier; `lane_acted_set` reads it, and the moved rules read it through IF-091 |
| `_ledger_read`, `_reaccepted_added`, `_snapshot_copy_rows` | LLR-364 (tags) | readers of the record at a revision, each telling an absent ledger or copy from one that cannot be read or does not parse. `_ledger_read` also serves `_ledger_acts` (LLR-278). They stay with the record they read, so the refusals TC-147 and TC-403 drive stay IF-091's (D4, D9) |
| `SNAPSHOT_DIR`, `SNAPSHOT_README`, `SNAPSHOT_ACTS`, `SNAPSHOT_OWN_FILES`, `_LEDGER`, `_snapshot_survives`, `_mirror_repair`, `staged_snapshot_findings`, `_written`, `_staged_copy_lines`, `committed_snapshot_findings`, `_whole_file_lines`, `_snapshot_write_revs` | LLR-178 | the mirror invariant |
| `_commit_parents` | LLR-298, LLR-302 (tags) | one commit object's parents; `held_status` (CMP-006), `text_then_act` and `adoption_record` read it besides the two moved commit forms |
| `_empty_tree` | LLR-298 | the empty tree's id; `held_status` reads it besides the staged ruling sync |
| `PARENT_FIRST_CSVS` | LLR-358 | the four spine tiers the parent-first rule reads; `held_status` reads it as `MARKED_SPINE`, so it stays a universe beside `ACCEPTANCE_ACT_CSVS` rather than pulling `held_status` across into CMP-008 |
| `verdict_rulings` | none | an alias of `kitlib.verdict.verdict_rulings` no script or test reads; pre-existing, surfaced (D10) |

`landing_rules` imports from `acceptance_record` exactly: `PARENT_FIRST_CSVS`,
`_commit_parents`, `_empty_tree`, `_reaccepted_added`, `_snapshot_copy_rows`,
`_spine_rows_at`, `_tier_of`, `_tier_reads` (IF-091), and
`split_changed_cells`, `accepted_text_digest` (IF-129). The underscore names
stay as they are: `held_status` and `text_then_act` already import several
of them, and renaming them would touch three more modules (D4).

After the move `acceptance_record` no longer imports `kitlib.decisions` or
`kitlib.registry` (only the ruling sync read them); its import roots stay
`record_rows`, `spine_carrier`, `kitlib`, `sys`, `pathlib`, `tomllib`,
`hashlib`, `json`, so `test_the_dependency_surface_is_the_argument_for_the_split`
holds unedited. Its docstring loses the ruling-sync section and the
paragraphs of IF-091's body for the three calls that leave, gains a
one-paragraph pointer to `landing_rules` (which rules left, why, and that the
import runs one way), and keeps its boundary sentence.

### 1.4 The merge-time re-acceptance refusal (LLR-278): stays CMP-006

`merge_acceptance_refusal` and its family stay. Three reasons, in the order
that decides it:

1. **The module states the design argument, and it still holds.**
   `lane_acceptance_refusal`'s docstring places the reading in this module
   on LLR-178's separation: the coordinator that merges is not the reader
   that decides what a spine delta did; `integrate._acceptance_act_refusal`
   supplies the merge base and the rung's place, the reading and the wording
   are the record's. LLR-278's own tag is CMP-006 (WI-1021's table), and the
   spec reads it as the spine's.
2. **It is built on the record's walk**: `staged_acceptance_acts`, the act
   ledger, the copy authorization by registry identity, and
   `lane_acceptance_refusal`/`backed_act_refusal` (LLR-158). Moving it moves
   LLR-158 code with it or widens the seam by the walk's internals.
3. **Its seam already exists**: IF-091 (owner CMP-006, requestor CMP-008)
   names `merge_acceptance_refusal`, and TC-278 and TC-331 verify it there.

Its reads of `kitlib.sitting` and `kitlib.verdict` (CMP-008) stay the
crossings they are today, covered by IF-287 and IF-175 (CMP-006 among their
requestors).

### 1.5 The judged-text identity: one function, in `acceptance_record`

`accepted_text_digest` stays where it is, behind IF-129. Its three readers
(WI-1069's `## Trust`) each call that one function and keep no copy:

| Reader | Component | Path to the function |
|---|---|---|
| the held act (`adjudicate_act._unbound_text`) | CMP-008 | `acceptance_record.accepted_text_digest`, unchanged (IF-129) |
| the held-claim exception (`held_status._excepted`) | CMP-006 | `acceptance_record.accepted_text_digest`, unchanged, internal |
| the record's kept-row reading (`text_as_bound`, moving to `landing_rules`) | CMP-008 | imported by name from `acceptance_record` (IF-129); `landing_rules` defines no digest |

The identity is defined on the comparison basis (IF-129's body: "on the same
basis" as `split_changed_cells`, classing cells by `spine_cell_class`); its
home beside the classifier is what makes "the identity a verdict binds and
the drift that comparison reports read one split" true. Moving it would
separate it from the classifier, add a crossing from `held_status` into
CMP-008 needing a new row, split IF-129's body across two components, and
make TC-398's and TC-461's IF-129 and IF-326 citations need re-pointing.
Kept, the move adds no crossing for it and IF-129, IF-326, TC-398 and TC-461
stay true. The LLR-359 *rule* (an act or claim is taken only while the bound
identity equals the committed row's) already lives in CMP-008
(`adjudicate_act`) and CMP-006 (`held_status`), neither of which moves; the
spec's `amendment_values` is no longer in this file (`amendment_brief.py`,
CMP-008). The Phase 2 boundary test pins the one home: `landing_rules`
defines no `accepted_text_digest` and imports it from `acceptance_record`.

## 2. The callers (Done-when 2)

Every importer of a moved name, by file and component, and its import after
the move. No compatibility re-export is left.

### 2.1 Scripts

| Importer | Component | Moved names it reads | After |
|---|---|---|---|
| `check.py` | CMP-007 | `staged_ruling_sync_lines`, `staged_parent_first_lines` | its two deferred `import acceptance_record` lines (in `_ruling_sync_refusal` and `_parent_first_refusal`) become `import landing_rules`, still deferred (the kitlib-only floor). It no longer imports `acceptance_record` at all |
| `integrate.py` | CMP-008 | `commit_ruling_sync_lines` | `_ruling_sync_refusal`'s deferred import is removed and `import landing_rules` joins the module-level imports: `text_then_act`, already imported at module level, imports `landing_rules` at module level, so deferring buys nothing, and the deferred-edge window stays at 46. `_acceptance_act_refusal` keeps its deferred `import acceptance_record` (`merge_acceptance_refusal` stays) |
| `intake.py` | CMP-008 | `settled_amendments`, `unanchored_rows`, `text_as_bound` | `import landing_rules` at module level beside `import acceptance_record`, which it keeps for `staged_spine_amendments`, `staged_drafted_rows` and `SPINE_CSVS` |
| `text_then_act.py` | CMP-008 | `commit_parent_first_lines` | leaves its `from acceptance_record import (...)` list in both arms of the sibling guard; `from landing_rules import commit_parent_first_lines` joins each arm. It keeps `ACCEPTANCE_ACT_CSVS`, `SNAPSHOT_DIR`, `_commit_parents`, `_spine_rows_at` from `acceptance_record` |
| `adjudicate_act.py` | CMP-008 | `parent_first_tiers` | `import landing_rules`; it keeps `acceptance_record` for `rows_at` and `accepted_text_digest` |
| `adoption_record.py`, `held_status.py`, `amendment_brief.py`, `baseline_snapshot.py`, `check_test_first.py`, `check_trajectory.py` | various | none | unchanged (every name they read stays; `check_trajectory`'s re-export list names none of the moved definitions) |

### 2.2 Tests (import changes only)

| Test module | Moved names it reads | After |
|---|---|---|
| `test_adjudicate_act.py` | `commit_parent_first_lines` | `landing_rules = load_script("landing_rules")`; three call sites qualified by it |
| `test_adoption_record.py` | `_tree_specs` | the in-test `load_script("acceptance_record")` loads `landing_rules` |
| `test_decision_overrule.py` | `staged_ruling_sync_lines`, `commit_ruling_sync_lines`, `_git_paths`, `_kitdecisions` | its `ar` loads `landing_rules` (which binds all four) |
| `test_intake_held_act.py` | `unanchored_rows` | a second load, `landing_rules`; two call sites qualified by it (`_ledger_acts`, `staged_spine_amendments` stay on `acceptance_record`) |
| `test_kitlib_spec_listing.py` | `_tree_specs` | its `acceptance` loads `landing_rules` |
| `test_parent_first.py` | `parent_first_lines`, the `_git` patch, `_kitgit` | a second load, `pf = load_script("landing_rules")`; `parent_first_lines` and `_fake_git`'s targets qualified by `pf`. Its `ar._claims_acceptance` identity pin stays on `acceptance_record` |
| `test_parent_first_git.py` | `staged_parent_first_lines`, `commit_parent_first_lines` | its `ar` loads `landing_rules` |
| `test_ruling_sync.py` | `staged_ruling_sync_lines`, `commit_ruling_sync_lines` | its `ar` loads `landing_rules` |

The other 17 test modules loading `acceptance_record` read only names that
stay, and change nothing.

## 3. The cover (Done-when 2)

F-2's rule (`arch_seams._call_cover`): an import from a file of X into a file
of Y is covered by a `call` row owned by Y naming X among its requestors.

### 3.1 Edges the move introduces, redirects or removes

| Edge | Components | Change | Cover |
|---|---|---|---|
| `check` -> `landing_rules` | CMP-007 -> CMP-008 | new; replaces `check` -> `acceptance_record` | **IF-308 re-owned** to CMP-008, requestors CMP-007 and CMP-008 kept; its `Contract IF-308:` body moves verbatim into `landing_rules`'s docstring (LLR-398: one body, in a file of the owner). IF-189 and IF-194 cover the pair as well |
| `landing_rules` -> `acceptance_record` | CMP-008 -> CMP-006 | new | **IF-091** (owner CMP-006, requestor CMP-008), its body rewritten to state the readers the rules call (3.2); **IF-129** (requestors CMP-006, CMP-008) for `split_changed_cells` and `accepted_text_digest`, unchanged |
| `landing_rules` -> `spine_carrier` | CMP-008 -> CMP-006 | new | **IF-102** (requestor CMP-008), unchanged: its data names `tier_carriers` and `rows_from_text`, two of the four readers the moved code calls; `stem` is named for CMP-008 by IF-110 and IF-133, and `carriers` by no row (the cover is the component pair, which IF-102 alone holds) |
| `intake`, `integrate`, `text_then_act`, `adjudicate_act` -> `landing_rules` | CMP-008 -> CMP-008 | new | internal, no row |
| `landing_rules` -> `kitlib/sitting`, `kitlib/decisions` | CMP-008 -> CMP-008 | new | internal |
| `landing_rules` -> `kitlib/git`, `kitlib/registry`, `kitlib/spine` | kernel | new | the shared kernel, not a seam |
| `check` -> `acceptance_record` | CMP-007 -> CMP-006 | removed | IF-308 leaves CMP-006 with it |
| `acceptance_record` -> `kitlib/decisions` | CMP-006 -> CMP-008 | removed | **IF-256 drops its CMP-006 requestor**: no other CMP-006 file imports `kitlib/decisions` (its importers outside CMP-008 are this one and `pending`, CMP-009) |
| `acceptance_record` -> `kitlib/registry` | kernel | removed | none |

The other crossings into `acceptance_record` (`adjudicate_act`,
`adoption_record`, `amendment_brief`, `intake`, `integrate`, `text_then_act`
from CMP-008; `check_test_first` from CMP-007) stay, for names that stay, under
their existing cover. IF-308 re-owned no longer covers the CMP-008 to
CMP-006 pair; 28 other rows do. Expected after: 122 non-kernel crossing
edges (121, less 2 removed, plus 3 new), none uncovered.

### 3.2 The row changes, with their contract bodies

All three rows are `Drafted`; each change is text on a `Drafted` row, so no
act beyond the first acceptance each already owes.

- **IF-308** (the parent-first commit judgement, offered as a call): `owner`
  `CMP-006` -> `CMP-008`. `requestors`, `rationale`, `data`, `notes` and
  `version` (`v1`) unchanged: the contract is the same, its owner moved. The
  body moves word for word from `acceptance_record`'s docstring to
  `landing_rules`'s.
- **IF-091**: `data` rewritten under the 160-character ceiling (it is 292
  today, an advisory at the base), for example
  `merge_acceptance_refusal -> refusal or None; the record at a revision:
  live rows, a tier's record copy, act-ledger entries a range added, a commit's
  parents`; `version` `v1` -> `v2` (three calls left its surface, readers
  joined; D5). Its body keeps the staged spine-amendment set, the
  acceptance-act questions and `merge_acceptance_refusal`, drops the three
  paragraphs for `settled_amendments`, `text_as_bound` and `unanchored_rows`
  (their statements move into `landing_rules`'s docstring as plain
  documentation, since an internal call needs no seam), and gains one
  paragraph:

  > THE RECORD AS THE LANDING RULES READ IT (WI-1045). `landing_rules`
  > reads the record through these, and through IF-129's two, and nothing
  > else of this module: `_spine_rows_at(root, prefix, registry, id_col)`,
  > a tier's live rows at a tree, `{}` where the tree lists no carrier;
  > `_tier_reads(root, prefix, registry, id_col, under="")`, each carrier of
  > a tier the tree lists, as `(path, rows, failure)`;
  > `_snapshot_copy_rows(root, rev, registry, id_col)` -> `(rows, failure)`,
  > the record's copy of that tier, `(None, None)` when the tree lists none
  > and a failure naming the copy, the revision and whether it cannot be read
  > or does not parse; `_reaccepted_added(root, base, head)` ->
  > `(entries, failure)`, the act-ledger entries `head` adds over `base` in
  > file order, or the failure naming the ledger, the revision and which;
  > `_tier_of(row id)` -> `(registry, id column)` or `(None, None)`;
  > `PARENT_FIRST_CSVS`, the need, requirement, design and test tiers;
  > `_commit_parents(root, rev, question, first=False)` -> `(parents,
  > lines)`, a commit's parents read off its object, an unreadable one a
  > line; `_empty_tree(root)`, the empty tree's id, or None off git. Each
  > reads git and writes nothing.

- **IF-256**: `requestors` `["CMP-006", "CMP-008", "CMP-009"]` ->
  `["CMP-008", "CMP-009"]`. Body (in `kitlib/decisions.py`) unchanged but for
  its pointer to where the ruling sync's git read lives (section 5).

No new row (D5). The ruling sync crosses from `check` on the same import edge
IF-308 covers; at the base it crossed on `check` -> `acceptance_record`,
covered at the component pair, with no row of its own either. Its contract
travels in `landing_rules`'s docstring as plain documentation.

### 3.3 What the cover leaves true

TC-397 (verifies IF-308) is unchanged; LLR-358's placement follows IF-308's
owner to CMP-008 alone (a derived view, regenerated). TC-147 and TC-403
(verify IF-091) are unchanged and stay true: the refusals they drive for an
unreadable or unparseable ledger or copy are `_reaccepted_added`'s and
`_snapshot_copy_rows`' failures, which stay behind IF-091 (D9).
`test_intake_held_act.py`'s three `IF-091:` docstrings stay true for the
same reason. TC-278 and TC-331 (IF-091, `merge_acceptance_refusal`), TC-398
(IF-129) and TC-461 (IF-326) are untouched.

## 4. Behaviour unchanged (Done-when 3)

No design row's text changes; no requirement, test-case or design row is
amended. Every moved definition is byte-identical (1.1). The test modules
this row runs for Done-when 3: the 25 that load `acceptance_record` (8 of
which load `landing_rules` after section 2.2) and the four that name the
file. Each changes only its imports (section 2.2), except these, each
named in the Deliverable with its reason:

1. **`tests/test_acceptance_record.py`** gains one test (the red-first test,
   section 7), modelled on `test_held_status_owns_IF_196`: `landing_rules`
   declares `Component: CMP-008`, `Contracts: IF-308` and its body, and
   `acceptance_record` declares neither; `landing_rules` defines every moved
   name and `acceptance_record` none (no copy, no shim); `acceptance_record`
   does not import `landing_rules` (one way); `landing_rules` defines no
   `accepted_text_digest` and imports it from `acceptance_record` (the one
   identity); `landing_rules`' rules call no `open` or `Path` (two trees, no
   working tree).
2. **`tests/test_adjudicate_act.py`**, `test_the_wait_is_read_from_the_parent_first_rules_one_predicate`:
   its source-text assertion `"acceptance_record.parent_first_tiers(" in
   source` becomes `"landing_rules.parent_first_tiers("`. The assertion pins
   where `adjudicate_act` reads the tiers from, which the move changes.
3. **`tests/test_bootstrap.py`**: `"scripts/landing_rules.py"` joins the
   scaffold's expected file list beside `"scripts/acceptance_record.py"`.
4. **`tests/test_module_size_ratchet.py`**: `intake.py` 1,946 -> 1,947
   (section 5).

## 5. The size baselines and the ratchets (Done-when 4)

- **`acceptance_record.py`**: 989 -> about 693 SLOC. It has no `BASELINE`
  entry to re-stamp, before or after (under `THRESHOLD`), so the census
  passes with no edit for it (D7).
- **`landing_rules.py`**: about 320 SLOC, under `THRESHOLD`: no entry.
- **`intake.py`**: +1 SLOC for its one new import line, 1,946 -> 1,947, a
  reviewed upward re-stamp with that reason (the three calls now land in
  another module; otherwise only their qualifier and docstring text change).
- **`integrate.py`** 1,788 and **`check.py`** 1,339: unchanged (one import
  line moved or renamed in each). `adjudicate_act.py` 374 -> 375,
  `text_then_act.py` 116 -> 116: no entries.
- **Import layers**: `check -> acceptance_record` (deferred) becomes
  `check -> landing_rules` (deferred); `integrate -> landing_rules` is
  module-level; the deferred count stays 46, inside 14..46, with no re-stamp.
  No cycle (`landing_rules` imports `acceptance_record`, `spine_carrier` and
  `kitlib`, none of which imports it). `landing_rules` is outside the
  lifecycle band; `intake -> landing_rules` points out of the band.
- **Complexity**: no function body changes. Neither sensor has a row keyed to
  a moved function, so no row is re-keyed; the new test stays under both
  limits.
- **Smoke tier**: +1 test (the boundary test), 3,959 -> 3,960 of 4,060.

## 6. Documents, the scaffold and the RESYNC entry

Text the move makes false is corrected on this branch:

- `kitlib/git.py` (its docstring: "the ruling sync and the overrule sync in
  `acceptance_record`") and `kitlib/decisions.py` (its docstring and IF-256's
  body: "the git read is the ruling sync's, in `acceptance_record`") name
  `landing_rules`.
- `text_then_act.py` (its docstring's "shares `acceptance_record._commit_parents`,
  the ruling sync's parent reader", and the comment naming
  `acceptance_record.commit_parent_first_lines`), `intake.py` (the docstring's
  triggers (a) and (f) and `_routed_amendments`' docstring),
  `integrate.py` (`_ruling_sync_refusal`'s docstring) and `check.py` (the two
  import comments).
- `docs/enforcement-audit.md`'s parent-first row:
  `acceptance_record.staged_parent_first_lines` -> `landing_rules.`.
- `project-trajectory/README.md`: a kit-contents row for
  `scripts/landing_rules.py` after `held_status.py`'s.
- `kitlib/bootstrap_manifest.py`: a `MAPPING` row
  `("scripts/landing_rules.py", "scripts/landing_rules.py")` after
  `held_status.py`'s, with its comment (`integrate.py`, `intake.py` and
  `text_then_act.py` import it unguarded, `adjudicate_act.py` at module level
  and `check.py`'s two steps deferred, all in this list).
- The generated views (`trunk_step.py --root . --regen`):
  `docs/interface-reference.md` (IF-308's body now harvested from
  `landing_rules`), `docs/requirements/components.derived.toml` (LLR-358's
  placement, IF-308's seam side, CMP-008's modules), `PROJECT_STATE.html`.

The RESYNC entry, appended after the last section 3 entry:

> ### The landing rules move out of the acceptance record into their own module [since 9e8eb6e57]
>
> *(Anchored at the preceding commit: the change lands in the commits after it.)*
>
> **What changed.** The rules the landing runs on top of the acceptance
> record move, unchanged, out of `scripts/acceptance_record.py` into a new
> `scripts/landing_rules.py`: the ruling sync (`ruling_sync_lines`,
> `staged_ruling_sync_lines`, `commit_ruling_sync_lines`), the parent-first
> judgement (`parent_first_lines`, `parent_first_tiers`,
> `staged_parent_first_lines`, `commit_parent_first_lines`) and the trunk
> mint's settled-amendment filter and held-act arms (`settled_amendments`,
> `unanchored_rows`, `text_as_bound`), with their helpers.
> `acceptance_record` no longer defines them and keeps no second name for
> them. Every finding, refusal, its wording and its order are unchanged.
> `acceptance_record` keeps the two-tree comparison, the mirror rules, the
> merge slot's acceptance-act refusal, the judged-text identity
> (`accepted_text_digest`) and the readers the new module calls.
> `integrate.py`, `intake.py` and `text_then_act.py` import the new module
> unguarded, so a scaffold without it cannot merge, mint or run the hook's
> text-then-act step.
>
> **What to do.** Copy the new file in with the overwrite. If your own code
> imports any of the moved names from `acceptance_record`, import them from
> `landing_rules` instead. No registry or setting changes.
>
> **Kit-owned files — overwrite:** `scripts/landing_rules.py` (new),
> `scripts/acceptance_record.py`, `scripts/check.py`, `scripts/integrate.py`,
> `scripts/intake.py`, `scripts/text_then_act.py`, `scripts/adjudicate_act.py`,
> `scripts/kitlib/bootstrap_manifest.py`, `scripts/kitlib/git.py`,
> `scripts/kitlib/decisions.py`, `README.md`.

## 7. Phase 2, in order

1. **Red.** Add section 4's boundary test and section 2.2's import changes;
   run `tests/test_acceptance_record.py` and the eight switched modules and
   record the red lines (the boundary test fails on the missing module, the
   switched modules fail to load it).
2. **Green.** Create `landing_rules.py`: the 33 definitions cut verbatim, the
   import block, the three aliases, the docstring (boundary, header, IF-308's
   body, the ruling sync's and the mint arms' documentation). Cut them from
   `acceptance_record.py` and rewrite its docstring and IF-091's body.
   Re-point the five importing scripts (section 2.1). Verify the verbatim
   claim by comparing each moved definition's source segment with the base's.
3. The registry rows (section 3.2), checked to parse with `tomllib`; the
   scaffold, documents and RESYNC entry (section 6); `intake.py`'s size
   re-stamp; `trunk_step.py --root . --regen`, staging what it changes.
4. **Runs** (builder rule 5): every test module importing a changed module
   (`acceptance_record`, `landing_rules`, `check`, `integrate`, `intake`,
   `text_then_act`, `adjudicate_act`, `kitlib/bootstrap_manifest`,
   `kitlib/git`, `kitlib/decisions`: 80 modules by a grep at the base), the
   modules holding the tests tagged TC-147, TC-313, TC-397, TC-398 and TC-403
   (all among them), plus `test_import_layers`, `test_module_size_ratchet`,
   `test_complexity_ratchet`, `test_dogfood_sync`; then `trace.py --root .
   --strict`, `check_trajectory.py --root . --strict` and
   `run_menu.py smoke` once at the end. Real summary lines into the
   Deliverable.
5. Close out as the brief says: the Deliverable, `spec_move.py`, `specref`
   cleared, `check_docs.py`, the log fragment.

The sibling WI-1024 slice 3 changes design rows and tests only; it shares no
file with this plan except the generated views, which regenerate at either
merge.

## Decisions for the coordinator to confirm

- **D1. One new module, `landing_rules.py` (CMP-008)**, holding all three
  rule families. The alternative is two (per-commit rules; the mint's arms),
  each reading the same readers through the same seam; one keeps one seam and
  one boundary sentence.
- **D2. LLR-278 stays CMP-006.** `merge_acceptance_refusal` and its family
  (the 17 definitions behind LLR-278 in section 1.3, and `backed_act_refusal` and
  `lane_acceptance_refusal`, LLR-158) stay in `acceptance_record`, behind
  IF-091, for section 1.4's reasons.
- **D3. The judged-text identity stays in `acceptance_record`**, behind
  IF-129: one function for its three readers, no new crossing, no row or TC
  re-pointed (section 1.5).
- **D4. The record's readers stay with the record, under their names.**
  `_ledger_read`, `_reaccepted_added`, `_snapshot_copy_rows` (LLR-364 tags),
  `_tier_of`, `_tier_reads`, `_spine_rows_at`, `_commit_parents`,
  `_empty_tree` and `PARENT_FIRST_CSVS` stay; `landing_rules` imports them.
  No rename to public names (that would touch `held_status`, `text_then_act`
  and `adoption_record`), and no move of the two git primitives to
  `kitlib/git` (a better long-term home, but outside this row).
- **D5. The cover is IF-308 re-owned, IF-091 rewritten (data under the
  ceiling, body, `v2`), IF-256 losing its CMP-006 requestor; no new row.**
  The alternative, if every redirected call is to have a contract row of its
  own: **IF-327** (the ruling sync, offered as a call; owner CMP-008,
  requestors CMP-007 and CMP-008; body in `landing_rules`), with **TC-606**
  (`Drafted`, verifying LLR-298 and IF-327, its evidence the existing
  ruling-sync tests gaining a `TC-606` tag), because `check_trajectory
  --strict` refuses an interface row no test case cites. That costs two new
  rows owing first acceptance and tag edits to `tests/test_ruling_sync.py`.
- **D6. No compatibility re-export.** Every caller imports from
  `landing_rules`; `integrate` at module level (no deferred edge added),
  `check` deferred as today.
- **D7. Done-when 4's re-stamp is vacuous for `acceptance_record.py`:** it has
  no size-ratchet entry (989 SLOC under the 1,000 threshold at the base). The
  Deliverable ticks the item on the measured drop, and the one size edit is
  `intake.py`'s +1.
- **D8. Tests changed beyond their imports:** the new boundary test,
  `test_adjudicate_act`'s source-text assertion, `test_bootstrap`'s file
  list, and `test_module_size_ratchet`'s `intake.py` entry (section 4).
- **D9. TC-147, TC-397 and TC-403 keep their `verifies` cells.** IF-308's
  contract is unchanged and only its owner moves; the ledger and copy
  refusals TC-147 and TC-403 drive stay IF-091's readers' failures.
- **D10. Two pre-existing items are surfaced, not fixed:** the dead
  `verdict_rulings` alias in `acceptance_record` (no reader; it keeps a
  CMP-006 to CMP-008 edge into `kitlib/verdict`, so CMP-006's accepted notes
  sentence that `kitlib/verdict`'s other edges are internal is not true), and
  the unread `ARCHIVE_WORK_DIR`, which moves verbatim. A follow-up row can
  remove both.
- **D11. Acts owed: none new.** No `Accepted` row is amended and no routed
  traced change lands on one; IF-091, IF-256 and IF-308 are `Drafted` rows
  rewritten, each still owing the first acceptance it owed before. (Under
  D5's alternative, IF-327 and TC-606 each owe a first acceptance.)
- **D12. No delegated decisions record** (`docs/decisions/maint-wi-1045.toml`):
  each call above is this plan's, confirmed here.
