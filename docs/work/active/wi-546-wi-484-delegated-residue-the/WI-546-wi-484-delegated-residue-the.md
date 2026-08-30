+++
id = "WI-546"
title = "WI-484 delegated residue: the hats.toml knowledge value-pass and the 17 approved-cell Rationale attribution deletions"
workstream = "requirements"
specref = "docs/requirements/open-items.toml#OI-32"
buildtier = "medium"
priority = 2
safety_class = "spine"
planmode = "single"
supersedes = "WI-484"
+++

## Context

Drafted by WI-544 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

Scope of the successor is items **3 and 5 only** of `WI-484`'s "Delegated for
the unattended run" section — the `knowledge` value-pass into
`docs/requirements/hats.toml` (re-pointing to existing `docs/knowledge/` packs
where one carries the perspective, drafting only where none does, each marked
draft) and the 17 approved-cell `Rationale` attribution deletions, both listed
for the owner in a re-attestation fragment. Item 7 (which traced cells are
staleness-bearing) is a classification ruling owed by nobody and is excluded.

## Deliverable

Two edits, both drafted for the owner's review at RETURN (not gated at the act;
the roster header and the `DevStg-Needs` human-held dial both put the cut at
return):

1. **`docs/requirements/hats.toml` `knowledge` value-pass (item 5 / Phase 4).**
   Each hat's `knowledge` cell is set where a perspective-knowledge body exists:
   re-pointed at an existing `docs/knowledge/` pack whose subject IS the hat's
   failure class, or given a newly drafted pack (marked DRAFT in its own header,
   grounded strictly in this repo) where none did. Hats whose perspective has no
   distinct knowledge body in this repo (the domain-silent tag-gated hats) stay
   empty — empty-is-honest, per `hats.py` `OPTIONAL_KEYS`.
2. **The 17 approved-cell `Rationale` attribution deletions (item 3).** The
   backfill left the deriving-hat attribution stated twice — once in `hat_refs`,
   once in `Rationale` prose. The prose statement of the attribution is removed;
   substantive derivation reasoning is preserved. Every touched cell is listed
   in the log fragment for the re-attestation brief; the snapshot diff against
   `docs/archive/last_approved/` carries the same set.

The log fragment (`docs/log.d/WI-546-delegated-residue.md`) is the owner-facing
record of both.
