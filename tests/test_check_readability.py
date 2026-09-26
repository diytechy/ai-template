"""Verifies SR-216 / LLR-256 (TC-249) — the per-change readability report.

Every case drives `check_readability.py` over a REAL git repository whose stack
profile declares the complexity measure against a stamped baseline, which is why
the module is registered in conftest.SLOW_MODULES: each case pays `git init`,
commits and, on the claimed-branch case, a linked worktree. Most cases call
`main()` in-process so a second measure adapter can be injected; the gating case
runs the delivered command as a subprocess, because its exit code is the whole
contract the harness reads back.

The fixture's two functions score 21 each (threshold 15). Only `tangled` has a
baseline row. `other` is unstamped debt in the SAME file, so a report that
measured the whole touched file instead of the touched functions would name it:
that is what makes "untouched functions are not measured" observable.
"""

import subprocess
import sys
from pathlib import Path

import pytest
from conftest import SCRIPTS, load_script, pin_autocrlf, run_py, skip_without_env_gates

TANGLED = """def tangled(a, b, c, d):
    for x in a:
        if b:
            while c:
                if d:
                    for y in d:
                        if y:
                            pass
    return a
"""

OTHER = """def other(a, b, c, d):
    for x in a:
        if b:
            while c:
                if d:
                    for y in d:
                        if y:
                            pass
    return b
"""

# One more top-level `if` in `tangled`: +1 cognitive, 21 -> 22.
TANGLED_WORSE = TANGLED.replace(
    "    for x in a:\n", "    if c:\n        a = b\n    for x in a:\n", 1
)
# A touched line that changes no score: `tangled` stays at 21.
TANGLED_SAME = TANGLED.replace("    return a\n", "    return b\n", 1)


@pytest.fixture
def cr():
    return load_script("check_readability")


def _git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _profile(measures="complexity", gating=None):
    text = "[readability]\nmeasures = {}\n".format(measures)
    return text + ("gating = {}\n".format(gating) if gating is not None else "")


def make_repo(root, profile=None):
    """A committed repo on `main`: `src/mod.py` holding `tangled` then `other`,
    a stack profile, and a complexity baseline stamped for `tangled` alone."""
    skip_without_env_gates("git")
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-q")
    pin_autocrlf(root)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    _write(root / "docs" / "stack.ini", _profile() if profile is None else profile)
    _write(root / "src" / "mod.py", TANGLED + "\n\n" + OTHER)
    cc = load_script("check_complexity")
    rows, _modules = cc.census(root, ("src/**/*.py",))
    stamped = [row for row in rows if row[1] == "tangled"]
    assert stamped and stamped[0][2] == 21, rows
    cc.write_baseline(root / cc.BASELINE, stamped, {})
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "base")
    return root


def stage_module(root, tangled):
    _write(root / "src" / "mod.py", tangled + "\n\n" + OTHER)
    _git(root, "add", "-A")


def drive(cr, root, capsys):
    code = cr.main(["--root", str(root)])
    out = capsys.readouterr().out
    return code, [line for line in out.splitlines() if line.strip()]


def worsening_lines(lines):
    return [line for line in lines if "worsened" in line]


def test_a_staged_raise_prints_one_line_naming_measure_function_and_delta(
    tmp_path, cr, capsys
):
    repo = make_repo(tmp_path / "repo")
    stage_module(repo, TANGLED_WORSE)
    code, lines = drive(cr, repo, capsys)
    assert code == 0, lines
    worse = worsening_lines(lines)
    assert len(worse) == 1, lines
    assert "complexity" in worse[0]
    assert "src/mod.py::tangled" in worse[0]
    assert "21 -> 22" in worse[0] and "(+1)" in worse[0], worse[0]


def test_untouched_functions_are_not_measured(tmp_path, cr, capsys):
    # `other` sits over the threshold with no baseline row, in the very file the
    # change touches; measuring the file rather than the touched function would
    # report it as new debt.
    repo = make_repo(tmp_path / "repo")
    stage_module(repo, TANGLED_WORSE)
    _code, lines = drive(cr, repo, capsys)
    assert not [line for line in lines if "::other" in line], lines


def test_complexity_measures_only_the_declared_source_and_test_roots(
    tmp_path, cr, capsys
):
    # A kit script vendored under scripts/ is not the project's code: its debt
    # must not bury the project's own worsening. `[paths]` names the roots.
    repo = make_repo(tmp_path / "repo", "[paths]\nsrc = src\n" + _profile())
    _write(repo / "scripts" / "vendored.py", OTHER)
    stage_module(repo, TANGLED_WORSE)
    _code, lines = drive(cr, repo, capsys)
    worse = worsening_lines(lines)
    assert len(worse) == 1 and "src/mod.py::tangled" in worse[0], lines


def test_a_change_worsening_nothing_prints_no_worsening_line(tmp_path, cr, capsys):
    repo = make_repo(tmp_path / "repo")
    stage_module(repo, TANGLED_SAME)
    code, lines = drive(cr, repo, capsys)
    assert code == 0, lines
    assert worsening_lines(lines) == [], lines
    assert lines, "the report says what it measured even when nothing worsened"


def test_an_injected_second_measure_reports_beside_complexity_in_one_report(
    tmp_path, cr, capsys, monkeypatch
):
    repo = make_repo(tmp_path / "repo", _profile("complexity, notes"))
    _write(repo / "docs" / "notes.md", "one\ntwo\n")
    stage_module(repo, TANGLED_WORSE)
    seen = []

    def notes(root, change):
        seen.append(sorted(change.parts))
        return [("docs/notes.md", "2 lines, was 0 (+2)")]

    monkeypatch.setitem(cr.MEASURES, "notes", notes)
    code, lines = drive(cr, repo, capsys)
    assert code == 0, lines
    assert seen == [["docs/notes.md", "src/mod.py"]], seen
    worse = worsening_lines(lines)
    assert len(worse) == 2, lines
    assert any("complexity" in w and "src/mod.py::tangled" in w for w in worse)
    assert any("notes" in w and "docs/notes.md" in w and "(+2)" in w for w in worse)
    assert "2 worsening" in lines[-1], lines


@pytest.mark.parametrize(
    "profile", ["[readability]\nmeasures =\n", "[paths]\nsrc = src\n"]
)
def test_a_profile_declaring_no_measure_prints_one_line_and_exits_zero(
    tmp_path, cr, capsys, profile
):
    repo = make_repo(tmp_path / "repo", profile)
    stage_module(repo, TANGLED_WORSE)
    code, lines = drive(cr, repo, capsys)
    assert code == 0
    assert len(lines) == 1, lines
    assert "nothing is measured" in lines[0], lines


def test_a_worsening_in_a_gating_measure_exits_nonzero(tmp_path):
    repo = make_repo(tmp_path / "repo", _profile(gating="complexity"))
    stage_module(repo, TANGLED_WORSE)
    proc = run_py([SCRIPTS / "check_readability.py", "--root", repo], cwd=repo)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "FAIL" in proc.stdout and "src/mod.py::tangled" in proc.stdout


def test_a_worsening_in_a_reporting_only_measure_exits_zero(tmp_path):
    repo = make_repo(tmp_path / "repo", _profile(gating=""))
    stage_module(repo, TANGLED_WORSE)
    proc = run_py([SCRIPTS / "check_readability.py", "--root", repo], cwd=repo)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARN" in proc.stdout and "src/mod.py::tangled" in proc.stdout


def test_the_complexity_adapter_calls_the_complexity_modules_own_comparison(
    tmp_path, cr, capsys, monkeypatch
):
    repo = make_repo(tmp_path / "repo")
    stage_module(repo, TANGLED_WORSE)
    module = cr.check_complexity
    # Identity first: the adapter's complexity module IS the census module on
    # disk, not a copy of its functions under another name.
    assert module is sys.modules["check_complexity"]
    want = (SCRIPTS / "check_complexity.py").resolve()
    assert Path(module.__file__).resolve() == want
    calls = []
    for name in ("census", "read_baseline", "compare"):
        own = getattr(module, name)

        def spy(*args, _own=own, _name=name):
            calls.append(_name)
            return _own(*args)

        monkeypatch.setattr(module, name, spy)
    _code, lines = drive(cr, repo, capsys)
    assert {"census", "read_baseline", "compare"} <= set(calls), calls
    assert len(worsening_lines(lines)) == 1, lines


def test_on_a_claimed_branch_the_change_is_read_from_the_merge_base(
    tmp_path, cr, capsys
):
    # The fixture must tell the merge base apart from the two wrong readings a
    # lane invites. The worsening is in the lane's FIRST commit and a second
    # commit follows it, so a HEAD^..HEAD reading sees no worsening. The trunk
    # then moves on its own, touching `other` (unstamped, over the threshold),
    # so a trunk-tip..HEAD reading would name `other` as a worsening.
    trunk = make_repo(tmp_path / "trunk")
    _write(trunk / "docs" / "work" / "active" / "lane" / "WI-001-x.md", "claim\n")
    _git(trunk, "add", "-A")
    _git(trunk, "commit", "-qm", "claim: WI-001 -> active/lane (bookkeeping)")
    # On the trunk the index matches HEAD: nothing to measure.
    _code, lines = drive(cr, trunk, capsys)
    assert worsening_lines(lines) == [], lines
    lane = tmp_path / "lane"
    _git(trunk, "worktree", "add", "-q", "-b", "lane", str(lane))
    stage_module(lane, TANGLED_WORSE)
    _git(lane, "commit", "-qm", "raise tangled")
    _write(lane / "docs" / "notes.md", "a later lane commit\n")
    _git(lane, "add", "-A")
    _git(lane, "commit", "-qm", "a second lane commit")
    _write(trunk / "src" / "mod.py", TANGLED + "\n\n" + OTHER.replace("b\n", "c\n"))
    _git(trunk, "add", "-A")
    _git(trunk, "commit", "-qm", "trunk moves on")
    base = _git(lane, "merge-base", "main", "HEAD").strip()
    assert base != _git(lane, "rev-parse", "HEAD~1").strip()
    assert base != _git(trunk, "rev-parse", "HEAD").strip()
    code, lines = drive(cr, lane, capsys)
    assert code == 0, lines
    worse = worsening_lines(lines)
    assert len(worse) == 1 and "src/mod.py::tangled" in worse[0], lines
    assert not [line for line in lines if "::other" in line], lines
    assert "merge base {} to HEAD".format(base[:10]) in lines[-1], lines


@pytest.mark.parametrize("gating", ["", "complexity"])
def test_an_unreadable_change_is_a_skip_that_exits_zero(
    tmp_path, cr, capsys, monkeypatch, gating
):
    # No repository: the change cannot be read. LLR-256 makes the exit nonzero
    # ONLY for a worsening in a gating measure, and an unreadable change is not
    # a worsening, so even a declared gating measure exits 0 — with a SKIP line
    # naming the measure it could not evaluate and why.
    root = tmp_path / "plain"
    _write(root / "docs" / "stack.ini", _profile(gating=gating))
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path))
    code, lines = drive(cr, root, capsys)
    assert code == 0, lines
    skip = [line for line in lines if "SKIP" in line]
    assert len(skip) == 1, lines
    assert "complexity" in skip[0] and "cannot be read" in skip[0], skip


def test_an_unknown_measure_is_reported_by_name_and_exits_zero(tmp_path, cr, capsys):
    repo = make_repo(tmp_path / "repo", _profile("complexity readabilty"))
    stage_module(repo, TANGLED_WORSE)
    code, lines = drive(cr, repo, capsys)
    assert code == 0, lines
    named = [line for line in lines if "'readabilty'" in line]
    assert len(named) == 1 and "unknown measure" in named[0], lines
    # The declared measure it does know still runs.
    assert len(worsening_lines(lines)) == 1, lines


def test_an_undeclared_gating_name_is_reported_by_name_and_exits_zero(
    tmp_path, cr, capsys
):
    repo = make_repo(tmp_path / "repo", _profile("complexity", gating="notes"))
    stage_module(repo, TANGLED_WORSE)
    code, lines = drive(cr, repo, capsys)
    assert code == 0, lines
    named = [line for line in lines if "'notes'" in line]
    assert len(named) == 1 and "gating" in named[0], lines
    assert len(worsening_lines(lines)) == 1, lines
