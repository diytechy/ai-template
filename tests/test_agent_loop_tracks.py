"""Multi-track coordinator wiring — scripts/agent_loop.py --track
(process-options.md "Parallel tracks"). Ported from the field adoption that
generalized the layer; exercised the kit way — the real loop as a subprocess
against a tiny fake agent in throwaway git repos, plus the pure helpers direct.

The load-bearing guarantees a broken edit here would silently violate — each
the failure mode that would corrupt an unattended parallel run:

  - pure helpers: lane path resolution, track-slug validation (no traversal),
    and the per-worktree kernel lock (excludes a second process; auto-released
    when the holder dies, so a crash never wedges the next run);
  - the loop reads the TRACK LANE's run-state and writes the lane's iteration
    logs, not docs/ (a track must never read another lane's contract);
  - single-lane operation (no --track) still uses docs/, unchanged;
  - preflight refuses --track off its llm/<track> branch, and fails closed on a
    detached HEAD (an unverifiable branch — the wrong-lane guard).
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
    lock = tmp_path / "out" / "agent-loop.lock"
    assert agent_loop.acquire_lock(lock) is None
    try:
        assert _probe_acquire(lock) == "REFUSED"
    finally:
        agent_loop.release_lock(lock)
    assert _probe_acquire(lock) == "ACQUIRED"


def test_lock_auto_released_when_holder_dies(tmp_path):
    # M4: a holder that crashes without releasing must not wedge the next run —
    # the OS drops the advisory lock on process death. The probe acquires then
    # hard-exits (no release/atexit); this process must then acquire cleanly.
    lock = tmp_path / "out" / "agent-loop.lock"
    assert _probe_acquire(lock, hard_exit=True) == "ACQUIRED"
    assert agent_loop.acquire_lock(lock) is None
    agent_loop.release_lock(lock)


def test_lock_refuses_on_contention_errno(tmp_path, monkeypatch):
    # A genuine "held" errno (EWOULDBLOCK) must REFUSE — the guard is never
    # dropped on contention, and an unknown error stays a refusal too (fail-safe).
    import errno

    def _held(fd):
        raise OSError(errno.EWOULDBLOCK, "held")

    lock = tmp_path / "out" / "agent-loop.lock"
    monkeypatch.setattr(agent_loop, "_take_os_lock", _held)
    err = agent_loop.acquire_lock(lock)
    assert err and "refusing to run two" in err


@pytest.mark.skipif(os.name == "nt", reason="advisory-lock degrade is POSIX-only")
def test_lock_degrades_on_unsupported_filesystem(tmp_path, monkeypatch, capsys):
    # A filesystem that cannot lock (ENOLCK) must DEGRADE — warn and proceed, not
    # fail closed on a legitimate run (Windows local FS always locks, so N/A there).
    import errno

    def _unsupported(fd):
        raise OSError(errno.ENOLCK, "no locks available")

    lock = tmp_path / "out" / "agent-loop.lock"
    monkeypatch.setattr(agent_loop, "_take_os_lock", _unsupported)
    assert agent_loop.acquire_lock(lock) is None  # proceeds, unguarded
    assert "without the one-coordinator" in capsys.readouterr().err.lower()
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


@needs_git
def test_track_on_detached_head_fails_closed(tmp_path):
    # M3: `git branch --show-current` is empty on a detached HEAD. The branch
    # guard must FAIL CLOSED (it cannot confirm the lane) rather than fall
    # through and let a track write from an unverifiable checkout.
    repo, fake = _make_repo(tmp_path, branch="llm/perception")
    _git(repo, "checkout", "-q", "--detach", "HEAD")
    lane = repo / "docs" / "tracks" / "perception"
    proc = _loop(repo, fake, lane / "run-state", "--track", "perception")

    assert proc.returncode == agent_loop.EXIT_PREFLIGHT, proc.stdout + proc.stderr
    assert "could not be determined" in (proc.stdout + proc.stderr)
    assert not lane.exists(), "a rejected track must not create its lane"
    assert not lane.exists(), "a rejected track must not create its lane"
