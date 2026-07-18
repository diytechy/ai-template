# Co-planning: reconciling independent work-item decompositions

**Research WI:** WI-190 (filed from the 2026-07-16 owner feedback session) ·
**retrieved:** 2026-07-16

## The design question

Two planner sessions independently decompose the same goal into rival work-item
plans (one proposes 4 WIs, the other 3). What reconciliation architecture is
best supported: (a) merging the plans, (b) an arbiter selecting one and porting
missing pieces, or (c) iterating the plans against each other's critique until
they agree?

## What the evidence rules out

- **Iterate-until-agree between peers.** Agents iterating on each other's
  feedback conform rather than challenge: group accuracy often *declines* over
  rounds even when stronger models hold the majority (Talk Isn't Always Cheap);
  measured sycophantic conformity reaches 85.5% of exchanges, and plurality
  consensus can *eliminate* a correct answer already on the table ("consensus
  collapse", gaps up to 32.3 pp) while isolated self-correction matches or beats
  unguided debate at 2.1–3.4× fewer tokens (Cost of Consensus). Refinement
  without an *external* signal degrades reasoning (Huang et al.), and peer LLM
  critique is not external in the relevant sense (CRITIC's tool-grounding
  ablation).
- **Many rounds.** Gains concentrate in round 1 and plateau by 2–3 across the
  debate literature (MAD survey); extended debates show "problem drift" — in one
  analysis ~0.5% of continued debates improved on the first-turn draft while
  ~0.8% got worse (Becker et al.). Budget one critique round, not n.
- **Debate as the default.** Multi-agent debate does not reliably beat
  self-consistency or ensembling at matched compute (Smit et al.); plain
  sample-then-select is a strong cheap baseline (More Agents Is All You Need;
  AlphaCode's sample-and-filter).
- **Plan merging.** Essentially unpublished: the closest method (DPPM) merges
  sub-plans of a *single* decomposition, never two rival full plans. Naive union
  of two WI DAGs risks incoherent predecessors and duplicated scope. No
  benchmark shows merge > select for divergent plans.

## What the evidence supports

- **Independent generation with real diversity.** Cross-model-family diversity
  drives the gains in multi-model consensus (ReConcile); two samples of one
  model share blind spots (the same popularity-trap correction
  `score_reviews.py` already encodes).
- **A judge separate from the debaters.** The published fix for
  degeneration-of-thought is engineered disagreement plus a *separate* judge
  (Liang et al.); structured two-sided argument judged by a fresh judge beats a
  single persuasive consultant (Khan et al., ICML 2024 best paper). The arbiter
  judges **artifacts, not conversations**.
- **Arbiter debiasing as the binding constraint.** LLM judges carry position
  bias, verbosity bias (a 4-WI plan beats a 3-WI plan for length alone), and
  self-preference — judges detectably favor their own model family's outputs
  (Zheng et al.; Panickssery et al.). Mitigations: different-family judge,
  anonymized provenance, position-swapped pairwise comparison, and rubric
  anchoring over bare "which is better" (rubric/pointwise scoring is more robust
  to judges being gamed by surface features).
- **Checkable feedback makes the one critique round work.** Refinement helps
  when feedback is external and locally verifiable (CRITIC; Self-Refine's
  domain split). Requiring every proposed WI to cite the SR/goal clauses it
  covers and the IF-IDs it touches makes rival plans **mechanically
  commensurable** — "what does plan A cover that plan B misses" becomes a
  computed diff, not a judgment call.
- **A published decomposition rubric exists**: solvability, completeness,
  non-redundancy (Agent-Oriented Planning), a starting point for the plan
  critique rubric.

## Net read

Select-and-port beats merge and beats consensus: two independent
different-family planners → mechanical coverage diff → **one** rubric-anchored
cross-critique + revision → a fresh third-family arbiter (provenance-anonymized,
position-swapped, rubric-anchored, warned against more-WIs-is-better) selects
one plan and ports named loser-WIs that close coverage gaps, each port a cited
delta. Human attestation closes acceptance per the gate philosophy.

**Transfer caveat (state it wherever this is applied):** the debate/selection
evidence comes from QA, math, and code with objective verifiers — nothing
benchmarks these protocols on *plan artifacts*, and two-planner reconciliation
evaluated for plan quality is an open research gap. The protocol above is the
best-supported extrapolation, not a proven design. Per-round drift figures rest
on abstracts/secondary summaries; verify against source tables before citing
numerically in a design ruling.

## Primary evidence (retrieved 2026-07-16)

- [Du et al., *Improving Factuality and Reasoning through Multiagent Debate* (2305.14325)](https://arxiv.org/abs/2305.14325)
- [Smit et al., *Should we be going MAD?* (2311.17371)](https://arxiv.org/abs/2311.17371)
- [Li et al., *More Agents Is All You Need* (2402.05120)](https://arxiv.org/abs/2402.05120)
- [Liang et al., *Encouraging Divergent Thinking in LLMs through Multi-Agent Debate* (2305.19118)](https://arxiv.org/abs/2305.19118)
- [*Talk Isn't Always Cheap: Failure Modes in Multi-Agent Debate* (2509.05396)](https://arxiv.org/abs/2509.05396)
- [Bertalanič et al., *The Cost of Consensus* (2605.00914)](https://arxiv.org/abs/2605.00914)
- [Kaesberg et al., *Voting or Consensus? Decision-Making in Multi-Agent Debate* (2502.19130)](https://arxiv.org/abs/2502.19130)
- [Chen et al., *ReConcile: Round-Table Conference Improves Reasoning* (2309.13007)](https://arxiv.org/abs/2309.13007)
- [Khan et al., *Debating with More Persuasive LLMs Leads to More Truthful Answers* (2402.06782)](https://arxiv.org/abs/2402.06782)
- [Li et al., *Agent-Oriented Planning in Multi-Agent Systems* (2410.02189)](https://arxiv.org/abs/2410.02189)
- [Becker et al., *Stay Focused: Problem Drift in Multi-Agent Debate* (2502.19559)](https://arxiv.org/abs/2502.19559)
- [*A Literature Review of Multi-Agent Debate for Problem-Solving* (2506.00066)](https://arxiv.org/abs/2506.00066)
- [Zheng et al., *Judging LLM-as-a-Judge with MT-Bench* (2306.05685)](https://arxiv.org/abs/2306.05685)
- [Panickssery et al., *LLM Evaluators Recognize and Favor Their Own Generations* (2404.13076)](https://arxiv.org/abs/2404.13076)
- [Huang et al., *LLMs Cannot Self-Correct Reasoning Yet* (2310.01798)](https://arxiv.org/abs/2310.01798)
- [Gou et al., *CRITIC: Tool-Interactive Critiquing* (2305.11738)](https://arxiv.org/abs/2305.11738)
- [Madaan et al., *Self-Refine: Iterative Refinement with Self-Feedback* (2303.17651)](https://arxiv.org/abs/2303.17651)
- [Snell et al., *Scaling LLM Test-Time Compute Optimally* (2408.03314)](https://arxiv.org/abs/2408.03314)
- [Li et al., *Competition-Level Code Generation with AlphaCode* (2203.07814)](https://arxiv.org/abs/2203.07814)
- [*Decompose, Plan in Parallel, and Merge* (2506.02683)](https://arxiv.org/abs/2506.02683)
