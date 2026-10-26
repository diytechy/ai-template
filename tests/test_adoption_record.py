"""WI-969: only the close writes a disposition's adoption record.

The close validates an adoption once, in the lane HEAD's tree, and writes the
validated ids into the closed spec's `adopted` cell; the sweep trusts that
record. So the record is authority, and the commit check
(`adoption_record.commit_adoption_record_lines`) admits a record change in
three cases only: the machinery's own close (one parent, paired moves from one
`active/<branch>/` into `complete/`, the composed subject, every path outside
`docs/work/` exactly the inbound relink those moves write, its record equal
to its request and valid in its parent's tree), a record carried unchanged,
and a merge by what neither parent carried. It rides the lane-commit walk at
the merge slot and runs as the pre-commit hook's `adoption-record` step,
squash landings included.

Real git throughout, so this module is in `tests/conftest.py` `SLOW_MODULES`;
its in-process pins are test_disposition_adoption.py's record-change table and
close-shape oracle. Every test here is new behaviour (coordinator-cycle skill
§3, Intent): each refusal test was red while no rule existed and the commit
was accepted; the pass tests were red while trunk's close refused the
adoption it closes.
"""

import posixpath
import sys

import pytest
from conftest import SCRIPTS, env_gate_skipif, load_script, pin_autocrlf, run_py
from test_handback import (
    ACTIVE_SPEC,
    COMPLETE_SPEC,
    _git,
    adopting_repo,
    hb,
    integ,
    lane,
    link_the_active_spec_from_a_review,
    merge_branch,
    successor_seed,
)

if str(SCRIPTS) not in sys.path:  # the kit's script-sibling import idiom
    sys.path.insert(0, str(SCRIPTS))

from kitlib import verdict as kverdict  # noqa: E402

ar = load_script("adoption_record")
spec_move = load_script("spec_move")
check = load_script("check")
tta = integ.text_then_act

pytestmark = env_gate_skipif("git")

BRANCH = "wi-401"
_REMAP = {ACTIVE_SPEC: COMPLETE_SPEC}


# --- fixtures -------------------------------------------------------------------


def _real_close(root):
    """The machinery's own close of WI-401; the lane tip it committed."""
    ids, refusal = hb.close_adjudication(root, BRANCH)
    assert refusal is None, refusal
    assert ids == ["WI-401"]
    return _git(root, "rev-parse", BRANCH).strip()


def _slot(root, branch=BRANCH):
    """The merge slot's one lane-commit walk with every per-commit rider:
    None when every lane commit passes, else `(sha, lines)`."""
    return integ._each_lane_commit(
        root, branch, "the lane commits", tta.LANE_COMMIT_RIDERS
    )


def _assert_slot_refuses(root, branch=BRANCH):
    found = _slot(root, branch)
    assert found is not None and not isinstance(found, str), found
    _sha, lines = found
    assert "WI-401" in " ".join(lines), lines


def _hook(root):
    """The `adoption-record` step's exit code over `root`'s index."""
    return ar.main(["--root", str(root)])


def _check_step(root):
    return run_py([SCRIPTS / "check.py", "--run-steps", "adoption-record"], root)


def _with_record(text, record):
    """`text` with an `adopted` record as the front matter's last line."""
    head, sep, body = text.partition("\n+++\n")
    cell = "adopted = [{}]".format(", ".join('"{}"'.format(w) for w in record))
    return head + "\n" + cell + sep + body


def _close_subject():
    return hb.station.mechanical_close_subject(["WI-401"])


def _hand_close(
    root, record=("WI-450",), subject=None, review=None, extra="", commit=True
):
    """Close WI-401 by hand in its lane: the close's own paired move and text,
    an `adopted` record (`record`, or none), the exact inbound relink of the
    `review` file (plus `extra` bytes), staged and, with `commit`, committed
    under `subject` (default: the machinery's composed subject) with the hook
    skipped. Returns the lane worktree."""
    wt = lane(root)
    closed = hb._adjudication_close_text(
        (wt / ACTIVE_SPEC).read_text(encoding="utf-8"),
        hb._ADJUDICATION_CLOSE_DELIVERABLE,
    )
    if record:
        closed = _with_record(closed, record)
    (wt / COMPLETE_SPEC).parent.mkdir(parents=True, exist_ok=True)
    (wt / COMPLETE_SPEC).write_text(closed, encoding="utf-8", newline="\n")
    (wt / ACTIVE_SPEC).unlink()
    if review:
        old = (wt / review).read_text(encoding="utf-8")
        new = spec_move.expected_relink(old, posixpath.dirname(review), _REMAP)
        assert new != old
        (wt / review).write_text(new + extra, encoding="utf-8", newline="\n")
    _git(wt, "add", "-A")
    if commit:
        _git(wt, "commit", "--no-verify", "-q", "-m", subject or _close_subject())
    return wt


def _lane_commit(root, edit, message):
    """Apply `edit(worktree)` in WI-401's lane and commit it, hook skipped."""
    wt = lane(root)
    edit(wt)
    _git(wt, "add", "-A")
    _git(wt, "commit", "--no-verify", "-q", "-m", message)
    return _git(wt, "rev-parse", "HEAD").strip()


def _edit_record(path, record):
    """Rewrite the `adopted` line of the spec at `path` (None: drop it)."""
    text = path.read_text(encoding="utf-8")
    kept = [ln for ln in text.split("\n") if not ln.startswith("adopted = ")]
    text = "\n".join(kept)
    path.write_text(
        _with_record(text, record) if record else text, encoding="utf-8", newline="\n"
    )


def _squash(root, branch=BRANCH):
    """Stage a `git merge --squash` of `branch` on trunk, as a landing does."""
    _git(root, "merge", "-q", "--squash", branch)


# --- D5: the close's own commit, and a record carried unchanged -----------------


def test_the_closes_own_commit_passes(tmp_path):
    root = adopting_repo(tmp_path)
    close = _real_close(root)
    assert ar.commit_adoption_record_lines(root, close) == []
    assert _slot(root) is None


def test_a_later_commit_carrying_the_record_unchanged_passes(tmp_path):
    root = adopting_repo(tmp_path)
    _real_close(root)

    def body_edit(wt):
        path = wt / COMPLETE_SPEC
        path.write_text(
            path.read_text(encoding="utf-8") + "\nA later note.\n",
            encoding="utf-8",
            newline="\n",
        )

    edited = _lane_commit(root, body_edit, "note the closed row\n\nWI: WI-401")
    assert ar.commit_adoption_record_lines(root, edited) == []

    def archive(wt):
        dest = wt / "docs" / "archive" / "work" / "complete" / "WI-401-dispose.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((wt / COMPLETE_SPEC).read_bytes())
        (wt / COMPLETE_SPEC).unlink()

    archived = _lane_commit(root, archive, "archive the closed row")
    assert ar.commit_adoption_record_lines(root, archived) == []
    assert _slot(root) is None


# --- the real close whose relink reaches outside docs/work ----------------------


def test_a_real_close_relinking_a_file_outside_docs_work_passes_the_rider_and_the_squash_hook(
    tmp_path,
):
    root = adopting_repo(tmp_path)
    review = link_the_active_spec_from_a_review(root)
    close = _real_close(root)
    # The case is real: the close rewrote the review's link to the spec.
    assert review in _git(root, "diff", "--name-only", close + "^", close).split()
    # The peel is unchanged: a close whose relink leaves docs/work is not peeled.
    assert kverdict.mechanical_close_attestation(root, close) is None
    assert _slot(root) is None
    _squash(root)
    assert _hook(root) == 0
    proc = _check_step(root)
    assert proc.returncode == 0, proc.stdout + proc.stderr


@pytest.mark.parametrize(
    "case", ["hand-subject", "relink-plus-one-byte", "record-unequal"]
)
def test_a_hand_written_record_beside_the_same_relink_is_refused(tmp_path, case):
    root = adopting_repo(tmp_path)
    review = link_the_active_spec_from_a_review(root)
    shape = {
        "hand-subject": {"subject": "close WI-401 by hand"},
        "relink-plus-one-byte": {"extra": " "},
        "record-unequal": {"record": ("WI-451",)},
    }[case]
    wt = _hand_close(root, review=review, commit=False, **shape)
    assert _hook(wt) == 1
    _git(
        wt,
        "commit",
        "--no-verify",
        "-q",
        "-m",
        shape.get("subject") or _close_subject(),
    )
    _assert_slot_refuses(root)


# --- D6: a record written anywhere but the close --------------------------------


def _record_in_the_active_spec(wt):
    _edit_record(wt / ACTIVE_SPEC, ("WI-450",))


def test_a_record_written_in_a_lane_commit_is_refused_at_the_slot(tmp_path):
    root = adopting_repo(tmp_path)
    sha = _lane_commit(root, _record_in_the_active_spec, "record the adoption")
    assert ar.commit_adoption_record_lines(root, sha) != []
    _assert_slot_refuses(root)


def test_a_hand_close_writing_a_record_is_refused(tmp_path):
    root = adopting_repo(tmp_path)
    wt = _hand_close(root, subject="close WI-401 by hand")
    sha = _git(wt, "rev-parse", "HEAD").strip()
    assert ar.commit_adoption_record_lines(root, sha) != []
    _assert_slot_refuses(root)


def test_a_record_staged_on_trunk_is_refused_by_the_hook_step(tmp_path):
    root = adopting_repo(tmp_path)
    _edit_record(root / ACTIVE_SPEC, ("WI-450",))
    _git(root, "add", "-A")
    assert _hook(root) == 1
    proc = _check_step(root)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "adoption-record" in proc.stdout


# --- D7: a close-shaped commit whose record is not the validated request --------


def test_a_close_shaped_commit_whose_record_differs_from_the_request_is_refused(
    tmp_path,
):
    root = adopting_repo(tmp_path)
    wt = _hand_close(root, record=("WI-451",))
    sha = _git(wt, "rev-parse", "HEAD").strip()
    assert ar.commit_adoption_record_lines(root, sha) != []
    _assert_slot_refuses(root)


def test_a_close_shaped_commit_whose_adoption_fails_in_the_parent_tree_is_refused(
    tmp_path,
):
    # The adopted row is already closed in the parent, so the close itself
    # would refuse; the commit is built by hand so the close shape holds.
    root = adopting_repo(tmp_path, seed=[successor_seed(state="complete")])
    wt = _hand_close(root)
    sha = _git(wt, "rev-parse", "HEAD").strip()
    assert ar.commit_adoption_record_lines(root, sha) != []
    _assert_slot_refuses(root)


# --- D8: a record changed or removed after the close ----------------------------


def _record_changed_later(tmp_path, change):
    root = adopting_repo(tmp_path)
    _real_close(root)
    sha = _lane_commit(
        root, lambda wt: _edit_record(wt / COMPLETE_SPEC, change), "edit the record"
    )
    assert ar.commit_adoption_record_lines(root, sha) != []
    _assert_slot_refuses(root)


def test_a_record_changed_later_is_refused(tmp_path):
    _record_changed_later(tmp_path, ("WI-451",))


def test_a_record_removed_later_is_refused(tmp_path):
    _record_changed_later(tmp_path, None)


@pytest.mark.parametrize("where", ["slot", "hook"])
def test_a_request_rewritten_under_a_carried_record_is_refused(tmp_path, where):
    # The record is carried unchanged, but the request it was recorded with
    # is rewritten: the record is admitted only with its request unchanged.
    root = adopting_repo(tmp_path)
    _real_close(root)

    def rewrite(wt):
        path = wt / COMPLETE_SPEC
        text = path.read_text(encoding="utf-8")
        assert 'adopts = "WI-450"' in text
        path.write_text(
            text.replace('adopts = "WI-450"', 'adopts = "WI-777"'),
            encoding="utf-8",
            newline="\n",
        )

    if where == "hook":
        wt = lane(root)
        rewrite(wt)
        _git(wt, "add", "-A")
        assert _hook(wt) == 1
        return
    sha = _lane_commit(root, rewrite, "rewrite the request\n\nWI: WI-401")
    lines = ar.commit_adoption_record_lines(root, sha)
    assert lines and "request" in " ".join(lines), lines
    _assert_slot_refuses(root)


# --- D9: a requesting spec moved into complete/ without a record ----------------


@pytest.mark.parametrize("where", ["slot", "hook"])
def test_a_requesting_spec_moved_into_complete_without_a_record_is_refused(
    tmp_path, where
):
    root = adopting_repo(tmp_path)
    if where == "hook":
        wt = _hand_close(root, record=None, commit=False)
        assert _hook(wt) == 1
        return
    wt = _hand_close(root, record=None)
    sha = _git(wt, "rev-parse", "HEAD").strip()
    assert ar.commit_adoption_record_lines(root, sha) != []
    _assert_slot_refuses(root)


# --- merges, parents and squashes -----------------------------------------------


def test_a_refresh_merge_carrying_trunks_record_passes(tmp_path):
    root = adopting_repo(tmp_path)
    _git(root, "branch", "wi-402", "main")
    other = tmp_path / "wt-402"
    _git(root, "worktree", "add", "-q", str(other), "wi-402")
    (other / "other.txt").write_text("other\n", encoding="utf-8", newline="\n")
    _git(other, "add", "-A")
    _git(other, "commit", "--no-verify", "-q", "-m", "other lane work")
    _real_close(root)
    merge_branch(root)  # trunk now carries the closed spec and its record
    _git(other, "merge", "--no-ff", "-q", "-m", "refresh from trunk", "main")
    refresh = _git(other, "rev-parse", "HEAD").strip()
    assert ar.commit_adoption_record_lines(root, refresh) == []
    assert _slot(root, "wi-402") is None


def test_a_parent_behind_a_shallow_boundary_is_refused_by_name(tmp_path):
    root = adopting_repo(tmp_path)
    sha = _lane_commit(root, _record_in_the_active_spec, "record the adoption")
    parent = _git(root, "rev-parse", sha + "^").strip()
    clone = tmp_path / "shallow"
    _git(
        tmp_path,
        "clone",
        "-q",
        "--depth",
        "1",
        "--branch",
        BRANCH,
        root.as_uri(),
        str(clone),
    )
    pin_autocrlf(clone)
    assert _git(clone, "rev-parse", "HEAD").strip() == sha
    lines = ar.commit_adoption_record_lines(clone, sha)
    assert len(lines) == 1, lines
    assert parent[:10] in lines[0] and "cannot be read" in lines[0], lines


def test_a_rebased_lanes_squash_landing_is_admitted(tmp_path):
    root = adopting_repo(tmp_path)
    _real_close(root)
    (root / "trunk-moved.txt").write_text("moved\n", encoding="utf-8", newline="\n")
    _git(root, "add", "-A")
    _git(root, "commit", "--no-verify", "-q", "-m", "trunk moves on")
    _git(lane(root), "rebase", "-q", "main")
    _squash(root)
    assert _hook(root) == 0


def test_a_squash_whose_index_edits_the_tips_record_is_refused(tmp_path):
    root = adopting_repo(tmp_path)
    _real_close(root)
    _squash(root)
    _edit_record(root / COMPLETE_SPEC, ("WI-451",))
    _git(root, "add", "-A")
    assert _hook(root) == 1


# --- wiring ---------------------------------------------------------------------


def test_the_pre_commit_hook_runs_the_adoption_record_step():
    hook = (SCRIPTS.parent / "hooks" / "pre-commit").read_text(encoding="utf-8")
    line = next(
        ln for ln in hook.splitlines() if ln.startswith('"$PY"') and "--run-steps" in ln
    )
    steps = line.split("--run-steps", 1)[1].split()[0].split(",")
    assert "adoption-record" in steps
    assert "adoption-record" in check.BUILTIN_STEP_NAMES


def test_the_record_rule_rides_the_lane_commit_walk():
    riders = [getattr(rule, "__name__", "") for rule in tta.LANE_COMMIT_RIDERS]
    assert "commit_adoption_record_lines" in riders


def test_a_record_refusal_at_the_slot_does_not_carry_the_text_then_act_remedy(
    tmp_path,
):
    root = adopting_repo(tmp_path)
    _lane_commit(root, _record_in_the_active_spec, "record the adoption")
    refusal = integ._text_then_act_refusal(root, BRANCH)
    assert refusal is not None and "close_adjudication" in refusal, refusal
    assert tta.TEXT_THEN_ACT_REMEDY not in refusal


def _spy_shared_walk(monkeypatch):
    """Wrap `kitlib.git.lane_commit_walk` with a spy recording each call's
    commits and riders, then walking them as the owner does."""
    from kitlib import git as kgit

    real = getattr(kgit, "lane_commit_walk", None)
    seen = []

    def spy(root, commits, riders):
        commits = list(commits)
        seen.append((commits, tuple(riders)))
        return real(root, commits, riders)

    monkeypatch.setattr(kgit, "lane_commit_walk", spy, raising=False)
    return seen


def test_a_squash_landing_is_judged_through_the_shared_walk(tmp_path, monkeypatch):
    """A rebased lane's squash landing is judged by `kitlib.git`'s walk over
    HEAD..tip with the record rule as its one rider, and is still admitted."""
    root = adopting_repo(tmp_path)
    _real_close(root)
    (root / "trunk-moved.txt").write_text("moved\n", encoding="utf-8", newline="\n")
    _git(root, "add", "-A")
    _git(root, "commit", "--no-verify", "-q", "-m", "trunk moves on")
    _git(lane(root), "rebase", "-q", "main")
    _squash(root)
    head = _git(root, "rev-parse", "HEAD").strip()
    tip = _git(root, "rev-parse", BRANCH).strip()
    commits = _git(root, "rev-list", "--reverse", head + ".." + tip).split()
    seen = _spy_shared_walk(monkeypatch)
    assert _hook(root) == 0
    assert seen == [(commits, (ar.commit_adoption_record_lines,))]


def test_each_spec_view_keeps_its_shape_over_one_tree(tmp_path):
    """The ruling sync's and the adoption record's views of one committed
    tree, read at HEAD and at the index: the ruling sync's `{id: path}` drops
    the `-000` example and keeps the last of WI-005's two paths; the adoption
    record's `{id: [path]}` keeps every path, so `_spec_at` refuses the two
    specs carrying WI-005; the registry loader's work-root relpaths leave the
    archive out. Files that are not `WI-*.md` reach no view.

    Adequacy witness: it fails for an implementation that serves one view to
    both callers. Serving the ruling sync's view collapses WI-005's duplicates
    for the adoption record, so the "2 specs carry one id" refusal never
    fires; serving the adoption record's view sends the `-000` example and
    the duplicate list to the ruling sync.
    """
    acceptance = load_script("acceptance_record")
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q")
    pin_autocrlf(root)
    archived = "docs/archive/work/complete/WI-005-five.md"
    active = "docs/work/active/wi-007/WI-007-seven.md"
    example = "docs/work/queued/WI-000-example.md"
    queued = "docs/work/queued/WI-005-five.md"
    others = ["docs/work/README.md", "docs/work/queued/WI-011-eleven.txt"]
    for rel in [archived, active, example, queued, *others]:
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text("spec\n", encoding="utf-8", newline="\n")
    _git(root, "add", "-A")
    _git(
        root,
        "-c",
        "user.name=t",
        "-c",
        "user.email=t@example.invalid",
        "commit",
        "--no-verify",
        "-q",
        "-m",
        "specs",
    )
    for rev in ("HEAD", None):
        assert acceptance._tree_specs(root, rev) == {
            "WI-005": queued,
            "WI-007": active,
        }, rev
        assert ar._spec_paths(root, rev) == {
            "WI-005": [archived, queued],
            "WI-007": [active],
            "WI-000": [example],
        }, rev
    assert [rel for rel, _read in ar.tree_specs(root, "HEAD")] == [
        "active/wi-007/WI-007-seven.md",
        "queued/WI-000-example.md",
        "queued/WI-005-five.md",
    ]
    with pytest.raises(ValueError, match="2 specs carry one id"):
        ar._spec_at(root, "HEAD", [archived, queued])
