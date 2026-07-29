+++
id = "WI-093"
title = "Phase derivation + [phase]-[g*] archetype"
workstream = "scripts"
needs = ["WI-091"]
order = 92
+++

## Deliverable

check_trajectory.py learns the phase archetype (spec §7/§9.3): a phase's pre-dev batch is a WI whose Title carries a `[<phase>]-[g<N>]` tag (g1 requirement-structuring, g2 decomposition+TCs). phase_anchors() parses them + warns on a duplicate (phase,gate) and a g2 anchor omitting its g1 predecessor. The phase-DROP detector reads the derived per-phase levels from docs/gate's `# basis:` line (read_derived_phases, the hybrid cache - no recompute; a shared format contract with derive_gate.basis_line): for each phase with a done `[phase]-[gN]` anchor recording its closed level, if the current derived level fell below N (new/reopened content), it warns to open a new phase-gate WI. All WARN-FIRST (never an exit-code change, the connectivity-coverage precedent), vacuous on a single-phase repo with no anchors (the meta) or a legacy docs/gate with no basis line. derive_gate._per_phase now reports the RAW per-phase min (unfloored, can read G0) so a phase's drop is visible in the cache. No spine change. Tests: test_trajectory.py (anchor parse+duplicate, g2-without-g1 warn, read_derived_phases, drop-detector warns+clears, vacuous-without-anchors).
