"""run_menu.py — the run capability menu the run.* launchers delegate to (WI-067).

Exercises the script the way the launchers do: a real docs/stack.ini [run]
section in a temp cwd, driven no-arg (menu), by-name (direct), and --list (agent
surface). Commands are launched through the shell (shell=True in run_menu), so
these also cover Windows/POSIX quoting.
"""

import os
import subprocess
import sys

import pytest

from conftest import SCRIPTS, augment_env

# A capability that records its argv (to prove shell tokenization + passthrough).
ECHO_ARGS = (
    "import sys, pathlib\n"
    "pathlib.Path('args.txt').write_text(chr(10).join(sys.argv[1:]), encoding='utf-8')\n"
)

PY = '"{}"'.format(sys.executable)  # quoted: the interpreter path may hold spaces


def _run(args, cwd, stdin=None, timeout=60):
    """Invoke run_menu.py in `cwd`. `stdin=None` closes stdin (DEVNULL) so a
    would-be prompt can't hang; a string feeds the interactive menu a pick."""
    kw = {"stdin": subprocess.DEVNULL} if stdin is None else {"input": stdin}
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "run_menu.py")] + args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",  # run_menu emits UTF-8; decode it as such, not the locale
        timeout=timeout,
        env=augment_env(dict(os.environ)),
        **kw,
    )


def _write_stack(cwd, run_body):
    """Write a docs/stack.ini carrying `run_body` under a [run] section (empty
    body = a present-but-empty section)."""
    ini = cwd / "docs" / "stack.ini"
    ini.parent.mkdir(parents=True, exist_ok=True)
    ini.write_text("[run]\n" + run_body, encoding="utf-8")


@pytest.fixture
def repo(tmp_path):
    """A cwd with the argv-recording helper; a [run] section with two
    capabilities (one with a .desc, one without)."""
    (tmp_path / "echo_args.py").write_text(ECHO_ARGS, encoding="utf-8")
    _write_stack(
        tmp_path,
        "serve = {py} echo_args.py served\n"
        "serve.desc = start the app\n"
        "build = {py} echo_args.py built\n".format(py=PY),
    )
    return tmp_path


def test_list_is_stable_name_tab_desc(repo):
    # --list is the agent surface: one `name<TAB>desc` line per capability in
    # declaration order; a capability with no .desc renders a trailing tab.
    proc = _run(["--list"], repo)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == "serve\tstart the app\nbuild\t\n"


def test_direct_launch_runs_command_and_passes_args(repo):
    # `run_menu.py <name>` runs that capability; trailing args pass through
    # (the old `exec $RUN_CMD "$@"` contract).
    proc = _run(["serve", "extra"], repo)
    assert proc.returncode == 0, proc.stderr
    args = (repo / "args.txt").read_text(encoding="utf-8").splitlines()
    assert args == ["served", "extra"]


def test_direct_launch_passes_exit_code(repo):
    # Exit-code passthrough: a nonzero from the launched command is the script's
    # exit code.
    _write_stack(repo, 'fail = {py} -c "import sys; sys.exit(7)"\n'.format(py=PY))
    proc = _run(["fail"], repo)
    assert proc.returncode == 7


def test_unknown_name_exits_2(repo):
    proc = _run(["nope"], repo)
    assert proc.returncode == 2
    assert "no capability named" in proc.stderr


def test_menu_launches_from_piped_stdin(repo):
    # No args = the numbered menu; feeding "1" selects the first capability and
    # runs it non-interactively.
    proc = _run([], repo, stdin="1\n")
    assert proc.returncode == 0, proc.stderr
    assert "1) serve" in proc.stdout
    assert "start the app" in proc.stdout  # the .desc renders in the menu
    assert "2) build" in proc.stdout
    assert (repo / "args.txt").read_text(encoding="utf-8").splitlines() == ["served"]


def test_menu_does_not_hang_on_closed_stdin(repo):
    # An unattended invocation (stdin closed) must exit, not block on the prompt.
    proc = _run([], repo)  # stdin=DEVNULL
    assert proc.returncode == 1
    assert "input closed" in proc.stderr


def test_menu_quit_is_clean(repo):
    proc = _run([], repo, stdin="q\n")
    assert proc.returncode == 0
    assert not (repo / "args.txt").exists()  # nothing launched


def test_absent_run_section_prints_guidance_and_exits_1(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "stack.ini").write_text(
        "[paths]\nsrc = src\n", encoding="utf-8"
    )
    proc = _run([], tmp_path)
    assert proc.returncode == 1
    assert "no run capabilities declared" in proc.stderr


def test_absent_stack_ini_prints_guidance_and_exits_1(tmp_path):
    proc = _run(["serve"], tmp_path)  # no docs/stack.ini at all
    assert proc.returncode == 1
    assert "no run capabilities declared" in proc.stderr


def test_list_on_empty_run_is_empty_and_exit_0(tmp_path):
    # The agent surface degrades to zero lines (not guidance prose on stdout).
    _write_stack(tmp_path, "")
    proc = _run(["--list"], tmp_path)
    assert proc.returncode == 0
    assert proc.stdout == ""


def test_shell_quoting_sanity(tmp_path):
    # A declared command with a quoted, space-bearing argument must reach the
    # program as one argv element on both cmd.exe and POSIX sh (shell=True).
    (tmp_path / "echo_args.py").write_text(ECHO_ARGS, encoding="utf-8")
    _write_stack(tmp_path, 'cap = {py} echo_args.py "a b" c\n'.format(py=PY))
    proc = _run(["cap"], tmp_path)
    assert proc.returncode == 0, proc.stderr
    assert (tmp_path / "args.txt").read_text(encoding="utf-8").splitlines() == [
        "a b",
        "c",
    ]


# WI-227: trailing args are DATA values, quoted per-platform so the shell
# delivers each whole (module docstring "Trailing arguments"). These run through
# the real platform shell (shell=True), so CI covers both cmd.exe and POSIX sh.
# Pre-fix (a bare `" ".join(extra)`) none of these reach the program intact — a
# space splits the value and a metacharacter executes or errors. The `"`-plus-
# separator rows are the review-18 regression: MSVCRT quoting alone left a `"` to
# end cmd.exe's quoted region early and re-expose the following `&`/`|`; the
# caret-escaping pass (_win_quote phase 2) keeps them literal on cmd.exe, and
# shlex.quote already did on POSIX.
@pytest.mark.parametrize(
    "arg",
    [
        "a b",  # a space must not split into two argv tokens
        "a&b",  # cmd.exe / sh command separator, kept literal
        "a|b",  # a pipe, kept literal
        "x && y",  # separators with surrounding spaces, one token
        'a"b',  # a literal double quote survives to the program
        'a"&b',  # a quote AND a separator together (cmd.exe quote-state gap)
        'a"|b',  # same, with a pipe
        'a"&b|c',  # a quote combined with BOTH separators in one value
        'a b"&c',  # quote+separator preceded by a space (both traps at once)
    ],
)
def test_trailing_data_arg_reaches_program_as_one_literal_token(repo, arg):
    proc = _run(["serve", arg], repo)
    assert proc.returncode == 0, proc.stderr
    args = (repo / "args.txt").read_text(encoding="utf-8").splitlines()
    assert args == ["served", arg]


@pytest.mark.skipif(
    os.name == "nt",
    reason="POSIX shlex.quote neutralizes shell expansion totally; cmd.exe %VAR% "
    "expansion is a documented Windows-only limit (run_menu module docstring)",
)
def test_trailing_arg_shell_expansion_is_neutralized_on_posix(repo):
    # The data-vs-fragment proof: a value that looks like shell expansion is
    # passed literally, never evaluated. Pre-fix each of these would expand or
    # run a subshell instead of reaching the program.
    proc = _run(["serve", "$HOME", "`id`", "$(echo hi)"], repo)
    assert proc.returncode == 0, proc.stderr
    args = (repo / "args.txt").read_text(encoding="utf-8").splitlines()
    assert args == ["served", "$HOME", "`id`", "$(echo hi)"]
