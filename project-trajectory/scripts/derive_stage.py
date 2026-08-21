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
import tempfile
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


# --- THE PHASE RULE (ruled plan §4 + owner answer §6.1/§6.2) ------------------
# The spine registries this rule reads on the BEFORE side, as
# `(declared-path, id-column, spine key)`. Declared here rather than re-derived
# from `kitstage.DECLARED_INPUTS` because that list is the FINGERPRINT's input
# set — it deliberately includes the frame registries and the dials, which this
# rule holds CONSTANT (see `_before_spine`). Two lists with two jobs beat one
# list quietly serving both.
_SPINE_REGISTRIES = (
    ("docs/requirements/system-requirements", "SR-ID", "srs"),
    ("docs/requirements/low-level-requirements", "LLR-ID", "llrs"),
    ("docs/test/test-cases", "TC-ID", "tcs"),
)

# THE EXEMPTION, and it is exactly one permutation (owner answer §6.2): a
# decrease landing precisely on DevStg-LLReqs -> DevStg-Arch is the PERMITTED
# DECOMPOSITION CYCLE — architecture rework surfaced by breaking a requirement
# down is within-phase churn, and any deeply decomposed problem would otherwise
# run the phase counter up. The owner declined a wider Arch-tier exemption, so
# this is a pair, not a predicate over the Arch rung: a two-rung drop that
# happens to END at Arch is NOT exempt, and neither is Arch -> anything.
_EXEMPT_DECREASE = (kitladder.STAGE_LLREQS, kitladder.STAGE_ARCH)


def _spine_at(root, rev):
    """`load_spine` over the DECLARED INPUTS as they stood at `rev`, or None when
    git cannot answer — the kit's silent-no-op degrade, not an error.

    THE INPUTS ARE MATERIALIZED INTO A TEMP TREE AND THE LIVE LOADER IS RUN OVER
    IT, rather than parsing each `git show` into rows here. Three things come
    free that a re-implementation would have to get right and could drift on:
    carrier resolution (`.toml` before `.csv`, and `.md` for needs), the `-000`
    example filter, and — the one that actually bites — the `have_bifs`/
    `have_cmps` applies-when, where an ABSENT registry and an EMPTY one mean
    opposite things at the two inserted rungs. Materializing only the files that
    existed at `rev` preserves absence as a value.

    THE WHOLE FRAME IS READ AT `rev`, NOT HELD AT THE LIVE TREE. Holding it
    constant was tried first and is wrong: the ruled exemption is
    `DevStg-LLReqs -> DevStg-Arch`, and the Arch rung is derived from the
    COMPONENT registry, so a frame pinned to the live tree makes the owner's one
    permitted decrease unreachable — the rule would be unable to see the very
    transition it is required to forgive."""
    if derive_gate._git(root, ["rev-parse", "--verify", "--quiet", rev]) is None:
        return None  # no git, or no such revision: nothing to compare against
    with tempfile.TemporaryDirectory() as tmp:
        found = False
        for declared, suffixes in kitstage.DECLARED_INPUTS:
            for suffix in suffixes:
                text = derive_gate._git(
                    root, ["show", "{}:{}{}".format(rev, declared, suffix)]
                )
                if text is None:
                    continue
                dest = Path(tmp) / (declared + suffix)
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(text, encoding="utf-8", newline="\n")
                found = True
                break
        if not found:
            return None
        return derive_gate.load_spine(Path(tmp) / "docs")


def _by_id(spine):
    """`{spine-key: {id: row}}` — the before-side lookup `_changed_rows` joins on."""
    return {
        key: {r[id_col]: r for r in spine.get(key, []) if r.get(id_col)}
        for _declared, id_col, key in _SPINE_REGISTRIES
    }


def _effective(spine):
    """The headline value for a spine dict — the settled, per-phase, floored fold,
    i.e. exactly what `derive()` puts in the `stage` field."""
    _live, settled_per_phase = _stage_map(spine, settled=True)
    return kitstage.effective_stage(settled_per_phase)[0]


def _changed_rows(live, before_rows):
    """Every spine row this edit ADDED or whose `Status` it MOVED, as
    `[(id, row, before-status-or-None)]`.

    THE TRIGGER SET IS WIDER THAN THE PLAN'S WORDS, and the measurement is why.
    Plan §4 says "a newly drafted/redrafted row"; driven on a frame-free spine
    (slice 3), a newly DRAFTED row cannot decrease the effective stage AT ALL —
    slice 1 excludes drafts from the settled fold, so that half of the phrase is
    inert by construction. What actually decreases it is a redrafted child
    (Impl -> LLReqs for an LLR, Impl -> Tests for a TC) and a newly RATIFIED
    parent with no children yet (Impl -> LLReqs). Narrowing to the literal words
    would have shipped a rule that cannot fire on the two shapes that matter, so
    the trigger is "added, or Status moved" — which CONTAINS the plan's set."""
    out = []
    for _declared, id_col, key in _SPINE_REGISTRIES:
        prior = before_rows.get(key, {})
        for row in live.get(key, []):
            rid = row.get(id_col)
            if not rid:
                continue
            was = prior.get(rid)
            before_status = None if was is None else (was.get("Status") or "").strip()
            now_status = (row.get("Status") or "").strip()
            if was is None or before_status.lower() != now_status.lower():
                out.append((rid, row, before_status))
    return out


def phase_rule_findings(root):
    """The authoring-time decrease rule (plan §4, owner answer §6.1).

    **A spine edit that LOWERS the effective stage must surface as a phase
    change.** When the effective stage decreased, every row this edit added or
    re-statused must carry a `Phase` tag that is NOT the phase the settled work
    was standing in — a NEW (higher) phase, or an already-open LOWER one. Both
    readings of "the scope moved" satisfy it; quietly adding regressing work to
    the phase you are standing in does not.

    WHY THIS SHAPE AND NOT A STORED COUNTER (plan §4, alternative (ii) rejected):
    phase stays a pure function of the registries. The derived `phase=` still
    increments BECAUSE the rows say so, so there is no second phase concept to
    drift against the row tags, and `docs/stage` records the derived value
    exactly as `docs/gate` did.

    WARN TIER, AND THE ARMING PATH IS THE POINT. This returns findings; `main`
    prints them and exits 0 unless `--strict`. New rules arm warn-first here
    unless a ruling says otherwise, and OI-51's ruling establishes that the rule
    EXISTS, not that it hard-fails on day one. It promotes by being wired into
    `check.py`'s `--strict` trio at a threshold — deliberately NOT done in this
    slice, because a rule whose fire has never been observed on real authoring
    should not be able to block a commit. The promotion is one call-site edit:
    the predicate and its vocabulary do not change (`trace.schema_advisories`'s
    warn-first twin idiom).

    DEGRADES SILENTLY WITHOUT GIT, like every other two-tree rule in the kit: no
    HEAD means no before-state, and a rule that cannot see the past has nothing
    to say rather than something to complain about.

    Implements: SR-139"""
    root = Path(root)
    live = derive_gate.load_spine(root / "docs")
    before = _spine_at(root, "HEAD")
    if before is None:
        return []
    before_rows = _by_id(before)

    was, now = _effective(before), _effective(live)
    if kitstage.order(now) >= kitstage.order(was):
        return []
    if (was, now) == _EXEMPT_DECREASE:
        return []

    # The phase the SETTLED work was standing in, on the BEFORE side — the value
    # a new tag has to differ from. Max over non-Drafted rows, which is `phase=`
    # itself, so the rule and the recorded field can never mean different things.
    prior_phases = [
        derive_gate.phase_num(r)
        for key in ("srs", "llrs", "tcs")
        for r in before.get(key, [])
        if not derive_gate.is_drafted(r)
    ]
    prior_phases = [p for p in prior_phases if p is not None]
    standing = max(prior_phases) if prior_phases else None

    findings = []
    for rid, row, before_status in sorted(_changed_rows(live, before_rows)):
        phase = derive_gate.phase_num(row)
        if standing is None or phase != standing:
            continue
        findings.append(
            "{} lowers the effective stage ({} -> {}) and carries no new phase: "
            "it is tagged phase {}, the phase the settled spine was already "
            "standing in. {} A stage decrease is a scope change and must surface "
            "as one — tag the row into a new phase ({}) or into an already-open "
            "lower phase.".format(
                rid,
                was,
                now,
                phase,
                (
                    "The row is new."
                    if before_status is None
                    else "Its status moved {} -> {}.".format(
                        before_status or "(blank)", (row.get("Status") or "").strip()
                    )
                ),
                standing + 1,
            )
        )
    return findings


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
    ap.add_argument(
        "--phase-rule",
        action="store_true",
        help="check the authoring-time stage-decrease rule against HEAD (warn-first)",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="with --phase-rule: exit 1 on a finding instead of warning",
    )
    args = ap.parse_args()
    root = Path(args.root)

    if args.phase_rule:
        findings = phase_rule_findings(root)
        for f in findings:
            print("{} - {}".format("FAIL" if args.strict else "WARN", f))
        if not findings:
            print("derive_stage: phase rule clean (no un-phased stage decrease).")
        return 1 if (findings and args.strict) else 0

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
