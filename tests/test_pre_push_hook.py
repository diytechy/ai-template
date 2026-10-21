"""The privacy-check pre-push privacy backstop (Thread 39, Layer 2).

Exercised end-to-end where a POSIX shell + git exist (Linux/macOS CI; Git Bash
on Windows): the hook receives the real stdin ref lines `git push` would send,
runs the deterministic lint over the outgoing range, and drives the REVIEW_CMD
reviewer slot with fake approve/block scripts — no CI dependency on a real
agent CLI. The Q12 ruling is pinned here: a missing reviewer FAILS CLOSED —
with WI-1.30's one declared opt-down (docs/privacy-review: warn-unwired),
which softens only the unwired case and is pinned just as hard.
"""

import os
import re
import shutil
import subprocess

import pytest
from conftest import (
    augment_env,
    env_gate_skipif,
    older_only_path,
    pin_autocrlf,
    set_process_key,
    sub_floor_interpreter,
)

HOOK = ".githooks/pre-push"
ZERO = "0" * 40
FAKE_USER = "privacyprobeuser"

# WI-326: the module-level form of the declared gate. Same reason string as the
# runtime helper, so the session banner and the terminal-summary count see this
# module's skips too.
pytestmark = env_gate_skipif("posix-shell", "git")


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
    pin_autocrlf(scaffold)  # WI-461/WI-465; see conftest.pin_autocrlf
    git(scaffold, "config", "user.name", "Test User")
    git(scaffold, "config", "user.email", "12345+t@users.noreply.github.com")
    git(scaffold, "config", "core.hooksPath", ".git/hooks")
    base = commit_file(scaffold, "a.txt", "clean base\n", "base")
    commit_file(scaffold, "b.txt", "middle change\n", "feat: MARKER-BEEF middle")
    head = commit_file(scaffold, "c.txt", "clean head\n", "head")
    return scaffold, base, head


def run_hook(root, stdin_text, review_cmd=None, env_extra=None):
    env = dict(os.environ, **(env_extra or {}))
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
        # Measure the check_privacy the hook invokes when pytest-cov is active
        # (Thread 47 phase 6) — the pre-push range scan is otherwise uninstrumented.
        env=augment_env(env),
    )


def set_privacy(root, value="true"):
    # SN-028: the toggle's home is docs/process.toml [policies] privacy_check,
    # which the hook reads with a KEYED grep (the M-42 pure-sh fail-closed path
    # survives the move; the file is written one `key = value` per line for
    # exactly this reason).
    set_process_key(root, "policies", "privacy_check", value == "true")


def push_line(head, remote_sha):
    return "refs/heads/main {} refs/heads/main {}\n".format(head, remote_sha)


def make_reviewer(tmp_path, name, body):
    script = tmp_path / name
    script.write_text("#!/bin/sh\n" + body, encoding="utf-8")
    return "sh " + _posix(script)


def test_pre_push_honors_kit_scripts_dir(repo):
    # C4: the harness-elsewhere layout (KIT_SCRIPTS_DIR, WI-1.42) must reach the
    # secrets floor at the push boundary too — not just pre-commit. Relocate the
    # harness and point the env var at it: a key in the outgoing range still
    # blocks (scripts found via the override); without the var, scripts/ is
    # absent at the root so the floor can't run, and the push is REFUSED with
    # the one scripts-lookup refusal every kit hook prints (WI-926).
    root, base, _head = repo
    shutil.move(str(root / "scripts"), str(root / "harness_scripts"))
    key = "-----BEGIN RSA " + "PRIVATE KEY-----\n"  # split so this line isn't a match
    keyed = commit_file(root, "leak.txt", key, "add config")

    def run(with_override):
        env = dict(os.environ)
        for var in ("LOGNAME", "USER", "LNAME", "USERNAME"):
            env[var] = FAKE_USER
        env.pop("REVIEW_CMD", None)
        if with_override:
            env["KIT_SCRIPTS_DIR"] = "harness_scripts"
        return subprocess.run(
            [shutil.which("sh"), HOOK, "origin", "https://example.invalid/r.git"],
            cwd=str(root),
            input=push_line(keyed, base),
            capture_output=True,
            text=True,
            env=augment_env(env),
        )

    blocked = run(with_override=True)
    assert blocked.returncode != 0, blocked.stdout + blocked.stderr
    assert "secrets floor" in blocked.stderr
    refused = run(with_override=False)  # harness unfindable -> refused
    assert refused.returncode != 0, refused.stdout + refused.stderr
    assert "cannot find the kit scripts dir" in refused.stderr, refused.stderr
    assert "REFUSING" in refused.stderr, refused.stderr
    assert "KIT_SCRIPTS_DIR in the delegating wrapper" in refused.stderr
    assert "git config --unset core.hooksPath" in refused.stderr


def test_privacy_off_is_inert(repo):
    # The scaffolded default: no reviewer wired, a push flows through — the
    # backstop costs unconcerned repos nothing.
    root, base, head = repo
    proc = run_hook(root, push_line(head, base))
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_secrets_floor_blocks_a_key_in_range(repo):
    # Thread 44: even a privacy-off repo's push is guarded by the always-on secrets
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


def test_secrets_scan_off_lets_it_through(repo):
    # The opt-out reaches the push boundary: docs/secrets-scan off disables the
    # floor, so the same key does not block an unconcerned repo's push.
    root, base, head = repo
    set_process_key(root, "policies", "secrets_scan", False)
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
    # NOTE the historical name: this is the unwired-REVIEWER posture
    # (docs/privacy-review -> [policies] privacy_review), NOT the reviewer-count
    # dial. No hook has ever read docs/review-policy.
    set_process_key(root, "policies", "privacy_review", value)


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
    # The remediation names the LIVE home. It used to say
    # `echo warn-unwired > docs/privacy-review`, which the same hook stopped
    # reading first at SN-028 — so an operator blocked from pushing followed
    # the advice and stayed blocked with no explanation. Advice that does
    # nothing is worse than no advice: it spends the reader's trust.
    assert "privacy_review" in proc.stderr
    assert "warn-unwired" in proc.stderr
    assert "docs/process.toml" in proc.stderr


_POSTURE_KEY = re.compile(r"^\s*privacy_review\s*=")
_DECOY_SECTION = '[decoy]\nprivacy_review = "warn-unwired"\n'
_DECOY_STRING = '[decoy]\nnote = """\nprivacy_review = "warn-unwired"\n"""\n'


def _declare_posture(root, value, legacy, decoy):
    """The unwired-reviewer posture as one case declares it: the scaffold's
    `privacy_review` line removed, then set to `value` under [policies]
    unless None; `legacy` as docs/privacy-review unless None; `decoy` text
    appended to the file unless None."""
    path = root / "docs" / "process.toml"
    kept = [
        line
        for line in path.read_text(encoding="utf-8").splitlines(keepends=True)
        if not _POSTURE_KEY.match(line)
    ]
    with path.open("w", encoding="utf-8", newline="") as fh:
        fh.write("".join(kept) + (decoy or ""))
    if value is not None:
        set_process_key(root, "policies", "privacy_review", value)
    if legacy is not None:
        (root / "docs" / "privacy-review").write_text(legacy + "\n", encoding="utf-8")


# (privacy on?, [policies] privacy_review or None, legacy file or None,
#  appended decoy or None, outcome). The two decoy rows catch a text read
# that finds the key outside [policies] and warns (a fail-open); every other
# row carries its adequacy witness in the comment beside it.
POSTURE_CASES = [
    # A reader that ignored the opt-down would refuse here.
    pytest.param(True, "warn-unwired", None, None, "warn", id="on-warn-unwired"),
    pytest.param(True, "require", None, None, "refuse", id="on-require"),
    # A reader that matched a prefix or a near-spelling would warn here.
    pytest.param(True, "warn-unwried", None, None, "refuse", id="on-typo"),
    # A reader that took any non-"require" value as the opt-down would warn.
    pytest.param(True, 1, None, None, "refuse", id="on-wrong-type"),
    # A case-insensitive reader would warn here.
    pytest.param(True, "WARN-UNWIRED", None, None, "refuse", id="on-uppercase"),
    # A reader defaulting to warn-unwired on absence would warn here.
    pytest.param(True, None, None, None, "refuse", id="on-absent"),
    # A reader that dropped the legacy window would refuse here.
    pytest.param(True, None, "warn-unwired", None, "warn", id="on-legacy-warn-unwired"),
    pytest.param(True, None, "require", None, "refuse", id="on-legacy-require"),
    pytest.param(
        True,
        None,
        None,
        _DECOY_SECTION,
        "refuse",
        id="on-decoy-section",
    ),
    pytest.param(
        True,
        None,
        None,
        _DECOY_STRING,
        "refuse",
        id="on-decoy-string",
    ),
    # A reader that demanded the reviewer whatever the privacy gate said
    # would refuse every privacy-off row.
    pytest.param(False, None, None, None, "proceed", id="off-absent"),
    pytest.param(False, "require", None, None, "proceed", id="off-require"),
    pytest.param(False, 1, None, None, "proceed", id="off-wrong-type"),
    pytest.param(False, "warn-unwried", None, None, "proceed", id="off-typo"),
]


@pytest.mark.parametrize("privacy,value,legacy,decoy,outcome", POSTURE_CASES)
def test_the_review_posture_follows_the_one_parse(
    repo, privacy, value, legacy, decoy, outcome
):
    """TC-031 (SR-031: one parse, one answer): with no reviewer wired, the
    push follows the posture the parse places under [policies]. Privacy on:
    exactly `"warn-unwired"` warns and proceeds; any other value, a wrong
    type, absence, or a copy outside [policies] (another section, inside a
    string) refuses; the legacy docs/privacy-review answers when the key is
    absent. Privacy off: the posture is moot and the push proceeds."""
    root, base, head = repo
    set_privacy(root, "true" if privacy else "false")
    _declare_posture(root, value, legacy, decoy)
    proc = run_hook(root, push_line(head, base))
    said = proc.stdout + proc.stderr
    if outcome == "refuse":
        assert proc.returncode != 0, said
        assert "FAILING CLOSED" in proc.stderr, said
    else:
        assert proc.returncode == 0, said
        assert "FAILING CLOSED" not in proc.stderr, said
        assert ("WARNING" in proc.stderr) is (outcome == "warn"), said


def test_pre_push_refuses_a_kit_scripts_dir_naming_a_missing_directory(repo):
    """TC-021 (SR-020, LLR-021): one scripts-directory rule for every hook. A
    KIT_SCRIPTS_DIR naming no directory refuses the push even though the
    scaffold's scripts/ is there to fall back on."""
    root, base, head = repo
    assert (root / "scripts").is_dir()
    proc = run_hook(
        root, push_line(head, base), env_extra={"KIT_SCRIPTS_DIR": "nope-not-here"}
    )
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "cannot find the kit scripts dir" in proc.stderr, proc.stderr
    assert "REFUSING the push" in proc.stderr, proc.stderr
    assert "KIT_SCRIPTS_DIR in the delegating wrapper" in proc.stderr, proc.stderr
    assert "git config --unset core.hooksPath" in proc.stderr, proc.stderr


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


def test_multi_ref_push_scans_every_ref(repo, tmp_path):
    # L-14: the reviewer and the lint run INSIDE the hook's while-read over its
    # own stdin (the ref lines); without the < /dev/null guards a stdin-reading
    # child ate the remaining lines, so ref 2 of a two-branch push was never
    # scanned. The reviewer here deliberately slurps stdin after approving
    # ref 1; the second ref carries a leak the deterministic lint must still
    # catch — a pre-guard hook exits 0 and ships it.
    root, base, head = repo
    set_privacy(root)
    leaky = commit_file(
        root, "leak.txt", "creds at C:\\Users\\bobsmith\\secrets\n", "add data"
    )
    ran = tmp_path / "reviewer-ran.txt"
    slurp = make_reviewer(
        tmp_path,
        "slurp.sh",
        'echo ran >> "{}"\ncat >/dev/null\necho APPROVE\n'.format(_posix(ran)),
    )
    two_refs = push_line(
        head, base
    ) + "refs/heads/feature {} refs/heads/feature {}\n".format(leaky, head)
    proc = run_hook(root, two_refs, review_cmd=slurp)
    assert ran.exists(), "the stdin-slurping reviewer must have run for ref 1"
    assert proc.returncode != 0, "ref 2's leak must still block the push"
    assert "privacy lint found" in proc.stderr
    assert "refs/heads/feature" in proc.stderr, "the finding must name ref 2"


def test_bootstrap_copies_pre_push_hook(scaffold):
    hook = scaffold / HOOK
    assert hook.exists(), "bootstrap must copy the pre-push hook to .githooks/"
    assert hook.read_text(encoding="utf-8").startswith("#!/bin/sh")


@pytest.fixture
def older():
    """A real installed Python below the 3.11 floor (skips where none is)."""
    found = sub_floor_interpreter()
    if found is None:
        pytest.skip("no Python below 3.11 is installed on this host")
    return found


def test_pre_push_never_runs_on_an_older_python(repo, older):
    """WI-880, real interpreters only: with a real Python below the 3.11 floor
    the only one on PATH, the pre-push hook neither scans the outgoing range on
    it nor skips the scan: it refuses the push and names dev-setup's install."""
    root, base, head = repo
    env = dict(os.environ, PATH=older_only_path(older))
    env.pop("VIRTUAL_ENV", None)
    proc = subprocess.run(
        [shutil.which("sh"), HOOK, "origin", "https://example.invalid/repo.git"],
        cwd=str(root),
        input=push_line(head, base),
        capture_output=True,
        text=True,
        env=env,
    )
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "Traceback" not in proc.stderr, proc.stderr
    assert "dev-setup" in proc.stderr and "3.11" in proc.stderr, proc.stderr
