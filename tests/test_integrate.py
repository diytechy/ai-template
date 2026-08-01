"""integrate.py — the local integrator, a serial fail-closed merge queue.

The Phase 4 backend of the one integration flow (docs/concurrency-restructure.md
§1.2): branch -> change request -> required checks on the composed tree -> merge.
This module pins the four gates that make it *fail-closed*, plus the whole flow
end-to-end:

  * **claim** (§2.3 steps 1+2) — the serial trunk move `queued/ ->
    active/<branch>/` and the branch cut from that commit, and the eight refusals
    that stand in front of it: the tracked pause (§5.6), a dirty trunk, a branch
    that already exists, a branch name that would not map to a flat claim
    directory, a spec whose `safety_class` is not `ordinary` (spine runs
    attended as the §3.2 barrier), (WI-370) a spec whose `SpecRef` is empty or
    does not resolve in-repo — the R-E debt that becomes unpayable once the
    closing branch exists, hoisted the same way R-D was — a WI that is not on
    the scheduler's ready frontier, and (WI-358) a claimed id named in
    hand-authored `docs/status.md` prose — the forward-only debt that would
    red R-D on the composed tree at close, hoisted to where a single trunk
    commit can still pay it.
  * **finished-branch detection** — the closing commit's move to `complete/` IS
    the finished signal: no state file, no ref, just the tree.
  * **the verdict gate** (RULING-7) — the dialed review artifact must be
    present, must parse as APPROVE, and must be FRESH: a verdict whose last
    commit predates a later code commit on the branch is a stale APPROVE and
    does not clear the gate. Fragment (`docs/log.d/`) and review commits are
    excluded from "code", so bookkeeping cannot stale a good verdict.
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
passes on the composed tree. `_run_bar` is never monkeypatched — a stubbed bar is
exactly the vacuous green this script exists to make impossible.
"""

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
    _commit(tmp_path, "file " + wi, when=T_CODE)
    return tmp_path


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


def test_claim_refuses_a_spec_that_is_not_safety_class_ordinary(tmp_path, capsys):
    # §3.2: a spine work item is a BARRIER, not a lane — it excludes all other
    # work and runs attended, solo. The integrator claims `ordinary` only, and
    # says which class it saw so the refusal is actionable.
    root = claim_repo(tmp_path, safety="spine")

    assert integ.claim(root, "WI-401", "wi-401") == 1
    err = capsys.readouterr().err
    assert "WI-401 is safety_class='spine'" in err
    assert "claims ordinary work only" in err
    assert (root / "docs" / "work" / "queued" / "WI-401-widget.md").is_file()
    assert "wi-401" not in _branches(root)


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
    assert integ._verdict_gate(root, "wi-401", ["WI-401"]) is None


def test_a_required_verdict_absent_from_the_branch_refuses_by_name(tmp_path):
    # Fail-closed and ACTIONABLE: the refusal names the exact path the branch
    # must carry, so the remedy needs no lookup.
    root = verdict_repo(tmp_path, policy="1")
    refusal = integ._verdict_gate(root, "wi-401", ["WI-401"])
    assert refusal is not None
    assert "docs/reviews/WI-401-REVIEW-A.md" in refusal
    assert "absent from wi-401" in refusal


def test_a_changes_requested_verdict_refuses(tmp_path):
    # Present is not enough — the machine line is PARSED (score_reviews), so a
    # verdict that asked for changes cannot clear the gate by existing.
    root = verdict_repo(tmp_path, policy="1")
    write_verdict(root, VERDICT_CHANGES, when=T_VERDICT)

    refusal = integ._verdict_gate(root, "wi-401", ["WI-401"])
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

    refusal = integ._verdict_gate(root, "wi-401", ["WI-401"])
    assert refusal is not None
    assert "predates the branch's last code commit" in refusal


def test_an_approve_committed_after_the_last_code_commit_passes(tmp_path):
    # The green path of the same rule — asserted alongside the stale case above
    # so the freshness comparison is proven to have two answers, not one.
    root = verdict_repo(tmp_path, policy="1")
    write_verdict(root, VERDICT_APPROVE, when=T_VERDICT)
    assert integ._verdict_gate(root, "wi-401", ["WI-401"]) is None


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

    assert integ._verdict_gate(root, "wi-401", ["WI-401"]) is None


def test_a_malformed_review_policy_fails_closed(tmp_path):
    # A dial nobody can parse must never read as "0 = no review required". The
    # refusal quotes what it read, because the typo is the whole diagnosis.
    root = verdict_repo(tmp_path, policy="sometimes")
    refusal = integ._verdict_gate(root, "wi-401", ["WI-401"])
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


# --- 4b. the composed tree's own harness (WI-368) -----------------------------


def test_the_composed_trees_copy_wins_under_the_invokers_layout(tmp_path, monkeypatch):
    # The meta-repo shape: the invoker sits INSIDE --root, and the candidate
    # carries the same relative layout — the candidate's copy must win, or a
    # branch that changed a generator is regenerated with the trunk's vintage
    # and refused by the merge commit's own freshness floor (the WI-368 hit).
    root = tmp_path / "root"
    inv = root / "kit" / "scripts"
    inv.mkdir(parents=True)
    (inv / "trunk_step.py").write_text("# invoker\n", encoding="utf-8", newline="\n")
    monkeypatch.setattr(integ, "SCRIPTS", inv)
    wt = tmp_path / "candidate"
    cand = wt / "kit" / "scripts"
    cand.mkdir(parents=True)
    (cand / "trunk_step.py").write_text("# composed\n", encoding="utf-8", newline="\n")
    got = integ._composed_tree_script(wt, root, "trunk_step.py")
    assert got == cand / "trunk_step.py"


def test_an_out_of_root_invoker_probes_the_known_layouts(tmp_path, monkeypatch):
    # The kit-source-against-a-scaffold shape (this suite's own e2e fixtures):
    # SCRIPTS is not under --root, so the relative-layout join cannot apply and
    # the scaffold's scripts/ copy is found by the known-layout probe.
    inv = tmp_path / "elsewhere" / "scripts"
    inv.mkdir(parents=True)
    (inv / "check.py").write_text("# invoker\n", encoding="utf-8", newline="\n")
    monkeypatch.setattr(integ, "SCRIPTS", inv)
    wt = tmp_path / "candidate"
    (wt / "scripts").mkdir(parents=True)
    (wt / "scripts" / "check.py").write_text(
        "# composed\n", encoding="utf-8", newline="\n"
    )
    got = integ._composed_tree_script(wt, tmp_path / "repo", "check.py")
    assert got == wt / "scripts" / "check.py"


def test_a_candidate_without_the_script_falls_back_to_the_invoker(
    tmp_path, monkeypatch
):
    # A candidate that predates the script (or carries no harness at all) must
    # still integrate: the invoker's copy is the declared fallback, not a crash
    # and not a silent skip.
    inv = tmp_path / "elsewhere" / "scripts"
    inv.mkdir(parents=True)
    (inv / "trunk_step.py").write_text("# invoker\n", encoding="utf-8", newline="\n")
    monkeypatch.setattr(integ, "SCRIPTS", inv)
    wt = tmp_path / "candidate"
    wt.mkdir()
    got = integ._composed_tree_script(wt, tmp_path / "repo", "trunk_step.py")
    assert got == inv / "trunk_step.py"


def test_run_trunk_step_executes_the_composed_trees_copy(tmp_path, monkeypatch):
    # The seam itself, non-vacuous against the pre-fix wiring: the invoker's
    # copy exits 3, the composed tree's writes a sentinel — so a pass proves
    # WHICH copy ran, not merely that something exited 0.
    inv = tmp_path / "elsewhere" / "scripts"
    inv.mkdir(parents=True)
    (inv / "trunk_step.py").write_text(
        "import sys\n\nsys.exit(3)\n", encoding="utf-8", newline="\n"
    )
    monkeypatch.setattr(integ, "SCRIPTS", inv)
    root = tmp_path / "repo"
    root.mkdir()
    wt = tmp_path / "candidate"
    (wt / "scripts").mkdir(parents=True)
    (wt / "scripts" / "trunk_step.py").write_text(
        'from pathlib import Path\n\nPath("sentinel.txt").write_text("composed\\n")\n',
        encoding="utf-8",
        newline="\n",
    )
    code, out = integ._run_trunk_step(wt, root)
    assert code == 0, out
    assert (wt / "sentinel.txt").read_text(encoding="utf-8") == "composed\n"


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
    fully traced SN->SR->LLR->TC chain, so `check.py` at the derived gate (G3) and
    the smoke tier genuinely passes on the composed tree — measured 17 PASS steps,
    zero SKIP. `_run_bar` is deliberately NOT stubbed by any caller: a
    monkeypatched bar would make every downstream assertion true of a queue that
    merges anything.

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
    assert "integrate: wi-401 merged (WI-401)" in out, out
    assert "integrate: audit clean" in out, out

    # The trunk advanced to a --no-ff MERGE of the branch onto the claim commit.
    parents = _git(repo, "rev-list", "--parents", "-n", "1", "HEAD").split()
    assert len(parents) == 3, parents
    assert parents[1] == claim_sha
    assert (
        _git(repo, "log", "-1", "--format=%s")
        .strip()
        .startswith("integrate: merge wi-401")
    )

    # The claim is released: the branch is gone and active/<branch>/ is empty in
    # the trunk's tree, with the spec closed by the branch's own closing move.
    assert "wi-401" not in _branches(repo)
    tracked = _git(repo, "ls-tree", "-r", "--name-only", "HEAD").split()
    assert not [p for p in tracked if p.startswith("docs/work/active/wi-401/")], tracked
    assert "docs/work/complete/WI-401-widget.md" in tracked
    # ...and the candidate worktree is torn down rather than left lying around.
    assert integ.CANDIDATE_BRANCH not in _branches(repo)
    assert not (tmp_path / "repo-integrate" / "candidate").exists()
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


def merged_branch_repo(tmp_path, ignore=None):
    """A trunk that has just merged `wi-401` --no-ff — the exact state
    `integrate_one` reaches immediately before it unloads the branch.

    `ignore` (a .gitignore body) is committed BEFORE the branch cut, so the rules
    are live on `wi-401` too: a worktree checked out from a branch that predates
    the .gitignore sees those paths as untracked, which would test the wrong
    read entirely."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git_repo(repo)
    if ignore:
        (repo / ".gitignore").write_text(ignore, encoding="utf-8", newline="\n")
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

    assert "integrate: wi-401 merged (WI-401)" in out, out
    assert "GC'd clean worker worktree" in out, out
    assert not worker.exists(), out
    assert "wi-401" not in _branches(repo)
    # The integrator's own candidate worktree is torn down too, so the trunk is
    # the only registration left — the drained-and-unloaded stop, in full.
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
    (worker / "orphan.txt").write_text(
        "the only copy\n", encoding="utf-8", newline="\n"
    )

    proc = run_py([SCRIPTS / "integrate.py", "integrate", "--tier", "smoke"], cwd=repo)
    out = proc.stdout + proc.stderr
    assert proc.returncode != 0, out
    assert "integrate: wi-401 merged (WI-401)" in out, out

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
