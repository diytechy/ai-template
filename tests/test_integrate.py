"""integrate.py — the local integrator, a serial fail-closed merge queue.

The Phase 4 backend of the one integration flow (docs/concurrency-restructure.md
§1.2): branch -> change request -> required checks on the composed tree -> merge.
This module pins the four gates that make it *fail-closed*, plus the whole flow
end-to-end:

  * **claim** (§2.3 steps 1+2) — the serial trunk move `queued/ ->
    active/<branch>/` and the branch cut from that commit, and the six refusals
    that stand in front of it: the tracked pause (§5.6), a dirty trunk, a branch
    that already exists, a branch name that would not map to a flat claim
    directory, a spec whose `safety_class` is not `ordinary` (spine runs
    attended as the §3.2 barrier), and a WI that is not on the scheduler's ready
    frontier.
  * **finished-branch detection** — the closing commit's move to `archive/` IS
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
):
    """One work-item spec in the format `scripts/wi_convert.py` emits (the
    tests/test_wi_folder_loaders.py `spec_text` shape).

    The `## Deliverable` body is written by DEFAULT because the archived form is
    the one that has to survive `check_trajectory` on the composed tree: R-A
    errors on a `status=done` WI with an empty Deliverable, and `archive/` is
    where every claimed spec ends up."""
    lines = [
        'id = "{}"'.format(wid),
        'title = "{}"'.format(title),
        'workstream = "ws"',
        'sr_refs = ["SR-001"]',
        "needs = [{}]".format(", ".join('"{}"'.format(n) for n in needs)),
        'safety_class = "{}"'.format(safety),
        "order = {}".format(order),
    ]
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
    no docs/requirements/work-items.csv is needed at all)."""
    git_repo(tmp_path, branch=branch)
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


def test_claim_refuses_a_wi_that_is_not_on_the_ready_frontier(tmp_path, capsys):
    # Readiness is DERIVED by schedule.py from the registry, never asserted by
    # the claimer: WI-401 hard-needs WI-999, which is still queued, so WI-401 is
    # `waiting` and claiming it would start work against an unbuilt dependency.
    root = git_repo(tmp_path)
    write_spec(tmp_path, "queued", "WI-401", needs=["WI-999"])
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


# --- 2. finished-branch detection: the tree IS the signal ---------------------


def test_finished_is_the_move_to_archive_not_a_state_file(tmp_path):
    # §2.3 step 3. A claimed branch is finished exactly when its TIP holds no
    # spec under active/<branch>/ — the closing commit's move to archive/ is the
    # whole signal, so there is no state file to go stale and no ref to leak.
    root = claim_repo(tmp_path)
    assert integ.claim(root, "WI-401", "wi-401") == 0

    # Claimed but still in flight: the spec is right where the claim put it.
    assert integ.finished_branches(root) == []

    _git(root, "checkout", "-q", "wi-401")
    (root / "docs" / "work" / "archive").mkdir(parents=True, exist_ok=True)
    _git(
        root,
        "mv",
        "docs/work/active/wi-401/WI-401-widget.md",
        "docs/work/archive/WI-401-widget.md",
    )
    _commit(root, "close: WI-401 -> archive", when=T_VERDICT)
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
    (root / "docs" / "work" / "archive").mkdir(parents=True, exist_ok=True)
    _git(
        root,
        "mv",
        "docs/work/active/wi-401/WI-401-widget.md",
        "docs/work/archive/WI-401-widget.md",
    )
    _commit(root, "close: WI-401 -> archive", when=T_VERDICT)
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


def test_claim_build_and_integrate_end_to_end(tmp_path):
    """The whole flow as a user runs it: scaffold -> claim -> build on the
    branch -> close -> `integrate --tier smoke`.

    The bar is REAL. `make_minimal_project` gives the scaffold a fully traced
    SN->SR->LLR->TC chain, so `check.py` at the derived gate (G3) and the smoke
    tier genuinely passes on the composed tree — measured 17 PASS steps, zero
    SKIP. `_run_bar` is deliberately NOT stubbed: a monkeypatched bar would make
    every assertion below true of a queue that merges anything.

    Two fixture notes, each a real property of the script under test:

      * NO `.venv` is seeded. `agent_common.harness_python` prefers the repo's
        own `.venv` and falls back to `sys.executable`; a `seed_venv`-style
        `venv.create(with_pip=False)` interpreter carries neither pytest nor
        ruff, so it would red the format/lint/test steps of the very bar this
        test needs to pass honestly. The fallback lands on THIS suite's
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
    write_spec(repo, "queued", "WI-401")

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
    _git(
        repo,
        "mv",
        "docs/work/active/wi-401/WI-401-widget.md",
        "docs/work/archive/WI-401-widget.md",
    )
    _commit(repo, "close: WI-401 -> archive", when=T_VERDICT)
    _git(repo, "checkout", "-q", "master")

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
    # the trunk's tree, with the spec archived by the branch's own closing move.
    assert "wi-401" not in _branches(repo)
    tracked = _git(repo, "ls-tree", "-r", "--name-only", "HEAD").split()
    assert not [p for p in tracked if p.startswith("docs/work/active/wi-401/")], tracked
    assert "docs/work/archive/WI-401-widget.md" in tracked
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
    (root / "docs" / "work" / "archive").mkdir(parents=True, exist_ok=True)
    _git(
        root,
        "mv",
        "docs/work/active/wi-401/WI-401-widget.md",
        "docs/work/archive/WI-401-widget.md",
    )
    _commit(root, "close: WI-401 -> archive", when=T_LATER)
    _git(root, "checkout", "-q", "main")

    proc = run_py([SCRIPTS / "integrate.py", "integrate"], cwd=root)
    out = proc.stdout + proc.stderr
    assert proc.returncode != 0, out
    assert "docs/stack.ini is absent" in out, out
    assert _rev(root, "HEAD") == trunk_before
    assert "wi-401" in _branches(root)


def test_the_git_dependency_is_declared_for_this_module():
    # This suite drives real repositories end to end; without git on PATH every
    # test above would SKIP and the module would still print a green. The
    # declared gate (conftest.ENV_GATES) is what makes that skip COUNTED in the
    # terminal summary rather than invisible (WI-326).
    assert shutil.which("git"), "the module-level env gate should have skipped"
