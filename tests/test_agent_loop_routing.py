"""agent_loop.py — RoutingState transitions and the session-outcome ladder
(WI-277: split verbatim from tests/test_agent_loop.py by behavior boundary).

Pure decision, in process: the RoutingState phase pick, route_intent family
exclusions and tier pins, apply_decision (swap / tier-up / page / next-primary),
the critique and review verdict bookkeeping, note_session/stall_verdict, the
win-stay policy executed end to end with the REAL functions, and the
classify_outcome ladder.
"""

import pytest
from conftest import load_script


# =============================================================================
# WI-080 Slice C — RoutingState transitions
# =============================================================================
# The serial loop's ~24 routing/escalation/critique/stall locals now live on one
# RoutingState whose methods are PURE transitions (mutate the object, return a
# decision — no I/O). These pin single transitions directly; the end-to-end
# routing/critique/stall behavior is still pinned by the golden-net suites in
# tests/test_agent_loop.py.  (WI-277 repointed 'above' at the split.)


def _rs(rp_int=1, cooldown_seconds=900, critique_srs=None, critique_max=3):
    """A RoutingState with defaults for a single-transition test."""
    al = load_script("agent_loop")
    return al.RoutingState(
        rp_int, cooldown_seconds, critique_srs or set(), critique_max, {}
    )


def test_routingstate_pick_phase_precedence():
    st = _rs()
    # Default: the held next_phase (BUILD), no review/critique.
    assert st.pick_phase() == ("BUILD", False, False)
    # A queued critique wins over the default.
    st.critique_queue = ["CRITIQUE"]
    assert st.pick_phase() == ("CRITIQUE", False, True)
    # A queued review phase wins over a queued critique (reviews drain first).
    st.review_queue = ["REVIEW-A", "REVIEW-B"]
    assert st.pick_phase() == ("REVIEW-A", True, False)


def test_routingstate_route_intent_review_excludes_impl_and_verdict_families():
    st = _rs()
    st.last_impl_family = "anthropic"
    st.round_verdicts = [("REVIEW-A", object(), "openai", "id-a")]
    tier, exclude, prefer = st.route_intent("REVIEW-A", True, False, {})
    assert prefer is True
    assert exclude == {"anthropic", "openai"}
    # A fresh set each call — mutating the returned set never bleeds into state.
    exclude.add("google")
    _t2, exclude2, _p2 = st.route_intent("REVIEW-A", True, False, {})
    assert exclude2 == {"anthropic", "openai"}


def test_routingstate_route_intent_critique_prefers_different_family():
    st = _rs()
    st.last_impl_family = "anthropic"
    tier, exclude, prefer = st.route_intent("CRITIQUE", False, True, {})
    assert prefer is True
    assert exclude == {"anthropic"}


def test_routingstate_route_intent_build_pins_tier():
    st = _rs()
    # phase_tier(BUILD) defaults to medium; the worker pin replaces it.
    tier, exclude, prefer = st.route_intent(
        "BUILD", False, False, {}, pinned_tier="strong"
    )
    assert tier == "strong"
    assert exclude == set()
    assert prefer is False


def test_routingstate_route_intent_build_override_beats_pin():
    st = _rs()
    st.impl_tier_override = "strong"
    tier, _exclude, _prefer = st.route_intent(
        "BUILD", False, False, {}, pinned_tier="quick"
    )
    assert tier == "strong"  # escalation override wins over the per-WI pin


def test_routingstate_route_intent_build_impl_exclude():
    st = _rs()
    st.impl_exclude = {"anthropic"}
    tier, exclude, prefer = st.route_intent("", False, False, {})
    assert exclude == {"anthropic"}
    assert prefer is True


def test_routingstate_route_intent_design_check():
    st = _rs()
    st.last_impl_family = "anthropic"
    tier, exclude, prefer = st.route_intent("DESIGN-CHECK", False, False, {})
    assert tier == "strong"  # DEFAULT_PHASE_TIER routes design-check strong
    assert exclude == {"anthropic"}
    assert prefer is True


def test_routingstate_apply_decision_swap():
    st = _rs()
    st.last_impl_family = "anthropic"
    st.critique_queue = ["CRITIQUE"]
    st.next_phase = "DESIGN-CHECK"
    st.apply_decision("swap-implementer", "CHANGES-REQUESTED")
    assert st.impl_exclude == {"anthropic"}
    assert st.swapped is True
    assert st.critique_queue == []  # the artifact will change; re-critique later
    assert st.next_phase == "BUILD"


def test_routingstate_apply_decision_tier_up():
    st = _rs()
    st.critique_queue = ["CRITIQUE"]
    st.apply_decision("tier-up", "CHANGES-REQUESTED")
    assert st.impl_tier_override == "strong"
    assert st.at_top_tier is True
    assert st.critique_queue == []
    assert st.next_phase == "BUILD"


def test_routingstate_apply_decision_page_rearms_fail_tally():
    st = _rs()
    st.rounds = [{}, {}, {}]
    st.next_phase = "BUILD"
    st.critique_queue = ["CRITIQUE"]
    st.apply_decision("page-human", "CHANGES-REQUESTED")
    # Re-armed to the current round count; nothing else touched (the page path's
    # I/O — failure_action / banner / run-state — stays with the caller).
    assert st.page_fails_since == 3
    assert st.next_phase == "BUILD"
    assert st.critique_queue == ["CRITIQUE"]


def test_routingstate_apply_decision_stores_and_clears_next_primary():
    # WI-264 (M-34): apply_decision must CONSUME the escalation's next_primary so
    # the win-stay directive reaches the draw — the wiring gap the finding named.
    # A win stores the winning reviewer family; the next decision refreshes it,
    # and a loss/page/swap (next_primary None) clears it (lose-shift).
    st = _rs()
    assert st.next_primary is None  # nothing decided yet
    st.apply_decision("continue", "APPROVE", "OPENAI")
    assert st.next_primary == "OPENAI"  # win-stay: remembered for the next draw
    st.apply_decision("continue", "APPROVE", "GOOGLE")
    assert st.next_primary == "GOOGLE"  # refreshed every round
    st.apply_decision("swap-implementer", "CHANGES-REQUESTED")  # None by default
    assert st.next_primary is None  # lose-shift: cleared, weighted baseline stands


def test_winstay_policy_executes_end_to_end_in_process(tmp_path):
    # WI-264: the whole seam the loop wires, exercised in-process with the REAL
    # functions in the loop's exact order — escalate -> apply_decision ->
    # winstay_preferred_ids -> the review draw's composed preferred_ids -> select.
    # Proves the documented win-stay/lose-shift POLICY executes (not prose-only).
    route = load_script("agent_route")
    reg_csv = (
        "Id,Family,Model,Version,Tier,CmdTemplate,Env,Notes\n"
        "PROVA-BUILD,PROVA,builda,1,medium,cli {prompt},,impl\n"
        "PROVB-REV,PROVB,revb,1,medium,cli {prompt},,\n"
        "PROVC-REV,PROVC,revc,1,medium,cli {prompt},,\n"
        "PROVD-REV,PROVD,revd,1,medium,cli {prompt},,\n"
    )
    (tmp_path / "agents.csv").write_text(reg_csv, encoding="utf-8")
    reg, errs = route.load_registry(tmp_path / "agents.csv")
    assert errs == []
    enabled = ["PROVA-BUILD", "PROVB-REV", "PROVC-REV", "PROVD-REV"]
    # The WI-263 weighted baseline for the REVIEW draw rotates PROVB:PROVD 1:2
    # (unequal shares -> a real rotation: counter 0 -> PROVB, counter 1 -> PROVD),
    # PROVC held out (0 = fallback-only).
    weights = {"PROVB-REV": 1, "PROVD-REV": 2, "PROVC-REV": 0}

    def draw(st, counter):
        # The loop's exact review-draw composition (agent_loop.py): win-stay
        # preferred_ids FIRST (override), then the phase pin (none here); both
        # over the different-family pool (REVIEW excludes the PROVA implementer).
        winstay = route.winstay_preferred_ids(st.next_primary, enabled, reg)
        chosen, _ = route.select(
            enabled,
            reg,
            "medium",
            exclude_families=["PROVA"],
            prefer_different=True,
            preferred_ids=list(winstay),
            weights=weights,
            counter=counter,
        )
        return chosen

    st = _rs()
    # SHIFT baseline first: with nothing decided, the weighted rotation governs
    # (counter 0 -> PROVB, counter 1 -> PROVD).
    assert draw(st, 0) == "PROVB-REV" and draw(st, 1) == "PROVD-REV"
    # A WIN whose primary is PROVB (producible margin 0.3 >= the 0.15 default).
    decision = route.escalate(
        [{"verdict": "APPROVE", "tier": "medium", "margin": 0.3, "primary": "PROVB"}],
        route.DEFAULT_CONSTANTS,
    )
    st.apply_decision(decision["action"], "APPROVE", decision.get("next_primary"))
    assert st.next_primary == "PROVB"
    # STAY: the very draw the baseline would send to PROVD (counter 1) now stays
    # on the winner PROVB — win-stay OVERRODE the weighted baseline.
    assert draw(st, 1) == "PROVB-REV"
    # SHIFT: a sub-threshold next round clears the directive; the draw returns to
    # the weighted baseline (counter 1 -> PROVD), never wedging.
    loss = route.escalate(
        [{"verdict": "APPROVE", "tier": "medium", "margin": 0.05, "primary": "PROVB"}],
        route.DEFAULT_CONSTANTS,
    )
    st.apply_decision(loss["action"], "APPROVE", loss.get("next_primary"))
    assert st.next_primary is None
    assert draw(st, 1) == "PROVD-REV"


def test_routingstate_record_critique_verdict_rework():
    st = _rs()
    st.critique_limit = 3
    st.critique_queue = ["CRITIQUE"]
    assert st.record_critique_verdict("CHANGES-REQUESTED") == "rework"
    assert st.critique_rounds == 1
    assert st.next_phase == "BUILD"
    assert st.critique_queue == []  # the round is consumed


def test_routingstate_record_critique_verdict_pages_at_budget():
    st = _rs()
    st.critique_limit = 2
    st.critique_rounds = 1  # one prior CHANGES-REQUESTED round
    st.critique_scope = {"SR-1"}
    assert st.record_critique_verdict("CHANGES-REQUESTED") == "page"
    # Reset on page so the next scope starts fresh.
    assert st.critique_rounds == 0
    assert st.critique_scope == set()


def test_routingstate_record_critique_verdict_infinite_budget_never_pages():
    st = _rs()
    st.critique_limit = None  # inf-until-APPROVE
    st.critique_rounds = 99
    assert st.record_critique_verdict("CHANGES-REQUESTED") == "rework"
    assert st.critique_rounds == 100


def test_routingstate_record_critique_verdict_approved_resets_scope():
    st = _rs()
    st.critique_scope = {"SR-1"}
    st.critique_rounds = 2
    assert st.record_critique_verdict("APPROVE") == "approved"
    assert st.critique_rounds == 0
    assert st.critique_scope == set()


def test_routingstate_schedule_critique_new_scope_resets_same_scope_preserves():
    st = _rs()
    st.critique_scope = {"SR-1"}
    st.critique_rounds = 2
    # A NEW scope starts a fresh budget.
    st.schedule_critique({"SR-2"}, 3, "move-on")
    assert st.critique_rounds == 0
    assert st.critique_scope == {"SR-2"}
    assert st.critique_queue == ["CRITIQUE"]
    assert st.critique_limit == 3
    assert st.critique_exhaustion == "move-on"
    # The SAME scope (a rework loop) preserves the count so the budget bounds it.
    st.critique_rounds = 2
    st.schedule_critique({"SR-2"}, 5, "block")
    assert st.critique_rounds == 2
    assert st.critique_exhaustion == "block"


def test_routingstate_schedule_review_round_by_policy():
    # rp 1 queues REVIEW-A only; rp 2 adds REVIEW-B; both clear round_verdicts.
    st1 = _rs(rp_int=1)
    st1.round_verdicts = [("x", object(), "f", "id")]
    assert st1.schedule_review_round() == ["REVIEW-A"]
    assert st1.review_queue == ["REVIEW-A"]
    assert st1.round_verdicts == []
    st2 = _rs(rp_int=2)
    assert st2.schedule_review_round() == ["REVIEW-A", "REVIEW-B"]
    # rp 0: the CALLER's schedule_review (rp_int >= 1) gate means the method is
    # never invoked, so review-policy 0 schedules no round.


def test_routingstate_record_review_verdict_pops_and_round_ready():
    st = _rs()
    st.review_queue = ["REVIEW-A", "REVIEW-B"]
    assert st.round_ready() is False  # no verdicts collected yet
    st.record_review_verdict("REVIEW-A", object(), "anthropic", "id-a")
    assert st.review_queue == ["REVIEW-B"]
    assert st.round_ready() is False  # queue not yet drained
    st.record_review_verdict("REVIEW-B", object(), "openai", "id-b")
    assert st.review_queue == []
    assert len(st.round_verdicts) == 2
    assert st.round_ready() is True


def test_routingstate_note_session_and_stall_verdict():
    st = _rs()
    # A no-commit session increments the stall; an ERROR qualifies the run.
    st.note_session(committed=False, errored=True)
    st.note_session(committed=False, errored=True)
    st.note_session(committed=False, errored=True)
    assert st.stall == 3
    assert st.errors == 3
    assert st.stall_verdict(3) == "agent-error"  # every stalled session errored
    # A NO-COMMIT (non-error) run at the limit is a plain work stall.
    st.errors = 1
    assert st.stall_verdict(3) == "stall"
    # Below the limit: keep going.
    assert st.stall_verdict(4) is None
    # A commit resets both counters.
    st.note_session(committed=True, errored=False)
    assert st.stall == 0
    assert st.errors == 0
    assert st.stall_verdict(1) is None


# --- WI-080 Slice D: the session-outcome ladder + worker end-state as module ---
# functions. classify_outcome (the outcome/errored ladder) and worker_endstate /
# worker_exit_banner (the worker's committed-evidence disposition) were extracted
# from main() to module level, unit-addressable without a coordinator run.
# (WI-277 kept the ladder here and moved the worker_endstate/worker_exit_banner
# half of this Slice to tests/test_agent_loop_worker.py, with the worker leg.)


@pytest.mark.parametrize(
    "args,expected",
    [
        # A rate limit wins as WAITING over everything — even timed_out True and
        # committed True — and never reads as errored (reset_hint gates it).
        (
            ("resets 3:45pm", True, "DONE", True, {"is_error": True}, 1),
            ("WAITING", False),
        ),
        # A timeout is its own outcome and beats a declared end-state.
        ((None, True, "DONE", False, {}, 0), ("TIMEOUT", False)),
        # Each declared end-state passes through (a healthy run-state commit).
        ((None, False, "DONE", True, {"is_error": False}, 0), ("DONE", False)),
        ((None, False, "BLOCKED", True, {"is_error": False}, 0), ("BLOCKED", False)),
        (
            (None, False, "NEEDS-JUDGEMENT", True, {"is_error": False}, 0),
            ("NEEDS-JUDGEMENT", False),
        ),
        # A commit with no end-state -> COMMITTED, not errored.
        ((None, False, "RUNNING", True, {}, 0), ("COMMITTED", False)),
        # is_error JSON -> ERROR + errored, even on a zero exit code.
        ((None, False, "RUNNING", False, {"is_error": True}, 0), ("ERROR", True)),
        # No JSON ({} — parse_json_result's "nothing parsed" signal) + nonzero
        # exit -> ERROR + errored (covers run_session's OSError sentinel).
        ((None, False, "RUNNING", False, {}, 1), ("ERROR", True)),
        # A healthy session that simply idled -> NO-COMMIT, not errored.
        ((None, False, "RUNNING", False, {"is_error": False}, 0), ("NO-COMMIT", False)),
    ],
)
def test_classify_outcome_ladder(args, expected):
    al = load_script("agent_loop")
    assert al.classify_outcome(*args) == expected
