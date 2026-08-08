"""Dependency-ledger enforcement (concurrency-restructure §1.3, RULING-3).

The policy is "no *unargued* dependencies": every non-stdlib Python import in
`project-trajectory/scripts/` must be declared as a `Kind=python` row in
`docs/dependencies.md`. This module scans real imports with `ast` and compares
against the ledger — so adding a dependency without a reviewed ledger row is a
red suite, and deleting the ledger reds it too.

The mutation proof lives INSIDE this suite (the standing vacuous-guard rule):
`test_scanner_detects_undeclared_import` drives the scanner over a fixture
tree containing a genuinely undeclared import and asserts it is CAUGHT, so the
guard is demonstrated able to fail before it is trusted to pass.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "project-trajectory" / "scripts"
LEDGER = REPO / "docs" / "dependencies.md"

_ROW = re.compile(r"^\|\s*(?P<name>[\w.-]+)\s*\|\s*(?P<kind>\w+)\s*\|")
# Full-row form: | Name | Kind | Tier | Replaces | Why hand-rolling is worse | Ruled |
_FULL_ROW = re.compile(
    r"^\|\s*(?P<name>[\w.-]+)\s*\|\s*(?P<kind>\w+)\s*\|\s*(?P<tier>\w+)\s*\|"
    r"(?P<replaces>[^|]*)\|(?P<why>[^|]*)\|(?P<ruled>[^|]*)\|?\s*$"
)


def ledger_rows(text: str | None = None) -> list[dict]:
    """Every declared row of the ledger table as a dict.

    THE one home for the ledger's table grammar (WI-420): `ledger_declared`
    below and `tests/test_shipped_tier.py`'s adopter-facing bar both read the
    same parse, so the Kind/Tier/Ruled columns can never be read two ways.
    Keys: name, kind, tier, replaces, why, ruled — all lowercased for kind/tier,
    stripped otherwise.
    """
    text = LEDGER.read_text(encoding="utf-8") if text is None else text
    rows = []
    for line in text.splitlines():
        m = _FULL_ROW.match(line.strip())
        if not m:
            continue
        rows.append(
            {
                "name": m.group("name"),
                "kind": m.group("kind").lower(),
                "tier": m.group("tier").lower(),
                "replaces": m.group("replaces").strip(),
                "why": m.group("why").strip(),
                "ruled": m.group("ruled").strip(),
            }
        )
    return rows


def ledger_declared(kind: str, text: str | None = None) -> set[str]:
    """Names declared in the ledger table with the given Kind."""
    text = LEDGER.read_text(encoding="utf-8") if text is None else text
    names = set()
    for line in text.splitlines():
        m = _ROW.match(line.strip())
        if m and m.group("kind").lower() == kind:
            names.add(m.group("name"))
    return names


def undeclared_imports(script_dir: Path, declared: set[str]) -> dict[str, set[str]]:
    """Map of script filename -> top-level imported modules that are neither
    stdlib, nor a sibling module in script_dir, nor declared in the ledger."""
    stdlib = sys.stdlib_module_names
    siblings = {p.stem for p in script_dir.glob("*.py")}
    offenders: dict[str, set[str]] = {}
    for path in sorted(script_dir.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                tops = {alias.name.split(".")[0] for alias in node.names}
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                tops = {node.module.split(".")[0]}
            else:
                continue
            for top in tops:
                if top not in stdlib and top not in siblings and top not in declared:
                    offenders.setdefault(path.name, set()).add(top)
    return offenders


def test_kit_scripts_have_no_undeclared_python_dependency():
    declared = ledger_declared("python")
    offenders = undeclared_imports(SCRIPTS, declared)
    assert offenders == {}, (
        f"undeclared Python dependencies in kit scripts: {offenders} — "
        "either make it stdlib, or add a reviewed row to docs/dependencies.md "
        "(Kind=python) stating what it replaces and why (RULING-3)"
    )


def test_ledger_exists_and_declares_the_substrates():
    # The two system rows the restructure rulings created; their absence means
    # the ledger was gutted or the table format drifted past the parser.
    system = ledger_declared("system")
    assert "git" in system and "gh" in system


def test_scanner_detects_undeclared_import(tmp_path):
    # Mutation proof: a module importing an undeclared third-party package.
    (tmp_path / "offender.py").write_text(
        "import requests\nfrom flask import Flask\n", encoding="utf-8"
    )
    found = undeclared_imports(tmp_path, declared=set())
    assert found == {"offender.py": {"requests", "flask"}}


def test_scanner_honors_stdlib_siblings_declared_and_relative(tmp_path):
    # None of these may be flagged: stdlib, a sibling module, a declared name,
    # a relative import, or a conditional/try import of a declared name.
    (tmp_path / "sibling.py").write_text("x = 1\n", encoding="utf-8")
    (tmp_path / "clean.py").write_text(
        "import json\nimport sibling\nfrom . import anything\n"
        "try:\n    import declared_dep\nexcept ImportError:\n    declared_dep = None\n",
        encoding="utf-8",
    )
    assert undeclared_imports(tmp_path, declared={"declared_dep"}) == {}


def test_ledger_parser_reads_kind_column(tmp_path):
    # Pin the row grammar the docs table must keep: name then kind.
    text = "| foo | python | coordinator | x | y | z |\n| bar | system | shipped | a | b | c |\n"
    assert ledger_declared("python", text) == {"foo"}
    assert ledger_declared("system", text) == {"bar"}
