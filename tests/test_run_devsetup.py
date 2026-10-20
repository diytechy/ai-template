"""run checks the workstation first; dev-setup's check for run (WI-834 parts C, D).

A bare `run` (the double-click) runs dev-setup's check for run once, from the
repository root, before the menu, and stops with the step to take when the
runtime stays missing; `run <name>` and `run --list` never call it, never
prompt and never pause. dev-setup reports the retained adjudicator's sign-in
(signed in, missing or unknown) through the kit's own readers, offers nothing
without an interactive terminal, and changes nothing on a denial. Driven as
subprocesses: the launchers against a stub dev-setup in a scratch root, and
the shipped dev-setup on a bootstrapped scaffold. The consent prompts need a
terminal, so the denial cases run under a pseudo-terminal on POSIX only.
"""

import datetime
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import (
    KIT,
    ROOT,
    SCRIPTS,
    hooked_checkout,
    load_script,
    older_only_path,
    run_py,
    skip_without_env_gates,
    sub_floor_interpreter,
)

WINDOWS = os.name == "nt"
STACK = "[run]\nhello = echo menu-ran\nhello.desc = say it\n"


def _sh():
    skip_without_env_gates("posix-shell")
    return shutil.which("sh")


def _powershell():
    found = shutil.which("powershell") or shutil.which("pwsh")
    if not found:
        pytest.skip("needs PowerShell")
    return found


# A menu stub that reports the interpreter it actually runs on (the WI-475
# ENGINE-UNDER method): the observation the one-interpreter pins make.
MENU_STUB = 'import sys\nprint("MENU-UNDER", sys.executable)\n'


def _launcher_root(tmp_path, devsetup_exit=0, menu_stub=False):
    """A scratch root holding the shipped run launchers, the real menu (or,
    with `menu_stub`, MENU_STUB in its place), a declared [run] section, and a
    stub dev-setup that records each call (its arguments and working
    directory) and exits `devsetup_exit`."""
    root = tmp_path / "repo"
    (root / "scripts").mkdir(parents=True)
    (root / "docs").mkdir()
    (root / "docs" / "stack.ini").write_text(STACK, encoding="utf-8")
    for name in ("run.sh", "run.command", "run.cmd"):
        source = SCRIPTS / name.replace("run.", "run.template.")
        shutil.copyfile(source, root / name)
    shutil.copyfile(SCRIPTS / "run_menu.py", root / "scripts" / "run_menu.py")
    if menu_stub:
        (root / "scripts" / "run_menu.py").write_text(MENU_STUB, encoding="utf-8")
    shutil.copytree(SCRIPTS / "kitlib", root / "scripts" / "kitlib")
    (root / "scripts" / "dev-setup.sh").write_text(
        'echo "devsetup $* cwd=$(pwd)" >> trace.txt\nexit {}\n'.format(devsetup_exit),
        encoding="utf-8",
    )
    (root / "scripts" / "dev-setup.ps1").write_text(
        "Add-Content -Path trace.txt -Value ('devsetup ' + ($args -join ' ') + "
        "' cwd=' + (Get-Location).Path)\r\nexit {}\r\n".format(devsetup_exit),
        encoding="utf-8",
    )
    return root


def _trace(root):
    path = root / "trace.txt"
    return path.read_text(encoding="utf-8").splitlines() if path.exists() else []


def _run(argv, root, stdin=""):
    return subprocess.run(
        argv,
        cwd=str(root),
        input=stdin,
        capture_output=True,
        text=True,
        timeout=120,
    )


# --- the launchers: POSIX --------------------------------------------------------


@pytest.mark.parametrize("entry", ["run.sh", "run.command"])
def test_a_bare_run_calls_the_check_once_from_the_root_before_the_menu(tmp_path, entry):
    sh = _sh()
    root = _launcher_root(tmp_path)
    proc = _run([sh, entry], root, stdin="1\n")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    (call,) = _trace(root)  # once, the macOS delegation included
    assert call.startswith("devsetup --for-run --python ")
    assert Path(call.split("cwd=", 1)[1]).name == "repo"
    assert "menu-ran" in proc.stdout  # the menu ran after it, on the piped pick


def test_a_bare_run_stops_with_the_step_when_the_runtime_stays_missing(tmp_path):
    sh = _sh()
    root = _launcher_root(tmp_path, devsetup_exit=1)
    proc = _run([sh, "run.sh"], root, stdin="1\n")
    assert proc.returncode == 1
    assert "runtime is still missing" in proc.stderr
    assert "menu-ran" not in proc.stdout


@pytest.mark.parametrize("args", [["--list"], ["hello"]])
def test_the_direct_and_list_forms_never_call_the_check(tmp_path, args):
    sh = _sh()
    root = _launcher_root(tmp_path)
    proc = _run([sh, "run.sh", *args], root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _trace(root) == []


# --- the launchers: Windows ------------------------------------------------------


def _cmd(root, *args, stdin=""):
    return _run(["cmd", "/d", "/c", str(root / "run.cmd"), *args], root, stdin=stdin)


@pytest.mark.skipif(not WINDOWS, reason="run.cmd is the Windows launcher")
def test_a_bare_run_cmd_calls_the_check_once_from_the_root_before_the_menu(tmp_path):
    _powershell()
    root = _launcher_root(tmp_path)
    proc = _cmd(root, stdin="1\r\n\r\n")
    (call,) = _trace(root)
    assert call.startswith("devsetup -ForRun -Python ")
    assert Path(call.split("cwd=", 1)[1]).name == "repo"
    assert "menu-ran" in proc.stdout
    assert proc.stdout.index("Running:") > 0


@pytest.mark.skipif(not WINDOWS, reason="run.cmd is the Windows launcher")
def test_a_bare_run_cmd_stops_with_the_step_when_the_runtime_stays_missing(tmp_path):
    _powershell()
    root = _launcher_root(tmp_path, devsetup_exit=1)
    proc = _cmd(root, stdin="\r\n")
    assert proc.returncode == 1
    assert "runtime is still missing" in proc.stdout
    assert "menu-ran" not in proc.stdout


@pytest.mark.skipif(not WINDOWS, reason="run.cmd is the Windows launcher")
@pytest.mark.parametrize("args", [["--list"], ["hello"]])
def test_the_direct_and_list_forms_of_run_cmd_never_check_or_pause(tmp_path, args):
    root = _launcher_root(tmp_path)
    proc = _cmd(root, *args)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _trace(root) == []
    assert "Press any key" not in proc.stdout


# --- one interpreter: the readiness step's and the menu's (WI-834 r4, 012 F1) ----


def _handed(call, flag):
    """The interpreter a recorded dev-setup call was handed with `flag`, or ""
    when it was handed none."""
    head = call.split(" cwd=", 1)[0]
    return head.split(" " + flag + " ", 1)[1] if (" " + flag + " ") in head else ""


def _menu_under(stdout):
    lines = [x for x in stdout.splitlines() if x.startswith("MENU-UNDER ")]
    return lines[0].split(" ", 1)[1].strip() if lines else ""


def _same_file(a, b):
    return os.path.normcase(os.path.realpath(a)) == os.path.normcase(
        os.path.realpath(b)
    )


def _passes_the_floor(interpreter):
    floor = "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"
    return subprocess.run([interpreter, "-c", floor]).returncode == 0


@pytest.mark.parametrize("entry", ["run.sh", "run.command", "run.cmd"])
def test_a_bare_run_hands_the_check_the_interpreter_its_menu_runs_on(tmp_path, entry):
    """The launcher's one resolution: the readiness step is handed the
    interpreter whose floor it checks, and the menu runs on exactly that
    interpreter. Deterministic on every host: the host's own 3.11+ is what
    gets resolved, and the menu stub reports where it really ran."""
    root = _launcher_root(tmp_path, menu_stub=True)
    if entry == "run.cmd":
        if not WINDOWS:
            pytest.skip("run.cmd is the Windows launcher")
        _powershell()
        argv, flag, stdin = ["cmd", "/d", "/c", str(root / entry)], "-Python", "\r\n"
    else:
        argv, flag, stdin = [_sh(), entry], "--python", ""
    proc = _run(argv, root, stdin=stdin)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    (call,) = _trace(root)
    handed = _handed(call, flag)
    ran_on = _menu_under(proc.stdout)
    assert handed, "the readiness step was handed no interpreter: " + call
    assert ran_on, proc.stdout + proc.stderr
    assert _same_file(handed, ran_on), (handed, ran_on)
    assert _passes_the_floor(ran_on)


def _sub_floor_path(tmp_path):
    """PATH with only sub-floor candidates first: the WI-475 fakes (the real
    interpreter with only `sys.version_info` spoofed, running the launcher's
    own probe string), so the floor is the only thing that can reject them."""
    from test_launcher_interpreter import OLD, _write_fake_bin

    fake = _write_fake_bin(tmp_path / "bin", OLD, "OLD")
    return str(fake) + os.pathsep + os.environ.get("PATH", "")


@pytest.mark.parametrize("args", [[], ["--list"], ["hello"]])
@pytest.mark.parametrize("entry", ["run.sh", "run.cmd"])
def test_no_form_of_run_starts_the_menu_below_the_floor(tmp_path, entry, args):
    """With only sub-floor interpreters to find, no form starts the menu:
    the bare form hands the readiness step no interpreter (and so ends with
    its step), and the direct and list forms exit 1 naming the floor, without
    the readiness step."""
    root = _launcher_root(tmp_path, devsetup_exit=1, menu_stub=True)
    if entry == "run.cmd":
        if not WINDOWS:
            pytest.skip("run.cmd is the Windows launcher")
        argv, flag = ["cmd", "/d", "/c", str(root / entry)], "-Python"
    else:
        argv, flag = [_sh(), entry], "--python"
    env = dict(os.environ, PATH=_sub_floor_path(tmp_path))
    env.pop("VIRTUAL_ENV", None)
    proc = subprocess.run(
        argv + args,
        cwd=str(root),
        env=env,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=180,
    )
    out = proc.stdout + proc.stderr
    assert proc.returncode != 0, out
    assert "MENU-UNDER" not in out and "FAKE-OLD ran" not in out, out
    if args:
        assert _trace(root) == [], out
        assert "3.11" in out, out
    else:
        (call,) = _trace(root)
        assert _handed(call, flag) == "", call


# Each run launcher beside the dev-setup whose runtime search it must match.
SEARCH_PAIRS = [
    (ROOT / "run.cmd", ROOT / "scripts" / "dev-setup.ps1"),
    (ROOT / "run.sh", ROOT / "scripts" / "dev-setup.sh"),
    # This repo's relaunch launchers run kit Python too (round 016 F2, D-019).
    (ROOT / "scripts" / "coordinator-relaunch.cmd", ROOT / "scripts" / "dev-setup.ps1"),
    (ROOT / "scripts" / "coordinator-relaunch.sh", ROOT / "scripts" / "dev-setup.sh"),
    (SCRIPTS / "run.template.cmd", SCRIPTS / "dev-setup.template.ps1"),
    (SCRIPTS / "run.template.sh", SCRIPTS / "dev-setup.template.sh"),
    # The shipped git hooks run kit Python on one floor-resolved interpreter
    # too, through the one probe they all source (WI-880); git runs them
    # through sh on every platform.
    (KIT / "hooks" / "kit-python.sh", SCRIPTS / "dev-setup.template.sh"),
]


def _launcher_search(path):
    """The launcher's resolution candidates after its .venv entries, in order:
    the quoted items of run.cmd's `for %%C in (...)`, or the words of
    run.sh's `for cand in ...; do`."""
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".cmd":
        (items,) = re.findall(r"(?m)^for %%C in \((.*?)\) do ", text)
        found = re.findall(r'"([^"]*)"', items)
    else:
        (items,) = re.findall(r"(?m)^\s*for cand in (.*?); do$", text)
        found = items.split()
    return [c for c in found if not c.startswith(".venv")]


def _devsetup_search(path):
    """dev-setup's own runtime search, in order: `$PyCandidates` (plain or
    nested arrays, a nested one read as its words) or `PY_CANDIDATES`."""
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix == ".ps1":
        (cell,) = re.findall(r"(?m)^\s*\$PyCandidates = @\((.*)\)\s*$", text)
        groups = re.findall(r"@\(([^()]*)\)", cell)
        if not groups:  # a flat list of single command names
            return re.findall(r'"([^"]*)"', cell)
        return [" ".join(re.findall(r'"([^"]*)"', g)) for g in groups]
    (cell,) = re.findall(r'(?m)^PY_CANDIDATES="([^"]*)"$', text)
    return cell.split()


@pytest.mark.parametrize(
    "launcher,devsetup",
    SEARCH_PAIRS,
    ids=[p[0].name + ":" + p[0].parent.name for p in SEARCH_PAIRS],
)
def test_each_run_launcher_searches_what_its_dev_setup_searches(launcher, devsetup):
    """Whenever a dev-setup check reports a runtime, its run launcher resolves
    one: after the .venv entries, the launcher probes the same interpreters, in
    the same order, as that dev-setup's own runtime search."""
    ours = _launcher_search(launcher)
    theirs = _devsetup_search(devsetup)
    assert theirs, devsetup
    assert ours == theirs, (launcher.name, ours, devsetup.name, theirs)


def test_an_installed_hook_denies_with_an_older_python_first(scaffold_root, tmp_path):
    """Real interpreters only (round 016 F2): the hook the real opt-in
    installs, run as Claude Code runs it (its command line through a shell)
    with a real Python below the floor first on PATH, runs on its bound
    interpreter on any day: exit 0, no traceback. When the real clock is
    inside the window it arms (judged by the guard's own window reader, the
    window being weekday-only), it denies a new subagent; outside it, it
    prints no decision. Skipped where no such Python exists."""
    older = sub_floor_interpreter()
    if older is None:
        pytest.skip("no Python below 3.11 is installed on this host")
    shell = _sh()
    root = tmp_path / "scaffold"
    shutil.copytree(scaffold_root, root, ignore=shutil.ignore_patterns(".git"))
    example = root / ".claude" / "settings.json.example"
    example.parent.mkdir(exist_ok=True)
    shutil.copyfile(KIT / "agent-hooks" / "claude.settings.json", example)
    now = datetime.datetime.now(datetime.timezone.utc)
    window = "{:%H:%M}-{:%H:%M}".format(
        now - datetime.timedelta(hours=1), now + datetime.timedelta(hours=1)
    )
    toml = root / "docs" / "process.toml"
    text = re.sub(
        r'(?m)^blackout = ".*"$',
        'blackout = "{}"'.format(window),
        toml.read_text(encoding="utf-8"),
    )
    toml.write_text(text, encoding="utf-8")
    # The write a yes leads to, bound to this interpreter.
    assert (
        load_script("coordinator_guard").guard_hooks.install_hooks(root, example).word
        == "on"
    )
    local = json.loads((root / ".claude" / "settings.local.json").read_text("utf-8"))
    (group,) = local["hooks"]["PreToolUse"]  # only the guard's group is installed
    command = group["hooks"][0]["command"]
    payload = {
        "hook_event_name": "PreToolUse",
        "session_id": "c0c0c0c0-0000-4000-8000-0000000000b1",
        "cwd": str(root),
        "tool_name": "Agent",
        "tool_input": {"prompt": "x"},
    }
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(root))
    env["PATH"] = os.path.dirname(older) + os.pathsep + env["PATH"]
    env.pop("VIRTUAL_ENV", None)
    proc = subprocess.run(
        [shell, "-c", command],
        input=json.dumps(payload),
        cwd=str(root),
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stderr
    assert "Traceback" not in proc.stderr, proc.stderr
    assert "ModuleNotFoundError" not in proc.stderr, proc.stderr
    armed = load_script("agent_common").blackout_at(root / "docs").end is not None
    if armed:
        spec = json.loads(proc.stdout)["hookSpecificOutput"]
        assert spec["permissionDecision"] == "deny"
    else:  # a weekend: the window this test arms is not in force
        assert "permissionDecision" not in proc.stdout, proc.stdout


def _emitted_guard_commands(guard, root, tmp_path):
    """The guard command lines the drain instruction tells the session to run,
    as the real hook emits them at a latch, each paired with the shells it is
    written for, its arguments swapped for `status`."""
    session = "c0c0c0c0-0000-4000-8000-0000000000b1"
    (root / "docs").mkdir(parents=True)
    (root / "docs" / "process.toml").write_text(
        "[coordinator]\ncontext_guard_pct = 50\ncontext_window_tokens = 1000\n",
        encoding="utf-8",
    )
    usage = {"input_tokens": 600, "cache_creation_input_tokens": 0}
    usage.update(cache_read_input_tokens=0, output_tokens=5)
    record = {"parentUuid": None, "isSidechain": False, "uuid": "u-1"}
    record.update(sessionId=session, type="assistant")
    record["message"] = {"role": "assistant", "model": "m", "usage": usage}
    transcript = tmp_path / "coord.jsonl"
    transcript.write_text(json.dumps(record) + "\n", encoding="utf-8")
    hooked_checkout(root)  # the take refuses a checkout without hooks
    assert guard.take(root, session, str(transcript)) is None
    payload = {"hook_event_name": "PostToolUse", "session_id": session}
    payload.update(cwd=str(root), transcript_path=str(transcript))
    text = guard.hook(payload, root, env={})["hookSpecificOutput"]["additionalContext"]
    args = "request-relaunch --handoff <path>"
    spans = [x for x in re.findall(r"`([^`]+)`", text) if args in x]
    assert spans, text
    lines = [x.replace(args, "status") for x in spans]
    if len(lines) == 1:
        return [(lines[0], "bash"), (lines[0], "powershell")]
    return [(x, "powershell" if x.startswith("& ") else "bash") for x in lines]


def _spaced_interpreter(tmp_path):
    """This interpreter reached through a link, whose name holds a space, to
    its installation (a junction on Windows; the whole prefix, so a virtual
    environment still finds its configuration), so the quoted forms run."""
    prefix = Path(sys.prefix)
    link = tmp_path / "py dir"
    if WINDOWS:
        made = subprocess.run(
            ["cmd", "/d", "/c", "mklink", "/J", str(link), str(prefix)],
            capture_output=True,
            text=True,
        )
        assert made.returncode == 0, made.stdout + made.stderr
    else:
        link.symlink_to(prefix, target_is_directory=True)
    return str(link / Path(sys.executable).relative_to(prefix))


def test_the_injected_guard_command_names_the_hooks_own_interpreter(
    tmp_path, monkeypatch
):
    """The drain instruction tells the session to run the guard on the
    interpreter the hook itself runs on (round 016 F2, D-019), never a bare
    `python`, in text that runs as typed in each supported shell, from any
    working directory (round 035 F1): each emitted line, run in the shell it
    is written for (PowerShell, and POSIX sh through its declared gate) from a
    directory outside the repository, exits 0. Both the plain form and, for
    an interpreter path holding a space, the quoted Bash and PowerShell forms."""
    guard = load_script("coordinator_guard")
    ran = []
    try:
        _run_each_emitted_line(guard, tmp_path, monkeypatch, ran)
    finally:
        link = tmp_path / "py dir"
        if os.path.lexists(link):  # the link only, never its target
            os.rmdir(link) if WINDOWS else link.unlink()
    assert ("plain", "bash") in ran and ("spaced", "bash") in ran, ran
    if WINDOWS:
        assert ("plain", "powershell") in ran and ("spaced", "powershell") in ran


def _run_each_emitted_line(guard, tmp_path, monkeypatch, ran):
    """Run each emitted guard line in its shell from outside the repository,
    for this interpreter and for it reached through a spaced path."""
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    for case, interpreter in (("plain", sys.executable), ("spaced", None)):
        if interpreter is None:
            interpreter = _spaced_interpreter(tmp_path)
        monkeypatch.setattr(sys, "executable", interpreter)
        root = tmp_path / case / "repo"
        env = dict(os.environ, CLAUDE_PROJECT_DIR=str(root))
        for line, shell in _emitted_guard_commands(guard, root, tmp_path / case):
            assert Path(interpreter).as_posix() in line, line
            if shell == "powershell" and not WINDOWS:
                continue
            argv = (
                [_powershell(), "-NoProfile", "-Command", line]
                if shell == "powershell"
                else [_sh(), "-c", line]
            )
            proc = subprocess.run(
                argv,
                cwd=str(elsewhere),
                env=env,
                capture_output=True,
                text=True,
                timeout=120,
            )
            assert proc.returncode == 0, (shell, line, proc.stdout + proc.stderr)
            assert '"lease"' in proc.stdout, (shell, line, proc.stdout)
            ran.append((case, shell))


def test_a_scaffold_keeps_the_machine_local_settings_out_of_git(scaffold_root):
    """The opt-in's file names this machine's interpreter, so the scaffold's
    ignore list keeps it out of every commit."""
    lines = (scaffold_root / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert ".claude/settings.local.json" in lines


# --- dev-setup's check for run, on a scaffold ---------------------------------------


@pytest.fixture(scope="module")
def scaffold_root(tmp_path_factory):
    dest = tmp_path_factory.mktemp("scaffold")
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", dest], cwd=dest)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    with (dest / "docs" / "stack.ini").open("a", encoding="utf-8") as handle:
        handle.write("\n" + STACK)
    return dest


def _retention(root, pct):
    path = root / "docs" / "process.toml"
    text = path.read_text(encoding="utf-8")
    head, tail = text.split("context_reset_pct = ", 1)
    tail = tail.split("\n", 1)[1]
    path.write_text(
        head + "context_reset_pct = {}\n".format(pct) + tail, encoding="utf-8"
    )


def _devsetup_env(**extra):
    env = os.environ.copy()
    env.pop("AGENT_CLAUDE_TOKEN_FILE", None)
    env.pop("CI", None)  # a CI host would read as no terminal
    env.update(extra)
    return env


def _signin_line(stdout):
    lines = [x for x in stdout.splitlines() if "retained adjudicator sign-in" in x]
    return lines[0] if lines else ""


def test_the_check_for_run_offers_nothing_without_a_terminal(scaffold_root):
    sh = _sh()
    proc = subprocess.run(
        [sh, "scripts/dev-setup.sh", "--for-run", "--python", sys.executable],
        cwd=str(scaffold_root),
        input="y\ny\ny\n",
        capture_output=True,
        text=True,
        env=_devsetup_env(),
        timeout=120,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "nothing is offered" in proc.stdout
    assert "[y/N]" not in proc.stdout


@pytest.mark.parametrize("family", ["sh", "ps1"])
def test_the_check_for_run_checks_only_the_interpreter_it_is_handed(
    scaffold_root, family
):
    """The readiness operation keeps no interpreter search of its own: handed
    none, it reports the runtime missing and exits 1 although a 3.11+ (this
    one) is on PATH; handed this interpreter, it reports it ready and exits 0.
    Its result therefore speaks for the interpreter the launcher runs."""
    if family == "sh":
        argv, flag = [_sh(), "scripts/dev-setup.sh", "--for-run"], "--python"
    elif WINDOWS:
        argv = [_powershell(), "-NoProfile", "-ExecutionPolicy", "Bypass"]
        argv, flag = argv + ["-File", "scripts/dev-setup.ps1", "-ForRun"], "-Python"
    else:
        pytest.skip("the PowerShell dev-setup on Windows")
    here = os.path.dirname(sys.executable)
    env = _devsetup_env(PATH=here + os.pathsep + os.environ.get("PATH", ""))
    results = {}
    for handed in ([], [flag, sys.executable]):
        proc = subprocess.run(
            argv + handed,
            cwd=str(scaffold_root),
            capture_output=True,
            text=True,
            input="",
            env=env,
            timeout=180,
        )
        results[bool(handed)] = (proc.returncode, proc.stdout + proc.stderr)
    code, out = results[False]
    assert code == 1, out
    assert "[missing] runtime" in out and "still missing" in out, out
    code, out = results[True]
    assert code == 0, out
    assert "[ok]      runtime" in out, out


def test_piped_menu_input_survives_the_check(scaffold_root):
    sh = _sh()
    proc = subprocess.run(
        [sh, "run.sh"],
        cwd=str(scaffold_root),
        input="1\n",
        capture_output=True,
        text=True,
        env=_devsetup_env(),
        timeout=120,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "nothing is offered" in proc.stdout
    assert "menu-ran" in proc.stdout


def test_the_sign_in_is_reported_signed_in_missing_or_off(scaffold_root, tmp_path):
    sh = _sh()

    def check(**env):
        proc = subprocess.run(
            [sh, "scripts/dev-setup.sh", "--check"],
            cwd=str(scaffold_root),
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            env=_devsetup_env(**env),
            timeout=120,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        return _signin_line(proc.stdout)

    assert check() == ""  # retention off (the shipped dial): no step at all
    _retention(scaffold_root, 55)
    try:
        assert "[missing]" in check()
        token = tmp_path / "token"
        token.write_text("canary", encoding="utf-8")
        assert "[ok]" in check(AGENT_CLAUDE_TOKEN_FILE=str(token))
    finally:
        _retention(scaffold_root, 0)


CANARY = "sk-ant-oat01-CANARY-834-never-shown"  # a fake token shaped like a real one; privacy-ok


@pytest.mark.parametrize("family", ["sh", "ps1"])
def test_the_sign_in_report_never_prints_or_stores_the_token(
    scaffold_root, tmp_path, family
):
    """Signed in, the report names the token's variable and never its value:
    the canary is in neither stream nor in any file under the repository."""
    if family == "sh":
        argv = [_sh(), "scripts/dev-setup.sh", "--check"]
    elif WINDOWS:
        argv = [_powershell(), "-NoProfile", "-ExecutionPolicy", "Bypass"]
        argv += ["-File", "scripts/dev-setup.ps1", "-Check"]
    else:
        pytest.skip("the PowerShell dev-setup on Windows")
    token = tmp_path / "token"
    token.write_text(CANARY + "\n", encoding="utf-8")
    _retention(scaffold_root, 55)
    try:
        proc = subprocess.run(
            argv,
            cwd=str(scaffold_root),
            capture_output=True,
            text=True,
            input="",
            env=_devsetup_env(AGENT_CLAUDE_TOKEN_FILE=str(token)),
            timeout=180,
        )
    finally:
        _retention(scaffold_root, 0)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "[ok]" in _signin_line(proc.stdout)
    assert CANARY not in proc.stdout + proc.stderr
    stored = [
        p
        for p in scaffold_root.rglob("*")
        if p.is_file() and CANARY.encode() in p.read_bytes()
    ]
    assert stored == []


@pytest.mark.skipif(WINDOWS, reason="fake interpreters are POSIX shell scripts")
def test_the_sign_in_reads_unknown_without_a_runtime(scaffold_root, tmp_path):
    sh = _sh()
    fakebin = tmp_path / "fakebin"
    fakebin.mkdir()
    for name in ("python", "python3"):
        fake = fakebin / name
        fake.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        fake.chmod(0o755)
    path = str(fakebin) + os.pathsep + os.environ.get("PATH", "")
    proc = subprocess.run(
        [sh, "scripts/dev-setup.sh", "--check"],
        cwd=str(scaffold_root),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        env=_devsetup_env(PATH=path),
        timeout=120,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "[unknown]" in _signin_line(proc.stdout)  # the rest still ran
    assert "component(s) missing" in proc.stdout


def _path_without_git():
    """A real static PATH with this interpreter's directory and the Windows
    system directories (cmd, PowerShell) and no Git: a workstation that has a
    runtime but no Git (round 024 F2). No fake executable."""
    system = os.environ.get("SystemRoot", r"C:\Windows")
    dirs = [os.path.dirname(sys.executable), os.path.join(system, "System32")]
    dirs += [os.path.join(system, "System32", "WindowsPowerShell", "v1.0"), system]
    path = os.pathsep.join(dirs)
    assert shutil.which("git", path=path) is None, path
    return path


def _without_git(argv, cwd, stdin):
    env = {k: v for k, v in os.environ.items() if k.upper() not in ("PATH", "CI")}
    env["PATH"] = _path_without_git()
    env.pop("VIRTUAL_ENV", None)
    proc = subprocess.run(
        argv,
        cwd=str(cwd),
        env=env,
        input=stdin,
        capture_output=True,
        text=True,
        timeout=300,
    )
    return proc.returncode, proc.stdout + proc.stderr


@pytest.mark.skipif(not WINDOWS, reason="the PowerShell dev-setup on Windows")
def test_without_git_the_check_reports_it_missing_and_the_run_reaches_its_menu(
    scaffold_root,
):
    """Round 024 F2: with a working runtime and no Git, the shipped readiness
    operation reports git missing and still returns the runtime result, the
    standalone check still exits 0, and a bare run reaches its menu."""
    shell = [_powershell(), "-NoProfile", "-ExecutionPolicy", "Bypass", "-File"]
    devsetup = shell + ["scripts/dev-setup.ps1"]
    code, out = _without_git(
        devsetup + ["-ForRun", "-Python", sys.executable], scaffold_root, ""
    )
    assert code == 0 and "[missing] git" in out, out
    code, out = _without_git(devsetup + ["-Check"], scaffold_root, "")
    assert code == 0 and "[missing] git" in out, out
    run = ["cmd", "/d", "/c", str(scaffold_root / "run.cmd")]
    code, out = _without_git(run, scaffold_root, "1\r\n\r\n")
    assert code == 0 and "menu-ran" in out, out


@pytest.mark.skipif(not WINDOWS, reason="the PowerShell dev-setup on Windows")
def test_without_git_this_repos_check_and_run_still_work():
    """The same for this repository's own dev-setup and actions menu."""
    shell = [_powershell(), "-NoProfile", "-ExecutionPolicy", "Bypass", "-File"]
    code, out = _without_git(shell + ["scripts/dev-setup.ps1", "-Check"], ROOT, "")
    assert code == 0 and "[missing] git" in out, out
    run = ["cmd", "/d", "/c", str(ROOT / "run.cmd")]
    code, out = _without_git(run, ROOT, "q\r\n\r\n")
    assert "[missing] git" in out and "trajectory" in out, out  # the menu


@pytest.mark.skipif(not WINDOWS, reason="the PowerShell dev-setup on Windows")
def test_the_powershell_check_reports_the_sign_in(scaffold_root, tmp_path):
    shell = _powershell()

    def check(**env):
        proc = subprocess.run(
            [
                shell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                "scripts/dev-setup.ps1",
                "-ForRun",
                "-Python",
                sys.executable,
            ],
            cwd=str(scaffold_root),
            capture_output=True,
            text=True,
            input="",
            env=_devsetup_env(**env),
            timeout=180,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        assert "nothing is offered" in proc.stdout
        return _signin_line(proc.stdout)

    assert check() == ""
    _retention(scaffold_root, 55)
    try:
        assert "[missing]" in check()
        token = tmp_path / "token"
        token.write_text("canary", encoding="utf-8")
        assert "[ok]" in check(AGENT_CLAUDE_TOKEN_FILE=str(token))
    finally:
        _retention(scaffold_root, 0)


@pytest.mark.skipif(WINDOWS, reason="a consent prompt needs a pseudo-terminal")
def test_a_denial_changes_no_configuration_or_credential(scaffold_root, tmp_path):
    """At a terminal every offer is declined: the hooks stay off, the token
    variable and git configuration are untouched."""
    import pty

    sh = _sh()
    example = scaffold_root / ".claude" / "settings.json.example"
    example.parent.mkdir(exist_ok=True)
    shutil.copyfile(KIT / "agent-hooks" / "claude.settings.json", example)
    before = subprocess.run(
        ["git", "config", "--list", "--local"],
        cwd=str(scaffold_root),
        capture_output=True,
        text=True,
    ).stdout
    _retention(scaffold_root, 55)
    fake = _with_fake_claude(tmp_path)
    master, slave = pty.openpty()
    try:
        proc = subprocess.Popen(
            [sh, "scripts/dev-setup.sh", "--for-run", "--python", sys.executable],
            cwd=str(scaffold_root),
            stdin=slave,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=_devsetup_env(PATH=fake),
        )
        os.write(master, b"n\n" * 20)
        out, _ = proc.communicate(timeout=180)
    finally:
        os.close(master)
        os.close(slave)
        _retention(scaffold_root, 0)
    text = out.decode("utf-8", "replace")
    assert "setup-token" in text and "skipped the token step" in text
    assert "skipped the coordinator hooks" in text
    assert not (scaffold_root / ".claude" / "settings.json").exists()
    assert not (scaffold_root / ".claude" / "settings.local.json").exists()
    # Nothing was recorded, so the next run asks again.
    code, again = _at_a_terminal(
        scaffold_root, ["--for-run", "--python", sys.executable], b"n\n" * 20, fake
    )
    assert code == 0, again
    assert "Write the coordinator's Claude Code hooks" in again, again
    assert "skipped the coordinator hooks" in again, again
    assert not (scaffold_root / ".claude" / "settings.local.json").exists()
    after = subprocess.run(
        ["git", "config", "--list", "--local"],
        cwd=str(scaffold_root),
        capture_output=True,
        text=True,
    ).stdout
    assert after == before
    assert not (tmp_path / "claude-ran").exists()


def _at_a_terminal(root, args, answers, path=None):
    """dev-setup.sh run with a pseudo-terminal on stdin (and CI unset), fed
    `answers`; returns its exit code and combined output."""
    import pty

    env = _devsetup_env(**({"PATH": path} if path else {}))
    env.pop("CI", None)
    master, slave = pty.openpty()
    try:
        proc = subprocess.Popen(
            [_sh(), "scripts/dev-setup.sh", *args],
            cwd=str(root),
            stdin=slave,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
        )
        os.write(master, answers)
        out, _ = proc.communicate(timeout=180)
    finally:
        os.close(master)
        os.close(slave)
    return proc.returncode, out.decode("utf-8", "replace")


@pytest.mark.skipif(WINDOWS, reason="a consent prompt needs a pseudo-terminal")
def test_at_a_terminal_each_missing_item_is_offered_consent_first(
    scaffold_root, tmp_path
):
    """The bare run's check, at a terminal: a missing role is reported, then
    its install is offered, and the install runs only on a yes."""
    root = tmp_path / "repo"
    (root / "scripts").mkdir(parents=True)
    marker = tmp_path / "installed"
    text = (scaffold_root / "scripts" / "dev-setup.sh").read_text(encoding="utf-8")
    text = text.replace('design_CMDS="inkscape"', 'design_CMDS="no-such-tool-834"')
    text = text.replace(
        'design_INSTALL=""', "design_INSTALL=\"touch '{}'\"".format(marker)
    )
    assert "no-such-tool-834" in text and str(marker) in text
    (root / "scripts" / "dev-setup.sh").write_text(text, encoding="utf-8")
    for answer, installed in ((b"n\n", False), (b"y\n", True)):
        code, out = _at_a_terminal(
            root, ["--for-run", "--python", sys.executable], answer + b"n\n" * 20
        )
        assert code == 0, out
        offer = out.index('Install role: design via "touch')
        assert out.index("[missing] role: design") < offer
        assert "[y/N]" in out[offer:]
        assert marker.exists() == installed, out


@pytest.mark.skipif(WINDOWS, reason="a consent prompt needs a pseudo-terminal")
def test_the_standalone_check_at_a_terminal_offers_and_writes_nothing(
    scaffold_root, tmp_path
):
    """--check, even at a terminal with the sign-in step and the hooks both
    offerable: no prompt, no change to the repository or its git config, no
    `claude` run, exit 0. (The interpreter's __pycache__ is not the report's.)"""
    example = scaffold_root / ".claude" / "settings.json.example"
    example.parent.mkdir(exist_ok=True)
    shutil.copyfile(KIT / "agent-hooks" / "claude.settings.json", example)

    def tree():
        files = scaffold_root.rglob("*")
        return {
            p: p.read_bytes()
            for p in files
            if p.is_file() and "__pycache__" not in p.parts
        }

    _retention(scaffold_root, 55)
    try:
        before = tree()
        code, out = _at_a_terminal(
            scaffold_root, ["--check"], b"y\n" * 20, path=_with_fake_claude(tmp_path)
        )
        after = tree()
    finally:
        _retention(scaffold_root, 0)
    assert code == 0, out
    assert "[missing] retained adjudicator sign-in" in out  # offerable, not offered
    assert "[y/N]" not in out
    assert after == before  # the repository and its git config
    assert not (tmp_path / "claude-ran").exists()


# Types into a real console. Run as its own short-lived process (so no test
# worker's console is ever freed or attached), it waits for the child's ready
# marker, which the child writes from inside its console before it runs the
# script, so the console exists when the typist attaches; it then writes the
# answers to that console's input buffer as key events (WriteConsoleInputW),
# the keystrokes a person would type, which wait there for the prompt. A
# marker that never appears fails loudly.
CONSOLE_TYPIST = r"""
import ctypes, os, sys, time
from ctypes import wintypes
pid, answers, ready = int(sys.argv[1]), sys.argv[2], sys.argv[3]
deadline = time.monotonic() + 60
while not os.path.exists(ready):
    if time.monotonic() > deadline:
        raise SystemExit("the child never wrote its ready marker: " + ready)
    time.sleep(0.05)
k = ctypes.WinDLL("kernel32", use_last_error=True)
k.FreeConsole()
if not k.AttachConsole(pid):
    raise SystemExit("AttachConsole failed: %d" % ctypes.get_last_error())
k.CreateFileW.restype = wintypes.HANDLE
conin = k.CreateFileW("CONIN$", 0xC0000000, 3, None, 3, 0, None)
class Key(ctypes.Structure):
    _fields_ = [("down", wintypes.BOOL), ("repeat", wintypes.WORD),
                ("vk", wintypes.WORD), ("scan", wintypes.WORD),
                ("char", wintypes.WCHAR), ("state", wintypes.DWORD)]
class Record(ctypes.Structure):
    _fields_ = [("kind", wintypes.WORD), ("pad", wintypes.WORD), ("key", Key)]
keys = [Record(1, 0, Key(down, 1, 0x0D if ch == "\r" else 0, 0, ch, 0))
        for ch in answers for down in (1, 0)]
written = wintypes.DWORD()
if not k.WriteConsoleInputW(conin, (Record * len(keys))(*keys), len(keys),
                            ctypes.byref(written)):
    raise SystemExit("WriteConsoleInputW failed: %d" % ctypes.get_last_error())
"""


def _at_a_console(script, args, answers, path, tmp_path):
    """A PowerShell script run in a new, real (hidden) Windows console, its
    input not redirected, with `answers` typed into that console; returns its
    exit code and its output. Skips when the host gives the console no
    interactive session (the script would offer nothing)."""
    out, ready = tmp_path / "console-out.txt", tmp_path / "console-ready"
    for stale in (out, ready):
        if stale.exists():
            stale.unlink()
    command = (
        "$env:PATH = '{path}'; Remove-Item Env:CI -ErrorAction SilentlyContinue; "
        "'interactive=' + ([Environment]::UserInteractive -and "
        "-not [Console]::IsInputRedirected) | Out-File -Encoding utf8 '{out}'; "
        "New-Item -ItemType File '{ready}' | Out-Null; "
        "& '{script}' {args} *>&1 | Out-File -Append -Width 4096 -Encoding utf8 "
        "'{out}'; exit $LASTEXITCODE"
    ).format(path=path, out=out, ready=ready, script=script, args=" ".join(args))
    hidden = subprocess.STARTUPINFO()
    hidden.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    hidden.wShowWindow = 0
    proc = subprocess.Popen(
        [
            _powershell(),
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            command,
        ],
        cwd=str(tmp_path),
        creationflags=subprocess.CREATE_NEW_CONSOLE,
        startupinfo=hidden,
    )
    try:
        typed = subprocess.run(
            [sys.executable, "-c", CONSOLE_TYPIST, str(proc.pid), answers, str(ready)],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW,
            timeout=120,
        )
        assert typed.returncode == 0, typed.stdout + typed.stderr
        code = proc.wait(timeout=180)
    finally:
        if proc.poll() is None:
            proc.kill()
    text = out.read_text(encoding="utf-8-sig") if out.exists() else ""
    if "interactive=True" not in text:
        pytest.skip("this host gives a new console no interactive session")
    return code, text


@pytest.mark.skipif(not WINDOWS, reason="a real Windows console")
@pytest.mark.parametrize("family", ["root", "template"])
def test_at_a_windows_console_the_missing_runtime_is_offered_consent_first(
    tmp_path, family
):
    """Round 032 F1: each Windows readiness operation, at an interactive
    console and handed no interpreter, offers the missing runtime
    consent-first through the install it declares; a decline runs nothing, an
    accept runs it, and either way the result is still the handed
    interpreter's (exit 1, the step to run again)."""
    root = tmp_path / "repo"
    (root / "scripts").mkdir(parents=True)
    marker = tmp_path / "runtime-installed"
    path = os.environ.get("PATH", "")
    if family == "root":
        shutil.copyfile(
            ROOT / "scripts" / "dev-setup.ps1", root / "scripts" / "dev-setup.ps1"
        )
        fakebin = tmp_path / "provisioner"
        fakebin.mkdir()
        (fakebin / "uv.cmd").write_text(
            '@echo off\r\necho %* > "{}"\r\n'.format(marker), encoding="utf-8"
        )
        path = str(fakebin) + os.pathsep + path
        skipped = "Skipped - install Python 3.11+ your own way"
    else:
        text = (SCRIPTS / "dev-setup.template.ps1").read_text(encoding="utf-8-sig")
        filled = "$RuntimeInstall = \"New-Item -ItemType File '{}'\"".format(marker)
        text = text.replace('$RuntimeInstall = ""', filled, 1)
        assert filled in text
        (root / "scripts" / "dev-setup.ps1").write_text(text, encoding="utf-8-sig")
        skipped = "- skipped runtime"
    script = root / "scripts" / "dev-setup.ps1"
    for answer, installed in (("n", False), ("y", True)):
        code, out = _at_a_console(
            script, ["-ForRun"], answer + "\r" + "n\r" * 20, path, tmp_path
        )
        assert code == 1, out
        assert "[missing] runtime" in out and "then run again" in out, out
        assert marker.exists() == installed, out
        assert (skipped in out) != installed, out


@pytest.mark.skipif(not WINDOWS, reason="a real Windows console")
def test_at_a_windows_console_install_offers_the_missing_runtime(tmp_path):
    """WI-880: this repository's `dev-setup.ps1 -Install` offers a missing
    runtime where `dev-setup.sh --install` does, consent-first through the
    provisioner it declares, then searches again. Real interpreters only: a
    real Python below the floor is the only one on PATH. A decline runs
    nothing, an accept runs the provisioner, and with still no 3.11+ found
    either way ends with the step (exit 1)."""
    older = sub_floor_interpreter()
    if older is None:
        pytest.skip("no Python below 3.11 is installed on this host")
    root = tmp_path / "repo"
    (root / "scripts").mkdir(parents=True)
    shutil.copyfile(
        ROOT / "scripts" / "dev-setup.ps1", root / "scripts" / "dev-setup.ps1"
    )
    marker = tmp_path / "runtime-installed"
    fakebin = tmp_path / "provisioner"
    fakebin.mkdir()
    (fakebin / "uv.cmd").write_text(
        '@echo off\r\necho %* > "{}"\r\n'.format(marker), encoding="utf-8"
    )
    path = older_only_path(older, fakebin)
    script = root / "scripts" / "dev-setup.ps1"
    for answer, installed in (("n", False), ("y", True)):
        code, out = _at_a_console(
            script, ["-Install"], answer + "\r" + "n\r" * 20, path, tmp_path
        )
        assert code == 1, out
        assert "[missing] runtime" in out, out
        assert marker.exists() == installed, out
        assert ("Skipped - install Python 3.11+" in out) != installed, out
        assert "Python 3.11+ not found" in out, out


@pytest.mark.parametrize("family", ["sh", "ps1"])
def test_this_repos_readiness_report_names_the_hooks_opt_in(family):
    """WI-880 (owner ruling 2026-10-10): this repository commits no guard
    hooks, so a machine runs them only after the machine-local opt-in, and
    dev-setup's readiness report says which state this machine is in."""
    if family == "sh":
        argv = [_sh(), "scripts/dev-setup.sh", "--check"]
    elif WINDOWS:
        argv = [_powershell(), "-NoProfile", "-ExecutionPolicy", "Bypass"]
        argv += ["-File", "scripts/dev-setup.ps1", "-Check"]
    else:
        pytest.skip("the PowerShell dev-setup on Windows")
    proc = subprocess.run(
        argv,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        input="",
        env=_devsetup_env(),
        timeout=180,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    lines = [
        x for x in proc.stdout.splitlines() if "coordinator Claude Code hooks" in x
    ]
    assert len(lines) == 1, proc.stdout
    if "[missing]" in lines[0]:  # occupied: the fix follows the line
        assert "move those hooks to another settings file" in proc.stdout
    else:
        assert "[ok]" in lines[0] or "offered by" in lines[0], lines[0]


def _with_fake_claude(tmp_path):
    """A `claude` on PATH that records any run, so a denial is shown to run
    nothing."""
    fakebin = tmp_path / "claudebin"
    fakebin.mkdir()
    fake = fakebin / "claude"
    fake.write_text(
        "#!/bin/sh\ntouch '{}'\n".format(tmp_path / "claude-ran"), encoding="utf-8"
    )
    fake.chmod(0o755)
    return str(fakebin) + os.pathsep + os.environ.get("PATH", "")


def test_the_hooks_command_reports_each_state_and_writes_nothing(tmp_path):
    """The read-only report, as a subprocess: absent (no file is created),
    on, occupied (exit 1, the event named on stderr) and none; the file's
    bytes never change across report runs."""
    root = tmp_path / "repo"
    (root / ".claude").mkdir(parents=True)
    example = root / ".claude" / "settings.json.example"
    shutil.copyfile(KIT / "agent-hooks" / "claude.settings.json", example)
    local = root / ".claude" / "settings.local.json"

    def hooks(source=example):
        proc = run_py(
            [SCRIPTS / "coordinator_guard.py", "--root", root, "hooks"]
            + ["--example", source],
            cwd=root,
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr

    assert hooks()[:2] == (0, "absent")
    assert not local.exists()
    assert (
        load_script("coordinator_guard").guard_hooks.install_hooks(root, example).word
        == "on"
    )
    before = local.read_bytes()
    assert hooks()[:2] == (0, "on")
    assert local.read_bytes() == before
    settings = json.loads(before)
    settings["hooks"]["Stop"].append({"hooks": [{"command": "echo mine"}]})
    local.write_text(json.dumps(settings), encoding="utf-8")
    before = local.read_bytes()
    code, word, err = hooks()
    assert (code, word) == (1, "occupied")
    assert "Stop" in err and "echo mine" in err, err
    plain = tmp_path / "plain.example"
    plain.write_text('{"hooks": {"Stop": [{"hooks": [{"command": "x"}]}]}}', "utf-8")
    assert hooks(plain)[:2] == (0, "none")
    assert local.read_bytes() == before
    assert not (root / ".claude" / "settings.json").exists()


# The stand-in hooks reader of a dev-setup copy: one that fails with an
# error, and one that exits 0 printing nothing.
FAILING_READERS = {
    "fails": "import sys\nsys.stderr.write('boom-927\\n')\nsys.exit(1)\n",
    "silent": "",
}
# Each dev-setup copy: (its source, where its hooks reader lives, its check).
DEVSETUP_COPIES = {
    "template-sh": ("scaffold", "scripts/dev-setup.sh", "scripts", "--check"),
    "template-ps1": ("scaffold", "scripts/dev-setup.ps1", "scripts", "-Check"),
    "root-sh": (
        "root",
        "scripts/dev-setup.sh",
        "project-trajectory/scripts",
        "--check",
    ),
    "root-ps1": (
        "root",
        "scripts/dev-setup.ps1",
        "project-trajectory/scripts",
        "-Check",
    ),
}


def _python_shims(tmp_path):
    """A PATH whose first directory runs this interpreter as `python3` and
    `python`, so each copy's runtime search finds a floor-passing one."""
    shims = tmp_path / "shims"
    shims.mkdir(exist_ok=True)
    for name in ("python3", "python"):
        shim = shims / name
        shim.write_text(
            '#!/bin/sh\nexec "{}" "$@"\n'.format(Path(sys.executable).as_posix()),
            encoding="utf-8",
        )
        shim.chmod(0o755)
        (shims / (name + ".cmd")).write_text(
            '@"{}" %*\r\n'.format(sys.executable), encoding="utf-8"
        )
    return str(shims) + os.pathsep + os.environ.get("PATH", "")


def _check_copy(scaffold_root, tmp_path, copy, reader):
    """Run one dev-setup copy's check in a scratch tree whose hooks reader is
    `reader`'s source; returns its stdout."""
    source, script, readers, flag = DEVSETUP_COPIES[copy]
    if script.endswith(".ps1"):
        if not WINDOWS:
            pytest.skip("the PowerShell dev-setup on Windows")
        argv = [_powershell(), "-NoProfile", "-ExecutionPolicy", "Bypass", "-File"]
    else:
        argv = [_sh()]
    root = tmp_path / "repo"
    for directory in (readers, "scripts", ".claude"):
        (root / directory).mkdir(parents=True, exist_ok=True)
    shutil.copyfile(
        KIT / "agent-hooks" / "claude.settings.json",
        root / ".claude" / "settings.json.example",
    )
    origin = scaffold_root if source == "scaffold" else ROOT
    shutil.copyfile(origin / script, root / script)
    (root / readers / "coordinator_guard.py").write_text(reader, encoding="utf-8")
    proc = subprocess.run(
        argv + [script, flag],
        cwd=str(root),
        capture_output=True,
        text=True,
        input="",
        env=_devsetup_env(PATH=_python_shims(tmp_path)),
        timeout=180,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _missing_count(out):
    found = re.search(r"(\d+) component\(s\) missing", out)
    return int(found.group(1)) if found else None


@pytest.mark.parametrize("reader", list(FAILING_READERS))
@pytest.mark.parametrize("copy", list(DEVSETUP_COPIES))
def test_a_failing_or_silent_hooks_reader_is_reported_missing_never_none(
    scaffold_root, tmp_path, copy, reader
):
    """A hooks reader that exits non-zero, or exits 0 printing nothing, is one
    `[missing]` line naming its error (or that it printed nothing), counted
    with the other missing components where the copy counts them; it is never
    read as none, which prints no line."""
    out = _check_copy(scaffold_root, tmp_path, copy, FAILING_READERS[reader])
    lines = [x for x in out.splitlines() if "coordinator Claude Code hooks" in x]
    assert len(lines) == 1, out
    assert lines[0].lstrip().startswith("[missing]"), lines[0]
    named = "boom-927" if reader == "fails" else "printed nothing"
    assert named in lines[0], lines[0]
    counted = _missing_count(out)
    if counted is not None:
        on = _check_copy(scaffold_root, tmp_path, copy, "print('on')\n")
        assert counted == _missing_count(on) + 1, (out, on)


def _hooks_scaffold(scaffold_root, dest, settings=None):
    """A copy of the scaffold at `dest` with the kit's example in place and
    the machine-local settings `settings` (None: no file; a str: its text)."""
    shutil.copytree(
        scaffold_root, dest, ignore=shutil.ignore_patterns(".git"), dirs_exist_ok=True
    )
    example = dest / ".claude" / "settings.json.example"
    example.parent.mkdir(exist_ok=True)
    shutil.copyfile(KIT / "agent-hooks" / "claude.settings.json", example)
    local = dest / ".claude" / "settings.local.json"
    if local.exists():
        local.unlink()
    if settings is not None:
        text = settings if isinstance(settings, str) else json.dumps(settings)
        local.write_text(text, encoding="utf-8")
    return local


ABSENT_SETTINGS = {
    "no file": None,
    "an empty object": {},
    "permissions only": {"permissions": {"allow": ["Bash(git status)"]}},
}
GUARD_EVENTS = {
    "SessionStart",
    "UserPromptSubmit",
    "PreToolUse",
    "PostToolUse",
    "PostToolUseFailure",
    "Stop",
    "PreCompact",
    "SessionEnd",
}


def _assert_installed(local, before, out):
    """Every guard event holds one group bound to this interpreter, and the
    keys that were there before are kept."""
    assert "Switched on the coordinator hooks" in out, out
    settings = json.loads(local.read_text(encoding="utf-8"))
    assert set(settings["hooks"]) == GUARD_EVENTS, settings
    bound = '"{}" '.format(Path(sys.executable).as_posix())
    for event in GUARD_EVENTS:
        ((entry,),) = [group["hooks"] for group in settings["hooks"][event]]
        assert entry["command"].startswith(bound), entry
    assert settings.get("permissions") == (before or {}).get("permissions")


@pytest.mark.skipif(WINDOWS, reason="a consent prompt needs a pseudo-terminal")
@pytest.mark.parametrize("before", list(ABSENT_SETTINGS))
def test_at_a_terminal_a_yes_installs_every_guard_group_keeping_other_keys(
    scaffold_root, tmp_path, before
):
    """The bare run's offer at a terminal: a yes writes every guard group,
    bound to the handed interpreter, keeping every other key."""
    root = tmp_path / "scaffold"
    local = _hooks_scaffold(scaffold_root, root, ABSENT_SETTINGS[before])
    code, out = _at_a_terminal(
        root, ["--for-run", "--python", sys.executable], b"y\n" + b"n\n" * 20
    )
    assert code == 0, out
    assert "Write the coordinator's Claude Code hooks" in out, out
    _assert_installed(local, ABSENT_SETTINGS[before], out)


ASKED = b"Write the coordinator's Claude Code hooks"


def _read_until(master, wanted, seconds):
    """Everything the terminal `master` shows until `wanted` appears, end of
    output, or `seconds` pass."""
    import select
    import time

    seen, end = b"", time.monotonic() + seconds
    while wanted not in seen and time.monotonic() < end:
        ready, _, _ = select.select([master], [], [], 0.2)
        if not ready:
            continue
        try:
            chunk = os.read(master, 4096)
        except OSError:  # the child closed the terminal
            break
        if not chunk:
            break
        seen += chunk
    return seen


def _on_one_terminal(argv, cwd, env, answers):
    """`argv` run with stdin, stdout and stderr all on one pseudo-terminal, as
    a person runs it. Returns what the terminal showed before the consent
    question's answer was typed, its exit code, and the whole output; the
    answers are typed only once the question is on the terminal."""
    import pty

    master, slave = pty.openpty()
    proc = subprocess.Popen(
        argv, cwd=str(cwd), stdin=slave, stdout=slave, stderr=slave, env=env
    )
    os.close(slave)
    try:
        before = _read_until(master, ASKED, 120)
        if ASKED in before:
            os.write(master, answers)
        after = _read_until(master, b"\0never\0", 60) if ASKED in before else b""
        if proc.poll() is None:
            proc.kill()
        code = proc.wait(timeout=60)
    finally:
        os.close(master)
    return (
        before.decode("utf-8", "replace"),
        code,
        (before + after).decode("utf-8", "replace"),
    )


@pytest.mark.skipif(WINDOWS, reason="a real terminal needs a pseudo-terminal")
def test_at_a_real_terminal_the_offer_shows_its_question_before_the_answer(
    scaffold_root, tmp_path
):
    """The bare run's offer with every stream on the terminal: the consent
    question is on the screen before anything is typed, and the yes then
    installs."""
    root = tmp_path / "scaffold"
    local = _hooks_scaffold(scaffold_root, root)
    before, code, out = _on_one_terminal(
        [_sh(), "scripts/dev-setup.sh", "--for-run", "--python", sys.executable],
        root,
        _devsetup_env(),
        b"y\n" + b"n\n" * 20,
    )
    assert ASKED.decode() in before, out
    assert code == 0, out
    _assert_installed(local, None, out)


@pytest.mark.skipif(WINDOWS, reason="a real terminal needs a pseudo-terminal")
def test_at_a_real_terminal_the_take_shows_its_question_before_the_answer(tmp_path):
    """The lease take with every stream on the terminal: the consent question
    is on the screen before anything is typed, and the yes then takes."""
    root, local = _take_root(tmp_path, "y")
    before, code, out = _on_one_terminal(
        [sys.executable, str(SCRIPTS / "coordinator_guard.py"), "--root", str(root)]
        + ["take", "--session", TAKER],
        root,
        _devsetup_env(),
        b"y\n",
    )
    assert ASKED.decode() in before, out
    _assert_taken(root, local, "y", code, out)


@pytest.mark.skipif(not WINDOWS, reason="a real Windows console")
@pytest.mark.parametrize("before", list(ABSENT_SETTINGS))
@pytest.mark.parametrize("family", ["root", "template"])
def test_at_a_windows_console_a_yes_installs_every_guard_group_keeping_other_keys(
    scaffold_root, tmp_path, family, before
):
    """The same offer through each Windows dev-setup at a real console."""
    script, local, path = _console_tree(
        scaffold_root, tmp_path, family, ABSENT_SETTINGS[before]
    )
    args = ["-ForRun", "-Python", "'{}'".format(sys.executable)]
    code, out = _at_a_console(script, args, "y\r" + "n\r" * 20, path, tmp_path)
    assert code == 0, out
    _assert_installed(local, ABSENT_SETTINGS[before], out)


def _console_tree(scaffold_root, tmp_path, family, settings):
    """A tree for one Windows dev-setup family holding the kit's example and
    the machine-local `settings` (None: no file); returns its dev-setup.ps1,
    the settings path, and a PATH on which both agent CLIs are present, so
    neither is offered."""
    fakebin = tmp_path / "clis"
    fakebin.mkdir()
    for cli in ("claude", "codex"):
        (fakebin / (cli + ".cmd")).write_text("@echo off\r\n", encoding="utf-8")
    path = str(fakebin) + os.pathsep + os.environ.get("PATH", "")
    if family == "root":
        tree = tmp_path / "repo"
        (tree / "scripts").mkdir(parents=True)
        shutil.copyfile(
            ROOT / "scripts" / "dev-setup.ps1", tree / "scripts" / "dev-setup.ps1"
        )
        shutil.copytree(
            SCRIPTS,
            tree / "project-trajectory" / "scripts",
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        local = tree / ".claude" / "settings.local.json"
        (tree / ".claude").mkdir(exist_ok=True)
        shutil.copyfile(
            KIT / "agent-hooks" / "claude.settings.json",
            tree / ".claude" / "settings.json.example",
        )
        if settings is not None:
            local.write_text(json.dumps(settings), encoding="utf-8")
    else:  # the template runs from its working directory, the console's
        tree = tmp_path
        local = _hooks_scaffold(scaffold_root, tree, settings)
    return tree / "scripts" / "dev-setup.ps1", local, path


def _assert_failed_install_named(local, before, out):
    """The offer's `[missing]` line names the settings file, the error and
    the fix, and the file keeps its bytes."""
    lines = [x for x in out.splitlines() if "[missing] coordinator Claude Code" in x]
    assert len(lines) == 1, out
    for part in ("settings.local.json", "could not be written", "move or repair"):
        assert part in lines[0], lines[0]
    assert local.read_bytes() == before


@pytest.mark.skipif(not WINDOWS, reason="a real Windows console")
@pytest.mark.parametrize("family", ["root", "template"])
def test_at_a_windows_console_a_failed_install_names_the_file_error_and_fix(
    scaffold_root, tmp_path, family
):
    """A yes whose write fails (a read-only settings file) leaves the file as
    it was, and the offer's `[missing]` line says what to do."""
    import stat

    script, local, path = _console_tree(
        scaffold_root, tmp_path, family, ABSENT_SETTINGS["permissions only"]
    )
    before = local.read_bytes()
    os.chmod(local, stat.S_IREAD)
    try:
        args = ["-ForRun", "-Python", "'{}'".format(sys.executable)]
        code, out = _at_a_console(script, args, "y\r" + "n\r" * 20, path, tmp_path)
    finally:
        os.chmod(local, stat.S_IREAD | stat.S_IWRITE)
    assert code == 0, out
    _assert_failed_install_named(local, before, out)


@pytest.mark.skipif(WINDOWS, reason="a real terminal needs a pseudo-terminal")
@pytest.mark.skipif(
    hasattr(os, "geteuid") and os.geteuid() == 0, reason="root writes anywhere"
)
def test_at_a_real_terminal_a_failed_install_names_the_file_error_and_fix(
    scaffold_root, tmp_path
):
    """The sh offer, with a yes whose write fails (the settings folder is
    read-only): the file keeps its bytes and the `[missing]` line says what
    to do."""
    import stat

    root = tmp_path / "scaffold"
    local = _hooks_scaffold(scaffold_root, root, ABSENT_SETTINGS["permissions only"])
    before = local.read_bytes()
    os.chmod(local.parent, stat.S_IREAD | stat.S_IEXEC)
    try:
        _asked, code, out = _on_one_terminal(
            [_sh(), "scripts/dev-setup.sh", "--for-run", "--python", sys.executable],
            root,
            _devsetup_env(),
            b"y\n" + b"n\n" * 20,
        )
    finally:
        os.chmod(local.parent, stat.S_IRWXU)
    assert code == 0, out
    _assert_failed_install_named(local, before, out)


TAKER = "c0c0c0c0-0000-4000-8000-0000000009a7"


def _take_root(tmp_path, answer):
    """A scratch repository holding the kit's example and no machine-local
    settings, one per answer; returns it and its settings path."""
    # the take refuses a checkout without hooks
    root = hooked_checkout(tmp_path / ("repo-" + answer))
    (root / ".claude").mkdir(parents=True)
    shutil.copyfile(
        KIT / "agent-hooks" / "claude.settings.json",
        root / ".claude" / "settings.json.example",
    )
    return root, root / ".claude" / "settings.local.json"


def _assert_taken(root, local, answer, code, out):
    """A yes installs the hooks and takes the lease; a no refuses, writing
    and recording nothing."""
    guard = load_script("coordinator_guard")
    holder = guard._load(guard.lease_dir(root)).get("holder")
    assert "Write the coordinator's Claude Code hooks" in out, out
    if answer == "y":
        assert code == 0, out
        assert holder == TAKER
        example = root / ".claude" / "settings.json.example"
        assert guard.guard_hooks.hooks_state(root, example).word == "on"
    else:
        assert code == 1, out
        assert holder is None and not local.exists(), out


@pytest.mark.skipif(WINDOWS, reason="a consent prompt needs a pseudo-terminal")
@pytest.mark.parametrize("answer", ["y", "n"])
def test_the_cli_take_at_a_pseudo_terminal_asks_and_installs(tmp_path, answer):
    import pty

    root, local = _take_root(tmp_path, answer)
    env = _devsetup_env()
    master, slave = pty.openpty()
    try:
        proc = subprocess.Popen(
            [sys.executable, str(SCRIPTS / "coordinator_guard.py"), "--root", str(root)]
            + ["take", "--session", TAKER],
            cwd=str(root),
            stdin=slave,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
        )
        os.write(master, (answer + "\n").encode("ascii"))
        out, _ = proc.communicate(timeout=120)
    finally:
        os.close(master)
        os.close(slave)
    _assert_taken(root, local, answer, proc.returncode, out.decode("utf-8", "replace"))


@pytest.mark.skipif(not WINDOWS, reason="a real Windows console")
@pytest.mark.parametrize("answer", ["y", "n"])
def test_the_cli_take_at_a_windows_console_asks_and_installs(tmp_path, answer):
    root, local = _take_root(tmp_path, answer)
    args = ["'{}'".format(SCRIPTS / "coordinator_guard.py"), "--root"]
    args += ["'{}'".format(root), "take", "--session", TAKER]
    code, out = _at_a_console(
        sys.executable, args, answer + "\r", os.environ.get("PATH", ""), tmp_path
    )
    _assert_taken(root, local, answer, code, out)


@pytest.mark.skipif(WINDOWS, reason="a consent prompt needs a pseudo-terminal")
def test_an_on_file_is_unchanged_and_not_offered_at_a_terminal(scaffold_root, tmp_path):
    """A file already holding the guard's groups by name is never offered,
    asked about or rewritten."""
    root = tmp_path / "scaffold"
    local = _hooks_scaffold(scaffold_root, root)
    guard = load_script("coordinator_guard")
    assert (
        guard.guard_hooks.install_hooks(
            root, root / ".claude" / "settings.json.example"
        ).word
        == "on"
    )
    before = local.read_bytes()
    code, out = _at_a_terminal(
        root, ["--for-run", "--python", sys.executable], b"n\n" * 20
    )
    assert code == 0, out
    assert "Write the coordinator's" not in out, out
    assert "[ok]      coordinator Claude Code hooks" in out, out
    assert local.read_bytes() == before


def _occupied(shape):
    """The machine-local settings text of one occupied shape over the kit's
    example: the example's own bare-`python` guard groups, changed."""
    example = json.loads(
        (KIT / "agent-hooks" / "claude.settings.json").read_text(encoding="utf-8")
    )
    groups = load_script("coordinator_guard").guard_hooks.guard_groups(example)
    settings = {"hooks": json.loads(json.dumps(groups))}
    hooks = settings["hooks"]
    if shape == "mixed":
        hooks["PreToolUse"][0]["hooks"].insert(0, {"command": "echo user-927"})
        return json.dumps(settings), ("PreToolUse", "echo user-927")
    if shape == "second group":
        hooks["Stop"].append({"hooks": [{"command": "echo user-927"}]})
        return json.dumps(settings), ("Stop", "echo user-927")
    if shape == "missing event":
        del hooks["SessionEnd"]
        return json.dumps(settings), ("SessionEnd", "missing")
    return "{not json", ("does not parse",)


OCCUPIED_SHAPES = ["mixed", "second group", "missing event", "unparseable"]


@pytest.mark.parametrize("shape", OCCUPIED_SHAPES)
def test_an_occupied_slot_is_reported_and_never_offered(scaffold_root, tmp_path, shape):
    """Occupied: the check reports one `[missing]` naming the events and
    commands in the way and the fix, writes nothing and goes on to its later
    sections; at a terminal, nothing is offered."""
    root = tmp_path / "scaffold"
    text, named = _occupied(shape)
    local = _hooks_scaffold(scaffold_root, root, text)
    before = local.read_bytes()
    runs = [[_sh(), "scripts/dev-setup.sh", "--check"]]
    if WINDOWS:
        runs.append(
            [_powershell(), "-NoProfile", "-ExecutionPolicy", "Bypass"]
            + ["-File", "scripts/dev-setup.ps1", "-Check"]
        )
    outs = []
    for argv in runs:
        proc = subprocess.run(
            argv,
            cwd=str(root),
            capture_output=True,
            text=True,
            input="",
            env=_devsetup_env(PATH=_python_shims(tmp_path)),
            timeout=180,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        outs.append(proc.stdout)
    if not WINDOWS:
        code, out = _at_a_terminal(
            root, ["--for-run", "--python", sys.executable], b"n\n" * 20
        )
        assert code == 0, out
        outs.append(out)
    for out in outs:
        lines = [x for x in out.splitlines() if "coordinator Claude Code hooks" in x]
        assert len(lines) == 1 and "[missing]" in lines[0], out
        tail = out[out.index(lines[0]) :]
        assert all(part in tail for part in named), out
        assert "move those hooks to another settings file" in tail, out
        assert "Write the coordinator's" not in out, out
        assert "Product toolchain" in tail, out
    assert local.read_bytes() == before


# --- this repo's own run: its actions menu after the check -----------------------


def test_this_repos_run_shows_its_menu_after_the_check():
    if WINDOWS:
        _powershell()
        argv = ["cmd", "/d", "/c", str(ROOT / "run.cmd")]
        stdin = "q\r\n\r\n"
    else:
        argv = [_sh(), "run.sh"]
        stdin = "q\n"
    proc = _run(argv, ROOT, stdin=stdin)
    out = proc.stdout
    assert "runtime (python" in out  # the check ran first ...
    assert out.index("runtime (python") < out.index("smoke")  # ... then the menu
    assert "trajectory" in out and "dashboard" in out
