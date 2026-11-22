#!/usr/bin/env python3
"""Component rules: the How-SW top view, knowledge coupling and the partition's derivation record.

`component_top_view` derives which components and modules make the software
architecture's first view. `component_findings` holds that view to
`TOP_VIEW_MAX`, asks every module to sit in a component once knowledge packs
exist, runs the cross-component seam check and the kernel allowlist's parse
rule from `arch_seams`, and checks each component row's derivation record
(`derivation_record_findings`). Their inputs come from `arch_inputs`;
``trajectory_arch`` re-exports them for ``check_trajectory``.

Component: CMP-006

Contracts: IF-320 — the interface seam this file declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-320: the component rule surface ``trajectory_arch`` re-exports.
`component_top_view(root)` returns the containment derivation as a dict
(`inventory`, `cmps`, `by_id`, `children_of`, `roots_of`, `module_cmps`,
`module_roots`, `top_roots`, `uncontained`, `count`), the one join the
dashboard and the bound both read. `component_findings(root)` returns finding
strings, `[]` when `[checks] components_check = false`.
`knowledge_packs(root)` lists the real packs under `docs/knowledge/`, and
`TOP_VIEW_MAX` is the bound. The module performs no writes.
"""

import re
import sys
from pathlib import Path

try:
    from kitlib import spine as _kitspine
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kitlib import spine as _kitspine

import spine_carrier
from arch_inputs import (
    CMP_CSV,
    CMP_ID_RE,
    _norm_module,
    arch_inventory,
    component_headers,
    load_cmps,
    read_components_check_enabled,
)
from arch_seams import cross_component_findings, kernel_allow_parse_findings


# The How-SW top view is bounded at this many items (top-level components +
# uncontained modules); exceeding it drives right-sizing of the component
# designations (WI-073, FB5 — warn plain, error --strict).
TOP_VIEW_MAX = 10


# --- the How-SW top-view right-sizing rule (WI-073/FB5) ------------------------
# The software-architecture diagram's first view is bounded at TOP_VIEW_MAX
# items = top-level components (a CMP with no PartOf that contains ≥1 arch-map
# module) + uncontained modules. Membership is each file's `Component:` header
# (`arch_inputs.component_headers`, joined by `kitlib.spine.module_components`);
# CMP nesting via PartOf.
# The derivation below is the ONE home for that join — gen_trajectory imports it
# (`ct.component_top_view`) so the render and this rule can never disagree on the
# count. Small stable loaders duplicated per the F5 convention (no sibling import
# into check_trajectory).


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


def component_top_view(root):
    """The How-SW containment derivation (WI-073), shared by the right-sizing
    rule and the dashboard render so the item count and the picture never
    disagree. Returns a dict:
      inventory    `{norm: display}` arch-map modules (empty pre-arch-map)
      cmps         `[cmp dict]` real CMP rows
      by_id        `{cmp id: cmp dict}`
      children_of  `{cmp id: sorted[child cmp ids]}` (PartOf inverted)
      roots_of     `{cmp id: set(top-level root ids)}` (PartOf resolved up)
      module_cmps  `{norm: set(real CMP ids its header declares)}`, empty
                   for a module with no valid declaration
      module_roots `{norm: set(top-level root ids)}` (derived, real modules only)
      top_roots    sorted `[cmp id]` top-level roots containing ≥1 module
      uncontained  sorted `[norm]` inventory modules with no membership
      count        `len(top_roots) + len(uncontained)`

    Implements: SR-159, LLR-049
    """
    names = arch_inventory(root)[0]
    inventory = {}
    for m in names:
        n = _norm_module(m)
        if n:
            inventory.setdefault(n, m)
    cmps = load_cmps(spine_carrier.load(root / CMP_CSV, "CMP-ID"))
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

    raw = _kitspine.module_components(component_headers(root)[0])
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


# --- the component derivation record (SR-165, LLR-172; WI-999) -----------------
# Eight flat cells on a CMP row, since the carrier refuses a nested table. One
# row per partition holds the record; the partition's other rows carry only
# `Derivation`, the id of that row. `component_findings` is its one reader.
_RECORD_ELEMENTS = tuple(
    "Candidates Objective Constraints Scores Selected Ruling".split()
)
_RECORD_CELLS = _RECORD_ELEMENTS + ("Override",)
_NUMBER_RE = re.compile(r"[-+]?\d+(?:\.\d+)?")
_NO_RECORD = (
    "no derivation record: declare candidates, objective, constraints, scores, "
    "selected and ruling, or cite the row holding the partition's record with "
    "derivation, or set docs/process.toml [checks] components_check = false"
)


def _cell(row, column):
    return (row.get(column) or "").strip()


def _entries(row, column):
    """A list cell's entries; the carrier joins a TOML array on `;`."""
    return [e.strip() for e in _cell(row, column).split(";") if e.strip()]


def _score_findings(row, candidates):
    """`(scores, findings)`: each candidate's number, then each score entry
    outside `<candidate>=<number>`, each extra score and each missing one."""
    scores, named, out = {}, set(), []
    for entry in _entries(row, "Scores"):
        name, sep, number = (part.strip() for part in entry.partition("="))
        if not sep or not _NUMBER_RE.fullmatch(number):
            out.append(f"`scores` entry {entry!r} is not `<candidate>=<number>`")
        elif name in named or (candidates and name not in candidates):
            out.append(f"`scores` entry {entry!r} is an extra score")
        else:
            scores[name] = float(number)
        named.add(name)
    missing = [c for c in candidates if c not in named] if _cell(row, "Scores") else []
    out += [f"`scores` has no score for candidate {c}" for c in missing]
    return scores, out


def _constraint_findings(row, candidates):
    """`(violators, findings)`: the candidates a constraint names, then each
    entry outside `<constraint>: <violators>` and each violator not a candidate.
    The single entry `none` declares no constraint."""
    entries = _entries(row, "Constraints")
    violators, out = set(), []
    for entry in [] if entries == ["none"] else entries:
        name, sep, who = entry.partition(":")
        if not sep or not name.strip():
            out.append(
                f"`constraints` entry {entry!r} is not `<name>: <violators>` "
                "or the single entry `none`"
            )
        violators.update(who.split())
    for v in sorted(violators - set(candidates)) if candidates else []:
        out.append(f"`constraints` names violator {v}, which is not a candidate")
    return violators, out


def _override_findings(override, selected):
    """The optional override: `<candidate>: <reason>`, naming `selected`."""
    who, sep, reason = (part.strip() for part in override.partition(":"))
    if override and (not sep or not who or not reason):
        return [f"`override` {override!r} is not `<candidate>: <reason>`"]
    if override and selected and who != selected:
        return [f"`override` names {who}, not the selected {selected}"]
    return []


def _record_findings(row):
    """`(record, findings)` for a row holding the record: one finding per
    missing element, then each malformed cell. `record` is None unless there
    is no finding, the one state the ranking recompute reads."""
    out = [f"`{c.lower()}` is missing" for c in _RECORD_ELEMENTS if not _cell(row, c)]
    candidates = _entries(row, "Candidates")
    for c in sorted({c for c in candidates if candidates.count(c) > 1}):
        out.append(f"`candidates` lists {c} more than once")
    objective = _cell(row, "Objective")
    verb, _, metric = objective.partition(" ")
    if objective and (verb not in ("minimize", "maximize") or not metric.strip()):
        out.append(f"`objective` {objective!r} is not `minimize|maximize <metric>`")
    scores, score_out = _score_findings(row, candidates)
    violators, constraint_out = _constraint_findings(row, candidates)
    out += score_out + constraint_out
    selected = _cell(row, "Selected")
    if selected and candidates and selected not in candidates:
        out.append(f"`selected` {selected} is not a candidate")
    out += _override_findings(_cell(row, "Override"), selected)
    sign = 1 if verb == "minimize" else -1
    key = {c: (c in violators, sign * scores.get(c, 0)) for c in candidates}
    return (None if out else (candidates, key, selected)), out


def _ranking_findings(record, override):
    """The recompute: a feasible candidate (one no constraint names) ranks above
    every infeasible one, then by score in the objective's direction; equal
    keys tie, and a tie may be listed in either order."""
    candidates, key, selected = record
    out = []
    for i, c in enumerate(candidates):
        above = [d for d in candidates[i + 1 :] if key[d] < key[c]]
        if above:
            out.append(f"the recompute ranks {above[0]} above {c}, listed before it")
            break
    first = not any(key[c] < key[selected] for c in candidates)
    if not first and not override:
        out.append(f"`selected` {selected} is not ranked first and has no `override`")
    if first and override:
        out.append(f"`override` is present although `selected` {selected} ranks first")
    return out


def _derivation_findings(rid, row, live):
    """Why a citing row's `Derivation` does not resolve, in one hop, to a live
    row holding the record ([] when it does)."""
    target = _cell(row, "Derivation")
    if any(_cell(row, c) for c in _RECORD_CELLS):
        return ["`derivation` sits beside record cells: hold the record or cite it"]
    if target == rid:
        return ["`derivation` points at the row itself"]
    if target not in live:
        return [f"`derivation` names {target}, which is no live component row"]
    if _cell(live[target], "Derivation"):
        return [f"`derivation` names {target}, which itself cites another row"]
    return []


def _row_causes(rid, row, live):
    """One live row's causes: its citation's when it cites, else its record's,
    the ranking recompute running only on a record with no other cause. None
    when the row neither holds a record nor cites one."""
    if _cell(row, "Derivation"):
        return _derivation_findings(rid, row, live)
    if not any(_cell(row, c) for c in _RECORD_CELLS):
        return None
    record, causes = _record_findings(row)
    return causes or _ranking_findings(record, _cell(row, "Override"))


def derivation_record_findings(rows):
    """Each live CMP row's derivation-record finding (SR-165): the row holds
    the record or cites, with `Derivation`, the one live row holding it. Absent,
    incomplete (one finding per missing element) and malformed records are
    reported, and only a record with none of those is recomputed: an order the
    recompute contradicts, a selection not ranked first with no override, and
    an override where the selection ranks first. A finding against a held
    record is reported once, on the holding row, naming the rows citing it.
    `-000` rows are vacuous, as is a registry with no live row.

    Implements: SR-165, LLR-172"""
    live, citers, out = {}, {}, []
    for r in rows:
        rid = _cell(r, "CMP-ID")
        if CMP_ID_RE.match(rid) and not rid.endswith("-000"):
            live[rid] = r
    for rid, row in live.items():
        if _cell(row, "Derivation") not in ("", rid):
            citers.setdefault(_cell(row, "Derivation"), []).append(rid)
    for rid, row in live.items():
        label = f"{CMP_CSV} {rid}"
        if rid in citers:
            label += " (record cited by {})".format(", ".join(citers[rid]))
        causes = _row_causes(rid, row, live)
        if causes is None:
            out.append(f"{label}: {_NO_RECORD}")
        out += [f"{label}: derivation record: {c}" for c in causes or []]
    return out


def component_findings(root):
    """The How-SW component-coverage finding(s) (process-options.md "Component
    layer"). Returns the finding strings ([] when opted out or clean). The caller
    prints them WARN plain and promotes them to ERROR under `--strict` (DevStg-Tests+).
    Opt-out via `[checks] components_check = false`. Six rules, all off the files'
    `Component:` headers, and the registry's own derivation record:

    - **Every file in the scope declares its component** (WI-1021): see
      `arch_inputs.component_headers` — a file whose header declaration is
      absent, doubled, malformed or names no live component row is a finding,
      and it belongs to no component.

    - **Top-view right-sizing** (WI-073/FB5): vacuous when the arch-map inventory
      has ≤ TOP_VIEW_MAX modules (a small or pre-arch-map repo can never exceed the
      bound — the bound, not the registry, is the rule). Only when the inventory
      itself is larger than the bound do the declared components decide: a
      right-sized handful of top-level CMPs brings the top view back under it.
    - **Knowledge⇒component coupling** (WI-153; research-knowledge.md §3a,
      operator-ruled 2026-07-14): when ≥1 knowledge pack exists the component web is
      *expected* — any arch-map module the CMP join leaves uncontained is a finding
      regardless of the bound, because packs tie the *what* to the knowledge behind
      the *how* and that web must be robust wherever packs are enabled. Arms the
      existing join from pack presence; invents no new join, and is dormant (no
      cost to a non-adopter) until `docs/knowledge/` holds a real pack.
    - (The WI-399 "containment owed where a module is ADDED" delta rule is
      RETIRED — WI-455 made the inventory the LIVE source tree, so a lane's
      added module is simply IN the inventory and the coupling rule above
      fires on it directly; there is no committed-vs-disk gap left to bridge.)
    - **Cross-CMP edges need a declared seam** (WI-064): see
      `cross_component_findings` — an import edge between two components with
      no covering IF-### row, and an edge touching a file with no valid
      declaration, reported as unclassified. An edge into a declared
      shared-kernel module (OI-48 (d), WI-494) is exempted once both ends are
      declared — see `_cross_component_scan`.
    - **Declared-kernel allowlist hygiene** (OI-48 (d), WI-494): see
      `kernel_allow_parse_findings` — a `docs/kernel-modules-allow` line the
      grammar cannot read (missing module, missing reason, or no separator)
      is reported, the same parse-honesty shape
      `if_tc_allow_hygiene_findings` and `provenance_allow_parse_findings`
      use for their own allow-files. A malformed line grants no exemption
      either way (fail-safe), so this rule is reporting, never gating, the
      fail-safe default — it just says so out loud instead of leaving the
      author to notice a seam finding that did not go away.
    - **The partition's derivation record** (SR-165, WI-999): see
      `derivation_record_findings` — each live CMP row holds the record or
      cites the row that does, and the record recomputes. Off the registry
      alone, so it needs no arch-map.

    Implements: SR-159, LLR-049, SR-165, LLR-172
    """
    if not read_components_check_enabled(root):
        return []
    view = component_top_view(root)
    out = []
    packs = knowledge_packs(root)
    if packs and view["inventory"] and view["uncontained"]:
        # The module NAMES ride in the finding (capped): the retired WI-399
        # delta message carried them so a lane knew WHICH file to tag, and
        # under the live inventory (WI-455) this rule is that lane's first
        # and only firing point.
        shown = ", ".join(view["uncontained"][:8]) + (
            ", …" if len(view["uncontained"]) > 8 else ""
        )
        out.append(
            "docs/knowledge/ holds {} pack(s) but {} arch-map module(s) are in no "
            "CMP-### component ({}); declare each one's component in its "
            "`Component:` header (process.md §8) so the knowledge⇒component web "
            "is complete, or set docs/process.toml [checks] components_check = "
            "false".format(len(packs), len(view["uncontained"]), shown)
        )
    if len(view["inventory"]) > TOP_VIEW_MAX and view["count"] > TOP_VIEW_MAX:
        out.append(
            "How-SW top view has {} items ({} top-level component(s) + {} "
            "uncontained module(s)) — exceeds the bound of {}; declare CMP-### "
            "components in {} to contain modules (nest with PartOf), or set "
            "docs/process.toml [checks] components_check = false".format(
                view["count"],
                len(view["top_roots"]),
                len(view["uncontained"]),
                TOP_VIEW_MAX,
                CMP_CSV,
            )
        )
    out.extend(component_headers(root)[1])
    out.extend(cross_component_findings(root))
    out.extend(kernel_allow_parse_findings(root))
    cmp_rows = spine_carrier.load(root / CMP_CSV, "CMP-ID")
    out.extend(derivation_record_findings(cmp_rows))
    return out
