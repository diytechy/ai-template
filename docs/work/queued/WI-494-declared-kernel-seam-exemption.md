+++
id = "WI-494"
title = "The declared-kernel seam exemption with a reuse provision (OI-48 ruled (d), 2026-08-21)"
specref = "docs/requirements/open-items.toml#OI-48"
workstream = "scripts"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "spine"
priority = 3
+++

## Context

Executes OI-48's ruling (d), generalised by the owner's own follow-through
question into a REUSE PROVISION. The operative shape, from the ruling:

- **One owning component for `scripts/kitlib/`.** The recorded closest-fit
  analysis points at `CMP-006` (the registry reader is the package's bulk);
  measure at execution and record the tag with reasoning on the row.
  `LLR-181`'s four-way `Component` tag collapses to the owning component
  (traced cell). Reconcile `LLR-182`'s single-tag `CMP-008` choice for
  `kitlib/station.py` with the ruled ownership — either the kernel
  declaration covers it or the tag moves; record which and why.
- **A declared kernel LIST, not a `kitlib` hardcode.** A new declared
  surface (home per the ruling: a small declared file or a `[checks]`-side
  declaration — pick the one consistent with the repo's declared-surface
  conventions and record why) listing kernel modules, one per entry, each
  with a recorded reason. Any future shared module whose consumers span
  components takes the same declared path; an addition is a deliberate
  recorded act. This is the owner's reuse provision: the same
  multiple-seams-into-multiple-components shape recurs for any reused
  module, so the mechanism must not be special-cased to kitlib.
- **`cross_component_findings` learns the exemption:** an import edge INTO
  a declared kernel module is not a seam finding. The rule stays fully live
  for every other edge — including edges OUT of a kernel module (kitlib
  importing a non-kitlib sibling is already refused by the WI-448 rule
  test; keep both directions covered).
- **The multi-membership advisory stays live** so future kernel candidates
  keep surfacing rather than being silently exempted.

Tests: the exemption bites only for declared entries (an undeclared shared
module still warns); an entry without a reason is refused or warned per the
allow-file grammar conventions (OI-41 ARM precedent); the seam rule still
fires on a planted non-kernel cross-component import. Scaffold-verify: the
checker ships; bootstrap a real scaffold and confirm the declared surface's
absence means no exemption (fail-safe default).

Sequencing: this row unblocks the wi448 consolidation slices (each adds
importers) and settles the question the wi483 lane kept open by choosing a
single-tag LLR-182. Both lane specs cite OI-48 as the gate — update their
Context lines at close.
