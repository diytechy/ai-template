"""Prompt-delivery path (WI-216, SR-026/LLR-026).

A CmdTemplate with a `{prompt}` placeholder rides the command line (`claude -p
{prompt}`) except through a Windows `.cmd`/`.bat` shim, which is refused because
cmd.exe can reparse prompt metacharacters even with `shell=False`; a template
WITHOUT `{prompt}` delivers the prompt on STDIN, so the command line stays short
and avoids that shell boundary. Against SN-016 (an unattended run never wedges
on stdin): the fixed prompt is written then stdin is closed, so the child reads
it and sees EOF — never an interactive wait.
"""

import json
import os
import sys
import time
import types

import pytest

from conftest import load_script

al = load_script("agent_loop")
adapters = load_script("session_adapters")
service = load_script("session_service")
agent_session = al.agent_session

# Cross-platform fake CLI: echo whatever arrived on stdin, bracketed, so a test
# can prove the prompt was delivered there (and only there).
ECHO_STDIN = [
    sys.executable,
    "-c",
    "import sys; sys.stdout.write('STDIN[' + sys.stdin.read() + ']')",
]


def test_build_argv_prompt_placeholder_rides_argv():
    argv, stdin_input = al.build_argv(
        "cli -p {prompt} --model {model}", "m5", "THE-PROMPT"
    )
    assert "THE-PROMPT" in argv
    assert "m5" in argv
    assert stdin_input is None


def test_build_argv_no_placeholder_routes_to_stdin():
    argv, stdin_input = al.build_argv(
        "codex exec --model {model} --yolo", "m5", "THE-PROMPT"
    )
    assert "THE-PROMPT" not in " ".join(argv)  # never on the command line
    assert stdin_input == "THE-PROMPT"


def test_windows_batch_detector_catches_explicit_shim():
    detect = al.agent_session._windows_batch_executable
    path = r"C:\tools\agent.CMD"
    assert detect(path, platform="nt") == path
    assert detect(path, platform="posix") == ""
    assert detect(r"C:\tools\agent.exe", platform="nt") == ""


def test_windows_batch_detector_uses_launch_environment_path(monkeypatch):
    seen = {}

    def fake_which(executable, path=None):
        seen["call"] = executable, path
        return r"C:\selected-tools\agent.bat"

    monkeypatch.setattr(al.agent_session.shutil, "which", fake_which)
    resolved = al.agent_session._windows_batch_executable(
        "agent",
        env={"PATH": r"C:\selected-tools"},
        platform="nt",
    )
    assert resolved == r"C:\selected-tools\agent.bat"
    assert seen["call"] == ("agent", r"C:\selected-tools")


def test_build_argv_refuses_prompt_placeholder_for_windows_batch_shim(monkeypatch):
    monkeypatch.setattr(
        al.agent_session,
        "_windows_batch_executable",
        lambda executable, env=None, platform=None: r"C:\tools\gemini.cmd",
    )
    with pytest.raises(ValueError, match=r"batch shim.*cmd\.exe"):
        al.build_argv("gemini -p {prompt}", "m5", "repo text & whoami")


def test_run_session_refuses_env_resolved_batch_before_spawn(monkeypatch, tmp_path):
    monkeypatch.setattr(
        al.agent_session,
        "_windows_batch_executable",
        lambda executable, env=None, platform=None: r"C:\env-tools\agent.bat",
    )
    code, output, timed_out = agent_session.run_session(
        ["agent", "-p", "repo text & whoami"],
        tmp_path,
        30,
        env={"PATH": r"C:\env-tools"},
    )
    assert code == -1 and not timed_out
    assert "unsafe prompt delivery refused" in output
    assert "stdin prompt path" in output


def test_windows_batch_shim_is_allowed_when_prompt_uses_stdin(monkeypatch, tmp_path):
    monkeypatch.setattr(
        al.agent_session,
        "_windows_batch_executable",
        lambda executable, env=None, platform=None: r"C:\tools\agent.cmd",
    )
    # The safety guard must not reject the supported transport. Use a missing
    # executable so the platform-independent test stops at the ordinary spawn
    # sentinel after proving it passed the batch-prompt guard.
    code, output, timed_out = agent_session.run_session(
        ["definitely-missing-agent-cli"],
        tmp_path,
        30,
        stdin_input="prompt-via-stdin",
    )
    assert code == -1 and not timed_out
    assert "unsafe prompt delivery refused" not in output
    assert "session error" in output


def test_run_session_delivers_stdin_input(tmp_path):
    code, output, timed_out = agent_session.run_session(
        ECHO_STDIN, tmp_path, 30, stdin_input="prompt-via-stdin"
    )
    assert code == 0 and not timed_out, output
    assert "STDIN[prompt-via-stdin]" in output


def test_run_session_without_stdin_input_gives_eof_not_hang(tmp_path):
    # No stdin_input -> DEVNULL -> the child's read() returns '' immediately. If
    # stdin were left open interactively, this would hang until the timeout.
    code, output, timed_out = agent_session.run_session(ECHO_STDIN, tmp_path, 30)
    assert code == 0 and not timed_out, output
    assert "STDIN[]" in output


def test_run_session_large_prompt_past_the_cmd_limit(tmp_path):
    # A prompt well past cmd.exe's 8191-char cap goes through stdin untruncated —
    # the whole point of the fix (gilbert's proven failing size).
    big = "x" * 20044
    code, output, timed_out = agent_session.run_session(
        ECHO_STDIN, tmp_path, 30, stdin_input=big
    )
    assert code == 0 and not timed_out, output[:200]
    assert "STDIN[" + big + "]" in output


# --- codex output-capture via --output-last-message (WI-217) -----------------
# codex echoes its banner + the whole prompt into stdout, so its own
# --output-last-message file is read back as the deterministic session result.


def test_codex_lastmsg_setup_appends_and_creates_file():
    argv, path = adapters._codex_lastmsg_setup(["codex", "exec", "--model", "x"])
    assert argv[-2:] == ["--output-last-message", path]
    assert path is not None and os.path.exists(path)
    os.unlink(path)


def test_codex_lastmsg_setup_case_insensitive_full_path():
    argv, path = adapters._codex_lastmsg_setup(["/opt/tools/CODEX.EXE", "exec"])
    assert path is not None and "--output-last-message" in argv
    os.unlink(path)


def test_codex_lastmsg_setup_ignores_non_codex():
    assert adapters._codex_lastmsg_setup(["claude", "-p"]) == (["claude", "-p"], None)
    assert adapters._codex_lastmsg_setup([]) == ([], None)


def test_codex_lastmsg_read_reads_then_deletes(tmp_path):
    f = tmp_path / "last.txt"
    f.write_text("  the clean result  ", encoding="utf-8")
    assert adapters._codex_lastmsg_read(str(f)) == "the clean result"
    assert not f.exists()
    assert adapters._codex_lastmsg_read(None) is None
    assert adapters._codex_lastmsg_read(str(tmp_path / "nope.txt")) == ""


def test_codex_session_reads_last_message_not_transcript(tmp_path):
    # A fake codex that echoes GARBAGE to stdout (as real codex echoes the prompt)
    # but writes the CLEAN result to its --output-last-message file. The session
    # boundary must return the file content, not the transcript: the codex
    # adapter adds the flag, and run_session itself captures the whole stream.
    impl = tmp_path / "impl.py"
    impl.write_text(
        "import sys\n"
        "sys.stdout.write('GARBAGE-TRANSCRIPT-echoing-the-whole-prompt\\n')\n"
        "a = sys.argv[1:]\n"
        "if '--output-last-message' in a:\n"
        "    p = a[a.index('--output-last-message') + 1]\n"
        "    open(p, 'w', encoding='utf-8').write('CLEAN-165-char-result-table')\n",
        encoding="utf-8",
    )
    if os.name == "nt":
        launcher = tmp_path / "codextest.cmd"
        launcher.write_text(
            '@"{}" "{}" %*\n'.format(sys.executable, impl), encoding="utf-8"
        )
    else:
        launcher = tmp_path / "codextest"
        launcher.write_text(
            '#!/bin/sh\nexec "{}" "{}" "$@"\n'.format(sys.executable, impl),
            encoding="utf-8",
        )
        launcher.chmod(0o755)

    # Deliver the prompt via stdin (WI-216), matching the real codex CmdTemplate
    # (no {prompt} placeholder) — the transport the H-4 guard (272a6e8) requires
    # for a Windows batch shim launcher; the impl above never reads stdin, so
    # this only proves the launch clears the guard and the capture still works.
    launched = service.act(
        service.Call(
            root=tmp_path,
            role="BUILD",
            template=json.dumps([str(launcher)]),
            prompt="the prompt",
            timeout=30,
        )
    )
    code, output, timed_out = launched.code, launched.text, launched.timed_out
    assert code == 0 and not timed_out, output
    assert output == "CLEAN-165-char-result-table"  # not the GARBAGE transcript
    assert "GARBAGE" not in output


# --- --interactive with a no-{prompt} template (review-17c H1) ----------------


def test_run_interactive_pipes_prompt_via_stdin(tmp_path):
    # A no-{prompt} interactive template (the registry's default form after
    # WI-217, reachable via the --interactive-cmd -> AGENT_CMD_INTERACTIVE ->
    # AGENT_CMD fallback chain) pipes the composed prompt to the child's stdin
    # in TEXT mode. Regression: a str input without text=True is a TypeError,
    # so the hands-on entry crashed on exactly the template shape the registry
    # ships. The guardrails core makes the composed prompt non-empty so the
    # probe can prove delivery, not just survival.
    (tmp_path / "docs" / "guardrails").mkdir(parents=True)
    (tmp_path / "docs" / "guardrails" / "core.md").write_text(
        "THE-GUARDRAILS-CORE", encoding="utf-8"
    )
    probe = tmp_path / "probe.py"
    probe.write_text(
        "import sys\nsys.exit(0 if 'THE-GUARDRAILS-CORE' in sys.stdin.read() else 3)\n",
        encoding="utf-8",
    )
    args = types.SimpleNamespace(
        interactive_cmd='"{}" "{}"'.format(sys.executable, probe), model="m5"
    )
    code = al.run_interactive(
        args,
        tmp_path,
        model_map={},
        cmd_map={},
        template="",
        guardrails_policy="all",
        warned_no_core=[],
    )
    assert code == 0  # the child read the piped prompt and saw EOF


def test_attached_interactive_runner_inherits_stdio(monkeypatch, tmp_path):
    calls = []

    def fake_run(argv, **kwargs):
        calls.append((argv, kwargs))
        return types.SimpleNamespace(returncode=7)

    monkeypatch.setattr(service.subprocess, "run", fake_run)
    assert service.run_attached(["agent"], tmp_path, None) == (7, "", False)
    assert calls == [(["agent"], {"cwd": str(tmp_path)})]


def test_interactive_launch_error_is_recorded_then_raised(tmp_path):
    args = types.SimpleNamespace(
        interactive_cmd="definitely-missing-interactive-agent", model="m5"
    )
    with pytest.raises(FileNotFoundError):
        al.run_interactive(
            args,
            tmp_path,
            model_map={},
            cmd_map={},
            template="",
            guardrails_policy="none",
            warned_no_core=[],
        )
    logs = list((tmp_path / "docs" / "iteration").glob("call_*.log"))
    assert len(logs) == 1
    meta = al.agent_common.read_log_meta(logs[0])
    assert meta["outcome"] == "ERROR"
    assert meta["usage-status"] == "unavailable"
    assert meta["invocation-id"]
    assert meta["started-at"] and meta["ended-at"]


# A grandchild that names itself, then outlives its parent unless the whole
# tree dies: the shape of a `.cmd` shim's `node` (repo-review 2026-07-21 H-2).
# It sleeps far past any kill path under test, so its exit is the kill's doing.
GRANDCHILD = (
    "import os, sys, time\n"
    "print('GRANDCHILD', os.getpid(), flush=True)\n"
    "time.sleep(300)\n"
)


def _session_with_a_grandchild(tmp_path, parent):
    """The argv of a session whose real work lives in a grandchild: a Python
    parent that spawns it, or (Windows) a `.cmd` shim, where cmd.exe is the
    direct child and the interpreter it launches is the grandchild."""
    script = tmp_path / "grandchild.py"
    script.write_text(GRANDCHILD, encoding="utf-8")
    if parent == "cmd-shim":
        shim = tmp_path / "agent.cmd"
        shim.write_text(
            '@echo off\r\n"{}" "{}"\r\n'.format(sys.executable, script),
            encoding="utf-8",
        )
        return [str(shim)]
    spawn = (
        "import subprocess, sys, time\n"
        "subprocess.Popen([sys.executable, sys.argv[1]])\n"
        "time.sleep(300)\n"
    )
    return [sys.executable, "-c", spawn, str(script)]


class _Watched:
    """Holds a live process by pid so a test can ask whether it has exited.
    Windows: a SYNCHRONIZE|TERMINATE handle opened while it runs, so the pid
    cannot be reused under the check. POSIX: the pid, with a zombie counted as
    exited (reaping is the adopting parent's job, not the kill's)."""

    def __init__(self, pid):
        self.pid = pid
        self.handle = None
        if os.name == "nt":
            self.k32 = _kernel32()
            self.handle = self.k32.OpenProcess(0x00100000 | 0x0001, False, pid)
            assert self.handle, "could not open the grandchild {}".format(pid)

    def exited_within(self, seconds):
        if os.name == "nt":
            return self.k32.WaitForSingleObject(self.handle, int(seconds * 1000)) == 0
        deadline = time.time() + seconds
        while self._alive_posix():  # checked at least once, even for 0 s
            if time.time() >= deadline:
                return False
            time.sleep(0.05)
        return True

    def _alive_posix(self):
        try:
            os.kill(self.pid, 0)
        except ProcessLookupError:
            return False
        try:
            with open("/proc/{}/stat".format(self.pid)) as fh:
                return fh.read().rsplit(")", 1)[1].split()[0] != "Z"
        except OSError:
            return True

    def reap(self):
        """Test hygiene only: kill a survivor so a red run leaks nothing."""
        if os.name == "nt":
            self.k32.TerminateProcess(self.handle, 1)
            self.k32.CloseHandle(self.handle)
        elif self._alive_posix():
            os.kill(self.pid, 9)


def _kernel32():
    import ctypes
    from ctypes import wintypes

    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.OpenProcess.restype = wintypes.HANDLE
    k32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    k32.WaitForSingleObject.restype = wintypes.DWORD
    k32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    k32.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
    k32.CloseHandle.argtypes = [wintypes.HANDLE]
    return k32


@pytest.mark.parametrize(
    "parent",
    [
        "python-parent",
        pytest.param(
            "cmd-shim",
            marks=pytest.mark.skipif(os.name != "nt", reason="a .cmd shim is Windows"),
        ),
    ],
)
def test_a_deadline_kill_ends_the_grandchild(tmp_path, parent):
    # WI-881 on repo-review 2026-07-21 H-2: a deadline kill ends the session's
    # whole tree, not just the direct child, on real processes — the grandchild
    # holds the work (and the stdout pipe) a `.cmd` shim's node would.
    watched = []

    def on_line(line):
        if line.startswith("GRANDCHILD "):
            watched.append(_Watched(int(line.split()[1])))

    try:
        code, output, timed_out = agent_session.run_session(
            _session_with_a_grandchild(tmp_path, parent),
            tmp_path,
            55,
            on_line=on_line,
            stdin_input="",  # a batch shim takes its prompt on stdin, never argv
            idle_timeout=2,
        )
        assert timed_out == "idle" and code == -1, output[-300:]
        assert len(watched) == 1, output[-300:]
        # No grace period (D-003): the kill returns only once the tree is
        # empty, so the grandchild is already gone when run_session returns.
        assert watched[0].exited_within(0), "the grandchild outlived the kill"
    finally:
        for proc in watched:
            proc.reap()


@pytest.mark.parametrize(
    "parent",
    [
        "python-parent",
        pytest.param(
            "cmd-shim",
            marks=pytest.mark.skipif(os.name != "nt", reason="a .cmd shim is Windows"),
        ),
    ],
)
def test_an_interruption_ends_the_grandchild(tmp_path, parent):
    # WI-881 (sitting 001's return): a KeyboardInterrupt in the coordinator
    # while _wait_for_exit waits takes the interrupt path, not the deadline
    # path: it ends the whole tree and propagates. interrupt_main() is raised
    # once the grandchild has named itself, so the main thread is waiting in
    # one-second slices (the wall deadline below) when it lands.
    import _thread

    watched = []

    def on_line(line):
        if line.startswith("GRANDCHILD "):
            watched.append(_Watched(int(line.split()[1])))
            _thread.interrupt_main()

    try:
        with pytest.raises(KeyboardInterrupt):
            agent_session.run_session(
                _session_with_a_grandchild(tmp_path, parent),
                tmp_path,
                55,
                on_line=on_line,
                stdin_input="",
            )
        assert len(watched) == 1, "the grandchild never started"
        assert watched[0].exited_within(0), "the grandchild outlived the interrupt"
    finally:
        for proc in watched:
            proc.reap()


@pytest.mark.skipif(os.name != "nt", reason="job containment is Windows")
def test_an_uncontainable_child_errors_before_it_runs(tmp_path, monkeypatch):
    # WI-881 (sitting 001's return): a child that cannot be put in a job is
    # killed while still suspended, so it never runs, and the session ends as
    # a session error; there is no uncontained fallback (D-001).
    marker = tmp_path / "ran.txt"

    def no_job(proc):
        raise OSError("forced containment failure")

    monkeypatch.setattr(agent_session, "_contain_in_job", no_job)
    code, output, timed_out = agent_session.run_session(
        [
            sys.executable,
            "-c",
            "open(r'{}', 'w').write('ran'); print('RAN')".format(marker),
        ],
        tmp_path,
        30,
    )
    assert (code, timed_out) == (-1, False)
    assert output == "coordinator: session error: forced containment failure"
    assert not marker.exists(), "the uncontained child ran"


def test_a_tree_not_ended_within_the_bound_raises(tmp_path, monkeypatch):
    # D-003: the kill waits for the session's group (POSIX) or job (Windows)
    # to empty, and past the stated bound it raises, naming the survivor,
    # instead of letting the coordinator continue. The probe is made to report
    # a survivor; the real child is still killed and reaped.
    monkeypatch.setattr(agent_session, "_TREE_END_SECONDS", 0.3)
    if os.name == "nt":
        monkeypatch.setattr(agent_session, "_job_active_processes", lambda job: 2)
    else:
        real_killpg = os.killpg

        def killpg(pgid, sig):
            if sig != 0:
                real_killpg(pgid, sig)

        monkeypatch.setattr(agent_session.os, "killpg", killpg)
    proc = agent_session._spawn_session(
        [sys.executable, "-c", "import time; time.sleep(30)"]
    )
    try:
        t0 = time.time()
        with pytest.raises(agent_session.TreeNotEnded) as raised:
            agent_session._kill_tree(proc)
        assert isinstance(raised.value, OSError), type(raised.value).__mro__
        assert time.time() - t0 < 5
        assert proc.returncode is not None, "the direct child was not reaped"
    finally:
        if proc.returncode is None:
            proc.kill()
            proc.wait()
    expected = (
        "2 processes still in the session's job"
        if os.name == "nt"
        else "process group {}".format(proc.pid)
    )
    assert expected in str(raised.value) and "0.3s" in str(raised.value)


def test_an_ordinary_launch_error_still_returns_the_session_error(tmp_path):
    # A launch that never created a child (a missing executable) returns
    # the ordinary session-error result.
    code, output, timed_out = agent_session.run_session(
        ["wi881-no-such-agent-cli"], tmp_path, 30
    )
    assert (code, timed_out) == (-1, False)
    assert output.startswith("coordinator: session error: "), output


@pytest.mark.skipif(os.name != "nt", reason="the job snapshot is Windows")
def test_a_member_the_kill_cannot_open_makes_it_raise(monkeypatch):
    # WI-881 S3 (D-004): a live member that denies the kill SYNCHRONIZE cannot
    # be waited on, so the kill terminates the job and then raises naming it,
    # rather than counting the member as already gone. A pid that no longer
    # exists (error 87) is still skipped.
    k32, _ = agent_session._win32()
    proc = agent_session._spawn_session(
        [sys.executable, "-c", "import time; time.sleep(30)"]
    )

    def denied(access, inherit, pid):
        import ctypes

        ctypes.set_last_error(5)  # ERROR_ACCESS_DENIED
        return None

    monkeypatch.setattr(k32, "OpenProcess", denied)
    try:
        with pytest.raises(agent_session.TreeNotEnded) as raised:
            agent_session._kill_tree(proc)
    finally:
        monkeypatch.undo()
    assert str(proc.pid) in str(raised.value), str(raised.value)
    assert proc.wait(timeout=10) is not None, "the job was not terminated"


SLEEPY_AFTER_ONE_LINE = [
    sys.executable,
    "-c",
    "import sys, time; print('hello'); sys.stdout.flush(); time.sleep(60)",
]


def test_run_session_idle_deadline_kills_a_silent_child(tmp_path):
    # C3 (docs/plans/2026-08-30-stall-guard-plan.md): a child that stops
    # emitting is killed at the IDLE deadline, not discovered at the wall —
    # two silent hangs on 2026-08-30 each burned a 7200 s wall slot.
    import time as _time

    t0 = _time.time()
    code, output, timed_out = agent_session.run_session(
        SLEEPY_AFTER_ONE_LINE, tmp_path, 55, idle_timeout=2
    )
    wall = _time.time() - t0
    assert timed_out == "idle"
    assert code == -1
    assert "idle-timed out" in output and "hello" in output
    assert wall < 40, "killed at the idle deadline, not the wall ({}s)".format(wall)


def test_run_session_wall_timeout_keeps_its_historical_shape(tmp_path):
    # The wall kill still reports timed_out is True (the historical value) so
    # every existing truthiness read holds; only the idle kill says "idle".
    code, output, timed_out = agent_session.run_session(
        SLEEPY_AFTER_ONE_LINE, tmp_path, 2, idle_timeout=None
    )
    assert timed_out is True
    assert code == -1
    assert "timed out after 2s" in output


def test_a_raising_renderer_never_stops_the_pump(tmp_path):
    # C3 hardening (2026-08-30, WI-548): an `on_line` renderer that raises —
    # a cp1252 console meeting a non-encodable character was the live case —
    # used to kill the pump thread; the child then blocked on a full pipe and
    # the session read as a silent hang until a deadline fired. The pump must
    # outlive its renderer: the session completes, the output is captured.
    chatty = [
        sys.executable,
        "-c",
        "import sys\nfor i in range(20000): print('line', i)",
    ]

    def boom(line):
        raise UnicodeEncodeError("cp1252", line, 0, 1, "renderer failed")

    code, output, timed_out = agent_session.run_session(
        chatty, tmp_path, 60, on_line=boom, idle_timeout=20
    )
    assert code == 0 and not timed_out, output[-300:]
    assert output.count("line") == 20000
