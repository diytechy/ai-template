+++
id = "WI-911"
title = "Review-churn batch 1, text: the review shape, binding pre-claim advice and the rules every later lane runs under"
workstream = "process"
sr_refs = ["SR-146", "SR-154", "SR-235"]
specref = "docs/plans/2026-10-11-review-churn/README.md#owner-rulings-2026-10-11"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
needs = []
+++

## Context

Filed on trunk on 2026-10-14 by the attended coordinator as the review-churn
program's batch row B1 (`docs/handoff-2026-10-11-attended-coordinator.md`,
the queue table). The plan's "Owner rulings" section, 2026-10-11 through
revision 37, is the spec of record: where this row and a ruling differ, the
ruling governs, and this row cites it rather than restating its reasons.

B1 is split at filing under S1 (coordinator-2026-10-14 D-002). This row is the
text every later lane runs under, plus the one render change the scope
critique's widened artifact line needs. The verdict/act split (plan item 16,
revisions 32 and 36: sitting briefs that judge only, an act turn in the
coordinator's adjudication entry point, and the `Loop-Session` trailer line
for a marked sitting) is WI-912, which lands after this row.

Until this row lands, the handoff's "How to run reviews now" section carries
these rules by hand. Once it lands, the skill carries them, and the next
handoff points at the skill instead.

## Deliverables

One lane, one landing. Each item names its ruling; the builder writes the
rule in the target's own voice and does not copy the plan's reasoning.

1. **The `coordinator-cycle` skill** (kit source
   `project-trajectory/skills/coordinator-cycle/`, synced to
   `.claude/skills/`; `scope: this-repo`, so no RESYNC entry):
   - **The review shape** (rulings 4 and 7, the revision 6–8 clarifications,
     revision 33, revision 37). There are no narrow rounds. Each round runs
     the full-lane reviewers in parallel, each from its own render of
     `review_brief.py review --scope full` with its own `--scratch`. Reviewer
     A is Codex Sol at medium (REVIEW-A). Reviewer B is another family or
     model, filed REVIEW-B: a Claude stand-in, recorded as a substitution in
     the lane's decisions, until WI-815's Gemini route has one verified
     launch. A Claude reviewer is a sub-agent given only its brief's path.
     During the review-churn program a third reviewer runs as a recorded
     trial: both Claude reviewers file REVIEW-B under their own numbers, and
     the lane's decisions name the model behind each file and which reviewer
     raised each accepted finding. Nothing is built for a third slot.
   - **Rounds and the cap.** At most three full rounds before the checkpoint.
     Rounds run until one has no BLOCKER or MAJOR code finding, and the
     checkpoint follows it. The gate over the checkpoint tip, and a round
     over a rebase that changed code or rows, always run, in convergence
     stance, and are not counted. At the cap, open findings go to one
     dispute sitting, which rules each FIX-as-successor, DISMISS or ESCALATE.
     A convergence-class finding (fail-open, data loss, Done-when gap) is
     never deferred: the sitting orders one more fix round or escalates.
     Successor rows are filed on trunk at the landing from the sitting's
     binding. Only BLOCKER and MAJOR cost a round; a MINOR goes to the spine
     change list or a successor row. A lane in flight when this lands starts
     its count at zero at its next review, recorded as a decision.
   - **The convergence round** never sees earlier verdicts. Before it, the
     coordinator maps every accepted finding to a regression test that fails
     on the pre-fix code, or, for a fix with no executable test, to
     independently checkable evidence (the corrected text at the cited site,
     or an inspection record). A round the coordinator cannot map in full
     does not start.
   - **What reviewers get:** the WI definition (spec, Done-when, Trust,
     touched rows), never the builder's coverage plan. The narrow-round steps
     go: iterate step 2, and carrying the coverage plan into the next review.
     The coverage plan stays the builder's tool before a fix.
   - **Before the claim** (rulings 1 and 9): every scope-critique
     recommendation gets a disposition, adopted (quoting the spec text that
     now carries it) or rejected (with the reason), and a fresh critique
     round confirms the adopted ones before the claim. A queued row born
     before S3, S4 and the delta question is re-critiqued when it comes up
     for claim, one at a time.
   - **After each build round** (ruling 6): `trace.py --strict` and
     `check_trajectory.py --strict` with the commit bar, at the closure check
     and at the landing check, never in the commit hook.
   - **Sub-agents** (revision 37): planners, builders and reviewers may spawn
     them within the spawner's bounds, as the ruling states them (a
     reviewer's see only its brief and write only its scratch; a builder's
     never put two writers on one file; none reviews or adjudicates its
     spawner's work; each test runner has its own `--basetemp`).
   - **Tests across parallel lanes** (owner, 2026-10-14): one basetemp per
     test runner; the landing's budget reading is taken quiet; free disk is
     checked before lanes fan out, and the full suite runs alone at phase
     close; a red that passes when re-run quietly is filed as a
     load-sensitive defect, never charged to the lane or re-run until green.
   - **§4, two landing rules** (owner, 2026-10-14): a lane that changes the
     machinery the cycle runs on lands alone, and the next such lane lands
     only after the cycle has run through the last one's changed step; a
     defect in a landed mechanism change is fixed forward in a lane with a
     regression test, never by reverting a landing, and a step the defect
     blocks runs by hand, attended and recorded, never through a bypass flag
     or a fallback path. A hook that refuses the fix commit is the owner's to
     decide.
2. **`docs/rubrics/scope-critique.md`** (this repo's rubric):
   - **S3, coverage is closed** (ruling 1): a promise over an input space is
     either an enumerated set with a declared default, or a construction
     that makes the space irrelevant (deny by default, or one schema over the
     whole record). For an unbounded grammar the spec chooses deny by
     default. The answer becomes spec text before the claim, in the
     Done-when or the Trust section.
   - **S4, the planning need** (ruling 9), recorded as the row's `planmode`:
     `single` when the row has a `## Trust` section, touches two or more
     script families or interface seams, or promises behaviour over an input
     space; `dual` only on the existing design-shaping applies-when; `none`
     for a diff a cheap test fully specifies. No size threshold.
   - **The architectural-delta question,** in plan item 12 entry point 2's
     own words: does the WI add a state, add a value to a domain, make an
     output depend on a new input, or cross a new boundary? Within the
     row's scope, the spec carries the change; beyond it, a refactor row is
     filed on trunk before the claim. No pointer to a rubric that does not
     exist yet (item 12's text lane adds it).
   - **A dependency anchor:** the rows the row waits on, each in its `needs`
     with the reason, and any new third-party package, tool or service, each
     needing a reviewed row in `docs/dependencies.md` before the build.
   - **B3,** a consumer that re-derives a past decision from history or
     current state (ruling 2). **B4,** owner-dependent work not separated: a
     Done-when that needs an owner act or credential, mixed with unattended
     work, with no stated hold or partial disposition (revision 35).
   - **The widened artifact line:** the spec file, its `specref` target, and
     the registries the critic reads for S3, the delta and the dependency
     anchors (`components.toml`, `interfaces.toml`, the derived architecture,
     the runtime flows and `docs/dependencies.md`), which are registries,
     never code.
   - **The verdict section** says every recommendation will be dispositioned
     before the claim, so the critic writes each as one concrete change.
3. **`review_brief.py critique`** names those registries in the brief for the
   critic to read, beside the spec and its `specref` target, with a test that
   fails without it. (A shipped script: RESYNC entry.)
4. **`PROCESS.md` §3, the record-at-event rule** (ruling 2), beside "When a
   guard is owed": a decision a later step depends on is recorded by the step
   that makes it, in the commit where it is made, and checked against that
   commit's parent; a later reader trusts the record and never recomputes it
   from history or from current state. Shipped text: RESYNC entry. Check the
   byte budget before and after (`byte-budget-guard`).
5. **`project-trajectory/prompts/spine-questions.md` §3:** "LLRs name modules
   and symbols by design" is rewritten to ruling 5's contract voice, and says
   that the traced `module` and `code_symbol` cells stay filled and binding
   until item 5's schema lane removes them (`trace.py --strict-schema`
   requires both; `check_doc_refs --strict` binds the symbol) (revisions 35
   and 36). Shipped text: RESYNC entry.
6. **`scripts/coordinator/terra-spine-prompt.template.md`:** the same
   correction, and its R2 line no longer sends a file name to SR acceptance
   as current-carrier evidence (ruling 5). This repo's tooling: no RESYNC
   entry.
7. **`project-trajectory/prompts/reviewer.template.md`** (shipped, RESYNC
   entry):
   - severity tied to reachability (item 4): a BLOCKER or MAJOR states a
     scenario reachable in normal use, or a fail-open, data-loss or security
     path; a rare or contrived edge is at most MINOR;
   - item 1's classification clause: an input outside the spec's declared
     set that the change fails closed on is a coverage-extension note; one it
     fails open on stays a finding; the reviewer decides which;
   - the convergence stance, for a round whose brief says so: confirm each
     fix through its regression test failing on the pre-fix code, or through
     its independently checkable evidence; check the Done-when's coverage and
     look for regressions; a new finding blocks only if it is fail-open, data
     loss or a Done-when gap, and anything else is marked for a successor
     row. How the coordinator marks a round as convergence is stated in the
     skill's recipes.

## Done-when

- Every deliverable above is in its target, each citing the ruling it
  carries, and the `coordinator-cycle` skill no longer describes narrow
  rounds or a single reviewer.
- The skill copy in `.claude/skills/` matches the kit source
  (`bootstrap.py --dest . --sync`).
- `review_brief.py critique` names the registries, with a test that fails on
  the code before the change; the change's trace rows are authored and sat at
  the lane's checkpoint.
- `RESYNC_PACK.md` carries one entry for the shipped changes (PROCESS.md §3,
  `spine-questions.md`, `reviewer.template.md`, `review_brief.py`), with no
  forced migration.
- The bar is green on the landing tip: the smoke tier within its budget,
  `check_trajectory.py --strict` clean, and `trace.py --strict` with no
  finding beyond LLR-292's (B2 fixes that one).

## Scope answers

- **S1:** one deliverable set, kept together: every item is text the next
  lane's cycle reads, plus the one render change the rubric's artifact line
  needs, and none is useful landed without the others. The verdict/act split
  is independently landable and is WI-912 (needs this row).
- **S2:** no file gains authority over a hold, an act or a gate. The skill and
  rubric text govern the coordinator's own procedure; the critique brief only
  names files for the critic to read. No Trust section.
- **S3:** no promise over an input space. The rubric's anchors are a closed
  list, and the critique brief's registry list is a fixed, named set.
- **S4:** `none` proposed: one script family (`review_brief.py`'s critique
  brief, a change a cheap test specifies), no Trust section, no input-space
  promise; the rest is text.
- **Architectural delta:** none. No state, domain value, input dependency or
  boundary is added; the critique brief gains read-only inputs it already
  has access to.
- **Dependencies:** no row; no third-party dependency. It lands first in the
  batch: every later row's critique and review runs under it.
