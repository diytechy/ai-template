+++
id = "WI-364"
title = "An LLR citing a superseded SR must red as an integrity ERROR, not a warn (owner ruling 2026-07-29: the registry is the live surface; supersession history lives in git). trace.py's SupersededBy validation (sr_supersession_findings, on the --strict-integrity floor) checks only the SR link graph — nothing shipped stops a live LLR from staying grounded on a dead SR; today that guarantee is this repo's pinning tests only, so a downstream adopter gets no guard. Add the LLR SR-Refs rule to the integrity floor; TC citations stay LEGAL (the TC-099/TC-133 evidence-map pattern requires them — a non-draft superseded SR still owes a TC); registries without the optional column are untouched. Pin both directions in tests/test_trace.py; this repo's registries are already clean under the new check. Spec: docs/specs/WI-364.md (row re-affirmed 2026-07-29 against the spec's keep-ruling note: the superseded rows stay)."
workstream = "scripts"
specref = "docs/specs/WI-364.md"
buildtier = "quick"
priority = 2
safety_class = "ordinary"
+++
