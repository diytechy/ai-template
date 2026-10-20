"""The `Bar-Green:` attestation: one grammar, one verifier, one tests digest
(WI-956), and the peel that must never read a `review` attestation.

The line is

    Bar-Green: tree=<40 hex> work=<40 hex> bar=<review|landing|no-bar> tests=<64 hex|none> <summary>

and it is an attestation only when it is the message's one column-0 label line,
its `tree=` and `work=` are the commit's own tree and first parent, and its bar
is in the closed set. Every refusal below is driven beside the honest commit it
differs from, so a verifier that refused everything fails here too.

The peel half is the one that destroys work when it is wrong: `work_tip` feeds
the refresh's `reset --hard`, so a `review` attestation sitting on the tip (a
build round's own record of green) must never be peeled, while a verified
`landing` or `no-bar` refresh still is.

Registered in `tests/conftest.py`'s `SLOW_MODULES`: each case but the digest's
commits to a real git repository.
"""

import re
import sys

import pytest
from conftest import SCRIPTS, env_gate_skipif
from integrate_fixtures import _commit, _git, _rev, git_repo

if str(SCRIPTS) not in sys.path:  # the kit's script-sibling import idiom
    sys.path.insert(0, str(SCRIPTS))

from kitlib import verdict as kv  # noqa: E402

pytestmark = env_gate_skipif("git")

BRANCH = "main"
DIGEST = "ab" * 32  # a well-formed tests digest, as a literal
HEX64 = re.compile(r"[0-9a-f]{64}")


def _repo(tmp_path):
    return git_repo(tmp_path, branch=BRANCH)


def _line(tree, work, bar="landing", tests="none", summary="bar PASS (2 steps)"):
    """A `Bar-Green:` line composed here, field by field, so the refusal cases
    pin the grammar itself rather than whatever the writer emits. `None` drops
    a field."""
    fields = ["tree=" + tree, "work=" + work]
    if bar is not None:
        fields.append("bar=" + bar)
    if tests is not None:
        fields.append("tests=" + tests)
    return "Bar-Green: " + " ".join(fields + [summary])


def _commit_naming(root, trailer_for, subject="WI-401: a work commit"):
    """Stage one new work file, name the tree the commit will have and the
    parent it will sit on, and commit a message whose body is
    `trailer_for(tree, parent)`. Returns `(sha, tree, parent)`."""
    n = len(list(root.glob("work-*.txt")))
    (root / "work-{}.txt".format(n)).write_text(
        "work {}\n".format(n), encoding="utf-8", newline="\n"
    )
    _git(root, "add", "-A")
    tree = _git(root, "write-tree").strip()
    parent = _rev(root, "HEAD")
    _commit(root, subject + "\n\n" + trailer_for(tree, parent))
    return _rev(root, "HEAD"), tree, parent


def _refresh_subject():
    return kv.refresh_subject(BRANCH) + "0123456789"


def _honest(root, bar="landing", subject="WI-401: a work commit"):
    """The control: a commit whose line names its own tree and parent."""
    return _commit_naming(root, lambda t, p: _line(t, p, bar=bar), subject)[0]


# --- the grammar and the verifier --------------------------------------------


@pytest.mark.parametrize("bar", ["review", "landing", "no-bar"])
def test_a_trailer_naming_its_own_tree_and_parent_verifies_for_each_bar(tmp_path, bar):
    # The writer and the verifier agree: what `format_bar_green` writes, on the
    # commit whose tree and parent it names, reads back field for field.
    root = _repo(tmp_path)
    sha, tree, parent = _commit_naming(
        root, lambda t, p: kv.format_bar_green(t, p, bar, DIGEST, "a summary")
    )
    attested = kv.bar_attestation(root, sha)
    assert attested is not None, _git(root, "log", "-1", "--format=%B", sha)
    assert (attested.tree, attested.work) == (tree, parent)
    assert (attested.bar, attested.tests, attested.summary) == (
        bar,
        DIGEST,
        "a summary",
    )


def test_a_wrong_tree_is_not_an_attestation(tmp_path):
    # `tree=` names the parent's tree, a real tree but not this commit's: the
    # line rode onto content it does not describe.
    root = _repo(tmp_path)
    assert kv.bar_attestation(root, _honest(root)) is not None
    parent_tree = _rev(root, "HEAD^{tree}")
    sha, _tree, _parent = _commit_naming(root, lambda t, p: _line(parent_tree, p))
    assert kv.bar_attestation(root, sha) is None


def test_a_wrong_parent_is_not_an_attestation(tmp_path):
    # `work=` names the grandparent, a real commit but not this one's parent:
    # what a rebase or a cherry-pick carries the line onto.
    root = _repo(tmp_path)
    honest = _honest(root)
    assert kv.bar_attestation(root, honest) is not None
    grandparent = _rev(root, honest + "^1")
    sha, _tree, _parent = _commit_naming(root, lambda t, p: _line(t, grandparent))
    assert kv.bar_attestation(root, sha) is None


def test_a_trailer_without_bar_is_not_an_attestation(tmp_path):
    # The old grammar, on a refresh subject, with a true tree and parent: it is
    # not read at all (no legacy path), so the refresh verifier refuses it too.
    root = _repo(tmp_path)
    honest = _honest(root, subject=_refresh_subject())
    assert kv.bar_attestation(root, honest) is not None
    sha, _tree, _parent = _commit_naming(
        root,
        lambda t, p: _line(t, p, bar=None, tests=None),
        subject=_refresh_subject(),
    )
    assert kv.refresh_attestation(root, BRANCH, sha) is None
    assert kv.bar_attestation(root, sha) is None


def test_an_unknown_bar_is_not_an_attestation(tmp_path):
    # The bar set is closed: a bar outside it is refused even with a true tree
    # and parent and the refresh subject.
    root = _repo(tmp_path)
    assert kv.bar_attestation(root, _honest(root)) is not None
    sha, _tree, _parent = _commit_naming(
        root, lambda t, p: _line(t, p, bar="nightly"), subject=_refresh_subject()
    )
    assert kv.refresh_attestation(root, BRANCH, sha) is None
    assert kv.bar_attestation(root, sha) is None


def test_a_trailer_without_tests_is_not_an_attestation(tmp_path):
    root = _repo(tmp_path)
    assert kv.bar_attestation(root, _honest(root)) is not None
    sha, _tree, _parent = _commit_naming(root, lambda t, p: _line(t, p, tests=None))
    assert kv.bar_attestation(root, sha) is None


@pytest.mark.parametrize(
    "lead", ["see ", "> ", "  "], ids=["after-text", "quoted", "indented"]
)
def test_a_trailer_quoted_mid_line_is_not_an_attestation(tmp_path, lead):
    # A true line that does not start at column 0 is a quotation of an
    # attestation, not one: the label counts only as the line's first bytes.
    root = _repo(tmp_path)
    assert kv.bar_attestation(root, _honest(root)) is not None
    sha, _tree, _parent = _commit_naming(root, lambda t, p: lead + _line(t, p))
    assert kv.bar_attestation(root, sha) is None


def test_two_label_lines_are_not_an_attestation(tmp_path):
    # Two true lines naming two bars: the message attests no single bar, so it
    # attests none.
    root = _repo(tmp_path)
    assert kv.bar_attestation(root, _honest(root)) is not None
    sha, _tree, _parent = _commit_naming(
        root,
        lambda t, p: _line(t, p, bar="landing") + "\n" + _line(t, p, bar="review"),
    )
    assert kv.bar_attestation(root, sha) is None


# --- the tests digest ---------------------------------------------------------

NAMED = ["tests/test_a.py", "tests/test_b.py"]


@pytest.mark.parametrize(
    "spelling",
    [
        ["tests/test_b.py", "tests/test_a.py"],
        ["tests/test_a.py", "tests/test_b.py", "tests/test_a.py"],
        ["./tests/test_a.py", "tests/test_b.py"],
        ["tests\\test_a.py", "tests/test_b.py"],
    ],
    ids=["reordered", "duplicated", "dot-slash", "backslash"],
)
def test_the_tests_digest_is_the_same_for_the_same_set_in_any_order(spelling):
    digest = kv.tests_digest(NAMED)
    assert HEX64.fullmatch(digest), digest
    assert kv.tests_digest(spelling) == digest


@pytest.mark.parametrize(
    "other",
    [
        NAMED + ["tests/test_c.py"],
        ["tests/test_a.py", "tests/test_c.py"],
        [],
    ],
    ids=["one-added", "one-swapped", "empty"],
)
def test_the_tests_digest_differs_for_a_different_set(other):
    digest = kv.tests_digest(NAMED)
    assert HEX64.fullmatch(digest), digest
    assert kv.tests_digest(other) != digest
    if not other:
        assert kv.tests_digest(other) == "none"


# --- the peel -----------------------------------------------------------------


def _review_on_refresh_subject(root):
    """A commit carrying the refresh subject AND a true `review` line: the
    sharpest shape, since only the bar field tells it from a refresh."""
    return _commit_naming(
        root,
        lambda t, p: _line(t, p, bar="review", tests=DIGEST),
        subject=_refresh_subject(),
    )[0]


def _is_verified_review(root, sha):
    attested = kv.bar_attestation(root, sha)
    return attested is not None and attested.bar == "review"


def test_work_tip_never_peels_a_review_attestation(tmp_path):
    # `work_tip` feeds `reset --hard`: peeling the review commit would drop the
    # build round it recorded. The peel is asserted first, then that what was
    # not peeled really is a verified review attestation.
    root = _repo(tmp_path)
    sha = _review_on_refresh_subject(root)
    assert kv.work_tip(root, BRANCH) == sha, "the review attestation was peeled"
    assert _is_verified_review(root, sha)


def test_governing_rev_never_peels_a_review_attestation(tmp_path):
    # The same commit carries a work change, so the verdict governs at it, not
    # at its parent.
    root = _repo(tmp_path)
    sha = _review_on_refresh_subject(root)
    assert kv.governing_rev(root, BRANCH) == sha, "the review attestation was peeled"
    assert _is_verified_review(root, sha)


@pytest.mark.parametrize("bar", ["landing", "no-bar"])
def test_a_verified_refresh_still_peels_under_the_new_grammar(tmp_path, bar):
    """Characterization: the peel of a verified refresh holds today and must
    survive the narrowing. Adequacy witness: a verifier that stopped reading
    the `bar=` field as part of a refresh line, or that admitted only one of
    `landing` and `no-bar`, leaves the refresh on the tip, and both readers
    then answer the refresh commit instead of the work commit under it."""
    root = _repo(tmp_path)
    work, _tree, _parent = _commit_naming(root, lambda t, p: "no trailer")
    refresh, _tree, parent = _commit_naming(
        root, lambda t, p: _line(t, p, bar=bar), subject=_refresh_subject()
    )
    assert parent == work and refresh != work
    assert kv.work_tip(root, BRANCH) == work
    assert kv.governing_rev(root, BRANCH) == work
