"""The train-build commit-message floor — the WI-282 addition to the commit-msg
hook (project-trajectory/hooks/commit-msg, copied to .githooks/commit-msg).

On a branch matching llm/train/*, a substantive build commit MUST carry a
parseable `WI: WI-<n>` trailer — the exact property
agent_dispatch.reviewed_train_head reads to resolve a train's reviewed head. A
malformed trailer block (a blank line interposed in the trailer paragraph) makes
git DROP the trailer, so the resolver SKIPS the commit and the integrator can
grade a stale verdict — the live 2026-07-23 failure (train p0-g3-WI-281-9ae9,
commit 45637d2) that parked an APPROVED train as rework. This floor fails that
one-line slip at commit time.

The floor is pure sh (it runs BEFORE the hook's Python/scripts discovery), so it
holds even on a Python-less box. The sanctioned integrate:/telemetry:/review:/
blocked: coordinator commits (subject prefix) and a blocked disposition
(Blocked-WI: trailer) stay legal. The hook runs via git's bundled sh on every
platform; where sh is absent the end-to-end tests skip.
"""

import os
import shutil
import subprocess

import pytest

from conftest import KIT, load_script, make_minimal_project

SHIPPED_HOOK = KIT / "hooks" / "commit-msg"
TRAIN = "llm/train/p0-g3-WI-282-eb40"

# A well-formed build message: the trailer paragraph is the LAST block, trailers
# only — what reviewed_train_head resolves a `WI:` token from.
GOOD = (
    "WI-282: enforce the trailer\n\nsome body\n\nWI: WI-282\nTrain: t\nBase: abc123\n"
)
# The regression shape: a blank line interposed IN the trailer block — a human
# reads a `WI:` line, but git drops every trailer above the blank, so the
# integrator's %(trailers:key=WI) read returns nothing.
MALFORMED = "WI-282: enforce the trailer\n\nWI: WI-282\n\nTrain: t\nBase: abc123\n"


def _sh_or_skip():
    sh = shutil.which("sh")
    if not sh or not shutil.which("git"):
        pytest.skip("needs a POSIX shell and git on PATH")
    return sh


def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=False)


@pytest.fixture
def train_repo(tmp_path):
    """A minimal git repo checked out on a train branch. The WI floor runs before
    the hook's Python/scripts discovery, so no scaffold is needed here."""
    _sh_or_skip()
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    _git(repo, "commit", "-q", "--allow-empty", "-m", "seed")
    _git(repo, "checkout", "-q", "-b", TRAIN)
    return repo


def _hook(repo, message, hook=None, env=None):
    (repo / "MSG.txt").write_text(message, encoding="utf-8")
    return subprocess.run(
        [shutil.which("sh"), str(hook or SHIPPED_HOOK), "MSG.txt"],
        cwd=str(repo),
        capture_output=True,
        text=True,
        env=env,
    )


def test_malformed_trailer_block_is_refused(train_repo):
    # THE regression: a blank line inside the trailer block. git drops the `WI:`
    # trailer, so the floor must refuse with an actionable, WI-naming message that
    # names the exact fix (the blank-line slip).
    r = _hook(train_repo, MALFORMED)
    assert r.returncode != 0, "a malformed trailer block must be refused"
    assert "WI-282" in r.stderr and "blank line" in r.stderr.lower(), r.stderr


def test_good_build_trailer_passes(train_repo):
    r = _hook(train_repo, GOOD)
    assert r.returncode == 0, r.stdout + r.stderr


def test_no_trailer_at_all_is_refused(train_repo):
    r = _hook(train_repo, "WI-282: work\n\njust a body, no trailer\n")
    assert r.returncode != 0


def test_wi_trailer_with_a_non_wi_value_is_refused(train_repo):
    # A `WI:` trailer whose value is not a WI-<n> token is not the property the
    # resolver keys on — refuse, matching reviewed_train_head's WI_TOKEN_RE.
    r = _hook(train_repo, "subj\n\nWI: banana\nTrain: t\nBase: abc\n")
    assert r.returncode != 0


@pytest.mark.parametrize(
    "subject",
    [
        "integrate: train t (WI-282)",
        "telemetry: session 001 review scoreboard",
        "review: record WI-282 verdict",
        "blocked: WI-282 (train t)",
    ],
)
def test_sanctioned_subject_prefixes_pass_without_a_trailer(train_repo, subject):
    # The coordinator/bookkeeping shapes legitimately carry no WI trailer.
    r = _hook(train_repo, subject + "\n\na body with no WI trailer\n")
    assert r.returncode == 0, r.stdout + r.stderr


def test_blocked_wi_trailer_passes_with_a_free_form_subject(train_repo):
    # A worker's blocked disposition carries Blocked-WI (+ BlockRef), not WI, and
    # its subject is free-form — the trailer, not a prefix, exempts it.
    r = _hook(train_repo, "partial evidence\n\nBlocked-WI: WI-282\nBlockRef: OI-4\n")
    assert r.returncode == 0, r.stdout + r.stderr


def test_off_train_branch_is_vacuous(train_repo):
    # The floor applies only on llm/train/*; a malformed message elsewhere passes.
    _git(train_repo, "checkout", "-q", "-b", "feature/x")
    r = _hook(train_repo, MALFORMED)
    assert r.returncode == 0, r.stdout + r.stderr


def test_floor_holds_without_python(train_repo):
    # The pure-sh floor's payoff over a Python helper: shadow python3/python with
    # fakes that exit nonzero and confirm a slip is STILL refused, where the
    # Python message scan below would only skip.
    fakebin = train_repo / "fakebin"
    fakebin.mkdir()
    for name in ("python3", "python"):
        cand = fakebin / name
        cand.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        cand.chmod(0o755)
    env = dict(os.environ, PATH=str(fakebin) + os.pathsep + os.environ.get("PATH", ""))
    r = _hook(train_repo, MALFORMED, env=env)
    assert r.returncode != 0, "the pure-sh floor must refuse a slip even without Python"


def test_hook_sanctioned_prefixes_mirror_the_shared_constant():
    # The hook hardcodes the sanctioned prefixes in sh; keep them in step with
    # agent_common.SANCTIONED_TRAIN_SUBJECT_PREFIXES (the reviewed-head diagnostic
    # reads the constant, the floor reads the sh case — they must never disagree).
    ac = load_script("agent_common")
    assert ac.SANCTIONED_TRAIN_SUBJECT_PREFIXES == (
        "integrate:",
        "telemetry:",
        "review:",
        "blocked:",
    )
    text = SHIPPED_HOOK.read_text(encoding="utf-8")
    assert "integrate:*|telemetry:*|review:*|blocked:*" in text


def test_end_to_end_through_the_installed_hook(scaffold):
    # The shipped/downstream shape: .githooks/commit-msg is the copied hook over a
    # real scaffold (default scripts/ layout, so the message scan runs after the
    # floor). On a train branch, a slip is aborted and a valid trailer accepted.
    sh = _sh_or_skip()
    make_minimal_project(scaffold)
    _git(scaffold, "init")
    _git(scaffold, "config", "user.email", "loop@example.com")
    _git(scaffold, "config", "user.name", "Loop Test")
    _git(scaffold, "add", "-A")
    _git(scaffold, "commit", "-q", "-m", "seed")
    _git(scaffold, "checkout", "-q", "-b", TRAIN)

    def commit(message):
        (scaffold / "MSG.txt").write_text(message, encoding="utf-8")
        return subprocess.run(
            [sh, ".githooks/commit-msg", "MSG.txt"],
            cwd=str(scaffold),
            capture_output=True,
            text=True,
        )

    blocked = commit(MALFORMED)
    assert blocked.returncode != 0 and "WI-282" in blocked.stderr, blocked.stderr
    ok = commit(GOOD)
    assert ok.returncode == 0, ok.stdout + ok.stderr
