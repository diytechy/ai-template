"""trace.py: orphan detection and the --require-verified DevBar-Release criterion.

WI-277 split this module by behavior boundary. What stays here is the
scaffold-driven half: the strict/schema gates, the verification-category
buckets (Test / Attest / Demonstrated / Critique), the IF seam tier, the Draft
exemptions, and the generated report/HTML render. The pure in-process rule
decisions moved to tests/test_trace_rules.py, the git-backed re-attestation
brief to tests/test_trace_briefs.py.
"""

from conftest import (
    KIT,
    load_script,
    make_minimal_project,
    record_ids,
    run_py,
)

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
    # DevBar-Reqs's "every SR links >=1 SN" is machine-checked from the orphan sweep (not
    # only at DevBar-Release --strict-schema): an SR with an empty SN-Refs fails --strict
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
    record_ids(scaffold)
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
    # A v2 SR that is not yet Verified fails an unscoped DevBar-Release check, but a
    # --phase v1 closure defers it explicitly (and the deferral is reported).
    make_phased_project(scaffold)
    record_ids(scaffold)
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
        s[2]
        for s in check.steps(80, "full", "DevBar-Release", "v1")
        if s[0] == "traceability"
    )
    assert "--phase" in trace_cmd and "v1" in trace_cmd
    # No phase given -> no --phase flag; DevBar-Tests never carries --require-verified.
    trace_cmd = next(
        s[2]
        for s in check.steps(80, "full", "DevBar-Release")
        if s[0] == "traceability"
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
    record_ids(scaffold)


def test_attest_sr_is_llr_exempt_but_needs_tc(scaffold):
    # SR-002 (Attest) has no LLR yet is not an orphan; it still needs its TC.
    make_attest_project(scaffold)
    record_ids(scaffold)
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
    # Under --require-verified (DevBar-Release), an Attest SR marked Verified passes, and the
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
    record_ids(scaffold)


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

    # The headline widening (M-5): regress SR-002 to Implemented. sr_bar already
    # caps it at DevBar-Tests, but the OLD --require-verified (Verification=Test only)
    # silently PASSED it. The widened bar now flags it, naming the real method.
    csv_path = scaffold / "docs" / "requirements" / "system-requirements.csv"
    csv_path.write_text(
        DEMO_SRS.replace(",H,Analysis,Verified", ",H,Analysis,Implemented"),
        encoding="utf-8",
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict", "--require-verified"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "status-findings=1" in proc.stdout
    assert "Verification=Analysis but Status=Implemented" in proc.stdout
    assert "DevBar-Release requires Verified" in proc.stdout


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


ASPECT_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status,Aspect
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Verified,perf
"""


def test_aspect_column_is_schema_safe(scaffold):
    # Multi-module scoping groups a module's rows by the optional `Aspect` tag on
    # SR/TC (process.md §10). Like `Lifecycle`, `Aspect` is an extra column outside
    # REQUIRED_FIELDS, so a module-tagged registry passes the strictest schema
    # check with no downstream migration — the precedent that makes module-scoped
    # review a convention over existing columns rather than new machinery.
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "system-requirements.csv").write_text(
        ASPECT_SRS, encoding="utf-8"
    )
    proc = run_py(
        ["scripts/trace.py", "--strict", "--strict-schema", "--no-placeholders"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr


# --- Thread 35: Area is a first-class (still optional) SR column ---------------

ASPECT_MIXED_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status,Aspect
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Verified,perf
SR-002,Addition report,SN-001,"The system shall report the sum.","Realizes SN-001.","Sum is printed.",,M,Attest,Verified,
"""


def _template_keys(name, table, example_id):
    """The keys the shipped template's `-000` example row declares.

    Since the carrier cutover a template has no header line: the
    example row IS the schema, so "the shipped registry carries column X" is
    "the example row sets key X". ORDER is not asserted — TOML key order in a
    table carries no meaning, so an ordering assertion here would pin a fact the
    format does not have."""
    import tomllib

    text = (KIT / "registries" / name).read_text(encoding="utf-8")
    return tomllib.loads(text)[table][example_id]


def test_shipped_sr_template_carries_aspect_column():
    # The shipped schema declares Aspect — the ruled cross-cutting review
    # grouping (sitting-2 decision 10) that replaced the free-text Area column —
    # so a project records it without inventing its own extra column (the
    # Finance-Auditor field report), and the retired name is GONE rather than
    # left beside it.
    keys = _template_keys("system-requirements.template.toml", "requirement", "SR-000")
    assert "aspect" in keys
    assert "area" not in keys
    # ...and it is guidance an author can act on, not an empty placeholder — the
    # failure this replaces was a column present in name only. It must also name
    # the CLOSED value set, since an author cannot honour a vocabulary the
    # template does not state.
    assert keys["aspect"].strip()
    for value in (
        "process",
        "trajectory",
        "unattended-loop",
        "connectivity",
        "perf",
        "portability",
    ):
        assert value in keys["aspect"], value


def test_shipped_tc_template_carries_evidence_column():
    # Thread 51: the shipped TC schema carries Evidence so the concrete test
    # location has a first-class home and stops overloading Parameters (which
    # stays dimensional, the gen_cases grammar). Both must be declared, and
    # distinctly — the defect was one standing in for the other.
    keys = _template_keys("test-cases.template.toml", "test", "TC-000")
    assert "evidence" in keys and "parameters" in keys
    assert keys["evidence"] != keys["parameters"]
    assert "phase" in keys and "status" in keys


def test_aspect_values_yield_report_section(scaffold):
    # A registry with real Aspect values gets a per-aspect SR count in the
    # report — report-only: the run stays green, and blank cells count as
    # untagged (a row that is not cross-cutting carries no aspect, by the rule).
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    (req / "system-requirements.csv").write_text(ASPECT_MIXED_SRS, encoding="utf-8")
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
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "## SRs by aspect (report-only)" in report
    assert "- perf: 1" in report
    assert "- (no aspect): 1" in report


def test_out_of_vocabulary_aspect_is_a_schema_finding(scaffold):
    # THE CLOSED VOCABULARY, DRIVEN (sitting-2 decision 10, executed by the
    # WI-451 re-tier). The point of closing it is that the retired free-text
    # `Area` let 31 values accrete, 25 of which were a component by another
    # name. A value outside the ruled six is now a --strict-schema finding that
    # NAMES the row and the allowed set — a checker that only says "invalid"
    # teaches the next author nothing.
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "system-requirements.csv").write_text(
        ASPECT_SRS.replace(",perf\n", ",Parallel dispatch\n"), encoding="utf-8"
    )
    # Reported at the schema tier, and GATING only under --strict — the same
    # severity contract its Verification/Tier siblings carry.
    proc = run_py(["scripts/trace.py", "--strict-schema"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "schema-findings=1" in proc.stdout
    # ...and under --strict it GATES and the finding names the row, the
    # offending value and the allowed set.
    strict = run_py(["scripts/trace.py", "--strict", "--strict-schema"], cwd=scaffold)
    assert strict.returncode == 1, strict.stdout + strict.stderr
    assert "SR-001" in strict.stdout
    assert "Parallel dispatch" in strict.stdout
    assert "portability" in strict.stdout, "the allowed set must be reported"


def test_blank_aspect_is_never_a_schema_finding(scaffold):
    # The complement, and it is the ruled behaviour rather than a leniency: an
    # aspect is a REVIEW grouping, so a requirement that is not cross-cutting
    # carries none. "Portability's homelessness is not a defect" is the ruling's
    # own phrasing; a checker that demanded a value on every row would push
    # authors straight back to inventing component-shaped ones.
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "system-requirements.csv").write_text(
        ASPECT_SRS.replace(",perf\n", ",\n"), encoding="utf-8"
    )
    proc = run_py(["scripts/trace.py", "--strict", "--strict-schema"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "schema-findings=0" in proc.stdout


def test_no_aspect_values_no_report_section(scaffold):
    # The minimal project's registry has no Aspect column at all: the section
    # must be absent, not rendered empty (legacy CSVs see zero change).
    make_minimal_project(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SRs by aspect" not in report


def test_require_verified_flags_unverified_test_sr(scaffold):
    make_minimal_project(scaffold)
    csv_path = scaffold / "docs" / "requirements" / "system-requirements.csv"
    csv_path.write_text(
        csv_path.read_text(encoding="utf-8").replace(
            ",M,Test,Verified", ",M,Test,Implemented"
        ),
        encoding="utf-8",
    )
    # Without the flag: still a clean trace (status is a DevBar-Release concern).
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # With the flag: the unverified Test SR fails the gate.
    proc = run_py(["scripts/trace.py", "--strict", "--require-verified"], cwd=scaffold)
    assert proc.returncode == 1
    assert "status-findings=1" in proc.stdout
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "DevBar-Release requires Verified" in report


# --- WI-056: the IF-### interface-seam tier (process.md §8) ---------------------
# trace.py now reads the interface catalog (the SR-002-era gap): IF id integrity,
# the SR-Refs back-link (a --strict finding, like PB's), and a warn-only endpoint
# advisory. The full architecture-connectivity coverage lives in check_trajectory.

IF_HEADER = (
    "IF-ID,Direction,ThisProject,Counterpart,Contract,Req-Refs,Version,"
    "Stability,Status,Component,Notes\n"
)


def _ifs_toml(body):
    """The CSV bodies below as the TOML carrier the tier moved to at WI-443.

    Translated rather than rewritten at every call site for the reason
    test_trajectory_arch states: these tests are about back-links, endpoints and
    seam citations, and burying their subject under a schema migration would
    cost more than it proves. `Status` is DROPPED — the column retired with the
    ruling. The CSV carrier itself keeps a test of its own
    (`test_legacy_interfaces_csv_still_reads_through_the_carrier`)."""
    import csv as _csv
    import io as _io

    keys = [
        ("Direction", "direction"),
        ("ThisProject", "this_project"),
        ("Counterpart", "counterpart"),
        ("Contract", "contract"),
        ("Version", "version"),
        ("Stability", "approval"),
        ("Component", "component"),
        ("Notes", "notes"),
    ]
    out = []
    for r in _csv.DictReader(_io.StringIO(IF_HEADER + body)):
        rid = (r.get("IF-ID") or "").strip()
        if not rid:
            continue
        out.append("[interface.{}]".format(rid))
        out.append('signal = "discrete"')
        for col, key in keys:
            value = (r.get(col) or "").strip()
            if value:
                out.append('{} = """{}"""'.format(key, value))
        refs = [t for t in (r.get("Req-Refs") or "").split(";") if t.strip()]
        # `owner` is REQUIRED since the 2026-08-15 rework and every body below
        # names one requirement, so it seeds from the first ref — the same
        # mechanical rule the live registry's 94 single-ref rows were seeded
        # by. A test that wants a bad owner writes TOML directly.
        if refs:
            out.append('owner = "%s"' % refs[0].strip())
        if refs:
            out.append("req_refs = [{}]".format(", ".join('"%s"' % t for t in refs)))
        out.append("")
    return "\n".join(out) + "\n"


def _write_ifs(scaffold, body):
    (scaffold / "docs" / "requirements" / "interfaces.toml").write_text(
        _ifs_toml(body), encoding="utf-8"
    )
    record_ids(scaffold)


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


# --- WI-443 / OI-14 part B: the IF+CMP schema tier, WARN-FIRST -----------------
# The ruled sequencing is advisory-until-the-corpus-converges, so EVERY test in
# this section asserts the WARN TEXT and `returncode == 0` under `--strict`. A
# rule that reddens a gate here would be this slice overreaching its ruling; a
# rule that says nothing would be the state OI-14 spent three days measuring the
# drift of. Both halves are pinned, per rule.

CLEAN_IF = (
    'IF-001,Provides,src/demo,external:git,"reads the ref state",'
    "SR-001,v1,approved,Active,,\n"
)


def _warn_run(scaffold, body):
    """`--strict` over one IF row; returns stdout and asserts the exit is
    UNTOUCHED — the warn-first contract, checked at every call site rather than
    once, because 'advisory' is the property most easily lost by accident."""
    _write_ifs(scaffold, body)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def test_clean_if_row_trips_none_of_the_new_rules(scaffold):
    # The other half of every test below: a clean row must be SILENT, or a rule
    # that fires on everything would pass each fires-on-a-defect assertion.
    make_minimal_project(scaffold)
    out = _warn_run(scaffold, CLEAN_IF)
    for noise in (
        "Contract names WI-",
        "cites decision",
        "Contract argues",
        "ceiling 500",
        "has empty required field",
        "closed vocabulary",
        "resolves to no module, file or directory",
    ):
        assert noise not in out, noise


def test_signal_refuses_an_unknown_value_as_a_warn(scaffold):
    # The owner's ruled typing is a CLOSED vocabulary. Written straight to TOML:
    # `_write_ifs` supplies `signal = "discrete"`, and the point here is a value
    # the vocabulary does not contain.
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "interfaces.toml").write_text(
        "[interface.IF-001]\n"
        'direction = "Provides"\n'
        'this_project = "src/demo"\n'
        'counterpart = "git"\n'
        'contract = "reads the ref state"\n'
        'signal = "analog"\n'
        'req_refs = ["SR-001"]\n'
        'version = "v1"\n'
        'approval = "approved"\n',
        encoding="utf-8",
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr  # warn-first
    assert "IF IF-001 has Signal='analog'" in proc.stdout
    assert "not in the closed vocabulary" in proc.stdout
    assert "discrete, variable" in proc.stdout


def test_approval_refuses_an_unknown_value_as_a_warn(scaffold):
    # The successor of the `Stability=Provisional` case (WI-442). `Provisional`
    # was the real value four live rows carried while `Stability` was declared by
    # process.md §8 and validated by nothing; the vocabulary is closed now, and
    # the check has to bite on the SUCCESSOR column or the lesson was migrated
    # away rather than kept.
    make_minimal_project(scaffold)
    out = _warn_run(scaffold, CLEAN_IF.replace(",v1,approved,", ",v1,Provisional,"))
    assert "IF IF-001 has Approval='Provisional'" in out
    assert "approved, draft" in out


def test_cmp_state_refuses_an_unknown_value_as_a_warn(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "components.toml").write_text(
        '[component.CMP-001]\nname = "Core"\ncategory = "software"\n'
        'state = "in-flight"\n',
        encoding="utf-8",
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "CMP CMP-001 has State='in-flight'" in proc.stdout
    assert "not in the closed vocabulary" in proc.stdout


def test_missing_required_if_field_is_a_warn(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "interfaces.toml").write_text(
        "[interface.IF-001]\n"
        'direction = "Provides"\n'
        'this_project = "src/demo"\n'
        'counterpart = "git"\n'
        'contract = "reads the ref state"\n'
        'req_refs = ["SR-001"]\n'
        'version = "v1"\n'
        'approval = "approved"\n',  # no `signal`
        encoding="utf-8",
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "IF IF-001 has empty required field Signal" in proc.stdout


def test_work_item_id_in_contract_is_a_refuse_class_warn(scaffold):
    # ~24% of live rows today. A work-item id AGES, and a cancelled row's id
    # sitting in a Contract cell still reads as authority.
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold,
        CLEAN_IF.replace("reads the ref state", "reads the ref state (WI-374)"),
    )
    assert "IF IF-001 Contract names WI-374" in out
    assert "belongs in the log" in out


def test_decision_citation_in_contract_is_a_refuse_class_warn(scaffold):
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold,
        CLEAN_IF.replace("reads the ref state", "reads the ref state per D-9"),
    )
    assert "IF IF-001 Contract cites decision D-9" in out


def test_a_crossing_id_is_not_read_as_a_decision(scaffold):
    # The narrowing that a broader `<LETTER>-<n>` pattern got wrong: it read the
    # part-A data pack's own crossing ids (M-10) as rulings, which is a check
    # inventing a rule nobody wrote.
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold, CLEAN_IF.replace("reads the ref state", "the M-10 crossing")
    )
    assert "cites decision" not in out


def test_rationale_connective_in_contract_warns(scaffold):
    make_minimal_project(scaffold)
    for word in ("because", "rather than", "so that", "since"):
        out = _warn_run(
            scaffold,
            CLEAN_IF.replace("reads the ref state", "reads it " + word + " it must"),
        )
        assert "Contract argues ('{}')".format(word) in out, word
        assert "the Rationale column is its home" in out


def test_contract_over_the_length_ceiling_warns(scaffold):
    # 34 live rows exceed 500 characters; the longest is 968.
    make_minimal_project(scaffold)
    out = _warn_run(scaffold, CLEAN_IF.replace("reads the ref state", "x" * 501))
    assert "IF IF-001 Contract is 501 characters (ceiling 500)" in out
    # ...and 500 exactly is inside the ceiling (a boundary, not an off-by-one).
    out = _warn_run(scaffold, CLEAN_IF.replace("reads the ref state", "y" * 500))
    assert "ceiling 500" not in out


def test_untagged_endpoint_advisory_classifies_instead_of_staying_silent(scaffold):
    """The coverage fix the part-A data pack demands.

    45 of 113 live rows have an endpoint carrying no component tag, which makes
    `cross_component_findings` VACUOUS for them — and the containment rule that
    was assumed to cover them CANNOT, because it ranges over arch-map modules
    while these endpoints are data files, directories and external actors. Both
    checks were green and neither was saying anything. This advisory does not
    make them findings; it makes them VISIBLE, and it names individually only
    the endpoints that resolve to nothing, which are the only actionable ones."""
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold,
        'IF-001,Provides,src/demo,docs/status.md,"writes",SR-001,v1,Stable,Active,,\n'
        'IF-002,Provides,src/demo,external:downstream adopter,"cli",'
        "SR-001,v1,Stable,Active,,\n"
        'IF-003,Provides,src/demo,docs/gone/nowhere.md,"x",SR-001,v1,Stable,Active,,\n',
    )
    assert "IF endpoint coverage:" in out
    assert "1 resolve to a file or directory in the tree" in out
    assert "1 are marked `external:`" in out
    assert "1 resolve to nothing" in out
    # Only the unresolved one is named individually.
    assert "IF IF-003 Counterpart='docs/gone/nowhere.md' resolves to no module" in out
    assert "IF IF-001 Counterpart" not in out
    assert "IF IF-002 Counterpart" not in out


def test_semicolon_joined_endpoint_is_several_endpoints(scaffold):
    # A `;`-joined cell names SEVERAL endpoints; reading it as one reported a
    # real three-module seam (IF-097) as a dangling path. IF-097 KEPT this shape
    # at the 2026-08-15 rework rather than splitting into three rows: the three
    # consumers share ONE contract, and three rows would be three copies of it.
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold,
        'IF-001,Provides,src/demo,"docs/status.md;docs/log.md","x",'
        "SR-001,v1,Stable,Active,,\n",
    )
    assert "2 resolve to a file or directory in the tree" in out
    assert "resolve to nothing" in out and "0 resolve to nothing" in out


# --- 2026-08-15 interface rework, step 2: endpoint validation ------------------
# The rule the plan asks for: an endpoint that resolves to NOTHING and carries no
# external marker is a named warn — in EITHER endpoint column, path-shaped or
# not. Before this, the classifier guessed from spelling, so a name-shaped rot
# was silently "an external actor" and a real actor could never be distinguished
# from one.


def test_actor_shaped_endpoint_without_the_marker_is_now_named(scaffold):
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold,
        'IF-001,Provides,src/demo,agent CLI,"x",SR-001,v1,Stable,Active,,\n',
    )
    assert "IF IF-001 Counterpart='agent CLI' resolves to no module" in out
    assert "mark it `external:<actor>`" in out
    assert "0 are marked `external:`" in out


def test_the_external_marker_silences_it_and_is_counted(scaffold):
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold,
        'IF-001,Provides,src/demo,external:agent CLI,"x",SR-001,v1,Stable,Active,,\n',
    )
    assert "resolves to no module" not in out
    assert "1 are marked `external:`" in out


def test_a_bare_external_marker_names_nobody_and_still_warns(scaffold):
    # The one way the marker could be worse than the guess it replaced: a cell
    # that claims externality without saying what is on the far side.
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold, 'IF-001,Provides,src/demo,external:,"x",SR-001,v1,Stable,Active,,\n'
    )
    assert "IF IF-001 Counterpart='external:' resolves to no module" in out


def test_this_project_endpoint_is_validated_too_not_just_counterpart(scaffold):
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold,
        'IF-001,Provides,src/gone,docs/status.md,"x",SR-001,v1,Stable,Active,,\n',
    )
    assert "IF IF-001 ThisProject='src/gone' resolves to no module" in out


# --- 2026-08-15 interface rework, steps 5 + 7: the Owner cell and carriage -----
# Q1 (an owner may be a requirement OR a design row, exactly one) and Q3 (an IF
# may name another IF as the bundle carrying it, and that graph must be acyclic
# and bounded). Both warn-first: the owner cells were seeded mechanically and
# every multi-ref pick is a provisional judgement, so gating on them would gate
# on a guess.


def _if_row(**kw):
    base = {
        "direction": "Provides",
        "this_project": "src/demo",
        "counterpart": "external:git",
        "contract": "reads the ref state",
        "signal": "discrete",
        "req_refs": '["SR-001"]',
        "owner": '"SR-001"',
        "version": '"v1"',
        "approval": '"draft"',
    }
    base.update(kw)
    lines = ["[interface.IF-001]"]
    for k, v in base.items():
        lines.append("{} = {}".format(k, v if v.startswith(("[", '"')) else '"%s"' % v))
    return "\n".join(lines) + "\n"


def _toml_warn_run(scaffold, text):
    (scaffold / "docs" / "requirements" / "interfaces.toml").write_text(
        text, encoding="utf-8"
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr  # warn-first, always
    return proc.stdout


def test_owner_may_be_a_requirement_or_a_design_row(scaffold):
    # Q1's whole content: BOTH tiers are legitimate, because requirements and
    # design rows decompose the same thing at different levels.
    make_minimal_project(scaffold)
    for oid in ('"SR-001"', '"LLR-001"'):
        out = _toml_warn_run(scaffold, _if_row(owner=oid))
        assert "Owner" not in out, oid


def test_owner_naming_several_rows_is_a_warn(scaffold):
    make_minimal_project(scaffold)
    out = _toml_warn_run(scaffold, _if_row(owner='"SR-001;LLR-001"'))
    assert "names 2 owners" in out
    assert "exactly one row is answerable" in out


def test_owner_that_resolves_to_nothing_is_a_warn(scaffold):
    make_minimal_project(scaffold)
    assert "Owner references unknown SR-404" in _toml_warn_run(
        scaffold, _if_row(owner='"SR-404"')
    )
    assert "Owner references unknown LLR-404" in _toml_warn_run(
        scaffold, _if_row(owner='"LLR-404"')
    )


def test_owner_that_is_not_an_id_is_a_warn(scaffold):
    # `this_project` holds a module PATH, which is exactly why Q1 overturned
    # "derive the owner": a path cannot express "SR-012 owns this".
    make_minimal_project(scaffold)
    out = _toml_warn_run(scaffold, _if_row(owner='"src/demo"'))
    assert "is not an SR-### or LLR-### id" in out


def test_a_missing_owner_is_the_required_field_rule_not_a_second_one(scaffold):
    # One defect, one sentence: an empty cell is already "has empty required
    # field Owner", and saying it twice teaches the reader there are two rules.
    make_minimal_project(scaffold)
    text = _if_row()
    out = _toml_warn_run(scaffold, text.replace('owner = "SR-001"\n', ""))
    assert "IF IF-001 has empty required field Owner" in out
    assert "answerable" not in out


def test_carried_by_resolves_and_a_self_carrier_is_named_as_such(scaffold):
    make_minimal_project(scaffold)
    out = _toml_warn_run(scaffold, _if_row(carried_by='"IF-404"'))
    assert "IF IF-001 CarriedBy references unknown IF-404" in out
    out = _toml_warn_run(scaffold, _if_row(carried_by='"IF-001"'))
    assert "CarriedBy names itself — leave the cell empty" in out


def test_a_carriage_cycle_is_reported_once_per_row_on_it(scaffold):
    # The obligation Q3 created: `IF-A carried by IF-B carried by IF-A` is
    # representable the moment a link may point at its own tier.
    make_minimal_project(scaffold)
    text = _if_row(carried_by='"IF-002"') + _if_row().replace(
        "IF-001", "IF-002"
    ).replace('approval = "draft"\n', 'approval = "draft"\ncarried_by = "IF-001"\n')
    out = _toml_warn_run(scaffold, text)
    assert out.count("sits on a CarriedBy CYCLE") == 2


def test_carriage_deeper_than_the_bound_warns_and_two_is_clean(scaffold):
    make_minimal_project(scaffold)

    def chain(n):
        # IF-001 -> IF-002 -> ... -> IF-00n, the last carrying nothing.
        out = []
        for i in range(1, n + 1):
            row = _if_row().replace("IF-001", "IF-00%d" % i)
            if i < n:
                row = row.replace(
                    'approval = "draft"\n',
                    'approval = "draft"\ncarried_by = "IF-00%d"\n' % (i + 1),
                )
            out.append(row)
        return "".join(out)

    assert "carriers deep" not in _toml_warn_run(scaffold, chain(3))  # depth 2
    out = _toml_warn_run(scaffold, chain(4))  # depth 3
    assert "IF IF-001 is 3 carriers deep (bound 2)" in out
    assert "the bound is provisional" in out


def test_a_declared_absence_is_not_a_dangling_endpoint(scaffold):
    """`docs/declared-absences` gets its third reader.

    An endpoint naming a path the repo has DECLARED it does not carry is neither
    rot nor external — the layer is opt-in and switched off, and the row is
    honest about what the module would read if it were on. This repo's worked
    case is `docs/requirements/performance-budgets.csv`: check_perf's budgets
    registry, absent because process.md §9's perf layer is not enabled, with the
    reason already written down one directory up. Naming it would have been the
    checker demanding the repo delete a true statement."""
    make_minimal_project(scaffold)
    body = (
        'IF-001,Provides,src/demo,docs/off/budgets.csv,"x",SR-001,v1,Stable,Active,,\n'
    )
    out = _warn_run(scaffold, body)
    assert "IF IF-001 Counterpart='docs/off/budgets.csv' resolves to no module" in out
    (scaffold / "docs" / "declared-absences").write_text(
        "# declared\ndocs/off/budgets.csv — the perf layer is not enabled\n",
        encoding="utf-8",
    )
    out = _warn_run(scaffold, body)
    assert "resolves to no module" not in out
    # A line with no reason declares nothing — the file requires one.
    (scaffold / "docs" / "declared-absences").write_text(
        "docs/off/budgets.csv\n", encoding="utf-8"
    )
    assert "resolves to no module" in _warn_run(scaffold, body)


def test_direction_refuses_an_unknown_value_as_a_warn(scaffold):
    # Step 1: `Direction` was the one IF column whose vocabulary process.md §8
    # stated and nothing checked.
    make_minimal_project(scaffold)
    out = _warn_run(scaffold, CLEAN_IF.replace("IF-001,Provides,", "IF-001,Serves,"))
    assert "IF IF-001 has Direction='Serves'" in out
    assert "Consumes, Provides" in out


def test_if_placeholder_and_absent_are_free(scaffold):
    # The scaffold ships an inert IF-000 placeholder: no interface section, green.
    make_minimal_project(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "interfaces=" not in proc.stdout  # only the -000 placeholder
    # A truly absent registry is equally free.
    (scaffold / "docs" / "requirements" / "interfaces.toml").unlink()
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_legacy_interfaces_csv_still_reads_through_the_carrier(scaffold):
    # NEVER-BREAKING, WI-443: the tier's home is `interfaces.toml` now, but an
    # adopter who has not migrated still has `interfaces.csv` — and it must keep
    # loading, including a pre-WI-056 file with no Notes column (the missing cell
    # reads as empty) and the retired `Status` column (an unknown column is
    # simply carried, not a crash).
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    (req / "interfaces.toml").unlink()  # the CSV is the ONLY home, not a second
    legacy = (
        "IF-ID,Direction,ThisProject,Counterpart,Contract,Req-Refs,Version,"
        "Stability,Status,Component\n"
    )
    (req / "interfaces.csv").write_text(
        legacy + 'IF-001,Provides,src/demo,git,"x",SR-001,v1,Stable,Active,\n',
        encoding="utf-8",
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "interfaces=1 interface-findings=0" in proc.stdout


def test_both_interface_carriers_at_once_is_refused(scaffold):
    # THE HOUSE RULE (spine_carrier.resolve): two homes for one fact is the state
    # a migration exists to LEAVE, so it is refused rather than resolved by
    # precedence — a precedence rule lets a half-finished migration keep working
    # while quietly reading the stale half, and nobody finds out.
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    assert (req / "interfaces.toml").exists()
    (req / "interfaces.csv").write_text(
        "IF-ID,Direction,ThisProject,Counterpart,Contract,Req-Refs,Version,"
        "Stability,Component,Notes\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode != 0
    assert "REFUSED" in (proc.stdout + proc.stderr)
    assert "BOTH carriers" in (proc.stdout + proc.stderr)


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
    seam = [ln for ln in proc.stderr.splitlines() if "cited by no TC" in ln]
    assert len(seam) == 1 and "IF-002" in seam[0] and "IF-001" not in seam[0]


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
# The derived-gate model (docs/archive/specs/derived-gate-model.2026-07-20.md §3) lets a requirement
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
    record_ids(scaffold)
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
    record_ids(scaffold)
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
    record_ids(scaffold)
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
# An SN under a heading whose text contains "draft" is unratified (DevBar-Below) and exempt
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
    record_ids(scaffold)
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


def test_phase_ratified_rule_is_numeric_only():
    # Owner ruling 2026-08-01 (WI-402): once armed, a ratified Phase cell is a
    # BARE INTEGER — digits only, full cell. A prefixed label still digit-parses
    # (phase_num is untouched, so legacy labels keep arming/filtering/deriving —
    # grandfathering), but the literal joins (--phase/--ratify scope match,
    # check_trajectory's per-phase= vs [phase]-[gN] anchor join) miss it
    # SILENTLY, which is worse than a crash — so the live cell must be numeric.
    f = TRACE.phase_ratified_findings
    # A vN-tagged ratified registry now arms the rule AND fails it, per cell
    # (the pre-WI-402 vN-passes compatibility guarantee, deliberately retired).
    fired = f(_real(["SR-001,Verified,v1", "SR-002,Verified,v2"]))
    assert len(fired) == 2
    assert all("bare integer" in msg for msg in fired)
    # A single prefixed cell beside bare integers fires alone, naming the row.
    fired = f(_real(["SR-001,Verified,1", "SR-002,Verified,P1"]))
    assert len(fired) == 1 and "SR-002" in fired[0]
    # Bare integers stay green (surrounding whitespace is stripped, not judged).
    assert f(_real(["SR-001,Verified,1", "SR-002,Verified, 2 "])) == []
    # A Draft row is exempt even with a prefixed cell (its phase is not yet
    # ratified scope; it takes its bare number at ratification).
    assert f(_real(["SR-001,Verified,1", "SR-002,Draft,v9"])) == []


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


def test_ratified_prefixed_phase_fails_strict_schema(scaffold):
    # WI-402: a prefixed-but-parseable cell (P1) arms the rule (digit-extract
    # arming) and fails it — the silently-vacuous literal-join shape, now a
    # schema finding rather than a quiet disarm.
    make_minimal_project(scaffold)
    _phase_scaffold(scaffold, sr="1", llr="1", tc="P1")
    proc = run_py(["scripts/trace.py", "--strict", "--strict-schema"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "ratified but its Phase" in report and "TC-001" in report
    assert "bare integer" in report


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
    assert "DevBar-Release requires Verified" in proc.stdout


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


def test_both_component_carriers_at_once_is_refused(scaffold):
    # The same house rule, pinned for the OTHER registry WI-443 converted —
    # the adversarial round found the components half untested, and a refusal
    # held by one registry's test does not hold its sibling's.
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    assert (req / "components.toml").exists()
    (req / "components.csv").write_text(
        "CMP-ID,Name,Mission,State,Notes\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode != 0
    assert "REFUSED" in (proc.stdout + proc.stderr)
    assert "BOTH carriers" in (proc.stdout + proc.stderr)
