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
a test — **plus** a version and a stability promise the other side can rely on.
Putting these in one place stops the classic failure of interlinked projects:
each side assumes a slightly different contract and they rot apart silently.

## ID scheme & columns

`IF-###` — Cross-Project Interface. Zero-padded, stable, never reused (its own
namespace, parallel to SN/SR/LLR/TC).

| Column | Meaning |
|---|---|
| `IF-ID` | Stable id for this interface. |
| `Direction` | `Provides` (we expose it) or `Consumes` (we depend on it). |
| `ThisProject` | This repo/project name (or, intra-repo, the module on this side of the seam). |
| `Counterpart` | The other project/repo — or, intra-repo, another module, a file path, or an external actor — on the far side of the contract. |
| `Contract` | One testable line naming the surface (REST route, CLI, file schema, event, library symbol) + a link to its spec. **What crosses, typed — nothing else** (process.md §8): no rationale, no work-item id, no decision citation, ≤500 characters. |
| `Signal` | **Closed**: `discrete` (a finite enumerable alphabet — exit code, gate name, status enum, dial) or `variable` (unbounded content — prose, file bytes, a count, a duration). If both cross, the row is `variable`. |
| `SignalNote` | Optional. Why the typing is not obvious — a crossing that carries both kinds, or one the `Contract` does not type. |
| `Rationale` | **Why the seam is drawn here.** Empty is allowed; this is the home the `Contract` cell's argument moves to. |
| `SR-Refs` | The system requirement(s) here that realize or rely on it — ties the interface into the local spine. |
| `Version` | Contract version the other side codes against (e.g. `v1`, a semver, a schema hash). |
| `Stability` | **Closed**, and the row's **one** maturity field: `Experimental` · `Stable` · `Deprecated`. Sets the change-notice bar. A seam a spec-of-record cites before a second consumer pins it is `Experimental` — cheap to revise. (An undeclared `Status` column shipped here until OI-14 part B retired it, 2026-08-13: it overlapped this one, and `Stable` appeared in both meaning different things.) |
| `Component` | Optional `CMP-###` membership tag for the component layer; empty when unused. |
| `Notes` | Free-form. The `source`/`sink` honesty valve lives here (silences the missing-direction coverage warn for `ThisProject` — see the registry's `-000` row). |

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
  written in `Counterpart` and `Contract`/`Notes`, **never in the `IF-ID`
  column** (`trace.py`'s `^IF-\d+$` integrity pattern rejects any qualified
  form there). Under a coordinator repo, the one stable global handle is the
  coordinator-level `CIF-###` (MULTI_REPO.md §3.3). Honesty note: no tool
  validates the far side of a cross-repo reference — it is a text convention;
  keep the trail two-way by recording the counterpart repo + matching id on
  both rows.
- **Stability gates change.** Changing a `Stable` contract requires a notice to
  the counterpart and a version bump; `Experimental` may change freely. Note
  breaking changes in the audit log and bump `Version`.
- **Direction drives ownership.** Only the `Provides` side may close the owner's final read on
  the contract's correctness; the `Consumes` side verifies against the pinned
  version.

## Worked snippet

```toml
[interface.IF-001]
direction = "Provides"
this_project = "billing-api"
counterpart = "reporting-etl"
contract = "GET /v1/invoices returns the documented JSON schema (see docs/openapi.yaml#/Invoice)."
signal = "variable"
rationale = "One read model for invoices; the ETL must not re-derive totals."
sr_refs = ["SR-014"]
version = "v1"
stability = "Stable"

[interface.IF-002]
direction = "Consumes"
this_project = "reporting-etl"
counterpart = "billing-api"
contract = "Reads GET /v1/invoices; depends on IF-001 v1 schema (pinned fixture in tests/fixtures/invoice_v1.json)."
signal = "variable"
sr_refs = ["SR-031"]
version = "v1"
stability = "Stable"
```

Read together: `billing-api` publishes `IF-001` (with a contract test on the
schema); `reporting-etl` consumes the same contract as `IF-002`, pins `v1`, and
tests against a recorded fixture. Grep `IF-001` across both repos to see the full
link. If `billing-api` needs a breaking change it bumps to `v2`, notifies
`reporting-etl`, and both rows move to the new version deliberately — never by
accident.
