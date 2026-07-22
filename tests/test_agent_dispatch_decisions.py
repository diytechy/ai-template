"""Value-only dispatcher decisions and traincar packing boundaries (WI-226).

These tests deliberately need no repo, Git process, worktree, journal, or worker
session. Effect-level dispatcher and train behavior stays in the corresponding
agent-loop end-to-end modules.
"""

import re

import pytest
from conftest import SCRIPTS, load_script

agent_loop = load_script("agent_loop")
schedule = load_script("schedule")
dispatcher = agent_loop.agent_dispatch
agent_common = load_script("agent_common")
_failure_tail = agent_common._failure_tail


@pytest.mark.parametrize(
    "ihead,dhead,int_ancestor,dev_ancestor,expected",
    [
        ("same", "same", False, False, "publish"),
        ("int", "dev", True, False, "fast-forward"),
        ("int", "dev", False, True, "publish"),
        ("int", "dev", False, False, "needs-human"),
    ],
)
def test_head_reconcile_decision(ihead, dhead, int_ancestor, dev_ancestor, expected):
    assert (
        dispatcher._head_reconcile_decision(ihead, dhead, int_ancestor, dev_ancestor)
        == expected
    )


@pytest.mark.parametrize(
    "wis,built,blocked,expected",
    [
        (("WI-1",), ("WI-1", "WI-9"), (), ("quarantined", ("WI-9",))),
        (("WI-1",), (), ("WI-1",), ("blocked", ())),
        (("WI-1",), ("WI-1",), (), ("ready-to-integrate", ())),
        (("WI-1", "WI-2"), ("WI-1",), (), ("resume", ())),
    ],
)
def test_train_evidence_decision(wis, built, blocked, expected):
    assert dispatcher._train_evidence_decision(wis, built, blocked) == expected


@pytest.mark.parametrize(
    "paused,blacked_out,ask,expected",
    [
        (None, False, "", True),
        ("owner", False, "", False),
        (None, True, "", False),
        (None, False, "page", False),
    ],
)
def test_dispatch_allowed_decision(paused, blacked_out, ask, expected):
    assert dispatcher._dispatch_allowed(paused, blacked_out, ask) is expected


@pytest.mark.parametrize(
    "state,now,retry_at,expected",
    [
        ("resume", 0, 100, True),
        ("waiting", 99, 100, False),
        ("waiting", 100, 100, True),
        ("integrated", 100, 0, False),
    ],
)
def test_retry_due_decision(state, now, retry_at, expected):
    assert dispatcher._retry_due(state, now, retry_at) is expected


@pytest.mark.parametrize(
    "code,spine,policy,expected",
    [
        (
            agent_loop.EXIT_DONE,
            False,
            "attended",
            ("ready-to-integrate", "worker-done", ""),
        ),
        (
            agent_loop.EXIT_DONE,
            True,
            "attended",
            ("ready-to-integrate", "worker-done", "ratify"),
        ),
        (
            agent_loop.EXIT_DONE,
            True,
            "autonomous",
            ("ready-to-integrate", "worker-done", ""),
        ),
        (
            agent_loop.EXIT_BLOCKED,
            False,
            "attended",
            ("blocked", "worker-blocked", "release-unstarted"),
        ),
        (
            agent_loop.EXIT_TRAIN_END,
            False,
            "attended",
            ("train-end", "worker-train-end", "release-unstarted"),
        ),
        (
            agent_loop.EXIT_WAITING,
            False,
            "attended",
            ("waiting", "worker-waiting", "retry"),
        ),
        (
            agent_loop.EXIT_NEEDS_HUMAN,
            False,
            "attended",
            ("needs-human", "worker-needs-human", "page"),
        ),
        (91, False, "attended", ("quarantined", "worker-quarantined", "")),
    ],
)
def test_worker_exit_decision(code, spine, policy, expected):
    assert dispatcher._worker_exit_decision(code, spine, policy) == expected


@pytest.mark.parametrize(
    "result,source,expected",
    [
        ("integrated", "ready-to-integrate", ("integrated", True, False)),
        ("integrated", "blocked", ("blocked-done", True, False)),
        ("recompose", "ready-to-integrate", ("ready-to-integrate", True, False)),
        ("error", "blocked", ("quarantined", False, True)),
        ("rework", "ready-to-integrate", ("rework", False, True)),
    ],
)
def test_integration_result_decision(result, source, expected):
    assert dispatcher._integration_result_decision(result, source) == expected


@pytest.mark.parametrize(
    "paused,ask,blackout,dispatchable,waiting,expected",
    [
        ("owner", "page", True, True, ["t"], "paused"),
        (None, "page", True, True, ["t"], "needs-human"),
        (None, "", True, True, [], "blackout-wait"),
        (None, "", False, False, ["t"], "waiting"),
        (None, "", False, False, [], "drained"),
        (None, "", False, True, [], "poll"),
    ],
)
def test_idle_decision(paused, ask, blackout, dispatchable, waiting, expected):
    assert (
        dispatcher._idle_decision(paused, ask, blackout, dispatchable, waiting)
        == expected
    )


@pytest.mark.parametrize(
    "attention,queued,unpublished,current,blocked,expected",
    [
        (
            ["t"],
            True,
            "new",
            "old",
            True,
            (
                "RUNNING",
                "trains need attention (re-review / rework / quarantine)",
                agent_loop.EXIT_STALL,
            ),
        ),
        (
            [],
            True,
            "new",
            "old",
            True,
            ("RUNNING", "build-out wave complete", agent_loop.EXIT_DONE),
        ),
        (
            [],
            False,
            "new",
            "old",
            True,
            (
                "RUNNING",
                "integration complete; publication deferred",
                agent_loop.EXIT_DONE,
            ),
        ),
        (
            [],
            False,
            "same",
            "same",
            True,
            ("BLOCKED", "run-state=BLOCKED", agent_loop.EXIT_BLOCKED),
        ),
        (
            [],
            False,
            "same",
            "same",
            False,
            ("DONE", "run-state=DONE", agent_loop.EXIT_DONE),
        ),
    ],
)
def test_terminal_decision(attention, queued, unpublished, current, blocked, expected):
    assert (
        dispatcher._terminal_decision(attention, queued, unpublished, current, blocked)
        == expected
    )


def _wi(wid, safety="ordinary", preds=()):
    return {
        "id": wid,
        "status": "queued",
        "preds": list(preds),
        "soft": [],
        "srs": [],
        "priority": 0,
        "exclusive": [],
        "blockref": "",
        "est_tokens": 0,
        "safetyclass": safety,
        "title": "w",
    }


def _pack(wis):
    return dispatcher.pack_traincars(
        schedule.evaluate(wis), {wi["id"]: wi for wi in wis}
    )


def test_unary_chain_packs_to_the_cap():
    wis = [
        _wi("WI-20%d" % index, preds=["WI-20%d" % (index - 1)] if index > 1 else [])
        for index in range(1, 6)
    ]
    assert [car["wis"] for car in _pack(wis)] == [
        ["WI-201", "WI-202", "WI-203", "WI-204"]
    ]


def test_spine_batch_packs_ready_spine_into_one_traincar():
    cars = _pack(
        [
            _wi("WI-210", safety="spine"),
            _wi("WI-211", safety="gate"),
            _wi("WI-212", safety="attestation"),
            _wi("WI-201"),
        ]
    )
    assert cars[0] == {
        "wis": ["WI-210", "WI-211", "WI-212"],
        "sched_class": schedule.SCHED_SPINE_SERIAL,
    }
    assert [car["wis"] for car in cars[1:]] == [["WI-201"]]


def test_spine_batch_absorbs_unlocked_successors_in_hard_edge_order():
    cars = _pack(
        [
            _wi("WI-210", safety="spine"),
            _wi("WI-211", safety="spine", preds=["WI-210"]),
            _wi("WI-220", safety="gate"),
        ]
    )
    assert len(cars) == 1
    assert cars[0]["sched_class"] == schedule.SCHED_SPINE_SERIAL
    assert set(cars[0]["wis"]) == {"WI-210", "WI-211", "WI-220"}
    assert cars[0]["wis"].index("WI-210") < cars[0]["wis"].index("WI-211")


def test_spine_batch_chunks_at_the_cap():
    cars = _pack([_wi("WI-21%d" % index, safety="spine") for index in range(5)])
    assert [car["wis"] for car in cars] == [
        ["WI-210", "WI-211", "WI-212", "WI-213"],
        ["WI-214"],
    ]
    assert all(car["sched_class"] == schedule.SCHED_SPINE_SERIAL for car in cars)


def test_spine_batch_never_packs_other_classes():
    cars = _pack(
        [
            _wi("WI-210", safety="spine"),
            _wi("WI-230", safety="protected"),
            _wi("WI-240", safety="high-risk"),
            _wi("WI-250", safety=""),
        ]
    )
    assert cars[0] == {
        "wis": ["WI-210"],
        "sched_class": schedule.SCHED_SPINE_SERIAL,
    }
    packed = [wid for car in cars for wid in car["wis"]]
    assert "WI-250" not in packed
    assert ["WI-230"] in [car["wis"] for car in cars]
    assert ["WI-240"] in [car["wis"] for car in cars]


def test_dual_row_never_joins_a_multi_wi_traincar():
    rows = []
    for wid, preds, planmode, safety in (
        ("WI-201", "", "dual", ""),
        ("WI-202", "WI-201", "", "ordinary"),
        ("WI-203", "WI-202", "", "ordinary"),
    ):
        rows.append(
            {
                "WI-ID": wid,
                "Title": wid,
                "Status": "queued",
                "Predecessors": preds,
                "SafetyClass": safety,
                "PlanMode": planmode,
            }
        )
    wis = schedule.load_wis(rows)
    cars = _pack(wis)
    dual_cars = [car for car in cars if "WI-201" in car["wis"]]
    assert dual_cars == [{"wis": ["WI-201"], "sched_class": schedule.SCHED_SINGLE_WI}]


# --- WI-240: park/quarantine details carry the FAILING step, not the head -------

# The exact WI-229 field string: a commit-hook `check.py --run-steps` output
# whose FIRST banner is a PASSING `=== derived-gate : <long python.exe cmd> ===`
# and whose real failure is a later `trajectory` step. The old `out[:200]` head
# cut kept the derived-gate banner and dropped the error; the helper must invert
# that.
WI229_HOOK_OUT = (
    "\n=== arch-map : python check.py --run-step arch-map ===\n"
    "  PASS  arch-map         0.2s\n"
    "\n=== derived-gate : C:/Users/x/.venv/Scripts/python.exe derive_gate.py "
    "--check --root . ===\n"
    "  PASS  derived-gate     0.1s\n"
    "\n=== trajectory : C:/Users/x/.venv/Scripts/python.exe check_trajectory.py "
    "--root . ===\n"
    "check_trajectory: ERROR - blocked-ref WI-229: status=blocked but BlockRef "
    "is empty\n"
    "  FAIL  trajectory       exit 1 (0.3s)\n"
)


def test_failure_tail_extracts_failing_step_not_first_banner():
    tail = _failure_tail(WI229_HOOK_OUT)
    # Names the failing step and its error line ...
    assert "  FAIL  trajectory" in tail
    assert "blocked-ref WI-229: status=blocked but BlockRef is empty" in tail
    # ... and DROPS the earlier passing banner that the [:200] head kept.
    assert "derived-gate" not in tail
    assert "arch-map" not in tail
    assert len(tail) <= 600


def test_failure_tail_single_line_passes_through():
    line = "fatal: nothing to commit, working tree clean"
    assert _failure_tail(line) == line


def test_failure_tail_no_fail_marker_is_bounded_tail_not_head():
    body = "FIRSTLINE\n" + "\n".join("row %d" % i for i in range(300))
    tail = _failure_tail(body, budget=40)
    assert "FIRSTLINE" not in tail  # never the head
    assert "row 299" in tail  # the tail survives
    assert len(tail) <= 40
    # Empty / None degrade to "", never crash a journal call.
    assert _failure_tail("") == ""
    assert _failure_tail(None) == ""


def test_every_dispatcher_family_detail_routes_through_failure_tail():
    """Census (mirrors test_fault_points_exist_for_every_matrix_boundary): no
    park/quarantine/journal detail in the dispatcher family may head-slice a
    harness/git output. Every `[:200]` on a failure detail is gone; the lone
    survivor is a SUCCESS event's path-LIST bound (integration-regenerated),
    which is not a failure tail."""
    disp = (SCRIPTS / "agent_dispatch.py").read_text(encoding="utf-8")
    common = (SCRIPTS / "agent_common.py").read_text(encoding="utf-8")
    surviving = re.findall(r"[\w.\"')\]]*\[:200\]", disp)
    assert len(surviving) == 1 and all("regenerated" in s for s in surviving), surviving
    assert "[:200]" not in common, "agent_common failure details must tail, not head"
    # And the helper is actually wired in at the failure sites, not just present.
    assert disp.count("_failure_tail(") >= 12
    assert "_failure_tail(out)" in common or "_failure_tail" in common


# --- WI-260: the verdict-gate required-phase classifier (design 1 + 3) --------


def _write_docs(tmp_path, srrefs="SR-063", critique=False):
    docs = tmp_path / "docs"
    (docs / "requirements").mkdir(parents=True)
    (docs / "requirements" / "work-items.csv").write_text(
        "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable,"
        "SpecRef,BuildTier,SafetyClass\n"
        "WI-201,Work,ws,{},,queued,,,medium,ordinary\n".format(srrefs),
        encoding="utf-8",
    )
    if critique:
        (docs / "requirements" / "system-requirements.csv").write_text(
            "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
            "Permutations,Priority,Verification,Status\n"
            "SR-050,Render,SN-001,req,rat,ac,,S,Critique,Verified\n",
            encoding="utf-8",
        )
    return docs


@pytest.mark.parametrize(
    "managed,rp_int,render,expected",
    [
        (False, 2, True, set()),  # unmanaged routing schedules nothing
        (True, 0, False, set()),  # dial-0 scripts: no verdict phase
        (True, 1, False, {"REVIEW-A"}),  # the dial counts REVIEWERS only
        (True, 2, False, {"REVIEW-A", "REVIEW-B"}),
        (True, 0, True, {"CRITIQUE"}),  # dial-0 render: critique alone gates
        (True, 1, True, {"REVIEW-A", "CRITIQUE"}),  # critique is orthogonal
        (True, 2, True, {"REVIEW-A", "REVIEW-B", "CRITIQUE"}),
    ],
)
def test_required_phases_classifier(tmp_path, managed, rp_int, render, expected):
    # The gate's required set is a pure function of the SAME dials the scheduler
    # reads (design 1: they cannot disagree) — REVIEW-A/B by the reviewer dial,
    # CRITIQUE orthogonally on a render-surface train (design 3).
    docs = _write_docs(
        tmp_path, srrefs="SR-050" if render else "SR-063", critique=render
    )
    got = dispatcher._required_phases(docs, ["WI-201"], (managed, rp_int))
    assert got == expected


def test_render_surface_is_delivering_a_critique_sr_not_merely_touching_one(tmp_path):
    # render-surface == the train DELIVERS a Critique-verified SR; a WI whose
    # SR-Refs name only a non-critique SR is not render-surface.
    render_docs = _write_docs(tmp_path / "a", srrefs="SR-050", critique=True)
    scripts_docs = _write_docs(tmp_path / "b", srrefs="SR-063", critique=True)
    assert dispatcher._train_is_render_surface(render_docs, ["WI-201"]) is True
    assert dispatcher._train_is_render_surface(scripts_docs, ["WI-201"]) is False
    # No critique SR anywhere -> the classifier is vacuous (non-adopter pays 0).
    plain = _write_docs(tmp_path / "c", srrefs="SR-050", critique=False)
    assert dispatcher._train_is_render_surface(plain, ["WI-201"]) is False
