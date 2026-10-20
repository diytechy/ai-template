"""integrate.py `attest` — a build round's own record of green (WI-956).

`attest` commits the lane's staged work (or, with nothing staged, an empty
commit on the tip) carrying a `Bar-Green:` line that names the `review` bar and
the digest of the tests it ran, through the one producer the station refresh
also commits through. It runs the review bar declared in `docs/stack.ini`
`[bars] review`, then the named tests through `[product] test` under the
lane's own `--basetemp`, and commits only when both are green.

Every failed write leaves the branch and the index exactly as they were: a
red bar or a red named test, a dirty worktree (refused before the bar), an
undeclared review bar (refused before the bar), a message that already carries
the label, a commit a hook refuses, and a commit a hook rewrites. The merge
seam reads the record too: a tip carrying only a `review` attestation is not
merge-ready, and the refusal names both bars.

Registered in `tests/conftest.py`'s `SLOW_MODULES` with its station
siblings: real repositories and lane worktrees.
"""

import json
import sys
from pathlib import Path

import pytest
from conftest import SCRIPTS, env_gate_skipif, run_py
from integrate_fixtures import T_LATER, _commit, _git, _rev, integ
from test_integrate_station import (
    STUB_CHECK_GREEN,
    STUB_CHECK_RED,
    STUB_NAMED_TESTS_RED,
    _lane,
    attest_repo,
    station_repo,
)

if str(SCRIPTS) not in sys.path:  # the kit's script-sibling import idiom
    sys.path.insert(0, str(SCRIPTS))

from kitlib import verdict as kv  # noqa: E402

pytestmark = env_gate_skipif("git")

BRANCH = "wi-401"
NAMED = ["tests/test_widget.py", "tests/test_gadget.py"]


def _ran(wt):
    """What the harness ran, in order: `check ...` for the review bar (the
    station stub records its argv) and `named` for `[product] test`."""
    path = wt.parent / "harness-order.txt"
    return path.read_text(encoding="utf-8").splitlines() if path.is_file() else []


def _named_args(wt):
    return json.loads((wt.parent / "named-args.json").read_text(encoding="utf-8"))


def _state(root, wt):
    """The branch tip and the lane's index, as trees: what a failed write must
    leave exactly as it found."""
    return _rev(root, BRANCH), _git(wt, "write-tree").strip()


def _stage(wt, name="staged.txt"):
    (wt / name).write_text("staged work\n", encoding="utf-8", newline="\n")
    _git(wt, "add", name)


def _hook(root, name, body):
    """Replace one of the fixture's commit hooks (`core.hooksPath` is the
    absolute `.githooks` of the trunk checkout, so the lane runs it too)."""
    hook = root / ".githooks" / name
    hook.write_text("#!/bin/sh\n" + body, encoding="utf-8", newline="\n")
    hook.chmod(0o755)


def _declare(wt, text):
    """Stage `text` as the lane's `docs/stack.ini`: the declaration the
    attested tree carries."""
    (wt / "docs" / "stack.ini").write_text(text, encoding="utf-8", newline="\n")
    _git(wt, "add", "docs/stack.ini")


def _attest(root, named=NAMED, message_file=None):
    return integ.attest(root, BRANCH, "review", named, message_file=message_file)


# --- the record a green build round leaves ------------------------------------


def test_attest_commits_staged_work_carrying_a_trailer_that_verifies(tmp_path):
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _stage(wt)
    sha, refusal = _attest(root)
    assert refusal is None, refusal
    assert sha == _rev(root, BRANCH)
    assert "staged.txt" in _git(root, "ls-tree", "-r", "--name-only", sha).split()
    attested = kv.bar_attestation(root, sha)
    assert attested is not None, _git(root, "log", "-1", "--format=%B", sha)
    assert attested.bar == "review"
    assert attested.tests == kv.tests_digest(NAMED) != "none"


def test_attest_with_nothing_staged_writes_an_empty_commit_that_verifies(tmp_path):
    root = attest_repo(tmp_path)
    tip = _rev(root, BRANCH)
    sha, refusal = _attest(root)
    assert refusal is None, refusal
    assert _rev(root, sha + "^1") == tip
    assert _rev(root, sha + "^{tree}") == _rev(root, tip + "^{tree}")
    attested = kv.bar_attestation(root, sha)
    assert attested is not None and attested.bar == "review"


@pytest.mark.parametrize(
    "arm, check_src, named_src, ran",
    [
        ("the review bar", STUB_CHECK_RED, None, "check"),
        ("a named test", None, STUB_NAMED_TESTS_RED, "named"),
    ],
    ids=["red-bar", "red-named-test"],
)
def test_a_red_review_bar_commits_nothing_and_leaves_branch_and_index(
    tmp_path, arm, check_src, named_src, ran
):
    kw = {"check_src": check_src} if check_src else {"named_src": named_src}
    root = attest_repo(tmp_path, **kw)
    wt = _lane(root, BRANCH)
    _stage(wt)
    before = _state(root, wt)
    sha, refusal = _attest(root)
    assert sha is None and refusal, arm
    assert _ran(wt) and ran in _ran(wt)[-1], "the red came from {}".format(arm)
    assert _state(root, wt) == before


@pytest.mark.parametrize(
    "dirt, refuses",
    [("tracked", True), ("untracked", True), ("ignored", False)],
    ids=["unstaged-tracked-edit", "untracked-file", "ignored-file"],
)
def test_attest_refuses_a_dirty_worktree_before_running_the_bar(
    tmp_path, dirt, refuses
):
    # The bar runs on the index as staged, so the worktree must equal it: an
    # unstaged edit or an untracked file would be barred-but-not-committed.
    # An ignored file is not the index's business and does not refuse.
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    path = {
        "tracked": "wi-401.txt",
        "untracked": "loose.txt",
        "ignored": "bar-cache/mine.txt",
    }[dirt]
    (wt / path).parent.mkdir(parents=True, exist_ok=True)
    (wt / path).write_text("not staged\n", encoding="utf-8", newline="\n")
    before = _state(root, wt)
    sha, refusal = _attest(root)
    if refuses:
        assert sha is None and path in (refusal or ""), refusal
        assert _ran(wt) == [], "the bar ran on a dirty worktree"
        assert _state(root, wt) == before
    else:
        assert refusal is None, refusal
        assert _ran(wt), "the bar never ran"


def test_attest_counts_untracked_files_whatever_status_shows(tmp_path):
    # `status.showUntrackedFiles=no` hides an untracked file from a plain
    # `git status`; the bar would still see it, so it still refuses.
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _git(wt, "config", "status.showUntrackedFiles", "no")
    (wt / "loose.txt").write_text("not staged\n", encoding="utf-8", newline="\n")
    before = _state(root, wt)
    sha, refusal = _attest(root)
    assert sha is None and "loose.txt" in (refusal or ""), refusal
    assert _ran(wt) == [], "the bar ran on a dirty worktree"
    assert _state(root, wt) == before


def test_attest_refuses_the_branch_the_main_checkout_holds(tmp_path):
    # The trunk moves only inside the merge slot, so attest resolves its lane
    # through the boundary the refresh uses and refuses the primary's branch.
    root = attest_repo(tmp_path)
    trunk = _git(root, "rev-parse", "--abbrev-ref", "HEAD").strip()
    _stage(root)
    tip = _rev(root, trunk)
    sha, refusal = integ.attest(root, trunk, "review", NAMED)
    assert sha is None
    assert "MAIN checkout" in (refusal or "") and trunk in refusal, refusal
    assert _rev(root, trunk) == tip
    assert "staged.txt" in _git(root, "diff", "--cached", "--name-only").split()


@pytest.mark.parametrize(
    "content",
    [None, b"WI-401: the build round\n\xff\xfe not UTF-8\n"],
    ids=["missing", "not-utf8"],
)
def test_an_unreadable_message_file_is_a_named_refusal(tmp_path, content):
    # An operator-supplied path: a refusal returned and naming it, never a raise.
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    message = tmp_path.parent / (tmp_path.name + "-attest-message.txt")
    if content is not None:
        message.write_bytes(content)
    tip = _rev(root, BRANCH)
    sha, refusal = _attest(root, message_file=message)
    assert sha is None and str(message) in (refusal or ""), refusal
    assert _ran(wt) == [] and _rev(root, BRANCH) == tip


@pytest.mark.parametrize(
    "declared",
    [
        None,
        "[product]\ntest = {py} scripts/named_tests.py\n",
        "[bars]\nother = python scripts/check.py\n",
        "[bars]\nreview =    \n",
        "[bars]\nreview = python scripts/check.py\n[bars]\nreview = python x.py\n",
    ],
    ids=["no-file", "no-section", "no-key", "whitespace-value", "unparseable"],
)
def test_attest_refuses_a_missing_review_bar_key_naming_it(tmp_path, declared):
    # No default and no fallback to another bar: the declaration staged in the
    # lane the record is for is absent or unusable, so attest names the file
    # and the key and runs nothing, though the primary checkout's own
    # declaration is whole.
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    if declared is None:
        _git(wt, "rm", "-q", "docs/stack.ini")
    else:
        _declare(wt, declared)
    tip = _rev(root, BRANCH)
    sha, refusal = _attest(root)
    assert sha is None
    assert "[bars] review" in (refusal or "") and "docs/stack.ini" in refusal
    assert _ran(wt) == [] and _rev(root, BRANCH) == tip


def test_attest_runs_the_declarations_staged_in_the_lane_not_the_primarys(tmp_path):
    # The record binds the staged tree, so the bar and the named-tests command
    # it runs are the ones that tree declares. The primary checkout declares
    # others; neither of them runs.
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _declare(
        wt,
        "[product]\ntest = {py} scripts/named_tests.py --lane-declared\n"
        "[bars]\nreview = python scripts/check.py --lane-declared\n",
    )
    sha, refusal = _attest(root)
    assert refusal is None, refusal
    assert _ran(wt) == ["check --lane-declared", "named"], _ran(wt)
    assert "--lane-declared" in _named_args(wt), _named_args(wt)
    attested = kv.bar_attestation(root, sha)
    assert attested is not None and attested.bar == "review"


def test_the_named_tests_run_after_the_review_bar_under_the_lanes_basetemp(tmp_path):
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _sha, refusal = _attest(root)
    assert refusal is None, refusal
    ran = _ran(wt)
    assert ran and ran[0].startswith("check ") and ran[1:] == ["named"], ran
    args = _named_args(wt)
    assert all(path in args for path in NAMED), args
    basetemps = [a for a in args if a.startswith("--basetemp=")]
    assert len(basetemps) == 1, args
    basetemp = Path(basetemps[0].split("=", 1)[1]).resolve()
    assert BRANCH in basetemp.name, basetemp
    assert wt.resolve() not in (basetemp, *basetemp.parents), "inside the lane"


# --- every failed write leaves the branch and the index -----------------------


def test_a_hook_refused_attest_commit_leaves_branch_and_index(tmp_path):
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _hook(root, "commit-msg", "exit 1\n")
    _stage(wt)
    before = _state(root, wt)
    sha, refusal = _attest(root)
    assert sha is None and refusal
    assert _ran(wt), "the refusal came before the bar, not at the commit"
    assert _state(root, wt) == before


def test_a_rewritten_attest_commit_is_undone_by_the_self_check(tmp_path):
    # A pre-commit hook that stages a file of its own moves the committed tree
    # off the one the bar saw; the line then names a tree that is not there,
    # and the producer undoes the commit and the hook's staging both.
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _hook(
        root,
        "pre-commit",
        "printf 'rewritten\\n' > hook-rewrote.txt\ngit add hook-rewrote.txt\n",
    )
    _stage(wt)
    before = _state(root, wt)
    sha, refusal = _attest(root)
    assert sha is None and refusal
    assert _ran(wt), "the refusal came before the bar, not at the self-check"
    assert _state(root, wt) == before


# A declared bar is the adopter's command and may write the tree it checks:
# a formatter rewriting a tracked file, or a step that stages its own edit.
# Each stub records its run like the station's, then moves the tree.
STUB_CHECK_EDITS = STUB_CHECK_GREEN + (
    "pathlib.Path('wi-401.txt').write_text('corrected\\n', encoding='utf-8')\n"
)
STUB_CHECK_STAGES = """import pathlib
import subprocess
import sys

pathlib.Path("..", "harness-order.txt").open("a", encoding="utf-8").write(
    "check-stages\\n"
)
pathlib.Path("wi-401.txt").write_text("staged by the bar\\n", encoding="utf-8")
subprocess.run(["git", "add", "wi-401.txt"], check=True)
sys.exit({code})
"""


@pytest.mark.parametrize("route", ["attest", "refresh"])
def test_a_bar_that_edits_a_tracked_file_attests_nothing(tmp_path, route):
    # The tree is named before the bar runs, so a bar that rewrites a tracked
    # file is caught: what it tested is no longer what would be committed.
    root = attest_repo(tmp_path, check_src=STUB_CHECK_EDITS)
    wt = _lane(root, BRANCH)
    if route == "attest":
        _stage(wt)  # the refresh stages its own composed tree
    tip, index = _state(root, wt)
    run = _attest if route == "attest" else lambda r: integ.refresh(r, BRANCH, "smoke")
    sha, refusal = run(root)
    assert sha is None and "wi-401.txt" in (refusal or ""), refusal
    assert _ran(wt), "the refusal came before the bar"
    assert _rev(root, BRANCH) == tip
    if route == "attest":
        assert _git(wt, "write-tree").strip() == index


@pytest.mark.parametrize("code", [1, 0], ids=["red", "green"])
def test_a_bar_that_stages_an_edit_leaves_the_index_as_staged(tmp_path, code):
    # Red or green, a bar that moves the index is not attested, and the index
    # goes back to the tree the caller staged.
    root = attest_repo(tmp_path, check_src=STUB_CHECK_STAGES.format(code=code))
    wt = _lane(root, BRANCH)
    _stage(wt)
    before = _state(root, wt)
    sha, refusal = _attest(root)
    assert sha is None and refusal
    assert _ran(wt)[:1] == ["check-stages"], _ran(wt)
    assert _state(root, wt) == before
    if code == 0:
        assert "wi-401.txt" in refusal, refusal


def test_the_attestation_joins_a_message_files_trailer_block(tmp_path):
    # git reads trailers from the last paragraph only, so the line extends the
    # message's own block rather than opening a paragraph after it.
    root = attest_repo(tmp_path)
    message = tmp_path.parent / (tmp_path.name + "-attest-message.txt")
    message.write_text(
        "WI-401: the build round\n\nBody.\n\nWI: WI-401\n"
        "Co-Authored-By: A Builder <builder@example.com>\n",
        encoding="utf-8",
        newline="\n",
    )
    sha, refusal = _attest(root, message_file=message)
    assert refusal is None, refusal

    def trailer(key):
        fmt = "--format=%(trailers:key={},valueonly)".format(key)
        return _git(root, "log", "-1", fmt, sha).strip()

    assert trailer("WI") == "WI-401"
    assert trailer("Co-Authored-By") == "A Builder <builder@example.com>"
    attested = kv.bar_attestation(root, sha)
    assert attested is not None and attested.bar == "review"


def test_attest_refuses_below_the_harness_floor_before_the_bar(tmp_path):
    # The refresh's floor: a repo that declares the pinned toolchain but has
    # no runnable .venv must not record a green run on ambient Python.
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    (root / "requirements-dev.txt").write_text("pytest\n", encoding="utf-8")
    _stage(wt)
    before = _state(root, wt)
    sha, refusal = _attest(root)
    assert sha is None and "harness floor" in (refusal or ""), refusal
    assert _ran(wt) == [], "the bar ran below the floor"
    assert _state(root, wt) == before


def test_a_message_file_carrying_the_label_is_refused_before_the_bar(tmp_path):
    # The producer writes the one label line; a message that brings its own
    # would make two, or a forged one.
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    message = tmp_path.parent / (tmp_path.name + "-attest-message.txt")
    message.write_text(
        "WI-401: the build round\n\nBar-Green: tree={} work={} bar=review "
        "tests=none hand-written\n".format("0" * 40, "1" * 40),
        encoding="utf-8",
        newline="\n",
    )
    tip = _rev(root, BRANCH)
    sha, refusal = _attest(root, message_file=message)
    assert sha is None and "Bar-Green" in (refusal or ""), refusal
    assert _ran(wt) == [] and _rev(root, BRANCH) == tip


def test_the_attest_cli_is_the_route_a_builder_calls(tmp_path):
    root = attest_repo(tmp_path)
    wt = _lane(root, BRANCH)
    argv = [SCRIPTS / "integrate.py", "attest", "--branch", BRANCH, "--bar"]
    proc = run_py(argv + ["review", "--tests"] + NAMED, cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    attested = kv.bar_attestation(root, BRANCH)
    assert attested is not None and attested.bar == "review"

    tip = _rev(root, BRANCH)
    (wt / "loose.txt").write_text("not staged\n", encoding="utf-8", newline="\n")
    proc = run_py(argv + ["review", "--tests"] + NAMED, cwd=root)
    assert proc.returncode == 1 and "loose.txt" in proc.stderr, proc.stderr
    # `landing` and `no-bar` are the refresh's alone.
    proc = run_py(argv + ["landing"], cwd=root)
    assert proc.returncode != 0 and _rev(root, BRANCH) == tip


# --- the merge seam reads the record ------------------------------------------


@pytest.mark.parametrize(
    "subject",
    ["refresh: wi-401 onto trunk 0123456789", "WI-401: the build round"],
    ids=["refresh-subject", "work-subject"],
)
def test_merge_ready_refuses_a_tip_carrying_only_a_review_attestation(
    tmp_path, subject
):
    # A build round's record of green is not the landing bar: the slot refuses
    # it and names the bar it found and the one it needs.
    root = station_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _stage(wt, "reviewed.txt")
    tree = _git(wt, "write-tree").strip()
    parent = _rev(root, BRANCH)
    line = kv.format_bar_green(
        tree, parent, "review", kv.tests_digest(NAMED), "review bar PASS"
    )
    _commit(wt, subject + "\n\n" + line, when=T_LATER)
    ready, why = integ._merge_ready(root, BRANCH)
    assert not ready and "review" in why and "landing" in why, why
    attested = kv.bar_attestation(root, BRANCH)
    assert attested is not None and attested.bar == "review"
