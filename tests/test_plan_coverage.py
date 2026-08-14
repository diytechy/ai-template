"""plan_coverage.py — the dual-plan coverage pre-pass (WI-190).

Exercises the commensurability contract end-to-end the way a dispatcher would:
a goal brief with C# clauses, two rival plan tables, the optional SR/IF
registries — asserting the computed coverage diff, the findings (unknown refs,
rationale-less Proposed seams, cycles), and the honest degradation when a
registry is absent.
"""

from conftest import SCRIPTS, run_py

SCRIPT = SCRIPTS / "plan_coverage.py"

GOAL = """# Goal brief

- C1: the dispatcher launches two planner sessions.
- C2: briefs are redacted by construction.
- **C3**: the verdict file records ports.
- C4: budgets bound every session.
"""

PLAN_A = """## Plan

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Launch planner sessions | C1 | IF-001 | |
| P2 | Redacted brief builder | C2; SR-001 | intra-module | P1 |

## Notes
- C3, C4 excluded: out of scope for the pilot.
"""

PLAN_B = """| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| Q1 | Session launcher | C1 | IF-001 | |
| Q2 | Verdict writer | C3 | Proposed: nearest is IF-001, wrong direction - a new Provides row is needed | Q1 |
"""

IFS = (
    "[interface.IF-001]\n"
    'direction = "Provides"\n'
    'this_project = "scripts/a"\n'
    'counterpart = "scripts/b"\n'
    'contract = "contract"\n'
    'signal = "discrete"\n'
    'sr_refs = ["SR-001"]\n'
    'version = "v1"\n'
    'approval = "approved"\n'
)
SRS = "SR-ID,Title,Requirement\nSR-001,One,shall\n"


def write_inputs(tmp_path, goal=GOAL, plans=(PLAN_A, PLAN_B), registries=True):
    (tmp_path / "goal.md").write_text(goal, encoding="utf-8")
    names = []
    for i, text in enumerate(plans):
        name = "plan-{}.md".format("AB"[i] if i < 2 else i)
        (tmp_path / name).write_text(text, encoding="utf-8")
        names.append(name)
    if registries:
        req = tmp_path / "docs" / "requirements"
        req.mkdir(parents=True)
        (req / "interfaces.toml").write_text(IFS, encoding="utf-8")
        (req / "system-requirements.csv").write_text(SRS, encoding="utf-8")
    return names


def run(tmp_path, names, extra=()):
    return run_py(
        [SCRIPT, "--goal", tmp_path / "goal.md", "--root", tmp_path]
        + [tmp_path / n for n in names]
        + list(extra),
        cwd=tmp_path,
    )


def test_two_plans_green_with_coverage_diff(tmp_path):
    names = write_inputs(tmp_path)
    proc = run(tmp_path, names)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    out = proc.stdout
    assert "only plan-A.md: C2" in out
    assert "only plan-B.md: C3" in out
    assert "both: C1" in out
    assert "neither: C4" in out
    assert "plan_coverage: OK" in out


def test_out_writes_the_report_file(tmp_path):
    names = write_inputs(tmp_path)
    proc = run(tmp_path, names, extra=["--out", tmp_path / "coverage.md"])
    assert proc.returncode == 0, proc.stdout + proc.stderr
    report = (tmp_path / "coverage.md").read_text(encoding="utf-8")
    assert "# Plan coverage report" in report
    assert "## Coverage diff: plan-A.md vs plan-B.md" in report


def test_unknown_clause_and_sr_refs_fail(tmp_path):
    bad = PLAN_A.replace("C2; SR-001", "C9; SR-999")
    names = write_inputs(tmp_path, plans=(bad,))
    proc = run(tmp_path, names)
    assert proc.returncode == 1
    assert "cites undeclared clause C9" in proc.stdout
    assert "cites unknown SR-999" in proc.stdout


def test_unresolvable_if_and_rationale_less_proposed_fail(tmp_path):
    bad = PLAN_B.replace(
        "Proposed: nearest is IF-001, wrong direction - a new Provides row is needed",
        "Proposed:",
    ).replace("IF-001", "IF-042")
    names = write_inputs(tmp_path, plans=(bad,))
    proc = run(tmp_path, names)
    assert proc.returncode == 1
    assert "IF-042 which resolves to no interfaces.toml row" in proc.stdout
    assert "proposes a seam with no rationale" in proc.stdout


def test_empty_interfaces_cell_without_escape_fails(tmp_path):
    bad = PLAN_A.replace("intra-module", "")
    names = write_inputs(tmp_path, plans=(bad,))
    proc = run(tmp_path, names)
    assert proc.returncode == 1
    assert "states no intra-module escape" in proc.stdout


def test_predecessor_cycle_and_unknown_pred_fail(tmp_path):
    bad = PLAN_A.replace(
        "| P1 | Launch planner sessions | C1 | IF-001 | |",
        "| P1 | Launch planner sessions | C1 | IF-001 | P2 |",
    )
    names = write_inputs(tmp_path, plans=(bad,))
    proc = run(tmp_path, names)
    assert proc.returncode == 1
    assert "predecessor cycle" in proc.stdout


def test_unknown_predecessor_fails(tmp_path):
    bad = PLAN_B.replace("| Q1 |\n", "| Q9 |\n")
    names = write_inputs(tmp_path, plans=(bad,))
    proc = run(tmp_path, names)
    assert proc.returncode == 1
    assert "names unknown predecessor Q9" in proc.stdout


def test_duplicate_plan_wi_id_fails(tmp_path):
    bad = PLAN_A.replace("| P2 |", "| P1 |")
    names = write_inputs(tmp_path, plans=(bad,))
    proc = run(tmp_path, names)
    assert proc.returncode == 1
    assert "duplicate Plan-WI id P1" in proc.stdout


def test_absent_registries_degrade_to_notes_not_findings(tmp_path):
    names = write_inputs(tmp_path, registries=False)
    proc = run(tmp_path, names)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "no system-requirements.csv; SR refs unvalidated" in proc.stdout
    assert "no interfaces.toml; IF refs unvalidated" in proc.stdout


def test_goal_without_clauses_is_a_malformed_input(tmp_path):
    names = write_inputs(tmp_path, goal="# just prose\n")
    proc = run(tmp_path, names)
    assert proc.returncode == 2
    assert "declares no clauses" in proc.stdout


def test_plan_without_table_is_a_malformed_input(tmp_path):
    names = write_inputs(tmp_path, plans=("no table here\n",))
    proc = run(tmp_path, names)
    assert proc.returncode == 2
    assert "has no Plan-WI table" in proc.stdout


def test_multi_covered_clause_is_reported_not_failed(tmp_path):
    plan = PLAN_A.replace("C2; SR-001", "C1; C2")
    names = write_inputs(tmp_path, plans=(plan,))
    proc = run(tmp_path, names)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "multi-covered: C1 (P1, P2)" in proc.stdout
