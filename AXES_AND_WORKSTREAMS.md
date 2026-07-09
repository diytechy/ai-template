# Axes & Workstreams — how to organize *what* / *why* / *how* / *when* without duplication

**Author:** Claude (Opus 4.8), design note from a working session ·
**Date:** 2026-07-08 (last updated 2026-07-09) · **Branch:** `MultiRepoSupport` (not pushed) ·
**Status:** **OPEN — a ruling-in-progress (iteration 7). Expect more passes before
implementation.** Nothing here is built; no registry or script has been touched.

## Provenance

This came out of reviewing the recent **"how"-emphasis** work — the trajectory /
work-items layer (Thread 52) — and the risks [`THREAD_52_REVIEW.md`](THREAD_52_REVIEW.md)
flagged. The owner's concern was that emphasising the *how* (mainly "tracks") may
be conflating **how** with **when**, and that there is no durable home for a
decomposition, so future iteration relearns what an older effort already worked out.

This is a **triage / design input, not a plan** (the same posture as the review).
It **folds in `THREAD_52_REVIEW.md` F3** (the work-items schema question) and
**touches F1** (tracing the layer's own code). It exists so the next session
inherits the framing instead of re-deriving it.

## Iterations (read this first)

- **Iteration 1** (commit `be2cd00`) — framed **four** axes: WHAT / HOW-physical /
  HOW-functional / WHEN. Named the "track" overload; proposed renaming the
  work-item `Track` → `Workstream`.
- **Iteration 2** (this revision) — the owner collapsed the two "HOW" axes. The key
  realisation: **the functional decomposition already lives in `SR → LLR`**, so
  there is no separate functional-decomposition axis to build. That leaves **one**
  decomposition axis — **Modules** (physical *or* software, one unit type) — joined
  to the spine by `LLR.Module`. The **module becomes the centre of gravity**:
  expectations, interfaces, category, knowledge, and lifecycle all attach to it;
  the workstream stays thin. "Knowledge packs" turn out to be ~80% the existing
  **skills layer**. Mating two modules is reframed as **work that consumes parts**
  (a BOM/BOP gap). Still OPEN.
- **Iteration 3** (this revision) — settled the **module-content format** (§3): a
  light **CSV row is primary** (the traceable graph), with an **optional
  markdown-frontmatter detail doc** for the heavy ones (`DetailDoc` empty ⇒ light
  module, no file). **Not ini** — ini is for config (`stack.ini`); md-frontmatter is
  the kit's existing heavy-per-entity format (skills). Polarity rule: machine truth
  in the row, prose in the doc, never both. And showed **geometry fits with no new
  axis** (§3a): the artifact → `ASSET-###`, the mating constraint → `IF-###`, the
  narrative → the detail doc. Still OPEN.
- **Iteration 4** (this revision) — three more boundaries. **(a)** An *assembly* is a
  **relationship graph**, not a fatter asset (§7): `ASSET` stays a flat artifact
  manifest; composition + connection **edges** carry the tree (the physical sibling of
  module composition + interfaces). **(b)** Software modules stay in sync by being
  **checked against source** — code-facing fields are references a freshness check
  validates (the `gen_arch_map.py` idiom; F1 / Thread 49), so module↔asset is partly
  the **mechanically-verifiable vs only-attestable** split (§3c). **(c)** The big one:
  parametric models, workstreams, and physical assemblies are the **same typed
  relationship graph** — **share the structure** (one edge vocabulary + a stdlib
  graph/traversal/render core) but **route out the resolvers** (kinematics /
  mass-properties / geometry are external, not the kit's job). See "Cross-cutting"
  after §8. Still OPEN.
- **Iteration 5** (this revision) — situating tweaks; mostly de-dup + placement.
  **(a)** The DAG is the **prospective roadmap**; "where we were" is derivable from
  **git**, so done work leaves the living DAG (§5a) — also F3's fix. **(b)** Refined
  the shared-graph claim: **not every graph is a DAG** — a **4-bar linkage** is a
  *cyclic* connection loop; `depends-on`/`contains` are acyclic, `connects-to` is
  general (Cross-cutting). **(c)** Knowledge packs gain a **derived** half (computed
  from a part's material / mates-to / forces) alongside the authored half (§4).
  **(d)** Physical containers are **domain-neutral** (hydraulic / electrical / aero …)
  — typed ports + open properties, resolvers stay routed (Cross-cutting). **(e)** New
  artifact spec: **`PROJECT_STATE.html`** at root — 4 views unifying `gen_trajectory` +
  `gen_arch_map`, with a **git-derived** "as-of" date (a wall-clock date would break
  the deterministic freshness gate). **(f)** New **dynamic-layer** section: the
  coordinator / planner / implementer / reviewer pipeline, mapped to `agent_loop.py` +
  the integrator role, with the coordinator split along the **loop-vs-judgment** seam.
  Still OPEN.
- **Iteration 6** (this revision) — rulings + a refactor. **Naming:** software unit =
  **`swBlock`** (not Module/Processor); physical = **part/assembly**; **`MOD-### →
  REPO-###`** (§9). **Direction flip:** the swBlock **owns `Realises`** (many LLRs;
  instancing deferred) — `LLR.Module` was too narrow (§2). **Workstream ≠ SN** — a
  mutable grouping *category* on swBlocks + assemblies (Q2 resolved, §5). **WI** names
  the swBlock(s)/part(s) it **affects + the gap** (§5). **Hard vs soft predecessors**
  expanded (§5b). **Design-order DAG** is the kit's scope — *parented by the interface
  owner*, derivable from `IF.Direction`, with the kit's-own-scripts example; physical
  assembly time/material/energy/sim is **solution-space** (§7a). **Knowledge packs** →
  `docs/knowledge/<label>.md` (§4). **`PROJECT_STATE.html`** as-of line visible on open.
  **Refactor:** the coordinator/roles dynamic layer **split out** to
  [`AGENT_ROLES.md`](AGENT_ROLES.md). Still OPEN.
- **Iteration 7** (this revision) — cleanup + refinements. **Renamed** "module" →
  **`swBlock`** / part / component throughout the body (the deferred iter-6 follow-up;
  the historical changelog is left as-is). **`LLR.Module` dropped entirely** — the
  swBlock↔LLR link is now **many-to-many both ways** (a swBlock realises ≥1 LLR; an LLR
  may be realised by several swBlocks), carried solely by `swBlock.Realises` (§2).
  **Knowledge** refs now sit on **swBlocks, parts, *and* assets**, one or many, M:N (§3b,
  §4). Q1's "retire/derive `LLR.Module`" is resolved (dropped); Q13 rename done. Still
  OPEN.
- **Iteration 8 — IN PROGRESS** (owner still thinking). Owner floated **trashing
  SWB/HWB** and deriving everything from **IF + ASSET + PART**; the counter is that
  **knowledge-for-*sets*** has no home there → a component survives, **slimmed to a
  domain-neutral `CMP-###`** (`id, Name, Category, Knowledge, State` + a `Component` tag
  on the primitives), structure **derived** from IF+ASSET+PART, SWB/HWB split retired.
  Owner **leans this way**. Also: **knowledge is layered by grain** (type→ASSET/PART,
  boundary→IF, impl→LLR, **set→CMP**); **mass/inertia/material are extractable from
  many CAD formats** via a **routed** tool (kit records, never parses CAD); **diagnosis
  walks IF → affected LLRs/assemblies → root**. See the "Iteration 8" section. OPEN —
  §3/§9's SWB/HWB split is under reconsideration.

> How to read: §1 the conflation (unchanged, still true). §2 the three-axis reframe
> + the `swBlock↔LLR` link. §3 the swBlock as centre of gravity (+ §3a content format,
> §3b geometry, §3c keeping swBlocks in sync). §4 knowledge packs ≈ skills
> (+ the derived half). §5 where work-definition lives (+ §5a temporal scope: roadmap
> is prospective, past = git). §6 larger change → swBlock lifecycle. §7 mating =
> contract + consuming work (+ assembly = a graph, not a fatter asset). §8 concrete
> tech (Elysia) + software tooling. **Cross-cutting** (after §8): the shared structure
> — one edge vocabulary, routed resolvers (+ not-every-graph-is-a-DAG, the 4-bar;
> domain-neutral containers). **The artifact** (`PROJECT_STATE.html`); the dynamic layer
> (coordinator/roles) is now the sibling [`AGENT_ROLES.md`](AGENT_ROLES.md). §9 naming
> (swBlock / part; MOD→REPO). §10 cautions. §11 decision. §12 open questions. *(iter 7:
> "module"→swBlock rename applied; `LLR.Module` dropped; §5b hard-vs-soft predecessors.)*

---

## 1. The conflation: "track" names two unrelated things

The word **track** means two things that have nothing to do with each other:

**(a) An execution lane.** In [`tracks-README.template.md`](project-trajectory/tracks-README.template.md)
and the "Parallel tracks" layer of [`PROCESS_OPTIONS.md`](project-trajectory/PROCESS_OPTIONS.md),
a track is a *worktree + `llm/<track>` branch + `docs/tracks/<track>/` lane* — a
**when / who-runs-it-in-parallel** concurrency device. Transient, chosen by
invocation, never committed.

**(b) A grouping label on a work item.** In
[`docs/requirements/work-items.csv`](docs/requirements/work-items.csv) the `Track`
column holds `docs` / `scripts` / `unattended` / `self-adoption`, and
[`gen_trajectory.py`](project-trajectory/scripts/gen_trajectory.py) uses it *only*
as a DAG cluster-order seed + display label + a count tile. It carries no
dependency semantics and no worktree reality.

So the `work-items.csv` "Track" **is not a track** — it is a grouping, and (per §2)
that grouping is best expressed as *which swBlock the work advances*. Reusing the
execution-lane word for it is the root cause of the how/when conflation.

---

## 2. The reframe: three axes, joined by the swBlock↔LLR link

The owner's *what / how / when* frame is right once you see that **"how" was hiding
two things, and one of them was already built.** `SR → LLR` **is** the functional
decomposition — each SR/LLR is a function the system must perform. So there is no
functional-decomposition axis to add; it is the WHAT. That leaves the **swBlock** (and
its physical sibling, the **part / assembly**) as the *implementation* decomposition,
linked to the spine by **`swBlock.Realises`** — the swBlock names the LLRs it satisfies.

| Axis | Home | Nature |
|---|---|---|
| **WHAT** — incl. the functional decomposition | `SN → SR → LLR → TC` | durable truth |
| **WHY** | README `PROJECT-VISION` (top) → SR rationale (mid) → LLR/impl intent (implicit) | durable, **distributed**, reference-not-restate |
| **HOW** — implementation decomposition | **swBlock** (software) / **part / assembly** (physical) — a new component registry (§3) | durable |
| **WHEN** | **Workstream** (a grouping category) + **Session**; plus the parallel-execution *tracks* | mutable / transient |

"Electrical power vs mechanical engineering," "software vs hardware" — these are
**not** a third decomposition tree. They are a **category + knowledge lens** over
swBlocks / parts (§3–4). Folding functional into WHAT is what keeps the model from
growing a redundant fourth hierarchy.

**Naming (§9).** The software decomposition unit is a **`swBlock`** — not "module"
(`MOD-###` already means a delegated repo), not "Processor" (reads as a CPU). The
physical unit is a **part / assembly**; "component" is the generic word for either.

**The swBlock↔LLR link is many-to-many, and `LLR.Module` is dropped.** An **LLR** is "a
decomposed need — an outcome fed elsewhere." A swBlock **realises ≥1** LLR, and an LLR
may be realised by **several** swBlocks (it depends on the functionality). A single
`LLR.Module` string can express neither direction, so it is **dropped entirely**; the
authoritative link is **`swBlock.Realises`** (a *list* of LLR ids). (A swBlock may also
be **instanced** — one *type*, many instances; the swBlock is the type, instances are
refs; deferred until a real case appears.)

**The unit has no registry yet** — it existed only as that free-text `LLR.Module` string
(now retired), and the existing
[`modules.csv` (`MOD-###`)](project-trajectory/registries/modules.template.csv) is a
*different* thing (a delegated **repo**, to be renamed `REPO-###`, §9). So the step is a
**new sibling** component registry (the Q12.1 lean), not a widened `MOD-###`.

The SSOT rule that ties all of this together **without duplication**: *each fact has
exactly one home; everything else references it by id; the dashboard is a generated
**view** that joins them* — the `trace.py` / "a view, never a source of truth" idiom. A
swBlock references its SR/LLR/TC (never restates them); a workstream is just a grouping
category over swBlocks / parts (never restates their definition).

---

## 3. The swBlock is the centre of gravity

*Naming: the unit is a `swBlock` (software) or a part/assembly (physical); "component"
is the generic term — see §2, §9. "swBlock" below stands in for either where the point
is general.*

*⚠ **Under reconsideration (iter 8):** the SWB/HWB split likely collapses to one
domain-neutral `CMP-###`, with structure derived from IF+ASSET+PART and the component
existing only as the knowledge-set + lifecycle home. See "Iteration 8".*

Put the durable material on the durable noun. A swBlock/part row carries:

- **Expectations / definition** — what it must satisfy, expressed as **references** to
  the `SR / LLR / TC` it realises via `Realises` (never restated). This is also where the
  swBlock says *how it breaks down*, so a workstream can just say "work on M."
- **Interfaces** — the `IF-###` seams by which it mates with other swBlocks / parts (§7).
- **Category** — a tag/lens (`software` │ `physical` │ …). Just a tag, **no registry**;
  it points at the relevant knowledge (§4).
- **Knowledge** — one or more `docs/knowledge/<label>` refs + skills (§4).
- **State / lifecycle** — `planned │ built │ verified │ has-gap │ deprecated │
  superseded-by:<id>` (§6).

**Keep components flat + composable, not rigidly levelled.** The owner is right that
"component → sub-component → …" gets arbitrary. Model composition with a
`Contains` / `PartOf` link and let a component slot in anywhere, rather than mandating
hierarchy depth. (This matches the existing `MOD-###` flatness.)

*Issues update the swBlock's definition; new learning updates its knowledge; everything
stays central to the swBlock when work is performed on it.* That centrality is the whole
point.

### 3a. swBlock content: a light row + an *optional* detail doc (not ini)

A swBlock is *both* a row and a document, and the light/heavy tension is the signal not
to force it to be one or the other:

- **The CSV row is primary** — the light, machine-joinable, traceable fields (id, name,
  category, state, `Realises` (LLR refs — a *list*), `Interfaces` (IF refs), `Assets`
  (ASSET refs), `Knowledge` (labels), `PartOf`, `DetailDoc`, `Notes`). `Realises`
  resolves to real LLRs here, and `trace.py` validates it cheaply, stdlib.
- **An optional detail doc holds the heavy prose** — `docs/swblocks/<id>.md` (a physical
  part gets its own dir), markdown-with-frontmatter (the **skills** format). Linked by
  the row's `DetailDoc` cell. **A light swBlock is just a row (`DetailDoc` empty); a
  heavy one adds the doc.** You never pay for a file a light swBlock doesn't need.

**Not ini.** ini is a *config* format (flat `key=value`) — right for `stack.ini`, wrong
for prose/lists/rationale. md-frontmatter is the kit's existing heavy-per-entity format;
reuse it rather than invent a fourth pattern. **Polarity rule (kills the "where do I
look?" confusion):** machine truth in the row, human prose in the doc, never the same
fact in both; the generated dashboard splices them into one panel at read time.

Do **not** flip to file-primary-with-generated-index (the skills polarity, `SKILL.md` +
`gen_skills_index.py`): that reintroduces a whole file *per light swBlock*, the exact tax
being avoided. Row-primary is the answer to the light/heavy tension. Also note most
swBlocks need **no** doc — reusable knowledge is a *skill* (already a file), so the
swBlock often just lists `Knowledge` refs; the doc is only for content *specific* to it.

```
# component registry — a swBlock (software) row; light: no DetailDoc
SWB-007, HTTP boundary, software, verified, LLR-014;LLR-021, IF-003, , skill-elysia, SWB-002, ,
# heavy swBlock: same shape, DetailDoc -> docs/swblocks/SWB-012.md
# physical parts share the registry (Category=physical); the id scheme (SWB- / PRT-) is Q13
```

### 3b. Where geometry lives (no new axis)

"Geometry" is three different things, each already homed:

- **The artifact** (STEP/native model, dimensioned drawing) → an **`ASSET-###`** row
  ([assets.csv](project-trajectory/registries/assets.template.csv)): the blob lives
  in git-LFS / a PLM store (`Location`), pinned by `Hash`+`Version` so it is
  verifiable though un-diffable — the *"track about the asset in text"* doctrine.
  Kind = `cad`/`drawing`/`model`; `Refs` back-links the LLR it realises.
- **The mating constraint** (bolt pattern, datum faces, fit/clearance) → an
  **`IF-###`** Contract ([interfaces.csv](project-trajectory/registries/interfaces.template.csv)):
  the seam "in one testable line," linking the drawing. Verified by a TC with
  `Method = Inspection`/`Demonstration` (CMM report, fit check).
- **The narrative** (GD&T rationale, assembly notes, revisions) → the part's **detail
  doc** (§3a), only if heavy.

The **component (part) row references the first two** (`Assets` → the CAD, `Interfaces`
→ the seam). This closes §7's assembly loop: `ASSET` (shape) + `IF` (what must line up) +
`PART` (fasteners consumed) + an assembly WI (`predecessors=[both parts],
consumes=[PART], satisfies=IF`). The light/heavy gradient holds: a stock screw is a
`PART` + datasheet (no ASSET); a bespoke part is an `ASSET` whose blob stays out-of-tree.
**SSOT nuance:** with `LLR.Module` dropped, the direct **component `Assets` cell** is the
authoritative asset↔component link and `ASSET.Refs` is the back-link. And an **ASSET row
also carries `Knowledge`** refs (one or more `docs/knowledge/` labels), exactly like a
swBlock/part — §4.

### 3c. Keeping a swBlock in sync with the code (the verifiability boundary)

The swBlock ↔ asset split is partly the split between **"mechanically verifiable against
source"** and **"only attestable."** A **physical** asset can't be diffed — you can't
mechanically verify a weld — so it is *attested / inspected* (the `ASSET` "track about it
in text" doctrine + an `Inspection`/`Attest` TC). A **swBlock** *can* be verified against
its source. So keep it current the way the kit keeps its own code map current —
**generated / checked, never hand-authored:**

- A swBlock's **code-facing fields are *references to source*** (a path, a code module,
  the symbols it comprises); a stdlib check verifies they *resolve in the actual code* —
  the `gen_arch_map.py --check` idiom. This is exactly
  [`THREAD_52_REVIEW.md`](THREAD_52_REVIEW.md) **F1** (untraced-code / symbol coverage)
  and **Thread 49** (symbol-reference validation): the swBlock-drift guard is a check the
  review already asked for, now given a home.
- Keep authored prose minimal — prose rots; the *sync-able* part is the references,
  and references get gated. Drift is prevented by *deriving / checking*, never by
  discipline.

---

## 4. "Knowledge packs" are ~80% the skills layer you already have

The kit already ships the mechanism: [`project-trajectory/skills/`](project-trajectory/skills/)
— agent-neutral `SKILL.md` files with an applicability schema, materialised
per-repo. A knowledge pack is essentially:

> **{ applicable skills } + { external resource refs } + { internal domain notes }**,
> attached to a swBlock, part, or asset.

So do **not** invent a parallel system. **Reusable** agent knowledge stays a *skill*
(`project-trajectory/skills/`); **project-specific** domain knowledge lives in
**`docs/knowledge/<label>.md`**, each file labelled by topic — the *core solution
context* for anything that relates to it. A swBlock / part **and an `ASSET`** row each
carry a `Knowledge` cell listing **one or more labels** (skill names + `docs/knowledge/`
labels + external URLs); the relationship is **many-to-many** — a component may cite
several packs, and a pack is shared by many components. No registry needed — labelled
docs referenced by label; promote to a registry only if reuse ever forces it.

**A knowledge pack has two halves — derived + authored.** The *authored* half is the
skills + refs above. The **derived** half is a *view* computed from the part's own
data + its edges — material + `connects-to` + load. *"Aluminium, bolted to steel,
500 N"* surfaces galvanic-corrosion / bolt-torque / fatigue considerations with no
hand-authoring. Being a *view* (never a source of truth), the derived half stays fresh
for free and is never restated — the same idiom as the generated dashboard.

**The loop this closes** (the owner's exact scenario — a gap found in an already-
`verified` swBlock):

1. A TC gap surfaces on swBlock M → open a **workstream** grouping targeting M.
2. M's row already carries its knowledge refs → **no rediscovery** of the base.
3. The work tightens the constraint → new/updated **LLR + TC** (the WHAT changes,
   referenced by M's `Realises`).
4. M's state flips `verified → has-gap → verified`; new learning **appends to the
   `docs/knowledge/` pack**.
5. The work item schedules the fix in the DAG; the session logs the evidence.

The knowledge survives on the durable swBlock, so iteration **rejoins** it instead of
relearning it.

---

## 5. Where the definition of work lives (swBlock vs workstream vs session)

Split by **durability** — this is the answer to "should session definition belong to
the workstream or the swBlock?":

- **swBlock / part** = durable *noun*. Owns *what it must become* (expectations →
  SR/LLR/TC, interfaces, knowledge, state). Survives across iterations.
- **Workstream** = a **mutable grouping category** (a column on swBlocks + assemblies),
  bounding deliverables that share dependencies — e.g. a *perception* workstream over
  the camera-input→depth swBlock. **Not an SN** (Q12.2 resolved); project-defined, and
  *how* it's derived is deliberately loose. It puts the roadmap into focus; it is not a
  heavyweight registry.
- **Session** = transient *verb*. Owns *evidence* — one sitting → an iteration log
  (already exists in the kit).

So neither the workstream nor the session owns the definition — **the swBlock/part
does.** Keeping the workstream a thin category is what makes re-opening cheap. A **work
item** names **what swBlock(s)/part(s) it affects and the gap it closes** (+
predecessors + status) — the *intersection* of (a workstream grouping) × (target
component) × (a DAG slot); its detail is written by the planner *into the component*,
not restated on the WI.

### 5a. Temporal scope: the roadmap is prospective; the past is git

The dependency DAG is the **living roadmap** — the *not-yet-processed* work, still
breathing and free to change. It is **not** an archive of history. **"Where we were"
is derivable from commit history**, so a node's evidence-of-completion lives in git,
not as accumulating prose in the registry. Done work therefore *leaves* the living DAG
(kept only while still a predecessor of live work); the full past can always be
reconstructed from git if wanted.

This is also the clean fix for [`THREAD_52_REVIEW.md`](THREAD_52_REVIEW.md) **F3** (the
dogfood DAG encoding narrative/ordering as fake edges): if history isn't stored in the
living DAG, there are no narrative edges to be wrong. And it feeds the artifact below —
the dashboard's *as-of* date is the latest source commit (git), not a wall clock.

### 5b. Hard vs soft predecessors

A predecessor edge makes one of two different claims, and today they wear one column:

- **Hard = *blocks*.** A must be *done* before B can be *built*; remove A and B breaks
  (a real technical dependency). Hard edges drive **readiness** (B is workable only when
  all its hard preds are done), the **acyclicity requirement** (a hard cycle is
  unstartable → ERROR), and **parallelism** (only hard edges constrain what runs at
  once).
- **Soft = *orders*.** B is *conventionally* after A — narrative coherence, review
  ergonomics, resource contention — but could proceed without it. Soft edges are
  **advisory**: presentation order + a suggested path; ignored for readiness, relaxable,
  and a soft cycle is a hint conflict, not an error.

This is F3 made precise: the dogfood DAG mixes them, so a soft "reads-well-after" edge
masquerades as a hard block and a reader (or scheduler) infers a constraint that isn't
there. F3's own case — `WI-014` (check_flows) after `WI-013` (check_docs) are
independent (*soft*), while `WI-031` (gen_trajectory) after `WI-030` (check_trajectory)
is a real import (*hard*). Model it as one `kind` on the edge (default `hard`; `soft`
advisory, dashed in the render). Downstream-migrating — decide with the other schema
changes (§10).

---

## 6. A larger change → the swBlock lifecycle is the stable identity

The ladder:

- **Tune** → new workstream, same swBlock definition, maybe a new TC.
- **Extend / constrain** → update the swBlock's expectations → new/changed SR/LLR/TC
  → work item(s); the knowledge grows.
- **New approach entirely** → **supersede**: mark M `deprecated`, `superseded-by: M'`;
  M' carries the knowledge forward; interfaces re-point.

The key move: make the **swBlock id the durable identity across a rewrite**, not the
SRs. Iteration 1 worried that a "new approach" changes the SRs and loses the
through-line — anchoring identity on the *swBlock* (which survives the SR rewrite) fixes
exactly that. The swBlock is what iteration returns to.

---

## 7. Mating two swBlocks / parts = a *contract* plus *work that consumes resources*

What the registries give you today, and the precise gap:

- **The static contract exists.** [`interfaces.csv`](project-trajectory/registries/interfaces.template.csv)
  `IF-###` has `Direction, Contract (one testable line, may link a spec), Version,
  Stability` — the seam's *what*.
- **The consumed material exists.** [`procurement.csv`](project-trajectory/registries/procurement.template.csv)
  `PART-###` has `Cost, Quantity`, links an `IF-Ref`. A weld filler or screws are
  PART rows.
- **The gap is the assembly *operation*.** Nothing models the *act* of mating —
  weld / torque / integration-test — as **work with duration and energy that
  consumes parts**. Today that would be a work item with `predecessors = [A, B]`, but
  WIs are bare DAG nodes: no `consumes`, no `duration/effort`, no `energy`.

So a mate decomposes as: **`IF-###` (contract) + an assembly WI**
(`predecessors=[A_done, B_done]`, `consumes=[PART-weld, PART-screws]`,
`satisfies=IF-###`, verified by an integration TC, carrying duration/energy). It
reuses IF + PART + the DAG; the only genuinely new modelling is a **`consumes` link
and an effort/duration field on work.** That is the classic **Bill of Materials vs
Bill of Process** split — and the procurement template already flags "per-module
allocation, roll-ups" as a *deliberately deferred* BOM extension. This is that
extension. In software the same shape degenerates to "integration WI,
predecessors = both swBlocks, cost = dev-time," which the DAG already handles — which
is why a software-only repo never felt the gap.

**An assembly is a *graph*, not a fatter asset.** When parts compose into an assembly,
don't grow the `ASSET` row to hold the tree — that repeats the ASSET≠PART overloading
mistake. `ASSET` stays a **flat artifact manifest** (one binary + its hash); the
assembly *structure* — which part `connects-to` which via which joint, which assembly
`contains` which sub-assembly — lives in **edges**. That edge graph is the **physical
sibling of component composition (`Contains`) + interfaces (`IF`)**: parts + connections,
exactly as components + interfaces. It is also where kinematics / CG / inertia and the
build sequence get *derived* — see "Cross-cutting" (after §8) for why the kit owns
that graph's **structure** but **routes out** those numeric resolvers.

### 7a. What the kit tracks: the design-order DAG (not the physical assembly)

Scope ruling (iter 6): the kit needs only the **design-order DAG** — *what to design
next, across all design phases* — **parented by the interface owner**. It does **not**
model physical assembly direction, and the mate's time / material / energy above is
**solution-space** — optional annotation, routed out, never resolved in-kit. The kit
supports agent-assisted (sometimes agent-automated) *design*; the actual mechanism
solution, simulation, and loop-back belong to the solution space.

**The order is largely *derivable*, not hand-authored.** `IF-###` already carries
`Direction` (Provides / Consumes): the **provider** of an interface is designed before
its **consumers**. So "parented by the interface owner" = the provider parents the
consumer, and the design-order edges fall out of the interface registry —
generated-not-hand-maintained.

**Worked example — the kit's own scripts** (already the predecessor chain in
`work-items.csv`):

- `trace.py` (WI-006) + `check.py` (WI-008) — the join engine + the harness contract;
  everyone builds against them → designed **first**.
- the `check_*` validators *consume* `check.py`'s step interface → **after** WI-008.
- `check_trajectory` (WI-030) *provides* the WI-registry validation interface → before
  its consumer.
- `gen_trajectory` (WI-031) *consumes* `check_trajectory` (a literal `import` — a
  **hard** dep, §5b) → designed **last**.

So `WI-006 → WI-008 → WI-030 → WI-031` *is* "design the interface owner before its
consumers." A physical part is identical: the part that **provides** a mating datum
(the chassis / ground link) is designed first; parts that **consume** it design against
that interface, after.

---

## 8. Concrete tech (Elysia.js) and other software tooling

**Elysia is a dependency/technology, not a swBlock** — it is the substrate that
software-category swBlocks are built *on*. It is handled by two things that already
exist:

1. **`docs/stack.ini`** — the declared toolchain ("one-file stack rewiring"). Elysia
   + its version live here.
2. **A knowledge pack / skill** — "when working on an HTTP-boundary swBlock, use
   Elysia's Eden end-to-end types + plugin lifecycle; here are the docs." Exactly the
   outside-resource-plus-skill pointer from §4.

No new axis. A framework is a stack choice taught by a skill — the case that
*validates* the knowledge-pack idea.

**Other software tooling worth considering — kept downstream, never in the core:**

- **Typed interface contracts at `IF-###`** *(highest value)*. The `Contract` cell
  already allows a linked spec; let a software seam link a **machine-checkable**
  contract (OpenAPI / JSON Schema / Elysia Eden types / tRPC / protobuf). This makes
  a software seam verifiable the way a drawing makes a weld verifiable.
- **Dependency manifest / SBOM as software "procurement."** `PART` (bought parts) ≈
  a dependency lock / SBOM; `pip-audit` / `npm audit` / CycloneDX are the "vendor
  datasheet" check. The kit already has `check_vendored.py` in this spirit.
- **Keep the core stdlib-only and stack-agnostic.** Elysia, Bun, tRPC — none belong
  *in* the kit; they are declared in `stack.ini` and taught by skills. **The kit
  provides the slots, never the fillings.**

---

## Cross-cutting — the shared structure: one edge vocabulary, routed resolvers

The deepest observation in this thread: **parametric CAD models, workstreams, and
physical assemblies are the same abstract object** — a *typed graph of entities
related by edges, traversed to derive properties*. Not speculative: the kit **already
contains two instances** — the work-item dependency DAG (`check_trajectory` validates
it, `gen_trajectory` ranks + renders it) and the `SN→SR→LLR→TC` join (`trace.py`). The
reuse is real, but it lives at one layer and **stops hard at the next.**

**Reusable — a small typed-edge vocabulary + a stdlib graph core (the kit's job).**
Nearly every relationship in the whole model is one of ~four edges:

| Edge | Software instance | Physical instance | Resolves to (stdlib) |
|---|---|---|---|
| `contains` / part-of | swBlock composition | assembly → sub-assembly → part | tree / roll-up order |
| `depends-on` / step | WI DAG, workstream iterations | assembly sequence, parametric steps | topological order = schedule / build order |
| `connects-to` / mates | `IF-###` interface | physical joint (+ consumes `PART`) | seam contract |
| `realises` / derived-from | `swBlock.Realises`, `TC→LLR` | `ASSET→LLR` | the trace join / verification |

Recording these in **one uniform edge form** (`from-id, to-id, type`) — even though
the *nodes* live in different registries — is the reuse win, and the shared core
(resolve endpoints, check acyclicity where required, emit topological order, feed the
generic SVG renderer) is ~the 80 lines already in `check_trajectory` + `gen_trajectory`.

**But not every graph is a DAG — edge *type* decides.** `depends-on` and `contains`
are acyclic (the roadmap, the build order, the part tree); `connects-to` is **general
— it has loops.** The clean test is a **4-bar linkage**, which is *three* graphs at
once: **composition** (mechanism ⊃ 4 links + 4 pins) is a *tree*; **connection**
(ground–crank–coupler–rocker–ground) is a **cyclic loop** — that closed loop *is* the
mechanism; and the **build process** (mount ground → pin each link → close the loop)
is a *DAG*. So "assembly as a DAG" holds for the *build sequence*, not the *connection
topology*. The stdlib core checks acyclicity only where the edge type requires it, and
a cyclic connection graph needs a **general graph layout**, not the layered-DAG
renderer `gen_trajectory` uses today. The loop's *kinematics* (DOF, motion) is a
routed-out resolver — never computed in-kit.

**Not reusable — the resolvers (the kit *routes*, never implements).** Topological
*ordering* is cheap and shared. But **kinematics** (constraint-solving DOF),
**mass-properties** (CG / inertia through the assembly transform tree), and
**parametric geometry** (re-evaluating features through a CAD kernel) are
numeric-geometry domains that blow past the stdlib-only / offline line. The kit
already has this stance — it *names and routes* CAD verification, perf, and LFS to
project-owned / external tools and only **records** the verdict at the gate. Same
here.

**The container abstracts across physical domains — keep it domain-neutral.** A
physical component is a *bounded container*; hydraulics, pneumatics, aerodynamics,
electrical, magnetic are just more property-and-port kinds on that container. The kit
must **not** solve any of them (the bloat trap) — it only needs its interfaces to be
**typed ports** (mechanical / electrical / fluid / …) and its properties an **open
key-value set**, not a fixed mechanical schema. Then every domain's physics (CFD / FEA
/ circuit-sim / magnetics) is a routed resolver behind the same bright line. The
structure abstracts; the kit stays out of the physics.

**Recommendation on reuse:**
- **Unify the edge vocabulary now** (cheap, design-time): one relationship
  representation across registries — pure SSOT, the kit's own instinct.
- **Extract the shared graph engine when the second consumer is real** (deferred):
  today `check_trajectory` is the only graph validator; when an assembly graph
  arrives, factor the common core out rather than copy it. YAGNI until then.
- **Draw a bright line at the resolver layer:** the kit owns *structure + traversal +
  validation + render*; it routes kinematics / mass / geometry to external tools and
  records their verdicts. That line is what stops this becoming a PLM / CAD engine
  masquerading as a stdlib kit.

---

## The artifact — `PROJECT_STATE.html` (evolving `trajectory.html`)

One self-contained HTML at the **repo root** — a single kit-generated file with **all
diagrams inside it** — and an **"as-of" line generated into the page, visible the moment
it opens** (*"state as of commit `abc123` · 2026-07-09"*) so a reader instantly sees how
fresh or stale the view is. It presents the whole model in four views:

| View | Axis | Source |
|---|---|---|
| **What** — SN breakdown | WHAT | the `SN→SR→LLR→TC` spine (today's icicle) |
| **How — physical** (if any) | HOW | the part/assembly **graph** (new; may be cyclic — see the 4-bar) |
| **How — SW architecture** | HOW | the code map (`gen_arch_map.py`) |
| **When — roadmap** | WHEN | the *prospective* WI DAG (§5a) |

So it mostly **unifies existing generators** (`gen_trajectory` = What + When,
`gen_arch_map` = How-SW) and adds one new **How-physical** graph view. Two constraints
carry over from the design:

- **The "last generated" date must stay deterministic.** `gen_trajectory` is clock-free
  *on purpose* so `--check` can byte-compare. Derive the stamp from the **latest commit
  touching the sources** (git), not `now()` — meaningful, byte-stable, and it *is*
  §5a's "the past is git."
- **The How-physical view renders a *general* graph** (loops allowed), not the
  layered-DAG layout — see Cross-cutting.

Rename `docs/trajectory.html` → root `PROJECT_STATE.html`, or keep both, is a small
migration call (open question §12).

---

## Operating the model — the dynamic layer (moved out, iter 6)

*The coordinator / planner / implementer / reviewer pipeline and the loop-vs-judgment
seam now live in their own sibling note — [`AGENT_ROLES.md`](AGENT_ROLES.md) — because
that is **process / orchestration**, a different concern from the static structure here
(the owner's call). The only tie-point that matters here: **each role writes exactly one
static home** — coordinator → the roadmap DAG, planner → the swBlock definition +
knowledge pack (+ the WI), implementer → the code, reviewer → test evidence. See the
sibling note for the pipeline and the coordinator breakup.*

---

## 9. Naming ruling (updated iter 6)

*⚠ **Iter 8 may supersede this:** SWB/HWB may collapse to one `CMP-###` (domain-neutral
component) — see "Iteration 8". The ruling below stands until that's confirmed.*

- **`swBlock`** — the **software** decomposition unit. Chosen over "Module" (collides
  with `MOD-###` = a delegated repo) and "Processor" (reads as a CPU). The **physical**
  unit is a **part / assembly**. "Module / component" stays the generic term for either.
- **`REPO-###`** (proposed) — **rename `MOD-###`**, the multi-repo delegation registry,
  since it is a delegated *repo*, not a component. This frees "module" from the collision.
- **Workstream** — a **mutable grouping category** on swBlocks + assemblies (not a
  campaign entity, not an SN). Bounds deliverables with shared dependencies; project-
  defined.
- **Track** — **retire from the WI layer.** "Track" means *only* the parallel-execution
  lane.

*The "module" → swBlock / part / component rename across this note was applied in iter 7.
`MOD-### → REPO-###` in the kit remains a mechanical follow-up (Q13).*

---

## 10. Cautions & staging

- **The core stays lean; the physical machinery is opt-in.** This model is elegant
  but hardware-flavoured (supersession, BOM/BOP, energy, assembly ops). Keep it
  **layered**: a pure-software repo sees only `swBlocks + Interfaces + Skills`; a
  hardware repo opts into `PART-consumption + assembly-ops + energy/time`. `MOD /
  ASSET / PART` are *already* opt-in "rung-3" layers — extend in that spirit.
- **Own the graph, route the resolvers.** The shared-structure insight (Cross-cutting,
  after §8) is *structural* reuse only. Do **not** build a general graph-resolver
  framework: kinematics, mass-properties, and parametric geometry are external tools
  the kit *routes and records*, never implements — the same stdlib-only / offline line
  that keeps it from reinventing a CAD / PLM engine.
- **This meta-repo cannot dogfood the physical half.** It is software and stdlib-only
  — the same limitation that stopped it dogfooding the README SN-inventory. The
  unifying *idea* (one component unit for both worlds) is the value; the physical parts
  ship untested-by-us and must be exercised by a real hardware adopter.
- **Downstream-migrating.** A new component registry + a renamed WI column is
  inherited by every adopter — exactly the class of change
  [`THREAD_52_REVIEW.md`](THREAD_52_REVIEW.md) **F3** says to decide *before* adoption
  spreads. F3's "hard-vs-soft predecessor edges" is the same schema conversation;
  settle them together.
- **Intersects F1.** F1 wants `SR-037/038` to trace the trajectory layer's own code
  and raises a G3 re-attestation question. If the WI schema changes anyway,
  **sequence F1 first** so the ratified spine is not re-attested twice.
- **Staging (recommended):**
  - **Now (cheap, non-migrating):** retire "track" from the WI layer; document the
    three-axis model + the swBlock-as-centre-of-gravity framing.
  - **Next:** stand up the **swBlock / component registry** (`Realises` + interfaces +
    category + knowledge refs + state; `LLR.Module` dropped) — the highest-leverage step.
  - **Later, gated on real need:** the `consumes`/effort fields (physical timelines),
    typed `IF-###` contracts, workstream registry. Don't build speculatively (YAGNI;
    the kit's "smallest change that works").

---

## 11. Provisional decision

Adopt: **three axes (WHAT incl. functional decomposition · WHY distributed · HOW =
swBlocks / parts · WHEN = Workstream + Session), each its own source of truth, joined by
id-references (`swBlock.Realises` is the WHAT↔HOW hinge), surfaced by generated views —
never by restating one axis inside another.** Make the **swBlock the centre of
gravity**: durable expectations + interfaces + category + knowledge + lifecycle; keep
the workstream a thin grouping category. Reuse the **skills layer** as the knowledge-pack substrate.
Treat **mating as work that consumes parts** and keep that (and all physical
machinery) an opt-in layer. Where relationships recur (composition, dependency,
connection, realises), **share the graph *structure*** — one edge vocabulary + a
stdlib traversal/render core — but **route out the domain resolvers** (kinematics /
mass / geometry are external tools the kit records, not implements).

**Status: provisional — not ratified, not built.** More passes expected before
implementation.

---

## 12. Open questions for the next iteration

1. **The `swBlock` / component registry — its exact schema.** A **sibling** registry
   (not a widened `MOD-###`), decided across iters 3–7: light CSV row + optional
   md-frontmatter detail doc, **not ini** (§3a); **owns `Realises`** (many LLRs, M:N,
   §2); geometry via `ASSET` + `IF` (§3b); **`LLR.Module` dropped entirely** (iter 7).
   *Still open:* the column set + **id scheme** (swBlock `SWB-` / part `PRT-`?), and
   **instancing** (type vs instance) — deferred until a real case.
2. **Is a Workstream distinct from an SN?** **RESOLVED (iter 6): yes** — a workstream is
   a *mutable grouping category* on swBlocks + assemblies (bounds shared-dependency
   deliverables), never an SN (§2, §5). No registry; a category column.
3. **`consumes` + duration/energy on work** — the physical-timeline gap (§7). What is
   the minimal schema, and does it stay vacuous for software repos?
4. **Typed `IF-###` contracts** (§8) — let a seam link a machine-checkable spec;
   which formats, and is there a check?
5. **Hard-vs-soft predecessor edges (F3)** — **expanded (iter 6) in §5b**: a `kind` on
   the edge (default `hard` = blocks; `soft` = advisory). Still a downstream-migrating
   schema call; decide with #3.
6. **Where does the knowledge pack live** — **RESOLVED (iter 6):** `docs/knowledge/
   <label>.md` (project domain knowledge) + `skills/` (reusable), referenced by label
   from the swBlock/part row (§4). Single-sourced; no registry.
7. **Migration ergonomics** — what `bootstrap.py` scaffolds and whether
   `downstream-resync` needs a step (downstream-migrating — §10).
8. **Unify the edge vocabulary?** One uniform `from-id, to-id, type` relationship form
   across registries (Cross-cutting) — worth doing at design time even before a second
   graph consumer exists? And when the assembly graph lands, extract the shared core
   from `check_trajectory` rather than copy it.
9. **The swBlock drift check (§3c)** — is the source-symbol check that keeps a swBlock
   current the *same* mechanism as F1's untraced-code / Thread 49's symbol-reference
   validation? If so, build it once, serve both.
10. **`PROJECT_STATE.html` migration** — rename `docs/trajectory.html` → root
    `PROJECT_STATE.html`, or keep both? Confirm the git-derived "as-of" stamp survives
    the deterministic `--check`.
11. **Cyclic-graph rendering** — the How-physical view needs a general graph layout
    (loops), not the layered-DAG renderer. A stdlib force-free layout, or route
    rendering out for the physical view only?
12. **Does the roles pipeline belong in this note or its own?** **RESOLVED (iter 6): its
    own** — split to [`AGENT_ROLES.md`](AGENT_ROLES.md) (the owner's call); its open
    questions live there now.
13. **Renames** — the note's "module" → swBlock / part / component rename is **done
    (iter 7)**; **`MOD-### → REPO-###`** in the *kit* remains a mechanical follow-up
    (downstream-migrating), sequenced after the schema settles.

---

## Iteration 8 (in progress) — the knowledge-grain question

**Status: the owner is mid-thought; this is a live capture, not a ruling.** It
supersedes the iter-6/7 SWB/HWB split *if* the leaning below is confirmed.

**The reframe (owner leans here).** Drop SWB/HWB as *structural* registries — their
structure (dependency DAG, assembly, kinematics) **derives from IF + ASSET + PART**.
Keep **one domain-neutral component, `CMP-###`** (`id, Name, Category, Knowledge,
State`), whose *only* job is to be the **durable, identified, set-grained home for
knowledge + lifecycle** — the thing an IF (too fine), a workstream (too mutable), or a
bare label (no lifecycle) cannot be. Membership is a `Component` tag on the
IF/ASSET/PART rows; the CMP row holds only what a tag can't.

**Knowledge is layered by grain** (this salvages the owner's "put knowledge on
LLRs/types/IFs" idea — it's right, just not a *replacement* for the set level):

| Grain | Home | Example |
|---|---|---|
| generic / by-type | `ASSET`/`PART` category (**derived**) | aluminium → galvanic + fatigue |
| boundary | `IF` | this interface needs special timing handling |
| implementation | `LLR` | this algorithm's numerical-stability caveat |
| **set / subsystem** | **`CMP`** | the perception pipeline's low-light strategy |

The floated *distributed-only* variant (a software block = an LLR carrying knowledge;
hardware knowledge keyed by asset/part *type*) is **leaner but re-creates the
knowledge-for-sets gap**: an LLR is finer than a component, and type-keyed knowledge is
*generic*, so **set-specific** knowledge ("*this* subsystem/assembly") goes homeless.
That is why it doesn't sit right — keep knowledge *layered*, with `CMP` holding the set
grain.

**CAD extraction (owner's question).** Geometry, **mass, inertia, and material are
extractable from many CAD formats.** Robotics formats (**URDF/SDF**) *declare* mass +
inertia tensor + material — a plain (even stdlib-XML) read; native CAD and **STEP
AP242** carry material and compute mass-props; **STL/mesh** carry geometry only (mass
computed from geometry + density). The heavy cases need a CAD kernel = an **external
tool**, so keep the extractor **project-owned (route + record)**, not in the kit core.
Consequence: `Material` / mass-props are **derivable from the ASSET** (a *view*), not
necessarily authored — which *strengthens* "structure derives from ASSET + IF" (one
routed extraction yields body + mass + inertia for the plant / kinematic model).

**Diagnosis navigates the grain** (owner's workflow): a problem → **probe the affected
`IF`** (seam) → **branch to the LLR software + the assemblies that mate** → root further
— surfacing boundary-, then implementation-, then set-knowledge as you descend,
*instead of ingesting the whole system*. The diagnosis walk *is* a walk down the
knowledge layers.

**Open (owner not done):** the owner's next concern was cut off mid-sentence — more to
come. Pending: CMP vs distributed-only; whether a primitive may belong to multiple
CMPs; how `Component` tags get assigned (authored vs inferred from packages / shared
knowledge labels).

---

## Cross-links

- [`THREAD_52_REVIEW.md`](THREAD_52_REVIEW.md) — the review that surfaced this; **F3**
  (schema/edge-semantics) and **F1** (trace the layer's own code) are the two
  findings this note is coupled to.
- [`docs/requirements/work-items.csv`](docs/requirements/work-items.csv) — the `Track`
  column to retire; [`gen_trajectory.py`](project-trajectory/scripts/gen_trajectory.py)
  / [`check_trajectory.py`](project-trajectory/scripts/check_trajectory.py) — the view
  + validator that follow.
- [`project-trajectory/registries/modules.template.csv`](project-trajectory/registries/modules.template.csv)
  (multi-repo `MOD-###`) ·
  [`interfaces.template.csv`](project-trajectory/registries/interfaces.template.csv)
  (`IF-###`) · [`procurement.template.csv`](project-trajectory/registries/procurement.template.csv)
  (`PART-###`) · [`assets.template.csv`](project-trajectory/registries/assets.template.csv)
  (`ASSET-###` — geometry/binary artifacts, §3b) — the physical-axis registries.
- [`project-trajectory/skills/`](project-trajectory/skills/) — reusable knowledge (§4);
  **`docs/knowledge/<label>.md`** — project-specific knowledge packs (iter 6, §4). ·
  `docs/stack.ini` — where a framework like Elysia is declared (§8).
- [`project-trajectory/scripts/gen_arch_map.py`](project-trajectory/scripts/gen_arch_map.py)
  — the generated + `--check`ed code map: the drift-guard idiom §3c applies to
  swBlocks, and it is the **How-SW** view of the artifact. `trace.py` +
  `check_trajectory.py` are the two **existing typed-graph instances** the
  Cross-cutting section would factor from.
- [`AGENT_ROLES.md`](AGENT_ROLES.md) — the **sibling note** for the dynamic layer
  (coordinator / planner / implementer / reviewer; the loop-vs-judgment seam), split out
  in iter 6. Its anchors: [`agent_loop.py`](project-trajectory/scripts/agent_loop.py),
  `docs/run-phase` (PLAN | BUILD), the integrator role (`tracks-README`).
- [`project-trajectory/PROCESS_OPTIONS.md`](project-trajectory/PROCESS_OPTIONS.md) —
  "Trajectory / work-items layer" (the `Track` prose) and "Parallel tracks" (the
  *other*, execution-lane meaning of "track").
