#!/usr/bin/env python3
"""One headless agent session: argv/stdin construction, launch, and capture.

Extracted VERBATIM from agent_loop.py (WI-218 slice B — a file split, not a
rewrite; the behaviors and their WI history are unchanged). This is the layer
that turns a CmdTemplate + model + prompt into one running CLI session and
returns its output:

  - `split_cmd`/`build_argv` — template -> argv, deciding prompt delivery:
    a `{prompt}` placeholder rides the command line except through a Windows
    batch shim (refused because cmd.exe reparses it); NO `{prompt}` routes the
    prompt to the child's STDIN (WI-216), immune to caps and batch-shell parsing.
  - `run_session` — one fresh headless driver session (stdin closed or fed +
    closed — never an interactive wait, SN-016), with a reader thread so the
    child can't block on a full pipe, a per-session timeout, and codex
    result capture via `--output-last-message` (WI-217).
  - `parse_json_result` — best-effort result-event parse of a
    --output-format json / stream-json transcript.
  - `summarize_session_line`/`echo_session_line`/`LiveStatus` (+ the TTY/VT
    probes) — the console rendering of a streaming session (WI-125/WI-136).

Stdlib only, Python 3.11+, Windows/POSIX. agent_loop.py (the coordinator) and
plan_runner.py (the dual-plan round) drive sessions exclusively through this
module; agent_loop re-exports these names so its public surface is unchanged.

Contracts: IF-041, IF-064 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import json
import os
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
from pathlib import Path


def split_cmd(template):
    """Split a command template into tokens.

    TWO ACCEPTED FORMS, and the second exists because the first cannot be made
    unambiguous. A `CmdTemplate` may be:

      a JSON ARRAY   `["claude", "-p", "--model", "{model}"]` — the tokens are
                     the tokens, full stop. No quoting rules, no shell grammar,
                     nothing for a Windows path or an embedded quote to trip
                     over. This is the form to declare a NEW route in
                     (plan §11.7).
      a SHELL STRING `claude -p --model {model}` — the historical form, split
                     quote-aware with backslash escaping DISABLED so Windows
                     paths survive (shlex's posix escape rules would eat
                     drive-letter separators). Every shipped row and every
                     existing adopter registry uses it, so it is read exactly
                     as before.

    The array form is recognised only when the value parses as a JSON list;
    anything else — including a string that merely starts with a bracket —
    falls through to the shell split, so no existing template can change
    meaning. A JSON array holding a NON-STRING token raises rather than being
    stringified into a command nobody wrote: a registry is config a human
    edits, and a silent coercion there is a launch that does not match its
    declaration."""
    text = (template or "").strip()
    if text.startswith("["):
        try:
            parsed = json.loads(text)
        except ValueError:
            parsed = None
        if isinstance(parsed, list):
            bad = [tok for tok in parsed if not isinstance(tok, str)]
            if bad:
                raise ValueError(
                    "CmdTemplate is a JSON array but holds a non-string token "
                    "{!r} — argv tokens are strings".format(bad[0])
                )
            return list(parsed)
    lex = shlex.shlex(template, posix=True)
    lex.whitespace_split = True
    lex.escape = ""
    lex.commenters = ""
    return list(lex)


def _windows_batch_executable(executable, env=None, platform=None):
    """Return the resolved Windows batch path for ``executable``, else ``""``.

    Windows may route ``.cmd``/``.bat`` files through ``cmd.exe`` even when
    ``subprocess`` is called with ``shell=False``. Keep that platform exception
    in one helper so preflight and the final launch boundary make the same
    decision. ``platform`` is injectable for cross-platform tests.
    """
    if (os.name if platform is None else platform) != "nt" or not executable:
        return ""
    if executable.lower().endswith((".cmd", ".bat")):
        return executable
    search_env = os.environ if env is None else env
    resolved = shutil.which(executable, path=search_env.get("PATH"))
    if resolved and resolved.lower().endswith((".cmd", ".bat")):
        return resolved
    return ""


def _batch_prompt_error(argv, stdin_input, env=None, platform=None):
    """Explain an unsafe prompt-in-argv Windows batch launch, or return ``""``."""
    if stdin_input is not None or not argv:
        return ""
    batch = _windows_batch_executable(argv[0], env=env, platform=platform)
    if not batch:
        return ""
    return (
        "unsafe prompt delivery refused: {!r} is a Windows batch shim, so "
        "cmd.exe can reparse a {{prompt}} argument even with shell=False; omit "
        "{{prompt}} and use the CLI's stdin prompt path, or configure a native "
        "executable"
    ).format(batch)


def _validate_prompt_transport(argv, stdin_input, env=None, platform=None):
    """Raise ``ValueError`` when prompt-in-argv would cross a batch shell."""
    error = _batch_prompt_error(argv, stdin_input, env=env, platform=platform)
    if error:
        raise ValueError(error)


def build_argv(template, model, prompt):
    """Build the session argv from a CmdTemplate and decide how the prompt is
    delivered. Returns `(argv, stdin_input)`:

    - A template that carries a `{prompt}` placeholder gets it substituted into
      argv, and `stdin_input` is None — the prompt rides the command line (the
      historical behavior; `claude -p {prompt}`).
    - A template with NO `{prompt}` placeholder delivers the prompt on STDIN
      instead: `stdin_input = prompt`, and argv carries only the flags. This keeps
      the command line short — a Windows npm `.CMD` shim runs under cmd.exe, whose
      **8191-char** command-line cap silently kills a brief-sized prompt-in-argv
      (the failure gilbert hit on `codex`) — while the CLI reads the prompt from
      stdin (`codex exec` with no PROMPT arg reads stdin; run_session pipes it).

    Substitution is per-token. On Windows a batch shim is the OS exception:
    ``.cmd``/``.bat`` arguments can be reparsed by ``cmd.exe`` even with
    ``shell=False``, so prompt-in-argv is refused for those executables; use
    stdin prompt delivery or a native executable instead."""
    argv = []
    saw_prompt = False
    for tok in split_cmd(template):
        if "{prompt}" in tok:
            saw_prompt = True
        argv.append(tok.replace("{model}", model).replace("{prompt}", prompt))
    stdin_input = None if saw_prompt else prompt
    _validate_prompt_transport(argv, stdin_input)
    return argv, stdin_input


def parse_json_result(output):
    """Best-effort parse of a --output-format json / stream-json run: the last
    line (or the whole output) that loads as a JSON object, preferring a
    `type: result` event — so a stream-json transcript whose tail carries a
    non-result event (a killed stream, trailing diagnostics) never shadows the
    session result. Returns {} when nothing parses."""
    candidates = [ln for ln in output.splitlines() if ln.strip()][-3:]
    dicts = []
    for text in reversed(candidates + [output.strip()]):
        try:
            data = json.loads(text)
        except ValueError:
            continue
        if isinstance(data, dict):
            dicts.append(data)
    for data in dicts:
        if data.get("type") == "result":
            return data
    return dicts[0] if dicts else {}


def _kill_tree(proc):
    """Kill the session's whole process tree, not just the direct child: a
    `.cmd`-shim CLI's real work happens in a grandchild (cmd.exe -> node), and
    a survivor keeps editing the worktree the coordinator is about to hand to
    the next session (repo-review 2026-07-21 H-2). POSIX: the child leads its
    own session (start_new_session at Popen), so SIGKILL its process group;
    fall back to proc.kill() if the group is already gone. Windows: taskkill
    /T walks the tree (ships with the OS); proc.kill() remains the backstop
    either way. Best-effort by design — the caller's wait() reaps the direct
    child regardless."""
    if os.name == "nt":
        try:
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
            )
        except OSError:
            pass
        try:
            proc.kill()
        except OSError:
            pass
    else:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except (OSError, ProcessLookupError):
            try:
                proc.kill()
            except OSError:
                pass


def summarize_session_line(line):
    """Parse one line of session output into zero or more compact console
    summaries (WI-125) — shared by the scrolling echo (echo_session_line) and
    the in-place live line (LiveStatus, WI-136). stream-json events render as
    `  > <assistant text>` / `  * <tool name>`; result/system/user events are
    suppressed (the coordinator prints its own outcome line, and tool results
    re-echo file contents). A line that isn't a JSON event — a plain-text CLI
    like opencode — passes through as one truncated summary. Every summary is
    truncated for console hygiene; the FULL stream is still captured for the
    session log + out/run-logs regardless."""
    s = line.rstrip()
    if not s:
        return []
    if s.startswith("{"):
        try:
            evt = json.loads(s)
        except ValueError:
            evt = None
        if isinstance(evt, dict):
            out = []
            if evt.get("type") == "assistant":
                for block in (evt.get("message") or {}).get("content") or []:
                    if block.get("type") == "text" and block.get("text", "").strip():
                        txt = " ".join(block["text"].split())
                        out.append(
                            "  > {}".format(
                                txt[:240] + ("..." if len(txt) > 240 else "")
                            )
                        )
                    elif block.get("type") == "tool_use":
                        out.append("  * {}".format(block.get("name", "tool")))
            return out  # every other event type is log detail, not progress
    return [s[:240] + ("..." if len(s) > 240 else "")]


def echo_session_line(line):
    """Scrolling live echo (WI-125): print each compact summary of one output
    line so a walk-away console shows progress instead of silent minutes."""
    for summary in summarize_session_line(line):
        print(summary)


def _stdout_is_tty():
    """True only when the coordinator console is an interactive terminal — the
    gate for the in-place live line (WI-136). A pipe / redirect / CI log is not
    a TTY, so it keeps the append-only scroll (CI logs must stay append-only)."""
    try:
        return bool(sys.stdout.isatty())
    except Exception:
        return False


def _enable_windows_vt():
    """Best-effort enable of ANSI/VT escape processing for the current Windows
    console (modern conhost + Windows Terminal support it, but the flag can be
    off). stdlib-only via ctypes — no curses / colorama dependency. Returns True
    when VT is usable (always so on a non-Windows OS), False when it could not be
    turned on, so the caller falls back to the plain scroll rather than emit raw
    escape bytes (never-breaking)."""
    if os.name != "nt":
        return True
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        if not handle or handle == -1:
            return False
        mode = ctypes.c_uint()
        if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            return False
        enable_vt = 0x0004  # ENABLE_VIRTUAL_TERMINAL_PROCESSING
        if mode.value & enable_vt:
            return True
        return bool(kernel32.SetConsoleMode(handle, mode.value | enable_vt))
    except Exception:
        return False


class LiveStatus:
    """One in-place console status line for a workstream (WI-136). Opt-in
    (--live-status / docs/live-status) and used only when stdout is a TTY with
    VT enabled — a non-TTY keeps the scrolling echo. Each streamed event
    rewrites a single line (carriage-return + clear-to-EOL) instead of
    scrolling, so a long walk-away session shows its current step rather than
    30 silent minutes. The FULL stream is still captured for the session log +
    out/run-logs; this only changes what the console shows."""

    def __init__(self, label):
        self.label = label
        self.active = False

    def event(self, line):
        for summary in summarize_session_line(line):
            self._render(summary)

    def _render(self, summary):
        prefix = "  [{}] ".format(self.label)
        width = shutil.get_terminal_size((80, 24)).columns
        text = (prefix + " ".join(summary.split()))[: max(1, width - 1)]
        # \r to column 0, \x1b[2K to clear the whole line, then rewrite it.
        sys.stdout.write("\r\x1b[2K" + text)
        sys.stdout.flush()
        self.active = True

    def finish(self):
        """Close the live line with a newline so the next scrolling print starts
        clean — a no-op when nothing was ever rendered (an idle/errored session)."""
        if self.active:
            sys.stdout.write("\n")
            sys.stdout.flush()
            self.active = False


def _codex_lastmsg_setup(argv):
    """If argv launches codex, append its `--output-last-message` temp file and
    return (augmented_argv, path); otherwise (argv, None). codex echoes its banner
    + the whole prompt into stdout, so that file — its own final-message contract —
    is the deterministic session result (WI-217, gilbert 9add15b).

    Detection is a basename-prefix heuristic (accepted trade-off): a lookalike
    CLI named codex-* would receive the flag too, and a template that already
    declares its own -o/--output-last-message gets a second one (codex
    last-wins, so the kit's temp file is the one read back). Revisit as a
    declared registry column only if that ever bites a real registry."""
    if not (argv and os.path.basename(argv[0]).lower().startswith("codex")):
        return argv, None
    fd, path = tempfile.mkstemp(prefix="codex-lastmsg-", suffix=".txt")
    os.close(fd)
    return argv + ["--output-last-message", path], path


def _codex_lastmsg_read(path):
    """Read then delete the codex last-message file (`path` None for a non-codex
    session -> None). Best-effort: a missing/unreadable file reads as empty."""
    if path is None:
        return None
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        text = ""
    try:
        os.unlink(path)
    except OSError:
        pass
    return text


def run_session(argv, root, timeout, env=None, on_line=None, stdin_input=None):
    """One fresh headless driver session. Returns (exit_code, output,
    timed_out). stdin is closed so a CLI that would wait on it can't hang —
    UNLESS `stdin_input` is given, in which case that fixed text is written to the
    child's stdin which is then closed: the child reads its prompt and sees EOF,
    so the no-wedge invariant (SN-016) still holds — there is never an interactive
    read. This is how a CmdTemplate with no `{prompt}` placeholder delivers the
    prompt (build_argv), keeping the command line short enough for the Windows
    cmd.exe 8191-char cap on `.CMD`-shim CLIs.

    `env` is the merged environment for a pair row that declares one (the
    registry `Env` column, already merged over os.environ by the caller); None
    means inherit the ambient environment exactly — today's call, byte for
    byte. `on_line`, when given, is called with each output line as it arrives —
    the console renderer (echo_session_line's scroll, WI-125, or LiveStatus's
    in-place line, WI-136); the returned output is the full captured stream
    either way."""
    if os.name == "nt":
        # CreateProcess resolves a bare argv[0] only to .exe/.com — never the
        # PATHEXT script shims (.cmd/.bat) npm-style CLIs install on Windows —
        # while preflight's shutil.which honors PATHEXT, so a shim-only CLI
        # passes preflight then dies here with [WinError 2] (WI-120). Hand
        # CreateProcess the which-resolved path (an explicit .cmd runs fine);
        # a miss, or a .ps1-only resolution (no CreateProcess interposition),
        # falls through unchanged to the OSError sentinel below.
        resolved = shutil.which(argv[0], path=(env or os.environ).get("PATH"))
        if resolved and not resolved.lower().endswith(".ps1"):
            argv = [resolved] + argv[1:]

    # codex echoes its banner + the WHOLE prompt into stdout, so its own
    # --output-last-message file is the deterministic result (WI-217).
    argv, codex_lastmsg = _codex_lastmsg_setup(argv)

    try:
        _validate_prompt_transport(argv, stdin_input, env=env)
        proc = subprocess.Popen(
            argv,
            cwd=str(root),
            stdin=(subprocess.PIPE if stdin_input is not None else subprocess.DEVNULL),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            # POSIX: lead a new session/process group so a timeout or interrupt
            # can kill the WHOLE tree (killpg below) — CLI-spawned tool
            # subprocesses otherwise survive proc.kill() and keep editing the
            # worktree the coordinator hands to the next session (repo-review
            # 2026-07-21 H-2). Windows: taskkill /T walks the tree instead.
            start_new_session=(os.name != "nt"),
        )
    except (OSError, ValueError) as exc:
        _codex_lastmsg_read(codex_lastmsg)  # cleanup the (unused) last-message file
        return -1, "coordinator: session error: {}".format(exc), False
    # A reader thread pumps the pipe so the child can never block on a full
    # buffer while the main thread waits — the same shape subprocess.run uses
    # internally, opened up so each line can be echoed as it arrives.
    lines = []

    def _pump():
        for line in proc.stdout:
            lines.append(line)
            if on_line is not None:
                on_line(line)
        proc.stdout.close()

    pump = threading.Thread(target=_pump, daemon=True)
    pump.start()

    # Deliver the prompt on stdin from a DAEMON thread, then close so the child
    # sees EOF. Threaded (not inline) so a large prompt to a child that never
    # drains stdin cannot block the main thread before proc.wait's timeout — the
    # timeout still fires and kills the child, so the no-wedge invariant (SN-016)
    # holds. The stdout pump is already draining, so the reverse deadlock (child
    # writing before it finishes reading) can't happen either.
    def _feed():
        try:
            proc.stdin.write(stdin_input)
        except (OSError, ValueError):
            pass  # child exited early; its status is captured by wait() below
        finally:
            try:
                proc.stdin.close()
            except (OSError, ValueError):
                pass

    if stdin_input is not None:
        threading.Thread(target=_feed, daemon=True).start()
    try:
        proc.wait(timeout=timeout or None)
    except subprocess.TimeoutExpired:
        _kill_tree(proc)
        proc.wait()
        pump.join(5)
        _codex_lastmsg_read(
            codex_lastmsg
        )  # cleanup; a timed-out session has no usable result
        return (
            -1,
            "".join(lines)
            + "\ncoordinator: session timed out after {}s".format(timeout),
            True,
        )
    except (KeyboardInterrupt, SystemExit):
        # An interrupted coordinator must not leave a live agent tree editing
        # the worktree (start_new_session detaches the child from the terminal
        # group, so Ctrl+C no longer reaches it implicitly — kill explicitly).
        _kill_tree(proc)
        proc.wait()
        raise
    pump.join(5)
    output = "".join(lines)
    last = _codex_lastmsg_read(codex_lastmsg)
    if last and proc.returncode == 0:
        output = last  # codex: the deterministic last message, not the transcript
    return proc.returncode, output, False
