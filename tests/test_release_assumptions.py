"""Release recalls falsifiers without changing assumption standing."""

import sys

import pytest
from conftest import load_script

release = load_script("gen_release_checklist")


def generate(tmp_path, monkeypatch, rows=None):
    docs = tmp_path / "docs"
    if rows is not None:
        requirements = docs / "requirements"
        requirements.mkdir(parents=True)
        (requirements / "assumptions.toml").write_text(rows, encoding="utf-8")
        tests = docs / "test"
        tests.mkdir()
        (tests / "test-cases.toml").write_text(
            '[test.TC-279]\nassumption_refs = ["DA-011"]\nautomated = "Yes"\n',
            encoding="utf-8",
        )
    monkeypatch.setattr(sys, "argv", ["gen_release_checklist", "--docs", str(docs)])
    monkeypatch.setattr(release, "_rejudge_checklist_line", lambda root: "rejudge")
    release.main()
    if rows is not None:
        assert (docs / "requirements/assumptions.toml").read_text(
            encoding="utf-8"
        ) == rows
    return (docs / "release-checklist.md").read_text(encoding="utf-8")


ACTIVE = (
    '[assumption.DA-011]\nstatus = "Approved"\nstanding = "active"\n'
    'falsifier = "A reader cannot explain it."\n'
)


def test_assumptions_section_and_marker(tmp_path, monkeypatch):
    text = generate(tmp_path, monkeypatch, ACTIVE)
    assert "## 7. Assumptions" in text
    assert (
        "- [ ] ASSUMPTION DA-011 — has its falsifier been observed? "
        "A reader cannot explain it. (method: TC-279)"
    ) in text
    assert "a person sets `standing`" in text


def test_no_falsifier_is_visible_even_when_drafted(tmp_path, monkeypatch):
    text = generate(tmp_path, monkeypatch, '[assumption.DA-012]\nstatus = "Drafted"\n')
    assert "ASSUMPTION DA-012" in text
    assert "no falsifier declared" in text


@pytest.mark.parametrize(
    "old,new", [('"active"', '"falsified"'), ('"Approved"', '"Drafted"')]
)
def test_ineligible_assumptions_omitted(tmp_path, monkeypatch, old, new):
    text = generate(tmp_path, monkeypatch, ACTIVE.replace(old, new))
    assert "ASSUMPTION DA-011" not in text


def test_missing_assumptions_registry_has_no_section(tmp_path, monkeypatch):
    assert "## 7. Assumptions" not in generate(tmp_path, monkeypatch)
