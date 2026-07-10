"""TC-034 — the kit scripts are stdlib-only (SR-034 / SN-011).

Mechanizes what was an Inspection ("confirmed by inspecting imports") into a
Test: AST-scan every kit script's imports and assert no top-level module
resolves to a third party. A downstream repo must be able to run the kit's own
checks on a clean Python 3.8+ with no `pip install`, so a stray third-party
import is a real regression, not a style nit.

Enforcement-audit note (docs/enforcement-audit.md): this is the EVAL/test-class
enforcer for SR-034 — the strongest enforcer available, replacing a human
eyeball that would not fire in CI.
"""

import ast
import os
import sys

from conftest import SCRIPTS


def stdlib_top_level_names():
    """The set of top-level module names that ship with this Python.

    On 3.10+ `sys.stdlib_module_names` is authoritative and platform-independent.
    On 3.8/3.9 (the kit's floor) it does not exist, so derive it: the C builtins
    (`sys.builtin_module_names`) plus a scan of the standard-library directory
    (`os.__file__`'s dir — never `site-packages`), plus a small allowlist of
    platform-gated stdlib modules a cross-platform scan cannot see (e.g. `fcntl`
    is POSIX-only, `msvcrt`/`winreg` Windows-only — the coordinator lock imports
    both under a try/except). The allowlist is inert on 3.10+.
    """
    names = set(sys.builtin_module_names)
    if hasattr(sys, "stdlib_module_names"):
        names |= set(sys.stdlib_module_names)
    libdir = os.path.dirname(os.__file__)
    for entry in os.listdir(libdir):
        path = os.path.join(libdir, entry)
        if entry.endswith(".py"):
            names.add(entry[:-3])
        elif os.path.isdir(path) and os.path.exists(os.path.join(path, "__init__.py")):
            names.add(entry)
    names |= {
        "fcntl",
        "msvcrt",
        "winreg",
        "termios",
        "grp",
        "pwd",
        "posix",
        "nt",
        "_winapi",
    }
    return names


def local_script_stems():
    """The kit scripts themselves — a sanctioned sibling import (e.g.
    gen_trajectory's `import check_trajectory`) is local, not third-party."""
    return {f[:-3] for f in os.listdir(SCRIPTS) if f.endswith(".py")}


def third_party_imports(source, filename, allowed):
    """Top-level import names in `source` that are neither stdlib nor local.

    Relative imports (`from . import x`) are local and skipped. `allowed` is the
    stdlib set ∪ the local script stems.
    """
    tree = ast.parse(source, filename)
    seen = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                seen.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            seen.add(node.module.split(".")[0])
    return sorted(name for name in seen if name not in allowed)


def test_no_kit_script_imports_third_party():
    """Every project-trajectory/scripts/*.py imports only stdlib + siblings."""
    allowed = stdlib_top_level_names() | local_script_stems()
    offenders = {}
    for entry in sorted(os.listdir(SCRIPTS)):
        if not entry.endswith(".py"):
            continue
        path = SCRIPTS / entry
        found = third_party_imports(path.read_text(encoding="utf-8"), entry, allowed)
        if found:
            offenders[entry] = found
    assert not offenders, (
        "third-party imports found (kit must stay stdlib-only): {}".format(offenders)
    )


def test_detector_flags_a_third_party_import():
    """Positive control: the scan actually catches a third-party import, so a
    green above is a real pass, not a vacuous one."""
    allowed = stdlib_top_level_names() | local_script_stems()
    src = (
        "import os\nimport requests\nfrom numpy import array\nimport check_trajectory\n"
    )
    found = third_party_imports(src, "<synthetic>", allowed)
    assert found == ["numpy", "requests"]  # os + the local sibling are not flagged
