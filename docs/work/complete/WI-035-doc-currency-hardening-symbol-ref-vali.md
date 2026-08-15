+++
id = "WI-035"
title = "Doc-currency hardening - symbol-ref validation"
workstream = "scripts"
sr_refs = ["SR-158"]
needs = ["WI-013", "WI-012"]
order = 34
+++

## Deliverable

Thread 49 landed (WI-1.50, 2026-07-10): check_doc_refs.py - path tier (aggressive, shape-bounded) + sym:<module>.<name> tier against the arch-map inventory; warn-first product-layer ([step:doc-refs] opt-in); generated blocks + path-ok exempt; SR-041/LLR-038/TC-041; freshness audit recorded (all generated artifacts carry --check; committed-composites deferred with reasoning); Q1 rider evaluation recorded in the plan entry.
