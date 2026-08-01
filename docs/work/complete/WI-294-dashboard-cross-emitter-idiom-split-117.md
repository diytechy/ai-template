+++
id = "WI-294"
title = "Dashboard cross-emitter idiom split (117-CRITIQUE U3) - two 'same concept rendered two ways' defects. (a) The hover-highlight ring is #f59e0b amber in the icicle (`#ice .cell.hl rect`) but var(--accent) indigo in every drill emitter (`.drill .block.hl rect`), so the same hovered-node concept differs between the What tab and the When/How/Knowledge tabs. (b) The When tab's phase key renders inline in the explainer as .55rem/2px-radius `span.ph` chips, while the status key on that same tab and the tier/type keys on What/How/Knowledge render as `.legend` rows of .8rem/3px-radius swatches. Fix: one shared highlight token across all SVG emitters, and render the phase key through the shared `.legend` component. Contributes to WI-272's block - SR-053 APPROVE requires U3 to pass, not just U5. MECHANIZE (OI-9): ship a cross-emitter token-equality check - the hover/highlight ring must resolve to ONE token across every SVG emitter, and each legend must render through the shared component. That check owns U3. | WI-300 (f) OBLIGATION (2026-07-25 ruling): this row now CLOSES BY BINDING its anchor - land the fix, the test that owns the anchor, AND the child LLR+TC rows naming that test in Evidence, in the SAME commit. A child row cannot land ahead of its test: Draft exempts it from --require-verified but derive_gate returns G0 for a draft, dropping the gate off G3. When the last mechanizable anchor under an SR is bound, retire the coarse LLR/TC and flip that SR to Verification=Test - tests first, flip second, never the reverse."
workstream = "dashboard"
sr_refs = ["SR-053"]
buildtier = "medium"
safety_class = "ordinary"
order = 291
+++

## Deliverable

gen_trajectory.py: hover/focus ring across every SVG emitter (drill/icicle/flat-DAG/knowledge) now resolves to one shared per-node --ring custom property (_ring_ink/_ring_style), replacing the var(--accent)-vs-#f59e0b split; the When tab's phase-accent legend now renders through the shared .legend/<i> component instead of its own span.ph/phaselegend idiom. LLR-103/TC-106 bind the U3 core.
