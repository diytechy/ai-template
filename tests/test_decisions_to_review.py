"""Decisions to review on the owner surface (WI-790; owner direction 2026-10-04).

The `reviewed` key alone marks a delegated-decisions entry reviewed: a TOML
`true`, a non-zero number, or one of `true yes y 1 reviewed done` (any case)
hides it; an absent key, `false`, `0`, or one of `false no n 0 ""` shows it;
anything else shows it AND is a format finding, so a typo never hides a
decision. The free-text `review` note no longer marks anything reviewed.
"""

import pytest

from conftest import KIT, load_script

gen = load_script("gen_open_items")
pending = load_script("pending")
status = load_script("traj_status")
decisions = pending._kitdecisions


def _entry(eid, reviewed=None, review=""):
    line = "" if reviewed is None else "reviewed = {}\n".format(reviewed)
    return (
        '[decision.{}]\ndecided = "chose {}"\nalternative = "a"\n'
        'reversal_cost = "c"\nwhy_not_escalated = "w"\nreview = "{}"\n{}\n'.format(
            eid, eid, review, line
        )
    )


def _record(root, name, entries, high_risk=()):
    folder = root / "docs/decisions"
    folder.mkdir(parents=True, exist_ok=True)
    head = "high_risk = [{}]\n\n".format(", ".join('"{}"'.format(h) for h in high_risk))
    (folder / name).write_text(head + "".join(entries), encoding="utf-8")


def _section(root):
    page = gen.render(root)
    return page.split('id="decisions-to-review"', 1)[1].split("</section>", 1)[0]


TRUTHY = [
    "true",
    "1",
    "2.5",
    '"true"',
    '"TRUE"',
    '"yes"',
    '"Y"',
    '"1"',
    '"reviewed"',
    '"Done"',
    '" yes "',
]
FALSY = ["false", "0", '""', '"no"', '"N"', '"false"', '"0"']


@pytest.mark.parametrize("value", TRUTHY)
def test_each_truthy_form_hides_the_entry(tmp_path, value):
    _record(tmp_path, "run.toml", [_entry("D-001", value), _entry("D-002")])
    section = _section(tmp_path)
    assert "chose D-001" not in section
    assert "chose D-002" in section
    assert (
        decisions.record_findings((tmp_path / "docs/decisions/run.toml").read_text())
        == []
    )


@pytest.mark.parametrize("value", FALSY + [None])
def test_each_falsy_form_and_an_absent_key_shows_the_entry(tmp_path, value):
    _record(tmp_path, "run.toml", [_entry("D-001", value)])
    section = _section(tmp_path)
    assert "chose D-001" in section and "docs/decisions/run.toml" in section
    for label in (
        "Decided",
        "Alternative passed over",
        "Reversal cost",
        "Why not escalated",
    ):
        assert label in section, label
    assert (
        decisions.record_findings((tmp_path / "docs/decisions/run.toml").read_text())
        == []
    )


@pytest.mark.parametrize("value", ['"maybe"', '"Reviewd"', "[1]"])
def test_an_unrecognized_value_is_shown_and_is_a_format_finding(tmp_path, value):
    _record(tmp_path, "run.toml", [_entry("D-001", value)])
    section = _section(tmp_path)
    assert "chose D-001" in section
    text = (tmp_path / "docs/decisions/run.toml").read_text()
    (finding,) = decisions.record_findings(text)
    assert finding.startswith("D-001: `reviewed`") and "not reviewed" in finding
    assert "Format findings" in section


def test_a_note_alone_no_longer_marks_an_entry_reviewed(tmp_path):
    _record(tmp_path, "run.toml", [_entry("D-001", None, review="looked at it")])
    assert "chose D-001" in _section(tmp_path)


def test_high_risk_entries_come_first_and_000_is_never_shown(tmp_path):
    _record(tmp_path, "a.toml", [_entry("D-001"), _entry("D-002")])
    _record(
        tmp_path,
        "b.toml",
        [_entry("D-000"), _entry("D-003")],
        high_risk=["D-003", "D-000"],
    )
    section = _section(tmp_path)
    assert "chose D-000" not in section
    assert section.index("chose D-003") < section.index("chose D-001")
    assert section.index("chose D-001") < section.index("chose D-002")
    assert "high risk" in section.split("chose D-003", 1)[0]


def test_an_all_reviewed_state_says_so(tmp_path):
    _record(tmp_path, "run.toml", [_entry("D-001", "true"), _entry("D-002", '"done"')])
    section = _section(tmp_path)
    assert "Nothing left to review — 2 entries marked reviewed." in section
    assert "Decisions to review:** 0" in status.status_block(tmp_path)


def test_the_status_snapshot_counts_what_is_left(tmp_path):
    _record(tmp_path, "run.toml", [_entry("D-001"), _entry("D-002", "true")])
    block = status.status_block(tmp_path)
    assert (
        "- **Decisions to review:** 1 — "
        "[open-items.html](open-items.html#decisions-to-review)" in block
    )


def test_no_decisions_directory_has_nothing_to_review(tmp_path):
    assert "No delegated-decisions record" in _section(tmp_path)
    assert "Decisions to review" not in status.status_block(tmp_path)


def test_the_shipped_template_entry_carries_reviewed_false():
    text = (KIT / "decisions.template.toml").read_text(encoding="utf-8")
    assert "reviewed = false" in text
    assert decisions.record_findings(text) == []
    assert decisions.review_queue(text) == ([], 0)  # -000 is never listed
    assert decisions.reviewed_state(None) is False
    assert (
        decisions.reviewed_state(True) is True and decisions.reviewed_state(0) is False
    )
    assert decisions.reviewed_state("perhaps") is None


def test_a_malformed_hoist_is_shown_as_a_finding_not_a_crash(tmp_path):
    # Sol review 1, MAJOR 3: a session-authored record whose `high_risk` holds
    # a non-string is reported by `record_findings`; the owner page still
    # renders every entry and shows that finding.
    folder = tmp_path / "docs/decisions"
    folder.mkdir(parents=True)
    (folder / "run.toml").write_text(
        'high_risk = [["D-001"]]\n\n' + _entry("D-001"), encoding="utf-8"
    )
    shown, reviewed = decisions.review_queue((folder / "run.toml").read_text())
    assert [e["id"] for e in shown] == ["D-001"] and reviewed == 0
    section = _section(tmp_path)
    assert "chose D-001" in section
    assert "Format findings" in section and "high_risk" in section
