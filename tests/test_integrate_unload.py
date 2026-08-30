"""integrate.py — the §5.6 unload: the branch AND its worker worktree (WI-359).

One of four modules `WI-521` slice 2 carved out of the 3,520-line
`test_integrate.py` monolith (M-06); the family and the rule for what is shared
are in `tests/integrate_fixtures.py`. This is the last act of the queue, and it
is the one with a destructive consequence, which is why it gets its own module:

After the merge the branch is deleted and a CLEAN linked worktree holding it is
GC'd, while a DIRTY one and the MAIN checkout are reported by branch and path on
stderr and left untouched. **"Dirty" counts IGNORED files and treats a failed
dirt read as dirt**: the content that exists nowhere else is usually the ignored
kind, and the consequence of a wrong answer is deletion. No outcome is
swallowed — a run that merged everything but left a branch held exits NONZERO,
because §5.6's stop is drained AND unloaded and nothing ever retries the unload.

The declared tool residue is the other half: a lane may be shed only when what
is left in it is EXACTLY the bar's own leavings, measured against the declared
set rather than a wildcard, and one undeclared file beside it refuses by name.
"""

import os

import pytest
from conftest import SCRIPTS, env_gate_skipif, run_py
from integrate_fixtures import (
    T_BASE,
    T_CODE,
    T_LATER,
    _branches,
    _commit,
    _git,
    _rev,
    _worktree_count,
    git_repo,
    integ,
    scaffolded_closed_branch,
)

pytestmark = env_gate_skipif("git")


def merged_branch_repo(tmp_path, ignore=None, files=None):
    """A trunk that has just merged `wi-401` --no-ff — the exact state
    `integrate_one` reaches immediately before it unloads the branch.

    `ignore` (a .gitignore body) is committed BEFORE the branch cut, so the rules
    are live on `wi-401` too: a worktree checked out from a branch that predates
    the .gitignore sees those paths as untracked, which would test the wrong
    read entirely. `files` (rel path -> body) are TRACKED neighbors committed the
    same way, for tests that need a lane-owned file standing beside residue."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git_repo(repo)
    if ignore:
        (repo / ".gitignore").write_text(ignore, encoding="utf-8", newline="\n")
    for rel, body in (files or {}).items():
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8", newline="\n")
    if ignore or files:
        _commit(repo, "chore: declare the ignore rules", when=T_BASE)
    _git(repo, "checkout", "-q", "-b", "wi-401")
    (repo / "widget.txt").write_text("1\n", encoding="utf-8", newline="\n")
    _commit(repo, "feat: the widget", when=T_CODE)
    _git(repo, "checkout", "-q", "main")
    _git(repo, "merge", "--no-ff", "-m", "integrate: merge wi-401 (WI-401)", "wi-401")
    return repo


def test_unload_deletes_the_merged_branch_when_nothing_holds_it(tmp_path):
    # The ordinary case, asserted so the two failure paths below are known to be
    # exceptions rather than the only behaviour the function has.
    repo = merged_branch_repo(tmp_path)
    unloaded, note = integ._unload_branch(repo, "wi-401")
    assert unloaded, note
    assert "unloaded wi-401" in note
    assert "wi-401" not in _branches(repo)


def test_the_holding_worktree_is_found_by_branch(tmp_path):
    # The lookup the report depends on: a branch checked out in a linked
    # worktree resolves to that worktree's PATH, so the operator is told where
    # the branch actually lives instead of only that the delete failed.
    repo = merged_branch_repo(tmp_path)
    worker = tmp_path / "worker"
    _git(repo, "worktree", "add", str(worker), "wi-401")

    holder, is_primary = integ._worktree_holding(repo, "wi-401")
    assert holder is not None and holder.samefile(worker)
    # A LINKED worktree, not the primary — git lists the main checkout first, so
    # the record index is what tells removable from un-removable.
    assert is_primary is False
    # A branch nothing has checked out resolves to nothing — the parse keys on
    # the record's `branch` line, not on the first `worktree` line it sees.
    assert integ._worktree_holding(repo, "no-such-branch") == (None, False)


def test_the_main_checkout_is_recognised_as_the_primary_worktree(tmp_path):
    # `git worktree list` includes the MAIN checkout, so a branch the trunk
    # itself has checked out resolves to a path that can NEVER be removed.
    repo = merged_branch_repo(tmp_path)
    _git(repo, "checkout", "-q", "wi-401")

    holder, is_primary = integ._worktree_holding(repo, "wi-401")
    assert holder is not None and holder.samefile(repo)
    assert is_primary is True


def test_unload_gcs_a_clean_worker_worktree_then_deletes_the_branch(tmp_path):
    # `git branch -d` refuses a branch checked out in a linked worktree. Where
    # the GC is SAFE the integrator owns it: a clean worktree holds nothing that
    # is not in the merged history, so it is removed and the delete retried —
    # this is the gap that let the old dispatcher accumulate 36 stale worktrees.
    repo = merged_branch_repo(tmp_path)
    worker = tmp_path / "worker"
    _git(repo, "worktree", "add", str(worker), "wi-401")

    unloaded, note = integ._unload_branch(repo, "wi-401")
    assert unloaded, note
    assert "worker" in note, note
    assert not worker.exists()
    assert "wi-401" not in _branches(repo)
    # The registration is gone too, not merely the directory — a pruned-but-
    # registered worktree is the residue the next `worktree add` trips over.
    # Counted rather than name-matched: pytest's tmp dir is itself named after
    # the test, so a substring check would find "worker" in the trunk's own row.
    assert _worktree_count(repo) == 1


def test_unload_reports_a_dirty_worker_worktree_and_touches_nothing(tmp_path):
    # The 2026-07-26 lesson: a worktree can hold orphaned files that exist
    # NOWHERE else, so dirt is evidence, not garbage. Nothing is forced — the
    # report names the branch, the path and the two commands, and the untracked
    # file is still on disk afterwards.
    repo = merged_branch_repo(tmp_path)
    worker = tmp_path / "worker"
    _git(repo, "worktree", "add", str(worker), "wi-401")
    (worker / "orphan.txt").write_text(
        "the only copy\n", encoding="utf-8", newline="\n"
    )

    unloaded, note = integ._unload_branch(repo, "wi-401")
    assert not unloaded
    assert "UNLOAD INCOMPLETE" in note
    assert "wi-401" in note and "worker" in note and "DIRTY" in note
    assert "git worktree remove" in note and "git branch -d" in note
    assert (worker / "orphan.txt").read_text(encoding="utf-8") == "the only copy\n"
    assert "wi-401" in _branches(repo)


def test_a_worktree_holding_only_gitignored_files_is_dirty(tmp_path):
    # The sharpest edge of the same lesson, and why the GC cannot read dirt with
    # `git status --porcelain` alone: the file that exists NOWHERE else is
    # typically an IGNORED one — a local `.env`. To a tracked-only read the
    # worktree looks pristine and `git worktree remove` deletes the lot without
    # a word. (The planted file was an out/run-logs/ session stream until
    # 2026-08-30 — that path is now DECLARED residue, the loop's own artifact
    # with a tracked clipped copy, C6/WI-548 — so the sole-copy example here is
    # the other canonical one.)
    repo = merged_branch_repo(tmp_path, ignore="out/\n.env\n")
    worker = tmp_path / "worker"
    _git(repo, "worktree", "add", str(worker), "wi-401")
    secret = worker / ".env"
    secret.write_text("the only copy of this key\n", encoding="utf-8", newline="\n")

    # The tracked-only read really does see nothing — this is the trap, pinned.
    assert integ.ac.working_tree_dirty(worker) == []
    assert integ._worktree_dirt(worker), "an ignored-only worktree must read dirty"

    unloaded, note = integ._unload_branch(repo, "wi-401")
    assert not unloaded
    assert "UNLOAD INCOMPLETE" in note and "DIRTY" in note
    assert secret.read_text(encoding="utf-8") == "the only copy of this key\n"


# The 2026-08-01 drain's holding set, verbatim (docs/archive/history/backlog-plan-2026-08-01.md
# row 9): every one of the five lane merges exited 1 at unload over these same
# six ignored paths — pure tool caches plus the gitignored generated trace
# report — and each worktree had to be removed by hand with --force. As files,
# one representative per measured path.
MEASURED_RESIDUE = (
    ".pytest_cache/v/cache/lastfailed",
    ".ruff_cache/0.8.0/12345",
    "__pycache__/conftest.cpython-313.pyc",
    "docs/test/report.md",
    "project-trajectory/scripts/__pycache__/integrate.cpython-313.pyc",
    "tests/__pycache__/test_widget.cpython-313.pyc",
)

# This repo's own ignore rules for those paths, mirrored so the fixture lane
# reads them as IGNORED (untracked-not-ignored would test the wrong ladder rung).
LANE_IGNORE = (
    "__pycache__/\n*.py[cod]\n.pytest_cache/\n.ruff_cache/\n"
    "docs/test/report.md\ndocs/test/report.html\nout/\n"
)


def residue_lane(tmp_path):
    """A merged lane worktree dirtied with EXACTLY the measured residue set,
    plus a tracked neighbor in `docs/test/` so the shed's reach is visible."""
    repo = merged_branch_repo(
        tmp_path,
        ignore=LANE_IGNORE,
        files={"docs/test/test-cases.csv": "TC-ID\n"},
    )
    worker = tmp_path / "worker"
    _git(repo, "worktree", "add", str(worker), "wi-401")
    for rel in MEASURED_RESIDUE:
        target = worker / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("tool residue\n", encoding="utf-8", newline="\n")
    return repo, worker


def test_unload_sheds_the_declared_tool_residue_and_removes_the_lane(tmp_path):
    # The defect this WI closes: a lane whose worker ever ran the suite arrives
    # at the merge slot holding tool caches git ignores, `_worktree_dirt` reads
    # them as dirt, and the unload refuses FOREVER — five of five lanes in the
    # 2026-08-01 drain. A lane dirty with exactly the DECLARED residue now
    # unloads clean through the integrator's own arm, with no --force anywhere.
    repo, worker = residue_lane(tmp_path)
    assert integ._worktree_dirt(worker), "fixture must start dirty to git"

    unloaded, note = integ._unload_branch(repo, "wi-401")
    assert unloaded, note
    assert not worker.exists()
    assert "wi-401" not in _branches(repo)
    assert _worktree_count(repo) == 1


def test_one_undeclared_file_beside_the_residue_still_refuses_named(tmp_path):
    # The orphan read is NOT loosened: the same lane plus ONE undeclared file
    # still refuses, and the refusal names the actual remainder rather than the
    # residue that was shed around it — the distinction, observable.
    repo, worker = residue_lane(tmp_path)
    (worker / "orphan.txt").write_text(
        "the only copy\n", encoding="utf-8", newline="\n"
    )

    unloaded, note = integ._unload_branch(repo, "wi-401")
    assert not unloaded
    assert "UNLOAD INCOMPLETE" in note and "DIRTY" in note
    assert "orphan.txt" in note
    assert ".pytest_cache" not in note, note
    assert (worker / "orphan.txt").read_text(encoding="utf-8") == "the only copy\n"
    assert "wi-401" in _branches(repo)


def test_the_shed_covers_the_loops_own_stream_but_never_the_root_out(tmp_path):
    # DELIBERATELY OVERTURNED 2026-08-30 (C6, the stall-guard plan; WI-548):
    # the ignored out/run-logs/ session stream is the LOOP'S OWN artifact —
    # its clipped copy is tracked under docs/iteration/ — and every mechanized
    # lane of the 2026-08-30 run ended UNLOAD INCOMPLETE over exactly it,
    # ending the run after every merge. It is now DECLARED residue (so is the
    # C2 out/review-owed marker, moot once the lane merged): the lane unloads
    # clean and both go with it. The other boundary STANDS: the shed operates
    # only inside the lane, so the repo-root out/ (WI-398's
    # refresh-refused-<branch>.log lives OUTSIDE any lane worktree) is never
    # reached.
    repo, worker = residue_lane(tmp_path)
    stream = worker / "out" / "run-logs" / "wi-401-003-20260830-161822.log"
    stream.parent.mkdir(parents=True)
    stream.write_text("the loop's own stream\n", encoding="utf-8", newline="\n")
    (worker / "out" / "review-owed").write_text(
        "train = wi-401\n", encoding="utf-8", newline="\n"
    )
    root_log = repo / "out" / "run-logs" / "refresh-refused-wi-401.log"
    root_log.parent.mkdir(parents=True)
    root_log.write_text("refresh refused\n", encoding="utf-8", newline="\n")

    unloaded, note = integ._unload_branch(repo, "wi-401")
    assert unloaded, note
    assert not worker.exists()
    assert root_log.read_text(encoding="utf-8") == "refresh refused\n"
    assert "wi-401" not in _branches(repo)


def test_the_declared_residue_set_is_exactly_the_bars_own_leavings():
    # The declaration, stated as data: every measured 2026-08-01 path is
    # declared residue; every name that CAN hold sole-copy evidence is not.
    for rel in MEASURED_RESIDUE:
        assert integ._is_declared_residue(rel), rel
    # Widened on measurement, the WI-400 scope guard working as designed:
    # check.py passes --html to its trace step at DevStg-Tests/DevStg-Impl, so the DECLARED bar
    # writes docs/test/report.html in whatever lane it runs in, and on
    # 2026-08-02 the wi-402 lane was measured holding exactly that file at
    # unload. Same class as report.md — rebuilt by the next bar run, sole-copy
    # evidence never (WI-407, REVIEW-A finding 2).
    assert integ._is_declared_residue("docs/test/report.html")
    # C6 (2026-08-30, WI-548): the loop's OWN artifacts joined the declared
    # set on measurement — every mechanized lane refused unload over its own
    # session stream, whose clipped copy is tracked under docs/iteration/.
    assert integ._is_declared_residue("out/run-logs/wi-401-003-20260830-161822.log")
    assert integ._is_declared_residue("out/review-owed")
    # ... and ONLY the loop's own stream shape (round 4): a foreign file under
    # the same directory is a surprise, and a surprise is evidence.
    for rel in (
        ".env",
        "orphan.txt",
        "docs/test/notes.md",
        "src/widget.pyc",
        "out/other-file.txt",
        "out/run-logs/session.md",
        "out/run-logs/operator-notes.txt",
        "out/run-logs/wi-401-003.log",
    ):
        assert not integ._is_declared_residue(rel), rel


def test_a_lane_holding_the_bars_html_report_unloads_clean(tmp_path):
    # REVIEW-A finding 2's judgment, taken with its test: the measured residue
    # set plus the bar's OWN html report unloads clean through the integrator's
    # arm — and the shed still operates only inside the lane, so the repo-root
    # out/ (WI-398's refresh-refused logs, outside any lane) is never reached.
    repo, worker = residue_lane(tmp_path)
    html = worker / "docs" / "test" / "report.html"
    html.write_text("<html>trace report</html>\n", encoding="utf-8", newline="\n")
    root_log = repo / "out" / "run-logs" / "refresh-refused-wi-401.log"
    root_log.parent.mkdir(parents=True)
    root_log.write_text("refresh refused\n", encoding="utf-8", newline="\n")

    unloaded, note = integ._unload_branch(repo, "wi-401")
    assert unloaded, note
    assert not worker.exists()
    assert "wi-401" not in _branches(repo)
    assert _worktree_count(repo) == 1
    assert root_log.read_text(encoding="utf-8") == "refresh refused\n"


@pytest.mark.skipif(os.name == "nt", reason="backslash is a separator on Windows")
def test_a_posix_backslash_name_no_longer_aliases_onto_a_tracked_path(tmp_path):
    # REVIEW-A finding 1, the reviewer's driven fixture: on POSIX a git-ignored
    # file literally NAMED x\__pycache__\evil.pyc was reported by
    # `ignored_files` as x/__pycache__/evil.pyc — `_is_declared_residue`
    # matched the mangled segments and the shed unlinked the TRACKED twin the
    # double-lock exists to protect. The normalization is Windows-only now: the
    # raw name has no "/" segments, matches nothing, and the alias file is
    # ordinary undeclared dirt — the unload refuses, and the twin SURVIVES.
    repo = merged_branch_repo(tmp_path, ignore=LANE_IGNORE)
    worker = tmp_path / "worker"
    _git(repo, "worktree", "add", str(worker), "wi-401")
    twin = worker / "x" / "__pycache__" / "evil.pyc"
    twin.parent.mkdir(parents=True)
    twin.write_text("tracked twin\n", encoding="utf-8", newline="\n")
    _git(worker, "add", "-f", "x/__pycache__/evil.pyc")
    _commit(worker, "feat: force-added tracked twin", when=T_LATER)
    _git(repo, "merge", "-q", "wi-401")  # keep the branch fully merged
    alias = worker / "x\\__pycache__\\evil.pyc"
    alias.write_text("ignored alias\n", encoding="utf-8", newline="\n")

    unloaded, note = integ._unload_branch(repo, "wi-401")
    assert not unloaded
    assert "UNLOAD INCOMPLETE" in note and "DIRTY" in note
    assert twin.read_text(encoding="utf-8") == "tracked twin\n", (
        "the shed deleted the tracked twin through the mangled alias"
    )
    assert alias.is_file(), "the alias file itself is evidence, never shed"
    assert "wi-401" in _branches(repo)


def test_the_backslash_normalization_is_windows_only(monkeypatch):
    # The mechanism behind the fixture above, unit-pinned on both arms so each
    # platform drives the other's behaviour too: git itself emits "/" on every
    # platform, so the replace is pure defense — legitimate only on Windows,
    # where "\" is a separator and never a filename byte. On POSIX it is a
    # filename byte, and normalizing it MINTS the alias.
    from pathlib import Path

    reported = (0, "x\\__pycache__\\evil.pyc\0sub/cache.pyc\0")
    monkeypatch.setattr(integ.ac, "git", lambda *a: reported)
    # The Path is built BEFORE os.name is patched: on the 3.11 floor Path()
    # dispatches on os.name at instantiation, so constructing it under the
    # posix patch mints a PosixPath and raises NotImplementedError on Windows
    # — and the exception detonates inside pytest's own reporting while the
    # patch is live, killing the whole session as an INTERNALERROR (xdist
    # worker crash). Python 3.13 removed that error, which is how this
    # slipped the floor (found 2026-08-15, sitting sweep).
    unused = Path("unused")
    monkeypatch.setattr(os, "name", "posix")
    assert integ.ignored_files(unused) == {
        "x\\__pycache__\\evil.pyc",
        "sub/cache.pyc",
    }
    monkeypatch.setattr(os, "name", "nt")
    assert integ.ignored_files(unused) == {
        "x/__pycache__/evil.pyc",
        "sub/cache.pyc",
    }


def test_the_sweep_leaves_a_non_ignored_empty_cache_directory_alone(tmp_path):
    # REVIEW-A finding 3: the directory half of the shed carried only the NAME
    # lock — an empty untracked x/__pycache__/keep/ in a repo whose rules do
    # NOT ignore __pycache__ was rmdir'd although it is the lane's (emptiness
    # can be load-bearing: the docstring's own docs/work/deferred/ example).
    # The sweep now carries the ignored lock too: git check-ignore must claim
    # the directory before it is removed.
    repo = merged_branch_repo(tmp_path)  # no ignore rules at all
    worker = tmp_path / "worker"
    _git(repo, "worktree", "add", str(worker), "wi-401")
    keep = worker / "x" / "__pycache__" / "keep"
    keep.mkdir(parents=True)

    integ._shed_declared_residue(worker)
    assert keep.is_dir(), "emptiness git does not ignore belongs to the lane"


def test_unload_run_from_inside_the_lane_steps_out_before_removing(
    tmp_path, monkeypatch
):
    # The second driven fact from the same day (the WI-397 close): `git
    # worktree remove` run from INSIDE the lane fails "Permission denied"
    # AFTER half-unregistering the worktree, leaving an empty directory. The
    # unload arm steps out of the lane before removing it, so the inside
    # invocation is safe — and the process ends standing somewhere that exists.
    from pathlib import Path

    repo = merged_branch_repo(tmp_path)
    worker = tmp_path / "worker"
    _git(repo, "worktree", "add", str(worker), "wi-401")
    monkeypatch.chdir(worker)

    unloaded, note = integ._unload_branch(repo, "wi-401")
    assert unloaded, note
    assert not worker.exists()
    # Raises on Linux (and reads as a deleted dir elsewhere) if the guard is
    # gone: without the chdir the process is left inside the removed lane.
    assert Path.cwd().exists()


def test_a_dirt_read_git_cannot_perform_counts_as_dirty(tmp_path):
    # Fail direction, stated as a test: an unreachable, corrupt or
    # permission-denied worktree must read DIRTY, never clean. A fail-open read
    # here would be the one fail-open path in a fail-closed script — and the one
    # whose consequence is deletion.
    dirt = integ._worktree_dirt(tmp_path / "not-a-worktree-at-all")
    assert dirt, "a dirt read git could not perform must never read as clean"
    assert "could not read this worktree" in dirt[0]


def test_unload_never_prescribes_removing_the_main_checkout(tmp_path):
    # `git worktree remove` refuses the primary FOREVER, so naming it as the
    # remedy would send the operator after a command that can never succeed. The
    # main checkout gets its own message — switch it off the branch — and is
    # never a removal candidate, dirty or clean.
    repo = merged_branch_repo(tmp_path)
    _git(repo, "checkout", "-q", "wi-401")

    unloaded, note = integ._unload_branch(repo, "wi-401")
    assert not unloaded
    assert "UNLOAD INCOMPLETE" in note
    assert "MAIN checkout" in note
    assert "git worktree remove" not in note, note
    assert "git branch -d wi-401" in note
    assert repo.is_dir() and "wi-401" in _branches(repo)


def test_a_branch_that_survives_with_no_holder_is_still_reported(tmp_path):
    # The swallow this replaces: `branch -d` on an UNMERGED branch fails and the
    # old code discarded the code and the message both. There is no worktree to
    # name here, so the git refusal itself has to reach the operator.
    repo = merged_branch_repo(tmp_path)
    _git(repo, "checkout", "-q", "-b", "wi-402")
    (repo / "unmerged.txt").write_text("x\n", encoding="utf-8", newline="\n")
    _commit(repo, "feat: never merged", when=T_LATER)
    _git(repo, "checkout", "-q", "main")

    unloaded, note = integ._unload_branch(repo, "wi-402")
    assert not unloaded
    assert "UNLOAD INCOMPLETE" in note
    assert "wi-402" in note
    assert "no registered worktree holds it" in note
    assert "wi-402" in _branches(repo)


def test_the_queue_gcs_a_clean_worker_worktree_end_to_end(tmp_path):
    # WI-359 through the real CLI: the §5.6 "drained and unloaded" stop is not
    # reached while a branch or its worktree lingers, so the queue must finish
    # the job itself on the safe path rather than leaving hand cleanup behind.
    repo, _claim_sha = scaffolded_closed_branch(tmp_path)
    worker = tmp_path / "worker"
    _git(repo, "worktree", "add", str(worker), "wi-401")

    proc = run_py([SCRIPTS / "integrate.py", "integrate", "--tier", "smoke"], cwd=repo)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out

    assert "integrate: wi-401 merged (WI-401=merged)" in out, out
    assert "GC'd clean worker worktree" in out, out
    assert not worker.exists(), out
    assert "wi-401" not in _branches(repo)
    # The trunk is the only registration left — the drained-and-unloaded stop,
    # in full. Note WHERE the bar ran to get here: in this very worktree. The
    # refresh sheds its own bar residue precisely so the §5.6 GC still sees a
    # clean tree; without that, every merge would exit nonzero over caches the
    # integrator had just created itself.
    assert _worktree_count(repo) == 1


def test_the_queue_exits_nonzero_when_a_merged_branch_stays_held(tmp_path):
    # The other half, and the assertion that the silent swallow is gone. §5.6's
    # stop is drained AND unloaded, and nothing ever retries an unload — a merged
    # branch is no longer a finished claimed branch, so the next queue run will
    # not see it. A green exit here would report a stop the run did not reach, so
    # the remainder is named on STDERR by branch and path and carried to the
    # exit code. The MERGE still stands: the trunk fast-forwarded before the
    # unload, and the nonzero code reports debt, it does not undo work.
    repo, _claim_sha = scaffolded_closed_branch(tmp_path)
    trunk_before = _rev(repo, "HEAD")
    worker = tmp_path / "worker"
    _git(repo, "worktree", "add", str(worker), "wi-401")
    # Refresh FIRST, on a clean lane (WI-386: the refresh resets to the last
    # work commit, so it refuses a dirty lane outright rather than resetting
    # over uncommitted work). The orphan then appears the way it really does —
    # after the lane finished — and the unload is what has to deal with it.
    proc = run_py(
        [SCRIPTS / "integrate.py", "refresh", "--branch", "wi-401", "--tier", "smoke"],
        cwd=repo,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    (worker / "orphan.txt").write_text(
        "the only copy\n", encoding="utf-8", newline="\n"
    )

    proc = run_py([SCRIPTS / "integrate.py", "integrate", "--tier", "smoke"], cwd=repo)
    out = proc.stdout + proc.stderr
    assert proc.returncode != 0, out
    assert "integrate: wi-401 merged (WI-401=merged)" in out, out

    assert "UNLOAD INCOMPLETE" in proc.stderr, out
    assert "STILL HELD - wi-401 at" in proc.stderr, out
    assert "INCOMPLETE - 1 merged branch(es) NOT unloaded" in proc.stderr, out
    assert "wi-401" in proc.stderr and "worker" in proc.stderr

    # The merge landed and stays landed — the exit code is about the remainder.
    assert _rev(repo, "HEAD") != trunk_before
    assert _git(repo, "log", "-1", "--format=%s").strip().startswith("integrate: merge")
    assert (worker / "orphan.txt").is_file()
    assert "wi-401" in _branches(repo)


def test_a_foreign_file_beside_the_loops_streams_refuses_by_name(tmp_path):
    # Round 4 (WI-548): the shed reaches the loop's OWN streams by NAME, never
    # the directory — an operator's sole-copy note beside them survives
    # byte-for-byte, the unload refuses naming it, and the stream that IS the
    # loop's is not what the refusal names.
    repo, worker = residue_lane(tmp_path)
    logs = worker / "out" / "run-logs"
    logs.mkdir(parents=True)
    (logs / "wi-401-003-20260830-161822.log").write_text(
        "the loop's own stream\n", encoding="utf-8", newline="\n"
    )
    note = logs / "operator-notes.txt"
    note.write_text("the only copy of these notes\n", encoding="utf-8", newline="\n")

    unloaded, message = integ._unload_branch(repo, "wi-401")
    assert not unloaded
    assert "UNLOAD INCOMPLETE" in message and "DIRTY" in message
    # git's ignored listing collapses an ignored directory to one entry, so the
    # refusal names the holding `out/` (the same shape the other residue tests
    # see) — never the stream that IS the loop's.
    assert "out/" in message
    assert "20260830-161822" not in message, message
    assert note.read_text(encoding="utf-8") == "the only copy of these notes\n"
    assert worker.exists()
    assert "wi-401" in _branches(repo)
