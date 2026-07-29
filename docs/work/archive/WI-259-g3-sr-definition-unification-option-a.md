+++
id = "WI-259"
title = "G3-SR definition unification, Option A (owner ruling 2026-07-21): widen trace.py --require-verified to demand Status=Verified for EVERY ratified (non-Draft, in-phase) SR regardless of Verification method - matching derive_gate.sr_gate, which already requires Verified for all SRs before deriving G3 (repo-review-2026-07-21 M-5). Record the ruling in the derived-gate model doc, pin the trace/derive_gate pair in test_rule_sync, keep the attested-vs-mechanized report split so non-Test Verified claims stay auditable. BUILD DOUBLE-CHECK (code-verified 2026-07-21): the report split (trace.py:1483-1492) is binary - Attest=attested, EVERYTHING ELSE=mechanized - so once non-Test methods become gate-required, Demonstration/Analysis/Inspection Verified SRs count as ''mechanized'' though they rest on human observation, overstating how much of the project rests on runnable checks. Refine the split (3-way: Test=mechanized, Attest=attested, other=demonstrated/observed) or relabel, so the audit surface stays honest under the widened criterion. Downstream migration flag: repos passing --require-verified today with non-Test SRs still Implemented will start failing - note in ADOPTING/resync guidance"
workstream = "scripts"
sr_refs = ["SR-049"]
buildtier = "medium"
safety_class = "ordinary"
order = 256
+++

## Deliverable

trace.py --require-verified widened to method-blind (Verified required for every ratified in-phase SR of any method, matching derive_gate.sr_gate); verification-basis report now 3-way (Test=mechanized / Demonstration-Manual-Analysis-Inspection-Critique=demonstrated-observed / Attest=attested); parity pinned in test_rule_sync driving the loop. Adversarial REVIEW-A APPROVE f=2 (both MINOR, applied).
