"""An accepted risk, bound to the acceptance act that accepted it (TC-234).

An assumption may carry a recorded accepted risk, and while that acceptance
stands it reads COVERED by it (SR-202). The acceptance is a judgment about one
assumption serving particular needs, so it is bound to their texts as they
stood in the act that accepted it: a later change to either, even one
re-accepted on its own, or a failed sample added after the act, reopens it,
and it reads UNPROVEN, naming the trigger, until an act accepts the risk
again. A passing result restores nothing: an assumption carries no evidence
level (operator ruling 2026-10-02), and a passed sample proves nothing beyond
itself. Time alone never reopens it, and the order of a failed sample is read
from commit ancestry, never from the timestamp the record carries.

Driven on real git repositories, with the acceptance act performed the way the
kit performs one (`baseline_snapshot.copy_live`, then a commit), so the
module is registered in `tests/conftest.py`'s `SLOW_MODULES`. The pure state
rule is `assumption_rules.accepted_risk_state`; the act is read from history by
`baseline_snapshot.risk_acceptance_act`.

Implements: TC-234
"""

import datetime
import subprocess

import pytest

from conftest import load_script, pin_autocrlf, run_py, SCRIPTS

CARRIER = load_script("spine_carrier")
SNAP = load_script("baseline_snapshot")
RULES = load_script("assumption_rules")
WRITER = load_script("record_observation")
import kitlib.observation as OBS  # noqa: E402

NEEDS_REL = "docs/requirements/stakeholder-needs.toml"
SR_REL = "docs/requirements/system-requirements.toml"
DA_REL = "docs/requirements/assumptions.toml"
TC_REL = "docs/test/test-cases.toml"
NOTES_REL = "docs/notes.md"

NEEDS = """
[need.SN-001]
need = "A reviewer can tell which requirements a claim about the world supports."
why = "A false claim hides behind a verified system."
priority = "M"
acceptance = "The reviewer names the requirements from the report alone."
status = "Accepted"

[need.SN-002]
need = "An adopter can resume work from the record alone."
why = "Sessions end mid-task."
priority = "S"
acceptance = "A fresh session names the next step from the record."
status = "Accepted"

[need.SN-009]
need = "An unrelated need."
why = "It serves nothing the assumption touches."
priority = "C"
acceptance = "Nothing here moves the risk."
status = "Accepted"
"""

REQUIREMENTS = """
[requirement.SR-001]
title = "Report the claims under each requirement"
sn_refs = ["SN-001"]
requirement = "The kit shall report the assumptions each requirement cites."
da_refs = ["DA-001"]
status = "Accepted"

[requirement.SR-002]
title = "Resume from the record"
sn_refs = ["SN-002"]
requirement = "The kit shall name the next step from the record."
da_refs = ["DA-001"]
status = "Accepted"

[requirement.SR-009]
title = "Unrelated"
sn_refs = ["SN-009"]
requirement = "The kit shall do something unrelated."
status = "Accepted"
"""

ASSUMPTIONS = """
[assumption.DA-001]
effect_at = ["B-01"]
assumption = "A reviewer reads the brief before accepting."
holds_when = "The brief is short enough to read in one sitting."
obstacle = "The brief grows past what one sitting reads."
falsifier = "An acceptance recorded before the brief was opened."
accepted_risk = "No reviewer population to sample yet; proceeding on the operator's say-so."
status = "Drafted"
standing = "active"
"""

TEST_CASES = """
[test.TC-001]
assumption_refs = ["DA-001"]
level = "System"
method = "A reviewer is watched approving a brief."
tier = "Release"
expected = "The brief is opened before the acceptance is recorded."
automated = "No"
evidence = "docs/notes.md"
status = "Accepted"
inputs = ["docs/notes.md"]
max_age = 30
sampling = "monitored"
"""

FRAME = """
[entity.EXT-001]
name = "Reviewer"
class = "operational"
description = "The person accepting a brief."
status = "Drafted"

[boundary.B-01]
entity = "EXT-001"
direction = "out"
carries = "the acceptance brief"
system = "operation"
status = "Drafted"
"""

FILES = {
    NEEDS_REL: NEEDS,
    SR_REL: REQUIREMENTS,
    DA_REL: ASSUMPTIONS,
    TC_REL: TEST_CASES,
    "docs/requirements/external.toml": FRAME,
    NOTES_REL: "What the reviewer is shown.\n",
}


def _git(root, *args):
    proc = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, encoding="utf-8"
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip()


def _commit(root, message):
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", message)
    return _git(root, "rev-parse", "HEAD")


def _edit(root, rel, old, new):
    path = root / rel
    text = path.read_text(encoding="utf-8")
    assert old in text, "fixture: {!r} not in {}".format(old, rel)
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


@pytest.fixture
def repo(tmp_path):
    """A repository whose DA-001, carrying an accepted risk, was accepted in
    an act: the row's Status flip and the record's copy in one commit."""
    root = tmp_path / "repo"
    root.mkdir()
    for rel, text in FILES.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text.lstrip("\n"), encoding="utf-8")
    _git(root, "init", "-q")
    pin_autocrlf(root)
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _commit(root, "draft the assumption")
    _edit(root, DA_REL, 'status = "Drafted"', 'status = "Accepted"')
    SNAP.copy_live(root, seed=True)
    act = _commit(root, "accept DA-001 and its accepted risk")
    return root, act


def _now():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)


def _utc(moment):
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def _state(root):
    """`(state, reasons)` for DA-001 as the checker composes it: the records
    on disk, the act from history. No clock is read."""
    (da,) = CARRIER.load(root / DA_REL, "DA-ID", keep_examples=False)
    tcs = CARRIER.load(root / TC_REL, "TC-ID", keep_examples=False)
    needs = CARRIER.load_needs(root / NEEDS_REL)
    records = OBS.read_records(root)
    view = SNAP.risk_acceptance_view(root, "DA-001")
    return RULES.accepted_risk_state(da, view, needs, tcs, records)


def _observe(root, outcome, observed=None, expires=None):
    """Write a record for TC-001 judging the notes as they are now."""
    observed = observed or _now() - datetime.timedelta(hours=1)
    expires = expires or observed + datetime.timedelta(days=30)
    record = {
        "tc": "TC-001",
        "outcome": outcome,
        "observed_at": _utc(observed),
        "provenance": "a reviewer watched at work",
        "expires": _utc(expires),
        "judged": WRITER.inputs_digest(root, [NOTES_REL]),
    }
    folder = root / OBS.OBSERVATIONS_DIR
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / OBS.record_name("TC-001", record["observed_at"])
    OBS.write_atomic(path, OBS.render(record))
    return path


def _reaccept(root):
    """Accept the risk again: an act re-accepting DA-001, its text unchanged by
    the act itself."""
    SNAP.copy_live(root, reaccepts={"DA-001"})
    return _commit(root, "re-accept DA-001's risk")


def _restorations(root):
    """From one reopened state: a current passing result restores nothing, and
    an act re-accepting the assumption re-binds the risk."""
    path = _observe(root, "pass")
    assert _state(root)[0] == RULES.RISK_UNPROVEN
    path.unlink()
    _reaccept(root)
    assert _state(root) == (RULES.RISK_COVERED, [])


# --- the act and the covered reading -------------------------------------------


def test_the_act_that_accepted_it_is_the_anchor(repo):
    root, act = repo
    anchor, reason = SNAP.risk_acceptance_act(root, "DA-001")
    assert anchor == act, reason


def test_a_risk_no_act_names_is_unanchored_and_no_history_is_walked(
    tmp_path, monkeypatch
):
    """With no acceptance act naming the assumption, nobody accepted its risk,
    so there is no anchor to find: the reader says so, naming the assumption
    and the act it owes, and walks no history of the live registry for a
    commit to bind it to. The risk was committed unchanged before an act that
    named other rows, so a walk would have found a commit to call its act."""
    root = tmp_path / "repo"
    root.mkdir()
    for rel, text in FILES.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text.lstrip("\n"), encoding="utf-8")
    _git(root, "init", "-q")
    pin_autocrlf(root)
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _commit(root, "draft the assumption, its accepted risk written")
    SNAP.copy_live(root, seed=True)
    _commit(root, "an act accepting the needs and requirements, not DA-001")
    calls = []
    real_git = SNAP._git

    def spy(where, argv, *rest, **kw):
        calls.append(list(argv))
        return real_git(where, argv, *rest, **kw)

    monkeypatch.setattr(SNAP, "_git", spy)
    anchor, reason = SNAP.risk_acceptance_act(root, "DA-001")
    assert anchor is None, reason
    assert "DA-001" in reason and "unanchored" in reason, reason
    assert "accept it in an acceptance act" in reason, reason
    walks = [argv for argv in calls if argv and argv[0] in ("log", "rev-list")]
    assert walks and all(DA_REL not in argv for argv in walks), walks
    state, reasons = _state(root)
    assert state == RULES.RISK_UNPROVEN
    assert any("DA-001" in r and "unanchored" in r for r in reasons), reasons


def test_with_no_evidence_an_accepted_risk_reads_covered(repo):
    root, _act = repo
    assert _state(root) == (RULES.RISK_COVERED, [])


def test_an_assumption_with_no_accepted_risk_has_no_risk_state(repo):
    root, _act = repo
    (da,) = CARRIER.load(root / DA_REL, "DA-ID", keep_examples=False)
    da = dict(da)
    da.pop("AcceptedRisk")
    assert RULES.accepted_risk_state(da, None, [], [], []) == (
        None,
        [],
    )


def test_two_identical_re_acceptances_on_one_day_are_two_acts(repo):
    """Each act is its own entry in the act ledger, so the latest act moves the
    anchor even when an earlier one the same day named the same rows in the
    same words: the second re-acceptance here re-binds the risk to the text it
    saw, and the first act's text no longer counts."""
    root, _act = repo
    _edit(root, DA_REL, "reads the brief", "reads the whole brief")
    _commit(root, "amend DA-001")
    first = _reaccept(root)
    assert _state(root) == (RULES.RISK_COVERED, [])
    _edit(root, DA_REL, "reads the whole brief", "reads every page of the brief")
    _commit(root, "amend DA-001 again")
    assert _state(root)[0] == RULES.RISK_UNPROVEN
    second = _reaccept(root)
    assert second != first
    assert SNAP.risk_acceptance_act(root, "DA-001")[0] == second
    assert _state(root) == (RULES.RISK_COVERED, [])


def test_the_prose_stamp_moves_no_anchor(repo):
    """The snapshot's README is prose for a human and nothing parses it: a line
    written into it by hand, however it is worded, is no act."""
    root, act = repo
    _edit(root, DA_REL, "reads the brief", "reads the whole brief")
    stamp = SNAP.snapshot_root(root) / SNAP.README
    stamp.write_text(
        (stamp.read_text(encoding="utf-8") if stamp.is_file() else "")
        + "- 2026-09-26 — refresh under acceptance. Copied: assumptions.toml "
        "(re-accepted: DA-001).\n",
        encoding="utf-8",
    )
    _commit(root, "amend DA-001 and write a stamp line by hand")
    assert SNAP.risk_acceptance_act(root, "DA-001")[0] == act
    assert _state(root)[0] == RULES.RISK_UNPROVEN


def test_a_malformed_act_ledger_in_history_refuses_rather_than_guesses(repo):
    """A ledger whose numbers repeat cannot say which entries a commit added,
    so the anchor is not read at all: the reason names the ledger, and the
    risk reads unproven until the ledger is repaired."""
    root, _act = repo
    _reaccept(root)
    ledger = SNAP.snapshot_root(root) / SNAP.ACTS
    _edit(root, "{}/{}".format(SNAP.SNAPSHOT_DIR, SNAP.ACTS), "seq = 2", "seq = 1")
    assert ledger.is_file()
    _commit(root, "renumber the ledger by hand")
    anchor, reason = SNAP.risk_acceptance_act(root, "DA-001")
    assert anchor is None and SNAP.ACTS in reason, reason
    state, reasons = _state(root)
    assert state == RULES.RISK_UNPROVEN
    assert any(SNAP.ACTS in r for r in reasons), reasons


# --- the three triggers, each with both restorations ----------------------------


def test_a_need_amended_then_re_accepted_on_its_own_still_reads_unproven(repo):
    root, act = repo
    _edit(
        root,
        NEEDS_REL,
        "The reviewer names the requirements from the report alone.",
        "The reviewer names the requirements and their needs from the report.",
    )
    _commit(root, "amend SN-001's acceptance")
    state, reasons = _state(root)
    assert state == RULES.RISK_UNPROVEN
    assert any("SN-001" in r for r in reasons), reasons
    # The need is re-accepted in a later act of its own: the record's copy of
    # the needs now holds the new text, and the risk still reads unproven,
    # because the comparison is with the act that accepted the risk.
    # Needs are compared tiers, so the act re-accepting the drifted need names
    # it (`--reaccepts`); naming the registry alone is refused.
    SNAP.copy_live(
        root, accepts={NEEDS_REL: "SN-001 re-accepted"}, reaccepts={"SN-001"}
    )
    _commit(root, "re-accept SN-001")
    assert SNAP.risk_acceptance_act(root, "DA-001")[0] == act
    state, reasons = _state(root)
    assert state == RULES.RISK_UNPROVEN
    assert any("SN-001" in r for r in reasons), reasons
    assert not any("SN-009" in r or "SN-002" in r for r in reasons), reasons
    _restorations(root)


def test_an_unrelated_needs_amendment_does_not_reopen_it(repo):
    root, _act = repo
    _edit(root, NEEDS_REL, "Nothing here moves the risk.", "Still nothing.")
    _commit(root, "amend SN-009")
    assert _state(root) == (RULES.RISK_COVERED, [])


def test_amending_the_assumptions_own_text_reads_unproven(repo):
    root, _act = repo
    _edit(
        root,
        DA_REL,
        "A reviewer reads the brief before accepting.",
        "A reviewer reads the whole brief before accepting.",
    )
    _commit(root, "amend DA-001")
    state, reasons = _state(root)
    assert state == RULES.RISK_UNPROVEN
    assert any("DA-001" in r and "Assumption" in r for r in reasons), reasons
    _restorations(root)


def test_a_failing_record_added_after_the_act_reads_unproven_whatever_its_timestamp(
    repo,
):
    root, _act = repo
    long_ago = datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc)
    path = _observe(
        root, "fail", observed=long_ago, expires=long_ago + datetime.timedelta(days=30)
    )
    _commit(root, "record a failed sample")
    state, reasons = _state(root)
    assert state == RULES.RISK_UNPROVEN
    assert any(path.name in r for r in reasons), reasons
    _restorations(root)


def test_a_failing_record_the_act_already_held_does_not_reopen_it(tmp_path):
    """Ordered by ancestry: a failure recorded before the act was known to it."""
    root = tmp_path / "repo"
    root.mkdir()
    for rel, text in FILES.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text.lstrip("\n"), encoding="utf-8")
    _git(root, "init", "-q")
    pin_autocrlf(root)
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _observe(root, "fail")
    _commit(root, "draft, with a failed sample on record")
    _edit(root, DA_REL, 'status = "Drafted"', 'status = "Accepted"')
    SNAP.copy_live(root, seed=True)
    _commit(root, "accept DA-001, accepting the risk over the failure")
    assert _state(root) == (RULES.RISK_COVERED, [])


# --- time, and history too shallow ------------------------------------------------


def test_advancing_the_clock_by_a_year_changes_nothing(repo):
    root, _act = repo
    # The rule takes no clock, so a year's passing is a record a year old: a
    # passing result, current or long expired, moves nothing either way.
    a_year_ago = _now() - datetime.timedelta(days=365)
    _observe(root, "pass", observed=a_year_ago)
    assert _state(root) == (RULES.RISK_COVERED, [])
    _observe(root, "pass")
    assert _state(root) == (RULES.RISK_COVERED, [])


def test_a_shallow_clone_missing_the_act_reads_unproven_with_the_reason(repo, tmp_path):
    root, _act = repo
    _edit(root, NOTES_REL, "What the reviewer is shown.", "What the reviewer sees.")
    _commit(root, "a later, unrelated commit")
    clone = tmp_path / "shallow"
    _git(tmp_path, "clone", "-q", "--depth", "1", root.as_uri(), str(clone))
    assert _git(clone, "rev-parse", "--is-shallow-repository") == "true"
    anchor, reason = SNAP.risk_acceptance_act(clone, "DA-001")
    assert anchor is None and "shallow" in reason, reason
    state, reasons = _state(clone)
    assert state == RULES.RISK_UNPROVEN
    assert any("shallow" in r for r in reasons), reasons


# --- the advisory, through the checker --------------------------------------------


def test_the_checker_reports_a_reopened_risk_naming_its_trigger(repo):
    root, _act = repo
    _edit(root, NEEDS_REL, "A fresh session names", "A fresh session always names")
    _commit(root, "amend SN-002's acceptance")
    proc = run_py([SCRIPTS / "trace.py", "--root", root], cwd=root)
    lines = [
        line
        for line in proc.stdout.splitlines()
        if "DA-001" in line and "accepted risk" in line
    ]
    assert len(lines) == 1, proc.stdout + proc.stderr
    assert "unproven" in lines[0] and "SN-002" in lines[0], lines[0]


# --- TC-500: the advisory words an unproven risk by why it reads unproven ---------
# Composed as the checker composes it: the act reader's view, read from real
# history, handed to the advisory rule beside the rows and records on disk.

RISK_LINE = (
    'accepted_risk = "No reviewer population to sample yet; proceeding on the '
    "operator's say-so.\"\n"
)


def _advisory(root):
    """The one advisory for DA-001's accepted risk, with the act reader's view
    it was read from."""
    (da,) = CARRIER.load(root / DA_REL, "DA-ID", keep_examples=False)
    tcs = CARRIER.load(root / TC_REL, "TC-ID", keep_examples=False)
    needs = CARRIER.load_needs(root / NEEDS_REL)
    view = SNAP.risk_acceptance_view(root, "DA-001")
    lines = RULES.accepted_risk_advisories(
        [da], tcs, needs, OBS.read_records(root), {"DA-001": view}
    )
    assert len(lines) == 1 and "DA-001" in lines[0], lines
    return lines[0], view


def _drafted_repo(tmp_path, assumptions=ASSUMPTIONS):
    """A repository holding the rows, DA-001 drafted, committed and in no act."""
    root = tmp_path / "repo"
    root.mkdir(parents=True)
    for rel, text in dict(FILES, **{DA_REL: assumptions}).items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text.lstrip("\n"), encoding="utf-8")
    _git(root, "init", "-q")
    pin_autocrlf(root)
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _commit(root, "draft the assumption")
    return root


def test_the_advisory_says_a_risk_an_act_accepted_has_reopened(repo):
    """A risk an act accepted, then undone by a change to the assumption's own
    text: the advisory says it has reopened and reads unproven until accepted
    again, naming the trigger.

    Implements: TC-500
    """
    root, _act = repo
    _edit(root, DA_REL, "reads the brief", "reads the whole brief")
    _commit(root, "amend DA-001")
    line, _view = _advisory(root)
    assert "has reopened" in line, line
    assert "unproven until the risk is accepted again" in line, line
    assert "DA-001's Assumption changed" in line, line
    assert "never accepted" not in line, line


def test_the_advisory_says_a_risk_no_act_accepted_was_never_accepted(tmp_path):
    """With the history and every act ledger on it read whole, no act there
    accepted the risk, either because no act names the assumption or because
    the acts naming it recorded no risk: the advisory says the risk was never
    accepted and that an act accepting it is what clears it, and claims no
    reopening.

    Implements: TC-500
    """
    root = _drafted_repo(tmp_path)
    SNAP.copy_live(root, seed=True)
    _commit(root, "an act accepting the needs and requirements, not DA-001")
    line, view = _advisory(root)
    assert view["act"] is None and view["unaccepted"] is True, view
    assert "never accepted" in line, line
    assert "unproven until an act accepts it" in line, line
    assert view["reason"] in line and "unanchored" in line, line
    assert "reopen" not in line and "accepted again" not in line, line

    assert RISK_LINE in ASSUMPTIONS, "fixture: the risk line moved"
    named = _drafted_repo(
        tmp_path / "named",
        ASSUMPTIONS.replace(RISK_LINE, "").replace('"Drafted"', '"Accepted"'),
    )
    SNAP.copy_live(named, seed=True)
    _commit(named, "accept DA-001 with no accepted risk")
    _edit(named, DA_REL, 'status = "Accepted"\n', 'status = "Accepted"\n' + RISK_LINE)
    _commit(named, "write the accepted risk after the act")
    line, view = _advisory(named)
    assert view["act"] is None and view["unaccepted"] is True, view
    assert "recorded no accepted risk" in view["reason"], view
    assert "never accepted" in line, line
    assert "unproven until an act accepts it" in line, line
    assert view["reason"] in line, line
    assert "reopen" not in line and "accepted again" not in line, line


def test_the_advisory_claims_neither_where_the_record_cannot_be_read_whole(
    repo, tmp_path
):
    """A shallow clone whose window lacks the act, and a malformed act ledger
    in the history, each leave the record unread whole: the advisory states the
    reading's own reason and claims neither a reopening nor a risk never
    accepted.

    Implements: TC-500
    """
    root, _act = repo
    _edit(root, NOTES_REL, "What the reviewer is shown.", "What the reviewer sees.")
    _commit(root, "a later, unrelated commit")
    clone = tmp_path / "shallow"
    _git(tmp_path, "clone", "-q", "--depth", "1", root.as_uri(), str(clone))
    line, view = _advisory(clone)
    assert view["act"] is None and view["unaccepted"] is False, view
    (reason,) = _state(clone)[1]
    assert "shallow" in reason and reason in line, (reason, line)
    assert "reopen" not in line and "never accepted" not in line, line

    _reaccept(root)
    _edit(root, "{}/{}".format(SNAP.SNAPSHOT_DIR, SNAP.ACTS), "seq = 2", "seq = 1")
    _commit(root, "renumber the ledger by hand")
    line, view = _advisory(root)
    assert view["act"] is None and view["unaccepted"] is False, view
    (reason,) = _state(root)[1]
    assert SNAP.ACTS in reason and reason in line, (reason, line)
    assert "reopen" not in line and "never accepted" not in line, line
