#!/usr/bin/env python3
"""Derive the EFFECTIVE STAGE from artifact states and cache it to `docs/stage`.

Stack-agnostic, standard-library only. This is the stage axis's own producer
(WI-498 slice 1, ruled plan `docs/plans/2026-08-21-stage-unification-plan.md`
§§1-3). `docs/gate` REMAINS and stays authoritative for its readers until slice 2
cuts them over; the two files are a deliberate transitional dual state, derived
from the same rows by the same predicates, and both freshness-gated.

WHAT THIS ADDS THAT `docs/gate` DID NOT HAVE.

1. **A per-phase stage.** `spine_stage` took no phase argument and `_per_phase`
   folded BARS, so "the current phase's stage" did not exist — the sharpest gap
   the deep-check found (Q2(iv)). It exists here.
2. **A draft-excluded reading.** `ex-draft=` is a bar and validating it against
   the stage ladder would type-check and return a wrong ordinal (Q2(v-d),
   refuted as a shortcut), so the counterfactual is computed here on its own axis.
   This is what stops one ordinary Drafted row from dropping a mature repo to
   what a fresh scaffold reads — C-01 on the new axis.
3. **A floor.** The bar axis floors at DevStg-Reqs and the stage axis did not, so
   the stage could reach ord 0, below every runnable rung. Under the at-or-above
   selection slice 2 lands, that is a repo where nothing runs and the run goes
   green because of it.
4. **A fingerprint of the declared inputs**, which is what lets any reader tell a
   current record from a stale one without parsing the registries.

THE DIVISION OF LABOUR. The pure half — the input list, the fingerprint, the file
format, the ordering, the floor and the fold — is `kitlib/stage.py`, because
`kitlib` may not import a sibling and the registry parse cannot go there. This
module is the half that needs the carrier: it loads the spine through
`derive_gate.load_spine`, groups the rows by phase, and calls `derive_gate`'s own
rung predicates so that the two axes can never disagree about what a Drafted row
is. When slice 3 re-discriminates the ladder it edits ONE fall-through
(`derive_gate.spine_stage`) and both files follow.
"""

import argparse
import datetime
import sys
from pathlib import Path

# Sibling: the derivation engine. This module reads its ROW PREDICATES and its
# rung fall-through rather than restating them — the two axes must never disagree
# about what a Drafted row is, and slice 3 re-discriminates the ladder in exactly
# one place because of it. Same guarded idiom the rest of the kit uses: run as a
# subprocess this script's own dir is sys.path[0], and the fallback covers an
# in-process import (a test) whose sys.path does not yet carry scripts/.
try:
    import derive_gate
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import derive_gate

try:
    from kitlib import ladder as kitladder
    from kitlib import stage as kitstage
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kitlib import ladder as kitladder
    from kitlib import stage as kitstage

STAGE_FILE = kitstage.STAGE_FILE


def _phase_label(row):
    """The phase bucket a row belongs to — the same `(default)` convention
    `derive_gate._per_phase` uses, so the two per-phase lines name the same
    buckets and a consumer can join them."""
    return (row.get("Phase") or "").strip() or "(default)"


def _phase_groups(srs, llrs, tcs):
    """`{phase-label: (srs, llrs, tcs)}` — the rows each phase's stage is derived
    from.

    ASSOCIATION IS BY REFERENCE, NOT BY THE CHILD'S OWN `Phase` CELL, matching
    `derive_gate._per_phase`. The rungs ask "does THIS SR have an LLR, and is that
    LLR settled" — so an LLR belongs to the phase of the SR it decomposes, whatever
    its own cell says, and a mislabelled child cannot hide a phase's undecomposed
    requirement. A TC that cites only its LLR (a legal shape) is resolved back to
    that LLR's SRs for the same reason: otherwise a Drafted TC in that shape lands
    in no phase at all."""
    by_phase = {}
    sr_phase = {}
    for row in srs:
        label = _phase_label(row)
        sr_phase[row["SR-ID"]] = label
        by_phase.setdefault(label, ([], [], []))[0].append(row)

    llr_srs = {}
    for row in llrs:
        cited = derive_gate.refs(row.get("SR-Refs"))
        llr_srs[row.get("LLR-ID") or ""] = cited
        for label in {sr_phase[s] for s in cited if s in sr_phase}:
            by_phase.setdefault(label, ([], [], []))[1].append(row)

    for row in tcs:
        labels = set()
        for ref in derive_gate.refs(row.get("Verifies")):
            for s in llr_srs.get(ref, [ref]):
                if s in sr_phase:
                    labels.add(sr_phase[s])
        for label in labels:
            by_phase.setdefault(label, ([], [], []))[2].append(row)
    return by_phase


def _settled_off_spine(rows, table):
    """The off-spine rows a SETTLED reading keeps: everything not at DRAFTED
    maturity.

    Only the maturity arm is filtered. A `Founded` component whose `Standing`
    records a known gap stays IN — that is a settled row honestly reporting that
    the partition does not hold, which is a real rung-3 fact, not a pending
    draft."""
    return [
        r
        for r in rows
        if not derive_gate._caps(derive_gate._maturity(r.get("Status"), table))
    ]


def _stage_map(spine, settled):
    """`(global-stage, {phase: stage})` over the live rows or the settled subset.

    A phase whose rows are ALL drafts disappears from the settled subset and is
    recorded as the `DevStg-Below` sentinel rather than dropped: the phase exists
    (its drafts say so) and has earned nothing, and those are different facts from
    "there is no such phase". `effective_stage` then ignores it, which is exactly
    how a brand-new phase is stopped from lowering the whole repo's reading."""
    srs, llrs, tcs = spine["srs"], spine["llrs"], spine["tcs"]
    sn_ids, sn_draft = spine["sn_ids"], spine["sn_draft"]
    bifs, cmps = spine["bifs"], spine["cmps"]
    live_labels = set(_phase_groups(srs, llrs, tcs))

    if settled:
        srs = [r for r in srs if not derive_gate.is_drafted(r)]
        llrs = [r for r in llrs if not derive_gate.is_drafted(r)]
        tcs = [r for r in tcs if not derive_gate.is_drafted(r)]
        sn_ids = sn_ids - sn_draft
        sn_draft = set()
        bifs = _settled_off_spine(bifs, derive_gate.BIF_MATURITY)
        cmps = _settled_off_spine(cmps, derive_gate.CMP_MATURITY)

    frame = dict(
        sn_ids=sn_ids,
        sn_draft=sn_draft,
        bifs=bifs,
        cmps=cmps,
        have_bifs=spine["have_bifs"],
        have_cmps=spine["have_cmps"],
    )
    overall = derive_gate.spine_stage(srs, llrs, tcs, **frame)
    groups = _phase_groups(srs, llrs, tcs)
    per_phase = {}
    for label in sorted(live_labels):
        group = groups.get(label)
        if not group or not group[0]:
            per_phase[label] = kitstage.BELOW
            continue
        per_phase[label] = derive_gate.spine_stage(
            group[0], group[1], group[2], cited_srs=srs, **frame
        )
    return overall, per_phase


def derive(root):
    """The stage record for the tree at `root` — the deriver the common reader
    calls on a fingerprint miss, and the value `--check` compares."""
    docs = Path(root) / "docs"
    spine = derive_gate.load_spine(docs)
    live, live_per_phase = _stage_map(spine, settled=False)
    _, settled_per_phase = _stage_map(spine, settled=True)

    effective, floored = kitstage.effective_stage(settled_per_phase)
    earned = [v for v in settled_per_phase.values() if v != kitstage.BELOW]
    settled_stage = min(earned, key=kitstage.order) if earned else kitstage.BELOW

    rows = spine["srs"] + spine["llrs"] + spine["tcs"]
    drafted = sum(1 for r in rows if derive_gate.is_drafted(r)) + len(spine["sn_draft"])
    phases = [derive_gate.phase_num(r) for r in rows if not derive_gate.is_drafted(r)]
    phases = [p for p in phases if p is not None]

    return {
        "stage": effective,
        "stage-ord": kitstage.order(effective),
        "stage-of": kitladder.STAGE_OF,
        "floored": floored,
        "settled-stage": settled_stage,
        "live-stage": live,
        "phase": max(phases) if phases else None,
        "per-phase": settled_per_phase,
        "per-phase-live": live_per_phase,
        "drafted": drafted,
    }


def read(root):
    """THE COMMON READER, wired. Every consumer that needs the current stage
    calls THIS — one line, so the deriver is named once in the kit rather than at
    each call site, and `kitlib.stage` stays free of the sibling import."""
    return kitstage.read_stage(root, derive)


def main():
    derive_gate._utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    ap.add_argument(
        "--check",
        action="store_true",
        help="recompute and compare to the cached docs/stage; exit 1 on drift",
    )
    ap.add_argument(
        "--print",
        dest="print_only",
        action="store_true",
        help="compute and print the derived record; do not write docs/stage",
    )
    args = ap.parse_args()
    root = Path(args.root)

    record = derive(root)
    record["fingerprint"] = kitstage.fingerprint(root)
    block = kitstage.field_block(record)

    if args.print_only:
        print(block)
        return 0

    path = root / STAGE_FILE
    if args.check:
        # THE FINGERPRINT IS NOT ENOUGH ON ITS OWN, and this is why `--check`
        # recomputes rather than comparing digests: a change to the DERIVATION
        # moves the recorded values while every input byte stays put. The
        # fingerprint answers "do the inputs still match", the recompute answers
        # "does the whole record still hold", and only the second is a freshness
        # guard. The same asymmetry `derive_gate --check` has always had.
        if not path.exists():
            print(
                "derive_stage: {} is absent — run `python scripts/derive_stage.py` "
                "to generate it".format(STAGE_FILE),
                file=sys.stderr,
            )
            return 1
        cached = kitstage.parse(path.read_text(encoding="utf-8", errors="replace"))
        if cached is None:
            # THE SCAFFOLD / MIGRATION FORM, and it PASSES — the same
            # smooth-transition path `derive_gate --check` gives a legacy
            # hand-set marker. A file with no stage field has never been
            # derived: it is `stage.template` as `bootstrap.py` copied it, or an
            # adopter's tree between the resync and the first regeneration.
            # There is nothing to compare it against and nothing it can be
            # stale relative to, so failing here would red every freshly
            # scaffolded repo — the shipped promise is that such a repo is
            # green. It is a NOTE, not a silent pass: the message names the one
            # command that ends the state, and `trunk_step --regen` runs it
            # unprompted at the next trunk regeneration point.
            print(
                "derive_stage: {} is not yet in derived form — run "
                "`python scripts/derive_stage.py` once to generate it.".format(
                    STAGE_FILE
                ),
                file=sys.stderr,
            )
            return 0
        cached_block = kitstage.field_block(cached)
        if cached_block == block:
            print(
                "derive_stage: {} up to date ({}).".format(STAGE_FILE, record["stage"])
            )
            return 0
        print(
            "derive_stage: {} STALE — the derived stage moved but the cache did "
            "not.\n  cached:\n{}\n  now:\n{}\n"
            "  run `python scripts/derive_stage.py` and commit the result.".format(
                STAGE_FILE, cached_block, block
            ),
            file=sys.stderr,
        )
        return 1

    as_of = derive_gate._git(root, ["rev-parse", "--short", "HEAD"]) or "no-git"
    date = (
        derive_gate._git(root, ["log", "-1", "--format=%cs"])
        or datetime.date.today().isoformat()
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        kitstage.render(record, as_of, date), encoding="utf-8", newline="\n"
    )
    print("derive_stage: wrote {} -> {}.".format(STAGE_FILE, record["stage"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
