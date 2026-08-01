+++
id = "WI-095"
title = "Process-doc rewrite (derived gate; parallel/series)"
workstream = "docs"
needs = ["WI-092", "WI-093", "WI-094"]
order = 94
+++

## Deliverable

Process docs rewritten for the derived gate (spec §10.7). PROCESS_OPTIONS gains a new '## Derived gate model' section (the working summary: the gate is computed from artifact states + cached; the Draft/Planned/Verified + SN section-as-state ladder; Draft artifacts live in the live spine, retiring the -000/off-spine workaround; ratification = a reviewed Status-change commit composing with the gate-authority levels; phase = a derived drop detector + a committed [phase]-[g*] anchor; the parallel-pre-dev/series-dev workflow with the picture). 'Phased delivery' reconciled: the 'already at G3 takes on new scope' bullet now enters new scope as Draft SN/SR in the live spine (the -000/off-spine language retired), the derived per-phase gate drops (the phase signal), and --phase still closes the shipped set; the section 'Builds on' the new model. The autonomous gate-authority step's 'driver bumps docs/gate' -> 'makes the ratifying Status-change commit + regenerates docs/gate'. PROCESS.md (core, byte-budgeted) got the minimal mechanism edits: §4's active-gate line + §7's active-gate paragraph rewritten to derived+ratification, and derive_gate.py added to §7's process-check list. FLAGGED byte growth: PROCESS.md 58,853 -> 59,638 (+785 B) - core (not opt-in) derived-gate mechanism; the bulk went to unbudgeted PROCESS_OPTIONS; baseline re-stamped 59,638 in byte-budget-guard (source + .claude + .agents). The PROCESS_OPTIONS->spec reference is a NON-link (the design spec is a meta-only artifact; a markdown link broke the scaffolded doc-nav - caught by the scaffold tests, fixed). No spine change. Docs only; caught+fixed a shipped-doc broken link via the profile/scaffold tests.
