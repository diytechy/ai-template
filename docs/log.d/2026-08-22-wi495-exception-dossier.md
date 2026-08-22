## 2026-08-22 — WI-495: the interface-rework exception dossier (OI-49 ruled (b))

Deferred open items: none — the ratifying Status-change commit itself, and
`OI-60`'s pending re-point question (item 1's coordination note, no new
deferral) are what the owner is now owed; this row files no new open item.

**Why.** `OI-49` (ruled 2026-08-21) accepted the bulk of the 2026-08-15
interface rework's live `owner`/carriage/`;` state and named seven rows as
the named exception list still owed a read: the two unargued owner picks
(`IF-013`, `IF-044`), the five-row loaders-vs-decision split
(`IF-056`/`082`/`084` vs `IF-071`/`085`), `IF-131`'s single-constituent
carriage bundle, and the still-provisional `carried_by` depth bound of 2.
This row is the dossier that prepares the owner's ratifying commit with a
recommendation per item, and does not itself flip any status/approval cell.

**Deliverables.**
- `docs/plans/2026-08-22-interface-exception-dossier.md` — one read each,
  full reasoning, and a recommendation per item.
- Two `notes` cells written into `docs/requirements/interfaces.toml`
  (`IF-013`, `IF-044`) — traced, not ratified (both rows are `Drafted`, so
  no re-attest window opens): each states the reason its owner pick is the
  right one, so the cell is reviewable without redoing the read.

**Recommendation per item, one line each:**
1. `IF-013` -> `SR-006` (not `SR-007`): KEEP — the contract's central claim
   restates SR-006's requirement text almost verbatim; SR-007 governs a
   different observable. `IF-044` -> `SR-154` (not `SR-155`): KEEP — five
   of seven named call surfaces serve SR-154's routing capability directly,
   `planner_pair`/`planner_fallback` serve SR-155's round as one input among
   several, not the round itself. Both rows are OI-60-census members (no
   design-tier owner exists yet for `scripts/check`/`scripts/agent_route`);
   three of OI-60's four options leave `owner` untouched, its re-point
   option would supersede these picks — noted in the dossier, not
   pre-empted.
2. The five-row loaders-vs-decision split: KEEP all five as recorded —
   `LLR-049`'s own `code_symbol`
   (`component_top_view`/`component_findings`/…) matches `IF-056`/`082`/
   `084`'s loaders/joins contract exactly, `LLR-058`'s own `code_symbol`
   (`ready`/`frontier`/`evaluate`) matches `IF-071`/`085`'s frontier-decision
   contract exactly. No cell edit — the grounding already lives in each
   row's own "Contract: IF-056's"/"Contract: IF-071's" prose.
3. `IF-131`'s single-constituent bundle: RECOMMEND THE PLAIN RE-POINT — drop
   `carried_by = "IF-131"` from `IF-132` and let its existing prose stand
   alone, matching the identical-shape `IF-056`/`082`/`083`/`084` precedent,
   which states the same "declared separately, one contract" fact in prose
   rather than the carriage field. Not executed by this row — the field is
   part of the judgement under ratification.
4. `carried_by` depth bound of 2: KEEP PROVISIONAL — direct grep of the
   registry's 20 `carried_by` cells confirms all three carriers (`IF-102`,
   `IF-123`, `IF-131`) carry no `carried_by` of their own, so every live
   chain today is exactly one hop deep; the depth-2 warn has never been
   approached by real data, let alone tested.
5. `IF-097`/`IF-080`: VERIFIED CLOSED, no action owed. `IF-097`'s `;`-cell
   coverage residue is confirmed fixed — `check_trajectory._declared_seam_pairs`
   now splits on `;` (docstring reads in the past tense, landed at the
   2026-08-21 review's W-12, commit `3c27291c`). `IF-080`'s `this_project`
   reads unchanged and correct as the ruling's own record states.

**Gates**, real output, Windows, `.venv` Python 3.11.9, `-n auto`:

- `python -m pytest -q -n auto -m smoke`: **1368 passed, 5 skipped in
  63.24s**
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=d2b5c48b -->.
- `python project-trajectory/scripts/check_docs.py --root . --stale`: OK —
  1010 doc(s), 1345 intra-repo link(s), 0 broken (1 pre-existing orphan
  warning; the rest are non-blocking staleness hints unrelated to this
  registry-only change)
  <!-- fig: cmd="python project-trajectory/scripts/check_docs.py --root . --stale" rev=d2b5c48b -->.
- `python project-trajectory/scripts/check_trajectory.py --root . --strict`:
  **byte-identical** before/after (101 lines both sides) — HOLD. The one
  `ERROR` line present both before and after (`R-F WI-501` SpecRef residue)
  is pre-existing and unrelated to this row; confirmed by running the same
  command on a clean stash of this session's changes.
- `python project-trajectory/scripts/trace.py --root . --strict
  --strict-integrity`: **byte-identical** before/after (136 lines both
  sides) — HOLD. The two new `notes` cells were checked for the citation-
  frame advisory the WI-501 precedent hit (an `WI-495`/`OI-49`/`OI-60`
  token in the prose) and reworded to drop it before the final run; the
  before/after diff confirms zero new findings.

Registry-only change (two `notes` cells) plus a new plan doc, so the full
unfiltered suite is not owed by `CLAUDE.md`'s own rule — no script or
scaffold-surface change.

**Deviations from spec.** None on the substantive work. Two close-mechanics
corrections were needed beyond the spec's own text, both standard R-F/R-D
close hygiene rather than scope changes: (1) `WI-495`'s own `specref` is
cleared (`""`) at close per the `docs/specs/README.md` terminal-clears-
SpecRef convention (`R-F`), which every other closed WI in `docs/work/
complete/` already follows — the Deliverable and this fragment carry the
`OI-49` record instead; (2) the hand-authored `docs/status.md` bullet that
named this row while it was queued had its `WI-495` token scrubbed at close
(status.md is forward-only; the R-D guard catches a done id there), leaving
the dossier pointer and the `OI-49` reference in place.
