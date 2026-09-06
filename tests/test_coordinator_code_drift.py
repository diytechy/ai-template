"""A long-lived coordinator stops at a durable boundary when its code moves."""

import os
from types import SimpleNamespace

import pytest

from conftest import load_script


def test_script_fingerprint_moves_with_python_source_only(tmp_path):
    ac = load_script("agent_common")
    scripts = tmp_path / "scripts"
    nested = scripts / "kitlib"
    nested.mkdir(parents=True)
    first = scripts / "agent_loop.py"
    sibling = nested / "state.py"
    first.write_text("value = 1\n", encoding="utf-8")
    sibling.write_text("state = 'ready'\n", encoding="utf-8")
    original = ac.scripts_fingerprint(scripts)

    (scripts / "README.md").write_text("operator prose\n", encoding="utf-8")
    assert ac.scripts_fingerprint(scripts) == original

    sibling.write_text("state = 'changed'\n", encoding="utf-8")
    edited = ac.scripts_fingerprint(scripts)
    assert edited != original

    sibling.rename(nested / "renamed.py")
    assert ac.scripts_fingerprint(scripts) != edited


def test_an_unreadable_source_scan_requests_a_typed_restart(monkeypatch):
    ac = load_script("agent_common")
    monkeypatch.setattr(
        ac,
        "scripts_fingerprint",
        lambda: (_ for _ in ()).throw(OSError("source moved during scan")),
    )
    assert ac.running_scripts_moved() is True


def test_worker_rechecks_after_a_blackout_wait(monkeypatch, tmp_path):
    al = load_script("agent_loop")
    moved = {"now": False}
    monkeypatch.setattr(al.agent_common, "running_scripts_moved", lambda: moved["now"])
    monkeypatch.setattr(
        al,
        "wait_out_blackout",
        lambda _lane: moved.update(now=True),
    )
    ctx = SimpleNamespace(
        args=SimpleNamespace(),
        root=tmp_path,
        lane=tmp_path,
        worker=None,
        run=SimpleNamespace(routing=SimpleNamespace()),
    )

    assert al.run_iteration(ctx, 1) == al.EXIT_RESTART


def _can_symlink(directory):
    try:
        os.symlink(directory / "nowhere", directory / "probe-link")
    except (OSError, NotImplementedError):
        return False
    return True


def test_a_dangling_lock_symlink_is_not_part_of_the_fingerprint(tmp_path):
    # An editor's lock file (`.#a.py`, a dangling symlink) matches `*.py` and
    # used to raise FileNotFoundError at IMPORT of every kit entry point that
    # loads agent_common (the 2026-09-06 review's finding 2).
    ac = load_script("agent_common")
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "a.py").write_text("x = 1\n", encoding="utf-8")
    clean = ac.scripts_fingerprint(scripts)
    if not _can_symlink(tmp_path):
        pytest.skip("symlinks need a privilege this box does not grant")
    os.symlink(tmp_path / "gone.py", scripts / ".#a.py")
    (scripts / "dir.py").mkdir()
    assert ac.scripts_fingerprint(scripts) == clean


def test_a_failed_launch_capture_disables_drift_detection_without_a_loop(
    monkeypatch, capsys
):
    ac = load_script("agent_common")
    monkeypatch.setattr(
        ac,
        "scripts_fingerprint",
        lambda *_a: (_ for _ in ()).throw(OSError("unreadable at launch")),
    )
    assert ac._launch_fingerprint() is None
    assert "drift detection unavailable" in capsys.readouterr().err
    # With no launch capture there is nothing to compare against: the answer
    # is "unavailable" (False), never a restart on every poll.
    monkeypatch.setattr(ac, "LAUNCHED_SCRIPTS_FINGERPRINT", None)
    monkeypatch.setattr(ac, "scripts_fingerprint", lambda *_a: "moved")
    assert ac.running_scripts_moved() is False
