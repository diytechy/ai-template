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
`SN→SR→LLR→TC` spine. The registry is `requirements/interfaces.csv`; this page
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
| `Contract` | One testable line naming the surface (REST route, CLI, file schema, event, library symbol) + a link to its spec. |
| `SR-Refs` | The system requirement(s) here that realize or rely on it — ties the interface into the local spine. |
| `Version` | Contract version the other side codes against (e.g. `v1`, a semver, a schema hash). |
| `Stability` | `Experimental` · `Stable` · `Deprecated`. Sets the change-notice bar. |
| `Status` | Open vocabulary (`Draft` \| `Proposed` \| `Active` \| `Stable` \| `Deprecated`): a seam a spec-of-record cites before a second consumer pins it is `Proposed` — cheap to revise. |
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
- **Both sides reference the same `IF-ID`.** Use identical ids across repos so a
  human or agent can grep one string and find both ends. Record the counterpart
  repo + the matching id so the trail is two-way.
- **Stability gates change.** Changing a `Stable` contract requires a notice to
  the counterpart and a version bump; `Experimental` may change freely. Note
  breaking changes in the audit log and bump `Version`.
- **Direction drives ownership.** Only the `Provides` side may close G-Final on
  the contract's correctness; the `Consumes` side verifies against the pinned
  version.

## Worked snippet

```csv
IF-ID,Direction,ThisProject,Counterpart,Contract,SR-Refs,Version,Stability,Status,Component,Notes
IF-001,Provides,billing-api,reporting-etl,"GET /v1/invoices returns the documented JSON schema (see docs/openapi.yaml#/Invoice).",SR-014,v1,Stable,Active,,
IF-002,Consumes,reporting-etl,billing-api,"Reads GET /v1/invoices; depends on IF-001 v1 schema (pinned fixture in tests/fixtures/invoice_v1.json).",SR-031,v1,Stable,Active,,
```

Read together: `billing-api` publishes `IF-001` (with a contract test on the
schema); `reporting-etl` consumes the same contract as `IF-002`, pins `v1`, and
tests against a recorded fixture. Grep `IF-001` across both repos to see the full
link. If `billing-api` needs a breaking change it bumps to `v2`, notifies
`reporting-etl`, and both rows move to the new version deliberately — never by
accident.
