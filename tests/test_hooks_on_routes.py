"""Every agent route refuses to start in a checkout whose commit hooks are not
on (`kitlib.commit_hooks`), before any work: no lock, no branch, no commit, no
session.

Each refusal case builds its repository the way the route's own tests do, then
turns the hooks off (`git config --unset core.hooksPath`), and asserts the
refusal names the setup command and that nothing moved. The census of which
entries call the check first is `tests/test_hooks_on_census.py`.
"""

import subprocess
import sys

import pytest
from conftest import SCRIPTS, hooks_on, load_script, pin_autocrlf, run_py
from integrate_fixtures import (
    _commit,
    _git,
    _rev,
    claim_repo,
    git_repo,
    integ,
)
from overnight_legs_fixtures import handoff_repo, load_launcher
from test_integrate_station import _lane, _order, attest_repo, station_repo

svc = load_script("session_service")
guard = load_script("coordinator_guard")

SETUP = "scripts/setup.sh"


def hooks_off(root):
    subprocess.run(
        ["git", "-C", str(root), "config", "--unset", "core.hooksPath"],
        capture_output=True,
    )
    return root


def hookless_repo(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    return hooks_off(git_repo(root))


def _branches(root):
    return sorted(_git(root, "branch", "--format=%(refname:short)").split())


# --- the loop's launch -------------------------------------------------------

MARKER_AGENT = """
import pathlib, sys
pathlib.Path(sys.argv[1]).write_text("ran", encoding="utf-8")
"""


def test_the_loop_refuses_a_hookless_checkout(tmp_path):
    root = hookless_repo(tmp_path)
    (root / "docs").mkdir(exist_ok=True)
    (root / "docs" / "status.md").write_text("# Status\n", encoding="utf-8")
    (root / ".gitignore").write_text("out/\n", encoding="utf-8")
    _commit(root, "status")
    agent = tmp_path / "agent.py"
    agent.write_text(MARKER_AGENT, encoding="utf-8")
    marker = tmp_path / "marker.txt"
    template = '"{}" "{}" "{}"'.format(sys.executable, agent, marker)
    head, branches = _rev(root, "HEAD"), _branches(root)
    proc = run_py(
        [SCRIPTS / "agent_loop.py", "--root", root, "--agent-cmd", template],
        cwd=root,
    )
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert SETUP in proc.stderr, proc.stdout + proc.stderr
    assert not (root / "out" / "agent-loop.lock").exists()
    assert (_rev(root, "HEAD"), _branches(root)) == (head, branches)
    assert not marker.exists()


# --- the session service's launch ----------------------------------------------


def _ran():
    calls = []

    def run(argv, root, timeout, **kw):
        calls.append(argv)
        return 0, '{"type":"result","result":"ok"}', False

    return calls, run


def test_act_refuses_a_hookless_checkout(tmp_path, monkeypatch):
    root = hookless_repo(tmp_path)
    released, written = [], []
    monkeypatch.setattr(
        svc.session_keep, "keep_release", lambda r, k: released.append(k)
    )
    monkeypatch.setattr(svc, "record", lambda *a, **k: written.append(a))
    calls, run = _ran()
    kept = object()
    call = svc.Call(
        root=root, role="BUILD", template="claude -p", model="m", runner=run, keep=kept
    )
    with pytest.raises(svc.HooksOffRefused, match="scripts/setup.sh"):
        svc.call(call)
    assert calls == [] and written == []
    assert released == [kept]


def test_act_runs_as_today_with_hooks_on(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    git_repo(root)
    calls, run = _ran()
    call = svc.Call(
        root=root, role="BUILD", template="claude -p", model="m", runner=run
    )
    assert svc.act(call).code == 0 and len(calls) == 1


def test_through_blackout_does_not_wait_out_a_hooks_refusal(tmp_path):
    root = hookless_repo(tmp_path)
    slept = []
    calls, run = _ran()
    call = svc.Call(
        root=root, role="BUILD", template="claude -p", model="m", runner=run
    )
    assert not issubclass(svc.HooksOffRefused, svc.BlackoutRefused)
    with pytest.raises(svc.HooksOffRefused):
        svc.through_blackout(
            lambda: svc.act(call), emit=lambda line: None, sleep=slept.append
        )
    assert slept == [] and calls == []


# --- the trunk writers -----------------------------------------------------------


def test_bookkeeping_commit_refuses_a_hookless_checkout(tmp_path):
    root = hookless_repo(tmp_path)
    head = _rev(root, "HEAD")
    wrote = []

    def write(scratch):
        wrote.append(scratch)
        (scratch / "note.txt").write_text("x\n", encoding="utf-8")

    sha, refusal = integ.bookkeeping.commit(
        root, ["note.txt"], write, "note", label="the probe"
    )
    assert sha is None
    assert refusal.startswith("the probe cannot start: ") and SETUP in refusal
    assert wrote == [] and _rev(root, "HEAD") == head


def _claim_state(root):
    return (
        _rev(root, "HEAD"),
        _branches(root),
        sorted(p.name for p in (root / "docs" / "work" / "queued").iterdir()),
        (root / "out" / "agent-loop.lock").exists(),
    )


def test_claim_refuses_a_hookless_checkout_first(tmp_path, capsys):
    root = hooks_off(claim_repo(tmp_path))
    before = _claim_state(root)
    assert integ.claim(root, "WI-401", "wi-401") == 1
    assert SETUP in capsys.readouterr().err
    assert _claim_state(root) == before
    assert "wi-401" not in before[1] and before[3] is False


def test_the_hooks_refusal_comes_before_the_coordinator_guards(tmp_path, capsys):
    # A checkout the context guard also refuses (the guard on, no lease held):
    # with the hooks on the guard's refusal is what the claim says, and with
    # them off the hooks refusal is, because it is the first rung.
    root = claim_repo(tmp_path)
    (root / "docs" / "process.toml").write_text(
        "[coordinator]\ncontext_guard_pct = 50\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "the guard on")
    assert integ.claim(root, "WI-401", "wi-401") == 1
    guarded = capsys.readouterr().err
    assert guarded and SETUP not in guarded
    hooks_off(root)
    assert integ.claim(root, "WI-401", "wi-401") == 1
    assert SETUP in capsys.readouterr().err


def test_refresh_refuses_a_hookless_checkout(tmp_path):
    # The station fixture declares a product bar and a green stub harness, so
    # with the hooks on this refresh runs its bar and commits; with them off it
    # refuses before the lane is touched.
    root = station_repo(tmp_path)
    tip = _rev(root, "wi-401")
    hooks_off(root)
    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert sha is None, "the refresh ran and committed {}".format(sha)
    assert refusal.startswith("refresh REFUSED for wi-401 - ") and SETUP in refusal
    assert _rev(root, "wi-401") == tip
    assert _order(_lane(root, "wi-401")) == []


def test_attest_refuses_a_hookless_checkout(tmp_path):
    # The attest fixture declares the review bar and a green stub harness, so
    # with the hooks on this attest runs its bar and commits the staged file;
    # with them off it refuses before the bar, leaving branch and index.
    root = attest_repo(tmp_path)
    wt = _lane(root, "wi-401")
    (wt / "staged.txt").write_text("staged\n", encoding="utf-8", newline="\n")
    _git(wt, "add", "staged.txt")
    tip, index = _rev(root, "wi-401"), _git(wt, "write-tree").strip()
    hooks_off(root)
    sha, refusal = integ.attest(root, "wi-401", "review", ["tests/test_widget.py"])
    assert sha is None, "the attest ran and committed {}".format(sha)
    assert refusal and SETUP in refusal, refusal
    assert _rev(root, "wi-401") == tip
    assert _git(wt, "write-tree").strip() == index
    assert _order(wt) == []


def test_merge_slot_refuses_a_hookless_checkout(tmp_path, capsys):
    # The same declared bar lets the slot refresh and merge this branch with
    # the hooks on; with them off it takes no lock and trunk does not move.
    root = station_repo(tmp_path)
    assert "wi-401" in integ.finished_branches(root)
    head = _rev(root, "HEAD")
    hooks_off(root)
    assert integ.integrate(root, "smoke") == 1
    assert SETUP in capsys.readouterr().err
    assert not (root / "out" / "integrate.lock").exists()
    assert _rev(root, "HEAD") == head
    assert "wi-401" in _branches(root)
    assert _order(_lane(root, "wi-401")) == []


# --- the lease's take and the headless legs ------------------------------------

COORD = "c0c0c0c0-0000-4000-8000-0000000000b1"


def test_take_refuses_a_hookless_checkout_and_records_no_holder(tmp_path):
    root = hookless_repo(tmp_path)
    refusal = guard.take(root, COORD)
    assert refusal and SETUP in refusal
    directory = guard.lease_dir(root)
    assert guard._load(directory) == {}
    assert not (directory / "events.jsonl").exists()


@pytest.fixture
def legs(tmp_path, monkeypatch):
    monkeypatch.setattr(sys, "path", list(sys.path))
    module = load_launcher()
    monkeypatch.setattr(module, "LOGDIR", tmp_path / "overnight-logs")
    monkeypatch.setattr(module, "lease_holder", lambda repo: None)
    monkeypatch.setattr(
        module,
        "prepare_run",
        lambda repo: ("block", "note", "claude", "s", "refs/heads/main"),
    )
    return module


def test_overnight_legs_refuses_a_hookless_checkout_before_any_log_dir(
    legs, tmp_path, capsys
):
    repo = hooks_off(handoff_repo(tmp_path / "repo"))
    assert legs.main(["--repo", str(repo), "--dry-run"]) == 2
    err = capsys.readouterr().err
    assert err.startswith("stop: ") and SETUP in err
    assert not (tmp_path / "overnight-logs").exists()


def test_overnight_legs_runs_as_today_with_hooks_on(legs, tmp_path):
    repo = handoff_repo(tmp_path / "repo")
    assert legs.main(["--repo", str(repo), "--dry-run"]) == 0
    assert (tmp_path / "overnight-logs").is_dir()


# --- the fixture helper is what turns them on --------------------------------------


def test_a_fresh_repo_reads_hookless_and_hooks_on_admits_it(tmp_path):
    root = tmp_path / "plain"
    root.mkdir()
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    pin_autocrlf(root)
    assert guard.take(root, COORD) is not None
    hooks_on(root)
    assert guard.take(root, COORD) is None
