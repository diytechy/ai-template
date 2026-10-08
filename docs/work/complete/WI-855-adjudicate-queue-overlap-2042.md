+++
id = "WI-855"
title = "adjudicate queue overlap [20424540cd76]: WI-798;WI-799;WI-800;WI-801;WI-802;WI-804;WI-805;WI-807;WI-808;WI-809;WI-810;WI-811;WI-813;WI-816;WI-817;WI-827;WI-828;WI-832;WI-833;WI-834;WI-846;WI-847;WI-848;WI-849;WI-850;WI-851;WI-852;WI-853;WI-854"
workstream = "process"
specref = ""
buildtier = "strong"
priority = 9
safety_class = "adjudication"
brief = "consolidate"
adjudicates = ["WI-798", "WI-799", "WI-800", "WI-801", "WI-802", "WI-804", "WI-805", "WI-807", "WI-808", "WI-809", "WI-810", "WI-811", "WI-813", "WI-816", "WI-817", "WI-827", "WI-828", "WI-832", "WI-833", "WI-834", "WI-846", "WI-847", "WI-848", "WI-849", "WI-850", "WI-851", "WI-852", "WI-853", "WI-854"]
digests = "83a94fde0f88|1237285c1cff"
+++

## Deliverable

Adjudication verdict recorded on the lane; this row is closed MECHANICALLY at its DONE (OI-70/OI-73). Its `## Dispositions` successors mint at this row's own merge (drafts-not-mints), the mint replaces the superseded row's inbound hard edges, and any human-owed answer becomes a `pending` open item the successor depends on. The verdict artifact is under `docs/reviews/`.

## Context

Minted by the CONSOLIDATION CENSUS (the 2026-09-02 backlog-restructure plan §1.3), which runs from an idle station with no judgement in progress and none queued over these rows or ahead of this one. The candidate cluster is 29 queued row(s): WI-798;WI-799;WI-800;WI-801;WI-802;WI-804;WI-805;WI-807;WI-808;WI-809;WI-810;WI-811;WI-813;WI-816;WI-817;WI-827;WI-828;WI-832;WI-833;WI-834;WI-846;WI-847;WI-848;WI-849;WI-850;WI-851;WI-852;WI-853;WI-854.

The mechanical pre-filter selected them; it has concluded NOTHING. Each line below is a hint a string comparison can produce, and two rows deliberately cut from one plan share its path and always will:

> WI-798 and WI-799 both touch agent_loop.py
> WI-798 and WI-800 are both open and both answer SR-222
> WI-798 and WI-800 both touch agent_loop.py;plan_runner.py;session_adapters.py;session_service.py
> WI-798 and WI-801 are both open and both answer SR-222
> WI-798 and WI-801 both touch agent_loop.py;plan_runner.py;session_adapters.py;session_service.py
> WI-798 and WI-802 both touch agent_loop.py;session_adapters.py;session_service.py
> WI-798 and WI-804 are both open and both answer SR-222
> WI-798 and WI-804 both touch agent_loop.py;plan_runner.py;session_adapters.py;session_service.py
> WI-798 and WI-805 both touch agent_loop.py
> WI-798 and WI-811 both touch agent_loop.py
> WI-798 and WI-813 both touch agent_loop.py;plan_runner.py
> WI-798 and WI-834 both touch agent_loop.py;session_adapters.py;session_service.py
> WI-798 and WI-846 both touch agent_loop.py;session_adapters.py;session_service.py
> WI-798 and WI-847 both touch agent_loop.py;session_adapters.py;session_service.py
> WI-798 and WI-849 both touch agent_loop.py
> WI-798 and WI-852 both touch agent_loop.py
> WI-798 and WI-853 both touch agent_loop.py;plan_runner.py
> WI-799 and WI-800 both touch adjudicate_brief.py;agent_loop.py
> WI-799 and WI-801 both touch agent_brief.py;agent_loop.py;done_when.py;intake.py;integrate.py;verdict.py
> WI-799 and WI-802 both touch adjudicate_brief.py;agent_loop.py
> WI-799 and WI-804 both touch agent_loop.py
> WI-799 and WI-805 both touch agent_brief.py;agent_loop.py;done_when.py;intake.py;integrate.py;verdict.py
> WI-799 and WI-807 both touch lane_state.py
> WI-799 and WI-808 both touch integrate.py
> WI-799 and WI-809 both touch adjudicate_brief.py;intake.py;verdict.py
> WI-799 and WI-810 both touch adjudicate_brief.py;intake.py
> WI-799 and WI-811 both touch agent_brief.py;agent_loop.py;done_when.py;intake.py;integrate.py;verdict.py
> WI-799 and WI-813 both touch agent_loop.py
> WI-799 and WI-816 both touch agent_common.py;intake.py;integrate.py
> WI-799 and WI-828 both touch integrate.py
> WI-799 and WI-833 both touch integrate.py
> WI-799 and WI-834 both touch adjudicate_brief.py;agent_loop.py;integrate.py
> WI-799 and WI-846 both touch adjudicate_brief.py;agent_loop.py
> WI-799 and WI-847 both touch adjudicate_brief.py;agent_loop.py
> WI-799 and WI-849 are both open and both answer SR-156
> WI-799 and WI-849 both touch adjudicate_brief.py;agent_brief.py;agent_common.py;agent_loop.py;bookkeeping.py;done_when.py;intake.py;integrate.py;lane.py;spec_move.py;verdict.py
> WI-799 and WI-850 both touch adjudicate_brief.py;verdict.py
> WI-799 and WI-851 both touch adjudicate_brief.py;agent_common.py;bookkeeping.py;handback.py;intake.py;integrate.py;verdict.py
> WI-799 and WI-852 both touch adjudicate_brief.py;agent_brief.py;agent_loop.py;done_when.py;intake.py;integrate.py;verdict.py
> WI-799 and WI-853 both touch agent_loop.py
> WI-799 and WI-854 both touch adjudicate_brief.py
> WI-800 and WI-801 are both open and both answer SR-222
> WI-800 and WI-801 both touch agent_loop.py;coordinator_adjudicate.py;plan_runner.py;session_adapters.py;session_service.py
> WI-800 and WI-802 are both open and both answer SR-227
> WI-800 and WI-802 both touch adjudicate_brief.py;agent_loop.py;coordinator_adjudicate.py;dispatch.py;session_adapters.py;session_keep.py;session_service.py
> WI-800 and WI-804 are both open and both answer SR-222
> WI-800 and WI-804 both touch agent_loop.py;plan_runner.py;session_adapters.py;session_service.py
> WI-800 and WI-805 both touch agent_loop.py
> WI-800 and WI-807 were commissioned by the same OI-109
> WI-800 and WI-809 both touch adjudicate_brief.py
> WI-800 and WI-810 both touch adjudicate_brief.py
> WI-800 and WI-811 both touch agent_loop.py
> WI-800 and WI-813 both touch agent_loop.py;plan_runner.py
> WI-800 and WI-834 are both open and both answer SR-227
> WI-800 and WI-834 both touch adjudicate_brief.py;agent_loop.py;coordinator_adjudicate.py;dispatch.py;session_adapters.py;session_keep.py;session_service.py
> WI-800 and WI-846 are both open and both answer SR-227
> WI-800 and WI-846 both touch adjudicate_brief.py;agent_loop.py;coordinator_adjudicate.py;dispatch.py;session_adapters.py;session_keep.py;session_service.py
> WI-800 and WI-847 are both open and both answer SR-227
> WI-800 and WI-847 both touch adjudicate_brief.py;agent_loop.py;coordinator_adjudicate.py;dispatch.py;session_adapters.py;session_keep.py;session_service.py
> WI-800 and WI-849 both touch adjudicate_brief.py;agent_loop.py
> WI-800 and WI-850 both touch adjudicate_brief.py
> WI-800 and WI-851 both touch adjudicate_brief.py
> WI-800 and WI-852 both touch adjudicate_brief.py;agent_loop.py
> WI-800 and WI-853 both touch agent_loop.py;plan_runner.py
> WI-800 and WI-854 both touch adjudicate_brief.py
> WI-801 and WI-802 both touch agent_loop.py;coordinator_adjudicate.py;session_adapters.py;session_service.py
> WI-801 and WI-804 are both open and both answer SR-222
> WI-801 and WI-804 both touch agent_loop.py;agent_route.py;plan_runner.py;session_adapters.py;session_service.py
> WI-801 and WI-805 are both open and both answer SR-154
> WI-801 and WI-805 both touch agent_brief.py;agent_loop.py;agent_route.py;done_when.py;intake.py;integrate.py;score_reviews.py;verdict.py
> WI-801 and WI-808 both touch integrate.py
> WI-801 and WI-809 both touch intake.py;verdict.py
> WI-801 and WI-810 both touch intake.py
> WI-801 and WI-811 are both open and both answer SR-154
> WI-801 and WI-811 both touch agent_brief.py;agent_loop.py;agent_route.py;done_when.py;intake.py;integrate.py;score_reviews.py;verdict.py
> WI-801 and WI-813 both touch agent_loop.py;agent_route.py;plan_runner.py
> WI-801 and WI-816 both touch intake.py;integrate.py
> WI-801 and WI-828 both touch integrate.py
> WI-801 and WI-833 both touch integrate.py
> WI-801 and WI-834 both touch agent_loop.py;coordinator_adjudicate.py;integrate.py;session_adapters.py;session_service.py
> WI-801 and WI-846 both touch agent_loop.py;coordinator_adjudicate.py;session_adapters.py;session_service.py
> WI-801 and WI-847 both touch agent_loop.py;coordinator_adjudicate.py;session_adapters.py;session_service.py
> WI-801 and WI-849 both touch agent_brief.py;agent_loop.py;done_when.py;intake.py;integrate.py;verdict.py
> WI-801 and WI-850 both touch verdict.py
> WI-801 and WI-851 both touch intake.py;integrate.py;verdict.py
> WI-801 and WI-852 are both open and both answer SR-154
> WI-801 and WI-852 both touch agent_brief.py;agent_loop.py;agent_route.py;ask.py;done_when.py;intake.py;integrate.py;score_reviews.py;verdict.py
> WI-801 and WI-853 both touch agent_loop.py;agent_route.py;plan_runner.py
> WI-802 and WI-804 both touch agent_loop.py;session_adapters.py;session_service.py
> WI-802 and WI-805 both touch agent_loop.py
> WI-802 and WI-809 both touch adjudicate_brief.py
> WI-802 and WI-810 both touch adjudicate_brief.py
> WI-802 and WI-811 both touch agent_loop.py
> WI-802 and WI-813 both touch agent_loop.py
> WI-802 and WI-834 are both open and both answer SR-227
> WI-802 and WI-834 both touch adjudicate_brief.py;agent_loop.py;coordinator_adjudicate.py;dispatch.py;session_adapters.py;session_keep.py;session_service.py
> WI-802 and WI-846 are both open and both answer SR-227
> WI-802 and WI-846 both touch adjudicate_brief.py;agent_loop.py;coordinator_adjudicate.py;dispatch.py;session_adapters.py;session_keep.py;session_service.py
> WI-802 and WI-847 are both open and both answer SR-227
> WI-802 and WI-847 both touch adjudicate_brief.py;agent_loop.py;coordinator_adjudicate.py;dispatch.py;session_adapters.py;session_keep.py;session_service.py
> WI-802 and WI-849 both touch adjudicate_brief.py;agent_loop.py
> WI-802 and WI-850 both touch adjudicate_brief.py
> WI-802 and WI-851 both touch adjudicate_brief.py
> WI-802 and WI-852 both touch adjudicate_brief.py;agent_loop.py
> WI-802 and WI-853 both touch agent_loop.py
> WI-802 and WI-854 both touch adjudicate_brief.py
> WI-804 and WI-805 both touch agent_loop.py;agent_route.py;plan_coverage.py
> WI-804 and WI-811 both touch agent_loop.py;agent_route.py
> WI-804 and WI-813 are both open and both answer SR-155
> WI-804 and WI-813 both touch agent_loop.py;agent_route.py;hats.py;plan_artifacts.py;plan_briefs.py;plan_coverage.py;plan_coverage_step.py;plan_round.py;plan_runner.py;schedule.py
> WI-804 and WI-834 both touch agent_loop.py;session_adapters.py;session_service.py
> WI-804 and WI-846 both touch agent_loop.py;session_adapters.py;session_service.py
> WI-804 and WI-847 both touch agent_loop.py;session_adapters.py;session_service.py
> WI-804 and WI-849 both touch agent_loop.py
> WI-804 and WI-852 both touch agent_loop.py;agent_route.py
> WI-804 and WI-853 are both open and both answer SR-155
> WI-804 and WI-853 both touch agent_loop.py;agent_route.py;hats.py;plan_artifacts.py;plan_briefs.py;plan_coverage.py;plan_coverage_step.py;plan_round.py;plan_runner.py;schedule.py
> WI-805 and WI-808 both touch integrate.py
> WI-805 and WI-809 both touch intake.py;verdict.py
> WI-805 and WI-810 both touch intake.py
> WI-805 and WI-811 are both open and both answer SR-154
> WI-805 and WI-811 both touch agent_brief.py;agent_loop.py;agent_route.py;done_when.py;intake.py;integrate.py;score_reviews.py;verdict.py
> WI-805 and WI-813 both touch agent_loop.py;agent_route.py;plan_coverage.py
> WI-805 and WI-816 both touch intake.py;integrate.py
> WI-805 and WI-828 both touch integrate.py
> WI-805 and WI-833 both touch integrate.py
> WI-805 and WI-834 both touch agent_loop.py;integrate.py
> WI-805 and WI-846 both touch agent_loop.py
> WI-805 and WI-847 both touch agent_loop.py
> WI-805 and WI-849 both touch agent_brief.py;agent_loop.py;done_when.py;intake.py;integrate.py;verdict.py
> WI-805 and WI-850 both touch verdict.py
> WI-805 and WI-851 both touch intake.py;integrate.py;verdict.py
> WI-805 and WI-852 are both open and both answer SR-154
> WI-805 and WI-852 both touch agent_brief.py;agent_loop.py;agent_route.py;done_when.py;intake.py;integrate.py;score_reviews.py;verdict.py
> WI-805 and WI-853 both touch agent_loop.py;agent_route.py;plan_coverage.py
> WI-807 and WI-817 both touch check.py
> WI-807 and WI-828 both touch check.py
> WI-807 and WI-851 both touch check.py
> WI-807 and WI-852 both touch gen_verdict_rollup.py
> WI-808 and WI-811 both touch integrate.py
> WI-808 and WI-816 both touch integrate.py
> WI-808 and WI-817 both touch agent_policy.py
> WI-808 and WI-828 both touch integrate.py
> WI-808 and WI-833 are both open and both answer SR-225
> WI-808 and WI-833 both touch agent_policy.py;decisions.py;gen_open_items.py;git.py;integrate.py;migrate_decisions.py;pending.py
> WI-808 and WI-834 both touch integrate.py
> WI-808 and WI-849 both touch integrate.py
> WI-808 and WI-851 both touch agent_policy.py;integrate.py
> WI-808 and WI-852 both touch integrate.py
> WI-809 and WI-810 both touch adjudicate_brief.py;intake.py
> WI-809 and WI-811 both touch intake.py;verdict.py
> WI-809 and WI-816 both touch intake.py
> WI-809 and WI-817 both touch trace.py
> WI-809 and WI-827 both touch trace.py
> WI-809 and WI-828 both touch acceptance_record.py;baseline_snapshot.py
> WI-809 and WI-834 both touch adjudicate_brief.py
> WI-809 and WI-846 both touch adjudicate_brief.py
> WI-809 and WI-847 both touch adjudicate_brief.py
> WI-809 and WI-849 are both open and both answer SR-178
> WI-809 and WI-849 both touch acceptance_record.py;adjudicate_brief.py;baseline_snapshot.py;intake.py;trace.py;verdict.py
> WI-809 and WI-850 are both open and both answer SR-178
> WI-809 and WI-850 both touch acceptance_record.py;adjudicate_brief.py;baseline_snapshot.py;trace.py;verdict.py
> WI-809 and WI-851 are both open and both answer SR-178
> WI-809 and WI-851 both touch acceptance_record.py;adjudicate_brief.py;baseline_snapshot.py;intake.py;trace.py;verdict.py
> WI-809 and WI-852 both touch adjudicate_brief.py;baseline_snapshot.py;intake.py;trace.py;verdict.py
> WI-809 and WI-854 both touch adjudicate_brief.py;baseline_snapshot.py;trace.py
> WI-810 and WI-811 both touch intake.py
> WI-810 and WI-816 both touch intake.py
> WI-810 and WI-834 both touch adjudicate_brief.py
> WI-810 and WI-846 both touch adjudicate_brief.py
> WI-810 and WI-847 both touch adjudicate_brief.py
> WI-810 and WI-849 both touch adjudicate_brief.py;intake.py
> WI-810 and WI-850 both touch adjudicate_brief.py
> WI-810 and WI-851 both touch adjudicate_brief.py;intake.py
> WI-810 and WI-852 both touch adjudicate_brief.py;intake.py
> WI-810 and WI-854 both touch adjudicate_brief.py
> WI-811 and WI-813 both touch agent_loop.py;agent_route.py
> WI-811 and WI-816 both touch intake.py;integrate.py
> WI-811 and WI-828 both touch integrate.py
> WI-811 and WI-833 both touch integrate.py
> WI-811 and WI-834 both touch agent_loop.py;integrate.py
> WI-811 and WI-846 both touch agent_loop.py
> WI-811 and WI-847 both touch agent_loop.py
> WI-811 and WI-849 both touch agent_brief.py;agent_loop.py;done_when.py;intake.py;integrate.py;verdict.py
> WI-811 and WI-850 both touch verdict.py
> WI-811 and WI-851 both touch intake.py;integrate.py;verdict.py
> WI-811 and WI-852 are both open and both answer SR-154
> WI-811 and WI-852 both touch agent_brief.py;agent_loop.py;agent_route.py;done_when.py;intake.py;integrate.py;score_reviews.py;verdict.py
> WI-811 and WI-853 both touch agent_loop.py;agent_route.py
> WI-813 and WI-834 both touch agent_loop.py
> WI-813 and WI-846 both touch agent_loop.py
> WI-813 and WI-847 both touch agent_loop.py
> WI-813 and WI-849 both touch agent_loop.py
> WI-813 and WI-852 both touch agent_loop.py;agent_route.py
> WI-813 and WI-853 are both open and both answer SR-155
> WI-813 and WI-853 both touch agent_loop.py;agent_route.py;hats.py;plan_artifacts.py;plan_briefs.py;plan_coverage.py;plan_coverage_step.py;plan_round.py;plan_runner.py;schedule.py
> WI-816 and WI-828 both touch integrate.py
> WI-816 and WI-833 both touch integrate.py
> WI-816 and WI-834 both touch integrate.py
> WI-816 and WI-849 both touch agent_common.py;intake.py;integrate.py
> WI-816 and WI-851 both touch agent_common.py;intake.py;integrate.py
> WI-816 and WI-852 both touch intake.py;integrate.py
> WI-817 and WI-827 both touch trace.py
> WI-817 and WI-828 both touch check.py
> WI-817 and WI-833 both touch agent_policy.py
> WI-817 and WI-849 both touch trace.py
> WI-817 and WI-850 both touch trace.py
> WI-817 and WI-851 both touch agent_policy.py;check.py;trace.py
> WI-817 and WI-852 both touch trace.py
> WI-817 and WI-854 both touch trace.py
> WI-827 and WI-849 both touch trace.py
> WI-827 and WI-850 both touch trace.py
> WI-827 and WI-851 both touch trace.py
> WI-827 and WI-852 both touch trace.py
> WI-827 and WI-854 both touch trace.py
> WI-828 and WI-833 both touch integrate.py
> WI-828 and WI-834 both touch integrate.py
> WI-828 and WI-849 both touch acceptance_record.py;baseline_snapshot.py;integrate.py
> WI-828 and WI-850 both touch acceptance_record.py;baseline_snapshot.py
> WI-828 and WI-851 both touch acceptance_record.py;baseline_snapshot.py;check.py;integrate.py
> WI-828 and WI-852 both touch baseline_snapshot.py;integrate.py
> WI-828 and WI-854 both touch baseline_snapshot.py
> WI-832 and WI-833 are both open and share one spec of record (docs/reviews/wi-818-owner-verdict/dispute-1-ruling.md)
> WI-832 and WI-833 were commissioned by the same docs/reviews/wi-818-owner-verdict/dispute-1-ruling.md
> WI-833 and WI-834 both touch integrate.py
> WI-833 and WI-849 both touch integrate.py
> WI-833 and WI-851 both touch agent_policy.py;integrate.py
> WI-833 and WI-852 both touch integrate.py
> WI-834 and WI-846 are both open and both answer SR-227
> WI-834 and WI-846 both touch adjudicate_brief.py;agent_loop.py;coordinator_adjudicate.py;dispatch.py;session_adapters.py;session_keep.py;session_service.py
> WI-834 and WI-847 are both open and both answer SR-227
> WI-834 and WI-847 both touch adjudicate_brief.py;agent_loop.py;coordinator_adjudicate.py;dispatch.py;session_adapters.py;session_keep.py;session_service.py
> WI-834 and WI-849 both touch adjudicate_brief.py;agent_loop.py;integrate.py
> WI-834 and WI-850 both touch adjudicate_brief.py
> WI-834 and WI-851 both touch adjudicate_brief.py;integrate.py
> WI-834 and WI-852 both touch adjudicate_brief.py;agent_loop.py;integrate.py
> WI-834 and WI-853 both touch agent_loop.py
> WI-834 and WI-854 both touch adjudicate_brief.py
> WI-846 and WI-847 are both open and both answer SR-227
> WI-846 and WI-847 are both open and share one spec of record (docs/log.d/2026-10-06-wave18-coordinator.md)
> WI-846 and WI-847 both touch adjudicate_brief.py;agent_loop.py;coordinator_adjudicate.py;dispatch.py;session_adapters.py;session_keep.py;session_service.py
> WI-846 and WI-847 were commissioned by the same docs/log.d/2026-10-06-wave18-coordinator.md
> WI-846 and WI-849 both touch adjudicate_brief.py;agent_loop.py
> WI-846 and WI-850 both touch adjudicate_brief.py
> WI-846 and WI-851 both touch adjudicate_brief.py
> WI-846 and WI-852 both touch adjudicate_brief.py;agent_loop.py
> WI-846 and WI-853 both touch agent_loop.py
> WI-846 and WI-854 both touch adjudicate_brief.py
> WI-847 and WI-849 both touch adjudicate_brief.py;agent_loop.py
> WI-847 and WI-850 both touch adjudicate_brief.py
> WI-847 and WI-851 both touch adjudicate_brief.py
> WI-847 and WI-852 both touch adjudicate_brief.py;agent_loop.py;prompts.py
> WI-847 and WI-853 both touch agent_loop.py
> WI-847 and WI-854 both touch adjudicate_brief.py;prompts.py
> WI-848 and WI-849 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-848 and WI-849 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-848 and WI-850 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-848 and WI-850 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-848 and WI-851 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-848 and WI-851 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-848 and WI-852 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-848 and WI-852 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-848 and WI-853 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-848 and WI-853 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-848 and WI-854 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-848 and WI-854 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-849 and WI-850 are both open and both answer SR-178
> WI-849 and WI-850 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-849 and WI-850 both touch acceptance_record.py;adjudicate_brief.py;baseline_snapshot.py;trace.py;verdict.py
> WI-849 and WI-850 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-849 and WI-851 are both open and both answer SR-178
> WI-849 and WI-851 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-849 and WI-851 both touch acceptance_record.py;adjudicate_brief.py;agent_common.py;baseline_snapshot.py;bookkeeping.py;intake.py;integrate.py;trace.py;verdict.py
> WI-849 and WI-851 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-849 and WI-852 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-849 and WI-852 both touch adjudicate_brief.py;agent_brief.py;agent_loop.py;baseline_snapshot.py;done_when.py;intake.py;integrate.py;trace.py;verdict.py
> WI-849 and WI-852 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-849 and WI-853 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-849 and WI-853 both touch agent_loop.py
> WI-849 and WI-853 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-849 and WI-854 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-849 and WI-854 both touch adjudicate_brief.py;baseline_snapshot.py;trace.py
> WI-849 and WI-854 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-850 and WI-851 are both open and both answer SR-178
> WI-850 and WI-851 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-850 and WI-851 both touch acceptance_record.py;adjudicate_brief.py;baseline_snapshot.py;trace.py;verdict.py
> WI-850 and WI-851 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-850 and WI-852 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-850 and WI-852 both touch adjudicate_brief.py;baseline_snapshot.py;trace.py;verdict.py
> WI-850 and WI-852 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-850 and WI-853 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-850 and WI-853 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-850 and WI-854 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-850 and WI-854 both touch adjudicate_brief.py;baseline_snapshot.py;trace.py
> WI-850 and WI-854 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-851 and WI-852 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-851 and WI-852 both touch adjudicate_brief.py;baseline_snapshot.py;intake.py;integrate.py;trace.py;verdict.py
> WI-851 and WI-852 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-851 and WI-853 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-851 and WI-853 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-851 and WI-854 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-851 and WI-854 both touch adjudicate_brief.py;baseline_snapshot.py;trace.py
> WI-851 and WI-854 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-852 and WI-853 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-852 and WI-853 both touch agent_loop.py;agent_route.py
> WI-852 and WI-853 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-852 and WI-854 are both open and both answer SR-146
> WI-852 and WI-854 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-852 and WI-854 both touch adjudicate_brief.py;agent_session.py;baseline_snapshot.py;gen_prompt_catalog.py;prompts.py;trace.py
> WI-852 and WI-854 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-853 and WI-854 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-853 and WI-854 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md

This row's `Adjudicates` cell fixes the population — judge those rows and no others. Its `Digests` cell is `20424540cd76|1237285c1cff`: the queue state and the spine state this question was asked against, so the census never asks it twice and a verdict that has gone stale is detectable rather than assumed fresh.

## Consolidation

Judged by an independent adjudicator; the verdict, with each finding, is
`docs/reviews/wi-855-adjudicate-queue-overlap-2042/001-ADJUDICATE-2d74139.md`.
No contradiction, no answered scope, no consolidation: six unordered
collisions get a hard edge. WI-833's two edges (on WI-828 and WI-832) are
recorded in the verdict for the coordinator, because WI-833 carries no `needs`
line the close can extend. A re-sitting
(`docs/reviews/wi-855-adjudicate-queue-overlap-2042/002-ADJUDICATE-e12a19e.md`,
which supersedes 001 for the close) added a seventh edge, WI-798 needs WI-834,
because WI-798 retires the per-family home that WI-846 authenticates and WI-834
checks, and it gives WI-798 a Done-when bullet to carry both across.
A third sitting
(`docs/reviews/wi-855-adjudicate-queue-overlap-2042/003-ADJUDICATE-75ca1b9.md`)
re-stamped the queue digest to `83a94fde0f88` after OI-110 (b) released WI-846:
the seven edges stand, and it records one hand edge for the coordinator, WI-848
needs WI-846 (WI-848 carries no `needs` line), with a Done-when bullet so the
coordinator-cycle recipes carry WI-846's token sign-in.

```toml
outcome = "queue-with-edge"
edges = [
  "WI-834 needs WI-846",
  "WI-847 needs WI-834",
  "WI-800 needs WI-847",
  "WI-851 needs WI-849",
  "WI-808 needs WI-832",
  "WI-801 needs WI-852",
  "WI-798 needs WI-834",
]
```
