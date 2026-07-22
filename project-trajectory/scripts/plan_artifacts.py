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
items in `docs/requirements/work-items.csv` — such that `check_trajectory.py`
passes on the result (R-A: a queued WI carries an empty Deliverable; the graph
stays acyclic; plan-local predecessors resolve to the freshly minted ids).

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

Contracts: IF-061 — the interface seam this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import csv
import re
from pathlib import Path

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
]

# A round directory: `DP-<digits>-<slug>` under docs/plans/.
DP_DIR_RE = re.compile(r"^DP-(\d+)-")
# A well-formed work-item id (`WI-001`); the `-000` example row matches too but
# is inert — it never constrains the next-id allocation (max real id + 1).
WI_ID_RE = re.compile(r"^WI-(\d+)$")

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


def _split_tokens(cell):
    """Ref tokens from a table cell: ids separated by ``;`` ``,`` or whitespace
    (the `_split_refs` idiom); an empty cell yields ``[]``."""
    return [t for t in re.split(r"[;,\s]+", (cell or "").strip()) if t]


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
    """The integer suffixes of every well-formed `WI-###` id already in the
    registry (the inert `-000` example included — it is still a real max floor
    of 0, never a collision), or an empty set when the file is absent."""
    nums = set()
    if not csv_path.exists():
        return nums
    # utf-8-sig: a BOM'd registry (Excel) renamed the first header key, so ZERO
    # existing ids were found and fresh children minted from WI-001 straight
    # into collisions (repo-review 2026-07-21 M-33).
    with csv_path.open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            m = WI_ID_RE.match((r.get("WI-ID") or "").strip())
            if m:
                nums.add(int(m.group(1)))
    return nums


def _registry_header(csv_path):
    """Return an existing registry's declared column order or the modern
    template header for an absent/empty registry."""
    if csv_path.exists() and csv_path.stat().st_size:
        # utf-8-sig: with a BOM the first header name became "﻿WI-ID" and
        # DictWriter(extrasaction="ignore") silently DROPPED every row's real
        # "WI-ID" value — appended rows carried empty id cells (M-33).
        with csv_path.open(encoding="utf-8-sig", newline="") as fh:
            header = next(csv.reader(fh), [])
        if header:
            return header
    return WI_HEADER


def _append_csv_rows(csv_path, rows):
    """Append mapping `rows` by the registry's actual header (quoting-safe),
    preserving line endings and terminating the prior last row first."""
    newline = _detect_newline(csv_path)
    write_header = not csv_path.exists() or csv_path.stat().st_size == 0
    needs_nl = csv_path.exists() and csv_path.read_bytes()[-1:] not in (b"", b"\n")
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("a", encoding="utf-8", newline="") as fh:
        if needs_nl:
            fh.write(newline)
        writer = csv.DictWriter(
            fh,
            fieldnames=_registry_header(csv_path),
            extrasaction="ignore",
            lineterminator=newline,
        )
        if write_header:
            writer.writeheader()
        for row in rows:
            writer.writerow(row)


def allocate_round_dir(root, slug):
    """Create and return the next `docs/plans/DP-NNN-<slug>/` directory.

    `NNN` = (max existing DP-### under docs/plans/) + 1, zero-padded to 3, so an
    empty tree yields `DP-001` and an existing `DP-001-...` yields `DP-002`. The
    allocation is deterministic (a pure function of the current tree) and creates
    the directory so the caller can immediately `write_stage` into it."""
    plans = Path(root) / "docs" / "plans"
    plans.mkdir(parents=True, exist_ok=True)
    nums = [
        int(m.group(1))
        for p in plans.iterdir()
        if p.is_dir()
        for m in [DP_DIR_RE.match(p.name)]
        if m
    ]
    nxt = (max(nums) + 1) if nums else 1
    round_dir = plans / "DP-{:03d}-{}".format(nxt, slug)
    round_dir.mkdir(parents=True, exist_ok=False)
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

    existing = _existing_wi_nums(csv_path)
    start = (max(existing) + 1) if existing else 1
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
    _append_csv_rows(csv_path, out_rows)
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
