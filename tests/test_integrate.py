"""integrate.py — the station protocol and its merge slot.

The backend of the one integration flow (docs/concurrency-restructure.md §1.2),
rebuilt by WI-386 on ONE constraint (docs/concurrency-v2.md §A2): **a branch may
not enter the merge queue unless trunk is already an ancestor of it.** The
lane-side `refresh` makes that true (merge trunk in, trunk_step, bar, commit)
and the slot verifies it. What this module pins, beyond the gates that were
always here, is that the constraint is really load-bearing rather than merely
documented:

  * **the constraint itself** — `trunk_is_ancestor` and `_merge_ready`, the two
    reads the slot makes, each proven to have two answers on a topology the
    test constructs;
  * **the refresh sequence AND its order** — merge trunk -> trunk_step -> bar ->
    commit, pinned by stub harness scripts that record the order they ran in, so
    a reordering is a failure rather than a silent change of meaning;
  * **the disposable-commit rule** (§A2.1) — a second refresh RESETS to the last
    work commit and redoes the merge; it never stacks, because docs/log.md is
    append-compiled and a stack would conflict on the file end;
  * **every refresh failure leaves the branch at its last work commit, clean** —
    a conflicting trunk merge and a red bar both, so nothing is ever parked;
  * **the slot has exactly one acquisition site** (§A2.0 requirement 1), asserted
    against the source, because "restricting to pessimistic is a one-line move"
    is only true while that stays true;
  * **the pessimistic path is not dead code** — a two-branch drain reaches it by
    construction, since the first merge moves trunk out from under the second.

It also pins the four gates that make the queue *fail-closed*, plus the whole
flow end-to-end:

  * **claim** (§2.3 steps 1+2) — the serial trunk move `queued/ ->
    active/<branch>/` and the branch cut from that commit, and the eight refusals
    that stand in front of it: the tracked pause (§5.6), a dirty trunk, a branch
    that already exists, a branch name that would not map to a flat claim
    directory, (WI-370) a spec whose `SpecRef` is empty or
    does not resolve in-repo — the R-E debt that becomes unpayable once the
    closing branch exists, hoisted the same way R-D was — a WI that is not on
    the scheduler's ready frontier, and (WI-358) a claimed id named in
    hand-authored `docs/status.md` prose — the forward-only debt that would
    red R-D on the composed tree at close, hoisted to where a single trunk
    commit can still pay it.
  * **finished-branch detection** — the closing commit's move to `complete/` IS
    the finished signal: no state file, no ref, just the tree.
  * **the R1 mint refusal** (WI-397) — a finished branch whose `docs/work/`
    delta ADDS a spec carrying an id it never claimed cannot merge, because
    minting is a serial trunk-side act and two lanes cannot see each other's
    trees. Driven on one topology built both ways (with and without the minted
    file), plus the shapes that must stay ADMITTED — a terminal-outcome move
    into `complete/` and `cancelled/`, a handback's return to `queued/` with its
    bar-inert `.patch`, and a TRUNK-side mint taken after the claim (free by
    construction: it is in the merge base, not in the branch's delta) — and the
    rename trap that makes `--no-renames` load-bearing rather than tidy.
  * **the verdict gate** (RULING-7) — the dialed review artifact must be
    present, must parse as APPROVE, and must be FRESH: a verdict whose last
    commit predates a later code commit on the branch is a stale APPROVE and
    does not clear the gate. Fragment (`docs/log.d/`) and review commits are
    excluded from "code", and so is the mechanical refresh commit (WI-386: it
    lands AFTER the review by construction, so counting it as code would make
    the gate unpassable) — bookkeeping cannot stale a good verdict.
  * **the declared bar** (§4) — a missing `docs/stack.ini`, an absent
    `[product] test`, or a declared-but-EMPTY one is a REFUSAL, never a skip.
  * **the RULING-6 window audit** — a non-merge trunk commit touching product
    paths is flagged by sha; bookkeeping surfaces and `--no-ff` merges are not.
  * **the §5.6 unload** (WI-359) — after the merge the branch is deleted and a
    CLEAN linked worktree holding it is GC'd, while a DIRTY one and the MAIN
    checkout are reported by branch and path on stderr and left untouched.
    "Dirty" counts IGNORED files and treats a failed dirt read as dirt: the
    content that exists nowhere else is usually the ignored kind, and the
    consequence of a wrong answer is deletion. No outcome is swallowed — a run
    that merged everything but left a branch held exits NONZERO, because §5.6's
    stop is drained AND unloaded and nothing ever retries the unload.

Every git fixture here is a REAL repository (the queue derives everything from
history — finished-ness from `ls-tree`, verdict freshness from commit times — so
a fake would test the wrong thing), and every ordering-sensitive commit is pinned
with `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE`: git records whole seconds, so two
back-to-back commits in a test tie and a tie would hide whether the freshness
rule is really time-derived (the tests/test_trunk_step.py idiom).

`integrate()` itself is only ever run as a SUBPROCESS here: it takes the
process-global coordinator lock fd (`agent_common.acquire_lock`), so calling it
in-process would leak a held descriptor into the rest of the suite. The
in-process tests call the pure-ish helpers, which take no lock.

The end-to-end test deliberately stands in the REAL bar: a bootstrapped scaffold
with a traced SN->SR->LLR->TC chain whose `check.py --tier smoke` genuinely
passes on the refreshed branch. `_run_bar` is never monkeypatched — a stubbed bar
is exactly the vacuous green this script exists to make impossible. The
station-protocol tests below use STUB harness scripts instead, and that is a
different claim, made honestly: they measure ORDER and TOPOLOGY (which script
ran when, which commit has which parents), which a real 11-minute bar would
measure no better and far more slowly. The real bar is still the one that
decides green, in the e2e above.
"""

import os
import re
import shutil
import subprocess

import pytest
from conftest import (
    SCRIPTS,
    env_gate_skipif,
    load_script,
    make_minimal_project,
    run_py,
    skip_without_env_gates,
)

pytestmark = env_gate_skipif("git")

integ = load_script("integrate")
spec_move = load_script("spec_move")

# Pinned commit stamps (unix seconds). Named rather than inlined so the ORDER a
# freshness test depends on is readable at the assertion.
T_BASE = 1_000_000
T_CODE = 1_000_100
T_VERDICT = 1_000_200
T_LATER = 1_000_300


# --- fixtures: real git repos ------------------------------------------------


def _git(root, *args, env=None):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _commit(root, message, when=None):
    """Commit everything staged/untracked, optionally at an EXACT timestamp
    (the tests/test_trunk_step.py `_commit` shape — git records whole seconds,
    so an unpinned pair of commits ties)."""
    import os

    env = dict(os.environ)
    if when is not None:
        stamp = "@{} +0000".format(when)  # git's raw date format
        env["GIT_AUTHOR_DATE"] = stamp
        env["GIT_COMMITTER_DATE"] = stamp
    _git(root, "add", "-A", env=env)
    _git(root, "commit", "-qm", message, env=env)


def git_repo(root, branch="main"):
    """A committed git repo on `branch` (the tests/test_check_lane.py `git_repo`
    shape, copied rather than imported — no test module in this suite imports
    another, and conftest is not this module's to extend).

    `git init -b` is 2.28+, so the branch is set with a symbolic-ref instead.
    The identity is repo-local because integrate.py commits through
    `agent_common.git`, which passes no `-c user.*`; signing is off so a
    developer's global `commit.gpgsign` cannot wedge the fixture."""
    skip_without_env_gates("git")
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "symbolic-ref", "HEAD", "refs/heads/" + branch)
    (root / "seed.txt").write_text("seed\n", encoding="utf-8", newline="\n")
    _commit(root, "seed", when=T_BASE)
    return root


def spec_text(
    wid,
    title="Widget",
    safety="ordinary",
    needs=(),
    order=0,
    deliverable="A widget, shipped.",
    specref=None,
    bar=None,
):
    """One work-item spec in the format `scripts/wi_convert.py` emits (the
    tests/test_wi_folder_loaders.py `spec_text` shape).

    The `## Deliverable` body is written by DEFAULT because the CLOSED form is
    the one that has to survive `check_trajectory` on the composed tree: R-A
    errors on a `status=done` WI with an empty Deliverable, and `complete/` is
    where every claimed spec ends up. `specref` is written only when given: the
    WI-370 claim rung wants it on a QUEUED spec, R-F wants it gone from an
    closed one, so each fixture states which shape it is."""
    lines = [
        'id = "{}"'.format(wid),
        'title = "{}"'.format(title),
        'workstream = "ws"',
        'sr_refs = ["SR-001"]',
        "needs = [{}]".format(", ".join('"{}"'.format(n) for n in needs)),
        'safety_class = "{}"'.format(safety),
        "order = {}".format(order),
    ]
    if specref:
        lines.append('specref = "{}"'.format(specref))
    if bar:
        lines.append('bar = "{}"'.format(bar))
    text = "+++\n" + "".join(ln + "\n" for ln in lines) + "+++\n"
    if deliverable:
        text += "\n## Deliverable\n\n" + deliverable + "\n"
    return text


def write_spec(root, where, wid, slug="widget", **kw):
    """Write `docs/work/<where>/<wid>-<slug>.md`; return its path.

    `newline="\\n"` explicitly: integrate._spec_frontmatter matches `+++\\n`, so
    a fixture that took the platform default would not parse on Windows — and a
    fixture that takes the platform default cannot test the platform (WI-337)."""
    path = root / "docs" / "work" / where / "{}-{}.md".format(wid, slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(spec_text(wid, **kw), encoding="utf-8", newline="\n")
    return path


def claim_dir(root, branch, wid="WI-999"):
    """A claim the Phase 2c way (§2.1/§2.3): the work item's spec sits in
    docs/work/active/<branch>/. The directory IS the claim."""
    path = write_spec(root, "active/" + branch, wid, slug="ghost")
    return path.parent


def _rev(root, ref):
    return _git(root, "rev-parse", ref).strip()


def _branches(root):
    return _git(root, "branch", "--format=%(refname:short)").split()


def claim_repo(tmp_path, branch="main", wi="WI-401", **spec_kw):
    """A trunk repo whose `docs/work/` spec folder IS the work-item registry
    (Phase 2b dual-read: real specs present => the folder is authoritative, so
    no docs/requirements/work-items.csv is needed at all). The queued spec
    resolves its SpecRef to the fixture's own seed file so the WI-370 rung
    passes by default — a rung-specific test overrides it."""
    git_repo(tmp_path, branch=branch)
    spec_kw.setdefault("specref", "seed.txt")
    write_spec(tmp_path, "queued", wi, **spec_kw)
    declare_generated(tmp_path)
    _commit(tmp_path, "file " + wi, when=T_CODE)
    return tmp_path


def declare_generated(root):
    """Declare the §5.2 generated set, the way the shipped stack.ini template
    does. NOT decoration: the claim folds `trunk_step --regen` into its commit,
    and with a `docs/work/` registry present that regen writes
    PROJECT_STATE.html — so a repo that has not declared its generated
    artifacts produces a claim commit touching an UNDECLARED path, which is the
    same thing `integrate audit` (RULING-6) flags and which `_abandoned_claim`
    reads with the same allowed set. Declaring it makes the fixture a repo the
    rest of the harness would also accept, rather than bending a rule to fit."""
    ini = root / "docs" / "stack.ini"
    ini.parent.mkdir(parents=True, exist_ok=True)
    text = ini.read_text(encoding="utf-8") if ini.exists() else ""
    if "[generated]" not in text:
        text += ("\n" if text and not text.endswith("\n") else "") + (
            "[generated]\nPROJECT_STATE.html = trajectory\n"
        )
    ini.write_text(text, encoding="utf-8", newline="\n")


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


# --- 2b. the OUTCOME is the folder (WI-387, §A3) ------------------------------


def _close_to(root, branch, directory, wi="WI-401", slug="widget"):
    """Move `branch`'s claimed spec into `directory` on the branch — the move
    that both finishes the lane and states its outcome."""
    _git(root, "checkout", "-q", branch)
    dest = root / "docs" / "work" / directory
    dest.mkdir(parents=True, exist_ok=True)
    _git(
        root,
        "mv",
        "docs/work/active/{}/{}-{}.md".format(branch, wi, slug),
        "docs/work/{}/{}-{}.md".format(directory, wi, slug),
    )
    _commit(root, "close: {} -> {}".format(wi, directory), when=T_VERDICT)
    _git(root, "checkout", "-q", "main")


def test_the_outcome_is_read_off_the_folder_the_specs_landed_in(tmp_path):
    # Three outcomes, one read, no state file — and the read must DISCRIMINATE,
    # so all three are driven on identical branches that differ only in which
    # folder the closing commit moved the spec into.
    for directory, outcome in (
        ("complete", "merged"),
        ("cancelled", "cancelled"),
        ("queued", "handback"),
        ("draft", "handback"),
    ):
        home = tmp_path / directory
        home.mkdir()
        root = claim_repo(home)
        assert integ.claim(root, "WI-401", "wi-401") == 0
        _close_to(root, "wi-401", directory)
        assert integ.finished_branches(root) == ["wi-401"]
        assert integ.branch_outcomes(root, "wi-401") == ({"WI-401": outcome}, [])


def test_a_claimed_spec_that_landed_TWICE_names_no_outcome_either(tmp_path):
    # The other half of "exactly one folder". A basename-keyed dict let the last
    # `ls-tree` line win — plain alphabetical precedence, which puts `queued`
    # (handback, no verdict owed) ahead of `complete` (merged, an APPROVE owed),
    # so a contradiction resolved silently toward the answer that SKIPS the
    # gate. REVIEW-A round 1 drove all three pairs. Fail-closure now lives where
    # the outcome is read, not in another script's duplicate-id rung.
    for first, second in (("complete", "queued"), ("cancelled", "queued")):
        home = tmp_path / (first + "-" + second)
        home.mkdir()
        root = claim_repo(home)
        assert integ.claim(root, "WI-401", "wi-401") == 0
        _git(root, "checkout", "-q", "wi-401")
        src = root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md"
        text = src.read_text(encoding="utf-8")
        for directory in (first, second):
            dst = root / "docs" / "work" / directory / "WI-401-widget.md"
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(text, encoding="utf-8", newline="\n")
        _git(root, "rm", "-q", "docs/work/active/wi-401/WI-401-widget.md")
        _commit(root, "close: WI-401 into two folders at once", when=T_VERDICT)
        _git(root, "checkout", "-q", "main")

        outcomes, unresolved = integ.branch_outcomes(root, "wi-401")
        assert outcomes == {} and unresolved == ["WI-401-widget.md"], (first, second)
        refusal = integ.integrate_one(root, "wi-401", "smoke")
        assert "exactly ONE declared state directory" in refusal
        assert _rev(root, "HEAD") != _rev(root, "wi-401")  # nothing merged


def test_a_claimed_spec_that_landed_nowhere_names_no_outcome(tmp_path):
    # Fail closed. A branch that DELETED its claimed spec is finished by the
    # active/-is-empty read but has stated nothing, and guessing an outcome for
    # it would let unreviewed work merge as if it had been approved.
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    _git(root, "checkout", "-q", "wi-401")
    _git(root, "rm", "-q", "docs/work/active/wi-401/WI-401-widget.md")
    _commit(root, "close: delete the spec instead of moving it", when=T_VERDICT)
    _git(root, "checkout", "-q", "main")

    assert integ.branch_outcomes(root, "wi-401") == ({}, ["WI-401-widget.md"])
    refusal = integ.integrate_one(root, "wi-401", "smoke")
    assert "exactly ONE declared state directory" in refusal
    assert _rev(root, "HEAD") != _rev(root, "wi-401")  # nothing merged


# --- 2c. the R1 mint refusal (WI-397) ----------------------------------------


def _mint_repo(home, minted=None, directory="complete"):
    """A claimed branch that CLOSED its own spec into `directory` — and, when
    `minted` is given, filed a spec for that id in the same commit.

    One builder for both sides of the rung, so "the same branch with the foreign
    spec removed" is literally the same topology minus one file rather than a
    second fixture that happens to look similar."""
    home.mkdir(parents=True, exist_ok=True)
    root = claim_repo(home)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    _git(root, "checkout", "-q", "wi-401")
    if minted is not None:
        write_spec(root, "queued", minted, slug="found-mid-flight", specref="seed.txt")
    dest = root / "docs" / "work" / directory
    dest.mkdir(parents=True, exist_ok=True)
    _git(
        root,
        "mv",
        "docs/work/active/wi-401/WI-401-widget.md",
        "docs/work/{}/WI-401-widget.md".format(directory),
    )
    _commit(root, "close: WI-401 -> {}".format(directory), when=T_VERDICT)
    _git(root, "checkout", "-q", "main")
    return root


def test_a_branch_that_mints_a_foreign_id_is_refused_at_the_merge_slot(tmp_path):
    # RULING R1 (owner, 2026-08-01). Two lanes cannot see each other's trees, so
    # a branch-side `max(id) + 1` collides by construction — it happened twice in
    # one session. The rung makes it unrepresentable at the one point every lane
    # passes through, and the refusal has to be ACTIONABLE: the foreign id, the
    # path that carries it, the claimed set it was judged against, and the rule.
    root = _mint_repo(tmp_path / "minted", minted="WI-777")

    refusal = integ.integrate_one(root, "wi-401", "smoke")
    assert refusal is not None
    assert "WI-777" in refusal
    assert "docs/work/queued/WI-777-found-mid-flight.md" in refusal
    assert "NEVER MINTS A WORK-ITEM ID" in refusal
    assert "(WI-401)" in refusal  # the claimed set, so the judgement is checkable
    assert _rev(root, "HEAD") != _rev(root, "wi-401")  # nothing merged


def test_the_same_branch_without_the_minted_spec_is_admitted(tmp_path):
    # The other half of the same topology: a rung that refused everything would
    # pass the test above. Driven twice — the rung itself says None, and the SLOT
    # gets past it to the NEXT refusal (this fixture declares no `[product] test`),
    # which is what proves the admission is in situ and not just in the helper.
    root = _mint_repo(tmp_path / "clean", minted=None)

    claimed = integ._claimed_wi_ids(root, "wi-401")
    assert claimed == ["WI-401"]
    assert integ._minted_id_refusal(root, "wi-401", claimed) is None
    refusal = integ.integrate_one(root, "wi-401", "smoke")
    assert "no [product] test declaration" in refusal
    assert "NEVER MINTS" not in refusal


def test_a_branchs_own_terminal_outcome_move_is_admitted(tmp_path):
    # The move that CLOSES a lane re-ADDS the spec under its terminal folder, so
    # a rung reading adds naively would refuse every branch that ever finished.
    # Both terminal folders, because both are that move.
    for directory in ("complete", "cancelled"):
        root = _mint_repo(tmp_path / directory, directory=directory)
        claimed = integ._claimed_wi_ids(root, "wi-401")
        added = [
            ln
            for ln in _git(
                root,
                "diff",
                "--name-status",
                "--no-renames",
                _rev(root, "main"),
                "wi-401",
                "--",
                "docs/work",
            ).splitlines()
            if ln.startswith("A")
        ]
        # The move really is an ADD on this side — the admission is the rung
        # reading the id, not the diff happening to be empty.
        assert added == ["A\tdocs/work/{}/WI-401-widget.md".format(directory)], added
        assert integ._minted_id_refusal(root, "wi-401", claimed) is None, directory


def test_a_handbacks_return_to_queued_and_its_artefact_are_admitted(tmp_path):
    # The third outcome (§A3). A handback ADDS its own spec back under `queued/`
    # and drops a bar-inert `.patch` beside it — the shape `handback.py` writes.
    # Neither is a mint: the returned spec's id is claimed, and the artefact
    # carries no spec filename at all.
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    _git(root, "checkout", "-q", "wi-401")
    _git(
        root,
        "mv",
        "docs/work/active/wi-401/WI-401-widget.md",
        "docs/work/queued/WI-401-widget.md",
    )
    patch = root / "docs" / "work" / "handback" / "wi-401.patch"
    patch.parent.mkdir(parents=True, exist_ok=True)
    patch.write_text("--- a/x\n+++ b/x\n", encoding="utf-8", newline="\n")
    _commit(root, "handback: WI-401 -> queued/", when=T_VERDICT)
    _git(root, "checkout", "-q", "main")

    assert integ.branch_outcomes(root, "wi-401") == ({"WI-401": "handback"}, [])
    assert integ._minted_id_refusal(root, "wi-401", ["WI-401"]) is None


def test_a_trunk_side_mint_after_the_claim_is_not_the_branchs(tmp_path):
    # The other half of the ruling, and the half a rung reading the WHOLE tree
    # would get wrong: trunk-side minting stays exactly as free as it was. It is
    # free by CONSTRUCTION rather than by exemption — whatever trunk did sits in
    # the merge BASE, so it is not in the branch's delta at all.
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    write_spec(root, "queued", "WI-500", slug="filed-on-trunk", specref="seed.txt")
    _commit(root, "file WI-500 on the trunk", when=T_LATER)
    _close_to(root, "wi-401", "complete")

    # The id really is present on trunk and really is not the branch's.
    assert (root / "docs" / "work" / "queued" / "WI-500-filed-on-trunk.md").is_file()
    assert integ._minted_id_refusal(root, "wi-401", ["WI-401"]) is None


def test_the_mint_is_seen_even_when_git_would_report_it_as_a_rename(tmp_path):
    # Why the diff is read `--no-renames`, driven rather than asserted. Rename
    # detection is free to pair the branch's own close (a DELETE under
    # `active/`) with the minted file — spec files are short and near-identical
    # — and then the mint arrives as one `R` record with no add left to see.
    # Here the minted spec is a BYTE COPY of the claimed one while the closed
    # copy was edited, so the pairing is unambiguous and reproducible.
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    _git(root, "checkout", "-q", "wi-401")
    src = root / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md"
    original = src.read_text(encoding="utf-8")
    (root / "docs" / "work" / "queued" / "WI-777-copy.md").write_text(
        original, encoding="utf-8", newline="\n"
    )
    dest = root / "docs" / "work" / "complete" / "WI-401-widget.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        original.replace("A widget, shipped.", "A widget, shipped, at last."),
        encoding="utf-8",
        newline="\n",
    )
    _git(root, "rm", "-q", "docs/work/active/wi-401/WI-401-widget.md")
    _commit(root, "close: WI-401 -> complete, and mint WI-777", when=T_VERDICT)
    _git(root, "checkout", "-q", "main")

    # The trap, MEASURED: with rename detection on, the mint appears in exactly
    # one record and that record is an `R` (git pairs it with the delete side of
    # the close). The only ADD left is the branch's own legitimate close — so an
    # add-reader would see nothing wrong and merge the collision.
    detected = _git(
        root,
        "diff",
        "--name-status",
        "-M",
        _rev(root, "main"),
        "wi-401",
        "--",
        "docs/work",
    )
    minted = [ln for ln in detected.splitlines() if "WI-777" in ln]
    assert len(minted) == 1 and minted[0].startswith("R"), detected
    assert "A\tdocs/work/complete/WI-401-widget.md" in detected, detected

    refusal = integ._minted_id_refusal(root, "wi-401", ["WI-401"])
    assert refusal is not None and "WI-777" in refusal


# --- 3. the verdict gate (RULING-7) ------------------------------------------


VERDICT_APPROVE = """# Review A — WI-401

Model: test/reviewer

VERDICT: APPROVE findings=0
"""

VERDICT_CHANGES = """# Review A — WI-401

Model: test/reviewer

- [MAJOR] src/widget.py:1 -> the value is wrong -> return 2
- [MINOR] src/widget.py:1 -> no docstring -> add one

VERDICT: CHANGES-REQUESTED findings=2
"""


def verdict_repo(tmp_path, policy="1"):
    """A trunk carrying the declared review-policy dial, plus a work branch with
    one code commit on it (pinned at T_CODE)."""
    root = git_repo(tmp_path)
    docs = root / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "review-policy").write_text(policy + "\n", encoding="utf-8", newline="\n")
    _commit(root, "declare the review policy", when=T_BASE)
    _git(root, "checkout", "-q", "-b", "wi-401")
    (root / "src").mkdir(exist_ok=True)
    (root / "src" / "widget.py").write_text(
        "VALUE = 1\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "feat: the widget", when=T_CODE)
    return root


def write_verdict(root, text, when):
    path = root / "docs" / "reviews" / "WI-401-REVIEW-A.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    _commit(root, "review: WI-401 REVIEW-A", when=when)


def test_verdict_is_not_required_at_review_policy_zero(tmp_path):
    # The dial off is a real configuration, not a loophole: at 0 the harness
    # gates ARE the bar and the queue asks for no verdict artifact.
    root = verdict_repo(tmp_path, policy="0")
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None


def test_a_required_verdict_absent_from_the_branch_refuses_by_name(tmp_path):
    # Fail-closed and ACTIONABLE: the refusal names the exact path the branch
    # must carry, so the remedy needs no lookup.
    root = verdict_repo(tmp_path, policy="1")
    refusal = integ._verdict_gate(root, "wi-401", {"WI-401": "merged"})
    assert refusal is not None
    assert "docs/reviews/WI-401-REVIEW-A.md" in refusal
    assert "absent from wi-401" in refusal


def test_a_changes_requested_verdict_refuses(tmp_path):
    # Present is not enough — the machine line is PARSED (score_reviews), so a
    # verdict that asked for changes cannot clear the gate by existing.
    root = verdict_repo(tmp_path, policy="1")
    write_verdict(root, VERDICT_CHANGES, when=T_VERDICT)

    refusal = integ._verdict_gate(root, "wi-401", {"WI-401": "merged"})
    assert refusal is not None
    assert "is not an APPROVE" in refusal
    assert "CHANGES-REQUESTED" in refusal


def test_an_approve_that_predates_a_later_code_commit_is_stale(tmp_path):
    # The §5.4 hole this closes: under WI-scoped verdict naming the FILENAME no
    # longer binds a verdict to a revision, so freshness is git-derived. An
    # APPROVE from an earlier iteration, with real code committed after it, is
    # exactly the stale pass that would silently clear the gate.
    root = verdict_repo(tmp_path, policy="1")
    write_verdict(root, VERDICT_APPROVE, when=T_VERDICT)
    (root / "src" / "widget.py").write_text(
        "VALUE = 2\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "feat: change the widget after the review", when=T_LATER)

    refusal = integ._verdict_gate(root, "wi-401", {"WI-401": "merged"})
    assert refusal is not None
    assert "predates the branch's last code commit" in refusal


def test_an_approve_committed_after_the_last_code_commit_passes(tmp_path):
    # The green path of the same rule — asserted alongside the stale case above
    # so the freshness comparison is proven to have two answers, not one.
    root = verdict_repo(tmp_path, policy="1")
    write_verdict(root, VERDICT_APPROVE, when=T_VERDICT)
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None


def test_a_later_log_fragment_commit_does_not_stale_a_good_verdict(tmp_path):
    # The `:(exclude)docs/log.d` half of the freshness pathspec. A branch drops
    # its §5.1 log fragment as the LAST thing it does, routinely after the
    # review — if bookkeeping counted as code, the honest flow would stale its
    # own verdict every time and the gate would be unpassable. The previous test
    # (a real src/ commit at the same later stamp DOES stale it) is what proves
    # this is an exclusion rather than a broken comparison.
    root = verdict_repo(tmp_path, policy="1")
    write_verdict(root, VERDICT_APPROVE, when=T_VERDICT)
    fragment = root / "docs" / "log.d" / "WI-401-widget.md"
    fragment.parent.mkdir(parents=True, exist_ok=True)
    fragment.write_text("## WI-401 — the widget\n", encoding="utf-8", newline="\n")
    _commit(root, "log: WI-401 fragment", when=T_LATER)

    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None


def test_only_the_merged_outcome_owes_a_verdict(tmp_path):
    # KEYED OFF THE OUTCOME, NOT THE CLAIM (WI-387, §A3). One repo, one missing
    # verdict, three answers: `merged` asserts the work is done and owes an
    # APPROVE; `cancelled` and `handback` assert the opposite and owe none.
    # Reading the requirement off the claim would deadlock the commonest
    # handback cause on itself — a review escalation is exactly the case where
    # no APPROVE exists, so the lane could not return the work it failed to get
    # approved.
    root = verdict_repo(tmp_path, policy="1")
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is not None
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "cancelled"}) is None
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "handback"}) is None
    # ...and a MIXED branch is gated on its merged constituent alone.
    mixed = {"WI-401": "handback", "WI-402": "merged"}
    assert "WI-402-REVIEW-A.md" in integ._verdict_gate(root, "wi-401", mixed)


def test_a_malformed_review_policy_fails_closed(tmp_path):
    # A dial nobody can parse must never read as "0 = no review required". The
    # refusal quotes what it read, because the typo is the whole diagnosis.
    root = verdict_repo(tmp_path, policy="sometimes")
    refusal = integ._verdict_gate(root, "wi-401", {"WI-401": "merged"})
    assert refusal is not None
    assert "docs/review-policy is not an integer" in refusal
    assert "sometimes" in refusal and "fail closed" in refusal


# --- 4. the declared bar (§4): undeclared is a refusal, never a skip ----------


def _stack_ini(tmp_path, text):
    docs = tmp_path / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "stack.ini").write_text(text, encoding="utf-8", newline="\n")
    return tmp_path


def test_an_absent_stack_ini_is_a_refusal(tmp_path):
    (tmp_path / "docs").mkdir()
    refusal = integ._declared_bar_or_refusal(tmp_path)
    assert refusal is not None and "docs/stack.ini is absent" in refusal


def test_a_stack_ini_without_a_product_test_key_is_a_refusal(tmp_path):
    # A [product] section that declares format/lint but no test is a repo whose
    # bar was never stated. Skipping it is how `bar_failures: 0` came to mean
    # "nothing ran" (the §4.4 fail-open lesson).
    _stack_ini(tmp_path, "[product]\nformat = ruff format --check src\n")
    refusal = integ._declared_bar_or_refusal(tmp_path)
    assert refusal is not None and "no [product] test declaration" in refusal


def test_a_declared_but_empty_test_command_is_a_refusal(tmp_path):
    # The sharpest edge: the key EXISTS, so a "did they declare it?" check would
    # pass. An empty command is a misconfiguration, and it is named as one.
    _stack_ini(tmp_path, "[product]\ntest =\n")
    refusal = integ._declared_bar_or_refusal(tmp_path)
    assert refusal is not None and "declared but EMPTY" in refusal


def test_a_declared_test_command_passes_the_bar_declaration_check(tmp_path):
    _stack_ini(tmp_path, "[product]\ntest = {py} -m pytest -q\n")
    assert integ._declared_bar_or_refusal(tmp_path) is None


def test_a_declared_toolchain_without_its_venv_refuses_the_bar(tmp_path):
    # WI-361: the re-homed WI-286 floor. A repo that DECLARES the pinned toolchain
    # (requirements-dev.txt) but has no ./.venv would otherwise run the composed-
    # tree bar on the ambient interpreter, whose green may be false. The queue
    # refuses instead, loudly and by name, before it composes anything.
    _stack_ini(tmp_path, "[product]\ntest = {py} -m pytest -q\n")
    (tmp_path / "requirements-dev.txt").write_text("pytest\n", encoding="utf-8")
    refusal = integ._declared_bar_or_refusal(tmp_path)
    assert refusal is not None
    assert "harness floor REFUSES" in refusal
    assert "no runnable ./.venv" in refusal and "dev-setup --install" in refusal


def test_a_scaffold_that_declares_no_toolchain_still_runs_the_bar(tmp_path):
    # The arming boundary from the wired side: the SAME venv-less root without the
    # declaration is not refused. This is the property the whole venv-less fixture
    # fleet (including the e2e scaffolds in this file) depends on.
    _stack_ini(tmp_path, "[product]\ntest = {py} -m pytest -q\n")
    assert integ._declared_bar_or_refusal(tmp_path) is None


# --- 4b. the BRANCH tree's own harness (WI-368, relocated by WI-386) ----------
#
# These four covered "the COMPOSED tree's copy of the harness must run, not the
# invoker's" — and the composed tree is exactly what WI-386 deleted. The
# behaviour did not go with it: the refresh regenerates and bars the BRANCH
# tree, and the invoker is still trunk-vintage whenever drive.py drives the loop
# in-process, so a branch that changes a generator must still be regenerated
# with its own copy. Coverage relocated, not deleted (the Phase 5 precedent).


def test_the_branch_trees_copy_wins_under_the_invokers_layout(tmp_path, monkeypatch):
    # The meta-repo shape: the invoker sits INSIDE --root, and the lane worktree
    # carries the same relative layout — the branch's copy must win, or a
    # branch that changed a generator is regenerated with the trunk's vintage
    # and refused by the refresh commit's own freshness floor (the WI-368 hit).
    root = tmp_path / "root"
    inv = root / "kit" / "scripts"
    inv.mkdir(parents=True)
    (inv / "trunk_step.py").write_text("# invoker\n", encoding="utf-8", newline="\n")
    monkeypatch.setattr(integ, "SCRIPTS", inv)
    wt = tmp_path / "lane"
    lane = wt / "kit" / "scripts"
    lane.mkdir(parents=True)
    (lane / "trunk_step.py").write_text("# branch\n", encoding="utf-8", newline="\n")
    got = integ._branch_tree_script(wt, root, "trunk_step.py")
    assert got == lane / "trunk_step.py"


def test_an_out_of_root_invoker_probes_the_known_layouts(tmp_path, monkeypatch):
    # The kit-source-against-a-scaffold shape (this suite's own e2e fixtures):
    # SCRIPTS is not under --root, so the relative-layout join cannot apply and
    # the scaffold's scripts/ copy is found by the known-layout probe.
    inv = tmp_path / "elsewhere" / "scripts"
    inv.mkdir(parents=True)
    (inv / "check.py").write_text("# invoker\n", encoding="utf-8", newline="\n")
    monkeypatch.setattr(integ, "SCRIPTS", inv)
    wt = tmp_path / "lane"
    (wt / "scripts").mkdir(parents=True)
    (wt / "scripts" / "check.py").write_text(
        "# branch\n", encoding="utf-8", newline="\n"
    )
    got = integ._branch_tree_script(wt, tmp_path / "repo", "check.py")
    assert got == wt / "scripts" / "check.py"


def test_a_branch_tree_without_the_script_falls_back_to_the_invoker(
    tmp_path, monkeypatch
):
    # A branch that predates the script (or carries no harness at all) must
    # still integrate: the invoker's copy is the declared fallback, not a crash
    # and not a silent skip.
    inv = tmp_path / "elsewhere" / "scripts"
    inv.mkdir(parents=True)
    (inv / "trunk_step.py").write_text("# invoker\n", encoding="utf-8", newline="\n")
    monkeypatch.setattr(integ, "SCRIPTS", inv)
    wt = tmp_path / "lane"
    wt.mkdir()
    got = integ._branch_tree_script(wt, tmp_path / "repo", "trunk_step.py")
    assert got == inv / "trunk_step.py"


def test_run_trunk_step_executes_the_branch_trees_copy(tmp_path, monkeypatch):
    # The seam itself, non-vacuous against the pre-fix wiring: the invoker's
    # copy exits 3, the branch tree's writes a sentinel — so a pass proves
    # WHICH copy ran, not merely that something exited 0.
    inv = tmp_path / "elsewhere" / "scripts"
    inv.mkdir(parents=True)
    (inv / "trunk_step.py").write_text(
        "import sys\n\nsys.exit(3)\n", encoding="utf-8", newline="\n"
    )
    monkeypatch.setattr(integ, "SCRIPTS", inv)
    root = tmp_path / "repo"
    root.mkdir()
    wt = tmp_path / "lane"
    (wt / "scripts").mkdir(parents=True)
    (wt / "scripts" / "trunk_step.py").write_text(
        'from pathlib import Path\n\nPath("sentinel.txt").write_text("branch\\n")\n',
        encoding="utf-8",
        newline="\n",
    )
    code, out = integ._run_trunk_step(wt, root)
    assert code == 0, out
    assert (wt / "sentinel.txt").read_text(encoding="utf-8") == "branch\n"


# --- 5. the RULING-6 window audit --------------------------------------------


def test_audit_flags_a_non_merge_trunk_commit_touching_product_paths(tmp_path, capsys):
    # RULING-6: product changes reach the trunk only through the integrator's
    # merge. A direct commit is named by sha AND by the path that convicted it,
    # so the finding is reviewable without re-running git.
    root = git_repo(tmp_path)
    base = _rev(root, "HEAD")
    (root / "src").mkdir()
    (root / "src" / "widget.py").write_text(
        "VALUE = 1\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "feat: straight onto the trunk", when=T_CODE)
    sha = _rev(root, "HEAD")

    assert integ.audit(root, base) == 1
    err = capsys.readouterr().err
    assert sha[:10] in err
    assert "src/widget.py" in err


def test_audit_passes_a_window_of_bookkeeping_commits_only(tmp_path, capsys):
    # The coordinator's own surfaces — the claim move, the fragment drop, the
    # compiled log — are content-free serial bookkeeping and are exactly what
    # the integrator itself commits during a run.
    root = git_repo(tmp_path)
    base = _rev(root, "HEAD")
    write_spec(root, "queued", "WI-401")
    _commit(root, "claim: bookkeeping", when=T_CODE)
    fragment = root / "docs" / "log.d" / "WI-401-widget.md"
    fragment.parent.mkdir(parents=True, exist_ok=True)
    fragment.write_text("## WI-401 — the widget\n", encoding="utf-8", newline="\n")
    _commit(root, "log: fragment", when=T_VERDICT)
    (root / "docs" / "log.md").write_text(
        "# Log\n\n## WI-401 — the widget\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "log: compile", when=T_LATER)

    assert integ.audit(root, base) == 0
    assert "audit clean" in capsys.readouterr().out


def test_audit_allows_product_changes_that_arrive_by_a_no_ff_merge(tmp_path, capsys):
    # The permitted shape, and the reason the audit reads `--first-parent
    # --no-merges`: the merge commit itself is excluded, and the branch's own
    # commits are not on the trunk's first-parent chain. A rule that flagged
    # these would flag the integrator's entire purpose.
    root = git_repo(tmp_path)
    base = _rev(root, "HEAD")
    _git(root, "checkout", "-q", "-b", "wi-401")
    (root / "src").mkdir()
    (root / "src" / "widget.py").write_text(
        "VALUE = 1\n", encoding="utf-8", newline="\n"
    )
    _commit(root, "feat: the widget", when=T_CODE)
    _git(root, "checkout", "-q", "main")
    _git(root, "merge", "--no-ff", "-m", "integrate: merge wi-401 (WI-401)", "wi-401")

    assert (root / "src" / "widget.py").is_file()  # the product change did land
    assert integ.audit(root, base) == 0
    assert "audit clean" in capsys.readouterr().out


# --- 5b. THE STATION PROTOCOL (WI-386) ---------------------------------------
#
# The one constraint, the refresh that satisfies it, and the two properties the
# owner's caveat turned into requirements. Every fixture below CONSTRUCTS the
# topology it measures — two branches cut from one base, a trunk that moves
# under a finished branch — rather than inheriting a repo's state, because the
# thing under test is a relationship between commits.

# A stub harness pair, written INTO the branch tree so `_branch_tree_script`
# finds it there. Each appends its own name to a `harness-order.txt` that sits
# OUTSIDE the worktree — the refresh sheds the residue its own bar leaves, and
# rightly, so a recorder placed inside the tree would be swept away by the very
# behaviour it is there to record. That file is what makes the ORDER assertion
# possible at all: the real bar can say "green", but only a recording stub can
# say "and I ran after the trunk step".
STUB_TRUNK_STEP = """import pathlib

pathlib.Path("..", "harness-order.txt").open("a", encoding="utf-8").write(
    "trunk_step\\n"
)
pathlib.Path("regenerated.txt").write_text("fresh\\n", encoding="utf-8")
"""

STUB_CHECK_GREEN = """import pathlib
import sys

pathlib.Path("..", "harness-order.txt").open("a", encoding="utf-8").write(
    "check " + " ".join(sys.argv[1:]) + "\\n"
)
pathlib.Path("bar-cache").mkdir(exist_ok=True)
pathlib.Path("bar-cache", "run.txt").write_text("a tool cache\\n", encoding="utf-8")
print("  PASS  format           0.1s")
print("  PASS  tests+coverage   0.2s")
"""

STUB_CHECK_RED = """import pathlib
import sys

pathlib.Path("..", "harness-order.txt").open("a", encoding="utf-8").write(
    "check-red\\n"
)
print("=== format : stub ruff format --check ===")
print("  PASS  format           0.1s")
print("=== tests+coverage : stub pytest -q ===")
print("FAILED tests/test_widget.py::test_value - AssertionError: VALUE")
print("1 failed, 3 passed in 0.2s")
print("  FAIL  tests+coverage   exit 1 (0.2s)")
print("=" * 56)
print("Check summary (gate G3, tier smoke):")
print("  PASS  format           0.1s")
print("  FAIL  tests+coverage   exit 1 (0.2s)")
print("=" * 56)
print("RESULT: FAIL (1 step(s) failed)")
sys.exit(1)
"""


def station_repo(
    tmp_path, check_src=STUB_CHECK_GREEN, policy="0", dest="complete", **spec_kw
):
    """A trunk with WI-401 claimed onto `wi-401` and CLOSED, plus a stub harness.

    Everything the slot reads is real: a real claim commit, a real branch, a
    real closing move. Only the two harness scripts are stubs, and they are
    stubs so the test can assert the ORDER they ran in — see above. `spec_kw`
    shapes the claimed spec (the WI-388 bar/no-bar tests declare `bar=` or
    `safety=` on it).
    """
    root = claim_repo(tmp_path, **spec_kw)
    (root / ".gitignore").write_text(
        "out/\nbar-cache/\n", encoding="utf-8", newline="\n"
    )
    (root / "docs" / "stack.ini").write_text(
        "[product]\ntest = {py} -m pytest -q\n", encoding="utf-8", newline="\n"
    )
    declare_generated(root)
    (root / "docs" / "review-policy").write_text(
        policy + "\n", encoding="utf-8", newline="\n"
    )
    scripts = root / "scripts"
    scripts.mkdir(exist_ok=True)
    (scripts / "trunk_step.py").write_text(
        STUB_TRUNK_STEP, encoding="utf-8", newline="\n"
    )
    (scripts / "check.py").write_text(check_src, encoding="utf-8", newline="\n")
    _commit(root, "chore: the stub harness and the declared bar", when=T_CODE)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    close_branch(root, "wi-401", dest=dest)
    return root


def close_branch(root, branch, wi="WI-401", slug="widget", extra=None, dest="complete"):
    """Build and CLOSE `branch` in its own lane worktree: one product commit and
    the §2.3 step-3 move to its TERMINAL directory. Leaves the worktree
    registered, which is where the refresh will run — the lane's own tree, by
    design. (WI-384 split `archive/` into `complete/` + `cancelled/`; the
    finished signal is unchanged — the tree no longer holds a spec under
    `active/<branch>/` — but the destination has to be a real state folder or
    the loaders refuse it.)"""
    wt = root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / branch
    _git(root, "worktree", "add", "-q", str(wt), branch)
    (wt / "{}.txt".format(branch)).write_text("1\n", encoding="utf-8", newline="\n")
    dst = wt / "docs" / "work" / dest / "{}-{}.md".format(wi, slug)
    dst.parent.mkdir(parents=True, exist_ok=True)
    src = wt / "docs" / "work" / "active" / branch / "{}-{}.md".format(wi, slug)
    dst.write_text(
        src.read_text(encoding="utf-8").replace('specref = "seed.txt"\n', ""),
        encoding="utf-8",
        newline="\n",
    )
    _git(wt, "rm", "-q", "docs/work/active/{}/{}-{}.md".format(branch, wi, slug))
    if extra:
        (wt / extra[0]).write_text(extra[1], encoding="utf-8", newline="\n")
    _commit(wt, "{}: build + close".format(wi), when=T_VERDICT)
    return wt


def _lane(root, branch):
    """The lane worktree path `station_repo`/`close_branch` put the branch in."""
    return root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / branch


def _order(wt):
    path = wt.parent / "harness-order.txt"
    return path.read_text(encoding="utf-8").split() if path.is_file() else []


def _refresh_commits(root, branch):
    """Every commit on `branch` carrying the bar-green trailer, tip-first."""
    out = _git(root, "log", "--format=%H%x1f%B%x1e", branch).split("\x1e")
    hits = []
    for entry in out:
        if not entry.strip():
            continue
        sha, _, body = entry.strip().partition("\x1f")
        if integ.BAR_GREEN in body:
            hits.append(sha)
    return hits


# 5b.1 — the constraint itself


def test_trunk_is_ancestor_has_two_answers_on_a_constructed_topology(tmp_path):
    # THE one line the whole design rests on, proven to discriminate. The branch
    # is cut from trunk (ancestor: yes); then trunk moves (ancestor: no). If this
    # read were vacuously true the slot would merge anything.
    root = station_repo(tmp_path)
    assert integ.trunk_is_ancestor(root, "wi-401")

    (root / "trunk-moved.txt").write_text("x\n", encoding="utf-8", newline="\n")
    _commit(root, "docs: trunk moves under the finished branch", when=T_LATER)
    assert not integ.trunk_is_ancestor(root, "wi-401")


def test_merge_ready_needs_the_ancestor_relation_AND_the_attestation(tmp_path):
    # Ancestry alone says nothing about whether anyone barred the composition,
    # so the tip must also carry the bar's own trailer. Both halves are shown
    # failing separately, then passing together — a single-answer gate is not a
    # gate.
    root = station_repo(tmp_path)
    ready, why = integ._merge_ready(root, "wi-401")
    assert not ready and "not a verified refresh commit" in why  # ancestor ok

    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    ready, why = integ._merge_ready(root, "wi-401")
    assert ready and "PASS" in why

    (root / "trunk-moved.txt").write_text("x\n", encoding="utf-8", newline="\n")
    _commit(root, "docs: trunk moves after the refresh", when=T_LATER)
    ready, why = integ._merge_ready(root, "wi-401")
    assert not ready and "is not an ancestor of it" in why
    assert sha == _rev(root, "wi-401")  # the attestation is still there; trunk moved


# 5b.2 — the refresh, and the order inside it


def test_the_refresh_merges_trunk_in_regenerates_bars_then_commits(tmp_path):
    # The order is FIXED and load-bearing (§A2.1): the compile has to see the
    # trunk's log before it appends, and the bar has to see what the compile and
    # the regen wrote. Asserted by recording stubs rather than by reading the
    # source, so a reordering fails here instead of passing quietly.
    root = station_repo(tmp_path)
    (root / "trunk-moved.txt").write_text("x\n", encoding="utf-8", newline="\n")
    _commit(root, "docs: trunk moves under the finished branch", when=T_LATER)
    trunk = _rev(root, "HEAD")
    work_tip = _rev(root, "wi-401")
    wt = root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / "wi-401"

    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal

    # 1. the harness ran in the declared order, and the bar was told to stand in
    #    the TRUNK lane (the freshness gates it just regenerated must run).
    assert _order(wt)[0] == "trunk_step"
    assert "check" in _order(wt) and "--trunk-lane" in _order(wt)
    assert _order(wt).index("trunk_step") < _order(wt).index("check")
    # 2. the refresh commit is a real MERGE of trunk into the branch's work tip.
    parents = _git(root, "rev-list", "--parents", "-n", "1", sha).split()
    assert parents[1:] == [work_tip, trunk], parents
    # 3. trunk is now an ancestor — which is the entire point of the operation.
    assert integ.trunk_is_ancestor(root, "wi-401")
    # 4. ...and the tree carries what the trunk step wrote, so the bar barred it.
    assert (wt / "regenerated.txt").is_file()
    assert "regenerated.txt" in _git(root, "ls-tree", "-r", "--name-only", sha)


def test_the_refresh_attests_the_bar_to_the_sha_it_produced(tmp_path):
    # "Attested to a TREE, not to a run" (§A2): the trailer lives in the commit,
    # so the slot verifies a property of the sha rather than someone's claim
    # about a run. A later commit on the branch therefore REVOKES it, because
    # the tip is no longer the tree that was barred.
    root = station_repo(tmp_path)
    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert integ.refresh_attestation(root, "wi-401", sha)
    assert integ.refresh_attestation(root, "wi-401")

    wt = root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / "wi-401"
    (wt / "afterthought.txt").write_text("x\n", encoding="utf-8", newline="\n")
    _commit(wt, "WI-401: one more idea", when=T_LATER)
    assert integ.refresh_attestation(root, "wi-401") is None
    ready, why = integ._merge_ready(root, "wi-401")
    assert not ready and "not a verified refresh commit" in why


def test_the_bar_residue_the_refresh_created_is_shed_but_the_lanes_is_not(tmp_path):
    # The refresh leaves the lane worktree as it found it plus one commit. It
    # sheds the IGNORED residue its own bar wrote (or §5.6's unload would refuse
    # to GC the lane over caches the integrator itself created), and touches
    # nothing that was there before — the `out/run-logs/` stream WI-359 names
    # must still block the unload.
    root = station_repo(tmp_path)
    wt = root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / "wi-401"
    logs = wt / "out" / "run-logs"
    logs.mkdir(parents=True)
    (logs / "session.md").write_text("the only copy\n", encoding="utf-8", newline="\n")

    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert (wt / "bar-cache").is_dir() is False, "the bar's own residue stays"
    assert (logs / "session.md").read_text(encoding="utf-8") == "the only copy\n"


# 5b.2-wi388 — the adjudication no-bar arm and the `bar` strictness key


def test_the_bar_key_reaches_check_gate(tmp_path):
    # WI-388 (5): an optional frontmatter `bar = G1|G2|G3` pins the lane's
    # verification strictness — the refresh passes it to check.py as --gate, so
    # a row claimed to deliver evidence at a level still bars at that level if
    # docs/gate moves mid-flight. Asserted off the recording stub's OWN argv.
    root = station_repo(tmp_path, bar="G2")
    wt = _lane(root, "wi-401")
    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    order = _order(wt)
    assert "--gate" in order and "G2" in order, order
    assert order.index("--gate") + 1 == order.index("G2")


def test_without_a_bar_key_the_refresh_passes_no_gate(tmp_path):
    # The complement, so the key cannot be mistaken for a default: an undeclared
    # bar leaves check.py on its own derived-gate read, exactly as before.
    root = station_repo(tmp_path)
    wt = _lane(root, "wi-401")
    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert "--gate" not in _order(wt)


def test_a_malformed_bar_value_refuses_the_refresh(tmp_path):
    # Fail closed and loud: a typo'd bar silently ignored would bar at whatever
    # docs/gate happens to read — the exact drift the key exists to pin. The
    # claimed spec lives on the branch, so the fix is a lane-side edit.
    root = station_repo(tmp_path, bar="G9")
    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert sha is None
    assert "bar" in refusal and "G9" in refusal


def test_an_adjudication_lane_runs_no_bar(tmp_path):
    # WI-388 (1): adjudication runs NO BAR (§A5.2) — its outputs are Status
    # cells and the work registry, nothing a product bar can speak to. The
    # refresh still merges trunk in and runs the trunk step, still commits a
    # verified Bar-Green attestation (the slot's contract), but the check
    # harness is never invoked and the summary says so.
    root = station_repo(tmp_path, safety="adjudication")
    wt = _lane(root, "wi-401")
    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert _order(wt) == ["trunk_step"], "the bar must not run for adjudication"
    attested = integ.refresh_attestation(root, "wi-401", sha)
    assert attested is not None
    assert "no-bar" in attested[1]
    ready, why = integ._merge_ready(root, "wi-401")
    assert ready and "no-bar" in why


def test_a_mixed_claim_still_runs_the_bar(tmp_path):
    # Fail toward the bar: the no-bar arm arms only when EVERY claimed spec is
    # the adjudication kind. A batch claim holding one ordinary row beside the
    # adjudication row bars as usual.
    root = claim_repo(tmp_path, safety="adjudication")
    write_spec(root, "queued", "WI-402", slug="extra", specref="seed.txt")
    (root / ".gitignore").write_text(
        "out/\nbar-cache/\n", encoding="utf-8", newline="\n"
    )
    (root / "docs" / "stack.ini").write_text(
        "[product]\ntest = {py} -m pytest -q\n", encoding="utf-8", newline="\n"
    )
    declare_generated(root)
    scripts = root / "scripts"
    scripts.mkdir(exist_ok=True)
    (scripts / "trunk_step.py").write_text(
        STUB_TRUNK_STEP, encoding="utf-8", newline="\n"
    )
    (scripts / "check.py").write_text(STUB_CHECK_GREEN, encoding="utf-8", newline="\n")
    _commit(root, "chore: the stub harness and the declared bar", when=T_CODE)
    assert integ.claim(root, ["WI-401", "WI-402"], "wi-401") == 0
    wt, err = integ.lane_worktree(root, "wi-401")
    assert err is None, err
    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert "check" in _order(wt)


# 5b.3 — the disposable-commit rule (§A2.1)


def test_a_second_refresh_replaces_the_first_and_never_stacks(tmp_path):
    # THE rule the determinism measurement forced. docs/log.md is APPEND-compiled
    # from docs/log.d/ fragments, so a second merge stacked on the first would
    # conflict on the file end — the exact failure §A2 exists to abolish. A retry
    # is therefore a reset to the last WORK commit and a fresh sequence: after
    # two refreshes the branch carries exactly ONE refresh commit, and its first
    # parent is still the work commit, not the previous refresh.
    root = station_repo(tmp_path)
    work_tip = _rev(root, "wi-401")
    first, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal

    (root / "trunk-moved.txt").write_text("x\n", encoding="utf-8", newline="\n")
    _commit(root, "docs: trunk moves, so the branch must refresh again", when=T_LATER)
    second, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal

    assert second != first
    assert _refresh_commits(root, "wi-401") == [second], "a refresh must not stack"
    assert _git(root, "rev-parse", second + "^1").strip() == work_tip
    assert integ._work_tip(root, "wi-401") == work_tip
    # The discarded first refresh is unreachable from the branch: nothing to
    # unpick, nothing to hand-merge.
    assert first not in _git(root, "rev-list", "wi-401").split()


def test_a_conflicting_trunk_merge_leaves_the_branch_at_its_work_commit(tmp_path):
    # The one place a conflict can still happen, and the lane owns it. What must
    # NOT happen is a parked half-merge: the branch is reset, the tree is clean,
    # MERGE_HEAD is gone, and the refusal says where to resolve it.
    root = station_repo(tmp_path)
    wt = root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / "wi-401"
    # Both sides edit the same line of the same file, from a common base.
    (wt / "contested.txt").write_text("branch side\n", encoding="utf-8", newline="\n")
    _commit(wt, "WI-401: the branch's take", when=T_VERDICT)
    (root / "contested.txt").write_text("trunk side\n", encoding="utf-8", newline="\n")
    _commit(root, "docs: the trunk's take", when=T_LATER)
    work_tip = _rev(root, "wi-401")

    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert sha is None
    assert "CONFLICTS" in refusal and str(wt) in refusal
    assert _rev(root, "wi-401") == work_tip
    assert _git(wt, "status", "--porcelain").strip() == ""
    assert integ.ac.git(wt, "rev-parse", "--verify", "--quiet", "MERGE_HEAD")[0] != 0


def test_a_red_refresh_bar_commits_nothing_and_leaves_the_branch_clean(tmp_path):
    # A red bar is the lane's to fix, so the branch goes back to where the lane
    # left it — no refresh commit, no attestation, and therefore no way for the
    # slot to merge it. The bar really ran (the stub recorded itself) before the
    # tree was restored.
    root = station_repo(tmp_path, check_src=STUB_CHECK_RED)
    wt = root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / "wi-401"
    work_tip = _rev(root, "wi-401")

    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert sha is None
    assert "the bar is RED on the refreshed tree" in refusal
    assert "bar exit 1" in refusal
    assert _rev(root, "wi-401") == work_tip
    assert _refresh_commits(root, "wi-401") == []
    assert _git(wt, "status", "--porcelain").strip() == ""
    ready, _why = integ._merge_ready(root, "wi-401")
    assert not ready


def test_a_red_refusal_carries_the_steps_own_output_and_names_the_kept_log(tmp_path):
    # WI-398, driven end-to-end. Two halves of one loss: (1) the refusal's
    # bounded tail must be the failing STEP's own output — not check.py's
    # closing summary re-print, which is all the WI-240 anchor could ever reach
    # on a full bar; (2) the undo below resets the very tree that produced the
    # evidence, so the FULL bar output must survive OUTSIDE the lane worktree,
    # at a path the refusal message itself names. The WI-387 red cost three
    # lost diagnoses of one failure because neither half held.
    root = station_repo(tmp_path, check_src=STUB_CHECK_RED)
    wt = _lane(root, "wi-401")

    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert sha is None
    # (1) the failing step's own output reached the refusal text ...
    assert "FAILED tests/test_widget.py::test_value" in refusal
    assert "  FAIL  tests+coverage" in refusal
    # ... and the summary re-print did not (the kept file holds it instead).
    assert "Check summary" not in refusal
    assert "RESULT: FAIL" not in refusal
    # (2) the message NAMES the retained full log, outside the lane worktree,
    # and the file really holds the WHOLE bar output — summary included.
    kept = root / "out" / "run-logs" / "refresh-refused-wi-401.log"
    assert str(kept) in refusal
    text = kept.read_text(encoding="utf-8")
    assert "FAILED tests/test_widget.py::test_value" in text
    assert "Check summary" in text and "RESULT: FAIL" in text
    # The evidence home survives the undo and leaves the lane clean: the next
    # refresh (or a hand rebuild) starts from the work tip, evidence in hand.
    assert _git(wt, "status", "--porcelain").strip() == ""
    assert _git(root, "status", "--porcelain").strip() == ""  # gitignored home


def test_the_refresh_refuses_rather_than_discard_uncommitted_lane_work(tmp_path):
    # The reset is what makes the retry safe, and it is also the one thing that
    # could destroy work. So the dirt check comes FIRST: a lane with uncommitted
    # changes is told to commit them, never reset over them.
    root = station_repo(tmp_path)
    wt = root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / "wi-401"
    (wt / "wi-401.txt").write_text("half-finished\n", encoding="utf-8", newline="\n")

    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert sha is None
    assert "is dirty" in refusal and "commit or stash it" in refusal
    assert (wt / "wi-401.txt").read_text(encoding="utf-8") == "half-finished\n"


# 5b.4 — the two requirements the owner's caveat produced


def test_slot_acquisition_has_exactly_one_call_site():
    # §A2.0 requirement 1, and it is a claim ABOUT THE SOURCE, so it is checked
    # against the source. "Restricting the design to pessimistic is a one-line
    # change" is only true while every refresh that happens inside the slot
    # happens under a lock taken in one place; a second acquisition site would
    # make that a rewrite, quietly, and nothing else would notice.
    src = (SCRIPTS / "integrate.py").read_text(encoding="utf-8")
    sites = [ln for ln in src.splitlines() if "acquire_lock(" in ln]
    assert len(sites) == 1, sites
    assert "def _slot(root)" in src
    # ...and it is inside `_slot`, not merely singular.
    body = src.split("def _slot(root):", 1)[1].split("\ndef ", 1)[0]
    assert "acquire_lock(" in body
    # And the SLOT, not just the lock call: counting `acquire_lock(` alone let
    # a second acquisition through the existing helper pass (REVIEW-A round 1
    # drove it — `_extra = _slot(root)` at the top of `integrate_one` was
    # green). `_slot(` must occur exactly twice: the definition and its one
    # call, so a second acquisition by EITHER route reds here.
    calls = [ln for ln in src.splitlines() if "_slot(" in ln]
    assert len(calls) == 2, calls
    assert any(ln.strip().startswith("def _slot(") for ln in calls), calls


def test_the_pessimistic_sequence_runs_when_a_lane_loses_the_race(tmp_path):
    # §A2.0 requirement 2: the one-lost-race fallback IS the pessimistic
    # sequence, and it must not be dead code. It is not, by CONSTRUCTION — this
    # is a two-branch drain, and merging the first moves trunk out from under the
    # second, so the second loses the race every single time. Both branches
    # refresh themselves first (the speculative half, as drive.py does it); only
    # the loser is re-refreshed, in the slot.
    root = station_repo(tmp_path)
    write_spec(root, "queued", "WI-402", slug="gadget", order=1, specref="seed.txt")
    _commit(root, "file WI-402", when=T_CODE)
    assert integ.claim(root, "WI-402", "wi-402") == 0
    close_branch(root, "wi-402", wi="WI-402", slug="gadget")

    for branch in ("wi-401", "wi-402"):
        _sha, refusal = integ.refresh(root, branch, "smoke")
        assert refusal is None, refusal
    assert integ.trunk_is_ancestor(root, "wi-401")
    assert integ.trunk_is_ancestor(root, "wi-402")

    proc = run_py([SCRIPTS / "integrate.py", "integrate", "--tier", "smoke"], cwd=root)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out

    # The winner merged on its speculative bar; the loser was named, refreshed
    # in the slot, and merged after — bar-time it would have paid anyway going
    # second, and nothing was reconciled because ancestry is all that moved.
    assert out.count("is not merge-ready") == 1, out
    assert "the pessimistic sequence" in out, out
    assert "wi-402 is not merge-ready" in out, out
    assert "integrate: wi-401 merged (WI-401=merged)" in out, out
    assert "integrate: wi-402 merged (WI-402=merged)" in out, out
    # Both landed, and the second composed ON TOP of the first — the Class C
    # coverage the deleted composed-tree bar used to buy, now free.
    tracked = _git(root, "ls-tree", "-r", "--name-only", "HEAD").split()
    assert "wi-401.txt" in tracked and "wi-402.txt" in tracked
    assert "wi-401" not in _branches(root) and "wi-402" not in _branches(root)


def test_a_branch_that_never_refreshed_is_refreshed_by_the_slot(tmp_path):
    # The degradation that makes the speculative half OPTIONAL: delete drive.py's
    # refresh call and the queue still works, one lane at a time, with the bar
    # inside the lock. That is the owner's caveat priced at one line — and it is
    # this path, so it is covered whether or not anyone ever exercises it.
    root = station_repo(tmp_path)
    assert integ.refresh_attestation(root, "wi-401") is None

    proc = run_py([SCRIPTS / "integrate.py", "integrate", "--tier", "smoke"], cwd=root)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "not a verified refresh commit" in out, out
    assert "integrate: wi-401 merged (WI-401=merged)" in out, out


def test_the_refresh_cli_is_the_lane_side_entry_point(tmp_path):
    # The seam drive.py and a worker share, exercised through the real CLI: one
    # operation, one branch, no slot taken. (`integrate` is the only operation
    # in this file that takes the slot — see the one-call-site test above.)
    root = station_repo(tmp_path)
    proc = run_py(
        [SCRIPTS / "integrate.py", "refresh", "--branch", "wi-401", "--tier", "smoke"],
        cwd=root,
    )
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "integrate: refreshed wi-401 onto trunk" in out, out
    assert integ.refresh_attestation(root, "wi-401")

    proc = run_py(
        [SCRIPTS / "integrate.py", "refresh", "--branch", "wi-999", "--tier", "smoke"],
        cwd=root,
    )
    assert proc.returncode != 0
    assert "cannot refresh wi-999" in proc.stdout + proc.stderr


# 5b.5 — the attestation is a BINDING, not a string (REVIEW-A round 1)
#
# Round 1 found the constraint's second half satisfiable by a message: any line
# starting with `Bar-Green:` made a branch merge-ready, so a forged trailer, a
# copied message and `commit --amend` all landed unbarred content on trunk, and
# the same unbound token drove a `reset --hard` that DELETED a work commit. Each
# of the four tests below is that exploit, kept as the regression.


FORGED_TRAILER = "Bar-Green: tree={t} work={w} bar PASS (2 steps, tier all)".format(
    t="0" * 40, w="1" * 40
)


def test_a_forged_bar_green_trailer_does_not_make_a_branch_merge_ready(tmp_path):
    # Exploit (a), three ways, because the fix has three independent checks and
    # a test that only drove one would let the other two rot. An ordinary
    # subject; the refresh SUBJECT with names that belong to nothing; and the
    # sharpest one — a genuine refresh commit's message COPIED verbatim onto a
    # different commit, which is what amend/rebase/cherry-pick do by accident.
    root = station_repo(tmp_path)
    wt = _lane(root, "wi-401")

    (wt / "sneaky.txt").write_text("unbarred\n", encoding="utf-8", newline="\n")
    _commit(wt, "WI-401: a perfectly ordinary work commit\n\n" + FORGED_TRAILER)
    ready, why = integ._merge_ready(root, "wi-401")
    assert not ready and "not a verified refresh commit" in why

    (wt / "sneaky.txt").write_text("still unbarred\n", encoding="utf-8", newline="\n")
    _commit(
        wt,
        "refresh: wi-401 onto trunk 0123456789\n\n" + FORGED_TRAILER,
        when=T_LATER,
    )
    assert integ.refresh_attestation(root, "wi-401") is None

    # Now a REAL refresh, then its whole message re-used on a new commit.
    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    genuine = _git(root, "log", "-1", "--format=%B", "wi-401")
    assert integ.refresh_attestation(root, "wi-401") is not None
    (wt / "carried.txt").write_text("rode in\n", encoding="utf-8", newline="\n")
    _commit(wt, genuine, when=T_LATER)
    assert integ.refresh_attestation(root, "wi-401") is None, (
        "a copied refresh message names another commit's tree and parent"
    )
    ready, _why = integ._merge_ready(root, "wi-401")
    assert not ready


def test_the_queue_refuses_to_land_a_forged_attestation_unbarred(tmp_path):
    # The exploit end to end, which is what made it MAJOR: round 1's
    # `integrate --tier smoke` exited 0 and put `sneaky.txt` on trunk with the
    # recording stub harness never invoked at all. Now the slot does not
    # believe the trailer, falls into its pessimistic arm, and the file only
    # reaches trunk AFTER a real bar ran on it.
    root = station_repo(tmp_path)
    wt = _lane(root, "wi-401")
    (wt / "sneaky.txt").write_text("unbarred\n", encoding="utf-8", newline="\n")
    _commit(wt, "WI-401: a perfectly ordinary work commit\n\n" + FORGED_TRAILER)
    assert _order(wt) == [], "no bar has run yet"

    proc = run_py([SCRIPTS / "integrate.py", "integrate", "--tier", "smoke"], cwd=root)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "not a verified refresh commit" in out, out
    # The bar DID run this time — the forgery bought nothing but a refresh.
    assert "trunk_step" in _order(wt) and "check" in _order(wt), out
    assert "sneaky.txt" in _git(root, "ls-tree", "-r", "--name-only", "HEAD")


def test_amending_a_refresh_commit_revokes_its_attestation(tmp_path):
    # Exploit (b): `commit --amend --no-edit` keeps the message while the tree
    # moves, so round 1 landed the amended-in file with the bar not re-run. The
    # trailer names the tree, so an amend that changes content cannot keep it.
    root = station_repo(tmp_path)
    wt = _lane(root, "wi-401")
    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    before = _git(root, "rev-parse", "wi-401^{tree}").strip()
    runs = len(_order(wt))

    (wt / "amended-in.txt").write_text("unbarred\n", encoding="utf-8", newline="\n")
    _git(wt, "add", "-A")
    _git(wt, "commit", "-q", "--amend", "--no-edit")
    assert _git(root, "rev-parse", "wi-401^{tree}").strip() != before

    assert integ.refresh_attestation(root, "wi-401") is None
    ready, why = integ._merge_ready(root, "wi-401")
    assert not ready and "not a verified refresh commit" in why
    # And end to end: the amended content still reaches trunk, but only through
    # a fresh bar — which is the correct outcome, not a refusal.
    proc = run_py([SCRIPTS / "integrate.py", "integrate", "--tier", "smoke"], cwd=root)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert len(_order(wt)) > runs, "the amended tree was barred before it merged"
    assert "amended-in.txt" in _git(root, "ls-tree", "-r", "--name-only", "HEAD")


def test_a_work_commit_that_quotes_the_trailer_is_never_peeled_away(tmp_path):
    # The data-loss half. `_work_tip` feeds a `reset --hard`, so peeling one
    # commit too far DESTROYS committed work: in round 1 a commit carrying
    # `Bar-Green: I ran it locally, honest` was peeled and its file left the
    # branch entirely. The peel now needs a commit that names its own tree and
    # parent, which no hand-written message can do by accident.
    root = station_repo(tmp_path)
    wt = _lane(root, "wi-401")
    (wt / "late.txt").write_text("real work\n", encoding="utf-8", newline="\n")
    _commit(wt, "WI-401: late fix\n\nBar-Green: I ran it locally, honest", when=T_LATER)
    tip = _rev(root, "wi-401")

    assert integ._work_tip(root, "wi-401") == tip, "an honest tip must not peel"
    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    tracked = _git(root, "ls-tree", "-r", "--name-only", "wi-401").split()
    assert "late.txt" in tracked, tracked
    # ...and the genuine refresh on top of it still peels back to exactly it.
    assert integ._work_tip(root, "wi-401") == tip


def test_the_refresh_sheds_its_residue_inside_a_directory_that_predates_it(tmp_path):
    # Round 1: `git status --ignored=matching` collapses an ignored directory to
    # ONE line at any -u setting, so a before/after line diff skipped the whole
    # directory when it already existed — and that is the NORMAL case, since the
    # worker builds in the same lane worktree the refresh then bars. Driven with
    # the directory pre-created, which the previous listing could not see into.
    root = station_repo(tmp_path)
    wt = _lane(root, "wi-401")
    (wt / "bar-cache").mkdir()
    (wt / "bar-cache" / "worker-run.txt").write_text(
        "the worker's, not ours\n", encoding="utf-8", newline="\n"
    )
    assert integ._worktree_dirt(wt) == ["!! bar-cache/"], "the collapsed listing"

    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert not (wt / "bar-cache" / "run.txt").exists(), "the refresh's own file"
    assert (wt / "bar-cache" / "worker-run.txt").is_file(), "the lane's own file"
    # The directory SURVIVES, because it still holds a file that predates the
    # refresh — and §5.6 will therefore still report this lane as dirty. That is
    # WI-359's rule working, and the refresh's promise is only that it added
    # nothing to the pile.
    assert (wt / "bar-cache").is_dir()


def test_an_empty_directory_that_predates_the_refresh_is_not_pruned(tmp_path):
    # REVIEW-A round 2. The prune has to exist — git DOES report an emptied
    # ignored directory (`!! bar-cache/`), so leaving one would make §5.6's
    # unload refuse over a directory the refresh had just emptied. But it
    # reached one step too far: an EMPTY directory that predates the refresh is
    # the lane's, and emptiness can be load-bearing — this repo's own
    # `docs/work/deferred/` is an empty untracked directory a link resolves
    # through. Driven with the directory pre-created and empty, which no git
    # listing can distinguish from one the bar made.
    root = station_repo(tmp_path)
    wt = _lane(root, "wi-401")
    (wt / "bar-cache").mkdir()  # pre-existing, EMPTY, ignored
    assert integ.ignored_files(wt) == set(), "git lists no file for an empty dir"

    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert not (wt / "bar-cache" / "run.txt").exists(), "the bar's file is shed"
    assert (wt / "bar-cache").is_dir(), "the lane's empty directory survives"


def test_a_directory_the_bar_itself_created_is_pruned(tmp_path):
    # The other answer, so the guard above is a rule with two outcomes rather
    # than a prune that never fires. Nothing pre-exists here, so `bar-cache/`
    # is the refresh's own and goes — otherwise git reports the emptied
    # directory and the merge exits nonzero over the integrator's own leavings.
    root = station_repo(tmp_path)
    wt = _lane(root, "wi-401")
    assert not (wt / "bar-cache").exists()

    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert not (wt / "bar-cache").exists(), "the refresh's own directory is shed"
    assert integ._worktree_dirt(wt) == [], "...so the lane reads clean to §5.6"


def test_a_deliberately_forged_attestation_is_a_STATED_limit_not_a_defence(tmp_path):
    # The honest bound, pinned so nobody re-reads the guarantee as stronger than
    # it is (REVIEW-A round 2 drove it). Naming the tree and the parent by hand
    # is four git invocations and no bar, and it VERIFIES — this test asserts the
    # limit rather than a defence, because the only structural closure is a
    # slot-side re-bar and DECISION 3 (owner ruling) deleted that outright.
    # If this test ever starts failing, the design changed: re-read §A2.0 and
    # `refresh_attestation`'s contract before "fixing" it.
    root = station_repo(tmp_path)
    wt = _lane(root, "wi-401")
    (wt / "never-barred.txt").write_text("no bar\n", encoding="utf-8", newline="\n")
    _git(wt, "add", "-A")
    tree = _git(wt, "write-tree").strip()
    parent = _rev(root, "wi-401")
    _git(
        wt,
        "-c",
        "commit.gpgsign=false",
        "commit",
        "-qm",
        "refresh: wi-401 onto trunk deadbeef01\n\n"
        "Bar-Green: tree={} work={} bar PASS (99 steps, tier all)".format(tree, parent),
    )

    assert integ.refresh_attestation(root, "wi-401") == (
        parent,
        "bar PASS (99 steps, tier all)",
    )
    ready, _why = integ._merge_ready(root, "wi-401")
    assert ready, "accepted BY DESIGN - the bound is accident, not intent"
    assert _order(wt) == [], "and no bar ever ran"


def test_a_cancelled_branch_merges_through_the_slot_owing_no_verdict(tmp_path):
    # The outcome keying, driven through the WHOLE slot rather than at the gate
    # helper: review-policy 1, no verdict artifact anywhere, and a lane whose
    # specs went to `cancelled/`. It merges — because the cancellation is a
    # trunk fact and the id stays retired, which is only true if the branch
    # lands. (`test_only_the_merged_outcome_owes_a_verdict` shows the same repo
    # shape refusing when the outcome is `merged`, so this is not vacuous.)
    root = station_repo(tmp_path, policy="1", dest="cancelled")

    assert integ.branch_outcomes(root, "wi-401") == ({"WI-401": "cancelled"}, [])
    assert integ.integrate(root, "smoke") == 0
    assert (root / "docs" / "work" / "cancelled" / "WI-401-widget.md").is_file()
    assert "wi-401" not in _branches(root)


def test_the_refresh_refuses_when_the_main_checkout_holds_the_branch(tmp_path):
    # Round 1: with the main checkout on the branch, `_head(root)` IS the branch,
    # so the refresh "merged trunk in" from itself, printed a trunk sha that was
    # the branch's own, and attested a composition that never happened. There is
    # no trunk to resolve while nothing has it checked out, so it refuses.
    root = station_repo(tmp_path)
    _git(root, "worktree", "remove", str(_lane(root, "wi-401")))
    (root / "trunk-moved.txt").write_text("x\n", encoding="utf-8", newline="\n")
    _commit(root, "docs: trunk moves", when=T_LATER)
    _git(root, "checkout", "-q", "wi-401")

    sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert sha is None
    assert "MAIN checkout" in refusal and "no trunk checked out" in refusal
    assert "checkout <trunk>" in refusal
    assert integ.refresh_attestation(root, "wi-401") is None
    assert not (root / "trunk-moved.txt").exists(), "nothing was merged in"


# 5b.6 — the refresh must not stale an honest verdict


def test_the_mechanical_refresh_does_not_stale_a_good_verdict(tmp_path):
    # A structural consequence of moving the bar onto the branch: the refresh is
    # the LAST commit before the merge, and it lands after the review by
    # construction. If it counted as "code", the RULING-7 freshness rule would
    # be unpassable for every WI. The refresh is peeled off (`_work_tip`) — and
    # the neighbouring stale-APPROVE tests are what prove this is an exclusion
    # rather than a broken comparison.
    root = station_repo(tmp_path)
    (root / "docs" / "review-policy").write_text("1\n", encoding="utf-8", newline="\n")
    _commit(root, "policy: require a verdict", when=T_CODE)
    wt = root.parent / (root.name + integ.LANE_WORKTREE_SUFFIX) / "wi-401"
    verdict = wt / "docs" / "reviews" / "WI-401-REVIEW-A.md"
    verdict.parent.mkdir(parents=True, exist_ok=True)
    verdict.write_text(VERDICT_APPROVE, encoding="utf-8", newline="\n")
    _commit(wt, "review: WI-401 REVIEW-A", when=T_LATER)
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None

    _sha, refusal = integ.refresh(root, "wi-401", "smoke")
    assert refusal is None, refusal
    assert integ._verdict_gate(root, "wi-401", {"WI-401": "merged"}) is None


# --- 6. end to end, against a REAL green bar ---------------------------------


E2E_DEMO_SRC = '''"""Demo pure core for the kit self-test. Pure — no I/O."""


def add(a, b):
    """Add two numbers. Implements: SR-001, LLR-001"""
    return a + b


def sub(a, b):
    """Subtract two numbers. Implements: SR-001, LLR-001"""
    return a - b
'''


def scaffolded_closed_branch(tmp_path):
    """A bootstrapped scaffold whose WI-401 is claimed, built and CLOSED on
    `wi-401`: exactly the state the queue runs against. Returns (repo, claim_sha).

    The bar this sets up for is REAL. `make_minimal_project` gives the scaffold a
    fully traced SN->SR->LLR->TC chain, so `check.py --trunk-lane` at the derived
    gate (G3) and the smoke tier genuinely passes on the refreshed branch —
    measured 17 PASS steps, zero SKIP. `_run_bar` is deliberately NOT stubbed by
    any caller: a monkeypatched bar would make every downstream assertion true of
    a queue that merges anything.

    Two fixture notes, each a real property of the script under test:

      * NO `.venv` is seeded. `agent_common.harness_python` prefers the repo's
        own `.venv` and falls back to `sys.executable`; a `seed_venv`-style
        `venv.create(with_pip=False)` interpreter carries neither pytest nor
        ruff, so it would red the format/lint/test steps of the very bar these
        tests need to pass honestly. The fallback lands on THIS suite's
        interpreter, which is floor-satisfying and carries the pinned tools.
      * `out/` is gitignored by the fixture. `integrate()` opens its coordinator
        lock at `out/integrate.lock` BEFORE checking the trunk is clean, and the
        shipped `gitignore.template` covers only `out/run-logs/` and
        `out/agent-loop.lock` — so on a stock scaffold the queue refuses itself
        as "dirty" on its own lock file (reported as a finding, not patched
        here).
    """
    skip_without_env_gates("git")
    repo = tmp_path / "repo"
    repo.mkdir()
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", repo], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    make_minimal_project(repo)

    (repo / "docs" / "review-policy").write_text("0\n", encoding="utf-8", newline="\n")
    with (repo / ".gitignore").open("a", encoding="utf-8", newline="\n") as fh:
        fh.write("out/\n")
    # A queued spec owes a resolving SpecRef (the WI-370 claim rung); the
    # scaffold's own docs/log.md serves. The closing move below CLEARS it,
    # because the closed form is what check_trajectory --strict sees on the
    # composed tree and R-F wants a terminal SpecRef empty.
    write_spec(repo, "queued", "WI-401", specref="docs/log.md")

    # The scaffold is committed as one seed on the default branch (bootstrap does
    # not init a repo), so the claim below is the FIRST thing the queue sees.
    _git(repo, "init", "-q")
    _git(
        repo, "symbolic-ref", "HEAD", "refs/heads/master"
    )  # local init.defaultBranch varies
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    _git(repo, "config", "commit.gpgsign", "false")
    _commit(repo, "seed: the scaffolded project", when=T_BASE)

    # 1. claim -> the trunk bookkeeping commit + the branch cut.
    proc = run_py(
        [
            SCRIPTS / "integrate.py",
            "--root",
            ".",
            "claim",
            "--wi",
            "WI-401",
            "--branch",
            "wi-401",
        ],
        cwd=repo,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    claim_sha = _rev(repo, "HEAD")

    # 2. the worker's branch: one product commit, then the closing move.
    _git(repo, "checkout", "-q", "wi-401")
    (repo / "src" / "demo.py").write_text(E2E_DEMO_SRC, encoding="utf-8", newline="\n")
    _commit(repo, "feat: subtract, verifying SR-001", when=T_CODE)
    # The closing move edits the spec the way a real close does: the file
    # lands in complete/ with its SpecRef cleared (R-F), not byte-moved.
    src = repo / "docs" / "work" / "active" / "wi-401" / "WI-401-widget.md"
    dst = repo / "docs" / "work" / "complete" / "WI-401-widget.md"
    dst.write_text(
        src.read_text(encoding="utf-8").replace('specref = "docs/log.md"\n', ""),
        encoding="utf-8",
        newline="\n",
    )
    _git(repo, "rm", "-q", "docs/work/active/wi-401/WI-401-widget.md")
    _commit(repo, "close: WI-401 -> complete", when=T_VERDICT)
    _git(repo, "checkout", "-q", "master")
    return repo, claim_sha


def test_claim_build_and_integrate_end_to_end(tmp_path):
    """The whole flow as a user runs it: scaffold -> claim -> build on the
    branch -> close -> `integrate --tier smoke`, against the REAL bar
    (`scaffolded_closed_branch` documents the fixture)."""
    repo, claim_sha = scaffolded_closed_branch(tmp_path)

    # 3. the queue.
    proc = run_py([SCRIPTS / "integrate.py", "integrate", "--tier", "smoke"], cwd=repo)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out

    # The bar really ran: a step count, at the tier asked for, with no SKIP.
    bar = re.search(r"bar PASS \((\d+) steps, tier smoke\)", out)
    assert bar, out
    assert int(bar.group(1)) >= 10, out
    assert "integrate: wi-401 merged (WI-401=merged)" in out, out
    assert "integrate: audit clean" in out, out

    # This branch never refreshed (nothing called it), so the slot said so and
    # ran the PESSIMISTIC sequence itself. That arm is on the ordinary path,
    # not an exotic one — which is exactly why it cannot rot (§A2.0).
    assert "is not merge-ready" in out, out
    assert "the pessimistic sequence" in out, out
    assert "integrate: refreshed wi-401 onto trunk" in out, out

    # The trunk advanced to a --no-ff MERGE of the branch onto the claim commit.
    parents = _git(repo, "rev-list", "--parents", "-n", "1", "HEAD").split()
    assert len(parents) == 3, parents
    assert parents[1] == claim_sha
    assert (
        _git(repo, "log", "-1", "--format=%s")
        .strip()
        .startswith("integrate: merge wi-401")
    )
    # ...and the merge's tree IS the branch tip's, byte for byte. That identity
    # is the whole reason the merge bar could be deleted: there is no composed
    # tree left to check, because the composition already happened at refresh.
    assert _git(repo, "rev-parse", "HEAD^{tree}") == _git(
        repo, "rev-parse", parents[2] + "^{tree}"
    )

    # The claim is released: the branch is gone and active/<branch>/ is empty in
    # the trunk's tree, with the spec closed by the branch's own closing move.
    assert "wi-401" not in _branches(repo)
    tracked = _git(repo, "ls-tree", "-r", "--name-only", "HEAD").split()
    assert not [p for p in tracked if p.startswith("docs/work/active/wi-401/")], tracked
    assert "docs/work/complete/WI-401-widget.md" in tracked
    # No integrator-owned worktree exists to tear down any more: the trunk is
    # the only registration left, and the lane the refresh used was GC'd by the
    # §5.6 unload rather than by a teardown of its own. (Trunk's side of this
    # merge asserted `CANDIDATE_BRANCH` was cleaned up; that constant and the
    # worktree it named are what this WI deleted, so the assertion is not
    # dropped to settle a conflict - it has no subject left.)
    assert not (tmp_path / "repo-integrate").exists()
    assert _worktree_count(repo) == 1
    assert _git(repo, "status", "--porcelain").strip() == ""


def test_integrate_is_a_noop_when_no_claimed_branch_has_finished(tmp_path):
    # The quiet steady state — the queue runs on a schedule, so "nothing to
    # merge" must be a cheap green, never a nonzero that would halt claiming.
    # Run as a SUBPROCESS: integrate() takes the process-global lock fd.
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    (root / ".gitignore").write_text("out/\n", encoding="utf-8", newline="\n")
    _commit(root, "chore: ignore the coordinator lock", when=T_VERDICT)

    proc = run_py([SCRIPTS / "integrate.py", "integrate"], cwd=root)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "no finished claimed branches" in out, out


def test_integrate_refuses_and_holds_the_trunk_when_the_bar_is_undeclared(tmp_path):
    # The §4 refusal reached through the real CLI, on a finished branch: the
    # queue would otherwise be free to merge, and a repo with no declared bar is
    # precisely where a fail-open merge does its damage. The trunk must not move.
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    # The fixture declares `[generated]` (see `declare_generated`), which is a
    # stack.ini — and THIS test is about the file being ABSENT, which is a
    # distinct §4 refusal from a stack.ini that declares no [product] test. So
    # it is removed here, after the claim that needed it, rather than the
    # assertion being softened to whichever refusal happens to fire.
    (root / "docs" / "stack.ini").unlink()
    (root / ".gitignore").write_text("out/\n", encoding="utf-8", newline="\n")
    _commit(root, "chore: ignore the coordinator lock", when=T_VERDICT)
    trunk_before = _rev(root, "HEAD")

    _git(root, "checkout", "-q", "wi-401")
    (root / "docs" / "work" / "complete").mkdir(parents=True, exist_ok=True)
    _git(
        root,
        "mv",
        "docs/work/active/wi-401/WI-401-widget.md",
        "docs/work/complete/WI-401-widget.md",
    )
    _commit(root, "close: WI-401 -> complete", when=T_LATER)
    _git(root, "checkout", "-q", "main")

    proc = run_py([SCRIPTS / "integrate.py", "integrate"], cwd=root)
    out = proc.stdout + proc.stderr
    assert proc.returncode != 0, out
    assert "docs/stack.ini is absent" in out, out
    assert _rev(root, "HEAD") == trunk_before
    assert "wi-401" in _branches(root)


# --- 7. the §5.6 unload: the branch AND its worker worktree (WI-359) ----------


def _worktree_count(root):
    """Registered worktrees, the trunk included (so a lone trunk counts 1)."""
    return len([ln for ln in _git(root, "worktree", "list").splitlines() if ln.strip()])


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
    # typically an IGNORED one — the unredacted `out/run-logs/` session stream, a
    # local `.env`. To a tracked-only read the worktree looks pristine and
    # `git worktree remove` deletes the lot without a word.
    repo = merged_branch_repo(tmp_path, ignore="out/\n.env\n")
    worker = tmp_path / "worker"
    _git(repo, "worktree", "add", str(worker), "wi-401")
    logs = worker / "out" / "run-logs"
    logs.mkdir(parents=True)
    (logs / "session.md").write_text(
        "the only copy of this session\n", encoding="utf-8", newline="\n"
    )

    # The tracked-only read really does see nothing — this is the trap, pinned.
    assert integ.ac.working_tree_dirty(worker) == []
    assert integ._worktree_dirt(worker), "an ignored-only worktree must read dirty"

    unloaded, note = integ._unload_branch(repo, "wi-401")
    assert not unloaded
    assert "UNLOAD INCOMPLETE" in note and "DIRTY" in note
    assert (logs / "session.md").read_text(encoding="utf-8") == (
        "the only copy of this session\n"
    )
    assert "wi-401" in _branches(repo)


# The 2026-08-01 drain's holding set, verbatim (docs/backlog-plan-2026-08-01.md
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


def test_the_shed_never_touches_an_ignored_stream_or_the_root_out(tmp_path):
    # Two boundaries at once. An ignored `out/run-logs/` session stream is
    # UNDECLARED — the 2026-07-26 lesson's canonical sole-copy file — so the
    # unload still refuses over it and the stream survives byte-for-byte. And
    # the shed operates only inside the lane: the repo-root `out/` (home of
    # WI-398's refresh-refused-<branch>.log, which lives OUTSIDE any lane
    # worktree) is never reached.
    repo, worker = residue_lane(tmp_path)
    stream = worker / "out" / "run-logs" / "session.md"
    stream.parent.mkdir(parents=True)
    stream.write_text("the only copy of this session\n", encoding="utf-8", newline="\n")
    root_log = repo / "out" / "run-logs" / "refresh-refused-wi-401.log"
    root_log.parent.mkdir(parents=True)
    root_log.write_text("refresh refused\n", encoding="utf-8", newline="\n")

    unloaded, note = integ._unload_branch(repo, "wi-401")
    assert not unloaded
    assert "UNLOAD INCOMPLETE" in note and "DIRTY" in note
    assert stream.read_text(encoding="utf-8") == "the only copy of this session\n"
    assert root_log.read_text(encoding="utf-8") == "refresh refused\n"
    assert "wi-401" in _branches(repo)


def test_the_declared_residue_set_is_exactly_the_bars_own_leavings():
    # The declaration, stated as data: every measured 2026-08-01 path is
    # declared residue; every name that CAN hold sole-copy evidence is not.
    for rel in MEASURED_RESIDUE:
        assert integ._is_declared_residue(rel), rel
    # Widened on measurement, the WI-400 scope guard working as designed:
    # check.py passes --html to its trace step at G2/G3, so the DECLARED bar
    # writes docs/test/report.html in whatever lane it runs in, and on
    # 2026-08-02 the wi-402 lane was measured holding exactly that file at
    # unload. Same class as report.md — rebuilt by the next bar run, sole-copy
    # evidence never (WI-407, REVIEW-A finding 2).
    assert integ._is_declared_residue("docs/test/report.html")
    for rel in (
        "out/run-logs/session.md",
        ".env",
        "orphan.txt",
        "docs/test/notes.md",
        "src/widget.pyc",
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
    monkeypatch.setattr(os, "name", "posix")
    assert integ.ignored_files(Path("unused")) == {
        "x\\__pycache__\\evil.pyc",
        "sub/cache.pyc",
    }
    monkeypatch.setattr(os, "name", "nt")
    assert integ.ignored_files(Path("unused")) == {
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


def test_the_git_dependency_is_declared_for_this_module():
    # This suite drives real repositories end to end; without git on PATH every
    # test above would SKIP and the module would still print a green. The
    # declared gate (conftest.ENV_GATES) is what makes that skip COUNTED in the
    # terminal summary rather than invisible (WI-326).
    assert shutil.which("git"), "the module-level env gate should have skipped"


# --- the bar step count is honest (WI-377) ------------------------------------


def test_bar_step_count_is_by_distinct_name_not_by_echoed_line():
    # Under --jobs each step's status line prints TWICE (the lane runner as it
    # finishes, then the final summary block), so a line count reported a
    # 20-step bar as ""bar PASS (40 steps)"" - a false measurement in the
    # merge record (WI-377). The count is by DISTINCT step name, so the
    # --jobs N output (doubled lines) and the --jobs 1 output (single lines)
    # of the same plan report the SAME step count.
    lane_echo = (
        "  PASS  format           0.1s\n"
        "  PASS  lint             0.2s\n"
        "  PASS  tests+coverage   61.0s\n"
    )
    summary = (
        "=" * 56 + "\n"
        "  PASS  format           0.1s\n"
        "  PASS  lint             0.2s\n"
        "  PASS  tests+coverage   61.0s\n"
    )
    jobs_n = lane_echo + summary  # every line twice, the --jobs shape
    jobs_1 = summary  # the serial shape
    assert integ._passed_steps(jobs_n) == integ._passed_steps(jobs_1)
    assert len(integ._passed_steps(jobs_n)) == 3
    # A FAIL/SKIP line never counts as a pass, and a malformed PASS line
    # (no name field) cannot crash the read.
    mixed = jobs_n + "  FAIL  dupes  exit 1 (0.1s)\n  SKIP  okf  absent\nPASS\n"
    assert len(integ._passed_steps(mixed)) == 3
