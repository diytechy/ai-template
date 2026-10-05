"""The coordinator context guard (WI-822) through real processes: the claim
refused on the CLI and through a wrapper, the hook CLI, the two relaunch
launchers with `claude` stubbed, and the close-out's git operations passing
while drain mode is latched. Subprocess-heavy, so in conftest SLOW_MODULES;
the in-process cases are test_coordinator_guard.py.
"""

import json
import os
import shutil
import subprocess
import sys

import pytest

from conftest import ROOT, SCRIPTS, env_gate_skipif, load_script
from test_coordinator_guard import COORD, OTHER, Transcript, make_root

guard = load_script("coordinator_guard")


def _env(**extra):
    env = dict(os.environ)
    env.pop(guard.SESSION_ENV, None)
    env.update(extra)
    return env


def _git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip()


@pytest.fixture
def draining(tmp_path):
    """A real git repo whose coordinator lease is held and latched."""
    root = make_root(tmp_path)
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "t")
    (root / "docs" / "work").mkdir(parents=True)
    (root / "docs" / "work" / "pause").write_text("since = 'x'\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "base")
    tx = Transcript(tmp_path / "coord.jsonl")
    tx.user()
    tx.reply(700)
    assert guard.take(root, COORD, str(tx.path)) is None
    guard.claim_refusal(root, env={guard.SESSION_ENV: COORD})
    assert guard._load(guard.lease_dir(root))["draining"] is True
    return root


def test_the_cli_claim_refuses_while_draining(draining):
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "integrate.py"),
            "--root",
            str(draining),
            "claim",
            "--wi",
            "WI-001",
            "--branch",
            "wi-001",
        ],
        capture_output=True,
        encoding="utf-8",
        env=_env(**{guard.SESSION_ENV: COORD}),
    )
    assert proc.returncode == 1 and "drain mode is latched" in proc.stderr


def test_a_wrapper_importing_integrate_is_refused(draining, tmp_path):
    wrapper = tmp_path / "wrapper.py"
    wrapper.write_text(
        "import sys\nsys.path.insert(0, {!r})\nimport integrate\n"
        "sys.exit(integrate.claim(__import__('pathlib').Path({!r}), ['WI-001'], 'wi-001'))\n".format(
            str(SCRIPTS), str(draining)
        ),
        encoding="utf-8",
    )
    proc = subprocess.run(
        [sys.executable, str(wrapper)],
        capture_output=True,
        encoding="utf-8",
        env=_env(**{guard.SESSION_ENV: OTHER}),
    )
    assert proc.returncode == 1 and "held by session " + COORD in proc.stderr


def test_the_hook_cli_reads_stdin_and_prints_its_output(draining, tmp_path):
    payload = {
        "hook_event_name": "SessionStart",
        "session_id": COORD,
        "transcript_path": str(tmp_path / "coord.jsonl"),
        "source": "resume",
    }
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "coordinator_guard.py"), "hook"],
        input=json.dumps(payload),
        capture_output=True,
        encoding="utf-8",
        env=_env(CLAUDE_PROJECT_DIR=str(draining)),
    )
    assert proc.returncode == 0, proc.stderr
    out = json.loads(proc.stdout)
    assert "drain mode is latched" in out["hookSpecificOutput"]["additionalContext"]
    broken = subprocess.run(
        [sys.executable, str(SCRIPTS / "coordinator_guard.py"), "hook"],
        input="{not json",
        capture_output=True,
        encoding="utf-8",
        env=_env(CLAUDE_PROJECT_DIR=str(draining)),
    )
    assert (
        broken.returncode == 0 and broken.stdout == "" and "hook error" in broken.stderr
    )


def test_close_out_git_operations_pass_while_draining(draining, tmp_path):
    """A verification worktree and its removal, a landing (squash), an
    archive ref, and the scoped-unpause restore all run while latched."""
    root = draining
    verify = tmp_path / "verify"
    _git(root, "worktree", "add", "--detach", str(verify), "HEAD")
    _git(root, "worktree", "remove", str(verify))
    _git(root, "rm", "-q", "docs/work/pause")
    _git(root, "commit", "-q", "-m", "unpause (scoped)")
    _git(root, "checkout", "-q", "-b", "wi-001")
    (root / "docs" / "x.md").write_text("x\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "lane work")
    _git(root, "checkout", "-q", "main")
    _git(root, "merge", "--squash", "-q", "wi-001")
    _git(root, "commit", "-q", "-m", "land wi-001")
    _git(root, "branch", "archive/lanes/wi-001", "wi-001")
    _git(root, "branch", "-D", "wi-001")
    _git(root, "checkout", "HEAD~2", "--", "docs/work/pause")
    _git(root, "commit", "-q", "-m", "restore the pause")
    assert (root / "docs" / "work" / "pause").is_file()
    assert guard._load(guard.lease_dir(root))["draining"] is True


def _launcher(tmp_path, name):
    shutil.copy(ROOT / "scripts" / name, tmp_path / name)
    return tmp_path / name


@env_gate_skipif("posix-shell")
def test_the_posix_launcher_runs_claude_in_the_root_with_the_prompt(tmp_path):
    bindir = tmp_path / "bin"
    bindir.mkdir()
    record = tmp_path / "record.txt"
    stub = bindir / "claude"
    stub.write_text(
        '#!/bin/sh\n{{ pwd; printf "%s\\n" "$PT_COORDINATOR_TAKE"; printf "%s" "$1"; }} > "{}"\n'.format(
            record.as_posix()
        ),
        encoding="utf-8",
        newline="\n",
    )
    stub.chmod(0o755)
    work = tmp_path / "work"
    work.mkdir()
    prompt = tmp_path / "prompt.txt"
    prompt.write_text('Read docs/status.md.\nThen "go".', encoding="utf-8")
    launcher = _launcher(tmp_path, "coordinator-relaunch.sh")
    env = _env(PATH=bindir.as_posix() + os.pathsep + os.environ.get("PATH", ""))
    proc = subprocess.run(
        [
            "sh",
            launcher.as_posix(),
            "--inner",
            work.as_posix(),
            prompt.as_posix(),
            "tok123",
        ],
        capture_output=True,
        encoding="utf-8",
        env=env,
    )
    assert proc.returncode == 0, proc.stderr
    cwd, token, text = record.read_text(encoding="utf-8").split("\n", 2)
    assert cwd.rstrip("/").endswith("work") and token == "tok123"
    assert text == 'Read docs/status.md.\nThen "go".'


@pytest.mark.skipif(os.name != "nt", reason="the .cmd launcher is Windows-only")
def test_the_windows_launcher_runs_the_guards_claude_step_in_the_root(tmp_path):
    work = tmp_path / "work"
    scripts = work / "project-trajectory" / "scripts"
    scripts.mkdir(parents=True)
    record = tmp_path / "record.json"
    (scripts / "coordinator_guard.py").write_text(
        "import json, os, sys\njson.dump({{'cwd': os.getcwd(), 'argv': sys.argv[1:], "
        "'token': os.environ.get('PT_COORDINATOR_TAKE')}}, open({!r}, 'w'))\n".format(
            str(record)
        ),
        encoding="utf-8",
    )
    launcher = _launcher(tmp_path, "coordinator-relaunch.cmd")
    prompt = tmp_path / "prompt.txt"
    env = _env(PATH=os.path.dirname(sys.executable) + os.pathsep + os.environ["PATH"])
    proc = subprocess.run(
        ["cmd", "/c", str(launcher), str(work), str(prompt), "tok123"],
        capture_output=True,
        encoding="utf-8",
        env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    seen = json.loads(record.read_text(encoding="utf-8"))
    assert os.path.samefile(seen["cwd"], work)
    assert seen["argv"] == ["exec-claude", "--prompt-file", str(prompt)]
    assert seen["token"] == "tok123"
