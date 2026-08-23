+++
id = "WI-484"
title = "Concern/hat references on SR and LLR rows and the generated component view: effective sets derived never copied, components.derived.toml generated, detail_doc retired (OI-32 ruled (d), 2026-08-20)"
specref = "docs/requirements/open-items.toml#OI-32"
workstream = "requirements"
sr_refs = []
needs = []
buildtier = "strong"
safety_class = "spine"
priority = 2
+++

## Context

**SLICES 1–4 LANDED (2026-08-20, 2026-08-22, 2026-08-23 ×2) — the row is
ACTIVE, not complete.** Phases 0, 1, 3 and 5 shipped whole; phase 2's backfill is
DONE and its writer is still owed; phase 4 is untouched and blocked. What is
still owed, in the order it should be taken:

1. ~~**Phase 2's judgement backfill.**~~ **DONE, slice 2 (2026-08-22)** — record:
   `docs/log.d/2026-08-22-wi484-hatrefs-backfill.md`. **55 SR cells and 8 LLR
   own refs** written by per-row judgement, against one stated rule (attribute a
   hat only where THAT hat's own `listens_for` names a failure the row prevents
   — not "which lens could be held up to it", which with nine `always` hats
   fills every cell and means nothing). `hat_refs` now stands on 72 of 74 SRs
   and 9 of 171 LLRs; coverage moved **184 → 4 of 245** uncovered by effective
   set, and unattributed hats **5 → 1**. The two known poison rows were read
   individually and BOTH STAY EMPTY: `SR-015`'s refusal of `hat.PERFORMANCE`
   is argued and correct, and no other hat bears once the checker splits to
   `SR-157`; `SR-040`'s struck lenses are not resurrected because the row itself
   records that their subject is gone. The four remaining uncovered rows are
   exactly those two plus their sole children (`LLR-015`, `LLR-037`), which is
   the derivation reporting correctly. `SAFETY` is the one hat nothing is
   attributable to — evidence for the open owner call in `hats.toml`'s header,
   not a hole. 160 of the 162 LLRs with no own cell are covered by INHERITANCE
   and need none.
2. **Phase 2's writer — STILL OWED, and slice 2 named its blocker.** Nothing
   composes the cell yet: `hats.applicable` + `plan_briefs.hat_surface` still
   only RENDER the questions into a brief. The blocker is a mismatch, not a size
   judgement: `{{HAT_QUESTIONS}}` has exactly ONE consumer,
   `prompts/dual-plan-planner.template.md`, whose output contract is a Plan-WI
   table (`Plan-WI | Title | Covers | Interfaces | Predecessors`) directing every
   perspective's answer into `## Notes` — **that brief mints no spine row at
   all**, so a write instruction appended to `hats.brief_block` would ship every
   adopter an instruction its own output contract makes unfollowable. The session
   that mints SR/LLR rows reads the `spine-authoring` skill instead, a different
   surface with a three-way per-agent fan-out under `--check-agents`. Widening
   the Plan-WI output contract vs stating the obligation at the spine-authoring
   tier is the decision this item owes.
3. **Phase 2's duplication.** The 17 migrated rows now state the attribution
   TWICE — once in `hat_refs`, once in the `Rationale` prose it came from.
   Deleting the prose touches an **approved** cell on Approved rows, so it is
   owner-adjacent and deliberately not taken here; the cell is the record and
   the prose is now commentary.
4. ~~**Phase 3 — the generated component view.**~~ **DONE, slice 3
   (2026-08-23)** — record: `docs/log.d/2026-08-23-wi484-component-view.md`.
   `gen_components.py`, `docs/requirements/components.derived.toml`, its
   `[generated]` row, its `component-view` freshness step and its `WIRED` entry
   landed together (the wiring test was driven RED in both directions first),
   plus a `trunk_step.REGEN_STEPS` entry and the adopter surface. `detail_doc`
   is RETIRED: no live CMP row carried it, so nothing needed migrating; the
   column is gone from the template, both carrier maps, `PROCESS_OPTIONS.md` and
   the test fixtures. The three coverage edges were RE-MEASURED (the brief's
   counts had all moved) and answered IN THE OUTPUT: the **5** childless SRs
   (not 12, and all five now `Approved`) are one counted repo-wide `[unplaced]`
   list, with the view deliberately NOT distinguishing "not yet decomposed" from
   "constraint over everything" because no registry cell does and a per-repo
   list of never-members has no place in shipped machinery; the **7**
   multi-component SRs (not 6) appear in EVERY component they reach and in each
   one's `sr_shared_refs`; seams DO enter the view, with all **130** placed
   (**62** by tag, 68 by endpoint resolution through `trace_text.norm_module`)
   and an unplaceable one named rather than dropped. Spine acts, all `Drafted`
   on the standing precedent: `LLR-199`, `TC-195`, `IF-139`–`IF-143`.

5. **Phase 4 — knowledge derived from concerns — has a blocker the brief did not
   know about.** `hats.py` enforces a STRICT unknown-key refusal
   (`REQUIRED_KEYS`, and `hats.py` raises on any extra key), and it has no
   notion of an optional key: adding `knowledge` to the roster therefore either
   makes it MANDATORY on all 16 live rows and all 16 shipped-template rows, or
   requires an `OPTIONAL_KEYS` concept minted first. `hats.toml` is also
   declared OWNER TEXT in its own header, so filling the values is not an
   agent's act.
6. ~~**Phase 5 — the amend-without-flip guard.**~~ **DONE, slice 4
   (2026-08-23)** — record: `docs/log.d/2026-08-23-wi484-amend-guard.md`.
   `staged_hat_refs_findings` is an ARM of the existing guard, not a new rule:
   it reads the one amendment set `staged_spine_amendments` already computes and
   fires on `approved` non-empty + `Hat-Refs` absent from `traced`, warn-first,
   `--staged` only, never an exit code. The comparison is by CELL CLASS, which
   is the whole design — it is silent on the phase-2 backfill's own edit shape.
   Baseline: HEAD vs the index over rows approved on both sides, the guard's own
   population; `docs/archive/last_approved` was considered and declined (it would
   make the finding STAND until answered, but the ruled home and OI-33's timing
   argument both point at the commit) — that promotion is the next rung, on
   evidence that the warn is ignored. Two honest vacuities: a row minted in the
   same commit has no baseline, and a row below approval has blessed nothing to
   amend. Measured: over the last 100 commits, 70 approved-cell amendments and
   **46** firings (the other 24 are test-case rows, a tier with no such column).
   Spine acts, both `Drafted` on the standing precedent: `LLR-202`, `TC-198`.

7. **The staleness-granularity follow-up, RECORDED here rather than fixed** (it
   is item 5's successor, and slice 4 is why it is stated this precisely).
   `backlog_staleness_findings` blames the SR registry by LINE, so writing an
   INFORMATIVE cell re-dates the row: at slice 4 one such warn was still live
   (`WI-508: cites SR-163`, whose newest blamed line is its `hat_refs`). The
   obvious fix — blame only approved-class lines — is the WRONG filter, not
   merely an expensive one: it would also silence a re-pointed
   `SN-Refs`/`Boundary-Refs`, which are traced but SCOPE-bearing and are exactly
   what a citing WI must re-validate against. The exact alternative (recompute
   the clock through `split_changed_cells` over a rev range) trades the check's
   bounded cost and inherits the approved-only population. Which traced cells
   are staleness-bearing is a new classification — a ruling, not a patch. The
   limitation is STATED in the docstring with its measured instance, on the
   WI-362 precedent; building the detection is owed by nobody yet.

**What phase 0 RULED, since it was delegated to the execution:** the field is
`hat_refs` / column `Hat-Refs` — the owner's vocabulary (hats, not concerns)
carried in the house idiom. `hats_ref` is the one form no sibling column takes
(`sn_refs`, `boundary_refs`, `sr_refs`, `req_refs` are all singular-noun +
`_refs`); `concern_refs` was declined on `boundary_refs`' own minting rule, that
a refs column is named for the tier it resolves INTO — a `concern` cell
resolving against `[hat.NAME]` rows is exactly the vocabulary hop that rule
refuses. The id space is the **roster NAMES**; the `C-SEC-2`-style clause
numbering in eight rationale cells is prose that resolves nowhere, and it is NOT
promoted to a second id space.

Executes OI-32's ruling — (d) THE GENERATED VIEW — per the combined brief's
six phases (the brief is the row's recommendation cell; read it whole first):

- **Phase 0** reconciles the two hat vocabularies and SETTLES THE FIELD NAME —
  the owner's word (2026-08-20) was "hats_ref", the brief proposed
  `concern_refs`; one name, ruled here, used everywhere.
- **Phase 1** adds the field on SR and LLR rows to say which hats bear on the
  row; an LLR's EFFECTIVE set is DERIVED (own refs + inherited), never copied.
- **Phase 2** decides who writes it and runs the backfill over the live rows.
- ~~**Phase 3**~~ **DONE** — generates `docs/requirements/components.derived.toml`
  via `gen_components.py`, declared in `docs/stack.ini` `[generated]`;
  `detail_doc` retired with it.
- **Phase 4** derives knowledge packs from concerns via a `knowledge` field on
  `hats.toml`.
- **Phase 5** is OI-33's surviving residue: the amend-without-flip-style guard
  — a row whose normative cells move while its concern refs do not is a
  finding.

Coverage edges the brief said the execution must answer explicitly rather than
paper over — ANSWERED at slice 3 against re-measured counts (5 childless SRs, 7
multi-component, 62 of 130 tagged IF rows); see item 4 above. Standing
constraint from OI-30 D3, honoured: a GENERATED file never carries an approval
(`human_approval_through`).

**Sequencing, the owner's own note (2026-08-20):** the new field is NOT
anticipated to be an attested cell, so it can be tacked on AFTER the sitting
without re-opening anything signed — this row deliberately waits for the
sitting rather than racing it (priority 2). If the schema work surfaces
anything that IS attestation-bearing, stop and raise it rather than folding
it in. `safety_class = "spine"` because the field lands on SR/LLR rows and
the schema of record moves, even though the cells it adds are informative.
