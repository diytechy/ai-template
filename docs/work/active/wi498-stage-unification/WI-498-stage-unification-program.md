+++
id = "WI-498"
title = "The stage unification program: one axis, one vocabulary, one owner (OI-51 ruled 2026-08-21; plan v1 FINAL)"
specref = "docs/plans/2026-08-21-stage-unification-plan.md"
workstream = "scripts"
sr_refs = []
needs = []
buildtier = "strong"
safety_class = "spine"
priority = 3
+++

## Context

Executes the owner's 2026-08-21 OI-51 ruling: the bar/gate/clear vocabulary
retires onto one stage axis. The spec-of-record is the ruled plan
(docs/plans/2026-08-21-stage-unification-plan.md, v1 FINAL — the owner's
four answers are its §6) with the design record and the three measurement
docs (census, deep-check, schedule map) as evidence. This is a
MULTI-SESSION PROGRAM lane; each slice ends green at the commit bar and
lands the largest honest coherent piece.

**Program state:** slices 0 and 1 landed 2026-08-21; slices 2-5 remain, in
order, and slice 2 (selection re-keys at-or-above) is next. Slice 1 delivered
`kitlib/stage.py` (the declared inputs, the fingerprint, the format, the floor,
the fold and the common reader), `derive_stage.py` (the per-phase,
draft-excluded, floored derivation), the committed `docs/stage`, and a
`derived-stage` freshness step wired exactly like `derived-gate`. **`docs/gate`
remains and is still authoritative for every one of its readers** — that is the
plan's transitional dual state, and cutting them over is slice 2's job. Slice 2
inherits two things it should read first: `derive_stage.read(root)` is the
one-line common reader to point consumers at, and the banked finding that the
bar axis must be swept by VALUE (`"DevStg-`), not by constant name.

The slices, in the plan's order (§5):

0. **One enum home** — LANDED 2026-08-21. The eight-rung ladder, its order,
   `STAGE_OF`, `STAGE_DESC`, `LADDER_RUNGS` and `stage_ord` now live in
   `project-trajectory/scripts/kitlib/ladder.py` (pure data — it imports
   nothing); `derive_gate` re-exports the former spellings, `agent_common` and
   `traj_status` bind to the shared objects, and the equality pin in
   `tests/test_ratification_level.py` retired in favour of identity assertions
   (WI-448 precedent). A FIFTH, unpinned copy the design record's §3 inventory
   missed — `traj_status._STAGE_LABELS` — died with it. `check_vocab` needed no
   change (its `DevStg-*` occurrences are all migration-shim alias tables).
   Owned by a Drafted mint, LLR-184 + TC-179, single-tagged `CMP-006`; the mint
   drags no bar (phase 5 was already floored). Adopter-facing: a RESYNC_PACK
   entry, the MAPPING row, the kit-contents README row. Record:
   `docs/log.d/2026-08-21-wi498-stage-unification.md`, "Slice 0".
   NOT touched, deliberately: `check.py`'s `BAR_*` literals and `derive_gate`'s
   bar ordinals / `BAR_NAMES` / `BAR_ORDER` / `STAGE_BAR` — the bar axis dies
   with slice 2, and slice 0 only extracts what survives.
1. **derive_stage + docs/stage + the common reader** — LANDED 2026-08-21.
   All nine deep-check corner cases are driven acceptance tests
   (`tests/test_kitlib_stage.py` for the five that are carrier properties,
   `tests/test_derive_stage.py` for the four needing real rows). The design
   decisions worth carrying forward: the reader takes the derivation as an
   ARGUMENT (kitlib may import no sibling, and the rung logic is rewritten by
   slices 2-3, so moving it would be work performed twice); the effective stage
   is the MIN over phases that have EARNED a rung — max would be a high-water
   reading process.md §4 forbids as a headline — with sentinel-carrying phases
   ignored, which is what stops one draft collapsing the repo; and the floor is
   a SELECTION guarantee with the honest unfloored value recorded beside it.
   `docs/stage` is key=value, not positional. Owned by LLR-185/186 + TC-180/181,
   single-tagged CMP-006. Record: `docs/log.d/2026-08-21-wi498-stage-unification.md`,
   "Slice 1".
   NOT touched, deliberately: no consumer re-keyed (slice 2), and the
   Impl/Release discriminator is unchanged (slice 3) — the effective stage is
   the designed aggregation over TODAY's rung mapping.
2. **Selection re-keys at-or-above** — gates= sets re-derived deliberately
   per step; bar constants deleted; all docs/gate readers onto the common
   reader.
3. **Ladder re-discrimination + the phase rule** — all-Founded →
   DevStg-Impl; Release evidence-gated (unreachable until the carrier row
   lands — honest); the authoring-time decrease check with exactly the
   LLReqs→Arch exemption.
4. **Event detectors over stage history** — phase-drop anchors; tier
   signal fixed and re-keyed (fold WI-497 if still open); dead
   read_declared removed.
5. **Vocabulary + migration** — PROCESS.md §4 + skills; check_vocab alias
   generation (reviewed, not scripted); RESYNC_PACK entries; fold WI-493;
   the 648-site sweep.

The test-evidence carrier (Release's input) is its OWN future row —
slice 3 does not wait for it. Standing constraints: adopter-facing changes
carry RESYNC entries; scaffold-surface changes are verified by
bootstrapping a real scaffold; byte-capped docs per the byte-budget-guard
convention; spine tiers human-held — any Approved-row amendment the sweep
needs goes to the owner, not the worker.
