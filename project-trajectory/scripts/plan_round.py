#!/usr/bin/env python3
"""The dual-plan round state machine: a pure, side-effect-free library the
coordinator drives (DP-001 selected plan P1 / WI-194; the protocol it models is
process-options.md "Dual-plan decomposition").

Stack-agnostic, standard-library only (Python 3.11+, Windows/POSIX). Like
`schedule.py` (the IF-053 shape this module deliberately mirrors), it never
launches a session, touches git, or writes a file — the coordinator
(`agent_loop`) asks *what is ready*, runs the sessions, and records the
results; this module owns the lifecycle, the **hard caps**, and the
**round-budget ledger**, so no caller can accidentally iterate past the
protocol's evidence-backed limits:

    plan ×2 → coverage (bounce ≤1 per plan per stage) → cross-critique (×1,
    ever) → revision (≤1 each, only against CHANGES-REQUESTED) → coverage →
    arbiter ×2 position-swapped → verdict (agreement required).

Typed outcomes, not conversations: every step result is recorded as data
(`ok`/`findings`/`verdict`/`selection`), and the machine's disposition is one
of `CONTINUE` (more ready steps), `SELECTED` (agreed verdict), or `PAGE`
(verdict disagreement, cap exhaustion, repeated coverage findings, or budget
exhaustion) — the coordinator maps `PAGE` onto the session-hold failure
semantics via `page_action()`. A cap violation by the *caller* (recording a
second critique, revising an approved plan) raises `RoundCapError`: that is a
coordinator bug, never a legal transition.

State is one JSON-able dict (`new_round()` → drive with `ready_steps()` /
`record()`), so a crashed coordinator can persist and resume a round the same
git-as-authority way the dispatcher persists everything else.

Small helpers are duplicated from siblings per the kit's independently
copy-able-script convention (F5). Usage (the CLI is a documentation aid):

    python scripts/plan_round.py walk [--budget N]   # print the happy path

Contracts: IF-058 — the interface seam this module declares (process.md §8;
rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import json
import sys

# --- step vocabulary (what the coordinator is asked to run) -------------------
STEP_PLAN = "PLAN"  # a planner session (per plan key)
STEP_COVERAGE = "COVERAGE"  # mechanical plan_coverage.py run (no budget)
STEP_REPAIR = "REPAIR"  # the one author repair after a findings exit
STEP_CRITIQUE = "CRITIQUE"  # the cross-family critique session
STEP_REVISE = "REVISE"  # the single revision session
STEP_ARBITER = "ARBITER"  # one of the two position-swapped arbiter runs

# --- dispositions (what the machine reports after each record) ----------------
DISP_CONTINUE = "CONTINUE"
DISP_SELECTED = "SELECTED"
DISP_PAGE = "PAGE"

# Critique verdict vocabulary (the S8 verdict line, first word after VERDICT:).
VERDICT_APPROVE = "APPROVE"
VERDICT_CHANGES = "CHANGES-REQUESTED"

PLAN_KEYS = ("A", "B")

# Happy path spends 8 sessions; two legal repairs plus fallback/relaunch
# headroom must still fit without weakening any per-step cap.
DEFAULT_ROUND_BUDGET = 14

# `page_action()` — the documented session-hold failure semantics
# (process-options.md "Unattended operation", failure-semantics bullet). The
# coordinator owns executing these; the map keeps the wording in one place.
_PAGE_ACTIONS = {
    # SN-029: keyed on the two independent bits the retired three-value enum
    # bundled — (is the tier human-held, may other work keep running) — so each
    # dial means exactly one thing and the third combination stops being
    # unreachable.
    (True, False): "stop-needs-human",
    (True, True): "surface-block-continue-others",
    (False, False): "design-check-session",
    (False, True): "design-check-session",
}


class RoundCapError(ValueError):
    """The caller attempted a transition the protocol forbids (a second
    critique round, a revision without CHANGES-REQUESTED, a third arbiter
    run). Raised, never recorded: a cap violation is a coordinator bug."""


def _utf8_console():
    """Emit UTF-8 whatever the console codepage is (the trace.py/check.py guard)."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def new_round(slug, budget=DEFAULT_ROUND_BUDGET):
    """A fresh round state: one JSON-able dict, no hidden objects."""
    return {
        "slug": slug,
        "budget": int(budget),
        "spent": 0,
        "stage": "plan",  # plan | coverage1 | critique | revise | coverage2 | arbiter
        "plans": {
            k: {
                "planned": False,
                "repaired": {"coverage1": False, "coverage2": False},
                "critique": None,  # None | APPROVE | CHANGES-REQUESTED
                "revised": False,
            }
            for k in PLAN_KEYS
        },
        "coverage": {"coverage1": None, "coverage2": None},  # None | ok | findings
        "pending_repairs": [],  # plan keys still owing their repair this stage
        "arbiter": {"1": None, "2": None},  # None | "A" | "B" (TRUE plan key)
        "selected": None,
        "ports": None,
        "page_reason": None,
    }


def _needs_coverage2(state):
    """Coverage re-runs only when a revision changed a plan; two clean
    APPROVEs skip straight to the arbiter on the stage-1 report."""
    return any(state["plans"][k]["revised"] for k in PLAN_KEYS)


def ready_steps(state):
    """The steps the coordinator may dispatch now (parallel-friendly: both
    planner sessions, both critiques, and both arbiter runs are offered
    together). Empty when the round is paged or complete."""
    if state["page_reason"] or state["selected"]:
        return []
    stage = state["stage"]
    plans = state["plans"]
    if stage == "plan":
        return [
            {"step": STEP_PLAN, "plan": k} for k in PLAN_KEYS if not plans[k]["planned"]
        ]
    if stage in ("coverage1", "coverage2"):
        if state["coverage"][stage] == "findings":
            return [
                {"step": STEP_REPAIR, "plan": k, "stage": stage}
                for k in state["pending_repairs"]
            ]
        return [{"step": STEP_COVERAGE, "stage": stage}]
    if stage == "critique":
        return [
            {"step": STEP_CRITIQUE, "plan": k}
            for k in PLAN_KEYS
            if plans[k]["critique"] is None
        ]
    if stage == "revise":
        return [
            {"step": STEP_REVISE, "plan": k}
            for k in PLAN_KEYS
            if plans[k]["critique"] == VERDICT_CHANGES and not plans[k]["revised"]
        ]
    if stage == "arbiter":
        return [
            {"step": STEP_ARBITER, "run": r}
            for r in ("1", "2")
            if state["arbiter"][r] is None
        ]
    return []


def _spend(state, reason):
    state["spent"] += 1
    if state["spent"] > state["budget"]:
        state["page_reason"] = "round budget exhausted at {} ({}/{})".format(
            reason, state["spent"], state["budget"]
        )
        return False
    return True


def _advance(state):
    """Move `stage` forward when its steps are all recorded."""
    plans, stage = state["plans"], state["stage"]
    if stage == "plan" and all(plans[k]["planned"] for k in PLAN_KEYS):
        state["stage"] = "coverage1"
    elif stage == "coverage1" and state["coverage"]["coverage1"] == "ok":
        state["stage"] = "critique"
    elif stage == "critique" and all(plans[k]["critique"] for k in PLAN_KEYS):
        state["stage"] = "revise"
    if state["stage"] == "revise":
        pending = [
            k
            for k in PLAN_KEYS
            if plans[k]["critique"] == VERDICT_CHANGES and not plans[k]["revised"]
        ]
        if not pending:
            state["stage"] = "coverage2" if _needs_coverage2(state) else "arbiter"
    if state["stage"] == "coverage2" and state["coverage"]["coverage2"] == "ok":
        state["stage"] = "arbiter"


def record(state, step, plan=None, stage=None, run=None, **result):
    """Record one finished step and return the round's disposition.

    Expected result keys per step: PLAN/REPAIR/REVISE `ok=True`; COVERAGE
    `findings=bool`; CRITIQUE `verdict=APPROVE|CHANGES-REQUESTED`; ARBITER
    `selection="A"|"B"` (the TRUE plan key — the coordinator de-anonymizes
    before recording) and, on the agreeing pair, `ports=int`."""
    if state["page_reason"] or state["selected"]:
        raise RoundCapError("round already closed ({})".format(disposition(state)))
    plans = state["plans"]

    if step == STEP_PLAN:
        if plans[plan]["planned"]:
            raise RoundCapError("plan {} already generated".format(plan))
        if not _spend(state, "PLAN " + plan):
            return DISP_PAGE
        plans[plan]["planned"] = True

    elif step == STEP_COVERAGE:
        if stage not in ("coverage1", "coverage2") or state["stage"] != stage:
            raise RoundCapError("coverage stage {!r} not active".format(stage))
        if result.get("findings"):
            # `plans=` names the implicated plan(s); absent means both.
            flagged = list(result.get("plans") or PLAN_KEYS)
            if any(plans[k]["repaired"][stage] for k in flagged):
                state["page_reason"] = (
                    "coverage findings persist after the one legal repair ({})".format(
                        stage
                    )
                )
                return DISP_PAGE
            state["coverage"][stage] = "findings"
            state["pending_repairs"] = flagged
        else:
            state["coverage"][stage] = "ok"

    elif step == STEP_REPAIR:
        if state["coverage"].get(stage) != "findings":
            raise RoundCapError("no findings to repair at {!r}".format(stage))
        if plan not in state["pending_repairs"]:
            raise RoundCapError(
                "plan {} owes no repair at {} (or already used its one repair)".format(
                    plan, stage
                )
            )
        if not _spend(state, "REPAIR " + plan):
            return DISP_PAGE
        plans[plan]["repaired"][stage] = True
        state["pending_repairs"] = [k for k in state["pending_repairs"] if k != plan]
        if not state["pending_repairs"]:
            state["coverage"][stage] = None  # all owed repairs in - re-run coverage

    elif step == STEP_CRITIQUE:
        if plans[plan]["critique"] is not None:
            raise RoundCapError(
                "plan {} already critiqued - the cap is one round, ever".format(plan)
            )
        verdict = result.get("verdict")
        if verdict not in (VERDICT_APPROVE, VERDICT_CHANGES):
            raise RoundCapError("critique verdict must be APPROVE|CHANGES-REQUESTED")
        if not _spend(state, "CRITIQUE " + plan):
            return DISP_PAGE
        plans[plan]["critique"] = verdict

    elif step == STEP_REVISE:
        if plans[plan]["critique"] != VERDICT_CHANGES:
            raise RoundCapError(
                "plan {} has no CHANGES-REQUESTED critique to revise against".format(
                    plan
                )
            )
        if plans[plan]["revised"]:
            raise RoundCapError("plan {} already used its one revision".format(plan))
        if not _spend(state, "REVISE " + plan):
            return DISP_PAGE
        plans[plan]["revised"] = True

    elif step == STEP_ARBITER:
        if run not in ("1", "2"):
            raise RoundCapError("arbiter run must be '1' or '2'")
        if state["arbiter"][run] is not None:
            raise RoundCapError("arbiter run {} already recorded".format(run))
        selection = result.get("selection")
        if selection not in PLAN_KEYS:
            raise RoundCapError("arbiter selection must be a true plan key A|B")
        if not _spend(state, "ARBITER " + run):
            return DISP_PAGE
        state["arbiter"][run] = selection
        one, two = state["arbiter"]["1"], state["arbiter"]["2"]
        if one and two:
            if one != two:
                state["page_reason"] = (
                    "position-unstable: swapped arbiter runs disagree "
                    "({} vs {})".format(one, two)
                )
                return DISP_PAGE
            state["selected"] = one
            state["ports"] = int(result.get("ports") or 0)
            return DISP_SELECTED

    else:
        raise RoundCapError("unknown step {!r}".format(step))

    _advance(state)
    return disposition(state)


def disposition(state):
    """The round's current disposition: PAGE / SELECTED / CONTINUE."""
    if state["page_reason"]:
        return DISP_PAGE
    if state["selected"]:
        return DISP_SELECTED
    return DISP_CONTINUE


def page_action(human_held, keep_nondependent=False):
    """The documented failure-semantics action for a PAGE at the declared
    ratification level (SN-029).

    `human_held` is `agent_common.human_holds`' answer — anything unreadable
    already resolved to True there, which is why this takes a bool rather than
    re-deriving one. But `bool(None)` is False, i.e. the MOST PERMISSIVE cell,
    so a caller that passes an un-resolved value reaches the opposite of the
    fail-safe direction this module claims. Since this is an independently
    copyable script with a public API, `None` is normalised here to the
    strictest cell rather than trusted to never arrive."""
    if human_held is None:
        human_held = True
    return _PAGE_ACTIONS[(bool(human_held), bool(keep_nondependent))]


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(description="dual-plan round lifecycle (WI-194)")
    ap.add_argument("command", choices=["walk"], help="print the happy-path walk")
    ap.add_argument("--budget", type=int, default=DEFAULT_ROUND_BUDGET)
    args = ap.parse_args()
    if args.command == "walk":
        state = new_round("demo", budget=args.budget)
        script = [
            (STEP_PLAN, {"plan": "A"}, {"ok": True}),
            (STEP_PLAN, {"plan": "B"}, {"ok": True}),
            (STEP_COVERAGE, {"stage": "coverage1"}, {"findings": False}),
            (STEP_CRITIQUE, {"plan": "A"}, {"verdict": VERDICT_CHANGES}),
            (STEP_CRITIQUE, {"plan": "B"}, {"verdict": VERDICT_CHANGES}),
            (STEP_REVISE, {"plan": "A"}, {"ok": True}),
            (STEP_REVISE, {"plan": "B"}, {"ok": True}),
            (STEP_COVERAGE, {"stage": "coverage2"}, {"findings": False}),
            (STEP_ARBITER, {"run": "1"}, {"selection": "B"}),
            (STEP_ARBITER, {"run": "2"}, {"selection": "B", "ports": 0}),
        ]
        for step, where, result in script:
            disp = record(state, step, **where, **result)
            print(
                "{:9s} {:18s} -> {} (spent {}/{})".format(
                    step,
                    json.dumps(where),
                    disp,
                    state["spent"],
                    state["budget"],
                )
            )
        print("selected={} ports={}".format(state["selected"], state["ports"]))


if __name__ == "__main__":
    main()
