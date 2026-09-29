"""retire.py — a retired spine row leaves one record of its own (SR-226, LLR-286).

A superseded row is deleted, and ids are never reused, so a reference to a
spent id stays unambiguous but explains nothing. The command that deletes the
row writes its record in the same working tree, one file per id under
`docs/log.d/retired/`, and the traceability check reports a record that moved
after it landed and a spent id that has none. Both reports warn; neither fails.

Every case here drives a REAL git repository under `tmp_path`: whether a
record landed, and with what text, is read from history, and the fold that
must leave the records alone is the real `trunk_step.py --compile-log`. The
real `docs/` is never written.
"""

import subprocess
import tomllib

import pytest

from conftest import (
    SCRIPTS,
    load_script,
    make_minimal_project,
    pin_autocrlf,
    record_ids,
    run_py,
)

rt = load_script("retire")
tr = load_script("trace")

SR_TOML = """[requirement.SR-001]
title = "One"
requirement = "The kit shall do one thing."
status = "Drafted"

[requirement.SR-002]
title = "Two"
requirement = \"\"\"The kit shall do two things.
[not a header, inside a string]\"\"\"
status = "Approved"

# A comment that belongs to SR-003.
[requirement.SR-003]
title = "Three"
requirement = "The kit shall do three things."
status = "Drafted"
"""

SN_TOML = """[need.SN-001]
need = "A need."
status = "Approved"
"""

LLR_TOML = """[design.LLR-001]
title = "A design."
status = "Drafted"
"""

TC_TOML = """[test.TC-001]
method = "A method."
status = "Drafted"
"""

# SR-004 and SR-005 were spent before the record began; nothing else is.
WATERMARK = "LLR = 1\nSN = 1\nSR = 5\nTC = 1\n"

SR_PATH = "docs/requirements/system-requirements.toml"


def _git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, encoding="utf-8"
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _commit(root, message="step"):
    _git(root, "add", "-A")
    _git(root, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", message)
    return _git(root, "rev-parse", "HEAD").strip()


def _write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


@pytest.fixture
def repo(tmp_path):
    """A committed repository holding the four spine registries, a watermark
    with two spent SR ids, a log and its fragment drop-box."""
    _write(tmp_path, "docs/requirements/stakeholder-needs.toml", SN_TOML)
    _write(tmp_path, SR_PATH, SR_TOML)
    _write(tmp_path, "docs/requirements/low-level-requirements.toml", LLR_TOML)
    _write(tmp_path, "docs/test/test-cases.toml", TC_TOML)
    _write(tmp_path, "docs/id-watermark", WATERMARK)
    _write(tmp_path, "docs/log.md", "# Log\n\n## Seed\n\n- seeded.\n")
    _write(tmp_path, "docs/log.d/.gitkeep", "")
    _git(tmp_path, "init", "-q")
    pin_autocrlf(tmp_path)  # WI-461/WI-465; see conftest.pin_autocrlf
    _commit(tmp_path, "seed")
    return tmp_path


def _retire(root, *args):
    return run_py([SCRIPTS / "retire.py", "--root", root, *args], cwd=root)


def _record(root, row_id):
    return root / "docs" / "log.d" / "retired" / (row_id + ".md")


def _rows(root):
    return tomllib.loads((root / SR_PATH).read_text(encoding="utf-8"))["requirement"]


# --- (a) the deletion writes its record ---------------------------------------


def test_retiring_a_live_row_removes_it_and_writes_its_record(repo):
    before = _rows(repo)
    proc = _retire(
        repo,
        "SR-002",
        "--reason",
        "Folded into SR-003, which states both things.",
        "--successor",
        "SR-003",
        "--date",
        "2026-09-28",
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr

    after = _rows(repo)
    # Exactly that row went; every other row reads as it did, cell for cell,
    # and the comment above the next row stayed with it.
    assert set(after) == {"SR-001", "SR-003"}
    assert after == {k: v for k, v in before.items() if k != "SR-002"}
    text = (repo / SR_PATH).read_text(encoding="utf-8")
    assert "# A comment that belongs to SR-003.\n[requirement.SR-003]" in text

    data = rt.parse_fragment(
        _record(repo, "SR-002").read_text(encoding="utf-8"), "SR-002.md"
    )
    assert data == {
        "id": "SR-002",
        "date": "2026-09-28",
        "successor": "SR-003",
        "reason": "Folded into SR-003, which states both things.",
    }

    # Both changes sit in the working tree for ONE commit, and nothing else.
    changed = sorted(
        line[3:] for line in _git(repo, "status", "--porcelain", "-uall").splitlines()
    )
    assert changed == ["docs/log.d/retired/SR-002.md", SR_PATH]
    sha = _commit(repo, "retire SR-002")
    landed = _git(repo, "show", "--name-only", "--format=", sha).split()
    assert sorted(landed) == ["docs/log.d/retired/SR-002.md", SR_PATH]


def test_a_retirement_without_a_successor_records_none(repo):
    proc = _retire(repo, "SN-001", "--reason", "No longer asked for.")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    data = rt.parse_fragment(
        _record(repo, "SN-001").read_text(encoding="utf-8"), "SN-001.md"
    )
    assert data["successor"] == ""
    assert data["reason"] == "No longer asked for."
    # With no --date the record carries a calendar date.
    assert len(data["date"]) == 10 and data["date"][4] == "-"
    assert "need" not in tomllib.loads(
        (repo / "docs/requirements/stakeholder-needs.toml").read_text(encoding="utf-8")
    )


# --- (b) every refusal writes nothing -----------------------------------------


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(["SR-004", "--reason", "x"], id="not-live"),
        pytest.param(["SR-000", "--reason", "x"], id="placeholder"),
        pytest.param(["IF-001", "--reason", "x"], id="outside-the-spine"),
        pytest.param(["SR-002", "--reason", "   "], id="blank-reason"),
        pytest.param(
            ["SR-002", "--reason", "x", "--successor", "SR-004"],
            id="successor-not-live",
        ),
        pytest.param(
            ["SR-002", "--reason", "x", "--successor", "SR-002"],
            id="successor-is-itself",
        ),
        pytest.param(
            ["SR-002", "--reason", "x", "--date", "2026-9-28"], id="malformed-date"
        ),
    ],
)
def test_each_refusal_writes_nothing(repo, args):
    before = (repo / SR_PATH).read_bytes()
    proc = _retire(repo, *args)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "retire: REFUSED" in proc.stderr
    assert (repo / SR_PATH).read_bytes() == before
    assert not (repo / "docs" / "log.d" / "retired").exists()


def test_an_id_already_recorded_is_refused(repo):
    # A record is written once; a second retirement of the id never overwrites it.
    existing = _write(
        repo,
        "docs/log.d/retired/SR-002.md",
        rt.fragment_text("SR-002", "2026-01-01", "", "An earlier record."),
    )
    before = (repo / SR_PATH).read_bytes()
    proc = _retire(repo, "SR-002", "--reason", "Again.")
    assert proc.returncode == 1
    assert "retire: REFUSED" in proc.stderr
    assert (repo / SR_PATH).read_bytes() == before
    assert "An earlier record." in existing.read_text(encoding="utf-8")


# --- (c) the fold leaves the records in place ---------------------------------


def test_the_log_fold_leaves_retirement_records_in_place(repo):
    assert (
        _retire(repo, "SR-001", "--reason", "Gone.", "--date", "2026-09-28").returncode
        == 0
    )
    _write(
        repo, "docs/log.d/WI-1-session.md", "## WI-1 — a session\n\n- did a thing.\n"
    )
    _commit(repo, "retire SR-001, log the session")
    record = _record(repo, "SR-001").read_bytes()

    proc = run_py(
        [SCRIPTS / "trunk_step.py", "--root", repo, "--compile-log"], cwd=repo
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr

    assert not (repo / "docs" / "log.d" / "WI-1-session.md").exists()
    assert _record(repo, "SR-001").read_bytes() == record
    log = (repo / "docs" / "log.md").read_text(encoding="utf-8")
    assert "WI-1 — a session" in log
    assert "Gone." not in log


# --- (d) the census of ids retired before the record --------------------------


def test_the_seed_declares_the_spent_ids_once(repo):
    assert (
        _retire(repo, "SR-001", "--reason", "Gone.", "--date", "2026-09-28").returncode
        == 0
    )
    proc = _retire(repo, "--seed")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    census, problems = rt.read_census(repo)
    assert problems == []
    # SR-001 has its record, so only the two ids spent before it are declared.
    assert census == {"SR": {4, 5}}
    text = (repo / "docs" / "log.d" / "retired" / rt.CENSUS).read_text(encoding="utf-8")
    assert 'SR = "4-5"' in text

    again = _retire(repo, "--seed")
    assert again.returncode == 1
    assert "retire: REFUSED" in again.stderr


# --- (e) a spent id with no record ---------------------------------------------


def test_a_spent_id_without_a_record_is_reported(repo):
    found = rt.retirement_findings(repo)
    assert len(found) == 1
    assert "SR-004" in found[0] and "SR-005" in found[0]
    # A live id, an id above its mark and an empty space are never named.
    for quiet in ("SR-001", "SR-002", "SR-003", "SR-006", "SN-", "LLR-", "TC-"):
        assert quiet not in found[0]

    # Declared before the record began: silent.
    assert _retire(repo, "--seed").returncode == 0
    assert rt.retirement_findings(repo) == []

    # A row deleted by hand after the record began, with no record: named alone.
    text = (repo / SR_PATH).read_text(encoding="utf-8")
    (repo / SR_PATH).write_text(
        text.split("[requirement.SR-002]")[0], encoding="utf-8", newline="\n"
    )
    found = rt.retirement_findings(repo)
    assert len(found) == 1
    assert "SR-002" in found[0] and "SR-003" in found[0]
    assert "SR-004" not in found[0]

    # Recorded through the command: silent again.
    _write(repo, SR_PATH, SR_TOML)
    assert _retire(repo, "SR-002", "--reason", "Gone.").returncode == 0
    assert rt.retirement_findings(repo) == []


def test_legacy_registry_rows_are_live_and_only_a_spent_id_is_reported(scaffold):
    make_minimal_project(scaffold)
    record_ids(scaffold)
    watermark = scaffold / "docs" / "id-watermark"
    watermark.write_text(
        watermark.read_text(encoding="utf-8").replace("SR = 1", "SR = 2"),
        encoding="utf-8",
        newline="\n",
    )

    found = rt.retirement_findings(scaffold)

    assert len(found) == 1
    assert "SR-002" in found[0]
    for live in ("SN-001", "SR-001", "LLR-001", "TC-001"):
        assert live not in found[0]


def test_the_missing_rule_is_pure_over_its_four_sets():
    marks = {"SR": 6, "TC": 2, "IF": 9}
    live = {"SR": {1, 2}, "TC": {1, 2}}
    recorded = {"SR": {3}}
    census = {"SR": {4}}
    found = rt.missing_findings(marks, live, recorded, census)
    assert len(found) == 1
    assert "SR-005" in found[0] and "SR-006" in found[0]
    # IF is not a spine tier: its spent ids are not this rule's.
    assert "IF-" not in found[0]
    assert rt.missing_findings(marks, live, {"SR": {3, 5, 6}}, census) == []


def test_an_unreadable_record_is_reported(repo):
    _write(repo, "docs/log.d/retired/SR-004.md", "no front matter here\n")
    _write(
        repo,
        "docs/log.d/retired/SR-005.md",
        rt.fragment_text("SR-009", "2026-09-28", "", "Named for another id."),
    )
    found = rt.retirement_findings(repo)
    assert any("SR-004.md" in f for f in found)
    assert any("SR-005.md" in f for f in found)


# --- (f) a record moved after it landed ---------------------------------------


def test_a_record_changed_after_it_landed_is_reported(repo):
    assert _retire(repo, "--seed").returncode == 0
    assert (
        _retire(repo, "SR-002", "--reason", "Gone.", "--date", "2026-09-28").returncode
        == 0
    )
    landing = _commit(repo, "retire SR-002")
    assert rt.retirement_findings(repo) == []
    record = _record(repo, "SR-002")
    original = record.read_text(encoding="utf-8")

    # Edited in the working tree: reported, naming the record and where it landed.
    record.write_text(
        original.replace("Gone.", "Gone, for a better reason."),
        encoding="utf-8",
        newline="\n",
    )
    found = rt.retirement_findings(repo)
    assert len(found) == 1
    assert "SR-002.md" in found[0] and landing[:7] in found[0]

    # Committed: still reported.
    _commit(repo, "reword the record")
    assert len(rt.retirement_findings(repo)) == 1

    # Put back as it landed: silent again.
    record.write_text(original, encoding="utf-8", newline="\n")
    _commit(repo, "restore the record")
    assert rt.retirement_findings(repo) == []

    # Removed after landing: reported.
    record.unlink()
    _commit(repo, "remove the record")
    found = [f for f in rt.retirement_findings(repo) if "SR-002.md" in f]
    assert len(found) == 1 and "removed" in found[0]


def test_an_uncommitted_record_is_not_an_edit(repo):
    assert _retire(repo, "--seed").returncode == 0
    _commit(repo, "seed the census")
    assert _retire(repo, "SR-003", "--reason", "Gone.").returncode == 0
    assert rt.retirement_findings(repo) == []


def test_off_git_the_edit_report_is_silent(tmp_path):
    _write(tmp_path, SR_PATH, SR_TOML)
    _write(tmp_path, "docs/id-watermark", "SR = 3\n")
    _write(
        tmp_path,
        "docs/log.d/retired/SR-009.md",
        rt.fragment_text("SR-009", "2026-09-28", "", "Gone."),
    )
    assert rt.edited_findings(tmp_path) == []


# --- (g) the reports warn and never fail --------------------------------------


def test_the_reports_never_change_the_exit_code():
    findings = tr.Findings(retired_advisories=["a spent id has no record"])

    class Args:
        strict = True
        strict_integrity = True

    assert tr.exit_code(findings, Args()) == 0


def test_trace_prints_the_reports_as_advisories(scaffold):
    sr = scaffold / SR_PATH
    sr.write_text(
        sr.read_text(encoding="utf-8")
        + '\n[requirement.SR-001]\ntitle = "One"\nrequirement = "The kit shall do one '
        'thing."\nstatus = "Drafted"\n',
        encoding="utf-8",
        newline="\n",
    )
    bump = run_py(
        [SCRIPTS / "trace.py", "--root", scaffold, "--bump-ids"], cwd=scaffold
    )
    assert bump.returncode == 0, bump.stdout + bump.stderr
    sr.write_text(
        sr.read_text(encoding="utf-8").split("\n[requirement.SR-001]")[0] + "\n",
        encoding="utf-8",
        newline="\n",
    )

    proc = run_py(
        [SCRIPTS / "trace.py", "--root", scaffold, "--strict-integrity"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    lines = [ln for ln in proc.stdout.splitlines() if "SR-001" in ln]
    assert lines and all(ln.startswith("WARNING (advisory):") for ln in lines)


# --- fix round: the census and reservations -----------------------------------


def test_the_seed_never_declares_an_excluded_id(repo):
    # SR-005 is reserved by a lane still building: it is not yet a row, and it
    # is not retired either, so the census must not say it is.
    proc = _retire(repo, "--seed", "--exclude", "SR-005,TC-009")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    census, problems = rt.read_census(repo)
    assert problems == []
    assert census == {"SR": {4}}
    # Until its row lands, the reserved id is reported, warn-only, as unrecorded.
    found = rt.retirement_findings(repo)
    assert len(found) == 1 and "SR-005" in found[0]


def test_a_malformed_exclusion_is_refused(repo):
    proc = _retire(repo, "--seed", "--exclude", "SR-005,not-an-id")
    assert proc.returncode == 1
    assert "retire: REFUSED" in proc.stderr
    assert not (repo / "docs" / "log.d" / "retired" / rt.CENSUS).exists()


def test_the_census_is_replaced_only_before_it_lands(repo):
    census = repo / "docs" / "log.d" / "retired" / rt.CENSUS
    assert _retire(repo, "--seed").returncode == 0
    # Not yet committed: a re-seed with --replace rewrites it, and nothing else.
    before = _git(repo, "status", "--porcelain", "-uall")
    proc = _retire(repo, "--seed", "--replace", "--exclude", "SR-005")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert rt.read_census(repo)[0] == {"SR": {4}}
    assert _git(repo, "status", "--porcelain", "-uall") == before
    # Without --replace an existing census is still refused.
    assert _retire(repo, "--seed").returncode == 1
    # Once it has landed it is append-only: --replace is refused, unchanged.
    _commit(repo, "seed the census")
    landed = census.read_bytes()
    proc = _retire(repo, "--seed", "--replace")
    assert proc.returncode == 1
    assert "retire: REFUSED" in proc.stderr
    assert census.read_bytes() == landed


# --- fix round: a shallow clone cannot vouch for a record ---------------------


def test_a_shallow_clone_says_the_record_is_unverifiable(repo, tmp_path):
    assert _retire(repo, "--seed").returncode == 0
    assert _retire(repo, "SR-002", "--reason", "Gone.").returncode == 0
    _commit(repo, "retire SR-002")
    record = _record(repo, "SR-002")
    record.write_text(
        record.read_text(encoding="utf-8").replace("Gone.", "Rewritten."),
        encoding="utf-8",
        newline="\n",
    )
    _commit(repo, "edit the record after it landed")
    # The full history sees the edit.
    assert any("SR-002.md" in f for f in rt.edited_findings(repo))

    clone = tmp_path / "clone"
    _git(tmp_path, "clone", "-q", "--depth", "1", repo.as_uri(), str(clone))
    found = [f for f in rt.edited_findings(clone) if "SR-002.md" in f]
    assert len(found) == 1
    assert "append-only status unverifiable" in found[0]
    # The census's landing is past the boundary too, so it is named as well.
    assert any(rt.CENSUS in f for f in rt.edited_findings(clone))
    # Warn-only all the same: it is in the advisories, never an integrity class.
    assert any("unverifiable" in f for f in rt.retirement_findings(clone))


# --- fix round: the record reader holds the declared format -------------------


# A well-formed record, final newline included: the one body the format allows
# after the fence is none at all.
_FENCED = rt.fragment_text("SR-004", "2026-09-28", "", "Gone.")


def test_the_final_newline_alone_is_not_a_body():
    assert rt.parse_fragment(_FENCED, "SR-004.md")["id"] == "SR-004"
    assert rt.parse_fragment(_FENCED.rstrip("\n"), "SR-004.md")["id"] == "SR-004"


def _plant(repo, row_id, text):
    return _write(repo, "docs/log.d/retired/{}.md".format(row_id), text)


@pytest.mark.parametrize(
    "text, why",
    [
        pytest.param(
            '+++\nid = "SR-004"\ndate = "2026-09-28"\nsuccessor = ""\n'
            'reason = "Gone."\nextra = "x"\n+++\n',
            "keys",
            id="an-extra-key",
        ),
        pytest.param(
            '+++\nid = "SR-004"\ndate = "2026-09-28"\nreason = "Gone."\n+++\n',
            "keys",
            id="a-missing-key",
        ),
        pytest.param(
            '+++\nid = "SR-004"\ndate = "2026-09-28"\nsuccessor = ""\n'
            'reason = "Gone."\n+++\nA body the format does not have.\n',
            "after",
            id="a-body",
        ),
        pytest.param(
            '+++\nid = "SR-004"\ndate = "2026-99-99"\nsuccessor = ""\n'
            'reason = "Gone."\n+++\n',
            "date",
            id="an-impossible-date",
        ),
        pytest.param(_FENCED + "\n", "after", id="a-blank-line-after"),
        pytest.param(_FENCED + "   \n", "after", id="spaces-after"),
        pytest.param(_FENCED + "\t", "after", id="a-tab-after"),
    ],
)
def test_a_record_outside_the_declared_format_is_unreadable(repo, text, why):
    with pytest.raises(ValueError, match=why):
        rt.parse_fragment(text, "SR-004.md")
    _plant(repo, "SR-004", text)
    found = rt.retirement_findings(repo)
    assert any("unreadable retirement record" in f and "SR-004.md" in f for f in found)
    # The written form still reads back.
    assert rt.parse_fragment(
        rt.fragment_text("SR-004", "2026-09-28", "", "Gone."), "SR-004.md"
    )


def test_an_exclusion_run_excludes_every_id_in_it_and_nothing_else(repo):
    # SR-004 to SR-009 are spent; the run SR-005..007 is reserved by a lane
    # still building, and SR-004, SR-008 and SR-009 are genuinely spent.
    _write(repo, "docs/id-watermark", "LLR = 1\nSN = 1\nSR = 9\nTC = 1\n")
    proc = _retire(repo, "--seed", "--exclude", "SR-005..007")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert rt.read_census(repo)[0] == {"SR": {4, 8, 9}}
    assert rt.parse_exclusions("LLR-266..270,TC-9") == {
        "LLR": {266, 267, 268, 269, 270},
        "TC": {9},
    }
    # A run that ends below its start is refused, writing nothing.
    (repo / "docs" / "log.d" / "retired" / rt.CENSUS).unlink()
    proc = _retire(repo, "--seed", "--exclude", "SR-007..005")
    assert proc.returncode == 1 and "retire: REFUSED" in proc.stderr
    assert not (repo / "docs" / "log.d" / "retired" / rt.CENSUS).exists()
