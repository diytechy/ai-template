## 2026-08-30 — WI-546: the WI-484 delegated residue — the hats.toml knowledge value-pass and the 17 approved-cell Rationale attribution deletions

Deferred open items: none — both edits are listed here for the owner's review at return, as the delegation asked; nothing is owed a ruling.

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

The WI-484 slice-2 backfill left the deriving-hat attribution stated **twice** —
once in the `hat_refs` cell (the record), once in the `Rationale` prose as a
`Hat-derived (hat.X …)` note. This deletes the prose note; `hat_refs` is
untouched and remains the record. **Amendment scope, deliberately narrow:** only
the `Hat-derived (…)` attribution note is removed — the hat name(s), any
clause-id (`C-SEC-2`…) and provenance-doc citation *inside that note*, and the
cross-hat gloss. The substantive derivation reasoning that followed it is KEPT
(recapitalised at the join). Clause-ids that sat in the *retained* reasoning were
left as-is; Phase 0 already ruled they resolve nowhere, and re-writing them is
out of this WI's scope.

These 17 rows are all `Approved`; the amendment proceeds under ordinary review
(`DevStg-Needs` human-held only), and the snapshot diff against
`docs/archive/last_approved/` carries the identical set for the re-attestation
brief compiled at RETURN. The Phase-5 amend-without-flip guard warns (never
gates) that a `Rationale` cell moved while `Hat-Refs` stayed put — which is
EXACTLY what this WI does on purpose: the deletion removes only the duplicate
attribution, the hats that reach each row are unchanged, and `hat_refs` is
therefore correctly left as the record. The guard cannot tell attribution-
removal from a substance change, so it fires; "leave it deliberately" (the
guard's own second option) is the right call here, and this fragment is that
record. **The two "poison" rows SR-015 and SR-040 (both `hat_refs = []`/absent)
are NOT touched** — their `hat.PERFORMANCE`/`hat.UX-ENGINEER` prose is an argued
*refusal* of attribution, the record itself, not a duplicate.

| SR | `hat_refs` (unchanged) | prose note removed |
|---|---|---|
| SR-024 | TEST-ENGINEER | `Hat-derived (hat.TEST-ENGINEER): ` label |
| SR-033 | PERFORMANCE | `Hat-derived (hat.PERFORMANCE), and ` label |
| SR-043 | SECURITY | `Hat-derived (hat.SECURITY): ` label |
| SR-052 | ACCESSIBILITY | `Hat-derived (hat.ACCESSIBILITY): ` label |
| SR-053 | CONSISTENCY | `Hat-derived (hat.CONSISTENCY): ` label |
| SR-054 | UX-DESIGNER, UX-ENGINEER | `Hat-derived (hat.UX-DESIGNER + hat.UX-ENGINEER): ` label |
| SR-111 | MAINTAINER | whole `Hat-derived (hat.MAINTAINER): C-MNT-7 … stands without the citation.` sentence pair — see note below |
| SR-112 | MAINTAINER | whole `Hat-derived (hat.MAINTAINER): … stands without the citation.` sentence pair — see note below |
| SR-129 | TEST-ENGINEER | `Hat-derived (hat.TEST-ENGINEER): ` label |
| SR-144 | UNATTENDED-OPS | `Hat-derived (hat.UNATTENDED-OPS): ` label |
| SR-146 | SECURITY | `Hat-derived (hat.SECURITY): ` label |
| SR-147 | TEST-ENGINEER | `Hat-derived (hat.TEST-ENGINEER): ` label |
| SR-149 | MAINTAINER | `Hat-derived (hat.MAINTAINER): ` label |
| SR-167 | PERFORMANCE | `Hat-derived (hat.PERFORMANCE): ` label |
| SR-175 | DATA-PROTECTION, LEGAL, SECURITY | leading `Hat-derived (hat.DATA-PROTECTION, with hat.SECURITY C-SEC-5 and hat.LEGAL C-LEG-3 … clause texts in docs/plans/…): ` parenthetical |
| SR-176 | DATA-PROTECTION | leading `Hat-derived (hat.DATA-PROTECTION, C-DPR-2 — clause text in docs/plans/…): ` parenthetical |
| SR-177 | PERFORMANCE | leading `Hat-derived (hat.PERFORMANCE, C-PRF-1 — clause text in docs/plans/…): ` parenthetical |

**SR-111 / SR-112 exception, flagged for the owner:** these two removed the
WHOLE attribution sentence pair rather than just the label, because each ends
with its own admission that *"the sentence above stands without the citation"* —
the `C-MNT-7` note there is self-described as removable commentary, and what it
restated (a scaffold with no recorded origin cannot identify its kit version) is
already the row's opening sentence. Nothing unique to the requirement was lost.
If the owner wants the `C-MNT-7` clause reference preserved, restore from
`docs/archive/last_approved/docs/requirements/system-requirements.toml`.

### Harness

Both edits are TOML value/prose changes to the requirements spine; no script
behaviour moved. `tests/test_hats.py` was widened (commit `ee0adb92`) to admit
the optional `knowledge` key that `hats.py` `OPTIONAL_KEYS` already allowed.

- Smoke tier + budget (the per-commit bar): `python -m pytest -q -n auto -m
  smoke` → **1424 passed, 6 skipped, 32.24 s**; `python
  scripts/check_smoke_budget.py --mode enforce` → **29.6 s vs 60 s budget →
  within**.
- Touched module: `python -m pytest -q tests/test_hats.py` → **55 passed**.
- Spine validators: `python project-trajectory/scripts/trace.py` → **exit 0**
  (the one `FINDING` names `LLR-197`/`WI-448`, present at the branch base
  `751eb058` and untouched here); `python project-trajectory/scripts/check.py`
  → **RESULT: PASS** (derived-stage / approval-fresh SKIP on a work branch by
  design, concurrency-restructure §5.2).
- Full unfiltered suite (`python -m pytest -q -n auto`): run at close before
  claiming the WI done — result pasted in the closing commit.
