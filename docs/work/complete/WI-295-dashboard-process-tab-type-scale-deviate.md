+++
id = "WI-295"
title = "Dashboard Process-tab type scale deviates (117-CRITIQUE U1) - the icicle, dag, SW and knowledge emitters all label nodes from the shared --nlabel:10px / --nsub:8.5px tokens, but the Process 'working loops' SVG uses ad-hoc 12px/9.5px/13px (`.stgt`/`.stgn`/`.hooplab`/`.hubname`) - a per-view deviation for the same node-label role (1280px-light-process-full.png vs 1280px-light-sw-full.png). Fix: reuse the shared node-label tokens, or add ONE documented scale step if the loops genuinely need a larger size. Contributes to WI-272's block - SR-053 APPROVE requires U1 to pass. MECHANIZE (OI-9): ship a check that every node-label selector resolves to the shared --nlabel/--nsub tokens (or to a documented, enumerated scale step). That check owns U1. | WI-300 (f) OBLIGATION (2026-07-25 ruling): this row now CLOSES BY BINDING its anchor - land the fix, the test that owns the anchor, AND the child LLR+TC rows naming that test in Evidence, in the SAME commit. A child row cannot land ahead of its test: Draft exempts it from --require-verified but derive_gate returns G0 for a draft, dropping the gate off G3. When the last mechanizable anchor under an SR is bound, retire the coarse LLR/TC and flip that SR to Verification=Test - tests first, flip second, never the reverse."
workstream = "dashboard"
sr_refs = ["SR-053"]
buildtier = "medium"
safety_class = "ordinary"
order = 292
+++

## Deliverable

gen_trajectory.py: Process tab's .stgt/.stgn reuse the shared --nlabel/--nsub tokens; .hooplab/.hubname take one new documented --nhead scale step instead of independently drifting 13px magic numbers. LLR-104/TC-107 bind the U1 core.
