+++
id = "WI-142"
title = "[v3] dev slice: Process tab intake + human-decision loops"
workstream = "dashboard"
sr_refs = ["SR-070"]
needs = ["WI-135", "WI-145"]
order = 141
+++

## Deliverable

Added Process-tab Panel 4 (SR-055): the two circular working loops as linked flow panels via a new gen_trajectory._loop_panel(root) — (A) intake: owner/agent intake -> triage into WIs -> resume loop (docs/next-wi) -> build/review -> merge; (B) human-decision: open-items population incl. the gate-ratification table -> human review/ruling -> log Decisions -> merge - sharing one LLM_Agent entry node rendered once. Each stage links to its canonical home (status.md/work-items.csv/next-wi/open-items.md/log.md) when present, else plain text so every emitted href resolves; the loop structure carries no repo data, so it renders byte-identically regardless of the registries. Reuses the existing .pflow chip idiom + a .loop wrap-back marker. SR-055/LLR-056/TC-056 Planned->Verified (v3 stays G2 until WI-143/144). 4 TC-056 tests in test_gen_trajectory.py.
