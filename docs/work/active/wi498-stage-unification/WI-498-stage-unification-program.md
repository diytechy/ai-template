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

**Program state:** slices 0-4 landed 2026-08-21; slice 5 (vocabulary +
migration) is the last one and is next.
Slice 2 re-keyed the whole harness selector onto the effective stage:
`check.py` reads `docs/stage` through `derive_stage.read` and reads `docs/gate`
NOWHERE, the bar constants and the membership rule are deleted, and the product
floor and advisory tier retired with the draft-collapse they compensated for.
Slice 3 then closed OI-51's vacant rung: a spine decomposed and TC'd through the
test tier reads **`DevStg-Impl`**, and **`DevStg-Release` is returned by
nothing** — evidence-gated, unreachable until the test-evidence carrier (its own
separately-sequenced row) lands. It also armed the authoring-time phase rule
WARN-FIRST and UNWIRED (`derive_stage --phase-rule`).

**`docs/gate` is still WRITTEN and still freshness-gated, and after slice 4 the
hand-off is EXACT: FOUR readers remain and all four are slice 5's.** Both EVENT
detectors are cut over. What is left is three DISPLAY readers (`traj_parse`,
`traj_panels`, `traj_status`) and — not display, and missing from slice 2's own
enumeration — `agent_common.spine_stage_of`, which scrapes `stage=` off the
`# basis:` line and feeds `human_holds`, i.e. RATIFICATION AUTHORITY. That fourth
reader is why the `derived-gate` freshness step stays wired until the file
retires: three of the four draw pages, one decides who may ratify.

Slice 5 inherits, all in the fragment's per-slice sections and the findings below
them: the OI-30 D2 ceiling's old→new mapping (the BAR half is kept verbatim and
dies WITH the file); the verified fact that `DIAL_HOLDS` needs no change because
rungs 6/7 stay inert at every dial; slice 4's ANCHOR TRANSLATION table, which is
the live example of why the shared spellings cannot be remapped mechanically
(`[p]-[reqs]` records `DevStg-LLReqs`, two rungs off the word it shares); and the
standing warning that the two repo-global frame rungs give the stage axis no
per-phase signal on THIS repo until the frame settles — now visible as the
detector's own stand-down warn rather than as silence.

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
2. **Selection re-keys at-or-above** — LANDED 2026-08-21. Every step's
   `gates=` set re-derived one at a time into a from-stage threshold under one
   stated rule (the lowest rung at which the artifact the step grades must
   exist and be complete), with the per-step table in the log fragment. The
   finding that shaped it: the retired bar was a MIN over every row, so
   `DevStg-Tests` was reached only by a fully decomposed spine — the
   `DevStg-Impl` RUNG — and mapping a bar tag to the floor of its span would
   have started five steps three rungs early. `traceability` lands at
   `DevStg-Impl` because its orphan rules ARE the rung-4/5 predicates.
   `format`/`lint`/`tests+coverage` become reachable from a derived value for
   the first time (OI-51's defect); `registry-integrity` is the one behavioural
   delta; `design-flows`/`trajectory`/`ratify-fresh` widen to the applies-when
   their own comments already claimed. `product_floor` and the advisory tier
   are DELETED. Flag surface: `--stage` canonical, `--gate` silent,
   `--stage-cleared` warns. Adopter `[step:*]` key `gates=` → `from-stage=`,
   legacy translated. Record:
   `docs/log.d/2026-08-21-wi498-stage-unification.md`, "Slice 2".
   NOT touched, deliberately: the two SEVERITY promotions stay at the Impl
   rung (widening one is a policy change, not a re-key); the WI `bar:`
   frontmatter key keeps its name (its three values are rungs and select
   identically — the rename is slice 5's); the detectors' internals and the
   display readers of `docs/gate` are left FUNCTIONING for slices 4 and 5.
3. **Ladder re-discrimination + the phase rule** — LANDED 2026-08-21. The
   Impl/Release cell discriminator is DELETED rather than re-polarized (both
   arms landed on Impl), so all-Founded → `DevStg-Impl` and `DevStg-Release` has
   no producer — pinned exhaustively (128 spines) and structurally (no
   `return STAGE_RELEASE` in the source). OI-30 D2's guard survives as that
   absence on the stage axis; its BAR half is kept verbatim while `docs/gate` is
   still written. The authoring-time decrease check lives in
   `derive_stage.phase_rule_findings` (`--phase-rule`, WARN-first, `--strict`
   promotes, unwired) with exactly the `LLReqs → Arch` exemption. Measured: this
   repo fires it zero times over 80 commits, so no allowlist was seeded. Nine
   test pins inverted, not the five the deep-check counted.
4. **Event detectors over stage history** — LANDED 2026-08-21, folding and
   closing **WI-497**. The phase-drop detector reads `docs/stage`'s
   `per-phase-live` through the common reader, and an anchor's recorded reach is
   a LADDER RUNG. Two decisions carry it. (a) THE ANCHOR TRANSLATION IS BY
   MEANING: a closed `[p]-[reqs]`/`[g1]` records `DevStg-LLReqs` and
   `[p]-[tests]`/`[g2]` records `DevStg-Impl` — both two rungs off the spelling
   they share with the ladder, in the direction that would make the detector
   under-report. Legacy anchors are TRANSLATED, never re-recorded (a WI title is
   committed history); new ones take the rung itself,
   `[<phase>]-[DevStg-<Rung>]`. (b) THE LIVE READING, NOT THE SETTLED ONE — a
   redraft IS the event, and the settled fold excludes drafts by construction,
   which also discharges slice 3's banked rung-3 tension: the recursion is
   visible where events are detected while selection stays uncollapsed. New: the
   detector ABSTAINS on the three repo-global rungs and says so once, instead of
   attributing a repo-wide fact to a phase. `intake._gate_moved` →
   `_stage_moved`, a two-point delta of `docs/stage`'s `stage` field across the
   two trees; `tier_signal`'s `strong` arm is driven end-to-end and proven able
   to fire for the first time since the derived-gate migration. The dead
   `read_declared`-reads-`docs/gate` claim is corrected in both homes (the
   function is live and untouched; only the claim was false). Record:
   `docs/log.d/2026-08-21-wi498-stage-unification.md`, "Slice 4".
   NOT touched, deliberately: the display readers and the ratification reader of
   `docs/gate` (slice 5), and the prose surfaces that still teach
   `[phase]-[g1|g2]` — the anchor GRAMMAR moved here, the teaching moves there.
5. **Vocabulary + migration** — PROCESS.md §4 + skills; check_vocab alias
   generation (reviewed, not scripted); RESYNC_PACK entries; fold WI-493;
   the 648-site sweep.

The test-evidence carrier (Release's input) is its OWN future row —
slice 3 does not wait for it. Standing constraints: adopter-facing changes
carry RESYNC entries; scaffold-surface changes are verified by
bootstrapping a real scaffold; byte-capped docs per the byte-budget-guard
convention; spine tiers human-held — any Approved-row amendment the sweep
needs goes to the owner, not the worker.
