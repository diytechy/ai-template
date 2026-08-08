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
def _independent_meta_expectations():
    """Per-phase gate expectations re-derived STRAIGHT from the registry CSVs
    with none of derive_gate's machinery — a deliberate second implementation,
    so the dogfood test can catch sr_gate breaking (the adversarial review's F3:
    compare-a-subprocess-to-the-same-function is tautological). Simplified on
    facts the meta's own harness enforces elsewhere (orphans=0 => every
    non-exempt SR is decomposed): a phase expects G0 if any of its SRs — OR
    any of its LLR/TC rows, the documented new-phase signal (derive_gate's
    "LLR/TC — Draft => G0"; first exercised by Phase 5's TC-133, a Draft TC
    under no Draft SR) — is Draft, else G2 if any SR is below Verified
    (Modified included), else G3."""
    import csv as _csv

    with (ROOT / "docs" / "requirements" / "system-requirements.csv").open(
        encoding="utf-8-sig", newline=""
    ) as fh:
        srs = [
            r
            for r in _csv.DictReader(fh)
            if (r.get("SR-ID") or "").startswith("SR-")
            and not r["SR-ID"].endswith("-000")
        ]
    phases = {}
    for r in srs:
        status = (r.get("Status") or "").strip().lower()
        phases.setdefault((r.get("Phase") or "").strip() or "(default)", []).append(
            status
        )
    draft_child_phases = set()
    for rel, idcol in (
        ("docs/requirements/low-level-requirements.csv", "LLR-ID"),
        ("docs/test/test-cases.csv", "TC-ID"),
    ):
        with (ROOT / rel).open(encoding="utf-8-sig", newline="") as fh:
            for r in _csv.DictReader(fh):
                rid = r.get(idcol) or ""
                if not rid or rid.endswith("-000"):
                    continue
                if (r.get("Status") or "").strip().lower() == "draft":
                    draft_child_phases.add(
                        (r.get("Phase") or "").strip() or "(default)"
                    )
    expect = {}
    for phase, statuses in phases.items():
        if any(s == "draft" for s in statuses) or phase in draft_child_phases:
            expect[phase] = "G0"
        elif any(s != "verified" for s in statuses):
            expect[phase] = "G2"
        else:
            expect[phase] = "G3"
    modified = sum(1 for sts in phases.values() for s in sts if s == "modified")
    return expect, modified


def test_meta_repo_phases_match_an_independent_derivation_and_cache_is_fresh():
    # The kit's north star, phase-aware since phase 2 opened (WI-116), re-scoped
    # by WI-316 and re-anchored by the adversarial review's F3: the per-phase
    # values are checked against an INDEPENDENT re-derivation from the raw CSVs
    # (not against compute() — that comparison could never fail), so a Modified
    # re-attest window legitimately reads G2 while a broken sr_gate rung (e.g.
    # Modified deriving G1) still reds the dogfood. Plus: the SR-level modified
    # count is a floor for the basis count, and the committed docs/gate cache
    # matches the recomputed state (--check green).
    expect, sr_modified = _independent_meta_expectations()
    result = _derive(ROOT)
    for phase, gate in expect.items():
        assert result["per_phase"].get(phase) == gate, (
            phase,
            gate,
            result["per_phase"],
        )
    assert result["modified"] >= sr_modified  # LLR/TC flags may add to the count
    proc = run_py([SCRIPTS / "derive_gate.py", "--print", "--root", ROOT], cwd=ROOT)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    for phase, gate in expect.items():
        assert "{}={}".format(phase, gate) in proc.stdout
    # The derived current phase, read from the same computation rather than
    # stamped: this pinned `phase=4` until the mechanized-loop sitting added a
    # Phase 5 batch, and a stamped number here only ever teaches a reader to
    # bump it. The property is that the printed basis agrees with `compute`.
    assert "phase={}".format(result["phase"]) in proc.stdout
    assert "modified={}".format(result["modified"]) in proc.stdout
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
    assert GATE.sn_gate("SN-009", {"SN-009"}, set()) == GATE.G0  # draft section
    # WI-401: a ratified SN must be cited by >=1 SR SN-Refs to contribute G3;
    # ratified-and-uncovered caps at G0 (an unanswered need has not earned G1).
    assert GATE.sn_gate("SN-001", {"SN-009"}, {"SN-001"}) == GATE.G3  # covered
    assert GATE.sn_gate("SN-001", {"SN-009"}, set()) == GATE.G0  # uncovered


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


def test_modified_sr_reads_g2_and_is_counted(scaffold):
    # WI-316: a Modified SR (post-attestation amendment, re-attest owed) pulls its
    # gate to G2 through the EXISTING decomposed-unverified rung — no rule of its
    # own — and the basis carries modified=N so the pending state never hides.
    # Children stay Verified: their status never independently gates (maturity),
    # so the pull is exactly one rung, not a G0 draft-drop.
    make_minimal_project(scaffold)
    # SR-001 keeps the minimal project's LLR/TC children (decomposed), so the
    # Modified status pulls exactly one rung — not the undecomposed G1.
    _write(scaffold, srs=_sr("SR-001", status="Modified"))
    result = _derive(scaffold)
    assert result["raw"] == GATE.G2
    assert result["gate"] == "G2"
    assert result["modified"] == 1
    assert result["drafts"] == 0
    # The emitted basis line surfaces the count between drafts and computed.
    assert "drafts=0 modified=1 uncovered=0 computed=G2" in GATE.basis_line(result)


def test_modified_children_are_counted_but_never_gate(scaffold):
    # A Modified LLR/TC joins the modified=N count (informational precision) but
    # caps nothing: maturity_gate stays Draft-only, so the SR's own status drives
    # the gate exactly as before — the anti-coupling rule the derived-gate model
    # dropped LLR/TC status for is untouched by WI-316.
    make_minimal_project(scaffold)
    _write(
        scaffold,
        srs=_sr("SR-001"),
        llrs='LLR-001,SR-001,Adder,src/demo,add,"d",(see TC),Modified\n',
        tcs='TC-001,SR-001;LLR-001,Unit,m,Smoke,"a=1","e",Yes,tests/test_demo.py::t,Modified\n',
    )
    result = _derive(scaffold)
    assert result["gate"] == "G3"  # SR Verified; children's status never caps
    assert result["modified"] == 2
    assert GATE.maturity_gate({"Status": "Modified"}) == GATE.G3


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
    # The double-counting seam (WI-401): SN-050 is cited by no SR, but a Draft
    # SN is EXEMPT from the coverage rung (as from trace's orphan rule) — the
    # one fact fires exactly one rung, the draft drop above.
    assert result["uncovered"] == 0


# --- WI-401: the SN-coverage rung ---------------------------------------------
def _append_ratified_sn(scaffold, row):
    """Append one table row to the fixture's ratified needs table (no draft
    heading above it, so the id is ratified by section-as-state)."""
    sn = scaffold / "docs" / "requirements" / "stakeholder-needs.md"
    sn.write_text(sn.read_text(encoding="utf-8") + row, encoding="utf-8")


def test_uncovered_ratified_sn_caps_the_gate(scaffold):
    # WI-401 (owner ruling 2026-08-01): a ratified SN cited by zero SR SN-Refs is
    # an unanswered need — G1 is not earned. The raw level caps at G0, the
    # runnable value floors to G1, and the basis carries uncovered=N so the cause
    # never hides (drafts=0 here: before this rung, computed=G0 implied a draft).
    make_minimal_project(scaffold)
    _append_ratified_sn(
        scaffold, "| SN-002 | Subtract two numbers. | Demo. | M | sub(3,2) is 1. |\n"
    )
    result = _derive(scaffold)
    assert result["raw"] == GATE.G0
    assert result["gate"] == "G1"
    assert result["drafts"] == 0
    assert result["uncovered"] == 1
    assert "uncovered=1 computed=G0" in GATE.basis_line(result)


def test_covering_the_sn_restores_the_prior_level(scaffold):
    # The counter-half: citing the need from an SR's SN-Refs releases the cap —
    # the same registry state otherwise reads G3 again, uncovered=0.
    make_minimal_project(scaffold)
    _append_ratified_sn(
        scaffold, "| SN-002 | Subtract two numbers. | Demo. | M | sub(3,2) is 1. |\n"
    )
    _write(scaffold, srs=_sr("SR-001", sn="SN-001;SN-002"))
    result = _derive(scaffold)
    assert result["raw"] == GATE.G3
    assert result["gate"] == "G3"
    assert result["uncovered"] == 0
    assert "uncovered=0 computed=G3" in GATE.basis_line(result)


def test_example_rows_are_ignored_by_the_coverage_rung(scaffold):
    # -000 rows on BOTH sides of the join are out of scope: an SN-000 placeholder
    # never fires the rung, and an example SR-000 row is filtered before the
    # coverage set is built, so its SN-Refs cannot fake coverage of a real need.
    make_minimal_project(scaffold)
    _append_ratified_sn(scaffold, "| SN-000 | Example placeholder. | M | n/a |\n")
    result = _derive(scaffold)
    assert result["uncovered"] == 0
    assert result["gate"] == "G3"
    # A real ratified need answered ONLY by an example SR row stays uncovered.
    _append_ratified_sn(scaffold, "| SN-002 | Real need. | M | tbd |\n")
    _write(scaffold, srs=_sr("SR-001") + _sr("SR-000", sn="SN-002"))
    result = _derive(scaffold)
    assert result["uncovered"] == 1
    assert result["raw"] == GATE.G0


def test_ex_draft_treats_the_coverage_rung_consistently(scaffold):
    # A ratified SN answered ONLY by a Draft SR. In the RAW view the citation
    # stands — trace.py's orphan rule reads the same cited set, so neither
    # surface calls the need uncovered (the Draft SR itself is what drops raw to
    # G0, one fact one finding). In the ex-draft counterfactual the SAME
    # arithmetic runs over the non-draft subset: the citation leaves with its
    # row, the need reads unanswered, and ex-draft stays G0 — removing a draft
    # answer must not fabricate coverage or a level the spine never earned.
    make_minimal_project(scaffold)
    _append_ratified_sn(
        scaffold, "| SN-002 | Subtract two numbers. | Demo. | M | sub(3,2) is 1. |\n"
    )
    _write(scaffold, srs=_sr("SR-001") + _sr("SR-002", status="Draft", sn="SN-002"))
    result = _derive(scaffold)
    assert result["raw"] == GATE.G0
    assert result["drafts"] == 1
    assert result["uncovered"] == 0  # the Draft SR's citation counts in the raw view
    assert result["ex_draft"] == GATE.G0  # ...but does not survive its row's removal


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


# --- WI-402: --next-phase, the derived next phase as an output mode -----------
def test_next_phase_prints_max_plus_one(scaffold):
    # --next-phase = max(phase over non-draft spine rows) + 1, printed bare so
    # the intake mint helper (WI-388) can shell out and int() the answer when a
    # confirmed scope change opens a new phase. A Draft row's phase is not yet
    # scope, so it never bumps the answer — same derivation as the basis line's
    # phase=N, exposed as an output mode.
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
    gate_file = scaffold / "docs" / "gate"
    before = gate_file.read_text(encoding="utf-8")
    proc = run_py(["scripts/derive_gate.py", "--next-phase"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stdout.strip() == "4"  # max ratified = 3; the Draft 4 is excluded
    # An output mode over the existing derivation: docs/gate is not rewritten.
    assert gate_file.read_text(encoding="utf-8") == before


def test_next_phase_on_an_unphased_spine(scaffold):
    # An unphased spine is the implicit foundation (phase 1) — what blank bought
    # before the phase model — so the first opened phase is 2, never 1, which
    # would collapse the new scope into the foundation the blank rows occupy.
    make_minimal_project(scaffold)
    proc = run_py(["scripts/derive_gate.py", "--next-phase"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stdout.strip() == "2"


def test_per_phase_resolves_tc_citing_only_its_llr(scaffold):
    # Repo-review 2026-07-21 M-6: a Draft TC citing only its LLR (a legal shape
    # the orphan rules accept) dropped the repo's raw min while the per-phase
    # view stayed green — the phase-drop detector then pointed at nothing. TC
    # refs now resolve through the LLR->SR map, so the phase bucket sees it.
    make_minimal_project(scaffold)
    _write(
        scaffold,
        srs=_sr("SR-001", status="Implemented"),
        llrs='LLR-001,SR-001,Adder,src/demo,add,"d",(see TC-001),Implemented\n',
        tcs='TC-001,LLR-001,Unit,m,Smoke,"a=1","e",Yes,tests,Draft\n',
    )
    result = _derive(scaffold)
    assert result["raw"] == GATE.G0
    assert result["per_phase"]["(default)"] == "G0"  # was G1/G2 before the fix


# --- ex-draft: the level the drafts are hiding (WI-341) -----------------------
def _mature_single_phase_reopened(scaffold):
    """A single-phase spine that reached G3, then had ONE Draft SR added.

    This is the shape 128-REVIEW-A (MAJOR 3) showed the old per-phase heuristic
    could not see: the Draft drops the only phase to G0, so the breakdown that
    was the evidence of maturity is erased by the very row it is meant to
    qualify.
    """
    make_minimal_project(scaffold)
    _write(
        scaffold,
        srs=_sr("SR-001") + _sr("SR-002", status="Draft"),
        llrs='LLR-001,SR-001,Adder,src/demo,add,"d",(see TC-001),Implemented\n',
        tcs='TC-001,SR-001;LLR-001,Unit,m,Smoke,"a=1","e",Yes,tests,Implemented\n',
    )
    return _derive(scaffold)


def test_ex_draft_reports_the_level_the_drafts_are_hiding(scaffold):
    result = _mature_single_phase_reopened(scaffold)
    # What the drafts produce...
    assert result["raw"] == GATE.G0
    assert result["per_phase"]["(default)"] == "G0"
    # ...and what the rows they did not touch still say. THIS is the evidence a
    # draft cannot erase, and it is why the field exists.
    assert result["ex_draft"] == GATE.G3
    assert "ex-draft=G3" in GATE.basis_line(result)


def test_ex_draft_stays_low_when_the_spine_never_climbed(scaffold):
    # The mirror case: drafts on a spine whose ratified rows are undecomposed.
    # Removing the drafts changes nothing, so there is no hidden maturity — the
    # early-project false positive stays fixed at the source, not by a heuristic.
    make_minimal_project(scaffold)
    _write(
        scaffold,
        srs=_sr("SR-001", status="Planned") + _sr("SR-002", status="Draft"),
        llrs=LLRS_H[:0],
        tcs=TCS_H[:0],
    )
    (scaffold / "docs" / "requirements" / "low-level-requirements.csv").write_text(
        LLRS_H, encoding="utf-8"
    )
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(TCS_H, encoding="utf-8")
    result = _derive(scaffold)
    assert result["raw"] == GATE.G0
    assert result["ex_draft"] == GATE.G1


def test_ex_draft_equals_computed_when_nothing_is_pending(scaffold):
    # No drafts -> the counterfactual IS the actual. A window test reading these
    # two can then never fire on a clean repo, whatever its level.
    make_minimal_project(scaffold)
    result = _derive(scaffold)
    assert result["drafts"] == 0
    assert result["ex_draft"] == result["raw"]
