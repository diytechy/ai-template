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
