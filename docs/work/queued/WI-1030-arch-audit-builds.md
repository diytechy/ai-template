+++
id = "WI-1030"
title = "Checks A and C, and the run menu's audit gains its architecture and hats parts with an independent critique"
workstream = "process"
sr_refs = ["SR-159", "SR-161"]
specref = "docs/plans/2026-10-11-review-churn/README.md#12-architectural-decomposition-encouraged-at-three-moments"
needs = ["WI-1025"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
planmode = "single"
+++

## Context

Variant F's tenth row (F-10), filed on trunk on 2026-11-21 (queue-drill
HANDOFF §3.3). It is item 12's builds, which the plan sequences after item
11's migration. Item 12's text pieces landed in phase 1 (WI-979: the
`architecture-decomposition` rubric and skill, the `spine-questions.md`
pointer, the plan-decomposition question). Ruled in revision 35: F-call 7
(check A advisory first; check B waits for a real condition-table use;
check C only as a dashboard suggestion) and item 12's call: one `run.cmd
audit` with `arch` and `hats` parts, on demand only.

**Check A, well-formed value domains.** Over each interface's form, read
through the one effective-contract reader (WI-1025), and each LLR's
`dimensions` cell (WI-1024): duplicate labels, a catch-all with no declared
behaviour, and clusters of booleans standing in for one domain. Advisory.

**Check C, a dependency matrix per component.** From the import graph by
`Component:` header (WI-1021) plus interface file edges and requestor
edges, it suggests where a component is under-decomposed (W3 Autonomy
first). Noisy, so it is a dashboard suggestion only, and it reports missing
endpoints rather than assuming the import graph is complete.

**The audit's parts.** Today `run.cmd audit` runs the ruled-cover report
(WI-1006) and the smoke budget. The `arch` part's mechanical half needs no
model: `trajectory_arch`, checks A and C, `check_complexity`, the
duplicates census and `gen_arch_map`, written to one findings bundle. Its
judgement half is an independent critique session reading the bundle
against `docs/rubrics/architecture-decomposition.md`, ranking components
by what a refactor would gain. The `hats` part runs `hats.py audit`
(mechanical) and a session putting each need's applicable hats' questions
to its SRs, in batches of a few needs (revision 24). Both write candidate
work items or open items through intake; the critic never edits the spine.
With an empty route pool, the judgement half refuses rather than falling
back (revision 8). The critique procedure is a skill shaped like
`render-dashboard-critique`.

**Needs:** WI-1025 (the effective-contract reader check A reads; it lands
after WI-1024's `dimensions` cell and WI-1021's headers).

## Scope answers

- **S1.** Deliverables, in order: (1) checks A and C, advisory; (2) the
  audit's `arch` and `hats` parts and the critique skill. (2) runs (1), so
  they share one lane; (1) may land alone if the lane splits.
- **S2.** No: advisory checks and an on-demand audit whose output is filed
  through intake; nothing gates.
- **S3.** Check A's findings are three enumerated classes; any other shape
  of domain is not judged by it. The audit's part names are a closed set
  (`arch`, `hats`); an unknown part is refused.
- **S4.** `single`: two checks, a run-menu action and a skill.
- **S5.** No change to the architecture; instruments for judging it.
- **S6.** No new package, tool or service; the optional third-party tools
  item 12 lists stay the adopter's to declare.

## Done-when

- [ ] Check A reports each of its three classes over forms and dimensions,
      advisory, in `trace.py`'s advisory output and the dashboard.
- [ ] Check C renders a per-component dependency matrix as a dashboard
      suggestion, naming missing endpoints.
- [ ] `run.cmd audit` runs its existing parts plus `arch` and `hats` by
      default, or one part by name; each part's mechanical half writes the
      shared findings bundle, and its judgement half runs an independent
      session from the enabled route pool, refusing on an empty pool.
- [ ] Findings are filed through intake as candidate work items or open
      items; the session writes nothing to the spine.
- [ ] A critique skill states the judgement half's procedure, citing the
      rubric rather than restating it; the skills index regenerates.
- [ ] Tests cover each check A class, check C's missing-endpoint report,
      the part selection and the empty-pool refusal; every importer of a
      changed module runs green.
- [ ] A RESYNC entry (variant F) ships the audit parts in the run-menu
      template; adopters migrate nothing.
