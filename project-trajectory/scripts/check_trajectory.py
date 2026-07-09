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

**Opt-out and vacuous by default** — the posture of the always-on
`docs/secrets-scan` floor. The check is on unless `docs/trajectory-check` reads
the one word `off`; and an *absent* or *placeholder-only* registry (nothing but
the inert `WI-000` example row) passes vacuously. So a fresh scaffold and a repo
that never adopts the layer both stay green for free — WI is an off-spine
optional registry, like procurement / assets, whose placeholder never blocks a
gate (`trace.py` does not read WI ids at all).

Usage:  python scripts/check_trajectory.py [--root .]
Exit codes: 0 clean / vacuous / opted-out, 1 a hard error, 2 usage/environment.
"""

import argparse
import csv
import re
import sys
from pathlib import Path

WI_CSV = "docs/requirements/work-items.csv"
SR_CSV = "docs/requirements/system-requirements.csv"

# A well-formed work-item id: `WI-` then digits (`WI-001`). The `-000` example
# row matches this shape but is inert (skipped from the graph — see load_wis).
WI_ID_RE = re.compile(r"^WI-\d+$")


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
            }
        )
    return wis, integrity


def _cycles(wis, pred_map):
    """Cycle strings found by DFS colouring over `pred_map` ([] = acyclic)."""
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {w["id"]: WHITE for w in wis}
    found = []

    def visit(node, stack):
        colour[node] = GREY
        for p in pred_map[node]:
            if colour[p] == GREY:
                found.append(" -> ".join(stack[stack.index(p) :] + [p]))
            elif colour[p] == WHITE:
                visit(p, stack + [p])
        colour[node] = BLACK

    for w in wis:
        if colour[w["id"]] == WHITE:
            visit(w["id"], [w["id"]])
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


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--root", default=".", help="repo root (default: current directory)"
    )
    args = ap.parse_args()
    root = Path(args.root).resolve()

    if not read_trajectory_enabled(root):
        print("check_trajectory: off (docs/trajectory-check) — nothing to check.")
        return 0

    wis, integrity = load_wis(read_rows(root / WI_CSV))
    if not wis and not integrity:
        print(
            "check_trajectory: clean (no work items — placeholder-only or absent "
            "registry; vacuously clean)."
        )
        return 0

    errors = integrity + validate(wis, load_known_srs(root))
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
