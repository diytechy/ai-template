## 2026-08-23 — OI-60 ruled (a): the two free corrections land, the `direction` shed is held on a second measurement, and the twelve SR-owned `Provides` rows get their report

Deferred open items: none — the ruling recorded below closes the last pending row
on the open-items surface, and nothing here defers a question. What remains is
not a decision: the twelve-row re-point is an owner act fed by the report this
slice ships, and the rename-then-shed is agent-executable work the ruling already
authorizes, held on `WI-455` item 1.

**One-line summary.** The owner ruled `OI-60` (a) in session; the two free
corrections it folds in LANDED, the twelve-row report the owner asked for
SHIPPED, and the `direction` shed did NOT — a measurement taken before the first
cell was touched shows the column is underivable on all 44 requirement-owned
rows, so (a)'s two clauses are ordered rather than parallel and the destructive
half was not run without the enabling one.

### The ruling

The owner's words, verbatim: *"It's not clear to me what the issue is, the SR
just doesn't have a consumer? You can fix the ones that are fixable now, but then
can you generate a report of what those SRs are? Either in markdown or html,
including the definition of the SR and the interfaces."*

Clarified back to the owner before the ruling was recorded: **the twelve rows are
`Provides` seams and their consumers are fine.** The underivable half is the
PROVIDER side — an SR owner carries no `Module` cell, so `this_project` is the
only record anywhere of which module provides the seam. The direction matches
`OI-60`'s recommendation (a): shed `direction` only, keep the provider-side
endpoint cell on ALL rows until the twelve are re-pointed, take the two free
corrections. `OI-60` is now `status = "ruled"`, `ruled_date = "2026-08-23"`,
`ruling_ref` this fragment, with the execution record written into its
`recommendation` field above the pre-ruling text (the `OI-54` pattern).

### The consumer re-census — what actually reads `direction`

Re-run against the tree rather than inherited from the `OI-60` brief, which
predates two of the columns' consumers:

| Reader | Reads `direction`? |
|---|---|
| `check_trajectory.load_ifs` → `interface_findings` | **YES** — flips producer/consumer credit in the connectivity advisory. |
| `traj_views.sw_seams` + `_layer_edges` | **YES**, two sites — orients the dashboard's seam arrows. |
| `gen_arch_map` (the map's dotted seam edges) | **YES** — points the edge. |
| `trace.py` schema | **YES** — a required IF column plus its closed `Provides`/`Consumes` vocabulary. |
| `check_trajectory._declared_seam_pairs` | **NO** — it stores every endpoint pair BOTH ways. The `interfaces.toml` header claimed it did; the claim is corrected in this slice. |
| `traj_parse.frame_context` / `traj_context.py` (post-census) | **NO** — their `direction` is `external.toml`'s crossing `in`/`out`/`inout`, a different column of a different registry. |
| `gen_components.py` (post-census) | **NO** — it reads `ThisProject` for endpoint→Module→Component placement, never the flow. |
| Docs surface | `INTERFACES.template.md` ("Direction drives ownership"), `registries/interfaces.template.toml`, `PROCESS.md` §8's field list, `EXAMPLE.md`'s four worked rows, the dual-plan planner prompt, `RESYNC_PACK.md` — untouched this slice, since nothing was shed. |

So the live reader set is **three orienting consumers plus the schema**, not the
two the recommendation assumed — and none of the three can recover the fact
without the column while `counterpart` still means "the far side".

### The measurement that held the shed

Taken over the live registry before any cell was edited. **135 live rows** (the
census read 129 on 2026-08-22; six rows have landed since), 89 `Consumes` / 46
`Provides`, owner a design id on 91 and a requirement id on 44.

<!-- fig: cmd="python - # tomllib over docs/requirements/interfaces.toml + low-level-requirements.toml: owner tier, owner-module-vs-endpoint agreement per direction, external counterpart classes" rev=31f6d6d7 -->

- **Design-owned rows: 90 of 91 derivable.** `direction` follows from
  `owner`→`module` — the owner's module is the provider-side endpoint on a
  `Provides` row and the counterpart on a `Consumes` row. Multi-module `module`
  cells are split on `;` before the join, which is what resolves the five
  apparent disagreements a naive whole-cell compare reports (`IF-088`, `IF-117`,
  `IF-131`, `IF-132`, `IF-141` — all agree once split).
- **One real disagreement: `IF-031`**, exactly the row the census named, and the
  free correction below resolves it.
- **Requirement-owned rows: 0 of 44 derivable** — 12 `Provides` + 32 `Consumes`.
  A requirement carries no module. This is `OI-60`'s own finding about
  `this_project` applied to the other column, and it is why the shed is not free:
  dropping `direction` today would read all 44 as `Provides` and silently reverse
  the 32 `Consumes` seams in all three orienting readers.
- **A third finding, not in the census: `direction` is not one fact.** 19
  `Consumes` rows name an `external:` counterpart (16 of them
  `external:downstream adopter`, `IF-032`/`IF-036`/`IF-041` the other three).
  On those the cell reads as what the FAR side does — the adopter consumes —
  where the other 70 `Consumes` rows read as what THIS side does. The column
  carries flow, coverage and, on that group, the far side's role.

**Conclusion, and the deviation it forces.** (a)'s premise — "its two readers
derive the same fact from owner-side versus consumer-side" — holds only after
(a)'s OTHER clause, the counterpart-to-consumers rename that makes this side the
provider on every row. The two clauses are ORDERED: rename first, shed
immediately behind it. Running the shed alone is the destructive half without the
enabling half, on the same population the report is about. **Rows shed: 0.**
Nothing was normalized to make the column look shed-able, and no consumer, doc,
template or resync entry was touched — a shed that did not happen owes no
migration.

### Deliverables

- **`OI-60` ruled (a)**, with the owner's words quoted on the row and the
  execution record (what landed, what was held, and why) written into it.
- **Free correction 1 — `IF-031`'s owner: `LLR-014` → `SR-015`.** The census
  named it as the one row in the registry authored under the reading that was not
  ruled: its owner was the module holding the CONSUMING code (`check_perf.py`)
  while the consumed medium is the PB-### budgets registry. No design row's
  `module` is that registry (nothing decomposes the file itself), so the owner
  falls back to the requirement stating the registry's own invariant — `SR-015`,
  already among the row's `req_refs`. The reason is written into the row's
  `notes`, including the cost: the row leaves the derivability advisory's
  population, the same gap the twelve have.
- **Free correction 2 — the ruled reading in the registry header.**
  `interfaces.toml`'s `owner` block now states `OI-54` (a) where an author meets
  it: on a `Consumes` row the owner is the PROVIDER of the medium consumed, never
  the module holding the consuming code, and the consumer side carries VERIFIED
  readers. The corollary is stated with its worked example (`IF-031`): when the
  medium is a file no design row decomposes, the SR fallback is correct, not
  sloppy.
- **A third header correction, unplanned and taken because it is false rather
  than stale:** the `direction` block claimed `_declared_seam_pairs` reads the
  column. It does not — it stores every pair both ways. The block now names the
  real three readers, and carries the removal evidence this header owns: why the
  column is still here, the 90/91-vs-0/44 measurement, and the exact moment it
  goes.
- **The report — [`docs/plans/2026-08-23-sr-owned-provides-report.md`](../plans/2026-08-23-sr-owned-provides-report.md).**
  Opens with the plain-language statement of the issue (provider-side
  derivability, NOT missing consumers) and what was and was not shed, then takes
  the twelve rows one at a time: contract, provider module, consumers, the owner
  SR's id, FULL requirement text and rationale summary, the candidate design rows
  in that module (3–15 each, measured by `module` resolution), the `WI-495`
  dossier's KEEP read where it covered the row (`IF-013`, `IF-044`), and what a
  re-point would decide. Its headline: **four rows are adopter-facing**
  (`IF-013`, `IF-014`, `IF-015`, `IF-081`, all facing `external:downstream
  adopter`), where SR ownership is arguably the CORRECT reading rather than a
  fallback — a promise to an adopter is a requirement's to hold; **eight are
  internal**, of which three (`IF-005`, `IF-044`, `IF-076`) are ordinary
  re-points with small candidate pools, two (`IF-065`, `IF-076`) record module
  extractions where a design owner fits better, and two (`IF-009`, `IF-011`) sit
  on modules whose own decomposition is an open question. It also names the
  **32 requirement-owned `Consumes` rows** that carry the identical gap, so the
  principle the owner sets for twelve answers forty-four.
- **`WI-455` slice 6 recorded**; the lane stays ACTIVE holding item 1, now
  unblocked. `docs/status.md` re-pointed forward-only: no pending open item, and
  the lane's next act is the rename-then-shed slice.

### Deviations from the brief

- **The brief's part B was not executed, and its premise did not hold.** B asked
  for the `direction` column to be deleted from all rows, "FIRST verify it is
  derivable row-by-row (the row kind Provides/Consumes carries it)". There is no
  separate row-kind cell: `direction` IS the Provides/Consumes cell, so there is
  nothing for it to agree or disagree with. The derivability question that DOES
  exist is the `owner`→`module` join, and it answers 90/91 and 0/44. Held under
  the brief's own instruction that a disagreement is a finding to resolve rather
  than something to normalize away, and reported rather than guessed.
- **No new open item was filed for the residue**, deliberately. What remains is
  authorized work under the ruling just taken (the rename, then the shed) plus an
  owner act the report feeds — neither is an unruled question, and minting a row
  for a question the owner answered this morning would be noise.
- **The lane was NOT closed and closure was not assessed row by row**: item 1 is
  still owed and agent-executable, so the question is moot this slice.

### Gates

- Smoke: `python -m pytest -q -n auto -m smoke` — 1311 passed, 5 skipped,
  26.75 s.
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=31f6d6d7 -->
- `python scripts/check_smoke_budget.py --mode enforce` — 24.0 s vs 60 s
  budget, within; exit 0.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=31f6d6d7 -->
- `python project-trajectory/scripts/check_docs.py --root . --stale` — exit 0,
  1046 docs, 1358 intra-repo links, **0 broken**.
- `python project-trajectory/scripts/check_trajectory.py --strict` — exit 0,
  clean (508 work items, graph acyclic).
- `python project-trajectory/scripts/trace.py --strict-integrity` —
  **integrity 0**, interface-findings 0, interfaces 135, orphans 4, drafts 21.
- `python project-trajectory/scripts/gen_open_items.py --check` — view up to
  date, and this fragment's deferral line is clean.
- Generated surfaces re-derived through `trunk_step.py --regen` (derived-stage,
  trajectory, status, open-items, component-view): `docs/stage` moved only its
  as-of stamp, the rung is unmoved at `DevStg-LLReqs`, and
  `components.derived.toml` did not move at all — the `IF-031` owner change does
  not cross a component boundary. The open-items view now reads **0 pending
  decision(s)**.
- Full unfiltered suite: `python -m pytest -q -n auto
  --basetemp=D:\pytest-tmp-oi60` — **2987 passed, 14 skipped, 1322.29 s
  (0:22:02)**.
  <!-- fig: cmd="python -m pytest -q -n auto --basetemp=D:\\pytest-tmp-oi60" rev=31f6d6d7 -->
- No byte-budgeted file was touched (`PROCESS.md`, `AGENTS.template.md` and the
  skills are all unmodified), and **no `RESYNC_PACK.md` entry is owed**: nothing
  shipped changed, because nothing was shed.
