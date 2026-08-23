"""check_dupes_census.py — the WI-448 duplication census, standing (WI-507).

WARN-ONLY FOREVER, by the D-7 ruling this reactivates a narrower half of:
never gates, not even under --strict. Fixtures build tiny synthetic
`project-trajectory/scripts/` trees so the tests never depend on this repo's
own live population (which drifts every commit).
"""

from conftest import SCRIPTS, run_py

DUPE_FN = """
def {name}():
    a = 1
    b = 2
    c = 3
    return a + b + c
"""

UNIQUE_FN = """
def solo():
    return 42
"""


def make_scripts_repo(root, files):
    """`files`: {relative_path: source}, rooted under project-trajectory/scripts/."""
    base = root / "project-trajectory" / "scripts"
    base.mkdir(parents=True, exist_ok=True)
    for rel, src in files.items():
        (base / rel).write_text(src, encoding="utf-8")
    return root


def stamp_baseline(root, groups, copies, lines):
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "stack.ini").write_text(
        "[dupes-census]\ngroups = {}\ncopies = {}\nlines = {}\n".format(
            groups, copies, lines
        ),
        encoding="utf-8",
    )


def census(root, *args):
    return run_py([SCRIPTS / "check_dupes_census.py", *args], cwd=root)


def test_no_baseline_reports_the_reading_and_passes(tmp_path):
    make_scripts_repo(
        tmp_path, {"a.py": DUPE_FN.format(name="f1"), "b.py": DUPE_FN.format(name="f2")}
    )
    proc = census(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "no baseline stamped" in proc.stdout
    assert "1 group(s)" in proc.stdout


def test_unchanged_reading_passes_ok(tmp_path):
    make_scripts_repo(
        tmp_path, {"a.py": DUPE_FN.format(name="f1"), "b.py": DUPE_FN.format(name="f2")}
    )
    stamp_baseline(tmp_path, groups=1, copies=1, lines=5)
    proc = census(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "OK" in proc.stdout
    assert "unchanged from baseline" in proc.stdout


def test_a_regression_warns_but_never_gates_even_under_strict(tmp_path):
    make_scripts_repo(
        tmp_path,
        {
            "a.py": DUPE_FN.format(name="f1"),
            "b.py": DUPE_FN.format(name="f2"),
            "c.py": DUPE_FN.format(name="f3"),
        },
    )
    stamp_baseline(tmp_path, groups=1, copies=1, lines=5)
    for extra in ((), ("--strict",)):
        proc = census(tmp_path, *extra)
        assert proc.returncode == 0, "never a gate, even under --strict"
        assert "WARN" in proc.stderr
        assert "duplication grew" in proc.stderr


def test_an_improvement_asks_for_a_downward_restamp(tmp_path):
    make_scripts_repo(tmp_path, {"a.py": UNIQUE_FN})
    stamp_baseline(tmp_path, groups=1, copies=1, lines=5)
    proc = census(tmp_path)
    assert proc.returncode == 0
    assert "the census improved" in proc.stderr
    assert "Re-stamp" in proc.stderr


def test_no_scripts_dir_is_vacuously_ok(tmp_path):
    (tmp_path / "docs").mkdir()
    proc = census(tmp_path)
    assert proc.returncode == 0
    assert "OK" in proc.stdout
