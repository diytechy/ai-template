"""The agent-neutral pre-commit hook (Thread 0b).

The hook is a thin POSIX wrapper around the kit's fast process checks, so we test
its *underlying logic* directly (run the same checks the hook runs) rather than
shelling out to `git commit`. Where a POSIX shell is available we also run the
hook script end-to-end to confirm the wiring.
"""

import json
import shutil
import subprocess

from conftest import KIT, LLRS, make_minimal_project, run_py

HOOK = ".githooks/pre-commit"
ARCH = "docs/architecture.md"
MAP_BEGIN = "<!-- BEGIN GENERATED MODULE MAP -->"


def test_bootstrap_copies_pre_commit_hook(scaffold):
    hook = scaffold / HOOK
    assert hook.exists(), "bootstrap must copy the pre-commit hook to .githooks/"
    assert hook.read_text(encoding="utf-8").startswith("#!/bin/sh")


def test_hook_checks_pass_on_clean_project(scaffold):
    # The two stdlib checks the hook always runs must pass on a fully-traced,
    # freshly-mapped project (the hook's "green commit" path).
    make_minimal_project(scaffold)
    archmap = run_py(["scripts/gen_arch_map.py", "--check"], cwd=scaffold)
    assert archmap.returncode == 0, archmap.stdout + archmap.stderr
    trace = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert trace.returncode == 0, trace.stdout + trace.stderr


def test_hook_blocks_stale_generated_block(scaffold):
    # A hand-edited GENERATED region must be caught by gen_arch_map --check (the
    # hook's "protect the GENERATED regions" guarantee).
    make_minimal_project(scaffold)
    arch = scaffold / ARCH
    text = arch.read_text(encoding="utf-8")
    assert MAP_BEGIN in text
    arch.write_text(
        text.replace(MAP_BEGIN, MAP_BEGIN + "\nHAND-EDITED — should be rejected.\n"),
        encoding="utf-8",
    )
    archmap = run_py(["scripts/gen_arch_map.py", "--check"], cwd=scaffold)
    assert archmap.returncode != 0, "stale generated block must fail --check"


def test_hook_arch_map_step_honors_declared_mode(scaffold):
    # WI-1.26 (Finance-Auditor re-sync field report): the hook's arch-map step
    # delegates to `check.py --run-step arch-map` (like its format step) so it
    # honors docs/stack.ini [arch-map]. A files-mode repo would otherwise have
    # every commit blocked: the hardcoded symbol parser reads a files-mode
    # architecture.md as stale.
    make_minimal_project(scaffold)
    ini = scaffold / "docs" / "stack.ini"
    ini.write_text(
        ini.read_text(encoding="utf-8").replace("mode = symbols", "mode = files", 1),
        encoding="utf-8",
    )
    regen = run_py(["scripts/gen_arch_map.py", "--mode", "files"], cwd=scaffold)
    assert regen.returncode == 0, regen.stdout + regen.stderr
    # The delegated step (what the hook now runs) agrees with the declared mode…
    ok = run_py(["scripts/check.py", "--run-step", "arch-map"], cwd=scaffold)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    # …where the hook's old hardcoded symbol-mode line reads the same repo as
    # stale — the every-commit-blocked failure the delegation removes.
    hard = run_py(["scripts/gen_arch_map.py", "--check"], cwd=scaffold)
    assert hard.returncode != 0
    # And the hook script itself carries the delegation, not the bare call.
    hook_text = (scaffold / HOOK).read_text(encoding="utf-8")
    assert "--run-step arch-map" in hook_text


def test_hook_blocks_duplicate_id_but_not_orphan(scaffold):
    # The hook's traceability command is --strict-integrity: a duplicated id is
    # wrong at any stage and must block, but an orphan is a G2+ *gate* criterion
    # (a mid-G1 registry legitimately has SRs with no LLR/TC) and must NOT block
    # a commit — the regression that made the hook wedge every G1-stage commit.
    make_minimal_project(scaffold)
    llr = scaffold / "docs" / "requirements" / "low-level-requirements.csv"
    llr.write_text(LLRS + LLRS.splitlines()[1] + "\n", encoding="utf-8")
    trace = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert trace.returncode != 0, "duplicate LLR id must fail --strict-integrity"

    # Restore, then simulate end-of-G1: an SR exists, its LLR/TC don't yet.
    llr.write_text(LLRS.splitlines()[0] + "\n", encoding="utf-8")
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status\n",
        encoding="utf-8",
    )
    strict = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert strict.returncode != 0, "orphans still fail the gate-scoped --strict"
    floor = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert floor.returncode == 0, (
        "a G1-stage registry must stay committable: " + floor.stdout + floor.stderr
    )


def test_hook_runs_end_to_end_when_sh_available(scaffold):
    # Where a POSIX shell exists (Linux/macOS CI; Git Bash on Windows), run the
    # actual hook so its interpreter discovery + command wiring are exercised.
    # A pre-commit hook only ever runs inside a git repo (its step 3 secrets
    # floor reads the staged diff), so init one — the realistic footing.
    sh = shutil.which("sh")
    if not sh or not shutil.which("git"):
        import pytest

        pytest.skip("needs a POSIX shell and git on PATH")
    make_minimal_project(scaffold)
    subprocess.run(["git", "init"], cwd=str(scaffold), capture_output=True)
    ok = subprocess.run([sh, HOOK], cwd=str(scaffold), capture_output=True, text=True)
    assert ok.returncode == 0, ok.stdout + ok.stderr

    # Tamper with the generated block; the hook must now block the commit.
    arch = scaffold / ARCH
    arch.write_text(
        arch.read_text(encoding="utf-8").replace(
            MAP_BEGIN, MAP_BEGIN + "\nHAND-EDITED — should be rejected.\n"
        ),
        encoding="utf-8",
    )
    blocked = subprocess.run(
        [sh, HOOK], cwd=str(scaffold), capture_output=True, text=True
    )
    assert blocked.returncode != 0, blocked.stdout + blocked.stderr


def test_hook_secrets_floor_blocks_staged_key_with_privacy_off(scaffold):
    # Thread 44: the pre-commit hook now runs the always-on secrets floor for
    # every repo, so a staged credential is blocked before the commit exists —
    # even with the scaffolded privacy gate off — and the opt-out lifts it.
    import pytest

    sh = shutil.which("sh")
    if not sh or not shutil.which("git"):
        pytest.skip("needs a POSIX shell and git on PATH")
    make_minimal_project(scaffold)

    def git(*args):
        return subprocess.run(
            ["git", *args], cwd=str(scaffold), capture_output=True, text=True
        )

    assert git("init").returncode == 0
    git("config", "user.name", "Test User")
    git("config", "user.email", "someone@example.com")
    key = "-----BEGIN RSA " + "PRIVATE KEY-----\n"  # split so this line is not a match
    (scaffold / "cfg.txt").write_text(key, encoding="utf-8")
    assert git("add", "cfg.txt").returncode == 0

    blocked = subprocess.run(
        [sh, HOOK], cwd=str(scaffold), capture_output=True, text=True
    )
    assert blocked.returncode != 0, "a staged private key must block with privacy off"
    assert "private key header" in (blocked.stdout + blocked.stderr)

    # The opt-out lifts the floor for a repo that needs it.
    (scaffold / "docs" / "secrets-scan").write_text("off\n", encoding="utf-8")
    ok = subprocess.run([sh, HOOK], cwd=str(scaffold), capture_output=True, text=True)
    assert ok.returncode == 0, ok.stdout + ok.stderr


def test_hook_privacy_author_guard(scaffold):
    # Identity->privacy reframe: with docs/privacy-check on, the hook's --author
    # step blocks a private (non-exempt) author before the commit exists and
    # passes an exempt no-reply one; the scaffolded default (privacy off) skips.
    import pytest

    sh = shutil.which("sh")
    if not sh or not shutil.which("git"):
        pytest.skip("needs a POSIX shell and git on PATH")
    make_minimal_project(scaffold)

    def git(*args):
        return subprocess.run(
            ["git", *args], cwd=str(scaffold), capture_output=True, text=True
        )

    assert git("init").returncode == 0
    git("config", "user.name", "Test User")
    git("config", "user.email", "real.person@gmail.com")

    def run_hook():
        return subprocess.run(
            [sh, HOOK], cwd=str(scaffold), capture_output=True, text=True
        )

    # The scaffolded default is privacy-check false: any identity passes.
    policy = scaffold / "docs" / "privacy-check"
    body = [
        ln
        for ln in policy.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.startswith("#")
    ]
    assert body == ["false"], "scaffold must default privacy-check to false"
    ok = run_hook()
    assert ok.returncode == 0, ok.stdout + ok.stderr

    # privacy-check on + a private (non-exempt) author: a designed block.
    policy.write_text("true\n", encoding="utf-8")
    blocked = run_hook()
    assert blocked.returncode != 0, "a private author must be blocked"
    assert "exempt allowlist" in blocked.stderr

    # An exempt no-reply author: green again.
    git("config", "user.email", "12345+user@users.noreply.github.com")
    ok = run_hook()
    assert ok.returncode == 0, ok.stdout + ok.stderr


def test_bootstrap_copies_commit_msg_hook(scaffold):
    hook = scaffold / ".githooks" / "commit-msg"
    assert hook.exists(), "bootstrap must copy the commit-msg hook to .githooks/"
    assert hook.read_text(encoding="utf-8").startswith("#!/bin/sh")


def test_commit_msg_hook_scans_message(scaffold):
    # The pile-up fix: pre-commit runs before the message exists, so the message
    # goes unscanned until push. The commit-msg hook closes the gap — git passes
    # the message file as $1 and a nonzero exit aborts the commit. The always-on
    # secrets floor scans every repo's message; the privacy layer adds its
    # classes only when docs/privacy-check is `true`.
    import pytest

    sh = shutil.which("sh")
    if not sh or not shutil.which("git"):
        pytest.skip("needs a POSIX shell and git on PATH")
    make_minimal_project(scaffold)
    subprocess.run(["git", "init"], cwd=str(scaffold), capture_output=True)
    HOOK_CM = ".githooks/commit-msg"

    def run_msg(text):
        msg = scaffold / "MSG.txt"
        msg.write_text(text, encoding="utf-8")
        return subprocess.run(
            [sh, HOOK_CM, "MSG.txt"], cwd=str(scaffold), capture_output=True, text=True
        )

    # Secrets floor (always on): a credential in the message body blocks.
    key = "-----BEGIN RSA " + "PRIVATE KEY-----"  # split so this line is not a match
    blocked = run_msg("add config\n\n" + key + "\n")
    assert blocked.returncode != 0, "a secret in the message must block"
    assert "private key header" in (blocked.stdout + blocked.stderr)

    # Privacy layer off (scaffold default): a private email in the message is a
    # privacy class, not a secret, so it passes.
    ok = run_msg("fix\n\nReported-by: real.person@gmail.com\n")
    assert ok.returncode == 0, ok.stdout + ok.stderr

    # Privacy layer on: the same private email now blocks; the exempt no-reply
    # co-author trailer passes.
    (scaffold / "docs" / "privacy-check").write_text("true\n", encoding="utf-8")
    blocked = run_msg("fix\n\nReported-by: real.person@gmail.com\n")
    assert blocked.returncode != 0, "a private email in the message must block when on"
    assert "exempt allowlist" in (blocked.stdout + blocked.stderr)
    ok = run_msg("fix\n\nCo-Authored-By: Claude <noreply@anthropic.com>\n")
    assert ok.returncode == 0, ok.stdout + ok.stderr


def test_optional_agent_hook_configs_are_valid_json():
    # The optional extras ship as real JSON the user can drop into .claude/.gemini.
    for name in ("claude.settings.json", "gemini.settings.json"):
        path = KIT / "agent-hooks" / name
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "hooks" in data, name + " must define a hooks block"
