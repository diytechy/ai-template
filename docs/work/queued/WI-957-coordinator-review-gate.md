+++
id = "WI-957"
title = "The coordinator's review brief is rendered only for a tip whose review bar is attested green for the tests the brief names"
workstream = "process"
sr_refs = ["SR-235", "SR-146"]
specref = "docs/plans/2026-10-11-review-churn/README.md#13-review-only-a-green-tip-review-test-cases-in-stages"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = ["WI-956", "~WI-955"]
+++

## Context

Review-churn item 13: "Review, only on a green record for the tip. The
coordinator and the loop both refuse to dispatch reviewers without it." This
row is the coordinator's half; WI-958 is the loop's.

Today the coordinator's only check before a review is that the commit landed
(`coordinator-cycle` SKILL §3, Iterate step 1: "`git log -1` moved"). A red
smoke has been committed through a chain that checked only an exit code
(recipes §6). Every coordinator round renders through one route,
`review_brief.py review` (`_cmd_review` -> `render_review`; grep finds no
other caller): counted rounds, convergence rounds, the gate over the
checkpoint tip, a round after a dispute sitting's FIX and a round over a
rebase. So one refusal there covers all of them.

**Without P8**, the brief's `--tests` list is the lane's named set, and the
attestation's `tests=` digest must match it. P8 later derives the set.

**Between this row and WI-958** the coordinator has the gate but no stated
red-round cap; a red tip goes back to the builder as today (recipes §1).

**Anchor.** SN-004 and SN-008 (approved). SR-235 (the attended launcher's
review record) is the existing row nearest the obligation. A derived SR, "a
review starts only on a tree whose review bar is attested green", with its
coordinator LLR and TCs, is drafted TC-first in the lane; WI-958 adds the
loop's LLR under the same SR.

## Deliverables

1. **The refusal.** `review_brief.py review` verifies, through WI-956's one
   verifier, that the reviewed commit carries a `bar=review` attestation
   whose tests digest equals the digest of its `--tests`. It looks at the
   reviewed commit and through the commits beneath it whose non-record
   identity equals their parent's (the step `governing_rev` already
   defines), so a round-file or telemetry commit on top does not force a
   re-bar. Otherwise it writes no brief and exits nonzero, naming the
   reviewed sha, what it found and the `integrate.py attest` command.
2. **The cycle text.** SKILL §3 Iterate step 1 becomes "the tip carries the
   review bar's attestation", and the commit step uses `integrate.py
   attest` in place of "run the commit bar, then commit" (recipes §1 and
   §6). Both skill copies stay byte-identical.
3. **Records.** IF-288's contract body (the `review` verb) states the
   refusal. No RESYNC entry is owed if `review_brief.py`'s shipped CLI
   change is covered by WI-956's entry; otherwise one entry.

## Trust

This row consumes WI-956's attestation; its Trust section holds the
producer and the full consumer list. This row's ruling, at its one consumer:

- **Absent, unreadable, malformed, unverified**: no brief, nonzero exit,
  the cause named. Never rendered with a warning.
- **Verified for another bar** (`landing`, `no-bar`) **or another test
  set**: refused, naming both digests.
- The render never runs the bar itself.
- **The bound** (PROCESS.md §6, "Review threat model"): the promise covers
  the tips and test lists the kit's own routes produce (`integrate.py
  attest`, the refresh, the record commits the cycle makes above an
  attested tip). A hand-edited trailer, a hand-chosen alias for a test
  path and sub-second timing windows are outside it.

## Done-when

Each named test fails on the code before the change.
- `review_brief.py review` writes no brief and exits nonzero for: a tip
  with no attestation; a trailer naming another tree; a `landing`
  attestation; a `review` attestation whose tests digest differs from
  `--tests`. Each message names the cause and the `attest` command.
- It renders for a tip carrying a matching `review` attestation, and for a
  tip whose only commits above the attested one change record paths.
- It refuses when a commit above the attested one changes non-record paths.
- The skill and recipes carry the new step 1 and the `attest` commit step;
  no text keeps "`git log -1` moved" as the pre-review check.
- On the landing tip, the commit bar is green, `check_trajectory.py
  --strict` and `trace.py --strict` clean; the derived SR, LLR and TCs are
  judged at the lane's sitting.

## Scope answers

- **S1.** One deliverable. Third of P1's four rows. The loop's gate and the
  red-round cap are WI-958, split off because the loop is paused and its
  scheduling is a separate surface.
- **S2.** A consumer of WI-956's trailer; the ruling is above.
- **S3.** Closed: verified `review` attestation with the matching digest,
  or refusal.
- **S4.** `single`: it promises refusal over the attestation's input space.
- **S5.** A new input to the review render. No new state or component.
- **S6.** `WI-956` (hard): the verifier and producer. `~WI-955`: the same
  §3 text.
- **B3.** Trusts the record; never re-runs the bar.
- **B4.** No owner act.
- **Machinery landing alone.** From its landing, every coordinator review
  render refuses an unattested tip, this lane's own rounds included
  (rendered from the lane's copy). The `attest` recipe lands in the same
  commit as the refusal. If the lane's gate is wrong, the defect is fixed
  forward in the lane with a regression test (revision 37); no review
  renders through another copy of the script to step around it.

## Critique dispositions

Scope critique round 1 (Codex Sol, medium, 2026-10-20; CHANGES-REQUESTED,
findings=2):

- **MAJOR, S2/S3 (rendering from trunk's copy bypasses the gate):
  adopted by removing the route.** "Machinery landing alone" now reads "the
  defect is fixed forward in the lane with a regression test (revision 37);
  no review renders through another copy of the script to step around it".
  Removing the authority is preferred over guarding it (recipes §1).
- **MINOR, S3 (the consumer's input bound): adopted.** The Trust section
  gains "The bound", in PROCESS.md §6's terms.
