+++
id = "WI-088"
title = "Derived gate model (replace monolithic gate) - design"
workstream = "scripts"
needs = ["WI-008", "WI-053"]
order = 87
+++

## Deliverable

Owner-ratified design (2026-07-12): docs/specs/derived-gate-model.md replaces the monolithic declared gate with a derived one - repo/phase gate computed from artifact states (Status + decomposition level), cached to docs/gate with a compute date (hybrid; --check guards rot); no new column (open-vocab Status gains Draft, ratification date git-derived); SN maturity = section-as-state; ratification = a reviewed Status-change commit (an agent may make it, gate-policy governs who); phase = derived-gate-drop detector + committed [phase]-[g*] anchor for identity/membership; parallel requirement structuring per phase then series per-WI dev; draft artifacts exempt from trace's orphan rule (retires the -000/off-spine workaround). Implementation filed as WI-089..096 (spec sec 10).
