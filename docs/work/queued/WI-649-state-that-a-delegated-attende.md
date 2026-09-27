+++
id = "WI-649"
title = "State once that an attended session acting on the owner's explicit delegation approves on a held rung, and a mechanically triggered session never does"
workstream = "process"
specref = "docs/log.d/2026-09-26-owner-rulings-oi82-oi94.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

OI-86 ruled 2026-09-26: the owner's delegation of a held-rung approval to the attended main session they are directing holds; the `human_approval_through` dial exists to stop a MECHANICALLY TRIGGERED session (the unattended loop, a launcher-spawned worker) approving without the owner's intent. Today the dial's comment in `docs/process.toml`, its shipped template and the gate-advance skill say only "the human approves", and PROCESS.md defines the dial without the distinction, so the phase-6 stand-in's act read as an irregularity (OI-86) when it was the owner's. WI-636's loop-trailer refusal already enforces the mechanical half; this item states the doctrine it enforces.

IN SCOPE: one statement where PROCESS.md defines the dial (byte-budget-guard; push detail to PROCESS_OPTIONS.md if the budget is tight): a held rung's approval is the owner's act, made by the owner or by an attended session acting on the owner's explicit, recorded delegation; the delegation and its scope are recorded in the approving commit or its log entry; a mechanically triggered session never approves on a held rung, and the loop-trailer refusal is the enforcer. Point the dial comment (this repo's and the template's), the gate-advance skill and AGENTS.template.md's approval line at it rather than restating it. NOT IN SCOPE: any change to the dial's values or to the refusal's code.

## Done-when

- PROCESS.md (or PROCESS_OPTIONS.md, linked from PROCESS.md) states the delegation rule once, naming the loop-trailer refusal as its enforcer.
- `docs/process.toml`, the shipped process template and the gate-advance skill point at that statement; `tests/test_dogfood_sync.py` still passes.
- Byte budgets hold (byte-budget-guard reports the deltas), and the commit bar passes.
