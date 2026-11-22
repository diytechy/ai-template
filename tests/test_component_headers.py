"""The `Component:` header: its grammar, its one reader, the census over the
closed scope, and component membership read from it (WI-1021, variant F's
first row).

A file names its one component on one line of the header that holds its
`Contracts:` marker. `gen_arch_map.file_component` reads it through each file
type's carrier; `arch_inputs.component_headers` walks the scope and reports
every file whose declaration is absent, doubled, malformed or names no live
component row; `kitlib.spine.module_components` turns the declarations into
the membership the cross-component rule, the top view and the component view
read. A file with no valid declaration belongs to no component, and an import
edge touching it is reported as unclassified, never treated as internal or
exempt.
"""

import pytest

from conftest import load_script

gen_arch_map = load_script("gen_arch_map")
arch_inputs = load_script("arch_inputs")
arch_seams = load_script("arch_seams")
arch_components = load_script("arch_components")


@pytest.fixture(autouse=True)
def _fresh_scan(monkeypatch):
    """The seam rule caches its scan per root path, and pytest reuses a passed
    test's directory name, so each case starts from an empty cache."""
    monkeypatch.setattr(arch_seams, "_SCAN_CACHE", {})


def _write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))
    return path


def _repo(root, files, cmps=("CMP-001", "CMP-002"), ifs=""):
    """A repository with `[paths] src = scripts`, the component rows `cmps`,
    the interface rows `ifs` (TOML text) and `files` ({repository path: text})."""
    _write(root, "docs/stack.ini", "[paths]\nsrc = scripts\n")
    _write(
        root,
        "docs/requirements/components.toml",
        "".join(
            '[component.{}]\nname = "{}"\ncategory = "software"\n'
            'status = "Accepted"\n\n'.format(cid, cid)
            for cid in cmps
        ),
    )
    if ifs:
        _write(root, "docs/requirements/interfaces.toml", ifs)
    for rel, text in files.items():
        _write(root, rel, text)


def _mod(component=None, body=""):
    """A Python module whose docstring declares `component` (none when None)."""
    doc = "A module." + ("\n\nComponent: {}\n".format(component) if component else "")
    return '"""{}"""\n{}'.format(doc, body)


# --- the grammar and its one reader (LLR-396) ---------------------------------

CARRIERS = [
    ("mod.py", '"""Summary.\n\nComponent: CMP-002\n\nMore prose.\n"""\nX = 1\n'),
    ("run.sh", "#!/bin/sh\n# Component: CMP-002\n#\n# Runs.\necho hi\n"),
    ("run.command", "#!/bin/sh\n# Component: CMP-002\nexec ./run.sh\n"),
    ("run.ps1", "# Component: CMP-002\n# Runs.\nWrite-Host hi\n"),
    ("conf.toml", "# A table.\n# Component: CMP-002\n[a]\nb = 1\n"),
    ("conf.ini", "# Component: CMP-002\n[a]\nb = 1\n"),
    ("rows.csv", "# Component: CMP-002\nA,B\n1,2\n"),
    ("pre-commit", "#!/bin/sh\n# Component: CMP-002\nexit 0\n"),
    ("run.cmd", "@echo off\r\nREM Component: CMP-002\r\nsetlocal\r\n"),
    ("doc.md", "<!--\nComponent: CMP-002\n-->\n\n# Doc\n"),
]


def test_each_carrier_declares_through_its_own_comment_syntax(tmp_path):
    """Implements: TC-457"""
    for name, text in CARRIERS:
        path = _write(tmp_path, name, text)
        assert gen_arch_map.file_component(path) == ("CMP-002", None), name


MALFORMED = [
    "Component:CMP-002",
    "component: CMP-002",
    "Component: CMP-002 (the gatekeeper)",
    "Component: CMP-002, CMP-003",
    "Component: cmp-002",
    "COMPONENT: CMP-002",
]


def test_a_line_shaped_like_a_declaration_but_not_exact_is_malformed(tmp_path):
    """Implements: TC-457"""
    for i, line in enumerate(MALFORMED):
        text = '"""A module.\n\n{}\n"""\n'.format(line)
        path = _write(tmp_path, "m{}.py".format(i), text)
        component, problem = gen_arch_map.file_component(path)
        assert component is None, line
        assert "is not a declaration" in problem and line in problem, line


def test_a_malformed_line_beside_an_exact_one_leaves_the_file_undeclared(tmp_path):
    """Implements: TC-457"""
    path = _write(
        tmp_path, "m.sh", "#!/bin/sh\n# Component: CMP-001\n# component: CMP-002\n"
    )
    component, problem = gen_arch_map.file_component(path)
    assert component is None and "is not a declaration" in problem


def test_two_declarations_are_doubled_even_naming_one_id(tmp_path):
    """Implements: TC-457"""
    two = _write(
        tmp_path, "two.py", '"""M.\n\nComponent: CMP-001\n\nComponent: CMP-002\n"""\n'
    )
    same = _write(tmp_path, "same.toml", "# Component: CMP-001\n# Component: CMP-001\n")
    for path in (two, same):
        component, problem = gen_arch_map.file_component(path)
        assert component is None
        assert "declares 2 components" in problem


OUTSIDE = [
    ("comment.py", '"""A module."""\n# Component: CMP-001\n'),
    ("late.py", '"""A module."""\nX = """\nComponent: CMP-001\n"""\n'),
    ("empty.py", ""),
    ("below.sh", "#!/bin/sh\necho hi\n# Component: CMP-001\n"),
    ("body.md", "<!-- A header. -->\n\nComponent: CMP-001\n"),
    ("prose.toml", "# The Component: CMP-001 line, mid-line.\n"),
    ("help.ps1", "<#\n.SYNOPSIS\n    Help.\nComponent: CMP-001\n#>\nWrite-Host\n"),
    ("colon.cmd", "@echo off\r\n:: Component: CMP-001\r\nsetlocal\r\n"),
]


def test_a_declaration_outside_the_carrier_declares_nothing(tmp_path):
    """A comment below a module's docstring, a later string, a line below the
    top-of-file comment block, Markdown outside the opening comment, a
    declaration mid-line, a PowerShell help block and a batch file's `::`
    line are not the header's declaring carrier, so the file is absent: the
    grammar names a `#` line for PowerShell and a `REM` line for batch.

    Implements: TC-457"""
    for name, text in OUTSIDE:
        path = _write(tmp_path, name, text)
        component, problem = gen_arch_map.file_component(path)
        assert component is None and "declares no component" in problem, name


# --- the scope and the census (LLR-397) ----------------------------------------


def test_the_census_names_every_finding_class_and_keeps_the_valid_ones(tmp_path):
    """Implements: TC-458"""
    _repo(
        tmp_path,
        {
            "scripts/ok.py": _mod("CMP-001"),
            "scripts/none.py": _mod(),
            "scripts/two.sh": "# Component: CMP-001\n# Component: CMP-002\n",
            "scripts/bad.cmd": "@echo off\r\nREM Component: CMP-1 and more\r\n",
            "scripts/ghost.ps1": "# Component: CMP-099\n",
            "scripts/example.ini": "# Component: CMP-000\n",
        },
    )
    declared, findings = arch_inputs.component_headers(tmp_path)
    assert declared == {"scripts/ok.py": "CMP-001"}
    text = "\n".join(findings)
    assert len(findings) == 5, text
    assert "scripts/none.py: declares no component" in text
    assert "scripts/two.sh: declares 2 components (CMP-001, CMP-002)" in text
    assert "scripts/bad.cmd: `Component: CMP-1 and more` is not a declaration" in text
    assert "scripts/ghost.ps1: declares CMP-099, which no live component row" in text
    assert "scripts/example.ini: declares CMP-000, which no live component row" in text


def test_the_scope_is_the_grammars_types_under_src_and_the_listed_headers(tmp_path):
    """`README.md` is documentation; a hidden directory and `__pycache__` are
    not source; a file of another type is outside the rule until it states a
    contract body; a file `[arch-map] headers` lists is in, a directory
    README outside the source root and a README under it among them; a listed
    path that is no file is a finding; a file nothing scopes is not walked,
    whatever it carries.

    Implements: TC-458"""
    _repo(
        tmp_path,
        {
            "scripts/ok.py": _mod("CMP-001"),
            "scripts/README.md": "<!--\nComponent: CMP-001\n-->\n",
            "scripts/.hidden/x.py": _mod(),
            "scripts/__pycache__/x.py": _mod(),
            "scripts/data.json": "{}\n",
            "scripts/lib.rs": "// Contracts: IF-001\n// Contract IF-001: a body.\n",
            "docs/config.toml": "# Contracts: IF-001\n[a]\n",
            "docs/notes/README.md": "<!-- Contracts: IF-002 -->\n",
            "docs/other.toml": "# component: CMP-001 malformed, unscoped\n",
        },
    )
    _write(
        tmp_path,
        "docs/stack.ini",
        "[paths]\nsrc = scripts\n[arch-map]\nheaders = docs/config.toml "
        "docs/notes/README.md scripts/README.md docs/missing.ini\n",
    )
    declared, findings = arch_inputs.component_headers(tmp_path)
    assert declared == {"scripts/ok.py": "CMP-001", "scripts/README.md": "CMP-001"}
    assert sorted(f.split(":")[0] for f in findings) == [
        "docs/config.toml",
        "docs/missing.ini",
        "docs/notes/README.md",
        "scripts/lib.rs",
    ], findings
    rs = [f for f in findings if f.startswith("scripts/lib.rs")][0]
    assert "`.rs`" in rs and "contract body" in rs


def test_the_census_is_vacuous_with_no_live_component_row(tmp_path):
    """Implements: TC-458"""
    _repo(tmp_path, {"scripts/none.py": _mod()}, cmps=("CMP-000",))
    assert arch_inputs.component_headers(tmp_path) == ({}, [])


def test_the_census_rides_the_component_rules_and_their_opt_out(tmp_path):
    """Implements: TC-458"""
    _repo(tmp_path, {"scripts/none.py": _mod()})
    assert any(
        "scripts/none.py: declares no component" in f
        for f in arch_components.component_findings(tmp_path)
    )
    _write(tmp_path, "docs/process.toml", "[checks]\ncomponents_check = false\n")
    assert arch_components.component_findings(tmp_path) == []


# --- membership read from the declarations (LLR-373, LLR-067) ------------------


def test_the_top_view_reads_the_headers_and_not_the_design_rows(tmp_path):
    """Implements: TC-459"""
    _repo(
        tmp_path,
        {
            "scripts/a.py": _mod("CMP-001", "def f():\n    pass\n"),
            "scripts/b.py": _mod(None, "def g():\n    pass\n"),
            "docs/requirements/low-level-requirements.toml": (
                '[design.LLR-001]\nsr_refs = ["SR-001"]\n'
            ),
        },
    )
    view = arch_components.component_top_view(tmp_path)
    assert view["module_cmps"]["scripts/a"] == {"CMP-001"}
    assert view["module_cmps"]["scripts/b"] == set()
    assert view["uncontained"] == ["scripts/b"]


IMPORTER = "import b\n\n\ndef f():\n    return b\n"
TARGET = "def g():\n    pass\n"


def _edge_repo(root, a_cmp, b_cmp, ifs="", kernel=False, b_extra=None):
    files = {
        "scripts/a.py": _mod(a_cmp, IMPORTER),
        "scripts/b.py": _mod(b_cmp, TARGET),
    }
    if b_extra:
        files.update(b_extra)
    if kernel:
        files["docs/kernel-modules-allow"] = "scripts/b.py — the fixture's kernel\n"
    _repo(root, files, ifs=ifs)


COVER = (
    '[interface.IF-001]\nowner = "CMP-002"\nrequestors = ["CMP-001"]\n'
    'channel = "call"\ndata = "g()"\n'
)


UNDECLARED = {
    "target-undeclared": ("CMP-001", None, "", False, None),
    "importer-undeclared": (None, "CMP-002", "", False, None),
    "covered": ("CMP-001", None, COVER, False, None),
    "kernel": ("CMP-001", None, "", True, None),
    # `b.sh` shares `b.py`'s module key but is no import's endpoint.
    "shell-on-the-key": (
        "CMP-001",
        None,
        "",
        False,
        {"scripts/b.sh": "# Component: CMP-001\n"},
    ),
}


def test_an_edge_touching_an_undeclared_module_is_unclassified(tmp_path):
    """The Trust ruling: the edge is reported before the cover and the kernel
    are read, so neither can make it internal or exempt; nor can a declared
    file of another type that shares the module's key.

    Implements: TC-459"""
    for case, (a_cmp, b_cmp, ifs, kernel, extra) in UNDECLARED.items():
        root = tmp_path / case
        _edge_repo(root, a_cmp, b_cmp, ifs=ifs, kernel=kernel, b_extra=extra)
        findings = arch_seams.cross_component_findings(root)
        assert len(findings) == 1, (case, findings)
        assert "scripts/a" in findings[0] and "scripts/b" in findings[0], case
        assert "unclassified" in findings[0], case


def test_a_key_two_files_share_silences_no_edge(tmp_path):
    """`check.py` and `check.sh` meet on one module key. A second component on
    the key used to make the edge's component sets overlap, which silenced it;
    an edge is internal only when both ends sit in the same one component.

    Implements: TC-459"""
    _edge_repo(
        tmp_path,
        "CMP-002",
        "CMP-001",
        b_extra={"scripts/b.sh": "# Component: CMP-002\n"},
    )
    findings = arch_seams.cross_component_findings(tmp_path)
    assert len(findings) == 1 and "has no declared IF-### seam" in findings[0]


def test_an_edge_inside_one_component_is_silent_and_the_advisory_is_gone(tmp_path):
    """Implements: TC-459"""
    _edge_repo(tmp_path, "CMP-001", "CMP-001")
    assert arch_seams.cross_component_findings(tmp_path) == []
    assert not hasattr(arch_seams, "cross_component_advisories")
