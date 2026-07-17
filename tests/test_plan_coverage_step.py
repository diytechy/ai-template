"""plan_coverage_step.py — the coverage step adapter (WI-197, DP-001 plan P4).

Drives the three P4 paths end-to-end WITH the real plan_round machine and the
real plan_coverage.py subprocess (no fakes): a clean pass advances the round; a
findings run bounces to a repair for exactly the implicated plan, and a repaired
file re-runs clean and advances; a findings run that repeats after its one repair
pages the round. Plus the exit-2 malformed outcome, single-plan implicated
parsing, and the captured report payload.
"""

from conftest import load_script

pr = load_script("plan_round")
step = load_script("plan_coverage_step")

# --- fixtures: the commensurability-contract shapes (copied from
# test_plan_coverage.py) --------------------------------------------------------
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
"""

# Plan B, clean: every Covers/Interfaces cite resolves.
PLAN_B_GOOD = """| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| Q1 | Session launcher | C1 | IF-001 | |
| Q2 | Verdict writer | C3 | Proposed: nearest is IF-001, wrong direction - a new Provides row is needed | Q1 |
"""

# Plan B, at fault: Q2 cites an undeclared clause -> exactly one plan implicated.
PLAN_B_BAD = PLAN_B_GOOD.replace(
    "| Q2 | Verdict writer | C3 |", "| Q2 | Verdict writer | C9 |"
)

IFS = (
    "IF-ID,Direction,ThisProject,Counterpart,Contract,SR-Refs,Version,Stability,Status,Component,Notes\n"
    "IF-001,Provides,scripts/a,scripts/b,contract,SR-001,v1,Stable,Stable,,\n"
)
SRS = "SR-ID,Title,Requirement\nSR-001,One,shall\n"


def key_of(basename):
    """Map a plan file basename to its true plan key (the coordinator's job)."""
    return {"plan-A.md": "A", "plan-B.md": "B"}.get(basename)


def write_case(tmp_path, plan_b, goal=GOAL, registries=True):
    (tmp_path / "goal.md").write_text(goal, encoding="utf-8")
    (tmp_path / "plan-A.md").write_text(PLAN_A, encoding="utf-8")
    (tmp_path / "plan-B.md").write_text(plan_b, encoding="utf-8")
    if registries:
        req = tmp_path / "docs" / "requirements"
        req.mkdir(parents=True, exist_ok=True)
        (req / "interfaces.csv").write_text(IFS, encoding="utf-8")
        (req / "system-requirements.csv").write_text(SRS, encoding="utf-8")
    return tmp_path / "goal.md", [tmp_path / "plan-A.md", tmp_path / "plan-B.md"]


def drive_to_coverage1(state):
    """Record both planner steps so the round sits at the coverage1 stage."""
    pr.record(state, pr.STEP_PLAN, plan="A", ok=True)
    pr.record(state, pr.STEP_PLAN, plan="B", ok=True)
    assert state["stage"] == "coverage1"


def run(tmp_path, goal, plans):
    return step.run_coverage(goal, plans, tmp_path, tmp_path / "coverage.md", key_of)


def repair_names(state):
    ready = pr.ready_steps(state)
    assert ready and all(s["step"] == pr.STEP_REPAIR for s in ready)
    return {s["plan"] for s in ready}


# --- path 1: clean pass advances the round ------------------------------------
def test_clean_pass_advances_the_round(tmp_path):
    goal, plans = write_case(tmp_path, PLAN_B_GOOD)
    state = pr.new_round("dp-clean")
    drive_to_coverage1(state)

    result = run(tmp_path, goal, plans)
    assert result["exit"] == 0
    assert result["findings"] is False
    assert result["malformed"] is False
    assert result["implicated"] == []

    disp = pr.record(
        state, pr.STEP_COVERAGE, stage="coverage1", **step.to_record_kwargs(result)
    )
    assert disp == pr.DISP_CONTINUE
    assert state["stage"] == "critique"  # coverage1 == ok -> the round moved on


# --- path 2: findings -> bounce -> repaired file -> clean re-run advances ------
def test_findings_bounce_then_repair_then_clean_advances(tmp_path):
    goal, plans = write_case(tmp_path, PLAN_B_BAD)
    state = pr.new_round("dp-bounce")
    drive_to_coverage1(state)

    bad = run(tmp_path, goal, plans)
    assert bad["exit"] == 1 and bad["findings"] is True
    assert bad["implicated"] == ["B"]  # only plan B is at fault

    disp = pr.record(
        state, pr.STEP_COVERAGE, stage="coverage1", **step.to_record_kwargs(bad)
    )
    assert disp == pr.DISP_CONTINUE
    assert state["stage"] == "coverage1"  # bounced, not advanced
    # The repair is offered for EXACTLY the implicated plan.
    assert repair_names(state) == {"B"}

    pr.record(state, pr.STEP_REPAIR, plan="B", stage="coverage1", ok=True)
    # The author repairs the file, then coverage re-runs.
    (tmp_path / "plan-B.md").write_text(PLAN_B_GOOD, encoding="utf-8")
    assert pr.ready_steps(state) == [{"step": pr.STEP_COVERAGE, "stage": "coverage1"}]

    good = run(tmp_path, goal, plans)
    assert good["exit"] == 0 and good["findings"] is False
    disp = pr.record(
        state, pr.STEP_COVERAGE, stage="coverage1", **step.to_record_kwargs(good)
    )
    assert disp == pr.DISP_CONTINUE
    assert state["stage"] == "critique"


# --- path 3: findings -> repair -> findings again -> the round PAGEs -----------
def test_findings_repeat_after_repair_pages(tmp_path):
    goal, plans = write_case(tmp_path, PLAN_B_BAD)
    state = pr.new_round("dp-page")
    drive_to_coverage1(state)

    first = run(tmp_path, goal, plans)
    pr.record(
        state, pr.STEP_COVERAGE, stage="coverage1", **step.to_record_kwargs(first)
    )
    pr.record(state, pr.STEP_REPAIR, plan="B", stage="coverage1", ok=True)

    # The file is NOT actually fixed: coverage still finds the same fault.
    again = run(tmp_path, goal, plans)
    assert again["implicated"] == ["B"]
    disp = pr.record(
        state, pr.STEP_COVERAGE, stage="coverage1", **step.to_record_kwargs(again)
    )
    assert disp == pr.DISP_PAGE
    assert "persist" in state["page_reason"]


# --- exit-2 malformed: its own outcome, bounces both plans --------------------
def test_malformed_inputs_are_their_own_outcome_and_bounce_both(tmp_path):
    goal, plans = write_case(tmp_path, PLAN_B_GOOD, goal="# just prose, no clauses\n")
    state = pr.new_round("dp-malformed")
    drive_to_coverage1(state)

    result = run(tmp_path, goal, plans)
    assert result["exit"] == 2
    assert result["malformed"] is True
    assert result["findings"] is False  # the distinction is preserved in the dict
    assert result["implicated"] == []
    assert "declares no clauses" in result["report"]  # the ERROR text is captured

    # ...but it bounces exactly like findings, with no parseable plan -> both.
    kwargs = step.to_record_kwargs(result)
    assert kwargs == {"findings": True, "plans": []}
    disp = pr.record(state, pr.STEP_COVERAGE, stage="coverage1", **kwargs)
    assert disp == pr.DISP_CONTINUE
    assert repair_names(state) == {"A", "B"}


# --- implicated parsing: only the faulting plan is named ----------------------
def test_implicated_parsing_names_only_the_faulting_plan(tmp_path):
    goal, plans = write_case(tmp_path, PLAN_B_BAD)
    result = run(tmp_path, goal, plans)
    assert result["exit"] == 1
    assert result["implicated"] == ["B"]  # plan A is clean and never named


# --- the report payload is captured for the briefs, not printed ---------------
def test_report_payload_is_captured(tmp_path, capsys):
    goal, plans = write_case(tmp_path, PLAN_B_GOOD)
    result = run(tmp_path, goal, plans)
    report = result["report"]
    assert "# Plan coverage report" in report
    assert "## Coverage diff: plan-A.md vs plan-B.md" in report
    assert "only plan-B.md: C3" in report
    # run_coverage returns the report; it never prints it.
    assert capsys.readouterr().out == ""
