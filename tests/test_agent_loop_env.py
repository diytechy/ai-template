"""Per-pair Env merge into the managed session launch (WI-069, the pair-row
registry). A registry row's `Env` (KEY=value;...) is merged over the inherited
environment at launch — the declarative selector for a router/second-account/API
key; an EMPTY Env inherits the ambient environment exactly (today's call).
Exercised end-to-end against a fake agent that records what it saw in os.environ,
so no test touches a real CLI."""

import csv
import subprocess
import sys

from conftest import SCRIPTS, run_py

# The fake agent: record the value of AGENT_TEST_ENV_MARKER it was launched with
# (or a sentinel when absent), commit one build, then write DONE to terminate.
FAKE = r"""
import argparse, os, pathlib, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument("--control", required=True)
ap.add_argument("--model", default="")
ap.add_argument("-p", "--prompt", default="")
args, _ = ap.parse_known_args()
ctl = pathlib.Path(args.control)
with open(str(ctl / "env-seen.txt"), "a", encoding="utf-8") as fh:
    fh.write(os.environ.get("AGENT_TEST_ENV_MARKER", "<ABSENT>") + "\n")
pathlib.Path("work.txt").write_text("built", encoding="utf-8")
subprocess.run(["git", "add", "work.txt"], check=True)
subprocess.run(["git", "commit", "-q", "-m", "WI-000: build"], check=True)
pathlib.Path("docs/run-state").write_text("DONE", encoding="utf-8")
sys.exit(0)
"""

STATUS_MD = "# Status\n\n## Current State\n\n- nothing pending\n"


def _git(repo, *args):
    p = subprocess.run(
        ["git", "-C", str(repo)] + list(args),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    assert p.returncode == 0, p.stdout + p.stderr
    return p.stdout.strip()


def _make_repo(tmp_path, env_cell):
    """A managed repo whose single enabled BUILD row carries `env_cell` as its
    Env column. review-policy 0 so only the build session runs."""
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "docs" / "status.md").write_text(STATUS_MD, encoding="utf-8")
    (repo / "docs" / "run-phase").write_text("BUILD\n", encoding="utf-8")
    (repo / "docs" / "review-policy").write_text("0\n", encoding="utf-8")
    _git(repo, "init")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "initial")

    ctl = tmp_path / "control"
    ctl.mkdir()
    fake = tmp_path / "fake.py"
    fake.write_text(FAKE, encoding="utf-8")
    cmd = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )
    rows = [
        ["Id", "Family", "Model", "Version", "Tier", "CmdTemplate", "Env", "Notes"],
        ["PROVA-BUILD-1", "PROVA", "builda", "1", "medium", cmd, env_cell, ""],
    ]
    with open(
        str(repo / "docs" / "agents.csv"), "w", encoding="utf-8", newline=""
    ) as fh:
        csv.writer(fh).writerows(rows)
    (repo / "docs" / "agents-enabled").write_text("PROVA-BUILD-1\n", encoding="utf-8")
    return repo, ctl, cmd


def _loop(repo, cmd):
    return run_py(
        [
            SCRIPTS / "agent_loop.py",
            "--root",
            repo,
            "--agent-cmd",
            cmd,
            "--pause",
            "0",
            "--model",
            "default-tier",
            "--max-iterations",
            "4",
        ],
        cwd=repo,
    )


def _seen(ctl):
    p = ctl / "env-seen.txt"
    return p.read_text(encoding="utf-8").split() if p.exists() else []


def test_pair_row_env_is_merged_into_the_launch(tmp_path):
    # A declared Env reaches the launched session.
    repo, ctl, cmd = _make_repo(tmp_path, "AGENT_TEST_ENV_MARKER=hello")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _seen(ctl) == ["hello"]


def test_empty_env_inherits_the_ambient_environment(tmp_path):
    # No Env column value -> the session inherits the ambient environment exactly
    # (session_env stays None; the marker is not injected). This is today's call.
    repo, ctl, cmd = _make_repo(tmp_path, "")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _seen(ctl) == ["<ABSENT>"]
