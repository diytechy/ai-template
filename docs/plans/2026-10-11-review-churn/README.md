# Review Churn Plan

*ai-template · 2026-10-11 · evidence window 2026-10-09 → 10-11 (21 WIs, 69 review rounds, 79 findings) · for the owner to confirm or overrule item by item*

**Status:** revision 17. Items 1–10 are ruled (see "Owner rulings, 2026-10-11"; the revision 6–7 clarifications not marked as rulings await the owner's confirm or overrule). Item 11 (what points where) is open; its terms (contract, module) and its two owner's queries (revision 11: contracts cited only where served; work items bound to the interfaces they serve) are the owner's. Revision 12 adds the open calls a GPT-6 Astra review of revision 11 raised (item 11's open calls, and "Open after revision 12" in the rulings section). Revision 13 adds those a Claude Fable 5.1 review of revision 12 raised, among them item 11's overlap with OI-112. Revision 14 answers the owner's follow-up on item 11 (are the LLRs fit to be carried by interfaces?): two independent analyses, GPT-6 Astra and Claude Fable 5.1 at medium effort, judged in [`item-11-llr-fitness-report.md`](item-11-llr-fitness-report.md). Both find that item 11 as proposed would not reduce rework, and both recommend a narrower variant E, with new owner calls. Revision 15 records the owner's refinement of E as variant F in item 11. It also loosens item 7's reviewer-family rule and withdraws item 5's per-module `Implements:` floor (both owner positions). It adds item 12 (architectural decomposition at three moments: a fresh-vision breakdown, an amendment that shifts the architecture, and an audit), at the owner's request, and item 13 (review only a green tip; test cases reviewed in stages). Revision 16 answers a GPT-6 Astra and a Claude Fable 5.1 review of revision 15 (both medium effort, both REVISE): F corrected in place, two new F-calls (8, 9), items 12 and 13 corrected; dispositions at the end. Revision 17 records the owner's answers to F-calls 8 (not required; placement derived through the verifying test's interface), 9 (the code's contract body) and 2 (not every file; the builder may mint files but must not duplicate), and to interactive dashboard evidence (executed, off the commit bar). It adds item 13's build bound (about three red rounds, then the adjudicator), the owner's positions on item 13's gate and TC order with the evidence found, a stamp of each dashboard view's last check, and the owner's position on in-lane dependency installs, plus the integrator's recommendation of option (i) for F-call 1. It withdraws the integrator's note that interface-owning files must be stubbed at design time: the contract has one home at a time, which the owner confirms. It maps what points at a component, where F-call 1 is the one open link, and records the owner's scoped test set for the gate and the mutation trial. The owner confirms F-call 1 (i), the mutation trial and the TC-first split; the in-lane dependency admission shape is proposed for confirmation.

The churn is real but concentrated: four WIs (WI-834, WI-902, WI-887, WI-881) took 41 of the 69 review rounds in the window. Adjudication upheld most contested findings, so the reviewer is not the problem. What keeps rounds coming is the shape of the work. Specs promise behaviour over open-ended inputs, and every fresh review samples a new corner. Advice about that from earlier reviews never becomes binding. Facts get re-derived from git history. And requirement rows restate code and drift with every fix.

Revision 2, after two independent reviews (Claude Sonnet 5.5 and Codex 6.1 Sol, same brief, against commit 85a37767a). Both returned REVISE; every finding was checked against the repo, and the dispositions are in the last section. The reviews themselves are in [`reviews/`](reviews/) beside this file. Revision 3 (owner direction, same day): item 4 becomes the review settings, item 6 shrinks to the hook change, and item 10 is added. Revision 4 records the owner's ruling on item 10 after a read-only investigation of both configuration files. Revision 5 records the owner's rulings on every open call (next section). Revision 6 answers an independent GPT-6 Astra review of revisions 3–5, and revision 7 a Claude Fable 5.1 review of revision 6 (dispositions at the end). Revision 8 records the owner's rulings on the three questions revision 7 raised. Revision 9 adds item 11 (what points where), from a read-only trace of how the interface, component and code links got their shape; its calls are open. Revision 10 adds the owner's definitions of contract and module to it. Revision 11 adds the owner's two queries and the two decomposition readings to item 11. Revision 12 answers a GPT-6 Astra review (low effort) of revision 11, and revision 13 a Claude Fable 5.1 review (medium effort) of revision 12 (dispositions at the end).

| # | Change | Kind | Cost | Aims at |
|---|---|---|---|---|
| 1 | Closed coverage, made binding: deny-by-default construction for unbounded syntax, an enumerated allow-set in the spec, and the reviewer classifying fail-open vs fail-closed | ruling + rubric | hours | the largest class: open input spaces re-sampled every round (WI-834's gate findings 016, 024, 028) |
| 6 | Run the strict lints after every build (commit bar, closure check, landing check; not the commit hook): fix LLR-292, add a RESYNC-presence check | small build | ~1 lane | findings an instrument would catch (~6 in the sample) |
| 8 | Record usage for every model call, under WI-800's invocation ledger: Sol and Terra through the session service, sub-agents from transcripts, deduplicated | small build | ~1 lane | ~74% of a leg's Claude output (builders) is unrecorded; makes every trial measurable |
| 2 | Record a decision at its event, validated by a commit-vs-parent check; never re-derive it from history. Reshape WI-902 first | ruling, then WI-902 reshape | 1 spec amendment | WI-902's history-replay findings |
| 9 | A planning need decided at mint; plan and scope advice becomes spec text before the claim; one planning path shared with WI-805 | ruling + ordering | hours, then one critique per planned row | advice that never binds (WI-834's pre-build reviews already asked for an enumerated list) |
| 4 | Review settings: reviewers and rounds per WI (ruled 0 / 0 / 2 / 3), an adjudicated exit at the cap, MINORs never cost a round, a convergence final round, severity tied to reachability | ruling + template change | 1 lane + migration | unbounded rounds (WI-834: 20); ad hoc breakers (WI-902); stale checkpoints |
| 7 | A second reviewer from a third family (Gemini) when available, otherwise a different family or model from the first, at the full reviews; the coordinator cycle reads item 4's `full_reviewers` | ruling + trial | waits on WI-815's route | earlier discovery, on a separate quota |
| 3 | Split at birth on independent deliverables, for containment; no size threshold (the data doesn't support one) | ruling | none | one stuck subsystem holding the rest |
| 10 | One configuration file in TOML (owner ruling 2026-10-11): `stack.ini`, routes and consent move into `process.toml`; adopter-owned values, kit-owned schema; re-sync adds, never replaces | ruled · 4–6 WIs | before the FileBackup re-sync | 13 separate parsers; routing in three homes; a re-sync that overwrites adopter values |
| 11 | What points where (open): code cites only interfaces; interfaces name the requirements they carry; files declare their component; LLR → component checked or derived. Revision 14 recommends variant E: keep `Implements:`, IF → LLR only on carrying interfaces, mint the missing delivered-artifact seams. Revision 15 adds the owner's variant F: components declared on the realization, no IF → LLR list, thin interfaces | open calls | folds into item 5's migration | the last mixed-direction links; mechanical blast radius per component |
| 12 | Architectural decomposition at three moments (open): one rubric and an `architecture-decomposition` skill, reached from a fresh-vision breakdown, the planner's architectural-delta question (handback when beyond scope) and an on-demand `run.cmd arch-audit`; dry-run on W3 first | text, then builds | ~1 lane of text; builds after item 11 | under-decomposed components (W3: 60 modules, the lane's stages inside) |
| 13 | Review only a green tip (open): lint, then tests, then review; nothing refuses a red-tip review today. Test cases reviewed in stages: written first with recorded red-before, mechanically at the gate, for adequacy by the reviewers, as text at the sitting; a mutation trial later | text + a small build | after item 6 | reviews spent on failures a tool would catch; weak tests that pass |
| 5 | Requirements never reference code; code points up (owner ruling 2026-10-11): schema, commit-time text check, contract voice, semantic trace check kept | ruled · 1–2 WIs, last | schema WI + migration | requirement churn from code moves |

Order is cheapest-and-surest first. Counting bases differ, so each figure names its source. The window counts (21 WIs, 69 rounds, 79 findings, and the late-finding taxonomy: 43 late findings, 18 from open input spaces, ~24 spine-text, ~6 mechanical) come from one analysis pass and have not been reproduced. Sol's reproducible added-file window gives 19 WIs, 65 REVIEW-A files and 74 verdict findings. A manifest of included files and per-finding classes is owed before any of these become a baseline (sequence, phase 0). The size table comes from `rows.json` and was reproduced by both reviewers.

## Owner rulings, 2026-10-11

Ruled in session, item by item. Where an item's text below differs, this section governs.

| # | Ruling |
|---|---|
| 1 | **Confirmed:** construction-first and binding. For an unbounded grammar the spec chooses deny-by-default (an enumerated allow-set plus a declared rule for everything else). Scope critique gains S3, and its answer becomes spec text before the claim. **Confirmed:** the reviewer, not the list's author, classifies an out-of-set input: fail-closed → a coverage-extension note; fail-open → a blocking finding. |
| 2 | **Confirmed:** reshape WI-902 to record-at-close before resuming. The close validates the adoption once, records it in the closing commit, and a check against the parent validates it; the sweep trusts the record. Its Trust ruling (D-005) is re-sat on the new shape. **Confirmed:** the record-at-event rule goes into `PROCESS.md` §3, with the scope-critique bad example. |
| 3 | **Confirmed:** S1 is the only split rule (independent deliverables with recorded dependencies, unless the owner keeps them together). No size threshold. Batching tiny rows was not adopted. |
| 4 | **Confirmed** `[review]`: `iteration_reviewers = 0`, `iteration_rounds_max = 0`, `full_reviewers = 2`, `full_rounds_max = 3`; `on_limit = "adjudicate"`; `block_on = ["BLOCKER", "MAJOR"]`; the last allowed round runs in convergence mode; severity is tied to reachability. Reviewers always receive the WI definition (spec, Done-when, Trust, touched rows) and never the builder's coverage plan. |
| 5 | **Refined and confirmed:** no implementation carrier (code file, function, symbol) in any requirement row. Shipped boundary artifacts (registries, templates, config, launchers) may be named at LLR and TC only. SN and SR rows name no file in any cell, rationale included (18–23 rows to reword, depending on the pattern counted). The commit-time check derives the boundary set from the shipped-file inventory minus code. **Confirmed:** IF and CMP rows name no code; functions cite their interfaces (the existing `Contract IF-NNN` docstrings); LLRs keep naming their component by id; file and module maps are generated. **Confirmed:** the judging split (the sitting judges wording and overlap; the code reviewer keeps code-versus-row correspondence, omissions included). |
| 6 | **Confirmed, not in the hook:** `trace.py --strict` and `check_trajectory --strict` run in the commit-bar command after each build round, in the closure check before a sitting, and in the landing check. Fix LLR-292; build the RESYNC-presence check. Commits stay light. |
| 7 | **Confirmed:** a Gemini reviewer B once WI-815's route works and one launch is verified. Until then, **Claude Sonnet** is the second reviewer, recorded as a stand-in substitution in each lane's decisions. |
| 8 | **Confirmed:** Sol and Terra launch through the session service, and sub-agent usage is ingested under WI-800's ledger contract (counted once per message, each invocation attributed exactly once), pulling that part forward. |
| 9 | **Confirmed:** every pre-claim recommendation gets an explicit disposition (adopted, quoting the carrying spec text, or rejected with a reason), and a fresh critique round confirms adopted ones are in the spec in the recommended shape before the claim. **Confirmed:** S4 decides `planmode` on the stated criteria. **Confirmed:** pull WI-805's plan gate forward. **Ruled:** fix dual-plan pickup as is (WI-813), arbiter kept. |
| 10 | **Ruled** (revision 4): one TOML file. **Confirmed:** keep the name `docs/process.toml`. **Not objected:** since WI-880 all three hooks refuse without Python 3.11+, so the shell grep and the one-key-per-line shape rule (SR-137) can go. The remaining shell reads (the missing-scripts-directory refusal, the mixed-config refusal, and the legacy `docs/privacy-check` read that retires with WI-817's window) become one `tomllib` read in `kit-python.sh`, after the interpreter check. |

**Revision 6–8 clarifications, after the Astra and Fable reviews (revision 8 entries are owner rulings; the rest are for the owner to confirm or overrule):**

- **Where the checkpoint sits (item 4; revised in revision 7).** `full_rounds_max = 3` caps the full rounds *before* the checkpoint. Rounds run until one has no BLOCKER or MAJOR code finding; the checkpoint (Terra reconcile, closure check, sitting) follows it. The gate over the checkpoint tip, and a round over a rebase that changed code or rows, always run, in convergence stance, and are not counted, so the tip that lands is always reviewed. If the cap is reached with findings open, `on_limit` fires.
- **A convergence-class defect is never deferred.** At the cap or at the gate, a fail-open, data-loss or Done-when-gap finding is never ruled FIX-as-successor: the sitting orders one more fix round or ESCALATEs to the owner. Other findings may become successors.
- **The convergence round never sees earlier verdicts** (owner ruling, revision 8). Showing a reviewer prior conclusions anchors it, and the kit already records that, both measured and cited (see item 4). A fix is confirmed by its regression test instead: every accepted finding carries a test that fails on the pre-fix code. Before the round, the coordinator checks that each accepted finding maps to such a test. (Revision 12: the reviewer template today verifies pre-fix failure only *where the diff adds* a regression test, so the per-finding rule is new template text. A wording, documentation or inspection defect has no executable test; what evidence confirms its fix is open, below.) `review_brief.py`'s rule that "a full-lane round is fresh" stays as is.
- **Successor rows** a sitting rules are filed on trunk at the landing, from the sitting's binding: a work branch never mints a WI id.
- **No consent means no managed loop (item 10; owner ruling, revision 8).** Today an absent or empty `agents-enabled` does not error: it silently falls back to the single-model `AGENT_CMD` / `[agent-loop]` path ("routing off"). Once `[agent-loop]` retires, that fallback goes, and the loop refuses to launch with an empty pool, naming the setting. A one-model setup is a pool of one route, and the template ships empty.
- **IF rows join layer 1 (item 5).** Their `owner`, `consumers` and `requestors` cells (203 of 243 owners are `scripts/…`) leave the schema and are generated from the code's `Contract IF-NNN` citations. (Revision 12: an untyped citation can't say which role a citing file plays. IF-175 has one owner and six requestors; IF-032's owner is `external:git` and only its consumer is local code. How the roles and external owners are declared is open, below.) Depending on the pattern counted, about 204–229 distinct interface ids are cited from code, so roughly 14–39 internal rows need a citation added, or the row retired, first. The 46 external crossings name their external party by id, not code. All IF rows are Drafted, so no batch act is needed.
- **The third shell read.** Besides the missing-scripts-directory refusal and the mixed-config refusal, the hooks read the legacy `docs/privacy-check` file in shell. It retires with WI-817's legacy window, which item 10 folds in. The shared `tomllib` read lives once, in `kit-python.sh` beside the interpreter probe, not in three hook copies.
- **Test files name their TC; TC rows name no test files or modules** (owner ruling, revision 8). It is the same up-pointing direction as code naming its LLR, so a module or test rename never reopens a TC row. The TC rows' test-file `evidence` column (test files named in 314 of 316 rows today) becomes generated from tags in the test files. Today 101–107 of 237 test files mention a TC id, depending on the pattern, covering 129 of 316 TCs; the rest need a tag added in their test file before the column can be generated. TC rows may still name shipped boundary files. (Revision 12: not every TC's evidence is a test file. TC-035 names the CI workflow, TC-209 an inspection record, and 185 evidence cells name a test node with `::`. How non-test evidence and node identity survive is open, below.)
- **Lanes already in flight** (WI-798, WI-902) start the count at zero at their next review under the new shape. The coordinator records that as a decision.
- **Session budget (item 4).** In the lane: up to three counted rounds plus the post-checkpoint gate, so eight review sessions in the ordinary case (four Codex, four Sonnet or Gemini), plus a dispute sitting at the cap. It is not a hard bound (revision 12): an extra fix round a convergence-class finding forces, and an uncounted round over a rebase that changed code or rows, each add two sessions. Before the claim: the scope critique and its disposition re-check (two Codex sessions), and one plan critique for a row S4 marks `single`.
- **IF rows name no files (item 5).** The ruling allows shipped boundary files at LLR and TC only, so interface rows use component and interface ids and artifact-class wording. The owner's earlier remark that interface definitions can label files tied back to assumption rows is kept as an open question, not an allowance.
- **The boundary-file set is an explicit classification.** The shipped-file inventory records source, destination and reference, not a boundary class. Subtracting "code" by directory or suffix would wrongly drop the launchers (which ship from `scripts/run.template.*`), and excluding only Python would admit other scripts. So the one inventory gains an explicit `boundary` class on each entry, matched on the destination path. That is a closed allowance, with no second list.
- **The planning gate comes before rows that need it (item 9).** Once S4 exists, a row it marks `single` waits for WI-805's pulled-forward plan gate. The gate's own row is built without the gate (it cannot plan itself), and that is recorded. The handoff's batch is ordered so.
- **`agents-enabled` as a setting (item 10).** The file is an ordered pool of route ids with per-phase draw weights and strict validation (`agent_route.py`), not a toggle. Its setting keeps exactly that: an ordered TOML array of tables, each an `id` with optional per-phase weights, validated as today. An absent or empty pool grants no managed-routing consent.

**Open after revision 12 (Astra review of revision 11; for the owner to rule):**

- **Confirming a non-executable fix.** The convergence ruling confirms fixes by a test that fails on the pre-fix code. A wording, documentation or inspection defect has none. Does it carry independently checkable evidence instead (the corrected text, an inspection record), which the coordinator maps the same way?
- **Generating IF roles.** (Revision 15: narrowed by item 11's variant F; see its status table.) If the IF `owner`, `consumers` and `requestors` cells are generated from code, the citation must carry the role (owner, consumer, requestor), and an external owner (`external:git`) has no code to cite. Is the role a typed citation (`Contract IF-NNN` for the owner, a consumer form for the rest), with external owners kept as an authored id cell?
- **TC evidence that isn't a test file.** Test-file tags can generate test evidence, but not CI results, inspection records or reviews, nor the 185 `::` node references. Do those stay authored in the TC row (CI configs and inspection records are boundary files), with only test-file evidence generated?

**Open after revision 13 (Fable review of revision 12; for the owner to rule):**

- **Item 11 and OI-112 are one question.** (Revision 15: answered by variant F; see item 11's status table.) OI-112 (pending since 2026-10-08, its WI-871 held) asks how far IF rows join the adjudicated spine: (a) route IF rows through the first-approval sitting; (b) each SR names the IF rows carrying its inputs and outputs. Its (b) points SR → IF; item 11 points IF → requirement. Ruling both separately would give the relation two homes. Does an item 11 ruling also answer OI-112, with one direction, or does item 11's calls 2 and 5 fold into OI-112's design pass?
- **Items 11 and 5 overlap.** (Revision 15: narrowed by variant F to the LLR → CMP reversal; see item 11's status table.) Ruling 5 says code references up to its requirements and LLRs keep naming their component. Item 11's call 1 (retire `Implements:`) and call 4's "derived" option would amend that wording: a reversal, not an extension.

Also ruled: coordination of the build runs interactively in this session, with Sol plus the Sonnet stand-in reviewing each change in parallel, in the shape item 4 sets.

## The owner's two questions

### Narrow rounds and the full gate: what's actually different?

Yes, a narrow round's reading scope is restricted to the diff since the last reviewed commit. But less separates the two than revision 1 claimed:

|  | Narrow round | Full-lane gate |
|---|---|---|
| Reading scope | `git diff <last reviewed>...<tip>`: the template's `{trunk}` slot is filled with the round's base (`review_brief.py:309`) | The whole lane from its trunk base to its tip, code and rows together |
| Instructions | The shared reviewer template (find the failure classes, "an APPROVE must mean you tried to break it", map Done-when items, name each changed side's counterparts), *plus* a range line: confirm each fix at its own site and try one other site of the same class (`agent_brief.narrow_scope_line`) | The same template, with the full range |
| Session | Fresh `codex exec` | Fresh `codex exec` (`final_reviewer = "fresh"`, `docs/process.toml:311`) |

Both briefs carry the Done-when and break-it instructions. A narrow range just can't satisfy them for code outside the delta. Narrow rounds do catch regressions: narrow round 030 caught a WI-834 fix that newly denied a valid command.

So what did the full reviews find right after a narrow approval? In WI-834, narrow approvals 010, 014, 020/022, 026, 034 and 037 were each followed by a full review with findings (012, 016, 024, 028, 035, 039), 9 in all:

- **016, 024, 028:** new shell forms the blackout hook let through (`$r = claude`, `. claude`, `time -p claude`). These are fresh samples of an open input space, not something the narrow scope hid.
- **039:** an over-denial (a PowerShell function definition), a side effect of the growing parser.
- **012:** an interpreter mismatch in a different subsystem (dev-setup readiness), a genuine new defect.
- **035:** two minors.

The narrow-then-gate surprise in WI-834 was therefore mostly the open input space (item 1), not a blind spot of narrow scope. One cost is real regardless: every narrow APPROVE triggers a checkpoint (Terra reconcile, closure check, sitting), and when the gate reopens the lane that checkpoint was wasted. Item 4's review settings address that: no narrow rounds, one checkpoint after the last full round, a cap with an adjudicated exit, and a convergence final round, which keeps full rounds from re-sampling an open space indefinitely. Item 1 still comes first.

### Does splitting a WI actually help, or just move the work around?

Your intuition holds: splitting by itself buys little. The data shows no size threshold where cost takes off, only overhead that each extra WI pays again, plus two confounded outliers.

Data: 38 code-changing WIs claimed and landed 2026-10-03 → 10-11 (`rows.json`). "Code lines" is gross lines added plus deleted under the scripts and tests, not net product code. "Sittings" counts adjudication files. "Gap-filtered hours" is claim-to-landing time minus every gap over 2 h between lane commits. That removes nights and rate-limit waits, but also removes long stretches of work without a commit, so it is not a measure of active labour.

| Code lines changed | WIs | Median rounds | Median sittings | Median gap-filtered h | per 100 lines |
|---|---|---|---|---|---|
| 1–299 | 16 | 2 | 1 | 1.15 | 1.19 |
| 300–999 | 6 | 2 | 3 | 1.2 | 0.16 |
| 1,000–2,999 | 14 | 4 | 4.5 | 3.45 | 0.27 |
| 3,000+ (WI-841, WI-834) | 2 | 19 | 16 | 12.8 | 0.30 |

- **Each WI carries overhead.** The nine smallest code WIs (under 120 lines) have a median near 1 h, 2 rounds and 1 sitting, with real spread: WI-901 took 0.3 h with no sitting, and WI-860 had four sittings. Splitting a small or medium row multiplies that overhead.
- **No threshold is visible.** WI-818 (2,041 lines, 5 rounds), WI-822 (2,552, 4) and WI-790 (2,873, 3) are ordinary. Only the two rows over 3,000 lines blew up, and both are confounded. WI-841 ran before narrow rounds existed. WI-834's churn was mostly an open input space, which item 1 addresses at any size. Two rows cannot establish a threshold or a savings figure, so revision 1's "15–25% saved" arithmetic is withdrawn.
- **What holds is containment.** In one lane, a finding in one subsystem holds every subsystem, and nothing lands until all are clean. Separate lanes land independently. That is a reason to split *independent deliverables*, whatever their size, and no reason to split a coherent one.

## 1. Closed coverage, made binding

**Evidence.** Every reviewer-run full review after a WI-834 narrow approval found new members of an open input space (016, 024, 028: allowed shell forms). The builder asked mid-lane for "a closed, declared list … so this class stops reopening one form per round" (`docs/reviews/wi-834/025-DISPUTE-findings.toml:18`). The churn ended only once dispute sittings drew that line (ruling 025 put script wrappers outside the hook's coverage by an owner-level choice; ruling 040 accepted a specific over-denial after weighing its cost). The idea wasn't new. WI-834's first pre-build Sol review (`docs/reviews/wi-834-plan/001-sol-plan-review.md:29`) had already said to "enumerate the supported direct shell forms and require script wrappers to use the guarded service". The analysis pass also counts store-record shapes in WI-887, history edge cases in WI-902 and an ambient credential source in WI-798 in this class, for 18 of 43 late findings; that taxonomy is unreproduced.

**Root cause.** A spec promises behaviour over an unbounded set (any command form, every failed-write shape). The reviewer brief demands an attempt to break it, and each review is a fresh session, so every round samples a new member. Each finding is valid; the set is the bug. Advice to bound the set exists but is advisory: it doesn't become spec text the build and the reviewers are held to.

### Proposal

1. **For unbounded syntax, construction first.** Where the input space is a grammar (shell lines, free-form text), the spec chooses a deny-by-default construction: an enumerated allow-set of guarded forms, and a declared rule for everything else (denied, or outside coverage by an owner-level choice, as ruling 025 did for wrappers). No promise over the open grammar itself.
2. **Scope critique gains anchor S3, "Coverage is closed"** (`docs/rubrics/scope-critique.md`). Any promise over an input space is either an enumerated set with a declared default, or a construction that makes the space irrelevant (deny by default, or validate a whole record against one schema). The critique's answer becomes spec text before the claim, in the Done-when or the Trust section. That is the step WI-834 lacked.
3. **Consolidate shape validation, keep each consumer's policy.** Every consumer of a carrier reads it through one owning parser that accepts exactly the well-formed shape. Each consumer keeps its own authority, binding and refusal policy: the close, the review scheduler, historical readers and the mint legitimately differ, as WI-902's Trust section shows. The parser removes duplicated parsing, not those decisions.
4. **The reviewer classifies, not the author.** An input outside the spec's declared set that the change fails *closed* on is filed as a `coverage-extension` note (spine change list or a successor row). One it fails *open* on stays a finding at full severity. The reviewer, independent of whoever wrote the list, decides which it is (`reviewer.template.md`, shipped).
5. **WI-834's parser: investigate before proposing anything.** A "deny any line that mentions a model CLI" rule would not cover wrapper launches, which carry no CLI name in the submitted line (ruling 025). It would also over-deny broadly in this repo, where `claude` appears in paths and skill names. Read WI-834's original rationale and count recent coordinator commands that would have been denied, before filing any row.

**Trade-off.** A closed set can miss a real form. Deny-by-default turns that miss into an over-refusal, not a hole, and a successor row extends the set on purpose.

**Measure.** Late findings from open input spaces, per landed WI, counted under the phase-0 manifest. No numeric target until that baseline exists.

**Downstream.** Step 4 changes a shipped template: one `RESYNC_PACK.md` entry, no migration. Steps 1–3 are this-repo rubric and procedure.

**Owner calls (ruled; the rulings section governs):**

- Confirm or overrule construction-first for unbounded syntax.
- Confirm or overrule S3, with the critique's answer becoming spec text before the claim.
- Confirm or overrule the reviewer classifying fail-open vs fail-closed.

## 2. Record the decision at its event, checked at the commit

**Evidence.** WI-902 lets a disposition name an existing successor. Its sweep "reads the open-state rule in the tree of the commit that landed the disposition (the oldest first-parent commit touching its spec in `complete/`)", added by review 001 F1, review 008 F1 and ruling 009. That history read then drew shallow-clone, lossy-decode and file-existence findings. The lane stopped under the two-round breaker after 9 rounds.

**Root cause.** The close and the sweep each re-validate the same adoption, and the sweep re-validates it on every run against whatever trunk is now. When that answer drifted (the successor completes later), the fix replayed history to recover the original answer. Your 2026-10-03 rule forbids exactly this: enforce at the commit, not through git-history archaeology.

### Proposal

1. **Reshape WI-902 before resuming it**, as a spec amendment with a scope critique, not another build round. The close validates the adoption (the named row is open and supersedes the disposed row) and records the result in the commit that closes the row, e.g. an `adopted = "WI-893"` cell. A commit-time check of that closing commit against its parent re-runs the same validation and refuses an invalid close. The record is the validated event's result, not a marker anyone can write. The sweep trusts the cell and never consults later trunk state or history. A disposition that lacks the cell where one is owed refuses the sweep; there is no fallback to re-deriving. A cell written by hand or by an agent outside the close fails the commit check, since agent-written repo content is in scope.
2. **State the rule once** in `PROCESS.md` §3, beside "When a guard is owed": a decision a later step depends on is recorded by the step that makes it, in the commit where it is made, and checked against that commit's parent. A later reader trusts the record and never recomputes it from history. Add a scope-critique bad example (B3: "a consumer that re-derives a past decision from history or current state").
3. **Audit the other history readers** (read-only research, not a build). About 21–22 kit scripts call `git log`, `rev-list` or `--first-parent`, depending on the pattern; most legitimately diff a range. File a row only for a script that recomputes a past decision.

**Measure.** The reshaped WI-902's rounds and findings, reported on their own, not pooled with item 4's trial. The audit's candidate count.

**Downstream.** WI-902 changes shipped scripts either way (its Done-when owes a RESYNC entry). The cell is new data, not a migration.

**Owner calls (ruled; the rulings section governs):**

- Resume WI-902 as built, or reshape it to record-at-close first (recommended)? Its Trust ruling (coordinator-2026-10-11 D-005) is still pending your confirm or overrule.
- Confirm or overrule the record-at-event rule for `PROCESS.md` §3.

## 3. Split at birth on independent deliverables

**Evidence.** See the splitting answer under the two questions: per-WI overhead is real, no size threshold is visible, and the two blow-ups are confounded. What holds is containment.

**Root cause.** S1 of the scope critique already names independently landable deliverables, and the owner may keep them together. WI-834's spec kept three subsystems together by recorded choice.

### Proposal

1. **Keep S1 as the split rule; add no size threshold.** Split when the deliverables are independent and their dependencies are recorded, unless the owner keeps them together, as today. The critique may report an expected size as information, not a trigger. That respects your 2026-10-07 ruling of no lane-size tripwire.
2. **Don't split to fix churn mid-lane.** A churning lane is usually an item 1 problem. The remedy is a dispute sitting that draws the coverage line.
3. **Optional: batch tiny rows that share context.** Where two or three small queued rows touch the same module and share a reviewer's context, one row saves the per-WI overhead.

**Owner calls (ruled; the rulings section governs):**

- Confirm or overrule keeping S1 as the only split rule.
- Decide whether same-module tiny rows should be batched.

## 4. Review settings: a cap, an exit, and a convergence round

**Evidence.** See the narrow-versus-full answer. In WI-834, six narrow approvals each triggered a checkpoint that the following full review reopened, mostly with new members of the open shell space. Nothing bounds the number of rounds: WI-834 ran 20, and dispute sittings drew the coverage line only at rounds 25 and 31. The "two-round breaker" that stopped WI-902 after two non-SOUND full gates was the coordinator's own call (coordinator-2026-10-11 D-015), not a setting. The kit has one review dial, `[policies] review_rounds = 0|1|2`. Despite its name, it counts independent reviewers, and only the managed loop reads it; the coordinator cycle hard-codes one Sol review per round.

**Root cause.** Review has no declared shape. How many reviewers, how many rounds, what happens at the limit, which findings block and how the last round behaves are all decided per lane, ad hoc.

### Proposal: one `[review]` section (owner's draft, refined)

| Key | Owner's value | Meaning |
|---|---|---|
| `iteration_reviewers` | 0 | Reviewers of each fix's delta (today's narrow round). 0 means no narrow rounds: a fix goes straight to the next full round. |
| `iteration_rounds_max` | 0 | Delta rounds allowed per WI. |
| `full_reviewers` | 2 | Independent full-lane reviewers per full round, run in parallel. Replaces `review_rounds`. |
| `full_rounds_max` | 3 (ruled; drafted as 2) | Full rounds per WI before `on_limit` fires. |
| `on_limit` | `"adjudicate"` (proposed) | Open findings at the cap go to one dispute sitting, which rules each FIX-as-successor-row, DISMISS, or ESCALATE to the owner. The lane then lands what is clean. A convergence-class finding (fail-open, data loss, Done-when gap) is never deferred to a successor (revision 7). The alternative value is `"owner"`. |
| `block_on` | `["BLOCKER", "MAJOR"]` (proposed) | Severities that cost a round. MINORs are recorded (spine change list or successor) and never trigger one. |
| `reviewer_families` | `["openai", "anthropic"]` until a Gemini route is verified, then `["openai", "google"]` (proposed; revision 15) | One family per reviewer slot. A third family is preferred when available; otherwise a different family or model from the first reviewer, recorded as a substitution (item 7). |
| `final_round_stance` | `"convergence"` (proposed) | How the last allowed round behaves (below). |

With the ruled values (0 / 0 / 2 / 3) a WI runs: build; up to three full rounds of two parallel reviewers, fixing between them; the checkpoint after the first round with no BLOCKER or MAJOR code finding; the post-checkpoint gate in convergence stance; then land, or adjudicate at the cap. That is eight review sessions per WI in the ordinary case (four Codex); a convergence-class fix round or an uncounted rebase round adds two each (rulings section). Most WIs already land within 1–2 rounds, so the cap only binds on the churners. `on_limit` is what makes the cap work: without it, a cap leaves open findings with nowhere to go, which is what happened ad hoc with WI-902. Where the checkpoint and its gate sit is set out in the rulings section's clarifications (revision 7).

### The reviewer's stance

Keep "try to break it", but calibrate it. That stance found the warm-tick race and the truncated fence. Two changes stop it from hunting rare, nuanced edge cases into an endless loop:

1. **Severity tied to reachability** (reviewer template, shipped). A BLOCKER or MAJOR needs a stated scenario reachable in normal use, or a fail-open, data-loss or security path. A rare or contrived edge case is at most MINOR, and under `block_on` it never costs a round. This extends the threat-model rule, which already dismisses compromised-host findings, to findings that are possible but unlikely.
2. **A convergence stance for the last allowed round.** The final round's reviewers never see earlier verdicts (revision 8 ruling), so they confirm fixes through the regression tests: they verify that the added tests fail on the pre-fix code, check Done-when coverage and look for regressions. A *new* finding blocks only if it is fail-open, data loss or a Done-when gap; anything else is filed as a successor row. This stops the cap's last round from becoming a fresh sample of the input space, as the 2026-10-04 research note advised: "a reviewer told to find gaps will always find some, so ground the review in the acceptance criteria". A per-slot stance (A adversarial, B acceptance-only) is possible later; the per-round form is the one aimed at convergence.

**Why the convergence round sees no earlier verdicts** (owner ruling, revision 8). The kit's own measurements: a leaked self-assessment collapses review finding rates several-fold, and when a lane's clipped verdict leaked into a judge's brief, the judge agreed with it (`project-trajectory/prompts/README.md`). The literature the kit cites (`docs/knowledge/co-planning.md`): agents shown peers' conclusions conform rather than challenge. Sycophantic conformity was measured in 85.5% of exchanges; consensus can eliminate a correct answer already on the table; and refinement without an external signal degrades (Huang et al.). The persistent-adjudicator study found anchoring too. Those studies cover QA, math and debate, not code review specifically, but prior reviewer verdicts are exactly a peer's conclusions. Regression tests are the external signal that confirms a fix without anchoring the reviewer.

**Trade-off.** A cap with an exit can leave a valid finding to a successor row instead of fixing it in the lane. That is deliberate: the dispute sitting decides, and the finding is recorded, not lost. The convergence round can miss a new subtle defect, but only a non-fail-open, non-data-loss one, and it still lands as a successor.

**Measure.** Rounds per landed WI. How often `on_limit` fires, and its outcomes (FIX-successor, DISMISS, ESCALATE). Successor rows minted by convergence rounds, counted against the net-queue measure so the queue doesn't grow by stealth.

**Downstream.** A new section in the shipped `process.toml` template (the structure must match, `test_dogfood_sync`), `review_rounds` migrated into it, and the reviewer template's severity rule: one RESYNC entry and a `--migrate-config` step. The coordinator cycle and the managed loop both read the section, so they mean the same thing.

**Owner calls (ruled; the rulings section governs):**

- Confirm or overrule the `[review]` keys and your values (ruled 0 / 0 / 2 / 3).
- Confirm or overrule `on_limit = "adjudicate"`, `block_on`, and the convergence round.
- Confirm or overrule severity tied to reachability.
- The builder's coverage plan in review briefs: today's recipes append it to each narrow brief. Should a reviewer see it, given the template's rule that a judge's brief carries no claim of the judged party?

## 5. Requirements never reference code; code points up

**Owner ruling, 2026-10-11:**

- Requirement rows carry no code references at all: no paths, modules, functions or symbols. Code blocks reference up to their requirements, and tests may still point to modules.
- Why: everything in the spine points up so that requirement ids stay stable. Code markers are not stable ids. A requirement that names code reopens every time the code moves, and that grinds requirements to a halt.
- Sequencing: this can be done last.

**Evidence.** All 302 LLR rows carry `module` and `code_symbol` cells (both reviewers confirmed). LLR-312's `code_symbol` names five functions, and its `detail` narrates how they work. The WI-798 sitting returned 11 rows at once. A rough token census (unreproduced, and it overcounts) finds code-like names in the prose of about 202 of 302 LLR rows, 25 of 131 SR rows and 6 of 31 stakeholder needs. Any fix that renames or reshapes a named function makes an Approved row untrue, and then Terra reconciles, the sitting re-judges, and a return costs another sitting.

**Root cause.** The trace direction is mixed. `Implements:` tags in code point up, but the LLR's `module` and `code_symbol` cells point down at the same facts and must be hand-synced. The R2 ruling (2026-08-15) kept SR cells free of artifacts but left two doors open: a filename in acceptance as "current carrier" evidence, and concrete names at the LLR tier.

### What the rule covers

| Artifact | May reference code? | Direction |
|---|---|---|
| SN, SR, LLR rows (every cell, acceptance included) | No | point up only (SR → SN, LLR → SR) |
| Code (functions, classes, modules) | Yes: `Implements: LLR-NNN` | points up to its LLR |
| TC rows | Shipped boundary files only; no test files or modules (revision 8) | verify up (TC → LLR) |
| Test files | Yes: a tag naming the TC they verify | point up to their TC; the TC evidence column is generated |
| Generated views (dashboard architecture, trace matrix) | Yes, derived | computed from the up-pointers, never authored |

Under this reading, "current carrier" evidence moves from SR acceptance to the TC rows that verify it, and the LLR tier states contracts, not code carriers. R2's third guarantee, "why does this file exist", was to be kept by an inverse check: every shipped module carries at least one `Implements:` tag naming a live LLR. That check is **new** (revision 12): today back-link coverage is a dial (`[checks] backlink_coverage_min`, shipped at 0 and measured, never a blanket rule; PROCESS.md §3, OI-42), so making it a per-module rule is a proposal with an adoption cost, not existing behaviour. **Withdrawn by the owner (revision 15, variant F):**
- **Encouraged, not mandated.** Every artifact is encouraged to link back to the spine, never required to.
- **What counts as a link back.** An `Implements:` tag, a `Contract` citation, or a link within the same artifact (for example, a shared header that the files using it import).
- **Why only encouraged.** It weighs discoverability (if something is wrong, what to change and what is affected) against rot (a pointer left stale). The dial measures it.

The pointer rules, as ruled, are drawn in [`pointer-rules.md`](pointer-rules.md) beside this file.

### Bounding it mechanically: three layers, strongest first

1. **Make it unrepresentable in the schema.** Delete `module` and `code_symbol` from the LLR schema (`kitlib/spine.py`), and make the loader refuse keys a requirement tier doesn't declare. Everything that reads those cells switches to one index generated from the `Implements:` tags. Readers today: `check_doc_refs.py`, `check_privacy.py`, `kitlib/spine.py`, `kitlib/secret_classes.py`, `lane.py`, `migrate_carrier.py`, `spine_carrier.py` and `trajectory_arch.py`, plus five tests (`test_assumption_gate`, `test_baseline_snapshot`, `test_derive_stage`, `test_module_size_ratchet`, `test_trajectory_arch`). IF rows' `owner`, `consumers` and `requestors` cells go the same way, generated from the code's `Contract IF-NNN` citations (revision 7; under item 11's variant F, the owner's form is F-call 1, revision 16). This removes the hand-synced cells, not the meaning check (below).
2. **A commit-time check on requirement text**, grown from the warn-only `trace_text.sr_artifact_advisories` (today: `*.py` in SR requirement cells). Its rules follow the ruling, tier by tier. Code tokens are refused in SN, SR, LLR, IF and CMP rows: paths to implementation files, and names defined in the shipped scripts (read by `ast` on every run) written as code (backticked, snake_case, CamelCase or a call). Shipped boundary-file names are refused in SN, SR, IF and CMP rows and allowed in LLR and TC rows, the boundary set being the inventory's explicit `boundary` class (revision 6). It compares the commit with its parent and looks only at *tokens added* to a requirement text cell. A lane that touches a row for a non-text reason (`test_refs`, phase, status) owes no prose rewrite, and untouched rows are left alone. An Approved row whose text is cleaned rides the layer-1 batch act or the lane's own sitting.
3. **Judgement layer.** The sitting brief and the `spine-authoring` skill extend K2 from SR to all requirement tiers as contract voice. An LLR states the observable obligation (inputs, outcome, refusal boundary) and survives a refactor that keeps behaviour. No lint can catch mechanism narrated in plain words; this layer does.

**Keep the meaning check.** An `Implements:` tag that names a live LLR doesn't prove the code implements it. The independent semantic check stays: the code reviewer judges, over the derived index, whether code and the rows the lane touches correspond. That includes omissions and inconsistent amendments of existing rows. What moves wholly to the sitting is wording quality and overlap, so the two judges stop overlapping without losing the correspondence check.

**Migration.** Layer 1 removes two cells from all 302 LLR rows, most of them Approved, which the `approval-immutable` check forbids today. That needs one ruled batch act, "trace cells removed, requirement text unchanged": a single sitting, not 302 re-attestations. The IF cells need no act, since every IF row is Drafted. Layer 2 needs no migration.

**Downstream.** A kit schema change: a `RESYNC_PACK.md` entry with a migration script (`migrate_carrier.py` is the precedent), an `ADOPTING.md` note and the template rows. With items 4 and 10, one of three changes that force adopters to migrate; they ship as one RESYNC entry.

**Measure.** Requirement rows amended because code moved: target 0. Rows returned per sitting.

**Open questions (ruled; the rulings section governs):**

- Confirm or overrule the reading above: no code in SN/SR/LLR rows, acceptance included, so carrier evidence moves to TC rows. This supersedes R2's two allowances.
- Do interface (IF) and component (CMP) rows count as requirements under this rule, or as architecture that may point at code? My lean: CMP points up like code; IF names a seam's contract, not its file. Needs its own look.
- Confirm or overrule the split: wording and overlap go to the sitting, and code-versus-row correspondence stays with the reviewer.

## 6. Run the strict lints after every build

**Evidence.** About 6 findings in the sample were things an existing instrument catches: SR-239's two "shall" clauses (`trace.py --strict`), IF-292's channel outside the closed set, an IF cell over 160 characters, a missing `RESYNC_PACK.md` entry, an undeclared IF seam. Each cost a 25–35 min review round.

**Root cause.** The lints exist but nothing runs them mechanically after a build. The commit hook runs `trace.py --strict-integrity` but not `--strict`, and runs `check_trajectory.py --staged` non-blocking (`|| true`, `project-trajectory/hooks/pre-commit:296`). A recipe line asking the coordinator to run them gets skipped; an earlier session already recorded "run check_trajectory --strict before a landing commit" as a trap.

**This is not a guard.** A guard, in the antidote sense, compensates for a bad state the design could have made impossible. Two "shall" clauses can't be made impossible, because they are authored text. The remedy is the lint step after the build, run at three boundaries nothing skips: the commit-bar command each build round already runs, the closure check before a sitting, and the landing check. The pre-commit hook stays as it is (ruled).

### Proposal

1. **Make trunk clean, then keep it at zero, after each build, not in every commit** (ruled). Fix LLR-292 ("minimal" with no measurable bound), the one finding that makes `trace.py --strict` exit 1 on trunk today. Then run `trace.py --strict` and `check_trajectory --strict` in the commit-bar command each build round already runs, in the closure check before a sitting, and in the landing check. The pre-commit hook stays as it is.
2. **Build the one missing check:** a shipped file changed in the commit with no `RESYNC_PACK.md` entry anchored at a trunk commit. No such check exists today.
3. **Retire rubric anchors as they become mechanical.** K4 becomes the RESYNC check. K3's module/symbol matching goes away with item 5's schema layer, and its meaning half stays as item 5's correspondence check. K2 becomes item 5's commit-time text check.

**Trade-off.** About 9 s per build round and at each closure and landing, not on every commit. A newly strict lint can surface old findings in an adopter's repo; the RESYNC entry says to run `trace.py --strict` once and clear them before upgrading.

**Measure.** Review findings an instrument would have caught: target 0.

**Downstream.** The commit-bar profile, the closure check and the landing check change; the hook does not: one RESYNC entry.

**Owner calls (ruled; the rulings section governs):**

- Confirm or overrule the LLR-292 fix and the lints after each build (not in the hook) as the first rows.

## 7. A second reviewer from a third model family

**Evidence.** The kit already ships the dial: `[policies] review_rounds = 0|1|2` (this repo: `1`, `docs/process.toml:202`). At `2` two independent reviewers split charters (A: method, risk, corner cases; B: process, trace, prose), and a cross-provider pair is the recommended setup, routed per phase through `AGENT_CMD_MAP`. Only the managed loop reads it. The coordinator cycle hard-codes one Sol review per round through `sol_review.sh`, and specs carry "Review bar: A".

**Why it helps, and what it won't fix.** Two reviewers in parallel pull discovery forward at no extra wall-clock, and a different family brings different blind spots. On an open input space they just sample twice as fast, so item 1 comes first.

### Proposal

1. **A third family when one is available** (selection mechanics clarified in revision 16: always distinct fresh reviewer sessions, chosen from the existing route registry in `process.toml` by route and model identity, a different family preferred, otherwise a different model, with the substitution recorded; duplicate family strings are not evidence that the models differ, and no session that authored the work reviews it, OI-111). The builder and the adjudicator are Claude, and Sol and Luna are OpenAI, so the preferred second reviewer is Gemini. Otherwise the second reviewer is an independent reviewer of a different family *or a different model* from the first reviewer (today, Claude Sonnet beside Codex Sol, per ruling 7), recorded as a substitution (owner, revision 15: "must be a third one" was too strict). The route is not close: WI-815 owns the Gemini stdin route (its title says "an untested Gemini route") and needs WI-798 and WI-801. The trial waits on WI-815 plus one verified independent Gemini launch.
2. **Trial with the kit's current charters.** Re-cutting B toward regressions and Done-when coverage only makes sense once items 5 and 6 have mechanized trace and prose checks. Revisit the charters after that.
3. **The reviewers come from item 4's settings** (`full_reviewers`, `reviewer_families`), read by the coordinator cycle and the managed loop alike, instead of one hard-coded Sol review.

**Measure.** Share of a lane's findings raised in its first review. Findings only one reviewer raised: if B's are mostly duplicates, it isn't earning its cost.

**Downstream.** None for the dial (it ships). A Gemini route is an adopter option.

**Owner calls (ruled; the rulings section governs):**

- Confirm or overrule a Gemini reviewer B, after WI-815 and a verified launch.
- Until the Gemini route works, should `full_reviewers = 2` run as two fresh Sol sessions (same family), or stay at 1?

## 8. Record usage for every model call, sub-agents included

**Evidence.** `session_service.py` calls itself "the one path every model call takes", but in the coordinator cycle only the adjudicator goes through it: the last 40 session logs in `docs/iteration/` are all `role: ADJUDICATE` (both reviewers confirmed). Builders are Claude Code sub-agents of the coordinator session. Sol and Terra launch through `coordinator-tools/sol_review.sh` and `terra_author.sh` straight to `codex exec`. The leg itself runs as `claude -p`. None of those are recorded.

**Size of the gap.** Leg 3 (2026-10-11), read from its transcripts and counted once per message id. Revision 1 summed repeated records of the same message, which doubled the totals. The coordinator: about 151k output tokens and 33.5M cache-read tokens. Nine `kit-builder` sub-agents: about 564k output. One `Plan` sub-agent: about 51k. Builders were about 74% of the leg's Claude output (all sub-agents about 80%), none of it in the kit's records. Sol and Terra usage is unmeasured.

**Where the data is.** Claude Code writes each sub-agent's transcript under `<session>/subagents/agent-*.jsonl`, beside a `.meta.json` naming the agent type, its task and its `spawnDepth`. A message's usage appears in several records and must be counted once. Where depth-2 transcripts land is unverified. WI-800 (queued) already owns the durable invocation store and an idempotent usage ledger.

### Proposal

1. **Route Sol and Terra through `session_service`**, as `coordinator_adjudicate.py` already routes the adjudicator. The launch scripts keep their sandbox, effort and HEAD/status checks but call the service.
2. **Ingest Claude sub-agent usage under WI-800's ledger contract.** Read the leg's transcript and its sub-agent transcripts. Count once per message id. Attribute each invocation exactly once (by invocation identity, so a repeated close-out or a resumed transcript adds nothing). Write through the service's one writer. Verify where nested transcripts land before claiming coverage of nested agents.
3. **Verify the alternative.** If a `claude -p` session's final usage includes its own sub-agents, builders could launch through the service directly. Unverified.
4. **Use the rows.** Per landed WI: builder, reviewer, author and adjudicator tokens and wall-clock beside its review rounds. That turns the re-measure (phase 4) into a query.

**Trade-off.** The transcript format belongs to Claude Code and can change. Keep the reader in one adapter (`session_adapters`), refusing loudly on an unknown shape.

**Downstream.** Step 1 touches this repo's coordinator tools. Step 2 adds an adapter to a shipped module: one RESYNC entry.

**Owner calls (ruled; the rulings section governs):**

- Confirm or overrule routing Sol and Terra through the session service.
- Confirm or overrule ingesting sub-agent usage under WI-800's ledger, ahead of WI-800's other parts if needed.

## 9. Planning need decided at mint; advice made binding

**Evidence.** The kit has two planning layers, and neither runs in the coordinator legs. **Dual-plan decomposition** (`planmode = "dual"`) breaks a goal into WIs: two planners from different families, a `plan_coverage.py` pre-pass, one cross-critique round, and an arbiter. Its engine exists, but `dispatch.py` never picks dual rows up (WI-813 queued to fix it), and its one round (DP-001) ended with the arbiter changing nothing. The **per-item single plan** (`planmode = "single"`) is designed (WI-788) and filed as WI-805, queued behind WI-804 (itself behind WI-801 and WI-803) and WI-799. What WI-834 *did* have was scope planning: two pre-build Sol reviews of its spec and plan (`docs/reviews/wi-834-plan/`). The first already asked for the enumerated list that rounds 25 and 31 finally drew. The build then produced twelve reactive coverage plans (`PLAN-r1` to `PLAN-r12`).

**Root cause.** Not a missing review. The pre-build review's recommendation did not become binding spec text, so the build and its reviewers were not held to it. A second gap: the `planmode` trigger exists ("one declared trigger at filing time"), but criteria exist only for dual, and no queued row sets it.

### Proposal

1. **Bind the advice.** A pre-claim review (scope critique, plan review) ends with its accepted recommendations written into the spec, in the Done-when or the Trust section, before the claim. A recommendation not adopted is recorded with the reason. This is item 1 step 2 applied to every pre-claim review.
2. **Scope critique decides the planning need** (anchor S4). The answer is none, single or dual, recorded as `planmode`. **single** when the row has a `## Trust` section, touches two or more script families or IF seams, or promises behaviour over an input space; **dual** only on the existing design-shaping applies-when; **none** for a diff a cheap test fully specifies. No size threshold, consistent with item 3.
3. **One planning path, not an interim one.** Either pull WI-805's plan gate forward (decoupled from the rest of its chain if the owner agrees), or wait for it. Revision 1's "light version" would have been a second path, and it allowed building without a passing critique; both are withdrawn. On the one path, a build starts only after a passing independent plan verdict. If the capped revision doesn't pass, it goes to a dispute sitting or to the owner, never to the build.
4. **Dual: fix its pickup as is** (ruled; WI-813), arbiter kept.

**Trade-off.** A planned row costs one more Codex session and ~15–20 min. A bad plan does worse than none (the 2026-10-04 research note), so the critique is grounded in the Done-when.

**Measure.** For `single` rows against comparable unplanned ones: review rounds, late findings, and how many late findings the bound spec text already named.

**Owner calls (ruled; the rulings section governs):**

- Confirm or overrule binding pre-claim advice into the spec.
- Confirm or overrule S4 and its criteria.
- Pull WI-805's plan gate forward, or wait for it.
- Fix dual's pickup (WI-813), or retire its arbiter.

## 10. One configuration file, in TOML

**Owner ruling, 2026-10-11:**

- The automated chain is configured from one file in one format. `docs/work/pause` stays a presence file, the main exception, so `docs/agents-enabled` becomes a setting.
- The format is TOML, in `docs/process.toml`. `stack.ini`'s content moves into it.
- A re-sync does not replace `process.toml`: the adopter's values stay, and only new settings are taken in. Re-sync is carried out mainly by an LLM, so it doesn't need to be mechanized. Nothing in re-sync does, though existing mechanization may stay.
- Sequence it before the FileBackup re-sync, so adopters migrate once.

**Why the split existed.** `stack.ini` was created on 2026-07-04, when the kit's Python floor was 3.8. Python 3.8 ships `configparser` but no TOML reader; `tomllib` arrived in 3.11. WI-262 raised the floor to 3.11 on 2026-07-22. `process.toml` followed on 2026-08-08 in TOML, its header noting the 3.8 constraint was "spent", but `stack.ini` was excluded for an ownership reason instead of converted. No shell or PowerShell script reads `stack.ini`: all 13 parse sites, in 12 scripts, are Python, and the hook only checks that the file exists. The shell-readability rule belongs to `process.toml` (two privacy keys), not to INI.

**Investigation (three read-only passes, 2026-10-11).**

- **Readers.** `stack.ini` is parsed separately in 13 places across 12 scripts (13 `ConfigParser` constructions; `check_trajectory.py` reuses `trajectory_arch.py`'s), each with its own `configparser`. No code writes it; bootstrap copies the template and does one text replace. `process.toml` is read mostly through a shared reader (`agent_policy.process_config`), plus five self-contained scripts and a two-key shell grep in the hooks. Its one writer (`bootstrap.set_process_key`) rewrites single lines and keeps comments.
- **Content.** `stack.ini` is 1,277 lines, of which 1,168 are comments, including an 865-line smoke-budget history log. Only 70 lines are settings. The chain-behaviour parts are `[agent-loop]` (model, model-map, read only when managed routing is off) and `[run]` (launcher capabilities).
- **TOML fit.** `[step:smoke]` becomes `[step.smoke]`. `smoke.desc` beside `smoke` becomes `[run.smoke] command / desc`. Path keys under `[generated]` are quoted. Windows paths use literal strings. Lists packed into comma-, pipe- and space-joined strings can become arrays. INI's key case-folding goes away.
- **Tests and spine.** About 55 test files touch `stack.ini` and 56 touch `process.toml`/`agents.toml`/`agents-enabled`, much of it fixture text. 24 LLR, 8 TC, 4 SR and 9 IF rows name one of the four files being folded (`stack.ini`, `process.toml`, `agents.toml`, `agents-enabled`). Under item 5's ruling the SR and IF mentions must go; LLR and TC rows may keep naming the configuration file, a shipped boundary file, but not code.
- **Downstream.** No adopter has taken even the 2026-08-08 `process.toml` migration. Gilbert, Finance-Auditor and NotHomeWrecker carry `stack.ini` and the legacy one-word files; FileBackup has neither. Their `stack.ini` content is small: paths, product, tiers, coverage, `arch-map`, and a few `[step:*]` gates of their own. None uses `[agent-loop]` or `[run]`.
- **Precedent and cost.** The 2026-08-08 migration was the same kind of work. It drew 8 BLOCKERs, including the privacy gate failing open on a decoy value in a TOML comment, and weeks of follow-ups.

### Program

1. **One shared loader for today's `stack.ini`**, replacing the 13 separate parses. A pure refactor with no format change. Every later step then touches one reader, and it is worth doing regardless.
2. **Settle the shell-grep rule.** The hooks grep `privacy_check` and `privacy_review` so a machine without Python still fails closed, and that is what imposes `process.toml`'s one-key-per-line shape (SR-137, SN-028). Verify whether the same hook already refuses to commit without a 3.11 interpreter; it runs `check.py` and points to the installer when none is found. If it does, the grep is redundant, and the shape rule can go by ruling. If not, the privacy keys keep a small section the grep reads, and the rest of the file may use full TOML.
3. **Adopter-owned values, kit-owned schema.** `process.toml` stops being "overwrite, then re-apply your dials". The kit ships the schema: a template that documents every setting and its default, and a validator that refuses unknown or malformed settings. The structure test changes from "live equals template" to "live satisfies the schema", so adopters can declare their own `[step.*]` sections. A re-sync adds new settings and never overwrites values. Per the ruling, the RESYNC entry says what to add and the LLM doing the re-sync applies it; no new migrator is built.
4. **Move `stack.ini`'s settings into `process.toml`** as TOML sections, through the shared loader from step 1. The smoke-budget history log moves out of config into the log. Readers use the new home only, with no dual-read window (no fallback paths). A repo that still has `docs/stack.ini` is refused by name, pointing at the RESYNC entry, so an unmigrated file is never silently ignored.
5. **Fold in routing and consent.** `agents.toml`'s routes become `process.toml` sections; its triple-quoted strings can stay, since the shape rule goes (step 2). `agents-enabled` becomes a setting that keeps its semantics: an ordered pool of route ids with per-phase weights, validated as today, where an absent or empty pool grants no consent. `[agent-loop]` retires into the routes. This repo's coordinator tools read their models from the routes instead of hard-coding them.
6. **Amend the spec rows and docs together with item 5**: the rows the investigation counts (24 LLR, 8 TC, 4 SR and 9 IF rows; recount at the build), about 10 adopter-facing docs (`RESYNC_PACK`, `ADOPTING`, `PROCESS_OPTIONS`, the kit README, …), and the generated references. Ship it all as one RESYNC entry, before FileBackup's re-sync.

**Trade-off.** A 4–6 WI program touching a security-relevant reader: the privacy keys. Step 2 settles that first, and the 2026-08-08 decoy-comment failure goes into each review brief as a named failure class.

**Downstream.** One migration for adopters instead of two. The RESYNC entry carries both the 2026-08-08 one-word-file fold and this consolidation, for an LLM to apply.

**Resolved (revision 5):**

- The file keeps the name `docs/process.toml` (ruled).
- Step 2: all three hooks refuse without Python 3.11+, so the shell grep and the shape rule go; the remaining shell reads, including the legacy `docs/privacy-check` read, become one `tomllib` read in `kit-python.sh` after the interpreter check (not objected).

## 11. What points where: interfaces as the measured boundary

The owner asked (2026-10-11) whether more of the pointer model should change. In the owner's proposal:

- implementation code points up only to the interface (IF), the contract whose behaviour can be measured;
- the IF points to the LLR or SR it carries;
- a code file names the component (CMP) it belongs to, as a physical part does its assembly;
- components then bound what is at risk, and what must stay compatible, when one changes.

Three read-only passes traced the history first, because the owner didn't recall how these links came to be.

**Terms (owner, 2026-10-11):**

- **Contract:** the stated bounds of what crosses one interface, such as the range of an output, the character limit of a stdout, the pattern of CLI output or the shape of a refusal. It is written in the owning module beside the code (`Contract IF-NNN:`). It is not the business behaviour the code exists to achieve; that is the LLR's ("an interface says what crosses; a requirement says what must be achieved", PROCESS.md). Some existing contract bodies read more like obligations (IF-001 opens "SR-157's obligation delivered as a CLI"), so they are tightened to interface bounds as they are touched. (Revision 12, Astra's sample: of the first fifteen bodies in file order, eleven mix obligations with bounds, e.g. IF-252 and IF-091, and four are bounds only, e.g. IF-260. Tightening "as touched" is a substantial cleanup, not an IF-001 one-off. PROCESS.md §8's "flags, schema, guarantees" is also broader than bare bounds; observable preconditions and refusals stay in the contract.)
- **Module:** one unit of realization, represented by one file in git. In a software project that is a code file; where physical parts join (Gilbert), it is the part's file. A component groups modules, and "file" is a valid synonym. (Revision 13, Fable's check: Gilbert has no instance of "the part's file". Its PART registry holds only the example row and has no file cell; a bought part "never reaches the LLR tier" (OI-20); its physical sources are parametric `.py` files bound in LLR `module` cells, the software mechanism; its ASSET locations are gitignored. The kit already has a word for the bound unit: "realization artifact (a code symbol, or a part source)" (PROCESS.md §4, OI-20). And the kit already uses module and file as different words: an IF `owner` may be "a module path, a file path" (PROCESS_OPTIONS.md).) Earlier sessions defined these terms for compatibility with physical projects, and the reviews cross-check that this reading matches. **Revision 12 (Astra's cross-check, confirmed):** the earlier uses are broader. The old `MOD-###` registry (`modules.template.csv`) tracked delegated *repositories*, and was renamed `REPO-###` on 2026-07-09 (`7f8cdc567`). PROCESS.md §10's rungs ("one module, one repo", "several modules, one repo") use module for a sub-system. In Gilbert, ASSET-001 is a fetched, gitignored directory of scene files, and a PART row records a bought part, not a source file. So "one file in git" fits software source files, not every realization unit. Whether to keep "module" for the source file and name the other units separately (realization unit, component, part, asset) is an open call.

**Owner's queries (2026-10-11, revision 11), for the reviews to test:**

1. **A contract is cited only where it is served, and never mandated.** Not every function is expected to have a contract today, and nothing in the proposal should require one: a module or function with no seam of its own carries no `Contract IF-NNN`. The other half is the one that needs a bound. A function names a contract only if it actually realizes that interface's outcome (it produces, checks or refuses what crosses that seam), never because it sits nearby or helps. Item 5's proposed rule that every shipped module carries at least one `Implements:` tag (new: today coverage is a dial shipped at 0) would become a per-module rule (a component declaration, plus at least one contract *or* an explicit "internal" standing), never a per-function one. Open for the reviews: what bounds an over-claimed citation mechanically, if anything does? Candidates are the contract's own TCs exercising the citing symbol, the citing file declaring the component that owns the IF or is a declared consumer of it, or review alone. Is review alone acceptable, given item 1's preference for closed rules?
2. **Work items bound to the interfaces they serve.** A WI row today carries `sr_refs` (the SRs it delivers, warning-level per PROCESS_OPTIONS.md; 24 of the 31 real queued rows fill it, WI-000 being the example) and `needs` (its DAG edges, authored by hand). The query is whether a WI should instead, or as well, name the interface(s) it serves or changes (an `if_refs` cell, ids only). Then its requirement trace is mechanical (WI → IF → LLR/SR), and so is its blast radius (WI → IF → component → the TCs verifying the carried requirements). The work-queue tree would then relate to the spine. Two WIs serving one IF *may* overlap (the consolidation census already flags "both answer SR-222" by string match, as "often correct; worth seeing"). A WI changing a consumed interface would often order before its consumers' WIs, from the IF's provider and consumer cells, though runtime order is not build order (revision 12, below). The 2026-07-14 intake considered a WI `IF-Refs` column and deliberately did not file it, on migration cost (`docs/log.md`, 2026-07-14). For the reviews:
   - Does `if_refs` replace `sr_refs`, or sit beside it? Work with no interface (process, adjudication and doc rows: 7 of 31 queued rows have no `sr_refs`) needs a declared standing, not a placeholder id.
   - Should `needs` edges be checked against IF provider and consumer order, or derived from it?
   - The requirement rows' dependencies are their parent links: SR → SN (`sn_refs`), LLR → SR (`sr_refs`), and an SR's joint-delivery siblings (`delivered_with`). With WI → IF → LLR/SR, the queue can group under that decomposition tree mechanically. The recursion the owner expects is designed in at the activity, not the tier. PROCESS.md §4 says "the tier does not recurse, the activity does": a requirement still to be allocated to sub-parts is a `DevStg-Reqs` requirement (an SR) for that sub-scope, and the LLR is the terminal floor (`DevStg-LLReqs`), bound to one realization artifact. But no cell found so far lets a sub-scope SR point up to the parent obligation it decomposes, or name its component scope: an SR carries only `sn_refs`. If so, the queue can mirror only one level of the tree. Two readings, judged on long-term design sustainability, not on what past rulings committed to (owner, 2026-10-11). (a) SRs state obligations at every component scope and decompose to a terminal LLR; this is the 2026-08-12 ladder as written. (b) SRs state behavioural expectations **only at the system boundary**, and architecture decomposes them into LLRs **recursively** (an LLR may decompose an LLR) down to where they can be implemented. **The owner leans to (b)** (not a ruling). Under (a), later churn that shows an LLR needs further breakdown forces it to change tier and become an SR. The owner expects that to be far more likely than a boundary change that alters an SR's definition. Under (b), only a boundary change moves an SR. For the reviews: give the strengths and weaknesses of each alternative, and the cost of (b). That cost includes a parent-LLR pointer, the ladder's "TERMINAL" and "the tier does not recurse" text, the `DevStg-Reqs`/`DevStg-Arch` recursion, SR → LLR coverage and orphan rules, the CMP tree, adopters' schemas, and Gilbert's physical parts. Two facts bear on it. Item 5 removes the `CodeSymbol` binding that defines the LLR floor today, so item 11's discharge rule (an LLR is discharged when a code-cited interface carries it) would re-found that floor. And the 2026-08-13 form rule already ties each shall to an interface at its own component level, which is item 11's IF → requirement link stated from the requirement's side. Neither the parent links nor `delivered_with` states a build order between siblings, so the order between WIs comes from the interfaces' provider and consumer cells.
   - Does this sit with item 3 (split on independent deliverables: one interface as the natural split unit?) and with item 9 (S4's "two or more IF seams" criterion becomes countable)?

### How the links got their shape

| Date | Change | Why (as recorded) |
|---|---|---|
| 2026-06-04 | The kit is born with two-way code links: LLR `Module`/`CodeSymbol` down, `Implements: SR, LLR` up | The initial template's design |
| 2026-07-09 | CMP is ratified as one domain-neutral id. LLR, IF, PART and ASSET rows name their component; the CMP row holds only what a tag can't. A design where the component listed its LLRs (`Realises`) was rejected. | Owner: "structure is derived, never restated". LLRs carry the tag because a software component has no members via IF alone. |
| 2026-07-11 | First filled IF registry (the template's `SR-Refs` requirement link dates from 2026-06-05, `af852db7a`), and a module path for this project's side. Every script gains a `Contracts: IF-NNN` header line. | WI-057 |
| 2026-07-14 | Allocation is LLR → CMP, stated once on the LLR; SRs reach components only through their LLRs | Owner intake answer |
| 2026-08-09/13 | OI-14 (raised 2026-08-09, ruled 2026-08-13): the component partition is "formative", and "a module belongs to exactly one component" (its recommended shape) | Owner: "component is not a function of module"; a module serving two components is evidence about the partition |
| 2026-08-12/13 | The eight-rung ladder (OI-21 re-ruled; WI-445): requirements before architecture, the boundary once, `DevStg-Reqs` and `DevStg-Arch` recurse per component scope, and `DevStg-LLReqs` is terminal. PROCESS.md §4: "the tier does not recurse, the activity does" | The LLR floor is defined by OI-20's binding rule (ruled 2026-08-13: "at least one identifier-shaped token in its `CodeSymbol` cell BINDS to a real symbol inside one of the `.py` modules its `Module` cell names"; the ruling admits "a module path, or a designed PART SOURCE"). That is the very cell item 5 retires. |
| 2026-08-13 | The requirement form rule (owner, verbatim in log.md, 2026-08-13s): "A single 'shall' statement is permitted, and must be applied to interfaces going to the respective component level". SR → boundary interface; LLR → component-level interface | Makes the one-shall rule recursive and "mis-tiered" detectable; a bundle is a legitimate interface if broken down in the component details. Softened the same day (2026-08-13v): single-shall is a guideline, with reasoned exceptions |
| 2026-08-13 | The then-live LLRs (149) and 54 IF `component` cells are re-pointed to the new components *mechanically from their module* | WI-441. In practice the authored LLR → CMP tag is a copy of a module → component map. |
| 2026-08-15 | IF `owner` becomes an id: a requirement may own a seam (Q1: "both"). R4 re-points owners toward the design tier. | Owner: "a requirement and a module can provide/own an interface" |
| 2026-08-18–20 | Research (OI-39, OI-42): registry → code "assert-and-verify" is kept, and is hard-gated by SR-180 (an LLR is discharged only when its `CodeSymbol` resolves). Code → registry tags are a measured convention with a coverage dial. | No standard or surveyed tool requires annotations in code, and annotations decay |
| 2026-08-29 | OI-67: IF `owner` flips back to a module path; the requirement column leaves the IF row. `Contract IF-NNN:` bodies are added to code (WI-527). | An SR-owned interface couldn't be traced to code (an SR has no module). The requirement links were "verified by nothing" and duplicated the owner → module → LLR join. |
| 2026-09-20/23 | A proposed IF → requirement `realizes` cell is rejected (the 2026-09-20 assumption-tier plan; Q18 decided 2026-09-23) | It "would give the relation two homes"; a single-valued cell can't express a shared seam |
| 2026-10-11 | Requirement rows name no code; code and tests point up (items 5 and 10) | Code markers aren't stable ids |

The "Why (as recorded)" cells mix sources (revision 13). Only the 2026-08-13 form rule and OI-14's "formative" are the owner's verbatim words. "Structure is derived, never restated" is the ratified AXES note; the 2026-07-14 row is the intake answer; the 2026-08-15 line is the log's paraphrase (the owner's words: "requirements are just decomposition of needs into measurable objectives, and modules are just physical implementations at a lower level"); OI-14's "exactly one component" is its brief's recommended shape. OI-42's and OI-67's `ruling_ref` cells point at `docs/log.d/` files that no longer exist, a hygiene gap outside this plan.

### Where things stand today

- **Code points up twice.** `Implements: SR, LLR` appears on about 900 lines, tagging 793 functions and covering 229 of 302 LLRs. `Contracts: IF-NNN` plus `Contract IF-NNN:` bodies name about 204–229 distinct interface ids (245 citations). 97 script files carry `Implements:` and 84–87 carry a contract; 76–78 carry both. Counts vary with the pattern: Fable (revision 13) finds 929 `Implements:` lines naming 230 LLR ids. The module header is the only place a contract is read today: `gen_arch_map.module_contracts` and `module_contract_bodies` parse the module docstring, or a `Contracts:` line in the first eight lines of top-of-file comments (revision 14 correction), so a function-level `Contract` mention is invisible to every check.
- **An IF reaches a requirement only indirectly:** owner module → the LLR rows whose `module` names it. That is the very down-pointer item 5 removes. Another route is the SR's `boundary_refs` to an external crossing. 95 of 316 TCs already list an IF in what they verify.
- **No code file has ever declared its component.** Each component's modules appear only in its hand-kept `notes`. The generated view places an IF by its tag, unioned with the components its endpoints resolve to.

### The proposal, and what it changes

Item 5's ruling removes the LLR → module join. That join was the one route from an IF to its requirement, and the main reason the IF → requirement pointer was dropped twice. With the join gone, an IF → requirement pointer is no longer a second home: it becomes the only home. And because code would cite its interfaces, the 2026-08-29 objection (an SR-owned seam can't be traced to code) also falls away.

| Link | Today | Proposed (for ruling) |
|---|---|---|
| Code → spine | `Implements: SR, LLR` per function, plus `Contract IF-NNN` | `Contract IF-NNN` only, on the symbols that realize the seam; `Implements:` retires |
| IF → requirement | none (derived through LLR `module`) | an authored list of the LLRs or SRs whose behaviour the interface carries (ids only) |
| Code file → component | none (the map is derived from LLR `module` + `component`) | each file declares its component in its header, as a PART row already does |
| IF → component | optional authored cell | derived from the owner file's component |
| LLR → component | authored allocation (ratified 2026-07-09) | kept as design intent, with a check that the files realizing it declare the same component; or derived and retired (owner call) |
| TC → what it verifies | LLR, SR, sometimes IF | unchanged; tests name their TC (revision 8) |

### Nuances the owner may want to weigh

- **Every LLR then needs an interface.** 55 of 302 LLRs live in modules that own no IF today. Under code → IF only, an LLR with no interface has no path to code. That fits the contract-voice rule (item 5: an LLR states observable behaviour, and behaviour is observable only at an interface). But it means adding `call`-channel interfaces for internal seams, or reframing or retiring those LLRs. The registry grows. (Revision 12: "no owned IF" is not "no observable interface": an existing or external seam may already carry some of the 55. Many sit in the shared kernel, and OI-48 ruled edges into a declared kernel are *not* seams, having declined option (b), an IF per helper edge, in its recommendation, because it makes the registry describe library usage rather than architecture; the ruling generalised (d) into a declared kernel list with a reason per entry. So the 55 are classified one by one, and the kernel case is resolved explicitly, before any `call` seam is minted.)
- **Granularity.** `Implements:` is per function (793 symbols); IFs are module seams (243 rows). Tracing through the IF loses which function realizes which LLR. Citing the contract on the realizing symbols does not recover it (revision 12): if two functions cite one IF carrying LLR-A and LLR-B, the join attributes both to both. The trace becomes coarse reachability, function → seam → obligations, and the coverage dial's meaning changes with it.
- **Two recorded decisions are reversed.** OI-67's removal of the IF requirement column, and the 2026-09-20/23 rejection of `realizes`. Removing the join answers the "two homes" objection, but not OI-67's other one (revision 12): the 48 requirement links that added anything were "hand-written and verified by nothing". One code-cited IF and passing TCs show reachability, not that each carried LLR is realized. So an authored IF → requirement list needs its own semantic check (the reviewer's correspondence check, item 5), and the owner should overrule both decisions explicitly.
- **SR-180 / LLR-180 / TC-175** state the registry → code "symbol resolves" gate as an approved requirement. Item 5 already retires that down-pointer, so these rows retire or are re-minted. The new discharge rule: an LLR is discharged when at least one interface carrying it is cited by code and a TC verifies it, both checkable at the commit; whether the TCs pass stays with the gate, since a test result is not a property of the commit (revision 13). Read SR-180's rationale before retiring it: it calls the symbol binding "the one that decides when decomposition is finished", and it states "nothing here obliges source code to carry a back-link naming the requirement it implements". Item 11 inverts both.
- **The 2026-08-18 research** found that code annotations decay and no standard requires them. Here the contracts and component declarations are enforced at the commit (a tag must name a live row, and every LLR must be reached), which the surveyed tools did not do. That is the trade.
- **Interfaces already have an approval status** (revision 12 correction): PROCESS.md §8 defines `Drafted` · `Approved` for IF rows, and `kitlib/authority.py` assigns interfaces to `DevStg-Arch`. All 243 are Drafted today, a population state. The question is whether a requirement-bearing allocation must be Approved and amendment-controlled under that existing authority.
- **Tools that count LLR ids in `Implements:` lines** (the test-first check, the coverage dial) would count through IF → LLR instead.
- **Shared code.** A file serving several components needs the shared-kernel declaration OI-48 already uses for `kitlib`, rather than a multi-tag.
- **Non-code realizations.** (Withdrawn under variant F, owner, revision 15.)
  - **Why the nuance existed.** It followed only from A's "every file declares its component in its header".
  - **Why it isn't needed (as first argued).** Ruling 5 lets an LLR name a shipped boundary file. The PART/ASSET schema carries `Component` (unfilled in Gilbert). A realization that can't carry a header declares itself in its registry row.
  - **Partly restored** (revision 16), from Fable. Naming a file says nothing about which component it belongs to. 26 LLRs name non-`.py` shipped files. A non-code shipped file declares its component in the `#` header beside its `Contracts:` marker, and a type with no comment syntax is declared on its `boundary` inventory entry (F point 1).

  The original text: shipped boundary files (templates, registries) have no docstring. Their component and interfaces need a comment header, or derivation from the IF `data` cells. Physical realizations are wider still: OI-20 admits designed part sources, and a fetched asset or a bought part has no file to carry a header (revision 12).
- **The minimum profile** (revision 13). PROCESS.md's standalone one-module project has no interface registry, and §8 says single-module projects skip it. Under code → IF only and "every LLR carried by an interface", such a project has no path from code to any LLR. The rule for it is open: a declared system-boundary IF becomes mandatory there, or `Implements:` survives there.
- **The SR half of IF → requirement already has a home** (revision 13). All 131 SR rows carry `boundary_refs` to a `B-xx` crossing, and 47 IF rows name the crossing they realize (`interface_from_external` / `interface_to_external`). SR ↔ boundary IF is derivable through the crossing (no check joins them today), so an authored IF → SR list would be a second home. Fable recommends restricting the authored list to IF → LLR and deriving the SR side; an owner call.
- **An over-claimed owner citation is refused today** (revision 13). `trajectory_arch`'s owner-exact check (warn) and the strict contract-body gate's stray-declaration error check a `Contract IF-NNN:` body against the registry's authored `owner` cell. If `owner` is generated from the citations, that check becomes circular, and a consumer-side citation is today exactly the strict error. Keeping an authored owner id per IF keeps the independent check (the "Generating IF roles" call).
- **Per-module pressure exists today** (revision 12). No check mandates a contract per function, but PROCESS.md §8 has a work item that creates a module mint its seam rows header-first, `trajectory_arch.interface_findings` warns on modules with no declared seam, and `gen_arch_map.py` harvests module headers, not symbol docstrings. Query 1's "contract or internal standing" must migrate these explicitly. A `source`/`sink` Notes token already plays the internal role for two of the three connectivity warns; whether the new standing replaces those tokens or adds a fourth declaration is open (revision 13). Citations on symbols are also a grammar change: today a contract body is one per owning module, read from its docstring, so `gen_arch_map`, `trajectory_arch` and the strict body gate are rewritten for it.
- **Generated IF cells need roles** (revision 12). See "Open after revision 12" in the rulings section.
- **Will the interface carry the requirement, or only reach it?** (owner's follow-up, 2026-10-12; a clarification of the "Every LLR then needs an interface" bullet above, not a ruling.) The 55 LLRs in modules with no IF are not all one case. Worked sample, the 12 LLRs on `traj_render.py`: LLR-087 ends "seams terminate at the correct ports", and nothing in the LLR defines "correct" (TC-089's tests carry what meaning there is); LLR-100 names markup (`<nav class="crumbs">`), and TC-103 asserts handler text (`trail=trail.slice(0,i+1)`) though its stated `expected` is the user-level outcome; LLR-101 is behavioural (no `role=img` svg over a focusable descendant), and TC-104 deliberately avoids pinning the implementation. All three verify the generated dashboard HTML, which is the user's view, but by parsing markup, never by running a click or measuring focusability in a browser. The suggestion: point them at one boundary-artifact interface (the dashboard HTML as delivered, whose contract is the bounds a user relies on), rather than minting call-seam IFs for the renderer's internals, which OI-48 declined as describing library usage. Before any LLR is attached to an interface, test it three ways (as first stated; tests (2) and (3) corrected in revision 14): (1) is its pass/fail wording defined in the LLR itself ("correct" fails), (2) does it state what the user observes, not the markup or handler that produces it, (3) do its TCs exercise the interface the LLR is attached to, at the level the user sees it? This is what keeps the item 11 migration from re-opening the spine: an LLR that fails (1) or (2) moves under the interface by rewording, and gains nothing from the move. Handoff: [`item-11-llr-interface-check-handoff.md`](item-11-llr-interface-check-handoff.md). **Answered in revision 14** ([`item-11-llr-fitness-report.md`](item-11-llr-fitness-report.md)):
  - **Counts.** The 55 reproduces; the handoff's 90 / 64 does not. 68–83 of 302 LLRs are fit as written, 215–226 need rewording and 4–8 need reframing or retiring. The rewording is almost all names of code symbols and narrated mechanism, which ruling 5 already requires removing.
  - **Tests (2) and (3) were mis-stated.** An LLR's observer is the consumer of its component-level seam, not the end user; held to the user's view, every LLR becomes an SR. The corrected tests are in the report.
  - **An owned IF is not a carrying IF.** IF-011, the renderer's only seam, is an exit code. The dashboard HTML has no IF row at all, and 21 LLRs are observable only there.
- **Blast radius becomes mechanical:** a changed file → its component → the interfaces on that component's boundary → the requirements those interfaces carry → the TCs verifying them. That answers the owner's "what is at risk when a component is updated".

**Scope.** A large program that belongs with item 5's migration, sequenced last. It touches the code tags (about 900 `Implements:` lines become contract tags), the IF schema (a requirement list in, generated owner/consumer cells per item 5), the CMP derivation, and the checks that read either.

**Downstream.** A schema and tag-grammar change for adopters, carried in item 5's RESYNC entry.

**Where every item 11 call stands after variant F** (revision 15 consolidation). F is still the owner's position, for confirmation; "answered" means F gives an answer, not that it is ruled. The lists below this table are kept as raised, as history.

| Call (as raised) | Status | Where |
|---|---|---|
| `Implements:` retires, or both tags kept? | **Answered:** kept and sparse; links back encouraged, measured by the dial. Ruling 5's "code references up to its requirements" stands, and the minimum profile works unchanged | F points 3 and 5 |
| IF names the LLRs or SRs it carries? | **Superseded:** the direction is reversed. An LLR names the IF it constrains; the SR side is derived through the crossings and the assumption bridge. No IF-side list exists, so OI-67's removal and the 2026-09-20 `realizes` rejection **stand** | F points 3 and 7 |
| Every LLR carried by an interface? | **Answered: yes, at some level; no seam is minted for it** (wording, revision 16). Every LLR is verified at its own interface or its parent's; interfaces are required at every architectural boundary. Whether each LLR *names* its interface is F-call 8: **not required** (owner, revision 17) | F point 3, F-call 8 |
| Files declare their component; LLR → CMP checked or derived? | **Answered:** the file header (or the PART/ASSET row) declares it, and LLR → CMP **retires**. That amends ruling 5's "LLRs keep naming their component by id", a reversal to overrule explicitly. IF → CMP is F-call 1 | F point 1, F-call 1 |
| Must a requirement-bearing IF allocation be Approved? | **Dissolved:** no IF row bears requirements. IFs are approved just in time at the level of use, through the sitting of the row they serve, judging payload compatibility, not class alone (revision 16) | F point 4 |
| Contract citations never mandated per function; what checks an over-claim? | **Answered in part:** never mandated (links back encouraged). The over-claim check is the authored owner component, F-call 1 (i), confirmed in revision 17 | F point 5, F-call 1 |
| WIs name the interfaces they serve (`if_refs`)? (query 2) | **Still open.** F doesn't address it. A possible derivation to weigh: a WI's touched LLRs → the IFs they constrain | — |
| Decomposition (a) or (b)? | **Still open; F leans (b).** With `part_of` the component tree is the one decomposition. New question for (b): does a deeper LLR point to its SR, to a parent LLR, or is its parent derived from the component tree (the LLR on the enclosing component's boundary)? | F-call 5 |
| Terminology: "module" | **Still open.** Fable's recommendation stands (module = source file; "realization artifact" for the bound unit) | — |
| How IF roles and external owners are declared | **Narrowed:** the owner is F-call 1, confirmed as (i) in revision 17. Consumers and requestors must resolve before any derivation; whether they are authored component ids or generated from typed citations is still open | F-call 1 |
| Rev 14: variant E or A–D? | **Superseded by F** (the owner's refinement of E) | F |
| Rev 14: mint a delivered-dashboard interface? | **Adopted in F,** with the other delivered-artifact and CLI interfaces judged one by one | F (agrees with E) |
| Rev 14: a reach dial or a gate? | **Answered: no gate.** Whether to measure reach as a dial is a minor, open detail | F point 3 |
| Rev 14: SR-180's replacement | **Answered:** SR-180, LLR-180 and TC-175 retire, and new ids carry the rule (structure at the commit, meaning by the reviewer, results at the gate) | F point 6 |
| Rev 14: fitness at touch; the guidance fix in phase 1 | **Fitness at touch adopted in F.** Scheduling the `spine-questions.md:218` fix is still open | F (agrees with E) |
| Rev 14: interactive dashboard evidence | **Answered (owner, revision 17): executed in a browser** (Astra's view), off the commit bar. The dashboard aids browsing and has no bearing on the delivered product, so it runs as an on-demand `run.cmd` action or every *n* WIs; the cadence is open. The handler-text pins (TC-057, TC-090, TC-103) are replaced. **Every view states when its checks last ran** (owner, revision 17), the interaction check and the render critique, so a reader can tell a stale picture from a broken one. The stamp is read from the newest observation record (`docs/test/observations/`, which already carry `observed_at`, the judged hash and an expiry), not the clock, so the generated page stays byte-deterministic | — |
| Rev 14: the 114 IF `data` cells naming code | **Still open, and sharpened:** under F a `data` cell becomes a value domain, generated from the code's contract body (F-call 9, revision 17), so each `call` row's body is reworded to a domain or the row retired | F points 4 and 8 |
| Item 11 and OI-112 are one question (rev 13) | **Answered, corrected in revision 16:** F takes (b)'s direction at LLR level, with the SR side derived, **and** (a)'s mechanism, with IFs approved through the sitting of the row they serve. OI-112 itself calls (a) a prerequisite of (b). The sitting judges meaning and payload compatibility, not class alone. (c) is declined. Revision 15's "(a) not adopted" was wrong. OI-112 can be ruled from F | F points 3 and 4 |
| Items 11 and 5 overlap (rev 13) | **Narrowed:** F keeps `Implements:`, so no reversal there; the one reversal left is LLR → CMP (above) | F point 1 |

**Owner calls as raised (revisions 9–14; history, statuses in the table above):**

- Code points up only to interfaces (`Implements:` retires), or keeps both tags? Retiring it amends ruling 5's "code blocks reference up to their requirements", and needs a rule for the minimum profile (revision 13).
- Interfaces name the LLRs or SRs they carry (overruling OI-67's removal and the 2026-09-20 rejection)? Or LLRs only, with the SR side derived through `boundary_refs` and the crossing cells (revision 13)? Either way, rule the direction once with OI-112.
- Every LLR must be carried by at least one interface (adding `call`-channel seams for the 55 LLRs in modules with no interface, or reframing them)?
- Code files declare their component; IF component is derived. Is LLR → component kept as checked allocation, or derived? "Derived" amends ruling 5's "LLRs keep naming their component by id" (revision 13).
- IF rows already carry `Drafted` · `Approved` under `DevStg-Arch` authority: must a requirement-bearing allocation be Approved, and amended only under that authority (revision 12 reword)?
- Are contract citations never mandated per function, and bounded to symbols that actually realize the seam (query 1)? And what checks an over-claimed citation?
- Do work items name the interfaces they serve (`if_refs`), replacing or beside `sr_refs`, with `needs` checked against or derived from the interfaces' provider and consumer order (query 2)?
- Decomposition: (a) SRs at every component scope with a terminal LLR (today's text, which seems to lack a sub-scope SR → parent pointer), or (b) SRs only at the system boundary with LLRs decomposing recursively (the owner's leaning, on churn grounds)? Astra (revision 12) confirms no SR cell names a parent SR or a component scope, and no LLR a parent LLR, and recommends (b) with an acyclic parent-LLR link, SR-root reachability, a CMP `part_of` scope check and evidence that children together satisfy each parent.
- Terminology (revision 12): keep "module" for the software source file and name the wider realization units separately (component, part, asset), or keep one word for all? Fable (revision 13) recommends "module" for the source file, the kit's existing "realization artifact" for the bound unit, and PART/ASSET as acquisition rows under a component, dropping "the part's file".
- How the IF roles (owner, consumer, requestor) and external owners are declared once the cells are generated (revision 12; see the rulings section's "Open after revision 12")?
- **Revision 14 (the fitness analysis; the full list and reasons are in the report's "Owner calls"):**
  - Which direction: variant E (recommended), or A, B, C or D?
  - Mint a delivered-dashboard interface, and judge the other delivered-artifact and CLI seams one by one?
  - "LLRs reachable from a code-cited seam": a measured dial with a closed internal allowance, or a gate?
  - SR-180's replacement: is discharge kept separate from reachability, with structure checked at the commit, meaning by the reviewer, and results at the gate?
  - Do the corrected fitness tests apply when a row is touched (rubric plus item 5's text check), with the authoring-guidance fix pulled into phase 1?
  - Interactive dashboard evidence: claims limited to the delivered document with interaction checked by inspection, or a browser harness (a dependency-ledger row)?
  - The 114 IF `data` cells that name code: classify the `call` rows (cross-component seam or helper usage) before item 5 rewords any?

**Astra's views (revision 12, not rulings).** The full views on each call are in [`reviews/astra-low-r11.md`](reviews/astra-low-r11.md). In brief: one authored trace through IFs, `Implements:` retiring only in one coordinated migration with its replacement checks; one IF → obligation list, with a semantic check of its own; every *leaf* obligation needs an observable realization, not decorative helper seams; keep LLR → CMP as independent design intent, since deriving both sides from one header is circular; `if_refs` optional *beside* `sr_refs`, with `needs` still authored and IF relations used for advisory overlap; and review is acceptable for semantic realization, beside the structural checks.

**Fable's views (revision 13, not rulings).** The full views are in [`reviews/fable-medium-r12.md`](reviews/fable-medium-r12.md). Where they add to Astra's: retire `Implements:` only in one migration gated on "every LLR reachable through a code-cited IF, or declared unreachable with a reason"; an authored IF → LLR list (SR derived), with its direction ruled once with OI-112; no `call` seams minted to satisfy a rule, with a closed "internal" allowance instead; component headers on software source files only; IF approval through the sitting (OI-112's (a)); keep an authored, role-bearing owner id per IF, the one independent check of an over-claimed citation; `if_refs` beside `sr_refs`, IF order used to warn on a missing `needs` edge, never to derive one. On decomposition, (b), on conditions: leaf versus aggregate derived from having children, one parent link per row, a leaf discharged by realization and a parent by its children plus an integration TC, shipped in item 5's schema WI as one RESYNC entry. Under (b), Gilbert's sub-scope SRs (SR-012's rig) would become parent LLRs with no artifact. Its contract sample counts 7 of 20 bodies mixing (Astra: 11 of 15); the difference is whether a rationale sentence counts, and Fable proposes the rule "a bound may carry its reason; it may not state what a caller must achieve".

**Recommended variant E (revision 14, not a ruling; refined by the owner into variant F, revision 15).** Two independent analyses of all 302 LLRs reach this on their own, and the integrator's checks confirm it ([`item-11-llr-fitness-report.md`](item-11-llr-fitness-report.md)).
- **Why not A.** A would not reduce rework. The defects that cause churn are symbols and mechanism in LLR text, and ruling 5 already removes them. A replaces about 527 code-side anchors with at least 508 authored links (302 or more IF → LLR plus about 206 code → IF), before file headers. It also adds an allocation that a seam split reopens.
- **What E keeps.** Code → LLR (`Implements:`), so ruling 5 stands as written and the minimum profile still has a path from code to its LLRs. LLR → CMP stays authored design intent. File component headers are deferred.
- **What E adds.** One delivered-dashboard interface and a few more delivered-artifact and CLI seams. IF → LLR only on interfaces that genuinely carry the behaviour, each reviewed, with the SR side derived. A reach dial with a closed internal allowance; no `call` seam is minted to satisfy a rule (OI-48).
- **Where the fitness tests go.** The three corrected tests go into the spine-authoring rubric and item 5's commit-time text check, applied when a row is touched. A 302-row gate is not used: the analysts disagree on 7 of the 15 rows both read by hand, so a fitness gate would itself generate review rounds.
- **The way back to A.** E can grow into A later without discarding anything.

**Variant F: the owner's refinement of E (revision 15, corrected in revision 16 after the Astra and Fable reviews; the owner's positions, for confirmation, not yet rulings).** It is kept as its own letter so the record shows what came from the analysts (E) and what from the owner (F), and so a later review can judge one against the other.

F agrees with E on four things: keep `Implements:`, no rule that every LLR is carried by an interface, mint the delivered-dashboard interface, and judge fitness when a row is touched. It goes further in seven places:

1. **One home for component membership: the realization.** A code file declares its component in its header. A part or a fetched asset declares it in its PART or ASSET row. The kit's PART/ASSET schema already carries `Component` (PART also has `IF-Ref`, the same shape as a file citing its contract), but **Gilbert fills neither, and has no CMP rows yet**, so its partition is a migration cost, not a working example (revision 16). A non-code shipped file declares its component in the same `#` header that holds its `Contracts:` marker (PROCESS.md §8); a file type with no comment syntax (CSV, HTML) is declared on its `boundary` entry in the shipped-file inventory, never in a second list (revision 16). **LLR → CMP retires.** Today the fact has two homes: 150 of 243 IF rows and all 302 LLRs carry a `component` cell.
2. **Files are created at design time.** When LLR and IF rows are written, their files are created as stubs: a component header and contract markers. This is PROCESS.md §8's existing "mint header-first" moved from the work item that creates a module to the design step.
   - **What a stub settles** (revision 16). A stub establishes *file* ownership before code exists. It does not by itself give a particular LLR a realization home, since it carries no LLR link; an LLR is placed by the interface it names (point 3). The test-first check and coverage dial never count a stub. Two views:
     - **The owner's position** (with Fable): mint the scope's stubs at `DevStg-Arch`.
     - **Astra:** mint a stub only where coordinated work needs the file allocation, leaving file layout an implementation choice otherwise.

     The choice is F-call 2's.
   - **Early work items stop clashing.** The first WIs no longer build a file structure around each other.
3. **No IF → LLR list.** Every defined behaviour is verified, either itself or through its parent. That is why an LLR exists: to be a testable point of reference.
   - **Where it is tested.** At the interface where its behaviour can be observed, often an outer one: many renderer LLRs are testable at the delivered dashboard. The test can be direct or a rubric.
   - **How the link is recorded.** Only where the test drives a separately measurable interface does the TC's `verifies` name that IF beside the LLR. That cell is the single home of "this LLR is checked at this interface"; nothing on the IF side repeats it.
   - **Blast radius** (revision 16) is derived as the union of two relations: the inverse of each LLR's named IF, and each TC's explicit observation IF, then on to the TCs verifying those LLRs. It is *potential* impact, not proof of exhaustive coverage; optional back-links and kernel exemptions bound its completeness.
   - **An LLR that constrains a defined interface names it** (owner, revision 15, refining the bullet above). Such an LLR states what must hold across that interface: the mapping from its input domain to its output domain. It names that IF by id, in the requirement → IF direction of OI-112's option (b), which also settles "rule the direction once with OI-112".
     - **A TC repeats nothing.** It names an IF only when it tests at a *different* interface, such as the outer delivered dashboard, so "checked at" and "constrains" each keep one home.
     - **An LLR with no defined interface of its own** is verified at its parent's interface, as above.
     - **Revision 16, from Fable: should every LLR name an interface?** With LLR → CMP retired and back-links optional, an LLR that names no IF has no component, no scope and no place in the derived architecture view. Today all 302 are placed by their `component` cell, and 72–74 carry no `Implements:` tag. Fable proposes one required cell per LLR naming the interface at which it is *observed*, its own or the enclosing boundary's: the same count as the `component` cell it replaces. That reverses the owner's earlier "not strictly required" and is **F-call 8**. **The owner keeps "not strictly required"** (revision 17): an LLR may not sit on a component's edge, and as long as it drives a behaviour test, that test runs on an interface, from which its placement is derived.
     - **The cell is a traced cell** (revision 16), like the `component` cell it replaces. OI-14: "`LLR.Component` is a traced cell, so no re-attest window opens". An interface split, merge or retirement re-points it mechanically through the retire/successor act, never through a sitting. Otherwise F moves refactor churn onto Approved requirement rows, the churn the fitness report rejected for A.
     - **What checks the cell** (revision 16). The sitting asks "does the named interface carry what this row constrains?" (a new `spine-questions.md` §3 question). A commit check refuses a TC that names its own LLR's IF. Where the LLR has an `Implements:` file, that file must be the IF's owner or a listed endpoint. This answers OI-67's "verified by nothing" for the new cell.
   - **Where interfaces are strictly required** (owner, revision 15): wherever the architecture draws a boundary, at any depth. That means the system boundary, plus every component and sub-component boundary a decomposition creates; the 2026-08-13 form rule already applies each shall "to interfaces going to the respective component level". Inside a component, interfaces are optional: the seam rule checks only cross-component edges (WI-064), and OI-48 separately exempts edges into a declared kernel (revision 16). A TC never mints an interface; it names one the architecture drew.
   - **The real gap risk** is a component drawn too coarse, not an LLR without an interface. The lane is the example. Planning, build, review, integration and handback all sit in CMP-008 W3 Autonomy, which holds 60 modules and 54 internal seams. So the stage handoffs are internal seams that nothing requires, and the stage sequence lives only in `runtime-flows.md` Flow 4. The fix is to decompose W3 into sub-components (F-call 5), which turns each handoff into a required boundary interface. Most lane handoffs pass through files (the review verdicts, IF-047; the work specs), which import analysis can't see, so those boundaries still depend on being authored and on the runtime flows.
4. **Interfaces are thin.** An IF row is a typed node joining ports: its channel class, owner, consumers and requestors (136 IFs have requestors and no consumers, IF-175 among them, so requestors are an endpoint role, not a detail (revision 16)).
   - **One home for the contract** (revision 16), from Fable. Today the row's `data` cell and the code's `Contract IF-NNN:` body both describe the payload. PROCESS.md §8 already says "the definition lives beside the code, and only there". F-call 9 picks one home: the body in the owning file's header, minted header-first in the stub, with the row's `data` cell generated from it; or the reverse. **The owner picks the code body** (revision 17), so the code states what it is committed to where it is implemented.
   - **Approval** (revision 16) takes OI-112 (a)'s mechanism: the IF is approved through the sitting of the row it serves, at the level of use. Class compatibility alone is not enough, since two incompatible file schemas share a channel class. That sitting also judges the payload's compatibility with what the row constrains, and the counterpart effects; `reviewer.template.md` already requires an independent semantic decision on both sides of a changed requirement–interface relation.
   - **Mechanizing** that approval comes last.
5. **Links back to the spine are encouraged, not mandated** (item 5's per-module floor is withdrawn). The trade is discoverability against rot, and the dial measures it.
6. **Id continuity.** A row keeps its id when amended only if its meaning stays close to the original purpose. In practice that means three things hold:
   - most existing links stay valid;
   - the rest can be updated with confidence;
   - a missed one, such as another repository citing the id, would not mislead.

   Otherwise the row retires with a successor record and new ids are minted. SR-180, LLR-180 and TC-175 retire outright, and new ids carry the new discharge rule. The kit already says ids are "never reused" (PROCESS.md §2) and splits amendments into CLARITY and MEANING (§4), but it never says when an amendment must become a successor. This rule fills that gap: a CLARITY amendment keeps its id; a MEANING amendment keeps it only under the test above. Re-pointing a traced cell (point 3) opens no re-attest window (OI-14) (revision 16).
   - **SR-180's successor** (revision 16), from Astra. Retiring SR-180, LLR-180 and TC-175 needs a stated successor obligation and its evidence, not just new ids. WI-472's rationale separates per-LLR realization discharge from a blanket back-link obligation. So the per-LLR discharge criterion is stated independently of the coverage dial: a structural relation checked at the commit (the LLR's named IF is cited by code, and a TC verifies the LLR), meaning by the reviewer, and results at the gate.
7. **The SR side is derived through the assumptions too.** Where a boundary crossing can't be measured, an assumption turns it into an interface that can, and that permits the connection. The links already exist: 17 DA rows carry `effect_at` naming a crossing, 9 IFs carry `bridged_by` DA ids (IF-013 by DA-001 and DA-002), and 3 surrogates `emulates` an external party. So SR → `B-xx` reaches an IF either directly (`interface_to_external`) or through a bridging DA. Some of this assumption work is still in the WI queue.
8. **Interfaces carry problem-oriented state; boundaries keep dependencies sparse** (owner, revision 15).
   - **An interface's value domain is closed** (corrected in revision 16; both reviewers). It is an enumeration where the values are finite and mutually exclusive, and otherwise one declared schema that admits exactly the well-formed shape (ruling 1's form is a closed grammar, not always an enumeration). Use tagged alternatives for mutually exclusive states, products for independent dimensions, and ranges or structured payloads where the data is numeric or structured. Of 243 `data` cells, 68 are alphabet-shaped; the `file`, `stdout`, `bytes` and `git` rows mostly carry schemas or documents (IF-047 carries a verdict, a findings count and free finding text). Test equivalence classes are enumerated separately from the payload. The out-of-domain rule is stated either way, and an UNKNOWN is declared only where it is a real specified state. Where the values *are* a set of states, take a parcel's location: one enumeration (MAILBOX, SORTING FACILITY, TRUCK, UNKNOWN) carries exactly the 4 valid cases, where four booleans carry 16 values, 12 of them invalid. Invalid states are unrepresentable by construction, and no value is carried twice.
     - **Two kinds of "unknown"** (research, revision 15). An UNKNOWN that is a real problem state needs declared behaviour, ruling 1's "declared rule for everything else". An out-of-domain input is instead rejected at the boundary ("parse, don't validate"; category-partition's `[error]` choice). Otherwise a catch-all absorbs real missing cases, and coverage passes trivially.
     - **Flags are not always wrong.** A product of flags is right where the dimensions are truly independent (statechart AND-regions; `--strict` and `--json`). The smell is a flag passed across a boundary to select the receiver's behaviour, which the literature calls *control coupling*.
   - **This extends ruling 1.** A WI spec facing an open input space chooses "an enumerated allow-set plus a declared rule for everything else"; here the same rule is applied to interfaces. The contract (the owner's term) is then the interface's value domain.
   - **Component boundaries are placed to keep each output's inputs few** (arithmetic corrected by the research, revision 15). Three rules:
     - **What to count.** An output's cost is the product of the number of equivalence classes of each input it depends on, the component's own state included. This is Schroeder and Korel's *input-output relation*.
     - **What a split saves.** One test drives every output at once, so a component's exhaustive suite covers the *union* of the per-output cases. Take a 4-state and a 2-state input, where one output depends only on the 2-state input: the component still needs 8 cases, split or not. A split there buys proof and blast radius, not cases: "this output ignores that input" becomes structural rather than claimed.
     - **Where the case count drops.** It drops where an output is reached only through a **narrower intermediate value**. Inputs of 4, 4 and 3 states need 48 cases as one component. If the output depends on the first two only through a 2-state intermediate, splitting there needs 16 + 2·3 = 22: the product becomes a sum. This is why the intermediate domains must be stated during breakdown, and it holds only if the intermediate value is the *whole* channel.
   - **The domains must exist before the split.** This presumes the domains, intermediate ones included, are stated during problem breakdown.
   - **Established names**, sourced in [`item-11-value-domain-research.md`](item-11-value-domain-research.md), each with the verification status the report marks (verified, record only, unverified) (revision 16); its vocabulary list is proposed for the spine-authoring rubric:
     - "make illegal states unrepresentable" (Minsky), with sum types against product types;
     - "parse, don't validate" (King);
     - the SCR/Parnas tabular method, whose mode classes are enumerations and whose condition tables are checked for **disjointness and coverage** (no input fits two cases; every input fits one); and Parnas and Madey's four-variable model, in which requirements speak only of quantities the system monitors and controls;
     - MECE, as a gloss only (the checkable form is disjointness and coverage);
     - Axiomatic Design's Independence Axiom and its uncoupled, decoupled and coupled design matrices (Suh), with the Design Structure Matrix (Steward, Eppinger). Suh's Information Axiom is a probability of meeting tolerances, not a case count, and is not the measure here;
     - information hiding and coupling (Parnas; Stevens, Myers and Constantine);
     - the category-partition method (Ostrand and Balcer), with pairwise testing (already in `gen_cases`), and input-output relation testing (Schroeder and Korel).

| Link or rule | E | F |
|---|---|---|
| Code → LLR (`Implements:`) | kept; coverage dial | kept, sparse; any link back (tag, contract, a link within the same artifact) counts |
| IF → LLR | authored on carrying interfaces (about 100–150 cells, reviewed) | **none on the IF side.** An LLR names the IF it constrains (requirement → IF, OI-112 (b)), as a traced cell, not required (F-call 8, owner): an LLR naming none is placed through the IF its verifying test drives; a TC names an IF only when it tests at a different one |
| Interface value domain | not addressed | **closed:** an enumeration where finite, otherwise one declared schema; an out-of-domain rule either way; boundaries placed to keep dependencies sparse (point 8). One home for the contract: the code body, the row's `data` cell generated (F-call 9, owner) |
| IF → SR | derived through `boundary_refs` and the crossing cells | derived the same way, **plus the assumption bridge** |
| LLR → CMP | authored design intent | **retired** |
| File → CMP | deferred | **declared in the file header**, or in the PART/ASSET row for a physical realization; created at design time |
| IF → CMP / IF owner | an authored owner id that names its role | **the producing component's id**, the existing optional `component` cell made the required owner; the path leaves `owner` (F-call 1 (i), confirmed in revision 17) |
| IF approval | through the sitting (Fable) | OI-112 (a)'s mechanism: through the sitting of the row it serves, at the level of use; judges payload compatibility and counterpart effects, not class alone |
| Where an IF is required | delivered artifacts and carrying seams; no `call` seams to satisfy a rule | **every architectural boundary at any depth** (system, component, sub-component); optional inside; components decompose recursively (F-call 5) by the descend test (F-call 6) |
| Id amendment | retire or re-mint | the continuity rule above |
| Authored links, against E | n/a | **Unknown until measured** (revision 16). F removes about 300 LLR → CMP cells and E's 100–150 IF → LLR cells, but adds up to 302 traced LLR → IF cells, 117–150 file headers, `part_of` cells, endpoint roles and residual TC observation links. Revision 15's "about 450 fewer" omitted F's own links. Recount on a migrated slice before claiming a saving |

**F's open calls:**
- **F-call 1: how an IF reaches its component.** **Confirmed by the owner (revision 17): (i),** with OI-67 (a)'s header text amended as below. Three positions, after the revision 16 reviews:
  - **(i) Authored component id** (Astra's pick). The IF owner is the producing component's id, as design intent, with typed realization citations checked against the owning file's header. These are two facts, so the check is not circular. **It amends OI-67 (a)'s header text** ("`owner` is the providing THING … NEVER a requirement or design id"). That text was written against requirement-owned seams that couldn't be traced to code. A component id traced through file headers is traceable, but the amendment must be explicit.
  - **(ii) Generated from a typed owner citation** plus the file header: ruling 5's generated-cell path, one home, but no independent check.
  - **(iii) Keep the authored module path** (Fable's pick), deriving IF → CMP from that file's header, with the existing stray-declaration rule as the check. **It conflicts with ruling 5** ("IF and CMP rows name no code") unless the owner amends it.

  Endpoint roles (consumers and requestors) resolve first, before any derivation. External parties stay authored ids (`external:git`). A file-channel producer such as IF-047's `docs/reviews/` needs an explicit owning component. Declared-kernel owners (12 `kitlib` IFs) are skipped by the boundary derivation.

  Either way, a file that serves no requirement-bound interface still declares its component in its own header, so the owner's worry about such files doesn't decide this call. The owner was undecided at revision 16, and confirmed (i) in revision 17.

  **The integrator recommends (i)** (revision 17, not a ruling). F-call 9's answer puts the contract body in the owning file, and the body marks that file, so (iii)'s path is no longer needed to find the header. What the path still adds is an independent check at file level, which is the cell ruling 5 removed, since every file rename or split would edit an IF row. (i) keeps the independent check one level up: the row names the owning component, and the file holding the body must declare that component in its header. A move inside the component touches no row; a move into another component's file fails. The cost is the explicit amendment of OI-67 (a)'s header text, "NEVER a requirement or design id", to "a component id or an `external:` party, never a requirement id". The 31 rows owned by a plain file or directory each need a named owning component, which F already requires of file-channel producers.

  **What points at a component, and where F-call 1 sits** (revision 17, the owner's question). Today two cells name a component: every LLR's `component` (302) and the IF row's *optional* `component` (150 of 243), beside the path-valued `owner`. The schema also has PART/ASSET `Component` and CMP `part_of`, both unfilled here, and no code file declares one (0 of 117). Under F:
  - **Authored:** a file's header (or its PART/ASSET row) → its component; `part_of` → the parent component; and the IF owner → its component, which is **F-call 1, the only open link of the four.** Consumers and requestors resolve to components too, and how is still open.
  - **Retired:** LLR → CMP.
  - **Derived from those:** an LLR's placement (through the IF it names, or the IF its test drives, F-call 8), an IF's placement in the views, each component's boundary set, a file's ancestry, and depth.

  So every LLR's placement runs through F-call 1. With the contract living in the row until the build (F-call 9, one home at a time), only (i) gives an interface an owner during decomposition. Under (ii) there is no code to generate an owner from until the build; under (iii) the path names a file the design has not chosen. And (i) needs no new cell: it makes the existing optional IF `component` cell the required owner, redefined as the producing component, and takes the path out of `owner`.
- **F-call 2: the design-time stubs.** At which rung are files created, and what may a stub carry? The test-first check must not count a stub as implementation. Revision 16 adds the scope question: every file of a scope at `DevStg-Arch` (the owner's position; Fable notes that 0 of 117 `.py` files carry a `Component:` header today, so the grammar is new and belongs in `gen_arch_map`'s header reader), or only where coordinated work needs it (Astra). Either way, a stub establishes file ownership, not an LLR's realization.
  - **Owner's answer (revision 17): not every file.** Stubs are minted where the design needs them. The builder may mint new files, but must take great care not to duplicate something that already exists, whether as an exact copy or in intent. Duplication is the curse of maintainability.
  - **Integrator's notes** (not rulings).
    - **No stub is required** (corrected in revision 17 after the owner's query). An earlier note required stubs for interface-owning files to hold the contract body; F-call 9's "one home at a time" removes that. A stub is the builder's choice, made at the start of the build. Its one use the process relies on is giving a test written first something to call, so that its red is a real failure (item 13).
    - **What guards against duplication today, checked.** PROCESS.md §3 states the rule ("one fact, one home"; the 0→A→B rule). `check_dupes_census.py` measures exact duplicate function bodies and is warn-only forever: the owner tore down its gate (D-7, 2026-08-10) after 93% of its findings proved to be accepted idioms. The plan-decomposition rubric's B1 catches a planned seam that near-duplicates an existing IF.
    - **The gap.** Neither the builder's instructions (`kit-builder.md`, `worker.template.md`) nor the reviewer template (`reviewer.template.md`) asks about duplication. Duplication in intent can't be mechanized, so this is text, not a gate (D-7 stands). The builder searches before minting a file or function, and names the nearest existing home it considered. The reviewer asks of each new file and function: does it repeat, exactly or in intent, something that already exists?
- **F-call 3: when a TC names an interface.** Confirm that a TC names an IF only where it tests at a *different* interface from the one its LLR names (revision 16 wording), and that a commit check refuses a TC naming its LLR's own IF. Exercise the rule on four cases: a same-interface TC, a dashboard-level integration TC, a TC spanning several LLRs, and a kernel LLR observed through an outer interface.
- **F-call 4: where the id-continuity rule lives.** Write it into PROCESS.md beside "never reused", tied to the CLARITY/MEANING split.
- **F-call 5: components decompose recursively.** A sub-component is linked to its parent component by `part_of`, with a scope check, as Astra suggested in revision 12. **The CMP schema already carries `PartOf`** (`kitlib/spine.py`, read by `coherence.py`, `trace.py` and `check_trajectory.py`), empty on the kit's four rows, so this is a change of use and constraints, not a new cell (revision 16 correction). Each sub-component follows the same rule: interfaces at its boundary, freedom inside.
  - **First test case:** W3 Autonomy. The dry run judges candidate cuts on evidence; it is not required to reproduce the lane's stages (item 12, revision 16).
  - **The depth-0 frame stays locked** at four components; sub-components sit under it.
  - **It ties to decomposition (b)** (SRs only at the system boundary, decomposed recursively by the architecture). The recursion would be carried by the component tree and its interfaces, and LLRs hang off it through their TCs.
  - **What is authored and what is derived** (owner, revision 15).
    - **Authored:** `part_of`, one cell per component naming its parent. It is the only authored *containment* link. The nesting can't be derived from the interfaces, because many groupings fit the same edges (a chain A → B → C could be {A, B} plus C, or A plus {B, C}). Choosing which boundary to enclose is the design decision, which is OI-14's "formative" partition.
    - **Derived from `part_of` and the IF → component map:**
      - an IF's *placement*: the lowest common ancestor of all its endpoints (owner, consumers, requestors). Placement only, for the views. Adding an external consumer can raise it to the root without changing any obligation (revision 16);
      - a component's boundary set, the IFs with one end inside and one outside, possibly crossing several nested boundaries;
      - an LLR's scope: the component of the producing side of the IF it names (the IF's owner), which stays stable when consumers change. It is **not** the LCA (revision 16, reconciling Astra and Fable);
      - a file's full ancestry, from its declared leaf component;
      - depth, which sets the critique cadence (item 12).

      An `external:` IF resolves to the system root, and edges into the declared kernel stay exempt (OI-48).
    - **Check C** (a dependency matrix per component) may *suggest* groupings; it never defines them.
  - **Not a second decomposition, but not a refinement proof either** (revision 16). Under (b) there is one *structural* tree. The component tree is the decomposition, IFs sit on its edges, and LLRs are *placed* on it by the IF they name (F point 3). Placement is not behavioural parentage: an enclosing component doesn't say which obligation a child refines, and several LLRs can constrain one interface (LLR-080 and LLR-181 span several modules). So F's (b) is **flat LLRs with direct SR roots**: each LLR keeps its `sr_refs`, and SR → LLR coverage and the orphan rules stand. An authored refinement edge between LLRs is added only if a trial shows aggregate obligations are needed. The test case is Gilbert's SR-012 rig. Containment never stands in for that proof. PROCESS.md §4's ladder text ("TERMINAL", "the tier does not recurse") changes with (b), and its approvals, orphan rules and adopter migrations are named together.
    - **Under (a),** sub-scope SRs would form a second tree that nothing links to the component tree. That is a further argument for (b).
    - **This is the standard product breakdown structure,** or bill of materials, or SysML composition. It is the owner's 2026-07-09 framing, "as a physical part does its assembly". Gilbert's schema has the `Component` columns, but no rows fill them and it has no CMP rows, so populating its tree, and migrating SR-012's sub-scope, is part of its re-sync cost.
- **F-call 6: a test for when to descend** (owner's criterion, revision 15). The aim is to keep interface permutations few, while keeping the spine light enough to maintain. The owner's position: decompose what a stakeholder can describe as a state; stop at the values they could only choose on seeing the implementation. Proposed wording for the `spine-questions.md` list, beside its existing "Descend only where a mechanized check earns its keep" and "Record the stopping boundary". Ask of each candidate child:
  1. **A describable state: descend into obligations, not yet into components.** Can the stakeholder name the state, what the system does in it, and what moves it on, in their own words and without inventing a number? This is an SCR *mode class*. Plan → build → review → land passes. That earns LLRs and a runtime flow. **Whether the states become components is a separate question** (revision 16, from Astra). Parnas's 1972 criteria paper contrasts decomposing by processing steps with decomposing by information hiding, and favours the latter. So candidate cuts are compared on the decisions each hides, cohesion and dependency reduction. IF-175's verdict service, shared by scheduling, review filing and integration, is the warning: a stage split would cut through one shared definition.
  2. **An invented number: stop.** Is the only new content a value the stakeholder could not state *or source* today and would pick only on seeing the implementation (a 6 px gap, an 8 pt font)? The parent keeps the quality ("legible"), verified by a rubric or `Attest`, and the value lives in code or config. A binary floor ("no two wires overlap", LLR-292) is a describable state and stays. So does a number the stakeholder can source, such as one set by a standard (INCOSE's "solution free unless there is rationale").
  3. **A paraphrase: stop** (existing rule).
  4. **No pass/fail of its own: stop** (existing rule).

  Interfaces then come from the boundaries the chosen cut draws. A linear flow's n − 1 transitions are not a count of IF rows: OI-67 requires separate rows for distinct information kinds and for request and answer directions (revision 16). The judgement stays subjective at the edges. The existing "record the stopping boundary" rule makes each call reviewable.
- **F-call 7: what to mechanize, and the vocabulary.** The research is done ([`item-11-value-domain-research.md`](item-11-value-domain-research.md)). It proposes three checks, all stdlib and advisory first:
  - **(A) Well-formed value domains** over the IF `data` alphabets and the `set{...}` dimensions: duplicate labels, a catch-all with no declared behaviour, and clusters of booleans. It needs no schema change. The SR `permutations` cell already uses the `gen_cases` grammar, and none of the kit's own 131 SRs fills it.
  - **(B) SCR disjointness and coverage** over a condition table. This needs a new optional cell, which is a downstream migration.
  - **(C) A dependency matrix per component** from the import graph plus IF file edges, suggesting where a component is under-decomposed (W3 first). It is noisy, so it would be a dashboard suggestion only.

  Also for ruling: adopt the report's ten terms in the spine-authoring rubric, with its glosses for *module* and *seam*. Check A reads the one home of the contract, the code body (F-call 9, answered in revision 17); B waits for a real condition-table use and item 5's RESYNC entry; C includes requestor and file-channel edges and reports missing endpoints rather than assuming the import graph is complete.
- **F-call 8: must every LLR name an interface?** (revision 16, from Fable). Either one required traced cell per LLR, naming the interface at which it is observed (own or enclosing), so every LLR is placed; or the owner's earlier position, where the cell exists only for an LLR that constrains a defined interface, and an unplaced LLR is accepted. Fable recommends the required cell; it reverses the owner's "not strictly required".
  - **Owner's answer (revision 17): not strictly required.** An LLR need not sit on a component's edge. Its placement is derived from the parent interface it serves, or from the interface its behaviour test drives.
  - **Integrator's notes on what that needs** (not rulings). The derivation reads the verifying TC's named interface. F-call 3 already lets a TC name the IF it drives when that differs from its LLR's, and an LLR that names none differs from every IF. So for that case the TC's naming becomes a "must", and no new cell is added. Two residues remain: an LLR verified only by an Inspection, Analysis or Attest TC, and one whose test drives no declared interface (a unit test of an internal function). The derived view shows those as unplaced, counted, not gated. An LLR verified at several interfaces is placed at each.
- **F-call 9: one home for the contract** (revision 16, from Fable). Either the code's `Contract IF-NNN:` body (PROCESS.md §8: "only there"), minted header-first in the stub, with the row's `data` cell generated; or the row's `data` cell, with the body carrying only what the domain can't. The integrator recommends the body, since it already has a design-time home in the stub.
  - **Owner's answer (revision 17): the code body,** so the code always states what it is committed to, where it is implemented.
  - **Integrator's notes on the consequences** (not rulings).
    - **One home at a time** (revision 17, withdrawing the integrator's first note that the owning file must exist when the IF row is written). The design names components, not files (F-call 1 (i); the builder mints files, F-call 2), so it can't know which file to stub without making an implementation choice early. Before any code exists, there is no "where it is implemented". So the contract has one home at a time. Until a body exists, the IF row's `data` cell holds it, written at design time and judged at the sitting. When the build writes the owning file's `Contract IF-NNN:` body, the body takes over, and the cell is generated from it from then on. A commit check decides which is the home: with a body present, an authored edit to the cell fails as stale. Any change made in the move shows as drift against the approved snapshot (next note). No stub is needed to hold a contract. **The owner confirms** (revision 17): the contract orients the work during decomposition and moves into the code during implementation, provided it only ever exists once.
    - **Approval stays decidable.** The approval baseline (`baseline_snapshot.py`) copies registries, not code. So the generated `data` cell is committed, checked current at the commit, and copied with the registry at approval. A body edit then shows as drift on an approved row, like any other.
    - **The module-path owner loses its role as a locator.** The body itself marks the owning file, so F-call 1's option (iii) no longer needs the path to find the header.

## 12. Architectural decomposition, encouraged at three moments

The owner asked (2026-10-12, revision 15) how to get LLMs to decompose the architecture well at three moments: when the spine is broken down from a fresh vision, when a WI is large enough to shift the architecture, and on demand as an audit of the current architecture. Variant F (item 11) says *what* good decomposition is. This item is *where an author or a reviewer meets that definition*.

**Root cause.** The kit has no home for the definition at the step where decomposition happens.
- **The question list skips the architecture rung.** `project-trajectory/prompts/spine-questions.md` has sections for SN intake, SR derivation and LLR/TC, and none for `DevStg-Arch`, even though the ladder repeats that step per component scope (PROCESS.md §4).
- **No skill covers breaking the spine down at the architecture rung.** `spine-authoring` is the adjudicator's question list per tier, and `deep-module-design` works at the code level. Hats don't fit (owner, revision 15): the roster's questions are put to SN → SR decomposition. 126 SRs carry `hat_refs`, against 13 LLRs and no SNs or IFs.
- **No rubric judges interfaces and boundaries.** The `docs/rubrics/` set has decomposition *proportionality* and *plan* decomposition, but nothing for components and interfaces.
- **No step asks whether a WI shifts the architecture.**

The result: W3 Autonomy grew to 60 modules with its lane stages inside it (item 11, F point 3).

### Proposal: one definition, three entry points

**The shared core, stated once.** Each entry point cites it; none restates it.
1. **A rubric, `docs/rubrics/architecture-decomposition.md`,** written from variant F. Its anchors:
   - each state a stakeholder can name is a mode class, with its transitions;
   - every interface carries a closed value domain, checked for disjointness and coverage, with the two kinds of UNKNOWN kept apart;
   - boundaries sit where dependencies are sparse or an intermediate value is narrow;
   - no control coupling across a boundary;
   - interfaces at every boundary, optional inside a component;
   - the stopping point is recorded, under the "state or source" test.

   Its failure patterns: a product of booleans standing in for one domain; one meaning carried by two interfaces; an under-decomposed component. Terms come from the vocabulary in [`item-11-value-domain-research.md`](item-11-value-domain-research.md).
2. **A skill, `architecture-decomposition`** (owner, revision 15, in place of a hat). It is the procedure an authoring LLM follows at `DevStg-Arch` and when planning a WI. It walks the author through four steps: name the states, state each boundary's value domain, tabulate which output depends on which inputs, and apply the descend test (F-call 6). It cites the rubric's anchors rather than restating them, and points to `deep-module-design` for the code level below.
3. **A one-line pointer in `spine-questions.md`** for adjudicating at `DevStg-Arch`: judge against the rubric. It restates nothing.
4. **Instruments:** checks A (well-formed value domains) and C (a dependency matrix per component) from item 11's F-call 7, as evidence for the judgement.

**Entry point 1: a fresh vision.** The `DevStg-Arch` step at each component scope gets a stated output, produced before any LLR at that scope:
- the state flow, as mode classes and transitions recorded in `runtime-flows.md`;
- the scope's boundary interfaces, each with its value domain;
- a small output × input dependency table.

LLRs then attach to those interfaces, as F requires. The skill guides the author. An independent critique against the rubric runs at the scopes the cadence below names, not at every scope. `DevStg-Arch` has no approval act of its own, so the critique gates an act that exists (revision 16; see "When the critique runs").

**Entry point 2: an amendment that shifts the architecture. The planner decides** (owner, revision 15). When a WI is planned (WI-805's plan gate, item 9), the planner follows the skill and answers the architectural-delta question: does the WI add a state, add a value to a domain, make an output depend on a new input, or cross a new boundary? The answer depends on the WI's scope:
- **Within its scope:** the plan carries the architecture change explicitly (interface and domain edits, perhaps a sub-component split). Item 3's split rule separates the refactor from the feature ("make the change easy, then make the easy change").
- **Beyond its scope:** the planner hands the WI back with a proposed refactor WI. This is the existing handback, not a new path.

The plan critique judges the answer; `docs/rubrics/plan-decomposition.md` gains the question. **Nothing triggers it automatically.** The planner may consult checks A and C as information.

**Entry point 3: an audit, `run.cmd arch-audit`, on demand only** (owner, revision 15). A new action in the run menu (`[run]`, in `process.toml` once item 10 lands), shaped like the `render-dashboard-critique` skill:
1. **The mechanical half** needs no model. It runs `trajectory_arch`, checks A and C, `check_complexity`, the duplicates census and `gen_arch_map`, and writes a findings bundle.
2. **The judgement half** is an independent critique session. It reads the bundle against the rubric and ranks components by what a refactor would gain.
3. **The output** is candidate WIs or open items filed through intake. The critic never edits the spine (`docs/rubrics/README.md`).

With an empty route pool, the judgement half refuses rather than falling back (revision 8 ruling).

### First step: a dry run on W3, before building anything

Give an independent model only the drafted rubric and W3 Autonomy's current shape: its modules, internal seams, the lane's runtime flow (Flow 4) and its interfaces. Ask it for candidate decompositions, compared on the decisions each hides, cohesion and dependency reduction.
- **The rubric works if its proposal is argued from evidence**: which decisions each cut hides, which dependencies it removes, and what it costs, such as IF-175's shared verdict service. The proposal may reject a stage split. Disagreeing with the lane stages a stakeholder would name is not a failure (revision 16, from Astra; Parnas 1972: decomposing by processing steps is the weaker criterion).
- **If its proposal is unargued, or ignores a shared definition,** the rubric is fixed while it is still text.

The dry run also gives F-call 5 (recursive components) its first worked case.

**Cost.**
- **Text only (phase 1):** the rubric, the skill, the spine-questions pointer and the plan-decomposition question, about one lane.
- **Builds (phase 3, after item 11's ruling):** checks A and C, the audit action and its critique skill.

**Downstream.** The rubric, skill, pointer and plan-critique question ship to adopters as kit-owned text; the audit action ships in the run-menu template. It is one RESYNC entry; adopters migrate nothing, since everything is additive.

**Decided by the owner (revision 15):** a skill, not a hat; the planner decides on an architectural delta, with no automatic trigger (a WI beyond its scope is handed back); the audit runs on demand.

**When the critique runs during the initial breakdown** (owner's position, revision 15; gates named in revision 16). Not at every component scope. `DevStg-Arch` has no approval act; the signed boundaries are DevStg-Reqs, DevStg-Tests and DevStg-Impl. So each critique gates an act that exists. Three moments:
- **The top level.** Read as the first architecture step below the SRs: depth 0, where SRs are allocated to components and the first LLRs attach. The SRs themselves are already judged by their own sitting. **Gate:** the first LLR sitting at depth 0 refuses without that scope's critique verdict on file (the `critique-provenance` rubric exists).
- **Once over the whole tree,** when the lower levels appear complete. **Gate:** entry to DevStg-Tests, not "the build".
- **Every second level of component depth** away from the SRs, in a deep tree. A wrong split is then caught at most two levels after it is made, instead of only at the whole-tree pass. **Gate:** the first LLR sitting at that depth, as at depth 0. Component and IF rows between critiques stay Drafted. The cadence schedules the critique; it never approves anything unreviewed.

*Open:* confirm the reading of "top level", and whether the every-two-levels rule applies always or only where the tree is deeper than two levels. The "floors" here are component depths, not spine tiers: the tiers stay SN, SR, LLR and TC, and the recursion is in the component tree (F-call 5).

**How a planner picks up the skill** (owner's concern, revision 15). The architectural-delta question arises inside a WI, so the planner must meet the skill without being told each time. Today nothing routes skills to a planner:
- **The frontmatter isn't read.** A skill's `phases` frontmatter (`dev`, `gate`, `release`) only feeds `skills/INDEX.csv`; no brief reads it.
- **The planner prompt doesn't mention skills.** `plan_briefs.py` and `prompts/dual-plan-planner.template.md` name none.
- **Model-dependent discovery.** A Claude session may find a skill from its `description` ("Use when …"); a Codex planner won't.

So the reliable route is the prompt. The planner template, and WI-805's single-plan prompt when it exists, carry one line naming the skill **by its shipped path**: answer the architectural-delta question by following `skills/architecture-decomposition/SKILL.md`. `plan_briefs.assemble` fills the template body into the planner's session, so a Codex planner reads it; that line is template text and needs a RESYNC entry (revision 16, both reviewers). The skill's `description` is written to trigger on planning, as a second route.

**An architecture role** (owner's position, revision 15). PROCESS.md §1's role table gains an **Architect** row owning `components.toml` (CMP) and `interfaces.toml` (IF), the rows no role owns today. The planner wears it whenever the architectural-delta question comes up, and the author wears it at `DevStg-Arch`. *Open:* whether `runtime-flows.md` moves from the Software Engineer to the Architect. Its state flows are the Architect's mode classes; its sequence detail is the engineer's.

**Code-hygiene instruments in the audit** (owner, revision 15, from a separate session's tool list). The audit's mechanical half covers the code level beside the architecture level. In-kit, stdlib-only:
- duplication: `check_dupes_census`;
- complexity and size: `check_complexity` (cognitive complexity and SLOC);
- `check_readability`.

Optional, declared by the adopter for their own stack (CLAUDE.md: tools a downstream project needs are theirs to install, and the kit must not require them to run its own checks):
- duplication across languages: jscpd;
- dead code: knip for JS/TS (unused files, exports and dependencies), vulture for Python;
- complexity: lizard (any language) or radon (Python);
- shell: shellcheck and PSScriptAnalyzer.

The audit runs each declared tool as a step and reads its output; it never changes code. **The kit has no dead-code check at all.** Whether a stdlib one belongs in the kit (unused module-level functions found by `ast`, with the false positives of dynamic dispatch) is a separate call, not part of this item. Python examples are marked "swap for your stack".

**Found on the way:** PROCESS.md §1's role table names no owner for the CMP and IF rows. The Architect role proposed above answers it.

## 13. Review only a green tip; review test cases in stages

The owner asked (2026-10-13, revision 15) how test cases should be reviewed, and proposed an order. Once test cases exist and the WI is queued: run the lints, *then* the tests, and start the review only if both pass. The owner's expectation is that this reduces churn, but whether today's process already does it was unknown.

### What happens today (checked)

**Nothing refuses a review on a red tip.** Smoke and its budget run before each commit, so a reviewed commit has usually passed them, but that is practice, not construction:
- **The coordinator.** Its only check before dispatching a review is that the commit landed: "`git log -1` moved" (`.claude/skills/coordinator-cycle/SKILL.md:100`).
- **The unattended loop.** It schedules a review as soon as the build is committed, treating the tip as "locally green" without checking (`agent_loop.py:2259`).
- **A red smoke has been committed before,** through a chain that checked only an exit code (coordinator-cycle `references/recipes.md:412`).

**The lints aren't in the path yet.**
- Ruling 6 puts `trace.py --strict` and `check_trajectory --strict` in the commit bar after each build. That hasn't reached `session-protocol` or the recipes.
- `trace.py --strict` runs only in the gate's `traceability` step from `DevStg-Impl` on (`check.py`), and nothing in the lane cycle invokes that gate; the hook and the closure check use `--strict-integrity` (corrected in revision 16). So the kit's own gate is red on trunk under LLR-292.
- The hook's `check_trajectory --staged` ends in `|| true`, so it never blocks.
- The builder and the reviewer each run lints by instruction, with nothing enforcing it.

**Test cases are written after the code in a lane.** The coordinator dispatches Terra to author the change set's spine rows *after* the first build round (`SKILL.md:88-94`). That is the reverse of the test-first order PROCESS.md sets for `DevStg-Impl` (§7: each TC becomes a failing test before code), and the `test-first` check that reads the order from history only warns.

**How test cases are reviewed today:**
- **TC rows** are judged as text at the combined sitting ("do the test cases that claim to verify this row verify what it actually says", `spine-questions.md`).
- **Test code** has no review of its own. It is part of the code diff, and the reviewer maps each Done-when item to a covering test.
- **Pre-fix failure** is confirmed only where the diff adds a regression test. Revision 8's per-finding rule is still unwritten template text.
- **Test strength** (would this test catch a broken implementation?) is checked by no one.

### Assessment

**The owner's order is right, and it is cheap.** Review sessions are the scarce, metered resource: Codex sessions are capped, and every round costs two reviewers. Lints and tests are cheap and deterministic. Spending a review on a tip a tool already knows is red buys a finding the tool would have produced. It also reviews code that is about to change. The precedent is Gerrit's `Verified` label, which AOSP introduced to mean "compiles, passes basic unit tests" before a change can submit. Gerrit gates *submission* and lets review run in parallel. The owner's stricter form, gating the *start* of review, fits a kit where reviews cost more than checks. It also serves item 6, whose aim is "review findings an instrument would catch: 0".

**But green only removes failures; it doesn't make the tests right.** A weak test (one that asserts handler text, or passes on a broken implementation) turns green just as easily. So the gate needs a second half: review of the tests themselves, staged so each stage catches what it is cheapest at catching.

**Three preconditions:**
1. **Trunk must be clean first** (item 6, step 1). Otherwise every lane inherits a red bar, starting with LLR-292's false positive under `trace.py --strict`.
2. **The green record is made at the commit and trusted at dispatch** (item 2's record-at-event rule), not re-run by whoever dispatches. **Corrected in revision 16 (both reviewers):** the existing `Bar-Green:` is not reusable as it stands. It is written only by the lane-side *refresh*, a disposable commit made once at landing (`integrate.py`); its recognizer is refresh-specific (`kitlib/verdict.py` `refresh_attestation`); and `work_tip`'s peeling and the refresh reset rely on that recognizer. A build-round tip carries no such record. So the proposal is one common, tree-bound bar attestation, with one trailer grammar and one verifier in `kitlib`. The builder's commit carries it for the bar declared *for review*; the landing refresh carries it for the landing bar. It names the bar it attests. Review dispatch and landing each check the same record format against their own required bar, with no history search, no marker file and no second store of "green". Refresh disposability stays recognized separately and unchanged. The gate covers the attended coordinator, the unattended loop, adjudication-triggered rounds and resumed rounds.
3. **A red bar returns to the builder without a review,** inside the builder's own bound. Otherwise the churn moves from review rounds to build rounds.
   - **The bound** (owner, revision 17). Revision 16 named a bound that exists nowhere: not in `kit-builder.md`, `process.toml` or the loop. The owner sets it at about three red rounds. At the bound, the lane goes to the adjudicator to decide what to do, never on to review. This is item 4's `on_limit = "adjudicate"` shape, applied to build rounds; the setting sits beside item 4's `[review]` values.
   - **Unmet prerequisites are the scheduler's,** not the builder's. That holds for work-item prerequisites today: a claim refuses a WI that is not on the ready frontier, "unmet needs or not queued" (`integrate.py`).

### Proposal: the order, and test cases reviewed in stages

1. **Test cases first.** In a lane, the TC rows and their failing tests are written before the code, for each Done-when item. This is PROCESS.md's test-first order, restored in the coordinator cycle.
   - **Within the lane, the failing tests are the build's first deliverable,** with their red-before recorded.
   - **For a pre-claim WI,** the TCs could be named in the spec (item 9's binding advice), so the queue holds testable work.
2. **Lint.** `trace.py --strict` and `check_trajectory --strict` (ruling 6).
3. **Tests.** The commit bar (smoke plus its budget), the lane's named tests, and each new test's recorded red-before and green-after on the exact tree. This is test review's mechanical stage:
   - every new **executable** TC has a test that names it (revision 8);
   - **the red-before is a record, not a history read** (revision 16, from Fable). The commit adding a test carries the harness's red result for that node, bound to the parent's tree (the `docs/test/evidence` shape), and it is verified against the parent at the commit. `check_test_first`'s history read (`rev-list --first-parent`, warn-only) retires into it;
   - **the red must reach the test's own check** (revision 17). A test written before its code can fail only because the code it imports doesn't exist yet: a collection or import error. A test that asserts nothing would fail the same way, so that red shows nothing about the test. The recorded red-before is a failure at the test's assertion, against existing code or a stub the build writes first (F-call 2);
   - **typed evidence** (revision 16, from Astra). Red-before applies to tests for new or corrected behaviour. A characterization test for already-correct behaviour needs a stated adequacy witness, not an invented failure. An Inspection, Analysis or Attest TC (TC-209 is an un-automated Inspection; TC-035 analyses CI results) carries its declared method's independently checkable evidence at the same gate. This is a typed evidence contract, not a bypass when a test can't be made red;
   - nothing previously green has regressed.
   - **Which tests** (owner, revision 17). Only the tests allocated to or under the SRs the WI builds, not all, so the gate is cheap. A rerun of the new and changed tests is encouraged, to show they aren't flaky; a test that flips is a defect to fix, never something to re-run until green.
   - **Integrator's notes on the scoped set** (not rulings).
     - **It is derived from the spine.** The set is SR → LLR → TC → the test files that name the TC (revision 8: test files name their TC). That replaces the coordinator's hand-picked `--tests` list (`recipes.md:63`).
     - **It needs the tags first.** Today only 129 of 316 TCs are reachable from a tagged test file (101–107 of 237 files, by pattern), so an untagged test is invisible to the selection. Finishing the tags, already owed under revision 8, comes first.
     - **Changes to shared code reach beyond the SR.** An edit to `kitlib` can break another SR's tests, which the scoped set can't see. The per-commit smoke tier (60 s, ruled) and the landing bar still catch it, so they stay as they are. The scoped set is the gate's addition, not a replacement. It can be widened by F's derived blast radius, the tests of LLRs at the interfaces the change touches, which also gives a WI that names no SR a set (Fable counted 7 of 31 queued rows naming no requirement).
4. **Review, only on a green record for the tip.** The coordinator and the loop both refuse to dispatch reviewers without it. The reviewers then judge what tools can't: whether the code meets the requirement, and whether **the tests are adequate**. That covers four questions:
   - Does each test drive the interface the requirement names, and not handler source (the report's corrected test 3)?
   - Would it fail on a plausible wrong implementation?
   - Is each Done-when item covered?
   - Does a test name the IF it drives, where variant F requires it?
5. **The sitting** judges TC *text* at the checkpoint, as today.
6. **Later, a measured trial: mutation testing**, after item 8 measures its runtime against the 60 s smoke budget, and after adequacy review is working. It compares the adopter's existing tools before the kit builds a mutator. It covers the lane's changed lines only, as advisory evidence of test strength for the reviewers. Google surfaces mutants of changed code during code review (Petrović, Ivanković, Fraser, Just, *Practical Mutation Testing at Scale*, arXiv 2102.11378). They first found most surfaced mutants unproductive, and fixed that by filtering mutants and choosing operators by their history. So the trial starts narrow and advisory. A stdlib mutator (operator, comparison and constant swaps) over the diff is feasible; its cost is test runtime.
   - **Cheap when scoped** (owner, revision 17): restricted to the changed lines and the scoped test set above, the trial costs little. Google narrows further, running each mutant only against the tests that cover its line. Line coverage is available through `pytest-cov`, already in this repo's dev tooling.

**Measure.**
- Review rounds started on a red tip: should be 0 (counted in the phase-0 manifest).
- Findings an instrument would catch: should be 0 (item 6's measure).
- Review rounds per landed WI: should fall.

**Cost.**
- **Text and a small build:** the dispatch gate in the coordinator cycle and the loop, on the one tree-bound bar attestation (precondition 2; `Bar-Green` as it stands is refresh-only). It comes after item 6.
- **Text only:** the TC-first order in the coordinator cycle and `in-lane.md`, and the test-adequacy questions in the reviewer template.
- **Optional, later:** the mutation trial.

**Owner calls (open):**
- **Where the gate sits.** Should it gate the *start* of review (the owner's order, recommended), or only landing, the Gerrit form that lets review run in parallel?
  - **The owner prefers the start of review** (revision 17): the builder tries to fix its own red before tokens are spent on review.
  - **Evidence found.** No study compares gating review's start with gating merge directly. Nearby findings:
    - After CI arrives, pull requests get less discussion for the same amount of work (Cassee, Vasilescu, Serebrenik, *The Silent Helper*, SANER 2020, 685 projects): checks take over communication reviewers would otherwise do.
    - Passed builds are more likely to draw new review participation (Rahman and Roy, MSR 2017, 578K builds).
    - Self-repair from test feedback helps, but modestly once its cost is counted, and the quality of the feedback is the bottleneck (Olausson et al., ICLR 2024). That supports a small cap and escalation over an open loop.
    - **Against: flaky checks.** In OpenStack's Gerrit, 55% of reviews re-ran a build after a failure; the re-run changed the outcome only 42% of the time, raised review waiting time by 2,200% on average, and cost an estimated 187 compute-years (arXiv 2308.10078). A start-of-review gate is only as good as the bar is deterministic, so a flaky test is a defect to fix, never a re-run.
    - **Against: design flaws found late.** A builder can grind to green on the wrong design. Here the scope and plan critiques (item 9) judge the design before the build.
- **TC-first in lanes.** Should TC rows and failing tests come before the first build? Today they come after.
  - **The owner's view** (revision 17). Test cases are part of the breakdown. The spine is broken down; iteration decomposes components and interfaces; at the end of that, behaviours are written, with tests across the interfaces that must show them. Today's queue is amendments to a spine already broken down, so the question is the lane's order.
  - **The ladder already has this order for a first breakdown:** `DevStg-Tests` requires every SR and LLR to have a TC before `DevStg-Impl`, and `DevStg-Impl` turns each TC into a failing test before code (PROCESS.md §4).
  - **Integrator's proposal, for the churn concern.** Split text from code. A TC *row* (what is checked, at which interface) is written with its LLR, in the spine step before the build; in a lane, that moves Terra's authoring ahead of build round 1. Test *code* is the build's first deliverable, failing, since test code written before its interface settles is what would churn. **Confirmed by the owner (revision 17).**
- **Mutation testing.** Should the trial run, advisory, on changed lines only? **Confirmed by the owner (revision 17):** yes, on the changed lines and the scoped test set (step 6).
- **Who may install a dependency** (owner's question, revision 17). Can the adjudicator, at the build bound, install a missing dependency without the owner's input? Part of this is ruled already. RULING-3 (2026-07-28, `docs/dependencies.md`) says "not 'no dependencies' — 'no unargued dependencies'". A non-stdlib import in the kit's scripts exists only as a reviewed ledger row, stating what it replaces, why hand-rolling is worse, and the ruling that admitted it, and `tests/test_dependency_ledger.py` fails on any undeclared import. A `shipped` row needs an owner ruling; the `coordinator` rows so far were admitted by a reviewed WI (WI-480). Downstream, PROCESS.md §7's setup helpers are "consent-first … never a silent or compiled installer". What is not ruled is who may admit a row in the middle of a lane.
  - **The owner's position** (revision 17). Make it a kit option in `process.toml`, since autonomy needs in-lane installs when a lane discovers something new. The decider is neither the adjudicator (its scope is the spine and behaviour) nor the builder. It is a quick, independent decision on a carefully built brief, permitted only where the option allows it in lane; otherwise the lane hands back. Something with no method of testing it should not be developed.
  - **The arbiter exists, but it is a narrower role:** `dual-plan-arbiter.template.md` selects one of two anonymized plans. The word is taken (`intake.py`: "the dual-plan arbiter owns that word"), so a dependency decider is a new hat on the same pattern: a fresh session, a composed brief, a fixed answer vocabulary.
  - **What the brief must guard against** (integrator).
    - **The package may not be the one intended.** Of the packages that code-generating models import, 5.2% (commercial models) and 21.7% (open-source models) did not exist (Spracklen et al., USENIX Security 2025, 576,000 samples), and attackers register such names ("slopsquatting"). A 2026 preprint, not peer reviewed, measures 4.6–6.1% on newer models. So the decider verifies identity (the index entry, the project and repository, the pinned version and hash, the licence) and never takes the builder's name for it.
    - **Lanes share one interpreter.** The coordinator's recipes run every lane on the main checkout's `.venv`. An in-lane `pip install` changes the environment every other lane and trunk use, so one lane's install can turn another's bar green or red. An admitted install needs a lane-local environment, or is applied only from declared files.
    - **An install not in the declared files works on one machine.** Admission is therefore a diff: the ledger row, the dependency file and the lock, reviewed with the lane's change. The install follows from the files, not the reverse.
    - **Tier.** A `shipped` dependency, forced on every adopter, keeps its owner ruling and always hands back. The option covers non-shipped tiers only, such as test tooling, which is also the commonest in-lane case ("X is needed to test Y"). An adopter's product runtime dependency is an architecture decision, so it hands back too.
  - **Proposed shape** (integrator, revision 17, for the owner to confirm or overrule).
    - **The setting.** One key in `[policies]`, beside `push`, which it mirrors: the key names the act, and the value names who may do it. `dependency_admission = "human"` is the shipped default: a lane that needs a new dependency hands back, and the owner rules the ledger row. `"independent"` lets a fresh admission session admit one in the lane. An undeclared key reads `"human"`, and any other value is refused. The tier limit is fixed by the kit, not a second key: a `shipped` dependency always hands back. `"independent"` also requires `[attestation] decision_recording` to be `"record"` or stricter, and the loader refuses the pair otherwise, so no admission goes unrecorded.
    - **The hat.** It is a new prompt, `dependency-admission.template.md`, not the arbiter's or the adjudicator's. It runs as a fresh session, independent of the builder and, where available, of another model family. It answers ADMIT, REFUSE (build without it) or HAND-BACK (to the owner).
  - **Who verifies what, in order.**
    1. **The builder stops and asks; it never installs.** The request states the need, which tests need it, what it replaces, and why the standard library or an existing dependency won't do.
    2. **A script gathers the identity facts, and judges none of them.** From the package index: whether the entry exists, its first release date and release history, its project and source-repository links, its licence, the exact version and its hashes, and known advisories (`pip-audit`, already this repo's tooling). It reads the index with `urllib` only. A newly registered, single-release package with no repository is the slopsquatting profile, and the brief shows that plainly.
    3. **The admission session decides** on that brief, before anything is installed in the lane.
    4. **On ADMIT, the change is a diff.** It contains the ledger row, whose "Ruled" cell cites the decision entry (`docs/decisions/<run>.toml#D-NNN`), the dependency file, and the regenerated lock. The install comes from the lock, into the lane's own environment, never the shared `.venv`.
    5. **Checks in the lane, before review:** `test_dependency_ledger.py` (the row exists), the lock check (the lock matches the file), and `pip-audit` over the new lock. Today the last two run only in CI on their own schedule (`lock-check.yml` after a test run, `sca.yml` weekly), so a lane whose diff touches the dependency files runs them in its pre-review bar (item 13). An adopter supplies its own stack's equivalents.
    6. **The lane's reviewers** read the dependency diff and the ledger row's argument with the rest of the change.
    7. **The landing bar** runs in an environment built from the lock, so a dependency that works only on one machine fails there.
    8. **The owner reads it afterwards.** The admission is a delegated decision, always listed in the record's `high_risk`, so it heads "Decisions to review". An overrule files a WI to remove it, through the existing overrule rule.
  - **When the steps run** (revision 17, the owner's question). Steps 1–4 run where the need is found, before the code that needs it is built. Steps 5–7 are not extra stages: they join the lane's existing order (step 5 in the pre-review bar, after lint and tests; step 6 in the review; step 7 at landing). Step 8 never blocks. There is one path, with two places it can start:
    - **At planning (preferred).** The scope critique and plan (item 9) name the dependencies a WI needs, so steps 1–4 run before the claim, and a WI whose admission is still pending is not claimable: the scheduler doesn't start work that can't work. The lane is then cut with the admitted lock.
    - **During the build,** when the builder finds a need the plan missed. The build pauses at step 1 and resumes after step 4. On REFUSE it builds without the dependency; where that is impossible, it hands back.
  - **What "hands back" means** (revision 17, the owner's question; the kit's existing mechanism, nothing new).
    - **The lane never stalls.** A partial close is the only sanctioned stop, and a lane is never held (OI-70). The lane closes `partial` (`handback.py`): its work is committed with a keep/discard split, any code the bar refuses is quarantined as a bar-inert `.patch`, and an immutable report is written under `docs/handbacks/`. The branch merges and the run moves on to independent work.
    - **An independent adjudicator judges the close, not the dependency** (`adjudicate-disposition.template.md`). It checks whether the claimed outcome is right and the keep/discard split honest, and it drafts the mandatory successor row.
    - **The dependency question goes to the owner as an open item.** Where what is left is the owner's to rule, the successor carries an `[open_item]` card (one line, blast radius, options, recommendation). The mint makes it a pending OI and writes the OI into the successor's `needs`, so the successor sits queued but blocked until the owner rules.
    - **The card cites the admission facts; it does not redo them.** The owner's scope rule keeps installability out of the adjudicator's judgement. So the handback report carries the builder's request, the gathered identity facts and, under `"independent"`, the admission session's reasons, and the card cites them instead of re-judging. The same OI gate serves a need found at planning under `"human"`: the queued WI's `needs` names the OI before any claim.

**Found on the way (separate, not fixed):** `coordinator-cycle/SKILL.md:93` says "interface rows have no approval status", which contradicts PROCESS.md §8's `Drafted` · `Approved` for IF rows (the revision 12 correction).

## Sequence and how we'll know

| Phase | What | Who |
|---|---|---|
| 0 · rulings and baseline | Owner calls still open: item 11's, and the "Open after revision 12" and "Open after revision 13" calls in the rulings section (items 1–10 are ruled). A baseline manifest: the included review files and a class for each finding, so the counts above become reproducible. No code. | Owner; analysis agent for the manifest |
| 1 · cheap builds | Item 6 (LLR-292, the lints after each build, the RESYNC check). Item 8 (usage), so every later change is measured. Item 10 step 1 (one shared `stack.ini` loader) and step 2 (settle the shell-grep rule). Rubric and skill edits for items 1, 2, 3 and 9 (S3, S4, B3, binding advice). The reviewer-template clause for item 1. WI-805's plan gate, pulled forward (ruling 9; the handoff orders it right after B1). Item 12's text pieces (the rubric, the `architecture-decomposition` skill, the `spine-questions.md` pointer, the plan-decomposition question), after its dry run on W3. Item 13's review gate (reusing the `Bar-Green` record) right after item 6, and its text: TC-first in lanes and the reviewer's test-adequacy questions. | Coordinator lanes |
| 2 · trials, one change at a time | WI-902 reshaped (item 2), measured on its own. Item 4's settings on the next lanes. Item 7's Gemini slot once WI-815's route works. Item 13's mutation trial (advisory, changed lines only), if ruled. | Coordinator |
| 3 · structural (last) | Item 5: schema removal, derived index, batch act, commit-time text check. Item 2's history-reader audit. Item 10 steps 3–6 with item 4's `[review]` section, shipped as one RESYNC entry before the FileBackup re-sync. Item 11, once ruled, with item 5's migration. Item 12's builds (checks A and C, the `arch-audit` action and its critique skill), after item 11 is ruled. | Coordinator lanes |
| 4 · re-measure | Over the next 15 landed WIs, against the phase-0 manifest. | Coordinator / analysis agent |

**Session budget.** Item 4's cap bounds review sessions per WI: eight in the ordinary case with the ruled values (four Codex), more when a convergence-class fix round or a changed rebase adds a round (rulings section), plus one plan critique for an item 9 row and one dispute sitting at the limit. A Gemini slot (item 7) draws on a different quota. Item 8 records the sessions, so the budget is measured, not estimated.

**Record per lane:** which changes applied, sessions by role, gap-filtered and wall-clock time. Isolating each change's effect needs that record, since several start at once.

| Measure | Baseline | Direction |
|---|---|---|
| Net queue: rows filed + successors minted − rows closed, per week | to be counted (phase 0) | negative: the queue shrinks |
| Review rounds per landed WI | 3.3 mean (69 / 21, unreproduced basis) | down |
| WIs needing ≥ 6 rounds | 4 of 21 | down |
| Late findings from open input spaces | manifest owed | down |
| Review findings an instrument would catch | ~6 in the sample | 0 |
| Full reviews reopening a lane after a checkpoint | 6 in WI-834 | near 0 |
| Model calls with a recorded usage row | adjudications only | every call |

What this plan deliberately doesn't do: reduce review depth or the reviewer's stance. Late rounds also caught genuine new defects (WI-834's warm-tick race and interpreter mismatch, WI-902's truncated fence, WI-887's misspelled config value). The aim is to stop paying for the same class over and over.

## Independent review and dispositions

Two reviewers, the same brief, against commit 85a37767a: Claude Sonnet 5.5 (REVISE, 16 findings) and Codex 6.1 Sol at medium effort (REVISE, 18 findings). Each finding was treated as a claim and checked before acting. Every finding was adopted, four of them only in part. The full texts are in [`reviews/sonnet.md`](reviews/sonnet.md) and [`reviews/sol.md`](reviews/sol.md); the shared brief is [`reviews/brief.md`](reviews/brief.md).

| Finding | From | Checked | Disposition |
|---|---|---|---|
| "Can only show up at the gate" is false; WI-834's post-approval gate findings were mostly new open-space forms; "15 regressions" unsupported | Sonnet BLOCKER; Sol MAJOR | Confirmed: read 012/016/024/028/035/039 and narrow 030 | Adopted: Q4 answer and item 4 rewritten; item 4 made secondary to item 1 |
| Narrow briefs carry the Done-when and break-it instructions too | Sol MAJOR; Sonnet MINOR | Confirmed (`reviewer.template.md` is shared) | Adopted: table corrected |
| Record-at-close without a commit-vs-parent check is a marker convention | Sol BLOCKER | Agreed against the owner rule | Adopted: item 2 adds the commit check; the cell is the validated result |
| `--allow-lint-fail` is a bypass; whole-tree `trace --strict` is red on trunk; enforce at the hook vs parent | Sol BLOCKER; Sonnet MAJOR | Confirmed: `trace.py --strict` exits 1 (LLR-292) | Adopted: item 6 rebuilt as a commit-time check; no override. Superseded by ruling 6: the lints run after the build, not in the hook |
| The light plan stage is a second path and can build without a passing critique | Sol BLOCKER; Sonnet MINOR | Agreed against the no-fallback rule | Adopted: item 9 uses one path (WI-805's gate) and requires a passing verdict |
| Item 9 omits WI-834's two pre-build plan reviews, which already asked for the enumerated list | Sol MAJOR | Confirmed (`wi-834-plan/001…:29`) | Adopted: item 9's root cause is now "advice not binding"; it feeds item 1 |
| Usage totals double-count repeated message records; one agent is a Plan agent | Sol MAJOR; Sonnet MAJOR | Confirmed: deduplicated 151k coordinator, 564k builders, 51k Plan | Adopted: figures corrected (builders ~74%); dedup made an adapter obligation |
| Harvesting needs exactly-once attribution; WI-800 owns the ledger; nested placement unverified | Sol MAJOR | Confirmed (WI-800 exists) | Adopted: item 8 step 2 under WI-800 |
| A Gemini route is WI-815's (untested; needs WI-798 and WI-801), not WI-798's | Sol MAJOR | Confirmed | Adopted: item 7 depends on WI-815 plus a verified launch |
| Item 7's re-cut charter assumes items 5–6 already built | Sonnet MAJOR | Agreed | Adopted: trial uses current charters |
| Splitting: causal claims, savings arithmetic and the 2,000-line threshold don't follow; "active hours" misnamed | Sol MAJOR ×2; Sonnet MAJOR | Confirmed (medians reproduce; WI-818/822/790 ordinary) | Adopted: answer made descriptive, arithmetic withdrawn, no threshold, metric renamed |
| Cohort, "late" and the finding classes have no manifest; two counting bases | Sol MAJOR; Sonnet MINOR | Agreed; not reproduced here | Adopted in part: bases labelled, taxonomy marked unreproduced, manifest made a phase-0 task |
| One owning parser can't replace consumer-specific policies | Sol MAJOR | Agreed (WI-902's Trust section) | Adopted: item 1 step 3 |
| Deny-on-mention misses wrapper launches and over-denies; read the rationale first | Sol MAJOR; Sonnet MINOR | Confirmed (ruling 025) | Adopted: item 1 step 5 is investigation only |
| Item 1's relief mostly illusory: fail-open stays blocking; list authorship; construction should be primary | Sonnet MAJOR | Agreed in part: the list sits in the spec, set at scope critique, not by the builder | Adopted in part: construction-first, the reviewer classifies, numeric target dropped |
| A full review before the checkpoint can't certify the reconciled rows | Sol MAJOR | Agreed | Adopted: the gate over the checkpoint tip stays |
| Feeding the builder's coverage plan to a full reviewer anchors it | Sonnet MAJOR | Agreed; today's narrow briefs already carry it | Adopted in part: excluded from full rounds; today's practice raised as an owner question |
| Removing K3 drops the semantic correspondence check; limiting Sol excludes omissions | Sol MAJOR | Agreed | Adopted: item 5 keeps the meaning check |
| The layer-2 text check would force prose rewrites on non-text edits | Sonnet MAJOR | Agreed | Adopted: added tokens in text cells only |
| Items 4, 7 and 9 add sessions with no combined budget | Sonnet MAJOR | Agreed | Adopted in part: a yield order and per-WI session tracking, not a fixed number |
| Simultaneous changes confound trials; no queue-growth metric | Sol MAJOR | Agreed | Adopted: per-lane change record, WI-902 measured alone, net-queue metric added |
| Twelve WI-834 coverage plans, not ten | Both, MINOR | Confirmed | Corrected |
| 31 stakeholder needs, not 35; "Approve filing" breaks the decision vocabulary | Sol MINOR | Confirmed | Corrected; owner calls now read "confirm or overrule" |
| `code_symbol` reader list wrong (not `trace.py`/`gen_trajectory.py`; add `secret_classes` and five tests) | Sonnet MINOR | Accepted (revision 1's grep also matched "module") | Corrected |
| History-reader count varies with the pattern (21–22) | Sonnet MINOR | Accepted | Corrected |
| Item 2: say who may write the cell and what a missing cell does | Sonnet MINOR | Accepted | Adopted in item 2 step 1 |

Left unchecked by either reviewer, and still claims: the late-finding taxonomy (18 of 43, ~24 spine-text, ~6 mechanical), the narrow and full wall-clock minutes, the prose census, and where nested sub-agent transcripts land.

### Review of revisions 3–5: GPT-6 Astra, low effort

One reviewer, against commit 88472beb0 (the ruled plan, `pointer-rules.md` and the attended handoff): REVISE, 11 findings. Each was checked before acting, and all were adopted. The full text is in [`reviews/astra.md`](reviews/astra.md).

| Finding | Checked | Disposition |
|---|---|---|
| BLOCKER: parallel reviewers given the same rendered brief share a verdict path and pytest `--basetemp` | Confirmed: both derive from scratch root, lane, sha and scope (`review_brief.py` `_run_lines`, verdict path) | Handoff: render one brief per reviewer with its own scratch directory; file B with `--phase REVIEW-B` |
| BLOCKER: the pointer table let IF rows name boundary files, but the ruling says LLR/TC only | Confirmed | IF exception removed from `pointer-rules.md` and the diagram page; the owner's IF remark kept as an open question |
| MAJOR: three rounds plus a gate over the checkpoint tip can't both hold; session budget wrong; existing lanes' counts unstated | Agreed | Clarified: the gate is a counted round, at most six sessions, lanes in flight restart at zero (rulings section, revision 6). Superseded in revision 7: the gate is uncounted, eight sessions in the ordinary case |
| MAJOR: item 5's text check refused all paths in LLR text and skipped IF/CMP; item 10 called LLR/TC config mentions violations | Confirmed | Check made tier-specific; item 10 corrected |
| MAJOR: item 6's summary, heading, rationale, downstream and phase row still said "hook" | Confirmed | All moved to the build bar, closure and landing |
| MAJOR: S4 would mark B3 `single` before the plan gate exists, and the ruling forbids an interim path | Agreed | Handoff orders WI-805's plan gate right after B1; its own row is built without it, recorded |
| MAJOR: B1 omitted item 1's reviewer classification clause | Confirmed | Added to B1 and to the hand-run brief instructions |
| MAJOR: `agents-enabled` is an ordered pool with weights, not a toggle | Confirmed (`agent_route.py`) | Item 10 specifies the TOML shape; absent or empty grants no consent |
| MAJOR: "inventory minus code" would drop the launchers or admit other scripts | Agreed | An explicit `boundary` class on each inventory entry |
| MINOR: 13 `ConfigParser` constructions across 12 files, not 14 parsers | Confirmed (grep: 13 in 12 files) | Corrected |
| MINOR: "the one item that forces migration" is stale; superseded choices still read as actionable | Confirmed | Corrected; every owner-call box labelled ruled |

### Review of revision 6: Claude Fable 5.1, low effort

One reviewer, a different model in the author's family, against commit 17e87484a: REVISE, 23 findings (6 MAJOR, 17 MINOR). Each was checked before acting, and all were adopted. The citation count did not reproduce exactly, so the plan now gives a range. The full text is in [`reviews/fable.md`](reviews/fable.md).

| Finding | Checked | Disposition |
|---|---|---|
| MAJOR: if the first clean round is round 3, the post-checkpoint gate would be a fourth round, so the landing tip goes unreviewed | Agreed (revision 6's own clarification) | Revised: the cap counts rounds before the checkpoint; the gate always runs, in convergence stance |
| MAJOR: a fail-open defect found at round 3 could land as FIX-as-successor | Agreed | Convergence-class findings are never deferred: one more fix round or ESCALATE |
| MAJOR: with `[agent-loop]` retired, the no-consent state has no behaviour | Confirmed (the unmanaged path reads `[agent-loop]`) | The loop refuses with an empty pool; one model is a pool of one; the template ships empty |
| MAJOR: IF rows' code-naming cells weren't in layer 1 or the migration | Confirmed: 203/243 owners are `scripts/…`, 46 external, all Drafted; 204–229 ids cited, by pattern | IF cells join layer 1, generated from `Contract` citations; uncited rows get a citation or retire; no act needed |
| MAJOR: the Sonnet stand-in's spawn, inputs and isolation unspecified; reads as forbidden self-review | Agreed | Handoff spells out `model: sonnet`, only the rendered REVIEW-B brief, writes only its scratch; why it isn't self-review |
| MAJOR: the convergence round must confirm fixes, but `--findings` is narrow-only | Confirmed (`review_brief.py`: "a full-lane round is fresh") | Superseded by owner ruling (revision 8): no prior verdicts; regression tests confirm fixes, and the coordinator checks each accepted finding maps to one |
| MINOR (×17): stale "14 readers", file-row counts, triple-quote conditional, superseded item-6 disposition, `review_rounds` in the summary, the 0/0/2/2 flow, handoff tip and "each row is new", WI-902's approved lane rows, pre-claim sessions missing from the budget, the third shell read, TC rows naming modules, "not carriers", G's launch path, claim-versus-plan order, successor filing, the 18-row census | Confirmed or agreed | All corrected. TC-rows-name-modules became an open owner question, ruled in revision 8 (TC rows name no test files or modules) |

### Review of revision 11: GPT-6 Astra, low effort

One reviewer, against commit be2d10c3d (the plan, `pointer-rules.md` and the attended handoff): REVISE, 17 findings (14 MAJOR, 3 MINOR), plus views on every item 11 call. Each was checked against the repository before acting. All were confirmed, one census figure in part. None decides an owner call: where a finding needs a ruling, it became an open call. The full text is in [`reviews/astra-low-r11.md`](reviews/astra-low-r11.md); its brief is [`reviews/brief-r11.md`](reviews/brief-r11.md).

| Finding | Checked | Disposition |
|---|---|---|
| MAJOR: generating IF owner/consumer/requestor cells from untyped citations loses roles; external owners have no file | Confirmed: IF-175 (one owner, six requestors), IF-032 (`external:git` owner) | Noted in the clarification; open call "Generating IF roles" |
| MAJOR: removing the join answers "two homes" but not OI-67's "verified by nothing" | Confirmed (OI-67's decision text: the 48 extra links were "hand-written and verified by nothing") | Item 11 nuance rewritten; the IF → requirement list needs its own semantic check |
| MAJOR: OI-48 exempts kernel edges from the seam rule, and rejected an IF per helper edge | Confirmed (OI-48, ruled (d) 2026-08-21; (b)'s AGAINST) | Item 11 nuance: classify the 55 one by one, resolve the kernel case first |
| MAJOR: "module = one file in git" is not the earlier meaning | Confirmed: `MOD-###` tracked delegated repos, renamed `REPO-###` (`7f8cdc567`); PROCESS.md §10 uses module for a sub-system; Gilbert ASSET-001 is a fetched directory | Recorded under item 11's terms; open call on terminology. The owner's definition stands until ruled |
| MAJOR: no current blanket `Implements:` rule; coverage is a dial at 0 | Confirmed (PROCESS.md §3; enforcement audit, OI-42) | Item 5 and query 1 now call the per-module rule new; pointer-rules.md marked |
| MAJOR: per-module contract pressure exists (PROCESS §8 header-first seam rows; connectivity warns; header harvesting) | Confirmed (PROCESS.md §8; `trajectory_arch.interface_findings`) | Item 11 nuance added; no per-function mandate exists |
| MAJOR: IF rows already have approval status and DevStg-Arch authority | Confirmed (PROCESS.md §8; `kitlib/authority.py` `APPROVAL_RUNGS`) | Nuance corrected; the open call reworded |
| MAJOR: symbol-level citations don't recover function → LLR allocation | Agreed (the join attributes every carried LLR to every citing symbol) | Granularity nuance corrected: coarse reachability |
| MAJOR: shared IFs imply potential, not certain, overlap; runtime order isn't WI order | Agreed; the census itself says "often correct" (`check_trajectory.py`) | Query 2 reworded; the 2026-07-14 decision not to file `IF-Refs` cited |
| MAJOR: generated TC evidence leaves CI, inspection and `::` node evidence unspecified | Confirmed: TC-035 names the CI workflow, TC-209 an inspection record, 185 cells carry `::` | Noted in the clarification; open call "TC evidence that isn't a test file" |
| MAJOR: "every accepted finding has a pre-fix-failing test" isn't what the template enforces and doesn't fit document defects | Confirmed: the template verifies pre-fix failure only where the diff adds a test | The factual claim corrected in the plan and the handoff; open call "Confirming a non-executable fix". The revision 8 ruling stands |
| MAJOR: "at most eight" sessions isn't a bound | Agreed | "Eight in the ordinary case", extras named; "Sequence" corrected from six |
| MAJOR: the handoff's "For the owner" and boot reading omit item 11 | Confirmed | Handoff: item 11 and the revision 12 open calls added; boot reading names item 11; pointer/schema migration held until ruled |
| MAJOR: WI-441 re-tagged 149 LLR and 54 IF cells, not "all 302 LLRs" | Confirmed (`docs/log.md`, WI-455 note) | History row corrected |
| MINOR: census methods mixed (793 functions, 107 test files, 314 cells, 25 of 32 rows) | In part: 102 of 237 test files match `TC-NNN` here, against Astra's 101 and the plan's 107 | Test-file count given as a range; the others are labelled by pattern in their sources and left |
| MINOR (for clarity): history omits 13v's softening, the 09-23 decision date, OI-14's ruling date, the 2026-07-14 `IF-Refs` deferral | Confirmed (`docs/log.md` 2026-08-13v; the 09-20 plan's Q18) | History table and query 2 amended |
| MINOR (for clarity): stale summaries (revision history, item 6's call, item 10 step 6's counts, WI-805 in phase 3, superseded dispositions); proposed diagram's IF arrow reaches only LLR; ruled TC row omits IF | Confirmed | All corrected |

### Review of revision 12: Claude Fable 5.1, medium effort

One reviewer, a different model in the author's family, as a sub-agent given only its brief, against commit 32868aa01: REVISE, 25 findings (10 MAJOR, 15 MINOR), plus views on every item 11 call. Each was checked against the repository before acting, and all were confirmed. Where a finding needs a ruling, it became an open call; no owner call was decided. The full text is in [`reviews/fable-medium-r12.md`](reviews/fable-medium-r12.md); its brief is [`reviews/brief-r12.md`](reviews/brief-r12.md).

| Finding | Checked | Disposition |
|---|---|---|
| MAJOR: item 11 never names OI-112, the same question pending since 2026-10-08, in the opposite direction | Confirmed (OI-112 options (a)/(b); WI-871 held) | "Open after revision 13"; call 2 asks for one direction ruled with OI-112; the handoff names it |
| MAJOR: the owner-exact and stray-declaration checks refuse an over-claimed owner citation today, and generating `owner` makes them circular | Confirmed (`trajectory_arch.py` contract-body shape (3), strict) | Item 11 nuance; feeds the "Generating IF roles" call |
| MAJOR: the SR half of IF → requirement already has a home through `boundary_refs` and the crossing cells | Confirmed: 131 of 131 SRs carry `boundary_refs`; 47 IF crossing cells | Nuance added; call 2 offers "LLRs only, SR derived". The owner's proposal is left as written until ruled |
| MAJOR: calls 1 and 4 amend ruling 5's wording without saying so | Confirmed (ruling 5's text) | Calls 1 and 4 say so; "Open after revision 13" |
| MAJOR: the minimum profile has no IF registry, so code → IF only leaves its LLRs unreachable | Confirmed (PROCESS.md minimum profile; §8's single-module skip) | Nuance added; call 1 names it |
| MAJOR: item 4's prose still says "at most eight" | Confirmed | Corrected |
| MAJOR: the shipped citation grammar is module-level only | Confirmed (`gen_arch_map.module_contracts`, `module_contract_bodies`) | "Where things stand" and the query 1 nuance say so; the grammar change is named |
| MAJOR: "its TCs pass" isn't commit-checkable; SR-180's rationale wasn't read | Confirmed (SR-180 rationale) | Discharge rule split (a TC verifies it; results stay with the gate); the rationale is quoted |
| MAJOR: the physical reading of "module" has no instance in Gilbert; the kit already says "realization artifact" | Confirmed (OI-20; PROCESS.md §4) | Recorded under the module term; Fable's recommendation added to the terminology call. The owner's definition stands until ruled |
| MAJOR: "the tier does not recurse" is PROCESS.md §4, not §5 | Confirmed | Corrected (two places) |
| MINOR: OI-14's dates and quote sources | Confirmed (raised 08-09, ruled 08-13) | Corrected; quote sources noted under the table |
| MINOR: "Owner:" cells quote paraphrases | Confirmed | A source note under the history table |
| MINOR: WI-057 was the first *filled* IF registry | Confirmed (`af852db7a`, 2026-06-05) | Corrected |
| MINOR: OI-20's rule is paraphrased | Confirmed | Quoted, with its admitted targets |
| MINOR: 204–245 mixes distinct ids and citations | Agreed | Separated |
| MINOR: 229 / 97 / 84 / 76 unlabelled | Agreed | Given as ranges, with Fable's counts |
| MINOR: 24 of 31 queued rows, not 25 of 32 | Confirmed | Corrected |
| MINOR: phase 0 still says items 1–9 | Confirmed | Reworded |
| MINOR: the handoff says "all four reviews" | Confirmed | Corrected |
| MINOR: item 4's "the final round's reviewers confirm the fixes" contradicts the revision 8 ruling | Confirmed | Reworded: they verify the regression tests fail pre-fix |
| MINOR: the proposed diagram draws call 4 as settled | Confirmed | Arrow labelled as the owner's call |
| MINOR (for clarity): does the internal standing replace the `source`/`sink` tokens? | Confirmed (`trajectory_arch.interface_findings`) | Left open in the nuance |
| MINOR (for clarity): module and file are already distinct words in the kit | Confirmed (PROCESS_OPTIONS.md IF `owner`) | Recorded under the module term |
| MINOR (for clarity): OI-48 declined (b) in its recommendation, not its ruling | Confirmed | Reworded |
| MINOR: OI-42's and OI-67's `ruling_ref` cells point at deleted `docs/log.d/` files | Confirmed | Noted under the history table; a hygiene row for the coordinator, outside this plan |

### The item 11 fitness question: GPT-6 Astra and Claude Fable 5.1, medium effort

Two analysts, run in parallel on one brief, each in its own detached worktree at commit eae8e1cbe. Neither saw the other's answer. The question was the owner's follow-up handoff, [`item-11-llr-interface-check-handoff.md`](item-11-llr-interface-check-handoff.md), framed by the owner's lens: long-term design sustainability, behaviour kept divorced from implementation, and no link whose upkeep outweighs the orientation it gives. Both left their worktree unchanged. Each claim used was checked against the repository; one figure was corrected. The judged synthesis is [`item-11-llr-fitness-report.md`](item-11-llr-fitness-report.md); the full texts are [`reviews/astra-medium-item11.md`](reviews/astra-medium-item11.md) and [`reviews/fable-medium-item11.md`](reviews/fable-medium-item11.md), with per-LLR tables `reviews/item11-classes-*.csv` and brief [`reviews/brief-item11.md`](reviews/brief-item11.md).

| Finding | From | Checked | Disposition |
|---|---|---|---|
| The 55 of 302 reproduces; the handoff's 90 / 64 does not (101 under "at least one module owns none") | Both | Confirmed (55 in 31 module sets; 101) | Report and item 11's clarification bullet |
| The handoff's tests 2 and 3 use the end user as observer; an LLR's observer is its seam's consumer | Both (raised in the brief) | Agreed (the 2026-08-13 form rule) | Corrected tests in the report; applied at touch |
| 215–226 of 302 LLRs need rewording, nearly all for code symbols or narrated mechanism, which ruling 5 already requires | Both | Confirmed by the two tables (fitness agrees on 254 rows) | The rewording is item 5's cost, not item 11's |
| Owned IF is not carrying IF (IF-011 is an exit code); the dashboard has no IF row | Both | Confirmed (IF-011's `data`; no IF names the dashboard) | Owner call: mint a delivered-dashboard IF |
| A needs at least 508 authored links against D's 527: no simplification | Astra | Arithmetic checked | Variant E recommended, alternatives tabled |
| Discharge is not reachability; SR-180's replacement must keep structure, meaning and results apart | Astra | Agreed (SR-180's rationale) | Owner call |
| Per-row fitness verdicts depend on the reviewer | Integrator, from the tables | 7 of 15 jointly hand-read rows differ | No 302-row gate; fitness at touch |
| `spine-questions.md:218` and the spine-authoring skill still tell authors to name modules and symbols in LLRs | Astra | Confirmed | Owner call: pull the text change into phase 1 |
| 114 of 243 IF `data` cells name code (103 on `call` rows); item 5 counted only `owner` | Integrator | Counted (identifier-shaped tokens) | Owner call: classify the `call` rows before rewording |
| 217 of 243 IFs are exempt from TC coverage | Fable | Refuted in part: 147 ids (217 is the file's line count) | Report gives 147 |
| LLR-292's strict-lint failure is a negated non-claim ("no claim is made … is minimal") | Fable | Confirmed (`trace.py --strict`) | Report finding; bears on item 6's "fix LLR-292" |
| TC-029/030 evidence names `test_agent_loop.py`; the lock tests are in `test_agent_loop_support.py` | Astra | Confirmed | Report finding, for the coordinator |
| "Module docstring only" is too narrow: top-of-file comments are read too | Astra | Confirmed (`gen_arch_map.module_contracts`) | Corrected under "Where things stand" |
| Interactive dashboard evidence: a browser (Astra) or the parsed document (Fable)? | Both, divergent | Both agree a handler-text pin is the defect | Owner call |
| Recursion (a) / (b) is separate from this decision | Astra | Agreed | Left as its own call |

### Review of revision 15: GPT-6 Astra and Claude Fable 5.1, medium effort

Two reviewers, run in parallel on one brief, each in its own detached worktree at commit 7bfe0c06b; neither saw the other, and both left their worktree unchanged. The brief carried the owner's two-phase stance: challenge first, then, if the proposal holds, stress-test it for breakdowns and contradictions. Both returned REVISE: Astra 14 findings (11 MAJOR, 3 MINOR), Fable 22 (14 MAJOR, 8 MINOR). On direction, both keep F: Astra "prefer that corrected F over E", and Fable gives no phase-1 objection beyond the traced-cell finding. Each finding was checked against the repository before acting. Owner calls were added (F-calls 8 and 9; F-call 1 restated), not decided. The full texts are [`reviews/astra-medium-r15.md`](reviews/astra-medium-r15.md) and [`reviews/fable-medium-r15.md`](reviews/fable-medium-r15.md); their brief is [`reviews/brief-r15.md`](reviews/brief-r15.md).

| Finding | From | Checked | Disposition |
|---|---|---|---|
| MAJOR: a value domain is not always an enumeration; F point 8 is unsatisfiable as written | Both | Confirmed (IF-047 carries a verdict, a count and free text; Fable's count of 68 alphabet-shaped cells not re-run) | F point 8: closed, an enumeration where finite, else one declared schema; UNKNOWN only where it is a real state |
| MAJOR: the existing `Bar-Green` is refresh-only and can't serve the review gate | Both | Confirmed (`kitlib/verdict.py` `refresh_attestation`, `work_tip`) | Item 13: one tree-bound bar attestation, one grammar and verifier, naming its bar; refresh disposability unchanged |
| MAJOR: the authored-link accounting omits F's own new links | Both | Agreed | E-vs-F row: unknown until measured on a migrated slice |
| MAJOR: Gilbert's PART/ASSET rows don't carry a component; Gilbert has no CMP rows | Both | Confirmed (all 8 ASSET `Component` cells empty; PART-000 and CMP-000 only) | Corrected everywhere; Gilbert's partition counted as a migration cost |
| MAJOR: pointer-rules.md's F summary omits LLR → IF and uses the old TC wording | Both | Confirmed | pointer-rules.md rewritten; handoff's stale IF-list call replaced |
| MAJOR: OI-112 (a) is not "not adopted": F point 4 is its mechanism, and OI-112 calls (a) a prerequisite of (b) | Both | Confirmed (OI-112's recommendation text) | Status table and F point 4 corrected; the sitting judges payload compatibility, not class alone |
| MAJOR: the describable-state test turns a process sequence into a component cut; the W3 dry run presumes its answer; n − 1 isn't an IF count | Astra | Agreed (Parnas 1972; IF-175's shared verdict service; OI-67's per-kind rows) | F-call 6 separates obligations from components; the dry run judges cuts on evidence |
| MAJOR: containment can't derive behavioural parentage | Astra | Agreed | F-call 5: (b) under F is flat LLRs with direct SR roots; a refinement edge only if the Gilbert SR-012 trial needs one |
| MAJOR: LCA is not total (136 requestor-only IFs; file-channel owners) and is not an LLR's scope | Astra | Confirmed (136; IF-047 owner `docs/reviews/`) | LCA used for placement only; an LLR's scope is its IF's owner component; endpoints resolve first; kernel owners skipped (Fable's 12 not re-run) |
| MAJOR: blast radius IF → TC → LLR misses the same-interface case | Astra (Fable similar) | Agreed | Union of the inverse LLR → IF and TC observation links; potential impact, not proof |
| MAJOR: stubs don't give an LLR a home; SR-180's successor is underspecified | Astra | Agreed (WI-472's rationale as Astra quotes it, not re-read here) | F point 2 and point 6 restated; stub scope added to F-call 2 with both views |
| MAJOR: item 13's red-before rule breaks non-executable TCs | Astra | Confirmed (TC-209 un-automated Inspection; TC-035 Analysis) | Typed evidence contract at the same gate |
| MAJOR: item 12's entry point 1 contradicts its cadence; `DevStg-Arch` has no approval act | Both | Confirmed (signed boundaries: Reqs, Tests, Impl) | Gates named: the first LLR sitting at a critiqued depth; the whole-tree pass gates DevStg-Tests entry |
| MAJOR: LLR → IF on Approved rows makes interface refactors re-open requirements | Fable | Confirmed (OI-14: a traced cell opens no re-attest window) | The cell is a traced cell, re-pointed by the retire/successor act |
| MAJOR: under F an LLR naming no IF is unplaced | Fable | Confirmed (all 302 placed by `component`; 72–74 untagged) | New F-call 8 (a required "observed at" cell); it reverses the owner's earlier position, so not decided |
| MAJOR: two homes for the contract (row `data` and code body) | Fable | Confirmed (PROCESS.md §8: "only there") | New F-call 9; integrator recommends the code body |
| MAJOR: the non-code-realizations withdrawal answered a different question | Fable | Agreed | Partly restored: `#` header beside `Contracts:`, or the file's inventory `boundary` entry |
| MAJOR: an authored CMP-id owner re-reverses OI-67 (a) | Fable | Confirmed (interfaces.toml header) | F-call 1 restated with three positions; Fable's own pick (a module path) conflicts with ruling 5, so it is recorded, not adopted |
| MAJOR: nothing checks an LLR's named IF | Fable | Agreed | A sitting question in `spine-questions.md` §3 plus a commit check |
| MAJOR: "recorded red-before" names no record and implies a history read | Fable | Confirmed (`check_test_first` reads `rev-list`, warns only) | A red result bound to the parent's tree in the adding commit; `check_test_first` retires into it |
| MINOR: `trace.py --strict` does run, in the DevStg-Impl gate step | Fable | Confirmed (`check.py`) | Corrected |
| MINOR (×8): skill by path for a Codex planner; `arch-audit` in `process.toml`; OI-48 vs WI-064; "every LLR carried" wording; §4 not §3; IF-owner parentheticals; the first-stated tests marked; reviewer-family selection over route identities | Fable; Astra | Confirmed or agreed | All corrected |

Where the reviewers differed, the plan records both. Interactive dashboard evidence: Astra wants executed evidence for interaction claims, Fable the inspected document; it stays open (revision 17: answered, Astra's view, off the commit bar). Stubs: Astra wants them only where coordinated work needs them, while the owner and Fable put them at `DevStg-Arch`; this is F-call 2 (revision 17: the owner's answer is not every file). Neither moved F's direction.
