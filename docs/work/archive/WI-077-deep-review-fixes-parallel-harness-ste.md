+++
id = "WI-077"
title = "Deep-review fixes + parallel harness steps"
workstream = "scripts"
needs = ["WI-075"]
order = 76
+++

## Deliverable

Owner-directed deep review 2026-07-12 (docs/archive/repo-review-2026-07-12.md) + its confident fixes. Review: full-repo, no critical findings; four owner rulings queued in status.md (F5 census/bound, [step:dupes], archive-anchor comments, the agent_loop/trace/bootstrap main() decomposition effort). Fixes: (H4) check.py --jobs N (0=auto) runs the gate plan's steps concurrently in lanes (registry-integrity + traceability share one lane - both trace.py runs rewrite docs/test/report.md; everything else is read-only or disjoint), output captured per step and printed whole, sequential --jobs 1 default byte-identical downstream; --run-steps A,B,... batch form of --run-step (lenient, parallel, reports EVERY failure); hooks/pre-commit's six chained --run-step/script calls collapsed to one batched call (faster + names all stale artifacts in one pass, superseding the set-e first-failure ordering); CI gate job runs --jobs 0. (H2) commit-bar text (session-protocol skill + fan-out + CLAUDE.md) now says pytest -q -n auto (~70s vs ~340s serial - the declared stack.ini command; biggest per-commit win). (H3) gen_trajectory's triplicated rank/order/barycentre/coords block deduplicated into _layered_layout (WI-DAG/sw/know callers; verified byte-identical - --check green without regen). (M3) duplicate id=dag in PROJECT_STATE.html: inner view div renamed dag-view (valid HTML, zero behavior change - getElementById already resolved the section). (M4) meta .gitattributes dead root-anchored hooks/pre-commit pattern replaced with .githooks/* + project-trajectory/hooks/*; gitattributes.template gains .githooks/commit-msg. No spine change: --jobs/--run-steps preserve SR-006's step-set + never-a-false-green semantics (concurrency is execution, not requirement surface; WI-075 precedent). Tests: 4 new in test_check_harness (batch green, batch reports every failure, unknown name loud, parallel plan matches sequential incl. false-green guard); hook/gen_trajectory test anchors updated.
