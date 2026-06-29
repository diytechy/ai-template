# Kit Improvement Plan

Derived from `TEMPLATE_REVIEW.md` (resolved 2026-06-28) plus follow-on design
threads and a cross-agent-portability decision. This file is the **spec a
fresh session implements from** — each thread is self-contained with Goal /
Steps / Tests / Risks / Done-when. Keep it updated as threads land (check items
off; record deviations).

Branch: `template-review-fixes` (the review fixes are already committed here).

Guiding constraints (from `CLAUDE.md`): kit scripts stay **stdlib-only, Python
3.8+, cross-platform**; **dogfood single-source-of-truth** (state a fact once,
link to it); **edit conservatively**; after any script change run
`python -m pytest -q` and paste real output; flag anything that forces downstream
repos to migrate.

---

## Thread 0 — Cross-agent portability (do first; foundational)

**Why first:** it reshapes where the agent guide and enforcement live, which the
other threads then target. The kit's substance (process, registries, scripts,
harness, CI) is already agent-agnostic; only the thin agent-facing skin needs
work. Verified landscape (2026): `AGENTS.md` is the cross-tool standard (Linux
Foundation; 28+ tools). Claude Code reads it (prefers `CLAUDE.md`); Codex reads
it (not `CLAUDE.md`); Gemini still prefers `GEMINI.md` with weaker `AGENTS.md`
support (~12k-char cap). Hooks do **not** standardize: Claude `.claude/settings
.json` (~12 events), Gemini `.gemini/settings.json` (~10), **Codex has no hooks**
(policy + OS sandbox). ⇒ standardize the *instructions file* on `AGENTS.md`; put
*enforcement* in the agent-neutral substrate (git hooks + CI), not agent hooks.

### 0a — `AGENTS.md` as the canonical agent guide

**Status: ✅ landed 2026-06-28.** Deviations from the spec as written: the code
map was *already* routed at `AGENTS.md` in `gen_arch_map.py`, `check.py`, and
`ARCHITECTURE.template.md` (a prior thread), so only a stale `gen_arch_map.py`
docstring line (`CLAUDE.template.md` → `AGENTS.template.md`) needed fixing. The
optional dogfood (meta-repo `AGENTS.md` stub → its `CLAUDE.md`) was added. The
renamed guide's own self-references (title, "copy this as", closing note) were
updated even though the plan said "unchanged content" — leaving them would have
been incorrect.

- Rename the content home: `project-trajectory/CLAUDE.template.md` →
  `project-trajectory/AGENTS.template.md` (full guide, unchanged content + the
  Thread-3 edits).
- Add thin per-agent stub templates that point at it (single source of truth):
  - `project-trajectory/CLAUDE.stub.template.md` — one short paragraph: "The
    agent guide for this repo is `AGENTS.md`; read it first." (Claude reads
    `CLAUDE.md` natively, so the stub guarantees it lands there.)
  - `project-trajectory/GEMINI.stub.template.md` — same, kept as a *real* file
    (not a symlink) because Gemini's `AGENTS.md` support is weakest. (No
    symlinks anywhere — fragile on Windows.)
- `bootstrap.py` MAPPING: create `AGENTS.md` (from `AGENTS.template.md`),
  `CLAUDE.md` (from `CLAUDE.stub.template.md`), `GEMINI.md` (from
  `GEMINI.stub.template.md`). **Decision:** create all three unconditionally —
  they're tiny and cost nothing (same rationale as always-copying interfaces).
- Route the generated code map at `AGENTS.md`: update the `gen_arch_map.py`
  docstring examples and the harness `--doc` guidance to mention `AGENTS.md`
  (the script is already target-agnostic; `--doc` is repeatable, no code change).
- Update every cross-reference from "CLAUDE.md (agent guide)" to "AGENTS.md
  (with CLAUDE.md/GEMINI.md stubs)": `README.md`, `project-trajectory/README.md`
  (contents table + How-to-use), `PROCESS.md`, `bootstrap.py` docstring,
  `KICKOFF_PROMPT.md`, and this repo's own `CLAUDE.md` repo-map. **Grep `CLAUDE`
  across the repo and reconcile each hit.**
- Optional (dogfood): give the meta-repo its own `AGENTS.md` stub pointing to its
  `CLAUDE.md`. Low priority; note only.

**Tests:** update `tests/test_bootstrap.py` (`test_scaffold_contains_expected_files`)
to expect `AGENTS.md` + `CLAUDE.md` + `GEMINI.md`; add an assertion that the
stubs reference `AGENTS.md` and that `AGENTS.md` carries the full guide. Grep the
test suite for `CLAUDE.md` and fix references.

**Risks:** wide but mechanical doc churn; a missed reference leaves a dangling
"CLAUDE.md". Mitigate with the grep sweep + the bootstrap file-list test.

**Done-when:** bootstrap yields `AGENTS.md` (full) + `CLAUDE.md`/`GEMINI.md`
(stubs); no doc calls `CLAUDE.md` the canonical guide; `pytest -q` green.

### 0b — Agent-neutral enforcement via git hooks

**Status: ✅ landed 2026-06-28.** `hooks/pre-commit` added (interpreter discovery
matches `setup.sh`; runs `gen_arch_map.py --check`, `trace.py --strict`, and
ruff-format on staged `.py` only if ruff is importable — detected the same way
`check.py` does). Wired opt-in in both setup launchers and via bootstrap MAPPING
(`.githooks/pre-commit`, executable on POSIX). Optional `agent-hooks/`
(`claude.settings.json`, `gemini.settings.json`) ship with a README caveat. Tests
in `tests/test_pre_commit_hook.py` cover the underlying checks, copy, and an
end-to-end `sh` run where a shell is available, plus JSON validity of the extras.

- Add `project-trajectory/hooks/pre-commit` (`#!/bin/sh`; Git-for-Windows runs
  hooks through its bundled sh, so one POSIX hook is cross-platform). It must:
  - find the interpreter the way `setup.sh` does (`python3` then `python`);
  - run only the **fast, always-valid process checks** so it never blocks a
    legitimate early-stage commit: `gen_arch_map.py --check` (stale generated
    block ⇒ blocked = the "protect GENERATED regions" guarantee), `trace.py
    --strict` (orphans/duplicate/malformed ids), and `ruff format --check` on
    changed files **iff ruff is importable** (skip silently if not — product
    tooling is optional at this layer).
  - **Do NOT** put `--no-placeholders` / `--strict-schema` / full tests here —
    those are gate-scoped (`check.py`) and belong in CI, or they'd block valid
    G0/G1 commits. Pre-commit = the universal process floor; CI = the full bar.
- Wire it opt-in and reversibly: `setup.sh`/`setup.ps1` run
  `git config core.hooksPath .githooks` (documented, undo = `git config --unset
  core.hooksPath`). bootstrap MAPPING: `hooks/pre-commit` → `.githooks/pre-commit`
  (chmod +x on POSIX, like the `.sh` launchers).
- Ship per-agent hook configs as **clearly-optional extras**, not wired by
  default: `project-trajectory/agent-hooks/claude.settings.json` and
  `gemini.settings.json`, each just invoking the same scripts on the agent's
  pre-commit/stop event, with a README note "optional; the git hook + CI are the
  source of truth."

**Tests:** test the pre-commit's underlying logic directly (don't shell out to
`git commit`): a clean minimal project passes; a hand-edited GENERATED block
fails (via `gen_arch_map --check`); an orphaned registry fails. Assert bootstrap
copies `.githooks/pre-commit`.

**Risks:** a slow or over-eager hook annoys users → keep it fast + only
always-valid checks + opt-in. Interpreter discovery must match `setup.sh`.

**Done-when:** a fresh clone that runs setup gets a working pre-commit that
blocks stale-map/orphan/format-broken commits regardless of agent; `pytest -q`
green.

---

## Thread 1 — Generated UN→SR→LLR→TC traceability views

**Status: ✅ landed 2026-06-28.** All three views ship from one join in
`trace.py`: a line-reviewable text outline and a colored Mermaid `graph LR` go
into `docs/test/report.md` every run (no flag); `--html` writes the dependency-
free collapsible `report.html`. Orphan ids are tracked alongside the existing
findings so the outline/graph/HTML flag the same nodes (orphan outranks draft).
The harness (`check.py`) and CI now pass `--html` and publish/ignore the
artifact; the "Reviewability" principle is named once in PROCESS.md §3 and
referenced from the script, gitignore, HTML header, and §7. **Deviations from
the spec as written:** (1) the Mermaid is a **single colored DAG**, not
Area/Phase subgraphs — shared UN/TC nodes straddle those boundaries and a node
can't live in two Mermaid subgraphs without breaking the graph; the text outline
and HTML are the scalable views (as the plan's own Risks line states), and the
DAG keeps its "small, diff-friendly" niche. (2) The **optional** `architecture.md`
`TRACEABILITY GRAPH` splice was skipped: a *tracked* generated block needs a
freshness gate, and `trace.py` has no `--check` staleness mode; the gitignored
report + HTML already carry the data. Both honor "edit conservatively."

**Goal:** a generated, very-traceable rendering of the requirement spine that
doubles as a gap visualizer. Data already exists in `trace.py`'s join; this is
rendering. **Decision (2026-06-28): produce three complementary views from the one
join** — a line-reviewable text outline, small diff-friendly Mermaid, and a
scalable HTML map — because no single format is both line-by-line reviewable and
big-graph-scalable.

- **Plain-text indented outline (primary, line-reviewable)** into
  `docs/test/report.md`: a `UN → SR → LLR → TC` tree, status/orphan flags inline.
  Pure text ⇒ reviews line-by-line and scales to any size; `report.md` is already
  regenerated each run and gitignored.
- **Mermaid `graph LR` (diff-friendly, small):** a DAG (**not** a mindmap — a TC
  verifies an SR *and* an LLR; an SR has many LLRs), **colored by `Status`/orphan
  state** (`classDef`) so a Draft/orphan stands out. Mermaid-in-markdown does
  **not** scale (GitHub caps complexity; no pan/zoom), so keep these **scoped**:
  group by `Area` / per-phase subgraphs. Emit into `report.md`; optionally splice
  a scoped one into `architecture.md` behind a new `TRACEABILITY GRAPH` marker.
- **`trace.py --html` (primary *scalable* view):** a static, **dependency-free**
  collapsible `<details>` tree (inline CSS, zero JS) of the full graph for
  browse/onboard/audit at any size. It is a generated composite artifact ⇒
  **gitignored** (add to `gitignore.template`), never the review surface for the
  data (review the registry CSV diff).
- **Reviewability principle (state once in PROCESS.md, reference elsewhere):** the
  **registries are the tracked, line-by-line-reviewable source of truth**;
  rendered views are generated. Small, diff-meaningful generated blocks live in
  tracked files behind `GENERATED` markers + a freshness gate (the arch map);
  **large composite artifacts** (full trace report, HTML map) are regenerated and
  **gitignored**. This is the "composite artifacts ignored from change tracking"
  rule, named.

**Tests:** `report.md` contains a ```mermaid graph **and** the text outline (the
minimal chain shows UN-001→SR-001→LLR-001→TC-001); an orphan/Draft node gets the
distinct Mermaid class **and** an inline flag in the outline; `--html` yields a
self-contained file with no `<script>`; `gitignore.template` ignores the HTML
artifact.

**Risks:** graph noise on big projects (mitigate via the text outline + scoped
Mermaid + the full-graph HTML); keep all three as stdlib string-building (no dep).

**Done-when:** a harness run regenerates all three views; gap states are visually
*and* textually distinct; the HTML artifact is gitignored; `pytest -q` green.

---

## Thread 2 — Name the process/product check split

**Status: ✅ landed 2026-06-28.** `check.py` step tuples gained a 5th `layer`
field (`"process"`/`"product"`); `--list` now renders `[layer] [gates]` (e.g.
`[process] [G2,G3]`), with the step list grouped product-then-process behind
section comments. PROCESS.md §7 defines the two layers once (process = kit-owned
stdlib `trace/check_flows/gen_arch_map`; product = wired `format/lint/tests`),
which the pre-commit hook and `check.py` already pointed at. EXAMPLE.md gained a
worked infrastructure SR (DB failover, SRE/Ops + DBA hats, `Verification=
Demonstration`, optional `Area=Infra/DB`, `Release`-tier procedure TC) plus a
"What to copy" tie-in. **Deviations from the spec as written:** (1) `layer` was
**appended** as the 5th tuple element, not inserted, so existing index access
(`s[2]`=cmd, `s[3]`=gates) and the `cmd_of` test helper stayed untouched — only
the two unpacking loops changed. (2) The infra example landed in **EXAMPLE.md**
(new §7), the worked-chain home, rather than PROCESS.md. (3) `test_step_plan_
wiring` now also asserts the invariant the layer formalizes — process steps have
`requires=()`, product steps name a tool — and a new `--list` test checks the
tags render against a scaffold. `pytest -q`: 61 passed, 1 skipped (the
`sh`-dependent pre-commit e2e, skipped on Windows).

**Goal:** make explicit the boundary you already feel — kit-owned **process
checks** (stdlib Python, identical everywhere, don't rewrite) vs project-owned
**product checks** (language-specific, you wire them). Partly a prerequisite for
0b (pre-commit = the process layer).

- `PROCESS.md` §7: define the two layers in one place. Map current steps:
  *process* = traceability, design-flows, arch-map (`requires=()`); *product* =
  format, lint, tests+coverage (`requires=("ruff"/"pytest")`).
- `check.py`: add a `layer` ("process"|"product") to each step tuple and show it
  in `--list` (e.g. `[process]`/`[product]`), so a newcomer sees which steps they
  must localize. The `requires` tuple already implies it — formalize + surface.
- Add one worked **infrastructure-requirement** example (DB/network/deploy) to
  show capture via a domain hat (SRE/Ops, DBA) + `Verification=Demonstration`/
  `Manual` + the optional `Area` tag — no new mechanism, just clarity.

**Tests:** `check.py --list` prints the layer tags; `test_step_plan_wiring`
extended to assert each step's layer; existing wiring tests unaffected.

**Risks:** tuple-shape change touches `steps()` consumers in tests — update them.

**Done-when:** `--list` distinguishes the layers; PROCESS.md names them;
`pytest -q` green.

---

## Thread 3 — Encode the five working-agreement directives

**Goal:** fold the user's five general directives into the canonical agent guide
(now `AGENTS.template.md`), integrated with the existing "Communication style"
(which already covers #1-partial, #2, #4). Gaps to add: #1's *unattended ⇒ record
the assumption*, #3 (don't touch unrelated code; surface smells separately), #5
(welcome better/strategic suggestions).

- Add a tight "Working agreement" block (dense — the file is loaded every
  session and Gemini caps at ~12k chars). **Wire #1's assumption-logging to a
  real home:** `docs/status.md` Open Items (or a small Assumptions log) so it's
  enforceable, not aspirational (per the file's own closing note).
- Lightly align this repo's own `CLAUDE.md` "Communication style" — reference,
  don't duplicate.

**Tests:** none (prose); verify no broken intra-doc links.

**Done-when:** all five directives present + integrated; assumption-logging
points at status.md.

---

## Thread 4 — Make test-driven development a co-headline discipline

**Goal:** elevate TDD from *implied* to an **explicitly stated working
discipline**. The process is already TDD-shaped — G2 requires a TC for every
SR/LLR *before* implementation at G3 — but the red→green→refactor loop is nowhere
named. **Decision (2026-06-28): co-headline it**, keeping requirement
traceability as the structural spine. Framing must stay consistent: traceability
is the spine; **TDD is how G3 code gets written**, not a competing claim.

- **`AGENTS.template.md`:** add a tight **test-first loop** — write the TC's
  failing test first, then the minimal code to pass, then refactor — folded into
  "How we work here" / "Code we want" without bloating the file (Gemini ~12k cap).
- **`PROCESS.md` G3:** state implementation proceeds **test-first** (the G2 TCs
  become failing tests before the code that satisfies them); reference the
  existing coverage/Verified criteria rather than restating them.
- **`README.md`:** sharpen the headline from "deep test coverage" to
  **test-driven** development, alongside traceability + gates.
- Don't imply TDD replaces the SN→SR→LLR→TC discipline; it operates within it.

**Tests:** none (prose); verify no broken intra-doc links and that
`AGENTS.template.md` stays within its size budget.

**Done-when:** the test-first loop is stated in `AGENTS.md` + `PROCESS.md` G3 and
headlined in `README.md`, integrated with (not duplicating) the traceability
spine.

---

## Thread 5 — Requirement lifecycle phase (ready / set / go)

**Goal:** make a requirement state **which operational phase of the product's
lifetime** it governs, so the perennially-neglected non-runtime phases get
first-class requirements instead of being discovered late. Today SN/SR capture
*what / why / acceptance* but not *when in the lifecycle*; the edge-case
checklist in `stakeholder-needs.template.md` already gestures at it ("First-run setup",
"Missing dependency / wrong version") without naming the dimension.

The discriminator is the **process boundary + frequency**, *not* the word
"setup" (almost everything readies *something*): ask **"at what point in the
process's lifetime must this hold, and how often?"** That yields three phases
(the user's "ready / set / go"):
- **Provision** (ready) — must be true *before the process can execute at all*:
  install, dependencies/runtime present, infra provisioned.
- **Startup** (set) — established *once per launch, before it serves*: load +
  validate config, run migrations, open the initial connection pool, allocate
  fixed resources, readiness probe.
- **Runtime** (go) — steady-state serving, *including recurring acquisition*:
  handle requests, reconnect on drop, lazy / per-request alloc, dynamic config
  reload.

Optional **Shutdown** / **Upgrade** cover drain, teardown, migration, rollback.

- **Name the dimension once in `PROCESS.md`** (near §1 roles / §2 ids, or a short
  note in §3) with the **default vocabulary `Provision` · `Startup` · `Runtime`**
  (deliberately avoid the overloaded label "Setup" — that word is what made the
  boundary ambiguous) and the **process-boundary + frequency discriminator**
  above. State it is an **open, project-named set** (extend with
  `Shutdown`/`Teardown`, `Upgrade`/`Rollback`, `Recovery` as the scope needs),
  exactly like `Area`/domain hats, **not** a fixed enum.
- **Disambiguation rule — "setup recurs," so classify by *when / how often*,** not
  by whether something looks like setup. Opening the connection pool *at boot* is
  **Startup**; reconnecting *mid-operation* is **Runtime**; a fixed buffer at
  launch is Startup, per-request alloc is Runtime. **One feature legitimately
  spans phases** — that's the payoff: a DB capability yields *provision the DB*
  (Provision) → *open the pool + migrate at boot* (Startup) → *reconnect on drop*
  (Runtime), and people usually write only the Runtime one.
- **Configuration straddles Provision↔Startup, and the boundary is
  application-dependent.** Config is **Provision** when it *must pre-exist* and the
  app has **no startup mechanism to obtain it**; it is **Startup** when the app
  *can* obtain/validate it at launch — interactively prompting the user (first-run
  wizard), erroring with a clear message, or falling back to defaults. So whether
  "define the config" is a Provision or a Startup requirement depends on the app's
  own startup capability; capture both the *definition* (where the config lives)
  and the *launch behavior when it is missing*.
- **Keep one axis, not two.** Dependencies and config are *subjects*, not phases —
  a dependency is **required** at Provision but **used** at Runtime; config **must
  exist** at Provision, is **loaded/validated** at Startup, may be **reloaded** at
  Runtime. The phase tag on each concrete requirement already places it; a second
  "kind" axis is the heavy-taxonomy scope-creep this thread avoids.
- **Avoid the `Phase` collision (critical).** The SR registry's existing `Phase`
  column is *delivery* phase (`v1`/`v2`, §4 "Phased delivery"). The lifecycle tag
  must use a **distinct name — recommend `Lifecycle`** — and PROCESS.md must say
  so explicitly so nobody overloads `Phase`.
- **Capture as an optional tag, mirroring `Area`** (the Thread-2 EXAMPLE §7
  addition): a `Lifecycle` column projects opt into on SN/SR; blank = unspecified
  (treat as Runtime). **Decision to make in-thread:** optional tag (recommended —
  no downstream migration, matches `Area`, schema-safe; see Tests) vs. a base
  template column (more discoverable but forces downstream churn). Recommend
  optional + a one-line prompt in the templates.
- **Prompt for it in the templates:** a short line in `stakeholder-needs.template.md`
  (intro + the edge-case note, observing those rows are mostly Provision/Startup)
  and in `system-requirements.template.csv` guidance.
- **One worked EXAMPLE.md illustration:** a Provision- or Startup-phase
  requirement (e.g. a dependency/version check tagged `Lifecycle=Provision`, or
  first-run config tagged `Lifecycle=Startup`), ideally reusing the §7 infra
  slice — *provisioning/migrating* the DB is Provision, *opening the pool at boot*
  is Startup, *failover* is Runtime — to show one feature spanning phases.
- Optionally one clause in `AGENTS.template.md`'s requirement-authoring guidance
  (mind the ~12k Gemini cap).

**Tests:** `trace.py` reads rows with `csv.DictReader` and validates only the
fixed `REQUIRED_FIELDS` allow-list (which already omits optional columns), so a
new `Lifecycle` column is schema-safe — add/confirm a test that an SR carrying a
`Lifecycle` column still passes `trace.py --strict-schema` (the optional-column
tolerance, made explicit). EXAMPLE.md `Permutations` snippets must still parse
(`test_gen_cases.test_example_md_specs_parse`). Otherwise prose — verify
intra-doc links.

**Risks:** scope creep into a heavy lifecycle taxonomy — keep it a light,
optional, project-named tag, not a required enum. Collision with delivery `Phase`
— mitigated by choosing `Lifecycle`. Don't force downstream migration (favor the
optional column).

**Done-when:** PROCESS.md names the lifecycle dimension + the
`Provision`/`Startup`/`Runtime` vocabulary and discriminator, distinct from
delivery `Phase`; the SN/SR templates prompt for it; EXAMPLE.md shows a
Provision/Startup-phase requirement; `pytest -q` green.

---

## Thread 6 — Requirement consistency review (contradictions + clarification)

**Goal:** add an explicit review activity that hunts for **mutual contradictions
and ambiguities** across needs/requirements and routes them to a human — distinct
from the *structural* checks `trace.py` already does. `trace.py` catches
orphans / duplicate-ids / schema; it **cannot** catch two requirements that
*conflict* (incompatible limits, mutually exclusive behavior, overlapping
Area/hat ownership) or a need that is *ambiguous* — that is human/LLM judgment, so
the kit should name it as a **non-machine-checkable review gate** (honest
classification, per §4's "classify the rest honestly"), not pretend a script does
it.

- **Add a consistency-review step to `PROCESS.md` §4 at G1** (and a re-check at G2
  when SRs decompose), **owned by the System Engineer hat** (already the
  gatekeeper). What it checks: conflicting acceptance criteria / limits; mutually
  exclusive behaviors; duplicate or overlapping requirements; ambiguous /
  underspecified needs; overlapping `Area`/hat ownership.
- **Wire outcomes to the existing findings protocol (§5):** each contradiction or
  ambiguity is a finding addressed to the owner; where it needs a human decision,
  **pause and ask — don't guess.** This is the *reachable-human flip side* of
  Thread 3's assumption-logging (record an assumption only when **unattended**;
  when a human is available, **solicit clarification**). Track unresolved
  ambiguities in `status.md` Open Items (Thread 3's home).
- **Keep it explicitly non-machine-checkable** — classify as a Manual/Analysis
  gate activity; do **not** imply `trace.py` performs it. Note that an
  independent LLM reviewer (§6 review-depth triage) is well-suited to a first-pass
  contradiction sweep, with the **human making the call**.
- **Light touch in `AGENTS.template.md`** working-agreement (Thread 3 home) so the
  agent surfaces contradictions and solicits input rather than silently resolving
  — one clause, mind the ~12k Gemini cap.

**Tests:** none (prose). Verify intra-doc links and that `AGENTS.template.md`
stays within its size budget.

**Risks:** turning a judgment activity into checkbox theater — keep it a genuine
review prompt tied to §5 findings, not a fake automated check. Overlap with G1's
existing *completeness* criteria — frame this as the **consistency** complement,
don't restate completeness.

**Done-when:** PROCESS.md §4 names a consistency review at G1/G2 owned by the
System Engineer, wired to §5 findings and the solicit-human-input directive,
integrated with (not duplicating) Thread 3's assumption-logging; links verified.

---

## Thread 7 — Name the top requirement tier honestly (User vs Stakeholder Need)

**Status: ✅ landed 2026-06-29.** Implemented the recommended **option 1**: the
top tier is now **Stakeholder Need (`SN-###`)**, owned by the **Stakeholder** hat
(end users, operators, or a consuming system's owner — End User folded in as one
example). One-pass mechanical sweep: `UN-###`→`SN-###`, `UN-Refs`→`SN-Refs`,
`UN-ID`→`SN-ID`; the registry renamed
`registries/user-needs.template.md`→`stakeholder-needs.template.md` (bootstrap
target `docs/requirements/stakeholder-needs.md`); the id regexes in
`trace.py`/`check_flows.py`/`gen_arch_map.py`, the `Stakeholder` hat across
`PROCESS.md`/`STATUS.template.md`/`KICKOFF_PROMPT.md`/`AGENTS.template.md`, the
G-Final acceptor (now "human/stakeholder"), every doc/README/EXAMPLE, and the
test fixtures (`conftest.py`, `test_trace.py`, `test_registry_checks.py`) updated.
**Deviations from the spec as written:** (1) kept the literal **"end-user
usability" lens** prose (KICKOFF lens section, READMEs) — it's the human-usability
discipline, distinct from the renamed hat and still valid when humans are among
the stakeholders. (2) **No downstream migration note shipped** — the user
confirmed the kit is pre-adoption, so the prefix-rename cost was paid now (the
hinge's "never cheaper than now") and the `sed UN-→SN-` note was unnecessary.
`pytest -q`: 61 passed, 1 skipped (the `sh`-dependent pre-commit e2e, skipped on
Windows).

**Goal:** decide whether the top tier — `UN-###`, "User Need," owned by the "End
User" hat — is mislabeled when the system serves **another system/module** rather
than a human, and pick a term that stays correct across human-facing,
operator-facing, and system-to-system products. This is a naming/identity
decision with a real migration cost, so the thread **frames** it; it does not
pre-decide it.

**Why it's a real gap.** The need that drives a system-to-system feature
originates from the *consuming system's* owners/integrators — a **stakeholder**,
where the immediate consumer is a system (e.g. "the billing service needs an
idempotent charge API so it can safely retry"). The kit already *half*-handles
this (domain hats in §1; cross-project interfaces `IF-###` in §8), but the top
tier's **label** still says "user." Standards anchor: **ISO/IEC/IEEE 29148** names
this tier **Stakeholder Requirements** (StRS), explicitly including users,
operators, maintainers, regulators, *and interfacing systems* — and the kit's
`UN→SR→LLR` spine already echoes 29148's `StRS→SyRS→SRS` layering, so "Stakeholder"
*tightens* an alignment the structure already implies. Keep the word **"Need"**
(the kit's deliberate plain-language-vs-engineering split: needs at the top,
requirements below); the change is only **"User" → "Stakeholder."**

**Candidate terms (the decision):**
1. **Stakeholder Need — `SN-###`** *(recommended).* Standards-aligned; inclusive
   of non-human consumers *and* non-consumer stakeholders (regulators, auditors,
   the Security hat). Cost: a wide mechanical prefix rename + "End User" hat →
   "Stakeholder" hat (End User kept as one example stakeholder) + a one-time
   downstream migration. Minor wart: `SN` reads close to `SR` (System Requirement).
2. **Consumer Need — `CN-###`.** More concrete/plain than "stakeholder"; covers
   human + system consumers; prefix distinct from `SR`. But narrower (misses
   non-consumer stakeholders) and "consumer" can imply a paying end-customer.
3. **Keep `UN-###`, broaden the *definition*.** Zero breaking change: redefine
   "user" as *any consumer — human, operator, or another system (represented by
   its owner/integrator)*. Defers rather than fixes the mislabel; stretches "user."

**The hinge — downstream adoption.** The term is mostly taste; the **prefix
rename** is the cost. `UN-###` is embedded in scripts, templates, tests, EXAMPLE,
and every cross-ref — the same wide-but-mechanical sweep as Thread 0a
(CLAUDE→AGENTS), *plus* it forces every repo already on `UN-###` to migrate (flag
per CLAUDE.md). **If the kit is still pre-adoption, do the clean rename now —
never cheaper than now.** If real downstream repos already depend on `UN-`, take
option 3 now and schedule the prefix rename for a major version.

**Steps (if a rename is chosen — option 1 or 2):**
- Grep-and-reconcile sweep of `UN-` / "User Need" / "End User" across
  `PROCESS.md` (§1 hat, §2 id-scheme row, §3, §4 gate sign-offs, §8), the registry
  file `registries/user-needs.template.md` (rename + headers), `EXAMPLE.md`,
  `README.md` / `project-trajectory/README.md`, `KICKOFF_PROMPT.md`,
  `AGENTS.template.md`.
- `bootstrap.py` MAPPING (registry filename) and any `trace.py` prefix handling;
  then update the test suite (grep it for `UN-` / "User Need"). Mitigate the wide
  churn with the bootstrap file-list + trace tests, exactly as Thread 0a did.
- Ship a one-line **downstream migration note** (sed `UN-`→`SN-`, rename the
  needs registry file).

**Steps (if keep-and-broaden — option 3):** one definition sentence in
`PROCESS.md` §2 + the UN-template intro, and an EXAMPLE row whose stakeholder is a
*consuming system*. No code/test churn.

**Tests:** rename path — grep the suite for `UN-` / `User Need` and update; the
bootstrap file-list + trace tests must stay green (`pytest -q`). Keep-and-broaden
path — prose only; verify links.

**Risks:** identity-level rename forces downstream migration — gate it on
adoption. `SN`/`SR` visual proximity. Bikeshedding — timebox the term choice.

**Done-when:** the top tier's label + definition stay correct for system-to-system
scope; the term + prefix decision (and its rationale) are recorded here; if
renamed, no dangling `UN-` / "User Need" / "End User" remains and `pytest -q` is
green.

---

## Sequencing & session strategy

Landed so far: **Thread 0a ✅**, **Thread 0b ✅**, **Thread 1 ✅**, **Thread 2 ✅**,
**Thread 3 ✅** (all 2026-06-28), **Thread 7 ✅** (2026-06-29 — the `UN→SN`
rename). Remaining threads are independent — any order:

1. **Thread 4** (TDD co-headline) — prose/framing; edits README + AGENTS.md +
   PROCESS.md.
2. **Thread 5** (requirement lifecycle phase) — small; PROCESS.md + SN/SR
   templates + EXAMPLE.md + one schema-tolerance test.
3. **Thread 6** (requirement consistency review) — prose; PROCESS.md §4/§5 +
   an AGENTS.md clause; pairs naturally with Thread 5 in one "requirements rigor"
   session.

Thread 7 landed first among the late threads (the wide rename is cheapest done
alone and before 5/6 touch the same registries); the `SN-###` ids it established
are already reflected in the specs for 5 and 6 above.

Each phase ends green (`pytest -q`, real output) and checks its items off here.

**Phase boundaries are natural session boundaries.** Thread 0a alone is a
wide rename; pairing it with everything else in one session risks context
exhaustion mid-rename. Capture is done (this file); implement per-phase in fresh
session(s) using this doc + the branch as the spec.
