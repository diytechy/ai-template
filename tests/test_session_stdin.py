"""Prompt-delivery path (WI-216, SR-026/LLR-026).

A CmdTemplate with a `{prompt}` placeholder rides the command line (`claude -p
{prompt}`); a template WITHOUT `{prompt}` delivers the prompt on STDIN, so the
command line stays short — a Windows npm `.CMD` shim runs under cmd.exe whose
8191-char cap silently kills a brief-sized prompt-in-argv (the failure gilbert hit
on `codex`, whose PROMPT is read from stdin when omitted). Against SN-016 (an
unattended run never wedges on stdin): the fixed prompt is written then stdin is
closed, so the child reads it and sees EOF — never an interactive wait.
"""

import os
import sys
import types

from conftest import load_script

al = load_script("agent_loop")

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


def test_run_session_delivers_stdin_input(tmp_path):
    code, output, timed_out = al.run_session(
        ECHO_STDIN, tmp_path, 30, stdin_input="prompt-via-stdin"
    )
    assert code == 0 and not timed_out, output
    assert "STDIN[prompt-via-stdin]" in output


def test_run_session_without_stdin_input_gives_eof_not_hang(tmp_path):
    # No stdin_input -> DEVNULL -> the child's read() returns '' immediately. If
    # stdin were left open interactively, this would hang until the timeout.
    code, output, timed_out = al.run_session(ECHO_STDIN, tmp_path, 30)
    assert code == 0 and not timed_out, output
    assert "STDIN[]" in output


def test_run_session_large_prompt_past_the_cmd_limit(tmp_path):
    # A prompt well past cmd.exe's 8191-char cap goes through stdin untruncated —
    # the whole point of the fix (gilbert's proven failing size).
    big = "x" * 20044
    code, output, timed_out = al.run_session(ECHO_STDIN, tmp_path, 30, stdin_input=big)
    assert code == 0 and not timed_out, output[:200]
    assert "STDIN[" + big + "]" in output


# --- codex output-capture via --output-last-message (WI-217) -----------------
# codex echoes its banner + the whole prompt into stdout, so its own
# --output-last-message file is read back as the deterministic session result.


def test_codex_lastmsg_setup_appends_and_creates_file():
    argv, path = al._codex_lastmsg_setup(["codex", "exec", "--model", "x"])
    assert argv[-2:] == ["--output-last-message", path]
    assert path is not None and os.path.exists(path)
    os.unlink(path)


def test_codex_lastmsg_setup_case_insensitive_full_path():
    argv, path = al._codex_lastmsg_setup(["/opt/tools/CODEX.EXE", "exec"])
    assert path is not None and "--output-last-message" in argv
    os.unlink(path)


def test_codex_lastmsg_setup_ignores_non_codex():
    assert al._codex_lastmsg_setup(["claude", "-p"]) == (["claude", "-p"], None)
    assert al._codex_lastmsg_setup([]) == ([], None)


def test_codex_lastmsg_read_reads_then_deletes(tmp_path):
    f = tmp_path / "last.txt"
    f.write_text("  the clean result  ", encoding="utf-8")
    assert al._codex_lastmsg_read(str(f)) == "the clean result"
    assert not f.exists()
    assert al._codex_lastmsg_read(None) is None
    assert al._codex_lastmsg_read(str(tmp_path / "nope.txt")) == ""


def test_run_session_codex_reads_last_message_not_transcript(tmp_path):
    # A fake codex that echoes GARBAGE to stdout (as real codex echoes the prompt)
    # but writes the CLEAN result to its --output-last-message file. run_session
    # must return the file content, not the transcript.
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

    code, output, timed_out = al.run_session([str(launcher)], tmp_path, 30)
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


def test_kill_tree_targets_the_whole_process_tree(monkeypatch):
    # Repo-review 2026-07-21 H-2: a timeout/interrupt must kill the session's
    # whole tree, not just the direct child (a .cmd shim's real work lives in a
    # grandchild). Unit-pin the platform branch: Windows walks the tree via
    # taskkill /T; POSIX signals the process group.
    ases = load_script("agent_session")
    fake = types.SimpleNamespace(pid=4242, killed=[])
    fake.kill = lambda: fake.killed.append(True)
    calls = []
    if os.name == "nt":
        monkeypatch.setattr(
            ases.subprocess, "run", lambda argv, **kw: calls.append(argv)
        )
        ases._kill_tree(fake)
        assert calls and calls[0][:4] == ["taskkill", "/F", "/T", "/PID"]
        assert calls[0][4] == "4242"
        assert fake.killed  # the direct-child backstop still fires
    else:
        monkeypatch.setattr(ases.os, "getpgid", lambda pid: 999)
        monkeypatch.setattr(
            ases.os, "killpg", lambda pgid, sig: calls.append((pgid, sig))
        )
        ases._kill_tree(fake)
        assert calls == [(999, ases.signal.SIGKILL)]
