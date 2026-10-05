"""The owner's verdict on a delegated decision, on the owner surface (WI-818;
owner direction 2026-10-04, superseding WI-790's `reviewed` key).

One key, `owner`, carries the owner's verdict: `confirmed` or `overruled`. An
absent key is NOT YET SEEN and lists the entry under "Decisions to review",
high-risk first. Any other value, and the retired `reviewed` key, is a format
finding and reads as not yet seen, so a typo never hides a decision; the
reader never reads `reviewed` beside `owner` (the migrator rewrites it). An
overruled entry states the direction instead in its `review` note (a blank
note is a finding) and is listed under its own heading with the work item
that cites it, so an overrule never disappears silently.
"""

import pytest

from conftest import KIT, load_script

gen = load_script("gen_open_items")
pending = load_script("pending")
status = load_script("traj_status")
decisions = pending._kitdecisions


def _entry(eid, owner=None, review="", extra=""):
    line = "" if owner is None else "owner = {}\n".format(owner)
    return (
        '[decision.{}]\ndecided = "chose {}"\nalternative = "a"\n'
        'reversal_cost = "c"\nwhy_not_escalated = "w"\nreview = "{}"\n{}{}\n'.format(
            eid, eid, review, line, extra
        )
    )


def _record(root, name, entries, high_risk=()):
    folder = root / "docs/decisions"
    folder.mkdir(parents=True, exist_ok=True)
    head = "high_risk = [{}]\n\n".format(", ".join('"{}"'.format(h) for h in high_risk))
    (folder / name).write_text(head + "".join(entries), encoding="utf-8")


def _text(root, name="run.toml"):
    return (root / "docs/decisions" / name).read_text(encoding="utf-8")


def _band(root):
    page = gen.render(root)
    return page.split('id="decisions-to-review"', 1)[1].split("</section>", 1)[0]


def _section(root):
    """The not-yet-seen half of the band: everything above the overruled
    heading."""
    return _band(root).split(gen.OVERRULED_HEADING, 1)[0]


def _overruled(root):
    band = _band(root)
    return (
        band.split(gen.OVERRULED_HEADING, 1)[1] if gen.OVERRULED_HEADING in band else ""
    )


def test_confirmed_hides_the_entry_and_is_sound(tmp_path):
    _record(tmp_path, "run.toml", [_entry("D-001", '"confirmed"'), _entry("D-002")])
    assert "chose D-001" not in _band(tmp_path)
    assert "chose D-002" in _section(tmp_path)
    assert decisions.record_findings(_text(tmp_path)) == []


def test_an_absent_key_reads_as_not_yet_seen(tmp_path):
    _record(tmp_path, "run.toml", [_entry("D-001")])
    section = _section(tmp_path)
    assert "chose D-001" in section and "docs/decisions/run.toml" in section
    for label in (
        "Decided",
        "Alternative passed over",
        "Reversal cost",
        "Why not escalated",
    ):
        assert label in section, label
    assert decisions.record_findings(_text(tmp_path)) == []


def test_overruled_leaves_the_queue_for_its_own_heading_with_the_citing_row(
    tmp_path,
):
    _record(
        tmp_path,
        "run.toml",
        [_entry("D-001", '"overruled"', review="Keep the old name instead.")],
    )
    spec = tmp_path / "docs/work/queued/WI-007-rename.md"
    spec.parent.mkdir(parents=True)
    spec.write_text(
        '+++\nid = "WI-007"\ntitle = "t"\n+++\n\n## Done-when\n\n'
        "- Undo docs/decisions/run.toml#D-001: keep the old name.\n",
        encoding="utf-8",
    )
    assert "chose D-001" not in _section(tmp_path)
    over = _overruled(tmp_path)
    assert "chose D-001" in over and "Keep the old name instead." in over
    assert "WI-007" in over and "queued" in over
    assert decisions.record_findings(_text(tmp_path)) == []


def test_an_overrule_no_row_cites_says_so(tmp_path):
    _record(tmp_path, "run.toml", [_entry("D-001", '"overruled"', review="Undo.")])
    assert "no work item cites" in _overruled(tmp_path)


@pytest.mark.parametrize(
    "value", ['"Confirmed"', '"maybe"', "true", '"reviewed"', "1", '""']
)
def test_an_unrecognized_value_is_shown_and_is_a_format_finding(tmp_path, value):
    _record(tmp_path, "run.toml", [_entry("D-001", value)])
    assert "chose D-001" in _section(tmp_path)
    (finding,) = decisions.record_findings(_text(tmp_path))
    assert finding.startswith("D-001: `owner`") and "not yet seen" in finding
    assert "Format findings" in _band(tmp_path)


@pytest.mark.parametrize("owner", [None, '"confirmed"'])
def test_the_retired_reviewed_key_is_a_finding_and_never_read(tmp_path, owner):
    # `reviewed = true` with no owner reads as not yet seen; beside an owner
    # key it is not read at all — the entry reads by `owner` alone.
    _record(tmp_path, "run.toml", [_entry("D-001", owner, extra="reviewed = true\n")])
    shown = "chose D-001" in _section(tmp_path)
    assert shown is (owner is None)
    (finding,) = decisions.record_findings(_text(tmp_path))
    assert finding.startswith("D-001: `reviewed` is retired")


def test_an_overrule_with_a_blank_note_is_a_format_finding(tmp_path):
    _record(tmp_path, "run.toml", [_entry("D-001", '"overruled"', review="  ")])
    (finding,) = decisions.record_findings(_text(tmp_path))
    assert finding.startswith("D-001: overruled with a blank `review`")
    assert "chose D-001" in _overruled(tmp_path)


def test_a_note_alone_marks_nothing(tmp_path):
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


def test_an_all_confirmed_state_says_so(tmp_path):
    _record(
        tmp_path,
        "run.toml",
        [_entry("D-001", '"confirmed"'), _entry("D-002", '"confirmed"')],
    )
    section = _section(tmp_path)
    assert "Nothing left to review — 2 entries confirmed." in section
    assert "Decisions to review:** 0" in status.status_block(tmp_path)


def test_the_status_snapshot_counts_what_is_left(tmp_path):
    _record(tmp_path, "run.toml", [_entry("D-001"), _entry("D-002", '"confirmed"')])
    block = status.status_block(tmp_path)
    assert (
        "- **Decisions to review:** 1 — "
        "[open-items.html](open-items.html#decisions-to-review)" in block
    )


def test_no_decisions_directory_has_nothing_to_review(tmp_path):
    assert "No delegated-decisions record" in _section(tmp_path)
    assert "Decisions to review" not in status.status_block(tmp_path)


def test_the_shipped_template_entry_leaves_the_owner_key_unset():
    text = (KIT / "decisions.template.toml").read_text(encoding="utf-8")
    assert "\nreviewed" not in text and "\nowner =" not in text
    assert decisions.record_findings(text) == []
    assert decisions.review_queue(text) == ([], [], 0)  # -000 is never listed
    assert decisions.owner_state(None) == ""
    assert decisions.owner_state("confirmed") == decisions.CONFIRMED
    assert decisions.owner_state("overruled") == decisions.OVERRULED
    assert decisions.owner_state(True) is None
    assert decisions.owner_state("perhaps") is None


def test_a_malformed_hoist_is_shown_as_a_finding_not_a_crash(tmp_path):
    folder = tmp_path / "docs/decisions"
    folder.mkdir(parents=True)
    (folder / "run.toml").write_text(
        'high_risk = [["D-001"]]\n\n' + _entry("D-001"), encoding="utf-8"
    )
    unseen, overruled, confirmed = decisions.review_queue(_text(tmp_path))
    assert [e["id"] for e in unseen] == ["D-001"] and confirmed == 0
    assert overruled == []
    band = _band(tmp_path)
    assert "chose D-001" in band
    assert "Format findings" in band and "high_risk" in band
