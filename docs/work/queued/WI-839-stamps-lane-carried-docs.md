+++
id = "WI-839"
title = "The docs state that a lane carries its module-size stamp, as the integrator already does"
workstream = "process"
specref = "docs/reviews/wi-835-coordinator-retained-adjudication/sol-review-r5-dispute.md"
buildtier = "quick"
safety_class = "ordinary"
priority = 2
+++

## Context

Filed by hand by the wave-17 coordinator on 2026-10-06. A reviewer of WI-835
read `project-trajectory/PROCESS_OPTIONS.md` ("Stamps and ratchets are
re-derived or re-stamped on the trunk, never hand-carried on work branches")
and `docs/concurrency-restructure.md` §5.3 as forbidding a lane's stamp edit to
`tests/test_module_size_ratchet.py`. Neither the code nor the ratchet can work
that way. The ratchet matches exactly: a module that grows or shrinks fails
until its stamp moves. `integrate.py`'s `_HAND_STAMPED_GENERATED_KINDS` names
`linecounts` as the one declared generated kind that no command re-derives,
re-stamped by hand with a reason, with the lane's side kept. The reviewer
withdrew the finding under dispute (`sol-review-r5-dispute.md`). The text should
say what the machinery does, so the next reviewer does not raise it again.

## Done-when

- PROCESS_OPTIONS.md and concurrency-restructure §5.3 state the hand-stamped
  exception: the lane that changes a stamped module re-stamps it, with the
  reason in that commit, and every other declared generated artifact stays
  trunk-only. Both cite `integrate.py`'s exception in one place, not paraphrased
  twice.
- The byte-budget guard passes on PROCESS_OPTIONS.md.
- Review bar: A (one cross-family REVIEW-A).
