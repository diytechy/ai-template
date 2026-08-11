#!/usr/bin/env python3
"""Convert the requirement registries from their `.md` + `.csv` carriers to one
TOML carrier (OI-12), losslessly and reversibly.

WHY ONE CARRIER. The spine shipped two: stakeholder needs as markdown prose
tables, SR/LLR/TC as CSV. The split has no recorded rationale anywhere, and it
costs. Reading 32 SN rows takes ~166 code lines across 14 functions in 8
modules; reading all 436 SR+LLR+TC rows takes `csv.DictReader`. TOML is stdlib
at the kit's 3.11 floor (`tomllib`), is already sanctioned in two homes here
(`docs/process.toml`, the `+++` frontmatter of every work-item spec), and holds
the cells that ACTUALLY exist rather than the cells CSV wishes existed: the
comma-bearing cells, the ones holding a literal `|`, the 1,500-character ones,
and the embedded newline CSV cannot represent at all.

WHAT THE CARRIER BUYS THAT A CHECK USED TO. Three integrity rules stop being
code and become properties of the parse:
  * a DUPLICATE ID is a `TOMLDecodeError` — the id is the table key, and TOML
    forbids declaring one twice;
  * a REF LIST is a typed array, retiring the split-on-whitespace rule and with
    it the `SN-001 and SN-002` -> "`and` is an orphan" defect;
  * an EMPTY CELL is an ABSENT KEY, so "unset" and "set to empty" stop being
    the same string.

WHAT THIS DELIBERATELY DOES NOT DO. Carrier only. `Status` keeps today's
vocabulary — `Draft` / `Verified` / `Modified` — because retiring `Modified`
is what the ladder migration does, and doing it here would stamp 38 rows clean
and launder the re-blessing they owe (repo-lock Q11). No anchor cells, no
`Priority` float, no `SupersededBy` deletion, no SN `Status`. Those land once,
on this carrier, in the D-3/D-4 pass.

REVERSIBILITY IS THE POINT OF `--check`. It re-reads what it wrote and asserts
the round-trip is cell-for-cell identical to the source, so a conversion that
silently drops a cell fails here rather than in a gate three commits later.

Contracts: IF-103 — the seam this module declares (process.md §8; row of record
in docs/requirements/interfaces.csv).

Requirements: SR-147 (one machine-parseable carrier for the spine).
"""

import argparse
import csv
import io
import re
import sys
import tomllib
from pathlib import Path

# The id prefix stays in the key (`[requirement.SR-137]`, bare — TOML allows
# `-` in a bare key). It is redundant inside a file already named
# system-requirements.toml, and that redundancy is exactly the point: the
# prefixed token is the join key ~6,400 hand-authored citations use, so the
# registry must remain findable by the same string every commit message,
# log entry and archived document cites.
SPINE = {
    "docs/requirements/system-requirements.csv": ("requirement", "SR-ID"),
    "docs/requirements/low-level-requirements.csv": ("design", "LLR-ID"),
    "docs/test/test-cases.csv": ("test", "TC-ID"),
}

# Cells that are REFERENCE LISTS become typed arrays. Everything else stays a
# string: this is a carrier change, not a schema change.
#
# `TestRefs` is DELIBERATELY NOT HERE, and it was until the cutover measured it.
# The column's conventional value is `(see TC-017)` — a prose pointer, which
# check_doc_refs names as such where it declines to read a path out of it — and
# only one row of 141 holds a bare id list. Splitting prose on whitespace made
# `test_refs = ["(see", "TC-017)"]`, which re-joins as `(see; TC-017)`: a
# TEXT CHANGE to 140 design rows, smuggled into a carrier-only migration, and
# the very defect the typed array exists to retire (`SN-001 and SN-002` ->
# "`and` is an orphan") committed in the other direction. As a plain string
# every shape round-trips byte-exact and every consumer keeps the split rule it
# already applied to this cell under CSV.
REF_COLS = {"SN-Refs", "SR-Refs", "Verifies", "SupersededBy"}
INT_COLS = {"Phase"}

# column -> TOML key. EXPLICIT, never derived: a derivation turns `SR-ID` into
# `s_r_i_d`, and the column name is a repo-wide term (D-3) that deserves a
# stated mapping rather than a regex nobody can predict.
KEY = {
    "Title": "title",
    "SN-Refs": "sn_refs",
    "SR-Refs": "sr_refs",
    "Verifies": "verifies",
    "Requirement": "requirement",
    "Rationale": "rationale",
    "AcceptanceCriteria": "acceptance_criteria",
    "Permutations": "permutations",
    "Priority": "priority",
    "Verification": "verification",
    "Status": "status",
    "Phase": "phase",
    "Area": "area",
    "SupersededBy": "superseded_by",
    "Lifecycle": "lifecycle",
    "Detail": "detail",
    "Module": "module",
    "CodeSymbol": "code_symbol",
    "TestRefs": "test_refs",
    "Level": "level",
    "Method": "method",
    "Expected": "expected",
    "Parameters": "parameters",
    "Automated": "automated",
    "Evidence": "evidence",
    "Tier": "tier",
    "Component": "component",
    "Notes": "notes",
}


def toml_scalar(value):
    """A Python str/int/list as a TOML value.

    Multi-line basic strings for anything long or newline-bearing, which is
    what makes the prose cells representable at all. `tomllib` is read-only by
    design (PEP 680 omitted a writer), so the kit emits its own — as it already
    does twice, in `wi_convert.toml_string` and `bootstrap.set_process_key`.
    """
    if isinstance(value, list):
        return "[" + ", ".join(toml_scalar(v) for v in value) + "]"
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    text = str(value)
    if "\n" in text or len(text) > 88:
        body = text.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
        # A value ending in `"` would glue to the closing delimiter.
        if body.endswith('"'):
            body = body[:-1] + '\\"'
        return '"""' + body + '"""'
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def cell_to_value(col, raw):
    """One CSV cell as the value its column means. Empty -> None (key omitted).

    A plain cell is carried VERBATIM, not stripped. Stripping looks harmless and
    is not: the conversion advertises "cell for cell", and a cell whose leading
    or trailing whitespace is content — an indented code fragment, a padded
    fixed-width note — silently lost it. Worse, the loss detector stripped BOTH
    sides, so it compared the converter's output against the converter's own
    reading and reported `findings=[]` on a real change. `.strip()` survives
    only where it decides EMPTINESS (a whitespace-only cell is an empty cell,
    which is an absent key), and in the ref/int parses where the surrounding
    whitespace is separator syntax rather than content."""
    text = (raw or "").strip()
    if not text:
        return None
    if col in REF_COLS:
        return [t for t in re.split(r"[;,\s]+", text) if t]
    if col in INT_COLS:
        try:
            return int(text)
        except ValueError:
            return text  # a non-integer Phase is data to preserve, not to crash on
    return raw


def rows_to_toml(table, id_col, rows, header):
    """The whole registry as TOML text, source order preserved."""
    out = io.StringIO()
    for row in rows:
        rid = (row.get(id_col) or "").strip()
        if not rid:
            continue
        out.write("[{}.{}]\n".format(table, rid))
        for col in header:
            if col == id_col:
                continue
            value = cell_to_value(col, row.get(col))
            if value is None:
                continue
            out.write("{} = {}\n".format(KEY.get(col, col), toml_scalar(value)))
        out.write("\n")
    return out.getvalue()


def value_to_cell(col, value):
    """The inverse of `cell_to_value`, for the round-trip check.

    A ref array re-joins on `;` — the separator the registry ACTUALLY USES, not
    a prettier one. Measured over this repo's own spine at the cutover: 271 of
    271 multi-ref cells wrote `A;B`, none wrote `A; B`. Joining on `"; "`
    therefore rewrote every one of them, which put ~40 spurious "cell changed"
    entries into the re-attestation brief the owner is about to work — the
    carrier migration manufacturing amendments in the one view that must show
    only real ones. The separator is not the meaning (`_cells_differ` compares
    token lists either way), which is exactly why the conversion has no licence
    to change it."""
    if value is None:
        return ""
    if isinstance(value, list):
        return ";".join(value)
    return str(value)


REF_KEYS = {KEY[c] for c in REF_COLS}


def _cells_differ(key, before, after):
    """Did this cell survive? Ref cells compare on the TOKEN LIST, because the
    conversion re-joins them with the canonical separator and the original
    spacing is not part of the meaning."""
    if key in REF_KEYS:
        split = lambda t: [x for x in re.split(r"[;,\s]+", t) if x]  # noqa: E731
        return split(before) != split(after)
    return before != after


# Every markdown line that IS a need row, read off the RAW source with no
# reference to how `read_sn` chose to interpret it. `^| SN-### |` is the shape
# the tier has always used, and it is the one thing about the legacy carrier
# that can be asserted without re-implementing the reader.
_RAW_SN_ROW = re.compile(r"^\|\s*(SN-\d+)\s*\|", re.MULTILINE)


def raw_need_findings(rel, raw, text):
    """Findings for any need present in the RAW markdown and absent from the
    emitted TOML — the oracle `compare` cannot be, because `compare` is handed
    the reader's output as its expectation.

    THIS IS THE SECOND, INDEPENDENT LEG. The self-oracle answers "did every cell
    the reader saw survive"; it is silent by construction about a row the reader
    never saw. A heading it did not recognise used to make a whole table
    invisible and still report `findings=[]` — a converter certifying its own
    blind spot. An adopter with locally edited registries is exactly who runs
    this, and they have no other way to find out."""
    try:
        got = tomllib.loads(text).get("need", {})
    except tomllib.TOMLDecodeError:
        return []  # `compare` reports the decode error; one finding is enough
    missing = sorted({rid for rid in _RAW_SN_ROW.findall(raw)} - set(got))
    return [
        "{}: {} is a need row in the source and is absent from the conversion "
        "— the reader did not recognise it (an unfamiliar heading?), so the "
        "round-trip check never saw it either".format(rel, rid)
        for rid in missing
    ]


def compare(rel, table, expected, text):
    """Findings for one converted registry. `expected` is {id: {key: text}} —
    built from CSV columns or from markdown cells, so ONE comparison serves
    both carriers instead of a second copy that drifts from the first."""
    try:
        got = tomllib.loads(text).get(table, {})
    except tomllib.TOMLDecodeError as exc:
        return ["{}: emitted TOML does not parse — {}".format(rel, exc)]
    findings = []
    if len(got) != len(expected):
        findings.append(
            "{}: {} rows in, {} tables out".format(rel, len(expected), len(got))
        )
    for rid, cells in expected.items():
        if rid not in got:
            findings.append("{}: {} missing after conversion".format(rel, rid))
            continue
        for key, before in cells.items():
            after = value_to_cell(key, got[rid].get(key))
            if _cells_differ(key, before, after):
                findings.append(
                    "{} {}.{}: {!r} -> {!r}".format(
                        rel, rid, key, before[:60], after[:60]
                    )
                )
    return findings


# --- the SN tier: markdown prose tables, three shapes -------------------------
# The edge-case table has its OWN columns (Lifecycle | Scenario | Expected), and
# they are kept as themselves here rather than folded onto the core four. The
# fold that traj_parse._sn_fields performs is a PRESENTATION rule for the
# exports — an edge row's Scenario reads as the need, its Lifecycle as the why —
# and presentation belongs in the exporter, not baked into the carrier. TOML can
# hold both shapes; the markdown table could not, which is why the fold existed.
SN_REL = "docs/requirements/stakeholder-needs.md"
SN_CORE = ("need", "why", "priority", "acceptance")
SN_EDGE = ("lifecycle", "scenario", "expected")


def read_sn(path):
    """[(id, kind, {field: text})] in document order.

    A ROW IS NEVER DROPPED FOR ITS HEADING. `kind` comes from the heading when
    the heading is one this reader knows, and from the table's SHAPE when it is
    not — the same fallback `spine_carrier.needs_from_markdown` applies, for a
    sharper reason on this side: a heading the vocabulary does not recognise
    ("## Miscellaneous", "## Deferred") used to make every need under it
    invisible, and because the loss oracle was built from THIS function's
    output, a whole table could vanish with `findings=[]`. An unrecognised
    heading is a naming choice; it is not a statement that the rows below are
    not needs (repo-lock D-5; the review's B2).

    Cells are stripped here and that is correct: the padding around `|` is the
    markdown table's SYNTAX, not content — unlike a CSV cell, where whitespace
    inside the quotes is data."""
    kind, out = None, []
    for line in path.read_text(encoding="utf-8").split("\n"):
        heading = re.match(r"^#{2,}\s+(.*)$", line)
        if heading:
            title = heading.group(1).lower()
            kind = (
                "draft"
                if "draft" in title
                else "edge"
                if "edge" in title
                else "core"
                if "core" in title or "need" in title
                else None
            )
            continue
        row = re.match(r"^\|\s*(SN-\d+)\s*\|", line)
        if not row:
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        # No heading, or one this reader does not name: resolve by the table's
        # width, exactly as the live reader does — the edge table is three cells
        # wide beside its id, the core table four.
        row_kind = kind or ("edge" if len(cells) - 1 == len(SN_EDGE) else "core")
        names = SN_EDGE if row_kind == "edge" else SN_CORE
        out.append((cells[0], row_kind, dict(zip(names, cells[1 : 1 + len(names)]))))
    return out


def sn_to_toml(needs):
    out = io.StringIO()
    for rid, kind, fields in needs:
        out.write("[need.{}]\n".format(rid))
        out.write('kind = "{}"\n'.format(kind))
        for name in SN_EDGE if kind == "edge" else SN_CORE:
            text = (fields.get(name) or "").strip()
            if text:
                out.write("{} = {}\n".format(name, toml_scalar(text)))
        out.write("\n")
    return out.getvalue()


def _emit(root, src, text, count, noun, write, written):
    """Write one converted registry beside its source and report it.

    Shared by both carriers rather than repeated per branch: the tail is
    identical, so a change to the report line cannot land in one branch only."""
    dest = src.with_suffix(".toml")
    if write:
        dest.write_text(text, encoding="utf-8", newline="\n")
        written.append(dest)
    print(
        "migrate_carrier: {} -> {} ({} {}, {} bytes)".format(
            src.relative_to(root).as_posix(),
            dest.relative_to(root).as_posix(),
            count,
            noun,
            len(text),
        )
    )
    return dest


def convert(root, write):
    """Convert every spine registry. Returns (findings, written_paths)."""
    findings, written = [], []
    sn_src = root / SN_REL
    if sn_src.is_file():
        raw = sn_src.read_text(encoding="utf-8")
        needs = read_sn(sn_src)
        text = sn_to_toml(needs)
        expected = {
            rid: dict(
                {"kind": kind}, **{k: v.strip() for k, v in f.items() if v.strip()}
            )
            for rid, kind, f in needs
        }
        findings += raw_need_findings(SN_REL, raw, text)
        findings += compare(SN_REL, "need", expected, text)
        _emit(root, sn_src, text, len(needs), "needs", write, written)
    for rel, (table, id_col) in sorted(SPINE.items()):
        src = root / rel
        if not src.is_file():
            continue
        with src.open(newline="", encoding="utf-8-sig", errors="replace") as fh:
            reader = csv.DictReader(fh)
            header = list(reader.fieldnames or [])
            rows = [r for r in reader if (r.get(id_col) or "").strip()]
        text = rows_to_toml(table, id_col, rows, header)
        # THE ORACLE READS THE RAW SOURCE, never the converter's own parse.
        # The cell text here is exactly what `csv` handed back — unstripped, so
        # a conversion that trimmed content is a FINDING rather than a match
        # against its own trimming. An oracle built from the thing under test
        # cannot fail, and this one did not (repo-lock D-5; the review's B2).
        expected = {
            (r.get(id_col) or "").strip(): {
                KEY.get(c, c): (r.get(c) or "")
                for c in header
                if c != id_col and (r.get(c) or "").strip()
            }
            for r in rows
        }
        findings += compare(rel, table, expected, text)
        _emit(root, src, text, len(rows), "rows", write, written)
    return findings, written


def main(argv=None):
    ap = argparse.ArgumentParser(description="CSV/markdown registries -> TOML (OI-12)")
    ap.add_argument("--root", default=".")
    ap.add_argument(
        "--check",
        action="store_true",
        help="convert in memory and verify the round-trip; write nothing",
    )
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    findings, _ = convert(root, write=not args.check)
    for f in findings:
        print("migrate_carrier: LOSSY - {}".format(f), file=sys.stderr)
    if findings:
        print(
            "migrate_carrier: REFUSED - {} cell(s) did not survive the "
            "round-trip".format(len(findings)),
            file=sys.stderr,
        )
        return 1
    print("migrate_carrier: round-trip clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
