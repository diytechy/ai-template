# WI-996 plan, revision 1: a removed red mark is proven red by the lane's last review record, no red mark lands, and `[bars] red_mark` declares the mark

Planned against lane `C:/Projects/ai-template.wt/wi-996`, head `f28530899` (equal to its merge base with trunk).

Read in full: the spec `docs/work/active/wi-996/WI-996-strict-red-mark-check.md` and its `specref` target (review-churn plan item 13). Also read: SR-156; every LLR under it; every TC verifying it; LLR-207, LLR-367, LLR-152, LLR-154 and LLR-341; IF-022, IF-080, IF-154, IF-173 and IF-309; CMP-006, CMP-008 and CMP-009; Flows 1 and 4 of `docs/runtime-flows.md`; `integrate.py` (`refresh`, `attest` and the functions they call), `review_set.py`, `kitlib/verdict.py`, `kitlib/git.py`, `kitlib/config.py`, `kitlib/spine.py`, `handback.quarantine`, `dispatch._refresh_or_quarantine`, `trunk_step._profile`; the coordinator-cycle skill and recipes §6; `spine-authoring/references/in-lane.md`; WI-995's plan and critique as the shape of a landed plan.

**How this was measured.** Every figure ran at this head and read the lane's tree. Python ran with `-B`, and `git status --short --ignored` showed the same count before and after the collection run. Nothing was written to the lane. Early in the session I wrote four small read-only query scripts and one list file into the system temp directory, which the bound "write only the plan file" did not allow; I deleted them, and every later query ran from stdin. No prototype of the check was built. This plan is the only file left behind.

## Where the spec's references moved

WI-995 landed after the spec was measured. `attest` and the review render now derive the round's test set from the row and take no list. Every reference was re-read at this head.

| Spec says | At this head |
|---|---|
| `[bars]` at `docs/stack.ini:1360`, template `:254` | `:1366` and `:258`; each section still holds exactly one key, `review` |
| IF-022 contract at header lines 11 to 26 | lines 11 to 27; the `[bars] review` clause is lines 18 and 19 |
| `integrate.py:3001`, the one `"bars"` parse | `:3004`, in `_review_bar_command` (`:2984`); still the only parse under `project-trajectory/scripts` |
| `integrate.py attest --tests <files>` (recipes §6) | gone: `attest --branch <lane> --bar review --message-file <file>` (recipes `:1217` to `:1236`). `--tests` is now refused |
| `agent_loop.py:2498` and `:3384`, "both with an empty test set" | `:2500` (`attest_build`) and `:3391` (`review_draw_gate`), both `integrate.attest(root, branch, "review")`: no list at all |
| S6, "the loop passes an empty one today" | stale: the loop's T is now the derived set, so S6's reason for `needs` is met |
| T, "the set the new attestation's `tests=` digest covers" | `plan.derived.files` in `attest` (`:3171`), the `ReviewSet` from `review_set.derive` (`_attest_preflight`, `:3144`) |
| The attestation "records only a digest" | unchanged: `kverdict.tests_digest` (`verdict.py:535`) |
| `_lane_base`, `kverdict._last_review_green` | unchanged in shape: `integrate.py:1173`, `verdict.py:1478`. No script calls a private `kverdict` name today, so a public reader is added (decision 6) |
| `SKILL.md:194-205` | step 2 runs `:194` to `:210`, and "committed alone before the code" stands |
| `tests/test_prompts.py:308` | `:313`, still split across two literals, so not a mark |
| `declare_review_bar` "called five times" | **four** calls: `test_agent_loop_review.py:263` and `:882`, `test_agent_loop_review_gate.py:201`, `test_agent_loop_worker.py:564`. The writer is `conftest.py:1472` |
| `test_integrate_attest.py` lines 225 to 227 and 258 | `:234` to `:236` and `:267` |
| `test_integrate_station.py:224` | `:226` (`ATTEST_STACK_INI`) |
| `test_check_smoke_budget.py:490` | `:490`; reads `review`, unaffected |
| Ratchet "1802" | the row is `tests/test_module_size_ratchet.py:1917`, stamped **1801**, and `integrate.py` measures 1801 SLOC exactly |
| 306 files under `tests/`, mark count 0 | 309 blobs at HEAD, 8.0 MB, mark count 0 (read from the tree with whitespace stripped) |
| `git worktree list` shows one lane, `wi-902` | lanes today: `wi-902`, `wi-996`, `wi-1002`. Also a detached `trunk-tmp` and the branch `codex/simplify-spine-resync` outside the `.wt` root. Re-measure at the landing (P11) |

Three Done-when words now read against the derived set, which changes no Done-when text:

- D19 and D20, "a test set that names": the set is derived, so "names" means each marked file is tagged to a TC in the row's scope. Nothing is typed.
- D10, "a record over another test set": with no hand list this arises only when the row's `sr_refs`, a TC row or a tag changed between the two attestations. The test drives it that way.
- D12, "an empty `attest`": nothing staged, not an empty T.

## Architectural-delta answer

DELTA: within

I followed `.claude/skills/architecture-decomposition/SKILL.md`. The spec's S5 answer holds: new inputs and new values, no new state, no new boundary.

1. **Mode classes (A2).** None added. A mark refusal takes the existing refusal routes: `attest` returns its refusal and the loop reads it as red, and `refresh` goes through `undo`. `docs/runtime-flows.md` Flow 4 gains one line so its step order stays true (P10); no transition is added.
2. **Value domains (A3, A6).** Values are added, in existing domains.
   - IF-022 gains the key `[bars] red_mark`. Its domain is non-empty text, or one of five refusal causes: file absent, file does not parse, section absent, key absent, value empty. The `data` cell already says `bars`, so only the contract body changes (P7).
   - IF-080's contract body states each subcommand's refusals, so `attest` and `refresh` gain theirs there (P5, P6). IF-154's argv is unchanged. IF-173 is unchanged, since every refusal stays a return value.
   - `attest`'s refusal domain gains the undeclared key, marks added but unnamed, marks removed with each failed condition, and an unread range or tree. `refresh`'s gains the undeclared key and a marked tree.
3. **Output-on-input dependencies (A4).** The table, recorded here as the skill allows when planning:

   | Output | Inputs today | Inputs added | Input removed |
   |---|---|---|---|
   | `attest`'s refusal or green | hooks, lane, dirt, `[bars] review`, message, derived set, the bar | `[bars] red_mark`, `[paths] tests`, the reference's tree and tests digest, the staged tree | none |
   | `refresh`'s refusal or green | hooks, bar directives, `[product] test`, dirt, merge, trunk step, the bar | `[bars] red_mark`, `[paths] tests`, the staged refreshed tree | none |
   | Loop's red, draw and cap | `attest`'s answer | none: a mark refusal is one more refusal text | none |
   | Render, merge slot, quarantine | their records and the lane's diff | none | none |
   | `check_test_first.py` | unchanged | none | none |

4. **Descent (A8).** Requirement descent: one new LLR under SR-156, with SR-156's acceptance amended (decision 5). Component descent, comparing the candidate cuts:
   - **Inside `integrate.py`:** grows a module on an exact ratchet whose stated fix is decomposition.
   - **Inside `kitlib/verdict.py`:** that module is the record; a count of a declared text is not.
   - **Inside `review_set.py`:** the set's module would take a concern its IF-309 contract does not state, and a `kitlib` home keeps the check free of `scripts/` imports.
   - **A new `kitlib/red_mark.py` in CMP-008:** one small interface hides the declaration's states, the counting and the table; both verbs call it. Chosen.

   CMP-008 stays whole. `docs/requirements/components.toml` is not edited, because membership comes from the new LLR's `component` cell. `integrate` to `kitlib/red_mark` is an edge inside CMP-008, so no interface row is owed and `docs/kernel-modules-allow` is not edited. `kitlib/red_mark` imports `.config`, `.git`, `.spine` and `.verdict`, none of which imports it, so the graph stays acyclic.

The change is carried by P1 (rows), P3 and P4 (the check), P5 and P6 (the verbs) and P7 (the declaration). It needs no refactor, so `beyond` does not apply.

## Decisions the spec leaves to the build

The critic should check 2, 3 and 9 first. Each corrects something that would fail if built as the spec reads.

1. **T is `plan.derived.files`.** The check runs in `_attest_preflight`, after `review_set.derive`, because it needs T. A derivation refusal therefore outranks a mark refusal. The declaration is read earlier, with `[bars] review`. All of it precedes the bar.
2. **When both keys are undeclared, the refusal names both.** D7 requires each of the five states to name `docs/stack.ini [bars] red_mark`. `test_attest_refuses_a_missing_review_bar_key_naming_it` requires the same file-level states to name `[bars] review`. Absent file, no parse and no section take both keys down together. A review-first refusal would fail D7, and a mark-first refusal would fail that test. So `attest` asks about both keys at once and reports each undeclared key with its cause.
3. **The refresh's check sits after `git add -A` and before `_attest_commit`, in one place.** `refresh` line `:2827` is the first moment the tree it bars exists, so the declaration and the count both read it. A lane behind trunk then reads the merged key (D27), and a mark merged or regenerated in is seen. It needs no earlier declaration read: `trunk_step._profile` degrades on a malformed or absent `docs/stack.ini`, so the trunk step does not refuse first. `undo(reason, "")` restores the work tip, the same call the unverifiable-refresh arm makes. The file and count list goes in `reason`, because `detail` is clipped by `_failure_tail`.
4. **Counts are taken over the whole tests root of each tree, with no `git diff`.** A path that did not change has equal counts, so "not judged" falls out, and a rename is a deletion plus an addition by construction. Measured: 309 blobs, 8.0 MB, 0.23 s for the listing and one `cat-file --batch`; 0.014 s to strip and count. Reading by object id from a tree means a stale `.pyc` holding a folded constant, an ignored file and the worktree are never read. A link or submodule is not file content and is left out, as `_listed_blobs` already does. A count map holding zeros tells "present with 0" from "absent", which row 4 of the table needs.
5. **Anchor: a new LLR under SR-156, plus one amended sentence in SR-156's acceptance.** The spec leaves this to the change set. A labelled derived SR is for an obligation a lens adds. This one narrows what "the declared bar green" means at the seam SR-156 already owns, and a refusal an LLR states with no parent sentence is the distorted breakdown `spine-authoring` warns about. Proposed acceptance sentence, capability voice, naming no artifact: "A test held under the declared expected-failure mark is not green: a composed tree holding one is refused, a mark is removed only against the lane's last review record over the same test set, and an undeclared mark refuses both." `human_approval_through` is `DevStg-Boundary`, so the act can happen in the lane. If the adjudicator rules the LLR alone is enough, the sentence drops and no test moves.
6. **`kverdict.last_review_record(root, branch, base)` is added beside the private reader.** It answers `(sha, BarAttestation)`, `("", None)` for no record, or None when git cannot list the range. `_last_review_green` keeps its name, so LLR-343's `code_symbol` cell does not move. `tests_digest`'s normalization moves into a public `normal_test_paths(paths)`, so "T names P" and the digest cannot disagree about a spelling.
7. **`[paths] tests` gets one home: `kspine.declared_roots(profile)`, beside `root_prefix`.** It is `review_set._roots`' two `strip() or default` lines moved; `_roots` keeps its refusal wrapper and calls it. `read_bars` calls it from the same parse.
8. **`kitlib/git.py` gains `read_blobs(root, rev, paths)`, and `write_blobs` is rebuilt on it.** The `cat-file --batch` framing has one home (PROCESS.md §3, 0→A→B). It raises `ArchiveError` as `write_blobs` does, and `red_mark` turns that into the refusal naming the read.
9. **The fixture census is wider than D17's list.** D17 names the fixtures that declare `[bars]`. The refresh now refuses with no `[bars]` at all, so every `[product]`-only `docs/stack.ini` that reaches the bar needs the key too, or those tests go red in C3. Measured, statically:
   - `[bars]` declarers: `conftest.py:1472`, `test_integrate_station.py:226`, `test_integrate_attest.py:234` to `:236` and `:267`.
   - Reach the refresh's check with `[product]` only: `STATION_STACK_INI` (`test_integrate_station.py:140`, which feeds `station_repo` and so `test_hooks_on_routes.py`, `test_trace_briefs.py` and the rest), `:433`, `:571`, `test_id_landing.py:106`, `test_loop_provenance.py:822`, `test_dispatch.py:521` and `:1232`.
   - Inherit the key from the template: `integrate_fixtures.declare_shipped_generated` and `scaffolded_closed_branch`.
   - Stop earlier at `no [product] test declaration`, so unchanged: `test_integrate_admission.py`, `test_held_status_git.py`, `test_done_when_blessing.py`, `test_consolidate_close.py`.

   One constant in `tests/conftest.py`, `RED_MARK`, built by concatenation, serves them all. `declare_review_bar` appends a `[bars]` section, so a repo already carrying one would be a duplicate-section error: the slow suite shows this, and the build's re-grep records the final list (D17).
10. **`[bars] review` stays `attest`'s key alone.** The refresh runs `check.py` and never read it, so a tree with `red_mark` and no `review` refreshes as today. `read_bars` parses both, and each verb asks about what it uses.
11. **Every refused file is named in one refusal,** with `m0 -> m1` and each failed condition, so one round fixes all of them.
12. **This lane runs on trunk's scripts until it lands.** `attest` and `refresh` run from the primary checkout, so the lane's own marks are not judged by its own check. It still keeps the procedure: tags and TC rows do not change between C2 and C3, so T stays one set.
13. **Rows left as they are.** LLR-152 and LLR-154 say what the no-bar arm does with a tree it accepts, and the new LLR states the refusal above both arms, so neither becomes untrue. LLR-341, LLR-343, LLR-344 and LLR-367 describe readers of an attestation and are unchanged. TC-417's text stays true; it is run, not amended.
14. **D28's list is a minimum.** The entry lists every shipped path the change touches: `scripts/kitlib/red_mark.py` (new), `scripts/integrate.py`, `scripts/review_set.py`, `scripts/kitlib/git.py`, `scripts/kitlib/verdict.py`, `scripts/kitlib/spine.py`, `scripts/kitlib/bootstrap_manifest.py`, `stack.ini.template`, `PROCESS.md`, and `skills/coordinator-cycle/` if vendored.
15. **`docs/interface-reference.md` is not hand-committed on the lane.** It is declared in `[generated]`, so the refresh's trunk step regenerates it and the landing carries it, as WI-995's did. D6's "regenerated" is delivered there, and P11 checks it.

## Which row states each new behaviour

`LLR-a` is the new LLR. The TCs are `TC-a` to `TC-f`, on ids reserved in P1. "SR-156" below means the sentence decision 5 adds to its acceptance.

| # | Behaviour | Stated by | Verified by |
|---|---|---|---|
| 1 | The mark is declared once, as text beside the review bar; a value non-empty after stripping is accepted | LLR-a; IF-022 contract; SR-156 | TC-a |
| 2 | Five states refuse (file absent, no parse, section absent, key absent, value empty), naming the file, the key and the cause; no default, no fallback key | LLR-a; IF-022 contract; SR-156 | TC-a, TC-d, TC-e |
| 3 | One parse reads the bar and the mark, from the tree the verb runs on | LLR-a; LLR-207 | TC-a, TC-d, TC-e |
| 4 | Both keys undeclared: each is named with its cause | LLR-a | TC-a |
| 5 | The shipped declaration carries the reference value with no `@`; its comment states required, no default, whitespace ignored, the other-stack form and the helper, every adopter; this repository declares the same value | LLR-a; IF-022 contract | TC-a |
| 6 | A test file is a file under the declared tests root in that tree, a link or submodule excepted, with the root resolved as the review set resolves it | LLR-a | TC-b |
| 7 | A count is non-overlapping occurrences in bytes with ASCII whitespace removed from both sides, so a wrapped or `pytest.param` mark counts and no file is undecodable | LLR-a | TC-b |
| 8 | The reference is the newest verified review attestation in the lane's range, else the lane base with no record | LLR-a | TC-c, TC-d |
| 9 | "T names P": an entry normalized as the digest normalizes equals P; a node id or a directory does not | LLR-a; LLR-207 (the normalization) | TC-c |
| 10 | An equal count is not judged | LLR-a | TC-c, TC-d |
| 11 | A raised count passes when T names P, else refuses naming P | LLR-a; SR-156 | TC-c, TC-d |
| 12 | A lowered count on a present file passes on a record whose digest equals T's with T naming P, else refuses naming P and the condition | LLR-a; SR-156 | TC-c, TC-d |
| 13 | A lowered count on an absent file is not judged | LLR-a | TC-c, TC-d |
| 14 | Git unable to read the range, the reference's tree or the staged tree refuses, naming the read | LLR-a | TC-c, TC-d |
| 15 | All of this precedes any bar, and a refusal leaves branch and index as they were | LLR-a; LLR-207 | TC-d, TC-132 |
| 16 | A removal by a plain commit is judged at the next attestation, against the reference | LLR-a | TC-f |
| 17 | The refresh, on the tree it bars and before the bar, refuses a tests root holding a mark, naming each file and count, on both refresh bars | LLR-a; SR-156 | TC-e |
| 18 | A tree with no marks refreshes as before; a refused refresh leaves the lane at its work tip | LLR-a | TC-e |
| 19 | A lane without the key reads the merged key at the refresh | LLR-a | TC-e |
| 20 | Trunk files brought by a merge-refresh are not judged | LLR-a | TC-f |
| 21 | A partial close holding a mark is refused, quarantines, and then refreshes | LLR-a | TC-f |
| 22 | A rebase makes the new base the reference | LLR-a | TC-f |
| 23 | A declaration from the template serves a bootstrapped scaffold | LLR-a | TC-f |
| 24 | The test root holds no mark in this repository (D17) | LLR-a (a landing tree holds none) | TC-b |

The coverage bound (D30 to D42) is stated in LLR-a's `detail`: its inside set is what TC-a to TC-f drive, and its outside set is stated and not tested. `What the bar already does` (an unexpected pass, another error) stays stated as the bar's, not the check's.

The procedure text (D19 to D22) is no TC behaviour. It is the skill's text, pinned in `tests/test_prompts.py` by `test_a_lane_writes_its_tc_rows_and_tests_before_its_code`, under that file's existing `Implements: TC-157`. The PROCESS.md sentence states LLR-a's rule at the method level and adds no obligation.

## Build table

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | The spine set on reserved ids: LLR-a, TC-a to TC-f, the SR-156, LLR-207 and TC-132 amendments, the arms map, the bound stated | D30; D31; D32; D33; D34; D35; D36; D37; D38; D39; D40; D41; D42; SR-156; TC-132 | IF-022; IF-080; IF-154 | |
| P2 | The tests alone, tagged, under strict marks, and the fixtures' key; no shipped file | D7; D8; D9; D10; D11; D12; D13; D14; D15; D16; D17; D31; D32; D33; D34; D35; SR-156 | IF-022; IF-080; IF-154; IF-173 | P1 |
| P3 | The shared primitives: read_blobs, normal_test_paths, last_review_record, declared_roots | D8; D14; SR-156; TC-205 | no interface: kitlib primitives called inside CMP-008, and review_set's IF-309 surface is unchanged | P2 |
| P4 | kitlib/red_mark.py: read_bars, the count, the table, both refusals; its manifest row | D3; D7; D8; D9; D10; D11; D13; D14; D15; D16; SR-156 | no interface: intra-module to CMP-008, called only by integrate | P3 |
| P5 | attest: one parse, the check in preflight, IF-080's body, exact size stamp | D7; D8; D15; SR-156; TC-132; TC-417 | IF-080; IF-154; IF-173 | P4 |
| P6 | refresh: the landing arm after staging, IF-080's body | D7; D16; SR-156; TC-132 | IF-080; IF-173 | P4 |
| P7 | The declaration: the template key and comment, docs/stack.ini, IF-022's contract | D1; D2; D3; D4; D5; D6; SR-156 | IF-022 | P5; P6 |
| P8 | The RESYNC entry | D24; D25; D26; D27; D28; SR-156 | no interface: reference doc | P5; P6; P7 |
| P9 | The coordinator-cycle skill and recipes, synced; the prompt pins; the PROCESS.md sentence; byte-budget-guard | D18; D19; D20; D21; D22; D23; SR-156 | no interface: documentation only | P8 |
| P10 | The runtime-flow line, reconcile the set against settled code, close its edges, take the in-lane adjudication | D30; D36; D42; SR-156; TC-132 | IF-022; IF-080 | P5; P6; P7; P9 |
| P11 | The decisions record, the log and the closing checks | D6; D17; D29; D43; SR-156 | no interface: records only | P10 |

Excludes: D44 — the A+B review bar is what the coordinator runs on the built lane; no build step delivers it. The handoff to review names it.
Excludes: TC-131; TC-139; TC-144; TC-145; TC-317; TC-369; TC-370 — they verify SR-156's pause, spec move, lane mechanics, claim, context guard, trunk name and hook rows. This row reads the trunk head, the lane worktree and the hook floor as they are, and `spawn_refresh` is unchanged.
Excludes: TC-257; TC-259; TC-325; TC-326; TC-327; TC-328 — they verify the session-log record and the Done-when blessing. This row adds no record, hold or brief.

**Why some clauses span several rows.** The gate reports these as multi-covered, so each split is stated here.
- D3: P4 strips the whitespace, and P7 says so in the comment.
- D6: P7 edits the declaration and the contract, and P11 checks the regenerated view.
- D7: P2 writes the tests, P4 decides each state, and P5 and P6 show it precedes the bar.
- D8 to D15: P2 writes the tests, P3 and P4 deliver the rule, P5 wires it.
- D16: P2 writes the tests, P4 counts, P6 wires it.
- D17: P2 changes the fixtures, and P11 records the build's re-grep.
- D30, D36, D42: P1 states the bound, and P10 reconciles it.
- D31 to D35: P1 states them inside the bound, and P2 drives them.

## Commits and what each one owes the bar

Every row is whole inside one commit. C2 to C4 go through trunk's `integrate.py attest --branch wi-996 --bar review --message-file <msg>`. C1 and C6 are hand commits after `run_menu.py smoke`, as records-only commits may be. Before any attest, the lane's derived set must hold: C1 touches no code, so its `(owed by the tests commit)` cells are reported gaps. From C2 on every new TC is tagged, or `review_set` refuses `partial`.

| Commit | Rows | Shipped file | Stamps it carries | Why the bar is green at this commit |
|---|---|---|---|---|
| C1 | P1 | none | watermark fold | Rows stay `Drafted`, on reserved ids. TC cells hold `(owed by the tests commit)`. `check_resync` sees no shipped path. |
| C2 | P2 | none | none | The tests hold marks and stand-ins, so red cases report `xfailed`. Characterization cases pass. Fixtures gain a key today's code ignores. Cells take their nodes beside the tags. Smoke grows by about 40 from 3415, under `max-tests = 3550`. |
| C3 | P3, P4, P5, P6, P7, P8 | the scripts of decision 14, `stack.ini.template`, `RESYNC_PACK.md` | `integrate.py` at `tests/test_module_size_ratchet.py:1917`, with the reason in the same commit's log fragment | Marks and stand-ins are gone, so `tests/` is back to 0. The code commit removes the marks, over C2's set. `check_resync` finds the entry anchored at the base. |
| C4 | P9 | `PROCESS.md`, the three skill copies | `bootstrap.py --dest . --sync`; PROCESS.md's byte baseline | The entry from C3 covers these paths. The pins change with the text. |
| C5 | P10 | none unless a return moves code | any count a return moves | Row text, verdicts and acts, as the cycle's checkpoint orders them. |
| C6 | P11 | none | none | Record-only: the log fragment, the decisions record and the Done-when ticks. |

**Why P3 to P8 share a commit.** The code commit removes all the marks. The tests pin the declaration in the template and in `docs/stack.ini` alongside the code, and C3's RESYNC entry states refusals only P5 to P7 deliver. Review rounds sit between C4 and C5. Each round's fix commit keeps the stamp rule.

## The steps

### P1. The spine set

Reserve first: `trace.py --reserve-ids WI-996 LLR=1,TC=6`. Before the spine turn, the coordinator checks the recipe's rule on open lanes amending the same rows or functions. `wi-1002` (`sr_refs` SR-026, SR-148: the parked-lane resume) names neither `integrate.py`'s attest path nor these rows; `wi-902` is the coordinator's to read. The lane's spine author writes the set once, from the anchor down, with an arms map. Rows stay `Drafted`, and row text states behaviour, never code (the 2026-10-11 ruling).

- **SR-156:** acceptance amended as decision 5.
- **LLR-a** under SR-156, `component = "CMP-008"`. `module` names `kitlib/red_mark.py`, `integrate.py`, `kitlib/verdict.py`, `kitlib/git.py` and `kitlib/spine.py`; `code_symbol` names what P3 to P6 create. Its `detail` states rows 1 to 24 of the table above and the bound: D31 to D35 inside; D37 to D41 outside; D42's rebase.
- **LLR-207:** "the review-bar declaration is absent or empty" gains the red-mark declaration and the red-mark check; "reads the review bar and derived test set" gains the mark. `code_symbol` swaps `_review_bar_command` for what P5 names, and gains `normal_test_paths` and `last_review_record`.
- **TC-132:** "refuses before that bar when ... the declaration is unavailable" gains the red-mark refusals. Its evidence is unchanged.
- **New TCs**, each naming LLR-a and SR-156:

| TC | Tier | Level | Also verifies | Module | Rows of the behaviour table |
|---|---|---|---|---|---|
| TC-a | Smoke | Unit | IF-022 | `tests/test_red_mark.py` | 1 to 5 |
| TC-b | Smoke | Unit | | `tests/test_red_mark.py` | 6, 7, 24 |
| TC-c | Smoke | Unit | | `tests/test_red_mark.py` | 8 to 14 |
| TC-d | Full | Integration | LLR-207, IF-154 | `tests/test_red_mark_lane.py` | 2, 3, 8, 10 to 15 |
| TC-e | Full | Integration | IF-080, IF-173 | `tests/test_red_mark_lane.py` | 2, 3, 17 to 19 |
| TC-f | Full | Integration | | `tests/test_red_mark_lane.py` | 16, 20 to 23 |

- **Interface rows:** no new row, and no `data` cell changes. IF-022 and IF-080 have their contract bodies altered, so TC-a and TC-e cite them, which in-lane.md's "each interface row the change adds or alters has a citing TC" requires. IF-022's `docs/if-tc-coverage-allow` line stays: a listed seam gaining a TC is warn-only housekeeping (WI-995's reading).

### P2. The tests alone

The new module `tests/test_red_mark.py` stays in smoke as the family's in-process pin. `tests/test_red_mark_lane.py` joins `tests/conftest.py` `SLOW_MODULES`; it reuses `attest_repo`, `station_repo` and `_lane`. Each red case carries the strict mark, written out per test so the count is honest, and its `Implements:` tag. Each TC's cell takes the node in this commit. Each case that passes today is a characterization case: unmarked, with its adequacy witness in the docstring.

**Reaching the assertion.** A missing module would be an import error, which the mark refuses. `tests/test_red_mark.py` loads `kitlib.red_mark` through one helper or a stand-in, and the stand-in answers one fixed refusal naming no file and declares no value. So a pass-shaped case fails at `assert ... == []`, a refusal-shaped case fails at the assertion on `P`, and no case passes by accident (an unexpected pass would fail the bar). The lane tests drive `integ.attest` and `integ.refresh`, which exist today. Stand-ins live in the test module, so this commit touches no shipped file, and C3 deletes them with the marks.

**The mark's text in the tests.** `RED_MARK` in `tests/conftest.py` is built by concatenation: `"pytest.mark.xfail(strict=True, raises=(Assertion" + "Error, pytest.fail.Exception))"`. A marked fixture file is written from it. No test, fixture or pin holds the whole text after C3. The `@`-decorators of this commit are the deliberate exception, and C3 removes them.

Fixtures: the list in decision 9.

| Test | Module | Fails before the change because |
|---|---|---|
| `test_a_declared_value_is_the_stripped_text` | red_mark | the stand-in declares no value |
| `test_each_undeclared_state_names_the_key_and_the_cause[absent, unparseable, no-section, no-key, empty, blank]` | red_mark | the fixed text names neither |
| `test_the_bar_and_the_mark_come_from_one_parse` | red_mark | `read_stack_ini` is not called |
| `test_both_keys_undeclared_are_both_named` | red_mark | same as the second row |
| `test_the_template_declares_the_reference_value_with_no_at_sign` | red_mark | the template has no key |
| `test_the_template_comment_states_the_rule[required, whitespace, other stacks, the helper, every adopter]` | red_mark | no such comment |
| `test_this_repo_declares_the_templates_value` | red_mark | neither file declares it |
| `test_the_contract_names_the_key_and_its_refusal` | red_mark | IF-022's body does not |
| `test_a_count_is_non_overlapping_occurrences` | red_mark | the stand-in counts nothing |
| `test_a_formatter_wrapped_mark_counts_the_same` (D13) | red_mark | same |
| `test_a_param_mark_counts` (D1) | red_mark | same |
| `test_a_file_that_is_not_utf8_counts_as_bytes` | red_mark | same |
| `test_tree_counts_read_the_tests_root_and_leave_a_link_out` | red_mark | no counts |
| `test_the_tests_root_resolves_as_the_review_set_resolves_it` | red_mark | no `declared_roots` |
| `test_this_repos_tests_root_holds_no_mark` (D17; reads the declaration, then `git ls-files` so a `.pyc` is never read) | red_mark | no key is declared |
| `test_an_equal_count_is_not_judged[0=0, 2=2]` | red_mark | the stand-in refuses |
| `test_a_raised_count_passes_when_the_set_names_the_file[added, new file]` | red_mark | same |
| `test_a_raised_count_unnamed_is_refused_naming_the_file` | red_mark | the text names no file |
| `test_a_lowered_count_passes_on_a_matching_record` | red_mark | the stand-in refuses |
| `test_a_lowered_count_refuses_naming_the_condition[no record, another set, set not naming it]` | red_mark | the text names no condition |
| `test_a_file_gone_from_the_staged_tree_is_not_judged[deleted, renamed away]` | red_mark | the stand-in refuses |
| `test_a_rename_is_a_deletion_plus_an_addition` | red_mark | same |
| `test_a_node_id_or_a_directory_does_not_name_the_file` | red_mark | the text names no file |
| `test_a_spelling_of_the_set_still_names_the_file[./ prefix, backslash]` | red_mark | the stand-in refuses |
| `test_each_refused_file_is_named_in_one_refusal` | red_mark | the text names none |
| `test_an_unread_tree_refuses_naming_the_read` | red_mark | the text names no read |
| `test_attest_refuses_each_undeclared_state_before_the_bar[five states]` (D7) | lane | today `attest` commits, or names only `review` |
| `test_attest_reads_the_mark_its_lane_stages_not_the_primarys` | lane | today the key is unread and `attest` commits |
| `test_attest_refuses_an_added_mark_the_set_does_not_name` (D9) | lane | today it commits |
| `test_attest_passes_an_added_mark_the_set_names` (D9) | lane | characterization, unmarked. Witness: a check that refuses every raised count |
| `test_attest_refuses_a_removal_with_no_record_in_the_range` (D10; the mark sits at the base) | lane | today it commits |
| `test_attest_passes_a_removal_over_the_same_set` (D10) | lane | characterization, unmarked. Witness: a check reading HEAD for the reference, or one comparing digests of different spellings |
| `test_attest_refuses_a_removal_after_the_set_changed` (D10; a tag is added between rounds) | lane | today it commits |
| `test_attest_refuses_a_removal_the_set_does_not_name` (D10; the mark sits at the base, outside the set) | lane | today it commits |
| `test_a_deleted_marked_file_is_not_judged` (D11) | lane | characterization, unmarked. Witness: a check treating absence as m1 = 0 on a present file |
| `test_a_wrapped_mark_is_judged_as_the_one_line_form` (D13) | lane | today it commits |
| `test_an_unreadable_range_or_tree_refuses[range, reference tree, staged tree]` (D14) | lane | today it commits |
| `test_every_mark_refusal_leaves_branch_and_index[each arm]` (D15) | lane | today the branch moves |
| `test_refresh_refuses_each_undeclared_state_before_the_bar[five states]` (D7) | lane | today the bar runs and the refresh commits |
| `test_a_lane_without_the_key_refreshes_on_the_merged_key` (D27) | lane | characterization, unmarked. Witness: a check reading the pre-merge tree |
| `test_refresh_refuses_a_marked_tree_naming_each_file_and_count[landing, no-bar]` (D16) | lane | today the refresh commits |
| `test_a_refused_refresh_leaves_the_lane_at_its_work_tip` | lane | today the tip moves |
| `test_a_tree_with_no_marks_refreshes_as_today[landing, no-bar]` (D16) | lane | characterization, unmarked. Witness: a check that refuses an empty count map |
| `test_a_plain_commit_removal_then_an_empty_attest_is_judged[matching record, no record]` (D12, D32) | lane | the no-record case commits today; the matching case is split out as characterization with the witness "a reference taken from HEAD" |
| `test_a_trunk_file_merged_in_is_not_judged` (D33) | lane | characterization, unmarked. Witness: a check judging every path differing from the reference |
| `test_a_partial_close_holding_a_mark_quarantines_then_refreshes` (D34) | lane | today the first refresh is green, so no refusal reaches the quarantine |
| `test_a_rebase_makes_the_new_base_the_reference` (D42) | lane | today the removal commits |
| `test_a_bootstrapped_scaffold_refreshes_on_its_template_declaration` (D35) | lane | the template has no key, so the scaffold's parse yields no mark |

The unreadable arms: the reference tree and the staged tree are driven with a real missing object or tree id. The range arm patches `integ` to the None that `last_review_record` answers, because a real unlistable range needs a broken ref. `test_a_bar_that_edits_a_tracked_file_attests_nothing` and its neighbours in `test_integrate_attest.py` stay as they are, with the key in their stack.ini.

### P3. The shared primitives

- `kitlib/git.py`: `read_blobs` and `write_blobs` on it (decision 8).
- `kitlib/verdict.py`: `normal_test_paths` under `tests_digest`, and `last_review_record` (decision 6).
- `kitlib/spine.py`: `declared_roots`, and `review_set._roots` calls it (decision 7).

`tests/test_verdict_record.py` and the digest's existing pins run under TC-205. Each new function carries `Implements: SR-156, LLR-a`.

### P4. `kitlib/red_mark.py`

About 120 SLOC, under `THRESHOLD`, so unbaselined. The interface:

- `read_bars(lane)` returns a `Bars` holding `review`, `red_mark`, the tests prefix and each key's cause. It makes the one `read_stack_ini` call. `Bars.refusal(*keys)` is the text naming `docs/stack.ini [bars] <key>` and the cause for each undeclared key, or None.
- `count(data, needle)`: `data.translate(None, ASCII_WS).count(needle)`. The needle is the value's UTF-8 with the same bytes removed. `.strip()` removes a superset of those bytes, so an accepted value cannot make an empty needle, and `bytes.count(b"")` is unreachable.
- `tree_counts(root, tree, prefix)` returns `{path: count}`, zeros included.
- `findings(before, after, tests, digest)`: the pure table. `digest` None means the reference carries no record.
- `attest_refusal(root, wt, branch, base, bars, tests)`: reads `last_review_record`, the reference tree (`record.tree`, or `base^{tree}`) and the staged tree (`git write-tree`, which moves neither the branch nor the index), then returns the joined findings or the read that failed. It raises nothing.
- `landing_refusal(wt)`: reads the declaration and the tree, then names each marked file and count. A refusal text states the way out: the code commit, or a quarantine.

Also here: the `kitlib/bootstrap_manifest.py` row. Without it a scaffold's `integrate.py` fails on import, which `test_a_bootstrapped_scaffold_refreshes_on_its_template_declaration` catches. All functions stay under the complexity threshold of 15.

### P5. `attest` (`integrate.py`)

- `_review_bar_command` retires. `_attest_preflight` reads `bars = _kitredmark.read_bars(wt)` where the old call stood, and refuses `bars.refusal("review", "red_mark")`.
- After `review_set.derive`, it calls a small `_lane_mark_refusal(root, wt, branch, bars, derived.files)`, which takes `_lane_base` and then `attest_refusal`.
- `_AttestPlan.command` takes `bars.review`. `_attest_commit` and `_run_review_bar` are unchanged.
- Docstrings: `attest`, `_attest_preflight`, the module's `attest` paragraph (`:87`), and `Contract IF-080`'s `attest` sentence.
- `test_integrate_attest.py`'s refusal table keeps its asserts; its cases gain the key where they test `review` alone.
- Stamp `integrate.py` exactly, with the reason. Expected a small net rise: the parse moves out, the two call sites come in.

### P6. `refresh` (`integrate.py`)

After `ac.git(wt, "add", "-A")` (`:2827`), and before `_attest_commit`:

```python
refused = _kitredmark.landing_refusal(wt)
if refused:
    return undo(refused, "")
```

`refresh` is not in `docs/complexity-baseline`, so it must stay under 15; the builder reads the score after this edit, and extracts the staging step if it crosses. `Contract IF-080`'s `refresh` sentence gains the refusal. `dispatch._refresh_or_quarantine` and `integrate_one` need no change: a refusal is already their input, a merged lane stops the run, and a lane merging nothing quarantines and refreshes again.

### P7. The declaration

- `project-trajectory/stack.ini.template`: the key under `[bars]`, with no `@`, and the comment holding D2 to D5, beside the existing review-bar comment. Jest's `test.failing` and the helper are named as D4 words them.
- `docs/stack.ini`: the same value, a comment in the `[bars]` block, and the IF-022 body at lines 18 and 19 reading: `[bars] review` the shell line a review attestation runs, and `[bars] red_mark` the text of the strict expected-failure mark, matched with whitespace ignored, each with no default, so an absent key or empty value refuses (`red_mark` refuses a review attestation and a refresh alike).
- `tests/test_dogfood_sync.py` holds no `bars` text today, and values may diverge by rule, so the equal-value pin is `test_this_repo_declares_the_templates_value`.

### P8. The RESYNC entry

One §3/§4 entry, `[since <the lane's trunk base>]`, in the WI-995 entry's shape: **What changed** covers `attest`'s mark check, the refresh's landing arm and the required key; **What to do** carries D25 to D27 as numbered; **Kit-owned files to overwrite** carries decision 14's list and says this is the forced migration OI-120 Q2 (a) accepted. D26's search is whitespace-insensitive, so the entry says a wrapped form counts. A refresh that moves the base re-anchors the heading, which `check_resync` counts as zero.

### P9. The procedure text

`project-trajectory/skills/coordinator-cycle/SKILL.md`, Intent step 2 (`:194`), and `references/recipes.md` §6 (`:1212`) gain:

- The tests commit goes through `integrate.py attest`, and the row's derived set must name each marked file: the file carries a tag to a TC in the row's scope. An unnamed marked file is refused.
- The code commit that removes the marks runs over the same derived set. Change no tag, TC row or `sr_refs` between them; a set that must change is attested with the marks kept first.
- A refresh refused for a mark ends in the code commit or a quarantine.
- A test the bar skips takes no mark, because a skip is never evidence: it is named, with its disposition, in the lane's decisions record.

The step keeps "The code commit removes the marks" and says `[bars] red_mark` declares the mark. `bootstrap.py --dest . --sync` updates the `.claude` and `.agents` copies; the repo has no `.gemini` copy of this skill. `tests/test_prompts.py`'s clause list gains the four clauses, none holding the mark whole.

`project-trajectory/PROCESS.md` §4, DevStg-Impl (`:537`), gains after "(red → green → refactor).": "In a lane, the failing test is proven by the mark `[bars] red_mark` declares, attested before the code and removed by it, and never landed." §-numbering does not move. Run `byte-budget-guard` before and after, re-stamp the PROCESS.md watched row (baseline 100,273) in the skill, keep the skill under its 5,000 cap (4,560 today), and report the delta.

### P10. The flow, the reconcile and the sitting

- `docs/runtime-flows.md`, Flow 4 (`:197`): "then trunk_step, then the check.py bar" gains the mark refusal before the bar, and the heading gains LLR-a. Flow 4's `alt refresh red` branch already describes both outcomes. Flow 1's note at `:91` stays true.
- Reconcile the set against settled code, and fill the trace fields.
- Close the edges as in-lane.md lists them: no `(owed by the tests commit)` left, each amended interface row cited, `check_trajectory.py --strict` and `trace.py --strict` green. Then one combined sitting.

### P11. The records and closing checks

- `docs/decisions/wi-996.toml`: the re-grep of `tests/` for `[bars]` and `stack.ini` writers (D17); the landing consequence with `git worktree list` re-run on that day (D29): every lane cut before this row lands refuses at `attest` until it carries the key, so `wi-902` and any open lane are named; any test the bar skipped and its disposition.
- `git diff --quiet <base> -- project-trajectory/scripts/check_test_first.py`, and `[checks] test_first_since` unchanged (D43).
- The mark count over `tests/` is 0, and `docs/interface-reference.md` shows the key after the refresh (D6).
- Log fragment, Done-when ticks, `run.cmd smoke`, and the full bar in the lane refresh's merge slot.

## Risks the build should watch

- **The C3 fixture sweep.** Decision 9 is a static census. A test reaching the refresh that it missed goes red in the slow suite with `docs/stack.ini [bars] red_mark` in the refusal, so run `test_integrate_station`, `test_integrate_unload`, `test_id_landing`, `test_loop_provenance` and `test_dispatch` before attesting C3.
- **The attest round's cost.** T here is every file tagged to SR-156's scope, plus the new lane module. WI-995's plan measured 34 files for SR-156; I did not re-measure that here. Each attest runs them all.
- **The set must hold still.** A review round's fix commit that adds a TC or a tag after C2 and before C3 changes T. That is decision 12's rule, and the lane's fix commits come after C3 in the cycle.
