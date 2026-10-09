## 2026-10-08 (second session) — Coordinator: WI-849, WI-846 and WI-864 landed; the review threat model ruled; WI-860 and WI-866 open mid-cycle

Resumed from [handoff-2026-10-08-coordinator.md](../handoff-2026-10-08-coordinator.md).
The next resume map is [handoff-2026-10-08b-coordinator.md](../handoff-2026-10-08b-coordinator.md).

**Landed.**

- **WI-849** (`ceab00c1`): the approval act may be taken in the authoring lane
  by an independent adjudicator. Round 4 built one parser for the claimed scope
  cell and one acted set; Codex Sol round 4 SOUND; the checkpoint sitting
  (verdict 002; the first call failed on the home's OAuth refresh before
  launch) re-attested seven rows, approved TC-331 and blessed the Done-when
  change; the fresh full-lane review SOUND. Re-mint WI-862 closed as settled.
- **WI-846** (`8ab50ddb`): the adjudicator's dedicated Claude home authenticates
  with the owner's long-lived token. Rounds 6 and 7 built one prepared runner
  for the probe and the launch, refused an unresolved runner (no bare-name
  fallback, D-008), withheld the credential from the version probe, and fixed
  the `{model}` substitution regression. Its two sittings were the token's first
  live runs; verdict 001 returned four rows whose rewording had dropped built
  obligations ("as before"), answered in the lane; verdict 002 re-attested seven
  rows and approved TC-330. The fresh full-lane review SOUND (at medium).
  Re-mint WI-863 closed as settled.
- **WI-864** (`f3f4b495`): a consolidation sitting over the review-response rows
  the owner chose (WI-805, WI-811, WI-847, WI-848, WI-852, WI-853, WI-854,
  WI-860): queue with edges, nothing absorbed. The order is WI-860, WI-852,
  WI-853, WI-848. The mechanical close wrote only the last of three edges on
  one waiter; the coordinator added the rest by hand (D-003) and filed WI-866.

**Owner rulings and directions (2026-10-08).**

- The review threat model
  ([log.d/2026-10-08-owner-ruling-review-threat-model.md](2026-10-08-owner-ruling-review-threat-model.md)):
  a finding needing a compromised or contrived host is dismissed, never
  answered with code; the adjudicator, not the coordinator, rules contested or
  repeated findings. Filed as WI-860; WI-861 (the dispute class) was folded into
  WI-811, then the coordinator path split back out as WI-865 so it does not wait
  behind WI-809, and WI-811's `needs` on WI-805 was dropped (text ordering only).
- Codex Sol reviews by hand at medium, not high.
- WI-846's round-6 findings needing a fake runner or a mid-call environment
  change were dismissed under the ruling (wi-846.toml D-009).

**Open mid-cycle.** WI-860 (the review threat model: built, its rows returned
twice and answered, third re-sit owed) and WI-866 (the close keeps every edge:
built, LLR-312 approved, TC-254's re-attestation owed). See the handoff.

**Bar.** The smoke tier passes but is over its 60 s budget (91.7 s at
`1f3f67dd`; 88.7 s at this session's starting commit `cb92f2cb`, so the breach
predates the session and tracks the workstation's job-object change WI-859
records). Not re-stamped; surfaced to the owner.

**Full suite** at `9559f785` (detached worktree, fixed basetemp under `review-tmp/2026-10-08-coordinator-b/`): **5425 passed, 17 skipped, 0 failed** in 724 s. The conftest isolation test WI-859 tracks passed this run. The basetemp was deleted once recorded.
