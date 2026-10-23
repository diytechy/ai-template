"""A spine row is approved only after the rows it hangs from are, on real
repositories.

A commit that leaves an approved row (`Approved` or `Founded`) under a parent
that is not approved is refused where the commit moved either row's status:
at pre-commit through `check.py --parent-first` over the index (against HEAD,
and MERGE_HEAD during a merge), and at the merge slot on each lane commit
through the shared lane-commit walk, so a `--no-verify` commit lands nothing.
A standing case the commit did not move is `trace.py`'s to report, not this
step's. Each registry is read at each tree: a registry absent on the parent
side counts every row as moved, one the parent cannot parse counts every
status as moved, and a commit that touches no registry is not read.

Real git throughout, so this module is in `tests/conftest.py`
`SLOW_MODULES`; its in-process pin is `test_parent_first.py`. Every test here
is new behaviour: each drives the step or the slot, so before the step existed
each failed on its exit-code assertion (the flag was unknown, so the exit was
2) or on the lane merging.
"""

import pytest
from conftest import (
    SCRIPTS,
    env_gate_skipif,
    fixture_commit,
    fixture_git,
    load_script,
    pin_autocrlf,
    run_py,
    trunk_repo,
)
from test_parent_first import PAIRS, TIERS, registries

ar = load_script("acceptance_record")
integrate = load_script("integrate")
tta = load_script("text_then_act")

pytestmark = env_gate_skipif("git")

SR_PATH = TIERS["SR"][0]
BROKEN = "[requirement.SR-001\nstatus = \n"


def _repo(tmp_path):
    """A repository on `main` whose one commit declares its trunk, with an
    identity for the merges the fixtures make."""
    root = trunk_repo(tmp_path / "repo")
    pin_autocrlf(root)
    fixture_git(root, "config", "user.email", "fixture@example.com")
    fixture_git(root, "config", "user.name", "Fixture")
    fixture_git(root, "config", "commit.gpgsign", "false")
    return root


def _write(root, files):
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)


def _commit(root, message, *specs, files=None):
    """Write the registries `specs` name (and any `files`), then commit."""
    _write(root, dict(registries(*specs), **(files or {})))
    fixture_commit(root, message)
    return fixture_git(root, "rev-parse", "HEAD")


def _stage(root, *specs, files=None):
    _write(root, dict(registries(*specs), **(files or {})))
    fixture_git(root, "add", "-A")


def _step(root):
    proc = run_py([SCRIPTS / "check.py", "--parent-first"], root)
    return proc.returncode, proc.stdout + proc.stderr


@pytest.mark.parametrize("pair", sorted(PAIRS), ids=sorted(PAIRS))
def test_staging_an_approved_child_under_a_drafted_parent_is_refused(tmp_path, pair):
    child, parent = PAIRS[pair]
    root = _repo(tmp_path)
    _commit(root, "drafts", (parent, "Drafted"), (child, "Drafted", parent))
    _stage(root, (parent, "Drafted"), (child, "Approved", parent))
    code, out = _step(root)
    assert code == 1, out
    assert child in out and parent in out, out


def test_demoting_a_parent_under_an_approved_child_is_refused(tmp_path):
    root = _repo(tmp_path)
    _commit(root, "approved", ("SR-001", "Approved"), ("LLR-001", "Approved", "SR-001"))
    _stage(root, ("SR-001", "Drafted"))
    code, out = _step(root)
    assert code == 1, out
    assert "LLR-001" in out and "SR-001" in out, out


def test_a_founded_child_flipped_under_a_drafted_parent_is_refused(tmp_path):
    root = _repo(tmp_path)
    _commit(root, "drafts", ("SR-001", "Drafted"), ("LLR-001", "Drafted", "SR-001"))
    _stage(root, ("LLR-001", "Founded", "SR-001"))
    code, out = _step(root)
    assert code == 1, out
    assert "LLR-001" in out and "Founded" in out, out


def test_an_act_approving_parent_and_child_together_passes(tmp_path):
    root = _repo(tmp_path)
    _commit(root, "drafts", ("SR-001", "Drafted"), ("LLR-001", "Drafted", "SR-001"))
    _stage(root, ("SR-001", "Approved"), ("LLR-001", "Approved", "SR-001"))
    code, out = _step(root)
    assert code == 0, out


def test_a_commit_moving_neither_row_passes_over_a_standing_case(tmp_path):
    root = _repo(tmp_path)
    _commit(root, "standing", ("SR-001", "Drafted"), ("LLR-001", "Approved", "SR-001"))
    _stage(root, ("LLR-001", "Approved", "SR-001"), ("LLR-002", "Drafted", "SR-001"))
    code, out = _step(root)
    assert code == 0, out


def test_a_commit_touching_no_registry_is_not_read(tmp_path):
    """HEAD's SR registry does not parse, so a judgement that read the
    registries of a commit touching none of them would refuse it."""
    root = _repo(tmp_path)
    _commit(
        root, "standing", ("LLR-001", "Approved", "SR-001"), files={SR_PATH: BROKEN}
    )
    _stage(root, files={"README.md": "an unrelated change\n"})
    code, out = _step(root)
    assert code == 0, out


def test_a_registry_added_with_a_violation_is_refused(tmp_path):
    root = _repo(tmp_path)
    _stage(root, ("SR-001", "Drafted"), ("LLR-001", "Approved", "SR-001"))
    code, out = _step(root)
    assert code == 1, out
    assert "LLR-001" in out and "SR-001" in out, out


def test_a_commit_repairing_an_unparseable_registry_is_judged_on_its_own_rows(
    tmp_path,
):
    root = _repo(tmp_path)
    _commit(root, "broken", ("LLR-001", "Approved", "SR-001"), files={SR_PATH: BROKEN})
    _stage(root, ("SR-001", "Approved"))
    code, out = _step(root)
    assert code == 0, out
    _stage(root, ("SR-001", "Drafted"))
    code, out = _step(root)
    assert code == 1, out
    assert "LLR-001" in out and "SR-001" in out, out


def test_a_merge_assembling_a_violation_from_two_sides_is_refused(tmp_path):
    """Each side is clean alone: the branch approves the LLR under an approved
    SR, trunk demotes the SR while its child is still Drafted. Only the merge
    leaves the approved child under the Drafted parent. The LLR's status moves
    against HEAD here, so a judgement against HEAD alone refuses this merge
    too: it pins the refusal of an assembled case, not that MERGE_HEAD is read
    as a base, which the next case pins."""
    root = _repo(tmp_path)
    _commit(root, "base", ("SR-001", "Approved"), ("LLR-001", "Drafted", "SR-001"))
    fixture_git(root, "checkout", "-q", "-b", "side")
    _commit(root, "approve the child", ("LLR-001", "Approved", "SR-001"))
    fixture_git(root, "checkout", "-q", "main")
    _commit(root, "demote the parent", ("SR-001", "Drafted"))
    fixture_git(root, "merge", "-q", "--no-commit", "--no-ff", "side")
    code, out = _step(root)
    assert code == 1, out
    assert "LLR-001" in out and "SR-001" in out, out


def test_a_merge_bringing_a_standing_case_to_the_other_side_is_refused(tmp_path):
    """HEAD already holds the approved LLR under its Drafted SR, unchanged by
    the merge; the merged side holds the LLR Drafted. Against HEAD neither
    status moved, so only a judgement that reads MERGE_HEAD as a base sees the
    merge move the LLR's status into the case. Adequacy witness: a staged
    judgement against HEAD alone passes this merge."""
    root = _repo(tmp_path)
    _commit(root, "base", ("SR-001", "Drafted"), ("LLR-001", "Drafted", "SR-001"))
    fixture_git(root, "checkout", "-q", "-b", "side")
    _commit(root, "unrelated", files={"README.md": "side\n"})
    fixture_git(root, "checkout", "-q", "main")
    _commit(root, "the standing case", ("LLR-001", "Approved", "SR-001"))
    fixture_git(root, "merge", "-q", "--no-commit", "--no-ff", "side")
    code, out = _step(root)
    assert code == 1, out
    assert "LLR-001" in out and "SR-001" in out, out


def test_a_no_verify_lane_commit_with_a_violation_is_refused_at_the_slot(tmp_path):
    root = _repo(tmp_path)
    _commit(root, "drafts", ("SR-001", "Drafted"), ("LLR-001", "Drafted", "SR-001"))
    fixture_git(root, "checkout", "-q", "-b", "wi-001")
    bad = _commit(root, "approve the child alone", ("LLR-001", "Approved", "SR-001"))
    fixture_git(root, "checkout", "-q", "main")
    refusal = integrate._text_then_act_refusal(root, "wi-001")
    assert refusal is not None
    assert bad[:10] in refusal and "LLR-001" in refusal and "SR-001" in refusal
    assert "return LLR-001 to Drafted" in refusal
    assert tta.TEXT_THEN_ACT_REMEDY not in refusal


def test_the_first_commit_is_not_judged(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    fixture_git(root, "init", "-q")
    fixture_git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    pin_autocrlf(root)
    _stage(root, ("SR-001", "Drafted"), ("LLR-001", "Approved", "SR-001"))
    code, out = _step(root)
    assert code == 0, out


def test_a_legacy_csv_carrier_is_judged_like_toml(tmp_path):
    root = _repo(tmp_path)
    sr = "docs/requirements/system-requirements.csv"
    llr = "docs/requirements/low-level-requirements.csv"
    sr_text = "SR-ID,Title,SN-Refs,Status\nSR-001,One,,Drafted\n"
    llr_head = "LLR-ID,SR-Refs,Title,Status\n"
    _commit(
        root,
        "drafts",
        files={sr: sr_text, llr: llr_head + "LLR-001,SR-001,a,Drafted\n"},
    )
    _stage(root, files={llr: llr_head + "LLR-001,SR-001,a,Approved\n"})
    code, out = _step(root)
    assert code == 1, out
    assert "LLR-001" in out and "SR-001" in out, out


# --- characterizations of the settled judgement ------------------------------

LINE = (
    "LLR-001 (Approved) is approved under SR-001 (Drafted), which is not: "
    "approve SR-001 in its own approval act, or return LLR-001 to Drafted"
)


def _standing_case_on_main_merged_with_a_side(root):
    """Main approves LLR-001 under its Drafted SR-001; `side`, cut before
    that, touches only the README. Returns the merge commit made on main."""
    _commit(root, "base", ("SR-001", "Drafted"), ("LLR-001", "Drafted", "SR-001"))
    fixture_git(root, "checkout", "-q", "-b", "side")
    _commit(root, "unrelated", files={"README.md": "side\n"})
    fixture_git(root, "checkout", "-q", "main")
    _commit(root, "the standing case", ("LLR-001", "Approved", "SR-001"))
    fixture_git(root, "merge", "-q", "--no-ff", "--no-edit", "side")
    return fixture_git(root, "rev-parse", "HEAD")


def test_a_lane_merge_commit_is_judged_against_every_parent(tmp_path):
    """The merge commit leaves the approved LLR-001 under the Drafted SR-001
    unchanged against its first parent and moved against its second, so it is
    refused. Adequacy witness: a judgement against the first parent alone
    passes it."""
    root = _repo(tmp_path)
    merge = _standing_case_on_main_merged_with_a_side(root)
    assert ar.commit_parent_first_lines(root, merge) == [
        "commit {}: {}".format(merge[:10], LINE)
    ]


def test_each_line_names_its_tree_before_the_relationship(tmp_path):
    """A staged line reads `the index: ` and a lane-commit line `commit
    <sha10>: `, each followed by the whole relationship and its remedy.
    Adequacy witness: a judgement that dropped the tree, or named a commit by
    another abbreviation, fails the equality."""
    root = _repo(tmp_path)
    _commit(root, "drafts", ("SR-001", "Drafted"), ("LLR-001", "Drafted", "SR-001"))
    _stage(root, ("LLR-001", "Approved", "SR-001"))
    assert ar.staged_parent_first_lines(root) == ["the index: " + LINE]
    sha = _commit(root, "approve the child alone")
    assert ar.commit_parent_first_lines(root, sha) == [
        "commit {}: {}".format(sha[:10], LINE)
    ]


@pytest.mark.parametrize(
    "parent_cell", ["", 'status = "Bananas"\n'], ids=["missing", "unknown"]
)
def test_a_parent_with_a_missing_or_unknown_status_refuses_the_commit(
    tmp_path, parent_cell
):
    """A staged commit that approves LLR-001 under an SR-001 with no `Status`
    cell, or with a word outside the vocabulary, is refused: neither claims
    approval. Adequacy witness: a judgement that read only `Drafted` as
    unapproved passes both."""
    root = _repo(tmp_path)
    _commit(root, "drafts", ("SR-001", "Drafted"), ("LLR-001", "Drafted", "SR-001"))
    _stage(
        root,
        ("LLR-001", "Approved", "SR-001"),
        files={SR_PATH: "[requirement.SR-001]\n" + parent_cell},
    )
    lines = ar.staged_parent_first_lines(root)
    assert len(lines) == 1 and "LLR-001 (Approved)" in lines[0], lines
    assert "under SR-001" in lines[0], lines


def test_a_root_commit_is_not_judged(tmp_path):
    """A commit with no parent in its object, carrying an approved child under
    a Drafted parent, is not refused. Adequacy witness: a judgement that read a
    root commit against the empty tree counts both rows as moved and refuses
    it."""
    root = tmp_path / "repo"
    root.mkdir()
    fixture_git(root, "init", "-q")
    fixture_git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    pin_autocrlf(root)
    sha = _commit(
        root, "root", ("SR-001", "Drafted"), ("LLR-001", "Approved", "SR-001")
    )
    assert ar.commit_parent_first_lines(root, sha) == []
