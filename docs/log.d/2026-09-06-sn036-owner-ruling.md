## 2026-09-06 — SN-036 / SR-161 owner ruling: review pass, not a guard

**Decision.** The owner ruled that SN-036's perspective coverage is satisfied by
construction — a recorded hat-by-hat review of each decomposition round — and
not by a machine-readable no-finding record plus a check. The proposed
`hats_no_finding` cell is withdrawn: with nine of sixteen roster hats on
`applies_when = "always"`, a per-need no-finding record is roughly 240 cells
that discriminate nothing, the exact failure WI-484's backfill measured for
`hat_refs` and refused.

**Origin evidence read at the sitting.** SN-036 landed 2026-08-12 with the
intake reviewer's amended text; the "machine-readable record … a check reports"
acceptance clause is the reviewer's specification, accepted at the sitting.
SR-161 was minted 2026-08-14 by WI-451 because the strict trace named SN-036 an
orphan; its requirement restates the acceptance one tier down. LLR-183 declined
the coverage half on purpose ("Absence is NOT RECORDED"). The hat-by-hat pass
the owner describes already ran once as a review artifact
([blind derivation C](../plans/2026-08-16-blind-derivation-c-hats.md)); the
guard would add only re-entrancy, which adjudicated WIs already carry.

**Acts, in order (owed to the next implementer, scope line included):**

1. Amend `SN-036.acceptance` (owner-tier act, needs-only snapshot through the
   same `intake.py snapshot --approves` route OI-85 used, citing this record):
   each decomposition round is reviewed against the applicable hats and the
   review record names each hat's outcome. Drop "machine-readable" and "a check
   reports". `need` and `why` are unchanged.
2. Re-point `SR-161` to the existing mechanism: the decomposition brief injects
   every applicable hat's question (hats roster + `plan_briefs`), the sitting's
   review record is the perspective record, and `hat_refs` remains provenance
   for hats that raised a row. Verification becomes `Inspection` of one real
   review record. Rationale names this ruling; no new cell, carrier or check.
3. Close LLR-183's `NOT DISCHARGED` clause by amendment to match.
4. Re-point the redesign's H5 chain (SR-186 / TC-211) so TC-211's normal sample
   inspects an actual review record instead of an absent producer. SR-184–186
   and TC-209–211 stay Drafted; their adjudication route is unchanged.

Do NOT build `hats_no_finding`, a sidecar record, or a coverage check. Do not
backfill the spine in the same commit. Keep the change to the four rows above,
their snapshot, and the Inspection procedure text.

**Still owed by the owner, not ruled here:** the control window's route-complete
spend arrangement, whether the launch waits for this work, queueing of the
Drafted amendment adjudications, OI-82, and the standing of the smoke-timing
exception.

Deferred open items: OI-82 — owner-held; named above as still owed, not ruled here.
