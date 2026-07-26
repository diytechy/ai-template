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


# --- WI-062: UNTRACED vs DANGLING ---------------------------------------------
# A path that isn't on disk is not automatically rot. Before the split this repo
# reported 561 findings, 534 of them explainable — and noise is how a real broken
# link hides. Each tier below classifies by a REASON, never by a suppression
# list, so the untraced count stays a number you can watch.


def test_kit_relative_path_is_untraced_not_dangling(tmp_path):
    # A kit's prose addresses its portable unit by the paths an ADOPTING repo
    # will have after copy-in, so `scripts/check.py` is right for its reader even
    # though this repo keeps it under project-trajectory/.
    make_repo(tmp_path, "Wire `scripts/check.py` into CI.\n")
    kit = tmp_path / "project-trajectory" / "scripts"
    kit.mkdir(parents=True)
    (kit / "check.py").write_text("x = 1\n", encoding="utf-8")

    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, "a kit-relative path must not gate"
    assert "scripts/check.py does not exist" not in proc.stderr
    assert "1 untraced" in proc.stdout
    listed = refs(tmp_path, "--show-untraced")
    assert "UNTRACED" in listed.stderr and "kit-relative" in listed.stderr

    # ...and the classification is a REASON, not a blanket pass: the same token
    # with no such file anywhere is still dangling.
    (kit / "check.py").unlink()
    assert refs(tmp_path, "--strict").returncode == 1


def test_record_surface_path_is_untraced_not_dangling(tmp_path):
    # A session log naming a since-retired file is accurate history. "Fixing" it
    # would falsify the record, so it can never be a gating finding.
    make_repo(tmp_path, "Nothing here.\n")
    (tmp_path / "docs" / "log.md").write_text(
        "2026-01-01 — retired `docs/next-wi` in favour of the scheduler.\n",
        encoding="utf-8",
    )
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "1 untraced" in proc.stdout
    listed = refs(tmp_path, "--show-untraced")
    assert "record surface" in listed.stderr

    # The SAME token in a LIVE doc still gates — the tier keys on the surface,
    # not on the token, so retired-file rot in live prose stays visible.
    (tmp_path / "README.md").write_text("Set `docs/next-wi`.\n", encoding="utf-8")
    assert refs(tmp_path, "--strict").returncode == 1


def test_untraced_count_is_always_reported_even_when_silent(tmp_path):
    # A classification whose size you cannot see is a suppression list. The count
    # prints on stdout whether or not the list is shown.
    make_repo(tmp_path, "Nothing here.\n")
    (tmp_path / "docs" / "log.md").write_text(
        "`docs/gone-a` and `docs/gone-b` were retired.\n", encoding="utf-8"
    )
    proc = refs(tmp_path)
    assert "2 untraced" in proc.stdout
    assert "UNTRACED" not in proc.stderr, "silent by default"


def test_placeholder_and_anchored_shapes_are_not_paths(tmp_path):
    # `WI-###`/`NNN` are FORMS ("your id here") and `…` is "and the rest"; an
    # anchored doc reference is a LINK, which is check_docs.py's job.
    make_repo(
        tmp_path,
        "Name it `docs/specs/WI-###.md`, file `docs/reviews/NNN-AUDIT.md`, "
        "see `docs/…` and `docs/specs/my-effort.md#s1--first-slice`.\n",
    )
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "untraced" not in proc.stdout, "these are not paths at all, not excuses"


def test_symbol_tier_skips_without_inventory(tmp_path):
    # A files-mode / non-Python stack has no symbol inventory: the sym: tier
    # skips with a note, and the path tier still runs.
    make_repo(tmp_path, "Call sym:demo.add; also `scripts/real.py`.\n", with_arch=False)
    proc = refs(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "skipped" in proc.stdout
