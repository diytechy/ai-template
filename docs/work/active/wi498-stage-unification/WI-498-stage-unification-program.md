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

**Program state:** slice 0 landed 2026-08-21; slices 1-5 remain, in order, and
slice 1 (`derive_stage` + `docs/stage` + the common reader) is next. Its module
name is already reserved: the ladder took `kitlib/ladder.py` deliberately so
`kitlib/stage.py` — the plan §2 "kitlib stage module" holding the declared input
set, the fingerprint and the self-healing reader — lands above it with the pure
vocabulary strictly below.

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
1. **derive_stage + docs/stage + the common reader** — the designed
   effective per-phase stage (draft-excluded, floored), the input
   fingerprint over the DECLARED derivation inputs, the self-healing
   read-only reader. The deep-check's nine corner cases are this slice's
   driven acceptance tests.
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
