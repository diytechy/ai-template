"""The unattended coordinator engine (Thread 33, process-options.md
"Unattended operation") — exercised end-to-end against a fake agent command,
so no test depends on any real agent CLI. The fake pops one action per
invocation from a control dir outside the repo: commit / noop / done /
blocked / needs-human / limit / sleep."""

import datetime
import subprocess
import sys

import pytest
from conftest import SCRIPTS, load_script, run_py

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
    pathlib.Path("docs/run-state").write_text(action.upper())
    print(json.dumps({"result": "ok",
                      "usage": {"input_tokens": 10, "output_tokens": 5},
                      "total_cost_usd": 0.12}))
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
    index = (repo / "docs" / "iteration_index.md").read_text(encoding="utf-8")
    assert "| 001 |" in index and "| 002 |" in index
    assert "COMMITTED" in index and "DONE" in index
    assert "10+5" in index and "0.12" in index  # tokens + cost from the JSON
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


def test_phase_model_map_picks_the_declared_tier(loop_repo):
    # docs/run-phase is the coordinator's model-tier key: a mapped phase gets
    # the strong model, everything else the default.
    repo, ctl, template = loop_repo
    (repo / "docs" / "run-phase").write_text("P2\n", encoding="utf-8")
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(repo, template, "--model-map", "P0=other,P2=strong-tier")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    models = (ctl / "models.txt").read_text(encoding="utf-8").split()
    assert models == ["strong-tier"]


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
    # policy=a model substring: the BUILD session (opus) is guarded; a PLAN
    # session (fable) would not be. Here BUILD runs, so the core is injected.
    repo, ctl, template = loop_repo
    _vendor_core(repo, "MARKER-CORE\n")
    (repo / "docs" / "guardrails-policy").write_text("opus\n", encoding="utf-8")
    (repo / "docs" / "run-phase").write_text("BUILD\n", encoding="utf-8")
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(repo, template, "--model-map", "PLAN=fable-5,BUILD=claude-opus-4-8")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "MARKER-CORE" in (ctl / "prompt.txt").read_text(encoding="utf-8")


def test_guardrails_strong_tier_is_not_injected(loop_repo):
    # Same policy, but the PLAN session runs on the frontier model (fable): no
    # substring match -> the guardrails core is not injected.
    repo, ctl, template = loop_repo
    _vendor_core(repo, "MARKER-CORE\n")
    (repo / "docs" / "guardrails-policy").write_text("opus\n", encoding="utf-8")
    (repo / "docs" / "run-phase").write_text("PLAN\n", encoding="utf-8")
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(repo, template, "--model-map", "PLAN=fable-5,BUILD=claude-opus-4-8")
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
    # WI-1.29: the engine's resume prompt is where the cadence becomes real —
    # without these instructions a driver session never bounces run-phase
    # between PLAN and BUILD, and the launcher's model map has nothing to key
    # on. Conditional ("where docs/plan.md exists"), like the iteration-branch
    # clause, so a repo without the plan surface is unchanged.
    prompt = load_script("agent_loop").DEFAULT_PROMPT
    assert "docs/plan.md" in prompt
    assert "PLAN" in prompt and "BUILD" in prompt
    assert "iteration_index.md" in prompt  # the sizing servo's sensor
    assert "where docs/plan.md exists" in prompt  # stays conditional


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
