+++
id = "WI-300"
title = "Critique/test boundary - RULED 2026-07-25 as option (f): decompose the LLR/TC layer so each mechanizable rubric anchor becomes a child LLR bound to a TC with Automated=Yes, and an SR keeps Verification=Critique only while a perceptual child remains under it. LLR-053/054/055 each near-verbatim restate their SR (a paraphrase, not a decomposition), which is why a train had to pass the whole rubric - the gate-shape debate was the symptom. Per-anchor pass in docs/specs/WI-300.md: 13 of 17 mechanize and the perceptual residue is entirely inside SR-054, so SR-052 and SR-053 flip to Verification=Test and all seven queued/blocked render rows stop owing a CRITIQUE dispatch. HARD SEQUENCING: land every child TC with real Evidence BEFORE flipping an SR's Verification, never the reverse. Ruling + alternatives passed over: docs/log.md Decisions 2026-07-25. | RE-AFFIRMED 2026-07-25 after slice 1: the anchors are already largely TESTED - what was missing is the registry binding - so the remaining work is mostly decomposition, gated not by test-authoring but by the OPEN DEFECTS on WI-292/294/295/299. Adversarial review of the first binding (WI-297) refuted it: LLR/TC scope must state what is PROVEN, never 'the whole document', because trace.py can confirm a TC exists and names tests but cannot tell that its Evidence describes the artifact wrongly."
workstream = "process"
buildtier = "strong"
priority = 1
safety_class = "spine"
order = 297
+++

## Deliverable

Option (f) delivered end to end. SR-053 flipped 2026-07-26 (five U-anchors bound); SR-052 flipped 2026-07-26 after WI-313 bound A1/A3/A4 (A2 was already LLR-101/TC-104 + LLR-108/TC-113), its coarse LLR-053/TC-053 superseded and docs/rubrics/dashboard-accessibility.md retired to a record with an anchor->LLR/TC map. perceptual-stale now names SR-054 ONLY - the ruling's central claim (an SR drops out of _load_critique_srs on its own when its last perceptual child leaves) demonstrated twice with no gate change and no checker edit. SR-054 keeps Verification=Critique BY DESIGN: its residue (T1 entry-point-obvious, T3 stays-oriented, plus the T2/T3/T5 residue rows LLR-099/100/105) describes a reader's experience, and whether to retire critiques outright - or mechanize T4/T7 with a browser harness - is an owner decision the WI-300 spec deliberately leaves UNFILED (spec section 6): do not quietly mechanize reader-experience clauses into proxies to green a gate. Spec archived to docs/archive/specs/.
