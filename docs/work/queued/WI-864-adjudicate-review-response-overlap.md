+++
id = "WI-864"
title = "adjudicate review-response overlap [af015cc7e32a]: WI-805;WI-811;WI-847;WI-848;WI-852;WI-853;WI-854;WI-860"
workstream = "process"
specref = "docs/log.d/2026-10-08-owner-ruling-review-threat-model.md"
buildtier = "strong"
priority = 9
safety_class = "adjudication"
brief = "consolidate"
adjudicates = ["WI-805", "WI-811", "WI-847", "WI-848", "WI-852", "WI-853", "WI-854", "WI-860"]
digests = "af015cc7e32a|a4596ff3f7d5"
+++

## Context

Minted BY HAND by the coordinator on 2026-10-08 at the owner's direction, as a consolidation sitting over the queued rows that shape how a review's findings are produced, routed and answered: WI-805, WI-811, WI-847, WI-848, WI-852, WI-853, WI-854 and WI-860. The owner asked whether these rows guard against the same thing from several directions, after a lane drew six review rounds and the owner ruled the review threat model (docs/log.d/2026-10-08-owner-ruling-review-threat-model.md). WI-861 was already folded into WI-811 by the owner's direction (87f718f9). The census over the whole queue would have re-judged the 29 rows WI-855 judged on 2026-10-08 and would have left out WI-860, which touches no code; the cluster is therefore chosen, not derived, and the judge rules on these rows only.

The mechanical pre-filter's hints for this cluster (a hint, not a finding; two rows cut from one plan share its path and always will):

> WI-805 and WI-811 are both open and both answer SR-154
> WI-805 and WI-811 both touch agent_brief.py;agent_loop.py;agent_route.py;done_when.py;intake.py;integrate.py;score_reviews.py;verdict.py
> WI-805 and WI-847 both touch agent_loop.py
> WI-805 and WI-852 are both open and both answer SR-154
> WI-805 and WI-852 both touch agent_brief.py;agent_loop.py;agent_route.py;done_when.py;intake.py;integrate.py;score_reviews.py;verdict.py
> WI-805 and WI-853 both touch agent_loop.py;agent_route.py;plan_coverage.py
> WI-811 and WI-847 both touch agent_loop.py
> WI-811 and WI-852 are both open and both answer SR-154
> WI-811 and WI-852 both touch agent_brief.py;agent_loop.py;agent_route.py;done_when.py;intake.py;integrate.py;score_reviews.py;verdict.py
> WI-811 and WI-853 both touch agent_loop.py;agent_route.py
> WI-847 and WI-852 both touch adjudicate_brief.py;agent_loop.py;prompts.py
> WI-847 and WI-853 both touch agent_loop.py
> WI-847 and WI-854 both touch adjudicate_brief.py;prompts.py
> WI-848 and WI-852 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-848 and WI-852 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-848 and WI-853 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-848 and WI-853 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-848 and WI-854 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-848 and WI-854 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-852 and WI-853 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-852 and WI-853 both touch agent_loop.py;agent_route.py
> WI-852 and WI-853 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-852 and WI-854 are both open and both answer SR-146
> WI-852 and WI-854 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-852 and WI-854 both touch adjudicate_brief.py;agent_session.py;baseline_snapshot.py;gen_prompt_catalog.py;prompts.py;trace.py
> WI-852 and WI-854 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-853 and WI-854 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-853 and WI-854 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
