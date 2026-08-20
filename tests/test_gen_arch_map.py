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


def _map_doc(scaffold):
    """A routed --doc target with the marker pair (WI-455: no scaffolded
    docs/architecture.md exists, so the CLI is exercised the way an adopter
    routes the map — an explicit --doc)."""
    doc = scaffold / "docs" / "code-map.md"
    doc.write_text(
        "# Map\n<!-- BEGIN GENERATED MODULE MAP -->\n"
        "<!-- END GENERATED MODULE MAP -->\n",
        encoding="utf-8",
    )
    return "docs/code-map.md"


def test_files_mode_end_to_end_and_staleness(scaffold):
    from conftest import run_py

    src = scaffold / "src"
    src.mkdir(exist_ok=True)
    (src / "app.ts").write_text(
        "// The TS entry point.\nexport const x = 1\n", encoding="utf-8"
    )
    doc = _map_doc(scaffold)
    proc = run_py(
        ["scripts/gen_arch_map.py", "--mode", "files", "--doc", doc], cwd=scaffold
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    arch = (scaffold / doc).read_text(encoding="utf-8")
    assert "src/app.ts" in arch and "The TS entry point." in arch
    # freshly generated ⇒ --check is green
    proc = run_py(
        ["scripts/gen_arch_map.py", "--mode", "files", "--doc", doc, "--check"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # add a file ⇒ stale ⇒ --check fails (the drift lever works for a TS/Go repo)
    (src / "util.go").write_text("// Helpers.\npackage util\n", encoding="utf-8")
    proc = run_py(
        ["scripts/gen_arch_map.py", "--mode", "files", "--doc", doc, "--check"],
        cwd=scaffold,
    )
    assert proc.returncode == 1
    assert "STALE" in proc.stderr


def test_files_mode_rejects_flow(scaffold):
    from conftest import run_py

    proc = run_py(
        [
            "scripts/gen_arch_map.py",
            "--mode",
            "files",
            "--flow",
            "run",
            "--doc",
            _map_doc(scaffold),
        ],
        cwd=scaffold,
    )
    assert proc.returncode != 0
    assert "flow" in (proc.stdout + proc.stderr).lower()


def test_files_mode_zero_source_warns_without_self_reference(scaffold):
    # In files mode the fallback IS running, so the warning must not tell the
    # user to switch to the mode they're already in.
    from conftest import run_py

    proc = run_py(
        ["scripts/gen_arch_map.py", "--mode", "files", "--doc", _map_doc(scaffold)],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "no source scanned" in proc.stderr
    assert "--mode files" not in proc.stderr


def test_zero_source_scan_warns_loudly(scaffold):
    # A repo whose code isn't Python (or has none yet) must not get a silently
    # vacuous map + freshness gate: the run stays green (pre-code repos are
    # legitimate) but says on stderr that the guarantee is not in force and
    # points at the porting contract (ADOPTING.md).
    from conftest import run_py

    doc = _map_doc(scaffold)
    run_py(["scripts/gen_arch_map.py", "--doc", doc], cwd=scaffold)
    proc = run_py(["scripts/gen_arch_map.py", "--doc", doc, "--check"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "no source scanned" in proc.stderr
    assert "ADOPTING.md" in proc.stderr


# --- WI-363: the hidden-file skip is RELATIVE to the scan root -----------------


@pytest.fixture
def dot_ancestor_src(tmp_path):
    """A two-module scan root sitting under a deliberately dot-prefixed
    ancestor — the shape a checkout in `~/.local/src`, a CI cache directory, or
    a `PYTEST_DEBUG_TEMPROOT` pointed at a dot-directory produces. Nothing about
    the tree *inside* the root is hidden."""
    src = tmp_path / ".cache" / "checkout" / "src"
    src.mkdir(parents=True)
    (src / "a.py").write_text(MOD_A, encoding="utf-8")
    (src / "b.py").write_text(MOD_B, encoding="utf-8")
    return str(src)


def test_dot_prefixed_ancestor_does_not_suppress_the_scan(dot_ancestor_src):
    # Regression: the skip tested the ABSOLUTE path parts, so one dot-prefixed
    # directory anywhere above the checkout emptied every collector at exit 0.
    out = gen_arch_map.build_map([dot_ancestor_src])
    assert "(no source scanned)" not in out
    assert "Module A — demo." in out and "`helper_b()`" in out
    diagram = gen_arch_map.build_dependency_diagram([dot_ancestor_src])
    assert "(no source scanned)" not in diagram
    # the parser-backed collectors travel the same walk
    assert "Run B." in gen_arch_map.build_flow([dot_ancestor_src], "b:run")
    assert gen_arch_map.collect_parse_errors([dot_ancestor_src]) == []


def test_files_mode_scans_under_a_dot_prefixed_ancestor(tmp_path):
    src = tmp_path / ".pytest-tmp" / "src"
    src.mkdir(parents=True)
    (src / "a.js").write_text("// Alpha.\n", encoding="utf-8")
    out = gen_arch_map.build_files_map(
        [str(src)], gen_arch_map.DEFAULT_COMMENT_PREFIXES
    )
    assert "`src/a.js`" in out and "Alpha." in out


def test_hidden_dir_inside_the_scan_root_is_still_skipped(two_module_src):
    # The preserved direction: root-relative dot/__pycache__ parts stay filtered.
    src = Path(two_module_src)
    (src / ".hidden").mkdir()
    (src / ".hidden" / "secret.py").write_text(
        '"""Secret module."""\n', encoding="utf-8"
    )
    (src / "__pycache__").mkdir()
    (src / "__pycache__" / "stale.py").write_text(
        '"""Stale artifact."""\n', encoding="utf-8"
    )
    out = gen_arch_map.build_map([two_module_src])
    assert "Secret module." not in out and "Stale artifact." not in out
    assert "Module A — demo." in out  # the visible modules still land
    files = gen_arch_map.build_files_map(
        [two_module_src], gen_arch_map.DEFAULT_COMMENT_PREFIXES
    )
    assert ".hidden" not in files and "__pycache__" not in files


def test_zero_modules_from_a_hidden_only_src_warns(scaffold):
    # The sharper of the two empty-scan warnings: the root DOES hold modules,
    # but a dot-prefixed directory inside it ate them all. Exit stays 0.
    from conftest import run_py

    # A fresh scaffold's src holds only .gitkeep — empty by design, so the
    # sharper warning must not cry wolf (a dot-prefixed FILE is not the shape).
    doc = _map_doc(scaffold)
    proc = run_py(["scripts/gen_arch_map.py", "--doc", doc], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "no source scanned" in proc.stderr
    assert "skipped as hidden" not in proc.stderr

    (scaffold / "src" / ".vendor").mkdir()
    (scaffold / "src" / ".vendor" / "app.py").write_text(
        '"""App."""\n', encoding="utf-8"
    )
    proc = run_py(["scripts/gen_arch_map.py", "--doc", doc], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "skipped as hidden" in proc.stderr
    assert "src/.vendor" in proc.stderr  # names the directory, not just the root


# --- WI-056: Contracts: docstring harvest + declared IF edges in the diagram ----


def test_contracts_and_if_edges(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "a.py").write_text(
        '"""Module A. Contracts: IF-003, IF-004"""\n\n\ndef run():\n    """go"""\n',
        encoding="utf-8",
    )
    (src / "b.py").write_text(
        '"""Module B."""\n\n\ndef go():\n    """g"""\n', encoding="utf-8"
    )
    out = gen_arch_map.build_map([str(src)])
    # The Contracts: docstring line is harvested into the module map (the oracle
    # check_trajectory reads for the docstring-vs-registry coverage warn).
    assert "Contracts (interfaces): IF-003, IF-004" in out

    # A module<->module IF row becomes a dotted, labeled edge, distinct from the
    # solid import arrows.
    if_rows = [
        {
            "IF-ID": "IF-003",
            "Direction": "Provides",
            "ThisProject": "src/a",
            "Counterpart": "src/b",
        }
    ]
    diag = gen_arch_map.build_dependency_diagram([str(src)], if_rows)
    assert "-. IF-003 .->" in diag

    # A seam to a file / external actor is a How-SW dashboard node, not a code
    # edge — it is skipped here.
    ext = [
        {
            "IF-ID": "IF-005",
            "Direction": "Provides",
            "ThisProject": "src/a",
            "Counterpart": "downstream adopter",
        }
    ]
    assert "IF-005" not in gen_arch_map.build_dependency_diagram([str(src)], ext)


# --- WI-478: the Contracts continuation grammar --------------------------------
# dispatch.py's real defect: `Contracts: IF-015 (...),` wraps mid-list, so
# IF-088/IF-089 each open their own continuation line instead of sitting on the
# marker line — the old harvester only ever scanned lines containing the literal
# word "Contracts", so both ids silently read as undeclared (two false
# check_trajectory --strict warnings on visibly-declared interfaces).


def test_contracts_continuation_refuses_ambiguous_wrap(tmp_path):
    """A multiline `Contracts:` block shaped exactly like dispatch.py's old
    defect — a marker line declaring one id, then further comma-separated list
    items that each wrap onto their OWN line — must not silently drop the
    wrapped ids. The declared marker-line-only grammar (WI-478) refuses the
    shape instead."""
    src = tmp_path / "src"
    src.mkdir()
    (src / "d.py").write_text(
        '"""D.\n\n'
        "Contracts: IF-015 (one seam),\n"
        "IF-088 (a continuation-line seam the old harvester missed),\n"
        "IF-089 (a second one).\n"
        '"""\n\n\ndef run():\n    """go"""\n',
        encoding="utf-8",
    )
    with pytest.raises(gen_arch_map.ContractsGrammarError, match="IF-088"):
        gen_arch_map.build_map([str(src)])


def test_contracts_continuation_may_repeat_a_marker_id(tmp_path):
    """A continuation line that opens with an id ALREADY on the marker line —
    the shape the kit's own modules use throughout (e.g. `Contracts: IF-084,
    IF-130 ...` followed by prose starting "IF-130 is...") — is ordinary
    explanatory prose, not ambiguous, and must still harvest cleanly."""
    src = tmp_path / "src"
    src.mkdir()
    (src / "d.py").write_text(
        '"""D.\n\n'
        "Contracts: IF-003, IF-004 - the seams this module declares.\n"
        "IF-004 is what this module provides to its one caller.\n"
        '"""\n\n\ndef run():\n    """go"""\n',
        encoding="utf-8",
    )
    out = gen_arch_map.build_map([str(src)])
    assert "Contracts (interfaces): IF-003, IF-004" in out


def test_if_edges_absent_registry_is_vacuous(tmp_path):
    # No IF rows -> the diagram is exactly the import graph (never-breaking).
    src = tmp_path / "src"
    src.mkdir()
    (src / "a.py").write_text(
        '"""A."""\n\n\ndef run():\n    """go"""\n', encoding="utf-8"
    )
    assert "-. " not in gen_arch_map.build_dependency_diagram([str(src)], [])
    assert "-. " not in gen_arch_map.build_dependency_diagram([str(src)], None)


# --- module_bindings: the symbol oracle the spine consumes (WI-429) -----------


def test_module_bindings_covers_every_rendered_public_item():
    """THE DRIFT GUARD. `module_bindings` and `scan_module` are two AST walks in
    one file — the residual cost of keeping symbol extraction in ONE module
    rather than copying a parser into the consumer (the D-6/F5 hazard). This
    pins them: every public item the map RENDERS for a module must be a name
    `module_bindings` reports for that module, across every module in this repo.
    A node type one walk learns and the other does not then reds here instead of
    silently reporting "that symbol does not exist" on the spine."""
    import ast

    from conftest import KIT

    files, internal = gen_arch_map._module_files([KIT])
    assert files, "the kit must have modules to check"
    checked = 0
    for path, base in files:
        rel, _summary, _imports, _contracts, rows = gen_arch_map.scan_module(
            path, base, internal
        )
        rendered = {
            name[: -len(" (class)")] if name.endswith(" (class)") else name
            for name, _sig, _summ, _ids in rows
            if name != "  methods"
        }
        if not rendered:
            continue
        bound = gen_arch_map.module_bindings(
            ast.parse(path.read_text(encoding="utf-8"))
        )
        assert rendered <= bound, "{}: rendered but not bound: {}".format(
            rel, sorted(rendered - bound)
        )
        checked += 1
    assert checked > 20, "the guard must actually have walked the kit"


def test_module_bindings_sees_what_the_rendered_map_cannot(tmp_path):
    """The whole reason this function exists: private helpers, module constants
    and class methods are real code the PUBLIC map deliberately drops."""
    import ast

    tree = ast.parse(
        "CONST = 1\n"
        "ANNOTATED: int = 2\n"
        "def _private():\n    pass\n"
        "def public():\n    pass\n"
        "class Klass:\n"
        "    def method(self):\n        pass\n"
        "    def _hidden(self):\n        pass\n"
    )
    bound = gen_arch_map.module_bindings(tree)
    assert bound == {
        "CONST",
        "ANNOTATED",
        "_private",
        "public",
        "Klass",
        "method",
        "_hidden",
    }


def test_module_bindings_stops_at_module_scope():
    """A function LOCAL is not a name the module offers. The census found
    `budget_findings` and `tier_legend` cited as symbols when both are locals;
    reporting them as bound would make the spine's answer meaningless."""
    import ast

    bound = gen_arch_map.module_bindings(
        ast.parse("def outer():\n    a_local = 1\n    def inner():\n        pass\n")
    )
    assert bound == {"outer"}


# --- WI-486: the literal back-link grammar + reverse coverage -----------------
# OI-42's measurement over this repo's own 781 public symbols: 50 got a
# non-empty `Implements` column carrying 62 back-links, 60 of which nobody had
# declared and 13 of which named no live row — `trace.id_sort_key`'s SORTING
# example ("SR-9 orders before SR-10") was recorded as two requirements that
# function implements. These pin the grammar that ended it, and the scan that
# runs it in reverse.


PROSE_MOD = '''"""A module whose prose merely MENTIONS spine ids.

SR-9 orders before SR-10 here — a sorting illustration, not a declaration.
"""


# A comment above the def naming LLR-1 and SR-2, as a counter-example.
def sorted_ids():
    """Explain that a TC citing LLR-1 next to SR-2 is the shape to avoid."""


def declared():
    """Does the thing. Implements: SR-070, LLR-071"""
'''


def test_prose_ids_near_a_symbol_are_no_longer_harvested(tmp_path):
    """THE REGRESSION PIN for OI-42's central defect: an id in a docstring
    sentence, or in a comment line above a `def`, is PROSE. Only a line carrying
    the literal token declares. Before WI-486 every id below was harvested and
    the map reported them as implemented requirements."""
    src = tmp_path / "src"
    src.mkdir()
    (src / "m.py").write_text(PROSE_MOD, encoding="utf-8")
    # The COLUMN, not the whole map: the rendered summary legitimately quotes
    # the prose those ids sit in — what must be empty is the back-link cell.
    ((_rel, _summary, _imports, _contracts, rows),) = gen_arch_map.scan_inventory(
        [str(src)]
    )
    column = {name: ids for name, _sig, _summ, ids in rows}
    assert column["sorted_ids"] == []
    # ...and the one real declaration still lands, or the tightening would have
    # emptied the column by breaking it rather than by being honest.
    assert column["declared"] == ["LLR-071", "SR-070"]
    assert "| LLR-071, SR-070 |" in gen_arch_map.build_map([str(src)])


def test_backlink_ids_is_the_one_definition_of_a_declaration():
    """The shared grammar itself, driven directly — `implements()` and
    `scan_backlinks()` both read it, so a divergence here is a divergence
    between the map's column and the coverage percentage."""
    f = gen_arch_map.backlink_ids
    assert f("    Implements: SR-007, LLR-014") == ["SR-007", "LLR-014"]
    assert f("# Implements: TC-003 and SN-004") == ["TC-003", "SN-004"]
    # No token: prose, however many ids it names.
    assert f("SR-9 orders before SR-10") == []
    assert f("see LLR-014 for the design") == []
    # An id BEFORE the token is not declared by it — position is the rule.
    assert f("SR-001 is history. Implements: SR-002") == ["SR-002"]
    # A wrapped list item is not a declaration; it is refused for `Contracts:`
    # and simply uncounted here (the module docstring states the asymmetry).
    assert f("  LLR-015 (the second item of a wrapped list),") == []


def _backlink_repo(tmp_path, llr_rows, dial=None, module=None):
    """A minimal repo: an LLR registry, an optional process.toml dial, and one
    source module. Returns (root, src_root)."""
    root = tmp_path
    (root / "docs" / "requirements").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "requirements" / "low-level-requirements.toml").write_text(
        "".join('[design."{}"]\ntitle = "row"\n'.format(r) for r in llr_rows),
        encoding="utf-8",
    )
    if dial is not None:
        (root / "docs" / "process.toml").write_text(
            "[checks]\nbacklink_coverage_min = {}\n".format(dial), encoding="utf-8"
        )
    src = root / "src"
    src.mkdir(exist_ok=True)
    if module is not None:
        (src / "m.py").write_text(module, encoding="utf-8")
    return root, str(src)


def test_reverse_coverage_counts_only_declarations(tmp_path):
    """The percentage is over LIVE LLR ROWS, and only a literal declaration
    covers one. The `-000` template row is not live and must not enter the
    denominator (a placeholder would otherwise dilute every fresh scaffold)."""
    root, src = _backlink_repo(
        tmp_path,
        ["LLR-000", "LLR-001", "LLR-002", "LLR-003"],
        module='"""M.\n\nLLR-002 is discussed here in prose.\n"""\n\n\n'
        'def go():\n    """Go. Implements: LLR-001"""\n',
    )
    covered, uncovered, pct = gen_arch_map.backlink_coverage(
        [src], gen_arch_map.live_llr_ids(root)
    )
    assert covered == ["LLR-001"]
    assert uncovered == ["LLR-002", "LLR-003"]  # the prose mention covers nothing
    assert round(pct, 1) == 33.3  # 1 of 3 live rows, LLR-000 excluded


def test_reverse_coverage_reads_non_python_source_but_not_unlisted_types(tmp_path):
    """Language-agnostic BY CONSTRUCTION — it reads comment text, not syntax —
    but only for the declared extension list. The `.md` case is the guard for
    OI-42's asymmetry: widening the list can only RAISE the score, so an
    over-inclusive default would score prose files as carriers."""
    root, src = _backlink_repo(tmp_path, ["LLR-001", "LLR-002"])
    (tmp_path / "src" / "run.go").write_text(
        "// Implements: LLR-001\nfunc main() {}\n", encoding="utf-8"
    )
    (tmp_path / "src" / "notes.md").write_text(
        "Implements: LLR-002\n", encoding="utf-8"
    )
    found = gen_arch_map.scan_backlinks([src])
    assert found == {"LLR-001": ["src/run.go"]}
    _covered, _unc, pct = gen_arch_map.backlink_coverage(
        [src], gen_arch_map.live_llr_ids(root)
    )
    assert pct == 50.0
    # ...and the list is overridable per repo, which is the declared escape.
    assert "LLR-002" in gen_arch_map.scan_backlinks([src], (".md",))


def test_the_dial_reads_zero_for_everything_it_cannot_trust(tmp_path):
    """0 is report-only AND the fallback: a threshold has no conservative
    default to fail toward, so an unreadable dial must not invent a bar. The
    loud half is `agent_common.PROCESS_ONLY_KEYS`, which refuses the wrong type
    outright — pinned in tests/test_rule_sync.py."""
    root, _src = _backlink_repo(tmp_path, ["LLR-001"], dial=50)
    assert gen_arch_map.read_backlink_min(root) == 50
    for bad in ('"50"', "true", "-1", "101"):
        (root / "docs" / "process.toml").write_text(
            "[checks]\nbacklink_coverage_min = {}\n".format(bad), encoding="utf-8"
        )
        assert gen_arch_map.read_backlink_min(root) == 0, bad
    (root / "docs" / "process.toml").unlink()
    assert gen_arch_map.read_backlink_min(root) == 0


def test_the_report_is_vacuous_without_llr_rows_and_gates_only_above_the_dial(
    tmp_path,
):
    """Three postures in one place, because they are one decision: no rows =
    vacuous (a fresh scaffold pays nothing), dial 0 = report the number and gate
    nothing (what the kit ships), dial above the measurement = the warning."""
    root, src = _backlink_repo(tmp_path, [])
    lines, ok = gen_arch_map.backlink_report([src], root)
    assert ok and "vacuous" in lines[0]

    root, src = _backlink_repo(tmp_path, ["LLR-001", "LLR-002"], dial=0)
    lines, ok = gen_arch_map.backlink_report([src], root)
    assert ok, lines
    assert "0/2 live LLR rows (0.0%)" in lines[0]
    assert "REPORT-ONLY" in lines[1]

    (root / "docs" / "process.toml").write_text(
        "[checks]\nbacklink_coverage_min = 50\n", encoding="utf-8"
    )
    lines, ok = gen_arch_map.backlink_report([src], root)
    assert not ok
    assert "WARNING" in lines[1] and "LLR-001" in lines[1]


def test_backlink_cli_is_warn_first_and_strict_only_on_demand(scaffold):
    """The exit contract, driven through the real CLI on a real scaffold: the
    report never needs a --doc target, a below-bar reading WARNS at exit 0, and
    only --strict-backlinks turns it into a failure. check.py appends that flag
    from DevStg-Tests on, which is what makes the dial a gate an adopter opts
    into rather than one the kit arms for them."""
    from conftest import run_py

    (scaffold / "docs" / "requirements" / "low-level-requirements.toml").write_text(
        '[design."LLR-001"]\ntitle = "row"\n', encoding="utf-8"
    )
    (scaffold / "docs" / "process.toml").write_text(
        "[checks]\nbacklink_coverage_min = 50\n", encoding="utf-8"
    )
    args = [
        "scripts/gen_arch_map.py",
        "--backlink-coverage",
        "--root",
        ".",
        "--src",
        "src",
    ]
    warn = run_py(args, cwd=scaffold)
    assert warn.returncode == 0
    assert "0/1 live LLR rows" in warn.stdout + warn.stderr
    strict = run_py(args + ["--strict-backlinks"], cwd=scaffold)
    assert strict.returncode == 1
    assert "WARNING" in strict.stdout + strict.stderr
