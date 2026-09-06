# Third Fable review — cross-check of the expanded plan

**Date:** 2026-09-05. **Reviewer:** Claude Fable 5.1 through Claude Code, same session as the second review, at revision `360a075a`. **Input:** the [cross-check brief](CROSSCHECK-BRIEF.md) and the documents it names, plus the [hats and decomposition sweep](HATS-AND-DECOMPOSITION-REVIEW.md). **Owner's framing:** check for gaps, and watch for places where the plan over-engineers or over-constrains the solution. No implementation, dial, registry, or queue change; no tests were run for the review itself (the commit bar for the resulting edits is recorded in the log fragment).

## 1. Verdict

**Executable for the next slice (P0a, P0b) with named corrections.** The expansion is well-grounded: every source symbol it cites exists, the 18-item backlog map and 27-need mapping are complete, and the fresh-builder-per-rework decision and the durable-boundary table are the right size. The corrections below are almost all in one direction: the plan has started to grow machinery beside the thing it exists to shrink. Four places add a tier, a policy engine, a schema, or a roster entry where a smaller form does the same job. Each correction names the smaller form and has been applied to the active documents (§6).

Nothing past P0 is executable yet, by the plan's own design: the decision gate, P1A and the P5 stop/go come first.

## 2. Corrections accepted from the expansion

Codex corrected two claims of the second review, and both corrections stand:

- **The DevStg-Tests bar is not a false claim.** `Bar-Green` names the steps it ran; a selected bar with no test step is honest labeling. The gap it leaves is treated in §3, C1.
- **Worktrunk.** `--no-commit --no-rebase` preserves the branch's commits, and git is already a required binary, so "the first non-Python binary dependency" should have read "the first binary beyond git." Also verified this round: `--yes` bypasses the hook-trust prompt and `--no-hooks` skips hooks entirely, so unattended use is feasible. The ruling (optional operator tool, no station prototype) is unchanged and the second review carries an addendum.

## 3. Findings

Ordered by consequence. Each names the plan section, the counterexample, the obligation at stake, the evidence, and the smallest correction. Findings are grouped as the brief asked: contradictions, then over-engineering, then untested hypotheses and gaps.

### Contradictions

**C1 — Merges at DevStg-Tests run no product step, and the replacement for the withdrawn fix is a policy engine.** *Section:* EXECUTION-DETAILS §4; IMPLEMENTATION P0 "Separate check selection from stage meaning." *Counterexample:* a lane edits `integrate.py`, breaks an existing behavior with a passing test, refreshes at DevStg-Tests, and merges with a green `Bar-Green`. *Obligation:* SN-008 (honest verdicts) and SN-007 (the kit verifies itself through changes). *Evidence:* `check.py --stage DevStg-Tests --list` selects fourteen process steps and zero product steps; `format`, `lint` and `tests+coverage` are keyed to DevStg-Impl in `check.py`. The repository has stood at DevStg-Tests for weeks with a stable codebase and about 3,254 tests. The proposed six-row "validation owed per change kind" table is a second selection mechanism beside the stage ladder, which the section itself says to avoid. *Smallest correction:* one declared step in this repository's `docs/stack.ini`, `[step:smoke]`, `from-stage = DevStg-Tests`, running the existing smoke tier (`{py} -m pytest -q -n auto -m smoke`). That is the per-commit bar the working agreement already demands of every agent by hand, made a step the station runs. It changes no ladder semantics and needs no SN-007 amendment (it adds a check; it narrows nothing). A failing-first test, when one exists, carries a marker excluded from that step; the marker is decided when the first such test is written, not before. Keep §4's table as vocabulary for reports ("selected checks passed" versus "full suite passed"); do not build it as a selector.

**C2 — Three decision agendas.** *Section:* README §6 (13 items), CROSSCHECK-BRIEF §3 (12 rows), and the Claude plan's §7 (11 items) now all serve as the ruling agenda. *Counterexample:* the owner rules on README item 12 and the brief's "Capabilities/cuts" row differently, and nothing says which wins. *Smallest correction:* the brief's §3 is the agenda; README §6 keeps its numbered list as the plan's positions and says so. Applied as a sentence, not a restructure.

### Over-engineering and over-constraint

**O1 — A sixth tier above the needs.** *Section:* VISION-OBJECTIVES.md; EXECUTION-DETAILS §7 rows P1b and P9b; IMPLEMENTATION P9. *What it adds:* six objective keys with HTML anchors, an `objective_refs` field on the SN carrier, parser and validation changes across five modules, approval-field classification, trace output, a downstream migration recipe, a dogfood fixture, adopter tests, and two implementation slices. *Counterexample:* the redesign's own thesis is that the spine carries too many tiers describing the kit to itself; this adds a tier while P9 is trying to remove rows, and SN-033 already requires each need to be recognizable as a stakeholder outcome. *Smallest correction:* the document's own fallback. Six headed clauses in the root README's vision section, prose anchors only, no schema field, no slices. The 27-row mapping stays in this folder as a review worksheet. Revisit a carrier field only if, after P9's consolidation, a reviewer still cannot navigate purpose to need. Applied: status block on the document; P1b and P9b marked deferred; the P9 bullet reworded.

**O2 — The invocation-metrics contract is sized for a billing system.** *Section:* EXECUTION-DETAILS §2. *What it adds:* seven field groups, six aggregation rules, a provisional-record spool with atomic finalize, restart reconciliation, a flush-after-P5-turn rule, coverage reporting, eight acceptance scenarios and sanitized provider fixtures. *The question it answers:* whether usage is tracked per session for later metrics. *Counterexample:* the first consumer of these records is the P0 control table, which needs role, WI, route, tier, tokens and cost per session. Nothing in P0 through P8 reads a cumulative-counter delta or an auxiliary-model inclusion flag. *Smallest correction:* P0b ships the minimum record by extending the existing session-log writer — `invocation_id`, `wi_id`, attempt, role, provider, requested and reported model, routed tier, roster row, start and end, exit status, and the token and cost counters as the provider reports them, with `null` for anything unavailable — under three rules: a new process is a new id even when it resumes a conversation; a failed or timed-out call still gets a row; an unknown number is never coerced to zero. Everything else in §2 is deferred until a consumer needs it. Applied as a "Minimum first" block; the fuller contract stays as the deferred design.

**O3 — The hats sweep adds a roster entry and pre-decides new requirement rows.** *Section:* HATS-AND-DECOMPOSITION-REVIEW §1 (a seventeenth hat and charter extensions for four hats), §2 H2, H3, H5 (new SR obligations), H4 (a landing obligation). *Counterexample:* the roster header itself asks the owner to cut hats that do not earn their place, and the audit shows SAFETY attributed to no row; an `always` hat whose usual answer is "no compatibility impact" is the ceremony that header warns about. Minting SRs while P0's disposition map is being built decides part of the map early. *Smallest correction:* H1 is a defect, not a decomposition question — the planner brief composes hat context from the WI row and never merges the referenced need's context, so LEGAL and DATA-PROTECTION do not reach an SN-026 decomposition. That is a targeted repair WI on its own evidence, now. H2 through H5 are "promise-tier clause with no SR home" entries in the P0/P1a disposition manifest, decided alongside every other row with the same six-way vocabulary. The upgrade question folds into FIRST-RUN-ADOPTER's charter as the sweep's own smaller alternative; a separate hat is minted only if the manifest shows the two questions cannot be kept distinct there. H7's carrier-drift repairs belong to P1A. Applied as dispositions here and a pointer in the README; the sweep document is unchanged.

**O4 — The per-slice reconciliation ritual.** *Section:* BACKLOG-MIGRATION §4. Six steps per authorized slice, each with a six-field record. Proportionate for slices that touch queued work; disproportionate for a parser cleanup. *Smallest correction:* none applied. Read "for each authorized slice" as "for each slice that overlaps a queued or active item," which is what §1 already says. Noted, not edited.

### Untested hypotheses and gaps

**GAP-1 — The control window may not have the work to fill it.** *Section:* EXECUTION-DETAILS §6 (two weeks, at least 20 completions). *Evidence:* the loop is paused; the queue holds 18 items, of which four are adjudications of earlier merges and two are held on owner rulings. The plan hedges ("keep the sample small and report uncertainty") but does not say what the gate does when evidence stays insufficient. *Smallest correction:* name the default now so the window cannot loop: insufficient evidence after the declared window resolves to *targeted repair* (the independently justified slices proceed; P3 through P8 stay closed), with a second window only by explicit ruling. Applied as one sentence in §6.

**GAP-2 — The plan's own preparation is generating the interventions it wants to measure.** *Evidence:* three log fragments this month record smoke-budget breaches, and both of codex's documentation commits needed an owner exception for a timing breach on a diff that touched no script or test. *Smallest correction (recommendation only, owner rule):* a diff that touches neither `project-trajectory/scripts` nor `tests/` owes the hook floor, not the timed smoke run, at the commit bar. That is a working-agreement change in CLAUDE.md and the session-protocol skill, byte-budgeted, so it is proposed here and not applied. The alternative kept from the Claude plan, reporting the budget as the median of three runs and flagging noise, is the larger change.

**GAP-3 — Fresh builder per rework: confirmed, one omission.** *Section:* EXECUTION-DETAILS §3. The decision matches current `apply_rework_scope` behavior and is the right default. It does not say what the rework brief carries when the *reviewer* changed between rounds (a tier escalation) and the new reviewer's findings contradict the old ones. *Smallest correction:* the brief carries every unresolved finding with its round and reviewer; a contradiction between rounds is a dispute routed to the existing one-attempt arbitration, not a third opinion. Applied as one sentence.

**GAP-4 — What the hats review verified and what it did not.** The `_hat_slots` probe is real and reproducible; the SN-to-SR sweep is source reading corroborated by an earlier alignment document. Treat its "covered" cells as one reader's judgment, as it says. No correction.

## 4. Proportionality report

The brief asked specifically whether the objective layer and the metrics and recovery contract remain proportionate.

- **Objective layer:** not proportionate as a carrier; proportionate as prose. Ruled to the smaller form (O1).
- **Metrics contract:** not proportionate for P0's consumer; proportionate as a deferred design. Ruled to a minimum record plus three rules (O2).
- **Recovery contract (EXECUTION-DETAILS §1 boundary table, §5 injected events):** proportionate. Nine boundaries and nine injected events is the state model P1 asked for, and each row is a test, not a mechanism.
- **Slice table (§7):** proportionate at seventeen rows after P1b and P9b are deferred. It is a planning aid, not a schedule.

## 5. Counterexamples from the brief, answered where the plan now stands

1 and 2 (objectives): moot under O1; the mapping is a worksheet. 3 and 4 (metrics replay, crash before export): deferred with the fuller contract; the minimum record has no replay path to get wrong. 5 (mixed review outcome): covered by §3's outcome table plus GAP-3. 6 and 7 (retention, WI-557 reports): covered by BACKLOG-MIGRATION and the §3 retention paragraph. 8 (self-relaxing policy, mid-flight tightening): covered by §1 and §5. 9 (failing-first versus regression): covered by C1's marker convention, decided when the first such test exists. 10 (WI-596 absorption): held in BACKLOG-MIGRATION. 11 (P5 serial cost): the P5 budget text already counts every turn. 12 (rollback after first acceptance): IMPLEMENTATION §5 covers it; unchanged.

## 6. Edits applied

- `VISION-OBJECTIVES.md` — disposition block after the status line: smaller alternative adopted, carrier field deferred.
- `EXECUTION-DETAILS.md` — §2 "Minimum first" block; §4 "Smallest sufficient form" paragraph; §3 one sentence on reviewer change between rounds; §6 one sentence on the insufficient-evidence default; §7 P1b and P9b marked deferred.
- `IMPLEMENTATION.md` — P0 check-selection bullet gains the smallest form; P9 objective bullet reworded to the deferred position.
- `README.md` — decision 9 gains the smallest form; decision 13 reworded; the brief's §3 named as the single agenda; the hats sweep pointer names this review's dispositions.
- `CROSSCHECK-BRIEF.md` — "Answered" line pointing here.
- `FABLE-REVIEW-2-GOVERNING-PLAN.md` — dated addendum accepting codex's two corrections.

The hats sweep, the historical Fable reviews and their metadata are unchanged.

## 7. Limits

Source reading and one harness listing; no tests run for the review itself. Worktrunk still read, not executed. The hats sweep's SR coverage judgments were spot-read, not re-derived. The smallest form in C1 was checked against the harness's step grammar and the smoke tier's existence, not by running the station with the new step.
