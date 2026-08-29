"""pending.py — the pending-owner-action read model: what the OWNER still owes.

A READ MODEL OVER THE COMMITTED TREE, and nothing else — the sibling of
`census.py`, which answers the other half of the same question. Where the census
asks *which gaps do the registries name?*, this module asks *which durable
actions is the owner holding?* and answers from three sources and no clock:

    blocked_pending   `queued/` work items carrying a `blockref` — the
                      attestation/approval page each one waits on
    spine_pending     `Drafted` SRs (a first approval is owed) and SRs whose
                      text has DRIFTED from its `docs/archive/last_approved/`
                      copy (a re-attest is owed, process.md §7)
    pause_pending     the tracked `docs/work/pause` declaration

`pending_items` joins the three into the typed model — one `PendingItem` per
action, carrying its `kind` and its rendered pointer line — and everything above
this module consumes THAT rather than the three sources by name:

    traj_status.py    re-exports the sources under their former names, so the
                      `gen_trajectory` facade and the dashboard family are
                      unchanged
    gen_open_items.py renders `pending_block` into section 3 of the generated
                      owner surface `docs/open-items.html`
    dispatch.py       counts `owner_cards` for the §A8 drained-queue banner

WHY THIS IS A MODULE AND NOT PART OF THE DASHBOARD (WI-483, slice 3). Until this
module the derivation lived in `traj_status.py`, a RENDER module inside the
`traj_*` family, reachable only through the ~1,000-line `gen_trajectory` facade —
so the two readers that are not the dashboard each imported that facade to get
at it, and one of them reached in for PRIVATE names (`_blocked_pending`,
`_spine_pending`) across a module boundary. The 2026-08-19 repository review
recorded both as bad edges: the private-name cross-module API (M-02) and
`gen_open_items` importing the large facade for a state query (H-02), the latter
DOCUMENTED by `IF-088` rather than removed. A derivation with three readers
belongs BELOW all three, which is the same cut `census.py` and
`kitlib/station.py` already applied.

NOT `kitlib`, and by the same hard rule that kept the census out: every module
of that package must stay import-clean of the rest of `scripts/`
(`tests/test_bootstrap.py::test_bootstrap_imports_only_the_common_package`),
because `bootstrap.py` imports it. This module reads the work registry through
the validator's loaders and the spine through `traj_parse`, so it imports
siblings by construction and is a plain sibling itself.

THE ITEMS CARRY RENDERED LINES, deliberately. A `PendingItem` is a `kind` plus
the markdown bullet a human reads, because every consumer wants one of exactly
two things — the COUNT of a kind, or the block of lines — and neither needs the
registry row behind the line. Splitting the bullet into fields would buy a
second formatter and a second place for the wording to drift; the `kind` is what
the one caller that discriminates (the dispatcher, which excludes the pause)
needs, and it is a FIELD rather than a substring match on the prose.

Contracts: IF-088 — the seam this module declares (process.md §8;
row of record in docs/requirements/interfaces.toml).

Contract IF-088: the dispatcher's exit banner calls `owner_cards(root)` — the
    same `pending_items(root)` read model the dashboard and the generated
    open-items surface render, minus the tracked-pause kind, whose pause has
    its own earlier exit. Each item is a `PendingItem(kind, line)`: a `kind` of
    `blocked` or `spine`, and the rendered markdown bullet a human reads. The
    kind is a FIELD, so the one caller that discriminates never parses prose to
    make a control-flow decision. The derivation is a pure function of the
    committed tree — sorted, no clocks — so the banner and the owner surfaces
    can never disagree about what is blocking, and the import is deferred: this
    seam costs nothing until an exit banner asks for it.

Stdlib only, cross-platform, deterministic (sorted rows, no clocks) so every
gated region derived from it is byte-stable.

Implements: SR-168, LLR-139, LLR-198
"""

from __future__ import annotations

from typing import NamedTuple

import baseline_snapshot
import check_trajectory as ct
from traj_parse import _spine

# --- the pending-owner-actions projection (WI-234) ------------------------------
# `--status` also splices a second GENERATED block — at the END of
# the generated owner surface docs/open-items.html (WI-322), beside the briefs
# leaves byte-untouched) — projecting every DURABLE pending-owner action so the
# owner's one review surface never misses a hard stop. A pure projection of
# committed-tree state ONLY:
#   (a) `blocked` WI rows carrying a BlockRef (the attestation/approval
#       page);
#   (b) Drafted/DRIFTED SR rows (WI-316): a `Drafted` SR owes an approval, and
#       an SR whose chain has moved away from its `docs/archive/last_approved/`
#       copy owes a re-attest (post-attestation amendment, process.md §7) — one
#       pointer line each, naming the on-demand brief (`trace.py --approve <id>`
#       / `--approve modified`) that carries the depth.
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


class PendingItem(NamedTuple):
    """One durable pending owner action: its source `kind` and its bullet.

    `kind` is one of `blocked`, `spine`, `pause` — a field rather than a prefix
    test on `line`, because the one caller that discriminates (`dispatch`,
    which excludes the pause) would otherwise be parsing prose to make a
    control-flow decision, which is the `NEEDS-HUMAN` lesson (LLR-161)."""

    kind: str
    line: str


BLOCKED, SPINE, PAUSE = "blocked", "spine", "pause"


def blocked_pending(root):
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
            "- **{}** blocked — attest/approve `{}`, then unblock the registry "
            "row.".format(w["id"], w["blockref"])
        )
        ids.add(w["id"])
    return lines, ids


# The SR registry, for the snapshot join. Restated rather than imported from
# `trace.SPINE_FILES[0]`: this module deliberately does not import `trace`
# (the dashboard reads the spine through `traj_parse`), and one path string is
# the cheapest thing in the kit to duplicate.
_SR_REL = "docs/requirements/system-requirements.toml"


def spine_pending(root):
    """Source (e), WI-316: one pointer line per `Drafted` SR (approval owed) and
    per SR whose chain has DRIFTED from the approved snapshot (re-attest owed —
    a post-approval amendment, process.md §7). Only SR rows project — deliberate
    surface economy, never
    attestation scope (a row's Status answers for its own cells, owner ruling
    2026-08-17m): a flagged LLR/TC under an unflagged SR shows in the registry
    and the trace report, not here. Durable committed-tree state, so these
    join the freshness-gated PURE region; pointer-only per this block's charter
    — the depth (per-cell before/after) lives in the on-demand brief the line
    names, `trace.py --approve modified`, never here. Sorted by id, no clocks.

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
    # approval. Only the SR arm projects (the docstring's surface-economy
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
                "project-trajectory/scripts/trace.py --approve {}`.".format(
                    sid, phase_note, title, sid
                )
            )
        else:
            lines.append(
                "- **{} DRIFTED from the approved snapshot**{}: {} — its "
                "approved text differs from its copy in `{}` while its own "
                "Status still claims approval, so nobody has read the change. "
                "Re-attest it, then run `intake.py snapshot` in the same "
                "commit; before/after brief: `python "
                "project-trajectory/scripts/trace.py --approve modified`.".format(
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


def pause_pending(root):
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


def pending_items(root):
    """THE READ MODEL: every durable pending owner action, in surface order
    (blocked rows, then spine rows owing an approval or re-attest, then the
    tracked pause). Deterministic and committed-tree-pure, so a caller may
    count it, filter it or render it and get the same answer the owner surfaces
    show — which is the WI-381 amendment's requirement (ruled 2026-08-01) held
    by construction rather than by three callers agreeing to be careful."""
    blocked_lines, _blocked_ids = blocked_pending(root)
    items = [PendingItem(BLOCKED, line) for line in blocked_lines]
    items += [PendingItem(SPINE, line) for line in spine_pending(root)]
    items += [PendingItem(PAUSE, line) for line in pause_pending(root)]
    return tuple(items)


def owner_cards(root):
    """The pending items a DRAINED-QUEUE banner names — every kind except the
    pause.

    The pause is excluded because a paused station has its own, earlier exit:
    naming it again at the drain would send the owner to `open-items.html` about
    a stop they were already stopped by. Same read as the owner surfaces, one
    declared filter — not a second derivation."""
    return tuple(i for i in pending_items(root) if i.kind != PAUSE)


PENDING_LEAD = (
    "_Pending owner actions — a generated projection of durable, "
    "committed-tree state (blocked rows with an approve/attest pointer, "
    "Drafted/drifted spine rows owing an approval or re-attest, and the "
    "tracked pause declaration); regenerated by `python "
    "project-trajectory/scripts/gen_trajectory.py --status`, do not hand-edit. "
    "This section is freshness-gated by the harness `status-map` step. The "
    "briefs above are hand-authored and untouched by regeneration._"
)

PENDING_NONE = "_None — no durable owner action is pending._"


def pending_block(root):
    """The GENERATED PENDING block CONTENT (between the markers) for the
    generated owner surface: the read model above, rendered. A pure function of
    the committed tree — deterministic (sorted, no clocks) — so the harness
    `open-items` freshness gate byte-compares the WHOLE block through
    `gen_open_items.py --check` (the renderer since WI-322, NOT `--status`) and
    it reads identically in any clone. (The dispatcher-era machine-local
    advisory region retired with the dispatcher at concurrency-restructure
    Phase 5.)"""
    items = pending_items(root)
    body = "\n".join(i.line for i in items) if items else PENDING_NONE
    return "{}\n\n{}".format(PENDING_LEAD, body)
