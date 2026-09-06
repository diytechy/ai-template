"""integrate.py — the CLAIM rung, and the refusals that stand in front of it.

One of four modules `WI-521` slice 2 carved out of the 3,520-line
`test_integrate.py` monolith (M-06); the family and the rule for what is shared
are in `tests/integrate_fixtures.py`. This module owns the first act of the
station protocol and nothing else.

**Claim** (§2.3 steps 1+2) is the serial trunk move `queued/ ->
active/<branch>/` plus the branch cut from that commit, and the refusals that
stand in front of it: the tracked pause (§5.6), a dirty trunk, a branch that
already exists, a branch name that would not map to a flat claim directory,
(WI-370) a spec whose `SpecRef` is empty or does not resolve in-repo — the R-E
debt that becomes unpayable once the closing branch exists, hoisted the same way
R-D was — a WI that is not on the scheduler's ready frontier, and (WI-358) a
claimed id named in hand-authored `docs/status.md` prose, the forward-only debt
that would red R-D on the composed tree at close, hoisted to where a single
trunk commit can still pay it.

Two harder things ride with it, because both are about telling a real claim from
something that merely looks like one:

  * **the link-aware move ritual and its forgeries.** A crashed claim leaves an
    orphan branch the next claim re-cuts — but only if the branch really is an
    abandoned claim. The EOL fixtures here forge line endings and assert on the
    BYTES `git cat-file` gives back (WI-403), which is why
    `integrate_fixtures.git_repo` pins `core.autocrlf`: on an unpinned Windows
    box the forged CRLF never reaches git at all and the convicting tests would
    pass vacuously (WI-337).
  * **finished-branch detection** — the closing commit's move to `complete/` IS
    the finished signal: no state file, no ref, just the tree.

`integrate()` itself is only ever run as a SUBPROCESS here: it takes the
process-global coordinator lock fd (`agent_common.acquire_lock`), so calling it
in-process would leak a held descriptor into the rest of the suite. The
in-process tests call the pure-ish helpers, which take no lock.
"""

import shutil

import pytest
from conftest import SCRIPTS, env_gate_skipif, load_script, run_py
from integrate_fixtures import (
    T_CODE,
    T_VERDICT,
    _branches,
    _commit,
    _git,
    _rev,
    claim_repo,
    declare_generated,
    git_repo,
    integ,
    write_spec,
)

pytestmark = env_gate_skipif("git")

spec_move = load_script("spec_move")


def claim_dir(root, branch, wid="WI-999"):
    """A claim the Phase 2c way (§2.1/§2.3): the work item's spec sits in
    docs/work/active/<branch>/. The directory IS the claim."""
    path = write_spec(root, "active/" + branch, wid, slug="ghost")
    return path.parent


# --- 1. claim: the refusals in front of the trunk move ------------------------


def test_claim_refuses_while_the_tracked_pause_is_present(tmp_path, capsys):
    # §5.6: pause = STOP CLAIMING. The refusal quotes the declaration's own
    # reason and stamp, because a pause a human cannot attribute is a pause a
    # human deletes. Nothing moves and no branch is cut — the whole point is
    # that a paused repo drains rather than accumulating fresh claims.
    root = claim_repo(tmp_path)
    (root / "docs" / "work" / "pause").write_text(
        'reason = "spine WI in flight"\nsince = "2026-07-29"\n',
        encoding="utf-8",
        newline="\n",
    )
    _commit(root, "pause: spine barrier", when=T_VERDICT)

    assert integ.claim(root, "WI-401", "wi-401") == 1
    err = capsys.readouterr().err
    assert "docs/work/pause is present" in err
    assert "spine WI in flight" in err and "2026-07-29" in err
    assert (root / "docs" / "work" / "queued" / "WI-401-widget.md").is_file()
    assert not (root / "docs" / "work" / "active").exists()
    assert "wi-401" not in _branches(root)


def test_claim_refuses_a_dirty_trunk(tmp_path, capsys):
    # A claim is a clean serial commit: claiming on a dirty trunk would sweep
    # whatever a human left lying around into the bookkeeping commit.
    root = claim_repo(tmp_path)
    (root / "scratch.txt").write_text("uncommitted\n", encoding="utf-8")

    assert integ.claim(root, "WI-401", "wi-401") == 1
    assert "working tree is dirty" in capsys.readouterr().err
    assert (root / "docs" / "work" / "queued" / "WI-401-widget.md").is_file()
    assert "wi-401" not in _branches(root)


def test_claim_refuses_when_the_branch_already_exists(tmp_path, capsys):
    # An existing branch means someone is already there (or a previous claim
    # never finished). Reusing it would cut a second claim from a tree that is
    # not the trunk's HEAD.
    root = claim_repo(tmp_path)
    _git(root, "branch", "wi-401")

    assert integ.claim(root, "WI-401", "wi-401") == 1
    assert "branch wi-401 already exists" in capsys.readouterr().err
    assert (root / "docs" / "work" / "queued" / "WI-401-widget.md").is_file()


@pytest.mark.parametrize("branch", ["feat/wi-401", "wi..401", "wi\\401"])
def test_claim_refuses_a_branch_name_that_is_not_a_flat_claim_dir(
    tmp_path, capsys, branch
):
    # The queue maps a branch to docs/work/active/<branch>/ as ONE directory
    # segment. A '/' would nest it (and check.py's own lane detector reads the
    # nested form), '..' would traverse out of the claim tree entirely — so the
    # queue refuses the names it cannot represent instead of guessing.
    root = claim_repo(tmp_path)

    assert integ.claim(root, "WI-401", branch) == 1
    assert "does not map to a flat claim directory" in capsys.readouterr().err
    assert (root / "docs" / "work" / "queued" / "WI-401-widget.md").is_file()
    assert not (root / "docs" / "work" / "active").exists()


def test_a_spine_claim_succeeds_on_an_idle_station(tmp_path):
    # QUESTION B RULED (WI-381, docs/concurrency-v2.md §A4.1): admission is the
    # DISPATCHER's scheduling decision, so `_claim_refusal`'s blunt
    # `safety_class != ordinary` arm is DELETED — a hard stop replaced by a
    # wait. A hand claim of a spine WI on an IDLE station works (useful, and
    # attended-serial per RULING-8); what keeps mid-flight authority safe is
    # the dispatch-lock constraint below, not a class refusal here.
    root = claim_repo(tmp_path, safety="spine")

    assert integ.claim(root, "WI-401", "wi-401") == 0
    assert (root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md").is_file()
    assert "wi-401" in _branches(root)


def test_a_hand_claim_during_live_lanes_is_unrepresentable(tmp_path, capsys):
    # §A4.1's authority hole, closed by a CONSTRAINT rather than a re-added
    # refusal: `integrate claim` is a hand-runnable CLI, and the claim now
    # REQUIRES the dispatch lock — the same out/agent-loop.lock a live
    # dispatcher holds for its whole process lifetime. While lanes are live
    # the lock cannot be taken, so the hand-claim-mid-flight STATE cannot be
    # written at all; on an idle station every other claim test in this file
    # is the proof it still works.
    root = claim_repo(tmp_path)
    (root / ".gitignore").write_text("out/\n", encoding="utf-8", newline="\n")
    _commit(root, "ignore the lock home", when=T_VERDICT)
    lock = integ.ac.dispatch_lock_path(root)
    assert integ.ac.acquire_lock(lock) is None  # stand in for the dispatcher
    try:
        assert integ.claim(root, "WI-401", "wi-401") == 1
        err = capsys.readouterr().err
        assert "the dispatch lock" in err and "unrepresentable" in err
        assert (root / "docs" / "work" / "queued" / "WI-401-widget.md").is_file()
        assert "wi-401" not in _branches(root)
        # The one caller that already holds the lock IS the dispatcher: its
        # in-process claim says so and proceeds.
        assert integ.claim(root, "WI-401", "wi-401", dispatch_lock_held=True) == 0
    finally:
        integ.ac.release_lock()


def test_a_spine_batch_claims_as_one_commit(tmp_path):
    # §A4 (WI-381): ALL spine WIs admit together — one branch, ONE claim
    # commit moving every batched spec into active/<branch>/, so N spine
    # changes cost one re-attest window and one owner sitting rather than N.
    root = git_repo(tmp_path)
    write_spec(
        root, "queued", "WI-501", slug="alpha", safety="spine", specref="seed.txt"
    )
    write_spec(
        root, "queued", "WI-502", slug="beta", safety="spine", specref="seed.txt"
    )
    declare_generated(root)
    _commit(root, "file the spine batch", when=T_CODE)

    assert integ.claim(root, ["WI-501", "WI-502"], "wi-501-alpha") == 0
    active = root / "docs" / "work" / "active" / "wi-501-alpha"
    assert (active / "WI-501-alpha.md").is_file()
    assert (active / "WI-502-beta.md").is_file()
    subject = _git(root, "log", "-1", "--format=%s").strip()
    assert subject == "claim: WI-501;WI-502 -> active/wi-501-alpha (bookkeeping)"
    assert integ._claimed_wi_ids(root, "wi-501-alpha") == ["WI-501", "WI-502"]


def test_claim_refuses_a_spec_without_a_specref(tmp_path, capsys):
    # WI-370: an open WI without a SpecRef reds R-E under --strict on every
    # composed tree that sees it, and the debt is unpayable once the closing
    # branch exists — so the claim is where it must be caught.
    root = claim_repo(tmp_path, specref=None)
    assert integ.claim(root, "WI-401", "wi-401") == 1
    err = capsys.readouterr().err
    assert "carries no SpecRef" in err and "WI-370" in err
    assert (root / "docs" / "work" / "queued" / "WI-401-widget.md").is_file()
    assert "wi-401" not in _branches(root)


def test_claim_refuses_a_specref_that_does_not_resolve(tmp_path, capsys):
    # R-E's own resolution rule at claim time: the path part must exist.
    root = claim_repo(tmp_path, specref="docs/ghost-spec.md")
    assert integ.claim(root, "WI-401", "wi-401") == 1
    err = capsys.readouterr().err
    assert "does not resolve to an in-repo FILE" in err
    assert "docs/ghost-spec.md" in err
    assert "wi-401" not in _branches(root)


def test_claim_refuses_a_bare_fragment_specref(tmp_path, capsys):
    # 131-REVIEW-A's R-E shape: "#anchor" has no path part. `root / ""` is the
    # repo root, which exists — the round-1 rung passed it and R-E then redded
    # the composed tree (WI-370-REVIEW-A finding 1).
    root = claim_repo(tmp_path, specref="#improvement-plan")
    assert integ.claim(root, "WI-401", "wi-401") == 1
    err = capsys.readouterr().err
    assert "has no path part" in err
    assert "wi-401" not in _branches(root)


def test_claim_refuses_a_directory_specref(tmp_path, capsys):
    # R-E's other path-half shape: a directory is not a document. `.exists()`
    # accepted it; the rung must hold `.is_file()`, the same bar R-E holds.
    root = claim_repo(tmp_path, specref="docs")
    assert integ.claim(root, "WI-401", "wi-401") == 1
    err = capsys.readouterr().err
    assert "does not resolve to an in-repo FILE" in err
    assert "wi-401" not in _branches(root)


def test_a_specref_anchor_resolves_by_its_path_part(tmp_path, capsys):
    # `path#anchor` is legal R-E form; the rung checks the PATH part only
    # (anchor resolution stays check_trajectory's job). The claim proceeds all
    # the way through, proving the rung sits quietly in the passing path.
    root = claim_repo(tmp_path, specref="seed.txt#section")
    (root / ".gitignore").write_text("out/\n", encoding="utf-8", newline="\n")
    _commit(root, "chore: ignore the coordinator lock", when=T_CODE)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    assert "wi-401" in _branches(root)


def test_claim_refuses_a_wi_that_is_not_on_the_ready_frontier(tmp_path, capsys):
    # Readiness is DERIVED by schedule.py from the registry, never asserted by
    # the claimer: WI-401 hard-needs WI-999, which is still queued, so WI-401 is
    # `waiting` and claiming it would start work against an unbuilt dependency.
    root = git_repo(tmp_path)
    write_spec(tmp_path, "queued", "WI-401", needs=["WI-999"], specref="seed.txt")
    write_spec(tmp_path, "queued", "WI-999", slug="dependency", order=1)
    _commit(root, "file the dependent pair", when=T_CODE)

    assert integ.claim(root, "WI-401", "wi-401") == 1
    assert "not on the ready frontier" in capsys.readouterr().err
    assert (root / "docs" / "work" / "queued" / "WI-401-widget.md").is_file()
    assert "wi-401" not in _branches(root)


def test_claim_moves_the_spec_commits_the_trunk_and_cuts_the_branch(tmp_path, capsys):
    # The green path, and the shape the rest of the queue depends on: ONE
    # bookkeeping commit that moves the spec, and a branch cut FROM that commit
    # (§2.3 steps 1+2) — so the claim is atomic in history and the branch's own
    # first parent is the claim.
    root = claim_repo(tmp_path)

    assert integ.claim(root, "WI-401", "wi-401") == 0
    assert "claimed WI-401 on wi-401" in capsys.readouterr().out

    assert (root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md").is_file()
    assert not (root / "docs" / "work" / "queued" / "WI-401-widget.md").exists()
    tracked = _git(root, "ls-tree", "-r", "--name-only", "HEAD").split()
    assert "docs/work/active/wi-401/WI-401-widget.md" in tracked
    assert "docs/work/queued/WI-401-widget.md" not in tracked
    # The move is COMMITTED, not merely staged: a claim that left a dirty trunk
    # would refuse the next claim (and the queue) on its own residue.
    assert _git(root, "status", "--porcelain").strip() == ""
    assert (
        _git(root, "log", "-1", "--format=%s").strip()
        == "claim: WI-401 -> active/wi-401 (bookkeeping)"
    )
    assert _rev(root, "wi-401") == _rev(root, "HEAD")
    lane, refusal = integ.lane_worktree(root, "wi-401")
    assert refusal is None, refusal
    assert integ.ac.claim_base(lane) == (_rev(root, "wi-401"), True)


def test_claim_runs_the_link_aware_move_ritual(tmp_path):
    """WI-393: the claim's move IS the indivisible ritual (WI-288/WI-353,
    rehomed in spec_move.py). Driven 2026-08-01: a claim's bare `git mv` broke
    the backlog plan's inbound row links, and WI-391 REVIEW-A measured a bare
    move reproducing both halves of the defect. The move, the inbound redirect
    and the outbound rebase land in the ONE claim commit, so no two-thirds
    state can reach trunk."""
    root = claim_repo(tmp_path)
    spec = root / "docs" / "work" / "queued" / "WI-401-widget.md"
    spec.write_text(
        spec.read_text(encoding="utf-8") + "\nSee [the seed](../../../seed.txt).\n",
        encoding="utf-8",
        newline="\n",
    )
    (root / "docs" / "log.md").write_text(
        "planned: [WI-401](work/queued/WI-401-widget.md#deliverable)\n",
        encoding="utf-8",
        newline="\n",
    )
    _commit(root, "link the queued spec", when=T_CODE)

    assert integ.claim(root, "WI-401", "wi-401") == 0

    claimed = root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md"
    text = claimed.read_text(encoding="utf-8")
    # the moved spec's OWN link resolves from one directory deeper (WI-353)
    assert "](../../../../seed.txt)" in text
    # the inbound link follows the move, text untouched, fragment carried (WI-288)
    log = (root / "docs" / "log.md").read_text(encoding="utf-8")
    assert "[WI-401](work/active/wi-401/WI-401-widget.md#deliverable)" in log
    # both rewrites are IN the claim commit — a claim may not leave a dirty trunk
    assert _git(root, "status", "--porcelain").strip() == ""


def crashed_claim(root, wi="WI-401", branch="wi-401"):
    """The state a crash inside the INVERTED claim leaves (WI-387, §A3): the
    branch exists on a claim commit, and trunk never moved onto it.

    Reproduced by claiming for real and then rewinding trunk alone, which is
    exactly what a process killed between `git branch` and the trunk advance
    would have left — the branch ref is durable, the trunk advance is not."""
    assert integ.claim(root, wi, branch) == 0
    _git(root, "reset", "--hard", "HEAD~1")
    return root


def test_a_crashed_claim_leaves_an_orphan_branch_the_next_claim_re_cuts(tmp_path):
    # THE WHOLE POINT OF THE INVERSION. Trunk-first left a claim no lane could
    # reach and cost an exit-2 refusal plus hand repair; branch-first leaves a
    # branch whose claim commit trunk never took, with the WI still queued — a
    # shape the claim resolves by itself.
    root = claim_repo(tmp_path)
    crashed_claim(root)

    # The benign shape, stated as the three facts that define it.
    assert "wi-401" in _branches(root)
    assert (root / "docs" / "work" / "queued" / "WI-401-widget.md").is_file()
    assert integ._abandoned_claim(root, "WI-401", "wi-401")

    assert integ.claim(root, "WI-401", "wi-401") == 0
    assert (root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md").is_file()
    assert _rev(root, "wi-401") == _rev(root, "HEAD")


def test_a_crashed_claim_that_relinked_docs_is_still_re_cut(tmp_path):
    """WI-393 x WI-387: the claim commit now carries the relink writes, so the
    conviction's content fact must recognise them as the claim's OWN — an
    M-status markdown path whose new content is EXACTLY the redirect this claim
    would make. Without that clause the ritual would break the crashed-claim
    re-cut, and a crash between `git branch` and the trunk advance would be
    back to hand repair."""
    root = claim_repo(tmp_path)
    (root / "docs" / "log.md").write_text(
        "planned: [WI-401](work/queued/WI-401-widget.md)\n",
        encoding="utf-8",
        newline="\n",
    )
    _commit(root, "link the queued spec", when=T_CODE)
    crashed_claim(root)

    # trunk rewound: the spec is back in queued/ and the log links it there
    assert (root / "docs" / "work" / "queued" / "WI-401-widget.md").is_file()
    assert "work/queued" in (root / "docs" / "log.md").read_text(encoding="utf-8")

    assert integ._abandoned_claim(root, "WI-401", "wi-401")
    assert integ.claim(root, "WI-401", "wi-401") == 0
    assert _rev(root, "wi-401") == _rev(root, "HEAD")


def test_an_md_edit_that_is_not_the_relink_still_convicts(tmp_path):
    """The narrowing that keeps the new clause honest: an .md modification the
    relink oracle cannot reproduce byte-for-byte is somebody's WORK, and the
    branch holding it is a collision, never an abandoned claim to delete."""
    root = claim_repo(tmp_path)
    (root / "docs" / "log.md").write_text(
        "planned: [WI-401](work/queued/WI-401-widget.md)\n",
        encoding="utf-8",
        newline="\n",
    )
    _commit(root, "link the queued spec", when=T_CODE)
    # Forge the exact claim shape — subject, spec move, one commit past trunk —
    # PLUS a log edit that is not the redirect the claim would have written.
    _git(root, "checkout", "-q", "-b", "wi-401")
    (root / "docs" / "work" / "active" / "wi-401").mkdir(parents=True)
    _git(
        root,
        "mv",
        "docs/work/queued/WI-401-widget.md",
        "docs/work/active/wi-401/WI-401-widget.md",
    )
    (root / "docs" / "log.md").write_text(
        "rewritten by hand - hours of prose, no link left\n",
        encoding="utf-8",
        newline="\n",
    )
    _commit(root, integ._claim_subject("WI-401", "wi-401"), when=T_VERDICT)
    _git(root, "checkout", "-q", "main")

    assert not integ._abandoned_claim(root, "WI-401", "wi-401")


def forged_relink_claim(root, mangle, wi="WI-401", branch="wi-401"):
    """A claim-shaped commit whose relink writes are GENUINE, with `mangle`
    applied to the relinked log afterwards — WI-393 REVIEW-A finding 1's drive
    recipe: exact `_claim_subject`, a real `spec_move.move_spec` move pair, one
    commit past trunk. Every fact `_abandoned_claim` checks holds except what
    `mangle` changed, so the relinked file's BYTES are the only thing left to
    convict on — a fixture built any looser cannot fail if the compare
    loosens."""
    _git(root, "checkout", "-q", "-b", branch)
    touched, refusal = spec_move.move_spec(
        root,
        "docs/work/queued/{}-widget.md".format(wi),
        "docs/work/active/{}/{}-widget.md".format(branch, wi),
    )
    assert refusal is None and "docs/log.md" in (touched or [])
    mangle(root / "docs" / "log.md")
    _commit(root, integ._claim_subject(wi, branch), when=T_VERDICT)
    _git(root, "checkout", "-q", "main")


def linked_log_repo(
    tmp_path, log_bytes=b"planned: [WI-401](work/queued/WI-401-widget.md)\n"
):
    """A claim_repo whose docs/log.md links the queued spec with EXACT bytes,
    so the claim's relink genuinely touches it and a byte-level mangle has a
    deterministic before-state."""
    root = claim_repo(tmp_path)
    (root / "docs" / "log.md").write_bytes(log_bytes)
    _commit(root, "link the queued spec", when=T_CODE)
    return root


def test_a_trailing_newline_only_hand_edit_in_a_claim_shape_convicts(tmp_path):
    """WI-403 (WI-393 REVIEW-A finding 1, driven excused 2026-08-01):
    `_relinked_exactly` read both sides through `ac.git`, whose text-mode
    success path `.strip()`s — so a hand edit consisting only of APPENDED BLANK
    LINES on a relinked doc compared equal to the ritual's own write and the
    branch carrying it was deleted. The oracle's reads are raw blob bytes now;
    an EOL-margin edit is somebody's work like any other byte."""
    root = linked_log_repo(tmp_path)
    forged_relink_claim(root, lambda log: log.write_bytes(log.read_bytes() + b"\n\n"))

    assert not integ._abandoned_claim(root, "WI-401", "wi-401")


def test_a_whole_file_crlf_relay_in_a_claim_shape_convicts(tmp_path):
    """WI-403 (WI-393 REVIEW-A finding 1, driven excused 2026-08-01): the
    text-mode read's universal-newlines decode folded `\\r\\n` to `\\n` on BOTH
    sides of the compare, so a whole-file CRLF relay of a relinked doc rode
    through as "relink-identical". This repo treats line endings as
    load-bearing (WI-234/WI-337 — spec_move itself preserves them via
    `newline=""`), so a relay is a real content change the oracle must see."""
    root = linked_log_repo(tmp_path)
    forged_relink_claim(
        root, lambda log: log.write_bytes(log.read_bytes().replace(b"\n", b"\r\n"))
    )

    assert not integ._abandoned_claim(root, "WI-401", "wi-401")


def test_one_extra_mid_file_byte_still_convicts(tmp_path):
    """The conviction the oracle always had (REVIEW-A's `one-extra-md-byte`
    drive returned False on the text-mode read too), pinned at the byte level
    so the raw-read rewrite cannot have loosened it: one byte in the MIDDLE of
    a relinked doc — where no strip or EOL fold could ever hide it — is
    somebody's work."""
    root = linked_log_repo(tmp_path)

    def one_extra_mid_file_byte(log):
        data = log.read_bytes()
        mid = len(data) // 2
        log.write_bytes(data[:mid] + b"x" + data[mid:])

    forged_relink_claim(root, one_extra_mid_file_byte)

    assert not integ._abandoned_claim(root, "WI-401", "wi-401")


def test_a_crashed_claim_that_relinked_a_crlf_doc_is_still_excused(tmp_path):
    """The fairness the text-mode decode bought by ACCIDENT — folding EOLs so a
    CRLF checkout compared equal — kept honestly by the raw read: spec_move
    preserves a CRLF doc's line endings (`newline=""`), so the genuine relink
    of a CRLF doc matches byte-for-byte and the crashed claim is still excused,
    not refused, on a CRLF checkout."""
    root = linked_log_repo(
        tmp_path, log_bytes=b"planned: [WI-401](work/queued/WI-401-widget.md)\r\n"
    )
    crashed_claim(root)

    assert integ._abandoned_claim(root, "WI-401", "wi-401")


def test_a_relinked_doc_the_ritual_would_have_skipped_convicts(tmp_path):
    """`_rewrite_md_links` SKIPS a non-UTF-8 file, so an .md modification whose
    parent content does not decode cannot be the ritual's own write — the raw
    read convicts it outright instead of comparing replacement-mangled text."""
    root = linked_log_repo(
        tmp_path,
        log_bytes=b"planned: [WI-401](work/queued/WI-401-widget.md) \xff\n",
    )

    def hand_edit_the_skipped_file(log):
        log.write_bytes(log.read_bytes() + b"an edit\n")

    _git(root, "checkout", "-q", "-b", "wi-401")
    touched, refusal = spec_move.move_spec(
        root,
        "docs/work/queued/WI-401-widget.md",
        "docs/work/active/wi-401/WI-401-widget.md",
    )
    # the ritual itself skipped the undecodable log — the forge hand-edits it
    assert refusal is None and "docs/log.md" not in (touched or [])
    hand_edit_the_skipped_file(root / "docs" / "log.md")
    _commit(root, integ._claim_subject("WI-401", "wi-401"), when=T_VERDICT)
    _git(root, "checkout", "-q", "main")

    assert not integ._abandoned_claim(root, "WI-401", "wi-401")


def forged_branch(root, subject, files, branch="wi-401"):
    """A ONE-COMMIT branch cut from trunk's tip with `subject` and `files`.

    The shape every `_abandoned_claim` negative below needs: its parent IS
    trunk's HEAD and it is not an ancestor of trunk, so the two ancestry facts
    both hold and ONLY the subject and the content can reject it. A negative
    built any other way cannot fail if the matcher loosens."""
    _git(root, "checkout", "-q", "-b", branch)
    for name, text in files:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")
    _commit(root, subject, when=T_VERDICT)
    _git(root, "checkout", "-q", "main")


def test_a_one_commit_branch_carrying_work_is_never_read_as_abandoned(tmp_path, capsys):
    # THE CONTENT FACT. "Its parent is an ancestor of trunk, so no work was
    # built on it" does not follow — a parent on trunk proves only ONE commit
    # ahead, and that commit can carry anything. Here the subject is the claim
    # subject EXACTLY, both ancestry facts hold, and the only thing left to
    # convict on is what the commit touches. REVIEW-A round 1 drove this branch
    # being deleted with its work on it.
    root = claim_repo(tmp_path)
    forged_branch(
        root,
        integ._claim_subject("WI-401", "wi-401"),
        [("real-work.txt", "hours of it\n")],
    )

    assert not integ._abandoned_claim(root, "WI-401", "wi-401")
    assert integ.claim(root, "WI-401", "wi-401") == 1
    assert "branch wi-401 already exists" in capsys.readouterr().err
    assert "real-work.txt" in _git(root, "ls-tree", "-r", "--name-only", "wi-401")


def test_a_subject_that_merely_ENDS_like_a_claim_is_not_a_claim(tmp_path, capsys):
    # THE EXACT-SUBJECT FACT, ISOLATED. `_claim_subject` exists so the writer
    # and this reader agree exactly; the reader used to test only
    # `endswith("-> active/<branch> (bookkeeping)")`, which this hand-written
    # subject satisfies. The commit touches ONLY a bookkeeping surface, so the
    # content fact and both ancestry facts pass and the subject is the only
    # thing left that can reject it — which is what makes this the test a suffix
    # matcher fails. (A draft spec is still somebody's work to lose.)
    root = claim_repo(tmp_path)
    forged_branch(
        root,
        "wip: nearly done -> active/wi-401 (bookkeeping)",
        [("docs/work/draft/WI-777-idea.md", '+++\nid = "WI-777"\n+++\n')],
    )

    assert not integ._abandoned_claim(root, "WI-401", "wi-401")
    assert integ.claim(root, "WI-401", "wi-401") == 1
    assert "already exists" in capsys.readouterr().err
    assert "WI-777-idea.md" in _git(root, "ls-tree", "-r", "--name-only", "wi-401")


def test_a_genuine_claim_subject_for_a_DIFFERENT_id_is_not_this_claim(tmp_path, capsys):
    # The id half of the exact match — and why `_abandoned_claim` has to be
    # PASSED the wi_id rather than inferring it from the branch name alone.
    # Bookkeeping-only again, so the id is the only discriminator left.
    root = claim_repo(tmp_path)
    forged_branch(
        root,
        integ._claim_subject("WI-999", "wi-401"),
        [("docs/log.d/WI-999-note.md", "## 2026-08-01 - someone's fragment\n")],
    )

    assert not integ._abandoned_claim(root, "WI-401", "wi-401")
    assert integ.claim(root, "WI-401", "wi-401") == 1
    assert "already exists" in capsys.readouterr().err
    assert "WI-999-note.md" in _git(root, "ls-tree", "-r", "--name-only", "wi-401")


def test_a_bookkeeping_only_branch_is_still_not_a_claim(tmp_path, capsys):
    # ROUND 2: "touches only bookkeeping surfaces" was still too wide. Each of
    # these carries the EXACT claim subject and only bookkeeping paths, so the
    # first three facts hold — and each is somebody's work to lose. The rule is
    # now what the claim actually WRITES: this WI's spec move into
    # active/<branch>/, plus declared generated artifacts, nothing else.
    for name, text in (
        ("docs/log.d/WI-401-hours.md", "## 2026-08-01 - an afternoon\n"),
        ("docs/log.md", "# Log\n\nA hand rewrite.\n"),
        ("docs/work/queued/WI-777-other.md", '+++\nid = "WI-777"\n+++\n'),
    ):
        home = tmp_path / name.replace("/", "_").replace(".", "_")
        home.mkdir()
        root = claim_repo(home)
        forged_branch(root, integ._claim_subject("WI-401", "wi-401"), [(name, text)])

        assert not integ._abandoned_claim(root, "WI-401", "wi-401"), name
        assert integ.claim(root, "WI-401", "wi-401") == 1, name
        assert "already exists" in capsys.readouterr().err
        tree = _git(root, "ls-tree", "-r", "--name-only", "wi-401")
        assert name in tree, name


def test_a_regeneration_that_moved_no_spec_is_not_a_claim(tmp_path, capsys):
    # The positive half of the same rule: the spec move is REQUIRED, so a
    # commit that only rewrote a declared generated artifact — which every
    # allowed path test would pass — still is not a claim commit.
    root = claim_repo(tmp_path)
    forged_branch(
        root,
        integ._claim_subject("WI-401", "wi-401"),
        [("PROJECT_STATE.html", "<html>regenerated by hand</html>\n")],
    )

    assert not integ._abandoned_claim(root, "WI-401", "wi-401")
    assert integ.claim(root, "WI-401", "wi-401") == 1
    assert "already exists" in capsys.readouterr().err


def test_a_held_abandoned_branch_refuses_by_name_instead_of_claiming_success(
    tmp_path, capsys
):
    # `git branch -D` refuses a branch a worktree has checked out. Announcing a
    # deletion that did not happen is the reports-success-on-failure shape that
    # hid the rename mis-parse next door, so the code is read and the HOLDER is
    # named — the operator's actual next move.
    home = tmp_path / "repo"
    home.mkdir()
    root = claim_repo(home)
    crashed_claim(root)
    # OUTSIDE the repo: a lane worktree under it would be untracked dirt and
    # the clean-trunk rung would refuse first, testing nothing.
    held = tmp_path / "lane"
    _git(root, "worktree", "add", "-q", str(held), "wi-401")

    assert integ._abandoned_claim(root, "WI-401", "wi-401")
    assert integ.claim(root, "WI-401", "wi-401") == 1
    captured = capsys.readouterr()
    assert "will not delete" in captured.err and str(held) in captured.err
    assert "deleted the abandoned claim branch" not in captured.out
    # Fails closed: the branch survives and the spec is still claimable.
    assert "wi-401" in _branches(root)
    assert (root / "docs" / "work" / "queued" / "WI-401-widget.md").is_file()
    assert _git(root, "status", "--porcelain").strip() == ""


def test_the_re_claim_names_the_sha_it_deleted(tmp_path, capsys):
    # A deletion the operator cannot reach by reflog is a deletion they cannot
    # audit, so the orphan's sha and the restore command are printed.
    root = claim_repo(tmp_path)
    crashed_claim(root)
    orphan = _rev(root, "wi-401")

    assert integ.claim(root, "WI-401", "wi-401") == 0
    out = capsys.readouterr().out
    assert "deleted the abandoned claim branch wi-401" in out
    assert orphan[:10] in out and "git branch wi-401 {}".format(orphan[:10]) in out


def test_a_branch_carrying_work_is_a_collision_the_claim_still_refuses(
    tmp_path, capsys
):
    # The re-claim deletes a branch, so it has to recognise the abandoned shape
    # EXACTLY. A branch of the same name carrying anything of its own — here a
    # commit on top of the claim, which is what a resumed lane looks like — is
    # a real collision and must still refuse rather than be deleted.
    root = claim_repo(tmp_path)
    crashed_claim(root)
    _git(root, "checkout", "-q", "wi-401")
    (root / "half-done.txt").write_text("1\n", encoding="utf-8", newline="\n")
    _commit(root, "WI-401: half a widget", when=T_VERDICT)
    _git(root, "checkout", "-q", "main")

    assert not integ._abandoned_claim(root, "WI-401", "wi-401")
    assert integ.claim(root, "WI-401", "wi-401") == 1
    assert "branch wi-401 already exists" in capsys.readouterr().err
    assert "half-done.txt" in _git(root, "ls-tree", "-r", "--name-only", "wi-401")


def test_an_unrelated_branch_of_the_same_name_is_never_deleted(tmp_path, capsys):
    # The other half of the same guard: a hand-made branch that merely collides
    # on the name carries no claim subject at all, so it fails the shape test on
    # its first condition and survives untouched.
    root = claim_repo(tmp_path)
    _git(root, "branch", "wi-401")

    assert not integ._abandoned_claim(root, "WI-401", "wi-401")
    assert integ.claim(root, "WI-401", "wi-401") == 1
    assert "already exists" in capsys.readouterr().err
    assert "wi-401" in _branches(root)


# --- 1b. claim: the status.md forward-only debt (WI-358) ----------------------


def write_status(root, text, when=T_VERDICT):
    path = root / "docs" / "status.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    _commit(root, "status: the working surface", when=when)


def test_claim_refuses_when_status_md_hand_prose_names_the_claimed_id(tmp_path, capsys):
    # WI-358. status.md is trunk-owned and forward-only, so the id named here
    # reds R-D on the COMPOSED tree the moment the WI closes — and the work
    # branch cannot scrub a file it does not own, so the red is undischargeable
    # from where it is discovered. The claim is the structural home: refuse now,
    # while the debt is one trunk commit, rather than at merge after the branch
    # is built. A warn would simply be ignored and the red would still land.
    root = claim_repo(tmp_path)
    write_status(
        root,
        "# Status\n\n## Next\n\n- Carry the WI-401 rewrite through review.\n",
    )

    assert integ.claim(root, "WI-401", "wi-401") == 1
    err = capsys.readouterr().err
    assert "WI-401 is named in hand-authored docs/status.md prose" in err
    assert "forward-only" in err
    # Nothing moved and no branch was cut: the debt is paid before the branch
    # exists, which is the whole point of hoisting the check to claim time.
    assert (root / "docs" / "work" / "queued" / "WI-401-widget.md").is_file()
    assert "wi-401" not in _branches(root)


def test_the_claim_refusal_names_the_offending_status_md_line(tmp_path, capsys):
    # Actionable like the rest of the ladder: the operator gets the line NUMBER
    # and the line TEXT, so the scrub needs no search. Line 5 is the bullet.
    root = claim_repo(tmp_path)
    write_status(
        root,
        "# Status\n"
        "\n"
        "## Next\n"
        "\n"
        "- Carry the WI-401 rewrite through review.\n"
        "- Unrelated WI-999 note.\n",
    )

    assert integ.claim(root, "WI-401", "wi-401") == 1
    err = capsys.readouterr().err
    assert "line 5" in err
    assert "Carry the WI-401 rewrite through review." in err
    # Only the matching id is quoted — a neighbouring bullet is not the debt.
    assert "WI-999" not in err


def test_claim_allows_an_id_that_appears_only_inside_the_generated_block(tmp_path):
    # The mode-aware half, matching check_trajectory's own R-D stand-down: a
    # generated status snapshot legitimately names QUEUED ids (it renders the
    # frontier), and its content is regenerated at close rather than scrubbed by
    # hand. Refusing on it would make every claim of a frontier WI impossible.
    root = claim_repo(tmp_path)
    write_status(
        root,
        "# Status\n"
        "\n"
        "<!-- BEGIN GENERATED STATUS -->\n"
        "- WI-401 — Widget (queued, ready)\n"
        "<!-- END GENERATED STATUS -->\n"
        "\n"
        "Hand prose that names no ids.\n",
    )

    assert integ.claim(root, "WI-401", "wi-401") == 0
    assert (root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md").is_file()
    assert "wi-401" in _branches(root)


def test_hand_prose_after_a_generated_block_is_still_policed(tmp_path):
    # The END sentinel really re-arms the scan — otherwise a status.md that
    # carries a generated block anywhere would exempt its whole tail, which is
    # exactly the hybrid-file hole check_trajectory's own R-D closed.
    root = claim_repo(tmp_path)
    write_status(
        root,
        "# Status\n"
        "\n"
        "<!-- BEGIN GENERATED STATUS -->\n"
        "- nothing here\n"
        "<!-- END GENERATED STATUS -->\n"
        "\n"
        "- Still to do: the WI-401 rewrite.\n",
    )

    assert integ.claim(root, "WI-401", "wi-401") == 1


def test_a_substring_id_in_status_prose_is_not_a_hit(tmp_path):
    # The token shape is check_trajectory's `\\bWI-\\d+\\b`, so WI-4010 is a
    # DIFFERENT work item, not a match on WI-401. Claim-time and merge-time must
    # agree on what counts as a token or the hoisted check drifts from the rule
    # it exists to pre-pay.
    root = claim_repo(tmp_path)
    write_status(root, "# Status\n\n- The WI-4010 rewrite is next.\n")

    assert integ.claim(root, "WI-401", "wi-401") == 0


def test_an_absent_status_md_is_not_a_claim_refusal(tmp_path):
    # status.md is optional (a fresh scaffold may not carry one); a missing file
    # is vacuously clean, never a fail-closed refusal — the rule being pre-paid
    # is itself vacuous there.
    root = claim_repo(tmp_path)
    assert not (root / "docs" / "status.md").exists()
    assert integ.claim(root, "WI-401", "wi-401") == 0


def test_a_status_md_that_cannot_be_read_is_a_refusal_not_a_traceback(tmp_path, capsys):
    # ABSENT is vacuously clean; PRESENT-BUT-UNREADABLE is not the same thing. A
    # directory (or a permission denial) at docs/status.md would otherwise escape
    # the claim as an OSError traceback, and — worse if it were caught loosely —
    # an unscanned status.md is exactly where the debt hides. Fail closed, with
    # the reason quoted.
    root = claim_repo(tmp_path)
    (root / "docs" / "status.md").mkdir(parents=True)

    assert integ.claim(root, "WI-401", "wi-401") == 1
    err = capsys.readouterr().err
    assert "docs/status.md exists but cannot be read" in err
    assert (root / "docs" / "work" / "queued" / "WI-401-widget.md").is_file()
    assert "wi-401" not in _branches(root)


def test_a_lowercase_wi_id_is_normalized_before_any_rung_runs(tmp_path):
    # `Path.glob` casefolds on Windows, so `--wi wi-401` resolves the queued spec
    # and then diverges from every rung that matches the canonical token: the
    # WI-358 status scan silently skipped, and the scheduler frontier refused
    # with a MISLEADING reason ("not on the ready frontier") for a WI that is on
    # it. One normalization at the CLI boundary keeps the rungs agreeing.
    root = claim_repo(tmp_path)
    write_status(root, "# Status\n\n- Carry the WI-401 rewrite through review.\n")

    proc = run_py(
        [
            SCRIPTS / "integrate.py",
            "--root",
            ".",
            "claim",
            "--wi",
            "wi-401",
            "--branch",
            "wi-401",
        ],
        cwd=root,
    )
    out = proc.stdout + proc.stderr
    assert proc.returncode == 1, out
    assert "named in hand-authored docs/status.md prose" in out, out
    assert "not on the ready frontier" not in out, out
    assert integ.normalize_wi_id("wi-401") == "WI-401"
    assert integ.normalize_wi_id("WI-401") == "WI-401"


# --- 2. finished-branch detection: the tree IS the signal ---------------------


def test_finished_is_the_move_to_complete_not_a_state_file(tmp_path):
    # §2.3 step 3. A claimed branch is finished exactly when its TIP holds no
    # spec under active/<branch>/ — the closing commit's move to complete/ is the
    # whole signal, so there is no state file to go stale and no ref to leak.
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0

    # Claimed but still in flight: the spec is right where the claim put it.
    assert integ.finished_branches(root) == []

    _git(root, "checkout", "-q", "wi-401")
    (root / "docs" / "work" / "complete").mkdir(parents=True, exist_ok=True)
    _git(
        root,
        "mv",
        "docs/work/active/wi-401/WI-401-widget.md",
        "docs/work/complete/WI-401-widget.md",
    )
    _commit(root, "close: WI-401 -> complete", when=T_VERDICT)
    _git(root, "checkout", "-q", "main")

    assert integ.finished_branches(root) == ["wi-401"]


def test_a_claim_dir_with_no_matching_branch_is_ignored(tmp_path):
    # Residue — a hand-made directory, an aborted claim, a branch deleted from
    # under one — must not enter the queue. Only a claim dir with a live branch
    # counts, and `ghost` sorts BEFORE `wi-401`, so a scan that failed open on
    # the first entry would be visible here.
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    _git(root, "checkout", "-q", "wi-401")
    (root / "docs" / "work" / "complete").mkdir(parents=True, exist_ok=True)
    _git(
        root,
        "mv",
        "docs/work/active/wi-401/WI-401-widget.md",
        "docs/work/complete/WI-401-widget.md",
    )
    _commit(root, "close: WI-401 -> complete", when=T_VERDICT)
    _git(root, "checkout", "-q", "main")

    claim_dir(root, "ghost")
    assert integ.finished_branches(root) == ["wi-401"]


def test_the_git_dependency_is_declared_for_this_module():
    # This suite drives real repositories end to end; without git on PATH every
    # test above would SKIP and the module would still print a green. The
    # declared gate (conftest.ENV_GATES) is what makes that skip COUNTED in the
    # terminal summary rather than invisible (WI-326).
    assert shutil.which("git"), "the module-level env gate should have skipped"
