+++
id = "WI-484"
title = "Concern/hat references on SR and LLR rows and the generated component view: effective sets derived never copied, components.derived.toml generated, detail_doc retired (OI-32 ruled (d), 2026-08-20)"
specref = "docs/requirements/open-items.toml#OI-32"
workstream = "requirements"
sr_refs = []
needs = []
buildtier = "strong"
safety_class = "spine"
priority = 2
+++

## Context

Executes OI-32's ruling — (d) THE GENERATED VIEW — per the combined brief's
six phases (the brief is the row's recommendation cell; read it whole first):

- **Phase 0** reconciles the two hat vocabularies and SETTLES THE FIELD NAME —
  the owner's word (2026-08-20) was "hats_ref", the brief proposed
  `concern_refs`; one name, ruled here, used everywhere.
- **Phase 1** adds the field on SR and LLR rows to say which hats bear on the
  row; an LLR's EFFECTIVE set is DERIVED (own refs + inherited), never copied.
- **Phase 2** decides who writes it and runs the backfill over the live rows.
- **Phase 3** generates `docs/requirements/components.derived.toml` via a
  `gen_components.py`, declared in `docs/stack.ini` `[generated]`;
  `detail_doc` retires.
- **Phase 4** derives knowledge packs from concerns via a `knowledge` field on
  `hats.toml`.
- **Phase 5** is OI-33's surviving residue: the amend-without-flip-style guard
  — a row whose normative cells move while its concern refs do not is a
  finding.

Coverage edges the brief says the execution must answer explicitly rather
than paper over: 12 SRs have no LLR (SR-034, SR-114, SR-036 never will);
6 SRs span more than one component; 57 of 125 IF rows carry a component tag.
Standing constraint from OI-30 D3: a GENERATED file never carries an approval
(`human_ratification_through`).

**Sequencing, the owner's own note (2026-08-20):** the new field is NOT
anticipated to be an attested cell, so it can be tacked on AFTER the sitting
without re-opening anything signed — this row deliberately waits for the
sitting rather than racing it (priority 2). If the schema work surfaces
anything that IS attestation-bearing, stop and raise it rather than folding
it in. `safety_class = "spine"` because the field lands on SR/LLR rows and
the schema of record moves, even though the cells it adds are informative.
