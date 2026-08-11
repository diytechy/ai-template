"""intake.py — the unified trunk-side intake mint (WI-388; docs/concurrency-v2.md §A5.2).

THE INVARIANT THIS MODULE SEALS (rulings R1 + R3, log.md Decisions
2026-08-01): **a WI id is created only by a human trunk commit or this
helper — lanes never mint.** A new id is `max(existing) + 1` over every spec
filename under `docs/work/` (every declared status directory, `active/<branch>/`
included — the id-reservation argument that earned `draft/` its folder, §B3),
and the mint runs only where trunk moves serially: the merge slot
(`integrate.integrate_one`'s post-merge arm) and the idle dispatcher
(`dispatch._station_exit`'s empty-frontier ladder, rung 1). Minting is
deterministic — no model anywhere in the path; a detected event becomes a row
with a **derived** description, so the work is forced into the registry with
nobody watching.

Three triggers, plus the drafts-not-mints arm:

  (a) **the ratified-cell diff on the merged commit** — via
      `check_trajectory.staged_spine_amendments(root, before, after)` (the
      WI-380 seam, consumed as-is). A record mints when it carries a ratified
      change or a ROUTED traced change (`ROUTED_TRACED_CELLS`: `SN-Refs`,
      `Verifies`, and `SR-Refs` — the last ruled traced at WI-388); the other
      traced cells are silent by ruling. One `adjudication` row per merge,
      listing each changed row, cell and before/after — the long form in the
      `## Context` body section, because R-A forbids a filled Deliverable on
      an open row.
  (b) **a merged spec carrying `## Handback`** — the DISPOSITION row (ruling
      R3): same `adjudication` kind, rank 1; its only outcomes are cancel /
      defer / re-queue with a drafted follow-up / surface an open item, and it
      may NEVER itself hand back. The no-recursion invariant is structural at
      both ends: `handback.hand_back` refuses to return an adjudication row,
      and this intake refuses to mint a disposition FOR one.
  (c) **the dispatcher's empty-frontier gap census** — the finding strings
      `dispatch.gap_census` hands over become concrete gap-closure rows with
      derived descriptions, deduped against open rows so the ladder cannot
      mint the same gap forever.
  (d) **drafts-not-mints** — an adjudication row files follow-ups as a
      `## Dispositions` section in its own spec body (one fenced ```toml
      block per draft); intake parses the section and mints them at ITS merge.
      An in-lane mint would trip WI-397's R1 rung at the row's own merge slot,
      which is the invariant working, not an inconvenience.

**Tier signals are measurable, never judged**: rows touched and a moved
`docs/gate` (trigger a), the handback reason class (trigger b), and the census
kind (trigger c) set `buildtier`; deeper review is reached by a drafted
follow-up carrying `planmode = "dual"` — never by a second kind (`arbiter` is
not used as a kind name; the dual-plan arbiter owns that word).

The mint commit mirrors the claim's bookkeeping shape (`integrate._claim_locked`):
regenerate the declared artifacts (RULING-6 — the registry changed, so the
regeneration folds into the same bookkeeping commit), `add -A`, un-stage the
dispatch lock file, then `write-tree`/`commit-tree` onto HEAD. All-or-nothing:
any refusal restores trunk and mints NOTHING, and every derived title is
deterministic (the amendment title carries its sha pair), so a recovery re-run
— `python intake.py sweep --before <sha> --after <sha>` — is idempotent by
exact-title dedup.

Contracts: IF-090, IF-091, IF-092, IF-101, IF-110 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

# Sibling: the spine's registry CARRIER (repo-lock D-5/D-6) — one home for the
# TOML tier tables, the key->column vocabulary and both readers.
try:
    import spine_carrier
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier

import agent_common as ac
import check_trajectory
import schedule
import trace
import wi_convert

SCRIPTS = Path(__file__).resolve().parent
WORK = "docs/work"

# The traced cells that ROUTE to adjudication rather than staying silent
# (§A5.1 for `SN-Refs`/`Verifies`; the WI-388 ruling for LLR `SR-Refs` —
# recorded at check_trajectory.SPINE_TRACED_CELLS, the cell-split table's
# home). Keyed per registry so a same-named column elsewhere never rides in.
ROUTED_TRACED_CELLS = {
    "docs/requirements/system-requirements.toml": frozenset({"SN-Refs"}),
    "docs/requirements/low-level-requirements.toml": frozenset({"SR-Refs"}),
    "docs/test/test-cases.toml": frozenset({"Verifies"}),
}

# The disposition row's face: the R3 outcome vocabulary, verbatim in the title
# so the claiming worker reads its whole authority off the row.
# SR-145 retired R3's `re-queue`: a terminal row is never put back on the
# frontier, so continuing the work means DRAFTING A SUCCESSOR (minted at this
# row's own merge, carrying `supersedes`). `handback._no_recursion_refusal`
# states the same four; the two homes must not disagree about a row's authority.
_DISPOSITION_OUTCOMES = "cancel / defer / draft a successor / surface an open item"

# A fenced TOML draft inside the ## Dispositions section.
_TOML_FENCE_RE = re.compile(r"```toml\s*\n(.*?)```", re.S)
# The keys a drafted follow-up may carry — a typo'd key is a refusal, because
# a silently dropped cell on a row minted with nobody watching is the exact
# failure shape this module exists to close.
_DRAFT_KEYS = frozenset(
    {
        "title",
        "workstream",
        "buildtier",
        "planmode",
        "safety_class",
        "specref",
        "sr_refs",
        "needs",
        "priority",
        "bar",
        # SR-145 lineage: a successor drafted by a disposition names the row it
        # continues, so partial work keeps its thread ACROSS the id change. It
        # is a lineage fact, not a revival — the superseded row stays terminal
        # and its scope stays exactly what it was.
        "supersedes",
    }
)

_WI_FILE_RE = re.compile(r"^WI-(\d+)-.+\.md$")
# SR-144: the per-close reports' home, and the `+++` block inside one. Outside
# `docs/work/` deliberately — `spec_files` rglobs `WI-*.md` there and would walk
# a report, raise on its undeclared directory, then SILENTLY SKIP it while the
# id mint counted it as taken.
REPORTS = "docs/handbacks"
_REPORT_FRONT_RE = re.compile(r"\+\+\+\n(.*?)\n\+\+\+", re.S)
# The folder -> outcome map the by-hand sweep walks. Stated once here rather
# than inlined per loop; `integrate.OUTCOME_DIRS` is its production twin (the
# sweep cannot import the integrator — that arrow runs the other way).
SWEEP_OUTCOMES = {"partial": "partial", "cancelled": "cancelled", "complete": "merged"}
# Clip widths for derived text: one cell value, one census line, one title.
_CELL_CLIP = 120
_LINE_CLIP = 140


def _say(msg, err=False):
    print("intake: {}".format(msg), file=sys.stderr if err else sys.stdout)


def _clip(text, width):
    text = " ".join(str(text).split())
    return text if len(text) <= width else text[: width - 1] + "…"


def next_wi_id(root):
    """`max(watermark, existing) + 1` — the mint counts from the WATERMARK.

    Filenames are still swept, for the same reason they always were (a broader
    read than the loaders: for a MINT, an id held anywhere is an id taken, and
    filenames never lie the way a malformed row can). But the FLOOR is now
    `docs/id-watermark`, because the live tree cannot answer the question that
    matters once D-4 lets a superseded row be DELETED: `max(live) + 1` re-issues
    the number of anything removed, and a reused id silently re-points every
    commit message and archived document that cites it.

    `trace.read_watermark` RAISES when the mark is absent or malformed rather
    than degrading to zero, and that refusal is deliberately not caught here: a
    mint with no record of what has been allocated is the one operation that
    must not proceed on a guess."""
    top = 0
    work = Path(root) / WORK
    if work.is_dir():
        for path in work.rglob("WI-*.md"):
            matched = _WI_FILE_RE.match(path.name)
            if matched:
                top = max(top, int(matched.group(1)))
    mark = trace.read_watermark(root).get("WI", 0)
    return "WI-{:03d}".format(max(top, mark) + 1)


def tier_signal(trigger, *, rows_touched=0, gate_moved=False):
    """`buildtier` from MEASURABLE inputs (the amendment's clause 2): rows
    touched + gate delta for an amendment, the census kind for a gap row.
    Deeper review is a drafted follow-up with `planmode = "dual"`, never a tier
    here and never a second kind.

    THE `handback` ARM IS GONE (SN-031, folding WI-417). It read
    `"NEEDS-HUMAN" in reason.upper()` — a magic substring inside free prose,
    with no constant, no validation and no refusal on a miss, so `NEEDS_HUMAN`
    or `needs human` silently downgraded a disposition's review tier. A close
    now states `suggested_tier` as a TYPED field in its own report, and
    `_close_drafts` reads it there: prose that carries control flow must be a
    typed field."""
    if trigger == "amendment":
        return "strong" if gate_moved or rows_touched > 3 else "medium"
    if trigger == "red-tc":
        # SR-142. One target is a local question (is this TC stale, or
        # was the close optimistic?); several mean the closed row's claim spans
        # requirements, and the judgement has to hold all of them at once. Same
        # shape as the amendment arm — breadth, counted, never judged — with the
        # threshold at 1 rather than 3 because a red TC is already a
        # contradiction, not a routine registry edit.
        return "strong" if rows_touched > 1 else "medium"
    return "medium"  # census gap closure: mechanical registry work


def _existing_titles(root):
    """`{title: status}` over the whole registry (the real loader, malformed
    specs skipped like every reader) — the dedup surface. Exact-title match is
    the idempotence rule: every derived title is deterministic for its event."""
    rows = ac.read_spec_rows(Path(root) / WORK)
    return {r["Title"]: r["Status"] for r in rows if r.get("Title")}


# --- the context block (clause 4): pure registry joins, advisory ---------------

# Bounds, in the pred_block spirit (agent_loop.worker_prompt clips predecessor
# deliverables at 200 chars and the diff at 30/60 lines): per-section item
# caps, per-item clips, and one whole-block line cap at the end.
_SECTION_ITEMS = 6
_BLOCK_LINES = 48
_OPEN = frozenset({"draft", "queued", "active", "deferred"})


# The registry CSV read and the ref-cell splitter are agent_common's
# (`_read_csv_rows`: [] on absent/unreadable, BOM-safe; `_refs`) — imported,
# not copied: intake is not one of the F5 independently-copyable three, so a
# shared reader beats another verbatim copy.
_csv_rows = ac._read_csv_rows
_split = ac._refs


def context_block(root, wi_row, rows=None):
    """The WI-388 context block: what the registries already know about this
    row's neighbourhood, as PURE joins — advisory, NEVER gating (any failure
    answers ""), clipped like `pred_block`. Content order by failure cost:

      1. cancelled precedent sharing `sr_refs`, WITH ITS REASONS — prevents
         re-proposing the refuted (the measured WI-391 failure mode);
      2. pending OIs whose WI-Refs intersect self / predecessors / siblings
         (premise risk);
      3. the LLR/TC decomposition rows with their Module/CodeSymbol/TestRefs
         code map;
      4. LLR.Component -> CMP.Knowledge packs;
      5. IF seams via LLR.Module;
      6. docs/reviews/ records of precedent rows.

    Excluded BY DESIGN: docs/status.md (not a resume surface, WI-210), the OKF
    bundle (generated copy — workers read its sources), and implementer
    self-assessments (review independence).

    Three consumers: written into every minted row's body at mint (minted rows
    have no spec author); computed fresh in `agent_loop.worker_prompt` at
    claim; and the warn-first pack-citation check on hand-authored specs
    (`check_trajectory.knowledge_pack_findings` makes the same
    Component->Knowledge join under its F5 independence)."""
    try:
        return _context_block(Path(root), wi_row or {}, rows)
    except Exception:  # advisory-never-gating: a broken join is no join
        return ""


def _context_block(root, wi_row, rows):
    rows = ac.read_spec_rows(root / WORK) if rows is None else rows
    wid = wi_row.get("WI-ID") or ""
    srs = set(_split(wi_row.get("SR-Refs")))
    preds = {p.lstrip("~") for p in _split(wi_row.get("Predecessors"))}
    cancelled = [
        r
        for r in rows
        if r.get("Status") == "cancelled" and srs & set(_split(r.get("SR-Refs")))
    ]
    siblings = {
        r["WI-ID"]
        for r in rows
        if r.get("WI-ID") != wid
        and r.get("Status") in _OPEN
        and srs & set(_split(r.get("SR-Refs")))
    }
    llrs = [
        r
        for r in spine_carrier.load(
            root / "docs/requirements/low-level-requirements.toml", "LLR-ID"
        )
        if srs & set(_split(r.get("SR-Refs")))
    ]
    sections = [
        (
            "Cancelled precedent on the same SRs (do not re-propose the refuted)",
            [
                "- {} (cancelled) {} — reason: {}".format(
                    r["WI-ID"],
                    _clip(r.get("Title"), 70),
                    _clip(r.get("Deliverable") or "(none recorded)", 160),
                )
                for r in cancelled
            ],
        ),
        (
            "Pending open items whose WI-Refs touch this row's kin (premise risk)",
            _pending_oi_lines(root, {wid} | preds | siblings),
        ),
        (
            "Decomposition code map (LLR/TC on the same SRs)",
            _code_map_lines(root, llrs, srs),
        ),
        (
            "Knowledge packs the touched components declare (read before building)",
            _pack_lines(root, llrs),
        ),
        ("Interface seams via the touched modules", _seam_lines(root, llrs)),
        (
            "Review records of precedent rows",
            _review_lines(root, preds | {r["WI-ID"] for r in cancelled}),
        ),
    ]
    lines = []
    for header, items in sections:
        if items:
            lines += ["### " + header] + items[:_SECTION_ITEMS] + [""]
    if not lines:
        return ""
    body = "Advisory registry joins (WI-388; never gating):\n\n" + "\n".join(lines)
    return ac._clip(body.rstrip("\n"), _BLOCK_LINES)


def _pending_oi_lines(root, kin):
    return [
        "- {} (pending): {}".format(
            o.get("OI-ID"), _clip(o.get("OneLine") or o.get("Title"), 160)
        )
        for o in _csv_rows(root / "docs/requirements/open-items.csv")
        if (o.get("Status") or "").strip().lower() == "pending"
        and kin & set(_split(o.get("WI-Refs")))
    ]


def _code_map_lines(root, llrs, srs):
    lines = [
        "- {} [{} :: {}] tests: {} — {}".format(
            r.get("LLR-ID"),
            r.get("Module") or "?",
            r.get("CodeSymbol") or "?",
            r.get("TestRefs") or "-",
            _clip(r.get("Title"), 60),
        )
        for r in llrs
    ]
    llr_ids = {r.get("LLR-ID") for r in llrs}
    lines += [
        "- {} -> {}".format(t.get("TC-ID"), t.get("Evidence") or "(no evidence yet)")
        for t in spine_carrier.load(root / "docs/test/test-cases.toml", "TC-ID")
        if (srs | llr_ids) & set(_split(t.get("Verifies")))
    ]
    return lines


def _pack_lines(root, llrs):
    comps = {r.get("Component") for r in llrs} - {"", None}
    return [
        "- {} {}: {}".format(
            c.get("CMP-ID"), _clip(c.get("Name"), 40), c.get("Knowledge")
        )
        for c in _csv_rows(root / "docs/requirements/components.csv")
        if c.get("CMP-ID") in comps and (c.get("Knowledge") or "").strip()
    ]


def _seam_lines(root, llrs):
    stems = {
        Path(r.get("Module") or "").stem
        for r in llrs
        if (r.get("Module") or "").strip()
    }
    return [
        "- {} ({}) {} <-> {}: {}".format(
            i.get("IF-ID"),
            i.get("Direction"),
            i.get("ThisProject"),
            i.get("Counterpart"),
            _clip(i.get("Contract"), 110),
        )
        for i in _csv_rows(root / "docs/requirements/interfaces.csv")
        if Path(i.get("ThisProject") or "").name in stems
        or Path(i.get("Counterpart") or "").name in stems
    ]


def _review_lines(root, precedent_ids):
    reviews = root / "docs" / "reviews"
    if not reviews.is_dir():
        return []
    return [
        "- docs/reviews/" + path.name
        for path in sorted(reviews.glob("WI-*.md"))
        if path.name.split("-", 2)[:2] != [] and _review_id(path.name) in precedent_ids
    ]


def _review_id(name):
    matched = re.match(r"^(WI-\d+)-", name)
    return matched.group(1) if matched else ""


# --- trigger (a): the ratified-cell diff on the merged commit ------------------


def _routed_amendments(root, before, after):
    """The amendment records that are adjudication's to judge: a ratified
    change, or a routed traced change (`ROUTED_TRACED_CELLS`). Everything else
    in the traced half is silent by ruling."""
    routed = []
    for rec in check_trajectory.staged_spine_amendments(root, before, after):
        routed_cells = {
            cell: change
            for cell, change in rec["traced"].items()
            # Keyed by the registry STEM: the record names whichever carrier
            # file git reported, and a suffix-keyed miss here would silently
            # reclassify a routed cell as an ordinary amendment (repo-lock D-5).
            if cell
            in {spine_carrier.stem(k): v for k, v in ROUTED_TRACED_CELLS.items()}.get(
                spine_carrier.stem(rec["registry"]), ()
            )
        }
        if rec["ratified"] or routed_cells:
            routed.append(dict(rec, routed=routed_cells))
    return routed


def _gate_moved(root, before, after):
    """Did `docs/gate`'s value move across the merge? Read off the two trees —
    a measurable input, not a judgement; unreadable answers False."""
    values = []
    for rev in (before, after):
        code, out = ac.git(root, "show", "{}:docs/gate".format(rev))
        values.append(out.splitlines()[0].strip() if code == 0 and out else None)
    return values[0] != values[1]


def _amendment_context(records):
    """The derived listing — each changed row, cell, and before/after — the
    §A5.2 'derived description' in its honest home (the advisory `## Context`
    section; R-A forbids a filled Deliverable on an open row)."""
    lines = [
        "Derived from `staged_spine_amendments` on the merged commit (§A5.2).",
        "Ratified and ROUTED traced cells only; other traced cells are silent",
        "by ruling. Each line: registry row / cell: before -> after.",
        "",
    ]
    for rec in records:
        cells = dict(rec["ratified"])
        cells.update(rec["routed"])
        for cell in sorted(cells):
            before, after = cells[cell]
            lines.append(
                "- {} `{}`: {!r} -> {!r}".format(
                    rec["id"],
                    cell,
                    _clip(before, _CELL_CLIP),
                    _clip(after, _CELL_CLIP),
                )
            )
    lines += [
        "",
        "Outcomes (§A5.2): flip rows back to Verified where no scope moved",
        "(per the declared ratification level in docs/process.toml — "
        "recommend-only while the tier is HUMAN-HELD, ruled decision",
        "2), or draft the real scope-change / re-scope / cancellation rows in",
        "a `## Dispositions` section of THIS spec — intake mints them at this",
        "row's merge (drafts-not-mints, R1).",
    ]
    return "\n".join(lines)


def _owning_srs(records):
    """The owning SR ids the amendment touches — the row itself when it is an
    SR; a re-pointed LLR contributes its BEFORE-side owner (the attested one).
    Advisory context for the row's `sr_refs`; bounded and best-effort."""
    srs = set()
    for rec in records:
        if rec["id"].startswith("SR-"):
            srs.add(rec["id"])
        change = rec["routed"].get("SR-Refs")
        if change:
            srs.update(tok.strip() for tok in change[0].split(";") if tok.strip())
    return sorted(srs)[:8]


def _amendment_drafts(root, before, after):
    records = _routed_amendments(root, before, after)
    if not records:
        return []
    ids = sorted({rec["id"] for rec in records})
    title = (
        "adjudicate: {} - ratified/routed cell(s) amended on merged trunk "
        "{}..{} (§A5.2); judge whether scope moved, then flip or draft "
        "follow-ups in ## Dispositions".format(
            ", ".join(ids), str(before)[:7], str(after)[:7]
        )
    )
    return [
        {
            "title": title,
            "kind": "adjudication",
            "brief": "amendment",
            "workstream": "process",
            "buildtier": tier_signal(
                "amendment",
                rows_touched=len(records),
                gate_moved=_gate_moved(root, before, after),
            ),
            "sr_refs": _owning_srs(records),
            "specref": records[0]["registry"],
            "context": _amendment_context(records),
        }
    ]


# --- trigger (b): a merged handback mints the disposition row ------------------


def _closed_spec(root, wi_id, dirs=("partial", "cancelled")):
    """The closed spec's `(relpath, frontmatter)` on the post-merge trunk —
    searched across the terminal directories the CALLER names. None when it
    cannot be found or read.

    The default is the EARLY-close pair on purpose: the disposition arm must
    not find a `complete/` spec and mint an early-close judgement for a clean
    one. The spot-check arm passes `("complete",)` explicitly, so which
    directory a caller means is always written down."""
    for status_dir in dirs:
        hits = sorted((Path(root) / WORK / status_dir).glob(wi_id + "-*.md"))
        for hit in hits:
            try:
                text = hit.read_text(encoding="utf-8")
                meta, _body = ac.parse_spec_frontmatter(
                    text, hit.relative_to(Path(root)).as_posix()
                )
            except (OSError, ValueError, UnicodeDecodeError):
                continue
            return hit.relative_to(Path(root)).as_posix(), meta
    return None


def _close_reports(root, wi_id):
    """Every per-close report on trunk for `wi_id`, newest-name last.

    THE REPORT IS THE EVENT'S IDENTITY (SR-144). Five earlier mechanisms tried
    to answer "is a judgement still owed for THIS close?" by reconstructing the
    event from the closed spec — a mutable, movable, self-referencing object —
    and every one leaked an owed judgement. An immutable document dissolves the
    question: a second close is a second file, and a disposition CITING a file
    is positive provenance rather than an inference."""
    directory = Path(root) / REPORTS
    if not directory.is_dir():
        return []
    return sorted(directory.glob(wi_id + "-*.md"))


def _report_meta(path):
    """One report's frontmatter dict, or `{}` — SAYING SO when the block is
    there but unreadable.

    A quiet `{}` is the WI-417 shape at a new site: `suggested_tier` would fall
    to `medium` and the row's derived text would describe a close it never
    read. Every sibling spec parser raises on a bad fence; this one cannot (a
    mint must not die on one malformed record), so it is loud instead."""
    text = path.read_text(encoding="utf-8", errors="replace")
    match = _REPORT_FRONT_RE.search(text)
    if match is None:
        _say(
            "{} has no +++ frontmatter - the close's typed fields are "
            "unreadable and the disposition falls back to defaults".format(path),
            err=True,
        )
        return {}
    data = ac.read_toml_text(match.group(1))
    if not isinstance(data, dict):
        _say(
            "{}'s +++ frontmatter does not parse as TOML - the close's typed "
            "fields are unreadable and the disposition falls back to "
            "defaults".format(path),
            err=True,
        )
        return {}
    return data


def _close_drafts(root, outcomes):
    """Trigger (b): one disposition row per EARLY CLOSE, keyed off the close's
    own immutable report.

    Every `partial` and `cancelled` close gets a disposition — both carry a
    claim about what was NOT delivered, and a claim is what an adjudicator is
    for. `complete` closes are spot-checked at a declared rate rather than
    gated: the merge slot already ran the declared bar on the composed tree and
    the review rounds already judged the work, so adjudicating every green close
    would rebuild the verdict gate under a new name.

    That last sentence described a dial nothing read for one review round —
    `complete_review` and `complete_sample_rate` were shipped, type-checked and
    consulted by no code, so the promised spot-check happened exactly never.
    `_complete_spot_checks` is its reader.
    """
    drafts = _complete_spot_checks(root, outcomes)
    for wi_id, outcome in sorted(
        (w, o) for w, o in (outcomes or {}).items() if o in ("partial", "cancelled")
    ):
        found = _closed_spec(root, wi_id)
        if found is None:
            _say(
                "{} merged as an early close but its spec is not readable in a "
                "terminal directory - no disposition minted; sweep by "
                "hand".format(wi_id),
                err=True,
            )
            continue
        relpath, meta = found
        if _is_adjudication(meta):
            # The no-recursion invariant, intake end: a disposition row never
            # spawns a disposition row. `close_partial` refuses this shape too;
            # a hand-made close that slipped past still dead-ends HERE.
            _say(
                "{} is an adjudication row closed early - NO disposition row "
                "is minted for it (R3: no recursion); its close is the "
                "owner's to read".format(wi_id),
                err=True,
            )
            continue
        reports = _close_reports(root, wi_id)
        if not reports and outcome == "cancelled":
            # A CANCELLED close needs no report, and asking for one would be
            # asking for a second copy of a record that already exists. The
            # lane's own Deliverable carries the reason (R-A makes that a hard
            # rule, not a convention), and `cancelled/` is terminal, so the
            # SPEC PATH is a sound event identity: a row cancels exactly once.
            # `partial` cannot lean on that — the spec's definition is left
            # byte-identical there, so it says nothing about the close at all.
            drafts.append(
                {
                    "title": (
                        "dispose: the cancellation recorded at {} - {} (a "
                        "disposition row never closes early; R3)".format(
                            relpath, _DISPOSITION_OUTCOMES
                        )
                    ),
                    "kind": "adjudication",
                    # NO `brief`: this arm is report-less by design (above),
                    # and the disposition brief is built around the report. A
                    # row must not declare a brief the kit cannot assemble -
                    # `agent_loop` HOLDS such a row for a human rather than
                    # dispatching it, which is right for a real gap and wrong
                    # for a close that never owed a report.
                    "workstream": "process",
                    "buildtier": "medium",
                    "specref": relpath,
                    "context": _cancel_context(relpath),
                }
            )
            continue
        if not reports:
            # F6: suppression must never be silent. A terminal spec whose close
            # report is missing (hand-deleted, renamed, or never written) has
            # an owed judgement nobody is holding — exactly the starvation this
            # contract exists to end — so it says so rather than minting zero
            # rows quietly.
            _say(
                "{} is closed in {} but NO per-close report exists at {}/{}-*.md "
                "- the close event has no record, so no disposition was minted. "
                "Write the report (or re-run the close) and sweep "
                "again".format(wi_id, relpath, REPORTS, wi_id),
                err=True,
            )
            continue
        for report in reports:
            rel_report = report.relative_to(Path(root)).as_posix()
            rmeta = _report_meta(report)
            tier = str(rmeta.get("suggested_tier") or "medium")
            if tier not in ("quick", "medium", "strong"):
                tier = "medium"
            drafts.append(
                {
                    # THE REPORT PATH is the title's event token. It is stable
                    # (an immutable document never moves) and unique per close,
                    # which is what makes exact-title dedup CORRECT here: a
                    # re-run dedupes exactly, and a genuinely second close is a
                    # second report and so a second row. No sha, no digest, no
                    # archaeology.
                    # THE TITLE KEYS ON THE REPORT PATH AND NOTHING ELSE.
                    # `_mint` dedups on the exact title, so every token in it
                    # is part of the event's identity — and the report path is
                    # the only one that cannot move: the file is immutable and
                    # its name is `<wi>-<branch>`. An earlier cut folded the
                    # report's `claimed_outcome` in as well, which re-read a
                    # MUTABLE field on every sweep, so one edit to a report
                    # minted a second disposition for the same close. That is
                    # the F1/F2 starvation class returning through a new proxy;
                    # the outcome belongs in the Context, where nothing dedups.
                    "title": (
                        "dispose: the close recorded at {} - {} (a disposition "
                        "row never closes early; R3)".format(
                            rel_report, _DISPOSITION_OUTCOMES
                        )
                    ),
                    "kind": "adjudication",
                    "brief": "disposition",
                    "workstream": "process",
                    # The TYPED field, not a substring of prose (SR-145 / the
                    # `NEEDS-HUMAN` fold): the close states the tier it thinks
                    # its judgement needs, and a value outside the vocabulary
                    # falls to `medium` rather than silently to whatever a
                    # case-folded search happened to match.
                    "buildtier": tier,
                    "specref": relpath,
                    "context": _close_context(relpath, rel_report),
                }
            )
    return drafts


def _merged_ids(outcomes):
    """The WI ids this merge closed CLEANLY, sorted — the one read of the
    outcomes map three arms make."""
    return sorted(w for w, o in (outcomes or {}).items() if o == "merged")


def _judgeable_close(root, wi_id, dirs):
    """The closed spec's relpath when a disposition may judge it, else None.

    Two conditions, and the second is R3's no-recursion invariant at the intake
    end: a disposition row never spawns a disposition row. `close_partial`
    refuses that shape at the other end too, so a hand-made close that slipped
    past still dead-ends here. Written once because both arms — the early-close
    disposition and the clean-close spot check — owe exactly this pair, and
    WI-347 rules an intra-file copy a defect however small."""
    found = _closed_spec(root, wi_id, dirs=dirs)
    if found is None:
        return None
    relpath, meta = found
    return None if _is_adjudication(meta) else relpath


def _is_adjudication(meta):
    """Whether a spec's frontmatter declares the adjudication kind — R3's
    no-recursion test, read off the same cell `schedule.classify` reads."""
    return (meta.get("safety_class") or "").strip().lower() == "adjudication"


def _complete_spot_checks(root, outcomes):
    """Disposition drafts for CLEAN closes, per `[attestation] complete_review`.

    `"off"` -> none. `"always"` -> every one. `"sample"` -> a DETERMINISTIC
    every-Nth over the sorted ids, not a random draw: a walk-away loop must
    produce the same registry from the same inputs, and a sampler nobody can
    reproduce is one nobody can audit. The id's own numeric tail is the
    selector, so which closes get checked does not depend on how many landed in
    one merge.

    The brief is deliberately thinner than the partial/cancelled one: there is
    no claim under judgement here. The question is only whether the shipped
    work matches what the row asked for — a spot-check, not an adjudication of
    a failure."""
    mode, rate = ac.complete_review(Path(root) / "docs")
    if mode == "off":
        return []
    drafts = []
    for wi_id in _merged_ids(outcomes):
        digits = "".join(ch for ch in wi_id if ch.isdigit())
        if mode == "sample" and (not digits or int(digits) % rate):
            continue
        judgeable = _judgeable_close(root, wi_id, ("complete",))
        if judgeable is None:
            continue
        relpath = judgeable
        drafts.append(
            {
                "title": (
                    "spot-check the clean close of {} - does the shipped work "
                    "match what the row asked for? ({})".format(
                        wi_id, _DISPOSITION_OUTCOMES
                    )
                ),
                "kind": "adjudication",
                # NO `brief`, for the cancellation arm's reason: a GREEN close
                # writes no report, so the disposition brief cannot be built
                # for it and the kit ships no "spot-check a clean close"
                # template. Declaring one would be a claim the assembler
                # cannot honour.
                "workstream": "process",
                "buildtier": "medium",
                "specref": relpath,
                "context": (
                    "This close was GREEN: the merge slot ran the declared bar "
                    "on the composed tree and the review rounds judged the "
                    "work. Nothing is alleged. It is here because "
                    "`docs/process.toml [attestation] complete_review` is "
                    "{mode!r}, and a process that only ever looks at its "
                    "failures learns nothing about its successes.\n\n"
                    "Read `{spec}` and ask ONE question: does what shipped "
                    "answer what the row asked for? A finding is a successor "
                    "row, never a reversal — the close stands."
                ).format(mode=mode, spec=relpath),
            }
        )
    return drafts


def _cancel_context(relpath):
    """The minted row's `## Context` for a CANCELLED close.

    Like its `partial` sibling it does not quote the lane: a judge's brief must
    not open with the defendant's verdict, and here the verdict IS the
    Deliverable. It is one `Read:` away."""
    return (
        "The cancelled spec is `{spec}` — READ ITS `## Deliverable` FIRST. That "
        "cell is where the lane recorded why this will never be built, and it "
        "is a CLAIM under judgement here, not this row's premise.\n\n"
        "Outcomes (R3): {outcomes}. An override moves the byte-identical spec "
        "to the corrected terminal folder and records the overridden claim; the "
        "cancellation itself is never reversed in place. An open item goes to "
        "docs/requirements/open-items.csv."
    ).format(spec=relpath, outcomes=_DISPOSITION_OUTCOMES)


def _close_context(relpath, rel_report):
    """The minted row's `## Context`. It names the report and STOPS.

    Deliberately free of the closing lane's own words. A judge's brief must not
    open with the defendant's verdict — that was measured: a returned spec's
    reason was clipped into the disposition's Context, so the adjudication began
    by reading the lane's own conclusion, truncated mid-word. The report is one
    `Read:` away and carries every typed field; quoting it here would buy
    nothing and cost the judgement's independence."""
    return (
        "The closed spec is `{spec}`.\n\n"
        "Its per-close report is `{report}` — READ IT FIRST. The report is the "
        "close EVENT's own immutable record: what the lane claims it delivered "
        "and did not, the commit range, the keep/discard split, and the review "
        "tier it suggests. The lane's claimed outcome is a CLAIM under "
        "judgement here, not this row's premise.\n\n"
        "Outcomes (R3): {outcomes}. Continuing the work MINTS A SUCCESSOR "
        "(drafted in THIS row's `## Dispositions` section, carrying "
        "`supersedes`), never a revival of the closed row — a closed row is "
        "never re-opened and a scope definition never changes to mean "
        "something else. An override moves the byte-identical spec to the "
        "corrected terminal folder; the report stays on record as the claim it "
        "was. An open item goes to docs/requirements/open-items.csv."
    ).format(spec=relpath, report=rel_report, outcomes=_DISPOSITION_OUTCOMES)


# --- drafts-not-mints: the ## Dispositions section -----------------------------


def parse_dispositions(text, where):
    """`(drafts, refusal)` — the `## Dispositions` section's fenced TOML
    blocks, validated. A malformed block is a REFUSAL, never a skip: a ruled
    follow-up silently dropped by a mint running with nobody watching is the
    exact loss this module exists to prevent (recovery: fix the completed spec
    trunk-side, then `python intake.py sweep`)."""
    _, sep, tail = text.partition("\n## Dispositions")
    if not sep:
        return [], None
    section = tail.split("\n## ", 1)[0]
    blocks = _TOML_FENCE_RE.findall(section)
    if not blocks:
        return [], (
            "{}: a ## Dispositions section with no ```toml draft block - "
            "nothing minted".format(where)
        )
    drafts = []
    for index, block in enumerate(blocks, 1):
        try:
            data = tomllib.loads(block)
        except tomllib.TOMLDecodeError as exc:
            return [], (
                "{}: ## Dispositions block {} is not valid TOML ({}) - "
                "nothing minted".format(where, index, exc)
            )
        refusal = _draft_refusal(data, where, index)
        if refusal:
            return [], refusal
        draft = {key: data.get(key) for key in _DRAFT_KEYS if key in data}
        draft["kind"] = draft.pop("safety_class", "") or (
            "" if draft.get("planmode") == "dual" else "ordinary"
        )
        drafts.append(draft)
    return drafts, None


def _draft_refusal(data, where, index):
    """One drafted follow-up's validation — loud on anything a mint with
    nobody watching would otherwise mis-file."""
    at = "{}: ## Dispositions block {}".format(where, index)
    unknown = sorted(set(data) - _DRAFT_KEYS)
    if unknown:
        return "{} carries unknown key(s) {} - nothing minted".format(at, unknown)
    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        return "{} carries no non-empty string title - nothing minted".format(at)
    declared = str(data.get("safety_class") or "").strip().lower()
    if declared == "adjudication":
        return (
            "{} declares safety_class = adjudication - deeper review is a "
            "drafted follow-up with planmode = dual, NEVER a second "
            "adjudication row; nothing minted".format(at)
        )
    if declared and declared not in schedule.SAFETY_CLASSES:
        return "{} declares unknown safety_class {!r} - nothing minted".format(
            at, declared
        )
    dual = str(data.get("planmode") or "").strip().lower() == "dual"
    if dual and declared and declared != "high-risk":
        return (
            "{} declares planmode = dual beside safety_class = {!r} - the "
            "kind is DERIVED from the dual signal (single-source); drop the "
            "cell; nothing minted".format(at, declared)
        )
    bar = str(data.get("bar") or "").strip().upper()
    if bar and bar not in ("G1", "G2", "G3"):
        return "{} declares bar = {!r} (G1|G2|G3) - nothing minted".format(
            at, data.get("bar")
        )
    return None


def _disposition_drafts(root, outcomes):
    """Trigger (d): drafts from every MERGED adjudication row's spec body."""
    drafts = []
    for wi_id in _merged_ids(outcomes):
        hits = sorted((Path(root) / WORK / "complete").glob(wi_id + "-*.md"))
        for hit in hits:
            relpath = hit.relative_to(Path(root)).as_posix()
            try:
                text = hit.read_text(encoding="utf-8")
                meta, _body = ac.parse_spec_frontmatter(text, relpath)
            except (OSError, ValueError, UnicodeDecodeError):
                continue
            if (meta.get("safety_class") or "").strip().lower() != "adjudication":
                continue
            parsed, refusal = parse_dispositions(text, relpath)
            if refusal:
                return [], refusal
            for draft in parsed:
                draft.setdefault("specref", relpath)
                draft.setdefault("workstream", meta.get("workstream") or "process")
                draft.setdefault("buildtier", "medium")
                draft["context"] = (
                    "Drafted by {} (its ## Dispositions section) and minted at "
                    "its merge - drafts-not-mints, ruling R1/R3.".format(wi_id)
                )
                drafts.append(draft)
    return drafts, None


# --- trigger (c): the gap census ----------------------------------------------

# census line -> the registry file that is the gap's spec-of-record (R-E wants
# an in-repo file). Ordered probes; first existing wins, SR registry fallback.
_CENSUS_SPECREFS = (
    ("SN", "docs/requirements/stakeholder-needs.toml"),
    ("LLR-", "docs/requirements/low-level-requirements.toml"),
    ("TC-", "docs/test/test-cases.toml"),
)
_SR_CSV = "docs/requirements/system-requirements.toml"
_TC_CSV = "docs/test/test-cases.toml"


def _live_registry(root, rel):
    """`rel` under whichever carrier the repo actually holds, or "".

    These are EXISTENCE PROBES (first existing wins), which is the one place a
    literal suffix is fatal: a `.toml`-only probe finds nothing in a repo still
    on CSV, every gap row is minted with an EMPTY SpecRef, and `integrate`
    refuses the branch for carrying no spec-of-record — a mint that fails at
    merge instead of at authoring (repo-lock D-5)."""
    suffixes = (
        spine_carrier.NEED_CARRIERS if "stakeholder-needs" in rel else None
    ) or spine_carrier.CARRIERS
    live = spine_carrier.resolve(Path(root) / rel, suffixes)
    return spine_carrier.stem(rel) + live.suffix if live is not None else ""


def _census_specref(root, line):
    for token, rel in _CENSUS_SPECREFS:
        if line.startswith(token) or token in line.split(" ", 1)[0]:
            live = _live_registry(root, rel)
            if live:
                return live
    return _live_registry(root, _SR_CSV)


def _census_drafts(root, census):
    # Dedup against EVERY row, open or terminal: a gap row that closed without
    # clearing its gap must not re-mint on the next idle tick (the walk-away
    # loop would otherwise mint the same gap forever) — re-opening a gap whose
    # row failed is a judgement, so it stays a human trunk commit.
    import dispatch

    titles = _existing_titles(root)
    drafts = []
    for line in census:
        red = dispatch.parse_red_tc(line)
        if red is not None:
            draft = _red_tc_draft(root, line, red[1])
        else:
            draft = {
                "title": "close registry gap: {}".format(_clip(line, _LINE_CLIP)),
                "kind": "ordinary",
                "workstream": "registry",
                "buildtier": tier_signal("census"),
                "specref": _census_specref(root, line),
                "context": (
                    "Minted from the dispatcher's empty-frontier gap census "
                    "(ladder rung 1, §A4 amendment): the registries name this "
                    "gap and the frontier is empty, so the closure becomes a "
                    "concrete row. The census line, verbatim:\n\n"
                    "> {}".format(line)
                ),
            }
        if draft["title"] in titles:
            continue
        drafts.append(draft)
    return drafts


def _red_tc_draft(root, line, targets):
    """SR-142: a red TC under a claimed implementation becomes an
    ADJUDICATION row, not an ordinary gap-closure row.

    The difference is who decides. An ordinary gap row says "the registry is
    missing a link; go add it" — mechanical, medium tier, mint and go. A red TC
    says something stronger and unresolved: a work item is CLOSED and the test
    for it is not green. That is one of three quite different situations — the
    TC is stale and its Status simply owes an update; the close was optimistic
    and owes a fix-to-green successor; or the requirement moved and the TC is
    now testing the wrong thing — and picking between them is a judgement, which
    is exactly what the `adjudication` kind is for.

    The tier is ESTIMATED rather than defaulted (§4 rung 1's "estimator"): the
    breadth of the contradiction is what makes it expensive to judge, and that
    is countable — `targets` comes from `dispatch.parse_red_tc`, the one reader
    of the census grammar, never from re-splitting this line's prose.

    NO `planmode` CELL, and the reason is a defect this row shipped with for
    exactly one review round: `planmode = "dual"` beside `safety_class =
    "adjudication"` is a shape `schedule.classify` REFUSES — it reads
    `unclassified`, drops off the frontier, and can never be re-minted because
    exact-title dedup has already claimed the title. The contradiction SR-142
    exists to surface would have been minted and then permanently
    parked, silently. `_draft_refusal` already refused that pair for a HUMAN
    draft; the automated mint went straight to `_draft_row` and bypassed it,
    which is why `_mint` now runs every draft past `_mint_shape_refusal`."""
    return {
        # Keyed on the census line, like every derived title: it is
        # deterministic for the (TC, targets, status) event, so a re-run
        # dedupes exactly and a status change is legitimately a new judgement.
        "title": "adjudicate {}".format(_clip(line, _LINE_CLIP)),
        "kind": "adjudication",
        "brief": "red-tc",
        "workstream": "process",
        "buildtier": tier_signal("red-tc", rows_touched=len(targets)),
        "specref": _live_registry(root, _TC_CSV),
        "context": _red_tc_context(line, targets),
    }


def _red_tc_context(line, targets):
    """The judge's brief for a red TC. Names the contradiction and the three
    live readings WITHOUT choosing between them — a brief that pre-selects an
    outcome is not a brief."""
    return (
        "The dispatcher's census found a TEST CASE that is not green while the "
        "work claiming to satisfy it is CLOSED. The census line, verbatim:\n\n"
        "> {line}\n\n"
        "Read `{tc}` for the TC row and the `docs/work/complete/` (or "
        "`partial/`) spec of whichever row cites {targets} — the contradiction "
        "is between those two documents and nothing here has judged it.\n\n"
        "Three readings are live and this row does not pick one: (1) the TC's "
        "Status is merely STALE and owes an update — the evidence is green and "
        "the registry is behind; (2) the close was OPTIMISTIC and owes a "
        "fix-to-green successor row (draft it with `supersedes` naming the "
        "closed row, so the thread survives the id change); (3) the "
        "REQUIREMENT moved and the TC now verifies the wrong thing, which is "
        "an amendment, not a bug. Say which, and why, before proposing work."
    ).format(line=line, tc=_TC_CSV, targets=";".join(targets) or "its targets")


# --- the mint itself -----------------------------------------------------------


def _draft_row(wi_id, draft):
    """One draft as the 18-column registry row `wi_convert.write_spec_file`
    materializes. Status is the DIRECTORY (queued); Deliverable stays empty
    (R-A: open rows carry none); blockref stays empty on adjudication rows —
    they are WORK, not decision briefs."""
    row = {column: "" for column in wi_convert.COLUMNS}
    row["WI-ID"] = wi_id
    row["Title"] = str(draft["title"]).strip()
    row["Status"] = "queued"
    row["Workstream"] = str(draft.get("workstream") or "")
    row["BuildTier"] = str(draft.get("buildtier") or "")
    row["SpecRef"] = str(draft.get("specref") or "")
    row["SafetyClass"] = str(draft.get("kind") or "")
    row["Brief"] = str(draft.get("brief") or "")
    row["PlanMode"] = str(draft.get("planmode") or "")
    row["Bar"] = str(draft.get("bar") or "").upper()
    row["SR-Refs"] = ";".join(draft.get("sr_refs") or [])
    row["Predecessors"] = ";".join(draft.get("needs") or [])
    if draft.get("priority") is not None:
        row["Priority"] = str(draft["priority"])
    return row


def _mint_shape_refusal(draft, subject_verb):
    """Refuse a draft this mint would write as an UNSCHEDULABLE row.

    THE GAP THIS CLOSES. `_draft_refusal` validates follow-ups a human wrote
    into a `## Dispositions` block, and it is thorough. Every DERIVED draft —
    the amendment row, the disposition rows, the census rows — went straight to
    `_draft_row` and was validated by nothing, so the one shape that mattered
    got through: `planmode = "dual"` beside `safety_class = "adjudication"`
    reads `unclassified` at `schedule.classify`, drops off the frontier, and
    exact-title dedup then guarantees it is never minted again. A row minted
    with nobody watching and quarantined with nobody watching is worse than one
    never minted, because the census reports the gap as handled.

    So the mint checks the two properties a row must have to be WORK AT ALL:
    a kind the scheduler classifies, and no kind/planmode contradiction. This
    is deliberately narrower than `_draft_refusal` — it is the floor every
    minted row must clear, not the full grammar a hand-authored block owes."""
    kind = str(draft.get("kind") or "").strip().lower()
    if kind and kind not in schedule.SAFETY_CLASSES:
        return (
            "{}: draft {!r} declares unknown safety_class {!r} - nothing minted".format(
                subject_verb, draft.get("title"), kind
            )
        )
    dual = str(draft.get("planmode") or "").strip().lower() == "dual"
    if dual and kind and kind != "high-risk":
        return (
            "{}: draft {!r} declares planmode = dual beside safety_class = "
            "{!r} - schedule.classify reads that pair as UNCLASSIFIED, so the "
            "row would be minted and then permanently parked off the "
            "frontier; nothing minted".format(subject_verb, draft.get("title"), kind)
        )
    return None


def _mint(root, drafts, subject_verb):
    """Write every draft as a queued spec, then ONE bookkeeping commit.
    `([(wi_id, relpath)], refusal)`; all-or-nothing — a refusal restores trunk
    and reports zero minted."""
    root = Path(root)
    registry = ac.read_spec_rows(root / WORK)
    titles = {r["Title"] for r in registry if r.get("Title")}
    drafts = [d for d in drafts if str(d["title"]).strip() not in titles]
    if not drafts:
        return [], None
    for draft in drafts:
        refusal = _mint_shape_refusal(draft, subject_verb)
        if refusal:
            return [], refusal
    minted = []
    for draft in drafts:
        wi_id = next_wi_id(root)
        row = _draft_row(wi_id, draft)
        try:
            rel = wi_convert.write_spec_file(root / WORK, row)
        except wi_convert.ConvertError as exc:
            ac.git(root, "reset", "--hard", "HEAD")
            ac.git(root, "clean", "-fd", "--", WORK)
            return [], "the mint could not write {}: {}".format(wi_id, exc)
        path = root / WORK / rel
        # The trigger's derived context, then the registry joins (clause 4,
        # consumer 1: minted rows have no spec author, so the block is written
        # at mint — advisory, and computed over the pre-mint registry).
        context = str(draft.get("context") or "").rstrip("\n")
        joins = context_block(root, row, registry)
        if joins:
            context = (context + "\n\n" if context else "") + joins
        if context:
            with path.open("a", encoding="utf-8", newline="\n") as fh:
                fh.write("\n## Context\n\n" + context + "\n")
        minted.append((wi_id, (Path(WORK) / rel).as_posix()))
    # RAISE THE MARK IN THE SAME COMMIT that files the specs. A mint that
    # allocates an id without recording it leaves the mark behind the tree, and
    # trace.py's integrity pass reads that as "an id was allocated past the
    # mark" — correctly, because it was. Safe against a later refusal: the
    # restore path is `git reset --hard HEAD`, whole-tree, so a bump written
    # before a refusal is reverted with the spec it was minted for.
    trace.bump_watermark(root)
    refusal = _bookkeeping_commit(
        root,
        "mint: {} - {} (WI-388 intake; bookkeeping)".format(
            ";".join(w for w, _ in minted), subject_verb
        ),
    )
    if refusal:
        return [], refusal
    for wi_id, rel in minted:
        _say("minted {} at {}".format(wi_id, rel))
    return minted, None


def _bookkeeping_commit(root, subject):
    """The claim-shaped bookkeeping commit (`integrate._claim_locked`'s write
    sequence, without the branch cut): regenerate the declared artifacts (the
    registry changed — RULING-6 folds regeneration into the bookkeeping lane),
    stage everything but the dispatch lock file, and commit via
    write-tree/commit-tree onto HEAD. A refusal restores trunk."""
    import subprocess

    def restore(reason, detail):
        ac.git(root, "reset", "--hard", "HEAD")
        ac.git(root, "clean", "-fd", "--", WORK)
        return "the intake mint {} (trunk restored):\n{}".format(
            reason, ac._failure_tail(detail)
        )

    proc = subprocess.run(
        [
            str(ac.harness_python(root)),
            str(SCRIPTS / "trunk_step.py"),
            "--root",
            ".",
            "--regen",
        ],
        cwd=str(root),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        return restore("regeneration failed", (proc.stdout or "") + (proc.stderr or ""))
    ac.git(root, "add", "-A")
    ac.git(
        root,
        "reset",
        "-q",
        "--",
        ac.dispatch_lock_path(root).relative_to(root).as_posix(),
    )
    code, tree = ac.git(root, "write-tree")
    if code != 0 or not tree.strip():
        return restore("could not name its tree", tree)
    code, commit = ac.git(
        root,
        "commit-tree",
        tree.strip(),
        "-p",
        ac.head_sha(root),
        "-m",
        "{}\n\nThe WI-388 unified intake mint (docs/concurrency-v2.md §A5.2; rulings\nR1/R3): a WI id is created only by a human trunk commit or this helper -\nlanes never mint. Derived description, no model in the path; the\nregeneration folds in per RULING-6.".format(
            subject
        ),
    )
    if code != 0 or not commit.strip():
        return restore("could not write its commit", commit)
    code, out = ac.git(root, "reset", "--hard", commit.strip())
    if code != 0:
        return "the intake mint commit {} exists but trunk did not advance:\n{}".format(
            commit.strip()[:10], ac._failure_tail(out)
        )
    return None


def intake_after_merge(root, before, after, outcomes=None, branch=""):
    """THE MERGE-SLOT ARM: triggers (a), (b) and (d) for one landed merge.
    `([(wi_id, relpath)], refusal)`. Serial by construction — the caller is
    `integrate.integrate_one`, inside the held slot. All-or-nothing: any
    refusal mints nothing (the merge itself STANDS; recovery is a trunk-side
    fix plus `python intake.py sweep --before {before} --after {after}`)."""
    drafts = _amendment_drafts(root, before, after)
    drafts += _close_drafts(root, outcomes)
    disposition, refusal = _disposition_drafts(root, outcomes)
    if refusal:
        return [], refusal
    drafts += disposition
    label = "intake at merge of {}".format(branch or str(after)[:7])
    return _mint(root, drafts, label)


def mint_gap_rows(root, census):
    """THE DISPATCHER'S RUNG-1 ARM (trigger c): the gap census, minted as
    concrete gap-closure rows. `([(wi_id, relpath)], refusal)`; an empty
    answer with a non-empty census means every gap already has an open row."""
    return _mint(root, _census_drafts(root, census), "empty-frontier gap census")


# --- CLI: the recovery / by-hand path ------------------------------------------


def _cmd_sweep(args):
    """Re-run the intake for a landed merge (idempotent by exact-title dedup):
    trigger (a) over --before/--after when given, plus a scan for handed-back
    specs owed a disposition and merged adjudication rows owed their drafted
    follow-ups."""
    root = Path(args.root).resolve()
    outcomes = {}
    # THE WI-413 FIX, and the reason that row cancels as superseded rather than
    # being built. The bare sweep used to scan open directories for a
    # `## Handback` section and tokenize the disposition title with the CURRENT
    # head — so a still-marked returned spec re-minted a duplicate disposition
    # on EVERY run. There is no token to get wrong now: a close is a REPORT, an
    # immutable file, and `_close_drafts` titles the disposition with that
    # file's path. Sweeping twice produces the same title twice and the mint's
    # exact-title dedup answers it; a genuinely second close is a second report
    # and so a second row.
    # One walk over the three TERMINAL folders, not one loop per outcome: the
    # only thing that differs is the folder -> outcome name, which
    # `integrate.OUTCOME_DIRS` already states once.
    for status_dir, outcome in sorted(SWEEP_OUTCOMES.items()):
        directory = root / WORK / status_dir
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("WI-*.md")):
            matched = _WI_FILE_RE.match(path.name)
            if matched:
                outcomes["WI-" + matched.group(1)] = outcome
    before = args.before or "HEAD"
    after = args.after or "HEAD"
    minted, refusal = intake_after_merge(root, before, after, outcomes)
    return _cli_result(refusal, "sweep minted {} row(s).".format(len(minted)))


# --- the gate-policy arms (ruled decision 2, owner 2026-07-31; §A8) ------------


def adjudication_action(human_held):
    """May adjudication FLIP `Modified` -> `Verified`? Ruled decision 2, re-keyed
    onto SN-029's ordinal: **recommend-only while the tier is HUMAN-HELD** — the
    flip is a Status change that RECOVERS THE GATE, i.e. a ratification, and a
    human-held tier's ratification is the human's act, so adjudication prepares
    the brief ("these cells are traced-only, no scope moved, recommend
    re-verify") and stops; **flip once the tier is loop-held**, where a recorded
    LLM verdict already carries ratification authority.

    Anything unreadable upstream resolves to human-held — `agent_common.
    human_holds` fails that way deliberately — so the failure direction is
    `recommend`, never a machine ratification. The kit DEFAULT holds every tier
    even though this repo holds none, which is why both arms are built and
    tested."""
    return "recommend" if human_held else "flip"


def flip_verified(root, ids):
    """Enact — or recommend — the adjudication row's cheap outcome for spine
    rows judged no-scope-moved: `Modified` -> `Verified`. Returns
    `(action, flipped_ids, refusal)`.

    The policy is read from `docs/gate-policy`, never passed by hand (the
    dial's one home). Under `recommend` NOTHING is touched and the prepared
    brief prints — the adjudication worker writes it into its spec and the
    open-items card carries the Modified rows to the sitting. Under `flip`
    only the named rows' Status cells move; every other cell of every row
    stays CELL-exact (and the live registries byte-identical — measured:
    their quoting is all by necessity, which QUOTE_MINIMAL reproduces), a
    row already past `Modified` is skipped (idempotent), and an unknown id
    refuses — a typo on a mechanical tool must never half-apply. The flipped
    registry still owes its regeneration (`derive_gate` recovers the gate);
    the lane's own refresh runs it."""
    root = Path(root)
    # SN-028: the mixed-config refusal, at the third entry point that reads
    # policy without passing through agent_loop.main. This arm decides whether
    # an LLM verdict carries RATIFICATION authority, so it is the last place
    # a half-migrated config should be resolved by precedence.
    conflicts = ac.config_conflicts(root / "docs")
    if conflicts:
        return "recommend", [], conflicts[0]
    # SN-029: the ordinal comparison, not the retired enum. `spine_stage_of`
    # reads the tier currently in process off the generated docs/gate basis
    # line; `human_holds` compares it against `human_ratification_through`.
    human_held = ac.human_holds(root / "docs", ac.spine_stage_of(root))
    level = "human-held" if human_held else "loop-held"
    action = adjudication_action(human_held)
    wanted = {i.strip() for i in ids if i.strip()}
    located, tables = _locate_spine_rows(root, wanted)
    missing = sorted(wanted - set(located))
    if missing:
        return (
            action,
            [],
            "row id(s) {} exist in no spine registry - nothing was flipped".format(
                ", ".join(missing)
            ),
        )
    if action == "recommend":
        for rid in sorted(wanted):
            _say(
                "recommend re-verify: {} (Status={}) - judged no-scope-moved; "
                "under gate-policy '{}' the flip is the human's (ruled "
                "decision 2). Write this brief into the adjudication row's "
                "spec; the open-items card carries the Modified rows.".format(
                    rid, located[rid][1], level
                )
            )
        return action, [], None
    flipped = _apply_flips(root, tables, located)
    # THE ANCHOR IS STILL OWED HERE (docs/repo-lock.md D-1). The flip and the
    # record of WHAT TEXT was blessed have to be one act: a ratification whose
    # anchor is written later is a window in which the registry says `Verified`
    # and nothing says what it agreed to. The ledger append that used to sit on
    # this line is retired with `attestations.csv`; the on-row anchor replacing
    # it waits on the carrier ruling (OI-12). Until then the flip stands alone
    # and the baseline degrades to the git walk `trace._attested_baseline` has
    # always fallen back to — which is where it stood before SN-029, since the
    # ledger never held a row.
    for rid in flipped:
        _say("flipped {} Modified -> Verified (gate-policy '{}')".format(rid, level))
    return action, flipped, None


def _locate_spine_rows(root, wanted):
    """`({id: (registry rel, status, row, status_ix)}, {registry rel: rows})`
    over the three spine registries — ONE parse, shared by the brief and the
    flip (under the CSV carrier the row objects are the live lists the rewrite
    mutates, so nothing scans twice).

    CARRIER-AWARE (repo-lock D-5). Each registry resolves to whichever of
    TOML/CSV is live, and the two carriers report differently because they are
    written differently: a CSV row is a mutable list plus the column index the
    rewrite pokes, while a TOML table is rewritten by LINE and needs neither.
    `row`/`status_ix` are None on the TOML arm, and `tables` holds the live
    path so the writer never re-guesses the suffix."""
    import csv

    located, tables = {}, {}
    for rel, id_col in check_trajectory.SPINE_CSVS:
        live = spine_carrier.resolve(root / rel)
        if live is None:
            continue
        tables[rel] = (live, None)
        if live.suffix == ".toml":
            for row in spine_carrier.load(live, id_col):
                rid = (row.get(id_col) or "").strip()
                if rid in wanted:
                    # ABSENT status is None, not "". Under this carrier an absent
                    # key is a real state, and it is not "not Modified": a row
                    # with no Status at all cannot be re-verified, and treating
                    # it as an idempotent no-op reports a clean adjudication over
                    # a row the registry never staged for one. `_apply_flips`
                    # refuses it (repo-lock D-5; fail closed).
                    status = row.get("Status")
                    located[rid] = (
                        rel,
                        None if status is None else status.strip(),
                        None,
                        None,
                    )
            continue
        with live.open(newline="", encoding="utf-8-sig") as fh:
            rows = list(csv.reader(fh))
        tables[rel] = (live, rows)
        header = rows[0] if rows else []
        status_ix = header.index("Status") if "Status" in header else None
        for row in rows[1:]:
            rid = row[0].strip() if row else ""
            if rid in wanted and status_ix is not None and len(row) > status_ix:
                located[rid] = (rel, row[status_ix].strip(), row, status_ix)
    return located, tables


# The one key this module ever writes on a spine row. Named rather than inlined
# because the carrier's key and the column name differ, and a rewrite that
# targets the wrong one is a no-op that reports success.
_STATUS_KEY = "status"


_TOML_MULTILINE = ('"""', "'''")


def _multiline_delims(text):
    """How many multi-line-string delimiters this line opens or closes, per
    delimiter kind — the minimum TOML awareness a line rewrite needs.

    Counted on the whole line, comment text included: a delimiter inside a `#`
    comment is not a string opener, but a `#` inside a string IS just text, and
    of the two ways to be wrong only treating a delimiter as significant is
    safe. An ODD count toggles the state; an even one — opened and closed on the
    same line, which is how a single-line triple-quoted cell reads — does not.
    """
    return {d: text.count(d) for d in _TOML_MULTILINE}


def _flip_status_lines(lines, table, rid):
    """Rewrite `[<table>.<rid>]`'s `status = ...` line to `Verified`, in place.
    True when a line moved. A LINE REWRITE ON `bootstrap.set_process_key`'s
    PATTERN, and for its reasons (repo-lock D-5 step 4): stdlib has no TOML
    writer, and re-serialising the registry to change one cell would normalise
    away every comment and the file's authored ordering — a whole-file diff for
    a one-word act, on the registry whose diffs the amendment guard reads.

    IT TRACKS MULTI-LINE STRING STATE, and that is not defensive tidiness — it
    is the difference between a ratification and a corruption. The spine's prose
    cells are `\"\"\"...\"\"\"` blocks that quote registry syntax freely, so a
    requirement can contain a line whose text reads `status = ...`. Rewriting by
    physical line alone edited THAT line, left the row's real `status` at
    `Modified`, and returned True — so the tool reported a flip it had not made
    while silently rewriting attested requirement text. A line inside a string
    is DATA; only a line at the table's top level is a key.

    The same state tracking is what makes the table-header scan sound: a `[` in
    the middle of a prose cell would otherwise read as the start of a new row
    and end the search early."""
    header = "[{}.{}]".format(table, rid)
    in_row = False
    open_delim = None  # the multi-line delimiter we are currently inside, if any
    for i, line in enumerate(lines):
        counts = _multiline_delims(line)
        if open_delim is not None:
            # Inside a multi-line string: this line is DATA. It can only end the
            # string, never open a table or set a key.
            if counts[open_delim] % 2:
                open_delim = None
            continue
        stripped = line.strip()
        opened = next((d for d in _TOML_MULTILINE if counts[d] % 2), None)
        if stripped.startswith("[") and stripped.endswith("]") and opened is None:
            in_row = stripped == header
            continue
        if in_row and stripped.split("=")[0].strip() == _STATUS_KEY and opened is None:
            lines[i] = '{} = "Verified"'.format(_STATUS_KEY)
            return True
        open_delim = opened
    return False


def _apply_flips(root, tables, located):
    """Move each located `Modified` row to `Verified` and rewrite exactly the
    registries that changed; the sorted flipped ids. Per carrier: a CSV rewrite
    re-emits the mutated rows, a TOML rewrite edits the one status LINE."""
    import csv

    flipped, changed = [], set()
    toml_edits = {}
    for rid, (rel, status, row, status_ix) in sorted(located.items()):
        if status is None:
            # The row exists and carries NO Status at all. Absent is not
            # "not Modified" — there is nothing here to re-verify, and skipping
            # it silently reports a clean adjudication over a row that never
            # staged one. Fail closed, naming the row.
            raise SystemExit(
                "intake: {} in {} has no `{}` — a row with no status cannot be "
                "re-verified, and treating that as a no-op would report an "
                "adjudication the registry does not record".format(
                    rid, tables[rel][0], _STATUS_KEY
                )
            )
        if status != "Modified":
            continue
        live, _rows = tables[rel]
        if live.suffix == ".toml":
            toml_edits.setdefault(rel, []).append(rid)
        else:
            row[status_ix] = "Verified"
        flipped.append(rid)
        changed.add(rel)
    for rel, ids in toml_edits.items():
        live, _rows = tables[rel]
        table = spine_carrier.SPINE_TABLE[dict(check_trajectory.SPINE_CSVS)[rel]]
        # The file's OWN newline style is preserved (repo-lock D-5; the
        # contract this writer advertises is that every byte except the one
        # status cell is unchanged, and silently converting a CRLF registry to
        # LF makes a one-word ratification a whole-file diff — on exactly the
        # registry whose diffs the amendment guard reads). `newline=""` keeps
        # the bytes; the split is on the detected terminator.
        raw = live.read_text(encoding="utf-8-sig", newline="")
        eol = "\r\n" if "\r\n" in raw else "\n"
        lines = raw.split(eol)
        for rid in ids:
            if not _flip_status_lines(lines, table, rid):
                # A located row whose status line cannot be found is a refusal
                # to write, never a silent skip: the caller already reported the
                # flip, so a no-op here would claim a ratification that is not
                # in the file.
                raise SystemExit(
                    "intake: {} has no `{}` line under [{}.{}] — refusing to "
                    "report a flip that was not written".format(
                        live, _STATUS_KEY, table, rid
                    )
                )
        live.write_text(eol.join(lines), encoding="utf-8", newline="")
    for rel in changed:
        live, rows = tables[rel]
        if rows is None:
            continue
        with live.open("w", newline="", encoding="utf-8") as fh:
            csv.writer(fh, quoting=csv.QUOTE_MINIMAL, lineterminator="\n").writerows(
                rows
            )
    return sorted(flipped)


def _cli_result(refusal, ok_message):
    """The CLI subcommands' one ending: the refusal to stderr and 1, or the
    summary line and 0."""
    if refusal:
        _say(refusal, err=True)
        return 1
    _say(ok_message)
    return 0


def _cmd_adjudicate(args):
    """The adjudication worker's mechanical tool: enact (or recommend) the
    no-scope-moved outcome per the declared gate-policy."""
    root = Path(args.root).resolve()
    action, flipped, refusal = flip_verified(root, _split(args.rows))
    return _cli_result(
        refusal, "action: {} ({} row(s) flipped)".format(action, len(flipped))
    )


def _cmd_census(args):
    """Rung 1 by hand: derive the gap census (via dispatch.gap_census) and
    mint the gap-closure rows."""
    import dispatch

    root = Path(args.root).resolve()
    census = dispatch.gap_census(root)
    if not census:
        _say("the registries name no gaps - nothing to mint.")
        return 0
    minted, refusal = mint_gap_rows(root, census)
    return _cli_result(
        refusal,
        "census named {} gap(s); minted {} row(s) (the rest have open rows).".format(
            len(census), len(minted)
        ),
    )


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    sub = ap.add_subparsers(dest="cmd")
    sweep = sub.add_parser(
        "sweep", help="re-run the merge-slot intake (idempotent recovery)"
    )
    sweep.add_argument("--before", help="pre-merge trunk sha (trigger a)")
    sweep.add_argument("--after", help="post-merge trunk sha (trigger a)")
    sweep.set_defaults(func=_cmd_sweep)
    census = sub.add_parser(
        "census", help="derive the gap census and mint gap-closure rows"
    )
    census.set_defaults(func=_cmd_census)
    adj = sub.add_parser(
        "adjudicate",
        help="enact (or recommend) the no-scope-moved flip — which of the two "
        "depends on whether the tier in process is still human-held "
        "(docs/process.toml [attestation] human_ratification_through)",
    )
    adj.add_argument(
        "--rows", required=True, help="spine row id(s), ;-joined (SR-/LLR-/TC-)"
    )
    adj.set_defaults(func=_cmd_adjudicate)
    # The `attest` subcommand retired with `attestations.csv` (docs/repo-lock.md
    # D-1). It returns with the anchor half, writing the accepted digest to the
    # artifact's own row instead of appending a ledger line — same name, same
    # `--rows`/`--decision` contract, different destination.
    args = ap.parse_args(argv)
    if not getattr(args, "cmd", None):
        ap.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
