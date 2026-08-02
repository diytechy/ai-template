"""dispatch.py admission — the spine barrier + the §A8 policy table (WI-381).

The dispatcher's ONE scheduling decision, pinned as a pure function so the
barrier semantics are driven without a git repo or a subprocess in sight (the
loop around it is tests/test_dispatch.py's, on real repos):

  * an exclusive-kind row on the frontier STOPS new admission — with lanes
    busy the answer is WAIT, never a parallel claim slipped past the barrier;
  * lanes back in the station -> ALL spine rows admit TOGETHER as one batch
    (one branch, one worker session, one re-attest window);
  * the §A8 kind x gate-policy table exactly as ruled: ordinary/critique
    parallel at every level, high-risk/protected exclusive at every level,
    spine dispatches at every level (building a scope change is WORK, not a
    ratification), attestation/gate does NOT dispatch under `attended` (drain,
    surface the cards, exit 0), dispatches only as the queued batch once
    nothing else remains under `single-ratify`, and dispatches under
    `autonomous` (a recorded fresh-context reviewer verdict ratifies);
  * the lanes dial resolves on the established ladder (CLI > AGENT_LANES >
    stack.ini [agent-loop] > code default) and an ABSENT key means 1 — the
    template seeds 2, but no long-adopted repo is upgraded into concurrency
    silently (docs/stack.ini is adopter-owned; §A4.3).

`schedule.kind_of` is pinned beside it because the admission table is keyed by
KIND: the resolution must agree with `classify` (one home, not a re-parse of
reason codes).
"""

import argparse

from conftest import load_script

dsp = load_script("dispatch")
sched = load_script("schedule")


def _wi(wid, safety, planmode="", critique=False):
    return {
        "id": wid,
        "safetyclass": safety,
        "planmode": planmode,
        "critique": critique,
    }


# --- schedule.kind_of agrees with classify (one resolution home) --------------


def test_kind_of_resolves_the_same_kind_classify_keys_its_tables_by():
    assert sched.kind_of(_wi("WI-1", "ordinary")) == "ordinary"
    assert sched.kind_of(_wi("WI-1", "spine")) == "spine"
    assert sched.kind_of(_wi("WI-1", "gate")) == "gate"
    assert sched.kind_of(_wi("WI-1", "", planmode="dual")) == "high-risk"
    assert sched.kind_of(_wi("WI-1", "ordinary", critique=True)) == "critique"
    # A declared exclusive kind wins over the critique flag (classify step 4).
    assert sched.kind_of(_wi("WI-1", "spine", critique=True)) == "spine"


def test_kind_of_fails_closed_exactly_where_classify_quarantines():
    quarantined = [
        _wi("WI-1", ""),  # missing
        _wi("WI-1", "bogus"),  # unknown value
        _wi("WI-1", "spine", planmode="dual"),  # contradicts the derivation
    ]
    for wi in quarantined:
        assert sched.kind_of(wi) is None
        assert sched.classify(wi)[0] == sched.CONCURRENCY_UNCLASSIFIED
    # ...and the structural contradiction quarantines through the same keyword.
    assert sched.kind_of(_wi("WI-1", "ordinary"), structural="spine") is None


# --- the §A8 policy table, verbatim ------------------------------------------


def test_the_kind_action_table_is_a8_verbatim():
    for level in ("attended", "single-ratify", "autonomous"):
        assert dsp._kind_action("ordinary", level) == "parallel"
        assert dsp._kind_action("critique", level) == "parallel"
        assert dsp._kind_action("high-risk", level) == "exclusive"
        assert dsp._kind_action("protected", level) == "exclusive"
        # spine dispatches at EVERY level: building a scope change is WORK,
        # not a ratification — it opens a window; closing it is the next
        # row's job.
        assert dsp._kind_action("spine", level) == "batch"
    for kind in ("attestation", "gate"):
        assert dsp._kind_action(kind, "attended") == "surface"
        assert dsp._kind_action(kind, "single-ratify") == "surface"
        assert dsp._kind_action(kind, "autonomous") == "exclusive"


# --- the barrier: batch-and-wait ---------------------------------------------


def test_an_exclusive_row_with_a_busy_lane_does_not_admit():
    # THE BARRIER. A spine row on the frontier stops the dispatcher admitting
    # new work — including the ordinary rows behind it — while a lane is busy.
    ready = [("WI-500", "spine"), ("WI-401", "ordinary")]
    verb, payload = dsp._admission(ready, "autonomous", busy=True, free=1)
    assert verb == "wait"
    # ...and the same frontier with NO exclusive row keeps filling lanes.
    verb, payload = dsp._admission(
        [("WI-401", "ordinary")], "autonomous", busy=True, free=1
    )
    assert verb == "admit" and payload == [["WI-401"]]


def test_lanes_back_in_the_station_the_spine_batch_admits_together():
    # N spine changes cost ONE re-attest window and one owner sitting: every
    # spine row on the frontier admits as ONE batch (agent_loop --wi 'A;B'),
    # ahead of the ordinary work behind it.
    ready = [("WI-500", "spine"), ("WI-501", "spine"), ("WI-401", "ordinary")]
    verb, payload = dsp._admission(ready, "attended", busy=False, free=2)
    assert verb == "admit-exclusive"
    assert payload == ["WI-500", "WI-501"]


def test_high_risk_admits_alone_not_batched():
    ready = [("WI-500", "high-risk"), ("WI-501", "high-risk")]
    verb, payload = dsp._admission(ready, "autonomous", busy=False, free=2)
    assert verb == "admit-exclusive"
    assert payload == ["WI-500"]


def test_parallel_rows_fill_free_lanes_in_frontier_order():
    ready = [("WI-401", "ordinary"), ("WI-402", "ordinary"), ("WI-403", "critique")]
    verb, payload = dsp._admission(ready, "autonomous", busy=True, free=2)
    assert verb == "admit"
    assert payload == [["WI-401"], ["WI-402"]]


def test_attended_attestation_surfaces_instead_of_dispatching():
    # §A8 attended row: do not dispatch — drain the lanes, surface the cards,
    # exit 0 into the owner's queue. Ordinary rows behind it do NOT slip past:
    # today's behaviour the owner confirmed must keep working is "no work can
    # be taken" once a ratification is pending.
    ready = [("WI-600", "gate"), ("WI-401", "ordinary")]
    verb, payload = dsp._admission(ready, "attended", busy=False, free=1)
    assert verb == "surface"
    assert payload == ["WI-600"]


def test_single_ratify_keeps_non_dependent_work_running():
    # §A8 single-ratify: keep working non-dependent WIs; the queued batch
    # dispatches only at the close, when nothing else remains.
    ready = [("WI-600", "attestation"), ("WI-401", "ordinary")]
    verb, payload = dsp._admission(ready, "single-ratify", busy=False, free=1)
    assert verb == "admit" and payload == [["WI-401"]]
    # The close: only the queued ratification batch remains, lanes idle.
    verb, payload = dsp._admission(
        [("WI-600", "attestation"), ("WI-601", "gate")],
        "single-ratify",
        busy=False,
        free=1,
    )
    assert verb == "admit-exclusive" and payload == ["WI-600", "WI-601"]
    # ...but not while a lane is still out.
    verb, _payload = dsp._admission(
        [("WI-600", "attestation")], "single-ratify", busy=True, free=1
    )
    assert verb == "wait"


def test_autonomous_gate_rows_dispatch_exclusive():
    ready = [("WI-600", "gate"), ("WI-401", "ordinary")]
    verb, payload = dsp._admission(ready, "autonomous", busy=False, free=1)
    assert verb == "admit-exclusive" and payload == ["WI-600"]


def test_an_empty_frontier_answers_empty():
    assert dsp._admission([], "attended", busy=False, free=1) == ("empty", [])


# --- the lanes dial ladder (§A4.3) -------------------------------------------


def _args(lanes=None):
    return argparse.Namespace(lanes=lanes)


def test_lanes_absent_key_means_one(tmp_path, monkeypatch):
    # The ruled split: the TEMPLATE seeds lanes = 2, but an absent key means 1
    # — docs/stack.ini is adopter-owned, so a re-sync never writes the key and
    # a code default of 2 would upgrade a long-adopted repo into concurrency
    # silently. Nobody is upgraded into concurrency they did not ask for.
    monkeypatch.delenv("AGENT_LANES", raising=False)
    assert dsp._lane_count(_args(), tmp_path) == 1


def test_lanes_ladder_cli_over_env_over_stack_ini(tmp_path, monkeypatch):
    ini = tmp_path / "docs" / "stack.ini"
    ini.parent.mkdir(parents=True, exist_ok=True)
    ini.write_text("[agent-loop]\nlanes = 3\n", encoding="utf-8", newline="\n")
    monkeypatch.delenv("AGENT_LANES", raising=False)
    assert dsp._lane_count(_args(), tmp_path) == 3
    monkeypatch.setenv("AGENT_LANES", "4")
    assert dsp._lane_count(_args(), tmp_path) == 4
    assert dsp._lane_count(_args(lanes=5), tmp_path) == 5


def test_lanes_malformed_or_sub_one_values_fall_to_serial(tmp_path, monkeypatch):
    monkeypatch.setenv("AGENT_LANES", "many")
    assert dsp._lane_count(_args(), tmp_path) == 1
    monkeypatch.setenv("AGENT_LANES", "0")
    assert dsp._lane_count(_args(), tmp_path) == 1
