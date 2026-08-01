+++
id = "WI-090"
title = "SN maturity - section-as-state + reader"
workstream = "scripts"
needs = ["WI-089"]
order = 89
+++

## Deliverable

SN maturity is now section-as-state (spec §4a decision (a)): a stakeholder-needs.md heading whose text contains `draft` (e.g. `## Draft needs (unratified)`) marks the SNs under it Draft/unratified (G0); SNs under any other heading are ratified (G1). No new column - the section IS the state, ratification date git-derived (the commit that moves a row up). trace.py gains sn_draft_ids(text) (line-scans headings, excludes -000) and exempts Draft SNs from the SN-with-no-SR orphan rule; draft SNs join the drafts=N count + the Draft-artifacts report section, and build_forest/mermaid_graph flag them like a Status=Draft row (threaded sn_draft, default-empty = never-breaking). check_docs._registry_needs exempts draft-section SNs from the Must/Should README-coverage floor (existence still holds). stakeholder-needs.template.md documents the convention + ships a `## Draft needs (unratified)` section (fresh scaffold stays vacuous - no SN ids under it). Tests: test_trace.py (SN exempt + ratify-to-orphan, sn_draft_ids reader) + test_check_docs.py (registry_needs draft exemption unit + end-to-end).
