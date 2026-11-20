"""The operator's verdict on a delegated decision, read in its record (WI-818;
operator direction 2026-10-04, superseding WI-790's `reviewed` key; WI-1009,
the operator's ruling of 2026-11-19).

The records under `docs/decisions/` are where the operator reads the entries:
one file per run, its `high_risk` list naming the entries to read first. One
key, `operator`, carries the verdict: `confirmed` or `overruled`. An absent
key is NOT YET SEEN. Any other value, and the retired `reviewed` key, is a
format finding and reads as not yet seen, so a typo never hides a decision;
the reader never reads `reviewed` beside `operator` (the migrator rewrites
it). An overruled entry states the direction instead in its `review` note (a
blank note is a finding).

`docs/open-items.html` lists no entry: it has no "Decisions to review" section
and no decision card (WI-1009). It reports only the records' format findings,
by file and entry, in a notice closing section 3, so a malformed record is
still told whatever the dial. `docs/status.md` counts the entries not yet seen
and points at the records.

Implements: TC-293
"""

import pytest

from conftest import KIT, load_script

gen = load_script("gen_open_items")
pending = load_script("pending")
status = load_script("traj_status")
decisions = pending._kitdecisions


def _entry(eid, owner=None, review="", extra=""):
    line = "" if owner is None else "operator = {}\n".format(owner)
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


def _unseen(root):
    return pending.decision_records(root)[0]


def _actions(root):
    """Section 3's band, which the findings notice closes."""
    page = gen.render(root)
    return page.split("3 · Pending operator actions", 1)[1].split("</section>", 1)[0]


def test_the_page_lists_no_entry_and_has_no_decisions_section(tmp_path):
    _record(
        tmp_path,
        "run.toml",
        [
            _entry("D-001"),
            _entry("D-002", '"confirmed"'),
            _entry("D-003", '"overruled"', review="Keep the old name instead."),
        ],
        high_risk=["D-001"],
    )
    spec = tmp_path / "docs/work/queued/WI-007-rename.md"
    spec.parent.mkdir(parents=True)
    spec.write_text(
        '+++\nid = "WI-007"\ntitle = "t"\n+++\n\n## Done-when\n\n'
        "- Undo docs/decisions/run.toml#D-003: keep the old name.\n",
        encoding="utf-8",
    )
    page = gen.render(tmp_path)
    assert 'id="decisions-to-review"' not in page
    assert "Decisions to review" not in page
    for eid in ("D-001", "D-002", "D-003"):
        assert "chose " + eid not in page, eid
    assert "Keep the old name instead." not in page
    assert "high risk" not in page
    # Sound records put nothing on the page at all.
    assert "docs/decisions" not in page


def test_confirmed_and_overruled_are_not_counted_and_are_sound(tmp_path):
    _record(
        tmp_path,
        "run.toml",
        [
            _entry("D-001", '"confirmed"'),
            _entry("D-002"),
            _entry("D-003", '"overruled"', review="Undo."),
        ],
    )
    assert pending.decision_records(tmp_path) == (1, [])
    assert decisions.record_findings(_text(tmp_path)) == []


@pytest.mark.parametrize(
    "value", ['"Confirmed"', '"maybe"', "true", '"reviewed"', "1", '""']
)
def test_an_unrecognized_value_reads_as_not_yet_seen_and_is_reported(tmp_path, value):
    _record(tmp_path, "run.toml", [_entry("D-001", value)])
    assert _unseen(tmp_path) == 1
    (finding,) = decisions.record_findings(_text(tmp_path))
    assert finding.startswith("D-001: `operator`") and "not yet seen" in finding
    assert "docs/decisions/run.toml: D-001: `operator`" in _actions(tmp_path)


@pytest.mark.parametrize("owner", [None, '"confirmed"'])
def test_the_retired_reviewed_key_is_a_finding_and_never_read(tmp_path, owner):
    # An entry still carrying `reviewed` reads as NOT YET SEEN whatever `operator`
    # says (the spec's first Done-when bullet): the stale key keeps it unseen
    # until the migrator removes it.
    _record(tmp_path, "run.toml", [_entry("D-001", owner, extra="reviewed = true\n")])
    assert _unseen(tmp_path) == 1
    unseen, overruled, confirmed = decisions.review_queue(_text(tmp_path))
    assert [e["id"] for e in unseen] == ["D-001"] and confirmed == 0
    (finding,) = decisions.record_findings(_text(tmp_path))
    assert finding.startswith("D-001: `reviewed` is retired")
    assert "D-001: `reviewed` is retired" in _actions(tmp_path)


def test_an_overrule_with_a_blank_note_is_a_format_finding(tmp_path):
    _record(tmp_path, "run.toml", [_entry("D-001", '"overruled"', review="  ")])
    (finding,) = decisions.record_findings(_text(tmp_path))
    assert finding.startswith("D-001: overruled with a blank `review`")
    assert "D-001: overruled with a blank" in _actions(tmp_path)
    assert _unseen(tmp_path) == 0


def test_a_note_alone_marks_nothing(tmp_path):
    _record(tmp_path, "run.toml", [_entry("D-001", None, review="looked at it")])
    assert _unseen(tmp_path) == 1


def test_000_is_never_counted_or_judged(tmp_path):
    _record(
        tmp_path,
        "b.toml",
        ['[decision.D-000]\ndecided = ""\n\n', _entry("D-003")],
        high_risk=["D-003", "D-000"],
    )
    assert pending.decision_records(tmp_path) == (1, [])


def test_records_are_summed_and_their_findings_named_by_file(tmp_path):
    _record(tmp_path, "a.toml", [_entry("D-001"), _entry("D-002")])
    _record(tmp_path, "b.toml", [_entry("D-001", '"maybe"')])
    unseen, findings = pending.decision_records(tmp_path)
    assert unseen == 3
    assert [f.split(": ", 1)[0] for f in findings] == ["docs/decisions/b.toml"]


def test_an_unparseable_record_is_reported_and_counts_nothing(tmp_path):
    folder = tmp_path / "docs/decisions"
    folder.mkdir(parents=True)
    (folder / "run.toml").write_text("high_risk = [\n[decision.D-001\n")
    unseen, (finding,) = pending.decision_records(tmp_path)
    assert unseen == 0
    assert finding.startswith("docs/decisions/run.toml: the record does not parse")
    assert "the record does not parse" in _actions(tmp_path)


def test_a_malformed_hoist_is_shown_as_a_finding_not_a_crash(tmp_path):
    """Implements: TC-293"""
    folder = tmp_path / "docs/decisions"
    folder.mkdir(parents=True)
    (folder / "run.toml").write_text(
        'high_risk = [["D-001"]]\n\n' + _entry("D-001"), encoding="utf-8"
    )
    unseen, overruled, confirmed = decisions.review_queue(_text(tmp_path))
    assert [e["id"] for e in unseen] == ["D-001"] and confirmed == 0
    assert overruled == []
    assert _unseen(tmp_path) == 1
    actions = _actions(tmp_path)
    assert "docs/decisions/run.toml" in actions and "high_risk" in actions
    assert "chose D-001" not in actions


def test_the_findings_notice_closes_section_three(tmp_path):
    _record(tmp_path, "run.toml", [_entry("D-001", '"maybe"')])
    actions = _actions(tmp_path)
    notice = actions.index("docs/decisions/run.toml: D-001")
    assert actions.index("</ul>", notice) == len(actions) - len("</ul>")


def test_sound_records_and_no_records_put_no_notice_on_the_page(tmp_path):
    assert "docs/decisions" not in gen.render(tmp_path)
    _record(tmp_path, "run.toml", [_entry("D-001"), _entry("D-002", '"confirmed"')])
    assert "docs/decisions" not in gen.render(tmp_path)


def test_the_status_snapshot_counts_what_is_left(tmp_path):
    _record(tmp_path, "run.toml", [_entry("D-001"), _entry("D-002", '"confirmed"')])
    block = status.status_block(tmp_path)
    assert (
        "- **Delegated decisions not yet seen:** 1 — [docs/decisions/](decisions/)"
        in block
    )
    assert "decisions-to-review" not in block
    assert "Decisions to review" not in block


def test_an_all_confirmed_state_counts_zero(tmp_path):
    _record(
        tmp_path,
        "run.toml",
        [_entry("D-001", '"confirmed"'), _entry("D-002", '"confirmed"')],
    )
    assert "Delegated decisions not yet seen:** 0 —" in status.status_block(tmp_path)


def test_no_decisions_directory_has_nothing_unseen(tmp_path):
    assert pending.decision_records(tmp_path) == (None, [])
    assert "Delegated decisions" not in status.status_block(tmp_path)


def test_the_shipped_template_entry_leaves_the_operator_key_unset():
    text = (KIT / "decisions.template.toml").read_text(encoding="utf-8")
    assert "\nreviewed" not in text and "\noperator =" not in text
    assert decisions.record_findings(text) == []
    assert decisions.review_queue(text) == ([], [], 0)  # -000 is never counted
    assert decisions.operator_state(None) == ""
    assert decisions.operator_state("confirmed") == decisions.CONFIRMED
    assert decisions.operator_state("overruled") == decisions.OVERRULED
    assert decisions.operator_state(True) is None
    assert decisions.operator_state("perhaps") is None


def test_the_shipped_template_sends_the_operator_to_the_record_files():
    # WI-1009: the header names no page section; the record files are where
    # the operator reads an entry with no `operator` key.
    text = (KIT / "decisions.template.toml").read_text(encoding="utf-8")
    assert "Decisions to review" not in text and "open-items.html" not in text
    assert "docs/decisions/<run>.toml" in text and "NOT YET SEEN" in text


def test_review_queue_lists_hoisted_first_then_by_id(tmp_path):
    # File order D-003, D-001, D-002 with D-002 hoisted: each list reads D-002,
    # D-001, D-003 (IF-256).
    over = [
        _entry(eid, '"overruled"', review="Undo {}.".format(eid))
        for eid in ("D-003", "D-001", "D-002")
    ]
    _record(tmp_path, "run.toml", over, high_risk=["D-002"])
    _unseen_list, overruled, _count = decisions.review_queue(_text(tmp_path))
    assert [e["id"] for e in overruled] == ["D-002", "D-001", "D-003"]
    _record(
        tmp_path,
        "run.toml",
        [_entry(e) for e in ("D-003", "D-001", "D-002")],
        high_risk=["D-002"],
    )
    unseen, _overruled, _count = decisions.review_queue(_text(tmp_path))
    assert [e["id"] for e in unseen] == ["D-002", "D-001", "D-003"]
