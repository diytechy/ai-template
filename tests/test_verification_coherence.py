"""The verification-coherence advisory on an Inspection row (TC-275).

`trace_text.verification_coherence_advisories` hunts a row whose prose claims a
critique instrument while its `Verification` says another method, the rot a
row mechanized out of Critique leaves behind. The detector is lexical, so a row
whose SUBJECT is a rubric or a verdict reads to it as a row claiming one as its
instrument. An Inspection row whose requirement SUBJECT (the text before its
`shall`) names a Critique record states what is inspected, never a second
method, so it is exempt. Every other Inspection row, including one that names a
Critique record only after its `shall`, is still judged.

The rest of the advisory's contract (the case split, the scanned cells, the one
direction) is pinned in `tests/test_trace_rules.py`.
"""

from conftest import load_script

TEXT = load_script("trace_text")

# The shape of the row the false positive was measured on: a requirement whose
# subject is Critique acceptance records, verified by Inspection.
SUBJECT_IS_A_RUBRIC = {
    "SR-ID": "SR-101",
    "Verification": "Inspection",
    "Requirement": "Where a capability requires Critique acceptance, the delivered "
    "acceptance record shall name its rubric and anchor every verdict.",
    "AcceptanceCriteria": "A Critique acceptance record names the rubric and ties "
    "every VERDICT and finding to a numbered rubric-anchor id.",
    "Rationale": "The record's process and provenance are inspectable against a "
    "written rubric.",
}


# The counterexample the exemption must not swallow: an Inspection row about
# something else whose acceptance directs an independent Critique verdict. That
# row states two methods, and the advisory exists for it.
DIRECTS_A_VERDICT = {
    "SR-ID": "SR-102",
    "Verification": "Inspection",
    "Requirement": "The delivered view shall keep every label legible at default zoom.",
    "AcceptanceCriteria": "A fresh CRITIQUE session returns APPROVE against the "
    "legibility rubric.",
}


def test_an_inspection_row_whose_subject_is_a_critique_record_raises_nothing():
    assert TEXT.verification_coherence_advisories([SUBJECT_IS_A_RUBRIC]) == []


def test_an_inspection_row_directing_an_independent_verdict_still_warns():
    [finding] = TEXT.verification_coherence_advisories([DIRECTS_A_VERDICT])
    assert "SR SR-102 AcceptanceCriteria" in finding
    assert "'Inspection'" in finding


def test_a_critique_record_named_after_the_shall_is_not_the_subject():
    # Both words present, but in the RESPONSE, after the `shall`: the row is
    # about a view that links to a record, not about the record itself, and its
    # acceptance directs an independent verdict.
    row = dict(
        DIRECTS_A_VERDICT,
        Requirement="The delivered view shall link each finding to its Critique "
        "record.",
    )
    assert len(TEXT.verification_coherence_advisories([row])) == 1


def test_a_requirement_with_no_shall_has_no_subject_to_exempt():
    row = dict(
        SUBJECT_IS_A_RUBRIC,
        Requirement="A Critique acceptance record names its rubric.",
    )
    assert len(TEXT.verification_coherence_advisories([row])) == 1


def test_a_critique_word_in_the_requirement_alone_is_not_a_record_subject():
    # The subject test asks for a Critique RECORD, not the word: a requirement
    # that merely mentions Critique keeps the advisory on.
    row = dict(
        DIRECTS_A_VERDICT,
        Requirement="The delivered view shall stay legible, Critique or not.",
    )
    assert len(TEXT.verification_coherence_advisories([row])) == 1


def test_the_same_prose_on_a_mechanized_method_still_warns():
    for method in ("Test", "Analysis", "Demonstration"):
        row = dict(SUBJECT_IS_A_RUBRIC, Verification=method)
        [finding] = TEXT.verification_coherence_advisories([row])
        assert "SR SR-101 Rationale/AcceptanceCriteria" in finding
        assert repr(method) in finding
