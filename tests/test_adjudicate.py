"""adjudicate.py — the disposition, the successor and the repair row
(SR-147/SR-151; LLR-177 + LLR-186; TC-171 + TC-180; the plan §7 policy).

Three properties are what these tests actually defend, and each is driven on the
shape that would break it rather than the shape that works:

  * **the policy is a policy, not a habit** — Complete must NOT draw a dedicated
    adjudicator on the ordinary path (running one over every completion is the
    existing verdict gate rebuilt under a new name), and it MUST draw one on
    each of the four declared triggers. Both directions are driven, because a
    policy that adjudicates everything is abandoned within a week and one that
    adjudicates nothing was never a policy. Sampling is driven for DETERMINISM
    specifically: the same event asked twice has to answer twice the same, or the
    loop stops being reproducible;

  * **the disposition never edits the claim** — the worker's outcome line is
    compared BYTE FOR BYTE after the ruling, and an override is checked to have
    moved the spec byte-identically to the corrected folder. The second ruling
    on one attempt is refused by name;

  * **exactly-once, by identity** — one attempt has one successor and one
    bar-failure has one repair row, and the second call drafts nothing. The
    dedup scan is driven with the candidate MOVED OUT of `draft/`, because the
    interesting repeat is the one that happens after the first candidate has
    been admitted and shipped.

The classification fixture is a REAL git repository, for `test_outcome.py`'s
reason: `outcome.classify_groups` reads a real `git diff`, so a fake would prove
something about the fake. The helpers are copied from that module's shapes
rather than imported — no test module in this suite imports another.
"""

import json
import shutil
import subprocess

import pytest
from conftest import SCRIPTS, env_gate_skipif, load_script

# The classification rung shells out to a real `git diff`, so the whole module
# is gated on git exactly as tests/test_outcome.py is.
pytestmark = env_gate_skipif("git")

adjudicate = load_script("adjudicate")
outcome = load_script("outcome")
config_mod = load_script("config")

TS = "2026-08-08T00:00:00Z"
CLAIM_BASE = "a" * 40
BRANCH_TIP = "b" * 40
TREE = "c" * 40
SCOPE = "0123456789abcdef"


# --- fixtures -----------------------------------------------------------------


def _spec_text(wi_id, title, extra=""):
    return (
        "+++\n"
        'id = "{}"\n'
        'title = "{}"\n'
        "{}"
        "+++\n"
        "\n## Context\n\n"
        "The obligation as filed.\n".format(wi_id, title, extra)
    )


def _tree(tmp_path, *, folder="partial", wi_id="WI-041", title="An attempt"):
    """A minimal repo-shaped tree: the work folders, one terminal spec and an
    empty event ledger directory."""
    root = tmp_path / "repo"
    for name in ("draft", "queued", "complete", "cancelled", "partial"):
        (root / "docs" / "work" / name).mkdir(parents=True, exist_ok=True)
    (root / "docs" / "events").mkdir(parents=True, exist_ok=True)
    spec = root / "docs" / "work" / folder / "{}-slug.md".format(wi_id)
    spec.write_text(_spec_text(wi_id, title), encoding="utf-8", newline="\n")
    return root


def _outcome_event(root, wi_id="WI-041", verdict="partial", **facts):
    event, findings = outcome.write_outcome(
        root,
        wi_id,
        verdict,
        CLAIM_BASE,
        BRANCH_TIP,
        SCOPE,
        ts=TS,
        commits=facts.pop("commits", [BRANCH_TIP]),
        checks=facts.pop("checks", [{"step": "tests", "result": "1 passed"}]),
        **facts,
    )
    assert findings == [], findings
    return event


def _failure_event(root, step="tests", output="AssertionError: boom", **kw):
    event, findings = outcome.failure_event(root, TREE, step, output, ts=TS, **kw)
    assert findings == [], findings
    return event


def _ledger_lines(root):
    path = root / "docs" / "events" / "outcomes.jsonl"
    return path.read_text(encoding="utf-8").splitlines()


def _complete_payload(**over):
    """A `complete` outcome event with NO evidence gaps — the baseline the
    trigger tests perturb one field at a time."""
    payload = {
        "schema": 1,
        "kind": "outcome",
        "wi": "WI-041",
        "outcome": "complete",
        "claim_base": CLAIM_BASE,
        "branch_tip": BRANCH_TIP,
        "scope": SCOPE,
        "files": ["a.py"],
        "commits": [BRANCH_TIP],
        "checks": [{"step": "tests", "result": "1 passed"}],
        "blockers": [],
        "unmet": [],
        "rationale": "",
    }
    payload.update(over)
    payload["id"] = adjudicate.event_id(payload)
    return payload


def _cfg(**over):
    """A `config.Config` over the declared defaults with the named dials moved."""
    values = dict(config_mod.DEFAULTS)
    values.update(over)
    return config_mod.Config(values)


# --- the plan §7 policy -------------------------------------------------------


@pytest.mark.parametrize(
    "verdict,expected",
    [("partial", "outcome-partial"), ("cancelled", "outcome-cancelled")],
)
def test_partial_and_cancelled_always_adjudicate(verdict, expected):
    """Something was owed and did not arrive, so the party that stopped is not
    the one who decides what happens to the rest — whatever the config says."""
    event = _complete_payload(outcome=verdict)
    cfg = _cfg(**{"outcomes.complete_sampling_rate": 0.0})
    assert adjudicate.needs_adjudication(event, {"SafetyClass": "ordinary"}, cfg) == (
        expected,
    )


def test_complete_with_an_approving_review_does_not_adjudicate():
    """THE LOAD-BEARING NEGATIVE. Complete's verdict already comes from the
    independent reviewer plus the composed-tree bar; drawing an adjudicator here
    would be a second verdict from no new evidence."""
    assert (
        adjudicate.needs_adjudication(
            _complete_payload(), {"SafetyClass": "ordinary"}, _cfg(), review="APPROVE"
        )
        == ()
    )


def test_complete_with_a_disagreeing_review_adjudicates():
    triggers = adjudicate.needs_adjudication(
        _complete_payload(),
        {"SafetyClass": "ordinary"},
        _cfg(),
        review={"verdict": "CHANGES-REQUESTED"},
    )
    assert triggers == ("review-disagrees",)


def test_a_declared_review_round_with_no_verdict_adjudicates():
    """ "Complete needs no adjudicator" is an argument FROM the review. With the
    declared review missing, the argument is missing too."""
    cfg = _cfg(**{"policy.review_rounds": 1})
    assert adjudicate.needs_adjudication(
        _complete_payload(), {"SafetyClass": "ordinary"}, cfg
    ) == ("review-disagrees",)


def test_zero_declared_review_rounds_is_not_a_missing_review():
    """A repo that declared no review is not missing one — refusing to tell the
    two apart would adjudicate every completion in a review-free repo."""
    cfg = _cfg(**{"policy.review_rounds": 0})
    assert (
        adjudicate.needs_adjudication(
            _complete_payload(), {"SafetyClass": "ordinary"}, cfg
        )
        == ()
    )


@pytest.mark.parametrize(
    "field,value,gap",
    [
        ("scope", "", "no-scope-digest"),
        ("scope", "not-a-digest", "no-scope-digest"),
        ("checks", [], "no-checks"),
        ("commits", [], "no-commits"),
        ("unmet", ["the second acceptance criterion"], "unmet-criteria"),
    ],
)
def test_incomplete_scope_or_bar_evidence_adjudicates(field, value, gap):
    event = _complete_payload(**{field: value})
    assert adjudicate.evidence_gaps(event) == [gap]
    triggers = adjudicate.needs_adjudication(
        event, {"SafetyClass": "ordinary"}, _cfg(), review="APPROVE"
    )
    assert triggers == ("evidence-incomplete",)


@pytest.mark.parametrize("key", ["SafetyClass", "safety_class"])
def test_a_risk_class_adjudicates_in_either_row_spelling(key):
    """The parsed registry row and the raw frontmatter both reach this policy;
    reading only one would make the trigger depend on the caller's parser."""
    triggers = adjudicate.needs_adjudication(
        _complete_payload(), {key: "spine"}, _cfg(), review="APPROVE"
    )
    assert triggers == ("safety-class",)


def test_an_unclassified_row_fails_closed_into_adjudication():
    triggers = adjudicate.needs_adjudication(
        _complete_payload(), {}, _cfg(), review="APPROVE"
    )
    assert triggers == ("safety-class",)
    assert adjudicate.safety_class_of({}) == "unclassified"


def test_a_class_outside_the_risk_set_does_not_adjudicate():
    cfg = _cfg(**{"outcomes.risk_safety_classes": ("spine",)})
    assert (
        adjudicate.needs_adjudication(
            _complete_payload(), {"SafetyClass": "gate"}, cfg, review="APPROVE"
        )
        == ()
    )


def test_sampling_at_zero_never_draws_and_at_one_always_does():
    event = _complete_payload()
    never = _cfg(**{"outcomes.complete_sampling_rate": 0.0})
    always = _cfg(**{"outcomes.complete_sampling_rate": 1.0})
    row = {"SafetyClass": "ordinary"}
    assert adjudicate.needs_adjudication(event, row, never, review="APPROVE") == ()
    assert adjudicate.needs_adjudication(event, row, always, review="APPROVE") == (
        "sampling",
    )


def test_sampling_is_deterministic_given_the_event():
    """A random draw would adjudicate a tree on one run and not the next, so no
    run could be reproduced. The bucket is a function of the event id, which is
    a function of the facts — so the answer is stable, and it straddles a rate
    set either side of the event's own bucket."""
    event = _complete_payload()
    bucket = adjudicate.sampling_bucket(event)
    assert 0.0 <= bucket < 1.0
    assert adjudicate.sampling_bucket(event) == bucket
    row = {"SafetyClass": "ordinary"}
    under = _cfg(**{"outcomes.complete_sampling_rate": bucket})
    over = _cfg(**{"outcomes.complete_sampling_rate": min(1.0, bucket + 1e-6)})
    # Two calls each: the same tree must answer the same way both times.
    assert [
        adjudicate.needs_adjudication(event, row, under, review="APPROVE")
        for _ in range(2)
    ] == [(), ()]
    assert [
        adjudicate.needs_adjudication(event, row, over, review="APPROVE")
        for _ in range(2)
    ] == [("sampling",), ("sampling",)]


def test_sampling_bucket_derives_an_absent_id_rather_than_drawing():
    payload = _complete_payload()
    stamped = adjudicate.sampling_bucket(payload)
    del payload["id"]
    assert adjudicate.sampling_bucket(payload) == stamped


def test_an_unreadable_outcome_word_fails_closed():
    """Only a hand-edited ledger can produce one; the safe reading of a record
    nobody can parse is that somebody has to look at it."""
    event = _complete_payload(outcome="finished-ish")
    assert adjudicate.needs_adjudication(event, {"SafetyClass": "spine"}, _cfg()) == (
        "outcome-unreadable",
    )


def test_triggers_come_back_in_the_declared_order():
    """Two runs that found the same triggers must print the same line."""
    event = _complete_payload(checks=[], unmet=["x"])
    cfg = _cfg(**{"outcomes.complete_sampling_rate": 1.0})
    triggers = adjudicate.needs_adjudication(
        event, {"SafetyClass": "spine"}, cfg, review="CHANGES-REQUESTED"
    )
    assert triggers == (
        "review-disagrees",
        "evidence-incomplete",
        "safety-class",
        "sampling",
    )
    assert list(triggers) == [t for t in adjudicate.TRIGGERS if t in triggers]


def test_the_policy_reads_declared_defaults_with_no_config():
    """A caller that holds no Config still gets the declared policy, not a
    second set of defaults invented here."""
    assert (
        adjudicate.needs_adjudication(
            _complete_payload(), {"SafetyClass": "ordinary"}, None, review="APPROVE"
        )
        == ()
    )


# --- the disposition ----------------------------------------------------------


def test_confirm_records_a_disposition_and_never_edits_the_claim(tmp_path):
    root = _tree(tmp_path)
    event = _outcome_event(root)
    before = _ledger_lines(root)

    written, findings = adjudicate.adjudicate(
        root, event["id"], "confirm", by="ANTHROPIC-OPUS-STRONG", rationale="matches"
    )
    assert findings == []
    after = _ledger_lines(root)
    # THE CLAIM IS UNTOUCHED: the worker's line is byte-identical and the
    # disposition is a new line beside it.
    assert after[: len(before)] == before
    assert len(after) == len(before) + 1
    assert written["kind"] == "disposition"
    assert written["corrected"] == ""
    assert written["moved"] == ""
    assert written["declared"] == "partial"
    # The spec did not move: a confirm corrects nothing.
    assert (root / "docs" / "work" / "partial" / "WI-041-slug.md").is_file()


def test_the_disposition_stores_the_ruling_under_reason_not_rationale(tmp_path):
    """`prompt_render`'s `worker-rationale` marker matches a serialized
    `"rationale":` key, so a disposition line fed to a later judge as ledger
    evidence would trip SR-156 and refuse an honest render."""
    root = _tree(tmp_path)
    event = _outcome_event(root)
    written, findings = adjudicate.adjudicate(
        root, event["id"], "confirm", by="judge", rationale="the record agrees"
    )
    assert findings == []
    assert written["reason"] == "the record agrees"
    assert "rationale" not in written
    assert '"rationale"' not in _ledger_lines(root)[-1]


def test_an_override_moves_the_byte_identical_spec(tmp_path):
    root = _tree(tmp_path)
    src = root / "docs" / "work" / "partial" / "WI-041-slug.md"
    original = src.read_bytes()
    event = _outcome_event(root)

    written, findings = adjudicate.adjudicate(
        root, event["id"], "override-complete", by="judge", rationale="all of it landed"
    )
    assert findings == []
    dest = root / "docs" / "work" / "complete" / "WI-041-slug.md"
    assert dest.is_file() and not src.exists()
    assert dest.read_bytes() == original
    assert written["corrected"] == "complete"
    assert written["moved"] == "docs/work/complete/WI-041-slug.md"


def test_the_effective_outcome_follows_the_override(tmp_path):
    root = _tree(tmp_path)
    event = _outcome_event(root)
    assert adjudicate.effective_outcome(root, event["id"])[0] == "partial"
    adjudicate.adjudicate(
        root, event["id"], "override-cancelled", by="judge", rationale="not wanted"
    )
    assert adjudicate.effective_outcome(root, event["id"])[0] == "cancelled"


def test_a_second_disposition_is_refused_by_name(tmp_path):
    root = _tree(tmp_path)
    event = _outcome_event(root)
    first, findings = adjudicate.adjudicate(
        root, event["id"], "confirm", by="judge", rationale=""
    )
    assert findings == []
    written, findings = adjudicate.adjudicate(
        root, event["id"], "override-complete", by="judge", rationale="second thoughts"
    )
    assert written is None
    assert any(first["id"] in f for f in findings), findings
    assert len(_ledger_lines(root)) == 2


def test_an_override_to_the_declared_outcome_is_refused(tmp_path):
    root = _tree(tmp_path)
    event = _outcome_event(root)
    written, findings = adjudicate.adjudicate(
        root, event["id"], "override-partial", by="judge", rationale=""
    )
    assert written is None
    assert any("already declared" in f for f in findings), findings


@pytest.mark.parametrize(
    "kwargs,needle",
    [
        ({"verdict": "looks-fine"}, "is not an adjudication verdict"),
        ({"by": "  "}, "names no adjudicator"),
    ],
)
def test_a_malformed_ruling_is_refused(tmp_path, kwargs, needle):
    root = _tree(tmp_path)
    event = _outcome_event(root)
    call = {"verdict": "confirm", "by": "judge"}
    call.update(kwargs)
    written, findings = adjudicate.adjudicate(
        root, event["id"], call["verdict"], by=call["by"], rationale=""
    )
    assert written is None
    assert any(needle in f for f in findings), findings
    assert len(_ledger_lines(root)) == 1


def test_an_unknown_event_is_refused_by_id(tmp_path):
    root = _tree(tmp_path)
    _outcome_event(root)
    written, findings = adjudicate.adjudicate(
        root, "deadbeefdeadbeef", "confirm", by="judge", rationale=""
    )
    assert written is None
    assert any("deadbeefdeadbeef" in f for f in findings), findings


def test_a_spec_in_the_wrong_folder_is_refused(tmp_path):
    """The folder and the ledger already disagree; an adjudicator rules on a
    record, and this one has two."""
    root = _tree(tmp_path)
    event = _outcome_event(root)
    src = root / "docs" / "work" / "partial" / "WI-041-slug.md"
    src.replace(root / "docs" / "work" / "complete" / "WI-041-slug.md")
    written, findings = adjudicate.adjudicate(
        root, event["id"], "confirm", by="judge", rationale=""
    )
    assert written is None
    assert any("complete/" in f and "partial" in f for f in findings), findings


def test_an_occupied_corrected_home_stops_the_ruling_before_it_is_recorded(tmp_path):
    """The move keeps the spec's filename, so anything already sitting at the
    corrected home carries this id too — and the one-item-one-file rung refuses
    first. What matters is WHERE it refuses: nothing is appended and nothing is
    overwritten, so the ledger never runs ahead of a move that cannot happen."""
    root = _tree(tmp_path)
    event = _outcome_event(root)
    occupant = root / "docs" / "work" / "complete" / "WI-041-slug.md"
    occupant.write_text("someone else\n", encoding="utf-8", newline="\n")
    written, findings = adjudicate.adjudicate(
        root, event["id"], "override-complete", by="judge", rationale=""
    )
    assert written is None
    assert any("2 specs" in f for f in findings), findings
    assert occupant.read_text(encoding="utf-8") == "someone else\n"
    assert len(_ledger_lines(root)) == 1


def test_a_duplicate_spec_id_is_refused(tmp_path):
    root = _tree(tmp_path)
    event = _outcome_event(root)
    (root / "docs" / "work" / "cancelled" / "WI-041-other.md").write_text(
        _spec_text("WI-041", "A twin"), encoding="utf-8", newline="\n"
    )
    written, findings = adjudicate.adjudicate(
        root, event["id"], "confirm", by="judge", rationale=""
    )
    assert written is None
    assert any("2 specs" in f for f in findings), findings


def test_insufficient_evidence_records_without_moving(tmp_path):
    root = _tree(tmp_path)
    event = _outcome_event(root)
    written, findings = adjudicate.adjudicate(
        root,
        event["id"],
        "insufficient-evidence",
        by="judge",
        rationale="the bar output is missing",
    )
    assert findings == []
    assert written["corrected"] == "" and written["moved"] == ""
    assert (root / "docs" / "work" / "partial" / "WI-041-slug.md").is_file()


def test_the_disposition_id_re_derives_from_its_own_payload(tmp_path):
    """Contracts §2's third property: a reader verifies the ledger rather than
    trusting it. `read_events` raises if any line's id stopped deriving."""
    root = _tree(tmp_path)
    event = _outcome_event(root)
    written, findings = adjudicate.adjudicate(
        root, event["id"], "confirm", by="judge", rationale=""
    )
    assert findings == []
    path = root / "docs" / "events" / "outcomes.jsonl"
    records = adjudicate.read_events(path)
    assert records[-1]["id"] == written["id"] == adjudicate.event_id(records[-1])


def test_a_tampered_ledger_line_refuses_rather_than_being_ruled_on(tmp_path):
    """A ledger repaired out of band is not a record to adjudicate. The id no
    longer derives from the payload, and that is the whole detection."""
    root = _tree(tmp_path)
    event = _outcome_event(root)
    path = root / "docs" / "events" / "outcomes.jsonl"
    record = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    record["outcome"] = "complete"
    path.write_text(json.dumps(record) + "\n", encoding="utf-8", newline="\n")
    written, findings = adjudicate.adjudicate(
        root, event["id"], "confirm", by="judge", rationale=""
    )
    assert written is None
    assert any("does not derive" in f for f in findings), findings


# --- the ledger helpers, pinned to outcome.py's (F5) --------------------------


def test_the_ledger_helpers_agree_with_outcomes(tmp_path):
    """The two modules append to ONE file, so a divergence here would give the
    ledger two id derivations and make every duplicate check answer wrong. The
    kit closes F5 duplication with a sync test rather than an extraction."""
    payloads = [
        {"schema": 1, "kind": "outcome", "wi": "WI-1", "outcome": "complete"},
        {"schema": 1, "kind": "disposition", "verdict": "confirm", "reason": "ok"},
        {"schema": 1, "kind": "bar-failure", "excerpt": "não-ascii — dash"},
    ]
    for payload in payloads:
        assert adjudicate.event_id(payload) == outcome.event_id(payload)

    path = tmp_path / "mixed.jsonl"
    adjudicate.append_event(path, dict(payloads[0], ts=TS))
    outcome.append_event(path, dict(payloads[1], ts=TS))
    mine = adjudicate.read_events(path)
    theirs = outcome.read_events(path)
    assert mine == theirs and len(mine) == 2


# --- the successor (LLR-177 / TC-171) -----------------------------------------


def _git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _attempt_repo(tmp_path):
    """A real repo whose branch changed two directories — so the classification
    has two groups to label, and a missing label is a state the test can build.
    """
    root = _tree(tmp_path)
    _git(root, "init", "-q", "-b", "trunk")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    (root / "src").mkdir()
    (root / "src" / "a.py").write_text("a = 1\n", encoding="utf-8", newline="\n")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "base")
    _git(root, "checkout", "-q", "-b", "wi-041")
    (root / "src" / "a.py").write_text("a = 2\n", encoding="utf-8", newline="\n")
    (root / "tests").mkdir()
    (root / "tests" / "t.py").write_text("t = 1\n", encoding="utf-8", newline="\n")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "attempt")
    _git(root, "checkout", "-q", "trunk")
    return root


LABELS = {"src": "keep", "tests": "quarantine"}


def test_a_successor_carries_only_the_remaining_scope_and_its_lineage(tmp_path):
    """TC-171. The successor names its predecessor and the outcome event, and
    carries only what is still owed — never the original revived."""
    root = _attempt_repo(tmp_path)
    original = (root / "docs" / "work" / "partial" / "WI-041-slug.md").read_bytes()
    event = _outcome_event(root)

    relpath, findings = adjudicate.draft_successor(
        root,
        event["id"],
        title="Finish the second half of the attempt",
        remaining="The reader half is still owed: parse the ledger and report it.",
        branch="wi-041",
        labels=LABELS,
        buildtier="medium",
    )
    assert findings == [], findings

    # It is a DRAFT. Queue entry is the admission transaction's act (plan §8).
    assert relpath.startswith("draft/")
    spec = root / "docs" / "work" / relpath
    text = spec.read_text(encoding="utf-8")
    lineage = adjudicate.read_lineage(text)
    assert lineage == {"supersedes": "WI-041", "source_event": event["id"]}
    assert "The reader half is still owed" in text
    # ONLY the remaining scope: the attempt's own obligation prose is not copied.
    assert "The obligation as filed." not in text
    assert 'buildtier = "medium"' in text

    # The original is untouched and still terminal — never edited, never requeued.
    assert (root / "docs" / "work" / "partial" / "WI-041-slug.md").read_bytes() == (
        original
    )
    assert not list((root / "docs" / "work" / "queued").glob("WI-*.md"))


def test_an_unlabelled_change_group_refuses_the_successor(tmp_path):
    """The 2026-08-03 incident (`08e6c08a`), mechanised: a successor in the
    queue reads as "the attempt is dealt with", so drafting one before the
    keep/discard/quarantine split would put the incident's precondition back."""
    root = _attempt_repo(tmp_path)
    event = _outcome_event(root)
    relpath, findings = adjudicate.draft_successor(
        root,
        event["id"],
        title="Finish it",
        remaining="the rest",
        branch="wi-041",
        labels={"src": "keep"},
    )
    assert relpath is None
    assert any("'tests'" in f and "label" in f for f in findings), findings
    assert not list((root / "docs" / "work" / "draft").glob("WI-*.md"))


def test_one_attempt_gets_one_successor(tmp_path):
    root = _attempt_repo(tmp_path)
    event = _outcome_event(root)
    call = dict(
        title="Finish it",
        remaining="the rest",
        branch="wi-041",
        labels=LABELS,
    )
    first, findings = adjudicate.draft_successor(root, event["id"], **call)
    assert findings == []
    second, findings = adjudicate.draft_successor(root, event["id"], **call)
    assert second is None
    assert any(first in f for f in findings), findings
    assert len(list((root / "docs" / "work" / "draft").glob("WI-*.md"))) == 1


def test_a_complete_attempt_has_no_remainder_to_carry(tmp_path):
    root = _attempt_repo(tmp_path)
    (root / "docs" / "work" / "partial" / "WI-041-slug.md").replace(
        root / "docs" / "work" / "complete" / "WI-041-slug.md"
    )
    event = _outcome_event(root, verdict="complete")
    relpath, findings = adjudicate.draft_successor(
        root,
        event["id"],
        title="More",
        remaining="the rest",
        branch="wi-041",
        labels=LABELS,
    )
    assert relpath is None
    assert any("effective outcome" in f for f in findings), findings


def test_an_override_to_partial_makes_a_cancelled_attempt_draftable(tmp_path):
    """The effective outcome is the adjudicated one — which is the whole reason
    the disposition exists."""
    root = _attempt_repo(tmp_path)
    (root / "docs" / "work" / "partial" / "WI-041-slug.md").replace(
        root / "docs" / "work" / "cancelled" / "WI-041-slug.md"
    )
    event = _outcome_event(root, verdict="cancelled")
    relpath, findings = adjudicate.draft_successor(
        root,
        event["id"],
        title="Finish it",
        remaining="the rest",
        branch="wi-041",
        labels=LABELS,
    )
    assert relpath is None and findings

    _written, findings = adjudicate.adjudicate(
        root, event["id"], "override-partial", by="judge", rationale="real work landed"
    )
    assert findings == []
    relpath, findings = adjudicate.draft_successor(
        root,
        event["id"],
        title="Finish it",
        remaining="the rest",
        branch="wi-041",
        labels=LABELS,
    )
    assert findings == [] and relpath.startswith("draft/")


@pytest.mark.parametrize(
    "remaining,needle",
    [
        ("   ", "states no remaining scope"),
        ("owed:\n\n## Deliverable\n\nnothing", "markdown heading"),
    ],
)
def test_unusable_remaining_scope_is_refused(tmp_path, remaining, needle):
    root = _attempt_repo(tmp_path)
    event = _outcome_event(root)
    relpath, findings = adjudicate.draft_successor(
        root,
        event["id"],
        title="Finish it",
        remaining=remaining,
        branch="wi-041",
        labels=LABELS,
    )
    assert relpath is None
    assert any(needle in f for f in findings), findings


# --- the repair row (LLR-186 / TC-180) ----------------------------------------


def test_remediation_first_repeat_and_different_step(tmp_path):
    """TC-180's three permutations, in one run because the second and third are
    about what the FIRST left behind."""
    root = _tree(tmp_path)
    first_event = _failure_event(root, step="tests")

    # first: one candidate, carrying the adjudicated estimate.
    relpath, findings = adjudicate.draft_remediation(
        root,
        first_event["id"],
        effort="40000",
        buildtier="strong",
        planmode="dual",
    )
    assert findings == [], findings
    assert relpath.startswith("draft/")
    text = (root / "docs" / "work" / relpath).read_text(encoding="utf-8")
    assert adjudicate.read_lineage(text)["source_event"] == first_event["id"]
    assert 'buildtier = "strong"' in text
    assert 'planmode = "dual"' in text
    assert 'est_tokens = "40000"' in text
    assert "AssertionError: boom" in text

    # repeat: the same event drafts NOTHING, and says which row already has it.
    again, findings = adjudicate.draft_remediation(root, first_event["id"])
    assert again is None
    assert any(relpath in f for f in findings), findings
    assert len(list((root / "docs" / "work" / "draft").glob("WI-*.md"))) == 1

    # different-step: a different failing step is a different id and drafts one
    # more.
    second_event = _failure_event(root, step="lint", output="E501 line too long")
    assert second_event["id"] != first_event["id"]
    other, findings = adjudicate.draft_remediation(root, second_event["id"])
    assert findings == [], findings
    assert other != relpath
    assert len(list((root / "docs" / "work" / "draft").glob("WI-*.md"))) == 2


def test_an_admitted_repair_row_still_blocks_a_second_draft(tmp_path):
    """The interesting repeat is the one AFTER the candidate has left `draft/`:
    a scan of `draft/` alone would re-draft every failure whose repair shipped."""
    root = _tree(tmp_path)
    event = _failure_event(root)
    relpath, findings = adjudicate.draft_remediation(root, event["id"])
    assert findings == []
    src = root / "docs" / "work" / relpath
    dest = root / "docs" / "work" / "complete" / src.name
    src.replace(dest)

    again, findings = adjudicate.draft_remediation(root, event["id"])
    assert again is None
    assert any("complete/" in f for f in findings), findings


def test_a_backticked_failure_excerpt_cannot_escape_its_fence(tmp_path):
    """A harness excerpt is somebody else's text: a bare three-backtick fence
    around output that itself contains one would end the block early and let a
    `##` line become a section of the frozen scope."""
    root = _tree(tmp_path)
    event = _failure_event(
        root, output="E   assert ```x``` == y\n## not a heading\nmore"
    )
    relpath, findings = adjudicate.draft_remediation(root, event["id"])
    assert findings == [], findings
    text = (root / "docs" / "work" / relpath).read_text(encoding="utf-8")
    regions = outcome.scope_regions(text)
    # ONE frozen body region: the excerpt's own `##` line stayed inside the
    # fence and did not carve a second one out of the obligation.
    assert [name for name in sorted(regions) if name.startswith("body:")] == [
        "body:Context"
    ]
    assert "```x```" in regions["body:Context"]


@pytest.mark.parametrize(
    "cells,needle",
    [
        ({"buildtier": "epic"}, "buildtier"),
        ({"planmode": "triple"}, "planmode"),
        ({"safety_class": "vibes"}, "safety_class"),
        ({"bar": "G9"}, "bar"),
    ],
)
def test_a_candidate_cell_outside_its_vocabulary_is_refused(tmp_path, cells, needle):
    """The same bar `intake._draft_refusal` applies: a row minted with nobody
    watching gets the declared vocabulary, whichever producer wrote it."""
    root = _tree(tmp_path)
    event = _failure_event(root)
    relpath, findings = adjudicate.draft_remediation(root, event["id"], **cells)
    assert relpath is None
    assert any(needle in f for f in findings), findings
    assert not list((root / "docs" / "work" / "draft").glob("WI-*.md"))


def test_an_unknown_failure_event_is_refused(tmp_path):
    root = _tree(tmp_path)
    relpath, findings = adjudicate.draft_remediation(root, "0" * 16)
    assert relpath is None
    assert any("bar-failure" in f for f in findings), findings


def test_an_outcome_event_is_not_a_bar_failure(tmp_path):
    """Naming the wrong ledger's event is a different fix from naming no event,
    and a bare None would say neither."""
    root = _tree(tmp_path)
    event = _outcome_event(root)
    # Point the failure lookup at the outcomes ledger so the id resolves to an
    # event of the wrong KIND rather than to nothing.
    relpath, findings = adjudicate.draft_remediation(
        root, event["id"], ledger=root / "docs" / "events" / "outcomes.jsonl"
    )
    assert relpath is None
    assert any("is a 'outcome' event" in f for f in findings), findings


# --- the brief (SR-156's structural half) -------------------------------------


def _config_root(tmp_path, root):
    """`root` given a docs/config.toml declaring the disposition prompt, with the
    kit's own reviewed template copied in."""
    template = SCRIPTS.parent / "prompts" / "adjudicate-disposition.md"
    dest = root / "prompts" / "adjudicate-disposition.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(template, dest)
    (root / "docs" / "config.toml").write_text(
        "schema = 1\n\n"
        '[prompts."adjudicate-disposition"]\n'
        'template = "prompts/adjudicate-disposition.md"\n'
        'required_slots = ["WI_ID"]\n'
        'allowed_sources = ["registry", "spec", "ledger", "harness", "diff"]\n'
        'prohibited_sources = ["self-assessment", "worker-rationale"]\n'
        'output_schema = "disposition-v1"\n',
        encoding="utf-8",
        newline="\n",
    )
    return root


def _brief_evidence():
    return {
        "BRANCH_COMMITS": {"source": "diff", "text": "abc1234 attempt"},
        "BRANCH_CHANGES": {"source": "diff", "text": "M\tsrc/a.py"},
        "CLASSIFICATION": {"source": "ledger", "text": "src=keep"},
        "HARNESS_RESULT": {"source": "harness", "text": "1 passed"},
        "DOWNSTREAM": {"source": "registry", "text": "(none)"},
    }


def test_the_brief_never_carries_the_workers_own_account(tmp_path):
    """SR-156, structurally: the slot set is an allowlist, so the rationale has
    no way in short of an edit to `BRIEF_SOURCED` — which is a reviewable act,
    not an oversight."""
    root = _config_root(tmp_path, _tree(tmp_path))
    event = _outcome_event(
        root, rationale="I ran out of budget and think it is basically fine"
    )
    rendered, findings = adjudicate.disposition_brief(
        root, event["id"], _brief_evidence()
    )
    assert findings == [], findings
    assert "basically fine" not in rendered.text
    assert "WI-041" in rendered.text
    assert "partial" in rendered.text
    assert "RATIONALE" not in rendered.text


def test_a_caller_may_not_restate_a_fact_of_record(tmp_path):
    root = _config_root(tmp_path, _tree(tmp_path))
    event = _outcome_event(root)
    evidence = _brief_evidence()
    evidence["DECLARED_OUTCOME"] = {"source": "ledger", "text": "complete"}
    rendered, findings = adjudicate.disposition_brief(root, event["id"], evidence)
    assert rendered is None
    assert any("DECLARED_OUTCOME" in f.key for f in findings), findings


# --- the CLI ------------------------------------------------------------------


def test_the_cli_records_a_disposition_and_exits_zero(tmp_path, capsys):
    root = _tree(tmp_path)
    event = _outcome_event(root)
    code = adjudicate.main(
        [
            "--root",
            str(root),
            "disposition",
            "--event",
            event["id"],
            "--verdict",
            "confirm",
            "--by",
            "judge",
        ]
    )
    assert code == 0
    assert "disposition" in capsys.readouterr().out
    assert len(_ledger_lines(root)) == 2


def test_the_cli_prints_every_refusal_and_exits_non_zero(tmp_path, capsys):
    root = _tree(tmp_path)
    code = adjudicate.main(
        [
            "--root",
            str(root),
            "remediation",
            "--event",
            "0" * 16,
        ]
    )
    assert code == 1
    assert "adjudicate: REFUSED" in capsys.readouterr().err
