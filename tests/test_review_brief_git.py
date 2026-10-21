"""review_brief.py's command line on a real git repository (WI-852).

The in-process render, refusal and filing cases are in test_review_brief.py,
in the per-commit smoke tier as this script family's in-process pin. These
cases build a real temporary git repository and drive `main` through
`lane_commits`, with nothing monkeypatched: a root not on a branch, a revision
that is not a commit and a base that is not an ancestor each refuse with
exit 2 and no output file, and a review render and a filing each exit 0 and
write only their requested file. They spawn git, so this module is registered
in `tests/conftest.py`'s `SLOW_MODULES`.

A review renders only over a commit whose review bar is attested green for
the round's named tests (WI-957, TC-371): the fixture's reviewed commits carry
that attestation, written by the kit's own `Bar-Green:` writer, and the gate's
cases commit the absent, unverified, malformed, other-bar and other-tests
records and the commits above an attested one.
"""

import re
import shlex
import shutil
import subprocess
import sys

import pytest
from conftest import SCRIPTS, load_script, pin_autocrlf

if str(SCRIPTS) not in sys.path:  # the kit's script-sibling import idiom
    sys.path.insert(0, str(SCRIPTS))

from kitlib import verdict as kverdict  # noqa: E402

rb = load_script("review_brief")

TESTS = ("tests/test_a.py",)

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


def _attest_tip(root, message, tests=TESTS, bar="review", tree=None, work=None):
    """Commit the staged work (or nothing) carrying a `Bar-Green:` line written
    by the kit's one writer: by default a verified `review` record for `tests`
    over the commit's own tree and first parent. `tree` and `work` override
    the named values, so a caller writes a record that names another tree or
    another parent. Returns the new commit's full id."""
    own_tree = _git(root, "write-tree")
    parent = _git(root, "rev-parse", "HEAD")
    line = kverdict.format_bar_green(
        tree or own_tree,
        work or parent,
        bar,
        kverdict.tests_digest(tests),
        "{} bar PASS".format(bar),
    )
    return _commit_message(root, message + "\n\n" + line)


def _malformed_attest_tip(root, message, tests=TESTS):
    """Commit the staged work carrying the older `Bar-Green:` grammar, with no
    `bar=` field: a line no reader verifies."""
    line = "{} tree={} work={} tests={} review bar PASS".format(
        kverdict.BAR_GREEN,
        _git(root, "write-tree"),
        _git(root, "rev-parse", "HEAD"),
        kverdict.tests_digest(tests),
    )
    return _commit_message(root, message + "\n\n" + line)


def _commit_message(root, message):
    _git(root, "commit", "-q", "--allow-empty", "-m", message)
    return _git(root, "rev-parse", "HEAD")


def _work(root, rel, text="work\n"):
    """Write and stage one file of the lane's work."""
    (root / rel).parent.mkdir(parents=True, exist_ok=True)
    (root / rel).write_text(text, encoding="utf-8")
    _git(root, "add", "-A")


@pytest.fixture
def git_lane(tmp_path):
    """A real lane: branch `wi-900` holding the spec at `base` and one more
    commit at `tip`, attested green for the review bar over `TESTS`, and a
    `side` commit off `base` that is not on the lane."""
    root = _lane(tmp_path / "lane")
    _git(root, "init", "-q", "-b", "wi-900")
    pin_autocrlf(root)
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "base")
    base = _git(root, "rev-parse", "HEAD")
    (root / "a.txt").write_text("a\n", encoding="utf-8")
    _git(root, "add", "-A")
    tip = _attest_tip(root, "tip")
    _git(root, "checkout", "-q", "-b", "side", base)
    (root / "b.txt").write_text("b\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "side")
    side = _git(root, "rev-parse", "HEAD")
    _git(root, "checkout", "-q", "wi-900")
    out = tmp_path / "out"
    out.mkdir()
    return root, base, tip, side, out


def _review_argv(root, base, sha, out, tests=TESTS):
    argv = ["review", "--root", str(root), "--wi", "WI-900", "--base", base]
    argv += ["--sha", sha, "--scope", "full", "--scratch", str(out)]
    return argv + ["--tests", *tests, "--out", str(out / "brief.md")]


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


def test_the_reading_scope_never_shows_a_record_of_earlier_findings(git_lane):
    # WI-911: a convergence round never sees earlier
    # verdicts (review-churn revision 8). The brief's own diff command keeps
    # every record that summarizes them out of its output: the review round
    # files, the lane's decisions record and the plan's filed critiques. A
    # changed work file is still read.
    root, base, _tip, _side, out = git_lane
    records = (
        "docs/reviews/wi-900/001-REVIEW-A-1111111.md",
        "docs/decisions/wi-900.toml",
        "docs/plans/WI-900/critique-1.md",
        "docs/plans/WI-900/critique-2.md",
    )
    for rel in records + ("src/app.py", "docs/plans/WI-900/plan.md"):
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text("F1: an earlier finding\n", encoding="utf-8")
    _git(root, "add", "-A")
    tip = _attest_tip(root, "records")
    argv = _review_argv(root, base, tip, out) + ["--stance", "convergence"]
    assert rb.main(argv) == 0
    brief = (out / "brief.md").read_text(encoding="utf-8")
    command = re.search(r"`(git diff {}\.\.\.{} -- [^`]+)`".format(base, tip), brief)
    assert command, "the brief states no reading-scope command"
    words = shlex.split(command.group(1))
    shown = _git(root, *words[1:2], "--name-only", *words[2:]).splitlines()
    assert "src/app.py" in shown and "docs/plans/WI-900/plan.md" in shown
    assert [rel for rel in records if rel in shown] == []


def test_an_ordinary_review_reads_the_decisions_record(git_lane):
    # WI-911 (review-churn revision 8): only a convergence round sets the
    # earlier findings' records aside. An ordinary round's own diff command,
    # the one a loop reviewer reads too, still shows the delegated-decisions
    # record it may dissent on and the plan's filed critiques; the round files
    # stay out of every round.
    root, base, _tip, _side, out = git_lane
    kept = ("docs/decisions/wi-900.toml", "docs/plans/WI-900/critique-1.md")
    for rel in kept + ("docs/reviews/wi-900/001-REVIEW-A-1111111.md", "src/app.py"):
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text("F1: an earlier finding\n", encoding="utf-8")
    _git(root, "add", "-A")
    tip = _attest_tip(root, "records")
    assert rb.main(_review_argv(root, base, tip, out)) == 0
    brief = (out / "brief.md").read_text(encoding="utf-8")
    command = re.search(r"`(git diff {}\.\.\.{} -- [^`]+)`".format(base, tip), brief)
    assert command, "the brief states no reading-scope command"
    words = shlex.split(command.group(1))
    shown = _git(root, *words[1:2], "--name-only", *words[2:]).splitlines()
    assert [rel for rel in kept + ("src/app.py",) if rel not in shown] == []
    assert "docs/reviews/wi-900/001-REVIEW-A-1111111.md" not in shown


# --- the review renders only over an attested tip (WI-957, TC-371) ------------------


def _refused(root, out, capsys, sha, tests=TESTS):
    """The render refused `sha`: exit 2 (asserted by the caller), no brief,
    an untouched lane, and a refusal naming the reviewed commit and the step
    that records a green review bar for the round's own tests. Returns the
    refusal text for the cause the caller asserts."""
    err = capsys.readouterr().err
    assert list(out.iterdir()) == []
    assert _git(root, "status", "--porcelain", "--untracked-files=all") == ""
    assert sha in err, err
    for named in ("integrate.py attest", "--branch wi-900", "--bar review", *tests):
        assert named in err, (named, err)
    return err


def _attested_line(stdout, sha, tests=TESTS):
    """The console line naming the attested commit and its tests digest."""
    digest = kverdict.tests_digest(tests)
    return [line for line in stdout.splitlines() if sha in line and digest in line]


def test_a_tip_with_no_attestation_refuses_naming_the_attest_command(git_lane, capsys):
    # TC-371. Adequacy witness: a render that ignores the record (today's)
    # writes the brief and exits 0.
    root, base, _tip, _side, out = git_lane
    _work(root, "src/app.py")
    _git(root, "commit", "-q", "-m", "unattested work")
    sha = _git(root, "rev-parse", "HEAD")
    assert rb.main(_review_argv(root, base, sha, out)) == 2
    err = _refused(root, out, capsys, sha)
    assert "has no verified attestation" in err, err
    assert "carries 0 `Bar-Green:` lines" in err, err


def _unverified_commit(root, case, tip):
    """A work commit on the lane whose record does not verify, and the values
    the refusal must name: (sha, cause, values)."""
    if case == "another-tree":
        _work(root, "src/other.py")
        other = _git(root, "write-tree")
        _work(root, "src/app.py")
        sha = _attest_tip(root, "names another tree", tree=other)
        return sha, "names tree", (other, _git(root, "rev-parse", sha + "^{tree}"))
    if case == "another-parent":
        # The rebase and cherry-pick case: the same tree over another parent,
        # the record still naming the parent it was attested over.
        _work(root, "src/app.py")
        attested = _attest_tip(root, "attested over the tip")
        _git(root, "reset", "-q", "--hard", tip)
        _git(root, "commit", "-q", "--allow-empty", "-m", "another parent")
        moved = _git(root, "rev-parse", "HEAD")
        _git(root, "cherry-pick", attested)
        sha = _git(root, "rev-parse", "HEAD")
        trees = [_git(root, "rev-parse", rev + "^{tree}") for rev in (sha, attested)]
        assert trees[0] == trees[1], "the picked commit's tree moved"
        return sha, "first parent", (tip, moved)
    _work(root, "src/app.py")
    return _malformed_attest_tip(root, "the older grammar"), "grammar", ()


@pytest.mark.parametrize("case", ["another-tree", "another-parent", "malformed"])
def test_an_attestation_that_does_not_name_the_tip_refuses_naming_the_cause(
    git_lane, capsys, case
):
    # TC-371. Adequacy witness: a render that reads only the label, or trusts
    # a record's `tree=`/`work=` without comparing them, renders here.
    root, base, tip, _side, out = git_lane
    sha, cause, values = _unverified_commit(root, case, tip)
    assert kverdict.bar_attestation(root, sha) is None, "the record verifies"
    assert rb.main(_review_argv(root, base, sha, out)) == 2
    err = _refused(root, out, capsys, sha)
    assert cause in err, err
    for value in values:
        assert value in err, (value, err)


def test_a_landing_attestation_refuses_naming_both_bars(git_lane, capsys):
    # TC-371. A refresh's verified landing record is another bar, never a
    # review one. Adequacy witness: a render that accepts any verified
    # record renders here.
    root, base, _tip, _side, out = git_lane
    _work(root, "src/trunk.py")
    sha = _attest_tip(root, "refresh: wi-900 onto trunk 0123456789", bar="landing")
    assert kverdict.bar_attestation(root, sha).bar == "landing"
    assert rb.main(_review_argv(root, base, sha, out)) == 2
    err = _refused(root, out, capsys, sha)
    assert "a verified `landing` attestation, not a `review` one" in err, err


def test_a_review_attestation_for_other_tests_refuses_naming_both_digests(
    git_lane, capsys
):
    # TC-371. Adequacy witness: a render that checks the bar but not the
    # tests digest renders here.
    root, base, tip, _side, out = git_lane
    other = ("tests/test_b.py",)
    assert rb.main(_review_argv(root, base, tip, out, tests=other)) == 2
    err = _refused(root, out, capsys, tip, tests=other)
    assert kverdict.tests_digest(TESTS) in err, err
    assert kverdict.tests_digest(other) in err, err


def test_a_matching_review_attestation_renders_and_names_it(git_lane, capsys):
    # TC-371. Another spelling of the same set has the same digest. Adequacy
    # witness: a render that compares the paths as typed refuses here, and
    # one that never reads the record names no attested commit.
    root, base, tip, _side, out = git_lane
    spelled = ("./tests\\test_a.py",)
    assert kverdict.bar_attestation(root, tip).bar == "review"
    assert rb.main(_review_argv(root, base, tip, out, tests=spelled)) == 0
    assert [p.name for p in out.iterdir()] == ["brief.md"]
    assert _attested_line(capsys.readouterr().out, tip), "no attested-commit line"


def test_record_only_commits_above_the_attested_one_render(git_lane, capsys):
    # TC-371. An empty commit, a round file and a telemetry fragment above
    # the attested commit force no new bar. Adequacy witness: a render that
    # reads only the reviewed commit's own record refuses here.
    root, base, tip, _side, out = git_lane
    _git(root, "commit", "-q", "--allow-empty", "-m", "an empty commit")
    for rel in ("docs/reviews/wi-900/001-REVIEW-A-1111111.md", "docs/log.d/wi-900.md"):
        _work(root, rel, "a record\n")
        _git(root, "commit", "-q", "-m", "record " + rel)
    head = _git(root, "rev-parse", "HEAD")
    assert rb.main(_review_argv(root, base, head, out)) == 0
    assert [p.name for p in out.iterdir()] == ["brief.md"]
    assert _attested_line(capsys.readouterr().out, tip), "no attested-commit line"


def _empty_commits(root, count):
    """Stack `count` empty commits on the lane's branch in one fast-import
    stream (a git process per commit would dominate the case). Returns the
    new tip."""
    parent = _git(root, "rev-parse", "HEAD")
    stream = []
    for n in range(count):
        message = "record {}".format(n).encode()
        stream += [b"commit refs/heads/wi-900", b"committer t <t@example.com> 0 +0000"]
        stream += [b"data %d" % len(message), message]
        if n == 0:
            stream.append(b"from " + parent.encode())
        stream.append(b"")
    subprocess.run(
        [shutil.which("git"), "-C", str(root), "fast-import", "--quiet", "--force"],
        input=b"\n".join(stream) + b"\n",
        check=True,
        capture_output=True,
    )
    _git(root, "reset", "-q", "--hard")
    return _git(root, "rev-parse", "HEAD")


def test_a_search_past_the_walk_bound_refuses(git_lane, capsys):
    # TC-371. The walk below the reviewed commit is bounded: one bound short
    # of it the attested commit still stands, one past it the render refuses
    # naming the bound. Adequacy witness: an unbounded walk renders past the
    # bound, and one that refuses below the bound refuses the first render.
    root, base, tip, _side, out = git_lane
    bound = kverdict._MAX_GOVERNING_WALK
    head = _empty_commits(root, bound - 1)
    assert rb.main(_review_argv(root, base, head, out)) == 0
    assert _attested_line(capsys.readouterr().out, tip), "no attested-commit line"
    (out / "brief.md").unlink()
    head = _empty_commits(root, 2)
    assert rb.main(_review_argv(root, base, head, out)) == 2
    err = _refused(root, out, capsys, head)
    assert "no verified attestation within 64 record-only commits" in err, err


@pytest.mark.parametrize("rel", ["src/app.py", "docs/decisions/wi-900.toml"])
def test_a_work_commit_above_the_attested_one_refuses(git_lane, capsys, rel):
    # TC-371. The decisions record is not a record path, so it needs the bar
    # too. Adequacy witness: a walk that steps over any commit renders here.
    root, base, _tip, _side, out = git_lane
    _work(root, rel)
    _git(root, "commit", "-q", "-m", "work above the attested commit")
    sha = _git(root, "rev-parse", "HEAD")
    assert rb.main(_review_argv(root, base, sha, out)) == 2
    err = _refused(root, out, capsys, sha)
    assert "changes non-record paths over its parent" in err, err
