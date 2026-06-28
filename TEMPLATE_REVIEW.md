# Template Repository Review

Date: 2026-06-26

## Summary

This repository has a strong foundation for a reusable, requirement-traced project template. The documentation is unusually explicit about gates, traceability, and human approval; the scripts are mostly stdlib-only where promised; and the self-tests exercise real downstream scaffolds, which is exactly the right kind of coverage for a template kit.

The main improvement theme is reducing the chance of a scaffold looking green before it is truly project-ready. The highest-value changes are to make command examples more portable, fail G2 when placeholder rows remain, and add registry schema validation beyond relationship tracing.

## Findings

### 1. High: README quick-start assumes `python`

`README.md` and `project-trajectory/README.md` use `python ...` directly in quick-start commands. On modern macOS, `python` is often absent. On the reviewed host, both `python3` and `git` were also intercepted by `xcode-select` because Apple command-line tools were missing.

The shipped `setup.sh` is more robust because it searches `python3` then `python`.

Recommendation:

- Prefer `./scripts/setup.sh`, `./scripts/check.sh`, or `python3` in user-facing examples.
- Add a short macOS note for installing Command Line Tools when `xcode-select` blocks `python3` or `git`.

Relevant files:

- `README.md`
- `project-trajectory/README.md`
- `project-trajectory/scripts/setup.sh`
- `project-trajectory/scripts/check.sh`

### 2. High: G3 harness is Python-default, while the kit markets itself as stack-agnostic

`project-trajectory/scripts/check.py` hardcodes `src`, `tests`, `ruff`, `pytest`, and Python coverage. The docs do say this is a Python reference implementation, but users bootstrapping a JavaScript, Go, Rust, or other non-Python repo will get failing checks unless they know exactly what to edit.

Recommendation:

- Add a prominent "customize these lines first" section near the bootstrap instructions.
- Consider splitting the harness into a small generic runner plus a visible step table/config section.
- Consider template variants such as `check.python.py`, `check.generic.py`, or a bootstrap option like `--python-reference` / `--generic`.

Relevant file:

- `project-trajectory/scripts/check.py`

### 3. Medium: fresh scaffolds can look green because placeholders are ignored or accepted

`trace.py` ignores IDs ending in `-000`, and `check_flows.py` accepts placeholder IDs such as `SR-000` and `LLR-000`. This is useful for making a fresh scaffold runnable, but it can create false confidence if someone runs G2 before replacing example rows and diagrams.

Recommendation:

- Add a `--no-placeholders` mode to `trace.py` and `check_flows.py`.
- Wire that mode into the harness from G2 onward.
- Alternatively, make `check.py --gate G2` fail when any `-000` placeholder remains in registries or runtime-flow diagrams.

Relevant files:

- `project-trajectory/scripts/trace.py`
- `project-trajectory/scripts/check_flows.py`
- `project-trajectory/scripts/check.py`
- `project-trajectory/ARCHITECTURE.template.md`
- `project-trajectory/registries/*.template.csv`

### 4. Medium: traceability validates links, but not registry data quality

`trace.py` checks orphan relationships, but it does not enforce required fields or valid values. For example, linked rows can still have empty or invalid `AcceptanceCriteria`, `Priority`, `Verification`, `Status`, `Tier`, or `Automated` values.

That means a requirement chain can be structurally linked but still too vague to implement, test, or approve.

Recommendation:

- Add `validate_registries.py`, or extend `trace.py` with schema checks.
- Validate required columns and required fields.
- Validate enum values.
- Detect duplicate IDs.
- Detect invalid ID formats.
- Detect unresolved references even when optional files are absent.

Suggested checks:

- SR rows: `SR-ID`, `Title`, `UN-Refs`, `Requirement`, `AcceptanceCriteria`, `Priority`, `Verification`, `Status`.
- LLR rows: `LLR-ID`, `SR-Refs`, `Title`, `Module`, `CodeSymbol`, `Detail`, `Status`.
- TC rows: `TC-ID`, `Verifies`, `Level`, `Method`, `Tier`, `Expected`, `Automated`, `Status`.
- Interface rows: `IF-ID`, `Direction`, `ThisProject`, `Counterpart`, `Contract`, `Version`, `Stability`, `Status`.

Relevant file:

- `project-trajectory/scripts/trace.py`

### 5. Medium: code map can silently preserve syntax-broken modules as generated text

`gen_arch_map.py` catches `SyntaxError` and renders it as a `PARSE ERROR` summary. That is helpful for surfacing the error in documentation, but freshness checking alone may still pass after regenerating that text.

For Python projects, lint/tests should catch syntax errors. For customized or non-Python projects, the generated map may be the only parse signal users keep.

Recommendation:

- Make parse errors fail `gen_arch_map.py --check`.
- Or add `--strict-parse` and wire it into G3.

Relevant file:

- `project-trajectory/scripts/gen_arch_map.py`

### 6. Medium: bootstrap always copies interface artifacts even though docs say they are optional

The bootstrap script always scaffolds `docs/interfaces.md` and `docs/requirements/interfaces.csv`, while the docs describe interfaces as useful only for interlinked projects.

Recommendation:

- Add `--with-interfaces` or `--no-interfaces`.
- Choose the default that matches the intended common path.
- If always copying them is intentional, adjust the docs to say "leave empty unless interlinked" rather than "use only if interlinked."

Relevant file:

- `project-trajectory/scripts/bootstrap.py`

### 7. Low: CI install sample can mask package install failures

The GitHub Actions workflow includes a commented sample line:

```bash
# pip install -e . || pip install -r requirements.txt || true
```

It is commented, but many users will uncomment it as-is. The trailing `|| true` can hide dependency installation failures in CI.

Recommendation:

- Replace this with separate explicit examples that fail normally.
- Example: "choose one of these" with separate `pip install -e .` and `pip install -r requirements.txt` comments.

Relevant file:

- `project-trajectory/ci/check.yml`

### 8. Low: generated architecture freshness does not enforce every stated architecture rule

`ARCHITECTURE.template.md` says "Design rules (enforced)," but the current generator primarily enforces freshness of the generated map and dependency diagram. It does not enforce rules like no duplication, pure-core boundaries, maximum module/function size, or forbidden import directions.

Recommendation:

- Reword this section to "Design rules (reviewed)" if enforcement remains human-driven.
- Or add configurable architecture checks, such as forbidden import edges or maximum public surface warnings.

Relevant file:

- `project-trajectory/ARCHITECTURE.template.md`

## Strengths

- The process documentation is clear about gates, roles, approval pauses, and traceability.
- The `UN -> SR -> LLR -> TC` spine is simple enough to use and concrete enough to audit.
- The harness uses the active interpreter for tools, which avoids a common virtualenv/PATH failure mode.
- The scripts are stdlib-only where that promise matters downstream.
- The self-tests bootstrap real scaffolded projects instead of only unit-testing helper functions.
- The generated architecture map and Mermaid dependency diagram are a strong fit for agent-assisted maintenance.
- The tiered test model is practical: smoke for cheap iteration, full for pre-merge, release for slow/manual-adjacent confidence.

## Suggested Next Improvements

The three highest-value next changes are:

1. Update README and template docs to prefer launchers or `python3` and document macOS Command Line Tools setup.
2. Add placeholder detection and fail G2 when `-000` examples remain.
3. Add registry schema validation so structurally linked rows are also meaningful and gate-ready.

After that, consider adding strict parse behavior for `gen_arch_map.py`, making interface scaffolding optional, and tightening the CI install sample.

## Verification Notes

The test suite could not be run on the reviewed host because `python3`, `git`, and related developer commands were intercepted by `xcode-select` due to missing Apple command-line tools.

Static review was completed against the working tree.
