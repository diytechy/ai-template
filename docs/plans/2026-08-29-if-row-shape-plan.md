# The interface row shape — the OI-67 (a) program plan

**Status: plan of record.** `OI-67` was ruled (a) by the owner on 2026-08-29
(record:
[../log.d/2026-08-29-oi67-ruled-a.md](../log.d/2026-08-29-oi67-ruled-a.md)).
This document turns the ruling into six sequenced slices, states the
decisions the ruling left to the driver with the alternative each one beat,
and is the `specref` every slice's row points at. The rows are filed under
`docs/work/queued/`; their order is the `needs` edges below, not this prose.

The owner's shape, in the owner's words: an interface says *what the
information plugs into, who it serves, and what the data is* — one row is one
direction of one kind of information. Everything below serves that sentence.

## 0. Where the program stands (2026-08-29, end of the first session)

Landed, in this order, on `contract_split`: **slice 1** (WI-528, the shape in
code and the registry converted), **slice 5** (WI-532, PROCESS.md §8, the
templates, the RESYNC entry, `migrate_carrier --if-shape`), **slice 2** (WI-529,
headers in non-Python owners and hooks, the owner-exact reverse check),
**slice 3** (WI-530, the four-worker cell pass — 132 of 136 definitions stated
beside their owners; the round at `docs/reviews/2026-08-29-oi67-slice3/`).
Remaining: **slice 4** (WI-531, the split — its per-row worklist is the `note`
field of each worker report in that folder, summarised in the WI-530 log
fragment) and **slice 6** (WI-533, arm the gate), plus two things slice 3 could
not place: the CSV loaders must skip a leading `#` header before `IF-031`'s
owner can declare, and a rule is owed for where our READING of an
`external:`-owned surface lives (`IF-032`, `IF-036`, `IF-041` keep their
legacy `contract` cell until then). Resume from `docs/status.md`.

**Program complete (2026-08-29, end of the third sitting).** Both remaining
slices landed: **slice 4** (WI-531, the split — one row, one direction, one
kind: twenty rows minted, two duplicate pairs collapsed, 136 → 154) and
**slice 6** (WI-533, the gate armed — every declared seam states its body, the
retired cells are strict findings, one CSV reader for every loader, and the
rule this section left owed: our reading of an `external:`-owned surface lives
in the header of the kit module that faces it, a row with no in-tree endpoint
at all being refused). The slice-6 cross-family adversarial round ran — eleven
findings, nine folded at the root (record
[../log.d/2026-08-29-oi67-slice6-round.md](../log.d/2026-08-29-oi67-slice6-round.md),
dispositions
[../reviews/2026-08-29-oi67-slice6/README.md](../reviews/2026-08-29-oi67-slice6/README.md)).
The arms the split surfaced landed as **WI-534** (nine rows `IF-165`–`IF-173`,
154 → 163; the reference at 74 / 163 / 163 — record
[../log.d/2026-08-29-wi534-if-arms.md](../log.d/2026-08-29-wi534-if-arms.md)).
The four decisions flagged for the owner (4.1, 6.2, 6.7, 6.8) were accepted
([../log.d/2026-08-29-owner-rulings-oi67-decisions.md](../log.d/2026-08-29-owner-rulings-oi67-decisions.md)).
Nothing remains on this plan; what stands after it is on `docs/status.md`.

## 1. The row, after

```toml
[interface.IF-013]
owner = "scripts/check"                       # REQUIRED — the providing THING
consumers = ["external:downstream adopter"]   # REQUIRED — who reads it
channel = "exit-code"                         # REQUIRED — closed vocabulary
data = "0 pass · 1 fail · 2 usage"            # OPTIONAL — the alphabet or schema pointer
version = "v1"
status = "Drafted"
interface_to_external = "B-05"                # unchanged optional cells follow
```

**Cells that leave:** `provider`, `req_refs`, `contract`, `signal`,
`signal_note`. **Cells unchanged:** `consumers`, `version`, `status`,
`carried_by`, `verified_by`, `interface_from_external`,
`interface_to_external`, `component`, `rationale`, `notes`.

### `owner` — the providing thing, one spelling

A module path (`scripts/check`), a file or directory path
(`docs/requirements/performance-budgets.csv`, `docs/work/`), or an
`external:` party (`external:git`). **Never a requirement or design id.**
Today's `owner` is id-typed and today's `provider` is the path; the two were
one fact in two spellings on 106 rows and the id alone on the rest. One cell,
one spelling, and it is the same spelling `consumers` already uses, so both
endpoint cells are validated by the same rule: a path must exist in the tree
(warn-first, as `consumers` is today), an `external:` prefix says it
deliberately does not.

*The alternative beaten:* keep `owner` polymorphic (`LLR-###` **or** a
path). Rejected because a design row → its module is a derivation, and the
kit's rule is that a derivable cell is a second spelling of a fact that
already has a home (the `provider` shed, OI-60). Every LLR owner converts
mechanically to its `module`.

**The spine link is derived, not stated.** An owner path reaches the spine
through the design rows whose `module` names it, or through the `Implements:`
lines in its header. A row whose owner reaches neither is an ADVISORY (warn
only — "this seam traces to no requirement"), replacing today's strict
back-link finding on `req_refs`. Seam-to-test coverage was never on this
cell: it joins on a TC's `Verifies`, unchanged.

### `channel` — closed, eight values

| `channel` | what crosses | today's `signal` reading |
|---|---|---|
| `cli` | an invocation surface — argv flags and arguments | — |
| `exit-code` | a finite code alphabet a process returns | `discrete` |
| `stdout` | text a process emits — findings, a report, a verdict line | `variable` |
| `file` | a file or directory medium with a schema — a registry, a config, a generated document | `variable` |
| `call` | an in-process API — a function, class or constant another module imports | `variable` |
| `env` | an environment variable or launcher slot | `discrete` |
| `git` | repository state — refs, trailers, a staged diff, hook argv | `variable` |
| `bytes` | opaque content — fetched sources, a vendored tree | `variable` |

A dial read from `docs/process.toml` is `file` (the medium is the file; `data`
names the key). A directory of Python sources walked by AST is `file`.
`signal`'s `discrete`/`variable` pair is subsumed: `exit-code` and `env` are
the discrete kinds, the rest are unbounded.

*The alternative beaten:* keep `signal` and add `channel` beside it. Rejected —
two typed cells that must agree is the shape that produced `Status` beside
`Stability`; `signal` reads `variable` on 127 of 136 rows and typed nothing.

### `data` — the alphabet, short, checked

OPTIONAL. The finite alphabet when there is one (`0 pass · 1 fail · 2
usage`, `off | ask | deny`), or a one-clause schema pointer (`[interface.IF-###]
rows, keys per the file header`). **Ceiling 160 characters**, and the four
form rules that policed `contract` move here unchanged: no work-item id, no
decision citation, no rationale connective, and a named symbol or path must
resolve. It is not the definition — the definition is the header body — it is
the row's typed summary of it, the thing a planner or a reader scans.

### The definition lives beside the code

What the owner promises — the flags, the schema, the guarantees — is the
`Contract IF-###:` body under the owner's `Contracts:` marker (WI-527), and
nowhere else. After this program a declared seam with no body is a FINDING
(slice 6), because under this shape it is an interface with no definition.

**Where the owner is not a Python module** (31 rows today) the body needs a
home, and slice 2 gives it one: a `#`-comment header at the top of a
TOML/INI/CSV/extensionless file carries the same `Contracts:` marker and
`Contract IF-###:` bodies, read by the same harvester. **A generated file's
definition is declared by the module that writes it** — its owner is the
writer module, `channel = "file"`, `data` names the path — because the writer is
the one home a check can hold to the code; a hand-edited file (a registry,
`stack.ini`, `process.toml`) declares in its own header.

### One row, one kind

A request and its answer are two rows with the same owner (`cli` in,
`exit-code` out). A module that reads one file and writes another is two rows
(a `file` row per medium, each owned by the medium's declarer). A seam that
today bundles several kinds — a library plus its CLI, ten registries read as
one — is split to one row per kind, **or** declared once as a carrier with
constituents on `carried_by` when the bundle is the unit a consumer really
pins (the spine registries as one format, `IF-021`). The measured population:
14 two-way rows (→ 35), 35 bundled rows (→ 91 if fully split); 87 already
clean.

## 2. What the readers and checks become

| Today | After |
|---|---|
| `spine_carrier` IF schema: `Contract`, `Signal`, `Req-Refs` required | `Owner`, `Consumers`, `Channel`, `Version`, `Status` required; `Data` optional; the five retired columns are schema findings (slice 6 — until then `Contract` reads as an optional LEGACY cell with an advisory counting it) |
| `kitlib.spine.seam_provider(row, llr_modules)` — derives through the LLR | `seam_owner(row)` — the cell, verbatim; the `llr_modules` join retires |
| `trace.interface_findings` — `Req-Refs` back-link (strict) + Provider endpoint advisory | owner resolution (strict: a path exists or is `external:`), spine-reachability advisory (warn) |
| `trace.if_ownership_advisories` — owner is exactly one SR/LLR | retired; owner is an endpoint and the endpoint rule covers it |
| `trace.if_contract_advisories` — five rules on `Contract` | the same five rules on `Data`, ceiling 160 |
| Provider derivability advisory + SR-owned-Provides report | retired — nothing to derive |
| `check_trajectory._declared_seam_pairs` — provider + consumers | owner + consumers |
| `check_trajectory` reverse check — id-global | owner-exact: the row's owner (module or file) must be the source that declares it |
| `gen_components.seam_placement` | owner + consumers |
| `gen_arch_map._seam_edges`, `load_seam_modules` | owner + consumers; the modules join retires |
| `plan_briefs.IF_SURFACE_COLUMNS` = ID, Owner, Provider, Consumers, Contract | ID, Owner, Consumers, Channel, Data |
| `gen_okf` description ← `Contract` | ← `Data`, else `Channel` |
| `intake._seam_lines` | owner → consumers: kind · data |
| `gen_release_checklist` §4 — reads `Counterpart` (retired at WI-455) and `Req-Refs` | owner · consumers · kind |
| `migrate_carrier` — CSV → TOML | + an in-place shape arm for a TOML registry in the old shape (slice 5) |

## 3. The slices

Each slice ends at the commit bar; the full suite runs before a slice is
claimed done. The `needs` edges are the order.

### Slice 1 — the shape in code

The readers, the checks, the schema, the test fixtures, and the kit's own
registry converted **mechanically**: `owner` ← stated `provider`, else the LLR
owner's `module`; `channel` seeded from the 2026-08-29 per-row classification;
`data` ← `signal_note` where an alphabet is stated; `provider`, `req_refs`,
`signal`, `signal_note` dropped. **`contract` is NOT dropped here** — it
stays as a legacy optional cell, counted by an advisory, until slice 3 gives
its content a home. 21 rows have no provider to fold (the published media no
cell names): their `owner` is authored by hand in this slice from the medium
the cell names, because a row with an empty required cell cannot land.

Done when: every reader in §2 reads the new cells; every check in §2 is
rewritten or retired with its tests; the kit's registry parses under the new
schema with zero strict findings; commit bar green; full suite green.

### Slice 2 — the header reaches every owner

`scan_contracts` reads a `#`-comment header at the top of any file under the
declared scan roots plus the registries and config the seams name — TOML,
INI, CSV, Markdown front-comment, and extensionless hooks — for the same
`Contracts:` marker and `Contract IF-###:` bodies. The reference lists them
under the file's path. The reverse check becomes owner-exact. `IF-134` and
`IF-135` (the git hooks) declare.

Done when: a `#` header in a non-Python file harvests identically to a
docstring; the hooks declare their seams; the reverse check names the row
whose owner is not its declarer; tests for each; commit bar green.

### Slice 3 — the cell pass, on the new shape

Per row: the `contract` cell's definition moves into the owner's `Contract
IF-###:` body (module docstring or file header), `channel` is confirmed or
corrected, `data` is written where an alphabet exists, and `contract` is
deleted. Per-row authoring, parallelised by module family (each worker owns a
disjoint set of source files and reports the row cells back; the registry is
folded serially). Done when: zero legacy `contract` cells; the reference
reads 0 "declared, not stated"; the measured authoring cost recorded.

### Slice 4 — the split

The 14 two-way rows first, then the 35 bundled rows — each either split to
one row per kind or declared once with constituents on `carried_by`. New ids
minted from the watermark, each `Drafted`; every `TC.Verifies`, `carried_by`,
`Implements:` line and `Contracts:` marker citing a split row re-pointed.
Done when: no row describes two kinds; the reference and the component view
regenerate clean; the watermark records the mint.

### Slice 5 — ship it

`PROCESS.md` §8 (inside its byte budget — the contract paragraphs shrink),
`PROCESS_OPTIONS.md` "Intra-repo interfaces & the architecture graph",
`interfaces.template.toml`, `INTERFACES.template.md`,
`docs/registry-machinery-reference.md`, `docs/enforcement-audit.md`, a
`RESYNC_PACK.md` entry, and the converter: `migrate_carrier --if-shape` does
to an adopter's registry what slice 1 did to ours and REPORTS every row it
could not finish (an owner it cannot derive, a `contract` it cannot place).
Done when: `test_dogfood_sync` passes against the shipped template; a
scaffold bootstraps and its example row parses; the RESYNC entry carries the
search recipe.

### Slice 6 — arm the gate

A declared seam with no `Contract IF-###:` body is a finding under
`--strict`; the five retired columns are schema findings rather than legacy
reads; the legacy advisory from slice 1 retires. Done when: the kit's own
tree is clean under the armed gate and a planted violation fires.

## 4. Decisions taken by the driver, for review at close

1. **`owner` is a path, never an id** (§1). Beat: polymorphic id-or-path.
2. **Eight `channel` values, `signal` retired** (§1). Beat: `signal` kept beside
   `channel`. Named `channel`, not `kind`: `kind` is already the relationship
   tier's column on the same carrier, and one name may carry one meaning
   repo-wide (D-3).
3. **`data` is optional and capped at 160** (§1). Beat: required (would force
   a value onto `call` rows whose alphabet is a signature the body states).
4. **The legacy `contract` cell survives slices 1–2** rather than being
   dropped with the others. Beat: drop-and-lose (its content has no home
   until slice 3) and defer-the-schema (the kit's own registry would then be
   the last to convert, and every test would be written against a shape the
   registry did not have).
5. **A generated file's definition is declared by its writer**; a hand-edited
   file declares in its own header (§1). Beat: every file declares in its own
   header (a generated file's header is overwritten by its generator — the
   body would have to be templated into the generator anyway).
6. **The spine link is an advisory, not a strict finding** (§1). Beat: strict
   — 31 rows are owned by files and external parties that no design row
   names today, and a strict rule would red the tree on the day it landed.
7. **Bundles split OR carry**, per row, not by rule (§1, slice 4). Beat:
   always split (213 rows, the spine registries as ten seams nobody pins
   separately) and always carry (hides the two-way rows inside carriers).
8. **The far side names the direction** (`requestors` | `consumers`, exactly
   one) — the owner's proposal. Beat: one far-side list with the direction
   implied by `channel` (the shape slice 1 first built; it had no cell for an
   owner that receives what it defines). Seeded from the channel — `cli`,
   `env`, `call` name requestors — and confirmed row by row in slice 3.
9. **Header-first for parallel work** (slice 5, PROCESS.md §8): a WI that
   mints a module mints its seam rows and the module's stub header with the
   `Contract IF-###:` bodies BEFORE any code, so workers coding against it
   read the same home the finished module will have. The "declared, not
   stated" line is the signal that a definition is not written yet. Beat:
   carrying the expected inputs/outputs in the WI spec (a second copy that
   drifts at close).

## 5. Measured baseline (2026-08-29, before slice 1)

- 136 live rows; `provider` stated on 30, absent on 106; `req_refs` redundant
  on 88; `signal` = `variable` on 127; `contract` required on all.
- Direction: 87 one-way · 14 two-way · 35 bundled · 0 unclear (every row
  read).
- Owners that are not Python modules: 31 (24 files, 4 directories, 3
  external). Bodies stated: 2 of 136.
- Shipped surfaces: 2 templates (260 lines), `PROCESS.md` §8,
  `PROCESS_OPTIONS.md` (82 lines), 39 doc references, 12 scripts, 31 test
  modules.

## 6. Risks named

- **Slice 1 is the widest diff** in the program and cannot be split without
  leaving the tree red between halves; it lands as one commit on the commit
  bar plus the full suite.
- **The mechanical `channel` seed is a classification, not a reading** — slice 3
  confirms every value. A row whose seed is wrong is wrong until then, and
  the plan says so rather than pretending the seed is authored.
- **Adopters lose `req_refs` outright.** The converter writes the dropped
  values into the RESYNC report so nothing leaves a repo unseen, and the
  entry says what replaces the grep.
