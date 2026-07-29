+++
id = "WI-161"
title = "Per-phase model preference knob (AGENT_PREFER_MAP - within-tier only)"
workstream = "unattended"
needs = ["WI-059", "WI-160"]
buildtier = "medium"
order = 160
+++

## Deliverable

Shipped AGENT_PREFER_MAP/--prefer-map with managed-routing preflight validation and within-tier-only selection: preferred, enabled, available ids lead the enable-list order; unknown/cooling/wrong-tier ids fall through; reviewer/critic family heterogeneity still wins. Added launcher/template slots and routing docs, restored the meta enable list to Fable-first while BUILD prefers OPENAI-SOL, and covered selection + end-to-end dispatch. No spine change.
