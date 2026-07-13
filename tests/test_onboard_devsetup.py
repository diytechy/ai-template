"""Onboarding-ladder helpers (Thread 15 Parts B/C/D, process.md §7).

Two cross-platform script families the kit scaffolds:
  - the Stage-0 `onboard.{sh,command,cmd}` guided onboarder, and
  - the developer-workstation `dev-setup.{sh,ps1}`.

They touch install/GUI/auth paths pytest can't fully drive, so the automated net
is a shell **smoke test** (syntax-valid onboarder; `dev-setup --check` runs and
reports) plus content assertions on the contract the spec pins (the end banner +
agent handoff, the templated clone URL, the EDIT-FOR-YOUR-STACK block). Deeper
cross-platform/GUI/auth behavior is verified manually per OS (see the plan).
"""

import os
import shutil
import subprocess

from conftest import KIT

REPO_ROOT = KIT.parent  # the meta-repo root (this kit dogfoods dev-setup here)

ONBOARD = ["scripts/onboard.sh", "scripts/onboard.command", "scripts/onboard.cmd"]
DEVSETUP = ["scripts/dev-setup.sh", "scripts/dev-setup.ps1"]
# macOS's double-clickable wrapper (Finder opens a bare .sh in an editor, it
# doesn't execute it) — asserted separately from DEVSETUP because it is a thin
# delegator, not an instantiation of the template's EDIT block.
DEVSETUP_COMMAND = "scripts/dev-setup.command"


def _sh():
    return shutil.which("sh")


def test_bootstrap_scaffolds_the_ladder_helpers(scaffold):
    for rel in ONBOARD + DEVSETUP:
        assert (scaffold / rel).exists(), "missing from scaffold: " + rel


def test_shell_helpers_are_executable_on_posix(scaffold):
    # .sh and .command must carry the exec bit so Finder/`./` can run them;
    # meaningless on Windows, so only assert where the OS tracks it.
    if os.name != "posix":
        import pytest

        pytest.skip("executable bit is not tracked on this OS")
    for rel in (
        "scripts/onboard.sh",
        "scripts/onboard.command",
        "scripts/dev-setup.sh",
    ):
        assert os.access(scaffold / rel, os.X_OK), rel + " must be executable"


def test_onboarder_carries_end_banner_agent_handoff_and_clone_url(scaffold):
    # Every platform variant must show the checkout dir + the agent-handoff line
    # (the non-coder's path) and expose a fill-in clone URL (the spec's contract).
    for rel in ONBOARD:
        text = (scaffold / rel).read_text(encoding="utf-8")
        assert "point it at this directory" in text, rel + " missing agent handoff"
        assert "https://github.com/OWNER/REPO.git" in text, (
            rel + " missing clone URL slot"
        )
        assert "EDIT FOR YOUR PROJECT" in text, rel + " missing the EDIT marker"


def test_devsetup_has_edit_block_tiers_and_profiles(scaffold):
    for rel in DEVSETUP:
        text = (scaffold / rel).read_text(encoding="utf-8")
        assert "EDIT FOR YOUR STACK" in text, rel + " missing the EDIT block"
        # The three tiers and the two declared example roles the spec pins.
        for token in ("check", "baseline", "full", "code", "design"):
            assert token in text, rel + " missing tier/role: " + token


def _devsetup_check(scaffold, *extra):
    sh = _sh()
    if not sh:
        import pytest

        pytest.skip("no POSIX shell on PATH")
    return subprocess.run(
        [sh, "scripts/dev-setup.sh", "--check", *extra],
        cwd=str(scaffold),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )


def test_devsetup_wires_the_process_floor_and_offers_setup_chain(scaffold):
    # WI-1.42: the pre-commit floor (core.hooksPath) is wired from the universal
    # dev-setup rung — not only from setup.* — and a code contributor is offered
    # the chain into setup for the product toolchain. Content on both launchers,
    # plus the --check report line (stdin closed -> non-interactive -> no prompt).
    for rel in DEVSETUP:
        text = (scaffold / rel).read_text(encoding="utf-8")
        assert "core.hooksPath .githooks" in text, rel + " does not wire the floor"
        assert "pre-commit floor" in text, rel + " missing the floor report"
        assert "Run scripts/setup" in text, rel + " missing the code-profile chain"
    proc = _devsetup_check(scaffold)
    assert "pre-commit floor (core.hooksPath)" in proc.stdout, proc.stdout


def test_devsetup_default_reports_every_role(scaffold):
    # No --profile installs/reports every declared role (the owner ruling: the
    # default does everything; a role is the opt-down).
    proc = _devsetup_check(scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "profile=all" in proc.stdout
    assert "role: code" in proc.stdout and "role: design" in proc.stdout


def test_devsetup_profile_narrows_to_one_role(scaffold):
    # --profile <role> narrows to the shared baseline + that role only.
    proc = _devsetup_check(scaffold, "--profile", "design")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "role: design" in proc.stdout
    assert "role: code" not in proc.stdout


def test_devsetup_unknown_profile_errors(scaffold):
    # An undeclared role never silently installs nothing: exit 2 naming the
    # declared roles.
    proc = _devsetup_check(scaffold, "--profile", "bogus")
    assert proc.returncode == 2
    assert "Unknown --profile 'bogus'" in proc.stderr
    assert "code design" in proc.stderr


def test_devsetup_check_runs_and_reports(scaffold):
    # The default tier must run and report without installing anything (exit 0),
    # so it is safe on a bare machine and in CI. Needs a POSIX shell.
    sh = _sh()
    if not sh:
        import pytest

        pytest.skip("no POSIX shell on PATH")
    proc = subprocess.run(
        [sh, "scripts/dev-setup.sh", "--check"],
        cwd=str(scaffold),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "tier=check" in proc.stdout
    assert "component(s) missing" in proc.stdout  # the report ran


def test_onboarder_sh_is_syntactically_valid(scaffold):
    # `sh -n` parses without executing — catches a broken onboarder before a
    # contributor ever runs it. (The .command/.cmd variants are per-OS manual.)
    sh = _sh()
    if not sh:
        import pytest

        pytest.skip("no POSIX shell on PATH")
    for rel in ("scripts/onboard.sh", "scripts/dev-setup.sh"):
        proc = subprocess.run(
            [sh, "-n", rel], cwd=str(scaffold), capture_output=True, text=True
        )
        assert proc.returncode == 0, rel + ": " + proc.stderr


def test_bootstrap_scaffolds_devsetup_command(scaffold):
    # The fresh-Mac rung: /usr/bin/{python3,git} ship as Command Line Tools
    # placeholders that satisfy `command -v` but only pop Apple's installer when
    # run, so the double-clickable wrapper must probe the real toolchain
    # (xcode-select -p), offer the one-time install, and otherwise delegate to
    # dev-setup.sh (the command lives once, there).
    path = scaffold / DEVSETUP_COMMAND
    assert path.exists(), "missing from scaffold: " + DEVSETUP_COMMAND
    text = path.read_text(encoding="utf-8")
    assert "xcode-select -p" in text, "missing the real-toolchain probe"
    assert "xcode-select --install" in text, "missing the CLT install kick-off"
    assert "dev-setup.sh" in text, "must delegate to the shared POSIX script"
    if os.name == "posix":
        assert os.access(path, os.X_OK), DEVSETUP_COMMAND + " must be executable"


def test_devsetup_command_is_syntactically_valid(scaffold):
    sh = _sh()
    if not sh:
        import pytest

        pytest.skip("no POSIX shell on PATH")
    proc = subprocess.run(
        [sh, "-n", DEVSETUP_COMMAND], cwd=str(scaffold), capture_output=True, text=True
    )
    assert proc.returncode == 0, DEVSETUP_COMMAND + ": " + proc.stderr


def test_devsetup_sees_through_macos_clt_placeholders(scaffold):
    # The false positive found on a real fresh Mac: `command -v python3`
    # succeeds against the placeholder, so detection must gate /usr/bin tools
    # on the toolchain actually being present.
    text = (scaffold / "scripts/dev-setup.sh").read_text(encoding="utf-8")
    assert "xcode-select -p" in text, "runtime/git detection trusts command -v alone"


def test_meta_repo_dogfoods_devsetup_command():
    path = REPO_ROOT / DEVSETUP_COMMAND
    assert path.exists(), "meta-repo missing dogfood " + DEVSETUP_COMMAND
    text = path.read_text(encoding="utf-8")
    assert "xcode-select -p" in text
    assert os.name != "posix" or os.access(path, os.X_OK)


def test_meta_repo_dogfoods_dev_setup():
    # Part D: the kit provisions itself with a concrete dev-setup in scripts/
    # (the same layout it scaffolds downstream), an instantiation of the
    # shipped template (points back at it).
    for name in DEVSETUP:
        path = REPO_ROOT / name
        assert path.exists(), "meta-repo missing dogfood " + name
        assert "dev-setup.template" in path.read_text(encoding="utf-8")

    sh = _sh()
    if not sh:
        import pytest

        pytest.skip("no POSIX shell on PATH")
    proc = subprocess.run(
        [sh, "scripts/dev-setup.sh", "--check"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "ai-template meta-repo" in proc.stdout
    # WI-075: dev-setup reports (and --install provisions) pytest-xdist, the
    # parallel `-n auto` runner the meta stack.ini now declares. The report label
    # prints whether or not the module is present, so this is stable in any env.
    assert "pytest-xdist" in proc.stdout
    # WI-109: the two agent CLIs the unattended layer routes through are named
    # required dev tools here (the labels print [ok]/[missing] either way, so
    # this is stable on a CI box that has neither). The ps1 twin carries the
    # same rows (asserted textually — no PowerShell on POSIX CI).
    assert "claude CLI" in proc.stdout
    assert "opencode CLI" in proc.stdout
    ps1 = (REPO_ROOT / "scripts/dev-setup.ps1").read_text(encoding="utf-8")
    assert "claude CLI" in ps1 and "opencode CLI" in ps1
    # WI-111: --install is delta-aware — the nothing-to-do fast path (skips the
    # prompt AND the pip self-upgrade when ./.venv already has all four tools)
    # exists in both twins. Asserted textually: executing --install in a test
    # would prompt or mutate an environment.
    for name in DEVSETUP:
        assert "nothing to install" in (REPO_ROOT / name).read_text(encoding="utf-8"), (
            name + " missing the WI-111 delta-aware fast path"
        )
    # WI-112: --install OFFERS each agent CLI individually ([y/N] per CLI, npm
    # package named), and both twins carry the emphasized consequence: with an
    # enabled row's CLI missing, agent-resume cannot boot the walk-away loop —
    # deferrable for users on their own tools / an IDE extension. Textual (the
    # live prompt/NOTE only prints when a CLI is missing, which varies per box).
    for name in DEVSETUP:
        text = (REPO_ROOT / name).read_text(encoding="utf-8")
        assert "CLI now (npm install -g" in text, name + " missing the per-CLI offer"
        assert "opencode-ai" in text and "@anthropic-ai/claude-code" in text, (
            name + " missing an npm package name"
        )
        assert "cannot boot the walk-away" in text, (
            name + " missing the emphasized agent-resume consequence"
        )
        assert "cannot boot the unattended" in text, (
            name + " missing the --check-mode warning"
        )
