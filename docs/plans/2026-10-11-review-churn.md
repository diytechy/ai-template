# Review Churn Plan

*ai-template · 2026-10-11 · evidence window 2026-10-09 → 10-11 (21 WIs, 69 review rounds, 79 findings) · for the owner to confirm or overrule item by item*

**Status:** open for owner ruling, item by item. Item 5's core rule (requirements never reference code) was ruled by the owner on 2026-10-11 and is recorded in item 5; its open questions remain.

The churn is real but concentrated: four WIs (WI-834, WI-902, WI-887, WI-881) took 41 of the 69 rounds. Adjudication upheld most contested findings, so the reviewer is not the problem. What keeps rounds coming is the shape of the work: specs that promise behaviour over open-ended inputs, facts re-derived from git history, narrow approvals that do not predict the gate, and requirement rows that restate code and drift with every fix.

| # | Change | Kind | Cost | Removes |
|---|---|---|---|---|
| 6 | Lint before review: the brief renderer refuses while mechanical checks fail | small build | ~1 lane | ~6 findings / 3 days, each a 25–35 min round |
| 1 | Closed coverage: promises over input spaces must be enumerated or fail closed by construction | ruling + rubric | hours | the largest class: 18 of 43 late findings |
| 4 | Make every review round full-lane (trial), so an APPROVE means the gate | ruling + trial | one lane to try | narrow-APPROVE → gate-finds-more loops (6 in WI-834) |
| 2 | Record a decision at its event; never re-derive it from history. Reshape WI-902 first | ruling, then WI-902 reshape | 1 spec amendment | WI-902's history-replay findings (6) |
| 5 | Requirements never reference code; code points up (owner ruling 2026-10-11): schema, commit-time lint, contract voice | ruled · 1–2 WIs, last | schema WI + migration | requirement churn from code moves; much of the ~24 spine-text findings |
| 3 | Split at birth when deliverables are independent and the WI is large | ruling | none | see the answer below: helps above a size, hurts below it |

Order is cheapest-and-surest first. Numbers come from one analysis pass over `docs/reviews/`, the handoffs and `docs/log.d/`; treat them as claims at the precision of a three-day sample.

## The owner's two questions

### Narrow rounds and the full gate: what's actually different?

Yes, a narrow round is restricted to the diff since the last reviewed commit. Three things separate it from the gate:

|  | Narrow round | Full-lane gate |
|---|---|---|
| Reading scope | `git diff <last reviewed>...<tip>`: only the commits since the last review. The template's `{trunk}` slot is filled with the round's base (`review_brief.py:309`) | The whole lane from its trunk base to its tip, code and rows together |
| Assignment | "For each finding, confirm the fix at its own site, then try one other site of the same failure class" (`agent_brief.py:653`). Row wording is deferred to the checkpoint. | "An APPROVE must mean you tried to break it and failed": map every Done-when item to a covering test, hunt the worst failure classes, sweep the rows (K1–K4) |
| Session | Fresh `codex exec` | Fresh `codex exec` (`final_reviewer = "fresh"` in `docs/process.toml`) |
| Wall-clock | 5–8 min | ~11 min |

So a narrow APPROVE certifies "the named fixes hold, plus one probe per class". It does not certify the lane. Three kinds of finding can only show up at the gate:

- **Regressions outside the delta.** A fix changes behaviour that unchanged code in the lane relies on, e.g. WI-834's "newly denies … (baseline allowed it)". The narrow reviewer reads the fix but not what the fix changed for its callers.
- **Done-when gaps.** Only the gate maps the spec to tests.
- **Re-sampling.** A fresh full reviewer picks a new corner of any open input space (item 1). That is luck of the draw, not a missed defect.

Every narrow APPROVE also triggers a checkpoint: a Terra reconcile, a closure check and a sitting. When the gate then finds code defects, the lane goes back to iterating and owes another checkpoint. That is where the time goes. The review step itself is only about 3–6 min dearer for a full read. Item 4 builds on this.

### Does splitting a WI actually help, or just move the work around?

Mostly your intuition is right. Splitting pays only at the very top of the size range, and it costs time everywhere else. Data: 38 code-changing WIs claimed and landed 2026-10-03 → 10-11. Active hours exclude any gap over 2 h, which strips nights and rate-limit waits.

| Code lines changed | WIs | Median rounds | Median sittings | Median active h | Active h / 100 lines |
|---|---|---|---|---|---|
| 1–299 | 16 | 2 | 1 | 1.15 | 1.19 |
| 300–999 | 6 | 2 | 3 | 1.2 | 0.16 |
| 1,000–2,999 | 14 | 4 | 4.5 | 3.45 | 0.27 |
| 3,000+ (WI-841, WI-834) | 2 | 19 | 16 | 12.8 | 0.30 |

- **There is a fixed floor of about 1 h, 2 rounds and 1 sitting per WI**, whatever its size. The nine smallest code WIs (under 120 lines) sit right on it. A split pays that floor again for every piece, so splitting anything under ~1,000 lines makes the queue slower, not faster.
- **Time per line stays roughly flat above 1,000 lines** (0.27 → 0.30 h per 100 lines). Cost does not explode with size in general.
- **Round counts do jump in the two WIs over 3,000 lines**: 17–21 rounds, against a median of 4. Both carry confounders, though. WI-841 ran before narrow rounds existed, and WI-834 combined an open input space (item 1) with six disputes. Item 1 would have prevented much of WI-834's churn at any size.
- **The arithmetic for a 4,000-line WI.** Kept whole, it took about 12–14 active hours and about 19 rounds. Split into three WIs of about 1,300 lines, it would take about 3 × 3.4 h ≈ 10 h and about 12 rounds. That saves 15–25% of the time and about a third of the rounds. Real, but modest, and smaller than what items 1, 4 and 6 can save across every WI.

Splitting has one benefit the hours don't show: **containment**. In one large lane, a finding in one subsystem forces a fresh full gate over all three, and nothing lands until everything is clean. Three lanes land independently, and a stuck piece doesn't hold the other two. That matters most when the subsystems really are separate, which was true of WI-834 (shell parser, dev-setup readiness, hook opt-in). So the rule in item 3 is narrow on purpose.

## 1. Closed coverage: bound the promise before the claim

**Evidence.** 18 of the 43 late findings came from enumerating an open input space. 8 were shell grammar forms in WI-834 (heredoc, `coproc`, `time -p`, `. claude`, function definitions…). 3 were malformed store records in WI-887. 6 were git-replay edge cases in WI-902, and 1 was an ambient credential source in WI-798. The builder asked mid-WI-834 for "a closed, declared list … so this class stops reopening one form per round" (`docs/reviews/wi-834/025-DISPUTE-findings.toml:18`); the churn ended only once dispute sittings drew that line at rounds 25 and 31.

**Root cause.** The spec and its `## Trust` section promise behaviour over an unbounded set ("any command word", "every failed-write shape", a ruling per consumer × per bad-input kind). The reviewer brief demands an attempt to break the change, and each gate is a fresh session, so every round samples a new member of the set. Each finding is valid. The set is the bug. WI-902's Trust section shows the multiplication: it rules absent / unreadable / failed / malformed for each of six consumers.

### Proposal

1. **Scope critique gains anchor S3, "Coverage is closed"** (`docs/rubrics/scope-critique.md`). Any promise over an input space is either (a) an enumerated list with a stated fail-closed default for everything else, or (b) a construction that makes the space irrelevant: deny by default, or validate a whole record against one schema. *Bad:* "detects any shell form that launches the CLI".
2. **The Trust ruling collapses to one reader.** Rewrite the bad-input part of the Trust question in `coordinator-cycle` §1: every consumer reads the carrier through one owning parser. That parser accepts exactly the well-formed shape and refuses everything else with one reason class. The Trust section then lists consumers but states one ruling, not a consumer × shape matrix. This is the reviewer template's own "validate once at a single owning boundary".
3. **Reviewer brief: out-of-list findings are classed, not blocking** (`project-trajectory/prompts/reviewer.template.md`, shipped). An input outside the spec's declared list that the change fails closed on becomes a `coverage-extension` note for the spine change list or a successor row. If the change fails *open* on it, it stays a finding at full severity.
4. **Revisit WI-834's parser (a candidate WI, not part of this program).** Ruling 040 already accepts over-denial inside a blackout window as failing closed (`docs/reviews/wi-834/040-ADJUDICATE…:72`). A "deny any line that mentions a model CLI" rule would delete the parser and its whole grammar class. Before filing, check whether that over-denial would bite real use.

**Trade-off.** A closed list can miss a real form. The fail-closed default turns that miss into an over-refusal, not a hole, and a successor row extends the list on purpose instead of a review round discovering it by accident.

**Measure.** The "open input space" share of late findings: 18/43 today, target ≤ 3 over the next 15 WIs.

**Downstream.** Step 3 changes a shipped template: one `RESYNC_PACK.md` entry, no migration. Steps 1–2 are this-repo only.

**Owner calls:**

- Confirm S3 as a scope-critique anchor.
- Confirm the one-reader Trust rule.
- Confirm that a fail-closed out-of-list input is a coverage note, not a blocking finding.

## 2. Record the decision at its event; never re-derive it from history

**Evidence.** WI-902 lets a disposition name an existing successor. Its sweep now "reads the open-state rule in the tree of the commit that landed the disposition (the oldest first-parent commit touching its spec in `complete/`)", added by review 001 F1, review 008 F1 and ruling 009 (spec, Consumers → The sweep). That history read then produced the shallow-clone, lossy-decode and file-existence findings. The lane stopped under the two-round breaker after 9 rounds and 6.3 h.

**Root cause.** Two consumers, the close and the sweep, each re-validate the same adoption, and the sweep re-validates it on every run against whatever trunk is now. When that answer turned out to drift (the successor completes later), the fix replayed history to recover the original answer. This is the pattern your 2026-10-03 rule forbids: enforce at the commit, not through git-history archaeology.

### Proposal

1. **Reshape WI-902 before resuming it**, as a spec amendment with a scope critique, not another build round. The close is the single owning boundary: it validates the adoption once (the named row is open and supersedes the disposed row) and records the result in the commit that closes the row, e.g. an `adopted = "WI-893"` cell on the closed row. The sweep trusts that recorded cell and never consults later trunk state or history. Most of the current Trust matrix and the history read go away.
2. **State the rule once** in `PROCESS.md` §3, beside "When a guard is owed": a decision a later step depends on is recorded by the step that makes it, in the commit where it is made. A later reader trusts the record and never recomputes it from history. Add the matching scope-critique bad example (B3: "a consumer that re-derives a past decision from history or current state").
3. **Audit the other history readers** (a read-only research task, not a build). 21 kit scripts call `git log`, `rev-list` or `--first-parent`; most legitimately diff a range. Classify each as "reads a range to review/check" (fine) or "recomputes a past decision" (candidate), and file a row only for the candidates.

**Trade-off.** One more recorded cell on the closed row. In exchange, the sweep's correctness no longer depends on clone depth, decode or file layout over time.

**Measure.** The reshaped WI-902 lands in ≤ 2 review rounds. The audit turns up few or no candidates.

**Downstream.** WI-902 changes shipped scripts either way (its Done-when already owes a RESYNC entry). The added cell is new data, not a migration.

**Owner calls:**

- Resume WI-902 as built, or reshape it to record-at-close first (recommended)? Its Trust ruling (coordinator-2026-10-11 D-005) is still pending your confirm or overrule.
- Confirm the record-at-event rule for `PROCESS.md` §3.

## 3. Split at birth, above a size

**Evidence.** See the splitting answer under "The owner's two questions". There is a floor of ~1 h, 2 rounds and 1 sitting per WI. Cost per line is flat from 1,000 to 3,000 lines. The only blow-ups (WI-841, WI-834) were both above 3,000 lines and both bundled independent subsystems.

**Root cause.** S1 of the scope critique already asks for independently landable deliverables, but it gives no basis for when keeping them together is costly. So the answer defaults to "keep together".

### Proposal

1. **Add a size basis to S1** (`docs/rubrics/scope-critique.md`). Split at birth only when *both* hold: the deliverables land independently (S1 already names them), and the row's expected code change is large, roughly 2,000+ lines or more than about four script families. Below that, keep the row whole even if it has several deliverables. This sits at birth, so it respects your 2026-10-07 ruling of no lane-size tripwire.
2. **Don't split to fix churn mid-lane.** A lane that starts churning is usually an item 1 problem (an open promise), not a size problem. The remedy is a dispute sitting that draws the coverage line, as WI-834's rounds 25 and 31 eventually did.
3. **Optional, data-backed: batch the tiny ones.** Docs- or spine-only rows land at ~0.5 h each. Code rows under ~150 lines pay the full ~1 h floor. Where two or three small queued rows touch the same module and share a reviewer's context, filing them as one row saves a floor each. Only worth doing when they truly share context.

**Trade-off.** A size estimate at birth is a guess. That's acceptable because the rule only bites on the very large rows, where the guess is easy.

**Measure.** No landed WI above ~3,000 code lines without a recorded owner reason to keep it whole.

**Downstream.** None (this-repo rubric).

**Owner calls:**

- Confirm the narrow split rule: independent deliverables and ~2,000+ code lines.
- Decide whether same-module tiny rows should be batched.

## 4. Make an APPROVE mean the gate

**Evidence.** In WI-834, narrow approvals 010, 014, 020/022, 026, 034 and 037 were each followed by a full gate that found new defects. 15 of the late findings were regressions from a previous fix. Each such loop cost a checkpoint (Terra reconcile, closure check, a 3–6 min sitting) that the next gate made stale.

**Root cause.** See the answer above: a narrow round verifies fixes, it does not certify the lane. Yet its APPROVE is what triggers the checkpoint.

### Options, recommended first

1. **Full-lane every round (trial on the next two lanes).** Drop narrow rounds. Every round is a fresh full-lane review that still carries the previous round file and the coverage plan as context, so it still confirms each fix. The checkpoint fires only on a full review with no BLOCKER or MAJOR, so a sitting is never spent on a lane the gate will reopen. Cost: ~3–6 min more per review and more Codex quota per round. Fewer rounds and fewer stale checkpoints should more than repay that, but measure it. Change lives in `coordinator-cycle` §3 and recipes §1; `review_brief.py` already supports `--scope full` with no findings file.
2. **Widen the narrow round to the fix's blast radius.** Keep narrow rounds, but the brief also lists the callers of every symbol the delta changed, and asks for one behaviour comparison against the lane's base for each. This catches the "baseline allowed it" regressions while keeping narrow rounds cheap. Needs a small `review_brief.py` change (shipped).
3. **Persisted final reviewer** (`final_reviewer = "persisted"`, built in WI-887, shipped off). The gate resumes the session that saw the earlier rounds, so it stops re-sampling from zero. Least preferred: your persistent-adjudicator study found anchoring evidence, and a reviewer that resumes its own approvals is the weakest form of independence. Worth trying only if options 1 and 2 don't move the numbers.

**Measure.** Checkpoints per landed WI. Full-gate rounds that find code defects after a checkpoint (target: near zero). Codex sessions per landed WI, against the ~15–24-session limit.

**Downstream.** Option 1: none (this-repo procedure). Option 2: shipped brief, a RESYNC entry. Option 3: a dial flip.

**Owner calls:**

- Pick the trial: full-lane every round (recommended), blast-radius narrow rounds, or the persisted gate.
- Confirm the trial length (two lanes) and the metrics above.

## 5. Requirements never reference code; code points up

**Owner ruling, 2026-10-11:**

- Requirement rows carry no code references at all: no paths, modules, functions or symbols. Code blocks reference up to their requirements, and tests may still point to modules.
- Why: everything in the spine points up so that requirement ids stay stable. Code markers are not stable ids. A requirement that names code reopens every time the code moves, and that grinds requirements to a halt.
- Sequencing: this can be done last.

**Evidence.** About 24 of 79 findings were requirement-chain text, and the WI-798 sitting returned 11 rows at once. All 302 LLR rows carry `module` and `code_symbol` cells. LLR-312's `code_symbol` names five functions, and its `detail` narrates how they work ("plans one ordered sequence of rewrites … each rewrite starts from the specification as it then stands"). By a rough token census, about 202 of 302 LLR rows, 25 of 131 SR rows and 6 of 35 SN rows also name code-like tokens in their prose. The heuristic overcounts, but the order of magnitude stands. Any fix that renames or reshapes one of those functions makes an Approved row untrue. Then Terra reconciles, the sitting re-judges, and a return costs another sitting.

**Root cause.** The trace direction is mixed. `Implements:` tags in code already point up, but the LLR's `module` and `code_symbol` cells point down at the same facts and must be hand-synced. The R2 ruling (2026-08-15) kept SR cells free of artifacts but left two doors open: a filename in acceptance as "current carrier" evidence, and concrete names at the LLR tier. Code churn reaches the spine through those doors.

### What the rule covers

| Artifact | May reference code? | Direction |
|---|---|---|
| SN, SR, LLR rows (every cell, acceptance included) | No | point up only (SR → SN, LLR → SR) |
| Code (functions, classes, modules) | Yes: `Implements: LLR-NNN` | points up to its LLR |
| TC rows and tests | Yes: may name test modules and modules under test | verifies up; names code as evidence |
| Generated views (dashboard architecture, trace matrix) | Yes, derived | computed from the up-pointers, never authored |

The R2 allowances go away under this reading: "current carrier" evidence moves from SR acceptance to the TC rows that verify it, and the LLR tier states contracts, not carriers. R2's third guarantee, "why does this file exist", is kept by the inverse check: every shipped module carries at least one `Implements:` tag naming a live LLR, so a file with no requirement above it is a finding.

### Bounding it mechanically: three layers, strongest first

1. **Make it unrepresentable in the schema.** Delete `module` and `code_symbol` from the LLR schema (`kitlib/spine.py`), and make the loader refuse keys a requirement tier doesn't declare, so a row *cannot* carry them. Everything that reads those cells today (`trace.py`'s back-link check, `trajectory_arch.py`/`gen_trajectory.py`, `lane.py`, `check_doc_refs.py`, `spine_carrier.py`/`migrate_carrier.py`, `check_privacy.py`) switches to one derived index built from the `Implements:` tags. The index is generated, never committed as authored data. This removes the hand-synced cells entirely, and with them the K3 rubric anchor.
2. **A commit-time check on requirement prose**, grown from the existing warn-only `trace_text.sr_artifact_advisories` (which today flags only `*.py` in SR requirement cells). Extend it to every text cell of SN, SR and LLR rows, and add a second token class derived from the code itself: the set of names defined in the shipped scripts (functions, classes, module constants, read by `ast`). A cell is refused if it contains a path-like token (`.py`, `scripts/`, a repo path that exists) or one of those code names written as code: backticked, snake_case with an underscore, CamelCase, or a call form. Plain English that happens to match a function name (`close`, `main`) passes. The name list comes from the code on every run, so nobody maintains it. Following your enforce-at-the-commit rule, it compares the commit against its parent: a row added or changed in the commit must be clean, and untouched rows are left alone. Existing prose then migrates as lanes touch rows, without a mass reopening. It runs in the pre-commit hook and in item 6's pre-review gate.
3. **Judgement layer.** The adjudicator's sitting brief and the `spine-authoring` skill extend K2 from SR to all requirement tiers, written as contract voice: an LLR states the observable obligation (inputs, outcome, refusal boundary) and must survive a refactor that keeps behaviour. Test: would renaming a private helper or reordering steps make the row untrue? If so, it is describing mechanism, which belongs in the docstring. The mechanical layers catch names; this layer catches mechanism narrated in plain words, which no lint can.

Alongside: **one judge per row.** The adjudicator's sitting is the sole judge of requirement text. Sol's code review raises a row finding only when code contradicts an Approved row, or a row the lane added is untrue against the code. That removes the double judging behind part of the spine-text churn, and both judges stay independent of the author.

**Migration.** Layer 1 removes two cells from all 302 LLR rows, most of them Approved, which the `approval-immutable` check forbids today. It needs one ruled batch act: "trace cells removed, requirement text unchanged". That is a single sitting for the batch, not 302 re-attestations. Layer 2 needs no migration: prose is cleaned as rows are next amended.

**Downstream.** A kit schema change. Adopters' LLR registries carry `module`/`code_symbol`, so this needs a `RESYNC_PACK.md` entry with a migration script (`migrate_carrier.py` is the precedent), an `ADOPTING.md` note and the template rows' update. Flagged per edit-conservatively: this is the one item in the plan that forces adopters to migrate.

**Measure.** Requirement rows amended because code moved: target 0. Rows returned per sitting. Spine-text findings per landed WI.

**Open questions for the owner:**

- Confirm the reading above: no code in SN/SR/LLR rows, acceptance included, so "current carrier" evidence moves to TC rows. This supersedes R2's two allowances.
- Interface (IF) and component (CMP) rows name concrete seams and modules today. Are they requirements under this rule, or architecture that may point at code? My lean: CMP rows point up like code; IF rows name a seam's contract, not its file, but a separate look is needed.
- Confirm the one-judge split between Sol and the sitting.

## 6. Lint before review

**Evidence.** About 6 findings were things an existing instrument already catches: SR-239's two "shall" clauses (`trace.py --strict`), IF-292's channel outside the closed set, an IF cell over 160 characters, a missing `RESYNC_PACK.md` entry, an undeclared IF seam. Each cost a 25–35 min round and Codex quota.

**Root cause.** The commit hook runs `trace.py --strict-integrity` but not the semantic `--strict` lints, and runs `check_trajectory.py --staged` non-blocking (`|| true`, `project-trajectory/hooks/pre-commit:296`). Nothing runs the stricter checks between a commit and a review, so a human-grade reviewer spends a round on them.

### Proposal

1. **`review_brief.py review` refuses to render while the pre-review lints fail**: `trace.py --strict`, `check_trajectory.py --strict`, and a RESYNC-presence check (a shipped file changed in the range ⇒ an entry anchored at a trunk commit). The refusal names each failure. The renderer is the one door every review goes through, so this is a mechanism, not another recipe line to remember.
2. **Mechanize what K2–K4 still ask a reviewer to eyeball** where it's cheap. K4 is step 1's RESYNC check. K3 (each `Implements:` tag matches its LLR's `module`/`code_symbol`) goes away with item 5's schema layer. K2 becomes item 5's commit-time prose check.
3. **Drop those anchors from the reviewer rubric** once each is mechanized, so the reviewer's attention goes to judgement.

**Trade-off.** The renderer gets slower by the lints' runtime, seconds against a 25–35 min round. Refusing at render could block a review of a deliberately red lane, so allow an explicit `--allow-lint-fail <reason>` that prints into the brief.

**Measure.** Findings an instrument would have caught → 0.

**Downstream.** `review_brief.py` is shipped: one RESYNC entry, no migration.

**Owner calls:**

- Approve filing this as the first build row.

## Sequence and how we'll know

| Phase | What | Who |
|---|---|---|
| 0 · rulings | Items 1 (S3, one-reader Trust, coverage notes), 2 (record-at-event rule, WI-902 reshape), 3 (split rule), 4 (pick the trial), 5's open questions (IF/CMP scope, one judge); 5's core rule is already ruled. No code. | Owner |
| 1 · cheap builds | Item 6 lint gate (first row). Rubric and skill edits for 1, 2, 3, 5. Reviewer-template clause for 1. | Coordinator lanes |
| 2 · trial | Item 4 on the next two lanes. WI-902 reshaped and resumed as the first lane under the new rules. | Coordinator |
| 3 · structural (last) | Item 5: schema removal, derived index and batch act, plus the commit-time prose check. Item 2 history-reader audit. The WI-834 deny-on-mention candidate, if the audit of real use supports it. | Coordinator lanes |
| 4 · re-measure | Re-run the same churn analysis over the next 15 landed WIs and compare against the baseline below. | Coordinator / analysis agent |

| Baseline (2026-10-09 → 10-11) | Now | Target |
|---|---|---|
| Review rounds per reviewed WI (mean, 69 / 21) | 3.3 | ≤ 2 |
| WIs needing ≥ 6 rounds | 4 of 21 | ≤ 1 in 15 |
| Late findings from open input spaces | 18 of 43 | ≤ 3 |
| Findings an instrument would catch | ~6 | 0 |
| Gate finds code defects after a checkpoint | 6 in WI-834 alone | ≈ 0 |

What this plan deliberately doesn't do: reduce review depth or the reviewer's stance. The 15 genuinely new defects caught in late rounds (WI-834's warm-tick race and interpreter mismatch, WI-902's truncated fence, WI-887's misspelled config value) were worth catching. The aim is to stop paying for the same class over and over.
