"""The delegated-decisions record at the merge slot, on a git scaffold
(SR-225, TC-294).

A lane is one delegated run, and the merge slot is where it closes. Under the
`[attestation] decision_recording` dial at `record` or `escalate-first`, a lane
whose work closed complete or cancelled without its record at
`docs/decisions/<branch>.toml` is refused, naming that path; one carrying it
merges past the rung, a malformed entry reported rather than refused. Under
`off` the rung reads nothing. A lane closed partial owes one too: every
delegated run closes with its record, and a refusal is a hold for a person to
write it. A dial value outside its alphabet is refused as configuration BEFORE
any record is read, so a typo is never reported as a missing record; a padded
or mixed-case value reads as its trimmed, lowercased word.

Registered in `SLOW_MODULES`: every case claims and closes a lane in a real
repository.
"""

import pytest
from conftest import env_gate_skipif
from integrate_fixtures import T_VERDICT, _commit, _git, claim_repo, integ

pytestmark = env_gate_skipif("git")

RECORD = "docs/decisions/wi-401.toml"

SOUND = """\
high_risk = []

[decision.D-001]
decided = "kept the widget's name"
alternative = "renamed it"
reversal_cost = "one commit"
why_not_escalated = "touched no registry"
review = ""
"""


def _lane(tmp_path, directory, record=None, dial=None, rel=RECORD):
    """A claimed lane closed into `directory`, optionally carrying `record` at
    `rel` (its run's path by default), with the trunk declaring `dial` (None
    declares nothing)."""
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    _git(root, "checkout", "-q", "wi-401")
    if record is not None:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(record, encoding="utf-8", newline="\n")
        _git(root, "add", rel)
    dest = root / "docs" / "archive" / "work" / directory
    dest.mkdir(parents=True, exist_ok=True)
    _git(
        root,
        "mv",
        "docs/work/active/wi-401/WI-401-widget.md",
        "docs/archive/work/{}/WI-401-widget.md".format(directory),
    )
    _commit(root, "close: WI-401 -> {}".format(directory), when=T_VERDICT)
    _git(root, "checkout", "-q", "main")
    if dial is not None:
        # A dial already written as a TOML literal (padded, mixed case) is
        # declared as given; a bare word is quoted.
        literal = dial if dial.startswith('"') else '"{}"'.format(dial)
        (root / "docs" / "process.toml").write_text(
            "[attestation]\ndecision_recording = {}\n".format(literal),
            encoding="utf-8",
            newline="\n",
        )
    return root


def _ladder(root):
    return integ._merge_refusal(root, "wi-401", ["WI-401"])[1]


@pytest.mark.parametrize("dial", ["record", "escalate-first"])
@pytest.mark.parametrize("directory", ["complete", "cancelled"])
def test_a_recording_dial_refuses_a_close_without_its_record(tmp_path, dial, directory):
    root = _lane(tmp_path, directory, dial=dial)
    refusal = _ladder(root)
    assert refusal is not None and RECORD in refusal
    assert "nothing was merged" in refusal


@pytest.mark.parametrize("dial", [None, "off"])
def test_the_off_dial_reads_nothing(tmp_path, dial):
    root = _lane(tmp_path, "complete", dial=dial)
    refusal = _ladder(root)
    assert refusal is None or RECORD not in refusal
    assert integ._decision_record_refusal(root, "wi-401", {"WI-401": "merged"}) is None


@pytest.mark.parametrize("dial", ["record", "escalate-first"])
def test_a_lane_carrying_its_record_passes_the_rung(tmp_path, dial, capsys):
    root = _lane(tmp_path, "complete", record=SOUND, dial=dial)
    refusal = _ladder(root)
    assert refusal is None or RECORD not in refusal
    assert integ._decision_record_refusal(root, "wi-401", {"WI-401": "merged"}) is None
    assert "decisions record" not in capsys.readouterr().out


def test_a_malformed_entry_is_reported_and_does_not_refuse(tmp_path, capsys):
    malformed = SOUND.replace('alternative = "renamed it"\n', "")
    root = _lane(tmp_path, "complete", record=malformed, dial="record")
    assert integ._decision_record_refusal(root, "wi-401", {"WI-401": "merged"}) is None
    out = capsys.readouterr().out
    assert RECORD in out and "D-001" in out and "alternative" in out


@pytest.mark.parametrize("dial", ["record", "escalate-first"])
def test_a_partial_close_without_its_record_is_refused_too(tmp_path, dial):
    root = _lane(tmp_path, "partial", dial=dial)
    refusal = integ._decision_record_refusal(root, "wi-401", {"WI-401": "partial"})
    assert refusal is not None and RECORD in refusal
    assert "nothing was merged" in refusal


def test_a_partial_close_carrying_its_record_passes_the_rung(tmp_path):
    root = _lane(tmp_path, "partial", record=SOUND, dial="record")
    assert integ._decision_record_refusal(root, "wi-401", {"WI-401": "partial"}) is None


def test_a_dial_typo_is_refused_as_configuration_before_any_record(tmp_path):
    root = _lane(tmp_path, "complete", dial="recrod")
    refusal = _ladder(root)
    assert refusal is not None and "decision_recording" in refusal
    assert "recrod" in refusal and RECORD not in refusal


@pytest.mark.parametrize("dial", ['" record "', '"Record"', '"ESCALATE-FIRST"'])
def test_a_padded_or_mixed_case_dial_reads_as_its_word(tmp_path, dial):
    root = _lane(tmp_path, "complete", dial=dial)
    refusal = _ladder(root)
    assert refusal is not None and RECORD in refusal, refusal
    home = tmp_path / "carrying"
    home.mkdir()
    carrying = _lane(home, "complete", record=SOUND, dial=dial)
    refusal = _ladder(carrying)
    assert refusal is None or (
        "decision_recording" not in refusal and RECORD not in refusal
    )


def test_a_branch_name_no_record_can_carry_is_refused(tmp_path):
    # WI-818 dispute 1: `#` is a valid branch character, and no record name
    # carries it. The lane's tree holds `owner-cleanup.toml`, another run's
    # record, which must not meet the rung: a name no record can carry is an
    # absent record, refused when one is owed.
    other = "docs/decisions/owner-cleanup.toml"
    root = _lane(tmp_path, "complete", record=SOUND, dial="record", rel=other)
    _git(root, "branch", "-m", "wi-401", "owner#cleanup")
    outcomes = {"WI-401": "merged"}
    refusal = integ._decision_record_refusal(root, "owner#cleanup", outcomes)
    assert refusal is not None and "owner#cleanup" in refusal, refusal
    assert "'#'" in refusal and "nothing was merged" in refusal
    assert other not in refusal
