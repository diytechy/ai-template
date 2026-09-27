"""The interface tier's reachability advisory: an owner reached either way is
silent, and an owner reached neither way still warns.

`trace.interface_findings` warns when a module-shaped owner is named by no
design row's `Module` and declares no `Implements:` line. Two readings made it
fire on owners that ARE traced: a `Module` cell listing several modules joined
by `;` was taken whole (one unusable key instead of one per module), and the
`Implements:` scan joined the declared source root to paths that already start
from its parent (`scripts/scripts/<mod>` keys that match no owner). Each way of
reaching the spine gets its own fixture here, so a regression in one cannot
hide behind the other. In memory apart from a few files under `tmp_path`: no
scaffold, no subprocess, no git.
"""

import pytest
from conftest import load_script


@pytest.fixture(scope="module")
def trace():
    return load_script("trace")


@pytest.fixture(scope="module")
def coherence():
    return load_script("coherence")


def _if_row(owner, iid="IF-001"):
    return {"IF-ID": iid, "Owner": owner, "Consumers": "scripts/reader"}


def _reach_advisories(trace, ifs, module_ids, root=None):
    _findings, advisories = trace.interface_findings(ifs, module_ids, root)
    return [a for a in advisories if "traces to no requirement" in a]


def test_a_joined_module_cell_contributes_one_key_per_module(coherence):
    llrs = [
        {"LLR-ID": "LLR-001", "Module": "scripts/a.py; scripts/b.py"},
        {"LLR-ID": "LLR-002", "Module": "scripts/c.py"},
        {"LLR-ID": "LLR-003", "Module": ""},
    ]
    assert coherence.llr_module_ids(llrs) == {
        "scripts/a.py",
        "scripts/b.py",
        "scripts/c.py",
    }


def test_an_owner_named_only_inside_a_joined_module_cell_is_reached(trace, coherence):
    llrs = [{"LLR-ID": "LLR-001", "Module": "scripts/a.py;scripts/b.py"}]
    module_ids = coherence.llr_module_ids(llrs)
    assert _reach_advisories(trace, [_if_row("scripts/b")], module_ids) == []


def _src_tree(root, body):
    """A repo whose declared source root sits two levels deep, the kit's own
    shape (`project-trajectory/scripts`), holding one module `c.py`."""
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "stack.ini").write_text(
        "[paths]\nsrc = project-trajectory/scripts\n", encoding="utf-8"
    )
    src = root / "project-trajectory" / "scripts"
    src.mkdir(parents=True, exist_ok=True)
    (src / "c.py").write_text(body, encoding="utf-8")
    return root


def test_an_owner_reached_only_through_an_implements_header_is_reached(trace, tmp_path):
    root = _src_tree(tmp_path, '"""A module.\n\nImplements: SR-001, LLR-001\n"""\n')
    # A design row names some OTHER module, so the advisory is armed and the
    # header is the only way this owner reaches the spine.
    module_ids = {"project-trajectory/scripts/other.py"}
    assert _reach_advisories(trace, [_if_row("scripts/c")], module_ids, root) == []


def test_an_owner_reached_neither_way_still_warns(trace, coherence, tmp_path):
    root = _src_tree(tmp_path, '"""A module with no back-link."""\n')
    llrs = [{"LLR-ID": "LLR-001", "Module": "scripts/a.py;scripts/b.py"}]
    found = _reach_advisories(
        trace, [_if_row("scripts/c")], coherence.llr_module_ids(llrs), root
    )
    assert len(found) == 1 and "IF IF-001 owner 'scripts/c'" in found[0]
