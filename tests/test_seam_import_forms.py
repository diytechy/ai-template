"""The seam check's import resolution: every form of internal import reaches the
cross-component rule as its inventory module, or is skipped (WI-1003).

`gen_arch_map.internal_imports` writes each import as a token: a bare stem
(`helper`), a dotted path (`kitlib.spine`) or a relative path (`.spine`). The
rule used to look the whole token up by its last segment, so every dotted and
relative token missed and the edges into a package went unchecked. One resolver,
`gen_arch_map.resolve_import`, now answers for the rule and for the dependency
diagram. Each case below adds one importer tagged CMP-001 to a fixture tree whose
other modules are CMP-002, and runs the rule in process: a resolved form reports
the cross-component finding naming its target; a skipped form reports nothing for
its importer.

Implements: TC-436
"""

import types

import pytest

from conftest import load_script

trajectory_arch = load_script("trajectory_arch")
gen_arch_map = load_script("gen_arch_map")

SPINE = (
    '"""Spine."""\n\n\ndef go():\n    """Go."""\n\n\ndef helper():\n    """Help."""\n'
)
# The fixture tree under the scan root `scripts`. `kitlib/deep/__init__.py` and
# `blank.py` are empty, so the walk sees their names but the inventory skips them.
TREE = {
    "kitlib/__init__.py": '"""Package."""\n',
    "kitlib/spine.py": SPINE,
    "kitlib/deep/__init__.py": "",
    "helper.py": '"""Helper."""\n',
    "a/pkg/util.py": '"""Util A."""\n',
    "b/pkg/util.py": '"""Util B."""\n',
    "blank.py": "",
}


def _tree(root, importer, statement):
    """Write the fixture tree with `importer` holding `statement`, its
    component tags and its scan profile; return the importer's module key."""
    files = dict(TREE)
    files[importer] = '"""Importer."""\n\n{}\n'.format(statement)
    for rel, text in files.items():
        path = root / "scripts" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    key = "scripts/" + importer[: -len(".py")].replace("/__init__", "")
    req = root / "docs" / "requirements"
    req.mkdir(parents=True)
    (root / "docs" / "stack.ini").write_text(
        "[paths]\nsrc = scripts\n", encoding="utf-8"
    )
    (req / "components.csv").write_text(
        "CMP-ID,Name\nCMP-001,A\nCMP-002,B\n", encoding="utf-8"
    )
    rows = "".join(
        "LLR-{:03d},SR-001,T,scripts/{},,d,(see TC),Accepted,{}\n".format(
            i + 1, rel, "CMP-001" if rel == importer else "CMP-002"
        )
        for i, rel in enumerate(sorted(files))
        if files[rel]
    )
    (req / "low-level-requirements.csv").write_text(
        "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status,Component\n"
        + rows,
        encoding="utf-8",
    )
    return key


RESOLVED = [
    ("dotted import", "user.py", "import kitlib.spine", "scripts/kitlib/spine"),
    (
        "dotted import with an alias",
        "user.py",
        "import kitlib.spine as s",
        "scripts/kitlib/spine",
    ),
    (
        "from a package, a submodule",
        "user.py",
        "from kitlib import spine",
        "scripts/kitlib/spine",
    ),
    (
        "from a module, a symbol",
        "user.py",
        "from kitlib.spine import go",
        "scripts/kitlib/spine",
    ),
    (
        "from a module, a symbol sharing another module's stem",
        "user.py",
        "from kitlib.spine import helper",
        "scripts/kitlib/spine",
    ),
    (
        "relative, from a sibling module",
        "kitlib/user.py",
        "from .spine import go",
        "scripts/kitlib/spine",
    ),
    (
        "relative, from the package itself",
        "kitlib/user.py",
        "from . import spine",
        "scripts/kitlib/spine",
    ),
    (
        "relative, two levels",
        "kitlib/deep/user.py",
        "from .. import spine",
        "scripts/kitlib/spine",
    ),
    (
        "relative, in the package's own __init__",
        "kitlib/__init__.py",
        "from . import spine",
        "scripts/kitlib/spine",
    ),
    ("bare stem, as today", "user.py", "import helper", "scripts/helper"),
]

SKIPPED = [
    ("bare stem, ambiguous", "user.py", "import util"),
    ("dotted, ambiguous", "user.py", "import pkg.util"),
    ("unknown: scanned, not in the inventory", "user.py", "import blank"),
    ("relative, climbing past the top", "kitlib/user.py", "from ... import spine"),
]


@pytest.mark.parametrize(
    "importer, statement, target",
    [case[1:] for case in RESOLVED],
    ids=[case[0] for case in RESOLVED],
)
def test_an_import_form_reaches_the_cross_component_rule_as_its_module(
    tmp_path, importer, statement, target
):
    """Implements: TC-436"""
    src = _tree(tmp_path, importer, statement)
    findings = trajectory_arch.cross_component_findings(tmp_path)
    edge = "cross-component import {} (CMP-001) -> {} (CMP-002)".format(src, target)
    assert [f for f in findings if f.startswith(edge)], findings


@pytest.mark.parametrize(
    "importer, statement",
    [case[1:] for case in SKIPPED],
    ids=[case[0] for case in SKIPPED],
)
def test_an_unknown_or_ambiguous_import_is_skipped(tmp_path, importer, statement):
    """Implements: TC-436"""
    src = _tree(tmp_path, importer, statement)
    findings = trajectory_arch.cross_component_findings(tmp_path)
    assert not [f for f in findings if "import {} (".format(src) in f], findings


def test_an_older_generator_without_the_resolver_leaves_the_rule_silent(
    tmp_path, monkeypatch
):
    """Implements: TC-436"""
    # IF-131: every gen_arch_map entry point is optional at the call site.
    _tree(tmp_path, "user.py", "import helper")
    older = types.SimpleNamespace(scan_inventory=gen_arch_map.scan_inventory)
    monkeypatch.setattr(trajectory_arch, "gen_arch_map", older)
    assert trajectory_arch.cross_component_findings(tmp_path) == []


def test_the_dependency_diagram_resolves_through_the_same_resolver(tmp_path):
    """Implements: TC-436"""
    # The arrow the diagram's own resolver missed: a relative import written in
    # a package's __init__.py.
    _tree(tmp_path, "kitlib/__init__.py", "from . import spine")
    out = gen_arch_map.build_dependency_diagram([str(tmp_path / "scripts")])
    assert "    m_scripts_kitlib --> m_scripts_kitlib_spine\n" in out
