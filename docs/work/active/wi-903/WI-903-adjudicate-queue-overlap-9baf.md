+++
id = "WI-903"
title = "adjudicate queue overlap [9bafb7b507a5]: WI-798;WI-799;WI-800;WI-801;WI-804;WI-805;WI-807;WI-808;WI-809;WI-810;WI-811;WI-813;WI-816;WI-817;WI-827;WI-832;WI-833;WI-850;WI-851;WI-856;WI-857;WI-858;WI-878;WI-887;WI-893;WI-895;WI-897;WI-901;WI-902"
workstream = "process"
specref = "docs/work/README.md"
buildtier = "strong"
priority = 9
safety_class = "adjudication"
brief = "consolidate"
adjudicates = ["WI-798", "WI-799", "WI-800", "WI-801", "WI-804", "WI-805", "WI-807", "WI-808", "WI-809", "WI-810", "WI-811", "WI-813", "WI-816", "WI-817", "WI-827", "WI-832", "WI-833", "WI-850", "WI-851", "WI-856", "WI-857", "WI-858", "WI-878", "WI-887", "WI-893", "WI-895", "WI-897", "WI-901", "WI-902"]
digests = "9bafb7b507a5|e3900a5ad95a"
+++

## Context

Minted by the CONSOLIDATION CENSUS (the 2026-09-02 backlog-restructure plan §1.3), which runs from an idle station with no judgement in progress and none queued over these rows or ahead of this one. The candidate cluster is 29 queued row(s): WI-798;WI-799;WI-800;WI-801;WI-804;WI-805;WI-807;WI-808;WI-809;WI-810;WI-811;WI-813;WI-816;WI-817;WI-827;WI-832;WI-833;WI-850;WI-851;WI-856;WI-857;WI-858;WI-878;WI-887;WI-893;WI-895;WI-897;WI-901;WI-902.

The mechanical pre-filter selected them; it has concluded NOTHING. Each line below is a hint a string comparison can produce, and two rows deliberately cut from one plan share its path and always will:

> WI-798 and WI-799 both touch agent_loop.py
> WI-798 and WI-800 are both open and both answer SR-222
> WI-798 and WI-800 both touch agent_loop.py;plan_runner.py;session_adapters.py;session_service.py
> WI-798 and WI-801 are both open and both answer SR-222
> WI-798 and WI-801 both touch agent_loop.py;plan_runner.py;session_adapters.py;session_service.py
> WI-798 and WI-804 are both open and both answer SR-222
> WI-798 and WI-804 both touch agent_loop.py;plan_runner.py;session_adapters.py;session_service.py
> WI-798 and WI-805 both touch agent_loop.py
> WI-798 and WI-811 both touch agent_loop.py
> WI-798 and WI-813 both touch agent_loop.py;plan_runner.py
> WI-798 and WI-857 both touch agent_loop.py
> WI-798 and WI-858 both touch agent_loop.py;session_adapters.py;session_service.py
> WI-798 and WI-887 both touch agent_loop.py;session_adapters.py;session_service.py
> WI-798 and WI-895 both touch session_adapters.py
> WI-799 and WI-800 both touch adjudicate_brief.py;agent_loop.py
> WI-799 and WI-801 both touch agent_brief.py;agent_loop.py;done_when.py;intake.py;integrate.py;verdict.py
> WI-799 and WI-804 both touch agent_loop.py
> WI-799 and WI-805 both touch agent_brief.py;agent_loop.py;done_when.py;intake.py;integrate.py;verdict.py
> WI-799 and WI-807 both touch lane_state.py
> WI-799 and WI-808 both touch integrate.py
> WI-799 and WI-809 both touch adjudicate_brief.py;intake.py;verdict.py
> WI-799 and WI-810 both touch adjudicate_brief.py;handback.py;intake.py
> WI-799 and WI-811 both touch agent_brief.py;agent_loop.py;done_when.py;intake.py;integrate.py;verdict.py
> WI-799 and WI-813 both touch agent_loop.py
> WI-799 and WI-816 both touch agent_common.py;intake.py;integrate.py
> WI-799 and WI-833 both touch integrate.py
> WI-799 and WI-850 both touch adjudicate_brief.py;verdict.py
> WI-799 and WI-851 both touch adjudicate_brief.py;agent_common.py;bookkeeping.py;handback.py;intake.py;integrate.py;verdict.py
> WI-799 and WI-856 both touch handback.py;intake.py
> WI-799 and WI-857 are both open and both answer SR-156
> WI-799 and WI-857 both touch adjudicate_brief.py;agent_brief.py;agent_common.py;agent_loop.py;bookkeeping.py;done_when.py;intake.py;integrate.py;lane.py;spec_move.py;verdict.py
> WI-799 and WI-858 both touch adjudicate_brief.py;agent_loop.py
> WI-799 and WI-887 both touch adjudicate_brief.py;agent_loop.py
> WI-799 and WI-893 both touch integrate.py
> WI-799 and WI-897 both touch integrate.py
> WI-799 and WI-901 both touch agent_common.py;bookkeeping.py;handback.py;intake.py;integrate.py
> WI-799 and WI-902 both touch handback.py;intake.py
> WI-800 and WI-801 are both open and both answer SR-222
> WI-800 and WI-801 both touch agent_loop.py;coordinator_adjudicate.py;plan_runner.py;session_adapters.py;session_service.py
> WI-800 and WI-804 are both open and both answer SR-222
> WI-800 and WI-804 both touch agent_loop.py;plan_runner.py;session_adapters.py;session_service.py
> WI-800 and WI-805 both touch agent_loop.py
> WI-800 and WI-807 were commissioned by the same OI-109
> WI-800 and WI-809 both touch adjudicate_brief.py
> WI-800 and WI-810 both touch adjudicate_brief.py
> WI-800 and WI-811 both touch agent_loop.py
> WI-800 and WI-813 both touch agent_loop.py;plan_runner.py
> WI-800 and WI-850 both touch adjudicate_brief.py
> WI-800 and WI-851 both touch adjudicate_brief.py
> WI-800 and WI-857 both touch adjudicate_brief.py;agent_loop.py
> WI-800 and WI-858 are both open and both answer SR-227
> WI-800 and WI-858 both touch adjudicate_brief.py;agent_loop.py;coordinator_adjudicate.py;dispatch.py;session_adapters.py;session_keep.py;session_service.py
> WI-800 and WI-887 are both open and both answer SR-227
> WI-800 and WI-887 both touch adjudicate_brief.py;agent_loop.py;coordinator_adjudicate.py;dispatch.py;session_adapters.py;session_keep.py;session_service.py
> WI-800 and WI-895 both touch session_adapters.py
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
> WI-801 and WI-833 both touch integrate.py
> WI-801 and WI-850 both touch verdict.py
> WI-801 and WI-851 both touch intake.py;integrate.py;verdict.py
> WI-801 and WI-856 both touch intake.py
> WI-801 and WI-857 both touch agent_brief.py;agent_loop.py;done_when.py;intake.py;integrate.py;verdict.py
> WI-801 and WI-858 both touch agent_loop.py;coordinator_adjudicate.py;session_adapters.py;session_service.py
> WI-801 and WI-887 both touch agent_loop.py;coordinator_adjudicate.py;session_adapters.py;session_service.py
> WI-801 and WI-893 both touch integrate.py
> WI-801 and WI-895 both touch session_adapters.py
> WI-801 and WI-897 both touch integrate.py
> WI-801 and WI-901 both touch intake.py;integrate.py
> WI-801 and WI-902 both touch intake.py
> WI-804 and WI-805 both touch agent_loop.py;agent_route.py;plan_coverage.py
> WI-804 and WI-811 both touch agent_loop.py;agent_route.py
> WI-804 and WI-813 are both open and both answer SR-155
> WI-804 and WI-813 both touch agent_loop.py;agent_route.py;hats.py;plan_artifacts.py;plan_briefs.py;plan_coverage.py;plan_coverage_step.py;plan_round.py;plan_runner.py;schedule.py
> WI-804 and WI-857 both touch agent_loop.py
> WI-804 and WI-858 both touch agent_loop.py;session_adapters.py;session_service.py
> WI-804 and WI-878 both touch plan_coverage.py
> WI-804 and WI-887 both touch agent_loop.py;session_adapters.py;session_service.py
> WI-804 and WI-895 both touch session_adapters.py
> WI-805 and WI-808 both touch integrate.py
> WI-805 and WI-809 both touch intake.py;verdict.py
> WI-805 and WI-810 both touch intake.py
> WI-805 and WI-811 are both open and both answer SR-154
> WI-805 and WI-811 both touch agent_brief.py;agent_loop.py;agent_route.py;done_when.py;intake.py;integrate.py;score_reviews.py;verdict.py
> WI-805 and WI-813 both touch agent_loop.py;agent_route.py;plan_coverage.py
> WI-805 and WI-816 both touch intake.py;integrate.py
> WI-805 and WI-833 both touch integrate.py
> WI-805 and WI-850 both touch verdict.py
> WI-805 and WI-851 both touch intake.py;integrate.py;verdict.py
> WI-805 and WI-856 both touch intake.py
> WI-805 and WI-857 both touch agent_brief.py;agent_loop.py;done_when.py;intake.py;integrate.py;verdict.py
> WI-805 and WI-858 both touch agent_loop.py
> WI-805 and WI-878 both touch plan_coverage.py
> WI-805 and WI-887 both touch agent_loop.py
> WI-805 and WI-893 both touch integrate.py
> WI-805 and WI-897 both touch integrate.py
> WI-805 and WI-901 both touch intake.py;integrate.py
> WI-805 and WI-902 both touch intake.py
> WI-807 and WI-817 both touch check.py
> WI-807 and WI-851 both touch check.py
> WI-807 and WI-893 both touch check.py
> WI-807 and WI-901 both touch check.py
> WI-808 and WI-811 both touch integrate.py
> WI-808 and WI-816 both touch integrate.py
> WI-808 and WI-817 both touch agent_policy.py
> WI-808 and WI-833 are both open and both answer SR-225
> WI-808 and WI-833 both touch agent_policy.py;decisions.py;gen_open_items.py;git.py;integrate.py;migrate_decisions.py;pending.py
> WI-808 and WI-851 both touch agent_policy.py;integrate.py
> WI-808 and WI-857 both touch integrate.py
> WI-808 and WI-893 both touch integrate.py
> WI-808 and WI-897 both touch integrate.py
> WI-808 and WI-901 both touch agent_policy.py;integrate.py
> WI-809 and WI-810 both touch adjudicate_brief.py;intake.py
> WI-809 and WI-811 both touch intake.py;verdict.py
> WI-809 and WI-816 both touch intake.py
> WI-809 and WI-817 both touch trace.py
> WI-809 and WI-827 both touch trace.py
> WI-809 and WI-850 are both open and both answer SR-178
> WI-809 and WI-850 both touch acceptance_record.py;adjudicate_brief.py;baseline_snapshot.py;trace.py;verdict.py
> WI-809 and WI-851 are both open and both answer SR-178
> WI-809 and WI-851 both touch acceptance_record.py;adjudicate_brief.py;baseline_snapshot.py;intake.py;trace.py;verdict.py
> WI-809 and WI-856 both touch intake.py
> WI-809 and WI-857 are both open and both answer SR-178
> WI-809 and WI-857 both touch acceptance_record.py;adjudicate_brief.py;baseline_snapshot.py;intake.py;trace.py;verdict.py
> WI-809 and WI-858 both touch adjudicate_brief.py
> WI-809 and WI-887 both touch adjudicate_brief.py
> WI-809 and WI-893 both touch acceptance_record.py;baseline_snapshot.py
> WI-809 and WI-901 both touch acceptance_record.py;intake.py
> WI-809 and WI-902 both touch intake.py
> WI-810 and WI-811 both touch intake.py
> WI-810 and WI-816 both touch intake.py
> WI-810 and WI-850 both touch adjudicate_brief.py
> WI-810 and WI-851 both touch adjudicate_brief.py;handback.py;intake.py
> WI-810 and WI-856 are both open and both answer SR-220
> WI-810 and WI-856 both touch consolidate.py;handback.py;intake.py
> WI-810 and WI-857 both touch adjudicate_brief.py;intake.py
> WI-810 and WI-858 both touch adjudicate_brief.py
> WI-810 and WI-887 both touch adjudicate_brief.py
> WI-810 and WI-901 both touch handback.py;intake.py
> WI-810 and WI-902 are both open and both answer SR-220
> WI-810 and WI-902 both touch consolidate.py;handback.py;intake.py
> WI-811 and WI-813 both touch agent_loop.py;agent_route.py
> WI-811 and WI-816 both touch intake.py;integrate.py
> WI-811 and WI-833 both touch integrate.py
> WI-811 and WI-850 both touch verdict.py
> WI-811 and WI-851 both touch intake.py;integrate.py;verdict.py
> WI-811 and WI-856 both touch intake.py
> WI-811 and WI-857 both touch agent_brief.py;agent_loop.py;done_when.py;intake.py;integrate.py;verdict.py
> WI-811 and WI-858 both touch agent_loop.py
> WI-811 and WI-887 both touch agent_loop.py
> WI-811 and WI-893 both touch integrate.py
> WI-811 and WI-897 both touch integrate.py
> WI-811 and WI-901 both touch intake.py;integrate.py
> WI-811 and WI-902 both touch intake.py
> WI-813 and WI-857 both touch agent_loop.py
> WI-813 and WI-858 both touch agent_loop.py
> WI-813 and WI-878 both touch plan_coverage.py
> WI-813 and WI-887 both touch agent_loop.py
> WI-816 and WI-833 both touch integrate.py
> WI-816 and WI-851 both touch agent_common.py;intake.py;integrate.py
> WI-816 and WI-856 both touch intake.py
> WI-816 and WI-857 both touch agent_common.py;intake.py;integrate.py
> WI-816 and WI-893 both touch integrate.py
> WI-816 and WI-897 both touch integrate.py
> WI-816 and WI-901 both touch agent_common.py;intake.py;integrate.py
> WI-816 and WI-902 both touch intake.py
> WI-817 and WI-827 both touch trace.py
> WI-817 and WI-833 both touch agent_policy.py
> WI-817 and WI-850 both touch trace.py
> WI-817 and WI-851 both touch agent_policy.py;check.py;trace.py
> WI-817 and WI-857 both touch trace.py
> WI-817 and WI-893 both touch check.py
> WI-817 and WI-901 both touch agent_policy.py;check.py
> WI-827 and WI-850 both touch trace.py
> WI-827 and WI-851 both touch trace.py
> WI-827 and WI-857 both touch trace.py
> WI-832 and WI-833 are both open and share one spec of record (docs/reviews/wi-818-owner-verdict/dispute-1-ruling.md)
> WI-832 and WI-833 were commissioned by the same docs/reviews/wi-818-owner-verdict/dispute-1-ruling.md
> WI-833 and WI-851 both touch agent_policy.py;integrate.py
> WI-833 and WI-857 both touch integrate.py
> WI-833 and WI-893 both touch integrate.py
> WI-833 and WI-897 both touch integrate.py
> WI-833 and WI-901 both touch agent_policy.py;integrate.py
> WI-850 and WI-851 are both open and both answer SR-178
> WI-850 and WI-851 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-850 and WI-851 both touch acceptance_record.py;adjudicate_brief.py;baseline_snapshot.py;trace.py;verdict.py
> WI-850 and WI-851 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-850 and WI-857 are both open and both answer SR-178
> WI-850 and WI-857 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-850 and WI-857 both touch acceptance_record.py;adjudicate_brief.py;baseline_snapshot.py;trace.py;verdict.py
> WI-850 and WI-857 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-850 and WI-858 both touch adjudicate_brief.py
> WI-850 and WI-887 both touch adjudicate_brief.py
> WI-850 and WI-893 both touch acceptance_record.py;baseline_snapshot.py
> WI-850 and WI-901 both touch acceptance_record.py
> WI-851 and WI-856 both touch handback.py;intake.py
> WI-851 and WI-857 are both open and both answer SR-178
> WI-851 and WI-857 are both open and share one spec of record (docs/plans/2026-10-07-wi841-retro/PROPOSAL.md)
> WI-851 and WI-857 both touch acceptance_record.py;adjudicate_brief.py;agent_common.py;baseline_snapshot.py;bookkeeping.py;intake.py;integrate.py;trace.py;verdict.py
> WI-851 and WI-857 were commissioned by the same docs/plans/2026-10-07-wi841-retro/PROPOSAL.md
> WI-851 and WI-858 both touch adjudicate_brief.py
> WI-851 and WI-887 both touch adjudicate_brief.py
> WI-851 and WI-893 both touch acceptance_record.py;baseline_snapshot.py;check.py;integrate.py
> WI-851 and WI-897 both touch integrate.py
> WI-851 and WI-901 are both open and both answer SR-208
> WI-851 and WI-901 both touch acceptance_record.py;agent_common.py;agent_policy.py;authority.py;bookkeeping.py;check.py;handback.py;intake.py;integrate.py
> WI-851 and WI-902 both touch handback.py;intake.py
> WI-856 and WI-857 both touch intake.py
> WI-856 and WI-901 both touch handback.py;intake.py
> WI-856 and WI-902 are both open and both answer SR-220
> WI-856 and WI-902 both touch consolidate.py;handback.py;intake.py
> WI-857 and WI-858 both touch adjudicate_brief.py;agent_loop.py
> WI-857 and WI-887 both touch adjudicate_brief.py;agent_loop.py
> WI-857 and WI-893 both touch acceptance_record.py;baseline_snapshot.py;integrate.py
> WI-857 and WI-897 both touch integrate.py
> WI-857 and WI-901 both touch acceptance_record.py;agent_common.py;bookkeeping.py;intake.py;integrate.py
> WI-857 and WI-902 both touch intake.py
> WI-858 and WI-887 are both open and both answer SR-227
> WI-858 and WI-887 both touch adjudicate_brief.py;agent_loop.py;coordinator_adjudicate.py;coordinator_guard.py;dispatch.py;session_adapters.py;session_keep.py;session_service.py
> WI-858 and WI-895 both touch session_adapters.py
> WI-858 and WI-897 both touch coordinator_guard.py
> WI-887 and WI-895 both touch session_adapters.py
> WI-887 and WI-897 both touch coordinator_guard.py
> WI-893 and WI-897 both touch integrate.py
> WI-893 and WI-901 both touch acceptance_record.py;check.py;integrate.py
> WI-897 and WI-901 both touch integrate.py
> WI-901 and WI-902 both touch handback.py;intake.py

This row's `Adjudicates` cell fixes the population — judge those rows and no others. Its `Digests` cell is `9bafb7b507a5|e3900a5ad95a`: the queue state and the spine state this question was asked against, so the census never asks it twice and a verdict that has gone stale is detectable rather than assumed fresh.
