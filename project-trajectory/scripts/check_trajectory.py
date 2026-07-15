#!/usr/bin/env python3
"""Validate the work-item registry (docs/requirements/work-items.csv) — stdlib only.

The `SN->SR->LLR->TC` spine answers *what must be true*. A **work item**
(`WI-###`) decomposes *how the work executes*: it delivers SR(s), belongs to a
**workstream** (a mutable grouping category — the legacy `Track` header is still
read), and depends on **predecessor** work items (the DAG edges), moving
`queued -> active -> done`. This is the validation half of the trajectory layer;
the offline dashboard that renders the same registry is generated separately (a
*view*, never a source of truth — the `trace.py` / `gen_arch_map.py` idiom).

Checks (integrity, in the spirit of `trace.py`):
  - `WI-###` id shape + uniqueness — a malformed or duplicated id is an ERROR.
  - every `Predecessors` id resolves to a real work item — an ERROR (a DAG edge
    to a work item that does not exist).
  - the work-item graph is ACYCLIC over its **hard** edges — a cycle is an
    ERROR (a trajectory that depends on itself can never start).
  - a predecessor may be marked **soft** with a `~` prefix (`~WI-013`): an
    advisory-ordering hint, not a blocker. A soft edge must still resolve
    (ERROR if not), but it is excluded from the cycle rule — a cycle that
    exists only through soft edges is a WARN (conflicting hints), never an
    error — and it never constrains readiness.
  - every `SR-Refs` id exists in `system-requirements.csv` — a WARN, not a
    failure (a draft SR referenced ahead of its registry row is legitimate).

**The status.md ↔ registry SSOT rules** (S1; process-options.md "Trajectory /
work-items layer"). status.md is **forward-only** (what happens next) and the WI
`Deliverable` is **backward-only** (what shipped); the bridge is a per-WI
`SpecRef` that lives while the WI is open and clears at close. Cross-reading
`work-items.csv` and `docs/status.md` mechanizes five rules:
  - **R-A** — a WI's `Deliverable` is non-empty **iff** `Status = done`. An open
    (queued/active/deferred) WI with a filled Deliverable, or a `done` WI with an
    empty one, is a hard **ERROR at every run** (no flag needed): a commit is the
    agent handoff point, so an incoherent WI state launches the next session
    wrong.
  - **R-B** — every open WI id appears as a token in `status.md` (its context).
  - **R-C** — `status.md` names at least one open WI id (the next/active work).
  - **R-D** — no `done` WI id token appears in `status.md` (closed work leaves the
    working surface).
  - **R-E** — every open WI carries a non-empty `SpecRef` resolving to an in-repo
    target (`path` or `path#anchor`; the path part must exist).
R-B…R-E are **WARN by default, ERROR under `--strict`** (wired at G2+). If
`status.md` is absent, R-B/R-C/R-D are vacuous (a repo may not use a status
blackboard). `--staged` adds the warn-first **no-validation-delta** checks: the
follow-up-on-a-done-SR ratchet, and the **critique-loop ratchet** (WI-068) — a WI
closing on a `Verification=Critique` SR while the latest `docs/reviews/*-CRITIQUE.md`
verdict is CHANGES-REQUESTED, without the staged set touching the TC registry, the
tests dir, or a `docs/rubrics/` file (harden the TC or add a rubric anchor).

**Opt-out and vacuous by default** — the posture of the always-on
`docs/secrets-scan` floor. The check is on unless `docs/trajectory-check` reads
the one word `off`; and an *absent* or *placeholder-only* registry (nothing but
the inert `WI-000` example row) passes vacuously. So a fresh scaffold and a repo
that never adopts the layer both stay green for free — WI is an off-spine
optional registry, like procurement / assets, whose placeholder never blocks a
gate (`trace.py` does not read WI ids at all).

**Architecture-connectivity coverage** (S5/WI-056; process.md §8). This step is
also the views-checker for the interface layer: every module in the arch-map
inventory (`docs/architecture.md`'s generated block) should appear as ≥1 IF-###
endpoint, each Active seam should be cited by a TC, and a `Contracts: IF-###`
docstring citation should match the registry. All **warn-first** (they never
change the exit code, at any gate) and printed at the hook. The ruled posture is
**opt-out, default-on**: the coverage warn fires even when `interfaces.csv` is
empty or absent — a multi-module arch-map with no declared seams reads
"connectivity undeclared" instead of passing vacuously. It is silenced only by
the one word `off` in `docs/interfaces-check`, or a ≤1-module inventory (nothing
to connect). The honesty valve for a deliberate source/sink is a `source`/`sink`
token in that module's IF row Notes (below).

**How-SW top-view right-sizing** (WI-073/FB5; process-options.md "Component
layer"). The software-architecture diagram's *first view* must show at most
``TOP_VIEW_MAX`` (10) items: top-level components (a `CMP-###` with no `PartOf`
that contains ≥1 arch-map module) plus **uncontained** modules (a module with no
`Component`-tagged LLR). Exceeding the bound is a **finding** — WARN at the
plain/hook run, **ERROR under `--strict` (G2+)** — that drives right-sizing of
the component designations. Membership derives from the AXES join: a `Component`
tag on an LLR row joins its `Module` → `CMP-###`; nesting via the CMP registry's
`PartOf` (a module counts only at its top-level root). Opt-out is the one word
`off` in `docs/components-check` (the `interfaces-check` idiom); a repo with ≤10
modules — or no arch-map inventory — passes trivially (the bound, not the
registry, is the rule), so a small or non-adopting repo is never broken.

**Knowledge⇒component coupling** (WI-153; research-knowledge.md §3a, owner-ruled
2026-07-14). The same finding is *armed independent of the bound* once
`docs/knowledge/` holds a real pack: an uncontained arch-map module is then a
finding even below the 10-item bound, because a knowledge pack ties the *what* to
the knowledge behind the *how*, so that web must be robust wherever packs are
enabled. It reuses the existing `Component`-tag join (no new join) and the same
`docs/components-check` opt-out, and is dormant — costing a non-adopter nothing —
until a pack (any `docs/knowledge/*.md` but the `README.md` index) exists.

**Phase archetype + phase-drop detector** (WI-093; derived-gate model §7/§9.3).
A phase's pre-dev batch is a first-class WI whose Title carries a `[<phase>]-[g<N>]`
tag (`[v2]-[g1]` = requirement structuring, `[v2]-[g2]` = decomposition + TCs).
This step recognizes those anchors and, reading the derived per-phase levels from
`docs/gate`'s `# basis:` line, warns when a phase's derived gate has **dropped
below** the level its own closed `[phase]-[gN]` anchor recorded — the signal that
new or reopened content entered and a new phase-gate WI is due. All **warn-first**
(never an exit-code change, at any gate); vacuous on a single-phase repo with no
anchors (the meta case) or a legacy `docs/gate` with no basis line.

Usage:  python scripts/check_trajectory.py [--root .] [--strict] [--staged]
Exit codes: 0 clean / vacuous / opted-out, 1 a hard error, 2 usage/environment.

Contracts: IF-009, IF-023 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import configparser
import csv
import re
import subprocess
import sys
from pathlib import Path

WI_CSV = "docs/requirements/work-items.csv"
SR_CSV = "docs/requirements/system-requirements.csv"
TC_CSV = "docs/test/test-cases.csv"
IF_CSV = "docs/requirements/interfaces.csv"
LLR_CSV = "docs/requirements/low-level-requirements.csv"
CMP_CSV = "docs/requirements/components.csv"
STATUS_MD = "docs/status.md"
RUN_STATE = "docs/run-state"
NEXT_WI = "docs/next-wi"
ARCH_MD = "docs/architecture.md"

# The How-SW top view is bounded at this many items (top-level components +
# uncontained modules); exceeding it drives right-sizing of the component
# designations (WI-073, FB5 — warn plain, error --strict).
TOP_VIEW_MAX = 10

# An IF-### interface-seam id token (process.md §8). Matched word-bounded so a
# `Contracts: IF-003, IF-004` docstring line (harvested into the arch-map) or an
# id cell yields each id cleanly.
IF_ID_RE = re.compile(r"IF-\d+")
# A CMP-### component id token (process-options.md "Component layer"). trace.py
# owns CMP integrity; this loader is lenient (skips a malformed id) — it only
# feeds the warn-first top-view coverage.
CMP_ID_RE = re.compile(r"^CMP-\d+$")

# A well-formed work-item id: `WI-` then digits (`WI-001`). The `-000` example
# row matches this shape but is inert (skipped from the graph — see load_wis).
WI_ID_RE = re.compile(r"^WI-\d+$")
# A word-bounded WI id token as it appears in prose (status.md): `re.findall`
# grabs each maximal `WI-<digits>` run, so `WI-053…WI-059` yields both ids and
# `WI-05` never matches inside `WI-053` (R-D's "bare id token" rule).
WI_TOKEN_RE = re.compile(r"WI-\d+")

# The work-item lifecycle vocabulary (S1). `deferred` is a first-class,
# queued-but-not-next state carrying a recorded reason; an unknown status is a
# lint (warn-first). "Open" = anything not yet `done`.
OPEN_STATUSES = ("queued", "active", "deferred")
KNOWN_STATUSES = ("queued", "active", "done", "deferred")


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is, so a
    non-ASCII work-item title / path can't raise UnicodeEncodeError on a legacy
    Windows cp1252 console (same guard as check.py / check_privacy.py)."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def _first_declared_line(path):
    """The first non-empty, non-comment line of a declared-policy file, or None
    (absent/empty) — the parse every kit reader shares (hooks, check_privacy.py,
    agent_loop.py)."""
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    return None


def read_trajectory_enabled(root):
    """Whether the trajectory check is on. `docs/trajectory-check` with the one
    word `off` opts out; absent or any other value reads on (the safe default),
    so an ordinary repo runs it without declaring anything — opt-out, like
    `docs/secrets-scan`."""
    return (
        _first_declared_line(root / "docs" / "trajectory-check") or ""
    ).lower() != "off"


def read_interfaces_check_enabled(root):
    """Whether the architecture-connectivity coverage warns are on (S5/WI-056).
    `docs/interfaces-check` with the one word `off` opts out; absent or any other
    value reads on — the ruled opt-out, default-on posture (same shape as
    `docs/trajectory-check`). Default-on means the coverage warn fires even with
    an empty/absent `interfaces.csv`; the off-switch or a ≤1-module inventory is
    the only silence."""
    return (
        _first_declared_line(root / "docs" / "interfaces-check") or ""
    ).lower() != "off"


def read_components_check_enabled(root):
    """Whether the How-SW top-view right-sizing rule is on (WI-073/FB5).
    `docs/components-check` with the one word `off` opts out; absent or any other
    value reads on — the ruled opt-out, default-on posture (same shape as
    `docs/interfaces-check`). Like that reader there is no scaffolded file:
    absence reads on, so a repo that never declares anything is still bounded."""
    return (
        _first_declared_line(root / "docs" / "components-check") or ""
    ).lower() != "off"


def _split_refs(cell):
    """Ref cells hold ids separated by ; , or whitespace; empty -> []."""
    return [t for t in re.split(r"[;,\s]+", (cell or "").strip()) if t]


def read_rows(path):
    """The CSV rows of `path` as dicts, or [] when the file is absent."""
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def load_wis(rows):
    """Parse work-item rows into `(wis, integrity_errors)`.

    `wis` are the real, well-formed items that form the graph; the inert `-000`
    example row is skipped (the `trace.py` placeholder rule — an off-spine
    optional registry's placeholder never blocks a gate). Integrity errors
    (malformed or duplicated ids) are collected on the raw rows so a broken id is
    *reported*, never silently dropped."""
    wis, integrity, seen = [], [], set()
    for r in rows:
        wid = (r.get("WI-ID") or "").strip()
        if not wid.startswith("WI-"):
            continue  # blank line / non-WI row
        if not WI_ID_RE.match(wid):
            integrity.append(
                "malformed work-item id {!r} (expected WI-<digits>)".format(wid)
            )
            continue
        if wid in seen:
            integrity.append("duplicate work-item id {}".format(wid))
            continue
        seen.add(wid)
        if wid.endswith("-000"):
            continue  # inert template example row (like trace.py)
        # A `~` prefix marks a soft (advisory-ordering) predecessor edge; the
        # bare id is a hard (blocking) edge — see the module docstring.
        preds, soft = [], []
        for p in _split_refs(r.get("Predecessors", "")):
            if p.startswith("~"):
                soft.append(p[1:])
            else:
                preds.append(p)
        wis.append(
            {
                "id": wid,
                "title": (r.get("Title") or "").strip(),
                "workstream": (r.get("Workstream") or r.get("Track") or "").strip()
                or "other",
                "srs": _split_refs(r.get("SR-Refs", "")),
                "preds": preds,
                "soft": soft,
                "status": (r.get("Status") or "queued").strip().lower(),
                # Backward-only summary (R-A) and the forward bridge (R-E). A
                # legacy CSV without the column reads as "" (DictReader -> None).
                "deliverable": (r.get("Deliverable") or "").strip(),
                "specref": (r.get("SpecRef") or "").strip(),
                # A mutable grouping tag in the `Workstream` precedent (WI-074) —
                # NOT id-checked (no vocabulary rule); empty = standalone. The
                # When-view dashboard bins the DAG by it; a legacy CSV without the
                # column reads "" (DictReader -> None), so it is never-breaking.
                "campaign": (r.get("Campaign") or "").strip(),
            }
        )
    return wis, integrity


def _cycles(wis, pred_map):
    """Cycle strings found by DFS colouring over `pred_map` ([] = acyclic).

    Iterative (explicit stack), not recursive: a work-item registry may encode an
    arbitrarily long dependency chain, and a recursive DFS would raise a raw
    ``RecursionError`` past CPython's ~1000-frame limit — the kit fails on bad
    data with a clear message, never an uncaught traceback. ``stack`` holds
    ``[node, next-pred-index]`` frames and ``path`` mirrors
    their nodes, so a back-edge to a GREY (on-path) node reconstructs the cycle
    exactly as the former recursion did."""
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {w["id"]: WHITE for w in wis}
    found = []
    for w in wis:
        if colour[w["id"]] != WHITE:
            continue
        stack = [[w["id"], 0]]
        path = [w["id"]]
        colour[w["id"]] = GREY
        while stack:
            node, i = stack[-1]
            preds = pred_map[node]
            if i < len(preds):
                stack[-1][1] += 1
                p = preds[i]
                if colour[p] == GREY:
                    found.append(" -> ".join(path[path.index(p) :] + [p]))
                elif colour[p] == WHITE:
                    colour[p] = GREY
                    stack.append([p, 0])
                    path.append(p)
            else:
                colour[node] = BLACK
                stack.pop()
                path.pop()
    return found


def validate(wis, known_srs):
    """Return the hard-error strings for the work-item graph ([] = clean).

    Dangling `SR-Refs` are WARNED on stderr (a draft SR referenced ahead of its
    row is legitimate), never failed — and only when the SR registry is
    non-empty, so a repo without SRs yet does not spuriously warn. Soft (`~`)
    predecessors must resolve like hard ones, but only **hard** edges are
    subject to the acyclicity ERROR — a cycle that needs a soft edge to close
    is a WARN (conflicting ordering hints), never a failure."""
    ids = {w["id"] for w in wis}
    errors = []

    for w in wis:
        for p in w["preds"] + w["soft"]:
            if p not in ids:
                errors.append(
                    "{}: predecessor {!r} is not a work item".format(w["id"], p)
                )
        for s in w["srs"]:
            if known_srs and s not in known_srs:
                print(
                    "check_trajectory: WARN - {} references {} "
                    "(not in the SR registry; draft?)".format(w["id"], s),
                    file=sys.stderr,
                )

    # A hard cycle makes the trajectory unstartable -> ERROR.
    hard_map = {w["id"]: [p for p in w["preds"] if p in ids] for w in wis}
    for cyc in _cycles(wis, hard_map):
        errors.append("dependency cycle: {}".format(cyc))

    # A cycle that only closes through soft edges is a hint conflict -> WARN.
    if not any(e.startswith("dependency cycle") for e in errors):
        both_map = {
            w["id"]: [p for p in w["preds"] + w["soft"] if p in ids] for w in wis
        }
        for cyc in _cycles(wis, both_map):
            print(
                "check_trajectory: WARN - soft-edge cycle (advisory ordering "
                "hints conflict; not a blocker): {}".format(cyc),
                file=sys.stderr,
            )
    return errors


def load_known_srs(root):
    """The set of real SR ids from system-requirements.csv (for the SR-ref warn)."""
    return {
        (r.get("SR-ID") or "").strip()
        for r in read_rows(root / SR_CSV)
        if (r.get("SR-ID") or "").startswith("SR-")
    }


# Source-file extensions stripped when normalizing a module path, so the arch-map
# name (`scripts/check`) and an IF endpoint written with the full repo path
# (`project-trajectory/scripts/check.py`) collapse to one key. Kept in sync with
# trace.py._MODULE_EXTS (a small stable helper duplicated per the F5 convention —
# check_trajectory must stay import-free of the joined-spine engine).
_MODULE_EXTS = (".py", ".sh", ".ps1", ".ts", ".js", ".go", ".rs", ".cmd")


def _norm_module(path):
    """A module path reduced to a naming-convention-neutral key: strip a leading
    `project-trajectory/`, any source extension, and `/__init__`."""
    p = (path or "").strip().replace("\\", "/")
    if p.startswith("project-trajectory/"):
        p = p[len("project-trajectory/") :]
    for ext in _MODULE_EXTS:
        if p.endswith(ext):
            p = p[: -len(ext)]
            break
    if p.endswith("/__init__"):
        p = p[: -len("/__init__")]
    return p


def load_ifs(rows):
    """Real (non-`-000`) IF-### interface rows as dicts. Lenient — `trace.py` owns
    IF integrity (malformed ids, SR-Ref resolution); this loader only feeds the
    warn-first coverage views, so a malformed id is simply skipped here."""
    out = []
    for r in rows:
        iid = (r.get("IF-ID") or "").strip()
        if not IF_ID_RE.fullmatch(iid) or iid.endswith("-000"):
            continue
        out.append(
            {
                "id": iid,
                "direction": (r.get("Direction") or "").strip().lower(),
                "this": (r.get("ThisProject") or "").strip(),
                "counterpart": (r.get("Counterpart") or "").strip(),
                "status": (r.get("Status") or "").strip().lower(),
                "notes": (r.get("Notes") or "").strip().lower(),
            }
        )
    return out


def arch_inventory(root):
    """`(module_names, {module: {IF ids}})` parsed from `docs/architecture.md`'s
    generated MODULE MAP block — the committed arch-map artifact (the same block
    `gen_trajectory.sw_modules` reads for the How-SW view, and `gen_arch_map`
    writes). `module_names` are the ``### `name``` headers; the IF map harvests
    the `Contracts (interfaces): IF-###, ...` line `gen_arch_map` emits from a
    module's `Contracts:` docstring. A small stable parser duplicated per the F5
    convention (sw_modules also collects symbols; this one collects the Contracts
    citations) — keep the header grammar in sync. Empty when the doc/block is
    absent, so the coverage layer is vacuous pre-arch-map."""
    md = root / ARCH_MD
    if not md.exists():
        return set(), {}
    names, contracts, current, inside = [], {}, None, False
    for line in md.read_text(encoding="utf-8", errors="replace").splitlines():
        if "BEGIN GENERATED MODULE MAP" in line:
            inside = True
            continue
        if "END GENERATED" in line:
            inside = False
            current = None
            continue
        if not inside:
            continue
        m = re.match(r"^### `([^`]+)`", line)
        if m:
            current = m.group(1)
            names.append(current)
        elif current and line.strip().startswith("Contracts (interfaces):"):
            contracts.setdefault(current, set()).update(IF_ID_RE.findall(line))
    return set(names), contracts


def interface_findings(root):
    """Architecture-connectivity coverage warns (S5/WI-056; process.md §8), all
    warn-first — the caller prints them and they never change the exit code, at
    any gate. Returns the warn strings ([] when opted out or vacuous).

    Ruled opt-out, default-on: fires even with an empty/absent `interfaces.csv`
    (a multi-module arch-map with no declared seams reads "connectivity
    undeclared"); silenced only by `docs/interfaces-check: off` or a ≤1-module
    inventory (nothing to connect)."""
    if not read_interfaces_check_enabled(root):
        return []
    inventory, declared_contracts = arch_inventory(root)
    if len(inventory) <= 1:
        return []  # nothing to connect (or no arch-map yet) — vacuous
    ifs = load_ifs(read_rows(root / IF_CSV))
    out = []
    if not ifs:
        return [
            "connectivity undeclared: the {}-module architecture declares no "
            "interfaces — add IF-### rows to {}, or set docs/interfaces-check: "
            "off".format(len(inventory), IF_CSV)
        ]

    inv_norm = {_norm_module(m): m for m in inventory}
    inv_norm.pop("", None)
    endpoints, provides, consumes = set(), set(), set()
    sources, sinks = set(), set()
    for r in ifs:
        this_n, cp_n = _norm_module(r["this"]), _norm_module(r["counterpart"])
        for n in (this_n, cp_n):
            if n in inv_norm:
                endpoints.add(n)
        # The honesty valve: a `source`/`sink` FIRST word in Notes marks
        # ThisProject a deliberate source (consumes nothing) / sink (provides
        # nothing), so it doesn't breed a boilerplate opposite-direction row.
        marker = r["notes"].split()
        first = marker[0].rstrip(":;,.") if marker else ""
        if first == "source":
            sources.add(this_n)
        elif first == "sink":
            sinks.add(this_n)
        # Producer -> consumer roles: Consumes flips the endpoints so the
        # producing/consuming credit lands on the right module either way.
        producer, consumer = (
            (cp_n, this_n) if r["direction"] == "consumes" else (this_n, cp_n)
        )
        if producer in inv_norm:
            provides.add(producer)
        if consumer in inv_norm:
            consumes.add(consumer)

    for n in sorted(inv_norm):
        module = inv_norm[n]
        if n not in endpoints:
            out.append(
                "connectivity undeclared: module {!r} is in the arch-map but no "
                "IF-### row names it".format(module)
            )
            continue
        if n not in consumes and n not in sources:
            out.append(
                "module {!r} declares no Consumes seam (mark it `source` in its "
                "IF row Notes if it deliberately consumes nothing)".format(module)
            )
        if n not in provides and n not in sinks:
            out.append(
                "module {!r} declares no Provides seam (mark it `sink` in its IF "
                "row Notes if it deliberately provides nothing)".format(module)
            )

    # Seam-TC citation: each Active IF id should be cited by >=1 TC (the rung-2
    # seam-TC rule, finally checkable now that trace reads the IF tier).
    tc_cited = set()
    for r in read_rows(root / TC_CSV):
        tc_cited.update(IF_ID_RE.findall(r.get("Verifies", "") or ""))
    for r in ifs:
        if r["status"] == "active" and r["id"] not in tc_cited:
            out.append(
                "IF {} is Active but cited by no TC (a seam should carry a "
                "contract/fixture test)".format(r["id"])
            )

    # Docstring citation: a `Contracts: IF-###` a script declares (harvested into
    # the arch-map) must exist in the registry; and, once the convention is in
    # use, a registry IF whose module declares no matching citation warns too.
    registry_ids = {r["id"] for r in ifs}
    for module, ids in sorted(declared_contracts.items()):
        for iid in sorted(ids - registry_ids):
            out.append(
                "module {!r} docstring declares Contracts: {} but no such IF-### "
                "row exists".format(module, iid)
            )
    if declared_contracts:  # reverse direction only "where sensible" — once opted in
        all_declared = set().union(*declared_contracts.values())
        for r in ifs:
            if r["id"] not in all_declared:
                out.append(
                    "IF {} is in the registry but no script declares it via a "
                    "Contracts: docstring line".format(r["id"])
                )
    return out


# --- the How-SW top-view right-sizing rule (WI-073/FB5) ------------------------
# The software-architecture diagram's first view is bounded at TOP_VIEW_MAX
# items = top-level components (a CMP with no PartOf that contains ≥1 arch-map
# module) + uncontained modules. Membership derives from the AXES join: a
# `Component` tag on an LLR joins LLR.Module → CMP-###; CMP nesting via PartOf.
# The derivation below is the ONE home for that join — gen_trajectory imports it
# (`ct.component_top_view`) so the render and this rule can never disagree on the
# count. Small stable loaders duplicated per the F5 convention (no sibling import
# into check_trajectory).


def load_cmps(rows):
    """Real (non-`-000`) CMP-### component rows as dicts (id, name, category,
    partof). Lenient — `trace.py` owns CMP integrity; a malformed id is skipped
    here, since this only feeds the warn-first top-view coverage."""
    out = []
    for r in rows:
        cid = (r.get("CMP-ID") or "").strip()
        if not CMP_ID_RE.match(cid) or cid.endswith("-000"):
            continue
        out.append(
            {
                "id": cid,
                "name": (r.get("Name") or "").strip(),
                "category": (r.get("Category") or "").strip(),
                "partof": [p for p in _split_refs(r.get("PartOf", "")) if p],
            }
        )
    return out


def _cmp_roots(cmps):
    """`{cmp id: set(top-level root ids)}` — walk `PartOf` upward to the root(s)
    (a CMP with no real PartOf is its own root). A PartOf parent that names no
    real CMP is ignored (trace.py flags it separately). Cycle-guarded (a `seen`
    frontier), so a pathological PartOf cycle degrades to the CMP itself rather
    than looping."""
    by_id = {c["id"]: c for c in cmps}
    roots = {}
    for c in cmps:
        seen, frontier, out = set(), [c["id"]], set()
        while frontier:
            n = frontier.pop()
            if n in seen:
                continue
            seen.add(n)
            parents = [p for p in by_id.get(n, {}).get("partof", []) if p in by_id]
            if parents:
                frontier.extend(parents)
            else:
                out.add(n)
        roots[c["id"]] = out or {c["id"]}
    return roots


def module_components(root):
    """`{normalized module key: set(real-looking CMP ids)}` from the LLR
    `Component` tags joined on `LLR.Module` — the AXES membership rule (a module
    belongs to the CMP(s) its LLRs are tagged with). Empty when the LLR registry
    has no `Component` column (legacy) or no tags, so it costs a non-adopter
    nothing. The tag set is left unfiltered against the CMP registry here; the
    caller intersects with the real ids (a phantom tag is trace.py's finding)."""
    out = {}
    for r in read_rows(root / LLR_CSV):
        lid = (r.get("LLR-ID") or "").strip()
        if not lid.startswith("LLR-") or lid.endswith("-000"):
            continue
        tags = {t for t in _split_refs(r.get("Component", "")) if t.startswith("CMP-")}
        if not tags:
            continue
        key = _norm_module(r.get("Module", ""))
        if key:
            out.setdefault(key, set()).update(tags)
    return out


def component_top_view(root):
    """The How-SW containment derivation (WI-073), shared by the right-sizing
    rule and the dashboard render so the item count and the picture never
    disagree. Returns a dict:
      inventory    `{norm: display}` arch-map modules (empty pre-arch-map)
      cmps         `[cmp dict]` real CMP rows
      by_id        `{cmp id: cmp dict}`
      children_of  `{cmp id: sorted[child cmp ids]}` (PartOf inverted)
      roots_of     `{cmp id: set(top-level root ids)}` (PartOf resolved up)
      module_cmps  `{norm: set(finest real CMP ids tagged on its LLRs)}`
      module_roots `{norm: set(top-level root ids)}` (derived, real modules only)
      top_roots    sorted `[cmp id]` top-level roots containing ≥1 module
      uncontained  sorted `[norm]` inventory modules with no membership
      count        `len(top_roots) + len(uncontained)`
    """
    names = arch_inventory(root)[0]
    inventory = {}
    for m in names:
        n = _norm_module(m)
        if n:
            inventory.setdefault(n, m)
    cmps = load_cmps(read_rows(root / CMP_CSV))
    by_id = {c["id"]: c for c in cmps}
    cmp_ids = set(by_id)
    roots_of = _cmp_roots(cmps)
    children_of = {c["id"]: [] for c in cmps}
    for c in cmps:
        for p in c["partof"]:
            if p in by_id:
                children_of[p].append(c["id"])
    for cid in children_of:
        children_of[cid] = sorted(children_of[cid])

    raw = module_components(root)
    module_cmps, module_roots = {}, {}
    top_roots, uncontained = set(), []
    for n in sorted(inventory):
        tags = raw.get(n, set()) & cmp_ids
        module_cmps[n] = tags
        if not tags:
            uncontained.append(n)
            module_roots[n] = set()
            continue
        r = set()
        for c in tags:
            r |= roots_of[c]
        module_roots[n] = r
        top_roots |= r
    return {
        "inventory": inventory,
        "cmps": cmps,
        "by_id": by_id,
        "children_of": children_of,
        "roots_of": roots_of,
        "module_cmps": module_cmps,
        "module_roots": module_roots,
        "top_roots": sorted(top_roots),
        "uncontained": uncontained,
        "count": len(top_roots) + len(uncontained),
    }


def knowledge_packs(root):
    """Real knowledge-pack labels under `docs/knowledge/` (research-knowledge.md
    §3a) — every `*.md` except the scaffolded `README.md` index. Empty (a
    non-adopter, an absent dir, or the index alone) means the knowledge layer is
    not in use, so the knowledge⇒component coupling stays dormant. Sorted for a
    deterministic count/message."""
    d = root / "docs" / "knowledge"
    if not d.is_dir():
        return []
    return sorted(p.stem for p in d.glob("*.md") if p.name.lower() != "readme.md")


def component_findings(root):
    """The How-SW component-coverage finding(s) (process-options.md "Component
    layer"). Returns the finding strings ([] when opted out or clean). The caller
    prints them WARN plain and promotes them to ERROR under `--strict` (G2+).
    Opt-out via `docs/components-check: off`. Two rules, both off the arch-map ⇒
    CMP join:

    - **Top-view right-sizing** (WI-073/FB5): vacuous when the arch-map inventory
      has ≤ TOP_VIEW_MAX modules (a small or pre-arch-map repo can never exceed the
      bound — the bound, not the registry, is the rule). Only when the inventory
      itself is larger than the bound do the declared components decide: a
      right-sized handful of top-level CMPs brings the top view back under it.
    - **Knowledge⇒component coupling** (WI-153; research-knowledge.md §3a,
      owner-ruled 2026-07-14): when ≥1 knowledge pack exists the component web is
      *expected* — any arch-map module the CMP join leaves uncontained is a finding
      regardless of the bound, because packs tie the *what* to the knowledge behind
      the *how* and that web must be robust wherever packs are enabled. Arms the
      existing join from pack presence; invents no new join, and is dormant (no
      cost to a non-adopter) until `docs/knowledge/` holds a real pack."""
    if not read_components_check_enabled(root):
        return []
    view = component_top_view(root)
    out = []
    packs = knowledge_packs(root)
    if packs and view["inventory"] and view["uncontained"]:
        out.append(
            "docs/knowledge/ holds {} pack(s) but {} arch-map module(s) are in no "
            "CMP-### component ({}); tag them via LLR `Component` cells so the "
            "knowledge⇒component web is complete, or set docs/components-check: "
            "off".format(len(packs), len(view["uncontained"]), CMP_CSV)
        )
    if len(view["inventory"]) > TOP_VIEW_MAX and view["count"] > TOP_VIEW_MAX:
        out.append(
            "How-SW top view has {} items ({} top-level component(s) + {} "
            "uncontained module(s)) — exceeds the bound of {}; declare CMP-### "
            "components in {} to contain modules (nest with PartOf), or set "
            "docs/components-check: off".format(
                view["count"],
                len(view["top_roots"]),
                len(view["uncontained"]),
                TOP_VIEW_MAX,
                CMP_CSV,
            )
        )
    return out


# --- the [phase]-[g*] archetype + phase-drop detector (WI-093) -----------------
# The derived-gate model (docs/specs/derived-gate-model.md §7/§9.3) structures a
# phase's pre-dev work as a first-class WI whose Title carries a `[<phase>]-[g<N>]`
# tag (g1 = requirement structuring, g2 = decomposition + TCs). The derived gate
# DROPPING below a phase's last-closed level is the signal that new/reopened
# content entered and a new phase-gate WI is due; the committed anchor is where
# phase identity + membership live (a git-history walk is rebase-sensitive and
# carries no membership, §9.3). Both checks are WARN-FIRST — like the connectivity
# coverage, they never change the exit code, at any gate.
GATE_FILE = "docs/gate"
PHASE_ANCHOR_RE = re.compile(r"^\[([^\]]+)\]-\[g([12])\]")
_GATE_LEVEL = {"G0": 0, "G1": 1, "G2": 2, "G3": 3}
_PER_PHASE_RE = re.compile(r"per-phase=(\S+)")


def read_derived_phases(root):
    """`{phase-label: gate-level-int}` parsed from the `# basis:` line of the
    generated docs/gate (derive_gate.py's hybrid cache — read the committed value,
    never recompute here). Empty when docs/gate is absent or a legacy hand-set gate
    with no basis line, so the drop detector is then vacuous. The basis format is
    derive_gate.basis_line's `per-phase=<label>=G<n>;...` (a shared contract)."""
    path = root / GATE_FILE
    if not path.exists():
        return {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if s.startswith("# basis:"):
            m = _PER_PHASE_RE.search(s)
            if not m or m.group(1) == "(none)":
                return {}
            out = {}
            for pair in m.group(1).split(";"):
                if "=" in pair:
                    label, gate = pair.rsplit("=", 1)
                    if gate in _GATE_LEVEL:
                        out[label] = _GATE_LEVEL[gate]
            return out
    return {}


def phase_anchors(wis):
    """`({(phase, gate): wi}, [shape-warnings])` — the `[phase]-[g*]` anchor WIs
    parsed from Titles. A duplicate (phase, gate) anchor, and a `-g2` whose
    predecessors omit its `-g1`, are warned (advisory only)."""
    anchors, warns = {}, []
    for w in wis:
        m = PHASE_ANCHOR_RE.match(w["title"])
        if not m:
            continue
        key = (m.group(1), int(m.group(2)))
        if key in anchors:
            warns.append(
                "duplicate phase-gate anchor [{}]-[g{}] ({} and {})".format(
                    key[0], key[1], anchors[key]["id"], w["id"]
                )
            )
            continue
        anchors[key] = w
    for (phase, gate), w in anchors.items():
        if gate == 2 and (phase, 1) in anchors:
            g1 = anchors[(phase, 1)]["id"]
            if g1 not in (w["preds"] + w["soft"]):
                warns.append(
                    "phase-gate anchor {} ([{}]-[g2]) does not list its "
                    "[{}]-[g1] ({}) as a predecessor".format(w["id"], phase, phase, g1)
                )
    return anchors, warns


def phase_findings(root, wis):
    """The phase-archetype + phase-drop warns (WI-093; warn-first). Returns the
    warn strings ([] when vacuous — no anchors and no per-phase drop data, the
    single-phase meta case). The drop detector reads the derived per-phase levels
    from docs/gate's basis: for each phase with a **done** `[phase]-[gN]` anchor
    (its recorded closed level), if the current derived level for that phase is
    below N, new/reopened content dropped it — warn to open a new phase-gate WI."""
    anchors, warns = phase_anchors(wis)
    derived = read_derived_phases(root)
    closed = {}  # phase -> highest gN whose [phase]-[gN] anchor is done
    for (phase, gate), w in anchors.items():
        if w["status"] == "done":
            closed[phase] = max(closed.get(phase, 0), gate)
    for phase, level in sorted(closed.items()):
        cur = derived.get(phase)
        if cur is not None and cur < level:
            warns.append(
                "phase {!r} dropped to G{} but its closed [{}]-[g{}] anchor recorded "
                "level G{} — new or reopened content entered; open a new "
                "[{}]-[g*] work item to structure it (derived-gate model §9.3)".format(
                    phase, cur, phase, level, level, phase
                )
            )
    return warns


def gate_first_findings(root, wis):
    """Warn when `next-wi` selects phase development ahead of unfinished G1/G2.

    The queue remains owner-ordered, so this is deliberately advisory. A selected
    non-anchor WI is a development candidate only when one of its SR refs names a
    Phase. For each such phase, an open `[phase]-[g1|g2]` anchor or a Draft SR is
    lower-gate work that should normally clear first. Repos without `next-wi`,
    phase tags, or a selected development WI are vacuous.
    """
    selected = _first_declared_line(root / NEXT_WI)
    if not selected:
        return []
    by_id = {w["id"]: w for w in wis}
    anchors, _ = phase_anchors(wis)
    sr_rows = {(r.get("SR-ID") or "").strip(): r for r in read_rows(root / SR_CSV)}
    findings = []
    for wid in _split_refs(selected.replace(";", " ")):
        wi = by_id.get(wid)
        if wi is None or any(wi is anchor for anchor in anchors.values()):
            continue
        phases = {
            (sr_rows.get(sid, {}).get("Phase") or "").strip() for sid in wi["srs"]
        }
        phases.discard("")
        for phase in sorted(phases):
            open_anchors = [
                (gate, anchor)
                for (anchor_phase, gate), anchor in anchors.items()
                if anchor_phase == phase and anchor["status"] != "done"
            ]
            if open_anchors:
                gate, anchor = min(open_anchors, key=lambda item: item[0])
                findings.append(
                    "dev {} queued ahead of open gate work {} in phase {} — clear "
                    "the lowest gate first ([{}]-[g{}])".format(
                        wid, anchor["id"], phase, phase, gate
                    )
                )
            drafts = sorted(
                sid
                for sid, sr in sr_rows.items()
                if (sr.get("Phase") or "").strip() == phase
                and (sr.get("Status") or "").strip().lower() == "draft"
            )
            if drafts:
                findings.append(
                    "dev {} queued while phase {} has Draft SR(s) {} — clear the "
                    "lowest gate first".format(wid, phase, ";".join(drafts))
                )
    return findings


def _read_status_tokens(root):
    """`(text, {WI ids named in status.md})`, or `(None, set())` when status.md
    is absent (R-B/R-C/R-D are then vacuous — a repo may keep no status
    blackboard). Read errors="replace" so a stray byte degrades, never crashes
    (the declared-policy reader idiom)."""
    path = root / STATUS_MD
    if not path.exists():
        return None, set()
    text = path.read_text(encoding="utf-8", errors="replace")
    return text, set(WI_TOKEN_RE.findall(text))


def ssot_findings(wis, root):
    """The status.md ↔ work-items.csv coherence findings (R-A…R-E) + the
    unknown-status lint, each as `(rule, hard, message)`.

    `hard=True` (R-A only) is an ERROR at every run — the incoherent-handoff
    rule. The rest are warn-first; the caller promotes them to errors under
    `--strict`. Kept OUT of `validate()` so the dashboard renderer
    (`gen_trajectory`, which imports `validate`) is unaffected by a status.md it
    never reads."""
    out = []
    status_text, status_tokens = _read_status_tokens(root)
    open_ids = {w["id"] for w in wis if w["status"] in OPEN_STATUSES}
    done_ids = {w["id"] for w in wis if w["status"] == "done"}

    for w in wis:
        st = w["status"]
        if st not in KNOWN_STATUSES:
            out.append(
                (
                    "status-vocab",
                    False,
                    "{}: unknown status {!r} (expected queued|active|done|"
                    "deferred)".format(w["id"], st),
                )
            )
        # R-A: Deliverable non-empty IFF done.
        if st == "done" and not w["deliverable"]:
            out.append(
                (
                    "R-A",
                    True,
                    "{}: status=done but the Deliverable is empty (a done WI "
                    "records what shipped)".format(w["id"]),
                )
            )
        elif st != "done" and w["deliverable"]:
            out.append(
                (
                    "R-A",
                    True,
                    "{}: status={} (open) but the Deliverable is non-empty (an "
                    "open WI's Deliverable is filled only at close)".format(
                        w["id"], st
                    ),
                )
            )
        # R-E: an open WI names a resolvable SpecRef (path or path#anchor).
        if st in OPEN_STATUSES:
            spec = w["specref"]
            if not spec:
                out.append(
                    (
                        "R-E",
                        False,
                        "{}: open WI has no SpecRef (name its spec-of-record: "
                        "docs/specs/WI-###.md or a doc#anchor)".format(w["id"]),
                    )
                )
            else:
                pathpart = spec.split("#", 1)[0].strip()
                if pathpart and not (root / pathpart).exists():
                    out.append(
                        (
                            "R-E",
                            False,
                            "{}: SpecRef {!r} does not resolve to an in-repo "
                            "file".format(w["id"], spec),
                        )
                    )

    # R-B/R-C/R-D need status.md; absent -> vacuous.
    if status_text is not None:
        for wid in sorted(open_ids):
            if wid not in status_tokens:
                out.append(
                    (
                        "R-B",
                        False,
                        "{}: open WI is not named in docs/status.md (its "
                        "context/lane)".format(wid),
                    )
                )
        if open_ids and not (open_ids & status_tokens):
            out.append(
                (
                    "R-C",
                    False,
                    "docs/status.md names no open WI id (it must name the "
                    "next/active work)",
                )
            )
        for wid in sorted(done_ids & status_tokens):
            out.append(
                (
                    "R-D",
                    False,
                    "{}: a done WI id appears in docs/status.md (closed work "
                    "leaves the working surface)".format(wid),
                )
            )
    return out


def run_state_findings(wis, root):
    """Warn when an end-state would park a runnable queued work item (WI-115).

    An absent ``docs/run-state`` means the repo has not adopted unattended
    operation, so this remains vacuous. Only hard predecessors constrain
    readiness; soft edges are advisory by definition.
    """
    state = _first_declared_line(root / RUN_STATE)
    if state not in ("NEEDS-HUMAN", "BLOCKED"):
        return []
    by_id = {w["id"]: w for w in wis}
    actionable = [
        w["id"]
        for w in wis
        if w["status"] == "queued"
        and all(by_id.get(pred, {}).get("status") == "done" for pred in w["preds"])
    ]
    if not actionable:
        return []
    return [
        "run-state {} but actionable queued WI(s) {} have all hard predecessors "
        "done — is the pause still real? A stale end-state parks agent-resume at "
        "boot".format(state, ";".join(sorted(actionable)))
    ]


def _git(root, args):
    """`git -C <root> <args>` stdout on success, else None (git absent, not a
    repo, no such object). Every staged-mode git call degrades to None so the
    no-validation-delta warn is a silent no-op outside a git checkout."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(root)] + args,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, ValueError):
        return None
    return proc.stdout if proc.returncode == 0 else None


def _tests_dir(root):
    """The declared tests root (docs/stack.ini [paths] tests), default `tests` —
    the surface a real validation-logic change would touch."""
    ini = root / "docs" / "stack.ini"
    if ini.exists():
        cp = configparser.ConfigParser(interpolation=None)
        try:
            cp.read_string(ini.read_text(encoding="utf-8", errors="replace"))
            if cp.has_option("paths", "tests"):
                return cp.get("paths", "tests").strip() or "tests"
        except configparser.Error:
            pass
    return "tests"


def _wi_status_map(rows):
    """`{wid: {"status", "srs"}}` for the real (non-`-000`) rows of a WI CSV."""
    out = {}
    for r in rows:
        wid = (r.get("WI-ID") or "").strip()
        if WI_ID_RE.match(wid) and not wid.endswith("-000"):
            out[wid] = {
                "status": (r.get("Status") or "queued").strip().lower(),
                "srs": _split_refs(r.get("SR-Refs", "")),
            }
    return out


def staged_findings(root):
    """The no-validation-delta warn (S0 ruling #2 corollary; warn-first).

    When a commit **closes** a WI (queued/active/deferred → done) that is a
    *follow-up* on an SR a previously-`done` WI already delivered (a shared
    `SR-Ref`), yet the staged change set touches neither the TC registry nor a
    file under the tests dir, the fix landed in the code but not the validation
    chain — so the same failure can recur. Returns warning strings ([] when not
    applicable). Compares the staged WI CSV against its HEAD version via git;
    any missing git context makes it a silent no-op (the hook has git; a gate
    run does not, and pays nothing). Line-splitting the HEAD CSV is safe here —
    a WI row is one physical line (no embedded newlines)."""
    staged = _git(root, ["diff", "--cached", "--name-only"])
    if staged is None:
        return []
    staged_names = set(staged.splitlines())
    if WI_CSV not in staged_names:
        return []  # no registry change staged -> nothing was closed here
    head_text = _git(root, ["show", "HEAD:" + WI_CSV])
    if head_text is None:
        return []  # first commit / file not in HEAD
    cur_map = _wi_status_map(read_rows(root / WI_CSV))
    head_map = _wi_status_map(list(csv.DictReader(head_text.splitlines())))

    prev_done_srs = {}  # SR id -> the done WI(s) that already delivered it
    for wid, h in head_map.items():
        if h["status"] == "done":
            for sr in h["srs"]:
                prev_done_srs.setdefault(sr, set()).add(wid)

    followups = []
    for wid, c in cur_map.items():
        was = head_map.get(wid, {}).get("status")
        if c["status"] == "done" and was != "done":
            shared = sorted(sr for sr in c["srs"] if sr in prev_done_srs)
            if shared:
                followups.append((wid, shared))
    if not followups:
        return []

    tests_prefix = _tests_dir(root).rstrip("/") + "/"
    chain_touched = any(f == TC_CSV or f.startswith(tests_prefix) for f in staged_names)
    if chain_touched:
        return []
    return [
        "{}: closes as a follow-up on {} (already delivered by a done WI) but "
        "the change set touches neither {} nor {} — the validation chain did "
        "not change (the fix must land in the chain, not just the code)".format(
            wid, ";".join(shared), TC_CSV, tests_prefix
        )
        for wid, shared in followups
    ]


# The critique-loop ratchet (WI-068). A `Verification=Critique` SR and its latest
# CRITIQUE verdict file (docs/reviews/NNN-CRITIQUE.md, the S8 verdict format).
RUBRICS_DIR = "docs/rubrics/"
REVIEWS_DIR = "docs/reviews"
CRITIQUE_VERDICT_RE = re.compile(
    r"^\s*VERDICT:\s*(APPROVE|CHANGES-REQUESTED)\s*(?:findings\s*=\s*(\d+))?",
    re.I | re.M,
)

OPEN_ITEMS_MD = "docs/open-items.md"
OI_SECTION_RE = re.compile(r"(?m)^(##\s+OI-\d+\b.*)$")
# A `[<phase>]-[g1|g2]` bracketed anchor appearing anywhere in a brief body (not
# line-anchored like PHASE_ANCHOR_RE, which matches a WI *title*).
RATIFY_ANCHOR_RE = re.compile(r"\[[^\]\[]+\]-\[g[12]\]")
# The brief satisfies the rule only by a Markdown *link* whose target names a
# ratification/hierarchy view — a bare `trace.py --ratify` command mention no
# longer counts (WI-146 REVIEW-A): a command can be unexecuted or wrong-scope, so
# it is not proof the generated view exists and is carried in the brief.
RATIFY_VIEW_RE = re.compile(r"\]\([^)]*(?:ratif|hierarch)[^)]*\)", re.IGNORECASE)


def ratify_brief_findings(root):
    """Warn-first brief lint (WI-146b): an `## OI-N` decision brief whose decision
    is a `[phase]-[g1|g2]` ratification should *link* the batch-scoped
    ratification hierarchy view (`trace.py --ratify <phase>`) instead of
    hand-copying registry rows. WARN only — never a gate fail (the house stance
    for prose surfaces, WI-129/132). Vacuous when `docs/open-items.md` is absent
    or carries no ratification brief, so a repo without the surface pays nothing."""
    path = root / OPEN_ITEMS_MD
    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    # Split on `## OI-N` headings: parts = [pre, head1, body1, head2, body2, ...],
    # so any intro prose before the first section (which may name a `[phase]-[g2]`
    # in passing) is correctly excluded from every brief body.
    parts = OI_SECTION_RE.split(text)
    out = []
    for i in range(1, len(parts), 2):
        head = parts[i].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        is_ratification = RATIFY_ANCHOR_RE.search(body) and re.search(
            r"ratif", body, re.IGNORECASE
        )
        if not is_ratification or RATIFY_VIEW_RE.search(body):
            continue
        oid = head.split()[1]  # the `OI-N` token
        out.append(
            "{}: a [phase]-[g1|g2] ratification brief should link the batch-scoped "
            "hierarchy view (generate it with `trace.py --ratify <phase>`) instead "
            "of hand-copying registry rows ({})".format(oid, OPEN_ITEMS_MD)
        )
    return out


def _load_critique_srs(root):
    """SR ids whose Verification is `Critique` (system-requirements.csv). Empty
    makes the critique ratchet vacuous — a repo with no perceptual SR pays
    nothing."""
    out = set()
    for r in read_rows(root / SR_CSV):
        sid = (r.get("SR-ID") or "").strip()
        if (
            sid
            and not sid.endswith("-000")
            and (r.get("Verification") or "").strip() == "Critique"
        ):
            out.add(sid)
    return out


def _latest_critique_verdict(root):
    """`(verdict, findings)` of the highest-numbered `docs/reviews/*-CRITIQUE.md`,
    or `(None, 0)`. The verdict file is not WI-tagged, so 'latest overall' is the
    honest proxy for 'the in-scope critique' (a recorded gap — the loop critiques
    one scope at a time, so the newest verdict is the live one in practice)."""
    d = root / REVIEWS_DIR
    if not d.is_dir():
        return None, 0
    files = sorted(d.glob("*-CRITIQUE.md"))
    if not files:
        return None, 0
    try:
        text = files[-1].read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None, 0
    m = CRITIQUE_VERDICT_RE.search(text)
    if not m:
        return None, 0
    return m.group(1).upper(), int(m.group(2) or 0)


def critique_ratchet_findings(root):
    """The lax-TC ratchet for the critique loop (WI-068; warn-first, the same
    no-validation-delta idea as `staged_findings`). When a staged commit **closes**
    a WI whose `SR-Refs` include a `Verification=Critique` SR, the latest CRITIQUE
    verdict is CHANGES-REQUESTED with findings, yet the staged set touches **neither**
    the TC registry, the tests dir, **nor** a `docs/rubrics/` file, the fix landed in
    the artifact but not the validation chain — so the same 'shipped it because
    nothing judged it' can recur. Returns warning strings ([] when not applicable).
    Any missing git context makes it a silent no-op, like `staged_findings`."""
    critique_srs = _load_critique_srs(root)
    if not critique_srs:
        return []
    verdict, findings = _latest_critique_verdict(root)
    if verdict != "CHANGES-REQUESTED" or findings <= 0:
        return []
    staged = _git(root, ["diff", "--cached", "--name-only"])
    if staged is None:
        return []
    staged_names = set(staged.splitlines())
    if WI_CSV not in staged_names:
        return []  # no WI close staged here
    head_text = _git(root, ["show", "HEAD:" + WI_CSV])
    if head_text is None:
        return []
    cur_map = _wi_status_map(read_rows(root / WI_CSV))
    head_map = _wi_status_map(list(csv.DictReader(head_text.splitlines())))

    closing = []
    for wid, c in cur_map.items():
        was = head_map.get(wid, {}).get("status")
        if c["status"] == "done" and was != "done":
            shared = sorted(sr for sr in c["srs"] if sr in critique_srs)
            if shared:
                closing.append((wid, shared))
    if not closing:
        return []

    tests_prefix = _tests_dir(root).rstrip("/") + "/"
    chain_touched = any(
        f == TC_CSV or f.startswith(tests_prefix) or f.startswith(RUBRICS_DIR)
        for f in staged_names
    )
    if chain_touched:
        return []
    return [
        "{}: closes on Critique-verified {} while the latest CRITIQUE verdict is "
        "CHANGES-REQUESTED ({} finding(s)), but the change set touches neither {}, "
        "{}, nor {} — harden the TC or add a rubric anchor (the fix must land in "
        "the chain, not just the artifact)".format(
            wid, ";".join(shared), findings, TC_CSV, tests_prefix, RUBRICS_DIR
        )
        for wid, shared in closing
    ]


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--root", default=".", help="repo root (default: current directory)"
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="promote the status↔registry coherence rules R-B…R-E from WARN to "
        "ERROR (wired at gate G2+; R-A always fails regardless)",
    )
    ap.add_argument(
        "--staged",
        action="store_true",
        help="run ONLY the warn-first no-validation-delta check over the staged "
        "commit (needs git; a silent no-op outside a git checkout)",
    )
    args = ap.parse_args()
    root = Path(args.root).resolve()

    if not read_trajectory_enabled(root):
        print("check_trajectory: off (docs/trajectory-check) — nothing to check.")
        return 0

    # --staged is the commit-time no-validation-delta warn only: never blocks,
    # never re-runs the full validation (the trajectory step already did). Two
    # warns: the follow-up-on-a-done-SR ratchet, and the critique-loop ratchet
    # (a WI closing under a CHANGES-REQUESTED critique without hardening the chain).
    if args.staged:
        for w in staged_findings(root) + critique_ratchet_findings(root):
            print("check_trajectory: WARN - {}".format(w), file=sys.stderr)
        return 0

    # Architecture-connectivity coverage (S5/WI-056; process.md §8) — warn-first,
    # never an exit-code change (even under --strict). Runs before the WI vacuity
    # return so a repo with modules + seams but no work items is still covered;
    # vacuous under docs/interfaces-check: off or a ≤1-module arch-map.
    for w in interface_findings(root):
        print("check_trajectory: WARN - {}".format(w), file=sys.stderr)

    # Ratification-brief hierarchy-view lint (WI-146b) — warn-first prose-surface
    # check: a `[phase]-[g1|g2]` ratification brief should link the generated
    # batch-scoped hierarchy view. Vacuous without a ratification brief.
    for w in ratify_brief_findings(root):
        print("check_trajectory: WARN - {}".format(w), file=sys.stderr)

    # How-SW top-view right-sizing (WI-073/FB5) — WARN plain, ERROR under --strict
    # (G2+). Runs before the WI vacuity return too (the bound is a property of the
    # arch-map inventory + the component registry, independent of work items), so
    # a repo with a big arch-map and no CMP rows still trips even with no WIs.
    comp_errors = []
    for msg in component_findings(root):
        if args.strict:
            comp_errors.append(msg)
        else:
            print("check_trajectory: WARN - {}".format(msg), file=sys.stderr)

    wis, integrity = load_wis(read_rows(root / WI_CSV))
    if not wis and not integrity:
        if comp_errors:
            for e in comp_errors:
                print("check_trajectory: ERROR - {}".format(e), file=sys.stderr)
            print(
                "check_trajectory: {} architecture finding(s).".format(
                    len(comp_errors)
                ),
                file=sys.stderr,
            )
            return 1
        print(
            "check_trajectory: clean (no work items — placeholder-only or absent "
            "registry; vacuously clean)."
        )
        return 0

    # Phase archetype + phase-drop detector (WI-093) — WARN-FIRST, never an
    # exit-code change (like the connectivity coverage). Vacuous on a single-phase
    # repo with no `[phase]-[g*]` anchors (the meta case).
    for w in phase_findings(root, wis):
        print("check_trajectory: WARN - {}".format(w), file=sys.stderr)
    # Lowest-gate-first queue ordering (WI-149) is an owner-order advisory, never
    # a gate failure; surface it beside the other phase-planning warnings.
    for w in gate_first_findings(root, wis):
        print("check_trajectory: WARN - {}".format(w), file=sys.stderr)

    errors = comp_errors + integrity + validate(wis, load_known_srs(root))
    # The SSOT coherence layer: R-A is always an error; R-B…R-E, the
    # run-state currency check, and the unknown-status lint are WARN unless
    # --strict promotes them.
    findings = ssot_findings(wis, root)
    findings.extend(("run-state", False, msg) for msg in run_state_findings(wis, root))
    for rule, hard, msg in findings:
        line = "{} {}".format(rule, msg)
        if hard or args.strict:
            errors.append(line)
        else:
            print("check_trajectory: WARN - {}".format(line), file=sys.stderr)
    if errors:
        for e in errors:
            print("check_trajectory: ERROR - {}".format(e), file=sys.stderr)
        print(
            "check_trajectory: {} error(s) in {}.".format(len(errors), WI_CSV),
            file=sys.stderr,
        )
        return 1

    done = sum(1 for w in wis if w["status"] == "done")
    print(
        "check_trajectory: clean ({} work item(s), {} done ({}%), graph "
        "acyclic).".format(len(wis), done, round(100 * done / len(wis)))
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
