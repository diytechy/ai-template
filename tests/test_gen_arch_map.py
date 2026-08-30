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
    # The marker OPENS its own line since OI-66: the mid-line form this fixture
    # used to carry declares nothing now, and
    # test_a_midline_marker_is_reported_not_silently_dropped covers that path.
    (src / "a.py").write_text(
        '"""Module A.\n\nContracts: IF-003, IF-004\n"""\n\n\ndef run():\n    """go"""\n',
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
    if_rows = [{"IF-ID": "IF-003", "Owner": "src/a", "Consumers": "src/b"}]
    diag = gen_arch_map.build_dependency_diagram([str(src)], if_rows)
    assert "-. IF-003 .->" in diag

    # The arrow runs the way the information does (OI-67): out of the owner on
    # a consumers row, INTO it on a requestors row — same two modules, the
    # edge reversed.
    def _edge(rows):
        return gen_arch_map._seam_edges(rows, {"a": "A", "b": "B"})

    assert _edge([{"IF-ID": "IF-006", "Owner": "a", "Consumers": "b"}]) == {
        ("A", "B", "IF-006")
    }
    assert _edge([{"IF-ID": "IF-006", "Owner": "a", "Requestors": "b"}]) == {
        ("B", "A", "IF-006")
    }
    # An owner is a PATH now, never a design id: an id-shaped owner is trace's
    # finding, and here it simply resolves to no node and draws nothing.
    assert _edge([{"IF-ID": "IF-006", "Owner": "LLR-001", "Consumers": "b"}]) == set()

    # A seam to a file / external actor is a How-SW dashboard node, not a code
    # edge — it is skipped here.
    ext = [{"IF-ID": "IF-005", "Provider": "src/a", "Consumers": "downstream adopter"}]
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
    """Does the thing.

    Implements: SR-070, LLR-071
    """
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
    # THE TOKEN MUST OPEN THE LINE (2026-08-21 review, M-3). Until then the
    # rule was only "ids after the token", so a SENTENCE that mentions the
    # token mid-line declared everything downstream of it — and two docstring
    # lines in check_trajectory.py explaining that `LLR-042` is DELIBERATELY
    # UNCLAIMED were harvested as declarations OF `LLR-042`, putting a false
    # link in a derived artifact sourced entirely from the sentence denying it.
    # A line whose token is preceded by prose declares nothing now, including
    # this previously-counted shape:
    assert f("SR-001 is history. Implements: SR-002") == []
    assert f("    DELIBERATELY UNCLAIMED (no `Implements:` line): `LLR-042`") == []
    assert f("    `Implements:` line names `LLR-042` here.") == []
    # Only whitespace, comment markers and quote characters may precede it —
    # the shapes a real declaration is actually written in.
    assert f('    """Implements: SR-005') == ["SR-005"]
    assert f("    #   Implements: SR-006") == ["SR-006"]
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
        # The declaration OPENS its line (2026-08-21 review, M-3); the
        # same-line-as-summary shape on `also()` declares nothing any more, and
        # is kept here so the narrowing is pinned rather than assumed.
        module='"""M.\n\nLLR-002 is discussed here in prose.\n"""\n\n\n'
        'def go():\n    """Go.\n\n    Implements: LLR-001\n    """\n\n\n'
        'def also():\n    """Also. Implements: LLR-003"""\n',
    )
    covered, uncovered, pct = gen_arch_map.backlink_coverage(
        [src], gen_arch_map.live_llr_ids(root)
    )
    assert covered == ["LLR-001"]
    # LLR-003's token sits after a summary sentence on the same line, so it is
    # a mention rather than a declaration — the M-3 narrowing, pinned.
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


# --- the generated CLI reference (OI-61 ruled (a), second step) ---------------

CLI_MOD = '''"""Widget CLI — demo.

Contracts: IF-101
"""

import argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", help="the tier to run")
    ap.add_argument("--strict", action="store_true", help="exit 1 on a finding")
    ap.add_argument("path")
'''

LIB_MOD = '''"""Library — no command line."""


def helper():
    """Not a CLI."""
'''


@pytest.fixture
def cli_src(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "widget.py").write_text(CLI_MOD, encoding="utf-8")
    (src / "library.py").write_text(LIB_MOD, encoding="utf-8")
    return src


def test_cli_reference_harvests_flags_help_and_declared_seams(cli_src):
    out = gen_arch_map.build_cli_reference([cli_src])
    assert "### `src/widget`" in out
    assert "_Widget CLI — demo._" in out
    # The `Contracts:` line is what makes this a REFERENCE for the interface
    # registry rather than a second document beside it.
    assert "Contracts (interfaces): IF-101" in out
    assert "| `--tier` | the tier to run |" in out
    assert "| `--strict` | exit 1 on a finding |" in out
    # A positional is a real part of the surface and is named by its dest.
    assert "| `path` |" in out
    # A module that builds no parser is not a CLI and is left out entirely —
    # the reference lists the surfaces an adopter can run, not the files.
    assert "library" not in out


def test_cli_reference_tracks_the_argparse_tree(cli_src):
    before = gen_arch_map.build_cli_reference([cli_src])
    (cli_src / "widget.py").write_text(
        CLI_MOD.replace('help="the tier to run"', 'help="the tier, renamed"'),
        encoding="utf-8",
    )
    after = gen_arch_map.build_cli_reference([cli_src])
    assert before != after
    assert "the tier, renamed" in after


def test_cli_reference_is_empty_but_honest_with_no_command_line(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "library.py").write_text(LIB_MOD, encoding="utf-8")
    out = gen_arch_map.build_cli_reference([src])
    assert "_(no command-line surface scanned)_" in out


def test_cli_doc_splices_and_check_reds_on_drift(tmp_path, cli_src):
    from conftest import run_py

    doc = tmp_path / "cli-reference.md"
    doc.write_text(
        "# CLI\n\n<!-- BEGIN GENERATED CLI REFERENCE -->\n"
        "<!-- END GENERATED CLI REFERENCE -->\n",
        encoding="utf-8",
    )
    script = Path(gen_arch_map.__file__)
    args = ["--src", str(cli_src), "--cli-doc", str(doc)]

    # A bare run writes the block; --check is then green.
    assert run_py([script] + args, cwd=tmp_path).returncode == 0
    assert "--tier" in doc.read_text(encoding="utf-8")
    assert run_py([script] + args + ["--check"], cwd=tmp_path).returncode == 0

    # Edit the argparse tree and the committed block is STALE — the whole point
    # of generating it rather than paraphrasing it by hand.
    (cli_src / "widget.py").write_text(
        CLI_MOD.replace("--tier", "--stratum"), encoding="utf-8"
    )
    red = run_py([script] + args + ["--check"], cwd=tmp_path)
    assert red.returncode == 1
    assert "STALE" in (red.stdout + red.stderr)

    # And regenerating clears it.
    assert run_py([script] + args, cwd=tmp_path).returncode == 0
    assert run_py([script] + args + ["--check"], cwd=tmp_path).returncode == 0


def test_cli_doc_is_vacuous_when_the_target_is_absent(tmp_path, cli_src):
    # The opt-in posture: a repo that has not adopted the reference has no file
    # to be stale, and the harness step must cost it nothing. (`--doc`'s
    # missing-target REFUSAL is deliberately the other way round — that target
    # is a hand-authored doc the caller named.)
    from conftest import run_py

    proc = run_py(
        [
            Path(gen_arch_map.__file__),
            "--src",
            str(cli_src),
            "--cli-doc",
            str(tmp_path / "absent.md"),
            "--check",
        ],
        cwd=tmp_path,
    )
    assert proc.returncode == 0
    assert "nothing to check" in proc.stdout


# --- OI-66 ruled (a): the component-side contract header -----------------------

CONTRACT_MOD = '''"""widget.py — the demo seam holder.

Contracts: IF-901, IF-902 — the seams this module declares.

Contract IF-901: consumes load(path) -> rows; the caller owns the parse, so a
    file that will not parse costs that module's rule rather than the run.
Contract IF-902: writes report.md; the exit code is the bounded part of the crossing.
"""
'''


@pytest.fixture()
def contract_src(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "widget.py").write_text(CONTRACT_MOD, encoding="utf-8")
    return src


def test_a_negated_contracts_line_is_not_a_declaration():
    # The defect this build was gated on: handback.py says "No `Contracts:`
    # line, deliberately: ... IF-080" and the old containment test harvested
    # IF-080 out of the denial. Line-start, not "contains the word".
    import ast

    def ids(src):
        return gen_arch_map.module_contracts(ast.parse(src), src.splitlines())

    assert ids('"""m.\n\nContracts: IF-001, IF-002 — the seams.\n"""\n') == [
        "IF-001",
        "IF-002",
    ]
    # A denial declares nothing, however it names the id.
    assert (
        ids('"""m.\n\nNo `Contracts:` line, deliberately: it extends IF-080.\n"""\n')
        == []
    )
    assert ids('"""m.\n\nSee the Contracts section for IF-003.\n"""\n') == []
    # Line-start alone was NOT enough: this opens correctly and must still
    # declare nothing, because the id list does not parse.
    assert (
        ids('"""m.\n\nContracts: not IF-080; an example, not a declaration.\n"""\n')
        == []
    )
    # A trailing full stop is ordinary writing and must not cost a declaration.
    # It is safe where a trailing `and`/comma is not: nothing can follow it, so
    # accepting it cannot drop an id.
    assert ids('"""m.\n\nContracts: IF-001, IF-002.\n"""\n') == [
        "IF-001",
        "IF-002",
    ]
    # `and` stays rejected precisely because accepting it would declare IF-001
    # and silently drop IF-002 — a partial parse is worse than none.
    assert ids('"""m.\n\nContracts: IF-001 and IF-002\n"""\n') == []
    # A separator style the tree already uses is not prose and must survive.
    assert ids('"""m.\n\nContracts: IF-061; IF-078 — semicolons.\n"""\n') == [
        "IF-061",
        "IF-078",
    ]
    # The top-of-file comment form reads the same, leading `#` and all.
    assert ids("# Contracts: IF-004 — the comment form.\nx = 1\n") == ["IF-004"]
    assert ids("# No Contracts: line here; IF-005 lives elsewhere.\nx = 1\n") == []


def test_a_contract_body_is_harvested_per_declared_seam():
    import ast

    bodies = gen_arch_map.module_contract_bodies(
        ast.parse(CONTRACT_MOD), CONTRACT_MOD.splitlines()
    )
    assert set(bodies) == {"IF-901", "IF-902"}
    # Wrapped lines join into one paragraph.
    assert bodies["IF-901"].startswith("consumes load(path) -> rows")
    assert "costs that module's rule rather than the run." in bodies["IF-901"]
    assert bodies["IF-902"] == (
        "writes report.md; the exit code is the bounded part of the crossing."
    )


def test_a_midline_marker_is_reported_not_silently_dropped():
    # Tightening a shipped grammar may not lose an adopter's declarations in
    # silence. Both lossy forms are NAMED so an upgrade tells you what stopped
    # declaring.
    import ast

    def findings(src):
        return gen_arch_map.contracts_grammar_findings(
            "demo", ast.parse(src), src.splitlines()
        )

    mid = '"""Module A. Contracts: IF-003, IF-004"""\n'
    assert any("MID-LINE" in f for f in findings(mid))

    malformed = '"""m.\n\nContracts: not IF-080; an example.\n"""\n'
    assert any("no parsable id list" in f for f in findings(malformed))

    # A clean declaration, and a denial that no longer mentions the marker,
    # both report nothing.
    assert findings('"""m.\n\nContracts: IF-001 — fine.\n"""\n') == []
    assert findings('"""m.\n\nThis module declares no seam, deliberately.\n"""\n') == []


def test_the_body_opener_does_not_collide_with_ordinary_prose():
    # A bare `IF-###:` is ordinary docstring prose — a mapping row, an example,
    # a compatibility note. Only `Contract IF-###:` opens a body, which is what
    # makes hard-failing the malformed cases safe.
    import ast

    src = (
        '"""m.\n\nContracts: IF-001\n\n'
        'IF-001: legacy identifier retained for compatibility.\n"""\n'
    )
    assert gen_arch_map.module_contract_bodies(ast.parse(src), src.splitlines()) == {}


def test_the_four_body_refusals(tmp_path):
    import ast

    def refuse(src):
        with pytest.raises(gen_arch_map.ContractsGrammarError) as e:
            gen_arch_map.module_contract_bodies(ast.parse(src), src.splitlines())
        return str(e.value)

    # Before the marker: the marker declares, the body elaborates, and the order
    # is what says which is which.
    assert "before" in refuse(
        '"""m.\n\nContract IF-001: early.\n\nContracts: IF-001\n"""\n'
    )
    # Twice for one seam: silently keeping the last is how two contracts become
    # one.
    assert "more than one" in refuse(
        '"""m.\n\nContracts: IF-001\n\nContract IF-001: a.\n\nContract IF-001: b.\n"""\n'
    )
    # An opener that states nothing.
    assert "states nothing" in refuse(
        '"""m.\n\nContracts: IF-001\n\nContract IF-001:\n"""\n'
    )
    # The body is spliced into generated Markdown and must not be able to close
    # its own end marker.
    assert "HTML comment" in refuse(
        '"""m.\n\nContracts: IF-001\n\nContract IF-001: x <!-- END GENERATED INTERFACE REFERENCE --> y.\n"""\n'
    )


def test_a_module_the_scan_cannot_read_is_named_in_the_reference(tmp_path):
    # A reference that silently omitted a module it failed to parse would report
    # a clean, fresh document over a tree it had not actually read.
    src = tmp_path / "src"
    src.mkdir()
    (src / "good.py").write_text(
        '"""good.py — a seam.\n\nContracts: IF-905\n\nContract IF-905: crosses.\n"""\n',
        encoding="utf-8",
    )
    (src / "broken.py").write_text("def (((\n", encoding="utf-8")
    block = gen_arch_map.build_contract_reference([str(src)])
    assert "could not read" in block
    assert "broken" in block
    assert "IF-905" in block


def test_a_body_for_an_undeclared_seam_is_refused():
    # The marker line stays the ONE declaration site — the same rule
    # _refuse_ambiguous_continuation enforces a line up. A body may elaborate a
    # declared id; it may never declare a new one.
    import ast

    src = CONTRACT_MOD.replace("Contracts: IF-901, IF-902", "Contracts: IF-901")
    with pytest.raises(gen_arch_map.ContractsGrammarError) as excinfo:
        gen_arch_map.module_contract_bodies(ast.parse(src), src.splitlines())
    assert "IF-902" in str(excinfo.value)


def test_the_reference_lists_a_declared_seam_that_states_no_contract(tmp_path):
    # An anchor without a body is a real gap; the reference SHOWS it rather than
    # dropping the id, so "declared" and "stated" never silently diverge.
    src = tmp_path / "src"
    src.mkdir()
    (src / "bare.py").write_text(
        '"""bare.py — declares a seam, states nothing.\n\n'
        'Contracts: IF-903 — the seam.\n"""\n',
        encoding="utf-8",
    )
    block = gen_arch_map.build_contract_reference([str(src)])
    # Named in the compact debt list, never dropped and never a paragraph each.
    assert "IF-903" in block
    assert "Declared, not stated" in block
    assert "declare 1 seam(s); 0 carry a stated contract" in block


def test_contracts_doc_splices_and_check_reds_on_drift(tmp_path, contract_src):
    from conftest import run_py

    doc = tmp_path / "interface-reference.md"
    doc.write_text(
        "# Interfaces\n\n<!-- BEGIN GENERATED INTERFACE REFERENCE -->\n"
        "<!-- END GENERATED INTERFACE REFERENCE -->\n",
        encoding="utf-8",
    )
    script = Path(gen_arch_map.__file__)
    args = ["--src", str(contract_src), "--contracts-doc", str(doc)]

    assert run_py([script] + args, cwd=tmp_path).returncode == 0
    assert "IF-901" in doc.read_text(encoding="utf-8")
    assert run_py([script] + args + ["--check"], cwd=tmp_path).returncode == 0

    # Edit the contract in the module and the committed block is STALE — which
    # is the whole reason the body lives beside the code.
    (contract_src / "widget.py").write_text(
        CONTRACT_MOD.replace("writes report.md", "writes summary.md"),
        encoding="utf-8",
    )
    red = run_py([script] + args + ["--check"], cwd=tmp_path)
    assert red.returncode == 1
    assert "STALE" in (red.stdout + red.stderr)

    assert run_py([script] + args, cwd=tmp_path).returncode == 0
    assert run_py([script] + args + ["--check"], cwd=tmp_path).returncode == 0


def test_both_doc_targets_are_processed_on_one_invocation(tmp_path, contract_src):
    # The modes COMPOSE. main() used to dispatch straight into `sys.exit` on the
    # first mode an invocation named, so `--cli-doc A --contracts-doc B --check`
    # reported A and exited 0 over a STALE B — a green verdict on a document
    # nothing had opened. Every named mode runs and the verdict is the worst.
    from conftest import run_py

    cli_doc = tmp_path / "cli-reference.md"
    cli_doc.write_text(
        "# CLI\n\n<!-- BEGIN GENERATED CLI REFERENCE -->\n"
        "<!-- END GENERATED CLI REFERENCE -->\n",
        encoding="utf-8",
    )
    contracts_doc = tmp_path / "interface-reference.md"
    contracts_doc.write_text(
        "# Interfaces\n\n<!-- BEGIN GENERATED INTERFACE REFERENCE -->\n"
        "<!-- END GENERATED INTERFACE REFERENCE -->\n",
        encoding="utf-8",
    )
    script = Path(gen_arch_map.__file__)
    args = [
        "--src",
        str(contract_src),
        "--cli-doc",
        str(cli_doc),
        "--contracts-doc",
        str(contracts_doc),
    ]

    # One invocation fills BOTH targets, and --check is then green on both.
    assert run_py([script] + args, cwd=tmp_path).returncode == 0
    assert "no command-line surface scanned" in cli_doc.read_text(encoding="utf-8")
    assert "IF-901" in contracts_doc.read_text(encoding="utf-8")
    assert run_py([script] + args + ["--check"], cwd=tmp_path).returncode == 0

    # Drift ONLY the contract body. The CLI reference is still fresh, so the
    # first mode named is green — and the run must still red on the second.
    (contract_src / "widget.py").write_text(
        CONTRACT_MOD.replace("writes report.md", "writes summary.md"),
        encoding="utf-8",
    )
    red = run_py([script] + args + ["--check"], cwd=tmp_path)
    assert red.returncode == 1
    assert "Interface reference STALE" in (red.stdout + red.stderr)

    # Both stale: both are named, not just whichever mode ran first.
    (contract_src / "tool.py").write_text(
        '''"""tool.py — a command line beside the seam holder."""

import argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", help="the tier to run")
''',
        encoding="utf-8",
    )
    both = run_py([script] + args + ["--check"], cwd=tmp_path)
    assert both.returncode == 1
    assert "CLI reference STALE" in (both.stdout + both.stderr)
    assert "Interface reference STALE" in (both.stdout + both.stderr)

    # And one regenerating run clears both.
    assert run_py([script] + args, cwd=tmp_path).returncode == 0
    assert run_py([script] + args + ["--check"], cwd=tmp_path).returncode == 0


def test_contracts_doc_is_vacuous_when_the_target_is_absent(tmp_path, contract_src):
    # Same opt-in posture as --cli-doc: a repo that has not adopted the
    # reference has no file to be stale and pays nothing for the step.
    from conftest import run_py

    proc = run_py(
        [
            Path(gen_arch_map.__file__),
            "--src",
            str(contract_src),
            "--contracts-doc",
            str(tmp_path / "absent.md"),
            "--check",
        ],
        cwd=tmp_path,
    )
    assert proc.returncode == 0
    assert "nothing to check" in (proc.stdout + proc.stderr)


# --- the adversarial round's confirmed findings, each with its reproduction ----


def test_no_id_may_survive_outside_the_parsed_list():
    # THE WORST FAILURE THIS GRAMMAR CAN HAVE is not refusing a line — it is
    # accepting one PART-WAY. `Contracts: IF-001 - IF-002` matched with `- IF-002`
    # read as trailing prose, so the module declared one seam, dropped the other,
    # and nothing said a word. A declaration that is quietly short is worse than
    # one that is refused, so a tail still carrying an id makes the whole line
    # malformed.
    import ast

    def ids(src):
        return gen_arch_map.module_contracts(ast.parse(src), src.splitlines())

    def findings(src):
        return gen_arch_map.contracts_grammar_findings(
            "demo", ast.parse(src), src.splitlines()
        )

    for lossy in (
        "Contracts: IF-001 - IF-002",
        "Contracts: IF-001 and IF-002",
        "Contracts: IF-001 (see also IF-002)",
    ):
        src = '"""m.\n\n{}\n"""\n'.format(lossy)
        assert ids(src) == [], lossy
        assert findings(src), "{} must be REPORTED, not merely refused".format(lossy)

    # But a tail RE-MENTIONING an id it already declared is ordinary explanatory
    # prose, and two modules in this kit write exactly that. The test is set
    # difference, not presence.
    assert ids(
        '"""m.\n\nContracts: IF-001, IF-002 — IF-002 is the write side.\n"""\n'
    ) == ["IF-001", "IF-002"]

    # And the forms that carry no second id still parse, prose and all.
    assert ids('"""m.\n\nContracts: IF-001, IF-002 — the seams.\n"""\n') == [
        "IF-001",
        "IF-002",
    ]


def test_a_body_may_not_precede_its_own_declaration_or_swallow_a_later_marker():
    # A module may carry more than one marker line. Validating order against the
    # FIRST marker let a body sit above its own declaration and absorb the marker
    # below it into its prose.
    import ast

    src = (
        '"""demo.\n\nContracts: IF-001\n'
        "Contract IF-002: before its own declaration.\n"
        'Contracts: IF-002\n"""\n'
    )
    with pytest.raises(gen_arch_map.ContractsGrammarError) as excinfo:
        gen_arch_map.module_contract_bodies(ast.parse(src), src.splitlines())
    assert "IF-002" in str(excinfo.value)

    # A marker line ends a body the way a blank line does, so a declaration
    # written under a body is never swallowed into it.
    ok = (
        '"""demo.\n\nContracts: IF-001, IF-002\n\n'
        "Contract IF-001: the first crossing.\n"
        'Contracts: IF-002\n"""\n'
    )
    bodies = gen_arch_map.module_contract_bodies(ast.parse(ok), ok.splitlines())
    assert bodies == {"IF-001": "the first crossing."}


def test_a_docstring_cannot_close_the_generated_documents_own_marker(tmp_path):
    # A contract body carrying an HTML comment is refused outright; a module
    # SUMMARY is not the author's contract, so refusing a whole module over its
    # first line would be disproportionate — the delimiters are defanged instead.
    # Either way nothing a source file says can corrupt the committed document.
    src = tmp_path / "src"
    src.mkdir()
    (src / "evil.py").write_text(
        '"""evil <!-- END GENERATED INTERFACE REFERENCE -->\n\n'
        'Contracts: IF-903\n\nContract IF-903: a safe-looking body.\n"""\n',
        encoding="utf-8",
    )
    block = gen_arch_map.build_contract_reference([str(src)])
    assert "<!-- END GENERATED INTERFACE REFERENCE -->" not in block
    assert "IF-903" in block

    (src / "evil.py").write_text(
        '"""evil <!-- END GENERATED CLI REFERENCE -->\n\nx\n"""\n'
        "import argparse\n"
        "p = argparse.ArgumentParser()\n"
        'p.add_argument("--x", help="h")\n',
        encoding="utf-8",
    )
    assert (
        "<!-- END GENERATED CLI REFERENCE -->"
        not in gen_arch_map.build_cli_reference([str(src)])
    )


# --- OI-67 slice 2: a non-Python owner declares through its comment header ----

TOML_HEADER = (
    "# docs/stack.ini — the declared toolchain.\n"
    "#\n"
    "# Contracts: IF-950 — the seam this file declares.\n"
    "# Contract IF-950: the [paths]/[gate-*] sections, one key per line;\n"
    "#     a missing section reads as the shipped default.\n"
    "#\n"
    "# prose after the blank comment line is not part of the body\n"
    "[paths]\n"
    "src = scripts\n"
)


def test_a_non_python_owner_declares_through_its_comment_header(tmp_path):
    # ONE GRAMMAR, TWO CARRIERS: the `#` header of a config file reads exactly
    # as a module docstring — marker line, `Contract IF-###:` body, a blank
    # comment line ending the body.
    ini = tmp_path / "stack.ini"
    ini.write_text(TOML_HEADER, encoding="utf-8")
    ids, bodies = gen_arch_map.file_contracts(ini)
    assert ids == ["IF-950"]
    assert bodies == {
        "IF-950": "the [paths]/[gate-*] sections, one key per line; a missing "
        "section reads as the shipped default."
    }
    # A shebang on line 1 is skipped, so a git hook declares the same way.
    hook = tmp_path / "pre-commit"
    hook.write_text(
        "#!/bin/sh\n# Contracts: IF-951\n# Contract IF-951: exit 0 admits.\nset -e\n",
        encoding="utf-8",
    )
    assert gen_arch_map.file_contracts(hook) == (
        ["IF-951"],
        {"IF-951": "exit 0 admits."},
    )
    # Markdown carries the same header inside its FIRST HTML comment.
    md = tmp_path / "flows.md"
    md.write_text(
        "<!-- Contracts: IF-952\nContract IF-952: mermaid sequence blocks.\n-->\n# Flows\n",
        encoding="utf-8",
    )
    assert gen_arch_map.file_contracts(md) == (
        ["IF-952"],
        {"IF-952": "mermaid sequence blocks."},
    )
    # A header is the FIRST thing in the file or it is not a header.
    late = tmp_path / "late.toml"
    late.write_text("[table]\n# Contracts: IF-953\n", encoding="utf-8")
    assert gen_arch_map.file_contracts(late) == ([], {})


def test_the_reference_lists_a_file_owner_beside_the_modules(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "mod.py").write_text('"""mod.\n\nContracts: IF-960\n"""\n', encoding="utf-8")
    ini = tmp_path / "docs" / "stack.ini"
    ini.parent.mkdir()
    ini.write_text(TOML_HEADER, encoding="utf-8")
    block = gen_arch_map.build_contract_reference([str(src)], [("docs/stack.ini", ini)])
    assert "2 source(s) declare 2 seam(s); 1 carry a stated contract" in block
    assert "### `docs/stack.ini`" in block and "**IF-950**" in block
    assert "IF-960" in block and "Declared, not stated" in block


def test_owner_files_names_the_files_and_readmes_the_registry_owns(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "stack.ini").write_text("# x\n", encoding="utf-8")
    (tmp_path / "docs" / "work").mkdir()
    (tmp_path / "docs" / "work" / "README.md").write_text("# w\n", encoding="utf-8")
    (tmp_path / "docs" / "bare").mkdir()
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "m.py").write_text("x = 1\n", encoding="utf-8")
    rows = [
        {"IF-ID": "IF-001", "Owner": "docs/stack.ini"},
        {"IF-ID": "IF-002", "Owner": "docs/work/"},  # a dir with a README
        {"IF-ID": "IF-003", "Owner": "docs/bare"},  # a dir without one: skipped
        {"IF-ID": "IF-004", "Owner": "src/m"},  # a module: the AST walk's
        {"IF-ID": "IF-005", "Owner": "external:git"},  # nothing to scan
        {"IF-ID": "IF-006", "Owner": "docs/stack.ini"},  # deduplicated
    ]
    assert gen_arch_map.owner_files(tmp_path, rows) == [
        ("docs/stack.ini", tmp_path / "docs" / "stack.ini"),
        ("docs/work/", tmp_path / "docs" / "work" / "README.md"),
    ]


def test_a_lossy_marker_in_a_file_header_is_reported_by_name(tmp_path):
    ini = tmp_path / "x.toml"
    ini.write_text("# Contracts: IF-970 - IF-971\n[t]\n", encoding="utf-8")
    found = gen_arch_map.file_grammar_findings("docs/x.toml", ini)
    assert len(found) == 1 and "docs/x.toml" in found[0]
    assert "declares no parsable id list" in found[0]
