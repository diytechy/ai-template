# WI-164 grounding review

**Date:** 2026-07-15 · **Verdict:** APPROVE

## Charter result

The seven cited primary sources exist, carry retrieval dates through the pack's
evidence heading, and support the load-bearing claims:

- Wolpert/Macready supports problem-conditioned algorithm choice rather than a
  universal optimizer.
- Bergstra/Bengio supports random search as the baseline over grids when only
  some dimensions matter.
- Hyperband supports early stopping and adaptive allocation of a declared
  resource across sampled configurations.
- Hansen supports CMA-ES for continuous, non-linear, non-convex black-box search
  and the pack limits that example to such spaces.
- Mouret/Clune supports an elite archive indexed by meaningful feature axes.
- OPRO demonstrates the LLM-as-optimizer loop; the independent revisit reports
  capability and cost limitations, so the pack does not claim universal
  superiority for LLM iteration.

The decision rubric, search-card fields, and convergence mapping are synthesis,
clearly presented as guidance rather than experimental findings. The WI-scale
two-promotion-round default is explicitly labeled a heuristic. Repo facts match
the current WI-163 dial semantics in PROCESS_OPTIONS. No claim requires
downgrading to ungrounded.

## Scope and duplication

PROCESS_OPTIONS holds only the stable route/search/stop discipline. The
algorithm detail, evidence, and heuristic remain in the knowledge pack. Neither
surface restates an SR/LLR/TC row, and no optimizer code or requirement-spine
change was introduced.

