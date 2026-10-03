"""The PER-DECOMPOSITION PERSPECTIVE RECORD (SR-161, LLR-297): what `hats.py
record` writes beside a decomposition, and what its check reports.

LLR-183 delivered the row half of SR-161 (`Hat-Refs`) and stated the other half
as undischarged: a record of the DECOMPOSITION, not of a row, that tells
"this perspective did not apply" apart from "it applied and found nothing". The
cases below pin each claim LLR-297 makes:

1. WRITE: applicability is DERIVED from the roster's predicates over the
   decomposition's parent needs, and `produced` is DERIVED from the in-scope
   rows' own `Hat-Refs`; nothing a person must hand-copy.
2. MISSING: an applicable perspective with neither produced rows nor an
   authored no-finding is reported, and stops being reported once a
   no-finding is written; the no-finding survives a rewrite.
3. THE DISTINCTION: a not-applicable perspective and a considered one with no
   finding read differently in the parsed file.
4. STALE / CONFLICT: a record whose derived fields no longer match regeneration
   is reported, and so is a no-finding that contradicts the derivation.
5. VACUITY: an absent roster is the layer's opt-out; the check reports nothing.
6. THE CLI: findings are warn-first; `--strict` turns them into exit 1.

Every finding case is driven over a tree built to produce it, so a green here
is demonstrated able to fail.
"""

from __future__ import annotations

import functools
import re
import tomllib

import pytest

from conftest import load_script
from kitlib import observation

hats = load_script("hats")

ROSTER = """
[hat.ALWAYS-ON]
applies_when = "always"
asks = "always question"
listens_for = "always failure"

[hat.SCRIPTS]
applies_when = 'tags contains "scripts"'
asks = "scripts question"
listens_for = "scripts failure"

[hat.UNREACHED]
applies_when = 'tags contains "nothing-carries-this"'
asks = "unreached question"
listens_for = "unreached failure"
"""

NEEDS = """
[need.SN-001]
status = "Approved"
need = "A need."
tags = ["scripts"]

[need.SN-002]
status = "Approved"
need = "Another need."
tags = ["ops"]
"""

SRS = """
[requirement.SR-001]
sn_refs = ["SN-001"]
hat_refs = ["ALWAYS-ON"]
requirement = "The system shall do one thing."

[requirement.SR-002]
sn_refs = ["SN-002"]
requirement = "The system shall do another thing."
"""

LLRS = """
[design.LLR-001]
sr_refs = ["SR-002"]
title = "A design row"
"""

TCS = """
[test.TC-001]
verifies = ["SR-001"]
method = "A method."

[test.TC-002]
verifies = ["LLR-001"]
method = "A method."
"""

REC = "docs/plans/DECOMP.perspectives.toml"


def _tree(tmp_path, roster=ROSTER, srs=SRS):
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "plans").mkdir(parents=True, exist_ok=True)
    if roster is not None:
        (req / "hats.toml").write_text(roster, encoding="utf-8")
    (req / "stakeholder-needs.toml").write_text(NEEDS, encoding="utf-8")
    (req / "system-requirements.toml").write_text(srs, encoding="utf-8")
    (req / "low-level-requirements.toml").write_text(LLRS, encoding="utf-8")
    (tmp_path / "docs" / "test" / "test-cases.toml").write_text(TCS, encoding="utf-8")
    return tmp_path


def _write(root, rows=("SR-001", "SR-002", "LLR-001", "TC-001")):
    return hats.write_record(
        root, REC, rows=list(rows), subject="DECOMP.md", by="test session"
    )


def _parsed(root):
    return tomllib.loads((root / REC).read_text(encoding="utf-8"))


def _classes(findings):
    return sorted({cls for cls, _text in findings})


def _set_no_finding(root, hat, reason):
    """Author a no-finding the way a person would: an edit to the record file."""
    path = root / REC
    text = path.read_text(encoding="utf-8")
    marker = "[perspective.{}]\n".format(hat)
    assert marker in text
    path.write_text(
        text.replace(
            marker, marker + "no_finding = {!r}\n".format(reason).replace("'", '"')
        ),
        encoding="utf-8",
    )


# --- 1. write: derived applicability and production ---------------------------
def test_write_derives_applicability_from_parents_and_production_from_hat_refs(
    tmp_path,
):
    root = _tree(tmp_path)
    _write(root)
    data = _parsed(root)
    assert data["decomposition"]["rows"] == ["SR-001", "SR-002", "LLR-001", "TC-001"]
    assert data["decomposition"]["parents"] == ["SN-001", "SN-002"]
    persp = data["perspective"]
    assert list(persp) == ["ALWAYS-ON", "SCRIPTS", "UNREACHED"]
    assert persp["ALWAYS-ON"]["applicable"] is True
    assert persp["ALWAYS-ON"]["produced"] == ["SR-001"]
    # SCRIPTS reaches SN-001 by its tag; the decomposition has no row citing it.
    assert persp["SCRIPTS"]["applicable"] is True
    assert persp["SCRIPTS"]["produced"] == []
    assert persp["UNREACHED"]["applicable"] is False
    assert persp["UNREACHED"]["applies_when"] == 'tags contains "nothing-carries-this"'


def test_declared_tags_widen_every_parent_context(tmp_path):
    root = _tree(tmp_path)
    hats.write_record(
        root,
        REC,
        rows=["SR-002"],
        subject="x",
        tags=["nothing-carries-this"],
        by="test session",
    )
    persp = _parsed(root)["perspective"]
    assert persp["UNREACHED"]["applicable"] is True
    assert persp["SCRIPTS"]["applicable"] is False, "SN-002 carries no scripts tag"


def test_an_unknown_row_refuses(tmp_path):
    root = _tree(tmp_path)
    with pytest.raises(hats.HatsError, match="SR-999"):
        _write(root, rows=["SR-001", "SR-999"])
    assert not (root / REC).exists()


def test_a_first_write_needs_rows(tmp_path):
    root = _tree(tmp_path)
    with pytest.raises(hats.HatsError, match="rows"):
        hats.write_record(root, REC)


# --- 1b. authorship: who recorded the authored judgements, and when -----------
def test_a_first_write_without_by_refuses(tmp_path):
    root = _tree(tmp_path)
    with pytest.raises(hats.HatsError, match="--by"):
        hats.write_record(root, REC, rows=["SR-001"], subject="DECOMP.md")
    assert not (root / REC).exists()


def test_the_record_names_who_and_when_and_a_refresh_keeps_them(tmp_path):
    root = _tree(tmp_path)
    _write(root)
    decomposition = _parsed(root)["decomposition"]
    assert decomposition["recorded_by"] == "test session"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", decomposition["recorded_on"])
    hats.write_record(root, REC)  # a refresh names nobody new
    again = _parsed(root)["decomposition"]
    assert again["recorded_by"] == "test session"
    assert again["recorded_on"] == decomposition["recorded_on"]


@pytest.mark.parametrize("field", ["recorded_by", "recorded_on"])
def test_a_record_that_lost_its_authorship_refuses(tmp_path, field):
    root = _tree(tmp_path)
    _write(root)
    path = root / REC
    kept = [
        ln
        for ln in path.read_text(encoding="utf-8").splitlines(True)
        if not ln.startswith(field + " =")
    ]
    path.write_text("".join(kept), encoding="utf-8")
    with pytest.raises(hats.HatsError, match=field):
        hats.record_findings(root, REC)
    with pytest.raises(hats.HatsError, match=field):
        hats.write_record(root, REC)


# --- 2. missing, and the no-finding that answers it ---------------------------
def test_an_applicable_perspective_with_nothing_recorded_is_missing(tmp_path):
    root = _tree(tmp_path)
    _write(root)
    findings = hats.record_findings(root, REC)
    assert findings == [
        ("MISSING", findings[0][1]),
    ], findings
    assert "SCRIPTS" in findings[0][1]


def test_a_no_finding_answers_missing_and_survives_a_rewrite(tmp_path):
    root = _tree(tmp_path)
    _write(root)
    _set_no_finding(root, "SCRIPTS", "Touches no script.")
    assert hats.record_findings(root, REC) == []
    hats.write_record(root, REC)  # a refresh from the file's own inputs
    assert _parsed(root)["perspective"]["SCRIPTS"]["no_finding"] == "Touches no script."
    assert _parsed(root)["decomposition"]["subject"] == "DECOMP.md"
    assert hats.record_findings(root, REC) == []


# --- 3. the distinction SR-161 names ------------------------------------------
def test_not_applicable_and_no_finding_read_differently(tmp_path):
    root = _tree(tmp_path)
    _write(root)
    _set_no_finding(root, "SCRIPTS", "Touches no script.")
    persp = _parsed(root)["perspective"]
    not_applicable, no_finding = persp["UNREACHED"], persp["SCRIPTS"]
    assert not_applicable["applicable"] is False and "no_finding" not in not_applicable
    assert no_finding["applicable"] is True and no_finding["produced"] == []
    assert no_finding["no_finding"]


# --- 4. stale and conflict ----------------------------------------------------
def test_a_record_whose_rows_moved_is_stale(tmp_path):
    root = _tree(tmp_path)
    _write(root)
    _set_no_finding(root, "SCRIPTS", "Touches no script.")
    moved = SRS.replace(
        'hat_refs = ["ALWAYS-ON"]', 'hat_refs = ["ALWAYS-ON", "SCRIPTS"]'
    )
    (root / "docs/requirements/system-requirements.toml").write_text(
        moved, encoding="utf-8"
    )
    classes = _classes(hats.record_findings(root, REC))
    # SCRIPTS now produced SR-001: the stored `produced` is stale, and the
    # authored no-finding contradicts the derivation.
    assert classes == ["CONFLICT", "STALE"]


def test_a_no_finding_on_a_not_applicable_perspective_is_a_conflict(tmp_path):
    root = _tree(tmp_path)
    _write(root)
    _set_no_finding(root, "SCRIPTS", "Touches no script.")
    _set_no_finding(root, "UNREACHED", "Not relevant.")
    findings = hats.record_findings(root, REC)
    assert _classes(findings) == ["CONFLICT"]
    assert "UNREACHED" in findings[0][1]


def test_an_entry_for_an_undeclared_hat_is_kept_and_reported_stale(tmp_path):
    root = _tree(tmp_path)
    _write(root)
    _set_no_finding(root, "SCRIPTS", "Touches no script.")
    (root / "docs/requirements/hats.toml").write_text(
        ROSTER.split("[hat.UNREACHED]")[0], encoding="utf-8"
    )
    findings = hats.record_findings(root, REC)
    assert _classes(findings) == ["STALE"]
    assert "UNREACHED" in findings[0][1]
    hats.write_record(root, REC)
    assert "UNREACHED" in _parsed(root)["perspective"], "authored text is never dropped"


def test_a_malformed_record_refuses(tmp_path):
    root = _tree(tmp_path)
    (root / REC).write_text("[decomposition]\nrows = 'SR-001'\n", encoding="utf-8")
    with pytest.raises(hats.HatsError, match="rows"):
        hats.record_findings(root, REC)


# --- 5. vacuity ---------------------------------------------------------------
def test_an_absent_roster_writes_no_perspectives_and_checks_vacuous(tmp_path):
    root = _tree(tmp_path, roster=None)
    _write(root)
    assert "perspective" not in _parsed(root)
    assert hats.record_findings(root, REC) == []


# --- 6. the CLI ---------------------------------------------------------------
def _cli(root, capsys, *args):
    code = hats.main(["--root", str(root), "record", REC, *args])
    return code, capsys.readouterr().out


def test_the_cli_is_warn_first_and_strict_exits_nonzero(tmp_path, capsys):
    root = _tree(tmp_path)
    code, out = _cli(
        root,
        capsys,
        "--row",
        "SR-001",
        "--row",
        "SR-002",
        "--subject",
        "DECOMP.md",
        "--by",
        "test session",
    )
    assert code == 0 and "MISSING" in out and "SCRIPTS" in out
    code, out = _cli(root, capsys, "--check")
    assert code == 0 and "MISSING" in out
    code, out = _cli(root, capsys, "--check", "--strict")
    assert code == 1
    _set_no_finding(root, "SCRIPTS", "Touches no script.")
    code, out = _cli(root, capsys, "--check", "--strict")
    assert code == 0 and "no findings" in out


def test_the_cli_refuses_inputs_alongside_check(tmp_path, capsys):
    root = _tree(tmp_path)
    assert (
        hats.main(["--root", str(root), "record", REC, "--check", "--row", "SR-001"])
        == 2
    )


# --- 7. derivation edges, refresh retention, and the atomic write -------------
SIBLING_ROSTER = (
    ROSTER
    + """
[hat.BOTH]
applies_when = 'tags contains "scripts" and tags contains "ops"'
asks = "q"
listens_for = "f"

[hat.EXTRA-OPS]
applies_when = 'tags contains "extra" and tags contains "ops"'
asks = "q"
listens_for = "f"

[hat.EXTRA-SCRIPTS]
applies_when = 'tags contains "extra" and tags contains "scripts"'
asks = "q"
listens_for = "f"
"""
)


@pytest.mark.parametrize(
    "rows, parents",
    [(["LLR-001"], ["SN-002"]), (["TC-001"], ["SN-001"]), (["TC-002"], ["SN-002"])],
)
def test_parents_are_reached_through_llr_and_tc_rows(tmp_path, rows, parents):
    root = _tree(tmp_path)
    hats.write_record(root, REC, rows=rows, by="test session")
    assert _parsed(root)["decomposition"]["parents"] == parents


def test_applicability_is_never_merged_across_sibling_needs(tmp_path):
    root = _tree(tmp_path, roster=SIBLING_ROSTER)
    hats.write_record(root, REC, rows=["SR-001", "SR-002"], by="test session")
    assert _parsed(root)["perspective"]["BOTH"]["applicable"] is False


def test_declared_tags_widen_each_parent_context_and_a_refresh_keeps_them(tmp_path):
    root = _tree(tmp_path, roster=SIBLING_ROSTER)
    hats.write_record(
        root, REC, rows=["SR-001", "SR-002"], tags=["extra"], by="test session"
    )
    hats.write_record(root, REC)
    data = _parsed(root)
    assert data["decomposition"]["tags"] == ["extra"]
    assert data["perspective"]["EXTRA-OPS"]["applicable"] is True
    assert data["perspective"]["EXTRA-SCRIPTS"]["applicable"] is True


def test_a_refresh_keeps_an_earlier_recorded_on(tmp_path):
    root = _tree(tmp_path)
    _write(root)
    path = root / REC
    text = re.sub(
        r'recorded_on = "[^"]*"',
        'recorded_on = "2000-01-01"',
        path.read_text(encoding="utf-8"),
    )
    path.write_text(text, encoding="utf-8")
    hats.write_record(root, REC)
    assert _parsed(root)["decomposition"]["recorded_on"] == "2000-01-01"


def test_a_moved_parent_set_is_stale(tmp_path):
    root = _tree(tmp_path)
    _write(root)
    _set_no_finding(root, "SCRIPTS", "Touches no script.")
    (root / "docs/requirements/system-requirements.toml").write_text(
        SRS.replace('sn_refs = ["SN-002"]', 'sn_refs = ["SN-001"]'), encoding="utf-8"
    )
    findings = hats.record_findings(root, REC)
    assert any(
        c == "STALE" and t.startswith("parents are now SN-001;") for c, t in findings
    ), findings


def test_missing_is_judged_on_the_regeneration(tmp_path):
    root = _tree(
        tmp_path,
        srs=SRS.replace(
            'hat_refs = ["ALWAYS-ON"]', 'hat_refs = ["ALWAYS-ON", "SCRIPTS"]'
        ),
    )
    _write(root)
    (root / "docs/requirements/system-requirements.toml").write_text(
        SRS, encoding="utf-8"
    )
    findings = hats.record_findings(root, REC)
    assert _classes(findings) == ["MISSING", "STALE"]
    assert any(c == "MISSING" and "SCRIPTS" in t for c, t in findings)


def test_an_interrupted_write_leaves_the_previous_record_whole(tmp_path, monkeypatch):
    root = _tree(tmp_path)
    _write(root)
    before = (root / REC).read_bytes()

    def boom(src, dst):
        raise OSError("interrupted")

    monkeypatch.setattr(
        hats, "write_atomic", functools.partial(observation.write_atomic, replace=boom)
    )
    with pytest.raises(OSError, match="interrupted"):
        _write(root, rows=("SR-001",))
    assert (root / REC).read_bytes() == before


def test_a_moved_predicate_and_a_new_hat_are_reported(tmp_path):
    root = _tree(tmp_path)
    _write(root)
    _set_no_finding(root, "SCRIPTS", "Touches no script.")
    (root / "docs/requirements/hats.toml").write_text(
        ROSTER.replace(
            "applies_when = 'tags contains \"scripts\"'",
            'applies_when = \'tags contains "scripts" or tags contains "ops"\'',
        )
        + """
[hat.LATE]
applies_when = 'tags contains "nothing-carries-this"'
asks = "q"
listens_for = "f"
""",
        encoding="utf-8",
    )
    findings = hats.record_findings(root, REC)
    assert any(
        c == "STALE" and t.startswith("SCRIPTS: applies_when") for c, t in findings
    ), findings
    assert any(
        c == "STALE" and t.startswith("LATE has no entry") for c, t in findings
    ), findings
    assert _classes(findings) == ["STALE"]
