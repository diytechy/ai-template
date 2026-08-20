"""The --status snapshot + pending projection (WI-280 split of gen_trajectory.py).

The docs/status.md GENERATED STATUS splice (WI-202), the pending-owner-
actions derivation gen_open_items renders (WI-234), and the generated
Ready-frontier lines. The facade re-exports, so consumers are unchanged.

Contracts: IF-084, IF-125, IF-130 — the seams this module declares (process.md
§8; rows of record in docs/requirements/interfaces.toml): IF-084 is IF-056's
derivation-loader read of check_trajectory, as held by the sibling that now
carries the import; IF-125 is the READ-ONLY consumption of the `last_approved`
baseline (IF-123), so the generated surface reports pending amendments against
what was blessed rather than against HEAD, and never refreshes the snapshot;
IF-130 is `_stage_line`'s call to derive_gate.bar_label, the ONE rendering
home for the release-ceiling note, so this surface can never word the
withheld top bar differently from the others.
"""

import re
import sys

import baseline_snapshot
import check_trajectory as ct

# The bar-name RENDERER only (`bar_label`) — not a second gate derivation. The
# value still comes from `docs/gate`'s cached basis line; this module asks
# derive_gate how a human should READ that value, which is the one home for the
# OI-30 D2 ceiling note.
import derive_gate
import traj_parse
from traj_parse import _spine, cmp_rows, spine_stats


# --- the docs/status.md derived-snapshot block (WI-202) ------------------------
# `--status` splices a GENERATED block into the OTHERWISE hand-authored status.md
# carrying ONLY derived facts (the spine + derived gate + the open-items
# one-liners), the gen_arch_map --doc block-splice idiom. Its
# `--check` is the freshness successor to the WI-200 forward-only token guard:
# with this marker present, check_trajectory.status_forward_only_findings stands
# its token rule down (the marker is `<!-- BEGIN GENERATED ... -->`, which its
# _STATUS_GENERATED_RE matches) and THIS byte-compare becomes the invariant. The
# forward-only INTENT — Next action, the OI briefs, Scope — stays hand-authored
# OUTSIDE the markers. Opt-in: a status.md without the marker pair is left
# untouched, so `--status --check` passes vacuously downstream.
STATUS_MD = "docs/status.md"
STATUS_BEGIN = "<!-- BEGIN GENERATED STATUS -->"
STATUS_END = "<!-- END GENERATED STATUS -->"
# derive_gate.py's cached `# basis:` line in docs/gate — the fresh, freshness-
# guarded derivation the status snapshot PROJECTS (never recomputes).
_GATE_BASIS_RE = re.compile(r"^#\s*basis:\s*(.+)$", re.M)

# --- the pending-owner-actions projection (WI-234) ------------------------------
# `--status` also splices a second GENERATED block — at the END of
# the generated owner surface docs/open-items.html (WI-322), beside the briefs
# leaves byte-untouched) — projecting every DURABLE pending-owner action so the
# owner's one review surface never misses a hard stop. A pure projection of
# committed-tree state ONLY:
#   (a) `blocked` WI rows carrying a BlockRef (the attestation/ratification
#       page);
#   (b) Drafted/DRIFTED SR rows (WI-316): a `Drafted` SR owes an approval, and
#       an SR whose chain has moved away from its `docs/archive/last_approved/`
#       copy owes a re-attest (post-attestation amendment, process.md §7) — one
#       pointer line each, naming the on-demand brief (`trace.py --ratify <id>`
#       / `--ratify modified`) that carries the depth.
#   (c) a tracked `docs/work/pause` (concurrency-restructure §5.6): one
#       `Paused since <date>` line, the declared reason rendered verbatim (no
#       clock), so an open pause is a visible accruing cost.
# One line per pending action with a pointer (never a brief — the depth stays in
# the hand-authored briefs). Deterministic (sorted rows, no clocks), so the
# gated region is byte-stable; a pure function of the committed tree, so the
# `--check` freshness gate byte-compares the WHOLE block in any clone. Opt-in:
# a repo carrying no open-items registry renders nothing.
# (The dispatcher-era MACHINE-LOCAL advisory region — refs/llm/* conflict/
# reservation/quarantine/stranded-train lines, excluded from the compare under
# M-10/WI-266 because those refs never transported — retired with the
# dispatcher at concurrency-restructure Phase 5, and the run-state ask source
# with it: git history and the integrator's own refusals are the record now.)


# --- the status.md derived snapshot (WI-202) -----------------------------------


def _gate_facts(root):
    """The derived-gate facts for the status snapshot, read from `docs/gate` — the
    cached, freshness-guarded SSOT (derive_gate.py owns it; check.py's `derived-gate`
    step keeps it fresh). Returns `(gate_value, basis)`: the gate is the first
    non-comment line; `basis` parses the `# basis:` line's `k=v` tokens
    (SN/SR/LLR/TC/drafts/computed/phase/per-phase) when present, else `{}` (a legacy
    hand-set gate with no basis line). The snapshot PROJECTS this rather than
    recomputing what derive_gate already cached — one home for the derivation."""
    p = root / "docs" / "gate"
    if not p.exists():
        return "", {}
    text = p.read_text(encoding="utf-8", errors="replace")
    gate = ""
    for ln in text.splitlines():
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            gate = ln
            break
    basis = {}
    m = _GATE_BASIS_RE.search(text)
    if m:
        for tok in m.group(1).split():
            if "=" in tok:
                k, v = tok.split("=", 1)
                basis[k] = v
    return gate, basis


def _spine_counts(root, basis):
    """`{SN,SR,LLR,TC}` string counts for the snapshot: the fresh `docs/gate`
    basis line when present (the authoritative derivation), else a direct count
    of the registries (the legacy-gate fallback)."""
    if all(k in basis for k in ("SN", "SR", "LLR", "TC")):
        return {k: basis[k] for k in ("SN", "SR", "LLR", "TC")}
    st = spine_stats(root)
    return {
        "SN": str(st["sn_total"]),
        "SR": str(st["sr_total"]),
        "LLR": str(st["llr_total"]),
        "TC": str(st["tc_total"]),
    }


_OI_ID_RE = re.compile(r"\bOI-\d+\b")


def _clean_oneliner(s):
    """Normalize a projected one-liner: Markdown link `[text](url)` -> its text,
    stray emphasis/backticks dropped, whitespace collapsed. Keeps the snapshot
    scannable and byte-stable regardless of the brief's inline markup."""
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"\*\*|`", "", s)
    return re.sub(r"\s+", " ", s).strip()


def _first_sentence(s):
    """The first sentence of `s` (up to the first sentence-ending `.`/`!`/`?`),
    else all of `s`. A `;`-joined clause stays whole — only a full stop ends it."""
    m = re.search(r"^(.*?[.!?])(?:\s|$)", s)
    return (m.group(1) if m else s).strip()


def _open_item_oneliners(root):
    """`[(OI-id, one-liner)]` for every PENDING decision, id-order — the status
    snapshot's one-line-per-item projection.

    Reads the open-items registry (WI-322, OI-10 ruled option (b); TOML since
    repo-lock §8.1, either carrier resolves):
    the registry is the source and `docs/open-items.html` is the rendered owner
    surface, so a markdown section parse has nothing left to parse. The
    one-liner is the row's `OneLine` cell, else the first sentence of its
    `Recommendation` — the same fallback the markdown contract had, kept so a
    row that states only a recommendation still projects something useful.
    Empty when the registry is absent (a repo carrying no decisions)."""
    p = root / "docs" / "requirements" / "open-items.toml"
    if ct.spine_carrier.resolve(p) is None:
        return []
    out = []
    # Through the CARRIER, not `read_rows`: this projection is spliced into
    # `status.md` and an unreadable registry that came back as no rows would
    # publish "no pending decisions" — the owner's queue reporting empty because
    # it could not be parsed. `load` raises there and returns [] only when the
    # registry is genuinely absent.
    for row in ct.spine_carrier.load(p, "OI-ID"):
        oid = (row.get("OI-ID") or "").strip()
        if not _OI_ID_RE.fullmatch(oid) or oid.endswith("-000"):
            continue
        if (row.get("Status") or "").strip().lower() != "pending":
            continue  # a ruled row is history; the Decisions log holds it
        one = (row.get("OneLine") or "").strip()
        if not one:
            reco = (row.get("Recommendation") or "").strip()
            one = _first_sentence(reco) if reco else ""
        out.append((oid, _clean_oneliner(one)))
    return sorted(out, key=lambda t: int(t[0].split("-")[1]))


# --- the pending-owner-actions projection sources (WI-234) ----------------------


def _blocked_pending(root):
    """Source (a): `(lines, ids)` — one line per blocked work item, and the set
    of WI ids covered. In the spec-folder registry blocked is DERIVED: a
    `queued/` item carrying a `blockref` key (concurrency-restructure §2.1 —
    `blocked` has no directory). The pointer is the BlockRef path."""
    wis, _ = ct.load_wis(ct.read_registry_rows(root / ct.WI_CSV))
    lines, ids = [], set()
    for w in sorted(wis, key=lambda w: w["id"]):
        if w["status"] != "queued" or not w["blockref"]:
            continue
        lines.append(
            "- **{}** blocked — attest/ratify `{}`, then unblock the registry "
            "row.".format(w["id"], w["blockref"])
        )
        ids.add(w["id"])
    return lines, ids


# The SR registry, for the snapshot join. Restated rather than imported from
# `trace.SPINE_FILES[0]`: this module deliberately does not import `trace`
# (the dashboard reads the spine through `traj_parse`), and one path string is
# the cheapest thing in the kit to duplicate.
_SR_REL = "docs/requirements/system-requirements.toml"


def _spine_pending(root):
    """Source (e), WI-316: one pointer line per `Drafted` SR (approval owed) and
    per SR whose chain has DRIFTED from the approved snapshot (re-attest owed —
    a post-approval amendment, process.md §7). Only SR rows project — deliberate
    surface economy, never
    attestation scope (a row's Status answers for its own cells, owner ruling
    2026-08-17m): a flagged LLR/TC under an unflagged SR shows in the registry
    and the trace report, not here. Durable committed-tree state, so these
    join the freshness-gated PURE region; pointer-only per this block's charter
    — the depth (per-cell before/after) lives in the on-demand brief the line
    names, `trace.py --ratify modified`, never here. Sorted by id, no clocks.

    THE `Planned` ARM LEFT AT D-9 STEP 5, with the word. It had joined at step 2
    because a Planned SR projected NOTHING on the owner's own pending-actions
    surface — the loudest instance of the `Planned`-reads-as-`Bananas` finding.
    OI-30 D1 then ruled the fold: those rows now read `Approved`, and an approved
    row owes nothing HERE. What it may still owe is caught by the drift arm below
    and, once the snapshot is seeded, by the UNANCHORED rule — an approval with
    no copy recording it — which is where "approved but nobody signed it" belongs.

    DRIFT JOINED AT D-9 STEP 4, and it is the arm no Status cell can carry: a
    row whose text has moved away from its copy in
    `docs/archive/last_approved/` while its own Status still claims approval.
    That is the state the migration exists for — under the new ladder an
    amendment no longer flips its row, so a projection keyed on status words
    alone goes quiet exactly when it matters. Vacuous while no snapshot exists.

    THE `Modified` ARM LEFT AT STEP 7, and this is the surface that shows why the
    steps were ordered as they were: the drift arm had already been rendering
    beside it since step 4, so the projection lost a word and kept the state.
    A projection that had swapped the two in ONE commit would have gone quiet for
    exactly as long as it took someone to notice."""
    # `skip_example=True`: a copied template's `-000` example row owes no
    # ratification. Only the SR arm projects (the docstring's surface-economy
    # note), so the LLR/TC arms of the loader go unused here.
    srs = _spine(root, skip_example=True)[0]
    snapshot = baseline_snapshot.load_all(root)
    snap_srs = baseline_snapshot.rows_for(snapshot, _SR_REL, "SR-ID")
    lines = []
    for r in sorted(srs, key=lambda x: x["SR-ID"]):
        status = (r.get("Status") or "").strip().lower()
        drifted = baseline_snapshot.is_drifted(_SR_REL, "SR-ID", r, snap_srs)
        if status != "drafted" and not drifted:
            continue
        sid = r["SR-ID"]
        title = (r.get("Title") or "").strip() or "(untitled)"
        phase = (r.get("Phase") or "").strip()
        phase_note = " (phase {} pulls the derived gate)".format(phase) if phase else ""
        if status == "drafted":
            lines.append(
                "- **{} `Drafted` — approval owed**{}: {} — approve in a "
                "reviewed Status-change commit (`Drafted`→`Approved`; the "
                "`gate-advance` skill); hierarchy brief: `python "
                "project-trajectory/scripts/trace.py --ratify {}`.".format(
                    sid, phase_note, title, sid
                )
            )
        else:
            lines.append(
                "- **{} DRIFTED from the approved snapshot**{}: {} — its "
                "ratified text differs from its copy in `{}` while its own "
                "Status still claims approval, so nobody has read the change. "
                "Re-attest it, then run `intake.py snapshot` in the same "
                "commit; before/after brief: `python "
                "project-trajectory/scripts/trace.py --ratify modified`.".format(
                    sid, phase_note, title, baseline_snapshot.SNAPSHOT_DIR
                )
            )
    return lines


# Byte-identical with `agent_common.PAUSE_MALFORMED`: the coordinator's reader
# and this projection must say the same thing about an unreadable pause file.
# Copied rather than imported — this module's ONE sanctioned sibling import is
# check_trajectory (see the header), and a renderer must not start depending on
# the coordinator layer for a string. `tests/test_gen_trajectory_pending.py`
# pins the two equal, so the copy cannot drift silently.
PAUSE_MALFORMED = "<malformed docs/work/pause — fix or delete it>"


def _pause_pending(root):
    """Source (f): the tracked pause declaration `docs/work/pause`
    (`docs/concurrency-restructure.md` §5.6) — TOML `reason` + `since`. Zero or
    one bullet, so an open pause is a VISIBLE accruing cost rather than a
    forgotten one (the stale-reason lesson); unpausing is a deletion commit, so
    the bullet clears itself.

    Committed-tree-PURE and deterministic: the declared `since` renders
    VERBATIM — never an age computed from `now()`, which would make the gated
    region change without a commit. Fail-CLOSED like the coordinator's reader: a
    malformed file still projects, loudly, because a pause you cannot read is
    still a pause. Where that reader NORMALIZES (its callers get a typed dict),
    this one only has to answer "readable or not" before formatting, so it asks
    once and catches — same outcomes, a renderer's shape."""
    import tomllib  # the module's only TOML reader; kept local to this one use

    p = root / "docs" / "work" / "pause"
    if not p.is_file():
        return []
    try:
        declared = tomllib.loads(p.read_text(encoding="utf-8"))
        reason, since = declared["reason"], declared.get("since") or ""
        if not isinstance(reason, str):
            raise TypeError("pause `reason` must be text")
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError, KeyError, TypeError):
        reason, since = PAUSE_MALFORMED, ""
    return [
        "- **Paused{}** — {}.".format(
            " since {}".format(since) if since else "",
            reason or "no reason declared",
        )
    ]


def pending_block(root):
    """The GENERATED PENDING block CONTENT (between the markers) for the
    generated owner surface: blocked WI rows with a BlockRef + Drafted/DRIFTED
    spine rows owing a ratification/re-attest + the tracked `docs/work/pause`
    declaration. A pure function of the committed tree — deterministic (sorted,
    no clocks) — so the harness `open-items` freshness gate byte-compares the
    WHOLE block through `gen_open_items.py --check` (the renderer since
    WI-322, NOT `--status`) and it reads identically in any clone. (The
    dispatcher-era machine-local advisory region retired with the dispatcher
    at concurrency-restructure Phase 5.)"""
    pure_lead = (
        "_Pending owner actions — a generated projection of durable, "
        "committed-tree state (blocked rows with a ratify/attest pointer, "
        "Drafted/drifted spine rows owing an approval or re-attest, and the "
        "tracked pause declaration); regenerated by `python "
        "project-trajectory/scripts/gen_trajectory.py --status`, do not hand-edit. "
        "This section is freshness-gated by the harness `status-map` step. The "
        "briefs above are hand-authored and untouched by regeneration._"
    )
    blocked_lines, _blocked_ids = _blocked_pending(root)
    pure_items = blocked_lines + _spine_pending(root) + _pause_pending(root)
    pure_body = (
        "\n".join(pure_items)
        if pure_items
        else "_None — no durable owner action is pending._"
    )
    return "{}\n\n{}".format(pure_lead, pure_body)


# The eight-rung stage ladder's descriptions, for the generated snapshot line.
# STATE units: a repo is IN a stage and CLEARS a bar (process.md §4 "The stage
# ladder"). Derived by derive_gate.py and read here off `docs/gate`'s `# basis:`
# line, never recomputed.
#
# THE ORDINAL IS NOT IN THIS TABLE, and that is the whole point of the label
# carrier (OI-21): the renderer reads `stage-ord=`/`stage-of=` off the same basis
# line, so inserting a rung self-corrects every rendered "stage N of M" with no
# edit here. This map holds only the human sentence each label expands to.
_STAGE_LABELS = {
    "DevStg-Needs": "vision and stakeholder needs in work",
    "DevStg-Boundary": "system boundary interfaces in work",
    "DevStg-Reqs": "requirement definition in work",
    "DevStg-Arch": "architecture (partition) in work",
    "DevStg-LLReqs": "LLR definition in work",
    "DevStg-Tests": "test-case definition in work",
    "DevStg-Impl": "implementation in work",
    "DevStg-Release": "nothing in work; release checklist available",
}


def _stage_line(gate, basis, gate_detail):
    """The snapshot's first bullet, STAGE-first.

    The bar value alone cannot say whether a boundary is ahead or behind, and —
    being a min floored by any Drafted row — it reads identically for a fresh
    scaffold and a mature spine holding one draft. The stage is the state; the bar
    is what must next be cleared, which is also the strictness the harness runs at.

    A `docs/gate` predating the `stage=` field, or carrying a label this ladder
    does not name (including a cache still holding the retired integer form),
    degrades to the bar-only wording rather than inventing a stage — the same
    absent-means-absent direction derive_gate takes.

    THE BAR NAME IS RENDERED THROUGH `derive_gate.bar_label`, not interpolated
    raw: while the OI-30 D2 ceiling holds, the name carries "(Release: pending
    harness driver)" so a reader never mistakes a withheld top bar for a
    regression. One home, so this surface and `PROJECT_STATE.html` (which renders
    this same block) cannot disagree."""
    gate_txt = derive_gate.bar_label(gate) if gate else "(none)"
    stage = basis.get("stage")
    link = "[`derive_gate.py`](../project-trajectory/scripts/derive_gate.py)"
    if stage in _STAGE_LABELS:
        ord_txt = basis.get("stage-ord")
        of_txt = basis.get("stage-of")
        # The position rides the basis line; when an older cache omits it, name
        # the rung without a position rather than guessing one.
        where = (
            "stage {o} of {n}".format(o=ord_txt, n=of_txt)
            if ord_txt is not None and of_txt is not None
            else "stage"
        )
        return (
            "- **In stage:** **{s}** ({where}, {label}) · **next to clear: {g}**"
            "{detail} — one vocabulary, and the VERB says which reading: a repo "
            "is IN a stage and CLEARS a stage. {link} derives both, cached to "
            "[`docs/gate`](gate).".format(
                s=stage,
                where=where,
                label=_STAGE_LABELS[stage],
                g=gate_txt,
                detail=gate_detail,
                link=link,
            )
        )
    return (
        "- **Next bar:** derived **{g}**{detail} — the harness at that bar is "
        "the bar. {link} derives it, cached to [`docs/gate`](gate).".format(
            g=gate_txt, detail=gate_detail, link=link
        )
    )


def status_block(root):
    """The GENERATED STATUS block CONTENT (between the markers) for docs/status.md:
    the derived gate + spine snapshot (projected from `docs/gate`, the freshness-
    guarded SSOT) plus the open-items one-liners (from the registry). Derived
    facts ONLY — the forward-only intent stays hand-authored outside the markers.
    Deterministic (no clocks), so the `--status --check` byte-compare is stable,
    exactly like the arch-map / dashboard freshness gates."""
    gate, basis = _gate_facts(root)
    counts = _spine_counts(root, basis)
    seams = len(ct.load_ifs(ct.spine_carrier.load(root / ct.IF_CSV, "IF-ID")))
    comps = len(cmp_rows(root))

    gate_bits = []
    if basis.get("per-phase"):
        gate_bits.append("per-phase `{}`".format(basis["per-phase"]))
    if basis.get("phase"):
        gate_bits.append("derived current **phase={}**".format(basis["phase"]))
    gate_detail = " ({})".format(", ".join(gate_bits)) if gate_bits else ""

    drafts = basis.get("drafted")  # renamed with the value at D-9 step 5
    draft_bit = ""
    if drafts is not None:
        draft_bit = " ({} draft{})".format(drafts, "" if drafts == "1" else "s")

    lines = [
        "_Derived facts — regenerated by `python "
        "project-trajectory/scripts/gen_trajectory.py --status`; do not hand-edit "
        "(the forward-only intent below is hand-authored)._",
        "",
        _stage_line(gate, basis, gate_detail),
        "- **Spine:** **SN={sn} SR={sr} LLR={llr} TC={tc}**{d} · {seams} seam{sp} · "
        "{comps} component{cp}.".format(
            sn=counts["SN"],
            sr=counts["SR"],
            llr=counts["LLR"],
            tc=counts["TC"],
            d=draft_bit,
            seams=seams,
            sp="" if seams == 1 else "s",
            comps=comps,
            cp="" if comps == 1 else "s",
        ),
    ]
    ois = _open_item_oneliners(root)
    if ois:
        # The LIVE carrier's name, never a hardcoded suffix: this block is
        # spliced into status.md, and a link at the file the repo no longer has
        # is a broken link on the working surface (check_docs's own hard
        # finding), manufactured by a generator.
        oi_rel = ct.spine_carrier.stem("requirements/open-items.toml") + (
            ct.spine_carrier.resolve(
                root / "docs" / "requirements" / "open-items.toml"
            ).suffix
        )
        lines.append(
            "- **Open items** _(pending rows of [{oi}]({oi}); each ".format(oi=oi_rel)
            + "item's blast radius, options and recommendation render in "
            "[open-items.html](open-items.html), the generated owner surface):_"
        )
        lines.extend("  - **{}** — {}".format(oid, one) for oid, one in ois)
    lines.extend(_frontier_lines(root))
    return "\n".join(lines)


# The forward-looking WI list is DERIVED here (WI-284), not hand-authored: the
# scheduler's dependency-ready frontier in build order. Because it lives inside
# the generated block (which check_trajectory.status_forward_only_findings
# exempts) AND is drawn only from ready — i.e. open, never-`done` — rows, a WI
# that integrates simply drops out on the next `--status` regen: the integrator
# runs that regen in _regenerate_disposition_artifacts, so status.md can no
# longer strand a closed id (the cascade that burned WI-276). Pure/deterministic
# (registry-derived, no reservations, no clocks), so `--status --check` stays a
# stable byte-compare. Capped so a long backlog stays one readable line-group.
_FRONTIER_CAP = 12


def _frontier_lines(root):
    """The `- **Ready frontier**` generated bullet: dependency-ready WIs in
    scheduler order, id + one-line title. Empty when nothing is ready (a drained
    or placeholder registry) OR when schedule.py is unavailable (a scaffold that
    omits it), so the block stays byte-stable and vacuous."""
    if traj_parse.schedule is None:
        return []
    try:
        rows = traj_parse.schedule.load_registry_rows(
            root / "docs/requirements/work-items.csv"
        )
        wis = traj_parse.schedule.load_wis(rows)
        # reserved=None -> pure registry frontier
        ready = traj_parse.schedule.frontier(wis)
    except (OSError, ValueError):
        return []
    if not ready:
        return []
    titles = {w["id"]: w.get("title", "") for w in wis}
    prios = {w["id"]: w.get("priority", 0) for w in wis}
    shown = ready[:_FRONTIER_CAP]
    out = [
        "- **Ready frontier** _(dependency-ready WIs in build order — generated "
        "from the scheduler; a closed WI drops out automatically, so this list "
        "is never stale and never names a `done` id):_"
    ]
    for r in shown:
        wid = r["id"]
        p = prios.get(wid, 0)
        pri = " `P{}`".format(p) if p else ""
        title = _clip_title(titles.get(wid, ""))
        out.append("  - **{}**{} — {}".format(wid, pri, title))
    if len(ready) > _FRONTIER_CAP:
        out.append(
            "  - _(+{} more ready — see the dashboard)_".format(
                len(ready) - _FRONTIER_CAP
            )
        )
    return out


def _title_clause(title):
    """The leading clause of a WI Title — the name of the work, before the
    rationale the registry cell carries after it."""
    return title.split(" - ")[0].split(" — ")[0].strip() or "(untitled)"


def _clip_title(title, limit=90):
    """First clause of a WI Title, clipped — the registry titles are long. The
    status.md frontier line still budgets by character (one markdown line, and
    status.md carries its own line budget); the dashboard card does not — see
    `_next_work_title`."""
    head = _title_clause(title)
    if len(head) > limit:
        head = head[: limit - 1].rstrip() + "…"
    return head


def _splice_status(doc_text, content):
    """Replace the text between the STATUS markers with `content`. Returns
    `(new_text, present)`; `present` is False when the marker pair is absent — the
    opt-in posture, a status.md without markers is left untouched so `--status
    --check` passes vacuously downstream. A duplicated marker is refused (it would
    make the splice ambiguous), the gen_arch_map.splice_region rule."""
    if STATUS_BEGIN not in doc_text or STATUS_END not in doc_text:
        return doc_text, False
    if doc_text.count(STATUS_BEGIN) > 1 or doc_text.count(STATUS_END) > 1:
        raise SystemExit(
            "{}: duplicated STATUS marker; keep exactly one {} / {} pair".format(
                STATUS_MD, STATUS_BEGIN, STATUS_END
            )
        )
    pre = doc_text.split(STATUS_BEGIN)[0]
    post = doc_text.split(STATUS_END)[1]
    return "{}{}\n{}\n{}{}".format(pre, STATUS_BEGIN, content, STATUS_END, post), True


def run_status(root, check):
    """`--status` mode: splice the derived snapshot into docs/status.md (or, with
    `check`, byte-compare and fail on drift). Vacuous — exit 0 — when status.md is
    absent or carries no marker pair (the opt-in posture)."""
    path = root / STATUS_MD
    if not path.exists():
        print("gen_trajectory: no {} — nothing to splice (vacuous).".format(STATUS_MD))
        return 0
    current = path.read_text(encoding="utf-8")
    updated, present = _splice_status(current, status_block(root))
    if not present:
        print(
            "gen_trajectory: {} has no GENERATED STATUS markers — vacuous (add the "
            "{} / {} pair to opt in).".format(STATUS_MD, STATUS_BEGIN, STATUS_END)
        )
        return 0
    if check:
        if updated != current:
            print(
                "status snapshot STALE in {}: run `python "
                "scripts/gen_trajectory.py --status`".format(STATUS_MD),
                file=sys.stderr,
            )
            return 1
        print("status snapshot up to date.")
        return 0
    if updated == current:
        print(
            "gen_trajectory: {} status snapshot already up to date.".format(STATUS_MD)
        )
    else:
        # newline="\n" via open() (write_text(newline=) is 3.10+; scripts stay
        # 3.9-runnable, floor 3.11): LF on every OS so the generated block stays
        # byte-stable regardless of a downstream .gitattributes rule.
        with path.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write(updated)
        print("gen_trajectory: status snapshot regenerated -> {}".format(STATUS_MD))
    return 0
