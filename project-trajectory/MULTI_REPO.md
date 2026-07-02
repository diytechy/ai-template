# Multi-repo coordinator model (design)

> **Status: design — mechanism deferred.** This document records the *model* for
> extending the single-repo spine across separate repositories under a
> **coordinator**. The confirmed decisions below are stable enough to build a real
> two-repo project by hand and to ship the thin schema seams described in
> "Schema seams" (an optional `modules.csv`, a `Delegated` SR marker, a module-SN
> `ParentRef`, and the `IF-###` catalog-reference convention). The heavier
> automation — a cross-repo trace join, coordinator gate aggregation, repo-creation
> scaffolding, artifact transport — is **not built**; it is routed to the
> cross-repo-tooling research track (see "Deferred mechanism" at the end).
> This is a stack-agnostic **design**, the same way `PROCESS.md` is: it names roles,
> registries, and conventions, not a build engine.

---

## 1. You almost certainly don't need this

Multi-repo is for **extreme-scope** products only, and it should be **rare**. Scale
is an **escalation ladder** (`PROCESS.md` §10); the default is the lowest rung, and a
reviewer should push back on a premature jump:

1. **One module, one repo** — the default for almost every project. The whole
   `SN→SR→LLR→TC` spine, one gate run, one release.
2. **Several modules, one repo** (`PROCESS.md` §10) — when a repo grows distinct
   sub-systems that still **build and release as one**. Partition the spine by the
   `Module`/`Area` columns; no new machinery.
3. **Several repos + a coordinator** (this document) — **only** when modules genuinely
   need *independent* versioning, ownership, access, or release cadence at a scale one
   repo can't sustain.

**Decide the rung at project creation** (KICKOFF / `bootstrap` / G1) and **bias low.**
A project starts single-repo unless its scope *demonstrably* demands more. The choice
is **revisitable**: start single and **promote a module to its own repo later**, once
it proves it needs the independence — far cheaper than a speculative split. If you are
reaching for multi-repo to get *one central build that assembles everything*, that is
the signal you want a **monorepo** (rung 2: one build, one `trace.py`), not this.

## 2. Coordination, not orchestration

"Orchestration" means two different things. The kit's no-build-system guardrail
(`PROCESS.md` §8) rejects one; the coordinator lives in the other.

- **Build/runtime orchestration (rejected).** A *running engine* that checks out N
  repos, builds them in dependency order, links artifacts, and runs/deploys the whole.
  Infrastructure the kit deliberately refuses to impose.
- **Requirement / interface / status coordination (all the coordinator is).** A
  *discipline over text*: trace requirements across the boundary, keep interface
  contracts consistent and versioned, and aggregate each module's **self-reported**
  gate status. Links, registries, PRs — no engine.

Each module **builds and gates itself** in its own repo (its own `check.py`). The
coordinator **reads** those results and **sequences / triggers** downstream repos; it
does not build or run anything. Actually *running* the assembled product needs a run
step, but that is **product-layer** (the project's CI / Make / compose — the §7
process-vs-product split at larger scale): the coordinator **invokes and aggregates**
it; the kit ships none of it.

**The absence of a central build engine is the defining property of choosing
multi-repo, not a compromise.** If you want heavy central orchestration, use a
monorepo.

## 3. The confirmed model

Six decisions, confirmed with the product owner. Each extends a seam the kit already
has (`IF-###`, the Integration/Coordination hat, `PB-###`, the recursive spine) across
a repo boundary — they are not new machinery.

### 3.1 Recursive handoff at the SR tier

A repo boundary is a **cut in the decomposition tree**. The coordinator decomposes
`SN→SR` as usual; an SR it chooses to **delegate** to a module repo is tagged
delegated and becomes that module repo's **top-tier `SN`** — its reason to exist. The
module's `SN` **back-links** the coordinator's `SR` id (`ParentRef`).

The cut is at the **SR tier, not LLR.** LLR is code-local (a symbol in a module); the
delegated unit is a **sub-system**, which is SR-shaped — a capability with its own
needs, requirements, code, and tests. So "delegate this SR" reads as "this whole SR is
another repo's job," and that repo re-enters the spine at its own G1 with the delegated
SR as its founding need.

### 3.2 Coordinator = the Integration/Coordination hat, elevated to a repo

The coordinator is the §1 **Integration/Coordination** hat given its own repository. It
holds:

- the **product-level `SN→SR→TC` chain** (the composition-scoped requirements — §4);
- an **assembly definition** (§3.4);
- an **interface catalog** (§3.3).

It contains **no functional build output** except the assembly definition. Note the
chain is `SN→SR→TC`, usually skipping LLR: the coordinator has no functional code of
its own, so its SRs are either **delegated** (§3.1, verified in a module repo) or
**composition-scoped** (§4, verified by the integration/plant repo). Neither
decomposes into a *coordinator-local* LLR.

### 3.3 Interface catalog = pointers, not copies

Every interface's spec lives **once, in its owner** (single source of truth, the §8
ICD model):

- for a surface some repo **builds**, that repo's `IF-###` is the authoritative spec;
- for a **purchased / external / reused** part that *no repo builds*, a
  **coordinator-held `IF-###`** row *is* the owner of record — it links the datasheet /
  part / vendor contract. Acquisition state for such a part (vendor, cost, order
  status, quantity) lives in the optional `procurement.csv` (`PART-###`) registry,
  each row's `IF-Ref` back-linking this owner `IF-###` (process-options.md
  "purchased parts"). It is minimal by design — a flat parts list, not a bill of
  materials; full BOM tracking is a deferred extension.

The coordinator's **catalog references** those owner `IF-###` ids and adds only
assembly-level **connection** information (which module's provided surface wires to
which consumer, at which pinned version). It never copies a spec. Interface
proliferation is expected (the "there are 16 competing standards" reality) and managed
by **owner-of-record**, not central control.

**Local id spaces + a coordinator-level handle (no cross-repo id collisions).** Each
repo owns its **own** `IF-###` space, so `IF-001` in two different module repos are
*different* interfaces that merely share a string — they would collide the moment the
coordinator referenced both. The catalog therefore keys each shared interface by a
**coordinator-level id (`CIF-###`)** that maps to the qualified owner tuple *(owner
module/repo, owner `IF-###`, owner version)* plus each consumer's **pinned** version.
Local ids never need to be globally unique; the `CIF-###` is the one stable, global
handle. Because it is stable while its *binding* can change, it composes with
assemblies-as-config (§3.4): assembly `edge` may bind `CIF-005` → `sensor-a:IF-003@v2`
and assembly `cloud` → `sensor-b:IF-007@v1` without renaming anything. (The catalog
registry and the check in §3.7 are deferred mechanism — §6/§7.)

### 3.4 Assemblies = configuration, not branches

A product **variant** is a configuration — `assemblies/<name>/` naming the module set,
the pinned versions, and which `SN`/`SR`/`TC` apply — **not** a long-lived coordinator
branch. Branches model *change over time*: they diverge and cannot be co-current, so
two variants that must both ship become a merge problem. Configurations are
co-current by construction: `assemblies/edge/` and `assemblies/cloud/` sit side by
side, each pinning its own module versions.

### 3.5 Coordinator gating = mechanical aggregation, judgment escalated

The coordinator (as agent) runs the **mechanical** cross-module gate — every module
passed its own gates, integration/plant tests are green, the interface catalog is
consistent — and surfaces only the **judgment** gates to the human. The human signs
the **integration** gate; module agents (and their humans) gate the modules. This is
the §6 review-depth triage at the coordinator level; it **does not remove the human**,
it routes the mechanical part away from them.

### 3.6 Cross-repo communication = async text + PR

A delegated SR **seeds** the module repo's `SN` registry; module status flows back as
**referenced ids** in a coordinator assembly/status doc (the `status.md` pattern across
the boundary). No live message bus, no daemon — the same async-text-and-PR discipline
the kit uses everywhere, applied across the repo boundary.

### 3.7 Interface compatibility across the boundary (version reconciliation)

A repo boundary breaks the single-repo safety net. In one repo a shared contract is
kept honest by its **fixture/contract test at the seam** (§8), re-run whenever either
side changes. Across repos, the owner can change an interface's *content* and ship a
new version while a **consumer in another repo stays pinned to the old one and builds
green in ignorance** — the drift the coordinator exists to catch. Split the job the
same way §3.5 splits gating:

- **The coordinator reconciles *versions* (mechanical).** The catalog records, per
  `CIF-###`, the owner's **current published version** and each consumer's **pinned**
  version. A consumer pinned below the owner's current version — the owner (parent)
  moved and the dependent didn't — is a **compatibility finding**, weighted by the §8
  `Stability` tier (an `Experimental` change is expected; a `Stable` one past a pin is
  a blocker). This is comparing versions the repos publish as text: no build engine.
- **The interface's own contract test verifies *compatibility* (already exists).**
  Whether the new version is actually compatible is answered by the dependent repo
  running the **owner's published contract/fixture** against it — the §8 test that
  backs every interface. The coordinator doesn't judge semantics; on a divergence it
  **sequences** the dependent's re-verification (async text + PR: open a
  bump-and-re-run in the dependent repo, §3.6) and escalates a genuine break to the
  human.

So "the parent changed — can every dependent adjust?" becomes a pipeline:
*coordinator detects the version divergence → triggers each dependent's contract test
against the new version → human signs any real break.* Same three layers as §3.5
(mechanical aggregation · existing test · human judgment). The reconciliation tool is
deferred (§7); the **design decision that makes it buildable** is §3.3's
coordinator-level id carrying the owner + consumer versions.

## 4. Two requirement scopes — name them

A multi-repo product has requirements at **two levels**, and conflating them is the
trap:

- **Module-scoped** — a module's own `SN→SR→LLR→TC`, verified **inside the module
  repo**, scoped to what that module does in isolation.
- **Composition-scoped (emergent / integration)** — requirements that exist **only for
  the assembled whole** and that *no single module owns*: end-to-end behavior across
  A→B→C, closed-loop stability of a controller against its plant, cross-module latency
  / throughput, disturbance rejection. These live in the **coordinator's** `SN→SR`
  chain and are **verified by the integration/plant repo's TCs** (typically
  `Verification=Demonstration` — run the sim), *not* by any module.

The handoff **generalizes the §3.1 SR-tier rule**: a composition SR delegates to the
**plant repo's `SN`** ("verify the composed product satisfies this"), exactly as a
functional SR delegates to a functional module's `SN`. The plant repo is simply "the
module whose deliverable is a runnable verification of the assembly."

## 5. The integration / "plant" environment is a delegated repo

A runtime test / simulation environment — assemble the modules' built runnables plus a
**plant model that virtualizes their external inputs**, then execute the assembly
(SIL / HIL / E2E) — is a **first-class module the coordinator delegates to**, exactly
like a functional module. It has its own `SN` (delegated from a coordinator SR),
consumes the other modules' published artifacts, and **gates itself**. So "all deps
green → queue the plant repo to assemble and run" is still *sequencing + triggering*
(read status, dispatch CI or open a PR, pass the version pins) — never the coordinator
building or running anything.

*"Plant"* is the control-systems term (the virtualized physical system under control);
generalize it to **any** environment that mocks the composition's external inputs — a
test rig, a mock-service harness, a scenario generator. The **artifact transport**
between repos (a package registry, an OCI image, a CI artifact) is **product-layer** —
the project's choice — and is deferred (see below).

## 6. Schema seams (the thin part that ships)

These are optional and schema-safe, the same way `Area`/`Lifecycle` (`PROCESS.md`
§1/§4) and `PB-###` (§9) are — they change no required field, and a single-repo
project never sees them. A coordinator repo adds them by hand (or via the future coordinator
`bootstrap` variant — deferred).

- **Coordinator `modules.csv` (`MOD-###`).** The coordinator's module registry:
  `MOD-ID, Module, Repo, DelegatedSRs, Version, Type (owned | external | reused),
  Owner, Notes`. `DelegatedSRs` back-links the coordinator `SR` ids delegated to that
  module (§3.1). `trace.py` keeps it honest **within the coordinator repo**: a
  malformed/duplicate `MOD-` id fails, and a `DelegatedSRs` value that names an SR the
  coordinator doesn't have fails — the `PB-###` back-link precedent (§9), applied to
  delegation. An `external`/`reused` part referenced only through the interface catalog
  may leave `DelegatedSRs` blank (unlike `PB`, an empty back-link is allowed here,
  because such a part fulfills no delegated *functional* SR). Optional and inert like
  `interfaces.csv`: absent file, no effect.
- **`Delegated` marker on a coordinator `SR`.** An optional column recording that an SR
  is delegated to a module repo (value: the `MOD-` id or module name). It signals, when
  reading the coordinator's SR registry, that this SR's decomposition and verification
  live **across the boundary** — not as a missing local LLR.
- **`ParentRef` on a module repo's `SN`.** An optional column (or inline annotation) on
  the delegated module's top `SN` naming the coordinator `SR` it descends from (§3.1).
  This link points **across the boundary**, so no single `trace.py` run can validate it
  — that reconciliation is the deferred cross-repo join. It is recorded now so the
  future aggregator has the edge to follow.
- **Interface catalog convention (`CIF-###` → owner tuple).** The coordinator keys each
  shared interface by a coordinator-level id mapping to *(owner repo, owner `IF-###`,
  version)* + each consumer's pinned version (§3.3), so per-repo `IF-###` spaces never
  collide. **The catalog registry itself and its §3.7 version-reconciliation check are
  deferred** (§7): unlike `modules.csv`, they need cross-repo mechanism to be useful, so
  only the *convention* (local ids + a coordinator handle) is fixed here.

**Honest limit — the coordinator repo's own gate.** Because a delegated SR's LLR and
tests live in another repo, that SR has **no local LLR or TC**, so a plain `trace.py
--strict` in the coordinator repo will report it as an orphan. The `Delegated` marker
records *why*, but reconciling it — closing the coordinator SR against the module's
returned status — is the **cross-repo trace join**, which one `trace.py` run cannot do.
The kit does **not** fake this: it ships the seams (so the edge is recorded) and defers
the join. Until then, a coordinator repo tracks delegated-SR closure by reading module
status by hand, exactly as §3.6 describes.

## 7. Deferred mechanism (the cross-repo tooling track)

Everything below is genuinely research-grade and **not built** here. Each is its own
future decision; the model above is what they will operationalize.

- **Cross-repo trace join** — reconciling `SN→SR→LLR→TC` across repos (coordinator SR
  ↔ module SN, and composition SR ↔ plant-repo TC). Almost certainly a coordinator-side
  **aggregation** that reads each module's *exported* trace summary, **not** one
  `trace.py` over many checkouts. Open: **pull** (the coordinator clones/reads) vs.
  **push** (modules publish a trace artifact it ingests).
- **Coordinator gate aggregation** — the mechanical "all modules green + integration
  green + catalog consistent" check (§3.5) as an actual stdlib command reading
  module-published gate/status artifacts, with escalation rules for the judgment gates.
- **Interface catalog + compatibility reconciliation** — the `CIF-###` catalog registry
  (§3.3) and the §3.7 version-reconciliation check: flag a consumer pinned below the
  owner's current version (weighted by `Stability`), and sequence the dependent repo's
  contract-test re-run when the parent interface changes. Reads published versions
  across repos; never builds. Same **pull-vs-push** question as the trace join.
- **Repo creation** — scaffolding a coordinator + N module repos (a `bootstrap
  --coordinator` mode, `gh repo create`): agent/host tooling, optional and
  agent-neutral — name the pattern, don't bake the automation in.
- **Module discovery / reuse catalog** — finding an existing reusable module or part
  for a delegated SR: an agent capability over a catalog, not a kit mechanism.
- **Cross-repo E2E + artifact transport** — the plant repo (§5) that consumes the
  modules' published artifacts, assembles them, runs SIL/HIL/E2E, and gates itself;
  plus how artifacts move between repos (registry / OCI / CI artifact) and where the
  composition-scoped TCs live.

See `EXAMPLE.md` §10 for a worked two-repo sketch of the model above.
