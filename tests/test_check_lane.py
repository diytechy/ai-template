"""check.py's TRUNK-LANE rule: generated-artifact freshness gates run on the
trunk only (docs/concurrency-restructure.md §5.2).

Work branches never commit generated artifacts — the trunk regenerates them in
one serial post-merge step — so freshness-gating a branch would red it for drift
it is forbidden to fix. This module pins the two halves of that rule:

  1. `_work_branch` — who counts as a claimed work branch, and (louder) who does
     NOT. The detector is fail-CLOSED: every uncertain answer is None, which
     means the full strict bar applies. A regression that made it answer
     truthily by accident would silently switch the freshness gates OFF on the
     trunk, and nothing else in the suite would notice.
  2. The skip itself — exactly the seven trunk-derived freshness steps, never
     `skills-sync` (hand-authored source on both sides) and never the registry /
     DAG / navigability gates that grade the branch's own edits.
  3. `--trunk-lane`, its one deliberate exception (WI-386). The rule rests on "a
     work branch never commits a generated artifact", which the station refresh
     (docs/concurrency-v2.md §A2) makes false for exactly one commit: it merges
     trunk in, regenerates ON the branch, and bars the result — a tree that is
     byte-identical to the one the merge produces, so it owes the trunk lane's
     gates. Opt-IN, so a caller that forgets the flag gets the stricter-for-the-
     trunk answer this module's fail-closed direction already prefers.
"""

import os
import shutil
import subprocess
import sys

import pytest
from conftest import SCRIPTS, load_script, pin_autocrlf, run_py, skip_without_env_gates

# The exact notice contract §5.2 asks for, restated once here rather than at each
# assertion — a test that spelled it out five times would be five places to edit.
NOTICE = (
    "{step}: skipped (work branch '{branch}' — generated freshness is the "
    "trunk lane's, concurrency-restructure §5.2)"
)

# A command that CANNOT pass. Every "was it skipped?" assertion below runs a step
# whose command would fail, so a skip is proven by the absence of the failure —
# not merely by a green that a vacuous check would also produce.
FAILING = [sys.executable, "-c", "raise SystemExit(1)"]


@pytest.fixture
def check():
    """check.py imported in-process, with its per-process work-branch memo
    cleared. The memo is deliberately never invalidated in production (one git
    call per run); tests move between fixture repos, so they clear it."""
    mod = load_script("check")
    mod._WORK_BRANCH_CACHE.clear()
    return mod


def git_repo(root, branch="main"):
    """A committed git repo on `branch`. `git init -b` is 2.28+, so the branch is
    set with a symbolic-ref instead — that works on every git the kit supports and
    is exactly the ref `_work_branch` reads. `conftest.pin_autocrlf` neutralizes
    the box's `core.autocrlf` (WI-461/WI-465; see its docstring)."""
    skip_without_env_gates("git")
    git = shutil.which("git")

    def run_git(*args):
        proc = subprocess.run(
            [git, "-C", str(root), *args], capture_output=True, text=True
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        return proc.stdout

    run_git("init")
    pin_autocrlf(root)
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    run_git("symbolic-ref", "HEAD", "refs/heads/" + branch)
    (root / "seed.txt").write_text("seed", encoding="utf-8")
    run_git("add", "-A")
    run_git("commit", "-qm", "seed")
    return run_git


def claim(root, branch):
    """Claim `branch` the Phase 2c way (§2.1/§2.3): its work-item specs live in
    docs/work/active/<branch>/. The directory IS the claim."""
    d = root / "docs" / "work" / "active" / branch
    d.mkdir(parents=True)
    (d / "WI-999-demo.md").write_text('+++\nid = "WI-999"\n+++\n', encoding="utf-8")
    return d


def close(root, branch):
    """§2.3 step 3: the close MOVES the specs to docs/work/complete/ and leaves no
    active/<branch>/ behind — including the rmdir the WI-357 workaround relied on
    nobody doing. After this the working tree carries no claim at all."""
    src = root / "docs" / "work" / "active" / branch
    dst = root / "docs" / "work" / "complete"
    dst.mkdir(parents=True, exist_ok=True)
    for spec in src.iterdir():
        spec.rename(dst / spec.name)
    src.rmdir()


# --- 1. the detector ---------------------------------------------------------


def test_off_git_is_not_a_work_branch(check, tmp_path):
    # No repo at all: the answer must be None, i.e. the STRICT bar. An adopter
    # running the harness from an unpacked tarball gets the full checks.
    claim(tmp_path, "main")  # even a claim dir cannot make it truthy off-git
    assert check._work_branch(tmp_path) is None


def test_trunk_branch_without_a_claim_is_not_a_work_branch(check, tmp_path):
    # The trunk is simply the branch nobody claimed a work item on — there is no
    # trunk NAME anywhere in the rule, so a repo whose trunk is `develop` or
    # `trunk` needs no configuration.
    git_repo(tmp_path, branch="main")
    claim(tmp_path, "wi-360-forge-seam")  # some OTHER branch's claim
    assert check._work_branch(tmp_path) is None


def test_claimed_branch_is_detected(check, tmp_path):
    git_repo(tmp_path, branch="wi-360-forge-seam")
    claim(tmp_path, "wi-360-forge-seam")
    assert check._work_branch(tmp_path) == "wi-360-forge-seam"


def test_slashed_branch_name_maps_to_its_nested_claim_dir(check, tmp_path):
    # Branch names carry '/'. It is a PATH separator here, not a character to
    # mangle: `feat/x` is claimed by docs/work/active/feat/x/ and nothing else.
    git_repo(tmp_path, branch="feat/x")
    claim(tmp_path, "feat/x")
    assert check._work_branch(tmp_path) == "feat/x"


def test_slashed_branch_needs_the_nested_dir_not_a_flattened_one(check, tmp_path):
    git_repo(tmp_path, branch="feat/x")
    claim(tmp_path, "feat-x")  # a flattened name is NOT the claim
    assert check._work_branch(tmp_path) is None


def test_the_closing_commit_does_not_un_claim_its_own_branch(check, tmp_path):
    # WI-357, hit three times in the Phase 4 acceptance. The close commit stages
    # active/<branch>/ -> complete/, so at the moment its own pre-commit bar runs
    # the working tree holds no claim and the trunk-freshness gates re-arm inside
    # the very commit that closes the WI — demanding artifacts §5.2 forbids the
    # branch to commit. The signal has to outlive the move, and history does.
    run_git = git_repo(tmp_path, branch="wi-360")
    claim(tmp_path, "wi-360")
    run_git("add", "-A")
    run_git("commit", "-qm", "claim: WI-999 -> active/wi-360")
    close(tmp_path, "wi-360")
    run_git("add", "-A")  # staged, uncommitted: exactly what the hook sees
    assert check._work_branch(tmp_path) == "wi-360"


def test_a_commit_after_the_close_still_reads_as_a_work_branch(check, tmp_path):
    # And it stays claimed afterwards: a review fixup or a log tweak pushed on the
    # same branch is still the branch's lane, not the trunk's. Once the close is
    # COMMITTED the claim exists nowhere but history, so this is the case a
    # HEAD-tree-only signal would still get wrong.
    run_git = git_repo(tmp_path, branch="wi-360")
    claim(tmp_path, "wi-360")
    run_git("add", "-A")
    run_git("commit", "-qm", "claim: WI-999 -> active/wi-360")
    close(tmp_path, "wi-360")
    run_git("add", "-A")
    run_git("commit", "-qm", "WI-999: close")
    (tmp_path / "after.txt").write_text("fixup", encoding="utf-8")
    run_git("add", "-A")
    run_git("commit", "-qm", "WI-999: review fixup")
    assert check._work_branch(tmp_path) == "wi-360"


def test_trunk_history_full_of_other_branches_claims_is_still_the_trunk(
    check, tmp_path
):
    # The realistic trunk: every merged WI left both its claim add and its close
    # move in trunk history. None of that names the TRUNK's own branch, so the
    # history signal must stay silent. This is the fail-direction that matters —
    # a false positive here switches the freshness gates off on the one branch
    # that owns regenerating them, and nothing else would catch the drift.
    run_git = git_repo(tmp_path, branch="main")
    claim(tmp_path, "wi-360-forge-seam")
    run_git("add", "-A")
    run_git("commit", "-qm", "claim: WI-360 -> active/wi-360-forge-seam")
    close(tmp_path, "wi-360-forge-seam")
    run_git("add", "-A")
    run_git("commit", "-qm", "WI-360: close")
    assert check._work_branch(tmp_path) is None


def test_detached_head_is_not_a_work_branch(check, tmp_path):
    # `symbolic-ref` fails on a detached HEAD (a bisect, a CI checkout of a SHA).
    # Fail-closed: full checks, never a silent free pass.
    run_git = git_repo(tmp_path, branch="wi-360")
    claim(tmp_path, "wi-360")
    sha = run_git("rev-parse", "HEAD").strip()
    run_git("checkout", "-q", "--detach", sha)
    assert check._work_branch(tmp_path) is None


def test_dotdot_in_a_branch_name_is_refused_loudly(check, tmp_path, capsys):
    # git's own ref rules forbid `..`, so reaching this branch means something
    # is feeding check.py a fake ref. It is a path traversal into whatever sits
    # above docs/work/active/, so it is refused — and said out loud, because a
    # silent refusal here looks identical to an ordinary trunk run.
    claim(tmp_path, "x")
    check._git_out = lambda root, args: "../../x\n"
    assert check._work_branch(tmp_path) is None
    assert "implausible branch name" in capsys.readouterr().err


def test_work_branch_is_memoized_per_process(check, tmp_path):
    # ~15 steps in a --gate run, each asking. Without the memo that is 15 git
    # subprocesses per check run, on every commit.
    git_repo(tmp_path, branch="wi-360")
    claim(tmp_path, "wi-360")
    assert check._work_branch(tmp_path) == "wi-360"
    calls = []
    check._git_out = lambda root, args: calls.append(args)
    assert check._work_branch(tmp_path) == "wi-360"
    assert calls == [], "the second ask re-ran git instead of reading the memo"


# --- 2. the skip -------------------------------------------------------------


def test_freshness_step_runs_when_not_on_a_work_branch(check, tmp_path, monkeypatch):
    # The control case, and the important one: OFF a work branch the step runs,
    # so a stale artifact is still flagged. Everything below only proves the
    # exception; this proves the rule it is an exception to.
    git_repo(tmp_path, branch="main")
    monkeypatch.chdir(tmp_path)
    status, _detail = check.run_step("status-map", (), FAILING, lenient=False)
    assert status == "FAIL"


def test_freshness_step_is_skipped_with_notice_on_a_work_branch(
    check, tmp_path, monkeypatch, capsys
):
    git_repo(tmp_path, branch="wi-360")
    claim(tmp_path, "wi-360")
    monkeypatch.chdir(tmp_path)
    status, detail = check.run_step("status-map", (), FAILING, lenient=False)
    # SKIP, not FAIL: the step whose command cannot pass was never run, so a
    # stale status.md block on this branch is NOT flagged — that is the trunk's.
    assert status == "SKIP"
    assert "work branch 'wi-360'" in detail
    assert NOTICE.format(step="status-map", branch="wi-360") in capsys.readouterr().out


def test_every_declared_freshness_step_is_skipped(check, tmp_path, monkeypatch):
    # The set is a contract with §5.2, so assert it whole rather than sampling:
    # a step quietly added to or dropped from _TRUNK_FRESHNESS_STEPS changes
    # which gates a branch answers for.
    git_repo(tmp_path, branch="wi-360")
    claim(tmp_path, "wi-360")
    monkeypatch.chdir(tmp_path)
    assert set(check._TRUNK_FRESHNESS_STEPS) == {
        # `derived-gate` left the set at WI-498 slice 5 with the docs/gate BAR
        # axis it guarded; `derived-stage` is the surviving derived-artifact step.
        "derived-stage",
        "trajectory-map",
        "status-map",
        "open-items",
        # WI-484 phase 3: the generated component view joins the set for the
        # same reason its siblings are in it — it is a trunk-owned generated
        # artifact a work branch must never commit, so a branch does not answer
        # for its freshness.
        "component-view",
        "okf",
        "approval-fresh",
    }
    for name in check._TRUNK_FRESHNESS_STEPS:
        assert check.run_step(name, (), FAILING, lenient=False)[0] == "SKIP", name


def test_skills_sync_is_not_skipped_on_a_work_branch(check, tmp_path, monkeypatch):
    # skills-sync compares one hand-authored SOURCE against its per-agent copies.
    # Both sides are the branch's to edit, so the branch owns keeping them in
    # step — this is NOT a trunk-derived view and must keep gating.
    git_repo(tmp_path, branch="wi-360")
    claim(tmp_path, "wi-360")
    monkeypatch.chdir(tmp_path)
    assert check.run_step("skills-sync", (), FAILING, lenient=False)[0] == "FAIL"


def test_branch_edit_gates_still_run_in_the_g3_plan(check, tmp_path, monkeypatch):
    # --gate DevStg-Impl on a work branch: the registry/DAG/navigability gates grade the
    # branch's OWN edits and must survive the lane rule. Asserted over the real
    # DevStg-Impl plan, so a step renamed in the table is caught here too.
    git_repo(tmp_path, branch="wi-360")
    claim(tmp_path, "wi-360")
    monkeypatch.chdir(tmp_path)
    plan = check.steps(80, "all", "DevStg-Impl")
    names = {s[0] for s in plan}
    for required in ("trajectory", "registry-integrity", "doc-navigability"):
        assert required in names, "{} left the DevStg-Impl plan".format(required)
        assert check._work_branch_skip(required) is None, required
    # ...while the plan still LISTS the skipped freshness steps. The skip is at
    # execution, never by deleting rows, so `--list` cannot understate the gate.
    assert check._TRUNK_FRESHNESS_STEPS <= names


def test_trunk_lane_forces_every_freshness_step_back_on(check, tmp_path, monkeypatch):
    # WI-386. The refresh bar runs on the branch, and the integrator reads any
    # SKIP as a refusal — so without this flag the seven freshness steps stand
    # down, the bar reports SKIP, and the refresh can never go green at all.
    # The flag MAKES the mechanical bar possible; it is not a rescue from a
    # false pass (REVIEW-A round 1 drove the direction). The branch is
    # genuinely claimed here (the detector still says so), which is what makes
    # this a forced OVERRIDE rather than a detection change.
    git_repo(tmp_path, branch="wi-360")
    claim(tmp_path, "wi-360")
    monkeypatch.chdir(tmp_path)
    assert check._work_branch(tmp_path) == "wi-360"
    monkeypatch.setattr(check, "_FORCE_TRUNK_LANE", True)
    for name in check._TRUNK_FRESHNESS_STEPS:
        assert check.run_step(name, (), FAILING, lenient=False)[0] == "FAIL", name
    # The captured (parallel) runner shares the same decision, or `--jobs N`
    # and `--jobs 1` would bar different things.
    assert check.run_step_captured("okf", (), FAILING, lenient=False)[0] == "FAIL"


def test_trunk_lane_is_opt_in_and_off_by_default(check, tmp_path, monkeypatch):
    # The arming boundary from the other side: the same claimed branch, the same
    # steps, no flag — every one still SKIPs. A default that had drifted to "on"
    # would red every honest work branch for drift §5.2 forbids it to fix.
    git_repo(tmp_path, branch="wi-360")
    claim(tmp_path, "wi-360")
    monkeypatch.chdir(tmp_path)
    assert check._FORCE_TRUNK_LANE is False
    for name in check._TRUNK_FRESHNESS_STEPS:
        assert check.run_step(name, (), FAILING, lenient=False)[0] == "SKIP", name


def test_trunk_lane_reaches_the_step_runner_through_the_real_cli(tmp_path):
    # End to end as integrate.py's refresh actually invokes it: the flag must
    # survive argparse and reach the runner, not merely exist in --help.
    git_repo(tmp_path, branch="wi-360")
    claim(tmp_path, "wi-360")
    proc = run_py(
        [SCRIPTS / "check.py", "--run-steps", "status-map", "--trunk-lane"],
        cwd=tmp_path,
    )
    out = proc.stdout + proc.stderr
    assert "skipped (work branch 'wi-360'" not in out, out
    # Proven by the CHILD's own output, not by an exit code: the generator
    # really executed on this claimed branch instead of being stood down.
    assert "gen_trajectory" in out, out
    # Without the flag, the same command on the same fixture stands down.
    plain = run_py([SCRIPTS / "check.py", "--run-steps", "status-map"], cwd=tmp_path)
    assert NOTICE.format(step="status-map", branch="wi-360") in (
        plain.stdout + plain.stderr
    )


def test_run_steps_end_to_end_reports_the_skip_and_exits_zero(tmp_path):
    # The pre-commit hook's real entry point, as a subprocess: a claimed branch
    # gets the notice and a green exit; the freshness step never runs.
    git_repo(tmp_path, branch="wi-360")
    claim(tmp_path, "wi-360")
    proc = run_py([SCRIPTS / "check.py", "--run-steps", "status-map"], cwd=tmp_path)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert NOTICE.format(step="status-map", branch="wi-360") in out, out


def test_cache_key_is_the_root_not_the_process(check, tmp_path):
    # Two repos in one process (the suite itself, and any tool that walks
    # several checkouts) must not be served each other's answer.
    trunk, work = tmp_path / "trunk", tmp_path / "work"
    for d in (trunk, work):
        d.mkdir()
    git_repo(trunk, branch="main")
    git_repo(work, branch="wi-360")
    claim(work, "wi-360")
    assert check._work_branch(trunk) is None
    assert check._work_branch(work) == "wi-360"
    assert check._work_branch(trunk) is None


def test_the_primary_checkout_is_not_a_work_branch(check):
    # The kit's PRIMARY checkout — the trunk lane — has no
    # docs/work/active/<branch>/ claim, so its own harness runs the full bar.
    # This is the guard that would catch a detector so loose it matched the
    # trunk — the failure mode that turns every freshness gate off everywhere.
    #
    # The subject is the primary checkout, not "wherever this suite happens to
    # run". Before the station protocol (WI-386) those were the same thing; a
    # lane worktree now runs this suite as a GATE during `integrate.py refresh`,
    # and a lane by construction HAS a claim — so asserting about the current
    # root made the guard false exactly where the protocol needs it green, and
    # the intent (the detector must not match trunk) is unchanged by naming the
    # trunk explicitly. The constructed both-ways proof is the test above; this
    # one is the live-repo canary over the real registry.
    root = SCRIPTS.parent.parent
    proc = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        cwd=os.fspath(root),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    common = (root / proc.stdout.strip()).resolve()
    assert check._work_branch(os.fspath(common.parent)) is None
