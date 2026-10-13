<!-- Independent analysis of the item 11 LLR-fitness question (item-11-llr-interface-check-handoff.md, with plan revision 13), at commit eae8e1cbe (Claude Fable 5.1, medium effort, as a sub-agent given only its brief; read-only; OWNER_SCRATCHPAD.md not read; brief: brief-item11.md). Recorded verbatim; its per-LLR table is item11-classes-fable.csv; the judged synthesis is ../item-11-llr-fitness-report.md. -->

# Item 11 fitness check: will "LLRs carried by interfaces" hold, or cause rework again?

*Independent analysis, Claude Fable 5.1, 2026-10-12, read-only against worktree `C:/Projects/ai-template.wt/item11-fit-fable-m` (commit `eae8e1cbe`) plus the two newer context files. Scratch scripts and intermediate JSON are in `review-tmp/2026-10-12-item11-fit/scratch/`; the per-LLR table is `fable-classes.csv` (302 rows, 45 by hand).*

## 1. The answer

**Counts (method in section 2).**

| Question | Result |
|---|---|
| LLRs whose module(s) own no IF row | **55 of 302** (the plan's figure reproduces exactly under the rule stated below; the prior session's "90 in 64 modules" does not: the nearest reading is 101 LLRs with *at least one* module owning no IF, over 59 such modules) |
| Of those 55, reachable through an existing seam anyway | 8 (for example LLR-147/157/185 are observable at `docs/stage`, IF-050; LLR-021 at the hook exit codes IF-134/135) |
| Of the 55, observable only in a delivered artifact with no IF row today | **33** (21 of them the dashboard `PROJECT_STATE.html`, which has no interface row at all; the rest launchers, generated documents, briefs, record files) |
| Of the 55, CLI entry points that simply never got a seam row | 4 (`check_vocab`, `check_dupes_census`, `dispatch`, plus one shared) |
| Of the 55, kernel or internal decision logic (OI-48 territory) | 8 (LLR-181/184/185/192 in `kitlib`; LLR-149/159/188/073 are pure decision or adapter logic) |
| Of the 55, no observable seam at all | 2 (LLR-050, a retirement record; LLR-197, a code-identity rule) |
| Fitness, all 302: fit as written / reword first / reframe or retire | **83 / 215 / 4** (script proxy for 257, hand for 45) |
| Fitness, the 55 only | 21 / 30 / 4 |
| Fail test 1 (pass/fail undefined in the row; keyword proxy) | 10 of 302 (3 of the 45 hand rows) |
| Fail test 2 (names an implementation symbol or mechanism; token proxy) | **213 of 302** (27 of 45 by hand). This is the same population item 5's census calls "~202 of 302" |
| Fail test 3 (evidence never exercises the seam; regex proxy, in-process-only) | 62 of 302 (18 of 45 by hand; 40 of the 247 that own an IF, 13 of the 55) |

**Verdict.** The owner's worry is confirmed, and it is larger than the 55. Moving an LLR under an interface does nothing to the thing that makes LLRs churn: 213 rows name symbols or narrate mechanism, and 62 are evidenced only in-process. Those defects follow the row to its new interface unchanged. The good news is that almost all of that rewrite is **already owed by ruling 5** (no code in requirement rows), so item 11 adds little new rewording cost; the bad news is that item 11 as proposed (A) adds a new authored relation (IF → LLR, about 300 entries) plus 6–10 new IF rows plus about 150 file headers, and reverses two recorded decisions, to buy one thing: a mechanical blast-radius query. It does not reduce rework by itself. Reword-first (B) is the right ordering but is not a separate design; it is item 5 done before any attach step.

**Recommendation: variant E, "D plus the missing boundary seams".** Keep `Implements:` as the code → LLR trace (it already points up and is checked at the commit). Mint the handful of IF rows the kit is missing for artifacts it actually delivers (the dashboard HTML above all, section 5). Add an authored IF → LLR list **only on IFs that genuinely carry a behaviour**, and derive the SR side through `boundary_refs` and the crossing cells. Make "every LLR reachable from a code-cited seam" a *measured dial* with a closed internal allowance (the `kernel-modules-allow` idiom), never a gate. Fold the three fitness tests into item 5's sitting rubric and its commit-time text check rather than into a migration gate. Section 6 scores this against A–D on the owner's lens.

**Owner calls that remain open** (section 7): whether to mint the dashboard and launcher seams; whether `Implements:` stays (this reverses item 11's call 1, not ruling 5); whether "every LLR carried" is a rule or a dial; what the closed internal allowance looks like; whether the 62 in-process-only evidence sets must re-point to the seam before attachment; and the four retire/reframe rows.

## 2. Method, counts, and how to reproduce them

Scripts (all stdlib, run with `python -I -X utf8` from `scratch/`): `load.py` (shapes), `counts.py` (matching and counts, writes `rows.json`/`counts.json`), `texttests.py` (tests 1–2 proxies), `test3proxy.py` (test 3 proxy), `sample.py <ids>` (extracts evidence test bodies for hand reading), `build_csv.py` (the CSV).

**Matching rule for "owns no IF".** An LLR `module` cell is split on `;` (85 of 302 cells name 2–6 modules). Each entry is normalized: strip the `project-trajectory/` prefix and a `.py` suffix, trailing `/` removed (IF `owner` cells are spelled `scripts/check`; 3 use the long prefix, 0 carry `.py`). An LLR *owns* an IF if **any** of its modules equals an IF `owner` cell exactly. 109 distinct normalized owners; 146 distinct LLR modules, 87 own at least one IF, 59 own none. Result: 55 LLRs own none (CMP-009 26, CMP-008 13, CMP-006 11, CMP-007 5). Changing the rule to "at least one module owns none" gives 101. Counting endpoints as reach (the LLR's module appears in a `requestors`/`consumers` list) leaves 30 LLRs with no IF relation of any kind.

**Other counts.** 243 IF rows, all Drafted, channels call 115 / file 51 / exit-code 36 / cli 22 / stdout 11 / bytes 4 / git 2 / env 2. 316 TCs, 95 list an IF in `verifies`; `docs/if-tc-coverage-allow` waives 217 IF rows from TC coverage; `verified_by` is used on 1 IF row. 230 LLR ids appear in `Implements:` lines; 83 script modules carry a `Contract`/`Contracts` citation; 60 LLRs have no module that cites any IF in code. 26 LLRs name a non-Python shipped file as a module (launchers, hooks, templates, registries, `ci/check.yml`, `PROCESS.md`). 39 LLRs sit on the dashboard renderer family (`gen_trajectory`, `traj_parse`, `rendering/*`, `traj_display`); `gen_trajectory` declares one seam, IF-011 (exit code). `PROJECT_STATE.html` is declared in `docs/stack.ini [generated]` (line 1233) and in no interface row; `docs/open-items.html` (IF-074) and `docs/test/report.html` do have rows.

**Test proxies (script rows).** Test 1: a vague-word regex over title+detail (`correct|appropriate|properly|as expected|sensible|reasonable|suitable|adequate|minimal|right`); 10 hits. Test 2: any snake_case identifier, CamelCase name, `name()` call, `.py` path or markup placeholder in title+detail; 213 hits (91 with the strong forms). Test 3: each evidence test body is classed boundary-level if it matches a subprocess/CLI/file-read pattern (`run_py`, `subprocess`, `gen(`, `html_of(`, `returncode`, `read_text`, `.main([`), in-process otherwise; an LLR fails when no evidence test is boundary-level. 53 in-process-only, 109 mixed, 137 boundary-dominant, 3 unresolved. Script fitness: `reword` on a test 1 or 2 hit, else `fit`; `reframe-or-retire` is assigned only by hand.

**Hand sample.** 45 rows (CMP-009 16, CMP-006 11, CMP-008 11, CMP-007 7), evidence tests read from source, not from the `level` cell. 11 of 45 pass all three tests. The hand sample agrees with the script on test 2 (27/45 vs 213/302 is the same rate) and is harsher on test 3 (18/45) because the regex misses tests that call `load_script(...)` and then assert on module constants (TC-105, TC-108).

## 3. The three tests, corrected

The handoff's tests are the right instrument but two are mis-stated for this kit.

- **Test 1 (decidable in the row) stands.** The keyword list under-counts badly (10 hits), because most undecidable rows are undecidable by *omission* (LLR-032 "runs to a green developer setup", LLR-050 a retirement narrative), not by a vague adjective. Only hand reading finds these. Corrected: "a reader with the row and the seam's contract, and nothing else, can say what would fail."
- **Test 2 ("the user-observable outcome") is wrong for component seams.** A kit LLR on a `call` or `file` seam has no user; its observable is what crosses *that* seam (a return value, a refusal, a file's shape, an exit code). Corrected: "states the outcome observable at the seam the LLR would attach to, not the symbol or mechanism that produces it." Two sub-cases matter for cost: (a) **symbol-only** (the row is behavioural but names `_ring_ink` or `spine_stage`): an item 5 lint edit, mechanical; (b) **mechanism narration** (LLR-147 narrates a deletion; LLR-176 pins which function reads which file): needs judgement. Of the 27 hand test-2 failures, about 10 are symbol-only. Markup and ARIA tokens (LLR-101's `role=img`, LLR-116's `width:100%`) are the artifact's own surface and belong in the IF contract body and the TC, not the LLR.
- **Test 3 ("at the level the user sees it") is wrong for the dashboard.** The kit ships HTML and tests with stdlib; it has no browser and should not. Parsing the delivered document *is* exercising the artifact seam. The handoff's "never by executing a click" is therefore not a defect of TC-089 or TC-104. What *does* fail the corrected test is a TC that asserts the emitter's source or handler text instead of the document: TC-103 (`trail=trail.slice(0,i+1)`), TC-090 (`addEventListener('dblclick'`), TC-057 (asserts `gt.DRILL_SCRIPT` strings), TC-105/TC-108 (palette constants read in-process, never the rendered colours). Corrected: "its evidence drives the seam the LLR attaches to and observes what crosses it."

Where the corrected and original tests differ, the CSV records the corrected result; the original would additionally fail every dashboard row on test 3 (all 21) and pass nothing more.

## 4. The classes, with the rows read by hand

**existing-if (255; 8 of the 55).** The LLR's behaviour is observable at an IF row that exists. Fit examples: LLR-001 (exit 1 under `--strict`, named ids; TC-001 runs `trace.py` as a subprocess), LLR-004, LLR-006, LLR-017, LLR-021 (hook probe, observable at IF-134/135). Reword examples: LLR-147 and LLR-157 (the rung rule is decidable but the rows narrate `sn_gate`'s deletion and name `spine_stage`; the seam is `docs/stage`, IF-050), LLR-201 (the orphan rules are observable in trace's report; the row states "below the engine" and nine symbols; TC-197 calls rule functions directly), LLR-319 (decidable; names `claim_work`, `blackout_at`; TC-338 monkeypatches internals). 191 of 255 fail test 2 by proxy, 40 fail test 3.

**boundary-artifact (33, all in the 55).** Observable only in a file the kit delivers, which has no seam row. The dashboard: 21 rows. Fit: LLR-052, LLR-120, LLR-292 (decidable floors, swept over the emitted SVG). Reword: LLR-087 ("correct ports", test 1), LLR-100 (markup plus handler text in TC-103), LLR-102 (five palette constants; the observable is "no two unrelated concepts share a colour in the document"), LLR-057 (`MAX_TIER_COL`, `mouseleave`; TC pins script source). Fit as written but evidence mis-levelled: LLR-088 (TC-090 asserts handler text). Beyond the dashboard: LLR-164 (the prompt catalogue file; IF-098 is only the call behind it), LLR-193/LLR-326 (launchers; mechanism names, live-run evidence), LLR-071/LLR-176 (the composed briefs), LLR-297/LLR-191 (record files), LLR-190/LLR-311 (CI workflow, shipped docs: fit), LLR-032 (a siting row with no predicate: reframe or retire).

**cli-seam-unregistered (4; a fifth class I added, stated here as a deviation from the brief's four).** A CLI entry point with an observable cli/exit-code seam that was never registered: LLR-169 (`check_vocab`, wired into `check.py`), LLR-195 (`check_dupes_census`, a `[step:]` in `stack.ini`), LLR-143 (`dispatch`, reached through `agent_loop.py`; IF-015 carries the exit codes). These are not OI-48 edges; `trajectory_arch.interface_findings` already warns on them.

**kernel-or-internal-edge (8).** LLR-181/184/185/192 live in the declared kernel (OI-48 (d): edges into it are not seams). LLR-181 is two obligations: package content (a kernel, not a seam) and "arrives whole in a scaffold" (observable at IF-014, bootstrap's output) — split it. LLR-184 (the eight-rung vocabulary as pure data) is observable only as the closed vocabulary `docs/stage` carries; it belongs in IF-050's `data` cell, with the identity test kept as a test. LLR-149/159 (admission table, stable partition) and LLR-188 (gap census read model) are pure decisions whose effect is observable at the claim seam (IF-173) only transitively; attaching them there would claim more than the seam carries. LLR-073 is an adapter between two IFs.

**no-observable-seam (2).** LLR-050 is a retirement record ("no successor function occupies this row"); LLR-197 is a code-structure rule ("re-exported names ARE the kitlib object", verified by `is`). Retire the first; reframe the second's one behavioural clause (case-insensitive Status) onto IF-051's data contract and keep the rest as a test.

## 5. Rework estimate per class

| Class | Item 11 (A) migration cost | Cost of leaving the spine as is |
|---|---|---|
| existing-if (255) | 255 authored IF → LLR entries; 191 rewords (already owed by item 5); ~40 TC re-points if test 3 is enforced; semantic check of each entry (OI-67's "verified by nothing") | item 5 still rewrites 191 rows; blast radius stays file → `Implements:` → LLR → CMP → TC, which already exists |
| boundary-artifact (33) | 6–10 new IF rows (dashboard HTML; agent-resume, dev-setup and run launchers; prompt catalogue and verdict rollup files; composed briefs; evidence and perspective records); 15 rewords (owed); 1 retire; ~5 TC re-points (TC-057/090/103/105/108) | the kit's main human-facing artifact stays outside the seam registry; `trajectory_arch` keeps warning on the renderer family |
| cli-seam-unregistered (4) | 3 seam rows, each a `Contract` body in the module header (owed anyway by the connectivity warn) | the warn persists |
| kernel-or-internal-edge (8) | no `call` seams (OI-48); 2 splits, 1 fold into IF-050's data cell; a closed internal allowance for 4 | nothing |
| no-observable-seam (2) | 1 retire, 1 reframe | two rows nobody can falsify |

Net: item 11's *own* rework over the 55 is about ten IF rows, a dozen TC re-points, four retire/reframe acts and the allowance; everything else is item 5's. The new standing cost is the authored IF → LLR relation (about 300 cells) and, under A, about 150 component headers.

## 6. Alternatives on the owner's lens

Scored on (a) one-time migration, (b) authored links to keep true and what breaks them, (c) orientation value, (d) behaviour divorced from implementation.

**A. Item 11 as proposed.** (a) Large: retire ~929 `Implements:` lines (230 LLR ids), author ~300 IF → LLR entries, ~150 file headers, 6–10 IF rows, rewrite `gen_arch_map`/`trajectory_arch`/the strict body gate for symbol-level citations, re-found the LLR floor, retire SR-180/LLR-180/TC-175, overrule OI-67 and the 2026-09-23 `realizes` rejection. (b) ~300 list entries break on LLR re-mint or IF split; ~150 headers break on a file move across components (a wanted signal); citations break on symbol moves. (c) High: one place answers "what does this seam promise and to whom". (d) Good for LLRs, but the trace becomes coarse reachability (two functions citing one IF carrying LLR-A and LLR-B attribute both to both) and the minimum profile has no path from code to any LLR.

**B. Reword first, then attach.** Same end state as A; the gate is "each LLR passes the corrected tests before it moves". (a) A's cost plus an explicit per-row gate; but the rewording is item 5's work, so B is an ordering, not a design. (b)–(d) as A. B is strictly better than A and is what item 5's sequencing already implies.

**C. Boundary-artifact variant.** A, but LLRs observable only in a delivered artifact attach to one IF for that artifact; no `call` seams for internals. (a) Smaller than A by the seams it refuses to mint, which is the right call under OI-48; 21 dashboard rows ride one row. (b) Fewer rows, same list. (c) Better than A for a reader: "the dashboard as delivered promises X" is the orientation the rubric anchors (A2, T3, U5) already give. (d) As A. C should be part of any answer, but it leaves A's `Implements:` retirement and header costs in place.

**D. Minimal change.** Keep code → LLR (`Implements:`), add IF → LLR only where an IF genuinely carries the behaviour, require no interface per LLR. (a) Smallest: the IF → LLR cells on the subset (my estimate 100–150, the boundary and cli seams plus the IFs whose `data` cell already states an obligation), no header migration, no grammar rewrite, no ruling reversed except OI-67's column removal. (b) Fewest new links; `Implements:` breaks only on LLR retire, which is the signal wanted. (c) Lower than A: a reader still has two hops (IF → LLR → `Implements:`) to find code, but that hop is generated. (d) Equal to A for the LLR text (that is item 5's doing), better for the trace (function-level kept).

**E. Recommended: D plus the missing boundary seams and a measured reach dial.** D, plus: mint the boundary-artifact and cli seams of section 5 (these are owed by the kit's own connectivity warn and by the fact that the dashboard is unregistered); add the IF → LLR list on carrying IFs only, SR side derived (the revision 13 point); report "LLRs reachable from a code-cited seam" as a dial beside `backlink_coverage_min`, with a closed `internal` allowance in the `kernel-modules-allow` idiom (one line, one reason) for the kernel and pure-decision rows; fold the three corrected tests into the `spine-authoring` K2 questions and item 5's commit-time text check (symbol tokens) so an LLR can never again be attached, or approved, naming mechanism. Blast radius is then file → `Implements:` → LLR → (CMP tag, IF → LLR inverse) → TC, all derived, with no new header grammar. What E gives up against A: a single authored code → IF direction (the kit keeps two up-pointers, `Implements:` and `Contract`), and the component declared on the file. The second is cheap to add later if the derived map proves wrong; the first is the price of keeping function-level trace and the minimum profile working.

## 7. Owner calls left open

1. **Mint the dashboard HTML seam** (owner `scripts/gen_trajectory`, channel `file`, consumers the human operator / `external:downstream adopter`, contract: the bounds the rubric anchors state), and the launcher, generated-document, brief and record seams of section 5? Without the first, 21 LLRs have no honest interface under any variant.
2. **`Implements:` stays (E/D) or retires (A)?** Retiring amends ruling 5's "code blocks reference up to their requirements" and needs the minimum-profile rule; keeping it leaves two up-pointers in code.
3. **"Every LLR carried by an interface": rule or dial?** As a rule it forces either OI-48-class seams or the retirement of decision-logic rows (LLR-149/159/188) that are real obligations; as a dial with a closed allowance it costs one file.
4. **Test 3 enforcement.** Must the 62 in-process-only evidence sets (40 on existing IFs) re-point to the seam before their LLR is attached, or is attachment allowed on the LLR text alone with the TC fixed as found? The hand sample says the handler-text pins (TC-057/090/103) are the ones that will reopen rows on a refactor; the constant-reading ones (TC-105/108) are harmless until the palette moves.
5. **The four retire/reframe rows:** LLR-050 (retire), LLR-032 (retire or restate with a predicate of its own; TC-032 already verifies SR-032 directly, and LLR-326 states the Windows half), LLR-184 (fold into IF-050's data cell), LLR-197 (reframe the Status-casing clause onto IF-051, keep the identity rule as a test). Each is an Approved row, so one batch act.
6. **Which test-2 failures item 5's lint owns.** Symbol tokens are mechanical (lint); mechanism narration is the sitting's. Confirm that split, or the 213 count becomes 213 sittings.

## 8. Design smells noticed (separate findings, not fixed)

- `PROJECT_STATE.html`, the kit's principal human-facing artifact, has no interface row; `docs/open-items.html` and `docs/test/report.html` do. `gen_trajectory` declares only IF-011, and the whole `rendering/` package is invisible to the seam registry because the `Contracts:` grammar is module-header-only and the facade holds the header.
- `docs/if-tc-coverage-allow` waives 217 of 243 IF rows from TC coverage; "95 TCs list an IF" overstates how far interfaces are verified today. Any IF → LLR list inherits that gap.
- `trace.py --strict` is red on LLR-292 for the word "minimal" inside "no claim is made that crossing count is minimal", a non-claim. Item 6's "fix LLR-292" would reword a correct sentence to satisfy a keyword lint; the lint should see negation or the sentence should be allowed by marker.
- History and retirement narratives live in requirement cells (LLR-050 whole; LLR-147 and LLR-157 in part), against the pattern the IF registry header enforces for its own `rationale` ("the argument, never the citation").
- `check_vocab` and `check_dupes_census` are wired into the gate (`check.py`, `stack.ini [step:dupes-census]`) yet own no seam; OI-48's text lists them as a "tolerated family". `dispatch` is a requestor on 15 IFs and owns none.
- 85 LLR `module` cells name several modules (up to six); for those the function-level trace is already coarse, which weakens the granularity argument on both sides of call 1.
- OI-42's and OI-67's `ruling_ref` cells point at `docs/log.d/` files that no longer exist (already noted in revision 13; still true at `eae8e1cbe`).

## 9. Claims in the handoff, checked

| Claim | Result |
|---|---|
| 55 of 302 LLRs sit in modules that own no IF | Confirmed under the rule in section 2 |
| A rough owner-path match gave 90 in 64 modules | Not reproduced; 101 LLRs / 59 modules under "any module owns none"; the 90/64 figure has no rule that yields it here |
| LLR-087's "correct" is undefined; TC-089 holds the meaning | Confirmed (`tests/test_traj_views.py::test_when_view_seams_wire_to_block_ports`) |
| LLR-100 names markup; TC-103 asserts handler text while `expected` states the outcome | Confirmed |
| LLR-101 is behavioural with a scope limit; TC-104 avoids pinning the implementation | Confirmed, and TC-104 also walks the shipped artifact |
| All three verify the dashboard by parsing markup, never a click | Confirmed as fact; not a defect under the corrected test 3 |
| No boundary-artifact IF for the dashboard exists; check the "Non-code realizations" nuance | Confirmed none exists; the nuance covers headers on shipped files, not a generated artifact as a seam, so it does not cover this |
| OI-48 declined an IF per helper edge | Confirmed (recommendation text; ruled (d) 2026-08-21, generalised to the declared kernel list) |
| LLR fields include `test_refs` | Present on 244 of 302 rows only |
