"""The launchers' interpreter SELECTION, executed (WI-475; repo-review 2026-08-19 H-01).

WHY THIS MODULE EXISTS. `test_bootstrap.py` already asserts that the root
`agent-resume.*` launchers ship inert with their EDIT slots — it reads launcher
TEXT. The review's finding is precisely what text-reading cannot see: on a box
where ambient `python` was 3.8.10 and a 3.11.9 `.venv` sat unused, the advertised
one-command entry point picked the ambient interpreter and the engine died at
`import tomllib`. Every launcher assertion in the suite passed. So this module
never greps a launcher; it RUNS one and observes which interpreter came out.

THE METHOD, and why it is not circular. A fake interpreter here is the REAL
python with `sys.version_info` SPOOFED, executing the launcher's own probe string
(`exec(sys.argv[1])`). That is what makes the tests measure the selection RULE
rather than a rehearsal of it: a launcher that probes only runnability (`-c ""`,
the pre-WI-475 behaviour) picks the fake and the below-floor tests go red, while
one that asks `sys.version_info` rejects it and says so. `test_the_fake_is
_runnable_and_only_its_version_is_fake` pins that discrimination directly, so a
green here can never come from a fake that was simply broken.

COVERAGE, and the one honest exception. Four launcher surfaces carry a probe —
the live root `agent-resume.{sh,cmd}` and their shipped `*.template.*` twins —
and each is driven through the same four cases (venv preferred, below-floor
refused, floor-satisfying PATH python taken, unusable venv falls back).
`agent-resume.command` carries NO probe: its whole body is `exec
./agent-resume.sh`, so the policy holds there by INHERITANCE. That is the one
launcher the "prefer the venv" rule reaches without a copy of its own — and it
is inheritance rather than a gap because the wrapper is executed here too, not
merely reasoned about.
"""

import os
import re
import shutil
import subprocess
import sys

import pytest

from conftest import KIT, ROOT, skip_without_env_gates

# The launcher families under test: the live root copy this repo runs on itself,
# and the template an adopter is scaffolded. `engine` is where each expects
# agent_loop.py to sit (the meta-repo self-application puts the kit under
# project-trajectory/), which is where the stub goes.
POSIX_LAUNCHERS = {
    "live": (ROOT / "agent-resume.sh", "project-trajectory/scripts/agent_loop.py"),
    "template": (
        KIT / "scripts" / "agent-resume.template.sh",
        "scripts/agent_loop.py",
    ),
}
CMD_LAUNCHERS = {
    "live": (ROOT / "agent-resume.cmd", "project-trajectory/scripts/agent_loop.py"),
    "template": (
        KIT / "scripts" / "agent-resume.template.cmd",
        "scripts/agent_loop.py",
    ),
}
COMMAND_WRAPPERS = {
    "live": (ROOT / "agent-resume.command", ROOT / "agent-resume.sh"),
    "template": (
        KIT / "scripts" / "agent-resume.template.command",
        KIT / "scripts" / "agent-resume.template.sh",
    ),
}

WINDOWS_ONLY = pytest.mark.skipif(
    sys.platform != "win32", reason="cmd.exe launcher: Windows only"
)

# The stub the launcher ends up running. It prints the interpreter that actually
# got there, which is the whole observation this module makes.
ENGINE_STUB = 'import sys\nprint("ENGINE-UNDER", sys.executable)\n'

# A fake interpreter, as a POSIX script and as the .cmd shim a Windows PATH
# python is often shaped like (pyenv-win ships exactly that shape). `{spoof}` is
# the version tuple it reports; everything else is the real interpreter, so the
# launcher's own probe string is what decides.
_FAKE_SH = """#!/bin/sh
if [ "$1" = "-c" ]; then
  exec "{real}" -c 'import sys; sys.version_info = {spoof}; exec(sys.argv[1])' "$2"
fi
echo "FAKE-{label} ran: $*"
exit 0
"""
_FAKE_CMD = """@echo off
if "%~1"=="-3" shift
if not "%~1"=="-c" goto notprobe
"{real}" -c "import sys; sys.version_info = {spoof}; exec(sys.argv[1])" %2
exit /b %ERRORLEVEL%
:notprobe
echo FAKE-{label} ran: %*
exit /b 0
"""

# Plain int tuples, deliberately: a real `sys.version_info` carries a
# releaselevel STRING, and its quotes cannot survive the single-quoted `-c`
# payload the POSIX fake passes through (an early version spoofed
# `(3, 8, 10, "final", 0)` and the shell ate the inner quotes, leaving the probe
# to die on a NameError that read as "not runnable"). Nothing under test reads
# anything but the ordered comparison, which a bare tuple answers identically.
OLD = (3, 8, 10)
NEW = (3, 12, 0)


def _write_shell_file(path, text, crlf=False):
    """Write a generated shell file with the line endings its kind really has.

    `Path.write_text` would translate to CRLF on Windows for everything, and a
    CRLF `#!/bin/sh` script is not executable at all — the trap the scaffolded
    `.gitattributes` documents, and one that made an early version of these tests
    report "not runnable here" for a perfectly good fake. The `.cmd` fakes go the
    other way (CRLF), because that is what `.gitattributes` declares for batch
    and what a Windows PATH shim actually looks like."""
    path.write_text(text, encoding="utf-8", newline="\r\n" if crlf else "\n")
    os.chmod(path, 0o755)


def _write_fake_bin(directory, spoof, label):
    """A PATH directory holding a fake `python`/`python3`/`py` in both the POSIX
    and the Windows-shim form, so the same directory serves an sh launcher and a
    cmd launcher. Returns the directory."""
    directory.mkdir(parents=True, exist_ok=True)
    real = sys.executable
    for name in ("python", "python3"):
        _write_shell_file(
            directory / name,
            _FAKE_SH.format(real=real.replace("\\", "/"), spoof=spoof, label=label),
        )
    for name in ("python.cmd", "python3.cmd", "py.cmd"):
        _write_shell_file(
            directory / name,
            _FAKE_CMD.format(real=real, spoof=spoof, label=label),
            crlf=True,
        )
    return directory


def _seed_agent_cmd(data):
    """Fill the launcher's AGENT_CMD slot the way `bootstrap.py --agents` does.

    On BYTES, and the `\\r?` is why: the launchers are copied verbatim (see
    `_install`), so a `.cmd` arrives with the CRLF `.gitattributes` declares for
    batch — the file kind whose own attributes comment warns that LF "can
    misparse labels/`goto`", which is exactly what the probe subroutine is made
    of. A str-mode rewrite would quietly normalise that away and test a file no
    adopter ever runs.

    The templates ship INERT (an empty slot prints guidance and exits), which is
    the behaviour `test_bootstrap.py` pins — so a template launcher never reaches
    its interpreter probe until an adopter has filled the slot. Seeding it here
    is what puts the code under test on the executed path."""
    data = re.sub(rb'(?m)^AGENT_CMD=""(\r?)$', rb'AGENT_CMD="stub-agent"\1', data)
    return re.sub(
        rb'(?m)^set "AGENT_CMD="(\r?)$', rb'set "AGENT_CMD=stub-agent"\1', data
    )


def _install(src, dest):
    """Copy a launcher BYTE FOR BYTE (bar the seeded slot) — see `_seed_agent_cmd`."""
    dest.write_bytes(_seed_agent_cmd(src.read_bytes()))
    os.chmod(dest, 0o755)
    return dest


def _repo(tmp_path, launcher, engine_rel, extra=()):
    """A throwaway repo holding one launcher, the engine stub it invokes, and any
    sibling files it delegates to. Returns the launcher's path in the repo."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    engine = tmp_path / engine_rel
    engine.parent.mkdir(parents=True, exist_ok=True)
    engine.write_text(ENGINE_STUB, encoding="utf-8")
    written = None
    for src in (launcher,) + tuple(extra):
        dest = _install(src, tmp_path / src.name.replace(".template", ""))
        written = written or dest
    return written


def _make_venv(root):
    """A REAL venv at `root/.venv` — this repo's own interpreter, which satisfies
    the floor by construction (the suite cannot run below it). `--without-pip`
    keeps it to ~0.2 s; nothing here imports a package."""
    subprocess.run(
        [sys.executable, "-m", "venv", "--without-pip", str(root / ".venv")],
        check=True,
        capture_output=True,
    )


def _run(argv, cwd, fake_bin):
    """Run a launcher with the fake interpreters FIRST on PATH.

    Prepended rather than substituted: the launchers legitimately use external
    tools (`dirname`), so an empty rest-of-PATH breaks them for reasons that have
    nothing to do with interpreter choice. Order is what makes the "nothing
    acceptable" case constructible on a provisioned machine — `python`,
    `python3` and `py` all resolve to a fake before the host's real ones."""
    env = dict(os.environ)
    env["PATH"] = str(fake_bin) + os.pathsep + env.get("PATH", "")
    env.pop("PYTHONHOME", None)
    return subprocess.run(
        argv,
        cwd=str(cwd),
        env=env,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,  # cmd.exe `pause` reads EOF and moves on
        timeout=180,
    )


def _run_sh(launcher, fake_bin):
    return _run([shutil.which("sh"), str(launcher)], launcher.parent, fake_bin)


def _run_cmd(launcher, fake_bin):
    comspec = os.environ.get("COMSPEC", "cmd.exe")
    return _run([comspec, "/c", str(launcher)], launcher.parent, fake_bin)


# --- the method's own guard ---------------------------------------------------


def test_the_fake_is_runnable_and_only_its_version_is_fake(tmp_path):
    """The fakes must be indistinguishable from a real interpreter EXCEPT in
    version, or every test below could be passing for the wrong reason (a broken
    fake is rejected as "not runnable" by a launcher that never checks a
    version). Both halves are asserted, and both fakes are driven."""
    old = _write_fake_bin(tmp_path / "old", OLD, "OLD")
    new = _write_fake_bin(tmp_path / "new", NEW, "NEW")
    floor = "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"
    # Whichever form THIS platform can execute directly: Windows cannot run the
    # extensionless POSIX script, and a POSIX box has no cmd.exe. The other
    # form's fidelity is pinned by the refusal tests, which assert the reason is
    # "older than", not "not runnable" — a broken fake fails them.
    windows = sys.platform == "win32"
    for directory, expected in ((old, 1), (new, 0)):
        for name in ["python.cmd"] if windows else ["python", "python3"]:
            argv = [str(directory / name)]
            if windows:
                argv = [os.environ.get("COMSPEC", "cmd.exe"), "/c"] + argv
            runs = subprocess.run(argv + ["-c", ""], capture_output=True)
            assert runs.returncode == 0, (
                "the fake must RUN — a fake that is merely broken would be "
                "rejected by a runnability probe and prove nothing about the "
                "version rule: " + str(runs.stderr)
            )
            probed = subprocess.run(argv + ["-c", floor], capture_output=True)
            assert probed.returncode == expected, (
                "%s answered the floor probe %r, expected %r"
                % (name, probed.returncode, expected)
            )


# --- POSIX: agent-resume.sh (live + template) ---------------------------------


@pytest.mark.parametrize("which", sorted(POSIX_LAUNCHERS))
def test_sh_prefers_the_project_venv_over_a_below_floor_ambient_python(which, tmp_path):
    """H-01 itself: a valid `.venv` beside a below-floor ambient `python`."""
    skip_without_env_gates("posix-shell")
    launcher, engine = POSIX_LAUNCHERS[which]
    path = _repo(tmp_path / "repo", launcher, engine)
    _make_venv(path.parent)
    done = _run_sh(path, _write_fake_bin(tmp_path / "bin", OLD, "OLD"))
    assert done.returncode == 0, done.stdout + done.stderr
    assert "ENGINE-UNDER" in done.stdout, done.stdout + done.stderr
    assert ".venv" in done.stdout.lower(), (
        "the engine ran, but not under the project venv: " + done.stdout
    )
    assert "FAKE-OLD" not in done.stdout


@pytest.mark.parametrize("which", sorted(POSIX_LAUNCHERS))
def test_sh_refuses_a_below_floor_interpreter_and_names_what_it_rejected(
    which, tmp_path
):
    """No venv, nothing on PATH above the floor: refuse, and say which candidates
    lost and why — the diagnostic the review asked for, since "not found" would
    be a lie about a python that is sitting right there."""
    skip_without_env_gates("posix-shell")
    launcher, engine = POSIX_LAUNCHERS[which]
    path = _repo(tmp_path / "repo", launcher, engine)
    done = _run_sh(path, _write_fake_bin(tmp_path / "bin", OLD, "OLD"))
    assert done.returncode != 0, done.stdout + done.stderr
    assert "ENGINE-UNDER" not in done.stdout, (
        "the engine was launched under a below-floor interpreter: " + done.stdout
    )
    message = done.stdout + done.stderr
    assert "3.11" in message, message
    assert "python3" in message and "older than" in message, (
        "the refusal must LIST the rejected candidates and why: " + message
    )


@pytest.mark.parametrize("which", sorted(POSIX_LAUNCHERS))
def test_sh_takes_a_path_python_that_satisfies_the_floor(which, tmp_path):
    """The other direction, without which the refusal above could be a launcher
    that simply never selects anything."""
    skip_without_env_gates("posix-shell")
    launcher, engine = POSIX_LAUNCHERS[which]
    path = _repo(tmp_path / "repo", launcher, engine)
    done = _run_sh(path, _write_fake_bin(tmp_path / "bin", NEW, "NEW"))
    assert done.returncode == 0, done.stdout + done.stderr
    assert "FAKE-NEW ran" in done.stdout, done.stdout + done.stderr


@pytest.mark.parametrize("which", sorted(POSIX_LAUNCHERS))
def test_sh_falls_back_when_the_venv_itself_is_below_the_floor(which, tmp_path):
    """The venv is PREFERRED, not exempt. A stale `.venv` built on an old python
    must lose to a good PATH python rather than wedge the launcher — otherwise
    "prefer the venv" trades one silent breakage for another."""
    skip_without_env_gates("posix-shell")
    launcher, engine = POSIX_LAUNCHERS[which]
    path = _repo(tmp_path / "repo", launcher, engine)
    stale = _write_fake_bin(path.parent / ".venv" / "bin", OLD, "STALE")
    assert (stale / "python").is_file()
    done = _run_sh(path, _write_fake_bin(tmp_path / "bin", NEW, "NEW"))
    assert done.returncode == 0, done.stdout + done.stderr
    assert "FAKE-NEW ran" in done.stdout, done.stdout + done.stderr
    assert "FAKE-STALE" not in done.stdout


# --- macOS: the .command wrapper inherits the policy --------------------------


@pytest.mark.parametrize("which", sorted(COMMAND_WRAPPERS))
def test_the_command_wrapper_inherits_the_venv_preference(which, tmp_path):
    """The launcher set's one exception, executed rather than asserted in prose:
    the Finder wrapper holds no probe because it `exec`s the .sh twin, so the
    same H-01 scenario must resolve the same way THROUGH it."""
    skip_without_env_gates("posix-shell")
    wrapper, twin = COMMAND_WRAPPERS[which]
    engine = POSIX_LAUNCHERS[which][1]
    path = _repo(tmp_path / "repo", wrapper, engine, extra=(twin,))
    _make_venv(path.parent)
    done = _run_sh(path, _write_fake_bin(tmp_path / "bin", OLD, "OLD"))
    assert done.returncode == 0, done.stdout + done.stderr
    assert ".venv" in done.stdout.lower(), done.stdout + done.stderr


@pytest.mark.parametrize("which", sorted(COMMAND_WRAPPERS))
def test_the_command_wrapper_declares_the_inheritance_and_holds_no_copy(which):
    """One home for the policy: the wrapper must not grow a probe of its own (a
    second copy is what drifts), and must SAY that it inherits one — a reader
    who finds no probe here has to be told where it lives."""
    wrapper, _ = COMMAND_WRAPPERS[which]
    text = wrapper.read_text(encoding="utf-8")
    assert "pick_py" not in text, "the wrapper carries a second copy of the probe"
    assert "agent-resume.sh" in text
    assert "venv" in text.lower(), (
        "the wrapper must name the policy it inherits, or its silence reads as "
        "an omission"
    )


# --- Windows: agent-resume.cmd (live + template) ------------------------------


@WINDOWS_ONLY
@pytest.mark.parametrize("which", sorted(CMD_LAUNCHERS))
def test_cmd_prefers_the_project_venv_over_a_below_floor_ambient_python(
    which, tmp_path
):
    launcher, engine = CMD_LAUNCHERS[which]
    path = _repo(tmp_path / "repo", launcher, engine)
    _make_venv(path.parent)
    done = _run_cmd(path, _write_fake_bin(tmp_path / "bin", OLD, "OLD"))
    assert done.returncode == 0, done.stdout + done.stderr
    assert "ENGINE-UNDER" in done.stdout, done.stdout + done.stderr
    assert ".venv" in done.stdout.lower(), (
        "the engine ran, but not under the project venv: " + done.stdout
    )
    assert "FAKE-OLD" not in done.stdout


@WINDOWS_ONLY
@pytest.mark.parametrize("which", sorted(CMD_LAUNCHERS))
def test_cmd_refuses_a_below_floor_interpreter_and_names_what_it_rejected(
    which, tmp_path
):
    launcher, engine = CMD_LAUNCHERS[which]
    path = _repo(tmp_path / "repo", launcher, engine)
    done = _run_cmd(path, _write_fake_bin(tmp_path / "bin", OLD, "OLD"))
    assert done.returncode != 0, done.stdout + done.stderr
    assert "ENGINE-UNDER" not in done.stdout, (
        "the engine was launched under a below-floor interpreter: " + done.stdout
    )
    message = done.stdout + done.stderr
    assert "3.11" in message, message
    assert "python" in message and "older than" in message, (
        "the refusal must LIST the rejected candidates and why: " + message
    )
    assert "py -3" in message, "the `py -3` candidate must be reported too: " + message


@WINDOWS_ONLY
@pytest.mark.parametrize("which", sorted(CMD_LAUNCHERS))
def test_cmd_takes_a_path_python_that_satisfies_the_floor(which, tmp_path):
    """Also the shim-transfer regression: the fakes are `.cmd` files, and without
    `call` cmd.exe hands control to such a shim and never returns — the launcher
    would exit silently instead of running the engine."""
    launcher, engine = CMD_LAUNCHERS[which]
    path = _repo(tmp_path / "repo", launcher, engine)
    done = _run_cmd(path, _write_fake_bin(tmp_path / "bin", NEW, "NEW"))
    assert done.returncode == 0, done.stdout + done.stderr
    assert "FAKE-NEW ran" in done.stdout, done.stdout + done.stderr


@WINDOWS_ONLY
@pytest.mark.parametrize("which", sorted(CMD_LAUNCHERS))
def test_cmd_falls_back_when_the_venv_is_present_but_unusable(which, tmp_path):
    """The Windows shape of "preferred, not exempt": a `.venv` whose python.exe
    exists but cannot execute (a stale or half-copied environment — the one an
    `if exist` test would happily select) falls back to a good PATH python."""
    launcher, engine = CMD_LAUNCHERS[which]
    path = _repo(tmp_path / "repo", launcher, engine)
    broken = path.parent / ".venv" / "Scripts"
    broken.mkdir(parents=True)
    (broken / "python.exe").write_text("not a real executable\n", encoding="utf-8")
    done = _run_cmd(path, _write_fake_bin(tmp_path / "bin", NEW, "NEW"))
    assert done.returncode == 0, done.stdout + done.stderr
    assert "FAKE-NEW ran" in done.stdout, done.stdout + done.stderr


@WINDOWS_ONLY
@pytest.mark.parametrize("which", sorted(CMD_LAUNCHERS))
def test_cmd_walks_past_an_alias_stub_to_the_py_launcher(which, tmp_path):
    """The two shapes only the Windows probe has, in one run: a candidate that
    EXISTS and runs nothing — the Microsoft-Store `python` alias stub, whose
    guard (repo-review 2026-07-21 M-16) this change had to keep — and `py -3`,
    the one candidate carrying a FLAG, which is where a batch subroutine's
    quoting goes wrong. Only `py` is a working fake here, so reaching the engine
    at all is proof both were handled."""
    launcher, engine = CMD_LAUNCHERS[which]
    path = _repo(tmp_path / "repo", launcher, engine)
    fake = _write_fake_bin(tmp_path / "bin", NEW, "NEW")
    for name in ("python.cmd", "python3.cmd"):
        # 9009 is what cmd.exe reports for a command it cannot run — the stub's
        # own answer, and deliberately NOT 1 (which would read as "too old").
        _write_shell_file(fake / name, "@echo off\nexit /b 9009\n", crlf=True)
    done = _run_cmd(path, fake)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "FAKE-NEW ran" in done.stdout, done.stdout + done.stderr


# --- the check.* launchers carry the same policy ------------------------------
# The review asked for it in the same breath as agent-resume, and for the same
# reason: `scripts/check.sh` / `check.ps1` are the harness's advertised entry
# point, check.py imports tomllib, and both already preferred `.venv` by mere
# EXISTENCE — which is the half of the rule that was never the problem.


def _check_repo(tmp_path):
    """A repo holding the kit's check launchers over a stub `check.py`, so what
    the test observes is which interpreter was selected, not a harness verdict."""
    scripts = tmp_path / "scripts"
    scripts.mkdir(parents=True)
    for name in ("check.sh", "check.ps1"):
        _install(KIT / "scripts" / name, scripts / name)
    (scripts / "check.py").write_text(ENGINE_STUB, encoding="utf-8")
    return scripts


@pytest.mark.parametrize("spoof,label", [(OLD, "OLD"), (NEW, "NEW")])
def test_check_sh_applies_the_same_floor(spoof, label, tmp_path):
    skip_without_env_gates("posix-shell")
    scripts = _check_repo(tmp_path / "repo")
    done = _run(
        [shutil.which("sh"), str(scripts / "check.sh")],
        scripts.parent,
        _write_fake_bin(tmp_path / "bin", spoof, label),
    )
    if label == "NEW":
        assert done.returncode == 0, done.stdout + done.stderr
        assert "FAKE-NEW ran" in done.stdout, done.stdout + done.stderr
    else:
        assert done.returncode != 0, done.stdout + done.stderr
        assert "older than Python 3.11" in done.stdout + done.stderr


@pytest.mark.parametrize("spoof,label", [(OLD, "OLD"), (NEW, "NEW")])
def test_check_ps1_applies_the_same_floor(spoof, label, tmp_path):
    """PowerShell is not a declared environment gate (nothing required skips on
    it), so this probes and skips locally — the shape `test_env_gates.py`
    exempts for an UNGATED tool, which is why the declared-gate helper is
    imported by this module."""
    powershell = shutil.which("pwsh") or shutil.which("powershell")
    if not powershell:
        pytest.skip("no powershell on this machine")
    scripts = _check_repo(tmp_path / "repo")
    done = _run(
        [powershell, "-NoProfile", "-File", str(scripts / "check.ps1")],
        scripts.parent,
        _write_fake_bin(tmp_path / "bin", spoof, label),
    )
    if label == "NEW":
        assert done.returncode == 0, done.stdout + done.stderr
        assert "FAKE-NEW ran" in done.stdout, done.stdout + done.stderr
    else:
        assert done.returncode != 0, done.stdout + done.stderr
        assert "older than Python 3.11" in done.stdout + done.stderr
