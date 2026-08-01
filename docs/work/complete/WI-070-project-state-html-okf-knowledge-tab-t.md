+++
id = "WI-070"
title = "PROJECT_STATE.html OKF knowledge tab - the first real consumer"
workstream = "scripts"
sr_refs = ["SR-038", "SR-042"]
needs = ["WI-034", "WI-039"]
order = 68
+++

## Deliverable

C4 (2026-07-11): the dashboard becomes docs/okf's first real consumer. gen_trajectory gains a stdlib OKF loader (_okf_frontmatter/_okf_nodes, DUPLICATED per the F5 small-loader rule - not a gen_okf import) that walks docs/okf/<tier>/*.md, parses the JSON-scalar frontmatter (type/title/description/resource) + the '- Label: [id](href)' link lists into typed nodes + tier-oriented spine edges, skips index.md/UPSTREAM.md, never reads the GENERATED banner as content, and skips a malformed file with a stderr warn (never crashes). New Knowledge tab (know_graph/_know_panel): the concept graph laid out server-side by the WI-DAG layouter (_dag_ranks + _reorder), nodes fill-keyed by OKF type, hover-highlight + click-to-detail reusing the vanilla-JS idiom; the detail panel embeds each concept's description and links out to docs/okf/<tier>/<id>.md (middle-path embedding, ruling #15). Fully self-contained in the conditional panel (its own style + inline script + embedded data), so a bundle-less repo renders byte-identically (proven by a round-trip test) and there is no new --check exclusion. Pre-commit hook reordered: okf freshness (now step 1b) reported before the dashboard's (1c) since the dashboard consumes the bundle; regen order arch-map -> okf -> trajectory documented in PROCESS_OPTIONS + ADOPTING + both READMEs. Spine: SR-038 Requirement+AcceptanceCriteria + SR-042 Rationale (no-consumer finding resolved) + LLR-035/TC-038 text extended (rides the pending G3 re-attestation). Meta dashboard 214,667 -> 394,909 B (+180 KB; the 219-concept bundle's embedded descriptions). Tests in test_gen_trajectory.py (renders-from-bundle, omitted+byte-identical, deterministic, --check stable, banner-never-rendered, malformed-skipped-with-warn, meta-bundle smoke).
