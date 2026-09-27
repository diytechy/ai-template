"""bookkeeping.py — the ONE trunk bookkeeping commit the claim and the mint share.

The loop's two trunk-side writers, `integrate.claim` and the intake mint, run in
the PRIMARY checkout, which is also where the owner works. Before WI-612 each
treated that whole working tree as its own: `git add -A` swept whatever was
lying there into the claim or mint commit, and `git reset --hard HEAD` (plus the
mint's `git clean -fd`) discarded it when either refused. What is pinned here is
the property that replaced them, driven on real repositories with the real
regeneration:

  * an unrelated modified file, an unrelated untracked file and an unrelated
    STAGED edit survive a successful claim, a refused claim, a refused mint and
    a successful mint byte-for-byte, and none of them lands in any commit;
  * a dirty path the step itself must write refuses BY NAME before anything is
    written - a hand-edited `docs/status.md` under regeneration, and a
    committed note the claim's link-aware move must rewrite whose uncommitted
    edit hides the link - and "before anything is written" is proven by
    counting the step's write entry points, not inferred from the final tree;
  * the scope is planned over HEAD: an uncommitted note ADDING a link to the
    spec neither widens the claim nor is touched;
  * the step and its regeneration run in a scratch worktree cut from HEAD
    (WI-647): an owner edit to an in-scope path made while the regeneration is
    blocked survives, is absent from the commit, and the step refuses naming
    it; an uncommitted edit to a generator INPUT outside the scope does not
    shape the artifacts the commit carries; and the regeneration runs the kit
    as HEAD commits it, not an uncommitted edit to it;
  * the drift check runs after the caller's `before_advance`: an edit landing
    during the claim's branch cut is named and left, and the branch it leaves
    is the abandoned claim the next claim re-cuts;
  * a step that RAISES leaves the checkout untouched and says so, and a scratch
    worktree that will not remove is named instead of leaving silent residue;
  * a refusal inside the install restores what the install wrote, while an
    owner edit landing on an in-scope path in that window is left and named;
  * no bookkeeping path in the primary checkout keeps a whole-tree git write;
  * the owner-only scratchpad no longer stops the merge slot (the dispatcher's
    own tick-top check is pinned beside its siblings in tests/test_dispatch.py).

The helper is reached THROUGH its two callers (`integ.bookkeeping`, never a
second `load_script` copy), because the claim of the design is that both
callers share one module object - a private copy would test something neither
caller runs.
"""

import ast
import threading
import time
from pathlib import Path

import pytest
from conftest import SCRIPTS, env_gate_skipif, load_script, run_py
from integrate_fixtures import (
    T_VERDICT,
    _branches,
    _commit,
    _git,
    _rev,
    _worktree_count,
    claim_repo,
    git_repo,
    integ,
    write_spec,
    write_watermark,
)

pytestmark = env_gate_skipif("git")

intake = load_script("intake")

GAP = "SR-001 is not Approved (Status=Drafted)"

# The owner's work, left lying in the primary checkout: one tracked file
# modified, one untracked, one STAGED. The staged one is the edit a commit built
# from the real index would carry even if it staged nothing else itself.
OWNER_EDITS = {
    "seed.txt": "the owner's half-written edit\n",
    "notes.txt": "an untracked note\n",
    "staged.txt": "a staged edit\n",
}
OWNER_STATUS = {"seed.txt": " M", "notes.txt": "??", "staged.txt": "M "}

# A trunk step that gets as far as writing a declared artifact and then fails -
# the refusal arrives AFTER the step has written, so the restore is exercised.
FAILING_REGEN = """import pathlib, sys
pathlib.Path("PROJECT_STATE.html").write_text("half-regenerated\\n", encoding="utf-8")
print("regen FAILED at trajectory (exit 1)", file=sys.stderr)
sys.exit(1)
"""

# A trunk step that only records that it ran, next to itself (outside the repo).
RECORDING_REGEN = """import pathlib, sys
pathlib.Path(sys.argv[0]).with_name("ran").write_text("ran\\n", encoding="utf-8")
"""

# The REAL trunk step, held at its door: it records where it was started, says
# it is blocked, and waits for the test to release it before running the real
# regeneration with the same arguments. What the test does while it waits is
# what an owner could do while a claim runs.
BLOCKING_REGEN = """import pathlib, subprocess, sys, time
here = pathlib.Path(sys.argv[0]).resolve().parent
(here / "cwd").write_text(str(pathlib.Path.cwd()), encoding="utf-8")
(here / "blocked").write_text("", encoding="utf-8")
deadline = time.monotonic() + 120
while not (here / "release").exists():
    if time.monotonic() > deadline:
        sys.exit("the test never released the regeneration")
    time.sleep(0.05)
sys.exit(subprocess.call([sys.executable, {real!r}, *sys.argv[1:]]))
"""

# A status page whose generated block the real regeneration rewrites, so the
# claim's own tree writes docs/status.md; the prose outside it is the owner's.
STATUS_WITH_BLOCK = (
    "# Status\n\nhand-authored\n\n<!-- BEGIN GENERATED STATUS -->\nstale\n"
    "<!-- END GENERATED STATUS -->\n"
)


def trunk(tmp_path):
    """Two queued WIs on a committed trunk that also carries a hand-authored
    `docs/status.md` (a path the regeneration writes), plus the three files the
    owner is about to edit."""
    root = tmp_path / "repo"
    root.mkdir()
    claim_repo(root)
    write_spec(
        root, "queued", "WI-402", slug="gadget", title="Gadget", specref="seed.txt"
    )
    write_watermark(root, WI=402)
    (root / "docs" / "status.md").write_text(
        "# Status\n\nhand-authored\n", encoding="utf-8", newline="\n"
    )
    (root / "staged.txt").write_text("staged base\n", encoding="utf-8", newline="\n")
    _commit(root, "setup", when=T_VERDICT)
    return root


def leave_owner_edits(root):
    for name, text in OWNER_EDITS.items():
        (root / name).write_text(text, encoding="utf-8", newline="\n")
    _git(root, "add", "--", "staged.txt")


def assert_owner_edits_untouched(root):
    for name, text in OWNER_EDITS.items():
        assert (root / name).read_text(encoding="utf-8") == text, name
    status = {
        line[3:]: line[:2]
        for line in _git(root, "status", "--porcelain").splitlines()
        if line.strip()
    }
    for name, code in OWNER_STATUS.items():
        assert status.get(name) == code, (name, status)


def repo_beside_stub(tmp_path):
    """A seeded repo one level down, so a `stub_regen` directory beside it is
    not an untracked path inside it."""
    root = tmp_path / "repo"
    root.mkdir()
    return git_repo(root)


def stub_regen(tmp_path, source):
    """A scripts/ directory holding only a stand-in `trunk_step.py`."""
    stub = tmp_path / "stub-scripts"
    stub.mkdir(exist_ok=True)
    (stub / "trunk_step.py").write_text(source, encoding="utf-8", newline="\n")
    return stub


def count_writes(monkeypatch):
    """Record every entry into a step's writes: the write callback handed to the
    shared helper, the claim's link-aware move, and the mint's per-draft write
    and watermark bump. A pre-check refusal must leave the record EMPTY. The
    final tree alone cannot show that: a regression that wrote, found the clash
    and restored would leave the very same tree."""
    calls = []
    bk = integ.bookkeeping
    real_commit = bk.commit

    def commit(root, scope, write, *args, **kwargs):
        def counted(scratch):
            calls.append("write")
            return write(scratch)

        return real_commit(root, scope, counted, *args, **kwargs)

    monkeypatch.setattr(bk, "commit", commit)
    for owner, name in (
        (integ.spec_move, "move_spec"),
        (intake, "_write_draft"),
        (intake.trace, "bump_watermark"),
    ):

        def entered(*args, _real=getattr(owner, name), _name=name, **kwargs):
            calls.append(_name)
            return _real(*args, **kwargs)

        monkeypatch.setattr(owner, name, entered)
    return calls


# --- the owner's uncommitted work survives every bookkeeping outcome ----------


def test_claims_and_mints_commit_only_what_they_wrote(tmp_path, monkeypatch, capsys):
    root = trunk(tmp_path)
    setup = _rev(root, "HEAD")
    leave_owner_edits(root)
    # ONE shared helper: both callers hold the same module object, and every
    # outcome below passes through its single entry point.
    bk = integ.bookkeeping
    assert intake.bookkeeping is bk
    labels = []
    real_commit, real_scripts = bk.commit, bk.SCRIPTS

    def spy(*args, **kwargs):
        labels.append(kwargs.get("label"))
        return real_commit(*args, **kwargs)

    monkeypatch.setattr(bk, "commit", spy)
    # The write counter the refusal tests below lean on, proven wired here: a
    # counter that never counts would make their "zero writes" vacuous.
    writes = count_writes(monkeypatch)

    # 1. A successful claim commits the move and its regeneration, nothing else.
    assert integ.claim(root, "WI-401", "wi-401") == 0, capsys.readouterr().err
    assert writes == ["write", "move_spec"]
    assert (root / "docs/work/active/wi-401/WI-401-widget.md").is_file()
    assert_owner_edits_untouched(root)
    head = _rev(root, "HEAD")
    state = (root / "PROJECT_STATE.html").read_bytes()
    mark = (root / "docs/id-watermark").read_bytes()

    # 2. A refused claim: the move and a partial regeneration are written in the
    #    scratch worktree, then the regeneration fails - and none of it reaches
    #    the checkout.
    monkeypatch.setattr(bk, "SCRIPTS", stub_regen(tmp_path, FAILING_REGEN))
    assert integ.claim(root, "WI-402", "wi-402") == 1
    assert "regeneration failed" in capsys.readouterr().err
    assert (root / "docs/work/queued/WI-402-gadget.md").is_file()
    assert not (root / "docs/work/active/wi-402/WI-402-gadget.md").exists()
    assert (root / "PROJECT_STATE.html").read_bytes() == state
    assert _rev(root, "HEAD") == head and "wi-402" not in _branches(root)
    assert_owner_edits_untouched(root)

    # 3. A refused mint: the spec and the raised watermark are written in the
    #    scratch worktree, then the same regeneration fails.
    minted, refusal = intake.mint_gap_rows(root, [GAP])
    assert minted == [] and "regeneration failed" in refusal
    assert not list((root / "docs/work/queued").glob("WI-403-*.md"))
    assert (root / "docs/id-watermark").read_bytes() == mark
    assert (root / "PROJECT_STATE.html").read_bytes() == state
    assert _rev(root, "HEAD") == head
    assert_owner_edits_untouched(root)

    # 4. A successful mint - and its id is WI-403, because the refused mint's
    #    raised mark never left the scratch worktree the spec was minted in.
    monkeypatch.setattr(bk, "SCRIPTS", real_scripts)
    del writes[:]
    minted, refusal = intake.mint_gap_rows(root, [GAP])
    assert refusal is None, refusal
    assert writes == ["write", "_write_draft", "bump_watermark"]
    assert [w for w, _ in minted] == ["WI-403"]
    assert _rev(root, "HEAD") != head
    assert_owner_edits_untouched(root)

    # Absent from EVERY commit since the setup, on trunk and on the claim branch.
    touched = _git(root, "log", "--all", "--format=", "--name-only", "^" + setup)
    touched = {ln for ln in touched.splitlines() if ln.strip()}
    assert "docs/work/active/wi-401/WI-401-widget.md" in touched
    assert set(OWNER_EDITS).isdisjoint(touched), touched
    assert labels == ["the claim", "the claim", "the intake mint", "the intake mint"]
    assert _worktree_count(root) == 1  # every scratch worktree was removed


# --- a dirty path the step must write refuses by name, before any write -------


def test_a_dirty_path_the_claim_must_write_refuses_by_name(
    tmp_path, monkeypatch, capsys
):
    root = trunk(tmp_path)
    stub = stub_regen(tmp_path, RECORDING_REGEN)
    monkeypatch.setattr(integ.bookkeeping, "SCRIPTS", stub)
    hand = "# Status\n\na hand edit the regeneration would overwrite\n"
    (root / "docs/status.md").write_text(hand, encoding="utf-8", newline="\n")
    head = _rev(root, "HEAD")
    writes = count_writes(monkeypatch)

    assert integ.claim(root, "WI-401", "wi-401") == 1
    assert "docs/status.md" in capsys.readouterr().err
    assert writes == []  # refused BEFORE the write callback or the move ran
    assert (root / "docs/status.md").read_text(encoding="utf-8") == hand
    assert (root / "docs/work/queued/WI-401-widget.md").is_file()
    assert not (root / "docs/work/active/wi-401/WI-401-widget.md").exists()
    assert _rev(root, "HEAD") == head and "wi-401" not in _branches(root)
    assert not (stub / "ran").exists()  # nothing regenerated either


def test_a_dirty_path_the_mint_must_write_refuses_by_name(tmp_path, monkeypatch):
    root = trunk(tmp_path)
    stub = stub_regen(tmp_path, RECORDING_REGEN)
    monkeypatch.setattr(intake.bookkeeping, "SCRIPTS", stub)
    hand = "# Status\n\na hand edit the regeneration would overwrite\n"
    (root / "docs/status.md").write_text(hand, encoding="utf-8", newline="\n")
    mark = (root / "docs/id-watermark").read_bytes()
    head = _rev(root, "HEAD")
    writes = count_writes(monkeypatch)

    minted, refusal = intake.mint_gap_rows(root, [GAP])
    assert minted == [] and "docs/status.md" in refusal
    assert writes == []  # no draft written, no mark raised, no callback entered
    assert (root / "docs/status.md").read_text(encoding="utf-8") == hand
    assert not list((root / "docs/work/queued").glob("WI-403-*.md"))
    assert (root / "docs/id-watermark").read_bytes() == mark
    assert _rev(root, "HEAD") == head
    assert not (stub / "ran").exists()


def test_an_uncommitted_link_to_the_spec_does_not_widen_the_claim(tmp_path, capsys):
    # The claim's move is link-aware: every file linking the moved spec is
    # rewritten. The plan is HEAD's, read in the scratch worktree the move runs
    # in, so an UNCOMMITTED note that adds a link to the spec is no path the
    # claim writes: it is neither refused, rewritten nor committed, and the
    # owner's draft stays exactly as typed.
    root = trunk(tmp_path)
    note = root / "plans" / "next.md"
    note.parent.mkdir()
    text = "See [the widget](../docs/work/queued/WI-401-widget.md).\n"
    note.write_text(text, encoding="utf-8", newline="\n")
    head = _rev(root, "HEAD")

    assert integ.claim(root, "WI-401", "wi-401") == 0, capsys.readouterr().err
    assert note.read_text(encoding="utf-8") == text
    assert (root / "docs/work/active/wi-401/WI-401-widget.md").is_file()
    touched = _git(root, "diff-tree", "--name-only", "-r", head, "HEAD").split()
    assert "plans/next.md" not in touched, touched
    left = _git(root, "status", "--porcelain", "--untracked-files=all")
    assert left.splitlines() == ["?? plans/next.md"], left


def test_an_uncommitted_edit_hiding_a_committed_link_refuses_by_name(
    tmp_path, monkeypatch, capsys
):
    # The other half: a COMMITTED note links the spec, and the owner's
    # uncommitted edit removes that link. HEAD's note is one the move must
    # rewrite, so it is in the plan whatever the checkout says, and its dirty
    # copy refuses by name before anything is written - rather than the scratch
    # relinking it and the commit silently keeping HEAD's stale link.
    root = trunk(tmp_path)
    note = root / "plans" / "next.md"
    note.parent.mkdir()
    note.write_text(
        "See [the widget](../docs/work/queued/WI-401-widget.md).\n",
        encoding="utf-8",
        newline="\n",
    )
    _commit(root, "a note linking the widget", when=T_VERDICT + 1)
    head = _rev(root, "HEAD")
    hidden = "The widget note, link removed while drafting.\n"
    note.write_text(hidden, encoding="utf-8", newline="\n")
    writes = count_writes(monkeypatch)

    assert integ.claim(root, "WI-401", "wi-401") == 1
    assert "plans/next.md" in capsys.readouterr().err
    assert writes == []  # refused BEFORE the write callback or the move ran
    assert note.read_text(encoding="utf-8") == hidden
    assert (root / "docs/work/queued/WI-401-widget.md").is_file()
    assert _rev(root, "HEAD") == head and "wi-401" not in _branches(root)


# --- the step runs in a scratch worktree; the install refuses on drift -------


def _wait_for(path, worker, seconds=120):
    deadline = time.monotonic() + seconds
    while not path.exists():
        assert worker.is_alive(), "the claim ended without reaching the regeneration"
        assert time.monotonic() < deadline, "the regeneration never blocked"
        time.sleep(0.05)


def test_an_owner_edit_while_the_regeneration_is_blocked_survives_and_refuses(
    tmp_path, monkeypatch, capsys
):
    # The window the helper used to state and not close: the pre-check has
    # passed, the step is running, and the owner types into an in-scope path -
    # here the prose of docs/status.md, which the regeneration also rewrites.
    # The step and its regeneration must be running somewhere else, the edit
    # must survive byte for byte, the commit the step built must not carry it,
    # and the step must refuse by name instead of installing over it.
    root = trunk(tmp_path)
    status = root / "docs" / "status.md"
    status.write_text(STATUS_WITH_BLOCK, encoding="utf-8", newline="\n")
    _commit(root, "the status page's generated block", when=T_VERDICT + 1)
    head = _rev(root, "HEAD")
    bk = integ.bookkeeping
    real = str(bk.SCRIPTS / "trunk_step.py")
    stub = stub_regen(tmp_path, BLOCKING_REGEN.format(real=real))
    monkeypatch.setattr(bk, "SCRIPTS", stub)
    built = []
    real_object = bk._commit_object

    def spy(*args, **kwargs):
        built.append(real_object(*args, **kwargs))
        return built[-1]

    monkeypatch.setattr(bk, "_commit_object", spy)
    outcome = {}

    def run():
        try:
            outcome["rc"] = integ.claim(root, "WI-401", "wi-401")
        except BaseException as exc:  # reported below, not lost in the thread
            outcome["raised"] = exc

    worker = threading.Thread(target=run)
    worker.start()
    owner = STATUS_WITH_BLOCK + "\nan owner line, typed while the claim ran\n"
    try:
        _wait_for(stub / "blocked", worker)
        # Blocked: the step has moved the spec by now, wherever it runs.
        ran_in = Path((stub / "cwd").read_text(encoding="utf-8")).resolve()
        still_queued = (root / "docs/work/queued/WI-401-widget.md").is_file()
        moved_here = (root / "docs/work/active/wi-401").exists()
        status.write_text(owner, encoding="utf-8", newline="\n")
    finally:
        (stub / "release").write_text("", encoding="utf-8")
        worker.join(timeout=300)
    assert "raised" not in outcome, outcome
    err = capsys.readouterr().err
    assert outcome.get("rc") == 1, err
    assert "docs/status.md" in err

    # Outside the primary checkout: nothing the step wrote was visible here.
    assert ran_in != root.resolve()
    assert still_queued and not moved_here
    # The owner's edit survives, and nothing was installed or advanced.
    assert status.read_text(encoding="utf-8") == owner
    assert _rev(root, "HEAD") == head
    assert (root / "docs/work/queued/WI-401-widget.md").is_file()
    assert not (root / "docs/work/active/wi-401").exists()
    # The drift check runs after the branch cut, so the refusal leaves the
    # abandoned-claim branch the next claim re-cuts, and says so.
    assert "wi-401" in _branches(root) and "re-cuts" in err
    # The commit the step built wrote docs/status.md - and not the owner's line.
    [sha] = built
    changed = _git(root, "diff-tree", "--name-only", "-r", head, sha).split()
    assert "docs/status.md" in changed, changed
    assert "docs/work/active/wi-401/WI-401-widget.md" in changed, changed
    committed = _git(root, "show", sha + ":docs/status.md")
    assert "an owner line" not in committed
    assert "WI-402" in committed  # the regenerated block, from the step's tree
    assert _worktree_count(root) == 1  # the scratch worktree is gone


def test_an_uncommitted_generator_input_stays_out_of_the_committed_artifacts(
    tmp_path, capsys
):
    # A path OUTSIDE the claim's scope that a generator READS: another queued
    # spec, whose title the dashboard renders. The owner's uncommitted retitle
    # is not the claim's to commit, and it must not shape the artifacts the
    # claim commits either: they are derived from HEAD plus the claim's writes.
    root = trunk(tmp_path)
    spec = root / "docs/work/queued/WI-402-gadget.md"
    draft = spec.read_text(encoding="utf-8").replace(
        'title = "Gadget"', 'title = "Gadget OwnerDraftRetitle"'
    )
    assert "OwnerDraftRetitle" in draft
    spec.write_text(draft, encoding="utf-8", newline="\n")

    assert integ.claim(root, "WI-401", "wi-401") == 0, capsys.readouterr().err
    committed = _git(root, "show", "HEAD:PROJECT_STATE.html")
    assert "Gadget" in committed  # the committed title is rendered...
    assert "OwnerDraftRetitle" not in committed  # ...and the draft is not
    assert spec.read_text(encoding="utf-8") == draft
    # Everything the claim wrote is installed as committed; the draft stays.
    left = _git(root, "status", "--porcelain").splitlines()
    assert left == [" M docs/work/queued/WI-402-gadget.md"], left


# --- a step that raises leaves the checkout untouched, and says so ----------


def test_a_raising_step_leaves_the_checkout_untouched_and_says_so(tmp_path):
    root = git_repo(tmp_path)
    bk = integ.bookkeeping
    seen = []

    def write(scratch):
        seen.append(Path(scratch))
        (scratch / "made.txt").write_text("the step's write\n", encoding="utf-8")
        (scratch / "seed.txt").write_text("overwritten\n", encoding="utf-8")
        raise RuntimeError("the step crashed")

    with pytest.raises(RuntimeError, match="the step crashed") as caught:
        bk.commit(root, ["made.txt", "seed.txt"], write, "unused", label="the step")
    notes = "\n".join(getattr(caught.value, "__notes__", []))
    assert "the step raised; the step wrote nothing in the checkout" in notes
    [scratch] = seen
    assert scratch.resolve() != root.resolve()
    assert not scratch.exists()  # removed on the way out, crash or not
    assert not (root / "made.txt").exists()
    assert (root / "seed.txt").read_text(encoding="utf-8") == "seed\n"
    assert _git(root, "status", "--porcelain").strip() == ""
    assert _worktree_count(root) == 1


def test_a_scratch_worktree_that_will_not_remove_is_named(
    tmp_path, monkeypatch, capsys
):
    # The removal fails the way a file another process holds open fails on
    # Windows. The crash still reaches the operator as the exception, and the
    # residue the removal could not clear is named with the command that does.
    root = git_repo(tmp_path)
    bk = integ.bookkeeping
    real_git = bk._git

    def held(where, *args, **kwargs):
        if args[:2] == ("worktree", "remove"):
            return 1, "error: failed to delete: Permission denied"
        return real_git(where, *args, **kwargs)

    monkeypatch.setattr(bk, "_git", held)
    seen = []

    def write(scratch):
        seen.append(Path(scratch))
        raise RuntimeError("the step crashed")

    with pytest.raises(RuntimeError, match="the step crashed"):
        bk.commit(root, ["made.txt"], write, "unused", label="the test step")
    err = capsys.readouterr().err
    [scratch] = seen
    try:
        assert "the test step's scratch worktree" in err and "would not remove" in err
        assert str(scratch) in err and "Permission denied" in err
        assert scratch.is_dir()  # the residue the warning names
    finally:
        real_git(root, "worktree", "remove", "--force", str(scratch))
    assert _worktree_count(root) == 1


# --- trunk moving under the step refuses before anything is installed -------


def test_a_trunk_that_moved_while_the_step_ran_refuses_before_installing(
    tmp_path, monkeypatch
):
    root = repo_beside_stub(tmp_path)
    bk = integ.bookkeeping
    monkeypatch.setattr(bk, "SCRIPTS", stub_regen(tmp_path, RECORDING_REGEN))

    def write(scratch):
        (scratch / "made.txt").write_text("the step's file\n", encoding="utf-8")
        # ...while, in the checkout, the owner commits something else.
        (root / "other.txt").write_text("the owner's commit\n", encoding="utf-8")
        _commit(root, "the owner commits while the step runs", when=T_VERDICT)

    sha, refusal = bk.commit(root, ["made.txt"], write, "unused", label="the step")
    assert sha is None and "trunk moved" in refusal, refusal
    assert "the step wrote nothing in the checkout" in refusal
    assert not (root / "made.txt").exists()
    subject = _git(root, "log", "-1", "--format=%s").strip()
    assert subject == "the owner commits while the step runs"


def test_the_drift_check_runs_after_before_advance(tmp_path, monkeypatch):
    # `before_advance` is the caller's, and nothing bounds what it does. An
    # in-scope edit landing while it runs must still be named and left: the
    # drift check is the LAST thing before the install, after the callback.
    root = repo_beside_stub(tmp_path)
    head = _rev(root, "HEAD")
    bk = integ.bookkeeping
    monkeypatch.setattr(bk, "SCRIPTS", stub_regen(tmp_path, RECORDING_REGEN))
    owner = "the owner's edit, made while before_advance ran\n"

    def write(scratch):
        (scratch / "seed.txt").write_text("the step's edit\n", encoding="utf-8")

    def before_advance(sha):
        (root / "seed.txt").write_text(owner, encoding="utf-8", newline="\n")

    sha, refusal = bk.commit(
        root,
        ["seed.txt"],
        write,
        "unused",
        label="the step",
        before_advance=before_advance,
    )
    assert sha is None and "seed.txt" in refusal, refusal
    assert "the step wrote nothing in the checkout" in refusal
    assert (root / "seed.txt").read_text(encoding="utf-8") == owner
    assert _rev(root, "HEAD") == head


def test_a_drift_after_the_branch_cut_leaves_a_claim_the_next_one_re_cuts(
    tmp_path, monkeypatch, capsys
):
    # Through the claim: the edit lands while the branch is being cut. The
    # claim refuses naming the path and installs nothing; the branch it cut
    # holds a claim trunk never took, the abandoned-claim shape, and the next
    # claim re-cuts it once the owner has set the edit aside.
    root = trunk(tmp_path)
    head = _rev(root, "HEAD")
    status = root / "docs" / "status.md"
    bk = integ.bookkeeping
    real_commit = bk.commit
    owner = "# Status\n\nan owner line, typed during the branch cut\n"

    def commit(*args, before_advance=None, **kwargs):
        def racing(sha):
            refusal = before_advance(sha)
            status.write_text(owner, encoding="utf-8", newline="\n")
            return refusal

        return real_commit(*args, before_advance=racing, **kwargs)

    monkeypatch.setattr(bk, "commit", commit)
    assert integ.claim(root, "WI-401", "wi-401") == 1
    err = capsys.readouterr().err
    assert "docs/status.md" in err and "wi-401" in err, err
    assert status.read_text(encoding="utf-8") == owner
    assert _rev(root, "HEAD") == head
    assert (root / "docs/work/queued/WI-401-widget.md").is_file()
    assert "wi-401" in _branches(root)  # the cut branch, never taken by trunk

    monkeypatch.setattr(bk, "commit", real_commit)
    _git(root, "checkout", "--", "docs/status.md")
    assert integ.claim(root, "WI-401", "wi-401") == 0, capsys.readouterr().err
    assert (root / "docs/work/active/wi-401/WI-401-widget.md").is_file()
    assert _rev(root, "wi-401") == _rev(root, "HEAD")


# --- the regeneration runs the kit as HEAD commits it ------------------------


def test_the_regeneration_runs_the_committed_kit_not_an_uncommitted_edit(
    tmp_path, monkeypatch
):
    # The kit lives inside the repository (as in every adopter), so its scripts
    # are committed code like any generator input: the regeneration runs the
    # scratch tree's committed copy, and an uncommitted edit to it in the
    # checkout neither runs nor shapes the commit. That holds for its write
    # table too: the loaded table here drops the committed kit's output (an
    # uncommitted REGEN_STEPS edit), and the caller does not name it, so only
    # the committed table can put it in scope.
    root = repo_beside_stub(tmp_path)
    kit = root / "kit"
    kit.mkdir()
    committed = (
        "import pathlib\n"
        "def regen_writes():\n"
        "    return ['regen.txt']\n"
        "if __name__ == '__main__':\n"
        "    pathlib.Path('regen.txt').write_text('committed kit', encoding='utf-8')\n"
    )
    (kit / "trunk_step.py").write_text(committed, encoding="utf-8", newline="\n")
    _commit(root, "the kit", when=T_VERDICT)
    edited = "import sys\nsys.exit('the uncommitted kit ran')\n"
    (kit / "trunk_step.py").write_text(edited, encoding="utf-8", newline="\n")
    bk = integ.bookkeeping
    monkeypatch.setattr(bk, "SCRIPTS", kit)
    monkeypatch.setattr(bk.trunk_step, "regen_writes", lambda: [])

    def write(scratch):
        (scratch / "made.txt").write_text("the step's file\n", encoding="utf-8")

    sha, refusal = bk.commit(root, ["made.txt"], write, "the step", label="the step")
    assert refusal is None, refusal
    assert _git(root, "show", sha + ":regen.txt").strip() == "committed kit"
    assert (kit / "trunk_step.py").read_text(encoding="utf-8") == edited


# --- a refusal inside the install restores it and leaves an edit made there --


def test_a_refusal_inside_the_install_restores_it_and_leaves_an_edit_made_there(
    tmp_path, monkeypatch
):
    # The one window left: the install's own few git calls. The commit's paths
    # are in the checkout when the owner edits an in-scope path, and then trunk
    # refuses to advance (a compare-and-swap lost to a trunk that moved). The
    # owner's line must SURVIVE and be named, while everything the install
    # wrote is restored. docs/status.md is a path the regeneration writes (its
    # status splice); here the step's own `write` stands in for that splice,
    # because the fixture carries no generated-status markers.
    root = repo_beside_stub(tmp_path)
    status = root / "docs" / "status.md"
    status.write_text("# Status\n", encoding="utf-8", newline="\n")
    _commit(root, "status", when=T_VERDICT)
    head = _rev(root, "HEAD")
    bk = integ.bookkeeping
    monkeypatch.setattr(bk, "SCRIPTS", stub_regen(tmp_path, RECORDING_REGEN))
    real_git = bk._git

    def racing(where, *args, **kwargs):
        if args[:1] == ("update-ref",):
            with status.open("a", encoding="utf-8", newline="\n") as fh:
                fh.write("an owner line\n")
            # ...and an in-scope path the install never wrote at all.
            (root / "PROJECT_STATE.html").write_text("owner draft\n", encoding="utf-8")
            return 1, "fatal: cannot lock ref 'HEAD': is at another commit"
        return real_git(where, *args, **kwargs)

    monkeypatch.setattr(bk, "_git", racing)

    def write(scratch):
        spliced = "# Status\n\nspliced\n"
        (scratch / "docs/status.md").write_text(spliced, encoding="utf-8", newline="\n")
        (scratch / "made.txt").write_text("the step's file\n", encoding="utf-8")
        (scratch / "seed.txt").write_text("the step's edit\n", encoding="utf-8")
        return None

    sha, refusal = bk.commit(
        root, ["made.txt", "seed.txt"], write, "unused", label="the step"
    )
    assert sha is None and "trunk did not advance" in refusal, refusal
    assert "LEFT" in refusal
    assert "docs/status.md" in refusal and "PROJECT_STATE.html" in refusal
    assert status.read_text(encoding="utf-8") == "# Status\n\nspliced\nan owner line\n"
    assert (root / "PROJECT_STATE.html").read_text(encoding="utf-8") == "owner draft\n"
    assert not (root / "made.txt").exists()
    assert (root / "seed.txt").read_text(encoding="utf-8") == "seed\n"
    assert _rev(root, "HEAD") == head
    left = sorted(_git(root, "status", "--porcelain").splitlines())
    assert left == [" M docs/status.md", "?? PROJECT_STATE.html"], left


# --- no whole-tree git write survives on a bookkeeping path -------------------

# (subcommand, flag) pairs that act on the WHOLE tree; `None` = any use at all.
WHOLE_TREE = {("add", "-A"), ("reset", "--hard"), ("clean", None)}
# The claim's functions in integrate.py. The module's refresh and unload paths
# reset LANE worktrees the loop owns, which is why the scan is scoped to these.
CLAIM_PATH = {"claim", "_claim_locked", "_claim_refusal", "_drop_abandoned"}


def _whole_tree_git_calls(path, only=None):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    scopes = (
        [tree]
        if only is None
        else [
            n
            for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name in only
        ]
    )
    hits = set()
    for scope in scopes:
        for call in ast.walk(scope):
            if not isinstance(call, ast.Call):
                continue
            words = [
                a.value
                for a in call.args
                if isinstance(a, ast.Constant) and isinstance(a.value, str)
            ]
            for sub, flag in WHOLE_TREE:
                if sub in words and (flag is None or flag in words):
                    hits.add(
                        "{}:{} git {} {}".format(path.name, call.lineno, sub, flag)
                    )
    return sorted(hits)


def test_no_bookkeeping_path_keeps_a_whole_tree_git_write():
    hits = (
        _whole_tree_git_calls(SCRIPTS / "bookkeeping.py")
        + _whole_tree_git_calls(SCRIPTS / "intake.py")
        + _whole_tree_git_calls(SCRIPTS / "integrate.py", only=CLAIM_PATH)
    )
    assert hits == []


# --- the owner-only scratchpad does not stop the merge slot -------------------


def test_the_merge_slot_reads_past_a_dirty_owner_scratchpad(tmp_path):
    root = trunk(tmp_path)
    pad = root / integ.ac.OWNER_ONLY_PATHS[0]
    pad.write_text("owner notes\n", encoding="utf-8", newline="\n")
    _commit(root, "the owner's scratchpad", when=T_VERDICT + 1)
    pad.write_text("owner notes, mid-edit\n", encoding="utf-8", newline="\n")

    proc = run_py([SCRIPTS / "integrate.py", "--root", ".", "integrate"], cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "dirty" not in proc.stderr
    assert pad.read_text(encoding="utf-8") == "owner notes, mid-edit\n"
