#!/usr/bin/env python3
"""The requirement spine's registry CARRIER (OI-12 / docs/repo-lock.md D-5).

ONE FILE PER TIER, id-keyed TOML:

    [requirement.SR-137]        # the id PREFIX is retained, and BARE
    title = "One policy home, with a checked shape"
    sn_refs = ["SN-028"]        # refs are typed arrays
    phase = 5                   # ints are ints
    requirement = \"\"\"...\"\"\"       # multi-line strings hold the prose cells

replacing the two carriers the spine shipped with — stakeholder needs as
markdown prose tables, SR/LLR/TC as CSV. `tomllib` is stdlib at the kit's 3.11
floor, and the kit already sanctions TOML in two homes (`docs/process.toml`,
the `+++` frontmatter of every `docs/work/` spec).

WHAT THE CARRIER BUYS THAT A CHECK USED TO. Three integrity rules stop being
code and become properties of the parse: a DUPLICATE ID is a decode error (the
id is the table key, and TOML forbids declaring one twice); a REF LIST is an
array, retiring the split-on-whitespace rule and with it the
`SN-001 and SN-002` -> "`and` is an orphan" defect; an EMPTY CELL is an ABSENT
KEY, so "unset" and "set to empty" stop being the same value.

ROWS COME BACK UNDER TODAY'S COLUMN NAMES (`SR-ID`, `Title`, `SN-Refs`, ...),
which is the whole point of this module existing: the carrier change is data
plus a loader, not a sixteen-module rename braided into a migration. D-3 is the
pass that renames things, and it renames them on this carrier afterwards.

WHY THIS IS A SIBLING MODULE AND NOT ELEVEN COPIES — OWNER RULING 2026-08-10,
recorded as repo-lock D-6, AMENDING the F5 ruling that rejected a shared
`_kitcommon.py` at WI-078. The F5 rule buys cross-script copy-ability, and it
is a good rule; it was written for small stable PLUMBING (a five-line CSV
loader, the argparse preamble), where a divergence between copies is visible
and cheap. This is not that. Measured before the ruling: two readers need all
28 columns, three need none, and the rest need between 1 and 20 — so the
duplicated form is ~300 lines of VOCABULARY across eleven modules, and its
failure mode is the one this repo keeps finding. A copy that has not learned a
column does not fail loudly; it returns a row with that cell missing, which
every consumer downstream reads as "the cell is empty". That is silent content
loss on the registries the kit exists to make trustworthy.

So the vocabulary gets ONE home and the readers import it. The cost is real and
is paid where it belongs: a kit re-sync copies this file alongside its
importers (ADOPTING.md §6 lists it), exactly as `trace.py` already ships with
`trace_text.py`. "Independently copyable" becomes "copyable with its declared
siblings", which is what the kit already practised and had not yet said.

PURE BY DESIGN, like `trace_text.py`: text in, rows out. No git, no argv, and
the only filesystem it touches is `resolve()`'s existence check — because the
one thing that MUST NOT be duplicated eleven ways is the dual-home refusal.
Every caller does its own reading, so a script keeps deciding its own I/O.

Contracts: IF-102 — the seam this module declares (process.md §8; row of record
in docs/requirements/interfaces.csv).

Requirements: SR-147 (one machine-parseable carrier for the spine).
"""

import csv
import io
import tomllib

# The tier each registry's rows live under, keyed by the registry's ID COLUMN
# rather than by its path. A path carries a carrier suffix and therefore moves;
# the tier is the thing that does not.
SPINE_TABLE = {"SR-ID": "requirement", "LLR-ID": "design", "TC-ID": "test"}

# The carrier's keys -> today's COLUMN NAMES. STATED, never derived. Two
# reasons, and the second is the load-bearing one:
#
#   * no rule turns `sr_id` back into `SR-ID` and `sn_refs` into `SN-Refs`
#     without a list of which letter-runs are acronyms — a regex here would be
#     a rule nobody can predict from either side;
#   * a DERIVED mapping means renaming a column in code silently renames the
#     key on disk, orphaning that cell in every committed row. A stated map
#     makes the rename a visible edit to a reviewed table.
#
# This is the exact inverse of `migrate_carrier.KEY` (the writer), and
# tests/test_rule_sync.py pins the two as inverses so a column can never be
# renamed on one side of the conversion only.
SPINE_COLUMN = {
    "title": "Title",
    "sn_refs": "SN-Refs",
    "sr_refs": "SR-Refs",
    "verifies": "Verifies",
    "requirement": "Requirement",
    "rationale": "Rationale",
    "acceptance_criteria": "AcceptanceCriteria",
    "permutations": "Permutations",
    "priority": "Priority",
    "verification": "Verification",
    "status": "Status",
    "phase": "Phase",
    "area": "Area",
    "superseded_by": "SupersededBy",
    "lifecycle": "Lifecycle",
    "detail": "Detail",
    "module": "Module",
    "code_symbol": "CodeSymbol",
    "test_refs": "TestRefs",
    "level": "Level",
    "method": "Method",
    "expected": "Expected",
    "parameters": "Parameters",
    "automated": "Automated",
    "evidence": "Evidence",
    "tier": "Tier",
    "component": "Component",
    "notes": "Notes",
}

CARRIERS = (".toml", ".csv")


def stem(rel_path):
    """A registry path with its carrier suffix removed, so one constant can
    name a registry across a carrier change."""
    return str(rel_path).rsplit(".", 1)[0]


def carriers(rel_path):
    """Both carrier paths a registry can appear under.

    An applicability test (`git diff --name-only` against a watched set) has to
    name BOTH or the cutover commit — which deletes the `.csv` and adds the
    `.toml` — matches neither name, and the check silently skips the one commit
    that rewrites every row it watches."""
    return [stem(rel_path) + s for s in CARRIERS]


def value_to_cell(value):
    """One TOML value as the cell text the CSV carrier held.

    The inverse of `migrate_carrier.cell_to_value`, and deliberately the same
    rules its `value_to_cell` writes by: a ref array re-joins on the canonical
    `; `, an int stringifies. A row read here is therefore cell-for-cell what
    the CSV row was, which is what lets every consumer stay unchanged."""
    if isinstance(value, list):
        return "; ".join(str(v) for v in value)
    return str(value)


def rows_from_toml(text, id_col):
    """`{id: row}` under today's column names, or None when `text` does not
    parse.

    An ABSENT key stays absent rather than being filled with `""`. That is the
    carrier's whole point — "unset" and "set to empty" stop being the same
    value — and it costs nothing downstream, because every consumer reads a
    cell as `.get(col) or ""`, so absent and empty compare equal where it
    matters and stay distinguishable where it does not.

    None (not `{}`) on a decode error, because the two are OPPOSITE claims.
    `{}` says "this registry had no rows", which for a baseline read means
    "re-bless everything with no diff" and for a gate means "nothing to check".
    A carrier that cannot be read is ABSENT, and the caller has to be able to
    tell the two apart rather than inheriting the reading that fails open."""
    try:
        tables = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    out = {}
    for rid, cells in (tables.get(SPINE_TABLE[id_col]) or {}).items():
        row = {id_col: rid}
        for key, value in cells.items():
            row[SPINE_COLUMN.get(key, key)] = value_to_cell(value)
        out[rid] = row
    return out


def rows_from_csv(text, id_col):
    """`{id: row}` from the CSV carrier.

    Parsed over the FULL text, never line-split: spine cells are long and
    RFC-4180 quoting spans lines. Callers strip a BOM first (adversarial-review
    F4 — `git show` preserves a committed BOM, and a BOM'd header glues to the
    first column name so every row hides)."""
    return {r[id_col]: r for r in csv.DictReader(io.StringIO(text)) if r.get(id_col)}


def rows_from_text(text, id_col, carrier):
    """`{id: row}` for the named carrier (`".toml"` / `".csv"`), or None when a
    TOML text does not parse. The `-000` template example rows are kept — the
    caller filters them, because `is_example` is trace_text's rule and this
    module does not own the spine's semantics, only its carrier."""
    text = text.lstrip("﻿")  # F4, as above
    if carrier == ".toml":
        return rows_from_toml(text, id_col)
    return rows_from_csv(text, id_col)


def resolve(path):
    """The live carrier file for a registry, given a path under EITHER suffix.

    REFUSES both homes at once by raising, rather than resolving by precedence.
    That is the rule `bootstrap.py --migrate-config` already applies to the
    policy dials — "running with both homes live is REFUSED, not resolved by
    precedence" — and it exists for the same reason: a precedence rule means a
    half-finished migration keeps working while quietly reading the stale half,
    so the conversion is never actually finished and nobody finds out. Returns
    None when neither exists, which is the pre-scaffold case and is not an
    error here."""
    import pathlib

    base = pathlib.Path(stem(path))
    live = [base.with_suffix(s) for s in CARRIERS if base.with_suffix(s).is_file()]
    if len(live) > 1:
        raise SystemExit(
            "spine_carrier: REFUSED — {} exists under BOTH carriers ({}). Two "
            "homes for one fact is the state the migration exists to leave; "
            "delete the stale one in the same commit that wrote the other "
            "rather than letting a precedence rule pick.".format(
                base.name, ", ".join(p.name for p in live)
            )
        )
    return live[0] if live else None


def load(path, id_col, keep_examples=True):
    """The live registry as a LIST of rows in file order — the shape
    `csv.DictReader` returns, so a caller swaps its loader and changes nothing
    else. `[]` when the registry does not exist.

    Raises SystemExit on a carrier that exists and does not parse: at a LIVE
    read there is a file to fix and a person to tell, so degrading to "no rows"
    here would turn a broken registry into a clean gate."""
    live = resolve(path)
    if live is None:
        return []
    carrier = live.suffix
    rows = rows_from_text(
        live.read_text(encoding="utf-8-sig", errors="replace"), id_col, carrier
    )
    if rows is None:
        raise SystemExit(
            "spine_carrier: {} does not parse as TOML — refusing to report an "
            "unreadable registry as an empty one".format(live)
        )
    return [
        r for rid, r in rows.items() if keep_examples or not str(rid).endswith("-000")
    ]
