## WI-546 — WI-484 delegated residue: the hats.toml knowledge value-pass and the 17 approved-cell Rationale attribution deletions

Successor to WI-484 (drafts-not-mints, R1/R3), scope items **3 and 5 only** of
WI-484's "Delegated for the unattended run" block (SpecRef
`docs/requirements/open-items.toml#OI-32`). Item 7 (which traced cells are
staleness-bearing) is a classification ruling owed by nobody and is excluded.
Owner review is at RETURN, not at the act — this session drafts, the owner cuts.

### Item 5 — Phase 4: the `hats.toml` `knowledge` value-pass (FOR OWNER REVIEW)

`hats.py` `OPTIONAL_KEYS` already admits `knowledge` (WI-511); this pass fills
it. The value-pass is DRAFTED, not ratified — `hats.toml` is owner text, cut at
RETURN. The existing `docs/knowledge/` packs are research-evidence notes tied to
components (CMP-006/008), so most did NOT carry a hat's *perspective*; where none
did and the hat has a real, repo-grounded perspective body, a new pack was
drafted and marked DRAFT in its own header. No path existence is enforced on the
cell (`hats.py` comment), but every cited pack exists.

**12 hats now carry `knowledge`; 4 stay empty.**

Re-pointed at existing packs (pack subject IS the hat's failure class):

| hat | knowledge |
|---|---|
| TEST-ENGINEER | `traceability-enforcement.md` (an enforcer that actually bites) |
| MAINTAINER | `instruction-file-adherence.md`, `traceability-enforcement.md` (load-bearing vs accident; reason not living only in the authoring session) |
| FIRST-RUN-ADOPTER | `instruction-file-adherence.md` (a stranger following the shipped instructions/examples) |
| PERFORMANCE | `prompt-image-token-efficiency.md`, `parallel-scheduling.md` (a size/speed claim measured, or a bound not proven) |

Given a NEW DRAFT pack (agent-authored, repo-grounded, header-marked DRAFT):

| hat | new pack |
|---|---|
| SECURITY | `security-review.md` |
| UNATTENDED-OPS | `unattended-operation.md` |
| CROSS-PLATFORM | `cross-platform-scripting.md` |
| INTEGRITY-RECOVERABILITY | `crash-atomicity-recovery.md` |
| UX-DESIGNER, UX-ENGINEER, ACCESSIBILITY | `rendered-surface-review.md` (one shared pack, an angle per hat) |
| CONSISTENCY | `rendered-surface-review.md` — a PARTIAL fit: the pack covers cross-view coherence (CONSISTENCY's core failure class across the dashboard / open-items / console), but not the template↔instance idiom half of the charter. Owner may want to broaden or split it. |

Left empty (empty-is-honest — no distinct perspective-knowledge body in this
repo; documented rather than filled with ceremony):

- **SAFETY, LEGAL, DATA-PROTECTION** — the tag-gated, domain-silent hats. The
  roster header already flags SAFETY as having "essentially one reachable
  referent" here; a drafted pack would be exactly the ceremony this tier was
  admitted to prevent.
- **PRODUCT-FITNESS** — a cross-cutting lens whose knowledge is the charter
  itself (who asked, does it still serve the need); no separable evidence body.

Owner calls this pass surfaces: (1) keep/cut/rewrite each of the 5 DRAFT packs;
(2) the 4 empties — draft a pack, gate the hat, or accept empty; (3) the
CONSISTENCY partial-fit above.

### Item 3 — the 17 approved-cell `Rationale` attribution deletions (FOR OWNER RE-ATTESTATION)

_(filled at close: each of the 17 SR rows, its `hat_refs` cell, and the
before→after of the deleted attribution prose — the snapshot diff against
`docs/archive/last_approved/` carries the same set for the re-attestation brief)_

### Harness

_(filled at close)_
