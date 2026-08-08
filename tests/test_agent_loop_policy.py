"""agent_loop.py — the declared-policy parsers and the coordinator dials
(WI-277: split verbatim from tests/test_agent_loop.py by behavior boundary).

The pure parse/decision half of the coordinator's configuration surface: the
tracked pause declaration, the WI-148 weekday blackout window (edges, wake
boundary, the wrap past midnight) and its WI-261 banner/countdown feedback, the
rate-limit `seconds_until_reset` clock readings, the one-rule declared-policy
file parser, `parse_map`, the WI-080 Slice B session-construction seams, the
WI-274/IF-068 single-home dial precedence, and the ungated Slice D/E main()
seams. No fake agent, no loop_repo, no git — every test here calls the function
directly, which is also why this module carries NO module-wide gate.
"""

import argparse
import datetime
import sys

import pytest
from conftest import load_script


def _vendor_core(repo, body):
    """Vendor a guardrails core.md (the tests/test_agent_loop.py helper, copied
    rather than imported — no test module in this suite imports another, and
    conftest is not this module's to extend; WI-277 kept that idiom when
    splitting the monolith). The parent still has its own copy."""
    gdir = repo / "docs" / "guardrails"
    gdir.mkdir(parents=True, exist_ok=True)
    (gdir / "core.md").write_text(body, encoding="utf-8")


# --- §5.6: the TRACKED pause declaration (docs/work/pause) --------------------
# `docs/concurrency-restructure.md` §5.6: the pause lives in the tree — TOML
# `reason` + `since`, presence pauses, an unpause is a deletion COMMIT. The
# legacy untracked `lane/pause` half (WI-147) retired with the dispatcher at
# Phase 5; `pause_reason` keeps its exact return contract (None / "" / reason)
# against the one tracked home.


def _tracked_pause(docs, body):
    (docs / "work").mkdir(parents=True, exist_ok=True)
    (docs / "work" / "pause").write_text(body, encoding="utf-8")


def test_tracked_pause_reads_reason_and_since(tmp_path):
    ac = load_script("agent_common")
    assert ac.tracked_pause(tmp_path) is None  # absent -> not paused
    _tracked_pause(
        tmp_path, 'reason = "draining for the audit"\nsince = "2026-07-29"\n'
    )
    assert ac.tracked_pause(tmp_path) == {
        "reason": "draining for the audit",
        "since": "2026-07-29",
    }
    # `since` is optional; a missing one reads "" (never a clock-derived age).
    _tracked_pause(tmp_path, 'reason = "draining"\n')
    assert ac.tracked_pause(tmp_path) == {"reason": "draining", "since": ""}


def test_tracked_pause_fails_closed_on_malformation(tmp_path):
    # A pause file we cannot read is STILL a pause: unparseable TOML and a
    # missing `reason` both return a paused dict carrying the loud message that
    # routes the human to the fix — never None, which would resume the loop.
    ac = load_script("agent_common")
    for body in ("this is not toml at all\n", 'since = "2026-07-29"\n', "reason = 7\n"):
        _tracked_pause(tmp_path, body)
        assert ac.tracked_pause(tmp_path) == {"reason": ac.PAUSE_MALFORMED, "since": ""}
        assert load_script("agent_loop").pause_reason(tmp_path) == ac.PAUSE_MALFORMED


def test_pause_reason_reads_the_tracked_home(tmp_path):
    al, ac = load_script("agent_loop"), load_script("agent_common")
    assert al.pause_reason(tmp_path) is None  # neither home -> not paused
    _tracked_pause(
        tmp_path, 'reason = "draining for the audit"\nsince = "2026-07-29"\n'
    )
    assert al.pause_reason(tmp_path) == "draining for the audit"
    # An empty declared reason is "paused, no reason" — the same `""` the legacy
    # empty file yields, so callers branching on `is None` are unaffected.
    _tracked_pause(tmp_path, 'reason = ""\nsince = "2026-07-29"\n')
    assert al.pause_reason(tmp_path) == ""
    assert ac.tracked_pause(tmp_path)["reason"] == ""


def test_legacy_pause_file_no_longer_pauses(tmp_path):
    # The legacy untracked `lane/pause` retired at Phase 5: a stray local file
    # must NOT pause (the one meaning lives in the tracked home), and the
    # tracked declaration still does.
    al = load_script("agent_loop")
    (tmp_path / "pause").write_text("local hold\n", encoding="utf-8")
    assert al.pause_reason(tmp_path) is None  # stray legacy file is inert
    _tracked_pause(tmp_path, 'reason = "tracked drain"\nsince = "2026-07-29"\n')
    assert al.pause_reason(tmp_path) == "tracked drain"
    (tmp_path / "work" / "pause").unlink()
    assert al.pause_reason(tmp_path) is None  # deletion commit resumes


# --- WI-148: weekday blackout window ------------------------------------------


def test_parse_blackout_edges():
    al = load_script("agent_loop")
    assert al.parse_blackout("12:00-19:00") == (720, 1140)
    assert al.parse_blackout("  09:30 - 17:45  ") == (570, 1065)
    assert al.parse_blackout("00:00-00:00") == (0, 0)  # parsed; disable is policy
    assert al.parse_blackout("") is None  # empty
    assert al.parse_blackout("not-a-window") is None  # malformed
    assert al.parse_blackout("24:00-19:00") is None  # hour out of range
    assert al.parse_blackout("12:60-19:00") is None  # minute out of range


def test_blackout_wake_boundary_minutes():
    al = load_script("agent_loop")
    line = "12:00-19:00"
    # A Monday (weekday 0) so the window is active.
    mon = datetime.datetime(2026, 7, 13)  # 2026-07-13 is a Monday

    def at(h, m, s=0):
        return mon.replace(hour=h, minute=m, second=s)

    # Half-open [start, end): the first minute is inside, `end` itself is clear.
    assert al.blackout_wake(line, at(11, 59)) is None  # just before -> unaffected
    assert al.blackout_wake(line, at(12, 0)) == 7 * 3600  # start -> 7h to 19:00
    assert al.blackout_wake(line, at(18, 59)) == 60  # last minute inside
    assert al.blackout_wake(line, at(18, 59, 30)) == 30  # seconds honored
    assert al.blackout_wake(line, at(19, 0)) is None  # end -> already clear
    assert al.blackout_wake(line, at(19, 1)) is None  # after -> unaffected


def test_blackout_wake_disable_and_weekend():
    al = load_script("agent_loop")
    mon_noon = datetime.datetime(2026, 7, 13, 12, 0)  # Monday, inside a 12-19 window
    sat_noon = datetime.datetime(2026, 7, 11, 12, 0)  # Saturday
    sun_noon = datetime.datetime(2026, 7, 12, 12, 0)  # Sunday
    # start == end disables even on a weekday inside "the window".
    assert al.blackout_wake("00:00-00:00", mon_noon) is None
    assert al.blackout_wake("12:00-12:00", mon_noon) is None
    # The window is Mon–Fri only — weekends are never blacked out.
    assert al.blackout_wake("12:00-19:00", sat_noon) is None
    assert al.blackout_wake("12:00-19:00", sun_noon) is None
    # Absent/malformed line = disabled.
    assert al.blackout_wake("", mon_noon) is None
    assert al.blackout_wake("garbage", mon_noon) is None


def test_blackout_wake_wraps_past_midnight():
    al = load_script("agent_loop")
    line = "22:00-06:00"  # start > end -> a window crossing UTC midnight
    tue = datetime.datetime(2026, 7, 14)  # a Tuesday
    assert (
        al.blackout_wake(line, tue.replace(hour=23, minute=0)) == 7 * 3600
    )  # -> 06:00 next day
    assert (
        al.blackout_wake(line, tue.replace(hour=2, minute=0)) == 4 * 3600
    )  # early-morning tail
    assert (
        al.blackout_wake(line, tue.replace(hour=12, minute=0)) is None
    )  # midday -> clear


# --- WI-261: blackout pause feedback (banner + countdown heartbeat) -----------


def test_blackout_banner_names_policy_window_weekday_and_resume():
    # WI-261: the pause banner must be self-explanatory — a walk-away launch can
    # read it and know WHY it is waiting, that the scope is weekday-only, and WHEN
    # it resumes. Bites on a revert to the old one-liner (which named neither the
    # policy file nor the weekday-only scope, and had no humanized wait length).
    ac = load_script("agent_common")
    resume_at = datetime.datetime(2026, 7, 13, 19, 0)  # a Monday, 19:00 UTC
    banner = ac.blackout_banner("12:00-19:00", resume_at, 7 * 3600)
    assert "automation.blackout" in banner  # the policy SOURCE is named
    # P14 deleted docs/blackout; a banner naming it would send a waiting
    # operator to a file that is not there, which is worse than saying nothing.
    assert "docs/blackout" not in banner
    assert "12:00-19:00" in banner  # the actual window is shown
    assert "weekday" in banner.lower()  # weekday-only scope stated plainly
    assert "19:00 UTC" in banner  # the resume time
    assert "7h 0m 0s" in banner  # the wait length, humanized
    assert "agent-resume -> agent_loop" in banner  # the path that honors it
    assert banner.count("\n") >= 4  # a multi-line banner, not a one-liner


def test_blackout_wait_emits_countdown_heartbeat_at_interval():
    # WI-261: while waiting out the window the loop must tick down at the injected
    # interval so an unattended launch is visibly WAITING, not hung. Deterministic
    # — a captured emit and a no-op sleep, NO real multi-second delay. Bites if
    # the heartbeat is dropped (the old code slept silently after one print).
    ac = load_script("agent_common")
    resume_at = datetime.datetime(2026, 7, 13, 19, 0)
    lines, slept = [], []
    ac.blackout_wait(
        180,
        "12:00-19:00",
        resume_at,
        emit=lines.append,
        sleep=slept.append,
        interval=60,
    )
    # The wait is unchanged: exactly `wake` slept, in interval-sized steps.
    assert slept == [60, 60, 60]
    assert sum(slept) == 180
    # First emit is the banner; then one countdown per completed step EXCEPT the
    # last (the loop resumes there, no redundant tick): 180->120->60->0 => 2 ticks.
    assert lines[0] == ac.blackout_banner("12:00-19:00", resume_at, 180)
    countdowns = [ln for ln in lines if "remaining" in ln]
    assert len(countdowns) == 2
    assert "~2m 0s remaining" in countdowns[0]
    assert "~1m 0s remaining" in countdowns[1]
    assert all("resuming 19:00 UTC" in ln for ln in countdowns)


def test_blackout_wait_short_window_slept_exactly_once():
    # A window shorter than one heartbeat interval sleeps once for the whole wait
    # and emits no countdown (the banner already stated the resume time). Guards
    # the interval>remaining branch and confirms no spin on a sub-interval wait.
    ac = load_script("agent_common")
    resume_at = datetime.datetime(2026, 7, 13, 12, 1)
    lines, slept = [], []
    ac.blackout_wait(
        30, "12:00-12:01", resume_at, emit=lines.append, sleep=slept.append
    )
    assert slept == [30]
    assert [ln for ln in lines if "remaining" in ln] == []  # no heartbeat needed


def test_seconds_until_reset_weekly_same_weekday():
    # A3: a named-weekday reset that already passed today is NEXT week's same
    # weekday (+~6 days), not tomorrow (+1 day, a different weekday).
    import datetime

    loop = load_script("agent_loop")
    now = datetime.datetime(2026, 7, 13, 15, 0)  # a Monday, 3pm
    secs = loop.seconds_until_reset("weekly limit resets Mon 12:00am", now)
    target = now + datetime.timedelta(seconds=secs)
    assert target.weekday() == 0  # Monday, not Tuesday
    assert 6 * 86400 < secs <= 7 * 86400  # ~6 days out, not ~9 hours
    # A future weekday this week is still this week (unchanged behavior).
    secs2 = loop.seconds_until_reset("resets Tue 12:00am", now)
    assert (now + datetime.timedelta(seconds=secs2)).weekday() == 1


def test_seconds_until_reset_parses_both_clock_formats():
    # The reset wording is locale-dependent: am/pm and 24-hour clocks must
    # both parse; anything else returns None (the fallback-nap signal).
    agent_loop = load_script("agent_loop")
    noon = datetime.datetime(2026, 7, 4, 12, 0, 0)
    assert agent_loop.seconds_until_reset("3:45pm", now=noon) == 13500
    assert agent_loop.seconds_until_reset("14:30", now=noon) == 9000
    assert agent_loop.seconds_until_reset("resets 14:30:00", now=noon) == 9000
    # A time already past rolls to tomorrow, never a negative sleep.
    assert agent_loop.seconds_until_reset("09:00", now=noon) == 75600
    for garbage in ("in a little while", "99:99", "soon", ""):
        assert agent_loop.seconds_until_reset(garbage, now=noon) is None


def test_the_declared_state_parse_reads_the_first_non_comment_line():
    # The one-word parse survives the P13 cutover only for the STATE surfaces
    # (docs/gate, run-state): the FIRST non-empty, non-comment line.
    #
    # This test used to pin `agent_loop.read_declared` and
    # `check_privacy._first_declared_line` EQUAL, because a multi-line policy
    # file that passed one gate and failed another would be a silent split. Both
    # sides of that pairing are gone in the direction the pairing wanted: the
    # behaviour dials moved to one validated document, so check_privacy has no
    # parser of its own to disagree with — it reads `policy.privacy_check`
    # through `config.load_config` like everything else, and its copy of the
    # parse was deleted with its last caller. What remains worth pinning is the
    # rule itself, on the surfaces that still use it.
    import tempfile
    from pathlib import Path

    agent_loop = load_script("agent_loop")
    check_privacy = load_script("check_privacy")
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "docs").mkdir()
        state = root / "docs" / "gate"
        state.write_text(
            "# comment header, as the shipped templates carry\n"
            "\n"
            "first-value\n"
            "second-value\n",
            encoding="utf-8",
        )
        assert agent_loop.read_declared(state, "G1") == "first-value"
    assert not hasattr(check_privacy, "_first_declared_line"), (
        "check_privacy grew back a private declared-file parser. Its policy has "
        "ONE reader now (config.load_config); a second one is how the two "
        "answers drift apart again."
    )


# --- WI-080 Slice A golden net: model-map / {model} preflight guards -----------


def test_parse_map_rejects_entry_without_equals():
    # The pure parser raises ValueError on a no-'=' entry (the guard the
    # model-map preflight in tests/test_agent_loop.py leans on); a well-formed
    # map still parses.  (WI-277 repointed 'above' when the split moved this
    # test out of that module.)
    agent_loop = load_script("agent_loop")
    with pytest.raises(ValueError):
        agent_loop.parse_map("BUILDstrong")
    assert agent_loop.parse_map("BUILD=strong,PLAN=fast") == {
        "BUILD": "strong",
        "PLAN": "fast",
    }


# --- WI-080 Slice B seams -----------------------------------------------------
# The three session-construction functions extracted from main() to module level:
# pure model/template selection and prompt composition, unit-addressable without a
# coordinator run.


def test_session_model_seam():
    # Empty map -> the phase is '' and the default model rides through; a
    # ''-keyed map entry overrides the default.
    al = load_script("agent_loop")
    assert al.session_model({}, "claude-opus-4-8") == ("", "claude-opus-4-8")
    assert al.session_model({"": "claude-fable-5"}, "claude-opus-4-8") == (
        "",
        "claude-fable-5",
    )


def test_session_template_seam():
    # A phase-keyed template wins; an unknown phase falls back to the default.
    al = load_script("agent_loop")
    cmd_map = {"REVIEW-A": "agent --review", "BUILD": "agent --build"}
    assert al.session_template(cmd_map, "agent --default", "REVIEW-A") == (
        "agent --review"
    )
    assert al.session_template(cmd_map, "agent --default", "PLAN") == "agent --default"


def test_compose_session_prompt_plain(tmp_path):
    # A bare body, no reconcile note, guardrails off -> unchanged base and
    # guarded False (WI-210: body is required — the resume default is retired).
    al = load_script("agent_loop")
    prompt, guarded = al.compose_session_prompt(
        "claude-opus-4-8", "BODY-PROMPT", "", "off", tmp_path, []
    )
    assert prompt == "BODY-PROMPT"
    assert guarded is False


def test_compose_session_prompt_ordering(tmp_path):
    # reconcile + body concatenate in exactly that order; guardrails off ->
    # guarded False.
    al = load_script("agent_loop")
    prompt, guarded = al.compose_session_prompt(
        "claude-opus-4-8", "BODY", "RECON\n", "off", tmp_path, []
    )
    assert prompt == "RECON\nBODY"
    assert guarded is False


def test_compose_session_prompt_guardrails_on(tmp_path):
    # policy selects the model and a real core.md is vendored -> the core is
    # prepended ahead of the base with the "---" separator, and guarded is True.
    al = load_script("agent_loop")
    _vendor_core(tmp_path, "CORE-RULES\n")
    prompt, guarded = al.compose_session_prompt(
        "claude-opus-4-8", "BASE", "", "opus", tmp_path, []
    )
    assert prompt == "CORE-RULES\n\n---\n\nBASE"
    assert guarded is True


def test_compose_session_prompt_guardrails_missing_core_warns_once(tmp_path, capsys):
    # policy selects the model but core.md is absent -> warn once to stderr,
    # return the base with guarded False; a SECOND call sharing warned_no_core
    # does not warn again.
    al = load_script("agent_loop")
    warned = []
    prompt, guarded = al.compose_session_prompt(
        "claude-opus-4-8", "BASE", "", "opus", tmp_path, warned
    )
    assert prompt == "BASE"
    assert guarded is False
    first = capsys.readouterr()
    assert "core.md is absent" in first.err
    assert warned == [True]

    prompt2, guarded2 = al.compose_session_prompt(
        "claude-opus-4-8", "BASE", "", "opus", tmp_path, warned
    )
    assert prompt2 == "BASE"
    assert guarded2 is False
    second = capsys.readouterr()
    assert "core.md is absent" not in second.err


# --- WI-274 part B / IF-068: the single-home coordinator dials -----------------
# agent_loop reads its dials from docs/stack.ini [agent-loop] with the precedence
# CLI flag > AGENT_* env > declared file > built-in default, so a one-dial change
# edits ONE file instead of the same value in three agent-resume launchers.


def test_read_agent_loop_config_reads_declared_dials(tmp_path):
    al = load_script("agent_loop")
    docs = tmp_path / "docs"
    docs.mkdir()
    # Absent stack.ini -> {} (fail-soft: the env slots + defaults still apply).
    assert al.read_agent_loop_config(docs) == {}
    # A present [agent-loop] section -> the declared dials, stripped; a BLANK
    # value is dropped (falls through to env/default), an absent key is absent.
    (docs / "stack.ini").write_text(
        "[product]\ntest = pytest\n\n"
        "[agent-loop]\njobs = 1\nmodel =  opus \nmodel-map =\n",
        encoding="utf-8",
    )
    assert al.read_agent_loop_config(docs) == {"jobs": "1", "model": "opus"}
    # A stack.ini WITHOUT the section -> {} (the section is optional).
    (docs / "stack.ini").write_text("[product]\ntest = pytest\n", encoding="utf-8")
    assert al.read_agent_loop_config(docs) == {}
    # A malformed stack.ini degrades to {} rather than crashing the loop.
    (docs / "stack.ini").write_text("[unclosed section\njobs = 1\n", encoding="utf-8")
    assert al.read_agent_loop_config(docs) == {}


def test_resolve_coordinator_dials_precedence(tmp_path):
    # (The jobs dial retired with the parallel dispatcher at Phase 5; a
    # declared [agent-loop] jobs value is read but ignored.)
    al = load_script("agent_loop")

    class Args:  # a stand-in for the argparse namespace (only the dial fields)
        def __init__(self, model=None, model_map=None):
            self.model, self.model_map = model, model_map

    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "stack.ini").write_text(
        "[agent-loop]\njobs = 1\nmodel = declared\nmodel-map = PLAN=declared\n",
        encoding="utf-8",
    )
    import os as _os

    for var in ("AGENT_MODEL", "AGENT_MODEL_MAP"):
        _os.environ.pop(var, None)
    # Nothing on CLI/env -> the declared file supplies every dial.
    assert al.resolve_coordinator_dials(Args(), docs) == (
        "declared",
        "PLAN=declared",
    )
    # An env slot beats the declared file; an explicit CLI value beats the env.
    _os.environ["AGENT_MODEL"] = "envm"
    try:
        assert al.resolve_coordinator_dials(Args(), docs)[0] == "envm"
        assert al.resolve_coordinator_dials(Args(model="clim"), docs)[0] == "clim"
    finally:
        _os.environ.pop("AGENT_MODEL", None)
    # No declared file + nothing else -> the built-in defaults.
    assert al.resolve_coordinator_dials(Args(), tmp_path / "nodocs") == ("", "")


# --- WI-080 Slice D/E: the PURE main()-seam units -----------------------------
# The ungated half of Slices D/E. worker_exit_banner and the two argument-shaped
# seams (build_worker_assignment's not-a-worker case, parse_args defaults) touch
# no git and no repo — they read/return values, so they belong with the parse
# and decision units here rather than in the worker leg's module, which carries
# a module-wide `pytestmark = env_gate_skipif("git")` that would ADD a gate they
# never had (REVIEW-A round 1: they went 3 passed -> 3 skipped with git off
# PATH when the split first parked them there). Their git-dependent siblings —
# worker_endstate and the build_worker_assignment cases that resolve a real
# base — are in tests/test_agent_loop_worker.py, where the gate is earned.


def test_worker_exit_banner_returns_code_and_prints(capsys):
    al = load_script("agent_loop")
    worker = {"train": "t1", "assigned": ["WI-201", "WI-204"]}
    code = al.worker_exit_banner(
        worker, (al.EXIT_DONE, "DONE", "every assigned WI built")
    )
    assert code == al.EXIT_DONE
    out = capsys.readouterr().out
    assert "worker t1 [WI-201;WI-204]: DONE" in out
    assert "every assigned WI built" in out


def test_build_worker_assignment_is_none_without_wi_and_train():
    al = load_script("agent_loop")
    args = argparse.Namespace(wi=None, train=None, base=None, rework=None)
    # Not a worker process — no root touched, no error.
    assert al.build_worker_assignment(args, "/does/not/matter") == (None, None)


def test_parse_args_defaults(monkeypatch):
    al = load_script("agent_loop")
    monkeypatch.setattr(sys, "argv", ["agent_loop.py"])
    args = al.parse_args()
    assert args.max_iterations == 40
    assert args.stall_limit == 3
    assert args.pause == 10
