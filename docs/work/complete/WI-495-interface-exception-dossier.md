+++
id = "WI-495"
title = "The interface-rework exception dossier for the owner's ratifying commit (OI-49 ruled (b), 2026-08-21)"
specref = ""
workstream = "requirements"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "spine"
priority = 2
+++

## Deliverable

Dossier: `docs/plans/2026-08-22-interface-exception-dossier.md`. One read
each, full reasoning, and a recommendation per item — no status/approval
cell flipped anywhere; the ratifying Status-change commit stays the
owner's.

Per-item recommendation:
1. `IF-013`→`SR-006` (not SR-007): KEEP — the contract's central claim
   restates SR-006's requirement text almost verbatim, SR-007 governs a
   different observable. `IF-044`→`SR-154` (not SR-155): KEEP — five of
   seven named call surfaces serve SR-154 directly; `planner_pair`/
   `planner_fallback` serve SR-155's round as one input, not the round
   itself. Reason written into both rows' `notes` cells (traced, not
   ratified — both `Drafted`). Both rows are OI-60 census members; the
   dossier states what each of OI-60's four options would do to the pick
   without pre-empting OI-60's ruling.
2. The five-row loaders-vs-decision split (`IF-056`/`082`/`084` vs
   `IF-071`/`085`): KEEP all five — each candidate owner's own
   `code_symbol` cell (`LLR-049`: `component_top_view`/…; `LLR-058`:
   `ready`/`frontier`/`evaluate`) matches its claimed contract side
   exactly. No cell edit — the grounding already lives in each row's own
   "Contract: IF-056's"/"Contract: IF-071's" prose.
3. `IF-131`'s single-constituent bundle: RECOMMEND THE PLAIN RE-POINT —
   drop `carried_by = "IF-131"` from `IF-132`, matching the identical-shape
   `IF-056`/`082`/`083`/`084` precedent (prose, not the carriage field).
   Not executed here — the field is part of the judgement under
   ratification.
4. `carried_by` depth bound of 2: KEEP PROVISIONAL — direct grep confirms
   none of the three carriers (`IF-102`, `IF-123`, `IF-131`) carries a
   `carried_by` of its own, so every live chain is one hop deep; the
   depth-2 warn has never been approached by real data.
5. `IF-097`/`IF-080`: VERIFIED CLOSED, no action. `IF-097`'s `;`-cell
   coverage residue is confirmed fixed (`check_trajectory._declared_seam_pairs`
   now splits on `;`, landed at the 2026-08-21 review's W-12, commit
   `3c27291c`). `IF-080`'s `this_project` reads unchanged and correct.

Full session record: `docs/log.d/2026-08-22-wi495-exception-dossier.md`.

## Context

Executes OI-49's ruling (b) RATIFY WITH A NAMED EXCEPTION LIST. The bulk of
the LIVE `owner` cells is accepted by the ruling — NOT the superseded
2026-08-15 list of 21 (ten picks have since legitimately moved to the
design tier; the ruling text is explicit that a ratification quoting the
old log entry would sign a superseded list). What this row prepares, one
read each with a written recommendation:

1. **The two unargued picks** — `IF-013`→`SR-006` and `IF-044`→`SR-154`,
   recorded as bare pairs. Read the contract, write the reason (or the
   re-pick), so the cell becomes reviewable.
2. **The five-row loaders-vs-decision split** — IF-056/IF-082/IF-084
   (owner = the loaders/joins) versus IF-071/IF-085 (owner = the
   ready-frontier decision). The executor self-flagged this as its most
   overturnable call; it turns entirely on what each contract says
   CROSSES. Read all five contracts and recommend keep-or-repick per row.
3. **`IF-131`'s single-constituent bundle** — a carrier with one
   constituent is a pointer wearing composition's field. Justify it or
   recommend the plain re-point.
4. **The depth bound of 2** on `carried_by` — still explicitly provisional,
   never re-examined. State the evidence (nothing has wanted a third
   level) and recommend keep-provisional or ratify-as-bound.

The deliverable is a dossier (a plan doc under docs/plans/ per convention)
plus any cheap traced-cell reason annotations the reads justify. The
RATIFYING Status-change commit stays the owner's — this row must not flip
any status. IF-097 and IF-080 are CLOSED by the ruling's own record — do
not re-derive them; the `;`-cell coverage residue was separately fixed at
the 2026-08-21 review iterate (W-12), so the OI's IF-097 caveat is already
discharged — verify and say so in the dossier.
