+++
id = "WI-579"
title = "The verdict carrier and the adjudication_review dial: gate over logged rounds, tree-bound trailer, generated rollup"
workstream = "process"
specref = ""
buildtier = "strong"
priority = 9
safety_class = "ordinary"
supersedes = "WI-558;WI-559;WI-560"
+++

## Deliverable

The merge gate reads the EVIDENCE and the evidence names the tree it judged.

`kitlib/verdict.py` (LLR-207, IF-175) is the verdict record's one home: the
non-record tree identity — a SHA-256 fold of `git ls-tree -r -z` with
`docs/reviews/`, `docs/log.d/` and `docs/iteration/` dropped — the
`Review-Verdict: APPROVE|CHANGES-REQUESTED rounds=<N> tree=<64 hex>` trailer
grammar, the round-file / session-log join, and the branch-scoped readers. Two
callers stand on it and that is the point: `integrate._verdict_gate` (may this
merge?) and `agent_loop.review_owed_by_evidence` (does this lane still owe a
round?) asked one question with two rules over two exclusion sets, and the gap
between them drew two identical rounds on WI-547.

- **WI-558 DW1** — the gate computes over the branch's own round files,
  restricted to rounds a LOGGED reviewer session produced: a file under
  `docs/reviews/` is a round only when the coordinator's own committed session
  log for that (train, ordinal) declares a REVIEW phase. Finding K closed —
  an implementer cannot author its own approval without also forging the loop's
  telemetry.
- **WI-558 DW2** — the machine half rides the round's own record commit as a
  trailer, written by the COORDINATOR and verified against its carrier's tree
  (the `Bar-Green` pattern). GOVERNING = TREE IDENTITY: a verdict counts only
  while it names the branch's current non-record tree, read at the WORK TIP so
  the station refresh still does not stale an honest APPROVE. The freshness
  comparison is gone; there is no ordering rule left. The trailer is a
  CROSS-CHECK and never an accept path — one that contradicts the rounds
  refuses the merge.
- **WI-558 DW3** — `gen_verdict_rollup.py` (LLR-208) rebirths the rollup as a
  GENERATED artifact: `docs/stack.ini [generated]`, `trunk_step.py --regen`, a
  `check.py verdict-rollup` freshness step on the hook floor and in
  `_TRUNK_FRESHNESS_STEPS`, and `--check` with two answers. The gate never reads
  it, and the file says so where a human will see it.
- **WI-558 DW4** — the migration window: the gate accepts EITHER the round
  evidence or a legacy hand-authored rollup, judged by the SAME identity rule,
  warning on stderr whenever the legacy path is what cleared it. Two
  `RESYNC_PACK.md` entries. The trailer is additive and costs an adopter nothing.
- **WI-558 DW5 / WI-560 DW4 / WI-559 DW3** — `tests/test_verdict_record.py`
  drives each half beside its opposite (TC-205, TC-206).
- **WI-560 DW1** — ONE definition of "the last commit that could invalidate a
  verdict", used by the merge slot AND the C2 review-owed derivation. That
  definition names a REV as well as a path set, so the station-refresh peel
  (`refresh_attestation` / `work_tip`) lives beside the fold and both readers
  call `governing_identity` rather than each choosing where to measure. The
  double-identical-round class is now unrepresentable, not policed: the commits
  that caused it cannot move the identity either reader compares.
- **WI-559 DW2** — a committing ADJUDICATE session schedules its round exactly
  as a committing BUILD does, under the dial; the phase stays in
  `NON_BUILD_PHASES` because a judgement is not a build. No exit banner claims a
  round that was never drawn — it counts them.
- **The dial** — `docs/process.toml [attestation] adjudication_review`
  (`never` / `when-minting` / `always`; template and this repo ship
  `when-minting`), read through `agent_common.adjudication_review_owed` by BOTH
  the scheduler and the gate, with a closed vocabulary refused at preflight and
  a conservative fallback. Its `docs/enforcement-audit.md` row and the
  `RESYNC_PACK.md` entry ship with it. An adjudication lane drafting ordinary
  successors now merges with NO verdict artifact present anywhere — the OI-76
  acceptance becomes measurable on the next unattended run.

Review A rework closed both evidence-boundary gaps. The loop's resume reader now
uses the same branch-scoped committed-path, logged-session and tree-bound entry
pipeline as the merge gate, so an approval-shaped file produced by a BUILD
session cannot suppress the round the gate requires. The trailer's `rounds=N`
field is now defined and checked as the completed review cycles represented at
the governing tree (a dual-review cycle counts once, and rework starts the
tree-scoped count over); both the coordinator writer and gate derive that value
from the shared evidence. LLR-207's rationale now carries only the standing
technical reason, without the decision's provenance narrative.

Review A round 007 closed four more, three of them one shape — a rule expressed
as a value something else got to choose. The identity's REV is now part of the
shared definition (the peel moved into `kitlib/verdict.py`, so a station refresh
no longer makes the two readers disagree); `branch_trailers` returns the ordered
SEQUENCE of attestations per tree, so the newest-first `git log` can no longer
hand a reader a superseded stamp and have the cross-check accuse an approved
lane of forgery; and `tree_identity` passes `-z` while `fold_listing` takes
decoded entries, so a quoted non-ASCII path can no longer fold a record file
into the identity. The DONE banner states rounds DRAWN this run and the latest
verdict, because the tally it reads holds every completed round whatever its
outcome.

`LLR-140`'s Approved detail cell was re-pointed IN-LANE: it asserted the retired
time comparison, which nothing detects once it is false. Ratchet bumps
(`agent_common` 1272→1305, `agent_loop` 2519→2578, `integrate` 1298→1382 and
then DOWN to 1352 when the peel left it, `check` 1163→1177, `bootstrap`
1658→1660, smoke membership 1480→1560) each carry
their reason at the entry; `_verdict_gate`'s complexity bump was REFUSED and the
function decomposed instead. Round-007 rework full suite, run at `025a0643`:
3342 passed, 24 skipped, 1 failed in 614.49s — the failure is `docs/stage`
freshness, a trunk-lane artifact a work branch must
not commit, bisected clean at the integration base. Account, deviations and the
one out-of-scope finding: `docs/log.d/WI-579-verdict-carrier-and-adjudication-review.md`.

## Context

Minted by the owner-directed backlog restructure of 2026-09-02 (plan of record `docs/plans/2026-09-02-backlog-restructure-and-consolidation.md` §2.2; executed out of band as a hand trunk commit series, not by a lane). The absorbed rows are archived under `docs/archive/work/restructured/` with their scope text untouched; their Done-when blocks are QUOTED below under their old ids and remain the spec this row must satisfy — decompose, don't paraphrase.

**Why one row.** WI-558 Done-when 2 retires the gate's freshness comparison in
favour of tree identity; WI-560 Done-when 1 builds one shared freshness
definition for the gate and the C2 review-owed derivation; WI-559 Done-when 2
makes an ADJUDICATE commit schedule a round, which only means something once
the round carrier WI-558 defines exists. Built apart in any order, the later
lane undoes part of the earlier one. Together: the gate and the review-owed
derivation read the SAME tree-identity trailer, and the round an adjudication
owes is drawn under the policy below.

**Adjudication review policy (plan §3, owner direction 2026-09-02).** The
adjudicator is already the cross-family judge by routing (`agent_loop`'s
ADJUDICATE arm excludes the builder's family). A round over every adjudication
is a fresh session with less context judging the one session that held the
whole chain, and today it is also the supervisor stop on every unattended run
(`integrate._verdict_gate` demands a REVIEW-A from a lane whose phase is in
`NON_BUILD_PHASES`, so nothing produces one). This row adds
`docs/process.toml [attestation] adjudication_review = "never" | "when-minting" | "always"`
(template ships `"when-minting"`, this repo sets `"when-minting"`):
- `never` — no round after ADJUDICATE; the gate never asks an adjudication
  lane for a verdict.
- `when-minting` — a round is scheduled, and the gate demands its verdict,
  when the merged adjudication's `## Dispositions` drafts ANY successor whose
  `safety_class` is `spine` or `high-risk`, or when its `brief` is
  `consolidate`. An amendment verdict that only recommends a flip, a red-tc
  that drafts ordinary fix rows, a clean-close spot check: no round.
- `always` — the intended-but-broken behaviour today, made real.
One reader function in `agent_common` (`adjudication_review_owed(docs, brief,
drafts)`) serves BOTH the round scheduler (ADJUDICATE leaves the unconditional
`NON_BUILD_PHASES` set; the dial decides) and `_verdict_gate` (which consults
the existing `integrate._adjudication_lane` plus the dial plus the merged
spec's drafts), so the two cannot disagree. Tests pin all three values on a
scaffold and pin that `never`/`when-minting` with ordinary drafts lets an
adjudication lane merge with NO REVIEW-A file present.

## Done-when

1. Every WI-558 Done-when item below, as written.
2. WI-560 Done-when 1 below, satisfied by the SAME trailer/tree-identity rule
   the gate uses (one definition, two readers).
3. WI-559 Done-when 2 below, under the `adjudication_review` dial.
4. The dial, its template row, `docs/enforcement-audit.md` row, and the
   `RESYNC_PACK.md` entry.
5. Full suite green; the OI-76 acceptance (three consecutive rows merged by
   one launch with zero supervisor commits) is measurable on the next
   unattended run.

### From WI-558 (Done-when, verbatim)

1. `integrate._verdict_gate` computes its predicate over the branch train's
   round files, restricted to rounds a LOGGED reviewer session produced (the
   telemetry commit is the anchor) — an implementer-authored file in the
   review path is not a round (the plan's finding K closed).
2. The round's own commit carries the machine half as a trailer —
   `Review-Verdict: APPROVE|CHANGES-REQUESTED rounds=N tree=<sha>` — the
   existing `Bar-Green` pattern. GOVERNING = TREE IDENTITY as ruled: a
   verdict counts only if it names the branch's current non-record tree; no
   ordering rule; the gate's freshness comparison retires.
3. The per-WI rollup becomes a GENERATED artifact: a regenerator compiles it
   from the round files, `--check` keeps it fresh, it is declared in
   `docs/stack.ini [generated]`, and the gate never reads it. The supervisor
   prompt's hand-compile instruction retires in the same change.
4. Migration window per the plan's section 6: during the window the gate
   accepts EITHER the round-file evidence or a legacy hand-authored rollup,
   warning on the legacy path; `RESYNC_PACK.md` carries the entry. The
   trailer is additive and costs an adopter nothing until their loop writes
   one.
5. Tests drive the gate's new predicate, the trailer identity rule, the
   logged-session restriction, and the migration warn on a scaffold; the
   full suite stays green.

### From WI-560 (Done-when 1 and 4, verbatim — 2 went to WI-580, 3 to WI-581; item 4 is shared)

1. ONE shared definition of "the last commit that could invalidate a
   verdict" (excluding `docs/reviews`, `docs/log.d`, `docs/iteration`) is
   used by both the merge slot and the C2 review-owed derivation; the
   double-identical-round class becomes unrepresentable on a scaffold.
4. Tests drive all three.

### From WI-559 (Done-when 2 and 3, verbatim — Done-when 1 went to WI-580; item 3 is shared with it)

2. A committing ADJUDICATE session schedules its review round exactly as a
   committing BUILD does, and no exit banner claims a round that was never
   drawn.
3. Tests drive the false-partial class (built-and-verified lane, long
   suite) and the adjudicate round scheduling on a scaffold.
