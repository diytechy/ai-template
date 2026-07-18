# Iterative optimization at WI scale

**Research WI:** WI-164 · **retrieved:** 2026-07-15

## Decision rubric

Choose the search mechanism from the representation and evaluator, not from a
generic preference for agents or optimizers:

| Situation | Default route | Why |
|---|---|---|
| The candidate is prose, architecture, visual composition, or another semantic artifact; quality needs judgment; edits are not safely parameterized | **LLM iteration** | The model can propose structural mutations and explain trade-offs that an explicit numeric search space would omit. Keep a small diverse beam and score against a fixed rubric. |
| The candidate has explicit bounded variables and a repeatable, cheap-enough objective; constraints can be encoded or rejected | **Constructed optimizer** | A coded loop makes sampling, evaluation, reproducibility, and stopping inspectable. Use gradients when trustworthy; otherwise start with random search and select a suitable black-box method only from observed structure. |
| Some choices are semantic while others are measurable parameters, or evaluation combines hard checks with judgment | **Hybrid** | Let the LLM define or mutate structure, then optimize explicit parameters in code; alternatively let deterministic gates filter candidates before rubric critique. Never ask an LLM to imitate arithmetic search over a space code can enumerate reliably. |

The decisive questions are: can candidates be encoded without throwing away
the property being improved; is the objective stable and repeatable; is an
evaluation cheap enough to sample; and does feedback identify useful local
changes? If all four are yes, construct the loop. If representation or
evaluation remains semantic, use LLM iteration. A hybrid is warranted only when
the boundary is explicit—name which variables and metrics are machine-owned and
which judgments are model/human-owned.

This is intentionally problem-conditioned. The no-free-lunch result rules out a
universally superior black-box algorithm over unrestricted problem classes; the
practical obligation is to state the assumptions that make the chosen search
bias appropriate.

## Solution-space layout and sampling

At WI scale, write a compact **search card** before spending the critique
budget:

1. Candidate representation and hard constraints.
2. One primary objective plus any guardrail thresholds; preserve a Pareto set
   when objectives genuinely conflict instead of hiding them in arbitrary
   weights.
3. Two to five behavior/features axes that describe meaningfully different
   candidates (not merely score components).
4. Evaluation protocol, noise controls, and cost per evaluation.
5. Initial sampling, promotion rule, and stop rule.

Use a deliberately heterogeneous seed set. For explicit independent variables,
random sampling is the baseline: Bergstra and Bengio show why grids waste trials
when only a subset of dimensions matters. Add boundary cases and known-good or
known-bad anchors. For semantic candidates, ask for contrasting strategies and
separate generation from scoring so one critique does not collapse every
candidate toward the same local style.

After the seed round:

- keep an **elite plus diversity archive**, not one incumbent; retain the best
  candidate in each useful behavior cell when several solution families matter
  (the MAP-Elites pattern);
- cross-pollinate by extracting independently successful traits, then request or
  construct candidates that combine named traits; evaluate combinations anew
  because interactions are not additive;
- promote promising candidates with more evaluation budget and stop weak ones
  early when partial evaluations are comparable (the successive-halving/
  Hyperband pattern);
- for expensive numeric black-box objectives with few dimensions, consider a
  surrogate-guided method; for continuous non-convex spaces with useful local
  correlations, a method such as CMA-ES can learn the sampling distribution.

Do not introduce a sophisticated optimizer before beating the recorded random
or diverse-beam baseline. The archive and evaluation log are part of the result:
without them, “cross-pollination” is only another untraceable prompt.

## Budget and convergence

WI-163's critique dial is a **hard resource ceiling**, not evidence of
convergence. Define stops before iteration and end on the first applicable one:

- **success:** all hard thresholds pass and the target score is met;
- **plateau:** no practically meaningful improvement in the best score or
  Pareto archive over a declared number of comparable rounds;
- **stability:** independent reruns or judges agree within the declared noise
  tolerance;
- **budget:** critique/evaluation limit is exhausted;
- **invalid search:** the objective drifts, evaluator disagreement dominates the
  expected gain, or constraints make sampled candidates mostly infeasible.

For a small WI, a useful default is a diverse seed round followed by two
promotion rounds, with a predeclared minimum effect size and patience of two
rounds. This is a starting heuristic, not a universal constant. `inf` permits
continued work but must not erase success, plateau, stability, or invalid-search
stops; `block` means budget exhaustion requires the declared human act. Record
best-so-far, diversity/archive coverage, evaluation count/cost, and the stop
reason. More rounds are not progress when the measurement cannot distinguish
them.

## Process boundary

PROCESS_OPTIONS should carry only the durable decision rule, the search-card
fields, and the distinction between resource ceilings and convergence. This
pack keeps algorithm selection detail, evidence, cautions, and the WI-scale
heuristic. Concrete optimizer code belongs in the adopting project's product
layer, never in the kit's process machinery.

## Primary evidence (retrieved 2026-07-15)

- [Wolpert and Macready, *No Free Lunch Theorems for Optimization*](https://doi.org/10.1109/4235.585893)
- [Bergstra and Bengio, *Random Search for Hyper-Parameter Optimization*](https://www.jmlr.org/papers/v13/bergstra12a.html)
- [Li et al., *Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization*](https://www.jmlr.org/papers/v18/16-558.html)
- [Hansen, *The CMA Evolution Strategy: A Tutorial*](https://arxiv.org/abs/1604.00772)
- [Mouret and Clune, *Illuminating search spaces by mapping elites*](https://arxiv.org/abs/1504.04909)
- [Yang et al., *Large Language Models as Optimizers*](https://arxiv.org/abs/2309.03409)
- [Zhang, Yuan, and Avestimehr, *Revisiting OPRO*](https://arxiv.org/abs/2405.10276)

