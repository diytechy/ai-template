#!/usr/bin/env python3
"""baseline_snapshot.py — the `last_approved` snapshot: what the spine looked
like when a human last blessed it.

Stack-agnostic, standard-library only (Python 3.11+, Windows/POSIX).

WHY THIS EXISTS (owner directive 2026-08-15; design:
docs/plans/2026-08-15-baseline-snapshot-design.md). Every "has this attested row
changed?" question in the kit used to be answered by DERIVING a baseline from
git — `trace._attested_baseline` walked the registry's history for the newest
commit at which the row read `Verified` (now `Approved`). That derivation is correct only while
every amendment flips its row's Status in the same commit, and D-9 deletes the
flip: under the new ladder an approved row STAYS approved while its text is
amended, so the newest-approved revision is HEAD and the diff is empty BY
CONSTRUCTION. The brief would return a clean bill forever, at exit 0, on exactly
the rows a sitting exists to judge.

So the baseline moves OUT of git history and onto disk: when an approval lands,
the registries are COPIED, byte for byte, into `docs/archive/last_approved/`.
Every comparison — the adjudicator, the human re-attest read, the HTML
generators — diffs the live registries against that copy. No hashes, no anchor
columns, no commit-id walk. The baseline becomes something a human can open in
an editor and diff with `git diff`, which is itself an argument for the design.

THREE PROPERTIES DO THE WORK, and each is worth stating because each replaces a
piece of machinery that no longer needs to exist:

  1. **Whole files, never extracted rows.** The copy is byte-for-byte, so
     "snapshot file == live file at the copy commit" is a DECIDABLE property —
     `check_trajectory.staged_snapshot_findings` is the guard that makes a
     hand-edited or partial snapshot fail loudly. Row extraction would destroy
     that, would re-serialise TOML (normalising away comments and authored
     ordering, which is the whole reason `intake._flip_status_lines` exists),
     and would silently drop the normative prose that lives OUTSIDE the rows.
  2. **The snapshot keeps each row's own `Status` cell.** That is what makes
     the UNANCHORED rule decidable: a live row claiming approval whose snapshot
     copy reads *below* approval is an approval that never rode a copy — the
     precise laundering this mechanism exists to catch.
  3. **Vacuous by absence, never by silence.** No directory means "this repo
     has approved nothing yet", which is honest and free for a fresh adopter.
     But once the directory exists, a missing registry INSIDE it is an error,
     and a snapshot file that does not parse RAISES rather than reading as
     empty — `{}` and `None` are opposite claims, and the empty one means
     "re-bless everything with no diff shown".

REPO-RELATIVE PATHS ARE PRESERVED UNDER THE SNAPSHOT ROOT
(`<root>/docs/archive/last_approved/docs/requirements/...`). `spine_carrier`'s
`resolve`/`carriers`/`stem` all take a registry path, so `snapshot_root / rel`
reuses every existing resolver verbatim, carrier fallback included. Flattening
would need a second path vocabulary and would give the resolver nothing to
resolve.

WHY `docs/archive/` IS THE RIGHT HOME, despite "archive is design history, not
a working surface": the placement is ACTIVELY load-bearing.
`check_vocab.EXEMPT_GLOBS` exempts `docs/archive/*`, and the snapshot
legitimately holds the PREVIOUS vocabulary — so anywhere else would red the
vocabulary enforcer on every signing. `check_docs._in_archive` exempts it from
orphan/stale findings and `check_doc_refs.RECORD_PREFIXES` keeps its inherited
citations from dangling. `check_trajectory.ARCHIVE_SPECS_DIR` already reads
archive as live machinery input, so the class is not new.

STATUS OF THIS MODULE, 2026-08-15: READER-FIRST AND ADVISORY. Nothing in the
kit writes a snapshot yet — `docs/archive/last_approved/` does not exist in this
repo, so every function here is vacuous, by design, until the owner's signing
act seeds it (migration step 6). `unanchored_findings` returns advisory strings
and joins no failure set; it is promoted to an integrity-class ERROR at
migration step 7, and not before, because against a pre-seed or pre-rename
snapshot it would red every row.

VOCABULARY NOTE — THE TRANSITIONAL MAPPING IS GONE (D-9 step 5, 2026-08-15).
This module was written against `Approved` before the value existed, and read
the two pre-rename values that together carried the claim (`Verified` and
`Planned`). Step 5 renamed both into `Approved`, so the spine arm of
`_claims_approval` collapsed to the single value its own docstring promised —
deleted, not re-keyed. THE SKEW THIS LEAVES IS REAL AND IS THE DESIGN'S §B6
axis 3: a snapshot copied BEFORE the rename speaks the retired words and would
read as unanchored everywhere, which is why the snapshot is ONE GENERATION,
replaced wholesale at each signing and never migrated in place, and why the
first seed happens AFTER the rename (step 6) and the UNANCHORED rule is armed
only after that (step 7).

Contracts: IF-123, IF-128, IF-129 — the seams this module declares (process.md
§8; rows of record in docs/requirements/interfaces.toml). IF-123 is what this
module PROVIDES; IF-128 and IF-129 are what it consumes — the registry CARRIER
and the ONE cell-comparison basis. MINTED 2026-08-15 (log 2026-08-15h) with the
design row LLR-173 and TC-167, closing the gap the previous version of this line
recorded honestly: the module shipped with no spine coverage of any kind. The
three rows that consume it are IF-124 (adjudicate_brief), IF-125 (traj_status)
and IF-126 (gen_open_items), each declared by its own module; `intake` is the
WRITER and is named as IF-123's counterpart. Everything here is PROVISIONAL —
the parent SR and the owner cells are recorded picks for the sitting to
overturn.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

# Sibling imports, the sanctioned idiom (see trace.py): run as a subprocess this
# script's own dir is sys.path[0], and the guard covers an in-process import (a
# test) whose sys.path does not yet carry scripts/.
try:
    import check_trajectory
    import derive_gate
    import spine_carrier
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import check_trajectory
    import derive_gate
    import spine_carrier

# The snapshot's root, repo-relative. One generation only: it is REPLACED
# WHOLESALE at each approval, never migrated in place — git holds the history,
# and a snapshot edited forward would be a second ledger of what was blessed.
SNAPSHOT_DIR = "docs/archive/last_approved"

# The prose stamp's filename. Rendered for a human, PARSED BY NOTHING (design
# §F8, repo-lock D-10's tripwire): every machine fact comes from the copied
# files or from git, so this file can never quietly become the ledger the
# mechanism replaced.
README = "README.md"

# The registries a signing copies. FOUR SPINE plus THREE OFF-SPINE, and the
# second group is not padding: `interfaces.toml` and `external.toml` carry
# `approval` cells and `components.toml` a `state` cell that only a human may
# move. A human-only approval cell with no baseline reopens the
# "approved text moved and nobody saw" hole exactly one tier down from the one
# this mechanism closes.
SNAPSHOTTED = (
    "docs/requirements/stakeholder-needs.toml",
    "docs/requirements/system-requirements.toml",
    "docs/requirements/low-level-requirements.toml",
    "docs/test/test-cases.toml",
    "docs/requirements/interfaces.toml",
    "docs/requirements/external.toml",
    "docs/requirements/components.toml",
)

# The needs registry reads through its own carrier pair (`.toml`/`.md`) and has
# no id COLUMN — needs are dicts keyed `id`. Named separately so the row-keyed
# loop below never has to special-case a path.
NEEDS_REL = SNAPSHOTTED[0]

# `(registry path, id column)` for every ROW-KEYED tier. Eight tiers over five
# files: `external.toml` carries entities, boundary crossings and relationships
# in one file because they are one statement, and each is its own tier with its
# own id column (`spine_carrier.OFFSPINE_TABLE`).
SNAPSHOT_TIERS = (
    ("docs/requirements/system-requirements.toml", "SR-ID"),
    ("docs/requirements/low-level-requirements.toml", "LLR-ID"),
    ("docs/test/test-cases.toml", "TC-ID"),
    ("docs/requirements/interfaces.toml", "IF-ID"),
    ("docs/requirements/components.toml", "CMP-ID"),
    ("docs/requirements/external.toml", "EXT-ID"),
    ("docs/requirements/external.toml", "B-ID"),
    ("docs/requirements/external.toml", "REL-ID"),
)

# The Status value that CLAIMS approval-or-above. ONE MEMBER since D-9 step 5
# (it held `verified` and `planned` before the fold). Lowercase, matching every
# other Status comparison in the kit (the one casing rule, process.md §4). Kept
# as a set rather than an `is_approved` call because this module must not import
# `trace` (`trace` imports IT), and a set is the honest way to say "the values
# that claim" in a module that owns no predicate copy.
_APPROVAL_CLAIMED = frozenset({"approved"})

# The OFF-SPINE tiers claim on the SAME CELL as the spine since 2026-08-17 —
# `interfaces.toml`, `external.toml` and `components.toml` spell it `status`,
# where they used to spell it `approval` and `state`. The three-cell read this
# replaced was found by adversarial round 2 (2026-08-15): reading only `Status`
# meant those four snapshotted tiers could never claim approval and so were never
# drift-compared, defeating the reason `SNAPSHOTTED` copies them at all.
#
# THE SETS STAY SEPARATE THOUGH THE CELL IS ONE, because they answer for
# different tiers and are not the same set: only CMP reaches `founded`. Unioning
# them into a hand-written literal would re-introduce exactly the rival answer
# the derivation below exists to prevent.
#
# DERIVED FROM `derive_gate`'s ONE RULED LADDER TABLE rather than restated as a
# literal set here, and that is the whole point of deriving it: derive_gate.py's
# `BIF_MATURITY`/`CMP_MATURITY` are where each vocabulary's ladder semantics are
# "stated here and nowhere else", so a second hand-written set would be a rival
# answer to "is this row settled" that agrees until someone edits one of them.
# `Approved` and `Founded` both claim — `Founded` is `Approved` plus a
# demonstration, and this predicate asks about the TEXT being blessed.
_CLAIMED_MATURITY = (derive_gate.APPROVED, derive_gate.FOUNDED)
_APPROVAL_CELL_CLAIMED = frozenset(
    k for k, v in derive_gate.BIF_MATURITY.items() if v in _CLAIMED_MATURITY
)
_STATE_CELL_CLAIMED = frozenset(
    k for k, v in derive_gate.CMP_MATURITY.items() if v in _CLAIMED_MATURITY
)


def snapshot_root(root):
    """The snapshot's directory as a path. Does not create it and does not
    check that it exists — `load_all` and `copy_live` each have their own,
    different, answer to absence."""
    return Path(root) / SNAPSHOT_DIR


def exists(root):
    """True when this repo has a snapshot at all — the vacuous-by-absence test.

    The MECHANICAL writer (`intake._apply_flips`) guards on this rather than
    letting `copy_live` refuse: before the first signing there is no directory,
    and a mechanical flip that HARD-FAILED for want of a snapshot would break
    the adjudication path in every repo that has not signed yet, including a
    fresh adopter's. `copy_live`'s refusal is for the HUMAN path, where "you
    meant `--seed`" is the useful answer."""
    return snapshot_root(root).is_dir()


def stamp(root):
    """`(short rev, date)` of the commit that last wrote the snapshot, or
    `("", "")` when there is none, git cannot answer, or this is not a checkout.

    ADVISORY, AND FROM GIT RATHER THAN FROM A FILE — deliberately. The stamp is
    a courtesy for a human reading a brief ("the baseline you are diffing
    against is from this date"), and it is derived, so it can never be the
    ledger the README's first line promises it is not. Every arm degrades to
    `("", "")` rather than raising: a missing stamp costs a reader one line of
    context, and nothing computes anything from it."""
    if not exists(root):
        return "", ""
    try:
        proc = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "log",
                "-1",
                "--format=%h %cs",
                "--",
                SNAPSHOT_DIR,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, ValueError):
        return "", ""
    if proc.returncode != 0:
        return "", ""
    parts = proc.stdout.strip().split()
    return (parts[0], parts[1]) if len(parts) >= 2 else ("", "")


def _claims_approval(row):
    """True when this row claims approval or above, on the ONE cell every tier
    now uses: `Status`, spine and off-spine alike.

    IT READ THREE CELLS UNTIL 2026-08-17 — `Status`, `Approval`, `State` — not
    as a design but because three registries spelled one axis three ways, and
    the cost was concrete: a predicate that read `Status` alone answered False
    for every off-spine row, so the copies `SNAPSHOTTED` takes precisely because
    those cells move only by human hand were never compared to anything. The
    registry status unification collapsed the spellings, so the OR over three
    cells collapses with them.

    Still an OR over the two VOCABULARY sets rather than a dispatch on tier:
    they differ (only CMP reaches `founded`), and a tier table here would be a
    second place to keep that mapping right.

    THE SPINE HALF COLLAPSED AT D-9 STEP 5, as this docstring said it would: the
    ladder has ONE word for the claim (`Approved`) and the two pre-rename values
    that split it (`Verified`, `Planned`) folded into it under OI-30 D1. The two
    off-spine arms were never transitional and are unchanged, except that
    `BIF_MATURITY`'s below-approval key is spelled `drafted` since 5b — which
    this reads through `derive_gate` rather than restating, so the re-spelling
    needed no edit here at all.

    **SN IS ABSENT BY DECISION, NOT BY OMISSION** (design §B7). The reason
    CHANGED on 2026-08-17 and the distinction now matters: needs used to carry no
    maturity key at all, so there was literally no cell to read. They now carry
    `status`, in the same words as the spine (the registry status unification).
    The omission is therefore a LIVE CHOICE rather than a vacuum — SN drift is
    still not status-gated, and wiring it is deliberately parked as its own pass
    (that plan's §7: a `status` nobody checks is the same defect with a better
    name, and sizing the wiring is separate work). What holds the omission in
    place mechanically is `SNAPSHOT_TIERS`, which does not list SN, so no SN row
    reaches this predicate at all. The tier is still COPIED —
    `stakeholder-needs.toml` is in `SNAPSHOTTED`, so the record of what was
    blessed is complete."""
    return (
        (row.get("Status") or "").strip().lower() in _APPROVAL_CLAIMED
        or (row.get("Status") or "").strip().lower() in _APPROVAL_CELL_CLAIMED
        or (row.get("Status") or "").strip().lower() in _STATE_CELL_CLAIMED
    )


def load_all(root):
    """Every snapshotted registry, parsed off the snapshot tree.

    `{(stem, id_col): {row id: row}}` for the row-keyed tiers, plus
    `{(stem, "SN-ID"): {need id: need}}` for the needs tier — keyed on the
    carrier-STRIPPED path so a snapshot taken under one carrier and read under
    another still joins.

    **None when the snapshot directory does not exist at all**, which is the
    only vacuous state and is the true pre-approval one. Callers test for None
    and skip; they must NOT treat it as an empty dict, because an empty dict
    says "the snapshot recorded no rows" and that reads as "everything drifted"
    or "nothing is anchored" depending on which way the caller leans.

    **Raises on a file that exists and does not parse.** `spine_carrier.load`
    already refuses rather than returning `[]`, and that refusal is the right
    one here for the reason its own docstring gives one level up: unlike git
    history, a snapshot file is on disk and a person can fix it. The
    advisory-print-and-fall-back degrade that a GIT-HISTORY reader is right to
    use (`check_trajectory._spine_rows_at`, reading a revision nobody can now
    edit) is wrong here."""
    base = snapshot_root(root)
    if not base.is_dir():
        return None
    out = {}
    for rel, id_col in SNAPSHOT_TIERS:
        rows = spine_carrier.load(base / rel, id_col, keep_examples=False)
        out[(spine_carrier.stem(rel), id_col)] = {
            str(r.get(id_col) or "").strip(): r
            for r in rows
            if str(r.get(id_col) or "").strip()
        }
    needs = spine_carrier.load_needs(base / NEEDS_REL)
    out[(spine_carrier.stem(NEEDS_REL), "SN-ID")] = {
        n["id"]: n for n in needs if n.get("id") and not str(n["id"]).endswith("-000")
    }
    return out


def rows_for(snapshot, rel, id_col):
    """One tier's snapshot rows, or `{}` when there is no snapshot at all.

    The ONE place the None-means-absent sentinel is collapsed, so a caller that
    genuinely wants "compare against nothing" writes it once here instead of
    each caller inventing its own `or {}` — which is how the absent/empty
    distinction gets lost."""
    if snapshot is None:
        return {}
    return snapshot.get((spine_carrier.stem(rel), id_col), {})


def copy_live(root, *, seed=False):
    """Mirror every SNAPSHOTTED registry into `docs/archive/last_approved/`;
    the sorted list of repo-relative paths written.

    Byte-for-byte (`shutil.copyfile`), the LIVE carrier only — and any
    OTHER-carrier file for the same stem is DELETED in the same act, or
    `spine_carrier.resolve` raises "exists under BOTH carriers" on the very next
    read of the snapshot. A registry with no live carrier at all is skipped and
    its stale snapshot copies are removed, so the snapshot never claims a
    registry the repo has deleted.

    **REFUSES to CREATE the directory unless `seed=True`.** That refusal is the
    bootstrap guard: the FIRST snapshot blesses whatever text it copies, so it
    must ride the owner's own reviewed signing commit and nothing else.
    `--seed` is reachable only from `intake.py snapshot --seed`, and
    `tests/test_baseline_snapshot.py` pins that no loop module, hook or
    `check.py` contains the flag.

    **NOTHING SHOULD EVER WIRE THIS INTO A FRESHNESS STEP.** Exactly two callers
    are sanctioned: `intake._apply_flips` (the mechanical path, called AFTER the
    status write so the copy captures the flip — which is what makes the
    unanchored rule decidable) and `intake.py snapshot` (the human path). Not
    `agent_loop`, not `dispatch`, not the hooks, not `check.py`. A step that
    REGENERATED the snapshot would defeat the whole mechanism: the snapshot is
    deliberately behind live whenever an amendment is pending, and that lag IS
    the signal."""
    base = snapshot_root(root)
    if not base.is_dir():
        if not seed:
            raise SystemExit(
                "baseline_snapshot: REFUSED — {} does not exist, and creating it "
                "would bless whatever text happens to be in the tree right now. "
                "The first snapshot rides the owner's signing commit: run "
                "`intake.py snapshot --seed` there, after every pending row has "
                "been ruled.".format(base)
            )
        base.mkdir(parents=True, exist_ok=True)
    written = []
    for rel in SNAPSHOTTED:
        suffixes = (
            spine_carrier.NEED_CARRIERS if rel == NEEDS_REL else spine_carrier.CARRIERS
        )
        live = spine_carrier.resolve(Path(root) / rel, suffixes)
        dest_dir = base / Path(rel).parent
        # Every carrier path for this stem, so the STALE one is removed whether
        # or not a live file is being written over it. Done before the copy, so
        # a carrier change lands as delete-then-write rather than leaving both.
        for cand in spine_carrier.carriers(rel, suffixes):
            stale = base / cand
            if stale.is_file() and (live is None or stale.name != live.name):
                stale.unlink()
        if live is None:
            continue
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / live.name
        shutil.copyfile(live, dest)
        written.append(dest.relative_to(Path(root)).as_posix())
    return sorted(written)


def is_drifted(rel, id_col, live_row, snapshot_rows):
    """True when this row claims approval-or-above AND its RATIFIED cells differ
    from its copy in the snapshot.

    A row BELOW approval is never drifted — it has made no claim to fall from,
    and a `Drafted` row differing from its snapshot copy is just work in progress.
    A claiming row ABSENT from the snapshot is not drifted either; it is
    UNANCHORED, a harder finding that `unanchored_findings` owns, and conflating
    the two would report "re-attest owed" for a row that was never approved at
    all.

    The comparison basis is `check_trajectory.split_changed_cells`, which
    already excludes the id (a join key, not content) and `Status` (the marker,
    not the amendment — folding it in would make every flip look like an
    amendment and every amendment invisible behind its own flip), and which
    already splits the remainder into the §A5.1 ratified/traced halves. Only the
    RATIFIED half arms drift: a re-pointed `SN-Refs`/`Verifies`/`SR-Refs` routes
    to adjudication and never arms a re-attest window (the WI-388 ruling,
    unchanged)."""
    if not _claims_approval(live_row):
        return False
    rid = str(live_row.get(id_col) or "").strip()
    before = snapshot_rows.get(rid)
    if before is None:
        return False  # unanchored, not drifted — a different finding entirely
    changed = check_trajectory.split_changed_cells(rel, id_col, before, live_row)
    return bool(changed["ratified"])


def drifted_cells(rel, id_col, live_row, snapshot_rows):
    """`{cell: (before, after)}` for the ratified cells `is_drifted` fired on,
    `{}` otherwise — the same call, kept beside its predicate so a renderer
    never re-derives the comparison with a second set of exclusions."""
    if not is_drifted(rel, id_col, live_row, snapshot_rows):
        return {}
    rid = str(live_row.get(id_col) or "").strip()
    return check_trajectory.split_changed_cells(
        rel, id_col, snapshot_rows[rid], live_row
    )["ratified"]


def unanchored_findings(root, snapshot=None):
    """The successor to repo-lock D-9's "approved-with-no-anchor is an ERROR",
    as ADVISORY STRINGS.

    A row whose live maturity claims approval-or-above is UNANCHORED when the
    snapshot does not contain its id, or contains it at a maturity that makes no
    such claim. The second half is the one that matters and it is only decidable
    because the copy is a WHOLE FILE: a live row reading approved whose snapshot
    copy reads `Drafted` is an approval that never rode a copy. Row extraction
    would have deleted the very evidence this reads.

    VACUOUS UNTIL THE SNAPSHOT HOLDS A REGISTRY. Once it holds one, a registry
    MISSING from beside it is itself reported here — a half-copied record is a
    record with a hole, which is the state worth being loud about.

    The vacuum is "no registry" rather than "no directory", and the distinction
    is not academic: `bootstrap.py` SCAFFOLDS `docs/archive/last_approved/` with
    its README and nothing else, deliberately ("an empty snapshot is the HONEST
    state for a repo that has approved nothing yet"), so a directory test would
    report all eight tiers missing in EVERY fresh adopter repo on day one — the
    reds-everything failure the arming note below exists to avoid, shipped
    downstream. Caught when this producer was first wired to `trace.py`
    (adversarial round 2, 2026-08-15): until then nothing called this, so
    nothing could notice. The deletion half is not lost with it — the mirror
    invariant refuses a registry deleted from a standing record in the commit
    that does it (`check_trajectory.staged_snapshot_findings`).

    **NOT ARMED.** These are advisory strings today and join no failure set.
    They are promoted to the integrity class — the always-on `--strict-integrity`
    floor plus the pre-commit hook — at migration step 7, and deliberately not
    before: run against a pre-seed snapshot (there is none) or a pre-rename one
    (it speaks the retired vocabulary), this rule reds every row in the repo,
    and a check that reds everything is a check that gets switched off."""
    if snapshot is None:
        snapshot = load_all(root)
    if snapshot is None:
        return []
    base = snapshot_root(root)
    if not any(spine_carrier.resolve(base / rel) for rel in SNAPSHOTTED):
        return []  # scaffolded-but-unsigned: the pre-signing state, honestly
    out = []
    for rel, id_col in SNAPSHOT_TIERS:
        if spine_carrier.resolve(base / rel) is None:
            out.append(
                "{} is missing from the {} snapshot — the snapshot exists, so a "
                "registry absent from it is a gap in the record of what was "
                "approved, not a repo that has approved nothing".format(
                    rel, SNAPSHOT_DIR
                )
            )
            continue
        before = rows_for(snapshot, rel, id_col)
        for row in spine_carrier.load(Path(root) / rel, id_col, keep_examples=False):
            rid = str(row.get(id_col) or "").strip()
            if not rid or not _claims_approval(row):
                continue
            snap = before.get(rid)
            if snap is None:
                out.append(
                    "{} reads Status={} but is ABSENT from the {} snapshot — "
                    "an approval that never rode a copy (adding a row and "
                    "approving it must be one act)".format(
                        rid, (row.get("Status") or "").strip(), SNAPSHOT_DIR
                    )
                )
            elif not _claims_approval(snap):
                out.append(
                    "{} reads Status={} but its {} copy reads Status={} — the "
                    "approval was written without copying the text it blessed".format(
                        rid,
                        (row.get("Status") or "").strip(),
                        SNAPSHOT_DIR,
                        (snap.get("Status") or "").strip() or "(unset)",
                    )
                )
    return sorted(out)
