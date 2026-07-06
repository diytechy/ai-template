"""The deterministic secrets + privacy lint (Thread 39 Layer 1; Thread 44 split).

Every detection class is exercised red/green on real staged diffs / trees /
commit ranges in a bootstrapped scaffold, because the lint's whole value is
what it blocks *and* what it deliberately lets through (placeholders, RFC 2606
example domains, `privacy-ok`-marked lines). Two layers are pinned separately:
the always-on **secrets floor** (key/token shapes, every repo — opt out with
`docs/secrets-scan: off`) and the **identity-leak** classes gated on a declared
`docs/commit-identity` pattern. An `inherit` repo with the floor opted out must
cost zero — that fast-exit keeps the step wireable unconditionally in check.py
and the pre-commit hook.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import run_py

ANON = "*@users.noreply.github.com"
SCRIPT = "scripts/check_privacy.py"
# This kit repo (a git checkout) and its real check_privacy.py, for the
# meta-repo dogfood — the scaffold copies live at scripts/, the source here does not.
REPO_ROOT = Path(__file__).resolve().parent.parent
KIT_SCRIPT = REPO_ROOT / "project-trajectory" / "scripts" / "check_privacy.py"
# A deterministic fake OS account: getpass.getuser() honors LOGNAME/USER/
# USERNAME (in that order) on every platform, so forcing all three makes the
# current-account class testable without depending on the machine's real user.
FAKE_USER = "privacyprobeuser"

needs_git = pytest.mark.skipif(not shutil.which("git"), reason="needs git on PATH")


def lint_env():
    env = dict(os.environ)
    for var in ("LOGNAME", "USER", "LNAME", "USERNAME"):
        env[var] = FAKE_USER
    return env


def run_lint(cwd, *args):
    return subprocess.run(
        [sys.executable, SCRIPT] + list(args),
        cwd=str(cwd),
        capture_output=True,
        text=True,
        env=lint_env(),
        stdin=subprocess.DEVNULL,
    )


def set_policy(root, value):
    (root / "docs" / "commit-identity").write_text(value + "\n", encoding="utf-8")


def set_secrets_scan(root, value):
    (root / "docs" / "secrets-scan").write_text(value + "\n", encoding="utf-8")


def git(root, *args):
    return subprocess.run(["git", *args], cwd=str(root), capture_output=True, text=True)


def init_repo(root):
    assert git(root, "init").returncode == 0
    git(root, "config", "user.name", "Test User")
    git(root, "config", "user.email", "12345+t@users.noreply.github.com")
    # Keep hook managers/global hooksPath out of the test repo's commits.
    git(root, "config", "core.hooksPath", ".git/hooks")


def stage(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    assert git(root, "add", rel).returncode == 0


@needs_git
def test_inherit_skips_identity_classes(scaffold):
    # The scaffolded default is inherit: the identity-leak classes (home-dir
    # paths, off-policy emails, the OS account) are not this repo's concern and
    # stay silent. The always-on secrets floor still runs (covered below), but a
    # home-dir path is not a secret, so the commit passes.
    init_repo(scaffold)
    stage(scaffold, "notes.md", "built at C:\\Users\\bobsmith\\proj\n")
    proc = run_lint(scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "home-dir path" not in proc.stdout


@needs_git
def test_secrets_floor_runs_under_inherit(scaffold):
    # Thread 44: a committed credential is a leak regardless of who authored it,
    # so the secrets floor fires even under the default inherit policy — the
    # security net an ordinary identified repo gets too.
    init_repo(scaffold)  # no commit-identity policy set: inherit
    stage(scaffold, "cfg.txt", "-----BEGIN RSA PRIVATE KEY-----\n")  # privacy-ok
    proc = run_lint(scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "private key header" in proc.stdout

    stage(scaffold, "cfg.txt", "aws = AKIA" + "A" * 16 + "\n")  # privacy-ok
    proc = run_lint(scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "aws access key id" in proc.stdout


@needs_git
def test_secrets_scan_off_opts_out(scaffold):
    # The opt-out: `docs/secrets-scan: off` disables the floor for the rare repo
    # whose content is secret-shaped. Under inherit + off, nothing runs at all.
    init_repo(scaffold)
    set_secrets_scan(scaffold, "off")
    stage(scaffold, "cfg.txt", "-----BEGIN RSA PRIVATE KEY-----\n")  # privacy-ok
    proc = run_lint(scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "nothing to check" in proc.stdout


@needs_git
def test_secrets_off_still_runs_identity_under_policy(scaffold):
    # The opt-out narrows only the secrets floor: under a declared anonymous
    # policy the identity classes still run, and a secret is let through.
    init_repo(scaffold)
    set_policy(scaffold, ANON)
    set_secrets_scan(scaffold, "off")
    stage(scaffold, "notes.md", "data at C:\\Users\\bobsmith\\proj\n")
    proc = run_lint(scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "home-dir path" in proc.stdout

    # A secret is let through when the floor is off (notes.md cleaned so the
    # only staged concern is the key the opt-out disables).
    stage(scaffold, "notes.md", "clean now\n")
    stage(scaffold, "cfg.txt", "-----BEGIN RSA PRIVATE KEY-----\n")  # privacy-ok
    proc = run_lint(scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr


@needs_git
def test_secrets_floor_in_repo_and_range_modes_under_inherit(scaffold):
    # The floor runs in all three modes even under inherit, not just the staged
    # diff: the --repo sweep and the --range history scan both catch it.
    init_repo(scaffold)
    (scaffold / "seed.txt").write_text("clean\n", encoding="utf-8")
    git(scaffold, "add", "seed.txt")
    assert git(scaffold, "commit", "-m", "base").returncode == 0
    base = git(scaffold, "rev-parse", "HEAD").stdout.strip()

    key = "-----BEGIN RSA PRIVATE KEY-----\n"  # privacy-ok
    (scaffold / "cfg.txt").write_text(key, encoding="utf-8")
    git(scaffold, "add", "cfg.txt")  # the sweep reads tracked (indexed) files
    proc = run_lint(scaffold, "--repo")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "private key header" in proc.stdout

    assert git(scaffold, "commit", "-m", "add cfg").returncode == 0
    proc = run_lint(scaffold, "--range", base + "..HEAD")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "private key header" in proc.stdout


@needs_git
def test_staged_home_dir_paths_red_placeholders_and_marker_green(scaffold):
    init_repo(scaffold)
    set_policy(scaffold, ANON)
    stage(scaffold, "notes.md", "data at C:\\Users\\bobsmith\\proj\n")
    proc = run_lint(scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "home-dir path" in proc.stdout
    assert "notes.md:1" in proc.stdout

    # POSIX shape too.
    stage(scaffold, "notes.md", "logs in /home/bobsmith/logs\n")
    assert run_lint(scaffold).returncode == 1

    # Placeholder-shaped usernames are documentation, not identity.
    stage(
        scaffold,
        "notes.md",
        "e.g. C:\\Users\\<x>\\proj or /home/username/proj or %USERPROFILE%\\x\n",
    )
    proc = run_lint(scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr

    # The inline allowlist marker exempts a documented example line.
    stage(scaffold, "notes.md", "data at C:\\Users\\bobsmith\\proj  privacy-ok\n")
    proc = run_lint(scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr


@needs_git
def test_staged_email_policy_and_example_domains(scaffold):
    init_repo(scaffold)
    set_policy(scaffold, ANON)
    stage(scaffold, "notes.md", "contact real.person@gmail.com about this\n")
    proc = run_lint(scaffold)
    assert proc.returncode == 1
    assert "email fails policy" in proc.stdout

    # Matching the declared pattern is the point of the policy; RFC 2606
    # example domains are documentation.
    stage(
        scaffold,
        "notes.md",
        "from 12345+x@users.noreply.github.com and someone@example.com\n",
    )
    proc = run_lint(scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr


@needs_git
def test_staged_current_account_word_boundary(scaffold):
    init_repo(scaffold)
    set_policy(scaffold, ANON)
    stage(scaffold, "notes.md", "session driven by {} yesterday\n".format(FAKE_USER))
    proc = run_lint(scaffold)
    assert proc.returncode == 1
    assert "current OS account" in proc.stdout

    # Substring inside a longer identifier is not the account name.
    stage(scaffold, "notes.md", "var {}extra = 1\n".format(FAKE_USER))
    proc = run_lint(scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr


@needs_git
def test_staged_key_and_token_shapes(scaffold):
    init_repo(scaffold)
    set_policy(scaffold, ANON)
    stage(scaffold, "cfg.txt", "-----BEGIN RSA PRIVATE KEY-----\n")
    proc = run_lint(scaffold)
    assert proc.returncode == 1
    assert "private key header" in proc.stdout

    stage(scaffold, "cfg.txt", "token = ghp_" + "a" * 36 + "\n")
    proc = run_lint(scaffold)
    assert proc.returncode == 1
    assert "github token" in proc.stdout


@needs_git
def test_removing_a_leak_is_never_flagged(scaffold):
    # The lint scans *added* lines only: deleting a leak must not block —
    # blocking the cleanup commit would train exactly the wrong behavior.
    init_repo(scaffold)
    stage(scaffold, "notes.md", "data at C:\\Users\\bobsmith\\proj\n")
    assert git(scaffold, "commit", "-m", "seed").returncode == 0
    set_policy(scaffold, ANON)
    stage(scaffold, "notes.md", "clean now\n")
    proc = run_lint(scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_repo_sweep_fresh_scaffold_green_then_seeded_leak_red(scaffold):
    # A fresh scaffold must itself survive an anonymous policy — the kit can't
    # ship content its own lint flags. (No git repo here: the sweep's
    # filesystem-walk fallback is exercised too.)
    set_policy(scaffold, ANON)
    proc = run_lint(scaffold, "--repo")
    assert proc.returncode == 0, proc.stdout + proc.stderr

    (scaffold / "docs" / "notes.md").write_text(
        "worked from /Users/bobsmith/checkout\n", encoding="utf-8"
    )
    proc = run_lint(scaffold, "--repo")
    assert proc.returncode == 1
    assert "docs/notes.md:1" in proc.stdout


@needs_git
def test_range_mode_catches_history_and_messages(scaffold):
    # The push-boundary property: a leak added in one commit and removed in a
    # later one ships in *history* even though the final tree is clean — and a
    # commit message is history too.
    init_repo(scaffold)
    set_policy(scaffold, ANON)
    stage(scaffold, "a.txt", "clean line\n")
    assert git(scaffold, "commit", "-m", "base").returncode == 0
    base = git(scaffold, "rev-parse", "HEAD").stdout.strip()

    stage(scaffold, "leak.txt", "creds at C:\\Users\\bobsmith\\secrets\n")
    assert git(scaffold, "commit", "-m", "add data file").returncode == 0
    git(scaffold, "rm", "-q", "leak.txt")
    assert git(scaffold, "commit", "-m", "remove data file").returncode == 0

    proc = run_lint(scaffold, "--range", base + "..HEAD")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "home-dir path" in proc.stdout

    # The removal-only tail of the range is clean: deletions never flag.
    proc = run_lint(scaffold, "--range", "HEAD~1..HEAD")
    assert proc.returncode == 0, proc.stdout + proc.stderr

    # A leak that exists only in a commit *message* is caught the same way.
    stage(scaffold, "b.txt", "fine\n")
    assert (
        git(scaffold, "commit", "-m", "notes from /home/bobsmith/session").returncode
        == 0
    )
    proc = run_lint(scaffold, "--range", "HEAD~1..HEAD")
    assert proc.returncode == 1
    assert "commit " in proc.stdout


def test_check_py_wires_privacy_as_process_step(scaffold):
    # The sweep is a [process] step at every gate; on the inherit scaffold the
    # whole G1 plan still passes — the secrets floor runs but a fresh scaffold
    # ships no credential shapes, so wiring it unconditionally never taxes an
    # unconcerned repo.
    proc = run_py(["scripts/check.py", "--gate", "G1", "--list"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert any("privacy" in ln and "[process]" in ln for ln in proc.stdout.splitlines())
    proc = run_py(["scripts/check.py", "--gate", "G1", "--lenient"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "RESULT: PASS" in proc.stdout


def test_check_py_gate_red_on_seeded_leak(scaffold):
    # Under a declared policy the same G1 gate goes red on a tracked leak —
    # the CI-side net for what slipped past --no-verify or predates the policy.
    set_policy(scaffold, ANON)
    (scaffold / "docs" / "notes.md").write_text(
        "worked from C:\\Users\\bobsmith\\checkout\n", encoding="utf-8"
    )
    proc = subprocess.run(
        [sys.executable, "scripts/check.py", "--gate", "G1", "--lenient"],
        cwd=str(scaffold),
        capture_output=True,
        text=True,
        env=lint_env(),
        stdin=subprocess.DEVNULL,
    )
    assert proc.returncode != 0
    assert any("FAIL" in ln and "privacy" in ln for ln in proc.stdout.splitlines()), (
        proc.stdout
    )


@needs_git
def test_meta_repo_tree_passes_the_secrets_floor():
    # Dogfood: this kit repo is `inherit`, so the always-on secrets floor now
    # applies to it. Its own tracked tree must ship no credential shapes — the
    # net that would catch a real key ever landing in the kit. Run against the
    # real repo root, not a scaffold.
    proc = subprocess.run(
        [sys.executable, str(KIT_SCRIPT), "--root", str(REPO_ROOT), "--repo"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
