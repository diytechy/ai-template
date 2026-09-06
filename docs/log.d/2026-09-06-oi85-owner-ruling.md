## 2026-09-06 — OI-85 owner re-attestation

**Decision.** The owner explicitly accepted OI-85 recommendation (a):
re-attest SN-007 and SN-026 as amended, and qualify SN-024's normative
acceptance so family heterogeneity binds unattended Critique. For attended
acceptance the human chooses the reviewer; fresh non-author review, a written
rubric independently derived from SN/SR intent, and numbered anchors remain
required. This is the owner-held need-tier act, recorded on the owner's behalf.

The reviewed delta against the existing needs snapshot is limited to:

- SN-007 `acceptance`: the declared landing bar replaces a whole-suite run
  before every change; the Full suite still bootstraps a temporary scaffold
  and exercises every delivered script.
- SN-026 `tags`: `legal` and `personal-data` activate the applicable existing
  hats. Normative need and acceptance text remain unchanged.
- SN-024 `acceptance`: unattended family heterogeneity and human choice of
  attended reviewer are now explicit in the normative cell.

The recording command is `intake.py --root . snapshot --approves
stakeholder-needs.toml=docs/log.d/2026-09-06-oi85-owner-ruling.md#2026-09-06--oi-85-owner-re-attestation`.
It copies only the needs registry into
[`last_approved/docs/requirements/stakeholder-needs.toml`](../archive/last_approved/docs/requirements/stakeholder-needs.toml)
and appends that scope to the existing stamp. No Status moves, other registry
snapshot refreshes, queue transitions or policy changes are part of this act.
The historical snapshot remains in Git. The generated modified-approval brief
does not render needs, so this record names the reviewed cells explicitly
instead of claiming that the brief covered them.

The need-drift detector is a separate implementation proposal and remains
deferred; it was not included in recommendation (a)'s implementation scope.
SN-024 now permits coherent adjudication of SR-184/TC-209. Their Drafted state
and outstanding implementation/Inspection work are separate from this ruling.

**Fable cross-check.** Its child-level correction was valid: a Drafted SR
could not narrow an Approved parent's family clause. The snapshot path in its
brief omitted `docs/requirements/`, and its description of `SNAPSHOT_TIERS`
omitted the off-spine tiers; both descriptions are corrected in OI-85. The
substantive finding that SN has no drift consumer remains true.

Validation and the implementation review are recorded in the continuation
session record when their commands finish. No test or Inspection result is
claimed by this owner decision alone.

Deferred open items: none.

The separately proposed detector remains outside this sitting's implementation scope.
