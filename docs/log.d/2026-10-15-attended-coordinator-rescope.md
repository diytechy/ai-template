## 2026-10-15 — attended coordinator: the process-text row's gate and fix round; the owner's re-scope walk; the removal rows drafted

An attended coordinator session under the review-churn program
([handoff-2026-10-15h-attended-coordinator](../handoff-2026-10-15h-attended-coordinator.md)).
Nothing landed on trunk but the close-out; no code changed on trunk.

- **WI-911, the process text** (lane `wi-911`):
  - **The uncounted gate** (convergence stance, three reviewers over
    `c0dfd1823..9f35d60ea`, the trunk-only views already matching the base).
    012 (Codex Sol) was CHANGES-REQUESTED, with one MAJOR, confirmed by
    reading. The reviewer template's convergence paragraph tagged each new
    BLOCKER or MAJOR, but it never bounded those severities to a reachable
    fail-open path, data loss or a Done-when gap, which LLR-311 (blessed at
    sitting 010) requires. 013 (Claude Fable) and 014 (Claude Opus) were
    APPROVE, with MINORs only. The triage is wi-911 D-019 (`68dbe4136`):
    - the MAJOR is fixed;
    - LLR-314's ruling set and SR-236's rationale, each raised by two
      reviewers, and the byte-budget figure are adopted;
    - K2's LLR extension and the TC-method question are deferred to item 5;
    - the plan.md reading-scope MINOR is not adopted.
  - **Spine rework** by Terra (`31422914d`), checked cell by cell. Sitting
    015 ruled CLARITY rows=2, and the adjudicator's act took seq 119
    (`95c92c2d2`).
  - **The fix round** (`c074151b7`) was built in two stages, on coverage
    plans (one per round file) that passed `plan_coverage.py` at exit 0. The
    template now states the bound, with two test assertions that failed on
    the old template first. The byte-budget rows record the measured delta.
    The second uncounted gate is next.
- **The owner's re-scope walk** (coordinator-2026-10-15 D-010), one row at
  a time, with the audit of contrived guards beside it:
  - D-012: WI-925 builds no reference-transaction hook. It keeps the
    declared trunk key, the relink fix and the carried text fixes.
  - D-013: WI-922 keeps SR-154's amendment and one dead branch's deletion.
  - D-014: D-008's fail-open row is not filed.
  - D-015: WI-926's calls.

  In each row, the hand shapes no supported route makes become stated
  residue.
- **The removal rows D-011 ordered**, drafted by planners after reading
  each original rationale, with the owner's calls ruled: D-016 (WI-834's
  grammar forms), D-017 (WI-852, two rows), D-018 (WI-881). WI-926 splits
  off the agent CLI's guard hooks (D-019), where the owner overruled the
  coordinator: the install keeps asking for consent. D-021 covers the
  no-terminal case. The coordinator's own calls on the redrafts are D-020.
  The seven drafts are in the session scratch, not yet filed.
- **Smoke tier under load:** the owner's editor and the Codex app loaded the
  box, with the tier at below-normal priority. It read 100.9 to 111.4 s on
  the lane and 105.5 s on trunk's tip, against 40.8 s at that tip's own
  commit. Each commit records the breach and the trunk reading.
- **Trial counts, the gate:** round-costing Sol 1, Fable 0, Opus 0; MINORs
  Sol 1, Fable 1, Opus 6, two shared.
