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
    written - a hand-edited `docs/status.md` under regeneration, and an
    uncommitted note the claim's link-aware move would have to rewrite - and
    "before anything is written" is proven by counting the step's write entry
    points, not inferred from the final tree;
  * a step that RAISES is restored, and a restore that fails is named on the
    exception instead of leaving silent residue;
  * an owner edit landing on an in-scope path AFTER the step wrote it is left
    in place and named when the helper then refuses, while the step's own
    writes are restored;
  * no bookkeeping path in the primary checkout keeps a whole-tree git write;
  * the owner-only scratchpad no longer stops the merge slot (the dispatcher's
    own tick-top check is pinned beside its siblings in tests/test_dispatch.py).

The helper is reached THROUGH its two callers (`integ.bookkeeping`, never a
second `load_script` copy), because the claim of the design is that both
callers share one module object - a private copy would test something neither
caller runs.
"""

import ast

import pytest
from conftest import SCRIPTS, env_gate_skipif, load_script, run_py
from integrate_fixtures import (
    T_VERDICT,
    _branches,
    _commit,
    _git,
    _rev,
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
        def counted():
            calls.append("write")
            return write()

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

    # 2. A refused claim: the move and a partial regeneration are written, then
    #    the regeneration fails - and only those writes are undone.
    monkeypatch.setattr(bk, "SCRIPTS", stub_regen(tmp_path, FAILING_REGEN))
    assert integ.claim(root, "WI-402", "wi-402") == 1
    assert "regeneration failed" in capsys.readouterr().err
    assert (root / "docs/work/queued/WI-402-gadget.md").is_file()
    assert not (root / "docs/work/active/wi-402/WI-402-gadget.md").exists()
    assert (root / "PROJECT_STATE.html").read_bytes() == state
    assert _rev(root, "HEAD") == head and "wi-402" not in _branches(root)
    assert_owner_edits_untouched(root)

    # 3. A refused mint: the spec and the raised watermark are written, then the
    #    same regeneration fails.
    minted, refusal = intake.mint_gap_rows(root, [GAP])
    assert minted == [] and "regeneration failed" in refusal
    assert not list((root / "docs/work/queued").glob("WI-403-*.md"))
    assert (root / "docs/id-watermark").read_bytes() == mark
    assert (root / "PROJECT_STATE.html").read_bytes() == state
    assert _rev(root, "HEAD") == head
    assert_owner_edits_untouched(root)

    # 4. A successful mint - and its id is WI-403, because the refused mint's
    #    raised mark was restored with the spec it was minted for.
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


def test_an_uncommitted_note_the_move_must_relink_refuses_by_name(
    tmp_path, monkeypatch, capsys
):
    # The claim's move is link-aware: every file linking the moved spec is
    # rewritten. An UNCOMMITTED note that links it is a path the claim must
    # write, so it is named before the move rather than rewritten and swept in.
    root = trunk(tmp_path)
    note = root / "plans" / "next.md"
    note.parent.mkdir()
    text = "See [the widget](../docs/work/queued/WI-401-widget.md).\n"
    note.write_text(text, encoding="utf-8", newline="\n")
    writes = count_writes(monkeypatch)

    assert integ.claim(root, "WI-401", "wi-401") == 1
    assert "plans/next.md" in capsys.readouterr().err
    assert writes == []
    assert note.read_text(encoding="utf-8") == text
    assert (root / "docs/work/queued/WI-401-widget.md").is_file()
    assert "wi-401" not in _branches(root)


# --- a step that raises is restored, and a failed restore is named ----------


def test_a_raising_step_carries_its_failed_restore_on_the_exception(
    tmp_path, monkeypatch
):
    # The step writes a file and then crashes; the restore's unlink of that file
    # then fails the way a file another process holds open fails on Windows.
    # Both have to reach the operator: the crash as the exception, and the
    # residue the restore could not remove as a note riding it.
    root = git_repo(tmp_path)
    bk = integ.bookkeeping
    real_unlink = bk.Path.unlink

    def held(self, *args, **kwargs):
        if self.name == "held.txt":
            raise PermissionError("held.txt is open in another process")
        return real_unlink(self, *args, **kwargs)

    def write():
        (root / "held.txt").write_text("the step's write\n", encoding="utf-8")
        monkeypatch.setattr(bk.Path, "unlink", held)
        raise RuntimeError("the step crashed")

    with pytest.raises(RuntimeError, match="the step crashed") as caught:
        bk.commit(root, ["held.txt"], write, "unused", label="the test step")
    notes = "\n".join(getattr(caught.value, "__notes__", []))
    assert "the test step raised" in notes
    assert "restore FAILED" in notes
    assert "held.txt" in notes and "open in another process" in notes
    assert (root / "held.txt").is_file()  # the residue the note names


def test_a_raising_step_is_restored_and_says_so(tmp_path):
    root = git_repo(tmp_path)
    bk = integ.bookkeeping

    def write():
        (root / "made.txt").write_text("the step's write\n", encoding="utf-8")
        (root / "seed.txt").write_text("overwritten\n", encoding="utf-8")
        raise RuntimeError("the step crashed")

    with pytest.raises(RuntimeError, match="the step crashed") as caught:
        bk.commit(root, ["made.txt", "seed.txt"], write, "unused", label="the step")
    notes = "\n".join(getattr(caught.value, "__notes__", []))
    assert "the step restored the paths it wrote and nothing else" in notes
    assert not (root / "made.txt").exists()
    assert (root / "seed.txt").read_text(encoding="utf-8") == "seed\n"
    assert _git(root, "status", "--porcelain").strip() == ""


# --- an owner edit landing after the step wrote survives a refusal ----------


def test_an_edit_after_the_step_wrote_is_left_and_named_on_a_refusal(tmp_path):
    # The declared window: the pre-check has passed and the step has written,
    # and the owner then edits an in-scope path before the helper finishes. On
    # the refusal that follows, the owner's line must SURVIVE and be named,
    # while every write the step itself made is restored. docs/status.md is a
    # path the regeneration writes (its status splice); here the step's own
    # `write` stands in for that splice, because the fixture carries no
    # generated-status markers for the real generator to find.
    root = git_repo(tmp_path)
    status = root / "docs" / "status.md"
    status.write_text("# Status\n", encoding="utf-8", newline="\n")
    _commit(root, "status", when=T_VERDICT)
    head = _rev(root, "HEAD")
    bk = integ.bookkeeping

    def write():
        status.write_text("# Status\n\nspliced\n", encoding="utf-8", newline="\n")
        (root / "made.txt").write_text("the step's file\n", encoding="utf-8")
        (root / "seed.txt").write_text("the step's edit\n", encoding="utf-8")
        return None

    def before_advance(_sha):
        with status.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write("an owner line\n")
        # ...and an in-scope path the step never wrote at all.
        (root / "PROJECT_STATE.html").write_text("owner draft\n", encoding="utf-8")
        return "the branch cut failed"

    sha, refusal = bk.commit(
        root,
        ["made.txt", "seed.txt"],
        write,
        "unused",
        label="the step",
        before_advance=before_advance,
    )
    assert sha is None and "the branch cut failed" in refusal
    assert "docs/status.md" in refusal and "PROJECT_STATE.html" in refusal
    assert "an owner line" in status.read_text(encoding="utf-8")
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
