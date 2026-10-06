+++
id = "WI-839"
title = "The docs state that a lane carries its module-size stamp, as the integrator already does"
workstream = "process"
specref = ""
buildtier = "quick"
safety_class = "ordinary"
priority = 9
+++

## Deliverable

PROCESS_OPTIONS.md's shared-surface rules now state the one exception to "stamps are re-derived or re-stamped on the trunk": the module-size ratchet (generated kind `linecounts`), which no command re-derives, is re-stamped by the lane that changes a stamped module, with the reason in that commit, and `integrate.py`'s `_HAND_STAMPED_GENERATED_KINDS` never settles a refresh conflict there by taking trunk's side. Every other declared generated artifact stays trunk-only. concurrency-restructure §5.2 and §5.3 name the exception and link to that one statement. The byte-budget-guard row for PROCESS_OPTIONS.md is re-stamped (+347 bytes). RESYNC_PACK carries a prose-correction entry (D-002 reversed D-001 after Sol's round-1 MAJOR). Codex 6.1 Sol: two rounds, the second SOUND (`29c20bec`). Decisions: `docs/decisions/wi-839.toml`.

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
