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
        # The three tiers and two contributor profiles the spec pins.
        for token in ("check", "baseline", "full", "code", "domain"):
            assert token in text, rel + " missing tier/profile: " + token


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


def test_meta_repo_dogfoods_dev_setup():
    # Part D: the kit provisions itself with a concrete dev-setup at the repo
    # root, an instantiation of the shipped template (points back at it).
    for name in ("dev-setup.sh", "dev-setup.ps1"):
        path = REPO_ROOT / name
        assert path.exists(), "meta-repo missing dogfood " + name
        assert "dev-setup.template" in path.read_text(encoding="utf-8")

    sh = _sh()
    if not sh:
        import pytest

        pytest.skip("no POSIX shell on PATH")
    proc = subprocess.run(
        [sh, "dev-setup.sh", "--check"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "ai-template meta-repo" in proc.stdout
