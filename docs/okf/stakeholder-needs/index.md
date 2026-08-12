---
type: "Index"
title: "stakeholder-needs"
description: "tier index"
tags: []
resource: "generated"
---
> **GENERATED — a reference copy, not the source of truth.** Derived from docs/requirements/stakeholder-needs.toml by scripts/gen_okf.py; edit the registry/doc, then rerun it (docs/process.toml [checks] okf_export = false silences the layer).

# stakeholder-needs — index

| id | summary |
|---|---|
| [SN-001](SN-001.md) | A team can drop the kit into a new or existing repo and get a working gated, requirement-… |
| [SN-002](SN-002.md) | The trace from need → requirement → design → test is mechanically verified, not manually … |
| [SN-003](SN-003.md) | The kit is stack-agnostic — a non-Python project uses it by re-pointing the harness at th… |
| [SN-004](SN-004.md) | Progress advances only through explicit approval gates (G1→G2→G3→…), and a gate passes on… |
| [SN-005](SN-005.md) | AI agents and humans work from the same playbook, with the process enforced agent-neutral… |
| [SN-006](SN-006.md) | An agent can run unattended and resume from repo text alone; such a run never blocks on a… |
| [SN-007](SN-007.md) | The kit's own changes stay traceable and tested — a change to a script is covered by a te… |
| [SN-008](SN-008.md) | Gates are honest — a green never hides a skipped check, a stub, or an unmet criterion. |
| [SN-009](SN-009.md) | A committed secret or private identity is caught before it publishes, in every repo, with… |
| [SN-010](SN-010.md) | Documentation stays navigable and honest — links resolve, the vision is declared once, an… |
| [SN-011](SN-011.md) | The kit's scripts run on a clean Python 3.11+ with minimal, argued dependencies — stdlib … |
| [SN-012](SN-012.md) | The process is right-sized, not ceremony for its own sake — small changes stay cheap, and… |
| [SN-013](SN-013.md) | No Python 3 interpreter on PATH (or the Windows Store alias that resolves but exits nonze… |
| [SN-014](SN-014.md) | A required harness tool is absent |
| [SN-015](SN-015.md) | The working directory is not a git repository |
| [SN-016](SN-016.md) | An unattended run must never block on a prompt at launch or mid-run |
| [SN-017](SN-017.md) | The coordinator is killed / power-lost mid-session |
| [SN-018](SN-018.md) | A second coordinator is launched in the same checkout |
| [SN-019](SN-019.md) | A repo with no commits yet (HEAD absent) |
| [SN-020](SN-020.md) | The agent CLI / model errors before doing work (retired model, expired auth) |
| [SN-021](SN-021.md) | A generated artifact (arch map, trace view) drifts from its source |
| [SN-022](SN-022.md) | A committed example row / placeholder is left in a registry at a gate |
| [SN-023](SN-023.md) | A reviewer can see the project's progress and how its parts connect from one dashboard-li… |
| [SN-024](SN-024.md) | Subjective/perceptual acceptance — a realistic-looking render, an artifact comparison wit… |
| [SN-025](SN-025.md) | A single command from the repo root (agent-resume) lets a configured LLM agent implement … |
| [SN-026](SN-026.md) | Several LLM families are configurable — selected per job and per capability level — and w… |
| [SN-027](SN-027.md) | Ready work fans out across bounded parallel lanes, while mutation of the integration bran… |
| [SN-028](SN-028.md) | Every policy dial has one home — a single hand-edited, machine-read file — and a repo tha… |
| [SN-029](SN-029.md) | An autonomous run gets as far as it honestly can. Once triggered, the coordinator stops f… |
