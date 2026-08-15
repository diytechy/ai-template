#!/usr/bin/env python3
"""Derive the dependency-ready WI frontier and its deterministic schedule.

Stack-agnostic, standard-library only (Python 3.11+, Windows/POSIX). This is the
scheduler contract of the parallel-WI-dispatch work (Slice A;
docs/specs/parallel-wi-dispatch.md LLR-058/LLR-059/LLR-089). It is a **pure, side-effect-free
library + CLI** shared by validation, the dashboard, the dispatcher, and tests —
it never mutates the registry, spawns a worker, or touches git. Readiness is
DERIVED from the tracked WI registry plus any reservations the caller passes
in; it is never copied into prose. The registry home is the spec folder
`docs/work/` (`load_registry_rows`; the CSV home retired at
concurrency-restructure Phase 5, RULING-4). Everything past that one function
— `load_wis` included — sees the same 18-key rows.

Two contracts live here:

  * **Frontier + deterministic order (LLR-058).** A queued WI is *ready* when every
    hard predecessor is integrated `done` (soft `~` edges never block). The ready
    set excludes `blocked`/`deferred`/`draft`/`cancelled`/reserved WIs and any WI
    the safety classifier deems ineligible, then orders the survivors by
    `(rank, Priority desc, transitive downstream-dependent count desc,
    remaining hard-path length desc, WI id)`.

  * **Deterministic safety classification on TWO axes (LLR-059/LLR-089;
    docs/concurrency-v2.md §A1).** One pure classifier maps a WI's declared
    `SafetyClass` (`ordinary|spine|gate|attestation|protected|high-risk`), its
    critique flag and the registry `PlanMode=dual` signal (LLR-095 — derived from
    the signal itself, never a second hand-set cell) to **two independent
    answers**, because the two questions are independent:

      - **concurrency** — *what may share the station?* `exclusive` (runs alone)
        or `parallel`. This is NOT the `Exclusive` mutex-key column below —
        different idea, same English word; the axis header says how they differ,
        and the emitted record spells the column `exclusive_keys` for that
        reason.
      - **rank** — *who goes first?* An integer, low first; it is the leading
        term of the order key and `Priority`/graph criticality/id break ties
        beneath it.

    They are read from two tables keyed by the same declared kind, never from
    each other, so changing one cannot move the other. Anything missing,
    unknown, or contradicting its structural evidence returns `unclassified`,
    which **fails closed** (never scheduled) for that WI without stopping
    disjoint classified work.

The optional schema columns (`Priority`, `Exclusive`, `BlockRef`, `EstTokens`,
`SafetyClass`) are read via `DictReader`, so a legacy registry without them reads
every value as its documented default — `Priority=0`, empty `Exclusive`,
`SafetyClass` absent => `unclassified` (empty is never silently `ordinary`).

Usage:
    python scripts/schedule.py ready [--explain] [--format text|json] [--root .]
    python scripts/schedule.py simulate --jobs N [--root .] [--format text|json]

Small CSV loaders are duplicated from trace.py / check_trajectory.py per the kit's
independently-copyable-script convention (the F5 rule): schedule.py stays a
self-contained drop-in, never importing the sibling engines.

Contracts: IF-053, IF-054 — the interface seams this module declares (process.md
§8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import csv
import json
import re
import sys
import tomllib
from pathlib import Path

WI_ID_RE = re.compile(r"^WI-\d+$")
REGISTRY = "docs/requirements/work-items.csv"

# --- safety classification vocabulary (LLR-059/LLR-089; spec §4 "Deterministic safety
# classification"). The DECLARED values a WI may carry in its SafetyClass cell.
# `adjudication` (WI-388, docs/concurrency-v2.md §A5.2) is the mechanical
# scope-judgement kind minted trunk-side at intake: exclusive, rank 1, and its
# lane runs NO product bar (integrate.refresh's no-bar arm) — its outputs are
# Status cells and the work registry, nothing a product bar can speak to. ---
SAFETY_CLASSES = (
    "ordinary",
    "spine",
    "gate",
    "attestation",
    "protected",
    "high-risk",
    "adjudication",
)

# --- the two axes the classifier RETURNS (docs/concurrency-v2.md §A1) ---------
# One declared kind answered two different questions through ONE five-value
# ladder (`spine-serial | protected-serial | single-wi | ordinary |
# unclassified`): `_GATE_RANK` made the class decide who goes first while
# `classify()` made the same class decide what may share the station. That is
# why `protected-serial` and `single-wi` looked like different things when both
# only ever meant *run alone*. The ladder is gone; the two questions are asked
# separately, of two tables keyed by the same declared kind.
#
# WORD OF WARNING, in the one module that has no excuse for one: this
# `exclusive` is NOT the `Exclusive` registry COLUMN. The column is a set of
# named mutex keys (`db`, `registry-lock`) that serializes the WIs sharing a
# key against EACH OTHER — see `_exclusive_conflicts`. This value is a WI's
# concurrency answer and names no key at all: `exclusive` here means alone in
# the station, full stop. The two travel together in one record, which is why
# the emitted key is `exclusive_keys` rather than `exclusive` (REVIEW-A round 1).
CONCURRENCY_EXCLUSIVE = "exclusive"  # runs alone — nothing else in the station
CONCURRENCY_PARALLEL = "parallel"  # may share the station with anything
CONCURRENCY_UNCLASSIFIED = "unclassified"  # fail closed — never scheduled

# Axis 1 — CONCURRENCY by declared kind. Note what is NOT here: the answer is
# read off the kind, never off the rank, and no kind is exclusive merely for
# being ranked early. `critique` is `parallel` because nothing about a critique
# touches product code; it was only ever serialized to keep it out of a packed
# multi-WI session, and with packing deleted (§A6.1) that had nothing left to
# prevent.
_KIND_CONCURRENCY = {
    "spine": CONCURRENCY_EXCLUSIVE,
    "adjudication": CONCURRENCY_EXCLUSIVE,
    "attestation": CONCURRENCY_EXCLUSIVE,
    "gate": CONCURRENCY_EXCLUSIVE,
    "protected": CONCURRENCY_EXCLUSIVE,
    "high-risk": CONCURRENCY_EXCLUSIVE,
    "critique": CONCURRENCY_PARALLEL,
    "ordinary": CONCURRENCY_PARALLEL,
}

# Axis 2 — RANK by declared kind: low first, the leading term of the order key.
# The numbers are §A1's ruled table verbatim. Rank 1 was written as a RESERVED
# gap for the `adjudication` kind; WI-388 filled it — one mapping added, no
# ruled number renumbered. Adjudication sorts behind spine (the scope change
# itself) and ahead of the window-closing kinds, because its judgement is what
# makes the narrowed detector (WI-380) safe: it must land before anything else
# builds on a premise the diff may have moved.
_KIND_RANK = {
    "spine": 0,
    "adjudication": 1,  # WI-388, §A5.2: exclusive, runs no bar
    "attestation": 2,
    "gate": 2,
    "protected": 3,
    "high-risk": 4,
    "critique": 5,
    "ordinary": 6,
}
# unclassified is excluded from the frontier, so its rank only matters for a
# stable total order in --explain output — last, behind every real kind.
RANK_UNCLASSIFIED = 7

# Tracked Status vocabulary (spec §3.1). Anything other than `done` is not-ready;
# `blocked`/`deferred`/`draft`/`cancelled`/reserved carry their own disposition
# (never silently scheduled) — the same fail-closed spirit. `cancelled` (WI-267
# as `retired`, respelled and given its own folder by WI-384) is a TERMINAL
# won't-build row: like `done` it is never in the ready frontier, but UNLIKE
# `done` a cancelled predecessor does NOT satisfy a successor's hard dependency
# (a cancelled WI never integrates, so a live WI hard-blocked on one can never
# run — it stays `waiting`, surfacing to the owner, rather than proceeding on a
# will-never-happen dependency; WI-267 design-decision 3).
_DONE = "done"
_CANCELLED = "cancelled"
_PARTIAL = "partial"
# The two never-ready OPEN states, which differ only in what they SAY (WI-384):
# `deferred` is a decision (we are not doing this now), `draft` is the absence of
# one (still being figured out). Neither is schedulable and neither is terminal,
# so each keeps its own disposition rather than being folded into the other.
_NEVER_READY = ("deferred", "draft")


def _utf8_console():
    """Emit UTF-8 whatever the console codepage is (the trace.py/check.py guard)."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


# --- small self-contained loaders (duplicated per the F5 rule) ----------------
def load_rows(path):
    if not Path(path).exists():
        return []
    with Path(path).open(newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


# --- the spec-folder registry reader (duplicated per the F5 rule) -------------
# `docs/work/<status>/WI-###-<slug>.md`: one Markdown spec per work item, its
# STATUS encoded as the DIRECTORY (docs/concurrency-restructure.md §2.1, Phase
# 2b). The reader emits rows carrying the SAME 18 keys `csv.DictReader` yields
# for `work-items.csv`, so the dual-read happens at the ROW level, once, here —
# `load_wis` and every consumer past it never learn which home is authoritative.
# The format's definition is `scripts/wi_convert.py` (`parse_spec` /
# `status_from_location`), which materializes the folder; this is its read half.
#
# Copied VERBATIM across schedule.py, check_trajectory.py and agent_common.py
# per the kit's F5 rule — a shared module was rejected (owner ruling
# 2026-07-12) so each script stays independently copy-able, and the one real
# risk of N parsers, DRIFT, is closed by tests/test_wi_loader_sync.py rather
# than by extraction (WI-291).
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
    # `Supersedes` reason above — `intake` writes it through
    # `wi_convert.write_spec_file`, which serializes from this table.
    "Brief",
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
    ("BlockRef", "blockref"),
    ("EstTokens", "est_tokens"),
    ("SafetyClass", "safety_class"),
    ("PlanMode", "planmode"),
    # WI-388: bar declares verification strictness for this row's lane; it
    # never affects scheduling. (DevBar-Reqs|DevBar-Tests|DevBar-Release — integrate.refresh passes it to
    # check.py --gate; load_wis deliberately does not parse it.)
    ("Bar", "bar"),
    ("Supersedes", "supersedes"),
    ("Brief", "brief"),
)
SPEC_LISTS = (("SR-Refs", "sr_refs"), ("Predecessors", "needs"))
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
SPEC_STATUS_DIRS = {
    "draft": "draft",
    "queued": "queued",
    "active": "active",
    "deferred": "deferred",
    "cancelled": "cancelled",
    "partial": "partial",
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


def spec_files(work_dir):
    """Every `<status>/WI-*.md` spec under `work_dir`, sorted by path; `[]` when
    the folder is absent or holds none. An empty answer is what leaves the CSV
    authoritative, so a stray file sitting DIRECTLY in `work_dir` — which has no
    status directory above it — deliberately does not count as a registry."""
    work_dir = Path(work_dir)
    if not work_dir.is_dir():
        return []
    return sorted(p for p in work_dir.rglob("WI-*.md") if p.parent != work_dir)


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


def parse_spec_row(text, relpath):
    """`(row, order)` for one spec file — an 18-key row shaped exactly like the
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
            row[column] = str(data[key])
    for column, key in SPEC_LISTS:
        if key in data:
            row[column] = ";".join(str(v) for v in data[key])
    order = data.get("order")
    return row, order if isinstance(order, int) else None


def read_spec_rows(work_dir, on_error=None):
    """The spec folder's rows in REGISTRY order — by the explicit `order` key,
    then by numeric id, which is the order the converter reproduces.

    A malformed spec is reported to `on_error` (a callable taking one message)
    and skipped; with no sink it is skipped SILENTLY. That mirrors the split this
    kit already draws over the CSV — a broken registry is the validator's job to
    report, not the scheduler's to crash on. Files are read with universal
    newlines, so a spec checked out CRLF parses identically to one checked out
    LF (the WI-337 lesson: line endings are a property of the checkout)."""
    parsed = []
    for path in spec_files(work_dir):
        relpath = path.relative_to(work_dir).as_posix()
        try:
            row, order = parse_spec_row(path.read_text(encoding="utf-8"), relpath)
        except (ValueError, OSError, UnicodeDecodeError) as exc:
            if on_error is not None:
                on_error(str(exc))
            continue
        parsed.append((order is None, order or 0, _spec_id_number(row["WI-ID"]), row))
    parsed.sort(key=lambda item: item[:3])
    return [item[-1] for item in parsed]


def _spec_id_number(wid):
    match = re.search(r"\d+", wid or "")
    return int(match.group()) if match else 0


# --- end of the F5-duplicated spec-folder reader ------------------------------


def load_registry_rows(path):
    """The work-item rows from the one registry home — the spec folder beside
    `path` (`docs/work/`, status = directory). The CSV home retired at
    concurrency-restructure Phase 5 (RULING-4); an absent folder reads as an
    empty registry, the non-adopter posture."""
    work_dir = spec_work_dir(path)
    return read_spec_rows(work_dir) if work_dir.is_dir() else []


def _split_refs(value):
    """Split a `;`/`,`/whitespace-separated ref cell into tokens."""
    return [t for t in re.split(r"[;,\s]+", (value or "").strip()) if t]


def _int(value, default=0):
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def load_wis(rows):
    """Parse work-item rows into a list of scheduler WI dicts (skips the inert
    `-000` example row and any malformed/duplicate id, exactly like
    check_trajectory.load_wis — a broken registry is the validator's job to
    report, not the scheduler's to crash on)."""
    wis, seen = [], set()
    for r in rows:
        wid = (r.get("WI-ID") or "").strip()
        if not wid.startswith("WI-") or not WI_ID_RE.match(wid) or wid in seen:
            continue
        seen.add(wid)
        if wid.endswith("-000"):
            continue
        preds, soft = [], []
        for p in _split_refs(r.get("Predecessors", "")):
            (soft if p.startswith("~") else preds).append(p.lstrip("~"))
        wis.append(
            {
                "id": wid,
                "title": (r.get("Title") or "").strip(),
                "status": (r.get("Status") or "queued").strip().lower(),
                "preds": preds,
                "soft": soft,
                "srs": _split_refs(r.get("SR-Refs", "")),
                "priority": _int(r.get("Priority"), 0),
                "exclusive": _split_refs(r.get("Exclusive", "")),
                "blockref": (r.get("BlockRef") or "").strip(),
                "est_tokens": _int(r.get("EstTokens"), 0),
                "safetyclass": (r.get("SafetyClass") or "").strip().lower(),
                "planmode": (r.get("PlanMode") or "").strip().lower(),
            }
        )
    return wis


# --- deterministic safety classification (LLR-059/LLR-089) ----------------------
def kind_of(wi, *, structural=None):
    """The declared KIND both §A1 axis tables are keyed by — `classify`'s
    step-1 resolution on its own, because the dispatcher's §A8 admission
    policy is keyed per kind per session hold (WI-381) and must read the
    ONE resolution rather than re-derive it or parse it back out of reason
    codes. Returns a `SAFETY_CLASSES` member or `"critique"`, or None exactly
    where `classify` quarantines (missing/unknown/contradicting declarations —
    the fail-closed rows that never reach a frontier)."""
    declared = (wi.get("safetyclass") or "").strip().lower()
    dual = (wi.get("planmode") or "").strip().lower() == "dual"
    if dual:
        if declared and declared != "high-risk":
            return None  # PlanMode contradicts the declared class (step 1)
        kind = "high-risk"
    else:
        if declared not in SAFETY_CLASSES:
            return None  # missing or unknown (step 2)
        struct = (structural or "").strip().lower() or None
        if declared == "ordinary" and struct in SAFETY_CLASSES and struct != "ordinary":
            return None  # contradicting structural evidence (step 3)
        kind = declared
    if kind == "ordinary" and bool(wi.get("critique")):
        kind = "critique"  # the promotion only lifts ordinary (step 4)
    return kind


def classify(wi, *, structural=None):
    """`(concurrency, rank, [reason_codes])` for one WI — a pure function.

    Inputs (§A1): the declared `SafetyClass`, a critique requirement (read off
    the WI's flags), the registry `PlanMode` signal, and optional `structural`
    evidence (the kind the repository graph implies, supplied by the validator).
    Resolution is two steps, and keeping them apart is the whole point of this
    function: first decide WHICH KIND this WI is, then read each axis off its
    own table.

      1. PlanMode=dual is the `high-risk` kind, DERIVED from the signal itself
         (LLR-095/WI-201: never a second hand-set cell; a declared SafetyClass
         other than empty or `high-risk` contradicts and quarantines).
      2. A declared SafetyClass that is missing or not in the vocabulary
         quarantines as `unclassified`.
      3. `ordinary` + contradicting structural evidence quarantines: a
         mis-declaration is never silently upgraded.
      4. The critique flag promotes only `ordinary` to the `critique` kind — a
         declared exclusive kind is the more constraining statement and wins.
      5. `_KIND_CONCURRENCY[kind]` and `_KIND_RANK[kind]`, read independently.

    A quarantined WI answers `(CONCURRENCY_UNCLASSIFIED, RANK_UNCLASSIFIED)`: it
    fails closed for itself and never blocks disjoint classified work.
    """
    declared = (wi.get("safetyclass") or "").strip().lower()
    dual = (wi.get("planmode") or "").strip().lower() == "dual"

    # Steps 1-4 live ONCE, in `kind_of`; what stays here is naming the cause a
    # quarantined row carries in --explain. A dual-plan round is the high-risk
    # kind and never needs a second hand-set SafetyClass cell (single-source);
    # a declared SafetyClass that contradicts the derivation quarantines — the
    # same cross-check posture as the structural rule, never a silent override.
    kind = kind_of(wi, structural=structural)
    if kind is None:
        if dual and declared and declared != "high-risk":
            return _unclassified("planmode-dual-vs-declared-%s" % declared)
        if not dual and declared not in SAFETY_CLASSES:
            code = "missing" if not declared else "unknown-value:%s" % declared
            return _unclassified(code)
        struct = (structural or "").strip().lower()
        return _unclassified("declared-ordinary-vs-structural-%s" % struct)

    concurrency, rank = _KIND_CONCURRENCY[kind], _KIND_RANK[kind]
    # The reason list names the concurrency answer and each signal that produced
    # it, so `--explain` stays readable: a dual row that ALSO declares high-risk
    # carries both codes, while a dual row with no SafetyClass cell (the
    # single-source shape) carries only the derived one.
    reasons = ["%s:dual-plan" % concurrency] if dual else []
    if declared:
        reasons.append("%s:%s" % (concurrency, kind))
    return concurrency, rank, reasons


def _unclassified(code):
    """The fail-closed answer, stated once so every quarantine path returns the
    same shape (both axes refused, never one)."""
    return CONCURRENCY_UNCLASSIFIED, RANK_UNCLASSIFIED, ["unclassified:%s" % code]


def is_schedulable(concurrency):
    """Only a positively-classified WI is eligible; unclassified fails closed."""
    return concurrency != CONCURRENCY_UNCLASSIFIED


# --- graph derivations (LLR-058) ----------------------------------------------
def _status(wis):
    return {w["id"]: w["status"] for w in wis}


def hard_preds_satisfied(wi, status):
    """Every hard predecessor is integrated `done`. An unknown predecessor id
    (dangling edge — the validator's error) OR a `retired` predecessor (WI-267:
    terminal, will never integrate) counts as NOT satisfied, so the scheduler
    fails closed rather than scheduling on a broken or dead-ended graph."""
    return all(status.get(p) == _DONE for p in wi["preds"])


def _hard_children(wis):
    """`{id: [hard-successor ids]}` — the hard-edge adjacency both graph
    derivations below walk (shared so the map is built once, one way)."""
    children = {w["id"]: [] for w in wis}
    ids = set(children)
    for w in wis:
        for p in w["preds"]:
            if p in ids:
                children[p].append(w["id"])
    return children


def downstream_counts(wis):
    """`{id: transitive hard-descendant count}` — how many distinct WIs depend on
    this one through hard edges (the unblocking-value signal in the order key).
    Explicit-stack DFS: a recursive walk hit Python's ~1000-frame limit on a
    long hard chain, crashing the scheduler on exactly the mature registries
    it exists for (repo-review 2026-07-21 L-23)."""
    children = _hard_children(wis)
    out = {}
    for wid in children:
        seen = set()
        stack = [wid]
        while stack:
            for c in children[stack.pop()]:
                if c not in seen:
                    seen.add(c)
                    stack.append(c)
        out[wid] = len(seen)
    return out


def hard_path_lengths(wis):
    """`{id: remaining hard-path length}` — the longest chain of hard descendants
    from this WI to a terminal (critical-path signal). Iterative memoized DFS —
    genuinely iterative now (an explicit frame stack): the previous version
    recursed per edge despite this docstring, so a hard chain deeper than
    Python's ~1000-frame limit crashed the scheduler (repo-review 2026-07-21
    L-23). A node already on the current path (a cycle — the validator's
    error) contributes 1 + 0, exactly as before."""
    children = _hard_children(wis)
    memo = {}

    def depth(root_wid):
        if root_wid in memo:
            return memo[root_wid]
        stack = [(root_wid, iter(children[root_wid]))]
        on_path = {root_wid}
        best = {root_wid: 0}
        while stack:
            wid, it = stack[-1]
            pushed = False
            for c in it:
                if c in memo:
                    best[wid] = max(best[wid], 1 + memo[c])
                elif c in on_path:  # cycle: bound the back-edge at 1 + 0
                    best[wid] = max(best[wid], 1)
                else:
                    stack.append((c, iter(children[c])))
                    on_path.add(c)
                    best[c] = 0
                    pushed = True
                    break
            if not pushed:
                stack.pop()
                on_path.discard(wid)
                memo[wid] = best[wid]
                if stack:
                    parent = stack[-1][0]
                    best[parent] = max(best[parent], 1 + memo[wid])
        return memo[root_wid]

    return {wid: depth(wid) for wid in children}


def order_key(wi, rank, downstream, hardpath):
    """The deterministic sort key: lowest rank first, then the human Priority
    override, then structural criticality, then WI id.

    It takes the RANK, not the classification, so the concurrency axis is not in
    the ordering decision (§A1). That is a convention, NOT a guarantee: the
    parameter is an untyped positional and nothing here inspects it, so the only
    thing keeping it true is the single call site in `evaluate`. REVIEW-A round 1
    drove `order_key(w, concurrency, …)` past the whole suite with byte-identical
    counts while genuinely reordering the frontier. What convicts that edit now
    is `test_the_frontier_orders_one_concurrency_group_by_rank`, which orders
    four kinds that share one concurrency value — do not weaken it into a test
    that hands this function a literal."""
    return (rank, -wi["priority"], -downstream, -hardpath, wi["id"])


def evaluate(wis, reserved=None):
    """Classify every WI and compute its readiness disposition — the one pass the
    frontier, --explain, and simulate all share. Returns a list of records dicts,
    one per WI, ordered by the deterministic key. `reserved` is an optional set of
    WI ids already claimed by a live train (excluded from the ready frontier)."""
    reserved = set(reserved or ())
    status = _status(wis)
    downstream = downstream_counts(wis)
    hardpath = hard_path_lengths(wis)
    exclusive_ready = _exclusive_conflicts(wis, status, reserved)

    records = []
    for w in wis:
        concurrency, rank, class_reasons = classify(w)
        disposition, reasons = _disposition(
            w, status, reserved, concurrency, class_reasons, exclusive_ready
        )
        records.append(
            {
                "id": w["id"],
                "status": w["status"],
                "concurrency": concurrency,
                "rank": rank,
                "disposition": disposition,
                "priority": w["priority"],
                "downstream": downstream[w["id"]],
                "hard_path": hardpath[w["id"]],
                # `exclusive_keys`, not `exclusive`: this is the mutex-key SET
                # from the `Exclusive` column, a different idea from the
                # `concurrency` value beside it (see the axis header above).
                "exclusive_keys": w["exclusive"],
                "reasons": reasons,
                "_key": order_key(w, rank, downstream[w["id"]], hardpath[w["id"]]),
            }
        )
    records.sort(key=lambda r: r["_key"])
    for r in records:
        del r["_key"]
    return records


def _exclusive_conflicts(wis, status, reserved):
    """`{exclusive-key: winning WI id}` — among the WIs that would otherwise be
    ready and share a non-empty `Exclusive` key, the deterministically-first one
    (by id) wins the key; the rest are exclusive-conflicting. A key held by a
    reserved/active WI is owned by it (a live train keeps its keys whatever its
    row now classifies as).

    This is the `Exclusive` COLUMN and has nothing to do with the `exclusive`
    CONCURRENCY value: a key serializes only the WIs that NAME THE SAME KEY
    against each other, while the concurrency value is about the station as a
    whole and names nothing. A `parallel` WI can hold a mutex key, and two
    `exclusive` WIs with no key still conflict — through the dispatcher's
    barrier, not through here."""
    holders = {}
    # A reserved WI owns each of its keys outright.
    for w in wis:
        if w["id"] in reserved:
            for k in w["exclusive"]:
                holders.setdefault(k, w["id"])
    # Otherwise the first ready WI (lowest id) claims each contested key. Only a
    # schedulable candidate may claim: an unclassified WI fails closed and can
    # never run, so letting it hold a mutex key would starve classified work the
    # key exists to serialize, not to freeze (the key guards CONCURRENT
    # execution; a quarantined WI is not executing).
    candidates = sorted(
        (
            w
            for w in wis
            if w["status"] == "queued"
            and w["id"] not in reserved
            and hard_preds_satisfied(w, status)
            and is_schedulable(classify(w)[0])
        ),
        key=lambda w: w["id"],
    )
    for w in candidates:
        for k in w["exclusive"]:
            holders.setdefault(k, w["id"])
    return holders


# Terminal statuses map straight to a not-in-the-frontier disposition + its own
# reason code (WI-267): `cancelled` is as final as `done` — never ready, never
# packed — but keeps a distinct code so the dead-end is legible in --explain.
_TERMINAL_DISPOSITION = {
    _DONE: ("done", "done:integrated"),
    _CANCELLED: ("cancelled", "cancelled:terminal-wont-build"),
    # LLR-161: `partial` is as final as the other two — a lane stopped early and
    # said so, and the disposition row it mints decides what happens next by
    # MINTING A SUCCESSOR, never by putting this row back on the frontier.
    # Read FIRST in `_disposition`, ahead of the queued+blockref arm, which is
    # the whole anti-livelock property: the old contract returned the spec to
    # `queued/` and leaned on a `blockref` to keep the driver from claiming,
    # handing back and re-claiming the same row forever.
    _PARTIAL: ("partial", "partial:terminal-stopped-early"),
}


def _waiting_reasons(wi, status):
    """Reason codes for a WI held `waiting` on unmet hard predecessors. WI-267
    design-decision 3: a cancelled predecessor is a DEAD hard edge — it will
    never integrate `done`, so the WI can never become ready. It is surfaced as
    its own reason code (the WI still just waits, never silently satisfied) so
    the owner sees the will-never-happen dependency."""
    unmet = [p for p in wi["preds"] if status.get(p) != _DONE]
    dead = [p for p in unmet if status.get(p) == _CANCELLED]
    reasons = ["waiting:hard-preds-not-done:%s" % ",".join(unmet)]
    if dead:
        reasons.insert(0, "waiting:hard-pred-cancelled:%s" % ",".join(dead))
    return reasons


def _disposition(wi, status, reserved, concurrency, class_reasons, exclusive_ready):
    """`(disposition, [reason_codes])` for one WI: ready | waiting | reserved |
    blocked | deferred | draft | done | cancelled | excluded. The reason list is
    its own codes; the classifier's reason is carried only where classification
    decides the outcome (`ready` shows why eligible, `unclassified` shows the
    fail-closed cause) — never as noise on a blocked/deferred/reserved/waiting
    item."""
    st = wi["status"]
    if st in _TERMINAL_DISPOSITION:
        disposition, code = _TERMINAL_DISPOSITION[st]
        return disposition, [code]
    # `blocked` has no directory in the spec-folder registry (concurrency-
    # restructure §2.1): a blocked item is `queued/` plus a `blockref` key, so
    # the disposition is DERIVED here rather than read as a status. (The
    # literal Status=blocked arm retired with the CSV home at Phase 5.)
    if st == "queued" and wi["blockref"]:
        return "blocked", ["excluded:blocked:%s" % wi["blockref"]]
    if st in _NEVER_READY:
        return st, ["excluded:%s" % st]
    if st not in ("queued", "active"):
        # A status this scheduler does not know (the legacy literal `blocked`
        # included) is never silently ready — the same fail-closed posture as
        # an unclassified SafetyClass.
        return "excluded", ["excluded:unknown-status:%s" % (st or "(empty)")]
    if wi["id"] in reserved:
        return "reserved", ["reserved:claimed-by-live-train"]
    if not hard_preds_satisfied(wi, status):
        return "waiting", _waiting_reasons(wi, status)
    if not is_schedulable(concurrency):
        return "excluded", list(class_reasons) + ["excluded:unclassified-fail-closed"]
    # Exclusive-key conflict: another WI owns a key this one needs.
    for k in wi["exclusive"]:
        owner = exclusive_ready.get(k)
        if owner and owner != wi["id"]:
            return "excluded", ["excluded:exclusive-conflict:%s@%s" % (k, owner)]
    return "ready", list(class_reasons) + ["ready"]


def frontier(wis, reserved=None):
    """The ordered ready frontier: records whose disposition is `ready`."""
    return [r for r in evaluate(wis, reserved) if r["disposition"] == "ready"]


def simulate(wis, jobs, reserved=None):
    """Greedy list-scheduling simulation over the hard DAG: each round assigns up
    to `jobs` ready WIs (in the deterministic order), marks them integrated, and
    rescans — the shape the dispatcher's dynamic refill produces. Returns a list
    of rounds, each a list of assigned WI ids. `--jobs 1` yields the serial order.

    This is a planning aid: it treats an assigned WI as immediately `done` and
    models neither build time nor reservations beyond the initial set. It does
    apply the `Exclusive` mutex keys (through `frontier`), but it does NOT apply
    the CONCURRENCY axis: a round here is "what could start", not "what the
    dispatcher admits" — the exclusive-runs-alone barrier is the dispatcher's
    (§A4). The two are different things; see the axis header."""
    if jobs < 1:
        raise ValueError("jobs must be >= 1")
    # Work on shallow copies so the caller's WIs are never mutated.
    work = [dict(w) for w in wis]
    reserved = set(reserved or ())
    rounds = []
    guard = len(work) + 1
    while guard >= 0:
        guard -= 1
        ready = [r["id"] for r in frontier(work, reserved)]
        if not ready:
            break
        assigned = ready[:jobs]
        rounds.append(assigned)
        done = set(assigned)
        for w in work:
            if w["id"] in done:
                w["status"] = _DONE
    return rounds


# --- CLI ----------------------------------------------------------------------
def _load(root):
    return load_wis(load_registry_rows(Path(root) / REGISTRY))


def _cmd_ready(args):
    wis = _load(args.root)
    if args.explain:
        records = evaluate(wis)
    else:
        records = frontier(wis)
    if args.format == "json":
        print(json.dumps(records, indent=2, sort_keys=True))
        return 0
    if not records:
        print(
            "schedule: no ready work items"
            if not args.explain
            else "schedule: (empty registry)"
        )
        return 0
    for r in records:
        if args.explain:
            display = dict(r)
            display["reasons"] = ";".join(r["reasons"])
            print(
                "{id:<10} {disposition:<9} {concurrency:<12} rank={rank} "
                "P{priority:<3} down={downstream:<3} path={hard_path:<3} {reasons}".format(
                    **display
                )
            )
        else:
            print(
                "{id:<10} {concurrency:<12} rank={rank} P{priority} "
                "down={downstream} path={hard_path}".format(**r)
            )
    return 0


def _cmd_simulate(args):
    wis = _load(args.root)
    rounds = simulate(wis, args.jobs)
    if args.format == "json":
        print(json.dumps({"jobs": args.jobs, "rounds": rounds}, indent=2))
        return 0
    if not rounds:
        print("schedule: nothing to schedule")
        return 0
    for i, rnd in enumerate(rounds, 1):
        print("round {:<3} ({}): {}".format(i, len(rnd), " ".join(rnd)))
    return 0


def main(argv=None):
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    sub = ap.add_subparsers(dest="cmd")

    ready = sub.add_parser("ready", help="print the dependency-ready frontier")
    ready.add_argument(
        "--explain", action="store_true", help="show every WI + reason codes"
    )
    ready.add_argument("--format", choices=("text", "json"), default="text")
    ready.set_defaults(func=_cmd_ready)

    sim = sub.add_parser(
        "simulate", help="greedy list-schedule the frontier over N workers"
    )
    sim.add_argument("--jobs", type=int, default=2, help="worker ceiling (default 2)")
    sim.add_argument("--format", choices=("text", "json"), default="text")
    sim.set_defaults(func=_cmd_simulate)

    args = ap.parse_args(argv)
    if not getattr(args, "cmd", None):
        ap.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
