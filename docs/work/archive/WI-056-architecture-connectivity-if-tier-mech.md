+++
id = "WI-056"
title = "Architecture connectivity - IF tier mechanize + graph views"
workstream = "scripts"
sr_refs = ["SR-044"]
needs = ["WI-006", "WI-012", "WI-031"]
order = 55
+++

## Deliverable

S5 (2026-07-11): architecture-connectivity mechanized. trace.py reads the IF-### seam tier (id shape/dup + SR-Refs back-link + a warn-only ThisProject<->LLR.Module endpoint advisory, closing the SR-002-era gap); check_trajectory.py runs warn-first coverage over the arch-map inventory - opt-out/default-on via docs/interfaces-check, so a multi-module map with no seams reads connectivity-undeclared; per-module missing-endpoint/direction (source/sink Notes honesty valve), Active-seam-TC and Contracts-docstring citations, all warn-first (never a gate/hook fail). gen_trajectory renders the How-SW panel as an IF graph reusing the WI-DAG layouter (module/file/external nodes, byte-deterministic; table fallback when no seams); gen_arch_map merges module<->module IF edges + harvests Contracts: docstrings. interfaces.template.csv gains a Notes column (legacy rows read empty). Spine: minted SN-023 (single-dashboard-with-relationships) + SR-044 + LLR-041/042 + TC-044. PROCESS.md 8 widened to intra-repo (+331 B flagged, baseline re-stamped) + PROCESS_OPTIONS section + ADOPTING 6. Rides the pending G3 re-attestation. The meta repo now emits one connectivity-undeclared warn (20 modules, 0 IF rows) - the WI-057 authoring driver.
