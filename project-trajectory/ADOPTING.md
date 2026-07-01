# Adopting the kit in an existing repo (retrofit guide)

> `bootstrap.py` and the README quick-start assume a **new, empty** repo. This
> guide covers the harder, more common case: dropping the kit into a repo that
> already has code, history, CI — and possibly a non-Python stack. It is a
> reference doc (like `EXAMPLE.md`), not scaffolded into projects.

The short version: the **process layer ports everywhere as-is**; the **product
layer you rewire**; the two Python-reference generators (`gen_arch_map.py`,
`check_stubs.py`) you **port or explicitly drop — never leave passing
vacuously**. Requirements are **backfilled from the boundary outward**, not
retro-documented wholesale.

## 1. Scaffold into the existing repo

From the kit folder: `python scripts/bootstrap.py --dest /path/to/repo`.
Bootstrap never overwrites an existing file (no `--force`), so collisions are
reported as `skipped (exists)` — resolve each by hand:

- **`.gitignore`** — skipped if present; merge `gitignore.template`'s entries in
  (the generated composites under `docs/test/` must be ignored, or they churn
  every diff).
- **`.github/workflows/check.yml`** — if you have CI already, add the
  `check.py` invocation to it instead of adopting the reference workflow
  wholesale. Keep one definition of "passing": CI runs the same command you run
  locally.
- **`pytest.ini`** — Python repos with an existing pytest config: merge the
  tier markers (`smoke`/`full`/`release`) rather than replacing the file.
- **`src/`, `tests/`** — bootstrap only adds `.gitkeep`s; your layout stays.
  Point the harness at the real roots (`SRC`/`TESTS` in `check.py`).
- **Pre-commit hook** — `setup.{sh,ps1}` set `git config core.hooksPath
  .githooks`, which **overrides** any existing `.git/hooks` or hook manager
  (husky, pre-commit-framework). If you already have hooks, either call
  `.githooks/pre-commit` from your existing hook chain or skip the wiring —
  CI remains the enforcement of record.
- Delete what genuinely doesn't apply (e.g. `docs/interfaces.md` for a
  standalone project) — but prefer leaving the inert optional registries in
  place; they cost nothing empty.

## 2. Wire the harness to your stack

Edit `scripts/check.py` (`SRC`/`TESTS` + the "EDIT FOR YOUR STACK" block in
`steps()`):

- **Product steps** (format / lint / tests+coverage) — swap the `ruff`/`pytest`
  commands for your toolchain (`gradle check`, `npm test`, `cargo clippy`, …)
  or drop a step you don't have. Keep each step's gate tags.
- **Process steps** (traceability, design-flows, doc-navigability,
  perf-budgets) — keep as-is. They are stdlib Python and read only the
  registries and docs, so they work identically for a Java, Kotlin, or Rust
  repo. The kit needs a Python 3.8+ interpreter on the machine for these even
  when the product isn't Python; that is the only requirement.

## 3. Non-Python stacks: the two generators (don't fake the guarantee)

Two shipped scripts parse **Python source specifically**:

- **`gen_arch_map.py`** (the code map + dependency diagram + `--check`
  freshness gate). On a repo with no `.py` under `SRC` it generates an empty
  map once, and `--check` then passes **vacuously forever** — the
  "architecture can't drift" guarantee silently lapses while the docs still
  claim it (the script now warns on stderr when it scans nothing). Pick one,
  explicitly:
  1. **Port it** (recommended for a repo you'll live in): any tool that can
     enumerate modules/symbols in your language (ts-morph, `go doc`, a Gradle
     task over the AST) writing into the **same marker block**
     (`<!-- BEGIN/END GENERATED MODULE MAP -->` etc.) — the marker block is
     the whole contract; `--check`-style freshness is a string comparison.
  2. **Remove the `arch-map` step** from `check.py` and delete the generated
     markers from `architecture.md`, keeping the hand-written overview. Honest,
     just weaker: record the loss in `docs/status.md` constraints.
- **`check_stubs.py`** is Python-only and already optional/product-layer: swap
  it for your language's equivalent or ignore it.

## 4. Backfill requirements from the boundary, not wholesale

Retro-documenting an entire existing codebase into SN→SR→LLR→TC rows is
make-work that produces paraphrase, not traceability. Instead:

- **Set `docs/gate` to `G1` honestly**, whatever the code's maturity — gates
  describe the *registry's* coverage of the product, and that coverage starts
  near zero. Claim G2/G3 only when their criteria genuinely hold for the scope
  the registries actually cover.
- **Write SNs/SRs for the load-bearing behavior first**: what the project must
  keep doing (the things a regression would page you for), plus the edge-case
  table. These are cheap rows with high protective value.
- **New work gets the full spine from day one**; existing code earns rows when
  you next touch it (the same change that edits the code adds its SR/LLR/TC).
  Coverage grows along the paths that actually change — which is where the
  risk is.
- Existing tests can be adopted as TCs: give each meaningful test a `TC-###`
  row and put the id in the test name — no rewrite needed.

## 5. First green run

```
python scripts/check.py            # gate from docs/gate (G1 to start)
python scripts/trace.py            # writes docs/test/report.md
```

The G1 bar is deliberately small (doc navigability). Bump `docs/gate` in a
reviewed commit as each gate's criteria are genuinely met — CI reads it and
raises the bar with you (process.md §7 "The active gate").
