"""The `--require-verified` bar against the stage derivation, driven end-to-end
on a bootstrapped scaffold.

Split out of `test_rule_sync.py` so the rest of that module, the identity and
value pins over the kit's one policy home, stays in the per-commit smoke tier.
This case takes the `scaffold` fixture (a real `bootstrap.py` subprocess) and
runs `trace.py` as a subprocess to prove the loop side is method-blind, so it is
registered in `tests/conftest.py`'s `SLOW_MODULES` and runs at slice/phase close
and in CI.
"""

from conftest import load_script, make_minimal_project, run_py

TRACE = load_script("trace")
GATE = load_script("spine_rules")


def test_require_verified_bar_matches_sr_gate_regardless_of_method(scaffold):
    # WI-259 (repo-review-2026-07-21 M-5): trace's --require-verified DevStg-Impl bar and
    # spine_rules.sr_bar must agree about which SRs must be Approved before DevStg-Impl.
    # sr_bar has always demanded is_approved for ANY decomposed SR with no
    # per-method carve-out; trace's bar used to fire only for Verification=Test, so
    # a decomposed Demonstration/Analysis/Inspection SR left Approved could never
    # derive DevStg-Impl yet passed trace's check — two scripts disagreeing about the gate.
    # Option A widened trace's bar: its loop now gates only on is_drafted (skip) then
    # is_approved (pass) and NEVER reads Verification, so it is method-blind exactly
    # like sr_bar. Pin the equivalence on the predicates each side actually uses,
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
    # Computed once from the first method, then every other method must match it:
    # the pin is SAMENESS across the vocabulary, so hard-coding the rung here
    # would make it a pin on the ladder instead.
    method_blind_rung = None
    for m in methods:
        # RE-POINTED AT D-9 STEP 5: the "approved but not approved" fixture was
        # `Planned`, which FOLDED into `Approved`. Under the narrowed enum the
        # only value that still means that is `Modified` — using `Approved` here
        # would have made both halves of the comparison the same row.
        implemented = {"Verification": m, "Status": "Modified"}
        verified = {"Verification": m, "Status": "Approved"}
        # trace's widened bar applies to every approved (non-Drafted) row — the skip
        # is is_drafted, which is method-blind — and then passes iff is_approved. So
        # an approved SR of ANY method flags exactly when it is not Approved.
        assert TRACE.is_drafted(implemented) is False, m  # bar applies (approved)
        assert TRACE.is_drafted(verified) is False, m  # bar applies (approved)
        assert TRACE.is_approved(verified) is True, m  # Approved -> passes
        assert TRACE.is_approved(implemented) is False, m  # not Approved -> flagged
        # RE-POINTED AT WI-498 slice 5: `sr_bar` is DELETED with the bar axis, so
        # the derivation side of this pin moves onto the rung fall-through that
        # replaced it. The claim is unchanged and is the half the OI-30 D2
        # ceiling never touched — a DECOMPOSED SR derives the same rung whatever
        # its Verification method says, so neither side can re-grow a method
        # filter. (An LLR is supplied for every method, so the LLR-exemption is
        # deliberately not what is being measured here; `test_llr_exempt_agrees`
        # owns that.)
        stage_v = GATE.spine_stage(
            [dict(verified, **{"SR-ID": "SR-001", "SN-Refs": "SN-001"})],
            [{"LLR-ID": "LLR-001", "SR-Refs": "SR-001", "Status": "Approved"}],
            [{"TC-ID": "TC-001", "Verifies": "SR-001", "Status": "Approved"}],
            {"SN-001"},
            set(),
        )
        if method_blind_rung is None:
            method_blind_rung = stage_v
        assert stage_v == method_blind_rung, m
    # A Drafted SR is pre-approval and exempt from trace's bar (is_drafted
    # True, so the loop `continue`s) while it HOLDS ITS RUNG OPEN on the
    # derivation side — the two are the same fact seen from each end, which is
    # what lets a draft live in the live spine and still show as work in
    # progress. `sr_bar` said this by returning the below-everything sentinel;
    # the fall-through says it by stopping at the requirements rung.
    draft = {"Verification": "Test", "Status": "Drafted"}
    assert TRACE.is_drafted(draft) is True
    assert (
        GATE.spine_stage(
            [dict(draft, **{"SR-ID": "SR-001", "SN-Refs": "SN-001"})],
            [{"LLR-ID": "LLR-001", "SR-Refs": "SR-001", "Status": "Approved"}],
            [{"TC-ID": "TC-001", "Verifies": "SR-001", "Status": "Approved"}],
            {"SN-001"},
            set(),
        )
        == GATE.STAGE_REQS
    )

    # The predicate pins above are necessary but not sufficient: because is_drafted/
    # is_approved read Status (not Verification), restoring a Verification=="Test"
    # guard INSIDE analyze()'s --require-verified loop would leave them all green.
    # So drive the real loop end-to-end — a decomposed, non-Test (Demonstration) SR
    # left below `Approved` MUST produce a status finding. This is the assertion that
    # actually pins the loop side method-blind: restore the Test-only guard and it
    # fails (Demonstration skipped -> status-findings=0 -> exit 0).
    make_minimal_project(scaffold)
    csv_path = scaffold / "docs" / "requirements" / "system-requirements.csv"
    csv_path.write_text(
        csv_path.read_text(encoding="utf-8").replace(
            ",M,Test,Approved", ",M,Demonstration,Modified"
        ),
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict", "--require-verified"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "status-findings=1" in proc.stdout
    assert "Verification=Demonstration but Status=Modified" in proc.stdout
