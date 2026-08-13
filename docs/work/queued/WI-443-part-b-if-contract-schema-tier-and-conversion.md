+++
id = "WI-443"
title = "OI-14 part B program (ruled B1, 2026-08-13): declare the interface contract and build IF's first schema tier, warn-first, then convert interfaces.csv and components.csv to the TOML carrier in the same batch (they have waited on this ruling precisely to convert once). The contract: an IF row is an INTERFACE only — what crosses, typed discrete-vs-variable (a NEW column plus its validation; zero rows carry any typing today) — with a Rationale home added so the why stops squatting in Contract. The schema tier: required fields; closed vocabularies for Stability, for Status (OI-13/D-9 parked IF's Status HERE — rule it in this pass; Stable currently appears in Status and Stability on one row meaning different things), and for the new type; a refusal when a component boundary has an uncovered crossing. The four negative rules, warn-first then promoted to ERROR once the corpus converges: refuse a work-item id in Contract (fires on ~24 percent today), refuse a repo-lock D-n citation (14 rows), warn on rationale connectives (because / rather than / so that / since), warn above a 500-character ceiling (34 rows). Existing cells migrate as rows are touched (B1, not B2 — no bulk rewrite nobody can review). Sequenced after part A because A decides which rows exist."
specref = "docs/requirements/open-items.toml"
workstream = "lock-program"
sr_refs = []
needs = ["WI-441"]
buildtier = "strong"
safety_class = "spine"
priority = 2
+++
