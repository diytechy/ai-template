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

WHY A BASELINE AND NOT "ASSERT NO CYCLES". Because there WAS a cycle when this
file landed, and a test that fails from the day it lands teaches people to skip
it. The baseline was a debt statement with a live owner (`WI-483`), not an
approval: every entry was architectural debt that program is paid to remove. It
is now EMPTY — WI-483 slices 1 and 2 removed all seven modules — and because the
ratchet compares for equality, an empty baseline is the strongest form of the
same test: any new cycle anywhere reds. The shape stays a list rather than
becoming `assert not cycles` so that a future component, if one is ever
deliberately accepted, is recorded with a size that can only shrink.

THE SELF-TEST MATTERS AS MUCH AS THE RATCHET. A walker that quietly stopped
descending into function bodies would make every cycle here vanish and this
whole file go green — the exact failure mode the review describes, reproduced in
the instrument meant to catch it. `test_the_graph_sees_imports_inside_function_
bodies` pins a known deferred edge so that regression fails loudly.

CYCLES ARE NOT THE ONLY DIRECTION RULE HERE. An acyclic tangle is still a
tangle, so the file also carries the DECLARED LAYER ORDER of the lifecycle band
(`LIFECYCLE_RANK`, WI-483 slice 7) and asserts every edge inside it points
strictly down — the property "`dispatch` is the sole composer" had been prose in
a spec file with nothing measuring it, and a sideways edge between two peers
leaves both cycle tests green.
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

# --- the lifecycle layer ORDER (WI-483 slice 7, program shape item 4) --------
#
# The cycle ratchet below says the lifecycle band has no cycles. It does NOT say
# the band is layered: an acyclic tangle is still a tangle, and "`dispatch` the
# sole composer with `integrate`/`handback`/`intake`/`lane` one-way below" was
# prose in a spec file with nothing measuring it — this file's own CYCLES
# comment said so ("the only rule policing direction today" was the view rule,
# which `integrate` is not subject to).
#
# So: a declared RANK per lifecycle module, and every edge inside the band must
# point STRICTLY DOWN. Strict, not `>=`, because a peer-to-peer edge between two
# modules of equal rank means one of them is really above the other and nobody
# has said which.
#
# Measured 2026-08-24, and this is the whole band:
#   dispatch -> handback, lane, integrate, intake   (module-level, the composer)
#   handback -> integrate                           (module-level)
#   lane     -> integrate                           (module-level)
#   integrate -> intake                             (deferred, the post-merge
#                                                    mint at the held slot)
# `intake` imports no lifecycle module at all. The ordering is therefore forced,
# not chosen: dispatch composes; handback and lane are peers that both drive the
# merge service; `integrate` merges; `intake` mints and reaches nothing above it.
#
# WHY `integrate -> intake` IS NOT AN INVERSION, recorded because WI-483's own
# spec called it one for two slices. That word was inherited from the era when
# `intake -> dispatch` existed: intake was then above integrate THROUGH THE
# CYCLE. Slice 2 cut that edge, and with it the only reason to call intake the
# higher module — it imports nothing here, which is the definition of the
# bottom. `integrate.integrate_one` composing "merge, then mint" is not a second
# composer either: the mint is required to run INSIDE the held merge slot
# (serial by construction, all-or-nothing on one trunk commit), so it is part of
# what taking the slot MEANS, not a lifecycle step sequenced from above.
#
# RE-RANKING TO GET GREEN IS ACCEPTING WHAT THIS MEASURES, exactly like editing
# CYCLES. A new edge that points up is decomposition work: move what crosses to
# a module below both (`kitlib/station.py`, `census.py`, `pending.py` are the
# three worked precedents in this program).
LIFECYCLE_RANK = {
    "dispatch": 0,  # the composer; nothing in the band may import it
    "handback": 1,  # closes a lane
    "lane": 1,  # opens/manages one — handback's peer, not its caller
    "integrate": 2,  # the merge slot
    "intake": 3,  # the mint; imports nothing in the band
}

# --- the cycle baseline ----------------------------------------------------
#
# Each entry is one strongly connected component of more than one module, as
# sorted module names. Re-stamp DOWNWARD only; the reason goes in the log.
CYCLES = [
    # EMPTY, and that is the whole point of this list being a ratchet.
    #
    # repo review 2026-08-19 H-02 recorded SEVEN modules in one component:
    #   dispatch, gen_trajectory, handback, intake, integrate, lane, traj_panels
    # WI-483 slice 1 removed `traj_panels` and `gen_trajectory` by moving the
    # lane-close terminal-outcome vocabulary out of `integrate` and into
    # `kitlib.station`, a dependency-neutral read model, leaving the five-module
    # lifecycle core. WI-483 slice 2 cut TWO of that core's three back edges and
    # the component fell apart entirely:
    #   `intake -> dispatch`    the registry-gap census moved OUT of the
    #                           scheduling composer into the sibling `census.py`,
    #                           below all three of its readers.
    #   `integrate -> handback` the per-close report's path/format/read/refusal
    #                           moved down into `kitlib.station` beside the
    #                           terminal-outcome vocabulary they describe; the
    #                           WRITES stayed in `handback`.
    # The third back edge, `integrate -> intake` (the post-merge mint at the
    # held slot), SURVIVES — it just no longer closes anything, because with
    # `intake -> dispatch` gone `intake` reaches nothing above it. WI-483 slice 7
    # MEASURED that survivor rather than inheriting the word "upward" from the
    # cycle era, and it is a DOWNWARD edge: see `LIFECYCLE_RANK` above, which
    # turns program shape item 4 into a test instead of a sentence.
    #
    # AN EMPTY LIST IS NOW A REAL ASSERTION: `test_no_new_import_cycle` compares
    # for EQUALITY, so any new cycle anywhere under `scripts/` reds here. Do not
    # add an entry back to get green — decompose.
]

# --- the cycle DENSITY baseline (2026-08-21 review, M-12 / Sol 4) ------------
#
# `CYCLES` is a partition — a set of module NAMES — so an edge added between
# two modules already in the same component leaves it byte-identical. The
# review proved the hole by mutation: two brand-new deferred cycle edges
# appended to `lane.py` (`import dispatch`, `import handback` inside a
# function) left all three tests green. That is the exact pattern this file's
# docstring calls "the failure mode the review describes", and WI-483's
# remaining slices were paid to REMOVE three such edges — a ratchet that reports
# success while the tangle tightens is worse than none. (Those three are gone,
# and WI-483 slice 7 re-ran the review's mutation rather than assuming: the
# deferred `lane -> dispatch` / `lane -> handback` pair now reds all three
# tests. The residual hole it leaves is the SIDEWAYS edge — `handback -> lane`,
# two peers, no cycle formed, both cycle tests green — and that is exactly what
# `test_a_lifecycle_edge_never_points_up` was added to catch. Mutation-checked
# the same way.)
#
# So: the number of edges whose head and tail are both inside one component,
# deferred function-body imports INCLUDED (they are the ones that hide).
# Measured 2026-08-21 at 9 for the single five-module component:
#   module-level: dispatch->handback, dispatch->intake, dispatch->integrate,
#                 dispatch->lane, handback->integrate, lane->integrate
#   deferred:     intake->dispatch, integrate->handback, integrate->intake
# Asserted `<=`, and re-stamped DOWNWARD only — cutting one is the work; the
# stamp follows the cut in the same commit, with the reason in the log.
#
# RE-STAMPED 9 -> 0 at WI-483 slice 2 (2026-08-22): with `CYCLES` empty there is
# no component left for an edge to be inside, so the density this number
# measures is vacuously zero. The count is kept rather than deleted because it
# is the half of the ratchet that survives a component REAPPEARING at a
# different size — `CYCLES` is a partition and cannot see density, which is the
# hole the 2026-08-21 review proved by mutation.
MAX_INTRA_CYCLE_EDGES = 0


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

    `integrate.py` imports `intake` INSIDE a function — the post-merge mint at
    the held slot. If the walker ever stops descending into function bodies,
    every deferred edge disappears, the cycle baseline below goes green for
    free, and the file reports the opposite of the truth. Pin a known deferred
    edge so that failure is loud.

    THE PIN MOVED at WI-483 slice 2, and the move is itself the record: it used
    to name `integrate -> handback`, which is one of the two back edges that
    slice CUT. A self-test pinned to an edge the program is paid to remove
    cannot survive the program; this one names an edge slice 7 ruled KEPT
    (see `LIFECYCLE_RANK`), so it is a stable pin rather than a countdown.
    """
    graph = import_graph()
    assert graph["integrate"].get("intake") == "function", (
        "the import walker no longer sees imports inside function bodies "
        "(or integrate's deferred intake import moved). Every cycle "
        "measured here would silently vanish; fix the walker, do not "
        "re-stamp CYCLES."
    )
    deferred = sum(
        1 for edges in graph.values() for kind in edges.values() if kind == "function"
    )
    # A STAMPED WINDOW, not a floor of 3 (2026-08-21 review, m-30). The tree
    # carries ~20 deferred edges; a `>= 3` corroborator would survive an 85%
    # loss of detection, which is not a sensor. The window is wide enough that
    # ordinary work does not touch it and narrow enough that a walker
    # regression cannot hide: measured 20 at 2026-08-21, 21 immediately before
    # WI-483 slice 2 and 19 after it (that slice cut the two deferred back edges
    # plus `adjudicate_brief -> dispatch`, and its extraction added one deferred
    # edge back for the census's new home). The WINDOW itself is unmoved —
    # re-stamp it deliberately, with the reason in the log, only when the number
    # legitimately leaves it.
    assert 14 <= deferred <= 26, (
        "deferred function-body imports read {}, outside the stamped window "
        "14..26 (measured 20 at 2026-08-21). A COLLAPSE means the walker "
        "stopped descending into function bodies and every cycle measured in "
        "this file is understated — fix the walker, do not re-stamp. A rise "
        "means the deferred-import population grew, which is the coupling "
        "WI-521 now owns reducing: re-stamp only with the reason.".format(deferred)
    )


def test_no_new_import_cycle():
    """The ratchet. Cycles may shrink or vanish, never grow or appear."""
    found = strongly_connected(import_graph())
    baseline = sorted(tuple(sorted(entry)) for entry in CYCLES)
    assert found == baseline, (
        "the import-cycle census changed.\n"
        "  found:    {}\n"
        "  baseline: {}\n"
        "A cycle that GREW or APPEARED is decomposition work (WI-521) — do "
        "NOT widen CYCLES to get green, because editing this list IS "
        "accepting what it measures. A cycle that SHRANK is a win: re-stamp "
        "the entry downward, or delete it, in the same commit, with the "
        "reason in the session log.".format(found, baseline)
    )


def intra_cycle_edges(graph=None):
    """Every edge with both ends inside one strongly connected component, as
    `(importer, imported, kind)` — the density `CYCLES` cannot see."""
    graph = import_graph() if graph is None else graph
    out = []
    for component in strongly_connected(graph):
        members = set(component)
        for importer in sorted(members):
            for imported, kind in sorted(graph.get(importer, {}).items()):
                if imported in members:
                    out.append((importer, imported, kind))
    return out


def test_no_new_edge_inside_an_existing_cycle():
    """The density half of the ratchet — see MAX_INTRA_CYCLE_EDGES."""
    edges = intra_cycle_edges()
    assert len(edges) <= MAX_INTRA_CYCLE_EDGES, (
        "the tangle inside the existing import cycle(s) GREW: {} intra-cycle "
        "edges against a baseline of {}.\n  {}\nAdding an edge between two "
        "modules already in one component leaves the CYCLES partition "
        "identical, which is why this count exists. Do NOT raise the number to "
        "get green — that IS accepting what it measures. Route the new call "
        "through a lower layer (`kitlib.station` is the precedent), or cut an "
        "existing edge to pay for it.".format(
            len(edges),
            MAX_INTRA_CYCLE_EDGES,
            "\n  ".join("{} -> {} ({})".format(*e) for e in edges),
        )
    )
    # DOWNWARD RE-STAMPS ARE OWED, not optional: a stale-high baseline is a
    # ratchet that has stopped ratcheting.
    assert len(edges) == MAX_INTRA_CYCLE_EDGES, (
        "intra-cycle edges are DOWN to {} from a baseline of {} — a win. "
        "Re-stamp MAX_INTRA_CYCLE_EDGES to {} in this commit and record which "
        "edge went, so the next slice starts from the real number.".format(
            len(edges), MAX_INTRA_CYCLE_EDGES, len(edges)
        )
    )


# --- the facade rule (WI-483 slice 3) ---------------------------------------
#
# `gen_trajectory` is a CLI ENTRY POINT that re-exports ~60 names from the
# `traj_*` family. Until this slice it was also the way two modules outside the
# dashboard reached a state query: `dispatch._pending_cards` imported it for the
# PRIVATE `_blocked_pending`/`_spine_pending` (documented as IF-088 rather than
# removed), and `gen_open_items.pending_block_text` imported it for
# `pending_block`. Both are the 2026-08-19 review's bad edges — H-02's "imports
# the large facade for a state query" and M-02's "private names as cross-module
# APIs" — and both are gone: the derivation is `pending.py`, below all three of
# its readers.
#
# Zero importers is the strongest form of the rule and it is the state today, so
# it is asserted as EQUALITY rather than as a ceiling, exactly like `CYCLES`. If
# a module ever genuinely needs something the facade owns, the answer is the
# same one that produced this test: the value belongs in the module that derives
# it, not in the re-export layer above it.
FACADES = frozenset({"gen_trajectory"})


def test_a_facade_is_an_entry_point_and_nothing_imports_it():
    """A re-export layer is for a CLI, never for reaching a sibling's state."""
    graph = import_graph()
    offenders = sorted(
        "{} -> {} [{}]".format(module, target, kind)
        for module, edges in graph.items()
        for target, kind in edges.items()
        if target in FACADES
    )
    assert not offenders, (
        "a module imports the dashboard facade: {}\n"
        "`gen_trajectory` re-exports the traj_* family for its own CLI; an "
        "importer is reaching THROUGH a ~1,000-line render layer for something "
        "a sibling derives. Import that sibling — or, if the derivation has "
        "readers outside the render family, move it below them the way "
        "`pending.py` and `census.py` were.".format(offenders)
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


def test_the_rank_map_covers_the_whole_lifecycle_band():
    """A new lifecycle module must be RANKED, not silently unpoliced.

    `LIFECYCLE` is what the view rule forbids reaching; `LIFECYCLE_RANK` is what
    orders it. If the two ever drift apart, a module could join the band and its
    edges would go unmeasured by the direction rule below — which is the same
    class of hole `MAX_INTRA_CYCLE_EDGES` exists to close for `CYCLES`.
    """
    assert set(LIFECYCLE_RANK) == set(LIFECYCLE), (
        "LIFECYCLE and LIFECYCLE_RANK disagree: {}\n"
        "Every lifecycle module needs a declared rank, so that adding one "
        "forces a decision about where it sits rather than exempting it from "
        "the direction rule.".format(sorted(set(LIFECYCLE_RANK) ^ set(LIFECYCLE)))
    )


def test_a_lifecycle_edge_never_points_up():
    """Program shape item 4, asserted rather than written down.

    `dispatch` is the sole composer and the rest of the band runs one way below
    it. See `LIFECYCLE_RANK` for the measured order, for why
    `integrate -> intake` is a DOWNWARD edge rather than the inversion WI-483's
    spec called it for two slices, and for why re-ranking to get green is
    accepting what this measures.
    """
    graph = import_graph()
    offenders = sorted(
        "{} (rank {}) -> {} (rank {}) [{}]".format(
            module, LIFECYCLE_RANK[module], target, LIFECYCLE_RANK[target], kind
        )
        for module, edges in graph.items()
        if module in LIFECYCLE_RANK
        for target, kind in edges.items()
        if target in LIFECYCLE_RANK and LIFECYCLE_RANK[target] <= LIFECYCLE_RANK[module]
    )
    assert not offenders, (
        "a lifecycle import points UP or SIDEWAYS: {}\n"
        "The band is layered: `dispatch` composes, `handback`/`lane` drive the "
        "merge service, `integrate` merges, `intake` mints. An edge that does "
        "not point strictly down means either the call belongs to a module "
        "BELOW both ends (`kitlib/station.py`, `census.py` and `pending.py` are "
        "this program's three precedents) or the declared order is wrong — and "
        "if it is wrong, say so in the log and re-rank deliberately. Editing "
        "LIFECYCLE_RANK to clear a finding IS accepting what it "
        "measures.".format(offenders)
    )
