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

Contracts: IF-090, IF-091, IF-092 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

import agent_common as ac
import check_trajectory
import schedule
import wi_convert

SCRIPTS = Path(__file__).resolve().parent
WORK = "docs/work"

# The traced cells that ROUTE to adjudication rather than staying silent
# (§A5.1 for `SN-Refs`/`Verifies`; the WI-388 ruling for LLR `SR-Refs` —
# recorded at check_trajectory.SPINE_TRACED_CELLS, the cell-split table's
# home). Keyed per registry so a same-named column elsewhere never rides in.
ROUTED_TRACED_CELLS = {
    "docs/requirements/system-requirements.csv": frozenset({"SN-Refs"}),
    "docs/requirements/low-level-requirements.csv": frozenset({"SR-Refs"}),
    "docs/test/test-cases.csv": frozenset({"Verifies"}),
}

# The disposition row's face: the R3 outcome vocabulary, verbatim in the title
# so the claiming worker reads its whole authority off the row.
_DISPOSITION_OUTCOMES = (
    "cancel / defer / re-queue with drafted follow-up / surface an open item"
)

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
    }
)

_WI_FILE_RE = re.compile(r"^WI-(\d+)-.+\.md$")
# Clip widths for derived text: one cell value, one census line, one title.
_CELL_CLIP = 120
_LINE_CLIP = 140


def _say(msg, err=False):
    print("intake: {}".format(msg), file=sys.stderr if err else sys.stdout)


def _clip(text, width):
    text = " ".join(str(text).split())
    return text if len(text) <= width else text[: width - 1] + "…"


def next_wi_id(root):
    """`max(existing) + 1` over EVERY spec filename under docs/work/ — every
    declared status directory including `active/<branch>/`, plus any residue
    folder (a broader read than the loaders on purpose: for a MINT, an id held
    anywhere is an id taken). Filenames only, never file contents — the same
    rule the loaders verify per-file."""
    top = 0
    work = Path(root) / WORK
    if work.is_dir():
        for path in work.rglob("WI-*.md"):
            matched = _WI_FILE_RE.match(path.name)
            if matched:
                top = max(top, int(matched.group(1)))
    return "WI-{:03d}".format(top + 1)


def tier_signal(trigger, *, rows_touched=0, gate_moved=False, reason=""):
    """`buildtier` from MEASURABLE inputs (the amendment's clause 2): rows
    touched + gate delta for an amendment, the handback reason class for a
    disposition, and the census kind for a gap row. Deeper review is a drafted
    follow-up with `planmode = "dual"`, never a tier here and never a second
    kind."""
    if trigger == "amendment":
        return "strong" if gate_moved or rows_touched > 3 else "medium"
    if trigger == "handback":
        return "strong" if "NEEDS-HUMAN" in (reason or "").upper() else "medium"
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
        for r in _csv_rows(root / "docs/requirements/low-level-requirements.csv")
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
        for t in _csv_rows(root / "docs/test/test-cases.csv")
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
            if cell in ROUTED_TRACED_CELLS.get(rec["registry"], ())
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
        "(per docs/gate-policy — recommend-only under attended, ruled decision",
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


def _returned_spec(root, wi_id):
    """The handed-back spec's `(relpath, frontmatter, handback_reason)` on the
    post-merge trunk — searched across the OPEN directories a handback may
    return to (queued/draft/deferred). None when it cannot be found/read."""
    for status_dir in ("queued", "draft", "deferred"):
        hits = sorted((Path(root) / WORK / status_dir).glob(wi_id + "-*.md"))
        for hit in hits:
            try:
                text = hit.read_text(encoding="utf-8")
                meta, body = ac.parse_spec_frontmatter(
                    text, hit.relative_to(Path(root)).as_posix()
                )
            except (OSError, ValueError, UnicodeDecodeError):
                continue
            reason = ""
            _, sep, note = text.partition(ac.SPEC_HANDBACK)
            if sep:
                reason = next(
                    (ln.strip() for ln in note.splitlines() if ln.strip()), ""
                )
            return hit.relative_to(Path(root)).as_posix(), meta, reason
    return None


def _rev7(root, rev):
    """`rev` resolved to its short sha (7), falling back to the raw text —
    the event token the derived titles carry, so a symbolic `HEAD` from the
    sweep CLI and the slot's full sha name the same event the same way."""
    code, out = ac.git(root, "rev-parse", str(rev))
    return out.strip()[:7] if code == 0 and out.strip() else str(rev)[:7]


def _handback_drafts(root, outcomes, after7):
    drafts = []
    for wi_id in sorted(w for w, o in (outcomes or {}).items() if o == "handback"):
        found = _returned_spec(root, wi_id)
        if found is None:
            _say(
                "{} merged as a handback but its returned spec is not "
                "readable in an open directory - no disposition minted; "
                "sweep by hand".format(wi_id),
                err=True,
            )
            continue
        relpath, meta, reason = found
        if (meta.get("safety_class") or "").strip().lower() == "adjudication":
            # The no-recursion invariant, intake end: a disposition row never
            # spawns a disposition row. hand_back refuses this shape too; a
            # hand-made handback that slipped past still dead-ends HERE.
            _say(
                "{} is an adjudication row handed back - NO disposition row "
                "is minted for it (R3: no recursion); its return is the "
                "owner's to read".format(wi_id),
                err=True,
            )
            continue
        drafts.append(
            {
                # The handback MERGE's sha is the title's event token
                # (REVIEW-A finding 3, the amendment title's sha discipline
                # applied to trigger b): a re-queued row's SECOND handback is
                # a NEW event that mints its own disposition — never a silent
                # dedupe that leaves nobody owed the judgement — while a
                # re-run for the SAME merge still dedupes exactly.
                "title": (
                    "dispose: {} handed back at {} ({}) - {} (a disposition "
                    "row never hands back; R3)".format(
                        wi_id, after7, relpath, _DISPOSITION_OUTCOMES
                    )
                ),
                "kind": "adjudication",
                "workstream": "process",
                "buildtier": tier_signal("handback", reason=reason),
                "specref": relpath,
                "context": (
                    "The handed-back spec is `{}`; its `## Handback` section "
                    "says:\n\n> {}\n\nOutcomes (R3): {}. Clearing its "
                    "blockref re-queues it; moving it to cancelled/ (reason "
                    "in the Deliverable) cancels it; a drafted follow-up "
                    "goes in THIS row's ## Dispositions section; an open "
                    "item goes to docs/requirements/open-items.csv.".format(
                        relpath, _clip(reason, _LINE_CLIP), _DISPOSITION_OUTCOMES
                    )
                ),
            }
        )
    return drafts


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
    for wi_id in sorted(w for w, o in (outcomes or {}).items() if o == "merged"):
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
    ("SN", "docs/requirements/stakeholder-needs.md"),
    ("LLR-", "docs/requirements/low-level-requirements.csv"),
    ("TC-", "docs/test/test-cases.csv"),
)
_SR_CSV = "docs/requirements/system-requirements.csv"


def _census_specref(root, line):
    for token, rel in _CENSUS_SPECREFS:
        if line.startswith(token) or token in line.split(" ", 1)[0]:
            if (Path(root) / rel).is_file():
                return rel
    return _SR_CSV if (Path(root) / _SR_CSV).is_file() else ""


def _census_drafts(root, census):
    # Dedup against EVERY row, open or terminal: a gap row that closed without
    # clearing its gap must not re-mint on the next idle tick (the walk-away
    # loop would otherwise mint the same gap forever) — re-opening a gap whose
    # row failed is a judgement, so it stays a human trunk commit.
    titles = _existing_titles(root)
    drafts = []
    for line in census:
        title = "close registry gap: {}".format(_clip(line, _LINE_CLIP))
        if title in titles:
            continue
        drafts.append(
            {
                "title": title,
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
        )
    return drafts


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
    row["PlanMode"] = str(draft.get("planmode") or "")
    row["Bar"] = str(draft.get("bar") or "").upper()
    row["SR-Refs"] = ";".join(draft.get("sr_refs") or [])
    row["Predecessors"] = ";".join(draft.get("needs") or [])
    if draft.get("priority") is not None:
        row["Priority"] = str(draft["priority"])
    return row


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
    drafts += _handback_drafts(root, outcomes, _rev7(root, after))
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
    for status_dir in ("queued", "draft", "deferred"):
        for path in sorted((root / WORK / status_dir).glob("WI-*.md")):
            matched = _WI_FILE_RE.match(path.name)
            if matched and ac.SPEC_HANDBACK in path.read_text(
                encoding="utf-8", errors="replace"
            ):
                outcomes["WI-" + matched.group(1)] = "handback"
    for path in sorted((root / WORK / "complete").glob("WI-*.md")):
        matched = _WI_FILE_RE.match(path.name)
        if matched:
            outcomes["WI-" + matched.group(1)] = "merged"
    before = args.before or "HEAD"
    after = args.after or "HEAD"
    minted, refusal = intake_after_merge(root, before, after, outcomes)
    return _cli_result(refusal, "sweep minted {} row(s).".format(len(minted)))


# --- the gate-policy arms (ruled decision 2, owner 2026-07-31; §A8) ------------


def adjudication_action(level):
    """May adjudication FLIP `Modified` -> `Verified`? Ruled decision 2:
    **recommend-only under `attended`** — the flip is a Status change that
    RECOVERS THE GATE, i.e. a ratification, and under attended ratification is
    the human's act, so adjudication prepares the brief ("these cells are
    traced-only, no scope moved, recommend re-verify") and stops; **flip under
    `single-ratify` and `autonomous`**, where an LLM verdict already carries
    ratification authority. An unknown level fails toward `recommend` — never
    toward a machine ratification. Attended is the kit DEFAULT even though
    this repo runs autonomous, which is why both arms are built and tested."""
    return "flip" if level in ("single-ratify", "autonomous") else "recommend"


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
    level = ac.read_declared(root / "docs" / "gate-policy", "attended").strip()
    action = adjudication_action(level.lower())
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
    for rid in flipped:
        _say("flipped {} Modified -> Verified (gate-policy '{}')".format(rid, level))
    return action, flipped, None


def _locate_spine_rows(root, wanted):
    """`({id: (csv path, status, row, status_ix)}, {csv path: rows})` over the
    three spine registries — ONE parse, shared by the brief and the flip (the
    row objects are the live lists the rewrite mutates, so nothing scans
    twice)."""
    import csv

    located, tables = {}, {}
    for csv_rel, _id_col in check_trajectory.SPINE_CSVS:
        path = root / csv_rel
        if not path.is_file():
            continue
        with path.open(newline="", encoding="utf-8-sig") as fh:
            rows = list(csv.reader(fh))
        tables[csv_rel] = rows
        header = rows[0] if rows else []
        status_ix = header.index("Status") if "Status" in header else None
        for row in rows[1:]:
            rid = row[0].strip() if row else ""
            if rid in wanted and status_ix is not None and len(row) > status_ix:
                located[rid] = (csv_rel, row[status_ix].strip(), row, status_ix)
    return located, tables


def _apply_flips(root, tables, located):
    """Mutate each located `Modified` row to `Verified` and rewrite exactly
    the registries that changed; the sorted flipped ids."""
    import csv

    flipped, changed = [], set()
    for rid, (csv_rel, status, row, status_ix) in located.items():
        if status == "Modified":
            row[status_ix] = "Verified"
            flipped.append(rid)
            changed.add(csv_rel)
    for csv_rel in changed:
        with (root / csv_rel).open("w", newline="", encoding="utf-8") as fh:
            csv.writer(fh, quoting=csv.QUOTE_MINIMAL, lineterminator="\n").writerows(
                tables[csv_rel]
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
        help="enact (or recommend) the no-scope-moved flip per docs/gate-policy",
    )
    adj.add_argument(
        "--rows", required=True, help="spine row id(s), ;-joined (SR-/LLR-/TC-)"
    )
    adj.set_defaults(func=_cmd_adjudicate)
    args = ap.parse_args(argv)
    if not getattr(args, "cmd", None):
        ap.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
