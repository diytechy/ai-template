"""The delegated-decisions record: its format, the dial that owes it, and the
note a delegated session is handed — the in-memory half (SR-225).

A delegated run makes calls on the owner's behalf that are too settled for a
pending open item and not settled enough for the log. The record is where the
owner is TOLD about them: one TOML file per run, one table per decision, each
carrying the four disclosure fields and a `review` cell the owner fills in place.
The `[attestation] decision_recording` dial decides whether a run owes one.

Nothing here touches git: the merge-slot rung that refuses a lane closing
without its record is driven on a scaffold in `test_decision_record_merge.py`.

  * TC-292 — the dial: three values, an absent key reading `off`, one
    normalization (trim, lowercase) shared by the reader and the validator, an
    unrecognized value refused where the policy file is checked and read as
    asking for a record.
  * TC-293 — the `kitlib.decisions` API (IF-256), clause by clause: a sound
    record yields nothing; each required key's absence, non-text value and
    blank value, a non-table entry, a malformed hoist and a dangling hoist are
    reported by entry; extra keys are not judged; the findings never raise; a
    `-000` entry is inert and the shipped template sound; every close owes a
    record under a recording dial; and the note reaches a build and an
    adjudication session and never a review session.
"""

import sys
import tomllib

import pytest
from conftest import KIT, ROOT, SCRIPTS, load_script

if str(SCRIPTS) not in sys.path:  # the kit's script-sibling import idiom
    sys.path.insert(0, str(SCRIPTS))

from kitlib import decisions as kd  # noqa: E402

ac = load_script("agent_common")
al = load_script("agent_loop")

NL = "\n"

SOUND = """\
high_risk = ["D-002"]

[decision.D-001]
decided = "kept the helper in its module"
alternative = "moved it to a sibling"
reversal_cost = "one commit"
why_not_escalated = "no registry or kit file moved"
review = ""

[decision.D-002]
decided = "authored a derived requirement"
alternative = "cited a need whose text does not demand it"
reversal_cost = "an amendment and a re-approval"
why_not_escalated = "the row is Drafted; approval stays the owner's act"
review = "fine by me"
"""


def _docs(tmp_path, body):
    docs = tmp_path / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "process.toml").write_text(body, encoding="utf-8", newline="\n")
    return docs


def _dial(tmp_path, value):
    return _docs(tmp_path, "[attestation]\ndecision_recording = {}\n".format(value))


def _one_entry(key, literal):
    """A one-entry record whose `key` holds the TOML `literal`, every other
    required key a sound string."""
    lines = ["high_risk = []", "[decision.D-001]"]
    lines += [
        "{} = {}".format(k, literal if k == key else '"x"') for k in kd.REQUIRED_KEYS
    ]
    return NL.join(lines) + NL


# --- TC-292: the dial -----------------------------------------------------------


@pytest.mark.parametrize("mode", ["off", "record", "escalate-first"])
def test_each_declared_value_reads_as_itself(tmp_path, mode):
    docs = _dial(tmp_path, '"{}"'.format(mode))
    assert ac.decision_recording(docs) == mode
    assert ac.config_conflicts(docs) == []


def test_an_undeclared_dial_reads_off(tmp_path):
    # The template's shipped value and the reading of a repo that never set it:
    # no obligation until an owner asks for one.
    assert ac.decision_recording(_docs(tmp_path, "[attestation]\n")) == "off"
    assert ac.decision_recording(tmp_path / "absent") == "off"


def test_an_unrecognized_value_is_refused_and_read_as_record(tmp_path):
    # A misspelling is a `str`, so the type check cannot see it. It is refused
    # loudly where the policy file is checked, naming the legal values, and the
    # reader keeps the obligation rather than silently recording nothing.
    docs = _dial(tmp_path, '"recrod"')
    conflicts = ac.config_conflicts(docs)
    assert len(conflicts) == 1, conflicts
    assert "decision_recording" in conflicts[0]
    for mode in kd.MODES:
        assert mode in conflicts[0]
    assert "rung" not in conflicts[0], "the rung dial's message is not this dial's"
    assert ac.decision_recording(docs) == "record"


@pytest.mark.parametrize(
    "declared,reads",
    [
        ('" record "', "record"),
        ('"Escalate-First"', "escalate-first"),
        ('"OFF"', "off"),
    ],
)
def test_a_padded_or_mixed_case_value_is_accepted_as_the_reader_reads_it(
    tmp_path, declared, reads
):
    # ONE normalization for the reader and the validator: a value the reader
    # honours is never refused, and one it would not honour is.
    docs = _dial(tmp_path, declared)
    assert ac.decision_recording(docs) == reads
    assert ac.config_conflicts(docs) == []


def test_the_reader_and_the_validator_share_one_normalization():
    for raw in (" record ", "RECORD", "Escalate-First", "\toff\n"):
        assert ac.mode_word(raw) == raw.strip().lower()
    assert ac.mode_word(3) is None


def test_a_wrong_typed_value_is_refused(tmp_path):
    docs = _dial(tmp_path, "true")
    assert any("decision_recording" in c for c in ac.config_conflicts(docs))
    assert ac.decision_recording(docs) == "record"


def test_the_template_ships_off_and_this_repo_records():
    template = tomllib.loads((KIT / "process.toml.template").read_text("utf-8"))
    live = tomllib.loads((ROOT / "docs" / "process.toml").read_text("utf-8"))
    assert template["attestation"]["decision_recording"] == "off"
    assert live["attestation"]["decision_recording"] == "record"


# --- TC-293: the format, the obligation, the session note ------------------------


def test_a_sound_record_yields_no_finding():
    assert kd.record_findings(SOUND) == []


def test_a_record_with_no_entries_is_sound():
    # A run that made no call worth the owner's eyes still closes with its
    # record; the empty hoist says so.
    assert kd.record_findings("high_risk = []\n") == []


@pytest.mark.parametrize("key", kd.REQUIRED_KEYS)
def test_each_missing_required_key_is_reported_by_entry(key):
    text = NL.join(ln for ln in SOUND.splitlines() if not ln.startswith(key + " "))
    findings = kd.record_findings(text)
    assert len(findings) == 2, findings
    assert all(key in f for f in findings)
    assert any("D-001" in f for f in findings) and any("D-002" in f for f in findings)


@pytest.mark.parametrize("key", kd.REQUIRED_KEYS)
@pytest.mark.parametrize("literal", ["7", "true", '["x"]', "{ a = 1 }"])
def test_each_required_key_holding_non_text_is_reported(key, literal):
    findings = kd.record_findings(_one_entry(key, literal))
    assert findings == ["D-001: `{}` is not text".format(key)]


@pytest.mark.parametrize("key", kd.REQUIRED_KEYS)
@pytest.mark.parametrize("literal", ['""', '"   "', '"\\t\\n"'])
def test_each_required_key_left_blank(key, literal):
    findings = kd.record_findings(_one_entry(key, literal))
    if key == "review":
        # The owner's cell: any string, blank included, is the owner's to write.
        assert findings == []
    else:
        assert findings == ["D-001: `{}` is blank".format(key)]


def test_a_non_table_entry_is_reported():
    findings = kd.record_findings('high_risk = []\n[decision]\nD-001 = "x"\n')
    assert len(findings) == 1 and "D-001" in findings[0] and "table" in findings[0]


def test_a_decision_key_that_is_not_a_table_is_reported():
    findings = kd.record_findings("high_risk = []\ndecision = 3\n")
    assert len(findings) == 1 and "decision" in findings[0]


@pytest.mark.parametrize("hoist", ['"D-002"', "[2]", '["D-002", 3]', "{ a = 1 }"])
def test_a_malformed_hoist_is_reported(hoist):
    text = SOUND.replace('high_risk = ["D-002"]', "high_risk = " + hoist)
    findings = kd.record_findings(text)
    assert len(findings) == 1 and "high_risk" in findings[0], findings


def test_extra_keys_on_an_entry_are_not_judged():
    text = SOUND.replace(
        'review = ""\n', 'review = ""\nconfidence = 0.4\ntouched = ["docs/x"]\n', 1
    )
    assert kd.record_findings(text) == []


@pytest.mark.parametrize(
    "text",
    [
        "",
        "decision = 3",
        "[decision]",
        "high_risk = [[]]",
        "high_risk = [1, 2]\n[decision.D-001]\ndecided = []",
        "[decision.D-001.deeper]\nx = 1",
        "\x00\xff garbage ===",
        "[[decision]]\ndecided = 1",
        "high_risk = []\n[decision.D-000]\n[decision.D-001]",
    ],
)
def test_the_findings_never_raise(text):
    findings = kd.record_findings(text)
    assert isinstance(findings, list) and all(isinstance(f, str) for f in findings)


def test_a_hoist_naming_an_absent_entry_is_reported():
    findings = kd.record_findings(SOUND.replace('["D-002"]', '["D-002", "D-009"]'))
    assert len(findings) == 1 and "D-009" in findings[0]


def test_a_missing_hoist_is_reported():
    findings = kd.record_findings(SOUND.replace('high_risk = ["D-002"]\n', ""))
    assert len(findings) == 1 and "high_risk" in findings[0]


def test_an_entry_id_outside_the_numbering_is_reported():
    findings = kd.record_findings(SOUND.replace("D-001]", "first]"))
    assert len(findings) == 1 and "first" in findings[0]


def test_an_unparseable_record_is_one_finding():
    findings = kd.record_findings("high_risk = [\n[decision.D-001\n")
    assert len(findings) == 1 and "TOML" in findings[0]


def test_a_000_entry_is_inert():
    # The template's example keeps it copy-ready: an entry numbered -000 is
    # never judged, even half-filled, and hoisting it is not a dangling name.
    text = 'high_risk = ["D-000"]\n\n[decision.D-000]\ndecided = "x"\n'
    assert kd.record_findings(text) == []


def test_the_shipped_template_is_sound_and_carries_the_example():
    text = (KIT / "decisions.template.toml").read_text(encoding="utf-8")
    assert kd.record_findings(text) == []
    data = tomllib.loads(text)
    example = data["decision"]["D-000"]
    assert set(kd.REQUIRED_KEYS) <= set(example)
    assert example["review"] == ""


def test_the_record_path_is_one_file_per_run():
    assert kd.record_path("wi-557-decisions") == "docs/decisions/wi-557-decisions.toml"
    # A branch name with a separator still names ONE file, never a directory.
    assert kd.record_path("build/wi-557") == "docs/decisions/build-wi-557.toml"


@pytest.mark.parametrize(
    "mode,outcomes,owed",
    [
        ("off", ["merged"], False),
        ("off", ["partial"], False),
        ("record", ["merged"], True),
        ("record", ["cancelled"], True),
        ("escalate-first", ["merged"], True),
        # EVERY delegated run closes with one record, a partial close included:
        # a lane the machinery closed with no session present is refused, and
        # the refusal is a hold for a person to write the record.
        ("record", ["partial"], True),
        ("escalate-first", ["partial"], True),
        ("record", ["partial", "merged"], True),
        ("record", [], False),
    ],
)
def test_which_closes_owe_a_record(mode, outcomes, owed):
    assert kd.owed(mode, outcomes) is owed


def test_the_session_note_names_the_path_only_under_a_recording_dial():
    assert kd.session_note("off", "wi-1-x") == ""
    note = kd.session_note("record", "wi-1-x")
    assert "docs/decisions/wi-1-x.toml" in note
    for key in kd.REQUIRED_KEYS:
        assert key in note
    assert "high_risk" in note
    assert "escalate-first" not in note
    ask_more = kd.session_note("escalate-first", "wi-1-x")
    assert "docs/decisions/wi-1-x.toml" in ask_more
    assert len(ask_more) > len(note), "escalate-first adds the prefer-the-exits rule"


def _worker(rows=None):
    return {
        "rows": rows or {},
        "train": "wi-9-x",
        "base": "",
        "rework": "",
        "assigned": [],
    }


def test_a_build_session_is_handed_the_note_by_the_dial(tmp_path, monkeypatch):
    # The one fork every non-review session takes appends the note, read from
    # the repository the session runs in.
    monkeypatch.setattr(al, "worker_prompt", lambda *a, **k: "BODY")
    args = (_worker(), "WI-9", "s", "", tmp_path / "reviews", {})
    _dial(tmp_path, '"record"')
    body, _verdict, hold, _brief = al.session_body(tmp_path, *args)
    assert hold is None
    assert body.startswith("BODY") and "docs/decisions/wi-9-x.toml" in body
    _dial(tmp_path, '"off"')
    assert al.session_body(tmp_path, *args)[0] == "BODY"


def test_an_adjudication_session_is_handed_the_note_too(tmp_path, monkeypatch):
    # The adjudicator is a delegated altitude that closes a lane, so its brief
    # carries the note through the same fork.
    monkeypatch.setattr(al.adjudicate_brief, "declared_brief", lambda row: "amendment")
    monkeypatch.setattr(
        al.adjudicate_brief, "compose", lambda root, row, vp, t: ("ADJ", None)
    )
    worker = _worker({"WI-9": {"SafetyClass": "adjudication"}})
    args = (worker, "WI-9", "s", "", tmp_path / "reviews", {})
    _dial(tmp_path, '"record"')
    body, _verdict, hold, brief = al.session_body(tmp_path, *args)
    assert hold is None and brief == "amendment"
    assert body.startswith("ADJ") and "docs/decisions/wi-9-x.toml" in body
    _dial(tmp_path, '"off"')
    assert al.session_body(tmp_path, *args)[0] == "ADJ"


def test_a_review_session_is_not_handed_the_note(tmp_path):
    # A reviewer closes nothing: its brief is composed apart from the fork that
    # carries the note, whatever the dial says.
    _dial(tmp_path, '"record"')
    text = al.reviewer_prompt(
        {"REVIEW-A": "REVIEW {verdict}"}, "REVIEW-A", "v.md", worker=_worker()
    )
    assert text.startswith("REVIEW v.md")
    assert "docs/decisions" not in text and "DECISIONS RECORD" not in text
