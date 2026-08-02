"""handback.py — the two lane closes that are not a merge (WI-387, §A3).

The invariant under test is "every lane ends in a merge, branches never hang",
and the only honest way to test it is to CONSTRUCT the topology: real temp git
repos, a real claim, a real lane worktree, real commits. What each group pins:

  * the RETURN is a real registry move — the spec is back in `queued/`, the
    branch is FINISHED by the integrator's own read, and `branch_outcomes`
    reads `handback` off the same move;
  * the returned spec LEAVES THE READY FRONTIER (queued + blockref = blocked).
    That is not decoration: without it the driver would claim, hand back and
    re-claim the same WI forever, so the anti-livelock property is asserted
    against `schedule.frontier` itself rather than against the blockref cell;
  * every registry reader still parses a returned spec. The `## Handback`
    section widened a body grammar that four copies enforce, so all four are
    driven over one returned file — the drift this repo closes by test rather
    than by extraction (WI-291);
  * the QUARANTINE is bar-inert AND lossless: the product paths go back to the
    base byte for byte, the `.patch` re-applies, and the bookkeeping the
    handback just wrote survives untouched.

Mutation notes are inline where a green could be vacuous — a revert that
reverted nothing, or a "blocked" assertion that would pass on an unblocked row.
"""

import shutil
import subprocess

from conftest import env_gate_skipif, load_script, skip_without_env_gates

pytestmark = env_gate_skipif("git")

hb = load_script("handback")
integ = hb.integrate
sched = load_script("schedule")
ctraj = load_script("check_trajectory")
acommon = load_script("agent_common")
wi_convert = load_script("wi_convert")

T_BASE = 1_000_000
T_CODE = 1_000_100


def _git(root, *args, check=True):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if check:
        assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _commit(root, message, when=T_CODE):
    import os

    env = dict(os.environ)
    env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = "@{} +0000".format(when)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True, env=env)
    subprocess.run(
        ["git", "-C", str(root), "commit", "-qm", message], check=True, env=env
    )


def spec_text(wid, specref="seed.txt", deliverable=""):
    lines = [
        'id = "{}"'.format(wid),
        'title = "Widget"',
        'workstream = "ws"',
        'sr_refs = ["SR-001"]',
        "needs = []",
        'safety_class = "ordinary"',
        "order = 0",
        'specref = "{}"'.format(specref),
    ]
    text = "+++\n" + "".join(ln + "\n" for ln in lines) + "+++\n"
    if deliverable:
        text += "\n## Deliverable\n\n" + deliverable + "\n"
    return text


def claimed_repo(tmp_path, wid="WI-401", branch="wi-401", extra=()):
    """A trunk with `wid` CLAIMED onto `branch` — the state a lane closes from.

    `extra` is `[(path, text)]` seeded BEFORE the claim, so a test that needs a
    file to rename has one at the base the quarantine reverts to."""
    skip_without_env_gates("git")
    root = tmp_path / "repo"
    root.mkdir()
    _git(root.parent, "init", "-q", str(root))
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    (root / "seed.txt").write_text("seed\n", encoding="utf-8", newline="\n")
    (root / ".gitignore").write_text("out/\n", encoding="utf-8", newline="\n")
    spec = root / "docs" / "work" / "queued" / "{}-widget.md".format(wid)
    spec.parent.mkdir(parents=True, exist_ok=True)
    spec.write_text(spec_text(wid), encoding="utf-8", newline="\n")
    for name, text in extra:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")
    _commit(root, "seed + file " + wid, when=T_BASE)
    assert integ.claim(root, wid, branch) == 0
    return root


def lane(root, branch="wi-401"):
    wt, err = integ.lane_worktree(root, branch)
    assert err is None, err
    return wt


def returned_spec_path(root, wid="WI-401"):
    return root / "docs" / "work" / "queued" / "{}-widget.md".format(wid)


def merge_branch(root, branch="wi-401"):
    """Land the branch on trunk the way the slot would — without the bar, which
    is `integrate`'s own suite's subject. Lets a test read the RETURNED spec on
    trunk, which is where the invariant says it has to end up."""
    _git(root, "merge", "--no-ff", "-q", "-m", "integrate: merge " + branch, branch)


# --- the return itself ---------------------------------------------------------


def test_handback_returns_the_spec_to_queued_and_finishes_the_branch(tmp_path):
    root = claimed_repo(tmp_path)
    wt = lane(root)
    (wt / "half-done.py").write_text("VALUE = 1\n", encoding="utf-8", newline="\n")

    ids, refusal = hb.hand_back(root, "wi-401", "worker exit 7 (NEEDS-HUMAN)")
    assert refusal is None, refusal
    assert ids == ["WI-401"]

    # The branch is now FINISHED by the integrator's own read — the same move
    # that returns the spec is the one that closes the lane, so there is no
    # second fact to keep in agreement.
    assert integ.finished_branches(root) == ["wi-401"]
    outcomes, unresolved = integ.branch_outcomes(root, "wi-401")
    assert outcomes == {"WI-401": "handback"} and unresolved == []

    # ...and the work so far is COMMITTED, not discarded: the lane worktree is
    # clean and the file is in the branch's tree.
    assert wt.joinpath("half-done.py").is_file()
    assert "half-done.py" in _git(root, "ls-tree", "-r", "--name-only", "wi-401")
    assert _git(wt, "status", "--porcelain").strip() == ""

    merge_branch(root)
    spec = returned_spec_path(root).read_text(encoding="utf-8")
    assert "## Handback" in spec
    assert 'blockref = "docs/work/queued/WI-401-widget.md"' in spec
    assert "worker exit 7 (NEEDS-HUMAN)" in spec
    assert not list((root / "docs" / "work" / "active").rglob("WI-*.md"))


def test_the_returned_spec_leaves_the_ready_frontier(tmp_path):
    # THE ANTI-LIVELOCK PROPERTY, asserted where it actually bites. A handback
    # puts the WI back in `queued/`, which is the ready state — so if the
    # blockref did not take, the driver would claim, hand back and re-claim the
    # same WI forever, moving trunk each time and never tripping the stall
    # guard. Driven both ways: ready before the claim, BLOCKED after the return.
    root = claimed_repo(tmp_path)

    _git(root, "checkout", "-q", "-b", "probe", "HEAD~1")
    ready = [r["id"] for r in sched.frontier(sched._load(root))]
    assert ready == ["WI-401"], ready
    _git(root, "checkout", "-q", "main")

    lane(root)
    _ids, refusal = hb.hand_back(root, "wi-401", "worker exit 7")
    assert refusal is None, refusal
    merge_branch(root)

    records = {r["id"]: r for r in sched.evaluate(sched._load(root))}
    assert records["WI-401"]["status"] == "queued"
    assert records["WI-401"]["disposition"] == "blocked"
    assert [r["id"] for r in sched.frontier(sched._load(root))] == []


def test_every_registry_reader_parses_a_returned_spec(tmp_path):
    # The `## Handback` section widened a body grammar FOUR copies enforce
    # (agent_common, check_trajectory, schedule per the F5 rule, plus the
    # converter). A returned spec that one reader accepted and another called
    # malformed would split the registry in half — schedule would see a blocked
    # row the validator had dropped — so all four are driven over one real file.
    root = claimed_repo(tmp_path)
    lane(root)
    assert hb.hand_back(root, "wi-401", "worker exit 7")[1] is None
    merge_branch(root)
    text = returned_spec_path(root).read_text(encoding="utf-8")
    rel = "queued/WI-401-widget.md"

    for reader in (acommon, ctraj, sched):
        row, _order = reader.parse_spec_row(text, rel)
        assert row["Status"] == "queued", reader.__name__
        assert row["Deliverable"] == "", reader.__name__
        assert row["BlockRef"] == "docs/work/queued/WI-401-widget.md", reader.__name__
    row, _order = wi_convert.parse_spec(text, rel)
    assert row["Status"] == "queued" and row["Deliverable"] == ""


def test_the_return_move_runs_the_link_aware_ritual(tmp_path):
    """WI-393: the return is the same indivisible move+relink the claim and the
    archival run (WI-288/WI-353, rehomed in spec_move.py). queued/ is one
    directory SHALLOWER than active/<branch>/, so a returned spec's own links
    must shorten, and every inbound link written against the active path must
    follow it back — in the same handback commit, never as residue."""
    # The link sits in the Deliverable section: the registry loaders drop a
    # spec whose body prose lives under no recognised heading.
    body = spec_text("WI-401", deliverable="See [the log](../../log.md).")
    root = claimed_repo(
        tmp_path,
        extra=(
            ("docs/work/queued/WI-401-widget.md", body),
            (
                "docs/log.md",
                "# Log\n\nplanned: [WI-401](work/queued/WI-401-widget.md)\n",
            ),
        ),
    )
    # The claim already ran the ritual: the spec's own link is one deeper and
    # the inbound link follows it — the premise the return move must invert.
    claimed = root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md"
    assert "[the log](../../../log.md)" in claimed.read_text(encoding="utf-8")
    assert "work/active/wi-401" in (root / "docs" / "log.md").read_text(
        encoding="utf-8"
    )

    wt = lane(root)
    # A fragment written during the lane's life links the ACTIVE spec path —
    # the inbound shape the return would otherwise strand.
    frag = wt / "docs" / "log.d" / "WI-401-notes.md"
    frag.parent.mkdir(parents=True, exist_ok=True)
    frag.write_text(
        "## note\n\nspec: [WI-401](../work/active/wi-401/WI-401-widget.md)\n",
        encoding="utf-8",
        newline="\n",
    )

    ids, refusal = hb.hand_back(root, "wi-401", "worker exit 7")
    assert refusal is None, refusal
    assert ids == ["WI-401"]

    returned = (wt / "docs" / "work" / "queued" / "WI-401-widget.md").read_text(
        encoding="utf-8"
    )
    assert "[the log](../../log.md)" in returned, returned
    assert "../../../log.md" not in returned
    for doc in (wt / "docs" / "log.md", wt / "docs" / "log.d" / "WI-401-notes.md"):
        text = doc.read_text(encoding="utf-8")
        assert "work/active/wi-401" not in text, (doc, text)
        assert "work/queued/WI-401-widget.md" in text, (doc, text)
    # the relinks are IN the handback commit, not left dirty in the lane
    assert _git(wt, "status", "--porcelain").strip() == ""


def test_a_returned_spec_keeps_a_deliverable_that_was_already_there(tmp_path):
    # The grammar is Deliverable-then-Handback, not either/or: a spec carrying
    # both must still yield its cell verbatim. Without the ordering rule the
    # partition would swallow the Deliverable, which no reader would report —
    # it would simply go blank.
    note = hb._note("wi-401", "worker exit 7", "aaaaaaaaaa..bbbbbbbbbb")
    text = hb.returned_spec(
        spec_text("WI-401", deliverable="A widget, half-shipped."),
        "docs/work/queued/WI-401-widget.md",
        note,
    )
    assert text.index("## Deliverable") < text.index("## Handback")
    row, _order = acommon.parse_spec_row(text, "queued/WI-401-widget.md")
    assert row["Deliverable"] == "A widget, half-shipped."


def test_a_spec_that_already_declares_a_blockref_keeps_its_own(tmp_path):
    text = spec_text("WI-401").replace(
        'specref = "seed.txt"', 'specref = "seed.txt"\nblockref = "docs/ratify/OI-9.md"'
    )
    out = hb.returned_spec(text, "docs/work/queued/WI-401-widget.md", "\n## Handback\n")
    assert 'blockref = "docs/ratify/OI-9.md"' in out
    assert out.count("blockref") == 1


def test_handback_refuses_a_branch_trunk_holds_no_claim_for(tmp_path):
    root = claimed_repo(tmp_path)
    ids, refusal = hb.hand_back(root, "wi-999", "worker exit 7")
    assert ids is None and "no claimed specs" in refusal


def test_a_disposition_rows_own_handback_is_refused_structurally(tmp_path):
    # WI-388 / ruling R3, the no-recursion invariant at the MACHINERY end: a
    # disposition row (the adjudication kind) may never itself hand back — its
    # only outcomes are cancel / defer / re-queue with drafted follow-up /
    # surface an open item. The refusal is structural (the function that would
    # perform the act refuses), never prose, and it leaves the claim exactly
    # where it was for a human to read.
    root = claimed_repo(tmp_path)
    spec = root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md"
    spec.write_text(
        spec.read_text(encoding="utf-8").replace(
            'safety_class = "ordinary"', 'safety_class = "adjudication"'
        ),
        encoding="utf-8",
        newline="\n",
    )
    _commit(root, "fixture: the claim is an adjudication row", when=T_CODE)

    ids, refusal = hb.hand_back(root, "wi-401", "worker exit 7 (NEEDS-HUMAN)")
    assert ids is None
    assert "never hands back" in refusal and "R3" in refusal
    assert spec.is_file()  # the claim did not move
    assert not (root / "docs" / "work" / "queued" / "WI-401-widget.md").exists()


# --- the quarantine (the RULED red arm) ---------------------------------------


def quarantined_repo(tmp_path):
    """A claimed lane that built REAL product changes — one edit, one new file,
    one deletion — so the revert has all three cases to get right."""
    root = claimed_repo(tmp_path)
    wt = lane(root)
    (wt / "seed.txt").write_text("edited\n", encoding="utf-8", newline="\n")
    (wt / "added.py").write_text("BROKEN = (\n", encoding="utf-8", newline="\n")
    (wt / ".gitignore").unlink()
    _commit(wt, "WI-401: half a widget")
    assert hb.hand_back(root, "wi-401", "worker exit 7")[1] is None
    return root, wt


def test_quarantine_reverts_the_product_and_keeps_the_failing_diff(tmp_path):
    root, wt = quarantined_repo(tmp_path)

    assert hb.quarantine(root, "wi-401", "bar exit 1") is None

    # Bar-inert: every product path is back to what the base had, in all THREE
    # diff shapes the lane produced. A revert that only handled modifications
    # would leave added.py — the unparseable file — right where the bar looks,
    # and a revert that ignored deletions would leave .gitignore missing.
    assert (wt / "seed.txt").read_text(encoding="utf-8") == "seed\n"
    assert not (wt / "added.py").exists()
    assert (wt / ".gitignore").read_text(encoding="utf-8") == "out/\n"
    tree = _git(root, "ls-tree", "-r", "--name-only", "wi-401").split()
    assert "added.py" not in tree and ".gitignore" in tree

    # Lossless: the failing diff rides along as a `.patch`, and it really is a
    # patch — git itself re-applies it. The quarantined tip IS the tree the
    # diff was taken against, so applying it here restores the lane's work
    # exactly, which is the property a future WI depends on.
    patch = wt / "docs" / "work" / "handback" / "wi-401.patch"
    assert patch.is_file()
    assert "docs/work/handback/wi-401.patch" in tree
    _git(wt, "apply", "--check", str(patch))
    _git(wt, "apply", str(patch))
    assert (wt / "added.py").read_text(encoding="utf-8") == "BROKEN = (\n"
    assert (wt / "seed.txt").read_text(encoding="utf-8") == "edited\n"
    assert not (wt / ".gitignore").exists()


def test_the_name_status_stream_is_read_as_records_not_pairs():
    # THE PARSE ITSELF, on the exact field list REVIEW-A round 1 drove. Read two
    # at a time this pairs as ('R100','Aold.py'), ('Anew.py','D'), … — paths in
    # the status slot, the bookkeeping filter blind, and `z_broken.py` (the
    # failing file) past the loop bound. A rename is THREE fields, and
    # `diff.renames` has defaulted true since Git 2.9, so this is ordinary
    # output rather than an exotic case.
    fields = [
        "R100",
        "Aold.py",
        "Anew.py",
        "D",
        "docs/work/active/wi-401/WI-401-widget.md",
        "A",
        "docs/work/queued/WI-401-widget.md",
        "M",
        "z_broken.py",
    ]
    assert hb.diff_records(fields) == [
        ("R100", ["Aold.py", "Anew.py"]),
        ("D", ["docs/work/active/wi-401/WI-401-widget.md"]),
        ("A", ["docs/work/queued/WI-401-widget.md"]),
        ("M", ["z_broken.py"]),
    ]
    # A copy is the other three-field form.
    assert hb.diff_records(["C75", "src/a.py", "src/b.py"]) == [
        ("C75", ["src/a.py", "src/b.py"])
    ]
    # A stream that ends mid-record is a TRUNCATED READ, not an empty diff:
    # None, so the caller refuses rather than quarantining a partial list.
    assert hb.diff_records(["R100", "Aold.py"]) is None
    assert hb.diff_records(["M"]) is None


def test_quarantine_reverts_a_rename_and_keeps_the_failing_file(tmp_path):
    # The end-to-end half of the same defect, in the DAMAGING alignment: the
    # rename sorts first (capital A before `docs/`) and the broken file sorts
    # last, so under the pair-parse `z_broken.py` was dropped entirely and the
    # run reported "4 path(s) reverted" over a branch still holding it.
    root = claimed_repo(tmp_path, extra=[("Aold.py", "OLD = 1\n")])
    wt = lane(root)
    _git(wt, "mv", "Aold.py", "Anew.py")
    (wt / "z_broken.py").write_text("VALUE = (\n", encoding="utf-8", newline="\n")
    _commit(wt, "WI-401: rename a module and break a file")
    assert hb.hand_back(root, "wi-401", "worker exit 7")[1] is None

    assert hb.quarantine(root, "wi-401", "bar exit 1") is None

    tree = _git(root, "ls-tree", "-r", "--name-only", "wi-401").split()
    # The rename is undone in BOTH directions...
    assert "Aold.py" in tree and "Anew.py" not in tree
    assert (wt / "Aold.py").read_text(encoding="utf-8") == "OLD = 1\n"
    assert not (wt / "Anew.py").exists()
    # ...and the failing file is really gone, not merely uncounted.
    assert "z_broken.py" not in tree and not (wt / "z_broken.py").exists()
    # The record keeps both, which is the other half of what the mis-parse lost.
    patch = (wt / "docs" / "work" / "handback" / "wi-401.patch").read_text(
        encoding="utf-8"
    )
    assert "z_broken.py" in patch and "Anew.py" in patch


def test_a_failed_revert_step_refuses_and_restores_rather_than_reporting(
    tmp_path, monkeypatch
):
    # The discarded return codes. Under the mis-parse four git calls were
    # no-match failures and every one was thrown away, which is why a wrong
    # revert printed a confident count. Fault-injected on the LAST revert step
    # so earlier ones have already run: the refusal names the path, and the
    # lane goes back to its tip instead of being left half-reverted.
    root, wt = quarantined_repo(tmp_path)
    real_git = hb.ac.git

    def flaky(cwd, *args):
        if args[:1] == ("checkout",) and args[-1] == "seed.txt":
            return 1, "fatal: simulated pathspec failure"
        return real_git(cwd, *args)

    monkeypatch.setattr(hb.ac, "git", flaky)
    refusal = hb.quarantine(root, "wi-401", "bar exit 1")
    monkeypatch.undo()

    assert refusal is not None
    assert "FAILED on seed.txt" in refusal and "nothing was quarantined" in refusal
    # Restored: the earlier `git rm` of added.py is undone, no artefact was
    # written into the tree, and the branch tip did not move.
    assert (wt / "added.py").is_file()
    assert not (wt / "docs" / "work" / "handback").exists()
    assert "quarantine" not in _git(root, "log", "-1", "--format=%s", "wi-401")


def test_quarantine_leaves_the_handback_bookkeeping_alone(tmp_path):
    # The spec move and the log fragments ARE the record being kept: reverting
    # them would revert the handback itself and put the WI back in `active/`
    # with no lane — the exact stranded shape this design abolishes.
    root, wt = quarantined_repo(tmp_path)
    fragment = wt / "docs" / "log.d" / "WI-401-widget.md"
    fragment.parent.mkdir(parents=True, exist_ok=True)
    fragment.write_text(
        "## 2026-08-01 — half a widget\n", encoding="utf-8", newline="\n"
    )
    _commit(wt, "log: WI-401 fragment")

    assert hb.quarantine(root, "wi-401", "bar exit 1") is None
    assert (wt / "docs" / "work" / "queued" / "WI-401-widget.md").is_file()
    assert fragment.is_file()
    assert integ.branch_outcomes(root, "wi-401")[0] == {"WI-401": "handback"}


def test_quarantine_refuses_when_the_red_is_not_the_lanes_own_code(tmp_path):
    # A lane that changed nothing outside the bookkeeping surfaces cannot have
    # caused the red, so there is nothing to revert and reverting nothing would
    # only buy a second identical bar run. It says so instead.
    root = claimed_repo(tmp_path)
    lane(root)
    assert hb.hand_back(root, "wi-401", "worker exit 7")[1] is None

    refusal = hb.quarantine(root, "wi-401", "bar exit 1")
    assert refusal is not None
    assert "nothing outside the bookkeeping surfaces" in refusal


def test_the_git_dependency_is_declared_for_this_module():
    # This suite drives real repositories end to end; without git on PATH every
    # test above would SKIP and the module would still print a green. The
    # declared gate (conftest.ENV_GATES) is what makes that skip COUNTED in the
    # terminal summary rather than invisible (WI-326).
    assert shutil.which("git"), "the module-level env gate should have skipped"
