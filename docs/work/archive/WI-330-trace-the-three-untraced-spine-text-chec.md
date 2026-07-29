+++
id = "WI-330"
title = "Trace the three untraced spine-text checkers (found 2026-07-27 while scoping WI-329; owner ruled clear it BEFORE any re-attest). provenance_findings and form_findings both GATE under --strict, and paraphrase_advisories warns, and all three shipped with no SR, no LLR and no TC. The convention is not a judgement call - ac_advisories, the same kind of thing, has SR-004 -> LLR-004 -> TC-004, one row per lint - so this is a gap, not a design choice. WHY THE HARNESS COULD NOT CATCH IT, worth recording: trace.py reports orphans among rows that EXIST; it has no notion of shipped behaviour with no row at all, because nothing points at the behaviour to begin with. The traceability harness cannot detect untraced work - only a reviewer reading the diff against the spine can, and TWO adversarial reviews of this change (124 and 125-REVIEW-A) missed it because both were scoped to prose fidelity rather than coverage. Registry rows only: no production code changes, because the behaviour already ships and the cited tests already pass."
workstream = "requirements"
needs = ["WI-328"]
buildtier = "quick"
priority = 1
safety_class = "spine"
order = 327
+++

## Deliverable

Three chains on the SR-004/LLR-004/TC-004 shape: SR-126 (spine stand-alone rule, gating) -> LLR-133/provenance_findings -> TC-126; SR-127 (one testable obligation, gating) -> LLR-134/form_findings -> TC-127; SR-128 (paraphrase advisory, warn-only) -> LLR-135/paraphrase_advisories -> TC-128. Each TC cites the pytest NODE ID of a test that already existed and already passed, so the rows describe shipped behaviour rather than promising it - verified by running the three named nodes (3 passed) before filing. ZERO production code changed. New rows land Modified, not Verified: the evidence exists but no human has attested them, and marking them Verified would be the driver signing for the owner. One self-inflicted finding on the way in, recorded because it is a real class: LLR-134's Detail DESCRIBED the no-obligation-keyword rule and therefore tripped it, since the checker cannot distinguish a mention from a use - reworded rather than exempted, on the WI-327 precedent that an exemption a checker cannot see is one an author can reach for. DELIBERATELY NOT DONE: widening trace.py to detect untraced behaviour, which would mean guessing which functions constitute behaviour - a heuristic with a large legitimate majority, the exact failure the provenance rule was measured to avoid. The honest control is review, and the spec records that it failed here twice.
