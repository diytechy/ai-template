"""The design rows' module keys: a `Module` cell listing several modules joined
by `;` contributes one key per module.

The interface tier's reachability advisory this module was written for (a
module-shaped owner named by no design row and declaring no `Implements:`
line) retired when interface owners became component ids (WI-1022): no owner
is a module any more. The module-key reading it relied on stays, for the
performance-budget back-links that still read it. In memory: no scaffold, no
subprocess, no git.
"""

import pytest
from conftest import load_script


@pytest.fixture(scope="module")
def coherence():
    return load_script("coherence")


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
