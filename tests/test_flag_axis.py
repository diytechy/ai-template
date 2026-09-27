"""Verifies SR-216 / LLR-261 (TC-256): the flag-axis measure of the per-change
readability report.

Every case is in memory: source text parsed by `ast`, a stack profile and a
baseline written under `tmp_path`, and the change the report reads handed in as
a `Change` with the new side's text served by a stand-in for the blob read. No
git, no subprocess, no scaffold, so the module stays in the per-commit tier; the
report's real change reading is TC-249's, over real repositories.

The measure's two counts are candidates for an enum state: a function taking
two or more boolean parameters, and a call site passing a boolean literal
positionally, where the reader cannot tell what `True` switches.
"""

import pytest
from conftest import load_script

TWO_FLAGS = "def export(rows, strict=True, verbose=False):\n    return rows\n"
ANNOTATED = "def merge(a, b, *, fast: bool, dry: bool):\n    return a\n"
ONE_FLAG = "def export(rows, strict=True):\n    return rows\n"
LITERAL_SITE = "export(rows, True)\n"
KEYWORD_SITE = "export(rows, strict=True)\nPath(p).mkdir(parents=True)\n"


@pytest.fixture
def fa():
    return load_script("flag_axis")


@pytest.fixture
def cr():
    return load_script("check_readability")


def _reading(fa, text):
    return fa.reading(fa.ast.parse(text))


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


# --- the two counts --------------------------------------------------------


def test_a_two_flag_function_is_counted_with_its_flags(fa):
    assert _reading(fa, TWO_FLAGS).functions == [("export", ("strict", "verbose"))]
    # A `bool` annotation marks a flag as a literal default does, keyword-only
    # parameters included.
    assert _reading(fa, ANNOTATED).functions == [("merge", ("fast", "dry"))]


def test_a_one_flag_function_is_not_counted(fa):
    assert _reading(fa, ONE_FLAG).functions == []


def test_a_method_is_named_as_the_complexity_census_names_it(fa):
    text = "class Job:\n    def run(self, a=True, b=False):\n        pass\n"
    assert _reading(fa, text).functions == [("Job.run", ("a", "b"))]


def test_a_boolean_literal_call_site_is_counted(fa):
    assert _reading(fa, LITERAL_SITE).sites == [(1, "export")]


def test_a_keyword_literal_is_not_a_call_site(fa):
    # Named at the call, the switch is legible, and a flag parameter behind it
    # is counted where it is defined; `mkdir(parents=True)` is a library's
    # signature the project cannot change.
    assert _reading(fa, KEYWORD_SITE).sites == []


# --- the stamped baseline and the whole-tree report ------------------------


def test_the_report_lists_each_module_and_the_totals_and_exits_zero(
    fa, tmp_path, capsys
):
    _write(tmp_path / "src" / "a.py", TWO_FLAGS + LITERAL_SITE)
    _write(tmp_path / "src" / "b.py", ONE_FLAG + LITERAL_SITE + LITERAL_SITE)
    _write(tmp_path / "src" / "c.py", "x = 1\n")
    code = fa.main(["--root", str(tmp_path), "--include", "src/**/*.py"])
    out = capsys.readouterr().out.splitlines()
    assert code == 0
    a = [line for line in out if line.startswith("flag_axis: src/a.py")]
    b = [line for line in out if line.startswith("flag_axis: src/b.py")]
    assert len(a) == 1 and "export(strict, verbose)" in a[0], out
    assert len(b) == 1 and "0 flag function" in b[0] and "2 boolean" in b[0], out
    assert not [line for line in out if "src/c.py" in line], out
    total = [line for line in out if "total" in line]
    assert len(total) == 1, out
    assert "1 flag function" in total[0] and "3 boolean" in total[0], out


def test_a_reading_above_its_stamped_row_warns_and_still_exits_zero(
    fa, tmp_path, capsys
):
    _write(tmp_path / "src" / "a.py", ONE_FLAG)
    assert (
        fa.main(["--root", str(tmp_path), "--include", "src/**/*.py", "--restamp"]) == 0
    )
    _write(tmp_path / "src" / "a.py", TWO_FLAGS + LITERAL_SITE)
    capsys.readouterr()
    code = fa.main(["--root", str(tmp_path), "--include", "src/**/*.py"])
    out = capsys.readouterr().out
    assert code == 0, out
    assert "WARN" in out and "src/a.py" in out and "0 -> 1" in out, out


def test_a_restamp_records_each_counted_module_and_reads_back_level(
    fa, tmp_path, capsys
):
    _write(tmp_path / "src" / "a.py", TWO_FLAGS + LITERAL_SITE)
    _write(tmp_path / "src" / "b.py", ONE_FLAG + LITERAL_SITE + LITERAL_SITE)
    _write(tmp_path / "src" / "c.py", "x = 1\n")
    fa.main(["--root", str(tmp_path), "--include", "src/**/*.py", "--restamp"])
    assert fa.read_baseline(tmp_path / fa.BASELINE) == {
        "src/a.py": (1, 1),
        "src/b.py": (0, 2),
    }
    capsys.readouterr()
    fa.main(["--root", str(tmp_path), "--include", "src/**/*.py"])
    assert "WARN" not in capsys.readouterr().out


def test_compare_names_only_the_counts_that_rose(fa):
    now = _reading(fa, TWO_FLAGS + LITERAL_SITE)
    assert fa.compare(now, (1, 1)) is None
    assert fa.compare(now, (2, 5)) is None, "below the row is not a worsening"
    delta = fa.compare(now, (1, 0))
    assert "boolean-literal call sites 0 -> 1 (+1)" in delta
    assert "flag functions" not in delta
    assert "flag functions 0 -> 1 (+1: export(strict, verbose))" in fa.compare(
        now, None
    )


def test_an_unreadable_or_invalid_module_is_skipped_and_the_report_exits_zero(
    fa, tmp_path, capsys
):
    _write(tmp_path / "src" / "a.py", TWO_FLAGS)
    _write(tmp_path / "src" / "broken.py", "def (:\n")
    (tmp_path / "src" / "latin.py").write_bytes(b"x = '\xe9'\n")
    for extra in ([], ["--restamp"]):
        code = fa.main(["--root", str(tmp_path), "--include", "src/**/*.py", *extra])
        out = capsys.readouterr().out
        assert code == 0, out
        assert "SKIP - cannot read or parse src/broken.py (SyntaxError)" in out, out
        assert "SKIP - cannot read or parse src/latin.py (UnicodeDecodeError)" in out
    assert fa.read_baseline(tmp_path / fa.BASELINE) == {"src/a.py": (1, 0)}


# --- the measure inside the per-change report ------------------------------


def _change(cr, monkeypatch, root, texts):
    """A change touching each path in `texts`, whose new side reads that text."""
    monkeypatch.setattr(
        cr,
        "git_bytes",
        lambda _root, argv: texts[argv[-1].split(":", 1)[1]].encode("utf-8"),
    )
    return cr.Change("", "index against HEAD", {p: frozenset({1}) for p in texts})


def _profile(root, measures="flag-axis", gating=""):
    _write(
        root / "docs" / "stack.ini",
        "[paths]\nsrc = src\ntests = tests\n\n[readability]\n"
        "measures = {}\ngating = {}\n".format(measures, gating),
    )


def test_the_measure_names_the_touched_module_it_worsened(
    fa, cr, tmp_path, monkeypatch
):
    _profile(tmp_path)
    _write(tmp_path / fa.BASELINE, "# path\tflag_functions\tliteral_call_sites\n")
    change = _change(
        cr,
        monkeypatch,
        tmp_path,
        {"src/mod.py": TWO_FLAGS, "src/same.py": ONE_FLAG, "vendor/x.py": TWO_FLAGS},
    )
    found = cr.MEASURES["flag-axis"](tmp_path, change)
    assert [part for part, _delta in found] == ["src/mod.py"], found
    assert "flag functions 0 -> 1" in found[0][1], found


def test_a_module_at_its_stamped_row_reports_nothing(fa, cr, tmp_path, monkeypatch):
    _profile(tmp_path)
    _write(tmp_path / fa.BASELINE, "src/mod.py\t1\t1\n")
    change = _change(
        cr, monkeypatch, tmp_path, {"src/mod.py": TWO_FLAGS + LITERAL_SITE}
    )
    assert cr.MEASURES["flag-axis"](tmp_path, change) == []


def test_declared_gating_the_flag_axis_gates_nothing_and_says_so(cr):
    profile = cr.check.configparser.ConfigParser()
    profile.read_string("[readability]\nmeasures = flag-axis\ngating = flag-axis\n")
    measures, gating, problems = cr.declared_measures(profile)
    assert measures == ["flag-axis"] and gating == [], (measures, gating)
    assert len(problems) == 1, problems
    assert "'flag-axis'" in problems[0], problems
    assert "never refuses" in problems[0], problems
    assert "gates nothing" in problems[0], problems


def test_a_flag_axis_worsening_never_refuses_the_change(
    fa, cr, tmp_path, monkeypatch, capsys
):
    _profile(tmp_path, gating="flag-axis")
    change = _change(cr, monkeypatch, tmp_path, {"src/mod.py": TWO_FLAGS})
    monkeypatch.setattr(cr, "changed_parts", lambda _root: change)
    code = cr.main(["--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert code == 0, out
    assert "WARN - flag-axis worsened src/mod.py" in out, out
