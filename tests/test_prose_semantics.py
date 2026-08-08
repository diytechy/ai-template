"""TC-157 / TC-158 / TC-159 — ledger-vs-current detection, and enacting a verdict.

This module drives SR-143 from the two ends the *other* two evidence files do
not: `attest.detect_candidates` as the **live detector** behind `intake`, and
`attest.enact` as the thing that ANSWERS a candidate. `tests/test_attest.py`
proves the digest and the chain in isolation and `tests/test_spine_stage.py`
proves the derived stage from hand-appended events; here the same permutations
are driven through the two production paths that will carry them.

**The detection gap, stated so the tests can aim at it.**
`check_trajectory.staged_spine_amendments` compares a STAGED diff, so it sees
only what one commit touched, and it deliberately skips a row whose Status
moved. Two amendments are therefore structurally invisible to it:

  (a) a row edited while it stays `Verified` — no `Modified` flag, no candidate,
      and the loop reads a stale approval as a current one;
  (b) the sanctioned amend-and-flip-to-`Modified`, skipped ON PURPOSE.

Both are driven explicitly below, and each is paired with its converse — a
Status flip ALONE moves no digest, and a canonicalisation-only edit raises no
candidate — because a detector that fires on everything is not better than one
that fires on nothing.

**The enactment's three properties, one per verdict.** `clarity` must advance
the anchor to the NEW digest (re-accepting the old one leaves the anchor
silently lagging the text — the subtle half); `meaning` must pull the derived
spine stage back to that artifact's tier; `override` must append while history
stays byte-identical. Each is asserted as the property, not as "an event was
written".

No git and no subprocess: every seam here is a file read, so the head-to-head
against the staged-diff detector (which needs real commits) is deliberately NOT
in this module — see the slice's reported gap.
"""

import json

import pytest
from conftest import load_script

ATTEST = load_script("attest")
GATE = load_script("derive_gate")
INTAKE = load_script("intake")

SN_MD = """# Stakeholder Needs

## Core needs

| SN-ID | Need (plain language) | Why it matters | Priority | Acceptance intent |
|---|---|---|---|---|
| SN-000 | _(example row, ignored)_ | _(why)_ | M | _(how we'd know)_ |
| SN-001 | A team can add two numbers. | It is the demo need. | M | add(1,2) gives 3. |
"""

SRS_H = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,"
    "Priority,Verification,Status,Phase,Area,SupersededBy\n"
)
SRS = (
    'SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.",'
    '"add(1,2) == 3",,M,Test,Verified,1,core,\n'
)
LLRS_H = (
    "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,Rationale,TestRefs,Status,"
    "Component,Phase\n"
)
LLRS = (
    'LLR-001,SR-001,Pure adder,src/demo,add,"Pure function: two numbers -> sum.",'
    '"Purity is testable.",(see TC),Implemented,CMP-001,1\n'
)
TCS_H = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,"
    "Status,Phase\n"
)
TCS = (
    'TC-001,SR-001;LLR-001,Unit,"call add and assert the sum",Smoke,"a=1; b=2",'
    '"Satisfies SR-001 AcceptanceCriteria",Yes,tests/test_demo.py,Verified,1\n'
)

# Which row of each tier the fixtures amend, and the file that tier lives in.
TIER_ROW = {"SN": "SN-001", "SR": "SR-001", "LLR": "LLR-001", "TC": "TC-001"}
TIER_FILE = {
    "SN": "docs/requirements/stakeholder-needs.md",
    "SR": "docs/requirements/system-requirements.csv",
    "LLR": "docs/requirements/low-level-requirements.csv",
    "TC": "docs/test/test-cases.csv",
}
TIERS = ("SN", "SR", "LLR", "TC")


def make_docs(root, sn=SN_MD, srs=SRS, llrs=LLRS, tcs=TCS, newline="\n"):
    """A complete four-tier spine under `root/docs`. `newline` exists for the
    CRLF permutation — a Windows checkout must digest like a POSIX one."""
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (root / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (req / "stakeholder-needs.md").write_text(sn, encoding="utf-8", newline=newline)
    (req / "system-requirements.csv").write_text(
        SRS_H + srs, encoding="utf-8", newline=newline
    )
    (req / "low-level-requirements.csv").write_text(
        LLRS_H + llrs, encoding="utf-8", newline=newline
    )
    (root / "docs" / "test" / "test-cases.csv").write_text(
        TCS_H + tcs, encoding="utf-8", newline=newline
    )
    return root / "docs"


def seeded(root):
    """A spine whose every row already has a baseline anchor — the state a repo
    is in the moment after the one-time migration, and the only state in which
    "the text moved" is a question with an answer."""
    docs = make_docs(root)
    ATTEST.seed(root, docs, by="test")
    assert ATTEST.detect_candidates(root, docs) == []
    return docs


# A REWORDED-NORMATIVE edit per tier: one cell whose change alters obligation.
REWORDED = {
    "SN": {"sn": SN_MD.replace("add two numbers.", "add three numbers.")},
    "SR": {
        "srs": SRS.replace("shall add two numbers", "shall add exactly two numbers")
    },
    "LLR": {"llrs": LLRS.replace("two numbers -> sum", "three numbers -> sum")},
    "TC": {"tcs": TCS.replace("a=1; b=2", "a=1; b=2; c=3")},
}

# A REWORDED-NON-NORMATIVE edit per tier: evidence pointers, phase labels, areas
# and the Status word itself may all move without invalidating an anchor. SN is
# absent by construction, not by omission — all four cells of the core needs
# table are normative, so that tier has no non-normative cell to move.
NON_NORMATIVE = {
    "SR": {"srs": SRS.replace(",Verified,1,core,", ",Modified,2,platform,")},
    "LLR": {"llrs": LLRS.replace(",Implemented,CMP-001,1", ",Planned,CMP-002,2")},
    "TC": {
        "tcs": TCS.replace(",tests/test_demo.py,Verified,1", ",tests/other.py,Draft,2")
    },
}


def head_of(root, kind, rid):
    chain = ATTEST.chain_map(
        ATTEST.read_events(ATTEST.ledger_path(root, "attestation"))
    ).get((kind, rid), [])
    return chain[-1]["id"] if chain else None


def ledger_lines(root):
    path = ATTEST.ledger_path(root, "attestation")
    return path.read_text(encoding="utf-8").splitlines() if path.exists() else []


def set_boundary(root, boundary):
    """Write the one dial this slice reads. A partial config is valid: every
    other key keeps its declared default."""
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "config.toml").write_text(
        "schema = 1\n\n[attestation]\nhuman_ratification_through = {}\n".format(
            boundary
        ),
        encoding="utf-8",
        newline="\n",
    )


# --- TC-157 (detection): identical | re-wrapped | reworded-normative |
# --- reworded-non-normative, each read through the LIVE detector --------------
def test_an_untouched_spine_raises_no_candidate_and_no_amendment(tmp_path):
    docs = seeded(tmp_path)
    make_docs(tmp_path)  # identical bytes rewritten: same text, same digests
    assert ATTEST.detect_candidates(tmp_path, docs) == []
    assert INTAKE.ledger_amendments(tmp_path, docs) == []
    assert INTAKE.ledger_amendment_drafts(tmp_path, docs) == []


REWRAPPED = {
    "collapsed-spaces": {
        "srs": SRS.replace("shall add two numbers", "shall  add   two    numbers")
    },
    "trailing-space": {"srs": SRS.replace("add two numbers.", "add two numbers.  ")},
    "crlf-checkout": {"newline": "\r\n"},
}


@pytest.mark.parametrize("case", sorted(REWRAPPED))
def test_a_canonicalisation_only_edit_produces_no_candidate(tmp_path, case):
    # The declared canonicalisation (contracts §4): a re-wrap costs nobody a
    # re-attestation. If this ever fires, every editor that trims whitespace on
    # save becomes a source of adjudication work.
    docs = seeded(tmp_path)
    make_docs(tmp_path, **REWRAPPED[case])
    assert ATTEST.detect_candidates(tmp_path, docs) == []
    assert INTAKE.ledger_amendments(tmp_path, docs) == []


@pytest.mark.parametrize("kind", TIERS)
def test_a_reworded_normative_cell_at_every_tier_is_detected(tmp_path, kind):
    docs = seeded(tmp_path)
    make_docs(tmp_path, **REWORDED[kind])
    candidates = ATTEST.detect_candidates(tmp_path, docs)
    assert [(c["kind"], c["id"], c["state"]) for c in candidates] == [
        (kind, TIER_ROW[kind], ATTEST.CHANGED)
    ]
    records = INTAKE.ledger_amendments(tmp_path, docs)
    assert [r["id"] for r in records] == [TIER_ROW[kind]]
    # The anchor is carried on the record, and it is the OLD digest: that pair
    # is the whole evidence an adjudicator reads.
    assert records[0]["anchor"] != records[0]["digest"]


@pytest.mark.parametrize("kind", sorted(NON_NORMATIVE))
def test_a_reworded_non_normative_cell_produces_no_candidate(tmp_path, kind):
    docs = seeded(tmp_path)
    make_docs(tmp_path, **NON_NORMATIVE[kind])
    assert ATTEST.detect_candidates(tmp_path, docs) == []
    assert INTAKE.ledger_amendments(tmp_path, docs) == []


# --- the two blind cases: the reason this slice exists ------------------------
def test_a_row_amended_while_it_stays_verified_is_detected(tmp_path):
    # Blind case (a). The row never flips to `Modified`, so nothing in the Status
    # column says anything happened; a diff-shaped check on a LATER commit sees
    # no change at all, and the loop reads the standing approval as current.
    docs = seeded(tmp_path)
    amended = SRS.replace("shall add two numbers", "shall add any two integers")
    assert ",Verified," in amended  # the flag that would have raised the alarm
    make_docs(tmp_path, srs=amended)
    records = INTAKE.ledger_amendments(tmp_path, docs)
    assert [r["id"] for r in records] == ["SR-001"]
    assert "normative text changed" in records[0]["reason"]


def test_the_sanctioned_amend_and_flip_to_modified_is_detected(tmp_path):
    # Blind case (b): the staged detector skips a row whose Status moved, ON
    # PURPOSE — someone made a deliberate call. That call is a request for
    # adjudication, not a reason to stop looking.
    docs = seeded(tmp_path)
    amended = SRS.replace("shall add two numbers", "shall add any two integers")
    make_docs(tmp_path, srs=amended.replace(",Verified,", ",Modified,"))
    records = INTAKE.ledger_amendments(tmp_path, docs)
    assert [r["id"] for r in records] == ["SR-001"]


def test_a_status_flip_alone_moves_no_digest(tmp_path):
    # The converse of blind case (b), and the reason it is catchable: Status is
    # not a normative cell, so the flip carries no information the digest reads.
    # A detector that fired on the flip would fire on every bookkeeping commit.
    docs = seeded(tmp_path)
    make_docs(tmp_path, srs=SRS.replace(",Verified,", ",Modified,"))
    assert ATTEST.detect_candidates(tmp_path, docs) == []


def test_an_unattested_row_is_a_candidate_but_never_an_amendment(tmp_path):
    # Nothing was approved, so nothing was amended. Minting adjudication here
    # would ask someone to judge a change that never happened.
    docs = make_docs(tmp_path)
    states = {c["state"] for c in ATTEST.detect_candidates(tmp_path, docs)}
    assert states == {ATTEST.UNATTESTED}
    assert INTAKE.ledger_amendments(tmp_path, docs) == []


def test_a_row_with_a_standing_meaning_verdict_is_not_minted_again(tmp_path):
    # A verdict already stands at this very text; a second row would leave two
    # owed for one answer.
    docs = seeded(tmp_path)
    make_docs(tmp_path, **REWORDED["SR"])
    ATTEST.enact(tmp_path, docs, "SR-001", "meaning", by="owner")
    assert [c["state"] for c in ATTEST.detect_candidates(tmp_path, docs)] == [
        ATTEST.PENDING
    ]
    assert INTAKE.ledger_amendments(tmp_path, docs) == []


# --- the minted row arm (a2) --------------------------------------------------
def test_the_draft_names_the_rows_the_tier_file_and_the_three_verdicts(tmp_path):
    docs = seeded(tmp_path)
    make_docs(tmp_path, **REWORDED["LLR"])
    draft = INTAKE.ledger_amendment_drafts(tmp_path, docs)[0]
    assert draft["kind"] == "adjudication"
    assert "LLR-001" in draft["title"]
    assert draft["specref"] == TIER_FILE["LLR"]
    for word in ("clarity", "meaning", "override"):
        assert word in draft["context"]
    assert "attest.py" in draft["context"]


def test_the_draft_specref_and_sr_refs_follow_the_lowest_tier(tmp_path):
    docs = seeded(tmp_path)
    make_docs(tmp_path, **dict(REWORDED["SR"], **REWORDED["TC"]))
    draft = INTAKE.ledger_amendment_drafts(tmp_path, docs)[0]
    assert draft["specref"] == TIER_FILE["SR"]  # SR is walked before TC
    assert draft["sr_refs"] == ["SR-001"]  # only real SR ids ride the ref cell
    assert "SR-001" in draft["title"] and "TC-001" in draft["title"]


def test_the_derived_title_is_stable_across_runs_and_moves_with_one_more_edit(tmp_path):
    # Idempotence by exact-title dedup is the mint's whole recovery story, and a
    # FURTHER edit has to be a new event rather than a silent dedupe that leaves
    # nobody owed the judgement.
    docs = seeded(tmp_path)
    make_docs(tmp_path, **REWORDED["SR"])
    first = INTAKE.ledger_amendment_drafts(tmp_path, docs)[0]["title"]
    assert INTAKE.ledger_amendment_drafts(tmp_path, docs)[0]["title"] == first
    make_docs(tmp_path, srs=SRS.replace("shall add two numbers", "shall add two ints"))
    assert INTAKE.ledger_amendment_drafts(tmp_path, docs)[0]["title"] != first


def test_the_intake_candidates_cli_reports_every_row_and_exits_one(tmp_path, capsys):
    # No --docs: the default is <root>/docs, which is the shape a hook or an
    # integrator actually types.
    seeded(tmp_path)
    assert INTAKE.main(["--root", str(tmp_path), "candidates"]) == 0
    assert "nothing to adjudicate" in capsys.readouterr().out
    make_docs(tmp_path, **dict(REWORDED["SN"], **REWORDED["TC"]))
    assert INTAKE.main(["--root", str(tmp_path), "candidates"]) == 1
    out = capsys.readouterr().out
    assert "SN-001" in out and "TC-001" in out
    assert "anchor" in out and "clarity" in out


def test_the_intake_cli_prints_the_ledger_refusal_rather_than_a_traceback(
    tmp_path, capsys
):
    # A ledger that cannot be read must not degrade to "nothing to adjudicate":
    # that would be the dishonest green in a new place.
    seeded(tmp_path)
    with ATTEST.ledger_path(tmp_path, "attestation").open(
        "a", encoding="utf-8", newline="\n"
    ) as fh:
        fh.write("{oops\n")
    assert INTAKE.main(["--root", str(tmp_path), "candidates"]) == 1
    assert "attestation.jsonl:5" in capsys.readouterr().err


# --- TC-159 (through the enactment): need | requirement | low-level |
# --- test-case | clarity ------------------------------------------------------
STAGE_OF = {"SN": 0, "SR": 1, "LLR": 2, "TC": 3}


@pytest.mark.parametrize("kind", TIERS)
def test_a_meaning_verdict_pulls_the_stage_back_to_its_own_tier(tmp_path, kind):
    docs = seeded(tmp_path)
    assert GATE.spine_stage(docs) == 4
    make_docs(tmp_path, **REWORDED[kind])
    rid = TIER_ROW[kind]
    anchor_before = ATTEST.accepted_anchor(tmp_path, kind, rid)["digest"]

    action, event, digest = ATTEST.enact(tmp_path, docs, rid, "meaning", by="owner")
    assert action == ATTEST.ENACT
    assert event["decision"] == "meaning" and event["digest"] == digest
    assert GATE.spine_stage(docs) == STAGE_OF[kind]
    # A meaning verdict decides that the obligation CHANGED, so it must not
    # accept: the anchor stays where it was and the row stays owed.
    assert ATTEST.accepted_anchor(tmp_path, kind, rid)["digest"] == anchor_before
    assert [c["state"] for c in ATTEST.detect_candidates(tmp_path, docs)] == [
        ATTEST.PENDING
    ]


@pytest.mark.parametrize("kind", TIERS)
def test_a_clarity_verdict_advances_the_anchor_to_the_new_digest(tmp_path, kind):
    # The subtle half: a clarity verdict must re-accept the text that is THERE.
    # Re-accepting the old digest would leave every surface reading "accepted"
    # while the anchor lagged the prose.
    docs = seeded(tmp_path)
    make_docs(tmp_path, **REWORDED[kind])
    rid = TIER_ROW[kind]
    stale = ATTEST.accepted_anchor(tmp_path, kind, rid)["digest"]
    assert GATE.spine_stage(docs) == STAGE_OF[kind]

    action, event, digest = ATTEST.enact(tmp_path, docs, rid, "clarity", by="owner")
    assert action == ATTEST.ENACT
    assert digest != stale
    assert ATTEST.accepted_anchor(tmp_path, kind, rid)["digest"] == digest
    assert event["digest"] == digest
    assert ATTEST.detect_candidates(tmp_path, docs) == []
    assert INTAKE.ledger_amendments(tmp_path, docs) == []
    assert GATE.spine_stage(docs) == 4  # the stage returns; nobody re-litigated


def test_a_clarity_verdict_does_not_lower_the_stage_at_all(tmp_path):
    # Stated as its own property because it is the one thing that separates the
    # two verdicts: same row, same digest, opposite effect on the derived stage.
    docs = seeded(tmp_path)
    make_docs(tmp_path, **REWORDED["SN"])
    ATTEST.enact(tmp_path, docs, "SN-001", "clarity", by="owner")
    assert GATE.spine_stage(docs) == 4
    assert GATE.verification_gate_for(GATE.spine_stage(docs)) == "G3"


# --- TC-158 (through the enactment): first | successor | stale-parent |
# --- override -----------------------------------------------------------------
def test_the_first_verdict_on_a_chain_names_no_parent_and_becomes_the_head(tmp_path):
    docs = make_docs(tmp_path)  # deliberately NOT seeded: no history at all
    action, event, _digest = ATTEST.enact(
        tmp_path, docs, "SR-001", "meaning", by="owner"
    )
    assert action == ATTEST.ENACT
    assert event["parent"] is None
    assert head_of(tmp_path, "SR", "SR-001") == event["id"]


def test_a_successor_verdict_chains_on_the_head_the_previous_one_left(tmp_path):
    docs = seeded(tmp_path)
    make_docs(tmp_path, **REWORDED["SR"])
    first = ATTEST.enact(tmp_path, docs, "SR-001", "meaning", by="owner")[1]
    second = ATTEST.enact(
        tmp_path, docs, "SR-001", "override", by="owner", accepted=True
    )[1]
    assert second["parent"] == first["id"]
    assert head_of(tmp_path, "SR", "SR-001") == second["id"]
    assert ATTEST.accepted_anchor(tmp_path, "SR", "SR-001")["id"] == second["id"]


def test_a_write_naming_a_stale_parent_is_refused_and_the_ledger_is_untouched(tmp_path):
    # The enactment always reads the head immediately before it appends, so the
    # stale-parent case is a SECOND writer: it read the head, the head moved,
    # and its write must not be flattened into a sequence that never happened.
    docs = seeded(tmp_path)
    make_docs(tmp_path, **REWORDED["SR"])
    stale_head = head_of(tmp_path, "SR", "SR-001")
    ATTEST.enact(tmp_path, docs, "SR-001", "meaning", by="owner")
    before = ledger_lines(tmp_path)

    row = next(
        r
        for r in ATTEST.load_artifacts(docs)["SR"]
        if ATTEST.row_id("SR", r) == "SR-001"
    )
    with pytest.raises(ValueError) as exc:
        ATTEST.append_event(
            tmp_path,
            ATTEST.attestation_event(
                "SR",
                "SR-001",
                ATTEST.normative_digest("SR", row),
                "clarity",
                stale_head,
                "other",
            ),
        )
    assert "REFUSED" in str(exc.value) and "SR-001" in str(exc.value)
    assert ledger_lines(tmp_path) == before


def test_an_override_appends_and_leaves_every_earlier_line_byte_identical(tmp_path):
    docs = seeded(tmp_path)
    make_docs(tmp_path, **REWORDED["TC"])
    ATTEST.enact(tmp_path, docs, "TC-001", "clarity", by="owner")
    before = ledger_lines(tmp_path)

    _action, event, _digest = ATTEST.enact(
        tmp_path,
        docs,
        "TC-001",
        "override",
        by="owner",
        accepted=False,
        note="re-read it; the obligation did move",
    )
    after = ledger_lines(tmp_path)
    assert after[: len(before)] == before  # history is never edited
    assert len(after) == len(before) + 1
    assert json.loads(after[-1])["id"] == event["id"]
    assert event["accepted"] is False and event["note"]
    # A refusing override does not accept, so the row is owed again — and the
    # derived stage says so without anyone editing a Status cell.
    assert [c["state"] for c in ATTEST.detect_candidates(tmp_path, docs)] == [
        ATTEST.PENDING
    ]
    assert GATE.spine_stage(docs) == STAGE_OF["TC"]


def test_a_stale_anchor_is_named_in_the_candidate_and_then_advanced(tmp_path):
    # The anchor lags the text by TWO edits: a meaning verdict stands at the
    # first wording, and the prose has moved again since. What a checkpoint
    # needs is "the standing approval is for neither of those".
    docs = seeded(tmp_path)
    baseline = ATTEST.accepted_anchor(tmp_path, "SR", "SR-001")["digest"]
    make_docs(tmp_path, **REWORDED["SR"])
    ATTEST.enact(tmp_path, docs, "SR-001", "meaning", by="owner")
    make_docs(tmp_path, srs=SRS.replace("shall add two numbers", "shall add a pair"))

    candidate = ATTEST.detect_candidates(tmp_path, docs)[0]
    assert candidate["state"] == ATTEST.CHANGED
    assert candidate["anchor"] == baseline  # still the migration's baseline
    assert baseline[:12] in candidate["reason"]
    assert candidate["digest"][:12] in candidate["reason"]

    ATTEST.enact(tmp_path, docs, "SR-001", "clarity", by="owner")
    assert (
        ATTEST.accepted_anchor(tmp_path, "SR", "SR-001")["digest"]
        == (candidate["digest"])
    )
    assert ATTEST.detect_candidates(tmp_path, docs) == []


# --- the ratification boundary: recommend below it, enact above it ------------
@pytest.mark.parametrize("boundary", [0, 1, 2, 3])
@pytest.mark.parametrize("kind", TIERS)
def test_the_action_matrix_is_the_boundary_matrix(boundary, kind):
    index = ATTEST.TIER_INDEX[kind]
    expected = ATTEST.RECOMMEND if index <= boundary else ATTEST.ENACT
    assert ATTEST.verdict_action(kind, boundary, ATTEST.ADJUDICATOR) == expected
    # A human may always decide: the dial says which tiers REQUIRE a human, not
    # which tiers forbid one.
    assert ATTEST.verdict_action(kind, boundary, ATTEST.HUMAN) == ATTEST.ENACT
    assert ATTEST.requires_human(index, boundary) is (expected == ATTEST.RECOMMEND)


def test_an_adjudicator_at_or_below_the_boundary_writes_nothing(tmp_path):
    docs = seeded(tmp_path)
    set_boundary(tmp_path, 1)  # SN + SR are the human's
    make_docs(tmp_path, **REWORDED["SR"])
    before = ledger_lines(tmp_path)

    action, event, digest = ATTEST.enact(
        tmp_path, docs, "SR-001", "clarity", by="ROUTE", actor=ATTEST.ADJUDICATOR
    )
    assert action == ATTEST.RECOMMEND
    assert event is None and digest
    assert ledger_lines(tmp_path) == before
    # Nothing was claimed, so the row is still owed on every surface.
    assert INTAKE.ledger_amendments(tmp_path, docs)[0]["id"] == "SR-001"
    assert GATE.spine_stage(docs) == 1


def test_an_adjudicator_above_the_boundary_may_enact(tmp_path):
    docs = seeded(tmp_path)
    set_boundary(tmp_path, 1)  # TC (index 3) is above it
    make_docs(tmp_path, **REWORDED["TC"])
    action, event, digest = ATTEST.enact(
        tmp_path, docs, "TC-001", "clarity", by="ROUTE", actor=ATTEST.ADJUDICATOR
    )
    assert action == ATTEST.ENACT
    assert event["by"] == "ROUTE"
    assert ATTEST.accepted_anchor(tmp_path, "TC", "TC-001")["digest"] == digest
    assert ATTEST.detect_candidates(tmp_path, docs) == []


def test_a_boundary_of_three_reserves_every_tier_for_a_human(tmp_path):
    docs = seeded(tmp_path)
    set_boundary(tmp_path, 3)
    for kind in TIERS:
        make_docs(tmp_path, **REWORDED[kind])
        assert (
            ATTEST.enact(
                tmp_path,
                docs,
                TIER_ROW[kind],
                "clarity",
                by="ROUTE",
                actor=ATTEST.ADJUDICATOR,
            )[0]
            == ATTEST.RECOMMEND
        )
        make_docs(tmp_path)  # put the tier back before moving to the next
    # Nothing was written at any tier: the four seeded baselines, and no more.
    assert len(ledger_lines(tmp_path)) == 4


def test_a_later_human_override_reverses_an_adjudicators_enactment(tmp_path):
    # The append-only answer to "who can undo an adjudicator?". No event is
    # edited, no dial is changed, and the derived state simply re-reads.
    docs = seeded(tmp_path)
    set_boundary(tmp_path, 0)  # only SN is the human's; TC is the adjudicator's
    make_docs(tmp_path, **REWORDED["TC"])
    enacted = ATTEST.enact(
        tmp_path, docs, "TC-001", "clarity", by="ROUTE", actor=ATTEST.ADJUDICATOR
    )[1]
    assert GATE.spine_stage(docs) == 4
    before = ledger_lines(tmp_path)

    reversed_ = ATTEST.enact(
        tmp_path,
        docs,
        "TC-001",
        "override",
        by="owner",
        accepted=False,
        note="the parameters changed what the case proves",
    )[1]
    assert reversed_["parent"] == enacted["id"]
    assert ledger_lines(tmp_path)[: len(before)] == before
    assert GATE.spine_stage(docs) == STAGE_OF["TC"]
    assert ATTEST.detect_candidates(tmp_path, docs)[0]["state"] == ATTEST.PENDING


# --- refusals, driven as hard as the happy path -------------------------------
def test_a_verdict_this_arm_does_not_enact_is_refused_by_name(tmp_path):
    docs = seeded(tmp_path)
    for word in ("ratified", ATTEST.BASELINE, "approve", ""):
        with pytest.raises(ValueError) as exc:
            ATTEST.enact(tmp_path, docs, "SR-001", word, by="owner")
        assert "REFUSED" in str(exc.value)
        assert " | ".join(ATTEST.ENACTABLE) in str(exc.value)
    assert len(ledger_lines(tmp_path)) == 4  # the seeded baselines, untouched


def test_an_override_that_says_neither_accept_nor_reject_is_refused(tmp_path):
    docs = seeded(tmp_path)
    with pytest.raises(ValueError) as exc:
        ATTEST.enact(tmp_path, docs, "SR-001", "override", by="owner")
    assert "REFUSED" in str(exc.value) and "SR-001" in str(exc.value)
    assert "--accept" in str(exc.value)


def test_both_accept_and_reject_at_once_is_refused_rather_than_ranked(tmp_path):
    with pytest.raises(ValueError) as exc:
        ATTEST._accepted_flag(True, True)
    assert "REFUSED" in str(exc.value)
    assert ATTEST._accepted_flag(True, False) is True
    assert ATTEST._accepted_flag(False, True) is False
    assert ATTEST._accepted_flag(False, False) is None


def test_a_clarity_verdict_on_a_row_with_no_history_is_refused(tmp_path):
    # There is no anchor for it to advance, so the event would claim a
    # re-acceptance nobody ever made.
    docs = make_docs(tmp_path)
    with pytest.raises(ValueError) as exc:
        ATTEST.enact(tmp_path, docs, "LLR-001", "clarity", by="owner")
    assert "REFUSED" in str(exc.value) and "LLR-001" in str(exc.value)
    assert "no attestation event" in str(exc.value)
    assert ledger_lines(tmp_path) == []


def test_a_clarity_verdict_on_already_accepted_text_is_refused(tmp_path):
    # It would record a decision-shaped event that decided nothing, and the next
    # counter reads decision words.
    docs = seeded(tmp_path)
    with pytest.raises(ValueError) as exc:
        ATTEST.enact(tmp_path, docs, "SR-001", "clarity", by="owner")
    assert "already accepted at its current text" in str(exc.value)
    assert len(ledger_lines(tmp_path)) == 4


def test_a_verdict_about_a_row_no_registry_carries_is_refused(tmp_path):
    docs = seeded(tmp_path)
    with pytest.raises(ValueError) as exc:
        ATTEST.enact(tmp_path, docs, "SR-999", "meaning", by="owner")
    assert "REFUSED" in str(exc.value) and "SR-999" in str(exc.value)


@pytest.mark.parametrize("rid", ["WI-001", "SR001", "", "NEED-001", None])
def test_an_id_with_no_spine_tier_prefix_is_refused(rid):
    with pytest.raises(ValueError) as exc:
        ATTEST.kind_of(rid)
    assert "REFUSED" in str(exc.value) and repr(rid) in str(exc.value)


def test_every_declared_tier_prefix_resolves_case_insensitively(tmp_path):
    for kind in TIERS:
        assert ATTEST.kind_of(TIER_ROW[kind]) == kind
        assert ATTEST.kind_of(TIER_ROW[kind].lower()) == kind
    # Only the PREFIX is this call's business; whether the rest names a real row
    # is `find_row`'s, and it refuses there rather than guessing a near-match.
    assert ATTEST.kind_of("sn-001x") == "SN"
    with pytest.raises(ValueError) as exc:
        ATTEST.find_row(make_docs(tmp_path), "sn-001x")
    assert "REFUSED" in str(exc.value) and "sn-001x" in str(exc.value)


def test_an_unattributed_verdict_is_refused(tmp_path):
    docs = seeded(tmp_path)
    for by in (None, "", "   "):
        with pytest.raises(ValueError) as exc:
            ATTEST.enact(tmp_path, docs, "SR-001", "meaning", by=by)
        assert "REFUSED" in str(exc.value) and "SR-001" in str(exc.value)


def test_an_unknown_actor_and_an_unknown_tier_are_refused_by_name():
    with pytest.raises(ValueError) as exc:
        ATTEST.verdict_action("SR", 1, "robot")
    assert "REFUSED" in str(exc.value) and "robot" in str(exc.value)
    with pytest.raises(ValueError) as exc:
        ATTEST.verdict_action("WI", 1, ATTEST.HUMAN)
    assert "REFUSED" in str(exc.value) and "'WI'" in str(exc.value)


@pytest.mark.parametrize("boundary", [-1, 4, True, "1", None])
def test_an_out_of_range_boundary_refuses_rather_than_routing_a_tier(boundary):
    with pytest.raises(ValueError) as exc:
        ATTEST.verdict_action("TC", boundary, ATTEST.ADJUDICATOR)
    assert "REFUSED" in str(exc.value)


def test_an_unreadable_dial_never_authorises_a_machine(tmp_path):
    # `attestation_config` falls back to the declared default when a dial cannot
    # be read — right for a reader, wrong for a writer. The misspelling is the
    # realistic shape: the adopter meant to reserve every tier and the file says
    # nothing this loader recognises.
    docs = seeded(tmp_path)
    (tmp_path / "docs" / "config.toml").write_text(
        "schema = 1\n\n[attestation]\nhuman_ratification_throuh = 3\n",
        encoding="utf-8",
        newline="\n",
    )
    make_docs(tmp_path, **REWORDED["TC"])
    with pytest.raises(ValueError) as exc:
        ATTEST.enact(
            tmp_path, docs, "TC-001", "clarity", by="ROUTE", actor=ATTEST.ADJUDICATOR
        )
    assert "REFUSED" in str(exc.value)
    assert "human_ratification_throuh" in str(exc.value)
    assert len(ledger_lines(tmp_path)) == 4
    # A human consulted no dial, so an unreadable one does not stop them.
    assert (
        ATTEST.enact(tmp_path, docs, "TC-001", "clarity", by="owner")[0] == ATTEST.ENACT
    )


def test_a_malformed_verdict_is_refused_even_when_the_actor_may_only_recommend(
    tmp_path,
):
    # Order matters: "we would have refused this" is what an adjudicator's
    # author needs to hear, not "a human will decide".
    docs = seeded(tmp_path)
    set_boundary(tmp_path, 3)
    with pytest.raises(ValueError) as exc:
        ATTEST.enact(
            tmp_path, docs, "SR-001", "approve", by="ROUTE", actor=ATTEST.ADJUDICATOR
        )
    assert "is not a verdict this arm enacts" in str(exc.value)


# --- the CLI arms -------------------------------------------------------------
def test_the_cli_prints_the_property_each_verdict_changed(tmp_path, capsys):
    docs = seeded(tmp_path)
    make_docs(tmp_path, **REWORDED["SR"])
    argv = ["--root", str(tmp_path), "--docs", str(docs), "--by", "owner"]

    assert ATTEST.main(argv + ["--meaning", "SR-001"]) == 0
    out = capsys.readouterr().out
    assert "meaning recorded for SR-001" in out and "pulls back to 1 (SR)" in out
    # A ledger write stales the generated artifacts, and the tool that broke the
    # tree is the one that has to say so.
    assert "docs/gate" in out

    assert ATTEST.main(argv + ["--clarity", "SR-001"]) == 0
    assert "the accepted anchor advances to" in capsys.readouterr().out

    make_docs(tmp_path, **REWORDED["TC"])
    assert ATTEST.main(argv + ["--override", "TC-001", "--reject"]) == 0
    assert "it REFUSES the current text" in capsys.readouterr().out
    assert ATTEST.main(argv + ["--override", "TC-001", "--accept"]) == 0
    assert "it ACCEPTS the current text" in capsys.readouterr().out


def test_the_cli_enacts_before_it_reports(tmp_path, capsys):
    # One run that decides and then lists must list the state its own write
    # produced — otherwise the report is a photograph of the past.
    docs = seeded(tmp_path)
    make_docs(tmp_path, **REWORDED["SR"])
    code = ATTEST.main(
        [
            "--root",
            str(tmp_path),
            "--docs",
            str(docs),
            "--by",
            "owner",
            "--clarity",
            "SR-001",
            "--candidates",
        ]
    )
    assert code == 0
    assert "every spine row matches its accepted anchor" in capsys.readouterr().out


def test_the_cli_recommendation_writes_nothing_and_still_exits_zero(tmp_path, capsys):
    # The adjudicator answered correctly for its authority and claimed nothing,
    # so this is not a failure — the row stays visibly owed.
    docs = seeded(tmp_path)
    set_boundary(tmp_path, 3)
    make_docs(tmp_path, **REWORDED["SN"])
    before = ledger_lines(tmp_path)
    code = ATTEST.main(
        [
            "--root",
            str(tmp_path),
            "--docs",
            str(docs),
            "--by",
            "ROUTE",
            "--actor",
            "adjudicator",
            "--meaning",
            "SN-001",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "RECOMMEND" in out and "SN-001" in out
    assert ATTEST.BOUNDARY_KEY in out
    assert ledger_lines(tmp_path) == before


def test_the_cli_refusal_names_the_offending_thing_and_exits_one(tmp_path, capsys):
    docs = seeded(tmp_path)
    code = ATTEST.main(
        ["--root", str(tmp_path), "--docs", str(docs), "--clarity", "SR-001"]
    )
    assert code == 1
    assert "REFUSED" in capsys.readouterr().err

    code = ATTEST.main(
        [
            "--root",
            str(tmp_path),
            "--docs",
            str(docs),
            "--by",
            "owner",
            "--override",
            "SR-001",
        ]
    )
    assert code == 1
    err = capsys.readouterr().err
    assert "REFUSED" in err and "SR-001" in err


def test_every_enactable_verdict_has_a_cli_arm(tmp_path, capsys):
    # The loop reads the option dest off the verdict word, so a verdict added to
    # the vocabulary without an option would be silently unreachable.
    docs = seeded(tmp_path)
    for verdict in ATTEST.ENACTABLE:
        assert (
            ATTEST.main(
                ["--root", str(tmp_path), "--docs", str(docs), "--" + verdict, "X-1"]
            )
            == 1
        )
        assert "REFUSED" in capsys.readouterr().err
