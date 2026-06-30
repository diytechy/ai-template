# Worked Example — one full SN → SR → LLR → TC chain

A concrete pattern to copy. The feature: **"export my records to a CSV I can
open in a spreadsheet"**, plus one **edge case** (interruption safety). It shows
the whole spine, including the two habits that keep projects maintainable:
**separate a pure testable core from the I/O shell**, and **capture an edge case
as its own requirement**.

---

## 1. Stakeholder Need — `requirements/stakeholder-needs.md`

| SN-ID | Need (plain language) | Why it matters | Priority | Acceptance intent |
|---|---|---|---|---|
| SN-001 | Export my records to a file I can open in a spreadsheet. | The data is useless if I can't get it into Excel/Sheets. | M | A new user clicks/exports and the file opens in a spreadsheet with the right columns and all their rows. |

Edge-case table:

| SN-ID | Scenario | Expected behavior |
|---|---|---|
| SN-013 | Export interrupted (crash / power loss / cancel) mid-write | I never end up with a half-written file that looks complete; I can just run it again. |

## 2. System Requirements — `requirements/system-requirements.csv`

```csv
SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status,Phase
SR-001,CSV export (RFC-4180),SN-001,"The system shall export records as RFC-4180 CSV with a header row.","Realizes SN-001 so the file opens cleanly in any spreadsheet.","Output parses as CSV; row count == records + 1 (header); columns match the documented schema in order; fields containing comma/quote/newline are quoted per RFC-4180.","field=set{plain,comma,quote,newline}",M,Test,Verified,
SR-002,Atomic export write,SN-013,"The system shall write the export to a temporary file and atomically rename it to the final name only after a successful write.","Realizes SN-013 so an interrupted run never leaves a complete-looking partial file.","A run interrupted before completion leaves no file at the final path (only a distinguishable temp); re-running completes normally.","interrupt=set{during-write,before-rename}",M,Demonstration,Implemented,
```

Note: each SR has **measurable** acceptance criteria a test can assert (not "exports correctly"), links its SN, and uses `Permutations` so one row covers many cases. The trailing `Phase` column is blank here (= in scope for every phase); a phased roadmap tags rows `v1`/`v2`/… so G3 can close per phase (process.md §4 "Phased delivery").

## 3. Low-Level Requirements — `requirements/low-level-requirements.csv`

```csv
LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status
LLR-001,SR-001,Pure records->CSV serializer,src/export/csv,to_csv,"Pure function: records -> String. Header from the schema; values quoted per RFC-4180. No I/O — unit-testable in isolation.",(see TC),Implemented
LLR-002,SR-002,Atomic file write,src/export/io,write_atomic,"Write bytes to <path>.tmp, then rename to <path>; remove the tmp on any error. Rename is atomic on the same volume. The I/O shell around the pure core.",(see TC),Implemented
```

Note the split: **`to_csv` is a pure core** (cheap, exhaustive unit tests);
**`write_atomic` is the I/O shell** (a smaller number of integration tests).
Detail *decomposes* the SR — it doesn't restate it.

## 4. Test Cases — `test/test-cases.csv`

```csv
TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status
TC-001,SR-001;LLR-001,Unit,"to_csv over records incl. special-character fields; parse the result back",Smoke,"field=set{plain,comma,quote,newline}","Satisfies SR-001 AcceptanceCriteria",Yes,Verified
TC-002,SR-002;LLR-002,Integration,"Abort write_atomic mid-write; assert no file at the final path and the tmp is cleaned; then a normal run succeeds",Full,"interrupt=set{during-write,before-rename}","Satisfies SR-002 AcceptanceCriteria",Yes,Verified
```

The `Tier` column controls when a test runs: the cheap `to_csv` unit test is
`Smoke` (every iteration); the slower interruption integration test is `Full`
(pre-merge). A test needing real hardware or a long soak would be `Release`.
Mark `Smoke` tests `@pytest.mark.smoke` and `Release` tests
`@pytest.mark.release`; an unmarked test lands in `Full` — the pre-merge tier —
by default, so `check.py --tier` can never silently skip it.

Each TC lists the SR **and** the LLR it covers (so both levels are covered by
one row), expands the requirement's `Permutations`, and **cites** the acceptance
criteria by id rather than paraphrasing them.

## 4b. Dimensional coverage — boundaries × combinations

`SR-001` has three variable inputs, so one happy-path test is not enough. Declare
the dimensions in its `Permutations` cell (note **boundary** values and a
strategy):

```
field=set{plain,comma,quote,newline}; size=range[0..2GiB]; enc=set{utf8,utf16}; @pairwise
```

`field` is an equivalence partition (one representative per special-char class);
`size` contributes its **boundaries** (empty `0` and the max `2GiB` — the
classic empty-input / overflow catchers); `enc` is two classes. The full product
is 4 × 2 × 2 = 16. Feed the cell to the generator:

```
$ python scripts/gen_cases.py --spec "field=set{plain,comma,quote,newline}; size=range[0..2GiB]; enc=set{utf8,utf16}; @pairwise" --id SR-001
# Dimensional analysis for SR-001
  - field (4 values): plain, comma, quote, newline
  - size (2 values): *0*, *2GiB*   (* = boundary)
  - enc (2 values): utf8, utf16
  strategy: pairwise   cases: 8  (full product = 16; 50% reduction)
```

Eight cases instead of sixteen, yet every value of every dimension is still paired
with every value of the others — e.g. `quote` is tried at both `0` and `2GiB` and
in both encodings. TC-001 then **expands** these into its `Parameters` (or a
parametrized test) instead of sixteen near-duplicate rows. If this were an
expensive integration path, `--strategy boundaries` would drop it to a handful of
extreme-corner cases for the `Release` tier; if it were a corruption-risk path,
`@full` would keep all sixteen. **Match the strategy to risk and run cost; let the
generator produce the combinations.**

## 5. Code back-links (in the source)

```rust
/// Serialize records to RFC-4180 CSV (header + one row each).
// Implements: SR-001, LLR-001
pub fn to_csv(schema: &Schema, records: &[Record]) -> String { /* ... */ }

#[test]
fn to_csv_quotes_special_fields_sr001() { /* ...asserts SR-001 AC... */ }
```

The test name embeds the verified id, and the item is annotated `Implements:`.
The CSV columns are authoritative; these annotations keep code and registries
honest and greppable.

## 6. The traceability result

Running `python scripts/trace.py --strict` over this chain reports:

```
Traceability: SN=2 SR=2 LLR=2 TC=2 orphans=0. Report -> docs/test/report.md
```

**Zero orphans**: every SN has an SR, every SR has an LLR + a TC, every LLR has a
parent + a TC, every TC verifies a known id. That is the bar each gate enforces.

## 7. A different shape — an infrastructure / operational requirement

Not every requirement is a pure function with a unit test. Operational needs —
databases, networking, deployment — flow through the **same spine**, with three
differences: a **domain hat** owns the rows, the verification method is
**Demonstration** or **Manual** (a human runs it and observes), and the rows
carry an optional **`Area`** tag so the slice is filterable (process.md §1
"Domain hats"). No new mechanism — just a different fill of the same columns.

Say the **SRE/Ops** hat owns availability and the **DBA** hat owns the data
store. A reliability need (`SN-020`) becomes an SR verified by demonstration:

```csv
SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status,Phase,Area,Lifecycle
SR-101,Database failover under primary loss,SN-020,"The system shall promote the standby database and resume serving within 30 s of losing the primary, with no committed transaction lost.","Realizes SN-020: the service survives a database outage.","With the primary killed, the app serves reads and writes from the standby within 30 s and the last transaction committed before the kill is present after promotion.","failure=set{kill,network-loss,disk-full}",H,Demonstration,Implemented,,Infra/DB,Runtime
```

The trailing **`Area`** column (`Infra/DB`) is an optional tag a project adds so a
domain hat can filter and own its slice; SRs without it leave it blank. The
**`Lifecycle`** column (`Runtime`) is the same kind of optional tag for *when in
the running product's life* the requirement holds (process.md §4 "Lifecycle
phase").

**One capability spans phases** — this is exactly where the tag earns its keep.
The same "use a database" feature implies three requirements, not one, and a team
that writes only the failover SR has silently skipped two:

| Lifecycle | Sibling SR (same DB capability) | Owner |
|---|---|---|
| **Provision** | `SR-100` — the DB instance + schema are provisioned before first run | DBA |
| **Startup** | `SR-102` — open the connection pool and run pending migrations at launch; fail loudly if either fails | DBA / SRE-Ops |
| **Runtime** | `SR-101` — promote the standby on primary loss (above) | SRE/Ops |

Each is a real SR with its own LLR + TC; tagging them by lifecycle is what makes
the missing Provision/Startup rows obvious at G1. The failover *logic* is still
real code, so `SR-101` keeps an LLR (`LLR-101 reconnect/promote-on-primary-loss`,
owned by the same hat) — only `Analysis`/`Inspection` SRs skip the LLR. The TC
records the **procedure**, not an assertion, and is `Automated=No`, so the release
checklist (`gen_release_checklist.py`) finds it:

```csv
TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status
TC-101,SR-101;LLR-101,System,"Kill the primary DB; observe promotion and that a write committed just before the kill is readable after",Release,"failure=set{kill,network-loss,disk-full}","Satisfies SR-101 AcceptanceCriteria",No,Verified
```

`Tier=Release` keeps this slow, environment-heavy test out of the per-push and
pre-merge runs; it executes at `G-Release`, where the human signs the generated
checklist. Same registries, same traceability join, same gates — only the
verification method, the owning hat, and the `Area` tag change.

## 8. A non-functional budget — `requirements/performance-budgets.csv`

Behavioral SRs say *what* the system does; they don't bound *what it costs*. A
quantitative budget lives in its own registry (`PB-###`), owned by the
**Integration/Coordination** hat, and **back-links** the SR / LLR / Module it
bounds so the separation never loses the thread (process.md §9):

```csv
PB-ID,Metric,Refs,Budget,Unit,Tolerance,Direction,Tier,Gate,Owner,Notes
PB-001,Peak RAM exporting the largest input,SR-001;LLR-001,512,MiB,10%,lower-better,Release,warn,Integration,"Measured at the 2GiB size boundary that SR-001's Permutations already enumerate."
PB-002,Model VRAM at inference,SR-030,8,GiB,5%,lower-better,Release,fail,Integration,"GPU module (hypothetical SR-030): a number the author can't invent, so the integrator sets the allocation."
```

`PB-001` bounds the *cost* of the CSV export `SR-001` already specifies — same
feature, different axis — and pins the measurement to a boundary that SR's
`Permutations` enumerate, so it restates no dimensions. `PB-002` shows a **VRAM**
budget for a GPU module: a value the module author can't invent, so the integrator
sets the slice and the module measures against it. `trace.py` checks each row's
`Refs` resolve to a real SR/LLR/Module and that the `PB-` id is well-formed — a
budget that drifts off a deleted requirement is caught like any orphan. *Comparing*
the measured numbers against these budgets over time is the harness's job:
`scripts/check_perf.py` (process.md §9) reads a product-emitted `perf-metrics.json`
and flags both an absolute breach (here `PB-002`'s `Gate=fail` would fail the
build) and a regression past `Tolerance` versus the committed `perf-baseline.json`.
The registry here is just the captured, tracked source of truth.

---

### What to copy from this pattern

- One **measurable** SR per need; push value-sets into `Permutations`, not
  duplicate rows.
- **Pure core vs. I/O/GUI shell** — it's the single biggest lever for testability
  and for keeping logic deduplicated and readable.
- **Edge cases are first-class requirements** (SN-013 → SR-002), not afterthoughts.
- Tests **cite** acceptance criteria by id; code **annotates** the ids; the matrix
  is **generated**, never hand-kept.
- **Operational requirements use the same spine** (§7) — a domain hat owns them,
  `Verification=Demonstration`/`Manual`, an optional `Area` tag, and a
  procedure-recording `Release`-tier TC the release checklist finds.
- **Tag the lifecycle phase** (§7) so the neglected Provision/Startup requirements
  a capability implies get written, not just its Runtime one.
- **Quantitative budgets go off the spine** (§8) — `PB-###` in
  `performance-budgets.csv`, owned by the Integration hat, back-linked to the
  SR/LLR/Module they bound.
