"""`kitlib.git`'s lane-commit walk, in process (TC-383).

The per-commit rules (text then act, the adoption record, the plan gate, the
held-status step and the merge slot) share one traversal: the HEAD / MERGE_HEAD
read of the commit being made, the walk over a listed range asking each rider
of each commit, and a staged squash's HEAD..tip step. These tests pin that
owner without building a repository: `kitlib.git.git_out` is replaced by a fake
answering the argv each read sends, and the riders are plain functions that
record what they were asked.

What an unlistable range means is the caller's own: `squash_lines` hands back
the line the caller passed in, or None when it passed None.
"""

from kitlib import git as kgit

HEAD_ID = "a" * 40
TIP_ID = "b" * 40


def _fake_git(monkeypatch, answers):
    """Replace `kitlib.git.git_out` with a fake: `answers(args)` gives the
    stdout (or None) for each argv; every argv is recorded in order."""
    seen = []

    def fake(_root, args, stdin=None):
        seen.append(list(args))
        return answers(list(args))

    monkeypatch.setattr(kgit, "git_out", fake)
    return seen


def _recording_riders(reports):
    """Two riders, `first` and `second`, each recording `(name, rev)` when
    asked and answering `reports[(name, rev)]` (default: no lines)."""
    asked = []

    def rider(name):
        def rule(_root, rev):
            asked.append((name, rev))
            return list(reports.get((name, rev), []))

        rule.__name__ = name
        return rule

    return (rider("first"), rider("second")), asked


def test_the_walk_asks_each_rider_of_each_commit_in_order_and_skips_empty_reports():
    assert hasattr(kgit, "lane_commit_walk")
    riders, asked = _recording_riders(
        {("second", "c1"): ["c1 two"], ("first", "c3"): ["c3 one", "c3 more"]}
    )
    found = list(kgit.lane_commit_walk("root", ["c1", "c2", "c3"], riders))
    assert asked == [
        ("first", "c1"),
        ("second", "c1"),
        ("first", "c2"),
        ("second", "c2"),
        ("first", "c3"),
        ("second", "c3"),
    ]
    assert found == [("c1", ["c1 two"]), ("c3", ["c3 one", "c3 more"])]


def test_the_walk_is_lazy_so_a_caller_stopping_at_the_first_report_judges_no_later_commit():
    assert hasattr(kgit, "lane_commit_walk")
    riders, asked = _recording_riders({("first", "c2"): ["held"]})
    walk = kgit.lane_commit_walk("root", ["c1", "c2", "c3"], riders)
    assert asked == [], "nothing is judged before the caller asks"
    assert next(walk, None) == ("c2", ["held"])
    assert asked == [("first", "c1"), ("second", "c1"), ("first", "c2")]


def test_staged_heads_reads_head_and_merge_head_and_answers_empty_when_absent(
    monkeypatch,
):
    assert hasattr(kgit, "staged_heads")

    def merging(args):
        if args[0] == "rev-parse" and args[-1] == "MERGE_HEAD":
            return TIP_ID + "\n"
        if args[0] == "rev-parse" and args[-1] == "HEAD":
            return HEAD_ID + "\n"
        return None

    seen = _fake_git(monkeypatch, merging)
    assert kgit.staged_heads("root") == (HEAD_ID, TIP_ID)
    assert {args[-1] for args in seen} == {"HEAD", "MERGE_HEAD"}
    assert all(args[0] == "rev-parse" and "--verify" in args for args in seen)

    def plain(args):
        return HEAD_ID + "\n" if args[-1] == "HEAD" else None

    _fake_git(monkeypatch, plain)
    assert kgit.staged_heads("root") == (HEAD_ID, "")

    _fake_git(monkeypatch, lambda _args: None)
    assert kgit.staged_heads("root") == ("", "")


def _range_git(contains, listing):
    """A fake answering the ancestry test with `contains` and the range
    listing with `listing` (None for a range git cannot list)."""

    def answers(args):
        if args[:2] == ["merge-base", "--is-ancestor"]:
            return "" if contains else None
        if args[0] == "rev-list":
            return listing
        return None

    return answers


def test_squash_lines_is_none_when_the_tip_does_not_contain_head(monkeypatch):
    assert hasattr(kgit, "squash_lines")
    seen = _fake_git(monkeypatch, _range_git(False, "c1\n"))
    riders, asked = _recording_riders({("first", "c1"): ["held"]})
    unlisted = ["cannot list"]
    assert kgit.squash_lines("root", HEAD_ID, TIP_ID, riders, unlisted) is None
    assert ["merge-base", "--is-ancestor", HEAD_ID, TIP_ID] in seen
    assert asked == []


def test_squash_lines_answers_the_callers_line_when_the_range_cannot_be_listed(
    monkeypatch,
):
    assert hasattr(kgit, "squash_lines")
    seen = _fake_git(monkeypatch, _range_git(True, None))
    riders, asked = _recording_riders({})
    unlisted = ["the caller's own line"]
    assert kgit.squash_lines("root", HEAD_ID, TIP_ID, riders, unlisted) == unlisted
    assert ["rev-list", "--reverse", HEAD_ID + ".." + TIP_ID] in seen
    assert kgit.squash_lines("root", HEAD_ID, TIP_ID, riders, None) is None
    assert asked == []


def test_squash_lines_returns_every_commits_lines_oldest_first(monkeypatch):
    assert hasattr(kgit, "squash_lines")
    seen = _fake_git(monkeypatch, _range_git(True, "c1\nc2\nc3\n"))
    riders, asked = _recording_riders(
        {
            ("first", "c1"): ["c1 one"],
            ("second", "c1"): ["c1 two"],
            ("second", "c3"): ["c3 two"],
        }
    )
    lines = kgit.squash_lines("root", HEAD_ID, TIP_ID, riders, ["unlisted"])
    assert lines == ["c1 one", "c1 two", "c3 two"]
    assert ["rev-list", "--reverse", HEAD_ID + ".." + TIP_ID] in seen
    assert [rev for _name, rev in asked] == ["c1", "c1", "c2", "c2", "c3", "c3"]
