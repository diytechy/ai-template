## 2026-08-30 — Review A — WI-508

- [BLOCKER] docs/ratify/CURRENT.md:51 -> TC-199 and TC-200 are rendered “Drafted, never approved” although `580df781` approved and snapshotted them; `4824c0ba` then rewrote that historical snapshot during a rollback, contrary to PROCESS.md §4's approval-only, wholesale snapshot rule, so this regeneration ships a false attestation record -> restore the actual approval snapshot, preserve the demotion as an auditable state, and regenerate the brief so it reports the prior approval instead of laundering it -> @owner
VERDICT: CHANGES-REQUESTED findings=1
