+++
id = "WI-153"
title = "Knowledge ref integrity - trace.py warn-first Knowledge resolution + knowledge->component coupling warn + fixtures"
workstream = "scripts"
needs = ["WI-152"]
buildtier = "medium"
order = 152
+++

## Deliverable

trace.py resolves a CMP Knowledge cell's docs/knowledge/<label> refs to real pack files as a warn-only advisory (a missing pack never gates - not even under --strict; .md suffix optional; skill names + URLs in the same cell left unchecked), surfaced in the report (### Knowledge-pack advisories), on stdout, and in the summary line (knowledge-advisories=N). check_trajectory.component_findings gains the knowledge->component coupling (owner-ruled 2026-07-14): once docs/knowledge/ holds a real pack (any *.md but the README index), an uncontained arch-map module is a finding regardless of the 10-item top-view bound - WARN plain, ERROR under --strict (G2+) - reusing the existing Component-tag join (no new join) + the docs/components-check opt-out, and dormant (zero cost to a non-adopter) until a pack exists. Tests: 5 trace Knowledge-ref cases (test_components_registry.py) + 7 coupling cases (test_trajectory.py). Meta spine unaffected - coupling dormant (docs/knowledge empty) and the kit's CMP Knowledge cells are skill names, so no advisories; full suite 799 passed / 3 skipped.
