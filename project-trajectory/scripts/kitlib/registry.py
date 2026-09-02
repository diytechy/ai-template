"""The `docs/work/` spec-folder work-item registry reader — the one read half.

`docs/work/<status>/WI-###-<slug>.md`: one Markdown spec per work item, its
STATUS encoded as the DIRECTORY (docs/concurrency-restructure.md §2.1, Phase
2b). The reader emits rows carrying the SAME 19 keys `csv.DictReader` used to
yield for the retired `work-items.csv`, so consumers past `load_wis` never
learn which home was authoritative. The format's DEFINITION is
`scripts/wi_convert.py` (`parse_spec` / `status_from_location`), which
materializes the folder; this module is its read half.

WHAT THIS REPLACES. Until WI-448 this 270-line block was copied VERBATIM into
`schedule.py`, `check_trajectory.py` and `agent_common.py` under the retired F5
rule, with `tests/test_wi_loader_sync.py` pinning the three parsers equal
because extraction had been refused (owner ruling 2026-07-12). D-8 reversed
that ruling. The extraction also settled a live question the pins could not
see: the three copies were NOT verbatim at the moment they were merged —
`agent_common`'s carried `a DevStg-* value` in the `Bar` comment where the
other two carried the literal `DevStg-Reqs|DevStg-Tests|DevStg-Impl` enum, a
comment-only drift from the 2026-08-18 one-vocabulary rename reaching two homes
of three. Behaviour-equal, so a behavioural pin was structurally blind to it;
the more informative spelling is the one kept below.

The three modules now import from here, so `load_wis`' own POLICY split — the
scheduler skips a malformed row, the validator reports it — stays where it
belongs: in each consumer, over one shared parse.
"""

import re
import tomllib
from pathlib import Path

__all__ = [
    "WI_COLUMNS",
    "SPEC_SCALARS",
    "SPEC_LISTS",
    "LIST_TOLERANT_SCALARS",
    "scalar_cell",
    "SPEC_STATUS_DIRS",
    "SPEC_FENCE",
    "SPEC_DELIVERABLE",
    "SPEC_HANDBACK",
    "SPEC_CONTEXT",
    "spec_work_dir",
    "spec_archive_dir",
    "spec_roots",
    "spec_files",
    "parse_spec_frontmatter",
    "parse_spec_status",
    "parse_spec_id",
    "parse_spec_deliverable",
    "parse_spec_row",
    "read_spec_rows",
    "spec_id_number",
]

WI_COLUMNS = (
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
    # `Supersedes` reason above — `intake` writes it through
    # `wi_convert.write_spec_file`, which serializes from this table.
    "Brief",
    # WI-572 SCOPE OF THE ACT. The registry row ids an adjudication was minted
    # OVER, `;`-joined — the population the merge handed it, and the bound the
    # brief's LIVE re-derivation intersects against so the act cannot widen past
    # what was handed over. Empty on every row that is not an adjudication.
    "Adjudicates",
)
SPEC_SCALARS = (
    ("Title", "title"),
    ("Workstream", "workstream"),
    ("SpecRef", "specref"),
    ("BuildTier", "buildtier"),
    ("CritiqueBudget", "critique_budget"),
    ("CritiqueExhaustion", "critique_exhaustion"),
    ("Priority", "priority"),
    ("Exclusive", "exclusive"),
    ("EstTokens", "est_tokens"),
    ("SafetyClass", "safety_class"),
    ("PlanMode", "planmode"),
    # WI-388: bar declares verification strictness for this row's lane; it
    # never affects scheduling. (DevStg-Reqs|DevStg-Tests|DevStg-Impl — integrate.refresh passes it to
    # check.py --gate; load_wis deliberately does not parse it.)
    ("Bar", "bar"),
    ("Supersedes", "supersedes"),
    ("Brief", "brief"),
)
SPEC_LISTS = (
    ("SR-Refs", "sr_refs"),
    ("Predecessors", "needs"),
    ("Adjudicates", "adjudicates"),
)
# The scalars whose frontmatter key may ALSO be written as a TOML list, read
# either way into the same `;`-joined cell. `supersedes` is the one (the
# 2026-09-02 restructure plan §1.5): a consolidation absorbs SEVERAL rows into
# one successor, so the successor's lineage names several predecessors, while
# every other successor names exactly one. Widening the CELL to a list would
# have re-typed a column and every reader of it for a shape most rows never
# carry; widening the FRONTMATTER is the whole change, and a bare string keeps
# reading byte-for-byte as it always did. Deliberately NOT a `SPEC_LISTS` entry:
# those columns are lists in every row, and a `SPEC_LISTS` `supersedes` would
# make `wi_convert` re-emit a one-id cell as a one-element list, changing every
# existing spec file's bytes for nothing.
LIST_TOLERANT_SCALARS = frozenset({"supersedes"})
# Directory -> Status. The directory is the WHOLE statement (WI-384): every
# state owns a folder — including BOTH terminals, `complete/` for work that
# shipped and `cancelled/` for work that never will — so nothing in the
# frontmatter disambiguates a folder and nothing can disagree with one.
# `draft/` is thinking-in-progress, and it is DECLARED rather than left as an
# unscanned folder because an undeclared directory's specs are skipped below:
# they never enter the registry, so the duplicate-id guard and the dashboard go
# blind to an id a draft holds. (The id MINT is safe either way — it reads
# FILENAMES, never this table — so declaring the folder makes the reservation
# CHECKED rather than incidental; driven at WI-384's review.) The two terminal
# WORDS differ for a reason:
# `complete/` renamed a folder whose rows still read `done` (the status word
# every consumer already speaks), while `cancelled` had no folder to rename —
# only the `disposition = "retired"` spelling this row deleted — so the word
# itself moved. `active/<branch>/` sits one level deeper, so the status is the
# FIRST path component, never the file's parent directory.
# `partial/` (SR-144) is the THIRD terminal, and the one that made the outcome
# model honest. A lane that stops early used to move back to `queued/` carrying
# a `## Handback` note and a `blockref` — which meant the return event had no
# artifact of its own, only a mutable, movable, self-referencing spec. Five
# successive dedup mechanisms tried to reconstruct "did a return happen, and was
# it judged?" from that spec, and every one leaked: an owed judgement silently
# not happening. `partial/` is TERMINAL — nothing re-claims it, so nothing
# strands — and the per-close report under docs/handbacks/ IS the event's
# identity. Continuing the work MINTS A SUCCESSOR (carrying `supersedes`),
# because a closed row is never revived and a scope definition never changes to
# mean something else.
# `restructured/` is the FOURTH terminal (2026-09-02 backlog-restructure plan
# §1.6). A consolidation judgement may ABSORB several queued rows into one
# successor; the absorbed row is not refuted (`cancelled` would brief every
# later row on the same SRs that its scope was refuted — `intake.context_block`
# joins exactly that) and it did not stop early (`partial` owes a per-close
# report and mints a disposition). It was carried onward: its scope text stays
# byte-identical, its Deliverable is the one line `Restructured into WI-<n>.`,
# and its inbound hard edges are re-pointed to the successor at the close. It is
# TERMINAL — never re-claimed, never revived, and no lane may close into it.
SPEC_STATUS_DIRS = {
    "draft": "draft",
    "queued": "queued",
    "active": "active",
    "deferred": "deferred",
    "cancelled": "cancelled",
    "partial": "partial",
    "restructured": "restructured",
    "complete": "done",
}
SPEC_FENCE = "+++"
SPEC_DELIVERABLE = "\n## Deliverable\n\n"
# The body's OTHER section (WI-387): a lane that HANDS a WI back writes a
# `## Handback` note after the Deliverable's place, so the returned spec says
# in trunk what remains and where the partial work is. It carries no registry
# cell — nothing here parses it — and is recognised only so an honest
# returned spec does not read as a malformed one.
SPEC_HANDBACK = "\n## Handback\n"
# The body's THIRD section (WI-388): the advisory `## Context` block the
# intake mint writes into every minted row (pure registry joins — precedent,
# open items, the code map, knowledge packs), advisory-never-gating. Like the
# Handback note it carries no registry cell and is read PAST, so a minted row
# whose body is context-only parses with an empty Deliverable rather than as
# a malformation.
SPEC_CONTEXT = "\n## Context\n"


def spec_work_dir(csv_path):
    """The `docs/work` folder that replaces the registry CSV at `csv_path` — its
    `docs/` directory plus `work`, derived from the one path each caller already
    declares rather than from a second constant that could disagree with it."""
    return Path(csv_path).parent.parent / "work"


def spec_archive_dir(work_dir):
    """`docs/work`'s archive sibling, `docs/archive/work` (WI-504): terminal
    history (`complete/`, `cancelled/`, `partial/`) lives there, one directory
    deeper than the active workspace. Derived from `work_dir` the same way
    `spec_work_dir` derives `work_dir` from the CSV path — one fact, not a
    second constant a caller could let drift."""
    work_dir = Path(work_dir)
    return work_dir.parent / "archive" / "work"


def spec_roots(work_dir):
    """`work_dir` plus its archive sibling — BOTH homes a spec may live in
    while WI-504's relocation is honoured everywhere it must be: the active
    workspace (`draft/queued/active/deferred`, and — until a repo's own move
    commit lands — terminal directories not yet relocated) and the archive
    (`complete/cancelled/partial`, the new terminal home). Order is stable
    (`work_dir` first) so an id or ordering tie breaks the same way it always
    has."""
    work_dir = Path(work_dir)
    archive_dir = spec_archive_dir(work_dir)
    return (work_dir,) if archive_dir == work_dir else (work_dir, archive_dir)


def _spec_files_under(root):
    root = Path(root)
    if not root.is_dir():
        return []
    return [p for p in root.rglob("WI-*.md") if p.parent != root]


def spec_files(work_dir):
    """Every `<status>/WI-*.md` spec under `work_dir`, sorted by path; `[]` when
    the folder is absent or holds none. An empty answer is what leaves the CSV
    authoritative, so a stray file sitting DIRECTLY in `work_dir` — which has no
    status directory above it — deliberately does not count as a registry.

    Single-root: this is the primitive `read_spec_rows` below builds the
    both-roots union on top of, and the narrower thing a caller that already
    knows which one tree it means (a branch's own claimed set, a status-dir
    census) still wants undiluted."""
    return sorted(_spec_files_under(work_dir))


def parse_spec_frontmatter(text, relpath):
    """`(data, body)` for one spec file: the TOML frontmatter between the `+++`
    fences, parsed, and everything after the closing fence, verbatim."""
    lines = text.split("\n")
    if not lines or lines[0] != SPEC_FENCE or SPEC_FENCE not in lines[1:]:
        raise ValueError(
            "{}: no closed `{}` frontmatter fence".format(relpath, SPEC_FENCE)
        )
    close = lines.index(SPEC_FENCE, 1)
    try:
        data = tomllib.loads("\n".join(lines[1:close]))
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(
            "{}: frontmatter is not valid TOML — {}".format(relpath, exc)
        ) from None
    return data, "\n".join(lines[close + 1 :])


def parse_spec_status(relpath):
    """The Status a spec's LOCATION encodes — the whole of it.

    Each state owns one directory, so there is no attribute to cross-check and
    no way for location and frontmatter to disagree: WI-384 split `archive/`
    into `complete/` + `cancelled/` and with it deleted the `disposition` key,
    the cross-check, and both of its raise paths. One refusal survives, because
    it is the one a folder-as-state model still needs: a directory nobody
    declared. Dropping it into `queued` would silently reclassify work, which
    is the catch-all shape this kit refuses on sight."""
    parts = relpath.split("/")
    status = SPEC_STATUS_DIRS.get(parts[0]) if len(parts) > 1 else None
    if status is None:
        raise ValueError(
            "{}: {!r} is not a status directory (the spec form knows only {})".format(
                relpath, parts[0], ", ".join(sorted(SPEC_STATUS_DIRS))
            )
        )
    return status


def parse_spec_id(relpath, data):
    """The work-item id, which must be a non-empty string AND must be the one
    the filename carries — two homes for one fact, so they are compared here
    rather than trusted apart."""
    wid = data.get("id")
    if not isinstance(wid, str) or not wid:
        raise ValueError("{}: frontmatter carries no string `id`".format(relpath))
    if not relpath.split("/")[-1].startswith(wid + "-"):
        raise ValueError(
            "{}: filename does not carry its own id {!r}".format(relpath, wid)
        )
    return wid


def parse_spec_deliverable(relpath, body):
    """The Deliverable cell a spec body carries, verbatim ("" when absent).

    The long cell lives in the BODY precisely because body text needs no
    escaping: it may hold newlines, quotes and markdown. This format owns the
    whole body shape, so anything that is neither empty nor one
    `## Deliverable` section (optionally joined by the `## Handback` note a
    returned spec carries, or the advisory `## Context` block a minted spec
    carries — both clipped off before the cell is read) is a malformation
    rather than free prose."""
    if not body:
        return ""
    body = body.partition(SPEC_HANDBACK)[0]
    body = body.partition(SPEC_CONTEXT)[0]
    if not body:
        return ""
    if not body.startswith(SPEC_DELIVERABLE) or not body.endswith("\n"):
        raise ValueError(
            "{}: body is neither empty nor one `## Deliverable` section".format(relpath)
        )
    return body[len(SPEC_DELIVERABLE) : -1]


def scalar_cell(key, value):
    """One frontmatter SCALAR as its registry cell.

    A `LIST_TOLERANT_SCALARS` key written as a TOML list reads as the `;`-joined
    cell — the same join `SPEC_LISTS` columns take — so the two spellings of
    `supersedes` (one id as a bare string, several as a list) produce one cell
    shape and every reader downstream sees `;`-joined ids or nothing. Any other
    value is `str()`, exactly as it always was."""
    if key in LIST_TOLERANT_SCALARS and isinstance(value, (list, tuple)):
        return ";".join(str(v) for v in value)
    return str(value)


def parse_spec_row(text, relpath):
    """`(row, order)` for one spec file — a 19-key row shaped exactly like the
    CSV's. Raises ValueError NAMING the file on any malformation: invalid TOML, a
    missing or non-string `id`, an id the filename disagrees with, a directory
    that is not a status, or a body that is not the single `## Deliverable`
    section this format owns."""
    data, body = parse_spec_frontmatter(text, relpath)
    row = dict.fromkeys(WI_COLUMNS, "")
    row["WI-ID"] = parse_spec_id(relpath, data)
    row["Status"] = parse_spec_status(relpath)
    row["Deliverable"] = parse_spec_deliverable(relpath, body)
    for column, key in SPEC_SCALARS:
        if key in data:
            row[column] = scalar_cell(key, data[key])
    for column, key in SPEC_LISTS:
        if key in data:
            row[column] = ";".join(str(v) for v in data[key])
    order = data.get("order")
    return row, order if isinstance(order, int) else None


def read_spec_rows(work_dir, on_error=None):
    """The spec folder's rows in REGISTRY order — by the explicit `order` key,
    then by numeric id, which is the order the converter reproduces.

    Reads BOTH `work_dir` and its archive sibling (`spec_roots`, WI-504): the
    registry is one logical set of rows split across two directory trees — the
    active workspace and the terminal-history archive — and every consumer of
    this function (the scheduler's done-set, the dashboard, the R-A/R-F close
    rules, `intake`'s dedup) wants the UNION, never one half. A relpath is
    computed against whichever root actually holds the file, so `parse_spec_row`
    sees the same `<status>/WI-###-slug.md` shape either way and cannot tell
    which tree it came from — status is the directory, and both trees use the
    identical directory names for it.

    A malformed spec is reported to `on_error` (a callable taking one message)
    and skipped; with no sink it is skipped SILENTLY. That mirrors the split this
    kit already draws over the CSV — a broken registry is the validator's job to
    report, not the scheduler's to crash on. Files are read with universal
    newlines, so a spec checked out CRLF parses identically to one checked out
    LF (the WI-337 lesson: line endings are a property of the checkout)."""
    parsed = []
    for root in spec_roots(work_dir):
        for path in sorted(_spec_files_under(root)):
            relpath = path.relative_to(root).as_posix()
            try:
                row, order = parse_spec_row(path.read_text(encoding="utf-8"), relpath)
            except (ValueError, OSError, UnicodeDecodeError) as exc:
                if on_error is not None:
                    on_error(str(exc))
                continue
            parsed.append(
                (order is None, order or 0, spec_id_number(row["WI-ID"]), row)
            )
    parsed.sort(key=lambda item: item[:3])
    return [item[-1] for item in parsed]


def spec_id_number(wid):
    match = re.search(r"\d+", wid or "")
    return int(match.group()) if match else 0
