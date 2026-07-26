"""Pin the gate-policy that trace.py and derive_gate.py each carry to be equal.

The F5 rule lets the kit's scripts duplicate *plumbing* (small CSV/heading loaders)
so each stays an independently-copyable drop-in. But the two files also duplicate
*policy* — which SR Verification methods are LLR-exempt, and what "Draft" means —
and policy disagreement is a false green or false red at a gate, the exact failure
class the kit exists to prevent (repo-review-2026-07-12b.md M1 -> WI-099). These
tests mechanize the "kept in sync" promise the two files used to make only in prose:
import both modules and assert they agree.
"""

from conftest import load_script, make_minimal_project, run_py

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


def test_is_verified_agrees():
    # Both files decide the terminal Verified state (the G3 --require-verified
    # criterion in trace.py, the gate derivation in derive_gate.py). Matched
    # case-insensitively — the one Status-casing rule (M3 -> WI-101) — so pin the
    # two equivalent across the same casing/whitespace/None battery as is_draft.
    cases = [
        {"Status": "Verified"},
        {"Status": "verified"},
        {"Status": "  VERIFIED  "},
        {"Status": "Draft"},
        {"Status": "Planned"},
        {"Status": ""},
        {"Status": None},
        {},
    ]
    for row in cases:
        assert TRACE.is_verified(row) == GATE.is_verified(row), row


def test_is_modified_agrees():
    # Both files recognize the post-attestation Modified state (WI-316): trace.py
    # for the chain-consistency warns + the --ratify modified brief, derive_gate.py
    # for the modified=N basis count. Divergence would let a pending re-attest hide
    # from one surface while the other reports it — the same false-green class the
    # is_draft/is_verified pins exist for. Same casing/whitespace/None battery,
    # plus the two sibling magic values (each must read NOT-modified in both).
    cases = [
        {"Status": "Modified"},
        {"Status": "modified"},
        {"Status": "  MODIFIED  "},
        {"Status": "Verified"},
        {"Status": "Draft"},
        {"Status": "Planned"},
        {"Status": ""},
        {"Status": None},
        {},
    ]
    for row in cases:
        assert TRACE.is_modified(row) == GATE.is_modified(row), row
    # The three recognized values are mutually exclusive on any single row.
    for val in ("Modified", "Draft", "Verified"):
        row = {"Status": val}
        assert (
            sum(
                (
                    TRACE.is_draft(row),
                    TRACE.is_verified(row),
                    TRACE.is_modified(row),
                )
            )
            == 1
        ), row


def test_llr_exempt_agrees():
    # Both files decide the LLR-exemption at their own decision point (trace's
    # orphan rule, derive_gate's sr_gate). Review 017 caught them disagreeing on
    # a whitespace-padded valid method (derive_gate stripped, trace did not) —
    # the exact false-green/false-red divergence WI-099 promised away. Pin the
    # predicate equivalent, and pin the padded case to the fixed direction.
    cases = [
        {"Verification": "Analysis"},
        {"Verification": " Analysis "},
        {"Verification": "Inspection"},
        {"Verification": "Attest"},
        {"Verification": "analysis"},  # closed vocab stays case-sensitive
        {"Verification": "Test"},
        {"Verification": ""},
        {"Verification": None},
        {},
    ]
    for row in cases:
        assert TRACE.llr_exempt(row) == GATE.llr_exempt(row), row
    # the 017 case itself: whitespace-padded valid method IS exempt, in both
    assert TRACE.llr_exempt({"Verification": " Analysis "}) is True
    assert GATE.llr_exempt({"Verification": "Attest  "}) is True


def test_require_verified_bar_matches_sr_gate_regardless_of_method(scaffold):
    # WI-259 (repo-review-2026-07-21 M-5): trace's --require-verified G3 bar and
    # derive_gate.sr_gate must agree about which SRs must be Verified before G3.
    # sr_gate has always demanded is_verified for ANY decomposed SR with no
    # per-method carve-out; trace's bar used to fire only for Verification=Test, so
    # a decomposed Demonstration/Analysis/Inspection SR left Implemented could never
    # derive G3 yet passed trace's check — two scripts disagreeing about the gate.
    # Option A widened trace's bar: its loop now gates only on is_draft (skip) then
    # is_verified (pass) and NEVER reads Verification, so it is method-blind exactly
    # like sr_gate. Pin the equivalence on the predicates each side actually uses,
    # across the full Verification vocabulary, so neither re-grows a method filter.
    methods = [
        "Test",
        "Demonstration",
        "Manual",
        "Analysis",
        "Inspection",
        "Attest",
        "Critique",
    ]
    for m in methods:
        implemented = {"Verification": m, "Status": "Implemented"}
        verified = {"Verification": m, "Status": "Verified"}
        # trace's widened bar applies to every ratified (non-Draft) row — the skip
        # is is_draft, which is method-blind — and then passes iff is_verified. So
        # a ratified SR of ANY method flags exactly when it is not Verified.
        assert TRACE.is_draft(implemented) is False, m  # bar applies (ratified)
        assert TRACE.is_draft(verified) is False, m  # bar applies (ratified)
        assert TRACE.is_verified(verified) is True, m  # Verified -> passes
        assert TRACE.is_verified(implemented) is False, m  # not Verified -> flagged
        # sr_gate's G3 for a decomposed SR is the SAME is_verified predicate, also
        # method-blind: Verified reaches G3, Implemented caps at G2 — every method.
        assert GATE.sr_gate(verified, True, True) == GATE.G3, m
        assert GATE.sr_gate(implemented, True, True) == GATE.G2, m
    # A Draft SR is pre-ratification and exempt from BOTH: trace's bar stands down
    # (is_draft True, so the loop `continue`s) and sr_gate returns G0 (below G1).
    draft = {"Verification": "Test", "Status": "Draft"}
    assert TRACE.is_draft(draft) is True
    assert GATE.sr_gate(draft, True, True) == GATE.G0

    # The predicate pins above are necessary but not sufficient: because is_draft/
    # is_verified read Status (not Verification), restoring a Verification=="Test"
    # guard INSIDE analyze()'s --require-verified loop would leave them all green.
    # So drive the real loop end-to-end — a decomposed, non-Test (Demonstration) SR
    # left Implemented MUST produce a status finding. This is the assertion that
    # actually pins the loop side method-blind: restore the Test-only guard and it
    # fails (Demonstration skipped -> status-findings=0 -> exit 0).
    make_minimal_project(scaffold)
    csv_path = scaffold / "docs" / "requirements" / "system-requirements.csv"
    csv_path.write_text(
        csv_path.read_text(encoding="utf-8").replace(
            ",M,Test,Verified", ",M,Demonstration,Implemented"
        ),
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict", "--require-verified"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "status-findings=1" in proc.stdout
    assert "Verification=Demonstration but Status=Implemented" in proc.stdout


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
