"""Pin the gate-policy that trace.py and derive_gate.py each carry to be equal.

The F5 rule lets the kit's scripts duplicate *plumbing* (small CSV/heading loaders)
so each stays an independently-copyable drop-in. But the two files also duplicate
*policy* — which SR Verification methods are LLR-exempt, and what "Draft" means —
and policy disagreement is a false green or false red at a gate, the exact failure
class the kit exists to prevent (repo-review-2026-07-12b.md M1 -> WI-099). These
tests mechanize the "kept in sync" promise the two files used to make only in prose:
import both modules and assert they agree.
"""

from conftest import load_script

TRACE = load_script("trace")
GATE = load_script("derive_gate")


def test_llr_exempt_sets_agree():
    # The one policy set: SR Verification methods that decompose to a TC but no
    # LLR. If one file adds a method to the exempt set and the other does not, the
    # orphan report and the derived gate disagree about what "decomposed" means.
    assert set(TRACE.LLR_EXEMPT) == set(GATE.LLR_EXEMPT)
    assert set(TRACE.LLR_EXEMPT) == {"Analysis", "Inspection", "Attest"}


def test_is_draft_agrees():
    # Both files decide the pre-ratification Draft state (Status open-vocab, only
    # "draft" acts). Pin them equivalent across the casing/whitespace/None battery.
    cases = [
        {"Status": "Draft"},
        {"Status": "draft"},
        {"Status": "  DRAFT  "},
        {"Status": "Verified"},
        {"Status": "Planned"},
        {"Status": ""},
        {"Status": None},
        {},
    ]
    for row in cases:
        assert TRACE.is_draft(row) == GATE.is_draft(row), row


def test_sn_draft_ids_agrees():
    # Both files scan stakeholder-needs.md for SNs under a "draft" heading
    # (section-as-state maturity). Pin them equivalent across headings, -000
    # placeholders, and section boundaries.
    texts = [
        "## Draft\nSN-010 something\n## Ratified\nSN-011 done\n",
        "# Needs\nSN-001\n### Draft candidates\nSN-020\nSN-021\n",
        "## DRAFT (in review)\nSN-030 SN-000 SN-031\n",
        "## Ratified only\nSN-040\n",
        "SN-050 no heading at all\n",
        "",
    ]
    for text in texts:
        assert TRACE.sn_draft_ids(text) == GATE.sn_draft_ids(text), text
