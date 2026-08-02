"""check_figures.py — declared-figure provenance, presence only (WI-392 rung 1).

A driven figure is evidence only at the revision it was driven on. The marker
is opt-in (`fig:` on the figure's own line — declare, don't infer), so the
check's honest claim is "declared figures carry provenance", never "all
figures do": it verifies a declared figure names the command that produced it
and the revision it was driven at (or a derivation from declared figures) —
presence, never truth. The three false figures of 2026-08-01 (WI-380's stale
mutation ledger, WI-391's unreproducible link count, WI-384's self-falsifying
"two false positives") are the fixtures: each would have been flagged.
Exercised over temp repos, warn-first (exit 0) unless --strict.
"""

from conftest import SCRIPTS, run_py

# The three false figures of 2026-08-01, verbatim, each declared with a bare
# marker carrying no provenance — the shape the check exists to flag.
THREE_FALSE_FIGURES = """# Session record

The mutation ledger read `2 failed, 7 passed`. <!-- fig: -->
The filed title read 109 links. <!-- fig: -->
The composed-tree paragraph reported two false positives. <!-- fig: -->
"""


def make_repo(root, body, name="README.md"):
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / name).write_text(body, encoding="utf-8")
    return root


def figs(root, *args):
    return run_py([SCRIPTS / "check_figures.py", *args], cwd=root)


def test_the_three_false_figures_each_flag_under_a_bare_marker(tmp_path):
    make_repo(tmp_path, THREE_FALSE_FIGURES)
    proc = figs(tmp_path)
    assert proc.returncode == 0, "warn-first: findings must not gate by default"
    for figure in ("2 failed, 7 passed", "109 links", "two false positives"):
        assert figure in proc.stderr, figure
    assert "3 declared figure(s) missing provenance" in proc.stdout


def test_findings_gate_only_under_strict(tmp_path):
    make_repo(tmp_path, THREE_FALSE_FIGURES)
    assert figs(tmp_path).returncode == 0
    assert figs(tmp_path, "--strict").returncode == 1


def test_command_plus_revision_passes(tmp_path):
    make_repo(
        tmp_path,
        "smoke: 597 passed / 25.8 s wall "
        '<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=6d6a1114 -->\n',
    )
    proc = figs(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "OK" in proc.stdout
    assert "1 declared figure(s)" in proc.stdout


def test_a_half_carrying_marker_names_its_missing_half(tmp_path):
    make_repo(
        tmp_path,
        'Counted 154 occurrences. <!-- fig: cmd="grep -c foo docs/log.md" -->\n'
        "Counted 101 targets. <!-- fig: rev=6d6a1114 -->\n",
    )
    proc = figs(tmp_path)
    assert "no rev=" in proc.stderr
    assert "no cmd=" in proc.stderr
    assert figs(tmp_path, "--strict").returncode == 1


def test_empty_attribute_values_count_as_missing(tmp_path):
    make_repo(tmp_path, 'Total 20 merges. <!-- fig: cmd="" rev=6d6a1114 -->\n')
    assert "no cmd=" in figs(tmp_path).stderr
    make_repo(tmp_path, 'Total 20 merges. <!-- fig: cmd="git log" rev= -->\n')
    assert "no rev=" in figs(tmp_path).stderr


def test_a_derived_figure_declares_its_derivation(tmp_path):
    # The fifth 2026-08-01 case: a complement mis-derived from a re-derived
    # census in the very paragraph explaining the hazard. Under the convention
    # the derived figure is itself declared.
    make_repo(
        tmp_path,
        "So thirteen of the twenty staled nothing "
        '<!-- fig: derived="20 (the git log count above) minus the 7 staled" -->\n',
    )
    proc = figs(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "OK" in proc.stdout


def test_an_empty_derivation_is_missing_provenance(tmp_path):
    make_repo(tmp_path, 'Twelve staled nothing. <!-- fig: derived="" -->\n')
    proc = figs(tmp_path)
    assert "derivation" in proc.stderr
    assert figs(tmp_path, "--strict").returncode == 1


def test_unmarked_figures_are_out_of_scope_by_design(tmp_path):
    # The honest claim: declared figures carry provenance — not all figures do.
    make_repo(tmp_path, "The suite ran 1802 passed / 10 skipped in 634 s.\n")
    proc = figs(tmp_path)
    assert proc.returncode == 0
    assert "no declared figures" in proc.stdout
    assert figs(tmp_path, "--strict").returncode == 0


def test_a_fig_ok_line_is_exempt(tmp_path):
    make_repo(
        tmp_path,
        "Write `fig:` on the figure's own line. "
        "<!-- fig-ok: prose about the convention, not a declaration -->\n",
    )
    assert figs(tmp_path, "--strict").returncode == 0


def test_generated_marker_blocks_are_skipped(tmp_path):
    make_repo(
        tmp_path,
        "<!-- BEGIN GENERATED MAP -->\n"
        "97 rows <!-- fig: -->\n"
        "<!-- END GENERATED MAP -->\n",
    )
    assert figs(tmp_path, "--strict").returncode == 0


def test_docs_stack_ini_is_a_declared_surface(tmp_path):
    make_repo(tmp_path, "No figures here.\n")
    (tmp_path / "docs" / "stack.ini").write_text(
        "# Measured 490 tests / 24.2 s wall fig:\n", encoding="utf-8"
    )
    proc = figs(tmp_path)
    assert "docs/stack.ini:1" in proc.stderr
    (tmp_path / "docs" / "stack.ini").write_text(
        '# Measured 490 tests / 24.2 s wall fig: cmd="python -m pytest -q '
        '-n auto -m smoke" rev=41d180e6\n',
        encoding="utf-8",
    )
    assert figs(tmp_path, "--strict").returncode == 0


def test_config_colon_is_not_a_marker(tmp_path):
    make_repo(tmp_path, "See config: and reconfig: notes; no figure declared.\n")
    proc = figs(tmp_path)
    assert proc.returncode == 0
    assert "no declared figures" in proc.stdout


def test_docs_tree_is_scanned_beside_the_root(tmp_path):
    make_repo(tmp_path, "Nothing at the root.\n")
    (tmp_path / "docs" / "log.md").write_text(
        "Census read 13 of 20. <!-- fig: -->\n", encoding="utf-8"
    )
    proc = figs(tmp_path)
    assert "docs/log.md:1" in proc.stderr
