"""The expected-failure marker on real lanes (WI-996): `integrate.py attest`
judges the staged tree against the lane's last attested tree, and the refresh
refuses a tree whose tests root holds the mark.

Each case drives `integ.attest` or `integ.refresh` through the station's
fixtures. A case that holds today is a characterization case, unmarked, with its
adequacy witness in its docstring: the wrong check it would catch. The rule's
in-process pin is `tests/test_red_mark.py`.

Registered in `tests/conftest.py`'s `SLOW_MODULES` with its station siblings:
real repositories and lane worktrees.
"""

import os
import re
import stat

import pytest
from conftest import (
    RED_MARK,
    declare_stack_key,
    env_gate_skipif,
    load_script,
    run_py,
    write_lf,
)
from integrate_fixtures import (
    T_LATER,
    _commit,
    _git,
    _rev,
    integ,
    scaffolded_closed_branch,
)
from kitlib import config as kconfig
from kitlib import verdict as kv
from test_integrate_attest import BRANCH, _attest, _declare, _ran, _state
from test_integrate_station import (
    ATTEST_FILES,
    _adjudication_station,
    _lane,
    _order,
    attest_repo,
    station_repo,
)

pytestmark = env_gate_skipif("git")

GADGET, WIDGET = ATTEST_FILES
LOOSE = "tests/test_loose.py"  # untagged, so the row's set never names it
LEGACY = "tests/test_legacy.py"
TAG = "TC-001"  # the fixture row's test case
# A `[product]` section that declares no marker.
PRODUCT = "[product]\ntest = {py} -m pytest -q\n"
MARKER_KEY = "expected_failure_marker"
# An undeclared marker's line opens with where it belongs, then the cause.
MARKER_AT = "docs/stack.ini [product] {} - ".format(MARKER_KEY)

# Each state of a lane's `[product]` section that leaves the marker
# undeclared (`None` is no `docs/stack.ini` at all), with the cause named.
UNDECLARED = [
    (None, "the file is absent"),
    (PRODUCT + PRODUCT, "the file does not parse ("),
    ("", "the section is absent"),
    (PRODUCT, "the key is absent"),
    (PRODUCT + MARKER_KEY + " =    \n", "the value is empty"),
    # The retired section still declaring the mark is named, never read.
    (
        PRODUCT + "[bars]\nred_mark = " + RED_MARK + "\n",
        "the key is absent; the retired [bars] red_mark still declares it and "
        "is no longer read",
    ),
]
UNDECLARED_IDS = ["absent", "unparseable", "no-section", "no-key", "empty", "retired"]


def _source(tag=None, mark=RED_MARK, cases=1):
    """A test file holding `cases` tests under `mark`; `tag` is its module tag."""
    doc = "Implements: " + tag if tag else "A file no tag reads."
    return '"""{}"""\n\nimport pytest\n{}'.format(
        doc,
        "".join(
            "\n\n@{}\ndef test_it_{}():\n    assert False\n".format(mark, n)
            for n in range(cases)
        ),
    )


def _plain(note="unmarked"):
    return '"""Implements: {}"""\n\n\ndef test_it():\n    assert "{}"\n'.format(
        TAG, note
    )


def _stage(wt, rel, text):
    write_lf(wt, rel, text)
    _git(wt, "add", "--", rel)


def _green(root):
    sha, refusal = _attest(root)
    assert refusal is None, refusal
    return sha


def _refused(root):
    sha, refusal = _attest(root)
    assert sha is None and refusal, "attest committed {}".format(sha)
    return refusal


def _marked_round(root, wt):
    """One green round over a lane that adds a mark to `WIDGET`: the review
    record a removal stands on. Returns its commit."""
    _stage(wt, WIDGET, _source(TAG))
    return _green(root)


def _merge_trunk(root, wt):
    _git(wt, "merge", "-q", "--no-edit", _rev(root, "HEAD"))


def _mark_at_base(root, wt, tag=None):
    """Put a marked `LEGACY` in the lane's base: a trunk commit, merged in."""
    write_lf(root, LEGACY, _source(tag))
    _commit(root, "the mark sits on trunk", when=T_LATER)
    _merge_trunk(root, wt)


def _no_product(wt):
    """The lane's declaration without its `[product]` section: the check
    suites and every other section stay as the fixture declared them."""
    text = (wt / "docs" / "stack.ini").read_text(encoding="utf-8")
    return re.sub(r"\[product\]\n(?:[^\[\n].*\n)*", "", text)


def _undeclare(wt, section):
    """Stage the lane's declaration with `section` as its `[product]`, `None`
    removing the file."""
    if section is None:
        _git(wt, "rm", "-q", "docs/stack.ini")
    else:
        _declare(wt, _no_product(wt) + section)


def _drop_object(root, sha):
    """Remove the loose object `sha`, so a read of it fails for real."""
    path = root / ".git" / "objects" / sha[:2] / sha[2:]
    os.chmod(path, stat.S_IWRITE)
    path.unlink()


def _refresh(root):
    return integ.refresh(root, BRANCH, "smoke")


def _refresh_refused(root):
    sha, refusal = _refresh(root)
    assert sha is None and refusal, "the refresh committed {}".format(sha)
    return refusal


def _bar_ran(wt):
    return any(step.startswith("check") for step in _order(wt))


def _refresh_arm(tmp_path, arm):
    """`(root, wt, where)` for a refresh bar: `where` is the checkout a marked
    file goes in. A `no-bar` lane's own delta must stay registry-shaped or the
    scope rung runs the bar, so its mark arrives from trunk."""
    if arm == "landing":
        root = station_repo(tmp_path)
        wt = _lane(root, BRANCH)
        return root, wt, wt
    root, wt = _adjudication_station(tmp_path)
    return root, wt, root


# --- attest: the declaration --------------------------------------------------


@pytest.mark.parametrize("section, cause", UNDECLARED, ids=UNDECLARED_IDS)
def test_attest_refuses_each_undeclared_state_before_the_bar(tmp_path, section, cause):
    """Implements: TC-424"""
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _undeclare(wt, section)
    tip = _rev(root, BRANCH)
    refusal = _refused(root)
    assert MARKER_AT + cause in refusal
    assert _ran(wt) == [] and _rev(root, BRANCH) == tip


def test_attest_reads_the_mark_its_lane_stages_not_the_primarys(tmp_path):
    """Implements: TC-424"""
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _declare(wt, _no_product(wt) + PRODUCT + MARKER_KEY + " = lane_mark(\n")
    _stage(wt, LOOSE, '"""A file no tag reads."""\n\nlane_mark()\n')
    assert LOOSE in _refused(root)


# --- attest: the table --------------------------------------------------------


def test_attest_refuses_an_added_mark_the_set_does_not_name(tmp_path):
    """Implements: TC-424"""
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _stage(wt, LOOSE, _source())
    assert LOOSE in _refused(root)
    assert _ran(wt) == []


def test_attest_passes_an_added_mark_the_set_names(tmp_path):
    """Adequacy witness: a check that refuses every raised count fails here,
    since the set names the file.

    Implements: TC-424
    """
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    sha = _marked_round(root, wt)
    assert kv.bar_attestation(root, sha).tests == kv.tests_digest(ATTEST_FILES)
    assert RED_MARK in _git(root, "show", "{}:{}".format(sha, WIDGET))


def test_attest_refuses_a_removal_with_no_record_in_the_range(tmp_path):
    """Implements: TC-424"""
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _mark_at_base(root, wt, TAG)
    _stage(wt, LEGACY, _plain())
    refusal = _refused(root)
    assert LEGACY in refusal and "no review record" in refusal
    assert _ran(wt) == []


def test_attest_passes_a_removal_over_the_same_set(tmp_path):
    """Adequacy witness: a plain commit sits on the record, so a check reading
    the record from HEAD finds none and refuses; a check comparing digests of
    different spellings refuses too.

    Implements: TC-424
    """
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _marked_round(root, wt)
    write_lf(wt, "note.txt", "a plain commit on the record\n")
    _commit(wt, "a plain commit", when=T_LATER)
    _stage(wt, WIDGET, _plain())
    sha = _green(root)
    assert RED_MARK not in _git(root, "show", "{}:{}".format(sha, WIDGET))


def test_attest_refuses_a_removal_after_the_set_changed(tmp_path):
    """Implements: TC-424"""
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _marked_round(root, wt)
    _stage(wt, WIDGET, _plain())
    _stage(wt, "tests/test_extra.py", _plain("a new tag between the rounds"))
    refusal = _refused(root)
    assert WIDGET in refusal and "another test set" in refusal


def test_attest_refuses_a_removal_the_set_does_not_name(tmp_path):
    """Implements: TC-424"""
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _mark_at_base(root, wt)
    _green(root)
    _stage(wt, LEGACY, '"""A file no tag reads."""\n')
    refusal = _refused(root)
    assert LEGACY in refusal and "does not name" in refusal


def test_a_deleted_marked_file_is_not_judged(tmp_path):
    """Adequacy witness: a check treating absence as a count of 0 on a present
    file refuses here, since the deletion also changes the row's set.

    Implements: TC-424
    """
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _marked_round(root, wt)
    _git(wt, "rm", "-q", WIDGET)
    attested = kv.bar_attestation(root, _green(root))
    assert attested.tests == kv.tests_digest([GADGET])


def test_a_wrapped_mark_is_judged_as_the_one_line_form(tmp_path):
    """Implements: TC-424"""
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    wrapped = RED_MARK.replace("(strict", "(\n    strict").replace(
        ", raises", ",\n    raises"
    )
    assert wrapped != RED_MARK
    _stage(wt, LOOSE, _source(mark=wrapped))
    assert LOOSE in _refused(root)


@pytest.mark.parametrize(
    "read",
    ["range", "reference tree", "staged tree"],
    ids=lambda r: r.replace(" ", "-"),
)
def test_an_unreadable_range_or_tree_refuses(tmp_path, monkeypatch, read):
    """Implements: TC-424"""
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    if read == "range":
        # A real unlistable range needs a broken ref, so the reader answers
        # what it answers when git cannot list one.
        monkeypatch.setattr(kv, "last_review_record", lambda *a: None, raising=False)
        _stage(wt, "staged.txt", "staged work\n")
    elif read == "reference tree":
        _stage(wt, WIDGET, _plain("the first round"))
        _green(root)
        blob = _git(wt, "rev-parse", "HEAD:" + WIDGET).strip()
        _stage(wt, WIDGET, _plain("the second round"))
        _drop_object(root, blob)
    else:
        _stage(wt, "staged.txt", "staged work\n")
        _drop_object(root, _git(wt, "rev-parse", ":staged.txt").strip())
    tip, index = _rev(root, BRANCH), _git(wt, "ls-files", "-s")
    assert "cannot read the " + read in _refused(root)
    assert (_rev(root, BRANCH), _git(wt, "ls-files", "-s")) == (tip, index)


def _undeclared_arm(root, wt):
    _undeclare(wt, PRODUCT)


def _added_arm(root, wt):
    _stage(wt, LOOSE, _source())


def _no_record_arm(root, wt):
    _mark_at_base(root, wt, TAG)
    _stage(wt, LEGACY, _plain())


def _another_set_arm(root, wt):
    _marked_round(root, wt)
    _stage(wt, WIDGET, _plain())
    _stage(wt, "tests/test_extra.py", _plain("a new tag between the rounds"))


def _unnamed_arm(root, wt):
    _mark_at_base(root, wt)
    _green(root)
    _stage(wt, LEGACY, '"""A file no tag reads."""\n')


@pytest.mark.parametrize(
    "arm",
    [_undeclared_arm, _added_arm, _no_record_arm, _another_set_arm, _unnamed_arm],
    ids=["undeclared", "added-unnamed", "no-record", "another-set", "removal-unnamed"],
)
def test_every_mark_refusal_leaves_branch_and_index(tmp_path, arm):
    """Implements: TC-424"""
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    arm(root, wt)
    before, runs = _state(root, wt), len(_ran(wt))
    _refused(root)
    assert _state(root, wt) == before
    assert len(_ran(wt)) == runs, "the bar ran"


# --- the refresh --------------------------------------------------------------


@pytest.mark.parametrize("section, cause", UNDECLARED, ids=UNDECLARED_IDS)
def test_refresh_refuses_each_undeclared_state_before_the_bar(tmp_path, section, cause):
    """Implements: TC-425"""
    root = station_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _undeclare(wt, section)
    _commit(wt, "the lane's declaration", when=T_LATER)
    tip = _rev(root, BRANCH)
    refusal = _refresh_refused(root)
    assert MARKER_AT + cause in refusal
    assert not _bar_ran(wt)
    assert _rev(root, BRANCH) == tip


def test_a_lane_without_the_key_refreshes_on_the_merged_key(tmp_path):
    """Adequacy witness: a check reading the pre-merge tree finds no key and
    refuses a lane the merge has just given one.

    Implements: TC-425
    """
    root = station_repo(tmp_path, stack_ini=PRODUCT)
    declare_stack_key(root, "product", MARKER_KEY, RED_MARK)
    _commit(root, "trunk declares the key", when=T_LATER)
    sha, refusal = _refresh(root)
    assert refusal is None, refusal
    assert RED_MARK in _git(root, "show", sha + ":docs/stack.ini")


@pytest.mark.parametrize("arm", ["landing", "no-bar"])
def test_refresh_refuses_a_marked_tree_naming_each_file_and_count(tmp_path, arm):
    """Implements: TC-425"""
    root, wt, where = _refresh_arm(tmp_path, arm)
    counts = {"tests/test_twice.py": 2, "tests/sub/test_once.py": 1}
    for rel, n in counts.items():
        write_lf(where, rel, _source(cases=n))
    _commit(where, "marked tests", when=T_LATER)
    refusal = _refresh_refused(root)
    for rel, n in counts.items():
        assert re.search(re.escape(rel) + r"\D*" + str(n), refusal), refusal
    assert not _bar_ran(wt)


def test_a_refused_refresh_leaves_the_lane_at_its_work_tip(tmp_path):
    """Implements: TC-425"""
    root = station_repo(tmp_path)
    wt = _lane(root, BRANCH)
    write_lf(wt, LOOSE, _source())
    _commit(wt, "a marked test", when=T_LATER)
    tip = _rev(root, BRANCH)
    _refresh_refused(root)
    assert _rev(root, BRANCH) == tip
    assert _git(wt, "status", "--porcelain") == ""


@pytest.mark.parametrize("arm", ["landing", "no-bar"])
def test_a_tree_with_no_marks_refreshes_as_today(tmp_path, arm):
    """Adequacy witness: a check that refuses an empty count map fails here,
    on a tests root holding no mark, or none at all on the no-bar lane.

    Implements: TC-425
    """
    root, wt, _where = _refresh_arm(tmp_path, arm)
    sha, refusal = _refresh(root)
    assert refusal is None, refusal
    assert kv.bar_attestation(root, sha).bar == arm
    assert _bar_ran(wt) == (arm == "landing")


# --- the routes a lane reaches them by ----------------------------------------


def test_a_plain_commit_removal_then_an_empty_attest_is_judged(tmp_path):
    """Implements: TC-426"""
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _mark_at_base(root, wt, TAG)
    write_lf(wt, LEGACY, _plain())
    _commit(wt, "the removal, by a plain commit", when=T_LATER)
    refusal = _refused(root)
    assert LEGACY in refusal and "no review record" in refusal


def test_a_plain_commit_removal_over_a_matching_record_passes(tmp_path):
    """Adequacy witness: a check that takes the record from HEAD finds none on
    the plain commit and refuses; so does one that refuses every lowered
    count. Its red sibling above catches a reference taken from HEAD.

    Implements: TC-426
    """
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _marked_round(root, wt)
    write_lf(wt, WIDGET, _plain())
    _commit(wt, "the removal, by a plain commit", when=T_LATER)
    tree = _rev(root, BRANCH + "^{tree}")
    assert kv.bar_attestation(root, _green(root)).tree == tree


def test_a_trunk_file_merged_in_is_not_judged(tmp_path):
    """Adequacy witness: a check that refuses each test path differing from
    the reference that the set does not name, instead of judging only a
    changed count, refuses the file trunk brought: it is new to the lane,
    unmarked and untagged.

    Implements: TC-426
    """
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _marked_round(root, wt)
    write_lf(root, "tests/test_trunk.py", '"""A file no tag reads."""\n')
    _commit(root, "trunk moves", when=T_LATER)
    _merge_trunk(root, wt)
    assert _green(root) == _rev(root, BRANCH)


def test_a_partial_close_holding_a_mark_quarantines_then_refreshes(tmp_path):
    """Implements: TC-426"""
    root = station_repo(tmp_path, dest="partial")
    wt = _lane(root, BRANCH)
    write_lf(wt, LOOSE, _source())
    _commit(wt, "a marked test the lane hands back", when=T_LATER)
    assert load_script("dispatch")._refresh_or_quarantine(root, BRANCH, "smoke") is None
    assert (wt / "docs" / "work" / "handback" / (BRANCH + ".patch")).is_file()
    assert not (wt / LOOSE).exists()


def test_a_rebase_makes_the_new_base_the_reference(tmp_path):
    """Implements: TC-426"""
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _mark_at_base(root, wt, TAG)
    _stage(wt, "staged.txt", "staged work\n")
    _green(root)
    write_lf(root, "trunk.txt", "trunk moves\n")
    _commit(root, "trunk moves", when=T_LATER)
    _git(wt, "rebase", "-q", _rev(root, "HEAD"))
    assert kv.bar_attestation(root, BRANCH) is None, "the record outlived the rebase"
    _stage(wt, LEGACY, _plain())
    refusal = _refused(root)
    assert LEGACY in refusal and "no review record" in refusal


def test_a_bootstrapped_scaffold_refreshes_on_its_template_declaration(tmp_path):
    """Implements: TC-426"""
    repo, _claim_sha = scaffolded_closed_branch(tmp_path)
    declared = kconfig.read_stack_ini(repo / "docs" / "stack.ini")
    assert declared.get("product", MARKER_KEY, fallback="") == RED_MARK
    proc = run_py(
        [repo / "scripts" / "integrate.py", "integrate", "--tier", "smoke"], cwd=repo
    )
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "integrate: refreshed wi-401 onto trunk" in out, out
