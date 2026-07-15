# Agent routing and heterogeneous review

This pack distills the evidence behind the unattended loop's routing choices.
The implemented behavior remains authoritative in [CMP-004](../requirements/components.csv)
and its linked requirements; the full historical research input is
[archived](../archive/AGENT_ROUTING_RESEARCH.md).

## Findings retained

- Independent, family-disjoint review is a useful defense against self-preference
  and correlated blind spots. Keep the reviewer fresh and do not reveal the
  implementer's self-assessment.
- Review value is better measured by specific, change-triggering findings than
  by finding count or prose length. Confident false findings are a material
  failure mode, so corroboration and diff-grounding matter.
- At this repo's sample size, a declared, legible escalation rule is more
  auditable than a learned router. Escalation is useful for model-specific
  failure; repeated cross-family failure points toward an ambiguous or hard
  problem that should be surfaced.
- Provider CLIs share the useful abstraction "command in, artifact out" while
  their flags and catalogs move. Store commands and tier assignments in repo
  data; do not vendor a model catalog without a real consumer.

## Evidence trail

The archived survey links the underlying papers and provider documentation and
records its 2026-07-10 retrieval context. It also flags practitioner reports and
single-preprint findings rather than promoting them to settled rules. Re-check
the external sources there before changing routing policy; model and CLI facts
are time-sensitive.

## Failed or bounded approaches

- Counting findings rewards verbosity and false positives.
- Same-session self-review is not an independent review.
- Multi-agent debate adds machinery without established advantage over
  independent parallel review at equal compute.
- A learned router needs more observations than one project normally produces.
