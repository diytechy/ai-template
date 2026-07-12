"""trace.py: orphan detection and the --require-verified G3 criterion."""

from conftest import KIT, make_minimal_project, run_py

# SR-002 is a genuine (ratified, non-Draft) orphan: Status=Planned, so the
# derived-gate Draft exemption (WI-089) does NOT apply and the decomposition
# rules still fire. A Draft SR would be exempt — see the WI-089 section below.
ORPHAN_SR = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Verified
SR-002,Orphaned,SN-001,"The system shall do something untested.","Demo orphan.","n/a",,M,Test,Planned
"""


def test_happy_chain_is_orphan_free(scaffold):
    make_minimal_project(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "orphans=0" in proc.stdout


def test_orphan_sr_fails_strict(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "system-requirements.csv").write_text(
        ORPHAN_SR, encoding="utf-8"
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SR SR-002 has no LLR" in report
    assert "SR SR-002 has no test (TC)" in report


NO_SN_SR = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,,"The system shall add two numbers.","Rootless.","add(1,2) == 3",,M,Test,Verified
"""


def test_sr_with_no_sn_link_is_an_orphan(scaffold):
    # G1's "every SR links >=1 SN" is machine-checked from the orphan sweep (not
    # only at G3 --strict-schema): an SR with an empty SN-Refs fails --strict
    # whenever the needs registry provides real SN ids.
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "system-requirements.csv").write_text(
        NO_SN_SR, encoding="utf-8"
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SR SR-001 links no SN" in report
    # ... and the un-referenced SN is reported from its own side too.
    assert "SN SN-001 has no SR" in report


def test_strict_integrity_ignores_orphans_but_fails_bad_ids(scaffold):
    # The pre-commit floor: orphans (a gate criterion) pass, a malformed id (an
    # always-invalid state) fails.
    make_minimal_project(scaffold)
    srs = scaffold / "docs" / "requirements" / "system-requirements.csv"
    srs.write_text(ORPHAN_SR, encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    srs.write_text(ORPHAN_SR.replace("SR-002", "SR-2x"), encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc.returncode == 1
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "malformed" in report


# SR-002 is Status=Implemented (ratified + built, not yet Verified) so the phase
# scoping of --require-verified is what the tests exercise — a Draft SR would be
# exempt from --require-verified entirely (WI-089), which is a different axis.
PHASED_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status,Phase
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Verified,v1
SR-002,Future thing,SN-001,"The system shall do a v2 thing.","Realizes SN-001 later.","v2 behavior",,S,Test,Implemented,v2
"""

PHASED_LLRS = """LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status
LLR-001,SR-001,Pure adder,src/demo,add,"Pure function: two numbers -> sum.",(see TC),Implemented
LLR-002,SR-002,Future part,src/future,todo,"Planned decomposition of the v2 SR.",(see TC),Planned
"""

PHASED_TCS = """TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status
TC-001,SR-001;LLR-001,Unit,call add and assert the sum,Smoke,"a=1; b=2","Satisfies SR-001 AcceptanceCriteria",Yes,Verified
TC-002,SR-002;LLR-002,Unit,planned v2 test,Full,,"Satisfies SR-002 AcceptanceCriteria",Yes,Draft
"""


def make_phased_project(scaffold):
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    (req / "system-requirements.csv").write_text(PHASED_SRS, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(PHASED_LLRS, encoding="utf-8")
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(
        PHASED_TCS, encoding="utf-8"
    )


def test_phase_scopes_require_verified(scaffold):
    # A v2 SR that is not yet Verified fails an unscoped G3 check, but a
    # --phase v1 closure defers it explicitly (and the deferral is reported).
    make_phased_project(scaffold)
    proc = run_py(["scripts/trace.py", "--strict", "--require-verified"], cwd=scaffold)
    assert proc.returncode == 1
    assert "status-findings=1" in proc.stdout

    proc = run_py(
        ["scripts/trace.py", "--strict", "--require-verified", "--phase", "v1"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "phase-deferred=1" in proc.stdout
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "Phase-deferred (explicitly out of scope)" in report
    assert "SR SR-002 (Phase=v2)" in report

    # Cumulative closure: once v2 is in scope, the Draft SR fails again.
    proc = run_py(
        ["scripts/trace.py", "--strict", "--require-verified", "--phase", "v1,v2"],
        cwd=scaffold,
    )
    assert proc.returncode == 1


def test_phase_blind_orphan_rules_still_apply(scaffold):
    # Tagging an SR v2 never exempts it from decomposition/coverage: drop its
    # TC and the trace fails even under --phase v1.
    make_phased_project(scaffold)
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(
        PHASED_TCS.replace(
            "TC-002,SR-002;LLR-002,Unit,planned v2 test,Full,,"
            '"Satisfies SR-002 AcceptanceCriteria",Yes,Draft\n',
            "",
        ),
        encoding="utf-8",
    )
    proc = run_py(
        ["scripts/trace.py", "--strict", "--require-verified", "--phase", "v1"],
        cwd=scaffold,
    )
    assert proc.returncode == 1
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SR SR-002 has no test (TC)" in report


def test_check_py_passes_phase_to_trace():
    from conftest import load_script

    check = load_script("check")
    trace_cmd = next(
        s[2] for s in check.steps(80, "full", "G3", "v1") if s[0] == "traceability"
    )
    assert "--phase" in trace_cmd and "v1" in trace_cmd
    # No phase given -> no --phase flag; G2 never carries --require-verified.
    trace_cmd = next(
        s[2] for s in check.steps(80, "full", "G3") if s[0] == "traceability"
    )
    assert "--phase" not in trace_cmd


# --- WI-1.7: human-attestation verification kind (Attest) ---------------------

# An Attest SR: a named human's recorded judgment, no code to decompose (so
# LLR-exempt), but it still needs a TC that records who/when attested.
ATTEST_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Verified
SR-002,Theme mood fit,SN-001,"The main theme shall match the mood brief.","Subjective; no automated check.","Creative lead records pass against the brief.",,H,Attest,Verified
"""

ATTEST_TCS = """TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status
TC-001,SR-001;LLR-001,Unit,call add and assert the sum,Smoke,"a=1; b=2","Satisfies SR-001 AcceptanceCriteria",Yes,tests/test_demo.py::test_add_sr001,Verified
TC-002,SR-002,System,creative review of the theme,Release,"attested-by=A. Rivera; attested-on=2026-07-02","Recorded pass judgment for SR-002",No,,Verified
"""


def make_attest_project(scaffold):
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    (req / "system-requirements.csv").write_text(ATTEST_SRS, encoding="utf-8")
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(
        ATTEST_TCS, encoding="utf-8"
    )


def test_attest_sr_is_llr_exempt_but_needs_tc(scaffold):
    # SR-002 (Attest) has no LLR yet is not an orphan; it still needs its TC.
    make_attest_project(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SR SR-002 has no LLR" not in report
    # Drop its TC -> now it is an orphan (every SR needs >=1 TC regardless of method).
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(
        ATTEST_TCS.replace(
            "TC-002,SR-002,System,creative review of the theme,Release,"
            '"attested-by=A. Rivera; attested-on=2026-07-02",'
            '"Recorded pass judgment for SR-002",No,,Verified\n',
            "",
        ),
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SR SR-002 has no test (TC)" in report


def test_attest_verified_accepted_and_surfaced_distinctly(scaffold):
    # Under --require-verified (G3), an Attest SR marked Verified passes, and the
    # report surfaces it under "attested vs mechanized" so the trust footprint is
    # auditable.
    make_attest_project(scaffold)
    proc = run_py(
        ["scripts/trace.py", "--strict", "--require-verified", "--strict-schema"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "verified-attested=1" in proc.stdout
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "Verification basis (attested vs mechanized)" in report
    assert "Attested (Attest): 1 — SR-002" in report
    assert "Verified SRs — attested (human, §4) | 1 |" in report
    assert "Verified SRs — mechanized | 1 |" in report


def test_attest_is_in_verification_vocabulary(scaffold):
    # --strict-schema must accept Attest (not reject it as out-of-vocabulary).
    make_attest_project(scaffold)
    proc = run_py(["scripts/trace.py", "--strict-schema"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SR-002 has Verification=" not in report  # no enum-violation finding


# --- WI-068: the Critique verification value ----------------------------------

# A Critique SR: subjective acceptance judged by an independent critical eye
# against a rubric. Unlike Attest, its artifact is PRODUCED BY CODE (only the
# acceptance is perceptual), so it is NOT LLR-exempt.
CRITIQUE_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Verified
SR-002,Render realism,SN-001,"The rendered scene shall look realistic.","Subjective; judged by a critic against a rubric.","Critic judges the render against docs/rubrics/render.md anchors.",,S,Critique,Verified
"""

CRITIQUE_TCS = """TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status
TC-001,SR-001;LLR-001,Unit,call add and assert the sum,Smoke,"a=1; b=2","Satisfies SR-001 AcceptanceCriteria",Yes,tests/test_demo.py::test_add_sr001,Verified
TC-002,SR-002,System,critique the render against the rubric,Release,"rubric=docs/rubrics/render.md; artifact=render.png","Critic APPROVE per the rubric anchors",No,,Verified
"""


def make_critique_project(scaffold):
    # SR-002 is Critique with NO LLR (the minimal chain keeps only LLR-001).
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    (req / "system-requirements.csv").write_text(CRITIQUE_SRS, encoding="utf-8")
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(
        CRITIQUE_TCS, encoding="utf-8"
    )


def test_critique_verification_value(scaffold):
    make_critique_project(scaffold)
    # 1) Critique is in the closed Verification vocabulary: --strict-schema does
    #    not flag it as out-of-vocabulary.
    proc = run_py(["scripts/trace.py", "--strict-schema"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SR-002 has Verification=" not in report
    # 2) A Critique SR is NOT LLR-exempt (unlike Attest): SR-002 has no LLR, so it
    #    is an orphan (the artifact is produced by code — only acceptance is
    #    subjective).
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SR SR-002 has no LLR" in report
    # 3) An unknown Verification value is still rejected.
    (scaffold / "docs" / "requirements" / "system-requirements.csv").write_text(
        CRITIQUE_SRS.replace(",Critique,", ",Perceptual,"), encoding="utf-8"
    )
    proc = run_py(["scripts/trace.py", "--strict", "--strict-schema"], cwd=scaffold)
    assert proc.returncode == 1
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "Perceptual" in report  # the out-of-vocabulary finding


# --- Thread 1: generated traceability views (outline + Mermaid + HTML) ---------


def _outline_section(report):
    """The text-outline block of report.md (between its two view headings)."""
    start = report.index("## Traceability outline")
    return report[start : report.index("## Traceability graph")]


def test_report_has_text_outline_and_mermaid_graph(scaffold):
    make_minimal_project(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    # The Mermaid DAG view is present.
    assert "```mermaid" in report
    assert "graph LR" in report
    # The text outline shows the minimal chain SN-001 -> SR-001 -> LLR-001 -> TC-001,
    # in nesting order.
    outline = _outline_section(report)
    positions = [outline.index(i) for i in ("SN-001", "SR-001", "LLR-001", "TC-001")]
    assert positions == sorted(positions), outline


def test_orphan_node_flagged_in_outline_and_graph(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "system-requirements.csv").write_text(
        ORPHAN_SR, encoding="utf-8"
    )
    proc = run_py(["scripts/trace.py"], cwd=scaffold)  # views render regardless of exit
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    # Mermaid: the orphan (Planned) SR-002 gets the distinct class.
    assert "classDef orphan" in report
    assert "class SR_002 orphan" in report
    # Outline: the same node carries an inline flag on its own line.
    sr002 = next(
        ln
        for ln in _outline_section(report).splitlines()
        if ln.strip().startswith("- SR-002")
    )
    assert "[orphan]" in sr002


def test_html_view_is_self_contained(scaffold):
    make_minimal_project(scaffold)
    proc = run_py(["scripts/trace.py", "--html"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    html_path = scaffold / "docs" / "test" / "report.html"
    assert html_path.exists()
    html = html_path.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in html
    assert "<details" in html  # collapsible tree
    assert "<script" not in html  # zero JS — self-contained


def test_gitignore_ignores_the_html_artifact(scaffold):
    gitignore = (scaffold / ".gitignore").read_text(encoding="utf-8")
    assert "docs/test/report.html" in gitignore


# --- Thread 5: the optional Lifecycle tag is a schema-safe extra column ---------

LIFECYCLE_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status,Lifecycle
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Verified,Startup
"""


def test_lifecycle_column_is_schema_safe(scaffold):
    # An SR carrying an optional Lifecycle column (mirroring Area) must pass even
    # the strictest schema check: trace.py validates a fixed REQUIRED_FIELDS
    # allow-list and tolerates unknown extra columns, so no downstream migration
    # is forced (process.md §4 "Lifecycle phase").
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "system-requirements.csv").write_text(
        LIFECYCLE_SRS, encoding="utf-8"
    )
    proc = run_py(
        ["scripts/trace.py", "--strict", "--strict-schema", "--no-placeholders"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


AREA_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status,Area
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Verified,math
"""


def test_area_column_is_schema_safe(scaffold):
    # Multi-module scoping groups a module's rows by the optional `Area` tag on
    # SR/TC (process.md §10). Like `Lifecycle`, `Area` is an extra column outside
    # REQUIRED_FIELDS, so a module-tagged registry passes the strictest schema
    # check with no downstream migration — the precedent that makes module-scoped
    # review a convention over existing columns rather than new machinery.
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "system-requirements.csv").write_text(
        AREA_SRS, encoding="utf-8"
    )
    proc = run_py(
        ["scripts/trace.py", "--strict", "--strict-schema", "--no-placeholders"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


# --- Thread 35: Area is a first-class (still optional) SR column ---------------

AREA_MIXED_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status,Area
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Verified,math
SR-002,Addition report,SN-001,"The system shall report the sum.","Realizes SN-001.","Sum is printed.",,M,Attest,Verified,
"""


def test_shipped_sr_template_carries_area_column():
    # The shipped header ends with Area so a project records hat ownership
    # without inventing its own 12th column (the Finance-Auditor field report).
    header = (
        (KIT / "registries" / "system-requirements.template.csv")
        .read_text(encoding="utf-8")
        .splitlines()[0]
    )
    assert header.split(",")[-1] == "Area"


def test_shipped_tc_template_carries_evidence_column():
    # Thread 51: the shipped TC header carries Evidence (between Automated and
    # Status) so the concrete test location has a first-class home and stops
    # overloading Parameters (which stays dimensional, the gen_cases grammar).
    header = (
        (KIT / "registries" / "test-cases.template.csv")
        .read_text(encoding="utf-8")
        .splitlines()[0]
    )
    assert header.split(",")[-3:] == ["Automated", "Evidence", "Status"]


def test_area_values_yield_report_section(scaffold):
    # A registry with real Area values gets a per-Area SR count in the report —
    # report-only: the run stays green, and blank cells count as untagged.
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    (req / "system-requirements.csv").write_text(AREA_MIXED_SRS, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(
        "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status\n"
        'LLR-001,SR-001,Pure adder,src/demo,add,"Two numbers -> sum.",(see TC),Implemented\n',
        encoding="utf-8",
    )
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status\n"
        'TC-001,SR-001;LLR-001,Unit,call add,Smoke,"a=1; b=2",Sum,Yes,Verified\n'
        "TC-002,SR-002,Manual,read the report,Full,,Sum printed,No,Verified\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "## SRs by Area (report-only)" in report
    assert "- math: 1" in report
    assert "- (no Area): 1" in report


def test_no_area_values_no_report_section(scaffold):
    # The minimal project's registry has no Area column at all: the section must
    # be absent, not rendered empty (legacy CSVs see zero change).
    make_minimal_project(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SRs by Area" not in report


def test_require_verified_flags_unverified_test_sr(scaffold):
    make_minimal_project(scaffold)
    csv_path = scaffold / "docs" / "requirements" / "system-requirements.csv"
    csv_path.write_text(
        csv_path.read_text(encoding="utf-8").replace(
            ",M,Test,Verified", ",M,Test,Implemented"
        ),
        encoding="utf-8",
    )
    # Without the flag: still a clean trace (status is a G3 concern).
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # With the flag: the unverified Test SR fails the gate.
    proc = run_py(["scripts/trace.py", "--strict", "--require-verified"], cwd=scaffold)
    assert proc.returncode == 1
    assert "status-findings=1" in proc.stdout
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "G3 requires Verified" in report


# --- WI-056: the IF-### interface-seam tier (process.md §8) ---------------------
# trace.py now reads the interface catalog (the SR-002-era gap): IF id integrity,
# the SR-Refs back-link (a --strict finding, like PB's), and a warn-only endpoint
# advisory. The full architecture-connectivity coverage lives in check_trajectory.

IF_HEADER = (
    "IF-ID,Direction,ThisProject,Counterpart,Contract,SR-Refs,Version,"
    "Stability,Status,Component,Notes\n"
)


def _write_ifs(scaffold, body):
    (scaffold / "docs" / "requirements" / "interfaces.csv").write_text(
        IF_HEADER + body, encoding="utf-8"
    )


def _report(scaffold):
    return (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")


def test_if_tier_integrity(scaffold):
    make_minimal_project(scaffold)
    # A clean seam: SR-Refs resolves (SR-001), ThisProject matches LLR Module.
    _write_ifs(
        scaffold,
        'IF-001,Provides,src/demo,downstream adopter,"cli --help exits 0",'
        "SR-001,v1,Stable,Active,,\n",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "interfaces=1 interface-findings=0" in proc.stdout

    # Empty SR-Refs -> a --strict finding (every seam links the spine, PB idiom).
    _write_ifs(scaffold, 'IF-001,Provides,src/demo,git,"pushes",,v1,Stable,Active,,\n')
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    assert "IF IF-001 links no SR" in _report(scaffold)

    # Unresolvable SR-Ref -> a finding naming the missing id.
    _write_ifs(
        scaffold, 'IF-001,Provides,src/demo,git,"pushes",SR-999,v1,Stable,Active,,\n'
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    assert "IF IF-001 references unknown SR-999" in _report(scaffold)

    # A malformed IF id joins the always-on integrity floor (--strict-integrity).
    _write_ifs(
        scaffold, 'IF-1x,Provides,src/demo,git,"pushes",SR-001,v1,Stable,Active,,\n'
    )
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc.returncode == 1
    assert "malformed" in _report(scaffold)


def test_if_endpoint_advisory_is_warn_only(scaffold):
    # A ThisProject matching no LLR Module is a warn-only advisory (the LLR Module
    # inventory is partial + differently named), never a failure.
    make_minimal_project(scaffold)
    _write_ifs(
        scaffold, 'IF-001,Provides,src/nowhere,git,"x",SR-001,v1,Stable,Active,,\n'
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "matches no LLR Module" in proc.stdout
    assert "endpoint advisories" in _report(scaffold).lower()


def test_if_placeholder_and_absent_are_free(scaffold):
    # The scaffold ships an inert IF-000 placeholder: no interface section, green.
    make_minimal_project(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "interfaces=" not in proc.stdout  # only the -000 placeholder
    # A truly absent registry is equally free.
    (scaffold / "docs" / "requirements" / "interfaces.csv").unlink()
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_legacy_interfaces_csv_without_notes_column_parses(scaffold):
    # A pre-WI-056 interfaces.csv (no Notes column) reads the missing cell as
    # empty and never crashes — never-breaking.
    make_minimal_project(scaffold)
    legacy = (
        "IF-ID,Direction,ThisProject,Counterpart,Contract,SR-Refs,Version,"
        "Stability,Status,Component\n"
    )
    (scaffold / "docs" / "requirements" / "interfaces.csv").write_text(
        legacy + 'IF-001,Provides,src/demo,git,"x",SR-001,v1,Stable,Active,\n',
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "interfaces=1 interface-findings=0" in proc.stdout


# --- WI-089: the Draft artifact state + decomposition exemption ---------------
# The derived-gate model (docs/specs/derived-gate-model.md §3) lets a requirement
# be drafted in the LIVE spine before it is decomposed: a `Draft` SR/LLR is exempt
# from the child-completeness orphan rules and the --require-verified criterion,
# retiring the -000/off-spine workaround. Parent-linkage + integrity still apply.

# SR-002 is Draft with NO LLR and NO TC (undecomposed), but it links SN-001. It
# must NOT orphan. SR-001 keeps the fully-traced happy chain.
DRAFT_SR = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Verified
SR-002,Drafted requirement,SN-001,"The system shall do a not-yet-decomposed thing.","Being drafted requirement-first.","some measurable outcome",,M,Test,Draft
"""


def test_draft_sr_is_exempt_from_decomposition(scaffold):
    # A Draft SR with no LLR/TC lives in the live spine without orphaning.
    make_minimal_project(scaffold)
    srs = scaffold / "docs" / "requirements" / "system-requirements.csv"
    srs.write_text(DRAFT_SR, encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "orphans=0" in proc.stdout
    assert "drafts=1" in proc.stdout
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SR SR-002 has no LLR" not in report
    assert "SR SR-002 has no test (TC)" not in report
    assert "## Draft artifacts (decomposition-exempt)" in report
    assert "SR-002 — Drafted requirement" in report
    # Ratify it (Draft -> Planned) and the decomposition rules fire again.
    srs.write_text(
        DRAFT_SR.replace(",M,Test,Draft", ",M,Test,Planned"), encoding="utf-8"
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SR SR-002 has no LLR" in report
    assert "SR SR-002 has no test (TC)" in report


# A Draft LLR decomposing SR-001 but with no TC: exempt from the "no TC" rule.
DRAFT_LLRS = """LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status
LLR-001,SR-001,Pure adder,src/demo,add,"Pure function: two numbers -> sum.",(see TC),Implemented
LLR-002,SR-001,Draft sub-part,src/demo,addfast,"A not-yet-tested decomposition.",(see TC),Draft
"""


def test_draft_llr_is_exempt_from_tc_rule(scaffold):
    make_minimal_project(scaffold)
    llrs = scaffold / "docs" / "requirements" / "low-level-requirements.csv"
    llrs.write_text(DRAFT_LLRS, encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "LLR LLR-002 has no test (TC)" not in report
    # Mark it Implemented and the missing TC is an orphan again.
    llrs.write_text(
        DRAFT_LLRS.replace("(see TC),Draft", "(see TC),Implemented"), encoding="utf-8"
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "LLR LLR-002 has no test (TC)" in report


# SR-002 is fully decomposed (LLR-002 + TC-002) so ONLY the status axis varies:
# Draft -> exempt from --require-verified; Implemented -> flagged.
RV_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Verified
SR-002,Drafted requirement,SN-001,"The system shall do a drafted thing.","Being drafted.","some measurable outcome",,M,Test,Draft
"""
RV_LLRS = """LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status
LLR-001,SR-001,Pure adder,src/demo,add,"Pure function: two numbers -> sum.",(see TC),Implemented
LLR-002,SR-002,Draft sub-part,src/demo,addfast,"A drafted decomposition.",(see TC),Draft
"""
RV_TCS = """TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status
TC-001,SR-001;LLR-001,Unit,call add and assert the sum,Smoke,"a=1; b=2","Satisfies SR-001 AcceptanceCriteria",Yes,tests/test_demo.py::test_add_sr001,Verified
TC-002,SR-002;LLR-002,Unit,drafted test,Full,,"Satisfies SR-002 AcceptanceCriteria",No,,Draft
"""


def test_draft_sr_is_exempt_from_require_verified(scaffold):
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    (req / "system-requirements.csv").write_text(RV_SRS, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(RV_LLRS, encoding="utf-8")
    srs = req / "system-requirements.csv"
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(RV_TCS, encoding="utf-8")
    # Draft SR-002 is pre-ratification: --require-verified does not flag it.
    proc = run_py(["scripts/trace.py", "--strict", "--require-verified"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "status-findings=0" in proc.stdout
    # Ratifying it to Implemented (Verification=Test, not yet Verified) flags it.
    srs.write_text(
        RV_SRS.replace(",M,Test,Draft", ",M,Test,Implemented"), encoding="utf-8"
    )
    proc = run_py(["scripts/trace.py", "--strict", "--require-verified"], cwd=scaffold)
    assert proc.returncode == 1
    assert "status-findings=1" in proc.stdout


def test_draft_sr_still_needs_sn_and_stays_integral(scaffold):
    # The Draft exemption is scoped to child-completeness: parent-linkage (the SN
    # link) and id integrity still apply to a Draft row.
    make_minimal_project(scaffold)
    srs = scaffold / "docs" / "requirements" / "system-requirements.csv"
    # A Draft SR with an empty SN-Refs still orphans (SN linkage is not exempt).
    srs.write_text(
        DRAFT_SR.replace(
            "SR-002,Drafted requirement,SN-001,", "SR-002,Drafted requirement,,"
        ),
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    assert "SR SR-002 links no SN" in _report(scaffold)
    # A malformed Draft id still fails the always-on integrity floor.
    srs.write_text(DRAFT_SR.replace("SR-002", "SR-2x"), encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc.returncode == 1
    assert "malformed" in _report(scaffold)
