"""plan_round.py — the dual-plan round state machine (WI-194).

Drives the pure lifecycle library with injected fake step results (the P1
done-condition): the happy path, the coverage bounce-once-then-page ladder,
the n=1 critique / one-revision caps as raised errors, the position-swap
agreement rule, the budget ledger, and the gate-policy page-action map.
"""

import json

import pytest
from conftest import SCRIPTS, load_script, run_py

pr = load_script("plan_round")


def test_default_budget_covers_repairs_and_relaunch_headroom():
    assert pr.DEFAULT_ROUND_BUDGET == 14
    assert pr.new_round("t")["budget"] == 14


def drive_to_critique(state, verdicts=("CHANGES-REQUESTED", "CHANGES-REQUESTED")):
    pr.record(state, pr.STEP_PLAN, plan="A", ok=True)
    pr.record(state, pr.STEP_PLAN, plan="B", ok=True)
    pr.record(state, pr.STEP_COVERAGE, stage="coverage1", findings=False)
    pr.record(state, pr.STEP_CRITIQUE, plan="A", verdict=verdicts[0])
    return pr.record(state, pr.STEP_CRITIQUE, plan="B", verdict=verdicts[1])


def drive_to_arbiter(state):
    drive_to_critique(state)
    pr.record(state, pr.STEP_REVISE, plan="A", ok=True)
    pr.record(state, pr.STEP_REVISE, plan="B", ok=True)
    return pr.record(state, pr.STEP_COVERAGE, stage="coverage2", findings=False)


def test_happy_path_selects_and_counts_budget():
    state = pr.new_round("t")
    drive_to_arbiter(state)
    assert state["stage"] == "arbiter"
    assert pr.record(state, pr.STEP_ARBITER, run="1", selection="B") == pr.DISP_CONTINUE
    disp = pr.record(state, pr.STEP_ARBITER, run="2", selection="B", ports=2)
    assert disp == pr.DISP_SELECTED
    assert state["selected"] == "B" and state["ports"] == 2
    assert state["spent"] == 8  # 2 plan + 2 critique + 2 revise + 2 arbiter
    assert pr.ready_steps(state) == []


def test_state_is_json_roundtrippable():
    state = pr.new_round("t")
    drive_to_critique(state)
    assert pr.disposition(json.loads(json.dumps(state))) == pr.DISP_CONTINUE


def test_ready_steps_offer_parallel_pairs():
    state = pr.new_round("t")
    assert [s["plan"] for s in pr.ready_steps(state)] == ["A", "B"]
    pr.record(state, pr.STEP_PLAN, plan="A", ok=True)
    assert [s["plan"] for s in pr.ready_steps(state)] == ["B"]


def test_approved_plans_skip_revision_and_coverage2():
    state = pr.new_round("t")
    drive_to_critique(state, verdicts=("APPROVE", "APPROVE"))
    # No revision happened, so the stage-1 report stands and the arbiter is next.
    assert state["stage"] == "arbiter"
    assert {s["step"] for s in pr.ready_steps(state)} == {pr.STEP_ARBITER}


def test_coverage_findings_bounce_once_then_page():
    state = pr.new_round("t")
    pr.record(state, pr.STEP_PLAN, plan="A", ok=True)
    pr.record(state, pr.STEP_PLAN, plan="B", ok=True)
    assert (
        pr.record(state, pr.STEP_COVERAGE, stage="coverage1", findings=True)
        == pr.DISP_CONTINUE
    )
    assert {s["step"] for s in pr.ready_steps(state)} == {pr.STEP_REPAIR}
    pr.record(state, pr.STEP_REPAIR, plan="A", stage="coverage1", ok=True)
    pr.record(state, pr.STEP_REPAIR, plan="B", stage="coverage1", ok=True)
    # Repaired set re-runs coverage; a second findings exit pages.
    disp = pr.record(state, pr.STEP_COVERAGE, stage="coverage1", findings=True)
    assert disp == pr.DISP_PAGE
    assert "one legal repair" in state["page_reason"]
    assert pr.ready_steps(state) == []


def test_second_repair_for_same_plan_is_a_cap_error():
    state = pr.new_round("t")
    pr.record(state, pr.STEP_PLAN, plan="A", ok=True)
    pr.record(state, pr.STEP_PLAN, plan="B", ok=True)
    pr.record(state, pr.STEP_COVERAGE, stage="coverage1", findings=True)
    pr.record(state, pr.STEP_REPAIR, plan="A", stage="coverage1", ok=True)
    with pytest.raises(pr.RoundCapError):
        pr.record(state, pr.STEP_REPAIR, plan="A", stage="coverage1", ok=True)


def test_single_plan_findings_repair_only_that_plan():
    state = pr.new_round("t")
    pr.record(state, pr.STEP_PLAN, plan="A", ok=True)
    pr.record(state, pr.STEP_PLAN, plan="B", ok=True)
    pr.record(state, pr.STEP_COVERAGE, stage="coverage1", findings=True, plans=["A"])
    assert pr.ready_steps(state) == [
        {"step": pr.STEP_REPAIR, "plan": "A", "stage": "coverage1"}
    ]
    with pytest.raises(pr.RoundCapError, match="owes no repair"):
        pr.record(state, pr.STEP_REPAIR, plan="B", stage="coverage1", ok=True)
    pr.record(state, pr.STEP_REPAIR, plan="A", stage="coverage1", ok=True)
    # The repaired set re-runs coverage; a clean pass proceeds to critique.
    pr.record(state, pr.STEP_COVERAGE, stage="coverage1", findings=False)
    assert state["stage"] == "critique"


def test_second_critique_is_a_cap_error():
    state = pr.new_round("t")
    drive_to_critique(state)
    with pytest.raises(pr.RoundCapError, match="one round, ever"):
        pr.record(state, pr.STEP_CRITIQUE, plan="A", verdict="APPROVE")


def test_revision_without_changes_requested_is_a_cap_error():
    state = pr.new_round("t")
    drive_to_critique(state, verdicts=("APPROVE", "CHANGES-REQUESTED"))
    with pytest.raises(pr.RoundCapError, match="no CHANGES-REQUESTED"):
        pr.record(state, pr.STEP_REVISE, plan="A", ok=True)
    pr.record(state, pr.STEP_REVISE, plan="B", ok=True)
    with pytest.raises(pr.RoundCapError, match="one revision"):
        pr.record(state, pr.STEP_REVISE, plan="B", ok=True)


def test_arbiter_disagreement_pages_position_unstable():
    state = pr.new_round("t")
    drive_to_arbiter(state)
    pr.record(state, pr.STEP_ARBITER, run="1", selection="A")
    disp = pr.record(state, pr.STEP_ARBITER, run="2", selection="B")
    assert disp == pr.DISP_PAGE
    assert "position-unstable" in state["page_reason"]


def test_third_arbiter_run_is_a_cap_error():
    state = pr.new_round("t")
    drive_to_arbiter(state)
    pr.record(state, pr.STEP_ARBITER, run="1", selection="A")
    with pytest.raises(pr.RoundCapError):
        pr.record(state, pr.STEP_ARBITER, run="1", selection="A")


def test_budget_exhaustion_pages():
    state = pr.new_round("t", budget=3)
    pr.record(state, pr.STEP_PLAN, plan="A", ok=True)
    pr.record(state, pr.STEP_PLAN, plan="B", ok=True)
    pr.record(state, pr.STEP_COVERAGE, stage="coverage1", findings=False)
    disp = pr.record(state, pr.STEP_CRITIQUE, plan="A", verdict="APPROVE")
    assert disp == pr.DISP_CONTINUE  # third session spends the last unit
    disp = pr.record(state, pr.STEP_CRITIQUE, plan="B", verdict="APPROVE")
    assert disp == pr.DISP_PAGE
    assert "budget exhausted" in state["page_reason"]


def test_recording_into_a_closed_round_is_a_cap_error():
    state = pr.new_round("t")
    drive_to_arbiter(state)
    pr.record(state, pr.STEP_ARBITER, run="1", selection="A")
    pr.record(state, pr.STEP_ARBITER, run="2", selection="A")
    with pytest.raises(pr.RoundCapError, match="already closed"):
        pr.record(state, pr.STEP_PLAN, plan="A", ok=True)


def test_page_action_maps_gate_policies_and_fails_safe():
    assert pr.page_action("attended") == "stop-needs-human"
    assert pr.page_action("single-ratify") == "surface-block-continue-others"
    assert pr.page_action("autonomous") == "design-check-session"
    assert pr.page_action(None) == "stop-needs-human"
    assert pr.page_action("bogus") == "stop-needs-human"


def test_cli_walk_prints_the_happy_path(tmp_path):
    proc = run_py([SCRIPTS / "plan_round.py", "walk"], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "selected=B ports=0" in proc.stdout
    assert "SELECTED" in proc.stdout
