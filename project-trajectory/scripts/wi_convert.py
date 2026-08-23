#!/usr/bin/env python3
"""Convert the work-item registry between its CSV row form and its spec-file form.

Stack-agnostic, standard-library only. This is the mechanical, provable half of
"specs are the registry" (docs/concurrency-restructure.md §2): the converter
plus the proof that the conversion loses nothing, because the design's own rule
is that *the converter is proven by a round-trip before the CSV is demoted* (the
140-cell lesson: you do not flip an authoritative registry on a conversion you
have not measured).

Written at Phase 2a as meta-repo tooling, it became a **kit script** at Phase
2c-i — the phase that ships the folder registry downstream (`bootstrap.py`
scaffolds `docs/work/{draft,queued,active,deferred,cancelled,complete}/` and the
`WI-000` example spec, and `plan_artifacts.py` imports this module as a sibling
to file a new work item as a spec file). Running it is still the adopter's
choice: it converts BETWEEN the two forms and never decides what the registry
is — the folder is the one live home (Phase 5, RULING-4); the CSV form survives
here as the legacy interchange format (migrate in, export for inspection).

The spec-file form, per §2.1/§2.2:

    docs/work/draft/WI-362-still-thinking.md   # written down, not claimable
    docs/work/queued/WI-360-forge-seam.md      # filed, unclaimed
    docs/work/deferred/WI-361-something.md     # filed, not now
    docs/work/complete/WI-359-done-thing.md    # shipped
    docs/work/cancelled/WI-358-wont-build.md   # will never ship, reason in body

**Status is location, and location is the WHOLE statement.** It is deliberately
NOT a frontmatter key: one home per fact, and a move between two distinct paths
is what makes two branches claiming the same work item a visible git move/move
conflict instead of a silent overwrite. WI-384 finished the job by giving the
two terminals their own directories: `archive/` used to hold both, so a
`disposition = "retired"` key and a validator kept folder and attribute honest —
splitting the folder deleted the key, the validator and both of its raise paths.
The status↔directory map is now a BIJECTION; ANY other status value is a refusal
naming the row, never a catch-all bucket — a classifier that can always finish is
a classifier that has stopped classifying.

**Frontmatter is TOML between `+++` lines** (the Hugo delimiter), read back with
stdlib `tomllib` (3.11+, so no dependency is incurred — RULING-3). `tomllib` is
read-ONLY, so the emitter below is a small hand-rolled serializer. It writes
basic strings with backslash, double-quote and control characters escaped, which
is the whole of what TOML needs to round-trip an arbitrary one-line value.

**The long `Deliverable` cell goes in the BODY**, under a `## Deliverable`
heading, verbatim. That is not a layout preference: a Deliverable may contain
newlines, quotes, backticks and markdown, and body text needs no escaping at
all, so the one cell most likely to break an escaper is the one cell that never
passes through it.

**`order` is a migration artifact, and says so.** The live CSV is NOT id-sorted
(three rows sit out of numeric order), so id order cannot reconstruct the file;
rather than silently reorder an authoritative registry the emitter carries the
row's index explicitly. When the CSV is deleted the key becomes meaningless and
goes with it.

Self-verification is not optional here. `--to-specs` re-reads and re-parses
EVERY file it writes and compares against the source row before moving on, so a
conversion defect surfaces at the row that caused it. `--verify` then runs the
whole registry through CSV -> specs -> CSV in a temp directory and compares
cell-exact; byte identity is REPORTED, never asserted, because CSV quoting style
is a property of the writer, not of the data.

Usage:
    python scripts/wi_convert.py --to-specs --csv docs/requirements/work-items.csv \\
        --work docs/work [--force]
    python scripts/wi_convert.py --to-csv --work docs/work --csv out/work-items.csv
    python scripts/wi_convert.py --verify --csv docs/requirements/work-items.csv

Small CLI/console helpers below are duplicated from the sibling scripts per the
kit's independently-copyable-script convention (the F5 rule) — this module stays
a self-contained drop-in, never importing a shared kit module.

Contracts: IF-079 — the interface seam this module declares (process.md §8; rows of record in docs/requirements/interfaces.toml).
"""

import argparse
import csv
import re
import sys
import tempfile
import tomllib
from pathlib import Path

# The console guard's one home is the shipped package (WI-448 / D-8);
# aliased to the module-local name so no call site changes.
from kitlib.config import utf8_console as _utf8_console

# The spec-folder reader's one home (D-8/OI-16): this module owns the WRITE side
# of the same rule and re-exports the read side rather than restating it.
from kitlib import registry as _kitregistry

# The registry's column order, which IS the schema (docs/requirements/
# work-items.csv; pinned against the shipped template by test_dogfood_sync).
# Reconstructing this header exactly is half of what "lossless" means.
COLUMNS = [
    "WI-ID",
    "Title",
    "Workstream",
    "SR-Refs",
    "Predecessors",
    "Status",
    "Deliverable",
    "SpecRef",
    "BuildTier",
    "CritiqueBudget",
    "CritiqueExhaustion",
    "Priority",
    "Exclusive",
    "BlockRef",
    "EstTokens",
    "SafetyClass",
    "PlanMode",
    "Bar",
    # LLR-161 LINEAGE. Partial work continues by MINTING A SUCCESSOR, never by
    # reviving the closed row — so the successor must be able to say which row
    # it continues, or the thread is lost at the id change. A real column, not
    # a frontmatter-only key, because `intake`'s drafts-not-mints arm writes
    # successors through `wi_convert.write_spec_file`, which serializes from
    # this table: a key that is not here would be silently dropped at the one
    # moment it matters.
    "Supersedes",
    # SN-032 BRIEF ROUTING. Which adjudicator brief this row's session is sent
    # (`amendment` | `disposition` | `conflict` | `red-tc`), empty on every row
    # that is not an adjudication. DECLARED rather than inferred from `SpecRef`
    # because the inference is provably ambiguous: an amendment to a test-case
    # row and a red-TC census row both carry `docs/test/test-cases.toml`, and
    # those two briefs give contradictory instructions. A real column for the
    # same reason `Supersedes` is one — `intake` writes it through
    # `write_spec_file`, which serializes from this table.
    "Brief",
]

# Status <-> directory (§2.1; WI-384). One directory per state, both terminals
# included, so the map INVERTS — there is no second fact to keep honest.
# Cancellation is still a MOVE with a recorded reason, never a deletion; the
# reason lives where it always did, in the Deliverable body.
STATUS_DIRS = {
    "draft": "draft",
    "queued": "queued",
    "deferred": "deferred",
    "done": "complete",
    "cancelled": "cancelled",
    # SR-144's third terminal: a lane that stopped early. Terminal, so nothing
    # re-claims it and nothing strands; the per-close report under
    # docs/handbacks/ carries what was and was not delivered.
    "partial": "partial",
}
# The inverse, built from the one table so the two directions cannot disagree.
DIR_STATUSES = {directory: status for status, directory in STATUS_DIRS.items()}

# Columns carried verbatim as single-valued frontmatter keys.
SCALAR_FIELDS = (
    ("Title", "title"),
    ("Workstream", "workstream"),
    ("SpecRef", "specref"),
    ("BuildTier", "buildtier"),
    ("CritiqueBudget", "critique_budget"),
    ("CritiqueExhaustion", "critique_exhaustion"),
    ("Exclusive", "exclusive"),
    ("BlockRef", "blockref"),
    ("EstTokens", "est_tokens"),
    ("SafetyClass", "safety_class"),
    ("PlanMode", "planmode"),
    # WI-388: bar declares verification strictness for this row's lane; it
    # never affects scheduling. (DevStg-Reqs|DevStg-Tests|DevStg-Impl — integrate.refresh passes it to
    # check.py --gate; the scheduler deliberately does not parse it.)
    ("Bar", "bar"),
    ("Supersedes", "supersedes"),
    ("Brief", "brief"),
)
# Columns carried as TOML arrays. Split on ';' WITHOUT stripping, so ';'.join()
# is an exact inverse for every possible cell — including the `~WI-013` SOFT
# dependency prefix, which is preserved verbatim because it is meaning
# (schedule.py's hard/soft predecessor split reads it), not decoration.
LIST_FIELDS = (
    ("SR-Refs", "sr_refs"),
    ("Predecessors", "needs"),
)
# Columns emitted as TOML integers when — and only when — the round-trip is
# exact (`str(int(cell)) == cell`). A cell like `01` stays a string rather than
# quietly becoming `1`.
INT_FIELDS = (("Priority", "priority"),)
# Column -> frontmatter-key lookups, built once from the three tables above so
# the tables stay the readable declaration and nothing rebuilds them per row.
_SCALAR_KEYS = dict(SCALAR_FIELDS)
_LIST_KEYS = dict(LIST_FIELDS)
_INT_KEYS = dict(INT_FIELDS)

SEP = ";"
FENCE = "+++"
DELIVERABLE_PREFIX = "\n## Deliverable\n\n"
# The body's OTHER section (WI-387): a returned WI carries a `## Handback` note
# after the Deliverable's place. It maps to no CSV column, so this converter
# READS past it and does not reproduce it — `--to-csv` on a folder holding a
# returned spec must not refuse, and `--to-specs` starts from a CSV that never
# had one. (`--verify` round-trips CSV -> specs -> CSV, so it never sees one.)
HANDBACK_PREFIX = "\n## Handback\n"
# The body's THIRD section (WI-388): the advisory `## Context` block the intake
# mint writes into every minted row (pure registry joins). It maps to no CSV
# column, so this converter READS past it exactly like the Handback note —
# `--to-csv` must not refuse a minted spec, and `--to-specs` starts from a CSV
# that never had one.
CONTEXT_PREFIX = "\n## Context\n"
# Slug source width: enough of a title to be recognizable in a directory
# listing, short enough to keep paths sane. This slug becomes a git branch
# name (dispatch._branch_for) that a lane worktree checks out INSIDE the
# worktree's own path, then repeats inside `docs/work/active/<branch>/` and
# again in the spec's own filename — three copies of it stack into one path.
# Measured 2026-08-15 (WI-462, one Windows dev box, `C:\Projects\...`-depth
# temp roots): a 40-char slug left a census-minted branch at 259/260 chars
# under pytest-xdist's extra `popen-gwN/` nesting, and `git worktree add`
# failed with "Filename too long". Trimmed to 30 for real margin (~30+ chars
# spare at that same depth) — this is one machine's default-Windows-config
# arithmetic, not a universal MAX_PATH proof; a repo with `core.longpaths`
# or a shallower temp root may never feel this, and one nested deeper still
# could. If it recurs, the fix is either a shorter cap still or documenting
# long-path support as a precondition — not disabling the tests it trips.
SLUG_CHARS = 30


class ConvertError(Exception):
    """A refusal: the input cannot be converted without inventing something."""


# --- the TOML emitter (tomllib is read-only) ---------------------------------
# Escapes exactly what TOML basic strings require: the backslash, the closing
# quote, and every control character. The named shorthands are used where TOML
# defines them and \uXXXX covers the rest, so nothing is left to the parser's
# discretion. Verified by re-parsing every emitted file with tomllib.
_TOML_ESCAPES = {
    "\\": "\\\\",
    '"': '\\"',
    "\b": "\\b",
    "\t": "\\t",
    "\n": "\\n",
    "\f": "\\f",
    "\r": "\\r",
}


def toml_string(value):
    """`value` as a TOML basic string, escaped so tomllib reads it back exactly."""
    out = ['"']
    for ch in value:
        escaped = _TOML_ESCAPES.get(ch)
        if escaped is not None:
            out.append(escaped)
        elif ord(ch) < 0x20 or ord(ch) == 0x7F:
            out.append("\\u{:04x}".format(ord(ch)))
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def toml_value(value):
    """`value` as TOML: int, array of basic strings, or basic string."""
    if isinstance(value, bool):  # guard: bool is an int subclass in Python
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(toml_string(v) for v in value) + "]"
    return toml_string(value)


def render_frontmatter(pairs):
    """`key = value` lines for an ordered `(key, value)` sequence."""
    return "".join("{} = {}\n".format(k, toml_value(v)) for k, v in pairs)


# --- CSV row <-> spec file ---------------------------------------------------
def slugify(title):
    """The filename slug: lowercase kebab of the title's first SLUG_CHARS
    characters, `[a-z0-9-]` only, no leading/trailing hyphen. Purely
    cosmetic — the id in front of it is what identifies the file — so a
    title that slugs to nothing falls back to `wi`, rather than producing
    `WI-360-.md`."""
    slug = re.sub(r"[^a-z0-9]+", "-", (title or "").lower()[:SLUG_CHARS]).strip("-")
    return slug or "wi"


def spec_filename(row):
    return "{}-{}.md".format(row["WI-ID"], slugify(row.get("Title")))


def status_dir(row):
    """The directory a row's Status maps to — or a refusal naming the row.

    No catch-all. An unrecognized status is a real question (is it a typo? a new
    lifecycle state that needs a directory and a rule?) and answering it by
    dropping the row into `queued/` would silently reclassify work.
    """
    status = (row.get("Status") or "").strip()
    directory = STATUS_DIRS.get(status)
    if directory is None:
        raise ConvertError(
            "{}: status {!r} has no directory — the spec form encodes status as "
            "LOCATION and knows only {}. Give it a directory and a rule, or fix "
            "the row; it will not be filed under a catch-all.".format(
                row.get("WI-ID") or "(row with no WI-ID)",
                status,
                ", ".join(sorted(STATUS_DIRS)),
            )
        )
    return directory


def frontmatter_pairs(row, order):
    """The ordered frontmatter of one registry row. Empty cells are OMITTED —
    absent and empty mean the same thing in this registry, and writing a wall of
    `= ""` would bury the fields that carry information.

    `order=None` omits the key entirely, which is what a spec FILED DIRECTLY into
    the folder gets: `order` exists only to reproduce a CSV whose row order the
    ids do not describe, so writing one for a spec that never came from a CSV
    would invent a migration artifact for a file that has no migration."""
    pairs = [("id", row["WI-ID"])]
    for column in COLUMNS:
        pair = _column_pair(column, row.get(column) or "")
        if pair is not None:
            pairs.append(pair)
    if order is not None:
        pairs.append(("order", order))
    return pairs


def _column_pair(column, cell):
    """The one frontmatter `(key, value)` a registry column contributes, or None
    when it contributes nothing.

    `Title` is the exception that is written even when empty: an untitled work
    item is a defect worth seeing in the file rather than an omission a reader
    has to infer. Columns in no table (`WI-ID`, `Status`, `Deliverable`) are
    carried elsewhere — the id by the caller, the status by the DIRECTORY, the
    Deliverable by the body — so they contribute nothing here by design.
    """
    if column == "Title":
        return ("title", cell)
    if not cell:
        return None
    if column in _LIST_KEYS:
        return (_LIST_KEYS[column], cell.split(SEP))
    if column in _INT_KEYS:
        return (_INT_KEYS[column], _int_or_text(cell))
    if column in _SCALAR_KEYS:
        return (_SCALAR_KEYS[column], cell)
    return None


def _int_or_text(cell):
    """`cell` as an int when that is exactly reversible, else the raw text."""
    try:
        number = int(cell)
    except ValueError:
        return cell
    return number if str(number) == cell else cell


def render_spec(row, order=None):
    """`(relative_path, text)` for one registry row."""
    text = FENCE + "\n" + render_frontmatter(frontmatter_pairs(row, order))
    text += FENCE + "\n"
    deliverable = row.get("Deliverable") or ""
    if deliverable:
        text += DELIVERABLE_PREFIX + deliverable + "\n"
    return "{}/{}".format(status_dir(row), spec_filename(row)), text


def split_spec(text, where):
    """`(frontmatter_text, body_text)` from a spec file's raw text.

    Split on bare `\\n` because the caller reads with `newline=""` (no universal
    -newline translation): a `\\r` that was genuinely IN the data survives to be
    compared, instead of being silently rewritten on the way in.
    """
    lines = text.split("\n")
    if not lines or lines[0] != FENCE:
        raise ConvertError(
            "{}: does not start with a {} frontmatter fence".format(where, FENCE)
        )
    try:
        close = lines.index(FENCE, 1)
    except ValueError:
        raise ConvertError(
            "{}: frontmatter fence is never closed".format(where)
        ) from None
    return "\n".join(lines[1:close]) + "\n", "\n".join(lines[close + 1 :])


def parse_deliverable(body, where):
    """The verbatim Deliverable cell from a spec body (empty when absent).
    The `## Handback` and `## Context` sections are read past, not carried —
    neither maps to a CSV column."""
    if body == "":
        return ""
    body = body.partition(HANDBACK_PREFIX)[0]
    body = body.partition(CONTEXT_PREFIX)[0]
    if body == "":
        return ""
    if not body.startswith(DELIVERABLE_PREFIX) or not body.endswith("\n"):
        raise ConvertError(
            "{}: body is neither empty nor a single `## Deliverable` "
            "section — this converter owns the whole body shape".format(where)
        )
    return body[len(DELIVERABLE_PREFIX) : -1]


def status_from_location(directory, where):
    """The Status a spec's location encodes — the inverse of `status_dir`.

    A plain table lookup since WI-384: one directory per state means the
    location IS the status, with nothing in the frontmatter to cross-check it
    against and so no way for the two to disagree. The only refusal left is a
    directory nobody declared.
    """
    status = DIR_STATUSES.get(directory)
    if status is None:
        raise ConvertError(
            "{}: directory {!r} is not a status — the spec form knows only {}".format(
                where, directory, ", ".join(sorted(DIR_STATUSES))
            )
        )
    return status


def parse_spec(text, relpath, where=None):
    """`(row, order)` reconstructed from one spec file.

    `relpath` supplies the Status, and supplies the whole of it: location is the
    state, with no frontmatter key duplicating it (WI-384).
    """
    where = where or relpath
    frontmatter, body = split_spec(text, where)
    try:
        data = tomllib.loads(frontmatter)
    except tomllib.TOMLDecodeError as exc:
        raise ConvertError(
            "{}: frontmatter is not valid TOML — {}".format(where, exc)
        ) from None

    row = {column: "" for column in COLUMNS}
    row["WI-ID"] = _text(data.get("id"), "id", where)
    # Status is the FIRST path component (the loaders' rule — active/<branch>/
    # sits one level deeper, so the parent dir is the branch, not the status).
    # An in-flight claim is not convertible content: a conversion is a
    # drained-stop operation (concurrency-restructure §3.2) — the branch either
    # integrates or parks first. Refused BY NAME, never coerced.
    parts = Path(relpath).parts
    top = parts[0] if len(parts) > 1 else ""
    if top == "active":
        raise ConvertError(
            "{}: an in-flight claim (active/{}) — conversion is a drained-stop "
            "operation (concurrency-restructure §3.2): integrate or park the "
            "branch, then convert".format(where, parts[1] if len(parts) > 2 else "?")
        )
    row["Status"] = status_from_location(top, where)
    row["Deliverable"] = parse_deliverable(body, where)
    for column, key in SCALAR_FIELDS:
        if key in data:
            row[column] = _text(data[key], key, where)
    for column, key in LIST_FIELDS:
        if key in data:
            row[column] = SEP.join(_text(v, key, where) for v in data[key])
    for column, key in INT_FIELDS:
        if key in data:
            value = data[key]
            row[column] = (
                str(value) if isinstance(value, int) else _text(value, key, where)
            )
    order = data.get("order")
    return row, order if isinstance(order, int) else None


def _text(value, key, where):
    if not isinstance(value, str):
        raise ConvertError(
            "{}: `{}` must be a string, got {!r}".format(where, key, value)
        )
    return value


# --- the two homes: which one a WRITER must file into -------------------------
# The READERS resolve this for themselves (`schedule.spec_registry_dir` and its
# two F5 copies); this is the same rule stated for the write side, where the
# converter is the module that already owns "what a spec file is". A writer that
# guessed differently from the readers would file work into the home nobody is
# reading, which is the one migration failure with no visible symptom.


# The `docs/work` folder that pairs with the registry CSV at `csv_path`, and
# every `<status>/WI-*.md` spec under it (sorted; `[]` when the folder is absent
# or holds none — a file sitting DIRECTLY in `work_dir` has no status directory
# above it, so it is deliberately not a spec).
#
# ONE HOME since WI-448 slice 4: `kitlib/registry.py` IS the spec-folder
# reader, and these two were the READ side of the same rule stated a second
# time for the write side. The re-export keeps this module's names, so the
# writer still declares the rule it files under — it just no longer restates
# it. NOT folded: `registry.spec_roots`/`read_spec_rows`' both-roots union
# (WI-504), which is a READER concern; a WRITER files into the active
# workspace, never into the archive.
work_dir_for = _kitregistry.spec_work_dir
spec_paths = _kitregistry.spec_files


# --- file-level operations ---------------------------------------------------
def load_csv(path):
    """The registry's rows, header-preserving. Refuses a header that is not the
    declared 18-column schema — a converter that guesses at an unknown shape is
    how a column gets dropped."""
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []
        if header != COLUMNS:
            raise ConvertError(
                "{}: header is not the declared work-item schema.\n"
                "  expected: {}\n  found:    {}".format(path, COLUMNS, header)
            )
        return [dict(row) for row in reader]


def write_csv(path, rows):
    """Write `rows` back as the 18-column registry: QUOTE_MINIMAL, LF."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        writer = csv.writer(handle, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        writer.writerow(COLUMNS)
        for row in rows:
            writer.writerow([row.get(column) or "" for column in COLUMNS])


def to_specs(csv_path, work_dir, force=False):
    """Write one spec file per CSV row under `work_dir`. Returns the relative
    paths written, in row order.

    Refuses a non-empty target unless `force`: materializing a registry twice
    into the same tree is how you end up with two files for one work item and no
    way to tell which one git should believe.
    """
    work_dir = Path(work_dir)
    if work_dir.exists() and any(work_dir.iterdir()) and not force:
        raise ConvertError(
            "{} is not empty — refusing to materialize the registry on top of "
            "existing work specs. Pass --force if that is really what you "
            "want.".format(work_dir)
        )
    rows = load_csv(csv_path)
    written = [write_spec_file(work_dir, row, order) for order, row in enumerate(rows)]
    duplicates = {p for p in written if written.count(p) > 1}
    if duplicates:
        raise ConvertError(
            "two rows produced the same spec path: {}".format(
                ", ".join(sorted(duplicates))
            )
        )
    return written


def write_spec_file(work_dir, row, order=None):
    """Write one registry row as a spec file under `work_dir`; return its
    relative path. The single writer of the format — `to_specs` (bulk migration)
    and `plan_artifacts` (filing one new work item) both go through it, so a
    spec cannot be produced by a path that skips the self-verification below.
    Written LF on every platform: a generated artifact's line endings are not
    the author's operating system's business (WI-348)."""
    relpath, text = render_spec(row, order)
    target = Path(work_dir) / relpath
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")
    _self_verify(target, relpath, row, order)
    return relpath


def _self_verify(target, relpath, row, order):
    """Re-read what was just written and prove it reconstructs the source row.

    A converter that only writes is a converter whose defects are found later,
    by whoever trusted it. Reading each file back at the moment it is produced
    puts the failure on the row that caused it.
    """
    text = target.open(encoding="utf-8", newline="").read()
    back, back_order = parse_spec(text, relpath, where=str(target))
    mismatches = [
        "{}: {!r} -> {!r}".format(column, row.get(column) or "", back.get(column) or "")
        for column in COLUMNS
        if (row.get(column) or "") != (back.get(column) or "")
    ]
    if back_order != order:
        mismatches.append("order: {!r} -> {!r}".format(order, back_order))
    if mismatches:
        raise ConvertError(
            "{}: does not read back as its source row — {}".format(
                target, "; ".join(mismatches)
            )
        )


def read_specs(work_dir):
    """`[(row, order, relpath)]` for every `*.md` under `work_dir`, sorted into
    registry order: by the explicit `order` key, then by numeric id.

    A spec with no `order` (hand-filed after the conversion) sorts after every
    numbered one, by id — deterministic, and honest that the key exists only to
    reproduce a file whose row order the ids do not describe.
    """
    work_dir = Path(work_dir)
    if not work_dir.is_dir():
        raise ConvertError("{}: no such work directory".format(work_dir))
    parsed = []
    for path in sorted(work_dir.rglob("*.md")):
        if path.parent == work_dir:
            # Status is the directory, so a file at the folder root (the
            # registry's own README) is not a row — same exclusion spec_files()
            # applies. Inside a status directory, strictness stands: every *.md
            # there must parse as a spec.
            continue
        relpath = path.relative_to(work_dir).as_posix()
        row, order = parse_spec(
            path.open(encoding="utf-8", newline="").read(), relpath, where=str(path)
        )
        parsed.append((row, order, relpath))
    parsed.sort(
        key=lambda item: (item[1] is None, item[1] or 0, _id_number(item[0]["WI-ID"]))
    )
    return parsed


def _id_number(wi_id):
    match = re.search(r"\d+", wi_id or "")
    return int(match.group()) if match else 0


def to_csv(work_dir, out_path):
    """Rebuild the registry CSV from a spec folder. Returns the row count."""
    parsed = read_specs(work_dir)
    write_csv(out_path, [row for row, _order, _rel in parsed])
    return len(parsed)


def verify(csv_path, emit=print):
    """Full round-trip: CSV -> specs -> CSV in a temp dir, compared CELL-EXACT.

    Byte identity is REPORTED, not asserted. The bytes can differ for a reason
    that is not a data loss — QUOTE_MINIMAL quotes a field the source author
    quoted differently, say — and asserting on them would make a cosmetic
    difference indistinguishable from a dropped cell, which is the distinction
    this whole exercise exists to keep.
    """
    csv_path = Path(csv_path)
    source = load_csv(csv_path)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        written = to_specs(csv_path, tmp / "work")
        rebuilt_path = tmp / "work-items.csv"
        count = to_csv(tmp / "work", rebuilt_path)
        rebuilt = load_csv(rebuilt_path)
        rebuilt_bytes = rebuilt_path.read_bytes()

    findings = []
    if len(source) != len(rebuilt):
        findings.append("row count: {} -> {}".format(len(source), len(rebuilt)))
    for index, (before, after) in enumerate(zip(source, rebuilt)):
        for column in COLUMNS:
            lhs, rhs = before.get(column) or "", after.get(column) or ""
            if lhs != rhs:
                findings.append(
                    "row {} ({}) {}: {!r} -> {!r}".format(
                        index + 2, before.get("WI-ID"), column, lhs, rhs
                    )
                )
    for finding in findings:
        emit("wi_convert: MISMATCH {}".format(finding))

    source_bytes = csv_path.read_bytes()
    identical = source_bytes == rebuilt_bytes
    emit(
        "wi_convert: {} rows -> {} spec files -> {} rows; cell-exact: {}; "
        "byte-identical: {}{}".format(
            len(source),
            len(written),
            count,
            "NO ({} mismatch(es))".format(len(findings)) if findings else "yes",
            "yes" if identical else "no",
            ""
            if identical
            else " ({})".format(_byte_reason(source_bytes, rebuilt_bytes)),
        )
    )
    return not findings


def _byte_reason(source_bytes, rebuilt_bytes):
    """A one-line, honest account of a byte difference that is not a cell
    difference — quoting style, a BOM, or line endings."""
    reasons = []
    if source_bytes.startswith(b"\xef\xbb\xbf") != rebuilt_bytes.startswith(
        b"\xef\xbb\xbf"
    ):
        reasons.append("BOM differs")
    if (b"\r\n" in source_bytes) != (b"\r\n" in rebuilt_bytes):
        reasons.append("line endings differ")
    if source_bytes.count(b'"') != rebuilt_bytes.count(b'"'):
        reasons.append(
            "quoting style: {} quote chars -> {} (QUOTE_MINIMAL re-decides which "
            "fields need quoting)".format(
                source_bytes.count(b'"'), rebuilt_bytes.count(b'"')
            )
        )
    if not reasons:
        reasons.append("whitespace or field-order difference outside the parsed cells")
    return "; ".join(reasons)


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--to-specs", action="store_true", help="write one spec file per CSV row"
    )
    mode.add_argument(
        "--to-csv",
        action="store_true",
        help="rebuild the registry CSV from a spec folder",
    )
    mode.add_argument(
        "--verify",
        action="store_true",
        help="round-trip the CSV through the spec form in a temp dir and compare "
        "cell-exact (exit 1 on any mismatch)",
    )
    ap.add_argument(
        "--csv", help="the work-item registry CSV (in, or out for --to-csv)"
    )
    ap.add_argument("--work", help="the spec folder (docs/work-shaped)")
    ap.add_argument(
        "--force",
        action="store_true",
        help="--to-specs: write into a non-empty work directory",
    )
    args = ap.parse_args()

    try:
        if args.to_specs:
            if not args.csv or not args.work:
                ap.error("--to-specs needs --csv and --work")
            written = to_specs(args.csv, args.work, force=args.force)
            print(
                "wi_convert: wrote {} spec files under {}".format(
                    len(written), args.work
                )
            )
            return 0
        if args.to_csv:
            if not args.csv or not args.work:
                ap.error("--to-csv needs --work and --csv")
            count = to_csv(args.work, args.csv)
            print("wi_convert: wrote {} rows to {}".format(count, args.csv))
            return 0
        if not args.csv:
            ap.error("--verify needs --csv")
        return 0 if verify(args.csv) else 1
    except ConvertError as exc:
        print("wi_convert: {}".format(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
