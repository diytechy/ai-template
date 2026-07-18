"""Value-only dispatcher decisions and traincar packing boundaries (WI-226).

These tests deliberately need no repo, Git process, worktree, journal, or worker
session. Effect-level dispatcher and train behavior stays in the corresponding
agent-loop end-to-end modules.
"""

import pytest
from conftest import load_script

agent_loop = load_script("agent_loop")
schedule = load_script("schedule")
dispatcher = agent_loop.agent_dispatch


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
