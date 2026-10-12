# Review Churn Plan

*ai-template · 2026-10-11 · evidence window 2026-10-09 → 10-11 (21 WIs, 69 review rounds, 79 findings) · for the owner to confirm or overrule item by item*

**Status:** revision 7, ruled. The owner ruled every open call on 2026-10-11 (see "Owner rulings, 2026-10-11"); the revision 6–7 clarifications after the Astra and Fable reviews are for the owner to confirm or overrule.

The churn is real but concentrated: four WIs (WI-834, WI-902, WI-887, WI-881) took 41 of the 69 review rounds in the window. Adjudication upheld most contested findings, so the reviewer is not the problem. What keeps rounds coming is the shape of the work. Specs promise behaviour over open-ended inputs, and every fresh review samples a new corner. Advice about that from earlier reviews never becomes binding. Facts get re-derived from git history. And requirement rows restate code and drift with every fix.

Revision 2, after two independent reviews (Claude Sonnet 5.5 and Codex 6.1 Sol, same brief, against commit 85a37767a). Both returned REVISE; every finding was checked against the repo, and the dispositions are in the last section. The reviews themselves are in [`reviews/`](reviews/) beside this file. Revision 3 (owner direction, same day): item 4 becomes the review settings, item 6 shrinks to the hook change, and item 10 is added. Revision 4 records the owner's ruling on item 10 after a read-only investigation of both configuration files. Revision 5 records the owner's rulings on every open call (next section). Revision 6 answers an independent GPT-6 Astra review of revisions 3–5, and revision 7 a Claude Fable 5.1 review of revision 6 (dispositions at the end).

| # | Change | Kind | Cost | Aims at |
|---|---|---|---|---|
| 1 | Closed coverage, made binding: deny-by-default construction for unbounded syntax, an enumerated allow-set in the spec, and the reviewer classifying fail-open vs fail-closed | ruling + rubric | hours | the largest class: open input spaces re-sampled every round (WI-834's gate findings 016, 024, 028) |
| 6 | Run the strict lints after every build (commit bar, closure check, landing check; not the commit hook): fix LLR-292, add a RESYNC-presence check | small build | ~1 lane | findings an instrument would catch (~6 in the sample) |
| 8 | Record usage for every model call, under WI-800's invocation ledger: Sol and Terra through the session service, sub-agents from transcripts, deduplicated | small build | ~1 lane | ~74% of a leg's Claude output (builders) is unrecorded; makes every trial measurable |
| 2 | Record a decision at its event, validated by a commit-vs-parent check; never re-derive it from history. Reshape WI-902 first | ruling, then WI-902 reshape | 1 spec amendment | WI-902's history-replay findings |
| 9 | A planning need decided at mint; plan and scope advice becomes spec text before the claim; one planning path shared with WI-805 | ruling + ordering | hours, then one critique per planned row | advice that never binds (WI-834's pre-build reviews already asked for an enumerated list) |
| 4 | Review settings: reviewers and rounds per WI (ruled 0 / 0 / 2 / 3), an adjudicated exit at the cap, MINORs never cost a round, a convergence final round, severity tied to reachability | ruling + template change | 1 lane + migration | unbounded rounds (WI-834: 20); ad hoc breakers (WI-902); stale checkpoints |
| 7 | A second reviewer from a third family (Gemini) at the full reviews; the coordinator cycle reads item 4's `full_reviewers` | ruling + trial | waits on WI-815's route | earlier discovery, on a separate quota |
| 3 | Split at birth on independent deliverables, for containment; no size threshold (the data doesn't support one) | ruling | none | one stuck subsystem holding the rest |
| 10 | One configuration file in TOML (owner ruling 2026-10-11): `stack.ini`, routes and consent move into `process.toml`; adopter-owned values, kit-owned schema; re-sync adds, never replaces | ruled · 4–6 WIs | before the FileBackup re-sync | 13 separate parsers; routing in three homes; a re-sync that overwrites adopter values |
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

**Revision 6–7 clarifications, after the Astra and Fable reviews (for the owner to confirm or overrule):**

- **Where the checkpoint sits (item 4; revised in revision 7).** `full_rounds_max = 3` caps the full rounds *before* the checkpoint. Rounds run until one has no BLOCKER or MAJOR code finding; the checkpoint (Terra reconcile, closure check, sitting) follows it. The gate over the checkpoint tip, and a round over a rebase that changed code or rows, always run, in convergence stance, and are not counted, so the tip that lands is always reviewed. If the cap is reached with findings open, `on_limit` fires.
- **A convergence-class defect is never deferred.** At the cap or at the gate, a fail-open, data-loss or Done-when-gap finding is never ruled FIX-as-successor: the sitting orders one more fix round or ESCALATEs to the owner. Other findings may become successors.
- **The convergence round sees the earlier verdicts.** To confirm fixes it receives the earlier rounds' reviewer verdicts (never the builder's coverage plan). `review_brief.py` refuses findings on a full-scope round by design ("a full-lane round is fresh"), so B1 lets the convergence round take them; until then the coordinator appends the prior verdict files to both renders by hand. This relaxes the freshness rule for the last round only.
- **Successor rows** a sitting rules are filed on trunk at the landing, from the sitting's binding: a work branch never mints a WI id.
- **No consent means no managed loop (item 10).** Once `[agent-loop]` retires into the routes, no single-model fallback survives. The loop refuses to launch with an empty pool, and a one-model setup is a pool of one route. The shipped template ships an empty pool, so a fresh scaffold names its routes before the loop runs.
- **IF rows join layer 1 (item 5).** Their `owner`, `consumers` and `requestors` cells (203 of 243 owners are `scripts/…`) leave the schema and are generated from the code's `Contract IF-NNN` citations. Depending on the pattern counted, about 204–229 distinct interface ids are cited from code, so roughly 14–39 internal rows need a citation added, or the row retired, first. The 46 external crossings name their external party by id, not code. All IF rows are Drafted, so no batch act is needed.
- **The third shell read.** Besides the missing-scripts-directory refusal and the mixed-config refusal, the hooks read the legacy `docs/privacy-check` file in shell. It retires with WI-817's legacy window, which item 10 folds in. The shared `tomllib` read lives once, in `kit-python.sh` beside the interpreter probe, not in three hook copies.
- **Open owner question: TC rows naming modules under test.** The ruling says tests may still point to modules. A TC row is a requirement-tier row, though, so a module rename would reopen it. Either the owner confirms TC rows may name modules under test, or that column is generated from the test files' tags.
- **Lanes already in flight** (WI-798, WI-902) start the count at zero at their next review under the new shape. The coordinator records that as a decision.
- **Session budget (item 4).** In the lane: up to three counted rounds plus the post-checkpoint gate, so at most eight review sessions (four Codex, four Sonnet or Gemini), plus a dispute sitting at the cap. Before the claim: the scope critique and its disposition re-check (two Codex sessions), and one plan critique for a row S4 marks `single`.
- **IF rows name no files (item 5).** The ruling allows shipped boundary files at LLR and TC only, so interface rows use component and interface ids and artifact-class wording. The owner's earlier remark that interface definitions can label files tied back to assumption rows is kept as an open question, not an allowance.
- **The boundary-file set is an explicit classification.** The shipped-file inventory records source, destination and reference, not a boundary class. Subtracting "code" by directory or suffix would wrongly drop the launchers (which ship from `scripts/run.template.*`), and excluding only Python would admit other scripts. So the one inventory gains an explicit `boundary` class on each entry, matched on the destination path. That is a closed allowance, with no second list.
- **The planning gate comes before rows that need it (item 9).** Once S4 exists, a row it marks `single` waits for WI-805's pulled-forward plan gate. The gate's own row is built without the gate (it cannot plan itself), and that is recorded. The handoff's batch is ordered so.
- **`agents-enabled` as a setting (item 10).** The file is an ordered pool of route ids with per-phase draw weights and strict validation (`agent_route.py`), not a toggle. Its setting keeps exactly that: an ordered TOML array of tables, each an `id` with optional per-phase weights, validated as today. An absent or empty pool grants no managed-routing consent.

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
| `reviewer_families` | `["openai", "google"]` (proposed) | One family per reviewer slot, each different from the builder's (item 7 has the Gemini route). |
| `final_round_stance` | `"convergence"` (proposed) | How the last allowed round behaves (below). |

With the ruled values (0 / 0 / 2 / 3) a WI runs: build; up to three full rounds of two parallel reviewers, fixing between them; the checkpoint after the first round with no BLOCKER or MAJOR code finding; the post-checkpoint gate in convergence stance; then land, or adjudicate at the cap. That is at most eight review sessions per WI (four Codex). Most WIs already land within 1–2 rounds, so the cap only binds on the churners. `on_limit` is what makes the cap work: without it, a cap leaves open findings with nowhere to go, which is what happened ad hoc with WI-902. Where the checkpoint and its gate sit is set out in the rulings section's clarifications (revision 7).

### The reviewer's stance

Keep "try to break it", but calibrate it. That stance found the warm-tick race and the truncated fence. Two changes stop it from hunting rare, nuanced edge cases into an endless loop:

1. **Severity tied to reachability** (reviewer template, shipped). A BLOCKER or MAJOR needs a stated scenario reachable in normal use, or a fail-open, data-loss or security path. A rare or contrived edge case is at most MINOR, and under `block_on` it never costs a round. This extends the threat-model rule, which already dismisses compromised-host findings, to findings that are possible but unlikely.
2. **A convergence stance for the last allowed round.** The final round's reviewers confirm the fixes, check Done-when coverage and look for regressions. A *new* finding blocks only if it is fail-open, data loss or a Done-when gap; anything else is filed as a successor row. This stops the cap's last round from becoming a fresh sample of the input space, as the 2026-10-04 research note advised: "a reviewer told to find gaps will always find some, so ground the review in the acceptance criteria". A per-slot stance (A adversarial, B acceptance-only) is possible later; the per-round form is the one aimed at convergence.

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
| TC rows and tests | Yes: may name test modules and modules under test | verifies up; names code as evidence |
| Generated views (dashboard architecture, trace matrix) | Yes, derived | computed from the up-pointers, never authored |

Under this reading, "current carrier" evidence moves from SR acceptance to the TC rows that verify it, and the LLR tier states contracts, not code carriers. R2's third guarantee, "why does this file exist", is kept by an inverse check: every shipped module carries at least one `Implements:` tag naming a live LLR.

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

- Confirm or overrule the LLR-292 fix and the hook change as the first rows.

## 7. A second reviewer from a third model family

**Evidence.** The kit already ships the dial: `[policies] review_rounds = 0|1|2` (this repo: `1`, `docs/process.toml:202`). At `2` two independent reviewers split charters (A: method, risk, corner cases; B: process, trace, prose), and a cross-provider pair is the recommended setup, routed per phase through `AGENT_CMD_MAP`. Only the managed loop reads it. The coordinator cycle hard-codes one Sol review per round through `sol_review.sh`, and specs carry "Review bar: A".

**Why it helps, and what it won't fix.** Two reviewers in parallel pull discovery forward at no extra wall-clock, and a different family brings different blind spots. On an open input space they just sample twice as fast, so item 1 comes first.

### Proposal

1. **The family must be a third one.** The builder and the adjudicator are Claude, and Sol and Luna are OpenAI. That leaves Gemini. The route is not close: WI-815 owns the Gemini stdin route (its title says "an untested Gemini route") and needs WI-798 and WI-801. The trial waits on WI-815 plus one verified independent Gemini launch.
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
6. **Amend the spec rows and docs together with item 5**: 23 LLR, 8 TC, 3 SR and 7 IF rows, about 10 adopter-facing docs (`RESYNC_PACK`, `ADOPTING`, `PROCESS_OPTIONS`, the kit README, …), and the generated references. Ship it all as one RESYNC entry, before FileBackup's re-sync.

**Trade-off.** A 4–6 WI program touching a security-relevant reader: the privacy keys. Step 2 settles that first, and the 2026-08-08 decoy-comment failure goes into each review brief as a named failure class.

**Downstream.** One migration for adopters instead of two. The RESYNC entry carries both the 2026-08-08 one-word-file fold and this consolidation, for an LLM to apply.

**Resolved (revision 5):**

- The file keeps the name `docs/process.toml` (ruled).
- Step 2: all three hooks refuse without Python 3.11+, so the shell grep and the shape rule go; the remaining shell reads, including the legacy `docs/privacy-check` read, become one `tomllib` read in `kit-python.sh` after the interpreter check (not objected).

## Sequence and how we'll know

| Phase | What | Who |
|---|---|---|
| 0 · rulings and baseline | Owner calls on items 1–9 (item 5's core rule is already ruled). A baseline manifest: the included review files and a class for each finding, so the counts above become reproducible. No code. | Owner; analysis agent for the manifest |
| 1 · cheap builds | Item 6 (LLR-292, the lints after each build, the RESYNC check). Item 8 (usage), so every later change is measured. Item 10 step 1 (one shared `stack.ini` loader) and step 2 (settle the shell-grep rule). Rubric and skill edits for items 1, 2, 3 and 9 (S3, S4, B3, binding advice). The reviewer-template clause for item 1. | Coordinator lanes |
| 2 · trials, one change at a time | WI-902 reshaped (item 2), measured on its own. Item 4's settings on the next lanes. Item 7's Gemini slot once WI-815's route works. | Coordinator |
| 3 · structural (last) | Item 5: schema removal, derived index, batch act, commit-time text check. Item 2's history-reader audit. Item 9's planning path, if WI-805 is pulled forward. Item 10 steps 3–6 with item 4's `[review]` section, shipped as one RESYNC entry before the FileBackup re-sync. | Coordinator lanes |
| 4 · re-measure | Over the next 15 landed WIs, against the phase-0 manifest. | Coordinator / analysis agent |

**Session budget.** Item 4's cap bounds review sessions per WI: at most six with the ruled values (three Codex), plus one plan critique for an item 9 row and one dispute sitting at the limit. A Gemini slot (item 7) draws on a different quota. Item 8 records the sessions, so the budget is measured, not estimated.

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
| MAJOR: three rounds plus a gate over the checkpoint tip can't both hold; session budget wrong; existing lanes' counts unstated | Agreed | Clarified: the gate is a counted round, at most six sessions, lanes in flight restart at zero (rulings section, revision 6) |
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
| MAJOR: the convergence round must confirm fixes, but `--findings` is narrow-only | Confirmed (`review_brief.py`: "a full-lane round is fresh") | B1 lets the convergence round take prior reviewer verdicts; appended by hand until then |
| MINOR (×17): stale "14 readers", file-row counts, triple-quote conditional, superseded item-6 disposition, `review_rounds` in the summary, the 0/0/2/2 flow, handoff tip and "each row is new", WI-902's approved lane rows, pre-claim sessions missing from the budget, the third shell read, TC rows naming modules, "not carriers", G's launch path, claim-versus-plan order, successor filing, the 18-row census | Confirmed or agreed | All corrected. TC-rows-name-modules is now an open owner question |
