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
| `Provider` | The side the contract is served **from** — a repo/project name, or intra-repo a module, the file medium itself, or an external actor. **Omit it wherever `Owner` derives it**: an `Owner` that is a design row naming exactly one `Module` IS the provider, and a derivable cell is a second spelling that can disagree with the first. State it when the owner is a requirement (which names no module), when the owner names several modules (a set, not the fact), or when the provider is a file or an `external:` party. A warn-only advisory names any row that states one its owner already derives. |
| `Consumers` | A **list** of the sides that read the contract — the other project/repo, or intra-repo other modules, a file path, or an external actor. Name every reader you have MEASURED, and the open-ended ones as a class (`external:downstream adopter`); one seam read by three modules is one row with three consumers, not three rows copying one `Contract`. **Both endpoint cells are checked against the tree**, warn-first: one that resolves to no module, file or directory is named individually (a spine file that migrated and left its seam row behind is the failure this catches). Prefix a deliberately-outside-the-tree endpoint with `external:` — `external:downstream adopter`, `external:git` — a value convention, not a column, so it rides the carrier and cannot drift from the cell it qualifies. |
| `Contract` | One testable line naming the surface (REST route, CLI, file schema, event, library symbol) + a link to its spec. **What crosses, typed — nothing else** (process.md §8): no rationale, no work-item id, no decision citation, ≤500 characters, and **no restatement of the `Owner` row** — where the detail already lives on the owner and in the module, the contract states the crossing and stops (`SR-006's obligation delivered as a CLI at check.py; crosses B-05`), keeping a clause only for a typed fact the owner does not state. A named symbol or path here is checked against the tree, warn-first: `SCHED_*`, `Foo.bar` or `CONSTANT_NAME` must resolve in the declared source surface, and a named path must exist. |
| `Signal` | **Closed**: `discrete` (a finite enumerable alphabet — exit code, gate name, status enum, dial) or `variable` (unbounded content — prose, file bytes, a count, a duration). If both cross, the row is `variable`. |
| `SignalNote` | Optional. Why the typing is not obvious — a crossing that carries both kinds, or one the `Contract` does not type. |
| `Rationale` | **Why the seam is drawn here.** Empty is allowed; this is the home the `Contract` cell's argument moves to. |
| `Owner` | **The one row answerable for this interface**, id-typed and polymorphic: an `SR-###` **or** a design-tier `LLR-###`, resolved against whichever registry the prefix names — both are legitimate because requirements and design rows decompose the same thing at different levels. Exactly one; naming nobody and naming several are both findings. Not `Req-Refs`: that lists everything the seam realizes or relies on, this names the row that answers for it. |
| `VerifiedBy` | Optional, and **empty is a real answer**: "verified in its own right". Filled, it names the parent whose tests cover a *low-level* seam — a `TC-###` or an `LLR-###` — so building blocks are not forced into a test each. This is the only place the position is sayable: `Verification`'s one exemption is LLR-exemption on an SR, and an IF row carries no `Verification` cell. Warn-first that the pointer resolves; nothing reads whether the named test really exercises the seam. |
| `CarriedBy` | Optional. **Interface composition** — a constituent naming the bundle that carries it (`IF-###`). Six seams riding one larger seam name the same carrier, so granularity stops being a forced choice: declare the bundle *and* its parts, and decompose only as far as is useful. The carriage graph must resolve and be acyclic; depth past 2 warns. Empty means "not a constituent", which is most rows. |
| `Req-Refs` | The requirement(s) here that realize or rely on it — ties the interface into the local spine. **Not the design tier's `SR-Refs`**, which names a row's *parent*: this one names the requirements the seam hangs off, which is a different relationship, so it gets a different name. |
| `Version` | Contract version the other side codes against (e.g. `v1`, a semver, a schema hash). |
| `Status` | **Closed**, and the row's **one** maturity field: `Drafted` · `Approved` — the spine's own words, shared with `external.toml`. `Founded` is **not applicable** to this tier and never will be: it means settled *and demonstrated*, while an approval says only that the seam is agreed. Flipping a cell to `Approved` is a human act in a reviewed commit. (Two columns retired into this one: `Stability` — `Experimental`/`Stable`/`Deprecated` — at WI-442, and a short-lived `Approval` at the 2026-08-17 status unification. Never carry a second maturity column beside it; the reason this tier has one field is that it once had two meaning different things on the same row.) |
| `interface_from_external` / `interface_to_external` | The directional tie-back to a `B-##` crossing in `external.toml`, present **only** when this row REALIZES one — `from` for an IN crossing, `to` for an OUT one, both for in/out. A row with neither is an internal seam; that absence IS the statement, so there is no "internal" value to set wrongly. |
| `Component` | Optional `CMP-###` membership tag for the component layer; empty when unused. |
| `Notes` | Free-form. The `source`/`sink` honesty valve lives here — `source` marks the row's `Provider`, `sink` its `Consumers`, silencing the missing-seam coverage warn for that side (see the registry's `-000` row). |

## Rules (keep links from rotting)

- **One contract, one home.** The owning side (`Provides`) holds the
  authoritative spec; the consuming side links it by `IF-ID` and never re-states
  it. If both repos describe the shape, they will diverge — link instead.
- **Every interface is backed by an SR and a TC.** A `Provides` interface needs
  a contract test that asserts the published shape; a `Consumes` interface needs
  a test (or recorded fixture/mock pinned to `Version`) proving we read it
  correctly. No interface ships untested.
- **`IF-` ids are repo-local — never reuse an id across repos.** Each repo owns
  its own `IF-###` space, so `IF-007` in two repos are *different* interfaces
  that merely share a string (MULTI_REPO.md §3.3 — they would collide the
  moment anything referenced both). The two ends of one cross-repo contract
  therefore carry **different local ids** (exactly as the snippet below shows),
  and a foreign seam is cited as the **qualified pair** — the counterpart repo
  (its name or `REPO-###` row) **plus** its local `IF-###` and pinned version —
  written in `Consumers` and `Contract`/`Notes`, **never in the `IF-ID`
  column** (`trace.py`'s `^IF-\d+$` integrity pattern rejects any qualified
  form there). Under a coordinator repo, the one stable global handle is the
  coordinator-level `CIF-###` (MULTI_REPO.md §3.3). Honesty note: no tool
  validates the far side of a cross-repo reference — it is a text convention;
  keep the trail two-way by recording the counterpart repo + matching id on
  both rows.
- **Approval gates change.** Changing an `Approved` contract requires a notice
  to the counterpart and a version bump; a `Drafted` one may change freely. Note
  breaking changes in the audit log and bump `Version`.
- **The `Owner` cell's side closes the read.** The row named in `Owner` is
  answerable for the contract's correctness and closes the final read on it; a
  consuming side verifies against the pinned version. (This replaces "Direction
  drives ownership. Only the `Provides` side may close the owner's final read",
  which fused two facts — and the `Direction` column it named is gone: flow is
  the shape of the row, `Provider` → `Consumers`, and ownership has its own
  cell.)

## Worked snippet

```toml
[interface.IF-001]
provider = "billing-api"
consumers = ["reporting-etl"]
contract = "GET /v1/invoices returns the documented JSON schema (see docs/openapi.yaml#/Invoice)."
signal = "variable"
rationale = "One read model for invoices; the ETL must not re-derive totals."
req_refs = ["SR-014"]
owner = "SR-014"
version = "v1"
status = "Approved"

[interface.IF-002]
provider = "billing-api"
consumers = ["reporting-etl"]
contract = "Reads GET /v1/invoices; depends on IF-001 v1 schema (pinned fixture in tests/fixtures/invoice_v1.json)."
signal = "variable"
req_refs = ["SR-031"]
owner = "SR-031"
version = "v1"
status = "Approved"
```

Read together: `billing-api` publishes `IF-001` (with a contract test on the
schema); `reporting-etl` consumes the same contract as `IF-002`, pins `v1`, and
tests against a recorded fixture. Grep `IF-001` across both repos to see the full
link. If `billing-api` needs a breaking change it bumps to `v2`, notifies
`reporting-etl`, and both rows move to the new version deliberately — never by
accident.
