+++
id = "WI-139"
title = "Review 017 remediation - llr_exempt predicate pinned across trace/derive_gate"
workstream = "scripts"
needs = ["WI-099"]
order = 138
+++

## Deliverable

WI-139 (2026-07-14, review 017's MAJOR, driver-remediated - the round predates the batch loop's remediation path and was left dangling): trace.py's orphan rule read the Verification cell raw while derive_gate.sr_gate stripped it, so a whitespace-padded valid method (e.g. 'Analysis ' ) was LLR-exempt in the derived gate but orphaned in the trace report - the exact orphan-report/derived-gate disagreement WI-099 promised away (test_rule_sync pinned only LLR_EXEMPT set-equality, not the decision itself). Fix per the finding: the decision named once per file as an F5-duplicated llr_exempt(row) predicate (stripped-cell match - the is_draft/is_verified pattern from WI-101), routed at BOTH decision points (trace orphan loop, derive_gate.sr_gate); new test_rule_sync::test_llr_exempt_agrees pins the predicates equivalent across a padded/case/empty/None battery AND pins the padded case to the fixed direction (exempt in both). Closed vocab stays case-sensitive ('analysis' non-exempt in both - Status casing was WI-101's scope, Verification is not Status). arch-map regenerated (+2 detail lines). No spine change; derived gate value unchanged (the meta spine carries unpadded methods).
