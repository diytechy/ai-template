"""integrate.py `record-checks` — a build round's own record of a pass (WI-956).

`record-checks` commits the lane's staged work (or, with nothing staged, an empty
commit on the tip) carrying a `Checks-Passed:` line that names `checks=commit` and
the digest of the tests it ran, through the one producer the station refresh
also commits through. It derives the row's review test set, runs the commit
checks (the check suite `docs/process.toml` `[required-checks] commit` names,
by the line `docs/stack.ini` `[check-suites]` gives it), then the derived
files through `[product] test` under the lane's own `--basetemp`, and commits
only when both pass.

Every failed write leaves the branch and the index exactly as they were: a
failing checks or a failing named test, a dirty worktree (refused before the checks),
undeclared commit checks (refused before the checks), a message that already carries
the label, a commit a hook refuses, and a commit a hook rewrites. The merge
seam reads the record too: a tip carrying only a `commit` record is not
merge-ready, and the refusal names both checks. The review render reads it as
its gate (WI-957): it renders over what `record-checks` writes, deriving the same set.

Registered in `tests/conftest.py`'s `SLOW_MODULES` with its station
siblings: real repositories and lane worktrees.

Implements: TC-132
"""

import json
import sys
from pathlib import Path

import pytest
from conftest import (
    MARKER_DECLARATION,
    COMMIT_SUITE,
    SCRIPTS,
    env_gate_skipif,
    load_script,
    require_commit_suite,
    run_py,
    seed_row,
    write_lf,
)
from integrate_fixtures import T_LATER, _commit, _git, _rev, integ
from test_integrate_station import (
    CHECKS_STACK_INI,
    STUB_CHECK_GREEN,
    STUB_CHECK_RED,
    STUB_NAMED_TESTS_RED,
    _lane,
    checks_repo,
    station_repo,
)

if str(SCRIPTS) not in sys.path:  # the kit's script-sibling import idiom
    sys.path.insert(0, str(SCRIPTS))

from kitlib import verdict as kv  # noqa: E402

pytestmark = env_gate_skipif("git")

review_brief = load_script("review_brief")

BRANCH = "wi-401"
NAMED = ["tests/test_widget.py", "tests/test_gadget.py"]
# The two files the commit checks are declared in: the suite's line, and the
# suite's name.
STACK, POLICY = "docs/stack.ini", "docs/process.toml"


def _ran(wt):
    """What the harness ran, in order: `check ...` for the commit checks (the
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


def _declare(wt, text, rel=STACK):
    """Stage `text` as the lane's `docs/stack.ini` (or `rel`): the
    declaration the recorded tree carries."""
    (wt / rel).write_text(text, encoding="utf-8", newline="\n")
    _git(wt, "add", rel)


def _record_checks(root, message_file=None):
    return integ.record_checks(root, BRANCH, "commit", message_file=message_file)


# --- the record a passing build round leaves ------------------------------------


def test_record_checks_commits_staged_work_carrying_a_trailer_that_verifies(tmp_path):
    root = checks_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _stage(wt)
    sha, refusal = _record_checks(root)
    assert refusal is None, refusal
    assert sha == _rev(root, BRANCH)
    assert "staged.txt" in _git(root, "ls-tree", "-r", "--name-only", sha).split()
    passed = kv.passed_checks(root, sha)
    assert passed is not None, _git(root, "log", "-1", "--format=%B", sha)
    assert passed.checks == "commit"
    assert passed.tests == kv.tests_digest(NAMED) != "none"


def test_record_checks_with_nothing_staged_writes_an_empty_commit_that_verifies(
    tmp_path,
):
    root = checks_repo(tmp_path)
    tip = _rev(root, BRANCH)
    sha, refusal = _record_checks(root)
    assert refusal is None, refusal
    assert _rev(root, sha + "^1") == tip
    assert _rev(root, sha + "^{tree}") == _rev(root, tip + "^{tree}")
    passed = kv.passed_checks(root, sha)
    assert passed is not None and passed.checks == "commit"


@pytest.mark.parametrize(
    "arm, check_src, named_src, ran",
    [
        ("the commit checks", STUB_CHECK_RED, None, "check"),
        ("a named test", None, STUB_NAMED_TESTS_RED, "named"),
    ],
    ids=["failing-checks", "failing-named-test"],
)
def test_failing_commit_checks_commit_nothing_and_leave_branch_and_index(
    tmp_path, arm, check_src, named_src, ran
):
    kw = {"check_src": check_src} if check_src else {"named_src": named_src}
    root = checks_repo(tmp_path, **kw)
    wt = _lane(root, BRANCH)
    _stage(wt)
    before = _state(root, wt)
    sha, refusal = _record_checks(root)
    assert sha is None and refusal, arm
    assert _ran(wt) and ran in _ran(wt)[-1], "the failure came from {}".format(arm)
    assert _state(root, wt) == before


@pytest.mark.parametrize(
    "dirt, refuses",
    [("tracked", True), ("untracked", True), ("ignored", False)],
    ids=["unstaged-tracked-edit", "untracked-file", "ignored-file"],
)
def test_record_checks_refuses_a_dirty_worktree_before_running_the_checks(
    tmp_path, dirt, refuses
):
    # The checks run on the index as staged, so the worktree must equal it: an
    # unstaged edit or an untracked file would be checked-but-not-committed.
    # An ignored file is not the index's business and does not refuse.
    root = checks_repo(tmp_path)
    wt = _lane(root, BRANCH)
    path = {
        "tracked": "wi-401.txt",
        "untracked": "loose.txt",
        "ignored": "checks-cache/mine.txt",
    }[dirt]
    (wt / path).parent.mkdir(parents=True, exist_ok=True)
    (wt / path).write_text("not staged\n", encoding="utf-8", newline="\n")
    before = _state(root, wt)
    sha, refusal = _record_checks(root)
    if refuses:
        assert sha is None and path in (refusal or ""), refusal
        assert _ran(wt) == [], "the checks ran on a dirty worktree"
        assert _state(root, wt) == before
    else:
        assert refusal is None, refusal
        assert _ran(wt), "the checks never ran"


def test_record_checks_counts_untracked_files_whatever_status_shows(tmp_path):
    # `status.showUntrackedFiles=no` hides an untracked file from a plain
    # `git status`; the checks would still see it, so it still refuses.
    root = checks_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _git(wt, "config", "status.showUntrackedFiles", "no")
    (wt / "loose.txt").write_text("not staged\n", encoding="utf-8", newline="\n")
    before = _state(root, wt)
    sha, refusal = _record_checks(root)
    assert sha is None and "loose.txt" in (refusal or ""), refusal
    assert _ran(wt) == [], "the checks ran on a dirty worktree"
    assert _state(root, wt) == before


def test_record_checks_refuses_the_branch_the_main_checkout_holds(tmp_path):
    # The trunk moves only inside the merge slot, so record-checks resolves its lane
    # through the boundary the refresh uses and refuses the primary's branch.
    root = checks_repo(tmp_path)
    trunk = _git(root, "rev-parse", "--abbrev-ref", "HEAD").strip()
    _stage(root)
    tip = _rev(root, trunk)
    sha, refusal = integ.record_checks(root, trunk, "commit")
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
    root = checks_repo(tmp_path)
    wt = _lane(root, BRANCH)
    message = tmp_path.parent / (tmp_path.name + "-checks-message.txt")
    if content is not None:
        message.write_bytes(content)
    tip = _rev(root, BRANCH)
    sha, refusal = _record_checks(root, message_file=message)
    assert sha is None and str(message) in (refusal or ""), refusal
    assert _ran(wt) == [] and _rev(root, BRANCH) == tip


# A lane's `docs/stack.ini` up to its check suites: `[product]` with the marker
# declared, so the commit checks are all a case leaves undeclared.
PRODUCT = "[product]\ntest = {py} scripts/named_tests.py\n" + MARKER_DECLARATION
# An undeclared value's line opens with where the value belongs: the suite's
# line under the suite's name, or the name itself.
SUITE_AT = "docs/stack.ini [check-suites] {} - ".format(COMMIT_SUITE)
NAME_AT = "docs/process.toml [required-checks] commit - "
RETIRED_REVIEW = "; the retired [bars] review still declares it and is no longer read"


@pytest.mark.parametrize(
    "rel, declared, named",
    [
        # The suite's line: `docs/stack.ini` `[check-suites]`, under the name
        # the lane's policy file gives.
        (STACK, None, [SUITE_AT + "the file is absent"]),
        (STACK, PRODUCT, [SUITE_AT + "the section is absent"]),
        (
            STACK,
            PRODUCT + "[check-suites]\nother = python scripts/check.py\n",
            [SUITE_AT + "the key is absent"],
        ),
        (
            STACK,
            PRODUCT + "[check-suites]\n" + COMMIT_SUITE + " =    \n",
            [SUITE_AT + "the value is empty"],
        ),
        (
            STACK,
            CHECKS_STACK_INI + "[check-suites]\nother = python x.py\n",
            [SUITE_AT + "the file does not parse ("],
        ),
        # The retired home of that line is named, and never run.
        (
            STACK,
            PRODUCT + "[bars]\nreview = python scripts/check.py\n",
            [SUITE_AT + "the section is absent", RETIRED_REVIEW],
        ),
        # The suite's name: `docs/process.toml` `[required-checks] commit`.
        (POLICY, None, [NAME_AT + "the file is absent"]),
        (POLICY, "[required-checks\n", [NAME_AT + "the file does not parse ("]),
        (POLICY, "", [NAME_AT + "the table is absent"]),
        (POLICY, "[required-checks]\n", [NAME_AT + "the key is absent"]),
        (
            POLICY,
            '[required-checks]\ncommit = ""\n',
            [NAME_AT + "the value is not a suite's name"],
        ),
        # A name no line of `[check-suites]` carries.
        (
            POLICY,
            '[required-checks]\ncommit = "nightly"\n',
            ["docs/stack.ini [check-suites] nightly - the key is absent"],
        ),
    ],
    ids=[
        "no-stack-file",
        "no-section",
        "no-suite-line",
        "whitespace-value",
        "unparseable-stack-file",
        "retired-bars-section",
        "no-policy-file",
        "unparseable-policy-file",
        "no-table",
        "no-key",
        "not-a-name",
        "a-name-with-no-line",
    ],
)
def test_record_checks_refuses_a_missing_commit_checks_key_naming_it(
    tmp_path, rel, declared, named
):
    # No default and no fallback to another checks: the declaration staged in the
    # lane the record is for is absent or unusable, so record-checks names the file,
    # the key and the cause and runs nothing, though the primary checkout's
    # own declaration is whole. `declared` is the lane's `rel`, None removing
    # it; of the policy file it is what follows the trunk's line.
    root = checks_repo(tmp_path)
    wt = _lane(root, BRANCH)
    if declared is None:
        _git(wt, "rm", "-q", rel)
    elif rel == POLICY:
        kept = (wt / POLICY).read_text(encoding="utf-8")
        _declare(wt, kept[: kept.index("[required-checks]")] + declared, POLICY)
    else:
        _declare(wt, declared)
    tip = _rev(root, BRANCH)
    sha, refusal = _record_checks(root)
    assert sha is None
    for text in named:
        assert text in (refusal or ""), refusal
    assert _ran(wt) == [] and _rev(root, BRANCH) == tip


def test_record_checks_runs_the_declarations_staged_in_the_lane_not_the_primarys(
    tmp_path,
):
    # The record binds the staged tree, so the checks and the named-tests command
    # it runs are the ones that tree declares: the suite the lane's policy
    # file names, by the line the lane's stack file gives it. The primary
    # checkout declares others; neither of them runs.
    root = checks_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _declare(
        wt,
        "[product]\ntest = {py} scripts/named_tests.py --lane-declared\n"
        + MARKER_DECLARATION
        + "[check-suites]\n"
        + COMMIT_SUITE
        + " = python scripts/check.py --the-primarys-name\n"
        "lane = python scripts/check.py --lane-declared\n",
    )
    require_commit_suite(wt, "lane")
    _git(wt, "add", POLICY)
    sha, refusal = _record_checks(root)
    assert refusal is None, refusal
    assert _ran(wt) == ["check --lane-declared", "named"], _ran(wt)
    assert "--lane-declared" in _named_args(wt), _named_args(wt)
    passed = kv.passed_checks(root, sha)
    assert passed is not None and passed.checks == "commit"


def test_the_named_tests_run_after_the_commit_checks_under_the_lanes_basetemp(tmp_path):
    root = checks_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _sha, refusal = _record_checks(root)
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


def test_a_hook_refused_record_checks_commit_leaves_branch_and_index(tmp_path):
    root = checks_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _hook(root, "commit-msg", "exit 1\n")
    _stage(wt)
    before = _state(root, wt)
    sha, refusal = _record_checks(root)
    assert sha is None and refusal
    assert _ran(wt), "the refusal came before the checks, not at the commit"
    assert _state(root, wt) == before


def test_a_rewritten_record_checks_commit_is_undone_by_the_self_check(tmp_path):
    # A pre-commit hook that stages a file of its own moves the committed tree
    # off the one the checks saw; the line then names a tree that is not there,
    # and the producer undoes the commit and the hook's staging both.
    root = checks_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _hook(
        root,
        "pre-commit",
        "printf 'rewritten\\n' > hook-rewrote.txt\ngit add hook-rewrote.txt\n",
    )
    _stage(wt)
    before = _state(root, wt)
    sha, refusal = _record_checks(root)
    assert sha is None and refusal
    assert _ran(wt), "the refusal came before the checks, not at the self-check"
    assert _state(root, wt) == before


# A declared checks are the adopter's command and may write the tree it checks:
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
pathlib.Path("wi-401.txt").write_text("staged by the checks\\n", encoding="utf-8")
subprocess.run(["git", "add", "wi-401.txt"], check=True)
sys.exit({code})
"""


@pytest.mark.parametrize("route", ["record-checks", "refresh"])
def test_checks_that_edit_a_tracked_file_record_nothing(tmp_path, route):
    # The tree is named before the checks run, so a check run that rewrites a tracked
    # file is caught: what it tested is no longer what would be committed.
    root = checks_repo(tmp_path, check_src=STUB_CHECK_EDITS)
    wt = _lane(root, BRANCH)
    if route == "record-checks":
        _stage(wt)  # the refresh stages its own composed tree
    tip, index = _state(root, wt)
    run = (
        _record_checks
        if route == "record-checks"
        else lambda r: integ.refresh(r, BRANCH, "smoke")
    )
    sha, refusal = run(root)
    assert sha is None and "wi-401.txt" in (refusal or ""), refusal
    assert _ran(wt), "the refusal came before the checks"
    assert _rev(root, BRANCH) == tip
    if route == "record-checks":
        assert _git(wt, "write-tree").strip() == index


@pytest.mark.parametrize("code", [1, 0], ids=["failing", "passing"])
def test_checks_that_stage_an_edit_leave_the_index_as_staged(tmp_path, code):
    # Failing or passing, a check run that moves the index records nothing, and the index
    # goes back to the tree the caller staged.
    root = checks_repo(tmp_path, check_src=STUB_CHECK_STAGES.format(code=code))
    wt = _lane(root, BRANCH)
    _stage(wt)
    before = _state(root, wt)
    sha, refusal = _record_checks(root)
    assert sha is None and refusal
    assert _ran(wt)[:1] == ["check-stages"], _ran(wt)
    assert _state(root, wt) == before
    if code == 0:
        assert "wi-401.txt" in refusal, refusal


def test_the_passed_checks_record_joins_a_message_files_trailer_block(tmp_path):
    # git reads trailers from the last paragraph only, so the line extends the
    # message's own block rather than opening a paragraph after it.
    root = checks_repo(tmp_path)
    message = tmp_path.parent / (tmp_path.name + "-checks-message.txt")
    message.write_text(
        "WI-401: the build round\n\nBody.\n\nWI: WI-401\n"
        "Co-Authored-By: A Builder <builder@example.com>\n",
        encoding="utf-8",
        newline="\n",
    )
    sha, refusal = _record_checks(root, message_file=message)
    assert refusal is None, refusal

    def trailer(key):
        fmt = "--format=%(trailers:key={},valueonly)".format(key)
        return _git(root, "log", "-1", fmt, sha).strip()

    assert trailer("WI") == "WI-401"
    assert trailer("Co-Authored-By") == "A Builder <builder@example.com>"
    passed = kv.passed_checks(root, sha)
    assert passed is not None and passed.checks == "commit"


def test_record_checks_refuses_below_the_harness_floor_before_the_checks(tmp_path):
    # The refresh's floor: a repo that declares the pinned toolchain but has
    # no runnable .venv must not record a passing run on ambient Python.
    root = checks_repo(tmp_path)
    wt = _lane(root, BRANCH)
    (root / "requirements-dev.txt").write_text("pytest\n", encoding="utf-8")
    _stage(wt)
    before = _state(root, wt)
    sha, refusal = _record_checks(root)
    assert sha is None and "harness floor" in (refusal or ""), refusal
    assert _ran(wt) == [], "the checks ran below the floor"
    assert _state(root, wt) == before


def test_a_message_file_carrying_the_label_is_refused_before_the_checks(tmp_path):
    # The producer writes the one label line; a message that brings its own
    # would make two, or a forged one.
    root = checks_repo(tmp_path)
    wt = _lane(root, BRANCH)
    message = tmp_path.parent / (tmp_path.name + "-checks-message.txt")
    message.write_text(
        "WI-401: the build round\n\nChecks-Passed: tree={} work={} checks=commit "
        "tests=none hand-written\n".format("0" * 40, "1" * 40),
        encoding="utf-8",
        newline="\n",
    )
    tip = _rev(root, BRANCH)
    sha, refusal = _record_checks(root, message_file=message)
    assert sha is None and "Checks-Passed" in (refusal or ""), refusal
    assert _ran(wt) == [] and _rev(root, BRANCH) == tip


def test_the_record_checks_cli_is_the_route_a_builder_calls(tmp_path):
    root = checks_repo(tmp_path)
    wt = _lane(root, BRANCH)
    argv = [SCRIPTS / "integrate.py", "record-checks", "--branch", BRANCH, "--checks"]
    proc = run_py(argv + ["commit"], cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    passed = kv.passed_checks(root, BRANCH)
    assert passed is not None and passed.checks == "commit"

    tip = _rev(root, BRANCH)
    (wt / "loose.txt").write_text("not staged\n", encoding="utf-8", newline="\n")
    proc = run_py(argv + ["commit"], cwd=root)
    assert proc.returncode == 1 and "loose.txt" in proc.stderr, proc.stderr
    # `landing` and `none` are the refresh's alone.
    proc = run_py(argv + ["landing"], cwd=root)
    assert proc.returncode != 0 and _rev(root, BRANCH) == tip


REVIEWED_SPEC = """+++
id = "WI-401"
title = "A widget under review"
+++

## Done-when

- It works.
"""


def test_the_review_render_reads_what_record_checks_writes(tmp_path, capsys):
    """Implements: TC-371"""
    # TC-371 (WI-957): the set `record-checks` derived and the set the render derives
    # agree. Adequacy witness: a render that never reads the record names no
    # recorded commit, and one that derives another set refuses here.
    root = checks_repo(tmp_path)
    wt = _lane(root, BRANCH)
    spec = wt / "docs" / "work" / "active" / BRANCH / "WI-401-widget.md"
    spec.parent.mkdir(parents=True, exist_ok=True)
    spec.write_text(REVIEWED_SPEC, encoding="utf-8", newline="\n")
    _git(wt, "add", "-A")
    base = _rev(root, BRANCH)
    sha, refusal = _record_checks(root)
    assert refusal is None, refusal
    capsys.readouterr()  # the route's own console lines are not the render's
    out = tmp_path / "review-out"
    out.mkdir()
    argv = ["review", "--root", str(wt), "--wi", "WI-401", "--base", base]
    argv += ["--sha", sha, "--scope", "full", "--scratch", str(out)]
    argv += ["--out", str(out / "brief.md")]
    assert review_brief.main(argv) == 0, capsys.readouterr().err
    assert [p.name for p in out.iterdir()] == ["brief.md"]
    digest = kv.tests_digest(NAMED)
    shown = capsys.readouterr().out.splitlines()
    assert [line for line in shown if sha in line and digest in line], shown


# --- the set the row derives (WI-995) -----------------------------------------

TEST_A = "tests/test_a.py"
TEST_B = "tests/test_b.py"


def _cli(root, *extra):
    argv = [
        SCRIPTS / "integrate.py",
        "record-checks",
        "--branch",
        BRANCH,
        "--checks",
        "commit",
    ]
    return run_py(argv + list(extra), cwd=root)


def _seeded(tmp_path, code=True, **seed):
    """The closed lane with `seed` staged as its spine, and code staged beside
    it when `code`. Returns `(root, wt)`."""
    root = checks_repo(tmp_path, row=False)
    wt = _lane(root, BRANCH)
    seed_row(wt, **seed)
    if code:
        write_lf(wt, "src/app.py", "work\n")
    _git(wt, "add", "-A")
    return root, wt


def _derived():
    """A row whose two cases are tagged, one with evidence outside the tests
    root: the set is both files, with `docs/hook.txt` listed beside it."""
    return {
        "srs": ["SR-001"],
        "tcs": {
            "TC-001": (["SR-001"], TEST_B + "; docs/hook.txt"),
            "TC-002": (["SR-001"], TEST_A),
        },
        "tags": {TEST_A: ["TC-002"], TEST_B: ["TC-001"]},
        "sr_refs": ["SR-001"],
    }


def test_record_checks_takes_no_tests_argument(tmp_path):
    """Implements: TC-417"""
    root, wt = _seeded(tmp_path, **_derived())
    before = _state(root, wt)
    proc = _cli(root, "--tests", TEST_A)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "--tests" in proc.stderr, proc.stderr
    assert _state(root, wt) == before


def _no_sr():
    return {"sr_refs": []}


def _partial():
    return {
        "srs": ["SR-001"],
        "tcs": {"TC-001": (["SR-001"], TEST_A)},
        "tags": {TEST_A: []},
        "sr_refs": ["SR-001"],
    }


def _empty():
    return {
        "srs": ["SR-001"],
        "tcs": {"TC-001": (["SR-001"], "docs/stack.ini")},
        "sr_refs": ["SR-001"],
    }


@pytest.mark.parametrize(
    "seed, kind",
    [(_no_sr, "names no SR"), (_partial, "partial"), (_empty, "empty")],
    ids=["no-sr", "partial", "empty"],
)
def test_a_derivation_refusal_runs_no_checks_and_leaves_branch_and_index(
    tmp_path, seed, kind
):
    """Implements: TC-417"""
    root, wt = _seeded(tmp_path, **seed())
    before = _state(root, wt)
    proc = _cli(root)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert kind in proc.stderr, proc.stderr
    assert _ran(wt) == [], "a check run ran before the derivation refused"
    assert _state(root, wt) == before


def test_record_checks_runs_the_commit_checks_then_the_derived_files(tmp_path):
    """Implements: TC-417"""
    root, wt = _seeded(tmp_path, **_derived())
    proc = _cli(root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    ran = _ran(wt)
    assert ran and ran[0].startswith("check ") and ran[1:] == ["named"], ran
    args = _named_args(wt)
    assert TEST_A in args and TEST_B in args, args
    passed = kv.passed_checks(root, BRANCH)
    assert passed is not None and passed.checks == "commit"
    assert passed.tests == kv.tests_digest([TEST_A, TEST_B])


def test_record_checks_prints_the_set_and_the_listed_evidence(tmp_path):
    """Implements: TC-417"""
    root, _wt = _seeded(tmp_path, **_derived())
    proc = _cli(root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    for named in (TEST_A, TEST_B, "docs/hook.txt"):
        assert named in proc.stdout, proc.stdout


def test_record_checks_prints_the_gaps_a_row_touching_no_code_reports(tmp_path):
    """Implements: TC-417"""
    root, _wt = _seeded(tmp_path, code=False, srs=["SR-001"], sr_refs=["SR-001"])
    proc = _cli(root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SR-001: no test case verifies it" in proc.stdout, proc.stdout


def test_a_row_touching_no_code_runs_the_check_suite_alone(tmp_path):
    """Implements: TC-417"""
    # TC-417. Characterization: a row touching no code and naming no SR has an
    # empty set, so the commit checks run alone and the record digests `none`, as
    # it does before the derivation exists. Adequacy witness: an implementation
    # that widened an empty set to the whole checks run `[product] test` with no
    # paths here, and `_ran` then ends in `named`.
    root, wt = _seeded(tmp_path, code=False, sr_refs=[])
    proc = _cli(root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    ran = _ran(wt)
    assert len(ran) == 1 and ran[0].startswith("check "), ran
    passed = kv.passed_checks(root, BRANCH)
    assert passed is not None and passed.tests == "none"


# --- the merge seam reads the record ------------------------------------------


@pytest.mark.parametrize(
    "subject",
    ["refresh: wi-401 onto trunk 0123456789", "WI-401: the build round"],
    ids=["refresh-subject", "work-subject"],
)
def test_merge_ready_refuses_a_tip_carrying_only_a_commit_checks_record(
    tmp_path, subject
):
    # A build round's passed-checks record is not the landing checks: the slot
    # refuses it and names the set it found and the one it needs.
    root = station_repo(tmp_path)
    wt = _lane(root, BRANCH)
    _stage(wt, "reviewed.txt")
    tree = _git(wt, "write-tree").strip()
    parent = _rev(root, BRANCH)
    line = kv.format_passed_checks(
        tree, parent, "commit", kv.tests_digest(NAMED), "commit checks PASS"
    )
    _commit(wt, subject + "\n\n" + line, when=T_LATER)
    ready, why = integ._merge_ready(root, BRANCH)
    assert not ready and "checks=commit" in why and "landing" in why, why
    passed = kv.passed_checks(root, BRANCH)
    assert passed is not None and passed.checks == "commit"
