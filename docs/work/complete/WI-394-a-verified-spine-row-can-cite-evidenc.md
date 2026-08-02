+++
id = "WI-394"
title = "A Verified spine row can cite evidence that has NEVER EXISTED - nothing validates that a TC `Evidence` test-node id resolves. FOUND while closing WI-383, whose own commit b8c7cc21 repointed TC-091's Evidence and left a dead sibling entry standing: TC-091 still names tests/test_agent_loop_dispatch.py::test_unclassified_wi_fails_closed_without_stopping_others, a module DELETED 2026-07-29 by 31ad569d with the parallel dispatcher, while the row reads Automated=Yes Status=Verified and every gate is green. DRIVEN, not argued (WI-383 REVIEW-A round 1): an entirely invented citation tests/this_file_has_never_existed.py::test_entirely_invented passes trace.py --strict --no-placeholders --require-verified --strict-schema (rc=0, orphans=0 schema-findings=0, TC-091 still Verified), check_trajectory --strict (rc=0), check_doc_refs --strict (rc=0) and pytest tests/test_trace.py tests/test_registry_checks.py (70 passed). THE CLASS IS WIDER THAN Evidence, MEASURED: LLR-059's Module set to project-trajectory/scripts/this_module_has_never_existed.py WITH CodeSymbol set to entirely_invented_symbol passes trace --strict and check_trajectory --strict at rc=0 (and 113 tests across six registry/trace modules pass), and TestRefs set to (see TC-999) does the same. THE BOUNDARY IS CRISP AND IS NOT `traced cells are unchecked` - a CONTROL run proves it: TC-091's Verifies set to SR-999;LLR-999 fails trace.py at rc=1 with FINDING (orphan): TC TC-091 references unknown SR-999. A pointer into ANOTHER REGISTRY is joined and validated (Verifies, SR-Refs, Component); a pointer OUT of the registries into the code or test tree - Evidence, Module, CodeSymbol, TestRefs - is not checked at all. Module is read only as a join key among LLR rows (the IF ThisProject endpoint join, PB Refs), so a Module no file backs simply joins to nothing, warn-only. WHY IT MATTERS: those four cells are exactly the ones carrying the spine's claim to be GROUNDED IN THE CODE - Evidence is what answers `how do you know this is Verified`, Module/CodeSymbol are what a maintainer follows to the governed thing - and every other link in the chain is mechanized. It rots silently and by default: nothing in a deletion asks what cited the deleted file, and docs/okf republishes the dead citation as generated prose. THREE HONEST OPTIONS, AND A BUILDER MUST NOT PICK - the owner rules this, because the one thing that is definitely wrong today is that the current state IMPLIES A CHECK NOBODY PERFORMS. (a) BUILD THE RESOLVER so the cell means what it says; the cheap half is most of the value, since the FILE path is checkable with Path.exists() stdlib-only and catches this finding and every deletion-driven one like it, while only the ::node suffix needs pytest and CodeSymbol already has an oracle in the generated arch-map inventory that check_doc_refs' symbol tier reuses; surfaces = trace.py or check_trajectory.py gains a finding class, docs/enforcement-audit.md moves these rules from Prose/Reviewer to Harness, and the existing dead citations need triage before it can gate (warn-first, the WI-062 precedent of 561 findings before the untraced split and 22 after); cost to weigh is HIGHER than a new-check argument and is TWO things: a new check is the shape concurrency-v2.md section 0 warns about, AND check_doc_refs ALREADY DECIDED THE OTHER WAY ON PURPOSE - its is_path_shaped short-circuits on `::` before any extension or prefix rule, with a comment naming `the kit's sanctioned Evidence form` and citing false-positive control - so a full resolver must overturn a deliberate decision rather than fill an unconsidered gap, and must answer that decision's real question, which is what a citation to a test RENAMED BUT STILL PRESENT should cost a reader - that question is exactly what (a) buys and (c) declines to. The decision is not only commented but GUARDED BY A NAMED REGRESSION TEST, tests/test_check_doc_refs.py::test_node_ids_and_joined_lists_are_not_path_flagged. (b) RULE THAT THE CELL IS PROSE and stop implying otherwise; surfaces = the registry template header comments in project-trajectory/registries/, PROCESS.md/PROCESS_OPTIONS.md wherever Evidence is described, EXAMPLE.md, and docs/enforcement-audit.md recording the gap AS ACCEPTED with its reason; cost to weigh = Automated=Yes plus Status=Verified beside an unchecked evidence pointer is a strong implication to leave standing on purpose. (c) THE FILE HALF ONLY, named so it is not mistaken for (a): check that the FILE exists and rule the ::node selector prose. It closes the whole failure mode this row was found by - every dead citation here died because its FILE was deleted, not because a test was renamed - (c) DOES NOT DODGE (a)'s OBSTACLE, IT NARROWS IT - it RE-SCOPES the `::` guard rather than conceding it, and reds the same named regression test (a) would, so both options must amend a deliberate, guarded decision and ONLY THE SIZE DIFFERS - which is the whole argument for (c). TWO SITES, NOT ONE, and this is a budgeting trap: is_path_shaped is a PREDICATE that returns a bool and cannot hand a rewritten token back, while path_findings (check_doc_refs.py:264) re-derives clean from the ORIGINAL token and stats it, so relaxing the guard ALONE makes the tool stat the whole path::node string and call a live file missing - measured at 10 dangling, FOUR OF THEM FALSE. With both sites changed the run is 6 dangling, all true, zero false positives, core change +4/-2. The registry side still needs a reader, because the tool scans markdown and never the CSVs, and that plus the guard test is the remaining work. NOT IN SCOPE: repairing the individual dead citations, which is a consequence of whichever option is ruled and would hide the evidence this row is built on. RELATED BUT SEPARATE: TC-091's Description/Method and SR-094's AcceptanceCriteria still name the checkpoint classifier input WI-383 deleted - RATIFIED cells, and WI-390's program close (concurrency-v2.md section A9.1). SAFE AS ORDINARY WORK, NOT SPINE: Evidence is a TRACED cell under concurrency-v2.md section A5.1 (WI-380) - spine_cell_class('docs/test/test-cases.csv','Evidence') returns traced - so this row arms NO re-attest window, and the same holds for LLR Module, CodeSymbol and TestRefs; option (b) is different in that it edits process prose and template headers, which is a cost to weigh when the option is chosen rather than now."
workstream = "process"
buildtier = "medium"
safety_class = "ordinary"
+++

## Deliverable

Owner ruling R2 (docs/backlog-plan-2026-08-01.md, 2026-08-01) picked **option
(c)** — the FILE-EXISTENCE half only, the `::node` selector ruled PROSE — and
that is what shipped, in `check_doc_refs.py` (commit `WI-394: build the
Evidence file-existence check`):

- **The `::` guard re-scoped at both sites**, exactly as the ruling measured:
  `is_path_shaped` now strips the node selector and judges the FILE half like
  any path (the `;`/`,` joined-list exclusion survives untouched), and the
  stat-side strip rides the same two-site rule WI-396 established for line
  suffixes — via a shared `judge_token` helper after `check_dupes` red the
  copied classification chain. The guarded decision was amended, not deleted:
  the named regression test
  (`test_node_ids_and_joined_lists_are_not_path_flagged`) became
  `test_node_id_file_half_is_judged_and_joined_lists_stay_out_of_scope`, and
  the re-scoped rule is pinned both ways (a live file half passes; an invented
  citation warns by default and gates under `--strict`; `path-ok` quotations
  stay exempt; the selector half is asserted NEVER validated).
- **The registry tier** — the reader the markdown scan never had: the spine's
  four Evidence-class cells (TC `Evidence`; LLR `Module`/`CodeSymbol`/
  `TestRefs`) are walked as known joined lists, each token's file half checked
  with stdlib `Path.exists`, findings named by row id + column, `*-000`
  placeholder rows skipped, absent registries skipped cleanly. Same warn-first
  / `--strict` wiring as the rest of the tool (the WI-062 precedent).
- **The census, measured and triaged**: 13 dangling before, 0 after. The 6
  true registry findings: TC-076's three
  `tests/test_agent_loop_dualplan.py::*` nodes repointed to the same three
  nodes preserved verbatim in `tests/test_dual_plan_round.py` by 31ad569d;
  TC-091's dead sibling (`tests/test_agent_loop_dispatch.py::…`, this row's <!-- path-ok: the triaged dead citation, quoted as record -->
  original find) removed beside WI-383's live `test_schedule.py` evidence;
  LLR-096 + LLR-132 dropped the deleted `agent_dispatch.py` from their Module
  lists (their Detail prose is RATIFIED — WI-390's program close, untouched).
  4 markdown findings were this spec quoting its own driven evidence — marked
  `path-ok` with reasons; the invented files were never created. 3 findings
  pre-dated the branch (`docs/test/report.md`, red on trunk) — declared
  LIFECYCLE in `docs/declared-absences`, the candidate the prior lane's
  finding 1 (log 2026-08-01) had already named.
- **The honesty surfaces**: `docs/enforcement-audit.md` gains the row — file
  half **Harness**, `::node` selector an **accepted Prose gap** with its
  reason, so a renamed-but-present test node is never implied as covered.

Not done, per the ruling: no pytest/node-id resolver, no `CodeSymbol` symbol
oracle (option (a) declined); the RATIFIED Description/Method cells naming
deleted inputs stay with WI-390.

Verification: module suite 39 passed; smoke 578 passed / 6 skipped; full
suite 1802 passed / 10 skipped in 4:36; `check_doc_refs --root . --strict`
rc=0 with 0 dangling.
