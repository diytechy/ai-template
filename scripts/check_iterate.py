#!/usr/bin/env python3
"""The iterate checks: prove the change in hand, then check the product is alive.

One run answers two questions, and its cost follows the size of the change,
not the size of the suite:

  FOCUS   Does the change I just made work? The test files this change names:
          a changed test file; the tests that name a changed script (an import,
          a `load_script` call, a `<name>.py` literal); the tests the spine
          links to it (the map `trace.py --tests-for` prints); and the tests
          that name a changed non-Python file.
  CANARY  Is every capability still basically alive? The fixed list in
          tests/canary.txt, one end-to-end happy path per capability. Its size
          is capped (tests/conftest.py CANARY_MAX), so it cannot grow with the
          suite.

The declared lints run beside the tests, not before them: they are the steps
of docs/stack.ini [run] smoke ahead of its tier step, read from there so the
list keeps one home.

A SENSOR, NEVER A PROOF. A pass here says the change works and nothing is
obviously broken. It makes no claim about a test this change does not name: a
dependency the selection missed stays unrun until a deeper run, and the plan
this step prints lists every changed path it could not map and every module
it narrowed. The deeper runs are unchanged and still own the claim "everything
passes": the in-process tier ([run] smoke), the unfiltered suite at a landing
and at phase close, and CI.

NARROWING A SHARED MODULE. A module whose tests hold more than HUB_FUNCTIONS
test functions is focused by the definitions the change touches: the module's own test files
(`test_<module>*.py`), the tests that mention a touched definition's name, and
the evidence of the test cases that verify the requirement ids on its
`Implements:` line. A change outside every definition, or one whose
definitions cannot be read, keeps the whole set.

WHAT RUNS NO TEST. A change made only of records (reviews, logs, plans,
handoffs) and of the state the lints already hold (work-item rows, generated
views) runs the lints alone.

WIDENING. A change no selection can be honest about runs the whole in-process
tier beside the canary set, and says so: pytest.ini, the coverage and
requirements files, a conftest hook, or a conftest change outside every
definition. `--wide` asks for that.

Usage:
  python scripts/check_iterate.py [--base REV] [--print] [--wide] [--no-lints]

  --base REV   the change is everything since the merge base with REV, the
               index, the working tree and untracked files included (default:
               HEAD, the uncommitted change)
  --print      print the plan as JSON and run nothing

Stdlib-only, cross-platform (a meta-repo dev tool, like check_smoke_budget.py).
"""

import argparse
import ast
import concurrent.futures
import json
import os
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "project-trajectory/scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_changed import changed_paths  # noqa: E402
from kitlib import config as _kitconfig  # noqa: E402

TESTS = "tests"
CANARY_LIST = "tests/canary.txt"
# Where a source module lives, and the dotted prefix a test imports it under.
SOURCE_ROOTS = ("project-trajectory/scripts/", "scripts/")
CONFTESTS = frozenset({"conftest.py", "tests/conftest.py"})
# A change here reaches every test, so no selection is honest: widen.
HARNESS = frozenset(
    {
        "pytest.ini",
        ".coveragerc",
        "requirements-dev.txt",
        "requirements-dev-lock-3.11.txt",
        "requirements-dev-lock-3.x.txt",
    }
)
# Records of work already done. No test reads one, and the lints hold their
# links and references.
RECORD_PREFIXES = (
    "docs/reviews/",
    "docs/archive/",
    "docs/iteration/",
    "docs/plans/",
    "docs/log.d/",
    "docs/decisions/",
    "docs/handbacks/",
    "docs/handoff-",
    "docs/log.md",
)
# State the declared lints and the commit hook's freshness steps already hold:
# the work-item rows and the generated views.
LINT_HELD_PREFIXES = (
    "docs/work/",
    "docs/status.md",
    "docs/stage",
    "docs/okf/",
    "docs/ratify/",
    "docs/open-items.html",
    "PROJECT_STATE.html",
)
NO_TEST_PREFIXES = RECORD_PREFIXES + LINT_HELD_PREFIXES
# A file name too common to search for; its directory names it instead.
GENERIC_NAMES = frozenset({"README.md", "SKILL.md", "__init__.py", "INDEX.csv"})
# A non-Python file named by more test files than this is shared furniture
# (every scaffold test writes a stack.ini): keep only the tests that read the
# repository's own copy, and past the limit again, leave it to the deeper runs.
BROAD_MENTION = 12
# The names a test spells the repository's own tree with.
LIVE_ROOT_NAMES = ("ROOT", "KIT", "SCRIPTS", "REPO")
# A module whose candidate tests hold more test functions than this is narrowed
# by what changed. Counted in functions, not files, because that is the cost.
HUB_FUNCTIONS = 150
# A test file carrying more script file names than this is an inventory (a
# scaffold file list, a ratchet table): the names it lists are not tests of
# those scripts, so only its imports and loads name a module.
INVENTORY_NAMES = 12
# Definition names every module has; mentioning one says nothing.
COMMON_SYMBOLS = frozenset({"main", "run", "ROOT", "__all__"})
# Below this many selected test functions a pool of workers costs more to
# start than it saves.
SERIAL_BELOW = 12
TESTS_PER_WORKER = 8


class Module(NamedTuple):
    """A changed source module: its dotted import name and its file stem."""

    dotted: str
    leaf: str


def source_module(path):
    """The `Module` a changed path is, or None when it is not a source file
    under a declared source root."""
    if not path.endswith(".py"):
        return None
    for prefix in SOURCE_ROOTS:
        if path.startswith(prefix):
            parts = path[len(prefix) : -len(".py")].split("/")
            if parts[-1] == "__init__":
                parts = parts[:-1]
            if not parts:
                return None
            return Module(".".join(parts), parts[-1])
    return None


class TestFile(NamedTuple):
    """What one file under tests/ names, read off its source without running
    it: the dotted names it imports, the stems it hands `load_script`, the
    `<stem>.py` literals it carries, the sibling helpers it imports, its text
    and test-function count, and whether it is an inventory of script names."""

    imports: frozenset
    loaded: frozenset
    files: frozenset
    helpers: frozenset
    text: str
    functions: int
    inventory: bool = False


_PY_LITERAL = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\.py\b")
_TEST_DEF = re.compile(r"^\s*(?:async\s+)?def test_", re.M)


def read_test_file(text, sibling_stems=(), source_stems=()):
    """The `TestFile` for one file's source text. A file that does not parse
    names nothing: it will fail its own collection, which is a failure already."""
    imports, loaded, files, helpers = set(), set(), set(), set()
    try:
        tree = ast.parse(text)
    except SyntaxError:
        tree = None
    for node in ast.walk(tree) if tree is not None else ():
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            imports.add(node.module)
            imports.update(node.module + "." + alias.name for alias in node.names)
        elif isinstance(node, ast.Call):
            name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
            first = node.args[0] if node.args else None
            if (
                name == "load_script"
                and isinstance(first, ast.Constant)
                and isinstance(first.value, str)
            ):
                loaded.add(first.value)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            files.update(_PY_LITERAL.findall(node.value))
    for dotted in imports:
        head = dotted.split(".")[0]
        if head in sibling_stems and head != "conftest":
            helpers.add(head)
    return TestFile(
        frozenset(imports),
        frozenset(loaded),
        frozenset(files),
        frozenset(helpers),
        text,
        len(_TEST_DEF.findall(text)),
        len(files.intersection(source_stems)) > INVENTORY_NAMES,
    )


def read_tests(root):
    """`{repo-relative path: TestFile}` for every Python file directly under
    tests/: the test files and the helper modules they share."""
    paths = sorted((root / TESTS).glob("*.py"))
    stems = frozenset(p.stem for p in paths)
    sources = frozenset(
        p.stem for prefix in SOURCE_ROOTS for p in (root / prefix).rglob("*.py")
    )
    return {
        TESTS + "/" + p.name: read_test_file(
            p.read_text(encoding="utf-8"), stems, sources
        )
        for p in paths
    }


def names_module(entry, module):
    """Whether a test file names `module`: imports it, loads it, or carries
    its file name (an inventory's list of file names does not count)."""
    if module.leaf in entry.loaded:
        return True
    if module.leaf in entry.files and not entry.inventory:
        return True
    return any(
        dotted == module.dotted or dotted.startswith(module.dotted + ".")
        for dotted in entry.imports
    )


def _is_test(path):
    return path.startswith(TESTS + "/test_") and path.endswith(".py")


def tests_naming(index, module):
    """The test files that name `module`, directly or through a helper module
    they import (conftest is everyone's helper, so it carries nothing)."""
    direct = {path for path, entry in index.items() if names_module(entry, module)}
    carriers = {Path(p).stem for p in direct if not _is_test(p)}
    carriers.discard("conftest")
    return sorted(
        path
        for path, entry in index.items()
        if _is_test(path) and (path in direct or carriers & entry.helpers)
    )


def _mention(token):
    return re.compile(r"(?<![\w.-])" + re.escape(token) + r"(?![\w-])")


def _symbol(name):
    """A definition's name as a test spells it, `module.name` included."""
    return re.compile(r"(?<!\w)" + re.escape(name) + r"(?!\w)")


def tests_mentioning(index, path):
    """`(test files, note)`: the tests that name the non-Python file `path`.

    A name carried by more than BROAD_MENTION files is narrowed to the lines
    that also spell the repository's own tree; still too many, and the answer
    is no tests with a note saying why."""
    name = Path(path).name
    token = Path(path).parent.name if name in GENERIC_NAMES else name
    if not token:
        return [], None
    pattern = _mention(token)
    hits = sorted(p for p, e in index.items() if _is_test(p) and pattern.search(e.text))
    if len(hits) <= BROAD_MENTION:
        return hits, None
    live = sorted(
        p
        for p in hits
        if any(
            pattern.search(line) and any(n in line for n in LIVE_ROOT_NAMES)
            for line in index[p].text.splitlines()
        )
    )
    if live and len(live) <= BROAD_MENTION:
        return live, None
    return [], "named by {} test files: too broad to focus".format(len(hits))


# --- What a change touches inside one Python file ------------------------------
class Touched(NamedTuple):
    """The definitions a change touches in one file: their names, the
    requirement ids on their `Implements:` lines, and whether a changed line
    sits outside every definition (so the whole module is in play)."""

    symbols: frozenset
    tags: frozenset
    whole: bool


_HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", re.M)
_IMPLEMENTS = re.compile(r"Implements:\s*([^\n]+)")
_ID = re.compile(r"\b[A-Z]{2,5}-\d+\b")


def hunk_ranges(diff_text):
    """The new-side `(first, last)` line ranges a unified diff changes. A hunk
    that only removes lines touches the line it closes up on."""
    ranges = []
    for start, count in _HUNK.findall(diff_text):
        first, size = int(start), int(count) if count else 1
        ranges.append((max(first, 1), max(first, 1) + max(size, 1) - 1))
    return ranges


def _implements(node):
    doc = ast.get_docstring(node, clean=False) or ""
    return {tag for line in _IMPLEMENTS.findall(doc) for tag in _ID.findall(line)}


def _start(node):
    return min([node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])])


def _assigned(node):
    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
    return {t.id for t in targets if isinstance(t, ast.Name)}


_DEFS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
_ASSIGNS = (ast.Assign, ast.AnnAssign, ast.AugAssign)


def touched(text, ranges):
    """The `Touched` for a file's new `text` and its changed line `ranges`,
    or None when the text does not parse. Blank lines, comments, imports and
    the module docstring touch nothing: a module that stops importing fails
    its own test files, which a narrowed selection always keeps."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return None
    lines = text.splitlines()
    body = list(tree.body)
    quiet = []  # spans that touch nothing
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(getattr(body[0], "value", None), ast.Constant)
    ):
        quiet.append((body[0].lineno, body[0].end_lineno))
    symbols, tags, whole = set(), set(), False
    for first, last in ranges:
        for number in range(first, min(last, len(lines)) + 1):
            line = lines[number - 1].strip()
            if not line or line.startswith("#"):
                continue
            if any(a <= number <= b for a, b in quiet):
                continue
            owner = next(
                (n for n in body if _start(n) <= number <= (n.end_lineno or n.lineno)),
                None,
            )
            if isinstance(owner, (ast.Import, ast.ImportFrom)):
                continue
            if isinstance(owner, _ASSIGNS):
                symbols |= _assigned(owner)
            elif isinstance(owner, _DEFS):
                symbols.add(owner.name)
                tags |= _implements(owner)
                for inner in getattr(owner, "body", []):
                    if isinstance(inner, _DEFS) and _start(inner) <= number <= (
                        inner.end_lineno or inner.lineno
                    ):
                        symbols.add(inner.name)
                        tags |= _implements(inner)
            else:
                whole = True
    return Touched(frozenset(symbols), frozenset(tags), whole)


def touched_in_worktree(root, base, path):
    """The `Touched` for `path` between `base` and the working tree, or None
    when it cannot be told: a file new since the base, an unreadable diff."""
    try:
        diff = subprocess.run(
            ["git", "diff", "-U0", "--no-renames", base, "--", path],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True,
        ).stdout.decode("utf-8", "replace")
        text = (root / path).read_text(encoding="utf-8")
    except (OSError, subprocess.CalledProcessError, UnicodeError):
        return None
    ranges = hunk_ranges(diff)
    return touched(text, ranges) if ranges else None


# --- The spine's links ----------------------------------------------------------
_SPINE = {}


def _spine_rows(root):
    """`(llrs, tcs)` from the repository's registries, read once per run;
    `None` when they are absent or unreadable."""
    if root not in _SPINE:
        try:
            import spine_carrier

            docs = root / "docs"
            _SPINE[root] = (
                spine_carrier.load(
                    docs / "requirements" / "low-level-requirements.toml",
                    "LLR-ID",
                    keep_examples=False,
                ),
                spine_carrier.load(docs / "test" / "test-cases.toml", "TC-ID"),
            )
        except Exception:  # noqa: BLE001 - an unreadable spine selects nothing
            _SPINE[root] = None
    return _SPINE[root]


def spine_tests(root, path):
    """The test files the spine links to the changed source `path`: its design
    rows' test cases' evidence, the map `trace.py --tests-for` prints. `[]`
    when the registries are absent or unreadable: the spine adds to a
    selection, it never gates one."""
    rows = _spine_rows(root)
    if rows is None:
        return []
    try:
        from kitlib import spine as kspine

        llrs, tcs = rows
        found = set()
        for module in kspine.resolve_modules(llrs, path):
            found.update(kspine.module_tests(llrs, tcs, module, TESTS))
        return sorted(p for p in found if _is_test(p) and (root / p).is_file())
    except Exception:  # noqa: BLE001
        return []


def design_tags(tags):
    """The ids to follow from a definition's `Implements:` line: its design
    rows when it names any, because a system requirement is verified by test
    cases across many definitions and would select them all."""
    design = frozenset(tag for tag in tags if tag.startswith("LLR-"))
    return design or frozenset(tags)


def tag_tests(root, tags):
    """The test files in the evidence of every test case that verifies one of
    the requirement ids `tags`."""
    rows = _spine_rows(root)
    if rows is None or not tags:
        return []
    try:
        from kitlib import spine as kspine

        found = set()
        for case in rows[1]:
            if tags.intersection(kspine.refs(case.get("Verifies"))):
                for path, _node in kspine.evidence_items(case.get("Evidence")):
                    if _is_test(path) and (root / path).is_file():
                        found.add(path)
        return sorted(found)
    except Exception:  # noqa: BLE001
        return []


class Selection(NamedTuple):
    """What a change selects: each focused test file with the reasons it is
    in; the changed paths nothing maps to; the modules it narrowed; the reason
    the run widens to the whole in-process tier (None when it does not); and
    whether the change can alter behaviour at all, which is what the canary
    set runs for."""

    files: dict
    unmapped: list
    notes: list
    widen: object
    behaviour: bool


def _own_tests(named, leaf):
    return [
        t
        for t in named
        if Path(t).stem == "test_" + leaf
        or Path(t).stem.startswith("test_" + leaf + "_")
    ]


def narrow(index, path, leaf, candidates, change, tagged):
    """`(kept, note)`: the candidates a change to a shared module keeps - its
    own test files, the tests mentioning a touched definition, and the tagged
    evidence - or `(candidates, None)` when the change cannot narrow it."""
    names = sorted(change.symbols - COMMON_SYMBOLS) if change else []
    if change is None or change.whole or not names:
        return candidates, None
    patterns = [_symbol(name) for name in names]
    kept = set(_own_tests(candidates, leaf)) | set(tagged)
    kept |= {
        t
        for t in candidates
        if t in index and any(p.search(index[t].text) for p in patterns)
    }
    note = "{}: {} test files name it; kept {} for the changed definition(s) {}".format(
        path, len(candidates), len(kept), ", ".join(names[:6])
    )
    return sorted(kept), note


def select(root, paths, index, *, spine=spine_tests, change_of=None, tagged=tag_tests):
    """The `Selection` for the changed `paths` (None: the comparison was
    unavailable, which widens rather than passing as an empty change).

    `change_of(path)` answers the `Touched` for a changed Python file, or None
    when it cannot; absent, nothing is narrowed."""
    if paths is None:
        return Selection({}, [], [], "the comparison base is unavailable", True)
    files, unmapped, notes, widen, behaviour = {}, [], [], None, False

    def add(test, reason):
        files.setdefault(test, [])
        if reason not in files[test]:
            files[test].append(reason)

    for path in paths:
        if path == CANARY_LIST or path.startswith(NO_TEST_PREFIXES):
            continue
        behaviour = True
        if path in HARNESS:
            widen = widen or "{} is shared by every test".format(path)
            continue
        if _is_test(path):
            if (root / path).is_file():
                add(path, "changed")
            continue
        change = change_of(path) if change_of and path.endswith(".py") else None
        if path in CONFTESTS:
            names = sorted(change.symbols) if change and not change.whole else []
            if not names or any(n.startswith("pytest_") for n in names):
                widen = widen or "{} changed outside a named helper".format(path)
                continue
            patterns = [_symbol(n) for n in names]
            for test, entry in index.items():
                if _is_test(test) and any(p.search(entry.text) for p in patterns):
                    add(test, "mentions {} ({})".format(names[0], path))
            continue
        module = source_module(path)
        if module is None and path.startswith(TESTS + "/") and path.endswith(".py"):
            module = Module(Path(path).stem, Path(path).stem)  # a shared helper
        if module is not None:
            named = tests_naming(index, module)
            linked = spine(root, path)
            candidates = sorted(set(named) | set(linked))
            if (
                sum(index[t].functions for t in candidates if t in index)
                > HUB_FUNCTIONS
            ):
                by_tag = tagged(root, design_tags(change.tags)) if change else []
                candidates, note = narrow(
                    index, path, module.leaf, candidates, change, by_tag
                )
                if note:
                    notes.append(note)
            for test in candidates:
                add(test, ("names " if test in named else "spine links ") + path)
            if not candidates:
                unmapped.append(path + " (no test names it)")
            continue
        hits, note = tests_mentioning(index, path)
        for test in hits:
            add(test, "names " + path)
        if note:
            unmapped.append("{} ({})".format(path, note))
        elif not hits:
            unmapped.append(path + " (no test names it)")
    return Selection(dict(sorted(files.items())), unmapped, notes, widen, behaviour)


def read_canary(root):
    """The canary node ids, in file order: one per line, `#` opens a comment."""
    listing = root / CANARY_LIST
    if not listing.is_file():
        return []
    out = []
    for line in listing.read_text(encoding="utf-8").splitlines():
        node = line.split("#", 1)[0].strip()
        if node:
            out.append(node)
    return out


def declared_lints(root):
    """The lint steps of the declared commit checks: docs/stack.ini [run] smoke,
    split on `&&`, less its tier step, read through the kit's one stack.ini
    parse. `[]` when the file or the section is absent; an unreadable profile
    raises, as it does for every other reader."""
    profile = _kitconfig.read_stack_ini(root / _kitconfig.STACK_INI)
    chain = profile.get("run", "smoke", fallback="") if profile is not None else ""
    steps = [step.strip() for step in chain.split("&&") if step.strip()]
    return [s for s in steps if "check_smoke_budget.py" not in s and "pytest" not in s]


def workers_for(functions, heavy=0):
    """The xdist worker count for a run of `functions` test functions, `heavy`
    of them end-to-end canary nodes: none for a handful, then one per
    TESTS_PER_WORKER, and at least one per two heavy nodes, up to half the
    machine."""
    if functions < SERIAL_BELOW:
        return 0
    half = max(1, (os.cpu_count() or 2) // 2)
    wanted = max(-(-functions // TESTS_PER_WORKER), -(-heavy // 2))
    return max(2, min(half, wanted))


def pytest_command(selection, canary, index):
    """`(argv, functions)`: the one pytest run, or `(None, 0)` when the change
    runs no test. Focused, it names the selected files and the canary nodes
    outside them; widened, it runs the in-process tier and the canary set by
    marker (functions unknown: None)."""
    base = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"]
    if selection.widen:
        return [*base, "-n", "auto", "-m", "smoke or canary"], None
    if not selection.behaviour:
        return None, 0
    extra = [node for node in canary if node.split("::", 1)[0] not in selection.files]
    functions = sum(index[p].functions for p in selection.files if p in index)
    functions += len(extra)
    if not functions:
        return None, 0
    workers = workers_for(functions, heavy=len(extra))
    parallel = ["-n", str(workers)] if workers else ["-p", "no:xdist"]
    return [*base, *parallel, *selection.files, *extra], functions


def plan(root, base, wide=False):
    """The whole plan as one JSON-ready mapping."""
    paths = changed_paths(root, base)
    index = read_tests(root)
    selection = select(
        root, paths, index, change_of=lambda p: touched_in_worktree(root, base, p)
    )
    if wide:
        selection = selection._replace(widen=selection.widen or "--wide was asked for")
    canary = read_canary(root)
    command, functions = pytest_command(selection, canary, index)
    return {
        "base": base,
        "changed": paths,
        "focus": selection.files,
        "canary": canary if command else [],
        "unmapped": selection.unmapped,
        "narrowed": selection.notes,
        "widen": selection.widen,
        "test-functions": functions,
        "pytest": command,
        "lints": declared_lints(root),
    }


def resolve_base(root, rev):
    """The merge base of HEAD and `rev`, or None when there is none."""
    try:
        return subprocess.run(
            ["git", "merge-base", "HEAD", rev],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def _run(command, root):
    """`(exit code, seconds, combined output)` for one step."""
    start = time.perf_counter()
    proc = subprocess.run(
        command,
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
    )
    return proc.returncode, time.perf_counter() - start, proc.stdout


def _lint_argv(step):
    """A declared lint line as argv on this interpreter: the declared lines open
    with `python`, which the launcher resolves; here it is this one."""
    words = shlex.split(step)
    return [sys.executable, *words[1:]] if words and words[0] == "python" else words


def describe(result):
    """The plan as the lines a person reads before the run."""
    changed = result["changed"]
    lines = [
        "iterate: {} changed path(s) against {}".format(
            "unknown" if changed is None else len(changed), result["base"][:10]
        )
    ]
    if result["widen"]:
        lines.append("iterate: WIDE - {}".format(result["widen"]))
    elif not result["pytest"]:
        lines.append("iterate: no test - the change is records or lint-held state")
    for test, reasons in result["focus"].items():
        lines.append("  focus    {}  ({})".format(test, "; ".join(reasons[:2])))
    if result["canary"]:
        lines.append(
            "  canary   {} node(s) from {}".format(len(result["canary"]), CANARY_LIST)
        )
    for note in result["narrowed"]:
        lines.append("  NARROWED {}".format(note))
    for path in result["unmapped"]:
        lines.append(
            "  UNMAPPED {} - the deeper runs cover it, this one does not".format(path)
        )
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--base",
        default="HEAD",
        help="the change is everything since the merge base with this revision "
        "(default: HEAD)",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        dest="show",
        help="print the plan as JSON and run nothing",
    )
    parser.add_argument(
        "--wide",
        action="store_true",
        help="run the whole in-process tier beside the canary set",
    )
    parser.add_argument(
        "--no-lints", action="store_true", help="skip the declared lints"
    )
    args = parser.parse_args(argv)
    _kitconfig.utf8_console()

    base = resolve_base(ROOT, args.base)
    if base is None:
        print("iterate: no merge base with {!r}".format(args.base), file=sys.stderr)
        return 2
    result = plan(ROOT, base, wide=args.wide)
    if args.show:
        print(json.dumps(result, indent=2))
        return 0
    print("\n".join(describe(result)), flush=True)

    steps = [] if args.no_lints else [(s, _lint_argv(s)) for s in result["lints"]]
    if result["pytest"]:
        steps.append(("tests", result["pytest"]))
    if not steps:
        print("iterate: nothing to run")
        return 0
    start = time.perf_counter()
    worst = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(steps)) as pool:
        futures = {pool.submit(_run, argv_, ROOT): label for label, argv_ in steps}
        for future in concurrent.futures.as_completed(futures):
            label = futures[future]
            code, seconds, output = future.result()
            tail = output.strip().splitlines()[-1] if output.strip() else ""
            print(
                "iterate: {} {:6.1f}s  {}  | {}".format(
                    "ok  " if code == 0 else "FAIL", seconds, label, tail[:160]
                ),
                flush=True,
            )
            if code:
                worst = worst or code
                print(output, flush=True)
    print(
        "iterate: {} in {:.1f}s wall. This is the change's own evidence, not a "
        "landing claim.".format(
            "passed" if worst == 0 else "FAILED", time.perf_counter() - start
        )
    )
    return worst


if __name__ == "__main__":
    sys.exit(main())
