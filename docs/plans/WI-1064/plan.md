# WI-1064 plan: the parent-first rule reads a child design row's parent link

Planned on branch `maint/wi-1064`, cut from `refactor_again` at `c7d6bd6f4`.
`planmode = "single"`: this commit carries the plan alone, and nothing else
changes until the coordinator's go-ahead.

Read in full: the spec (`docs/work/queued/WI-1064-parent-first-llr-parent.md`),
its scope critique (`docs/reviews/2026-11-23-scope-critiques/WI-1064.md`), its
specref (WI-1027's archived spec, `docs/archive/work/complete/WI-1027-parent-llr-link.md`)
and WI-1027's plan (`docs/plans/WI-1027/plan.md`, its D2 and the
"Parent-first ... unchanged here" paragraph). Rows read: SR-245, SR-246,
LLR-338, LLR-357, LLR-358, IF-308, TC-368, TC-396, TC-397. Code read,
by function, in §2 and §3 below.

## 0. Measured (tree at `c7d6bd6f4`)

- **The gap is real.** Two design rows, one top-level and `Drafted`, its child
  `Accepted` and naming it in `parent`, read through the carrier (TOML and
  legacy CSV both give the child a `Parent` cell) produce no entry from
  `kitlib.spine.parent_first_findings`. So no route reports or refuses them.
- **No standing case on this repository.** 368 design rows (360 `Accepted`,
  8 `Drafted`); none carries a `parent` cell, and the rule's findings over
  the four tiers as the commit judgement reads them (`parent_first_tiers(root, ":")`)
  are `[]` with no read failure. Adding the edge moves no finding here.
- **The edge list's one home** is `kitlib.spine.PARENT_EDGES`, a dict of one
  `(cell, parent tiers)` pair per child tier; nothing else reads it (the act
  assembler's test pins that it does not restate it). `parent_first_findings`
  is its one reader; it is cyclomatic 4 (ruff C901), the limit 10.
  `kitlib/spine.py` is 834 SLOC (module-size threshold 1000, not baselined).
- **Smoke tier:** 3877 of `max-tests = 3890` collected (`pytest --collect-only -q -m smoke`
  on this tree). This row adds 4 in-process cases (§5), leaving 9.
- **Importers:** 26 test modules import `kitlib.spine` directly;
  `trace.py --tests-for project-trajectory/scripts/kitlib/spine.py` lists 31
  spine-linked modules (§5 lists the run).

## 1. The edge (brief item 1)

**Where the closed list lives.** In code, `PARENT_EDGES` in
`project-trajectory/scripts/kitlib/spine.py`: `"SR": ("SN-Refs", ("SN",))`,
`"LLR": ("SR-Refs", ("SR",))`, `"TC": ("Verifies", ("SR", "LLR"))`. In rows,
SR-245 (the requirement and its acceptance criteria name the three child
kinds) and LLR-357 ("It classifies only declared SN-to-SR, SR-to-LLR, and
SR-or-LLR-to-TC references"); TC-396's method names the four edges it drives.
In prose, the `spine-authoring` skill ("An SR waits for every SN it cites,
an LLR for every SR, and a TC for every SR and LLR it verifies"), the
registry machinery reference §4.1 and the enforcement audit's row for the
rule.

**How the parent link joins it.** `PARENT_EDGES` maps each child tier to a
tuple of `(cell, parent tiers)` pairs, and the design tier gains a second:

```python
PARENT_EDGES = {
    "SR": (("SN-Refs", ("SN",)),),
    "LLR": (("SR-Refs", ("SR",)), ("Parent", ("LLR",))),
    "TC": (("Verifies", ("SR", "LLR")),),
}
```

`parent_first_findings` walks each child tier, each row in registry order,
and, for an accepted row, each of its tier's pairs through the unchanged
`_unaccepted_parents`. So the output keeps its contract (child tiers in SR,
LLR, TC order, rows in registry order), with a design row's `SR-Refs`
findings before its `Parent` finding; the docstring's contract says so. A
flat list of `(child tier, cell, parent tiers)` triples was the alternative:
it would list every `SR-Refs` finding of the design tier before any `Parent`
finding, breaking "rows in registry order". The cell is read by the same
`refs()` the tree walk (`llr_tree`) reads it with.

**What it inherits, unchanged.**
- *Classification.* The child side is the shared predicate
  (`claims_acceptance`: `Accepted` or `Founded`, any letter case); the parent
  side is `_unaccepted_parents`: a declared parent that does not claim
  acceptance, a missing status reading `no status`. The line and its remedy
  are `parent_first_line`'s, unchanged.
- *Exclusions.* The parent tier of the new edge is the design tier alone, as
  an LLR's `SR-Refs` reads only SRs and a TC's `Verifies` only SRs and LLRs.
  So a `parent` cell naming an SR, an undeclared id or a `-000` row raises no
  parent-first finding: each is already the orphan rules' finding (`names
  parent Z, which is no live design row`), as "unresolved parentage is the
  orphan rules'" says beside the table. `-000` children are skipped by
  `_declared_rows`, so the shipped template's example row (`parent = "LLR-000"`)
  stays silent. A `parent` cell naming several ids, or a cycle, judges each
  declared design row it names, as any cell does; the orphan rules report
  the shape.
- *Status movement.* The commit judgement's `_status_moved` compares the
  child's and the parent's statuses by id across every tier, so a design-row
  parent's status is read with no change. One consequence, the same as for a
  re-pointed `SR-Refs` today: re-parenting an accepted child under a
  `Drafted` design row with no status move is not refused by the
  `parent-first` step; it is the standing finding (the hook's
  `registry-integrity` step runs it), and the re-parent is an amendment of
  the row, since `Parent` is accepted text (WI-1027's D1).
- *Chains.* Each link is judged once: a child under an accepted parent that
  is itself under a `Drafted` SR is not a finding; the parent is.

## 2. Every route (brief item 2)

Each route below reaches the rule through `parent_first_findings` and reads
rows from a carrier read that already yields the `Parent` cell, so none
changes:

| Route | Path, read | Reaches the edge by |
|---|---|---|
| The standing integrity check | `trace.integrity_sweep` (from `analyze`): `_spine.parent_first_findings(dict(raw, SN=reg.raw_sns))`, each line prefixed `parent-first: `; `raw["LLR"]` is `spine_carrier.load(...)` rows. Run by `trace.py --strict-integrity` and `--strict`, the hook's `registry-integrity` step, every stage's checks, CI and the slot's landing checks | the new table entry |
| The commit hook's staged check | `check.py --parent-first` (the hook's `parent-first` step, `_parent_first_mode` -> `_parent_first_refusal`) -> `acceptance_record.staged_parent_first_lines` -> `parent_first_lines(root, [HEAD, MERGE_HEAD])` -> `parent_first_tiers` (`_tier_reads` -> `spine_carrier.tier_rows_from_text`) and `parent_first_findings`, filtered by `_status_moved` | the new table entry |
| A supported lane commit's admission (IF-308) | the merge slot, `integrate._text_then_act_refusal` -> `_each_lane_commit` over `text_then_act.LANE_COMMIT_RIDERS`, whose third rider is `acceptance_record.commit_parent_first_lines` -> `parent_first_lines(root, parents, rev)` | the new table entry |
| The derived act's waiting flips | `adjudicate_act._derive` -> `_waits` -> `acceptance_record.parent_first_tiers(root, rev + ":")` -> `_waiting` -> `_findings` -> `kspine.parent_first_findings` | the new table entry (§3) |

Searched for any other: every module naming `parent_first`, `PARENT_EDGES`
or "parent-first" is above (`acceptance_record`, `adjudicate_act`, `check`,
`text_then_act`, `trace`, `kitlib/spine`); `held_status` (the fourth lane
rider) judges rungs, not parent edges; the squash path judges no
parent-first commit ("a squash's staged tree is judged like any other").
The acceptance brief's hierarchy and the act brief's wording only render.

## 3. The derived act's waiting flips (brief item 3)

They follow the new edge with no change of their own. `_findings(tiers,
accepted)` reads every row in `accepted` as `Accepted` on a copy and asks
`kspine.parent_first_findings`; the rows are the hook's own
(`parent_first_tiers`), which carry `Parent`. `_waiting` drops, to a fixpoint,
every flip the findings name as an accepted child, so a child design row
whose parent design row is neither accepted at the revision nor flipped by
a non-waiting flip waits, and a grandchild under a waiting child waits too.
`_waiting_lines` names each parent with its status; the brief's "a parent it
cites is not accepted" reads true of a parent cell. LLR-338 states the wait
generically ("a parent the parent-first rule reads for it"), so its text
holds. One test edit only: the pin that the act restates no edge
(`test_the_wait_is_read_from_the_parent_first_rules_one_predicate`) adds
`'"Parent"'` to the cells it forbids in the act's source.

## 4. The rows (brief item 4)

No new row; no id minted (D4 is the one place a new id could be wanted:
TC-581). Amended, text only (each row `Accepted`; each owes an amendment
act). Checked under the three row rules: no code name (none inherited in
the cells touched; TC-396's "strict-integrity" spelling of the flag is
scrubbed to "strict integrity"); one `shall`; each new clause driven by a
test tagged with the row's TC (§5); each child within its parent.

**SR-245, `requirement`** (insertion: "or names a declared parent LLR in its
parent cell"):

> The delivered governance capability shall report every standing case in
> which an SR with Accepted or Founded status cites a declared SN parent, an
> LLR with either status cites a declared SR parent or names a declared
> parent LLR in its parent cell, or a TC with either status cites a declared
> SR or LLR parent that lacks either status as one parent-first integrity
> finding that names the child and parent with both statuses, reads a
> missing status as no status, directs acceptance of the parent or return of
> the child to Drafted, and causes strict integrity to fail; treat only
> Accepted or Founded, regardless of letter case, as accepted and an
> out-of-vocabulary status as unaccepted; exclude IF, B, DA, undeclared, and
> -000 references from this judgement; and replace the former non-failing
> advisory for an Accepted TC citing a Drafted LLR with that integrity
> finding.

**SR-245, `acceptance_criteria`** (insertion: "or naming such a declared
parent LLR in its parent cell"):

> Each Accepted or Founded SR citing a Drafted, missing-status, or
> unknown-status declared SN parent, LLR citing such a declared SR parent or
> naming such a declared parent LLR in its parent cell, or TC citing such a
> declared SR or LLR parent produces exactly one strict integrity finding
> beginning parent-first: and reading <child> (<status>) is accepted under
> <parent> (<status>), which is not: accept <parent> in its own acceptance
> act, or return <child> to Drafted; a missing parent status reads no
> status, and strict integrity fails. Accepted and Founded are recognized
> regardless of letter case, while an out-of-vocabulary status is
> unaccepted. A Founded parent produces no finding. IF, B, DA, undeclared,
> and -000 references produce no parent-first finding. No non-failing
> LLR-status advisory remains for an Accepted TC citing a Drafted LLR.

Title, rationale and coincident unchanged (each speaks of "an accepted child
beneath an unaccepted parent", true of the new edge).

**LLR-357, `detail`** (the second sentence gains the edge and what it reads):

> The parent-first rule uses one shared acceptance predicate with
> acceptance-act readers: it recognizes Accepted or Founded regardless of
> letter case, and an absent or out-of-vocabulary status does not claim
> acceptance. It classifies only declared SN-to-SR, SR-to-LLR, LLR-to-LLR,
> and SR-or-LLR-to-TC references in supplied spine rows, an LLR-to-LLR
> reference being the parent LLR that a child LLR's parent cell names. It
> emits one finding for each child that claims acceptance whose declared
> parent does not, carrying the child and parent identities and statuses,
> and renders that finding as <child> (<status>) is accepted under <parent>
> (<status>), which is not: accept <parent> in its own acceptance act, or
> return <child> to Drafted, with no status for a missing status. It emits
> none for a parent that claims acceptance, an undeclared or non-spine
> reference, or a -000 example row. The integrity result includes each
> standing finding under the parent-first integrity label, so strict
> integrity fails, and that finding replaces the former non-failing advisory
> for an Accepted TC citing a Drafted LLR.

Rule 3: within SR-245 as amended (the same edge, read from the same cell).
A `parent` cell naming an SR is no LLR-to-LLR reference, so "classifies
only" leaves it out, which is §1's exclusion.

**TC-396, `method`:**

> Exercise the shared, case-insensitive Accepted-or-Founded predicate and
> the in-process parent-first rule for each SR-to-SN, LLR-to-SR,
> child-LLR-to-parent-LLR, TC-to-SR, and TC-to-LLR edge; founded,
> missing-status, and unknown-status cases; the exact finding and remedy;
> undeclared, non-spine, and -000 exclusions, a child LLR's parent cell
> naming a requirement among them; then exercise an Accepted SR under a
> Drafted SN and an Accepted child LLR under a Drafted parent LLR through
> the strict integrity finding, and the retirement of the former LLR-status
> advisory.

**TC-396, `expected`:**

> The shared predicate recognizes Accepted or Founded regardless of letter
> case and rejects an absent or out-of-vocabulary status; each child it
> recognizes under a declared parent it does not, a child LLR under the
> parent LLR its parent cell names included, produces exactly one
> parent-first integrity finding whose text names both rows and statuses,
> reads a missing status as no status, gives the acceptance-or-Drafted
> remedy, and makes strict integrity fail; a parent the predicate
> recognizes, an IF, B, DA, undeclared, or -000 reference, and a parent cell
> naming a requirement produce none; the former LLR-status advisory is
> absent.

Rule 3: within SR-245 and LLR-357 as amended.

**Not amended (D3).** SR-246, LLR-358 and TC-397 state no edge list: SR-246
refuses "an Accepted or Founded child under a declared parent without either
status", LLR-358 returns "a parent-first finding", TC-397 drives "each parent
edge". Each takes its edges from the rule SR-245 and LLR-357 state, so each
stays true with the edge added, and the new tests tagged TC-397 (§5) are
cases of its existing text. LLR-338 and TC-368 are unchanged (§3); IF-308
(`Drafted`, the call) is unchanged. TC-396's and TC-397's `evidence` cells
are regenerated from the tags (traced and not routed: no act).

The fallback, if the coordinator wants SR-246 and LLR-358 amended anyway:
SR-246's requirement and acceptance criteria and LLR-358's detail each read
"declared parent" as "declared parent, a child LLR's parent LLR among them",
nothing else changing; TC-397 unchanged.

## 5. The tests (brief item 5)

Red first: each new-behaviour test is written and run against the unchanged
rule, and its failure line quoted in the Deliverable; then the table entry.
Characterizations name, in their docstring, the wrong implementation they
catch (the module's convention).

| Module | Test | Done-when | Kind | TC |
|---|---|---|---|---|
| `test_parent_first.py` | `PAIRS` gains `"LLR-LLR": ("LLR-002", "LLR-001")`; the builders write a child's design-row parents into `Parent` (`row`) and `parent = "..."` (`registry_text`); so `test_an_accepted_child_under_an_unaccepted_parent_is_found[LLR-LLR]` gives the one entry | 1 | red first | TC-396 |
| `test_parent_first.py` | new `test_a_parent_cell_is_judged_only_against_declared_design_rows`: one real case beside a `parent` naming a `Drafted` SR, an undeclared id, a `-000` row and a `Founded` design row; exactly the one entry | 1 (exclusions) | red first (the real case) | TC-396 |
| `test_parent_first.py` | new `test_a_child_design_row_is_refused_at_the_commit_only_where_a_status_moved`: the commit judgement with git reads replaced: a flip of the child under a `Drafted` parent design row is one `the index: ` line; the same standing case under an unrelated change is `[]` | 1 (status movement), in-process pin of the staged route | red first (first half) | TC-397 |
| `test_parent_first_git.py` | `test_staging_an_accepted_child_under_a_drafted_parent_is_refused[LLR-LLR]`, through `PAIRS`: `check.py --parent-first` exits 1 naming both rows | 3: the staged refusal | red first | TC-397 |
| `test_parent_first_git.py` | `test_a_no_verify_lane_commit_with_a_violation_is_refused_at_the_slot`, parametrized over `PAIRS` (D5): the slot refuses the lane commit, naming its sha10, both rows and the child's remedy, and not text then act's | 3: the lane commit's refusal | red first (`[LLR-LLR]`) | TC-397 |
| `test_parent_first_git.py` | `test_an_act_accepting_parent_and_child_together_passes`, parametrized over `PAIRS` (D5): exit 0. Witness: a judgement reading the parent's status from the parent tree refuses it | 3: the simultaneous acceptance | characterization | TC-397 |
| `test_trace_rules.py` | new `test_an_accepted_child_design_row_under_a_drafted_parent_reds_strict_integrity`: the minimal scaffold's design registry gains a `Parent` column, a `Drafted` top-level row and an `Accepted` child (its case verifying the SR and the child); `trace.py --strict-integrity` exits 1 with `parent-first: LLR-002 (Accepted) is accepted under LLR-001 (Drafted)` | 3: the standing finding | red first | TC-396 |
| `test_adjudicate_act.py` | new `test_a_child_design_row_waits_on_its_returned_parent_design_row`: a verdict accepting a top-level row under the accepted SR and a child design row, and returning the child's `Drafted` parent; the act lists the first, names the child `waiting on LLR-003 (Drafted)`, and the listed act, taken, passes the commit judgement | 3: the derived act's waiting child | red first | none (D4) |
| `test_adjudicate_act.py` | `test_the_wait_is_read_from_the_parent_first_rules_one_predicate` forbids `'"Parent"'` too | §3 | strengthened pin | TC-368 (as now) |

Done-when 2 (the coverage bound) is a statement of scope, no test: the
routes above are the kit's, and the Deliverable says hand-edited kit-written
state is outside the promise (PROCESS.md §6, "Review threat model").
Done-when 4 is the Deliverable's list of acts owed.

**The run** (the drill's rule 5): every test module importing `kitlib.spine`
(the 26) and every one `trace.py --tests-for` lists for it (the 31, merged);
the modules holding TC-396's, TC-397's and TC-368's tests
(`test_parent_first`, `test_parent_first_git`, `test_trace_rules`,
`test_adjudicate_act`, `test_coordinator_act`); for the skill edit
`test_skills_sync`, `test_skills_index`, `test_prompts`,
`test_adjudicate_brief`; and `test_import_layers`,
`test_module_size_ratchet`, `test_complexity_ratchet`, `test_dogfood_sync`.
Then `trace.py --root . --strict`, `check_trajectory.py --root . --strict`,
`trunk_step.py --root . --regen` before the registry commit, and
`run_menu.py smoke` once at the end.

## 6. Prose (D6)

The three places that enumerate the rule's edges, each by one clause:
- the `spine-authoring` skill (`project-trajectory/skills/`, synced to
  `.claude/skills/` and `.agents/skills/`): "An SR waits for every SN it
  cites, an LLR for every SR it cites and a child LLR for the parent LLR it
  names, and a TC for every SR and LLR it verifies.";
- `docs/registry-machinery-reference.md` §4.1: "whose cited SN, SR or LLR
  parent (a child design row's `Parent` included) is not accepted", and the
  `Parent` row of §4's column table gains "A parent-first edge (§4.1).";
- `docs/enforcement-audit.md`, the rule's row: "..., an LLR after every SR,
  a child LLR after the parent LLR it names (WI-1064), a TC after ...".

No PROCESS.md text states the edges; none changes.

## 7. The RESYNC entry

Appended after the requirement-tree entry in
`project-trajectory/RESYNC_PACK.md`:

> ### The parent-first rule reads a child design row's parent link [since c7d6bd6f4]
>
> *(Anchored at the preceding commit: the change lands in the commits after it.)*
>
> **What changed.** The parent-first rule (`scripts/kitlib/spine.py`) judged
> three kinds of parent: a requirement's needs, a design row's requirements
> (`sr_refs`) and a test case's verified rows. A child design row's `parent`
> (the requirement-tree entry above) is now a fourth: an accepted
> (`Accepted` or `Founded`) child design row whose `parent` names a declared
> design row that is not accepted is one parent-first finding, worded as the
> others. Every route that reads the rule takes it with no change of its
> own: `trace.py --strict-integrity` (and `--strict`) reports a standing
> case; the pre-commit `parent-first` step and the merge slot's lane-commit
> walk refuse a commit that moves either status into one; a derived act
> names such a child's flip as waiting while its parent stays unaccepted
> after the act. The edge keeps the rule's exclusions and the commit
> judgement's status-movement condition: a `parent` naming an SR, an
> undeclared id or a `-000` row is not judged here (the orphan rules report
> it), and a commit that moves neither status is not refused. The
> `spine-authoring` skill's statement of the rule names the edge.
>
> **What to do.** Nothing for a registry whose design rows carry no
> `parent`. Where one does, run `python scripts/trace.py --strict-integrity`:
> each child accepted under a parent design row that is not accepted is now
> a finding, cleared by accepting the parent in its own acceptance act or
> returning the child to `Drafted`.
>
> **Kit-owned files — overwrite:** `scripts/kitlib/spine.py`,
> `skills/spine-authoring/SKILL.md`.
>
> **Project-owned files — edit:** none.

## 8. Commits (Phase 2)

1. The tests, red (quoted, not committed red): then `PARENT_EDGES` and
   `parent_first_findings`, the rows, the regenerated evidence and views
   (`trunk_step.py --regen`); one commit, `WI-1064: the parent-first rule
   reads a child design row's parent link`.
2. The prose (§6) and the RESYNC entry: `WI-1064: the skill, the reference,
   the audit and the RESYNC entry name the parent-link edge`.
3. The close-out: the Deliverable, `spec_move.py` to `complete/`, `specref`
   cleared, `check_docs.py --root .`, the log fragment
   `docs/log.d/WI-1064-parent-first-llr-parent.md`.

No decisions record (the drill's rule 11): the one design call, which tier
a `parent` cell's parent is read from, is stated by the amended SR-245 and
LLR-357.

## 9. Decisions for the coordinator

- **D1. The edge's shape and parent tier.** `PARENT_EDGES` maps a child tier
  to its `(cell, parent tiers)` pairs; the design tier gains `("Parent",
  ("LLR",))`, judged per row after `SR-Refs`. A `parent` naming an SR, an
  undeclared id or a `-000` row raises no parent-first finding (the orphan
  rules own it).
- **D2. No route's code changes.** The standing check, the staged step, the
  lane commit's admission (IF-308) and the derived act's waiting flips all
  reach the edge through the one table; only the rule and its docstring
  change.
- **D3. SR-246, LLR-358 and TC-397 are not amended**, against Done-when 4's
  wording, since none states an edge list; the Deliverable says so per row.
  Alternative: §4's fallback (one phrase in each of SR-246's two cells and
  LLR-358's detail), two more amendment acts.
- **D4. The derived-act test stays untagged** (WI-1027's D5 precedent: a
  reader case for an untouched row), in the module holding TC-368's tests,
  so any review set reaching LLR-338 runs it; mapped to Done-when 3 in the
  Deliverable. Alternative: a new `Drafted` TC-581 verifying LLR-338, owing a
  first acceptance.
- **D5. The lane-commit and simultaneous-acceptance git tests are
  parametrized over every edge (`PAIRS`)**, four more slow cases each.
  Alternative: one new test per Done-when item for the new edge alone.
- **D6. The prose of §6** (the skill in its three copies, the reference, the
  audit) is updated in this row; nothing in PROCESS.md.
- **D7. The inherited re-parent consequence (§1, "Status movement")**:
  re-parenting an accepted child under a `Drafted` design row with no status
  move is the standing finding and an amendment, not a `parent-first` step
  refusal, exactly as re-pointing an accepted design row's `SR-Refs` is
  today. Confirm that "inherits unchanged" means this.
- **D8. The RESYNC entry** as §7 writes it.
