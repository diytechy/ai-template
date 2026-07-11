# Working-surface SSOT + architecture-connectivity restructure — PLAN

**Status:** 🟡 **PROPOSED — for owner review.** Not ratified, not scheduled, no
code written. This is the spec-of-record for a future `S0…S7` work-item series.
It deliberately lives in `docs/specs/` and is the **first inhabitant** of that
directory — dogfooding the `SpecRef` convention it defines (S1).

**Provenance:** consolidates the owner's 2026-07-10 direction on status.md ↔
work-items.csv single-source-of-truth, the ratified AXES component/interface
model (`docs/archive/AXES_AND_WORKSTREAMS.md`), the "software architecture shows
no connections" discussion, and the cross-agent skill-drift finding (`.claude`
vs `.agents` vs the neutral source). Sequenced **after** the pending G3
re-attestation, because S1/S5/S6/S7 touch the spine.

---

## Why (the five problems)

1. **status.md and work-items.csv compete.** Both carry work descriptions;
   they drift (status.md already went stale on WI counts twice this month).
2. **Closed work and codenames leak onto the working surface.** status.md
   accretes finished-item narrative and session-local labels ("the F2 floor
   rule", "B1", "the grind") that only resolve by spelunking archived docs.
3. **Spec-of-record is free-text prose.** A WI's spec lives in its `Deliverable`
   cell as an inline mention; nothing checks that an *open* WI names a reachable
   spec, so a queued item can be un-implementable and no gate notices.
4. **The architecture view shows no connections.** `PROJECT_STATE.html`'s How-SW
   panel lists modules with no edges, because the kit's real seams (subprocess
   calls, file-mediated dataflow) are never declared as interfaces — the `IF-###`
   tier exists in the templates but the meta-repo has zero rows.
5. **Per-agent skill copies drift.** The one neutral source
   (`project-trajectory/skills/`) is fanned out by verbatim copy into per-agent
   dirs (`.claude/skills/`, `.agents/skills/`, `.gemini/skills/`), but the copy
   is write-once and unchecked, so they rot — the `session-protocol` skill went
   **three ways** in one session (source + `.claude` updated, `.agents` left on
   the pre-archive text, `.claude` separately hand-gaining a `--stale` flag).

## The target model — the SSOT rules

Formalized from the owner's direction. **status.md is forward-only; the WI
Deliverable is backward-only.** The bridge between them is a per-WI spec that
lives while the WI is open and is removed at close.

| Rule | Statement | Enforcer (S1) |
|---|---|---|
| **R-A** | A WI's `Deliverable` is non-empty **iff** `Status = done`. An open WI (queued/active/deferred) has an **empty** Deliverable. | check_trajectory |
| **R-B** | Every **open** WI is described in a `status.md` lane (its context); a `deferred` WI additionally carries its **reason**. | check_trajectory (id present) + review (prose quality) |
| **R-C** | `status.md` names the **next/active** WI, which must exist in `work-items.csv` in a non-`done` state. | check_trajectory |
| **R-D** | A `done` WI id **must not** appear anywhere in `status.md` — closed work leaves the working surface. | check_trajectory |
| **R-E** | Every **open** WI has a non-empty `SpecRef` resolving to an in-repo target (`docs/specs/WI-###.md` or a `doc#anchor`); the spec is deleted/archived **at close**, so no plan file can re-grow. | check_trajectory + check_doc_refs (path tier) |

**WI lifecycle under the model:**
`queued` (Deliverable empty · SpecRef→`docs/specs/…` · described in status.md) →
`active` (same) → `done` (Deliverable filled with what shipped · SpecRef cleared,
spec file archived/removed · **absent** from status.md). A `deferred` state is
added to the vocabulary (queued-but-not-next, with a recorded reason).

---

## S0 — Rulings (settle before S1)

Open micro-decisions; each has a working default so S1 can proceed if unruled.

1. **R-A strictness:** hard-fail an open WI with a non-empty Deliverable under
   `--strict`, or warn-only? *(default: warn at commit, fail at G2+.)*
2. **SpecRef at close:** delete the `docs/specs/WI-###.md` file, or move it to
   `docs/archive/specs/`? *(default: delete — git retains history; the
   Deliverable + log carry the summary.)*
3. **R-D scope:** does "referenced in status.md" mean the bare WI id only, or
   also its title text? *(default: the id token — titles are too fuzzy to gate.)*
4. **`deferred` vocab:** add `deferred` as a first-class status, or keep
   `queued` + a `Deferred` lane in status.md? *(default: add `deferred` — it is
   a distinct DAG state, not "next".)*
5. **SpecRef granularity:** one file per WI, or allow a shared spec doc with
   `#anchor` (this plan is one shared doc for S0–S6)? *(default: allow both; a
   `doc#anchor` is a valid SpecRef.)*

**Rulings (owner, 2026-07-10) — four of five settled:**

1. **R-A fails the commit** (stricter than the default). A commit is the agent
   **handoff point** — a fresh session launches from repo text alone, so an
   incoherent WI state (an open WI with a filled Deliverable) launches the next
   session into the wrong work item. The pre-commit floor enforces R-A as a
   **fail**, not a warn.
2. **Archive, don't delete.** At close the spec moves to `docs/archive/specs/`
   with the **close date appended** and must **name the WI it was attributed
   to** (future context). Corollary check (new, S1): a spec that forced design
   iteration means there was a gap somewhere — so a **rework WI that changes no
   part of the validation chain warns**: if neither TC prose nor actual test
   logic changed, the same failure recurs (the fix must land in the chain, not
   just the code). Warn-first; mechanics shaped in S1.
3. **R-D = the bare id token only** (default confirmed).
4. **`deferred` becomes a first-class status** (default confirmed).
5. **Open** — pends the sessions↔WI cardinality framing (many-to-many in
   practice: a WI spans sittings, one sitting may close several WIs; the
   default "allow both" fits that, owner still to rule).

## S1 — Mechanize the SSOT

**Goal.** Turn R-A…R-E into checks so the model holds without discipline.

**Steps.**
- Add a **`SpecRef`** column to `registries/work-items.template.csv` and the
  meta `work-items.csv` (legacy rows without it read as empty — never-breaking).
- Add `deferred` to the status vocabulary in `check_trajectory.py` and the
  template explainer.
- Implement R-A/R-C/R-D/R-E in `check_trajectory.py` by cross-reading
  `work-items.csv` **and** `docs/status.md`: Deliverable-vs-status coherence
  (R-A), the named next WI is open (R-C), no `done` id appears in status.md
  (R-D), every open WI has a resolvable `SpecRef` (R-E). Warn-first; `--strict`
  (G2+) gates. Vacuous on a placeholder-only registry.
- `SpecRef` path resolution rides `check_doc_refs.py`'s path tier.
- Add the **no-validation-delta warn** (S0 ruling #2's corollary): a WI
  addressing a prior failure that changes neither TC prose nor test code
  warns — warn-first, exact trigger (re-opened WI vs. follow-up WI on the same
  SR) shaped here.
- Scaffold `docs/specs/` (a `README.md` + a `WI-000.md` example) in
  `bootstrap.py`; document the layer in PROCESS_OPTIONS "Trajectory / work-items".

**Tests.** open WI with a Deliverable fails R-A; a `done` id in status.md fails
R-D; an open WI with an empty/dangling SpecRef fails R-E; a compliant registry +
status.md passes; placeholder-only is vacuous.

**Spine impact.** Extends **SR-037** (work-item registry validation) — its text
grows to cover the status↔registry coherence rules → **re-attestation**.

**Done-when.** A non-compliant meta state fails `check_trajectory --strict`; the
scaffold ships the `SpecRef` column + `docs/specs/`.

## S2 — Meta-repo compliance

**Goal.** Bring the kit's *own* status.md + work-items.csv into the new shape,
so it dogfoods the rules S1 added.

**Steps.** Backfill `SpecRef` for every open WI (today: only WI-033 active).
Empty the Deliverable of any non-`done` row (none today — all are `done`, which
is itself a smell the audit should note). Strip `done`-WI references and
codenames out of status.md so R-D/S4 pass. Move the still-live deferred backlog
(currently prose bullets in status.md) into `deferred` WI rows with `SpecRef`s.

**Spine impact.** None (data only). **Done-when.** `check_trajectory --strict`
green on the meta-repo.

## S3 — Dissolve IMPROVEMENT_PLAN — ✅ DONE (2026-07-10)

Landed ahead of this plan: `IMPROVEMENT_PLAN.md` archived to `docs/archive/`,
the `session-protocol` skill re-pointed to the live homes (`status.md` +
`work-items.csv` + `log.md`). Recorded here as **superseded** so the series
reads honestly. (Commit `da438f1`.)

## S4 — Codename discipline

**Goal.** Stop session-local labels ("F2", "B1", "Q1", "the grind") from
becoming durable references nobody can resolve later.

**Rule.** *Every durable reference in a registry or spec is a `WI-/SR-/LLR-/TC-`
id or an in-repo path — never a session-local codename.* Codenames may appear in
a `log.md` session entry (ephemeral narrative) but not in `work-items.csv`, the
SR/LLR/TC registries, or `docs/specs/`.

**Steps.** State the rule in PROCESS_OPTIONS + the reviewer charter (a
process/trace-reviewer checklist item). **Optional, deferred:** a narrow lint
in `check_trajectory` flagging finding-codename shapes in durable cells — but
only if a real pattern earns it (naive `[A-Z]\d+` would false-positive on `G3`,
`SR-…`), so this stays a writing rule + review item until it does.

**Spine impact.** None (docs). **Done-when.** The rule is documented and on the
reviewer's checklist.

## S5 — Architecture-connectivity mechanize

**Goal.** Make the architecture view show how modules connect, from declared
`IF-###` interfaces — the seam the AXES ratification already sanctioned ("a
cross-component edge without a declared interface is a finding").

**Model.** One `IF-###` row per **directed seam**: `ThisProject` = the module
path; `Counterpart` = the other module, a **file** (path — giving module→file→
module dataflow), or an external actor (`downstream adopter`, `git`, `agent
CLI`); `Contract` = the one testable line (CLI flags + exit codes, or the file
schema); `Direction` = Provides/Consumes; `SR-Refs` links the spine. A shared
file (`stack.ini`) is a hub node many modules Consume.

**Two refinements.**
- Every module in the arch-map inventory appears as **≥1 IF endpoint** — a
  missing direction **warns** unless the row set marks it a deliberate
  source/sink (the honesty valve, so pure sinks don't breed boilerplate rows).
- IF rows carry `SR-Refs`, so every IF is **transitively TC-covered** via the
  spine; plus a warn that each `Active` IF id is **cited by ≥1 TC** (the rung-2
  seam-TC rule, finally checkable).

**Ruling (owner, 2026-07-10) — the layer is opt-out, not opt-in.** By default a
contract IF must define how the software architecture connects: the
inventory-coverage warn above runs even when `interfaces.csv` has no real rows,
so a multi-module arch-map with an empty IF registry reads **"connectivity
undeclared"** instead of passing vacuously — the How-SW panel stays a bare list
exactly when the seams are undeclared, and the organized graph is earned by
declaring them. A repo with genuinely nothing to declare silences the layer
with the one-word `docs/interfaces-check` = `off` (the
`trajectory-check`/`okf-export` idiom); a single-module inventory is vacuous.
Knock-ons: the views-checker's "vacuous without an `interfaces.csv`" clause
inverts (vacuous only under the off-switch or one module); PROCESS.md §8's
"only when projects interlink" framing widens to *the seam registry* —
cross-project **and** intra-repo (§8 is in the byte-watched core; flag the
delta when it lands); and default-on strengthens the **one-new-SR**
recommendation for the spine cut below.

**Steps.**
- `trace.py`: `IF-###` id integrity (closes the SR-002 gap — trace never read
  the IF tier), `SR-Refs` resolution, and an endpoint↔`LLR.Module` join.
- The views-checker (`check_trajectory`): inventory-coverage + docstring-citation
  + seam-TC-citation **warns** (they run at the hook; all warn-first, vacuous
  without an `interfaces.csv`).
- `gen_trajectory`: render the How-SW panel as a real **graph** — module + file
  + external nodes, IF-labeled directed edges — **reusing the WI-DAG layouter**
  (`_dag_ranks` + barycentre sweeps); keep the symbol table beneath it.
- `gen_arch_map`: merge declared IF edges into the Mermaid diagram, styled
  distinctly from (empty-by-design) import edges.
- Scripts declare seams: a `Contracts: IF-###` docstring line, **harvested like
  the existing `Implements:` tag** (closing the enforcement-audit gap #2).
- Template + docs: `interfaces.template.csv` explainer row; PROCESS_OPTIONS
  "Intra-repo interfaces & the architecture graph" subsection building on §8;
  ADOPTING §6 note. All never-breaking; the layer itself is **opt-out,
  default-on** per the ruling above (scaffold ships `docs/interfaces-check`).

**Spine impact.** Extends **SR-005** (off-spine registries — `IF` joins
PB/PART/ASSET/REPO) and **SR-038** (the dashboard gains the graph clause), or
one new SR — an S0-style ruling. → **re-attestation.**

**Risk.** ~30–35 hand-authored IF rows are a new maintenance surface whose
`Contract` text has no mechanical oracle (a renamed flag the row misses). The
joins bound the rot to that one column; CLI contracts are already pinned by the
never-break-downstream rule.

## S6 — Meta-repo authoring (the dogfood)

**Goal.** Write the kit's own interfaces so its architecture view shows the real
system (check.py as the hub; hooks + agent_loop feeding it; stack.ini + the
registries as shared-contract nodes).

**Steps.** Author `docs/requirements/interfaces.csv` (~30–35 rows: one
Provides-CLI row per script — the downstream compatibility surface, now formal —
plus ~10 shared-file contracts and the subprocess seams). Add `Contracts: IF-###`
docstring lines to every script. Optionally seed `Implements: SR-/LLR-` on the
`CodeSymbol`-named functions (filling the permanently-empty arch-map column).
Regen map/dashboard/OKF; full gate.

**Spine impact.** Data + docstrings; no SR text change beyond S5's.
**Done-when.** How-SW renders the real graph; every module is an IF endpoint.

## S7 — Cross-agent skill sync (checked fan-out from one source)

**Goal.** Keep the per-agent skill copies in lockstep with the one neutral
source, so a cross-agent repo (Claude + Codex + Gemini in the same tree) does
not drift — the intra-agent-compatibility seam. Format is **not** the problem:
all locations use the same Anthropic Agent Skills `SKILL.md` with the kit's
neutral frontmatter (`name/scope/stacks/domains/phases/tags`), so `.claude/
skills/`, `.agents/skills/` (Codex's AGENTS.md-mirror location) and `.gemini/
skills/` are just different **directories holding byte-identical files**, needed
only because agent skill *locations* don't standardize (same reason the kit
keeps separate hook configs). This is a **fan-out/sync** problem, not a compat
one.

**Current state (the drift is live and now tracked).** `materialize_agent_layer`
does a verbatim `shutil.copyfile` but is **write-once** (`if dst.exists() and not
force: continue`), so re-runs never refresh. `bootstrap` targets only
`.claude`/`.gemini`; `.agents/skills/` was created by Codex outside the kit and
committed (5 skills, no `INDEX.csv`/`README`) — its `session-protocol` copy is
already stale vs source.

**Steps.**
- Add **`.agents/skills/`** as a first-class `bootstrap` target (a `codex`/
  `agents` entry in the `AGENTS` dict, `skills_dir=".agents/skills"`), so a fresh
  checkout populates it from the same source instead of an agent doing it by hand.
- Make materialization a **refresh**, not write-once — a `--sync` mode (or force-
  overwrite the skills subtree) so "edit source → re-materialize" is one command;
  keep write-once for the other scaffolded files (never clobber project content).
- Add a **drift check** — `check_skills_sync` (or `gen_skills_index --check`
  extended): every `<agent>/skills/<name>/SKILL.md` is byte-identical to
  `project-trajectory/skills/<name>/SKILL.md`. Warn-first; wired into the
  pre-commit floor + gate like arch-map/okf freshness; vacuous when a repo has no
  per-agent dirs.
- State the tenability constraint: **skill frontmatter stays agent-neutral.**
  Verbatim fan-out holds only while no skill needs an agent-specific field; the
  day one does, materialization gains a per-agent transform (map/strip fields) —
  deferred until a real need earns it.
- Docs: PROCESS_OPTIONS "Skills layer" note + `skills/README.md`; record the
  tracking convention (below).

**Tests.** a hand-edited (drifted) copy fails the sync check; a re-materialize
brings every target byte-identical to source; a repo with no per-agent dirs is
vacuous; `bootstrap --agents codex` populates `.agents/skills/` matching source.

**Spine impact.** Closest existing SR is **SR-025** (skills index generation);
extend it to cover the checked per-agent fan-out, **or** mint one new SR (an
S0-style ruling — recommendation: extend SR-025, same "generated, not
hand-maintained" property). → **re-attestation** if the SR text changes.

**Ruling — track vs. regenerate the copies.** Interim owner decision
(2026-07-10): **tracked** (committed `.agents/` for now), matching how
`.claude/skills/` is handled, *may move to gitignore + regenerate-on-setup*
after iteration. Whichever wins must apply to **all** per-agent dirs
consistently (today `.claude` is tracked, `.agents` newly tracked, and a
regenerate model would gitignore both). The drift check keeps the tracked model
honest; a regenerate model leans on `setup` + the check instead.

**Risk.** The frontmatter-dialect boundary above; and a re-materialize that
force-overwrites must touch **only** the skills subtree, never project-authored
files.

**Done-when.** An out-of-sync per-agent copy fails the check; `bootstrap
--agents` populates `.agents/` from source; the meta-repo's three targets are
byte-identical to source (the current `session-protocol` drift resolved).

---

## Sequencing & spine bundling

```
S0 rulings ─▶ S1 mechanize ─▶ S2 meta compliance
S3 dissolve IMPROVEMENT_PLAN  ✅ done
S4 codename discipline        (docs; any time)
S5 arch mechanize ─▶ S6 meta authoring (dogfood)
S7 cross-agent skill sync     (SR-025; independent of the SSOT/arch halves)
```

**Bundle the spine-touchers.** S1 (SR-037), S5 (SR-005/SR-038 or a new SR), S7
(SR-025 or a new SR), and the already-filed TC-034→Test upgrade all edit the
spine. Landing the spine-touching phases **together before the next
re-attestation** means **one owner sitting** covers them all, instead of several.
That is the strongest argument for doing this as one campaign rather than
separate threads. S7 is independent of the SSOT (S1–S2) and architecture (S5–S6)
halves — it can ride the same re-attestation or ship on its own.

## Consolidated rulings (owner, 2026-07-10)

**Ruled:**

- ✅ **S0 #1–#4** — see the S0 rulings block (R-A **fails the commit** — the
  agent-handoff argument; spec **archived with date + WI attribution** at close
  plus the no-validation-delta warn; R-D id-token-only; `deferred` added).
- ✅ **S5 posture:** the interface layer is **opt-out, default-on** — see the
  ruling block in S5.
- ✅ **S5 spine cut: one new SR**, hung from an **SN stating the
  single-dashboard intent** — reviewing the project's progress *and
  relationships* from one dashboard-like file (root `PROJECT_STATE.html`) —
  and propagating outward (SN → SR → LLR/TC). At ingest, check whether an
  existing SN already states that intent (SR-038's parent); mint the SN if not.
- ✅ **S7 spine cut:** extend **SR-025** (the checked per-agent fan-out is the
  same "generated, not hand-maintained" property).
- ✅ **Campaign, not increments:** land the spine-touchers (S1 + S5 + S6 + S7)
  as **one re-attested campaign**. Generalized (owner): *campaign* is good
  semantics for **any** batch of spine-touching work headed for a
  re-attestation — batch them so one owner sitting covers each; candidate
  PROCESS_OPTIONS language when this series lands.
- **WI ids:** this series is `S0…S7` here; on ingest they become `WI-053…`
  registry rows with this doc's `#anchors` as their `SpecRef` (`WI-050…052`
  were consumed by the 2026-07-10 late batch).

**Still open:**

- **S0 #5 (SpecRef granularity)** — pends the sessions↔WI cardinality framing
  (see the S0 block).
- **S7 tracking:** tracked (interim ruling stands) vs. gitignore + regenerate,
  applied uniformly to `.claude`/`.agents`/`.gemini`.
