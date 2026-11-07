# WI-995 plan, revision 1: the review test set is derived from the row's SRs through the test-file tags

Planned against lane `C:/Projects/ai-template.wt/wi-995`, head `ee2b19b9e` (equal to its merge base with trunk).

Read in full: the spec `docs/work/active/wi-995/WI-995-review-test-set-derived.md`, its `specref` target (review-churn plan item 13), OI-120 and OI-125. Also read: SR-241, SR-156, SR-154 and SR-242 in `docs/requirements/system-requirements.toml`; every LLR under them in `docs/requirements/low-level-requirements.toml`; every TC verifying them in `docs/test/test-cases.toml`; IF-109, IF-110, IF-131, IF-154, IF-173, IF-175 and IF-288 in `docs/requirements/interfaces.toml`; `docs/requirements/components.toml`; `docs/runtime-flows.md`; the `architecture-decomposition` skill and rubric; `spine-authoring/references/in-lane.md`; the `coordinator-cycle` skill and recipes; and the code named below.

**How this was measured.** Every figure marked measured ran at this head, reading the lane's tree, with nothing written to it. The derivation prototype ran from one throwaway script in the system temp directory, which I deleted after the run. That script and this plan are the only files I wrote.

## Measured, against the spec's figures

The spec measured at `c57796e63`, before the tags. WI-994 and WI-997 have landed since.

| Figure | Spec | Measured at this head |
|---|---|---|
| TCs | 357 | 366 live, 357 of them tagged, 0 findings from `read_test_tags` |
| TCs with no tag | all | 9: TC-035, TC-036, TC-055, TC-165, TC-166, TC-209, TC-210, TC-211, TC-279 |
| This row's scope (SR-241, SR-156, SR-154) | not given | 22 LLRs, 33 TCs, 45 test files, 0 gaps, 1 listed item (TC-325's hook file) |
| Files per SR | median 2, maximum 34 | median 2, maximum 34 (SR-156), 6 SRs reach none |
| SRs with a gap | not given | 2: SR-035 (TC-165, cell `(owed by WI-1000)`) and SR-165 (TC-166, cell `(owed by WI-999)`) |
| Queued rows a partial refusal would hit | not given | WI-999 and WI-1000 only, both until they write the owed test, which is the rule working |
| Queued rows naming no SR | WI-795, WI-827 | the same two; both are owner acts, so neither touches code |
| Smoke tier | not given | 3392 collected, ceiling `max-tests = 3410`, so 18 of headroom |
| SLOC stamps | not given | `integrate.py` 1802 and `agent_loop.py` 2526, both exact; `review_brief.py` 778, `kitlib/spine.py` 474, both unbaselined under the 1000 threshold |

## Architectural-delta answer

DELTA: within

I followed `.claude/skills/architecture-decomposition/SKILL.md`. The spec's S5 answer holds, with one correction: the boundary is three interface rows, not one (step 2 below).

1. **Mode classes (A2).** None added. A derivation refusal takes the loop's existing red route, and `attest` and the render gain refusals, not states. `docs/runtime-flows.md` Flow 1's note about attested tips is reworded to stay true (P10), and no transition is added.
2. **Value domains (A3, A6).** Values are added, and new boundaries are crossed. Both are carried as rows in P1.
   - `attest`'s refusal domain gains names-no-SR, malformed, empty and partial. The render's refusal domain gains the same four. The loop's red cause gains them as text only.
   - The set's domain is `ReviewSet(files, listed, gaps, code_touching)`, or one refusal, never both.
   - A TC's class is a closed enumeration: tagged, untagged executable, declared non-executable, no evidence. An `if`/`elif` chain makes the four disjoint and covering by construction.
   - Three new interface rows, all `call`, each with a contract body in its owner's header:
     - owner `scripts/review_set`, requestors `scripts/integrate`, `scripts/agent_loop`, `scripts/review_brief`: the derivation;
     - owner `scripts/gen_arch_map`, requestor `scripts/review_set`: `read_test_tags`. The module's CMP-006/CMP-009 tags make this a cross-component edge, so `cross_component_findings` requires a row. IF-131 is the nearest, but its notes state an intra-CMP-006 import, so a separate row keeps that statement true;
     - owner `scripts/spine_carrier`, requestor `scripts/review_set`: the SR, LLR and TC loads, following IF-109 and IF-110, one row per requestor.
   - IF-154's `data` cell loses `--tests`. IF-288's `data` cell does not name `--tests`, so only its `Contract IF-288` body changes (decision 8). IF-173's cell names `attest` without its arguments, so it is not edited.
3. **Output-on-input dependencies (A4).** The table, recorded here as the skill allows when planning:

   | Output | Inputs today | Inputs added | Input removed |
   |---|---|---|---|
   | The files `attest` runs and the `tests=` digest | operator's `--tests`; `[]` from the loop | row's `sr_refs`; SR, LLR and TC rows; test-file tags; `[paths] src` and `tests`; `trunk`; changed paths since the merge base | operator's `--tests` |
   | `attest`'s refusal or green | hooks, lane, dirt, `[bars] review`, message, the bar | the derivation's answer | none |
   | The draw's round or red | tip's record against `[]`, recorded red, the bar | the derivation's answer, and the record compared against it | none |
   | The render's brief or refusal | tip's record against `--tests`, spec, templates | the derivation's answer | operator's `--tests` |
   | Landing bar, `refresh`, smoke tier, `trace.py --tests-for` | unchanged | none | none |

4. **Descent (A8).** Requirement descent: one new LLR under SR-241, with SR-241's text amended (decision 9). Component descent, comparing the candidate cuts for the tree read:
   - **Inside `integrate.py`:** forces `review_brief` to import the merge service, and grows a module on an exact ratchet whose stated fix is decomposition.
   - **Inside `agent_common.py`:** puts the AST walk of every test file behind a module nearly every script imports.
   - **Inside `kitlib/`:** refused by construction. The package stays import-clean of `scripts/`, and the tag reader lives there.
   - **A new sibling module in CMP-008:** one small interface hides how a row's set is read, and all three consumers call it. Chosen.

   CMP-008 stays whole: no sub-component and no cut. `docs/requirements/components.toml` is not edited, because membership comes from the new LLR's `component` cell, and CMP-008's `notes` list is already partial (it omits `review_brief`). The import graph stays acyclic: `review_set` imports `agent_common`, `gen_arch_map`, `spine_carrier` and `kitlib`, and none of those imports it.

The change is carried by P1 (rows), P3 and P4 (the derivation) and P5 to P7 (the consumers). It needs no refactor, so `beyond` does not apply.

## Decisions the spec leaves to the build

The critic should check these first. Decision 1 corrects the spec's stated input.

1. **A lane's row is read through its closed copy too.** The spec gives the input as `docs/work/active/<branch>/WI-*.md`, and its Trust ruling refuses when that copy is absent. Read literally, that reds every unattended lane:
   - `prompts/worker.template.md` tells the worker to CLOSE THE ROW before it stops, so the spec leaves `active/<branch>/` in the lane.
   - `agent_loop.attest_build` then runs after that session, and `attest` runs on a tree holding only `docs/archive/work/complete/WI-N-*.md`.
   - `session_service._lane_claims` already names this route ("a lane closed under close-first and not yet merged"), and `tests/test_integrate_station.py`'s `attest_repo` is exactly that closed lane.

   The existing readers answer it, with no new path:
   - The id is the one id `kitlib.git.claimed_specs` finds for the branch at HEAD or at the merge base. The claim is a trunk commit, so the base always holds it on a real route, and HEAD holds it for a lane claimed on its own branch (`conftest.claim_on_branch`).
   - The text is `kitlib.done_when.spec_at(lane, None, branch, wi)`: "its closed copy once the lane has closed it, else its copy under `active/<branch>/`".

   No id, more than one id, or no copy in the tree refuses, naming the path. This changes no Done-when wording: D1 says "the lane's claim copy", and the closed copy is that file moved. LLR-a states it (row table below).
2. **Order of reads.** Claim, then `sr_refs`, then base and changed paths, then `[paths]`. A row naming no SR is answered there, as the Trust ruling's order has it, before any registry or tag is read. It has nothing to walk, and an owner-act row needs no registry to stay green. Every other input is read before the four-way answer, so a malformed input outranks partial and empty.
3. **A row that touches no code and has a non-empty set runs that set.** The spec's "`[bars] review` alone" sentence follows "an empty set is allowed", and the Trust ruling scopes it to an empty set. So a docs row naming SR-156 runs its tagged files. Only an empty set runs the bar alone.
4. **The set is files.** A node tag `tests/x.py::test_y` contributes `tests/x.py`, as the spec's "tagged test files" says. A tagged file with another extension is passed to `[product] test` as it stands: the tests root is the adopter's and the command is theirs.
5. **Names.** `review_set.py`, `derive`, `ReviewSet`, and `kitlib.spine.llrs_under` and `review_scope`. No name starts `test_` or `Test`, because pytest would collect a re-exported `Test*` class.
6. **What is read from where.** The claim listing and row text are read from git (HEAD, base, index). Registries, `docs/stack.ini` and tags are read from the lane checkout. `attest` has already refused a worktree differing from the index, so at `attest` the two agree. At the render and the draw a working-tree edit can only change the derived list, and the digest compare then refuses, which is the spec's binding.
7. **The change set is wider than D9's list, as `in-lane.md` requires.** It says to include "each approved row whose text the change makes untrue". Four more rows are:
   - **LLR-313:** "requires its test list". An empty set is now a valid round.
   - **TC-333:** "An empty test list ... refused", and its evidence names `test_a_round_with_no_tests_refuses`, which this row inverts.
   - **TC-132:** "the bar and named-tests command declared by its lane staged tree".
   - **TC-371:** "render with an equivalent reordered test list" and "The record producer and rendering consumer agree on a reordered equivalent test set". With no hand list there is nothing to reorder, so the case becomes "the set `attest` derived and the set the render derives agree". The spelling pin stays at `tests_digest` (LLR-207, TC-205).
8. **IF-288.** D9 lists its data cell, but that cell is `review / critique [--plan --sha] / file / plan [--revise] / plan-file (...)` and holds no `--tests`. There is nothing to delete, so the body and the module's usage line change (P7). The adjudicator sees this stated.
9. **SR-241: amend it as well as adding the LLR.** D9 leaves this to the in-lane adjudicator. I propose both, because a refusal an LLR states and its SR does not is the distorted breakdown `spine-authoring` warns about. SR-241 today says only "the named test set", and has no refusal for a row naming no requirement or for an empty or partial set. The proposed text keeps the capability voice and names no artifact: the record is for "the test set derived from the work item's requirements", and the acceptance gains the refusals and the non-code exemption. `human_approval_through` is `DevStg-Boundary`, so `DevStg-Reqs` is released and the act can happen in the lane. If the adjudicator rules LLR-only, the code and tests do not move, and the table below keeps its rows.
10. **The gate derives once to compare, and `attest` derives again.** On a refusal the gate leaves `attested` as None and falls through to its existing arm, so `integrate.attest` refuses with the same text and `record_bar_result` records it. That is the "no new route": no separate refusal arm exists to diverge. It costs a second tag read on that path (about 3 s, per WI-994's measure).
11. **SR-242 and LLR-343 stay as they are.** LLR-343 counts recorded red build commits, whatever the cause, and LLR-344's amendment states that a derivation refusal is recorded as a red. SR-242's "red review-bar rounds" then holds.
12. **A red record is clipped.** `format_red_record` keeps 240 characters, head and tail, so the refusal text opens with its kind and gap count. The session log's body keeps the whole text, and the worker's next `attest` prints it all.
13. **`[product] test` becomes load-bearing for the loop.** `_run_review_bar` already refuses a non-empty set with no `[product] test`, and the loop never reached that line because it passed `[]`. The shipped template declares the key, so a default adopter is unaffected. The RESYNC entry says so.
14. **An in-flight lane re-attests once.** A record made from a hand list digests differently, so after this lands a render or a draw on an open lane refuses or re-attests. It fails closed and nothing migrates, and the RESYNC entry states it.
15. **This lane runs on trunk's scripts until it lands.** `attest` and `review_brief.py` run from the primary checkout, so this lane keeps typing `--tests` until landing. Every commit below names its list. The derived list only takes over after landing, under the cycle's rule that a lane changing the machinery lands alone.
16. **`module_tests` shares one line.** Its test-root prefix moves into a private helper that `review_scope` also calls, so `--tests-for` behaves the same (`tests/test_evidence_join.py` pins it). Nothing else in that function changes.

## Which row states each new behaviour

Every behaviour a new or amended TC verifies, and the row that states it. `LLR-a` is the new LLR. The TCs are `TC-a` to `TC-h`, on ids reserved in P1.

| # | Behaviour | Stated by | Verified by |
|---|---|---|---|
| 1 | S is the row's `sr_refs`; L is every LLR naming an SR in S; T is every TC of any status verifying an SR in S or an LLR in L; the walk has one home | LLR-a | TC-a |
| 2 | A TC in T falls in exactly one of the four classes, with each class's rule | LLR-a | TC-a |
| 3 | The set is the sorted union of tagged test files; a tagged TC's non-test evidence is listed; a declared non-executable TC is listed, not run, and is no gap | LLR-a | TC-a |
| 4 | An SR verified only by a direct TC has no gap | LLR-a | TC-a |
| 5 | Gaps: an SR no TC verifies, directly or through its LLRs; an LLR no TC verifies, sibling LLRs included; an untagged executable TC; a no-evidence TC | LLR-a | TC-b |
| 6 | Partial means at least one gap, and names every gap; empty means no tagged file and no gap | LLR-a; SR-241 acceptance | TC-b, TC-c |
| 7 | Code-touching means a path changed from the merge base to the staged tree, renames counted both ways, under `[paths] src` or `tests`; every other path is not code | LLR-a | TC-c |
| 8 | A code-touching row naming no SR is refused by name; a row touching no code and naming no SR is an empty set | LLR-a; SR-241 acceptance | TC-c |
| 9 | For a row touching no code, gaps are reported and never refused; a non-empty set still runs | LLR-a | TC-c |
| 10 | Malformed: no claim, more than one, unparseable frontmatter, `sr_refs` not a list of id strings, an SR the registry lacks, an unreadable registry, `docs/stack.ini` or trunk declaration, and the tag reader's own refusal passed through with its text | LLR-a | TC-d |
| 11 | The row is read from its closed copy once the lane has closed it | LLR-a | TC-d |
| 12 | `attest` takes no list; it derives after its other preflight and before any bar; a refusal leaves branch and index as they were and runs no bar | LLR-207; IF-154 | TC-e, TC-132 |
| 13 | `attest` runs the review bar, then the derived files; records their digest in the unchanged grammar; an empty set runs the bar alone | LLR-207 | TC-e, TC-132 |
| 14 | `attest` prints the set, the listed evidence and any reported gaps | LLR-207 | TC-e |
| 15 | A draw compares the tip's record against the derived set | LLR-344 | TC-f |
| 16 | A derivation refusal is a red: no round, rework naming it, recorded against the build, counted by the red cap | LLR-344 | TC-f |
| 17 | A closed lane draws through its closed copy | LLR-344; LLR-a | TC-f |
| 18 | The render takes no list and renders the derived one; its record search compares against that set | LLR-341; IF-288 body | TC-g, TC-371 |
| 19 | A record whose digest differs refuses, naming both digests; a derivation refusal refuses with the same text; the hint names `attest` with no list | LLR-341; SR-241 acceptance | TC-g, TC-371 |
| 20 | An empty set is a valid round: no pytest line, and the brief says the row touches no code | LLR-313 | TC-g, TC-333 |
| 21 | The derivation works in a bootstrapped scaffold | LLR-a | TC-h |

The coverage bound (D11) is stated in LLR-a's `detail`: its inside set is what TC-a to TC-h drive, and its outside set is stated and not tested.

## Build table

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The spine set on reserved ids: LLR-a, TC-a to TC-h, three interface rows, the amendments, the arms map | D9; D11; SR-241; SR-156; SR-154; TC-132; TC-333; TC-371 | IF-154; IF-288; IF-131; Proposed: three call rows owned by review_set, gen_arch_map and spine_carrier, nearest IF-173, IF-131 and IF-109 | |
| P2 | The tests alone, tagged, under strict xfail marks; no shipped file | D1; D2; D3; D4; D5; D6; D7; D11; SR-241; SR-156; SR-154; TC-375; TC-376; TC-377 | IF-154; IF-288; IF-173 | P1 |
| P3 | The pure walk and classes beside module_tests in kitlib/spine.py | D1; D3; SR-241 | no interface: rows-only functions, intra-module to the kernel | P2 |
| P4 | review_set.py: the tree read, the refusals, its manifest row and contract bodies | D1; D2; D3; D4; D11; SR-241 | Proposed: the three call rows of P1, nearest IF-173, IF-131 and IF-109 | P3 |
| P5 | attest: --tests retires, the set is derived in preflight, run, digested and printed; exact size stamp | D2; D5; SR-156; TC-132; TC-205 | IF-154; IF-173 | P4 |
| P6 | The loop: the draw compares against the derived set, and attest_build and the draw lose the list; exact size stamp | D6; SR-154; TC-082; TC-375; TC-376; TC-377 | IF-173 | P5 |
| P7 | The render: --tests retires, the derived list renders, an empty set has no pytest line, the hint is corrected | D7; SR-241; SR-154; TC-333; TC-371 | IF-288 | P5 |
| P8 | The RESYNC entry and both stack.ini comments | D10; SR-156 | no interface: reference doc | P5; P6; P7 |
| P9 | The coordinator-cycle skill and recipes, synced | D8; SR-156 | no interface: documentation only | P8 |
| P10 | The runtime-flow note, reconcile the set against settled code, close its edges, take the in-lane adjudication | D9; SR-241; SR-156; SR-154; TC-132; TC-333; TC-371 | IF-154; IF-288 | P5; P6; P7; P9 |
| P11 | The log and the closing checks | D1; D11; SR-241; SR-156; SR-154 | no interface: records only | P10 |

Excludes: D12 — the A+B review bar is what the coordinator runs on the built lane; no build step delivers it. The handoff to review names it.
Excludes: TC-046; TC-048; TC-083; TC-084; TC-085; TC-361; TC-362; TC-363; TC-364; TC-365; TC-366 — they verify SR-154's routing, critique dispatch, scoring, escalation and account rows, none of which reads a review test set.
Excludes: TC-131; TC-139; TC-144; TC-145; TC-317; TC-369; TC-370 — they verify SR-156's pause, spec move, dispatch, claim, context guard, trunk name and hook rows. This row reads the trunk reader, the claim listing and the hook floor as they are and changes none of them.
Excludes: TC-257; TC-259; TC-325; TC-326; TC-327; TC-328 — they verify the session-log record and the Done-when blessing. This row reads `spec_at` unchanged and adds no record or hold.
Excludes: TC-367 — it verifies the single-plan pass gate, which no part of this row touches.

**Why some clauses span several rows.** The gate reports these as multi-covered, so each split is stated here.
- D1: P2 writes the tests, P3 the walk, P4 the tree read, and P11 records the live measure.
- D2: P4 decides the refusal, and P5 shows that no bar runs.
- D3: P3 finds the gaps, and P4 turns them into a refusal.
- D4 to D7: P2 writes the tests, and the row named in the table delivers the behaviour.
- D9: P1 authors the set, and P10 reconciles it and takes the sitting.
- D11: P1 states the bound, P2 and P4 hold to it, and P11 records it.

## Commits and what each one owes the bar

Every row is whole inside one commit. All commits go through trunk's `integrate.py attest --bar review --tests <list>`, except C1 and C6, which are hand commits under the cycle's rules, each after `run_menu.py smoke`. The bar's steps are `trace.py --strict`, `check_trajectory.py --strict`, `check_docs.py --stale`, `check_resync.py` and the smoke tier.

The list for C2 to C4 is `tests/test_review_set_walk.py tests/test_review_set.py tests/test_integrate_attest.py tests/test_agent_loop_review_gate.py tests/test_review_brief_git.py tests/test_review_brief.py`.

| Commit | Rows | Shipped file | Stamps it carries | Why the bar is green at this commit |
|---|---|---|---|---|
| C1 | P1 | none | watermark fold | Rows stay `Drafted`, on reserved ids. TC evidence cells hold `(owed by the tests commit)`. `check_resync` sees no shipped path. `review_set` named before it exists is warn-first: `if_endpoint_class_advisories`, the undeclared-owner reverse check and `if_data_advisories` never join the exit code, and the owner rule passes because LLR-a's `module` names it. If the strict lints refuse anyway, the three new rows and their TC cites move to C3, and nothing else moves. |
| C2 | P2 | none | none | `check_resync` sees no shipped path. No script size moves. Cells take their nodes beside the tags, so `check_trajectory --strict` holds. Red cases report `xfailed`. Smoke grows by 14, within the 18 of headroom. |
| C3 | P3, P4, P5, P6, P7, P8 | the scripts below, `stack.ini.template`, `RESYNC_PACK.md` | `integrate.py` and `agent_loop.py` in `tests/test_module_size_ratchet.py`, with the reason in the same commit's log fragment; `docs/flag-axis-baseline` if a reading falls | Marks and stand-ins are gone, and existing tests move to the new signature in this commit. `check_resync` finds the entry anchored at the base. |
| C4 | P9 | the three skill copies | `bootstrap.py --dest . --sync` | The entry from C3 covers these paths. Smoke grows by the one or two cases P9 adds, 16 at most in all. |
| C5 | P10 | none unless a return moves code | any count a return moves | Row text, verdicts and acts, as the cycle's checkpoint orders them. |
| C6 | P11 | none | none | Record-only: the log fragment and the Done-when ticks. A tick does not unbind the pass record. |

**Why P3 to P8 share a commit.** The spec's S1 says the three consumers switch together, since the digest changes meaning. `attest` commits one staged round, the code commit removes all the marks, and the RESYNC entry states refusals only P5 to P7 deliver. Review rounds sit between C4 and C5, as the cycle orders them. Each round's fix commit keeps the stamp rule: a change that moves a ratcheted size re-stamps in that commit.

Trunk-only artifacts are left to the landing regeneration: `docs/cli-reference.md`, `docs/interface-reference.md`, `docs/requirements/components.derived.toml` and `docs/ratify/CURRENT.md`.

## The steps

### P1. The spine set

Reserve first: `trace.py --reserve-ids WI-995 LLR=1,TC=8,IF=3`. Before the spine turn, the coordinator checks the recipe's rule on open lanes amending the same rows or functions. The lane's spine author writes the set once, from the anchor down, with an arms map. Rows stay `Drafted`, and row text states behaviour, never code (the 2026-10-11 ruling).

- **SR-241:** amended as decision 9.
- **LLR-a** under SR-241, `component = "CMP-008"`, `module` naming `review_set.py` and `kitlib/spine.py`: rows 1 to 11 and 21 of the table above, plus the coverage bound. It states the closed-copy reading (decision 1) and the order of reads (decision 2).
- **LLR-207:** "reads the review bar and named tests from the attested lane's own declarations" becomes the derived set; the refusal list gains the derivation's refusal; the printing joins it.
- **LLR-341:** "the round's named tests" becomes the derived set; the refusal's "attest step with the lane and round test list" loses the list; a derivation refusal joins.
- **LLR-344:** the record compared is the derived set's; a derivation refusal is recorded as a red; the draw over a closed lane.
- **LLR-313:** "requires its test list" goes; an empty set renders with no test command and says why.
- **TC-132, TC-333, TC-371:** amended as decision 7. Each keeps its id. Their evidence cells change only where a test is renamed.
- **New TCs**, each naming its LLR and that LLR's SR:

| TC | Tier | `verifies` | Module | Rows of the behaviour table |
|---|---|---|---|---|
| TC-a | Smoke | SR-241, LLR-a | `tests/test_review_set_walk.py` | 1, 2, 3, 4 |
| TC-b | Smoke | SR-241, LLR-a | `tests/test_review_set_walk.py` | 5, 6 |
| TC-c | Full | SR-241, LLR-a, the new `review_set` row | `tests/test_review_set.py` | 6, 7, 8, 9 |
| TC-d | Full | SR-241, LLR-a, the two new read rows | `tests/test_review_set.py` | 10, 11 |
| TC-e | Full | SR-156, LLR-207, IF-154 | `tests/test_integrate_attest.py` | 12, 13, 14 |
| TC-f | Full | SR-154, LLR-344, IF-173 | `tests/test_agent_loop_review_gate.py` | 15, 16, 17 |
| TC-g | Full | SR-241, LLR-341, LLR-313, IF-288 | `tests/test_review_brief_git.py` | 18, 19, 20 |
| TC-h | Full | SR-241, LLR-a | `tests/test_review_set.py` | 21 |

- **Interface rows:** the three new rows and IF-154's `data` cell. IF-154 gets its first citing TC (TC-e), and IF-173 is cited by TC-f because the loop's call changes shape. Their `docs/if-tc-coverage-allow` lines stay: a listed seam gaining a TC is warn-only housekeeping, and pruning would move `test_this_repos_seam_tc_allowlist_is_exactly_its_seeded_set`'s pin for no gain (WI-994's decision 16).

### P2. The tests alone

Every new case carries a strict expected-failure mark and its `Implements:` tag, and each TC's cell takes the node in this commit. `test_review_set` joins `tests/conftest.py` `SLOW_MODULES`. `tests/test_review_set_walk.py` stays in smoke as the family's in-process pin.

**Reaching the assertion.** A missing module or a changed signature would fail with an import or type error, which the mark refuses. So:
- The walk tests call `getattr(kspine, "review_scope", <stand-in returning an empty answer>)`.
- The lane tests go through one helper that loads `review_set` or a stand-in answering `(None, "no derivation")`.
- The `attest`, draw and render tests drive the command line and the loop, whose surfaces exist today.

All stand-ins live in the test modules, so this commit touches no shipped file. P4 deletes them with the marks.

A shared fixture, `seed_row(root, srs, llrs, tcs, tags, sr_refs)`, writes the registries, the tagged test files and the row. It goes in `tests/conftest.py`.

| Test | Module | Fails before the change because |
|---|---|---|
| `test_the_walk_unions_direct_tcs_and_tcs_through_the_llrs` | walk | the stand-in returns no files |
| `test_an_llr_naming_two_srs_is_reached_from_either` | walk | same |
| `test_a_drafted_tc_is_in_scope` | walk | same |
| `test_a_tc_falls_in_exactly_one_class[tagged, untagged, non-executable, no cell, missing path]` | walk | no class is returned |
| `test_a_tagged_tc_lists_its_non_test_evidence_beside_the_set` | walk | nothing is listed |
| `test_the_set_is_the_sorted_files_of_the_tagged_nodes` | walk | no files |
| `test_an_sr_verified_only_directly_has_no_gap` | walk | no files or listed item |
| `test_each_gap_is_named[sr, llr, sibling llr]` | walk | no gaps are returned |
| `test_a_src_or_tests_change_is_code_touching_and_any_other_path_is_not` | set | the stand-in gives no answer |
| `test_a_rename_out_of_src_still_touches_code` | set | same |
| `test_the_changed_paths_are_counted_from_the_merge_base` | set | same |
| `test_a_code_touching_row_naming_no_sr_is_refused_by_name[absent, empty]` | set | the text is not the named refusal |
| `test_a_row_touching_no_code_and_naming_no_sr_is_an_empty_set` | set | no set is returned |
| `test_partial_names_every_gap_and_outranks_empty` | set | not the named refusal |
| `test_empty_is_refused_only_with_no_gap_and_no_tagged_file` | set | same |
| `test_gaps_on_a_row_touching_no_code_are_reported_never_refused` | set | no set or gaps |
| `test_each_unreadable_input_refuses_by_name[...]`, one id per arm of row 10 | set | not the named refusal |
| `test_the_tag_readers_refusal_passes_through` | set | same |
| `test_a_lane_closed_in_its_own_tree_reads_its_closed_copy` | set | no set |
| `test_a_bootstrapped_scaffold_derives_the_set` | set | no `scripts/review_set.py` in the scaffold |
| `test_attest_takes_no_tests_argument` | attest | `--tests` is accepted today |
| `test_a_derivation_refusal_runs_no_bar_and_leaves_branch_and_index[no sr, partial, empty]` | attest | today `attest` commits a record |
| `test_attest_runs_the_review_bar_then_the_derived_files` | attest | today's digest is `none`, and no files run |
| `test_attest_prints_the_set_and_the_listed_evidence` | attest | not printed |
| `test_a_row_touching_no_code_runs_the_bar_alone` | attest | characterization of today's empty run, unmarked, with its adequacy witness: an implementation that widened to the whole bar |
| `test_a_code_lane_with_an_untagged_tc_draws_no_round` (D6's regression) | gate | today the draw attests `[]` and draws |
| `test_a_derivation_refusal_counts_toward_the_red_cap` | gate | no red record exists |
| `test_the_draw_runs_the_derived_files_and_compares_their_digest` | gate | today's record digests `none` |
| `test_a_closed_lane_draws_over_its_closed_copy` | gate | the digest is `none`, not the set's |
| `test_the_render_takes_no_tests_argument` | brief git | `--tests` is required today, so the render exits 2 |
| `test_the_render_lists_the_derived_files` | brief git | same |
| `test_a_working_tree_tag_edit_refuses_naming_both_digests` | brief git | same, so neither digest appears |
| `test_a_derivation_refusal_refuses_the_render_with_its_text` | brief git | same |
| `test_the_refusal_hint_names_attest_without_tests` | brief git | the hint carries `--tests` |
| `test_an_empty_set_renders_no_pytest_line_and_says_why` | brief git | exit 2 |

Smoke grows by 14 here (the walk module's collected cases).

### P3. The pure walk (`kitlib/spine.py`)

- `llrs_under(srs, llrs)`: the one home of the SR → LLR walk. Item 5's schema lane extends this one function.
- `review_scope(srs, llrs, tcs, tags, test_root, exists)`: returns files, listed and gaps. `exists` is a predicate the caller hands in, so the kernel still reads rows only. `tags` is `read_test_tags`' map. Evidence is read with `evidence_items`.
- The class is an `if`/`elif` chain in the spec's order: tagged, any item under the tests root, items present and all existing, else no evidence. Gaps read `SR-n: no test case verifies it`, `LLR-n: ...`, `TC-n: no test file tags it (evidence names <path>)` and `TC-n: no evidence (<cell, or the missing path>)`.
- The shared prefix helper (decision 16).

Each function carries `Implements: SR-241, LLR-a`. All stay under the complexity threshold.

### P4. `review_set.py`

`derive(lane, branch)` returns `(ReviewSet, None)` or `(None, refusal)`: a refusal is a return value, as IF-173 promises. The refusal opens with its kind and, for partial, the gap count (decision 12). The reads:

- **Row:** decision 1, then `kregistry.parse_spec_frontmatter`.
- **Base:** `agent_common.worker_base(lane)`, which turns `TrunkUndeclared` into a reason.
- **Changed paths:** `git_paths(lane, ["diff", "--no-renames", "--name-only", "--cached", base])`. `--no-renames` makes a rename out of `src` count from both ends. `git_paths` supplies `-z`.
- **`[paths]`:** `kitlib.config.read_stack_ini`, with `src` and `tests` defaults as `_declared_test_command` has them. `StackIniError` or an absent file refuses.
- **Registries:** `spine_carrier.resolve` then `load(..., keep_examples=False)`. An absent registry refuses by name, and the `SystemExit` that `load` raises on an unparseable carrier is caught and returned as the refusal. Left alone it would kill the loop instead of taking the red route.
- **Tags:** `gen_arch_map.read_test_tags(lane, tests_dir, live_tcs)`, unguarded. Any finding refuses with the finding lines, so a stale sibling fails loudly, as `tc_tag_findings` chose.

`ReviewSet.lines()` gives the printed lines, one home for `attest` and the render.

Also here: the `bootstrap_manifest.py` entry, the `Contracts:` marker and bodies for the three new rows, in `review_set.py`, `gen_arch_map.py` and `spine_carrier.py`. Only docstrings move in the last two, so neither SLOC stamp moves.

### P5. `attest` (`integrate.py`)

- `attest(root, branch, bar, message_file=None)`, and the `--tests` argument goes.
- `_attest_preflight` calls `review_set.derive(wt, branch)` after the dirt check. It returns one small named tuple or a refusal, so its refusal arms stop padding four-tuples.
- `_attest_commit` and `_run_review_bar` are unchanged. They receive `list(derived.files)`.
- After the commit, `attest` prints `derived.lines()`.
- The docstring's `Contract IF-154` and the module's step text change.
- Existing callers move here: `tests/test_integrate_attest.py` (`_attest`, the CLI cases, and the reorder case at lines 464 to 478, which becomes the agreement case of decision 7), `tests/test_integrate_station.py:1402`, `tests/test_hooks_on_routes.py:226`. `attest_repo` gains a `seed_row` seed, so its closed `wi-401` lane derives a set through its closed copy.
- Stamp `integrate.py` exactly, with the reason.

### P6. The loop (`agent_loop.py`)

`review_draw_gate`:

```python
branch = lane_branch(root)
derived, refused = review_set.derive(root, branch)
attested, _cause = (
    (None, refused) if refused
    else kverdict.review_attestation(root, "HEAD", derived.files)
)
```

The rest of the function is unchanged (decision 10), and `integrate.attest` loses its list here and in `attest_build`. A worker fixture with no row in its tree gains `claim_on_branch` (`tests/test_agent_loop_worker.py:563`, `tests/test_agent_loop_review.py`'s two fixtures already have it). The assertion at `tests/test_agent_loop_review_gate.py:535` keeps `[]`, because its lane touches no code and names no SR. Stamp `agent_loop.py` exactly.

### P7. The render (`review_brief.py`)

- `--tests` goes from the parser, the usage line and `Contract IF-288`.
- `_cmd_review` calls `review_set.derive(args.root, lane)` after `lane_commits`, and a refusal raises `BriefError` with its text.
- `Round` loses "a round names the tests" and gains `listed`.
- `_run_lines` writes the pytest line only for a non-empty set. For an empty one it writes a fixed line saying the set is empty because the row touches no code. A pytest line with no paths would run the whole suite.
- Listed evidence and reported gaps render as facts beside it.
- `_review_bar_refusal`'s hint drops `--tests {}`.
- `tests/test_review_brief.py` lines 180, 333 and 354 and `tests/test_review_brief_git.py`'s `_review_argv` move here. `test_a_round_with_no_tests_refuses` becomes the empty-round case, one for one, so the smoke count holds.

### P8. The RESYNC entry

Heading: `### The review test set is derived from the row's SRs [since <merge-base>]`, followed by the pack's anchoring line, re-anchored if the lane rebases. It states:

- `attest` and `review_brief.py review` lose `--tests`.
- The review bar runs the row's tagged tests through `[product] test`, the unattended loop's included (decision 13).
- A code-touching row names its SRs or is refused, and an empty or partial set refuses.
- No data, key or record format migrates, and an open lane re-attests once (decision 14).
- Row 1's entry (the tags) is the precondition.
- Kit-owned overwrite: `scripts/review_set.py` (new), `scripts/integrate.py`, `scripts/agent_loop.py`, `scripts/review_brief.py`, `scripts/gen_arch_map.py`, `scripts/spine_carrier.py`, `scripts/kitlib/spine.py`, `scripts/kitlib/bootstrap_manifest.py`.

The comment above `[bars]` in `project-trajectory/stack.ini.template` and `docs/stack.ini` changes from "the round's named tests" to the row's derived set. It is comment text, so `tests/test_dogfood_sync.py` sees no structure move.

### P9. The coordinator text

Edit `project-trajectory/skills/coordinator-cycle/` and sync with `bootstrap.py --dest . --sync`, which writes `.claude/` and `.agents/`.

- **`SKILL.md` Iterate step 1:** drops "with the round's `--tests`".
- **`references/recipes.md` §1:** the render command loses `--tests <files>`, and the two sentences explaining the flag go, replaced by what the render derives and refuses.
- **The two `attest` lines (1219, 1233):** lose `--tests <files>`.
- **The trap at 1302:** retired.
- **New text:**
  - The spine-step order: a commit adding TC rows before their tests is made without an attestation, or staged into the attest that carries those tests, because the first attest after it must hold their tagged tests or it refuses as partial.
  - How each refusal is fixed: partial, tag the test or write it in the lane; names no SR, amend the row's `sr_refs` on trunk and rebase the lane, since the set reads the lane's own copy; empty, a code row whose SRs reach only non-executable evidence names an SR with a test, or adds one; malformed, fix the named input.

One test joins `tests/test_prompts.py`: no copy holds an `attest` or `review` line with `--tests`, and the retired trap is gone. It fails today on all three copies. It brings smoke's growth to 15, or 16 if the builder splits it per copy.

### P10. Reconcile and adjudicate

- Flow 1's note in `docs/runtime-flows.md` reads "attested green for the row's derived test set (LLR-344)". The heading's cited rows gain none.
- Reconcile the row text against the settled code, close the edges (`in-lane.md`: parents in the set, each TC names its LLR and SR, each altered interface row has a citing TC, no `(owed ...)` note left), and take one combined sitting, approving parents first.
- D9 passes when that sitting does. Decisions 7, 8 and 9 go to the adjudicator stated, not implied.

### P11. Log and closing checks

The fragment `docs/log.d/WI-995-review-test-set-derived.md` opens at C3 with the stamps' reasons. P11 completes it with:

- the live measure of D1: this row's own derived set, and the SR-034 and SR-184 shapes on the real tree;
- `derive`'s wall time over this repo;
- the smoke count against `max-tests`.

Run `trace.py --strict`, `check_trajectory.py --strict` and `run_menu.py smoke`. The full suite stays with the lane refresh and phase close, as `CLAUDE.md` orders.

## Budgets

- `integrate.py`: exact ratchet at 1802. About +6 for the derive call, the import and the printing, less the argument, and the named tuple may offset it. Stamped in C3 at the exact census.
- `agent_loop.py`: exact ratchet at 2526, about +6, stamped in C3.
- `review_set.py`: about 130 SLOC, new, under the 1000 threshold, so no entry.
- `kitlib/spine.py`, `review_brief.py`: unbaselined, far under 1000.
- `docs/complexity-baseline` only tightens, and no listed function grows. New functions and tests stay under the threshold. `check_complexity` also reads `tests/`.
- `docs/flag-axis-baseline`: `integrate.py` and `agent_loop.py` may shed a literal call site, re-stamped downward in C3 if so.
- Smoke: 3392 now, about 3408 after this lane, ceiling 3410. If trunk's growth takes that past the ceiling at a rebase, the walk cases are in-process units, so `max-tests` is re-stamped with the reason in the log, as `tests/test_smoke_budget.py` directs.
- Wall time: the tag read costs about 3 s on a loaded box, once per `attest` and render, and at most twice per draw. The bar gains the row's files: 45 for this row's own SRs, median 2 per SR.

## Coverage bound

D11's inside set is driven: filing and claiming a row by the fixtures' own writers, in-lane spine authoring by `seed_row`, tagging by the real reader, `attest` and the loop's draw end to end, and a closed lane by `attest_repo`. Its outside set is stated in LLR-a and is not tested: a hand-edited claim copy or `Bar-Green:` line, hand-chosen path aliases, and sub-second windows. The spec's bound on a lane narrowing its own `sr_refs` stands, and this row adds no guard against it.

## Found outside this row, not changed

- `Contract IF-173` in `integrate.py` names three siblings and omits `agent_loop` and `attest`, though the row lists both.
- CMP-008's `notes` list omits `review_brief` and other members.
- PROCESS.md states nothing about a code row naming its SRs. The RESYNC entry and the skill carry it, as the spec orders, and whether the rule also belongs in PROCESS.md is a separate call.
