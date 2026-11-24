+++
id = "WI-1064"
title = "The parent-first rule reads a child design row's authored parent link, as it reads a design row's requirements"
workstream = "process"
specref = ""
sr_refs = ["SR-245", "SR-246"]
needs = ["WI-1027"]
buildtier = "medium"
planmode = "single"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Built on the maintenance branch `maint/wi-1064`, cut from `refactor_again` at
`c7d6bd6f4`, with the commit hooks on, under the plan
[plan.md](../../../plans/WI-1064/plan.md) (`76f388527`) and the coordinator's
go-ahead, which confirmed D1 to D8 and ruled on D3 and D7 (both below). Not
merged with trunk (`f78cb0a57`, WI-1067's rows): the coordinator merges at the
end. The specref (WI-1027's spec) is cleared at close.

- `76f388527`: the plan.
- `9ed8a5268`: the edge, the tests, the rows, the regenerated evidence and
  views, the prose and the RESYNC entry.
- The close-out commit after it: this Deliverable, the move to `complete/`
  and the log fragment.

**The edge** (Done-when 1). `kitlib.spine.PARENT_EDGES` now maps each child
tier to its `(cell, parent tiers)` pairs, and the design tier has two:
`("SR-Refs", ("SR",))` as before and `("Parent", ("LLR",))`, new.
`parent_first_findings` asks each accepted row each of its tier's pairs
through the unchanged `_unaccepted_parents`, so the output keeps its order
(child tiers SR, LLR, TC; rows in registry order; a design row's `SR-Refs`
findings before its `Parent` finding). An accepted child design row under a
parent design row that does not claim acceptance is one entry, worded by the
unchanged `parent_first_line`: `LLR-002 (Accepted) is accepted under LLR-001
(Drafted), which is not: accept LLR-001 in its own acceptance act, or return
LLR-002 to Drafted`. It inherits, unchanged:
- *the classification*: the shared acceptance predicate on the child side,
  and on the parent side a declared row that does not claim acceptance, a
  missing status reading `no status`;
- *the exclusions*: the edge's parent tier is the design tier alone, so a
  `Parent` naming an SR, an id no row declares or a `-000` row is not judged
  (each is already the orphan rules' finding), and a `-000` child is skipped;
- *the status-movement conditions*: the commit judgement refuses only where
  the child's or the parent's status moved against some parent tree. So, as
  the coordinator ruled on D7, re-parenting an accepted child under a
  `Drafted` design row with no status move is not the `parent-first` step's
  to refuse: the hook's `registry-integrity` step refuses that commit with
  the standing finding, exactly as it refuses re-pointing an accepted design
  row's `SR-Refs` at a `Drafted` requirement today, and the re-parent is an
  amendment of the row, since `Parent` is accepted text.

Every route that judges the existing edges reaches the new one through that
one table, with no change of its own (D2), each confirmed by reading:
- the standing integrity check (`trace.integrity_sweep`, run by
  `trace.py --strict-integrity` and `--strict`, the hook's
  `registry-integrity` step, every stage's checks, CI and the slot's landing
  checks), over rows the carrier reads with their `Parent` cell;
- the commit hook's staged check (`check.py --parent-first` ->
  `staged_parent_first_lines` -> `parent_first_lines`), over
  `parent_first_tiers`;
- a supported lane commit's admission (IF-308): the merge slot's walk over
  `LANE_COMMIT_RIDERS`, whose third rider is `commit_parent_first_lines`;
- the derived act's waiting flips (`adjudicate_act._findings`, over
  `parent_first_tiers`), whose fixpoint keys on the rule's findings, so a
  child design row waits on a parent design row the act leaves unaccepted,
  and a grandchild under a waiting child waits too. The pin that the act
  restates no edge now forbids `"Parent"` in its source as well.

No other route judges a parent edge: every module naming the rule is one of
the four, `held_status` (the fourth lane rider) judges rungs, and a squash's
staged tree is judged like any other.

**The coverage bound** (Done-when 2). The promise reaches registries as the
supported workflows and the kit's own routes write them (the requirement
tree's `parent` cell, the acceptance acts, lane commits through the slot). A
registry or record a person hand-edits past a refusing hook is outside it, as
PROCESS.md §6, "Review threat model", rules.

**The tests** (Done-when 3), each red first against the unchanged rule
unless marked a characterization:
- the standing finding: `test_trace_rules.py::test_an_accepted_child_design_row_under_a_drafted_parent_reds_strict_integrity`
  (TC-396): the minimal scaffold with a `Parent` column, a `Drafted`
  top-level row and an `Accepted` child; `trace.py --strict-integrity` exits
  1 with exactly one parent-first line;
- the staged refusal: `test_parent_first_git.py::test_staging_an_accepted_child_under_a_drafted_parent_is_refused[LLR-LLR]`
  (TC-397), the new pair in `PAIRS`;
- the lane commit's refusal: `test_parent_first_git.py::test_a_no_verify_lane_commit_with_a_violation_is_refused_at_the_slot`,
  now over every edge (D5; TC-397);
- a simultaneous parent-and-child acceptance passing:
  `test_parent_first_git.py::test_an_act_accepting_parent_and_child_together_passes`,
  now over every edge (D5; TC-397), a characterization: it passes before the
  change too, and its witness is a judgement that read the parent's status
  from the parent tree, which refuses it;
- a derived act naming such a child as waiting: `test_adjudicate_act.py::test_a_child_design_row_waits_on_its_returned_parent_design_row`
  (untagged, D4): LLR-002 listed, LLR-004 named `waiting on LLR-003
  (Drafted)`, and the listed act, taken, passes the commit judgement;
- the D7 re-parent: `test_parent_first_git.py::test_re_pointing_an_accepted_design_row_at_a_drafted_parent_is_refused_as_standing`
  (TC-396, TC-397), over `SR-Refs` and `Parent`: after a control in which
  both steps pass, `check.py --run-steps parent-first,registry-integrity` on
  the re-pointed tree reads `parent-first` PASS and `registry-integrity`
  FAIL, naming the standing case. No existing test covered the `SR-Refs`
  case, so the test is new and covers both;
- in process, in `test_parent_first.py`:
  `test_an_accepted_child_under_an_unaccepted_parent_is_found[LLR-LLR]` and
  `test_a_parent_cell_is_judged_only_against_declared_design_rows` (TC-396:
  the one real case beside a `Parent` naming a `Drafted` SR, an undeclared
  id, the `-000` row and a child of a `Founded` parent), and
  `test_a_child_design_row_is_refused_at_the_commit_only_where_a_status_moved`
  (TC-397, the staged route's in-process pin).

The builders gained `ref_column` (a child LLR's design-row parents go in
`Parent`, or `parent = "..."` in TOML), and a row naming no parent now
leaves its refs key out, as the carrier asks of an unset cell (the full
loader refuses an explicit empty list; the readers treat both alike).

**Red before the code** (the eight new-edge cases, run against the unchanged
rule; every other case run passed): `8 failed, 55 passed in 22.20s` over
`test_parent_first.py`, `test_parent_first_git.py`, the new case of
`test_trace_rules.py` and the new case and the strengthened pin of
`test_adjudicate_act.py`, each failing at its own assertion:
  <!-- fig: cmd="python -m pytest -q -n 8 tests/test_parent_first.py tests/test_parent_first_git.py <the two new cases>" rev="76f388527 with the tests written, before the rule's change" -->
- `test_parent_first.py` `[LLR-LLR]`, the parent-cell case and the
  in-process commit case: each `assert [] == [...]`;
- the staged `[LLR-LLR]`: exit 0 with `ok    parent-first  no staged status
  leaves an accepted row under an unaccepted parent`;
- the slot `[LLR-LLR]`: refused, but only by the held-rung rider (this
  fixture's default dial holds the design rung), with no parent-first line,
  since the walk reports the first rider with lines and the parent-first
  rider, third, had none; on a released rung nothing refused it;
- the D7 `[Parent]` case: both steps PASS on the re-parented tree (exit 0);
  its `[SR-Refs]` case passed before and after;
- the standing case: exit 0, `integrity=0`;
- the derived act: LLR-004 listed for flipping beside LLR-002, no `waiting`.

**Rows** (Done-when 4). No row written and no id minted. Amended, text only,
each `Accepted` and each owed an amendment act for automated adjudication:
- **SR-245**, `Requirement` and `AcceptanceCriteria`: an LLR "cites a
  declared SR parent or names a declared parent LLR in its parent cell"
  (and "or naming such a declared parent LLR in its parent cell" in the
  criteria). Title, rationale and coincident unchanged.
- **LLR-357**, `Detail`: "It classifies only declared SN-to-SR, SR-to-LLR,
  LLR-to-LLR, and SR-or-LLR-to-TC references in supplied spine rows, an
  LLR-to-LLR reference being the parent LLR that a child LLR's parent cell
  names."
- **TC-396**, `Method` (the child-LLR-to-parent-LLR edge, the parent cell
  naming a requirement among the exclusions, the child under a Drafted
  parent through the strict integrity finding, and the inherited
  "strict-integrity" spelling of the flag scrubbed to "strict integrity")
  and `Expected` (the child LLR under its parent LLR included; a parent cell
  naming a requirement produces none).

Each new clause is driven by a test its TC names; LLR-357 stays within
SR-245, and TC-396 within both. No routed traced change to an `Accepted`
row. TC-396's and TC-397's `Evidence` are regenerated from the tags
(traced, not routed: no act). No new or rewritten `Drafted` row.

**SR-246 and LLR-358, read and left unamended** (D3, as the coordinator
confirmed, against this item's naming of their amendments): neither states
an edge list. SR-246 refuses "an Accepted or Founded child under a declared
parent without either status" and LLR-358 returns "a parent-first finding",
so each takes its edges from the rule SR-245 and LLR-357 state and stays
true with the edge added; TC-397, which drives "each parent edge", is
unamended for the same reason, its new cases being cases of its existing
text. LLR-338, TC-368 and IF-308 are unchanged too.

**Prose** (D6): the `spine-authoring` skill (its three copies) says "an LLR
for every SR it cites and a child LLR for the parent LLR it names";
`docs/registry-machinery-reference.md` §4.1 and its `Parent` column row, and
`docs/enforcement-audit.md`'s row for the rule, name the edge. A RESYNC entry,
anchored `[since c7d6bd6f4]`, names `scripts/kitlib/spine.py` and the skill.

**Tests run:**
- The four touched modules after the change: `159 passed in 56.90s`.
  <!-- fig: cmd="python -m pytest -q -n 8 tests/test_parent_first.py tests/test_parent_first_git.py tests/test_trace_rules.py tests/test_adjudicate_act.py" rev="the tree committed as 9ed8a5268, before the commit" -->
- The rule-5 set, 50 modules: the 26 importing `kitlib.spine`, the 31
  `trace.py --tests-for` lists for it, the modules holding TC-396's,
  TC-397's and TC-368's tests (`test_parent_first`, `test_parent_first_git`,
  `test_trace_rules`, `test_adjudicate_act`, `test_coordinator_act`), for
  the skill edit `test_skills_sync`, `test_skills_index`, `test_prompts` and
  `test_adjudicate_brief`, and `test_import_layers`,
  `test_module_size_ratchet`, `test_complexity_ratchet` and
  `test_dogfood_sync`: `1 failed, 1957 passed, 2 skipped, 18 warnings in
  491.54s (0:08:11)`. The one failure,
  `test_snapshot_readers.py::test_a_lone_retirement_on_a_held_rung_is_refused_by_row`,
  is not this row's: it passes alone (`1 passed in 17.10s`), fails each
  time its module runs in parallel (`1 failed, 56 passed in 86.68s`), and
  fails the same way with this branch's changes stashed (`1 failed, 56
  passed in 103.01s`, at `76f388527`); its line names a held-rung claim on
  SR-001 where the case expects SR-002.
  <!-- fig: cmd="python -m pytest -q -n auto <the 50 modules>; python -m pytest -q -n 8 tests/test_snapshot_readers.py (changes stashed for the last)" rev="the tree committed as 9ed8a5268, before the commit; 76f388527 for the stashed run" -->
- `trace.py --root . --strict`: exit 0 (`orphans=0 integrity=0`);
  `check_trajectory.py --root . --strict`: exit 0 (`clean (1066 work
  item(s), 935 done (88%), 37 cancelled, graph acyclic)`);
  `scripts/check_resync.py`: `OK, 2 shipped path(s) changed; entry anchored
  at c7d6bd6f4...`. The build commit's hook: `check_complexity: OK - 168
  row(s) over 15, unchanged from baseline`; one non-gating readability
  warning, `flag-axis worsened tests/test_adjudicate_act.py: flag functions
  0 -> 1 (+1: _verdict(commit, bind))`, on a helper this row calls without
  either flag and does not change. No ratchet re-stamped.
- `run_menu.py smoke`, once at the end: exit 0, the strict lints first,
  then the tier `3878 passed, 3 skipped, 18 warnings in 184.71s (0:03:04)`
  (3881 cases against `max-tests = 3890`: no re-stamp); its budget line
  reads `CPU 715.3 s vs 540 s cpu-seconds; wall 185.4 s vs 600 s
  wall-seconds ... -> OVER`, warn-only by rule (the tier overrun WI-1039
  is filed for); `check_resync: OK, 2 shipped path(s) changed`.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="the close-out tree" -->
- `check_docs.py --root .` after the move: `OK - 3694 doc(s), 3834
  intra-repo link(s), 0 broken` (the plan link, relinked one level too
  deep by the move, set back by hand first).
  <!-- fig: cmd="python project-trajectory/scripts/check_docs.py --root ." rev="the close-out tree" -->
- The unfiltered suite was not run, as the brief directs.

**Review record.** Round 1 (2026-11-23, over `c7d6bd6f4..4d11e2e2b`; the
coordinator's brief): OpenAI Sol (low) `VERDICT: APPROVE findings=0` over
the whole diff; Gemini Hydrogen (low) `VERDICT: APPROVE findings=0` over
the prose, the rows and this record. No fix was owed. The builder's red in
`test_snapshot_readers.py` under `-n 8` does not reproduce on trunk: at
`f78cb0a57` the module gives `57 passed`, so it is a worktree's red, not
this row's (recorded at the merge, which runs the smoke tier on the merged
trunk).

## Context

Filed on trunk on 2026-11-23 by the queue drill's coordinator, from
WI-1027's plan (F-7, the specref), its second decision. F-7 adds an
authored `parent` link: a child design row names one parent design row and
carries no requirement link of its own. The parent-first rule (SR-245,
SR-246, LLR-357, LLR-358) states a closed list of edges: a requirement's
needs, a design row's requirements, a test case's verified rows. A child
design row's parent is not among them. So once F-7 lands, a child can be
accepted under a parent design row that stays `Drafted`, and neither the
standing integrity finding nor the commit hook's parent-first step reports
it. F-7 keeps that closed list unchanged on purpose, since its rows and
test case state the list. This row extends it.

The derived act's waiting flips (WI-1059) read the parent-first rule's own
findings, so they follow the new edge with no change of their own.

Critiqued 2026-11-23 (Sol and Hydrogen;
`docs/reviews/2026-11-23-scope-critiques/WI-1064.md`): `planmode` is
`single`, since the edge reaches three admission routes, and the edge holds
at each of them.

## Done-when

- [x] The parent-first rule treats a child design row's parent link as a
      declared parent edge: an accepted child under a parent design row
      that does not claim acceptance is one parent-first finding, with the
      same wording and remedy as the existing edges, at every route that
      judges the existing edges: the standing integrity check, the commit
      hook's staged check, and a supported lane commit's admission (the
      interface carrying the parent-first findings to a lane, IF-308). The
      new edge inherits the existing edges' classification, exclusions and
      status-movement conditions unchanged.
- [x] Coverage bound: the promise reaches registries as supported
      workflows and the kit's own routes write them; hand-edited kit-written
      state is outside it (PROCESS.md §6, "Review threat model").
- [x] A test shows each: the standing finding, the staged refusal, the
      lane commit's refusal, a simultaneous parent-and-child acceptance
      passing, and a derived act naming such a child as waiting.
- [x] SR-245's, SR-246's, LLR-357's and LLR-358's amendments (text only, no
      code names) and their test cases' are listed in the Deliverable as
      owed to adjudication.
