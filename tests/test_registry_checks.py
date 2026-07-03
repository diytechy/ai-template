"""trace.py integrity / placeholder / schema checks and their harness wiring
(template-review findings F3 'placeholders → false green' and F4 'data quality').
"""

from conftest import load_script, make_minimal_project, run_py


def sr_path(root):
    return root / "docs" / "requirements" / "system-requirements.csv"


def report_of(root):
    return (root / "docs" / "test" / "report.md").read_text(encoding="utf-8")


# --- Integrity: duplicate / malformed ids (always on; fail under --strict) -----

DUP_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add.","r.","add(1,2) == 3",,M,Test,Verified
SR-001,Duplicate,SN-001,"The system shall add again.","r.","dup",,M,Test,Verified
"""

MALFORMED_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-XX,Addition,SN-001,"The system shall add.","r.","add(1,2) == 3",,M,Test,Verified
"""


def test_duplicate_id_fails_strict(scaffold):
    make_minimal_project(scaffold)
    sr_path(scaffold).write_text(DUP_SRS, encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "SR id SR-001 is duplicated" in report_of(scaffold)


def test_malformed_id_fails_strict(scaffold):
    make_minimal_project(scaffold)
    sr_path(scaffold).write_text(MALFORMED_SRS, encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "is malformed" in report_of(scaffold)


# --- Structure: parsed column count must match the header (WI-1.15) ------------
# The Gilbert G2 finding: unquoted commas inside Permutations sets (set{a,b,c})
# or free-text Rationale cells silently shift every later column; a compliant
# parser sees 12 columns against a 10-column header, and nothing failed until
# G3 --strict-schema. Structure is integrity-class: wrong at any stage.

# Permutations cell `set{a,b}` unquoted -> 11 parsed columns vs the 10-col header.
UNQUOTED_COMMA_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add.","r.","add(1,2) == 3",set{a,b},M,Test,Verified
"""

# Same row properly quoted -> exactly 10 columns; the control must stay green.
QUOTED_COMMA_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add.","r.","add(1,2) == 3","set{a,b}",M,Test,Verified
"""

# A short row (trailing cells lost, e.g. a hand-edit that ate the Status cell).
SHORT_ROW_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add.","r.","add(1,2) == 3",,M
"""


def test_unquoted_comma_fails_strict_integrity_with_loud_detail(scaffold):
    make_minimal_project(scaffold)
    sr_path(scaffold).write_text(UNQUOTED_COMMA_SRS, encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    report = report_of(scaffold)
    # Loud and actionable: file, row id, line, and expected/actual counts.
    assert "requirements/system-requirements.csv" in report
    assert "SR-001" in report
    assert "11 column(s)" in report
    assert "header has 10" in report


def test_unquoted_comma_fails_strict_too(scaffold):
    make_minimal_project(scaffold)
    sr_path(scaffold).write_text(UNQUOTED_COMMA_SRS, encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr


def test_quoted_comma_control_stays_green(scaffold):
    make_minimal_project(scaffold)
    sr_path(scaffold).write_text(QUOTED_COMMA_SRS, encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict", "--strict-integrity"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_short_row_fails_strict_integrity(scaffold):
    make_minimal_project(scaffold)
    sr_path(scaffold).write_text(SHORT_ROW_SRS, encoding="utf-8")
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "8 column(s)" in report_of(scaffold)


def test_structure_swept_across_all_registry_csvs(scaffold):
    # The sweep must cover every *.csv under docs/requirements/ + docs/test/ —
    # including registries trace.py never joins (interfaces.csv) — so a
    # project-added off-spine registry can't rot silently.
    make_minimal_project(scaffold)
    if_csv = scaffold / "docs" / "requirements" / "interfaces.csv"
    header = if_csv.read_text(encoding="utf-8").splitlines()[0]
    ncols = len(header.split(","))
    if_csv.write_text(
        header + "\n" + ",".join("x" for _ in range(ncols + 2)) + "\n",
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "requirements/interfaces.csv" in report_of(scaffold)


def test_structure_ignores_blank_rows_and_quoted_newlines():
    # Unit level: a trailing blank line is not a finding; a quoted multi-line
    # cell parses as one row of the right width.
    trace = load_script("trace")
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "x.csv"
        p.write_text('A,B\n1,"two\nlines"\n\n', encoding="utf-8")
        assert trace.structure_findings(p, "x.csv") == []
        p.write_text("A,B\n1,2,3\n", encoding="utf-8")
        (finding,) = trace.structure_findings(p, "x.csv")
        assert "x.csv" in finding and "3 column(s)" in finding
        assert "header has 2" in finding


def test_harness_runs_registry_integrity_at_g1(scaffold):
    # Gate wiring: G1 gets the always-valid integrity floor (the Gilbert defect
    # class must fail at the FIRST gate, not surface at G3 --strict-schema).
    check = load_script("check")
    g1 = [s for s in check.steps(80, "full", "G1") if "G1" in s[3]]
    (step,) = [s for s in g1 if s[0] == "registry-integrity"]
    assert step[4] == "process" and step[1] == ()
    assert "--strict-integrity" in step[2]
    # End-to-end: a fresh scaffold passes G1; a seeded misquote fails it.
    proc = run_py(["scripts/check.py", "--gate", "G1", "--lenient"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    make_minimal_project(scaffold)
    sr_path(scaffold).write_text(UNQUOTED_COMMA_SRS, encoding="utf-8")
    proc = run_py(["scripts/check.py", "--gate", "G1", "--lenient"], cwd=scaffold)
    assert proc.returncode != 0
    assert "RESULT: FAIL" in proc.stdout


# --- Placeholders: a fresh scaffold is green by default, fails opt-in ----------


def test_fresh_scaffold_ignores_placeholders_by_default(scaffold):
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_no_placeholders_flags_template_rows(scaffold):
    proc = run_py(["scripts/trace.py", "--strict", "--no-placeholders"], cwd=scaffold)
    assert proc.returncode == 1
    assert "placeholders=" in proc.stdout
    assert "placeholder row SR-000 still present" in report_of(scaffold)


def test_harness_g2_fails_on_unfilled_scaffold(scaffold):
    # The key F3 behavior: you cannot claim G2 with placeholder-only registries.
    proc = run_py(["scripts/check.py", "--gate", "G2"], cwd=scaffold)
    assert proc.returncode != 0
    assert "RESULT: FAIL" in proc.stdout


def test_check_flows_no_placeholders_flags_cited_000(scaffold):
    # The scaffold's authored flow still cites SR-000/LLR-000.
    proc = run_py(["scripts/check_flows.py", "--no-placeholders"], cwd=scaffold)
    assert proc.returncode == 1
    assert "placeholder id still cited" in proc.stdout
    # Without the flag the same scaffold is green (placeholders ignored).
    proc = run_py(["scripts/check_flows.py"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr


# --- Schema: required fields + the two closed vocabularies (opt-in) ------------


def test_strict_schema_flags_empty_required_field(scaffold):
    make_minimal_project(scaffold)
    csv = sr_path(scaffold)
    csv.write_text(
        csv.read_text(encoding="utf-8").replace('"add(1,2) == 3"', '""'),
        encoding="utf-8",
    )
    # Empty AcceptanceCriteria is a structurally-fine chain, so plain trace passes.
    assert run_py(["scripts/trace.py", "--strict"], cwd=scaffold).returncode == 0
    proc = run_py(["scripts/trace.py", "--strict", "--strict-schema"], cwd=scaffold)
    assert proc.returncode == 1
    assert "empty required field AcceptanceCriteria" in report_of(scaffold)


def test_strict_schema_flags_bad_enum(scaffold):
    make_minimal_project(scaffold)
    csv = sr_path(scaffold)
    csv.write_text(
        csv.read_text(encoding="utf-8").replace(
            ",M,Test,Verified", ",M,Testing,Verified"
        ),
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict", "--strict-schema"], cwd=scaffold)
    assert proc.returncode == 1
    assert "has Verification='Testing'" in report_of(scaffold)


def test_strict_schema_leaves_priority_and_status_open(scaffold):
    # The method does not close the Priority/Status vocabularies (process.md §4):
    # Priority=S and Status=Planned must NOT be schema findings.
    make_minimal_project(scaffold)
    csv = sr_path(scaffold)
    csv.write_text(
        csv.read_text(encoding="utf-8").replace(",M,Test,Verified", ",S,Test,Planned"),
        encoding="utf-8",
    )
    proc = run_py(["scripts/trace.py", "--strict", "--strict-schema"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr


# --- Harness wiring -----------------------------------------------------------


def test_harness_wires_new_flags():
    check = load_script("check")

    def cmd_of(plan, name):
        return next(s[2] for s in plan if s[0] == name)

    g2 = check.steps(80, "full", "G2")
    allg = check.steps(80, "full", "all")
    # --no-placeholders is on from G2; --strict-schema is G3/all only.
    assert "--no-placeholders" in cmd_of(g2, "traceability")
    assert "--strict-schema" not in cmd_of(g2, "traceability")
    assert "--strict-schema" in cmd_of(allg, "traceability")
    assert "--no-placeholders" in cmd_of(g2, "design-flows")
    assert "--strict-parse" in cmd_of(allg, "arch-map")


def test_strict_parse_cli_fails_only_with_flag(scaffold):
    # A syntax-broken module: bake the PARSE ERROR text in first so --check alone
    # sees the map as up to date, then show --strict-parse still fails (F5).
    (scaffold / "src" / "broken.py").write_text("def x(:\n", encoding="utf-8")
    run_py(["scripts/gen_arch_map.py"], cwd=scaffold)
    ok = run_py(["scripts/gen_arch_map.py", "--check"], cwd=scaffold)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    strict = run_py(
        ["scripts/gen_arch_map.py", "--check", "--strict-parse"], cwd=scaffold
    )
    assert strict.returncode == 1
    assert "failed to parse" in strict.stderr
