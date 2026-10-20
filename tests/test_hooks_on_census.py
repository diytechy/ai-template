"""The census of agent routes that call the commit-hooks check first (WI-926).

Every agent route refuses to start in a checkout whose commit hooks are not on,
and it asks `kitlib.commit_hooks.hooks_refusal` before any other kit call.
`ROUTES` is the reviewed declaration of those entries: the six shipped routes
and this repository's headless-leg launcher. Each entry names the calls it may
make before the check (its argument parsing, its root resolution), and the
census asserts that the first call outside that preamble is the check, handed
exactly the entry's root and nothing else, so no argument can switch it off.

Read from the function bodies by AST, in process, as
`tests/test_commit_floor_census.py` reads the floor. A new route added without
the call fails here only once it is listed: the list is the declaration, and
adding to it is the reviewed act. The mutation test shows the census is not
vacuous: moving each entry's check below its next working statement, or
deleting it, is reported.
"""

import ast
import copy

import pytest
from conftest import ROOT, SCRIPTS

LEGS = ROOT / "scripts" / "coordinator" / "overnight_legs.py"
ROOT_PATH = ("Path",)

# (file, function, the root expression the check is handed, the preamble).
ROUTES = (
    (
        SCRIPTS / "agent_loop.py",
        "main",
        "root",
        ("_utf8_console", "parse_args", "_resolve_root"),
    ),
    (SCRIPTS / "session_service.py", "act", "call.root", ()),
    (SCRIPTS / "bookkeeping.py", "commit", "root", ROOT_PATH),
    (SCRIPTS / "integrate.py", "refresh", "root", ()),
    (SCRIPTS / "integrate.py", "integrate", "root", ()),
    (SCRIPTS / "coordinator_guard.py", "take", "root", ()),
    (
        LEGS,
        "main",
        "repo",
        (
            # `check-lane` is a read that sets no marker and commits nothing;
            # it returns before the launcher's own run starts.
            "list",
            "check_lane_main",
            "argparse.ArgumentParser",
            "ap.add_argument",
            "ap.parse_args",
            "Path",
            "Path().resolve",
            "str",
            "sys.path.insert",
        ),
    ),
)


def _callee(node):
    """A call's callee as a dotted name; `()` marks a call in the chain."""
    func = node.func
    parts = []
    while isinstance(func, ast.Attribute):
        parts.append(func.attr)
        func = func.value
    if isinstance(func, ast.Name):
        parts.append(func.id)
    elif isinstance(func, ast.Call):
        parts.append(_callee(func) + "()")
    else:
        parts.append("?")
    return ".".join(reversed(parts))


def _is_check(name):
    head, _, attr = name.rpartition(".")
    return attr == "hooks_refusal" and head.endswith("commit_hooks")


class _Calls(ast.NodeVisitor):
    """Every call in a body, in source order, nested definitions skipped."""

    def __init__(self):
        self.calls = []

    def visit_Call(self, node):
        self.calls.append(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        return None

    visit_AsyncFunctionDef = visit_FunctionDef
    visit_Lambda = visit_FunctionDef


def _calls_in_order(statements):
    """Statement by statement in body order, and by source position within
    one statement, so a statement moved in the tree is read where it now is."""
    ordered = []
    for statement in statements:
        collector = _Calls()
        collector.visit(statement)
        ordered += sorted(collector.calls, key=lambda n: (n.lineno, n.col_offset))
    return ordered


def judge(fn, root_expr, preamble):
    """None when `fn`'s first call outside `preamble` is the commit-hooks check
    handed exactly `root_expr`, else the finding."""
    for call in _calls_in_order(fn.body):
        name = _callee(call)
        if name in preamble:
            continue
        if not _is_check(name):
            return "{}: first call outside its preamble is {}, not the check".format(
                fn.name, name
            )
        handed = [ast.unparse(a) for a in call.args]
        if handed != [root_expr] or call.keywords:
            return "{}: the check is handed {} (and {} keywords), not {}".format(
                fn.name, handed, len(call.keywords), root_expr
            )
        return None
    return "{}: never calls the check".format(fn.name)


def _function(path, name):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    raise AssertionError("{} defines no top-level {}".format(path.name, name))


def _route_id(route):
    return "{}::{}".format(route[0].name, route[1])


@pytest.mark.parametrize("route", ROUTES, ids=_route_id)
def test_each_route_calls_the_check_first(route):
    path, name, root_expr, preamble = route
    assert judge(_function(path, name), root_expr, preamble) is None


def test_the_census_lists_the_six_routes_and_the_legs_launcher():
    assert len(ROUTES) == 7
    assert len({_route_id(r) for r in ROUTES}) == 7


def _check_index(fn):
    for i, statement in enumerate(fn.body):
        if any(_is_check(_callee(c)) for c in _calls_in_order([statement])):
            return i
    raise AssertionError("{} holds no check".format(fn.name))


def _deleted(fn):
    mutant = copy.deepcopy(fn)
    del mutant.body[_check_index(mutant)]
    return mutant


def _moved_down(fn):
    """The check moved below the first later statement that makes a call:
    the route's own work now runs before it."""
    mutant = copy.deepcopy(fn)
    i = _check_index(mutant)
    check = mutant.body.pop(i)
    j = next(k for k in range(i, len(mutant.body)) if _calls_in_order([mutant.body[k]]))
    mutant.body.insert(j + 1, check)
    return mutant


@pytest.mark.parametrize("route", ROUTES, ids=_route_id)
@pytest.mark.parametrize("mutate", [_deleted, _moved_down], ids=["deleted", "moved"])
def test_the_census_fails_when_an_entry_stops_calling_first(route, mutate):
    path, name, root_expr, preamble = route
    finding = judge(mutate(_function(path, name)), root_expr, preamble)
    assert finding is not None and finding.startswith(name)


def test_the_census_reports_a_check_handed_anything_but_the_root():
    fn = ast.parse(
        "def take(root, session_id):\n"
        "    refusal = commit_hooks.hooks_refusal(root, strict=False)\n"
    ).body[0]
    assert "keywords" in judge(fn, "root", ())
    fn = ast.parse(
        "def take(root, session_id):\n"
        "    refusal = commit_hooks.hooks_refusal(session_id)\n"
    ).body[0]
    assert "handed" in judge(fn, "root", ())
