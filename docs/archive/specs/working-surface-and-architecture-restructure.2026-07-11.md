> **ARCHIVE** — design history as of 2026-07-11; not current guidance.

# Working-surface SSOT + architecture-connectivity restructure — PLAN

> **ARCHIVED 2026-07-11 — campaign complete.** This was the spec-of-record for
> work items **WI-053, WI-054, WI-055, WI-056, WI-057, WI-058, WI-059** (all
> `done`; deliverables in `docs/requirements/work-items.csv`, session record in
> `docs/log.md`). Archived per the S0 #2 ruling: close date appended to the
> filename, attributed WIs named here. The deferred backlog rows it spawned
> (WI-060…WI-065) carry their own live SpecRefs.

**Status:** 🟢 **RULED — every open decision settled by the owner
(2026-07-10; see "Consolidated rulings").** Not yet scheduled, no code written;
ingests as `WI-053…` when the campaign is scheduled, bundled with the pending
G3 re-attestation (the campaign ruling). **S8** (heterogeneous
implementer/reviewer scheduling) was added and ruled the same day — see its
rulings block. This is the spec-of-record for the
`S0…S8` work-item series. It deliberately lives in `docs/specs/` and is the
**first inhabitant** of that directory — dogfooding the `SpecRef` convention it
defines (S1).

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
5. ✅ **Allow both** (ruled 2026-07-10): one file per standalone WI, or a
   shared campaign doc with `#anchor` for a series. (Sessions↔WIs is
   many-to-many — a WI spans sittings, one sitting may close several WIs — so
   the spec is the cross-session memory either way.) Plus the **Done-when
   checklist** convention: the scaffolded per-WI spec template carries a
   Done-when list and sessions tick items as they land, so a half-complete
   WI's frontier is the **first unticked box**, not prose discipline (ticks
   are transient working state — the spec archives at close). A shared
   campaign doc archives, date-stamped and WI-attributed, when its **last**
   open WI closes.

## S1 — Mechanize the SSOT — ✅ DONE (2026-07-10)

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
  The `WI-000.md` example ships the **Done-when checklist** (S0 ruling #5) —
  the frontier of a half-complete WI is its first unticked box.

**Tests.** open WI with a Deliverable fails R-A; a `done` id in status.md fails
R-D; an open WI with an empty/dangling SpecRef fails R-E; a compliant registry +
status.md passes; placeholder-only is vacuous.

**Spine impact.** Extends **SR-037** (work-item registry validation) — its text
grows to cover the status↔registry coherence rules → **re-attestation**.

**Done-when.** A non-compliant meta state fails `check_trajectory --strict`; the
scaffold ships the `SpecRef` column + `docs/specs/`.

## S2 — Meta-repo compliance — ✅ DONE (2026-07-10)

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

## S4 — Codename discipline — ✅ DONE (2026-07-10)

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

## S5 — Architecture-connectivity mechanize — ✅ DONE (2026-07-11)

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

## S6 — Meta-repo authoring (the dogfood) — ✅ DONE (2026-07-11)

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

## S7 — Cross-agent skill sync (checked fan-out from one source) — ✅ DONE (2026-07-11)

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

**Ruling — track vs. regenerate the copies. ✅ CONFIRMED (owner, 2026-07-10):
tracked + drift check**, applied uniformly to **all** per-agent dirs
(`.claude`/`.agents`/`.gemini`). Rationale: while the copies are byte-identical,
tracked-plus-freshness-gate is the kit's own idiom for committed generated
artifacts (arch map, `PROJECT_STATE.html`, OKF), and a fresh clone has working
skills before setup ever runs. **Revisit trigger, recorded:** the day a skill
needs an agent-specific frontmatter field, fan-out gains the per-agent
transform and the model flips to gitignore + regenerate-on-setup — tracking
*transformed* artifacts invites hand-edits, the rot class the kit exists to
prevent.

**Risk.** The frontmatter-dialect boundary above; and a re-materialize that
force-overwrites must touch **only** the skills subtree, never project-authored
files.

**Done-when.** An out-of-sync per-agent copy fails the check; `bootstrap
--agents` populates `.agents/` from source; the meta-repo's three targets are
byte-identical to source (the current `session-protocol` drift resolved).

## S8 — Heterogeneous implementer/reviewer scheduling *(✅ DONE 2026-07-11)*

**Status: ✅ DONE (2026-07-11; WI-059).** Ruled 2026-07-10 (research-backed) and
landed 2026-07-11 — see the ticked Done-when checklist below; the rulings block
closes this section. Provenance: owner direction (separately scheduled
implementer/reviewer sessions; per-job model complexity; cross-**provider**
selection by problem type or review-feedback strength; the provider/model
catalog question) + three research passes condensed in
[`AGENT_ROUTING_RESEARCH.md`](../AGENT_ROUTING_RESEARCH.md). Builds on
the **ratified** `AGENT_ROLES.md` pipeline (`run-phase ∈ {PLAN, BUILD,
REVIEW-A, REVIEW-B, INTEGRATE}`); of its build-calls, `AGENT_CMD_MAP`
(per-phase whole-command routing), `docs/review-policy`, and the status-size
guard have landed — `--prompt-map` and loop-side reviewer dispatch have not.

**Goal.** The coordinator schedules separate implementer and reviewer sessions
across tiers **and providers**; next-round routing is a **declared, legible
policy** informed by mechanically scored review substance; everything stays
stdlib, consent-explicit (no silent swaps), never-breaking.

**The model.**

- **Roles ride `run-phase`** (ratified). New build: loop-side reviewer
  dispatch — after a BUILD session, `docs/review-policy ≥ 1` schedules
  `REVIEW-A` (`= 2` also `REVIEW-B`) before the next BUILD — plus
  `--prompt-map`/`AGENT_PROMPT_MAP` (per-phase prompt templates), the one
  AGENT_ROLES build-call still open.
- **A model registry, not a model catalog** (`docs/agents.csv`; ruled shape).
  One row per usable **model**, keyed **`[PROVIDER]-[MODEL_NAME]-[VERSION]`**
  (`ANTHROPIC-OPUS-4.8`, `OPENAI-GPT-5.2`, `GOOGLE-GEMINI-3-PRO`) — released
  model names are immutable, so these ids are *more* durable than sequential
  `###` ids (unlike iterating repo artifacts). `Provider`/`Model`/`Version`
  stay separate columns (machine truth; the id is the join key, never parsed
  — model names contain hyphens), plus `Tier (strong|medium|weak)`,
  `CmdTemplate` (`{model}`/`{prompt}` slots), `Notes`; id charset uppercase +
  digits + hyphen + dot (dated snapshots and `-PREVIEW` tags are valid
  versions — verified against Anthropic/OpenAI/Google/Meta/Mistral/DeepSeek
  naming). Ships example rows for the verified headless shapes (`claude -p` /
  `codex exec` / `gemini -p`, all JSON-capable). **No vendored model catalog**
  — richer data is a documented pointer to the maintained registries
  (models.dev `api.json`; LiteLLM's model-prices JSON); a `check_vendored`-
  style pinned snapshot is deferred until a real consumer exists.
- **Routing = an enable-list + availability, not per-role maps** (ruled).
  `docs/agents-enabled` lists, in preference order, the registry ids this
  repo may use — the consent surface. Per session the loop selects from that
  **enabled pool** by the phase's tier plus the heterogeneity rules
  (reviewers: two providers, ≥1 ≠ implementer's); a model whose session
  fails to start or stalls out goes on **cooldown** (its limit is probably
  exhausted — the existing rate-limit backoff, generalized per-model) and is
  retried later; when no enabled model of the preferred tier is available,
  the **next tier up** is selected — never a weaker one. Every selection and
  cooldown is logged before launch (the no-silent-swap rule: consent = the
  enabled set + these declared rules). Absent files default to today's
  `AGENT_CMD`/`AGENT_MODEL` — a fresh scaffold pays nothing.
- **Reviewer independence (the evidence-backed core):** reviewers are fresh
  sessions, **two providers, ≥ 1 differing from the implementer's** —
  *preferred, not required*; the reviewer prompt gets the diff + requirements
  and **never the implementer's self-assessment** (leaking it collapses
  finding rates 3–4×); **no debate rounds** — independent parallel reviews,
  mechanical merge. **Degraded availability (ruled):** when only one provider
  is responding, review with what's available — two independent
  **same-provider** sessions are legal. Fresh-context independence is the
  invariant; provider diversity is best-effort (the scorer already weights
  cross-family corroboration above same-family, so a same-provider round
  simply earns a weaker corroboration signal). Verdicts are
  **repo files** in the log.md block format plus one machine line
  (`VERDICT: APPROVE|CHANGES-REQUESTED findings=N`) — exit codes are not
  portable across CLIs; verdict files are, and they fit repo-text-as-memory.
- **The substance scorer** (new stdlib script — the genuinely novel piece:
  review-substance-as-routing-signal has **no published precedent**; keep it
  conservative). Scores a verdict block by **confirmed-finding rate** (a later
  commit touches ± 10 lines of the finding's anchor — change-triggering is the
  canonical usefulness measure), **cross-reviewer corroboration**
  (cross-family matches weighted up), **anchored-finding precision** (anchors
  must resolve; capped), and **actionability rate**. Severity hygiene and the
  anti-gaming tripwires are **gates, never scores**; length never scores
  positively. Scoreboard = one small decayed-tally text file.
- **Fixed escalation policy, not a learned router** (per-project sample sizes
  are far too small for bandits): **win-stay/lose-shift** — the
  higher-substance provider becomes the next round's primary feedback source
  only on a **margin ≥ 2**; the implementer's provider swaps after
  **2 consecutive** failed review gates (a cheap test for idiosyncratic
  failure); tier rises only after the swap also fails; **page the human** on 2
  top-tier failures (the shared-failure regime — the spec is wrong, not the
  model), on opposite verdicts twice running, or on any tripwire (finding-cap
  pinning, near-duplicate review text, implementer diffs touching
  review/policy paths, mass finding-rejection).
- **Failure semantics follow `docs/gate-policy`** (ruled). On a page-the-human
  condition the causing WI **and its hard-edge dependents pause** in every
  mode; what happens next is the declared mode's call — **attended:** start
  nothing new, let in-flight sessions close out, then alert the user;
  **single-ratify:** keep working non-dependent WIs to completion, surface
  the block for ratification; **autonomous:** autonomous means autonomous —
  schedule a fresh **design-check session** (different provider, strong tier)
  to rule grind-through vs. genuine redesign, document every
  assumption/decision, and continue; a redesign verdict re-enters the
  change-intake flow (process.md §5). The escalation constants (margin ≥ 2,
  the 2-round streaks) ship as legible per-repo-overridable defaults —
  calibration values, not spine facts.
- **Existing doctrine preserved.** Every routing decision is *written* (a
  declared file + the iteration log) before the session launches — the
  no-silent-swap rule; the **gate-closure review keeps the strong-model
  floor** — cheap-but-heterogeneous applies to *iteration-loop* reviewers only
  (this narrows the current "reviewer tier never delegated down" wording to
  gate reviews — a PROCESS_OPTIONS text change to rule on).

**Spine impact.** One new SR under SN-006 (unattended operation) for
role-scheduled, registry-routed sessions + the scorer — or extend the loop's
existing SR (an S0-style ruling). Rides the campaign re-attestation if
ingested with S1–S7.

**Risk.** The routing signal is novel and gameable — the tripwires and
margin/streak thresholds are the defense, and the scoreboard stays
**advisory** (the declared policy picks; nothing auto-optimizes). "A
same-provider reviewer is softer on same-provider code" is an inference from
judge-bias literature, not a measured code-review result — run a cheap in-kit
A/B once the loop ships.

**Done-when.**
- [x] `--prompt-map` + loop-side reviewer dispatch land test-first;
      `review-policy` `0|1|2` is enforced by the loop. *(agent_loop managed
      mode, gated on `docs/agents-enabled`; `AGENT_PROMPT_MAP` preflighted;
      tests in test_agent_loop_review.py.)*
- [x] `docs/agents.csv` registry + routing composition land, defaulting to
      today's behavior when absent. *(agent_route.py; enable-list is the
      consent surface + on-switch; absent = legacy behavior byte-for-byte.)*
- [x] The substance scorer lands with the tripwires; the scoreboard file is
      documented. *(score_reviews.py; `docs/reviews/scoreboard.txt`; the four
      tripwires are non-scored gates.)*
- [x] PROCESS_OPTIONS "Unattended operation" gains the routing/escalation
      subsection; the redacted-reviewer prompt template ships. *(embedded
      `REVIEWER_PROMPT` default, `--prompt-map` file override.)*
- [x] The root README's unattended-operation bullet gains the
      iteration-review summary for context (separate fresh reviewer sessions,
      enable-list provider selection, win-stay/lose-shift — no rotation, the
      degraded-availability rule), pointing at the PROCESS_OPTIONS detail —
      the context lands where readers start.

**Rulings (owner, 2026-07-10) — all eight settled:** registry =
`docs/agents.csv` with `[PROVIDER]-[MODEL_NAME]-[VERSION]` ids (model bullet
above); routing = the enable-list + cooldown + tier-up-never-down selection
(bullet above); the scorer ships as **its own script**; the strong-model
reviewer floor narrows to **gate-closure** reviews (iteration reviewers
cheap-but-heterogeneous); **no LLM-judge tiebreaker** — "the math is
arbitrating; we don't need another LLM to do that; none of it will be
perfect"; spine cut = **one new SR under SN-006**; S8 **rides the campaign**,
sequenced last and detachable; failure semantics keyed to `gate-policy`
(bullet above), with the escalation constants as overridable defaults;
**degraded availability** — a single responding provider reviews with what's
available, incl. two independent same-provider sessions (fresh context is the
invariant, diversity best-effort).

---

## Sequencing & spine bundling

```
S0 rulings ─▶ S1 mechanize ─▶ S2 meta compliance
S3 dissolve IMPROVEMENT_PLAN  ✅ done
S4 codename discipline        (docs; any time)
S5 arch mechanize ─▶ S6 meta authoring (dogfood)
S7 cross-agent skill sync     (SR-025; independent of the SSOT/arch halves)
S8 heterogeneous impl/review  (ruled; independent — extends the unattended
                               layer; rides the campaign, sequenced last)
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

- ✅ **S7 tracking: tracked + drift check** (confirmed from interim), uniform
  across `.claude`/`.agents`/`.gemini`, with the revisit trigger recorded — see
  the ruling paragraph in S7.
- ✅ **S8 (added + ruled 2026-07-10):** `[PROVIDER]-[MODEL_NAME]-[VERSION]`
  registry ids, enable-list + cooldown + tier-up routing, own-script scorer,
  gate-only reviewer floor, no LLM judge, one new SR under SN-006, rides the
  campaign, `gate-policy`-keyed failure semantics — see the S8 rulings block.

- ✅ **S0 #5: allow both** — a per-WI file or a shared campaign doc with
  `#anchor` — plus the **Done-when checklist** convention in the scaffolded
  spec template (see the S0 rulings block).

**Still open:** none — the spec is **fully ruled**. Next step: schedule the
campaign (S1 + S5 + S6 + S7, bundled with the pending G3 re-attestation per
the campaign ruling).
