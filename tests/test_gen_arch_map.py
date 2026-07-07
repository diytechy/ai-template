"""gen_arch_map.py: map content, flow entry resolution, the Mermaid dependency
diagram, and splice safety."""

from pathlib import Path

import pytest

from conftest import load_script

gen_arch_map = load_script("gen_arch_map")

MOD_A = '''"""Module A — demo."""


def helper_a():
    """Helper in A."""


def run():
    """Run A. Implements: SR-001"""
    helper_a()
'''

MOD_B = '''"""Module B — demo."""


def helper_b():
    """Helper in B."""


def run():
    """Run B."""
    helper_b()
'''


@pytest.fixture
def two_module_src(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "a.py").write_text(MOD_A, encoding="utf-8")
    (src / "b.py").write_text(MOD_B, encoding="utf-8")
    return str(src)


def test_map_harvests_summaries_and_implements(two_module_src):
    out = gen_arch_map.build_map([two_module_src])
    assert "Module A — demo." in out
    assert "SR-001" in out  # Implements back-link from the docstring
    assert "`helper_b()`" in out


def test_flow_module_qualifier_selects_the_right_run(two_module_src):
    # Regression: the `module:entry` form used to be accepted but ignored.
    flow_b = gen_arch_map.build_flow([two_module_src], "b:run")
    assert "Run B." in flow_b
    assert "helper_b" in flow_b
    assert "helper_a" not in flow_b


def test_flow_ambiguous_bare_name_errors(two_module_src):
    with pytest.raises(SystemExit, match="ambiguous"):
        gen_arch_map.build_flow([two_module_src], "run")


def test_flow_unknown_entry_errors(two_module_src):
    with pytest.raises(SystemExit, match="not found"):
        gen_arch_map.build_flow([two_module_src], "nope")


def test_dependency_diagram_renders_absolute_imports(two_module_src):
    (Path(two_module_src) / "c.py").write_text(
        '"""Module C — uses B."""\n\nimport b\n', encoding="utf-8"
    )
    out = gen_arch_map.build_dependency_diagram([two_module_src])
    assert "```mermaid" in out and "graph LR" in out
    assert 'm_src_c["src/c — Module C — uses B."]' in out  # labeled node
    assert "m_src_c --> m_src_b" in out  # the import edge
    assert "m_src_a --> " not in out  # a imports nothing


def test_dependency_diagram_resolves_relative_imports(tmp_path):
    pkg = tmp_path / "src" / "pkg"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text('"""Package demo."""\n', encoding="utf-8")
    (pkg / "util.py").write_text(
        '"""Util — pure helpers."""\n\n\ndef util():\n    """Helper."""\n',
        encoding="utf-8",
    )
    (pkg / "mod.py").write_text(
        '"""Mod — uses util."""\n\nfrom .util import util\n\n\n'
        'def go():\n    """Go."""\n    util()\n',
        encoding="utf-8",
    )
    out = gen_arch_map.build_dependency_diagram([str(tmp_path / "src")])
    assert "m_src_pkg_mod --> m_src_pkg_util" in out
    assert "src/pkg/mod" in out  # node labels carry the module path


def test_dependency_diagram_from_import_targets_the_submodule(tmp_path):
    # `from export import io` depends on export/io, not just the package;
    # `from .util import util` (name shadowing the module) targets the module.
    src = tmp_path / "src"
    pkg = src / "export"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text('"""Export package."""\n', encoding="utf-8")
    (pkg / "io.py").write_text('"""IO shell."""\n', encoding="utf-8")
    (src / "cli.py").write_text(
        '"""CLI entry."""\n\nfrom export import io\n', encoding="utf-8"
    )
    out = gen_arch_map.build_dependency_diagram([str(src)])
    assert "m_src_cli --> m_src_export_io" in out
    assert "m_src_cli --> m_src_export\n" not in out


def test_dependency_diagram_empty_src(tmp_path):
    out = gen_arch_map.build_dependency_diagram([str(tmp_path / "nothing")])
    assert "(no source scanned)" in out


def test_collect_parse_errors_flags_bad_module(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "ok.py").write_text('"""OK."""\n', encoding="utf-8")
    (src / "bad.py").write_text("def oops(:\n    pass\n", encoding="utf-8")
    errs = gen_arch_map.collect_parse_errors([str(src)])
    assert [rel for rel, _ in errs] == ["src/bad"]


def test_collect_parse_errors_clean_tree(two_module_src):
    assert gen_arch_map.collect_parse_errors([two_module_src]) == []


def test_splice_refuses_duplicated_markers():
    b, e = gen_arch_map.BEGIN, gen_arch_map.END
    doc = "x\n{b}\nold\n{e}\ny\n{b}\nagain\n{e}\n".format(b=b, e=e)
    with pytest.raises(SystemExit, match="duplicated marker"):
        gen_arch_map.splice_region(doc, b, e, "new", "doc.md", required=True)


def test_splice_replaces_between_markers():
    b, e = gen_arch_map.BEGIN, gen_arch_map.END
    doc = "intro\n{}\nold\n{}\noutro\n".format(b, e)
    out = gen_arch_map.splice_region(doc, b, e, "new", "doc.md", required=True)
    assert "old" not in out
    assert "new" in out
    assert out.startswith("intro\n") and out.endswith("outro\n")


def test_first_comment_summary_variants():
    f = gen_arch_map.first_comment_summary
    p = gen_arch_map.DEFAULT_COMMENT_PREFIXES
    assert (
        f("#!/usr/bin/env node\n// Real summary.\n", p) == "Real summary."
    )  # shebang skipped
    assert f("# Top comment\n", p) == "Top comment"
    assert f("-- SQL module summary\n", p) == "SQL module summary"
    assert f("/// Rust doc line\n", p) == "Rust doc line"  # extra slash stripped
    assert (
        f("export const x = 1\n// later\n", p) == ""
    )  # opens with code, not a comment
    assert f("", p) == ""
    assert f("<!-- HTML page -->\n", ("<!--",)) == "HTML page"  # block close stripped


def test_files_mode_reflects_tree_changes(tmp_path):
    # The whole point of --mode files: a real freshness check for any stack.
    src = tmp_path / "src"
    src.mkdir()
    (src / "a.js").write_text("// Alpha.\n", encoding="utf-8")
    (src / "b.rb").write_text("# Beta.\n", encoding="utf-8")
    p = gen_arch_map.DEFAULT_COMMENT_PREFIXES
    m1 = gen_arch_map.build_files_map([str(src)], p)
    assert "`src/a.js`" in m1 and "Alpha." in m1
    assert "`src/b.rb`" in m1 and "Beta." in m1
    assert "--mode files" in m1  # note names the fallback
    # rename ⇒ map changes (add/remove behave the same way)
    (src / "b.rb").rename(src / "c.rb")
    m2 = gen_arch_map.build_files_map([str(src)], p)
    assert m2 != m1 and "`src/c.rb`" in m2 and "`src/b.rb`" not in m2
    # summary edit ⇒ map changes
    (src / "a.js").write_text("// Alpha renamed.\n", encoding="utf-8")
    m3 = gen_arch_map.build_files_map([str(src)], p)
    assert m3 != m2 and "Alpha renamed." in m3


def test_files_map_empty_scan(tmp_path):
    out = gen_arch_map.build_files_map([str(tmp_path / "nothing")], ("#",))
    assert "(no source scanned)" in out


def test_symbols_mode_unaffected_by_files_addition(two_module_src):
    # Regression guard: the default (symbols) map still emits symbol-level rows,
    # not file rows — --mode files is strictly additive/opt-in.
    out = gen_arch_map.build_map([two_module_src])
    assert "`helper_a()`" in out  # a symbol signature, not a file path
    assert "--mode files" not in out  # not the fallback note


def test_files_mode_end_to_end_and_staleness(scaffold):
    from conftest import run_py

    src = scaffold / "src"
    src.mkdir(exist_ok=True)
    (src / "app.ts").write_text(
        "// The TS entry point.\nexport const x = 1\n", encoding="utf-8"
    )
    proc = run_py(["scripts/gen_arch_map.py", "--mode", "files"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    arch = (scaffold / "docs" / "architecture.md").read_text(encoding="utf-8")
    assert "src/app.ts" in arch and "The TS entry point." in arch
    # freshly generated ⇒ --check is green (the arch-map step passes)
    proc = run_py(
        ["scripts/gen_arch_map.py", "--mode", "files", "--check"], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # add a file ⇒ stale ⇒ --check fails (the drift lever works for a TS/Go repo)
    (src / "util.go").write_text("// Helpers.\npackage util\n", encoding="utf-8")
    proc = run_py(
        ["scripts/gen_arch_map.py", "--mode", "files", "--check"], cwd=scaffold
    )
    assert proc.returncode == 1
    assert "STALE" in proc.stderr


def test_files_mode_rejects_flow(scaffold):
    from conftest import run_py

    proc = run_py(
        ["scripts/gen_arch_map.py", "--mode", "files", "--flow", "run"], cwd=scaffold
    )
    assert proc.returncode != 0
    assert "flow" in (proc.stdout + proc.stderr).lower()


def test_files_mode_zero_source_warns_without_self_reference(scaffold):
    # In files mode the fallback IS running, so the warning must not tell the
    # user to switch to the mode they're already in.
    from conftest import run_py

    proc = run_py(["scripts/gen_arch_map.py", "--mode", "files"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "no source scanned" in proc.stderr
    assert "--mode files" not in proc.stderr


def test_zero_source_scan_warns_loudly(scaffold):
    # A repo whose code isn't Python (or has none yet) must not get a silently
    # vacuous map + freshness gate: the run stays green (pre-code repos are
    # legitimate) but says on stderr that the guarantee is not in force and
    # points at the porting contract (ADOPTING.md).
    from conftest import run_py

    proc = run_py(["scripts/gen_arch_map.py", "--check"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "no source scanned" in proc.stderr
    assert "ADOPTING.md" in proc.stderr
