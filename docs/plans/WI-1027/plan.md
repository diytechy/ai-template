# WI-1027 plan: the parent-LLR link and one requirement-tree walk

Planned on branch `maint/wi-1027`, cut from `refactor_again` at `bba30552f`.
`planmode = "single"`: this commit carries the plan alone, and nothing else
changes until the coordinator's go-ahead.

Read in full: the spec (`docs/work/queued/WI-1027-parent-llr-link.md`), its
scope critique (`docs/reviews/2026-11-21-scope-critiques/WI-1027.md`), the
pointer rules (`docs/plans/2026-10-11-review-churn/pointer-rules.md`: the
model, the LLR row of the rules table, "A child LLR's SR", "What changes"),
the review-churn plan's F-call 5 and decomposition (b) text (README lines
111 and 508), the queue-drill hand-off's §0 steps 1 to 4, §3.3 and §3.4,
WI-1060's plan on its branch (§1's traced-cell rule C, §7's `record_rows.py`),
and the WI-1024 and WI-1029 specs. Code read, by function, in §3 below.
Rows read: SR-049, SR-139, SR-157, SR-168, SR-178, SR-186, SR-212, SR-217,
SR-241, SR-245, SR-248; LLR-001, 002, 003, 099, 118, 135, 153, 158, 167, 183,
186, 197, 199, 201, 210, 230, 231, 244, 245, 257, 259, 357, 360, 367, 403,
404, 408; TC-001, 147, 178, 181, 195, 197, 211, 399, 413 to 420, 485.

## 0. Measured (tree at `bba30552f`)

- **Design rows:** 356 live, all `Accepted`, all top-level: none carries a
  parent cell, none names no SR, 35 name two or more SRs. So no row migrates,
  and every reader below must give byte-identical output for this spine.
- **Test cases:** 427 live; 7 cite a design row without its SR (the shape the
  stage derivation resolves back through the design row).
- **Readers:** 33 scripts contain `sr_refs`, `SR-Refs` or `llrs_under`. 20
  read the design tier's link (§3 lists them by function; 19 change); 13 read
  only the work registry's `sr_refs` or carry the name in a comment.
- **The walk's home exists:** `kitlib.spine.llrs_under` already says it is
  "the one home of the SR-to-LLR walk, so a parent link between LLRs extends
  it here". It has one caller, `review_scope`. Every other reader re-derives
  the link from the cell.
- **Sizes (module-size ratchet, SLOC, threshold 1000):** `kitlib/spine.py`
  656; `rendering/traj_views.py` 987 (13 lines of room); `assumption_rules.py`
  958; `acceptance_record.py` 972; `trace.py` 3784, `intake.py` 1946 and
  `check_trajectory.py` 1663 are baselined exactly, so any growth there is a
  reviewed bump with its reason in the log fragment.
- **Test importers:** 130 of the 283 test modules import a module this row
  changes (`trace` 72, `check_trajectory` 40, `intake` 35, `spine_carrier`
  32, `kitlib.spine` 24, `acceptance_record` 24, ...). That is the Phase 2 run
  set under builder rule 5.
- **Blast radius is not on trunk:** `maint/wi-1024` carries no commit past its
  base, so WI-1024 adopts this walk (Done-when 2's "otherwise" arm).

## Rules every row this plan writes is held to

1. **No code names.** Row text names no file, module, function, symbol, CLI
   flag, step name or test name, inherited ones included; registry column
   names (`SR-Refs`, `Verifies`, `BridgedBy` ...) stay, as schema vocabulary.
   Of the three rows amended, LLR-367 and LLR-244 carry no code name today;
   LLR-257 carries four (a settings key, a tag spelling, a step name and a
   git feature name), each scrubbed in §7.
2. **One obligation, every clause tested.** Each new row states one
   obligation; each clause of a new or amended row is driven by a test its
   test case names (§8's map). No SR is written or amended.
3. **A child within its parent.** Checked per row in §7.
4. New rows are `Drafted`, phase 6 (the phase of the latest rows, LLR-404 to
   LLR-408). Amended `Accepted` rows change text only.

## 1. The cell (Done-when 1)

**Form.** Key `parent` on the design tier, column `Parent`: a plain string
naming one design row id, never an array (a child has one parent).

**Declared, loaded, shipped.**
- `kitlib.spine.SPINE_TIER_KEYS["LLR-ID"]` gains `parent` after `sr_refs`.
  The loader's undeclared-key rule (`spine_carrier.undeclared_key_findings`,
  WI-1023) refuses the key until then, which is the red test.
- `spine_carrier.SPINE_COLUMN` gains `"parent": "Parent"`;
  `migrate_carrier.KEY` gains the inverse `"Parent": "parent"` (the pinned
  pair in `test_rule_sync`). Not in `REF_COLS`: one id, kept a string.
- The shipped template `registries/low-level-requirements.template.toml`: its
  `-000` row, which is the tier's schema, gains `parent = "LLR-000"` with an
  OPTIONAL comment (a child names its one parent design row and carries no
  `sr_refs`; a top-level row omits the key and names its SRs); the header
  names the rule in one line. `test_dogfood_sync`'s three legs then agree.
  The live registry has no header and no row changes.
- `docs/registry-machinery-reference.md`: §4's table gains a `Parent` row and
  `SR-Refs` reads "required on a top-level row"; §5.1's triangle sentence reads
  a design row's requirements up its chain; §6 lists the new orphan findings;
  the hats paragraph's "its `SR-Refs` parents'" reads up the chain; §12's
  cell-split table adds `Parent` to the accepted column; §12.10, stale since
  `SR-Refs` became traced and routed, is rewritten to state both cells' class.

**Findings** (`coherence.py`, the orphan family beside "has no SR parent",
each naming the row, at any status, all failing `--strict`):
1. a top-level row naming no SR: today's `LLR X has no SR parent`, unchanged;
2. a child naming SRs: `LLR X is a child of LLR-Y and names SR-Refs (...)`;
3. a parent cell naming no live design row (a missing id, an SR id, a `-000`
   id): `LLR X names parent Z, which is no live design row`;
4. a parent cell naming several ids: `LLR X names N parents (...)`;
5. each row on a cycle, once: `LLR X is on a parent cycle (X -> Y -> X)`;
6. each row whose chain ends at 3, 4 or 5: `LLR X reaches no SR: its parent
   chain breaks at LLR-Y`.
`LLR X references unknown SR-Z` stays for a top-level row. The schema sweep:
`trace.REQUIRED_FIELDS["LLR"]` drops `SR-Refs`, and `schema_findings` asks it
of a row with no parent cell only, with today's message. Why the orphan
family and not the integrity floor: the two faults of the same kind today
(no SR parent, unknown SR) are there, and the Done-when says `--strict` (D8).

**Class in the acceptance record's cell split: accepted, not routed (D1).**
- *Accepted:* a re-parent changes which decomposition the row's detail is read
  against, so the acceptor's reading depends on it. As an accepted cell it
  drifts the row, shows in every drift reader and the operator page, drops
  the derived stage until re-accepted (SR-049's amendment arm), is bound into
  the verdict's judged-text identity, and the merge's amendment mint routes it
  to adjudication. Under WI-1060's rule C an unnamed row with drifted
  accepted cells keeps its recorded text, so it waits for its own act either
  way. Code: `acceptance_record.SPINE_ACCEPTED_CELLS` for the design registry
  gains `Parent` by name (the residual already classes it accepted, so this
  only states it); `ROUTED_TRACED_CELLS`, which WI-1060 moves to
  `record_rows.py`, is untouched. No accepted row enumerates the design
  tier's accepted cells, so no row is re-cut.
- *The alternative, traced and routed* like `SR-Refs` (the WI-388 ruling's
  shape), re-cuts two accepted rows that enumerate the routed cells: LLR-153
  ("routed traced cells: SR SN-Refs and Boundary-Refs, LLR SR-Refs and TC
  Verifies"), a 4,557-character row whose rewrite would scrub a dozen code
  names, and LLR-245 as WI-1060 rewrites it. It would also touch the two
  modules WI-1060 reworks. Not recommended.
- No spine row states any column's class, so if D1 stands its record is this
  plan, the reference doc's table and the RESYNC entry (D13 asks whether a
  decisions-record entry is wanted too).

**Parent-first (the acceptance-order rule): unchanged here (D2).** An
accepted child under a `Drafted` parent row is the same defect the rule
exists for, but SR-245 and LLR-357 each state a closed edge list ("SN-to-SR,
SR-to-LLR, and SR-or-LLR-to-TC"; "only declared ... references"), so adding
the LLR-to-LLR edge re-cuts an accepted SR's requirement and acceptance
criteria, its LLR and a TC. The gap is latent while no child exists.
Recommended: a follow-up row (I cannot mint a WI id).

## 2. The one walk (Done-when 2)

In `kitlib/spine.py`, beside `llrs_under`:

- **`llr_tree(llrs) -> LlrTree`**, one pure pass over the design rows, built
  once by a reader that walks many requirements (the quadratic-join reason
  `trace._bucket_by_ref` records). A frozen record of:
  - `below`: for each SR id and each design-row id, the design rows below it,
    every descendant once, in registry order. **Down from an SR:** the
    top-level rows naming it and every row below them. **Down from a design
    row:** its children and every row below them (blast radius's second arm).
  - `srs_of`: for each design-row id, the SR ids its chain reaches. **Up from
    a child:** the `SR-Refs` of the top-level row its parent chain ends at; a
    top-level row's own; `[]` for a broken chain.
  - `parent_of` and `depth` (0 for a top-level row), for the views.
  - `broken`: for each row whose chain does not end at a top-level row, why
    (missing, several, cycle, under) and the row it breaks at; the rules in
    §1 read it.
- **Edges.** A row hangs from its parent when its parent cell names an id,
  else from its `SR-Refs`. A child's own `SR-Refs` are ignored by the walk
  (finding 2 reports them), so a malformed row has one answer everywhere.
- **How it refuses a cycle.** It does not follow one. The up-walk keeps the
  ids its current chain has passed; meeting one again marks every row on the
  loop `cycle` and every row whose chain entered it `under`. Those rows reach
  no SR and sit below none, the rules report each, and no reader loops or
  raises. Each row's answer is memoized, so the pass is linear in the rows.
- **`llrs_under(srs, llrs)`** keeps its signature and registry order and reads
  `llr_tree(llrs).below`. `review_scope` is unchanged; `_unverified` counts an
  SR verified through any scoped row whose `srs_of` names it.

## 3. Every reader, by function

**Read the design tier's link; changed to the walk (19 files):**

| File | Function | Direction | Change and why |
|---|---|---|---|
| `kitlib/spine.py` | `llrs_under`, `_unverified` | down, up | the review test set (`review_set.py` reaches it only through `review_scope`, so that file is unchanged) |
| `coherence.py` | `_llr_orphan_findings`, `spine_orphan_findings` | up | §1's findings; the no-test finding on a parent says its children's cases do not discharge it (§4) |
| `trace.py` | `REQUIRED_FIELDS`, `schema_findings` | | `SR-Refs` required on a top-level row only |
| `trace.py` | `triangle_findings` | up | a TC citing a grandchild beside its chain's SR is coherent, beside another SR incoherent |
| `trace.py` | `effective_hats` (+ `hat_findings`) | up | an optional argument takes the walk's `srs_of`; a child's set unions its chain's SRs' hats. IF-141's contract body names the argument (a Drafted interface; its `data` cell is unchanged) |
| `trace.py` | `chain_buckets` -> `spine_chain` -> `reaccept_model`, and `reaccept_model`'s snapshot bucketing | down | an SR's chain holds every row below it, live and recorded, so the acceptance brief (`--accept modified`), `gen_open_items`, `amendment_brief.amendment_values` and the first-acceptance adjudication brief (`adjudicate_brief.first_acceptance_values`) see a child with no change of their own |
| `trace.py` | `acceptance_lines` | down | the batch acceptance hierarchy (`--accept <scope>`) nests a child under its parent; the direct-TC exclusion spans the subtree |
| `trace.py` | `build_forest`, `render_report` (matrix), `mermaid_graph` | down | the report's outline and HTML nest a child under its parent; only a row reaching no live SR is in "(LLRs with no SR parent)"; the matrix lists every row below an SR; the graph draws each parent link |
| `trace_text.py` | `paraphrase_advisories` | up | a child's Detail is compared with its chain's SRs |
| `derive_stage.py` | `_phase_groups`, `_ATTRIBUTED_ROWS` | up | a row joins its chain's SRs' phases, the walk built over the live rows so a settled child under a `Drafted` parent keeps its phase in the settled reading; a TC citing a design row resolves through `srs_of`; `Parent` joins the design row's attributed cells |
| `adjudicate_brief.py` | `_cited_spine` | down | the consolidation brief's `{spine}` names every row below the cluster's SRs |
| `intake.py` | `_context_block` (design-row join only) | down | the planning briefs: the context block the minted row's Context and the worker prompt render (D9) |
| `gen_components.py` | `_add_members` | up | a placed child reaches its chain's SRs |
| `assumption_rules.py` | `module_srs`, `component_srs` | up | the architecture arm's reach (D3) |
| `check_test_first.py` | `_associations`, `_members` | up, down | a TC is paired with a requirement through any row below it in the same copy (D3) |
| `census.py` | `_implemented_ids` (design half) | up | a row is claimed when every SR its chain reaches is a done row's |
| `consolidate.py` | `_llr_modules` | down | the touched-module pre-filter sees a child's files |
| `gen_release_checklist.py` | `_scope_ids` | down | a TC naming only a child stays in phase scope |
| `gen_okf.py` | `emit` | | the bundle exports the authored cell: a child's page links its parent, a parent's page lists its children |
| `check_trajectory.py` | `_placed_sr_components` | up | the knowledge-pack warn reaches a placed child's SR |
| `rendering/traj_views.py` | `_add_tier_rows`, `arch_icicle` | down | the dashboard (§5) |
| `spine_carrier.py`, `migrate_carrier.py`, `acceptance_record.py` | the column maps, `SPINE_ACCEPTED_CELLS` | | §1 |

**Read the design tier's link; unchanged (with why):**
- `spine_rules._decomposed_sr_ids` and `coherence._sr_orphan_findings`
  ("does this SR have a design row"): only top-level rows carry `SR-Refs` and
  every child sits under one, so the set is the walk's on every tree the
  strict check passes (D14).
- `trace_text.sr_fanout_advisories`: counts an SR's direct children, which
  are the top-level rows naming it by definition; nesting is the remedy the
  advisory points at.
- `kitlib.spine.PARENT_EDGES` / `parent_first_findings`: D2.
- `intake._owning_srs`: reads a routed `SR-Refs` record; under D1 a re-parent
  is an accepted change and never reaches that arm.

**Read only the work registry's `sr_refs`, or name it in a comment (13
files, unchanged):** `agent_brief` (`worker_prompt`, `build_scope_srs`),
`kitlib/registry.py`, `wi_convert.py`, `plan_artifacts.py`, `plan_briefs.py`
(`_parent_need_ids`, `hat_surface_for_work_item`, `round_questions`: a row's
SRs up to its needs, never to a design row), `plan_coverage.load_item`,
`rejudge._draft`, `review_brief._spec_text`, `review_set._row_srs`,
`schedule.load_wis`, and the comments in `baseline_snapshot`, `bootstrap`
and `check_doc_refs`; plus the work-row halves of `check_trajectory`,
`intake`, `census`, `consolidate` and `adjudicate_brief._other_open_rows`.

**Blast radius:** not on trunk. WI-1024 adopts `llr_tree(...).below` for an
SR and for a design row; if WI-1024 merges first, the coordinator decides
how this branch picks that up before its review (D10).

## 4. A parent's discharge, coverage and the stage over the tree (Done-when 3)

- **Discharge.** A parent is a row some child's parent cell names. LLR-408
  already holds the rule: a design row is discharged only by a live test case
  naming *it*, and one past `Drafted` that none names is reported and fails
  `--strict`. A parent's children's cases name the children, so they never
  discharge it; its own case is its integration TC. Code: the no-test finding
  on a parent appends `(a parent: its children's test cases do not discharge
  it)`. A `Drafted` parent is exempt as every `Drafted` design row is, which
  is what SR-248's acceptance criteria say ("a Drafted row that none verifies
  is not reported while it stays Drafted"); reporting a `Drafted` parent
  would contradict that accepted SR (D7).
- **Coverage over the tree.** Each descendant counts as a top-level row counts
  today, through the walk: an SR is verified through any verified row below
  it (`_unverified`), an unverified row below it is a gap in the review test
  set (a partial refusal for code-touching work), and an unverified row past
  `Drafted` is the orphan pass's no-test finding.
- **The stage over the tree.** `spine_stage` holds the design-row rung on
  any `Drafted` design row, children included, already; what changes is the
  per-phase grouping (§3), so a `Drafted` grandchild holds its SR's phase.

## 5. The dashboard's requirement-tree view (Done-when 4)

The What tab's icicle (`traj_views.arch_icicle`, flat and per-need drill
layers) has four fixed columns today (SN, SR, LLR, TC). It becomes one design
column per tree depth: a top-level row links to its first SR as now, a child
links to its parent and is drawn inside the parent's span one column further
in, and the TC column follows the deepest design column. As the component
view nests a part inside its whole, the tree reads as nesting rather than as
a second decomposition beside the first. With no child (this repository) the
render is byte-identical, so `PROJECT_STATE.html` does not move. The column
arithmetic goes into a small helper beside `TIER_COL` in
`rendering/traj_render.py` (570 SLOC) if `traj_views.py` would cross 1000.
The recursive weight/collect/draw walks stay recursive: links come from the
walk, which never links a cycle, so their depth is the tree's depth plus
three, and the comment claiming "capped at 4 by construction" is rewritten to
say so (D12).

## 6. PROCESS.md §4, the skills and the question list (Done-when 5)

PROCESS.md §4 states decomposition (b) once (the exact text is D6):

- The ladder block: `DevStg-Reqs` becomes "the obligations at the system's
  boundary. ONCE PER BOUNDARY" (under (b) an SR states behaviour at the
  system boundary only; "system and component alike. RECURSES" is (a)'s
  text); `DevStg-LLReqs` becomes "the design rows, each decomposing an SR or
  a parent row, down to rows one realization artifact (code, or a part
  source) carries. RECURSES IN ITS ROWS; ONE RUNG" in place of "TERMINAL".
- The paragraph "The boundary happens once; the recursion lives in the two
  rungs after it ... The tier does not recurse, the activity does ... no
  sub-rungs" becomes: only the system's frame comes from the needs, an SR
  states behaviour at that boundary, and below it two trees decompose
  together (the component tree by `PartOf`; the requirement tree by
  `parent`): a child names one parent row and carries no `sr_refs`, only a
  top-level row names its SRs, a child's SR is read up its acyclic chain, a
  parent is discharged by its children plus its own integration TC, and every
  derivation from an SR to its design rows walks the whole tree. "The rung
  does not recurse; the rows do": one `DevStg-LLReqs` rung holds while any
  row of the tree is in work, and the ladder adds no sub-rungs.
- "`DevStg-Reqs` and `DevStg-Arch` oscillate as the recursion descends"
  becomes `DevStg-Arch` and `DevStg-LLReqs` (the decrease `derive_stage`
  already exempts).
- §2's identifier table: the LLR parent link reads "`SR-Refs` on a top-level
  row, `Parent` on a child (§4)".

PROCESS.md is watched, not capped; the delta (about +600 bytes) is flagged in
the log fragment and the byte-budget table re-stamped.

Pointers, not restatements: the spine-authoring skill's "Authority" sentence
names §4 for "the requirement tree a design row decomposes into";
`prompts/spine-questions.md` §3 gains one bullet ("Decompose a design row
into child rows, not a sub-scope SR: `docs/process.md` §4") and its
`Hat-Refs` bullet reads "unioned with its SRs', a child's read up its chain".
The gate-advance skill restates the ladder lines and says `TERMINAL` and
"`DevStg-Reqs` and `DevStg-Arch` oscillate"; it is brought into line, since
leaving it would contradict §4. Each skill's three copies (`project-trajectory/
skills/`, `.claude/skills/`, `.agents/skills/`) stay byte-identical
(`test_skills_sync`). EXAMPLE.md and ADOPTING.md are unchanged.

## 7. The rows

### Accepted rows the change re-cuts: three, amended text only

**LLR-367 (SR-241, the review test set).** "every low-level requirement
referring to any of them" is false for a child, which refers to none. One
phrase changes; the title and rationale stay. Check against SR-241: a set
"derived from the work item's requirements" that reaches every row below
them stays inside it. Code names: none.

> The derivation reads the merge base, then one claimed work item found at the lane tip or that base, using its closed copy when available, then its requirement references, its changed paths and declared paths, before registries and test declarations. Its scope is the row's referenced system requirements, every low-level requirement below any of them in the requirement tree (one referring to it, and every row whose parent chain ends at such a row), and every test case of any status verifying either; directly verified system requirements have no gap. Each scoped test case is exactly one of tagged, declared non-executable, untagged executable, or no evidence. It returns the sorted union of tagged test files, lists a tagged test case's non-test evidence and declared non-executable evidence without running it, and returns every gap: a system requirement that no scoped test case verifies, directly or through a scoped low-level requirement, or a low-level requirement that no scoped test case verifies, an untagged executable test case, or a test case with no evidence; sibling low-level requirements are included. Code-touching is a changed path from merge base to staged tree under the declared source or tests roots, with both ends of a rename counted; all other paths are not code-touching. A code-touching row with no requirement reference refuses by name; one with any gap refuses partial naming every gap; one with no tagged file and no gap refuses empty; a row not touching code reports gaps without refusal, permits an empty set, and runs a non-empty set. Missing or multiple claims, malformed frontmatter or requirement references, a missing referenced system requirement, unreadable or malformed registries, paths declaration, trunk declaration, or a test-declaration refusal refuse by name; an unreadable input outranks partial and empty. The derivation reads the lane's own tree and never widens to the whole checks. Its covered behavior is the claim copy, scope walk, classes, changed-path decision, input refusals, set printing, recording, draw, rendering, and closed-lane routes; hand-edited claim copies or records, path aliases, and sub-second timing windows are outside this bound.

**LLR-244 (SR-212, the boundary and architecture arms), if D3 stands.** "the
requirements named in SR-Refs by the design rows" is false for a child. The
first sentence changes; the row has no title change and no rationale. Check
against SR-212, whose acceptance criteria say "reaches the requirements of the
design rows realized in the one file": inside it. Code names: none (column
names and stage labels stay).

> Each boundary interface, one carrying a from- or to-external tie-back, reaches the requirements of the design rows realized in the one file stating its contract body, a design row's requirements being those the requirement tree gives it: its own SR-Refs when it is top-level, and those of the top-level row its parent chain ends at when it is a child. That file is the one the definition gate's scan finds; the files realizing a design row are those the back-link index names for it; the two are compared through the one path normalizer. An interface with no contract body yet reaches none. Where no source is scanned, an interface instead reaches the requirements of the design rows placed in its owner component, a design row placed through the interfaces its verifying test cases name. The architecture arm judges each requirement whose form is interface against every boundary interface reaching it: one reached by none fails naming the requirement and stating that no boundary interface reaches it; each reaching interface with no Coincident whose BridgedBy shares no assumption with the requirement's DA-Refs fails naming the requirement and that interface, so one valid interface never excuses another invalid one. The harness gains a built-in step for the architecture arm at the DevStg-Arch threshold, gated by the same setting. The boundary arm judges the frame's crossings: each interface-form requirement with no Coincident fails once for each declared crossing its Boundary-Refs names on which no assumption in its DA-Refs lands (EffectAt), naming the requirement and that crossing; a crossing the frame does not declare is left to the frame's own reference rule. The harness gains a built-in step for the boundary arm at the DevStg-Boundary threshold, gated by the same setting. The relation is derived here and never recorded on an interface, and the stage fold gains no interface parameter.

**LLR-257 (SR-217, the test-first order), if D3 stands.** "through a design
row whose SR-Refs name the requirement" is false for a child. That phrase
changes, and four inherited code names are scrubbed: the settings key, the
`Implements:` tag spelling, the step name and "pickaxe". Check against
SR-217, whose acceptance criteria say "names the requirement or one of its
design rows": inside it.

> The start is a commit id the process settings declare for this check, read as text. When each requirement, and each pair of a test case and a requirement it names, was first accepted is read from the acceptance record, never by replaying the registries: the commits read are those that wrote the act ledger or the record's copies of the requirement, design and test-case registries at the record's current path, found by the act ledger's one history walk widened to those copies, and each commit's copies are read against every parent's through the shared row reader and acceptance-act rule. A commit that added a ledger entry is an act and dates exactly each row it carried into acceptance and each pair new in its copies, a pair being a test case accepted in a copy while it names the requirement directly or through a design row below the requirement in that same copy's requirement tree (one whose SR-Refs name the requirement, or a child whose parent chain ends at such a row), so a test case accepted earlier and re-pointed at the requirement, or reached through a design row re-pointed at it, is dated at the act that re-accepts it; a row born Accepted counts at its act, and a row's later re-acceptances are not its first. An act made on a side branch is ordered at the first first-parent commit that contains it, as a landing is, and named by its own commit. The record's first commit at its current path is its cut: nothing before it is read, in any earlier spelling of the record, since no reader is kept for a spelling the record has left behind and its history is cut cleanly there rather than translated; each acceptance its copies carry is known only to be at or before the cut while its ledger records an act, and is unread when the cut holds no ledger, an empty one or a malformed one; in this repository the cut is the vocabulary move, which reached trunk at the declared start. A row moved into Accepted from a word outside the status vocabulary is likewise known only to be at or before its act. Such a date settles the order when it falls at or before the landing, and for a requirement's own acceptance at or before the start; otherwise the requirement is reported as unread, never as a pass. A commit that changes the copies with a flip or a new pair and adds no ledger entry, or whose ledger or its parent's is malformed, is a gap: what it carries is unread, never a pass and never dated at a later act, and so is a requirement or test case reading accepted at the tip that no act in the record accepted. The start applies to the requirement's acceptance only, and test-case acceptances are read over the whole record, so a test case accepted after the implementation landed is reported even when both precede the start. Counting a row's occurrences in a commit's diff is not used, because an act accepting one row while withdrawing another nets to zero. A requirement's implementation lands at the earliest first-parent commit adding a back-link line naming it or one of its design rows, read with the one back-link grammar the reverse back-link scan defines. Each requirement accepted after the start whose implementation has landed is judged over the test cases whose Verifies name it or one of its design rows at the tip: the check reports each one accepted for it after the landing, naming the requirement, the implementation commit and each such acceptance commit, and each one that does not read accepted at the tip or that no act has accepted while it names the requirement, by name, on one line carrying the warning that those test cases' results may not reflect the intended behaviour. A shallow clone, a start commit that no longer exists or is not a first-parent ancestor of trunk, a start before the TOML registries, and registries still under an older carrier are reported as unreadable, never as a pass, the design registry held to both carrier rules with the requirement and test-case registries, since a test case reaching a requirement through a design row the TOML reader cannot see would otherwise drop out in silence; a rewrite that keeps the start on trunk is read as the history it now is. The harness's checks gain a warn-only built-in step for this order.

### Rows the spec names that need no amendment (D15)

Each stays true because LLR-481 (below) defines a design row's SRs, and an
SR's design rows, through the tree: wherever an accepted row says "the SR it
decomposes", "its SR parents" or "the chain", a child's answer is read up its
chain. Behaviour for a top-level row does not change.

- **LLR-001** (the orphan set: "LLR/TC without a parent"): a child with a
  resolvable chain has a parent; one without is still reported. The
  parenthetical summarises and already omits other orphan kinds (unknown ids,
  seam-only citations); LLR-480 states the new ones.
- **LLR-201** ("an LLR its SR parent and TC"): a child's SR parent is read up
  its chain; the tree rules join the cross-row module the row describes.
- **LLR-186** (per-phase grouping: "an LLR belongs to the phase of the SR it
  decomposes"): a child decomposes its chain's SR.
- **LLR-197** (the row vocabulary in the shared kernel): it enumerates
  neither the schema's keys nor the kernel's joins, and says "NOT CLAIMED:
  that these are the only shared row rules". Amending it would mean
  rewriting a long row dense with inherited code names for no false clause.
- Likewise unchanged: LLR-002 (triangle), LLR-135 (paraphrase: "its parent
  SR"), LLR-183 (effective hats: "its SR parents'"), LLR-199 (component view),
  LLR-153 (the context block's code map), LLR-167 and LLR-259 (the briefs'
  chains), LLR-118 (the operator page's chains), LLR-231, LLR-003, LLR-158
  (no row lists the design tier's accepted cells), LLR-408 (§4).

### New rows (`Drafted`, phase 6)

**LLR-480** (`sr_refs = ["SR-157"]`, `test_refs = "TC-560"`)
- title: "A design row hangs from one parent row or from its system requirements, and a malformed tree fails the strict check"
- detail: "A design row's parent cell, when present, names one other design row: the row is then a child and names no system requirement, its requirements being read up its parent chain; a row with no parent cell is top-level and names at least one system requirement. The strict check reports each of these, naming the row, whatever its status: a top-level row naming no system requirement; a child naming one; a parent cell naming anything but exactly one live design row, an example row not being live; each row on a cycle of parent links, naming the cycle's rows; and each row whose parent chain ends at one of those faults, naming the row where the chain breaks. The required-field check asks for system-requirement references on a top-level row only."
- rationale: "A child naming its own system requirements would give its parentage two homes that can disagree, so the chain is the one home. A row on a cycle or under a missing parent reaches no requirement, so every derivation starting from a requirement would drop it and its test cases; reporting it at the strict check keeps that loss visible."
- Within SR-157: each fault is a declared rule violation reported naming the row and failing the declared strict set.

**LLR-481** (`sr_refs = ["SR-157", "SR-049"]`, `test_refs = "TC-561; TC-567"`)
- title: "One walk over the requirement tree answers both directions, below every reader"
- detail: "One derivation relates system requirements and design rows. Down, from a system requirement or a design row, it returns every design row below it, each once, in registry order: the top-level rows naming the requirement, or the rows whose parent cell names the design row, and every row below those. Up, from a design row, it returns the system requirements its chain reaches: a top-level row's own, a child's those of the top-level row its parent chain ends at, and none for a row whose chain meets a missing parent or a cycle. It answers every input without raising and without looping, following each chain until a top-level row, a missing parent or a row the chain has already passed. The checker's rules and reports and the stage derivation take the relation from it, so a row below a top-level row counts wherever a top-level row counts."
- rationale: "A reader taking a design row's requirements from its own cell would lose every child, and two copies of the walk could disagree about which rows a requirement holds; one walk below its readers keeps a child's test cases in every derivation that starts from a requirement."
- Within SR-157 (the join its rules check) and SR-049 (the stage derived from the artifact states), the two parents LLR-197's shared-kernel row already has; the spec's `sr_refs` name both.

**LLR-482** (`sr_refs = ["SR-168"]`, `test_refs = "TC-562"`)
- title: "The state view draws a child design row inside its parent"
- detail: "In the state view's requirement decomposition, a child design row is drawn inside its parent row's span, one column further in than its parent; the test-case column follows the deepest design column, so a decomposition with no child row keeps one design column."
- rationale: "A child drawn beside its parent would read as a second decomposition of the requirement; drawn inside it, the view shows which row the child refines, as the component view shows a part inside its whole."
- Within SR-168 ("the requirement decomposition down to its leaves").

Test cases (each `Unit`, `Smoke`, automated, its evidence generated from the
tests' tags; `verifies` names the SRs beside the LLRs, as the triangle rule
asks):

| Id | Verifies | Method | Expected |
|---|---|---|---|
| TC-560 | SR-157, LLR-480 | Run the orphan pass and the strict check over a three-level tree of design rows beside one row of each fault: a top-level row naming no system requirement, a child naming one, a parent cell naming a missing row, one naming a system requirement, one naming two rows, a cycle of two rows and a cycle of one, and a row below the missing parent; once with the faulty rows Drafted and once Accepted. Run the required-field check over a child and a top-level row that each name no system requirement. Load a design registry whose rows carry parent cells. | The well-formed tree produces no report. Each faulty row is reported once, naming the row and its fault, at both statuses, and the strict check fails: each row on a cycle names the cycle's rows, and the row below the missing parent names the row where its chain breaks. The required-field check reports the top-level row and not the child. The registry loads. |
| TC-561 | SR-157, SR-049, LLR-481 | Call the walk over design rows listed out of tree order: a top-level row under one requirement with a child and a grandchild, a second requirement's top-level row, a child whose parent is missing, a cycle of two rows, and a row below the cycle. | Down from the first requirement: the top-level row, the child and the grandchild, each once, in registry order; down from the top-level row: the child and the grandchild; up from the grandchild: the first requirement; up from the row below the missing parent and from each row on or below the cycle: none. Every call returns. |
| TC-567 | SR-157, SR-049, LLR-481 | Over the three-level tree with one test case per row, run the checker's orphan pass; its triangle rule over a test case citing the grandchild beside each requirement; its paraphrase advisory over a grandchild echoing the first requirement; its perspective coverage with a perspective only on the first requirement; and its report's outline, matrix and graph. Derive the per-phase stage with the two requirements in two phases, with every row settled and then with the grandchild Drafted. | No row of the tree is reported as missing a system requirement; the case citing the grandchild beside the first requirement is coherent and beside the second is reported; the grandchild's echo is reported against the first requirement; its effective perspectives include the first requirement's; the outline nests the grandchild under the child under the top-level row, the matrix lists all three under the first requirement, and the graph draws each parent link. The grandchild falls in the first requirement's phase; Drafted, it holds that phase's live reading at the design-row rung, and the phase's settled reading equals the reading with it settled. |
| TC-562 | SR-168, LLR-482 | Render the state view's requirement decomposition over a three-level tree with one test case under each design row, and over the same requirements with every design row top-level. | The child is drawn inside the top-level row's span one column further in, and the grandchild inside the child's one column further again; the test-case column follows the grandchild's. With every row top-level the decomposition has one design column, followed by the test-case column. |
| TC-563 | SR-241, LLR-367 | Derive the review test set for one requirement over a three-level tree whose grandchild's test case is tagged, then with the grandchild's test case removed. | The grandchild's tagged test file is in the set and no gap is reported; without its test case the grandchild is named as a gap. |
| TC-564 (D3) | SR-212, LLR-244 | Run the architecture arm over an interface-form requirement whose only design row realized in a boundary interface's body file is a grandchild of a top-level row naming the requirement; once with the source scanned, and once unscanned with the grandchild placed in the interface's owner component. | In both readings the interface reaches the requirement, which is judged against it as one reached through a top-level row is. |
| TC-565 (D3) | SR-217, LLR-257 | Pair the test cases with the requirements over one copy of the registries in which a test case names only the grandchild of a top-level row naming a requirement. | The test case is paired with that requirement. |
| TC-566 | SR-248, LLR-408 | Run the orphan rules over a parent design row past Drafted whose child and grandchild each have a test case and which no test case names; again with a test case naming the parent; again with the parent Drafted and named by none; and over an Accepted grandchild no test case verifies. | The parent no case names is reported as having no test case, naming it, though its descendants are verified, and the strict check fails; named by a case it is not reported; Drafted it is not reported; the unverified Accepted grandchild is reported as having no test case. |

Checks: each TC's clauses sit inside the rows it verifies (TC-560's load
clause is LLR-480's cell; TC-567's readers are LLR-481's "checker's rules
and reports and the stage derivation"; TC-566 is LLR-408's rule on a parent).
Spare ids: LLR-483 to LLR-489, TC-568 to TC-574. After minting,
`trace.py --root . --bump-ids`.

**Acts owed for automated adjudication** (listed in the Deliverable): first
acceptances of LLR-480, LLR-481, LLR-482 and TC-560 to TC-567 (TC-564 and
TC-565 only under D3); amendments of `Accepted` LLR-367, and under D3
LLR-244 and LLR-257, each in its `Detail` cell. No routed traced change to
an accepted row.

## 8. The tests (Done-when 6), red before each walk changes

One fixture, `tests/llr_tree_fixtures.py` (a helper, not a test module):
SR-001 and SR-002 (two phases); LLR-001 top-level under SR-001, LLR-002 its
child, LLR-003 the grandchild; LLR-009 top-level under SR-002; one TC per
row, the parent's TC its integration TC; builders for the fault rows and a
writer that lays the registries into a temporary repository. New cases are
in-process, in the smoke tier: one new module, `tests/test_requirement_tree.py`,
except where an existing module is the reader's home. Each case is written,
run red against the unchanged reader, and its red line kept for the
Deliverable; then the reader changes.

| Module | Case (one line each) | TC | Done-when |
|---|---|---|---|
| `test_requirement_tree` | the walk down from an SR, down from a row, up from a grandchild, the missing parent, the cycle, registry order | TC-561 | 2 |
| `test_requirement_tree` | each of the six findings, at Drafted and Accepted; the well-formed tree is silent | TC-560 | 1 |
| `test_requirement_tree` | the required-field check asks `SR-Refs` of a top-level row only | TC-560 | 1 |
| `test_spine_carrier` | a design registry whose rows carry `parent` loads | TC-560 | 1 |
| `test_requirement_tree` | the cell split classes `Parent` accepted (D1) | (none) | 1 |
| `test_requirement_tree` | a parent past Drafted with verified children and no TC naming it is reported; named, or Drafted, it is not; an unverified Accepted grandchild is reported | TC-566 | 3 |
| `test_requirement_tree` | orphan pass, triangle, paraphrase, effective hats, outline, matrix and graph reach the grandchild | TC-567 | 2 |
| `test_requirement_tree` | the per-phase stage places the grandchild in SR-001's phase; Drafted, it holds the live reading | TC-567 | 2, 3 |
| `test_review_set_walk` | the grandchild's tagged file is in the set; untested, it is a gap | TC-563 | 2, 3 |
| `test_requirement_tree` | the icicle nests the grandchild two columns in, TC column last; an all-top-level spine renders byte-identically | TC-562 | 4 |
| `test_requirement_tree` | `--accept <scope>` nests the grandchild; the re-acceptance model's SR-001 chain holds a Drafted grandchild | (none) | 2 |
| `test_requirement_tree` | the first-acceptance brief's chain lists the Drafted grandchild; the consolidation brief's `{spine}` names it | (none) | 2 |
| `test_requirement_tree` | the context block's code map names the grandchild's files | (none) | 2 |
| `test_requirement_tree` | the component view, the implemented-id census, the touched-module pre-filter, the release checklist's scope, the OKF export and the knowledge-pack warn each reach the grandchild | (none) | 2 |
| `test_assumption_rules` | the architecture arm reaches the requirement through the grandchild, scanned and unscanned (D3) | TC-564 | 2 |
| `test_requirement_tree` | the test-first pairing reaches the requirement through the grandchild (D3) | TC-565 | 2 |

Cases marked "(none)" exercise readers whose rows this branch does not touch
and whose text holds under LLR-481's reading; they stay untagged regression
cases (D5). Existing guards that must stay green unchanged:
`test_trace_golden` (the report for a spine with no child is identical),
`test_dogfood_sync` (the three schema legs), `test_rule_sync` (the column
maps), `test_skills_sync`, `test_bootstrap` (byte caps), the spine-questions
quote checks in `test_architecture_decomposition_rubric`. Phase 2 runs the
130 importing modules, the modules holding every TC this branch touches, the
four the brief names, the two strict lints and `run_menu.py smoke` once. The
smoke tier gains about 50 in-process cases against `max-tests = 3890`; the
count is measured at the build, and a re-stamp, if needed, carries its reason.

## 9. The RESYNC entry (Done-when 7)

Variant F's entry after WI-1023's, anchored at the preceding commit:
"A design row may name one parent design row, and every walk from a
requirement to its design rows walks the tree". **What changed:** the
optional `parent` cell, the six findings, `SR-Refs` required on a top-level
row only, a re-parent of an accepted row being an amendment of that row, the
walk's readers (§3) and the dashboard's nested columns, PROCESS.md §4's
decomposition (b). **What to do:** nothing for existing rows (every row is
top-level); to decompose a row, write each child with `parent = "LLR-###"`
and no `sr_refs`, give the parent its own integration TC, and run
`python scripts/trace.py --strict`. **Kit-owned files, overwrite:** every
file under `scripts/`, `registries/low-level-requirements.template.toml`,
`PROCESS.md`, `prompts/spine-questions.md`, `skills/spine-authoring/` and
`skills/gate-advance/`. **Project-owned files:** none.

## Order of work (Phase 2, after the go-ahead)

1. The walk and the fixture (red: no walk), then `kitlib.spine`.
2. The cell: schema, carrier maps, template, cell split, the six findings and
   the schema sweep, the parent note (red each), then the code.
3. The checker, the stage and the review test set walk the tree.
4. The acceptance, adjudication and planning briefs walk the tree.
5. The dashboard.
6. The remaining readers (and D3's two).
7. The rows: three new LLRs, the TCs, the amendments; `--bump-ids`;
   `--regen-evidence`; `trunk_step.py --root . --regen`.
8. PROCESS.md §4, the skills, the question list, the reference doc, the
   RESYNC entry; `check_docs.py`.
9. Close: the Deliverable (each Done-when item, the red-first lines, the
   tests with their summary lines, the acts owed), the spec moved to
   `complete/` with `specref` cleared, the log fragment
   `docs/log.d/WI-1027-parent-llr-link.md` (the trace.py ratchet bump and the
   PROCESS.md byte delta with their reasons).

## Decisions for the coordinator

- **D1. The cell's class: accepted** (stated by name in the cell split),
  not traced-and-routed like `SR-Refs`: no accepted row re-cut, and no change
  to the routed table WI-1060 moves. The alternative re-cuts LLR-153 and
  LLR-245.
- **D2. Parent-first is not extended to the parent link here**; a follow-up
  row carries it, since SR-245, LLR-357 and a TC each state the closed edge
  list. Latent while no child exists.
- **D3. Change the architecture arm's reach and the test-first pairing to
  the walk**, amending LLR-244 and LLR-257 (one phrase each, plus LLR-257's
  four scrubs) with TC-564 and TC-565. The alternative leaves both readers on
  the cell and files them as a follow-up: neither is in the Done-when's
  list, and both are latent until a child exists.
- **D4. The new rows:** LLR-480 (the cell and its faults, SR-157), LLR-481
  (the walk, SR-157 and SR-049), LLR-482 (the dashboard, SR-168); TC-560 to
  TC-567 as in §7.
- **D5. Reader cases for untouched rows stay untagged** (mapped to Done-when
  2 in the Deliverable), rather than tagged into those rows' accepted TCs,
  whose method text does not describe them, or given new TCs.
- **D6. PROCESS.md §4's text** as §6 sets out, including the `DevStg-Reqs`
  line ("at the system's boundary", no longer "RECURSES") and the
  oscillation sentence (`DevStg-Arch` and `DevStg-LLReqs`), and the
  gate-advance skill brought into line.
- **D7. A `Drafted` parent owes no integration TC yet**, as every `Drafted`
  design row (SR-248's acceptance criteria); the finding fires on a parent
  past `Drafted`.
- **D8. The tree's faults are orphan-family findings** (fail `--strict`, not
  the commit hook's `--strict-integrity`), beside "has no SR parent".
- **D9. "The planning briefs" are the context block** (`intake.context_block`,
  in the minted row's Context and the worker prompt); `plan_briefs.py` reads
  a row's SRs up to needs and reaches no design row, so it is unchanged.
- **D10. Blast radius:** WI-1024 adopts `llr_tree(...).below` for an SR and
  a design row. If WI-1024 merges first, how this branch takes it up before
  review is yours to call.
- **D11. `effective_hats` takes the walk's answer as an optional argument**
  and unions the chain's SRs' hats, not an intermediate parent row's own
  (LLR-183 says "its SR parents'"; widening it would re-cut that row).
- **D12. The dashboard:** one design column per depth, TC column last,
  byte-identical with no child, the column helper in `traj_render.py` if
  `traj_views.py` would cross 1000, the recursive walks kept with the
  rewritten depth comment.
- **D13. A decisions-record entry for D1:** no spine row states any column's
  class; is this plan and the reference doc the record, or do you want
  `docs/decisions/maint-wi-1027.toml`?
- **D14. `spine_rules._decomposed_sr_ids` and `coherence._sr_orphan_findings`
  stay on the cell:** the same set as the walk's on every tree the strict
  check passes.
- **D15. LLR-001, LLR-201, LLR-186 and LLR-197 are not amended** (§7's
  reasons), so of the spec's S5 list only LLR-367 is re-cut.
