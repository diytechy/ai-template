# Review Churn Plan

*ai-template · 2026-10-11 · evidence window 2026-10-09 → 10-11 (21 WIs, 69 review rounds, 79 findings) · for the owner to confirm or overrule item by item*

**Status:** revision 15. Items 1–10 are ruled (see "Owner rulings, 2026-10-11"; the revision 6–7 clarifications not marked as rulings await the owner's confirm or overrule). Item 11 (what points where) is open; its terms (contract, module) and its two owner's queries (revision 11: contracts cited only where served; work items bound to the interfaces they serve) are the owner's. Revision 12 adds the open calls a GPT-6 Astra review of revision 11 raised (item 11's open calls, and "Open after revision 12" in the rulings section). Revision 13 adds those a Claude Fable 5.1 review of revision 12 raised, among them item 11's overlap with OI-112. Revision 14 answers the owner's follow-up on item 11 (are the LLRs fit to be carried by interfaces?): two independent analyses, GPT-6 Astra and Claude Fable 5.1 at medium effort, judged in [`item-11-llr-fitness-report.md`](item-11-llr-fitness-report.md). Both find that item 11 as proposed would not reduce rework, and both recommend a narrower variant E, with new owner calls. Revision 15 records the owner's refinement of E as variant F in item 11. It also loosens item 7's reviewer-family rule and withdraws item 5's per-module `Implements:` floor (both owner positions). It adds item 12 (architectural decomposition at three moments: a fresh-vision breakdown, an amendment that shifts the architecture, and an audit), at the owner's request.

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
- **Generating IF roles.** If the IF `owner`, `consumers` and `requestors` cells are generated from code, the citation must carry the role (owner, consumer, requestor), and an external owner (`external:git`) has no code to cite. Is the role a typed citation (`Contract IF-NNN` for the owner, a consumer form for the rest), with external owners kept as an authored id cell?
- **TC evidence that isn't a test file.** Test-file tags can generate test evidence, but not CI results, inspection records or reviews, nor the 185 `::` node references. Do those stay authored in the TC row (CI configs and inspection records are boundary files), with only test-file evidence generated?

**Open after revision 13 (Fable review of revision 12; for the owner to rule):**

- **Item 11 and OI-112 are one question.** OI-112 (pending since 2026-10-08, its WI-871 held) asks how far IF rows join the adjudicated spine: (a) route IF rows through the first-approval sitting; (b) each SR names the IF rows carrying its inputs and outputs. Its (b) points SR → IF; item 11 points IF → requirement. Ruling both separately would give the relation two homes. Does an item 11 ruling also answer OI-112, with one direction, or does item 11's calls 2 and 5 fold into OI-112's design pass?
- **Items 11 and 5 overlap.** Ruling 5 says code references up to its requirements and LLRs keep naming their component. Item 11's call 1 (retire `Implements:`) and call 4's "derived" option would amend that wording: a reversal, not an extension.

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

1. **Make it unrepresentable in the schema.** Delete `module` and `code_symbol` from the LLR schema (`kitlib/spine.py`), and make the loader refuse keys a requirement tier doesn't declare. Everything that reads those cells switches to one index generated from the `Implements:` tags. Readers today: `check_doc_refs.py`, `check_privacy.py`, `kitlib/spine.py`, `kitlib/secret_classes.py`, `lane.py`, `migrate_carrier.py`, `spine_carrier.py` and `trajectory_arch.py`, plus five tests (`test_assumption_gate`, `test_baseline_snapshot`, `test_derive_stage`, `test_module_size_ratchet`, `test_trajectory_arch`). IF rows' `owner`, `consumers` and `requestors` cells go the same way, generated from the code's `Contract IF-NNN` citations (revision 7). This removes the hand-synced cells, not the meaning check (below).
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

1. **A third family when one is available.** The builder and the adjudicator are Claude, and Sol and Luna are OpenAI, so the preferred second reviewer is Gemini. Otherwise the second reviewer is an independent reviewer of a different family *or a different model* from the first reviewer (today, Claude Sonnet beside Codex Sol, per ruling 7), recorded as a substitution (owner, revision 15: "must be a third one" was too strict). The route is not close: WI-815 owns the Gemini stdin route (its title says "an untested Gemini route") and needs WI-798 and WI-801. The trial waits on WI-815 plus one verified independent Gemini launch.
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
  - **Why it isn't needed.** Ruling 5 lets an LLR name a shipped boundary file. Gilbert's PART rows already carry `IF-Ref` and `Component`, and its ASSET rows carry `Component`. A realization that can't carry a header declares itself in its registry row.

  The original text: shipped boundary files (templates, registries) have no docstring. Their component and interfaces need a comment header, or derivation from the IF `data` cells. Physical realizations are wider still: OI-20 admits designed part sources, and a fetched asset or a bought part has no file to carry a header (revision 12).
- **The minimum profile** (revision 13). PROCESS.md's standalone one-module project has no interface registry, and §8 says single-module projects skip it. Under code → IF only and "every LLR carried by an interface", such a project has no path from code to any LLR. The rule for it is open: a declared system-boundary IF becomes mandatory there, or `Implements:` survives there.
- **The SR half of IF → requirement already has a home** (revision 13). All 131 SR rows carry `boundary_refs` to a `B-xx` crossing, and 47 IF rows name the crossing they realize (`interface_from_external` / `interface_to_external`). SR ↔ boundary IF is derivable through the crossing (no check joins them today), so an authored IF → SR list would be a second home. Fable recommends restricting the authored list to IF → LLR and deriving the SR side; an owner call.
- **An over-claimed owner citation is refused today** (revision 13). `trajectory_arch`'s owner-exact check (warn) and the strict contract-body gate's stray-declaration error check a `Contract IF-NNN:` body against the registry's authored `owner` cell. If `owner` is generated from the citations, that check becomes circular, and a consumer-side citation is today exactly the strict error. Keeping an authored owner id per IF keeps the independent check (the "Generating IF roles" call).
- **Per-module pressure exists today** (revision 12). No check mandates a contract per function, but PROCESS.md §8 has a work item that creates a module mint its seam rows header-first, `trajectory_arch.interface_findings` warns on modules with no declared seam, and `gen_arch_map.py` harvests module headers, not symbol docstrings. Query 1's "contract or internal standing" must migrate these explicitly. A `source`/`sink` Notes token already plays the internal role for two of the three connectivity warns; whether the new standing replaces those tokens or adds a fourth declaration is open (revision 13). Citations on symbols are also a grammar change: today a contract body is one per owning module, read from its docstring, so `gen_arch_map`, `trajectory_arch` and the strict body gate are rewritten for it.
- **Generated IF cells need roles** (revision 12). See "Open after revision 12" in the rulings section.
- **Will the interface carry the requirement, or only reach it?** (owner's follow-up, 2026-10-12; a clarification of the "Every LLR then needs an interface" bullet above, not a ruling.) The 55 LLRs in modules with no IF are not all one case. Worked sample, the 12 LLRs on `traj_render.py`: LLR-087 ends "seams terminate at the correct ports", and nothing in the LLR defines "correct" (TC-089's tests carry what meaning there is); LLR-100 names markup (`<nav class="crumbs">`), and TC-103 asserts handler text (`trail=trail.slice(0,i+1)`) though its stated `expected` is the user-level outcome; LLR-101 is behavioural (no `role=img` svg over a focusable descendant), and TC-104 deliberately avoids pinning the implementation. All three verify the generated dashboard HTML, which is the user's view, but by parsing markup, never by running a click or measuring focusability in a browser. The suggestion: point them at one boundary-artifact interface (the dashboard HTML as delivered, whose contract is the bounds a user relies on), rather than minting call-seam IFs for the renderer's internals, which OI-48 declined as describing library usage. Before any LLR is attached to an interface, test it three ways: (1) is its pass/fail wording defined in the LLR itself ("correct" fails), (2) does it state what the user observes, not the markup or handler that produces it, (3) do its TCs exercise the interface the LLR is attached to, at the level the user sees it? This is what keeps the item 11 migration from re-opening the spine: an LLR that fails (1) or (2) moves under the interface by rewording, and gains nothing from the move. Handoff: [`item-11-llr-interface-check-handoff.md`](item-11-llr-interface-check-handoff.md). **Answered in revision 14** ([`item-11-llr-fitness-report.md`](item-11-llr-fitness-report.md)):
  - **Counts.** The 55 reproduces; the handoff's 90 / 64 does not. 68–83 of 302 LLRs are fit as written, 215–226 need rewording and 4–8 need reframing or retiring. The rewording is almost all names of code symbols and narrated mechanism, which ruling 5 already requires removing.
  - **Tests (2) and (3) were mis-stated.** An LLR's observer is the consumer of its component-level seam, not the end user; held to the user's view, every LLR becomes an SR. The corrected tests are in the report.
  - **An owned IF is not a carrying IF.** IF-011, the renderer's only seam, is an exit code. The dashboard HTML has no IF row at all, and 21 LLRs are observable only there.
- **Blast radius becomes mechanical:** a changed file → its component → the interfaces on that component's boundary → the requirements those interfaces carry → the TCs verifying them. That answers the owner's "what is at risk when a component is updated".

**Scope.** A large program that belongs with item 5's migration, sequenced last. It touches the code tags (about 900 `Implements:` lines become contract tags), the IF schema (a requirement list in, generated owner/consumer cells per item 5), the CMP derivation, and the checks that read either.

**Downstream.** A schema and tag-grammar change for adopters, carried in item 5's RESYNC entry.

**Owner calls (open):**

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

**Recommended variant E (revision 14, not a ruling).** Two independent analyses of all 302 LLRs reach this on their own, and the integrator's checks confirm it ([`item-11-llr-fitness-report.md`](item-11-llr-fitness-report.md)).
- **Why not A.** A would not reduce rework. The defects that cause churn are symbols and mechanism in LLR text, and ruling 5 already removes them. A replaces about 527 code-side anchors with at least 508 authored links (302 or more IF → LLR plus about 206 code → IF), before file headers. It also adds an allocation that a seam split reopens.
- **What E keeps.** Code → LLR (`Implements:`), so ruling 5 stands as written and the minimum profile still has a path from code to its LLRs. LLR → CMP stays authored design intent. File component headers are deferred.
- **What E adds.** One delivered-dashboard interface and a few more delivered-artifact and CLI seams. IF → LLR only on interfaces that genuinely carry the behaviour, each reviewed, with the SR side derived. A reach dial with a closed internal allowance; no `call` seam is minted to satisfy a rule (OI-48).
- **Where the fitness tests go.** The three corrected tests go into the spine-authoring rubric and item 5's commit-time text check, applied when a row is touched. A 302-row gate is not used: the analysts disagree on 7 of the 15 rows both read by hand, so a fitness gate would itself generate review rounds.
- **The way back to A.** E can grow into A later without discarding anything.

**Variant F: the owner's refinement of E (revision 15; the owner's positions, for confirmation, not yet rulings).** It is kept as its own letter so the record shows what came from the analysts (E) and what from the owner (F), and so a later review can judge one against the other.

F agrees with E on four things: keep `Implements:`, no rule that every LLR is carried by an interface, mint the delivered-dashboard interface, and judge fitness when a row is touched. It goes further in seven places:

1. **One home for component membership: the realization.** A code file declares its component in its header. A part or a fetched asset declares it in its PART or ASSET row; Gilbert's already have `Component`, and PART also has `IF-Ref`, the same shape as a file citing its contract. **LLR → CMP retires.** Today the fact has two homes: 150 of 243 IF rows and all 302 LLRs carry a `component` cell.
2. **Files are created at design time.** When LLR and IF rows are written, their files are created as stubs: a component header and contract markers. This is PROCESS.md §8's existing "mint header-first" moved from the work item that creates a module to the design step.
   - **The pre-code gap closes.** An approved LLR's realization has a home before the code exists.
   - **Early work items stop clashing.** The first WIs no longer build a file structure around each other.
3. **No IF → LLR list.** Every defined behaviour is verified, either itself or through its parent. That is why an LLR exists: to be a testable point of reference.
   - **Where it is tested.** At the interface where its behaviour can be observed, often an outer one: many renderer LLRs are testable at the delivered dashboard. The test can be direct or a rubric.
   - **How the link is recorded.** Only where the test drives a separately measurable interface does the TC's `verifies` name that IF beside the LLR. That cell is the single home of "this LLR is checked at this interface"; nothing on the IF side repeats it.
   - **Blast radius** (IF → TC → LLR) is derived.
   - **An LLR that constrains a defined interface names it** (owner, revision 15, refining the bullet above). Such an LLR states what must hold across that interface: the mapping from its input domain to its output domain. It names that IF by id, in the requirement → IF direction of OI-112's option (b), which also settles "rule the direction once with OI-112".
     - **A TC repeats nothing.** It names an IF only when it tests at a *different* interface, such as the outer delivered dashboard, so "checked at" and "constrains" each keep one home.
     - **An LLR with no defined interface of its own** is verified at its parent's interface, as above.
   - **Where interfaces are strictly required** (owner, revision 15): wherever the architecture draws a boundary, at any depth. That means the system boundary, plus every component and sub-component boundary a decomposition creates; the 2026-08-13 form rule already applies each shall "to interfaces going to the respective component level". Inside a component, interfaces are optional (OI-48's line). A TC never mints an interface; it names one the architecture drew.
   - **The real gap risk** is a component drawn too coarse, not an LLR without an interface. The lane is the example. Planning, build, review, integration and handback all sit in CMP-008 W3 Autonomy, which holds 60 modules and 54 internal seams. So the stage handoffs are internal seams that nothing requires, and the stage sequence lives only in `runtime-flows.md` Flow 4. The fix is to decompose W3 into sub-components (F-call 5), which turns each handoff into a required boundary interface. Most lane handoffs pass through files (the review verdicts, IF-047; the work specs), which import analysis can't see, so those boundaries still depend on being authored and on the runtime flows.
4. **Interfaces are thin.** An IF row is a typed node joining ports: its channel class, owner and consumers. The contract body lives in code.
   - **Approval** is given at the level the interface is used, just before the SR or LLR it serves, and checks only that the interface class fits what it serves.
   - **Mechanizing** that approval comes last.
5. **Links back to the spine are encouraged, not mandated** (item 5's per-module floor is withdrawn). The trade is discoverability against rot, and the dial measures it.
6. **Id continuity.** A row keeps its id when amended only if its meaning stays close to the original purpose. In practice that means three things hold:
   - most existing links stay valid;
   - the rest can be updated with confidence;
   - a missed one, such as another repository citing the id, would not mislead.

   Otherwise the row retires with a successor record and new ids are minted. SR-180, LLR-180 and TC-175 retire outright, and new ids carry the new discharge rule. The kit already says ids are "never reused" (PROCESS.md §2) and splits amendments into CLARITY and MEANING (§3), but it never says when an amendment must become a successor. This rule fills that gap: a CLARITY amendment keeps its id; a MEANING amendment keeps it only under the test above.
7. **The SR side is derived through the assumptions too.** Where a boundary crossing can't be measured, an assumption turns it into an interface that can, and that permits the connection. The links already exist: 17 DA rows carry `effect_at` naming a crossing, 9 IFs carry `bridged_by` DA ids (IF-013 by DA-001 and DA-002), and 3 surrogates `emulates` an external party. So SR → `B-xx` reaches an IF either directly (`interface_to_external`) or through a bridging DA. Some of this assumption work is still in the WI queue.
8. **Interfaces carry problem-oriented state; boundaries keep dependencies sparse** (owner, revision 15).
   - **An interface's value domain is a closed enumeration.** Its values are mutually exclusive and collectively exhaustive, with an explicit catch-all such as UNKNOWN. Take a parcel's location: one enumeration (MAILBOX, SORTING FACILITY, TRUCK, UNKNOWN) carries exactly the 4 valid cases, where four booleans carry 16 values, 12 of them invalid. Invalid states are unrepresentable by construction, and no value is carried twice.
     - **Two kinds of "unknown"** (research, revision 15). An UNKNOWN that is a real problem state needs declared behaviour, ruling 1's "declared rule for everything else". An out-of-domain input is instead rejected at the boundary ("parse, don't validate"; category-partition's `[error]` choice). Otherwise a catch-all absorbs real missing cases, and coverage passes trivially.
     - **Flags are not always wrong.** A product of flags is right where the dimensions are truly independent (statechart AND-regions; `--strict` and `--json`). The smell is a flag passed across a boundary to select the receiver's behaviour, which the literature calls *control coupling*.
   - **This extends ruling 1.** A WI spec facing an open input space chooses "an enumerated allow-set plus a declared rule for everything else"; here the same rule is applied to interfaces. The contract (the owner's term) is then the interface's value domain.
   - **Component boundaries are placed to keep each output's inputs few** (arithmetic corrected by the research, revision 15). Three rules:
     - **What to count.** An output's cost is the product of the number of equivalence classes of each input it depends on, the component's own state included. This is Schroeder and Korel's *input-output relation*.
     - **What a split saves.** One test drives every output at once, so a component's exhaustive suite covers the *union* of the per-output cases. Take a 4-state and a 2-state input, where one output depends only on the 2-state input: the component still needs 8 cases, split or not. A split there buys proof and blast radius, not cases: "this output ignores that input" becomes structural rather than claimed.
     - **Where the case count drops.** It drops where an output is reached only through a **narrower intermediate value**. Inputs of 4, 4 and 3 states need 48 cases as one component. If the output depends on the first two only through a 2-state intermediate, splitting there needs 16 + 2·3 = 22: the product becomes a sum. This is why the intermediate domains must be stated during breakdown, and it holds only if the intermediate value is the *whole* channel.
   - **The domains must exist before the split.** This presumes the domains, intermediate ones included, are stated during problem breakdown.
   - **Established names**, confirmed with sources in [`item-11-value-domain-research.md`](item-11-value-domain-research.md); its vocabulary list is proposed for the spine-authoring rubric:
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
| IF → LLR | authored on carrying interfaces (about 100–150 cells, reviewed) | **none on the IF side.** An LLR that constrains a defined interface names it (requirement → IF, OI-112 (b)); a TC names an IF only when it tests at a different one |
| Interface value domain | not addressed | **a closed enumeration** (mutually exclusive, collectively exhaustive, with a catch-all), so invalid states are unrepresentable; boundaries placed to keep dependencies sparse (point 8) |
| IF → SR | derived through `boundary_refs` and the crossing cells | derived the same way, **plus the assumption bridge** |
| LLR → CMP | authored design intent | **retired** |
| File → CMP | deferred | **declared in the file header**, or in the PART/ASSET row for a physical realization; created at design time |
| IF → CMP / IF owner | an authored owner id that names its role | open (F-call 1) |
| IF approval | through the sitting (Fable) | just in time, at the level of use; class compatibility only; mechanized last |
| Where an IF is required | delivered artifacts and carrying seams; no `call` seams to satisfy a rule | **every architectural boundary at any depth** (system, component, sub-component); optional inside; components decompose recursively (F-call 5) by the descend test (F-call 6) |
| Id amendment | retire or re-mint | the continuity rule above |
| Authored links, against E | n/a | about 300 LLR → CMP cells and about 100–150 IF → LLR cells removed; about 117–150 file headers added |

**F's open calls:**
- **F-call 1: how an IF reaches its component.** Two options:
  - Authored: the IF owner is the producing component's id, as design intent, checked against the owning file's header. This is two facts, so the check is not circular.
  - Derived from the owning file: one home, but no independent check.

  Either way, a file that serves no requirement-bound interface still declares its component in its own header, so the owner's worry about such files doesn't decide this call. The owner is undecided.
- **F-call 2: the design-time stubs.** At which rung are files created, and what may a stub carry? The test-first check must not count a stub as implementation.
- **F-call 3: when a TC names an interface.** Confirm that a TC names an IF only where it drives a separately measurable interface.
- **F-call 4: where the id-continuity rule lives.** Write it into PROCESS.md beside "never reused", tied to the CLARITY/MEANING split.
- **F-call 5: components decompose recursively.** A sub-component is linked to its parent component (`part_of`, with a scope check, as Astra suggested in revision 12), and it follows the same rule: interfaces at its boundary, freedom inside.
  - **First test case:** W3 Autonomy, split into the lane's stages (planning, build, review, landing).
  - **The depth-0 frame stays locked** at four components; sub-components sit under it.
  - **It ties to decomposition (b)** (SRs only at the system boundary, decomposed recursively by the architecture). The recursion would be carried by the component tree and its interfaces, and LLRs hang off it through their TCs.
- **F-call 6: a test for when to descend** (owner's criterion, revision 15). The aim is to keep interface permutations few, while keeping the spine light enough to maintain. The owner's position: decompose what a stakeholder can describe as a state; stop at the values they could only choose on seeing the implementation. Proposed wording for the `spine-questions.md` list, beside its existing "Descend only where a mechanized check earns its keep" and "Record the stopping boundary". Ask of each candidate child:
  1. **A describable state: descend.** Can the stakeholder name the state, what the system does in it, and what moves it on, in their own words and without inventing a number? This is an SCR *mode class*. Plan → build → review → land passes. Where one state hands its output to the next, the handoff is an interface. Where the states own files, they are sub-components.
  2. **An invented number: stop.** Is the only new content a value the stakeholder could not state *or source* today and would pick only on seeing the implementation (a 6 px gap, an 8 pt font)? The parent keeps the quality ("legible"), verified by a rubric or `Attest`, and the value lives in code or config. A binary floor ("no two wires overlap", LLR-292) is a describable state and stays. So does a number the stakeholder can source, such as one set by a standard (INCOSE's "solution free unless there is rationale").
  3. **A paraphrase: stop** (existing rule).
  4. **No pass/fail of its own: stop** (existing rule).

  Interfaces then come only from handoffs between describable states, so a linear flow of n stages has n − 1 of them, and they match the handoffs the runtime flow draws. The judgement stays subjective at the edges. The existing "record the stopping boundary" rule makes each call reviewable.
- **F-call 7: what to mechanize, and the vocabulary.** The research is done ([`item-11-value-domain-research.md`](item-11-value-domain-research.md)). It proposes three checks, all stdlib and advisory first:
  - **(A) Well-formed value domains** over the IF `data` alphabets and the `set{...}` dimensions: duplicate labels, a catch-all with no declared behaviour, and clusters of booleans. It needs no schema change. The SR `permutations` cell already uses the `gen_cases` grammar, and none of the kit's own 131 SRs fills it.
  - **(B) SCR disjointness and coverage** over a condition table. This needs a new optional cell, which is a downstream migration.
  - **(C) A dependency matrix per component** from the import graph plus IF file edges, suggesting where a component is under-decomposed (W3 first). It is noisy, so it would be a dashboard suggestion only.

  Also for ruling: adopt the report's ten terms in the spine-authoring rubric, with its glosses for *module* and *seam*.

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

LLRs then attach to those interfaces, as F requires. The skill guides the author. An independent critique against the rubric runs before the step is approved.

**Entry point 2: an amendment that shifts the architecture. The planner decides** (owner, revision 15). When a WI is planned (WI-805's plan gate, item 9), the planner follows the skill and answers the architectural-delta question: does the WI add a state, add a value to a domain, make an output depend on a new input, or cross a new boundary? The answer depends on the WI's scope:
- **Within its scope:** the plan carries the architecture change explicitly (interface and domain edits, perhaps a sub-component split). Item 3's split rule separates the refactor from the feature ("make the change easy, then make the easy change").
- **Beyond its scope:** the planner hands the WI back with a proposed refactor WI. This is the existing handback, not a new path.

The plan critique judges the answer; `docs/rubrics/plan-decomposition.md` gains the question. **Nothing triggers it automatically.** The planner may consult checks A and C as information.

**Entry point 3: an audit, `run.cmd arch-audit`, on demand only** (owner, revision 15). A new action in `docs/stack.ini [run]`, shaped like the `render-dashboard-critique` skill:
1. **The mechanical half** needs no model. It runs `trajectory_arch`, checks A and C, `check_complexity`, the duplicates census and `gen_arch_map`, and writes a findings bundle.
2. **The judgement half** is an independent critique session. It reads the bundle against the rubric and ranks components by what a refactor would gain.
3. **The output** is candidate WIs or open items filed through intake. The critic never edits the spine (`docs/rubrics/README.md`).

With an empty route pool, the judgement half refuses rather than falling back (revision 8 ruling).

### First step: a dry run on W3, before building anything

Give an independent model only the drafted rubric and W3 Autonomy's current shape: its modules, internal seams, the lane's runtime flow (Flow 4) and its interfaces. Ask it for a decomposition.
- **If it proposes a lane split** close to the stages a stakeholder would name (planning, build, review, landing), with sensible handoff domains, the rubric works.
- **If not, the rubric is fixed** while it is still text.

The dry run also gives F-call 5 (recursive components) its first worked case.

**Cost.**
- **Text only (phase 1):** the rubric, the skill, the spine-questions pointer and the plan-decomposition question, about one lane.
- **Builds (phase 3, after item 11's ruling):** checks A and C, the audit action and its critique skill.

**Downstream.** The rubric, skill, pointer and plan-critique question ship to adopters as kit-owned text; the audit action ships in the run-menu template. It is one RESYNC entry; adopters migrate nothing, since everything is additive.

**Decided by the owner (revision 15):** a skill, not a hat; the planner decides on an architectural delta, with no automatic trigger (a WI beyond its scope is handed back); the audit runs on demand.

**When the critique runs during the initial breakdown** (owner's position, revision 15). Not at every component scope. Three moments:
- **The top level.** Read as the first architecture step below the SRs: depth 0, where SRs are allocated to components and the first LLRs attach. The SRs themselves are already judged by their own sitting.
- **Once over the whole tree,** when the lower levels appear complete and before the build begins.
- **Every second level of component depth** away from the SRs, in a deep tree. A wrong split is then caught at most two levels after it is made, instead of only at the pre-build pass.

*Open:* confirm the reading of "top level", and whether the every-two-levels rule applies always or only where the tree is deeper than two levels. The "floors" here are component depths, not spine tiers: the tiers stay SN, SR, LLR and TC, and the recursion is in the component tree (F-call 5).

**How a planner picks up the skill** (owner's concern, revision 15). The architectural-delta question arises inside a WI, so the planner must meet the skill without being told each time. Today nothing routes skills to a planner:
- **The frontmatter isn't read.** A skill's `phases` frontmatter (`dev`, `gate`, `release`) only feeds `skills/INDEX.csv`; no brief reads it.
- **The planner prompt doesn't mention skills.** `plan_briefs.py` and `prompts/dual-plan-planner.template.md` name none.
- **Model-dependent discovery.** A Claude session may find a skill from its `description` ("Use when …"); a Codex planner won't.

So the reliable route is the prompt. The planner template, and WI-805's single-plan prompt when it exists, carry one line: answer the architectural-delta question by following the `architecture-decomposition` skill. The skill's `description` is written to trigger on planning, as a second route.

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

## Sequence and how we'll know

| Phase | What | Who |
|---|---|---|
| 0 · rulings and baseline | Owner calls still open: item 11's, and the "Open after revision 12" and "Open after revision 13" calls in the rulings section (items 1–10 are ruled). A baseline manifest: the included review files and a class for each finding, so the counts above become reproducible. No code. | Owner; analysis agent for the manifest |
| 1 · cheap builds | Item 6 (LLR-292, the lints after each build, the RESYNC check). Item 8 (usage), so every later change is measured. Item 10 step 1 (one shared `stack.ini` loader) and step 2 (settle the shell-grep rule). Rubric and skill edits for items 1, 2, 3 and 9 (S3, S4, B3, binding advice). The reviewer-template clause for item 1. WI-805's plan gate, pulled forward (ruling 9; the handoff orders it right after B1). Item 12's text pieces (the rubric, the `architecture-decomposition` skill, the `spine-questions.md` pointer, the plan-decomposition question), after its dry run on W3. | Coordinator lanes |
| 2 · trials, one change at a time | WI-902 reshaped (item 2), measured on its own. Item 4's settings on the next lanes. Item 7's Gemini slot once WI-815's route works. | Coordinator |
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
