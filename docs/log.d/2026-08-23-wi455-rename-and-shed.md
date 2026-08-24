## 2026-08-23 — WI-455 item 1 lands and the lane CLOSES: `counterpart` becomes `consumers`, `direction` and the derivable endpoint cell are shed

Deferred open items: none — `OI-60` (a) is the ruling this slice executes, both
of its ordered clauses; nothing here asks the owner a question. The two things
left standing are named as residue, not as decisions: the twelve-row re-point is
an owner-informed act the shipped report already feeds (and `trace.py` now names
each cell as its owner moves), and recording a medium as the provider on the 21
published-medium rows is authoring per row, not a rename.

*Dates, stated because they differ: the pass ran 2026-08-23; verification and
the commit landed 2026-08-24 after a session interruption.*

**One-line summary.** `OI-60`'s two ORDERED clauses ran in one reviewed schema
pass over all 135 interface rows — `counterpart` → `consumers` first, then the
`direction` and derivable-provider shed immediately behind it — with the
transform's losslessness measured row-by-row before and after, driven as tests
rather than claimed, and the whole `WI-455` program closed behind it.

### The end-state schema, as landed

| was | now |
|---|---|
| `direction = "Provides"` / `"Consumes"` | **deleted** — flow is the SHAPE of the row, `provider` → `consumers` |
| `this_project` (this side) | `provider` on a Provides row; folded into `consumers` on a Consumes row |
| `counterpart` (the far side) | `consumers` (a LIST, required); or `provider`, where the far side IS the provider or the medium |

**The surviving cell is named `provider`, and the choice is the smallest honest
one.** Keeping the name `this_project` was refused: its meaning was
direction-dependent (the provider on a `Provides` row, the consumer on a
`Consumes` row), so carrying it forward would leave one column meaning two
things across the population — the D-3 defect the shed exists to remove. A
separate `medium` cell was also refused: the endpoint grammar is
module-or-path-or-`external:` already, so a file medium IS the provider-side
endpoint (`IF-070`'s `docs/coverage-floors`, `IF-031`'s budgets registry), and a
second column for 12 rows would state the same fact under a second name. One
cell, one meaning, on every row.

### The per-class transform — all four counterpart classes, and both `Provides` classes

Classified BEFORE any cell was edited, per the recorded readings, and asserted
rather than inferred: every row falls in exactly one class and the counts are
checked by the transform itself.

<!-- fig: cmd="python - # tomllib over docs/requirements/interfaces.toml at HEAD and in the tree + low-level-requirements.toml: per-class counts and the row-by-row losslessness compare" rev=55d1cb77-dirty -->

| Class | Rows | `consumers` becomes | `provider` becomes |
|---|---|---|---|
| **P1** design-owned `Provides` | 34 | `counterpart`, split | `this_project` — SHED, derivable |
| **P2** requirement-owned `Provides` (the report's twelve) | 12 | `counterpart`, split | `this_project` — KEPT |
| **C1** carrier `Consumes` (the far side is the provider module) | 56 | `this_project` | `counterpart` — SHED on 51, KEPT on 5 |
| **C2** medium `Consumes` (the far side is the file/directory/`external:` party consumed) | 12 | `this_project` | `counterpart` — KEPT |
| **C3** consumer-CLASS `Consumes` (the 16 `B-05` rows) | 16 | `this_project` **+** `counterpart` — both sides are consumers | none — none was ever recorded |
| **C4** reader-SET `Consumes` (`WI-469`'s measured readers: `IF-029`, `IF-035`, `IF-037`, `IF-047`, `IF-072`) | 5 | `this_project` ∪ `counterpart`, deduped | none — none was ever recorded |

135 rows, 162 consumer endpoints, 29 stated providers. **Losslessness was
MEASURED, not argued:** every row's post-transform `(provider-or-derived,
consumers)` was compared against the pre-transform fact its class defines —
**0 mismatches on 135 rows**, and no row was normalized to make a column look
shed-able.

### The shed census — what died, what survived, per column

| Column | Died on | Survived on |
|---|---|---|
| `direction` | **135 of 135** | — |
| `this_project` / `counterpart` (as names) | **135 of 135** | — |
| the provider FACT | — | 29 rows state it; 85 derive it from `owner`→LLR→`module`; 21 never recorded one |

**The derivability rule, stated executably and held by test:** the provider cell
is absent exactly where `owner` is a design row naming exactly ONE `module`. It
survives on **29** rows in three groups, each for a stated reason — **12** with a
requirement owner and a real module (the `Provides` report's twelve); **12** whose
provider is a file, a directory or an `external:` party that no design row can
ever be (`IF-025`, `IF-026`, `IF-028`, `IF-031`, `IF-032`, `IF-036`, `IF-041`,
`IF-045`, `IF-052`, `IF-070`, `IF-127`, `IF-143`); and **5** whose owner names
SEVERAL modules (`IF-088`, `IF-117`, `IF-131`, `IF-132`, `IF-141`), where the
derivation yields a SET and the set is not the fact. That last group is a
correction to the staged spec's arithmetic, found by measuring: R4 says the cell
dies "once derivable as owner→LLR→`module`", and on a multi-module owner it is
not.

**21 rows state no provider, and that is the honest reading rather than a gap
the shed opened.** On a published-medium row (`IF-021`'s spine registries,
`IF-029`'s runtime-flows doc, the 16 rows facing `external:downstream adopter`)
what the row RECORDS is the measured reader set; the medium is named in
`contract`, and no endpoint cell ever claimed it. Nothing was lost — but the
shed EXPOSES it, which is why it is declared here, in the registry header, in
`tests/test_seam_resolution.py`'s `NO_PROVIDER` set and in the resync entry.

### Stops: none — and the one thing that came closest

No row was ambiguous under the recorded readings. The nearest thing to a stop
was **C4**, a class the `OI-54` census did not name: five `Consumes` rows whose
`counterpart` is the measured READER SET of a file medium (`IF-029` names three
readers including its own side). Read as C1/C2 they would have made the reader
list the provider and silently reversed five seams. They are separated by the
evidence already on the rows — each one's own `notes` cell states its fan-out
census — so the class is recorded rather than guessed, and the ids are pinned in
the transform, in the resync entry and in the tests.

### The readers, all of them, and the one home they now share

`kitlib.spine` gains `seam_provider` / `seam_consumers` / `seam_endpoints`, and
`spine_carrier.llr_modules` the design-tier join they take;
`check_trajectory.load_ifs` RESOLVES each row once (with `load_seams` as the one
live-registry call every seam view makes, so no consumer can forget the join).
So the orientation is derived in ONE place instead of six re-deriving it from a
flag: `trace` (schema, enum, both endpoint advisories), `trace_text`,
`check_trajectory` (connectivity credit + declared seam pairs), `traj_views`
(both seam graphs), `gen_arch_map` (dotted edges), `gen_components` (placement),
`traj_parse` (untied `external:` endpoints), `intake`, `plan_briefs`,
`spine_carrier` + `migrate_carrier` (the pinned column bijection).

**`trace_text.if_this_project_advisories` became `if_provider_advisories`**, and
its subject changed with the schema: the countdown to dropping a column is now
the rule that HOLDS the state it counted down to — a row stating a provider its
owner already derives is named as redundant, one contradicting its owner as a
disagreement. It is the executable half of the twelve-row re-point: move a row's
owner to the design tier and the advisory asks for the cell back.

**Three behaviour changes, none silent.**

1. **A multi-endpoint cell is now several endpoints everywhere.** `IF-097`'s
   three consumers used to reach `traj_views` and `gen_components` as ONE
   unsplit string that resolved to nothing; the component view moves four rows
   for that reason alone (`IF-097` boundary → internal; `IF-029`, `IF-037`,
   `IF-047` gain the boundary refs their split endpoints resolve to). A latent
   defect the code's own comments had already named, fixed by the shape rather
   than by a patch.
2. **The `source`/`sink` honesty valve marks a ROLE, not a cell** — `source` the
   row's provider, `sink` its consumers. Verified equivalent on the live corpus:
   all 8 `source` rows were `Provides` (where `this_project` WAS the provider)
   and all 10 `sink` rows `Consumes` (where it was a consumer), so the rule
   reproduces today's marks exactly while surviving the cell it was keyed on.
3. **The How-SW seam graph draws nothing for a provider-less row.** Those 21
   arrows used to run FROM `external:downstream adopter` INTO the module — the
   inverted orientation the `OI-60` census measured — so what is lost is a wrong
   arrow, and what is left is the row's honest one-sided state.

**The D-3 collision closed itself, exactly as `spine_carrier`'s note promised:**
`Direction` now carries ONE vocabulary on the carrier (the boundary tier's
`in|out|inout`), and the note says so instead of watching.

### The derivations ship as tests

`tests/test_seam_resolution.py` (5 nodes, in-process, over the LIVE registry):
no row carries a retired cell and every row's `consumers` is a non-empty list;
flow is recoverable on every row (a provider or a declared provider-less id, a
consumer set, and never an endpoint on both sides of its own seam); the provider
cell is present exactly where the owner cannot derive it uniquely; the report's
twelve still carry their provider fact and their owners are still requirements;
and `seam_provider` prefers the stated cell over the derivation, so a re-pointed
owner can never silently overrule an authored endpoint.

Existing tests moved with the schema rather than being deleted:
`test_trace_rules`' four derivability tests became three about the new rule,
`test_trace` / `test_trajectory_arch`'s CSV→TOML fixture translators apply the
rename (so ~24 call sites keep their subject), `traj_fixtures.if_row` lost its
direction argument, and `test_gen_arch_map` gains the derived-provider case.
Three goldens regenerated: the diff is the section rename and its one-line
census, nothing else.

### The cells that describe the schema, amended with it

Twelve live cells stated the retired shape and were corrected in the same pass,
because a cell describing a surface that changed is false, not stale — `IF-013`,
`IF-025`, `IF-031`, `IF-044`, `IF-045`, `IF-059`, `IF-060`, `IF-076`, `IF-088`,
`IF-093`, `IF-102`, `IF-128`. Two carry weight: `IF-059`'s `contract` (the
excerpt `plan_briefs` embeds is now `IF-ID/Owner/Provider/Consumers/Contract`),
and the rest are `notes` prose naming `counterpart` as a cell or a row's kind as
`Provides`/`Consumes`. Beside them, **`LLR-041`'s `Detail`** —
the design row for trace's IF-tier integrity, whose text promised "an unmatched
`ThisProject` endpoint stays advisory-only". `LLR-041` is `Approved`, so that
touch is NAMED here per the re-tier ruling 6 pattern: it is a text amendment
following the behaviour it describes, no `Status` moved, and the snapshot
comparison reports it as the pending amendment it is.

The amendment SHOWS UP where it should: the pre-commit `approval-fresh` step
refused the commit until `docs/ratify/CURRENT.md` was regenerated, and the
re-generated brief now carries `LLR-041` under `SR-159` with its before/after
text — one row awaiting the owner's read, which is exactly what amending an
`Approved` row is supposed to cost.

`migrate_carrier`'s legacy-CSV degrade gained a test rather than a promise
(`test_a_retired_endpoint_column_converts_under_its_own_name`): a CSV still
carrying `ThisProject`/`Counterpart` keys them as THEMSELVES, so the schema tier
names them and the adopter renames deliberately. Guessing a side there would
silently reverse every consuming row — the one failure the resync entry exists
to prevent.

### Warrant: none demanded, verified rather than assumed

All 135 rows are `Drafted`, no cell moved to or from `Approved`, and
`human_approves(docs, "interfaces")` governs a `status` writer — not an endpoint
cell. No snapshot was refreshed and no attestation was ridden. The
`docs/archive/last_approved/` mirror is untouched.

### Ratchets and budgets, all re-stamped deliberately with reasons

- **Complexity, both DOWN:** `check_trajectory.interface_findings` 22 → **20**
  (the orientation left the function), `gen_arch_map.build_dependency_diagram`
  14 → **11** (the seam walk went out to `_seam_edges`). `traj_views._layer_edges`
  would have crossed the bound at 12; `_wire_blocks` was extracted instead, so it
  stays off the census — decomposition, the escape this ratchet prefers.
- **Module size:** `check_trajectory.py` 4880 → 4903 (+23), `trace.py` 5322 →
  5324 (+2), `intake.py` 1960 → **1959** (−1, the seam-line read got shorter),
  each with its reason on the row. The last two were first stamped from a
  pre-`ruff format` measurement (+5 / +2) and corrected once the formatter
  reflowed them — a baseline is the file's real size or it is noise.
- **Smoke membership:** 1320 → **1335**, +15 over the measured 1322 — the five
  new derivation nodes and the legacy-column degrade test, plus headroom; the
  wall clock is unmoved at ~21 s.
- **Byte budgets:** `PROCESS.md` 85,862 → 85,984 (**+122**, FLAGGED: §8's field
  list re-states the two cells and the omit-when-derivable rule; the skill's
  baseline row was ALSO stale at 85,889 — 27 bytes above the file it pinned —
  and is re-stamped to the real size in the same commit).
  `PROCESS_OPTIONS.md` 178,307 → 178,760 (**+453**, FLAGGED: the intra-repo seam
  model and the honesty valve re-stated). One CAPPED file moved — the
  `byte-budget-guard` skill itself, 4,827 → **4,878** of its 5,000 cap, carrying
  those two re-stamps; the first full-suite run FAILED on its self-pin
  (`test_capped_doc_baselines_match_the_real_sizes`) because a row that records
  its own file's size has to be re-stamped after it is edited, which is the
  guard working exactly as designed. The other two capped files are untouched:
  `AGENTS.template.md` 9,980 (cap 10,000), `CLAUDE.md` 7,827 (cap 8,500).

### Deviations

- **The staged spec's `provider`-dies rule needed one correction**, found by
  measurement and taken: a multi-module owner derives a SET, so five rows keep
  the cell. Recorded above and in the registry header rather than normalized
  away.
- **`direction`'s LABEL is not recoverable, and does not need to be.** The FLOW
  is (provider → consumers, tested). What `Provides` vs `Consumes` additionally
  recorded was which SIDE authored the row — provenance, not content — and
  `owner` records answerability already. Stated here because "the column is
  derivable" would have been the easy claim and is not the true one.
- **A fourth `Consumes` class (C4) exists that `OI-54`'s census did not name.**
  Handled per the evidence on the rows; see the stops section.
- **`migrate_carrier`'s legacy CSV map lost the retired columns.** A legacy
  registry still carrying them keys them as themselves and the schema tier names
  them — the same handling the retired `Status` column already had, and the
  resync entry says so.

### Gates

- Smoke: `python -m pytest -q -n auto -m smoke` — **1317 passed, 5 skipped,
  20.75 s** (53.70 s on the cold first run after the edit; one box, both
  readings stated).
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=55d1cb77-dirty -->
- `python scripts/check_smoke_budget.py --mode enforce` — it re-runs the tier
  and times it: **21.0 s vs the 60 s budget, within**; exit 0.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=55d1cb77-dirty -->
- `python project-trajectory/scripts/check_docs.py --root . --stale` — exit 0,
  1051 docs, 1362 intra-repo links, **0 broken**.
- `python project-trajectory/scripts/check_trajectory.py --strict` — exit 0,
  clean (509 work items, graph acyclic).
- `python project-trajectory/scripts/trace.py --strict-integrity` — exit 0,
  **integrity 0**, interfaces 135, interface-findings 0, orphans 4, drafts 19.
- `python project-trajectory/scripts/gen_open_items.py --check` — view up to
  date.
- Generated surfaces re-derived through `trunk_step.py --regen`:
  `components.derived.toml` moved the four rows named above, `docs/stage` moved
  only its as-of stamp (rung unmoved at `DevStg-LLReqs`), `PROJECT_STATE.html`
  re-rendered.
- Full unfiltered suite: `python -m pytest -q -n auto
  --basetemp=D:\pytest-tmp-w455f2` — **2992 passed, 14 skipped, 1116.96 s
  (0:18:36)**. Its FIRST run (`--basetemp=D:\pytest-tmp-w455f`) read 2991 passed
  / **1 failed** — the capped-doc baseline named above — and is reported here
  rather than quietly replaced: the re-stamp is what the second run confirms.
  <!-- fig: cmd="python -m pytest -q -n auto --basetemp=D:\\pytest-tmp-w455f2" rev=55d1cb77-dirty -->

### The lane CLOSES

Re-read against the title's three numbered deliverables and every slice record:
`check_flows`' input (slice 1, the flows moved and the checker followed);
`bootstrap.py`'s MAPPING and the scaffold surface (slice 1, verified by
bootstrapping a real scaffold, with its resync entry); the per-block disposition
of the ~192 hand-authored lines (slice 1's table). The Context's own three
remainders are struck in turn — the provenance citations (slice 4), the
`external.toml` context view (slice 5, which completes sitting-2 decision 8's
execution), and item 1 here. Nothing is owed, so the spec moves to
[`../archive/work/complete/`](../archive/work/complete/WI-455-architecture-md-retirement-program.md)
with its `## Deliverable` filled and `specref` cleared, and the active directory
is gone. **`WI-512` is thereby dependency-ready** — its `needs = ["WI-455"]`
resolves, and its own sequencing clause ("(a) runs AFTER `WI-455` item 1's
`counterpart` → consumers rename") is satisfied by this slice.
