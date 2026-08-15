# Worked Example — one full SN → SR → LLR → TC chain

A concrete pattern to copy. The feature: **"export my records to a CSV I can
open in a spreadsheet"**, plus one **edge case** (interruption safety). It shows
the whole spine, including the two habits that keep projects maintainable:
**separate a pure testable core from the I/O shell**, and **capture an edge case
as its own requirement**.

---

## 1. Stakeholder Need — `requirements/stakeholder-needs.md`

The needs sit under the project's vision — one tagged statement in the README
(`README.md#vision`, the canonical home every other doc points at) that DevBar-Reqs
checks each need against. A worked one for this project:

> **PROJECT-VISION:** For spreadsheet-first users who keep their records in
> this tool: get those records into Excel/Sheets in one click, and never hand
> them a half-written file.

| SN-ID | Need (plain language) | Why it matters | Priority | Acceptance intent |
|---|---|---|---|---|
| SN-001 | Export my records to a file I can open in a spreadsheet. | The data is useless if I can't get it into Excel/Sheets. | M | A new user clicks/exports and the file opens in a spreadsheet with the right columns and all their rows. |

Edge-case table:

| SN-ID | Scenario | Expected behavior |
|---|---|---|
| SN-013 | Export interrupted (crash / power loss / cancel) mid-write | I never end up with a half-written file that looks complete; I can just run it again. |

## 2. System Requirements — `requirements/system-requirements.csv`

```csv
SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status,Phase,Aspect
SR-001,CSV export (RFC-4180),SN-001,"The system shall export records as RFC-4180 CSV with a header row.","Realizes SN-001 so the file opens cleanly in any spreadsheet.","Output parses as CSV; row count == records + 1 (header); columns match the documented schema in order; fields containing comma/quote/newline are quoted per RFC-4180.","field=set{plain,comma,quote,newline}",M,Test,Verified,,
SR-002,Atomic export write,SN-013,"The system shall write the export to a temporary file and atomically rename it to the final name only after a successful write.","Realizes SN-013 so an interrupted run never leaves a complete-looking partial file.","A run interrupted before completion leaves no file at the final path (only a distinguishable temp); re-running completes normally.","interrupt=set{during-write,before-rename}",M,Demonstration,Implemented,,
```

Note: each SR has **measurable** acceptance criteria a test can assert (not "exports correctly"), links its SN, and uses `Permutations` so one row covers many cases. The trailing `Phase` column is blank throughout because this is a single-shot deliverable (no phased roadmap): with nothing phased the ratified-row Phase rule stays unarmed, and blank means in scope for every phase. A phased roadmap instead tags every ratified SR/LLR/TC with the integer phase it shipped in (`1`/`2`/… — digits only, full cell; a prefixed `v2` on a ratified row is a `--strict-schema` finding), the project's current phase is *derived* as the highest, and only a `Draft` row may then leave `Phase` blank — see process.md §4 "Phased delivery". `Aspect` (optional, process.md §1) is blank throughout because none of these rows is cross-cutting — it takes a CLOSED value naming a concern no component partition can express, never a domain or owner tag, and trace.py reports per-aspect SR counts when it is filled.

## 3. Low-Level Requirements — `requirements/low-level-requirements.csv`

```csv
LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,Rationale,TestRefs,Status,Phase
LLR-001,SR-001,Pure records->CSV serializer,src/export/csv,to_csv,"Pure function: records -> String. Header from the schema; values quoted per RFC-4180. No I/O — unit-testable in isolation.",,(see TC),Implemented,
LLR-002,SR-002,Atomic file write,src/export/io,write_atomic,"Write bytes to <path>.tmp, then rename to <path>; remove the tmp on any error. Rename is atomic on the same volume. The I/O shell around the pure core.","Streaming the write in place was ruled out: a crash mid-write leaves a half-file the next run reads as valid. Costs one temp file per export.",(see TC),Implemented,
```

Note the split: **`to_csv` is a pure core** (cheap, exhaustive unit tests);
**`write_atomic` is the I/O shell** (a smaller number of integration tests).
Detail *decomposes* the SR — it doesn't restate it.

Note also the **`Rationale`** split, and that `LLR-001` leaves it blank. `Detail`
says *what this row is*; `Rationale` says *why it is that and not something else*
— what breaks without it, which alternative lost. It is optional, and blank is
the right answer for a row like `LLR-001` whose why is simply its parent SR's.
Reach for it when the decomposition itself was a decision (`LLR-002` chose atomic
rename over a streaming write). Keeping the two apart is what stops a `Detail`
growing into a wall of mechanism, justification and edit history at once.

## 4. Test Cases — `test/test-cases.csv`

```csv
TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status,Phase
TC-001,SR-001;LLR-001,Unit,"to_csv over records incl. special-character fields; parse the result back",Smoke,"field=set{plain,comma,quote,newline}","Satisfies SR-001 AcceptanceCriteria",Yes,tests/test_export.py::test_to_csv_roundtrip,Verified,
TC-002,SR-002;LLR-002,Integration,"Abort write_atomic mid-write; assert no file at the final path and the tmp is cleaned; then a normal run succeeds",Full,"interrupt=set{during-write,before-rename}","Satisfies SR-002 AcceptanceCriteria",Yes,tests/test_export.py::test_atomic_interrupt,Verified,
```

The `Evidence` column names the **concrete test that provides the proof** — a
pytest node id, a script path, or a procedure-doc link (inspection-only text,
never a mechanized resolve). It is optional in general, but a row claiming
`Automated=Yes` must cite it under `--strict-schema` (DevBar-Release): a claimed-automated
test with no cited location is a soft false-green. Keep `Parameters` for the
*dimensional inputs* a test exercises (the `gen_cases.py` grammar below) — the
test's location never belongs there.

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
are identified by their LLRs' **`Module`**/component so the slice is filterable
(process.md §1 "Domain hats"). No new mechanism — just a different fill of the
same columns.

Say the **SRE/Ops** hat owns availability and the **DBA** hat owns the data
store. A reliability need (`SN-020`) becomes an SR verified by demonstration:

```csv
SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status,Phase,Lifecycle
SR-101,Database failover under primary loss,SN-020,"The system shall promote the standby database and resume serving within 30 s of losing the primary, with no committed transaction lost.","Realizes SN-020: the service survives a database outage.","With the primary killed, the app serves reads and writes from the standby within 30 s and the last transaction committed before the kill is present after promotion.","failure=set{kill,network-loss,disk-full}",H,Demonstration,Implemented,,Runtime
```

The domain hat filters and owns its slice through the rows' LLR
**`Module`**/component, not through a tag on the SR. The trailing
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
the missing Provision/Startup rows obvious at DevBar-Reqs. The failover *logic* is still
real code, so `SR-101` keeps an LLR (`LLR-101 reconnect/promote-on-primary-loss`,
owned by the same hat) — only `Analysis`/`Inspection`/`Attest` SRs skip the LLR
(§7.1 shows an `Attest` one). The TC
records the **procedure**, not an assertion, and is `Automated=No`, so the release
checklist (`gen_release_checklist.py`) finds it:

```csv
TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status,Phase
TC-101,SR-101;LLR-101,System,"Kill the primary DB; observe promotion and that a write committed just before the kill is readable after",Release,"failure=set{kill,network-loss,disk-full}","Satisfies SR-101 AcceptanceCriteria",No,docs/test/failover-procedure.md,Verified,
```

`Tier=Release` keeps this slow, environment-heavy test out of the per-push and
pre-merge runs; it executes at `DevStg-Release`, where the human signs the generated
checklist. Same registries, same traceability join, same gates — only the
verification method and the owning hat change.

### 7.1 The honest floor — an `Attest` requirement (human judgment, not a check)

Some acceptance criteria can't be mechanized *at all* — a subjective, mostly
binary asset judged by a person: does this cutscene land emotionally, does the
main theme fit the game's mood, did the voice actor deliver the line. For these
the honest verification method is **`Attest`**: a **named human's recorded
judgment** (process.md §4 "Verification methods" + the Proportionality doctrine).
It is trust-based — the box can be checked without the work having happened — so
the process makes the attestation *explicit, named, and auditable* rather than
pretending it's a check. An `Attest` SR is **LLR-exempt** (there's no code symbol
to decompose — the deliverable is the asset itself), but like every SR it still
needs ≥1 TC, whose cell records **who attested and when**:

```csv
SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status,Phase,Aspect
SR-201,Main-theme mood fit,SN-040,"The main theme shall match the game's established mood (heroic, wistful undertone) as judged by the creative lead.","Realizes SN-040: the score sets the emotional tone; no automated check can judge 'fit'.","The creative lead reviews the rendered track against the mood brief and records a pass/fail with notes.",,H,Attest,Verified,,
```

```csv
TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status,Phase
TC-201,SR-201,System,"Creative review of the rendered main theme against the mood brief",Release,"attested-by=A. Rivera (creative lead); attested-on=2026-07-02","Recorded judgment that SR-201's mood-fit criterion is met (pass, with notes)",No,docs/reviews/main-theme-signoff.md,Verified,
```

`trace.py` accepts `SR-201` as legitimately `Verified` but reports it under
**"Verification basis (attested vs mechanized)"** — so an audit always sees how
much of the project rests on trust versus a runnable check. Note the spine here
stays at **high altitude**: `SN-040 → SR-201` ensures the theme's mood isn't
missed or silently broken, and it deliberately *doesn't* decompose "is it
moving?" into finer rows a script still couldn't verify (the doctrine's
creative-domain stance, process-options.md "Proportionality doctrine"). The
binary track itself is managed as a pointer + manifest with its provenance and
license tracked in text (process.md §8 "Binary assets"; §8.1 below).

## 8. A non-functional budget — `requirements/performance-budgets.csv`

Behavioral SRs say *what* the system does; they don't bound *what it costs*. A
quantitative budget lives in its own registry (`PB-###`), owned by the
**Integration/Coordination** hat, and **back-links** the SR / LLR / Module it
bounds so the separation never loses the thread (process.md §9):

```csv
PB-ID,Metric,Refs,Budget,Unit,Tolerance,Direction,Tier,Gate,Owner,Notes
PB-001,Peak RAM exporting the largest input,SR-001;LLR-001,512,MiB,10%,lower-better,Release,warn,Integration,"Measured at the 2GiB size boundary that SR-001's Permutations already enumerate."
PB-002,Model VRAM at inference,SR-030,8,GiB,5%,lower-better,Release,fail,Integration,"GPU module (hypothetical SR-030): a number the author can't invent, so the integrator sets the allocation."
PB-003,Unit BOM cost of the field sensor,SR-040,12,USD,5%,lower-better,Release,warn,Integration,"Cost is a metric like any other (hypothetical hardware SR-040): ISO 25010 omits it, so §9's checklist prompts for it; same registry, same comparator."
```

`PB-001` bounds the *cost* of the CSV export `SR-001` already specifies — same
feature, different axis — and pins the measurement to a boundary that SR's
`Permutations` enumerate, so it restates no dimensions. `PB-002` shows a **VRAM**
budget for a GPU module: a value the module author can't invent, so the integrator
sets the slice and the module measures against it. `PB-003` shows an **economic**
budget — unit BOM cost for a hardware scope — carried by the same registry and
comparator with no new mechanism: cost is simply a metric ISO 25010's
software-quality checklist never prompts for, which is why §9 names it. `trace.py` checks each row's
`Refs` resolve to a real SR/LLR/Module and that the `PB-` id is well-formed — a
budget that drifts off a deleted requirement is caught like any orphan. *Comparing*
the measured numbers against these budgets over time is the harness's job:
`scripts/check_perf.py` (process.md §9) reads a product-emitted `perf-metrics.json`
and flags both an absolute breach (here `PB-002`'s `Gate=fail` would fail the
build) and a regression past `Tolerance` versus the committed `perf-baseline.json`.
The registry here is just the captured, tracked source of truth.

## 9. Two modules in one repo — an internal seam

Everything above is **one module**. A larger repo may hold **several** modules on
the same spine, grouped by the `Module`/component columns, each with an explicit
contract and an integration test at its seam — no new machinery (process.md §10).
Say this repo grows a second module, **`delivery`**, that ships a completed export
to a destination; it consumes the **`export`** module's output. A new stakeholder
need `SN-030` ("get my export off the box automatically") drives its SR. Tag each
module's rows through their LLRs' `Module`/component so a domain hat can own and
filter its slice:

```csv
SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status,Phase,Aspect
SR-001,CSV export (RFC-4180),SN-001,"The system shall export records as RFC-4180 CSV with a header row.","Realizes SN-001.","Output parses as CSV; columns match the schema; special-char fields quoted per RFC-4180.","field=set{plain,comma,quote,newline}",M,Test,Verified,,
SR-050,Deliver export to destination,SN-030,"The system shall upload a completed export to the configured destination and confirm receipt.","Realizes SN-030: the file is useless until it reaches the target.","A completed export reaches the destination and receipt is confirmed; a failed upload is retried and surfaced, never silently dropped.","dest=set{local,s3,sftp}",M,Test,Implemented,,
```

The boundary between the two is a **contract**, so it is an `IF-###` (process.md
§8) — which applies *within* a repo just as across repos, the counterpart naming
the other **module** rather than another repo, both rows in the one
`interfaces.toml`:

```toml
[interface.IF-001]
direction = "Provides"
this_project = "export"
counterpart = "delivery"
contract = "Writes an RFC-4180 CSV at the agreed path with the documented schema (per SR-001)."
signal = "variable"
rationale = "One writer for the export file; delivery must not re-derive its schema."
req_refs = ["SR-001"]
version = "v1"
approval = "approved"

[interface.IF-002]
direction = "Consumes"
this_project = "delivery"
counterpart = "export"
contract = "Reads the export file produced per IF-001 v1 before uploading it."
signal = "variable"
req_refs = ["SR-050"]
version = "v1"
approval = "approved"
```

And the seam gets its **own** integration TC — covered by neither module's internal
unit tests — so the boundary is a tested contract, not a gap between two green
modules (process.md §10). It verifies the consuming SR (`SR-050`, the side that
relies on the contract; `IF-002` links the interface to that SR, and the TC covers
the SR):

```csv
TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status,Phase
TC-050,SR-050,Integration,"Run export then delivery end-to-end; assert the delivered file matches the RFC-4180 contract IF-001 publishes, and that a forced upload failure is retried and surfaced",Full,"dest=set{local,s3,sftp}","Satisfies SR-050 AcceptanceCriteria",Yes,tests/test_delivery_seam.py,Verified,
```

Each module's SRs still decompose into their own `Module`-tagged LLRs as usual (§3;
omitted here to keep the seam in focus), so `SR-050` carries a `delivery`-module LLR
just as `SR-001` carries its `export` one. `Tier=Full` keeps the cross-module test
in the pre-merge suite; the whole-repo `python scripts/trace.py --strict` still
demands **0 orphans across both modules and the seam**. Filtering the registries by
`Module`/component (`export` vs `delivery`) is how each hat reviews its own slice — a reading
convention over columns that already exist, never a separate per-module gate
(process.md §10).

## 10. The next rung — separate repos under a coordinator (design sketch)

> **Rare, and design-only.** This is rung 3 of the escalation ladder (process.md
> §10) — reached **only** when modules need *independent* versioning / ownership /
> release cadence at a scale one repo can't sustain. The full model, and the honest
> limits below, live in `MULTI_REPO.md`; the cross-repo tooling is deferred. Most
> projects stop at §9.

Say the `delivery` module from §9 grows to need its own release cadence, so it is
**promoted to its own repo** (revisitable, far cheaper than a speculative split).
Now a **coordinator** — the Integration/Coordination hat elevated to a repo — holds
the product-level spine and delegates each sub-system. The coordinator delegates an
SR at the **SR tier**: the delegated SR becomes the module repo's top-tier **`SN`**,
which back-links the coordinator SR via a **`ParentRef`**.

The coordinator lists its delegated repos in an optional **`repos.csv`** (`REPO-###`,
`MULTI_REPO.md` §6) — the multi-repo layer a single-repo project never has:

```csv
REPO-ID,Name,Repo,DelegatedSRs,Version,Type,Owner,Notes
REPO-001,export,https://git.example/acme/export,SR-009,v2,owned,Integration,"CSV export, promoted to its own repo."
REPO-002,delivery,https://git.example/acme/delivery,SR-010,v1,owned,Integration,"Uploads a completed export to the destination."
REPO-003,plant,https://git.example/acme/plant,SR-011,v1,owned,Integration,"Integration/plant repo: assembles export+delivery and runs the end-to-end demonstration."
REPO-004,object-store,—,,vendor-2024,external,Integration,"Purchased S3-compatible store; no repo builds it. Referenced via the catalog IF-### (owner of record = coordinator); delegates no functional SR."
```

`trace.py` keeps `DelegatedSRs` honest **within the coordinator repo**: `SR-009/010/011`
must be real coordinator SRs, and a malformed `REPO-` id fails — the same back-link
discipline as `PB-###`. The `external` part `REPO-004` delegates nothing (an empty
back-link is allowed here — it is referenced only through the interface catalog).

**The SR-tier handoff.** The coordinator's `SR-010` is tagged delegated; in the
`delivery` **repo** it reappears as that repo's founding `SN`:

| Repo | Row | Delegated / ParentRef |
|---|---|---|
| coordinator | `SR-010` — records reach the configured destination and receipt is confirmed | `Delegated=REPO-002` |
| delivery | `SN-001` — deliver a completed export to the destination and confirm receipt | `ParentRef=SR-010` |

`Delegated` and `ParentRef` are optional, schema-safe columns (like `Lifecycle`).
The `ParentRef` link points **across the boundary** into the coordinator repo, so no
single `trace.py` run validates it — that reconciliation is the deferred cross-repo
join (`MULTI_REPO.md` §7).

**Interfaces are pointers, not copies** (process.md §8, applied across repos). Each
contract's spec lives once in its **owner**; the coordinator's catalog only references
the owner `IF-###`:

```csv
IF-ID,Direction,ThisProject,Counterpart,Contract,Req-Refs,Version,Approval
IF-010,Provides,export,delivery,"RFC-4180 CSV at the agreed path (spec owned by the export repo, per its SR-009).",SR-009,v2,Stable,Verified
IF-011,Consumes,delivery,object-store,"S3 PutObject API of the purchased store; the coordinator catalog is the owner of record and links the vendor datasheet.",SR-010,vendor-2024,Stable,Verified
```

`IF-010`'s spec is owned by a repo that **builds** the surface (`export`); `IF-011` is
a **purchased part no repo builds**, so its owner of record is a **coordinator-held**
catalog row linking the datasheet.

These `IF-###` ids are **owner-local** — each repo has its own `IF-001…`, so the
coordinator references them by a stable coordinator-level id (`CIF-###`) that also
records the owner's current version and each consumer's pin. That mapping is what lets
the coordinator catch **drift**: if the `export` repo ships `IF-010@v3` while `delivery`
still pins `@v2`, the coordinator flags the stale pin (weighted by `Approval`) and
sequences `delivery`'s contract-test re-run against v3 — the interface's own §8 fixture
judges actual compatibility, the human signs a real break. The catalog registry and
that check are deferred tooling (`MULTI_REPO.md` §3.3, §3.7, §7).

**Two requirement scopes.** `SR-010` is *module-scoped* — verified inside the delivery
repo. But "an exported file arrives intact at the destination end-to-end" is
*composition-scoped*: it exists only for the assembled whole and no single module owns
it. It is a coordinator SR (`SR-011`, `Verification=Demonstration`) delegated to the
**plant repo** (`REPO-003`), which assembles export + delivery + a virtualized
destination and runs the demonstration — "the module whose deliverable is a runnable
verification of the assembly."

**The honest limit.** A delegated SR (`SR-010`, `SR-011`) has no LLR or TC *in the
coordinator repo* — its code and tests are across the boundary — so a plain `trace.py
--strict` there reports it as an orphan. The `Delegated` marker records why; closing it
against the module's returned status is the **cross-repo trace join**, which one
`trace.py` run cannot do and the kit does **not** fake (`MULTI_REPO.md` §6–§7). The
coordinator sequences and reads status; it never builds or runs anything.

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
  `Verification=Demonstration`/`Manual`, and a
  procedure-recording `Release`-tier TC the release checklist finds.
- **Tag the lifecycle phase** (§7) so the phase your product tends to neglect
  gets written — Provision/Startup for tools, the Runtime *operating environment*
  for embodied/service products — not just the one you're already looking at.
- **Quantitative budgets go off the spine** (§8) — `PB-###` in
  `performance-budgets.csv`, owned by the Integration hat, back-linked to the
  SR/LLR/Module they bound.
- **Substance, not just existence** (DevBar-Release) — the implementing symbol must do real
  work, not a `pass`/`...`/`NotImplementedError` stub that still satisfies its
  trace links. It's an Inspection call; `scripts/check_stubs.py` is the optional,
  warn-first Python tripwire that surfaces candidates (process.md §4).
- **Several modules share one repo and one spine** (§9) — group each module's rows
  by `Module`/component, record every internal seam as an `IF-###`, and test it with a
  dedicated integration TC; the whole-repo trace gate stays the source of truth
  (process.md §10). Single-module is still the default — scale up only when the
  scope forces it.
- **Separate repos under a coordinator are the rare top rung** (§10) — delegate an
  SR to a module repo (it becomes that repo's `SN`, back-linked by `ParentRef`),
  list delegated repos in the optional `repos.csv`, keep interfaces as pointers to their
  owner, and verify emergent behavior in a delegated plant repo. It is a *design*
  (`MULTI_REPO.md`); the cross-repo tooling is deferred. You almost certainly don't
  need it.
