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
import re
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

# The row tiers moved CSV -> TOML; the need tier moved markdown -> TOML. Both
# lists are ordered NEW FIRST, because resolution prefers the destination
# carrier and falls back to the legacy one — never the other way round, or a
# half-finished migration keeps reading the file it was supposed to leave.
CARRIERS = (".toml", ".csv")
NEED_CARRIERS = (".toml", ".md")


def stem(rel_path):
    """A registry path with its carrier suffix removed, so one constant can
    name a registry across a carrier change."""
    return str(rel_path).rsplit(".", 1)[0]


def carriers(rel_path, suffixes=CARRIERS):
    """Both carrier paths a registry can appear under.

    An applicability test (`git diff --name-only` against a watched set) has to
    name BOTH or the cutover commit — which deletes the `.csv` and adds the
    `.toml` — matches neither name, and the check silently skips the one commit
    that rewrites every row it watches."""
    return [stem(rel_path) + s for s in suffixes]


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


def resolve(path, suffixes=CARRIERS):
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
    live = [base.with_suffix(s) for s in suffixes if base.with_suffix(s).is_file()]
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


# --- the stakeholder-need tier ------------------------------------------------
# The SN tier is the reason the spine had TWO carriers: needs shipped as
# markdown prose tables in three different SHAPES, and reading 32 of them cost
# ~166 code lines across 14 functions in 8 modules while reading all 436
# SR+LLR+TC rows cost `csv.DictReader`. Under one carrier a need is a table like
# any other row, and two long-standing sharp edges go with the markdown:
#
#   * SECTION-AS-STATE is retired. Draft-ness was "appears under a heading whose
#     text contains the word draft", scraped by one function while the id
#     universe was scraped by another — and during the 2026-08-10 sitting a
#     prose MENTION of an id under the draft heading silently re-drafted an
#     already-attested need. `kind` is now a field on the need itself.
#   * THE EDGE-CASE TIER keeps its own fields (`lifecycle` / `scenario` /
#     `expected`) instead of being folded onto the core four at read time.
NEED_TABLE = "need"
SN_CORE = ("need", "why", "priority", "acceptance")
SN_EDGE = ("lifecycle", "scenario", "expected")
_SN_HEADING = re.compile(r"^#{2,}\s+(.*)$")
_SN_ROW = re.compile(r"^\|\s*(SN-\d+)\s*\|")


def _kind_from_heading(title):
    """Which of the three tables a markdown heading opens. Legacy carrier only:
    under TOML the need CARRIES its kind, which is the whole point."""
    t = title.lower()
    if "draft" in t:
        return "draft"
    if "edge" in t:
        return "edge"
    return "core" if ("core" in t or "need" in t) else None


def needs_from_markdown(text):
    """`[{id, kind, **fields}]` from the legacy prose tables, document order.

    Cells are resolved by the table's SHAPE, never by fixed offset: the three
    tables have different widths, and reading an edge row at the core offsets is
    what published SN-013 as "Provision" — its LIFECYCLE word — for the whole
    life of the dashboard and the OKF bundle."""
    kind, out = None, []
    for line in text.split("\n"):
        heading = _SN_HEADING.match(line)
        if heading:
            kind = _kind_from_heading(heading.group(1))
            continue
        row = _SN_ROW.match(line)
        if not row:
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        # A row with NO heading above it is resolved by the table's SHAPE, which
        # is what the readers this replaces always did: the edge table is three
        # cells wide and carries no priority, the core table four. Requiring a
        # heading would refuse a headerless fragment — and the fragment is the
        # normal case for a test fixture and for a table pasted into a brief.
        row_kind = kind or ("edge" if len(cells) - 1 == len(SN_EDGE) else "core")
        names = SN_EDGE if row_kind == "edge" else SN_CORE
        need = {"id": cells[0], "kind": row_kind}
        need.update(dict(zip(names, cells[1 : 1 + len(names)])))
        out.append(need)
    return out


def needs_from_toml(text):
    """`[{id, kind, **fields}]` from the TOML carrier, or None when it does not
    parse. Same absent-vs-empty and None-vs-`{}` rules as the row tiers."""
    try:
        tables = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    out = []
    for rid, cells in (tables.get(NEED_TABLE) or {}).items():
        need = {"id": rid, "kind": "core"}
        need.update({k: value_to_cell(v) for k, v in cells.items()})
        out.append(need)
    return out


def needs_from_text(text):
    """`[{id, kind, **fields}]` for a needs registry given only its TEXT, by
    sniffing which carrier wrote it.

    Exists because the two SN scrapers the gate depends on take TEXT, not a
    path, and are pinned equal across `trace` and `derive_gate`. Under TOML the
    id scrape happens to keep working — `[need.SN-001]` still contains the token
    — but the DRAFT scan does not: it looks for a markdown heading containing
    the word "draft", finds none, and reports zero drafts. Every draft need
    would read as ratified and the derived gate would RISE. That is the failure
    this dispatch exists to make impossible; it is not a convenience."""
    parsed = needs_from_toml(text)
    if parsed is not None and (parsed or NEED_TABLE + "." in text):
        return parsed
    return needs_from_markdown(text)


def load_needs(path):
    """Every stakeholder need, through whichever carrier is live.

    `path` may name either suffix; `resolve` refuses both at once. `[]` when the
    registry is absent, and SystemExit when a carrier exists and cannot be read
    — an unreadable needs registry must not read as "this project has no needs",
    which is a G0 gate and a vacuous orphan check at the same time."""
    live = resolve(path, NEED_CARRIERS)
    if live is None:
        return []
    text = live.read_text(encoding="utf-8-sig", errors="replace")
    if live.suffix == ".md":
        return needs_from_markdown(text)
    needs = needs_from_toml(text)
    if needs is None:
        raise SystemExit(
            "spine_carrier: {} does not parse as TOML — refusing to report an "
            "unreadable needs registry as an empty one".format(live)
        )
    return needs


def folded(need):
    """A need projected onto the CORE four, for a reader that renders one shape.

    This is the PRESENTATION rule the markdown tables forced, kept out of the
    carrier deliberately (repo-lock D-5) — but kept in ONE place, which the
    carrier did not previously manage. `traj_parse._sn_rows` and
    `gen_okf.sn_rows` each carried a copy pinned by nothing but a docstring
    saying "change both together"; they drifted, and the dashboard rendered a
    phantom `SN-000` root (§6 F-6). An edge row reads as: the SCENARIO is the
    need, the LIFECYCLE phase is the why, and the EXPECTED behavior is the
    acceptance — never the lifecycle word as the title."""
    if need.get("kind") != "edge":
        return {k: need.get(k, "") for k in ("id",) + SN_CORE}
    return {
        "id": need["id"],
        "need": need.get("scenario", ""),
        "why": need.get("lifecycle", ""),
        "priority": need.get("priority", "n/a"),
        "acceptance": need.get("expected", ""),
    }


def draft_ids_from_text(text):
    """Draft need ids for a needs registry given only its TEXT, per carrier.

    THE TWO CARRIERS ARE DELIBERATELY NOT UNIFIED HERE, and that is the whole
    care in this function. Under TOML draft-ness is a FIELD, which is what
    retires section-as-state and kills the sharp edge the 2026-08-10 sitting
    hit — a prose MENTION of an id under the draft heading silently re-drafted
    an already-attested need, because the id universe is a whole-text scrape
    while draft-ness was a heading scan. Under MARKDOWN the heading scan is
    reproduced EXACTLY as it always behaved, prose mentions and all.

    Reading legacy text by the new rule would be a silent behaviour change for
    every repo that has not migrated yet: needs that were draft would stop
    being draft, and the derived gate would rise. The ruling retires the sharp
    edge WITH the carrier, not ahead of it, so a file gets the semantics it was
    written under."""
    parsed = needs_from_toml(text)
    if parsed is not None and (parsed or NEED_TABLE + "." in text):
        return draft_need_ids(parsed)
    draft, in_draft = set(), False
    for line in text.splitlines():
        heading = _SN_HEADING.match(line)
        if heading:
            in_draft = "draft" in heading.group(1).lower()
            continue
        if in_draft:
            draft.update(
                u for u in re.findall(r"\bSN-\d+\b", line) if not u.endswith("-000")
            )
    return draft


_SN_EMPHASIS = re.compile(r"\*\*|`")


def folded_needs(path):
    """Every need as the CORE four, `-000` skipped and id-sorted — the shape
    every renderer of the need tier wants.

    THIS COLLAPSES A KNOWN-DRIFTING TRIPLET. `traj_parse._sn_rows`,
    `gen_okf.sn_rows` and `trace._sn_prose` each carried this rule with a
    docstring saying "change all three together"; that is a promise, not a
    mechanism, and they broke it — one kept the `-000` example row and one did
    not, which rendered a phantom `SN-000` root in the dashboard's icicle. It is
    the same argument that put the column vocabulary in one home (D-6): a
    duplicated RULE whose copies disagree does not fail loudly, it renders
    something subtly wrong on a surface a human is expected to trust.

    Markdown emphasis is stripped because these cells are prose written for a
    table and re-rendered somewhere that is not one."""
    out = []
    for need in load_needs(path):
        if str(need.get("id", "")).endswith("-000"):
            continue
        row = folded(need)
        out.append({k: _SN_EMPHASIS.sub("", v).strip() for k, v in row.items()})
    return sorted(out, key=lambda r: r["id"])


def need_ids(needs):
    """Every declared need id — the UNIVERSE the draft set is carved out of."""
    return {n["id"] for n in needs}


def draft_need_ids(needs):
    """The needs still at draft. A FIELD now, not a heading a prose mention can
    fall under."""
    return {n["id"] for n in needs if n.get("kind") == "draft"}
