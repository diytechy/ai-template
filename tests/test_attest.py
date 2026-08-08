"""TC-156 / TC-157 / TC-158 / TC-161 — the attestation ledger and its refusals.

The value of this module is entirely in what it REFUSES, so the refusals are
driven as hard as the happy path: a stale parent, a duplicate id, a hand-edited
line, a decision naming a request that is not open, a boundary outside 0..3.
Each is asserted to name the offending thing, because a bare `False` at any of
these seams is indistinguishable from "nothing was wrong".

The two candidate cases that motivated the digest get their own tests: a row
edited while it stays `Verified`, and the sanctioned amend-and-flip to
`Modified` that `check_trajectory.staged_spine_amendments` deliberately skips.
Both are invisible to the diff-shaped check and must be caught here.
"""

import json
import re

import pytest
from conftest import load_script

ATTEST = load_script("attest")

# Spelled out rather than written as escapes: a line-ending fixture whose CR was
# silently normalised by an editor would make the CRLF test vacuous, and the
# vacuity would be invisible in the source.
CR, LF = chr(13), chr(10)

SN_MD = """# Stakeholder Needs

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


def make_docs(root):
    """A minimal but complete four-tier spine under `root/docs`."""
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (root / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (req / "stakeholder-needs.md").write_text(SN_MD, encoding="utf-8", newline="\n")
    (req / "system-requirements.csv").write_text(
        SRS_H + SRS, encoding="utf-8", newline="\n"
    )
    (req / "low-level-requirements.csv").write_text(
        LLRS_H + LLRS, encoding="utf-8", newline="\n"
    )
    (root / "docs" / "test" / "test-cases.csv").write_text(
        TCS_H + TCS, encoding="utf-8", newline="\n"
    )
    return root / "docs"


def head_id(root, ledger_kind, artifact_kind, artifact_id):
    events = ATTEST.read_events(ATTEST.ledger_path(root, ledger_kind))
    chain = [e for e in events if ATTEST.chain_key(e) == (artifact_kind, artifact_id)]
    return chain[-1]["id"] if chain else None


def ledger_lines(root, ledger_kind):
    path = ATTEST.ledger_path(root, ledger_kind)
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8").splitlines()


# --- TC-156: the boundary-to-tier routing table (SR-142 / LLR-162) ------------
# boundary 0 | 1 | 2 | 3 | out-of-range
BOUNDARY_TABLE = {
    0: (True, False, False, False),  # SN only
    1: (True, True, False, False),  # SN + SR
    2: (True, True, True, False),  # SN + SR + LLR
    3: (True, True, True, True),  # the whole spine
}


@pytest.mark.parametrize("boundary", sorted(BOUNDARY_TABLE))
def test_every_boundary_routes_the_four_tiers_as_the_inclusive_table_declares(boundary):
    # The dial is CUMULATIVE and INCLUSIVE (decisions §1): at or below the
    # boundary a human decides, above it an adjudicator may enact.
    for tier, wants_human in enumerate(BOUNDARY_TABLE[boundary]):
        assert ATTEST.requires_human(tier, boundary) is wants_human, (tier, boundary)


def test_the_tier_indices_are_the_declared_spine_order():
    # The routing table above is meaningless if SN..TC are not 0..3, and the
    # same ordering is the spine-stage axis — one ordering, two consumers.
    assert ATTEST.TIERS == ("SN", "SR", "LLR", "TC")
    assert ATTEST.TIER_INDEX == {"SN": 0, "SR": 1, "LLR": 2, "TC": 3}


@pytest.mark.parametrize("boundary", [-1, 4, 99, "1", None, True, 1.0])
def test_an_out_of_range_boundary_refuses_by_name(boundary):
    # Refused, never clamped: clamping would silently route a tier to the
    # adjudicator that the adopter reserved for a human.
    with pytest.raises(ValueError) as exc:
        ATTEST.requires_human(0, boundary)
    assert "REFUSED" in str(exc.value)
    assert "human ratification boundary" in str(exc.value)
    assert repr(boundary) in str(exc.value)


@pytest.mark.parametrize("tier", [-1, 4, "SR", None])
def test_an_out_of_range_tier_index_refuses_by_name(tier):
    with pytest.raises(ValueError) as exc:
        ATTEST.requires_human(tier, 1)
    assert "spine tier index" in str(exc.value)
    assert repr(tier) in str(exc.value)


def test_the_declared_default_boundary_is_used_when_no_config_exists(tmp_path):
    # config.py is another slice; the deferred import must degrade to the
    # declared default rather than failing the import chain (contracts §6).
    assert ATTEST.boundary_from_config(tmp_path) == ATTEST.DEFAULT_BOUNDARY


# --- TC-157: canonicalisation and the normative digest (SR-143 / LLR-163) -----
# identical | re-wrapped | reworded-normative | reworded-non-normative
def sr_row(**overrides):
    row = {
        "SR-ID": "SR-001",
        "Title": "Addition",
        "SN-Refs": "SN-001",
        "Requirement": "The system shall add two numbers.",
        "Rationale": "Realizes SN-001.",
        "AcceptanceCriteria": "add(1,2) == 3",
        "Permutations": "",
        "Priority": "M",
        "Verification": "Test",
        "Status": "Verified",
        "Phase": "1",
    }
    row.update(overrides)
    return row


def test_identical_rows_digest_identically():
    assert ATTEST.normative_digest("SR", sr_row()) == ATTEST.normative_digest(
        "SR", sr_row()
    )


def test_a_rewrap_produces_the_same_digest():
    # Every canonicalisation rule contracts §4 declares, at once: a run of
    # spaces, a tab, and leading/trailing whitespace. None is a meaning change,
    # so none may cost a re-attestation.
    rewrapped = sr_row(
        Requirement="  The system shall   add  two	numbers.   ",
        Title="Addition ",
        Priority=" M",
    )
    assert ATTEST.normative_digest("SR", rewrapped) == ATTEST.normative_digest(
        "SR", sr_row()
    )


def test_a_crlf_checkout_digests_like_an_lf_one():
    # The rule that matters most in practice: a Windows checkout with autocrlf
    # must not re-digest the entire spine.
    crlf = "The system shall add two numbers." + CR + LF + "   Twice.  "
    lf = "The system shall add two numbers." + LF + "Twice."
    assert ATTEST.normative_digest(
        "SR", sr_row(Requirement=crlf)
    ) == ATTEST.normative_digest("SR", sr_row(Requirement=lf))


def test_a_composed_and_decomposed_grapheme_digest_alike():
    # NFC first (contracts §4 step 1): an editor that normalises on save is not
    # an amendment. The two literals below are deliberately different BYTES.
    composed = ATTEST.normative_digest("SR", sr_row(Title="Résumé"))
    decomposed = ATTEST.normative_digest("SR", sr_row(Title="Résumé"))
    assert composed == decomposed


def test_a_hard_newline_is_a_digest_change_by_declared_rule():
    # The declared BOUNDARY of the canonicalisation, asserted rather than
    # assumed: step 3 collapses runs of spaces and tabs, not line breaks, and
    # step 4 strips per line — so lines survive. Reflowing a quoted CSV cell
    # ACROSS lines therefore moves the digest and reads as a candidate; the
    # adjudicator's `clarity` verdict is the declared answer to that, not a
    # wider canonicalisation. Change this only by changing contracts §4 and the
    # `attest-v1` prefix together.
    wrapped = "The system shall" + LF + "add two numbers."
    assert ATTEST.normative_digest(
        "SR", sr_row(Requirement=wrapped)
    ) != ATTEST.normative_digest("SR", sr_row())


def test_a_reworded_normative_cell_produces_a_different_digest():
    reworded = sr_row(Requirement="The system shall add three numbers.")
    assert ATTEST.normative_digest("SR", reworded) != ATTEST.normative_digest(
        "SR", sr_row()
    )


def test_a_non_normative_cell_change_produces_the_same_digest():
    # Status/Phase/Rationale are outside the declared cell list, so a
    # bookkeeping edit is never an amendment.
    moved = sr_row(Status="Modified", Phase="2", Rationale="Rewritten rationale.")
    assert ATTEST.normative_digest("SR", moved) == ATTEST.normative_digest(
        "SR", sr_row()
    )


def test_a_non_normative_change_produces_no_candidate(tmp_path):
    docs = make_docs(tmp_path)
    ATTEST.seed(tmp_path, docs, by="test")
    assert ATTEST.detect_candidates(tmp_path, docs) == []
    (docs / "requirements" / "system-requirements.csv").write_text(
        SRS_H + SRS.replace(",Verified,1,core,", ",Modified,2,core,"),
        encoding="utf-8",
        newline="\n",
    )
    assert ATTEST.detect_candidates(tmp_path, docs) == []


def test_the_digest_binds_the_kind_and_the_id():
    # Two artifacts with identical prose are two anchors, or moving a row's
    # text to a new id would inherit the old id's approval.
    other = sr_row(**{"SR-ID": "SR-002"})
    assert ATTEST.normative_digest("SR", other) != ATTEST.normative_digest(
        "SR", sr_row()
    )
    llr = {"LLR-ID": "SR-001", "SR-Refs": "SN-001", "Title": "Addition", "Detail": ""}
    assert ATTEST.normative_digest("LLR", llr) != ATTEST.normative_digest(
        "SR", sr_row()
    )


def test_the_digest_carries_its_rule_version():
    # The prefix is inside the hashed bytes, so changing the canonicalisation
    # rule makes old anchors recognisably old rather than silently wrong.
    assert ATTEST.DIGEST_PREFIX == "attest-v1"
    v1 = ATTEST.normative_digest("SR", sr_row())
    try:
        ATTEST.DIGEST_PREFIX = "attest-v2"
        v2 = ATTEST.normative_digest("SR", sr_row())
    finally:
        ATTEST.DIGEST_PREFIX = "attest-v1"
    assert v1 != v2
    assert ATTEST.normative_digest("SR", sr_row()) == v1


def test_an_unknown_kind_and_an_id_less_row_refuse_by_name():
    with pytest.raises(ValueError) as exc:
        ATTEST.normative_digest("WI", {"WI-ID": "WI-001"})
    assert "not a spine artifact kind" in str(exc.value)
    with pytest.raises(ValueError) as exc:
        ATTEST.normative_digest("SR", sr_row(**{"SR-ID": "  "}))
    assert "SR-ID" in str(exc.value)


def test_sn_cells_come_from_the_markdown_table_row():
    rows = ATTEST.sn_rows(SN_MD)
    assert [r["SN-ID"] for r in rows] == ["SN-001"]  # the -000 example is excluded
    assert rows[0]["Priority"] == "M"
    assert rows[0]["Acceptance"] == "add(1,2) gives 3."
    # A short row (the edge-case table is three cells wide) pads rather than
    # dropping the need — an edge-case need is still a need.
    short = ATTEST.sn_rows("| SN-013 | Provision | No interpreter | reports clearly |")
    assert short[0]["Acceptance"] == ""
    assert short[0]["Why"] == "No interpreter"


# --- TC-158: the append-only chain (SR-143 / LLR-164) ------------------------
# first | successor | stale-parent | override
def test_first_and_successor_events_append_and_become_the_head(tmp_path):
    first = ATTEST.append_event(
        tmp_path, ATTEST.attestation_event("SR", "SR-001", "d1", "ratified", None, "me")
    )
    assert head_id(tmp_path, "attestation", "SR", "SR-001") == first["id"]
    second = ATTEST.append_event(
        tmp_path,
        ATTEST.attestation_event("SR", "SR-001", "d2", "meaning", first["id"], "me"),
    )
    assert head_id(tmp_path, "attestation", "SR", "SR-001") == second["id"]
    assert len(ledger_lines(tmp_path, "attestation")) == 2


def test_a_stale_parent_is_refused_and_the_ledger_is_untouched(tmp_path):
    first = ATTEST.append_event(
        tmp_path, ATTEST.attestation_event("SR", "SR-001", "d1", "ratified", None, "me")
    )
    ATTEST.append_event(
        tmp_path,
        ATTEST.attestation_event("SR", "SR-001", "d2", "meaning", first["id"], "me"),
    )
    before = ledger_lines(tmp_path, "attestation")
    with pytest.raises(ValueError) as exc:
        ATTEST.append_event(
            tmp_path,
            ATTEST.attestation_event(
                "SR", "SR-001", "d3", "ratified", first["id"], "me"
            ),
        )
    assert "SR-001" in str(exc.value) and "head of that chain" in str(exc.value)
    assert ledger_lines(tmp_path, "attestation") == before


def test_a_first_event_naming_a_parent_is_refused(tmp_path):
    with pytest.raises(ValueError) as exc:
        ATTEST.append_event(
            tmp_path,
            ATTEST.attestation_event(
                "SR", "SR-001", "d1", "ratified", "deadbeef", "me"
            ),
        )
    assert "'deadbeef'" in str(exc.value) and "None" in str(exc.value)


def test_an_override_appends_without_editing_history(tmp_path):
    first = ATTEST.append_event(
        tmp_path, ATTEST.attestation_event("SR", "SR-001", "d1", "ratified", None, "me")
    )
    pending = ATTEST.append_event(
        tmp_path,
        ATTEST.attestation_event("SR", "SR-001", "d2", "meaning", first["id"], "me"),
    )
    before = ledger_lines(tmp_path, "attestation")
    ATTEST.append_event(
        tmp_path,
        ATTEST.attestation_event(
            "SR", "SR-001", "d2", "override", pending["id"], "owner", accepted=True
        ),
    )
    after = ledger_lines(tmp_path, "attestation")
    assert after[:2] == before  # history is bytes, not opinion
    assert len(after) == 3
    assert ATTEST.accepted_anchor(tmp_path, "SR", "SR-001")["digest"] == "d2"


def test_an_override_must_say_whether_it_accepts(tmp_path):
    with pytest.raises(ValueError) as exc:
        ATTEST.append_event(
            tmp_path,
            ATTEST.attestation_event("SR", "SR-001", "d1", "override", None, "owner"),
        )
    assert "accepted" in str(exc.value)


def test_a_rejecting_override_does_not_become_the_anchor(tmp_path):
    first = ATTEST.append_event(
        tmp_path, ATTEST.attestation_event("SR", "SR-001", "d1", "ratified", None, "me")
    )
    ATTEST.append_event(
        tmp_path,
        ATTEST.attestation_event(
            "SR", "SR-001", "d2", "override", first["id"], "owner", accepted=False
        ),
    )
    assert ATTEST.accepted_anchor(tmp_path, "SR", "SR-001")["digest"] == "d1"


def test_a_meaning_decision_is_pending_and_does_not_move_the_anchor(tmp_path):
    first = ATTEST.append_event(
        tmp_path, ATTEST.attestation_event("SR", "SR-001", "d1", "ratified", None, "me")
    )
    ATTEST.append_event(
        tmp_path,
        ATTEST.attestation_event("SR", "SR-001", "d2", "meaning", first["id"], "me"),
    )
    assert ATTEST.accepted_anchor(tmp_path, "SR", "SR-001")["digest"] == "d1"
    events = ATTEST.read_events(ATTEST.ledger_path(tmp_path, "attestation"))
    chain = ATTEST.chain_map(events)[("SR", "SR-001")]
    assert ATTEST.chain_state(chain, "d2") == ATTEST.PENDING


def test_a_clarity_decision_advances_the_anchor(tmp_path):
    first = ATTEST.append_event(
        tmp_path, ATTEST.attestation_event("SR", "SR-001", "d1", "ratified", None, "me")
    )
    ATTEST.append_event(
        tmp_path,
        ATTEST.attestation_event("SR", "SR-001", "d2", "clarity", first["id"], "me"),
    )
    assert ATTEST.accepted_anchor(tmp_path, "SR", "SR-001")["digest"] == "d2"


def test_chains_are_per_artifact(tmp_path):
    # Two artifacts must not serialise against each other, or the first row
    # attested would block every other row's first event.
    ATTEST.append_event(
        tmp_path, ATTEST.attestation_event("SR", "SR-001", "d1", "ratified", None, "me")
    )
    ATTEST.append_event(
        tmp_path, ATTEST.attestation_event("SR", "SR-002", "d1", "ratified", None, "me")
    )
    assert len(ledger_lines(tmp_path, "attestation")) == 2


def test_observing_the_same_fact_twice_is_not_two_events(tmp_path):
    # `ts` is excluded from the id precisely so that a second observation of one
    # fact is not a second event (contracts §2) — assert the property, then the
    # refusal it buys. Inside a CHAINED ledger the parent rule is what fires
    # (`parent` is part of the digested payload, so the second write also names
    # a stale head); the id guard behind it covers a ledger repaired or written
    # out of band.
    event = ATTEST.attestation_event("SR", "SR-001", "d1", "ratified", None, "me")
    assert ATTEST.event_id(dict(event, ts="2026-08-08T00:00:00Z")) == ATTEST.event_id(
        dict(event, ts="2026-08-09T00:00:00Z")
    )
    ATTEST.append_event(tmp_path, event, ts="2026-08-08T00:00:00Z")
    with pytest.raises(ValueError) as exc:
        ATTEST.append_event(tmp_path, event, ts="2026-08-09T00:00:00Z")
    assert "SR-001" in str(exc.value)
    assert len(ledger_lines(tmp_path, "attestation")) == 1


def test_the_event_id_is_content_derived_and_verifiable(tmp_path):
    event = ATTEST.append_event(
        tmp_path,
        ATTEST.attestation_event("SR", "SR-001", "d1", "ratified", None, "me"),
        ts="2026-08-08T00:00:00Z",
    )
    assert len(event["id"]) == 16
    assert event["id"] == ATTEST.event_id(event)
    payload = json.loads(ledger_lines(tmp_path, "attestation")[0])
    assert payload == event
    # A caller cannot bring its own id: the ledger mints it from the facts, and
    # silently overwriting a supplied one would hide the caller's bug.
    with pytest.raises(ValueError) as exc:
        ATTEST.append_event(tmp_path, event)
    assert "must not carry an `id`" in str(exc.value)


def test_a_malformed_line_is_a_hard_read_error_naming_file_and_line(tmp_path):
    ATTEST.append_event(
        tmp_path, ATTEST.attestation_event("SR", "SR-001", "d1", "ratified", None, "me")
    )
    path = ATTEST.ledger_path(tmp_path, "attestation")
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write("{not json\n")
    with pytest.raises(ValueError) as exc:
        ATTEST.read_events(path)
    assert "attestation.jsonl:2" in str(exc.value)


def test_a_hand_edited_line_is_refused_because_its_id_no_longer_derives(tmp_path):
    event = ATTEST.append_event(
        tmp_path, ATTEST.attestation_event("SR", "SR-001", "d1", "ratified", None, "me")
    )
    path = ATTEST.ledger_path(tmp_path, "attestation")
    tampered = dict(event, digest="d9")
    path.write_text(
        json.dumps(tampered, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    with pytest.raises(ValueError) as exc:
        ATTEST.read_events(path)
    assert "does not match its payload" in str(exc.value)
    assert "attestation.jsonl:1" in str(exc.value)


def test_an_unknown_key_and_a_bad_schema_refuse_by_name(tmp_path):
    with pytest.raises(ValueError) as exc:
        ATTEST.append_event(
            tmp_path,
            ATTEST.attestation_event(
                "SR", "SR-001", "d1", "ratified", None, "me", desicion="typo"
            ),
        )
    assert "'desicion'" in str(exc.value)
    with pytest.raises(ValueError) as exc:
        ATTEST.append_event(
            tmp_path,
            dict(
                ATTEST.attestation_event("SR", "SR-001", "d1", "ratified", None, "me"),
                schema=99,
            ),
        )
    assert "schema" in str(exc.value)


def test_an_unknown_decision_and_a_non_spine_artifact_kind_refuse(tmp_path):
    with pytest.raises(ValueError) as exc:
        ATTEST.append_event(
            tmp_path,
            ATTEST.attestation_event("SR", "SR-001", "d1", "approved", None, "me"),
        )
    assert "'approved'" in str(exc.value)
    with pytest.raises(ValueError) as exc:
        ATTEST.append_event(
            tmp_path,
            ATTEST.attestation_event("WI", "WI-001", "d1", "ratified", None, "me"),
        )
    assert "not a spine tier" in str(exc.value)


def test_the_ledger_is_written_with_lf_newlines(tmp_path):
    ATTEST.append_event(
        tmp_path, ATTEST.attestation_event("SR", "SR-001", "d1", "ratified", None, "me")
    )
    raw = ATTEST.ledger_path(tmp_path, "attestation").read_bytes()
    assert b"\r\n" not in raw and raw.endswith(b"\n")


# --- detect_candidates: the two cases the staged check cannot see -------------
def test_a_row_changed_while_it_stays_verified_is_a_candidate(tmp_path):
    docs = make_docs(tmp_path)
    ATTEST.seed(tmp_path, docs, by="test")
    (docs / "requirements" / "system-requirements.csv").write_text(
        SRS_H + SRS.replace("add two numbers", "add three numbers"),
        encoding="utf-8",
        newline="\n",
    )
    candidates = ATTEST.detect_candidates(tmp_path, docs)
    assert [c["id"] for c in candidates] == ["SR-001"]
    assert candidates[0]["state"] == ATTEST.CHANGED
    assert "changed since its accepted anchor" in candidates[0]["reason"]


def test_the_sanctioned_amend_and_flip_to_modified_is_a_candidate(tmp_path):
    # staged_spine_amendments skips a row whose Status moved, by design. The
    # digest does not care about Status, so the amend-and-flip is still caught.
    docs = make_docs(tmp_path)
    ATTEST.seed(tmp_path, docs, by="test")
    amended = SRS.replace("add two numbers", "add three numbers").replace(
        ",Verified,1,core,", ",Modified,1,core,"
    )
    (docs / "requirements" / "system-requirements.csv").write_text(
        SRS_H + amended, encoding="utf-8", newline="\n"
    )
    assert [c["id"] for c in ATTEST.detect_candidates(tmp_path, docs)] == ["SR-001"]


def test_every_tier_is_a_candidate_before_seeding_and_none_after(tmp_path):
    docs = make_docs(tmp_path)
    before = ATTEST.detect_candidates(tmp_path, docs)
    assert [c["kind"] for c in before] == ["SN", "SR", "LLR", "TC"]
    assert all(c["state"] == ATTEST.UNATTESTED for c in before)
    written = ATTEST.seed(tmp_path, docs, by="test")
    assert written == {"SN": 1, "SR": 1, "LLR": 1, "TC": 1}
    assert ATTEST.detect_candidates(tmp_path, docs) == []
    # Seeding is idempotent: a second run has nothing left to anchor.
    assert ATTEST.seed(tmp_path, docs, by="test") == {
        "SN": 0,
        "SR": 0,
        "LLR": 0,
        "TC": 0,
    }


def test_a_pending_meaning_event_keeps_the_row_a_candidate(tmp_path):
    docs = make_docs(tmp_path)
    ATTEST.seed(tmp_path, docs, by="test")
    head = head_id(tmp_path, "attestation", "SR", "SR-001")
    new_text = SRS.replace("add two numbers", "add three numbers")
    (docs / "requirements" / "system-requirements.csv").write_text(
        SRS_H + new_text, encoding="utf-8", newline="\n"
    )
    digest = ATTEST.detect_candidates(tmp_path, docs)[0]["digest"]
    ATTEST.append_event(
        tmp_path,
        ATTEST.attestation_event("SR", "SR-001", digest, "meaning", head, "owner"),
    )
    candidates = ATTEST.detect_candidates(tmp_path, docs)
    assert candidates[0]["state"] == ATTEST.PENDING
    assert "pending meaning event" in candidates[0]["reason"]


# --- TC-161: durable review requests (SR-144 / LLR-167) ----------------------
# recorded | after-restart | closed | persistent-policy
def record_request(root, reason="pre-release full-spine review", by="owner"):
    events = ATTEST.read_events(ATTEST.ledger_path(root, "review-request"))
    parent = events[-1]["id"] if events else None
    return ATTEST.append_event(root, ATTEST.review_request_event(reason, by, parent))


def close_request(root, request_id, by="owner", verdict="approved"):
    events = ATTEST.read_events(ATTEST.ledger_path(root, "review-request"))
    parent = events[-1]["id"] if events else None
    return ATTEST.append_event(
        root, ATTEST.review_decision_event(request_id, verdict, by, parent)
    )


def test_a_recorded_request_is_open_and_blocks_the_checkpoint(tmp_path):
    assert ATTEST.review_requests(tmp_path) == []
    assert ATTEST.full_spine_block(tmp_path) is None
    request = record_request(tmp_path)
    assert [r["id"] for r in ATTEST.review_requests(tmp_path)] == [request["id"]]
    block = ATTEST.full_spine_block(tmp_path)
    assert request["id"] in block and "pre-release" in block


def test_the_open_set_survives_a_process_restart(tmp_path):
    # The whole point of SR-144: a fresh process holding NO in-memory state
    # replays the ledger and reaches the same answer, because open-ness is
    # derived rather than stored.
    request = record_request(tmp_path)
    restarted = load_script("attest")
    assert restarted is not ATTEST
    assert [r["id"] for r in restarted.review_requests(tmp_path)] == [request["id"]]
    assert restarted.full_spine_block(tmp_path) is not None


def test_a_recorded_human_decision_closes_the_request(tmp_path):
    request = record_request(tmp_path)
    close_request(tmp_path, request["id"])
    assert ATTEST.review_requests(tmp_path) == []
    assert ATTEST.full_spine_block(tmp_path) is None
    # Closing is an APPEND: both events are still on disk.
    assert len(ledger_lines(tmp_path, "review-request")) == 2


def test_the_persistent_policy_blocks_without_any_request_event(tmp_path):
    assert ATTEST.review_requests(tmp_path) == []
    assert ATTEST.full_spine_block(tmp_path, policy="always") == (
        "final_full_spine_review=always"
    )
    assert ATTEST.full_spine_block(tmp_path, policy="never") is None


def test_two_requests_close_independently(tmp_path):
    first = record_request(tmp_path, "first ask")
    second = record_request(tmp_path, "second ask")
    close_request(tmp_path, first["id"])
    assert [r["id"] for r in ATTEST.review_requests(tmp_path)] == [second["id"]]


def test_a_decision_naming_an_unknown_or_closed_request_refuses(tmp_path):
    request = record_request(tmp_path)
    with pytest.raises(ValueError) as exc:
        close_request(tmp_path, "0123456789abcdef")
    assert "not in the ledger" in str(exc.value)
    close_request(tmp_path, request["id"])
    with pytest.raises(ValueError) as exc:
        close_request(tmp_path, request["id"], verdict="again")
    assert "already closed" in str(exc.value)


def test_an_unattributed_request_is_refused(tmp_path):
    with pytest.raises(ValueError) as exc:
        ATTEST.append_event(tmp_path, ATTEST.review_request_event("why", "", None))
    assert "'by'" in str(exc.value) or "by" in str(exc.value)


# --- the CLI arms -------------------------------------------------------------
def test_cli_seed_then_candidates_reports_a_moved_row(tmp_path, capsys):
    docs = make_docs(tmp_path)
    args = ["--root", str(tmp_path), "--docs", str(docs)]
    assert ATTEST.main(args + ["--seed"]) == 0
    assert "seeded 4 anchor(s)" in capsys.readouterr().out
    assert ATTEST.main(args + ["--candidates"]) == 0
    assert "OK" in capsys.readouterr().out
    (docs / "requirements" / "system-requirements.csv").write_text(
        SRS_H + SRS.replace("add two numbers", "add three numbers"),
        encoding="utf-8",
        newline="\n",
    )
    assert ATTEST.main(args + ["--candidates"]) == 1
    out = capsys.readouterr().out
    assert "CANDIDATE" in out and "SR-001" in out


def test_cli_request_open_decide_round_trip(tmp_path, capsys):
    args = ["--root", str(tmp_path)]
    assert ATTEST.main(args + ["--request", "final look", "--by", "owner"]) == 0
    # Matched, not scraped off the last token: the arm also names the generated
    # artifacts the write staled, and a positional parse reads one of those.
    recorded = re.search(
        r"recorded review request ([0-9a-f]{16})", capsys.readouterr().out
    )
    assert recorded
    request_id = recorded.group(1)
    assert ATTEST.main(args + ["--open"]) == 0
    assert "final look" in capsys.readouterr().out
    assert ATTEST.main(args + ["--decide", request_id, "--by", "owner"]) == 0
    capsys.readouterr()
    assert ATTEST.main(args + ["--open"]) == 0
    assert "no open review requests" in capsys.readouterr().out


def test_cli_refuses_an_unattributed_ask_and_a_corrupt_ledger(tmp_path, capsys):
    assert ATTEST.main(["--root", str(tmp_path), "--request", "why"]) == 1
    assert "REFUSED" in capsys.readouterr().err
    path = ATTEST.ledger_path(tmp_path, "attestation")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("not json\n", encoding="utf-8", newline="\n")
    docs = make_docs(tmp_path)
    assert ATTEST.main(["--root", str(tmp_path), "--docs", str(docs), "--seed"]) == 1
    assert "attestation.jsonl:1" in capsys.readouterr().err


# --- review-B 2 / 5 / 20: the id must be THERE, or nothing can verify the line -
def write_lines(root, ledger_kind, *payloads):
    """Hand-write raw ledger lines, the way an editor or a repair script would."""
    path = ATTEST.ledger_path(root, ledger_kind)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(
        json.dumps(p, sort_keys=True, separators=(",", ":")) + "\n" for p in payloads
    )
    path.write_text(body, encoding="utf-8", newline="\n")
    return path


ID_LESS_ANCHOR = {
    "schema": 1,
    "kind": "attestation",
    "artifact_kind": "SR",
    "artifact_id": "SR-001",
    "digest": "deadbeef",
    "decision": "ratified",
    "parent": None,
}
ID_LESS_REQUEST = {
    "schema": 1,
    "kind": "review-request",
    "artifact_kind": "review",
    "artifact_id": "full-spine",
    "reason": "hand-written",
    "by": "someone",
    "parent": None,
}


def test_an_id_less_line_is_refused_on_read_rather_than_trusted_as_an_anchor(tmp_path):
    # Dropping `id` was the one edit that passed every rung: the derived-id check
    # was gated on the presence of the field it checks, so the line was accepted
    # unverified and then trusted as THE accepted anchor.
    path = write_lines(tmp_path, "attestation", ID_LESS_ANCHOR)
    with pytest.raises(ValueError) as exc:
        ATTEST.read_events(path)
    assert "REFUSED" in str(exc.value)
    assert "attestation.jsonl:1" in str(exc.value)
    assert "no `id`" in str(exc.value)
    with pytest.raises(ValueError):
        ATTEST.accepted_anchor(tmp_path, "SR", "SR-001")


def test_an_id_less_line_refuses_the_next_append_by_name_not_with_a_key_error(tmp_path):
    # The reader crashed with a bare `KeyError: 'id'` at `chain[-1]["id"]`, which
    # `main()` does not catch — so the declared refusal shape was never printed.
    write_lines(tmp_path, "attestation", ID_LESS_ANCHOR)
    with pytest.raises(ValueError) as exc:
        ATTEST.append_event(
            tmp_path, ATTEST.attestation_event("SR", "SR-001", "d2", "ratified", None)
        )
    assert "REFUSED" in str(exc.value)


def test_an_id_less_review_request_refuses_the_cli_instead_of_tracebacking(
    tmp_path, capsys
):
    # `_open_requests` indexes the open set BY id, so an id-less request line
    # killed --checkpoint/--open/--request with a KeyError escaping main().
    write_lines(tmp_path, "review-request", ID_LESS_REQUEST)
    docs = make_docs(tmp_path)
    args = ["--root", str(tmp_path), "--docs", str(docs)]
    assert ATTEST.main(args + ["--checkpoint"]) == 1
    assert "REFUSED" in capsys.readouterr().err
    assert ATTEST.main(args + ["--open"]) == 1
    assert "review-requests.jsonl:1" in capsys.readouterr().err


# --- review-B 6 / 8 / 23 / 37: what the one-time migration may NOT do ---------
def amend_sr(docs, text="add three numbers"):
    (docs / "requirements" / "system-requirements.csv").write_text(
        SRS_H + SRS.replace("add two numbers", text), encoding="utf-8", newline="\n"
    )


def chain_of(root, kind, rid):
    events = ATTEST.read_events(ATTEST.ledger_path(root, "attestation"))
    return [
        (e["decision"], e.get("by"))
        for e in events
        if ATTEST.chain_key(e) == (kind, rid)
    ]


def test_seed_does_not_re_ratify_an_amended_row(tmp_path):
    # The guard asked "is the current text accepted?" when the migration's
    # question is "does this row have ANY history?" — so an amended row fell
    # through and got a fresh accepting anchor at the NEW digest, with no human
    # decision and no clarity-vs-meaning call.
    docs = make_docs(tmp_path)
    ATTEST.seed(tmp_path, docs, by="seed")
    amend_sr(docs)
    assert [c["state"] for c in ATTEST.detect_candidates(tmp_path, docs)] == [
        ATTEST.CHANGED
    ]
    assert ATTEST.seed(tmp_path, docs, by="seed")["SR"] == 0
    assert len(chain_of(tmp_path, "SR", "SR-001")) == 1
    assert [c["id"] for c in ATTEST.detect_candidates(tmp_path, docs)] == ["SR-001"]


def test_seed_does_not_walk_over_a_standing_meaning_verdict(tmp_path):
    # `meaning` is the one decision the module documents as never accepting. A
    # migration command answering it — with `by="seed"` — is the ratification
    # boundary being crossed by a machine.
    docs = make_docs(tmp_path)
    ATTEST.seed(tmp_path, docs, by="seed")
    amend_sr(docs)
    candidate = ATTEST.detect_candidates(tmp_path, docs)[0]
    ATTEST.append_event(
        tmp_path,
        ATTEST.attestation_event(
            "SR",
            "SR-001",
            candidate["digest"],
            "meaning",
            head_id(tmp_path, "attestation", "SR", "SR-001"),
            "peter",
        ),
    )
    ATTEST.seed(tmp_path, docs, by="seed")
    assert chain_of(tmp_path, "SR", "SR-001") == [
        (ATTEST.BASELINE, "seed"),
        ("meaning", "peter"),
    ]
    assert ATTEST.detect_candidates(tmp_path, docs)[0]["state"] == ATTEST.PENDING


def test_a_seeded_anchor_says_baseline_not_ratified(tmp_path):
    # 523 machine migrations must not be readable as 523 human ratifications:
    # `is_accepting` decides from the decision WORD alone, and `by` is optional
    # and read by no attestation consumer.
    docs = make_docs(tmp_path)
    ATTEST.seed(tmp_path, docs, by="seed")
    events = ATTEST.read_events(ATTEST.ledger_path(tmp_path, "attestation"))
    assert {e["decision"] for e in events} == {ATTEST.BASELINE}
    assert ATTEST.BASELINE not in ATTEST.VERDICTS
    assert ATTEST.BASELINE in ATTEST.ACCEPTING  # still an anchor, just not a verdict


DRAFT_ROW = (
    "| SN-090 | A team can subtract. | Nobody has agreed to this yet. | S |"
    " sub(3,1) gives 2. |"
)
SN_WITH_DRAFT = (
    SN_MD
    + """
## Draft needs (unratified)

Ratifying a need = moving its row up into Core needs in a reviewed commit.

| SN-ID | Need (plain language) | Why it matters | Priority | Acceptance intent |
|---|---|---|---|---|
"""
    + DRAFT_ROW
    + "\n"
)


def test_the_migration_does_not_anchor_a_need_parked_under_a_draft_heading(tmp_path):
    # Anchoring a Draft need makes the declared ratification act — moving the row
    # up into the core table — produce no candidate and no event, because the row
    # is already accepted at exactly that text.
    docs = make_docs(tmp_path)
    (docs / "requirements" / "stakeholder-needs.md").write_text(
        SN_WITH_DRAFT, encoding="utf-8", newline="\n"
    )
    assert ATTEST.seed(tmp_path, docs, by="seed")["SN"] == 1
    assert chain_of(tmp_path, "SN", "SN-090") == []
    # Ratifying it = MOVING the row up into Core needs. That must raise a
    # candidate; with a draft anchor already standing at that very text it
    # raised none, and the reviewed commit passed unnoticed.
    (docs / "requirements" / "stakeholder-needs.md").write_text(
        SN_WITH_DRAFT.replace(DRAFT_ROW + "\n", "").replace(
            SN_MD, SN_MD + DRAFT_ROW + "\n"
        ),
        encoding="utf-8",
        newline="\n",
    )
    assert [c["id"] for c in ATTEST.detect_candidates(tmp_path, docs)] == ["SN-090"]


# --- review-B 7 / 11 / 21 / 29: the SN digest is per-table, and it is TOTAL ----
SN_TWO_TABLES = """# Stakeholder Needs

## Core needs

| SN-ID | Need | Why it matters | Priority | Acceptance intent |
|---|---|---|---|---|
| SN-001 | A team can add two numbers. | It is the demo need. | M | add(1,2) gives 3. |

## Edge-case expectations

| SN-ID | Lifecycle | Scenario | Expected behavior |
|---|---|---|---|
| SN-013 | Provision | No Python 3 interpreter on PATH | Reports clearly; never crashes. |
"""


def test_the_edge_case_table_records_its_own_declared_cell_names():
    # Contracts §4 declares the cells PER TABLE and names the single-table read
    # as the rejected shape: the cell NAMES are inside the hashed bytes, so
    # recording `Lifecycle` under the name `Need` misleads anyone reading a diff.
    rows = {r["SN-ID"]: r for r in ATTEST.sn_rows(SN_TWO_TABLES)}
    assert ATTEST.SN_TABLES["edge"] == ("Lifecycle", "Scenario", "Expected")
    edge = rows["SN-013"]
    assert edge["SN-Table"] == "edge"
    assert edge["Lifecycle"] == "Provision"
    assert edge["Expected"] == "Reports clearly; never crashes."
    assert "Need" not in edge and "Priority" not in edge
    assert rows["SN-001"]["SN-Table"] == "core"


def test_one_table_of_cells_cannot_answer_for_the_other():
    # The digest reads the cells of the table the row came from, so the same
    # prose under two different tables is two different records.
    core, edge = ATTEST.sn_rows(SN_TWO_TABLES)
    assert ATTEST.cells_for("SN", core) == ATTEST.NORMATIVE_CELLS["SN"]
    assert ATTEST.cells_for("SN", edge) == ATTEST.SN_TABLES["edge"]
    same_prose = {"SN-ID": "SN-013", "Lifecycle": "x", "Scenario": "y", "Expected": "z"}
    as_edge = ATTEST.normative_digest("SN", dict(same_prose, **{"SN-Table": "edge"}))
    as_core = ATTEST.normative_digest(
        "SN", {"SN-ID": "SN-013", "Need": "x", "Why": "y", "Priority": "z"}
    )
    assert as_edge != as_core


def test_a_cell_past_the_declared_width_refuses_instead_of_dropping_out_of_the_hash():
    # A row was padded to five fields and read positionally, with no counterpart
    # for a LONG row: every field past the fifth was discarded silently, so an
    # edit there changed meaning and moved no digest.
    wide = SN_TWO_TABLES.replace(
        "| SN-013 | Provision | No Python 3 interpreter on PATH |"
        " Reports clearly; never crashes. |",
        "| SN-013 | Provision | No Python 3 interpreter on PATH |"
        " Reports clearly; never crashes. | THE-LOOP-MAY-SELF-BLESS |",
    )
    with pytest.raises(ValueError) as exc:
        ATTEST.sn_rows(wide)
    assert "REFUSED" in str(exc.value)
    assert "SN-013" in str(exc.value)
    assert "would not be digested" in str(exc.value)


def test_a_genuinely_empty_last_cell_is_still_a_cell():
    # Only ONE trailing field is dropped (the closing pipe's), so an under-filled
    # row still pads rather than refusing.
    rows = ATTEST.sn_rows("## Core needs\n\n| SN-002 | Need text | Why text | M | |\n")
    assert rows[0]["Acceptance"] == ""
    assert rows[0]["Priority"] == "M"


# --- review-B 9: a dial that could not be READ never said "no" ----------------
def write_config(root, body):
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "config.toml").write_text(body, encoding="utf-8", newline="\n")


@pytest.mark.parametrize(
    "body,needle",
    [
        (
            "schema = 1\n\n[attestaton]\nhuman_ratification_through = 3\n"
            'final_full_spine_review = "always"\n',
            "attestaton",
        ),
        (
            "schema = 1\n\n[attestation]\nhuman_ratification_through = 1\n"
            'final_full_spine_reveiw = "always"\n',
            "final_full_spine_reveiw",
        ),
    ],
)
def test_a_misspelled_attestation_dial_blocks_the_checkpoint(
    tmp_path, capsys, body, needle
):
    # The filter compared against the CORRECTLY-SPELLED key names, so by
    # construction no misspelling of an attestation dial could ever match — and a
    # policy the adopter wrote as `always` answered "checkpoint clear", exit 0.
    docs = make_docs(tmp_path)
    write_config(tmp_path, body)
    projection = ATTEST.ratification_projection(tmp_path, docs)
    assert any(needle in f for f in projection["findings"]), projection["findings"]
    assert projection["boundary"] is None
    assert projection["tiers"] == []
    args = ["--root", str(tmp_path), "--docs", str(docs)]
    assert ATTEST.main(args + ["--checkpoint"]) == 1
    assert "checkpoint clear" not in capsys.readouterr().out


def test_a_finding_on_a_declared_unrelated_dial_is_still_not_ours(tmp_path):
    # The negative half, kept beside the fix: scoping is what keeps the one line
    # that changes what a human owes from being buried under the whole config
    # report. A key the loader RECOGNISED and attributed elsewhere stays there.
    docs = make_docs(tmp_path)
    write_config(
        tmp_path,
        "schema = 1\n\n[attestation]\nhuman_ratification_through = 2\n\n"
        "[policy]\npush = 'nobody'\nreview_rouunds = 1\n",
    )
    projection = ATTEST.ratification_projection(tmp_path, docs)
    assert projection["findings"] == []
    assert projection["boundary"] == 2


# --- review-B 38: the tool that broke the tree is the one that says so --------
def test_a_ledger_write_names_the_generated_artifacts_it_staled(tmp_path, capsys):
    # `docs/open-items.html` and `docs/gate` both render these ledgers, and
    # pre-commit checks both unconditionally — so the documented way to ask for a
    # review left the tree uncommittable with no hint from the tool that did it.
    docs = make_docs(tmp_path)
    assert ATTEST.main(["--root", str(tmp_path), "--docs", str(docs), "--seed"]) == 0
    seeded = capsys.readouterr().out
    assert "NOTE" in seeded
    assert "docs/gate" in seeded and "derive_gate.py" in seeded
    assert "docs/open-items.html" in seeded and "gen_open_items.py" in seeded
    assert (
        ATTEST.main(["--root", str(tmp_path), "--request", "look", "--by", "owner"])
        == 0
    )
    asked = capsys.readouterr().out
    assert "NOTE" in asked and "docs/open-items.html" in asked
    # A seed that anchored nothing broke nothing, so it must not cry stale.
    assert ATTEST.main(["--root", str(tmp_path), "--docs", str(docs), "--seed"]) == 0
    assert "NOTE" not in capsys.readouterr().out
