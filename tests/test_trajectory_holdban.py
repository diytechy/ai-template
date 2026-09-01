"""check_trajectory.py — the hold-by-rename ban (WI-553, OI-70).

A `docs/work/active/<branch>/` claim directory with no matching branch ref is
the exact signature OI-70 bans: a lane parked by renaming its ref while its
claim stays on trunk. These tests drive the detector both ways on a real git
scaffold (matching ref: silent; renamed ref: named) and pin the severity tier
(WARN at the commit bar, ERROR under --strict, the DevStg-Impl gate), plus the
two fail-soft edges (an empty claim dir is ignored; off-git degrades silently).
"""

import shutil
import subprocess

from conftest import (
    ROOT,
    SCRIPTS,
    load_script,
    pin_autocrlf,
    run_py,
    skip_without_env_gates,
)

wi_convert = load_script("wi_convert")
check_trajectory = load_script("check_trajectory")

ACTIVE_BRANCH = "wi-fixture"


def _write_active_lane(root):
    """A minimal, otherwise-clean registry: WI-001 done (delivered SR-001) and
    WI-002 active under `active/<ACTIVE_BRANCH>/`, its SpecRef resolvable so the
    only promotable finding a --strict run can raise is the hold-by-rename one."""
    work = root / "docs" / "work"
    if work.exists():
        shutil.rmtree(work)
    done = {
        "WI-ID": "WI-001",
        "Title": "First",
        "Workstream": "scripts",
        "SR-Refs": "SR-001",
        "Status": "done",
        "Deliverable": "delivered SR-001",
    }
    active = {
        "WI-ID": "WI-002",
        "Title": "Second",
        "Workstream": "scripts",
        "SR-Refs": "SR-001",
        "Predecessors": "WI-001",
        "Status": "active",
        "SpecRef": "docs/specs/WI-002.md#scope",
    }
    wi_convert.write_spec_file(work, _row(done), order=1)
    # The active row's directory is the integrator's branch, which the writer
    # deliberately does not know — supply it and reuse the same renderer.
    text = wi_convert.FENCE + "\n"
    text += wi_convert.render_frontmatter(wi_convert.frontmatter_pairs(_row(active), 2))
    text += wi_convert.FENCE + "\n"
    path = work / "active" / ACTIVE_BRANCH / wi_convert.spec_filename(_row(active))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    # A resolvable SpecRef target (path + anchor), so R-E stays clean under --strict.
    spec = root / "docs" / "specs" / "WI-002.md"
    spec.parent.mkdir(parents=True, exist_ok=True)
    spec.write_text("# spec\n\n## scope\n", encoding="utf-8")


def _row(cells):
    row = dict.fromkeys(wi_convert.COLUMNS, "")
    row.update(cells)
    return row


def _init_repo(root):
    skip_without_env_gates("git")
    git = shutil.which("git")

    def run_git(*a):
        return subprocess.run(
            [git, "-C", str(root), *a], capture_output=True, text=True
        )

    run_git("init")
    pin_autocrlf(root)
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    _write_active_lane(root)
    run_git("add", "-A")
    run_git("commit", "-m", "init")
    # The lane's own branch ref, cut like the integrator cuts it.
    run_git("branch", ACTIVE_BRANCH, "HEAD")
    return run_git


def run_traj(root, *extra):
    return run_py([SCRIPTS / "check_trajectory.py", "--root", root, *extra], cwd=root)


# --- the detector directly ------------------------------------------------------


def test_empty_active_claim_dir_is_ignored(tmp_path):
    # A claim dir with no WI-*.md is claim-machinery leftover, not a hold.
    (tmp_path / "docs" / "work" / "active" / "wi-empty").mkdir(parents=True)
    assert check_trajectory.holdbyrename_findings(tmp_path) == []


def test_off_git_degrades_silently(tmp_path):
    # A claim dir with a spec but no git repository: no refs to match, so the
    # detector says nothing rather than flagging every active lane.
    d = tmp_path / "docs" / "work" / "active" / "wi-nogit"
    d.mkdir(parents=True)
    (d / "WI-003-x.md").write_text("+++\nid = 'WI-003'\n+++\n", encoding="utf-8")
    assert check_trajectory.holdbyrename_findings(tmp_path) == []


# --- end to end, both ways + severity ------------------------------------------


def test_matching_ref_is_silent(tmp_path):
    run_git = _init_repo(tmp_path)
    r = run_traj(tmp_path)
    assert "hold-by-rename" not in (r.stdout + r.stderr)
    # And clean at the gate too — the fixture is otherwise --strict-clean.
    rs = run_traj(tmp_path, "--strict")
    assert "hold-by-rename" not in (rs.stdout + rs.stderr)
    assert rs.returncode == 0


def test_renamed_ref_is_named_and_warns_then_gates(tmp_path):
    run_git = _init_repo(tmp_path)
    # The literal hold-by-rename: the ref is renamed away, the claim stays.
    run_git("branch", "-m", ACTIVE_BRANCH, ACTIVE_BRANCH + "-HELD-for-owner-verdict")
    # Commit bar: WARN, never the exit code.
    r = run_traj(tmp_path)
    assert "hold-by-rename" in r.stderr
    assert ACTIVE_BRANCH in r.stderr
    assert "OI-70" in r.stderr
    assert r.returncode == 0
    # DevStg-Impl gate: --strict promotes it to an ERROR that reds the run.
    rs = run_traj(tmp_path, "--strict")
    assert "hold-by-rename" in rs.stderr
    assert "ERROR" in rs.stderr
    assert rs.returncode == 1


def test_meta_repo_source_is_importable():
    # The detector ships in the traced product, not only the fixture copy.
    assert hasattr(check_trajectory, "holdbyrename_findings")
    assert (SCRIPTS / "check_trajectory.py").exists()
    assert (ROOT / "docs").is_dir()
