"""THE FRAME AND NEED-TIER RULES — pure joins over the depth-0 frame's rows.

The sibling of `coherence.py`, and built the same way: every rule here is a
JOIN ACROSS ROWS, it reads no file, and `trace.analyze` composes it and stays
its only caller. `trace.py` is held to an exact size ratchet, so a new rule
family lands here and `trace.py` grows by the composition lines alone (spine
map D21).

What lives here is the frame's own vocabulary about SYSTEMS OF INTEREST. A frame
can hold two: the system in OPERATION, and the system that builds and DELIVERS
it (`kitlib.spine.SYSTEM_VALUES`). Each boundary crossing names which one it
belongs to (SR-187), and a requirement's system is DERIVED from the crossings
its `Boundary-Refs` name (SR-219), recomputed on every run and never written
back to the requirement.

Rows are the carrier's column-keyed dicts (`B-ID`, `System`, `SR-ID`,
`Boundary-Refs`), exactly as `trace.load_registries` hands them over. Every
function returns plain finding strings, per `trace.frame_findings`' note on the
pair shape.

Stdlib only. A plain sibling of `scripts/`, not a `kitlib` module, for the
reason `coherence.py` records: these are the checker's rules, and the
scaffolder has no business importing them.

Contracts: IF-180 — the seam this module declares (process.md §8; row of record
in docs/requirements/interfaces.toml).

Contract IF-180: the frame and need-tier rule surface `trace.py` imports. Rows
    in, findings out, and nothing else: no I/O, no git, no filesystem, no argv.
    `frame_system_findings(bifs)` returns `(failures, advisories)`: the
    failures join the frame class and `trace.py --strict`'s exit code, the
    advisories ride the warn pipe and never join a failure set.
    `sr_system_advisories(srs, bifs)` returns warn-only advisories, and
    `crossing_systems(bifs)` returns a crossing-id to system map. Rows are the
    carrier's column-keyed dicts, and no function writes to a row it is handed.
"""

try:
    from kitlib.spine import SYSTEM_VALUES, refs
except ImportError:  # pragma: no cover - in-process fallback
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kitlib.spine import SYSTEM_VALUES, refs


def _system(row):
    """A crossing's declared system, stripped; `""` when it declares none."""
    return (row.get("System") or "").strip()


def frame_system_findings(bifs):
    """SR-187's crossing rule, as `(failures, advisories)`.

    A `System` value outside `SYSTEM_VALUES` is a FAILURE naming the crossing:
    the caller adds it to the frame class, which fails `--strict` beside the
    frame's other reference rules. A crossing declaring no value is an ADVISORY
    naming it and rides the warn pipe, because a frame drawn before the two
    systems were told apart is mid-authoring, not wrong. The frame's schema tier
    stays warn-only and judges no vocabulary for this cell, so this is the one
    place the pair is enforced. Vacuous when the frame declares no crossing.

    Implements: SR-187, LLR-212
    """
    failures, advisories = [], []
    allowed = " | ".join(SYSTEM_VALUES)
    for r in bifs:
        bid = r["B-ID"]
        value = _system(r)
        if not value:
            advisories.append(
                f"boundary {bid} declares no System ({allowed}) — the requirements "
                "naming it are placed by their other crossings"
            )
        elif value not in SYSTEM_VALUES:
            failures.append(
                f"boundary {bid} System={value!r} is not one of the two systems "
                f"of interest ({allowed})"
            )
    return failures, advisories


def crossing_systems(bifs):
    """Each crossing id -> its declared system, leaving out a crossing with none
    (and one whose value is outside the pair, which `frame_system_findings`
    already fails): such a crossing places no requirement.

    Implements: SR-219, LLR-213
    """
    return {r["B-ID"]: _system(r) for r in bifs if _system(r) in SYSTEM_VALUES}


def sr_system_advisories(srs, bifs):
    """SR-219's derived placement, as advisories: one per requirement whose
    named crossings belong to BOTH systems, naming the requirement and one
    crossing from each system.

    A requirement is placed by the crossings its `Boundary-Refs` name through
    `crossing_systems`; a crossing with no system contributes nothing, so the
    requirement is placed by its others. Nothing is written back to a row: the
    placement is recomputed on every run. Vacuous with no crossing declared.

    Implements: SR-219, LLR-213
    """
    systems = crossing_systems(bifs)
    if not systems:
        return []
    out = []
    for r in srs:
        first = {}
        for bid in refs(r.get("Boundary-Refs")):
            system = systems.get(bid)
            if system:
                first.setdefault(system, bid)
        if len(first) > 1:
            named = " and ".join(
                f"{first[s]} ({s})" for s in SYSTEM_VALUES if s in first
            )
            out.append(
                f"SR {r['SR-ID']} names crossings of both systems of interest: "
                f"{named} — a requirement belongs to one system; split it or "
                "re-point a crossing"
            )
    return out
