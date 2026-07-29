+++
id = "WI-176"
title = "Parallel WI dispatch - redesign to a parallel-by-default dispatcher (documentation)"
workstream = "unattended"
needs = ["WI-162"]
buildtier = "strong"
order = 175
+++

## Deliverable

Documentation-only redesign of docs/specs/parallel-wi-dispatch.md from the opt-in --track-lane design (WI-162) to a parallel-by-default dispatcher: WI-DAG scheduling; agent-resume as dispatcher/integrator (--jobs, default 2); traincars (one Build -> one Review, accepted-on-train, no WI done until the train integrates); reconcile->gate->build-out launch sequence; planning-declared AND enforced Exclusive keys + hard edges (dispatcher never invents them; undeclared collision recorded, reconciled without pausing); conflict-triggered focused re-review; atomic CAS integration; git-as-authority crash recovery; {phase}-{gate} train branch naming (docs/run-phase retired, SR Phase + derived-gate untouched); soft-edge audit before the parallel flip; research-informed clustering with EstTokens (no approximation bound claimed). Eight implementation slices A-H specified for filing on ratification. Companion decision log docs/specs/parallel-dispatch-design-notes.md; scheduling survey docs/knowledge/parallel-scheduling.md. Incorporated a Codex review pass (self-inflicted contradictions reconciled).
