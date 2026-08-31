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
import ast
import dataclasses
import datetime
import inspect
import re
import sys
import textwrap

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
    assert "docs/blackout" in banner  # the policy file is named
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


def test_declared_policy_parsers_agree():
    # One parse rule for the one-word policy files (docs/gate, gate-policy,
    # push-policy, privacy-check, run-state): the FIRST non-empty, non-comment
    # line — the rule the git hooks (head -n 1 of the non-comment lines) already
    # enforce. agent_loop and check_privacy must agree, or a multi-line file
    # would pass one gate and fail another.
    import tempfile
    from pathlib import Path

    agent_loop = load_script("agent_loop")
    check_privacy = load_script("check_privacy")
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "docs").mkdir()
        policy = root / "docs" / "privacy-check"
        policy.write_text(
            "# comment header, as the shipped templates carry\n"
            "\n"
            "first-value\n"
            "second-value\n",
            encoding="utf-8",
        )
        assert agent_loop.read_declared(policy, "false") == "first-value"
        assert check_privacy._first_declared_line(policy) == "first-value"


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


# --- WI-483 slice 5: the loop-startup split, and the two typed records --------
# `main` was 402 lines / C901 27, resolving its whole configuration inline; the
# resolution is now pure functions returning frozen records and `main` keeps the
# effects. These guard the BOUNDARY — that the records stay total and frozen,
# that the S8 knob idiom survives extraction, and that `main` stays a composer —
# rather than re-asserting rules already covered end-to-end through the engine.


def test_int_env_falls_back_on_junk_and_below_floor(monkeypatch):
    al = load_script("agent_loop")
    monkeypatch.delenv("AL_KNOB", raising=False)
    assert al._int_env("AL_KNOB", 7) == 7  # absent -> the built-in default
    monkeypatch.setenv("AL_KNOB", "12")
    assert al._int_env("AL_KNOB", 7) == 12
    monkeypatch.setenv("AL_KNOB", "not-a-number")
    assert al._int_env("AL_KNOB", 7) == 7
    monkeypatch.setenv("AL_KNOB", "0")
    # A budget is >= 1; below the floor falls back rather than wedging the run.
    assert al._int_env("AL_KNOB", 3, minimum=1) == 3
    assert al._int_env("AL_KNOB", 3) == 0  # no floor declared -> honored


def test_clamped_review_rounds_is_lenient_then_clamped():
    al = load_script("agent_loop")
    assert al._clamped_review_rounds("2") == 2
    assert al._clamped_review_rounds("banana") == 1  # unparseable -> 1
    assert al._clamped_review_rounds("7") == 2  # out of range -> clamped
    assert al._clamped_review_rounds("-3") == 0


def test_is_drive_launch_only_when_no_role_flag():
    al = load_script("agent_loop")

    def args(**over):
        base = dict(wi=None, train=None, interactive=False, dual_plan=None)
        base.update(over)
        return argparse.Namespace(**base)

    assert al.is_drive_launch(args())
    for flag in ("wi", "train", "dual_plan"):
        assert not al.is_drive_launch(args(**{flag: "WI-1"}))
    assert not al.is_drive_launch(args(interactive=True))


def test_possible_session_models_reads_the_enabled_rows_under_managed():
    al = load_script("agent_loop")
    ar = load_script("agent_route")
    args = argparse.Namespace(model="cli-model")
    legacy = al.RoutingSetup(
        registry={},
        managed=False,
        enabled=[],
        weight_map={},
        reg_errors=[],
        enable_errors=[],
    )
    assert al.possible_session_models(args, {"BUILD": "mapped"}, legacy) == {
        "cli-model",
        "mapped",
    }
    row = ar.Model("P-B-1", "P", "rowmodel", "1", "medium", "")
    managed = al.RoutingSetup(
        registry={"P-B-1": row},
        managed=True,
        enabled=["P-B-1"],
        weight_map={},
        reg_errors=[],
        enable_errors=[],
    )
    # Under managed routing the ENABLED rows' models join the set — the inert
    # check must be computed against what will actually run (L-20).
    assert "rowmodel" in al.possible_session_models(args, {}, managed)


def test_loop_context_is_frozen_and_total():
    al = load_script("agent_loop")
    fields = {f.name: f for f in dataclasses.fields(al.LoopContext)}
    # TOTAL: no field carries a default, so a forgotten one is a TypeError at
    # the single construction site rather than a silent getattr fallback.
    assert all(
        f.default is dataclasses.MISSING and f.default_factory is dataclasses.MISSING
        for f in fields.values()
    ), "LoopContext fields must not carry defaults"
    assert "human_held" in fields and "keep_nondependent" in fields
    ctx = al.LoopContext(**{name: None for name in fields})
    with pytest.raises(dataclasses.FrozenInstanceError):
        ctx.root = "elsewhere"


def test_loop_run_is_the_mutable_half_with_per_instance_defaults():
    al = load_script("agent_loop")
    a = al.LoopRun(routing=None)
    b = al.LoopRun(routing=None)
    assert a.state == "RUNNING"
    a.state = "DONE"  # the mutable half: an iteration may write it
    a.warned_no_core.append("core")
    assert b.state == "RUNNING" and b.warned_no_core == []


def test_no_defensive_getattr_reads_survive_on_the_context():
    al = load_script("agent_loop")
    tree = ast.parse(inspect.getsource(al))
    reads = [
        n
        for n in ast.walk(tree)
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Name)
        and n.func.id == "getattr"
        and n.args
        and isinstance(n.args[0], ast.Name)
        and n.args[0].id == "ctx"
    ]
    assert not reads, (
        "a total frozen record cannot be missing a field — a getattr(ctx, ..., "
        "default) read silently substitutes a policy value instead of failing"
    )


def test_main_stays_a_composer():
    al = load_script("agent_loop")
    src, _ = inspect.getsourcelines(al.main)
    # 402 lines at WI-483 slice 5; the ceiling is a red for re-accretion, not a
    # target. `main` also nests no def — the C901 trap the program records is
    # that a helper extracted INWARD is charged to its enclosing function.
    assert len(src) < 200, "main is re-accreting; decompose OUTWARD"
    body = ast.parse(textwrap.dedent("".join(src)))
    assert not [
        n for n in ast.walk(body) if isinstance(n, ast.FunctionDef) and n.name != "main"
    ], "no nested def in main — extract outward, not inward"


# --- WI-483 slice 6: the per-session consequence ladders -----------------------
# `session_bookkeeping` (325 lines / C901 31, the kit's most complex surviving
# function) and `run_iteration` (326 / 20) split on the same boundary: what a
# session's OUTCOME MEANS is a named function over routing state — several of
# them returning frozen records — while the arms keep the effects. These guard
# the boundary, not the rules already driven end-to-end through the engine in
# tests/test_agent_loop{,_review,_critique}.py.


def _fa(mode, keep, design_check=False):
    """An `agent_route.failure_action` result, as the page paths read it."""
    return {
        "mode": mode,
        "keep_nondependent": keep,
        "note": "n",
        "design_check": design_check,
    }


def test_page_consequence_is_the_one_rule_both_page_paths_obey():
    al = load_script("agent_loop")
    # SN-029: keyed on the MODE the ordinal produced, never on the retired enum.
    assert al.page_consequence(_fa("human-held", False)).stop
    assert not al.page_consequence(_fa("human-held", True)).stop
    assert not al.page_consequence(_fa("loop-held", False)).stop
    # The critique arm's declared `exhaustion = block` stops whatever the hold
    # says — the one asymmetry between the two callers, stated as an argument
    # rather than duplicated as a second ladder.
    assert al.page_consequence(_fa("loop-held", True), force_block=True).stop


def test_a_stopping_page_never_also_re_arms_the_design_check():
    al = load_script("agent_loop")
    # The original returned before the design-check arm on every stop path;
    # that ordering is now a field of the record rather than a `return`'s luck.
    stopping = al.page_consequence(_fa("human-held", False, design_check=True))
    assert stopping.stop and not stopping.design_check
    going = al.page_consequence(_fa("loop-held", True, design_check=True))
    assert not going.stop and going.design_check


def test_rate_limit_wait_naps_only_within_the_consented_ceiling():
    al = load_script("agent_loop")

    def args(wait_on_limit, fallback=3600):
        return argparse.Namespace(
            wait_on_limit=wait_on_limit, limit_retry_fallback=fallback
        )

    # Unrecognized reset wording -> the bounded fallback, capped at the ceiling
    # the human already consented to.
    unknown = al.rate_limit_wait(args(600), "in a little while")
    assert unknown.nap and unknown.seconds == 600
    assert "--limit-retry-fallback" in unknown.message
    # No consent to wait at all -> no nap, whatever the hint says.
    assert not al.rate_limit_wait(args(0), "in a little while").nap
    assert not al.rate_limit_wait(args(0), "resets 3:45pm").nap


def test_limit_wait_carries_an_explicit_nap_flag_not_a_falsy_second():
    al = load_script("agent_loop")
    # The discriminator exists so a ZERO-second wait is still a wait: `seconds`
    # alone is falsy at 0 and would read as "do not nap".
    assert al.LimitWait(True, 0, "m").nap
    assert not al.LimitWait(False, 0, "").nap
    with pytest.raises(dataclasses.FrozenInstanceError):
        al.LimitWait(False, 0, "").nap = True


def test_impl_changed_paths_excludes_the_trains_own_review_bookkeeping():
    al = load_script("agent_loop")

    class St:
        impl_range = ""

    st = St()
    # No reviewed range -> no git call at all (this module touches no repo).
    assert al.impl_changed_paths("/nowhere", st, "t1") == []
    st.impl_range = "aaa..bbb"
    diff = "\n".join(
        [
            "src/thing.py",
            "docs/reviews/t1/WI-1-REVIEW-A.md",
            "docs\\reviews\\t1\\scoreboard.txt",
            "docs/iteration/1-g3-x.log",
            "docs/reviews/t2/other.md",
            "   ",
        ]
    )
    al_git = al.git
    try:
        al.git = lambda *a, **k: (0, diff)
        # The train's OWN committed verdicts/scoreboard/telemetry are not the
        # implementer touching a review path (the false-fire this excludes);
        # another train's are.
        assert al.impl_changed_paths("/nowhere", st, "t1") == [
            "src/thing.py",
            "docs/reviews/t2/other.md",
        ]
    finally:
        al.git = al_git


def test_round_substance_is_a_frozen_record_and_a_solo_round_has_no_winner():
    al = load_script("agent_loop")

    class St:
        round_verdicts = [("REVIEW-A", object(), "FAM", "P-1")]

    scores = iter([0.7])
    sr = al.score_reviews
    try:
        al.score_reviews = type(
            "S", (), {"substance": staticmethod(lambda *a, **k: next(scores))}
        )
        sub = al.round_substance(St(), "/nowhere")
    finally:
        al.score_reviews = sr
    # One reviewer is no comparison: margin 0.0 and NO primary family. The
    # record says so in fields rather than in three locals a caller must keep
    # in step.
    assert sub.margin == 0.0 and sub.primary is None
    assert sub.family_substance == {"FAM": 0.7}
    with pytest.raises(dataclasses.FrozenInstanceError):
        sub.margin = 1.0


def test_session_meta_is_the_log_row_in_the_logs_own_column_order():
    al = load_script("agent_loop")
    src = inspect.getsource(al.session_meta)
    # The projection stays a dict because it IS write_session_log's column set;
    # pin the order so a reorder is a red rather than a silently reshaped log.
    keys = [m for m in re.findall(r'^\s{8}"([a-z-]+)":', src, re.M)]
    assert keys == [
        "session",
        "stamp",
        "date",
        "train",
        "base",
        "phase",
        "wi",
        "model",
        "guardrails",
        "outcome",
        "commits",
        "tokens",
        "cost-usd",
        "wall-secs",
        "api-secs",
        "turns",
        "ttft-secs",
        "cache-read",
        "cache-create",
        "effort",
        "fast",
        "prompt-chars",
        "prompt-template",
        "prompt-sha",
        "exit-code",
        "session-id",
        "context-used",
        "context-window",
        "context-pct",
    ]


def test_family_context_telemetry_reads_anthropics_own_result_json():
    # WI-535 (telemetry first, dial off): no mint, no resume — just what
    # ANTHROPIC's stream-json result already reports on a plain one-shot
    # call. The window comes from the modelUsage entry whose own input/output
    # counts match the top-level usage totals, not the first entry in the
    # dict — a subagent draw on a different model must not be mistaken for
    # the session's own window.
    al = load_script("agent_loop")
    data = {
        "session_id": "cc77a65f-c2f7-4779-bd42-0be7e188a717",
        "usage": {
            "input_tokens": 5201,
            "output_tokens": 6529,
            "cache_read_input_tokens": 154637,
            "cache_creation_input_tokens": 66231,
        },
        "modelUsage": {
            "claude-haiku-4-5-20251001": {
                "inputTokens": 10974,
                "outputTokens": 19,
                "contextWindow": 200000,
            },
            "claude-opus-4-8": {
                "inputTokens": 5201,
                "outputTokens": 6529,
                "contextWindow": 1000000,
            },
        },
    }
    session_id, occupancy, window, pct = al.family_context_telemetry("ANTHROPIC", data)
    assert session_id == "cc77a65f-c2f7-4779-bd42-0be7e188a717"
    assert occupancy == 5201 + 6529 + 154637 + 66231
    assert window == 1000000
    assert pct == round(occupancy * 100 / window)


def test_family_context_telemetry_blank_window_on_no_usage_or_match():
    al = load_script("agent_loop")
    # No usage at all (a plain-text/errored session): everything but a
    # captured session id stays blank, never a guess.
    assert al.family_context_telemetry("ANTHROPIC", {"session_id": "x"}) == (
        "x",
        "",
        "",
        "",
    )
    # Usage present but no modelUsage entry matches it: occupancy is still
    # computable from the top-level totals, but window is left blank rather
    # than guessed from an unrelated entry.
    data = {
        "usage": {"input_tokens": 10, "output_tokens": 5},
        "modelUsage": {
            "claude-haiku-4-5-20251001": {"inputTokens": 999, "outputTokens": 1}
        },
    }
    assert al.family_context_telemetry("ANTHROPIC", data) == ("", 15, "", "")


def test_family_context_telemetry_blank_for_families_with_no_json_yet():
    # OPENAI/OPENCODE's shipped one-shot templates carry no --json/--format
    # json, so there is nothing to parse until WI-540's per-family adapter
    # lands — blank, not a guess from the transcript text.
    al = load_script("agent_loop")
    data = {"session_id": "should-not-surface", "usage": {"input_tokens": 1}}
    assert al.family_context_telemetry("OPENAI", data) == ("", "", "", "")
    assert al.family_context_telemetry("OPENCODE", data) == ("", "", "", "")
    assert al.family_context_telemetry("", data) == ("", "", "", "")


@pytest.mark.parametrize(
    "name,ceiling",
    [("session_bookkeeping", 40), ("run_iteration", 130)],
)
def test_the_session_ladders_stay_composers(name, ceiling):
    al = load_script("agent_loop")
    src, _ = inspect.getsourcelines(getattr(al, name))
    # 325 and 326 lines respectively before WI-483 slice 6; the ceiling is a red
    # for re-accretion, not a target. Neither may nest a def — the recorded C901
    # trap is that a helper extracted INWARD is charged to its enclosing
    # function, so the extraction raises the number it was meant to lower.
    assert len(src) < ceiling, "{} is re-accreting; decompose OUTWARD".format(name)
    body = ast.parse(textwrap.dedent("".join(src)))
    assert not [
        n for n in ast.walk(body) if isinstance(n, ast.FunctionDef) and n.name != name
    ], "no nested def in {} — extract outward, not inward".format(name)
