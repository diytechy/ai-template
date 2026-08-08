+++
id = "WI-390"
title = "PROGRAM CLOSE for concurrency-v2 (docs/concurrency-v2.md §A9 deletion ledger). NOT a sweep-up-dead-code row, and must not be built as one: EVERY ROW IN THIS PROGRAM DELETES ITS OWN MACHINERY as part of its own scope, and deferring a deletion to this row is the mothballing the governing principle exists to prevent. This row owns ONLY the surfaces no single builder can own. (1) THE SPINE AMENDMENT, which is why this is safety_class=spine. Live SRs describe the model the program replaces and will be FALSE once it lands: SR-093 `Pure safety classification` and SR-124 `Contradiction-safe dual-plan dispatcher class` both describe the five-scheduling-class ladder WI-383 collapses into two axes (exclusive|parallel + rank), and SR-124 names `single-WI` specifically, a class that ceases to exist; SR-132 `Local integrator: serial fail-closed merge queue` describes the composed-tree bar and candidate worktree WI-386 deletes outright. Check SR-131 (tracked pause drains claiming to a merged stop) against WI-387's terminal outcomes and SR-133 (work-branch lane skip for freshness steps) against WI-386's refresh, both of which MAY be affected - verify, do not assume. Any further amendments the seven builds surface land here too. THE POINT OF BATCHING THEM: per §A4 all spine WIs admit together as ONE re-attest window and ONE owner sitting, so this program costs the owner a single sitting instead of one per row - which is the WI-280 pain the whole design exists to prevent, applied to the design itself. Follow the repo's existing convention for rows the program retires rather than amends: mark them `Superseded: <title>` as Phase 5 did for the deleted dispatcher's SRs, never delete the row. (2) CONNECTIVITY AND THE INTERFACE REGISTRY. drive.py -> dispatch.py + lane.py moves the arch-map entry and the Contracts: docstring declarations. Note the registry is ALREADY drifting before this program starts - check_trajectory currently WARNs that scripts/drive, traj_graph, traj_panels and traj_render sit in the arch-map with no IF-### row naming them, that trunk_step declares no Consumes seam, and that IF-055, IF-080 and IF-081 are in the registry with no script declaring them - so close the drift this program CAUSES and record, without silently absorbing, the drift it merely inherits. (3) THE PROSE THAT DESCRIBES THE OLD MODEL: PROCESS_OPTIONS.md (rewritten onto the seam model at Phase 5, and the station protocol changes that seam), AGENTS.template.md, and concurrency-restructure.md's forward-looking claims - the last is HISTORY and must be read as the account of what was built, never edited into a claim about what now exists. (4) THE STAMPS: deletions SHRINK modules, and the standing rule is that a size/complexity entry is retired or deleted rather than re-stamped up - the mirror obligation is to re-stamp DOWN rather than leave a generous ceiling that would silently permit regrowth, and to check whether any docs/dupes-allow census sanction has gone vacuous. VERIFY MECHANICALLY, NOT BY EYE: run check_stubs.py, check_dupes.py, the size ratchet, and check_trajectory.py --strict unfiltered, and quote the real output - the question `is anything left behind?` has mechanized answers in this repo and must not be answered by reading code. Hard-blocked on every row that changes a contract so the spine amendment reflects the final state; soft edge on the Process-tab render, which changes no contract."
workstream = "process"
buildtier = "medium"
safety_class = "spine"
needs = ["WI-380", "WI-381", "WI-383", "WI-384", "WI-386", "WI-387", "WI-388", "~WI-389"]
+++

## Deliverable

**CANCELLED 2026-08-08 — absorbed into the mechanized-loop program (P1 and P13).**

Not abandoned: every obligation this row carried is now owned by a named
phase of the [stakeholder-needs build plan](../../stakeholder-needs-build-plan-2026-08-08.md), which replaces the
concurrency-v2 machinery this close was going to describe.

- **(1) The spine amendment.** Absorbed into **P1**. Amending SR-093 / SR-124 /
  SR-131 / SR-132 / SR-133 to describe the two-axis scheduler immediately before
  this program replaces the scheduler would buy one sitting and then owe another.
  P1 runs the single combined sitting the plan §4 declares — the five new needs,
  the SN-026 amendment, and the 21 already-`Modified` rows — and the affected
  rows are amended once, against the model that will actually be live.
- **(2) Connectivity and the interface registry.** Absorbed into **P13**, whose
  scope already includes regenerating every declared artifact and closing the
  arch-map / `IF-###` drift this program causes. The drift this row *inherited*
  (drive/traj_graph/traj_panels/traj_render unnamed; trunk_step declaring no
  `Consumes` seam; IF-055/IF-080/IF-081 unclaimed) is recorded here rather than
  silently absorbed, and is re-checked at P13 rather than assumed closed.
- **(3) The prose describing the old model.** Absorbed into **P13**.

Explicitly **not** absorbed: this row was never an unused-function sweep, and
the plan agrees — P14 mints that sweep separately and measured.

Ratification: [mechanized-loop decisions](../../mechanized-loop-decisions.md) §6 (the combined sitting).

## Context

### Re-scope (WI-414, 2026-08-02)

Added by the WI-414 adjudication of `TC-056 Verifies` on merged trunk
`7894457..5211f07`, as the §A5.2 scope-moved output. This row's spine amendment
explicitly covers the ratified prose WI-389 left describing the deleted
two-intersecting-hoops render, which the merge made false:

- `SR-055` — still requires "two circular working loops" and one shared
  `LLM_Agent` hub; still `Verified`.
- `LLR-056` — still describes those loops.
- `TC-056` `Method` + `Expected` — still specify two hoops and the 6+5=11 edge
  count, while the row's `Evidence` now cites the station-cycle tests and the
  shipped render emits ONE station cycle.

WI-389's own Deliverable already routed these here ("amending it is the program
close's spine scope, not this ordinary row's") and names SR-050/LLR-051/TC-051
alongside them; WI-414 confirms the routing from the adjudication side and adds
nothing new to own. The Modified/re-attest flow for these cells belongs to this
row's owner sitting — deliberately NOT flipped at WI-414, which is why no Status
moved there.

This section also re-dates this row against its amended SpecRef
(`docs/concurrency-v2.md`), which is the re-affirmation the standing
`check_trajectory` SpecRef-clock warning asks for.
