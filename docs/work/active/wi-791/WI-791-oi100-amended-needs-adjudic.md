+++
id = "WI-791"
title = "Route amended needs to the meaning-or-clarity adjudication; CLARITY re-attests on a held rung"
workstream = "process"
specref = "docs/requirements/system-requirements.toml#SR-228"
sr_refs = ["SR-178", "SR-207", "SR-228"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-03, when the owner ruled **OI-100**
option (a): "Agreed with recommendation." OI-100's `decision`, `blast_radius`,
`options` and `recommendation` cells in `docs/requirements/open-items.toml` are this
row's spec of record. The ruling's record is
`docs/log.d/2026-10-03-owner-rulings-oi100-oi102.md`.

It extends the existing mechanism and builds nothing parallel: WI-388's amendment
trigger and its one-question brief (MEANING or CLARITY). No script approves anything;
OI-45 stands.

## Done-when

- **Gap 0.** The shipped amendment brief's aftermath
  (`prompts/adjudicate-amendment.template.md`) says that a CLARITY verdict names its
  rows in the act's `--reattests` where the dial releases the rung, so the anchor
  copy stops drifting. Coordinators already do this.
- **Gap 1.** The amendment walk (`acceptance_record.SPINE_CSVS`, read by
  `intake._amendment_drafts`) also covers the need, assumption and surrogate tiers.
  The pre-commit warning's scope is decided in the same change and stated. A test
  shows that an amended approved need mints one `amendment` adjudication row.
- **Gap 2.** On a held rung, an independent adjudicator session re-attests a row it
  rules CLARITY, as a judgement act recorded in the act ledger with its verdict. It
  recommends a MEANING row to the owner, and it never approves a first draft on a
  held rung. This amends ruled decision 2's held-rung arm
  (`intake.adjudication_action`), the brief's held-rung aftermath and PROCESS.md §4,
  with one stated case and tests.
- **Gap 3** stays as it is: one MEANING row still holds its CLARITY siblings in the
  same registry until the owner signs, and the coordinator puts them in the same
  sitting. The brief says so.
- Every held-rung CLARITY re-attestation stays listed on the owner's surface for audit
  after the fact.
- The spine rows that pin the amendment trigger, ruled decision 2 and the brief are
  identified and amended through in-lane adjudication. This row's `sr_refs` and
  `specref` are set to them, replacing the open-items reference.
- A RESYNC_PACK entry: adopters who hold the needs rung will see need amendments
  minted as adjudication rows. No migration is forced.
- The commit bar passes.
