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

  (a) **the approved-cell diff on the merged commit** — via
      `acceptance_record.staged_spine_amendments(root, before, after)` (the
      WI-380 seam, consumed as-is). A record mints when it carries an approved
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
      `census.gap_census` hands over become concrete gap-closure rows with
      derived descriptions, deduped against open rows so the ladder cannot
      mint the same gap forever.
  (d) **drafts-not-mints** — an adjudication row files follow-ups as a
      `## Dispositions` section in its own spec body (one fenced ```toml
      block per draft); intake parses the section and mints them at ITS merge.
      An in-lane mint would trip WI-397's R1 rung at the row's own merge slot,
      which is the invariant working, not an inconvenience.

**Tier signals are measurable, never judged**: rows touched and a moved
`docs/stage` (trigger a), the handback reason class (trigger b), and the census
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

Contracts: IF-090 — the interface seam this module declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-090: the trunk-side intake mint, by importer.
    `intake_after_merge(root, before, after, outcomes, branch)` is integrate's
    post-merge arm: it mints one landed merge's forced rows — the amendment
    adjudications, the close dispositions and the drafts a close names — as ONE
    bookkeeping commit inside the slot the caller holds, returning them with a
    refusal slot. `mint_gap_rows(root, lines)` is the dispatcher's
    empty-frontier arm over a census, and `context_block(root, wi_row)` renders
    the registry joins a worker prompt embeds — advisory: agent_loop imports it
    lazily and reads a failure as no join. `adjudication_action` and
    `flip_verified` are CLI-driven only. ALL-OR-NOTHING: any refusal mints
    nothing and restores trunk while the merge stands, and deterministic titles
    make the CLI recovery re-run idempotent by exact-title dedup.
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
import tomllib
from pathlib import Path

# Sibling: the spine's registry CARRIER — one home for the
# TOML tier tables, the key->column vocabulary and both readers.
try:
    import spine_carrier
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier

# The stage axis's format + parser (WI-498). `_stage_moved` reads `docs/stage` out
# of two git trees, so it needs the FORMAT reader, not the filesystem-bound common
# one — the parse rule has exactly one home either way.
try:
    from kitlib import stage as kitstage
    from kitlib import spine as _spine
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kitlib import stage as kitstage
    from kitlib import spine as _spine

import acceptance_record
import agent_common as ac
import baseline_snapshot
import census
import schedule
import trace
import wi_convert

SCRIPTS = Path(__file__).resolve().parent
WORK = "docs/work"
# Terminal history's home since WI-504 (OI-55 ruled (a)): `complete/`,
# `cancelled/` and `partial/` moved out of the active workspace, one directory
# deeper, under the archive. A closed spec this module needs to find — for a
# disposition draft, a spot-check, or the by-hand recovery sweep — may now be
# in either root (a legacy repo mid-migration, or simply because the two
# terminal directories share their status-dir NAMES) so every terminal-folder
# read goes through `_terminal_hits` rather than a bare `WORK` glob.
ARCHIVE_WORK = "docs/archive/work"

# --- the WI `bar:` vocabulary (OI-21 contract break 3) -------------------------
# The bar a work item is held to, in the stage-ladder vocabulary. A WI's `bar:`
# frontmatter is a value the AUTHOR writes, so the retired `DevStg-Reqs|DevStg-Tests|DevStg-Impl` tags
# translate on read — silently, like `docs/stack.ini`'s `gates=` and for the same
# reason: check_vocab.py sees the authored spec file and can name the line, which
# is a better message than a loader could produce. New rows author the new form.
#
# The retired matching was `.upper()` + an uppercase tuple, which is why this is a
# named helper now rather than an inline expression: `"DevStg-Reqs".upper()` is
# `"DEVBAR-REQS"`, so a case-folding comparison would have silently rejected every
# correctly-authored new value.
WI_BARS = ("DevStg-Reqs", "DevStg-Tests", "DevStg-Impl")
_RETIRED_WI_BARS = {
    "g1": "DevStg-Reqs",
    "g2": "DevStg-Tests",
    "g3": "DevStg-Impl",
    # The `DevBar-*` prefix, retired 2026-08-18 (one vocabulary; the verb carries
    # the axis). Keyed lower-case like the rows above, since this table is looked
    # up case-insensitively. The Release row translates to `DevStg-Impl`, NOT to
    # `DevStg-Release`: that bar closed the Impl rung and `DevStg-Release` is not
    # clearable at all, so the alias carries the correction, not a prefix swap.
    "devbar-reqs": "DevStg-Reqs",  # check_vocab: allow
    "devbar-tests": "DevStg-Tests",  # check_vocab: allow
    "devbar-release": "DevStg-Impl",  # check_vocab: allow
}


def normalize_bar(value):
    """A `bar:` cell as a canonical `DevStg-*` name ("" when blank).

    Retired tags translate case-insensitively; a canonical value is matched
    case-insensitively too and returned in its declared casing, so `devbar-reqs`
    is accepted without the value ever being stored mis-cased. Anything else comes
    back stripped and unchanged, for the caller to refuse by name."""
    raw = str(value or "").strip()
    if not raw:
        return ""
    low = raw.lower()
    if low in _RETIRED_WI_BARS:
        return _RETIRED_WI_BARS[low]
    for canonical in WI_BARS:
        if low == canonical.lower():
            return canonical
    return raw


# The traced cells that ROUTE to adjudication rather than staying silent
# (§A5.1 for `SN-Refs`/`Verifies`; the WI-388 ruling for LLR `SR-Refs` —
# recorded at acceptance_record.SPINE_TRACED_CELLS, the cell-split table's
# home). Keyed per registry so a same-named column elsewhere never rides in.
ROUTED_TRACED_CELLS = {
    "docs/requirements/system-requirements.toml": frozenset(
        {"SN-Refs", "Boundary-Refs"}
    ),
    "docs/requirements/low-level-requirements.toml": frozenset({"SR-Refs"}),
    "docs/test/test-cases.toml": frozenset({"Verifies"}),
}

# The disposition row's face: the R3 outcome vocabulary, verbatim in the title
# so the claiming worker reads its whole authority off the row.
# LLR-161 retired R3's `re-queue`: a terminal row is never put back on the
# frontier, so continuing the work means DRAFTING A SUCCESSOR (minted at this
# row's own merge, carrying `supersedes`). `handback._no_recursion_refusal`
# states the same four; the two homes must not disagree about a row's authority.
_DISPOSITION_OUTCOMES = "cancel / defer / draft a successor / surface an open item"

# The title prefix the two EARLY-CLOSE disposition arms share (`_close_drafts`:
# the partial and the cancelled arm). It is the ONE durable signal the refusal
# invariant can read at BOTH ends of the close: `specref` points at the closed
# spec (the outcome under judgement) but the close CLEARS it, and `brief` is
# `"disposition"` only for the partial arm — the cancelled arm is brief-LESS by
# design — so neither survives-and-distinguishes. The kit generates every one of
# these titles, so a shared constant keeps the writer and the guards in one
# home; the clean-close spot check ("spot-check ..."), the amendment
# ("adjudicate: ...") and the census rows do NOT carry it and owe no successor.
_DISPOSITION_TITLE_PREFIX = "dispose:"


def owes_successor(meta):
    """Whether an adjudication row judges an EARLY close (partial/cancelled) and
    so MUST queue at least one successor (OI-70/OI-73, no third exit).

    Read off the kit-generated title prefix the two early-close arms share, NOT
    the `brief` cell (which distinguishes only the partial arm) or `specref`
    (which the close clears): the title is preserved across the close, so the
    close-side guard (`handback.close_adjudication`, pre-close) and the
    merge-side guard (`_disposition_drafts`, post-close, on a row an agent may
    have SELF-closed past the first guard) read the same durable signal."""
    return (
        str(meta.get("title") or "").strip().startswith(_DISPOSITION_TITLE_PREFIX)
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
        # LLR-161 lineage: a successor drafted by a disposition names the row it
        # continues, so partial work keeps its thread ACROSS the id change. It
        # is a lineage fact, not a revival — the superseded row stays terminal
        # and its scope stays exactly what it was.
        "supersedes",
        # OI-73 exit (B), as a typed dependency: where the answer is human-owed
        # and the adjudicator found no alternative route, the draft names the
        # human question here. The mint creates a `pending` open item for it
        # (id from the watermark's OI space) and lands that OI id in THIS
        # successor's `needs`, so the ruling gates the successor's readiness
        # rather than relying on adjudicator restraint. A standalone OI exit no
        # longer exists — the OI is always a dependency of a queued successor.
        "open_item",
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
    # Both roots (WI-504): a filename swept for "is this id taken" must be
    # found wherever a spec might carry it, and terminal specs now live under
    # the archive, one directory deeper than the active workspace.
    for base in (WORK, ARCHIVE_WORK):
        tree = Path(root) / base
        if not tree.is_dir():
            continue
        for path in tree.rglob("WI-*.md"):
            matched = _WI_FILE_RE.match(path.name)
            if matched:
                top = max(top, int(matched.group(1)))
    mark = trace.read_watermark(root).get("WI", 0)
    return "WI-{:03d}".format(max(top, mark) + 1)


# The OI registry (OI-73 exit (B)). Reads through the same rel `trace` uses so a
# minted edge and the readiness gate resolve the same file.
OPEN_ITEMS_REL = "docs/requirements/open-items.toml"
_OI_ID_RE = re.compile(r"^\[open_item\.(OI-\d+)\]", re.M)


def next_oi_id(root):
    """`max(watermark, existing) + 1` in the OI space — the same read-and-bump
    discipline `next_wi_id` uses (OI-70 clarity answer: the watermark already
    carries the OI space, so the mint needs no new id machinery). OI ids are not
    zero-padded, matching the hand-authored rows already in the registry."""
    mark = trace.read_watermark(root).get("OI", 0)
    live = trace.live_max_ids(root).get("OI", 0)
    return "OI-{}".format(max(mark, live) + 1)


def _mint_open_item(root, question, wi_ref, *, date=None):
    """Append one `pending` open item for a human-owed answer and return its id
    (OI-73 exit (B)). `docs/open-items.html` is regenerated by the mint's
    bookkeeping commit (`trunk_step --regen` runs `gen_open_items`), so the
    surface and the registry land in the same commit. `(oi_id, None)` or
    `(None, refusal)` — refuses on a non-TOML carrier, since appending a table
    is a TOML act; a downstream repo on a CSV open-items registry keeps its
    hand-authored path rather than getting a malformed row."""
    live = spine_carrier.resolve(Path(root) / OPEN_ITEMS_REL)
    if live is None or live.suffix != ".toml":
        return None, (
            "the OI mint needs a TOML open-items registry at {} (found {}); "
            "the human-owed answer must be recorded by hand".format(
                OPEN_ITEMS_REL, live.name if live is not None else "none"
            )
        )
    oi_id = next_oi_id(root)
    raised = date or datetime.date.today().isoformat()
    table = (
        "\n[open_item.{}]\n".format(oi_id)
        + "title = {}\n".format(wi_convert.toml_string(_clip(question, 100)))
        + 'status = "pending"\n'
        + "raised = {}\n".format(wi_convert.toml_string(raised))
        + "one_line = {}\n".format(wi_convert.toml_string(question))
        + "wi_refs = {}\n".format(wi_convert.toml_value([wi_ref]))
    )
    with live.open("r", encoding="utf-8") as fh:
        existing = fh.read()
    sep = "" if existing.endswith("\n") else "\n"
    with live.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(sep + table)
    return oi_id, None


def tier_signal(trigger, *, rows_touched=0, stage_moved=False):
    """`buildtier` from MEASURABLE inputs (the amendment's clause 2): rows
    touched + STAGE delta for an amendment, the census kind for a gap row.
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
        return "strong" if stage_moved or rows_touched > 3 else "medium"
    if trigger == "red-tc":
        # LLR-159. One target is a local question (is this TC stale, or
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


# The ref-cell splitter is agent_common's (`_refs`) — imported, not copied:
# intake is not one of the F5 independently-copyable three, so a shared reader
# beats another verbatim copy. (`_csv_rows = ac._read_csv_rows` sat here until
# WI-443 moved the last two registries this module reads — components and
# interfaces — onto the TOML carrier; every registry read here now goes through
# `spine_carrier.load`, which answers whichever carrier is live.)
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
        for o in spine_carrier.load(root / "docs/requirements/open-items.toml", "OI-ID")
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
        for c in spine_carrier.load(
            root / "docs/requirements/components.toml", "CMP-ID"
        )
        if c.get("CMP-ID") in comps and (c.get("Knowledge") or "").strip()
    ]


def _seam_lines(root, llrs):
    stems = {
        Path(r.get("Module") or "").stem
        for r in llrs
        if (r.get("Module") or "").strip()
    }
    return [
        "- {} {} {} {}: {}".format(
            i.get("IF-ID"),
            i.get("Owner"),
            "<-" if i.get("Requestors") else "->",
            i.get("Requestors") or i.get("Consumers"),
            "{} {}".format(i.get("Channel"), _clip(i.get("Data"), 110)),
        )
        for i in spine_carrier.load(root / "docs/requirements/interfaces.toml", "IF-ID")
        if Path(i.get("Owner") or "").name in stems
        or any(
            Path(c).name in stems
            for c in (i.get("Requestors") or i.get("Consumers") or "").split(";")
        )
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


# --- trigger (a): the approved-cell diff on the merged commit ------------------


def _routed_amendments(root, before, after):
    """The amendment records that are adjudication's to judge: an approved
    change, or a routed traced change (`ROUTED_TRACED_CELLS`). Everything else
    in the traced half is silent by ruling."""
    routed = []
    for rec in acceptance_record.staged_spine_amendments(root, before, after):
        routed_cells = {
            cell: change
            for cell, change in rec["traced"].items()
            # Keyed by the registry STEM: the record names whichever carrier
            # file git reported, and a suffix-keyed miss here would silently
            # reclassify a routed cell as an ordinary amendment.
            if cell
            in {spine_carrier.stem(k): v for k, v in ROUTED_TRACED_CELLS.items()}.get(
                spine_carrier.stem(rec["registry"]), ()
            )
        }
        if rec["approved"] or routed_cells:
            routed.append(dict(rec, routed=routed_cells))
    return routed


def _stage_moved(root, before, after):
    """Did the repo's effective STAGE move across the merge? A two-point delta of
    `docs/stage`'s headline value, read off the two git trees — a measurable
    input, not a judgement.

    THIS FUNCTION WAS DEAD FOR THE WHOLE DERIVED-GATE ERA (WI-497, folded into
    WI-498 slice 4). It read `docs/gate` and took `splitlines()[0]` — the FIRST
    line, which since the derived model is the static do-not-hand-edit header and
    is byte-identical at every revision, not the first NON-COMMENT line every
    other reader took. So it answered False unconditionally and `tier_signal`
    could never mint its `strong` adjudication row. It worked before the derived
    migration, when a hand-set gate file's line 0 WAS the value, and broke
    silently at it. The fix is not a better line index: `docs/stage` is key=value
    precisely so a reader addresses a FIELD (slice 1), and `kitlib.stage.parse` is
    the one parser for it.

    UNREADABLE ON EITHER SIDE ANSWERS FALSE, which is a deliberate tightening of
    the retired contract ("unreadable answers False" was written but not
    implemented — a None on one side and a value on the other compared unequal and
    reported a move). It also keeps the one-time migration boundary quiet: at the
    commit that first wrote `docs/stage` the before side has no file, and that is
    a kit upgrade, not an approval."""
    values = []
    for rev in (before, after):
        code, out = ac.git(root, "show", "{}:{}".format(rev, kitstage.STAGE_FILE))
        if code != 0 or not out:
            return False
        try:
            record = kitstage.parse(out)
        except ValueError:
            # A rung this kit does not know, at one of the two revisions. The
            # `derived-stage` step is what reports that; a tier signal declines
            # to guess rather than minting a strong row off an unreadable value.
            return False
        if record is None:
            return False
        values.append(record["stage"])
    return values[0] != values[1]


def _amendment_context(records):
    """The derived listing — each changed row, cell, and before/after — the
    §A5.2 'derived description' in its honest home (the advisory `## Context`
    section; R-A forbids a filled Deliverable on an open row)."""
    lines = [
        "Derived from `staged_spine_amendments` on the merged commit (§A5.2).",
        "Approved and ROUTED traced cells only; other traced cells are silent",
        "by ruling. Each line: registry row / cell: before -> after.",
        "",
    ]
    for rec in records:
        cells = dict(rec["approved"])
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
        "Outcomes (§A5.2): flip rows back to Approved where no scope moved",
        "(per the declared approval level in docs/process.toml — "
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
        "adjudicate: {} - approved/routed cell(s) amended on merged trunk "
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
                stage_moved=_stage_moved(root, before, after),
            ),
            "sr_refs": _owning_srs(records),
            "specref": records[0]["registry"],
            "context": _amendment_context(records),
        }
    ]


# --- trigger (b): a merged handback mints the disposition row ------------------


def _terminal_hits(root, status_dir, pattern):
    """Every match for `pattern` under `status_dir`, unioned across the active
    workspace and its archive sibling (WI-504) — a terminal spec's status
    directory name is the same in both, so a caller that means "the `partial/`
    population" gets it whole regardless of which root a given close landed
    in."""
    root = Path(root)
    hits = []
    for base in (WORK, ARCHIVE_WORK):
        hits.extend((root / base / status_dir).glob(pattern))
    return sorted(hits)


def _closed_spec(root, wi_id, dirs=("partial", "cancelled")):
    """The closed spec's `(relpath, frontmatter)` on the post-merge trunk —
    searched across the terminal directories the CALLER names. None when it
    cannot be found or read.

    The default is the EARLY-close pair on purpose: the disposition arm must
    not find a `complete/` spec and mint an early-close judgement for a clean
    one. The spot-check arm passes `("complete",)` explicitly, so which
    directory a caller means is always written down."""
    for status_dir in dirs:
        hits = _terminal_hits(root, status_dir, wi_id + "-*.md")
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
                        "{} the cancellation recorded at {} - {} (a "
                        "disposition row never closes early; R3)".format(
                            _DISPOSITION_TITLE_PREFIX, relpath, _DISPOSITION_OUTCOMES
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
                        "{} the close recorded at {} - {} (a disposition "
                        "row never closes early; R3)".format(
                            _DISPOSITION_TITLE_PREFIX, rel_report, _DISPOSITION_OUTCOMES
                        )
                    ),
                    "kind": "adjudication",
                    "brief": "disposition",
                    "workstream": "process",
                    # The TYPED field, not a substring of prose (LLR-161 / the
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
        "docs/requirements/open-items.toml."
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
        "was. An open item goes to docs/requirements/open-items.toml."
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
    # The prose after each block, up to the next one: the adjudicator's own
    # statement of the successor's scope, which rides into the minted Context
    # verbatim - the cells alone cannot carry a boundary or an exclusion.
    prose = _TOML_FENCE_RE.split(section)[2::2]
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
        draft["scope"] = prose[index - 1].strip("\n") if index <= len(prose) else ""
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
    bar = normalize_bar(data.get("bar"))
    if bar and bar not in WI_BARS:
        return "{} declares bar = {!r} ({}) - nothing minted".format(
            at, data.get("bar"), "|".join(WI_BARS)
        )
    return None


def _disposition_drafts(root, outcomes):
    """Trigger (d): drafts from every MERGED adjudication row's spec body."""
    drafts = []
    for wi_id in _merged_ids(outcomes):
        hits = _terminal_hits(root, "complete", wi_id + "-*.md")
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
            # THE REFUSAL INVARIANT (OI-70, tightened by OI-73): a PARTIAL or
            # CANCELLED close MUST queue at least one successor — an OI alone no
            # longer discharges it (OI-70 exit-(B)-alone is retired), and there
            # is no third exit. `owes_successor` reads the durable title signal,
            # NOT `brief`: the `partial` arm carries `brief = "disposition"` but
            # the `cancelled` arm is brief-LESS by design (it owes no report, so
            # the kit assembles no brief and `agent_loop` gives it the ordinary
            # worker assignment), and gating on `brief` let a cancelled close
            # queue no successor and merge silently. THIS guard is the one that
            # catches the SELF-close path — an agent that moved its own spec to
            # `complete/` never reaches `close_adjudication` (dispatch short-
            # circuits on a finished branch), and the self-close CLEARS specref,
            # so the title is the only signal left. A clean-close spot check owes
            # none and is not caught. A merged early-close row with an empty
            # `## Dispositions` section is REFUSED here: the merge stands
            # (all-or-nothing mint), the run stops, and a human reads the lane
            # rather than a close silently vanishing without a continuation.
            if owes_successor(meta) and not parsed:
                return [], (
                    "{}: an early-close (partial/cancelled) adjudication row "
                    "merged with an EMPTY ## Dispositions section — such a close "
                    "must queue at least one successor (OI-70/OI-73, no third "
                    "exit). Draft the successor in the row's ## Dispositions "
                    "section and re-run `python intake.py sweep`".format(relpath)
                )
            for draft in parsed:
                draft.setdefault("specref", relpath)
                draft.setdefault("workstream", meta.get("workstream") or "process")
                draft.setdefault("buildtier", "medium")
                draft["context"] = (
                    "Drafted by {} (its ## Dispositions section) and minted at "
                    "its merge - drafts-not-mints, ruling R1/R3.".format(wi_id)
                ) + ("\n\n" + draft["scope"] if draft.get("scope") else "")
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
    merge instead of at authoring."""
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


def _census_drafts(root, lines):
    # Dedup against EVERY row, open or terminal: a gap row that closed without
    # clearing its gap must not re-mint on the next idle tick (the walk-away
    # loop would otherwise mint the same gap forever) — re-opening a gap whose
    # row failed is a judgement, so it stays a human trunk commit.
    titles = _existing_titles(root)
    drafts = []
    for line in lines:
        red = census.parse_red_tc(line)
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
    """LLR-159: a red TC under a claimed implementation becomes an
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
    is countable — `targets` comes from `census.parse_red_tc`, the one reader
    of the census grammar, never from re-splitting this line's prose.

    NO `planmode` CELL, and the reason is a defect this row shipped with for
    exactly one review round: `planmode = "dual"` beside `safety_class =
    "adjudication"` is a shape `schedule.classify` REFUSES — it reads
    `unclassified`, drops off the frontier, and can never be re-minted because
    exact-title dedup has already claimed the title. The contradiction LLR-159
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

# The OPEN statuses whose inbound edges a supersede-carrying mint re-points
# (OI-73 arm 4). A terminal row's `needs` is historical record — never rewritten
# — so only these four are candidates. `parse_spec_status` maps `complete/` to
# `done`, so a terminal row is anything outside this set.
_OPEN_STATUSES = frozenset({"draft", "queued", "active", "deferred"})
# The frontmatter `needs = [...]` array line, replaced surgically so the rest of
# a spec (its `## Context`, its Deliverable, every other cell) is untouched.
_SPEC_NEEDS_RE = re.compile(r"(?m)^needs\s*=\s*\[.*?\]\s*$")


def _replace_inbound_edges(root, superseded, successor):
    """Re-point every OPEN row's HARD `needs` edge on `superseded` to
    `successor` (OI-73 arm 4). Returns the relpaths changed.

    THE STRAND THIS MAKES UNREPRESENTABLE. A partial/cancelled close leaves the
    closed row terminal, and any live WI that hard-depended on it can never
    become ready (`schedule.hard_preds_satisfied` requires `done`). The WI-541
    -> WI-540 strand waited invisibly and was repaired by hand. OI-73 rules the
    repair mechanical: at the mint of a successor carrying `supersedes`, the
    superseded row's inbound HARD edges are REPLACED with the successor, so the
    dependent's readiness now waits on the row that actually continues the work.
    Soft (`~`) edges are advisory ordering and are left alone; a terminal row's
    own `needs` is history and is never touched. The edit is surgical (only the
    `needs` line) so a dependent's `## Context` and Deliverable are preserved.
    """
    changed = []
    work = Path(root) / WORK
    for path in ac.spec_files(work):
        # `parse_spec_status` reads the STATUS directory as the first path
        # segment, so the relpath is taken against the work dir, not the repo.
        rel = path.relative_to(work).as_posix()
        try:
            if ac.parse_spec_status(rel) not in _OPEN_STATUSES:
                continue
            text = path.read_text(encoding="utf-8")
            data, _body = ac.parse_spec_frontmatter(text, rel)
        except (OSError, ValueError, UnicodeDecodeError):
            continue
        needs = [str(v) for v in (data.get("needs") or [])]
        if superseded not in needs:
            continue
        new_needs = []
        for tok in needs:
            repl = successor if tok == superseded else tok
            if repl not in new_needs:
                new_needs.append(repl)
        new_line = "needs = " + wi_convert.toml_value(new_needs)
        new_text, n = _SPEC_NEEDS_RE.subn(new_line, text, count=1)
        if n:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            changed.append(rel)
    return changed


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
    row["Bar"] = normalize_bar(draft.get("bar"))
    row["SR-Refs"] = ";".join(draft.get("sr_refs") or [])
    row["Predecessors"] = ";".join(draft.get("needs") or [])
    row["Supersedes"] = str(draft.get("supersedes") or "")  # LLR-161 lineage
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


def _write_context(path, root, draft, row, registry):
    """Append the minted row's `## Context` — the trigger's derived context then
    the advisory registry joins (clause 4, consumer 1: a minted row has no spec
    author, so the block is written at mint, computed over the pre-mint
    registry). A no-op when neither is present."""
    context = str(draft.get("context") or "").rstrip("\n")
    joins = context_block(root, row, registry)
    if joins:
        context = (context + "\n\n" if context else "") + joins
    if context:
        with path.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write("\n## Context\n\n" + context + "\n")


def _apply_supersede(root, draft, wi_id):
    """OI-73 arm 4: a successor carrying `supersedes` REPLACES the superseded
    row's inbound hard edges, in the SAME commit as the mint, so the WI-541-class
    strand (a live dependent left waiting on a terminal row) is unrepresentable
    rather than merely reported by the validator net."""
    superseded = str(draft.get("supersedes") or "").strip()
    if not superseded:
        return
    for rel_changed in _replace_inbound_edges(root, superseded, wi_id):
        _say("re-pointed {}'s edge {} -> {}".format(rel_changed, superseded, wi_id))


def _inject_open_item(root, draft, wi_id):
    """OI-73 exit (B): where a draft names a human-owed `open_item`, mint a
    `pending` open item (id from the watermark's OI space) and land its id in
    THIS successor's `needs` — BEFORE the row is written, so the ruling gates
    the successor's readiness (a new waiting reason) instead of relying on
    adjudicator restraint. No standalone OI exit exists. Returns `(draft,
    refusal)`; the draft is unchanged when it names no open item."""
    question = str(draft.get("open_item") or "").strip()
    if not question:
        return draft, None
    oi_id, refusal = _mint_open_item(root, question, wi_id)
    if refusal:
        return draft, refusal
    needs = list(draft.get("needs") or [])
    if oi_id not in needs:
        needs.append(oi_id)
    return dict(draft, needs=needs), None


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
        draft, oi_refusal = _inject_open_item(root, draft, wi_id)
        if oi_refusal:
            ac.git(root, "reset", "--hard", "HEAD")
            ac.git(root, "clean", "-fd", "--", WORK)
            return [], "{}: {}".format(subject_verb, oi_refusal)
        row = _draft_row(wi_id, draft)
        try:
            rel = wi_convert.write_spec_file(root / WORK, row)
        except wi_convert.ConvertError as exc:
            ac.git(root, "reset", "--hard", "HEAD")
            ac.git(root, "clean", "-fd", "--", WORK)
            return [], "the mint could not write {}: {}".format(wi_id, exc)
        _write_context(root / WORK / rel, root, draft, row, registry)
        minted.append((wi_id, (Path(WORK) / rel).as_posix()))
        _apply_supersede(root, draft, wi_id)
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


def mint_gap_rows(root, lines):
    """THE DISPATCHER'S RUNG-1 ARM (trigger c): the gap census, minted as
    concrete gap-closure rows. `([(wi_id, relpath)], refusal)`; an empty
    answer with a non-empty census means every gap already has an open row."""
    return _mint(root, _census_drafts(root, lines), "empty-frontier gap census")


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
        for path in _terminal_hits(root, status_dir, "WI-*.md"):
            matched = _WI_FILE_RE.match(path.name)
            if matched:
                outcomes["WI-" + matched.group(1)] = outcome
    before = args.before or "HEAD"
    after = args.after or "HEAD"
    minted, refusal = intake_after_merge(root, before, after, outcomes)
    return _cli_result(refusal, "sweep minted {} row(s).".format(len(minted)))


# --- the session-hold arms (ruled decision 2, owner 2026-07-31; §A8) -----------


def adjudication_action(human_held):
    """May adjudication FLIP a spine row to `Approved`? Ruled decision 2, re-keyed
    onto SN-029's ordinal: **recommend-only while the tier is HUMAN-HELD** — the
    flip is a Status change that RECOVERS THE GATE, i.e. an approval, and a
    human-held tier's approval is the human's act, so adjudication prepares
    the brief ("these cells are traced-only, no scope moved, recommend
    re-verify") and stops; **flip once the tier is loop-held**, where a recorded
    LLM verdict already carries approval authority.

    Anything unreadable upstream resolves to human-held — `agent_common.
    human_holds` fails that way deliberately — so the failure direction is
    `recommend`, never a machine approval. The kit DEFAULT holds every tier
    even though this repo holds none, which is why both arms are built and
    tested.

    OI-45 RULED (b) RETIRE THE ARM (2026-08-20, executed by WI-490): even where
    this reads `flip`, `_apply_flips` writes NOTHING — it skips an
    already-blessed row and refuses every other state. The name survives
    because the two readings still distinguish which brief the caller owes
    (recommend-and-stop vs. attempt-and-refuse); approval itself moves only
    through the human reviewed-commit path, with `intake.py snapshot` as the
    record's one mechanical door."""
    return "recommend" if human_held else "flip"


def flip_verified(root, ids):
    """Enact — or recommend — the adjudication row's cheap outcome for spine
    rows judged no-scope-moved. Returns `(action, flipped_ids, refusal)`.

    The hold is derived from `docs/process.toml`, never passed by hand (the
    dial's one home). Under `recommend` NOTHING is touched and the prepared
    brief prints — the adjudication worker writes it into its spec and the
    open-items card carries the pending rows to the sitting. Under `flip`
    only the named rows' Status cells move; every other cell of every row
    stays CELL-exact (and the live registries byte-identical — measured:
    their quoting is all by necessity, which QUOTE_MINIMAL reproduces), a
    row already at `Approved` is skipped (idempotent), and an unknown id
    refuses — a typo on a mechanical tool must never half-apply. The flipped
    registry still owes its regeneration (`spine_rules` recovers the gate);
    the lane's own refresh runs it.

    THE `flip` ARM IS THE RULED SHAPE, not an interim state (OI-45, ruled
    2026-08-20, executed by WI-490): mechanical approval is RETIRED —
    `_apply_flips` skips an already-blessed row and refuses everything else, so
    this action writes nothing, permanently. Approval stays a human
    reviewed-commit act; `intake.py snapshot`'s authority-gated refresh is the
    one mechanical door touching the approval record. That is a statement about
    this SCRIPT, not about agent judgment — an LLM session or adjudicator is
    still expected to move a row's Status through the reviewed-commit path for
    spine content past the declared approval level
    (`agent_common.human_holds` says which). `recommend` is unaffected and is
    this repo's live arm (every spine tier is human-held)."""
    root = Path(root)
    # SN-028: the mixed-config refusal, at the third entry point that reads
    # policy without passing through agent_loop.main. This arm decides whether
    # an LLM verdict carries APPROVAL authority, so it is the last place
    # a half-migrated config should be resolved by precedence.
    conflicts = ac.config_conflicts(root / "docs")
    if conflicts:
        return "recommend", [], conflicts[0]
    # SN-029: the ordinal comparison, not the retired enum. `spine_stage_of`
    # reads the tier currently in process through `kitlib.stage.read_stage`;
    # `human_holds` compares it against `human_approval_through`.
    human_held = ac.human_holds(root / "docs", ac.spine_stage_of(root))
    session_hold = "human-held" if human_held else "loop-held"
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
                "under session-hold '{}' the flip is the human's (ruled "
                "decision 2). Write this brief into the adjudication row's "
                "spec; the open-items card carries the pending rows.".format(
                    rid, located[rid][1], session_hold
                )
            )
        return action, [], None
    flipped = _apply_flips(root, tables, located)
    # NO ANCHOR IS OWED HERE, AND NO COPY IS TAKEN — because nothing is written.
    # `_apply_flips` skips an already-blessed row and refuses every other state,
    # so this list is empty and the snapshot is untouched by the mechanical path
    # (2026-08-20: the unreachable write-and-copy block went with the dead arm).
    # OI-45 RULED (b) RETIRE THE ARM (2026-08-20): no mechanical path regains the
    # authority; approval stays human, and `intake.py snapshot`'s
    # authority-gated refresh is the record's one mechanical door.
    for rid in flipped:
        _say("flipped {} -> Approved ({})".format(rid, session_hold))
    return action, flipped, None


def _locate_spine_rows(root, wanted):
    """`({id: (registry rel, status, row, status_ix)}, {registry rel: rows})`
    over the three spine registries — ONE parse, shared by the brief and the
    flip (under the CSV carrier the row objects are the live lists the rewrite
    mutates, so nothing scans twice).

    CARRIER-AWARE. Each registry resolves to whichever of
    TOML/CSV is live, and the two carriers report differently because they are
    written differently: a CSV row is a mutable list plus the column index the
    rewrite pokes, while a TOML table is rewritten by LINE and needs neither.
    `row`/`status_ix` are None on the TOML arm, and `tables` holds the live
    path so the writer never re-guesses the suffix."""
    import csv
    import io

    located, tables = {}, {}
    for rel, id_col in acceptance_record.SPINE_CSVS:
        live = spine_carrier.resolve(root / rel)
        if live is None:
            continue
        tables[rel] = (live, None)
        if live.suffix == ".toml":
            for row in spine_carrier.load(live, id_col):
                rid = (row.get(id_col) or "").strip()
                if rid in wanted:
                    # ABSENT status is None, not "". Under this carrier an absent
                    # key is a real state, and it is not the same as any value:
                    # a row with no Status at all cannot be re-verified, and
                    # treating it as an idempotent no-op reports a clean
                    # adjudication over a row the registry never staged for one.
                    # `_apply_flips` refuses it under its own arm (fail closed),
                    # ahead of the value guard, so the message names the real
                    # fault rather than quoting an empty cell back.
                    status = row.get("Status")
                    located[rid] = (
                        rel,
                        None if status is None else status.strip(),
                        None,
                        None,
                    )
            continue
        # Through the ONE comment-skipping reader (WI-533): a CSV carrier may
        # open with a `#` declaration header, and reading it raw would take that
        # header's first line as `rows[0]` — the id column then holds a comment
        # and every staged row reads as absent.
        text = live.read_text(encoding="utf-8-sig", errors="replace")
        rows = list(csv.reader(io.StringIO(_spine.csv_body(text))))
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
    """Rewrite `[<table>.<rid>]`'s `status = ...` line to `Approved`, in place.
    True when a line moved. A LINE REWRITE ON `bootstrap.set_process_key`'s
    PATTERN, and for its reasons: stdlib has no TOML
    writer, and re-serialising the registry to change one cell would normalise
    away every comment and the file's authored ordering — a whole-file diff for
    a one-word act, on the registry whose diffs the amendment guard reads.

    IT TRACKS MULTI-LINE STRING STATE, and that is not defensive tidiness — it
    is the difference between an approval and a corruption. The spine's prose
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
            lines[i] = '{} = "Approved"'.format(_STATUS_KEY)
            return True
        open_delim = opened
    return False


def _rewrite_toml_statuses(live, rel, ids):
    """Move every named row's status line to `Approved` in one TOML registry.

    Split out of `_apply_flips` when the snapshot copy joined it (D-9 step 3):
    the carrier-specific write is a self-contained job with its own refusal, and
    keeping it inline made the caller's branch count grow every time a step was
    added to an act that is really "flip, then record what was flipped".

    The file's OWN newline style is preserved. The contract this writer
    advertises is that every byte except the one status cell is unchanged, and
    silently converting a CRLF registry to LF makes a one-word approval a
    whole-file diff — on exactly the registry whose diffs the amendment guard
    reads. `newline=""` keeps the bytes; the split is on the detected
    terminator."""
    table = spine_carrier.SPINE_TABLE[dict(acceptance_record.SPINE_CSVS)[rel]]
    # open() rather than Path.read_text: read_text only grew a `newline`
    # parameter at Python 3.13, and the kit's floor is 3.11 — on the floor the
    # keyword is a TypeError, found 2026-08-15 when the suite first ran on the
    # repo's own 3.11.9 venv (the sitting-sweep log entry carries the account).
    with open(live, "r", encoding="utf-8-sig", newline="") as fh:
        raw = fh.read()
    eol = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.split(eol)
    for rid in ids:
        if not _flip_status_lines(lines, table, rid):
            # A located row whose status line cannot be found is a refusal to
            # write, never a silent skip: the caller already reported the flip,
            # so a no-op here would claim an approval that is not in the file.
            raise SystemExit(
                "intake: {} has no `{}` line under [{}.{}] — refusing to "
                "report a flip that was not written".format(
                    live, _STATUS_KEY, table, rid
                )
            )
    live.write_text(eol.join(lines), encoding="utf-8", newline="")


def _apply_flips(root, tables, located):
    """SKIP an already-blessed row, REFUSE everything else, WRITE NOTHING; the
    sorted flipped ids, which is now always empty — and permanently so. OI-45
    (ruled 2026-08-20, executed by WI-490) settled the question this function
    used to carry open.

    **THE STATE THIS ACT MOVED FROM RETIRED AT D-9 STEP 7.** It enacted ruled
    decision 2's cheap outcome (`Modified` -> `Approved` for a row judged
    no-scope-moved); under the snapshot ladder an amendment never flips its
    row, so an amended row already reads `Approved` and there is no cell to
    move. D-9 step 7 left two candidate resolutions on the table — re-bless a
    drifted `Approved` row under loop-hold (a), or retire the arm (b) — and
    OI-45 RULED (b): the guard below is the ruled shape, not a stopgap awaiting
    an owner call.

    OI-45 IS THE RECORD, and what it retires is precise: MECHANICAL
    approval — a scripted path moving a Status cell with no judgment behind
    it. It does not say no agent may ever move a Status cell. An LLM session or
    adjudicator is fully expected to flip a row to `Approved`, and further to
    `Founded`, for spine content past the declared human-approval level
    (`agent_common.human_holds` says which) — at the human's request, or when
    working through content the level does not hold to human approval. The
    dial says who holds what; this function's refusal says only that no SCRIPT
    decides. `_cmd_snapshot`'s authority-gated refresh is the one mechanical
    door the approval record has.

    **THE MACHINERY FOR RE-BLESSING IS GONE (2026-08-20)**: the write loops it
    left standing were unreachable behind the refusal, so what looked like
    "kept intact for (a)" was dead code with a source-grep test pinning it. The
    signature keeps `root`/`tables` because the caller's contract is unchanged
    — not because a future ruling might restore a writer here; restoring one
    would be reopening OI-45, not extending this function."""
    flipped = []
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
        # RESOLVED AT D-9 STEP 7, as the guard this replaces promised. It read
        # `if status != "Modified": continue` — one silent skip over two unrelated
        # states: an already-blessed row (idempotent, correct) and a row this act
        # has no business touching (silent, wrong). The resolution splits them.
        if status == "Approved":
            # Already at the value this act writes — the one legitimate skip, and
            # the idempotence `flip_verified`'s docstring advertises.
            continue
        # Everything else is REFUSED, naming the row. Fail-CLOSED and strictly
        # less permissive than the skip it replaces:
        #   `Drafted`  a FIRST approval, not an adjudication's cheap outcome.
        #   `Founded`  ABOVE `Approved` — writing `Approved` moves it DOWN.
        #   anything   outside the closed enum, already an integrity error.
        raise SystemExit(
            'intake: {} in {} reads `{} = "{}"` — this act moves a row TO '
            "`Approved` and the only state it moved FROM (`Modified`) retired at "
            "D-9 migration step 7. Under the snapshot ladder an amendment does "
            "not flip its row at all, so there is no cell for a mechanical "
            "adjudication to move: an amended row still reads `Approved`, and "
            "what it owes is a fresh human read plus `intake.py snapshot` in the "
            "same commit. Refusing rather than skipping, so the row is named "
            "instead of being passed over.".format(
                rid, tables[rel][0], _STATUS_KEY, status
            )
        )
    # THE WRITE LOOPS AND THE COPY WENT WITH THE ARM (2026-08-20, the batch
    # review's MINOR-12). Everything that used to follow the refusal above — the
    # per-carrier status write, the CSV re-emit, and the `copy_live` that rode
    # them — was UNREACHABLE from the moment the refusal replaced the silent
    # skip: the loop now either `continue`s an already-blessed row or raises.
    # Dead code that LOOKS live is worse than no code, and a test was pinning a
    # guard on it by source grep, which reads as coverage of a path nothing can
    # execute. OI-45 RULED (b) RETIRE THE ARM (2026-08-20, executed by WI-490):
    # mechanical approval is retired for good, not deferred, and
    # `_cmd_snapshot`'s authority-gated refresh is the one mechanical door the
    # approval record has. An agent may still move a Status cell through the
    # reviewed-commit path under the declared authority dial
    # (`agent_common.human_holds`) — the retirement is of this SCRIPT, not of
    # agent judgment. Restoring writes here means reopening the ruling, not
    # un-commenting this.
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
    """The adjudication worker's mechanical tool: RECOMMEND the no-scope-moved
    outcome per the derived session hold. Mechanical enactment is RETIRED
    (OI-45, ruled 2026-08-20) — the `flip` reading of the derived action
    survives in `flip_verified`'s brief text, but `_apply_flips` writes
    nothing, ever; approval stays a human reviewed-commit act."""
    root = Path(args.root).resolve()
    action, flipped, refusal = flip_verified(root, _split(args.rows))
    return _cli_result(
        refusal, "action: {} ({} row(s) flipped)".format(action, len(flipped))
    )


def _cmd_census(args):
    """Rung 1 by hand: derive the gap census (via census.gap_census) and
    mint the gap-closure rows."""
    root = Path(args.root).resolve()
    lines = census.gap_census(root)
    if not lines:
        _say("the registries name no gaps - nothing to mint.")
        return 0
    minted, refusal = mint_gap_rows(root, lines)
    return _cli_result(
        refusal,
        "census named {} gap(s); minted {} row(s) (the rest have open rows).".format(
            len(lines), len(minted)
        ),
    )


def _cmd_snapshot(args):
    """THE HUMAN PATH to the `last_approved` snapshot: copy every snapshotted
    registry into `docs/archive/last_approved/`.

    APPROVAL AUTHORITY WAS DELIBERATELY NOT MECHANIZED (OI-45, ruled
    2026-08-20) — this refresh is the ONE mechanical toucher of the approval
    record, and it is authority-gated (`--approves` below) rather than
    unconditional. That is a statement about which SCRIPT decides, not about
    who may act: an LLM session or adjudicator is fully expected to move a
    row's Status to `Approved`, and further to `Founded`, through the reviewed
    commit this refresh then copies — at the human's request, or for spine
    content past the declared approval level (`agent_common.human_holds`
    says which). `intake.flip_verified`'s mechanical `_apply_flips` is the
    retired candidate (OI-45 (b)); this copy was never it.

    The owner's hand sequence at a sitting is: edit the Status cells in the
    reviewed commit -> run `intake.py snapshot` -> commit both together. The
    mirror invariant (`acceptance_record.staged_snapshot_findings`) is what makes
    "together" checkable rather than remembered.

    `--seed` is the ONLY way the directory is created, and it exists for one
    commit in the life of a repo: the signing act that first blesses the spine,
    after every pending row has been ruled. Copying before that sitting would
    launder exactly the re-blessing those rows owe (repo-lock D-10's sequencing
    rule, with "stamping hashes" swapped for "copying files").

    `--approves <ref>` NAMES THE APPROVAL ACT, and is needed only when the copy
    would absorb APPROVED text that no `Status` flip in the same registry
    authorises (`baseline_snapshot.refresh_refusal`, 2026-08-20). It is the
    door the adversarial round found standing open: creating the record was
    guarded and rewriting it was not, so a two-commit path — amend an Approved
    row, then refresh — re-blessed the amendment with every check green. The
    ref is a human's citation, recorded into the snapshot's prose stamp; nothing
    validates it, because nothing can. What it buys is that the act is named.
    Traced-cell refreshes (the common case) still need no flag at all.

    IT COPIES OFF-SPINE APPROVAL CELLS AND DOES NOT MOVE THEM, which is the
    distinction OI-30 D3 makes and the reason this path needs no
    `agent_common.human_approves` refusal. `SNAPSHOTTED` includes
    `interfaces.toml`, `external.toml` and `components.toml` precisely so the
    record of what was blessed is whole — but a COPY records a human's decision,
    it never makes one, so no authority question arises. The refusal belongs on
    a WRITER, and this module ships none: `_apply_flips` moves SPINE `status`
    cells only (`acceptance_record.SPINE_CSVS` is its universe). If a future
    command here learns to write an `approval`, it must consult
    `agent_common.human_approves(root / "docs", <registry stem>)` and refuse
    when it answers True — the contract is stated at the predicate, and
    `tests/test_approval_level.py` fails the moment a shipped loop module
    starts writing one."""
    root = Path(args.root).resolve()
    approves = getattr(args, "approves", None)
    written = baseline_snapshot.copy_live(root, seed=args.seed, approves=approves)
    return _cli_result(
        None,
        "snapshot: {} registry file(s) copied to {}{}{}".format(
            len(written),
            baseline_snapshot.SNAPSHOT_DIR,
            " (SEEDED — this is the first snapshot; it blesses the text you just ruled)"
            if args.seed
            else "",
            " (APPROVED BY: {} — recorded in the snapshot's stamp)".format(approves)
            if approves
            else "",
        ),
    )


def main(argv=None):
    # UTF-8 stdio whatever the console codepage (run_py's documented contract:
    # "the kit scripts emit UTF-8 via _utf8_console") — this was the one CLI
    # that never called it, so its refusal banners reached a Windows pipe as
    # cp1252 and broke any UTF-8 reader (found 2026-08-15, sitting sweep).
    ac._utf8_console()
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
    census_cmd = sub.add_parser(
        "census", help="derive the gap census and mint gap-closure rows"
    )
    census_cmd.set_defaults(func=_cmd_census)
    adj = sub.add_parser(
        "adjudicate",
        help="recommend re-verify for spine rows judged no-scope-moved — "
        "mechanical enactment is RETIRED (OI-45); approval stays a human "
        "reviewed-commit act (docs/process.toml [attestation] "
        "human_approval_through)",
    )
    adj.add_argument(
        "--rows", required=True, help="spine row id(s), ;-joined (SR-/LLR-/TC-)"
    )
    adj.set_defaults(func=_cmd_adjudicate)
    # The slot the retired `attest` subcommand reserved, filled. The destination
    # changed — a whole-file copy, not a ledger line or a digest cell — so the
    # name changed with it, and there is deliberately no `--rows`: a whole-file
    # mirror has no row scope to take.
    snap = sub.add_parser(
        "snapshot",
        help="copy every spine + approval-carrying registry into "
        "docs/archive/last_approved/ — the record of WHAT TEXT an approval "
        "blessed. Run it in the same reviewed commit as the Status edits",
    )
    snap.add_argument(
        "--seed",
        action="store_true",
        help="CREATE the snapshot directory. For the FIRST snapshot only, in "
        "the owner's signing commit, after every pending row has been ruled — "
        "seeding earlier blesses text nobody read. Unreachable from every loop "
        "module and hook (pinned by tests/test_baseline_snapshot.py)",
    )
    snap.add_argument(
        "--approves",
        default=None,
        metavar="REF",
        help="NAME THE APPROVAL ACT this refresh rides — a sitting, a log "
        "fragment, a commit. Required only when the copy would absorb approved "
        "text that no Status flip authorises; the ref is recorded into the "
        "snapshot's prose stamp. A traced-cell refresh needs no flag",
    )
    snap.set_defaults(func=_cmd_snapshot)
    args = ap.parse_args(argv)
    if not getattr(args, "cmd", None):
        ap.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
