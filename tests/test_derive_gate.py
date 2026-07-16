"""derive_gate.py: the gate computed from artifact states (the derived-gate model).

The derivation is the trust root of the whole model, so every per-artifact rule,
the min-aggregation, the draft drop, and the --check rot guard get a red->green
test here. The meta-repo smoke test proves the dogfood: the derived gate reads G3,
byte-for-byte with today's declared docs/gate (docs/specs/derived-gate-model.md
§11 done-when).
"""

from conftest import ROOT, SCRIPTS, load_script, make_minimal_project, run_py

GATE = load_script("derive_gate")

# Registry helpers -------------------------------------------------------------
SRS_H = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,"
    "Priority,Verification,Status\n"
)
LLRS_H = "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status\n"
TCS_H = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
)


def _sr(sid, verification="Test", status="Verified", sn="SN-001"):
    return '{},T,{},"r","why","ac",,M,{},{}\n'.format(sid, sn, verification, status)


def _write(scaffold, srs="", llrs="", tcs=""):
    req = scaffold / "docs" / "requirements"
    if srs:
        (req / "system-requirements.csv").write_text(SRS_H + srs, encoding="utf-8")
    if llrs:
        (req / "low-level-requirements.csv").write_text(LLRS_H + llrs, encoding="utf-8")
    if tcs:
        (scaffold / "docs" / "test" / "test-cases.csv").write_text(
            TCS_H + tcs, encoding="utf-8"
        )


def _derive(scaffold):
    return GATE.compute(scaffold / "docs")


# --- the meta-repo dogfood ----------------------------------------------------
def test_meta_repo_default_phase_holds_g3_and_cache_is_fresh():
    # The kit's north star, phase-aware since phase 2 opened (WI-116): the
    # meta's verified spine — foundation phase 1 — holds G3 regardless of what
    # pre-dev drafts a later phase carries, and the committed docs/gate cache
    # matches the recomputed state (--check green). Run against the real meta root.
    # The back-filled spine is fully phased (1..4), so the derived current phase = 4.
    proc = run_py([SCRIPTS / "derive_gate.py", "--print", "--root", ROOT], cwd=ROOT)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "1=G3" in proc.stdout
    assert "phase=4" in proc.stdout
    check = run_py([SCRIPTS / "derive_gate.py", "--check", "--root", ROOT], cwd=ROOT)
    assert check.returncode == 0, check.stdout + check.stderr


# --- per-artifact gate rules --------------------------------------------------
def test_sr_gate_rules():
    draft = {"Status": "Draft", "Verification": "Test"}
    assert GATE.sr_gate(draft, True, True) == GATE.G0
    planned = {"Status": "Planned", "Verification": "Test"}
    assert GATE.sr_gate(planned, False, False) == GATE.G1  # ratified, undecomposed
    assert GATE.sr_gate(planned, True, True) == GATE.G2  # decomposed, not verified
    verified = {"Status": "Verified", "Verification": "Test"}
    assert GATE.sr_gate(verified, True, True) == GATE.G3
    # An LLR-exempt method needs only a TC to be decomposed (no LLR).
    attest = {"Status": "Verified", "Verification": "Attest"}
    assert GATE.sr_gate(attest, False, True) == GATE.G3
    assert GATE.sr_gate(attest, False, False) == GATE.G1  # still needs its TC


def test_maturity_and_sn_gate_rules():
    # A present LLR/TC caps only when Draft; its own Status does not gate G3 (the
    # SR's Verified status does), so Implemented and Verified both contribute G3.
    assert GATE.maturity_gate({"Status": "Draft"}) == GATE.G0
    assert GATE.maturity_gate({"Status": "Implemented"}) == GATE.G3
    assert GATE.maturity_gate({"Status": "Verified"}) == GATE.G3
    assert GATE.sn_gate("SN-009", {"SN-009"}) == GATE.G0  # draft section
    assert GATE.sn_gate("SN-001", {"SN-009"}) == GATE.G3  # ratified: never caps


# --- aggregation over a real scaffold -----------------------------------------
def test_minimal_project_derives_g3(scaffold):
    make_minimal_project(scaffold)
    assert _derive(scaffold)["gate"] == "G3"


def test_draft_sr_drops_the_gate(scaffold):
    # A Draft SR sits at G0, dropping the min; the runnable value floors to G1 and
    # the raw G0 is recorded in the basis (the new-phase-pending signal).
    make_minimal_project(scaffold)
    _write(
        scaffold,
        srs=_sr("SR-001") + _sr("SR-002", status="Draft"),
    )
    result = _derive(scaffold)
    assert result["raw"] == GATE.G0
    assert result["gate"] == "G1"
    assert result["drafts"] == 1


def test_undecomposed_sr_is_g1(scaffold):
    # A ratified (Planned) SR with no LLR/TC is at G1 (requirement not decomposed).
    make_minimal_project(scaffold)
    _write(scaffold, srs=_sr("SR-001", status="Planned"))
    # Empty (header-only) LLR/TC registries: SR-001 has no decomposition.
    (scaffold / "docs" / "requirements" / "low-level-requirements.csv").write_text(
        LLRS_H, encoding="utf-8"
    )
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(TCS_H, encoding="utf-8")
    assert _derive(scaffold)["gate"] == "G1"


def test_decomposed_unverified_is_g2(scaffold):
    # SR + LLR + TC all present but not Verified -> G2 (decomposed, not verified).
    make_minimal_project(scaffold)
    _write(
        scaffold,
        srs=_sr("SR-001", status="Implemented"),
        llrs='LLR-001,SR-001,Adder,src/demo,add,"d",(see TC),Implemented\n',
        tcs='TC-001,SR-001;LLR-001,Unit,m,Smoke,"a=1","e",Yes,tests/test_demo.py::t,Implemented\n',
    )
    assert _derive(scaffold)["gate"] == "G2"


def test_no_real_srs_is_g1(scaffold):
    # A fresh scaffold (only -000 placeholders) is at G1, never a vacuous G3.
    assert _derive(scaffold)["gate"] == "G1"


# --- the cache + --check rot guard --------------------------------------------
def test_write_then_check_roundtrips(scaffold):
    make_minimal_project(scaffold)
    write = run_py(["scripts/derive_gate.py"], cwd=scaffold)
    assert write.returncode == 0, write.stdout + write.stderr
    gate_text = (scaffold / "docs" / "gate").read_text(encoding="utf-8")
    assert "# basis:" in gate_text
    assert gate_text.strip().splitlines()[-1] == "G3"  # the runnable value last
    # A fresh compute matches the cache.
    check = run_py(["scripts/derive_gate.py", "--check"], cwd=scaffold)
    assert check.returncode == 0, check.stdout + check.stderr
    assert "up to date" in check.stdout


def test_check_detects_state_drift(scaffold):
    make_minimal_project(scaffold)
    run_py(["scripts/derive_gate.py"], cwd=scaffold)
    # Un-verify an SR: the derived gate drops but the cache still says G3 -> STALE.
    srs = scaffold / "docs" / "requirements" / "system-requirements.csv"
    srs.write_text(
        srs.read_text(encoding="utf-8").replace(",Test,Verified", ",Test,Implemented"),
        encoding="utf-8",
    )
    check = run_py(["scripts/derive_gate.py", "--check"], cwd=scaffold)
    assert check.returncode == 1
    assert "STALE" in check.stdout + check.stderr


def test_check_legacy_gate_compares_value_only(scaffold):
    # A hand-set docs/gate with no basis line (pre-migration) passes --check when
    # its VALUE matches the derived one (the smooth-transition path), and fails
    # when it does not.
    make_minimal_project(scaffold)
    gate = scaffold / "docs" / "gate"
    gate.write_text("# legacy hand-set\nG3\n", encoding="utf-8")
    ok = run_py(["scripts/derive_gate.py", "--check"], cwd=scaffold)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert "not yet in derived form" in ok.stdout + ok.stderr
    gate.write_text("# legacy hand-set\nG2\n", encoding="utf-8")
    bad = run_py(["scripts/derive_gate.py", "--check"], cwd=scaffold)
    assert bad.returncode == 1
    assert "STALE" in bad.stdout + bad.stderr


def test_requirement_first_lifecycle_end_to_end(scaffold):
    # The full derived-gate lifecycle on a fixture (spec §11 done-when): draft a
    # requirement in the LIVE spine (the gate drops), then ratify -> decompose ->
    # verify (the gate climbs back), with trace.py clean throughout.
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    srs = req / "system-requirements.csv"
    llrs = req / "low-level-requirements.csv"
    tcs = scaffold / "docs" / "test" / "test-cases.csv"

    # 1) Requirement-first: a Draft SR-002 with no LLR/TC. trace stays clean (the
    #    draft is exempt), and the derived gate drops to G1 (raw G0 in the basis).
    srs.write_text(
        SRS_H + _sr("SR-001") + _sr("SR-002", status="Draft"), encoding="utf-8"
    )
    trace = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert trace.returncode == 0, trace.stdout + trace.stderr
    r = _derive(scaffold)
    assert r["raw"] == GATE.G0 and r["gate"] == "G1"

    # 2) Ratify + decompose: Draft->Planned, add LLR-002 + TC-002 (not Verified).
    #    The derived gate rises to G2.
    srs.write_text(
        SRS_H + _sr("SR-001") + _sr("SR-002", status="Planned"), encoding="utf-8"
    )
    llrs.write_text(
        LLRS_H
        + 'LLR-001,SR-001,Adder,src/demo,add,"d",(see TC),Verified\n'
        + 'LLR-002,SR-002,Part,src/demo,two,"d",(see TC),Implemented\n',
        encoding="utf-8",
    )
    tcs.write_text(
        TCS_H
        + 'TC-001,SR-001;LLR-001,Unit,m,Smoke,"a=1","e",Yes,tests/test_demo.py::t,Verified\n'
        + 'TC-002,SR-002;LLR-002,Unit,m,Full,,"e",Yes,tests/test_demo.py::t2,Implemented\n',
        encoding="utf-8",
    )
    assert _derive(scaffold)["gate"] == "G2"

    # 3) Verify: SR-002 + its TC reach Verified. The derived gate returns to G3.
    srs.write_text(
        SRS_H + _sr("SR-001") + _sr("SR-002", status="Verified"), encoding="utf-8"
    )
    tcs.write_text(
        TCS_H
        + 'TC-001,SR-001;LLR-001,Unit,m,Smoke,"a=1","e",Yes,tests/test_demo.py::t,Verified\n'
        + 'TC-002,SR-002;LLR-002,Unit,m,Full,,"e",Yes,tests/test_demo.py::t2,Verified\n',
        encoding="utf-8",
    )
    assert _derive(scaffold)["gate"] == "G3"


def test_draft_sn_drops_the_gate(scaffold):
    # A Draft SN (section-as-state) sits at G0 and drops the derived gate too.
    make_minimal_project(scaffold)
    sn = scaffold / "docs" / "requirements" / "stakeholder-needs.md"
    sn.write_text(
        sn.read_text(encoding="utf-8") + "\n## Draft needs (unratified)\n\n"
        "| SN-ID | Need | Priority | Acceptance |\n|---|---|---|---|\n"
        "| SN-050 | drafted | S | tbd |\n",
        encoding="utf-8",
    )
    result = _derive(scaffold)
    assert result["raw"] == GATE.G0
    assert result["drafts"] == 1


# --- WI-188: the derived current phase ----------------------------------------
def test_phase_num_digit_parses():
    # The one phase-parse the kit shares: bare integers and vN both digit-parse.
    assert GATE.phase_num({"Phase": "v2"}) == 2
    assert GATE.phase_num({"Phase": "3"}) == 3
    assert GATE.phase_num({"Phase": ""}) is None
    assert GATE.phase_num({"Phase": "later"}) is None
    assert GATE.phase_num({}) is None


def test_derived_current_phase(scaffold):
    # The derived current phase = the highest phase over RATIFIED rows; a Draft in a
    # not-yet-ratified higher phase does not bump it (the phase analogue of the gate).
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "system-requirements.csv").write_text(
        SRS_H.rstrip("\n")
        + ",Phase\n"
        + _sr("SR-001").rstrip("\n")
        + ",1\n"
        + _sr("SR-002").rstrip("\n")
        + ",3\n"
        + _sr("SR-003", status="Draft").rstrip("\n")
        + ",4\n",
        encoding="utf-8",
    )
    assert _derive(scaffold)["phase"] == 3  # SR-003's phase 4 is Draft, so excluded


def test_derived_phase_none_when_unphased(scaffold):
    # An unphased spine (no Phase column) reads phase=(none) — a non-adopter is
    # unaffected, exactly like the all-blank --strict-schema case.
    make_minimal_project(scaffold)
    assert _derive(scaffold)["phase"] is None
