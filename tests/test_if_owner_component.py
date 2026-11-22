"""Interface rows name components, not files (WI-1022, variant F's second row).

An interface row's `owner` is a live `CMP-###` id or an `external:` party the
registry header declares, and its `consumers` and `requestors` hold only those
forms (`trace.py`, LLR-041). At most one file on the declared scan surface
states each `Contract IF-###:` body, and that file's `Component:` header names
the owner, or, for an `external:`-owned row, a component on its far side
(`arch_interfaces`, LLR-398). An import between components is covered only by
a `call` row owned by the imported file's component naming the importer's
(`arch_seams`, LLR-067). A row's place in the component view is derived from
its endpoints (`gen_components`, LLR-199), and the interface-form gate reaches
a requirement through the file stating the row's body (`assumption_rules`,
LLR-244).
"""

import pytest

from conftest import load_script

trace = load_script("trace")
trace_text = load_script("trace_text")
arch_inputs = load_script("arch_inputs")
arch_interfaces = load_script("arch_interfaces")
arch_seams = load_script("arch_seams")
gen_components = load_script("gen_components")
assumption_rules = load_script("assumption_rules")
spine_carrier = load_script("spine_carrier")


@pytest.fixture(autouse=True)
def _fresh_scan(monkeypatch):
    """The seam rule caches its scan per root path."""
    monkeypatch.setattr(arch_seams, "_SCAN_CACHE", {})


def _write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))
    return path


PARTIES = "# External party: git\n# External party: downstream adopter\n"


def _repo(root, files, ifs="", headers=(), cmps=("CMP-001", "CMP-002")):
    """A repository with `[paths] src = scripts`, `[arch-map] headers`, the
    component rows `cmps`, the interface rows `ifs` (TOML text, under the
    party lines) and `files` ({repository path: text})."""
    stack = "[paths]\nsrc = scripts\n"
    if headers:
        stack += "[arch-map]\nheaders = {}\n".format(" ".join(headers))
    _write(root, "docs/stack.ini", stack)
    _write(
        root,
        "docs/requirements/components.toml",
        "".join(
            '[component.{}]\nname = "{}"\ncategory = "software"\n'
            'status = "Accepted"\n\n'.format(cid, cid)
            for cid in cmps
        ),
    )
    _write(root, "docs/requirements/interfaces.toml", PARTIES + "\n" + ifs)
    for rel, text in files.items():
        _write(root, rel, text)


def _mod(component, contracts="", body="X = 1\n"):
    """A Python module declaring `component`, with a `Contracts:` paragraph
    (`contracts` is the paragraph's text, ids and bodies) when given."""
    doc = (
        "A module.\n\nComponent: {}\n".format(component) if component else "A module.\n"
    )
    if contracts:
        doc += "\n" + contracts
    return '"""{}"""\n{}'.format(doc, body)


def _row(iid, owner, far, key="requestors", channel="call"):
    return '[interface.{}]\nowner = "{}"\n{} = [{}]\nchannel = "{}"\n\n'.format(
        iid, owner, key, ", ".join('"{}"'.format(e) for e in far), channel
    )


# --- the endpoint form and the party list (LLR-041) -----------------------------


def _the_party_list_is_read_from_the_registry_header_only():
    text = (
        "# A registry.\n#\n# External party: git\n"
        "#   External party:   downstream adopter  \n"
        "# prose naming `external:coordinator` mid-line declares nothing\n"
        "\n[interface.IF-001]\n# External party: after the first table\n"
    )
    assert trace_text.declared_parties(text) == frozenset({"git", "downstream adopter"})
    assert trace_text.declared_parties("") == frozenset()


ENDPOINTS = {
    "CMP-001": None,
    "external:git": None,
    "scripts/check": "is not a component id or an `external:` party",
    "docs/stack.ini": "is not a component id or an `external:` party",
    "LLR-041": "names a requirement or design id",
    "CMP-099": "names no live component row",
    "external:coordinator": "names a party the registry header does not declare",
    "external:": "names no party",
}


def _each_endpoint_form_and_its_finding():
    for endpoint, problem in ENDPOINTS.items():
        got = trace_text.endpoint_problem(endpoint, {"CMP-001"}, {"git"})
        if problem is None:
            assert got is None, endpoint
        else:
            assert got and problem in got, (endpoint, got)


def _ifs(root, body):
    _write(root, "docs/requirements/interfaces.toml", PARTIES + "\n" + body)
    return spine_carrier.load(root / "docs/requirements/interfaces.toml", "IF-ID")


def _every_endpoint_cell_is_judged_and_a_clean_row_is_silent(tmp_path):
    """The owner and each far-side entry are held to the forms; a path in
    any of them is a strict finding naming the row and the cell."""
    rows = _ifs(
        tmp_path,
        _row("IF-001", "CMP-001", ["CMP-002", "external:git"])
        + _row("IF-002", "scripts/check", ["CMP-002"])
        + _row("IF-003", "CMP-001", ["scripts/trace"], key="consumers", channel="file")
        + _row("IF-004", "CMP-001", ["external:coordinator"], channel="cli"),
    )
    parties = frozenset({"git", "downstream adopter"})
    findings, _adv = trace.interface_findings(
        rows, {"CMP-001", "CMP-002"}, parties, tmp_path
    )
    text = "\n".join(findings)
    assert "IF-001" not in text, text
    assert "IF IF-002 Owner='scripts/check'" in text
    assert "IF IF-003 Consumers='scripts/trace'" in text
    assert "IF IF-004 Requestors='external:coordinator'" in text
    assert len(findings) == 3, text


def _an_all_external_row_stays_refused_and_the_component_cell_is_retired(tmp_path):
    rows = _ifs(
        tmp_path,
        _row("IF-001", "external:git", ["external:downstream adopter"], channel="git")
        + _row("IF-002", "CMP-001", ["CMP-002"]).rstrip("\n")
        + '\ncomponent = "CMP-001"\n\n',
    )
    parties = frozenset({"git", "downstream adopter"})
    findings, _adv = trace.interface_findings(
        rows, {"CMP-001", "CMP-002"}, parties, tmp_path
    )
    text = "\n".join(findings)
    assert "IF IF-001 has no in-tree endpoint" in text
    assert "component" in text and "IF-002" in text
    assert len(findings) == 2, text


# --- one body per interface (LLR-398) --------------------------------------------

BODY = "Contracts: IF-001 — the seam.\n\nContract IF-001: the form.\n"


def _bodies(root, files, ifs=None, headers=()):
    _repo(
        root,
        files,
        ifs=_row("IF-001", "CMP-001", ["CMP-002"]) if ifs is None else ifs,
        headers=headers,
    )
    return arch_interfaces.contract_body_findings(root)


def _zero_bodies_is_valid_and_one_in_the_owners_file_is_clean(tmp_path):
    """Zero bodies is the pre-build state, the row's `data` cell the
    contract's home, for an `external:`-owned row too."""
    ext = _row("IF-001", "external:git", ["CMP-002"], key="consumers", channel="git")
    assert _bodies(tmp_path / "zero", {"scripts/a.py": _mod("CMP-001")}) == []
    assert _bodies(tmp_path / "ext", {"scripts/a.py": _mod("CMP-002")}, ext) == []
    assert _bodies(tmp_path / "one", {"scripts/a.py": _mod("CMP-001", BODY)}) == []


def _a_body_in_another_components_file_is_a_finding(tmp_path):
    out = _bodies(tmp_path, {"scripts/b.py": _mod("CMP-002", BODY)})
    assert len(out) == 1, out
    assert "IF-001" in out[0] and "CMP-001" in out[0] and "CMP-002" in out[0]
    assert "scripts/b.py" in out[0]
    none = _bodies(tmp_path / "none", {"scripts/b.py": _mod(None, BODY)})
    assert len(none) == 1 and "no component" in none[0], none


def _two_bodies_are_one_finding_naming_both_files(tmp_path):
    out = _bodies(
        tmp_path,
        {
            "scripts/a.py": _mod("CMP-001", BODY),
            "scripts/c.sh": "# Component: CMP-001\n# "
            + BODY.replace("\n", "\n# ")
            + "\n",
        },
    )
    assert len(out) == 1, out
    assert "IF-001" in out[0] and "scripts/a.py" in out[0] and "scripts/c.sh" in out[0]
    assert "2 files" in out[0]


def _an_external_owned_body_sits_in_a_far_side_component(tmp_path):
    ifs = _row("IF-001", "external:git", ["CMP-002"], key="consumers", channel="git")
    assert _bodies(tmp_path / "far", {"scripts/b.py": _mod("CMP-002", BODY)}, ifs) == []
    out = _bodies(tmp_path / "near", {"scripts/a.py": _mod("CMP-001", BODY)}, ifs)
    assert len(out) == 1 and "external:git" in out[0] and "CMP-001" in out[0], out


def _a_declaration_with_no_body_is_still_a_finding(tmp_path):
    out = _bodies(tmp_path, {"scripts/a.py": _mod("CMP-001", "Contracts: IF-001\n")})
    assert len(out) == 1 and "states no `Contract IF-001:` body" in out[0], out


def _the_surface_is_the_source_root_and_the_declared_headers(tmp_path):
    """A listed configuration file is read; a body quoted in a review record,
    a plan or the approval snapshot is outside the surface and is never a
    second body."""
    quoted = "<!--\nContracts: IF-001\n\nContract IF-001: a quoted copy.\n-->\n"
    files = {
        "scripts/a.py": _mod("CMP-001", BODY),
        "docs/reviews/r.md": quoted,
        "docs/plans/p.md": quoted,
        "docs/archive/last_accepted/docs/requirements/interfaces.toml": (
            "# Contracts: IF-001\n#\n# Contract IF-001: the snapshot.\n"
        ),
    }
    assert _bodies(tmp_path / "out", files) == []
    files["docs/conf.toml"] = (
        "# Component: CMP-002\n#\n# Contracts: IF-001\n#\n# Contract IF-001: a copy.\n"
    )
    out = _bodies(tmp_path / "in", files, headers=("docs/conf.toml",))
    assert len(out) == 1 and "docs/conf.toml" in out[0] and "2 files" in out[0], out


def test_each_endpoint_takes_one_of_two_forms(tmp_path):
    """The party list, each endpoint form and its finding, every endpoint
    cell judged, the all-external refusal and the retired cell.

    Implements: TC-462"""
    _the_party_list_is_read_from_the_registry_header_only()
    _each_endpoint_form_and_its_finding()
    _every_endpoint_cell_is_judged_and_a_clean_row_is_silent(tmp_path / "cells")
    _an_all_external_row_stays_refused_and_the_component_cell_is_retired(
        tmp_path / "external"
    )


def test_one_body_per_interface_in_a_file_of_the_right_component(tmp_path):
    """Zero, one and two bodies, the local and external header rules, a
    declaration with no body and the scan surface's edges.

    Implements: TC-463"""
    _zero_bodies_is_valid_and_one_in_the_owners_file_is_clean(tmp_path / "zero")
    _a_body_in_another_components_file_is_a_finding(tmp_path / "other")
    _two_bodies_are_one_finding_naming_both_files(tmp_path / "two")
    _an_external_owned_body_sits_in_a_far_side_component(tmp_path / "far")
    _a_declaration_with_no_body_is_still_a_finding(tmp_path / "undeclared")
    _the_surface_is_the_source_root_and_the_declared_headers(tmp_path / "surface")


# --- the stricter cover (LLR-067) ------------------------------------------------

IMPORTER = "import b\n\n\ndef f():\n    return b\n"


def _cover(root, ifs):
    _repo(
        root,
        {
            "scripts/a.py": _mod("CMP-001", body=IMPORTER),
            "scripts/b.py": _mod("CMP-002", body="def g():\n    pass\n"),
        },
        ifs=ifs,
    )
    return arch_seams.cross_component_findings(root)


def test_only_a_call_row_owned_by_the_imported_component_naming_the_importer_covers(
    tmp_path,
):
    """Implements: TC-464"""
    assert _cover(tmp_path / "cover", _row("IF-001", "CMP-002", ["CMP-001"])) == []
    uncovered = {
        "none": "",
        "reversed": _row("IF-001", "CMP-001", ["CMP-002"]),
        "a file row": _row("IF-001", "CMP-002", ["CMP-001"], "consumers", "file"),
        "a cli row": _row("IF-001", "CMP-002", ["CMP-001"], channel="cli"),
    }
    for case, ifs in uncovered.items():
        out = _cover(tmp_path / case.replace(" ", "-"), ifs)
        assert len(out) == 1 and "has no declared IF-### seam" in out[0], (case, out)


# --- placement in the views (LLR-199) --------------------------------------------


def test_a_row_is_internal_to_the_lowest_component_enclosing_every_endpoint():
    """Implements: TC-465"""
    parents = {"CMP-003": ["CMP-001"], "CMP-004": ["CMP-001"]}

    def place(owner, far, key="Requestors"):
        row = {"Owner": owner, key: "; ".join(far)}
        return gen_components.seam_placement(row, parents)

    assert place("CMP-001", ["CMP-001"]) == ({"CMP-001"}, {"CMP-001"})
    assert place("CMP-001", ["CMP-002"]) == ({"CMP-001", "CMP-002"}, set())
    assert place("CMP-001", ["external:git"], "Consumers") == ({"CMP-001"}, set())
    placed, internal = place("CMP-003", ["CMP-004"])
    assert placed == {"CMP-001", "CMP-003", "CMP-004"} and internal == {"CMP-001"}


# --- the interface-form gate's reach (LLR-244) -----------------------------------


def test_a_boundary_row_reaches_requirements_through_the_file_stating_its_body():
    """Implements: TC-466"""
    ifs = [
        {"IF-ID": "IF-001", "Owner": "CMP-001", "InterfaceToExternal": "B-01"},
        {"IF-ID": "IF-002", "Owner": "CMP-001", "InterfaceToExternal": "B-01"},
        {"IF-ID": "IF-003", "Owner": "CMP-001"},
    ]
    llrs = [
        {
            "LLR-ID": "LLR-001",
            "Module": "project-trajectory/scripts/a.py",
            "SR-Refs": "SR-001",
        },
        {"LLR-ID": "LLR-002", "Module": "scripts/b.py", "SR-Refs": "SR-002"},
    ]
    homes = {"IF-001": "project-trajectory/scripts/a.py", "IF-003": "scripts/b.py"}
    assert assumption_rules.if_reached_srs(ifs, llrs, homes) == {
        "IF-001": ["SR-001"],
        "IF-002": [],
    }
    # With no scanned source (`files` mode) there are no homes: each boundary
    # row reaches the requirements of the design rows placed in its owner.
    llrs[1]["Component"] = "CMP-001"
    assert assumption_rules.if_reached_srs(ifs, llrs, None) == {
        "IF-001": ["SR-002"],
        "IF-002": ["SR-002"],
    }


# --- connectivity over components (LLR-042) --------------------------------------


def test_connectivity_warns_name_components_not_modules(tmp_path):
    """Implements: TC-467"""
    _repo(
        tmp_path,
        {
            "scripts/a.py": _mod("CMP-001", body="def f():\n    pass\n"),
            "scripts/b.py": _mod("CMP-002", body="def g():\n    pass\n"),
        },
        ifs=_row("IF-001", "CMP-002", ["external:git"], channel="cli"),
    )
    out = arch_interfaces.interface_findings(tmp_path)
    text = "\n".join(out)
    assert "component 'CMP-001'" in text and "no IF-### row names it" in text
    assert "component 'CMP-002' declares no Consumes seam" in text
    assert "module " not in text, text
