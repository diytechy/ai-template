# Kit Improvement Plan

Derived from `TEMPLATE_REVIEW.md` (resolved 2026-06-28) plus follow-on design
threads and a cross-agent-portability decision. This file is the **spec a
fresh session implements from** — each thread is self-contained with Goal /
Steps / Tests / Risks / Done-when. Keep it updated as threads land (check items
off; record deviations).

Branch: the current working branch — `MultiRepoSupport` as of 2026-07-01
(Threads 0–11 landed on `template-review-fixes`, since merged; keep this line
current when the working branch changes, or a cold session commits to the
wrong one).

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

**Status: ✅ landed 2026-06-28** (first wave, with 0a/0b/1/2; Status block recorded
retroactively 2026-06-29 — this thread predated the per-thread Status-block
convention). `AGENTS.template.md` carries a dense **"Working agreement"** section
folding in all five directives: #1 *ask, don't assume — and when unattended, pick
the most reasonable interpretation, proceed, and record it under **Assumptions**
in `docs/status.md`* (the home exists: `STATUS.template.md` "Assumptions
(unattended)"); #2/#4 via the existing Communication style; #3 *stay in your lane —
don't change unrelated code, surface a design smell as a separate finding*; #5
*propose the stronger / longer-lived approach*. This repo's own `CLAUDE.md`
"Communication style" **references** that block ("the shipped guide states the full
version — `AGENTS.template.md` 'Working agreement'") rather than duplicating it, per
the thread's single-source intent. Thread 6 later added the consistency-review
clause to the same "Ask, don't assume" bullet as the reachable-human flip side of
the assumption-logging. **No deviations.** Prose only (no tests).

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

**Status: ✅ landed 2026-06-29.** TDD co-headlined without displacing the
traceability spine. `README.md`: the opening headline now reads built
**test-first** (was "deep test coverage"), and "Why this produces sustainable
code" gained a **Test-driven** bullet (the G2 TC is a failing test before the
code — red→green→refactor — so implementation is pulled by the spec, not
retrofitted). `PROCESS.md` G3 is retitled **Implementation (test-first)** and
states the loop (each G2 TC becomes a failing test before its code), explicitly
framed as operating *within* the `SN→SR→LLR→TC` discipline, not instead of it.
`AGENTS.template.md` gained a tight **Write the test first (TDD)** bullet in "How
we work here." **Deviation from the spec as written:** the AGENTS bullet leans on
the adjacent "Everything traces" bullet for the spine framing rather than
restating it, and three nearby lines were tightened, to keep the file under the
~12k Gemini cap (11,993 chars after; see Thread 6 note). `pytest -q`: 62 passed.

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

**Status: ✅ landed 2026-06-29.** The lifecycle dimension is named once in
`PROCESS.md` §4 (immediately after "Phased delivery", so the delivery-`Phase` vs
lifecycle distinction is adjacent and explicit): the **`Provision`/`Startup`/
`Runtime`** default vocabulary (open, project-named — extend like `Area`), the
**when/how-often discriminator** ("setup recurs"), the **one-capability-spans-
phases** payoff, the **config straddles Provision↔Startup (app-dependently)**
rule, and **keep one axis** (dependencies/config are *subjects*, not phases).
Captured as an **optional `Lifecycle` tag mirroring `Area`** — the in-thread
decision went to *optional, not a base column* (no downstream migration,
schema-safe). Prompts added to `stakeholder-needs.template.md` (intro lifecycle
question + a note that the edge-case rows are mostly Provision/Startup) and to the
`system-requirements.template.csv` `Phase` cell, which now explicitly warns *not*
to overload `Phase` and points at the `Lifecycle` tag — the exact point of
confusion. `EXAMPLE.md` §7 tags the failover SR `Lifecycle=Runtime` and adds a
table showing the **same DB capability spanning Provision/Startup/Runtime** (the
two usually-missed siblings). New test `test_lifecycle_column_is_schema_safe`
makes `trace.py`'s optional-column tolerance explicit. **Deviations from the spec
as written:** (1) landed in **§4** (adjacent to delivery `Phase`) rather than
§1/§2/§3, because the `Phase` collision is the whole risk and adjacency is the
clearest disambiguation home; (2) the **optional `AGENTS.md` clause was skipped** —
`AGENTS.template.md` sits at the ~12k Gemini cap (11,998 chars), so the guidance
stays single-sourced in PROCESS.md (the call Thread 8 made). `pytest -q`: 69
passed.

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

**Status: ✅ landed 2026-06-29.** `PROCESS.md` §4 gained a **Consistency review
(G1; re-checked at G2)** block owned by the **System Engineer** hat: it reads the
needs/requirements *against each other* for the conflicts a script can't see
(contradictory acceptance criteria/limits, mutually exclusive behaviors,
duplicate/overlapping requirements, ambiguous/underspecified needs, overlapping
`Area`/hat ownership), explicitly classified **non-machine-checkable**
(Manual/Analysis — never implying `trace.py` does it; an independent LLM reviewer
§6 may do a first-pass sweep but the human makes the call), wired to the §5
findings protocol with **pause-and-ask** for human decisions, integrated as the
reachable-human flip side of Thread 3's *Assumptions* logging (assume only when
unattended; solicit clarification when a human is available), with unresolved
items tracked in `status.md` *Open items* and framed as the **consistency**
complement to G1 *completeness* (not a restatement). `AGENTS.template.md`'s "Ask,
don't assume" working-agreement bullet gained a clause to raise a conflict/
ambiguity as a finding rather than silently resolve it. **No deviations.**
`pytest -q`: 62 passed.

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

## Thread 8 — Name the companion-tooling boundary (measure vs. generate; map vs. index)

**Status: ✅ landed 2026-06-29.** Both boundaries named in `PROCESS.md` (the
canonical home) with a brief `README.md` echo. §3 (by the generated code map)
states **the committed map is a contract, not a search index**: `gen_arch_map.py`
is a committed/diff-reviewable/drift-gated artifact, while query-time
**semantic-retrieval tools** (LSP code-graph servers, Serena-style MCP indexes)
are an optional downstream accelerator that **doesn't replace** it and must **not**
be hard-wired (would break stdlib-only / add a server/LSP dep). §7 states **the
kit generates legibility; it does not score it**: *measuring* legibility over time
(AI-readiness, complexity/churn dashboards) runs as an optional **external
readiness assessor**, the same stance as `ruff`/`pytest` (name the gate; the
project picks the tool) — "generate here; measure there." `README.md`'s "Why"
section gained a **Scope — generate vs. measure** note pointing at §7.
**Deviation from the spec as written:** no `AGENTS.md` change — the thread's
"prefer PROCESS.md + README, link from AGENTS.md" was taken as PROCESS+README
only, to protect the ~12k cap already spent by Threads 4/6. No new kit dependency
introduced. `pytest -q`: 62 passed.

**Why (from a survey of the sibling `ai-native-toolkit`, 2026-06-29):** the kit is
the **generative** half of codebase legibility — it *builds* the traced spine, the
committed code map, the gates. A whole **measurement** half exists too (e.g. that
project's `/assess`: a deterministic, ~zero-token engine scoring an 8-layer
AI-readiness model with complexity/churn heatmaps and a doc-navigability graph). A
repo scaffolded from this kit should *score well by construction* — it already
generates the Layer-0/3/5/6 artifacts such an assessor looks for. Naming the
boundary stops two recurring confusions: (1) "should the kit also measure?" (no —
different dependency budget) and (2) "is the generated map a code-search index?"
(no — it's a *contract*).

- **State the generate-vs-measure split** once (PROCESS.md §7 / README): the kit
  builds legibility; to *track* it over time, run an **external readiness
  assessor** as optional downstream tooling. Frame by **category, with `e.g.`
  examples** — never a hard dependency or endorsement (same stance as
  `ruff`/`pytest`: the kit names the gate, the project picks the tool).
- **State the committed-map-vs-query-index distinction** (PROCESS.md §3, by the
  "Generated code map"): `gen_arch_map.py` is a **committed, diff-reviewable,
  drift-gated artifact** (part of the source of truth). **Semantic-retrieval tools
  — LSP-backed code-graph servers, Serena-style MCP indexes — are a different
  thing**: query-time, not committed, language-server-dependent. They are a
  legitimate *optional downstream accelerator* for chasing references across a
  large repo; they **do not replace** the committed map and the kit must **not**
  hard-wire one (it would break stdlib-only and add a server/LSP dependency).
- Keep it tight and stack-agnostic; mind the AGENTS.md ~12k cap if it lands there
  (prefer PROCESS.md + README, link from AGENTS.md).

**Tests:** none (prose). Verify intra-doc links (see Thread 9 — this is exactly
the check that would automate that step).

**Risks:** naming third-party tools dates the doc / reads as endorsement —
mitigate by naming the *category* and using `e.g.`; revisit names rarely. Scope
creep into a tool shoot-out — one paragraph each, not a survey.

**Done-when:** PROCESS.md/README name (a) the generate-vs-measure split with an
external assessor as optional companion, and (b) the committed-map-vs-query-index
distinction with semantic-retrieval tools as optional/non-core; no new kit
dependency introduced.

---

## Thread 9 — Doc navigability & staleness check (stdlib)

**Status: ✅ landed 2026-06-29.** New stdlib `scripts/check_docs.py` (process
layer, `requires=()`) parses the Markdown under `docs/` + root `*.md`, builds the
link graph, and reports three classes: **broken intra-repo links** (missing
target file/dir or `#anchor` — hard fail, exit 1), **orphan docs** (unreachable
from an entry root — warn by default, `--strict-orphans` escalates to fail), and
**staleness** (`--stale`, git-gated, warn-only: a doc linking a *non-doc* file
committed more recently than the doc; degrades to a clean skip when git is absent
or the tree isn't a work tree). Scope is the high-value 80% — inline `[text](dest)`
links + same-file/`file#frag` anchors against GitHub-style heading slugs (plus
`{#id}` suffixes and `<a name=…>`); images, reference-style links, and links
inside fenced/inline code are deliberately out of scope (documented in the
docstring). Wired into `check.py` as a `doc-navigability` **process** step at
**{G1,G2,G3}** (G1 now has a real check), passing `--ignore docs/test/report.md`
so the gitignored generated composite isn't scanned. Principle named once in
`PROCESS.md` §3 ("The doc set must stay navigable") and listed in §7 (process-check
list + script reference); `bootstrap.py` MAPPING + docstring ship it; both READMEs
mention it. New `tests/test_check_docs.py` (13 cases): CLI behavior on a real
scaffold (clean pass, broken file link, broken/valid anchor, orphan warn-vs-strict,
reachable-clears-orphan, `--ignore` drop, staleness skip-without-git), harness
wiring at G1, and importable units (`slugify`, `parse_doc` scope, `find_stale` with
an injected commit-time lookup, `git_commit_lookup` None outside a work tree).
**Deviations from the spec as written:** (1) `--ignore` was made *drop-from-scan*
(not just orphan-suppression) so generated composites are excluded entirely and
the harness can hold `report.md` out — cleaner than a hardcoded skip; (2) staleness
compares a doc only against **non-Markdown** linked targets (doc-to-doc freshness
is too noisy a signal), kept warn-only and clearly heuristic; (3) the `docs/index.md`
Map-of-Content stays an *optional* reachability root recognized when present, not a
convention forced on the scaffold (no downstream churn); (4) not added to the
`pre-commit` hook — Thread 9 says "wire into the harness," and broken-doc-link churn
is better surfaced at the gate than blocking every early commit. `pytest -q`: **82
passed** (was 69; +13).

**Why:** the kit gates the freshness of *generated* blocks (the code map) but never
checks that the **hand-written** doc set stays navigable and honest — the gap the
sibling project's doc-graph fills ("is every doc reachable? is this a *lying map* —
a frozen doc beside churning code?"). The kit already asks humans to "verify no
broken intra-doc links" by hand in several gates (Threads 3/4/6 Done-whens, and
Thread 8 above); this **operationalizes** that into a machine check, extending the
"the map must stay honest" guarantee from code to docs. Must stay **stdlib-only,
3.8+, cross-platform** — re-implement the *technique*, never vendor the sibling's
`networkx`/`grimp` engine.

- **New process-layer check** (Thread 2 taxonomy: kit-owned, stdlib, `requires=()`)
  — `scripts/check_docs.py` (name TBD). Parse Markdown under `docs/` (+ root
  `*.md`), extract links, build the link graph, and report:
  - **broken intra-repo links** (target file/anchor missing) — a hard finding;
  - **orphan / unreachable docs** (no inbound link, or unreachable from an entry
    root — `AGENTS.md`/`README`/an optional `docs/index.md` Map-of-Content);
  - *(optional, git-gated)* **staleness**: a doc untouched while the modules it
    references churned — degrade gracefully (skip) when git or the link target
    isn't resolvable, exactly as the sibling does, so a non-git checkout still runs.
- **Wire into the harness** as a process step (likely G1+ since docs exist early);
  decide failure vs. warn per finding class (broken links fail; orphans/staleness
  may warn first). Consider a small **`docs/index.md` Map-of-Content** convention
  as the reachability root (the kit's doc set is small; the value is for the
  *downstream* project's growing `docs/`).
- **Single-source the principle** in PROCESS.md §3 "Reviewability" (the doc map
  must stay honest like the code map), referenced from the script and harness —
  don't restate it in five places.

**Tests:** a fixture doc tree with a broken link fails; an orphan doc is reported;
a clean tree passes; staleness degrades to skip without git. Add to the kit's
pytest suite; keep the script importable for unit tests like `trace.py`.

**Risks:** Markdown link parsing is fiddly (relative paths, anchors, reference-
style, images) — start with the high-value 80% (relative file links + anchors),
document what's out of scope. Over-eager orphan rules annoy on legitimately
standalone docs — make the entry-root and ignore set configurable. Staleness is a
heuristic, not truth — keep it warn-only and clearly labeled.

**Done-when:** a stdlib `check_docs` reports broken links + orphans (staleness
optional/warn), is wired into the harness as a process check, names its principle
once in PROCESS.md §3, and `pytest -q` is green.

---

**Deferred (considered, deliberately not a thread) — risk-aware ("hotspot") map.**
Folding a complexity×churn signal into `gen_arch_map.py` (the sibling's heatmap
idea) was considered and **dropped**: a red "danger" tint in the map invites
"refactor the red thing" reflexes that can *fight* good design — a legitimately
complex pure core or a deliberately central thin orchestrator would read as a
problem to dissolve. The map's job is *legibility and drift-proofing*, not risk
scoring; risk/hotspot analysis belongs to the external **measurement** companion
(Thread 8), where a human reads it as advice, not as a tripwire baked into the
source-of-truth artifact. Revisit only with a design that can't bias decomposition.

---

## Thread 10 — Non-functional requirements first-class (perf/resource budgets in their own registry)

**Status: ✅ landed 2026-06-29.** NFRs made first-class via a new `PROCESS.md` **§9
"Non-functional requirements & performance budgets"** (added as a new end section
parallel to §8, so nothing renumbers): the **consideration checklist** (a prompt,
not a mandate; anchored on **ISO/IEC 25010**, with a "don't double-prompt — the
kit already covers maintainability/usability/fault-tolerance/`IF-###`" note), the
**three-homes routing** (allocation→budgets registry; behavioral→ordinary SRs;
hard external limits→`status.md` constraints), and the **`performance-budgets.csv`
(`PB-###`)** registry owned by a new **Integration/Coordination** domain hat
(added to §1). New `registries/performance-budgets.template.csv` (`PB-ID, Metric,
Refs, Budget, Unit, Tolerance, Direction, Tier, Gate, Owner, Notes`), wired into
`bootstrap.py` MAPPING (→ `docs/requirements/performance-budgets.csv`) +
docstring; optional and inert like `interfaces.csv`. **`trace.py` keeps it
traceable** (the spec's optional hook): each `PB` row's `Refs` must back-link a
real SR/LLR/Module and a malformed/duplicate `PB-` id fails like any integrity
error — but PB is held *out* of the placeholder/schema sweeps so a leftover
`PB-000` never blocks a gate a project doesn't use. `EXAMPLE.md` gains a new §8
with two worked rows (peak-RAM linked to the export SR/LLR at its `Permutations`
boundary, and a **VRAM** row for a GPU module the integrator allocates); READMEs
updated. **Deviations from the spec as written:** the **optional `AGENTS.md`
clause was skipped** (same ~12k-cap reason as Threads 5/8); the
comparator/regression harness is **deliberately out of scope** — it is Thread 11
(Session D), and §9 ends by pointing at it without building it. New tests:
`test_perf_budgets.py` (6 cases) + the bootstrap file-list assertion. `pytest -q`:
69 passed.

**Why:** the SN→SR→LLR→TC spine is built for **functional** verification; the
test content audits behavior, not **resource cost**. Non-functional requirements
(NFRs) — performance, RAM/VRAM, artifact size, reliability, security, etc. — are
*expressible* as SRs but nothing **prompts** their capture, and quantitative
budgets often aren't knowable by the requirement author: a module that is part of
a larger whole is *handed* a slice of a system-level budget by an integrator, and
the metrics should be **minimized within reason**, not pinned to a number the
author invents.

**Decision (2026-06-29, with the user):** keep quantitative perf/resource budgets
in a **separate `performance-budgets.csv`**, owned by a **coordinator/integration
hat**, so SN→SR→LLR stays functional-focused and an integrator can (re)allocate
budgets across modules without churning the functional breakdown. This is the
same pattern `interfaces.csv` (IF-###, §8) uses for cross-repo contracts — a
coordination registry separate from the spine. The visibility cost the user
flagged is mitigated by **linking each budget row back** to the SR/LLR/Module it
bounds (separate, but still traceable).

- **NFR consideration checklist** (a *prompt*, not a mandate — "don't wear a hat
  the scope doesn't need"): a section in `stakeholder-needs.template.md` (or a
  sibling note) listing the NFR categories to **consider**, each with an
  "applies-when" and a home. Anchor on **ISO/IEC 25010** (product-quality model;
  the 2023 revision added Safety). Candidate set (trim per scope): performance
  efficiency; reliability/availability/recoverability; **security** (authn/authz,
  data protection, secrets, audit, dependency-vuln/supply-chain);
  **observability/operability** (logging/metrics/tracing/health — also the
  prerequisite for measuring Thread 11's metrics); scalability/capacity;
  compatibility/interoperability; portability/installability (incl. app size);
  compliance/legal/licensing; safety (cyber-physical); data integrity/durability.
  **Note what the kit already covers** so it doesn't double-prompt: maintainability
  (= core), usability (= the end-user lens), some fault tolerance (= the edge-case
  table), cross-project contracts (= IF-###).
- **Three homes by nature** (state this so authors route correctly): *allocation/
  coordination* NFRs (perf budgets, capacity, availability targets) → the new
  integrator-owned registry; *behavioral* NFRs (security, observability, safety,
  data integrity) → ordinary **SRs** with measurable AcceptanceCriteria + honest
  Verification, owned by a domain hat; *hard external limits* (compliance,
  supported platforms) → `status.md` constraints.
- **New `registries/performance-budgets.template.csv`** — columns roughly
  `PB-ID, Metric, Target(SR/LLR/Module-Refs), Budget, Unit, Tolerance,
  Direction(lower|higher-better), Tier, Gate(fail|warn), Owner/Area, Notes`. Add a
  **coordinator/integration hat** to PROCESS.md §1 domain hats as its owner; a
  module ships provisional self-measured budgets, the integrator sets the real
  allocation.
- **Preserve traceability:** `trace.py` (optionally) flags a budget row that
  references an unknown SR/LLR/Module id and a malformed `PB-` id — separation
  never means disconnection.
- **EXAMPLE.md:** one worked budget row (e.g. peak-RAM at a `Permutations` size,
  plus a **VRAM** row for a GPU module) showing the PB↔SR link.

**Tests:** `trace.py` accepts a `performance-budgets.csv`; if the orphan hook is
added, a budget referencing an unknown id is flagged and a clean set passes;
EXAMPLE budget rows parse. Otherwise prose + a small registry template.

**Risks:** a second registry is a second home — keep it strictly for *quantitative
coordination budgets*; behavioral NFRs stay SRs, or it bloats. The checklist must
stay a *consideration prompt*, not a mandate, or tiny projects drown in N/A rows.
PB↔SR drift — the back-link is the tie; the trace hook keeps it honest.

**Done-when:** PROCESS.md names NFRs + the consideration checklist + the
three-homes routing; a `performance-budgets.template.csv` exists, owned by a
coordinator hat, traceably linked to the spine; EXAMPLE shows a budget row;
`pytest -q` green.

---

## Thread 11 — Performance budget & regression harness (stdlib comparator)

**Status: ✅ landed 2026-06-29.** New stdlib, metric-agnostic
`scripts/check_perf.py` (process layer, `requires=()`) compares a product-emitted
`docs/test/perf-metrics.json` (`PB-ID → number`) against the
`performance-budgets.csv` registry and a committed `docs/test/perf-baseline.json`:
per metric an **absolute** check (vs `Budget`, per `Direction`) and a
**regression** check (vs baseline outside the `Tolerance` band), writing the
gitignored composite `docs/test/perf-report.md`. Exit is nonzero **only** on a
hard-gated breach — a `Gate=fail` row breaching/regressing **within the run tier**
(cumulative `--tier`, blank row-tier defaults to Full); `Gate=warn` rows only warn,
and an absent metrics file or budget set **skips** (never a false failure).
`--update-baseline` rewrites the golden from current metrics (the reviewed,
in-PR way to accept a move). Wired into `check.py` as a `perf-budgets` **process**
step at **{G3}**, tier-threaded (`--tier <tier>`), with a comment marking the
*measurement* that emits `perf-metrics.json` as the project's **product** step.
PROCESS.md §9 gained the comparator subsection (absolute-vs-regression, the
process/product split, the three reviewability classes, baseline-as-golden, the
warn-first honest-gate rule); §3 names the new **committed-golden** class
(`perf-baseline.json`) and adds `perf-report.md` to the gitignored composites; §7
lists the script + the process-check line. `gitignore.template` ignores
`perf-report.md` + `perf-metrics.json` (baseline stays tracked); `bootstrap.py`
MAPPING/docstring ship it; `ci/check.yml` publishes the report; EXAMPLE §8 points
at it; both READMEs carry a row. `gen_release_checklist.py` gained a
**Performance budgets within allocation** section (the warn-tier runtime budgets
never gate, so the human ticks them at release). New `tests/test_check_perf.py`
(15 cases): scaffold CLI (no-budgets pass, no-metrics skip, absolute fail-vs-warn,
within/beyond-tolerance regression, tier scoping, `--update-baseline`), harness
G3 wiring + `--list` layer tag, the release-checklist section, and importable
units (`evaluate`, `parse_tolerance`, `in_tier`, `update_baseline`). **Deviations
from the spec as written:** (1) the metrics↔budget join is by **`PB-ID`** (stable)
rather than the human `Metric` label; (2) `gen_release_checklist.py` Release-hygiene
section renumbered 5→6 to seat the new perf section (the conditional-section
numbering already had gaps, so no churn beyond the one header); (3) no `AGENTS.md`
clause (the ~12k Gemini cap, single-sourced in PROCESS.md — the call every late
thread made). `pytest -q`: **97 passed** (was 82; +15).

**Why:** captured budgets (Thread 10) are inert without a check that **tracks the
numbers over time and alerts**. Two distinct questions: "**worse than expected**"
(absolute budget breach) and "**suddenly much worse**" (regression vs. a
baseline). The work splits cleanly along Thread 2's **process/product** line:
**measuring** a metric is *product-layer* (you wire `/usr/bin/time`,
`tracemalloc`, `nvidia-smi` / `torch.cuda.max_memory_allocated`, a size command,
`pytest-benchmark` / `hyperfine`); **comparing** is *process-layer* (kit-owned,
**stdlib, metric-agnostic** — arithmetic over JSON). The kit owns the comparator;
the project owns the meters.

- **`scripts/check_perf.py`** (stdlib): inputs = the project's measured
  `perf-metrics.json` (product-emitted), the tracked `performance-budgets.csv`
  (Thread 10), and a committed `perf-baseline.json`. Per metric: **absolute**
  check (vs Budget, per Direction) and **regression** check (vs baseline ±
  Tolerance). Emit a **gitignored** `perf-report.md` (current vs baseline vs budget
  + deltas). Exit nonzero only on hard-gated breaches.
- **Baseline-as-golden protocol:** accepting a regression = committing a new
  `perf-baseline.json` **in the same PR** (the diff shows the number move —
  explicit, reviewed, never silent; same discipline as the coverage threshold and
  phase-deferred SRs). Ship a `--update-baseline` mode.
- **Noise discipline — start narrow:** the MVP gates only **deterministic,
  low-noise metrics** (artifact/binary size, dependency count) — stable enough for
  a real gate at the `full` tier. Noisy runtime metrics (latency, peak RAM, VRAM,
  throughput) default **warn-only**, `release` tier, with per-metric tolerance
  bands and a "same runner / best-of-N" note. **Honest-gate rule** (§4): a metric
  that can't be a reliable `Test` gate is warn-tracking or `Demonstration`, never a
  faked binary gate.
- **Harness wiring (Thread 2 layers):** `check_perf.py` is a **process** step; the
  project's measurement that produces `perf-metrics.json` is the **product** step.
  Metrics absent ⇒ skip/warn (like a missing tool). Size gated at `full`, runtime
  perf warn at `release`; CI publishes `perf-report.md` as an artifact.
- **Reviewability (§3):** `performance-budgets.csv` = tracked source of truth;
  `perf-baseline.json` = committed golden (updated deliberately); `perf-report.md`
  = gitignored composite (add to `gitignore.template`).
- Optional: `gen_release_checklist.py` lists perf budgets as Release items.

**Tests:** comparator unit tests (stdlib) — absolute breach fails when Gate=fail;
within-tolerance regression passes; beyond-tolerance regression warns/fails;
missing metrics skip; `--update-baseline` writes the file. Drive from a fixture
metrics+budgets+baseline set; keep the script importable like `trace.py`.

**Risks:** perf flakiness ⇒ false alarms erode trust — mitigate with warn-first,
tolerances, same-runner guidance, start-with-size. Don't build a benchmarking
framework — that's *product* tooling; the kit only compares numbers. Baseline
drift if updates aren't reviewed — the PR diff is the control.

**Done-when:** a stdlib `check_perf` compares measured metrics against budgets +
baseline (absolute + regression, warn-vs-fail per metric) with a baseline-update
protocol, is wired into the harness (size gated at `full`, runtime warn at
`release`), names its principle once, and `pytest -q` green.

---

## Thread 12 — Name the spec-vs-runtime-harness boundary (a turnkey agent harness as optional downstream accelerator)

**Status: ✅ landed 2026-06-30** (Session E, the clubbed prose batch). `PROCESS.md`
§7 gained a **"The kit is a spec; a turnkey agent-runtime harness is a different
layer"** paragraph, placed right after the Thread-8 generate-vs-measure note (the
third §7/§8-style boundary, named by **category with `e.g.`** exactly as Thread 8
mitigates dating the doc) — states the spec/harness split, that they **compose**
rather than depend on each other, and notes the genuine §6 philosophical fit
without adopting it as a dependency. `README.md` gained a matching one-line
**"Scope — spec vs. runtime harness"** echo next to the Thread-8 echo it sits
beside. **Deviation from the spec as written:** no `AGENTS.template.md` clause —
the file sits at 11,998/~12,000 chars with effectively zero slack and Session E
has four other threads (13/17/18, plus 15A's own no-clause call) competing for
the same budget; reconciling that in one pass (as the Session E note anticipated)
would mean fragile byte-shaving across unrelated bullets for a 3-4-word pointer
each, so the call for all of Session E's threads was **PROCESS-only**, per each
thread's own "else PROCESS-only" fallback. No new dependency introduced.

**Goal:** name, once, the boundary between *this kit* — a stack-agnostic, stdlib,
agent-neutral process **spec** you copy into a repo — and a *turnkey agent-runtime
**harness*** that implements a similar gated/verified process but as an installed,
tool-specific **product** (e.g. **DonnyClaude**: an `npx` Node engine + skills /
agents / hooks / MCP for Claude Code, with deterministic verification gates,
model-tiered subagents, and a `.planning/`-style context layer). This is the third
of the §7/§8-style boundary notes, alongside Thread 8's *generate-vs-measure*
(external readiness assessor) and *map-vs-index* (Serena / code-graph): name the
**category**, mark it **optional**, never hard-wire or endorse.

**Why:** a reader who finds DonnyClaude (or a successor) will ask "should the kit
bundle that, or depend on it?" Answer once: **no — different layer and dependency
budget.** The kit is the portable *spec*; a runtime harness is a concrete *product*
a downstream Claude-Code shop may additionally run. **They compose** (a repo
scaffolded from this kit can be driven by such a harness); neither is a dependency
of the other. Recording it in-repo stops the question being re-litigated, and notes
the genuine philosophical fit — its "never grade your own work, back the verdict
with a deterministic gate" stance matches §6 — without adopting its weight (the
kit's stdlib-only + stack-agnostic + agent-neutral rules rule it out *as a
dependency*).

- **PROCESS.md §7** (by the Thread-8 generate-vs-measure / map-vs-index notes): add
  a *spec-vs-runtime-harness* boundary. State it by **category with `e.g.`** (an
  `npx`/Node-installed engine with deterministic gates, model-tiered subagents, a
  `.planning/` context layer), explicitly **optional, tool-specific, not a kit
  dependency**; note the §6 fit and the three constraints that keep it external.
- **README** echo (one line), like Thread 8's "Scope — generate vs. measure" note.
- **Mind the 12k AGENTS.md cap** — no AGENTS.md clause; single-source in PROCESS.md
  (the call every late thread made).

**Tests:** none (prose). Verify intra-doc links — now automatic via `check_docs.py`
(Thread 9).

**Risks:** naming a third-party tool dates the doc / reads as endorsement —
mitigate by naming the *category* + `e.g.`, exactly as Thread 8; one paragraph, not
a tool shoot-out.

**Done-when:** PROCESS.md §7 names the spec-vs-runtime-harness boundary with a
turnkey harness as an optional, non-core downstream accelerator; README echoes it;
no new dependency; links pass.

**Model tier — Sonnet-able end to end.** Mechanical prose mirroring an existing
pattern (Thread 8), with a deterministic link check (`check_docs.py`) as the
backstop. The only strong-model input *is this spec*; execution needs no further
judgment.

---

## Thread 13 — Fold in the "lazy senior dev" coding discipline (right-size guardrails + shortcut-comment convention)

**Status: ✅ landed 2026-06-30** (Session E, the clubbed prose batch). `PROCESS.md`
§3 gained a **"Right-sizing has guardrails — and a name for the calibrated
shortcut"** paragraph, placed right after "Thin orchestrators" and before
"Reviewability" (the existing "named once, referenced elsewhere" home for §3
principles): the **never-cut guardrail list** (validation at trust boundaries,
data-loss-preventing error handling, security, accessibility, understand-before-
you-fix) plus the **`SHORTCUT:`** comment convention (ceiling + upgrade path), a
**kit-neutral tag** rather than Ponytail's branded marker, exactly as the thread
required. **Deviations from the spec as written:** (1) `AGENTS.template.md` was
**left unchanged** — at 11,998/~12,000 chars it has no slack, and Session E
bundles three threads (13/17/18) each wanting a pointer, so the coordinated cap
reconciliation landed on PROCESS-only for all three (see Thread 12's note; the
"else PROCESS-only" branch every one of these threads specs); (2) the optional
`EXAMPLE.md` code-comment illustration was **skipped** — EXAMPLE.md's §5 code
back-link sample shows a fully-implemented function, and grafting a deliberate
shortcut onto it would read as inconsistent with that worked feature, so the
PROCESS.md prose stands alone (no downstream churn either way). `pytest -q`:
unaffected (prose only).

**Goal:** grow the kit's single "Right-size the solution" directive into (a) an
explicit **guardrail list** of what right-sizing must *never* cut, and (b) a named
**intentional-shortcut comment convention** so a deliberate simplification records
its own ceiling and upgrade path. Both are language-neutral and align with the
kit's existing minimal/conservative ethos; the source is Ponytail's YAGNI ladder +
its `ponytail:` shortcut marker.

**Why:** "simplest thing that works" is today one bullet
(`AGENTS.template.md` "Right-size the solution") and can be misread as
"flimsiest." Ponytail's real contribution is the **calibration** — never lazy about
validation at trust boundaries, error handling that prevents data loss, security,
accessibility, or understanding-the-problem-first (root-cause-not-symptom) — plus a
one-line marker that turns an undocumented shortcut into a tracked, upgradable
decision. The marker dovetails with the kit's existing honesty machinery (the
*Assumptions* log, §4 consistency findings) and is the natural feedstock for a debt
ledger should one ever be built (a deliberately deferred harvester, noted below).

- **PROCESS.md (single-sourced home — the 12k cap is full):** name the right-sizing
  **guardrails** once (the "never cut" list), near the §3 modularity/dedup
  discipline or §6 review triage. State the **shortcut-comment convention**: a
  deliberate simplification carries a one-line tag naming the **ceiling** (e.g.
  global lock, O(n²) scan, naive heuristic) **and** the **upgrade path**, so it is
  greppable and reviewable. Use a **kit-neutral tag** (e.g. `SHORTCUT:` /
  `# shortcut:`), *not* a Ponytail-branded one — the kit names conventions
  generically.
- **AGENTS.template.md** is at **11,998 / ~12,000 chars** — do **not** grow it.
  Either (i) tighten the existing "Right-size the solution" bullet to add a
  3–4-word pointer to the PROCESS.md guardrails + the shortcut tag, reclaiming the
  chars from adjacent lines (the Sessions A/B technique), or (ii) add nothing and
  rely on the PROCESS.md link. Prefer (i) iff the result stays ≤ the cap; else (ii).
- **EXAMPLE.md (optional):** one code-comment example showing the tag on a
  deliberately minimal implementation, if it fits without bloating the worked chain.

**Tests:** none (prose). Verify intra-doc links (`check_docs.py`) **and** that
`AGENTS.template.md` stays **≤ ~12,000 chars** (`wc -c` — the hard constraint).

**Risks:** the cap — any AGENTS.md addition must be paid for by tightening
elsewhere or skipped (every late thread hit this). Convention proliferation — one
tag, defined once, not a taxonomy. Don't import Ponytail's branding / benchmarks /
plugin packaging — only the language-neutral discipline.

**Done-when:** PROCESS.md names the right-sizing guardrails + the shortcut-comment
convention once; AGENTS.md either points at them within budget or is deliberately
left unchanged; EXAMPLE optionally illustrates the tag; links pass; `wc -c
AGENTS.template.md` ≤ ~12k.

**Model tier — Sonnet drafts the prose; strong model owns the cap juggling.**
Writing the guardrail/convention text is well within Sonnet. The fiddly judgment is
the AGENTS.md byte budget — *which* adjacent lines to compress without losing
meaning — which every late thread treated carefully. Either do that pass on the
strong model, or let Sonnet draft and **verify the byte count green** before
commit. No script, so the safety net is only link-check + size; a quick
strong-model glance before commit is cheap insurance.

---

## Thread 14 — "Existence ≠ implementation": a no-stub / substance gate (decided: A+C)

**Status: ✅ landed 2026-06-30** (Session F). Both halves shipped. **A** —
`PROCESS.md` §4 G3 gained a clause ("each in-scope SR's implementing symbol is
**substantive, not a stub**") plus a **"No-stub / substance review (G3)"**
paragraph parallel to the existing "Consistency review": defines the criterion,
explains why coverage+TDD don't already cover it (a test can exercise a stub's
trivial path; Demonstration/Manual/Analysis SRs have no test to fail), classifies
it **Inspection — human/LLM judgment, never a machine verdict**, folds the prompt
into §6's independent-reviewer checklist, and points at the §3 code map (it already
harvests each symbol's summary + `Implements:` back-links the reviewer reads).
**C** — new stdlib `scripts/check_stubs.py` (AST): lists public functions/methods
whose body is `pass` / `...` / `raise NotImplementedError` (bare or called) / bare
`return None` / docstring-only, writes the gitignored composite
`docs/test/stub-report.md`, and is **warn-first** (exit 0; `--strict` gates).
Skips private names, private classes, `@abstractmethod`/`@overload`, and never
flags a value-returning function (the tiny-pure-core false positive). New
`tests/test_check_stubs.py` (13 cases): fixture-tree CLI (substantive passes; every
stub shape flagged; warn-first vs `--strict`; tiny-pure not over-flagged;
private/abstract/overload skipped; `--exclude`; no-src OK), report-gitignored +
bootstrap-ships-it assertions, and importable units (`stub_kind` per shape,
`scan_source` scope/skips, line numbers). `pytest -q`: **110 passed** (was 97; +13).

**Deviations from the spec as written:** (1) the detector is **not wired into
`check.py`'s default `steps()` plan** — it ships standalone (bootstrap MAPPING +
docstring) with a **commented wiring example** in `check.py`'s product block.
Rationale: the spec's own "**like the perf meter**" + "**outside the required
process floor**" point at the perf-*meter* precedent (the meter is a comment, not
a default step), and a stdlib-but-Python-specific step can't be added as `product`
without breaking the `test_step_plan_wiring` invariant (`product` ⇒ names a tool)
or mislabeled `process` (≠ stack-agnostic). So the optional **`--list` layer-tag**
test the spec floated was replaced by **direct script tests** (units + fixture-tree
+ warn-first/`--strict` exit + bootstrap file-list), which exercise the same
contract without polluting the floor. (2) EXAMPLE.md had no dedicated "G3
checklist," so the criterion is shown as a **"Substance, not just existence"**
bullet in §"What to copy". (3) **No `AGENTS.md` clause** (the ~12k Gemini cap, as
Threads 5/8/10). `bootstrap.py` had a **pre-existing** over-long `stakeholder-needs`
MAPPING line (Thread 7's rename); left untouched per "edit conservatively."

**Goal:** close the one capability the kit lacks that DonnyClaude has — a check that
an implementation which satisfies its trace links and a thin test isn't a hollow
**stub** (a body that is `pass` / `...` / `return None` / `raise
NotImplementedError`, a handler that only logs, a placeholder return). The kit's
gates verify *traceability + coverage + tests pass*; **none asserts substance.**

**Why:** TDD (G3) mitigates this — a red-first test should fail against a stub — but
coverage can be satisfied by a test that exercises a stub's trivial path, and
Demonstration / Manual / Analysis SRs have **no** automated test to fail.
DonnyClaude's `verification-patterns.md` ("existence ≠ implementation", wiring
checks) is grep/heuristic and JS/React-flavored, which **collides head-on** with the
kit's stdlib-only + stack-agnostic + "generate, don't score" constraints (Thread
8). **So the design decision *is* the thread.**

**The options considered (decision made — A + C; kept for rationale):**
1. **A — Convention + gate criterion only (no script).** Add a G3 exit criterion:
   "every in-scope SR's implementing symbol is substantive, not a stub," classified
   **Inspection/Analysis** (human/LLM judgment, per §4 "classify the rest
   honestly"), with a reviewer prompt folded into §6's independent-reviewer
   checklist. Zero new code; stdlib-clean; stack-agnostic; honest. Cheapest; matches
   the kit's "name the gate, the project picks the tool" stance.
2. **B — A light stdlib heuristic *process* check.** A new `check_*.py` flagging
   trivial-bodied public symbols. **Tension:** one detector can't be stack-agnostic
   (stub shapes differ per language); it would be Python-reference only — but unlike
   `gen_arch_map.py` (which every stack re-implements into the *same marker*), a
   stub detector has no shared artifact, so a *required* Python-only gate is exactly
   what the kit elsewhere avoids. Higher false-positive risk (a legitimately tiny
   pure function reads as a stub) ⇒ would need warn-first, like the perf comparator.
3. **C — Product-layer detector; kit owns only the criterion** (mirrors Thread 11's
   measure/compare split). The kit defines the G3 *no-stub criterion* in prose
   (= A), and ships an **optional Python-reference** AST helper (lists public
   symbols with trivial bodies) as a *product* example the project wires — exactly
   as the perf *meters* are product and the *comparator* is process. A non-Python
   stack swaps or drops the detector.

**Decision (confirmed with the user 2026-06-30): A (always-on criterion) + C — and
ship the Python-reference detector.** Keeps the kit stdlib + stack-agnostic + honest;
gives Python projects a concrete tripwire without forcing one on every stack or
pretending a heuristic is a universal gate. The detector is **selected to ship** (the
user: "probably still good to have"), not merely named as a possibility — but stays
**optional + product-layer + warn-first** (a Python project opts in; a non-Python
stack swaps or drops it). **B rejected as required** — a required Python-only
heuristic gate violates the kit's own boundaries.

**Steps (A + C):**
- **PROCESS.md §4 G3:** add the **no-stub / substance** exit criterion, classified
  Inspection/Analysis; reference §6 (reviewer prompt) and §3 (the code map already
  harvests the symbol summaries a reviewer reads). Mind the cap — no AGENTS.md
  clause.
- **`scripts/` (C — ships):** an **opt-in, stdlib, Python-reference** AST helper
  listing public symbols with trivial bodies (`pass`, `...`, bare `raise
  NotImplementedError`, `return None`-only), emitting a report the project wires as a
  **product** step (like the perf meter). Clearly product-layer, **warn-first**,
  outside the required process floor. Importable units + a fixture-tree test like
  `check_docs`/`check_perf`; `pytest -q` green.
- **EXAMPLE.md (optional):** show the criterion in the G3 checklist.

**Tests:** A — none (prose); links. C (ships) — units over a fixture module (a stub
flagged; a substantive symbol not; a deliberately tiny pure function **not**
over-flagged), the `--list` layer tag (product, or a clearly-optional process step),
and the warn-first exit behavior; `pytest -q` green.

**Risks:** false positives fighting good design (a tiny pure core flagged) ⇒
warn-first, advisory, **never a hard fail** — the same restraint as the deferred
"hotspot map" note (above Thread 10) and the perf warn-tier. Stack-agnostic
violation ⇒ solved by routing the detector to the product layer. Scope creep into a
wiring/linter ⇒ out of scope; the kit names the criterion, the project picks the
linter (the ruff/pytest stance).

**Done-when:** the A+C decision + rationale recorded here (done); PROCESS.md G3
names the substance criterion, honestly classified; the Python-reference detector
ships — optional, product-layer, warn-first, with green tests; no new required
dependency; links pass.

**Model tier — decision made (A+C); now execution-tiered.** The design decision is
closed. The **A** G3-criterion prose is **Sonnet-able** (link check as backstop). The
**C** Python-reference detector is a from-scratch stdlib script + test suite — a
Sessions-C/D-style **solo build** — Sonnet-executable green against `pytest` **once a
strong-model glance locks the detector contract** (what counts as a stub: `pass` /
`...` / bare `raise NotImplementedError` / `return None`-only; warn-first;
product-layer, not a required gate). The build is why Session F stays solo, not
folded into the Session E prose batch.

**Deferred (noted, not in scope): a `shortcut:`/`ponytail:`-tag harvester.** A
script that harvests Thread 13's shortcut comments into a debt ledger (Donny's
`/ponytail-debt` idea) is a separate solo script build; queue it only if the
convention sees real use. Strong model to spec; Sonnet to build against `pytest`.

---

## Thread 15 — Onboarding & contributor-workspace provisioning (zero-to-running ladder)

**Status: ✅ fully landed — Part A 2026-06-30 (Session E); Parts B/C/D 2026-06-30
(Session G).** Added 2026-06-30 from the scratch.md "Ensure full provision" notes + the
start-from-zero / non-code-contributor discussion. **Scope confirmed with the user
2026-06-30.** **Part A landed:** `PROCESS.md` §7 (right after the existing "Two
check layers" bullets, before the generate-vs-measure note) gained three new
paragraphs — **"A third toolchain layer — the developer workstation"** (names
process/product/workstation, resolving the "no required tools" conflation);
**"The onboarding ladder"** (the `Stage 0 → dev-setup → setup → check` diagram,
explicitly the §4 lifecycle phases applied one level up to the act of developing,
each rung optional/readable/consent-first, non-code contributors named
explicitly); and **"Offline-render principle"** (local-only rendering, pointing
back at §3's Mermaid-in-Markdown choice). `README.md` gained a matching
**"Onboarding ladder"** echo. **Deviations from the spec as written:** (1) landed
in **§7** rather than near §1 — the three-layer split is a direct continuation of
§7's existing process-vs-product toolchain paragraph, so extending it there (vs.
opening a new location) keeps the toolchain-layers concept single-homed; (2) no
`AGENTS.template.md` clause, as the thread itself already calls for ("no AGENTS.md
clause; a README echo is fine") — consistent with Thread 12/13/17/18's same-cap
call this session.

**Parts B/C/D ✅ landed 2026-06-30 (Session G).** Shipped the build half.
**B** — three readable Stage-0 onboarders `onboard.template.{sh,command,cmd}`
(one double-clickable entry point per platform): consent banner → native folder
picker (zenity · `osascript 'choose folder'` · PowerShell `FolderBrowserDialog`)
→ ensure-git (apt/dnf/pacman · brew/xcode-select · winget/choco) → HTTPS clone →
**end banner naming the checkout dir + the "point an AI agent at this directory"
handoff** → offers `dev-setup --check`. Each carries a `REPO_URL` EDIT slot the
project fills; none pipes a remote script to a shell; auth is delegated to the
host CLI (`gh auth login`) per the decision (no hand-rolled SSH/keys). **C** — the
tiered `dev-setup.template.{sh,ps1}` with an EDIT-FOR-YOUR-STACK/DOMAIN block:
`--check` (default; detect+report, installs nothing, always exit 0) · `--baseline`
· `--full` (opt-in, skipped when headless/non-interactive), and `--profile
code|domain` (the non-code contributor gets git + offline renderer + a
project-filled domain viewer). **D** — the meta-repo dogfoods it with a concrete
root `dev-setup.{sh,ps1}` (python, ruff, pytest, a Mermaid renderer). Wired into
`bootstrap.py` MAPPING + docstring (and the chmod rule now sets +x on `.command`
too) and both READMEs. **Deviations:** (1) Part D landed as a **lean concrete**
script (a report-then-`--install` dogfood), not a full filled copy of the tiered
template — conservative and readable, avoiding ~100 lines of duplicated tier
machinery at the meta-repo root while still provisioning this repo and pointing
back at the template; (2) no `AGENTS.md` clause (the ~12k cap, as in Part A). New
`tests/test_onboard_devsetup.py` (7 cases: bootstrap file-list, posix exec-bit,
onboarder end-banner/handoff/clone-URL, dev-setup EDIT/tiers/profiles, an `sh`
smoke test of `dev-setup --check`, `sh -n` syntax of the onboarder, and the
meta-repo dogfood). **Model tier:** built on the strong model with the automated
net at the shell-smoke level the thread specifies; the cross-platform GUI/auth
paths (folder pickers, winget/brew, `gh`) are **manually verified per OS** — a
green pytest is not proof the Windows/macOS/auth paths work. `pytest -q`: **116
passed, 1 skipped** (was 110; +6 run, +1 the posix-only exec-bit check skipped on
Windows).

**Goal:** make a fresh contributor — including a **non-code** one (art/UI, CAD,
electronics, publications) whose work still lives as reviewable git changes — go
from a bare machine to an editable, viewable, testable checkout with minimal
friction and **no required git literacy**. Separate the conflated "setup" concerns
into an explicit ladder and ship readable, optional, consent-first helpers per rung.

**Why:** the kit generates legibility artifacts (Mermaid diagrams, the HTML trace
map, the arch map) that are worthless if a contributor can't *render* them, and it
assumes git + a toolchain a domain contributor may not have. "No required tools"
was always a statement about the **process-check layer** (stdlib Python), never a
claim that a human needs nothing. Naming the layers resolves the conflation; the
guided onboarder serves "start from zero" without forcing change-control knowledge
on someone whose focus is their domain — an AI agent can drive git for them (see
the parked follow-on).

**The ladder** (each rung an optional, readable helper; maps to Thread 5's
lifecycle, applied to the *act of developing*):

```
Stage 0           →  dev-setup       →  setup          →  check
get git + repo        workstation        product deps      run gates
(pre-clone)           (post-clone)       (venv/tools)      (exists)
≈ Provision-for-dev   ≈ Startup-for-dev                    ≈ Runtime-for-dev
```

**Decision (recorded): "guided skeleton."** Readable, consent-first scripts (incl. a
**native GUI folder picker**); the kit ships + scaffolds the skeleton, and a
downstream project may serve it as a **GitHub Release asset** (manual upload, stable
download URL) — signing / turnkey packaging is *their* call and cost. **Rejected:** a
compiled/opaque binary, silent or timeout-default auto-install, and hand-rolled
SSH-key/account auth (**delegate to `gh`/host CLI**). **Not chosen:** document-only
(too thin for start-from-zero).

**Three toolchain layers, named once in PROCESS.md** (this resolves the conflation
the user flagged):
- **Process toolchain** — none; stdlib Python; the kit's floor. *(exists)*
- **Product toolchain** — language/stack tools (ruff/pytest reference);
  `setup.{sh,ps1}`. *(exists)*
- **Developer workstation** — what a human needs to view/render/edit/run: a runtime,
  git, an **offline** Markdown+Mermaid renderer, optionally an IDE + a domain viewer.
  *(new)*

Plus the **offline-render principle:** legibility artifacts must render with
**local, offline** tooling — never a cloud service (the kit already chose
Mermaid-in-Markdown for exactly this, §3). Point at a local renderer (VS Code + a
Mermaid preview extension, or `@mermaid-js/mermaid-cli`); a Kroki/PlantUML
*container* only if a project outgrows Mermaid (§3 already says so).

**Parts:**

**A — PROCESS.md (prose).** Name the three layers + the onboarding ladder + the
Provision-for-development framing + the offline-render principle. Single-source;
mind the 12k AGENTS.md cap (no AGENTS.md clause; a README echo is fine).

**B — Stage-0 onboarder template** `onboard.template.{cmd,command,sh}` (one
readable entry point per platform). Flow: **print what it will do → user accepts →
native folder picker** (PowerShell `FolderBrowserDialog` · macOS `osascript 'choose
folder'` · Linux `zenity`/CLI fallback) **→ ensure git** (winget/choco · brew · apt)
**→ HTTPS clone** (`gh auth login` only if push access is needed) **→ END BANNER →
kick off `dev-setup`.**
- **End banner (required), printed right before the `dev-setup` consent prompt:**
  prominently shows the **cloned repo directory path** and the line *"If you'd like
  an AI agent to manage your changes (commits, pushes, reviews) for you, point it at
  this directory."* Then the prompt that launches `dev-setup`.
- `bootstrap.py` scaffolds it with the project's clone URL filled in (a templated
  placeholder). The project may attach the file to a Release (documented option; the
  kit does **not** run a release CI action).

**C — dev-setup template** `dev-setup.template.{sh,ps1}` (launcher tier, readable,
with an **EDIT FOR YOUR STACK / DOMAIN** block like `check.py`). Tiers: `--check`
(**default** — detect + report, install nothing) · *baseline* (runtime + git +
offline renderer + test-ability) · *full* (+ IDE + extensions; **opt-in**, skipped
when headless/non-interactive). **Contributor profiles:** a *code* profile (runtime
+ linter + test tools) and a *domain* profile (git + offline renderer + a **domain
viewer the project fills in** — CAD/KiCad/image/publication). Domain viewers are
project-customized; the kit can't pre-know them.

**D — Meta-repo dogfood.** A concrete `dev-setup` for *this* repo (python, ruff,
pytest, a Mermaid-capable viewer) so the kit supports itself; the *template* ships
only the universal baseline + EDIT slots. A meta-repo release-served onboarder is
low value — deferred.

**Steps:** PROCESS.md edits (A) + README echo; new template scripts (B, C) +
`bootstrap.py` MAPPING + docstring; meta-repo dogfood (D); tests.

**Tests:** bootstrap file-list asserts the new templates scaffold; where a shell
exists, a smoke test that `onboard` is syntactically valid and `dev-setup --check`
runs and reports (mirroring the existing `sh` pre-commit e2e, skipped where no
shell). Cross-platform/GUI/auth behavior beyond that is **manually verified per OS**
(weak automated net — see Model tier). Verify intra-doc links; AGENTS.md ≤ ~12k.

**Risks:** scope creep into a general-purpose installer / IDE-provisioner — keep
helpers thin, optional, consent-first, readable; the kit owns the *skeleton +
structure*, **not** signing/distribution or the domain-viewer matrix. Cross-platform
shell + native pickers are fiddly and weakly testable — manual per-OS verification.
Unsigned-script OS warnings (SmartScreen/Gatekeeper) are unavoidable without signing
— document a "download, read, run" expectation; **never pipe-to-shell**. Don't force
git literacy — the end banner + agent handoff is the non-coder's path.

**Done-when:** PROCESS.md names the three layers + ladder + offline-render
principle; `onboard.template.*` and `dev-setup.template.*` scaffold via bootstrap,
consent-first and readable, with the end banner naming the repo dir + agent handoff;
the meta-repo dogfoods `dev-setup`; no compiled binary, no hand-rolled auth; links
pass; `pytest -q` green.

**Model tier — decision + cross-platform/auth/GUI design on the strong model; prose
+ wiring Sonnet-able.** Part A (prose) and the bootstrap/README wiring are
Sonnet-able once specced. Parts B/C touch **install, auth, and credentials with a
weak automated backstop** (pytest covers `.py`, not deep cross-platform
`.cmd`/`.command`/`.sh` or GUI pickers) — design and review on the strong model with
**manual per-OS verification**; don't treat green pytest as proof the
Windows/macOS/auth paths work. **Sessions:** A is prose (could ride Session E);
B+C+D are a solo, multi-platform script build — its own session, higher-care than
the Python `check_*` builds.

**Parked follow-on (not in scope) — agent selection & auto-provisioning.**
Automatically choosing and installing an AI agent (Claude Code / others) for the
domain contributor is **parked**: agent tooling is fast-moving, opinionated, and
tool-specific (the same anti-lock-in logic the kit applies to ruff/IDEs/Serena). For
now the onboarder's **end banner** simply tells the user they *can* point an agent at
the repo directory. Revive as its own thread only if a stable, neutral
agent-provisioning path emerges.

> **✅ Revived + resolved 2026-07-02 as WI-1.9** (Post-plan WI log below). The
> *auto-install* half stays parked (still opinionated/tool-specific), but the
> **agent-selection + skills** half is now built: `bootstrap.py --agents
> claude|gemini|both|none` asks (interactive) which agent the user already has and
> materializes that agent's neutral skills — anti-lock-in preserved (neutral
> `skills/` source; `none` default keeps the scaffold agent-neutral). Also
> resolves the scratch "AGENTS.md budget vs. guardrail coverage / what AI skills
> should the template make available" open item and the Thread-28-adjacent "should
> the onboarder ask about agent use" question (answer: at *bootstrap*, not the
> onboarder — the user has an agent by repo-setup time).

---

## Thread 16 — Verifying non-code artifacts (stub: sketch now, build later)

**Status: ⏳ stub, added 2026-06-30.** A spin-off of the Thread-15
non-code-contributor discussion; **deliberately not specced to depth** — confirmed
with the user as a separate, later thread.

**Goal (sketch):** give projects whose deliverables are non-code (art/UI, CAD,
electronics, publications) a way to *verify* those artifacts within the SN→SR→LLR→TC
spine. The kit **already** models this at the *method* level — §4's `Demonstration`
/ `Inspection` / `Manual` methods + "every SR needs ≥1 TC regardless of method
(human methods record the procedure)" already express "a human or agent reviews the
rendered output against acceptance criteria." What's missing is **product-layer
tooling**: render-on-change, visual/image diff, PCB design-rule checks, publication
lint — none of which the kit should own (stack/domain-specific), but which it should
**name and route**, the meters-vs-comparator split from Thread 11: the project
renders/diffs; the kit's gate records the verification.

**Open questions (for when this is specced):** how binary/large artifacts interact
with "review the source, not the render" (§3) when the *source* is itself binary;
whether a generated, gitignored "render report" (like the perf/trace composites) is
the review surface; how an AI agent's visual review is recorded as an honest TC
verdict (Demonstration, not Test).

**Model tier:** spec on the strong model when revived (a methodology-extension
decision); any concrete renderer/diff helper is product-layer and project-owned.

**Update (WI-1.7, 2026-07-02):** partially advanced. WI-1.7 landed the
**`Attest`** verification kind (a named human's recorded judgment — the honest TC
verdict this stub asked about, made a first-class method) and the `ASSET-###`
binary-asset provenance registry (tracks provenance/license/hash *about* the
un-diffable asset in text — the "review the source is binary" open question,
resolved by reviewing the *record* instead). The **"asset manifest freshness
check"** (verify each ASSET row against its store) is named as a **deferred
product-layer idea in this stub's family** (process-options.md "Binary assets").
Still open: render-on-change / visual-diff / design-rule tooling and the
gitignored "render report" review surface.

---

## Thread 17 — Voice policy + the agent-layer carve-out

**Status: ✅ landed 2026-06-30** (Session E, the clubbed prose batch). Framing
confirmed with the user 2026-06-30. `PROCESS.md` §5 gained a **"Voice policy —
warmth has a layer boundary"** paragraph, placed right after the verdict-protocol
block it protects: the **human-facing vs. machine/agent-facing split** (findings,
verdicts, subagent prompts, registry cells, commit messages stay literal/terse/
no-whimsy), the **restrained default** voice ("direct and concrete; dry wit at
most; never at the expense of clarity or honesty"), and the **optional, named
tone knob** — never a baked-in persona. **Deviations from the spec as written:**
(1) landed in **§5**, not §6 — the thread offered both as a home, and §5 is the
section the carve-out most directly protects (the findings/verdict format whimsy
would corrupt); (2) no `AGENTS.template.md` pointer and no `KICKOFF_PROMPT.md`
tone note — the file's at 11,998/~12,000 chars with three threads (13/17/18)
competing for the same slack this session, so the coordinated call (Thread 12's
note) was PROCESS-only across all of them; the optional KICKOFF note was likewise
skipped to keep the session's footprint to its specced files. `pytest -q`:
unaffected (prose only).

**Goal:** let a project add warmth/levity to **human-facing** agent output without
poisoning the **machine/agent-facing** layer — by stating a voice policy with an
explicit carve-out, a restrained default, and an optional project-tunable dial.
Applies to this repo and repos templated from it.

**Why:** personality is a human value, but agent-driven development runs most of its
traffic **agent-to-agent** (subagent prompts, `status.md` findings, §5 verdicts,
registry cells, commit messages). Levity there costs tokens (against the open
"Agent verbosity" concern + the 12k AGENTS.md cap), introduces **parse ambiguity**
for the next agent (irony/understatement is exactly what a downstream parser
mis-reads), and **erodes the honesty/severity signal** the kit's spine depends on.
The valuable rule is the carve-out, not the humor.

**Decision (recorded):** ship the **carve-out + a restrained default + an optional
dial**, **not** a baked-in persona — a *template* can't pick a tone that fits a
medical-device repo and a game studio both. Default voice = "direct and concrete;
dry wit at most; never at the expense of clarity or honesty."

- **The split:**
  - **Human-facing** (CLI/chat narration, kickoff greeting, release-checklist
    intro): warmth + light **dry wit** welcome.
  - **Machine/agent-facing** (findings, subagent prompts, §5 verdicts, registries,
    commit messages): literal, terse, structured — **no whimsy.**
- An **optional, project-tunable tone knob** (a named setting, like
  `COVERAGE_THRESHOLD` is a named constant) so a project dials levity up/down;
  default restrained.

**Steps:**
- **PROCESS.md (single-sourced home):** state the voice policy + the
  human-vs-machine carve-out once, near §5 (the verdict/findings protocol it
  protects) or the §6/communication area; name the optional tone knob + restrained
  default.
- **AGENTS.template.md** is at the ~12k cap — no new clause unless paid for by
  tightening; at most a 3–4-word pointer in the existing "Communication style" /
  working-agreement to the PROCESS.md policy. Prefer the pointer iff ≤ cap, else
  PROCESS-only.
- Optionally a one-line tone note in `KICKOFF_PROMPT.md` / the release-checklist
  intro showing where human-facing warmth is appropriate.

**Tests:** none (prose). Verify intra-doc links (`check_docs.py`); AGENTS.md ≤ ~12k.

**Risks:** undercutting the kit's trustworthy/serious brand — default to restraint,
levity opt-in. Personality leaking into the machine layer — the carve-out is the
guard; state it plainly. Don't prescribe a persona (ages badly; wrong for many
domains). Tension with the "Agent verbosity" goal — resolved by
human-facing-only + dry-wit-not-padding.

**Done-when:** PROCESS.md names the voice policy + the human-vs-machine carve-out +
an optional tone knob with a restrained default; AGENTS.md points at it within
budget or stays unchanged; links pass; no machine-layer artifact invites whimsy.

**Model tier — Sonnet-able end to end** once specced: prose mirroring the kit's
existing communication-style + single-source patterns; the only care point is the
AGENTS.md byte budget (a strong-model glance before commit, like Thread 13).

---

## Thread 18 — Model/agent-tiering discipline (recommend + record, not enforce)

**Status: ✅ landed 2026-06-30** (Session E, the clubbed prose batch). Honest
framing confirmed with the user 2026-06-30. This **formalizes the per-thread "Model
tier" convention this very plan has been using ad hoc** since 2026-06-30.
`PROCESS.md` §6 gained a **"Model/agent tiering — recommend + record, not
enforce"** paragraph after the existing review-depth-triage bullets: names the
triage axis as also a **tiering** axis (strong model for planning/decomposition/
decisions/high-risk; cheaper tier for mechanical/well-specced/low-risk), states
the **gates-as-backstop** rationale (tiering down is safe specifically because a
cheap executor can't silently drift past a deterministic check), the
**recorded-tier-hint** convention generalizing the ad-hoc "Model tier:" lines this
very plan has used since Thread 12, and **host-specific levers as optional,
named-by-category examples** (a strong-model-plans/cheaper-model-executes mode,
per-subagent overrides, a model-selection command) — explicitly **not** a
model-selection engine. **Deviations from the spec as written:** (1) no
`AGENTS.template.md` pointer and no `STATUS.template.md`/`KICKOFF_PROMPT.md`
note — same cap-and-scope call as Threads 13/17 this session (PROCESS-only); (2)
host levers are named **inline in the §6 paragraph** rather than in a separate
note by `agent-hooks/README.md` (the thread's other suggested home) — that file
is specifically about per-agent *hook* configs, a topical mismatch for
model-selection levers, so keeping it in one self-contained §6 paragraph avoided
spreading the convention across an unrelated doc. `pytest -q`: unaffected (prose
only).

**Goal:** bake a model/agent efficiency discipline into the template — classify work
by kind and route it to an appropriately-tiered model/agent — at the only honest
level available: **stated discipline + a recorded tier hint**, with host-specific
enforcement as documented optional examples. The kit **cannot force** a model (a
host concern that doesn't standardize — the Thread 0b lesson), and tiering can't be
gate-enforced (gates run *after* the work); say so plainly.

**Why:** agent-driven development wastes budget when a strong model does mechanical
work or a cheap model attempts judgment-heavy decomposition. The kit already has the
seeds — **§6 review-depth triage** is a tiering scheme for *review effort*, and the
per-thread Model-tier notes (added 2026-06-30) are the same idea for *execution*.
The kit's distinctive enabler: **deterministic gates + tests mean a cheaper executor
can't silently drift**, so tiering-down is *safe here specifically* in a way it
isn't in an ungated workflow — that's the insight to centralize.

- **Task-classification → tier mapping**, extending §6 (same risk axis it already
  triages for review depth): planning / decomposition / decisions / high-risk
  review → strong model; mechanical execution / well-specced builds / prose /
  low-risk → cheaper tier.
- **Gates-as-backstop:** state that tiering-down is safe *because* the harness/gates
  catch regressions — the reason the kit can recommend a cheap executor where an
  ungated process couldn't.
- **Recorded-tier convention (generalize the dogfooded one):** any planned unit of
  work — a thread, a phase, a `status.md` task — may carry a **model-tier hint** an
  agent reads. It's metadata, not a hook ⇒ agent-neutral + portable. Promote the
  ad-hoc "Model tier:" line (Threads 12–17) to a stated convention.
- **Host levers = optional, documented examples** (the `agent-hooks/` pattern from
  Thread 0b): Claude Code opusplan (Opus plans / Sonnet executes) + per-subagent
  model overrides + `/model`; Gemini/Codex equivalents. Named per host, never
  required — the kit states the policy, the host provides the lever. (Generic form
  of the "advisor strategy" / opusplan pattern — reference the *pattern*, not a
  vendor blog as a dependency.)
- **Honesty (critical):** classify as **guidance + a recorded hint, not
  enforcement** — an agent/human can ignore a hint, the same status as any AGENTS.md
  directive (intent, not guarantee; Thread 0b put *enforcement* in the neutral
  substrate, which isn't available for model choice). **Do not** build a
  model-selection engine (DonnyClaude's Claude-specific `model-profiles` path —
  rejected for the same stack-agnostic / agent-neutral reasons as the rest of that
  survey, Thread 12).

**Steps:**
- **PROCESS.md §6 (the triage home):** add the task→tier mapping + the
  gates-as-backstop rationale + the recorded-tier-hint convention, framed as
  guidance not enforcement.
- **Document host levers** as optional examples (a short note by §6 or in the
  `agent-hooks/` README — the existing optional-extras home), clearly per-host and
  non-required.
- **AGENTS.template.md:** at most a thin pointer if the cap allows; else
  PROCESS-only.
- Optionally note the convention in `STATUS.template.md` (a task may carry a tier
  hint) and/or `KICKOFF_PROMPT.md`.

**Tests:** none (prose). Verify intra-doc links; AGENTS.md ≤ ~12k.

**Risks:** over-promising "force" — frame honestly as recommend+record.
Over-engineering into a model-selection engine — rejected; keep to policy + hint +
host examples. Dating the doc by naming models/tools — name the *pattern* + per-host
*category* with `e.g.` (the Thread 8 mitigation). Tool-lock — the convention is
metadata; the levers are optional per host.

**Done-when:** PROCESS.md §6 names the task→tier mapping, the gates-as-backstop
rationale, and the recorded-tier-hint convention (framed as guidance, not
enforcement); host levers are documented as optional examples; no model-selection
engine added; links pass.

**Model tier — Sonnet-able to execute** once specced (prose extending §6 + the
agent-hooks optional-extras pattern); the dogfood irony — this thread *defines* the
convention the plan already follows — makes it low-risk. Strong-model glance only
for the AGENTS.md cap, if touched.

---

## Thread 19 — Multi-module scoping (single-repo sub-systems)

**Status: ✅ landed 2026-06-30** (Session H). Multi-module scoping shipped as
prose + a light EXAMPLE slice + a confirming test — **no script change** (the
in-thread decision). New **PROCESS.md §10 "Project scale — one module, several
modules, several repos"** (appended after §9 so nothing renumbers — the Thread-10
precedent): the **escalation ladder** (rung 1 single-module default · rung 2
several-modules-one-repo · rung 3 multi-repo+coordinator), decide-at-creation,
bias-low, revisitable, with rungs 1–2 detailed and rung 3 named + pointed forward
to the multi-repo model (Thread 20/Session I) in **link-safe prose** (no dangling
link to a not-yet-existing doc); the **several-modules-in-one-repo model**
(sub-trees grouped by the existing LLR `Module` / optional SR·TC `Area` columns,
per-module domain hats via §1); **integration TCs for the seams**
(`Tier=Full`/`Release`); and **`IF-###` applied within a repo** (counterpart names
the other module; both rows in one `interfaces.csv`). **Scoping decision —
convention, not a flag:** the kit ships **no** `--module`/`--area` filter on
`trace.py`/`check.py` — a per-module gate would either hide the cross-module seams
(a false "green" masking exactly the integration gaps this thread makes
first-class) or need real seam-vs-orphan machinery; the whole-repo `trace.py
--strict` 0-orphan gate already spans every module + seam, so per-module *review*
is a reading convention over columns that already exist. `EXAMPLE.md` gained **§9**
(a two-module `export`↔`delivery` repo: `Area`-tagged SRs, an intra-repo
`IF-001`/`IF-002` pair, and an integration `TC-050`) + a "What to copy" bullet;
both READMEs got a project-scale scope note / tuning knob. New test
`test_area_column_is_schema_safe` mirrors Thread 5's lifecycle test (an `Area`
column passes `--strict-schema`), making the convention's schema-safety explicit.
**Deviations from the spec as written:** (1) the new section landed as **§10** (an
appended end-section) rather than literally "near §1/§8", to avoid renumbering
§1–§9 and every `§N` cross-reference (edit-conservatively) — this means Session I's
multi-repo doc should be **§11 or `MULTI_REPO.md`**, not §10; (2) **no `AGENTS.md`
change** (already cap-safe per the spec — the guidance stays single-sourced in
PROCESS.md). `pytest -q`: **117 passed, 1 skipped** (was 116/1; +1).

**Original queued note (for provenance):** near-term; mostly prose + light
template. The four multi-repo decisions were confirmed with the user 2026-06-30
(see Thread 20); this is the **cheaper first rung** of that track.

**Goal:** state explicitly that the kit is **single-module by default**, and
describe how **one repo** can hold **several modules/sub-systems** without new
machinery — sub-trees of the SN→SR→LLR→TC spine grouped by `Module`/`Area`, with
trace + gates scopable to a module and explicit **integration** TCs for the seams.

**Why:** the kit reads as single-module today (the scratch note), but the
registries already carry `Module`/`Area` columns, the arch map already surfaces
internal dependencies and makes layering invariants auditable, and `IF-###` (§8)
already handles contracts between parts. So "multi-module in one repo" is mostly
*naming and scoping what exists* — not building — and shipping it first gives a
working multi-module project that de-risks the Thread-20 coordinator.

- **State the default + the extension** in PROCESS.md: single-module by default; a
  larger project may host several modules in one repo, each a sub-tree tagged by
  `Module`/`Area` (already optional columns — the Thread 5/10 pattern), with its own
  domain hat(s) where the scope needs them (§1 already allows this). State the
  **escalation ladder's rungs 1–2** (single-module → multi-module-one-repo) here and
  point at Thread 20 for rung 3 + the rarity / decide-at-creation stance —
  multi-module is a step taken only when a repo genuinely grows several sub-systems,
  never a default.
- **Module-scoped trace + gates:** name the convention for closing a module's own
  G2/G3 within the repo while the repo-level gate covers the whole. **Decide
  in-thread:** purely conventional (filter on the existing `Area`/`Module` column)
  vs. a cheap `--area`/`--module` flag on `trace.py`/`check.py` — bias to convention
  + existing columns unless a flag is cheap and clearly useful.
- **Integration TCs for the seams:** module boundaries get their own TCs (shared
  contracts are the §8 `IF-###` fixture tests; intra-repo seams get integration
  TCs, likely `Tier=Full`/`Release`) so the seam isn't an untested gap.
- **`IF-###` applies *within* a repo too** (between modules), not only across repos
  — same contract/owner/version discipline, no cross-repo machinery.
- PROCESS.md home; no AGENTS.md clause needed (cap-safe).

**Steps:** PROCESS.md edits (default + a multi-module section near §1/§8); an
optional EXAMPLE.md two-module illustration (intra-repo `IF-###` + an integration
TC); confirm the trace/check scoping decision; README echo if warranted.

**Tests:** if a scoping flag is added, importable unit tests like the other
scripts; else confirm the optional-column tolerance covers `Module`/`Area`
(precedent: Thread 5's `test_lifecycle_column_is_schema_safe`). Verify links;
AGENTS.md ≤ ~12k.

**Risks:** creep toward the full coordinator — Thread 19 stays *single-repo*;
cross-repo is Thread 20. Adding flags the kit doesn't need — prefer convention +
existing columns. Don't imply every project is multi-module — single-module stays
the default and simplest path.

**Done-when:** PROCESS.md states the single-module default + the single-repo
multi-module model (sub-trees by `Module`/`Area`, module-scoped gates, integration
TCs, intra-repo `IF-###`); EXAMPLE optionally shows it; any scoping flag has tests;
`pytest -q` green.

**Model tier — mostly Sonnet-able prose** once specced; **if** a trace/check
scoping flag is built, that small slice is a script change (strong-model glance for
the flag contract, Sonnet to implement against `pytest`). Strong-model glance for
the AGENTS.md cap only if touched (likely not).

---

## Thread 20 — Multi-repo coordinator model (design-first)

**Status: ✅ landed 2026-06-30** (Session I — design-first, the most decision-heavy
thread). The confirmed model is documented and the thinnest schema seams shipped;
heavy tooling routed to Thread 21. New **`project-trajectory/MULTI_REPO.md`** (a kit
*reference* doc like `EXAMPLE.md`, marked *design — mechanism deferred*): leads with
the rarity stance + escalation ladder (default rung 1, decide-at-creation, bias-low,
revisitable), the coordination-vs-orchestration line, the confirmed model (SR-tier
handoff, coordinator-as-Integration-hat, catalog-not-copy interfaces,
assemblies-as-config, mechanical-aggregation gating, async-text coordination), the
two requirement scopes (module vs composition, the latter verified by a delegated
**plant** repo), the schema seams, and the Thread-21 deferrals. **Schema seams
shipped (in-thread decision — the smallest traceable set):** new
**`registries/modules.template.csv`** (`MOD-###`: `MOD-ID, Module, Repo,
DelegatedSRs, Version, Type, Owner, Notes`) validated by `trace.py` **within the
coordinator repo** — each `DelegatedSRs` must resolve to a real coordinator SR and a
malformed/duplicate `MOD-` id fails (the `PB-###` precedent), but an **empty**
delegation is allowed for external/reused parts referenced only via the interface
catalog; held out of the placeholder/schema sweeps like PB. The optional `Delegated`
(coordinator SR) and `ParentRef` (module SN) markers are documented as **schema-safe
conventions**, no code (the `Area`/`Lifecycle` tolerance). `EXAMPLE.md` **§10**
sketches a two-repo `export`/`delivery`/`plant` product (delegated SR→module SN, a
`modules.csv` incl. an external purchased part, an owned-vs-coordinator-owned
`IF-###` pair, the composition-scoped SR verified by the plant repo, and the honest
delegated-SR-orphan limit). `PROCESS.md` §10 rung 3 now names `MULTI_REPO.md`
(link-safe backtick prose, matching Thread 19's forward-pointer); both READMEs +
`CLAUDE.md` repo map cross-link it; `KICKOFF_PROMPT.md` poses a **Project scale**
brief question biased to single-repo; `bootstrap.py`'s docstring documents the
`--coordinator` variant as a **deferred, not-built** concept. New
`tests/test_modules_registry.py` (7 cases). **Deviations from the spec as written:**
(1) the design landed as a separate **`MULTI_REPO.md`**, not PROCESS §11 — §10 rung 3
already promised "documented separately," and keeping multi-repo an optional layer a
single-repo project never reads argues against bloating PROCESS.md (the `EXAMPLE.md`
precedent: a kit reference doc named in prose, not bootstrapped); (2) **`modules.csv`
is *not* added to the default bootstrap MAPPING** — it is coordinator-only, so
scaffolding it into every repo would contradict "single-module never sees it"; the
documented coordinator variant (deferred) places it, and `trace.py` tolerates its
absence; (3) the `bootstrap --coordinator` mode is **documented + stubbed**, not built
(bias to documented+stub, per the spec); (4) **no `AGENTS.md` change** (~12k cap).
`pytest -q`: **124 passed, 1 skipped** (was 117/1; +7).

**Refinement (2026-07-01, post-landing — design-only, no code).** Two cross-repo
interface questions from the next-considerations scratch batch were resolved into the
design doc: (1) **id namespacing** — each repo owns its local `IF-###` space, so the
coordinator catalog keys interfaces by a **coordinator-level id (`CIF-###`)** mapping
to the owner tuple *(repo, IF-id, version)* + consumer pins (chosen over a bare
qualified pair because it stays stable while its binding varies by assembly — it
composes with assemblies-as-config); (2) **content/version drift** — the coordinator
runs a mechanical **version-reconciliation** check (owner-current vs each consumer-pin,
weighted by §8 `Stability`) and *sequences* the dependent repo's contract-test re-run,
while the interface's own §8 fixture judges actual compatibility and the human signs a
real break — the same three-layer split as §3.5 gating. Folded into `MULTI_REPO.md`
§3.3/§3.7/§6/§7 + `EXAMPLE.md` §10; the catalog **registry + reconciliation tool are
routed to Thread 21** (deferred mechanism, still design-first — no code this session).

**Original queued note (for provenance):** Core model **decisions 1–4 confirmed with
the user 2026-06-30**; this thread **documents the model and defers most mechanism**
to Thread 21.

**Goal:** name, in a design/architecture doc, how the single-module spine extends
across **separate repositories** under a **coordinator** — **without becoming a
multi-repo build/orchestration engine** (the §8 guardrail; see *Coordination vs.
orchestration* below for the precise line). Capture the north star;
build only the thinnest enabling seams; route the heavy/automation parts to Thread
21 stubs.

**Why:** large products span repos (independent versioning, ownership, access). The
kit already has the seams — §8 `IF-###`, the §1 Integration/Coordination hat, §9
`PB-###`, and the recursive spine — so multi-repo is mostly *extending them across a
boundary* + naming the coordinator role, not new machinery. But it is genuinely hard
and uncertain, so this thread is design-first: decisions + a documented model now,
mechanism later.

**Rarity & the escalation ladder (default low; decide at creation) — the shipped
docs must lead with this.** Multi-repo is for **extreme-scope** products only and
should be **rare**; the design doc opens by saying so, not by selling it. State a
clear ladder with the **default at the lowest rung**, climbed only when scope forces
it:
1. **Single module, one repo** — the default for almost every project.
2. **Multiple modules, one repo** (Thread 19) — when a repo grows several sub-systems
   but still builds/releases as one.
3. **Multi-repo + coordinator** (this thread) — **only** when modules genuinely need
   *independent* versioning / ownership / access / release cadence at a scale one
   repo can't sustain.

The choice is made **at project creation** (KICKOFF / `bootstrap` / G1) and **defaults
to rung 1**: a project starts single-repo unless its scope *demonstrably* demands
higher, and a reviewer should push back on a premature jump. It is **revisitable** —
start single and **promote a module to its own repo later**, when it proves it needs
independence (far cheaper than a speculative split). So KICKOFF/bootstrap pose the
scope question and bias low; "you almost certainly don't need this" is the right tone
in the shipped docs. (Thread 19 owns stating rungs 1–2; this thread owns rung 3 + the
rarity stance.)

**Confirmed model (decisions 1–4, 2026-06-30):**
- **Recursive handoff at the SR tier.** A repo boundary is a *cut in the
  decomposition tree*. The coordinator decomposes SN→SR; an SR it chooses to
  **delegate** to a module repo is tagged delegated and becomes that module repo's
  **SN** (its reason-to-exist); the module's SN back-links the coordinator's SR id.
  *Not* LLR→SN — LLR is code-local; the delegated unit is a sub-system, which is
  SR-shaped.
- **Coordinator = the Integration/Coordination hat (§1), elevated to a repo.** It
  holds the product-level SN→SR→TC chain + an **assembly definition** + an
  **interface catalog**; it contains **no functional build output** except the
  assembly definition.
- **Interface catalog = pointers, not copies (single-source-of-truth).** Each
  interface's spec lives once in its **owner** — the owning repo's `IF-###`, or, for
  purchased/external/reused parts no repo builds, a coordinator-held `IF-###` row
  that *is* the owner of record (linking the datasheet/part). The catalog
  **references** owner `IF-###` + adds only assembly-level *connection* info.
  Ownership follows the §8 ICD model; proliferation is accepted (the "16 standards"
  reality) and managed by owner-of-record, not central control.
- **Assemblies = configuration, not branches.** A product variant is an
  `assemblies/<name>/` configuration (module set + pinned versions + which SN/SR/TC
  apply), **not** a long-lived coordinator branch (branches model change-in-time,
  diverge, and can't be co-current).
- **Coordinator gating = mechanical aggregation, judgment escalated.** The
  coordinator (as agent) runs the *mechanical* cross-module gate — every module
  passed its own gates + integration tests green + catalog consistent — and surfaces
  only the *judgment* gates to the human. The human signs the **integration** gate;
  module agents gate the modules. This is the §6 review-depth triage at the
  coordinator level; it does **not** remove the human.
- **Cross-repo communication = async text + PR.** A delegated SR *seeds* the module
  repo's SN registry; module status flows back as referenced ids in a coordinator
  assembly/status doc (the STATUS.md pattern across the boundary). No live message
  bus / daemon.

**Coordination vs. orchestration — the line (clarified 2026-06-30).** "Orchestration"
means two different things; the §8 guardrail rejects one, the coordinator lives in
the other:
- **Build/runtime orchestration (rejected):** a *running engine* that checks out N
  repos, builds them in dependency order, links artifacts, and runs/deploys the
  whole. Infrastructure the kit refuses to impose (§8).
- **Requirement/interface/status coordination (all the coordinator is):** a
  *discipline over text* — trace across the boundary, keep interface contracts
  consistent + versioned, aggregate each module's *self-reported* gate status. Links,
  registries, PRs; no engine.

Each module **builds and gates itself** in its own repo (its own `check.py`); the
coordinator **reads** results and **sequences/triggers** downstream repos — it does
not build or run anything. The honest edge: actually *running* the assembled product
needs a run step, but that is **product-layer** (the project's CI/Make/compose — the
Thread 2 process/product split at larger scale): the coordinator **invokes and
aggregates** it; the kit ships none of it (Thread 21). **The absence of a central
build engine is the defining property of choosing multi-repo, not a compromise** — if
heavy central orchestration is wanted, that is the signal to use a monorepo (one
build, one `trace.py`): Thread 19's single-repo multi-module instead.

**The integration / "plant" environment is itself a delegated repo (or several), not
coordinator machinery.** A runtime test / simulation environment — assemble the
modules' built runnables + a **plant model that virtualizes their external inputs**,
then execute the assembly (SIL/HIL/E2E) — is a **first-class module the coordinator
delegates to**, exactly like a functional module: it has its own SN (delegated from a
coordinator SR), consumes the other modules' published artifacts, and **gates
itself**. So "deps are green → queue the plant repo to assemble + run" is still
*sequencing + triggering* (read status, dispatch CI / open a PR, pass version pins),
never the coordinator building or running anything. ("Plant" is the control-systems
term — the virtualized physical system; generalize it to *any* environment that mocks
the composition's external inputs: a test rig, a mock-service harness, a scenario
generator.) The **artifact transport** between repos (a package registry, OCI image,
CI artifact — the earlier "maven? local publish?" question) is **product-layer**, the
project's choice, Thread 21.

**Two requirement scopes — name them (the crux of this nuance).** A multi-repo
product has requirements at *two* levels, and conflating them is the trap:
- **Module-scoped** — a module's own SN→SR→LLR→TC, verified **inside the module
  repo**, scoped to what that module does in isolation.
- **Composition-scoped (emergent / integration)** — requirements that exist **only
  for the assembled whole** and that *no single module owns*: end-to-end behavior
  across A→B→C, closed-loop stability of a controller against its plant, cross-module
  latency/throughput, disturbance rejection. These live in the **coordinator's**
  SN→SR chain and are **verified by the integration/plant repo's TCs** (typically
  `Verification=Demonstration` — run the sim), *not* by any module. The handoff
  **generalizes the SR-tier rule**: a composition SR delegates to the **plant repo's
  SN** ("verify the composed product satisfies this"), exactly as a functional SR
  delegates to a functional module's SN. The plant repo is "the module whose
  deliverable is a runnable verification of the assembly."

**What this thread writes (thin):**
- A **design doc** (`project-trajectory/MULTI_REPO.md`, or a PROCESS.md §10)
  capturing the confirmed model, explicitly marked *design — mechanism deferred*.
- The minimal **schema seams** that are cheap + schema-safe (optional, like
  `Lifecycle`/`Area`): an SR `Delegated`/`ModuleRef` marker; a module SN `ParentRef`
  (the coordinator SR id); a coordinator `modules.csv` (module repo + delegated
  SR-refs + version + `Type=owned|external|reused`); the `IF-###` catalog-reference
  convention. **Decide in-thread** how much to ship now vs. stub — bias to the
  smallest set that lets a real two-repo example exist.
- A **coordinator `bootstrap` variant** concept (opt-in): scaffold a coordinator
  repo (no `src/` build; has assembly + catalog) vs. a module repo (normal kit + a
  `ParentRef`). Whether `bootstrap.py` grows a `--coordinator` mode now or it's
  documented + stubbed → decide in-thread (bias to documented + stub; repo
  creation/automation is Thread 21).
- Keep multi-repo an **optional layer**: single-module never sees it; single-repo
  multi-module (Thread 19) never needs it.

**Steps:** the design doc; the cheapest schema seams (optional columns + a
`modules.csv` template, if shipped); a worked **two-repo EXAMPLE** sketch
(coordinator SR → module SN; one shared `IF-###` owned by the module; one
purchased-part interface owned by the coordinator); README/PROCESS cross-links.
Defer tooling to Thread 21.

**Tests:** if any registry seam ships, schema-safety + back-link tests like
`IF-###`/`PB-###` (`trace.py` flags a `ModuleRef`/`ParentRef`/catalog row pointing
at an unknown id; optional columns don't break `--strict-schema`). Else prose;
verify links; AGENTS.md ≤ ~12k.

**Risks:** scope explosion / becoming a PLM or multi-repo build system — the §8
guardrail (no build system) + "design-first, mechanism deferred" + "optional layer"
are the controls. Cross-repo trace can't be one `trace.py` run — acknowledge it
(Thread 21), don't fake it. Over-shipping schema nobody uses — smallest set + a
worked example. Identity drift — opt-in coordinator variant, not a base change.

**Done-when:** a design doc **leads with the rarity stance** (escalation ladder,
default rung 1, decide-at-creation, revisitable) and records the confirmed model
(SR-tier handoff, coordinator-as-Integration-hat, catalog-not-copy interfaces,
assemblies-as-config, mechanical-aggregation gating, async-text coordination, the
coordination-vs-orchestration line, and the **two requirement scopes** — module vs
composition, the latter verified by a delegated plant repo); KICKOFF/bootstrap pose
the scope question and bias to single-repo; any shipped seam is optional,
schema-safe, traceable, with tests; the heavy tooling is routed to Thread 21;
`pytest -q` green.

**Model tier — strong model + human throughout the design; only the mechanical
seam-wiring is Sonnet-able.** The most judgment-heavy thread in the plan: the design
doc, the schema-seam decisions, and the two-repo example are strong-model +
human-in-the-loop. Once a specific seam's contract is locked, its registry template
+ `trace.py` back-link wiring + tests are Sonnet-executable against `pytest` (the
`IF-###`/`PB-###` precedent). **Do not** hand the model decisions to a lower tier.

---

## Thread 21 — Cross-repo tooling & automation (research stubs)

**Status: ⏳ stub (sketch only; each part its own future thread/decision),
added 2026-06-30; Session-I hand-off note added 2026-07-01.** The heavy/uncertain
mechanism deferred from Thread 20.

**Seams already shipped (Session I, build on these — don't re-derive).** Thread 20
landed the *recorded edges* this thread's tooling consumes, so a reviver starts from
data, not a blank page: `registries/modules.template.csv` (`MOD-###`, with `Repo` +
`DelegatedSRs` + `Version` + `Type`), the optional SR **`Delegated`** marker, and the
module-SN **`ParentRef`**. `trace.py` already validates `DelegatedSRs` *within* the
coordinator repo (the within-repo half of the join). The design + the honest limit
live in `MULTI_REPO.md` §6–§7. **This thread builds the cross-boundary half only.**

**Goal (sketch):** the tooling that *operationalizes* Thread 20's model, each part
genuinely research-grade and deferred:
- **Cross-repo traceability** — joining SN→SR→LLR→TC across repos (coordinator SR ↔
  module SN via `ParentRef`), likely a coordinator-side aggregation reading each
  module's *exported trace summary* (not one `trace.py` over many checkouts). Decide:
  **pull** (the coordinator clones/reads) vs. **push** (modules publish a trace
  artifact it ingests). **The concrete crux (Session I):** a *delegated* coordinator
  SR has no local LLR/TC, so a plain `trace.py --strict` in the coordinator repo
  reports it as an **orphan** — the `Delegated` marker records *why*, but only this
  join *closes* it (reconciling the coordinator SR against the module's returned
  gate status). Until it exists, a coordinator repo can't be 0-orphan for delegated
  SRs by machine; that gap is acknowledged, never faked (`MULTI_REPO.md` §6).
- **Coordinator gate aggregation** — the mechanical "all modules green + integration
  green + catalog consistent" check (Thread 20's gating model) as an actual stdlib
  command reading module-published gate/status artifacts, with escalation rules for
  the judgment gates.
- **Interface catalog + compatibility reconciliation** (added 2026-07-01, from the
  Thread 20 refinement) — the `CIF-###` catalog registry (owner tuple + consumer pins,
  `MULTI_REPO.md` §3.3) and the mechanical **version-drift check** (§3.7): flag a
  consumer pinned below the owner's *current* published version (weighted by the §8
  `Stability` tier), and **sequence the dependent repo's contract-test re-run** when a
  parent interface changes — the coordinator reconciles versions and triggers; the
  interface's own §8 fixture judges actual compatibility; the human signs a real break.
  Reads published versions across repos; never builds. Same **pull-vs-push** decision
  as the trace join.
- **Repo creation** — scaffolding a coordinator + N module repos (`bootstrap
  --coordinator`, `gh repo create`): agent/host tooling, optional, agent-neutral
  (the Thread 18 stance — name it, don't bake the automation in).
- **Module discovery / suggestion / reuse catalog** — finding existing reusable
  modules/parts for a delegated SR: an agent capability over a catalog, not a kit
  mechanism.
- **Cross-repo / cross-module E2E testing** — likely a **dedicated integration /
  plant repo** (Thread 20) that consumes the modules' published artifacts, assembles
  them with a virtualized-input plant model, runs SIL/HIL/E2E, and **gates itself**;
  the coordinator only sequences/triggers it. Includes the **artifact transport**
  between repos (registry / OCI / CI artifact — the "maven? local?" question) and
  where the **composition-scoped** TCs live (the plant repo). The "End-to-end
  testing" scratch note.

**Open questions when revived:** pull vs. push for trace/status; where cross-repo
E2E lives + who runs it; how much (if any) repo-creation automation is kit vs. agent
vs. host; keeping all of it stdlib + agent-neutral + no-multi-repo-build-system.

**Model tier:** each part is decision-first on the strong model + human when
revived; concrete stdlib tools (aggregators, comparators) are Sonnet-executable
against `pytest` once a part's contract is locked — the `check_*` shape, but only
after the model questions resolve.

---

## Thread 22 — Cost / economic NFRs (broaden the consideration prompt beyond software quality)

**Status: ✅ landed 2026-07-01** (Session J, the adversarial-review batch). §9's
consideration checklist gained a **cost / economics** category (unit/BOM,
licensing, cloud spend; procurement/supply-chain for hardware scopes) with the
explicit "25010 is software-quality-only, these sit alongside it" note and the
"a cost budget is just a `PB-###` row, compared by `check_perf.py` like any RAM
budget — no new mechanism" routing; `EXAMPLE.md` §8 gained a worked
unit-BOM-cost `PB-003` row (hypothetical hardware SR-040, `lower-better`,
`Gate=warn`, `Owner=Integration`); the SN template's NFR prompt now names cost.
**No deviations.** `pytest -q` (affected files): 11 passed.

**Goal:** make **cost / economic** non-functional attributes (unit / BOM cost,
licensing, cloud spend) a first-class *consideration* at G1, and make explicit that the
existing `performance-budgets.csv` already carries a quantitative cost budget with **no
new mechanism**.

**Why:** §9's NFR consideration checklist anchors on **ISO/IEC 25010**, which is a
*software-quality* model and omits cost entirely — so a mechatronics BOM or a cloud
bill never gets surfaced at G1, and cost-driven rework is discovered late. The
*mechanism* already exists: `PB-###` is **metric-agnostic** (a cost budget is
`Metric=Unit BOM cost, Unit=USD, Direction=lower-better, Gate=warn, Owner=Integration`),
and `check_perf.py` compares it identically to a RAM budget. The only gap is
**prompting** — naming cost as a category to weigh, and pointing at the registry that
already fits it. This is the same "emphasize the non-functional attributes so they
aren't forgotten" point Thread 10 makes, extended past 25010's software-only scope.

- **Broaden the §9 checklist** to name **cost / economic** (and, for hardware scopes,
  procurement / supply-chain / safety-of-supply) as a category to *consider* — a
  prompt, not a mandate — explicitly noting 25010 is software-quality-only, so the
  systems-engineering NFRs (cost, supply, physical safety) sit **alongside** it.
- **One worked cost `PB-###` row** in `EXAMPLE.md` §8 (e.g. unit BOM cost,
  `lower-better`, `Owner=Integration`) showing the registry already carries it — same
  shape as the RAM/VRAM rows, different metric.
- **A one-line prompt** in `stakeholder-needs.template.md`'s NFR note ("…performance,
  memory/size, **cost**, reliability…").

**Tests:** none new — `PB` is metric-agnostic, so a cost row already parses and
validates (`trace.py` back-links + `check_perf.py` compare); confirm the new EXAMPLE
cost row's `Refs` resolve and the gen_cases/link checks stay green. Prose + one row.

**Risks:** scope creep into a costing/BOM methodology — keep it a *consideration
prompt* + "cost is just a `PB` metric," never an ERP/BOM mechanism. Don't imply every
project needs it: a pure-software project skips it, like the rest of §9's checklist.

**Done-when:** §9 names cost/economic NFRs as a consideration distinct from 25010's
software-quality set; `EXAMPLE.md` shows a cost budget row; no new mechanism;
`pytest -q` green.

**Model tier — Sonnet-able prose** once specced (it's a checklist line + one EXAMPLE
row against the existing registry); strong-model glance only if it touches the
`AGENTS.md` cap (it should not — single-source in PROCESS.md §9, like Thread 10).

---

## Thread 23 — Documentation / publication composition (operator + technical manuals)

**Status: ⏳ stub (design-first; sketch only, each part its own future decision),
added 2026-07-01** from the next-considerations scratch batch.

**Goal (sketch):** name whether/how a composite **operator / technical manual** can be
*generated* from the doc flow — single-repo first, then the hard multi-repo /
multi-version composition — **without the kit becoming a publishing toolchain**.

**Why:** the kit already generates human artifacts from the registries
(`gen_release_checklist.py` from SN/SR/TC/IF), so the same **single-source,
generate-not-hand-maintain** technique could *scaffold* a manual: each SR is a
documented capability, each SN acceptance-intent a user-facing behavior, each `IF-###`
an interface doc, each `PB-###` a stated limit. But a full publishing pipeline
(PDF / DITA / static-site) and cross-repo / cross-version composition is heavyweight
**product-layer** — the same boundary the kit draws for perf *meters* and the diagram
render toolchain (§7): name the pattern, don't ship the engine.

**Open questions when revived:**
- Is an **operator manual still the right artifact**, or is a queryable /
  agent-navigated documentation surface the better concept for an AI-driven workflow?
  (The user's own framing — "maybe a completely different concept is needed.")
- Where does a **multi-repo / multi-version** composite manual live and who assembles
  it — a neighbor of the Thread 21 plant/coordinator (compose docs the way the plant
  repo composes runnables), reading each module's *published* doc artifacts?
- What is the **minimum generate-from-registries scaffold** worth shipping in-kit (a
  stdlib "manual skeleton from the registries") vs. what stays product-layer?
- Keep it **stdlib + offline-render (§7) + no vendored publishing engine**.

**Model tier:** decision-first on the strong model + human when revived (the "is a
manual the right artifact" question is a judgment call); a concrete stdlib scaffolder is
Sonnet-executable once the contract is locked — the `gen_*` precedent.

---

## Thread 24 — Adoption hardening (hook floor · active gate · SR↔SN rule · interpreter probe)

**Status: ✅ landed 2026-07-01** (Session J). Four fixes from the 2026-07-01
adversarial review, each **empirically confirmed against a fresh scaffold
before fixing**:

1. **Pre-commit hook no longer blocks G1-stage commits.** `trace.py` gained
   `--strict-integrity` (fails *only* on duplicate/malformed ids — the
   always-valid class); the hook and the optional `agent-hooks/` configs use it
   instead of `--strict`. Previously the hook wedged every commit from the
   first real SR until G2 decomposition completed (orphans are a *gate*
   criterion, not a mid-edit invariant) — the exact "never block a legitimate
   early-stage commit" promise Thread 0b made and the old wiring broke.
2. **The active gate is machine-readable and CI honors it.** New
   `gate.template` → `docs/gate` (bootstrap MAPPING; starts at `G1`);
   `check.py --gate` now defaults to it (explicit flag wins; garbage in the
   file fails loudly); `ci/check.yml` passes no gate on push/PR (a release tag
   still runs the full bar). Previously shipped CI ran G3/`all` from day one —
   red from bootstrap until deep G3 (verified: 3 failing steps on both
   triggers), training users to ignore it. Closing a gate = bump `docs/gate`
   in a reviewed commit (PROCESS.md §4/§7; STATUS template mirrors it).
3. **New orphan rule:** an SR with an empty `SN-Refs` fails `--strict` whenever
   the needs registry provides real SN ids — G1's "every SR links ≥1 SN",
   previously unchecked by machine until G3 `--strict-schema`.
4. **Interpreter probe:** `hooks/pre-commit` + `setup.sh` now *run* each
   candidate (`"$cand" -c ""`) instead of trusting `command -v` — the Windows
   Store `python3` alias exists on PATH but doesn't run.

Also reconciled: KICKOFF_PROMPT drift (stale `STEPS` → `steps()`; G3 gained its
test-first clause; harness description names doc-navigability + `docs/gate`).
Tests: hook orphan test rewritten to the integrity contract (+ the G1-stage
regression case), `--strict-integrity` + SR-no-SN trace tests, `docs/gate` in
the bootstrap file list, and a gate-file resolution test proving a fresh
scaffold's default (CI) run is green. **No deviations.**

## Thread 25 — Retrofit path (ADOPTING.md + no vacuous arch-map pass)

**Status: ✅ landed 2026-07-01** (Session J). The kit's quick-start was
new-repo-shaped; adopting into an **existing** repo (code, history, CI, a
non-Python stack — the review's target case) was undocumented, and on a
non-Python repo `gen_arch_map.py --check` passed **vacuously** forever (an
empty map is always "fresh") while the docs still promised drift-proofing.
Shipped: **`ADOPTING.md`** (a reference doc like `EXAMPLE.md`, not scaffolded) —
bootstrap-collision resolution (`.gitignore`/CI/pytest.ini merges; the
`core.hooksPath`-overrides-existing-hooks caveat), product-step rewiring, the
**port-or-explicitly-drop** rule for the two Python-reference generators (the
marker block is the porting contract; never leave a vacuous pass), and
backfill-from-the-boundary requirements guidance (`docs/gate` starts at G1
honestly; new work gets the full spine; existing code earns rows when touched).
`gen_arch_map.py` now **warns on stderr when it scans zero source files**
(still exit 0 — pre-code repos are legitimate), naming the hazard and pointing
at ADOPTING.md; test added. Kit README + meta `CLAUDE.md` cross-link it.
**No deviations.**

## Thread 26 — AGENTS.template.md trim (restore cap headroom, enforce the budget)

**Status: ✅ landed 2026-07-01** (Session J; trimming confirmed with the user
over the alternative of dropping the cap doctrine). The template sat at
**11,998/~12,000 chars** while telling downstream users to fill the Project
section and add rules — any real project busted the Gemini cap on first use,
contradicting the byte-discipline Sessions A–I maintained. Compressed wording
(not rules) **11,998 → 9,702 bytes**: every rule and every externally
referenced heading/bullet kept ("Comment for humans — and the map", "Define
the interface (contract) at the code", "Right-size the solution", "Working
agreement", …). The freed budget paid for the pointers late threads skipped:
`docs/gate` in the harness bullet and the §3 right-sizing-guardrails +
`SHORTCUT:` pointer in the Right-size bullet. **Creep guard** (the user's
stated worry): the Customizing note now names the budget ("pay for a new rule
by tightening another"; keep ≥2k headroom) and a new meta-repo test
(`test_agents_template_stays_within_size_budget`) fails the suite past
**10,000 bytes**. **No deviations.**

## Thread 27 — PROCESS.md verbosity squeeze + core/optional split (queued; solo session)

**Status: ✅ landed 2026-07-01 (solo session).** PROCESS.md compressed
**51,406 → 42,932 bytes** (−8,474, ~16.5%) with **§-numbering held stable**
(§1–§10 intact — the safer arm of the plan's "keep numbering stable **or** full
grep-and-reconcile" constraint, since `§N` refs pervade 41 files), so no external
cross-ref moved. New companion **`PROCESS_OPTIONS.md`** (14,434 bytes) holds the
relocated opt-in detail: phased delivery, lifecycle vocabulary, the three §7
boundary notes (developer-workstation · onboarding ladder · offline-render — plus
generate-vs-measure and spec-vs-harness), the full §9 25010 NFR checklist, the §9
perf-comparator guidance, and the rung-2 several-modules-one-repo detail — each
with an **applies-when** line. In PROCESS.md those sections now carry a tight core
statement + `*(opt-in)*` marker + a link into the companion; every **normative
rule and every registry/script contract stayed in the core** (only expanded
rationale/examples moved). Added a **header block**: a "read §1–§7 for the core"
orientation line and a **minimum-profile paragraph** ("a standalone one-module
project needs exactly: …"), resolving the review's "no lite mode" finding.
In-section prose across §1/§3/§4/§7 was squeezed for wording, not rules
(every externally referenced bullet/heading kept). AGENTS.template.md was **not
touched** — Thread 26 already trimmed it to 9,702 bytes; the thread context's
"~11,998" was the pre-Thread-26 figure, and this thread's scope is PROCESS.md.

**Decisions made in-thread:** (1) **companion is scaffolded** (bootstrap MAPPING
`PROCESS_OPTIONS.md → docs/process-options.md`), *not* left unscaffolded like
`EXAMPLE.md`. Reason: the plan links to it with real `[..](..)` markdown links
(so `check_docs` validates the anchors), and a downstream repo that opts into a
layer wants the doc present and clickable; the `EXAMPLE.md` "bare inline-code
reference" convention would have dodged `check_docs` but left dead links. Cost was
one MAPPING entry (the plan sanctioned deciding this in-thread). (2) Anchor slugs
match `check_docs.slugify` (drops `§`, spaces→hyphens): e.g. `#7-boundary-notes`,
`#9-nfr-checklist`, `#10-several-modules-one-repo`.

**Meaning-preservation judgment calls:** §8 (already 11 lines) and the core
testing blocks (dimensional coverage, gates, verdict protocol §5, review triage
§6) were kept **in the core** and only lightly reworded — they are load-bearing,
not optional. The §9 registry column list and the trace/check_perf contract text
stayed verbatim in the core (scripts + EXAMPLE depend on the exact columns/flags).
"Reviewability" three-tier list, the code-map routing options, and runtime-flows
block were reworded but every clause preserved.

**Left open:** **pilot validation on a real repo runs next as its own session.**
Designated pilot repo: **`C:\Projects\FileBackup`** (decided 2026-07-01). This
session did **not** touch FileBackup — it only landed the kit change. The pilot
should scaffold/refresh from the kit and confirm the split reads well and
`check_docs`/`check.py` stay green against a real `docs/process.md` +
`docs/process-options.md`.

**Tests:** `pytest -q` → **129 passed, 1 skipped** (the `sh`-dependent pre-commit
e2e, skipped on Windows). Updated `test_bootstrap.py` to expect
`docs/process-options.md`; `check_docs` reports 0 broken links on a fresh scaffold
(the new anchor links resolve). READMEs (kit contents table) + this repo's
`CLAUDE.md` repo-map updated to name the companion.

---

**Original spec (for reference).** PROCESS.md
was ~50KB across 10 sections; the user judged much of the prose "highly
verbose" and asked to (a) **squeeze the repetition so long as quality doesn't
suffer**, and (b) **split a core minimum profile from an auxiliary doc
outlining what is genuinely optional** — resolving the review's "no lite mode"
finding (today "drop a hat for tiny projects" is the only relief, so every
small adoption re-derives the judgment).

**Goal:** a shorter PROCESS.md every project reads (the load-bearing core:
roles, ids, §3 discipline, gates, verdict protocol, harness contract), plus an
auxiliary reference doc (e.g. `PROCESS_OPTIONS.md`, unscaffolded like
`EXAMPLE.md` — name in-thread) holding the opt-in layers (phased delivery,
lifecycle tags, §8 interfaces, §9 NFR/perf budgets, §10 scale ladder, the §7
boundary notes) each with an "applies-when."

**Steps:** inventory §-by-§ (core vs optional vs restated); squeeze first,
split second; a **minimum-profile table** ("a small project needs exactly:
…") near the top of the core doc. **Constraint:** `§N` cross-references
pervade PROCESS.md, both READMEs, AGENTS/EXAMPLE/MULTI_REPO/ADOPTING, script
docstrings, and tests — either keep section numbering stable or do a full
grep-and-reconcile sweep (the Thread 0a technique). `check_docs.py` +
`pytest -q` are the backstops; scaffolded `docs/process.md` must stay a single
copied file or `bootstrap.py` MAPPING grows a second entry (decide in-thread).

**Risks:** quality loss from over-compression (the user's explicit caveat —
prefer keeping a rule's *why* over hitting a size target); dangling `§N` refs;
downstream churn (pre-adoption, so cheap now — the Thread 7 hinge). **This is
the wide, context-heavy change the sequencing rule says to solo** — do not
fold it into another session.

**Done-when:** core PROCESS.md reads in one sitting; the optional layers live
in the auxiliary doc with applies-when lines; a minimum profile is stated
once; no dangling §-refs (`check_docs` green); `pytest -q` green.

**Model tier — strong model** (editorial judgment over the kit's canonical
doc; the same class as Session I).

## Thread 28 — Agent memory: repo text is the durable layer (boundary note + promote rule)

**Status: ✅ landed 2026-07-01.** All five recommended decisions taken as
specified. PROCESS.md §7's "Two more boundary notes" updated to "Three more
boundary notes" adding the memory-boundary + promote-rule one-liner and a scope
note (decisions 1, 2, 5). PROCESS_OPTIONS.md §7 boundary notes gained the full
expansion ("Repo text is the durable agent memory layer" + promote rule + no
tooling installed). `AGENTS.template.md` gained one working-agreement bullet
(~286 bytes; file now 9,988/10,000 bytes — within budget, size test green).
No-install/no-prompt stance recorded in PROCESS_OPTIONS.md (decision 3). No
deviations. `pytest -q`: **129 passed, 1 skipped** (unchanged).

**Why:** the note asks whether repos that interact with agents need
memory-management tooling deployed at dev-setup, whether the onboarder should
ask about agent use, and whether scope changes the recommendation. The kit has
already answered most of this **structurally, without naming it**: its
committed artifacts *are* the agent-memory layer — `status.md`'s *Current
State* header (cheap context reload, §6), `AGENTS.md` (re-read every session),
the generated code map (don't re-derive the layout), the registries,
`docs/gate`. What's genuinely new is the **adversarial half**: an agent's
*native* memory (auto-memory dirs, MCP memory servers, memory-bank/context
layers) is a **competing home for facts** — load-bearing knowledge hoarded
there is unreviewable, invisible to other agents/humans, and silently erodes
the single-source-of-truth discipline. The fix is a policy, not a tool.

**Recommended decisions (confirm at pickup):**
1. **Name the boundary once in PROCESS.md §7** (the fourth boundary note,
   beside generate-vs-measure / map-vs-index / spec-vs-harness): the committed
   artifacts are the durable, agent-neutral memory layer; **agent-native
   memory tools are an optional per-host category** (name by category with
   `e.g.` — native auto-memory, MCP memory servers; Serena-style indexes and
   `.planning/`-style context layers are *already* named in §3/§7) — never
   installed, required, or configured by the kit.
2. **The promote rule:** agent-native memory is legitimate *scratch*; anything
   durable (a decision, constraint, gotcha) is **promoted** into
   `status.md`/the registries/`AGENTS.md` — the flip side of the *Assumptions*
   log, stated once.
3. **No onboarder/dev-setup prompt or install** — dev-setup provisions the
   *workstation*, not the agent; extends Thread 15's parked
   agent-provisioning stance (record as decided, not just parked).
4. **One `AGENTS.template.md` working-agreement bullet** (~250 bytes: "your
   memory is not the project's memory — record durable facts in `docs/`, not
   agent-private memory") — affordable post-Thread 26 (9,702/10,000 budget);
   the size test is the backstop. This is the one decision with a real cost.
5. **Scope note, one line:** bigger repo ⇒ the committed layer matters more
   (keep *Current State* tight) and a query-time index helps more — both
   already stated; no machinery.

**Tests:** none (prose); `check_docs.py` for links; the AGENTS size-budget
test if decision 4 lands. **Risks:** naming tools dates the doc (category +
`e.g.`, the Thread 8 mitigation); scope creep into an agent-config manager
(out — agent-neutral); don't imply agent memory is *bad* — the rule is only
about where **durable** facts live.

**Done-when:** PROCESS.md names the boundary + promote rule once; the
no-install/no-prompt decision is recorded; AGENTS bullet landed-or-declined
within budget; links + `pytest -q` green.

**Model tier — Sonnet-able end to end** (mirrors the Thread 8/12 boundary-note
pattern; the AGENTS byte-budget is test-enforced now, so no strong-model cap
juggling needed).

---

## Sequencing & session strategy

**Landed:** **0a ✅**, **0b ✅**, **1 ✅**, **2 ✅**, **3 ✅** (2026-06-28),
**7 ✅**, **4 ✅**, **6 ✅**, **8 ✅**, **5 ✅**, **10 ✅**, **9 ✅**, **11 ✅**
(2026-06-29); **12 ✅, 13 ✅, 15A ✅, 17 ✅, 18 ✅** (2026-06-30, Session E);
**14 ✅** (2026-06-30, Session F); **15 B/C/D ✅** (2026-06-30, Session G);
**19 ✅** (2026-06-30, Session H); **20 ✅** (2026-06-30, Session I);
**24 ✅, 25 ✅, 26 ✅, 22 ✅** (2026-07-01, Session J); **27 ✅, 28 ✅**
(2026-07-01, Session K). **All 28 threads complete.**
**Reopened 2026-06-30** with **Threads 12–18**: 12–14 from the
DonnyClaude/Ponytail sibling survey (the same survey→thread move that produced
8/9 from `ai-native-toolkit`); 15 (onboarding/contributor-workspace ladder) +
16 (verifying non-code artifacts, a stub) from the start-from-zero discussion;
17 (voice policy + agent-layer carve-out) + 18 (model/agent-tiering discipline)
from the voice/efficiency discussion; 19 (multi-module scoping) + 20 (multi-repo
coordinator, design-first) + 21 (cross-repo tooling, a stub) from the multi-repo
discussion. **Added 2026-07-01** (next-considerations scratch batch): **Thread 22**
(cost/economic NFRs — a light §9 amendment, queued) + **Thread 23** (documentation /
publication composition, a stub), plus a cross-repo **interface-drift refinement**
folded into Threads 20/21 (design-only, no code). **▶ ALL PLANNED SESSIONS (A–I)
LANDED.** Remaining: **Thread 22** (small, queued — schedule when convenient) and the
**stubs** (16, 21, 23 — each needs a decision to revive). No auto-session; confirm
with the user before starting. The rule applied
throughout: **batch the light, file-coherent threads; keep each new-script build
solo** — re-establishing context per thread is the cost to avoid, and a
from-scratch script + test-suite + debug loop is the context-heavy case the "wide
change" caution (below) is about. **Model-tier rule (new, 2026-06-30):** spec /
decision work stays on the strong model; once a thread is specced, execute it on a
lower tier (Sonnet) with `pytest -q` + the process checks as the backstop — each
thread's **Model tier** line says where the handoff is safe.

> **Session A ✅ landed 2026-06-29 · Process-doc framing (Threads 4, 6, 8).** Pure
> prose. 4→PROCESS G3 (Implementation test-first), 6→PROCESS §4 (Consistency
> review block) + §5 wiring, 8→PROCESS §3 (map-vs-index) + §7 (generate-vs-measure),
> plus README + AGENTS.md clauses for 4/6. The coordinated AGENTS.md pass landed at
> 11,993 chars (under the ~12k Gemini cap) by tightening the new bullets and three
> adjacent lines; Thread 8 stayed out of AGENTS.md to protect that budget.

> **Session B ✅ landed 2026-06-29 · Requirement-capture enrichment (Threads 5,
> 10).** One coherent pass over the SN/SR templates + EXAMPLE + PROCESS: 5 → the
> `Lifecycle` tag in PROCESS §4 (adjacent to delivery `Phase`) + template prompts +
> EXAMPLE §7 phase-spanning table; 10 → PROCESS §9 (NFR checklist + three-homes +
> the `performance-budgets.csv`/`PB-###` registry under a new
> Integration/Coordination hat) + the registry template + `bootstrap.py` wiring + a
> `trace.py` back-link hook + EXAMPLE §8. Both optional `AGENTS.md` clauses were
> skipped to hold the ~12k Gemini cap (single-sourced in PROCESS.md instead). New
> tests: `test_perf_budgets.py` (6) + `test_lifecycle_column_is_schema_safe` + the
> bootstrap file-list assertion. `pytest -q`: 69 passed.

> **Session C ✅ landed 2026-06-29 · Doc navigability check (Thread 9).** Solo
> build — new stdlib `check_docs.py` (broken-link fail / orphan warn / git-gated
> staleness) + a `doc-navigability` process step wired at {G1,G2,G3} + 13 fixture
> tests. It establishes the "add a `check_*` step" pattern Session D reuses;
> `pytest -q`: 82 passed.

> **Session D ✅ landed 2026-06-29 · Perf budget harness (Thread 11).** Solo build,
> the last and highest-noise. New stdlib `check_perf.py` (absolute + regression
> comparator, tier-scoped warn-vs-fail, `--update-baseline`) reusing Session C's
> `check_*`-step pattern; wired as a `perf-budgets` process step at {G3}; PROCESS §9
> comparator subsection + §3 committed-golden class; gitignore/CI/EXAMPLE/README +
> a release-checklist perf section; 15 new tests. `pytest -q`: 97 passed.

> **Session E ✅ landed 2026-06-30 · The prose batch (Threads 12, 13, 15A, 17,
> 18).** **Clubbed 2026-06-30** (was Sessions E + G + I): all five are
> PROCESS.md/README prose. Landed: **12** → PROCESS.md §7 (spec-vs-runtime-harness
> boundary; a turnkey harness named by category as an optional accelerator) +
> README echo; **13** → §3 right-sizing guardrails + the `SHORTCUT:` comment
> convention; **15A** → §7 the three toolchain layers + the `Stage 0 → dev-setup →
> setup → check` onboarding ladder + the offline-render principle + README echo
> (Thread 15's *prose* part only; its script build stays queued for Session G);
> **17** → §5 voice policy (human-vs-machine carve-out + restrained default + tone
> knob); **18** → §6 the task→tier mapping + gates-as-backstop rationale + the
> recorded-tier-hint convention + host-lever examples. **Cap reconciliation
> (the binding constraint, as anticipated): PROCESS-only for all five.**
> `AGENTS.template.md` sat at 11,998/~12,000 chars with effectively zero slack
> and three of the five threads (13/17/18) each wanting a pointer; rather than
> fragile byte-shaving across unrelated bullets for five ~3-4-word pointers, every
> thread's own "else PROCESS-only" fallback was taken, so `AGENTS.template.md` is
> **unchanged** this session (still 11,998 chars — verified, not just assumed).
> No scripts; backstop was `pytest -q` (97 passed, unaffected — prose only) +
> a manual link check (no `#anchor` links were added; all new file links reuse
> already-valid relative paths).

> **Session F ✅ landed 2026-06-30 · Substance gate (Thread 14) — A + C.** Shipped
> the **A** G3 no-stub criterion (PROCESS.md §4 clause + a "No-stub / substance
> review" paragraph, classified Inspection, wired to §6/§3) and **built C**, the
> optional stdlib `scripts/check_stubs.py` AST detector (warn-first; `--strict`
> gates; gitignored `stub-report.md`) with `tests/test_check_stubs.py` (13 cases).
> **Key deviation:** the detector is **not** added to `check.py`'s default plan —
> it ships standalone with a commented wiring example (the perf-*meter* precedent
> the spec named), which keeps it "outside the required process floor" and preserves
> the `test_step_plan_wiring` process⇔stdlib / product⇔tool invariant; see the
> Thread 14 Status block for the full deviation list. `pytest -q`: **110 passed**
> (was 97; +13). No `AGENTS.md` change (the ~12k cap).

> **Session G ✅ landed 2026-06-30 · Onboarder + dev-setup build (Thread 15 Parts
> B/C/D).** Solo, multi-platform build. Shipped the `onboard.template.{sh,command,
> cmd}` guided skeleton (consent banner → native folder picker → ensure-git →
> HTTPS clone → end banner naming the checkout dir + the agent handoff → offers
> `dev-setup --check`), the tiered `dev-setup.template.{sh,ps1}` (`--check` default
> / `--baseline` / `--full`, `--profile code|domain`, EDIT-FOR-YOUR-STACK block),
> bootstrap MAPPING/docstring wiring (+ `.command` exec bit), both READMEs, and the
> meta-repo dogfood (concrete root `dev-setup.{sh,ps1}`). New
> `tests/test_onboard_devsetup.py` (7 cases; `sh` smoke + content assertions).
> Deviation: Part D is a lean concrete dogfood, not a full filled copy of the
> template. **Model tier honored:** built on the strong model; the automated net is
> the shell smoke test only — the cross-platform GUI/auth paths are **manually
> verified per OS**, so a green pytest is not proof those work. `pytest -q`: **116
> passed, 1 skipped**. **Thread 16 is a stub — no session until revived.**

> **Session H ✅ landed 2026-06-30 · Multi-module scoping (Thread 19).** Prose +
> a light EXAMPLE slice + one confirming test; **no script change**. New PROCESS.md
> **§10** (appended after §9, no renumbering): the escalation ladder (single-module
> default → several-modules-one-repo → multi-repo, decide-at-creation/bias-low/
> revisitable, rung 3 pointed forward to Session I in link-safe prose), the
> several-modules-in-one-repo model (sub-trees by the existing `Module`/`Area`
> columns + per-module domain hats), integration TCs for the seams, and `IF-###`
> *within* a repo. **Scoping decision: convention, not a flag** — no `--module`
> filter on `trace.py`/`check.py`; a per-module gate would hide the seams or need
> seam-vs-orphan machinery, and the whole-repo 0-orphan gate already spans them.
> `EXAMPLE.md` §9 shows a two-module `export`↔`delivery` repo (intra-repo
> `IF-001`/`IF-002` + integration `TC-050`); both READMEs got a project-scale note.
> New `test_area_column_is_schema_safe` (mirrors Thread 5's lifecycle test).
> **Note for Session I:** §10 is now taken, so the multi-repo doc is **§11 or
> `MULTI_REPO.md`**. `pytest -q`: **117 passed, 1 skipped** (+1).

> **Session I ✅ landed 2026-06-30 · Multi-repo coordinator design (Thread 20) —
> design-first, the most decision-heavy session.** New **`MULTI_REPO.md`** (a kit
> reference doc, not PROCESS §11 — see the Thread 20 Status block for that
> in-thread call) recording the confirmed model (SR-tier handoff,
> coordinator-as-Integration-hat, catalog-not-copy interfaces, assemblies-as-config,
> mechanical-aggregation gating, async-text coordination, the two requirement scopes
> + the delegated plant repo) led by the rarity/ladder stance. Thinnest schema seams
> shipped: `registries/modules.template.csv` (`MOD-###`) with a `trace.py`
> within-repo `DelegatedSRs` back-link check (the PB precedent; empty allowed for
> external parts), plus the schema-safe `Delegated`/`ParentRef` conventions;
> `EXAMPLE.md` §10 two-repo sketch; `PROCESS.md` §10 / both READMEs / `CLAUDE.md` /
> `KICKOFF_PROMPT.md` (a scale brief question) / `bootstrap.py` docstring (deferred
> `--coordinator` stub). Heavy tooling stays in the **Thread 21 stub**. **Built on
> the strong model** (Opus) throughout the design; `test_modules_registry.py` (7) is
> the seam-wiring backstop. `pytest -q`: **124 passed, 1 skipped** (+7).

**▶ ALL 28 PLANNED THREADS LANDED. Sessions A–K complete.**
Threads 0a, 0b, 1–11 landed (on `template-review-fixes`, since merged into the current
working branch); Session E (12, 13, 15A, 17, 18), Session F (14), Session G (15 Parts
B/C/D), Session H (19), and Session I (20) landed 2026-06-30. **Session J landed
2026-07-01** (from the same-day adversarial review + user decisions): **Threads 24,
25, 26, and 22** — one commit per thread on `MultiRepoSupport`. **Thread 27**
(PROCESS.md squeeze + PROCESS_OPTIONS.md split) and **Thread 28** (agent-memory
boundary note + promote rule) also landed 2026-07-01. **Remaining: stubs 16 / 21 / 23**
(non-code artifact verification · cross-repo tooling · publication composition —
each its own future thread/decision, no session until revived). **Next recommended
step: pilot the kit on one real repo** (smallest first) and feed the friction back
as its own thread — the kit has not yet been used in anger, and one pilot will
teach more than further prose threads.

> **Session J ✅ landed 2026-07-01 · Adversarial-review hardening (Threads 24, 25,
> 26, 22).** Sourced from a same-session adversarial review of the whole kit
> (findings verified empirically on a fresh scaffold, then fixed): the pre-commit
> hook's G1-commit wedge (24.1), day-one-red CI (24.2), the unchecked SR→SN edge
> (24.3), the Windows Store-alias probe (24.4), the missing retrofit path + the
> vacuous non-Python arch-map pass (25), the AGENTS.md zero-headroom cap
> contradiction (26), and the queued cost-NFR amendment (22). `pytest -q` after
> the batch: **129 passed, 1 skipped** (was 124/1; +5 — gate-file resolution,
> SR-no-SN orphan, `--strict-integrity`, AGENTS size budget, zero-source
> arch-map warning; the hook orphan test rewritten to the integrity contract).

> **Session K ✅ landed 2026-07-01 · Agent-memory boundary note (Thread 28).**
> Pure prose. PROCESS.md §7's two-boundary-note paragraph → three notes, adding
> "repo text is the durable agent memory layer" (one-liner + scope note).
> PROCESS_OPTIONS.md §7 gained the full "Repo text is the durable agent memory
> layer" expansion (promote rule + no-tooling-installed stance). `AGENTS.template.md`
> gained one working-agreement bullet ("Repo text is the project's memory; yours
> is scratch" + promote-rule pointer); file now 9,988/10,000 bytes. No deviations.
> `pytest -q`: **129 passed, 1 skipped** (unchanged — prose only).

### Post-plan work items (WI-1.x)

The 28-thread plan is complete; work items below are **new scope** raised after
it, each landed as its own commit(s) on the working branch and recorded here for
continuity (same style as the session log above).

> **WI-1.3 ✅ landed 2026-07-01 · Minimal purchased-parts registry (PART-###).**
> Optional off-spine procurement registry for parts a project *buys* rather than
> builds (each row's `IF-Ref` names its owning interface row, MULTI_REPO.md §3.3);
> `trace.py` integrity-checks the ids, bootstrap scaffolds it inert, prose in
> PROCESS_OPTIONS.md + one PROCESS.md §8 pointer. Deliberately minimal per owner
> decision; full-BOM tracking deferred. (Recorded retroactively for a complete
> WI log.)

> **WI-1.5 ✅ landed 2026-07-01 · Adoption hardening from the FileBackup pilot.**
> Five friction items from the kit's first real re-sync (branch
> `kit-resync-2026-07`, used read-only as the PowerShell-adoption reference).
> Four logical commits:
> 1. **Kit version stamp + .gitattributes + template meta-prose** (friction 1, 4,
>    5a). `bootstrap.py` now writes `docs/kit-version` (kit short-SHA + date) so
>    staleness is detectable and re-sync is a diff, not a guess; it refuses to pin
>    an unreproducible state (dirty kit tree → `<sha>-dirty` + loud WARNING — the
>    pilot's kit HEAD moved twice mid-adoption). Scaffolds a `.gitattributes`
>    pinning `.githooks/pre-commit` to `eol=lf` (a CRLF shebang breaks the sh hook
>    under Windows autocrlf — pilot hit it). Strips the `(template)` title +
>    "Copy this into a new repo" prose from the scaffolded `docs/process.md`.
> 2. **utf-8 console guard + uniform `--root`/`--docs`** (friction 5b, 5c). A
>    `_utf8_console()` reconfigure guard on the six printing scripts turns a
>    cp1252 `UnicodeEncodeError` (the pilot hit it printing `§`) into correct
>    output; trace.py + check_perf.py gain the `--root`/`--docs` pair check_docs
>    already had (one root flag drives all three process checks).
> 3. **PowerShell reference port** (friction 3). Ship
>    `scripts/gen_arch_map.reference.ps1` (generalized from the pilot's working
>    `gen_arch_map.ps1`) filling the same marker blocks from the PowerShell AST,
>    `-Check` freshness + zero-source warning; hook carries the port swap as an
>    EDIT marker; README row. Not bootstrap-scaffolded (a retrofit copies it).
> 4. **ADOPTING.md** (friction 2, + 3's canonical command, + 5's check_flows and
>    gitignored-composite notes). New §6 "Re-syncing an existing adoption":
>    sync-from-committed-state + kit-version diffing, overwrite-vs-preserve, the
>    process.md-split and UN→SN rename migrations (keep id numbers; don't rewrite
>    audit-log evidence quotes; trace.py deliberately does **not** bridge legacy
>    UN-Refs — that's a local patch, not kit scope), and the inverted
>    AGENTS/CLAUDE-convention case (the pilot's layout). §3 names `check.ps1` as
>    the one canonical passing command on a PowerShell repo and adds check_flows
>    retrofit guidance.
>
> **Byte budgets:** `AGENTS.template.md` **untouched** (9,988/10,000 — ~12 B
> headroom; not needed); `PROCESS.md`/`PROCESS_OPTIONS.md` **unchanged** (all new
> prose went to ADOPTING.md + docstrings, per the squeeze constraint). **Deferred
> nothing** of the five; **judged not worth doing:** a `trace.py` UN-Refs
> compatibility shim (the friction log floated it "your call") — a lingering
> `UN-` after a claimed rename is a real orphan worth surfacing, and the migration
> is a one-time find-replace, so a permanent alias would only let the dead prefix
> live forever; recorded as docs-only in ADOPTING.md §6. `pytest -q`: **137
> passed, 1 skipped** (was 134/1; +3 bootstrap tests — kit-version stamp,
> .gitattributes hook pin, process.md meta-prose strip).

> **WI-1.6 ✅ landed 2026-07-01 · Three micro-fixes from the WI-5.2/5.3
> re-syncs (PictureSorter + Pictures2VideoSlideShow).** One commit.
> 1. **ADOPTING.md §6 — `gen_release_checklist.py` function rename.** Added a
>    sub-bullet under the UN→SN recipe noting that overwriting the script also
>    renames its public function `read_user_needs` → `read_stakeholder_needs`;
>    downstream tests importing the old name break (PictureSorter was bitten).
>    Recipe: grep for `read_user_needs` in tests/scripts and update callers.
> 2. **Bootstrap/scripts path robustness (`check.py` + pre-commit hook).** Kit
>    scripts referenced sibling scripts as cwd-relative `"scripts/..."` strings,
>    which break on case-sensitive Linux CI when the repo's existing directory is
>    `"Scripts/"` (NTFS case-preserving; Pictures2VideoSlideShow was bitten).
>    `check.py` now resolves all process-layer scripts via
>    `_SCRIPTS = Path(__file__).resolve().parent` (absolute path, correct
>    regardless of casing). `hooks/pre-commit` computes `SCRIPTS_DIR` at
>    runtime by probing `$REPO_ROOT/scripts` then `$REPO_ROOT/Scripts`
>    (repo root via `$(dirname "$0")/../`). New assertion in
>    `test_step_plan_wiring` verifies every process-step script arg is absolute.
> 3. **ADOPTING.md §6 — legacy TC CSVs missing `Tier` column.** Added a
>    migration recipe: add a `Tier` column with default `Full`; mark
>    hardware/network/interactive cases `Release`. `trace.py --strict-schema`
>    (required at G3) validates the column as non-empty and checks values are in
>    `{Smoke, Full, Release}`. No code change — prose-only recipe.
>
> **Byte deltas:** `ADOPTING.md` +861 B (13812→14673); `AGENTS.template.md`
> **untouched** (9988/10000); `PROCESS.md` **untouched**. `pytest -q`: **137
> passed, 1 skipped** (unchanged — new assertions added inside the existing
> `test_step_plan_wiring` function, not as a separate test).

> **WI-1.7 ✅ landed 2026-07-02 · Proportionality doctrine + human-attestation
> (`Attest`) + binary-asset provenance registry.** Owner-directed
> (2026-07-02), prompted by planning a creative project (video game: story,
> music, artwork, voice acting — mostly binary, mostly subjectively verified).
> Owner's spec: change-trackable assets are an **ideal, not a requirement**;
> where verification can't be mechanized the honest floor is a recorded human
> attestation (trust-based — the box can be checked without the work having
> happened); over-aggressive traceability is itself a failure mode; and for
> creative/subjective domains the SN→SR→LLR→TC spine's value is at **high
> altitude** (ensure nothing key is missed/broken), not fine-grained
> decomposition of subjective work. Three logical commits:
> 1. **Proportionality doctrine.** Tight core statement in `PROCESS.md` next to
>    the minimum-profile paragraph (a/b: ideal-not-requirement; attestation is
>    the honest, trust-based floor) + (c/d) woven into the §3 "Right-sizing"
>    block as one voice (over-aggressive traceability is a failure mode;
>    creative domains fly high, descend to LLR/TC only where a mechanized check
>    earns its keep). Full four-point doctrine in `PROCESS_OPTIONS.md`
>    ("Proportionality doctrine", applies-always).
> 2. **`Attest` verification kind.** Added to the closed `Verification`
>    vocabulary (`trace.py` `ENUM_FIELDS`): a named human's recorded judgment,
>    not a runnable check. LLR-exempt like Analysis/Inspection (subjective/binary
>    asset, no code symbol) but keeps the ≥1-TC rule; the TC records who/when
>    (`Parameters`/`Expected` cell — no schema-breaking new column). `trace.py`
>    accepts an `Attest` SR as legitimately Verified **and** always reports a
>    **"Verification basis (attested vs mechanized)"** count + section so an audit
>    sees the trust footprint. `PROCESS.md` §4 vocabulary expanded; `EXAMPLE.md`
>    §7.1 shows a worked attested row (game main-theme mood-fit). 3 new trace
>    tests.
> 3. **Binary-asset / provenance registry.** New **sibling** registry
>    `registries/assets.template.csv` (`ASSET-###`) — *not* a widened
>    `procurement.csv` (procurement = parts you **buy**, owner-of-record an
>    `IF-###`; assets = created/commissioned digital work with license /
>    provenance / release paperwork — different subject, would force irrelevant
>    columns on both). Columns: license, attribution, provenance
>    (human-made/ai-generated/mixed — real driver: Steam-style AI-content
>    disclosure), contract/release link, + `Location` pointer/`Hash`/`Version`.
>    `trace.py` integrity-checks the `ASSET-` id only (off-spine like PART);
>    bootstrap scaffolds it inert; `PROCESS.md` §8 tight "Binary assets" note +
>    `PROCESS_OPTIONS.md` "Binary assets" expansion (git-LFS/manifest pointer
>    model; the **"asset manifest freshness check"** named as a deferred
>    product-layer idea in the **Thread-16 CAD-stub family**); README row;
>    `ADOPTING.md` §6 migration recipe. 4 new asset tests.
>
> **Tension (doctrine 1 "don't over-constrain" vs. deliverables 2/3 adding
> machinery), and how resolved:** both new mechanisms are **opt-in and honesty-
> increasing, not constraint-increasing.** `Attest` doesn't *demand* more
> decomposition — it gives subjective work an honest home so it **isn't** faked
> into a `Test`, and it is LLR-exempt (fewer required rows, not more). The asset
> registry is off-spine, integrity-only, and inert until used. Neither raises the
> gate bar for a project that doesn't need them; both make the *existing* floor
> more truthful. The doctrine itself is the guardrail that says when to stop
> descending — so 2/3 are the doctrine applied, not a contradiction of it.
> **Byte deltas:** `PROCESS.md` **+3,277** (43,883→47,160 — a genuine new
> verification kind + doctrine, every clause normative); `PROCESS_OPTIONS.md`
> **+7,086** (18,458→25,544, the two expansions, per the squeeze); `ADOPTING.md`
> +1,214; `EXAMPLE.md` +2,432; **`AGENTS.template.md` untouched (9,988/10,000 —
> 12 B headroom preserved).** `pytest -q`: **144 passed, 1 skipped** (was 137/1;
> +3 Attest + 4 asset tests). `check_docs` green on repo + fresh scaffold.

> **WI-1.8 ✅ landed 2026-07-02 · Terminology alignment with systems-engineering
> standards + standards crosswalk.** Owner-approved (2026-07-02): several kit
> concepts are light re-derivations of established standards, so using the
> standard terms buys instant onboarding for humans/tools/LLMs from
> standards-world and lets definition disputes be settled by citation — but as
> **alignment + citation only, never incorporation of standard-mandated
> ceremony** (that process weight is exactly what the Proportionality doctrine
> warns against; IEEE texts are paywalled, so terminology is aligned, never
> copied). Two logical commits:
> 1. **§4 Verification vocabulary → TDIA.** `PROCESS.md` §4 now cites the classic
>    four methods — `Test`/`Demonstration`/`Inspection`/`Analysis` (`TDIA`, per
>    MIL-STD-961E / ISO/IEC/IEEE 29148 / INCOSE SE Handbook) — and leans the
>    definitions on the standard instead of restating them; `Manual` and `Attest`
>    are framed as the kit's explicit named extensions, with `Attest`'s nearest
>    standard analog (a witnessed test / QA sign-off record) noted and the
>    attested-vs-mechanized *reporting* called out as deliberately beyond the
>    standards. **`Demonstration` was already in the closed vocabulary** (added
>    pre-WI-1.8), so this deliverable was terminology/citation, not a new kind:
>    **decided `Demonstration` keeps the LLR requirement** (it runs the system and
>    describes implemented behavior — the standard reading puts it closer to
>    `Test` than to the analytic `Analysis`/`Inspection`/`Attest` trio, which are
>    the only LLR-exempt methods). Purely additive: the closed vocabulary is
>    unchanged → **zero migration burden** for existing adopters. No `trace.py`
>    change needed (vocabulary + exemption logic already correct); no new
>    `EXAMPLE.md` row (SR-002/SR-101/SR-011 already demonstrate `Demonstration`).
> 2. **Standards crosswalk table → `ADOPTING.md` §7.** Chose `ADOPTING.md` over
>    `PROCESS_OPTIONS.md`: the crosswalk's audience is standards-fluent adopters
>    mapping an existing practice onto the kit, which is precisely the retrofit
>    guide's job; a crosswalk isn't an opt-in *process layer*. Compact table
>    mapping SN→SR→LLR→TC (IEEE 29148 StRS/SyRS/SRS + DO-178C HLR/LLR),
>    `trace.py`→RTM, gates→SRR/PDR/CDR/TRR + FCA/PCA (IEEE 15288.2), IF-###→ICD,
>    PB-###→TPMs, ASSET-###→config items/baselines (IEEE 828 / ISO 10007),
>    `status.md` risks→risk register (ISO 31000), Verification→TDIA, and the
>    overall shape→FDA design controls (21 CFR 820.30) / ISO 13485 DHF as a
>    structural cousin. Framed with the doctrine's spirit (right-sized application
>    of the ideas, for communication/citation not obligation). Every mapping
>    **web-verified before writing** (TDIA method set; IEEE 15288.2 review/audit
>    list; IEEE 29148 StRS/SyRS/SRS levels; IEEE 828 / ISO 10007 CI+baseline;
>    ISO 31000 risk register) — **no rows dropped**; the two hedged ones (gates
>    G1–G3 as an *altitude* match not 1:1, and FDA/ISO 13485 as a *structural
>    cousin* not a compliance claim) carry that hedge in their Notes cell.
>
> **Byte deltas:** `PROCESS.md` **+316** (47,160→47,476 — flagged: it grew, but
> the §4 edit was tightened twice so the citation nets only the standard family +
> the Demonstration-LLR call + the Attest analog note; a first pass was +535 B,
> trimmed to +316); `ADOPTING.md` **+3,170** (16,073→19,243, the crosswalk, in the
> adopting layer only per the constraint); `PROCESS_OPTIONS.md` **untouched**;
> `EXAMPLE.md` **untouched** (Demonstration already exemplified); **`AGENTS.template.md`
> untouched (9,988/10,000 — 12 B headroom preserved).** `pytest -q`: **144 passed,
> 1 skipped** (unchanged — no code change, so no new tests). `check_docs` green on
> fresh scaffold (the pytest suite's bootstrap run); the crosswalk uses inline-code
> standard names, not intra-repo links, so adds no link surface.

> **WI-1.9 ✅ landed 2026-07-02 · Repo-setup agent selection + a portable skills
> layer.** Owner-directed (2026-07-02): at repo setup the user most likely has an
> agent configured, so per-repo setup should ask which agent (X / Y / both / none)
> and fetch skills relevant to the project's scope — bringing that agent's LLM
> skills into the repo fold while the template stays reusable.
> **Backlogged stub found + resolved:** the **Thread-15 "Parked follow-on — agent
> selection & auto-provisioning"** (its ✅-revived note now links here), plus the
> scratch open item *"AGENTS.md budget vs. guardrail coverage / what AI skills
> should the template make available"* and the Thread-28-adjacent *"should the
> onboarder ask about agent use"* question (answered: ask at **bootstrap**, not the
> onboarder). The auto-*install* half stays parked; the selection+skills half is
> built. Also grounded in Thread-12's spec-vs-runtime-harness boundary — the kit
> now ships neutral opt-in skills without becoming a turnkey harness. Four logical
> commits:
> 1. **Skills layer source (`project-trajectory/skills/`).** Agent-neutral
>    `<name>/SKILL.md` files whose frontmatter carries BOTH the agent-facing
>    `name`/`description` (the shared **Agent-Skills open standard** both Claude
>    Code and Gemini CLI read — web-verified 2026-07) AND this kit's applicability
>    schema (`stacks`/`domains`/`phases`/`tags` + a `scope` of `kit`|`this-repo`).
>    `scripts/gen_skills_index.py` generates `skills/INDEX.csv` (the cheap scan
>    surface) with `--check` freshness, like `gen_arch_map.py`. `skills/README.md`
>    is the full contract incl. the **future external-source plug-in** (naming,
>    frontmatter shape, neutral landing zone, trust/review).
> 2. **Five skills authored** (bodies grounded in real repo commands, each
>    verified): *kit*-scope (ship + materialize downstream) — `registry-hygiene`
>    (trace/check flags, orphan/schema fixes), `downstream-resync` (ADOPTING §6
>    walk), `gate-advance` (G1→G2→G3 honestly, Attest + attested-vs-mechanized);
>    *this-repo*-scope (maintain THIS template, dogfooded into `.claude/skills/`,
>    NOT shipped) — `byte-budget-guard`, `session-protocol`. Split rationale: the
>    kit ones are generic to any adopted repo; the byte budgets + WI/thread ritual
>    are this template's own attributes.
> 3. **Bootstrap agent selection + matcher.** `bootstrap.py --agents
>    claude|gemini|both|none`; omitted + interactive TTY → **ASK** (agent, then ≤2
>    scope questions: stack? domain? + advisory binary/hardware?); omitted +
>    non-interactive → **`none`**, materializing nothing so the historical scaffold
>    is byte-for-byte unchanged (the CI-safe property, pinned by a test). Selection
>    materializes the matched *kit*-scope skills into the agent's native dir
>    (`.claude/skills/…`, `.gemini/skills/…` — straight copy, same standard) + the
>    agent's hook config copied **inert** as `settings.json.example` (the
>    less-surprising call: never silently install a `Stop` hook; git+CI stay the
>    floor) + a dated setup note in `docs/status.md`. Matcher is a **trivial tag
>    intersection** (`any` always matches) — the metadata convention is the
>    deliverable, not an engine. AGENTS.md stays canonical whichever agent is
>    chosen.
> 4. **Wiring + docs + tests.** README kit-contents rows (`skills/` +
>    `gen_skills_index.py`), `agent-hooks/README.md` (inert-copy behavior),
>    `ADOPTING.md` §6 skills re-sync recipe, `CLAUDE.md` repo-map entry, top-level
>    README quick-start `--agents` example. `conftest.run_py` now closes stdin so
>    the omitted-flag path is deterministically non-interactive in tests.
>
> **agent-hooks decision (wire vs. copy):** *copy inert*, not wire — a scaffold
> that silently runs commands on every agent `Stop` is the surprising outcome; the
> example + one-line note preserves the existing "enforcement lives in git+CI"
> stance while still materializing the file for the chosen agent.
> **Gemini equivalence (researched):** Gemini CLI adopted the **same Agent-Skills
> `SKILL.md` standard** (`.gemini/skills/<name>/SKILL.md` workspace skills), so
> materialization is a straight copy for both — no Claude-only fallback needed; the
> neutral source stays ready for a future third agent.
> **Byte deltas:** **`AGENTS.template.md` untouched (9,988/10,000 — 12 B headroom
> preserved; the skills mention went to PROCESS_OPTIONS + README only, per the
> constraint).** `PROCESS.md` **+129** (47,476→47,605 — flagged: one-line §7
> pointer to the new PROCESS_OPTIONS section, the minimum honest cross-ref);
> `PROCESS_OPTIONS.md` **+2,935** (25,544→28,479, the "Skills layer" section);
> `README.md` (kit) +1,216; `ADOPTING.md` +697; root `README.md`/`CLAUDE.md` small.
> `pytest -q`: **156 passed, 1 skipped** (was 144/1; +8 bootstrap agent/skills
> tests, +4 skills-index tests). `check_docs` green on repo + fresh scaffold; the
> scaffolded process docs reference `skills/README.md` as inline code, not a link,
> so no broken-link surface downstream (skills source isn't scaffolded).

> **WI-1.10 ✅ landed 2026-07-02 · Decision-surfacing dial + in-flight tier
> step-down.** Owner-raised emphasis pair. (1) **Decision-surfacing rate is a
> setup-time, risk-calibrated dial, not a constant**: specialized/high-consequence
> domains (safety even as an *ancillary* risk) surface decisions often for human
> ratification; low-risk creative work lets a confident agent decide autonomously
> *provided every autonomous decision is recorded* (Decisions log/Assumptions).
> Gates and contradiction-findings stay fixed at every setting. Doctrine point
> (e) in PROCESS_OPTIONS.md, operational paragraph in PROCESS.md §6, pointer in
> the PROCESS.md header. (2) **Tiering is an in-flight duty, not just plan-time
> metadata**: step *down* to a cheaper-tier subagent for mechanical well-specced
> subtasks; step *sideways* to a fresh-context peer for bulk content — even
> though hosts increasingly do this automatically. PROCESS.md §6 tiering
> paragraph extended; §1's "spawn a separate agent **only** for review" relaxed
> to name the two delegation cases (it contradicted the duty).
> **Byte deltas:** `AGENTS.template.md` 9,988→9,997 (3 B headroom): the spawn
> bullet now names all three subagent cases and the ask-don't-assume bullet
> gained the decision-dial pointer, paid for by trimming redundancy (gen_cases
> example list, comment/style/intro wording). `PROCESS.md` +1,689
> (47,605→49,294); `PROCESS_OPTIONS.md` +1,252 (28,479→29,731, doctrine (e)).

> **WI-1.11 ✅ landed 2026-07-02 · Commit cadence named as a rule.** Owner-raised
> gap: the kit was saturated with *committed-artifact* language (committed
> goldens/map, reviewed gate commits, a pre-commit floor designed to "never block
> a legitimate early-stage commit") yet never told the working agent to **commit
> often** — and every readable-change property the process buys evaporates for
> work stranded uncommitted. Added: PROCESS.md §3 "Commit cadence" paragraph
> (reviewable change exists only at commit granularity; small single-purpose
> commit per green step, never a session-sized batch; the always-valid floor is
> deliberately cheap *so that* frequent commits stay cheap; a commit is not a
> release — floor-green + coherent change, not perfection; end sessions with a
> clean tree or explicitly parked work) + AGENTS template session bullet gains
> "**Commit early and often** … End sessions with a clean tree."
> **Byte deltas:** `AGENTS.template.md` 9,997→9,990 (headroom *grew* to 10 B;
> paid by trimming: Mermaid "no toolchain" aside, reproducibility tautology,
> harvest-intro wording, "Becomes its summary in the map", "low-risk").
> `PROCESS.md` +1,015 (49,294→50,309).

> **WI-1.12 ✅ landed 2026-07-02 · The evaluator's rungs: README scaffold + run
> launchers.** Owner-raised pair, surfaced by the life-tracker adoption review
> (README existed but pointed at nothing; no way to launch without recalling
> commands). (1) **`README.template.md` → the scaffold's `README.md`**: the
> human front door exists from day one — bootstrap fills `{{PROJECT_NAME}}`
> from the dest folder, never overwrites an existing README (adoption-safe),
> and the kickoff agent builds the rest out from the PROJECT BRIEF
> (KICKOFF_PROMPT.md artifacts list gained the bullet). Skeleton links the run
> launchers, the onboarding ladder, and AGENTS/docs — link-checked by the
> existing scaffold check_docs test. (2) **Root `run.{cmd,sh,command}` product
> launchers**: every launchable project gets a double-clickable start per
> platform — ease of access is a requirement of its own; recall is the enemy
> even when the command is obvious or documented. Ship **inert** (empty
> `RUN_CMD` prints guidance, exits nonzero — the always-scaffolded-inert
> registry stance); `run.command` delegates to `run.sh` so the command lives
> exactly twice (Windows + POSIX), never three times; a pure library deletes
> them. **Root, not scripts/** (deliberate): the double-click use case is
> "open the checkout folder and click" — one hop shallower matters for a
> non-code evaluator. gitattributes template already pins `*.sh`/`*.command`
> LF and `*.cmd` CRLF; bootstrap's existing suffix chmod covers the exec bits.
> Prose: PROCESS.md §7 ladder paragraph gains the evaluator's-rungs sentence;
> PROCESS_OPTIONS.md §7 boundary notes gain the full expansion; ADOPTING.md §1
> gains the README-retrofit bullet; kit README two table rows. Tests: +3
> (name-fill, never-overwrite, inert-launchers) and the expected-files list;
> 159 pass. **Byte deltas:** `AGENTS.template.md` untouched (9,990); PROCESS.md
> +525 (50,309→50,834); PROCESS_OPTIONS.md +1,549 (29,731→31,280).
> *(Also restores the "### Session protocol" heading the WI-1.11 edit
> accidentally consumed.)*

> **WI-1.13 ✅ landed 2026-07-02 · Re-sync must not regenerate a foreign-owned
> arch map.** Friction from the 2026-07-02 downstream re-syncs (FileBackup):
> `initialize_generated_docs` ran unconditionally, so a bootstrap re-run
> against an **adopted** repo executed the freshly-copied Python
> `gen_arch_map.py` over an architecture.md whose generated block is owned by
> a *different* generator (FileBackup's gen_arch_map.ps1 port) — clobbering
> the ps1-generated dependency diagram with empty Python-AST output. Fix: the
> initializer is now gated on **this run having created docs/architecture.md**
> (the fresh-scaffold marker); a re-sync that only adds new registries/
> launchers touches nothing generated. +1 test (sentinel inside the GENERATED
> markers survives a re-run); 160 pass.

> **WI-1.14 ✅ landed 2026-07-02 · Edge-case seeds must cover the whole
> lifecycle.** Friction from Gilbert's G1 (first hardware-domain adoption): the
> stakeholder-needs template's seven seeded edge-case rows were all
> tool-shaped (missing dependency, unwritable output, first-run), and its
> prose asserted one direction of neglect ("most of these rows are
> Provision/Startup — exactly the phases that get neglected"). True for CLIs;
> inverted for embodied/service products — the driver filled the registry with
> toolchain failures while the robot-in-environment edge cases (bystander
> interference, ambiguous irreversible actions, degraded sensors) landed
> off-spine in a side catalog. Fix, two files: (1) the template's edge table
> gains a `Lifecycle` column with seeds per phase, including five generic
> Runtime-environment rows (environment changed mid-operation; third-party
> interference; irreversible action on ambiguous target; degraded-but-present
> input; safe partial abandonment), and the one-directional claim is replaced
> with the symmetric rule (which phase gets neglected depends on the product);
> (2) PROCESS.md §4 G1 now requires edge cases to cover each lifecycle phase
> or record an explicit n/a. **r2 (fresh-context review, same day):** the
> reviewer found three stale restatements of the old bias the r1 sweep
> missed — EXAMPLE.md's "neglected Provision/Startup" pattern line, the
> Minimum-profile "skip Lifecycle tags" clause left unreconciled with the new
> G1 sub-criterion, and KICKOFF_PROMPT.md's edge-case lens (the G1 bullet's
> own checklist) still stating the old bar — plus the unattended-run seed row
> narrowed to Startup only. All four fixed in the r2 commit: symmetric
> wording in EXAMPLE.md, tag-skip ≠ sweep-skip carve-out in the Minimum
> profile, phase-sweep intro + "Live environment" bullet in the kickoff lens,
> Startup→Runtime span on the unattended row. **Deferred, needs owner
> decision:** (a)
> domain-conditional seed rows in `bootstrap.py` (`domain=hardware` swapping
> in physical-world scenarios) — cheap but adds a template-content fork to
> maintain; (b) a mechanized phase-coverage check — the edge table lives in
> free-form Markdown, so parsing it would make a process check depend on prose
> structure; the honest mechanization would move edge cases into a schema'd
> CSV, a larger redesign than this fix warrants.

> **WI-1.15 ✅ landed 2026-07-03 · Registry CSV structural integrity (column
> count vs header) at every gate.** Friction from Gilbert's G2 consistency
> review (second finding from that adoption, after WI-1.14): 19 of 22 rows of
> its `system-requirements.csv` carried unquoted commas (inside `Permutations`
> sets like `set{a,b,c}` and free-text Rationale cells), so a compliant CSV
> parser saw 14–17 columns against a 13-column header — and `trace.py`'s
> DictReader join silently read misaligned cells through G1 *and* G2; the
> defect would only have surfaced at G3 `--strict-schema`. Fix, tests-first:
> 1. **`trace.py` — new `structure_findings()`**, integrity-class (wrong at any
>    stage, like a duplicated id): every data row of every registry CSV must
>    parse (RFC-4180) to exactly the header's column count. Swept **by
>    location, not by a known-file list** — every `*.csv` under
>    `docs/requirements/` + `docs/test/` — so off-spine registries the join
>    never reads (`interfaces.csv`) and project-added ones (Gilbert's CAP) are
>    guarded too; the check needs a file's header, not its semantics. Findings
>    are loud and actionable (docs-relative path + row id + line + parsed vs
>    header column counts + "quote any cell containing a comma") and join the
>    `--strict` / `--strict-integrity` failure sets, so the pre-commit hook now
>    blocks the defect class on every commit with no hook change. Blank rows
>    skipped; `-000` example rows NOT skipped (a template row must parse too);
>    quoted multi-line cells handled (real csv parse, line numbers from
>    `reader.line_num`).
> 2. **`check.py` — new `registry-integrity` process step at {G1}** running
>    `trace.py --strict-integrity`: G2/G3 already fail on integrity via the
>    traceability step's `--strict`, but that step only runs from G2, so the
>    G1 gate previously never executed trace.py at all. Listed before
>    traceability so a `--gate all` run's fuller report.md wins.
> 3. **Prose:** PROCESS.md §7 pre-commit-floor and `trace.py`/gate-wiring
>    bullets updated ("ids + CSV row structure"; "called at every gate");
>    `registry-hygiene` skill (kit source + dogfooded copy) floor comment and
>    integrity bullet updated. Skills INDEX unchanged (body-only edit;
>    `--check` fresh).
> 4. **Tests (7 new, written red-first):** unquoted-comma row fails
>    `--strict-integrity` and `--strict` with file/id/counts in the report;
>    quoted control stays green; short row fails; seeded `interfaces.csv`
>    violation proves the all-registries sweep; unit test for blank-row skip +
>    quoted-newline tolerance; harness wiring (G1 plan carries the step,
>    process-layer, `requires=()`) + end-to-end fresh-scaffold-green /
>    seeded-violation-red at `--gate G1`.
>
> **Downstream note (re-sync):** an adopted repo whose registries carry
> misquoted cells goes red at its next commit/G1 run after overwriting
> `trace.py`/`check.py` — intended (that red is exactly Gilbert's silent
> defect); the fix is quoting the offending cells, no schema change.
> **Byte deltas:** `PROCESS.md` 51,175→51,517 (+342 — the two §7 accuracy
> edits + the every-gate wiring sentence; flagged, no paid trim available
> without losing normative content); `AGENTS.template.md` **untouched
> (9,990/10,000)**. `pytest -q`: **167 passed, 1 skipped** (was 160/1; +7).
> `check_docs --root .`: OK, 0 broken.

> **WI-1.16 ✅ landed 2026-07-03 · Acceptance-criteria testability: comparative
> terms must name their predicate (warn-only lint + §4 reviewer rule).** Third
> finding from Gilbert's adoption: SR-013's AC said a consumer "cannot
> distinguish source by schema" / "schema-identical" — a comparative with no
> named predicate — and it sailed through G1, needing a manual pin at G2.
> Mechanism decision: **both** halves of the proposed fix, split by what each
> does well — a heuristic can *notice* the wording, only a human can *judge*
> it, so the lint **warns and never fails** (the honest-classification stance
> §4's consistency review already takes: never imply `trace.py` performs the
> judgment). Tests-first:
> 1. **`trace.py` — `ac_advisories()`**, always-on and warn-only: a
>    comparative/absolute term in a real SR's `AcceptanceCriteria`
>    (`identical`, `indistinguishable`, `equivalent`, `interchangeable`,
>    `same as`, `matches`, `cannot (be) distinguish(ed)`, `no difference`;
>    word-boundary matched, so "schema-identical" hits and "mismatches"
>    doesn't) with no pinning marker in the cell (`i.e.`/`e.g.`/`defined`/
>    `listed`/`per `/`measured`/`tolerance`/`±`/`golden`/`byte-for-byte`/`==`/
>    `regex`/`checksum`/...) prints `WARNING (advisory): ...` on stdout and
>    fills a new report section "Acceptance-criteria advisories (warn-only)" +
>    an `ac-advisories=N` summary suffix. **Never joins any failure set**
>    (exit 0 under `--strict`/`--strict-integrity`/`--strict-schema`). Via
>    WI-1.15's G1 `registry-integrity` step the warning now *surfaces at G1* —
>    exactly where Gilbert's wording slipped through — while the gate stays
>    green.
> 2. **`PROCESS.md` §4 consistency review** gains the named rule: every
>    comparative/absolute term in an acceptance criterion must say identical
>    *in what*, judged *how*; `trace.py`'s advisory is explicitly a heuristic
>    lint the reviewer resolves (pin the predicate or accept knowingly).
> 3. **`registry-hygiene` skill** (kit source + dogfooded copy): "Reading
>    findings" gains the AC-advisory bullet. Skills INDEX body-only, `--check`
>    fresh.
> 4. **Tests (4 new, red-first, `tests/test_ac_advisory.py`):** unpinned
>    comparative warns loudly but exits 0 under every strict flag; pinned
>    variant ("i.e. same field names and dtypes") not flagged; the minimal
>    project's ordinary AC not flagged; `check.py --gate G1` shows the WARNING
>    while `RESULT: PASS` holds (warn, not fail).
>
> **Deliberately left out:** scanning SN acceptance-intent prose (free-form
> Markdown — same reason WI-1.14 deferred its mechanized phase check) and any
> fail mode for the lint (a wording heuristic must not gate; §4 owns the
> judgment). **Byte deltas:** `PROCESS.md` 51,517→52,064 (+547 — the §4 rule,
> normative; flagged); `AGENTS.template.md` **untouched (9,990/10,000)**.
> `pytest -q`: **171 passed, 1 skipped** (was 167/1; +4). `check_docs --root .`:
> OK, 0 broken.

> **WI-1.17 ✅ landed 2026-07-03 · status.md Open items: scannable bullet
> format, prescribed by the template.** Fourth finding from Gilbert's adoption:
> `STATUS.template.md` seeded *Open items* as a one-line prose field ("the few
> things blocking the current gate, by ID"), and in practice it accreted into a
> comma-spliced wall of text ("(a) … (b) … (h) …") the human reviewer could not
> scan. The reviewer's need, from `status.md` alone: see every open item as a
> bullet, know which need a human decision vs which are in flight, and click
> through to the artifact each concerns. Fix, one file — the **template carries
> the format** (a short seeded example, not just prose guidance), per
> single-source-of-truth:
> 1. **`STATUS.template.md` Current State**: *Open items* now prescribes one
>    bullet per item (**hard rule — never inline-enumerated prose**); stable
>    short ids (OI-1, OI-2, … — never renumbered; closed items removed or
>    struck through) so humans can cite them from memory; a **Needs `<human>`**
>    (decision stated per item) vs **In flight** (driver; no approval needed)
>    split; every bullet ends with a markdown link to the artifact it concerns;
>    the same bullet discipline applies to any deferrals/decisions lists. Two
>    seeded example bullets (OI-1 decision-shaped, OI-2 in-flight-shaped) whose
>    links resolve in a fresh scaffold (`requirements/system-requirements.csv`),
>    so `check_docs` stays green.
> 2. **No other doc changed** — PROCESS.md §6 only says keep the header *short*
>    (compatible; it never described the shape), so there is no second copy of
>    the format to reconcile: the template is the single source of truth.
>
> **Deliberately left out:** a mechanized format check (free-form Markdown —
> same reason WI-1.14/WI-1.16 kept prose out of the failure sets; the G-gate
> reviewer owns the blackboard's readability). **Byte deltas:**
> `STATUS.template.md` 2,082→2,826 (+744 — the seeded example; not a
> budget-watched file); `PROCESS.md` **untouched (52,064)**;
> `AGENTS.template.md` **untouched (9,990/10,000)**. `pytest -q`:
> **171 passed, 1 skipped** (no script change; suite re-run for the
> template's scaffold/bootstrap/check_docs coverage).

### Session protocol (for a cold session pointed only at this file)

0. **If there is no ▶ NEXT session marker, don't invent one — confirm first.** As of
   2026-07-01, all 28 planned threads have landed (sessions A–K). What remains are
   the **stubs** (16 non-code-artifact verification · 21 cross-repo tooling · 23
   publication composition), which each need a human decision to revive. Ask the user
   which to pick up (and confirm the open decisions each lists) before doing anything.
1. Implement the threads in the **▶ NEXT** session — and only those. Each thread's
   own section above is its spec (Goal/Steps/Tests/Risks/Done-when).
2. **End green:** run `python -m pytest -q` and paste the real output (per
   `CLAUDE.md`); never report a green you didn't produce.
3. Add a **`Status: ✅ landed <date>`** block to each finished thread (one-line
   summary + any deviations from its spec), matching the landed threads above.
4. **Update this block:** mark the session done (move it out of NEXT) and move the
   **▶ NEXT** marker to the following session. If a decision a thread left open got
   resolved, record it in that thread.
5. Commit — one commit per session (or per thread); branch is whatever the
   header's **Branch:** line names (keep that line current).

**Why solo the script builds (the "wide change" caution).** Thread 0a alone was a
wide rename; pairing a context-heavy change with everything else risks exhaustion
mid-build. Sessions C and D are each a from-scratch script + test-suite + debug
loop, so they get their own session; the prose/template batches (A, B) are the
opposite — cheap, low-risk, and cheaper done together than re-entered per thread.

**Provenance (why the late threads exist).** Thread 7 was done first among the
late threads (the wide rename is cheapest alone, before B touches the same
registries); its `SN-###` ids are already reflected in every spec above. Threads
8/9 came from a 2026-06-29 survey of the sibling `ai-native-toolkit` (its
`/assess` engine) — 8 names the boundary to that *measurement* half, 9 ports one
stdlib-portable technique (doc-graph) without its `networkx`/`grimp` deps. Threads
10/11 came from the same day's resource-cost discussion. A risk-aware "hotspot"
map was considered and **deferred** (the note just above this Sequencing section).
