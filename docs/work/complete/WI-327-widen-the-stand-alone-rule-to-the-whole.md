+++
id = "WI-327"
title = "Widen the stand-alone rule to the WHOLE spine and GATE it (owner ruling 2026-07-27, raised at the first re-attestation sitting): the rule shipped SR-only and warn-only, and the owner found LLR-050 carrying a `WI-316:` changelog prefix that no checker watched. Measured before acting: 2 SRs carried a WI id in normative text - the scope the lint had - while 26 LLRs, 8 TCs and 9 more SR Title/Rationale cells did too, none of them watched, and the largest pocket was the layer the rule could not see. It also kept GROWING while the rule was green: three of the dirty rows were written the same week the lint landed, by the agent that wrote the lint."
workstream = "docs"
needs = ["WI-321"]
buildtier = "medium"
safety_class = "ordinary"
order = 324
+++

## Deliverable

provenance_findings replaces standalone_sr_advisories: every normative cell of all three spine registries (SR Title/Requirement/Rationale/AcceptanceCriteria, LLR Title/Detail, TC Method/Expected/Parameters), flagging a WI id or a process-doc citation, GATING under --strict via exit_code rather than warning. Pointer columns (Module, CodeSymbol, TestRefs, Evidence) are out of scope by design - they exist to point - and the negative half of the test carries the reason the rule stays narrow: a script name, an artifact path and a rubric are NOT provenance, because this kit's product IS its scripts. The whole population was cleaned in the same pass: 48 cells across 44 rows, mechanism preserved verbatim, provenance dropped, zero residue - so the rule guards zero-to-zero instead of dictating a cleanup schedule. 42 rows flipped Verified -> Modified (the 3 already Modified stayed), landing in the sitting already open. Proven to bite by reintroducing the owner's own example: LLR-050's WI-316 prefix fails --strict at exit 1. KNOWN COST accepted: a WI id is forbidden even where it is DATA (a row naming a rendered dashboard node); the one occurrence was reworded and the id kept in the log, because an exemption a checker cannot distinguish from the defect is one an author can reach for.
