"""trace.py integrity / placeholder / schema checks and their harness wiring
(template-review findings F3 'placeholders → false green' and F4 'data quality').
"""

from conftest import load_script, make_minimal_project, run_py


def sr_path(root):
    return root / "docs" / "requirements" / "system-requirements.csv"


def report_of(root):
    return (root / "docs" / "test" / "report.md").read_text(encoding="utf-8")


# --- Integrity: duplicate / malformed ids (always on; fail under --strict) -----

DUP_SRS = """SR-ID,Title,UN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,UN-001,"The system shall add.","r.","add(1,2) == 3",,M,Test,Verified
SR-001,Duplicate,UN-001,"The system shall add again.","r.","dup",,M,Test,Verified
"""

MALFORMED_SRS = """SR-ID,Title,UN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-XX,Addition,UN-001,"The system shall add.","r.","add(1,2) == 3",,M,Test,Verified
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
