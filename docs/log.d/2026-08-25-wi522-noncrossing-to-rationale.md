## 2026-08-25 — WI-522: the non-crossing content leaves `contract` for `rationale`, and the destination's own grammar decides ten rows

**Summary.** `OI-63`'s ruled option (d) executed over the 46 `nonx > 0` rows of
`docs/requirements/interfaces.toml`: **36 rows MOVED** their M/X clauses into
`rationale`, **8 are FLAGGED** and **2 RE-JUDGED** as not non-crossing. The
per-row record is a disposition addendum on
[../plans/2026-08-25-if-contract-verdicts.md](../plans/2026-08-25-if-contract-verdicts.md),
so the placement re-ask reads one document rather than a log and a table.
Registry-and-docs only: no script, test or kit file changed.

Deferred open items: none. The ruling this row executes is already ruled, and
the two findings it surfaces (the `rationale` lint gap; the case-sensitive
`_WI_TOKEN_RE`) are recorded for triage — neither is a decision this session
owes the owner an answer to.

### THE NUMBERS, measured on the tree rather than estimated

| | before | after |
|---|---|---|
| `contract` characters over the 108-row population | 43,995 | **37,859** (−6,136, **−13.9%**) |
| `contract` characters over the 36 edited rows | 18,611 | **12,475** (−6,136, **−33.0%**) |
| rows carrying a `rationale` | 1 (`IF-141`) | **37** |
| `rationale` characters | 156 | **7,491** (+7,335) |
| `trace.py` "Contract argues" advisory | 27 rows | **17 rows** |
| `trace.py` over-ceiling (500) advisory | 30 rows | **17 rows** |
| all `IF` row advisories | 67 | **42** |

`OI-63`'s brief sized the non-crossing population at **6,715 characters over 46
rows**; **6,136 of it (91.4%) left the cell** and the residual **679** is the
ten rows flagged or re-judged. **The moved text got LONGER than the text
removed** — 7,335 written against 6,136 cut, **+1,199** — because a clause
excised from mid-sentence has to become a sentence to stand alone in a reason
cell. Disclosed rather than netted out.

<!-- fig: cmd="python project-trajectory/scripts/trace.py --root . --strict-integrity" rev=bad71010 -->

### The destination has a declared grammar, and that is what decided the flags

The kit template states `rationale`'s rule: *"the ARGUMENT, never the CITATION …
no work-item id, ruling, sitting, review-round or open-item reference, decision
id, edit verb or date stamp"*. A non-crossing span that is a bare CITATION
therefore cannot move there without importing a violation into the destination —
and **deletion was not ruled**, so those spans stay exactly where they were and
are flagged. That is the whole of the FLAGGED bucket: `IF-080`
(`concurrency-restructure SS1.2/SS2.3`, `RULING-6`/`RULING-7`), `IF-088`'s
dated `§A4` amendment pointer, `IF-089`/`IF-136`/`IF-137`'s plan-doc pointers,
`IF-090`'s `ruled decision 2` and `IF-094`'s `the ruled A1/A8 tables` (both the
`IF-080` class the measuring pass named — a citation resolving to nothing a
reader can reach), `IF-117`'s three-way rot, and `IF-127`'s 16-character
`Imported LAZILY.` whose reason already sits in the row's own `notes`.

Every cell this pass wrote was checked against the mechanical detector —
`trace_text.provenance_tokens(cell, reason=True)` — **0 tokens over 36 cells.**

### Two findings owed the owner, from checking the destination first

1. **Nothing lints an IF `rationale`.** `trace.IF_REASON_CELLS` is
   `("Notes", "SignalNote")`; `trace_text`'s three provenance column tables name
   SN/SR/LLR/TC/CMP/EXT and no IF tier; `IF_CONTRACT_MAX` is `Contract`-scoped
   and deliberately so; nothing renders the cell and no script reads it by name.
   The grammar the shipped template declares for it is author-held and nothing
   else — the same "the largest pocket is the layer the rule cannot see" shape
   `if_note_advisories`' own docstring names one cell over. **Surfaced as a
   finding, not fixed here**: widening the arm is an executable change on a
   registry-only row, and it is the owner's call whether the cell that just went
   from 1 user to 37 gets the arm.
2. **An empty `rationale` is a HARD refusal** — `spine_carrier` raises on an
   empty-string cell at every live read, so a row carries the key or omits it.
   Recorded in the registry header as a trap, because nothing says it elsewhere.

### The three cross-review re-adjudications — all three CONFIRM the reviewer

None of them moved a span, and that is the finding rather than a shortfall:

- **`IF-050`** — *"every consumer reads it through kitlib.stage.read_stage"* is
  a FALSE UNIVERSAL. `kitlib/stage.py`'s own "WHO THE FRESHNESS GUARANTEE
  COVERS" block states that `traj_parse._stage_value` and
  `traj_status._stage_facts` deliberately parse the recorded file directly.
  Verified in-tree. But that is crossing content which is WRONG, not
  non-crossing content in the wrong cell — a correction, and correction was not
  what was ruled. `nonx` stays 0.
- **`IF-061`** — the span splits, exactly as the reviewer predicted.
  `plan_artifacts.py` records the CSV append as retired at Phase 5 (so
  `legacy work-items.csv rows via dual-write` is ROT) while `_existing_wi_nums`
  reads the stray CSV *and* the spec folder (so `ids allocated over BOTH homes`
  is a LIVE class-H guarantee). Neither is M/X: `nonx` re-judged **78 → 0**, rot
  flagged.
- **`IF-098`** — remeasured. `(key, file, slots, digest)` (47 chars) and
  `render()` is pure (18) both appear in the HARVESTED one-line summaries of
  `catalog_rows()` and `render()`, confirmed by running
  `gen_arch_map.scan_inventory`, so they are R2 restatement. Remainder falls
  **219 → 81** characters (the `and nothing else` exclusion plus the
  never-disagree guarantee); 166 if the trailing `--check` clause is counted as
  remainder, which it is only because R2 is defined as the summary and the
  summary truncates. `nonx` stays 0.

### Deviations from spec

- **The spec said claim into `docs/work/active/`; the spec file went
  `queued/` → `docs/archive/work/complete/` in one commit instead**, following
  the `WI-519` precedent three commits back (`c3bc6e07`) for a single-sitting
  row: an `active/` stop created and removed inside one commit records a state
  the registry never actually held.
- **Two rows moved WIDER than their verdict line estimated** (`IF-076`,
  `IF-056`) and the total moved is 6,136 against an estimate of 6,036 on those
  rows. The verdicts are accurate to the clause and not to the character by
  their own statement, and the spec directed a re-judgement, so the estimate was
  the starting claim and not the instruction.
- **The registry header gained a `rationale` field entry** it never had — 14
  fields were documented and this one was not, though `contract`'s entry already
  pointed at it. Forced rather than opportunistic: the pass takes the field from
  1 row to 37. In the same edit the header's *"The other 108 rows are
  deliberately untouched — that pass is what this one's measurement decides"*
  was corrected, because the measurement has run and 36 of those rows are no
  longer untouched. Leaving it would have left the header asserting something
  false about the registry it heads — the `WI-512` `signal_note` situation
  again.
- **Two tripwire advisories went quiet for a non-repair reason and are called
  out as such** in the addendum: `IF-072`'s `SCAFFOLD_OMISSIONS` and `IF-132`'s
  `registries/source` (both already adjudicated FALSE POSITIVES) stopped firing
  only because the tokens rode their clauses into a cell the arm does not scan.
  The known real rot, `IF-055`'s `SCHED_*`, is untouched and still reported.

### Flagged, not deleted — and one detector gap

Deletion was not ruled, so every flagged span is still in its cell; the
addendum's "Flagged for the owner" list is the queue. One extra finding
belonging to no bucket: **`IF-082`, `IF-083` and `IF-084` carry `wI-280` in
`notes`**, a work-item id the citation-frame detector misses because
`_WI_TOKEN_RE` is case-sensitive. Reported, not fixed — a detector question.

### Gates

Registry-and-docs only, so the **full unfiltered suite is NOT owed** and is not
claimed (the `WI-516` precedent): nothing executable changed — `git diff --stat`
touches `docs/` alone.

- `check_trajectory.py --root . --strict` → **clean (519 work items, graph
  acyclic)**; the WARNs are the pre-existing set.
- `trace.py --root . --strict-integrity` → exit 0, `integrity=0
  interface-findings=0 interfaces=135`, all 135 rows `Drafted` before and after.
- `check_docs.py --root . --stale` → **1099 docs, 1443 links, 0 broken**.
- `check_vocab.py --root . --strict` → **clean (440 live authored files)**.
- `pytest -q -n auto -m smoke` → **1363 passed, 6 skipped in 26.12s**;
  `check_smoke_budget.py --mode enforce` → **25.1s vs 60s budget → within**.

**On the seconds, since the preceding commit's reading needs pairing:** the
`OI-63`/`OI-64` ruling commit recorded **101.7s / 102.1s** at the same budget
under an interactive non-repo load (~74% CPU, a game client), and refused to
re-stamp the budget or re-tier a module off that reading. The box is quiet
again and the same tier measures **25.1s** one commit later, against the
**22.9s** the WI-521 sitting saw. The loaded reading measured the game, exactly
as it was recorded to have done; nothing was moved to fit either number.

<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=bad71010 -->
<!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=bad71010 -->
