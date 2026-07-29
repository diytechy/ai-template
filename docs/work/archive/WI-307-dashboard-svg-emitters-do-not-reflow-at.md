+++
id = "WI-307"
title = "Dashboard SVG emitters do not reflow at their declared viewport widths (119-CRITIQUE T7) - two independent instances: at 390px the How-SW module graph is sliced mid-label at the viewport edge (CMP-002 reads 'CMP...') forcing a sideways scroll; at the desktop 1280px width the What icicle's TC lane is clipped at the card's right edge and fades out, a fit failure at a DESKTOP width, not just mobile. The 390px above-the-fold landing is clean (cards reflow, nothing clipped), so the fault is specific to the SVG emitters, not the page layout. Fix: make the SVG viewBox responsive (scale-to-fit or re-layout under a width threshold) so narrow/wide content reflows; keep the sideways-scroll hint only as a fallback for content that genuinely cannot fit. Re-affirmed 2026-07-26 against the amended SR-054 (the T1/T3 ruling touches T1 and T3 only; T7 stays a live critique anchor and this defect is unaffected)."
workstream = "dashboard"
sr_refs = ["SR-054"]
buildtier = "medium"
safety_class = "ordinary"
order = 304
+++

## Deliverable

Delivered 2026-07-26. Every emitted SVG now scales to fit its container (width:100% + max-width:<natural> + min-width:<natural x SHRINK_FLOOR>) instead of pinning a FIXED pixel width - the reason a viewBox alone never fixed it. Applied in the three shared wrappers, so 73 emitted SVGs are responsive and ZERO keep a bare fixed width. The floor is load-bearing: pure scale-to-fit trades T7 for T4 (a 900px graph in 390px shrinks a 12px label past readable), so shrinking stops at 62% and the existing scroll + cue take over - the row's own fallback rule made mechanical. RESIDUE STATED: a view whose natural width exceeds 390 / 0.62 still scrolls at 390px with its cue; closing that needs a narrow-width re-layout (stacked columns), a larger change than this row scopes. Bound as LLR-116/TC-121 (T7 leaves the critique; live anchors now T2, T4, T5, T6, T8). Guards derive every svg from the emitted document, so a fourth emitter cannot skip the rule. Ratchet re-stamped 5156->5186.
