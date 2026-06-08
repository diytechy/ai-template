# CLAUDE.md — Agent & Contributor Guide

**What this file does:** the standing brief for any agent or human working in
this repo. It encodes *how we build here* so quality doesn't depend on who (or
which model) shows up. It is loaded into an agent's context every session —
keep it short, concrete, and current. Project facts live in `docs/`; this file
points at them rather than restating them.

> Copy this into a new repo as `CLAUDE.md`, then fill the **Project** section and
> delete guidance that doesn't apply. Everything below the line is the durable
> part — change it deliberately, not per-task.

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

This repo follows a **gated, requirement-traced process**. Read
[docs/process.md](docs/process.md) once; it is the source of truth for roles,
gates, and the ID scheme. The short version an agent needs every session:

- **One driver wears role "hats" in sequence** (End User → UX/Docs → System
  Engineer → Software Engineer → Test Engineer), keeping context. Spawn a
  separate reviewer only for an independent pre-gate audit of high-risk work.
- **Everything traces:** `UN → SR → LLR → TC`. Intent lives once, as an id, and
  children link to it. The matrix is generated (`scripts/trace.py`) and must
  report **0 orphans** before a gate.
- **Gates G1→G2→G3→G-Final each pause for human approval.** Don't advance past a
  gate on your own; record the decision in [docs/status.md](docs/status.md).
- **The check harness is the bar:** `python scripts/check.py` (or
  `scripts/check.sh` / `scripts/check.ps1`) runs format, lint, tests, coverage,
  traceability, and architecture-map freshness. Use `--tier smoke` for the fast
  every-iteration subset; the full/release tiers run pre-merge and at release.
  Never report a result you didn't run — paste the real output.
- **Releases (if this project ships versioned):** the G-Release gate runs the
  `release` tier and a generated human checklist
  (`scripts/gen_release_checklist.py`) covering every Demonstration/Manual item.
- **The code map is generated** (`scripts/gen_arch_map.py`, AST): per-module
  summary, internal dependencies, and public symbols with `Implements:`
  back-links. It lives in [docs/architecture.md](docs/architecture.md) (and may
  be embedded here between the `GENERATED MODULE MAP` markers). **Read it to find
  where a capability lives before searching the tree**; the harness keeps it
  current, so don't hand-edit it.
- **Start each session** by reading the *Current State* header of
  [docs/status.md](docs/status.md); end each turn by updating it (active gate,
  what changed, next action awaiting approval).

## Code we want (readability for humans *and* agents)

The goal is code a newcomer — human or model — can navigate without re-deriving
the design. Concretely:

- **One responsibility per module/function; small functions.** If a function
  needs a "and" to describe it, split it.
- **Separate a pure, testable core from the I/O/network/GUI shell.** Logic that
  decides goes in pure functions (exhaustively unit-tested); side effects live
  in thin shells (Demonstration/integration-tested). This is the single biggest
  lever for testability and clarity.
- **One fact, one home — in code too.** No copy-paste logic; shared behavior
  lives in exactly one place and is imported.
- **Intention-revealing names; no cryptic abbreviations.** Comments explain
  *why*, not *what*; the code says what.
- **Back-link to requirements.** Annotate implementing symbols
  `Implements: SR-007, LLR-014` and name tests so the verified id is visible
  (e.g. `test_export_quotes_special_fields_sr001`). `scripts/gen_arch_map.py`
  surfaces these in the architecture map.
- **Match the surrounding style.** Read a neighboring file first; mirror its
  idioms, error handling, and structure rather than importing your own.
- **Fail loudly, never silently.** Surface errors with context; no bare excepts
  that swallow failure; non-zero exit on failure for anything scriptable.
- **Automation-safe by default.** Anything interactive needs a non-interactive
  path that never blocks; no destructive default; don't mutate inputs in place.

### Comment for humans — and the map

Comment **generously and deliberately**. The bar isn't "every line"; it's that a
reader (human or model) never has to reverse-engineer *intent*. The generated
code map (`scripts/gen_arch_map.py`) **harvests your module docstrings and public
symbol docstrings**, so good comments pay double — they teach the reader at the
code *and* populate the index agents read first. Concretely:

- **Every module/file: a header docstring** stating its single responsibility and
  any invariant it upholds (e.g. "pure core — no I/O"; "must not import Engine").
  This line becomes the module's summary in the map.
- **Every public function/type: a docstring** giving its purpose, the *meaning*
  (and units) of parameters and return, and its failure modes — not a restatement
  of the signature. Include `Implements: SR-/LLR-` so the back-link lands in the map.
- **Explain the *why* at every non-obvious point:** why this algorithm/order/
  constant, which edge case a branch guards, what invariant must hold here, any
  gotcha or external reference (spec/ticket/URL). Assume the next reader lacks the
  context you have right now.
- **Comment the surprising, not the obvious.** Don't narrate self-evident code
  (`i += 1  # increment i`); do flag anything that would make a careful reader
  pause. When in doubt on intent-bearing code, err toward more.
- **A comment is a promise — keep it true.** Update comments in the same edit as
  the code; a stale comment is a bug. Never leave a comment describing behavior
  that no longer exists.

## For analytics / data code specifically

- **Reproducibility is a requirement, not a nicety.** Pin random seeds; record
  data source + version/snapshot; make a run reproducible from inputs alone.
- **Notebooks are for exploration; ship modules.** Promote anything reused or
  tested out of a notebook into `src/` so it can be imported and unit-tested.
- **Separate data I/O from transforms.** Pure transform functions (dataframe in
  → dataframe out) are unit-tested on small fixtures; loading/writing is the
  shell. Validate schema/shape at the boundary and fail loudly on surprises.
- **Test the math on known cases.** Every nontrivial calculation gets a test
  with a hand-checked expected value, not just "it runs".
- **Exercise the input space.** For variable inputs, cover the **boundaries**
  (min/max, empty, zero, one, largest) and combine dimensions deliberately —
  pairwise by default, full only when small or high-risk. Let
  `scripts/gen_cases.py` derive the combinations from the SR's `Permutations`;
  see PROCESS.md "Dimensional coverage".

## Communication style

- Direct and concrete; explain the *why* behind a recommendation, then the *how*.
- Surface trade-offs and uncertainty honestly; ask before assuming on anything
  irreversible or ambiguous.
- Prefer the simplest thing that satisfies the requirement; flag when a request
  looks over-engineered for its need.

---

> **Customizing:** add a rule here only after you've had to repeat it. Delete
> rules you don't enforce — an aspirational CLAUDE.md that the harness doesn't
> back up just adds noise. The best version of this file evolves from real usage.
