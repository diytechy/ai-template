"""derive_gate.py: the gate computed from artifact states (the derived-gate model).

The derivation is the trust root of the whole model, so every per-artifact rule,
the min-aggregation, the draft drop, and the --check rot guard get a red->green
test here. The meta-repo smoke test proves the dogfood: the derived gate reads DevStg-Impl,
byte-for-byte with today's declared docs/gate (docs/archive/specs/derived-gate-model.2026-07-20.md
§11 done-when).
"""

from conftest import (
    ROOT,
    SCRIPTS,
    load_script,
    make_minimal_project,
    run_py,
    record_ids,
)

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


def _sr(sid, verification="Test", status="Approved", sn="SN-001"):
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
    so the dogfood test can catch sr_bar breaking (the adversarial review's F3:
    compare-a-subprocess-to-the-same-function is tautological). A phase expects
    DevStg-Below if any of its SRs — OR any of its LLR/TC rows, the documented
    new-phase signal (derive_gate's "LLR/TC — Drafted => DevStg-Below"; first
    exercised by Phase 5's TC-133, a Drafted TC under no Drafted SR) — is
    Drafted; else DevStg-Reqs if any SR is UNDECOMPOSED (no LLR cites it and no
    TC verifies it — real since the 2026-08-20 signing approved nine SRs ahead
    of their chains, the declared orphans debt; the old "orphans=0 => every
    non-exempt SR is decomposed" simplification died with it); else
    DevStg-Tests."""
    # Read with STDLIB `tomllib` straight off the file, not through
    # spine_carrier: the independence this re-derivation buys is the point (F3),
    # and it now covers the carrier as well as the gate arithmetic — if the
    # kit's own loader ever mis-read a Status or a Phase, a `want` side built on
    # it would agree with the bug.
    import tomllib as _toml

    def _rows(rel, table, prefix):
        text = (ROOT / rel).read_text(encoding="utf-8-sig")
        rows = _toml.loads(text).get(table, {})
        return [
            dict(cells, _id=rid)
            for rid, cells in rows.items()
            if rid.startswith(prefix) and not rid.endswith("-000")
        ]

    def _phase(row):
        # `Phase` is a real int under this carrier; the gate groups by its text.
        value = row.get("phase", "")
        return str(value).strip() or "(default)"

    srs = _rows("docs/requirements/system-requirements.toml", "requirement", "SR-")
    assert srs, "no SR rows read — the re-derivation would be vacuous"
    phases = {}
    for r in srs:
        status = str(r.get("status") or "").strip().lower()
        phases.setdefault(_phase(r), []).append(status)
    draft_child_phases = set()
    cited_srs = set()
    import re as _re

    for rel, table, prefix in (
        ("docs/requirements/low-level-requirements.toml", "design", "LLR-"),
        ("docs/test/test-cases.toml", "test", "TC-"),
    ):
        for r in _rows(rel, table, prefix):
            if str(r.get("status") or "").strip().lower() == "drafted":
                draft_child_phases.add(_phase(r))
            for key in ("sr_refs", "verifies"):
                cited_srs.update(_re.findall(r"SR-\d+", str(r.get(key, ""))))
    undecomposed_phases = {_phase(r) for r in srs if r["_id"] not in cited_srs}
    expect = {}
    for phase, statuses in phases.items():
        if any(s == "drafted" for s in statuses) or phase in draft_child_phases:
            expect[phase] = "DevStg-Below"
        elif phase in undecomposed_phases:
            # An Approved SR no LLR cites and no TC verifies is undecomposed:
            # sr_bar holds its phase at the Reqs bar until the chain exists.
            expect[phase] = "DevStg-Reqs"
        elif any(s != "approved" for s in statuses):
            expect[phase] = "DevStg-Tests"
        else:
            # OI-30 D2's ceiling, mirrored in the INDEPENDENT re-derivation
            # so this side is not simply agreeing with the code it checks.
            expect[phase] = "DevStg-Tests"
    return expect


def test_meta_repo_phases_match_an_independent_derivation_and_cache_is_fresh():
    # The kit's north star, phase-aware since phase 2 opened (WI-116), re-scoped
    # by WI-316 and re-anchored by the adversarial review's F3: the per-phase
    # values are checked against an INDEPENDENT re-derivation from the raw CSVs
    # (not against compute() — that comparison could never fail), so a Modified
    # re-attest window legitimately reads DevStg-Tests while a broken sr_bar rung (e.g.
    # Modified deriving DevStg-Reqs) still reds the dogfood. Plus: the SR-level modified
    # count is a floor for the basis count, and the committed docs/gate cache
    # matches the recomputed state (--check green).
    expect = _independent_meta_expectations()
    result = _derive(ROOT)
    for phase, gate in expect.items():
        assert result["per_phase"].get(phase) == gate, (
            phase,
            gate,
            result["per_phase"],
        )
    proc = run_py([SCRIPTS / "derive_gate.py", "--print", "--root", ROOT], cwd=ROOT)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    for phase, gate in expect.items():
        assert "{}={}".format(phase, gate) in proc.stdout
    # A deliberate SNAPSHOT of the meta-repo's own derived phase, so a silent
    # phase drift reds here rather than passing unnoticed. Bump it when a
    # ratification legitimately advances the phase (4 -> 5 at the 2026-08-13
    # re-attest sitting, which ratified the last draft SNs and SR-137..149).
    assert "phase=5" in proc.stdout
    # ...and the RETIRED field is absent from the emitted line. `modified=`
    # left with `is_modified` at D-9 step 7 (a count of a value the closed
    # enum no longer admits is a count of an integrity error, not of a
    # pending state); `check._BASIS_RE` keeps honouring it when a file
    # carries one, which the round-trip pin below drives from both sides.
    assert "modified=" not in proc.stdout
    check = run_py([SCRIPTS / "derive_gate.py", "--check", "--root", ROOT], cwd=ROOT)
    assert check.returncode == 0, check.stdout + check.stderr


# --- per-artifact gate rules --------------------------------------------------
def test_sr_gate_rules():
    draft = {"Status": "Drafted", "Verification": "Test"}
    assert GATE.sr_bar(draft, True, True) == GATE.BAR_BELOW
    # RE-POINTED AGAIN AT D-9 STEPS 7/8. It read `Planned` (folded into
    # `Approved` at OI-30 D1), then `Modified` (retired at step 7). `sr_bar`
    # never read either word — it reads `is_drafted` and then DECOMPOSITION —
    # so the honest fixture for "ratified, undecomposed" is any non-Drafted
    # value, and `Founded` is the one this step added.
    founded = {"Status": "Founded", "Verification": "Test"}
    assert GATE.sr_bar(founded, False, False) == GATE.BAR_REQS  # ratified, undecomposed
    assert (
        GATE.sr_bar(founded, True, True) == GATE.BAR_TESTS
    )  # decomposed — the OI-30 D2 ceiling, whatever the cell says
    # OI-30 D2's ceiling: decomposed tops out at DevStg-Tests, whatever the cell
    # says. The dedicated pin is
    # `test_sr_bar_CEILINGS_at_DevStg_Tests_and_impl_is_unreachable_by_cell`.
    approved = {"Status": "Approved", "Verification": "Test"}
    assert GATE.sr_bar(approved, True, True) == GATE.BAR_TESTS
    # An LLR-exempt method needs only a TC to be decomposed (no LLR).
    attest = {"Status": "Approved", "Verification": "Attest"}
    assert GATE.sr_bar(attest, False, True) == GATE.BAR_TESTS
    assert GATE.sr_bar(attest, False, False) == GATE.BAR_REQS  # still needs its TC


def test_maturity_and_sn_gate_rules():
    # A present LLR/TC caps only when Drafted; its own Status does not gate (the
    # SR's does), so `Approved` and `Founded` both contribute DevStg-Impl —
    # and so does an UNRECOGNIZED value, which is `SPINE_MATURITY`'s deliberate
    # spine-only default (the closed enum names it on the integrity floor
    # instead; see maturity_bar). The RETIRED `Modified` is driven here too,
    # and it lands on the unrecognized arm — which is the safe direction: the
    # word retiring must not LOWER a downstream repo's derived gate, it must
    # surface as an integrity finding on the cell.
    assert GATE.maturity_bar({"Status": "Drafted"}) == GATE.BAR_BELOW
    assert GATE.maturity_bar({"Status": "Approved"}) == GATE.BAR_RELEASE
    assert GATE.maturity_bar({"Status": "Founded"}) == GATE.BAR_RELEASE
    assert GATE.maturity_bar({"Status": "Modified"}) == GATE.BAR_RELEASE
    assert GATE.maturity_bar({"Status": "Implemented"}) == GATE.BAR_RELEASE
    assert GATE.sn_bar("SN-009", {"SN-009"}, set()) == GATE.BAR_BELOW  # draft section
    # WI-401: a ratified SN must be cited by >=1 SR SN-Refs to contribute DevStg-Impl;
    # ratified-and-uncovered caps at DevStg-Below (an unanswered need has not earned DevStg-Reqs).
    assert GATE.sn_bar("SN-001", {"SN-009"}, {"SN-001"}) == GATE.BAR_RELEASE  # covered
    assert GATE.sn_bar("SN-001", {"SN-009"}, set()) == GATE.BAR_BELOW  # uncovered


# --- aggregation over a real scaffold -----------------------------------------
def test_minimal_project_derives_the_ceilinged_top(scaffold):
    # WAS DevStg-Impl. Under the OI-30 D2 ceiling a fully decomposed, fully
    # approved spine reads DevStg-Tests: the release bar is the harness's answer,
    # not a Status cell's.
    make_minimal_project(scaffold)
    assert _derive(scaffold)["gate"] == "DevStg-Tests"


def test_draft_sr_drops_the_gate(scaffold):
    # A Drafted SR sits at DevStg-Below, dropping the min; the runnable value floors to DevStg-Reqs and
    # the raw DevStg-Below is recorded in the basis (the new-phase-pending signal).
    make_minimal_project(scaffold)
    _write(
        scaffold,
        srs=_sr("SR-001") + _sr("SR-002", status="Drafted"),
    )
    result = _derive(scaffold)
    assert result["raw"] == GATE.BAR_BELOW
    assert result["gate"] == "DevStg-Reqs"
    assert result["drafted"] == 1


def test_undecomposed_sr_is_g1(scaffold):
    # A ratified (Approved) SR with no LLR/TC is at DevStg-Reqs (requirement not decomposed).
    make_minimal_project(scaffold)
    _write(scaffold, srs=_sr("SR-001", status="Approved"))
    # Empty (header-only) LLR/TC registries: SR-001 has no decomposition.
    (scaffold / "docs" / "requirements" / "low-level-requirements.csv").write_text(
        LLRS_H, encoding="utf-8"
    )
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(TCS_H, encoding="utf-8")
    assert _derive(scaffold)["gate"] == "DevStg-Reqs"


def test_decomposed_unverified_is_g2(scaffold):
    # SR + LLR + TC all present but the SR not Approved -> DevStg-Tests
    # (decomposed, re-attest owed). RE-POINTED AT D-9 STEP 5: the fixture was
    # `Planned`, which folded into `Approved`; `Modified` is the one remaining
    # ratified-but-unblessed value.
    make_minimal_project(scaffold)
    _write(
        scaffold,
        srs=_sr("SR-001", status="Modified"),
        llrs='LLR-001,SR-001,Adder,src/demo,add,"d",(see TC),Approved\n',
        tcs='TC-001,SR-001;LLR-001,Unit,m,Smoke,"a=1","e",Yes,tests/test_demo.py::t,Approved\n',
    )
    assert _derive(scaffold)["gate"] == "DevStg-Tests"


def test_no_real_srs_is_g1(scaffold):
    # A fresh scaffold (only -000 placeholders) is at DevStg-Reqs, never a vacuous DevStg-Impl.
    assert _derive(scaffold)["gate"] == "DevStg-Reqs"


def test_the_modified_basis_counter_RETIRED_with_its_predicate(scaffold):
    """D-9 STEP 7, and this replaces two tests rather than dropping them.

    They pinned `modified=N`: that a `Modified` SR pulled its phase to
    DevStg-Tests through the existing decomposed-unapproved rung (no rule of
    its own), and that a `Modified` LLR/TC joined the count while capping
    nothing. `Modified` retired at step 7, so neither state is reachable in a
    conformant repo and neither assertion can be made about one.

    What survives is the property that mattered, restated on the live
    vocabulary and made STRONGER: the counter is GONE from the result dict and
    from the emitted line, so nothing can quietly report zero pending rows
    from a field that can only ever be zero. The rung it exercised is pinned
    where it belongs, on `sr_bar` (an approved-and-decomposed SR reads
    DevStg-Tests) and on `maturity_bar` (a child's status never caps past
    Drafted) — both directly asserted below on values that still exist.
    """
    make_minimal_project(scaffold)
    _write(scaffold, srs=_sr("SR-001"))
    result = _derive(scaffold)
    assert result["raw"] == GATE.BAR_TESTS
    assert result["gate"] == "DevStg-Tests"
    assert result["drafted"] == 0
    assert "modified" not in result
    line = GATE.basis_line(result)
    assert "modified=" not in line
    assert "drafted=0 uncovered=0 computed=DevStg-Tests" in line
    # The child-never-caps rule, on the values the enum still has — including
    # `Founded`, armed for the spine at step 8 and mapping ABOVE Approved.
    assert GATE.maturity_bar({"Status": "Approved"}) == GATE.BAR_RELEASE
    assert GATE.maturity_bar({"Status": "Founded"}) == GATE.BAR_RELEASE
    assert GATE.maturity_bar({"Status": "Drafted"}) == GATE.BAR_BELOW


# --- the cache + --check rot guard --------------------------------------------
def test_write_then_check_roundtrips(scaffold):
    make_minimal_project(scaffold)
    write = run_py(["scripts/derive_gate.py"], cwd=scaffold)
    assert write.returncode == 0, write.stdout + write.stderr
    gate_text = (scaffold / "docs" / "gate").read_text(encoding="utf-8")
    assert "# basis:" in gate_text
    assert (
        gate_text.strip().splitlines()[-1] == "DevStg-Tests"  # OI-30 D2 ceiling
    )  # the runnable value last
    # A fresh compute matches the cache.
    check = run_py(["scripts/derive_gate.py", "--check"], cwd=scaffold)
    assert check.returncode == 0, check.stdout + check.stderr
    assert "up to date" in check.stdout


def test_check_detects_state_drift(scaffold):
    make_minimal_project(scaffold)
    run_py(["scripts/derive_gate.py"], cwd=scaffold)
    # Un-bless an SR: the derived gate drops but the cache still says
    # DevStg-Impl -> STALE. `Drafted` since D-9 step 7 — it was `Modified`,
    # which is no longer in the closed enum, so a fixture using it would be
    # driving the derivation with a value the integrity floor refuses.
    srs = scaffold / "docs" / "requirements" / "system-requirements.csv"
    srs.write_text(
        srs.read_text(encoding="utf-8").replace(",Test,Approved", ",Test,Drafted"),
        encoding="utf-8",
    )
    check = run_py(["scripts/derive_gate.py", "--check"], cwd=scaffold)
    assert check.returncode == 1
    assert "STALE" in check.stdout + check.stderr


def test_check_legacy_gate_compares_value_only(scaffold):
    # A hand-set docs/gate with no basis line (pre-migration) passes --check when
    # its VALUE matches the derived one (the smooth-transition path), and fails
    # when it does not. Stated in the CURRENT vocabulary — see the test below for
    # what a cache still carrying the retired one does.
    make_minimal_project(scaffold)
    gate = scaffold / "docs" / "gate"
    gate.write_text("# legacy hand-set\nDevStg-Tests\n", encoding="utf-8")
    ok = run_py(["scripts/derive_gate.py", "--check"], cwd=scaffold)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert "not yet in derived form" in ok.stdout + ok.stderr
    # The mismatching half: a value the derivation does NOT produce. It reads
    # DevStg-Impl deliberately — under the OI-30 D2 ceiling that is exactly a
    # value no cell can derive, which is the cleanest possible mismatch.
    gate.write_text("# legacy hand-set\nDevStg-Impl\n", encoding="utf-8")
    bad = run_py(["scripts/derive_gate.py", "--check"], cwd=scaffold)
    assert bad.returncode == 1
    assert "STALE" in bad.stdout + bad.stderr


def test_a_cache_carrying_the_RETIRED_vocabulary_reports_STALE(scaffold):
    """THE MIGRATION, PINNED (OI-21 contract break 5): field-compatible, not
    value-compatible — one forced regenerate, NO COMPAT SHIM.

    A `docs/gate` written before the conversion carries the retired tags on its
    value line and in its basis (`G3`; `computed=G0 ... stage=4`)  (check_vocab: allow)
    — spelled out here because the fixture below writes them.
    `--check` must call that STALE on the
    first recompute rather than silently accepting both vocabularies, because a
    reader that accepted both is precisely how the retired tags would grow back —
    and because the stale `stage=4` means something DIFFERENT under the eight-rung
    ladder than it did under the six-integer one.

    The failure direction is safe: a stale cache makes `spine_stage_of` read None,
    which `human_holds` treats as human-held. The one state this can produce is
    MORE human involvement, never less."""
    make_minimal_project(scaffold)
    gate = scaffold / "docs" / "gate"
    gate.write_text("# legacy hand-set\nG3\n", encoding="utf-8")
    stale = run_py(["scripts/derive_gate.py", "--check"], cwd=scaffold)
    assert stale.returncode == 1
    out = stale.stdout + stale.stderr
    assert "STALE" in out and "DevStg-Tests" in out
    # ...and ONE regenerate fixes it, which is the whole migration for an adopter.
    assert run_py(["scripts/derive_gate.py"], cwd=scaffold).returncode == 0
    assert run_py(["scripts/derive_gate.py", "--check"], cwd=scaffold).returncode == 0
    text = gate.read_text(encoding="utf-8")
    assert "stage=DevStg-" in text and "stage-ord=" in text and "stage-of=8" in text


def test_requirement_first_lifecycle_end_to_end(scaffold):
    # The full derived-gate lifecycle on a fixture (spec §11 done-when): draft a
    # requirement in the LIVE spine (the gate drops), then ratify -> decompose ->
    # verify (the gate climbs back), with trace.py clean throughout.
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    srs = req / "system-requirements.csv"
    llrs = req / "low-level-requirements.csv"
    tcs = scaffold / "docs" / "test" / "test-cases.csv"

    # 1) Requirement-first: a Drafted SR-002 with no LLR/TC. trace stays clean (the
    #    draft is exempt), and the derived gate drops to DevStg-Reqs (raw DevStg-Below in the basis).
    srs.write_text(
        SRS_H + _sr("SR-001") + _sr("SR-002", status="Drafted"), encoding="utf-8"
    )
    record_ids(scaffold)
    trace = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert trace.returncode == 0, trace.stdout + trace.stderr
    r = _derive(scaffold)
    assert r["raw"] == GATE.BAR_BELOW and r["gate"] == "DevStg-Reqs"

    # 2) Decompose while the SR still owes a human act: add LLR-002 + TC-002.
    #    The derived gate rises to DevStg-Tests. RE-POINTED AT D-9 STEP 5 — this
    #    rung's fixture was `Planned` (ratified text, evidence pending), which
    #    folded into `Approved`; `Modified` is what still reads below approval.
    srs.write_text(
        SRS_H + _sr("SR-001") + _sr("SR-002", status="Modified"), encoding="utf-8"
    )
    llrs.write_text(
        LLRS_H
        + 'LLR-001,SR-001,Adder,src/demo,add,"d",(see TC),Approved\n'
        + 'LLR-002,SR-002,Part,src/demo,two,"d",(see TC),Approved\n',
        encoding="utf-8",
    )
    tcs.write_text(
        TCS_H
        + 'TC-001,SR-001;LLR-001,Unit,m,Smoke,"a=1","e",Yes,tests/test_demo.py::t,Approved\n'
        + 'TC-002,SR-002;LLR-002,Unit,m,Full,,"e",Yes,tests/test_demo.py::t2,Approved\n',
        encoding="utf-8",
    )
    assert _derive(scaffold)["gate"] == "DevStg-Tests"

    # 3) Approve: SR-002 + its TC reach `Approved`. The derived gate returns to
    #    its ceiling, DevStg-Tests (OI-30 D2) — never to DevStg-Impl by cell.
    srs.write_text(
        SRS_H + _sr("SR-001") + _sr("SR-002", status="Approved"), encoding="utf-8"
    )
    tcs.write_text(
        TCS_H
        + 'TC-001,SR-001;LLR-001,Unit,m,Smoke,"a=1","e",Yes,tests/test_demo.py::t,Approved\n'
        + 'TC-002,SR-002;LLR-002,Unit,m,Full,,"e",Yes,tests/test_demo.py::t2,Approved\n',
        encoding="utf-8",
    )
    assert _derive(scaffold)["gate"] == "DevStg-Tests"


def test_draft_sn_drops_the_gate(scaffold):
    # A Drafted SN (section-as-state) sits at DevStg-Below and drops the derived gate too.
    make_minimal_project(scaffold)
    sn = scaffold / "docs" / "requirements" / "stakeholder-needs.md"
    sn.write_text(
        sn.read_text(encoding="utf-8") + "\n## Draft needs (unratified)\n\n"
        "| SN-ID | Need | Priority | Acceptance |\n|---|---|---|---|\n"
        "| SN-050 | drafted | S | tbd |\n",
        encoding="utf-8",
    )
    result = _derive(scaffold)
    assert result["raw"] == GATE.BAR_BELOW
    assert result["drafted"] == 1
    # The double-counting seam (WI-401): SN-050 is cited by no SR, but a Drafted
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
    # an unanswered need — DevStg-Reqs is not earned. The raw level caps at DevStg-Below, the
    # runnable value floors to DevStg-Reqs, and the basis carries uncovered=N so the cause
    # never hides (drafted=0 here: before this rung, computed=DevStg-Below implied a draft).
    make_minimal_project(scaffold)
    _append_ratified_sn(
        scaffold, "| SN-002 | Subtract two numbers. | Demo. | M | sub(3,2) is 1. |\n"
    )
    result = _derive(scaffold)
    assert result["raw"] == GATE.BAR_BELOW
    assert result["gate"] == "DevStg-Reqs"
    assert result["drafted"] == 0
    assert result["uncovered"] == 1
    assert "uncovered=1 computed=DevStg-Below" in GATE.basis_line(result)


def test_covering_the_sn_restores_the_prior_level(scaffold):
    # The counter-half: citing the need from an SR's SN-Refs releases the cap —
    # the same registry state otherwise reads its ceiling again, uncovered=0.
    make_minimal_project(scaffold)
    _append_ratified_sn(
        scaffold, "| SN-002 | Subtract two numbers. | Demo. | M | sub(3,2) is 1. |\n"
    )
    _write(scaffold, srs=_sr("SR-001", sn="SN-001;SN-002"))
    result = _derive(scaffold)
    assert result["raw"] == GATE.BAR_TESTS  # OI-30 D2 ceiling
    assert result["gate"] == "DevStg-Tests"
    assert result["uncovered"] == 0
    assert "uncovered=0 computed=DevStg-Tests" in GATE.basis_line(result)


def test_example_rows_are_ignored_by_the_coverage_rung(scaffold):
    # -000 rows on BOTH sides of the join are out of scope: an SN-000 placeholder
    # never fires the rung, and an example SR-000 row is filtered before the
    # coverage set is built, so its SN-Refs cannot fake coverage of a real need.
    make_minimal_project(scaffold)
    _append_ratified_sn(scaffold, "| SN-000 | Example placeholder. | M | n/a |\n")
    result = _derive(scaffold)
    assert result["uncovered"] == 0
    assert result["gate"] == "DevStg-Tests"
    # A real ratified need answered ONLY by an example SR row stays uncovered.
    _append_ratified_sn(scaffold, "| SN-002 | Real need. | M | tbd |\n")
    _write(scaffold, srs=_sr("SR-001") + _sr("SR-000", sn="SN-002"))
    result = _derive(scaffold)
    assert result["uncovered"] == 1
    assert result["raw"] == GATE.BAR_BELOW


def test_ex_draft_treats_the_coverage_rung_consistently(scaffold):
    # A ratified SN answered ONLY by a Drafted SR. In the RAW view the citation
    # stands — trace.py's orphan rule reads the same cited set, so neither
    # surface calls the need uncovered (the Drafted SR itself is what drops raw to
    # DevStg-Below, one fact one finding). In the ex-draft counterfactual the SAME
    # arithmetic runs over the non-draft subset: the citation leaves with its
    # row, the need reads unanswered, and ex-draft stays DevStg-Below — removing a draft
    # answer must not fabricate coverage or a level the spine never earned.
    make_minimal_project(scaffold)
    _append_ratified_sn(
        scaffold, "| SN-002 | Subtract two numbers. | Demo. | M | sub(3,2) is 1. |\n"
    )
    _write(scaffold, srs=_sr("SR-001") + _sr("SR-002", status="Drafted", sn="SN-002"))
    result = _derive(scaffold)
    assert result["raw"] == GATE.BAR_BELOW
    assert result["drafted"] == 1
    assert result["uncovered"] == 0  # the Drafted SR's citation counts in the raw view
    assert (
        result["ex_draft"] == GATE.BAR_BELOW
    )  # ...but does not survive its row's removal


# --- WI-188: the derived current phase ----------------------------------------
def test_phase_num_digit_parses():
    # The one phase-parse the kit shares: bare integers and vN both digit-parse.
    assert GATE.phase_num({"Phase": "v2"}) == 2
    assert GATE.phase_num({"Phase": "3"}) == 3
    assert GATE.phase_num({"Phase": ""}) is None
    assert GATE.phase_num({"Phase": "later"}) is None
    assert GATE.phase_num({}) is None


def test_derived_current_phase(scaffold):
    # The derived current phase = the highest phase over RATIFIED rows; a Drafted in a
    # not-yet-ratified higher phase does not bump it (the phase analogue of the gate).
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "system-requirements.csv").write_text(
        SRS_H.rstrip("\n")
        + ",Phase\n"
        + _sr("SR-001").rstrip("\n")
        + ",1\n"
        + _sr("SR-002").rstrip("\n")
        + ",3\n"
        + _sr("SR-003", status="Drafted").rstrip("\n")
        + ",4\n",
        encoding="utf-8",
    )
    assert _derive(scaffold)["phase"] == 3  # SR-003's phase 4 is Drafted, so excluded


def test_derived_phase_none_when_unphased(scaffold):
    # An unphased spine (no Phase column) reads phase=(none) — a non-adopter is
    # unaffected, exactly like the all-blank --strict-schema case.
    make_minimal_project(scaffold)
    assert _derive(scaffold)["phase"] is None


# --- WI-402: --next-phase, the derived next phase as an output mode -----------
def test_next_phase_prints_max_plus_one(scaffold):
    # --next-phase = max(phase over non-draft spine rows) + 1, printed bare so
    # the intake mint helper (WI-388) can shell out and int() the answer when a
    # confirmed scope change opens a new phase. A Drafted row's phase is not yet
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
        + _sr("SR-003", status="Drafted").rstrip("\n")
        + ",4\n",
        encoding="utf-8",
    )
    gate_file = scaffold / "docs" / "gate"
    before = gate_file.read_text(encoding="utf-8")
    proc = run_py(["scripts/derive_gate.py", "--next-phase"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stdout.strip() == "4"  # max ratified = 3; the Drafted 4 is excluded
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
    # Repo-review 2026-07-21 M-6: a Drafted TC citing only its LLR (a legal shape
    # the orphan rules accept) dropped the repo's raw min while the per-phase
    # view stayed green — the phase-drop detector then pointed at nothing. TC
    # refs now resolve through the LLR->SR map, so the phase bucket sees it.
    make_minimal_project(scaffold)
    _write(
        scaffold,
        srs=_sr("SR-001", status="Approved"),
        llrs='LLR-001,SR-001,Adder,src/demo,add,"d",(see TC-001),Approved\n',
        tcs='TC-001,LLR-001,Unit,m,Smoke,"a=1","e",Yes,tests,Drafted\n',
    )
    result = _derive(scaffold)
    assert result["raw"] == GATE.BAR_BELOW
    assert (
        result["per_phase"]["(default)"] == "DevStg-Below"
    )  # was DevStg-Reqs/DevStg-Tests before the fix


# --- ex-draft: the level the drafts are hiding (WI-341) -----------------------
def _mature_single_phase_reopened(scaffold):
    """A single-phase spine at its ceiling, then ONE Drafted SR added.

    This is the shape 128-REVIEW-A (MAJOR 3) showed the old per-phase heuristic
    could not see: the Drafted drops the only phase to DevStg-Below, so the breakdown that
    was the evidence of maturity is erased by the very row it is meant to
    qualify.
    """
    make_minimal_project(scaffold)
    _write(
        scaffold,
        srs=_sr("SR-001") + _sr("SR-002", status="Drafted"),
        llrs='LLR-001,SR-001,Adder,src/demo,add,"d",(see TC-001),Approved\n',
        tcs='TC-001,SR-001;LLR-001,Unit,m,Smoke,"a=1","e",Yes,tests,Approved\n',
    )
    return _derive(scaffold)


def test_ex_draft_reports_the_level_the_drafts_are_hiding(scaffold):
    result = _mature_single_phase_reopened(scaffold)
    # What the drafts produce...
    assert result["raw"] == GATE.BAR_BELOW
    assert result["per_phase"]["(default)"] == "DevStg-Below"
    # ...and what the rows they did not touch still say. THIS is the evidence a
    # draft cannot erase, and it is why the field exists.
    assert result["ex_draft"] == GATE.BAR_TESTS  # OI-30 D2 ceiling
    assert "ex-draft=DevStg-Tests" in GATE.basis_line(result)


def test_ex_draft_stays_low_when_the_spine_never_climbed(scaffold):
    # The mirror case: drafts on a spine whose ratified rows are undecomposed.
    # Removing the drafts changes nothing, so there is no hidden maturity — the
    # early-project false positive stays fixed at the source, not by a heuristic.
    make_minimal_project(scaffold)
    _write(
        scaffold,
        srs=_sr("SR-001", status="Approved") + _sr("SR-002", status="Drafted"),
        llrs=LLRS_H[:0],
        tcs=TCS_H[:0],
    )
    (scaffold / "docs" / "requirements" / "low-level-requirements.csv").write_text(
        LLRS_H, encoding="utf-8"
    )
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(TCS_H, encoding="utf-8")
    result = _derive(scaffold)
    assert result["raw"] == GATE.BAR_BELOW
    assert result["ex_draft"] == GATE.BAR_REQS


def test_ex_draft_equals_computed_when_nothing_is_pending(scaffold):
    # No drafts -> the counterfactual IS the actual. A window test reading these
    # two can then never fire on a clean repo, whatever its level.
    make_minimal_project(scaffold)
    result = _derive(scaffold)
    assert result["drafted"] == 0
    assert result["ex_draft"] == result["raw"]


def test_the_basis_line_still_parses_under_checks_window_regexes(scaffold):
    """THE PRODUCER-CONSUMER ROUND TRIP (D-9 migration §F1, risk 1).

    `check.window_open` decides whether an open ratification window is
    SUPPRESSING the derived bar, and it decides it by regex over the one line
    this module writes. When that pairing breaks, nothing fails: the detector
    silently answers "no window", and the twelve gate steps a window would have
    kept running stop running — measured, over twelve commits, at the
    2026-07-26/27 window (check.py's own `window_open` docstring).

    So the pin is the round trip itself, not a literal: every field
    `check.py` extracts must be extractable from what `basis_line` actually
    emits. A future field insert that breaks any of the four fails HERE, in the
    commit that makes it, instead of going quiet in production.
    """
    check = load_script("check")
    make_minimal_project(scaffold)
    _write(
        scaffold,
        srs=_sr("SR-001", status="Drafted") + _sr("SR-002", status="Approved"),
    )
    result = _derive(scaffold)
    line = GATE.basis_line(result)
    basis = check._BASIS_RE.search(line)
    assert basis is not None, "check._BASIS_RE no longer matches basis_line: " + line
    # ...and it extracts the counts the window test reads, by VALUE — a regex
    # that matched while capturing the wrong groups would be worse than one
    # that did not match at all. `_basis_counts` is the reader, so the round
    # trip is driven through IT rather than through raw groups: the absent
    # `modified=` field must arrive as 0, not as None.
    assert check._basis_counts(basis) == (1, 0), line
    for name in ("_COMPUTED_RE", "_EX_DRAFT_RE", "_PER_PHASE_RE"):
        assert getattr(check, name).search(line) is not None, (name, line)
    # THE FIELD EDITS ARE PINNED, in both directions. `drafts=` became
    # `drafted=`, `planned=` was DELETED at step 5, and `modified=` was DELETED
    # at step 7 — each half has to be visible here or the regex above could be
    # matching a field that no longer means what the consumer thinks it means.
    assert " drafted=" in line and " drafts=" not in line, line
    assert "planned=" not in line, line
    assert "modified=" not in line, line
    assert result["drafted"] == 1 and "drafted=1" in line, line
    # THE CONSUMER STILL HONOURS THE RETIRED FIELD, which is the asymmetry
    # step 7 chose deliberately: this kit stopped EMITTING `modified=`, but a
    # gate file it did not produce — a downstream repo mid-migration, or one
    # regenerated by an older kit — still carries one, and dropping the
    # consumer half would silently disarm the window detector's one
    # CONCLUSIVE arm for exactly those repos. Drive both files through the
    # real reader.
    legacy = line.replace(" drafted=", " drafted=0 modified=7 IGNORED=", 1)
    legacy_match = check._BASIS_RE.search(legacy)
    assert legacy_match is not None, legacy
    assert check._basis_counts(legacy_match) == (0, 7), legacy
    gate_file = scaffold / "docs" / "gate"
    gate_file.write_text(legacy + "\nDevStg-Reqs\n", encoding="utf-8", newline="\n")
    assert check.window_open(gate_file) is True


# --- OI-30 D2: the sr_bar ceiling and its one rendering home ------------------
def test_sr_bar_CEILINGS_at_DevStg_Tests_and_impl_is_unreachable_by_cell():
    """THE REGRESSION PIN FOR THE CEILING (owner ruling OI-30 D2, 2026-08-15).

    DELETE THIS TEST DELIBERATELY, IN THE COMMIT THAT LANDS THE HARNESS DRIVER,
    together with `derive_gate._RELEASE_CEILING`. It exists so that removing the
    ceiling is an ACT — a red test somebody has to answer for — rather than a
    drift nobody notices. Do not "fix" it by loosening the assertion.

    What it guards: D-9 step 5 deleted the pass claim from the Status vocabulary
    (`Verified` and `Planned` both folded into `Approved`, OI-30 D1). Without the
    ceiling, a decomposed row that was `Planned` — ratified text, evidence never
    established — would satisfy the old `decomposed and verified` rule and RAISE
    the derived gate to DevStg-Impl, having passed nothing. That is the
    migration plan's §F5 risk arriving in production.
    """
    approved = {"Status": "Approved", "Verification": "Test"}
    assert GATE.sr_bar(approved, True, True) == GATE.BAR_TESTS
    # ...and by every other route to "decomposed", including the LLR-exempt
    # methods, which reach decomposed on a TC alone.
    for method in ("Analysis", "Inspection", "Attest"):
        exempt = {"Status": "Approved", "Verification": method}
        assert GATE.sr_bar(exempt, False, True) == GATE.BAR_TESTS, method
    # No SR row of ANY live Status reaches the top bar by cell.
    for status in ("Drafted", "Approved", "Modified"):
        for has_llr in (True, False):
            for has_tc in (True, False):
                row = {"Status": status, "Verification": "Test"}
                assert GATE.sr_bar(row, has_llr, has_tc) != GATE.BAR_RELEASE, (
                    status,
                    has_llr,
                    has_tc,
                )
    # The bar itself is NOT deleted — `--gate DevStg-Impl` stays invocable, so
    # the ceiling withholds escalation rather than removing a plan.
    assert GATE.BAR_NAMES[GATE.BAR_RELEASE] == "DevStg-Impl"
    assert GATE.BAR_NAMES[GATE.BAR_RELEASE] in GATE.BAR_ORDER


def test_the_ceiling_note_has_exactly_ONE_rendering_home():
    """The mitigation the ruling rides on: while the ceiling holds, the derived
    bar's HUMAN rendering says so, from one home, so no surface can quietly omit
    it and read as a regression."""
    assert GATE.bar_label("DevStg-Tests") == (
        "DevStg-Tests (Release: pending harness driver)"
    )
    # Every other value passes through UNTOUCHED — including an unrecognized one
    # off an older cache, which a surface should report as found, not decorate.
    # (the retired-tag entry quotes the old vocabulary on purpose — an older
    # cache is exactly what "pass through untouched" has to cover)
    retired_tag = "G2"  # check_vocab: allow
    for other in ("DevStg-Reqs", "DevStg-Impl", "DevStg-Below", retired_tag, ""):
        assert GATE.bar_label(other) == other, other
    # THE ONE HOME, asserted structurally: the note's text appears in exactly one
    # shipped script, and every other surface reaches it through `bar_label`. A
    # second formatter is the failure this pin exists for.
    from pathlib import Path as _Path

    scripts = _Path(__file__).resolve().parents[1] / "project-trajectory" / "scripts"
    carriers = [
        p.name
        for p in sorted(scripts.glob("*.py"))
        if "Release: pending harness driver" in p.read_text(encoding="utf-8")
    ]
    assert carriers == ["derive_gate.py"], carriers
    # ...and the human status surface CALLS it rather than interpolating a name.
    traj_status = (scripts / "traj_status.py").read_text(encoding="utf-8")
    assert "derive_gate.bar_label(" in traj_status


def test_the_ceiling_note_never_reaches_the_MACHINE_value(scaffold):
    """`docs/gate`'s last line is matched exactly by `check.py` and by CI. The
    note is for readers; putting it there would break every consumer to make a
    comment."""
    make_minimal_project(scaffold)
    run_py(["scripts/derive_gate.py"], cwd=scaffold)
    text = (scaffold / "docs" / "gate").read_text(encoding="utf-8")
    assert "pending harness driver" not in text
    value = [ln for ln in text.splitlines() if ln and not ln.startswith("#")][-1]
    assert value in GATE.BAR_ORDER, value
