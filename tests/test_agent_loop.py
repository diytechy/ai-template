"""The unattended coordinator engine (Thread 33, process-options.md
"Unattended operation") — exercised end-to-end against a fake agent command,
so no test depends on any real agent CLI. The fake pops one action per
invocation from a control dir outside the repo: commit / noop / done /
blocked / needs-human / limit / sleep.

WI-277 split this module by behavior boundary. What stays here is everything
that needs the FAKE_AGENT/loop_repo subprocess harness, plus the lock, the
git-helper and zero-commit effect tests. The pure declared-policy/dial parsers
moved to tests/test_agent_loop_policy.py, the RoutingState transitions and the
outcome ladder to tests/test_agent_loop_routing.py, and the worker end-state /
assignment seam to tests/test_agent_loop_worker.py (its own leg's module).
"""

import datetime
import os
import re
import subprocess
import sys

import pytest
from conftest import (
    SCRIPTS,
    augment_env,
    load_script,
    pin_autocrlf,
    run_py,
    write_wi_registry,
)

# The fake agent: records every invocation + the model it was handed, then
# performs the next scripted action in the repo it was launched in (cwd),
# exactly as a headless driver session would.
FAKE_AGENT = """
import argparse, json, pathlib, re, subprocess, sys, time

ap = argparse.ArgumentParser()
ap.add_argument("--control", required=True)
ap.add_argument("--model", default="")
ap.add_argument("-p", "--prompt", default="")
args, extra = ap.parse_known_args()
if not args.prompt:
    # No {prompt} on the command line -> the WI-216 stdin path delivered it
    # instead (run_session writes it then closes stdin, so this never hangs).
    args.prompt = sys.stdin.read()
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
elif action in ("done", "blocked"):
    # WI-210: end states are committed WORKER EVIDENCE (trailers parsed from
    # the assignment prompt), never a run-state write — the serial driver
    # that read run-state back is retired.
    m = re.search(r"- WI: (WI-\\d+)", args.prompt)
    wi = m.group(1) if m else "WI-201"
    m = re.search(r"- Branch: (\\S+) \\(its claim", args.prompt)
    train = m.group(1) if m else "t1"
    m = re.search(r"integration base ([0-9a-f]+)\\)", args.prompt)
    base = m.group(1) if m else ""
    pathlib.Path("work.txt").write_text("finishing" + str(count))
    subprocess.run(["git", "add", "-A"], check=True)
    if action == "blocked":
        msg = ("blocked " + wi + "\\n\\nBlocked-WI: " + wi +
               "\\nBlockRef: OI-1\\nTrain: " + train + "\\nBase: " + base)
    else:
        msg = ("build " + wi + "\\n\\nWI: " + wi + "\\nTrain: " + train +
               "\\nBase: " + base)
    subprocess.run(["git", "commit", "-q", "-m", msg], check=True)
    print(json.dumps({"result": "ok",
                      "usage": {"input_tokens": 10, "output_tokens": 5,
                                "cache_read_input_tokens": 70000,
                                "cache_creation_input_tokens": 9000},
                      "total_cost_usd": 0.12,
                      "duration_api_ms": 61000, "num_turns": 7,
                      "ttft_ms": 4200, "fast_mode_state": "off"}))
elif action == "stream-done":
    # A stream-json CLI: per-turn events, then the result event NOT last (a
    # trailing event must not shadow it - the parse preference under test).
    m = re.search(r"- WI: (WI-\\d+)", args.prompt)
    wi = m.group(1) if m else "WI-201"
    m = re.search(r"- Branch: (\\S+) \\(its claim", args.prompt)
    train = m.group(1) if m else "t1"
    m = re.search(r"integration base ([0-9a-f]+)\\)", args.prompt)
    base = m.group(1) if m else ""
    pathlib.Path("work.txt").write_text("finishing" + str(count))
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-q", "-m",
                    "build " + wi + "\\n\\nWI: " + wi + "\\nTrain: " +
                    train + "\\nBase: " + base], check=True)
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

- **Active gate:** DevStg-Reqs
- **Open items:**
  - **Needs <human>**:
    - OI-1 — decide: approve the demo gate (blocks: DevStg-Reqs)

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
    (repo / "docs" / "requirements").mkdir(parents=True)
    (repo / "docs" / "status.md").write_text(STATUS_MD, encoding="utf-8")
    # out/ (the lock + raw run logs) must never dirty the tree: a worker's
    # DONE is judged from committed evidence + a clean tree (worker_endstate).
    (repo / ".gitignore").write_text("out/\n", encoding="utf-8")
    write_wi_registry(
        repo,
        [
            [
                "WI-200",
                "Earlier thing",
                "ws",
                "",
                "",
                "done",
                "shipped",
                "",
                "quick",
                "",
            ],
            [
                "WI-201",
                "Scoped work for WI-201",
                "ws",
                "",
                "WI-200",
                "queued",
                "",
                "docs/specs/thing.md",
                "medium",
                "ordinary",
            ],
        ],
    )
    _git(repo, "init")
    pin_autocrlf(repo)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "initial")
    _git(repo, "checkout", "-q", "-b", "llm/train/t1")
    ctl = tmp_path / "control"
    ctl.mkdir()
    fake = tmp_path / "fake_agent.py"
    fake.write_text(FAKE_AGENT, encoding="utf-8")
    template = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )
    return repo, ctl, template


def _loop(repo, template, *extra):
    # The worker assignment (--wi/--train; --base defaults to HEAD at worker
    # start) — WI-210 retired the bare resume launch, so the engine tests
    # drive the same worker path the dispatcher spawns.
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
            "--wi",
            "WI-201",
            "--train",
            "t1",
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
    assert "worker t1 [WI-201]: DONE" in proc.stdout
    assert "CONSENT" in proc.stdout, "the banner must state the consent line"
    logs = sorted((repo / "docs" / "iteration").glob("t1-*.log"))
    assert len(logs) == 2
    meta = logs[1].read_text(encoding="utf-8")
    assert "# outcome: COMMITTED" in meta  # the trailer commit; DONE is the
    assert "# exit-code: 0" in meta  # worker exit banner, not a session state
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
    # A worker never regenerates the iteration index — it is a GENERATED root
    # artifact the integrator rebuilds on the composed tree (spec §5.1).
    assert not (repo / "docs" / "iteration_index.md").exists()
    # The raw unbounded stream lands in the gitignored out/run-logs/.
    assert list((repo / "out" / "run-logs").glob("*.log"))


def test_blocked_exit(loop_repo):
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("blocked", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 3, proc.stdout + proc.stderr
    assert "worker t1 [WI-201]: BLOCKED" in proc.stdout
    assert "BlockRef: OI-1" in proc.stdout


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


# --- WI-148: weekday blackout window ------------------------------------------


def test_blackout_present_but_inactive_does_not_block(loop_repo):
    # A docs/blackout file whose window does NOT cover "now" is a no-op: the
    # session runs and the loop reaches DONE (proves the loop reads the file and
    # only waits when actually inside the window).
    repo, ctl, template = loop_repo
    now = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    # A 1-minute window THIRTY minutes ahead — never active at loop start,
    # whatever the wall clock or weekday. (Thirty, not two: on a saturated CI
    # box a >2-minute stall between computing the window and the loop's check
    # would put "now" INSIDE the window and wedge the run — repo-review
    # 2026-07-21 L-17.)
    start = (now + datetime.timedelta(minutes=30)).strftime("%H:%M")
    end = (now + datetime.timedelta(minutes=31)).strftime("%H:%M")
    (repo / "docs" / "blackout").write_text(
        "{}-{}\n".format(start, end), encoding="utf-8"
    )
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "worker t1 [WI-201]: DONE" in proc.stdout
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
    assert "- WI: WI-201" in prompt  # the assignment prompt still follows


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
    log = sorted((repo / "docs" / "iteration").glob("t1-*.log"))[0].read_text(
        encoding="utf-8"
    )
    assert "# outcome: WAITING" in log


def test_error_session_reads_error_not_no_commit(loop_repo):
    # Thread 45: a session the CLI reports as errored (is_error, not a rate
    # limit) is logged ERROR, distinct from a healthy no-commit session — so the
    # index tells "agent failed" apart from "ran and idled". The run continues
    # (one error is under the stall limit) and finishes on the next session.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("error done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    logs = sorted((repo / "docs" / "iteration").glob("t1-*.log"))
    heads = [lg.read_text(encoding="utf-8") for lg in logs]
    assert any("# outcome: ERROR" in h for h in heads)
    assert not any("# outcome: NO-COMMIT" in h for h in heads)


def test_plain_text_nonzero_exit_reads_error(loop_repo):
    # No JSON, just a nonzero exit (a plain-text agent template that failed) is
    # also ERROR — the same signal limit_reset_hint trusts, and it covers the
    # unlaunchable-session sentinel too.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("error-plain done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    logs = sorted((repo / "docs" / "iteration").glob("t1-*.log"))
    assert any("# outcome: ERROR" in lg.read_text(encoding="utf-8") for lg in logs)


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


def test_commit_resets_the_stall_counter(loop_repo):
    # SR-172: the stall window is CONSECUTIVE no-progress sessions — a session
    # that commits resets the counter, so interleaved progress is never ended
    # by the limit. noop commit noop noop at --stall-limit 2: without the reset
    # the two non-adjacent noops would abort the run at session 3; with it the
    # stalling pair is sessions 3–4 and the abort lands at session 4.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("noop commit noop noop", encoding="utf-8")
    proc = _loop(repo, template, "--stall-limit", "2", "--max-iterations", "6")
    assert proc.returncode == 4, proc.stdout + proc.stderr
    assert "STALL" in proc.stdout
    assert _invocations(ctl) == 4, "the commit must reset the stall counter"


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


def _nosleep_loop(tmp_path, repo, template, *extra, freeze_now=None):
    """Run the loop through a driver that replaces time.sleep with a recorder.

    The parsed-reset wait is wall-clock sized (seconds until "3:45pm" — up to a
    day) and the fallback default is a full hour, so those sleeps must be
    OBSERVED, never served: the driver records each requested duration to a
    file and returns immediately. Returns (proc, recorded-waits).

    `freeze_now` (a `datetime`) additionally pins the loop's clock. Without it
    the parsed wait depends on the wall clock, so a test CANNOT choose a ceiling
    equal to it — which is why the `<=` boundary went unpinned. `seconds_until_reset`
    reads `datetime.datetime.now()` through the module attribute, so replacing
    that attribute in the driver makes the parsed wait exactly computable."""
    sleep_log = tmp_path / "sleeps.txt"
    driver = tmp_path / "nosleep_driver.py"
    freeze_src = ""
    if freeze_now is not None:
        freeze_src = (
            "import datetime as _dt\n"
            "class _Frozen(_dt.datetime):\n"
            "    @classmethod\n"
            "    def now(cls, tz=None):\n"
            "        return cls({}, {}, {}, {}, {}, {})\n"
            "_dt.datetime = _Frozen\n"
        ).format(
            freeze_now.year,
            freeze_now.month,
            freeze_now.day,
            freeze_now.hour,
            freeze_now.minute,
            freeze_now.second,
        )
    driver.write_text(
        "import pathlib, runpy, sys, time\n"
        + freeze_src
        + "log = pathlib.Path(sys.argv[1])\n"
        "script = sys.argv[2]\n"
        "def record(secs):\n"
        "    with log.open('a') as fh:\n"
        "        fh.write('{}\\n'.format(secs))\n"
        "time.sleep = record\n"
        "sys.argv = [script] + sys.argv[3:]\n"
        "runpy.run_path(script, run_name='__main__')\n",
        encoding="utf-8",
    )
    proc = run_py(
        [
            driver,
            sleep_log,
            SCRIPTS / "agent_loop.py",
            "--root",
            repo,
            "--agent-cmd",
            template,
            "--pause",
            "0",
            "--model",
            "default-tier",
            "--wi",
            "WI-201",
            "--train",
            "t1",
            *extra,
        ],
        cwd=repo,
    )
    waits = []
    if sleep_log.exists():
        waits = [float(x) for x in sleep_log.read_text(encoding="utf-8").split()]
    return proc, waits


def test_fallback_nap_is_capped_at_the_wait_ceiling(loop_repo, tmp_path):
    # Round-2 F5 pin (a), RE-PINNED ON THE SERVED SLEEP (2026-08-17 desk round,
    # F13). With the declared fallback ABOVE the ceiling (5 > 1) the nap must be
    # the ceiling — min(fallback, ceiling) is load-bearing.
    #
    # WHY THE PRINT IS NOT THE PIN. The loop computes `wait = min(fallback,
    # ceiling)`, PRINTS it, then sleeps it, so a string assertion on the message
    # only catches mutations that move both. Napping the raw dial while leaving
    # the print untouched (`time.sleep(args.limit_retry_fallback)`) demonstrably
    # slept 5s past a 1s ceiling and this test PASSED — the runtime was the only
    # tell (1.53s -> 5.57s). The subject of this pin is a wait duration, so it
    # is measured with the instrument that can see one: the recording driver.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("limit-odd done", encoding="utf-8")
    proc, waits = _nosleep_loop(
        tmp_path, repo, template, "--wait-on-limit", "1", "--limit-retry-fallback", "5"
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "sleeping 1s (--limit-retry-fallback)" in proc.stdout, proc.stdout
    # THE ASSERTIONS THAT BITE — what was SERVED, not what was said. Both
    # directions, because "the ceiling was slept" and "the raw dial was never
    # slept" fail under different mutations.
    assert 1.0 in waits, waits
    assert 5.0 not in waits, "the raw fallback must never be served past the ceiling"
    assert _invocations(ctl) == 2, "the throttled session must be retried"


def test_parsed_reset_within_ceiling_sleeps_and_retries(loop_repo, tmp_path):
    # Round-2 F5 pin (b): a PARSEABLE reset wording ("resets 3:45pm") within
    # the ceiling drives the wait through seconds_until_reset — the loop prints
    # the parsed wait with its reset time, sleeps it, and RETRIES the session,
    # never exiting WAITING and never taking the unparseable-fallback nap.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("limit done", encoding="utf-8")
    # Ceiling 90000 > 86400: any time of day parses to a wait under the
    # ceiling, whatever the wall clock says when this runs.
    proc, waits = _nosleep_loop(tmp_path, repo, template, "--wait-on-limit", "90000")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    m = re.search(r"sleeping (\d+)s until the reset \(3:45pm\)", proc.stdout)
    assert m, "the parsed-reset branch must print its wait: " + proc.stdout
    assert 0 < int(m.group(1)) <= 86400
    assert float(m.group(1)) in waits, "the printed wait must be the slept wait"
    assert "(--limit-retry-fallback)" not in proc.stdout, "fallback must not fire"
    assert _invocations(ctl) == 2, "the throttled session must be retried"


def test_a_reset_landing_EXACTLY_on_the_ceiling_is_slept_not_abandoned(
    loop_repo, tmp_path
):
    """The `<=` boundary, pinned in BOTH directions (2026-08-17 desk round, F15).

    LLR-174 states the fork explicitly — a parsed reset *within* the ceiling is
    slept and retried, *past* it the run stops at EXIT_WAITING — so the equal
    case belongs to the sleeping arm. Nothing pinned it: mutating
    `wait <= args.wait_on_limit` to `wait <` left the whole agent-loop suite
    green (88 passed, 1 skipped), because the one parsed-reset test uses a
    ceiling of 90000 against a wait structurally under 86400, a 3600-second gap
    the boundary can never be reached through.

    Freezing the clock is what makes the equal case constructible: at
    2026-01-01 12:00:00 a "3:45pm" hint parses to exactly 13500s, so the ceiling
    can be set to precisely that."""
    repo, ctl, template = loop_repo
    frozen = datetime.datetime(2026, 1, 1, 12, 0, 0)
    exact = 3 * 3600 + 45 * 60  # 12:00:00 -> 15:45:00
    al = load_script("agent_loop")
    assert al.seconds_until_reset("resets 3:45pm", now=frozen) == exact

    (ctl / "actions.txt").write_text("limit done", encoding="utf-8")
    proc, waits = _nosleep_loop(
        tmp_path,
        repo,
        template,
        "--wait-on-limit",
        str(exact),
        freeze_now=frozen,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert float(exact) in waits, waits
    assert _invocations(ctl) == 2, "a reset AT the ceiling must be waited out"


def test_a_reset_ONE_SECOND_past_the_ceiling_abandons_the_run(loop_repo, tmp_path):
    """The other arm of the same fork, so the boundary pin above cannot be
    satisfied by a predicate that simply always sleeps. Same frozen clock, same
    13500s parsed wait, ceiling one second lower: the run must stop at
    EXIT_WAITING (5) rather than sleep past what the human consented to."""
    repo, ctl, template = loop_repo
    frozen = datetime.datetime(2026, 1, 1, 12, 0, 0)
    exact = 3 * 3600 + 45 * 60
    (ctl / "actions.txt").write_text("limit done", encoding="utf-8")
    proc, waits = _nosleep_loop(
        tmp_path,
        repo,
        template,
        "--wait-on-limit",
        str(exact - 1),
        freeze_now=frozen,
    )
    assert proc.returncode == 5, proc.stdout + proc.stderr
    assert float(exact) not in waits, waits


def test_limit_retry_fallback_defaults_to_3600(loop_repo, tmp_path):
    # Round-2 F5 pin (c): LLR-174 declares the fallback dial's default 3600 —
    # with --wait-on-limit above it and NO --limit-retry-fallback flag, the
    # unparseable-reset nap must be exactly 3600s (the declared default, not an
    # in-line literal), printed and slept (observed via the recording driver).
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("limit-odd done", encoding="utf-8")
    proc, waits = _nosleep_loop(tmp_path, repo, template, "--wait-on-limit", "90000")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "sleeping 3600s (--limit-retry-fallback)" in proc.stdout, proc.stdout
    assert 3600.0 in waits, "the declared default must be the slept wait"
    assert _invocations(ctl) == 2, "the throttled session must be retried"


def test_stall_limit_defaults_to_three_no_commit_sessions(loop_repo):
    # Round-2 F6 pin: LLR-175 declares --stall-limit's default 3. No flag
    # passed, every session noops: the SECOND no-commit session must not end
    # the run (a third invocation happens) and the THIRD must — EXIT_STALL (4)
    # at exactly three invocations, not two, not the 6-session budget.
    repo, ctl, template = loop_repo  # no actions file -> every session noops
    proc = _loop(repo, template, "--max-iterations", "6")
    assert proc.returncode == 4, proc.stdout + proc.stderr
    assert "STALL" in proc.stdout
    assert _invocations(ctl) == 3, "the declared default (3) must stop the run"


def test_healthy_transcript_mentioning_limits_is_not_a_throttle(loop_repo):
    # The limit regex is gated on an error signal (is_error / nonzero exit):
    # the fake's commit action succeeds (exit 0) while its transcript says
    # "usage limit resets 3:45pm" — that session must read COMMITTED, never
    # WAITING.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("commit done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0
    heads = [
        lg.read_text(encoding="utf-8")
        for lg in (repo / "docs" / "iteration").glob("t1-*.log")
    ]
    assert not any("# outcome: WAITING" in h for h in heads)
    assert any("# outcome: COMMITTED" in h for h in heads)


def test_session_timeout_cannot_wedge_the_loop(loop_repo):
    # A hung session is cut off at --session-timeout, logged as TIMEOUT, and
    # counts toward the stall guard (it produced no commit).
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("sleep", encoding="utf-8")
    proc = _loop(repo, template, "--session-timeout", "2", "--stall-limit", "1")
    assert proc.returncode == 4, proc.stdout + proc.stderr
    logs = sorted((repo / "docs" / "iteration").glob("t1-*.log"))
    assert any("# outcome: TIMEOUT" in lg.read_text(encoding="utf-8") for lg in logs)


def test_interactive_boots_exactly_one_session(loop_repo):
    # --interactive is its own explicit role (never a worker assignment), so
    # it launches without --wi/--train.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("noop noop noop", encoding="utf-8")
    proc = run_py(
        [
            SCRIPTS / "agent_loop.py",
            "--root",
            repo,
            "--agent-cmd",
            template,
            "--model",
            "default-tier",
            "--interactive",
        ],
        cwd=repo,
    )
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
    # (the NHW original assumed HEAD exists). A dispatcher never assigns from
    # an unborn HEAD, so the worker here simply must run controlled — first
    # commit range (root).., no traceback — and exit on its budget.
    repo = tmp_path / "repo"
    (repo / "docs" / "requirements").mkdir(parents=True)
    (repo / "docs" / "status.md").write_text(STATUS_MD, encoding="utf-8")
    write_wi_registry(
        repo,
        [
            [
                "WI-201",
                "Scoped work for WI-201",
                "ws",
                "",
                "",
                "queued",
                "",
                "",
                "medium",
                "ordinary",
            ]
        ],
    )
    (repo / ".gitignore").write_text("out/\n", encoding="utf-8")
    _git_ok = subprocess.run(
        ["git", "-C", str(repo), "init"], capture_output=True, text=True
    )
    assert _git_ok.returncode == 0
    pin_autocrlf(repo)  # WI-461/WI-465; see conftest.pin_autocrlf
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "l@e.com"])
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "L"])
    subprocess.run(
        ["git", "-C", str(repo), "checkout", "-q", "-b", "llm/train/t1"],
        capture_output=True,
    )
    ctl = tmp_path / "control"
    ctl.mkdir()
    fake = tmp_path / "fake_agent.py"
    fake.write_text(FAKE_AGENT, encoding="utf-8")
    template = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )
    (ctl / "actions.txt").write_text("commit commit", encoding="utf-8")
    proc = _loop(repo, template, "--max-iterations", "2")
    # A worker has no integration base on an unborn HEAD: the guard is a
    # controlled fail-closed preflight refusal, never a crash.
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "Traceback" not in proc.stdout + proc.stderr
    assert "no HEAD commit" in proc.stderr


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
    assert "uncommitted changes" not in prompt  # no reconcile note injected
    assert prompt.startswith("You are an unattended worker") or "- WI: WI-201" in prompt
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
    pin_autocrlf(repo)  # WI-461/WI-465; see conftest.pin_autocrlf
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


def _git_repo(tmp_path):
    # A one-config git repo for the agent_common.git() wrapper tests (WI-233).
    repo = tmp_path / "r"
    repo.mkdir()
    _git(repo, "init")
    pin_autocrlf(repo)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(repo, "config", "user.email", "a@b.com")
    _git(repo, "config", "user.name", "A")
    return repo


def test_git_appends_stderr_on_hook_rejection(tmp_path):
    # WI-233: a commit the pre-commit hook rejects (its whole report goes to
    # stderr) must return the hook's failing check in the text — not the blank
    # detail every `detail=out[:200]` park reason carried before. The hook is a
    # #!/bin/sh script git runs cross-platform (via its bundled sh on Windows).
    ac = load_script("agent_common")
    repo = _git_repo(tmp_path)
    hooks = tmp_path / "hooks"
    hooks.mkdir()
    _git(repo, "config", "core.hooksPath", str(hooks))
    hook = hooks / "pre-commit"
    hook.write_text(
        "#!/bin/sh\necho 'SECRETS FLOOR: rejected' 1>&2\nexit 1\n", encoding="utf-8"
    )
    os.chmod(str(hook), 0o755)
    (repo / "a.txt").write_text("hi\n", encoding="utf-8")
    _git(repo, "add", "-A")
    code, out = ac.git(repo, "commit", "-q", "-m", "should be rejected")
    assert code != 0
    assert "SECRETS FLOOR: rejected" in out  # the reason, not "" after the colon


def test_git_returns_text_on_stderr_only_fatal(tmp_path):
    # WI-233: a fatal that writes stderr only (rev-parse --verify on a missing
    # ref) must return non-empty text — the failure detail is no longer blank.
    ac = load_script("agent_common")
    repo = _git_repo(tmp_path)
    (repo / "a.txt").write_text("hi\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    code, out = ac.git(repo, "rev-parse", "--verify", "refs/heads/nope")
    assert code != 0
    assert out.strip()  # git's fatal message survives, not ""


def test_git_success_returns_stdout_only_unchanged(tmp_path):
    # WI-233: a SUCCESSFUL call that also chatters on stderr (a warning) returns
    # stdout alone, byte-identical to today — no stderr bleed on the success path.
    # A pre-commit hook warns on stderr yet exits 0, so the commit succeeds; the
    # returned text must be the commit's stdout summary, never the warning.
    ac = load_script("agent_common")
    repo = _git_repo(tmp_path)
    hooks = tmp_path / "hooks"
    hooks.mkdir()
    _git(repo, "config", "core.hooksPath", str(hooks))
    hook = hooks / "pre-commit"
    hook.write_text(
        "#!/bin/sh\necho 'WARN: noisy hook chatter' 1>&2\nexit 0\n", encoding="utf-8"
    )
    os.chmod(str(hook), 0o755)
    (repo / "a.txt").write_text("hi\n", encoding="utf-8")
    _git(repo, "add", "-A")
    code, out = ac.git(repo, "commit", "-m", "seed with a warning")
    assert code == 0
    assert "WARN" not in out  # stderr is NOT appended on the success path
    assert "seed with a warning" in out  # stdout summary preserved, unchanged


def test_substantive_dirty_drops_owner_scratchpad(tmp_path):
    # WI-203: OWNER_SCRATCHPAD.md is perpetually owner-edited, so the loop's
    # dirty-tree signal drops it — the raw primitive still counts it, but the
    # substantive view (used by the resume note + done detection) reads clean.
    loop = load_script("agent_loop")
    repo = tmp_path / "r"
    repo.mkdir()
    _git(repo, "init")
    pin_autocrlf(repo)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(repo, "config", "user.email", "a@b.com")
    _git(repo, "config", "user.name", "A")
    (repo / "OWNER_SCRATCHPAD.md").write_text("notes\n", encoding="utf-8")
    (repo / "a.txt").write_text("hi\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    # only the owner scratchpad is dirty -> raw sees it, substantive does not
    (repo / "OWNER_SCRATCHPAD.md").write_text("edited\n", encoding="utf-8")
    assert len(loop.working_tree_dirty(repo)) == 1  # the primitive stays honest
    assert loop.substantive_working_tree_dirty(repo) == []  # the loop reads clean
    # a real deliverable still counts; the scratchpad is still dropped
    (repo / "a.txt").write_text("changed\n", encoding="utf-8")
    sub = loop.substantive_working_tree_dirty(repo)
    assert len(sub) == 1 and "a.txt" in sub[0]
    assert len(loop.working_tree_dirty(repo)) == 2  # raw counts both


def test_owner_scratchpad_dirty_at_start_injects_nothing(loop_repo):
    # WI-203: an owner-only-dirty tree at loop start is NOT interrupted residue —
    # no WI-076 reconcile note, no dirty line logged (the prompt stays
    # byte-identical to the clean default), so the note fires only on real residue.
    repo, ctl, template = loop_repo
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    (repo / "OWNER_SCRATCHPAD.md").write_text("owner edit\n", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    prompt = (ctl / "prompt.txt").read_text(encoding="utf-8")
    assert "uncommitted changes" not in prompt  # no reconcile note injected
    assert prompt.startswith("You are an unattended worker") or "- WI: WI-201" in prompt
    assert "uncommitted path(s)" not in proc.stderr


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
            # No {prompt} placeholder: the H-4 guard (272a6e8) refuses
            # prompt-in-argv through a Windows batch shim, so the prompt rides
            # stdin instead (WI-216) — the shim still spawns via the
            # which-resolved CreateProcess path (WI-120's concern).
            'fakecli --control "{}" --model {{model}}'.format(ctl),
            "--pause",
            "0",
            "--model",
            "default-tier",
            "--wi",
            "WI-201",
            "--train",
            "t1",
        ],
        cwd=str(repo),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _invocations(ctl) == 1
    assert "worker t1 [WI-201]: DONE" in proc.stdout
    heads = [
        lg.read_text(encoding="utf-8")
        for lg in (repo / "docs" / "iteration").glob("t1-*.log")
    ]
    assert not any("# outcome: ERROR" in h for h in heads)


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
    assert "# outcome: COMMITTED" in log  # DONE is the worker exit banner
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
    # The telemetry commit is distinct from the session's own work commits.
    assert "progress" in subjects and "build WI-201" in subjects
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
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    proc = _loop(repo, template)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    log = sorted((repo / "docs" / "iteration").glob("t1-*.log"))[0].read_text(
        encoding="utf-8"
    )
    assert "# wi: WI-201" in log  # the assignment's WI is the session label


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
            "--wi",
            "WI-201",
            "--train",
            "t1",
            # deliberately NO --model / --model-map / AGENT_MODEL
        ],
        cwd=repo,
    )
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "no model is configured for this phase" in proc.stderr
    assert _invocations(ctl) == 0, "the guard fires before any session launches"


@pytest.mark.parametrize(
    "env_model,cli_model,expected",
    [
        (None, None, "declared-tier"),  # declared file wins over the built-in default
        ("env-tier", None, "env-tier"),  # AGENT_MODEL env beats the declared file
        ("env-tier", "cli-tier", "cli-tier"),  # an explicit --model beats both
    ],
)
def test_model_dial_precedence(loop_repo, monkeypatch, env_model, cli_model, expected):
    # IF-068 end-to-end through the real worker path (the fake agent records the
    # {model} it was handed): CLI flag > AGENT_MODEL env > docs/stack.ini
    # [agent-loop] model > built-in default. A fresh loop_repo per case keeps the
    # single build clean. `jobs`/`model-map` share the identical ladder in main().
    repo, ctl, template = loop_repo
    (repo / "docs" / "stack.ini").write_text(
        "[agent-loop]\nmodel = declared-tier\n", encoding="utf-8"
    )
    (ctl / "actions.txt").write_text("done", encoding="utf-8")
    monkeypatch.delenv("AGENT_MODEL", raising=False)
    monkeypatch.delenv("AGENT_MODEL_MAP", raising=False)
    if env_model is not None:
        monkeypatch.setenv("AGENT_MODEL", env_model)
    extra = ["--model", cli_model] if cli_model is not None else []
    proc = run_py(
        [
            SCRIPTS / "agent_loop.py",
            "--root",
            repo,
            "--agent-cmd",
            template,
            "--pause",
            "0",
            "--wi",
            "WI-201",
            "--train",
            "t1",
            *extra,
        ],
        cwd=repo,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (ctl / "models.txt").read_text(encoding="utf-8").split()[0] == expected


# --- the per-checkout coordinator lock (SR-027) --------------------------------
# Ported from the retired tracks suite (WI-210): the lock outlives the track
# lanes — the dispatcher, every worker, and an --interactive sitting take it.

# A probe that takes the lock in a SEPARATE process (the only way to observe the
# real cross-process kernel-lock contract). With `hard`, it dies without any
# release/atexit (os._exit) — modelling a crash so the caller can prove the OS
# auto-released the lock.
_LOCK_PROBE = """
import importlib.util, os, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location("agent_loop", sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
err = m.acquire_lock(Path(sys.argv[2]))
sys.stdout.write("REFUSED" if err else "ACQUIRED")
sys.stdout.flush()
if len(sys.argv) > 3 and sys.argv[3] == "hard":
    os._exit(0)
"""


def _probe_acquire(lock, hard_exit=False):
    argv = [
        sys.executable,
        "-c",
        _LOCK_PROBE,
        str(SCRIPTS / "agent_loop.py"),
        str(lock),
    ]
    if hard_exit:
        argv.append("hard")
    return subprocess.run(argv, capture_output=True, text=True).stdout.strip()


def test_lock_excludes_a_second_process(tmp_path):
    # The real contract: one coordinator per checkout. This process holds the
    # kernel lock; a separate process is refused, then succeeds once it's freed.
    agent_loop = load_script("agent_loop")
    lock = tmp_path / "out" / "agent-loop.lock"
    assert agent_loop.acquire_lock(lock) is None
    try:
        assert _probe_acquire(lock) == "REFUSED"
    finally:
        agent_loop.release_lock(lock)
    assert _probe_acquire(lock) == "ACQUIRED"


def test_lock_auto_released_when_holder_dies(tmp_path):
    # A holder that crashes without releasing must not wedge the next run —
    # the OS drops the advisory lock on process death. The probe acquires then
    # hard-exits (no release/atexit); this process must then acquire cleanly.
    agent_loop = load_script("agent_loop")
    lock = tmp_path / "out" / "agent-loop.lock"
    assert _probe_acquire(lock, hard_exit=True) == "ACQUIRED"
    assert agent_loop.acquire_lock(lock) is None
    agent_loop.release_lock(lock)


def test_lock_refuses_on_contention_errno(tmp_path, monkeypatch):
    # A genuine "held" errno (EWOULDBLOCK) must REFUSE — the guard is never
    # dropped on contention, and an unknown error stays a refusal too (fail-safe).
    import errno

    agent_loop = load_script("agent_loop")
    # The lock family lives in agent_common (WI-218 slice C): acquire_lock
    # resolves _take_os_lock in ITS namespace, so patch the instance
    # agent_loop actually imported (load_script would mint a fresh copy).
    agent_common = agent_loop.agent_common

    def _held(fd):
        raise OSError(errno.EWOULDBLOCK, "held")

    lock = tmp_path / "out" / "agent-loop.lock"
    monkeypatch.setattr(agent_common, "_take_os_lock", _held)
    err = agent_loop.acquire_lock(lock)
    assert err and "refusing to run two" in err


@pytest.mark.skipif(os.name == "nt", reason="advisory-lock degrade is POSIX-only")
def test_lock_degrades_on_unsupported_filesystem(tmp_path, monkeypatch, capsys):
    # A filesystem that cannot lock (ENOLCK) must DEGRADE — warn and proceed, not
    # fail closed on a legitimate run (Windows local FS always locks, so N/A there).
    import errno

    agent_loop = load_script("agent_loop")
    agent_common = agent_loop.agent_common  # the lock family's home (WI-218)

    def _unsupported(fd):
        raise OSError(errno.ENOLCK, "no locks available")

    lock = tmp_path / "out" / "agent-loop.lock"
    monkeypatch.setattr(agent_common, "_take_os_lock", _unsupported)
    assert agent_loop.acquire_lock(lock) is None  # proceeds, unguarded
    assert "without the one-coordinator" in capsys.readouterr().err.lower()
    agent_loop.release_lock(lock)


# --- repo-review 2026-07-21 regressions ---------------------------------------


def test_read_csv_rows_tolerates_a_bom(tmp_path):
    # M-23: an Excel-written BOM renamed the first header key to '﻿WI-ID',
    # so load_wi_registry returned {} while schedule.load_rows (utf-8-sig)
    # parsed fine — the dispatcher and the worker held two different views of
    # one registry, and a BOM'd system-requirements.csv silently vacated the
    # critique gate. The reader must strip the BOM and keep quoted multi-line
    # cells parseable. (The WI registry left CSV at Phase 5, so this reader now
    # serves the SR/TC registries — the regression it pins is the reader's, and
    # the original WI-shaped fixture is kept as the defect's own shape.)
    ac = load_script("agent_common")
    p = tmp_path / "work-items.csv"
    p.write_bytes(b'\xef\xbb\xbfWI-ID,Title,Status\nWI-001,"two\nline title",active\n')
    rows = ac._read_csv_rows(p)
    assert rows and rows[0].get("WI-ID") == "WI-001"  # not '﻿WI-ID'
    assert rows[0]["Title"] == "two\nline title"  # quoted newline survives


def test_session_log_redacts_credential_shapes(tmp_path):
    # M-19: session transcripts are committed to tracked history; well-known
    # credential shapes must not land there verbatim (a CLI auth error echoing
    # a key was permanent history with only push-policy in the way).
    ac = load_script("agent_common")
    transcript = (
        "auth failed: invalid x-api-key sk-ant-api03-{}\n"
        "also: Bearer {} and AKIA{} here\n"
        "normal line stays intact\n"
    ).format("A" * 30, "B" * 30, "BCDEFGHIJKLMNOPQ")
    meta = {"session": "007", "stamp": "test"}
    path = ac.write_session_log(tmp_path, meta, transcript)
    text = path.read_text(encoding="utf-8")
    assert "[REDACTED]" in text
    assert "sk-ant-api03" not in text
    assert "AKIA" + "BCDEFGHIJKLMNOPQ" not in text  # split so the floor stays clean
    assert "normal line stays intact" in text
    assert "# redacted: 3 credential-shaped token(s)" in text
