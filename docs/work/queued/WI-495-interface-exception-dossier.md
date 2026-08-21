+++
id = "WI-495"
title = "The interface-rework exception dossier for the owner's ratifying commit (OI-49 ruled (b), 2026-08-21)"
specref = "docs/requirements/open-items.toml#OI-49"
workstream = "requirements"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "spine"
priority = 2
+++

## Context

Executes OI-49's ruling (b) RATIFY WITH A NAMED EXCEPTION LIST. The bulk of
the LIVE `owner` cells is accepted by the ruling — NOT the superseded
2026-08-15 list of 21 (ten picks have since legitimately moved to the
design tier; the ruling text is explicit that a ratification quoting the
old log entry would sign a superseded list). What this row prepares, one
read each with a written recommendation:

1. **The two unargued picks** — `IF-013`→`SR-006` and `IF-044`→`SR-154`,
   recorded as bare pairs. Read the contract, write the reason (or the
   re-pick), so the cell becomes reviewable.
2. **The five-row loaders-vs-decision split** — IF-056/IF-082/IF-084
   (owner = the loaders/joins) versus IF-071/IF-085 (owner = the
   ready-frontier decision). The executor self-flagged this as its most
   overturnable call; it turns entirely on what each contract says
   CROSSES. Read all five contracts and recommend keep-or-repick per row.
3. **`IF-131`'s single-constituent bundle** — a carrier with one
   constituent is a pointer wearing composition's field. Justify it or
   recommend the plain re-point.
4. **The depth bound of 2** on `carried_by` — still explicitly provisional,
   never re-examined. State the evidence (nothing has wanted a third
   level) and recommend keep-provisional or ratify-as-bound.

The deliverable is a dossier (a plan doc under docs/plans/ per convention)
plus any cheap traced-cell reason annotations the reads justify. The
RATIFYING Status-change commit stays the owner's — this row must not flip
any status. IF-097 and IF-080 are CLOSED by the ruling's own record — do
not re-derive them; the `;`-cell coverage residue was separately fixed at
the 2026-08-21 review iterate (W-12), so the OI's IF-097 caveat is already
discharged — verify and say so in the dossier.
