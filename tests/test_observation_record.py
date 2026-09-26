"""The observation record's format, strict reader and atomic write (TC-229).

An observation test case is a judgment the harness cannot rerun, so its result
is recorded apart from the case, one file per result under
`docs/test/observations/` (SR-199). `kitlib/observation.py` owns that file: the
fields every record carries, the one canonical UTC form its two instants are
written in, the reader that refuses anything short of a whole record, and the
write that never leaves half a record where a reader looks. Driven here in a
temporary directory, with no scaffold, subprocess or git, so the module stays in
the per-commit tier. The writer's command and the checker's reading of records
on disk are pinned in `tests/test_observation_writer.py`.
"""

import pytest

from conftest import load_script

load_script("spine_carrier")  # puts scripts/ on the path for the package import
import kitlib.observation as OBS  # noqa: E402


def _record(**cells):
    """A complete record; a case below changes one field at a time."""
    rec = {
        "tc": "TC-001",
        "outcome": "pass",
        "observed_at": "2026-09-01T10:15:00Z",
        "provenance": "a reader new to the code",
        "expires": "2026-10-01T10:15:00Z",
        "judged": "sha256:" + "ab" * 32,
    }
    rec.update(cells)
    return rec


def _text(**cells):
    return OBS.render(_record(**cells))


def _without(text, field):
    """`text` with the one line assigning `field` removed."""
    lines = text.split("\n")
    kept = [line for line in lines if not line.startswith(field + " =")]
    assert len(kept) == len(lines) - 1, "fixture: no single line assigns " + field
    return "\n".join(kept)


# --- the fields and the round trip -------------------------------------------


def test_the_record_declares_its_six_fields_and_two_outcomes():
    assert OBS.FIELDS == (
        "tc",
        "outcome",
        "observed_at",
        "provenance",
        "expires",
        "judged",
    )
    assert OBS.OUTCOMES == ("pass", "fail")
    assert OBS.OBSERVATIONS_DIR == "docs/test/observations"


def test_a_record_with_every_field_round_trips():
    rec = _record()
    parsed = OBS.parse(OBS.render(rec))
    assert parsed is not None
    assert {k: parsed[k] for k in OBS.FIELDS} == rec


def test_awkward_provenance_text_round_trips():
    rec = _record(provenance='the "owner", reading C:\\repo on a Tuesday')
    assert OBS.parse(OBS.render(rec))["provenance"] == rec["provenance"]


@pytest.mark.parametrize("field", OBS.FIELDS)
def test_a_record_missing_any_one_field_parses_to_nothing(field):
    assert OBS.parse(_without(_text(), field)) is None


def test_a_record_cut_off_mid_file_parses_to_nothing():
    """Every cut before the last value's closing quote leaves either an
    unterminated string or a missing field: none of them is a record."""
    text = _text()
    last_quote = text.rstrip().rfind('"')
    assert OBS.parse(text[: last_quote + 1]) is not None, "the uncut text is valid"
    for cut in range(last_quote + 1):
        assert OBS.parse(text[:cut]) is None, repr(text[:cut])


def test_an_empty_judged_digest_is_valid():
    """A case declaring no inputs judges nothing: its record's digest is the
    empty string, and the record is still whole."""
    parsed = OBS.parse(_text(judged=""))
    assert parsed is not None and parsed["judged"] == ""


# --- what the strict reader refuses ------------------------------------------


@pytest.mark.parametrize("outcome", ["passed", "PASS", "inconclusive", ""])
def test_an_outcome_outside_pass_and_fail_parses_to_nothing(outcome):
    assert OBS.parse(_text(outcome=outcome)) is None


@pytest.mark.parametrize("outcome", ["pass", "fail"])
def test_both_outcomes_parse(outcome):
    assert OBS.parse(_text(outcome=outcome))["outcome"] == outcome


NOT_CANONICAL = [
    "2026-09-01 10:15:00Z",
    "2026-09-01T10:15:00+00:00",
    "2026-09-01T10:15Z",
    "2026-09-01T10:15:00.250Z",
    "2026-09-01T10:15:00",
    "2026-13-01T10:15:00Z",
    "2026-09-31T10:15:00Z",
    "20260901T101500Z",
    "",
]


@pytest.mark.parametrize("value", NOT_CANONICAL)
def test_an_observed_at_not_in_the_canonical_utc_form_parses_to_nothing(value):
    assert OBS.parse(_text(observed_at=value)) is None


@pytest.mark.parametrize("value", NOT_CANONICAL)
def test_an_expires_not_in_the_canonical_utc_form_parses_to_nothing(value):
    assert OBS.parse(_text(expires=value)) is None


def test_a_bare_toml_datetime_is_not_the_canonical_form():
    """The canonical form is a quoted string. A TOML datetime literal reads as
    a datetime, not as the text the record promises."""
    text = _text().replace(
        'observed_at = "2026-09-01T10:15:00Z"', "observed_at = 2026-09-01T10:15:00Z"
    )
    assert "observed_at = 2026-09-01T10:15:00Z" in text
    assert OBS.parse(text) is None


def test_parse_utc_accepts_only_the_canonical_form():
    moment = OBS.parse_utc("2026-09-01T10:15:00Z")
    assert moment is not None
    assert (moment.year, moment.month, moment.day) == (2026, 9, 1)
    assert moment.utcoffset().total_seconds() == 0
    for value in NOT_CANONICAL:
        assert OBS.parse_utc(value) is None, value


def test_an_expiry_earlier_than_the_observation_parses_to_nothing():
    assert OBS.parse(_text(expires="2026-09-01T10:14:59Z")) is None


def test_an_expiry_at_the_observation_itself_is_valid():
    assert OBS.parse(_text(expires="2026-09-01T10:15:00Z")) is not None


@pytest.mark.parametrize("provenance", ["", " ", "\t\n "])
def test_an_empty_or_whitespace_provenance_parses_to_nothing(provenance):
    assert OBS.parse(_text(provenance=provenance)) is None


def test_the_reason_a_text_is_not_a_record_is_stated():
    """The checker names the defect beside the file, so the reader's refusal
    carries its reason; a whole record has none."""
    assert OBS.problem(_text()) is None
    assert "provenance" in OBS.problem(_text(provenance=" "))
    assert "expires" in OBS.problem(_text(expires="2026-08-01T00:00:00Z"))
    assert "observed_at" in OBS.problem(_text(observed_at="yesterday"))


# --- reading the directory -----------------------------------------------------


def _write(root, name, text):
    folder = root / OBS.OBSERVATIONS_DIR
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_text(text, encoding="utf-8")


def test_a_leading_dot_file_is_never_read(tmp_path):
    _write(tmp_path, ".TC-001.2026-09-01T101500Z.toml", _text())
    _write(tmp_path, "TC-002.2026-09-01T101500Z.toml", _text(tc="TC-002"))
    assert list(OBS.read_files(tmp_path)) == ["TC-002.2026-09-01T101500Z.toml"]
    assert [r["tc"] for r in OBS.read_records(tmp_path)] == ["TC-002"]


def test_a_file_that_does_not_parse_is_read_but_is_never_a_result(tmp_path):
    _write(tmp_path, "TC-001.2026-09-01T101500Z.toml", _text()[:40])
    _write(
        tmp_path,
        "TC-001.2026-09-02T101500Z.toml",
        _text(observed_at="2026-09-02T10:15:00Z", expires="2026-10-02T10:15:00Z"),
    )
    assert len(OBS.read_files(tmp_path)) == 2
    records = OBS.read_records(tmp_path)
    assert [r["file"] for r in records] == ["TC-001.2026-09-02T101500Z.toml"]


def test_a_whole_record_under_any_other_name_is_never_a_result(tmp_path):
    """A record's file is named by its case and its instant (LLR-234), so a
    valid record saved under another name, or under another case's or
    instant's name, is read, for the checker to name, and never evidences
    anything."""
    good = OBS.record_name("TC-001", "2026-09-01T10:15:00Z")
    _write(tmp_path, good, _text())
    _write(tmp_path, "arbitrary.toml", _text())
    _write(tmp_path, "TC-002.2026-09-01T101500Z.toml", _text())
    _write(tmp_path, "TC-001.2026-09-09T101500Z.toml", _text())
    assert len(OBS.read_files(tmp_path)) == 4
    assert [r["file"] for r in OBS.read_records(tmp_path)] == [good]


def test_the_name_a_record_must_carry_is_the_stated_reason():
    text = _text()
    right = OBS.record_name("TC-001", "2026-09-01T10:15:00Z")
    assert OBS.problem(text, right) is None and OBS.parse(text, right) is not None
    why = OBS.problem(text, "arbitrary.toml")
    assert why is not None and right in why, why
    assert OBS.parse(text, "arbitrary.toml") is None
    # With no name, the content alone is judged: the writer names the file.
    assert OBS.parse(text) is not None


def test_records_already_read_are_parsed_without_reading_again(tmp_path):
    files = {"TC-001.2026-09-01T101500Z.toml": _text()}
    assert [r["tc"] for r in OBS.read_records(tmp_path, files)] == ["TC-001"]


def test_no_directory_reads_as_no_records(tmp_path):
    assert OBS.read_files(tmp_path) == {}
    assert OBS.read_records(tmp_path) == []


def test_latest_returns_the_newest_record_by_observation_time():
    older = _record(observed_at="2026-09-01T10:15:00Z", outcome="fail")
    newest = _record(observed_at="2026-09-03T08:00:00Z", expires="2026-10-03T08:00:00Z")
    middle = _record(observed_at="2026-09-02T23:59:59Z")
    other = _record(tc="TC-002", observed_at="2026-09-09T00:00:00Z")
    assert OBS.latest([middle, newest, older, other], "TC-001") is newest
    assert OBS.latest([older, other], "TC-002") is other
    assert OBS.latest([older, other], "TC-003") is None


def test_the_record_name_carries_the_case_and_a_colon_free_utc_instant():
    name = OBS.record_name("TC-001", "2026-09-01T10:15:00Z")
    assert name == "TC-001.2026-09-01T101500Z.toml"
    assert ":" not in name


# --- the atomic write ------------------------------------------------------------


class _FlakyReplace:
    """A stand-in for `os.replace` refusing the first `failures` calls with the
    PermissionError Windows raises while another process holds the target."""

    def __init__(self, failures):
        import os

        self.failures = failures
        self.calls = 0
        self._real = os.replace

    def __call__(self, src, dst):
        self.calls += 1
        if self.calls <= self.failures:
            raise PermissionError(13, "The process cannot access the file", str(dst))
        self._real(src, dst)


def test_the_write_retries_a_refused_replace_and_then_succeeds(tmp_path):
    folder = tmp_path / OBS.OBSERVATIONS_DIR
    folder.mkdir(parents=True)
    target = folder / "TC-001.2026-09-01T101500Z.toml"
    replace = _FlakyReplace(failures=2)
    OBS.write_atomic(target, _text(), replace=replace, pause=0)
    assert replace.calls == 3
    assert OBS.parse(target.read_text(encoding="utf-8")) is not None
    assert [p.name for p in folder.iterdir()] == [target.name], "no temp file left"


def test_the_write_raises_after_its_bounded_retries_and_leaves_no_readable_record(
    tmp_path,
):
    folder = tmp_path / OBS.OBSERVATIONS_DIR
    folder.mkdir(parents=True)
    target = folder / "TC-001.2026-09-01T101500Z.toml"
    replace = _FlakyReplace(failures=10**6)
    with pytest.raises(PermissionError):
        OBS.write_atomic(target, _text(), replace=replace, pause=0)
    assert replace.calls == OBS.REPLACE_ATTEMPTS
    assert OBS.REPLACE_ATTEMPTS > 1, "a bounded number of RETRIES, not one try"
    assert not target.exists()
    assert OBS.read_records(tmp_path) == []
    assert all(p.name.startswith(".") for p in folder.iterdir())
