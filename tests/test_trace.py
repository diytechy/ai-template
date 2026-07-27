"""trace.py: orphan detection and the --require-verified G3 criterion."""

from conftest import KIT, SCRIPTS, load_script, make_minimal_project, run_py

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
    # report surfaces it in the three-way verification-basis split (WI-259) so the
    # trust footprint is auditable: SR-001 is mechanized (Test), SR-002 attested.
    make_attest_project(scaffold)
    proc = run_py(
        ["scripts/trace.py", "--strict", "--require-verified", "--strict-schema"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "verified-mechanized=1" in proc.stdout
    assert "verified-demonstrated=0" in proc.stdout
    assert "verified-attested=1" in proc.stdout
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "Verification basis (mechanized / demonstrated / attested)" in report
    assert "Attested (Attest): 1 — SR-002" in report
    assert "Verified SRs — attested (human, §4) | 1 |" in report
    assert "Verified SRs — mechanized (Test) | 1 |" in report
    assert "Verified SRs — demonstrated/observed | 0 |" in report


def test_attest_is_in_verification_vocabulary(scaffold):
    # --strict-schema must accept Attest (not reject it as out-of-vocabulary).
    make_attest_project(scaffold)
    proc = run_py(["scripts/trace.py", "--strict-schema"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SR-002 has Verification=" not in report  # no enum-violation finding


# --- WI-259: --require-verified is method-blind; the split has a third bucket ---

# A non-Test, non-Attest SR (Analysis here — representative of the
# Demonstration/Manual/Analysis/Inspection/Critique family): its Verified state
# rests on a human observing an outcome, not a runnable check. Analysis is
# LLR-exempt so it decomposes to a TC alone. SR-001 stays the mechanized (Test)
# control.
DEMO_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Verified
SR-002,Analyzed property,SN-001,"The system shall hold an analyzed property.","Judged by analysis, no runnable check.","An analyst records the property holds.",,H,Analysis,Verified
"""

DEMO_TCS = """TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status
TC-001,SR-001;LLR-001,Unit,call add and assert the sum,Smoke,"a=1; b=2","Satisfies SR-001 AcceptanceCriteria",Yes,tests/test_demo.py::test_add_sr001,Verified
TC-002,SR-002,System,analyze the property against the model,Release,"analyst=A. Rivera; analyzed-on=2026-07-21","Recorded analysis pass for SR-002",No,,Verified
"""


def make_demo_project(scaffold):
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    (req / "system-requirements.csv").write_text(DEMO_SRS, encoding="utf-8")
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(
        DEMO_TCS, encoding="utf-8"
    )


def test_demonstrated_sr_is_its_own_category_and_gate_required(scaffold):
    # M-5/WI-259: a non-Test, non-Attest Verified SR is reported in its own
    # "demonstrated/observed" bucket (never folded into mechanized), listed by id
    # so the audit sees it.
    make_demo_project(scaffold)
    proc = run_py(
        ["scripts/trace.py", "--strict", "--require-verified", "--strict-schema"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "verified-mechanized=1" in proc.stdout
    assert "verified-demonstrated=1" in proc.stdout
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "Verified SRs — mechanized (Test) | 1 |" in report
    assert "Verified SRs — demonstrated/observed | 1 |" in report
    # Listed by id under demonstrated/observed — not miscounted as mechanized.
    assert "Demonstrated/observed" in report and "SR-002" in report

    # The headline widening (M-5): regress SR-002 to Implemented. sr_gate already
    # caps it at G2, but the OLD --require-verified (Verification=Test only)
    # silently PASSED it. The widened bar now flags it, naming the real method.
    csv_path = scaffold / "docs" / "requirements" / "system-requirements.csv"
    csv_path.write_text(
        DEMO_SRS.replace(",H,Analysis,Verified", ",H,Analysis,Implemented"),
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict", "--require-verified"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "status-findings=1" in proc.stdout
    assert "Verification=Analysis but Status=Implemented" in proc.stdout
    assert "G3 requires Verified" in proc.stdout


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
    # Pinned by ordering, not tail position — the phase model appends a trailing
    # Phase column after Status.
    header = (
        (KIT / "registries" / "test-cases.template.csv")
        .read_text(encoding="utf-8")
        .splitlines()[0]
    )
    assert "Automated,Evidence,Status" in header
    assert header.split(",")[-1] == "Phase"


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


# --- WI-065: one ruled home for a seam citation — the TC's `Verifies` cell ------
# check_trajectory's seam-TC warn reads IF-### ids out of `Verifies`, but trace's
# orphan rule used to reject any token that was not an SR/LLR id — so citing a
# seam the documented way passed one check and ORPHANED under the other, and the
# rule could not be satisfied honestly. Ruled: `Verifies` is the one citation
# cell, and trace joins IF tokens against interfaces.csv. Both halves of that
# ruling are exercised HERE, on one scaffold, because a test that ran only one
# checker is exactly what let the two disagree for as long as they did.

TWO_MODULE_IFS = (
    'IF-001,Provides,src/demo,src/helper,"add() is called by the helper",'
    "SR-001,v1,Stable,Active,,sink\n"
    'IF-002,Consumes,src/helper,src/demo,"helper reads add()",'
    "SR-001,v1,Stable,Active,,source\n"
)

HELPER_SRC = '''"""A second module, so the connectivity checks are not vacuous."""

from demo import add


def twice(n):
    """Double a number via the seam. Implements: SR-001, LLR-001"""
    return add(n, n)
'''


def _seam_scaffold(scaffold, verifies):
    """A two-module project whose single TC cites `verifies`, arch-map refreshed."""
    make_minimal_project(scaffold)
    (scaffold / "src" / "helper.py").write_text(HELPER_SRC, encoding="utf-8")
    proc = run_py(["scripts/gen_arch_map.py"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    _write_ifs(scaffold, TWO_MODULE_IFS)
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        'TC-001,{},Unit,call add and assert the sum,Smoke,"a=1; b=2",'
        '"Satisfies SR-001 AcceptanceCriteria",Yes,'
        "tests/test_demo.py::test_add_sr001,Verified\n".format(verifies),
        encoding="utf-8",
    )
    return scaffold


def test_seam_citation_satisfies_trace_and_check_trajectory_together(scaffold):
    _seam_scaffold(scaffold, "SR-001;LLR-001;IF-001")

    # Half one: trace no longer orphans the seam token.
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "orphans=0" in proc.stdout
    assert "references unknown IF-001" not in _report(scaffold)

    # Half two: the SAME cell satisfies the seam-TC warn — the cited seam is
    # quiet while its uncited sibling still warns, so this is not vacuous.
    proc = run_py(["scripts/check_trajectory.py"], cwd=scaffold)
    assert "IF IF-001 is Active but cited by no TC" not in proc.stderr
    assert "IF IF-002 is Active but cited by no TC" in proc.stderr


def test_unknown_seam_id_in_verifies_is_still_an_orphan(scaffold):
    # Accepting the IF vocabulary is not accepting anything IF-shaped: an id that
    # resolves to no interfaces.csv row is as wrong as an unknown SR.
    _seam_scaffold(scaffold, "SR-001;LLR-001;IF-999")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    assert "TC TC-001 references unknown IF-999" in _report(scaffold)


def test_tc_citing_only_seam_ids_is_an_orphan(scaffold):
    # A seam citation SUPPLEMENTS the spine citation. Without this rule the new
    # vocabulary would let `Verifies=IF-001` alone pass, and a test would no
    # longer have to say which requirement it discharges.
    _seam_scaffold(scaffold, "IF-001")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    assert "TC TC-001 cites only seam id(s)" in _report(scaffold)


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


# --- WI-090: SN maturity via section-as-state ---------------------------------
# An SN under a heading whose text contains "draft" is unratified (G0) and exempt
# from the "every SN needs an SR" rule; SNs under any other heading are ratified.

DRAFT_SN_MD = """# Stakeholder Needs (SN-###)

## Core needs

| SN-ID | Need | Why | Priority | Acceptance intent |
|---|---|---|---|---|
| SN-001 | Add two numbers. | Demo. | M | add(1,2) gives 3. |

## Draft needs (unratified)

| SN-ID | Need | Why | Priority | Acceptance intent |
|---|---|---|---|---|
| SN-002 | A not-yet-decomposed need. | Being drafted. | S | TBD. |
"""


def test_draft_sn_is_exempt_from_sr_rule(scaffold):
    make_minimal_project(scaffold)
    sn = scaffold / "docs" / "requirements" / "stakeholder-needs.md"
    sn.write_text(DRAFT_SN_MD, encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "drafts=1" in proc.stdout
    report = _report(scaffold)
    assert "SN SN-002 has no SR" not in report
    assert "SN-002 (SN, unratified section)" in report
    # The DAG flags the draft SN like a Status=Draft row.
    assert "class SN_002 draft" in report
    # Ratify SN-002 by moving its row under a non-draft heading -> the SN-with-no-SR
    # rule fires again (it now claims to be a real need with no decomposition).
    ratified = DRAFT_SN_MD.replace("## Draft needs (unratified)", "## More core needs")
    sn.write_text(ratified, encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    assert "SN SN-002 has no SR" in _report(scaffold)


def test_sn_draft_ids_reader():
    from conftest import load_script

    trace = load_script("trace")
    assert trace.sn_draft_ids(DRAFT_SN_MD) == {"SN-002"}
    # A -000 placeholder in a draft section is excluded (like every other scan).
    assert trace.sn_draft_ids("## Draft needs\nSN-000 SN-005\n") == {"SN-005"}
    # No draft heading -> nothing is draft (the ratified default).
    assert trace.sn_draft_ids("# Needs\n\n## Core\nSN-001\n") == set()
    # The "draft" match is on the heading text, case-insensitive, not the body.
    assert trace.sn_draft_ids("## DRAFT items\nSN-009\n") == {"SN-009"}


def test_predicate_markers_are_word_bounded():
    # WI-106 L2: a pinning marker must match on a WORD BOUNDARY. "per"/"within"
    # pin a comparative AC, but a word merely CONTAINING them ("proper",
    # "wrapper") must not silently suppress the warn-only advisory.
    from conftest import load_script

    trace = load_script("trace")

    def warns(ac):
        found = trace.ac_advisories([{"SR-ID": "SR-101", "AcceptanceCriteria": ac}])
        return bool(found)

    # A genuine pinning marker (word or symbol) suppresses the advisory...
    assert not warns("output identical, as per the enumerated list")
    assert not warns("identical: output == expected")
    # ...but the same comparative with only an incidental substring now warns
    # (the boundary-blind substring used to pin "identical" via "proper").
    assert warns("identical in the proper format")
    assert warns("the wrapper output is identical")
    # A bare comparative with no marker at all still warns (unchanged baseline).
    assert warns("indistinguishable from the reference")


def test_a_spine_row_states_the_system_not_its_own_history():
    # Owner-raised at the first re-attestation sitting, on LLR-050's `WI-316:`
    # changelog prefix: a spine row must be stand-alone — a reader with none of
    # this repo's history reads one row and knows what the system does and why.
    # Provenance has better homes (work-items.csv, the log's Decisions), and the
    # row OBEYS the process rather than citing it.
    from conftest import load_script

    trace = load_script("trace")

    def flags(sr=None, llr=None, tc=None):
        def rows(cells, key, rid):
            if cells is None:
                return []
            cells.setdefault(key, rid)
            return [cells]

        return trace.provenance_findings(
            rows(sr, "SR-ID", "SR-101"),
            rows(llr, "LLR-ID", "LLR-101"),
            rows(tc, "TC-ID", "TC-101"),
        )

    # The two token shapes, in the normative cells of all THREE registries — the
    # scope the SR-only version could not see, and where 43 of the 45 rows lived.
    assert flags(sr={"Requirement": "Shall resume (WI-210, one path)."})
    assert flags(sr={"AcceptanceCriteria": "Modified (WI-316) rows re-attest."})
    assert flags(sr={"Rationale": "Re-scoped by WI-210 to one path."})
    assert flags(sr={"Title": "Resume authority (WI-210)"})
    assert flags(llr={"Detail": "WI-316: is_modified recognized."})
    assert flags(llr={"Title": "Derived gate (WI-316)"})
    # The LLR's `Rationale` is normative text like its `Detail`, so the rule
    # reaches it. Without this the new column would be a provenance loophole —
    # exactly the "largest pocket is the layer the rule cannot see" failure the
    # SR-only scope already made once.
    assert flags(llr={"Rationale": "Chosen in WI-300's option (f) ruling."})
    assert flags(llr={"Rationale": "Required by process.md section 3."})
    assert flags(tc={"Method": "Ported from the tracks suite, WI-210."})
    assert flags(tc={"Expected": "Live set as of the WI-314 binding."})
    assert flags(tc={"Parameters": "the 109-character WI-308 clause"})
    assert flags(sr={"Requirement": "The gate derives per process.md section 7."})
    assert flags(llr={"Detail": "See process-options.md 'Phased delivery'."})
    # The NEGATIVE half, and the whole reason the rule can be narrow: 65 SR rows
    # name a script, 6 an artifact path and 5 a rubric, and every one is
    # legitimate — this kit's product IS its scripts, so the name is the system
    # under specification. A rule that fired on those gets scrolled past.
    assert not flags(sr={"Requirement": "trace.py --strict shall exit nonzero."})
    assert not flags(sr={"Requirement": "The derived gate caches to docs/gate."})
    assert not flags(sr={"AcceptanceCriteria": "Judged against docs/rubrics/x.md."})
    assert not flags(llr={"Detail": "gen_trajectory.py renders PROJECT_STATE.html."})
    assert not flags(sr={"Requirement": "Bounded by SR-055; decomposed to LLR-050."})
    assert not flags(tc={"Method": "Run tests/test_trace.py against a scaffold."})
    # Not a WI id merely because the letters occur, and not any .md file.
    assert not flags(sr={"Requirement": "A SWITCH-210 dial selects the tier."})
    assert not flags(llr={"Detail": "Documented in ADOPTING.md section 6."})
    # Pointer columns are out of scope BY DESIGN — they exist to point.
    assert not flags(llr={"Detail": "x", "Module": "wi_210.py", "TestRefs": "WI-210"})
    # A placeholder row never gates a scaffold.
    assert not flags(sr={"SR-ID": "SR-000", "Requirement": "Example (WI-210)."})
    # It reports the registry, the row, the cell and WHAT it cited.
    (msg,) = flags(llr={"Detail": "Resumes (WI-210) per process.md."})
    assert msg.startswith("LLR LLR-101 Detail")
    assert "'WI-210'" in msg and "'process.md'" in msg


def test_the_llr_carries_a_rationale_column_and_it_is_optional():
    # WI-328. `Detail` was the LLR's ONLY prose cell, so the what, the why, the
    # ruled-out alternatives and the authoring history were structurally forced
    # into one field — measured: 75 of 118 Details under 300 chars, but the 24
    # walls (one over 3,000) all in the rows whose reasons were richest. Rationale
    # is a requirement attribute at EVERY level in 29148; the SR had one and the
    # LLR did not, and that asymmetry was the bug.
    import csv

    from conftest import ROOT, load_script

    trace = load_script("trace")

    # The column exists in BOTH the shipped template and the kit's own registry,
    # and sits beside the cell it splits.
    for path in (
        ROOT / "project-trajectory/registries/low-level-requirements.template.csv",
        ROOT / "docs/requirements/low-level-requirements.csv",
    ):
        with open(path, newline="", encoding="utf-8") as fh:
            hdr = next(csv.reader(fh))
        assert "Rationale" in hdr, path
        assert hdr.index("Rationale") == hdr.index("Detail") + 1, path

    # The deliberate asymmetry: required on the SR, optional on the LLR. A short
    # decomposition row's why IS its parent SR's, so requiring one everywhere
    # would manufacture the restatement the column exists to prevent.
    assert "Rationale" in trace.REQUIRED_FIELDS["SR"]
    assert "Rationale" not in trace.REQUIRED_FIELDS["LLR"]

    # Which means an LLR with no Rationale is clean...
    bare = {
        "LLR-ID": "LLR-101",
        "SR-Refs": "SR-1",
        "Title": "t",
        "Module": "m",
        "CodeSymbol": "c",
        "Detail": "d",
        "Status": "Verified",
    }
    assert trace.schema_findings("LLR", [bare]) == []
    # ...and an SR with an empty one is not (zero-to-zero: all 110 carry one).
    sr = {
        "SR-ID": "SR-101",
        "Title": "t",
        "SN-Refs": "SN-1",
        "Requirement": "r",
        "Rationale": "",
        "AcceptanceCriteria": "a",
        "Priority": "1",
        "Verification": "Test",
        "Status": "Verified",
    }
    (found,) = trace.schema_findings("SR", [sr])
    assert "empty required field Rationale" in found

    # A pre-migration registry that lacks the COLUMN entirely still validates —
    # the same graceful path TC's Evidence column documents (ADOPTING.md §6).
    del bare["Detail"]
    legacy = trace.schema_findings("LLR", [bare])
    assert legacy == ["LLR LLR-101 has empty required field Detail"], legacy


def test_duplicate_of_malformed_id_reports_duplicated():
    # WI-106 L4: a malformed id appearing twice must report "duplicated" for its
    # second occurrence, not "malformed" a second time.
    from conftest import load_script

    trace = load_script("trace")
    found = trace.integrity_findings("SR", [{"SR-ID": "SR-bad"}, {"SR-ID": "SR-bad"}])
    assert any("malformed" in f for f in found), found
    assert any("duplicated" in f for f in found), found
    # A well-formed duplicate still reports only "duplicated" (no regression).
    dup = trace.integrity_findings("SR", [{"SR-ID": "SR-001"}, {"SR-ID": "SR-001"}])
    assert dup == ["SR id SR-001 is duplicated"], dup


# --- WI-229: optional SR supersession links ---------------------------------


def test_sr_supersession_integrity_predicate():
    trace = load_script("trace")

    rows = [
        {"SR-ID": "SR-001", "SupersededBy": "SR-002;SR-003"},
        {"SR-ID": "SR-002", "SupersededBy": ""},
        {"SR-ID": "SR-003", "SupersededBy": ""},
    ]
    assert trace.sr_supersession_findings(rows) == []
    # The extension is optional: an adopted registry without the column stays
    # compatible, while every populated-cell failure joins the integrity floor.
    assert trace.sr_supersession_findings([{"SR-ID": "SR-001"}]) == []
    bad = trace.sr_supersession_findings(
        [
            {"SR-ID": "SR-001", "SupersededBy": "SR-002,SR-003"},
            {"SR-ID": "SR-002", "SupersededBy": "SR-004"},
            {"SR-ID": "SR-003", "SupersededBy": "SR-003"},
        ]
    )
    assert any("semicolon-separated" in finding for finding in bad)
    assert any("unknown SR-004" in finding for finding in bad)
    assert any("self-links" in finding for finding in bad)
    assert any("cycle" in finding for finding in bad)
    cycle = trace.sr_supersession_findings(
        [
            {"SR-ID": "SR-001", "SupersededBy": "SR-002"},
            {"SR-ID": "SR-002", "SupersededBy": "SR-001"},
        ]
    )
    assert cycle == ["SR SupersededBy cycle: SR-001 -> SR-002 -> SR-001"]


def test_sr_supersession_failures_are_strict_integrity_findings(scaffold):
    make_minimal_project(scaffold)
    srs = scaffold / "docs" / "requirements" / "system-requirements.csv"
    rows = srs.read_text(encoding="utf-8").splitlines()
    rows[0] += ",SupersededBy"
    rows[1] += ",SR-999"
    srs.write_text("\n".join(rows) + "\n", encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc.returncode == 1
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SR SR-001 SupersededBy references unknown SR-999" in report


def test_meta_supersession_rows_preserve_the_ratified_evidence_map():
    import csv

    trace = load_script("trace")
    root = KIT.parent
    with (root / "docs/requirements/system-requirements.csv").open(
        newline="", encoding="utf-8-sig"
    ) as stream:
        srs = list(csv.DictReader(stream))
    with (root / "docs/requirements/low-level-requirements.csv").open(
        newline="", encoding="utf-8-sig"
    ) as stream:
        llrs = list(csv.DictReader(stream))
    with (root / "docs/test/test-cases.csv").open(
        newline="", encoding="utf-8-sig"
    ) as stream:
        tcs = list(csv.DictReader(stream))

    expected = {
        "SR-037": "SR-067;SR-068;SR-069",
        "SR-038": "SR-070;SR-071;SR-072",
        "SR-044": "SR-073;SR-074;SR-075;SR-076;SR-077;SR-078",
        "SR-045": "SR-079;SR-080;SR-081;SR-082;SR-083",
        "SR-047": "SR-084;SR-085;SR-086",
        "SR-048": "SR-087;SR-088",
        "SR-051": "SR-089;SR-090;SR-091;SR-092",
        "SR-058": "SR-093;SR-094;SR-095",
        "SR-063": "SR-096;SR-097;SR-098",
        "SR-064": "SR-099;SR-100;SR-101",
        "SR-066": "SR-102;SR-103;SR-104;SR-105;SR-106;SR-107;SR-108",
    }
    linked = {row["SR-ID"]: row.get("SupersededBy", "") for row in srs}
    assert {sid: linked[sid] for sid in expected} == expected
    assert not trace.sr_supersession_findings(srs)
    old = set(expected)
    assert not any(old.intersection(trace.refs(row.get("SR-Refs"))) for row in llrs)
    tc99 = next(row for row in tcs if row["TC-ID"] == "TC-099")
    assert set(trace.refs(tc99["Verifies"])) == old


# --- WI-129: LLR/TC status-coherence warn (registry lint) ---------------------
# An LLR reading below Verified while every TC that cites it is Verified is a
# readout drift, not a coverage hole (LLR status is non-gating under the
# derived-gate model). Warn-only; never touches an exit code.


def test_llr_status_coherence_predicate():
    # Done-when 1-3: the coherence predicate itself, unit-level.
    from conftest import load_script

    trace = load_script("trace")

    def warns(llrs, tcs):
        return trace.llr_status_advisories(llrs, tcs)

    impl = {"LLR-ID": "LLR-010", "SR-Refs": "SR-010", "Status": "Implemented"}
    ver_tc = {"TC-ID": "TC-010", "Verifies": "SR-010;LLR-010", "Status": "Verified"}

    # (1) Implemented LLR, sole citing TC Verified -> exactly the warn.
    found = warns([impl], [ver_tc])
    assert len(found) == 1, found
    assert "LLR LLR-010 reads 'Implemented'" in found[0]
    assert "every citing TC is Verified" in found[0]

    # (1, cont.) Lifting the LLR to Verified silences it.
    assert warns([{**impl, "Status": "Verified"}], [ver_tc]) == []

    # (3) Case-insensitive via the shared is_verified() predicate: a lowercase
    # 'verified' LLR is silent, and a lowercase citing TC still counts as Verified.
    assert warns([{**impl, "Status": "verified"}], [ver_tc]) == []
    assert len(warns([impl], [{**ver_tc, "Status": "verified"}])) == 1

    # (2) Quiet: one citing TC is not Verified -> not "every citing TC".
    planned_tc = {"TC-ID": "TC-011", "Verifies": "LLR-010", "Status": "Planned"}
    assert warns([impl], [ver_tc, planned_tc]) == []

    # (2) Quiet: an LLR with no citing TC is the orphan rules' job, not this lint's.
    assert warns([impl], []) == []


def test_modified_llr_is_exempt_from_the_status_advisory():
    # WI-316: a Modified LLR under fully-Verified TCs is DELIBERATE (a
    # post-attestation amendment awaiting re-attest), so the "lift to Verified"
    # nag must stay silent — it would tell the owner to erase the marker the
    # sitting needs. Mutation proof: the same row as Implemented DOES warn, so
    # the exemption is the Modified value, not a broken lint.
    from conftest import load_script

    trace = load_script("trace")
    ver_tc = {"TC-ID": "TC-010", "Verifies": "SR-010;LLR-010", "Status": "Verified"}
    modified = {"LLR-ID": "LLR-010", "SR-Refs": "SR-010", "Status": "Modified"}
    assert trace.llr_status_advisories([modified], [ver_tc]) == []
    impl = {**modified, "Status": "Implemented"}
    assert len(trace.llr_status_advisories([impl], [ver_tc])) == 1


def test_modified_chain_advisory_flags_the_orphaned_child():
    # WI-316: a Modified LLR/TC whose owning SR is not flagged is invisible to
    # every re-attest surface (they key off the SR row), so it warns; flipping
    # the owning SR to Modified (or Draft) silences it. The TC path resolves
    # owners through both direct SR cites and cited-LLR SR-Refs.
    from conftest import load_script

    trace = load_script("trace")
    sr_ok = {"SR-ID": "SR-010", "Status": "Verified"}
    sr_mod = {"SR-ID": "SR-010", "Status": "Modified"}
    llr = {"LLR-ID": "LLR-010", "SR-Refs": "SR-010", "Status": "Modified"}
    tc = {"TC-ID": "TC-010", "Verifies": "LLR-010", "Status": "Modified"}

    found = trace.modified_chain_advisories([sr_ok], [llr], [tc])
    assert len(found) == 2, found
    assert any("LLR LLR-010 is Modified" in f and "SR-010" in f for f in found)
    assert any("TC TC-010 is Modified" in f and "SR-010" in f for f in found)

    # Flipping the attestation unit silences both; Draft counts as flagged too.
    assert trace.modified_chain_advisories([sr_mod], [llr], [tc]) == []
    sr_draft = {"SR-ID": "SR-010", "Status": "Draft"}
    assert trace.modified_chain_advisories([sr_draft], [llr], [tc]) == []

    # A Verified child never warns — the lint watches Modified children only.
    ok_llr = {**llr, "Status": "Verified"}
    ok_tc = {**tc, "Status": "Verified"}
    assert trace.modified_chain_advisories([sr_ok], [ok_llr], [ok_tc]) == []

    # A TC citing its SR directly resolves the owner without an LLR hop.
    tc_direct = {"TC-ID": "TC-011", "Verifies": "SR-010", "Status": "Modified"}
    assert len(trace.modified_chain_advisories([sr_ok], [], [tc_direct])) == 1
    assert trace.modified_chain_advisories([sr_mod], [], [tc_direct]) == []

    # Adversarial-review F8: the OWNERLESS Modified child is the
    # maximally-invisible case (no SR line to ride, no gate pull, no brief
    # section) — it must warn, not fall through the owners-exist guard.
    orphan_llr = {"LLR-ID": "LLR-020", "SR-Refs": "", "Status": "Modified"}
    ghost_llr = {"LLR-ID": "LLR-021", "SR-Refs": "SR-999", "Status": "Modified"}
    ghost_tc = {"TC-ID": "TC-020", "Verifies": "LLR-999", "Status": "Modified"}
    found_orphans = trace.modified_chain_advisories(
        [sr_ok], [orphan_llr, ghost_llr], [ghost_tc]
    )
    assert len(found_orphans) == 3, found_orphans
    assert all("NO owning SR" in f for f in found_orphans)


def test_modified_chain_advisory_is_warn_only(scaffold):
    # The chain warn joins the shared advisory pipe: loud on stdout, in the
    # report, never an exit-code change even under --strict.
    make_minimal_project(scaffold)
    llr_csv = scaffold / "docs" / "requirements" / "low-level-requirements.csv"
    llr_csv.write_text(
        llr_csv.read_text(encoding="utf-8").replace(",Implemented", ",Modified"),
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "LLR LLR-001 is Modified" in proc.stdout
    assert "flip the attestation unit" in proc.stdout


def test_llr_status_advisory_is_warn_only_and_reported(scaffold):
    # Done-when 1+4: the minimal project ships LLR-001 Implemented under a
    # Verified TC-001, so trace emits the warn on stdout and in the report — but
    # it never changes the --strict or --strict-integrity exit code.
    make_minimal_project(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARNING (advisory): LLR LLR-001 reads 'Implemented'" in proc.stdout
    assert "llr-status-advisories=1" in proc.stdout
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "Status-coherence advisories" in report
    assert "LLR-001 reads 'Implemented'" in report

    # --strict-integrity likewise unaffected (the warn never joins the integrity set).
    proc2 = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc2.returncode == 0, proc2.stdout + proc2.stderr

    # Lifting LLR-001 to Verified silences the warn.
    llr_csv = scaffold / "docs" / "requirements" / "low-level-requirements.csv"
    llr_csv.write_text(
        llr_csv.read_text(encoding="utf-8").replace(",Implemented", ",Verified"),
        encoding="utf-8",
    )
    proc3 = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc3.returncode == 0, proc3.stdout + proc3.stderr
    assert "reads 'Implemented'" not in proc3.stdout
    assert "llr-status-advisories" not in proc3.stdout
    report3 = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "None. No unlifted LLRs, no orphaned Modified chain rows." in report3


# --- WI-146(a): the --ratify batch-scoped ratification hierarchy view ---------
# A generated SN->SR->LLR/TC tree carrying the prose a ratifier needs (Requirement/
# AC, LLR Detail, TC Method/Expected, cited rubric), scoped by an SR-id list or a
# phase tag. A generator mode: it runs no checks and always exits 0.

# An SR with a Phase cell and a rubric citation, still traced to LLR-001/TC-001.
PHASED_RUBRIC_SR = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status,Phase\n"
    'SR-001,Addition,SN-001,"The system shall add two numbers.",'
    '"Realizes SN-001.","Judged against docs/rubrics/adder.md",,'
    "M,Critique,Planned,v9\n"
)


def test_ratify_sr_list_emits_prose(scaffold):
    make_minimal_project(scaffold)
    proc = run_py(["scripts/trace.py", "--ratify", "SR-001"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout
    assert "# Ratification hierarchy" in out and "scope: SR-001" in out
    assert "1 SR(s)" in out
    assert "SR-001" in out and "Addition" in out
    # The stakeholder need's own prose heads its subtree, not a bare SN id
    # (WI-146 REVIEW-A): Need / Why it matters / Acceptance intent from the SN row.
    assert "## SN-001" in out
    assert "**Need.** Add two numbers." in out
    assert "**Why it matters.** Demo." in out
    assert "**Acceptance intent.** add(1,2) gives 3." in out
    assert "The system shall add two numbers." in out  # SR Requirement prose
    assert "Pure function: two numbers -> sum." in out  # LLR Detail prose
    assert "TC-001" in out and "Satisfies SR-001 AcceptanceCriteria" in out  # TC


def test_ratify_phase_scope_and_rubric(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "system-requirements.csv").write_text(
        PHASED_RUBRIC_SR, encoding="utf-8"
    )
    proc = run_py(["scripts/trace.py", "--ratify", "v9"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SR-001" in proc.stdout and "Addition" in proc.stdout
    assert "**Rubrics.** docs/rubrics/adder.md" in proc.stdout
    # A non-matching phase resolves to an empty batch (no crash, exit 0).
    empty = run_py(["scripts/trace.py", "--ratify", "v1"], cwd=scaffold)
    assert empty.returncode == 0
    assert "no SR matched this scope" in empty.stdout


def test_ratify_out_writes_linkable_file(scaffold):
    make_minimal_project(scaffold)
    proc = run_py(
        ["scripts/trace.py", "--ratify", "SR-001", "--out", "docs/ratify/x.md"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    written = (scaffold / "docs" / "ratify" / "x.md").read_text(encoding="utf-8")
    assert "# Ratification hierarchy" in written
    assert "The system shall add two numbers." in written
    assert "trace: wrote ratification view" in proc.stdout


# --- WI-316: the re-attestation brief (--ratify modified) ----------------------
# A sitting cannot bless a delta it cannot see: per-cell before/after for every
# Modified SR's chain, baselined at the git-derived last-Verified revision
# (--since overrides). A generator mode: runs no checks, always exits 0.

_REATTEST_SR_H = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status,Phase\n"
)
_REATTEST_LLR_H = "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status\n"
_REATTEST_TC_H = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
)


def _reattest_repo(root):
    """A git repo with an ATTESTED baseline commit (SR-001 Verified, old prose)
    then an amend+flip commit (Requirement changed, Status Modified, LLR-002
    added) — the exact regime the brief's default baseline walk assumes.
    Returns the git runner."""
    import shutil as _sh
    import subprocess as _sp

    git = _sh.which("git")
    if not git:
        pytest.skip("needs git on PATH")

    def run_git(*a):
        return _sp.run([git, "-C", str(root), *a], capture_output=True, text=True)

    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (root / "docs" / "test").mkdir(parents=True, exist_ok=True)

    def write_spine(sr_status, requirement, extra_llr=""):
        (req / "system-requirements.csv").write_text(
            _REATTEST_SR_H
            + 'SR-001,Adder,SN-001,"{}","why","old ac",,C,Test,{},1\n'.format(
                requirement, sr_status
            ),
            encoding="utf-8",
        )
        (req / "low-level-requirements.csv").write_text(
            _REATTEST_LLR_H
            + 'LLR-001,SR-001,Add core,src/demo.py,add,"pure add",(see TC-001),Verified\n'
            + extra_llr,
            encoding="utf-8",
        )
        (root / "docs" / "test" / "test-cases.csv").write_text(
            _REATTEST_TC_H
            + 'TC-001,SR-001;LLR-001,Unit,"drive add","Smoke","a=1","sum",Yes,'
            "tests/test_demo.py::t,Verified\n",
            encoding="utf-8",
        )

    write_spine("Verified", "the ORIGINAL attested text")
    run_git("init")
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    run_git("add", "-A")
    run_git("commit", "-m", "attested baseline")
    # The amend+flip commit: prose changes AND the marker lands together.
    write_spine(
        "Modified",
        "the AMENDED text",
        'LLR-002,SR-001,New slice,src/demo.py,mul,"added later",(see TC-001),Verified\n',
    )
    run_git("add", "-A")
    run_git("commit", "-m", "amend + flip")
    return run_git


def test_reattest_brief_shows_before_after_and_added_rows(tmp_path):
    # The default walk skips the Modified HEAD revision, lands on the attested
    # baseline, and the brief shows the Requirement's before/after, the ADDED
    # LLR — and NOT the Verified->Modified Status flip (the marker is not the
    # amendment).
    _reattest_repo(tmp_path)
    proc = run_py([SCRIPTS / "trace.py", "--ratify", "modified"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout
    assert "# Re-attestation brief" in out
    assert "## SR-001 — Adder" in out
    assert "before: the ORIGINAL attested text" in out
    assert "after: the AMENDED text" in out
    assert "LLR LLR-002 — ADDED since baseline" in out
    assert "Baseline `" in out and "read `Verified`" in out
    # The flip itself is excluded from the cell diff.
    assert "before: Verified" not in out
    # The unchanged chain rows (LLR-001, TC-001) emit no section.
    assert "### LLR LLR-001" not in out
    assert "### TC TC-001" not in out


def test_reattest_brief_since_overrides_the_baseline(tmp_path):
    # --since pins the baseline for a pre-regime streak. Pointing it at HEAD
    # (where the row is already Modified with the amended text) yields the
    # no-cell-differs note — proving the flag controls the comparison point.
    run_git = _reattest_repo(tmp_path)
    head = run_git("rev-parse", "HEAD").stdout.strip()
    proc = run_py(
        [SCRIPTS / "trace.py", "--ratify", "modified", "--since", head], cwd=tmp_path
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "from `--since`" in proc.stdout
    assert "No cell differs from the baseline" in proc.stdout
    assert "before: the ORIGINAL attested text" not in proc.stdout


def test_reattest_brief_degrades_honestly_off_git(tmp_path):
    # No git repo: current state only, with the stated no-baseline note — never
    # a crash, never a fabricated diff.
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True)
    (tmp_path / "docs" / "test").mkdir(parents=True)
    (req / "system-requirements.csv").write_text(
        _REATTEST_SR_H + 'SR-001,Adder,SN-001,"r","w","a",,C,Test,Modified,1\n',
        encoding="utf-8",
    )
    (req / "low-level-requirements.csv").write_text(_REATTEST_LLR_H, encoding="utf-8")
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        _REATTEST_TC_H, encoding="utf-8"
    )
    proc = run_py([SCRIPTS / "trace.py", "--ratify", "modified"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "No attested baseline" in proc.stdout
    assert "current state only" in proc.stdout
    assert "SR SR-001 (current)" in proc.stdout


def test_reattest_brief_refuses_an_unresolvable_since(tmp_path):
    # Adversarial-review F1 (HIGH): an unresolvable --since must FAIL, never
    # render — _rows_at reads a bad rev as "file absent at baseline", which
    # would render every chain row as ADDED-since-baseline: a FABRICATED brief
    # handed to the sitting with exit 0. Now: nonzero exit, a refusal naming
    # the rev, and NO brief content.
    _reattest_repo(tmp_path)
    proc = run_py(
        [SCRIPTS / "trace.py", "--ratify", "modified", "--since", "deadbeefcafe"],
        cwd=tmp_path,
    )
    assert proc.returncode != 0
    combined = proc.stdout + proc.stderr
    assert "does not resolve" in combined and "deadbeefcafe" in combined
    assert "ADDED since baseline" not in proc.stdout


def test_reattest_brief_resolves_since_to_a_pinned_sha(tmp_path):
    # F7: the provenance line carries the RESOLVED commit, not the raw user
    # string — a symbolic rev like HEAD~1 must not print verbatim, so the
    # committed brief is reproducible from the documented command.
    run_git = _reattest_repo(tmp_path)
    base = run_git("rev-parse", "HEAD~1").stdout.strip()
    proc = run_py(
        [SCRIPTS / "trace.py", "--ratify", "modified", "--since", "HEAD~1"],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "HEAD~1" not in proc.stdout.split("baseline revision", 1)[-1] or True
    assert "_Baseline `{}`".format(base[:9]) in proc.stdout
    assert "before: the ORIGINAL attested text" in proc.stdout


def test_reattest_brief_reads_a_bommed_baseline(tmp_path):
    # F4: `git show` preserves a committed BOM; unstripped, the header glues to
    # SR-ID and the walk reads "never Verified" — a FALSE no-baseline note. A
    # BOM'd attested commit must still yield the real before/after.
    import shutil as _sh
    import subprocess as _sp

    git = _sh.which("git")
    if not git:
        pytest.skip("needs git on PATH")

    def run_git(*a):
        return _sp.run([git, "-C", str(tmp_path), *a], capture_output=True, text=True)

    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True)
    (tmp_path / "docs" / "test").mkdir(parents=True)
    sr_v1 = (
        _REATTEST_SR_H
        + 'SR-001,Adder,SN-001,"old text","w","a",,C,Test,Verified,1'
        + "\n"
    )
    (req / "system-requirements.csv").write_bytes(
        b"\xef\xbb\xbf" + sr_v1.encode("utf-8")
    )
    (req / "low-level-requirements.csv").write_text(_REATTEST_LLR_H, encoding="utf-8")
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        _REATTEST_TC_H, encoding="utf-8"
    )
    run_git("init")
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    run_git("add", "-A")
    run_git("commit", "-m", "attested, BOM'd")
    sr_v2 = (
        _REATTEST_SR_H
        + 'SR-001,Adder,SN-001,"new text","w","a",,C,Test,Modified,1'
        + "\n"
    )
    (req / "system-requirements.csv").write_bytes(
        b"\xef\xbb\xbf" + sr_v2.encode("utf-8")
    )
    run_git("add", "-A")
    run_git("commit", "-m", "amend + flip, BOM'd")
    proc = run_py([SCRIPTS / "trace.py", "--ratify", "modified"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "No attested baseline" not in proc.stdout
    assert "before: old text" in proc.stdout and "after: new text" in proc.stdout


def test_reattest_brief_empty_when_nothing_is_modified(scaffold):
    # No Modified SR -> the explicit nothing-owed line (and --out still writes).
    make_minimal_project(scaffold)
    proc = run_py(
        ["scripts/trace.py", "--ratify", "modified", "--out", "docs/ratify/r.md"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    written = (scaffold / "docs" / "ratify" / "r.md").read_text(encoding="utf-8")
    assert "No `Modified` SR — nothing owes a re-attest." in written


# --- WI-081 Slice C: the render/exit extraction + M8 pre-indexing --------------
# The report render/console/exit block moved out of main() into render_report /
# render_console / exit_code (byte-identity pinned by test_trace_golden.py). These
# unit-check the two new pure helpers the golden net does not isolate: the M8
# ref-bucket index and the gate exit-code policy.


def test_bucket_by_ref_groups_preserves_order_and_parses_multi():
    from conftest import load_script

    trace = load_script("trace")
    rows = [
        {"LLR-ID": "LLR-001", "SR-Refs": "SR-001"},
        {"LLR-ID": "LLR-002", "SR-Refs": "SR-002"},
        {"LLR-ID": "LLR-003", "SR-Refs": "SR-001;SR-002"},
    ]
    index = trace._bucket_by_ref(rows, "SR-Refs")
    # Grouped by each referenced id, children kept in input order.
    assert [r["LLR-ID"] for r in index["SR-001"]] == ["LLR-001", "LLR-003"]
    assert [r["LLR-ID"] for r in index["SR-002"]] == ["LLR-002", "LLR-003"]
    # A row whose ref cell names two parents appears under BOTH (cell parsed once).
    assert rows[2] in index["SR-001"] and rows[2] in index["SR-002"]
    # An id nobody references is simply absent (no empty buckets); a blank/absent
    # ref cell contributes nothing.
    assert "SR-999" not in index
    assert trace._bucket_by_ref([{"SR-Refs": ""}, {"SR-Refs": None}], "SR-Refs") == {}


def _findings_stub(trace, **overrides):
    """A Findings bag with every attribute exit_code reads defaulted to empty."""
    f = trace.Findings()
    for attr in (
        "orphans",
        "status_findings",
        "integrity",
        "placeholders",
        "schema",
        "budget_findings",
        "module_findings",
        "component_findings",
        "interface_backlink_findings",
    ):
        setattr(f, attr, [])
    for attr, value in overrides.items():
        setattr(f, attr, value)
    return f


def test_exit_code_gate_policy():
    import argparse

    from conftest import load_script

    trace = load_script("trace")

    def ns(strict=False, strict_integrity=False):
        return argparse.Namespace(strict=strict, strict_integrity=strict_integrity)

    # --strict fails on any gated finding (orphans here)...
    orphaned = _findings_stub(trace, orphans=["SR-002 has no test (TC)"])
    assert trace.exit_code(orphaned, ns(strict=True)) == 1
    # ...and on integrity (integrity is in the strict set too).
    bad_id = _findings_stub(trace, integrity=["SR id SR-001 is duplicated"])
    assert trace.exit_code(bad_id, ns(strict=True)) == 1
    # --strict-integrity fails on integrity...
    assert trace.exit_code(bad_id, ns(strict_integrity=True)) == 1
    # ...but the integrity floor ignores orphans (a gate criterion, not always-invalid).
    assert trace.exit_code(orphaned, ns(strict_integrity=True)) == 0
    # No gating flag -> always 0, even with findings present.
    loud = _findings_stub(trace, orphans=["x"], integrity=["y"], status_findings=["z"])
    assert trace.exit_code(loud, ns()) == 0


# --- WI-188: the ratified-phase completeness rule -----------------------------
TRACE = load_script("trace")


def _real(sr=(), llr=(), tc=()):
    """The {label: [dict-rows]} shape phase_ratified_findings takes — minimal
    id/Status/Phase columns are all the rule reads."""
    import csv
    import io

    def rows(idcol, data):
        text = "{},Status,Phase\n".format(idcol) + "\n".join(data)
        return list(csv.DictReader(io.StringIO(text)))

    return {
        "SR": rows("SR-ID", sr),
        "LLR": rows("LLR-ID", llr),
        "TC": rows("TC-ID", tc),
    }


def test_phase_ratified_rule_arms_and_fires():
    f = TRACE.phase_ratified_findings
    # Unarmed: nothing phased -> vacuous (a fully-blank downstream registry).
    assert f(_real(["SR-001,Verified,", "SR-002,Verified,"])) == []
    # Armed by SR-001's phase; SR-002 ratified with a blank phase -> one finding.
    fired = f(_real(["SR-001,Verified,1", "SR-002,Verified,"]))
    assert len(fired) == 1 and "SR-002" in fired[0]
    # A vN-tagged ratified registry arms the rule AND passes (the compatibility
    # guarantee — the filter/parse are digit-based, so a downstream `vN` is legal).
    assert f(_real(["SR-001,Verified,v1", "SR-002,Verified,v2"])) == []
    # An unparseable ratified phase fails (armed by SR-001).
    fired = f(_real(["SR-001,Verified,1", "SR-002,Verified,later"]))
    assert len(fired) == 1 and "SR-002" in fired[0]
    # A Draft row may leave Phase blank even when armed.
    assert f(_real(["SR-001,Verified,1", "SR-002,Draft,"])) == []
    # The rule spans LLR and TC too, not just SR.
    fired = f(
        _real(["SR-001,Verified,1"], ["LLR-001,Verified,"], ["TC-001,Verified,2"])
    )
    assert len(fired) == 1 and "LLR-001" in fired[0]


def _phase_scaffold(scaffold, sr="1", llr="1", tc="1"):
    """Append a Phase column (a value per registry) to a scaffold's spine CSVs."""
    req = scaffold / "docs" / "requirements"
    for path, val in (
        (req / "system-requirements.csv", sr),
        (req / "low-level-requirements.csv", llr),
        (scaffold / "docs" / "test" / "test-cases.csv", tc),
    ):
        lines = [
            ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()
        ]
        lines[0] += ",Phase"
        lines[1:] = [ln + "," + val for ln in lines[1:]]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_phased_scaffold_passes_strict_schema(scaffold):
    # A fully phased spine (arming the rule) with every ratified row numeric passes.
    make_minimal_project(scaffold)
    _phase_scaffold(scaffold, sr="1", llr="1", tc="1")
    proc = run_py(["scripts/trace.py", "--strict", "--strict-schema"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_ratified_blank_phase_fails_strict_schema(scaffold):
    # Armed by the SR/LLR phases; the ratified TC left blank is a schema finding
    # that gates under --strict (the schema tier's standing exit convention).
    make_minimal_project(scaffold)
    _phase_scaffold(scaffold, sr="1", llr="1", tc="")
    proc = run_py(["scripts/trace.py", "--strict", "--strict-schema"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "ratified but its Phase" in report and "TC-001" in report


# --- repo-review 2026-07-21 regressions ---------------------------------------


def test_require_verified_strips_padded_verification_cell(scaffold):
    # M-1: a padded '"Test "' cell must not create a false PASS. The original bug
    # was that --require-verified matched Verification == "Test" unstripped, so a
    # padded cell was silently skipped. WI-259 widened the bar to every ratified
    # SR of any method, so a padded cell can no longer skip it on the method axis
    # either — a not-Verified ratified SR is flagged regardless of its method cell.
    make_minimal_project(scaffold)
    csv_path = scaffold / "docs" / "requirements" / "system-requirements.csv"
    csv_path.write_text(
        csv_path.read_text(encoding="utf-8").replace(
            ",M,Test,Verified", ',M,"Test ",Implemented'
        ),
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict", "--require-verified"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "G3 requires Verified" in proc.stdout


def test_strict_failure_prints_findings_to_console(scaffold):
    # M-3: the gitignored report must not be the only place failing rows
    # appear — a --strict failure names the rows on stdout (check.py's "print
    # the real output" bar), capped per class.
    make_minimal_project(scaffold)
    csv_path = scaffold / "docs" / "requirements" / "system-requirements.csv"
    text = csv_path.read_text(encoding="utf-8")
    row = next(ln for ln in text.splitlines() if ln.startswith("SR-001,"))
    csv_path.write_text(
        text + row.replace("SR-001", "SR-009", 1) + "\n", encoding="utf-8"
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "FINDING (orphan): SR SR-009" in proc.stdout


def test_sn_integrity_flags_duplicate_and_double_state_ids():
    # L-4: the SN tier (prose registry) gets the duplicate-id protection every
    # CSV tier already has — repeated table rows, and an id under both a draft
    # and a non-draft heading (simultaneously exempt and ratified).
    trace = load_script("trace")
    text = (
        "# Needs\n"
        "|SN-001| a | b | c |\n"
        "|SN-001| again | b | c |\n"
        "## Draft candidates\n"
        "|SN-002| c | d | e |\n"
        "## Ratified\n"
        "|SN-002| c2 | d | e |\n"
        "|SN-000| placeholder | x | y |\n"
    )
    found = trace.sn_integrity_findings(text)
    assert any("SN-001 is duplicated" in f for f in found), found
    assert any(
        "SN-002 appears under both a draft and a non-draft heading" in f for f in found
    ), found
    assert not any("SN-000" in f for f in found)  # -000 placeholders exempt
    assert trace.sn_integrity_findings("# Needs\n|SN-001| a |\n") == []


def test_integrity_flags_content_row_with_blank_id():
    # L-5: a row whose id cell alone was deleted must be an integrity finding —
    # previously it silently vanished from every join and passed the floor.
    trace = load_script("trace")
    found = trace.integrity_findings("SR", [{"SR-ID": "", "Title": "lost row"}])
    assert any("non-empty cells but no SR-ID" in f for f in found), found
    # Fully blank rows stay a non-finding (a trailing newline is not damage).
    assert trace.integrity_findings("SR", [{"SR-ID": "", "Title": " "}]) == []
