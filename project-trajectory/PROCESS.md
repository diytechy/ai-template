# Development Process (template)

Canonical method for a gated, requirement-traced project. Copy this into a new
repo as `docs/process.md`. It is **stack-agnostic** — wire the harness commands
to your project's language/tooling. Other docs reference this file by section
rather than restating it.

---

## 1. Roles (hats), not necessarily separate agents

One driver wears these hats in sequence, keeping context. Spawn a *separate*
agent only for an independent pre-gate review (see §6).

| Hat | Owns (single source of truth) |
|---|---|
| Stakeholder | `requirements/stakeholder-needs.md` (SN-###) + edge-case expectations |
| UX / Docs | documentation quality, quick-reference, usability findings |
| System Engineer | `requirements/system-requirements.csv` (SR-###); **gatekeeper** |
| Software Engineer | `requirements/low-level-requirements.csv` (LLR-###) + code + `architecture.md` |
| Test Engineer | `test/test-cases.csv` (TC-###) + the check harness + coverage/trace reports |

A hat only edits artifacts it owns; to change another, file a finding addressed
to its owner (§5).

**Domain hats (scope-dependent).** The five above are the spine; choose
additional discipline hats at project setup to match the scope — e.g. **Network
Engineer**, **Security Engineer**, **Data/ML Engineer**, **Hardware/Mechanical
Engineer**, **Mechatronics Engineer**, **DBA**, **SRE/Ops**, and an
**Integration/Coordination** hat that allocates the cross-module performance and
resource budgets (`requirements/performance-budgets.csv`, §9). A domain hat owns
the slice of `SR-###`/`LLR-###` rows in its area (tag them, e.g. an `Area`
column or an `SR-NET-###`-style prefix) and brings its own edge-case and
release-checklist items. Record the **active hats** for this project in
`status.md`; don't wear a hat the scope doesn't need. Like the others, a domain
hat is usually the same driver switching context — spawn a separate specialist
agent only for an independent high-risk review (§6).

## 2. Identifier scheme

| Prefix | Level | Parent link |
|---|---|---|
| `SN-###` | Stakeholder Need | — |
| `SR-###` | System Requirement | `SN-Refs` |
| `LLR-###` | Low-Level Requirement | `SR-Refs` (+ Module/CodeSymbol) |
| `TC-###` | Test Case | `Verifies` (SR/LLR) |

Stable, zero-padded, never reused.

## 3. Traceability & anti-duplication

- **One fact, one home.** Reference by ID and link; never restate.
- **Decompose, don't paraphrase.** A child adds detail; if it would merely
  repeat its parent, link instead.
- **Registries are the machine source of truth; prose is thin** and links by ID.
- **The traceability matrix is generated** by a small join over the registries'
  ID/parent columns; it reports **orphans** (req with no child/test; test/LLR
  with no parent). Hand-maintaining the matrix is forbidden.
- **Code carries back-links** (`Implements: SR-007, LLR-014`); test names embed
  the verified ID. CSV columns are authoritative.
- **Architecture is generated** (module/function map) so it cannot drift; keep a
  hand-written one-page overview above it.
- **Modularity/dedup**: shared logic in exactly one place; pure cores separated
  from I/O/GUI shells; small functions; one-page-readable architecture.
- **Thin orchestrators**: an entry point / top-level routine should *compose, not
  compute* — a short, ordered sequence of well-named calls so that reading it is
  the high-level flow. Push logic down into the named steps. The flow is
  generated from the orchestrator (`gen_arch_map.py --flow`, see below), so a
  routine that inlines logic instead of delegating shows up as a short,
  uninformative flow — a built-in tripwire.

**Right-sizing has guardrails — and a name for the calibrated shortcut.**
"Simplest thing that works" (the agent guide's "Right-size the solution") is
calibrated, not flimsy: it never trims **validation at trust boundaries**, error
handling that would **lose or corrupt data**, **security**, **accessibility**, or
skipping straight to a fix before **understanding the problem** (root cause, not
symptom). Where a deliberate simplification is still the right call, mark it
inline with a **`SHORTCUT:`** comment naming the **ceiling** it accepts (e.g. a
global lock, an O(n²) scan, a naive heuristic) and the **upgrade path** past it —
so the shortcut is greppable, reviewable, and never silently mistaken for the
final design. One tag, defined once; not a taxonomy.

**Reviewability — review the source, not the render.** The registries (the
`SN`/`SR`/`LLR`/`TC` CSVs) are the tracked, line-by-line-reviewable source of
truth; every other view is *generated* from them. Generated output splits by
size into two tiers:

- **Small, diff-meaningful blocks** live in tracked files behind `GENERATED`
  markers and are kept honest by a freshness gate — the code map, dependency
  diagram, and program flow (`gen_arch_map.py --check` fails a commit that left
  them stale). These you *do* read in diffs.
- **Large composite artifacts** — the full trace report (`test/report.md`: the
  counts, matrix, the `SN→SR→LLR→TC` text outline, and the Mermaid graph), the
  HTML map (`trace.py --html`), and the **performance report** (`test/perf-report.md`,
  §9) — are regenerated every run, **gitignored**, and published by CI as
  artifacts. Don't diff or review these; review the registry change that produced
  them.
- **Committed goldens** — a small generated file you *do* commit, and whose diff
  is reviewed as the record of an accepted change: the **performance baseline**
  (`test/perf-baseline.json`, §9). Moving a number means committing the new golden
  in the same PR, so the change is explicit, never silent.

This is the "composite artifacts are ignored from change tracking" rule, named:
the cost of reviewing a big regenerated file is never paid, because the small
registry diff already carries the intent.

**The doc set must stay navigable (the doc map stays honest like the code map).**
The freshness gate above keeps *generated* blocks honest; the hand-written docs
need the same guarantee. `scripts/check_docs.py` (stdlib, a process check — §7)
parses the Markdown under `docs/` plus the root `*.md`, builds the link graph,
and **fails on broken intra-repo links** (a missing target file or `#anchor`) —
the machine version of the "verify no broken intra-doc links" step the gates
otherwise ask a human to do. It also **warns on orphan docs** (no path from an
entry root — root-level `*.md`, an optional `docs/index.md` Map-of-Content, or a
configured entry) and, with `--stale` (git-gated), on a doc left frozen beside a
non-doc file it links that has since changed. Broken links are a hard finding;
orphans/staleness are warnings, because a young project legitimately has
standalone docs until it links them. Run by `check.py` from G1 on.

**Interface contracts live at the code, referenced — not restated.** Every public
module/function documents its contract once, where it is implemented, as a
structured block an agent (or human) can read inline and grep:

- *Inputs* — each parameter's type and, where it matters, its **range/enum/units**;
- *Outputs* — return type/shape;
- *Config* — config keys it reads and their constraints (+ where they live);
- *Raises/Errors* — failure modes and what they signal.

Keep it **non-duplicative by referencing IDs**: a constraint that is already a
requirement (an input range, an accepted set) lives once in the SR — its
`AcceptanceCriteria` and the `Permutations` dimensions — and the block cites the
id (`SR-012`) instead of restating the range. The block carries `Implements:
SR/LLR`, so the *intent* stays in the registry, the *implemented signature* stays
in the code, and the link is explicit. The code map harvests the symbol's summary
and back-links, so a reader can find the contract from the map in one hop. (The
exact tag syntax is the agent guide's job — see `AGENTS.template.md` "Define the
interface (contract) at the code".)

**Generated code map — route the AST into the agent's working file.** An agent
edits faster and more safely when a *current* index of the code is in the file it
already reads, instead of re-deriving the layout each session. So the harness
generates, by parsing the source (AST), a per-module map between marker comments:

- each module's **one-line summary** (from its module docstring/header),
- its **internal dependencies** (which in-tree modules it imports) — this makes
  layering invariants auditable (e.g. "Common must not import Engine") and shows
  the blast radius of a change,
- each public symbol's **signature**, summary, and `Implements: SR/LLR` back-links.

Because the map is *harvested from docstrings and `Implements:` comments*,
commenting for humans (see the agent guide's "Comment for humans — and the map")
directly improves the map. The reference generator is `scripts/gen_arch_map.py`
(Python AST, stdlib); each stack ships its own equivalent (e.g. a PowerShell or
ts-morph version) writing into the **same marker block** — that block is the only
contract.

**Routing (where the map lands).** `gen_arch_map.py --doc` is repeatable. Put the
marker pair wherever agents read and the generator keeps it fresh:
- *Full map in `architecture.md`, the agent guide links to it* — cleanest;
  one home; the agent takes one hop. Good default for large codebases.
- *Map embedded directly in `AGENTS.md` / `CLAUDE.md`* — the agent sees it inline
  with zero hops; cost is that the guide's diff churns whenever the code changes.
  Good for small/medium codebases where the map fits on a screen.
Either way the harness regenerates it (`--check` fails the gate if stale), so it
never rots. Don't hand-maintain a code map.

**The committed map is a contract, not a search index.** `gen_arch_map.py`
produces a **committed, diff-reviewable, drift-gated** artifact — part of the
source of truth, read to learn the code's *intended* shape. Query-time
**semantic-retrieval tools** (LSP-backed code-graph servers, Serena-style MCP
indexes) are a *different* thing: not committed, language-server-dependent, and
rebuilt on demand. They are a legitimate **optional downstream accelerator** for
chasing references across a large repo, but they **don't replace** the committed
map, and the kit must **not** hard-wire one — that would break stdlib-only and add
a server/LSP dependency. Use one if it helps; keep it out of the required path.

**Generated high-level flow.** `gen_arch_map.py --flow <entry>` emits the ordered
internal calls of an entry/orchestrator function (each with the callee's summary)
into a `GENERATED FLOW` marker block — a generated, drift-proof rendering of the
"Thin orchestrators" rule above. Put the markers in `architecture.md` (and/or the
agent file) and add `--flow` to the harness's map step. It complements, and does
not replace, the hand-written flow overview that shows control flow.

**Design-time runtime flows (authored at G2, checked).** Everything above is
harvested from code, so none of it exists at G2 — yet G2 is exactly when a
human reviews the LLRs, and runtime *behavior* (ordering, concurrency,
background work, what blocks on what) is the thing most easily misread from
CSV rows. So the Software Engineer hat authors a **"Runtime flows"** section in
`architecture.md` **with the LLRs, before the G2 review**: one Mermaid
`sequenceDiagram` per key user-visible scenario, and always one for any
behavior that is concurrent / asynchronous / non-blocking. Participants are
the planned modules (the LLR `Module` column); each diagram cites the SR/LLR
ids it renders. The G2/G3 harness runs `scripts/check_flows.py`, which fails
when the section is missing, has no diagrams, a diagram cites no SR/LLR id, or
a cited id doesn't exist in the registries. The human's G2 review starts from
these diagrams — verify the flow there, then spot-check the rows. Update a
flow in the same change that alters its LLRs; from G3 on, the generated
map/flow corroborates these authored diagrams rather than replacing them.

**Diagrams are text (Mermaid); the dependency graph is generated.** Diagrams
live as ```` ```mermaid ```` fenced blocks inside the Markdown docs — rendered
natively by GitHub/GitLab/Gitea and the VS Code Markdown preview (offline-
capable), so no diagram toolchain is required and the diagram source diffs like
prose. Hand-written diagrams (the one-page flow, sequence diagrams for key
interactions) follow the same anti-duplication rule as prose: reference IDs,
don't restate requirements. The module **dependency diagram is generated**:
`gen_arch_map.py` splices a Mermaid graph of the internal imports into the
`GENERATED DEPENDENCY DIAGRAM` markers wherever a routed doc carries them
(`architecture.md` ships with the pair), covered by the same `--check` — so the
picture of the layering can't drift any more than the map can. Don't commit
exported diagram images; the text block is the source. If a project genuinely
needs diagram types beyond Mermaid (PlantUML/C4/BPMN) or has AsciiDoc sources,
wire a Kroki/PlantUML toolchain as *project* tooling — it is deliberately
outside the kit's required path.

## 4. Objectives, gates, and exit criteria

Advance only when criteria pass; **pause for human approval at each gate**.
Define machine-checkable criteria wherever possible; classify the rest honestly.

- **G1 — Requirements, UX & constraints.** SN complete (priority + measurable
  acceptance intent + edge cases); every SR links ≥1 SN with measurable
  acceptance criteria; usability/doc needs + constraints + non-goals captured.
  Sign-offs: Stakeholder, UX, System Engineer.
- **G2 — Decomposition & test coverage.** Every SR → ≥1 LLR (or
  Analysis/Inspection); every SR and LLR → ≥1 TC; traceability **0 orphans** and
  ids unique/well-formed; **no `-000` placeholder rows or flow citations remain**
  (`trace.py`/`check_flows.py --no-placeholders`); **every SR with variable
  inputs has its dimensions enumerated (`Permutations`) and a stated combination
  strategy, with boundary values covered** (see "Dimensional coverage" below);
  **key runtime flows are diagrammed and pass `check_flows.py`** (see §3
  "Design-time runtime flows"); harness runs locally + CI. Sign-offs: System
  Engineer, Test Engineer.
- **G3 — Implementation (test-first).** Code is written **test-first**: each G2
  TC becomes a *failing* test before the code that satisfies it, then the minimal
  code to pass, then refactor (red → green → refactor). TDD is *how* G3 code gets
  written; the SN→SR→LLR→TC spine is *what* it must satisfy — it operates within
  the traceability discipline, not instead of it. The exit criteria below
  (coverage, every in-scope SR Verified) are what that loop drives toward.
  Format/lint clean; every source module parses
  (`gen_arch_map.py --strict-parse`); the **full** test tier passes; coverage ≥
  `COVERAGE_THRESHOLD`; registry **schema** holds (required fields non-empty,
  `Verification`/`Tier` in vocabulary — `trace.py --strict-schema`); every
  **in-scope** test-verifiable SR **Verified** (phase-scoped — see "Phased
  delivery" below); every other SR explicitly **Demonstration / Manual /
  Inspection**; each in-scope SR's implementing symbol is **substantive, not a
  stub** (Inspection — see "No-stub / substance review" below). Sign-offs: System
  Engineer, Test Engineer.
- **G-Release — Release readiness** *(per release; skip for a one-off
  deliverable)*. The **release** test tier passes (incl. slow/hardware tests);
  the generated **release checklist** (`scripts/gen_release_checklist.py`) is
  completed and signed; version bumped; changed `Stable` interface versions
  communicated to counterparts; docs/changelog updated. Sign-offs: Test Engineer,
  any active domain hats, Human.
- **G-Final — Acceptance.** Human/stakeholder exercises the real product (incl.
  Demonstration/Manual items) and approves. For shipped software this is the
  human half of G-Release; for a bespoke deliverable it stands alone.

**Consistency review (G1; re-checked at G2).** Separate from the *structural*
checks `trace.py` runs — orphans, duplicate ids, schema — the **System Engineer**
hat reads the needs and requirements **against each other** for the conflicts a
script can't see: contradictory acceptance criteria or limits, mutually exclusive
behaviors, duplicate or overlapping requirements, ambiguous / underspecified
needs, and overlapping `Area`/hat ownership. This is the **consistency**
complement to G1's *completeness* criteria, not a restatement of them, and it is
**human/LLM judgment, not a machine check** — classify it as a Manual/Analysis
activity and never imply `trace.py` performs it. (An independent LLM reviewer
(§6) is well-suited to a first-pass contradiction sweep, but the **human makes the
call**.) Route each contradiction or ambiguity through the §5 findings protocol to
its owner; where it needs a human decision, **pause and ask — don't guess**. This
is the reachable-human flip side of *Assumptions* logging: record an assumption
only when **unattended**; when a human is available, **solicit clarification**.
Track unresolved ambiguities in `status.md` *Open items*, and re-run the review at
G2 when SRs decompose into LLRs.

**No-stub / substance review (G3).** Traceability, coverage, and a green test
suite confirm an implementation *exists* and *passes*; none of them, on its own,
confirms it has **substance**. A body that is `pass` / `...` / `raise
NotImplementedError` / a bare `return None` / a placeholder return satisfies its
trace links and can even hold a coverage line, yet does nothing. The G3 criterion
above therefore adds: **every in-scope SR's implementing symbol does real work, not
a stub.** TDD (G3) mitigates this — a red-first test should fail against a stub —
but coverage can be met by a test that exercises a stub's trivial path, and
Demonstration / Manual / Analysis SRs have **no** automated test to fail, so the
check is named explicitly. It is **Inspection** — human/LLM judgment, classified
honestly, **never a machine verdict** — so fold the prompt into §6's
independent-reviewer checklist (a fresh-context reviewer reads the §3 code map,
which already harvests each public symbol's summary and `Implements:` back-links,
and confirms the body matches the requirement). The kit ships an **optional,
Python-reference tripwire** for it — `scripts/check_stubs.py` (§7), which lists
trivial-bodied public symbols — but, like the perf *meters*, that detector is
**product-layer and warn-first** (a stub's shape is language-specific; a tiny pure
function is not an unfinished one), so it informs the Inspection, it does not
replace it. Same stance as `ruff`/`pytest`: name the criterion; the project picks
and wires the tool.

**Phased delivery (version subsets).** A roadmap that ships v1 before v2/v3
needs gates that close *per phase* without dishonesty. SRs may carry an
optional **`Phase`** tag (e.g. `v1`, `v2`; blank = in scope for every phase).
Semantics:
- **Traceability is phase-blind.** Every SR keeps its LLR + TC rows from G2 on,
  whatever its phase — decomposition is cheap and pins the design.
- **The G3 Verified criterion is phase-scoped.** `check.py --gate G3 --phase v1`
  (cumulative for later closures: `--phase v1,v2`) requires Verified only for
  in-scope SRs; out-of-scope SRs are listed in the trace report as
  **phase-deferred** — an explicit, recorded exemption, never a silent skip.
- **G-Release is phase-scoped the same way:** `gen_release_checklist.py
  --phase v1` includes only in-scope human items and the release-tier/manual
  TCs verifying them.
- Later phases re-enter at G1/G2 as requirement increments and close their own
  G3/G-Release with the grown phase list.

**Lifecycle phase (when in the running product's life a requirement holds).**
Distinct from the delivery `Phase` above (which is *when we ship it* — v1/v2), a
requirement also has a **lifecycle phase**: *at what point in the running
product's lifetime must this hold, and how often?* Naming it stops the perennial
miss of writing only steady-state requirements and discovering the install/setup
ones late. Capture it as an **optional `Lifecycle` tag** on an SN/SR (a column or
inline tag, mirroring `Area`; blank = unspecified, treat as **Runtime**) — use the
distinct name `Lifecycle`, never overload the delivery `Phase` column. The default
vocabulary is an **open, project-named set** (extend it per scope like `Area`; it
is **not** a fixed enum):

- **Provision** (ready) — must hold *before the process can run at all*: install,
  dependencies/runtime present, infra provisioned.
- **Startup** (set) — established *once per launch, before it serves*: load +
  validate config, run migrations, open the initial pool, allocate fixed
  resources, readiness probe.
- **Runtime** (go) — steady-state serving, *including recurring acquisition*:
  handle requests, reconnect on drop, per-request alloc, dynamic config reload.

Optional **Shutdown**/**Teardown**, **Upgrade**/**Rollback**, **Recovery** extend
the set when the scope needs them.

- **Discriminate by *when / how often*, not by the word "setup"** — almost
  everything readies *something*. Opening the connection pool *at boot* is Startup;
  reconnecting *mid-operation* is Runtime; a fixed buffer at launch is Startup,
  per-request alloc is Runtime. **One capability legitimately spans phases** — that
  is the payoff: a DB feature yields *provision the DB* (Provision) → *open the
  pool + migrate at boot* (Startup) → *reconnect on drop* (Runtime), and people
  usually write only the Runtime one.
- **Configuration straddles Provision↔Startup, app-dependently.** Config is
  **Provision** when it *must pre-exist* and the app has no way to obtain it at
  launch; it is **Startup** when the app *can* obtain/validate it at launch (a
  first-run wizard, a clear error, or a default fallback). Capture both the
  *definition* (where the config lives) and the *launch behavior when it is
  missing*.
- **Keep one axis.** Dependencies and config are *subjects*, not phases — a
  dependency is required at Provision but used at Runtime; config must exist at
  Provision, is loaded at Startup, may reload at Runtime. The `Lifecycle` tag on
  the concrete requirement already places it; don't add a second "kind" axis.

**Constants:** `MAX_ROUNDS = 4` per gate (then escalate to the human);
`COVERAGE_THRESHOLD = 80%` line coverage (adjust by agreement; record here).

**Verification methods:** `Test` (automated) · `Demonstration` (run + observe,
e.g. a GUI or a real device) · `Manual` (human procedure) · `Analysis` ·
`Inspection`. Pick the cheapest method that actually establishes the criterion;
don't claim `Test` for something only a human can confirm. The method drives
what `trace.py` requires: only `Analysis`/`Inspection` SRs are exempt from the
LLR requirement (they have no code to decompose; `Demonstration`/`Manual` SRs
still describe implemented behavior, so they keep it), and **every SR needs ≥1
TC row regardless of method** — for human methods the TC records the procedure
(`Automated=No`, usually `Tier=Release`), which is how the release checklist
finds it.

**Test tiers (run cost vs. confidence).** Running the whole suite every iteration
gets untenable as a project grows (and CI has time/quota limits), so each
`TC-###` carries a **`Tier`**: `Smoke` (fast, run every iteration / on every
push), `Full` (the pre-merge suite, run on PRs), `Release` (slow, hardware,
manual-adjacent, or long-running — run at `G-Release`). Tiers are cumulative:
`full` includes smoke, `release` includes both. The harness selects a tier
(`check.py --tier`) via pytest markers, with a safe default: an **unmarked test
runs in `full` and `release`**, so a forgotten marker can never silently drop a
test from the pre-merge suite — `smoke` is opt-in, and marking `release` opts a
test out of pre-merge. The `Tier` column is the source of truth. Keep at least
the critical paths in `Smoke` so the cheap gate still catches regressions; the
coverage threshold is enforced at `full`/`release` only (the smoke subset alone
isn't expected to meet it).

**Dimensional coverage (exercise the input space, not just the happy path).** A
requirement with variable inputs is rarely satisfied by one example test. Treat
each variable input as a **dimension** and test deliberately, because defects
cluster in two places: at the **boundaries** of each dimension and in the
**interactions** between dimensions.

1. **Per dimension — pick the values that matter, not arbitrary ones.**
   - *Boundary-value analysis (BVA):* for any range, test the **min and the
     max**, and the **degenerate** boundaries — empty, zero, one, single-element,
     and the largest allowed. These catch off-by-one, overflow, and empty-input
     bugs. For inputs with validation, also test **just outside** each bound (the
     first invalid value) as its own — often error-path — case. These invalid
     cases assert *rejection*, not the SR's acceptance criteria, so design them
     by hand as their own TCs; `gen_cases.py` combines over the valid space only.
   - *Equivalence partitioning:* for a set of discrete modes/types, test **one
     representative per class** (classes that the code treats differently), not
     every literal value.
2. **Across dimensions — choose a combination strategy by risk and cost.** The
   full Cartesian product exercises every interaction but grows as `k**d` and
   becomes untenable; don't default to it. Decide per requirement:
   - **Full product** — when the combination count is small (rule of thumb ≤ ~12)
     **or** the interaction is high-risk (data loss, corruption, security, money)
     *and* each case is cheap.
   - **Pairwise (all-pairs)** — the default for ≥3 dimensions: cover every pair of
     values across every pair of dimensions at least once. Empirically catches the
     large majority of interaction defects for a small fraction of the cases.
   - **Boundary-corners** — when even pairwise is too costly or each run is
     expensive (hardware / integration): all-low, all-high, and each dimension
     flipped to its other extreme (single-factor sweeps that localize the failing
     dimension).
3. **Balance against time/complexity via the tiers.** Cheap pure-core
   combinations (unit level) can afford full/pairwise and live in `Smoke`/`Full`;
   expensive integration/hardware combinations use boundary-corners and live in
   `Release`. Don't run a 4-mode × N-size sweep on every push — push the heavy
   combinations to the release tier and keep a boundary slice in smoke.

Record each requirement's dimensions in the SR **`Permutations`** column using
this grammar, so one SR stands in for many near-duplicate rows and the intent is
machine-readable:

```
field=set{plain,comma,quote,newline}; size=range[0..2GiB]; enc=set{utf8,utf16}; @pairwise
```

`scripts/gen_cases.py` reads exactly that grammar and emits the derived value sets
and the chosen combinations (and shows the reduction vs. the full product) — copy
its output into `Parameters` cells / parametrized tests. The generated cases are
the source; do not hand-curate combinations the generator should produce.

## 5. Verdict & status protocol

Reviews append to `status.md`:

```
### <HAT or REVIEWER> — <Gate> — Round <r> — <YYYY-MM-DD>
Verdict: APPROVE | CHANGES-REQUESTED
Findings:
- [BLOCKER|MAJOR|MINOR] <ID or area> → <issue> → <suggested change> → @<owner>
```

Gate sign-offs live in the **Gate Sign-offs** table; the driver records the gate
decision and pauses for the human.

**Voice policy — warmth has a layer boundary.** Personality is a human value, not
a machine one: **human-facing** output (CLI narration, a kickoff greeting, a
release-checklist intro) may carry warmth and **dry wit at most**;
**machine/agent-facing** output — this protocol's findings and verdicts,
subagent prompts, registry cells, commit messages — stays **literal, terse,
structured: no whimsy**. Levity there costs tokens, reads ambiguously to the
next agent (irony/understatement is exactly what a parser misreads), and
erodes the honesty/severity signal this protocol depends on. Default voice is
**restrained**
("direct and concrete; dry wit at most; never at the expense of clarity or
honesty"); a project may expose an optional, named **tone knob** to dial levity
up or down — never a baked-in persona, since no single tone fits both a
medical-device repo and a game studio.

## 6. Review-depth triage (efficiency)

- **High-risk** (security, data loss, crash-safety, money, irreversible, gate
  closure): spawn an **independent** reviewer with a fresh-context, defect-
  hunting prompt. Verify its file edits; never trust an unverified "green."
- **Medium**: self-review against the gate checklist + run the harness.
- **Low/mechanical** (rename, doc tweak, config): just run the harness.

Keep the status file's *Current State / Open Items* header short so a reviewer
can orient cheaply; the full log lives below and need not be re-read each pass.

**Model/agent tiering — recommend + record, not enforce.** The risk triage above
is also a **tiering** axis: planning, decomposition, decisions, and high-risk
review need a **strong model**; mechanical execution, well-specced builds, and
low-risk/prose work tolerate a **cheaper tier**. Tiering down is **safe
specifically because of the gates** above — the harness + tests mean a cheaper
executor can't silently drift past a check, a guarantee an ungated workflow can't
make. The kit **cannot force** a model choice (a fast-moving, host-specific
concern); it offers a **recorded-tier-hint** convention instead: any planned
unit of work (a thread, a phase, a `status.md` task) may carry a **model-tier
hint** — metadata an agent reads and may act on, guidance like any other
`AGENTS.md` directive, not a guarantee. Host-specific levers (e.g. a
strong-model-plans/cheaper-model-executes mode, per-subagent model overrides,
a model-selection command) are optional, documented per-host examples — name
the pattern, never a vendor-specific model-selection engine.

## 7. Harness contract (wire to your stack)

`scripts/check` (and the CI workflow) must run, and fail nonzero on any failure:
format check · linter (warnings as errors) · unit + integration tests · coverage
(≥ threshold) · the traceability check (0 orphans for the active gate). Emit the
coverage + traceability reports as artifacts. Prefer a generated architecture
map step so `architecture.md` stays current.

**Two check layers — process vs. product.** The harness runs two kinds of check,
and naming the split is what keeps the kit portable across stacks:

- **Process checks are kit-owned and stdlib-only** (`requires=()` in `check.py`):
  traceability (`trace.py`), design-flow validation (`check_flows.py`),
  doc navigability (`check_docs.py`), perf-budget comparison (`check_perf.py`), and
  architecture-map freshness (`gen_arch_map.py`). They are identical in every
  project and every language — **don't rewrite them.** (The perf *comparator* is
  process; the *measurement* that feeds it is product — see §9.) They are the
  universal floor the agent-neutral `pre-commit` hook also enforces
  (`.githooks/pre-commit`, enabled by `scripts/setup.{sh,ps1}`).
- **Product checks are project-owned and language-specific** (`requires` names a
  tool — `ruff`/`pytest` in the Python reference): format, lint, and
  tests+coverage. **You wire these to your stack** in `check.py`'s "EDIT FOR YOUR
  STACK" block; a non-Python project swaps the commands or drops a step it lacks.

The empty-vs-named `requires` tuple already implies which layer a step is in;
`check.py --list` makes it explicit, tagging each step `[process]`/`[product]` so
a newcomer sees at a glance which steps are fixed and which they must localize.

**A third toolchain layer — the developer workstation.** The two layers above
cover what the *project* needs to pass its own gates. A third, often-conflated
concern is what a **human** needs to view, render, edit, and run any of it at
all: a language/runtime, `git`, an **offline** Markdown+Mermaid renderer (e.g.
VS Code's preview, or `@mermaid-js/mermaid-cli`), and optionally an IDE or a
domain-specific viewer (CAD/image/publication tooling). "No required tools" was
always a claim about the **process** layer (stdlib only); it never meant a human
needs nothing. Naming this third layer resolves the conflation between
"procurement for the product" and "procurement for developing the product."

**The onboarding ladder — Provision-for-development, applied to the act of
developing itself.** A fresh contributor's path to a running checkout mirrors
the §4 lifecycle phases, one level up:

```
Stage 0           →  dev-setup       →  setup          →  check
get git + repo        workstation        product deps      run gates
(pre-clone)           (post-clone)       (venv/tools)       (exists)
```

`Stage 0` and `dev-setup` provision the **developer workstation** above (rare,
once per contributor); `setup` provisions the **product toolchain** (recurs per
clone/CI run); `check` is the **process** floor that already exists. Each rung is
an optional, readable, **consent-first** helper — never a silent or compiled
installer — so a contributor (including a non-code one, whose deliverable is
still a reviewable git change) can go from a bare machine to an editable,
testable checkout without needing prior git literacy.

**Offline-render principle.** Legibility artifacts (the Mermaid diagrams, the
trace HTML map, the code map) must render with **local, offline** tooling —
never a cloud rendering service — the same reason the kit chose
Mermaid-in-Markdown (§3) in the first place. Point contributors at a local
renderer; reach for a Kroki/PlantUML *container* only if a project genuinely
outgrows Mermaid.

**The kit generates legibility; it does not score it.** The harness *builds* the
traced spine, the committed code map, and the gates, so a repo scaffolded from
this kit should score well **by construction**. *Measuring* that legibility over
time (AI-readiness, complexity/churn dashboards, doc-navigability scores) is a
separate, deliberately **external** concern — run an **external readiness
assessor** (e.g. a deterministic codebase-scoring tool) as **optional downstream
tooling**, never a kit dependency. This is the same stance the kit takes on
`ruff`/`pytest`: it names the gate; the project picks the tool. Generate here;
measure there.

**The kit is a spec; a turnkey agent-runtime harness is a different layer.**
This kit is a stack-agnostic, stdlib, agent-neutral process **spec** you copy
into a repo. A **turnkey agent-runtime harness** — e.g. an `npx`/Node-installed
engine shipping skills/agents/hooks/MCP for one tool, with deterministic
verification gates, model-tiered subagents, and a project-context layer — is a
different, installed **product** a downstream shop may run *in addition*. They
**compose** (a repo scaffolded from this kit can be driven by such a harness)
but neither depends on the other: a runtime harness is optional, tool-specific,
downstream tooling, never a kit dependency. Its "back every verdict with a
deterministic gate" stance is the same one §6 already takes — the philosophical
fit is real, the dependency isn't.

Ready reference scripts ship with this template (Python 3.8+, stdlib only — no
pip needed to run them):

- `scripts/check.py` — the harness itself. Gate-scoped (`--gate G2|G3|all`), runs
  format · lint · tests · coverage · traceability · arch-map freshness, and exits
  nonzero on any failure. Wire it to your stack by editing the step list its
  `steps()` function returns (and the `SRC`/`TESTS`/tool names in the "EDIT FOR
  YOUR STACK" block at the top); the contract is the gates + exit code, not the
  specific tools. CI runs the same command (`ci/check.yml`).
- `scripts/trace.py` — joins the registries, writes `docs/test/report.md` (the
  counts, the SR→LLR→TC matrix, a line-reviewable `SN→SR→LLR→TC` **text
  outline**, and a small **Mermaid `graph LR`** colored by orphan/draft state),
  and exits nonzero on orphans with `--strict`. `--html` additionally writes a
  dependency-free, collapsible `docs/test/report.html` map of the full graph that
  scales to any size (a gitignored composite artifact — see "Reviewability" in
  §3). It also always checks **integrity**
  (duplicate or malformed ids). `--require-verified` adds the G3 status
  criterion (every `Verification=Test` SR must be `Verified`); `--phase v1`
  scopes that criterion for phased delivery (§4), reporting out-of-phase SRs as
  explicitly deferred. `--no-placeholders` rejects any leftover `-000` template
  row (so a scaffold can't pass a gate unfilled); `--strict-schema` requires the
  non-empty fields and the two closed vocabularies (`Verification`, `Tier`) the
  method defines — `Priority`/`Status` are intentionally left open. Called by
  `check.py` at G2/G3: the G2+ run adds `--no-placeholders`; the G3 run adds
  `--require-verified` and `--strict-schema` (plus `--phase` when given).
- `scripts/check_flows.py` — verifies the authored **"Runtime flows"** section
  (§3 "Design-time runtime flows"): present, ≥1 Mermaid diagram, every cited
  SR/LLR id real. Run by `check.py` at G2/G3.
- `scripts/check_docs.py` — **doc navigability** (§3 "The doc set must stay
  navigable"): parses the docs' link graph and fails on broken intra-repo links
  (missing file or `#anchor`), warns on orphan docs (and, with `--stale`,
  git-gated freshness). Stdlib-only; run by `check.py` from G1 on.
- `scripts/check_perf.py` — the **perf-budget comparator** (§9): compares the
  product-emitted `perf-metrics.json` against `performance-budgets.csv` and the
  committed `perf-baseline.json` — absolute breach (vs `Budget`) and regression
  (vs baseline ± `Tolerance`), warn-vs-fail per the row's `Gate`, tier-scoped —
  and writes the gitignored `perf-report.md`. `--update-baseline` accepts a move.
  Stdlib-only, metric-agnostic; run by `check.py` at G3 (absent metrics skip).
- `scripts/check_stubs.py` — the **no-stub / substance** tripwire (§4 G3): lists
  public symbols whose body is a stub (`pass` / `...` / `raise NotImplementedError`
  / bare `return None` / docstring-only), writing the gitignored `stub-report.md`.
  Stdlib, but **product-layer, not process** — a stub's shape is language-specific,
  so it ships like the perf *meters*: **opt-in and warn-first** (exit 0 unless
  `--strict`), **not** wired into `check.py`'s required floor. A Python project runs
  it to inform the G3 Inspection; a non-Python stack swaps or drops it.
- `scripts/gen_arch_map.py` — regenerates the module/function map in
  `architecture.md` from the source tree (and surfaces `Implements:` back-links),
  plus the Mermaid **dependency diagram** between its markers; `--check` fails
  when the doc is stale, so neither can drift. `--strict-parse` additionally
  fails on any module that won't parse (the G3 run passes it).
- `scripts/gen_release_checklist.py` — generates the human **release checklist**
  for `G-Release` from the registries: every Demonstration/Manual/Inspection SR,
  every Release-tier/manual TC, the SN acceptance intents, and provided
  interfaces — each a tick-box back-linked to its id. Keep the completed copy as
  the sign-off record.
- `scripts/gen_cases.py` — expands an SR's `Permutations` (input dimensions) into
  boundary-aware test combinations by strategy (full / pairwise / boundaries),
  and reports the reduction vs. the full product (see "Dimensional coverage" in
  §4). Use it at G2 to design test cases that exercise the input space.

**Cross-platform launchers** (so a fresh clone is trivial to run on any OS):
`scripts/setup.{sh,ps1}` create a venv and install the toolchain;
`scripts/check.{sh,ps1}` are thin wrappers that forward to `check.py`. Provide
the pair for every platform the project supports.

`scripts/bootstrap.py` scaffolds all of the above (plus `docs/` and CI) into a new
repo in one command. See `EXAMPLE.md` for a complete worked SN→SR→LLR→TC chain.

## 8. Cross-project interfaces (only when projects interlink)

When this project provides or consumes a contract shared with another repo,
record each shared surface once in `requirements/interfaces.csv` as an `IF-###`
(see `INTERFACES.template.md`): direction, counterpart, contract, the `SR-Refs`
that realize/rely on it, version, and stability. The owning (`Provides`) side
holds the authoritative spec; the consuming side links the same `IF-###` and
pins the version. Every interface is backed by an SR and a contract/fixture test.
This keeps interlinked projects from silently drifting apart without imposing a
multi-repo build system. Standalone projects skip this section.

## 9. Non-functional requirements & performance budgets

The `SN→SR→LLR→TC` spine verifies **behavior**; on its own it never prompts the
**cost** of that behavior — performance, memory, artifact size, reliability,
security. Non-functional requirements (NFRs) are expressible as ordinary SRs, but
nothing makes you *consider* them, and quantitative budgets often aren't the
author's to invent: a module that is one part of a larger system is *handed* a
slice of a system-level budget by an integrator, and most metrics should be
**minimized within reason**, not pinned to a number the author guessed.

**Consideration checklist (a prompt, not a mandate — don't wear a hat the scope
doesn't need).** At G1, consider which categories apply and route each to a home
(anchor: the **ISO/IEC 25010** product-quality model):

- performance efficiency (time, throughput) and resource use (RAM/VRAM, disk);
- reliability / availability / recoverability;
- **security** (authn/authz, data protection, secrets, audit, dependency / supply-chain);
- **observability / operability** (logging, metrics, tracing, health — also the
  prerequisite for *measuring* any of the budgets below);
- scalability / capacity; compatibility / interoperability;
- portability / installability (incl. artifact size); compliance / legal / licensing;
- safety (cyber-physical); data integrity / durability.

The kit already covers some — **don't double-prompt**: maintainability (= the core
discipline), usability (= the end-user lens), basic fault tolerance (= the
edge-case table and the SN edge cases), cross-project contracts (= `IF-###`, §8).

**Three homes — route by nature:**

1. *Allocation / coordination* NFRs (perf budgets, capacity, availability targets)
   → the **`performance-budgets.csv`** registry below.
2. *Behavioral* NFRs (security, observability, safety, data integrity) → ordinary
   **SRs** with measurable `AcceptanceCriteria` + honest `Verification`, owned by a
   domain hat (Security, SRE/Ops, …).
3. *Hard external limits* (compliance, supported platforms) → `status.md`
   constraints.

**The performance-budgets registry (`requirements/performance-budgets.csv`,
`PB-###`).** Quantitative perf/resource budgets live **separate from the spine**,
the same way cross-repo contracts do (`IF-###`, §8), so `SN→SR→LLR` stays
functional-focused and an **Integration/Coordination** hat (§1) can (re)allocate
budgets across modules without churning the functional breakdown. A module ships
provisional, self-measured budgets; the integrator sets the real allocation.
**Separation is not disconnection:** every budget row **back-links** the SR / LLR /
Module it bounds (its `Refs`), and `trace.py` flags a row whose `Refs` name an
unknown id or whose `PB-` id is malformed. Columns: `PB-ID, Metric, Refs, Budget,
Unit, Tolerance, Direction (lower-better | higher-better), Tier, Gate (fail |
warn), Owner, Notes`. Standalone projects with no resource concerns skip this
section, exactly like §8.

**Tracking the numbers over time — the comparator (`scripts/check_perf.py`).** A
captured budget is inert until something compares the *measured* number against
it. That comparison answers two distinct questions per metric: **absolute** —
"worse than the budget?" (measured vs `Budget`, per `Direction`) — and
**regression** — "suddenly much worse?" (measured vs a committed baseline, outside
the `Tolerance` band). The work splits along the §7 **process/product** line:
*measuring* a metric is **product** work the project wires (`/usr/bin/time`,
`tracemalloc`, `nvidia-smi`, a size command, `pytest-benchmark`/`hyperfine`),
emitting a `docs/test/perf-metrics.json` map of `PB-ID → number`; *comparing* is
**process** work the kit owns — `check_perf.py`, stdlib-only and metric-agnostic
(arithmetic over JSON). The kit owns the comparator; the project owns the meters.

- **Three artifacts, three reviewability classes (§3):** `performance-budgets.csv`
  is the tracked source of truth; `perf-baseline.json` is a **committed golden**
  updated *deliberately*; `perf-report.md` is a **gitignored composite** (current
  vs baseline vs budget + deltas), regenerated each run and published by CI.
- **Baseline-as-golden protocol.** Accepting a regression = committing a new
  `perf-baseline.json` **in the same PR**, so the number move is explicit and
  reviewed — never silent (the same discipline as the coverage threshold and
  phase-deferred SRs). `check_perf.py --update-baseline` rewrites it from the
  current metrics for exactly that purpose.
- **Warn-first; start with the deterministic metrics (honest-gate rule, §4).** The
  per-row `Gate` decides fail-vs-warn and `Tier` decides *when* a row is in scope:
  gate the **low-noise, deterministic** metrics (artifact/binary size, dependency
  count) at `full`; default **noisy runtime** metrics (latency, peak RAM, VRAM,
  throughput) to `Gate=warn` at `release`, with tolerance bands and same-runner /
  best-of-N measurement. A number that can't be a reliable `Test` gate is
  warn-tracked or `Demonstration`, never faked into a binary gate. A budget with no
  measurement this run is skipped, like a missing tool — absent metrics never fail.

## 10. Project scale — one module, several modules, several repos

Everything above (§1–§9) assumes the common case: **one module in one repo**, and
that is the default. Scale is an **escalation ladder** — climb a rung only when the
scope genuinely forces it, decide the rung **at project creation**, and bias to the
lowest one, because each higher rung buys coordination cost a single module never
pays:

1. **One module, one repo** — the default for almost every project. The whole
   `SN→SR→LLR→TC` spine, one gate run, one release.
2. **Several modules, one repo** — when a repo grows distinct sub-systems that still
   **build and release as one** (this section).
3. **Several repos + a coordinator** — only when modules genuinely need *independent*
   versioning, ownership, access, or release cadence at a scale one repo can't
   sustain. A heavier, deliberately **rare** step with its own coordinator role,
   documented separately (the multi-repo model); you almost certainly don't need it,
   and a reviewer should push back on a premature jump. It is **revisitable** — start
   single and promote a module to its own repo *later*, once it proves it needs the
   independence, which is far cheaper than a speculative split.

**Several modules in one repo — no new machinery, just partition the spine.** A
multi-module repo is the *same* spine, grouped by columns that already exist: the
LLR **`Module`** column and the optional **`Area`** tag on SR/TC (§1 "Domain
hats"). Each module is a sub-tree of `SN→SR→LLR→TC`; where a module needs its own
discipline it gets its own **domain hat** owning that slice (§1 already allows
this). The repo still builds, gates, and releases as a whole.

- **Module-scoped review is a convention over the existing columns, not a new
  flag.** A module owner reviews their slice by filtering the registries on
  `Area`/`Module` (a grep or spreadsheet filter); the **repo-level gate stays the
  source of truth** — `trace.py --strict` still requires **0 orphans across the
  whole repo, seams included**. The kit deliberately ships **no** `--module`/`--area`
  filter on `trace.py`/`check.py`: a per-module gate would either hide the
  cross-module seams (a false "green" masking exactly the integration gaps this
  method wants first-class) or need real machinery to tell a legitimate seam from an
  orphan. The whole-repo gate already spans every module; per-module *ownership* is a
  reading convention, not a gate of its own.
- **Integration TCs for the seams.** A module boundary is where two parts must
  agree, so it gets its **own** TCs — not merely each module's internal unit tests.
  These are integration/system-level, usually `Tier=Full` or `Release` (§4 "Test
  tiers"), so the seam is a tested contract rather than an untested gap between two
  individually-green modules.
- **`IF-###` applies *within* a repo, too.** The interface registry (§8) is not only
  for separate repos: two modules in one repo that share a contract record it as an
  `IF-###`, with the counterpart naming the **other module** instead of another
  repo and both rows living in the one `interfaces.csv`. Same
  direction/owner/version/stability discipline, same "one contract, one home, backed
  by a test" rule — applied to the internal seam, with no cross-repo build machinery.
