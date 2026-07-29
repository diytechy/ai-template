+++
id = "WI-270"
title = "Reconcile the Python-floor requirement spine to 3.11 (SN-011/SR-034/SR-035 + architecture.md + SR-035 CI-matrix narrative; catch up to WI-262)"
workstream = "docs"
sr_refs = ["SR-034", "SR-035"]
needs = ["~WI-262"]
buildtier = "strong"
safety_class = "spine"
order = 267
+++

## Deliverable

Requirement spine reconciled to the shipped 3.11 floor (text + re-attestation, no code): SN-011 / SR-034 / SR-035 / TC-035 + architecture.md + status.md Scope + the WI-064 build-note moved 3.8 -> 3.11. SR-035's AC narrative rewritten to match test.yml's actual matrix (ubuntu/windows/macos x {3.11,3.x}, macOS+3.11 excluded as a redundant-coverage call per M-27, NOT arm64-availability - 3.11 has arm64 macOS builds). SR-034 (AST-scan AC, version-agnostic) and SR-035 (verified by TC-035 -> test.yml) stay Verified; spine counts unchanged (SN=25 SR=109 LLR=97 TC=100), derived gate G3. check.py --gate G3 RESULT: PASS (1368 passed, cov 91.53%). Adversarial 114-REVIEW-A APPROVE f=1 (one MINOR: inverted spec prose fixed before archiving; the shipped SR-035 AC was already correct).
