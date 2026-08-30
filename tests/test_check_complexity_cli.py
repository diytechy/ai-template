"""Verifies SR-183 / LLR-206 (TC-202) — check_complexity.py driven as a subprocess.

The CLI half of the census's tests: every mode driven the way an adopter's
`stack.ini` would, against synthetic `project-trajectory/scripts/` fixtures. Kept
SEPARATE from the in-process unit module (test_check_complexity.py) and re-tiered
into conftest.SLOW_MODULES: each case pays interpreter startup, so this is the
subprocess-dominated class that the per-commit smoke bar drops and the
slice/phase-close + CI run exercises in full. The counting metric itself is
pinned in-process next door, where it is cheap.
"""

from conftest import SCRIPTS, run_py

SAMPLE = """
def tangled(a, b, c, d):
    for x in a:
        if b:
            while c:
                if d:
                    for y in d:
                        if y:
                            pass
    return a


def simple(a):
    return a
"""


def drive(root, *args):
    return run_py([SCRIPTS / "check_complexity.py", "--root", root, *args], cwd=root)


def _write_sample_repo(root):
    target = root / "project-trajectory" / "scripts"
    target.mkdir(parents=True)
    (target / "mod.py").write_text(SAMPLE, encoding="utf-8")


def test_report_mode_exits_zero_and_prints_every_function(tmp_path):
    _write_sample_repo(tmp_path)
    proc = drive(tmp_path, "--report")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stdout.startswith("# path\tfunction\tcognitive\tsloc")
    assert "\tsimple\t0\t" in proc.stdout


def test_restamp_then_enforce_is_green(tmp_path):
    _write_sample_repo(tmp_path)
    assert drive(tmp_path, "--restamp").returncode == 0
    proc = drive(tmp_path, "--mode", "enforce")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "unchanged from baseline" in proc.stdout


def test_enforce_fails_on_growth(tmp_path):
    _write_sample_repo(tmp_path)
    drive(tmp_path, "--restamp")
    mod = tmp_path / "project-trajectory" / "scripts" / "mod.py"
    mod.write_text(
        SAMPLE.replace("    return a\n", "    if b:\n        return a\n"),
        encoding="utf-8",
    )
    proc = drive(tmp_path, "--mode", "enforce")
    assert proc.returncode == 1
    assert "SIMPLIFY" in proc.stderr
    assert "decompose OUTWARD" in proc.stderr


def test_enforce_fails_on_unstamped_improvement(tmp_path):
    _write_sample_repo(tmp_path)
    drive(tmp_path, "--restamp")
    mod = tmp_path / "project-trajectory" / "scripts" / "mod.py"
    mod.write_text(
        SAMPLE.replace(
            "                        if y:\n                            pass\n",
            "                        pass\n",
        ),
        encoding="utf-8",
    )
    proc = drive(tmp_path, "--mode", "enforce")
    assert proc.returncode == 1
    assert "RE-STAMP" in proc.stderr


def test_enforce_fails_when_a_baselined_function_vanishes(tmp_path):
    _write_sample_repo(tmp_path)
    drive(tmp_path, "--restamp")
    mod = tmp_path / "project-trajectory" / "scripts" / "mod.py"
    mod.write_text("def simple(a):\n    return a\n", encoding="utf-8")
    proc = drive(tmp_path, "--mode", "enforce")
    assert proc.returncode == 1
    assert "RE-STAMP" in proc.stderr


def test_a_suppression_shaped_comment_changes_nothing(tmp_path):
    """There is no inline pragma: a `# noqa`-shaped comment in the source is
    inert, so the census reads it the same as any other function."""
    _write_sample_repo(tmp_path)
    drive(tmp_path, "--restamp")
    mod = tmp_path / "project-trajectory" / "scripts" / "mod.py"
    mod.write_text(
        SAMPLE.replace(
            "def tangled(a, b, c, d):", "def tangled(a, b, c, d):  # noqa: complexity"
        ),
        encoding="utf-8",
    )
    proc = drive(tmp_path, "--mode", "enforce")
    assert proc.returncode == 0, (
        "a suppression comment is not honoured, but it changes no score"
    )
    assert "unchanged from baseline" in proc.stdout


def test_no_source_dir_is_vacuously_ok(tmp_path):
    (tmp_path / "docs").mkdir()
    proc = drive(tmp_path, "--mode", "enforce")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "OK" in proc.stdout


CONTROL_FLOW_DEFS = """
for _i in range(1):
    def hidden_by_for(a):
        if a:
            return 1

while False:
    def hidden_by_while(a):
        return a

match 0:
    case 0:
        def hidden_by_match(a):
            return a
"""


def test_functions_under_control_flow_are_censused(tmp_path):
    """Regression: a module-level `def` wrapped in `for`/`while`/`match` (not
    just `if`/`try`/`with`) is a real module symbol and must appear in the
    census, both as a row and in the module's public-symbol count."""
    target = tmp_path / "project-trajectory" / "scripts"
    target.mkdir(parents=True)
    (target / "mod.py").write_text(CONTROL_FLOW_DEFS, encoding="utf-8")
    proc = drive(tmp_path, "--report")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    for name in ("hidden_by_for", "hidden_by_while", "hidden_by_match"):
        assert "\t{}\t".format(name) in proc.stdout, name
    assert "# module\tproject-trajectory/scripts/mod.py\t3\t" in proc.stdout


def test_include_globs_are_repeatable(tmp_path):
    _write_sample_repo(tmp_path)
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_x.py").write_text(SAMPLE, encoding="utf-8")
    proc = drive(
        tmp_path,
        "--report",
        "--include",
        "project-trajectory/scripts/**/*.py",
        "--include",
        "tests/**/*.py",
    )
    assert "tests/test_x.py\ttangled" in proc.stdout
    assert "project-trajectory/scripts/mod.py\ttangled" in proc.stdout
