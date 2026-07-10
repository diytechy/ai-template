"""check_doc_refs.py — dangling path/symbol references in prose (Thread 49).

False-positive control is the design center: only path-shaped backticked
tokens and the explicit `sym:` convention are validated — never every
backticked word. Warn-first (exit 0) unless --strict; the sym: tier skips
cleanly without a module-map inventory. Exercised over temp repos.
"""

from conftest import SCRIPTS, run_py

ARCH = """# Architecture

<!-- BEGIN GENERATED MODULE MAP -->
### `src/demo`
_Demo module._

| Public item | Summary | Implements |
|---|---|---|
| `add(a, b)` | Adds. |  |
| `sub(a, b)` | Subtracts. |  |
<!-- END GENERATED MODULE MAP -->
"""


def make_repo(root, body, with_arch=True):
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "README.md").write_text(body, encoding="utf-8")
    if with_arch:
        (root / "docs" / "architecture.md").write_text(ARCH, encoding="utf-8")
    (root / "scripts").mkdir(exist_ok=True)
    (root / "scripts" / "real.py").write_text("x = 1\n", encoding="utf-8")
    return root


def refs(root, *args):
    return run_py([SCRIPTS / "check_doc_refs.py", *args], cwd=root)


def test_existing_path_and_symbol_pass(tmp_path):
    make_repo(tmp_path, "See `scripts/real.py` and sym:demo.add for the core.\n")
    proc = refs(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "OK" in proc.stdout


def test_dangling_path_warns_then_gates_under_strict(tmp_path):
    make_repo(tmp_path, "The old `scripts/deleted.py` did this.\n")
    proc = refs(tmp_path)
    assert proc.returncode == 0, "warn-first: findings must not gate by default"
    assert "scripts/deleted.py" in proc.stderr
    strict = refs(tmp_path, "--strict")
    assert strict.returncode == 1


def test_non_path_backticks_urls_and_globs_are_ignored(tmp_path):
    make_repo(
        tmp_path,
        "Use `off` or `type`; see `https://example.com/a.py` and "
        "`scripts/*.py` and `docs/{name}.md` shapes.\n",
    )
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_path_ok_line_is_exempt(tmp_path):
    make_repo(
        tmp_path,
        "A downstream repo gets `scripts/not-here.py` <!-- path-ok -->\n",
    )
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_dangling_symbol_is_flagged_against_the_inventory(tmp_path):
    make_repo(tmp_path, "Call sym:demo.multiply to combine.\n")
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 1
    assert "multiply" in proc.stderr and "public inventory" in proc.stderr


def test_unknown_module_is_flagged(tmp_path):
    make_repo(tmp_path, "See sym:ghost.add.\n")
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 1
    assert "not in the module map" in proc.stderr


def test_node_ids_and_joined_lists_are_not_path_flagged(tmp_path):
    # A2: a pytest node id (the sanctioned Evidence form) and a ;-joined path
    # list are not single filesystem paths — the path tier must not flag them.
    make_repo(
        tmp_path,
        "Evidence `tests/real.py::test_it` and `tests/real.py;scripts/real.py`.\n",
    )
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_generated_linguist_tree_is_not_linted(tmp_path):
    # A2: a dir marked linguist-generated in .gitattributes (e.g. docs/okf/) is
    # the generator's output — never hand-authored prose — so it is skipped,
    # even when it names a path that doesn't exist here.
    make_repo(tmp_path, "clean root doc\n")
    (tmp_path / ".gitattributes").write_text(
        "docs/okf/** linguist-generated=true -diff\n", encoding="utf-8"
    )
    gen = tmp_path / "docs" / "okf"
    gen.mkdir(parents=True)
    (gen / "SR-001.md").write_text(
        "**Evidence.** `tests/gone.py::test_x`\nalso `scripts/gone.py`\n",
        encoding="utf-8",
    )
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_symbol_tier_skips_without_inventory(tmp_path):
    # A files-mode / non-Python stack has no symbol inventory: the sym: tier
    # skips with a note, and the path tier still runs.
    make_repo(tmp_path, "Call sym:demo.add; also `scripts/real.py`.\n", with_arch=False)
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "skipped" in proc.stdout
