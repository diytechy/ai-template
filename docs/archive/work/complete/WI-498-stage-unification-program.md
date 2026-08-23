+++
id = "WI-498"
title = "The stage unification program: one axis, one vocabulary, one owner (OI-51 ruled 2026-08-21; plan v1 FINAL)"
specref = ""
workstream = "scripts"
sr_refs = []
needs = []
buildtier = "strong"
safety_class = "spine"
priority = 3
+++

## Deliverable

**CLOSED COMPLETE 2026-08-22.** All six ruled slices landed 2026-08-21
(slice 5 recovered from an interrupted session, residue reconciled); the
adversarial program close ran 2026-08-22 (internal Opus + cross-family
Sol, docs/reviews/2026-08-22-wi498-program-close/) and its 17-item
consolidated worklist was executed in full — including both reviewers'
Release-producer mutants now redding the rebuilt pins, the staged-
divergence promotion (OI-31's gap closed), the five false blessed prose
cells re-authored, and the stale-row census rebuilt BY VALUE (22 rows,
carried by WI-501). The signed figures were independently reproduced
(2831/14 exact at the approval commit). Every item the close owed is
dispositioned: WI-473 closed complete-with-supersession; the stale
Approved cells re-scoped into WI-501; `docs/process.toml` dropped from
DECLARED_INPUTS by owner ruling, pinned; PB-002 and PB-004 re-measured on
the live machinery. What the program deliberately leaves open has rows:
WI-500 (the test-evidence carrier that makes Release reachable), WI-501/
WI-502 (the cell repairs + the mechanized cross-check), WI-503 (the
ratify-brief immutability split), and the wi455/wi448/wi483/wi484 lanes
it unblocked or reshaped. The spine mints it produced were approved by
the owner's 2026-08-22 written act (ac121647). One axis, one vocabulary,
one owner — delivered.

## Context

Executes the owner's 2026-08-21 OI-51 ruling: the bar/gate/clear vocabulary
retires onto one stage axis. The spec-of-record is the ruled plan
(docs/plans/2026-08-21-stage-unification-plan.md, v1 FINAL — the owner's
four answers are its §6) with the design record and the three measurement
docs (census, deep-check, schedule map) as evidence. This is a
MULTI-SESSION PROGRAM lane; each slice ends green at the commit bar and
lands the largest honest coherent piece.

**Program state:** slices 0-5 ALL LANDED 2026-08-21. The build is done; what
the program row still owes is the CLOSE (below).

Slice 2 re-keyed the whole harness selector onto the effective stage and deleted
the bar constants, the product floor and the advisory tier. Slice 3 closed
OI-51's vacant rung — a spine decomposed and TC'd through the test tier reads
**`DevStg-Impl`**, and **`DevStg-Release` is returned by nothing** (evidence-
gated, unreachable until the test-evidence carrier, its own separately-sequenced
row, lands) — and armed the authoring-time phase rule WARN-FIRST and UNWIRED
(`derive_stage --phase-rule`). Slice 4 cut both EVENT detectors onto stage
history and folded WI-497.

**Slice 5 finished the unification: `docs/gate` IS GONE, and so is the axis.**
All four remaining readers were cut over — the three DISPLAY readers now render
the stage vocabulary, and `agent_common.spine_stage_of` (RATIFICATION AUTHORITY,
not display) now goes through the common reader, which makes its written trust
invariant true by construction instead of merely documented. Then the writer, the
`derived-gate` freshness step, the file, `gate.template` and the scaffold row all
retired together. **`derive_gate.py` was renamed `spine_rules.py`** — 1,523 lines
to ~800 — because what survives derives no gate and writes no file: the row
predicates, the maturity tables and the rung fall-through, paired with
`spine_carrier` (the carrier LOADS rows, the rules JUDGE them). **WI-493 folded
and closed**: the ratification dial `human_ratification_through` now takes a
`DevStg-*` rung, and `DIAL_HOLDS` retired rather than re-keying because under one
vocabulary the dial and the stage are the SAME ladder, so the bridge had nothing
left to bridge. The vocabulary sweep re-taught PROCESS.md §4, PROCESS_OPTIONS.md's
phase-anchor grammar and the `gate-advance` skill, `check_vocab` gained the
reviewed anchor aliases, and RESYNC_PACK carries one migration entry set an
adopter can execute the whole program from.

**WHAT THE PROGRAM CLOSE STILL OWES** (the orchestrator's, not a slice worker's):

1. **WI-473's disposition.** Its row is still in `docs/work/queued/` and its
   mechanism (the monotonic product floor) was SUPERSEDED by slice 2 under the
   ruled plan. It SHIPPED and was then superseded, so `complete` versus
   `cancelled` is a real judgement. Whoever closes it also owns
   `docs/work/queued/WI-473-monotonic-product-floor.md:62`, which cites the
   deleted `tests/test_product_floor.py`.
2. **SEVEN APPROVED spine rows now describe a system that no longer exists.**
   The seventh, found at the slice-5 close, is the sharpest: **SR-148**'s
   ACCEPTANCE CRITERION grades the system at `human_ratification_through = 0`
   and "levels 1 through 4", the 0-4 ordinal WI-493 retired — an Approved row
   whose test cannot be run as written. Its meaning survives (the re-key is
   behaviourally inert by the driven equivalence) but its literal values are
   unreachable. The other six are
   LLR-050 ("Derived-gate computation + hybrid cache"), LLR-051, LLR-142,
   LLR-148, LLR-157 ("The second axis...") and SR-006. Slice 5 re-pointed only
   what a rename or a move makes mechanically wrong (the `module =` carriers, and
   LLR-148's, because `--next-phase` moved to `derive_stage.py`); it did NOT
   re-author the design prose, because that is a ratification-bearing act and this
   repo holds every rung. LLR-050 in particular designates a DELETED behaviour
   whose successors already have their own rows (LLR-185/186).
3. **The `DECLARED_INPUTS` cost model, measured and handed over.**
   `kitlib/stage.py` declares `docs/process.toml` a derivation input although the
   derivation does not read it, defending the over-inclusion as costing "a
   spurious re-derivation (milliseconds, correct answer)". That holds for
   `read_stage` and NOT for `--check`, which hard-fails — so the real price is a
   red commit bar after any policy-dial edit. Driven at the slice-5 close: a
   `privacy_check` write re-staled `docs/stage` and took the pre-commit floor
   down. NOT changed, because ruled plan §2 names the file in the input set —
   the owner should re-decide it with the corrected cost stated.
4. **PB-002 needs a real re-measurement.** Its metric and `fig:` provenance name
   `derive_gate.py --check`, pinned to `rev=94489f7a`. The slice-5 sweep had
   rewritten the command and left the revision, falsifying the provenance and
   naming a command that can no longer run; that hunk was REVERTED at the close
   rather than re-pointed, because a `fig:` line is a claim about how a figure
   was produced. A fresh measurement against `derive_stage.py --check` with a new
   revision stamp is a small row of its own.
5. **Final verification + the owner handoff**, and the smoke wall-clock question,
   which remains OI-52's.

**Slice 5 landed across THREE sittings, two of them interrupted before
committing.** The third reconciled ~121 files of residue against this plan
before doing new work: the build was kept whole and verified piece by piece,
three hunks were REVERTED as out of scope (a ruled OI-51 owner record, PB-002's
`fig:` provenance, and the superseded WI-473 spec — all three cases of a
mechanical rename rewriting a record of the PAST), and six defects were
corrected that only running things could find, including a `KeyError` crash in
`check_vocab` itself and three failures in `tests/test_pre_commit_hook.py` that
the smoke tier structurally cannot see. Full account:
`docs/log.d/2026-08-21-wi498-stage-unification.md`, "Slice 5".

The per-slice records, the banked findings and the deferred-item declarations are
all in `docs/log.d/2026-08-21-wi498-stage-unification.md`.

The slices, in the plan's order (§5):

0. **One enum home** — LANDED 2026-08-21. The eight-rung ladder, its order,
   `STAGE_OF`, `STAGE_DESC`, `LADDER_RUNGS` and `stage_ord` now live in
   `project-trajectory/scripts/kitlib/ladder.py` (pure data — it imports
   nothing); `spine_rules` re-exports the former spellings, `agent_common` and
   `traj_status` bind to the shared objects, and the equality pin in
   `tests/test_ratification_level.py` retired in favour of identity assertions
   (WI-448 precedent). A FIFTH, unpinned copy the design record's §3 inventory
   missed — `traj_status._STAGE_LABELS` — died with it. `check_vocab` needed no
   change (its `DevStg-*` occurrences are all migration-shim alias tables).
   Owned by a Drafted mint, LLR-184 + TC-179, single-tagged `CMP-006`; the mint
   drags no bar (phase 5 was already floored). Adopter-facing: a RESYNC_PACK
   entry, the MAPPING row, the kit-contents README row. Record:
   `docs/log.d/2026-08-21-wi498-stage-unification.md`, "Slice 0".
   NOT touched, deliberately: `check.py`'s `BAR_*` literals and `spine_rules`'s
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
   MEANING: a closed `[p]-[reqs]`/`[g1]` records `DevStg-LLReqs` and  check_vocab: allow
   `[p]-[tests]`/`[g2]` records `DevStg-Impl` — both two rungs off the spelling  check_vocab: allow
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
5. **Vocabulary + migration** — LANDED 2026-08-21 (across three sittings; the
   first two were interrupted before committing and the third RECONCILED their
   residue against this plan before finishing — see the fragment's "Slice 5").
   `docs/gate`, `gate.template`, the `derived-gate` step and the whole bar axis
   are deleted; `derive_gate.py` is `spine_rules.py` (import-only — its CLI went
   with the file, and `--next-phase` was REHOMED onto `derive_stage.py` so the
   printed number and the recorded `phase =` cannot diverge). All four surviving
   readers cut over in TWO classes, deliberately: `agent_common.spine_stage_of`
   (ratification authority) onto the SELF-HEALING reader, the three display
   readers onto the COMMITTED record via `kitlib.stage.parse`, so a page and the
   file it cites describe one commit. **WI-493 folded and closed** — the dial
   takes a rung and `DIAL_HOLDS` RETIRED rather than re-keying, equivalence
   driven over all five former levels before the deletion. `check_vocab` gained
   the reviewed ANCHOR aliases (by MEANING, not spelling: `[g1]` →  <!-- check_vocab: allow -->
   `DevStg-LLReqs`, `[g2]` → `DevStg-Impl`); no VALUE alias generation was owed,  <!-- check_vocab: allow -->
   because the three shared bar spellings are all legal rungs — what migrates is
   the READING, by a RESYNC note. Record:
   `docs/log.d/2026-08-21-wi498-stage-unification.md`, "Slice 5".
   NOT touched, deliberately: the WI `bar:` frontmatter key (0 of 495 specs set
   it; its three values are rungs, so nothing mis-selects — the rename is a
   migration entry of its own), and the Approved design prose in item 2 above.

The test-evidence carrier (Release's input) is its OWN future row —
slice 3 does not wait for it. Standing constraints: adopter-facing changes
carry RESYNC entries; scaffold-surface changes are verified by
bootstrapping a real scaffold; byte-capped docs per the byte-budget-guard
convention; spine tiers human-held — any Approved-row amendment the sweep
needs goes to the owner, not the worker.
