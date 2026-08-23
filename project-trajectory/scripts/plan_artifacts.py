#!/usr/bin/env python3
"""The dual-plan round artifact filer: the coordinator's write-side of a round
(DP-001 selected plan P5 / WI-198; the protocol it serves is
process-options.md "Dual-plan decomposition").

Stack-agnostic, standard-library only (Python 3.11+, Windows/POSIX). Where
`plan_round.py` (IF-058) is the pure lifecycle and `plan_coverage.py` (IF-057)
is the read-side coverage pre-pass, this module is the round's **effects**: it
allocates the round's `docs/plans/DP-NNN-<slug>/` directory, writes each stage
artifact (briefs, plans, revisions, critiques, coverage reports, verdict) as a
tracked UTF-8 file with a stable name, appends the verdict summary to
`docs/log.md`, and files the selected plan's `Plan-WI` rows as **queued** work
items in the registry's home — `docs/work/queued/` spec files when the folder
is the registry (via the `wi_convert` sibling, IF-078), legacy
spec files (the one registry home since Phase 5) — such that
`check_trajectory.py` passes on the result (R-A: a queued WI carries an empty
Deliverable; the graph stays acyclic; plan-local predecessors resolve to the
freshly minted ids).

Four effects, each a plain function the coordinator calls:

    allocate_round_dir(root, slug)  -> the next DP-NNN-<slug>/ (deterministic)
    write_stage(round_dir, name, text)  -> one tracked stage artifact
    file_selected_wis(root, plan_text, spec_ref, workstream, predecessor_wi,
                      tier_map=None)  -> {plan-local id: new WI id}
    append_log_summary(root, text)  -> the verdict block appended to docs/log.md

The `Plan-WI` table it parses is `plan_coverage.py`'s commensurability
contract: `| Plan-WI | Title | Covers | Interfaces | Predecessors |`. A small
parser is duplicated here (never a sibling import — the kit's independently
copy-able-script convention, F5); this one only needs id/title/predecessors, so
it stays deliberately smaller than `plan_coverage.parse_plan`.

Contracts: IF-061; IF-078; IF-116 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.toml).
"""

import csv
import re
import sys
from pathlib import Path

# Sibling import (the gen_trajectory -> check_trajectory pattern): scripts/ is
# not a package, so a by-path load (tests, embedding) needs scripts/ on
# sys.path before the sibling resolves. wi_convert is the registry's single
# spec-file writer — filing and bulk migration MUST share it so a spec cannot
# be produced by a path that skips its self-verification (IF-078).
try:
    import wi_convert
except ImportError:  # pragma: no cover - direct-path loads only
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import wi_convert

# AFTER the path fix, never as the probe — `trace` collides with a STDLIB module
# of that name, so importing it first would resolve to the wrong module instead
# of raising the ImportError this fallback keys on (`intake.py` orders its
# imports the same way, for the same reason). It is the id watermark's home:
# both mints below count from the MARK, never from `max(live)` (repo-lock D-4).
import trace  # noqa: E402

# The shipped shared-helper package: the spine ROW cell vocabulary (D-8/OI-16).
from kitlib import spine as _kitspine  # noqa: E402

WI_CSV = "docs/requirements/work-items.csv"
# The modern header of record for a new work-item registry. Existing registries
# are appended in THEIR declared order so legacy or extended schemas stay
# structurally valid; optional scheduler fields are deliberately left blank.
WI_HEADER = [
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
    "Supersedes",
    "Brief",
]

# A round directory: `DP-<digits>-<slug>` under docs/plans/.
DP_DIR_RE = re.compile(r"^DP-(\d+)-")
# A well-formed work-item id (`WI-001`); the `-000` example row matches too but
# is inert — it never constrains the next-id allocation (max real id + 1).
WI_ID_RE = re.compile(r"^WI-(\d+)$")
# A spec FILENAME's id prefix (`WI-011-some-slug.md`) — the folder home's ids
# are read off filenames, never file contents (the loaders verify the
# frontmatter id against the filename on every read, so the filename is safe
# to trust here).
WI_FILE_RE = re.compile(r"^WI-(\d+)-.*\.md$")

DEFAULT_TIER = "medium"


def _detect_newline(path, default="\n"):
    """The line-ending convention of an existing text file (``\\r\\n`` or
    ``\\n``), so an append preserves it rather than mixing conventions. Absent
    or empty file -> `default`."""
    if not path.exists():
        return default
    data = path.read_bytes()
    if b"\r\n" in data:
        return "\r\n"
    if b"\n" in data:
        return "\n"
    return default


# Ref tokens from a table cell: ids separated by ``;`` ``,`` or whitespace; an
# empty cell yields ``[]``. ONE HOME since WI-448 slice 4
# (`kitlib.spine.refs`) — this was one of six copies of the same body, kept
# under its own local name so no call site below moves.
_split_tokens = _kitspine.refs


def parse_plan_wis(text):
    """The selected plan's `Plan-WI` rows (id/title/predecessors) from the first
    markdown table whose header carries a `Plan-WI` column, or ``[]`` when no
    such table exists.

    A small parser duplicated from `plan_coverage.parse_plan` per the kit's
    copy-able-script convention (F5) — the filer only needs the id, the title,
    and the plan-local predecessor edges, so it does not carry the Covers /
    Interfaces cells."""
    header = None
    rows = []
    for line in text.splitlines():
        if "|" not in line:
            if header is not None and rows:
                break  # the table ended
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            if any(c.lower() == "plan-wi" for c in cells):
                header = [c.lower() for c in cells]
            continue
        if set("".join(cells)) <= set("-: "):
            continue  # the |---|---| separator line
        row = dict(zip(header, cells))
        if row.get("plan-wi"):
            rows.append(
                {
                    "id": row.get("plan-wi", ""),
                    "title": row.get("title", ""),
                    "predecessors": row.get("predecessors", ""),
                }
            )
    return rows


def _existing_wi_nums(csv_path):
    """The integer suffixes of every well-formed `WI-###` id in the folder home
    plus any stray legacy CSV (the inert `-000` example included — a real max
    floor of 0, never a collision). The CSV home retired at Phase 5, but a
    stray file's ids still count: an allocator that ignored them could mint a
    collision while the validator routes the human to delete the file."""
    nums = set()
    if csv_path.exists():
        # utf-8-sig: a BOM'd registry (Excel) renamed the first header key, so
        # ZERO existing ids were found and fresh children minted from WI-001
        # straight into collisions (repo-review 2026-07-21 M-33).
        with csv_path.open(encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                m = WI_ID_RE.match((r.get("WI-ID") or "").strip())
                if m:
                    nums.add(int(m.group(1)))
    for path in wi_convert.spec_paths(wi_convert.work_dir_for(csv_path)):
        m = WI_FILE_RE.match(path.name)
        if m:
            nums.add(int(m.group(1)))
    return nums


# (_registry_header/_append_csv_rows — the CSV home's append — retired with
# the CSV registry at concurrency-restructure Phase 5; the folder writer
# below is the one filing path.)


def _write_spec_rows(csv_path, rows):
    """The folder home's append: file each mapping row as a spec file in
    `docs/work/queued/` via `wi_convert.write_spec_file` (the format's single
    writer). Refuses BY NAME if a spec in ANY status directory already carries
    an id being filed — two files for one work item is the one state the
    registry cannot represent, and a silent overwrite would destroy the older
    record. Returns the written relative paths."""
    work_dir = wi_convert.work_dir_for(csv_path)
    existing = {}
    for path in wi_convert.spec_paths(work_dir):
        m = WI_FILE_RE.match(path.name)
        if m:
            existing["WI-" + m.group(1)] = path.relative_to(work_dir).as_posix()
    written = []
    for row in rows:
        wid = row["WI-ID"]
        if wid in existing:
            raise ValueError(
                "cannot file {}: a spec already carries this id at {} — "
                "the allocator and the tree disagree; resolve before "
                "filing".format(wid, existing[wid])
            )
        written.append(wi_convert.write_spec_file(work_dir, row))
    return written


def allocate_round_dir(root, slug):
    """Create and return the next `docs/plans/DP-NNN-<slug>/` directory.

    `NNN` = `max(live directories, docs/id-watermark's DP mark) + 1`, zero-padded
    to 3, so an empty tree yields `DP-001` and an existing `DP-001-...` yields
    `DP-002`. Live directories are still swept, for the same reason
    `intake.next_wi_id` still sweeps filenames: for a MINT, an id held anywhere
    is an id taken. But the FLOOR is the mark, because `max(live) + 1` re-issues
    the number of any round that has been DELETED — and deletion is how
    supersession works, so a reused DP id silently re-points every log entry
    and commit message citing that round.

    The mark is then RAISED in the same act, matching `intake`'s mint: an
    allocation that does not record itself leaves the mark behind the tree, and
    `trace.py`'s integrity pass reads that as "an id was allocated past the
    mark" — correctly, because it was. `trace.read_watermark` RAISES on an
    absent or malformed mark and that refusal is deliberately not caught: a mint
    with no record of what has been allocated must not proceed on a guess."""
    plans = Path(root) / "docs" / "plans"
    plans.mkdir(parents=True, exist_ok=True)
    nums = [
        int(m.group(1))
        for p in plans.iterdir()
        if p.is_dir()
        for m in [DP_DIR_RE.match(p.name)]
        if m
    ]
    mark = trace.read_watermark(root).get("DP", 0)
    round_dir = plans / "DP-{:03d}-{}".format(max(max(nums, default=0), mark) + 1, slug)
    round_dir.mkdir(parents=True, exist_ok=False)
    # After the mkdir: `bump_watermark` reads the LIVE tree, so the directory has
    # to exist for the bump to see the number it just handed out.
    trace.bump_watermark(root)
    return round_dir


def write_stage(round_dir, name, text):
    """Write one stage artifact `name` (a stable filename — `goal.md`,
    `plan-A.md`, `coverage-r1.md`, `verdict.md`, ...) into `round_dir` as a
    tracked UTF-8 file, and return its path. Line endings are written verbatim
    (``newline=""``) so the committed artifact is byte-stable across platforms."""
    round_dir = Path(round_dir)
    round_dir.mkdir(parents=True, exist_ok=True)
    path = round_dir / name
    with path.open("w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    return path


def file_selected_wis(
    root, plan_text, spec_ref, workstream, predecessor_wi, tier_map=None
):
    """Append the selected plan's `Plan-WI` rows as **queued** work items and
    return the ``{plan-local id: new WI id}`` mapping.

    Each plan row becomes one registry row: a fresh sequential id (max existing
    `WI-###` + 1 onward), Title from the plan, the given `workstream`, an empty
    `SR-Refs`, `Status=queued`, an empty `Deliverable` (R-A), `SpecRef=spec_ref`,
    and `BuildTier` from `tier_map` (plan-local id -> tier) defaulting to
    ``medium``. Predecessors are the plan-local edges mapped to the new real ids,
    plus `predecessor_wi` (the round's parent WI) on **every** row when given —
    so the filed slice hangs off its parent and stays an acyclic extension of the
    existing DAG. All ids are allocated before predecessors are mapped, so a
    fan-in row referencing later plan rows resolves correctly."""
    tier_map = tier_map or {}
    csv_path = Path(root) / WI_CSV
    rows = parse_plan_wis(plan_text)
    if not rows:
        return {}

    # The filer is the last writer before the serialized integration commit, so
    # it fails closed on damaged input instead of trusting the coverage pass
    # upstream (which the manual --dual-plan flow can bypass) — repo-review
    # 2026-07-21 L-29. The caller has a PAGE channel for the ValueError.
    ids = [r["id"] for r in rows]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        raise ValueError(
            "selected plan repeats Plan-WI id(s) {} — duplicate plan-local ids "
            "would mint one real WI id for two rows".format(", ".join(dupes))
        )

    # `max(live, mark) + 1` — the same mint `intake.next_wi_id` performs, and for
    # the same reason: `max(live) + 1` re-issues the id of any spec that has been
    # DELETED, which is how a superseded work item goes away.
    # The union over both homes stays (a live id anywhere is taken); the mark is
    # the FLOOR under it, and the reader RAISES rather than degrading to zero.
    existing = _existing_wi_nums(csv_path)
    mark = trace.read_watermark(root).get("WI", 0)
    start = max(max(existing, default=0), mark) + 1
    mapping = {r["id"]: "WI-{:03d}".format(start + i) for i, r in enumerate(rows)}

    out_rows = []
    for r in rows:
        preds = [mapping.get(tok, tok) for tok in _split_tokens(r["predecessors"])]
        unknown = [
            t for t in preds if t not in mapping.values() and not WI_ID_RE.match(t)
        ]
        if unknown:
            raise ValueError(
                "plan row {} names predecessor token(s) {} that are neither "
                "plan-local ids nor WI-### shaped".format(r["id"], ", ".join(unknown))
            )
        if predecessor_wi and predecessor_wi not in preds:
            preds.append(predecessor_wi)
        out_rows.append(
            {
                "WI-ID": mapping[r["id"]],
                "Title": r["title"],
                "Workstream": workstream,
                "SR-Refs": "",
                "Predecessors": ";".join(preds),
                "Status": "queued",
                "Deliverable": "",  # R-A: filled only when closed
                "SpecRef": spec_ref,
                "BuildTier": tier_map.get(r["id"], DEFAULT_TIER),
            }
        )
    # Filing home: the spec folder, the one registry home since the CSV
    # retired (concurrency-restructure Phase 5, RULING-4).
    _write_spec_rows(csv_path, out_rows)
    # RAISE THE MARK in the same act that files the specs (intake's rule), and
    # only after they are on disk — `bump_watermark` reads the live tree.
    trace.bump_watermark(root)
    return mapping


def append_log_summary(root, text):
    """Append a verdict-summary block (`text`, composed by the caller — it owns
    the ``## `` heading) to `docs/log.md`, separated from prior content by one
    blank line and terminated with a newline. Preserves the log's existing
    line-ending convention; returns the log path."""
    log = Path(root) / "docs" / "log.md"
    newline = _detect_newline(log)
    existing = log.read_text(encoding="utf-8") if log.exists() else ""
    prefix = ""
    if existing and not existing.endswith("\n\n"):
        prefix = "\n" if existing.endswith("\n") else "\n\n"
    body = prefix + (text if text.endswith("\n") else text + "\n")
    if newline != "\n":
        body = body.replace("\n", newline)
    with log.open("a", encoding="utf-8", newline="") as fh:
        fh.write(body)
    return log
