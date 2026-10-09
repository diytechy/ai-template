"""review_brief.py's command line on a real git repository (WI-852).

The in-process render, refusal and filing cases are in test_review_brief.py,
in the per-commit smoke tier as this script family's in-process pin. These
cases build a real temporary git repository and drive `main` through
`lane_commits`, with nothing monkeypatched: a root not on a branch, a revision
that is not a commit and a base that is not an ancestor each refuse with
exit 2 and no output file, and a review render and a filing each exit 0 and
write only their requested file. They spawn git, so this module is registered
in `tests/conftest.py`'s `SLOW_MODULES`.
"""

import shutil
import subprocess

import pytest
from conftest import load_script, pin_autocrlf

rb = load_script("review_brief")

SPEC = """+++
id = "WI-900"
title = "A lane under review"
+++

## Done-when

- It works.
"""


def _lane(root):
    spec = root / "docs" / "work" / "active" / "wi-900" / "WI-900-a-lane.md"
    spec.parent.mkdir(parents=True)
    spec.write_text(SPEC, encoding="utf-8")
    return root


# --- the command line on a real git repository ---------------------------------------


def _git(root, *args):
    done = subprocess.run(
        [shutil.which("git"), "-C", str(root), "-c", "user.name=t"]
        + ["-c", "user.email=t@example.com", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return done.stdout.strip()


@pytest.fixture
def git_lane(tmp_path):
    """A real lane: branch `wi-900` holding the spec at `base` and one more
    commit at `tip`, and a `side` commit off `base` that is not on the lane."""
    root = _lane(tmp_path / "lane")
    _git(root, "init", "-q", "-b", "wi-900")
    pin_autocrlf(root)
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "base")
    base = _git(root, "rev-parse", "HEAD")
    (root / "a.txt").write_text("a\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "tip")
    tip = _git(root, "rev-parse", "HEAD")
    _git(root, "checkout", "-q", "-b", "side", base)
    (root / "b.txt").write_text("b\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "side")
    side = _git(root, "rev-parse", "HEAD")
    _git(root, "checkout", "-q", "wi-900")
    out = tmp_path / "out"
    out.mkdir()
    return root, base, tip, side, out


def _review_argv(root, base, sha, out):
    argv = ["review", "--root", str(root), "--wi", "WI-900", "--base", base]
    argv += ["--sha", sha, "--scope", "full", "--scratch", str(out)]
    return argv + ["--tests", "tests/test_a.py", "--out", str(out / "brief.md")]


@pytest.mark.parametrize(
    "case, why",
    [
        ("detached", "is not on a branch"),
        ("not-a-commit", "'no-such-rev' is not a commit"),
        ("not-an-ancestor", "is not an ancestor of"),
    ],
)
def test_the_command_line_refuses_a_lane_the_git_reads_reject(
    git_lane, capsys, case, why
):
    root, base, tip, side, out = git_lane
    if case == "detached":
        _git(root, "checkout", "-q", "--detach", tip)
    if case == "not-a-commit":
        base = "no-such-rev"
    if case == "not-an-ancestor":
        base = side
    assert rb.main(_review_argv(root, base, tip, out)) == 2
    assert why in capsys.readouterr().err
    assert list(out.iterdir()) == []
    assert _git(root, "status", "--porcelain", "--untracked-files=all") == ""


def test_a_review_render_exits_zero_and_writes_only_the_brief(git_lane):
    root, base, tip, _side, out = git_lane
    assert rb.main(_review_argv(root, base[:8], "HEAD", out)) == 0
    assert [p.name for p in out.iterdir()] == ["brief.md"]
    brief = (out / "brief.md").read_text(encoding="utf-8")
    assert "`{}..{}`".format(base, tip) in brief
    assert "Reviewed: {}".format(tip) in brief
    assert _git(root, "status", "--porcelain", "--untracked-files=all") == ""
    # A reviewed commit behind the lane's tip bounds every range the brief
    # states; the later commit is never in its reading scope.
    (root / "c.txt").write_text("c\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "after the reviewed commit")
    (out / "brief.md").unlink()
    assert rb.main(_review_argv(root, base, tip[:9], out)) == 0
    brief = (out / "brief.md").read_text(encoding="utf-8")
    assert "git diff {}...{} --".format(base, tip) in brief
    assert "...HEAD" not in brief and "Reviewed: {}".format(tip) in brief


def test_filing_a_review_exits_zero_and_writes_only_the_round_file(git_lane):
    root, _base, tip, _side, out = git_lane
    verdict = out / "v.md"
    verdict.write_text(
        "Reviewed: {}\n\nVERDICT: APPROVE findings=0\n".format(tip), encoding="utf-8"
    )
    argv = ["file", "--root", str(root), "--review", str(verdict)]
    assert rb.main(argv + ["--sha", "HEAD", "--scope", "full"]) == 0
    status = _git(root, "status", "--porcelain", "--untracked-files=all")
    assert status == "?? docs/reviews/wi-900/001-REVIEW-A-{}.md".format(tip[:7])
    assert [p.name for p in out.iterdir()] == ["v.md"]
    # A branch the round reader cannot read as a review scope refuses with
    # exit 2 and files nothing (its `/` would nest the round a level deeper).
    _git(root, "checkout", "-q", "-b", "feature/wi-900")
    assert rb.main(argv + ["--sha", "HEAD", "--scope", "full"]) == 2
    status = _git(root, "status", "--porcelain", "--untracked-files=all")
    assert status == "?? docs/reviews/wi-900/001-REVIEW-A-{}.md".format(tip[:7])
    # A branch named for the rollup generator's own directory refuses too, in
    # any case: the generator owns that directory and prunes what it did not
    # write, and a case-insensitive filesystem makes `Rollup` the same one.
    # Each branch is deleted before the next, since a case-insensitive ref
    # store cannot hold `rollup` and `Rollup` side by side.
    for name in ("rollup", "Rollup", "ROLLUP"):
        _git(root, "checkout", "-q", "-b", name)
        assert rb.main(argv + ["--sha", "HEAD", "--scope", "full"]) == 2
        status = _git(root, "status", "--porcelain", "--untracked-files=all")
        assert status == "?? docs/reviews/wi-900/001-REVIEW-A-{}.md".format(tip[:7])
        _git(root, "checkout", "-q", "--detach")
        _git(root, "branch", "-q", "-D", name)
