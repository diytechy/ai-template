+++
id = "WI-313"
title = "Bind A1/A3/A4 so SR-052 can flip to Verification=Test - WI-300's option (f) applied to the accessibility rubric, the same job SR-053 completed 2026-07-26. A2 is already bound (LLR-101/TC-104 + LLR-108/TC-113); A1, A3 and A4 are UNDECOMPOSED and still ride the coarse LLR-053/TC-053. Note the distinction that cost a false start: clearing a residue clause is not the same as binding an anchor. Measured 2026-07-26 - A1's structural half already passes (0 interaction hooks lack tabindex; 2 <details> without <summary> want a look), A3 is 4/4 status + 4/4 tier + 6/6 type + 8/8 phase explained once CSS tokens are resolved with one open question (sw-node component #44403c, which is not painted as a node fill at all), and A4 already has SIX owning tests so the work is mostly binding plus checking the pair set is closed. Resumption guide with the method, the measurements and the hazards: docs/specs/WI-300-sr052-binding.md."
workstream = "docs"
sr_refs = ["SR-052"]
needs = ["~WI-300"]
buildtier = "strong"
priority = 1
safety_class = "protected"
order = 310
+++

## Deliverable

A1/A3/A4 bound and SR-052 flipped to Verification=Test, per the spec's done-when. A1 -> LLR-112/TC-117 (wired-selector closure DERIVED from the emitted JS's own querySelectorAll calls + the no-positive-tabindex order rule; the '2 <details> without <summary>' claim resolved as a measurement artifact - prose inside the embedded JSON, zero <details> in the markup). A3 -> LLR-113/TC-118 (every painted vocabulary member resolves to a worded legend swatch in the same document, tokens resolved; the #44403c question resolved OUT of scope - it paints only as the JS detail-badge background whose own visible text names the concept). A4 -> LLR-114/TC-119 (the six existing floor tests bound + the set closed by reflection). Measure-first found TWO live A3 defects the handoff's document-wide scan missed: the What-tab tier legend hardcoded a stale TC swatch (#047857, by then STATUS_FILL[done]) - now derived from TIER_FILL and pinned as a bijection - and the flat How-SW seam graph had NO legend for its kind-by-fill encoding (only the drill did). Five guard-bites mutation proofs, each restored byte-identical; the two A3 defects were caught live by the new tests before their fixes existed. LLR-053/TC-053 superseded; rubric retired with the anchor->LLR/TC map; perceptual-stale names SR-054 only. Spec archived to docs/archive/specs/.
