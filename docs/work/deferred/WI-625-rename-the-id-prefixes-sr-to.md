+++
id = "WI-625"
title = "Rename the id prefixes SR- to SS- and LLR- to DE- across the repository, archives included (Q9, S2; last)"
workstream = "requirements"
needs = ["WI-615"]
specref = "docs/plans/2026-09-20-validation-gap-and-the-assumption-tier.md#121-decisions"
buildtier = "medium"
priority = 0
safety_class = "spine"
+++

## Context

DEFERRED by the owner's direction (2026-09-24; Q9 and the sister plan's S2):
taken last, at the lowest priority, after everything else. The owner judged it
low-risk find-and-replace, applied globally, archives and old logs included;
for this step that supersedes the sister plan §1.2's "historical quotes
untouched". What makes it more than find-and-replace, to settle with the owner
when it is taken:

- **Scale:** `LLR` alone was 832 occurrences in 66 kit scripts, 936 in 74 test
  modules, and 16,829 across 1,070 files under `docs/` (sister plan §1.2,
  2026-09-23); `SR` is larger.
- **Code:** id regexes, the carrier maps, the watermark spaces
  (`docs/id-watermark`), TOML table names and test fixtures.
- **Approval identity:** the approved-text snapshot
  (`docs/archive/last_approved/`) and the fingerprints must change in the same
  commit as the registries, or every approved row reads as drifted, and a
  snapshot refresh is itself an approval act (Q26's row-level refusal).
- **Adopters:** every adopter's registries carry `SR-` and `LLR-` ids; the
  UN -> SN precedent kept no legacy bridge, and it needs a `RESYNC_PACK.md`
  entry.
- **What cannot change:** commit messages and pushed history keep the old ids.
- **Collisions:** `SR-` and `DE-` as substrings of other tokens, and whether
  the rung `DevStg-LLReqs` is renamed with it (the owner's call).

## Done-when

- The owner confirms the scope list above when the item is taken.
- One reviewed change renames the prefixes, keeping every number, with the
  registries, snapshot and fingerprints consistent, so no approved row reads as
  drifted.
- The full suite and `check_trajectory.py --strict` pass afterwards, and
  `RESYNC_PACK.md` carries the rename.
