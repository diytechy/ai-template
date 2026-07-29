+++
id = "WI-132"
title = "status-surface lint in check_docs - budget, order, OI coherence (warn-tier)"
workstream = "scripts"
needs = ["WI-131"]
order = 131
+++

## Deliverable

WI-132 (2026-07-13, open-items-surface slice 3 - phase close): the status-surface lint. check_docs.check_status_surface() - S-1 line budget (default 120; docs/status-lint run-phase-idiom policy file: integer override or off disabling S-1..S-3); S-2 the Open-items marker must precede ## Scope (plus Scope-with-no-marker); S-3 OI coherence with docs/open-items.md (every Needs-<human> OI-N token - best-effort block extraction over the template shape, bullet-indent or heading scoped - has a ## OI-N section; every section id appears in status.md; vacuous when open-items.md is absent). ALL warn-only - never the exit code (WI-129 stance; the module docstring + the spec record gate-promotion as the un-defer trigger for a spine SR). PROCESS_OPTIONS 'Trajectory / work-items layer' gains the owner-decision-surface block (the one home). Tests (test_check_docs.py, 6 new): scaffold-clean zero S-warnings, budget-warn-exit-0, policy override + off, order + missing-marker, coherence both directions incl. in-flight-needs-no-brief, vacuous-absent. Meta dogfood: this repo's own status.md + open-items.md pass S-1..S-3 with zero warnings.
