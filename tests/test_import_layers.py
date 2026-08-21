"""The import-topology ratchet — repo review 2026-08-19, H-02 (WI-483 step 7).

The 2026-08-19 review found that the kit's coordinator, merge service, handback,
intake, lane management and dashboard are not layered services but ONE cyclic
subsystem: a seven-module strongly connected component. Lazy imports inside
function bodies kept the process from dying at startup, but they removed no
coupling at all — they only made the cycle invisible to every tool that reads
top-of-file imports, including a reader. The prose had already drifted past the
code: `handback.py` claimed integration never imports back while
`integrate.py` imported it.

So this file measures the ONE property the drift could hide: how much of the
graph is cyclic, counted over an import graph that INCLUDES imports inside
function bodies. It is the topology sibling of `test_module_size_ratchet.py`
(file scale) and `test_complexity_ratchet.py` (function scale), and it follows
the same ratchet convention:

- A cycle that GREW, or a NEW cycle: the fix is DECOMPOSITION, not a baseline
  edit. Adding a module to `CYCLES` to get green is accepting what it measures.
- A cycle that SHRANK or disappeared: re-stamp the baseline downward — or delete
  the entry — in the same commit, so the ratchet only ever tightens.

WHY A BASELINE AND NOT "ASSERT NO CYCLES". Because there IS a cycle, today, and
a test that fails from the day it lands teaches people to skip it. The baseline
is a debt statement with a live owner (`WI-483`), not an approval: every entry
below is architectural debt this program is paid to remove.

THE SELF-TEST MATTERS AS MUCH AS THE RATCHET. A walker that quietly stopped
descending into function bodies would make every cycle here vanish and this
whole file go green — the exact failure mode the review describes, reproduced in
the instrument meant to catch it. `test_the_graph_sees_imports_inside_function_
bodies` pins a known deferred edge so that regression fails loudly.
"""

import ast
import pathlib

from conftest import SCRIPTS

# --- the declared layering -------------------------------------------------
#
# VIEWS render; they must never be able to mutate. LIFECYCLE services claim
# lanes, merge branches, move specs and mint rows. An edge from a view INTO a
# lifecycle service is the direction a layered system forbids outright, and it
# is how the dashboard used to drag the merge coordinator into read-only
# rendering: `traj_panels` imported the 2,500-line `integrate` for two
# constants (WI-483 moved them down to `kitlib.station`).
#
# `dispatch` is deliberately NOT a view even though it renders a banner: it is
# the composer, above both bands, and it is allowed to import either.
VIEW_PREFIXES = ("traj_", "gen_")
LIFECYCLE = frozenset({"dispatch", "handback", "intake", "integrate", "lane"})

# --- the cycle baseline ----------------------------------------------------
#
# Each entry is one strongly connected component of more than one module, as
# sorted module names. Re-stamp DOWNWARD only; the reason goes in the log.
CYCLES = [
    # repo review 2026-08-19 H-02 recorded this at SEVEN modules:
    #   dispatch, gen_trajectory, handback, intake, integrate, lane, traj_panels
    # WI-483 slice 1 removed `traj_panels` and `gen_trajectory` by moving the
    # lane-close terminal-outcome vocabulary out of `integrate` and into
    # `kitlib.station`, a dependency-neutral read model. `traj_panels`' only
    # edge into the component was that constants import, and `gen_trajectory`'s
    # only route in was through `traj_panels`, so cutting one edge dropped two
    # modules. The five that remain are the lifecycle core proper, and their
    # back edges (`intake -> dispatch`, `integrate -> handback`,
    # `integrate -> intake`) are all deferred function-body imports — WI-483's
    # remaining slices.
    ("dispatch", "handback", "intake", "integrate", "lane"),
]


def _module_name(path):
    """The dotted module name a scripts-relative path imports as."""
    rel = path.relative_to(SCRIPTS).with_suffix("")
    return ".".join(rel.parts)


def _internal_modules():
    """`{dotted name: path}` for every module under `scripts/`, packages too."""
    out = {}
    for path in sorted(pathlib.Path(SCRIPTS).rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        out[_module_name(path)] = path
    return out


def _resolve(target, known):
    """The internal module `target` names, or None.

    Handles all three spellings the kit uses: `import trace_text` (a bare
    module), `from kitlib.station import X` (a module inside a package) and
    `from kitlib import station` (the package, whose `__init__` is what
    actually executes). Longest prefix wins, so `kitlib.station` resolves to
    the module rather than to the package.
    """
    parts = target.split(".")
    for cut in range(len(parts), 0, -1):
        name = ".".join(parts[:cut])
        if name in known:
            return name
        if name + ".__init__" in known:
            return name + ".__init__"
    return None


def import_graph():
    """`{module: {imported module: 'module' | 'function'}}` over `scripts/`.

    `'function'` marks an edge that exists ONLY inside a function body — the
    deferred imports the review found hiding the cycle. They are edges: the
    coupling is identical, only the failure timing differs.
    """
    known = _internal_modules()
    graph = {name: {} for name in known}

    for name, path in known.items():
        depth = [0]

        def record(target, node_depth, _name=name):
            hit = _resolve(target, known)
            if hit is None or hit == _name:
                return
            kind = "function" if node_depth else "module"
            # a module-level import outranks a deferred one for reporting
            if graph[_name].get(hit) != "module":
                graph[_name][hit] = kind

        def walk(node):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    depth[0] += 1
                    walk(child)
                    depth[0] -= 1
                    continue
                if isinstance(child, ast.Import):
                    for alias in child.names:
                        record(alias.name, depth[0])
                elif isinstance(child, ast.ImportFrom):
                    if child.level:
                        base = name.rsplit(".", 1)[0] if "." in name else ""
                        target = (base + "." + (child.module or "")).strip(".")
                    else:
                        target = child.module or ""
                    if target:
                        record(target, depth[0])
                    # `from pkg import mod` also names pkg.mod
                    for alias in child.names:
                        if target:
                            record(target + "." + alias.name, depth[0])
                walk(child)

        walk(ast.parse(pathlib.Path(path).read_bytes()))

    return graph


def strongly_connected(graph):
    """Non-trivial SCCs as sorted tuples, sorted. Iterative — the graph is
    small, but a recursive Tarjan on a 60-module graph is a stack risk nobody
    needs to take in a test."""
    index, low, on_stack, stack, order, out = {}, {}, {}, [], [0], []

    for root in sorted(graph):
        if root in index:
            continue
        work = [(root, 0)]
        while work:
            node, next_child = work[-1]
            if next_child == 0:
                index[node] = low[node] = order[0]
                order[0] += 1
                stack.append(node)
                on_stack[node] = True
            successors = sorted(graph[node])
            descended = False
            for pos in range(next_child, len(successors)):
                nxt = successors[pos]
                if nxt not in index:
                    work[-1] = (node, pos + 1)
                    work.append((nxt, 0))
                    descended = True
                    break
                if on_stack.get(nxt):
                    low[node] = min(low[node], index[nxt])
            if descended:
                continue
            if low[node] == index[node]:
                component = []
                while True:
                    popped = stack.pop()
                    on_stack[popped] = False
                    component.append(popped)
                    if popped == node:
                        break
                if len(component) > 1:
                    out.append(tuple(sorted(component)))
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[node])
    return sorted(out)


def test_the_graph_sees_imports_inside_function_bodies():
    """The instrument's own self-test, and the reason this file can be trusted.

    `integrate.py` imports `handback` INSIDE a function. If the walker ever
    stops descending into function bodies, every deferred edge disappears, the
    cycle baseline below goes green for free, and the file reports the opposite
    of the truth. Pin the known deferred edge so that failure is loud.
    """
    graph = import_graph()
    assert graph["integrate"].get("handback") == "function", (
        "the import walker no longer sees imports inside function bodies "
        "(or integrate's deferred handback import moved). Every cycle "
        "measured here would silently vanish; fix the walker, do not "
        "re-stamp CYCLES."
    )
    deferred = sum(
        1 for edges in graph.values() for kind in edges.values() if kind == "function"
    )
    assert deferred >= 3, (
        "expected the kit's known deferred imports in the graph, saw {}".format(
            deferred
        )
    )


def test_no_new_import_cycle():
    """The ratchet. Cycles may shrink or vanish, never grow or appear."""
    found = strongly_connected(import_graph())
    baseline = sorted(tuple(sorted(entry)) for entry in CYCLES)
    assert found == baseline, (
        "the import-cycle census changed.\n"
        "  found:    {}\n"
        "  baseline: {}\n"
        "A cycle that GREW or APPEARED is decomposition work (WI-483) — do "
        "NOT widen CYCLES to get green, because editing this list IS "
        "accepting what it measures. A cycle that SHRANK is a win: re-stamp "
        "the entry downward, or delete it, in the same commit, with the "
        "reason in the session log.".format(found, baseline)
    )


def test_a_view_never_imports_a_lifecycle_service():
    """The layer rule WI-483 slice 1 established, asserted rather than written.

    A render module must not be able to reach a module that claims lanes,
    merges branches or moves specs. This is stricter than the cycle ratchet on
    purpose: an edge from a view into a lifecycle service is wrong even when it
    closes no cycle.
    """
    graph = import_graph()
    offenders = sorted(
        "{} -> {} [{}]".format(module, target, kind)
        for module, edges in graph.items()
        if module.startswith(VIEW_PREFIXES)
        for target, kind in edges.items()
        if target in LIFECYCLE
    )
    assert not offenders, (
        "a view imports a lifecycle service: {}\n"
        "Views depend on read models only. If the view needs a value the "
        "service owns, the value belongs BELOW both — see "
        "`kitlib/station.py`, which is exactly this fix applied to the "
        "terminal-outcome vocabulary.".format(offenders)
    )
