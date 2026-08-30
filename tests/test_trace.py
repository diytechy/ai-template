"""trace.py: orphan detection and the --require-verified DevStg-Impl criterion.

WI-277 split this module by behavior boundary. What stays here is the
scaffold-driven half: the strict/schema gates, the verification-category
buckets (Test / Attest / Demonstrated / Critique), the IF seam tier, the Drafted
exemptions, and the generated report/HTML render. The pure in-process rule
decisions moved to tests/test_trace_rules.py, the git-backed re-attestation
brief to tests/test_trace_briefs.py.
"""

import pytest
from conftest import (
    KIT,
    load_script,
    make_minimal_project,
    record_ids,
    run_py,
)

# SR-002 is a genuine (approved, non-Drafted) orphan: Status=Approved, so the
# derived-gate Drafted exemption (WI-089) does NOT apply and the decomposition
# rules still fire. A Drafted SR would be exempt — see the WI-089 section below.
ORPHAN_SR = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Approved
SR-002,Orphaned,SN-001,"The system shall do something untested.","Demo orphan.","n/a",,M,Test,Approved
"""


def test_happy_chain_is_orphan_free(scaffold):
    make_minimal_project(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "orphans=0" in proc.stdout


def test_verified_triple_prints_when_only_mechanized_is_nonzero(scaffold):
    # WI-466: the summary line's print guard used to read `(demonstrated_verified
    # or attested_verified)`, so a nonzero mechanized-only count — the common
    # case, and what a happy-chain minimal project produces (SR-001 is
    # Test/Approved) — silently hid the whole triple once the other two legs
    # drained to zero (re-tier v2 S3, log 2026-08-16e: SR-034/SR-036 were the
    # registry's only demonstrated-verified rows and both flipped Modified).
    make_minimal_project(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "verified-mechanized=1" in proc.stdout
    assert "verified-demonstrated=0" in proc.stdout
    assert "verified-attested=0" in proc.stdout


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
SR-001,Addition,,"The system shall add two numbers.","Rootless.","add(1,2) == 3",,M,Test,Approved
"""


def test_sr_with_no_sn_link_is_an_orphan(scaffold):
    # DevStg-Reqs's "every SR links >=1 SN" is machine-checked from the orphan sweep (not
    # only at DevStg-Impl --strict-schema): an SR with an empty SN-Refs fails --strict
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


# SR-002 is Status=Modified — a RETIRED value since D-9 step 7, and deliberately
# kept here as the mid-migration fixture. The phase scoping of --require-verified
# is what these tests exercise, so the row has to be one the bar FLAGS: a Drafted
# SR is exempt from --require-verified entirely (WI-089, a different axis), and
# `Approved`/`Founded` both pass, which leaves no LIVE value that reaches the bar.
# The cost is that this fixture also reds the enum floor, which
# `test_phase_scopes_require_verified` states rather than works around.
PHASED_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status,Phase
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Approved,v1
SR-002,Future thing,SN-001,"The system shall do a v2 thing.","Realizes SN-001 later.","v2 behavior",,S,Test,Modified,v2
"""

PHASED_LLRS = """LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status
LLR-001,SR-001,Pure adder,src/demo,add,"Pure function: two numbers -> sum.",(see TC),Approved
LLR-002,SR-002,Future part,src/future,todo,"Approved decomposition of the v2 SR.",(see TC),Approved
"""

PHASED_TCS = """TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status
TC-001,SR-001;LLR-001,Unit,call add and assert the sum,Smoke,"a=1; b=2","Satisfies SR-001 AcceptanceCriteria",Yes,Approved
TC-002,SR-002;LLR-002,Unit,planned v2 test,Full,,"Satisfies SR-002 AcceptanceCriteria",Yes,Drafted
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
    """A v2 SR that is not yet Approved fails an unscoped DevStg-Impl check; a
    `--phase v1` closure DEFERS it explicitly, and the deferral is reported.

    THE ASSERTIONS MOVED FROM EXIT CODES TO COUNTERS AT D-9 STEPS 7/8, and the
    reason is the fixture, not the property. `--require-verified`'s population
    is now unreachable-by-cell for a conformant repo — every live value either
    stands the bar down or passes it — so the only row that can drive this test
    is the mid-migration one PHASED_SRS carries, whose out-of-vocabulary Status
    ALSO reds the always-on integrity floor. The exit code therefore stays 1
    throughout and can no longer tell the deferred run from the scoped one.
    `status-findings=` / `phase-deferred=` can, and they are what the phase
    scoping actually moves."""
    make_phased_project(scaffold)
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict", "--require-verified"], cwd=scaffold)
    assert proc.returncode == 1
    assert "status-findings=1" in proc.stdout

    proc = run_py(
        ["scripts/trace.py", "--strict", "--require-verified", "--phase", "v1"],
        cwd=scaffold,
    )
    # DEFERRED: the bar stood down for the out-of-phase row...
    assert "status-findings=0" in proc.stdout, proc.stdout
    assert "phase-deferred=1" in proc.stdout
    # ...and the ONLY thing still failing is the enum floor, which is phase-blind
    # BY DESIGN: an unmigrated word is wrong at any stage, in any phase.
    assert "integrity=1" in proc.stdout
    assert "not in the closed vocabulary" in proc.stdout
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "Phase-deferred (explicitly out of scope)" in report
    assert "SR SR-002 (Phase=v2)" in report

    # Cumulative closure: once v2 is in scope, the unblessed SR is flagged again.
    proc = run_py(
        ["scripts/trace.py", "--strict", "--require-verified", "--phase", "v1,v2"],
        cwd=scaffold,
    )
    assert proc.returncode == 1
    assert "status-findings=1" in proc.stdout
    assert "phase-deferred=0" in proc.stdout or "phase-deferred=" not in proc.stdout


def test_phase_blind_orphan_rules_still_apply(scaffold):
    # Tagging an SR v2 never exempts it from decomposition/coverage: drop its
    # TC and the trace fails even under --phase v1.
    make_phased_project(scaffold)
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(
        PHASED_TCS.replace(
            "TC-002,SR-002;LLR-002,Unit,planned v2 test,Full,,"
            '"Satisfies SR-002 AcceptanceCriteria",Yes,Drafted\n',
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
        for s in check.steps(80, "full", "DevStg-Impl", "v1")
        if s[0] == "traceability"
    )
    assert "--phase" in trace_cmd and "v1" in trace_cmd
    # No phase given -> no --phase flag; DevStg-Tests never carries --require-verified.
    trace_cmd = next(
        s[2] for s in check.steps(80, "full", "DevStg-Impl") if s[0] == "traceability"
    )
    assert "--phase" not in trace_cmd


# --- WI-1.7: human-attestation verification kind (Attest) ---------------------

# An Attest SR: a named human's recorded judgment, no code to decompose (so
# LLR-exempt), but it still needs a TC that records who/when attested.
ATTEST_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Approved
SR-002,Theme mood fit,SN-001,"The main theme shall match the mood brief.","Subjective; no automated check.","Creative lead records pass against the brief.",,H,Attest,Approved
"""

ATTEST_TCS = """TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status
TC-001,SR-001;LLR-001,Unit,call add and assert the sum,Smoke,"a=1; b=2","Satisfies SR-001 AcceptanceCriteria",Yes,tests/test_demo.py::test_add_sr001,Approved
TC-002,SR-002,System,creative review of the theme,Release,"attested-by=A. Rivera; attested-on=2026-07-02","Recorded pass judgment for SR-002",No,,Approved
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
            '"Recorded pass judgment for SR-002",No,,Approved\n',
            "",
        ),
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SR SR-002 has no test (TC)" in report


def test_attest_verified_accepted_and_surfaced_distinctly(scaffold):
    # Under --require-verified (DevStg-Impl), an Attest SR marked Approved passes, and the
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
    assert "Approved SRs — attested (human, §4) | 1 |" in report
    assert "Approved SRs — mechanized (Test) | 1 |" in report
    assert "Approved SRs — demonstrated/observed | 0 |" in report


def test_attest_is_in_verification_vocabulary(scaffold):
    # --strict-schema must accept Attest (not reject it as out-of-vocabulary).
    make_attest_project(scaffold)
    proc = run_py(["scripts/trace.py", "--strict-schema"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SR-002 has Verification=" not in report  # no enum-violation finding


# --- WI-259: --require-verified is method-blind; the split has a third bucket ---

# A non-Test, non-Attest SR (Analysis here — representative of the
# Demonstration/Manual/Analysis/Inspection/Critique family): its Approved state
# rests on a human observing an outcome, not a runnable check. Analysis is
# LLR-exempt so it decomposes to a TC alone. SR-001 stays the mechanized (Test)
# control.
DEMO_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Approved
SR-002,Analyzed property,SN-001,"The system shall hold an analyzed property.","Judged by analysis, no runnable check.","An analyst records the property holds.",,H,Analysis,Approved
"""

DEMO_TCS = """TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status
TC-001,SR-001;LLR-001,Unit,call add and assert the sum,Smoke,"a=1; b=2","Satisfies SR-001 AcceptanceCriteria",Yes,tests/test_demo.py::test_add_sr001,Approved
TC-002,SR-002,System,analyze the property against the model,Release,"analyst=A. Rivera; analyzed-on=2026-07-21","Recorded analysis pass for SR-002",No,,Approved
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
    # M-5/WI-259: a non-Test, non-Attest Approved SR is reported in its own
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
    assert "Approved SRs — mechanized (Test) | 1 |" in report
    assert "Approved SRs — demonstrated/observed | 1 |" in report
    # Listed by id under demonstrated/observed — not miscounted as mechanized.
    assert "Demonstrated/observed" in report and "SR-002" in report

    # The headline widening (M-5): regress SR-002 to Modified. sr_bar already
    # caps it at DevStg-Tests, but the OLD --require-verified (Verification=Test only)
    # silently PASSED it. The widened bar now flags it, naming the real method.
    csv_path = scaffold / "docs" / "requirements" / "system-requirements.csv"
    csv_path.write_text(
        DEMO_SRS.replace(",H,Analysis,Approved", ",H,Analysis,Modified"),
        encoding="utf-8",
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict", "--require-verified"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "status-findings=1" in proc.stdout
    assert "Verification=Analysis but Status=Modified" in proc.stdout
    assert "DevStg-Impl requires Approved" in proc.stdout


# --- WI-068: the Critique verification value ----------------------------------

# A Critique SR: subjective acceptance judged by an independent critical eye
# against a rubric. Unlike Attest, its artifact is PRODUCED BY CODE (only the
# acceptance is perceptual), so it is NOT LLR-exempt.
CRITIQUE_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Approved
SR-002,Render realism,SN-001,"The rendered scene shall look realistic.","Subjective; judged by a critic against a rubric.","Critic judges the render against docs/rubrics/render.md anchors.",,S,Critique,Approved
"""

CRITIQUE_TCS = """TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status
TC-001,SR-001;LLR-001,Unit,call add and assert the sum,Smoke,"a=1; b=2","Satisfies SR-001 AcceptanceCriteria",Yes,tests/test_demo.py::test_add_sr001,Approved
TC-002,SR-002,System,critique the render against the rubric,Release,"rubric=docs/rubrics/render.md; artifact=render.png","Critic APPROVE per the rubric anchors",No,,Approved
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
    # Mermaid: the orphan (Approved) SR-002 gets the distinct class.
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
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Approved,Startup
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
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Approved,perf
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
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Approved,perf
SR-002,Addition report,SN-001,"The system shall report the sum.","Realizes SN-001.","Sum is printed.",,M,Attest,Approved,
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
        'LLR-001,SR-001,Pure adder,src/demo,add,"Two numbers -> sum.",(see TC),Approved\n',
        encoding="utf-8",
    )
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status\n"
        'TC-001,SR-001;LLR-001,Unit,call add,Smoke,"a=1; b=2",Sum,Yes,Approved\n'
        "TC-002,SR-002,Manual,read the report,Full,,Sum printed,No,Approved\n",
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


def test_require_verified_flags_an_UNMIGRATED_status(scaffold):
    """The bar's surviving population since D-9 steps 7/8, and it is smaller
    than it was — stated rather than discovered.

    Under the closed enum every LIVE value either stands the bar down
    (`Drafted`, pre-approval) or passes it (`Approved`, `Founded`), so a
    conformant repo can no longer reach this finding by cell. The case that
    remains is the one that matters most: a DOWNSTREAM repo mid-migration
    whose rows still read `Modified` (or `Implemented`, or anything else) must
    not pass a DevStg-Impl gate silently. So the fixture drives an
    out-of-vocabulary value deliberately, and asserts BOTH findings — this bar
    ("this row is not blessed") and the integrity floor ("this word is not in
    the vocabulary"). Two findings for one fault is the right count: they
    answer different questions, and only the second survives if the bar is
    never run.
    """
    make_minimal_project(scaffold)
    csv_path = scaffold / "docs" / "requirements" / "system-requirements.csv"
    csv_path.write_text(
        csv_path.read_text(encoding="utf-8").replace(
            ",M,Test,Approved", ",M,Test,Modified"
        ),
        encoding="utf-8",
    )
    # Without the flag: the ENUM floor already names it (D-9 correction C1 —
    # a retired word is wrong at any stage, so it does not wait for the top
    # bar). This used to read "still a clean trace"; the closure is what
    # changed, and it changed in the loud direction.
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "not in the closed vocabulary" in proc.stdout
    assert "status-findings=" not in proc.stdout  # the bar did not run
    # With the flag: the unblessed Test SR fails the DevStg-Impl bar too.
    proc = run_py(["scripts/trace.py", "--strict", "--require-verified"], cwd=scaffold)
    assert proc.returncode == 1
    assert "status-findings=1" in proc.stdout
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "DevStg-Impl requires Approved" in report


def test_require_verified_passes_EVERY_blessed_value(scaffold):
    """The mutation half, and the one that would have failed silently: D-9
    step 8 armed `Founded`, and a bar reading `is_approved` alone would have
    FLAGGED every row that reached the top rung — an arming that fails what it
    promotes. Both blessed values pass; `Drafted` stands the bar down."""
    make_minimal_project(scaffold)
    csv_path = scaffold / "docs" / "requirements" / "system-requirements.csv"
    original = csv_path.read_text(encoding="utf-8")
    for value in ("Approved", "Founded", "Drafted"):
        csv_path.write_text(
            original.replace(",M,Test,Approved", ",M,Test," + value),
            encoding="utf-8",
        )
        proc = run_py(
            ["scripts/trace.py", "--strict-integrity", "--require-verified"],
            cwd=scaffold,
        )
        assert "status-findings=0" in proc.stdout, value + proc.stdout
        assert "not in the closed vocabulary" not in proc.stdout, value


# --- WI-056: the IF-### interface-seam tier (process.md §8) ---------------------
# trace.py now reads the interface catalog (the SR-002-era gap): IF id integrity,
# the owner-SHAPE findings (a --strict finding, like PB's), and a warn-only
# reachability advisory. The full architecture-connectivity coverage lives in
# check_trajectory.

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

    # The fixture bodies keep the legacy CSV's column shape because that is what
    # the legacy carrier holds; the translation applies the renames the registry
    # took. OI-67 (ruled (a), 2026-08-29) is the latest: the row is ONE OWNER,
    # ITS CONSUMERS AND A TYPED STATEMENT, so `ThisProject` is now the `owner`
    # (the providing THING, in the one spelling `consumers` uses) and `Contract`
    # is the `data` summary. `Direction` and `Req-Refs` translate to NOTHING —
    # flow is the shape of the row, and the spine link is reached THROUGH the
    # owner rather than stated on it.
    keys = [
        ("ThisProject", "owner"),
        ("Contract", "data"),
        ("Version", "version"),
        ("Stability", "status"),
        ("Component", "component"),
        ("Notes", "notes"),
    ]
    out = []
    for r in _csv.DictReader(_io.StringIO(IF_HEADER + body)):
        rid = (r.get("IF-ID") or "").strip()
        if not rid:
            continue
        out.append("[interface.{}]".format(rid))
        # `channel` is REQUIRED and closed. The bodies below are module-to-module
        # seams, so `call` is the honest seed; a test about the vocabulary itself
        # writes TOML directly.
        out.append('channel = "call"')
        consumers = [
            c.strip() for c in (r.get("Counterpart") or "").split(";") if c.strip()
        ]
        out.append(
            "consumers = [{}]".format(
                ", ".join('"{}"'.format(c.replace('"', '\\"')) for c in consumers)
            )
        )
        for col, key in keys:
            value = (r.get(col) or "").strip()
            if value:
                out.append('{} = """{}"""'.format(key, value))
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
    # A clean seam: the owner is a module path LLR-001's `Module` names.
    _write_ifs(
        scaffold,
        'IF-001,Provides,src/demo,downstream adopter,"cli --help exits 0",'
        "SR-001,v1,Stable,Active,,\n",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "interfaces=1 interface-findings=0" in proc.stdout

    # An ID-SHAPED owner -> a --strict finding. This was the `Req-Refs` back-link
    # rule until OI-67 (ruled (a), 2026-08-29): the spine link is REACHED through
    # the owner now, so stating a requirement id in the cell that must hold the
    # providing THING is the wrong shape rather than a missing link.
    _write_ifs(scaffold, 'IF-001,Provides,SR-001,git,"pushes",,v1,Stable,Active,,\n')
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    assert "IF IF-001 Owner='SR-001' names a requirement or design id" in _report(
        scaffold
    )

    # And it is the SHAPE that is wrong, not the resolution: an id nothing
    # resolves reports the same finding, in the same words.
    _write_ifs(scaffold, 'IF-001,Provides,LLR-999,git,"pushes",,v1,Stable,Active,,\n')
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    assert "IF IF-001 Owner='LLR-999' names a requirement or design id" in _report(
        scaffold
    )

    # A malformed IF id joins the always-on integrity floor (--strict-integrity).
    _write_ifs(
        scaffold, 'IF-1x,Provides,src/demo,git,"pushes",SR-001,v1,Stable,Active,,\n'
    )
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc.returncode == 1
    assert "malformed" in _report(scaffold)


def test_if_endpoint_advisory_is_warn_only(scaffold):
    # A module-shaped owner that no design row's `Module` names and whose header
    # declares no `Implements:` line traces to no requirement — warn-only since
    # OI-67, because a file-owned or external-owned seam legitimately reaches no
    # design row and the class that does is a debt list, not a gate.
    make_minimal_project(scaffold)
    _write_ifs(
        scaffold, 'IF-001,Provides,src/nowhere,git,"x",SR-001,v1,Stable,Active,,\n'
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "this seam traces to no requirement" in proc.stdout
    assert "endpoint advisories" in _report(scaffold).lower()
    # The other half: the SAME body owned by the module LLR-001 names is silent,
    # so the advisory is the reachability judgement and not a rule that fires on
    # every row.
    _write_ifs(scaffold, 'IF-001,Provides,src/demo,git,"x",SR-001,v1,Stable,Active,,\n')
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "traces to no requirement" not in proc.stdout


def test_a_row_with_no_in_tree_endpoint_is_a_strict_finding(scaffold):
    # Adversarial review 2026-08-29, F2. An `external:` owner is exempt from
    # the reachability advisory (an external party has no design row) — and
    # that exemption used to be the row's LAST rule, so a row whose far side
    # was `external:` too owed nothing to anybody: not a design row, not a
    # `Contract IF-###:` body (the armed gate states our reading of an external
    # surface in the header of the kit module that FACES it, and here there is
    # none). A crossing between two external parties is `external.toml`'s row,
    # not this tier's.
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    all_external = (
        "[interface.IF-001]\n"
        'owner = "external:git"\n'
        'consumers = ["external:downstream adopter"]\n'
        'channel = "git"\n'
        'data = "the ref state"\n'
        'status = "Drafted"\n'
    )
    (req / "interfaces.toml").write_text(all_external, encoding="utf-8")
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "IF IF-001 has no in-tree endpoint" in _report(scaffold)

    # The other half: ONE kit module on the far side and the row is a seam of
    # this system again — the rule is "no endpoint in the tree", not "the owner
    # is external".
    (req / "interfaces.toml").write_text(
        all_external.replace(
            'consumers = ["external:downstream adopter"]', 'consumers = ["src/demo"]'
        ),
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "no in-tree endpoint" not in _report(scaffold)


# --- WI-443 / OI-14 part B: the IF+CMP schema tier, WARN-FIRST -----------------
# The ruled sequencing is advisory-until-the-corpus-converges, so EVERY test in
# this section asserts the WARN TEXT and `returncode == 0` under `--strict`. A
# rule that reddens a gate here would be this slice overreaching its ruling; a
# rule that says nothing would be the state OI-14 spent three days measuring the
# drift of. Both halves are pinned, per rule.

CLEAN_IF = (
    'IF-001,Provides,src/demo,external:git,"reads the ref state",'
    "SR-001,v1,Approved,Active,,\n"
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
        "Data names WI-",
        "cites decision",
        "Data argues",
        "ceiling 160",
        "has empty required field",
        "closed vocabulary",
        "resolves to no module, file or directory",
        "carries the retired",
    ):
        assert noise not in out, noise


def test_a_retired_cell_is_a_strict_finding(scaffold):
    # OI-67 slice 6, the armed gate's registry half: the five cells the ruling
    # took off the row are the wrong SHAPE wherever they still appear — a
    # `contract` (the definition has one home, the owner's header), a
    # `provider`/`req_refs`/`signal`/`signal_note` (derived or subsumed). Each
    # is named by key; the legacy summarizing warning is gone. ONE finding per
    # retired KEY, naming the rows that carry it (adversarial review
    # 2026-08-29, F7) — the registry is what carries a retired column, and a
    # per-row copy of one column's finding says the same thing N times.
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "interfaces.toml").write_text(
        "[interface.IF-001]\n"
        'owner = "src/demo"\n'
        'consumers = ["external:git"]\n'
        'channel = "call"\n'
        'contract = "the definition, in the wrong home"\n'
        'req_refs = ["SR-001"]\n'
        'version = "v1"\n'
        'status = "Drafted"\n',
        encoding="utf-8",
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    report = _report(scaffold)
    assert "carries the retired `contract` cell (set on IF-001)" in report
    assert "carries the retired `req_refs` cell (set on IF-001)" in report
    assert "legacy `contract` cell" not in proc.stdout
    # Delete them and the row is clean: the finding is the cell, not the row.
    (scaffold / "docs" / "requirements" / "interfaces.toml").write_text(
        "[interface.IF-001]\n"
        'owner = "src/demo"\n'
        'consumers = ["external:git"]\n'
        'channel = "call"\n'
        'version = "v1"\n'
        'status = "Drafted"\n',
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "carries the retired" not in _report(scaffold)


def test_a_retired_column_in_a_legacy_csv_header_is_a_strict_finding(scaffold):
    # THE HOLE THE PRESENCE RULE CLOSES (adversarial review 2026-08-29, F7).
    # The retired SHAPE is the key, not its value: under the legacy CSV carrier
    # a header column is present on EVERY row whether or not anyone filled it
    # in, so a value test read a retired column with empty cells as absent and
    # a registry could carry it indefinitely by keeping it blank. Reported ONCE
    # per column, naming the header — not once per row, which would say the
    # same thing as many times as the registry has rows.
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    (req / "interfaces.toml").unlink()  # the CSV is the ONLY home, not a second
    (req / "interfaces.csv").write_text(
        "IF-ID,Owner,Consumers,Channel,Data,Contract,Version,Status\n"
        "IF-001,src/demo,external:git,call,the ref state,,v1,Drafted\n"
        "IF-002,src/demo,external:git,call,the commit range,,v1,Drafted\n",
        encoding="utf-8",
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    report = _report(scaffold)
    assert (
        "carries the retired `contract` cell (the header column `Contract`)" in report
    )
    assert report.count("carries the retired") == 1, report
    # Drop the column and the registry is clean — the finding is the column.
    (req / "interfaces.csv").write_text(
        "IF-ID,Owner,Consumers,Channel,Data,Version,Status\n"
        "IF-001,src/demo,external:git,call,the ref state,v1,Drafted\n"
        "IF-002,src/demo,external:git,call,the commit range,v1,Drafted\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "carries the retired" not in _report(scaffold)


def test_an_empty_retired_cell_and_a_nested_sub_table_are_refused_by_the_carrier(
    scaffold,
):
    # The other two shapes the 2026-08-29 review named, PINNED HERE rather than
    # re-implemented in `interface_findings`: `spine_carrier.load` already
    # refuses both over every TOML registry it reads, this tier included, and a
    # second copy of a rule that already fires is exactly what the 0→A→B rule
    # forbids. `provider = ""` is the explicit-empty refusal (under this
    # carrier an unset cell is an ABSENT key); `[interface.IF-002.legacy]` is
    # the nested-table refusal (a cell that is itself a table is not a cell).
    # Both land as a REFUSAL rather than a report — the fail-closed half of the
    # carrier fork — so `--strict` reds either way.
    make_minimal_project(scaffold)
    ifs = scaffold / "docs" / "requirements" / "interfaces.toml"
    clean = (
        "[interface.IF-001]\n"
        'owner = "src/demo"\n'
        'consumers = ["external:git"]\n'
        'channel = "call"\n'
        'data = "the ref state"\n'
        'status = "Drafted"\n'
    )
    ifs.write_text(clean, encoding="utf-8")
    record_ids(scaffold)
    assert run_py(["scripts/trace.py", "--strict"], cwd=scaffold).returncode == 0

    ifs.write_text(clean + 'provider = ""\n', encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "IF-001 sets `provider` to an EMPTY STRING" in proc.stdout + proc.stderr

    ifs.write_text(
        clean + '\n[interface.IF-001.legacy]\ncontract = "an old body"\n',
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "IF-001.legacy is a TABLE, not a cell" in proc.stdout + proc.stderr


def test_channel_refuses_an_unknown_value_as_a_warn(scaffold):
    # The owner's ruled typing is a CLOSED vocabulary — `Channel` since OI-67,
    # which subsumed `Signal`'s discrete/variable pair (`exit-code` and `env` are
    # the discrete kinds; the rest are unbounded). Written straight to TOML:
    # `_write_ifs` supplies `channel = "call"`, and the point here is a value the
    # vocabulary does not contain.
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "interfaces.toml").write_text(
        "[interface.IF-001]\n"
        'owner = "src/demo"\n'
        'consumers = ["external:git"]\n'
        'channel = "analog"\n'
        'data = "reads the ref state"\n'
        'version = "v1"\n'
        'status = "Approved"\n',
        encoding="utf-8",
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr  # warn-first
    assert "IF IF-001 has Channel='analog'" in proc.stdout
    assert "not in the closed vocabulary" in proc.stdout
    assert "bytes, call, cli, env, exit-code, file, git, stdout" in proc.stdout


def test_approval_refuses_an_unknown_value_as_a_warn(scaffold):
    # The successor of the `Stability=Provisional` case (WI-442). `Provisional`
    # was the real value four live rows carried while `Stability` was declared by
    # process.md §8 and validated by nothing; the vocabulary is closed now, and
    # the check has to bite on the SUCCESSOR column or the lesson was migrated
    # away rather than kept.
    make_minimal_project(scaffold)
    out = _warn_run(scaffold, CLEAN_IF.replace(",v1,Approved,", ",v1,Provisional,"))
    assert "IF IF-001 has Status='Provisional'" in out
    assert "Approved, Drafted" in out


def test_cmp_state_refuses_an_unknown_value_as_a_warn(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "components.toml").write_text(
        '[component.CMP-001]\nname = "Core"\ncategory = "software"\n'
        'status = "in-flight"\n',
        encoding="utf-8",
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "CMP CMP-001 has Status='in-flight'" in proc.stdout
    assert "not in the closed vocabulary" in proc.stdout


# --- the SN tier's Status vocabulary (the enum floor's fourth tier) -----------
# `ENUM_FIELDS["SN"]["Status"]` was DECLARED while analyze()'s enum fold ran over
# `{"SR", "LLR", "TC"}` only, so a need could carry any word at all and no bar
# said so. These two are the always-on floor's fires-on-a-defect / silent-on-a-
# clean-row pair, run through the CLI like every other vocabulary case above.
NEEDS_TOML = """[need.SN-001]
status = "{status}"
priority = "M"
need = "Add two numbers."
why = "Demo."
acceptance = "add(1,2) gives 3."
"""


def _needs_on_toml(scaffold, status):
    """Re-home the scaffold's need tier on the TOML carrier at one status.

    The markdown file is REMOVED, not left beside it: `spine_carrier.resolve`
    refuses both homes at once (and that refusal is the rule working), which is
    the same reason `use_legacy_spine_carrier` drops the home it is not using."""
    req = scaffold / "docs" / "requirements"
    (req / "stakeholder-needs.md").unlink(missing_ok=True)
    (req / "stakeholder-needs.toml").write_text(
        NEEDS_TOML.format(status=status), encoding="utf-8"
    )


def test_sn_status_outside_the_closed_vocabulary_is_an_integrity_finding(scaffold):
    make_minimal_project(scaffold)
    _needs_on_toml(scaffold, "Bananas")
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert "SN SN-001 has Status='Bananas'" in proc.stdout
    assert "not in the closed vocabulary" in proc.stdout
    # INTEGRITY-class, so it gates at the always-on floor rather than waiting for
    # --strict-schema at DevStg-Impl (the D-9 correction C1 routing).
    assert proc.returncode == 1, proc.stdout + proc.stderr


def test_every_declared_sn_status_leaves_the_enum_floor_silent(scaffold):
    # The other half: a rule that fired on everything would pass the assertions
    # above. All three live vocabulary words, each on its own scaffold run.
    make_minimal_project(scaffold)
    for status in ("Drafted", "Approved", "Founded"):
        _needs_on_toml(scaffold, status)
        proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
        assert "closed vocabulary" not in proc.stdout, status
        assert proc.returncode == 0, status + proc.stdout + proc.stderr


def test_missing_required_if_field_is_a_warn(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "interfaces.toml").write_text(
        "[interface.IF-001]\n"
        'owner = "src/demo"\n'
        'consumers = ["external:git"]\n'
        'data = "reads the ref state"\n'
        'version = "v1"\n'
        'status = "Approved"\n',  # no `channel`
        encoding="utf-8",
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "IF IF-001 has empty required field Channel" in proc.stdout


def test_work_item_id_in_data_is_a_refuse_class_warn(scaffold):
    # ~24% of live rows carried one when the rule was written. A work-item id
    # AGES, and a cancelled row's id sitting in the cell still reads as
    # authority. The four form rules moved from `Contract` to `Data` unchanged
    # at OI-67 — the cell they police is the row's typed statement now.
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold,
        CLEAN_IF.replace("reads the ref state", "reads the ref state (WI-374)"),
    )
    assert "IF IF-001 Data names WI-374" in out
    assert "belongs in the log" in out


def test_decision_citation_in_data_is_a_refuse_class_warn(scaffold):
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold,
        CLEAN_IF.replace("reads the ref state", "reads the ref state per D-9"),
    )
    assert "IF IF-001 Data cites decision D-9" in out


def test_a_crossing_id_is_not_read_as_a_decision(scaffold):
    # The narrowing that a broader `<LETTER>-<n>` pattern got wrong: it read the
    # part-A data pack's own crossing ids (M-10) as rulings, which is a check
    # inventing a rule nobody wrote.
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold, CLEAN_IF.replace("reads the ref state", "the M-10 crossing")
    )
    assert "cites decision" not in out


def test_rationale_connective_in_data_warns(scaffold):
    make_minimal_project(scaffold)
    for word in ("because", "rather than", "so that", "since"):
        out = _warn_run(
            scaffold,
            CLEAN_IF.replace("reads the ref state", "reads it " + word + " it must"),
        )
        assert "Data argues ('{}')".format(word) in out, word
        assert "move the ARGUMENT to the Rationale column" in out
        # The CITATION half now points at the log, not at Rationale: the owner
        # ruling forbids a citation frame in any living registry cell, so the
        # advice that used to send it next door would send it somewhere it is
        # equally forbidden.
        assert "any citation inside it to the log" in out


def test_data_over_the_length_ceiling_warns(scaffold):
    # The ceiling came DOWN from 500 to 160 with the cell (OI-67): `Data` is the
    # alphabet or a one-clause schema pointer, and the definition it used to hold
    # lives in the owner's `Contract IF-###:` body.
    make_minimal_project(scaffold)
    out = _warn_run(scaffold, CLEAN_IF.replace("reads the ref state", "x" * 161))
    assert "IF IF-001 Data is 161 characters (ceiling 160)" in out
    # ...and 160 exactly is inside the ceiling (a boundary, not an off-by-one).
    out = _warn_run(scaffold, CLEAN_IF.replace("reads the ref state", "y" * 160))
    assert "ceiling 160" not in out


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
    assert "IF IF-003 Consumers='docs/gone/nowhere.md' resolves to no module" in out
    assert "IF IF-001 Consumers" not in out
    assert "IF IF-002 Consumers" not in out


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
    assert "IF IF-001 Consumers='agent CLI' resolves to no module" in out
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
    assert "IF IF-001 Consumers='external:' resolves to no module" in out


def test_the_owner_endpoint_is_validated_too_not_just_consumers(scaffold):
    make_minimal_project(scaffold)
    out = _warn_run(
        scaffold,
        'IF-001,Provides,src/gone,docs/status.md,"x",SR-001,v1,Stable,Active,,\n',
    )
    assert "IF IF-001 Owner='src/gone' resolves to no module" in out


# --- OI-67 ruled (a): the Owner cell is the providing THING, plus carriage -----
# The owner is one endpoint in the one spelling `consumers` uses — a module path,
# a file or directory path, or an `external:` party — and the SHAPE is a --strict
# finding, because an id-typed owner and a path-typed provider were the same fact
# in two spellings and only one of them survived. Q3's carriage rules (an IF may
# name another IF as the bundle carrying it, and that graph must be acyclic and
# bounded) stay warn-first beside it: the bound is provisional.


def _if_row(**kw):
    base = {
        "owner": "src/demo",
        "consumers": '["external:git"]',
        "channel": "call",
        "data": "reads the ref state",
        "version": '"v1"',
        "status": '"Drafted"',
    }
    base.update(kw)
    lines = ["[interface.IF-001]"]
    for k, v in base.items():
        lines.append("{} = {}".format(k, v if v.startswith(("[", '"')) else '"%s"' % v))
    return "\n".join(lines) + "\n"


def _toml_write(scaffold, text):
    (scaffold / "docs" / "requirements" / "interfaces.toml").write_text(
        text, encoding="utf-8"
    )
    record_ids(scaffold)


def _toml_warn_run(scaffold, text):
    _toml_write(scaffold, text)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr  # warn-first, always
    return proc.stdout


def _toml_finding_run(scaffold, text):
    """`--strict` over one IF row that is expected to FAIL, returning stdout.

    The owner-shape rules are the one arm of this tier that GATES, so their call
    sites assert the nonzero exit as loudly as the warn-first sites assert the
    zero one — a finding that stopped joining the failure set would otherwise
    read as a passing test."""
    _toml_write(scaffold, text)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    return proc.stdout


def test_an_owner_that_names_a_requirement_or_design_row_is_a_finding(scaffold):
    # The shape OI-67 retired, and BOTH tiers are wrong for the same reason: a
    # design row's module IS the providing thing, so naming the row instead of
    # the thing states a derivable fact in a second spelling.
    make_minimal_project(scaffold)
    for oid in ('"SR-001"', '"LLR-001"'):
        out = _toml_finding_run(scaffold, _if_row(owner=oid))
        assert "names a requirement or design id" in out, oid
        assert "the owner is the providing THING" in out, oid


def test_an_owner_that_is_a_path_is_the_clean_shape(scaffold):
    # The other half, and the one that keeps the rule from firing on everything:
    # a module path, a file path and a marked external party are the three
    # legitimate spellings, and none of them reports.
    make_minimal_project(scaffold)
    for owner, extra in (
        ("src/demo", {}),
        ("docs/status.md", {}),
        # An `external:` owner needs a kit module on its FAR SIDE to be a seam
        # of this system at all — the default `consumers` cell is itself
        # `external:git`, which is
        # `test_a_row_with_no_in_tree_endpoint_is_a_strict_finding`'s subject
        # and not this test's. The owner spelling is what is under test here.
        ("external:git", {"consumers": '["src/demo"]'}),
    ):
        out = _toml_warn_run(scaffold, _if_row(owner='"%s"' % owner, **extra))
        assert "Owner=" not in out, owner
        assert "no in-tree endpoint" not in out, owner


def test_an_owner_naming_several_endpoints_is_a_finding(scaffold):
    # One row has ONE owner: a `;`-joined cell is a bundle wearing one row's
    # clothes, and the ruling splits it or declares a carrier on `carried_by`.
    make_minimal_project(scaffold)
    out = _toml_finding_run(scaffold, _if_row(owner='"src/demo;src/helper"'))
    assert "names 2 endpoints" in out
    assert "one row has ONE owner" in out


def test_the_far_side_names_the_direction_and_both_or_neither_is_a_warn(scaffold):
    # THE FAR SIDE IS EXACTLY ONE OF `requestors` / `consumers` (OI-67, the
    # owner's own addition): the key name is the direction. Both or neither is
    # reported WARN-FIRST — the same tier as an empty required cell, because a
    # row with no far side is incomplete (an adopter mid-migration), where an
    # id-shaped owner is wrong (the retired meaning, stated) and gates.
    make_minimal_project(scaffold)
    consumers_line = 'consumers = ["external:git"]\n'
    neither = _if_row().replace(consumers_line, "")
    out = _toml_warn_run(scaffold, neither)
    assert "IF IF-001 names neither Requestors and Consumers" in out
    both = _if_row(requestors='["src/helper"]')
    out = _toml_warn_run(scaffold, both)
    assert "IF IF-001 names both Requestors and Consumers" in out
    # ...and a requestors-only row is the clean shape, exactly as consumers-only is.
    only = _if_row(requestors='["src/helper"]').replace(consumers_line, "")
    assert "Requestors and Consumers" not in _toml_warn_run(scaffold, only)


def test_a_missing_owner_is_the_required_field_rule_not_a_second_one(scaffold):
    # One defect, one sentence: an empty cell is already "has empty required
    # field Owner", and saying it twice teaches the reader there are two rules.
    make_minimal_project(scaffold)
    text = _if_row()
    out = _toml_warn_run(scaffold, text.replace('owner = "src/demo"\n', ""))
    assert "IF IF-001 has empty required field Owner" in out
    assert "Owner=" not in out


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
    ).replace('status = "Drafted"\n', 'status = "Drafted"\ncarried_by = "IF-001"\n')
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
                    'status = "Drafted"\n',
                    'status = "Drafted"\ncarried_by = "IF-00%d"\n' % (i + 1),
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
    case is `docs/requirements/assets.csv`: the off-spine asset registry, absent
    because a meta-repo ships no binary assets, with the reason already written
    down one directory up. Naming it would have been the checker demanding the
    repo delete a true statement.

    RE-POINTED 2026-08-20 (the batch review's MINOR-19): the example was
    `performance-budgets.csv` until WI-481 seeded that registry and deleted its
    declared-absence line, which left this docstring teaching a worked case that
    had become live. The scenario below uses a synthetic path, so only the
    example named in words moved."""
    make_minimal_project(scaffold)
    body = (
        'IF-001,Provides,src/demo,docs/off/budgets.csv,"x",SR-001,v1,Stable,Active,,\n'
    )
    out = _warn_run(scaffold, body)
    assert "IF IF-001 Consumers='docs/off/budgets.csv' resolves to no module" in out
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


def test_the_retired_direction_column_closes_no_vocabulary_here(scaffold):
    # Step 1 closed `Direction`'s vocabulary — the one IF column process.md §8
    # stated and nothing checked. WI-455 then retired the column itself (OI-60
    # ruled (a)): flow is the SHAPE of the row, owner -> consumers. The
    # vocabulary must go WITH it, or the tier keeps refusing values for a cell
    # no row is allowed to carry — and the enum survives, correctly, on the
    # BOUNDARY tier, which is the collision the shed closed.
    make_minimal_project(scaffold)
    out = _warn_run(scaffold, CLEAN_IF.replace("IF-001,Provides,", "IF-001,Serves,"))
    assert "Direction" not in out
    assert "Consumes, Provides" not in out


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
        "IF-ID,Direction,ThisProject,Counterpart,Version,Stability,Status,Component\n"
    )
    # The RETIRED columns are gone from the header, and that is the rule rather
    # than tidiness: since the presence fix (2026-08-29) a retired column is a
    # strict finding wherever it is DECLARED, and a CSV header declares it on
    # every row (test_a_retired_column_in_a_legacy_csv_header_is_a_strict_finding).
    # What this test is about survives unchanged — the columns the tier retired
    # but never banned (`Direction`, `ThisProject`, `Counterpart`, `Stability`)
    # are simply carried, a pre-WI-056 file with no Notes column still reads,
    # and nothing crashes.
    (req / "interfaces.csv").write_text(
        legacy + "IF-001,Provides,src/demo,git,v1,Stable,Active,\n",
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
    """A two-module project whose single TC cites `verifies` (no arch-map
    refresh since WI-455 — trace joins IF endpoints to LLR Module cells, and
    the derived inventory reads the source tree directly)."""
    make_minimal_project(scaffold)
    (scaffold / "src" / "helper.py").write_text(HELPER_SRC, encoding="utf-8")
    _write_ifs(scaffold, TWO_MODULE_IFS)
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        'TC-001,{},Unit,call add and assert the sum,Smoke,"a=1; b=2",'
        '"Satisfies SR-001 AcceptanceCriteria",Yes,'
        "tests/test_demo.py::test_add_sr001,Approved\n".format(verifies),
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


# --- WI-089: the Drafted artifact state + decomposition exemption ---------------
# The derived-gate model (docs/archive/specs/derived-gate-model.2026-07-20.md §3) lets a requirement
# be drafted in the LIVE spine before it is decomposed: a `Drafted` SR/LLR is exempt
# from the child-completeness orphan rules and the --require-verified criterion,
# retiring the -000/off-spine workaround. Parent-linkage + integrity still apply.

# SR-002 is Drafted with NO LLR and NO TC (undecomposed), but it links SN-001. It
# must NOT orphan. SR-001 keeps the fully-traced happy chain.
DRAFT_SR = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Approved
SR-002,Drafted requirement,SN-001,"The system shall do a not-yet-decomposed thing.","Being drafted requirement-first.","some measurable outcome",,M,Test,Drafted
"""


def test_draft_sr_is_exempt_from_decomposition(scaffold):
    # A Drafted SR with no LLR/TC lives in the live spine without orphaning.
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
    assert "## Drafted artifacts (decomposition-exempt)" in report
    assert "SR-002 — Drafted requirement" in report
    # Approve it (Drafted -> Approved) and the decomposition rules fire again.
    srs.write_text(
        DRAFT_SR.replace(",M,Test,Drafted", ",M,Test,Approved"), encoding="utf-8"
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "SR SR-002 has no LLR" in report
    assert "SR SR-002 has no test (TC)" in report


# A Drafted LLR decomposing SR-001 but with no TC: exempt from the "no TC" rule.
DRAFT_LLRS = """LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status
LLR-001,SR-001,Pure adder,src/demo,add,"Pure function: two numbers -> sum.",(see TC),Approved
LLR-002,SR-001,Drafted sub-part,src/demo,addfast,"A not-yet-tested decomposition.",(see TC),Drafted
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
    # Mark it Approved and the missing TC is an orphan again.
    llrs.write_text(
        DRAFT_LLRS.replace("(see TC),Drafted", "(see TC),Approved"), encoding="utf-8"
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "LLR LLR-002 has no test (TC)" in report


# SR-002 is fully decomposed (LLR-002 + TC-002) so ONLY the status axis varies:
# Drafted -> exempt from --require-verified; Approved -> flagged.
RV_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Approved
SR-002,Drafted requirement,SN-001,"The system shall do a drafted thing.","Being drafted.","some measurable outcome",,M,Test,Drafted
"""
RV_LLRS = """LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status
LLR-001,SR-001,Pure adder,src/demo,add,"Pure function: two numbers -> sum.",(see TC),Approved
LLR-002,SR-002,Drafted sub-part,src/demo,addfast,"A drafted decomposition.",(see TC),Drafted
"""
RV_TCS = """TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status
TC-001,SR-001;LLR-001,Unit,call add and assert the sum,Smoke,"a=1; b=2","Satisfies SR-001 AcceptanceCriteria",Yes,tests/test_demo.py::test_add_sr001,Approved
TC-002,SR-002;LLR-002,Unit,drafted test,Full,,"Satisfies SR-002 AcceptanceCriteria",No,,Drafted
"""


def test_draft_sr_is_exempt_from_require_verified(scaffold):
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    (req / "system-requirements.csv").write_text(RV_SRS, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(RV_LLRS, encoding="utf-8")
    srs = req / "system-requirements.csv"
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(RV_TCS, encoding="utf-8")
    # Drafted SR-002 is pre-approval: --require-verified does not flag it.
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict", "--require-verified"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "status-findings=0" in proc.stdout
    # Approving it (Verification=Test, not yet `Approved`) flags it.
    srs.write_text(
        RV_SRS.replace(",M,Test,Drafted", ",M,Test,Modified"), encoding="utf-8"
    )
    proc = run_py(["scripts/trace.py", "--strict", "--require-verified"], cwd=scaffold)
    assert proc.returncode == 1
    assert "status-findings=1" in proc.stdout


def test_draft_sr_still_needs_sn_and_stays_integral(scaffold):
    # The Drafted exemption is scoped to child-completeness: parent-linkage (the SN
    # link) and id integrity still apply to a Drafted row.
    make_minimal_project(scaffold)
    srs = scaffold / "docs" / "requirements" / "system-requirements.csv"
    # A Drafted SR with an empty SN-Refs still orphans (SN linkage is not exempt).
    srs.write_text(
        DRAFT_SR.replace(
            "SR-002,Drafted requirement,SN-001,", "SR-002,Drafted requirement,,"
        ),
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    assert "SR SR-002 links no SN" in _report(scaffold)
    # A malformed Drafted id still fails the always-on integrity floor.
    srs.write_text(DRAFT_SR.replace("SR-002", "SR-2x"), encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc.returncode == 1
    assert "malformed" in _report(scaffold)


# --- WI-090: SN maturity via section-as-state ---------------------------------
# An SN under a heading whose text contains "draft" is unapproved (DevStg-Below) and exempt
# from the "every SN needs an SR" rule; SNs under any other heading are approved.

DRAFT_SN_MD = """# Stakeholder Needs (SN-###)

## Core needs

| SN-ID | Need | Why | Priority | Acceptance intent |
|---|---|---|---|---|
| SN-001 | Add two numbers. | Demo. | M | add(1,2) gives 3. |

## Draft needs (unapproved)

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
    assert "SN-002 (SN, unapproved section)" in report
    # The DAG flags the draft SN like a Status=Drafted row.
    assert "class SN_002 draft" in report
    # Approve SN-002 by moving its row under a non-draft heading -> the SN-with-no-SR
    # rule fires again (it now claims to be a real need with no decomposition).
    approved = DRAFT_SN_MD.replace("## Draft needs (unapproved)", "## More core needs")
    sn.write_text(approved, encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    assert "SN SN-002 has no SR" in _report(scaffold)


def test_sn_draft_ids_reader():
    from conftest import load_script

    trace = load_script("trace")
    assert trace.sn_draft_ids(DRAFT_SN_MD) == {"SN-002"}
    # A -000 placeholder in a draft section is excluded (like every other scan).
    assert trace.sn_draft_ids("## Draft needs\nSN-000 SN-005\n") == {"SN-005"}
    # No draft heading -> nothing is draft (the approved default).
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


# --- WI-188: the approved-phase completeness rule -----------------------------
TRACE = load_script("trace")


def _real(sr=(), llr=(), tc=()):
    """The {label: [dict-rows]} shape phase_approved_findings takes — minimal
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


def test_phase_approved_rule_arms_and_fires():
    f = TRACE.phase_approved_findings
    # Unarmed: nothing phased -> vacuous (a fully-blank downstream registry).
    assert f(_real(["SR-001,Approved,", "SR-002,Approved,"])) == []
    # Armed by SR-001's phase; SR-002 approved with a blank phase -> one finding.
    fired = f(_real(["SR-001,Approved,1", "SR-002,Approved,"]))
    assert len(fired) == 1 and "SR-002" in fired[0]
    # An unparseable approved phase fails (armed by SR-001).
    fired = f(_real(["SR-001,Approved,1", "SR-002,Approved,later"]))
    assert len(fired) == 1 and "SR-002" in fired[0]
    # A Drafted row may leave Phase blank even when armed.
    assert f(_real(["SR-001,Approved,1", "SR-002,Drafted,"])) == []
    # The rule spans LLR and TC too, not just SR.
    fired = f(
        _real(["SR-001,Approved,1"], ["LLR-001,Approved,"], ["TC-001,Approved,2"])
    )
    assert len(fired) == 1 and "LLR-001" in fired[0]


def test_phase_approved_rule_is_numeric_only():
    # Owner ruling 2026-08-01 (WI-402): once armed, an approved Phase cell is a
    # BARE INTEGER — digits only, full cell. A prefixed label still digit-parses
    # (phase_num is untouched, so legacy labels keep arming/filtering/deriving —
    # grandfathering), but the literal joins (--phase/--approve scope match,
    # check_trajectory's per-phase= vs [phase]-[gN] anchor join) miss it
    # SILENTLY, which is worse than a crash — so the live cell must be numeric.
    f = TRACE.phase_approved_findings
    # A vN-tagged approved registry now arms the rule AND fails it, per cell
    # (the pre-WI-402 vN-passes compatibility guarantee, deliberately retired).
    fired = f(_real(["SR-001,Approved,v1", "SR-002,Approved,v2"]))
    assert len(fired) == 2
    assert all("bare integer" in msg for msg in fired)
    # A single prefixed cell beside bare integers fires alone, naming the row.
    fired = f(_real(["SR-001,Approved,1", "SR-002,Approved,P1"]))
    assert len(fired) == 1 and "SR-002" in fired[0]
    # Bare integers stay green (surrounding whitespace is stripped, not judged).
    assert f(_real(["SR-001,Approved,1", "SR-002,Approved, 2 "])) == []
    # A Drafted row is exempt even with a prefixed cell (its phase is not yet
    # approved scope; it takes its bare number at approval).
    assert f(_real(["SR-001,Approved,1", "SR-002,Drafted,v9"])) == []


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
    # A fully phased spine (arming the rule) with every approved row numeric passes.
    make_minimal_project(scaffold)
    _phase_scaffold(scaffold, sr="1", llr="1", tc="1")
    proc = run_py(["scripts/trace.py", "--strict", "--strict-schema"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_approved_blank_phase_fails_strict_schema(scaffold):
    # Armed by the SR/LLR phases; the approved TC left blank is a schema finding
    # that gates under --strict (the schema tier's standing exit convention).
    make_minimal_project(scaffold)
    _phase_scaffold(scaffold, sr="1", llr="1", tc="")
    proc = run_py(["scripts/trace.py", "--strict", "--strict-schema"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "approved but its Phase" in report and "TC-001" in report


def test_approved_prefixed_phase_fails_strict_schema(scaffold):
    # WI-402: a prefixed-but-parseable cell (P1) arms the rule (digit-extract
    # arming) and fails it — the silently-vacuous literal-join shape, now a
    # schema finding rather than a quiet disarm.
    make_minimal_project(scaffold)
    _phase_scaffold(scaffold, sr="1", llr="1", tc="P1")
    proc = run_py(["scripts/trace.py", "--strict", "--strict-schema"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    report = (scaffold / "docs" / "test" / "report.md").read_text(encoding="utf-8")
    assert "approved but its Phase" in report and "TC-001" in report
    assert "bare integer" in report


# --- repo-review 2026-07-21 regressions ---------------------------------------


def test_require_verified_strips_padded_verification_cell(scaffold):
    # M-1: a padded '"Test "' cell must not create a false PASS. The original bug
    # was that --require-verified matched Verification == "Test" unstripped, so a
    # padded cell was silently skipped. WI-259 widened the bar to every approved
    # SR of any method, so a padded cell can no longer skip it on the method axis
    # either — a not-Approved approved SR is flagged regardless of its method cell.
    make_minimal_project(scaffold)
    csv_path = scaffold / "docs" / "requirements" / "system-requirements.csv"
    csv_path.write_text(
        csv_path.read_text(encoding="utf-8").replace(
            ",M,Test,Approved", ',M,"Test ",Modified'
        ),
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict", "--require-verified"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "DevStg-Impl requires Approved" in proc.stdout


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
    # and a non-draft heading (simultaneously exempt and approved).
    trace = load_script("trace")
    text = (
        "# Needs\n"
        "|SN-001| a | b | c |\n"
        "|SN-001| again | b | c |\n"
        "## Drafted candidates\n"
        "|SN-002| c | d | e |\n"
        "## Approved\n"
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


def test_the_provenance_allow_file_is_read_token_scoped(tmp_path):
    # `docs/provenance-allow`, the reviewed exception list for the citation-frame
    # advisory. Its key is `<ROW-ID> <Cell> <token>` — THREE fields — and the
    # third is what the whole design turns on: the earlier row/cell key
    # suppressed a whole cell while every entry justified one token, which was
    # measured hiding 67 unadjudicated tokens over 22 live rows.
    trace = load_script("trace")

    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "provenance-allow").write_text(
        "# a comment line declares nothing\n"
        "\n"
        "SR-040 Rationale investigated 2026-08-18 — the carrier-less residue.\n"
        "TC-040 Method CORRECTED 2026-08-18 — the other half of the tripwire.\n"
        "SR-101 Rationale   MINTED   out of  SR-140 — whitespace is collapsed.\n"
        "SR-102 Rationale added 2026-08-16 no separator so this declares nothing\n"
        "SR-103 Rationale — two fields before the separator declare nothing\n"
        "SR-104 — one field declares nothing\n",
        encoding="utf-8",
    )
    allow = trace.load_provenance_allow(tmp_path)

    assert trace.is_allowed(allow, "SR-040", "Rationale", "investigated 2026-08-18")
    assert trace.is_allowed(allow, "TC-040", "Method", "CORRECTED 2026-08-18")
    # Whitespace is collapsed on BOTH sides, so a cell that wraps mid-token still
    # matches the entry that names it; case is folded for the same reason.
    assert trace.is_allowed(allow, "SR-101", "Rationale", "MINTED out of SR-140")
    assert trace.is_allowed(allow, "SR-101", "Rationale", "minted out of\n  SR-140")
    # A malformed entry declares NOTHING — fail-soft in the LOUD direction, so
    # the worst it can do is leave a finding reported.
    assert not trace.is_allowed(allow, "SR-102", "Rationale", "added 2026-08-16")
    assert not trace.is_allowed(allow, "SR-103", "Rationale", "added 2026-08-16")
    assert not trace.is_allowed(allow, "SR-104", "Rationale", "added 2026-08-16")
    # Right row, right cell, DIFFERENT token: still reported. This is the whole
    # point of the token scope — an allowed frame never covers its neighbours.
    assert not trace.is_allowed(allow, "SR-040", "Rationale", "added 2026-08-16")
    assert not trace.is_allowed(allow, "SR-040", "Title", "investigated 2026-08-18")
    # An absent file is an empty set, never a crash.
    assert trace.load_provenance_allow(tmp_path / "nowhere") == set()


def test_this_repos_own_provenance_allow_entries_all_still_bite():
    # A reviewed exception that no longer matches anything is a claim nobody is
    # checking — and the token-scoped migration makes that failure mode real,
    # because re-wording an allowed cell now orphans its entry instead of
    # silently laundering whatever replaced it. Three pre-migration entries were
    # already dead this way (IF-123/127/130, whose reason named the PROVISIONAL
    # marker, which is not a citation token) and were retired rather than kept.
    trace = load_script("trace")
    text = load_script("trace_text")
    spine_carrier = load_script("spine_carrier")
    root = KIT.parent
    allow = trace.load_provenance_allow(root)
    # ANTI-VACUITY, and it may no longer be "the list is non-empty". OI-34's and
    # OI-37's executions retired the last two groups of entries, so an EMPTY list
    # is the file's legitimate resting state — the intended end for an exception
    # (the marker leaves the cell and the entry goes with it), not a reader that
    # silently returned nothing. The guard that survives that and still catches
    # what the non-empty one was reaching for is ONE KEY PER DECLARING LINE: a
    # parse that drops entries fails it at every population size, zero included,
    # and a line in this repo's own file that declares nothing fails it too.
    declared = [
        ln
        for ln in (root / trace.PROVENANCE_ALLOW)
        .read_text(encoding="utf-8-sig")
        .splitlines()
        if ln.strip() and not ln.lstrip().startswith("#")
    ]
    assert len(allow) == len(declared), (
        "docs/provenance-allow has {} declaring line(s) but the reader yielded "
        "{} key(s): {}".format(len(declared), len(allow), declared)
    )
    # ...and when the population IS zero, SAY SO IN THE RUN (2026-08-20, the
    # batch review's MINOR-14). The one-key-per-line guard above is real at
    # every size, but the LIVENESS sweep below has nothing to sweep with an
    # empty list, and a dot in the output reads exactly like a list that was
    # checked. A skip is the honest render of "this half did not run".
    if not declared:
        pytest.skip(
            "docs/provenance-allow declares nothing — the one-key-per-line "
            "guard above held at zero population, and the liveness sweep below "
            "has no entry to match against a live token"
        )

    tiers = (
        ("SR-ID", ("Title", "Requirement", "Rationale", "AcceptanceCriteria")),
        ("LLR-ID", ("Title", "Detail", "Rationale")),
        ("TC-ID", ("Method", "Expected", "Parameters")),
        ("IF-ID", ("Notes", "Rationale")),
        ("CMP-ID", ("Name", "Notes")),
        ("EXT-ID", ("Name", "Description", "Notes")),
    )
    live = set()
    for path in sorted((root / "docs").rglob("*.toml")):
        for key, cols in tiers:
            for row in spine_carrier.load(path, key):
                rid = str(row.get(key) or "").strip()
                if not rid or text.is_example(rid):
                    continue
                for col in cols:
                    reason = col in text.REASON_CELLS or key == "IF-ID"
                    for _, token in text.provenance_tokens(row.get(col), reason):
                        live.add(text.allow_key(rid, col, token))
    dead = sorted(k for k in allow if k not in live)
    assert not dead, "provenance-allow entries matching no live token: {}".format(dead)


# --- OI-41 ARM 1: the allow entry NAMES the open item it defers ---------------


def _allow_repo(tmp_path, entries, oi_rows='[open_item.OI-5]\nstatus = "pending"\n'):
    """A repo carrying only the two files ARM 1 reads: the allow file and the
    open-items registry (omitted entirely when `oi_rows` is None)."""
    (tmp_path / "docs" / "requirements").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "provenance-allow").write_text(entries, encoding="utf-8")
    if oi_rows is not None:
        (tmp_path / "docs" / "requirements" / "open-items.toml").write_text(
            oi_rows, encoding="utf-8"
        )
    return tmp_path


def test_an_allow_entry_names_the_open_item_it_defers(tmp_path):
    # ARM 1 (OI-41 ruled (e), 2026-08-20). The 19 entries this replaced PROMISED
    # an open-item row in prose and produced none: the promise and the queue were
    # two unconnected artifacts. As a FIELD the bad state is unrepresentable, and
    # it has no false positives — which is why it is hard at birth.
    trace = load_script("trace")
    root = _allow_repo(
        tmp_path,
        "# a comment declares nothing\n"
        "SR-001 Rationale added 2026-08-16 — OI-5: the reviewed reason.\n"
        "SR-002 Rationale added 2026-08-16 — no row is named here.\n"
        "SR-003 Rationale added 2026-08-16 — OI-99: a row that does not exist.\n",
    )
    entries = trace.parse_provenance_allow(root)
    assert [e["oi"] for e in entries] == ["OI-5", None, "OI-99"]
    findings = trace.provenance_allow_findings(entries, trace.open_item_states(root))
    assert len(findings) == 2, findings
    assert "SR-002 Rationale): the entry names no OI-###" in findings[0]
    assert "docs/provenance-allow:3" in findings[0]
    assert "SR-003" in findings[1] and "names OI-99, which has no row" in findings[1]
    # The compliant entry is quiet, and the KEY the suppression turns on is
    # unchanged by the new field — one parser, so the grammar that reports and
    # the grammar that silences cannot drift apart.
    assert trace.is_allowed(
        trace.load_provenance_allow(root), "SR-001", "Rationale", "added 2026-08-16"
    )


def test_the_allow_field_is_a_position_not_a_mention(tmp_path):
    # A field, not a phrase match: the id is the FIRST token of the reason. An id
    # discussed later in the sentence is prose — accepting it would re-introduce
    # exactly the "grabs items that are not applicable" failure the owner refused.
    trace = load_script("trace")
    root = _allow_repo(
        tmp_path,
        "SR-001 Rationale added 2026-08-16 — see the analysis under OI-5 someday.\n",
    )
    entries = trace.parse_provenance_allow(root)
    assert entries[0]["oi"] is None
    assert trace.provenance_allow_findings(entries, trace.open_item_states(root))


def test_a_ruled_row_still_satisfies_arm_1_and_no_registry_is_vacuous(tmp_path):
    # The row's STATE is deliberately NOT an arm here. Ruled-but-not-yet-executed
    # is a legal transient (the entry retires with the execution), and the count
    # contradiction it can hide is ARM 3's, which names the same entries once
    # rather than twice.
    trace = load_script("trace")
    entry = "SR-001 Rationale added 2026-08-16 — OI-5: ruled, execution owed.\n"
    ruled = _allow_repo(
        tmp_path / "ruled", entry, '[open_item.OI-5]\nstatus = "ruled"\n'
    )
    assert not trace.provenance_allow_findings(
        trace.parse_provenance_allow(ruled), trace.open_item_states(ruled)
    )
    # No registry at all -> the rule cannot run: demanding a row from a file the
    # repo does not have is a MIGRATION, and the always-on layer's own S-3 says
    # so in words (check_docs.check_status_surface). None, never {} — D-5.
    bare = _allow_repo(tmp_path / "bare", entry, oi_rows=None)
    assert trace.open_item_states(bare) is None
    assert not trace.provenance_allow_findings(trace.parse_provenance_allow(bare), None)


def test_a_line_the_grammar_cannot_read_is_REPORTED_not_silently_dropped(tmp_path):
    """PARSE HONESTY (2026-08-20, the batch review's MAJOR-6). "Fail-soft in the
    LOUD direction" was half true: dropping a malformed entry does un-silence the
    finding it was written for, but it also removes the entry from every COUNT —
    and OI-41's vacuity arm IS a count. One mistyped separator and an exception
    that a human reads as live counts as none, so the arm prints an all-clear
    over a surface that still defers."""
    trace = load_script("trace")
    root = _allow_repo(
        tmp_path,
        "# a comment declares nothing, and is not counted\n"
        "SR-001 Rationale added 2026-08-16 — OI-5: the reviewed reason.\n"
        "SR-002 Rationale added 2026-08-16 -- OI-5: a hyphen, not an em dash.\n"
        "SR-003 — OI-5: too few key fields to name a token.\n",
    )
    entries, unparsed = trace.read_provenance_allow(root)
    assert len(entries) == 1
    assert [ln for ln, _text in unparsed] == [3, 4]
    findings = trace.provenance_allow_parse_findings(root)
    assert len(findings) == 1, findings
    assert "docs/provenance-allow:3" in findings[0]
    assert "2 such line(s)" in findings[0]
    # The legal file says nothing at all.
    clean = _allow_repo(
        tmp_path / "clean",
        "SR-001 Rationale added 2026-08-16 — OI-5: the reviewed reason.\n",
    )
    assert trace.provenance_allow_parse_findings(clean) == []


def test_an_unreadable_allow_line_reds_the_integrity_floor(scaffold):
    # Integrity-class like ARM 1's field rule, and for the same reason: the line
    # either parses or it does not, so there is no false positive to warn-first
    # about, and the always-on floor is the only pipe that runs at every gate.
    (scaffold / "docs" / "provenance-allow").write_text(
        "SR-001 Rationale added 2026-08-16 -- OI-1: a hyphen, not an em dash.\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 1, out
    assert "DECLARES an exception and the grammar cannot read it" in out, out
    (scaffold / "docs" / "provenance-allow").write_text(
        "SR-001 Rationale added 2026-08-16 — OI-1: the reviewed reason.\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_an_unresolved_allow_entry_reds_the_integrity_floor(scaffold):
    # HARD AT BIRTH, on the always-on floor the pre-commit hook runs: a field
    # with no false positives needs no warn-first program. The scaffold's own
    # registry carries pending OI-1, so the repaired entry is green.
    (scaffold / "docs" / "provenance-allow").write_text(
        "SR-001 Rationale added 2026-08-16 — owes an open-item row at the sitting.\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "the entry names no OI-###" in proc.stdout + proc.stderr
    (scaffold / "docs" / "provenance-allow").write_text(
        "SR-001 Rationale added 2026-08-16 — OI-1: the reviewed reason.\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
