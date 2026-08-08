"""TC-159 / TC-160 — the second derived axis: spine stage, and its gate join.

`spine_stage` and `verification_gate` are separate derived facts (decision 3),
so the load-bearing assertion in this module is not just that each stage maps to
its declared gate — it is that introducing the stage moves **nothing** about the
gate. `check.py` reads the first non-comment line of `docs/gate`, and every
existing basis field is compared whole by `--check`; a stage that perturbed
either would be a silent harness change dressed as a new report.

The stage is derived from attested TEXT while the gate is derived from artifact
STRUCTURE, so the two legitimately disagree: these fixtures hold a fully
decomposed, Verified spine (G3) at every stage from 0 to 4 by moving only the
ledger. That is the state today's model cannot express at all.
"""

import sys

import pytest
from conftest import load_script

ATTEST = load_script("attest")
GATE = load_script("derive_gate")

SN_MD = """# Stakeholder Needs

| SN-ID | Need (plain language) | Why it matters | Priority | Acceptance intent |
|---|---|---|---|---|
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


def make_docs(root, srs=SRS):
    """A minimal but complete, fully decomposed and Verified spine — G3 by the
    gate's arithmetic, whatever the ledger says."""
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (root / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (req / "stakeholder-needs.md").write_text(SN_MD, encoding="utf-8", newline="\n")
    (req / "system-requirements.csv").write_text(
        SRS_H + srs, encoding="utf-8", newline="\n"
    )
    (req / "low-level-requirements.csv").write_text(
        LLRS_H + LLRS, encoding="utf-8", newline="\n"
    )
    (root / "docs" / "test" / "test-cases.csv").write_text(
        TCS_H + TCS, encoding="utf-8", newline="\n"
    )
    return root / "docs"


def anchor(root, docs, kinds, decision="ratified"):
    """Attest exactly the named tiers at their current text, in tier order."""
    artifacts = ATTEST.load_artifacts(docs)
    for kind in kinds:
        for row in artifacts[kind]:
            rid = ATTEST.row_id(kind, row)
            chain = ATTEST.chain_map(
                ATTEST.read_events(ATTEST.ledger_path(root, "attestation"))
            ).get((kind, rid), [])
            ATTEST.append_event(
                root,
                ATTEST.attestation_event(
                    kind,
                    rid,
                    ATTEST.normative_digest(kind, row),
                    decision,
                    chain[-1]["id"] if chain else None,
                    "test",
                ),
            )


def head_of(root, kind, rid):
    chain = ATTEST.chain_map(
        ATTEST.read_events(ATTEST.ledger_path(root, "attestation"))
    ).get((kind, rid), [])
    return chain[-1]["id"] if chain else None


# --- TC-160: the declared stage-to-gate table (SR-143 / LLR-166) -------------
# stage 0 | 1 | 2 | 3 | 4
STAGE_TO_GATE = {0: "G1", 1: "G1", 2: "G2", 3: "G2", 4: "G3"}


def test_the_declared_table_is_the_ratified_one():
    assert GATE.STAGE_GATE == STAGE_TO_GATE


@pytest.mark.parametrize("stage,gate", sorted(STAGE_TO_GATE.items()))
def test_every_stage_maps_to_its_declared_gate(stage, gate):
    assert GATE.verification_gate_for(stage) == gate


@pytest.mark.parametrize("stage", [-1, 5, "2", None, True, 2.0])
def test_an_out_of_range_stage_refuses_rather_than_clamping(stage):
    with pytest.raises(ValueError) as exc:
        GATE.verification_gate_for(stage)
    assert "REFUSED" in str(exc.value)
    assert repr(stage) in str(exc.value)


# The tiers attested at each stage: stage N means tier N is the first one still
# in process, so tiers 0..N-1 are accepted.
STAGE_ANCHORS = {
    0: (),
    1: ("SN",),
    2: ("SN", "SR"),
    3: ("SN", "SR", "LLR"),
    4: ("SN", "SR", "LLR", "TC"),
}


@pytest.mark.parametrize("stage", sorted(STAGE_ANCHORS))
def test_the_stage_is_present_on_the_cached_basis_line(tmp_path, stage):
    docs = make_docs(tmp_path)
    anchor(tmp_path, docs, STAGE_ANCHORS[stage])
    result = GATE.compute(docs)
    assert result["spine_stage"] == stage
    basis = GATE.basis_line(result)
    assert "spine-stage={}".format(stage) in basis
    # Read it back the way a consumer does: out of the cached file.
    cached_gate, cached_basis = GATE.parse_cache(
        GATE.render_cache(result, "abc1234", "2026-08-08")
    )
    assert cached_basis == basis
    assert cached_gate == result["gate"]
    assert GATE.verification_gate_for(stage) == STAGE_TO_GATE[stage]


def test_the_stage_changes_nothing_about_the_gate(tmp_path):
    # The same fully-decomposed Verified spine at all five stages: the runnable
    # value, the raw level, the per-phase breakdown and every pre-existing basis
    # field are byte-identical. Only `spine-stage=` moves.
    docs = make_docs(tmp_path)
    seen = set()
    for stage in sorted(STAGE_ANCHORS):
        (tmp_path / "docs" / "events" / "attestation.jsonl").unlink(missing_ok=True)
        anchor(tmp_path, docs, STAGE_ANCHORS[stage])
        result = GATE.compute(docs)
        assert result["gate"] == "G3"
        assert result["raw"] == GATE.G3
        seen.add(
            GATE.basis_line(result).replace(
                "spine-stage={}".format(stage), "spine-stage="
            )
        )
    assert len(seen) == 1, seen


def test_the_basis_line_keeps_the_open_ended_per_phase_list_last(tmp_path):
    # check.py and check_trajectory parse this line with regexes anchored on
    # `\\bper-phase=(\\S+)`; a field appended AFTER it would be swallowed by that
    # `\\S+` on a per-phase value that ends in a separator.
    docs = make_docs(tmp_path)
    basis = GATE.basis_line(GATE.compute(docs))
    assert basis.index("spine-stage=") < basis.index("per-phase=")
    assert basis.rstrip().endswith("per-phase=1=G3")


def test_an_absent_ledger_reads_stage_zero_not_a_vacuous_four(tmp_path):
    docs = make_docs(tmp_path)
    assert not (tmp_path / "docs" / "events").exists()
    assert GATE.spine_stage(docs) == 0


def test_an_empty_spine_reads_stage_zero(tmp_path):
    # The stage's mirror of the gate's vacuous-G3 refusal: nothing to attest is
    # not "implemented and validated".
    docs = tmp_path / "docs"
    (docs / "requirements").mkdir(parents=True)
    assert GATE.spine_stage(docs) == 0


# --- TC-159: the meaning verdict at each tier (SR-143 / LLR-165) -------------
# need | requirement | low-level | test-case | clarity
MEANING_CASES = {
    "need": ("SN", "SN-001", 0),
    "requirement": ("SR", "SR-001", 1),
    "low-level": ("LLR", "LLR-001", 2),
    "test-case": ("TC", "TC-001", 3),
}


@pytest.mark.parametrize("case", sorted(MEANING_CASES))
def test_a_meaning_verdict_derives_the_stage_of_the_tier_it_names(tmp_path, case):
    kind, rid, expected = MEANING_CASES[case]
    docs = make_docs(tmp_path)
    ATTEST.seed(tmp_path, docs, by="test")
    assert GATE.spine_stage(docs) == 4  # every tier accepted first

    row = next(
        r for r in ATTEST.load_artifacts(docs)[kind] if ATTEST.row_id(kind, r) == rid
    )
    digest = ATTEST.normative_digest(kind, row)
    ATTEST.append_event(
        tmp_path,
        ATTEST.attestation_event(
            kind, rid, digest, "meaning", head_of(tmp_path, kind, rid), "owner"
        ),
    )
    assert GATE.spine_stage(docs) == expected
    # The gate is untouched by the stage regression — the two axes are separate.
    assert GATE.compute(docs)["gate"] == "G3"
    assert GATE.verification_gate_for(expected) == STAGE_TO_GATE[expected]


def test_a_clarity_verdict_advances_the_anchor_and_leaves_the_stage(tmp_path):
    # A digest change that is not a meaning change: the full stop is dropped.
    # Before the verdict the row is honestly a candidate; the clarity verdict
    # re-accepts the NEW text and the stage returns to where it stood, without
    # anyone re-litigating the requirement.
    docs = make_docs(tmp_path)
    ATTEST.seed(tmp_path, docs, by="test")
    assert GATE.spine_stage(docs) == 4

    reworded = SRS.replace("add two numbers.", "add two numbers")
    (docs / "requirements" / "system-requirements.csv").write_text(
        SRS_H + reworded, encoding="utf-8", newline="\n"
    )
    assert GATE.spine_stage(docs) == 1  # in process until someone decides
    candidate = ATTEST.detect_candidates(tmp_path, docs)[0]
    assert candidate["id"] == "SR-001"

    ATTEST.append_event(
        tmp_path,
        ATTEST.attestation_event(
            "SR",
            "SR-001",
            candidate["digest"],
            "clarity",
            head_of(tmp_path, "SR", "SR-001"),
            "owner",
        ),
    )
    assert GATE.spine_stage(docs) == 4
    anchor_event = ATTEST.accepted_anchor(tmp_path, "SR", "SR-001")
    assert anchor_event["digest"] == candidate["digest"]
    assert ATTEST.detect_candidates(tmp_path, docs) == []


def test_the_lowest_unaccepted_tier_wins(tmp_path):
    # Two tiers pending at once: the stage names the LOWEST, because that is the
    # tier the workflow has to re-open first.
    docs = make_docs(tmp_path)
    ATTEST.seed(tmp_path, docs, by="test")
    for kind, rid in (("SR", "SR-001"), ("TC", "TC-001")):
        row = next(
            r
            for r in ATTEST.load_artifacts(docs)[kind]
            if ATTEST.row_id(kind, r) == rid
        )
        ATTEST.append_event(
            tmp_path,
            ATTEST.attestation_event(
                kind,
                rid,
                ATTEST.normative_digest(kind, row),
                "meaning",
                head_of(tmp_path, kind, rid),
                "owner",
            ),
        )
    assert GATE.spine_stage(docs) == 1


def test_a_corrupt_ledger_refuses_by_name_instead_of_reporting_a_stage(
    tmp_path, monkeypatch, capsys
):
    # A ledger that cannot be read must not silently degrade to "stage 0" — that
    # would be a fabricated fact. The refusal names file and line, and the CLI
    # (which the pre-commit hook runs) prints it rather than a traceback.
    docs = make_docs(tmp_path)
    ATTEST.seed(tmp_path, docs, by="test")
    path = ATTEST.ledger_path(tmp_path, "attestation")
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write("{oops\n")
    with pytest.raises(ValueError) as exc:
        GATE.spine_stage(docs)
    assert "attestation.jsonl:5" in str(exc.value)
    monkeypatch.setattr(
        sys, "argv", ["derive_gate.py", "--root", str(tmp_path), "--print"]
    )
    assert GATE.main() == 1
    assert "attestation.jsonl:5" in capsys.readouterr().err
