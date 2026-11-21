+++
id = "WI-1030"
title = "Checks A and C, and the run menu's audit gains its architecture and hats parts with an independent critique"
workstream = "process"
sr_refs = ["SR-159", "SR-161"]
specref = "docs/plans/2026-10-11-review-churn/README.md#12-architectural-decomposition-encouraged-at-three-moments"
needs = ["WI-1021", "WI-1024", "WI-1025"]
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

**The audit.** Today `run.cmd audit` (`[run]` in `docs/stack.ini`) runs the
ruled-cover report (WI-1006, complete) and then the smoke-budget judgement.
This row adds the `arch` and `hats` parts (Done-when 3 and 4). Each has a
mechanical half needing no model and a judgement half: an independent
critique session that files candidate work items or open items through
intake and never edits the spine. With an empty route pool, the judgement
half refuses rather than falling back (revision 8). The critique procedure
is a skill shaped like `render-dashboard-critique`.

## Scope answers

- **S1.** Deliverables, in order: (1) checks A and C, advisory; (2) the
  audit's `arch` and `hats` parts and the critique skill. (2) runs (1), so
  they share one lane; (1) may land alone if the lane splits.
- **S2.** No: advisory checks and an on-demand audit whose output is filed
  through intake; nothing gates.
- **S3.** Check A's findings are three enumerated classes; any other shape
  of domain is not judged by it. The audit's part names are a closed set
  (Done-when 3); any other argument is refused.
- **S4.** `single`: two checks, a run-menu action and a skill.
- **S5.** No change to the architecture; instruments for judging it. Its
  cross-component edges are the audit's launch of a critique session, its
  filing through `intake.py` (CMP-008), and check C's read of the import
  graph and headers (CMP-006). The lane's plan names the interface row each
  edge rides and declares a `Drafted` row where none covers it. Re-cut LLRs
  (text only, drifting): LLR-047 (the run menu reader), LLR-370 (the audit's
  ruled-cover part), and the hats LLRs LLR-168 and LLR-251; the plan
  completes the list.
- **S6.** `needs` WI-1021: check C groups the import graph by header;
  WI-1024: check A reads `dimensions`; WI-1025: check A reads forms
  through the effective-contract reader. WI-1006 is complete. No new
  package, tool or service. The optional third-party tools item 12 lists
  stay the adopter's to install and declare.

## Done-when

- [ ] Check A reports each of its three classes over forms and dimensions,
      advisory, in `trace.py`'s advisory output and the dashboard.
- [ ] Check C renders a per-component dependency matrix as a dashboard
      suggestion, naming missing endpoints.
- [ ] `run.cmd audit` takes no argument or one part name from the closed
      set `ruled-cover`, `smoke`, `arch`, `hats`. With none it runs all
      four in that order; with one it runs that part; any other argument is
      refused, naming the set.
- [ ] **The `arch` part.** Its mechanical half runs `trajectory_arch`,
      checks A and C, `check_complexity`, `check_readability`, the
      duplicates census and `gen_arch_map`, plus each tool on the run menu's
      declared audit-tool list (empty by default). It writes their output
      and exit codes to one findings bundle; a declared tool that is not
      installed is reported in the bundle, not failed. Its judgement half
      reads the bundle against `docs/rubrics/architecture-decomposition.md`
      and ranks components by what a refactor would gain.
- [ ] **The `hats` part.** Its mechanical half runs `hats.py audit`. Its
      judgement half puts each need's applicable hats' questions to that
      need's SRs, a few needs per session (revision 24), for the scope
      named at launch: one need, a set, or all.
- [ ] Each judgement half runs as an independent session from the enabled
      route pool, refusing on an empty pool, and files its findings through
      intake as candidate work items or open items; it writes nothing to the
      spine.
- [ ] A critique skill states both judgement halves' procedure, citing the
      rubric rather than restating it; the skills index regenerates.
- [ ] Tests cover each check A class, check C's missing-endpoint report,
      the part selection and refusal, a declared tool that is absent, and
      the empty-pool refusal; every importer of a changed module runs green.
- [ ] A RESYNC entry (variant F) ships the audit parts in the run-menu
      template; adopters migrate nothing.
