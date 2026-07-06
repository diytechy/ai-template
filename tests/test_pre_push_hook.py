"""The anonymous-repo pre-push privacy backstop (Thread 39, Layer 2).

Exercised end-to-end where a POSIX shell + git exist (Linux/macOS CI; Git Bash
on Windows): the hook receives the real stdin ref lines `git push` would send,
runs the deterministic lint over the outgoing range, and drives the REVIEW_CMD
reviewer slot with fake approve/block scripts — no CI dependency on a real
agent CLI. The Q12 ruling is pinned here: a missing reviewer FAILS CLOSED —
with WI-1.30's one declared opt-down (docs/privacy-review: warn-unwired),
which softens only the unwired case and is pinned just as hard.
"""

import os
import shutil
import subprocess

import pytest

HOOK = ".githooks/pre-push"
ZERO = "0" * 40
FAKE_USER = "privacyprobeuser"

pytestmark = pytest.mark.skipif(
    not (shutil.which("sh") and shutil.which("git")),
    reason="needs a POSIX shell and git on PATH",
)


def _posix(path):
    return str(path).replace("\\", "/")


def git(root, *args):
    return subprocess.run(["git", *args], cwd=str(root), capture_output=True, text=True)


def commit_file(root, rel, text, msg):
    (root / rel).write_text(text, encoding="utf-8")
    assert git(root, "add", rel).returncode == 0
    proc = git(root, "commit", "-m", msg)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return git(root, "rev-parse", "HEAD").stdout.strip()


@pytest.fixture
def repo(scaffold):
    """Scaffold + git repo with three clean commits (base → middle → head).
    The middle commit's message carries a marker so tests can prove the
    reviewer saw the *intermediate* history, not just the endpoints."""
    assert git(scaffold, "init").returncode == 0
    git(scaffold, "config", "user.name", "Test User")
    git(scaffold, "config", "user.email", "12345+t@users.noreply.github.com")
    git(scaffold, "config", "core.hooksPath", ".git/hooks")
    base = commit_file(scaffold, "a.txt", "clean base\n", "base")
    commit_file(scaffold, "b.txt", "middle change\n", "feat: MARKER-BEEF middle")
    head = commit_file(scaffold, "c.txt", "clean head\n", "head")
    return scaffold, base, head


def run_hook(root, stdin_text, review_cmd=None):
    env = dict(os.environ)
    # Deterministic lint identity (see test_check_privacy.FAKE_USER rationale).
    for var in ("LOGNAME", "USER", "LNAME", "USERNAME"):
        env[var] = FAKE_USER
    env.pop("REVIEW_CMD", None)
    if review_cmd is not None:
        env["REVIEW_CMD"] = review_cmd
    return subprocess.run(
        [shutil.which("sh"), HOOK, "origin", "https://example.invalid/repo.git"],
        cwd=str(root),
        input=stdin_text,
        capture_output=True,
        text=True,
        env=env,
    )


def set_privacy(root, value="true"):
    (root / "docs" / "privacy-check").write_text(value + "\n", encoding="utf-8")


def push_line(head, remote_sha):
    return "refs/heads/main {} refs/heads/main {}\n".format(head, remote_sha)


def make_reviewer(tmp_path, name, body):
    script = tmp_path / name
    script.write_text("#!/bin/sh\n" + body, encoding="utf-8")
    return "sh " + _posix(script)


def test_inherit_policy_is_inert(repo):
    # The scaffolded default: no reviewer wired, a push flows through — the
    # backstop costs unconcerned repos nothing.
    root, base, head = repo
    proc = run_hook(root, push_line(head, base))
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_inherit_secrets_floor_blocks_a_key_in_range(repo):
    # Thread 44: even an inherit repo's push is guarded by the always-on secrets
    # floor — a key/token shape in the outgoing history blocks, with no reviewer
    # machinery and no fail-closed (the identity guarantee does not apply here).
    root, base, head = repo
    key = (
        "-----BEGIN RSA " + "PRIVATE KEY-----\n"
    )  # split so this source line is not itself a match
    leaky = commit_file(root, "cfg.txt", key, "add cfg")
    proc = run_hook(root, push_line(leaky, head))
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "secrets floor" in proc.stderr


def test_inherit_secrets_scan_off_lets_it_through(repo):
    # The opt-out reaches the push boundary: docs/secrets-scan off disables the
    # floor, so the same key does not block an unconcerned repo's push.
    root, base, head = repo
    (root / "docs" / "secrets-scan").write_text("off\n", encoding="utf-8")
    key = "-----BEGIN RSA " + "PRIVATE KEY-----\n"
    leaky = commit_file(root, "cfg.txt", key, "add cfg")
    proc = run_hook(root, push_line(leaky, head))
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_missing_reviewer_fails_closed(repo):
    # The Q12 ruling: under a declared policy a missing reviewer is never a
    # pass at the one boundary that matters — block, with the wiring spelled out.
    root, base, head = repo
    set_privacy(root)
    proc = run_hook(root, push_line(head, base))
    assert proc.returncode != 0, "missing reviewer must fail closed"
    assert "REVIEW_CMD" in proc.stderr
    assert "privacy.reviewcmd" in proc.stderr


def set_review_policy(root, value):
    (root / "docs" / "privacy-review").write_text(value + "\n", encoding="utf-8")


def test_warn_unwired_optdown_warns_and_proceeds(repo):
    # WI-1.30 (refining Q12): the adopted-but-not-wired-yet window. With the
    # tracked opt-down declared and a clean outgoing range, an unwired
    # reviewer warns — naming what actually guarded the push — and the push
    # proceeds on the deterministic layer alone.
    root, base, head = repo
    set_privacy(root)
    set_review_policy(root, "warn-unwired")
    proc = run_hook(root, push_line(head, base))
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARNING" in proc.stderr
    assert "warn-unwired" in proc.stderr
    assert "deterministic lint" in proc.stderr


def test_warn_unwired_does_not_soften_the_lint_floor(repo):
    # The opt-down softens ONLY the unwired-reviewer case: a deterministic
    # finding in the outgoing history still blocks.
    root, base, head = repo
    set_privacy(root)
    set_review_policy(root, "warn-unwired")
    new_head = commit_file(
        root, "leak.txt", "creds at C:\\Users\\bobsmith\\secrets\n", "add data"
    )
    proc = run_hook(root, push_line(new_head, head))
    assert proc.returncode != 0, "lint findings must block regardless of opt-down"
    assert "privacy lint found" in proc.stderr


def test_warn_unwired_does_not_soften_a_wired_block(repo, tmp_path):
    # A WIRED reviewer's BLOCK still blocks under the opt-down — the policy
    # speaks only to the reviewer being absent, never to its verdict.
    root, base, head = repo
    set_privacy(root)
    set_review_policy(root, "warn-unwired")
    block = make_reviewer(tmp_path, "block.sh", 'echo "BLOCK: leak"\nexit 1\n')
    proc = run_hook(root, push_line(head, base), review_cmd=block)
    assert proc.returncode != 0
    assert "BLOCKED" in proc.stderr


def test_review_policy_typo_stays_fail_closed(repo):
    # Any value other than the exact word — including a typo — reads as
    # require: a mistake yields the stricter behavior, never a silent pass.
    # The fail-closed message names the recorded opt-down as the escape.
    root, base, head = repo
    set_privacy(root)
    set_review_policy(root, "warn-unwried")  # deliberate typo
    proc = run_hook(root, push_line(head, base))
    assert proc.returncode != 0
    assert "FAILING CLOSED" in proc.stderr
    assert "docs/privacy-review" in proc.stderr


def test_approve_proceeds_and_reviewer_sees_full_range(repo, tmp_path):
    root, base, head = repo
    set_privacy(root)
    capture = tmp_path / "dump-capture.txt"
    approve = make_reviewer(
        tmp_path, "approve.sh", 'cp "$1" "{}"\necho APPROVE\n'.format(_posix(capture))
    )
    proc = run_hook(root, push_line(head, base), review_cmd=approve)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    dump = capture.read_text(encoding="utf-8")
    # The brief + the whole outgoing range: intermediate commit messages and
    # diffs ship in history, so the reviewer must have seen them.
    assert "PRIVACY REVIEW REQUEST" in dump
    assert "MARKER-BEEF" in dump  # the intermediate commit's message
    assert "middle change" in dump  # ... and its diff
    assert "clean head" in dump


def test_reviewer_via_git_config_slot(repo, tmp_path):
    # REVIEW_CMD's per-clone home: `git config privacy.reviewcmd` (env unset).
    root, base, head = repo
    set_privacy(root)
    approve = make_reviewer(tmp_path, "approve.sh", "echo APPROVE\n")
    git(root, "config", "privacy.reviewcmd", approve)
    proc = run_hook(root, push_line(head, base))
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_block_stops_the_push(repo, tmp_path):
    root, base, head = repo
    set_privacy(root)
    block = make_reviewer(
        tmp_path, "block.sh", 'echo "BLOCK: identity leak in commit 2"\nexit 1\n'
    )
    proc = run_hook(root, push_line(head, base), review_cmd=block)
    assert proc.returncode != 0
    assert "BLOCKED" in proc.stderr


def test_block_verdict_with_zero_exit_still_blocks(repo, tmp_path):
    # An agent CLI exits 0 after *printing* its verdict — the hook must read
    # the verdict, not just the exit code.
    root, base, head = repo
    set_privacy(root)
    sneaky = make_reviewer(
        tmp_path, "sneaky.sh", 'echo "BLOCK: found a real name"\nexit 0\n'
    )
    proc = run_hook(root, push_line(head, base), review_cmd=sneaky)
    assert proc.returncode != 0


def test_no_verdict_fails_closed(repo, tmp_path):
    # Chatter without an APPROVE is not an approval (a crashed or misbriefed
    # reviewer must not wave the push through).
    root, base, head = repo
    set_privacy(root)
    mute = make_reviewer(tmp_path, "mute.sh", 'echo "hello there"\nexit 0\n')
    proc = run_hook(root, push_line(head, base), review_cmd=mute)
    assert proc.returncode != 0
    assert "no APPROVE" in proc.stderr


def test_lint_layer_blocks_before_reviewer(repo, tmp_path):
    # Add-then-remove: the final tree is clean but the leak ships in history.
    # The deterministic floor catches it and the reviewer is never spent.
    root, base, head = repo
    set_privacy(root)
    leaky = commit_file(
        root, "leak.txt", "creds at C:\\Users\\bobsmith\\secrets\n", "add data"
    )
    git(root, "rm", "-q", "leak.txt")
    assert git(root, "commit", "-m", "remove data").returncode == 0
    new_head = git(root, "rev-parse", "HEAD").stdout.strip()
    assert leaky != new_head

    capture = tmp_path / "dump-capture.txt"
    approve = make_reviewer(
        tmp_path, "approve.sh", 'cp "$1" "{}"\necho APPROVE\n'.format(_posix(capture))
    )
    proc = run_hook(root, push_line(new_head, head), review_cmd=approve)
    assert proc.returncode != 0
    assert "privacy lint found" in proc.stderr
    assert not capture.exists(), "reviewer must not run once the lint blocked"


def test_deleting_a_remote_ref_is_not_outgoing_content(repo):
    root, base, head = repo
    set_privacy(root)
    proc = run_hook(root, "refs/heads/main {} refs/heads/main {}\n".format(ZERO, head))
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_bootstrap_copies_pre_push_hook(scaffold):
    hook = scaffold / HOOK
    assert hook.exists(), "bootstrap must copy the pre-push hook to .githooks/"
    assert hook.read_text(encoding="utf-8").startswith("#!/bin/sh")
