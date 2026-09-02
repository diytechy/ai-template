"""The BOUNDARY of the acceptance-record split (WI-521 slice 1).

`acceptance_record.py` came out of `check_trajectory.py` verbatim, so the
amendment and mirror RULES themselves are already covered where they always
were — `tests/test_trajectory_staged.py` drives them through the CLI and
`tests/test_baseline_snapshot.py` through the API. Re-asserting them here would
be duplication, and the thing a verbatim move can silently lose is not a rule
but the LINE: the seam that made the cut honest, and the shims that make it
invisible to callers.

So every test here pins the boundary rather than a finding:

  * the module's dependency surface, which is the whole argument for the cut —
    two names and no filesystem;
  * that it never reaches back up into the checker (the extracted module must
    stay BELOW every module that reads it, `WI-483`'s rule);
  * that `check_trajectory` re-exports the same OBJECTS rather than
    re-implementing anything, so a second opinion cannot grow;
  * that `_git` resolves to the one declared home in both modules.
"""

import ast

from conftest import SCRIPTS, load_script

acceptance_record = load_script("acceptance_record")
baseline_snapshot = load_script("baseline_snapshot")
check_trajectory = load_script("check_trajectory")

SOURCE = (SCRIPTS / "acceptance_record.py").read_text(encoding="utf-8")
TREE = ast.parse(SOURCE)

# Every name the module defines at module scope and re-exports through the
# checker. The list is EXPLICIT rather than derived from `dir()`: the point of
# the shim is that a caller written against the old spelling still resolves, and
# a derived list would silently shrink with the thing it is meant to hold.
MOVED = (
    "SPINE_CSVS",
    "SPINE_TABLE",
    "SPINE_COLUMN",
    "SPINE_TRACED_CELLS",
    "SPINE_APPROVED_CELLS",
    "HAT_REFS_CELL",
    "SNAPSHOT_DIR",
    "SNAPSHOT_README",
    "_APPROVED_TEXT",
    "_spine_stem",
    "_spine_carriers",
    "_spine_rows_at",
    "_spine_revs",
    "_snapshot_survives",
    "_snapshot_write_revs",
    "spine_cell_class",
    "traced_cells",
    "split_changed_cells",
    "staged_spine_amendments",
    "staged_spine_findings",
    "staged_hat_refs_findings",
    "staged_snapshot_findings",
    "committed_snapshot_findings",
)


def _imported_roots():
    """Top-level module names this file imports, anywhere — function bodies
    included, so a deferred import cannot hide from the census."""
    roots = set()
    for node in ast.walk(TREE):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            roots.add(node.module.split(".")[0])
    return roots


def test_the_dependency_surface_is_the_argument_for_the_split():
    """Two names, and that is the whole import list.

    This is the measurement that made the cut defensible rather than a line
    count: the 677 moved lines referenced exactly `spine_carrier` and one git
    primitive out of everything `check_trajectory.py` had in scope — no
    `argparse`, `csv`, `re`, `difflib`, `configparser` or `pathlib`. A seam that
    narrow is found, not carved. If a future edit widens it, the split's premise
    has changed and that should be argued, not absorbed.
    """
    assert _imported_roots() == {"spine_carrier", "kitlib", "sys", "pathlib"}, sorted(
        _imported_roots()
    )
    # `sys`/`pathlib` are the sanctioned-sibling fallback only — they must not
    # be reachable as module attributes for a rule to use.
    assert not hasattr(acceptance_record, "csv")
    assert not hasattr(acceptance_record, "re")


def test_it_never_reads_the_working_tree():
    """Every read goes through git, which is what "compares two trees" MEANS.

    `check_trajectory.py`'s other half is a working-tree validator; this half
    asks what a revision held. If a rule here ever calls `open()` or builds a
    `Path`, the two halves have started answering the same question again and
    the boundary sentence in the module docstring has stopped being true.
    """
    calls = {
        node.func.id
        for top in TREE.body
        if isinstance(top, ast.FunctionDef)
        for node in ast.walk(top)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    # Scoped to the RULES, not the file: the sanctioned-sibling import guard at
    # module scope builds one `Path(__file__)` to find its own directory, which
    # is the house idiom every extracted sibling carries and reads no repository
    # content at all.
    assert "open" not in calls
    assert "Path" not in calls


def test_it_does_not_import_the_module_it_came_out_of():
    """The extracted module sits BELOW its reader (WI-483's layering rule).

    `check_trajectory` imports this one unguarded; the reverse edge would be a
    cycle, and `tests/test_import_layers.py` would red on it. Pinned here too
    because that file measures the whole graph while this states the one edge
    the split created, so a reader of either learns the direction.
    """
    assert "check_trajectory" not in _imported_roots()
    assert not hasattr(acceptance_record, "check_trajectory")


def test_the_checker_re_exports_the_same_objects_not_copies():
    """Identity, not equality — a copy is how a second opinion starts.

    Every former spelling still resolves on `check_trajectory` (no caller
    moved), and each one IS the object the new module defines. Asserting
    equality would pass for a re-implementation that happened to agree today.

    The reference is `check_trajectory.acceptance_record` — the module object
    the checker itself imported — and NOT this file's `load_script` copy:
    `load_script` execs a fresh module that never enters `sys.modules`, so the
    two are legitimately different objects and comparing across them would
    measure the test harness rather than the shim.
    """
    source = check_trajectory.acceptance_record
    for name in MOVED:
        assert hasattr(acceptance_record, name), "moved name missing: " + name
        assert hasattr(check_trajectory, name), "shim missing: " + name
        assert getattr(check_trajectory, name) is getattr(source, name), (
            "check_trajectory.{} is not the acceptance_record object — a "
            "re-implementation, not a re-export".format(name)
        )


def test_the_moved_block_left_no_definition_behind():
    """The move was verbatim, so the old home defines none of it any more.

    Parses `check_trajectory.py`'s SOURCE rather than reading its namespace,
    because the re-export assignments above put every name back on the module
    object — the only place the difference is visible is the file itself.
    """
    old = ast.parse((SCRIPTS / "check_trajectory.py").read_text(encoding="utf-8"))
    defined = {
        node.name
        for node in old.body
        if isinstance(node, (ast.FunctionDef, ast.ClassDef))
    }
    assert not defined & set(MOVED), sorted(defined & set(MOVED))


def test_the_git_degrade_has_one_home_in_both_modules():
    """`kitlib.git.git_out` is the declared home for "git, or None".

    `check_trajectory._git` was a fourth copy of it that the D-8/`OI-16`
    consolidation missed — the same body plus an optional `stdin`, which is why
    it read as a different function. Both spellings are now that one object; a
    future edit that re-opens a local body fails here rather than drifting.
    """
    from kitlib import git as kitgit

    assert acceptance_record._git is kitgit.git_out
    assert check_trajectory._git is kitgit.git_out


def test_git_out_passes_batch_input_through():
    """The `stdin` parameter is load-bearing, not decorative.

    `committed_snapshot_findings` asks git about many blobs in ONE
    `cat-file --batch-check` call because that scan rides the always-on floor.
    Folding the fourth copy into `kitlib.git` had to carry that, so it is driven
    rather than assumed — and the default (no input) is driven beside it, since
    that is the behaviour every other caller of `git_out` already had.
    """
    from conftest import ROOT
    from kitlib import git as kitgit

    out = kitgit.git_out(ROOT, ["cat-file", "--batch-check"], stdin="HEAD\n")
    assert out is not None and " commit " in out
    assert kitgit.git_out(ROOT, ["rev-parse", "--verify", "HEAD"]) is not None


def test_the_cell_split_tables_still_cover_both_halves():
    """The one INVARIANT worth restating at the new home, because it is the
    reason the tables are here at all: a column in neither set falls through to
    APPROVED (fail-safe loud, never silently un-approved), and the two halves
    must not disagree about a column they both name."""
    for rel, _ in acceptance_record.SPINE_CSVS:
        traced = acceptance_record.SPINE_TRACED_CELLS[rel]
        approved = acceptance_record.SPINE_APPROVED_CELLS[rel]
        assert not traced & approved, (rel, sorted(traced & approved))
        assert acceptance_record.spine_cell_class(rel, "NoSuchColumn") == "approved"


def test_no_snapshotted_tier_can_go_unseen_by_the_approval_rung():
    """The approval-act reader's registry set and the snapshot's are ONE closed
    statement (WI-572 REVIEW-A round 7, MAJOR 1).

    `lane_approval_refusal` walks `APPROVAL_ACT_CSVS` — the four SPINE tiers,
    SN/SR/LLR/TC — while `baseline_snapshot.SNAPSHOTTED` names SEVEN registries
    whose `Status` a snapshot anchors. Both are hand-written literals, in
    different modules, hundreds of lines apart, and NOTHING joined them: a tier
    could be added to the snapshot and reach no approval reader at all,
    silently. The remaining narrowness is RULED — the owner's 2026-09-01 ruling
    scopes the act to SPINE rows, and the off-spine three carry approval cells
    governed by OI-30 D3 — so this pin does not decide the rung's width. It
    makes the boundary a statement someone must edit ON PURPOSE.

    ROUND 028 MOVED ONE TIER ACROSS IT, which is the pin working as intended:
    `stakeholder-needs.toml` left `OUTSIDE_THE_APPROVAL_ACT` for the covered
    set, because SN is a spine tier and the half of DevStg-Reqs the dial holds
    for the owner — a lane flipping it is the worst case, not an exempt one.

    A new tier therefore fails HERE, naming itself, and its author has to put it
    on one side or the other."""
    snapshotted = set(baseline_snapshot.SNAPSHOTTED)
    refused = {rel for rel, _ in acceptance_record.APPROVAL_ACT_CSVS}
    declared_out = set(acceptance_record.OUTSIDE_THE_APPROVAL_ACT)

    # Neither side may name a registry the snapshot does not anchor...
    assert refused <= snapshotted, sorted(refused - snapshotted)
    assert declared_out <= snapshotted, sorted(declared_out - snapshotted)
    # ...the two sides are disjoint (a tier cannot be both refused and exempt)...
    assert not refused & declared_out, sorted(refused & declared_out)
    # ...and TOGETHER they are exhaustive, which is the property that makes
    # "a snapshotted tier no approval reader sees" unconstructible rather than
    # merely absent.
    assert refused | declared_out == snapshotted, sorted(
        snapshotted - (refused | declared_out)
    )


def test_an_off_spine_status_flip_is_not_the_act_this_rung_refuses(tmp_path):
    """The DELIBERATE half of the boundary above, driven rather than declared.

    The review found no test asserting either that the off-spine tiers are
    refused or that they are out of scope, so the omission read as an
    oversight from the outside. It is the ruling: a lane may move an interface
    row's `status`, and that is not the approval act on a spine row. (The SN
    tier was in this exempt set until round 028 and is now covered — see
    `tests/test_intake.py::test_a_lane_flipping_a_STAKEHOLDER_NEED_is_refused_and_mints_nothing`.) Driven
    against a real git tree so this pins the READER's behaviour, not a re-reading
    of the constant the test above already pins."""
    import subprocess

    def git(*args):
        subprocess.run(
            ["git", "-C", str(tmp_path)] + list(args),
            check=True,
            capture_output=True,
            stdin=subprocess.DEVNULL,
        )

    git("init")
    git("config", "user.email", "loop@example.com")
    git("config", "user.name", "Loop Test")
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True)
    interfaces = req / "interfaces.toml"
    interfaces.write_text(
        '[interface.IF-001]\nowner = "scripts/demo"\nstatus = "Drafted"\n',
        encoding="utf-8",
    )
    git("add", "-A")
    git("commit", "-q", "-m", "seed")

    # The flip an off-spine tier CAN carry: Drafted -> Approved on its own cell.
    interfaces.write_text(
        '[interface.IF-001]\nowner = "scripts/demo"\nstatus = "Approved"\n',
        encoding="utf-8",
    )
    git("add", "-A")
    git("commit", "-q", "-m", "approve the seam")

    assert acceptance_record.staged_approval_acts(tmp_path, "HEAD~1", "HEAD") == []
    assert (
        acceptance_record.lane_approval_refusal(tmp_path, "HEAD~1", "HEAD") is None
    ), "an off-spine flip is outside the ruled scope of this rung"
