+++
id = "WI-667"
title = "Decide how a red assumption-evidence test case reaches the dispatch census, once the red-TC rung is re-armed"
workstream = "unattended"
specref = "project-trajectory/scripts/census.py"
sr_refs = ["SR-197"]
needs = ["WI-631"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

WI-631 built `census.red_tc_census(..., assumptions=True)`, which counts
assumption-evidence test cases apart from requirement evidence (LLR-231), and
deliberately left it off the dispatch seam: `gap_census` and the intake mint
read only the requirement half, and the docstrings say so. The codex review
wanted it wired; the arbiter ruled wiring now would invent policy no row
states (whether a red premise mints an ordinary gap row or an adjudication
row, and with which brief), and noted the decisive fact: the red-TC rung is
structurally dead in any conformant repository today, because
`_TC_NOT_RED` spans the whole closed Status vocabulary, and re-arming it is
an owner judgement item.

IN SCOPE, once the rung's re-arming is ruled: decide the routing (the row
kind, its brief, and when a red assumption case counts as red: every
requirement citing its assumptions claimed built), draft the requirement or
design row that states it, and wire the assumption half into `gap_census`
and `intake._census_drafts` under that row.

Noted 2026-09-27 (the WI-689 consolidation verdict, `docs/reviews/wi-689-adjudicate-queue-overlap-af58/001-ADJUDICATE-e26e22a.md`, confirmed by Codex Sol): this row's scope is gated on an owner ruling that re-arms the red-TC rung, but no `needs` target or open item carries that gate, so the row reads claimable while it cannot be built. When the ruling's row is filed, add it to `needs`.

Folded 2026-09-28 (the fifth coordinator session), on the same surface, how an assumption-evidence case reaches the adjudication machinery: an assumption-only test case (one that verifies a DA and no SR or LLR, like TC-279 for DA-011) is invisible to two of the kit's own briefs. The first-approval composer renders chains by SR, so it never showed TC-279: spine-acts batch C approved WI-696 with TC-279 unjudged in its scope. The re-judge composer refuses outright ("TC-279 has no `Verifies` cell"), so WI-697 (TC-279's re-judge) is held. Both composers need an arm for an assumption-only case, rendered under its assumption's chain as the assumptions approval brief already does.

## Done-when

- An assumption-only test case (verifying a DA and no SR or LLR) is rendered by both the first-approval and the re-judge briefs under its assumption's chain, with a test for each; WI-697's brief then composes.
- A row states how a red assumption-evidence case is routed, and it is
  approved through the normal route.
- `gap_census` carries the assumption half under its own prefix, and a test
  shows a red assumption case minting the ruled row kind while the
  requirement half's output is unchanged.
- The commit bar passes.

## Owner position 2026-09-30 (open; not yet a ruling)

See WI-697: the owner doubts an assumption is verified rather than asserted
(Status carries it). That bears on the first Done-when (composer arm for an
assumption-only case) and on whether a "red assumption case" exists at all.
Resolve it before building either.

Reference for the ruling (2026-10-02): the spine's `Status` vocabulary is
closed, `Drafted`, `Approved`, `Founded` (PROCESS.md §4). `Approved` blesses the
row's text; `Founded` is computed (the artifacts the row calls for exist), never
typed. An assumption row already carries `status` (Drafted/Approved) and a
separate `standing` (`active` | `falsified`). The owner's position (no evidence
for an assumption, only a status) would mean: drop `assumption_refs` on test
cases, and let a falsified `standing`, set by a person, be the only signal.

## Proposed ruling 2026-10-02 (for the owner's signature; not yet a ruling)

Basis: `docs/plans/2026-09-20-validation-gap-and-the-assumption-tier.md` §5 (status
and standing are separate) and §7 ("a passed sparse probe is not evidence that an
assumption holds; only a failed one is evidence that it does not").

1. An assumption carries `status` (Drafted | Approved) and `standing` (active |
   falsified), plus its `falsifier`. It has no evidence level and no positive
   evidence: drop the `assumed | specified | monitored | sampled` ladder and any
   rule that the gate needs current evidence for an assumption.
2. The only evidence-shaped signal is falsification: a failing observation
   (`record_observation.py --outcome fail`) or an adjudication/outcome review
   finding. A person or an adjudication then sets `standing = falsified`; the
   `accepted_risk` reopen triggers stay.
3. So no "red assumption case" exists to route: the census's assumption half
   (WI-631's `assumptions=True`) and this row's second and third Done-when lines
   are dropped, not built. The first Done-when line stays, narrowed: the first-approval
   and re-judge briefs render an assumption-only observation case (TC-279) under its
   assumption's chain, because it verifies no SR or LLR.
4. Cost to check before signing: SN-043's text ("premises ... are recorded and
   checked") and the plan's C3 (`assumption_refs`, per-observation results) and C5
   (gate) were built or designed for the evidence model; C3 shrinks to the
   falsification route and C5 loses its evidence arm. File the amendments through
   the artifact adjudication route when ruled.
