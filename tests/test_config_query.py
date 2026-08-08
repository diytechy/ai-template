"""config_query.py — the fail-closed one-key reader the git hooks call (SR-139).

TC-152 permutations: declared | undeclared | below-floor.

The hooks treat a non-zero exit as a BLOCK, so every refusal path is tested as a
first-class behaviour: an undeclared key, a config that does not validate, a
malformed command line, and an interpreter below the declared floor. The
below-floor case is driven by moving the FLOOR rather than the interpreter —
there is no below-floor Python to hand this suite, and a hidden test-only
argument on `main` would be a second contract nobody else could rely on.
"""

import pytest
from conftest import ROOT, SCRIPTS, load_script, run_py

QUERY = load_script("config_query")
CONFIG = load_script("config")


def write_config(root, text):
    docs = root / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "config.toml").write_text(text, encoding="utf-8", newline="\n")
    return root


# --- TC-152: declared ---------------------------------------------------------
def test_declared_key_prints_its_value_and_exits_zero(tmp_path, capsys):
    write_config(tmp_path, 'schema = 1\n\n[policy]\npush = "agent"\n')
    assert QUERY.main(["--root", str(tmp_path), "policy.push"]) == 0
    assert capsys.readouterr().out == "agent\n"


def test_declared_key_falls_back_to_the_schema_default(tmp_path, capsys):
    assert QUERY.main(["--root", str(tmp_path), "policy.review_rounds"]) == 0
    assert capsys.readouterr().out == "1\n"


@pytest.mark.parametrize("declared,printed", [("true", "true"), ("false", "false")])
def test_booleans_print_in_the_retired_files_vocabulary(
    tmp_path, capsys, declared, printed
):
    # The hooks compare against the literal word the one-word files used, so a
    # Python `True` would silently never match.
    write_config(
        tmp_path, "schema = 1\n\n[policy]\nprivacy_check = {}\n".format(declared)
    )
    assert QUERY.main(["--root", str(tmp_path), "policy.privacy_check"]) == 0
    assert capsys.readouterr().out == printed + "\n"


def test_an_array_prints_one_element_per_line(tmp_path, capsys):
    write_config(
        tmp_path,
        'schema = 1\n\n[outcomes]\nrisk_safety_classes = ["spine", "gate"]\n',
    )
    assert QUERY.main(["--root", str(tmp_path), "outcomes.risk_safety_classes"]) == 0
    assert capsys.readouterr().out == "spine\ngate\n"


def test_every_declared_key_is_answerable(tmp_path, capsys):
    for path in CONFIG.DEFAULTS:
        assert QUERY.main(["--root", str(tmp_path), path]) == 0, path
    out = capsys.readouterr().out.splitlines()
    assert len(out) >= len(CONFIG.DEFAULTS)


# --- TC-152: undeclared -------------------------------------------------------
def test_undeclared_key_exits_non_zero_naming_it(tmp_path, capsys):
    assert QUERY.main(["--root", str(tmp_path), "policy.privacy_chek"]) != 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "config_query: REFUSED - policy.privacy_chek" in captured.err
    # The refusal is actionable: it lists what IS declared in that section.
    assert "policy.privacy_check" in captured.err


def test_an_undeclared_section_still_refuses_cleanly(tmp_path, capsys):
    assert QUERY.main(["--root", str(tmp_path), "nonsense.key"]) != 0
    assert "not a declared key" in capsys.readouterr().err


@pytest.mark.parametrize(
    "argv", [[], ["a.b", "c.d"], ["--root"], ["--bogus", "policy.push"]]
)
def test_a_malformed_command_line_refuses(argv, capsys):
    assert QUERY.main(argv) != 0
    assert "config_query: REFUSED" in capsys.readouterr().err


# --- TC-152: below-floor ------------------------------------------------------
def test_below_floor_interpreter_refuses_naming_the_floor(
    tmp_path, capsys, monkeypatch
):
    monkeypatch.setattr(QUERY, "MIN_PYTHON", (99, 0))
    assert QUERY.main(["--root", str(tmp_path), "policy.push"]) != 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "99.0" in captured.err, "the refusal must name the floor it wants"
    assert "config_query: REFUSED" in captured.err


def test_the_floor_is_checked_before_anything_heavy_is_imported(monkeypatch):
    # The refusal must not depend on `import tomllib` succeeding — that import
    # is exactly what fails on a below-floor box.
    monkeypatch.setattr(QUERY, "MIN_PYTHON", (99, 0))
    assert QUERY.floor_refusal() is not None
    assert QUERY.floor_refusal((99, 0)) is None


def test_this_interpreter_satisfies_the_floor():
    assert QUERY.floor_refusal() is None


def test_the_declared_floor_matches_the_kits_one_floor():
    # Duplicated per the F5 independently-copyable rule (config_query must
    # answer before agent_common is importable); pinned equal here.
    assert tuple(QUERY.MIN_PYTHON) == tuple(load_script("agent_common").MIN_PYTHON)


# --- a config that does not validate is a refusal, not an answer --------------
def test_an_invalid_config_refuses_rather_than_answering_a_default(tmp_path, capsys):
    write_config(tmp_path, "schema = 1\n\n[policy]\nbogus = 1\n")
    assert QUERY.main(["--root", str(tmp_path), "policy.privacy_check"]) != 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "config_query: REFUSED - policy.bogus" in captured.err


def test_an_invalid_config_reports_every_finding(tmp_path, capsys):
    write_config(tmp_path, "schema = 1\n\n[policy]\nbogus = 1\nalso_bogus = 2\n")
    assert QUERY.main(["--root", str(tmp_path), "policy.push"]) != 0
    err = capsys.readouterr().err
    assert "policy.bogus" in err and "policy.also_bogus" in err


def test_a_mid_migration_tree_still_answers(tmp_path, capsys):
    # The mixed-source refusal belongs to the session preflight, NOT here: a
    # repo legitimately carries both for the length of its migration, and
    # folding that refusal in would stop the migration being committed at all.
    write_config(tmp_path, 'schema = 1\n\n[policy]\npush = "agent"\n')
    (tmp_path / "docs" / "push-policy").write_text("human\n", encoding="utf-8")
    assert CONFIG.mixed_source_findings(tmp_path) != []
    assert QUERY.main(["--root", str(tmp_path), "policy.push"]) == 0
    assert capsys.readouterr().out == "agent\n"


# --- the real subprocess the hooks actually spawn -----------------------------
def test_the_script_runs_as_a_subprocess(tmp_path):
    write_config(tmp_path, "schema = 1\n\n[policy]\nprivacy_check = true\n")
    proc = run_py(
        [SCRIPTS / "config_query.py", "--root", str(tmp_path), "policy.privacy_check"],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stdout.strip() == "true"


def test_the_script_refuses_as_a_subprocess(tmp_path):
    proc = run_py(
        [SCRIPTS / "config_query.py", "--root", str(tmp_path), "policy.nope"],
        cwd=tmp_path,
    )
    assert proc.returncode != 0
    assert proc.stdout.strip() == ""
    assert "REFUSED" in proc.stderr


def test_reading_this_repos_own_policy_agrees_with_the_old_reader():
    # The agreement bar for the cutover: over this repo, the NEW authority and
    # the OLD declared-file reader must answer the same question the same way.
    common = load_script("agent_common")
    old = common.read_declared(ROOT / "docs" / "privacy-check", "false").lower()
    proc = run_py(
        [SCRIPTS / "config_query.py", "--root", str(ROOT), "policy.privacy_check"],
        cwd=ROOT,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert proc.stdout.strip() == old
