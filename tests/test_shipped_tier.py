"""TC-149 — the adopter-facing (`shipped`) half of SR-034 / SN-011 (WI-420).

SN-011 and SR-034 draw a distinction the ledger's own suite does not check:
a dependency reached by a check an **adopter runs** forces every adopting repo
to install it, so it needs an owner ruling and stdlib stays *preferred* there;
a `coordinator` dependency only this repo installs carries a far lower bar.
`test_dependency_ledger.py` asks one question — *is this import declared?* — and
never reads the `Tier` column, so before this module nothing stopped a
`coordinator`-tier package (or an unruled one) from being imported by
`trace.py` and shipped to every adopter.

**How the adopter-facing set is derived, not guessed.** `check.py`'s step table
already tags each step `layer="process"` (kit-owned, identical in every project
— the checks an adopter runs) or `"product"` (wire it to your stack). This
module takes the `process` steps' entry scripts, walks their *transitive* sibling
imports inside `scripts/`, and holds every non-stdlib module in that closure to
the shipped bar. Transitive matters: `trace.py` importing a sibling that imports
a package ships that package just as surely as a direct import.

The plan is built with `profile=None` — the **built-in** process steps, i.e. what
the kit ships — not this repo's `docs/stack.ini`, because the bar is about what
adopters inherit, not what this meta-repo happens to run locally.

Today this is green with nothing to check: the ledger declares zero `Kind=python`
rows (only the `git`/`gh` substrates), so the closure is pure stdlib. That is the
point — it bites the day the first adopter-facing package is proposed, which is
exactly when a human should be reading. Per the standing vacuous-guard rule the
mutation proof lives in this file: `test_bar_catches_a_coordinator_tier_import`
and `test_bar_catches_an_unruled_shipped_import` drive the checker over
synthetic trees and assert it CATCHES, so the green above is demonstrated able
to fail before it is trusted to pass.

Enforcement-audit note (docs/enforcement-audit.md): this is the EVAL/test-class
enforcer for SR-034's shipped-tier clause, which had **no** mechanical enforcer
before WI-420 — it was carried by prose in docs/dependencies.md alone.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

from conftest import SCRIPTS, load_script
from test_dependency_ledger import ledger_rows


def process_entry_scripts() -> set[str]:
    """Module stems of the entry scripts of every `layer="process"` check step.

    Read from check.py's own plan rather than a hand-copied list, so a step that
    changes layer or command cannot drift away from this bar.
    """
    check = load_script("check")
    plan = check.steps(
        coverage=80, tier="full", stage="DevStg-Impl", phase=None, profile=None
    )
    stems = set()
    for _name, _requires, cmd, _threshold, layer in plan:
        if layer != "process":
            continue
        for arg in cmd:
            if isinstance(arg, str) and arg.endswith(".py"):
                stems.add(Path(arg).stem)
    return stems


def top_level_imports(path: Path) -> set[str]:
    """Top-level module names imported by one script (absolute imports only)."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    tops: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            tops |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            tops.add(node.module.split(".")[0])
    return tops


def sibling_sources(script_dir: Path, name: str) -> list[Path]:
    """Every source file the sibling `name` contributes, or [] if it is none.

    A sibling is a `*.py` beside the entry script OR A SHIPPED PACKAGE
    DIRECTORY — a subdirectory holding `__init__.py` (WI-448 added the first,
    `kitlib/`). Before that, `siblings` was a set of top-level `*.py` stems and
    a package read as a THIRD-PARTY dependency: `kitlib` is not in
    `sys.stdlib_module_names`, so the shipped bar demanded a
    `docs/dependencies.md` row for the kit's own code. Worse than the false
    red, and the reason this returns a file LIST rather than one path: the walk
    would then never open the package's modules, so a real non-stdlib import
    hidden inside `kitlib/` would be invisible to the bar it is most subject
    to — the package is adopter-facing by construction.
    """
    module = script_dir / (name + ".py")
    if module.is_file():
        return [module]
    package = script_dir / name
    if (package / "__init__.py").is_file():
        return sorted(package.glob("*.py"))
    return []


def reachable_nonstdlib(script_dir: Path, entries: set[str]) -> dict[str, set[str]]:
    """Non-stdlib modules reachable from `entries`, mapped module -> importers.

    Walks sibling imports transitively (see `sibling_sources` for what counts),
    so an indirect dependency is attributed to the sibling that actually imports
    it — the file an author has to open to fix it.
    """
    siblings = {p.stem for p in script_dir.glob("*.py")} | {
        p.parent.name for p in script_dir.glob("*/__init__.py")
    }
    seen: set[str] = set()
    queue = [s for s in sorted(entries) if s in siblings]
    found: dict[str, set[str]] = {}
    while queue:
        stem = queue.pop()
        if stem in seen:
            continue
        seen.add(stem)
        for source in sibling_sources(script_dir, stem):
            for top in sorted(top_level_imports(source)):
                if top in siblings:
                    queue.append(top)
                elif top not in sys.stdlib_module_names:
                    found.setdefault(top, set()).add(stem)
    return found


def shipped_bar_violations(
    script_dir: Path, entries: set[str], rows: list[dict]
) -> dict[str, str]:
    """Reachable non-stdlib modules that fail the shipped bar, module -> reason.

    A module passes only as a `Kind=python` ledger row that is `Tier=shipped`
    AND carries a non-empty `Ruled` cell. Undeclared, coordinator-tier and
    unruled rows each fail with their own reason, so the message names the fix.
    """
    by_name = {r["name"]: r for r in rows if r["kind"] == "python"}
    bad: dict[str, str] = {}
    for module, importers in sorted(reachable_nonstdlib(script_dir, entries).items()):
        via = ", ".join(sorted(importers))
        row = by_name.get(module)
        if row is None:
            bad[module] = (
                f"imported by {via} (reached by an adopter-facing `process` check) "
                "but has no Kind=python row in docs/dependencies.md"
            )
        elif row["tier"] != "shipped":
            bad[module] = (
                f"imported by {via} (adopter-facing) but its ledger row is "
                f"Tier={row['tier']!r} — an adopter-facing dependency must be "
                "Tier=shipped, which carries the higher bar"
            )
        elif not row["ruled"] or row["ruled"] in {"—", "-"}:
            bad[module] = (
                f"imported by {via} and declared Tier=shipped, but its `Ruled` "
                "cell is empty — a shipped-tier dependency forces every adopter "
                "to install it and needs an owner ruling recorded in the ledger"
            )
    return bad


def test_adopter_facing_checks_meet_the_shipped_bar():
    """The real bar: nothing an adopter runs pulls an unruled/coordinator dep."""
    entries = process_entry_scripts()
    assert entries, "no process-layer steps found — check.py's plan or layer tags moved"
    violations = shipped_bar_violations(SCRIPTS, entries, ledger_rows())
    assert violations == {}, (
        "adopter-facing (`process`-layer) checks reach dependencies that fail the "
        "shipped-tier bar of SR-034/SN-011: {}".format(violations)
    )


def test_the_process_layer_still_covers_the_kit_floor():
    """Guard the derivation itself: if check.py stopped tagging the traceability
    or derived-gate steps `process`, this bar would silently cover nothing."""
    entries = process_entry_scripts()
    for expected in ("trace", "derive_gate", "check_docs"):
        assert expected in entries, (
            f"{expected}.py is no longer an entry script of any `process`-layer "
            "step — either check.py's layer tags moved or this bar has gone blind"
        )


def _fixture_tree(tmp_path, files):
    for name, src in files.items():
        (tmp_path / name).write_text(src, encoding="utf-8")
    return tmp_path


def test_bar_catches_a_coordinator_tier_import(tmp_path):
    """Mutation proof: a coordinator-tier package reached by a process check is
    CAUGHT — the distinction this module exists to draw."""
    tree = _fixture_tree(
        tmp_path,
        {
            "trace.py": "import os\nimport helper\n",
            "helper.py": "import pandas\n",  # indirect — the transitive case
        },
    )
    rows = [{"name": "pandas", "kind": "python", "tier": "coordinator", "ruled": "R-9"}]
    bad = shipped_bar_violations(tree, {"trace"}, rows)
    assert "pandas" in bad and "coordinator" in bad["pandas"]
    assert "helper" in bad["pandas"]  # attributed to the file that imports it


def test_bar_catches_an_unruled_shipped_import(tmp_path):
    """Mutation proof: Tier=shipped with no owner ruling is still a failure."""
    tree = _fixture_tree(tmp_path, {"trace.py": "import yaml\n"})
    rows = [{"name": "yaml", "kind": "python", "tier": "shipped", "ruled": ""}]
    bad = shipped_bar_violations(tree, {"trace"}, rows)
    assert "yaml" in bad and "owner ruling" in bad["yaml"]


def test_bar_catches_an_undeclared_import(tmp_path):
    """Mutation proof: no ledger row at all is caught, naming the ledger."""
    tree = _fixture_tree(tmp_path, {"trace.py": "import requests\n"})
    bad = shipped_bar_violations(tree, {"trace"}, [])
    assert "requests" in bad and "docs/dependencies.md" in bad["requests"]


def test_a_ruled_shipped_dependency_passes(tmp_path):
    """The bar is a bar, not a ban: a properly ruled shipped row is allowed, so
    the check cannot be mistaken for the stdlib-only rule it replaced."""
    tree = _fixture_tree(tmp_path, {"trace.py": "import tomlkit\nimport os\n"})
    rows = [
        {"name": "tomlkit", "kind": "python", "tier": "shipped", "ruled": "R-7, 2026"}
    ]
    assert shipped_bar_violations(tree, {"trace"}, rows) == {}


def test_stdlib_and_siblings_are_never_flagged(tmp_path):
    """A sibling import is traversed, not reported; stdlib is ignored."""
    tree = _fixture_tree(
        tmp_path,
        {"trace.py": "import json\nimport sibling\n", "sibling.py": "import pathlib\n"},
    )
    assert shipped_bar_violations(tree, {"trace"}, []) == {}
