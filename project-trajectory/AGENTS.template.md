# AGENTS.md — Agent & Contributor Guide

**What this file does:** the standing brief for any agent or human working in
this repo — *how we build here*, so quality doesn't depend on who (or which
model) shows up. It is loaded every session: keep it short and current.
Project facts live in `docs/`; this file points at them.

<!-- kit-only -->
> Scaffolds to `AGENTS.md` (the cross-tool standard) via `bootstrap.py`.
<!-- /kit-only -->
> Thin `CLAUDE.md`/`GEMINI.md` stubs point back here. Fill the **Project**
> section, delete guidance that doesn't apply. Everything below the line is
> durable — change it deliberately, not per-task.

---

## Project (fill this in)

- **What this is / one-line purpose:**
- **Primary users & their expertise level:**
- **Stack & layout:** language(s); source in `src/`, tests in `tests/`.
- **How to run the app / pipeline:**
- **Non-goals (explicitly out of scope):**
- **Sibling/linked projects (if any):** see `docs/interfaces.md`.

---

## How we work here (the process)

This repo follows a **staged, requirement-traced process** — read
[docs/process.md](docs/process.md) once; it is the source of truth for roles,
the ladder, and the ID scheme. The short version needed every session:

- **One driver wears role "hats" in sequence** (Stakeholder → UX/Docs → System
  Engineer → Software Engineer → Test Engineer). Spawn subagents deliberately
  (process.md §6).
- **Everything traces:** `SN → SR → LLR → TC`. Intent lives once, as an id;
  children link to it. The matrix is generated (`scripts/trace.py`) and must
  report **0 orphans** before a bar.
- **Write the test first (TDD).** A requirement's test case is a *failing*
  test before the code that satisfies it: red → green → refactor — within the
  traceability spine, not instead of it.
- **The stage ladder:** `DevStg-` Needs · Boundary · Reqs · Arch · LLReqs ·
  Tests · Impl · Release. You are IN a stage and CLEAR a bar (`DevStg-Reqs` →
  `-Tests` → `-Release`) per `docs/process.toml`. Never self-advance; log it.
- **The check harness is the bar:** `python scripts/check.py` runs format,
  lint, tests, coverage, traceability, flow checks and map freshness at the
  derived bar (`docs/gate`); `--tier smoke` is the fast subset. Never report a
  result you didn't run — paste the real output.
- **Behavior is reviewed as diagrams, not rows:** runtime flows (especially
  concurrent ones) are authored Mermaid sequence diagrams in
  [docs/runtime-flows.md](docs/runtime-flows.md), kept current
  with the LLRs (`scripts/check_flows.py` enforces; §3).
- **Releases (if versioned):** `DevStg-Release` runs the `release` tier plus
  the generated checklist (`scripts/gen_release_checklist.py`).
- **The code map is derived from the source AST**: per-module summary and
  public symbols with `Implements:` back-links, rendered live in
  `PROJECT_STATE.html`'s How-SW tab. **Read it to
  find where a capability lives before searching the tree**;
  `scripts/gen_arch_map.py --doc` can also splice it here — never hand-edit
  between `GENERATED` markers; never commit exported diagrams.
- **Start each session** with *Current State* in
  [docs/status.md](docs/status.md); end each turn by updating it (stage, what
  changed, next action). **Commit early and often** — small and green per
  logical step. Pushing follows the `push` dial (default: the human
  publishes). End with a clean tree.

## Code we want (readability for humans *and* agents)

Code a newcomer — human or model — can navigate without re-deriving the design:

- **One responsibility per module/function; small functions.** If describing a
  function needs an "and", split it.
- **Separate the pure, testable core from the I/O/network/GUI shell.** Logic
  that decides goes in pure functions (exhaustively unit-tested); side effects
  live in thin shells (Demonstration/integration-tested).
- **Entry points orchestrate, they don't compute.** A top-level routine reads
  as a short list of well-named step calls; push logic into the steps.
- **One fact, one home — in code too.** No copy-paste logic; shared behavior
  lives in exactly one place.
- **Intention-revealing names; no cryptic abbreviations.** Comments explain
  *why*; the code says what.
- **Back-link to requirements:** `Implements: SR-007, LLR-014` on implementing
  symbols; test names embed the verified id
  (`test_export_quotes_special_fields_sr001`).
- **Match the surrounding style.** Read a neighboring file first; mirror its
  idioms.
- **Fail loudly, never silently.** No bare excepts; nonzero exit on failure
  for anything scriptable.
- **Automation-safe by default.** Anything interactive needs a non-interactive
  path that never blocks; no destructive defaults; don't mutate inputs in place.

### Comment for humans — and the map

Comment **generously and deliberately** — a reader must never have to
reverse-engineer *intent*. The generated code map **harvests module and
public-symbol docstrings** into the index agents read first:

- **Every module: a header docstring** — its single responsibility plus any
  invariant it upholds ("pure core — no I/O").
- **Every public symbol: a docstring** — purpose, the *meaning* (and units) of
  parameters and return, failure modes; include `Implements: SR-/LLR-` so the
  back-link lands in the map.
- **Explain the *why* at every non-obvious point:** the algorithm/order/
  constant choice, the edge case a branch guards, the invariant that must
  hold. Comment the surprising, not the obvious.
- **A comment is a promise — keep it true.** Update it in the same edit as the
  code; a stale comment is a bug.

### Define the interface (contract) at the code

Every public module/function states its contract once, in its docstring, so a
caller never has to read the body to use it safely. Cover **Inputs** (type +
range/enum/units), **Outputs**, **Config** (keys + constraints + where they
live), **Raises** — and **cite requirement ids instead of restating
constraints** already in an SR (`AcceptanceCriteria` + `Permutations`).
Reference shape:

```
"""Back up one source set: hash, dedup, snapshot, write manifest.

Contract:
  Inputs:  source_path: str (existing dir; see SR-014)
  Outputs: BackupResult { copied: int, snapshotted: bool }
  Config:  compress: bool; hash_frequency_days: int >= 0  [BackupConfig.xml]
  Raises:  PermissionError if backup_path is unwritable  (SR-017)
Implements: SR-014, LLR-014
"""
```

Keep tag names greppable; update the contract with the signature — a wrong
contract is worse than none.

## For analytics / data code

- **Reproducibility is a requirement:** pin random seeds; record data source +
  version/snapshot.
- **Notebooks explore; modules ship.** Promote anything reused or tested into
  `src/` so it can be imported and unit-tested.
- **Separate data I/O from transforms:** pure transforms unit-tested on small
  fixtures; validate schema/shape at the boundary, failing loudly on surprises.
- **Test the math on hand-checked cases**, and **exercise the input space** —
  `scripts/gen_cases.py` derives boundary + combination cases from the SR's
  `Permutations` (process.md "Dimensional coverage").

## Working agreement

Direct and concrete; explain the *why* before the *how*.

- **Ask, don't assume.** Unclear intent, architecture, or requirement → ask
  before writing code — one question, with a **recommended default**.
  Unattended: pick the most reasonable reading, proceed, and **record it**
  under *Assumptions* in `docs/status.md` to confirm or revert at the next
  bar. When reality contradicts the plan, **the contradiction is the
  deliverable**: raise the conflict as a finding — never silently resolve,
  average, or route around it (process.md §4 "Consistency review"). The
  **decision dial** (process.md §6) sets asking eagerness: high-risk ratifies
  often, low-risk decides-and-records.
- **Right-size the solution.** The simplest thing that satisfies the
  requirement; no speculative flexibility — **every line is a liability**, so
  before adding, ask what you can delete. Judge "simple" against the whole
  design; flag over-engineering either way. (`SHORTCUT:` convention: §3.)
- **Scope is a promise; stay in your lane.** Don't change unrelated code — the
  silent extra is what destroys trust; surface a design smell as a separate
  finding to its owner, not an inline fix.
- **Flag uncertainty honestly — and distrust certainty**, yours or a
  reviewer's: a finding is a claim, so confirm or refute it first
  (process-options.md "finding lifecycle"). An experiment with hypothesis +
  result beats confident guessing; peak confidence is when the 30-second
  recheck is cheapest (process.md §6).
- **No sunk-cost shipping, keeping, or blind retries.** An approach found
  wrong late is still wrong — drop it; never retry past a failure whose cause
  you haven't found (process.md §6). A wrong design is escalated as a written
  case to its owner, never patched around or parked — costly rework is
  sanctioned.
- **Repo text is the project's memory; yours is scratch.** Durable facts — a
  decision, constraint or gotcha — belong in `docs/` (status, registries,
  AGENTS.md), not in agent-private memory. Promote them before closing a
  session (process.md §7). Undoing takes the same evidence as doing: read the
  record behind landed work before reverting it.
- **State the constraint, not its history.** Cite a decision record only where
  a reader could plausibly undo it — **at most once per module**, a header
  pointer, never a per-site sprinkle. Provenance belongs in the archive.

---

> **Customizing:** add a rule only after you've had to repeat it, and **pay for
> it by tightening another** — this file has a hard byte budget (keep ≥2k
> headroom under Gemini's ~12k AGENTS.md cap for project facts). Delete rules
> you don't enforce — unbacked rules are noise.
