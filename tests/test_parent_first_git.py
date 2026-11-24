"""A spine row is accepted only after the rows it hangs from are, on real
repositories.

A commit that leaves an accepted row (`Accepted` or `Founded`) under a parent
that is not accepted is refused where the commit moved either row's status:
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
def test_staging_an_accepted_child_under_a_drafted_parent_is_refused(tmp_path, pair):
    """Implements: TC-397"""
    child, parent = PAIRS[pair]
    root = _repo(tmp_path)
    _commit(root, "drafts", (parent, "Drafted"), (child, "Drafted", parent))
    _stage(root, (parent, "Drafted"), (child, "Accepted", parent))
    code, out = _step(root)
    assert code == 1, out
    assert child in out and parent in out, out


def test_demoting_a_parent_under_an_accepted_child_is_refused(tmp_path):
    """Implements: TC-397"""
    root = _repo(tmp_path)
    _commit(root, "accepted", ("SR-001", "Accepted"), ("LLR-001", "Accepted", "SR-001"))
    _stage(root, ("SR-001", "Drafted"))
    code, out = _step(root)
    assert code == 1, out
    assert "LLR-001" in out and "SR-001" in out, out


def test_a_founded_child_flipped_under_a_drafted_parent_is_refused(tmp_path):
    """Implements: TC-397"""
    root = _repo(tmp_path)
    _commit(root, "drafts", ("SR-001", "Drafted"), ("LLR-001", "Drafted", "SR-001"))
    _stage(root, ("LLR-001", "Founded", "SR-001"))
    code, out = _step(root)
    assert code == 1, out
    assert "LLR-001" in out and "Founded" in out, out


@pytest.mark.parametrize("pair", sorted(PAIRS), ids=sorted(PAIRS))
def test_an_act_accepting_parent_and_child_together_passes(tmp_path, pair):
    """On every edge, a child design row under its parent design row among
    them. Adequacy witness: a judgement that read the parent's status from the
    parent tree instead of the staged one refuses each.

    Implements: TC-397
    """
    child, parent = PAIRS[pair]
    root = _repo(tmp_path)
    _commit(root, "drafts", (parent, "Drafted"), (child, "Drafted", parent))
    _stage(root, (parent, "Accepted"), (child, "Accepted", parent))
    code, out = _step(root)
    assert code == 0, out


def test_a_commit_moving_neither_row_passes_over_a_standing_case(tmp_path):
    """Implements: TC-397"""
    root = _repo(tmp_path)
    _commit(root, "standing", ("SR-001", "Drafted"), ("LLR-001", "Accepted", "SR-001"))
    _stage(root, ("LLR-001", "Accepted", "SR-001"), ("LLR-002", "Drafted", "SR-001"))
    code, out = _step(root)
    assert code == 0, out


#: Re-pointing an accepted design row from an accepted parent to a Drafted
#: one, by the cell each edge reads: (the parent it leaves, the parent it
#: takes), each with its status.
REPOINTS = {
    "SR-Refs": (("SR-001", "Accepted"), ("SR-002", "Drafted")),
    "Parent": (("LLR-001", "Accepted"), ("LLR-003", "Drafted")),
}


@pytest.mark.parametrize("cell", sorted(REPOINTS))
def test_re_pointing_an_accepted_design_row_at_a_drafted_parent_is_refused_as_standing(
    tmp_path, cell
):
    """An accepted LLR-002 moved from an accepted parent to a Drafted one moves
    neither status, so the `parent-first` step passes it; the hook's
    `registry-integrity` step refuses the same commit with the standing
    finding. The parent link inherits this from `SR-Refs` unchanged. Adequacy
    witness: a rule that did not read the parent link passes the `Parent` case
    at both steps.

    Implements: TC-396, TC-397
    """
    left, taken = REPOINTS[cell]
    root = _repo(tmp_path)
    _write(root, registries(left, taken, ("LLR-002", "Accepted", left[0])))
    proc = run_py([SCRIPTS / "trace.py", "--bump-ids"], root)  # allocate, record
    assert proc.returncode == 0, proc.stdout + proc.stderr
    _commit(root, "accepted")
    steps = [SCRIPTS / "check.py", "--run-steps", "parent-first,registry-integrity"]
    clean = run_py(steps, root)  # the control: both steps pass before the move
    assert clean.returncode == 0, clean.stdout + clean.stderr
    _stage(root, left, taken, ("LLR-002", "Accepted", taken[0]))
    proc = run_py(steps, root)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 1, out
    verdicts = {
        ln.split()[1]: ln.split()[0]
        for ln in out.splitlines()
        if ln.startswith(("  PASS", "  FAIL"))
    }
    assert verdicts == {"parent-first": "PASS", "registry-integrity": "FAIL"}, out
    assert (
        "parent-first: LLR-002 (Accepted) is accepted under {} (Drafted)".format(
            taken[0]
        )
        in out
    ), out


def test_a_commit_touching_no_registry_is_not_read(tmp_path):
    """HEAD's SR registry does not parse, so a judgement that read the
    registries of a commit touching none of them would refuse it.

    Implements: TC-397
    """
    root = _repo(tmp_path)
    _commit(
        root, "standing", ("LLR-001", "Accepted", "SR-001"), files={SR_PATH: BROKEN}
    )
    _stage(root, files={"README.md": "an unrelated change\n"})
    code, out = _step(root)
    assert code == 0, out


def test_a_registry_added_with_a_violation_is_refused(tmp_path):
    """Implements: TC-397"""
    root = _repo(tmp_path)
    _stage(root, ("SR-001", "Drafted"), ("LLR-001", "Accepted", "SR-001"))
    code, out = _step(root)
    assert code == 1, out
    assert "LLR-001" in out and "SR-001" in out, out


def test_a_commit_repairing_an_unparseable_registry_is_judged_on_its_own_rows(
    tmp_path,
):
    """Implements: TC-397"""
    root = _repo(tmp_path)
    _commit(root, "broken", ("LLR-001", "Accepted", "SR-001"), files={SR_PATH: BROKEN})
    _stage(root, ("SR-001", "Accepted"))
    code, out = _step(root)
    assert code == 0, out
    _stage(root, ("SR-001", "Drafted"))
    code, out = _step(root)
    assert code == 1, out
    assert "LLR-001" in out and "SR-001" in out, out


def test_a_merge_assembling_a_violation_from_two_sides_is_refused(tmp_path):
    """Each side is clean alone: the branch accepts the LLR under an accepted
    SR, trunk demotes the SR while its child is still Drafted. Only the merge
    leaves the accepted child under the Drafted parent. The LLR's status moves
    against HEAD here, so a judgement against HEAD alone refuses this merge
    too: it pins the refusal of an assembled case, not that MERGE_HEAD is read
    as a base, which the next case pins.

    Implements: TC-397
    """
    root = _repo(tmp_path)
    _commit(root, "base", ("SR-001", "Accepted"), ("LLR-001", "Drafted", "SR-001"))
    fixture_git(root, "checkout", "-q", "-b", "side")
    _commit(root, "accept the child", ("LLR-001", "Accepted", "SR-001"))
    fixture_git(root, "checkout", "-q", "main")
    _commit(root, "demote the parent", ("SR-001", "Drafted"))
    fixture_git(root, "merge", "-q", "--no-commit", "--no-ff", "side")
    code, out = _step(root)
    assert code == 1, out
    assert "LLR-001" in out and "SR-001" in out, out


def test_a_merge_bringing_a_standing_case_to_the_other_side_is_refused(tmp_path):
    """HEAD already holds the accepted LLR under its Drafted SR, unchanged by
    the merge; the merged side holds the LLR Drafted. Against HEAD neither
    status moved, so only a judgement that reads MERGE_HEAD as a base sees the
    merge move the LLR's status into the case. Adequacy witness: a staged
    judgement against HEAD alone passes this merge.

    Implements: TC-397
    """
    root = _repo(tmp_path)
    _commit(root, "base", ("SR-001", "Drafted"), ("LLR-001", "Drafted", "SR-001"))
    fixture_git(root, "checkout", "-q", "-b", "side")
    _commit(root, "unrelated", files={"README.md": "side\n"})
    fixture_git(root, "checkout", "-q", "main")
    _commit(root, "the standing case", ("LLR-001", "Accepted", "SR-001"))
    fixture_git(root, "merge", "-q", "--no-commit", "--no-ff", "side")
    code, out = _step(root)
    assert code == 1, out
    assert "LLR-001" in out and "SR-001" in out, out


@pytest.mark.parametrize("pair", sorted(PAIRS), ids=sorted(PAIRS))
def test_a_no_verify_lane_commit_with_a_violation_is_refused_at_the_slot(
    tmp_path, pair
):
    """On every edge, a child design row under its parent design row among
    them: the lane commit accepting the child alone is refused at the slot.

    Implements: TC-397
    """
    child, parent = PAIRS[pair]
    root = _repo(tmp_path)
    _commit(root, "drafts", (parent, "Drafted"), (child, "Drafted", parent))
    fixture_git(root, "checkout", "-q", "-b", "wi-001")
    bad = _commit(
        root, "accept the child alone", (parent, "Drafted"), (child, "Accepted", parent)
    )
    fixture_git(root, "checkout", "-q", "main")
    refusal = integrate._text_then_act_refusal(root, "wi-001")
    assert refusal is not None, pair
    assert bad[:10] in refusal and child in refusal and parent in refusal
    assert "return {} to Drafted".format(child) in refusal
    assert tta.TEXT_THEN_ACT_REMEDY not in refusal


def test_the_first_commit_is_not_judged(tmp_path):
    """Implements: TC-397"""
    root = tmp_path / "repo"
    root.mkdir()
    fixture_git(root, "init", "-q")
    fixture_git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    pin_autocrlf(root)
    _stage(root, ("SR-001", "Drafted"), ("LLR-001", "Accepted", "SR-001"))
    code, out = _step(root)
    assert code == 0, out


def test_a_legacy_csv_carrier_is_judged_like_toml(tmp_path):
    """Implements: TC-397"""
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
    _stage(root, files={llr: llr_head + "LLR-001,SR-001,a,Accepted\n"})
    code, out = _step(root)
    assert code == 1, out
    assert "LLR-001" in out and "SR-001" in out, out


# --- characterizations of the settled judgement ------------------------------

LINE = (
    "LLR-001 (Accepted) is accepted under SR-001 (Drafted), which is not: "
    "accept SR-001 in its own acceptance act, or return LLR-001 to Drafted"
)


def _standing_case_on_main_merged_with_a_side(root):
    """Main accepts LLR-001 under its Drafted SR-001; `side`, cut before
    that, touches only the README. Returns the merge commit made on main."""
    _commit(root, "base", ("SR-001", "Drafted"), ("LLR-001", "Drafted", "SR-001"))
    fixture_git(root, "checkout", "-q", "-b", "side")
    _commit(root, "unrelated", files={"README.md": "side\n"})
    fixture_git(root, "checkout", "-q", "main")
    _commit(root, "the standing case", ("LLR-001", "Accepted", "SR-001"))
    fixture_git(root, "merge", "-q", "--no-ff", "--no-edit", "side")
    return fixture_git(root, "rev-parse", "HEAD")


def test_a_lane_merge_commit_is_judged_against_every_parent(tmp_path):
    """The merge commit leaves the accepted LLR-001 under the Drafted SR-001
    unchanged against its first parent and moved against its second, so it is
    refused. Adequacy witness: a judgement against the first parent alone
    passes it.

    Implements: TC-397
    """
    root = _repo(tmp_path)
    merge = _standing_case_on_main_merged_with_a_side(root)
    assert ar.commit_parent_first_lines(root, merge) == [
        "commit {}: {}".format(merge[:10], LINE)
    ]


def test_each_line_names_its_tree_before_the_relationship(tmp_path):
    """A staged line reads `the index: ` and a lane-commit line `commit
    <sha10>: `, each followed by the whole relationship and its remedy.
    Adequacy witness: a judgement that dropped the tree, or named a commit by
    another abbreviation, fails the equality.

    Implements: TC-397
    """
    root = _repo(tmp_path)
    _commit(root, "drafts", ("SR-001", "Drafted"), ("LLR-001", "Drafted", "SR-001"))
    _stage(root, ("LLR-001", "Accepted", "SR-001"))
    assert ar.staged_parent_first_lines(root) == ["the index: " + LINE]
    sha = _commit(root, "accept the child alone")
    assert ar.commit_parent_first_lines(root, sha) == [
        "commit {}: {}".format(sha[:10], LINE)
    ]


@pytest.mark.parametrize(
    "parent_cell", ["", 'status = "Bananas"\n'], ids=["missing", "unknown"]
)
def test_a_parent_with_a_missing_or_unknown_status_refuses_the_commit(
    tmp_path, parent_cell
):
    """A staged commit that accepts LLR-001 under an SR-001 with no `Status`
    cell, or with a word outside the vocabulary, is refused: neither claims
    acceptance. Adequacy witness: a judgement that read only `Drafted` as
    unaccepted passes both.

    Implements: TC-397
    """
    root = _repo(tmp_path)
    _commit(root, "drafts", ("SR-001", "Drafted"), ("LLR-001", "Drafted", "SR-001"))
    _stage(
        root,
        ("LLR-001", "Accepted", "SR-001"),
        files={SR_PATH: "[requirement.SR-001]\n" + parent_cell},
    )
    lines = ar.staged_parent_first_lines(root)
    assert len(lines) == 1 and "LLR-001 (Accepted)" in lines[0], lines
    assert "under SR-001" in lines[0], lines


def test_a_root_commit_is_not_judged(tmp_path):
    """A commit with no parent in its object, carrying an accepted child under
    a Drafted parent, is not refused. Adequacy witness: a judgement that read a
    root commit against the empty tree counts both rows as moved and refuses
    it.

    Implements: TC-397
    """
    root = tmp_path / "repo"
    root.mkdir()
    fixture_git(root, "init", "-q")
    fixture_git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    pin_autocrlf(root)
    sha = _commit(
        root, "root", ("SR-001", "Drafted"), ("LLR-001", "Accepted", "SR-001")
    )
    assert ar.commit_parent_first_lines(root, sha) == []
