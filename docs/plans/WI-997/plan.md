# WI-997 plan, revision 3: this repository's test files carry their test-case tags, and a strict finding holds tags and evidence cells equal

Planned against lane `C:/Projects/ai-template.wt/wi-997`, head `2633ea689` (base `cffb626c5`).

Read in full: the spec `docs/work/active/wi-997/WI-997-tag-this-repos-test-files.md`, its `specref` target (review-churn plan item 13), OI-127 and OI-129 in `docs/requirements/open-items.toml`, `docs/decisions/coordinator-2026-11-05.toml` D-001, WI-999, WI-1000 and WI-1001. Also read: SR-157, LLR-260, LLR-365, TC-404 to TC-409, IF-131, IF-263, CMP-006, `docs/runtime-flows.md`, the row-1 code in `gen_arch_map.py` and `trajectory_arch.py`, and `coordinator-cycle` with its recipes.

**How this was measured.** Everything marked measured ran at this head, in a throwaway clone under the scratch root, with nothing written to the lane. The clone took the repoints, the two moved cells, a prototype seed and a prototype check, and ran the full suite.

## What changed from revision 2

The critique's one finding, F1, is confirmed. A counted round always precedes the checkpoint (`coordinator-cycle` §3), and P8 opens after such a round, so P9's handoff reached the reviewers after the rounds and the gate it exists for.

One part of its remedy changes. It asks to move "the review brief" forward, but a brief moved forward still would not reach a reviewer. A round's brief is rendered by `review_brief.py review`, which has no slot for this, and the recipes forbid adding to it: "Never write a review brief by hand", and a handoff's builder notes "for the reviewers" stay out too. Revision 2's P9 was wrong on that as well. So the handoff becomes a committed file inside the reviewers' reading scope (decision 16).

- **New:** row P7a and commit C5a. They commit the seed's evidence and the tag sample after C5's final build checks and before the first round is rendered.
- **Changed:** P8 consumes that file, and P9 keeps only the log and the closing checks.
- **Updated to match:** the build table, the commit table, "Why some clauses span several rows", the checker's name in P3, and a closing line under the delta answer.

The rest stands, each measurement included: the commits since `2633ea689` are records (the plan, a session log and the critique).

## What changed from revision 1

Revision 1 was committed before OI-127 was ruled and was never critiqued. I re-checked each claim I kept.

- **Gone:** the stop section, P1's stop and the disposition routes. OI-127 ruled (b), revised, so D3 moves TC-165 and TC-166 out and the row does not stop for them.
- **New:** P2, the two moved cases, with the cell form confirmed by running the checks.
- **New:** a table naming which row states each new behaviour.
- **Renumbered:** the `D#` clauses moved, and every cite below is against the current list.
- **Corrected:**
  - Revision 1's `code_symbol` named only `tc_tag_findings` while the helper carried the `Implements:` tag. The crosscheck reads that as a mismatch, so the cell names both (P4).
  - Revision 1 had `EXAMPLE.md`'s TC-002 name the Rust file, but the Rust snippet tags only TC-001, which would read one finding. The snippet tags both (P7).
- **Now measured, not predicted:** the fixture the check turns red, the collected ids, the complexity rows, the check's 0 findings on the real tree, and the check's wall time.

## Measured, against the spec's figures

| Figure | Spec | Measured at this head | Note |
|---|---|---|---|
| Live TCs | 357 | 363 | All Approved |
| Evidence parts | about 2222 | 2311: 2303 under `tests/`, 8 outside | Before P2. The 8 are real CI, inspection, review and text records. Trunk's WI-982 and WI-983 added 21 node parts since revision 1 |
| File-only parts | 169 | 169, across 146 TCs | P2 removes two |
| Node parts | 2045 + 19 | 2134: 2056 distinct, 20 parametrized | |
| Method parts | 5 | **0** | No part uses `path::Class::name`. The rule still pins the form (P5) |
| Nodes naming no def | 19 | **4** through `kitlib.spine.evidence_items` | See below |
| Test files holding a part | 219 | 217, and **216** after P2 | All `test_*.py`, so every module-tag target is a read position |

**The 19 are 4 stale nodes plus 15 cells a `;`-only split misreads.** I replayed a `;`-only split at this head and got exactly 19. Fifteen of them are cells that separate items by whitespace: TC-051, TC-056, TC-057, TC-102, TC-104, TC-105, TC-106, TC-113, TC-115, TC-117, TC-118, TC-119, TC-120, TC-121, TC-124. `evidence_items`, the reader the spec requires, reads each item correctly, and every item names a real def. OI-127's text records the same reading.

The 4 real ones. I confirmed each against history:

| TC | Stale part | Repoint to | Why it is the same case |
|---|---|---|---|
| TC-079 | `tests/test_traj_parse.py::test_asof_stamp_from_git_and_excluded_from_check` | `tests/test_gen_trajectory.py::test_asof_stamp_from_git_and_excluded_from_check` | Same test, same name, moved at `cde260dd0` |
| TC-079 | `tests/test_traj_parse.py::test_no_git_means_no_stamp_and_stays_deterministic` | `tests/test_gen_trajectory.py::test_no_git_means_no_stamp_and_stays_deterministic` | Same test, same name, moved at `cde260dd0` |
| TC-194 | `tests/test_gen_trajectory_pending.py::test_the_dashboard_still_answers_to_the_former_private_names` | `tests/test_gen_trajectory.py::test_facade_reexports_pending_compatibility_names` | Moved and renamed at `cde260dd0`, with the same loop over the three former names TC-194's method lists. TC-194 keeps Smoke evidence: the tier test stayed green in the clone |
| TC-333 | `tests/test_plan_pass.py::test_the_shipped_planner_template_names_no_skill_and_no_row_of_this_repo` | `tests/test_plan_pass.py::test_the_shipped_planner_template_names_the_architecture_skill_by_its_agent_paths_and_no_row_of_this_repo` | Renamed and widened at `489678a52`, in the same place |

None of the four old names appears in any TC's `method` or `expected`, so these are traced-only changes.

**The prototype seed over the real tree, after P1 and P2:**

- 216 files and 2172 tags: 1509 new test docstrings and 663 extended (21 one-line, 513 with the closing quotes after text, 129 with them on their own line). 116 files take a module tag, and none needs a new module docstring. About 3370 lines added.
- No file carries a BOM or CRLF, no docstring is raw or single-quoted, and no target is a one-line def.
- Each changed file's AST, docstrings stripped, is unchanged in all 216.
- `pytest --collect-only`: 7720 ids before and after, byte-identical once sorted.
- `read_test_tags` reports 0 findings, and tags equal parts for every live TC: 0 missing, 0 extra.
- `check_complexity.py`: "183 row(s) over 15, unchanged from baseline". `ruff check tests` and `ruff format --check tests` are clean, 3 new docstrings needing the blank-line rule in P3.
- `check_resync.py` is OK at the seed commit: no shipped path changed.
- The longest tag is 90 characters, 10 ids. 2074 of 2172 tags hold one id.

**The prototype check over that tree:**

- `check_trajectory.py --strict` is clean: 0 findings on the real tree. Its wall time is unchanged, 62 s against 63 s.
- A module tag `Implements: TC-165` added to `tests/test_bootstrap.py` reads `TC-165: tag without evidence: tests/test_bootstrap.py`. So once the check lands, D3's "neither file takes a tag" holds mechanically.
- `trajectory_arch.py` goes from 971 to 995 SLOC, 5 under the 1000 threshold.
- **The full suite: 13 failed, 7674 passed, 33 skipped, in 26 minutes.** All 13 are accounted for:
  - **8 are the one fixture the check reads**, `conftest.DEMO_TEST`, as `TC-001: evidence without a tag: tests/test_demo.py::test_add_sr001`. They are three in `tests/test_check_harness.py`, two in `tests/test_integrate_unload.py`, and one each in `tests/test_dispatch.py`, `tests/test_integrate_station.py` and `tests/test_pre_commit_hook.py`. With the fixture's test tagged, all 8 passed.
  - **4 are in `tests/test_session_adapters.py`.** They fail at the lane's own head in the clone too: the clone has no commit hooks, so `HooksOffRefused`.
  - **1 is `test_this_repo_s_committed_stage_is_current`.** It asserts the trunk-only `docs/stage` off a claimed branch, and the clone's branch was not claimed (the recipes' wi-921 D-020 note).
  - So in the lane, with hooks on and the branch claimed, the expected red set after P5's fixture tag is empty.

## The cell form for the two moved cases

D3 orders the build to confirm the form, so I ran each candidate through every reader of the cell. The readers are `trace.py`'s schema rule, `check_doc_refs.py`'s registry tier, `kitlib.spine.tier_findings`, the carrier and the spec's equality rule.

| Form | `trace.py --strict`, `--strict-integrity --strict-schema` | `check_trajectory.py --strict`, `--staged` | `check_docs`, `check_doc_refs` | `tests/test_evidence_join.py` | Read by `evidence_items` as |
|---|---|---|---|---|---|
| `evidence = "(owed by WI-1000)"` | exit 0, schema-findings 1, the baseline | exit 0 | exit 0 | 16 passed; advisory "TC-165: tier Full, but none of its evidence is slow (no evidence)" | no part |
| `evidence = "WI-1000"` | exit 0, same | exit 0 | exit 0 | 16 passed; same advisory naming `WI-1000` as a path | a part, path `WI-1000` |
| `evidence = ""` | **exit 1**: the carrier refuses an explicit empty | **exit 1** under `--strict`; `--staged` exit 0 | `check_docs` exit 0, `check_doc_refs` exit 1 | 2 failed | refused |
| key absent | schema-findings 1 to 3, one per row, the "cites no Evidence" finding | not run | not run | not run | no part |

**Chosen: `(owed by WI-1000)` and `(owed by WI-999)`.**

- LLR-260 already states "a parenthetical note dropped", so the cell names its debt row in the one form the reader defines as not a path.
- A bare id reads as a path part, which is the false reading D2 exists to remove. It would pass only by sitting outside the tests root.
- The cost is the same for both forms: two new warn-only tier advisories on TC-165 and TC-166, since `tests/test_bootstrap.py` and `tests/test_components_registry.py` are slow and the new cells name no test. "No evidence" is true, and it is the debt showing. The tier test warns and does not fail.

The cell does not gain `tests/test_profile.py`, though that test drives TC-165's scaffold half. D3 says the cell names its debt row, and a test part would read TC-165 as covered for WI-995. WI-1000's Done-when owns it.

## Architectural-delta answer

DELTA: within

I followed `.claude/skills/architecture-decomposition/SKILL.md`. Each step's result:

1. **Mode classes (A2).** None added. The comparison is a pure function of what it reads and keeps no state. `docs/runtime-flows.md` names none of these modules, so no flow changes.
2. **Value domains (A3, A6).** Two values added to the finding domain: `evidence without a tag` and `tag without evidence`. IF-263's `data` cell records them in P4. IF-131 is unchanged, since `read_test_tags` keeps its signature and return.
3. **Output-on-input dependencies (A4).**

   | Output | Inputs today | Input added |
   |---|---|---|
   | `check_trajectory` WARN/ERROR lines and exit code | registries incl. TC rows, work specs, source AST, the files under `[paths] tests` | none as a source; within the TC rows, the `evidence` cell now joins the tag read |
   | `trace.py --tests-for`, tier findings | TC `evidence` cells | none |

4. **Descent (A8).** Requirement descent: one new LLR under SR-157 (P4). Component descent: `trajectory_arch` already imports `kitlib.spine` as `_kitspine`, no interface row declares that shared-package edge, and both sit in CMP-006. So there is no new boundary, no sub-component and no edit to `docs/requirements/components.toml`.

The spec's S5 answer holds. P4 carries the interface and LLR edits and P6 the code and its contract body. It needs no refactor.

P7a changes none of the four answers: its file is the output of unshipped tooling, and no shipped code reads it.

## Which row states each new behaviour

A test case states only what its rows state, so each behaviour below has its sentence in a named row before a TC method may claim it. "LLR-new" is the one LLR of P4.

| Behaviour | Stated by | Verified by | Test (P5) |
|---|---|---|---|
| Two findings, each naming case and node | LLR-new; IF-263 `data` | TC-a | `test_evidence_without_a_tag_is_named`, `test_a_tag_without_evidence_is_named` |
| WARN plain, ERROR under strict, gating from `DevStg-Impl`, warning below it in a new project | LLR-new | TC-a | the two above; `test_the_equality_check_on_a_bootstrapped_scaffold` |
| A Drafted case is judged | LLR-new | TC-a | `test_a_draft_tc_is_judged` |
| A `[case]` is dropped, so a part matches its test's tag | LLR-new | TC-b | `test_a_parametrized_part_matches_its_tests_tag` |
| A file part binds to a file-level tag, not a test's tag | LLR-new | TC-b | `test_a_file_only_part_matches_a_module_tag_and_not_a_tests_tag` |
| `path::Class::name` is kept whole | LLR-new | TC-b | `test_a_class_method_part_matches_its_tag` |
| A test part in a file read at file level is two differences | LLR-new, beside LLR-365's "declarations are read at file level" | TC-b | `test_a_non_python_node_part_reads_both_findings` |
| The cell is read as its other readers read it: both separators | LLR-new, pointing at the reading LLR-260 states | TC-b | `test_a_whitespace_separated_cell_reads_as_its_items` |
| A cell holding only a note has no part, so a tag on it is a finding | LLR-new, pointing at LLR-260's "a parenthetical note dropped" | TC-c | `test_a_note_only_cell_has_no_part_and_a_tag_on_it_is_a_finding` |
| A part outside the tests root is outside the rule | LLR-new | TC-c | `test_a_part_outside_the_tests_root_is_ignored` |
| Vacuous with no tests root or no registry | LLR-new | TC-c | `test_the_equality_check_is_vacuous_with_no_tests_root_or_no_registry` |
| An unreadable file adds no finding here | LLR-new; row 1's finding stays LLR-365's | TC-c | `test_an_unreadable_file_adds_no_equality_finding` |
| The bound | LLR-new's closing sentence | none: the outside set is stated, not tested | |

**Stated by no row, on purpose:**

- The seed script is unshipped tooling. Its result is pinned by its equivalence evidence and the log.
- The lane routine and the RESYNC entry are text.
- The retirement is a comment.
- The TC-165 and TC-166 cell form is a traced cell, recorded in the decisions.

No TC method mentions any of these, because a sitting returns a method sentence no verified row states (recipes, wi-918 sitting 003).

## Decisions the spec leaves to the build

The critic should check these first.

1. **The 15 whitespace cells are left alone.** They name real defs and the required reader reads them, so nothing needs repointing, and normalizing separators would touch 15 Approved rows for no behaviour. D2's "each of the 19" is met by four repoints and one decisions entry listing the 15 as read correctly, which is OI-127's own account. P5's whitespace test keeps a hand-rolled split from creeping in.
2. **One read, inside `tc_tag_findings`.** It already reads the rows and calls `read_test_tags`. It gains one call to a new private helper, `_tag_evidence_findings(rows, tags, refused, tests_dir)`, taking those values. So the tests are read once, `check_trajectory.py`'s code does not change (its promotable loop already holds the call, so its ratchet row does not move), and the retirement is one helper and one call.
3. **Vacuity needs its own guard.** Row 1 is vacuous over a missing tests root because walking nothing yields nothing. Here it would yield one finding per part. So the helper runs only when `(root / tests_dir).is_dir()`.
4. **"A file row 1's reader refuses" means `unreadable`.** That is the one shape that refuses a file: no tags are read, so every part naming it would be a false finding. The other three refuse a tag. A malformed tag on a test gives row 1's finding and an evidence-without-a-tag finding, both true, and one fix clears both. Skipping every file with any finding would drop real differences from a file with one bad line.
5. **Prefix.** `Path(tests_dir.replace("\\", "/")).as_posix().rstrip("/") + "/"`, so `tests`, `tests/` and `./tests` compare equal to the repo-relative parts. `module_tests`' own prefix does not handle `./`, and is left alone.
6. **Reduction.** A part becomes `path`, or `path + "::" + node.split("[", 1)[0]`. The cell is read by `_kitspine.evidence_items` only.
7. **A part with no tag form reads a finding, and the RESYNC entry says so.** The reader cannot give a tag for a `path::node` in a non-Python file, a file type it does not read, or a helper module, whose docstrings are refused as misplaced. The spec's rule stands, and the fix is the cell naming a test file, whole where the file is read at file level. P5 pins the non-Python case.
8. **Finding text.** `<TC>: evidence without a tag: <node>` and `<TC>: tag without evidence: <node>`, sorted by TC then node, naming the row and the node as SR-157 asks.
9. **The migration runs before the spine set, against Intent's usual first step.** Run after the new rows, the seed would meet evidence naming tests that do not exist yet. Run first, its refusal of a node naming no def stays absolute, with no skip list. It adds no behaviour, so the tests-first order is untouched.
10. **The seed script's home is `docs/plans/WI-997/seed_tags.py`.** Outside `project-trajectory/`, so it does not ship, which `check_resync.py` confirms. It is committed because the reviewers read it and a scratch root is lost between legs. P6's full suite shows nothing in the repository trips on it.
11. **The seed is idempotent and is re-run after every rebase.** A tag already present is left alone, so a re-run adds only what trunk brought, and the checker re-runs against that commit's parent. A conflict in the seed commit is resolved by taking trunk's file and re-running.
12. **The demo fixture takes its tag in P5.** Measured above: `DEMO_TEST`'s `test_add_sr001` is the only fixture the check reddened. The tag is one line inside a fixture string, which row 1 does not read.
13. **Text that becomes false changes with the check.** The spec does not list these, but each would contradict the code:
    - `PROCESS.md` §3, "an untagged test is no finding";
    - `check_trajectory.py`'s module docstring, "an untagged file is no finding";
    - `docs/registry-machinery-reference.md` §5, "tags and the `Evidence` cell are not compared";
    - `docs/enforcement-audit.md`'s WI-994 row;
    - `EXAMPLE.md`: TC-001 and TC-002 name a Python node over a Rust test file tagged only for TC-001. They read findings under this rule, so both cells name `tests/test_export.rs` whole and the snippet's tag reads `// Implements: TC-001, TC-002`. This closes WI-994 D-007's follow-up.

    WI-994's RESYNC entry stays as written, because it describes that entry's point in history.
14. **RESYNC anchor.** D9's "anchored at the trunk commit carrying the check" is the pack's convention: `[since <merge-base>]`, then the "Anchored at the preceding commit" line, as `check_resync.py` requires. It is re-anchored on a rebase. The entry classes PROCESS text by §2.2 (WI-994 D-007 records that row 1's entry got this wrong).
15. **Row text.** As for LLR-365, "no code named" applies to `title`, `detail`, `rationale` and the TC rows' prose. `module` and `code_symbol` stay, for the CodeSymbol crosscheck.
16. **D12's handoff is a committed file, never brief text.** Three facts fix its form:
    - **The brief takes nothing.** It is rendered, and "a judge's brief carries no claim of the judged party" (recipes, "A review round").
    - **Where it can live.** The reading scope is the range's diff. It always leaves out `docs/log.d` and `docs/reviews`, and in convergence stance, which the gate runs in, `docs/decisions` too. `docs/plans/WI-997/` stays inside it in both stances, so that folder holds the handoff, and the log and the decisions cannot.
    - **What it costs.** `docs/plans/` is not a record path (`RECORD_PREFIXES` in `kitlib/verdict.py`), so the commit goes through `attest`, or the render refuses the tip. `pass.toml` binds `plan.md`'s bytes, so the new file leaves the pass standing.

    The file holds the checker's output and no prose of the builder's. A reviewer re-runs the command it prints and compares, so what it reads is evidence it can reproduce and not a claim it must trust.

## Build table

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The stale parts: repoint four nodes and record the fifteen cells | D2; SR-157; TC-079; TC-194; TC-333 | no interface: evidence cells only | |
| P2 | The two moved cases: confirm the cell form, then TC-165 and TC-166 name WI-1000 and WI-999 | D3; SR-157; TC-165; TC-166 | no interface: evidence cells only | P1 |
| P3 | The seed: every evidence part tagged by a scripted edit, with its equivalence evidence | D1; D7; D11; SR-157 | IF-131 | P2 |
| P4 | The spine set on reserved ids: one LLR, three TCs with their evidence cells, the IF-263 data edit | D8; D11; SR-157 | IF-263 | P3 |
| P5 | The tests alone under strict xfail marks, tagged, with the demo fixture's tag | D5; D11; SR-157; TC-409 | IF-263 | P4 |
| P6 | The check: the helper, its header comment, the contract bodies, marks removed | D4; D7; D10; SR-157; TC-037; TC-075; TC-077; TC-100; TC-409 | IF-131; IF-263 | P5 |
| P7 | The RESYNC entry, the lane routine in the recipes, one home for the rule, with byte stamps and the skill sync | D6; D7; D9; SR-157 | no interface: documentation only | P6 |
| P7a | The review handoff: the seed's evidence and a seeded tag sample, committed before the first round is rendered | D1; D12; F1; SR-157 | IF-131 | P7 |
| P8 | Reconcile the set against settled code, close its edges, take the in-lane adjudication, anchor the registry, with every round and the gate reading P7a's file | D2; D3; D8; D12; F1; SR-157 | IF-263 | P6; P7a |
| P9 | The log and the closing checks | D1; D4; SR-157 | IF-131; IF-263 | P7; P8 |

Excludes: TC-001; TC-002; TC-003; TC-004; TC-005; TC-126; TC-127; TC-128; TC-174; TC-193; TC-197; TC-255; TC-270; TC-273; TC-275 — they verify SR-157's spine-row rules in `trace.py`, `trace_text.py`, `kitlib/spine.py`, `coherence.py` and `absolute_terms.py`; this row changes none of those modules, and their tests only gain tags, which P3's equivalence evidence covers.
Excludes: TC-086 — it verifies the critique vocabulary and closure ratchet in the `--staged` branch, which returns before this check, so its path is unchanged.
Excludes: TC-155 — it verifies the queue-overlap pre-filter, a separate rule that reads neither test files nor this finding.
Excludes: TC-404; TC-405; TC-406; TC-407; TC-408 — they verify the tag reader, whose code and return this row leave unchanged; TC-409, the surface, is named by P5 and P6.

**Why some clauses span several rows.**

- D1: P3 delivers the tags, P7a puts their evidence before the reviewers, and P9 states the result in the log.
- D2 and D3: P1 and P2 edit the cells, and P8's act anchors them.
- D4: P6 delivers the check, and P9 shows it landing at 0 findings.
- D7: each row that could move a size carries its own stamp, which is the rule itself.
- D8: P4 authors the rows, and P8 reconciles them and takes the adjudication.
- D11: P4 states the bound, and P3 and P5 hold to it and drive it.
- D12: P7a supplies what the reviewers judge through, and P8's rounds and gate read it.

## Commits and what each one owes the bar

Each row is whole inside one commit, and a row moving a stamped size carries that stamp. Python changes commit through `integrate.py attest --bar review`, with `--tests tests/test_trajectory_arch.py tests/test_trajectory.py tests/test_evidence_join.py` from C4. The bar runs both strict lints, so `check_trajectory.py --strict` reads every tag from C2 on.

| Commit | Rows | Shipped file | Stamps | Why the bar is green here |
|---|---|---|---|---|
| C1 | P1, P2 | none | none | `evidence` is a traced cell, silent by ruling and owing no sitting. The clone committed both edits, and both strict lints exited 0 |
| C2 | P3 | none | none measured | Docstrings only, so SLOC, the smoke count and the collected ids hold. Every tag names a live TC, so row 1's check reads clean. `check_resync.py` measured OK |
| C3 | P4 | none | none | Rows stay `Drafted` on reserved ids. Evidence naming tests that do not exist yet passes while the check is absent: the file half resolves, and the node half is prose to `check_doc_refs` |
| C4 | P5 | none | none | `test_trajectory_arch` is in `SLOW_MODULES`, so the smoke count holds, and `attest --tests` reports the red cases `xfailed`. Their tags name C3's rows, so they are live |
| C5 | P6, P7 | `trajectory_arch.py`, `check_trajectory.py`, `RESYNC_PACK.md`, `PROCESS.md`, `EXAMPLE.md`, the recipes | byte rows, skill sync | The check turns on over a tree already equal. The entry is in the same commit, so `check_resync.py` passes. **The full suite runs here once, in the foreground** |
| C5a | P7a | none | none | It adds one file under `docs/plans/WI-997/` and changes no test or registry. That folder is not a record path, so it commits through `attest` with C5's `--tests`, and it is the tip the first round renders at |
| C6 | P8 | none unless a return moves code | any count a return moves | Row text, verdicts and acts, as the cycle's checkpoint orders them |
| C7 | P9 | none | none | Records only |

P6 and P7 share a commit because `check_resync.py` refuses a shipped change with no entry (measured at the prototype helper), and the entry states findings only P6 delivers. Review rounds sit between C5a and C6, so the first round already has the handoff, and each fix keeps the stamp rule and D6's own rule. Trunk moving under the lane triggers decision 11's re-run, a RESYNC re-anchor and P7a's refresh.

## The steps

### P1. The stale parts

- Edit the four parts in `docs/test/test-cases.toml` by the table above, byte-exact, through a guarded replace that asserts each old string occurs once.
- Record in `docs/decisions/wi-997.toml`: one entry per repoint with its evidence (the commit that moved it), and one entry listing the 15 cells as read correctly and left alone, citing OI-127.

No test added: a traced cell adds no behaviour. Its mechanical pin is P3's refusal of a node naming no def, which fails before this step on exactly these four nodes, and then P6's check.

### P2. The two moved cases

1. **Confirm the form first, at the build's own head.** Make the two cell edits uncommitted, then run `trace.py --strict`, `trace.py --strict-integrity --strict-schema`, `check_trajectory.py --strict`, `check_docs.py --root . --stale`, `check_doc_refs.py` and `pytest tests/test_evidence_join.py`.
2. Record the commands and their results in `docs/decisions/wi-997.toml`, with why the parenthetical beat the bare id, which D3 orders.
3. The edits: `evidence = "(owed by WI-1000)"` on TC-165 and `evidence = "(owed by WI-999)"` on TC-166, through the same guarded replace.

**If trunk moved a check under the parenthetical,** the bare id is the second form measured passing. Record the switch; the row does not stop for these cases, by D3. P5's note test then changes with it.

No tag goes on `tests/test_bootstrap.py` or `tests/test_components_registry.py` for either case, and the seed cannot write one, since the cells now hold no part. No other TC cell changes, and `method`, `expected` and `automated` stay: OI-127 moved the cases, and WI-999 and WI-1000 own them under OI-129.

Red before it: the explicit empty form is refused by the carrier, the absent key is a schema finding, and P6's check reads a tag here as `tag without evidence`.

### P3. The seed

`docs/plans/WI-997/seed_tags.py`, stdlib only, reading cells through `kitlib.spine.evidence_items`. Its rules, each proven necessary by the prototype:

- A file-only part goes to the module docstring, a node part to that test's docstring, and a parametrized part to its test. Free-text mentions are never a source.
- Ids go on one line, sorted numerically, `Implements: TC-1, TC-2`. Row 1 refuses a wrapped list, and the longest is 90 characters.
- **A test with no docstring** takes `"""Implements: TC-1"""` as its first statement, above any leading comment. A blank line follows when the next statement is a def or class, for `ruff format` (3 cases).
- **A one-line docstring** is split: text, blank line, tag, closing quotes on their own line. Left on one line, the token follows prose and row 1 refuses it (21 cases).
- **Closing quotes after text** are moved to their own line the same way (513 cases). With closing quotes on their own line, the blank line and tag go above them (129 cases). The tag is always the last paragraph, so no prose can follow it as a false wrap.
- **`ast` column offsets are UTF-8 bytes,** so slice encoded lines. `tests/test_schedule.py` holds `§` and `—`.
- **Write bytes, never `write_text`,** which turns `\n` into CRLF on Windows.
- **It refuses and writes nothing** on a node naming no def, a non-test file, or a docstring form it does not handle (single-quoted, raw). So anything P1 missed cannot pass through it.
- It is idempotent (decision 11).

Equivalence evidence, by a separate checker, `docs/plans/WI-997/check_seed.py`, reading the parent commit through `git show`, kept beside the script (P7a states its command line):

1. Each changed file's `ast.dump`, docstrings stripped, equals its parent's.
2. `pytest --collect-only -q` before and after: the sorted node ids are identical, so the count is too.
3. The tags read by `read_test_tags` equal the reduced parts for every live TC, and the reader reports 0 findings.
4. `check_complexity.py` reports no row moved. It is never run with `--restamp` (D7).

No new test: the migration adds no behaviour, and P6's check is its durable guard. Row 1's bound holds for these tags (D11).

### P4. The spine set

Reserve first: `trace.py --reserve-ids WI-997 LLR=1,TC=3`. The lane's spine author writes the set once, with an arms map. Rows stay `Drafted`, component CMP-006, phase 6.

- **LLR**, under SR-157, in contract voice with no code named:
  - **Rule:** for each live test case, a Drafted one included, the test-file declarations naming it must equal the parts of its evidence cell under the declared tests root.
  - **Reading:** the cell is read as its other readers read it, so a separator changes nothing and a cell holding only a note has no part.
  - **Reduction:** a part is its file, or its file and test with any class kept and any parametrized case dropped.
  - **Binding:** a file part matches a file-level declaration only, and a test part a declaration on that test only, so a test part in a file read at file level is two differences.
  - **Outside:** a part outside the tests root is outside the rule.
  - **Findings:** a part no declaration covers is reported as evidence without a tag, and a declaration no part names as a tag without evidence, each naming the test case and the node.
  - **Absent or refused inputs:** a file refused as unreadable adds no finding here, and an absent tests root or test-case registry makes the check vacuous.
  - **Severity:** findings warn without strict checking and error under it; they gate from DevStg-Impl and remain warnings below that rung, including in a newly created project.
  - **Bound:** the `detail` closes with D11's bound in LLR-365's form.
  - **Cells:** `module` is `project-trajectory/scripts/trajectory_arch.py`, `code_symbol` is `tc_tag_findings/_tag_evidence_findings`, and `test_refs` names the three TCs.
- **Three TCs**, `verifies = ["SR-157", "LLR-<new>"]`, `tier = "Full"` because the module is in `SLOW_MODULES`, `evidence` naming P5's nodes:
  - TC-a, the two findings, their severity and the Drafted case, also citing IF-263;
  - TC-b, what matches: the reductions, the level a part binds to, and the cell's reading;
  - TC-c, what is outside: the tests root, vacuity, an unreadable file and a note-only cell.
- **`interfaces.toml`:** IF-263's `data` gains the tag and evidence-cell equality, inside the 160-character rule. TC-a cites the altered row, as `in-lane.md` requires.

No approved row's text becomes untrue, so no amendment is owed. LLR-171, LLR-172, TC-165 and TC-166 keep their text, and SR-157's acceptance already takes a new rule in by default.

### P5. The tests alone (`tests/test_trajectory_arch.py`)

Each takes `@pytest.mark.xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))` and drives `check_trajectory` through `run_traj`. Each has a half that is red before P6, since a strict mark fails on an unexpected pass. Each test's docstring carries its `Implements:` tag, and its node is in that TC's evidence cell (D6's rule, applied here first).

| Test | TC | Clause | Fails before the change because |
|---|---|---|---|
| `test_evidence_without_a_tag_is_named` (WARN and exit 0 plain, ERROR and exit 1 under `--strict`, naming TC and node; with and without work items) | a | D4; D5 | no finding |
| `test_a_tag_without_evidence_is_named` (same two levels) | a | D4; D5 | no finding |
| `test_a_draft_tc_is_judged` (a Drafted row with an untagged part reads a finding) | a | D5; D11 | no finding |
| `test_the_equality_check_on_a_bootstrapped_scaffold` (`scaffold`: an untagged part warns below `DevStg-Impl` and fails `check.py` at it; a tagged part is clean) | a | D4; D9; D11 | no finding |
| `test_a_parametrized_part_matches_its_tests_tag` (a `[case]` part on a tagged test is clean, one on an untagged test is a finding naming the reduced node) | b | D5 | the second half has no finding |
| `test_a_file_only_part_matches_a_module_tag_and_not_a_tests_tag` (module tag clean; a test's tag reads both findings) | b | D5 | no finding |
| `test_a_class_method_part_matches_its_tag` (`path::TestC::test_m` clean, a mismatched class a finding) | b | D5 | the second half has no finding |
| `test_a_whitespace_separated_cell_reads_as_its_items` (two items, one tagged: one finding, naming the untagged one) | b | D4 | no finding |
| `test_a_non_python_node_part_reads_both_findings` (decision 7; the file-only form clean) | b | D9 | no finding |
| `test_a_part_outside_the_tests_root_is_ignored` (a doc part, and a `tests/` part under `qa/tests`, beside an in-root untagged part that is a finding; a trailing-slash root) | c | D5 | the paired half has no finding |
| `test_the_equality_check_is_vacuous_with_no_tests_root_or_no_registry` (paired with the same tree holding both, which reads a finding) | c | D4 | the paired half has no finding |
| `test_an_unreadable_file_adds_no_equality_finding` (one `unreadable` finding for it; a readable file's untagged part in the same run is a finding) | c | D4 | the paired half has no finding |
| `test_a_note_only_cell_has_no_part_and_a_tag_on_it_is_a_finding` (an automated case whose cell is `(owed by WI-900)`: untagged is clean, tagged reads `tag without evidence`) | c | D3; D4 | the tagged half has no finding |

Whole values are compared, never indexed, because an `IndexError` is outside the mark's `raises`.

Also in this commit: `conftest.DEMO_TEST`'s `test_add_sr001` gains `"""Implements: TC-001"""` (decision 12). The row-1 tests in this module stayed green under the prototype check, so none changes.

### P6. The check (`trajectory_arch.py`)

- `_tag_evidence_findings(rows, tags, refused, tests_dir)` beside `tc_tag_findings`, as decisions 2 to 8 describe, with `Implements: SR-157, LLR-<new>` in its docstring.
- **Header comment (D10):** directly above the helper, it states that this check holds two homes of one fact equal, and that it retires when the evidence column is generated from the tags, at which point this helper and its one call are deleted. This row builds no retirement. Comments are outside SLOC.
- `tc_tag_findings`'s docstring, the Contract IF-263 body and `check_trajectory.py`'s rule paragraph state the rule.
- The marks go. Run by name: `tests/test_trajectory.py` for TC-037, TC-075, TC-077 and TC-100, since the strict loop's output grows, and `tests/test_trajectory_arch.py` for TC-409.
- Then the full suite, on the claimed branch with hooks on. Expected red set: none. Anything else is fixed in this commit.
- `check_trajectory.py --strict` on the real tree: 0 findings.

### P7. Text

- **`project-trajectory/RESYNC_PACK.md`:** an entry headed `### Test-file tags and evidence cells are held equal [since <merge-base>]`, with the pack's anchor line.
  - **What changed:** the rule and the two findings: a WARN, and an ERROR under `--strict`, so an adopter's gate refuses from `DevStg-Impl`.
  - **Retirement:** the check retires when the evidence column is generated.
  - **What to do:** seed your tags by the seed rule before re-syncing past this entry, because a repository with evidence cells and no tags reads one finding per part from `DevStg-Impl`. It states decision 7's cases. This is the forced migration OI-120 call 2 accepted, no second one.
  - **Closing:** no setting and no schema changes.
- **`project-trajectory/skills/coordinator-cycle/references/recipes.md`:** one bullet stating that a lane writes a test's tag and its evidence part in one commit, since the bar runs the check under `--strict`, and that a renamed test moves both. Then `bootstrap.py --dest . --sync`.
- **Decision 13's five files.** `PROCESS.md` §3 is the one statement of the rule; the others link or state only their own enforcer's facts.
- **Byte stamps.** Run `byte-budget-guard` before and after. `PROCESS.md` is watched, so its row takes the delta and reason in this commit, then the skill sync. `AGENTS.template.md` is not touched.

Red before it: `scripts/check_resync.py` exits 1 naming the shipped paths (measured), and `test_capped_doc_baselines_match_the_real_sizes` holds the stamp.

### P7a. The review handoff

This runs after C5's full suite and `check_trajectory.py --strict`, and before the first round is rendered.

- **The checker's command line:** `check_seed.py --seed-commit <sha> --scratch <dir> [--out <file>]`. `--seed-commit` repeats if decision 11's re-run adds a commit. It reads the commits through `git show`, collects in a throwaway clone under `--scratch`, and writes only there and to `--out`. So a reviewer runs it from its own scratch, and the launch's lane-change check stays quiet.
- **The file:** `docs/plans/WI-997/seed-evidence.txt`, the checker's output unedited, written as UTF-8 bytes. It holds:
  - the command line, with the seed commit in full and `<scratch>` printed literally, so two runs compare byte for byte;
  - P3's four results over the files the commit changes under the tests root: files changed and AST differences; the id count and the sha256 of the sorted ids, before and after; tags, reader findings, missing and extra; and `check_complexity.py`'s line;
  - the sample: 40 tags drawn by `random.Random(997).sample` from the seed's tags in sorted order across the files, each with its file, its target, its ids and the evidence parts it answers.
- **It depends on the seed commit alone.** Every result and the sample are taken at the seed commit and its parent, never the tip, so a fix round that leaves the seed commit in place leaves the file true. The tip's equality is the check's job, which D12 names beside the evidence and which the reviewers run.
- **Refresh.** A new seed commit, from a rebase or a fix to the script, re-runs the checker and commits the new file through `attest` before the next render.
- **Before every render,** a counted round's or the gate's, the coordinator runs the checker with `--out` under the scratch root and compares by `cmp`. A difference or a missing file holds the render until the refresh is committed.
- **The render stays plain.** Each reviewer's brief is `review_brief.py review --scope full` with nothing appended. The file reaches the reviewer through the diff, and D12 reaches it through the spec it maps coverage against. Both hold in convergence stance (decision 16).

No new test: unshipped tooling adds no behaviour. Red before it: the `cmp` fails on the missing file, so C5's tip goes to no round. The prototype ran these checks by hand in a clone. This command line is new, and P3's run right after C2 is its first use.

### P8. Reconcile, adjudicate, anchor

At the cycle's checkpoint, after a counted round with no BLOCKER or MAJOR. Every counted round reads P7a's file at a tip past C5a, and so does the gate over the checkpoint tip, each after P7a's `cmp`. That is how D12's reviewers judge the seed through its evidence, the check and the sample, not each edit. The spine author reconciles the set against settled code. The closure check then runs: parents, the arms map, TC to LLR and SR, IF-263's citation, `trace.py --strict` and `check_trajectory.py --strict`. One combined sitting judges the LLR and the TCs, with the IF edit named in the arms map, since an interface row has no kind token (D8).

**Anchoring D2 and D3's traced changes.** The first-approval act copies `docs/test/test-cases.toml` whole, so it carries P1's and P2's cells. The live registry and `docs/archive/last_approved/docs/test/test-cases.toml` are byte-equal at this head, and they must be again after the act: run `cmp`, because in the clone a committed traced-only change left both strict lints at exit 0, so no lane check prompts this. A traced change after the act re-anchors in the lane, as its last spine commit, by `intake.py snapshot --approves "docs/test/test-cases.toml=<ref>"`, the ref naming the sitting that last anchored it.

### P9. Log and closing checks

- `docs/log.d/WI-997-tag-this-repos-test-files.md` states D1's result: files, tags, the equivalence results and the collected count. It also states D2's and D3's outcomes and the re-measured figures above, including why 19 became 4.
- `run.cmd smoke`, whose `check_trajectory.py --strict` is D4's "lands green": 0 findings on the real tree, the new tests included.
- Trunk-only views regenerate at landing, not on the lane. The lane lands alone, and open lanes rebase onto it (S1).

## Budgets

- **`trajectory_arch.py`:** 971 SLOC against the 1000 threshold, unbaselined. The prototype helper and call added 24, so 995. **Past 1000 it is decomposed, never bumped:** the part reduction moves to `kitlib/spine.py` beside `evidence_items`.
- **`check_trajectory.py`:** docstring only, so its 1658 stamp holds. Docstrings are outside SLOC.
- **Test files (D7):** `check_complexity.py` reports no row moved after the prototype seed, since the sensor's `sloc` excludes docstrings. If a rebase changes that, the row alone is edited by hand in the commit that moves it, with its reason. `tests/conftest.py` gains no function.
- **Wall time:** measured unchanged, 62 s against 63 s for `check_trajectory.py --strict`.

## Coverage bound

D11's inside set is driven. A builder's or a re-sync's tags are the fixtures of P5, the scaffold case included. A TC row authored through a lane is the Drafted case. Row 1's bound holds for the tags, and the outside set is stated in the LLR (P4) and not tested.

## Found outside this row, not changed

- TC-165's scaffold half is driven by `tests/test_profile.py`'s permutation test, and after P2 no cell points there. WI-1000's Done-when restores it.
- P2 adds two warn-only tier advisories. They clear with WI-999 and WI-1000.
- The recipes say the strict lints catch a traced cell off its anchor. In the clone, on an unclaimed branch, both exited 0 on a committed traced-only change. It may be trunk-only; I did not trace it further, and P8's `cmp` does not depend on the answer.
- `module_tests`' prefix does not normalize a `./` tests root (decision 5).
- The spec's "5 a method" and "19 nodes" came from a reading that is not `evidence_items`. WI-995 should re-measure through the reader before quoting either.
