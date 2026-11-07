"""The review test set read from a real lane (WI-995).

A lane's set is derived from its row's SRs through the test-file tags: the row
read from its claim copy or its closed copy, the changed paths since the merge
base with the declared trunk, the declared roots, the three registries and the
tag reader. The answer is the set or exactly one named refusal, and it never
widens to the whole bar. The pure walk is in `tests/test_review_set_walk.py`.

Every case builds a real repository and lane, so this module is filed in
`tests/conftest.py`'s `SLOW_MODULES`.
"""

import pytest
from conftest import (
    claim_on_branch,
    claimed_lane,
    declare_trunk,
    env_gate_skipif,
    fixture_commit,
    fixture_git,
    lane_checkout,
    load_script,
    pin_autocrlf,
    run_py,
    seed_row,
    write_lf,
)

pytestmark = env_gate_skipif("git")

BRANCH = "wi-1"
CLAIM = "docs/work/active/wi-1/WI-1-x.md"
SR_TOML = "docs/requirements/system-requirements.toml"
LLR_TOML = "docs/requirements/low-level-requirements.toml"
TC_TOML = "docs/test/test-cases.toml"
TEST_A = "tests/test_a.py"
TEST_B = "tests/test_b.py"


def _derive(lane, branch=BRANCH):
    return load_script("review_set").derive(lane, branch)


def _tagged():
    """A row whose one case is tagged: the set is `TEST_A`, with no gap."""
    return {
        "srs": ["SR-001"],
        "tcs": {"TC-001": (["SR-001"], TEST_A)},
        "tags": {TEST_A: ["TC-001"]},
        "sr_refs": ["SR-001"],
    }


def _gapped():
    """A row whose one case its evidence names and no file tags: one gap."""
    return {
        "srs": ["SR-001"],
        "tcs": {"TC-001": (["SR-001"], TEST_A)},
        "tags": {TEST_A: []},
        "sr_refs": ["SR-001"],
    }


def _advance_trunk(lane):
    """Move the trunk up to the lane's tip, so its merge base is that tip."""
    fixture_git(lane.with_name("primary"), "merge", "-q", "--ff-only", BRANCH)


def _lane(tmp, files=None, trunk=True, **seed):
    """A claimed lane whose seeded spine is already on the trunk, so it has
    changed nothing yet. `files` join the claim's commit."""
    lane = claimed_lane(tmp, files=files, trunk=trunk)
    seed_row(lane, **seed)
    fixture_commit(lane, "seed the row")
    _advance_trunk(lane)
    return lane


def _stage(lane, rel, text="work\n"):
    write_lf(lane, rel, text)
    fixture_git(lane, "add", "-A")


# --- what touches code --------------------------------------------------------


@pytest.mark.parametrize(
    "rel, roots, touches",
    [
        pytest.param("src/app.py", None, True, id="src"),
        pytest.param("tests/test_new.py", None, True, id="tests"),
        pytest.param("docs/note.md", None, False, id="docs"),
        pytest.param("hooks/pre-commit", None, False, id="another-root"),
        pytest.param("lib/app.py", "lib", True, id="declared-src"),
        pytest.param("src/app.py", "lib", False, id="undeclared-src"),
        pytest.param("docs/note.md", ".", True, id="the-repo-root-as-src"),
    ],
)
def test_a_src_or_tests_change_is_code_touching_and_any_other_path_is_not(
    tmp_path, rel, roots, touches
):
    """Implements: TC-415"""
    declared = "[paths]\nsrc = {}\ntests = tests\n".format(roots)
    lane = _lane(tmp_path, {"docs/stack.ini": declared} if roots else None, **_tagged())
    _stage(lane, rel)
    derived, refusal = _derive(lane)
    assert refusal is None, refusal
    assert derived.code_touching is touches


def test_a_rename_out_of_src_still_touches_code(tmp_path):
    """Implements: TC-415"""
    lane = _lane(tmp_path, {"src/app.py": "work\n"}, **_tagged())
    fixture_git(lane, "mv", "src/app.py", "docs/app.txt")
    derived, refusal = _derive(lane)
    assert refusal is None, refusal
    assert derived.code_touching is True


def test_the_changed_paths_are_counted_from_the_merge_base(tmp_path):
    """Implements: TC-415"""
    # A trunk commit after the lane was cut is not the lane's change; a commit
    # on the lane is, as staged work is.
    lane = _lane(tmp_path, **_tagged())
    primary = lane.with_name("primary")
    write_lf(primary, "src/trunk.py", "trunk\n")
    fixture_commit(primary, "trunk moves on")
    _stage(lane, "docs/note.md")
    derived, refusal = _derive(lane)
    assert refusal is None, refusal
    assert derived.code_touching is False
    _stage(lane, "src/app.py")
    fixture_commit(lane, "code on the lane")
    derived, refusal = _derive(lane)
    assert refusal is None, refusal
    assert derived.code_touching is True


# --- a row naming no SR -------------------------------------------------------


@pytest.mark.parametrize("sr_refs", [None, []], ids=["absent", "empty"])
def test_a_code_touching_row_naming_no_sr_is_refused_by_name(tmp_path, sr_refs):
    """Implements: TC-415"""
    lane = _lane(tmp_path, sr_refs=sr_refs)
    _stage(lane, "src/app.py")
    derived, refusal = _derive(lane)
    assert derived is None
    assert refusal.startswith("names no SR"), refusal


def test_a_row_touching_no_code_and_naming_no_sr_is_an_empty_set(tmp_path):
    """Implements: TC-415"""
    lane = _lane(tmp_path)
    _stage(lane, "docs/note.md")
    derived, refusal = _derive(lane)
    assert refusal is None, refusal
    assert list(derived.files) == [] and list(derived.gaps) == []


# --- partial and empty --------------------------------------------------------


@pytest.mark.parametrize(
    "tagged_file", [False, True], ids=["no-tagged-file", "a-tagged-file"]
)
def test_partial_names_every_gap_and_outranks_empty(tmp_path, tagged_file):
    """Implements: TC-414, TC-415"""
    tcs = {
        "TC-001": (["SR-001"], TEST_A),
        "TC-002": (["SR-001"], None),
        "TC-003": (["SR-001"], "docs/gone.md"),
    }
    tags = {TEST_A: []}
    if tagged_file:
        tcs["TC-004"] = (["SR-001"], TEST_B)
        tags[TEST_B] = ["TC-004"]
    lane = _lane(
        tmp_path,
        srs=["SR-001", "SR-002"],
        llrs={"LLR-001": ["SR-001"]},
        tcs=tcs,
        tags=tags,
        sr_refs=["SR-001", "SR-002"],
    )
    _stage(lane, "src/app.py")
    derived, refusal = _derive(lane)
    assert derived is None
    assert refusal.startswith("partial"), refusal
    for gap in ("SR-002", "LLR-001", "TC-001", TEST_A, "TC-002", "TC-003", "gone.md"):
        assert gap in refusal, (gap, refusal)


def test_empty_is_refused_only_with_no_gap_and_no_tagged_file(tmp_path):
    """Implements: TC-414, TC-415"""
    lane = _lane(
        tmp_path / "empty",
        {"docs/inspect.md": "an inspection record\n"},
        srs=["SR-001"],
        tcs={"TC-001": (["SR-001"], "docs/inspect.md")},
        sr_refs=["SR-001"],
    )
    _stage(lane, "src/app.py")
    derived, refusal = _derive(lane)
    assert derived is None
    assert refusal.startswith("empty"), refusal

    lane = _lane(tmp_path / "set", **_tagged())
    _stage(lane, "src/app.py")
    derived, refusal = _derive(lane)
    assert refusal is None, refusal
    assert list(derived.files) == [TEST_A]


def test_gaps_on_a_row_touching_no_code_are_reported_never_refused(tmp_path):
    """Implements: TC-415"""
    lane = _lane(
        tmp_path,
        srs=["SR-001"],
        tcs={"TC-001": (["SR-001"], TEST_A), "TC-002": (["SR-001"], TEST_B)},
        tags={TEST_A: ["TC-001"], TEST_B: []},
        sr_refs=["SR-001"],
    )
    _stage(lane, "docs/note.md")
    derived, refusal = _derive(lane)
    assert refusal is None, refusal
    assert list(derived.files) == [TEST_A]
    assert [gap for gap in derived.gaps if "TC-002" in str(gap)], derived.gaps


# --- inputs that cannot be read -----------------------------------------------


def _no_claim(lane):
    fixture_git(lane, "rm", "-q", CLAIM)
    fixture_commit(lane, "drop the claim")
    _advance_trunk(lane)


def _two_claims(lane):
    write_lf(lane, "docs/work/active/wi-1/WI-2-y.md", "+++\nid = 'WI-2'\n+++\n")
    fixture_commit(lane, "a second claim")


def _no_copy(lane):
    fixture_git(lane, "rm", "-q", CLAIM)


def _writes(rel, text):
    return lambda lane: write_lf(lane, rel, text)


def _removes(rel):
    return lambda lane: (lane / rel).unlink()


def _row_refs(value):
    return lambda lane: seed_row(lane, ["SR-001"], sr_refs=value)


@pytest.mark.parametrize(
    "arm, named",
    [
        pytest.param(_no_claim, "docs/work/active/wi-1", id="no-claim"),
        pytest.param(_two_claims, "docs/work/active/wi-1", id="two-claims"),
        pytest.param(_no_copy, "WI-1", id="no-copy-in-the-tree"),
        pytest.param(_writes(CLAIM, "+++\nid =\n+++\n"), CLAIM, id="frontmatter"),
        pytest.param(_row_refs("SR-001"), "sr_refs", id="sr-refs-not-a-list"),
        pytest.param(_row_refs([1]), "sr_refs", id="sr-refs-not-strings"),
        pytest.param(_row_refs(["SR-404"]), "SR-404", id="an-sr-the-registry-lacks"),
        pytest.param(_removes(SR_TOML), SR_TOML, id="sr-registry-absent"),
        pytest.param(_removes(LLR_TOML), LLR_TOML, id="llr-registry-absent"),
        pytest.param(_removes(TC_TOML), TC_TOML, id="tc-registry-absent"),
        pytest.param(_writes(SR_TOML, "[requirement\n"), "system-req", id="sr-toml"),
        pytest.param(_writes(LLR_TOML, "[design\n"), "low-level", id="llr-toml"),
        pytest.param(_writes(TC_TOML, "[test\n"), "test-cases", id="tc-toml"),
        pytest.param(_removes("docs/stack.ini"), "stack.ini", id="stack-ini-absent"),
        pytest.param(
            _writes("docs/stack.ini", "[paths\n"), "stack.ini", id="stack-ini-parse"
        ),
        pytest.param(_removes("docs/process.toml"), "trunk", id="trunk-undeclared"),
        pytest.param(
            _writes("docs/process.toml", "[policies\n"), "trunk", id="trunk-parse"
        ),
    ],
)
def test_each_unreadable_input_refuses_by_name(tmp_path, arm, named):
    """Implements: TC-416"""
    # The lane holds a gap and touches code, so each arm outranks partial.
    lane = _lane(tmp_path, **_gapped())
    arm(lane)
    _stage(lane, "src/app.py")
    derived, refusal = _derive(lane)
    assert derived is None
    assert refusal.startswith("malformed"), refusal
    assert named in refusal, refusal


def test_the_tag_readers_refusal_passes_through(tmp_path):
    """Implements: TC-416"""
    seed = _tagged()
    seed["tags"] = {TEST_A: ["TC-001"], TEST_B: ["TC-404"]}
    lane = _lane(tmp_path, **seed)
    _stage(lane, "src/app.py")
    derived, refusal = _derive(lane)
    assert derived is None
    assert "TC-404 is no live row of the test-case registry" in refusal, refusal
    assert TEST_B in refusal, refusal


# --- the closed copy and a scaffold -------------------------------------------


def test_a_lane_closed_in_its_own_tree_reads_its_closed_copy(tmp_path):
    """Implements: TC-416"""
    # The closed copy names another SR than the claim on the trunk does, so a
    # read of the trunk's claim answers the other set.
    lane = _lane(
        tmp_path,
        srs=["SR-001", "SR-002"],
        tcs={"TC-001": (["SR-001"], TEST_A), "TC-002": (["SR-002"], TEST_B)},
        tags={TEST_A: ["TC-001"], TEST_B: ["TC-002"]},
        sr_refs=["SR-001"],
    )
    closed = "docs/archive/work/complete/WI-1-x.md"
    text = (lane / CLAIM).read_text(encoding="utf-8")
    fixture_git(lane, "rm", "-q", CLAIM)
    _stage(lane, closed, text.replace('"SR-001"', '"SR-002"'))
    fixture_commit(lane, "close the row")
    derived, refusal = _derive(lane)
    assert refusal is None, refusal
    assert list(derived.files) == [TEST_B]


SCAFFOLD_DERIVE = """import pathlib, sys
sys.path.insert(0, "scripts")
import review_set
derived, refusal = review_set.derive(pathlib.Path(".").resolve(), sys.argv[1])
print(refusal or " ".join(derived.files))
"""


def test_a_bootstrapped_scaffold_derives_the_set(scaffold):
    """Implements: TC-420"""
    fixture_git(scaffold, "init", "-q", "-b", "main")
    pin_autocrlf(scaffold)
    declare_trunk(scaffold)
    fixture_commit(scaffold, "the scaffold")
    lane = claim_on_branch(lane_checkout(scaffold, BRANCH), "WI-1")
    seed_row(lane, **_tagged())
    _stage(lane, "src/app.py")
    proc = run_py(["-c", SCAFFOLD_DERIVE, BRANCH], cwd=lane)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stdout.split() == [TEST_A], proc.stdout
