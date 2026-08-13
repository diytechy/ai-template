+++
id = "WI-449"
title = "OI-20 execution (ratified as built, 2026-08-13): write the ruled CodeSymbol grammar into the discharge rule's documentation and enforcement — a cell may name a resolvable code symbol, a module path, or a designed PART SOURCE (parametric code authoring a physical part binds like any symbol); a generated artifact or a prose contract is NOT admissible, so the four unfounded rows stay honestly unfounded with their recorded reasons (re-confirm each reason still holds). Make the non-.py skip VISIBLE: a row whose modules are all non-Python currently discharges by DEFAULT, silently — report it per row (skipped-with-reason, never red, never silent), which is the OI-28 guard on template paths ruled admissible in Module cells as realization artifacts. The grammar note also records the ruling's weight: this rule is the decomposition FLOOR (OI-21's ladder rung 4 terminates where a token binds)."
workstream = "lock-program"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "spine"
priority = 2
+++

## Deliverable

Completed 2026-08-13. The ruled CodeSymbol grammar is stated where it binds
(symbol_findings' docstring in check_doc_refs.py) and in the reference doc's
new §4.2: admissible — a resolvable code symbol, a module path, a designed
part source; not admissible — a generated artifact or a prose contract; with
the ruling's weight recorded (the rule is the decomposition floor — OI-21's
rung 4 terminates where a token binds). The four unfounded rows' recorded
reasons were re-verified against live code and ALL HOLD (LLR-015 function
local; LLR-087/088 symbols never existed per git log -S; LLR-112 prose) —
rows honestly unfounded, unedited. The non-.py skip is now VISIBLE: a third
ADVISORY ink (never gates, never hidden) names each row discharging by
default — 5 today (LLR-019/020/021/032/122, hooks and shell templates),
folding to one summary line past 15. Discharge itself unchanged — exit codes
measured identical either side of the diff. Two stale reference-doc claims
corrected (§4 'not checked against real code'; §12.4 marked CLOSED, numbering
stable). Builder totals: full suite 2351 passed / 6 skipped twice on the
final tree; touched modules 231 passed; 5 new tests. Review note: this
slice's adversarial pass rides the next combined codex round — the change is
advisory-ink + docs with measured exit-code invariance, the lightest class
this program carries. One latent flake flagged for a future WI: two
test_traj_views tests read the real repo's architecture.md and are exposed
to concurrent regeneration.
