"""drive.py — the serial claim->build->integrate driver (WI-374).

The drive loop is COMPOSITION: schedule.py's frontier picks, integrate.py
claims and merges, agent_loop.py's worker role builds. What this module pins
is the loop's own contract — the joints, not the parts (each part's own suite
already pins it):

  * an unwired agent command refuses BEFORE anything is claimed;
  * an empty frontier drains the queue and exits 0 — success, not an error;
  * a refusing claim rung stops the run loudly (never skipped);
  * the tracked pause appearing MID-RUN stops the next cycle (exit 8);
  * a worker that reports DONE without finishing its branch trips the drive
    loop's own stall guard (the trunk-unmoved counter);
  * NEEDS-HUMAN (7) and other worker failures propagate, with the claim left
    parked so a relaunch resumes it;
  * end-to-end on a REAL scaffold: claim -> injected worker close -> the REAL
    composed-tree bar -> merge -> drained banner; and the same flow with a
    breaking change stops on the RED bar with the branch still parked.

The worker seam is injected in every test (`run(root, args, worker=...)`) —
the real subprocess launch of agent_loop.py --wi is agent_loop's own tested
surface — but integrate.py and the bar are REAL: a stubbed bar here would be
exactly the vacuous green the integrator exists to make impossible. Git
fixtures are real repositories for the same reason as tests/test_integrate.py
(the queue derives everything from history), and the helper shapes are copied
from that module per this suite's no-cross-test-import idiom.
"""

import argparse
import os
import subprocess

from conftest import (
    SCRIPTS,
    env_gate_skipif,
    load_script,
    make_minimal_project,
    run_py,
    skip_without_env_gates,
)

pytestmark = env_gate_skipif("git")

drv = load_script("drive")

T_BASE = 1_000_000
T_CODE = 1_000_100
T_LATER = 1_000_200


def _git(root, *args, env=None):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _commit(root, message, when=None):
    env = dict(os.environ)
    if when is not None:
        stamp = "@{} +0000".format(when)
        env["GIT_AUTHOR_DATE"] = stamp
        env["GIT_COMMITTER_DATE"] = stamp
    _git(root, "add", "-A", env=env)
    _git(root, "commit", "-qm", message, env=env)


def git_repo(root, branch="main"):
    skip_without_env_gates("git")
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "symbolic-ref", "HEAD", "refs/heads/" + branch)
    (root / "seed.txt").write_text("seed\n", encoding="utf-8", newline="\n")
    # out/ holds integrate.py's lock file, which persists between drains; an
    # unignored one reads as dirt at the NEXT cycle's clean-trunk check (the
    # same stock-scaffold finding tests/test_integrate.py records).
    (root / ".gitignore").write_text("out/\n", encoding="utf-8", newline="\n")
    _commit(root, "seed", when=T_BASE)
    return root


def spec_text(wid, safety="ordinary", specref=None, deliverable="A widget, shipped."):
    lines = [
        'id = "{}"'.format(wid),
        'title = "Widget"',
        'workstream = "ws"',
        'sr_refs = ["SR-001"]',
        "needs = []",
        'safety_class = "{}"'.format(safety),
        "order = 0",
    ]
    if specref:
        lines.append('specref = "{}"'.format(specref))
    text = "+++\n" + "".join(ln + "\n" for ln in lines) + "+++\n"
    if deliverable:
        text += "\n## Deliverable\n\n" + deliverable + "\n"
    return text


def write_spec(root, where, wid, slug="widget", **kw):
    path = root / "docs" / "work" / where / "{}-{}.md".format(wid, slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(spec_text(wid, **kw), encoding="utf-8", newline="\n")
    return path


def drive_args(**kw):
    """The argparse surface drive.run reads, with per-test overrides."""
    ns = argparse.Namespace(
        agent_cmd="stub-agent",
        session_timeout=0,
        no_session_echo=False,
        live_status=False,
        max_iterations=10,
        stall_limit=3,
        model="",
        model_map="",
        cmd_map="",
        prompt_map="",
        tier_map="",
        prefer_map="",
        wait_on_limit=0,
        limit_retry_fallback=3600,
    )
    for k, v in kw.items():
        setattr(ns, k, v)
    return ns


def parked_repo(tmp_path, wid="WI-401", branch="wi-401"):
    """An interrupted run's state: the trunk holds active/<branch>/<spec> and
    the branch exists with that same tree (unfinished — the spec never moved
    to complete/), which is exactly what _parked_branches must resume."""
    root = git_repo(tmp_path)
    write_spec(root, "active/" + branch, wid, specref="seed.txt")
    _commit(root, "claim: {} -> active/{}".format(wid, branch), when=T_CODE)
    _git(root, "branch", branch)
    return root


class Recorder:
    """A worker stand-in that records calls and plays scripted exit codes."""

    def __init__(self, outcomes=(0,), effect=None):
        self.calls = []
        self.outcomes = list(outcomes)
        self.effect = effect

    def __call__(self, root, branch, wi_ids, args):
        self.calls.append((branch, tuple(wi_ids)))
        if self.effect is not None:
            self.effect(root, branch, wi_ids)
        return self.outcomes.pop(0) if self.outcomes else 0


# --- preflight and the empty frontier -----------------------------------------


def test_drive_refuses_an_unwired_agent_command_before_claiming(
    tmp_path, capsys, monkeypatch
):
    # The claim is a trunk commit; a run that would claim first and then
    # discover no worker can launch leaves a parked branch behind for nothing.
    monkeypatch.delenv("AGENT_CMD", raising=False)
    root = git_repo(tmp_path)
    write_spec(root, "queued", "WI-401", specref="seed.txt")
    _commit(root, "file WI-401", when=T_CODE)

    rc = drv.run(root, drive_args(agent_cmd=None), worker=None)
    assert rc == 2
    assert "no agent command wired" in capsys.readouterr().err
    assert (root / "docs" / "work" / "queued" / "WI-401-widget.md").is_file()
    assert "wi-401-widget" not in _git(root, "branch", "--format=%(refname:short)")


def test_drive_unwired_config_still_drains_an_empty_queue_to_zero(
    tmp_path, capsys, monkeypatch
):
    # The config preflight is applied only when work needs a worker: an inert
    # scaffold (empty AGENT_CMD, no enable-list) with an EMPTY queue is a
    # successful drain, not a config error — the spec's empty-frontier
    # contract wins (codex cross-review, round 1).
    monkeypatch.delenv("AGENT_CMD", raising=False)
    root = git_repo(tmp_path)

    rc = drv.run(root, drive_args(agent_cmd=None), worker=None)
    assert rc == 0
    assert "queue drained" in capsys.readouterr().out


def test_drive_refuses_a_stranded_claim_rather_than_draining(tmp_path, capsys):
    # A half-completed claim — active/<branch>/ holds specs but the branch
    # ref is gone — is invisible to both the frontier (status=active) and the
    # parked-resume read (no ref). The run must fail closed naming it, never
    # report the queue drained over work nobody can reach.
    root = git_repo(tmp_path)
    write_spec(root, "active/wi-401", "WI-401", specref="seed.txt")
    _commit(root, "claim: WI-401 -> active/wi-401 (branch cut lost)", when=T_CODE)
    worker = Recorder()

    rc = drv.run(root, drive_args(), worker=worker)
    assert rc == 2
    err = capsys.readouterr().err
    assert "NO branch ref" in err and "wi-401" in err
    assert worker.calls == []


def test_drive_refuses_a_dirty_trunk_before_resuming(tmp_path, capsys):
    # The claim rung's clean-trunk refusal, hoisted to the cycle top: the
    # parked-resume path must meet it too, BEFORE a worker session runs.
    root = parked_repo(tmp_path)
    (root / "scratch.txt").write_text("uncommitted\n", encoding="utf-8")
    worker = Recorder()

    rc = drv.run(root, drive_args(), worker=worker)
    assert rc == 2
    assert "working tree is dirty" in capsys.readouterr().err
    assert worker.calls == []


def test_drive_empty_frontier_drains_and_exits_zero(tmp_path, capsys):
    # A finished queue is SUCCESS: the drained banner at exit 0 (the done-when
    # names this outcome explicitly — an empty frontier is not an error).
    root = git_repo(tmp_path)
    worker = Recorder()

    rc = drv.run(root, drive_args(), worker=worker)
    assert rc == 0
    out = capsys.readouterr().out
    assert "queue drained" in out and "0 WI(s) integrated" in out
    assert worker.calls == []


# --- the composed refusals stop the run ---------------------------------------


def test_drive_claim_refusal_stops_the_run(tmp_path, capsys):
    # The SpecRef rung (WI-370) fires inside integrate.claim; the driver must
    # surface it and STOP — never skip to the next WI, never talk past it.
    root = git_repo(tmp_path)
    write_spec(root, "queued", "WI-401", specref=None)
    _commit(root, "file WI-401", when=T_CODE)
    worker = Recorder()

    rc = drv.run(root, drive_args(), worker=worker)
    assert rc == 1
    assert "carries no SpecRef" in capsys.readouterr().err
    assert worker.calls == []
    assert (root / "docs" / "work" / "queued" / "WI-401-widget.md").is_file()


def test_drive_pause_appearing_mid_run_stops_the_next_cycle(tmp_path, capsys):
    # §5.6: pause = stop claiming. The check sits at the top of EVERY cycle,
    # so a pause dropped while a worker ran stops the next claim — with the
    # pause banner (exit 8), not a claim-rung refusal.
    root = parked_repo(tmp_path)

    def drop_pause(r, branch, wi_ids):
        (r / "docs" / "work" / "pause").write_text(
            'reason = "owner says stop"\nsince = "2026-07-31"\n',
            encoding="utf-8",
            newline="\n",
        )
        _commit(r, "pause: owner says stop", when=T_LATER)

    worker = Recorder(outcomes=(0,), effect=drop_pause)
    rc = drv.run(root, drive_args(), worker=worker)
    assert rc == 8
    err = capsys.readouterr().err
    assert "PAUSED" in err and "owner says stop" in err
    assert len(worker.calls) == 1


def test_drive_resumes_a_parked_branch_and_stalls_on_no_progress(tmp_path, capsys):
    # A parked claim from an interrupted run is picked up FIRST (resume, not
    # refuse) — and a worker that keeps reporting DONE without finishing its
    # branch cannot loop forever: the trunk never moves, so the drive loop's
    # own stall guard aborts (exit 4).
    root = parked_repo(tmp_path)
    worker = Recorder(outcomes=(0, 0))

    rc = drv.run(root, drive_args(stall_limit=2), worker=worker)
    assert rc == 4
    assert "STALL" in capsys.readouterr().err
    assert worker.calls == [("wi-401", ("WI-401",)), ("wi-401", ("WI-401",))]


def test_drive_propagates_needs_human_and_leaves_the_claim_parked(tmp_path, capsys):
    root = parked_repo(tmp_path)
    worker = Recorder(outcomes=(7,))

    rc = drv.run(root, drive_args(), worker=worker)
    assert rc == 7
    assert "NEEDS-HUMAN" in capsys.readouterr().err
    # The claim survives for the relaunch to resume.
    assert (root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md").is_file()
    assert "wi-401" in _git(root, "branch", "--format=%(refname:short)")


def test_drive_stops_on_a_failing_worker_with_the_claim_parked(tmp_path, capsys):
    root = parked_repo(tmp_path)
    worker = Recorder(outcomes=(3,))

    rc = drv.run(root, drive_args(), worker=worker)
    assert rc == 3
    assert "stays parked" in capsys.readouterr().err
    assert len(worker.calls) == 1


# --- end to end against the REAL bar ------------------------------------------

E2E_GOOD_SRC = '''"""Demo module. Implements: SR-001"""


def add(a, b):
    """Add two numbers. Implements: SR-001, LLR-001"""
    return a + b
'''

E2E_BAD_SRC = '''"""Demo module. Implements: SR-001"""


def add(a, b):
    """Add two numbers. Implements: SR-001, LLR-001"""
    return a - b
'''


def scaffold_with_queued_wi(tmp_path):
    """A bootstrapped, G3-complete scaffold with WI-401 queued — the state a
    plain launch starts from. Mirrors test_integrate.scaffolded_closed_branch
    (fixture notes there), except the WI is still QUEUED: claiming it is the
    driver's job under test."""
    skip_without_env_gates("git")
    repo = tmp_path / "repo"
    repo.mkdir()
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", repo], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    make_minimal_project(repo)
    (repo / "docs" / "review-policy").write_text("0\n", encoding="utf-8", newline="\n")
    with (repo / ".gitignore").open("a", encoding="utf-8", newline="\n") as fh:
        fh.write("out/\n")
    write_spec(repo, "queued", "WI-401", specref="docs/log.md")
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    _git(repo, "config", "commit.gpgsign", "false")
    _commit(repo, "seed: the scaffolded project", when=T_BASE)
    return repo


def closing_worker(src_text):
    """The injected worker: does what a real worker session's committed
    evidence amounts to — one product commit + the closing move to complete/
    (SpecRef cleared per R-F) on the claimed branch, via its own worktree."""

    def worker(root, branch, wi_ids, args):
        wt = root.parent / ("wt-" + branch)
        _git(root, "worktree", "add", str(wt), branch)
        (wt / "src" / "demo.py").write_text(src_text, encoding="utf-8", newline="\n")
        spec = wt / "docs" / "work" / "active" / branch / "WI-401-widget.md"
        dst = wt / "docs" / "work" / "complete" / "WI-401-widget.md"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(
            spec.read_text(encoding="utf-8").replace('specref = "docs/log.md"\n', ""),
            encoding="utf-8",
            newline="\n",
        )
        _git(wt, "rm", "-q", "docs/work/active/{}/WI-401-widget.md".format(branch))
        _commit(wt, "WI-401: build + close", when=T_CODE)
        return 0

    return worker


def test_drive_end_to_end_claims_builds_merges_and_drains(tmp_path):
    repo = scaffold_with_queued_wi(tmp_path)

    rc = drv.run(repo, drive_args(), worker=closing_worker(E2E_GOOD_SRC), tier="smoke")
    assert rc == 0

    # The claim happened, the merge landed, the branch unloaded, the worker
    # worktree GC'd, and the drained banner counted the one integration.
    assert (repo / "docs" / "work" / "complete" / "WI-401-widget.md").is_file()
    # git tracks files, not directories: the emptied active/<branch>/ dir may
    # linger on disk — what must be gone is any claimed SPEC.
    assert not list((repo / "docs" / "work" / "active").rglob("WI-*.md"))
    branches = _git(repo, "branch", "--format=%(refname:short)")
    assert "wi-401-widget" not in branches
    assert not (repo.parent / "wt-wi-401-widget").exists()


def test_drive_stops_on_a_red_composed_tree_bar(tmp_path, capsys):
    # The worker's "close" breaks the product test: the REAL bar on the
    # composed tree goes red, integrate parks the candidate, and the driver
    # STOPS with the branch still claimed — nothing merged, nothing skipped.
    repo = scaffold_with_queued_wi(tmp_path)

    rc = drv.run(repo, drive_args(), worker=closing_worker(E2E_BAD_SRC), tier="smoke")
    assert rc == 1
    err = capsys.readouterr().err
    assert "bar is RED" in err
    assert "wi-401-widget" in _git(repo, "branch", "--format=%(refname:short)")
    assert not (repo / "docs" / "work" / "complete" / "WI-401-widget.md").exists()


# --- the plain-launch seam (IF-015) -------------------------------------------


def test_plain_agent_loop_launch_enters_the_drive_mode(tmp_path, monkeypatch):
    # IF-015 v3: a plain launch (no role flag) DRIVES instead of refusing with
    # the map. On an empty registry that is the drained banner at exit 0 —
    # run as a real subprocess through agent_loop.py, the launcher's own path.
    root = git_repo(tmp_path)
    monkeypatch.setenv("AGENT_CMD", "stub-agent")
    proc = run_py([SCRIPTS / "agent_loop.py", "--root", str(root)], cwd=root)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "queue drained" in out
    assert "no role given" not in out
