## 2026-08-22 — WI-455 slice 3: SR-162 is decomposed, and the D-3 shed stops at its own census

Deferred open items: OI-60 — the D-3 `direction`/`this_project` shed was
measured before it was executed, and the measurement says the staged spec's
own precondition is unmet on 12 rows while `counterpart` means three different
things on the `Consumes` side. The registry was not touched; the question is
filed with the census, four options and a recommendation.

**One-line summary.** The lane's owner-directed orphan fold-in landed
(`SR-162` → `LLR-187` + `TC-182`, both `Drafted`); the D-3 shed the same
ruling unblocked did **not**, because the 129-row census taken before the
first edit found the transform to be a registry-wide schema change with two
unmet preconditions rather than the ~20-row cell pass `OI-54`'s blast radius
described.

### Deliverables

- **`LLR-187`** — *Boundary references as resolvable cells: the frame's own
  joins, the SR→crossing rule, and the severity split that makes both
  adoptable.* Module `project-trajectory/scripts/trace.py`, symbols
  `frame_findings`/`sr_boundary_findings`/`_frame_report_section`, component
  `CMP-006`, `Drafted`. The machinery was already delivered — the row RECORDS
  it. Two clauses of the parent are stated as NOT DISCHARGED in the tier's
  debt-stating pattern: the joined-seam signal-compatibility rule has no
  seam-to-seam join carrying a signal vocabulary to read (the carriage cell is
  the only such edge and it carries none), and the two-sided-change obligation
  is the parent's own named residual. The interface-cell half is claimed
  explicitly: the endpoint-pair cells and the closed `discrete`/`variable`
  vocabulary are `SR-162`'s observables, declared at trace's IF entries and
  executed by the generic checker that stays `LLR-003`'s — the carve-out
  ruled on the connectivity row, now written where it can be found.
- **`TC-182`** — Integration / Full, `Drafted`, verifying `SR-162` +
  `LLR-187` over five claims (hard resolution; the empty-entity-set guard that
  is a finding rather than a vacuous pass; real vacuity for a frameless
  project; the SR join at both severities; the carved-out signal vocabulary).
  Evidence is 13 EXISTING test nodes — twelve in
  `tests/test_external_frame.py`, one in `tests/test_trace.py` — so the row
  cites what runs, not what is wished for.
- **`OI-60`** (pending) — the shed's blocking question, with the census below
  as its body.
- Watermarks `LLR` 186 → 187, `TC` 181 → 182, `OI` 59 → 60, all via
  `trace.py --bump-ids`. Surfaces regenerated: report, open-items,
  `docs/stage` (`drafted` 0 → 2, rung unmoved at `DevStg-LLReqs`),
  `PROJECT_STATE.html`.

### The census — why the transform stopped

Taken over the live registry before any cell was edited: **129 rows, 85
`Consumes` / 44 `Provides`; `owner` is a design id on 86 and a requirement id
on 43.**

<!-- fig: cmd="python - # tomllib over docs/requirements/interfaces.toml + low-level-requirements.toml: direction split, owner tier, endpoint-vs-owner-module agreement" rev=2eae651e -->

| Class | Rows | What the shed does to it |
|---|---|---|
| Design-owned `Consumes` | 54 | 53 already satisfy `OI-54` (a) by construction — `counterpart` IS the owner row's module, the provider. Lossless. |
| — the exception | 1 (`IF-031`) | Owner is the module holding the CONSUMING code (`check_perf`); counterpart is the budgets registry. The one row authored under the reading that was not ruled. |
| Design-owned `Provides` | 32 | `this_project` equals the owner's module on all 32. Shed lossless. |
| Requirement-owned `Provides` | 12 | `this_project` names a real module and the target shape has **no cell that can hold it**. Shed is LOSSY. |
| Requirement-owned `Consumes` | 31 | `counterpart` is medium, consumer, or consumer-CLASS depending on the row. Per-row re-judgement, not a transform. |

The three findings, stated once:

1. **The ruled reading costs nothing to adopt** — it is already the authoring
   on 53 of 54 design-owned `Consumes` rows, which is why the question stayed
   invisible for so long.
2. **R4 conditions `this_project`'s death on derivability** (*"dies once
   derivable as owner→LLR→`module`"*), and it is underivable on exactly 12
   rows: `IF-001`, `IF-005`, `IF-009`, `IF-011`, `IF-013`, `IF-014`, `IF-015`,
   `IF-044`, `IF-053`, `IF-065`, `IF-076`, `IF-081`. Dropping the column there
   deletes the providing module outright, and with it the row's producer
   credit in the connectivity advisory and its source end in the declared-seam
   pairs that discharge the cross-component rule — a hard failure class from
   the tests rung upward, so the cost lands on adopters standing higher on the
   ladder than this repo.
3. **`counterpart` is tri-modal on `Consumes` rows** after `WI-469`'s medium
   pass: provider (the carrier rows), medium (`IF-070`, `IF-045`, `IF-025`),
   consumer class (the 16 rows tied to `B-05`). On the third group the ruled
   reading puts the counterpart *beside* `this_project` in the consumers list
   rather than opposite it — a shape `OI-54` does not state — and on the
   second the medium identity has no cell in the target shape at all.

And the scope fact behind all three: shedding two columns is registry-wide
over 129 rows plus the connectivity advisory, the declared-seam pairs, the
dashboard's seam orientation, the dual-plan IF surface, the shipped template
and interface guide (whose own rule is *"Direction drives ownership"*), the
process master's field list, the reference example's worked rows, structural
template parity, and a resync-pack entry. `OI-54` recorded a blast radius of
*"CELLS ONLY, ~20 rows … no re-attestation"*. Executing the larger thing under
the smaller sanction is what the stop declines to do.

**Per-row transform record: none — no row in `docs/requirements/interfaces.toml`
was edited.** That file is byte-identical to its state at the slice's start.

### Deviations from the slice brief

- The brief scoped **A** as the transform executed "in one reviewed pass per
  its staged spec", with a stop condition only for *no staged spec found*. A
  staged spec WAS found — R4 §1.4 of
  [`../plans/2026-08-15-retier-v2-one-decision-tiering.md`](../plans/2026-08-15-retier-v2-one-decision-tiering.md),
  which the brief's other sources point at — and the stop is on a different
  ground: that spec states a precondition (`this_project` dies *once
  derivable*) which the measurement shows unmet on 12 rows, and the ruling
  covering the ambiguity does not reach it. Stopped under the brief's
  standing instruction to stop rather than guess at an owner-level question,
  and filed as a row rather than as prose.
- Item 1 of the WI Context is therefore **not struck**; it is re-blocked, this
  time on a scoped row (`OI-60`) instead of on status prose. Items 2 and 3
  stay owed and are unaffected — both are executable now.
- `IF-031`'s owner cell was left alone though the census names it as
  mis-shaped under the ruled reading: it is one cell of the pass `OI-60` is
  about, and correcting it now would be a second pass over the same row.

### Gates

- Smoke: `python -m pytest -q -n auto -m smoke` — 1368 passed, 5 skipped,
  56.03 s.
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=2eae651e -->
- `python project-trajectory/scripts/check_docs.py --root . --stale` — 0
  broken references.
- `python project-trajectory/scripts/check_trajectory.py --strict` — exit 0.
- `python project-trajectory/scripts/trace.py` — integrity 0, orphans 13
  (`SR-162` is no longer among them; the report's join now reads
  `SR-162 | LLR-187 | TC-182`), drafts 2, interface-findings 0.
- Full unfiltered suite: `python -m pytest -q -n auto --basetemp=D:\pytest-tmp`
  — 2847 passed, 14 skipped, 1074.26 s (0:17:54).
  <!-- fig: cmd="python -m pytest -q -n auto --basetemp=D:\\pytest-tmp" rev=2eae651e -->
