+++
id = "WI-605"
title = "adjudicate: SR-161, LLR-183, TC-178 owner-ruled perspective-review amendment; judge scope and snapshot absorption explicitly"
workstream = "process"
sr_refs = ["SR-161"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["SR-161", "LLR-183", "TC-178"]
+++

## Deliverable

Restructured into WI-610.

## Context

Prepared from the SN-036 owner ruling and the live snapshot-drift brief. Source amendments are limited to the approved amendments to SR-161, LLR-183 and TC-178, while reading their whole chain, the revised direct Inspection route through TC-211, and TC-178's surviving supplementary Hat-Refs linkage. Decide whether each amended cell preserves or changes scope; The adjudication also judges the complete whole-registry absorption population below before any copy; it may re-attest only cells whose full chain and before/after it actually judged.

Supervisor clarification superseding the preceding legacy phrasing: "approved amendments",
"judges the complete whole-registry absorption population" and "re-attest" do
not assert acceptance or enlarge this WI's scope. This turn adjudicates only
SR-161, LLR-183 and TC-178. The remaining ledger is a publication precondition:
an unjudged changed cell requires RETURN with zero accepted cells and a precise
continuation; it does not transfer that cell's ownership to WI-605.

Required snapshot absorption ledger before any snapshot write:

- Targeted SR amendment: SR-161 (`Requirement`, `Rationale`, `AcceptanceCriteria`, `Verification`).
- Targeted LLR amendment: LLR-183 (`Detail`).
- Older SR rationale drift that a whole `system-requirements.toml` snapshot would also absorb, which must each receive an explicit independent judgment before copying (this WI does not authorize editing them): SR-024, SR-033, SR-043, SR-052, SR-053, SR-054, SR-111, SR-112, SR-129, SR-144, SR-146, SR-147, SR-149, SR-162, SR-167, SR-175, SR-176, SR-177.
- Older LLR drift that a whole `low-level-requirements.toml` snapshot would also absorb, which must each receive an explicit independent judgment before copying (this WI does not authorize editing them): LLR-035, LLR-051, LLR-052, LLR-055, LLR-056, LLR-057, LLR-061, LLR-078, LLR-080, LLR-085, LLR-086, LLR-087, LLR-088, LLR-099, LLR-100, LLR-101, LLR-102, LLR-103, LLR-104, LLR-105, LLR-106, LLR-107, LLR-108, LLR-109, LLR-110, LLR-113, LLR-114, LLR-115, LLR-116, LLR-119, LLR-120, LLR-160, LLR-167, LLR-200. WI-601 retains LLR-061 and WI-603 retains LLR-167; this row neither duplicates nor absorbs their scopes.
- Targeted TC amendment: TC-178 (`Expected`), corrected after the independent method-flip review. Its direct SR-161 link is retained as supplementary evidence, explicitly distinguished from TC-211 in the result wording. Judge that retention reason.
- TC-178 remains mechanically useful for LLR-183's Hat-Refs resolution, vacuity, advisory and effective-set claims, but its `Verifies = ["SR-161", "LLR-183"]` and parent-satisfaction wording must be judged against SR-161's new Inspection method. Do not silently treat its Unit evidence as the perspective-review Inspection.

- Newly present Drafted SR-183/SR-184/SR-185/SR-186 and LLR-210 would also ride their respective copies. Preserve their Drafted statuses; this is not their first approval. LLR-210 remains with WI-604.
- Test registry absorption population: `docs/test/test-cases.toml` differs from its snapshot on TC-178's Expected cell and newly present Drafted TC-208/TC-209/TC-210/TC-211. No other existing test row differs at preparation. Read it again at execution. Copying these new Drafted rows does not approve them; their Status must remain Drafted until their own first-approval adjudication (TC-208 remains with WI-604; TC-209–211 with the dependent batch). No other test cell or Status is authorized to change here.

The primary publisher may write no snapshot for any of the three affected registries unless every additional changed cell it would absorb has an independently reviewed judgment explicitly listed in the approval record. For older SR/LLR cells, cite a prior whole-chain judgment covering the exact live text; WI-605 does not independently acquire those scopes. Preserve WI-601 and WI-603 as the owners of their existing scopes: cite their completed judgments when available; do not close, absorb or duplicate those WIs. If any necessary judgment is unavailable or the scoped cell cannot be accepted, RETURN with findings and draft the precisely scoped successor in `## Dispositions`; do not request a copy. An approval reference names a completed judgment and never waives this review. Do not request any unrelated Status change. The existing pause remains; this is adjudication preparation, not a claim.

Supervisor migration continuity: this same WI was returned from its stopped
legacy worktree to the queue under the repaired primary-turn contract. Read
`docs/reviews/2026-09-07-WI-605-supervisor-migration.md` before judgment. The
preserved branch, round files and interruption patch are incident evidence and
claims under review; none is an accepted approval payload or executable patch.
