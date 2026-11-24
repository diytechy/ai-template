#!/usr/bin/env python3
"""The component view, GENERATED (WI-484 phase 3; OI-32 ruled option (d)).

One living answer to "what is this component obliged to do", derived from rows
that already have to be correct for the gate to pass — never hand-maintained,
so it cannot rot the way a prose detail document rots. It replaces the CMP
`DetailDoc` column, which shipped inert since it was minted, named a directory
the kit never created, and was read by no script: the generated view is the home
that column was pointing at, so the column retires with this file.

  docs/requirements/components.toml              WHICH components exist (hand)
  each file's `Component:` header                which files each one holds
  docs/requirements/low-level-requirements.toml  the design rows + the SR reach
  docs/requirements/system-requirements.toml     the requirement tier + hats
  docs/requirements/interfaces.toml              the seams
  docs/test/test-cases.toml                      where each design row sits
  -> docs/requirements/components.derived.toml   this view

THE SPLIT, and it is the ruling's: the hand file DECLARES a component (that it
exists, its name, its category, its knowledge refs, its acceptance); this file
DESCRIBES it. A GENERATED FILE NEVER CARRIES AN ACCEPTANCE (OI-30 D3) — machine
flipping an acceptance routes around the very dial `operator_accepts_through`
governs — so no maturity, standing or acceptance cell appears here, and nothing
here may be cited as evidence that an operator blessed anything.

WHAT IT DOES NOT SHOW, stated because the operator's own ruling states it: NOT
INTERNALS. A requirement list says what a component is obliged to do and nothing
about how its parts fit together. That is the ruled trade — the artifact that
stays true beats the artifact that shows mechanism and drifts — and a reader who
needs mechanism reads the design rows themselves, which this view names.

THE THREE COVERAGE EDGES, each answered EXPLICITLY here rather than papered
over (the brief demanded that; a generator that silently drops rows is
indistinguishable from one with a bug):

  * A DESIGN ROW IS PLACED, NEVER TAGGED (WI-1023, variant F): it sits at the
    owner component of each interface a test case verifying it names
    (`kitlib.spine.llr_placement`), at each when there are several, and one
    placed nowhere is listed in `[unplaced] llr_refs` and counted, never
    refused. A row names no component of its own.
  * AN SR THAT REACHES NO COMPONENT IS LISTED, ONCE, in `[unplaced]`. An SR
    carries no `Component` cell, so its components are derived through its
    placed LLR children, and an SR with none has none. Some of those are decompositions not yet written; some are CONSTRAINTS
    OVER EVERY COMPONENT (a stdlib rule, a cross-OS rule) that name no object and
    correctly belong to no component. THIS VIEW DOES NOT DISTINGUISH THE TWO,
    because nothing in the registries does, and inventing a per-repo list of
    "never will have children" inside shipped kit machinery would ship an
    adopter a judgement about rows in a repo they cannot read. Both are named
    and counted, and the reading is stated in the emitted header.
  * AN SR REACHING MORE THAN ONE COMPONENT APPEARS IN EVERY ONE OF THEM, and
    additionally in that component's `sr_shared_refs`. The view must not imply
    exclusive ownership: a requirement legitimately lives inside two components,
    and the shared list is what makes that visible rather than looking like a
    duplicate.
  * SEAMS ENTER THE VIEW — they are the one input that shows a component's EDGES
    rather than only its obligations. An IF row names its owner and far side
    as component ids or `external:` parties, and its place is DERIVED from
    them (variant F; there is no placement cell): it appears in each component
    it names, as `seam_internal_refs` of the lowest component enclosing every
    endpoint through `part_of` (none when an endpoint is `external:` or no
    component encloses them all) and as `seam_boundary_refs` of every other. A
    seam between two components is a boundary of BOTH. A row naming no
    component the registry declares is listed in `[unplaced]` rather than
    dropped.

Stdlib only, cross-platform, deterministic (sorted inputs, no clocks) so the
`--check` byte-compare is stable in any clone.

Component: CMP-009

Contracts: IF-139, IF-140 — the interface seams this module declares
(process.md §8; rows of record in docs/requirements/interfaces.toml).

Contract IF-139: the derived view's generator, delivered as a CLI. A plain run
    writes the view with explicit LF endings and exits 0, printing where it
    wrote or that the file was already current. `--check` writes nothing and
    exits 1 when the committed view is missing or stale — naming the command
    that regenerates it — and 0 when it is current. A repo that declares no
    real `CMP-###` row and carries no view is VACUOUS: exit 0, nothing written,
    so an optional layer nobody opted into can never fail a gate. `--root` and
    `--out` relocate the read and the write.
Contract IF-140: the derived view itself — a TOML document carrying one
    `[derived]` census table, one `[component_view.CMP-###]` table per declared
    component (`name`, `sr_refs`, `sr_shared_refs`, `llr_refs`, `hat_refs`,
    `modules`, `seam_internal_refs`, `seam_boundary_refs`) and one `[unplaced]`
    table naming the requirements, design rows and seams that reach no
    component; the census counts the unplaced design rows too. Every
    collection is sorted and nothing reads a clock or the environment, so the
    byte-compare behind `--check` is stable in any clone. It carries no
    maturity, standing or acceptance cell, ever, and nothing in it may be cited
    as evidence that an operator blessed anything.
"""

import argparse
import sys
from pathlib import Path

# The console guard's one home is the shipped package (WI-448 / D-8).
from kitlib.config import utf8_console as _utf8_console
from kitlib import spine as _kitspine
from kitlib.spine import is_example, refs

sys.path.insert(0, str(Path(__file__).resolve().parent))

import arch_inputs  # noqa: E402  (path set above)
import spine_carrier  # noqa: E402
import trace as tr  # noqa: E402

CMP_REL = "docs/requirements/components.toml"
SR_REL = "docs/requirements/system-requirements.toml"
LLR_REL = "docs/requirements/low-level-requirements.toml"
IF_REL = "docs/requirements/interfaces.toml"
TC_REL = "docs/test/test-cases.toml"
OUT_REL = "docs/requirements/components.derived.toml"

# The generated-but-LIVE staleness form (WI-505 / OI-56 ruled (a)): a generated
# artifact says who wrote it, that it is not hand-editable, what to cite
# INSTEAD, and the one command that re-derives it.
BANNER = (
    "# GENERATED by scripts/gen_components.py — do not hand-edit; cite the spine\n"
    "# registries (docs/requirements/*.toml), not this rendering.\n"
    "# Regenerate: python scripts/gen_components.py\n"
    "#\n"
    "# The component view: what each component is OBLIGED to do, derived from the\n"
    "# rows that already carry the obligation. It shows no internals, by design —\n"
    "# for mechanism, read the design rows named here.\n"
    "#\n"
    "# NO ACCEPTANCE CELL APPEARS HERE, EVER: maturity lives on the\n"
    "# hand-authored components.toml row, and nothing in this file is evidence\n"
    "# that an operator blessed anything.\n"
    "#\n"
    "# A design row sits at the owner component of each interface a test case\n"
    "# verifying it names; `[unplaced] llr_refs` lists the rows placed nowhere.\n"
    "#\n"
    "# An `[unplaced] sr_refs` entry reaches no component because it has no placed\n"
    "# design child — a decomposition not yet written or placed, or a constraint\n"
    "# over EVERY component that names no single object. This view does not\n"
    "# distinguish the two: no registry cell does, and the distinction is a\n"
    "# judgement about a specific repo's rows.\n"
)


def _load(root):
    """The five registries this view joins, each through the carrier resolver so
    a repo that has not migrated off CSV still renders."""
    root = Path(root)
    return (
        spine_carrier.load(root / CMP_REL, "CMP-ID", keep_examples=False),
        spine_carrier.load(root / SR_REL, "SR-ID", keep_examples=False),
        spine_carrier.load(root / LLR_REL, "LLR-ID", keep_examples=False),
        spine_carrier.load(root / IF_REL, "IF-ID", keep_examples=False),
        spine_carrier.load(root / TC_REL, "TC-ID", keep_examples=False),
    )


def seam_placement(row, parents):
    """One IF row as `(placed, internal)` — the components it is shown in, and
    the one it is INTERNAL to, from its endpoint cells alone.

    `parents` is `{CMP id: [part_of ids]}`. A row is shown in each component
    it names, and is internal to the lowest component enclosing every
    endpoint: the deepest component on every endpoint's `part_of` chain, which
    is shown too. An `external:` endpoint is enclosed by no component, so a row
    with one is internal to none. Placement is direction-blind and is for the
    views only; nothing checks against it.

    Implements: SR-070, LLR-199"""
    ends = [_kitspine.seam_owner(row)] + _kitspine.seam_far_side(row)[1]
    local = {e for e in ends if e.startswith("CMP-")}
    chains = [_ancestry(e, parents) for e in ends if e]
    common = set(chains[0]).intersection(*chains[1:]) if chains else set()
    lowest = next((c for c in chains[0] if c in common), None) if chains else None
    internal = {lowest} if lowest else set()
    return local | internal, internal


def _ancestry(cid, parents):
    """`cid` then its `part_of` ancestors, nearest first, cycle-guarded; an
    `external:` endpoint has none, not even itself."""
    chain = []
    while cid and cid.startswith("CMP-") and cid not in chain:
        chain.append(cid)
        cid = next(iter(parents.get(cid, ())), "")
    return chain


def _blank(name):
    return {
        "name": name,
        "modules": set(),
        "llr_refs": set(),
        "sr_refs": set(),
        "sr_shared_refs": set(),
        "hat_refs": set(),
        "seam_internal_refs": set(),
        "seam_boundary_refs": set(),
    }


def _add_members(view, srs, llrs, placement):
    """Fold the design tier into `view` and return `{SR id: {CMP ids}}`. Each
    design row's derived placement (`placement`, `kitlib.spine.llr_placement`)
    places the row and the requirements it reaches; the files are
    `_add_modules`'.

    A row placed at a component nothing declares is NOT invented here as a
    section: the interface naming that owner is trace.py's finding, and a view
    that materialized the id would hide it behind a plausible-looking heading.

    Implements: SR-070, LLR-199, LLR-403"""
    sr_by_id = {r["SR-ID"]: r for r in srs}
    sr_components = {}
    for row in llrs:
        hats = tr.effective_hats(row, sr_by_id)
        parents = [x for x in refs(row.get("SR-Refs")) if x in sr_by_id]
        for cid in placement.get(row["LLR-ID"], ()):
            if cid not in view:
                continue
            view[cid]["llr_refs"].add(row["LLR-ID"])
            view[cid]["hat_refs"].update(hats)
            view[cid]["sr_refs"].update(parents)
            for pid in parents:
                sr_components.setdefault(pid, set()).add(cid)
    for pid, comps in sr_components.items():
        for cid in comps if len(comps) > 1 else ():
            view[cid]["sr_shared_refs"].add(pid)
    return sr_components


def _add_modules(view, declared):
    """Fold each declared file into its component's `modules`: a file belongs
    to the component its `Component:` header declares (`declared`, `{path: CMP
    id}`), and a component nothing declares gets no section here either."""
    for path, cid in declared.items():
        if cid in view:
            view[cid]["modules"].add(path)


def _add_seams(view, ifs, parents):
    """Fold the seam tier into `view` and return the ids it could not place."""
    unplaced = []
    for row in ifs:
        placed, internal = seam_placement(row, parents)
        placed &= set(view)
        if not placed:
            unplaced.append(row["IF-ID"])
        for cid in placed:
            key = "seam_internal_refs" if cid in internal else "seam_boundary_refs"
            view[cid][key].add(row["IF-ID"])
    return unplaced


def build(cmps, srs, llrs, ifs, tcs, declared):
    """The whole view as plain data: `(per_component, unplaced)`.

    Separated from `render` so the derivation is testable without parsing TOML
    back out of a string.

    `declared` is each file's component as its `Component:` header declares it
    (`arch_inputs.component_headers`), which places the files. A seam is placed
    from its endpoint cells and the components' `part_of` (`seam_placement`).
    A design row is placed through the interfaces the test cases `tcs`
    verifying it name (`kitlib.spine.llr_placement`); one placed nowhere is in
    `unplaced["llr_refs"]`.

    Implements: SR-070, LLR-199, LLR-403"""
    view = {r["CMP-ID"]: _blank((r.get("Name") or "").strip()) for r in cmps}
    placement = _kitspine.llr_placement(tcs, ifs, llrs)
    sr_components = _add_members(view, srs, llrs, placement)
    _add_modules(view, declared)
    parents = {r["CMP-ID"]: refs(r.get("PartOf")) for r in cmps}
    unplaced_seams = _add_seams(view, ifs, parents)
    unplaced_srs = sorted(r["SR-ID"] for r in srs if r["SR-ID"] not in sr_components)
    placed = {lid for v in view.values() for lid in v["llr_refs"]}
    return view, {
        "sr_refs": unplaced_srs,
        "llr_refs": sorted(r["LLR-ID"] for r in llrs if r["LLR-ID"] not in placed),
        "seam_refs": sorted(unplaced_seams),
    }


def _array(name, values):
    """One TOML array, one element per line — so a `git diff` of this file names
    the row that entered or left rather than re-wrapping a paragraph."""
    if not values:
        return "{} = []\n".format(name)
    body = "".join('  "{}",\n'.format(v) for v in values)
    return "{} = [\n{}]\n".format(name, body)


def render(root):
    """The whole file as text. Deterministic: every collection is sorted and
    nothing reads a clock or the environment."""
    cmps, srs, llrs, ifs, tcs = _load(root)
    declared = arch_inputs.component_headers(root)[0]
    view, unplaced = build(cmps, srs, llrs, ifs, tcs, declared)
    out = [BANNER]
    out.append(
        "\n[derived]\n"
        + "components = {}\n".format(len(view))
        + "design_rows = {}\n".format(sum(len(v["llr_refs"]) for v in view.values()))
        + "design_rows_unplaced = {}\n".format(len(unplaced["llr_refs"]))
        + "seam_rows = {}\n".format(len(ifs))
        + "requirements_placed = {}\n".format(len(srs) - len(unplaced["sr_refs"]))
        + "requirements_unplaced = {}\n".format(len(unplaced["sr_refs"]))
        + "seams_unplaced = {}\n".format(len(unplaced["seam_refs"]))
    )
    for cid in sorted(view):
        row = view[cid]
        out.append("\n[component_view.{}]\n".format(cid))
        out.append('name = "{}"\n'.format(row["name"].replace('"', "'")))
        for key in (
            "sr_refs",
            "sr_shared_refs",
            "llr_refs",
            "hat_refs",
            "modules",
            "seam_internal_refs",
            "seam_boundary_refs",
        ):
            out.append(_array(key, sorted(row[key])))
    out.append("\n[unplaced]\n")
    out.append(_array("sr_refs", unplaced["sr_refs"]))
    out.append(_array("llr_refs", unplaced["llr_refs"]))
    out.append(_array("seam_refs", unplaced["seam_refs"]))
    return "".join(out)


def _has_components(root):
    """True when a real (non-`-000`) CMP row exists. The whole layer is optional
    and off-spine, so a repo that never names a component pays nothing."""
    rows = spine_carrier.load(Path(root) / CMP_REL, "CMP-ID", keep_examples=True)
    return any(not is_example(r["CMP-ID"]) for r in rows)


def main(argv=None):
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument(
        "--out", default=None, help="output path (default {})".format(OUT_REL)
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="exit 1 when the view is stale, writing nothing (the freshness gate)",
    )
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    out = Path(args.out) if args.out else root / OUT_REL
    # Vacuous — exit 0, write nothing — for a repo that declares no component and
    # carries no view: a fresh scaffold ships only the inert CMP-000 row, and the
    # gate must not fail it over an optional layer it never opted into.
    if not _has_components(root) and not out.is_file():
        print(
            "gen_components: no real CMP row in {} and no {} — nothing to "
            "derive (vacuous).".format(CMP_REL, OUT_REL)
        )
        return 0
    fresh = render(root)
    if args.check:
        if not out.is_file():
            print(
                "gen_components: {} missing — run "
                "`python scripts/gen_components.py`".format(OUT_REL)
            )
            return 1
        if out.read_text(encoding="utf-8").replace("\r\n", "\n") != fresh:
            print(
                "gen_components: {} STALE — run "
                "`python scripts/gen_components.py`".format(OUT_REL)
            )
            return 1
        print("gen_components: component view up to date.")
        return 0
    if out.is_file() and out.read_text(encoding="utf-8").replace("\r\n", "\n") == fresh:
        print("gen_components: already up to date -> {}".format(out))
        return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    # Explicit LF: `write_text` newline-translates, and a CRLF copy would fail
    # `--check` immediately after being generated (the 122-REVIEW-A defect).
    with out.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(fresh)
    print("gen_components: wrote {}".format(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
