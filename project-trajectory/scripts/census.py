"""census.py — the registry-gap census: what the registries themselves say is missing.

A READ MODEL OVER THE REGISTRIES, and nothing else. Every function here answers
one question — "which gaps do the spine registries name right now?" — from
`trace.py`'s single orphan/status engine plus the work registry. Nothing here
claims a lane, mints a row, moves a spec or writes a byte; the callers do that,
and they are deliberately three different kinds of caller:

    dispatch.py         the empty-frontier ladder's rung 1 — derive the census,
                        hand it to the mint (docs/concurrency-v2.md §A4/§A5.2)
    intake.py           `mint_gap_rows` and the `intake.py census` hand path,
                        which turn census lines into concrete gap-closure and
                        adjudication rows
    adjudicate_brief.py the disposition brief, which re-runs the red-TC census
                        LIVE rather than trusting a remembered one

WHY THIS IS A MODULE AND NOT PART OF THE DISPATCHER (WI-483, slice 2). Until
this module the census lived in `dispatch.py`, the tick loop and admission
authority — so every reader of a census line imported the SCHEDULING COMPOSER
to reach it. Two of the three readers above are below the dispatcher, not above
it, and one of them (`intake`) imported it back: that deferred
`intake -> dispatch` import was a back edge of the five-module strongly
connected component the 2026-08-19 repository review recorded (H-02). The
census depends on nothing in the lifecycle band — it reads registries — so it
belongs below all three readers, which is the same cut `kitlib/station.py`
already applied to the lane-close outcome vocabulary.

NOT `kitlib`, and the reason is a hard rule rather than taste: every module of
that package must stay import-clean of the rest of `scripts/`
(`tests/test_bootstrap.py::test_bootstrap_imports_only_the_common_package`),
because `bootstrap.py` imports it and would otherwise drag the whole graph into
the scaffolder. This module's whole job is to REUSE `trace.analyze` rather than
re-derive it, so it imports a sibling by construction and is a plain sibling
itself.

THE SEAM CARRIES STRINGS, and the grammar for the one structured line class has
exactly one home — here, both halves of it. `_red_tc_line` formats and
`parse_red_tc` reads; they sit adjacent on purpose, because a producer and a
parser in separate modules is a contract nothing checks. Everything else on the
seam is free prose a human reads, and the mint keys off it only through
`parse_red_tc`.

Implements: SR-148, LLR-159, LLR-188
"""

from __future__ import annotations

import re
from pathlib import Path

import agent_common as ac
import schedule


def gap_census(root):
    """THE WI-388 HANDOFF SEAM — ladder rung 1 (§A4 amendment, ruled
    2026-08-01). The mechanical registry-gap census the dispatcher derives
    when the frontier is empty: unverified in-scope SRs, orphan rows, draft
    SNs — exactly what trace.py already names, re-used rather than re-derived
    (`trace.analyze` is the one orphan/status engine). `intake.mint_gap_rows`
    consumes this list at `dispatch._station_exit` rung 1 to mint concrete
    gap-closure rows with derived descriptions — no model anywhere in the path,
    and the mint dedupes so one gap can never mint twice. Returns finding
    strings; [] when the registries are complete (or absent — a scaffold with
    no spine yet has no gaps to name)."""
    import trace as tr

    reg = tr.load_registries(Path(root) / "docs")
    # The engine's config as its own record (WI-483): this used to forge an
    # `argparse.Namespace` for four values, which is what a non-CLI caller has to
    # do when a CLI namespace IS the config type.
    findings = tr.analyze(reg, tr.AnalysisFlags(require_verified=True))
    census = list(findings.orphans)
    census += list(findings.status_findings)
    census += [
        "SN {} is a draft need (unapproved)".format(s) for s in sorted(reg.sn_draft)
    ]
    census += red_tc_census(root, reg)
    return census


# LLR-159's marker. The census is a list of STRINGS by contract (the seam
# `intake.mint_gap_rows` consumes), so a distinct class announces itself with a
# distinct prefix rather than by growing the seam a second shape. `intake.
# _census_drafts` routes on exactly this token; nothing else parses the line.
RED_TC_PREFIX = "red TC "

# The three statuses this rung does NOT call red, each because another rung
# owns it. Stated as exemptions because Status was an open vocabulary when this
# was written — see `red_tc_census`; D-9 step 1 closed it, and the exemption
# form is kept because it still fails toward NAMING a gap.
#
# THE `planned` QUESTION DISSOLVED AT D-9 STEP 5, exactly as the step-2 entry
# said it might. Step 2 declined to add `planned` here on arithmetic rather than
# taste: `Status` was closed to four values and is a REQUIRED TC field, so a
# fourth member would have made this set the WHOLE vocabulary and left the
# census firing only on a row with no Status at all — a state the schema tier
# refuses and `adjudicate_brief.TC_CELLS` will not brief, so census -> mint ->
# brief would have been unreachable end to end (a deleted feature, LLR-159, not
# a narrowed rung). OI-30 D1 then folded `Planned` into `Approved`, and the
# arithmetic now cuts the OTHER way: the enum narrowed to exactly these three
# states, so the exemption covers the WHOLE vocabulary and the census is
# structurally dead in any conformant repo (tests/test_adjudicate_brief.py
# records the same fact and moved its fixtures out-of-enum to stay meaningful).
# Deliberately kept rather than deleted: whether the rung RETIRES or re-arms on
# a narrower exempt set is the owner's call, recorded as a judgement item at
# the 2026-08-15 sitting sweep.
#
# D-9 STEPS 7/8 SWAPPED ONE MEMBER FOR ANOTHER AND THE ARITHMETIC IS UNMOVED:
# `modified` left with the value (it can no longer appear in a conformant repo,
# and a set that exempts a retired word is a live reader of one), `founded`
# joined — a TC at the top rung is green a fortiori, so exempting it is not a
# widening. The set still covers the WHOLE closed vocabulary, so the census
# remains structurally dead in a conformant repo, which is precisely the fact
# the owner's judgement item is about. A DOWNSTREAM repo still carrying
# `Modified` TCs now sees them as red here — that repo is already failing the
# always-on integrity floor on the same cells, so the rung is naming a gap the
# floor has already named rather than inventing one.
_TC_NOT_RED = frozenset({"approved", "drafted", "founded"})


def red_tc_census(root, reg=None):
    """LLR-159: TEST CASES LEFT RED UNDER A CLAIMED IMPLEMENTATION.

    A TC that is not `Approved` is ordinary unfinished work — unless something
    already claims to have BUILT what it verifies, and that is the state this
    names: a TC outside the three exempt statuses, all of whose `Verifies`
    targets are cited by at least one WI recorded `done`. The pair is a
    contradiction the registries state plainly and nothing was reading: the work
    is closed and the evidence for it is red.

    Status is CLOSED (D-9 step 1) but the rule stays stated as exemptions rather
    than as a list of red words — anything else is red, which fails toward
    naming a gap rather than toward missing one, and keeps working for a
    downstream repo mid-migration:

      Approved  green, by definition.
      Drafted   pre-approval; "not yet green" is its CORRECT state.
      Founded   Approved plus a demonstration — green a fortiori (D-9 step 8).
                It replaced `Modified`, which named the post-approval amendment
                state the §A5.1 adjudication owns; that state no longer has a
                word, and the amendment path still owns it via snapshot drift.

    A TC whose targets no closed row cites is also exempt: that is work not
    started, which the orphan/status rungs already cover, and a second row for
    it would double-count. Same for `partial`/`cancelled` closers — see
    `_implemented_ids`.

    Implements: SR-148, LLR-159
    """

    import trace as tr

    root = Path(root)
    if reg is None:
        reg = tr.load_registries(root / "docs")
    claimed = _implemented_ids(root)
    if not claimed:
        return []
    census = []
    for row in reg.tcs:
        tc_id = (row.get("TC-ID") or "").strip()
        status = (row.get("Status") or "").strip().lower()
        if not tc_id or tc_id.endswith("-000") or status in _TC_NOT_RED:
            continue
        targets = [t for t in ac._refs(row.get("Verifies")) if not t.endswith("-000")]
        if not targets or not all(t in claimed for t in targets):
            continue
        census.append(_red_tc_line(tc_id, status, targets))
    return census


def _red_tc_line(tc_id, status, targets):
    """Format ONE red-TC census line. Paired with `parse_red_tc` below, and the
    two must stay adjacent: the seam carries strings, so this grammar gets
    exactly one home — which is now this module, so the producer and the reader
    are no longer a contract between two modules at all."""
    return (
        "{}{} [{}] is {} under a claimed implementation (a closed row "
        "claims the work; its evidence is not green)".format(
            RED_TC_PREFIX, tc_id, ";".join(targets), status or "unset"
        )
    )


_RED_TC_RE = re.compile(re.escape(RED_TC_PREFIX) + r"(\S+) \[([^\]]*)\]")


def parse_red_tc(line):
    """`(tc_id, [target, ...])` for a red-TC census line, or None for any other
    line. The ONE reader of `_red_tc_line`'s grammar — `intake._census_drafts`
    routes through this rather than re-splitting the prose, because prose that
    carries control flow has to be a parsed field with a refusal, not a
    substring search that silently matches nothing (the `NEEDS-HUMAN` lesson,
    LLR-161)."""
    matched = _RED_TC_RE.match(line or "")
    if not matched:
        return None
    return matched.group(1), [t for t in matched.group(2).split(";") if t]


def _implemented_ids(root):
    """The set of SR/LLR ids some `done` work item cites — "somebody claims to
    have built this".

    Read off `SR-Refs` (the WI registry's only requirement link) plus the LLRs
    those SRs own, because a TC usually verifies the LLR while the work item
    cites the SR. A row in any non-`done` status contributes nothing: `partial`
    and `cancelled` are precisely the outcomes that say the work is NOT
    delivered, so a red TC under one of those is expected, not a contradiction —
    and its close already earned a disposition row of its own.

    The work registry is read through `agent_common.load_registry_rows`, the one
    home that derives `docs/work/` from the path its callers already declare, so
    this module needs no `docs/work` literal of its own — and, more to the
    point, no import of the minting module that used to supply the constant."""
    import trace as tr

    wis = schedule.load_wis(ac.load_registry_rows(root))
    srs = {
        ref
        for w in wis
        if (w.get("status") or "").strip().lower() == "done"
        for ref in (w.get("srs") or ())
    }
    if not srs:
        return set()
    reg = tr.load_registries(Path(root) / "docs")
    claimed = set(srs)
    for row in reg.llrs:
        owner = ac._refs(row.get("SR-Refs"))
        if owner and all(o in srs for o in owner):
            claimed.add((row.get("LLR-ID") or "").strip())
    claimed.discard("")
    return claimed
