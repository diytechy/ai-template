"""record_rows.py — the acceptance record written and judged row by row (WI-1060).

In-process cases over texts: how a registry text splits into a head, rows and a
tail; which side the rule takes each row from; the copy an act writes, byte for
byte; and the parse-level reading of a written copy that the writer re-reads
its result with and the record's mirror rules name a fault by. The acts
themselves, through the snapshot command and over git, are driven in
`tests/test_baseline_snapshot.py`.

Implements: TC-167, TC-240
"""

import pytest
from conftest import ROOT, load_script

RR = load_script("record_rows")
AR = load_script("acceptance_record")
SPLIT = AR.split_changed_cells
SR = "docs/requirements/system-requirements.toml"

HEAD = "# The requirement registry.\n#\n# A header comment.\n\n"


def _row(rid, status, title, sn="SN-001", phase=1, eol="\n"):
    return (
        '[requirement.{}]{e}title = "{}"{e}sn_refs = ["{}"]{e}phase = {}{e}'
        'status = "{}"{e}'.format(rid, title, sn, phase, status, e=eol)
    )


def _copy(prev, live, named=()):
    return RR.expected_copy(SR, (prev, ".toml"), (live, ".toml"), set(named), SPLIT)


def test_the_split_round_trips_every_registry_the_record_copies():
    """Every registry this repository records, and every template an adopter
    starts from, splits into whole rows that concatenate back to its text."""
    paths = [ROOT / rel for rel in load_script("baseline_snapshot").SNAPSHOTTED]
    paths += sorted(
        (ROOT / "project-trajectory" / "registries").glob("*.template.toml")
    )
    paths = [p for p in paths if p.is_file() and "hats" not in p.name]
    paths = [p for p in paths if "open-items" not in p.name]
    assert len(paths) >= 14, paths
    for path in paths:
        text = path.read_bytes().decode("utf-8")
        head, rows, tail = RR.row_segments(text)
        assert head + "".join(seg for _key, seg in rows) + tail == text, path
        assert len({key for key, _seg in rows}) == len(rows), path


def test_a_text_that_does_not_split_into_whole_rows_is_refused():
    """A header-looking line inside a multi-line string, and a table that is no
    tier's, are refused rather than split by guess."""
    hidden = '[requirement.SR-1]\ntitle = """two\n[requirement.SR-2]\nlines"""\n'
    with pytest.raises(RR.RowRecordError):
        RR.row_segments(hidden)
    with pytest.raises(RR.RowRecordError):
        RR.row_segments('[notes.N-1]\ntext = "x"\n')


def test_the_rule_takes_each_row_from_the_side_the_act_names():
    """The rule's table, one row per case: named rows (amended, flipped,
    retired) take live; an unnamed row follows live when it claims no
    acceptance in live (Drafted, de-accepted, new, or gone and recorded
    Drafted) or when its accepted and routed cells are unchanged (a silent
    trace cell refreshed); an unnamed accepted row whose accepted text or
    routed link moved, or that live no longer carries, keeps its record; an
    unnamed flip or a row born accepted unnamed stays as recorded."""
    prev = HEAD + "".join(
        [
            _row("SR-1", "Accepted", "Named"),
            _row("SR-2", "Drafted", "Flipped"),
            _row("SR-3", "Accepted", "Retired"),
            _row("SR-4", "Drafted", "Drafted"),
            _row("SR-5", "Accepted", "Deaccepted"),
            _row("SR-6", "Drafted", "Gone"),
            _row("SR-7", "Accepted", "Silent"),
            _row("SR-8", "Accepted", "Drift"),
            _row("SR-9", "Accepted", "Routed"),
            _row("SR-10", "Accepted", "Removed"),
            _row("SR-11", "Drafted", "Unnamed flip"),
        ]
    )
    live = HEAD + "".join(
        [
            _row("SR-1", "Accepted", "Named, amended"),
            _row("SR-2", "Accepted", "Flipped"),
            _row("SR-4", "Drafted", "Drafted, reworded"),
            _row("SR-5", "Drafted", "Deaccepted, reworded"),
            _row("SR-7", "Accepted", "Silent", phase=2),
            _row("SR-8", "Accepted", "Drift, unread"),
            _row("SR-9", "Accepted", "Routed", sn="SN-002"),
            _row("SR-11", "Accepted", "Unnamed flip"),
            _row("SR-12", "Drafted", "New"),
            _row("SR-13", "Accepted", "Born unnamed"),
        ]
    )
    rows = {k[1]: k for k in RR.file_rows(prev, ".toml")}
    sources = RR.row_rule(
        SR,
        RR.file_rows(prev, ".toml"),
        RR.file_rows(live, ".toml"),
        {"SR-1", "SR-2", "SR-3"},
        SPLIT,
    )
    by_id = {key[1]: src for key, src in sources.items()}
    assert by_id == {
        "SR-1": "live",
        "SR-2": "live",
        "SR-3": None,
        "SR-4": "live",
        "SR-5": "live",
        "SR-6": None,
        "SR-7": "live",
        "SR-8": "record",
        "SR-9": "record",
        "SR-10": "record",
        "SR-11": "record",
        "SR-12": "live",
        "SR-13": None,
    }, by_id
    assert rows["SR-1"][0] == "SR-ID"
    text, kept = _copy(prev, live, {"SR-1", "SR-2", "SR-3"})
    assert kept == ["SR-10", "SR-11", "SR-8", "SR-9"]
    assert (
        RR.row_problems(
            SR, (prev, ".toml"), (live, ".toml"), text, {"SR-1", "SR-2", "SR-3"}, SPLIT
        )
        == []
    )


def test_an_act_that_keeps_no_row_writes_the_live_text_byte_for_byte():
    """No previous copy (the seed) with every accepted row named, and a
    previous copy whose drift the act names, both write the live text
    unchanged; so does a legacy CSV carrier with nothing kept."""
    live = (
        HEAD + _row("SR-1", "Accepted", "One") + "\n" + _row("SR-2", "Drafted", "Two")
    )
    assert RR.expected_copy(SR, None, (live, ".toml"), {"SR-1"}, SPLIT) == (live, [])
    prev = HEAD + _row("SR-1", "Accepted", "Old")
    assert _copy(prev, live, {"SR-1"}) == (live, [])
    csv = "SR-ID,Title,Status\nSR-1,One,Accepted\n"
    old = "SR-ID,Title,Status\nSR-1,Zero,Accepted\n"
    assert RR.expected_copy(SR, (old, ".csv"), (csv, ".csv"), {"SR-1"}, SPLIT) == (
        csv,
        [],
    )


def test_the_copy_keeps_live_bytes_around_rows_and_each_rows_own_bytes():
    """Live's head and tail, live's row order and each row's bytes whole: a
    comment between rows travels with the row it precedes, a kept row keeps
    its recorded bytes and line endings, a quoted id splits like a bare one,
    and a kept row live no longer carries stays after the row it followed."""
    prev = (
        HEAD
        + _row("SR-1", "Accepted", "One")
        + "\n# --- a section ---\n\n"
        + _row("SR-2", "Accepted", "Two", eol="\r\n")
        + '\n[requirement."SR-3"]\ntitle = "Three"\nstatus = "Accepted"\n'
        + "\n"
        + _row("SR-4", "Accepted", "Four")
    )
    live = (
        "# The requirement registry, reworded.\n\n"
        + _row("SR-1", "Accepted", "One, amended")
        + "\n# --- a section, renamed ---\n\n"
        + _row("SR-2", "Accepted", "Two, unread")
        + '\n[requirement."SR-3"]\ntitle = "Three"\nstatus = "Accepted"\n'
        + "\n# trailing\n"
    )
    text, kept = _copy(prev, live, {"SR-1"})
    assert kept == ["SR-2", "SR-4"]
    assert text == (
        "# The requirement registry, reworded.\n\n"
        + _row("SR-1", "Accepted", "One, amended")
        + "\n# --- a section ---\n\n"
        + _row("SR-2", "Accepted", "Two", eol="\r\n")
        + '\n[requirement."SR-3"]\ntitle = "Three"\nstatus = "Accepted"\n'
        + "\n"
        + _row("SR-4", "Accepted", "Four")
        + "\n# trailing\n"
    ), text


def test_a_legacy_carrier_is_refused_when_a_row_would_be_kept():
    """A CSV registry is copied only whole: an act that would keep a drifted
    row in it is refused naming the row."""
    old = "SR-ID,Title,Status\nSR-1,One,Accepted\nSR-2,Two,Accepted\n"
    live = "SR-ID,Title,Status\nSR-1,One!,Accepted\nSR-2,Two!,Accepted\n"
    with pytest.raises(RR.RowRecordError, match="SR-2"):
        RR.expected_copy(SR, (old, ".csv"), (live, ".csv"), {"SR-1"}, SPLIT)


def test_a_written_copy_is_read_row_by_row_and_each_fault_named():
    """The parse-level reading names each wrong row and why, and the judge's
    comparison names bytes outside the rows when every row reads right."""
    prev = HEAD + _row("SR-1", "Accepted", "A") + "\n" + _row("SR-2", "Accepted", "B")
    live = HEAD + _row("SR-1", "Accepted", "A2") + "\n" + _row("SR-2", "Accepted", "B2")
    named = {"SR-1"}
    want, kept = _copy(prev, live, named)
    assert kept == ["SR-2"]
    pair = (prev, ".toml"), (live, ".toml")

    def faults(written):
        return RR.copy_problems(SR, *pair, written, named, SPLIT)

    assert faults(want) == []
    assert any("SR-2" in f and "did not name" in f for f in faults(live))
    edited = want.replace('title = "A2"', 'title = "A3"')
    assert any("SR-1" in f and "named by the act" in f for f in faults(edited))
    dropped = want.replace("\n" + _row("SR-2", "Accepted", "B"), "")
    assert any("SR-2" in f and "no act retired it" in f for f in faults(dropped))
    assert faults(want + "# a comment\n") == [
        "{}: its bytes between or around the rows are not live's".format(SR)
    ]


def test_a_template_example_row_follows_live_whatever_its_status():
    """A `-000` row is a template's placeholder, which no reader of the record
    reads, so it follows live even when it reads `Accepted` and no act names
    it, as a shipped template's example stakeholder does; a seed with no
    previous copy therefore copies a template whole."""
    live = (
        HEAD
        + _row("SR-000", "Accepted", "Example")
        + "\n"
        + _row("SR-1", "Accepted", "One")
    )
    assert RR.expected_copy(SR, None, (live, ".toml"), {"SR-1"}, SPLIT) == (live, [])
    prev = (
        HEAD
        + _row("SR-000", "Accepted", "Old example")
        + "\n"
        + _row("SR-1", "Accepted", "One")
    )
    assert _copy(prev, live) == (live, [])
