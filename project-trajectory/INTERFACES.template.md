# Cross-Project Interfaces (IF-###)

<!-- kit-only -->
Copied into a new repo as `docs/interfaces.md` by `scripts/bootstrap.py`.
<!-- /kit-only -->
Owned by the **System Engineer** hat. Use this when a project provides or
consumes a contract shared with another project/repo, or — intra-repo — when
module-to-module seams are worth declaring (process.md §8); a single-module
standalone deliverable skips it.

It keeps interlinked projects honest without heavy multi-repo machinery: each
shared contract gets one stable id, one home, and a link back into the same
`SN→SR→LLR→TC` spine. The registry is `requirements/interfaces.toml`; this page
is the thin, human-readable index over it.

---

## Why a separate registry

A cross-project link is a requirement with an *external* counterpart, so it
needs the things ordinary requirements have — an owner, an acceptance contract,
a test — **plus** a version and a `Status` the other side can rely on.
Putting these in one place stops the classic failure of interlinked projects:
each side assumes a slightly different contract and they rot apart silently.

## ID scheme & columns

`IF-###` — Cross-Project Interface. Zero-padded, stable, never reused (its own
namespace, parallel to SN/SR/LLR/TC).

| Column | Meaning |
|---|---|
| `IF-ID` | Stable id for this interface. |
| `Owner` | **Required.** The providing *thing*, in the one spelling `Consumers` uses: a module path (`scripts/check`), a file or directory path (`docs/stack.ini`, `docs/work/`), or an `external:` party. **Never a requirement or design id** — the requirement the seam answers to is reached *through* the owner (the design rows whose `Module` names it, or the `Implements:` line in its header) and is not stated on the row. An id-shaped owner is a finding; a module-shaped owner that reaches no requirement is a warning. A generated file is owned by the module that writes it; a hand-edited file is owned as itself and declares in its own header. |
| `Requestors` / `Consumers` | **The far side names the direction — exactly one of the two is set**, a **list** either way. `Requestors` put information *into* the surface the owner defines (they call the function, invoke the CLI, set the env var, write the file); `Consumers` take what the owner emits (they read the file, the exit code, the stdout). The owner defines the surface in both cases; the key says which way the information runs, so one row is one direction by construction — a call is one row, a CLI's arguments and its exit code are two. Both or neither is a finding. Name the sides you have MEASURED, and the open-ended ones as a class (`external:downstream adopter`). Every endpoint cell is checked against the tree, warn-first; prefix a deliberately-outside-the-tree endpoint with `external:`. |
| `Channel` | **Required, closed**: what crosses, typed — `cli` (an invocation surface: argv), `exit-code` (a finite code alphabet), `stdout` (emitted text: findings, a report), `file` (a file or directory medium with a schema), `call` (an in-process API), `env` (an environment variable or launcher slot), `git` (repository state), `bytes` (opaque content). A dial read from a config file is `file`; a source tree walked by AST is `file`. |
| `Data` | Optional. The finite alphabet when there is one (`0 pass · 1 fail · 2 usage`, `off | ask | deny`) or a one-clause schema pointer. ≤160 characters; no work-item id, no decision citation, no rationale connective; a named symbol or path must resolve (warn-first). The row's typed summary — **not the definition**, which lives beside the code in the owner's `Contract IF-###:` body and is harvested into the interface reference. |
| `Rationale` | **Why the seam is drawn here.** Empty is allowed; the argument, never the citation. |
| `VerifiedBy` | Optional, and **empty is a real answer**: "verified in its own right". Filled, it names the parent whose tests cover a *low-level* seam — a `TC-###` or an `LLR-###` — so building blocks are not forced into a test each. Warn-first that the pointer resolves; nothing reads whether the named test really exercises the seam. |
| `CarriedBy` | Optional. **Interface composition** — a constituent naming the bundle that carries it (`IF-###`). A constituent is still one owner and one channel; the bundle is the unit a consumer pins. The carriage graph must resolve and be acyclic; depth past 2 warns. Empty means "not a constituent", which is most rows. |
| `Version` | Contract version the other side codes against (e.g. `v1`, a semver, a schema hash). |
| `Status` | **Closed**, and the row's **one** maturity field: `Drafted` · `Approved` — the spine's own words, shared with `external.toml`. `Founded` is **not applicable** to this tier: it means settled *and demonstrated*, while an approval says only that the seam is agreed. Flipping a cell to `Approved` is a human act in a reviewed commit. |
| `interface_from_external` / `interface_to_external` | The directional tie-back to a `B-##` crossing in `external.toml`, present **only** when this row REALIZES one — `from` for an IN crossing, `to` for an OUT one, both for in/out. A row with neither is an internal seam; that absence IS the statement. |
| `Component` | Optional `CMP-###` membership tag for the component layer; empty when unused. |
| `Notes` | Free-form; argument, never citation. The `source`/`sink` honesty valve lives here — `source` marks the row's `Owner`, `sink` its far side, silencing the missing-seam coverage warn for that side (see the registry's `-000` row). |

## Rules (keep links from rotting)

- **One definition, one home.** The owner's header holds the authoritative
  definition (`Contracts:` marker + `Contract IF-###:` bodies); the far side
  links it by `IF-ID` and never re-states it. If both repos describe the shape,
  they will diverge — link instead. **The gate is armed:** a row whose owner
  declares it but states no body is a `check_trajectory --strict` finding, and
  so is a source whose header the contract grammar refuses; a source declaring
  a row another in-tree source owns is one too. An owner that declares nothing
  only warns (the migration list, visible in the reference's summary line). An
  `external:`-owned row is stated by the
  kit module on its far side — our reading of a surface we do not own. The
  retired cells (`Contract`, `Provider`, `Req-Refs`, `Signal`, `SignalNote`)
  are `trace.py --strict` findings wherever they still appear. A CSV registry
  may carry the same `#` header; every kit reader strips it.
- **Every interface is backed by a TC.** A seam this repo owns needs a contract
  test that asserts the published shape; a seam an `external:` owner serves
  needs a test (or recorded fixture/mock pinned to `Version`) proving we read or
  request it correctly. No interface ships untested. The requirement a seam
  answers to is reached through its owner — a design row naming the module, or
  the module's `Implements:` line — not stated on the row.
- **`IF-` ids are repo-local — never reuse an id across repos.** Each repo owns
  its own `IF-###` space, so `IF-007` in two repos are *different* interfaces
  that merely share a string (MULTI_REPO.md §3.3 — they would collide the
  moment anything referenced both). The two ends of one cross-repo contract
  therefore carry **different local ids** (exactly as the snippet below shows),
  and a foreign seam is cited as the **qualified pair** — the counterpart repo
  (its name or `REPO-###` row) **plus** its local `IF-###` and pinned version —
  written in the far-side cell and `Data`/`Notes`, **never in the `IF-ID`
  column** (`trace.py`'s `^IF-\d+$` integrity pattern rejects any qualified
  form there). Under a coordinator repo, the one stable global handle is the
  coordinator-level `CIF-###` (MULTI_REPO.md §3.3). Honesty note: no tool
  validates the far side of a cross-repo reference — it is a text convention;
  keep the trail two-way by recording the counterpart repo + matching id on
  both rows.
- **Approval gates change.** Changing an `Approved` contract requires a notice
  to the counterpart and a version bump; a `Drafted` one may change freely. Note
  breaking changes in the audit log and bump `Version`.
- **The owner's side closes the read.** The thing named in `Owner` defines the
  surface and answers for its correctness; a far side verifies against the
  pinned version. There is no direction column: the far-side KEY is the
  direction (`Requestors` into the owner, `Consumers` out of it), and ownership
  is the owner cell.

## Worked snippet

```toml
# In billing-api's registry — it OWNS the route (its module defines it) and
# reporting-etl REQUESTS it; the schema itself is stated in the handler's
# `Contract IF-001:` body, not here.
[interface.IF-001]
owner = "src/api/invoices"
requestors = ["external:reporting-etl"]
channel = "call"
data = "GET /v1/invoices -> JSON per docs/openapi.yaml#/Invoice"
rationale = "One read model for invoices; the ETL must not re-derive totals."
version = "v1"
status = "Approved"

# In reporting-etl's registry — the same seam from the far end: the owner is
# the OTHER repo, this repo's module is the requestor, and the pin is stated.
[interface.IF-002]
owner = "external:billing-api"
requestors = ["src/etl/invoices"]
channel = "call"
data = "GET /v1/invoices, billing-api IF-001 v1; fixture tests/fixtures/invoice_v1.json"
version = "v1"
status = "Approved"
```

Read together: `billing-api` publishes `IF-001` (with a contract test on the
schema); `reporting-etl` requests the same contract as `IF-002`, pins `v1`, and
tests against a recorded fixture. Grep `IF-001` across both repos to see the full
link. If `billing-api` needs a breaking change it bumps to `v2`, notifies
`reporting-etl`, and both rows move to the new version deliberately — never by
accident.
