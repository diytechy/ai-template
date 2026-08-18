"""check_stubs.py: the optional, warn-first, product-layer tripwire for the DevStg-Impl
no-stub / substance criterion (process.md §4). It lists public symbols whose body
does nothing (`pass`/`...`/`raise NotImplementedError`/bare `return None`/
docstring-only), warns by default (exit 0) and gates only with `--strict`, and
never over-flags a substantive tiny pure function.
"""

import ast

from conftest import load_script, run_py

# A source file mixing real work, a tiny pure function, every stub shape, and the
# skip cases (private name, private class, @abstractmethod, @overload).
SRC = '''"""Fixture module for the stub detector."""

from abc import abstractmethod
from typing import overload


def compute(x):
    """Real work."""
    return x * 2 + 1


def identity(x):
    return x  # tiny pure function — returns a real value, not a stub


def todo_pass():
    pass


def todo_ellipsis(): ...


def todo_raise():
    """Approved."""
    raise NotImplementedError("later")


def todo_return_none(a):
    return None


def todo_docstring_only():
    """Nothing here yet."""


def _private_helper():
    pass


class Service:
    def handle(self):
        pass

    def serve(self):
        return self.handle() or 1

    @abstractmethod
    def contract(self): ...

    @overload
    def variant(self, x): ...


class _Internal:
    def skipped(self):
        pass
'''


def write_src(root, text=SRC, name="mod.py"):
    (root / "src" / name).write_text(text, encoding="utf-8")


def stub_report(root):
    return (root / "docs" / "test" / "stub-report.md").read_text(encoding="utf-8")


# --- CLI behavior on a real scaffold -----------------------------------------


def test_substantive_only_passes(scaffold):
    write_src(scaffold, '"""Pure."""\n\n\ndef add(a, b):\n    return a + b\n')
    proc = run_py(["scripts/check_stubs.py"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "check_stubs: OK" in proc.stdout


def test_stub_flagged_but_warn_first(scaffold):
    write_src(scaffold)
    proc = run_py(["scripts/check_stubs.py"], cwd=scaffold)
    # Warn-first: stubs are found, but the run still exits 0 (advisory).
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARN" in proc.stdout
    assert "todo_pass" in proc.stdout and "(pass)" in proc.stdout
    assert "advisory" in proc.stdout
    # The report is written with the candidate rows.
    report = stub_report(scaffold)
    assert "todo_raise" in report and "raise NotImplementedError" in report


def test_strict_gates_when_stubs_present(scaffold):
    write_src(scaffold)
    proc = run_py(["scripts/check_stubs.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "check_stubs: FAIL" in proc.stdout


def test_tiny_pure_function_not_over_flagged(scaffold):
    write_src(scaffold)
    proc = run_py(["scripts/check_stubs.py"], cwd=scaffold)
    # `identity`/`compute` return real values; `serve` calls and returns — none
    # are stubs even though they're short.
    assert "identity" not in proc.stdout
    assert "compute" not in proc.stdout
    assert "Service.serve" not in proc.stdout


def test_skips_private_and_abstract_and_overload(scaffold):
    write_src(scaffold)
    proc = run_py(["scripts/check_stubs.py"], cwd=scaffold)
    out = proc.stdout
    assert "_private_helper" not in out  # private name
    assert "_Internal" not in out  # private class -> methods skipped
    assert "contract" not in out  # @abstractmethod is meant to be empty
    assert "variant" not in out  # @overload is meant to be empty
    # But the genuinely-empty public method IS flagged.
    assert "Service.handle" in out


def test_no_source_dir_is_ok(scaffold):
    proc = run_py(["scripts/check_stubs.py", "--src", "nonexistent"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "no source directory" in proc.stdout


def test_exclude_drops_files(scaffold):
    write_src(scaffold, name="mod.py")
    proc = run_py(["scripts/check_stubs.py", "--exclude", "src/mod.py"], cwd=scaffold)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "todo_pass" not in proc.stdout


def test_report_is_gitignored_by_scaffold(scaffold):
    ignore = (scaffold / ".gitignore").read_text(encoding="utf-8")
    assert "docs/test/stub-report.md" in ignore


def test_bootstrap_ships_check_stubs(scaffold):
    assert (scaffold / "scripts" / "check_stubs.py").exists()


# --- importable units (no subprocess) ----------------------------------------


def _kind(src):
    check = load_script("check_stubs")
    return check.stub_kind(ast.parse(src).body[0])


def test_stub_kind_recognizes_every_shape():
    assert _kind("def f():\n    pass\n") == "pass"
    assert _kind("def f(): ...\n") == "..."
    assert (
        _kind("def f():\n    raise NotImplementedError\n")
        == "raise NotImplementedError"
    )
    assert _kind("def f():\n    raise NotImplementedError('x')\n") == (
        "raise NotImplementedError"
    )
    assert _kind("def f():\n    return None\n") == "return None"
    assert _kind("def f():\n    return\n") == "return None"
    assert _kind('def f():\n    """doc"""\n') == "docstring-only"
    # docstring + a single stub statement still reads as that stub.
    assert _kind('def f():\n    """doc"""\n    pass\n') == "pass"


def test_stub_kind_passes_real_bodies():
    assert _kind("def f(x):\n    return x\n") is None
    assert _kind("def f(x):\n    return x * 2\n") is None
    assert _kind("def f():\n    raise ValueError('no')\n") is None  # not NotImplemented
    assert _kind("def f():\n    x = 1\n    return x\n") is None
    assert _kind('def f():\n    """doc"""\n    return compute()\n') is None


def test_find_stubs_scope_and_skips():
    check = load_script("check_stubs")
    found = {f["name"]: f["kind"] for f in check.scan_source(SRC)}
    # Every public stub shape is reported, qualified for methods.
    assert found["todo_pass"] == "pass"
    assert found["todo_ellipsis"] == "..."
    assert found["todo_raise"] == "raise NotImplementedError"
    assert found["todo_return_none"] == "return None"
    assert found["todo_docstring_only"] == "docstring-only"
    assert found["Service.handle"] == "pass"
    # Substantive, private, abstract, overload, and private-class symbols are out.
    for absent in (
        "compute",
        "identity",
        "Service.serve",
        "_private_helper",
        "Service.contract",
        "Service.variant",
        "_Internal.skipped",
    ):
        assert absent not in found, absent


def test_scan_source_reports_line_numbers():
    check = load_script("check_stubs")
    found = check.scan_source("def a():\n    return 1\n\n\ndef b():\n    pass\n")
    assert found == [{"name": "b", "lineno": 5, "kind": "pass"}]
