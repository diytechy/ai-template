+++
id = "WI-194"
title = "Dual-plan round state machine - pure side-effect-free round-lifecycle library (plan/coverage/critique/revision/arbiter-x2/verdict) with typed step outcomes + hard caps + round-budget ledger mapping to gate-policy (DP-001 selected plan P1)"
workstream = "unattended"
needs = ["WI-190"]
buildtier = "strong"
order = 190
+++

## Deliverable

WI-194 (2026-07-16, fable): scripts/plan_round.py - the pure round-lifecycle library (schedule.py shape: never launches/writes; JSON-able state, crash-resumable). ready_steps() offers parallel-friendly typed steps (PLAN/COVERAGE/REPAIR/CRITIQUE/REVISE/ARBITER); record() enforces the caps as RoundCapError (one critique round ever, one revision each only against CHANGES-REQUESTED, one coverage repair per implicated plan per stage - coverage findings NAME the implicated plans, repeat findings PAGE), a session-budget ledger (default 10 = happy-path 8 + two legal repairs), the arbiter x2 position-swap agreement rule (disagreement pages position-unstable), page_action() maps PAGE to gate-policy failure semantics failing safe to attended; APPROVE-only critiques skip revision+coverage2. 16 unit tests vs injected fake results + a walk CLI. Spine LLR-070/TC-070 under SR-061 (provisional pending the structuring WI); Proposed IF-058 (source; nearest IF-053), CMP-004; scaffolded; 2 F5 census pairs.
