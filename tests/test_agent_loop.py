"""The unattended coordinator engine (Thread 33, process-options.md
"Unattended operation") — exercised end-to-end against a fake agent command,
so no test depends on any real agent CLI. The fake pops one action per
invocation from a control dir outside the repo: commit / noop / done /
blocked / needs-human / limit / sleep."""

import datetime
import os
import re
import subprocess
import sys

import pytest
from conftest import SCRIPTS, augment_env, load_script, run_py

# The fake agent: records every invocation + the model it was handed, then
# performs the next scripted action in the repo it was launched in (cwd),
# exactly as a headless driver session would.
FAKE_AGENT = """
import argparse, json, pathlib, subprocess, sys, time

ap = argparse.ArgumentParser()
ap.add_argument("--control", required=True)
ap.add_argument("--model", default="")
ap.add_argument("-p", "--prompt", default="")
args, extra = ap.parse_known_args()
ctl = pathlib.Path(args.control)
inv = ctl / "invocations.txt"
count = len(inv.read_text().splitlines()) if inv.exists() else 0
with open(str(inv), "a") as fh:
    fh.write("call\\n")
with open(str(ctl / "models.txt"), "a") as fh:
    fh.write(args.model + "\\n")
pathlib.Path(str(ctl / "prompt.txt")).write_text(args.prompt, encoding="utf-8")
actions = []
if (ctl / "actions.txt").exists():
    actions = (ctl / "actions.txt").read_text().split()
action = actions[count] if count < len(actions) else "noop"


def commit(msg):
    pathlib.Path("work.txt").write_text(msg + str(count))
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-q", "-m", msg], check=True)


if action == "commit":
    commit("progress")
    # Healthy prose that *mentions* limits: must never read as a throttle
    # (the engine gates the limit regex on an error signal).
    print("session committed progress; noted the usage limit resets 3:45pm")
elif action in ("done", "blocked", "needs-human"):
    commit("finishing")
    state = action.upper()
    if action == "needs-human":
        # WI-127: a driver follows the state word with the one-line ask.
        state += "\\nask: OI-1 needs the demo-gate approval"
    pathlib.Path("docs/run-state").write_text(state)
    print(json.dumps({"result": "ok",
                      "usage": {"input_tokens": 10, "output_tokens": 5,
                                "cache_read_input_tokens": 70000,
                                "cache_creation_input_tokens": 9000},
                      "total_cost_usd": 0.12,
                      "duration_api_ms": 61000, "num_turns": 7,
                      "ttft_ms": 4200, "fast_mode_state": "off"}))
elif action == "pause":
    # WI-147: a session that (over)writes docs/pause mid-run — the loop must let
    # this session finish and commit, then stop at the NEXT boundary.
    commit("pausing")
    pathlib.Path("docs/pause").write_text("owner requested a break")
    print("session committed progress; wrote docs/pause")
elif action == "stream-done":
    # A stream-json CLI: per-turn events, then the result event NOT last (a
    # trailing event must not shadow it - the parse preference under test).
    commit("finishing")
    pathlib.Path("docs/run-state").write_text("DONE")
    print(json.dumps({"type": "assistant", "message": {"content": [
        {"type": "text", "text": "refactoring the parser now"}]}}))
    print(json.dumps({"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": "Edit", "input": {}}]}}))
    print(json.dumps({"type": "result", "result": "ok",
                      "usage": {"input_tokens": 3, "output_tokens": 2},
                      "total_cost_usd": 0.01, "duration_api_ms": 1000,
                      "num_turns": 2}))
    print(json.dumps({"type": "system", "subtype": "trailing"}))
elif action == "limit":
    print(json.dumps({"is_error": True,
                      "result": "You've hit your session limit \\u00b7 resets 3:45pm"}))
    sys.exit(1)
elif action == "limit-odd":
    # A reset wording neither clock parser recognizes (locale/format drift).
    print(json.dumps({"is_error": True,
                      "result": "You've hit your session limit \\u00b7 resets in a little while"}))
    sys.exit(1)
elif action == "error":
    # An error result that is NOT a rate limit (model retired / auth expired /
    # CLI broke): is_error, no reset wording -> the engine reads ERROR.
    print(json.dumps({"is_error": True,
                      "result": "API error: the model 'retired-x' is not supported"}))
    sys.exit(1)
elif action == "error-plain":
    # A plain-text (no JSON) session that fails: nonzero exit, no is_error flag.
    print("fatal: could not reach the model endpoint")
    sys.exit(2)
elif action == "sleep":
    time.sleep(8)
else:
    print("session ok, nothing to commit")
sys.exit(0)
"""

STATUS_MD = """# Project Status

## Current State

- **Active gate:** G1
- **Open items:**
  - **Needs <human>**:
    - OI-1 — decide: approve the demo gate (blocks: G1)

## Scope

- **Goal:** exercise the coordinator.
"""


def _git(repo, *args):
    proc = subprocess.run(
        ["git", "-C", str(repo)] + list(args),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip()


@pytest.fixture
def loop_repo(tmp_path):
    """A minimal git repo (one commit) + a control dir for the fake agent.
    Returns (repo, control-dir, AGENT_CMD template)."""
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "docs" / "status.md").write_text(STATUS_MD, encoding="utf-8")
    _git(repo, "init")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "initial")
    ctl = tmp_path / "control"
    ctl.mkdir()
    fake = tmp_path / "fake_agent.py"
    fake.write_text(FAKE_AGENT, encoding="utf-8")
    template = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )
    return repo, ctl, template


def _loop(repo, template, *extra):
    return run_py(
        [
            SCRIPTS / "agent_loop.py",
            "--root",
            repo,
            "--agent-cmd",
            template,
            "--pause",
            "0",
            "--model",
            "default-tier",
            *extra,
        ],
        cwd=repo,
    )


def _invocations(ctl):
    inv = ctl / "invocations.txt"
    return len(inv.read_text(encoding="utf-8").splitlines()) if inv.exists() else 0


def test_done_exit_writes_logs_and_index(loop_repo):
    # DONE ends the loop (exit 0), the banner surfaces status.md's pending
    # asks, and each session left a tracked bounded log + a regenerated index
    # carrying outcome / commit range / tokens / cost.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("commit done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "run-state=DONE" in proc.stdout
    assert "OI-1" in proc.stdout, "exit banner must surface the pending asks"
    assert "CONSENT" in proc.stdout, "the banner must state the consent line"
    logs = sorted((repo / "docs" / "iteration").glob("*.log"))
    assert len(logs) == 2
    meta = logs[1].read_text(encoding="utf-8")
    assert "# outcome: DONE" in meta
    assert "# exit-code: 0" in meta
    # The time signal (WI-119): wall seconds measured by the coordinator's own
    # clock (never blank), API seconds + turns parsed from the CLI JSON.
    assert re.search(r"^# wall-secs: \d+$", meta, re.M)
    assert "# api-secs: 61" in meta
    assert "# turns: 7" in meta
    # Session-shape telemetry (WI-124): boot latency, context volumes, and the
    # two per-turn speed dials, plus the coordinator-side prompt size.
    assert "# ttft-secs: 4" in meta
    assert "# cache-read: 70000" in meta
    assert "# cache-create: 9000" in meta
    assert "# fast: off" in meta
    assert "# effort:" in meta  # key present; value is whatever env was launched
    assert re.search(r"^# prompt-chars: \d+$", meta, re.M)
    index = (repo / "docs" / "iteration_index.md").read_text(encoding="utf-8")
    assert "| 001 |" in index and "| 002 |" in index
    assert "COMMITTED" in index and "DONE" in index
    assert "10+5" in index and "0.12" in index  # tokens + cost from the JSON
    assert "| Wall s | API s | Turns | s/turn | Ctx/turn |" in index
    # 61 s API / 7 turns = 8.7 s/turn; 70000 cache-read / 7 turns = 10k ctx/turn
    assert "| 61 | 7 | 8.7 | 10k |" in index
    assert "never hand-edited" in index
    # The raw unbounded stream lands in the gitignored out/run-logs/.
    assert list((repo / "out" / "run-logs").glob("*.log"))


def test_blocked_exit(loop_repo):
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("blocked", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 3, proc.stdout + proc.stderr
    assert "run-state=BLOCKED" in proc.stdout
    assert "OI-1" in proc.stdout


def test_needs_human_exit_surfaces_the_ask(loop_repo):
    # Q7d: the loop runs under every gate policy; when progress needs a human
    # act the driver writes NEEDS-HUMAN and the coordinator exits printing the
    # asks — interrupt-and-report, never infer-and-continue.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("needs-human", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 7, proc.stdout + proc.stderr
    assert "run-state=NEEDS-HUMAN" in proc.stdout
    assert "OI-1" in proc.stdout
    # WI-127: the driver's run-state ask line is the banner's headline — it
    # must surface even when the status excerpt would truncate before the
    # Needs-<human> items.
    assert "ask: OI-1 needs the demo-gate approval" in proc.stdout


def test_stall_guard_aborts_after_no_commit_sessions(loop_repo):
    repo, ctl, template = loop_repo  # no actions file -> every session noops
    proc = _loop(repo, template, "--stall-limit", "2", "--max-iterations", "6")
    assert proc.returncode == 4, proc.stdout + proc.stderr
    assert "STALL" in proc.stdout
    assert _invocations(ctl) == 2, "must stop at the stall limit, not the budget"


def test_budget_ceiling(loop_repo):
    # Commits every session (never stalls, never ends) -> the MaxIterations
    # budget ceiling is what stops the run.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("commit commit commit", encoding="utf-8")
    proc = _loop(repo, template, "--max-iterations", "3")
    assert proc.returncode == 6, proc.stdout + proc.stderr
    assert "budget" in proc.stdout.lower()
    assert _invocations(ctl) == 3


# --- WI-147: graceful pause (docs/pause) --------------------------------------


def test_pause_present_at_launch_refuses_to_start(loop_repo):
    # docs/pause present at launch = launch-time refusal: no session runs, the
    # loop stops with exit 8 and a banner naming the file + its reason.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("done", encoding="utf-8")  # would DONE if run
    (repo / "docs" / "pause").write_text("out for lunch", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 8, proc.stdout + proc.stderr
    assert "paused (docs/pause present)" in proc.stdout
    assert "out for lunch" in proc.stdout
    assert _invocations(ctl) == 0, "no session may start while paused"


def test_pause_mid_run_stops_after_the_current_session(loop_repo):
    # A session writes docs/pause; it still finishes and commits (graceful), and
    # the NEXT boundary stops the loop — never a mid-session kill.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("commit pause commit", encoding="utf-8")
    proc = _loop(repo, template, "--max-iterations", "6")
    assert proc.returncode == 8, proc.stdout + proc.stderr
    assert "paused (docs/pause present)" in proc.stdout
    # Sessions 1 (commit) and 2 (pause) ran; session 3 was refused at the boundary.
    assert _invocations(ctl) == 2
    # The pausing session's own commit landed — the stop was graceful, not a kill.
    assert "pausing" in _git(repo, "log", "--format=%s")


def test_pause_delete_resumes(loop_repo):
    # Deleting docs/pause and re-launching resumes work (the file is the whole
    # contract — run-state is never touched, so resume is a single act).
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    (repo / "docs" / "pause").write_text("", encoding="utf-8")
    paused = _loop(repo, template)
    assert paused.returncode == 8 and _invocations(ctl) == 0
    (repo / "docs" / "pause").unlink()
    resumed = _loop(repo, template)
    assert resumed.returncode == 0, resumed.stdout + resumed.stderr
    assert "run-state=DONE" in resumed.stdout
    assert _invocations(ctl) == 1


def test_pause_reason_helper_edges(tmp_path):
    al = load_script("agent_loop")
    assert al.pause_reason(tmp_path) is None  # absent -> not paused
    (tmp_path / "pause").write_text("", encoding="utf-8")
    assert al.pause_reason(tmp_path) == ""  # present but empty -> paused, no reason
    (tmp_path / "pause").write_text("# note\nbudget check\n", encoding="utf-8")
    assert al.pause_reason(tmp_path) == "budget check"  # first non-comment line


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


def test_blackout_present_but_inactive_does_not_block(loop_repo):
    # A docs/blackout file whose window does NOT cover "now" is a no-op: the
    # session runs and the loop reaches DONE (proves the loop reads the file and
    # only waits when actually inside the window).
    repo, ctl, template = loop_repo
    now = datetime.datetime.utcnow()
    # A 1-minute window two minutes ahead — never active at loop start, whatever
    # the wall clock or weekday (an inactive window is a no-op regardless).
    start = (now + datetime.timedelta(minutes=2)).strftime("%H:%M")
    end = (now + datetime.timedelta(minutes=3)).strftime("%H:%M")
    (repo / "docs" / "blackout").write_text(
        "{}-{}\n".format(start, end), encoding="utf-8"
    )
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "run-state=DONE" in proc.stdout
    assert _invocations(ctl) == 1


def test_cmd_map_broken_entry_fails_preflight(loop_repo):
    # A broken REVIEW-B entry must fail before iteration 1 (the preflight
    # contract), not at the first review session mid-run.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(repo, template, "--cmd-map", "REVIEW-B=no-such-cli-xyz -p {prompt}")
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "cmd-map [REVIEW-B]" in proc.stderr
    assert _invocations(ctl) == 0


def test_review_policy_surfaced_in_banner(loop_repo):
    # WI-042: docs/review-policy (the reviewer dial) is surfaced at run start —
    # and only surfaced: the loop never enforces it (R2's zero-code convention).
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    (repo / "docs" / "review-policy").write_text(
        "# reviewer dial\n2\n", encoding="utf-8"
    )
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "review-policy: 2" in proc.stdout


def test_status_size_guard_warns_only(loop_repo):
    # AGENT_ROLES R3: a bloated resume surface draws a warn-only preflight
    # tripwire (every session inherits it); the run itself proceeds untouched.
    repo, ctl, template = loop_repo
    (repo / "docs" / "status.md").write_text(
        STATUS_MD + ("filler line — evidence that belongs in log.md\n" * 400),
        encoding="utf-8",
    )
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr  # warn, never block
    assert "prune it to one screen" in proc.stderr


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


def test_status_size_warning_helper_edges():
    # The helper is pure: absent file and limit<=0 (AGENT_STATUS_WARN_BYTES=0)
    # both disable; an oversized file names the size and the charter.
    from pathlib import Path

    loop = load_script("agent_loop")
    assert loop.status_size_warning(Path("no/such/status.md"), 8192) is None
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "status.md"
        p.write_text("x" * 9000, encoding="utf-8")
        assert loop.status_size_warning(p, 0) is None  # 0 disables
        msg = loop.status_size_warning(p, 8192)
        assert msg and "9000" in msg and "one screen" in msg


def _vendor_core(repo, body):
    gdir = repo / "docs" / "guardrails"
    gdir.mkdir(parents=True, exist_ok=True)
    (gdir / "core.md").write_text(body, encoding="utf-8")


def test_guardrails_apply_policy_matrix():
    # off/absent -> never; all -> always; an allowlist of substrings -> guard on
    # ANY match; `all except <sub> ...` -> guard everything but the excepted.
    al = load_script("agent_loop")
    assert al.guardrails_apply("", "claude-opus-4-8") is False
    assert al.guardrails_apply("off", "claude-opus-4-8") is False
    assert al.guardrails_apply("all", "anything") is True
    # single-substring allowlist
    assert al.guardrails_apply("opus", "claude-opus-4-8") is True
    assert al.guardrails_apply("opus", "claude-fable-5") is False
    # multi-substring allowlist (OR)
    assert al.guardrails_apply("opus sonnet", "claude-sonnet-5") is True
    assert al.guardrails_apply("opus sonnet", "claude-fable-5") is False
    # all-except (denylist): guard everything but the named frontier model(s)
    assert al.guardrails_apply("all except fable", "claude-opus-4-8") is True
    assert al.guardrails_apply("all except fable", "claude-fable-5") is False
    assert al.guardrails_apply("all except fable opus", "claude-opus-4-8") is False


def test_guardrails_off_by_default_injects_nothing(loop_repo):
    # No docs/guardrails-policy -> the prompt reaches the agent unchanged.
    repo, ctl, template = loop_repo
    _vendor_core(repo, "MARKER-CORE do X\n")  # present but policy is off
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "MARKER-CORE" not in (ctl / "prompt.txt").read_text(encoding="utf-8")


def test_guardrails_all_injects_only_the_kit_core_block(loop_repo):
    # policy=all -> the BEGIN/END KIT CORE block (not surrounding upstream prose)
    # is prepended, and the coordinator's own prompt still follows.
    repo, ctl, template = loop_repo
    _vendor_core(
        repo,
        "upstream preamble ignored\n"
        "<!-- BEGIN KIT CORE v1.0 -->\nMARKER-CORE rules.\n<!-- END KIT CORE -->\n"
        "upstream footer ignored\n",
    )
    (repo / "docs" / "guardrails-policy").write_text("all\n", encoding="utf-8")
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    prompt = (ctl / "prompt.txt").read_text(encoding="utf-8")
    assert "MARKER-CORE rules." in prompt
    assert "ignored" not in prompt  # only the marked block, not the whole file
    assert "unattended coordinator" in prompt  # the base prompt still follows


def test_guardrails_weak_tier_injects_only_matching_model(loop_repo):
    # policy=a model substring: a session on the matching model (opus) is
    # guarded. The model map still declares the pool so the policy is not inert.
    repo, ctl, template = loop_repo
    _vendor_core(repo, "MARKER-CORE\n")
    (repo / "docs" / "guardrails-policy").write_text("opus\n", encoding="utf-8")
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(
        repo, template, "--model", "claude-opus-4-8", "--model-map", "PLAN=fable-5"
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "MARKER-CORE" in (ctl / "prompt.txt").read_text(encoding="utf-8")


def test_guardrails_strong_tier_is_not_injected(loop_repo):
    # Same policy, but the session runs on the frontier model (fable): no
    # substring match -> the guardrails core is not injected (opus stays in the
    # declared pool, so the policy is not inert — it just doesn't match this run).
    repo, ctl, template = loop_repo
    _vendor_core(repo, "MARKER-CORE\n")
    (repo / "docs" / "guardrails-policy").write_text("opus\n", encoding="utf-8")
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(
        repo, template, "--model", "fable-5", "--model-map", "BUILD=claude-opus-4-8"
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "MARKER-CORE" not in (ctl / "prompt.txt").read_text(encoding="utf-8")


def test_guardrails_selected_but_missing_core_warns_and_runs(loop_repo):
    # policy selects the model but no vendored core -> warn once, run anyway
    # (guardrails accelerate weak tiers; they never gate a run).
    repo, ctl, template = loop_repo
    (repo / "docs" / "guardrails-policy").write_text("all\n", encoding="utf-8")
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "core.md is absent" in (proc.stdout + proc.stderr)


def test_guardrails_inert_helper():
    # off/all are never inert; a guarding policy is inert only when it would
    # guard none of the models a run could use (stale allowlist, or an
    # all-except that excludes every configured model).
    al = load_script("agent_loop")
    assert al.guardrails_inert("off", {"claude-opus-4-8"}) is False
    assert al.guardrails_inert("all", set()) is False
    assert al.guardrails_inert("opus", {"claude-opus-4-8", "fable-5"}) is False
    assert al.guardrails_inert("opus", {"fable-5", "sonnet-6"}) is True
    assert al.guardrails_inert("opus", set()) is True
    # all-except that excludes every configured model guards nothing -> inert
    assert al.guardrails_inert("all except fable", {"claude-fable-5"}) is True
    assert al.guardrails_inert("all except fable", {"fable-5", "opus-4-8"}) is False


def test_guardrails_inert_policy_warns_at_startup(loop_repo):
    # A policy token matching no configured model warns that the guard is inert
    # (the stale-substring rot), but the run still proceeds.
    repo, ctl, template = loop_repo
    (repo / "docs" / "guardrails-policy").write_text("opus\n", encoding="utf-8")
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(repo, template)  # --model default-tier, no map -> no 'opus'
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "would guard none of the configured models" in (proc.stdout + proc.stderr)


def test_guardrails_matched_policy_does_not_warn(loop_repo):
    # When the token matches a model in the map, no inert warning fires.
    repo, ctl, template = loop_repo
    (repo / "docs" / "guardrails-policy").write_text("opus\n", encoding="utf-8")
    (repo / "docs" / "run-phase").write_text("BUILD\n", encoding="utf-8")
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(repo, template, "--model-map", "BUILD=claude-opus-4-8")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "would guard none of the configured models" not in (
        proc.stdout + proc.stderr
    )


def test_guardrails_all_except_guards_non_frontier(loop_repo):
    # 'all except <frontier>': a session whose model isn't the named frontier is
    # guarded (a spaced, multi-token policy flows through read_declared intact).
    repo, ctl, template = loop_repo
    _vendor_core(repo, "MARKER-CORE\n")
    (repo / "docs" / "guardrails-policy").write_text(
        "all except fable\n", encoding="utf-8"
    )
    (repo / "docs" / "run-phase").write_text("BUILD\n", encoding="utf-8")
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(
        repo, template, "--model-map", "PLAN=claude-fable-5,BUILD=claude-opus-4-8"
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "MARKER-CORE" in (ctl / "prompt.txt").read_text(encoding="utf-8")


def test_limit_hit_backs_off_without_counting_stall(loop_repo):
    # A throttled session must read WAITING, not a stall: with stall-limit 1 a
    # no-commit session would abort STALL (exit 4); the limit message must
    # instead exit WAITING (5) naming the reset time, and the index must
    # record the WAITING outcome.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("limit", encoding="utf-8")
    proc = _loop(repo, template, "--stall-limit", "1")
    assert proc.returncode == 5, proc.stdout + proc.stderr
    assert "WAITING" in proc.stdout
    assert "3:45pm" in proc.stdout, "banner must name the resume time"
    index = (repo / "docs" / "iteration_index.md").read_text(encoding="utf-8")
    assert "WAITING" in index


def test_error_session_reads_error_not_no_commit(loop_repo):
    # Thread 45: a session the CLI reports as errored (is_error, not a rate
    # limit) is logged ERROR, distinct from a healthy no-commit session — so the
    # index tells "agent failed" apart from "ran and idled". The run continues
    # (one error is under the stall limit) and finishes on the next session.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("error done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    index = (repo / "docs" / "iteration_index.md").read_text(encoding="utf-8")
    assert "ERROR" in index
    assert "NO-COMMIT" not in index  # the errored session is not mislabeled
    log = sorted((repo / "docs" / "iteration").glob("*.log"))[0].read_text(
        encoding="utf-8"
    )
    assert "# outcome: ERROR" in log


def test_plain_text_nonzero_exit_reads_error(loop_repo):
    # No JSON, just a nonzero exit (a plain-text agent template that failed) is
    # also ERROR — the same signal limit_reset_hint trusts, and it covers the
    # unlaunchable-session sentinel too.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("error-plain done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    index = (repo / "docs" / "iteration_index.md").read_text(encoding="utf-8")
    assert "ERROR" in index


def test_all_error_stall_names_an_agent_error(loop_repo):
    # When every session that trips the stall guard errored before working, the
    # abort banner names an unavailable agent (not a work stall) and points at
    # the model/auth fix — the misreport Thread 45 removes.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("error error", encoding="utf-8")
    proc = _loop(repo, template, "--stall-limit", "2", "--max-iterations", "6")
    assert proc.returncode == 4, proc.stdout + proc.stderr
    assert "errored before doing work" in proc.stdout
    assert "agent error" in proc.stdout.lower()
    assert _invocations(ctl) == 2, "must stop at the stall limit, not the budget"


def test_mixed_no_commit_and_error_stall_stays_generic(loop_repo):
    # A stall of mixed causes (a healthy idle + an error) is not purely an agent
    # failure, so it keeps the generic work-stall banner — the agent-error
    # wording is reserved for an all-ERROR run.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("noop error", encoding="utf-8")
    proc = _loop(repo, template, "--stall-limit", "2", "--max-iterations", "6")
    assert proc.returncode == 4, proc.stdout + proc.stderr
    assert "STALL" in proc.stdout
    assert "errored before doing work" not in proc.stdout


def test_unparseable_reset_falls_back_and_retries(loop_repo):
    # A reset wording neither clock format matches must not kill a walk-away
    # run: with --wait-on-limit set, the loop naps --limit-retry-fallback
    # seconds (capped at the wait ceiling) and retries instead of exiting.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("limit-odd done", encoding="utf-8")
    proc = _loop(repo, template, "--wait-on-limit", "30", "--limit-retry-fallback", "1")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "not recognized" in proc.stdout
    assert _invocations(ctl) == 2, "the throttled session must be retried"


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


def test_default_prompt_carries_the_plan_build_cadence():
    # WI-1.29 / WI-180: the engine's resume prompt carries the plan cadence. With
    # docs/run-phase retired the PLAN/BUILD phase bounce is gone from the prompt,
    # but the plan-surface cadence remains: work the next block, and re-chunk
    # against the iteration sensor when the plan is exhausted or wrong.
    # Conditional ("where docs/plan.md exists"), so a repo without the plan
    # surface is unchanged.
    prompt = load_script("agent_loop").DEFAULT_PROMPT
    assert "docs/plan.md" in prompt
    assert "iteration_index.md" in prompt  # the sizing servo's sensor
    assert "where docs/plan.md exists" in prompt  # stays conditional
    assert "run-phase" not in prompt  # the retired phase file is gone (WI-180)


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


def test_healthy_transcript_mentioning_limits_is_not_a_throttle(loop_repo):
    # The limit regex is gated on an error signal (is_error / nonzero exit):
    # the fake's commit action succeeds (exit 0) while its transcript says
    # "usage limit resets 3:45pm" — that session must read COMMITTED, never
    # WAITING.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("commit done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0
    index = (repo / "docs" / "iteration_index.md").read_text(encoding="utf-8")
    assert "WAITING" not in index
    assert "COMMITTED" in index


def test_session_timeout_cannot_wedge_the_loop(loop_repo):
    # A hung session is cut off at --session-timeout, logged as TIMEOUT, and
    # counts toward the stall guard (it produced no commit).
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("sleep", encoding="utf-8")
    proc = _loop(repo, template, "--session-timeout", "2", "--stall-limit", "1")
    assert proc.returncode == 4, proc.stdout + proc.stderr
    index = (repo / "docs" / "iteration_index.md").read_text(encoding="utf-8")
    assert "TIMEOUT" in index


def test_interactive_boots_exactly_one_session(loop_repo):
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("noop noop noop", encoding="utf-8")
    proc = _loop(repo, template, "--interactive")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _invocations(ctl) == 1
    # A hands-on session writes no unattended artifacts.
    assert not (repo / "docs" / "iteration").exists()


def test_unfilled_agent_cmd_is_inert_guidance(loop_repo):
    repo, _, _ = loop_repo
    proc = _loop(repo, "")
    assert proc.returncode == 2
    assert "AGENT_CMD" in proc.stderr


def test_missing_cli_fails_preflight_never_hangs(loop_repo):
    repo, _, _ = loop_repo
    proc = _loop(repo, "definitely-missing-agent-xyz --model {model}")
    assert proc.returncode == 2
    assert "not found" in proc.stderr


def test_privacy_check_author_violation_blocks_iteration_one(loop_repo):
    # Identity->privacy reframe (Thread 38 x 33): an unattended run under a
    # private (non-exempt) author is the history-leak disaster case — preflight
    # refuses to start.
    repo, ctl, template = loop_repo
    (repo / "docs" / "privacy-check").write_text("true\n", encoding="utf-8")
    # A genuinely private author (loop_repo's default loop@example.com is an
    # exempt RFC 2606 domain, so it would pass).
    subprocess.run(
        ["git", "-C", str(repo), "config", "user.email", "real.person@gmail.com"],
        capture_output=True,
    )
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "privacy-check author" in proc.stderr
    assert _invocations(ctl) == 0, "no session may run under a violated policy"


def test_zero_commit_repo_is_guarded(tmp_path):
    # The rev-parse guard: a repo with no commits yet must not crash the loop
    # (the NHW original assumed HEAD exists).
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "docs" / "status.md").write_text(STATUS_MD, encoding="utf-8")
    _git_ok = subprocess.run(
        ["git", "-C", str(repo), "init"], capture_output=True, text=True
    )
    assert _git_ok.returncode == 0
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "l@e.com"])
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "L"])
    ctl = tmp_path / "control"
    ctl.mkdir()
    fake = tmp_path / "fake_agent.py"
    fake.write_text(FAKE_AGENT, encoding="utf-8")
    template = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )
    (ctl / "actions.txt").write_text("commit done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    index = (repo / "docs" / "iteration_index.md").read_text(encoding="utf-8")
    assert "(root).." in index, "the first commit range starts at (root)"


def test_dirty_tree_at_start_injects_reconcile_and_logs(loop_repo):
    # WI-076: a non-empty working tree at loop start is residue from an
    # interrupted session. The loop logs one line and prepends the reconcile note
    # to the FIRST session's prompt — surface only: it never stashes or cleans.
    repo, ctl, template = loop_repo
    (repo / "leftover.txt").write_text("residue\n", encoding="utf-8")  # untracked
    proc = _loop(repo, template, "--max-iterations", "1")  # a single noop session
    assert "uncommitted path(s)" in proc.stderr
    assert "likely an interrupted session" in proc.stderr
    prompt = (ctl / "prompt.txt").read_text(encoding="utf-8")
    assert "reconcile them against the open work item" in prompt
    # surface only — the loop neither committed nor cleaned the residue
    assert (repo / "leftover.txt").read_text(encoding="utf-8") == "residue\n"
    assert "leftover.txt" in _git(repo, "status", "--porcelain")


def test_clean_tree_prompt_is_byte_identical(loop_repo):
    # WI-076: a clean tree at loop start injects nothing — the composed prompt is
    # byte-for-byte the default resume prompt, and no dirty-tree line is logged.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    prompt = (ctl / "prompt.txt").read_text(encoding="utf-8")
    assert prompt == load_script("agent_loop").DEFAULT_PROMPT
    assert "uncommitted path(s)" not in proc.stderr


def test_working_tree_dirty_counts_renames_and_untracked(tmp_path):
    # WI-076: porcelain parsing counts each uncommitted path once — a rename is a
    # single entry (not two), an untracked file a single '?? path' entry — and a
    # clean tree is empty. Exercised against a real repo (the encoding-safe
    # git() reader).
    loop = load_script("agent_loop")
    repo = tmp_path / "r"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "a@b.com")
    _git(repo, "config", "user.name", "A")
    (repo / "a.txt").write_text("hi\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    assert loop.working_tree_dirty(repo) == []  # clean
    (repo / "b.txt").write_text("new\n", encoding="utf-8")  # untracked
    assert len(loop.working_tree_dirty(repo)) == 1
    _git(repo, "add", "-A")
    _git(repo, "mv", "a.txt", "c.txt")  # a staged rename
    lines = loop.working_tree_dirty(repo)
    assert len(lines) == 2, lines  # the rename is ONE entry (+ b.txt), not three


@pytest.mark.skipif(os.name != "nt", reason="Windows CreateProcess/PATHEXT shim path")
def test_cmd_shim_cli_spawns_on_windows(loop_repo, tmp_path):
    # WI-120: an npm-style CLI installed only as a .cmd shim (no .exe) passes
    # preflight — shutil.which honors PATHEXT — but a bare argv[0] hits
    # CreateProcess, which resolves only .exe/.com, so every session died at
    # spawn with [WinError 2] (live: the opencode rows, sessions 002/005 of the
    # 2026-07-12 run). run_session now hands CreateProcess the which-resolved
    # path; the shim must launch, work, and end the run DONE with no ERROR row.
    repo, ctl, _template = loop_repo
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    shims = tmp_path / "shims"
    shims.mkdir()
    (shims / "fakecli.cmd").write_text(
        '@echo off\n"{}" "{}" %*\n'.format(sys.executable, tmp_path / "fake_agent.py"),
        encoding="utf-8",
    )
    env = augment_env(dict(os.environ))
    env["PATH"] = str(shims) + os.pathsep + env["PATH"]
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "agent_loop.py"),
            "--root",
            str(repo),
            "--agent-cmd",
            'fakecli --control "{}" --model {{model}} -p {{prompt}}'.format(ctl),
            "--pause",
            "0",
            "--model",
            "default-tier",
        ],
        cwd=str(repo),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _invocations(ctl) == 1
    index = (repo / "docs" / "iteration_index.md").read_text(encoding="utf-8")
    assert "DONE" in index and "ERROR" not in index


def test_stream_json_echo_and_result_parse(loop_repo):
    # WI-125: a stream-json session's events render live on the coordinator
    # console (assistant text as '  > ...', tool calls as '  * <name>'), and
    # the type:result event is parsed for outcome/telemetry even when a
    # trailing non-result event follows it (a killed stream must not shadow
    # the result; result/system events themselves are not echoed).
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("stream-done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "> refactoring the parser now" in proc.stdout
    assert "* Edit" in proc.stdout
    assert '"type": "result"' not in proc.stdout  # events echo compact, not raw
    log = sorted((repo / "docs" / "iteration").glob("*.log"))[0].read_text(
        encoding="utf-8"
    )
    assert "# outcome: DONE" in log
    assert "# tokens: 3+2" in log  # from the result event, not the trailing one
    assert "# turns: 2" in log


def test_no_session_echo_silences_the_console_not_the_log(loop_repo):
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("stream-done", encoding="utf-8")
    proc = _loop(repo, template, "--no-session-echo")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "refactoring the parser" not in proc.stdout  # console silenced...
    log = sorted((repo / "docs" / "iteration").glob("*.log"))[0].read_text(
        encoding="utf-8"
    )
    assert "refactoring the parser" in log  # ...but the stream is captured


# --- WI-137: telemetry commit hygiene + WI-keyed labels -----------------------


def test_telemetry_commits_itself_not_riding_the_next_commit(loop_repo):
    # WI-137: the coordinator commits its own bookkeeping (the iteration log +
    # regenerated index) in its own `telemetry:` commit right after writing it —
    # so it never dangles or rides the next session's work commit (session-021
    # defect-shape). After a run the tree carries no uncommitted iteration file,
    # and a telemetry commit exists naming the session.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("commit done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    porcelain = _git(repo, "status", "--porcelain")
    assert "docs/iteration" not in porcelain, "telemetry must not dangle"
    assert "iteration_index.md" not in porcelain
    subjects = _git(repo, "log", "--format=%s")
    assert "telemetry: session" in subjects, subjects
    # The telemetry commit is distinct from the session's own work commit.
    assert "progress" in subjects and "finishing" in subjects
    # The iteration logs are tracked, not just present on disk.
    tracked = _git(repo, "ls-files", "docs/iteration")
    assert tracked.count(".log") == 2


def test_telemetry_commit_is_best_effort_when_the_hook_vetoes(loop_repo):
    # WI-137 never-breaking: a pre-commit hook that vetoes the telemetry commit
    # must not abort the run — the files stay in the tree (today's behavior) and
    # the loop keeps going. Simulate with a hook that always fails; noop sessions
    # never make a work commit, so only the telemetry commit meets the veto.
    repo, ctl, template = loop_repo
    hook = repo / ".git" / "hooks" / "pre-commit"
    hook.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
    hook.chmod(0o755)
    (ctl / "actions.txt").write_text("noop noop", encoding="utf-8")
    proc = _loop(repo, template, "--max-iterations", "2", "--stall-limit", "9")
    assert proc.returncode == 6, proc.stdout + proc.stderr  # budget, not a crash
    assert "telemetry commit skipped" in proc.stderr
    assert len(sorted((repo / "docs" / "iteration").glob("*.log"))) == 2  # on disk
    # ...and unstaged: the veto leaves the index as before, not `A  <path>`
    # primed to ride the next session's work commit (review 031-A).
    staged = _git(repo, "diff", "--cached", "--name-only")
    assert "docs/iteration" not in staged, staged
    assert "iteration_index.md" not in staged, staged


def test_wi_label_recorded_in_log_header_and_index(loop_repo):
    # WI-137 / WI-180: the WI the session claims is captured at session start into
    # a `# wi:` log header line and a WI index column. With docs/next-wi retired,
    # the durable per-session scope pointer is docs/rework-wi (a review rework
    # override); the dispatcher supplies the explicit assignment (Slice D).
    repo, ctl, template = loop_repo
    (repo / "docs" / "rework-wi").write_text("# comment\nWI-137\n", encoding="utf-8")
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    log = sorted((repo / "docs" / "iteration").glob("*.log"))[0].read_text(
        encoding="utf-8"
    )
    assert "# wi: WI-137" in log
    index = (repo / "docs" / "iteration_index.md").read_text(encoding="utf-8")
    assert "| WI | Model |" in index  # the new column header
    assert "WI-137" in index


# --- WI-136: live per-workstream status line ----------------------------------


def test_summarize_session_line_shapes():
    import json

    loop = load_script("agent_loop")
    txt = json.dumps(
        {"type": "assistant", "message": {"content": [{"type": "text", "text": "hi"}]}}
    )
    assert loop.summarize_session_line(txt) == ["  > hi"]
    tool = json.dumps(
        {
            "type": "assistant",
            "message": {"content": [{"type": "tool_use", "name": "Edit", "input": {}}]},
        }
    )
    assert loop.summarize_session_line(tool) == ["  * Edit"]
    # result/system events are log detail, not progress.
    assert loop.summarize_session_line(json.dumps({"type": "result"})) == []
    # a non-JSON plain-text line passes through.
    assert loop.summarize_session_line("plain cli output") == ["plain cli output"]
    assert loop.summarize_session_line("   ") == []


def test_live_status_rewrites_one_line_in_place():
    import io
    import json

    loop = load_script("agent_loop")
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        ls = loop.LiveStatus("single")
        ls.event(
            json.dumps(
                {
                    "type": "assistant",
                    "message": {
                        "content": [{"type": "tool_use", "name": "Edit", "input": {}}]
                    },
                }
            )
        )
        ls.event(
            json.dumps(
                {
                    "type": "assistant",
                    "message": {"content": [{"type": "text", "text": "next step"}]},
                }
            )
        )
        ls.finish()
    finally:
        sys.stdout = old
    out = buf.getvalue()
    assert "\r\x1b[2K" in out  # carriage-return + clear-to-EOL rewrite
    assert "[single]" in out and "Edit" in out and "next step" in out
    assert out.endswith("\n")  # finish() closes the line
    # A no-op finish (nothing rendered) writes nothing.
    buf2 = io.StringIO()
    sys.stdout = buf2
    try:
        loop.LiveStatus("x").finish()
    finally:
        sys.stdout = old
    assert buf2.getvalue() == ""


def test_live_status_falls_back_to_scroll_on_non_tty(loop_repo):
    # WI-136 never-breaking: --live-status on a non-TTY (the test subprocess's
    # stdout is a pipe) must keep the append-only scroll, not emit raw escapes —
    # CI logs stay readable. The scrolling summaries still appear.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("stream-done", encoding="utf-8")
    proc = _loop(repo, template, "--live-status")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "> refactoring the parser" in proc.stdout  # scrolled, not rewritten
    assert "\x1b[2K" not in proc.stdout  # no in-place escapes on a non-TTY


# --- WI-080 Slice A golden net: model-map / {model} preflight guards -----------


def test_model_map_entry_without_equals_fails_preflight(loop_repo):
    # A --model-map entry lacking '=' is a parse error -> EXIT_PREFLIGHT before any
    # session runs, with the message on stderr (the preflight contract).
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(repo, template, "--model-map", "BUILDstrong")
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "without '='" in proc.stderr
    assert _invocations(ctl) == 0, "a parse failure must start no session"


def test_parse_map_rejects_entry_without_equals():
    # The pure parser raises ValueError on a no-'=' entry (the guard the preflight
    # above leans on); a well-formed map still parses.
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
    # body None -> the default prompt, no preamble/reconcile, guardrails off ->
    # unchanged base and guarded False.
    al = load_script("agent_loop")
    prompt, guarded = al.compose_session_prompt(
        "claude-opus-4-8", None, "", "", "DEFAULT-PROMPT", "off", tmp_path, []
    )
    assert prompt == "DEFAULT-PROMPT"
    assert guarded is False


def test_compose_session_prompt_ordering(tmp_path):
    # reconcile + preamble + body concatenate in exactly that order (body
    # overrides the default prompt); guardrails off -> guarded False.
    al = load_script("agent_loop")
    prompt, guarded = al.compose_session_prompt(
        "claude-opus-4-8", "BODY", "RECON\n", "PRE\n", "DEFAULT", "off", tmp_path, []
    )
    assert prompt == "RECON\nPRE\nBODY"
    assert guarded is False


def test_compose_session_prompt_guardrails_on(tmp_path):
    # policy selects the model and a real core.md is vendored -> the core is
    # prepended ahead of the base with the "---" separator, and guarded is True.
    al = load_script("agent_loop")
    _vendor_core(tmp_path, "CORE-RULES\n")
    prompt, guarded = al.compose_session_prompt(
        "claude-opus-4-8", None, "", "", "BASE", "opus", tmp_path, []
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
        "claude-opus-4-8", None, "", "", "BASE", "opus", tmp_path, warned
    )
    assert prompt == "BASE"
    assert guarded is False
    first = capsys.readouterr()
    assert "core.md is absent" in first.err
    assert warned == [True]

    prompt2, guarded2 = al.compose_session_prompt(
        "claude-opus-4-8", None, "", "", "BASE", "opus", tmp_path, warned
    )
    assert prompt2 == "BASE"
    assert guarded2 is False
    second = capsys.readouterr()
    assert "core.md is absent" not in second.err


def test_model_placeholder_without_model_fails_preflight(loop_repo):
    # A template carrying {model} with NO model configured (no --model /
    # --model-map / AGENT_MODEL) must exit EXIT_PREFLIGHT naming the missing model.
    # preflight() accepts the launchable template, so the mid-loop guard is what
    # fires at iteration 1 — before any session runs (the _loop helper is bypassed
    # here precisely because it always wires --model).
    repo, ctl, template = loop_repo  # template carries `--model {model}`
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = run_py(
        [
            SCRIPTS / "agent_loop.py",
            "--root",
            repo,
            "--agent-cmd",
            template,
            "--pause",
            "0",
            # deliberately NO --model / --model-map / AGENT_MODEL
        ],
        cwd=repo,
    )
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "no model is configured for this phase" in proc.stderr
    assert _invocations(ctl) == 0, "the guard fires before any session launches"


# =============================================================================
# WI-080 Slice C — RoutingState transitions
# =============================================================================
# The serial loop's ~24 routing/escalation/critique/stall locals now live on one
# RoutingState whose methods are PURE transitions (mutate the object, return a
# decision — no I/O). These pin single transitions directly; the end-to-end
# routing/critique/stall behavior is still pinned by the golden-net suites above.


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
            (None, False, "NEEDS-HUMAN", True, {"is_error": False}, 0),
            ("NEEDS-HUMAN", False),
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


def _train_repo(tmp_path, train="t1", assigned=("WI-201",)):
    """A throwaway repo: a seed commit (the integration base), then branch
    llm/train/<train>. Returns (repo, base, worker-dict) — the worker carries
    exactly the keys worker_endstate reads."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    (repo / ".gitignore").write_text("out/\n", encoding="utf-8")
    (repo / "seed.txt").write_text("seed\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    base = _git(repo, "rev-parse", "HEAD")
    _git(repo, "checkout", "-q", "-b", "llm/train/" + train)
    worker = {"train": train, "assigned": list(assigned), "base": base, "rework": ""}
    return repo, base, worker


def _build_commit(repo, wi, train, base):
    (repo / ("work-" + wi + ".txt")).write_text("work " + wi, encoding="utf-8")
    _git(repo, "add", "-A")
    msg = "build {}\n\nWI: {}\nTrain: {}\nBase: {}\n".format(wi, wi, train, base)
    _git(repo, "commit", "-q", "-m", msg)


@pytest.mark.skipif(not __import__("shutil").which("git"), reason="needs git on PATH")
def test_worker_endstate_done_names_train_branch(tmp_path):
    al = load_script("agent_loop")
    repo, base, worker = _train_repo(tmp_path)
    _build_commit(repo, "WI-201", "t1", base)
    end = al.worker_endstate(str(repo), worker, False, False, 1)
    assert end is not None
    code, label, detail = end
    assert code == al.EXIT_DONE
    assert label == "DONE"
    assert al.TRAIN_BRANCH_PREFIX + "t1" in detail


@pytest.mark.skipif(not __import__("shutil").which("git"), reason="needs git on PATH")
def test_worker_endstate_review_open_defers(tmp_path):
    al = load_script("agent_loop")
    repo, base, worker = _train_repo(tmp_path)
    _build_commit(repo, "WI-201", "t1", base)
    # Built + clean, but the caller reports the train's review cycle still open.
    assert al.worker_endstate(str(repo), worker, True, False, 1) is None


@pytest.mark.skipif(not __import__("shutil").which("git"), reason="needs git on PATH")
def test_worker_endstate_rework_pending_defers(tmp_path):
    al = load_script("agent_loop")
    repo, base, worker = _train_repo(tmp_path)
    _build_commit(repo, "WI-201", "t1", base)
    worker["rework"] = "a CHANGES-REQUESTED verdict is pending"
    assert al.worker_endstate(str(repo), worker, False, False, 1) is None


@pytest.mark.skipif(not __import__("shutil").which("git"), reason="needs git on PATH")
def test_worker_endstate_blocked_trailer_exits_blocked(tmp_path):
    al = load_script("agent_loop")
    repo, base, worker = _train_repo(tmp_path)
    (repo / "work-WI-201.txt").write_text("stuck", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(
        repo,
        "commit",
        "-q",
        "-m",
        "blocked WI-201\n\nBlocked-WI: WI-201\nBlockRef: OI-99\n",
    )
    end = al.worker_endstate(str(repo), worker, False, False, 1)
    assert end is not None
    code, label, detail = end
    assert code == al.EXIT_BLOCKED
    assert label == "BLOCKED"
    assert "OI-99" in detail


@pytest.mark.skipif(not __import__("shutil").which("git"), reason="needs git on PATH")
def test_worker_endstate_dirty_tree_defers(tmp_path):
    al = load_script("agent_loop")
    repo, base, worker = _train_repo(tmp_path)
    _build_commit(repo, "WI-201", "t1", base)
    # Committed evidence is complete, but an uncommitted path means not-done.
    (repo / "scratch.txt").write_text("uncommitted", encoding="utf-8")
    assert al.worker_endstate(str(repo), worker, False, False, 1) is None


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
