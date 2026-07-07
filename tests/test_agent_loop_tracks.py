"""Multi-track coordinator wiring — scripts/agent_loop.py --track
(process-options.md "Parallel tracks"). Ported from the field adoption that
generalized the layer; exercised the kit way — the real loop as a subprocess
against a tiny fake agent in throwaway git repos, plus the pure helpers direct.

The load-bearing guarantees a broken edit here would silently violate — each
the failure mode that would corrupt an unattended parallel run:

  - pure helpers: lane path resolution, track-slug validation (no traversal),
    non-signalling pid liveness, and the per-worktree lockfile (reclaim a dead
    pid, refuse a live one — the two-writer race guard);
  - the loop reads the TRACK LANE's run-state and writes the lane's iteration
    logs, not docs/ (a track must never read another lane's contract);
  - single-lane operation (no --track) still uses docs/, unchanged;
  - preflight refuses --track off its llm/<track> branch (wrong-lane guard).
"""

import os
import shutil
import subprocess
import sys

import pytest
from conftest import SCRIPTS, load_script, run_py

agent_loop = load_script("agent_loop")

needs_git = pytest.mark.skipif(not shutil.which("git"), reason="needs git on PATH")


# --- pure helpers (no subprocess) -------------------------------------------


def test_lane_dir_single_vs_track():
    from pathlib import Path

    docs = Path("docs")
    assert agent_loop.lane_dir(docs, None) == docs
    assert agent_loop.lane_dir(docs, "perception") == docs / "tracks" / "perception"


@pytest.mark.parametrize("good", ["perception", "hardware", "sw-pkg", "goals2"])
def test_sanitize_track_accepts_slugs(good):
    assert agent_loop.sanitize_track(good) == good


@pytest.mark.parametrize("bad", ["../x", "Perception", "x/y", "-x", "x y", ""])
def test_sanitize_track_rejects_traversal_and_junk(bad):
    with pytest.raises(ValueError):
        agent_loop.sanitize_track(bad)


def test_pid_alive_self_true_absurd_false():
    # Never signals: os.kill on Windows would kill; this must merely observe.
    assert agent_loop._pid_alive(os.getpid()) is True
    assert agent_loop._pid_alive(2_000_000_001) is False


def test_lockfile_reclaims_dead_refuses_live(tmp_path):
    lock = tmp_path / "out" / "agent-loop.lock"
    assert agent_loop.acquire_lock(lock) is None  # first take
    err = agent_loop.acquire_lock(lock)  # our own live pid still holds it
    assert err and "holds" in err
    agent_loop.release_lock(lock)
    assert not lock.exists()
    # a stale lock from a dead pid on this host is reclaimed, not honored
    lock.parent.mkdir(parents=True, exist_ok=True)
    lock.write_text("2000000002\n{}\n2020-01-01 00:00:00\n".format(agent_loop._host()))
    assert agent_loop.acquire_lock(lock) is None
    agent_loop.release_lock(lock)


# --- loop integration against a fake agent ----------------------------------

# The fake driver: one unit of work (a commit) so the loop sees progress, then
# it declares DONE by writing the run-state at the path it was handed — the
# lane's for a track run, docs/ for single-lane. It ignores model/prompt.
FAKE_AGENT = """
import argparse, json, pathlib, subprocess, time

ap = argparse.ArgumentParser()
ap.add_argument("--runstate", required=True)
ap.add_argument("--model", default="")
ap.add_argument("-p", "--prompt", default="")
args, extra = ap.parse_known_args()
pathlib.Path("work.txt").write_text(str(time.time()))
subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(["git", "commit", "-q", "-m", "fake work"], check=True)
rs = pathlib.Path(args.runstate)
rs.parent.mkdir(parents=True, exist_ok=True)
rs.write_text("DONE\\n")
print(json.dumps({"is_error": False, "result": "ok"}))
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


def _make_repo(tmp_path, branch=None):
    """A throwaway git repo (one commit) + the fake agent script. Returns
    (repo, fake_agent_path)."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    (repo / "seed.txt").write_text("seed", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seed")
    if branch:
        _git(repo, "checkout", "-q", "-b", branch)
    fake = tmp_path / "fake_agent.py"
    fake.write_text(FAKE_AGENT, encoding="utf-8")
    return repo, fake


def _loop(repo, fake, runstate, *extra):
    template = '"{}" "{}" --runstate "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, runstate
    )
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
            "test",
            "--max-iterations",
            "2",
            *extra,
        ],
        cwd=repo,
    )


@needs_git
def test_track_run_uses_lane_not_docs(tmp_path):
    # --track perception: the loop reads docs/tracks/perception/run-state and
    # writes the lane's iteration logs — never docs/ (lane isolation).
    repo, fake = _make_repo(tmp_path, branch="llm/perception")
    lane = repo / "docs" / "tracks" / "perception"
    proc = _loop(repo, fake, lane / "run-state", "--track", "perception")

    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    assert (lane / "run-state").read_text().strip() == "DONE"
    assert list((lane / "iteration").glob("001-*.log")), "lane session log missing"
    assert (lane / "iteration_index.md").exists()
    assert not (repo / "docs" / "iteration").exists(), "wrote docs/ not the lane"


@needs_git
def test_single_lane_uses_docs(tmp_path):
    # No --track: unchanged behavior — docs/run-state and docs/iteration, and
    # no docs/tracks/ lane is created.
    repo, fake = _make_repo(tmp_path)  # stays on the default branch
    proc = _loop(repo, fake, repo / "docs" / "run-state")

    assert proc.returncode == agent_loop.EXIT_DONE, proc.stdout + proc.stderr
    assert (repo / "docs" / "run-state").read_text().strip() == "DONE"
    assert list((repo / "docs" / "iteration").glob("001-*.log"))
    assert not (repo / "docs" / "tracks").exists()


@needs_git
def test_track_off_its_branch_is_preflight_failure(tmp_path):
    # A track must run on its own llm/<track> branch — the wrong-lane guard
    # fails before any session (llm/hardware is the wrong lane for perception).
    repo, fake = _make_repo(tmp_path, branch="llm/hardware")
    lane = repo / "docs" / "tracks" / "perception"
    proc = _loop(repo, fake, lane / "run-state", "--track", "perception")

    assert proc.returncode == agent_loop.EXIT_PREFLIGHT, proc.stdout + proc.stderr
    assert "must run on its own branch" in (proc.stdout + proc.stderr)
    assert not lane.exists(), "a rejected track must not create its lane"
