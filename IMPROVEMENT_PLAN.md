# Kit Improvement Plan

Derived from `docs/archive/TEMPLATE_REVIEW.md` (resolved 2026-06-28) plus follow-on design
threads and a cross-agent-portability decision; **extended 2026-07-04** with
Threads 29–40 from the downstream-adoption field report
(`docs/archive/kit-adoption-field-report.md`, Finance-Auditor boot), a review of
NotHomeWrecker's unattended coordinator (`trigger.ps1` + `llm-gate-policy.md`),
and owner directives (automation levels; the status.md/history split; the
vision tag; per-repo commit identity + anonymous-repo privacy review; the
LLM iteration-branch sync protocol + tracked iteration logs).
This file is the **spec a
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
(Session G).** Added 2026-06-30 from the scratch.md (now `docs/archive/scratch.md`) "Ensure full provision" notes + the
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

## Thread 29 — Field-report R1: "missing tool ≠ pass" must cover commands, not just Python modules

**Status: ✅ landed 2026-07-04 (Session L).** `run_step()` resolves `cmd[0]`
(`Path.exists()` or `shutil.which`, which honors `PATHEXT`) before executing
and returns the same lenient-aware SKIP/FAIL as the module guard, with the
"command {!r} not found — wire your stack's toolchain (see the EDIT FOR YOUR
STACK block)" detail; the docstring's "Missing tool != pass" bullet now covers
modules **and** commands. Deviation: PROCESS.md §7 needed no edit — it never
names the module mechanism specifically (grep confirmed), so the spec's
conditional clause didn't fire. Tests: `test_missing_command_is_designed_failure`
(FAIL with detail; `--lenient` → SKIP; `sys.executable` steps unaffected).
**Source:** field report A2/R1 (High — "the single highest value-to-effort change").

**Why:** `check.py run_step()` guards a step's `requires` tuple by *Python-module
importability* (`importlib.util.find_spec`). The default plan launches everything
via `sys.executable`, so the guard is complete for the Python reference — but the
documented rewiring path ("swap the format/lint/test commands for your
toolchain") produces steps like `["npx", "vitest", ...]` whose absence the guard
cannot see. A missing Node/other toolchain either crashes with a raw
`FileNotFoundError` traceback or (if someone wraps it) becomes skippable — the
kit's flagship anti-false-green guarantee silently doesn't hold on any non-Python
stack. Finance-Auditor re-implemented the guard downstream; promote it upstream.

**Steps:**
- In `run_step()`, before executing: resolve `cmd[0]`
  (`Path(cmd[0]).exists() or shutil.which(cmd[0])`); on failure return the same
  lenient-aware `SKIP`/`FAIL` as the module guard, with a
  "command {!r} not found — wire your stack's toolchain (see the EDIT FOR YOUR
  STACK block)" detail. Harmless for the reference plan (`sys.executable` always
  resolves); stdlib; cross-platform (`shutil.which` honors `PATHEXT`).
- Update the docstring's "Missing tool != pass" bullet (modules **and**
  commands) and, if PROCESS.md §7 names the module mechanism specifically,
  loosen that one clause to match.

**Tests:** a step whose command names a nonexistent binary FAILs with the
missing-command detail (designed failure, no traceback); `--lenient` → SKIP;
existing suite green (Python steps unaffected).

**Risks:** effectively none — additive guard; the only behavior change is a
confusing crash becoming a designed failure.

**Done-when:** a scaffold whose product step names an absent binary reports
FAIL/SKIP(missing-command); `pytest -q` green.

**Model tier — Sonnet-able** (fully specced; ~6 lines + 2 tests).

---

## Thread 30 — Field-report R2/A3/A4: declare the product toolchain once (stack profile)

**Status: ✅ landed 2026-07-04 (Session N).** New `stack.ini.template` →
`docs/stack.ini` (configparser, `interpolation=None`) with four sections:
`[paths]` src/tests · `[product]` format/lint/test · `[tiers]`
smoke/full/release/all (stack-native selectors appended to the test command —
the A3 gap closed: a non-pytest stack declares its tiers here) · `[coverage]`
threshold + args. Scaffolded unconditionally with the Python-reference values,
so behavior is unchanged out of the box. `check.py` reads it at repo root:
`steps()` gained a `profile=` param; product commands + tier/coverage flow
through one `_expand` path (shlex-split THEN per-token substitute, so a Windows
`{py}` path with spaces survives), and `_requires` derives the needed import
from `{py} -m <mod>` (+ pytest-cov via a `--cov*` flag) so a profile author
declares nothing extra. **Absent/partial profile → the built-in defaults,
verified byte-identical** across every gate×tier (unit + an end-to-end
delete-and-diff `--list`). A **malformed** profile (or non-integer threshold)
exits nonzero naming the file — never silently ignored. `--coverage` wins over
the profile threshold. New `check.py --run-step NAME` runs one step lenient
about a missing tool (SKIP→exit 0) but fails on a real violation (exit 1); the
pre-commit hook's format step now delegates to `--run-step format` when a
profile exists (else the historical staged-`.py` ruff fallback). CI/`setup.*`
EDIT markers now point at `docs/stack.ini` as the one home for check *commands*
(their install commands stay, inherently stack-specific). Non-Python scaffold's
OI-3/OI-6 rewiring checklist repointed at `docs/stack.ini`. PROCESS.md §7 +
ADOPTING §2/§6 + README name it as the single toolchain home; ADOPTING now
lists `check.py` as overwrite-wholesale (customization moved out) and
`docs/stack.ini` as preserve-always.

**Deviations from spec:** (1) mechanism is **`--run-step`** not the spec's
example `--print-step` — check.py runs the format command itself, avoiding
shell-quoting a Windows interpreter path in the POSIX hook. (2) The hook's
profile path runs the profile's **whole-tree** format check (its `{src}/{tests}`
scope) rather than the legacy staged-`.py`-only subset — the single-source
delegation; a format-clean repo is unaffected, and a missing tool still SKIPs so
a not-set-up repo commits. (3) **Per-`--stack` command seeding** (a `node`
scaffold starting with vitest-shaped commands — a Q1 *gain*, not a Done-when)
was **not** built: the profile ships the Python reference and the OI checklist
flags editing it; auto-seeding every stack's commands is deferred as
gold-plating. **Byte deltas:** AGENTS.template.md 9,998 → 9,998 (untouched);
PROCESS.md 54,961 → 55,123 (**+162 B** — the §7 profile pointer, two swaps,
flagged per the budget convention); new `stack.ini.template` 2,504 B (a
scaffolded config file, not a budgeted doc). **Gates:** `pytest -q` **264
passed, 1 skipped** (the same pre-existing skip; +12 new in
`tests/test_stack_profile.py`); `check_docs --root .` **0 broken**.
**Source:** field report R2 (High), A3/A4 (Med).

**Why:** the product toolchain is encoded in ~6 places: `check.py` (step
commands + `SRC`/`TESTS`), `setup.sh`/`setup.ps1` (venv + pip install
ruff/pytest), `ci/check.yml` ("Install tooling"), `hooks/pre-commit`
(ruff-format on staged `.py`), `pytest.ini` (tier markers). A stack swap must
find and rewire all of them, and the copies drift — the exact
single-source-of-truth failure the kit warns downstream about. Test tiering is
additionally pytest-marker-shaped with no declared alternative (A3), so
non-pytest stacks invent one (Finance-Auditor used directory tiers for vitest).

**Design (recommended — confirm Q1):** a small declared profile,
`docs/stack.ini` (`configparser`: stdlib 3.8+, comments allowed — preferred
over JSON for a human-edited file), scaffolded with the Python reference
values so behavior is unchanged out of the box:
`[paths] src/tests` · `[product] format/lint/test commands` ·
`[tiers] smoke/full/release` (stack-native tier expressions — pytest `-m` for
the reference; a directory/pattern for e.g. vitest) · `[coverage] threshold`.
`check.py steps()` reads it when present; **absent → today's built-ins**
(zero migration for existing adopters). The launchers/CI/hook reduce to
pointers: CI's install block and `setup.*` keep their inherently
stack-specific *install* commands but their EDIT markers point at the profile
as the one place check *commands* live; `hooks/pre-commit` sources its format
step from the profile (mechanism decided in-thread — e.g. a
`check.py --print-step format` helper — falling back to the current
ruff-iff-importable when no profile exists).

**Phasing (from the report):** Phase 1 = CI/pre-commit delegate to `check.py`
wherever they duplicate a product command; Phase 2 = the profile file. Phase 1
alone removes most drift risk but keeps ~4 EDIT sites.

**Tests:** profile-present scaffold runs the profile's commands (`--list`
shows them); profile-absent behavior byte-identical to today; a malformed
profile fails loudly (never silently ignored); a non-Python profile naming a
missing binary hits Thread 29's guard (integration); tier expressions thread
through to the test step.

**Risks:** a config surface can rot against the docstrings — make the
scaffolded profile the single documented home and point every EDIT marker at
it; scope creep into a build system — the profile declares *commands*, it
never installs anything.

**Done-when:** exactly one scaffolded file declares the product toolchain;
`check.py --list` reflects it; CI/pre-commit/setup no longer restate a command
they can delegate or reference; `pytest -q` green.

**Model tier — spec/edge-cases on the strong model; build is a solo session**
(new parsing + wiring across 6 files = the "wide change" caution).

---

## Thread 31 — Field-report R3: a non-Python architecture-map path

**Status: ✅ landed 2026-07-04 (Session O).** Built option (b) as ruled: a
stack-neutral `--mode files` in `gen_arch_map.py` (default `symbols` mode
byte-for-byte unchanged). It fills the **same MODULE MAP marker block** with one
row per source file (`_source_files` scans every non-hidden regular file under
`--src`, no extension filter) — the summary is the file's first comment line
(`first_comment_summary`, shebang-skipping, block-close-stripping; comment tokens
from `--comment-prefix`, default `#`/`//`/`--`). `--check` freshness is identical
(string compare), so a file added/removed/renamed or a summary edit trips it;
the zero-scan WARNING is now mode-aware and, in `symbols` mode, points at the new
fallback. **Deviations:** (1) `--flow` + the dependency diagram stay symbol-mode
only (they need a parser) — passing `--flow` with `--mode files` errors rather
than silently no-ops; in files mode the DIAGRAM/FLOW blocks are left untouched.
(2) ADOPTING.md's port-or-drop rule became **port / run the fallback / remove**
(three options, the middle one new) — "never leave a vacuous pass" per the spec.
Gates below.
**Source:** field report A1/R3 (High).

**Why:** the marker-block contract is language-agnostic, but the fillers are
Python-AST + the PowerShell reference port only. A TS/JS/Go repo must
"drop-and-record" the freshness check (ADOPTING.md's port-or-drop rule) —
losing exactly the anti-drift lever the kit prizes. Finance-Auditor dropped it.

**Options:**
- **(a) JS/TS reference port** (`gen_arch_map.reference.mjs`, Node-native,
  heuristic export/import extraction) — the ps1-port precedent; symbol-level
  fidelity; the kit's pytest suite can only smoke-test it where node exists.
- **(b) Stack-neutral fallback mode in `gen_arch_map.py` itself** (stdlib):
  a `--mode files` that fills the marker block from the *source tree* —
  per-file rows (path + first-comment-line summary, comment prefixes
  configurable, e.g. `//`,`#`,`--`) instead of symbol-level rows. Real
  code-derived freshness (file added/removed/renamed or summary drift ⇒ stale
  map ⇒ blocked commit), coarser granularity, works for every stack forever,
  fully testable in the kit's own suite.
- **(c)** both.

**Recommendation: (b) now** — it restores *a* freshness check universally with
zero new runtimes; per-stack symbol-level ports remain contributed references
as adopters materialize them (the ps1 precedent). Confirm whether file-level
granularity is an acceptable fallback bar, or whether (a) should be built now
too (Q3).

**Steps (for b):** the new mode in `gen_arch_map.py` (default mode unchanged);
ADOPTING.md's port-or-explicitly-drop rule gains the third option ("or run the
file-level fallback — never leave a vacuous pass"); hook/`check.py` wiring
unchanged (same script, new flag); zero-source warning still applies.

**Tests:** files-mode fills the block; `--check` goes stale on file
add/remove/rename and summary-line change; Python-AST mode byte-identical to
today; a scaffold wired with `--mode files` passes the arch-map step end to end.

**Risks:** two modes in one script must not blur the contract — the marker
block + `--check` semantics stay identical; only row granularity differs.

**Done-when:** a non-Python repo keeps a real, gate-wired arch-map freshness
check without porting a generator; `pytest -q` green.

**Model tier — solo build session** (new mode + tests), spec already strong.

---

## Thread 32 — Gate authority as declared policy: the three automation levels

**Status: ✅ landed 2026-07-04 (Session M, after Thread 36).** New
`gate-policy.template` → `docs/gate-policy` (one word, tracked like
`docs/gate`, scaffolded `attended`); PROCESS.md §4 is the single canonical
statement (the three Q4-confirmed levels + the four fixed points); new
PROCESS_OPTIONS **"Gate authority levels"** layer carries the full mechanics —
selection-before-port, the deviation-register pattern, the LLM-gate verdict
protocol, Blocked register, Decisions log, LLM-Attest, and the single-ratify
protocol with ratification **fixed at G2 close** (Q5; relocation = amending
the repo's own register) and post-ratification routing **by revert-cost per
the Q6 Hybrid ruling** (LOW → decide+record; MEDIUM/HIGH → Blocked register;
never a mid-run pause). Record homes per Thread 36 (verdicts + ratified
decisions → `docs/log.md`). De-dup sweep landed: AGENTS gates bullet
(byte-funded), KICKOFF 4→1 + the agent-recommendation step + a PROJECT-BRIEF
field, kit README, PROCESS §5/§6, PROCESS_OPTIONS dial prose.
`bootstrap.py --gate-policy` (interactive ASK; non-interactive `attended`);
non-default levels pre-fill the register skeleton (level rows + fixed
points). New `tests/test_gate_policy.py` incl. the R4 tripwire (the authority
claim ≤1 per shipped prose file). Deviations: none. Byte deltas:
AGENTS.template.md 9,990 → 9,998 (gates-bullet edit funded by trims; 2 B
headroom left); PROCESS.md 52,813 → 53,681 (**+868 B**, the §4 canonical
statement — flagged). Gates: `pytest -q` 189 passed, 1 skipped; `check_docs`
0 broken.
**Source:** field report B1/B2/R4 (High) + the owner's automation-levels
directive (2026-07-04) + NotHomeWrecker's ratified `llm-gate-policy.md` as the
proven downstream prototype.

**Why (two halves, one mechanism):**
1. *The report's half:* gate authority is hard-coded prose restated across 5+
   files ("pause for human approval" — AGENTS.template.md:42,
   KICKOFF_PROMPT.md ×3, PROCESS.md §4, PROCESS_OPTIONS.md, README.md, plus
   per-gate Sign-offs lines), and duplicated *within* files. A legitimate
   policy override becomes a scattered `MODIFIED-FROM-KIT` patch whose copies
   get missed — the kit violating its own single-source-of-truth rule.
2. *The owner's half:* the level of human interaction should be **selected
   before the kit is ported** — by the user, with an agent recommendation —
   from three named levels rather than hand-derived per repo.

NotHomeWrecker proved the shape downstream: a repo-local **deviation register**
(`llm-gate-policy.md`) that amends an *untouched* kit-owned process.md —
LLM-gate (fresh-context adversarial reviewer that runs the harness itself and
records a Model:/Role:-stamped verdict), Blocked register instead of mid-run
escalation, Decisions log instead of ask-the-human, LLM-Attest, a model-tier
floor, and fixed points nothing overrides. Upstream that pattern as a
first-class, selectable policy instead of every autonomous repo re-inventing it.

**The three levels** (proposed names — Q4):
- **`attended`** *(default — the current behavior, unchanged):* a human
  approves each gate (G1/G2/G3/G-Release) and G-Final.
- **`single-ratify`** *(new):* the driver advances through G1+G2 with
  LLM-gate-style review, **queuing every human decision** as a
  `Needs <human>` Open-items bullet (the WI-1.17 format) plus provisional
  decisions in a Decisions log; at one **ratification point** the human
  reviews the full list + gate evidence in a single sitting and ratifies (or
  amends); G3→G-Release then run under autonomous rules. **Post-ratification
  questions route by revert-cost (Q6 ruling, 2026-07-04 — Hybrid):** LOW →
  decide + record in the Decisions log; MEDIUM/HIGH → the Blocked register —
  never a mid-run pause either way; the mode's value is momentum, the
  ratifier has accepted bounded risk, and "grind vs pause" is exactly what
  the revert-cost dial encodes. G-Final stays human. **Ratification point:
  fixed at G2 close (Q5 ruling)** — all requirement/design ambiguity is
  resolved exactly once, before the expensive autonomous implementation
  stretch; one prose line notes an adopting repo *may* relocate it by
  modifying its own copy (the deviation-register pattern), but the kit does
  not parameterize it.
- **`autonomous`:** every gate except G-Final closes on an independent
  fresh-context LLM reviewer's recorded verdict (the NHW §2 mechanism:
  reviewer runs `check.py`/`trace.py` itself; verdict recorded per §5 with
  `Model:` + `Role: LLM-GATE`; reviewer tier never delegated down), with the
  Blocked register, Decisions log (+ HIGH-revert-cost second opinions), and
  LLM-Attest.

**Fixed points at every level** (from NHW §8 — these are the floor, confirm
Q4): G-Final is the human's; no un-run greens; the harness is still the bar
(LLM judgment never waives a red check); ratified owner decisions are never
re-decided by an agent.

**Steps:**
- **`docs/gate-policy`** — one word (`attended|single-ratify|autonomous`),
  scaffolded `attended`, tracked like `docs/gate`. New `gate-policy.template`.
- **Define the levels once:** a tight core statement in PROCESS.md §4 (the
  levels + fixed points, a few lines) with the full mechanics in a new
  PROCESS_OPTIONS **"Gate authority levels"** layer (LLM-gate verdict
  protocol, Blocked register, Decisions log, LLM-Attest, the single-ratify
  ratification protocol) — generalized from NHW's register, which becomes the
  layer's worked reference.
- **De-duplication sweep:** every other assertion of gate authority collapses
  to **one reference per file** — "gates advance per the repo's declared gate
  authority (`docs/gate-policy`; default: pause for human approval)". Targets:
  AGENTS.template.md gates bullet (**byte budget: 9,990/10,000 — the edit must
  be paid for by a trim; run byte-budget-guard**), KICKOFF_PROMPT.md (4 hits →
  1 + the recommendation step below), README.md:83, PROCESS_OPTIONS.md:75.
  §4's per-gate *Sign-offs:* lines stay — they define **who signs**, which is
  the single home; the levels redefine who the acceptor is, not the criteria.
- **Tripwire test (kit-side):** a meta-repo test asserting the
  "pause for human approval" phrase (and near-variants) appears at most once
  per shipped file — so a future edit can't quietly re-scatter the claim (the
  mechanically-checkable de-dup R4 asks for).
- **Selection before port:** `bootstrap.py --gate-policy` (flag or
  interactive ASK; non-interactive default `attended`); non-default levels
  also scaffold the deviation-register skeleton (`docs/gate-policy.md`,
  pre-filled for the chosen level with its fixed points). KICKOFF_PROMPT.md
  gains the **agent-recommendation step**: recommend a level from the PROJECT
  BRIEF, risk-calibrated per the §6 decision-surfacing dial (safety / money /
  privacy / irreversibility ⇒ `attended`; low-risk creative/tooling ⇒
  `autonomous` eligible), and record recommendation + owner's choice in
  status.md.
- **Machine surface:** none beyond the file — `check.py`/`trace.py` behavior
  is identical at every level (authority is *who approves*, not what runs).
  The Gate Sign-offs record's acceptor column carries `LLM-GATE` verdicts at
  the autonomous level. **Record home (2026-07-04):** per Thread 36, verdict
  blocks + the ratified Decisions log are appended to `docs/log.md`;
  status.md keeps the Blocked register, pending-ratification items, and the
  pointer — land Thread 36 first (same session).

**Tests:** bootstrap writes `docs/gate-policy` (default `attended`;
`--gate-policy autonomous` scaffolds the register skeleton); the tripwire
grep test; AGENTS size-budget test stays green; `check_docs` green (new links
resolve).

**Risks:** the AGENTS budget (10 B headroom — the trim must fund the edit);
overreach — the kit must *name* the levels, not become an agent-orchestration
framework (execution stays Thread 33's reference layer); wording drift between
PROCESS.md core and the OPTIONS layer — core states, layer expands, nothing
restates.

**Done-when:** gate authority is asserted in exactly one canonical place and
referenced everywhere else (tripwire-enforced); a policy override is a
one-line `docs/gate-policy` change + register skeleton, not a 5-file patch;
bootstrap/kickoff select + recommend the level before work starts;
`pytest -q` green.

**Model tier — strong model, solo session** (editorial judgment across the
canonical docs + the byte-budget squeeze; same class as Threads 26/27).

---

## Thread 33 — Agent-resume entry point + unattended coordinator (protocol · engine · root launchers)

**Status: ✅ landed 2026-07-04 (Session P).** Delivered: (a) the
PROCESS_OPTIONS **"Unattended operation (walk-away runs)"** layer (the
run-state contract with the Q7d `NEEDS-HUMAN` interrupt-and-report;
optional run-phase; commit-every-session / no-elevation /
no-interactive-tools / lean-status.md discipline; end-of-run evidence;
iteration logs + generated index; Thread-40 alignment; the consent framing;
provenance citing `trigger.ps1` as superseded) + a PROCESS.md §4 pointer;
(b) stdlib **`scripts/agent_loop.py`** — fresh headless sessions until
run-state DONE/BLOCKED/NEEDS-HUMAN, git-HEAD stall guard, MaxIterations
ceiling, `docs/run-phase` → `--model-map` tier pick, per-session
`--session-timeout`, guarded rev-parse on zero-commit repos, CLI exit code
captured into the log, limit-aware backoff per (g) with WAITING sessions
never counting toward the stall guard; preflight blocks a violated
`docs/commit-identity` before iteration 1, a missing CLI (report, never a
hang), and a non-git root; (c) root **`agent-resume.{cmd,sh,command}`**
launchers scaffolded like `run.*`, inert until `AGENT_CMD` is filled, with
`--interactive` booting one hands-on session; bootstrap `--agents` seeds
the slots with the chosen agent's example command (permission-bypass flag
included — consent stated in launcher header, loop banner, and READMEs);
(e) tracked `docs/iteration/NNN-<stamp>.log` (cap pinned in-session: head
60 + tail 400 lines, 64 KB ceiling; raw stream additionally to gitignored
`out/run-logs/`) and `docs/iteration_index.md` regenerated from the logs'
metadata headers. Wiring: bootstrap MAPPING + docstring, gitignore entry,
kit README rows, README.template resume note, ADOPTING §6 recipe +
preserve-list rows. Tests: 14 engine tests against a fake `AGENT_CMD` (no
real-CLI dependency) + 4 bootstrap launcher/seeding tests.
**Deviations:** the `AGENT_CMD` EDIT slot lives in the *launchers* (env →
engine), not in the kit-owned engine file, so a later re-sync overwrite can
never clobber a repo's wiring (the RUN_CMD stance applied literally); limit
detection is gated on an error signal (JSON `is_error` / nonzero exit) so a
healthy transcript merely mentioning limits can't read as a throttle; on a
limit hit the default is exit-WAITING naming the reset time
(sleep-until-reset is the opt-in `--wait-on-limit N`) — the spec allowed
either; distinct exit codes per end state (0 DONE · 2 preflight · 3 BLOCKED
· 4 stall · 5 WAITING · 6 budget · 7 NEEDS-HUMAN). Residue for Thread 34's
zero-findings sweep: once a downstream run creates `docs/iteration_index.md`,
`check_docs` will orphan-warn it (nothing links it; a scaffolded link would
be a broken link on a fresh repo).
*(Ruled 2026-07-04: Q7a/b/c confirmed; Q7d amended → the `NEEDS-HUMAN`
run-state, one loop for every policy. Built on Threads 32 + 36 + 40.)*
**Source:** NotHomeWrecker `trigger.cmd`/`trigger.ps1` + kickoff.md
"Unattended mode" (reviewed 2026-07-04) + owner directive (2026-07-04): a
root, double-clickable way to "kick off the correct session at the correct
tier … an easy way to grind through big items from a single point."

**Why:** NHW's coordinator implements walk-away autonomy: loop fresh headless
driver sessions (repo text as the only memory), each resuming from
`status.md`, until `docs/run-state` says DONE/BLOCKED, a stall guard trips
(N consecutive no-commit sessions), or a MaxIterations budget ceiling hits;
`docs/run-phase` maps high-risk phases to a stronger model tier. The
*protocol* is agent-neutral repo text and pairs exactly with Thread 32's
levels. The owner's directive extends WI-1.12's evaluator's-rungs logic
("recall is the enemy") from *running the product* to *resuming the work*:
the repo root offers one entry point that boots the right agent, at the right
tier, in the right mode. **Because the launcher starts in the repo root, the
booted session inherits the whole committed context for free** —
AGENTS.md/CLAUDE.md, `docs/status.md` + `gate` + `gate-policy` + `run-state`,
materialized skills — the Thread-28 repo-text-is-memory property is exactly
what makes a dumb launcher sufficient. (The per-machine half — CLI installed,
authenticated, models available — stays outside the repo; the launcher
preflights and reports it, as NHW's does.)

**Steps:**
- **(a) Protocol → PROCESS_OPTIONS "Unattended operation (walk-away runs)"**
  (applies-when: gate-policy `autonomous`, or `single-ratify` after
  ratification): the `docs/run-state` contract (one word, tracked like
  `docs/gate`: `RUNNING` while work remains; `DONE` only at the policy's end
  state; `BLOCKED` when everything remaining is in the Blocked register;
  **`NEEDS-HUMAN`** (Q7d ruling, 2026-07-04) when the next step requires a
  human act — a gate sign-off under `attended`, the `single-ratify`
  ratification, a decision the §6 dial requires surfaced — written only
  *after* the ask is stated as `Needs <human>` Open-items bullets in
  status.md, so stopping is always interrupt-and-report, never
  infer-and-continue; **a wrong DONE is a false green**); optional
  `docs/run-phase` (the phase the
  *next* session should drive — the coordinator's model-tier key, kept
  current in the finishing commit); commit-every-session (the stall guard
  makes an empty session an abort signal — even a Blocked entry is a commit);
  no-elevation and no-interactive-tools rules; **keep status.md lean across
  iterations** — each session appends its evidence (verdicts, decisions,
  session summary) to the Thread-36 log and leaves status.md holding only the
  resume point + open/blocked items, so the next fresh session's reload stays
  cheap; end-of-run evidence (status.md Current State + Blocked register;
  verdicts + Decisions in `docs/log.md`; clean tree).
- **(b) One coordinator engine, stdlib Python:** `scripts/agent_loop.py` —
  port trigger.ps1's proven loop (fresh sessions until DONE/BLOCKED, git-HEAD
  stall guard, MaxIterations budget ceiling, per-phase model map) onto the
  kit's process-script substrate: **stdlib-only, 3.8+, one implementation for every
  platform** (instead of maintaining ps1+sh twins), and **testable in the
  kit's pytest suite against a fake agent command** (a script that commits /
  writes run-state) — coverage the ps1 original never had. The agent
  invocation is an **`AGENT_CMD` EDIT slot** (the RUN_CMD stance), seeded
  from the bootstrap `--agents` choice (e.g. `claude -p <resume prompt>
  --model <tier>`); a missing CLI → preflight report and nonzero exit, never
  a hang. Preflight also verifies the Thread-38 commit-identity policy before
  iteration 1 — an unattended run is the wrongly-attributed-history disaster
  case. Hardening over the NHW original: capture the CLI exit code into the
  log, guard `rev-parse` on a zero-commit repo, optional per-session timeout
  so a hung session can't wedge the loop.
- **(c) Root launchers — one loop for every policy (Q7d ruling,
  2026-07-04):** `agent-resume.{cmd,sh,command}` scaffolded like `run.*`
  (`.command` delegates to `.sh`; all three are thin wrappers over the
  Python engine). The loop runs under **every** gate policy; what differs is
  where it stops. The driver writes `NEEDS-HUMAN` (see (a)) the moment
  progress requires a human act, and the coordinator exits printing the
  pending asks from status.md Current State in its banner — so an `attended`
  repo's double-click grinds the in-gate work and stops *at* the gate with
  the sign-off request stated, rather than being refused or, worse, inferring
  its way past. An `--interactive` flag boots a single hands-on session
  instead of the loop. Ships **inert** until `AGENT_CMD` is filled (guidance
  + nonzero exit — the WI-1.12 stance); a repo that doesn't want it deletes
  it. This ties the kit to *a* model chain only as a seeded example: the
  slot is stack-agnostic in substance, and unused it costs nothing.
- **(d) Provenance, not a second artifact:** the PROCESS_OPTIONS layer cites
  NHW's `trigger.ps1` as the field-proven origin; the engine supersedes it
  (no separate reference-only ps1 to keep in sync).
- **(e) Iteration logs are tracked, indexed repo artifacts** (owner item 2,
  2026-07-04 — amends the original gitignored-`out/run-logs` stance; Q13d):
  the engine writes each session's log to **`docs/iteration/NNN-<stamp>.log`**
  (size-bounded: head + capped tail of the transcript, cap pinned in-thread;
  the raw unbounded stream may additionally go to gitignored `out/run-logs/`
  for local debugging) and regenerates **`docs/iteration_index.md`** — one
  row per session: number, date, model/tier, phase, outcome, commit range,
  log link. The index is generated-not-hand-maintained (the kit's standing
  rule) and gives the quick pointer; `docs/log.md` (Thread 36) stays the
  *collated* human-review layer above it. On an anonymous repo the logs ride
  the Thread-40 iteration branch and pass its scrub with everything else.
- **(f) Thread-40 alignment (2026-07-04):** the coordinator drives sessions
  on the iteration branch (never the development branch), triggers the sync
  ritual at the end states (full block / gate closure / DONE), and honors
  `docs/push-policy` — under the default it never pushes, even if asked.
- **(g) Limit-aware backoff (verified against Claude Code docs 2026-07-04):**
  plan-usage state (5-hour window / weekly limit / resets) is **not
  scriptable** — `/usage` is interactive-TUI-only, there is no `claude usage`
  subcommand, and headless `/usage` is unconfirmed — so the engine cannot
  preflight remaining budget and must handle the wall reactively. A
  limit-hit `-p` run returns `is_error` with a machine-parseable message
  carrying the reset time ("You've hit your session limit · resets 3:45pm" /
  "…weekly limit · resets Mon 12:00am"): the engine regex-parses it,
  **sleeps until reset (bounded) or exits with a WAITING banner naming the
  resume time**, and — critically — **limit-hit sessions do not count toward
  the stall guard** (the NHW original would misread three throttled sessions
  as a stall and abort). Run sessions with `--output-format json`: per-run
  `usage` tokens + `total_cost_usd` (client-side estimate) feed the (e)
  iteration-index row, and `--max-budget-usd` is the optional per-session
  hard-cap knob beside MaxIterations. Tests: fake agent emitting the
  limit-hit message → engine backs off without incrementing stall, and the
  index row records the WAITING outcome.
- **Consent:** unattended mode passes the agent's permission-bypass flag —
  the loop banner and README say so plainly; the human consents by filling
  `AGENT_CMD` *and* declaring a non-attended gate policy *and* running it.
  git + CI remain the enforcement floor.

**Tests:** engine integration with a fake `AGENT_CMD` — stall guard aborts
after N no-commit sessions; DONE/BLOCKED exits; phase→model mapping picks the
declared tier; logs written; a fake driver that writes `NEEDS-HUMAN` exits
the loop with the status.md ask surfaced in the exit banner (DONE/BLOCKED
exit likewise); `--interactive` launches exactly one session; launchers in
the scaffold file list, inert by default; `check_docs` green; no CI
dependency on any real agent CLI.

**Risks:** shipping a permission-bypass path needs unmissable consent framing
(banner + README + the policy refusal above); model-chain coupling — the
`AGENT_CMD` slot is seeded only when an agent was chosen at bootstrap, so the
kit stays agent-neutral in substance; scope — the engine loops sessions, it
is **not** a scheduler/orchestrator (no queues, no parallel agents).

**Done-when:** a fresh scaffold (agent chosen) can double-click
`agent-resume.*` and get the right session at the right tier under the
declared gate policy; the unattended loop honors run-state / stall / budget
with pytest-proven behavior; the protocol prose stands alone for a downstream
that builds its own coordinator; `pytest -q` + `check_docs` green.

**Model tier — strong model, solo build session** (a new script + test suite
— the "wide change" caution; spec is complete but the loop/timeout/subprocess
edges deserve the tier).

---

## Thread 34 — Conditional scaffold generation (profile-omitted templates, §N-constant) + the mechanical cleanups

**Status: ✅ landed 2026-07-04 (Session S).** Conditional scaffold generation
shipped per the Q8 ruling. Bootstrap now *generates* every Markdown doc from
marker-carrying masters: `<!-- kit-only -->` regions dropped (all copy-me
prose migrated — AGENTS/PROCESS/INTERFACES; `TEMPLATE_REWRITES` kept only for
the "(template)" title), `<!-- profile: axis -->` regions kept or stubbed per
the resolved profile. Axes kept **few and boolean** per the risk line: `nfr`
(§9 + its two process-options expansions) and `multi-module` (§10 + the
rung-2 expansion) — the principle's longer candidate list (interfaces layer,
G-Release, lifecycle prompts, …) deliberately not marked up yet; extension is
monotonic, and interfaces stay always-scaffolded per step 4. § headings sit
*outside* the markers, so an omitted section keeps its literal §N heading plus
a one-line stub (a deliberate strengthening of the spec's single-line stub:
anchors resolve, `check_docs` green on every permutation). `--stack` gained
`node` (bootstrap + skills vocab/frontmatter + regenerated INDEX); an
explicitly non-Python stack skips pytest.ini and appends the OI-3..OI-6
rewiring checklist (WI-1.17 bullet shape) to the fresh status.md — the
tier-mapping bullet does **not** yet name `docs/stack.ini` (Thread 30
pending). `docs/kit-profile` (beside kit-version, rewritten every run)
records `stack=`/`omit=`; a re-sync **regenerates from it** (explicit flags
override) — ADOPTING §1/§6 + the downstream-resync skill carry the
delete-and-rerun recipe and the accepted one-time migration for older
adoptions. Fresh scaffold fully green *including warnings*: README.template
gained the interfaces link **and** a stakeholder-needs link (the second
orphan the zero-findings bar surfaced). Interactive-UX deviation: the stack
question is now asked whenever interactive, agent chosen or not (it drives
the profile, no longer just skill matching). Tests: **21 new** in
`tests/test_profile.py` — marker-grammar unit + per-template lint (balance +
known axes), leftover-phrase grep, the 8-permutation matrix (stable §N
labels, stub counts, zero doc findings, trace green), node gating,
any==default byte-for-byte, resync regeneration, flag-over-record override,
unknown-axis rejection, node skill vocab.
**Source:** the owner's generation question (2026-07-04) + field report
R5/R6/R7/R8, C1/C2/C3, D2.

**The principle — Q8 ruling (owner, 2026-07-04), superseding the original
config-over-generation recommendation: full conditional templating.** The
kit's master templates contain **all permutations**; `bootstrap.py`
generates each repo's artifacts by **omitting** the sections its declared
profile doesn't use. The owner's constraint that makes this sound: **§N
labels stay constant across every variant** — section numbers are literal
text labels in the master, never renumbered by omission, so a finding citing
§7 describes the same relationship in every adopted repo, and new sections
extend the master monotonically. Mechanics that keep it honest:
- **Omission leaves a resolvable stub:** an omitted numbered section renders
  as one line ("§9 Non-functional budgets — omitted by this repo's profile;
  see the kit master"), so cross-references in kept text never dangle and
  `check_docs` stays green on every permutation.
- **The profile is recorded in-repo** (`docs/kit-profile`, beside the
  kit-version stamp): re-sync **regenerates from the recorded profile**
  instead of raw-copying — the downstream-resync skill/ADOPTING §6 path
  changes accordingly. Migration risk for existing adopters (one
  regeneration on their next upgrade) explicitly **accepted by the owner**.
- **Scaffold-stable vs runtime-changeable:** conditional omission applies to
  *structural* choices fixed at adoption (interfaces layer, NFR/perf
  budgets, multi-module ladder, G-Release, lifecycle prompts, stack-specific
  artifacts, unused gate-authority level expansions). State that can change
  mid-project (`docs/gate`, `docs/gate-policy`, `docs/stack.ini`) **remains
  referenced config** — its optional doc *expansions* may still be
  profile-omitted with stubs, and changing such a policy later means
  re-running the generator with the updated profile. (This preserves
  Threads 24/30/32 unchanged.)
- **Per-permutation test matrix:** the kit suite generates every profile and
  asserts `check_docs`/trace/harness green, stable §N labels, and stub lines
  where sections were omitted.
The scaffold-once/downstream-owned distinction survives where it always
applied: AGENTS.md, README.md, status.md, and the registries are generated
once and never overwritten; judgment-bearing content (the PROJECT BRIEF,
requirement rows) stays with the kickoff agent.

**Steps (the generator core + the mechanical cleanups — one marker
machinery):**
1. **Profile markers (the generator's core; `kit-only` is the degenerate
   case):** bootstrap strips regions between
   `<!-- profile: X -->` … `<!-- /profile -->` when the recorded profile
   doesn't select `X` — emitting the §-stub line instead when the region is
   a whole numbered section — and `<!-- kit-only -->` … `<!-- /kit-only -->`
   is simply the profile no repo ever selects (R5/C1). Migrate copy-me prose
   in **every** template into markers (INTERFACES.template.md's "Copy to
   `docs/interfaces.md`" is the confirmed miss; sweep all `*.template.*` +
   PROCESS_OPTIONS). Keep `TEMPLATE_REWRITES` only for in-line rewrites a
   strip can't express (the "(template)" title). A kit-side test greps the
   scaffold for leftover marker text and copy-me phrases.
2. **`--stack` gains `node`** (JS/TS — one label; `js`/`ts` would fragment
   the vocabulary) in bootstrap + the skills-matcher vocab (D2/R6).
3. **Stack-gated artifacts (R7/C3):** when the declared stack is explicitly
   non-Python (`node|go|rust|powershell`), don't copy `pytest.ini`; append the
   **rewiring checklist as `Needs <human>`/`In flight` Open-items bullets in
   the scaffolded status.md** (check.py EDIT block / setup.* / CI install
   step / tier mapping — naming `docs/stack.ini` once Thread 30 lands) so the
   remaining hand-edits are visible work items, not folklore. Blank/`any` →
   today's behavior, byte-for-byte.
4. **Fresh scaffold fully green, warnings included (R8/C2):**
   README.template.md's Development section gains the one-line
   `docs/interfaces.md` link ("only if this repo shares contracts…"), killing
   the orphan-doc warn; add a test asserting `check_docs` on a fresh scaffold
   reports **zero findings of any class**, not just zero failures.

**Tests:** per-step above, plus: `--stack node` scaffold lacks pytest.ini and
carries the checklist bullets; default scaffold unchanged byte-for-byte
(the CI-safe property test extends).

**Risks:** marker-stripping is a transform over every template — keep it
dumb (exact marker lines, no nesting) and tested per template; the
status.md-checklist coupling to WI-1.17's format (reuse its bullet shape
verbatim); under Q8, master readability degrades as markers multiply — keep
the profile axes **few and boolean**, and the permutation matrix is what
holds the line (every profile must scaffold green); the downstream-resync
skill must be updated in the same session (regenerate-from-profile), or
upgrades silently raw-copy the master.

**Done-when:** no scaffolded doc reads as a template; a non-Python `--stack`
choice yields no dead Python artifacts + a visible rewiring checklist; a
fresh scaffold is *fully* green including warnings; **every profile
permutation scaffolds green with stable §N labels and resolvable stubs**;
`docs/kit-profile` records the choice and re-sync regenerates from it;
`pytest -q` green.

**Model tier — strong model, solo build (Session S)** — the Q8 ruling turned
this from a mechanical sweep into the batch's widest build (generator +
resync regeneration + the per-permutation matrix).

---

## Thread 35 — Field-report R9/D1: first-class `Area` column on the SR registry

**Status: ✅ landed 2026-07-04 (Session L).** `Area` appended as the SR
template's last column (guidance cell points at process.md §1 and states the
report-only stance); `trace.py` counts real SRs per non-blank Area and renders
an "SRs by Area (report-only)" section with an untagged count — never a
finding, never an exit-code change; `Area` stays out of `REQUIRED_FIELDS` (the
Thread-5/H schema-safety tests already pin legacy tolerance). EXAMPLE.md §2
header synced (blank cells + a note pointing at §7's filled demo); ADOPTING.md
§6 bullet states adding the column is optional, not a migration. Tests:
shipped-header pin, per-Area report section, section absent for a no-Area
registry.
**Source:** field report D1/R9 (Low).

**Why:** the process assigns SR ownership to domain hats and EXAMPLE.md §7
already demonstrates an ad-hoc `Area` column, but the shipped SR header
doesn't carry it — so each project invents its own 12th column
(Finance-Auditor did) and `trace.py` can't report hat coverage.

**Steps:** append `Area` to `system-requirements.template.csv` (last column —
minimal downstream diff), guidance cell text ("optional owner-hat/domain tag,
blank OK — see process.md §1"); `trace.py` keeps it **out of
`REQUIRED_FIELDS`** (blank cells + legacy CSVs without the column stay green —
the Thread-5/H schema-safety tests already pin this) but, when the column is
present with real values, reports a per-Area SR count section (report-only,
never gating); EXAMPLE.md header-sync check (CLAUDE.md's standing rule);
one-line ADOPTING.md §6 note (adding the column to an existing CSV is
optional, not a migration).

**Tests:** template header carries `Area`; a fresh scaffold passes every gate
untouched; an Area-tagged registry yields the report section; legacy
no-Area CSV still passes `--strict-schema`.

**Risks:** none structural (optional column); mild schema-bloat concern — this
is the report's lowest-priority item, hence Q9.

**Done-when:** a project can record hat ownership without inventing a column,
and trace.py reports it; `pytest -q` green.

**Model tier — Sonnet-able.**

---

## Thread 36 — status.md is the working surface only: history moves to a pointed-to log

**Status: ✅ landed 2026-07-04 (Session M, first).** New `LOG.template.md` →
`docs/log.md` (bootstrap MAPPING + docstring): the Gate Sign-offs table and
Audit log moved with **headings preserved verbatim**, plus a Decisions log
(ratified/executed only — pending stays a status.md Open item);
STATUS.template.md is the pure working surface (Current State / Open items /
Assumptions / Next action / Scope) with the `History: log.md` header pointer
and the optional **`blocks:`** clause seeded in the Open-items example bullet
(WI-1.17 single-source stance). Prose sweep: PROCESS.md §5 states the
now-vs-history rule once (*act from status.md; append evidence to log.md*)
and §6 generalizes the tight-header rule to the whole file; KICKOFF artifacts
list + verdict recording; gate-advance + downstream-resync skills (kit source
+ dogfooded copies); PROCESS_OPTIONS pending-vs-ratified decision homes;
ADOPTING §6 gained the optional, never-forced migration recipe + `docs/log.md`
in the preserve-always list. AGENTS.template.md untouched at this thread
(wording stays true per spec). New test:
`test_status_is_working_surface_history_lives_in_log`; scaffold file list
gains `docs/log.md`. Deviations: none. Byte deltas: PROCESS.md 52,305 →
52,813 (**+508 B**, the §5 rule stated once — flagged); AGENTS.template.md
9,990 → 9,990. Gates: `pytest -q` 184 passed, 1 skipped; `check_docs` 0
broken.
**Source:** owner note (2026-07-04).

**Why:** status.md is currently both the blackboard *and* the archive:
`STATUS.template.md` carries Current State + Open items + Assumptions **and**
the Gate Sign-offs table, KICKOFF_PROMPT.md names status.md the home of the
"append-only audit log", and WI-1.7/NotHomeWrecker additionally write verdict
blocks and Decisions-log entries there. Every session — human or fresh-context
agent — re-reads the file to find *what to do next*, so history accretion
taxes exactly the cheap-context-reload property PROCESS.md §6 prizes (and
Thread 28 named). It bites hardest in Thread 33's unattended loop: dozens of
fresh sessions each reload status.md and append to it, so by iteration 30 the
"resume point" is buried in evidence. Owner's rule: **status.md holds only
what the agent or human must perform next; historical context / report
history lives in a separate append-only doc that status.md points to.**

**The boundary (recommended — confirm Q10):**
- **Stays in status.md (actionable):** the Current State header (gate / phase /
  resume point), Open items (Needs-human + In-flight, WI-1.17 format), the
  Blocked register (Thread 32's levels), assumptions/decisions **awaiting
  ratification**, the exact next action.
- **Moves to `docs/log.md` (append-only history):** the audit log, Gate
  Sign-offs records + LLM-gate verdict blocks, the Decisions log (ratified /
  executed — a decision still awaiting a human is an Open item), session
  summaries / report notes. status.md's header carries the pointer
  ("History: docs/log.md").
- **Third tier (owner item 2, 2026-07-04):** raw per-session detail lives in
  tracked `docs/iteration/` logs with a generated `docs/iteration_index.md`
  (Thread 33e / Q13d). The architecture reads **status.md → log.md → index +
  iteration logs** = *now → curated history → forensic detail*; log.md stays
  compact precisely because the detail has a durable home below it. Citation
  rule (Thread 40): these files cite stable ids (OI-n, gates, dates), never
  iteration-branch SHAs, which scrub/collation may rewrite.

**Steps:**
- Split `STATUS.template.md`; new `LOG.template.md` → bootstrap MAPPING
  `docs/log.md`. The history sections move with their **headings preserved
  verbatim** so downstream greps and the §5 protocol wording survive.
- **Open-items bullets gain an optional `blocks:` clause** (owner note
  2026-07-04): each OI bullet may name what it holds up (`blocks: G2` /
  `blocks: TC-012` / omit when nothing waits on it), complementing the
  already-landed WI-1.17 **Needs `<human>`** vs **In flight** split — so a
  reviewer sees at a glance which open items gate progress and which merely
  accumulate. Seeded in the template's example bullets (the WI-1.17
  single-source stance: the template carries the format; no second copy).
- Prose sweep (single-source): PROCESS.md §5 (verdicts "recorded in
  status.md" → recorded in the log, cited from the status.md gate row) and §6
  (the tight-header rule generalizes: the *whole file* is the working
  surface); KICKOFF_PROMPT.md artifacts list (line 59's "append-only audit
  log" moves to the log doc); the gate-advance + session-protocol skills'
  sign-off wording (kit source + dogfooded copies); `AGENTS.template.md`
  session bullet **only if its wording becomes false** — "update status.md"
  stays true under the split, and headroom is 10 B, so prefer no edit.
- Thread-32/33 alignment: the verdict blocks, Decisions log, and end-of-run
  evidence those threads specify are written to the log; status.md keeps the
  Blocked register and the pointer (their specs updated 2026-07-04).
- ADOPTING.md §6 migration recipe (optional, proportionate — never forced):
  create `docs/log.md`, cut the accreted history sections over, leave the
  pointer; an adopted repo may keep its merged file.
- `check_docs`: log.md is reachable via the status.md link (no orphan warn);
  fresh scaffold stays fully green.

**Tests:** bootstrap file list gains `docs/log.md`; scaffolded status.md
contains no history-section headings (grep); the log template carries the
Sign-offs/audit headings the prose references; scaffold `check_docs` fully
green.

**Risks:** a two-file ritual adds a step to every session — keep the rule
crisp (*act from status.md; append evidence to log.md*); moving the
Sign-offs table breaks downstream muscle memory — headings preserved verbatim
+ the ADOPTING recipe; don't let the log become a second spec home — it is
evidence-only, never normative.

**Done-when:** a fresh scaffold's status.md reads as "what next" only, with
history in a linked append-only log; every kit reference to the old combined
home is reconciled; `pytest -q` + `check_docs` green.

**Model tier — strong model, same session as Thread 32** (same canonical
files; 36 lands first).

---

## Thread 37 — Vision / elevator statement: README-canonical, one searchable tag

**Status: ✅ landed 2026-07-04 (Session L).** README.template.md gained the
canonical `## Vision` section opening with the **`PROJECT-VISION:`** token
(1–3-sentence guidance + the pointer rule); stakeholder-needs.template.md
opens with a real `[PROJECT-VISION](../../README.md#vision)` link carrying the
G1 lens (scope creep / contradiction), mechanically validated by the scaffold's
check_docs run; KICKOFF's README bullet seeds the vision from the brief's
"Goal" line, written before needs are derived, and states the pointer rule
once; PROCESS.md §4 G1 gained the criterion (**+241 B**, flagged below);
EXAMPLE.md shows a worked statement above its SN slice; meta-repo dogfood:
this repo's README.md opens with the token and CLAUDE.md "What we're
optimizing for" points at it. AGENTS.template.md untouched (9,990 B, 10 B
headroom preserved). New test: `test_readme_vision_tag_and_needs_pointer`.
**Source:** owner notes (2026-07-04).

**Why:** nothing in the kit is named Vision. The purpose fact exists as three
unconnected fill-ins — KICKOFF brief "Goal / one-line description",
AGENTS.template.md "What this is / one-line purpose", README.template.md
"*(fill in: one-line purpose…)*" — and the **stakeholder-needs registry, the
top of the spine, has none**: it opens straight into the Core-needs table.
A very short vision at the registry top (a) ties the SN rows together — G1's
consistency review gains a cheap lens: a need serving no part of the vision is
scope creep or a missing vision clause, a need contradicting it is a finding;
(b) fixes the **canonical home** for the purpose fact the other three echo
(today: three homes, no owner — the kit's own single-source smell). Standards
echo: ISO 29148's StRS purpose/scope + ConOps vision — alignment, not ceremony
(the WI-1.8 stance).

**The pattern (owner refinement):** the **README carries the vision** — it is
the first thing a human references — under **one unique, searchable tag**;
every other document *points at the tag* instead of restating it.

**Steps:**
- **`README.template.md` is the canonical home:** its purpose fill-in becomes
  a `## Vision` section whose statement opens with the singleton token
  **`PROJECT-VISION:`** (bold prefix, no number — a grep for `PROJECT-VISION`
  can never confuse it with prose uses of "vision"; the heading doubles as a
  stable `README.md#vision` anchor, which `check_docs` link-validates). 1–3
  sentences max: *for whom · what · the one thing that makes it worth
  building*.
- **`stakeholder-needs.template.md`** gains a one-line top block pointing at
  the tag — "Every need below serves the `[PROJECT-VISION](../../README.md#vision)`"
  (written as a **real markdown link in the scaffolded doc**, so the
  doc-navigability gate mechanically enforces that the pointer never
  dangles). The G1 lens reads through it: needs are checked against the
  vision.
- `KICKOFF_PROMPT.md`: the brief's "Goal / one-line description" **seeds** the
  README Vision section (written first, then needs are derived against it);
  the pointer rule stated once — other docs (the AGENTS "What this is" line
  included) reference the tag, never re-author a variant.
- `PROCESS.md` §4 G1 completeness gains the criterion (the `PROJECT-VISION`
  tag exists in README; the consistency review checks needs against it —
  human-judged, the WI-1.16 honesty stance). Byte cost ~1–2 sentences;
  flagged.
- `EXAMPLE.md`: one worked `PROJECT-VISION:` statement above its SN slice
  (the header-sync rule).
- `AGENTS.template.md`: **untouched** (10 B headroom; its purpose line already
  reads correctly as an echo — the pointer rule lives in KICKOFF).
- **Meta-repo dogfood (owner-confirmed):** this repo's `README.md` opening
  paragraph gains the `PROJECT-VISION:` token, and `CLAUDE.md` "What we're
  optimizing for" points at it — one canonical statement here too.

**Tests:** prose-only — scaffold `check_docs` fully green **including the new
needs→README anchor link** (slug must match `check_docs.slugify`); the
EXAMPLE `Permutations` parse test unaffected.

**Risks:** vision creep into a mission page — the template guidance caps it at
three sentences; the anchor path from `docs/requirements/` is `../../README.md`
— covered by the scaffold link-check test.

**Done-when:** README opens with the tagged vision; the needs registry (and
any other doc that wants it) points at the tag via a link the gate validates;
kickoff seeds it from the brief; G1 names the criterion; EXAMPLE shows a
worked one; the meta-repo dogfoods it; `pytest -q` + `check_docs` green.

**Model tier — Sonnet-able** (prose batch; rides Session L).

---

## Thread 38 — Per-repo commit identity: anonymous vs identified, declared and guarded

**Status: ✅ landed 2026-07-04 (Session L).** New `commit-identity.template` →
`docs/commit-identity` (default `inherit`; explanatory header kept in the
file). `.githooks/pre-commit` gained a **Python-free** identity guard that runs
*before* interpreter discovery (a Python-less machine is still held to the
policy): glob-matches the author email from `git var GIT_AUTHOR_IDENT`, blocks
with the three-way fix message (setup · repo-local git config · inherit);
`inherit`/no-file skips at zero cost. `setup.{sh,ps1}` apply the policy
consent-first: TTY → prompt name/email (suggesting the host noreply form) and
set **repo-local** config, never `--global`; non-interactive → warn only (the
hook is the enforcement). `bootstrap.py` scaffolds the file, adds
`--commit-identity <pattern|inherit>` + an interactive ASK (same consent shape
as `--agents`; CI default `inherit`), and an explicit non-inherit answer
overwrites the scaffolded default at creation. PROCESS_OPTIONS.md "Commit
identity & anonymity" states mechanism + the honest boundary (history /
hosting account / content leaks — no thread ids in shipped prose); ADOPTING.md
§6 migration bullet; kit README row. Thread 33's preflight stays with Session
P as specced. Tests: hook guard end-to-end (sh+git, skip-guarded), scaffold
default, flag override + kept header, repo-local-only static check on both
setup scripts. Deviation: setup's *interactive* config application is covered
by the static + hook tests rather than a TTY-simulation harness (the prompt
path needs a pty; the enforcement path is fully tested).
**Source:** owner question (2026-07-04): "how do we ensure commits follow the
user's preference per repo — anonymous or user-identifiable?"

**Why:** git stamps author/committer from `user.name`/`user.email` — the
machine's **global** config unless the repo overrides it — and nothing in the
kit touches identity: whichever identity the machine happens to carry lands
in the history. The mistake is near-irreversible (fixing attribution after a
push is a history rewrite), and the highest-risk case is the kit's own
direction of travel: an unattended loop (Thread 33) committing dozens of
sessions under the wrong identity before anyone looks. Git's native primitive
is the right one (repo-local `git config user.name/user.email` overrides
global, per clone); the kit's job is to **(1) ask once at repo setup, (2)
record the declared policy in the repo, (3) guard it mechanically** before
each commit and before an unattended run.

**Design:**
- **Policy file `docs/commit-identity`** (one line, tracked, like
  `docs/gate`): `inherit` (default — no constraint, today's behavior) **or an
  email pattern the author identity must match** — e.g.
  `*@users.noreply.github.com` (anonymous) or a pinned address (identified).
  The pattern declares *intent* and is safe to publish in both modes; the
  identity itself stays in git config (per-clone, never committed).
- **`setup.{sh,ps1}` applies it** (consent-first, its existing style): when
  the policy is non-`inherit` and the repo-local identity is
  unset/mismatched, prompt for name/email (suggesting the host's noreply form
  for anonymous) and run repo-local `git config user.name` / `user.email` —
  **never `--global`**.
- **`hooks/pre-commit` guards it:** compare `git var GIT_AUTHOR_IDENT`
  against the policy; a mismatch **blocks** (integrity-class — wrong at any
  stage, expensive after push) with an actionable message (run
  scripts/setup · or `git config user.email …` · or set the policy to
  `inherit`). `inherit` skips the check entirely — zero cost for repos that
  don't care.
- **Thread 33 preflight:** the coordinator refuses to start iteration 1 while
  the policy is violated (cross-ref'd in that spec).
- **`bootstrap.py`:** scaffold the file as `inherit`; optional
  `--commit-identity <pattern|inherit>` flag + interactive ASK alongside
  `--agents` — identity belongs at repo creation, **before the first
  commit**, the only moment it is free to fix.
- **Prose:** PROCESS_OPTIONS opt-in section "Commit identity & anonymity"
  (applies-when: pseudonymous/public repos, privacy constraints): the policy
  file + guard, noreply-email guidance, and the **honest boundary** — the
  guard covers *future commits in clones that ran setup*; it cannot fix
  existing history (rewrite out of scope; ADOPTING.md note), and anonymity
  also depends on the *hosting account* pushing the commits and on keeping
  machine-local paths/usernames out of committed text (Thread 39 mechanizes
  that content half for anonymous repos; the unattended run logs are already
  gitignored). `AGENTS.template.md`
  untouched (budget — enforcement lives below the guide, not restated in it).

**Tests:** hook blocks a mismatched author under a pattern policy and passes
a matching one; `inherit` passes anything; bootstrap writes the file and
honors the flag; setup's config application covered where `sh` is available;
a default scaffold stays green (policy `inherit`).

**Risks:** multi-contributor repos — the policy is deliberately **repo-wide**
(a pseudonymous repo constrains every contributor; per-person freedom =
`inherit`); keep matching dead-simple glob, never touch global config; don't
grow this into a secrets/PII scanner — one advisory line, the guard checks
identity only.

**Done-when:** a repo can declare anonymous-or-identified once at creation;
setup applies it per clone; the hook and the unattended preflight block a
violation before it exists; the limits (history, hosting account, content
leaks) are stated honestly; `pytest -q` green.

**Model tier — Sonnet-able once Q11 rules** (small and well-bounded: hook +
setup + bootstrap + prose + tests).

---

## Thread 39 — Anonymous repos: privacy-leak review before publication (lint floor + subagent reviewer)

**Status: ✅ landed 2026-07-04 (Session Q).** (Ruled 2026-07-04; re-homed
same day by owner ruling — Q12 → Thread 40; fail-closed residue confirmed.)
Deliverables: `scripts/check_privacy.py` (staged-diff default + `--repo`
sweep + a **`--range` history mode — a deviation**, added so the pre-push
floor and the Thread-40 scrub base pass scan diffs *and* commit messages
*and* author lines of a whole range); pre-commit wiring under the policy
gate; a `privacy` [process] step in `check.py` at every gate (the script
self-skips under `inherit`, so it wires unconditionally at zero cost);
`hooks/pre-push` → `.githooks/pre-push` (deterministic lint over the
outgoing range **before** the reviewer — another small deviation, so the
cheap floor never spends the LLM; then the `REVIEW_CMD` slot — env var or
per-clone `git config privacy.reviewcmd`; approval = exit 0 **and** an
APPROVE-without-BLOCK token in the output, so an agent CLI that exits 0
while printing BLOCK still blocks; a missing reviewer **fails closed** per
Q12; verdict-to-`log.md` is the reviewer's briefed duty, stated, not
hook-enforced); PROCESS_OPTIONS "Commit identity & anonymity" grew the
content-privacy layers + process rule + remediation recipe and an honestly
rewritten boundary paragraph; the §8 Binary-assets EXIF advisory; the sync
scrub step now names the lint. In-thread allowlist decision: the inline
`privacy-ok` marker (self-documenting at the site; no config list). Tests:
`tests/test_check_privacy.py` (every class red/green incl. placeholder and
RFC-2606 exemptions, removal-never-flags, fresh-scaffold sweep green under
an anonymous policy) + `tests/test_pre_push_hook.py` (fake
approve/block/sneaky/mute reviewers, git-config slot, add-then-remove
history blocks before the reviewer runs, ref deletion inert). The hook
tolerates a stray CR on its stdin (tr -d). ADOPTING.md's overwrite list
gained the new script + hooks. PROCESS.md and AGENTS.template.md untouched.
**Source:** owner question (2026-07-04): when the repo's state is anonymous,
can a hook (or other method) put a subagent review before every commit,
checking for leakage of personally identifiable or private information?

**Amendment (2026-07-04, owner ruling):** hooks are per-clone and
tool-circumventable, so the LLM review's **primary home moves to Thread 40's
sync ritual** (the scrub step over the iteration branch's history, before
anything reaches the pushable development branch). Unchanged from this spec:
the per-commit deterministic lint (Layer 1) and the `--repo`/gate sweep. The
pre-push hook (Layer 2 below) ships as an **optional backstop** — it still
catches direct-to-dev-branch edits in clones that ran setup, and its
coverage limits are stated rather than pretended away.

**Why:** Thread 38 protects the *author field*; **content** is the bigger
leak surface — absolute paths carrying the OS username, the real identity
from global git config pasted into a doc, an email in a test fixture, a bio
detail in a README, EXIF in a committed asset. A leak becomes harmful at
**publication** (push) and is effectively unrecallable once mirrored/cached,
so the judgment layer belongs at that boundary. Two honesty constraints shape
the design: (1) LLM review is probabilistic — it layers *above* a
deterministic floor and is never sold as a guarantee (the §4
honest-classification stance, same family as LLM-Attest); (2) an LLM call in
every commit would tax the WI-1.11 commit-often cadence into disuse — the
predictable failure mode is people batching commits to dodge the reviewer,
which is *worse* for privacy and for review.

**Design (everything gated on `docs/commit-identity` declaring anonymous —
`inherit` repos pay zero):**
- **Layer 1 — deterministic lint, stdlib, per commit.** New
  `scripts/check_privacy.py` scans the **staged diff** for high-confidence
  classes: home-dir/username path shapes (`C:\Users\<x>`, `/home/<x>`,
  `/Users/<x>`) and the current account/hostname specifically; email
  addresses failing the policy pattern; the real name/email from **global**
  git config appearing in content; private-key headers + a few universal
  token shapes. Wired into `hooks/pre-commit` under the policy gate; blocks
  with file:line findings. Also a `--repo` sweep mode wired as a
  policy-gated process step in `check.py` (catches what slipped in before
  the policy existed or via `--no-verify`) — CI-runnable. Deep secrets
  scanning stays a named external category (e.g. gitleaks, trufflehog) —
  product-layer, never rebuilt in the kit (the Thread-8 stance).
- **Layer 2 — LLM subagent review at the push boundary.** New
  `hooks/pre-push` (bootstrap MAPPING; `core.hooksPath` already covers any
  hook in `.githooks/`): when the policy demands review, invoke a declared
  reviewer slot (**`REVIEW_CMD`**, the Thread-33 `AGENT_CMD` family) over
  the **full outgoing range the pre-push hook receives** — diffs *and*
  commit messages, so a leak added in commit 2 and removed in commit 5
  still gets caught (it ships in history even though the final tree is
  clean). The reviewer is a fresh-context subagent with a tight brief (hunt
  PII / identity / private data; APPROVE/BLOCK + findings); the verdict is
  recorded in `docs/log.md` per §5 extended with `Model:` +
  `Role: PRIVACY-REVIEW` (the Thread-32 convention). Unavailability
  behavior per Q12 (recommend fail-closed).
- **Process rule (agent-driven work):** in an anonymous repo the driver
  routes privacy findings like consistency findings (§5); the Thread-33
  coordinator runs the same review before any push step and refuses on
  BLOCK. `git push --no-verify` remains git's own escape hatch for a human —
  stated honestly rather than pretended away.
- **Remediation recipe** (extends Thread 38's PROCESS_OPTIONS "Commit
  identity & anonymity" section): caught pre-push = rewrite **local**
  history before it publishes (interactive rebase / a filter tool named by
  category); already published = treat as disclosed — rotate/react, a
  rewrite is cosmetic. Binary assets: one advisory line in the §8 assets
  prose — EXIF/author metadata is out of lint scope; strip on ingest.
- **What this is not:** a guarantee or a DLP product. The lint is patterns;
  the reviewer is judgment; both limits are stated where the policy is
  documented (the attested-vs-mechanized spirit — the trust footprint stays
  visible).

**Tests:** lint — each detection class red/green on fixture diffs; policy
`inherit` adds zero hook checks; `--repo` sweep + `check.py` wiring green on
a fresh scaffold, red on a seeded leak. Pre-push — against fake `REVIEW_CMD`
approve/block scripts: BLOCK stops the push path, APPROVE proceeds, missing
reviewer behaves per the Q12 ruling; the outgoing-range assembly covers
commit messages and intermediate commits. No CI dependency on a real agent
CLI.

**Risks:** false positives on legitimate content (documented example paths)
— the lint needs an allowlist affordance (inline `privacy-ok` marker or a
small config list; decide in-thread) or it trains bypass; push
latency/cost — one review per batch, tier per §6 triage; the reviewer itself
sees the private content — it runs under the user's own agent account, the
same trust domain as the driver (no third-party service is introduced);
scope creep — the kit ships the floor and names categories, no more.

**Done-when:** an anonymous repo blocks patterned leaks at every commit and
gets a recorded subagent verdict over the full outgoing history before
anything publishes; `inherit` repos pay nothing; the limits are stated
honestly; `pytest -q` green.

**Model tier — spec/edge decisions on the strong model; build Sonnet-able**
(lint + hook + fake-reviewer tests are well-bounded).

---

## Thread 40 — LLM iteration branch: sync protocol (backup → scrub → collate → land) + push authority

**Status: ✅ landed 2026-07-04 (Session R).** New PROCESS_OPTIONS **"Agent
iteration branch & sync"** layer: the model (agent work on `llm/{branch}`,
the dev branch curated by construction), the five-step sync ritual
(backup → scrub → optional push → collate → land) with the Q12 fail-closed
scrub residue and the Q13a/c rulings stated verbatim (landing ≠ stop; the
type list a default vocabulary, never linted), the three push-policy levels,
the why-structural record, and the two-histories/stable-id rule. New
`push-policy.template` → `docs/push-policy` (scaffolded `human`) + bootstrap
MAPPING/docstring + `--push-policy` flag with interactive ASK
(non-interactive `human`). Pointers: PROCESS.md §3 commit-cadence (collated
categorical commits at sync) + §7 "Push authority" (**+761 B**, flagged);
AGENTS.template.md session bullet gained "Pushing follows
`docs/push-policy` (default: the human publishes)" **funded by two trims**
(the check-launchers parenthetical; the §7 memory-note title quote) —
9,998 B holds. LOG.template.md header carries the SHA-citation rule;
`ci/check.yml` triggers on `llm/**`; ADOPTING.md §6 migration recipe;
gate-advance skill gained the sync-before-bump step (kit source + dogfooded
copy). Pinned in-thread: backup ref = dated tag
`backup/llm-<branch>-<YYYYMMDD>`; the scrub rewrite **does** stamp the
`Scrubbed:` trailer. Threads 33/39 alignment stays spec-side (Sessions P/Q
build against this layer; none of their code exists yet). Tests:
`tests/test_push_policy.py` (5: scaffold default / flag set /
explicit-human / CI trigger / citation rule) + the bootstrap file list.
Deviations: none. Gates: `pytest -q` 194 passed, 1 skipped; `check_docs`
0 broken.
**Source:** owner directive (2026-07-04), refining the Q12 ruling: hooks are
per-clone and tool-circumventable (a user pushing from a different tool may
never hit them), so anonymity — and history quality — should be
**structural**: the agent iterates on its own branch, and what lands on the
development branch is scrubbed and curated *by construction*, not filtered at
push time.

**The model:**
- **The agent never commits to the development branch.** All agent work
  happens on an iteration branch (**`llm/{branch}`** — Q13b ruling; slash
  namespacing groups agent branches in git tooling). The pre-commit floor + Thread-39 privacy lint run there per commit, cheap
  and unchanged; **WI-1.11's commit-often cadence lives on this branch**,
  where granularity is free.
- **Sync points** — a full block (everything remaining Blocked), a gate
  closure, or project-vision completion (the Thread-32 end states). Each sync
  runs five steps:
  1. **Backup:** snapshot the iteration history (dated backup ref/tag) so a
     failed reintegration can never lose work; retired once the sync lands.
  2. **Scrub (anonymous repos only):** a separate fresh-context agent walks
     every commit since divergence — diffs, **commit messages**, and the
     committed iteration logs (Thread 33) — removing/anonymizing PII via
     history rewrite, with the Thread-39 lint as its deterministic base pass
     over each commit. The rewrite can stamp a `Scrubbed:` trailer so later
     checks can tell scrubbed history from raw (pin in-thread).
  3. **Optional push of the iteration branch** — only if the push policy
     allows agent pushes; preserves the granular (scrubbed) history remotely
     for backup/forensics.
  4. **Collate:** a separate agent reorganizes the leg's commits into
     **categorical commits** (Conventional-Commit style with optional scope —
     `feat(addon):` / `fix(biome):` / `perf(noise):` / `docs:` / `build:`,
     the exact shape of the owner's Terra history; Q13c), each a coherent,
     reviewable, why-and-impact-shaped change. Many tiny green commits in;
     few subject-shaped commits out. **The type list is a default
     vocabulary, never a restriction** (Q13c ruling): a project
     renames/extends the types to fit its domain, and nothing lints the
     exact set.
  5. **Land:** the collated commits go onto the development branch. **The
     human pushes at their leisure (default)** — or the agent does, iff the
     push policy says so. **Landing is not a stopping point (Q13a ruling):**
     under an autonomous gate the loop syncs and rolls straight into the
     next leg — unpushed landed legs accumulate, and the human may push
     several at once; the run pauses only on `NEEDS-HUMAN` (Thread 33), i.e.
     when intervention is *required*, never merely because a sync happened.
- **Push authority is a declared policy** (Q13a): new one-liner
  `docs/push-policy` — `human` (default: **the agent never pushes, even if
  asked mid-session**; it prepares the branch and requests) ·
  `agent-iteration` (may push only the scrubbed iteration branch) · `agent`
  (may push the dev branch after a landed sync). Enforced as a process rule
  (AGENTS/PROCESS) and honored by the Thread-33 coordinator; hooks can only
  *assist* (per-clone) — which is exactly why the authority is structural,
  not hook-based.
- **Applies-when:** the branch + sync discipline is a general opt-in layer
  for agent-driven work (curated history is valuable everywhere); the scrub
  step activates only when `docs/commit-identity` declares anonymous.

**Why this beats the push-time filter (recorded):** (1) a structural model
cannot be circumvented by pushing with a different tool — the branch the
user pushes never contained the leak; (2) it solves add-then-strip *by
construction* (raw history never reaches the published branch), where a
diff-of-final-tree check would miss it; (3) it reconciles commit-often with
readable history — the classic feature-branch/curated-integration pattern,
with agents doing the curation.

**Mechanics to pin in-thread:** landing = rebase/cherry-pick of the collated
commits (dev history stays linear; no merge bubbles); after landing, the
iteration branch resets onto the new dev head for the next leg (backup ref
archived or dropped); **SHA citations** — status.md/log.md cite stable ids
(OI-n, gate names, dates), never iteration-branch SHAs, since scrub/collation
rewrites them (one rule line in the Thread-36 templates); optionally add the
iteration-branch pattern to `ci/check.yml` triggers so the floor runs
remotely; a conflict during landing is a **Blocked item**, never a silent
force-through.

**Steps:** PROCESS_OPTIONS layer ("Agent iteration branch & sync": the
five-step ritual + applies-when); one budgeted pointer each in PROCESS.md
§3/§7; `push-policy.template` → `docs/push-policy` + bootstrap MAPPING (+
interactive ASK alongside `--agents`); Thread-33 coordinator alignment
(iterate on the branch, sync at end states, honor the policy); Thread-39
alignment (amended); `AGENTS.template.md` one session-bullet clause **iff**
budget allows, else PROCESS-only (the standing fallback); ADOPTING.md note;
the gate-advance skill gains the sync step.

**Tests:** mechanize the mechanical: push-policy scaffolded + parsed; the
coordinator respects it against a fake agent (T33 suite); docs link-check.
The scrub/collate steps are LLM judgment verified by their recorded §5
verdicts, not pytest — stated honestly.

**Risks:** history rewriting is sharp — confined to the *iteration* branch
before landing, never the dev branch, with the step-1 backup as the net;
ritual weight — this is the heaviest protocol in the kit, so it ships as an
opt-in layer with a clear applies-when; two histories (granular iteration vs
curated dev) can confuse — the iteration index (Thread 33) and log.md state
which is authoritative (dev).

**Model tier — strong model** (protocol design across the canonical docs;
the Thread-32 class).

---

## Thread 41 — Tier-conditional guardrails: the kit ships the hook, content by pointer

**Status: ✅ landed 2026-07-05.** `agent_loop.py` gained `guardrails_apply(policy,
model)` + `guardrails_core(root)` and a per-session `session_prompt()` that
prepends the vendored core to the prompt when `docs/guardrails-policy` selects
the session's resolved model — applied in both the loop and `--interactive`
paths, from the **local** `docs/guardrails/core.md` only (never fetched at
launch), extracting its `BEGIN/END KIT CORE` block (whole file if unmarked).
Policy is one word (absent=`off`): `off`/`all`/a case-insensitive model
substring (name the weaker model to guard only its sessions). Selected-but-absent
core warns once and runs on (accelerator, not a gate); each session log records
`guardrails: on/—`; the coordinator header prints the policy. New
`check_vendored.py` (stdlib, network-gated, warn-first): hash-compares each
vendored file against its pinned raw URL in `docs/guardrails/UPSTREAM`, degrades
to a clean skip offline, `--strict` exits 1; **not** wired into `check.py` (gate
stays hermetic). New PROCESS_OPTIONS "Tier-conditional guardrails" layer (model,
policy, vendoring recipe, the in-session-vs-artifacts boundary). bootstrap
scaffolds `check_vendored.py` (MAPPING + docstring + presence test); kit README
gains its row. Meta-repo dogfoods the mechanism via tests but runs policy `off`
(frontier-tier sessions — nothing to guard), stated in the layer. **Deviations
from spec:** (1) `weak-tiers` as a magic classifier was realized as the more
explicit **model-substring** policy value (the kit can't rank model names, and
this needs no taxonomy that would rot as models ship); (2) drift-check reuses a
generic `check_vendored.py` as the spec anticipated. Tests: +10
(`test_agent_loop.py` +5: policy matrix, off-default, all-injects-block-only,
weak-injects / strong-skips, missing-core warns; `test_check_vendored.py` +5:
match, drift warn + `--strict` fail, offline skip, missing-file warn, no-manifest
noop). `pytest -q`: 316 passed, 1 skipped; `check_docs --root . --stale`: 0
broken. Byte deltas: AGENTS.template.md / PROCESS.md untouched (the layer lives
in PROCESS_OPTIONS + the scripts).

> **Follow-up 2026-07-05 (owner-approved): stale-substring visibility.** Since a
> policy token is a per-repo model substring, a renamed/typo'd token silently
> makes the guard inert. `agent_loop.py` now warns at **startup** when a
> *specific* policy (not off/all) matches none of the run's configured models
> (`--model` + every `--model-map` value) — `guardrails_inert(policy, models)`,
> deterministic and independent of run exit. Tests +3 (helper matrix, warns
> when unmatched, silent when matched); PROCESS_OPTIONS policy bullet notes it.
> `pytest -q`: 319 passed, 1 skipped.

> **Follow-up 2026-07-05 (owner-approved): richer policy grammar.**
> `guardrails-policy` now supports **multiple substrings** (`opus sonnet` — an
> allowlist, guard on any match) and a **denylist** (`all except fable` — guard
> everything but the named frontier model, so a newly added weak tier is
> guarded automatically; the more rot-resistant form). `off`/`all`/single-sub
> unchanged; `guardrails_inert` + the startup warning generalize (an all-except
> covering every configured model is also inert). Tests: matrix + inert +
> all-except integration. `pytest -q`: 321 passed, 1 skipped.

**Rulings:** (a) sync = **vendored
verbatim copy + warn-only drift check** (pinned upstream commit; never
auto-update); (b) scope = **the kit ships only the mechanism** — each repo
vendors the guardrails content itself from upstream (one staleness hop, no
license redistribution).

**Source:** owner (2026-07-05), from the review of the sibling **Guardrails
Kit** repo (`C:\Projects\FableClaudeMDForOpus`, public at
https://github.com/TheColliny/FableClaudeMDForOpus): a CLAUDE.md core
(event-phrased routing table + iron rules + hard stops) plus on-demand
`docs/guardrails/*.md` playbooks that make weaker models operate
procedurally. Owner intent: those procedures can really help **lower-tier
models during their implementation turn**; strong tiers shouldn't pay the
ritual noise.

**Why this shape.** The guardrail docs are *inert unless something routes to
them*, so they can sit permanently on disk for every tier — only the ~45-line
always-on core needs to be tier-conditional, and `agent_loop.py` is the single
point that already knows the launched model (the per-phase model map,
`docs/run-phase`). Injecting at launch means **zero workspace mutation** (no
copy-in/remove churn, no dirty tree, no thrash when PLAN/BUILD alternate
tiers) and no collision with the scaffolded AGENTS.md/CLAUDE.md stubs (the
upstream kit's own install wants to own CLAUDE.md; we deliberately don't use
it — the core is vendored as a standalone file instead).

**The model:**
- **`docs/guardrails/` is a documented optional slot**, filled by the repo
  itself: a vendoring recipe (ADOPTING-style) copies the upstream docs
  verbatim plus the CLAUDE.md KIT-CORE block extracted to a standalone
  `CORE.md`. The kit never redistributes the content (upstream has no
  LICENSE; pointer-not-copy sidesteps it).
- **`docs/guardrails-policy`** — one-word declared-policy file, same
  first-line parse idiom as `gate-policy`/`push-policy`; absent = off (the
  WI-1.30 optional-file precedent, not scaffolded). Values ≈ `off` /
  `weak-tiers` / `all`; the exact weak-tier matching rule against the
  `docs/run-phase` model map is **pinned in-thread at build time**.
- **Injection at launch:** when the policy matches the session's resolved
  model, `agent_loop.py` carries the vendored `CORE.md` into the session
  (`--append-system-prompt` on the Claude CLI; prompt-preamble fallback for
  agents without the flag). Content comes **only from the local vendored
  copy — never fetched at launch** (remote text into agent instructions is a
  supply-chain surface; the pin + reviewed update commit is the control).
- **Drift check, warn-only:** `docs/guardrails/UPSTREAM` records URL +
  pinned commit SHA; a stdlib, network-gated check hash-compares the local
  files against the pinned raw URLs (warns "locally modified") and
  optionally the default branch (warns "upstream moved"), degrading to a
  clean skip offline — the `check_docs --stale` degrade precedent. Updating
  = a human-reviewed wholesale re-copy commit bumping the SHA (upstream's
  own UPGRADE semantics: whole-file swaps, never paraphrase).

**Steps:** PROCESS_OPTIONS layer ("Tier-conditional guardrails",
applies-when: unattended loop + mixed-tier model map) with the vendoring
recipe; `agent_loop.py` injection + policy parse; the drift check (likely a
small generic `check_vendored.py` — pinned-raw-URL hash compare is useful
beyond guardrails; pin in-thread); meta-repo dogfood honestly scoped (this
repo's launchers run the strong tier, so the policy here is `off` — the
mechanism is exercised by tests, not by our own loop).

**Tests:** policy parse (absent/off/match); a fake weak-tier launch carries
the core and a strong-tier launch doesn't (the T33 fake-agent suite);
drift check against a local fixture upstream (file:// or monkeypatched
urlopen — no network in tests); offline degrade; tampered-copy warns.

**Risks:** scope bleed between the guardrails' in-session procedures and
PROCESS.md's artifact/gate rules — one boundary sentence in the options
layer (guardrails govern session mechanics; the process governs artifacts
and gates); CLI flag drift across agent versions — keep the preamble
fallback; ceremony noise if a strong model gets injected — that's what the
policy default `off` and the explicit tier match are for.

**Done-when:** policy declared + parsed; weak-tier launch carries the core,
strong-tier doesn't; drift check warns on local modification and skips
cleanly offline; options layer + recipe documented; `pytest -q` +
`check_docs` green.

**Model tier — strong model** (agent_loop surgery + a new check script; the
Thread-33 class).

---

## Thread 42 — README SN inventory: authored bullets + coverage check (+ `--stale` wired)

**Status: ✅ landed 2026-07-05.** `check_docs.py` gained a fifth finding class
(`check_inventory`): when the root README carries an opt-in
`<!-- sn-inventory -->` section, every cited SN id must exist in
`stakeholder-needs.md` **and** every Must/Should need must be cited by some
bullet — both hard fails; absent section = silent (opt-in by presence).
`_registry_needs` reuses trace.py's whole-file `\bSN-\d+\b` scrape for
existence and reads the Priority column of the core-needs table for the
Must/Should floor (edge-case/Could rows excluded; `-000` ignored). Template:
`README.template.md` ships the markers + a placeholder bullet citing `SN-000`
(inert, copy-ready). `--stale` wired into `check.py`'s doc-navigability step
(warn-only) and this repo's own gate (`status.md` bar + `session-protocol`
skill §3). `gen_release_checklist.py` gained the wording-review hygiene item.
Both READMEs' check_docs descriptions updated. **Deviation from spec:** the
Must/Should floor is priority-column-parsed (the spec floated a "light ID-column
scan"); the fuller parse is what the coverage direction actually needs and it
mirrors `gen_release_checklist.read_stakeholder_needs`. The `make_minimal_project`
fixture now cites its real `SN-001` (a fully-traced project covers its needs in
the README too) — the drift the gate is meant to catch. Tests: +6
(`test_check_docs.py`: clean scaffold, uncovered-Must fails, bad-citation fails,
absent-section opt-in, `_registry_needs` priority parse, harness `--stale`
wiring). `pytest -q`: 302 passed, 1 skipped; `check_docs --root . --stale`: 0
broken. Byte deltas: AGENTS.template.md / PROCESS.md untouched.

> **Follow-up 2026-07-05 (owner-approved): staleness → `hint` severity.** The
> `--stale` heuristic is a low-confidence nudge, but it shared the `WARN` tag
> with orphan docs (a real structural finding), over-weighting it — and on a
> README that deep-links churning scripts it false-positives constantly (the
> SN inventory above is the content-aware freshness net now). `check_docs.py`
> now prints staleness as a distinct lowercase **`hint`** (below `WARN`, never
> counted toward exit status); kept firing for doc→source maps that have no
> content check. `--stale` stays wired into the harness + this repo's gate
> (it's global, not README-only; the hint downgrade de-alarms it). Test:
> `test_staleness_prints_hint_not_warn` (git-scenario, first integration test
> of a real stale hit). `pytest -q`: 321 passed, 1 skipped.

**Source:** owner field reports (2026-07-05): downstream READMEs go stale.
Ruling: the **authored-bullets variant** (human-voiced terse bullets citing SN
ids, mechanically coverage-checked), not the generated-registry-dump variant.
The `--stale` wiring below was approved outright.

**Source:** owner field reports (2026-07-05): downstream READMEs go stale
because nothing *pulls* on them when requirements move. Extends Thread 37 /
WI-1.31 (the vision tag made canonical, then mechanically guarded) to the
rest of the README's claims.

**The model:** a marked README section — `<!-- sn-inventory -->` …
`<!-- /sn-inventory -->` — of short hand-written bullets, each citing the SN
ids it summarizes (many-to-one by design):

    - **Clean imports** — bank CSVs load without hand-fixing,
      duplicates flagged (SN-001, SN-002)

Detail (priority, acceptance, edge cases) stays single-homed in the
registry; the README holds a clause + ids. The check enforces both
directions: **every cited id exists** (fail), and **every Must/Should SN is
cited by some bullet** (fail) — so adding SN-011 without touching the README
fails the gate, and deleting an SN a bullet cites fails too. Structural rot
becomes impossible; **wording rot is honestly out of scope** (a bullet's
prose can lag an SN's acceptance change) and is mopped up by `--stale`, the
release-checklist attestation, and keeping bullets terse.

**Mechanics:**
- Check lives beside the WI-1.31 vision check (`check_docs.py` owns the
  README surface); it reads SN ids with a light scan of the
  `stakeholder-needs.md` ID column — registry *semantics* stay `trace.py`'s
  job. Section absent → check silent (**opt-in by presence**).
- `README.template.md` ships the markers with one placeholder bullet citing
  `SN-000` — the `-000` placeholder convention keeps a fresh scaffold green
  and copy-ready; the checker ignores `-000` like `trace.py` does.
- Priority floor: Must + Should required, Could/Won't optional; the floor is
  fixed for now (a knob is deferred until someone needs it).
- **`--stale` wiring:** `check.py`'s doc-navigability step gains `--stale`
  (warn-only, so the floor stays green), and this repo's own session-gate
  command (session-protocol skill §3 + the protocol section here) gains it
  too.
- `gen_release_checklist.py` gains the attested item "README reviewed
  against the current SN registry".
- Meta-repo dogfood: **n/a and stated** — this repo has no SN registry (the
  spine is deliberately not self-applied, status.md Non-goals); scaffold
  tests carry the coverage.

**Tests:** fresh scaffold green (placeholder bullet); cited-missing fails;
uncovered Must fails; Could not required; section-absent silent; `-000`
ignored; check.py passes `--stale` (step-args assertion); checklist line
present.

**Risks:** README-churn friction on every SN add — intended (that *is* the
pull), and the fix is a one-line id append; loose table parsing — malformed
registries are `trace.py --strict`'s finding, this check degrades
gracefully; byte creep — PROCESS.md untouched (the convention lives in the
template comments + this spec; flag if a pointer sentence proves necessary).

**Done-when:** both check directions enforced on scaffolds; template
copy-ready; `--stale` wired in the harness and this repo's gate command;
checklist item ships; `pytest -q` + `check_docs` green.

**Model tier — strong model for the check + tests; the template/checklist
prose is Sonnet-able.**

---

## Thread 43 — dev-setup role profiles: default installs everything, a named role narrows to its slice

**Status: ✅ landed 2026-07-05.** Both `dev-setup.template.{sh,ps1}`
generalized from the single `DOMAIN_VIEWER_*` slot to N declared roles over the
unchanged shared baseline (runtime, git, offline renderer). Default (no
`--profile`) reports/installs **every** declared role; `--profile <role>`
narrows to baseline + that role; an unknown role exits 2 naming the declared
roles. Ships `code` (empty install — the toolchain is setup.*'s job) + `design`
(example asset-viewer role) so a fresh scaffold's `--check` is green and
copy-ready. sh uses `eval`-indirection on `<role>_CMDS/_INSTALL`; ps1 uses an
`[ordered]` role hashtable (cleaner where the language has one). Verified both
shells: default lists code+design, `--profile design` drops code, bad role
exits 2 (sh `sh -n` + runs; ps1 `Parser::ParseFile` + `pwsh -File` runs — fixed
a latent `$label:` scope-parse bug and made the ps1 error exit 2, not
Write-Error's 1). READMEs (kit + root) + ADOPTING migration note updated.
**Deviations from spec:** (1) the optional interactive TTY role-selector was
**not** built — default=all already covers the common case and it kept the
dual-shell surface small (noted, not in Done-when); (2) the meta-repo dogfood
`scripts/dev-setup.*` stays single-stack per spec (untouched). Tests: +3
(`test_onboard_devsetup.py`: default reports every role, `--profile` narrows,
unknown-profile exit 2) + the existing token test updated `domain`→`design`.
`pytest -q`: 305 passed, 1 skipped; `check_docs --root . --stale`: 0 broken.
Byte deltas: AGENTS.template.md / PROCESS.md untouched.

**Source / spec (owner direction this session).** Ruling: **the default installs
every role's packages**
(the common case — a fresh clone or solo dev wants the lot); a **named role
installs only that role's relevant packages** (the opt-down). Heavy per-repo
customization is expected; the template ships the *structure* so every repo
declares roles the same way.

**Source:** owner (2026-07-05), from downstream field reports: repos with
multiple contributor kinds (UX asset designer, physical-part/CAD, marketer,
code) outgrow one generic `--profile code|domain` split.

**Why.** Today the tiered `dev-setup.template.{sh,ps1}` has exactly two
profiles — `code` (default) and `domain` — over a runtime + git +
offline-renderer baseline everyone shares, with a **single** role-specific
install slot (`DOMAIN_VIEWER_CMDS` / `DOMAIN_VIEWER_INSTALL`). That collapses
every non-code contributor into one "domain" bucket a UX/CAD/marketing mix
outgrows. Generalizing that one slot to **N declared roles, default = union**
keeps every current property (consent-first, detect-first, headless-safe) and
gives multi-contributor repos a consistent, greppable role vocabulary — the
consistency the owner is after even though the fills are per-repo.

**The model:**
- **Universal baseline stays unconditional** — runtime, git, the offline
  Mermaid renderer are detected/installed for every profile (workstation
  table stakes, not a role's concern; unchanged from today).
- **Roles are additive on top of the baseline** — the template declares a
  role list and, per role, a detection-commands list + an install command:
  exactly today's `DOMAIN_VIEWER_CMDS`/`DOMAIN_VIEWER_INSTALL` shape, lifted
  from one hardcoded slot to N.
- **Default (no `--profile`) = every role.** `--check` reports on all;
  `--baseline`/`--full` install the baseline plus **every** declared role's
  packages (consent-first, one prompt per install, as today).
- **`--profile <role>` = baseline + that role only** — the opt-down. An
  unknown role name errors with the declared list (never silently installs
  nothing).
- **Ships `code` pre-filled + one placeholder role** (e.g. `design`,
  commented and inert like the `-000` registry rows) so a fresh scaffold's
  `--check` runs green and the fill structure is obvious.
- **Optional TTY sugar:** when interactive with no `--profile`, offer the
  role list (Enter = all); silently defaults to all when headless/CI (the
  existing `interactive()` guard) so no automated run blocks.

**Steps:** generalize both `dev-setup.template.sh` and `.ps1` (the POSIX sh
needs portable indirection for `<role>_INSTALL` — **pin the exact technique
at build time**: `eval`-based lookup vs. a case dispatch the project fills,
choosing the more *readable* per the copy-ready rule); update the two
contributor-profile mentions in `project-trajectory/README.md` +
`README.template.md`; ADOPTING.md gains a one-line migration note for repos
that filled `DOMAIN_VIEWER_*`; the meta-repo dogfood
(`scripts/dev-setup.{sh,ps1}`) stays single-stack (one implicit `code` role)
— note it, don't force roles onto a one-stack repo.

**Tests:** `test_onboard_devsetup.py` —
`test_devsetup_has_edit_block_tiers_and_profiles` updated to the new role
tokens; default `--check` reports all roles; `--profile <role>` reports
baseline + that role only; unknown `--profile` exits nonzero naming the
declared roles; `sh -n` syntax valid; the headless no-TTY path still defaults
to all and exits 0.

**Risks:** **downstream migration** — this changes the profile vocabulary and
flips the default from `code`-only to all-roles, so a repo that filled
`DOMAIN_VIEWER_*` must move it into a role block (mechanical; the ADOPTING
note covers it) and installs slightly more by default (intended — "all
relevant packages"). Keep `code` + `design` (the renamed `domain`) as the
shipped examples so the rename is minimal. POSIX-sh indirection is sharp —
favor the readable dispatch, lean on `sh -n` + the smoke test. Scope creep
into a package manager — dev-setup stays detect-and-consent-install per
component, never a lockfile resolver.

**Done-when:** default installs baseline + every declared role; `--profile
<role>` narrows to that role; unknown role errors helpfully; the template
ships copy-ready with `code` + a placeholder role green on a fresh scaffold;
both READMEs + ADOPTING updated; `pytest -q` + `check_docs` green.

**Model tier — strong model** (dual sh/PowerShell surgery + test updates; the
Thread-15 class).

---

## Thread 44 — Security floor: an always-on secrets scan, split from the identity gate (opt-out)

**Status: ✅ landed 2026-07-05.** `check_privacy.py` now scans two independently
gated classes: the always-on **secrets floor** (private-key headers +
GitHub/Slack/AWS/`sk-…` shapes) runs in every repo including `inherit`, and the
**identity-leak** classes (home-dir usernames, off-policy emails, account/
hostname, global-git identity) stay gated on `docs/commit-identity`. Opt out of
the floor with the one word `off` in **`docs/secrets-scan`** (absent = on; the
`_first_declared_line` parse is now shared by both policy reads). The script
exits 0 fast only when *both* layers are off. Wiring: the pre-commit step now
runs unconditionally (the script decides); `check.py`'s `--repo` step already
ran unconditionally (comment corrected); the pre-push hook gained a
self-contained `inherit` branch that runs the secrets floor over the outgoing
`--range` — **tooling-gated, never fail-closed** (the identity guarantee doesn't
apply), leaving the anonymous review path byte-for-byte unchanged. Docs:
process-options gained a "Secrets floor (every repo)" subsection + the §9 NFR
security bullet pointer; both READMEs' script/hook rows; an ADOPTING.md §6
migration recipe flagging the behavior change (an `inherit` repo starts scanning
— that's the point; `off` is the escape). **Deviations / additions beyond the
spec's Done-when:** (1) kept one file (the spec's recommended conservative
default), no `check_secrets.py`; (2) added a **meta-repo dogfood** test asserting
this kit's own tracked tree passes the floor under its `inherit` policy — a real
net (this repo is `inherit`, so the floor newly applies), the honest form of the
spec's dogfood claim; (3) `test_pre_commit_hook`'s end-to-end test now `git
init`s its scaffold, since the now-unconditional step 3 reads the staged diff and
a pre-commit hook only ever runs inside a git repo. Tests: +8
(`test_check_privacy`: floor-under-inherit, opt-out, secrets-off-keeps-identity,
repo+range modes, meta-repo dogfood; `test_pre_commit_hook`: staged-key blocked +
opt-out; `test_pre_push_hook`: inherit floor blocks + opt-out). `pytest -q`: 329
passed, 1 skipped; `check_docs --root . --stale`: OK, 0 broken. Byte deltas:
AGENTS.template.md / PROCESS.md untouched (the knob lives in PROCESS_OPTIONS + the
hooks + the script).

**Source of scope (retained):** owner ask — give *every* repo a deterministic
secrets floor, not just anonymous ones, with an explicit opt-out for the rare
repo that needs an exit.

**Source:** owner review of the security posture (2026-07-05). Privacy
provisions exist (Threads 38/39/40) but security has no always-on floor. The
high-confidence secret patterns — private-key headers and the GitHub / Slack /
AWS / `sk-…` token shapes — already live in `scripts/check_privacy.py`, but the
**whole lint is gated on `docs/commit-identity` declaring a pattern** (an
`inherit` repo exits 0 immediately). So an ordinary identified repo — the
common home-brew case — commits an AWS key with **nothing in the kit flagging
it**, at any layer. That is an accident of where the patterns landed (the
docstring frames them as "universal token shapes," unrelated to anonymity),
not a design decision.

**The split.** Two classes of pattern, two gates:
- **Secrets floor — always on** (opt-out): private-key headers + the universal
  token shapes. These have nothing to do with identity; they run regardless of
  `docs/commit-identity`.
- **Identity-leak layer — policy-gated as today**: home-dir path shapes carrying
  an OS username, the current account/hostname, emails failing the declared
  pattern, the global-git-config identity appearing in content. These only make
  sense under an anonymity policy and stay gated on it (`inherit` pays zero for
  *these*, as now).

**Opt-out.** A one-word declared-policy file `docs/secrets-scan` (same
first-line parse as `docs/gate-policy` / `docs/push-policy` / `docs/privacy-review`):
absent or any value but `off` reads **on** (the safe default); `off` is the
deliberate exit for the strange repo that needs it (e.g. a repo whose *content
is* secret-shaped test fixtures and drowns in false positives — mark lines with
`privacy-ok` first; `off` is the last resort). The opt-out is a repo decision,
so it lives in a tracked file, not a flag.

**Mechanics:**
- **Keep one file** (SSOT for the patterns): broaden `check_privacy.py` rather
  than fork a `check_secrets.py` — a rename/second-file both cost downstream
  hook migration and split the pattern list. The docstring's "Honesty boundary"
  and gating prose get rewritten to describe the two-class split. *(Open
  spec-time call: if the identity framing of the filename grates, a thin
  `check_secrets.py` that imports the shared pattern constants is the
  alternative — but default to the conservative in-place broadening.)*
- The three existing modes are unchanged in shape (staged diff at pre-commit,
  `--repo` at gates, `--range` at pre-push) — but the **secrets subset now runs
  in all of them even under `inherit`**, gated only on `docs/secrets-scan`.
- The deep-scan boundary is **restated, not moved**: this is the deterministic
  floor of high-confidence patternable classes; gitleaks / trufflehog stay the
  named external product-layer category (never rebuilt in the kit).
- **Meta-repo dogfood — real, not n/a:** this repo is `inherit` (identity not
  declared), so the secrets floor **newly applies here** and the pre-commit /
  gate wiring is exercised on the kit itself.
- Docs: process-options "Commit identity & anonymity" gains a short "Secrets
  floor (all repos)" note distinguishing it from the identity-gated content
  privacy; the §9 NFR checklist's **security** bullet points at it.

**Tests:** an `inherit` repo with an AWS/`sk-…`/private-key line in the staged
diff now **fails** (was silent); the same repo with `docs/secrets-scan: off`
passes; an identity-only leak (home-dir username) stays **silent** under
`inherit` (still policy-gated) and still fails under a declared pattern; a
`privacy-ok` line is still exempt; RFC 2606 example domains still exempt;
`--repo` and `--range` exercise the secrets subset under `inherit`.

**Risks:** **downstream migration — flag it.** An identified repo that had *no*
scanning now gets secrets scanning on every commit; a repo carrying a
committed token that previously passed will start failing (that is the point,
but it is a behavior change — the ADOPTING resync note must call it out, and
`docs/secrets-scan: off` is the documented escape). False positives on
secret-shaped fixtures — the `privacy-ok` marker is the per-line affordance
before the repo-wide `off`. Scope creep — resist adding entropy heuristics or
new token vendors here; that is the external-product boundary.

**Done-when:** the secrets subset runs under `inherit`; `docs/secrets-scan:
off` disables it; the identity layer stays policy-gated and unchanged;
process-options + the NFR security bullet updated; the ADOPTING migration note
added; `pytest -q` + `check_docs` green.

**Model tier — strong model** (a gating-logic change in a security-sensitive
lint with a downstream-migration edge; the test matrix is the backstop).

---

## Thread 45 — Coordinator: a differentiated fail region (session errored ≠ ran-no-commit)

**Status: ✅ landed 2026-07-05.** `agent_loop.py` gained an **`ERROR`** outcome
between `COMMITTED` and `NO-COMMIT` in the per-session ladder, chosen when a
session failed *before it could work* and it is not a rate limit (`WAITING`
wins) or a timeout (`TIMEOUT` wins): the JSON result carries `is_error`, or a
non-JSON session exited nonzero. A new consecutive-`ERROR` counter (`errors`)
sits beside the single stall counter — kept single, so a persistently broken
agent still stops the loop and protects the budget — and picks the abort banner:
when a whole stall run was `ERROR`s the banner names an **unavailable agent**
(check the AGENT_CMD model + auth; an unsupported model is repointed by hand via
`--model` / the model map), otherwise the generic work-stall banner. Reporting
only: the `ERROR` label flows into the session log + `iteration_index.md` Outcome
column; exit code is unchanged (both aborts return `EXIT_STALL`). Auto model
fallback stays **out** (owner decision) — a silent tier swap could run an
unlisted, unguarded model. Docs: process-options "A failed session is not a work
stall" note under Unattended operation; the engine docstring (per-session bullet
+ exit-code line); the kit README coordinator row. **Deviation from spec:** the
detection was generalized past the spec's two named signals (`is_error` +
OSError sentinel) to *any* non-JSON nonzero exit — it mirrors the error signal
`limit_reset_hint` already trusts and subsumes the OSError-launch sentinel
cleanly (no fragile transcript substring match), covering plain-text agent
templates too. The dedicated exit code the spec floated as an open question was
**considered and declined** — no clean case; `EXIT_STALL` with a distinguishing
banner is the honest minimum. Tests: +4 (`test_agent_loop`: is_error→ERROR,
plain-text nonzero→ERROR, all-ERROR stall names an agent error, mixed
stall stays generic). `pytest -q`: 333 passed, 1 skipped; `check_docs --root .
--stale`: OK, 0 broken. Byte deltas: AGENTS.template.md / PROCESS.md untouched.

**Source of scope (retained):** owner ask — distinguish a session that
**errored before doing any work** from one that **ran and produced no commit**,
so a walk-away run that died fast doesn't misreport as a work stall.
Auto-fallback to a substitute model is **out of scope by owner decision** — an
unsupported model is handled manually (edit `docs/status.md` / the model map to
point at a live tier).

**Source:** owner review of `scripts/agent_loop.py` (2026-07-05). Today only
rate-limit wording gets special detection; every other pre-work failure —
`OSError` launching the CLI, an auth-expired / model-retired / broken-CLI
session that returns an error result — logs as `NO-COMMIT` and counts toward
the stall guard exactly like a healthy session that chose to do nothing. Three
failures in thirty seconds abort with the generic **STALL** banner ("N
consecutive sessions without a commit — aborting to protect the budget"),
which points the human at a *work-stall* diagnosis when the real cause is an
unavailable agent.

**The change (reporting, not new control flow):**
- A distinct **`ERROR`** outcome in the session-log metadata + the
  `iteration_index.md` Outcome column, chosen when the session failed **before
  work was possible** and it is **not** a rate limit: `run_session` returned an
  `OSError` (already `-1` with `coordinator: session error:`), **or** the JSON
  result carries `is_error` with no parseable reset hint. Ordering matters —
  the existing `WAITING` (rate-limit) branch wins first; `ERROR` is the
  not-a-limit error case; `NO-COMMIT` stays the *healthy-but-idle* case.
- The abort banner differentiates: when the runs that tripped the guard were
  `ERROR`s, the stop banner names it a **session/agent error** (point at the
  exit code + the latest `docs/iteration/` log, suggest checking the model map
  / auth / CLI), not a work stall.

**Deliberately minimal (record the deferred knobs):** keep the **single** stall
counter — a persistently-broken agent still stops the loop and protects the
budget; only the *label and the banner* differentiate. A separate
`--error-limit` (abort faster on hard errors than on idle sessions) and any
declared model-fallback are **deferred** — the owner ruled manual handling
sufficient for the unsupported-model case, and cross-CLI failure wording is the
hard, defer-until-seen part (the same reason the rate-limit parser only handles
observed wordings).

**Mechanics:**
- The outcome ladder in `main()` (around the current `WAITING / TIMEOUT /
  END_STATES / COMMITTED / NO-COMMIT` cascade) gains the `ERROR` rung between
  `TIMEOUT` and the state checks; reuse `limit_reset_hint(...) is None` as the
  not-a-limit guard and the `parse_json_result` `is_error` / `code` signals
  already computed.
- No change to exit codes (an `ERROR` run still flows to the stall path); the
  differentiation is the log metadata + the banner text. *(If the spec session
  finds a clean case for a dedicated exit code, raise it as a finding — don't
  add one silently.)*

**Tests:** an `OSError` launch logs `ERROR`, not `NO-COMMIT`; an `is_error`
JSON result with no reset hint logs `ERROR`; a healthy zero-commit session
still logs `NO-COMMIT`; a rate-limit session still logs `WAITING` (unchanged);
the abort banner text differs when the tripping runs were `ERROR`s.

**Risks:** mislabeling a *healthy* session as `ERROR` (a transcript that merely
mentions an error) — bind `ERROR` to the same *is-it-actually-an-error* signals
`limit_reset_hint` already trusts (`is_error` / nonzero exit / `OSError`), never
a substring scan of the transcript. Low downstream impact — this is
coordinator-internal reporting, no artifact-format or gate change.

**Done-when:** `ERROR` is a distinct logged outcome bound to real pre-work
failure signals; the stall/abort banner distinguishes an agent error from a
work stall; rate-limit and healthy-idle paths unchanged; `pytest -q`
(`test_agent_loop.py` extended) green.

**Model tier — Sonnet-able once specced** (a localized outcome-ladder edit with
a tight test matrix; strong model only if the spec session reopens the
exit-code question).

---

## Thread 46 — Identity→privacy reframe: `docs/privacy-check` toggle + commit-msg gate

**Status: ✅ landed 2026-07-06.** Split *identity* from *privacy* on the second
axis (Thread 44 kept the secrets floor untouched). The old
`docs/commit-identity` email **glob** did two jobs at once — the author *pin*
and the content *allowlist* — so loosening the allowlist to admit a tool's
`Co-Authored-By <noreply@anthropic.com>` co-author trailer collaterally
loosened the identity pin. Field trigger: a downstream (Finance-Auditor) repo's
push blocked on that trailer, and separately, commit **messages** were never
scanned at commit time (pre-commit runs before the message exists), so trailer
leaks piled up across 16 commits before pre-push surfaced them.

The reframe:
- **`docs/commit-identity` (glob) → `docs/privacy-check` (`true`/`false`
  toggle).** Which account authors is now the user's own git config, not pinned
  by a repo file. The gate defends *privacy* (no real, contactable person),
  keeping the Thread-44 secrets floor as the separate always-on axis.
- **Exempt-email allowlist moved into `check_privacy.py`** (`EXEMPT_EMAILS`,
  default `*noreply*`; a tight enumerated list ships commented-out). A no-reply
  address carries no contactable person, so it is exempt — a PII-risk reduction,
  not an anonymity guarantee. This admits the Claude trailer with no rewrite.
- **New `--author` mode** (author email must be exempt; wired into pre-commit,
  replacing the old pure-shell pin — recorded trade: no Python-less floor) and
  **`--message` mode** feeding a **new `.githooks/commit-msg` hook** that blocks
  a leaking title/body at the first commit.
- **Rewired:** pre-commit / commit-msg / pre-push, `bootstrap.py`
  (`--commit-identity` → `--privacy-check`; `commit-identity.template` →
  `privacy-check.template`; scaffolds commit-msg), `agent_loop.py` preflight,
  `setup.{sh,ps1}` (advise, no longer set identity), `check.py`. Docs:
  process-options "Commit identity & anonymity", both READMEs, CLAUDE.md, and an
  ADOPTING.md migration recipe (commit-identity → privacy-check). Tests: the
  5 privacy/hook/bootstrap/agent-loop files reframed + new commit-msg / --author
  / --message / EXEMPT coverage; `pytest -q`: 338 passed, 1 skipped.

**Model tier — landed.** Authored as an upstream port of the downstream field
fix; the privacy-check review path and the secrets floor are unchanged in shape.

---

## Thread 47 — Self-adoption: the kit runs its own `SN→SR→LLR→TC` spine (dogfood)

**Status: ✅ COMPLETE — landed 2026-07-07 (phases 1–7).** Session 1 (phases 1–2:
layout + SN), session 2 (phases 3–5: SR→LLR→TC spine, reached G2), session 3
(phases 6–7: the G3 walk). The meta-repo now **passes its own gates at G3**:
`check.py --gate G3` → PASS (format · lint · tests+coverage ~91% · traceability
`--require-verified` · privacy · doc-nav · perf · flows · arch-map), CI runs the
gate on itself, `docs/gate` = **G3**. Spine: SN=22 SR=36 LLR=33 TC=36, 0 orphans.
G1+G2 human-ratified 2026-07-07; **G3 ratification pending** (`docs/gate-policy` =
attended). Full gate-walk record in `docs/log.md`. The kit is now a project built
with the kit — the strongest evidence the method works. Dogfood findings it
surfaced and this thread resolved: **Thread 50** (SR/LLR citation coherence,
landed) + **Thread 51** (TC evidence column, backlog). The kick-off brief and
per-phase detail below are retained as the *why*.

> **Session 1 (2026-07-07, WI-1.39) — phases 1–2.** Layout laid: `docs/stack.ini`
> (`src=project-trajectory/scripts`, `tests=tests`; coverage threshold PROVISIONAL
> pending phase-6 subprocess-coverage), `docs/gate` (G1), the `docs/requirements/`
> + `docs/test/` registries (headers only), `docs/log.md`. Authored
> `docs/requirements/stakeholder-needs.md` — **SN-001..022** (12 core needs across
> the four stakeholders + privacy + proportionality; 10 edge-case rows, several
> citing the tests that already assert them). Reconciled `CLAUDE.md` +
> `docs/status.md`: the "SN-spine not self-applied" non-goal is **lifted**. Two
> dogfood papercuts found + fixed — the meta-repo README lacked the `#vision`
> anchor the SN template links to (added `<a id="vision">`); the bare `check_docs`
> gate flags the gitignored `docs/test/report.md` unless `--ignore` is passed
> (phase-6 `check.py` wiring passes it; deleted for now). **Gates:**
> `check_docs --root . --stale` OK, 0 broken; `pytest -q` **358 passed, 2 skipped**.
> `trace.py`: SN=22 SR=0 (22 SN-with-no-SR orphans — a **G2** bar, not gated at G1).
> **Deviations:** none. **Byte-budgeted files:** none touched.

> **Session 2 (2026-07-07, phases 3–5) — reached G2.** Authored the full
> `SR → LLR → TC` spine: **35 SR** (one cluster per shipped script/hook/policy,
> every SN-001..022 cited), **32 LLR** (one design-tier LLR per `Test`-verified
> SR — the `trace.py` orphan floor), **35 TC** (one per SR, the pytest node path
> in `Parameters`). SR-033/034/035 are `Inspection`/`Analysis` and LLR-exempt
> (release-checklist untested; stdlib-only + portability inspected). Authored
> `docs/architecture.md` with the **G2 Runtime flows** (3 sequence diagrams,
> 24 SR/LLR ids) that `check_flows.py` requires — see the deviation below.
> **Gates:** `trace.py --strict --no-placeholders --strict-schema` → `SN=22 SR=35
> LLR=32 TC=35 orphans=0 integrity=0 placeholders=0 schema-findings=0`;
> `check.py --gate G2` → **PASS** (traceability · privacy · doc-navigability ·
> design-flows); `pytest -q` → **358 passed, 2 skipped**; `check_docs --stale` →
> OK, 0 broken, 0 orphans. `docs/gate` G1 → **G2**; sign-off in `docs/log.md`
> (Human ratification PENDING under the `attended` gate-policy).
> **Deviation:** the brief sequenced `docs/architecture.md` into phase 6, but
> `design-flows` is a **G2** harness step and `check_flows.py` hard-fails without
> a "Runtime flows" section — which PROCESS.md §3 correctly places at G2 (flows
> authored *with the LLRs*). The Runtime-flows section was pulled forward to keep
> G2 honest; only the *generated* module map (`gen_arch_map.py`, a G3 step) stays
> in phase 6. **Kit-improvement finding:** `test-cases.template.csv` has no
> test-evidence column, so the concrete test is cited in `Parameters` as
> `node=…`; an `Evidence`/`Test` column is the cleaner upstream fix (dogfood
> surface). **Byte-budgeted files:** none touched (CLAUDE.md is not budgeted).

**Goal / why.** The kit *ships* the traceability spine + gates but does not yet
**apply them to itself**. Its own requirements live informally as these
IMPROVEMENT_PLAN threads, and its ~338 tests aren't traced to any need. Close the
loop: make the kit a project **built with the kit** — a derived vision,
stakeholder needs, system requirements, LLRs where they earn their keep, and test
cases that **point at the existing tests** — with `trace.py`/`check.py` green on
the meta-repo and CI enforcing it. The kit passing its **own** gates is the
strongest possible evidence the method works (and it will surface every rough
edge an adopter hits, from the inside).

**Start-state (already dogfooded — build on it, don't redo).** WI-1.22
("self-apply the unattended layer to this repo") already gave the meta-repo root
`docs/gate-policy`, `docs/push-policy`, and now `docs/privacy-check` (Thread 46
migrated it from `docs/commit-identity`). **Missing** for full self-adoption:
- `docs/requirements/{stakeholder-needs.md, system-requirements.csv,
  low-level-requirements.csv}` **and `docs/test/test-cases.csv`** — the kit's
  **own** registries (distinct instances, *not* the
  `project-trajectory/registries/*.template.*` files it ships to adopters). Mind
  the split: `trace.py` loads SR/LLR/SN from `docs/requirements/` but the TC tier
  from **`docs/test/`** (`load_csv(docs / "test" / "test-cases.csv")`);
- `docs/architecture.md` (one-page + generated map over
  `project-trajectory/scripts/` + authored runtime-flows for bootstrap and the
  coordinator);
- `docs/stack.ini` (declare `src = project-trajectory/scripts`, `tests = tests`,
  the ruff/pytest commands, coverage threshold), `docs/gate` (start G1),
  `docs/status.md` + `docs/log.md` for the meta-repo;
- the README `PROJECT-VISION:` tag already exists — reuse it as the kit's own
  vision (check_docs already enforces it).

**Approach (phased — a realistic first session lands 1–5 to reach G2 [SN→SR→LLR→TC
authored, zero orphans — LLRs are part of the G2 bar, not deferrable]; 6–7, the
full G3 walk + CI wiring + thread-history reconcile, may be a second session).**

1. **Layout decision (do first, record it).** The meta-repo's "product" is
   `project-trajectory/` (scripts, hooks, templates) + `tests/`. Put the kit's
   own trace files at **root** under `docs/requirements/` (SR/LLR/SN) and
   `docs/test/` (TCs) — the layout `trace.py` expects — and keep them **separate
   from the shipped templates** in `project-trajectory/registries/`. Add a short note
   to `CLAUDE.md` distinguishing "the kit's own spine (traces the kit)" from "the
   templates the kit ships". Point `docs/stack.ini` at
   `src=project-trajectory/scripts`, `tests=tests`.
2. **Vision + Stakeholder Needs (`SN`).** Derive from the README `PROJECT-VISION:`
   tag + `PROCESS.md`. Author `docs/requirements/stakeholder-needs.md` with an SN
   per stakeholder and their edge cases: **adopting developer** (mechanically-
   verified traceability; stack-agnostic portability), **AI agent / coordinator**
   (agent-neutral enforcement; safe, resumable unattended runs), **kit maintainer**
   (the kit's own changes stay traced/tested), **project evaluator** (gates are
   honest, never a false green). Include the privacy/secrets need explicitly.
3. **System Requirements (`SR`).** Decompose SN → measurable SRs, one cluster per
   shipped capability, each mapping to a script/hook so acceptance is already
   testable: traceability (`trace.py`), gate harness (`check.py`),
   doc-navigability (`check_docs.py`), arch-map freshness (`gen_arch_map.py`),
   secrets floor + privacy gate (`check_privacy.py` + the three hooks), scaffold
   (`bootstrap.py`), unattended coordinator (`agent_loop.py`), flows/perf/stubs,
   the declared-policy readers. Acceptance criteria = the behaviors the existing
   tests already assert.
4. **`TC` ← existing tests (the core mapping).** Author **`docs/test/test-cases.csv`**
   (note the path — the TC registry lives under `docs/test/`, *not*
   `docs/requirements/`) with TC rows: `Verifies = SR-###`, `Automated = yes`,
   `Tier` per the test's speed. **Recording the link to the concrete test needs a
   convention the kit doesn't yet ship:** the TC schema is
   `TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status` — there
   is no test-id field. Default to putting the **pytest node id** in `Parameters`
   (e.g. `node=tests/test_check_privacy.py::test_x`) so `--strict-schema`'s
   required-field checks stay satisfied; a first-class `Evidence`/`Test` column is
   the cleaner model but touches the shipped template — **capture that as a
   kit-improvement finding to upstream into `test-cases.template.csv`** (this is
   exactly the rough edge the dogfood exists to surface). **Keep it tractable —
   proportionality:** map at the *behavior* granularity (roughly one TC per test
   function, grouped by test file → SR), NOT a new test per row (the tests exist).
   Seed the rows mechanically: `pytest --collect-only -q` lists every node id;
   hand-assign `Verifies`. ~338 nodes collapse into SR-scoped TC clusters — do not
   over-explode micro-asserts.
5. **`LLR` — required for every Test/Demonstration/Manual SR, not optional.**
   Reconcile the proportionality instinct with `trace.py`'s hard orphan rule
   ("SR with no LLR"): an SR is LLR-**exempt only** when its `Verification` is
   `Analysis`, `Inspection`, or `Attest`. The kit's SRs are overwhelmingly
   `Test`-verified (the 338 automated tests), so **each Test-backed SR needs ≥1
   LLR** or it orphans at G2 — the "SR→TC direct, LLRs sparingly" shortcut would
   break this plan's own zero-orphan bar. Resolve it two honest ways, never by
   faking a method: (a) write **one design-tier LLR per capability SR** — the
   *design element* that implements it (e.g.
   `LLR: check_privacy.KEY_RE + scan_line detect PEM headers`), one-per-SR, **not**
   a micro-LLR per assert; and (b) set `Verification = Inspection`/`Analysis` where
   the SR is *genuinely* inspected rather than executed — "scripts are stdlib-only
   / run on 3.8+", "templates are copy-ready", "the process is stack-agnostic" —
   those are legitimately LLR-exempt. Still add LLRs for the load-bearing
   cross-script contracts regardless: the shared `_first_declared_line`
   declared-policy parse (hooks + `agent_loop` + `check_privacy` must agree —
   already tested), the arch-map marker-block contract, the `EXEMPT_EMAILS` /
   two-axis gating semantics. Guiding rule stays "no micro-LLRs the tests already
   cover" — but "one LLR per Test-SR" is the floor trace.py enforces, not a choice.
6. **Wire + walk the gates.** Add `docs/stack.ini`, `docs/gate` (G1, then bump),
   `docs/architecture.md` (+ `gen_arch_map.py` over `project-trajectory/scripts`,
   + a "Runtime flows" section for bootstrap and the coordinator loop). Run
   `trace.py --strict` (zero orphans), then `check.py --gate G2`, then `--gate G3`
   on the meta-repo; fix orphans and coverage. Extend the meta-repo's CI (today:
   pytest + check_docs) to run `check.py` on itself. Record gate sign-offs in the
   meta-repo's `docs/log.md`.
7. **Reconcile with the thread history.** These threads are the *design history*
   — don't delete them. Add a back-pointer from each major SR cluster to the
   thread(s) that motivated it (e.g. SR-privacy ← Threads 38/39/44/46), so the
   registries become the normative spec while the threads remain the *why*.

**Scope & proportionality (read `PROCESS_OPTIONS.md` "Proportionality doctrine"
first).** This is a **high-altitude** dogfood: the win is `SN→SR` ensuring
nothing key is missed + `TC←existing-tests` proving each SR is verified. Resist
turning tooling behavior into micro-LLRs. Target: an SR for every shipped
script/hook/policy-file, TCs citing the existing tests, **zero trace orphans**,
`check.py` green at the chosen gate.

**Complications to expect.**
- **Meta-repo layout vs. shipped templates** — keep the kit's own registries
  (`docs/requirements/` for SR/LLR/SN + `docs/test/` for TCs) distinct from
  `project-trajectory/registries/` (the templates it ships); `trace.py` runs over
  the former pair, `check_docs.py` over the docs. `bootstrap.py`'s own tests
  scaffold into temp dirs, so they won't collide.
- **The "product" spans Python + `sh` hooks + `md` templates.** `gen_arch_map`
  covers the Python; `architecture.md`'s prose + runtime-flows cover the hooks
  and the scaffold contract.
- **Coverage reads ~0 under the current test architecture — plan for it, don't
  discover it at G3.** `check.py --tier full` enforces `--cov-fail-under=80`, but
  the meta-tests run every script as a **subprocess** (`conftest.run_py` →
  `subprocess.run([sys.executable, …])`) and coverage only instruments the
  *current* process — so `--cov=project-trajectory/scripts` reports near-nothing
  however thoroughly the scripts are exercised, and there is no
  `.coveragerc`/`COVERAGE_PROCESS_START` plumbing today. The honest number isn't
  "low", it's *uninstrumented*. Two exits: wire **subprocess coverage**
  (`COVERAGE_PROCESS_START` + a `.pth`/sitecustomize, `parallel=true`,
  `coverage combine`) so the real figure appears, or set the meta-repo's
  `stack.ini` threshold to what *is* measured with a recorded note of why (the
  kit's own §4 "never hand-waved" rule). Do **not** silently lower the bar.
- **Chicken-and-egg.** The meta-repo **hand-authors** its registries from the
  templates; it can't bootstrap itself onto itself. Expected, not a blocker.
- **Some scripts are the checkers** (`trace.py`, `check.py`) — their SRs are
  verified by the tests that already run them against fixtures.

**Kick-off note (new session).** Read this thread + README `PROJECT-VISION:` +
`PROCESS.md` §1–4; run `pytest --collect-only -q` to inventory the tests you'll
map; author `docs/requirements/stakeholder-needs.md`; grow the spine as a real
**G1→G2→G3** walk on the meta-repo under its declared `docs/gate-policy`.

**Model tier — strong model for the vision/SN/SR derivation and the LLR
right-sizing** (judgment-heavy); the `TC` back-mapping is mechanical and
Sonnet-able once the SR skeleton exists.

### Session 2 kick-off — phases 3–5 (detailed, self-contained)

**Where session 1 (WI-1.39) left off.** `docs/requirements/stakeholder-needs.md`
holds **SN-001..022** (12 core + 10 edge). `system-requirements.csv`,
`low-level-requirements.csv`, `docs/test/test-cases.csv` are **header-only**.
`docs/gate` = **G1**. `trace.py`: SN=22 SR=0 (22 SN-with-no-SR orphans, un-gated
at G1). **Goal of session 2: author `SR → LLR → TC`, drive orphans to zero, bump
`docs/gate` to G2, and sign it off in `docs/log.md`.**

**The backbone — capability → script → tests → SR cluster.** Each row is one SR
cluster (1–3 SRs); its `AcceptanceCriteria` are what its tests already assert;
its TC cites the test file. (Counts from `pytest --collect-only` 2026-07-07;
~360 tests total.)

| Area (SR cluster) | Script(s) | Test file(s) — count | SN-Refs (main) |
|---|---|---|---|
| Traceability + integrity | `trace.py` | test_trace (20), test_registry_checks (18), test_ac_advisory (7) | SN-002, SN-022 |
| Off-spine registries (MOD/PART/ASSET) | `trace.py` | test_modules_registry (7), test_procurement (5), test_assets (4) | SN-002 |
| Gate/tier harness | `check.py` | test_check_harness (8) | SN-004, SN-008, SN-014 |
| Declared stack profile | `check.py` + stack.ini | test_stack_profile (23) | SN-003 |
| Conditional scaffold profiles | `bootstrap.py` | test_profile (21) | SN-003, SN-012 |
| Scaffold generation | `bootstrap.py` | test_bootstrap (33) | SN-001 |
| Doc navigability | `check_docs.py` | test_check_docs (24) | SN-010 |
| Runtime-flows check | `check_flows.py` | test_check_flows (6) | SN-010 |
| Perf comparator + budgets | `check_perf.py` | test_check_perf (15), test_perf_budgets (6) | SN-004 |
| No-stub detector | `check_stubs.py` | test_check_stubs (13) | SN-008 |
| Secrets + privacy lint | `check_privacy.py` | test_check_privacy (18) | SN-009 |
| Git hooks (process floor) | hooks/* + check_privacy | test_pre_commit_hook (11), test_pre_push_hook (16) | SN-005, SN-009, SN-013 |
| Vendored-doc drift | `check_vendored.py` | test_check_vendored (5) | SN-010 |
| Arch-map generation | `gen_arch_map.py` | test_gen_arch_map (20) | SN-010, SN-021 |
| Permutation case gen | `gen_cases.py` | test_gen_cases (5) | SN-002 |
| Skills index | `gen_skills_index.py` | test_skills_index (4) | SN-012 |
| Unattended coordinator | `agent_loop.py` | test_agent_loop (32) | SN-006, SN-015, SN-016, SN-019, SN-020 |
| Parallel tracks | `agent_loop.py` | test_agent_loop_tracks (19) | SN-006, SN-017, SN-018 |
| Declared-policy readers | shared `_first_declared_line` | test_gate_policy (5), test_push_policy (5) | SN-004 |
| Onboarding + dev-setup | onboard/dev-setup templates | test_onboard_devsetup (10) | SN-001 |
| Release checklist | `gen_release_checklist.py` | ⚠ **no dedicated test file** | SN-004 |
| Portability (Inspection/Analysis) | all scripts | — (inspected, not executed) | SN-003, SN-011 |

**Phase 3 — SRs (`docs/requirements/system-requirements.csv`).** One cluster per
row above, 1–3 SRs each (**~30–40 total**). Columns
`SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status,Phase,Area`:
- `SN-Refs` — the need(s) realized (table's last column). **Every SN-001..022
  must be cited by ≥1 SR** (the G1 coverage rule; `trace.py` flags an SN with no
  SR). The edge-case needs SN-013..022 are realized by the **coordinator / hooks
  / trace / arch-map** clusters' *failure-handling* AcceptanceCriteria — make
  sure each is cited so none orphans.
- `AcceptanceCriteria` — **the behavior the tests assert** (cite it; don't invent
  a new bar).
- `Verification` — **`Test`** for anything a pytest exercises (the vast
  majority); **`Inspection`** for "scripts are stdlib-only" / "templates are
  copy-ready"; **`Analysis`** for "the process is stack-agnostic / runs on 3.8+".
  *Load-bearing:* a `Test`/`Demonstration`/`Manual` SR **requires an LLR**
  (phase 5); an `Inspection`/`Analysis`/`Attest` SR is **LLR-exempt**.
- `Area` = the cluster name (enables `Area`-filtered review); `Phase` = blank
  (all in scope now); `Status` = `Verified` (its tests pass) — keep one
  convention. Drop a **thread back-pointer** in `Rationale` (phase 7, cheap now):
  privacy ← Threads 38/39/44/46; coordinator ← 33/45; tracks ← "Parallel tracks".

**Phase 4 — TCs (`docs/test/test-cases.csv`).** **One TC per SR** (proportional —
NOT one per test function): `TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status`:
- `Verifies` = the `SR-###` **plus its `LLR-###`** once phase 5 exists
  (`SR-0xx;LLR-0xx`).
- `Parameters` = the **pytest node path** citing the test file:
  `node=tests/test_check_privacy.py` (the whole file is the behavior cluster; add
  `::test_x` only to pin a single decisive case). *The schema has no test-id
  column — this is the agreed workaround; **also file the kit-improvement finding
  to add an `Evidence` column to `test-cases.template.csv`** (surfaced by this
  dogfood).*
- `Tier` = `Full` (or `Smoke` for a `@pytest.mark.smoke` test); `Automated` =
  `Yes`; `Method` = one line ("run the file's suite; all pass").

**Phase 5 — LLRs (`docs/requirements/low-level-requirements.csv`).** **One
design-tier LLR per `Test`-verified SR** (the `trace.py` orphan floor — not
optional): `LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status`:
- `Module` = `project-trajectory/scripts/<script>`; `CodeSymbol` = the key
  function/class (e.g. `check_privacy.scan_line`, `agent_loop.acquire_lock`,
  `trace` load+join); `Detail` = the design element in one line; `SR-Refs` = its
  SR; `TestRefs` = "(see TC-0xx)".
- **Not** a micro-LLR per assert. Skip LLRs only for `Inspection`/`Analysis` SRs.
  Add the cross-script contract LLRs the parent plan names
  (`_first_declared_line` shared parse; arch-map marker-block contract;
  `EXEMPT_EMAILS` / two-axis gating) if not already an SR's design element.

**Order of operations (keep trace checkable).** (1) Author **all SRs** →
`trace.py` (SR-with-no-LLR/TC orphans expected, fine at G1). (2) **One LLR per
Test-SR**. (3) **One TC per SR**. (4) `trace.py --strict` → drive orphans to
**0** (every SR: SN + LLR-or-exempt + TC; every LLR: SR + TC; every TC verifies a
real SR/LLR; every SN: ≥1 SR). (5) `trace.py --no-placeholders --strict-schema` →
no leftover `-000`, required fields non-empty. (6) bump `docs/gate` → **G2**, run
`check.py --gate G2` — **leave coverage / `--tier full` for phase 6** (the
subprocess-coverage issue). (7) record the G2 sign-off in `docs/log.md`.

**Done-when (G2).** `trace.py --strict --no-placeholders` = 0 orphans / 0
integrity; every SN-001..022 cited; `pytest -q` + `check_docs --root . --stale`
green; `docs/gate` = G2 with a `docs/log.md` sign-off; Thread 47 status updated
(session-protocol step 4). **~30–40 SR / ~30–40 LLR / ~30–40 TC** is the expected
size — resist exploding to per-test rows.

**Gotchas.** (a) `gen_release_checklist.py` has **no dedicated test** — give it an
`Inspection` SR or note the coverage gap honestly; don't fake a TC. (b) The bare
`check_docs` flags the gitignored `docs/test/report.md` — delete it before the
gate or pass `--ignore 'docs/test/report.md'` (phase 6's `check.py` passes it).
(c) Coverage `--cov` under-reports (subprocess) — **phase 6**, not now. (d) Keep
the meta-repo registries under `docs/requirements/` + `docs/test/`, never the
shipped `project-trajectory/registries/` templates. **Model tier — strong for
the SR derivation + Verification-method calls; the TC/LLR back-mapping is
mechanical once the SR skeleton + this table are in hand.**

---

## Thread 48 — Open Knowledge Format (OKF) export: the traceability graph as a portable knowledge bundle

**Status: 📋 PLANNED — spec for a fresh session (unscheduled).** This entry *is*
the kick-off brief; a new session reads it top-to-bottom, then executes. Two
layers: **A** = the requirement-graph export (the clear win, do first); **B** =
the process docs as concepts (optional, secondary).

**Goal / why.** Google's **Open Knowledge Format** (OKF v0.1,
`GoogleCloudPlatform/knowledge-catalog/okf`) is an open, vendor-neutral spec for
AI-consumable knowledge: a **directory of markdown files with YAML frontmatter**,
one file per *concept*, **file-path-as-identity**, normal markdown links forming
a graph, optional `index.md` (progressive disclosure) and `log.md` (history),
*minimally opinionated* (only a `type` field is required). The kit is already
~80% an OKF-shaped thing — markdown docs, an append-only `log.md`, stable
never-renumbered IDs (a natural file identity), and a real concept graph in
`SN→SR→LLR→TC`. This thread makes that latent alignment explicit by
**generating** an OKF bundle from the existing registries, so the kit's
traceability knowledge is portable into any OKF consumer (Google's static-HTML
visualizer, a company-wide knowledge catalog, another org's agents) with **no new
source of truth and no runtime dependency**. It extends the kit's mission —
"readable for humans and agents alike" — from *process* to *knowledge interop*,
and is the natural next generated view after Thread 1 (generated traceability
views) within Thread 8's map-vs-index boundary (this is a generated **map**,
never hand-maintained).

**The iron constraint (read first).** OKF here is a **generated export, never a
parallel source of truth.** The reviewed truth stays the CSV registries; the
bundle is regenerated from them and freshness-checked (`--check`) exactly like
the arch map. A hand-edited OKF copy of the requirements would reintroduce the
drift the whole kit exists to prevent. Corollary for **stdlib-only**: *emitting*
YAML frontmatter is trivial string-formatting (no parser, no dependency); the kit
must **not** try to *parse/validate arbitrary* OKF (stdlib has no YAML) — it
emits, and leans on OKF's own reference tooling to consume.

**Start-state (build on it, don't rebuild).**
- `scripts/trace.py` already **loads every registry and builds the join**
  (`SN→SR→LLR→TC` + off-spine `IF/PB/PART/ASSET`) and emits a generated
  HTML/Mermaid view — reuse its load+join, don't re-parse the CSVs.
- The **generator pattern** is established and stdlib: `gen_arch_map.py`,
  `gen_release_checklist.py`, `gen_cases.py`, `gen_skills_index.py`, each with a
  `--check` freshness mode. `gen_okf.py` is one more of these.
- Stable IDs (`SR-042`, never renumbered — Threads 1/35) map directly onto OKF's
  "file path is the concept's identity."
- `docs/log.md` (Thread 36) is already an append-only history — OKF's optional
  `log.md`, for free.
- `check_vendored.py` (the guardrails layer, Thread 41) is the exact pattern for
  pinning an upstream (OKF v0.1) and warning on drift.

**Missing:** `scripts/gen_okf.py`, the emitted `docs/okf/` bundle, the stable
`type`-name vocabulary, the freshness/CI wiring, bootstrap scaffolding, tests,
and a commit-vs-gitignore ruling for the bundle.

**Layer A — the requirement graph as an OKF bundle (do this first).**

1. **Bundle layout + identity.** Emit a generated root `docs/okf/`, one
   subdirectory per tier, one file per concept, path = identity:
   ```
   docs/okf/
     index.md
     stakeholder-needs/    SN-001.md …   (+ index.md)
     system-requirements/  SR-001.md …   (+ index.md)
     low-level-requirements/ LLR-001.md …
     test-cases/           TC-001.md …
     interfaces/           IF-001.md …   (off-spine, when present)
   ```
2. **Frontmatter mapping (a stable `type` vocabulary — document it once).** Per
   concept, a YAML frontmatter block written by string-formatting: `type`
   (required — "Stakeholder Need" / "System Requirement" / "Low-Level
   Requirement" / "Test Case" / "Interface" / "Performance Budget"), `title` (the
   row's Title), `description` (the Requirement/Need one-liner), `tags`
   (Area/Priority/Verification/Status where that column exists), `timestamp`
   (generation time), `resource` (a stable back-anchor to the CSV row of record).
   Only fields the registries actually carry; OKF is minimally opinionated, so
   extra columns ride as tags or body sections.
3. **Body + the graph (markdown links).** The body carries the human content
   (AcceptanceCriteria, Rationale, Detail) and **reconstructs the graph as normal
   markdown links** from trace.py's join: an `SR` links **up** to its `SN`s
   (`SN-Refs`) and **down** to its `LLR`s and `TC`s (reverse lookups); a `TC`
   links to what it `Verifies`; an `LLR` to its `SR` parent + `Module`. This is
   the "weave the wiki in" step — the wiki *is* the browsable graph view of the
   spine.
4. **`index.md` progressive disclosure.** A root `index.md` (counts + links to
   each tier index) and a per-tier `index.md` (one-line-per-concept table), so an
   agent navigates top-down — the OKF pattern the kit already approximates with
   AGENTS.md → PROCESS.md → registries.
5. **Freshness contract + floor placement — ruled (owner): on by default,
   opt-out.** `gen_okf.py --check` regenerates into memory and diffs the on-disk
   bundle, nonzero on drift — the `gen_arch_map.py --check` contract, and a
   **required `check.py` floor step**. Governed by a `docs/okf-export`
   declared-policy on the **secrets-scan pattern**: absent / any value = **on**
   (the agent-dev readability win ships by default), the one word `off` opts out
   (the escape for a repo where the churn or the external-spec coupling bites —
   Complications). **Because it is on by default, fresh-scaffold greenness is a
   hard requirement:** bootstrap scaffolds a valid (empty/placeholder) bundle and
   `gen_okf --check` passes on a clean scaffold out of the box (mirror
   `test_fresh_scaffold_passes_archmap_check_and_trace`).
6. **Commit the bundle — ruled (owner).** Commit `docs/okf/` **and** the other
   generated composites (trace `report.html`/`report.md`, `perf-report.md`) —
   **for availability, not change control**: a fresh clone / CI has the rendered
   outputs immediately, no regen step required to view them. Un-ignore them in
   `gitignore.template`. Three riders keep committed-generated painless: (a) mark
   them `linguist-generated` + `-diff` in `.gitattributes` so their diffs are
   suppressed from review (availability, not change-control — literally); (b)
   **write-if-changed** on generation, so a no-op run never dirties the working
   tree; (c) keep each under a `--check` step so a committed artifact can never
   silently rot — committing *enables* the freshness enforcement, it doesn't
   weaken it. (Owner may revert to gitignore if diff sizes grow.)

**Layer B — the process docs as OKF concepts (optional, secondary).** Makes the
*whole* repo — process knowledge + requirement graph — one conformant bundle.
Two shapes:
- **B2 (recommended, non-intrusive):** `gen_okf.py` also emits `type: Process
  Guide` concept files that summarize + `resource`-link the real docs
  (`AGENTS.md`, `PROCESS.md`, `status.md`, `architecture.md`, `interfaces.md`),
  leaving the sources untouched — single-source-friendly, no byte-budget hit.
- **B1 (opt-in, intrusive):** add `type:` frontmatter to the source docs
  themselves so `docs/` is *natively* a bundle. Costs: touches every scaffolded
  doc template, and **`AGENTS.md` is byte-budget-watched** (Thread 26) —
  frontmatter eats headroom. Reserve for a repo that specifically wants
  doc-native OKF.
Default to **B2**; ship **B1** only behind a flag.

**Scope & proportionality.** A **generated interop view**, opt-in, off the gate
floor — in the lineage of Thread 1 and Thread 8. Resist building a
*validator/consumer* (stdlib has no YAML; OKF ships its own tools). Target:
`gen_okf.py --check` green, a conformant bundle from the demo project, **zero**
new required-gate surface, **zero** runtime deps.

**Complications to expect.**
- **v0.1 churn.** OKF is "a starting point, not a finished standard." Pin the
  targeted spec commit in a `docs/okf/UPSTREAM`-style note and hash-check it via
  the `check_vendored.py` pattern, so a spec bump is a visible, human-reviewed
  re-target, never silent drift.
- **stdlib emit-only.** Emitting frontmatter = string formatting (fine). Never
  add a YAML dependency to *read* OKF — that is the consumer's job.
- **Off-spine tiers.** `IF/PB/PART/ASSET` are integrity-only, not on the joined
  spine — include them as concepts but don't fabricate spine edges trace.py
  doesn't assert.
- **Default-on risks (accepted; `docs/okf-export: off` is the escape).** On by
  default means every repo carries bundle generation + committed churn and — the
  one to watch — **the gate is coupled to an external v0.1 spec**: a breaking OKF
  change could block gate advancement until you re-target. Pinning via the
  `check_vendored` pattern makes that a *visible, human-reviewed* bump, not silent
  drift. The owner accepts these for the agent-dev readability win and will
  iterate; `off` is the one-word opt-out where the churn or coupling bites, and
  the per-permutation matrix must include an `okf-export: off` cell so the skip
  path stays tested.
- **Parallel tracks.** Under the "Parallel tracks" layer the spine stays
  repo-singular, so there is **one** bundle per repo — never per-track bundles.

**Kick-off note (new session).** Read this thread + the OKF v0.1 spec
(`GoogleCloudPlatform/knowledge-catalog/okf`) + `scripts/trace.py` (reuse its
load+join). Prototype `gen_okf.py` against the demo project (conftest
`make_minimal_project`), eyeball the bundle in OKF's static-HTML visualizer, then
wire `--check` + a test asserting: every emitted file has a `type` frontmatter,
every markdown link resolves (reuse `check_docs.py`), and `--check` fails on a
stale bundle. Land Layer A; leave Layer B (B2) as a follow-commit.

**Model tier — mid/strong for the mapping design** (judgment: the `type`
vocabulary, link topology, the commit-vs-gitignore call); the emitter itself is
mechanical once the mapping is fixed.

---

## Thread 49 — Documentation-currency hardening: symbol-reference validation + deterministic freshness

**Status: 📋 PLANNED — spec for a fresh session (unscheduled).** Kick-off brief.
Encapsulates the two anti-rot gaps that link-validation alone leaves open (raised
alongside Thread 48).

**Goal / why.** `check_docs.py` validates that a markdown link *resolves*; it
does **not** catch two rot classes: (1) prose that names a code symbol / file /
flag which no longer exists (the link resolves, the sentence is stale — invisible
today), and (2) a *generated* artifact that has drifted from its source, because
the only freshness signal for docs is an **mtime `--stale` hint** that is
*non-gating* and *unreliable in git* (clones reset mtime; it has fired
spuriously). Close both so documentation currency is machine-enforced where it
can be, advisory only where it genuinely must be. This is the general form of the
lever Thread 48 leans on (generate + `--check` + commit); Thread 49 extends it to
hand-authored prose and audits the enforcement.

**Start-state (build on it).**
- `check_docs.py` = intra-repo link *resolution* + the mtime `--stale` hint.
- `gen_arch_map.py` already **extracts the public symbol inventory** per module
  (summaries, dependencies, public symbols with `Implements:` backlinks) — that
  inventory is the **oracle** for item 1; reuse it, don't re-parse the AST.
- The generator/`--check` pattern is established (`gen_arch_map`,
  `gen_release_checklist`, `gen_cases`, `gen_skills_index`, Thread 48's
  `gen_okf`). Item 2 is about which freshness signals *gate*.
- `check_stubs.py` is the model for a **warn-first, product-layer,
  language-specific** check that is *not* wired into the required floor — the
  right shape for the symbol side.

**Item 1 — symbol-reference validation (the real gap).** A check (extend
`check_docs.py` or a sibling `check_doc_refs.py`) that fails on a documentation
reference to a code entity that does not exist. The whole design problem is
**false-positive control** — you cannot flag every backticked token (`off`,
`type`, shell snippets, other repos' names). Two precise tiers:
- **Paths/filenames — validated aggressively** (low ambiguity, high value): a
  backticked token matching a repo-path shape (`*.py`, `scripts/*`, `docs/*`,
  `.githooks/*`) that does **not** exist on disk is almost always rot → flag it. A
  renamed/deleted file named in a doc is one of the commonest real rots.
- **Code symbols — validated via an explicit opt-in convention** (no heuristic
  storm): only references written in a declared form (e.g. an `Implements:`-style
  `sym:<module>.<name>` marker, or a dedicated link scheme) are checked against
  the arch-map inventory. Precise like the kit's other conventions (`privacy-ok`,
  `Implements:`, the `-000` placeholder rule): you *assert* a symbol exists and
  the check holds you to it, instead of guessing which words are symbols.
- **Ships warn-first** (exit 0 unless `--strict`), product-layer like
  `check_stubs.py`: symbol conventions are language-specific, so it informs the
  human/LLM review and a non-Python stack degrades gracefully (no arch-map
  symbols → the symbol tier skips, the path tier still runs).

**Item 2 — deterministic freshness, promoted to a gate (generated content only).**
The mtime hint is the wrong primitive (unreliable in git) and the wrong severity
(advisory). The fix is **not** to harden mtime — it is to give *generated*
artifacts a **deterministic** freshness contract and enforce it:
- Every generated artifact gets a `--check` that **regenerates-and-diffs** (or
  compares a **source-content-hash stamp** in its header) — no mtime. Audit the
  set: `gen_arch_map`/`gen_skills_index` already have it; the trace `report.*` and
  `perf-report.*` (now **committed** per Thread 48) need one; `gen_okf --check` is
  Thread 48.
- Wire these `--check`s as **required `check.py` steps** so a stale *generated*
  doc fails CI, not merely hints. Committing the artifacts (Thread 48) is what
  makes this enforceable.
- **Hand-authored prose stays advisory:** nothing to regenerate-and-diff, so keep
  a *clearly-labeled* hint and rely on item 1 for the concrete rot prose actually
  suffers. Do **not** promote the mtime prose hint to a failure — that is the
  false-positive trap.

**Scope & proportionality.** **Not** a general prose linter. Bound it to (a)
path/filename existence, (b) opt-in symbol references, (c) deterministic `--check`
on generated artifacts. Only (c) joins the required floor; the symbol tier is
warn-first/product-layer. Target: a renamed file or a dangling *asserted* symbol
is caught; a clone never false-fails on mtime; zero new runtime deps (reuse the
arch-map extractor).

**Complications to expect.**
- **False positives are the whole risk.** The path-shape + opt-in-symbol split is
  the mitigation; resist "validate every backtick."
- **Non-Python stacks.** The symbol oracle is the arch map, which degrades to
  files-mode on non-Python (no symbol inventory) → the symbol tier skips, the path
  tier still runs. Same posture as `check_stubs`.
- **mtime is not the fix.** Deterministic freshness (regenerate-diff /
  source-hash) replaces it for generated docs; don't gate on mtime anywhere.
- **Interaction with Thread 48.** OKF bundles are generated + link-only, so
  item 2's `--check` covers them and they add no prose-rot surface; item 1 targets
  the hand-authored docs.

**Kick-off note (new session).** Read this thread + `check_docs.py` +
`gen_arch_map.py` (the symbol extractor is the oracle). Prototype the
**path-existence** tier first (cheap, high-value, low-false-positive), then the
**opt-in symbol** convention; add the deterministic-freshness audit as a separate
pass. Test against the demo project (`make_minimal_project`): a doc naming a
deleted `scripts/x.py` fails; a valid asserted symbol passes; a clone (mtime
reset) never false-fails.

**Model tier — mid for the convention design** (the false-positive boundary is
the judgment call); mechanical to implement once the reference syntax + the tier
split are fixed.

---

## Thread 50 — `trace.py`: TC triangle-consistency check (SR/LLR citation coherence)

**Status: ✅ landed 2026-07-07.** `trace.py` gained `triangle_findings()`, wired
into the integrity set (joins `--strict` and the `--strict-integrity` pre-commit
floor); 4 tests in `tests/test_registry_checks.py` (incoherent pair fails
integrity + strict, coherent chain green, a unit test over the function). The
kit's own 35 TCs pass unchanged (coherent by construction); `EXAMPLE.md` and the
`-000` template rows are coherent/excluded, so a fresh scaffold stays green.
`pytest -q` → 362 passed, 2 skipped. **Deviation:** none. **Byte-budgeted files:**
none touched — PROCESS.md's integrity parenthetical is illustrative, and the
authoritative integrity enumeration is the `trace.py` docstring (which was
updated), so PROCESS.md stayed flat (56375 B). The spec/rationale below is
retained as the *why*.

**Status: 📋 SPEC — surfaced by Thread 47 (self-adoption) 2026-07-07; owner
direction recorded below.** A small, well-scoped change to a shipped kit script.

**The finding.** A `TC`'s `Verifies` cell may cite an SR **and** an LLR at once
(the `SR-0NN;LLR-0NN` form the kit uses so *one* real test discharges both the
"SR needs a TC" and "LLR needs a TC" orphan rules — coverage is not transitive,
[trace.py:762](project-trajectory/scripts/trace.py#L762)/[778](project-trajectory/scripts/trace.py#L778)/[803](project-trajectory/scripts/trace.py#L803)).
But the SR↔LLR relationship is *also* recorded canonically on the LLR's
`SR-Refs`. So the combined TC citation **duplicates** that relationship, and
`trace.py`'s TC validation only checks that each cited id **exists**
([trace.py:808-817](project-trajectory/scripts/trace.py#L808-L817)) — it never
checks the pair is coherent. An inconsistent triangle passes clean today:
`TC-099,SR-005;LLR-001` where `LLR-001` decomposes `SR-001`, not `SR-005`.

**Owner direction (2026-07-07).** Accept the duplication as the smaller evil and
add a consistency check, rather than the two rejected alternatives: (a) make the
TC `Verifies` **exclusive** (a single SR *or* LLR) plus a **transitive-coverage**
rule ("an SR with no direct TC is covered if an LLR of it has a TC") — rejected as
more confusing and a change to the orphan model; (b) **expand** the TC table to a
separate SR-level and LLR-level test per behavior — rejected as a giant, low-value
row explosion (the very thing the proportionality doctrine and the Thread-47 TC
mapping avoid). The canonical SR↔LLR edge stays the LLR's `SR-Refs`; the TC's
combined citation is a derived convenience the checker must keep honest.

**The change.** When a TC cites both an SR and an LLR in one `Verifies` cell, the
LLR's `SR-Refs` **must include that SR**; otherwise it is a finding. This is a
structural-coherence error, wrong at any stage like a malformed/duplicate id — so
it belongs in the **integrity class** (joins `--strict-integrity`, the pre-commit
floor), not the gate-scoped orphan set. Add the check in the TC loop next to the
existing unknown-ref check; new tests in `tests/test_registry_checks.py` (a
coherent triangle passes; an incoherent one fails `--strict-integrity`). Update
`trace.py`'s module docstring (the "Always … integrity" list) and, if the shipped
`EXAMPLE.md`/templates lean on the combined citation, keep them coherent.

**Done-when.** `--strict-integrity` fails an incoherent SR/LLR pairing and passes
a coherent one; existing suites stay green; the kit's own registries (35 TC,
already coherent by construction) still pass. **Model tier — mechanical once the
rule is fixed** (it is, above).

---

## Thread 51 — `TC` schema: a first-class test-evidence column

**Status: 📋 BACKLOG — surfaced by Thread 47 (self-adoption) 2026-07-07; recorded
for posterity, not yet ruled.** A change to a **shipped** artifact (adopter-facing),
so weigh it more carefully than Thread 50.

**The finding.** The `TC` schema
(`TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status`) has **no
column for the concrete test that provides the evidence** — the pytest node, the
demo script, the manual-procedure doc. Thread 47's self-adoption needed to cite
the real test per TC and had nowhere clean to put it, so it overloaded
`Parameters` with a `node=tests/test_x.py` string (see the phase-4 note + the 35
rows in `docs/test/test-cases.csv`). That works but conflates two ideas:
`Parameters` is meant for the *dimensional inputs* a test exercises (the
`gen_cases.py` grammar), not a pointer to the test's location.

**Proposal (to be ruled).** Add an `Evidence` (or `Test`) column to
`registries/test-cases.template.csv` naming the test's location — a path, a node
id, or a procedure-doc link. Keep `Parameters` for dimensional inputs. Open
questions the ruling must settle:
- **Required or optional?** Likely *optional* at G2, *required-non-empty for
  `Automated=Yes` rows at G3* (a claimed-automated test with no cited location is
  a soft false-green). If required, it joins `REQUIRED_FIELDS["TC"]` under
  `--strict-schema`.
- **Validated how?** Path-existence checking is stack-specific and brittle
  (pytest node ids aren't filesystem paths); probably **inspection-only** text,
  like the `Method` cell — not a mechanized resolve.
- **Migration cost.** Adds a column to a shipped template → every adopter's
  `test-cases.csv` gains a field; `EXAMPLE.md`, the `bootstrap.py` file lists, and
  the `trace.py`/`check.py` readers must stay coherent. This is the reason it's
  backlog, not a quick fix.

**Why lower priority than Thread 50.** Thread 50 keeps an *existing* rule honest
(a bug-class); this *adds* a field to the shipped schema (an enhancement with
migration cost). Do Thread 50 first; ruling on Thread 51 can wait until the
`Parameters`-overload has bitten more than once. **Model tier — mid for the
required/validated ruling; mechanical to implement once ruled.**

---

## Thread 52 — Trajectory / work-items layer (upstreaming gilbert WB19 · D19-6)

**Status: ✅ COMPLETE — all 4 phases landed (P1–P3 2026-07-07, P4 2026-07-08);
the layer is built, documented, and dogfooded on real data. Records below.** A
**new opt-out kit layer**: a machine-readable work-item
registry + a generated, fully-offline trajectory dashboard. Bigger than Threads
48–51 — multi-phase, touches shipped templates, the spine, PROCESS_OPTIONS, and
(Phase 4) the kit's own plan. **Downstream-migrating.**

**Phase 1 landed 2026-07-07 (this session).** The registry + validation half,
fully offline (no JS). **Deliverables:** `registries/work-items.template.csv` (the
gilbert schema `WI-ID,Title,Track,SR-Refs,Predecessors,Status,Deliverable` + an
inert `WI-000` example row); `scripts/check_trajectory.py` — a stdlib validator:
WI-id shape + uniqueness, resolvable predecessors (**error**), an acyclic graph
(**error**), existing SR-refs (**warn**, draft SRs are legit); wired as a
**built-in `trajectory` `check.py` step** ({G2,G3}, process layer) that skips
vacuously on an absent/placeholder-only registry and honors a `docs/trajectory-check:
off` opt-out; `bootstrap.py` MAPPING + docstring (ships the template + script);
`tests/test_bootstrap.py` file-list; `tests/test_trajectory.py` (13 cases: absent
+ placeholder vacuous, opt-out silences, valid DAG, two-node cycle, self-loop,
unresolved predecessor, duplicate/malformed id, SR-ref warn/quiet, messy rows).
Regenerated `docs/architecture.md` (the new script joined the meta-repo symbol
map). **Decisions taken** (the spec left them open — "decide by size"): **(1)** a
standalone `check_trajectory.py` in the `check_*` validator family, *not* growing
`gen_trajectory.py --check` now — Phase 2's renderer reuses its validation, so each
phase ships a whole artifact rather than a half-built generator; **(2)** a
**built-in `check.py` step**, *not* a `[step:trajectory]` in the `stack.ini`
template — this is a kit opt-out *layer* (the `docs/secrets-scan` posture), so it
ships identically everywhere via take-wholesale `check.py`, never a per-repo profile
line. **No deviations** from the spec's validation semantics. **Byte budgets:**
untouched (no `AGENTS.template.md` / `PROCESS.md` edits — the PROCESS_OPTIONS
section is Phase 3). **Gates:** `pytest -q` **384 passed, 2 skipped**;
`check_docs.py --root . --stale` clean; `check_trajectory.py` 98% covered (only the
shared `_utf8_console` reconfigure guard uncovered); the meta-repo (G3, no
`work-items.csv` yet) passes the new step vacuously; `check.py --list --gate G3`
shows `trajectory` at [G2,G3]. **Next: Phase 2** (the offline SVG dashboard).

**Phase 2 landed 2026-07-07 (this session).** The fully-offline dashboard.
**Deliverables:** `scripts/gen_trajectory.py` renders `docs/trajectory.html` from
the WI registry + the `SN->SR->LLR->TC` spine, **reusing `check_trajectory.py`'s
load + validation** (one home for the rules — a sibling import; both ship
together). Two **plain-SVG** views, **no CDN / no JS layout library** (ruling A):
(1) the spine **icicle** ported ~as-is from gilbert; (2) a **layered work-item DAG
computed in Python** — longest-path ranking → deterministic barycentre
crossing-reduction → coordinate assignment → SVG, with a few lines of inline
vanilla JS wiring hover/click. Plus a vision header (the README `PROJECT-VISION:`
tag), definition/execution %-meters, and SN/SR/LLR/TC/WI/track tiles. `--check` is
a **freshness contract** (regenerate-in-memory + byte-compare, like `gen_arch_map
--check`), wired as a new **`trajectory-map` process step at {G3}** beside
`arch-map`; **vacuous** on an absent/placeholder-only registry and silent under the
opt-out toggle. `bootstrap.py` MAPPING + docstring ship the script; `test_bootstrap`
file-list; `tests/test_gen_trajectory.py` (10 cases); regenerated
`docs/architecture.md` (the new script joined the symbol map). **Decision:** kept
**two steps** — validation (`trajectory`, {G2,G3}) separate from freshness
(`trajectory-map`, {G3}), mirroring the `traceability` (registry) vs `arch-map`
(generated view) split, so the churny freshness check doesn't gate at G2. **No
deviations.** **Verified beyond the unit tests:** byte-identical across re-runs
(determinism → stable `--check`); the diamond DAG lays out with correct dependency
ranks + zero node overlaps; adversarial registry text (`</script>`, quotes,
unicode) is HTML/JSON-escaped — no `<script>` breakout, every embedded JSON blob
parses; 0 external references in the output. **Byte budgets:** untouched (the
PROCESS_OPTIONS section is Phase 3). **Gates:** `pytest -q` **393 passed, 2
skipped**; `check_docs --stale` clean; ruff format+lint clean; `gen_trajectory.py`
98% covered; the meta-repo passes `trajectory-map` vacuously. **Next: Phase 3**
(PROCESS_OPTIONS "Trajectory / work-items layer" section + README kit-contents /
scaffold surface).

**Phase 3 landed 2026-07-07 (this session).** Process + docs — the layer is now
documented and discoverable. **Deliverables:** a new **PROCESS_OPTIONS.md
"Trajectory / work-items layer"** section (placed in the §7 harness cluster after
"Skills layer", with an *applies-when*): what a work item is, the
`queued→active→done` lifecycle, how it complements the spine's *what* with the
execution *how* (a WI is to an SR what a build step is to a spec; the two coexist —
the CSV doesn't replace the prose), the registry schema, the two gate steps
(validation + freshness), the offline-SVG render, and the opt-out/vacuous contract.
The **STATUS.template.md** "Work items?" convention bullet (mirrors the "Parallel
tracks?" opt-in line — the Next action names the next `WI-###`(s)). **README**
kit-contents: three rows in `project-trajectory/README.md`
(`work-items.template.csv`, `check_trajectory.py`, `gen_trajectory.py`) + the root
`README.md` runnable-scripts entry. **Byte budget respected:** `PROCESS.md`
(56,375 B) and `AGENTS.template.md` (9,976 B) **byte-for-byte unchanged** — no edit
needed: §7 already links to `process-options.md` generally, and the section follows
the "Parallel tracks" precedent (a process-options layer not separately named in
PROCESS.md). SSOT held — the detail lives once in PROCESS_OPTIONS; the
READMEs/STATUS point at it, never restate it. **Docs-only** — no script/behavior
change, so arch-map + ruff were untouched. **No deviations.** **Gates:** `pytest -q`
**393 passed, 2 skipped**; `check_docs --stale` clean (73 links, 0 broken — the two
new README links resolve; the README-churn hints clear on commit); byte budgets
flat. **Next: Phase 4** (dogfood — decompose this plan into a real `work-items.csv`
by track + generate the kit's own dashboard).

**Phase 4 landed 2026-07-08 (this session) — Thread 52 COMPLETE.** The dogfood:
the kit now runs its own trajectory layer on real data. **Deliverables:**
`docs/requirements/work-items.csv` — **37 work items** mapping the kit's landed
history into a real DAG across four tracks (`scripts`, `docs`, `unattended`,
`self-adoption`), covering **all 36 SRs** (every SR delivered by a WI, none
dangling), with `active` = the trajectory P4 dogfood (this work) and `queued` =
the deferred/backlog threads (48/49/51/53). Generated the kit's own
`docs/trajectory.html` (≈114 KB, fully offline): the icicle shows the real spine
(22 SN / 36 SR / 33 LLR / 36 TC), the DAG lays out **37 nodes across 10 dependency
ranks** (foundation → frontier) with **zero node overlaps**; **Execution 86 %**
(32/37 done), **Definition 100 %** (36/36 SRs Verified). **Mapping approach**
(ruling C, "map, don't renumber blindly"): coherent-deliverable granularity — one
WI per thread or tight cluster, each naming its source thread(s)/`WI-1.x` in the
Deliverable column — rather than a 1:1 blow-up of all 54 threads + 42 `WI-1.x`
(~96 arbitrary nodes); the CSV is the machine-readable execution registry that
**coexists** with the prose plan (an SR row vs the thread that argued it). **Gate
now green on REAL data:** `trajectory` (validation) + `trajectory-map` (freshness)
were vacuous before — they now validate the 37-WI registry and byte-check the
committed dashboard. `trace.py` unaffected (WI is off-spine, SN=22 SR=36 LLR=33
TC=36 orphans=0); `check_docs` does not touch the `.html`; arch-map + ruff untouched
(no script change). `CLAUDE.md` repo-map now names the self-adopted
`work-items.csv` + `trajectory.html`. **No deviations** from the spec; the mapping
granularity is a documented **first honest pass**, open to owner refinement.
**Verified:** deterministic (byte-identical regen → stable `--check`); every DAG
edge resolves; the full spine renders in the icicle. **Gates:** `pytest -q`
**393 passed, 2 skipped**; `check_docs --stale` clean; `check_trajectory` +
`gen_trajectory --check` green on the meta-repo. **Thread 52 done** — the
trajectory/work-items layer ships and the kit demonstrates it on itself.

**Source (reference implementation).** Built and proven downstream in the
**gilbert** repo (a kit adopter, synced to kit-version `767487c`): its WB19 thread
`docs/whiteboard/19-trajectory-work-items.md` and `scripts/gen_trajectory.py`
(719 lines, stdlib-only) → `docs/trajectory.html`. gilbert flagged **D19-6
"upstream"** as open; this thread is that upstreaming. The repo is on the owner's
machine at `c:\Projects\gilbert` — consult it as the reference, but **adapt to
current kit conventions** (arg style, `rel()`/`blank_fenced` helpers, `--check`
exit semantics); gilbert is `767487c`-old, so diff, don't copy verbatim.

**The gap it fills.** The spine answers *what must be true* (SN→SR→LLR→TC). No kit
artifact carries **execution "how"** — cross-track order, which deliverable gates
which, where tracks meet, %-complete. A **work item** (`WI-###`) decomposes how
work executes: it delivers SR(s), sits on a **track**, depends on **predecessor**
WIs (the DAG edges), and moves `queued→active→done`. The dashboard is a *view*
(text is truth; `trace.py`/`gen_arch_map` idiom) — never a source of truth.

**Phase-0 rulings (Peter, 2026-07-07) — do NOT re-litigate:**
- **(A) DAG render = plain SVG computed in Python.** No Cytoscape/ELK/CDN — the
  kit's offline-render principle forbids cloud-loaded legibility (gilbert's CDN
  version is out). Implement a **layered-DAG layout in stdlib**: topological rank →
  node ordering to reduce edge crossings → coordinate assignment → emit SVG with
  hover/click via a few lines of inline vanilla JS (CSP-safe, no libs). The
  SN→SR→LLR→TC **icicle** view is already plain SVG in gilbert — port ~as-is.
- **(B) Opt-out positioning** (mirrors WI-1.41 README-coverage). On by default; a
  fresh scaffold with only a `-000` placeholder WI is **vacuously clean**; a repo
  that never wants it opts out with a toggle (`docs/trajectory-check: off`, like
  `docs/secrets-scan`). Costs a non-user nothing but ships present.
- **(C) The kit dogfoods it** (Phase 4) — decompose THIS `IMPROVEMENT_PLAN.md`'s
  Threads/`WI-1.x` into a real `docs/requirements/work-items.csv` organized **by
  track**, so the kit's own history demonstrates the DAG. Owner accepts this is a
  deep reshuffle; stage it LAST, once the tooling validates it. Reconcile with the
  existing `WI-1.x`/Thread numbering (map, don't renumber blindly).

**Registry schema** (gilbert's, adopt as-is): `work-items.csv` columns
`WI-ID,Title,Track,SR-Refs,Predecessors,Status,Deliverable`. `Status ∈
{queued,active,done}`; `Predecessors`/`SR-Refs` are `;`-joined id lists;
a `-000` placeholder row ships in the template.

**Validation (`--check`, the Phase-1 core — pure stdlib):** every `Predecessors`
id resolves to a real WI (**error**); the WI graph is **acyclic** (a cycle is an
**error** — a trajectory that depends on itself can't start); every `SR-Refs` id
exists in `system-requirements.csv` (**warn**, draft SRs are legitimate);
`WI-###` id shape + uniqueness (integrity, like `trace.py`).

**Phases (separate commits; end each green — `pytest -q` + `check_docs`):**
1. ✅ **Registry + validation (fully offline, no JS)** — **landed 2026-07-07** (see
   the Phase 1 record above). Ship
   `registries/work-items.template.csv` (+ `bootstrap.py` MAPPING + `test_bootstrap`
   file lists); port the validation half as `gen_trajectory.py --check` (or a
   `check_trajectory.py` — decide by size); wire an **opt-out** gate step
   (`[step:trajectory]` in the `stack.ini` template, or a built-in check.py step)
   that **skips vacuously** on a placeholder-only registry and honors the opt-out
   toggle; `tests/test_trajectory.py` (cycle fails, unresolved predecessor fails,
   dangling SR-ref warns, placeholder-only passes, opt-out silences).
2. ✅ **Offline dashboard** — **landed 2026-07-07** (see the Phase 2 record above).
   Port the SVG **icicle** ~as-is; **build the plain-SVG
   layered DAG** (ruling A); vision header + definition/execution %-meters; one
   self-contained `docs/trajectory.html`. Add a `--check` **freshness** contract
   (regenerate-in-memory + byte-compare, like `gen_arch_map --check`) wired into
   the generated-artifact freshness gate. Tests: deterministic generation; stale
   html trips `--check`.
3. ✅ **Process + docs** — **landed 2026-07-07** (see the Phase 3 record above).
   A PROCESS_OPTIONS "Trajectory / work-items layer" section
   (what a WI is, the lifecycle, how it complements the spine's *what* with *how*,
   the offline-SVG render, the opt-out). `status.md` "points at next work items"
   convention. `README.md` kit-contents bullet + scaffold surface. **Byte budget:**
   keep PROCESS.md flat — detail goes to PROCESS_OPTIONS (§7 already links there).
4. ✅ **Dogfood reshuffle (ruling C)** — **landed 2026-07-08** (see the Phase 4
   record above). Author `docs/requirements/work-items.csv` for
   the kit itself: map landed Threads + `WI-1.x` into `WI-###` rows with tracks
   (e.g. `scripts`, `docs/process`, `self-adoption`, `unattended`) + predecessors +
   SR-refs; generate the kit's own `docs/trajectory.html`; the gate goes green on
   real data. Validates the layer end-to-end and demonstrates the capability.

**Risks / watch-items.**
- **WI-registry vs the kit's existing WI/Thread log** — the subtle one. Decide
  whether `work-items.csv` *replaces* or *coexists with* the prose log; likely
  coexist: the CSV is the machine-readable execution registry, the prose thread
  stays as the "why" (like an SR row vs the thread that argued it).
- **Layered-SVG layout** (Phase 2) is the real build; crossing-reduction is
  heuristic — keep it **deterministic** (stable output, so `--check` is byte-stable;
  sort everything, no clocks/time-hashes). Both SVG views must regenerate identically.
- **Opt-out semantics** must match WI-1.41 exactly (vacuous on placeholder; explicit
  toggle) so a fresh scaffold stays green.

**Done-when.** `work-items.template.csv` ships; the generator validates (acyclic +
refs) and renders a fully-offline `docs/trajectory.html` (SVG icicle + SVG DAG, no
CDN); the opt-out gate step is green on a placeholder scaffold and on the kit's own
migrated registry; PROCESS_OPTIONS documents the layer; PROCESS.md /
AGENTS.template.md byte budgets untouched; `check.py --gate G3` PASS; (Phase 4) the
kit's own plan is represented as `work-items.csv`. **Model tier — high** (new layout
algorithm + shipped-template migration + the dogfood reshuffle).

**Scope guard.** ONLY the trajectory/work-items layer. gilbert's other new scripts
are a SEPARATE triage — `check_dupes.py` is **Thread 53** below; `check_licenses.py`
is a maybe-reference (Python-packaging-specific); `check_caps.py`/`check_dataflows.py`
demonstrate patterns the kit already has (`trace.py` integrity / `gen_arch_map
--check` freshness); `fetch_vendor`/`diag_*`/`live_view` are gilbert-domain
(robotics). None of those are in Thread 52.

---

## Thread 53 — `check_dupes.py`: mechanical anti-duplication for code (upstream gilbert)

**Status: 📋 BACKLOG — surfaced 2026-07-07 (adopter review of gilbert); not yet
scheduled.** The kit **preaches** "one fact, one home — in code too" (the AGENTS
working agreement) but has **no mechanical enforcement** of *code* duplication —
only doc/registry single-sourcing. gilbert's `scripts/check_dupes.py` (stdlib only)
tokenizes sources and flags any window of ≥ `MIN_TOKENS` significant tokens
appearing at >1 location (comments/blank/indentation excluded; exact-token, so fast
+ deterministic; renamed-identifier near-dupes are out of scope).

**Why it fits the kit.** Generic, stdlib-only, stack-adaptable (the tokenizer is
per-language — Python reference, "swap for your stack" like the rest of the
harness), and it closes a real gap between what the kit preaches and what it
mechanically checks. **Proposal (to be ruled):** ship as an **opt-in** reference
`[step:dupes]` at G2+ with a tunable `MIN_TOKENS` and a per-repo allowlist for
legitimate repetition; adapt gilbert's implementation to kit conventions; tests.
**Not bundled with Thread 52** (different concern). **Model tier — mid** (the
detector exists; the ruling is threshold/allowlist policy + stack-agnostic framing).

---

## 2026-07-04 batch — decision briefs (all ruled by the owner 2026-07-04)

**Rulings (owner, 2026-07-04).** The briefs below are kept as the *why*; each
thread's Status line carries the operative form:

- **Q1 ★** full `docs/stack.ini` profile. **Q2 ★** INI. **Q3 ★** file-level
  fallback only (symbol-level ports stay contributions). **Q4 ★** level names
  + all four fixed points confirmed.
- **Q5 ★** G2-close, fixed — plus prose noting an adopting repo *may*
  relocate it by modifying its own copy (the deviation-register pattern); the
  kit itself does not parameterize it.
- **Q6 → Hybrid** (overrides the ★): post-ratification questions route by
  revert-cost — LOW = decide + record in the Decisions log; MEDIUM/HIGH =
  Blocked register. Owner's reasoning: one-ratification's whole value is
  momentum; the ratifier accepted bounded risk, and "grind vs pause" is
  exactly what the revert-cost dial encodes.
- **Q7a/b/c ★. Q7d → amended:** no flat refusal — the loop runs under
  *every* gate policy and stops on a new **`NEEDS-HUMAN`** run-state the
  driver writes when progress requires a human act, *after* stating the ask
  as status.md `Needs <human>` bullets (interrupt-and-report, never
  infer-and-continue; a wrong DONE stays a false green). Thread 33
  re-specced.
- **Q8 → Full conditional templating** (overrides the ★), under the owner's
  §N-constancy caveat: the master templates hold **all permutations**;
  omission never renumbers (§ labels are literal text); omitted sections
  leave resolvable one-line stubs; re-sync regenerates from a recorded
  `docs/kit-profile`; the existing-adopter migration risk is accepted.
  Thread 34 re-specced (now a solo build — Session S).
- **Q9 ★. Q10 ★. Q11 ★. Q12 ★** (fail-closed residue confirmed).
- **Q13a ★ + nuance:** sync ≠ stop — landing never waits for a human push;
  under autonomous gates the loop rolls straight into the next leg, and the
  run pauses only on `NEEDS-HUMAN`. **Q13b ★** `llm/{branch}`. **Q13c ★ as a
  default vocabulary, not a restriction** — the type list is exemplary,
  extensible per project, never linted. **Q13d ★.**

### Q1 — How far to take the stack profile *(Thread 30)*

**Decides:** whether the product toolchain (format/lint/test commands, tier
mapping, src/tests paths) becomes a single declared file. Today it is encoded
in ~6 places (`check.py`, `setup.sh`, `setup.ps1`, `ci/check.yml`,
`hooks/pre-commit`, `pytest.ini`); a stack swap must find and rewire all of
them, and the copies drift apart silently.

- ★ **Full profile (`docs/stack.ini`)** — *gain:* a stack swap becomes editing
  one file; CI/hook/harness can never drift; bootstrap can seed the profile
  per `--stack` (a `node` scaffold starts with vitest-shaped commands);
  Thread 34's rewiring checklist gets one target to name. *Downstream feel:*
  declare your commands once, everything reads them. *cost:* a new scaffolded
  file + parsing code the kit maintains forever; one indirection when
  debugging a failing step; INI values are strings (multi-line commands need
  care).
- **Phase 1 only (CI + pre-commit delegate to `check.py`; no new file)** —
  *gain:* cheap; kills the worst drift (CI's copy vs the harness). *cost:* a
  stack swap still touches ~4 EDIT sites; tier mapping stays pytest-shaped
  (A3 unresolved); nothing for bootstrap to tailor.
- **Status quo (EDIT markers in each file)** — *gain:* zero work; commands
  stay visible in the file that runs them. *cost:* the field report's
  #2-ranked adoption pain persists for every non-Python repo.

### Q2 — Profile file format *(Thread 30; moot if Q1 = status quo)*

- ★ **INI (`configparser`)** — *gain:* stdlib on 3.8+; **comments allowed**,
  so the profile self-documents the way the EDIT blocks it replaces do;
  forgiving to hand-edit. *cost:* everything is a string and complex quoting
  is awkward — acceptable here, since the values *are* shell commands.
- **JSON** — *gain:* precise; trivially machine-written. *cost:* no comments,
  which kills the guided-EDIT-surface quality; quoting/trailing-comma
  foot-guns for humans.
- **TOML — rejected up front:** `tomllib` is Python 3.11+ (breaks the kit's
  3.8 floor) and write support isn't stdlib at all; a hand-rolled parser
  violates edit-conservatively.

### Q3 — Non-Python architecture map *(Thread 31)*

**Decides:** what a non-Python repo runs so the committed code map stays
freshness-gated instead of dropped. (Finance-Auditor dropped it — losing the
exact anti-drift lever the kit prizes — because drop was the only option.)

**Why this one script is stack-coupled at all (owner asked 2026-07-04):**
the process layer *does* stay stdlib Python on every adopter — trace /
check_docs / flows read **kit-owned artifacts** (CSVs, Markdown), which are
stack-neutral, and they survived a full stack swap byte-for-byte.
`gen_arch_map.py` is the one process script whose **input is the product's
source code**: it parses `src/` with Python's `ast` module, which can only
read *Python*. On a TS repo the script runs fine, sees zero parseable files,
and fills an empty map that is "fresh" forever (the Thread-25 vacuous pass).
The implementation language was never the issue — the *parseable* language
is. Symbol-level parsing of language X needs a parser from X's own ecosystem
(the FileBackup ps1 port is written *in* PowerShell for the same reason);
option (b) instead keeps the script Python forever by reading what any
language can supply — the file tree + a summary-comment convention.

- ★ **Stdlib file-level fallback (`gen_arch_map.py --mode files`)** — *gain:*
  works for every stack forever with zero new runtimes; testable in the kit's
  own suite; the drift gate stays real (file added/removed/renamed or a
  summary line changed ⇒ stale map ⇒ blocked commit). *Downstream feel:* keep
  the arch-map step, change one flag. *cost:* coarser — per-file rows, no
  symbols or dependency edges; summaries rely on a first-comment-line
  convention the team must adopt.
- **JS/TS port now (`gen_arch_map.reference.mjs`)** — *gain:* symbol-level
  parity for the most common web stack. *cost:* a second-language codebase to
  maintain; kit CI can't exercise it without node; helps only JS/TS — Go,
  Rust, etc. still have nothing without the fallback.
- **Both** — *gain:* universal floor + best-in-class for node. *cost:* most
  work now, and the `.mjs` risks rotting untested until a real node adopter
  exercises it (cheaper to accept as a contribution then).

### Q4 — Automation-level names + the fixed points *(Thread 32)*

**Decides:** the vocabulary the policy file, the prose, and the bootstrap
prompt all use — and whether the non-negotiables are the right set.

- ★ **`attended` / `single-ratify` / `autonomous`** — *gain:* self-describing
  single words that read naturally both in prose and as a one-word
  `docs/gate-policy` value; named by *how much human attention*, not by
  mechanism, so the set can grow. *cost:* new vocabulary to define (once, in
  §4).
- **Acceptor-named (`human-gates` / `batch-ratify` / `llm-gates`)** — *gain:*
  says who signs directly. *cost:* bakes the mechanism into the name
  (`llm-gates` mislabels any future variant); clumsier in prose.
- **Fixed points to confirm (hold at *every* level):** G-Final is the
  human's · no un-run greens · the harness is never waived by LLM judgment ·
  ratified owner decisions are never re-decided by an agent. These are NHW's
  ratified floor; removing any one makes the policy unauditable — flag if you
  want a different set.

### Q5 — Where `single-ratify` ratifies *(Thread 32)*

**Decides:** the one point where the human reviews the accumulated question
list + gate evidence before the agent runs free.

- ★ **Fixed at G2 close** — *gain:* every requirement + design ambiguity
  lands in one sitting, reviewed as cheap artifacts (registries and docs, not
  code); the expensive autonomous stretch (G3 implementation) starts fully
  specced; simplest to document and teach. *Downstream feel:* one calendar
  block of reading, then walk away. *cost:* questions arising during G3 get
  no second batch (they route per Q6); a wrong design runs to completion
  before you see it (mitigated by the LLM-gates + the harness).
- **Configurable (`ratify-at: G1|G2|G3`)** — *gain:* per-project flexibility.
  *cost:* more states to document and test; adds back a setup decision the
  level exists to remove.
- **G1 close** — *gain:* earliest human touch. *cost:* design (G2), where the
  consequential decisions live, would run unratified — largely defeats the
  review's purpose.

### Q6 — Post-ratification human questions under `single-ratify` *(Thread 32)*

**Decides:** what happens when a genuinely human-shaped question appears
*after* the one ratification sitting.

- ★ **Blocked register** — *gain:* pause-free, so the level's promise holds;
  NHW-proven; every block surfaces prominently in the end-of-run report;
  honest — human calls wait for the human. *cost:* work depending on a
  blocked item stalls to run-end; the deliverable may arrive partial
  (honestly labeled, never silently).
- **Decide + record (NHW full-autonomous style)** — *gain:* maximum
  throughput, fewest leftovers. *cost:* erodes the level's contract — the
  human ratified a specific list, then decisions were made beyond it.
- **Hybrid (decide+record LOW revert-cost; Block MEDIUM/HIGH)** — *gain:*
  throughput with bounded exposure. *cost:* the revert-cost judgment is the
  agent's own; requires the Decisions-log discipline anyway.

### Q7 — The resume launcher: four calls *(Thread 33)*

**(a) When is it scaffolded?**
- ★ **Always, inert** (like `run.*`: an empty `AGENT_CMD` prints guidance and
  exits nonzero) — *gain:* discoverable in every repo ("there *is* a resume
  button"); consistent with the launcher precedent; costs nothing unused; any
  agent CLI can fill the slot, so it stays agent-neutral in substance.
  *cost:* one more root file in agent-less repos (deletable); the
  `--agents none` byte-identical-scaffold test gets updated.
- **Only when bootstrap `--agents` chose an agent** — *gain:* agent-less
  scaffolds stay minimal; matches the skills-materialization pattern. *cost:*
  the non-interactive default is `none`, so programmatic scaffolds never get
  it; retrofitting means re-running bootstrap.

**(b) Name**
- ★ **`agent-resume.{cmd,sh,command}`** — matches the kit's lowercase-short
  launcher naming (`run.*`, `onboard.*`) and the AGENTS.md vocabulary.
- **`LLM-Agent-Resume.cmd`** — maximally explicit; casing and "LLM"
  vocabulary inconsistent with every other kit artifact.
- **`resume.*`** — shortest; ambiguous (reads like resuming the *product*).

**(c) The engine**
- ★ **Stdlib Python `scripts/agent_loop.py`** — *gain:* one implementation
  for all platforms; pytest-testable against a fake agent command (stall
  guard, DONE/BLOCKED exits, tier mapping — coverage the ps1 never had); the
  same substrate as every other kit script. *cost:* a real build effort; a
  Python process supervising long CLI sessions must handle per-OS
  console/signal quirks the native ps1 sidesteps.
- **Ship the generalized `trigger.ps1` as a reference** — *gain:* proven
  verbatim, near-zero build. *cost:* Windows-only; untestable in the suite; a
  POSIX twin appears the first time a Linux adopter wants it, and then there
  are two to keep in sync.

**(d) Behavior under an `attended` gate policy**
- ★ **Refuse the loop; boot one interactive session at the right tier** —
  *gain:* a double-click can never bypass the declared policy; still the
  "grind from a single point" entry. *cost:* an unattended run first requires
  flipping `docs/gate-policy` in a reviewed commit — which is the point.
- **Allow with a `--force` flag** — *gain:* convenience. *cost:* the policy
  file stops being authoritative.

### Q8 — The config-over-generation rule *(Thread 34)*

**Decides:** the kit's standing answer to "should Python scripts generate the
artifacts per-repo instead of the agent hand-editing them?"

- ★ **Ownership rule** — kit-owned, re-sync-overwritten files (process docs,
  scripts) are **never** generated per-repo: they read declared config
  (`docs/gate`, `docs/gate-policy`, `docs/stack.ini`). Scaffold-once,
  downstream-owned files (AGENTS.md, README, status.md) **may** be lightly
  generated at bootstrap (placeholders, marker-stripping, file selection).
  *gain:* re-sync stays a clean overwrite + diff (the kit-version stamp keeps
  working); the canonical process doc never forks, so every adopted repo
  reads identically — humans and agents build shared fluency and findings can
  cite a stable §N anywhere; generation eliminates exactly the mechanical
  hand-edits. *cost:* process.md stays generic — a repo reads opt-in sections
  it may not use (mitigated by the applies-when lines + minimum-profile
  header); behavior lives one indirection away in config files.
- **Full conditional templating** (generate per-repo process.md/AGENTS
  variants from profile flags) — *gain:* each repo reads only its own
  process; shorter docs. *cost:* re-sync must re-run generation with the
  recorded parameters or it silently clobbers; the stable-§N shared-reference
  property dies; the kit's test matrix multiplies per flag combination.
- **Status quo (agent hand-edits each adoption)** — *gain:* none beyond zero
  kit work. *cost:* the field report's B-class findings — scattered edits,
  missed duplicated assertions, caught only by independent review.

### Q9 — `Area` column now or later *(Thread 35)*

- ★ **Land now** — *gain:* pre-mass-adoption is the cheap moment (the
  Thread-7 hinge); an optional column forces zero migration (legacy CSVs
  still pass); `trace.py` can report hat coverage; ends each project
  inventing its own 12th column (Finance-Auditor already did). *cost:* one
  more column of width + one more concept in every new scaffold's SR header.
- **Defer** — *gain:* minimal header; gather more field evidence. *cost:*
  adopters keep inventing ad-hoc variants meanwhile (D1 observed exactly
  this), and a later standardization inherits their migrations.

### Q10 — The status/history split: boundary + name *(Thread 36)*

- ★ **Proposed carve** — audit log, Gate Sign-offs records, verdict blocks,
  and the *ratified* Decisions log → `docs/log.md`; Open items, the Blocked
  register, and anything still **awaiting** a human stay in status.md.
  *gain:* status.md is pure "what next" (your rule, verbatim); the unattended
  loop's per-session reload stays cheap at iteration 30; the
  pending-vs-ratified line gives every decision exactly one home. *cost:* two
  files in the session ritual; sign-off history sits one hop from current
  gate state.
- **Keep the Sign-offs table in status.md; move only audit log + notes** —
  *gain:* gate evidence beside gate state (the current reviewer habit).
  *cost:* sign-offs and verdicts are exactly what accretes per gate × phase ×
  review round — the growth the rule targets.
- **Name:** ★ `docs/log.md` (short; pairs with status.md) ·
  `docs/history.md` (self-describing; hints narrative) · `docs/audit-log.md`
  (matches the §6 phrase; longest). Cheap call — pick any.

### Q11 — Commit-identity enforcement posture *(Thread 38)*

**Decides:** how strongly the kit ensures each repo's commits carry the
identity the user chose for it (anonymous vs identified). Today: not at all —
whatever git config resolves is what history gets, and after a push the fix
is a history rewrite.

- ★ **Declared policy + hard guard** — `docs/commit-identity` (default
  `inherit` = no constraint) holds an email pattern; bootstrap asks at repo
  creation; setup applies repo-local git config per clone; the pre-commit
  hook **and** the Thread-33 unattended preflight **block** a mismatch.
  *gain:* the mistake is caught before it exists — the only cheap moment;
  zero cost for repos that don't care. *Downstream feel:* one setup question;
  a fresh clone that forgot gets a clear block + the fix command, not silent
  leakage. *cost:* one more scaffolded file + hook check; the policy is
  repo-wide by design (a pseudonymous repo constrains every contributor).
- **Warn-only** — *gain:* never blocks a commit. *cost:* the warning scrolls
  by unread in exactly the case that matters most (unattended, nobody
  watching) — the 40-wrongly-attributed-commits scenario survives.
- **Prose-only guidance** — *gain:* zero machinery. *cost:* "ensure" becomes
  "remember"; the failure stays silent and near-irreversible.

### Q12 — Privacy-leak review: ★ ruled 2026-07-04 (re-homed structurally); one residue *(Threads 39 → 40)*

**Owner ruling:** not per-commit (confirmed — too painful); the
push-boundary *direction* was right, but hooks are per-clone and
tool-circumventable — a user pushing with a different tool may never hit
them, and the agent should not be the pusher by default anyway. So the
review's primary home moves to **Thread 40's sync ritual**: the agent
iterates on its own branch; a scrub agent rewrites PII out of the *history*
(diffs, messages, iteration logs) before anything reaches the development
branch; the human pushes a branch that never contained the leak. This closes
the add-then-strip hole structurally. Unchanged: the per-commit
deterministic lint + the gate/CI sweep; the pre-push hook ships as an
optional backstop with its limits stated.

**Residue to confirm:** when the scrub/review agent *can't run* at a sync
point on an anonymous repo — ★ **fail-closed** (the sync waits; nothing
lands on the pushable branch unscrubbed; missing tool ≠ pass at the one
boundary that matters) vs **fail-open with warning** (never blocks, but the
warning scrolls by in exactly the unattended case).

> _Refined 2026-07-05 (WI-1.30, owner ruling): fail-closed stays the default,
> but the pre-push **hook** (not the sync ritual) gains a **declared opt-down**
> — `docs/privacy-review: warn-unwired` — for the adopted-but-not-wired-yet
> window. Rationale: under `push-policy: human` the hook's warning reaches a
> human at a terminal, so the "scrolls by unattended" concern doesn't apply to
> this surface; the opt-down is tracked repo text, softens only the unwired
> case, and the deterministic lint stays the blocking floor._

### Q13 — The iteration-branch protocol: four calls *(Thread 40)*

**(a) Push authority default**
- ★ **`human`** — the agent **never pushes, even if asked mid-session**; it
  prepares the branch and requests. *gain:* publication is a deliberate
  human act, immune to hook/tool circumvention by construction (your stated
  preference). *cost:* the human is the bottleneck for every publish —
  cheap, since pushing is rare and takes seconds.
- **`agent-iteration`** — the agent may push only the *scrubbed iteration
  branch* (remote backup + visibility); the dev branch stays human-pushed.
- **`agent`** — full delegation (the NHW walk-away shape), still gated by
  the sync ritual.

**(b) Iteration-branch name**
- **`{branch}_LLM_Iteration`** (your proposal) — explicit and
  self-describing in a flat branch list.
- ★ **`llm/{branch}`** — slash namespacing groups every agent branch under
  one prefix in git tooling/UIs (the conventional shape); otherwise
  identical. Pure taste — your suffix stands if you prefer it visible
  without grouping.

**(c) Collated-commit vocabulary**
- ★ **Conventional Commits with optional scope** (`feat(addon):` /
  `fix(biome):` / `perf(noise):` / `docs:` / `build:` — verified as exactly
  your Terra history's shape) — *gain:* why-and-impact at a glance;
  de-facto standard; machine-parseable for changelogs later. *cost:* one
  more convention to state (a line in the sync step).
- **Free-form subject collation** — nothing to learn; loses the at-a-glance
  category and changelog parseability.

**(d) Iteration logs (your item 2) — tracked how much?**
- ★ **Tracked, size-bounded logs + a generated index** —
  `docs/iteration/NNN-<stamp>.log` (head + capped tail per session; cap
  pinned in-thread) + `docs/iteration_index.md` regenerated per iteration
  (session, date, model/tier, phase, outcome, commit range, link). *gain:*
  forensic detail survives machine death and travels with the repo; the
  index answers "which session did this" at a glance; anonymous repos stay
  safe because the logs ride the iteration branch through the scrub.
  *cost:* repo weight grows per session (bounded); one more scrub surface.
- **Gitignored raw logs (the NHW status quo)** — zero repo weight; detail
  dies with the machine and there is nothing durable to index.
- **Track full unbounded transcripts** — maximal forensics; a 40-iteration
  run can add tens of MB, compounding per leg.

**Proposed sessions (rulings landed 2026-07-04).**
**▶ ALL PLANNED SESSIONS (L–S) LANDED** (2026-07-04). No ▶ NEXT session —
per Session-protocol step 0, don't invent one; confirm with the owner before
starting new work. Remaining open items are the **stubs** (Thread 16
non-code-artifact verification · Thread 21 cross-repo tooling · Thread 23
publication composition), each needing a decision to revive.
- **Session L ✅ landed 2026-07-04** — Threads **29 + 35 + 37 + 38**
  (mechanical, file-coherent batch: check.py guard + registry column + the
  vision tag + the commit-identity guard; per-thread Status blocks above).
  Gates: `pytest -q` **183 passed, 1 skipped** (pre-existing, outside the
  touched files); `check_docs --root .` **0 broken**. Byte deltas:
  AGENTS.template.md 9,990 → 9,990 (untouched); PROCESS.md 52,064 → 52,305
  (**+241 B** — the Thread 37 G1 vision criterion, ~2 sentences, flagged per
  the budget convention). *Thread 34 moved out — the Q8 ruling made it a
  solo build (Session S).*
- **Session M ✅ landed 2026-07-04** — Threads **36 + 32** (the status/log
  split, then the gate-authority levels writing to the moved record home;
  per-thread Status blocks above). Gates: `pytest -q` **189 passed, 1
  skipped** (the same pre-existing skip); `check_docs --root .` **0 broken**.
  Byte deltas: AGENTS.template.md 9,990 → 9,998 (Thread 32's gates-bullet
  edit, funded by trims); PROCESS.md 52,305 → 53,681 (**+1,376 B** across the
  two threads, flagged per-thread above).
- **Session R ✅ landed 2026-07-04** — Thread **40** solo (the iteration
  branch & sync protocol: PROCESS_OPTIONS layer + `docs/push-policy` +
  the cross-doc wiring; Status block above). Gates: `pytest -q` **194
  passed, 1 skipped** (the same pre-existing skip); `check_docs --root .`
  **0 broken**. Byte deltas: AGENTS.template.md 9,998 → 9,998 (the
  push-policy session-bullet clause, funded by two trims); PROCESS.md
  53,681 → 54,442 (**+761 B** — the §3 collated-cadence and §7
  push-authority pointers, flagged per the budget convention).
- **Session P ✅ landed 2026-07-04** — Thread **33** solo (the unattended
  coordinator: PROCESS_OPTIONS layer + `agent_loop.py` engine + root
  `agent-resume.*` launchers + iteration logs/index; Status block above).
  Gates: `pytest -q` **211 passed, 1 skipped** (the same pre-existing skip);
  `check_docs --root .` **0 broken**. Byte deltas: AGENTS.template.md
  9,998 → 9,998 (untouched); PROCESS.md 54,442 → 54,669 (**+227 B** — the §4
  unattended-operation pointer, flagged per the budget convention).
- **Session Q ✅ landed 2026-07-04** — Thread **39** solo (the privacy lint +
  the push-boundary review backstop: `check_privacy.py`, pre-commit/check.py
  wiring, `hooks/pre-push` + `REVIEW_CMD`; Status block above). Gates:
  `pytest -q` **231 passed, 1 skipped** (the same pre-existing skip);
  `check_docs --root .` **0 broken**. Byte deltas: AGENTS.template.md
  9,998 → 9,998 (untouched); PROCESS.md 54,669 → 54,669 (untouched — the
  whole layer lives in PROCESS_OPTIONS/ADOPTING, per the budget convention).
- **Session S ✅ landed 2026-07-04** — Thread **34** solo (the conditional
  scaffold generator: kit-only/profile markers across the masters +
  `docs/kit-profile` + `--stack node` gating + resync regeneration + the
  8-permutation matrix; Status block above). Gates: `pytest -q` **252
  passed, 1 skipped** (the same pre-existing skip); `check_docs --root .`
  **0 broken**. Byte deltas: AGENTS.template.md 9,998 → 9,998 (the kit-only
  wrap funded by three trims; the *generated* AGENTS.md sheds ~110 B
  downstream); PROCESS.md 54,669 → 54,961 (**+292 B** — the kit-only header
  block + four profile marker lines, all stripped from every scaffold;
  flagged per the budget convention).
- **Session N ✅ landed 2026-07-04** — Thread **30** solo (the stack profile:
  `stack.ini.template` → `docs/stack.ini` + check.py profile reader +
  `--run-step` hook delegation + CI/setup/§7 repointing; per-thread Status
  block above). Gates: `pytest -q` **264 passed, 1 skipped** (the same
  pre-existing skip); `check_docs --root .` **0 broken**. Byte deltas:
  AGENTS.template.md 9,998 → 9,998 (untouched); PROCESS.md 54,961 → 55,123
  (**+162 B** — the §7 profile pointer, flagged per the budget convention).
- **Session O ✅ landed 2026-07-04** — Thread **31** solo (the stack-neutral
  arch-map fallback: `gen_arch_map.py --mode files` + `--comment-prefix`,
  ADOPTING.md's third port-or-drop option; per-thread Status block above).
  Gates: `pytest -q` **271 passed, 1 skipped** (the same pre-existing skip; +19
  vs Session N's 252/1 — 8 new files-mode tests plus the run re-counts all).
  `check_docs --root .` **0 broken**. Byte deltas: AGENTS.template.md
  9,998 → 9,998 (untouched); PROCESS.md 55,123 → 55,123 (untouched — the whole
  change lives in the script + ADOPTING.md, per the budget convention).
- **Session R** — Thread **40** solo, strong model (after M, before P and Q;
  the branch/sync protocol design — PROCESS_OPTIONS layer + push-policy file;
  P and Q build against it). *Reference material (summarized in the spec;
  consult for ground truth):* `C:\Projects\NotHomeWrecker\docs\llm-gate-policy.md`.
- **Session P** — Thread **33** solo, strong model (after M and R; the
  coordinator engine + root launchers + protocol layer — a new-script build).
  *Reference material:* `C:\Projects\NotHomeWrecker\trigger.ps1` +
  `docs\kickoff.md` "Unattended mode" (the field-proven loop the engine ports).
- **Session Q** — Thread **39** (after L, M, and R; the privacy lint + hook
  backstop — a new-script build with fake-reviewer tests; the scrub-agent
  half is Thread 40 protocol, not script).
- **Session S** — Thread **34** solo, strong model (after M; the conditional
  scaffold generator: profile markers across every template +
  `docs/kit-profile` + resync regeneration + the per-permutation test
  matrix — the widest build of the batch).

---

## Sequencing & session strategy

**Landed:** **0a ✅**, **0b ✅**, **1 ✅**, **2 ✅**, **3 ✅** (2026-06-28),
**7 ✅**, **4 ✅**, **6 ✅**, **8 ✅**, **5 ✅**, **10 ✅**, **9 ✅**, **11 ✅**
(2026-06-29); **12 ✅, 13 ✅, 15A ✅, 17 ✅, 18 ✅** (2026-06-30, Session E);
**14 ✅** (2026-06-30, Session F); **15 B/C/D ✅** (2026-06-30, Session G);
**19 ✅** (2026-06-30, Session H); **20 ✅** (2026-06-30, Session I);
**24 ✅, 25 ✅, 26 ✅, 22 ✅** (2026-07-01, Session J); **27 ✅, 28 ✅**
(2026-07-01, Session K). **All 28 threads complete.**
**Reopened 2026-07-04** with **Threads 29–40** (the downstream-adoption field
report + the NotHomeWrecker unattended-coordinator review + owner directives) —
specs above. **29 ✅, 35 ✅, 37 ✅, 38 ✅** (2026-07-04, Session L);
**36 ✅, 32 ✅** (2026-07-04, Session M); **40 ✅** (2026-07-04, Session R);
**33 ✅** (2026-07-04, Session P); **39 ✅** (2026-07-04, Session Q);
**34 ✅** (2026-07-04, Session S); **30 ✅** (2026-07-04, Session N);
**31 ✅** (2026-07-04, Session O). **All 12 threads (29–40) complete —
Sessions L–S all landed.**
**All questions ruled by the owner 2026-07-04** — the batch's decision-briefs
section records the rulings (Q6 Hybrid and Q8 full-conditional-templating
override the recommendations; Q7d/Q13a amended Threads 33/40). Remaining open
items: the **stubs** (16, 21, 23 — each needs a decision to revive).
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

> **WI-1.18 ✅ landed 2026-07-03 · AC advisory: "byte-identical"/"bit-identical"
> are self-pinning.** Real false positives from Gilbert (the WI-1.16 advisory's
> first downstream contact): three SRs were flagged although their comparatives
> name their predicate — "topic names and schema references are byte-identical",
> "two consecutive runs produce byte-identical files", "two export runs produce
> byte-identical STL files". "byte-identical"/"bit-identical" state the
> comparison basis (raw bytes/bits), exactly like the already-recognized
> "byte-for-byte"/"bit-for-bit" markers. Fix, tests-first:
> 1. **`trace.py`** — `byte-identical` + `bit-identical` added to
>    `PREDICATE_MARKERS` (existing heuristic structure unchanged: a cell
>    containing them is treated as pinned), with a comment naming the
>    self-pinning rationale; the module docstring's marker enumeration updated.
> 2. **`PROCESS.md` §4 untouched** — its advisory paragraph enumerates the
>    *comparative terms*, not the pinning markers, so there is no second marker
>    list to reconcile (single source: the code).
> 3. **Tests (3 new, red-first, `tests/test_ac_advisory.py`):**
>    "byte-identical" cell → no advisory; "bit-identical" cell → no advisory;
>    bare "identical" still warns (guards WI-1.16's behavior).
>
> **Byte deltas:** `PROCESS.md` **untouched (52,064)**; `AGENTS.template.md`
> **untouched (9,990/10,000)**. `pytest -q`: **174 passed, 1 skipped** (was
> 171/1; +3). `check_docs --root .`: OK, 0 broken.

> _WI-1.19–1.23 below are one 2026-07-04 post-plan batch, built and
> gate-checked in a single session and committed after owner review
> (status.md OI-1, closed) as four logical commits — 1.20/1.21 share one
> (same files, same review)._

> **WI-1.19 ✅ landed 2026-07-04 · Root cleanup + `docs/archive/` + root-README
> refresh.** Owner-raised: root carried dead working files and the README
> lagged the Thread 29–40 landings. Moved `TEMPLATE_REVIEW.md`,
> `kit-adoption-field-report.md`, `scratch.md` → `docs/archive/` (with an
> index README; all references updated — plan header, Thread 15,
> `session-protocol` skill kit + dogfooded copies; archive linked from
> CLAUDE.md's repo map so `check_docs` sees it reachable). Root README gained
> `check_flows.py`/`check_privacy.py` in the scripts bullet, an **Unattended
> agent operation** headline bullet, a skills+hooks bullet, and the quick
> start now names the `run.*`/`agent-resume.*` launchers + policy files.

> **WI-1.20 ✅ landed 2026-07-04 · Locale-tolerant rate-limit backoff.**
> Owner-raised: `seconds_until_reset` only understood am/pm clocks — 24-hour
> regions would exit WAITING on every throttle. `agent_loop.py` now parses
> both clock conventions (`3:45pm` / `14:30` / `Tue 09:00`, bounds-checked),
> and a new `--limit-retry-fallback N` (default 3600) sleeps-and-retries on an
> *unrecognized* reset wording instead of exiting — only when
> `--wait-on-limit` is set (waiting stays consent-gated) and capped at that
> ceiling. Tests: clock-format unit sweep + an e2e unparseable-throttle
> retry; PROCESS_OPTIONS "Limits are handled reactively" updated.

> **WI-1.21 ✅ landed 2026-07-04 · One parse rule for declared-policy files.**
> Found during the 2026-07-04 duplicate-logic review: four readers of the
> one-word policy files disagreed — `agent_loop.read_declared` took the
> *last* non-comment line, the git hooks and `check_privacy.read_policy` the
> *first*, and `check.py resolve_gate` tolerated no comments at all. Rule
> unified to **first non-empty, non-comment line** (matches the enforcement
> floor): `read_declared` aligned; `resolve_gate` made comment-tolerant.
> Tests: cross-parser agreement fixture (`test_declared_policy_parsers_agree`)
> + a commented-`docs/gate` harness case.

> **WI-1.22 ✅ landed 2026-07-04 · Unattended layer self-applied to this repo.**
> Owner-directed: apply the template to itself so the repo shows its own
> structure. Root `agent-resume.{cmd,sh,command}` wired live for Claude
> (kit seed command, `AGENT_MODEL=opus`, passing `--root .` because the
> engine's script-relative default would resolve to `project-trajectory/`);
> `docs/status.md` blackboard + `gate-policy` (attended), `push-policy`
> (human), `commit-identity` (inherit), `run-state` (RUNNING); `out/`
> gitignored; CLAUDE.md repo map documents it. **Deliberate boundary** (stated
> in status.md Non-goals): no SN→TC registries, no `run.*` launchers, no
> scaffolded `docs/process.md` for the meta-repo.

> **WI-1.23 ✅ landed 2026-07-04 · Working-agreement disciplines from field
> feedback.** Owner-supplied cross-thread feedback triaged: most principles
> already covered (often mechanized — gates, Blocked register, Assumptions,
> decision dial); three genuine gaps adopted. **PROCESS.md §6** gained "Three
> cheap disciplines the dial never relaxes": verify at peak confidence
> (wrong-and-confident is the costliest state), sunk work is not an argument,
> never retry past an unexplained failure (record the rule that would have
> prevented it, §7). **AGENTS.template.md** carries the headlines — the
> uncertainty bullet extended ("distrust certainty"), a new sunk-cost/blind-
> retry bullet, and "ask as one question with a recommended default" — paid
> for by folding "Propose better ways" into stay-in-your-lane and trimming
> redundant comment/style prose (motivation text survives in EXAMPLE.md).
> Not imported (out of kit scope): host-runtime context-frugality mechanics;
> subagent management already lives in §6 tiering.
>
> **Byte deltas:** `AGENTS.template.md` **9,998 → 9,976** (≤10,000; headroom
> grew 2 → 24); `PROCESS.md` **55,123 → 56,230 (+1,107)** — the §6 doctrine
> paragraph is the single-source home the AGENTS bullets cite, per the
> decompose-don't-paraphrase rule. `pytest -q` (whole batch): **259 passed,
> 16 skipped** (was 256/16; +3). `check_docs --root .`: OK, 0 broken.

> **WI-1.24 ✅ landed 2026-07-04 · Readiness polish: opus seed, skill
> baseline, meta-repo resume prompt.** The three small items from the
> post-batch readiness review, owner-approved:
> 1. **`bootstrap.py` Claude seed `sonnet` → `opus`** (comment states the
>    rationale: driver sessions carry gate-bearing judgment, §6 tiering —
>    cheaper phases are `AGENT_MODEL_MAP`'s job, not the loop default);
>    `test_bootstrap` assertion updated.
> 2. **`byte-budget-guard` skill baseline re-stamped** (kit + dogfooded
>    copies): PROCESS.md watched baseline ~47,476 → **56,230 as of
>    2026-07-04/WI-1.23**, with an instruction to re-stamp both copies when
>    a flagged growth lands; report-shape example numbers refreshed.
> 3. **Root launchers gain an `AGENT_PROMPT` slot** (meta-repo resume
>    prompt): the engine default assumes a scaffolded downstream repo
>    (`docs/process.md`), so this repo's launchers now name its real
>    surfaces (CLAUDE.md, plan/WI scope rule, pytest+check_docs gates,
>    push-policy) — empty slot falls back to the engine default; explicit
>    flags precede `$@`/`%*` so command-line overrides win. Found + fixed in
>    verification: `agent-resume.cmd`'s working copy was LF-only (Write
>    artifact) and cmd.exe misparsed it — exactly the failure
>    `.gitattributes` documents; normalized to CRLF (committed form was
>    already correct — index normalizes; fresh checkouts were never broken).
>    Both launchers now verified end-to-end via `--help` through the full
>    quoting path.
>
> **Byte deltas:** `AGENTS.template.md` + `PROCESS.md` **untouched**
> (9,976 / 56,230). `pytest -q`: **259 passed, 16 skipped** (assertion
> updated, count unchanged). `check_docs --root .`: OK, 0 broken.

> **WI-1.25 ✅ landed 2026-07-05 · Downstream field report (TS-repo adoption):
> run_step Windows exec bug + arch-map mode wired through stack.ini.** Both
> MODIFIED-FROM-KIT deltas the adopter carried, verified against the kit and
> absorbed upstream:
> 1. **`check.py run_step` executed the unresolved argv** — the guard resolved
>    `cmd[0]` via `shutil.which` (PATHEXT-aware, finds `npx.cmd`), then ran the
>    bare name; Windows `CreateProcess` applies no PATHEXT, so `npx`/`eslint`
>    passed the guard and crashed with WinError 2 — the exact raw
>    `FileNotFoundError` the guard's own comment claims to avoid. The Python
>    reference commands (`{py} -m ruff`) never exercised the path, which is
>    why the suite missed it. Fix: run the resolved path
>    (`subprocess.run([exe] + cmd[1:])`). Regression test runs a bare-name
>    shim through `--run-step` — a real `.cmd` on Windows CI, a shell script
>    on POSIX.
> 2. **Arch-map mode is now declared, not hand-edited:** new
>    `[arch-map] mode = symbols|files` in `docs/stack.ini` (default `symbols`
>    = byte-identical historical plan; invalid values fail loudly), plus
>    optional `comment-prefixes` for the files-mode summary token. `check.py`
>    builds the step from it — the take-wholesale file stays wholesale.
>    `bootstrap.py --stack node|go|rust|powershell` seeds `mode = files`
>    (only on the run that created the profile), and
>    `initialize_generated_docs` honors the seeded mode so generator and
>    checker agree — a fresh non-Python scaffold's freshness gate is real and
>    green on day one, not vacuous-then-stale. `stack.ini.template` documents
>    the section; ADOPTING.md §3 option 2 now points at the profile key
>    instead of a check.py hand-edit.
> Tests: +4 in `test_stack_profile.py` (resolved-path exec, files-mode plan
> + comment-prefixes, invalid-mode loud failure, non-Python seed end-to-end
> through `--run-step arch-map`).

> **WI-1.26 ✅ landed 2026-07-05 · Finance-Auditor re-sync follow-through:
> hook honors the declared arch-map mode; gate-advance skill names the
> declared acceptor.** Inspected the adopter's re-sync to `8dad711` (their
> `check.py` is take-wholesale again, zero deltas). One remaining
> field-reported delta absorbed: **`hooks/pre-commit` hardcoded symbol-mode
> `gen_arch_map.py --check`**, so a files-mode repo had every commit read as
> stale — the hook now delegates to `check.py --run-step arch-map`
> (mirroring its format delegation; their exact local fix), with the
> EDIT marker rewritten for the ported-generator swap. Verified end-to-end:
> a fresh `--stack node` scaffold's hook runs the generator `--mode files`
> and exits 0. Second, their `gate-advance` skill marker exposed a soft kit
> gap: the skill still said "human decision" unconditionally while the kit
> ships declared gate-authority levels (Thread 32) — both copies now name
> the `docs/gate-policy` acceptor (default attended = human). Their other
> markers are local specialization, correctly theirs. Tests: +1
> (`test_hook_arch_map_step_honors_declared_mode` — delegation green in
> files mode where the old hardcoded line reads the same repo as stale).

> **WI-1.27 ⏸ deferred (backlog, raised 2026-07-05) · Coordinator working-tree
> safety on a hard-killed session.** Owner-raised while auditing the unattended
> layer: `agent_loop.py` treats committed repo text as the only memory and
> spawns a fresh session per turn, so there is no chat history to lose — but it
> has **no stash/rollback of the working tree between sessions**. The clean
> rate-limit path is handled (a throttled session returns the reset message →
> `WAITING`, never counted as a stall). The unhandled case is a usage limit (or
> any signal) **hard-killing the CLI mid-edit**, after Write/Edit calls but
> before the driver's "commit your progress before stopping" step runs: the
> partial, uncommitted tree is inherited by the next fresh session. Partial
> mitigations today: the pre-commit gates are a floor against a broken partial
> being committed as a false green, and a well-behaved fresh session *should*
> reconcile a dirty tree (behavioral, not enforced). **Owner decision
> 2026-07-05: deferred — rely on fresh-session reconciliation for now and
> revisit only if pollution is observed in practice.** Sketch if revived:
> snapshot HEAD at session start; on a session that ends with a dirty tree and
> no new commit (a hard-kill signature), either auto-stash the residue to a
> named ref or reset to HEAD, recording the discard in the iteration log so no
> silent work loss. Product-layer-adjacent but coordinator-owned; strong-model
> decision when specced.

> **WI-1.28 ✅ landed 2026-07-05 · Project-specific gate steps declared in
> `docs/stack.ini` (`[step:<name>]`), completing check.py's take-wholesale
> promise.** Third field signal in the WI-1.25/1.26 family (a downstream — Gilbert
> — re-sync flagged this): the Thread-30 profile moved format/lint/test/tiers/
> coverage/arch-map into `docs/stack.ini`, and ADOPTING §6 then declared
> `check.py` take-wholesale — but a repo that added its **own** gates (Gilbert's
> dup-code · license-lint · cap-integrity · dataflow-freshness) had nowhere to
> put them **but** hand-edits inside the take-wholesale script, so the promise was
> only half-true and the docs contradicted each other (ADOPTING said take-
> wholesale; the downstream-resync skill still said "re-apply your EDIT block").
> Fix — make the profile express the *whole* toolchain: `check.py` now reads
> `[step:<name>]` sections (`command` required; `gates` default G3; `layer`
> default product), auto-derives each step's required import from its argv (same
> rule as the built-in product steps), slots them into the plan with the other
> product steps, and validates loudly (empty name · built-in-name shadow · missing
> command · bad gate token · bad layer all `sys.exit`). Gate-scoped via the
> existing `main()` filter; `--run-step <name>` drives one (hook/CLI). Docs
> reconciled: stack.ini.template gains a documented **commented** example (kept
> commented so the reference profile still equals the built-in plan byte-for-
> byte), ADOPTING §2 + §6 and the downstream-resync skill now say custom gates
> live in the profile and `check.py` is take-wholesale, and PROCESS.md §7 names
> the `[step:]` route. **Migration for an existing custom-`check.py` adopter:**
> move each hand-added step into a `[step:]` section once, then take the kit
> `check.py` wholesale forever after. **Deviations from the offer:** none.
> **Byte deltas:** AGENTS.template.md 9976 → 9976 (untouched); PROCESS.md 56,230
> → 56,375 (+145 B, flagged — one clause in the §7 product-checks bullet naming
> the `[step:]` route; baseline re-stamped in both byte-budget-guard skill
> copies). Tests: +7 in `test_stack_profile.py` (plan join + derived requires,
> gate scoping, `--run-step`, and the four loud-failure guards, plus a guard that
> the shipped profile has no active `[step:]`). `pytest -q`: 286 passed, 1
> skipped (was 279 passed pre-WI); `check_docs.py --root .`: OK, 0 broken.

> **WI-1.29 ✅ landed 2026-07-05 · Plan/build cadence: strong-tier PLAN sessions
> write `docs/plan.md`, cheap-tier BUILD sessions execute it, `run-phase` is the
> bounce.** Owner-raised (with the NHW tiny-session commit as field evidence):
> the unattended layer had the §6 tiering *doctrine* (strong plans / cheap
> executes) and the *mechanism* (`run-phase` + `--model-map`) but no named
> convention connecting them — and the engine's default prompt said only "work
> as far as you can," with **no plan artifact downstream at all** (the meta-repo
> dogfoods IMPROVEMENT_PLAN.md; a scaffolded repo had nothing), so each session
> invented its own next step and the safe invention was always a too-small one.
> Landed, per the owner's rulings (plan home = new scaffolded file; implement
> now): **(1)** `PLAN.template.md` → `docs/plan.md` — sequenced blocks (stable
> `B-n` ids, scope, observable done-when, size class, §6 tier hint) + the bounce
> rule + a "notes for the next PLAN session" tail; wired through bootstrap
> `MAPPING`, the docstring tree, README's scaffold list, and a status.template
> pointer (status stays the lean resume surface — names the current block, never
> holds the plan). **(2)** PROCESS_OPTIONS "Unattended operation" gains the
> **Plan/build cadence** subsection: the bounce protocol, the
> `AGENT_MODEL_MAP="PLAN=<strong>,BUILD=<cheap>"` wiring, the sizing heuristics
> (block = one deliverable + tests; deep solo, wide-mechanical solo, cheap prose
> clubbed; too-small = trivial sessions re-paying context reload, too-big =
> timeouts/stalls), and the **sizing servo** — PLAN sessions read the recent
> `iteration_index.md` token/outcome rows before re-chunking, making the
> existing telemetry load-bearing. Also notes the cadence works attended (a
> human alternating tiers is the same protocol). **(3)** `agent_loop.py`
> `DEFAULT_PROMPT` carries the discipline, conditional ("where docs/plan.md
> exists") like the iteration-branch clause — a repo without the surface is
> unchanged. **(4)** Launcher templates seed the model-map example naming
> PLAN/BUILD. **(5)** `docs/plan.md` added to the preserve-always lists
> (ADOPTING §6 + downstream-resync skill, both copies). **Also fixed en route:**
> WI-1.28 updated only the dogfooded `.claude/` copy of the downstream-resync
> skill; the kit-source copy (`project-trajectory/skills/…` — what ships) still
> said "re-apply your EDIT block". Both copies now match. **Deviations:** none.
> **Byte deltas:** AGENTS.template.md 9976 → 9976 (untouched); PROCESS.md 56,375
> → 56,375 (untouched — cadence lives in PROCESS_OPTIONS, the expansion home).
> Tests: +2 (`test_plan_build_cadence_surfaces`,
> `test_default_prompt_carries_the_plan_build_cadence`) + the scaffold file-list
> pin. `pytest -q`: 288 passed, 1 skipped; `check_docs.py --root .`: OK, 0
> broken.
> **Review follow-up (owner, same day):** "will a single session still plan
> *and* implement on small scope?" — mostly yes by design (attended sessions
> never see the cadence prompt; nothing stops a PLAN session after chunking),
> but the prompt's "then set run-phase to BUILD" was readable as a terminal
> act. Tightened in both homes (DEFAULT_PROMPT + the PROCESS_OPTIONS
> subsection): *the bounce governs who plans, not how much one session does* —
> only BUILD→PLAN mandates a stop; a PLAN session rolls straight into the
> first block budget-allowing, so small scope collapses to plan-and-build in
> one session. BUILD's one-block-per-session stays strict deliberately (the
> cheap tier must not self-scope; the servo coarsens instead).

> **WI-1.30 ✅ landed 2026-07-05 · Pre-push privacy review: declared opt-down
> for the unwired-reviewer window (`docs/privacy-review: warn-unwired`).**
> Owner-raised adoption friction: an anonymous repo adopted with the *intent*
> to wire the LLM privacy reviewer later couldn't push at all — the hook
> failed closed on the unwired slot even with the deterministic lint green
> (the Q12 residue ruling, chosen when the concern was warnings scrolling by
> unattended). **Owner ruling 2026-07-05 (AskUserQuestion): declared
> opt-down** — fail-closed stays the default; a repo may track the one-word
> `warn-unwired` in `docs/privacy-review` (same first-line parse as every
> declared-policy file; absent or any other value — including a typo — reads
> as require, the stricter direction). Under the opt-down an *unwired*
> reviewer warns (naming what actually guarded the push) and the push
> proceeds on the deterministic floor. Deliberately narrow: lint findings
> still block, a wired reviewer's BLOCK still blocks, missing Python still
> fails closed (the deterministic layer can't run either). Not scaffolded (an
> optional file, like `docs/run-phase`); the hook's fail-closed message names
> the escape at the moment it fires. Q12-residue note annotated in the
> decision record (the "scrolls by unattended" rationale doesn't apply to
> this surface: under `push-policy: human` the pusher is a human at a
> terminal). Docs: process-options "Commit identity & anonymity" Layer-2
> bullet + the hook header. Tests: +4 (`test_pre_push_hook.py` — opt-down
> warns-and-proceeds, lint floor unsoftened, wired BLOCK unsoftened, typo
> stays fail-closed). `pytest -q`: 292 passed, 1 skipped; `check_docs.py
> --root .`: OK, 0 broken. Byte deltas: AGENTS.template.md / PROCESS.md
> untouched (the knob lives in PROCESS_OPTIONS + the hook).

> **WI-1.31 ✅ landed 2026-07-05 · check_docs guards the README
> `PROJECT-VISION:` tag (Thread 37's mechanizable half).** Owner-raised from
> downstream field reports (2026-07-05): nothing mechanical checked the tag
> *existed* — the needs-registry pointer link protects the `#vision` anchor,
> but delete the tag and the pointer together and no gate fires.
> `check_docs.py` gains a fourth finding class: the root README must state
> the singleton `PROJECT-VISION:` tag **exactly once** — zero (the canonical
> vision statement is missing) or several (a re-authored variant) is a hard
> FAIL; code spans/fences are stripped first (quoting the convention isn't
> stating a vision); no root README at all degrades to WARN so bare doc
> trees stay usable. Runs wherever check_docs runs (check.py's
> doc-navigability step, G1–G3), mechanizing the §4 G1 criterion's
> tag-exists half; the needs-vs-vision consistency review stays human-judged
> (the WI-1.16 honesty stance — no PROCESS.md edit needed, its G1 text
> already reads correctly). Docs: both READMEs' check_docs descriptions.
> Tests: +4 (`test_check_docs.py` — missing tag fails, duplicate fails,
> code-span/fence mention doesn't count, no-README warns not fails).
> `pytest -q`: 296 passed, 1 skipped; `check_docs.py --root .`: OK, 0
> broken. Byte deltas: AGENTS.template.md / PROCESS.md untouched.

> **WI-1.32 ✅ landed 2026-07-05 · Meta-repo dev-setup moved to `scripts/`
> (match the scaffolded layout).** Owner ruling 2026-07-05: this repo's
> layout should track its own kit definition — the dogfooded
> `dev-setup.{sh,ps1}` sat at the repo root while bootstrap scaffolds
> `scripts/dev-setup.*` downstream. Moved (`git mv`) into a new root
> `scripts/`; both launchers now anchor to the repo root from one level down
> (`cd "$(dirname "$0")/.."` / `Split-Path $PSScriptRoot -Parent`) so
> `.venv` still lands at the root, and every usage/cross-reference line says
> `scripts/…`. The Thread-15 Part-D "root dev-setup" wording earlier in this
> file is historical log, left as written.
> `test_meta_repo_dogfoods_dev_setup` now reuses the scaffold's `DEVSETUP`
> relative paths, so the meta-repo and scaffold layouts can't silently drift
> apart again. `pytest -q`: 296 passed, 1 skipped (same run as WI-1.31).
> Byte deltas: no budgeted file touched.

> **WI-1.41 ✅ landed 2026-07-07 · README need-coverage guard: opt-in → opt-out,
> marker-free.** Owner-raised during the Thread 47 self-adoption walk-through:
> traceability is the kit's core value, so the root README should honor it **by
> default**, and the `<!-- sn-inventory -->` delimiter markers are needless
> ceremony. `check_docs.check_inventory` is reworked — it now scans the **whole
> README** for `SN-###` citations (no markers) and is **ON by default**: every
> Must/Should need in the registry must be cited somewhere in the README, and
> every cited id must exist. A README opts out with an `sn-inventory: off` HTML
> comment **on its own line** (anchored regex, so prose that merely *documents*
> the opt-out can't trip it — a footgun the change itself surfaced when the
> template's guidance comment silently opted the scaffold out). A repo with only
> the `-000` placeholder is vacuously clean, so a fresh scaffold passes.
> **⚠ Downstream migration (breaking):** an existing adopter with real
> Must/Should needs whose README does not cite them will now **FAIL check_docs at
> every gate** on their next re-sync — they must add the citations or the opt-out
> comment (previously the check was silent unless they added the markers).
> Meta-repo dogfood: the root README now cites all 12 core needs (SN-001..012) on
> its existing capability bullets + self-adoption note (no duplicated inventory),
> and gained a "gates at a glance" quick-reference. Docs: shipped
> `README.template.md` (marker-free pattern + opt-out note), both READMEs'
> check_docs descriptions. Tests: `test_check_docs` inventory tests reworked
> (default-on fails an uncovered Must with no markers; the opt-out comment
> silences; a bad citation fails). `pytest -q`: **366 passed, 2 skipped**;
> `check_docs --root . --stale`: OK, 0 broken. Byte deltas: AGENTS.template.md /
> PROCESS.md untouched.

> **WI-1.42 ✅ landed 2026-07-07 · Arm the process floor from the universal
> onboarding rung (not only from `setup`).** Surfaced by an adversarial G3
> review: the meta-repo shipped with its git-hook floor **dormant**
> (`core.hooksPath` unset, no `.githooks/`), so WI-1.41's docstring edit staled
> the generated code map and that **slipped past commit** — caught only later at
> the full `check.py --gate G3` (the arch-map `--check` step). Root cause is a
> design gap, not a one-off: hook-wiring (`git config core.hooksPath .githooks`)
> lives **only** in `setup.{sh,ps1}` — the per-clone *product-toolchain* rung. A
> non-code contributor (who runs only `dev-setup`), and any clone that skips
> `setup`, never gets the floor — even though wiring it is universal (every
> committer wants it), zero-dependency, and reversible. **SR-032** doesn't catch
> this either: it verifies the scripts "run to a green setup," not that the floor
> is *active* afterward.
> **Proposed (kit change — keep the two rungs, move the wiring):**
> 1. Wire `core.hooksPath` in **`dev-setup`'s baseline** (universal, zero-dep,
>    idempotent); keep `setup.{sh,ps1}` wiring it too so a setup-only clone stays
>    covered — single-source the one-liner in a shared helper, don't duplicate it.
> 2. For the **code** profile, `dev-setup --baseline` offers (consent-first) to
>    chain into `setup`, so a code contributor reaches workstation + toolchain +
>    floor from one command; a non-code profile does **not** pull the test venv.
> 3. Tighten **SR-032** acceptance to "…and the process floor is active after
>    setup," with a TC asserting `core.hooksPath` is set on a fresh scaffold.
> 4. Generalize the shipped `pre-commit` so a **non-standard layout** (harness not
>    under `scripts/`) works via an optional scripts-dir override, instead of every
>    such repo hand-maintaining a copy — this meta-repo's `.githooks/pre-commit`
>    (added as the interim fix below) is the reference case.
> **⚠ Downstream impact:** touches kit-owned `setup.template.*`,
> `dev-setup.template.*`, PROCESS.md §7 + PROCESS_OPTIONS §7 boundary notes, and
> SR-032/its TC. On the next re-sync an adopter's `dev-setup`/`setup` are
> overwritten (kit-owned files) and their fresh scaffold begins wiring the floor
> from `dev-setup`; an adopter who hand-customized those launchers must re-merge.
> **No git-history or commit-format change** — `core.hooksPath` is local per-clone
> config, opt-in and reversible (`git config --unset core.hooksPath`); the change
> is additive (a floor that was absent turns on), not a new rule against existing
> commits.
> **Interim — landed this session (the "small" self-adoption fix):** this repo now
> carries its own layout-adapted `.githooks/pre-commit` (points the floor at
> `project-trajectory/scripts/`) and `core.hooksPath=.githooks` is set locally, so
> the meta-repo's floor is finally live (verified: passes clean, blocks a staged
> stale map). commit-msg/pre-push adaptation is deferred to this WI —
> `docs/privacy-check` is `false` here, so those hooks are ~no-ops today.
>
> **Landed 2026-07-07 (this session, 3 commits).** All items done:
> **(4)** `hooks/pre-commit` generalized — `REPO_ROOT` via `git rev-parse` (so a
> wrapper can delegate), an optional `KIT_SCRIPTS_DIR` override (relative or
> absolute; a bad value skips clearly, never a silent pass), and the venv-preference
> moved here so it is single-sourced for every repo. The meta-repo's
> `.githooks/pre-commit` is now a 14-line WRAPPER (was a 46-line hand copy),
> delegating with `KIT_SCRIPTS_DIR=project-trajectory/scripts` — retiring
> adversarial findings #2 (hand-copy drift) and #3 (venv-preference) for good.
> **(1)** `dev-setup.template.{sh,ps1}` now wire `core.hooksPath` from `--baseline`
> and report floor status on `--check`. **(2)** a code-profile `dev-setup` offers to
> chain into `setup`; a non-code role is not asked. **(3)** SR-032 + LLR-032 + TC-032
> tightened to assert dev-setup wires the floor (spine stays 0-orphan/0-schema);
> `test_onboard_devsetup` gains a floor+chain test; `test_pre_commit_hook` gains an
> override test. **(5)** the boundary-note detail went to **PROCESS_OPTIONS §7**
> (PROCESS.md §7 already links there), so the **byte-budgeted PROCESS.md /
> AGENTS.template.md are untouched**.
> **Deviation from spec:** item 1's "single-source the wiring in a shared helper"
> was NOT done as a new scaffolded file — the wiring is a 3-line idempotent
> `git config`, so duplicating it across `setup` + `dev-setup` beats adding scaffold
> surface + a bootstrap MAPPING entry for a trivially-stable command.
> **⚠ Downstream:** a re-sync overwrites `hooks/pre-commit` + `dev-setup.template.*`
> (kit-owned); a standard `scripts/` layout is behavior-identical (override unset)
> plus the venv-preference + rev-parse robustness; an adopter who hand-customized
> `dev-setup` re-merges. `core.hooksPath` stays local/opt-in/reversible.
> `check.py --gate G3` → **PASS** (9/9); `pytest -q` **371 passed, 2 skipped**;
> coverage **90.56%** (3273/309); trace SN=22 SR=36 LLR=33 TC=36, 0 orphans.
> Byte-budgeted files untouched.

> **WI-1.43 ✅ landed 2026-07-09 · Trace the trajectory layer in the self-adopted
> spine (THREAD_52_REVIEW F1, HIGH).** Thread 52 left `check_trajectory.py` +
> `gen_trajectory.py` the only product scripts with no SR/LLR/TC — tested (~98%)
> but untraced, invisible to `trace.py` (it checks declared-row coherence, not
> symbol coverage). Owner authorized the spine change and scoped the SRs
> (2026-07-09, need-level not code-descriptive): **SR-037** work-item registry
> validation (LLR-034 → `load_wis`/`validate`; TC-037 → `tests/test_trajectory.py`)
> and **SR-038** offline project-state view — single self-contained HTML,
> definition + execution completeness, the SN→SR→LLR→TC hierarchy, the roadmap
> DAG, **usable on mobile viewports** (LLR-035 →
> `build_html`/`spine_stats`/`arch_icicle`/`dag_svg`; TC-038 →
> `tests/test_gen_trajectory.py` + new `test_mobile_responsive_shell` asserting
> the responsive markers, so the mobile criterion is mechanized, not hoped).
> **Future scope deliberately not claimed:** the HOW view + root
> `PROJECT_STATE.html` + git-derived as-of stamp are roadmapped as **WI-039**
> (queued) per the ratified AXES_AND_WORKSTREAMS.md spec — Verified rows state
> only what is true today. **WI-038** (done) records the fix in the dogfood
> registry; dashboard regenerated. Also removed a stray "how" line accidentally
> saved into `low-level-requirements.csv`.
> **Deviation from spec:** none (the review's suggested local fix + the owner's
> scope ruling; the review's "deeper thread" — a mechanical untraced-code check —
> stays open, Thread 49-adjacent).
> `check.py --gate G3` → **PASS** (11/11); `pytest -q` **394 passed, 2 skipped**;
> trace **SN=22 SR=38 LLR=35 TC=38**, 0 orphans/integrity/schema. Byte-budgeted
> files untouched. **G3 re-attestation pending owner sign-off** (`docs/log.md`).

> **WI-1.44 ✅ landed 2026-07-09 · The component/workstream schema bundle (the
> AXES_AND_WORKSTREAMS.md iter-9 ratified design, one migration event).** Owner
> authorized in-session ("you can implement"). Four coupled, never-breaking
> registry changes, three logical commits: **(1) `Track` → `Workstream`** on
> work-items (the "track" overload killed: the word now means only the
> parallel-execution lane; legacy header still read) **+ hard/soft predecessor
> edges** — bare id = hard (blocks: readiness, ranking, acyclicity ERROR),
> `~id` = soft (advisory: must resolve, soft-only cycles WARN, dashed in the
> dashboard render, never a rank constraint). F3's known false edge
> (WI-014→WI-013) demoted to soft in the dogfood registry; the full 39-edge
> data pass remains the owner's review item. **(2) The CMP component layer:**
> new optional off-spine `components.template.csv`
> (`CMP-ID,Name,Category,Knowledge,State,SupersededBy,PartOf,DetailDoc,Notes`),
> scaffolded by bootstrap; LLR/IF/ASSET/PART templates gain an optional
> `Component` tag cell (structure derived from membership tags, never restated
> on the CMP row); `trace.py` integrity-checks `CMP-` ids and resolves the
> joins (PartOf/SupersededBy + primitive tags) under `--strict`;
> PROCESS_OPTIONS gains the "Component layer" section. **(3) `MOD-###` →
> `REPO-###`** (`repos.template.csv`; a delegated repo was never a component):
> `trace.py` reads `repos.csv` and the legacy `modules.csv` (coexistence
> allowed); MULTI_REPO/EXAMPLE/README/skill renamed with legacy notes. Plus an
> ADOPTING.md §6 migration recipe for the whole bundle.
> **Deviation from spec:** none vs the ratified notes; the deferred-on-need
> items (consumes/effort, typed-IF check, graph-engine extraction, cyclic
> renderer, CAD extractor, cross-CMP-import check) stay deferred as ratified.
> `check.py --gate G3` → **PASS** (11/11); `pytest -q` **408 passed, 2
> skipped**; trace SN=22 SR=38 LLR=35 TC=38, 0 orphans. Byte-budgeted files
> untouched (PROCESS.md / AGENTS.template.md unmodified).

> **WI-1.45 ✅ landed 2026-07-09 · Trajectory-dashboard freshness at commit
> (THREAD_52_REVIEW F2, MEDIUM).** The shipped `hooks/pre-commit` gains step 1b:
> `check.py --run-step trajectory-map`, delegated exactly like the arch-map step
> (the WI-1.26 idiom) — so a registry or README-vision edit that stales
> `docs/trajectory.html` blocks at commit instead of surfacing first in CI (the
> F2 failure that actually bit during the SR-035 session). Vacuous for a
> non-adopter (absent/placeholder-only `work-items.csv` passes;
> `docs/trajectory-check: off` silences); the review's latency question
> measured: **~0.2 s per commit** on the meta-repo's real 40-WI registry. The
> deeper hook-vs-CI question (review cross-cutting #2) is settled and **stated
> once, in the hook's step-1b comment**: a generated artifact's freshness check
> joins the floor when regeneration is one stdlib command and the step is
> vacuous for a repo that never adopted the layer; checks needing the product
> toolchain or gate context (tests, perf, flows) stay in check.py / CI.
> Deliverables: the hook step + rule comment; `test_hook_trajectory_map_step`
> (vacuous → blocks-on-stale → regen-green → `off` opt-out → hook text carries
> the step); a one-line PROCESS_OPTIONS truth-up; WI-040 dogfood row
> (hard edges WI-022 + WI-031 only — no narrative edges, per F3) + regenerated
> dashboard; F2 marked RESOLVED in THREAD_52_REVIEW.md.
> **Deviation from spec:** none (the review's suggested local fix, verbatim).
> **⚠ Downstream:** a re-sync overwrites `hooks/pre-commit` (kit-owned). A
> mixed-state repo that re-syncs only the hook against a pre-Thread-52
> `check.py` fails clearly (`check: no step named 'trajectory-map'`) — ADOPTING
> §6 re-syncs the kit-owned set together; same class as WI-1.26's delegation.
> `check.py --gate G3` → **PASS** (11/11, incl. the new step); `pytest -q`
> **409 passed, 2 skipped**; trace SN=22 SR=38 LLR=35 TC=38, 0 orphans.
> Byte-budgeted files untouched.

### Session protocol (for a cold session pointed only at this file)

0. **If there is no ▶ NEXT session marker, don't invent one — confirm first.** As of
   2026-07-04: Threads 0–28 have landed (sessions A–K, plus the WI-1.x items).
   **Threads 29–40 are specced and ruled** (owner rulings 2026-07-04 — the
   "2026-07-04 batch — decision briefs" section records them; each thread's
   Status line carries its operative form). Sessions L/M/N/O/P/Q/R/S are
   sequenced by the **▶ NEXT marker** in the sessions block (set 2026-07-04
   with the owner's rulings) — follow it per steps 1–5. **Threads 41–43 all
   landed 2026-07-05 (WI-1.33/1.34 + the three thread Status blocks).**
   **Threads 44–45 ✅ landed 2026-07-05** (44: always-on secrets floor, split
   from the identity gate, with a `docs/secrets-scan: off` opt-out; 45:
   coordinator `ERROR` outcome — session-errored ≠ ran-no-commit, agent-error
   abort banner). The **stubs** (16 non-code-artifact
   verification · 21 cross-repo tooling · 23 publication composition) still
   each need a decision to revive.
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
