# Planning before the build: preliminary research (2026-10-04)

**Status:** preliminary research feeding [WI-788](../work/queued/WI-788-provider-homes-and-new-routes.md)'s
half-1 design note. It was gathered by a research subagent on 2026-10-03/04 and has
not been checked further by the coordinator. The 2026 papers were read from their
abstracts only. The questions WI-788 must still uncover are listed in its spec,
under "Scope widened 2026-10-04".

## The question

Should a work item get an explicit planning session before its build? A single plan
with a review, or two competing plans with critique and an arbiter? Asked in terms of
outcome quality, iterations and rework, and cost against accuracy.

## What the kit has today

- The **builder plans inside its own session.** No loop phase plans before a build.
- **Dual-plan decomposition** (PROCESS_OPTIONS.md, "Dual-plan decomposition";
  SN-024, SR-155) is an opt-in *decomposition* layer, not a per-item build step. Two
  planners write rival breakdowns of a design-shaping goal into work items, critique
  each other after a coverage pre-pass, and two arbiter runs with swapped positions
  pick one. The winner's child rows are filed.
- **History:**
  - WI-199 (2026-07-17) made the loop run the round unattended.
  - WI-209 (2026-07-17) made the dispatcher start it for a `planmode = "dual"` row.
    That closed a "quiet park", where such a row sat idle.
  - Concurrency-restructure Phase 5 (`31ad569d`, 2026-07-29) deleted the old
    dispatcher (`agent_dispatch.py`), and that start went with it. The round engine
    (`plan_runner.py`, `agent_loop.py --dual-plan`) and its tests were kept, and the
    new `dispatch.py` never picks dual rows up.
  - So a dual row is claimed, refused at the worker's preflight
    (`agent_loop.py:1317-1329`), parked and resumed in a loop. This is a regression,
    not a ruling. No live row is marked dual, so it has not fired.

## Findings

**Well supported**
- **A plan improves correctness on non-trivial work.**
  - Self-planning: HumanEval pass@1 rose from 48.1% to 60.3%, and the method was weak
    in small models ([arXiv 2303.06689](https://arxiv.org/abs/2303.06689)).
  - MapCoder: removing the planner cost about 16.7%, and its token use is high
    ([arXiv 2405.11403](https://arxiv.org/html/2405.11403v1)).
  - CodePlan: 5 of 6 repo migrations passed, against 0 of 6 for the baselines
    ([arXiv 2309.12499](https://arxiv.org/abs/2309.12499)).
- **Splitting design from editing helps.** Aider's architect/editor pairing scored 3
  to 10 points over solo runs, 85.0% at best
  ([aider.chat](https://aider.chat/2024/09/26/architect.html)).
- **Plan quality decides the outcome.**
  - A bad plan does worse than no plan across 21k SWE-agent trajectories
    ([arXiv 2604.12147](https://arxiv.org/abs/2604.12147), abstract only).
  - Plan-and-Act on web tasks, not coding: an untrained planner gave a small gain,
    and replanning during the task added about 10 points
    ([arXiv 2503.09572](https://arxiv.org/html/2503.09572v3)).
- **Debate rarely pays.** Debate between instances of one model rarely beats cheaper
  single-agent ensembles at equal or lower cost
  ([arXiv 2311.17371](https://arxiv.org/abs/2311.17371),
  [arXiv 2502.08788](https://arxiv.org/abs/2502.08788),
  [arXiv 2402.18272](https://arxiv.org/abs/2402.18272)). Using **different models**
  was the one factor that consistently helped.
- **Self-critique without external feedback is unreliable**
  ([arXiv 2310.01798](https://arxiv.org/abs/2310.01798)).

**Weaker or contested**
- **Cost.** Planning every time is expensive. AdaCoder plans only after a cheap
  plan-free attempt fails, and reports +27.69% pass@1 at 16× faster and 12× fewer
  tokens than MapCoder ([arXiv 2504.04220](https://arxiv.org/abs/2504.04220)).
- **Rework.** No controlled study measures it. Anthropic's guidance that a plan
  prevents "solving the wrong problem" is practitioner guidance
  ([Claude Code best practices](https://code.claude.com/docs/en/best-practices);
  [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)).
- **Dual plans plus an arbiter** has no direct study in agentic coding. The supported
  pieces:
  - diverse plans raise the ceiling, but only with a selector (PlanSearch,
    [arXiv 2409.03733](https://arxiv.org/abs/2409.03733));
  - selection works when the arbiter is backed by execution or tests (Trae on
    SWE-bench Verified, a
    [vendor blog](https://se-research.bytedance.com/blogs/trae-on-swe-bench-verified-71)).

## The kit's own evidence on the arbiter (2026-10-04)

The owner: "even before this the arbiter never was actually needed, the
cross-critique always resulted in both drafters selecting the same plan at the end."

This repo records one round, DP-001 (2026-07-16,
[verdict](../archive/plans/DP-001-dual-plan-loop-wiring/verdict.md)):
- each cross-critique raised one finding;
- both position-swapped arbiter runs selected the same plan, with nothing ported.

This fits the literature above: cross-family critique and revision does the useful
work, and a second judgement over two converged plans adds cost without changing the
outcome. WI-788 counts convergence across every available round before it decides
whether the arbiter stays.

## Guidance as it stands

- **No plan** when the diff fits in one sentence or a cheap test fully specifies the
  task.
- **One plan plus a fresh-context review** for multi-file, unfamiliar or ambiguous
  work, with replanning allowed. A reviewer told to find gaps will always find some,
  so ground the review in the acceptance criteria.
- **Plan on demand:** plan after a cheap attempt fails (AdaCoder). This maps onto the
  kit's existing escalation ladder (swap family, then tier up, then page).
- **Dual plans** only for high-risk, design-shaping decisions, with planners from
  different families and an arbiter grounded in testable criteria (Done-when
  coverage, TC coverage) rather than persuasiveness.

Most numbers come from function-level benchmarks, 2023–24 models, or web tasks.
