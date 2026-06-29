# Kit Improvement Plan

Derived from `TEMPLATE_REVIEW.md` (resolved 2026-06-28) plus four follow-on
design threads and a cross-agent-portability decision. This file is the **spec a
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

## Thread 1 — Generated UN→SR→LLR→TC traceability graph

**Goal:** a generated, browsable picture of the requirement spine that doubles as
a gap visualizer. Data already exists in `trace.py`'s join; this is rendering.

- Emit a Mermaid `graph LR` (a DAG, **not** a mindmap — a TC verifies an SR *and*
  an LLR; an SR has many LLRs) into `docs/test/report.md` (regenerated every run
  ⇒ fresh at each gate automatically; no staleness check needed). Optionally also
  splice into `architecture.md` behind a new `TRACEABILITY GRAPH` marker pair.
- Nodes: UN/SR/LLR/TC; edges follow the existing parent links. **Color by
  `Status`/orphan state** (Mermaid `classDef`) so a Draft/orphan stands out — the
  "requirement clarity" payoff. Scale guard: for large graphs, group by `Area`
  or emit per-phase subgraphs.
- Optional secondary: `trace.py --html` → a static, **dependency-free**
  collapsible `<details>` tree (inline CSS, zero JS) for browsing/onboarding.
  Framed as secondary (HTML doesn't diff/review like the Mermaid block).

**Tests:** `report.md` contains a ```mermaid graph; the minimal chain renders
UN-001→SR-001→LLR-001→TC-001 edges; an orphan/Draft node gets the distinct
class. If `--html`, assert a self-contained file with no `<script>`.

**Risks:** graph noise on big projects (mitigate via grouping/per-phase);
keep the Mermaid generation stdlib string-building (no new dep).

**Done-when:** harness run regenerates the graph; gap states are visually
distinct; `pytest -q` green.

---

## Thread 2 — Name the process/product check split

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

## Sequencing & session strategy

Dependencies: Thread 2's process/product *concept* feeds 0b; Threads 1 and 3 are
independent. Recommended order:

1. **Thread 0a** (AGENTS pivot) — structural rename; do with fresh context.
2. **Thread 0b + Thread 2 concept** (git hooks + name the layers).
3. **Thread 3** (directives) — small; can ride with 0a since it edits the same
   file.
4. **Thread 1** (traceability graph) — visible feature, independent.

Each phase ends green (`pytest -q`, real output) and checks its items off here.

**Phase boundaries are natural session boundaries.** Thread 0a alone is a
wide rename; pairing it with everything else in one session risks context
exhaustion mid-rename. Capture is done (this file); implement per-phase in fresh
session(s) using this doc + the branch as the spec.
