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

**SLICES 1 AND 2 LANDED (2026-08-20, 2026-08-22) — the row is ACTIVE, not
complete.** Phases 0 and 1 shipped whole; phase 2's backfill is DONE and its
writer is still owed; phases 3, 4 and 5 are untouched. What is still owed, in
the order it should be taken:

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
4. **Phase 3 — the generated component view.** `gen_components.py`,
   `docs/requirements/components.derived.toml`, its `[generated]` row, its
   `check.py` freshness step and its `WIRED` entry in
   `tests/test_generated_freshness_wiring.py` (that test fails both ways, so the
   four land together), plus `detail_doc`'s retirement. **Untouched.** The
   coverage edges the brief demands explicit answers for — the 12 childless SRs
   (3 of which never will have children), the 6 multi-component SRs, and whether
   the 57-of-125 tagged IF rows enter the view — are all Phase 3's and are all
   still unanswered.
5. **Phase 4 — knowledge derived from concerns — has a blocker the brief did not
   know about.** `hats.py` enforces a STRICT unknown-key refusal
   (`REQUIRED_KEYS`, and `hats.py` raises on any extra key), and it has no
   notion of an optional key: adding `knowledge` to the roster therefore either
   makes it MANDATORY on all 16 live rows and all 16 shipped-template rows, or
   requires an `OPTIONAL_KEYS` concept minted first. `hats.toml` is also
   declared OWNER TEXT in its own header, so filling the values is not an
   agent's act.
6. **Phase 5 — the amend-without-flip guard.** Untouched. The mechanism the
   brief names is in place and ready (`split_changed_cells` /
   `spine_cell_class`), and `Hat-Refs` is now classified `traced` at both tiers,
   which is the precondition. The interaction slice 1 flagged is now GONE — the
   backfill leaves only 4 of 245 rows with no effective set, so the guard has
   something to compare on nearly every row. Slice 2 replaced it with a sharper
   one, measured: `backlog_staleness_findings` blames the SR registry by LINE, so
   writing an INFORMATIVE cell re-dated five open WIs' cited rows and raised
   seven warns. A `blame` line time cannot tell a normative cell from a traced
   one; the guard must key off `split_changed_cells`' class split, which is the
   whole reason `Hat-Refs` was classified rather than left residual.

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
- **Phase 3** generates `docs/requirements/components.derived.toml` via a
  `gen_components.py`, declared in `docs/stack.ini` `[generated]`;
  `detail_doc` retires.
- **Phase 4** derives knowledge packs from concerns via a `knowledge` field on
  `hats.toml`.
- **Phase 5** is OI-33's surviving residue: the amend-without-flip-style guard
  — a row whose normative cells move while its concern refs do not is a
  finding.

Coverage edges the brief says the execution must answer explicitly rather
than paper over: 12 SRs have no LLR (SR-034, SR-114, SR-036 never will);
6 SRs span more than one component; 57 of 125 IF rows carry a component tag.
Standing constraint from OI-30 D3: a GENERATED file never carries an approval
(`human_approval_through`).

**Sequencing, the owner's own note (2026-08-20):** the new field is NOT
anticipated to be an attested cell, so it can be tacked on AFTER the sitting
without re-opening anything signed — this row deliberately waits for the
sitting rather than racing it (priority 2). If the schema work surfaces
anything that IS attestation-bearing, stop and raise it rather than folding
it in. `safety_class = "spine"` because the field lands on SR/LLR rows and
the schema of record moves, even though the cells it adds are informative.
