## 2026-08-30 — WI-484: the six-phase program's residue is OWNER-GATED, and this worker session BLOCKS on it rather than manufacturing a slice

**Assessment session, no code changed.** This claim branch
(`wi484-concern-refs-component-view`, base `9ab30d64`) was cut fresh and carries
zero commits over base beyond this record. WI-484's five agent-doable slices had
already landed in the base; what a worker session can add here is nothing but the
honest finding that the remaining owed items are the owner's, not an agent's.

### What is already in the base (verified on disk, not assumed)

- **Phase 0** — field settled as `hat_refs` / column `Hat-Refs` (spec item "What
  phase 0 RULED").
- **Phase 1** — the field on SR/LLR; an LLR's effective set DERIVED (own +
  inherited), never copied.
- **Phase 2** — backfill (slice 2) + writer at the `spine-authoring` tier
  (slice 5).
- **Phase 3** — `project-trajectory/scripts/gen_components.py` and
  `docs/requirements/components.derived.toml` both present; `detail_doc` retired
  from the live/template registries and both carrier maps (residual `detail_doc`
  hits are all history: `open-items.toml`, the slice-3 log, `RESYNC_PACK.md`).
- **Phase 4 mechanism** — `hats.py` `OPTIONAL_KEYS = ("knowledge",)` (WI-511).
- **Phase 5** — the amend-without-flip guard arm `staged_hat_refs_findings`
  (slice 4).

### Why every remaining item is owner-gated

The spec's own Context names the three still owed and characterises each as
owner-or-nobody; re-reading confirmed, not overturned, that characterisation:

- **Item 3 — phase-2 duplication.** The 17 migrated rows state the attribution
  twice: once in `hat_refs`, once in the `rationale` prose it came from. Deleting
  the prose edits an **Approved** cell on **Approved** rows — the re-attestation
  surface this WI's own slice-4 guard (`staged_hat_refs_findings`) exists to
  watch. The prior slice recorded it as owner-adjacent and deliberately not
  taken; a worker session overriding that would be routing around the very sign
  the guard protects. NOT TAKEN.
- **Item 5 — phase-4 value-fill.** Filling `knowledge` values into
  `docs/requirements/hats.toml`. That file's header declares it OWNER TEXT,
  MARKED FOR THE OWNER'S EDIT AT RETURN. The mechanism is done (WI-511); the
  values are the owner's act by the file's own declaration. NOT AN AGENT'S ACT.
- **Item 7 — staleness granularity.** Which traced cells are staleness-bearing is
  a new classification — a RULING, not a patch (the spec states the obvious
  approved-only filter is the WRONG filter, not merely an expensive one). The
  spec records the limitation in the docstring with its measured instance on the
  WI-362 precedent, and says building the detection is owed by nobody yet.

### Disposition

No agent-doable, in-scope work remains on WI-484. The residue is three owner acts
(a value-pass on owner text, an approved-cell prose deletion, and a
cell-classification ruling), each recorded in the spec and untouched here. This
session commits the finding with `Blocked-WI` rather than a WI trailer, so the
integrator/owner can decide close-with-tracked-residue vs. hold — a disposition
that is theirs, not a worker's. Nothing signed moved; the tree is otherwise clean.
