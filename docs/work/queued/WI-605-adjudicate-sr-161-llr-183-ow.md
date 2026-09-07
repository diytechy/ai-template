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

## Approval

```toml
version = 1
turn = "WI-605-b830f202c551c7c11d1a63ea4baff84a7ff6e596"
base = "b830f202c551c7c11d1a63ea4baff84a7ff6e596"
proposal = "375552089aff471b7cfe17c2dbd3954bccd8154acce0f33f2edf4659d37b4be3"

[[decision]]
registry = "docs/requirements/system-requirements.toml"
row = "SR-161"
classification = "return"
before = { Requirement = "435d8ce708795a5e3f9451ff0d171824b2b3c452", Rationale = "435d8ce708795a5e3f9451ff0d171824b2b3c452", AcceptanceCriteria = "435d8ce708795a5e3f9451ff0d171824b2b3c452", Verification = "435d8ce708795a5e3f9451ff0d171824b2b3c452" }
after = { Requirement = "6524fbb9f27d1735b33cab2731a32f86943f33e8", Rationale = "6524fbb9f27d1735b33cab2731a32f86943f33e8", AcceptanceCriteria = "6524fbb9f27d1735b33cab2731a32f86943f33e8", Verification = "6524fbb9f27d1735b33cab2731a32f86943f33e8" }
evidence = ["be785dcc9cddac3d86a2fa32d5d38f018e04c1a4"]

[[decision]]
registry = "docs/requirements/low-level-requirements.toml"
row = "LLR-183"
classification = "return"
before = { Detail = "1ec0ab08fcea5f7dd638651e4281322bbd031705" }
after = { Detail = "da0762f8d0f124b086c1e3a7b1e67086e1ba31ac" }
evidence = ["be785dcc9cddac3d86a2fa32d5d38f018e04c1a4"]

[[decision]]
registry = "docs/test/test-cases.toml"
row = "TC-178"
classification = "return"
before = { Expected = "ca71cc09e6093c5c5ff299e8d077453c967140d2" }
after = { Expected = "354a27de0df76fa86c195d023d7b835bdd25d4d6" }
evidence = ["be785dcc9cddac3d86a2fa32d5d38f018e04c1a4"]
```

Judgment: `docs/reviews/contract_split/001-ADJUDICATE-65eda1b.md` at
`be785dcc9cddac3d86a2fa32d5d38f018e04c1a4` — MEANING on all three rows; every decision is `return`
with zero accepted cells, so no absorption or impact ledger is carried. SR-161
Rationale cites a path that does not exist
(`docs/log.d/2026-09-06-sn036-owner-ruling.md`; the ruling lives at the
docs/log.md heading "2026-09-06 — SN-036 / SR-161 owner ruling: review pass,
not a guard"). Every one of the three registries would also absorb Approved
cells with no completed judgment: SR-162 Rationale (sitting commit 77612fb2);
LLR-140, LLR-152, LLR-153, LLR-154, LLR-158, LLR-207 Detail and TC-146,
TC-147, TC-148, TC-153, TC-161, TC-205 Method (sitting commit 0f106ce9);
LLR-061 (WI-601) and LLR-167 (WI-603) still queued. Equivalence and coherence
observations in the verdict are findings only.

## Dispositions

```toml
title = "Correct SR-161 Rationale's ruling citation to the record that exists, then let the merge-side mint raise the reanchor"
workstream = "process"
buildtier = "quick"
priority = 2
specref = "docs/requirements/system-requirements.toml"
sr_refs = ["SR-161"]
```

WI-605 (verdict `be785dcc9cddac3d86a2fa32d5d38f018e04c1a4`) judged the SN-036 owner-ruling amendment of SR-161
MEANING and coherent with the approved SN-036 acceptance, but RETURNED the
Rationale cell: its closing sentence cites
`docs/log.d/2026-09-06-sn036-owner-ruling.md`, which does not exist. IN
SCOPE: amend ONLY that citation frame in SR-161's `rationale` so it names the
ruling's real home — the docs/log.md heading "2026-09-06 — SN-036 / SR-161
owner ruling: review pass, not a guard" — or drops the dated record citation
in favour of stating the decision (review pass, not a guard) in the cell's own
words; leave Requirement, AcceptanceCriteria, Verification=Inspection, Hat-Refs
and every other SR-161 cell byte-identical, and touch no other row. The
approved-cell diff on this row's merge mints the SR-161 amendment adjudication
(intake trigger (a)); that reanchor must read the whole chain — LLR-183,
LLR-202, TC-178 (supplementary Verifies), TC-198, and TC-211's Inspection
result — and may publish `system-requirements.toml` only once SR-162 (below)
and the seventeen WI-547-judged Rationale cells are each listed with an
accepted judgment. EXPLICITLY NOT IN SCOPE: LLR-183, TC-178, any snapshot,
any Status change, and the Drafted SR-183–SR-186 (WI-606 owns SR-184–186).

```toml
title = "Queue the amendment adjudications the 2026-09-06/07 sitting commits owe: SR-162 Rationale, six LLR Detail rows, six TC Method rows"
workstream = "process"
buildtier = "medium"
planmode = "dual"
priority = 2
```

Two sitting commits landed directly on trunk and so never met the merge-side
amendment mint: 77612fb2 dropped "and no SR states it yet" from SR-162's
Rationale, and 0f106ce9 rewrote the Detail of LLR-140, LLR-152, LLR-153,
LLR-154, LLR-158 and LLR-207 (with CodeSymbol/Module) and the Method of
TC-146, TC-147, TC-148, TC-153, TC-161 and TC-205. All thirteen are Approved
rows whose approved text now differs from `docs/archive/last_approved/` with
no completed judgment and no queued owner, and WI-605 (verdict `be785dcc9cddac3d86a2fa32d5d38f018e04c1a4`) found
them UNJUDGED; until each is judged no whole-file snapshot of
`system-requirements.toml`, `low-level-requirements.toml` or
`test-cases.toml` can be published by any turn. IN SCOPE: through the intake
route the supervisor used to queue WI-601 and WI-603 (never by editing a cell
and never as a Dispositions draft, which cannot declare the adjudication
class), queue amendment adjudication rows covering exactly those thirteen
rows and cells with their before/after listing, grouped by registry; keep
WI-601 (LLR-061) and WI-603 (LLR-167) as the sole owners of their rows;
record in this row's close which queued ids now own which cells, so the
later LLR/TC reanchor can cite them. The LLR reanchor additionally depends on
WI-601 and WI-603 completing; the TC reanchor on WI-604 (TC-208) and WI-606
(TC-209–211) staying Drafted riders. EXPLICITLY NOT IN SCOPE: judging any of
the thirteen cells, SR-161/LLR-183/TC-178, the traced-only `module`/
`code_symbol` movement on LLR-035–LLR-200 and LLR-160 (declared traced, no
judgment owed), and any Status or snapshot effect.
