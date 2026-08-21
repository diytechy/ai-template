#!/usr/bin/env python3
"""Derive the harness BAR from artifact states — the hybrid, cached selector.

RETIRED-VOCABULARY DECLARATION SITE (check_vocab: allow-file) — this module is
the ONE home of the `G0`/`G1`/`G2`/`G3` -> `DevStg-*` translation table, so the
retired tags appear here by design and the vocabulary enforcer exempts the file.
Nowhere else in the kit may name them outside a read-side alias lookup.

Stack-agnostic, standard-library only. This replaces the hand-set `docs/gate`
marker with one *computed* from the spine's own maturity states
(docs/archive/specs/derived-gate-model.2026-07-20.md; the ruled stage/bar
semantics are process.md §4 "The stage ladder — state vs. certified boundary").
**A repo is IN a stage; it CLEARS a bar.** The value written to `docs/gate` is
therefore not a claim that the repo "is at" that bar: it is the bar the repo
must next clear, taken as the **min** over every in-scope SN/SR/LLR/TC, so the
least-mature row selects the strictness the harness holds everyone to. SSOT
applied to that selector — you no longer bump a line, you ratify artifacts (in a
reviewed commit) and the derived value follows.

(The FILE keeps its name. `docs/gate` and `derive_gate.py` are paths adopters'
hooks and CI invoke literally, and OI-21 retired the G-TAGS, not the word "gate"
where it means a check that can fail. Renaming the file would break every adopter
for a cosmetic gain; renaming the vocabulary inside it is the whole point.)

The model is **hybrid**: the computed value is *cached* to `docs/gate` (now a
generated file) with a compute date, so the bar is known on checkout with no
recompute; `--check` recomputes and guards the cache against rot, the same
freshness discipline the kit already runs for the arch-map / OKF / dashboard.
`check.py`'s `resolve_gate()` still reads the first non-comment line of
`docs/gate` — the value is simply derived now, not declared.

Per-artifact bar (docs/archive/specs/derived-gate-model.2026-07-20.md §3), on the
internal ladder DevStg-Below < DevStg-Reqs < DevStg-Tests < DevStg-Impl.
**`DevStg-Below` is NOT a bar** — nothing clears it. It survives only as the
arithmetic sentinel for *below the lowest runnable bar*, because the min-fold
needs a value under `DevStg-Reqs`. Say "stage Needs / Boundary" of the repo; say
`DevStg-Below` only of this internal fold:
  - **SN** — Drafted => `DevStg-Below`; ratified AND cited by >=1 SR `SN-Refs` => it
    has no obligation past `DevStg-Reqs`, so it never caps the repo (contributes
    `DevStg-Impl` to the min); ratified but cited by NO SR (WI-401) =>
    `DevStg-Below` — a ratified-but-unanswered need means `DevStg-Reqs` is not
    earned. The `uncovered=N` basis count surfaces the cause beside
    `drafted=N` (a Drafted SN is exempt from the coverage rung — it
    already reads `DevStg-Below` via the draft rung, one fact one rung; the
    itemized "SN has no SR" listing stays trace.py's orphan finding at
    `DevStg-Tests` strictness, this rung being the bar-input half of that split).
  - **SR** — Drafted (Status) => `DevStg-Below`; ratified but not decomposed =>
    `DevStg-Reqs`; decomposed (has its required LLR — unless the Verification is
    LLR-exempt Analysis/Inspection/Attest — AND a TC) => `DevStg-Tests`, WHICH IS
    THE CEILING (OI-30 D2: `DevStg-Impl` is unreachable-by-cell until the
    harness driver computes it from test evidence — see `sr_bar`). A `Founded`
    SR (D-9's top rung, armed for the spine at migration step 8) needs no rule of
    its own either: it is settled, so it reads exactly as `Approved` does here —
    the demonstration `Founded` records is about the row's CHILDREN existing, not
    about the harness, and only the harness moves `DevStg-Tests` -> `DevStg-Impl`.
  - **LLR / TC** — Drafted => `DevStg-Below` (the new-phase signal). Once present,
    its Status does not independently gate: the SR's `Approved` status drives
    `DevStg-Tests` -> `DevStg-Impl` (matching trace.py's --require-verified,
    which checks SRs, not LLR/TC status), so a present LLR/TC never caps below
    `DevStg-Impl`.

Aggregation: the derived value = **min over all in-scope artifacts** (a phase's
value is the min over that phase's artifacts; the repo's is the min over phases,
which is the same set — also reported per-phase). A repo with **no** real SRs yet
(a fresh scaffold) derives **`DevStg-Reqs`** (the requirements-drafting start),
never a vacuous `DevStg-Impl`. A draft artifact reads `DevStg-Below`, so
introducing draft/reopened content **drops** the derived value — the signal that a
new phase is due (the phase-anchor detector lives in check_trajectory). The cached
runnable value is floored at `DevStg-Reqs` (check.py's bar vocabulary is the three
runnable bars); the raw computed level, including a `DevStg-Below` drop, is
recorded in the `# basis:` comment so nothing hides. Because it is a min and a
floor, the value answers **"what must still be cleared"**, never "what has been
achieved": a mature spine with one reopened draft derives `DevStg-Reqs` exactly as
a fresh scaffold does, and it is `ex-draft=`/`stage=` on the basis line that tell
the two apart.

THE SECOND AXIS, and the one this module's vocabulary is named for: the EIGHT-RUNG
STAGE LADDER (OI-21, ruled 2026-08-13) — Needs, Boundary, Reqs, Arch, LLReqs,
Tests, Impl, Release. A repo is IN a stage and CLEARS a bar. Stages are
`DevStg-<Label>` over a closed vocabulary with the position DERIVED; the three
bars partition the ladder. See the ladder block below `sn_bar` for the full model,
the recursion argument and the applies-when on the two inserted rungs.

This script reads STATES and picks the LEVEL; `trace.py` (run by check.py at that
level) ENFORCES the structure — orphans/decomposition/verified — at the derived
bar. The two compose: a draft is exempt from trace's orphan rule (so it can live
in the live spine) yet sits at `DevStg-Below` here (so it drops the bar). Auditing
correctness is the whole point, so every rule is fixture-tested.

Note: the derived range is the three runnable bars (the SN/SR/LLR/TC-derivable
ones). Release milestones beyond the spine stay separately recorded.

Usage:
    python scripts/derive_gate.py [--root .] [--docs DIR]   # compute + write docs/gate
    python scripts/derive_gate.py --check                    # recompute + guard rot (exit 1 on drift)
    python scripts/derive_gate.py --print                    # compute + print, do not write

Small CSV/heading loaders below are duplicated from trace.py per the kit's
independently-copyable-script convention (the F5 rule) — derive_gate.py stays a
self-contained drop-in, never importing the joined-spine engine.

Contracts: IF-050, IF-051 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.toml).
"""

import argparse
import csv
import datetime
import re
import subprocess
import sys
from pathlib import Path

# Sibling: the spine's registry CARRIER — the one home for
# the TOML tier tables, the key->column vocabulary and both readers. Run as a
# subprocess this script's own dir is sys.path[0] so a plain import resolves;
# the guard covers an in-process import (a test) whose sys.path does not yet
# carry scripts/ — the sanctioned-sibling idiom trace.py uses for trace_text.
try:
    import spine_carrier
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier

# THE SHIPPED SHARED-HELPER PACKAGE (owner ruling D-8, `OI-16`): `kitlib.ladder`
# is the ONE home for the eight-rung stage vocabulary this module used to define
# (WI-498 slice 0). Same guarded idiom as the sibling import above.
try:
    from kitlib import ladder as _ladder
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kitlib import ladder as _ladder

# --- THE BAR LADDER (the strictness axis) --------------------------------------
# The derived bar. `DevStg-Reqs` / `DevStg-Tests` / `DevStg-Impl` are the three
# runnable bars check.py knows; `DevStg-Below` is the INTERNAL sentinel for "below
# the lowest runnable bar" (pre-ratification / drafted), not a bar anyone clears
# or sits at — see the module docstring. BAR_NAMES maps the internal int back to
# the marker string.
#
# ONE VOCABULARY, TWO READINGS (owner ruling 2026-08-18). The `DevBar-*` prefix
# is retired: a repo is IN a stage and CLEARS a stage, and the SAME token names
# both — what differentiates them is the VERB, never a second spelling. So the
# clearable set is a strict SUBSET of the eight rungs, and a bar is named for the
# rung it CLOSES OUT, which is what the event is about:
#
#     clearing DevStg-Reqs   closes Needs, Boundary, Reqs  -> enters DevStg-Arch
#     clearing DevStg-Tests  closes Arch, LLReqs, Tests    -> enters DevStg-Impl
#     clearing DevStg-Impl   closes Impl                   -> enters DevStg-Release
#
# `DevStg-Impl` (was `DevBar-Release`) is the rename that is NOT a copy/replace,
# and the correction is deliberate: this bar never certified the Release rung —
# `DevStg-Release` sits OUTSIDE the derived range entirely (no `--stage-cleared`
# value runs it; see the registry-machinery reference). The old name and the live
# `DevStg-Release` rung differed by three letters while meaning a strictness
# level and a per-release milestone; collapsing removes that trap.
#
# The retired spellings survive ONLY as read-side aliases so an adopter's hooks,
# CI and `docs/stack.ini` keep working across the re-sync; nothing authored anew
# uses them.
BAR_BELOW, BAR_REQS, BAR_TESTS, BAR_RELEASE = 0, 1, 2, 3
BAR_NAMES = {
    BAR_BELOW: "DevStg-Below",
    BAR_REQS: "DevStg-Reqs",
    BAR_TESTS: "DevStg-Tests",
    BAR_RELEASE: "DevStg-Impl",
}
# The runnable bars, lowest first — the vocabulary check.py selects steps from.
BAR_ORDER = [BAR_NAMES[BAR_REQS], BAR_NAMES[BAR_TESTS], BAR_NAMES[BAR_RELEASE]]

# THE RETIRED-TAG ALIASES, stated ONCE here and imported by every reader (check.py,
# the stack.ini step loader, the WI `bar:` loader). One home, so the translation
# cannot drift between the three places an adopter's old value can arrive.
RETIRED_BAR_ALIASES = {
    "G1": BAR_NAMES[BAR_REQS],
    "G2": BAR_NAMES[BAR_TESTS],
    "G3": BAR_NAMES[BAR_RELEASE],
    # The `DevBar-*` prefix, retired 2026-08-18 for the one-vocabulary ruling.
    # Same contract as the `G*` row above it: a value an adopter's hook or CI
    # passes LITERALLY keeps working, and nothing authored anew emits one.
    # NOTE `DevBar-Release` resolves to `DevStg-Impl`, not to `DevStg-Release` —
    # the alias carries the correction, which is the whole reason it is a table
    # rather than a prefix swap.
    "DevBar-Reqs": BAR_NAMES[BAR_REQS],  # check_vocab: allow
    "DevBar-Tests": BAR_NAMES[BAR_TESTS],  # check_vocab: allow
    "DevBar-Release": BAR_NAMES[BAR_RELEASE],  # check_vocab: allow
}


def bar_ord(name):
    """The position of a bar name on BAR_ORDER — and it RAISES on an unknown value
    rather than degrading, exactly as `stage_ord` does for the stage axis.

    This is the rule the retired vocabulary broke: `check.py` used to compare gate
    NAMES as strings, which was correct only because `G1 < G2 < G3` happens to
    alphabetize. `DevStg-Impl < DevStg-Reqs < DevStg-Tests` lexically, so a
    lexical comparison on the new vocabulary is WRONG — and obviously wrong, which
    is the point. Route every comparison through here."""
    try:
        return BAR_ORDER.index(name)
    except ValueError:
        raise ValueError(
            "derive_gate: {!r} is not a bar on the ladder — expected one of {}"
            " (the retired G1/G2/G3 tags translate via RETIRED_BAR_ALIASES)".format(
                name, ", ".join(BAR_ORDER)
            )
        ) from None


def resolve_bar(value):
    """A caller-supplied bar name, with any retired gate tag translated via
    RETIRED_BAR_ALIASES.

    Returns `(canonical_name, was_retired)` so the caller can decide its own
    deprecation posture — check.py WARNS on the CLI (an adopter's hook passes the
    literal string and only a message will move them), while the stack.ini and WI
    `bar:` readers translate SILENTLY and leave the nagging to check_vocab.py,
    which sees the authored file and can name the line."""
    v = (value or "").strip()
    if v in RETIRED_BAR_ALIASES:
        return RETIRED_BAR_ALIASES[v], True
    return v, False


# SR Verification methods with no code to decompose, so they need a TC but no LLR.
# This is the same policy as trace.py's orphan rule (trace.LLR_EXEMPT); the promise
# is mechanized, not just prose — tests/test_rule_sync.py pins the two sets equal
# (WI-099). Critique is NOT here: its artifact is produced by code, only its
# acceptance is subjective.
LLR_EXEMPT = {"Analysis", "Inspection", "Attest"}

GATE_FILE = "docs/gate"


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is (the same
    guard as trace.py / check.py — a non-ASCII path can't wedge a cp1252 console)."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


# --- small self-contained loaders (duplicated from trace.py per the F5 rule) ---
def load_csv(path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig", errors="replace") as f:
        return list(csv.DictReader(f))


def refs(value):
    """Split a multi-ref cell (';', ',' or whitespace separated) into ids."""
    return [t for t in re.split(r"[;,\s]+", (value or "").strip()) if t]


def is_example(rid):
    return (rid or "").endswith("-000")


def is_drafted(row):
    """A row in the pre-approval `Drafted` state (closed Status vocabulary since
    D-9 step 1; renamed from `is_draft` with its value at step 5)."""
    return (row.get("Status") or "").strip().lower() == "drafted"


def is_approved(row):
    """The `Approved` state — the row's TEXT is blessed by a human — matched
    case-insensitively, the SAME rule as is_drafted (the one Status-casing rule,
    process.md §4). RENAMED FROM `is_verified` AT D-9 STEP 5, carrying the ruling
    that the vocabulary no longer makes a pass claim: `Verified` and `Planned`
    both fold here (OI-30 D1), and whether the tests pass is the harness's
    answer. Duplicated from trace.py per the F5 rule; pinned equal by
    test_rule_sync."""
    return (row.get("Status") or "").strip().lower() == "approved"


def llr_exempt(row):
    """SR Verification method in LLR_EXEMPT, matched on the stripped cell.
    Duplicated in trace.py per the F5 rule; pinned equal by test_rule_sync."""
    return (row.get("Verification") or "").strip() in LLR_EXEMPT


def phase_num(row):
    """The integer a row's free-form `Phase` cell digit-parses to (`v2`->2, `2`->2);
    None when blank/unparseable. The one phase-parse the kit uses — trace.py's
    schema rule and its `--phase` foundation filter reuse the same `\\d+` extraction
    so a downstream repo that kept `vN` labels parses identically (the phase doctrine,
    process.md §4). Duplicated in trace.py per the F5 rule."""
    m = re.search(r"\d+", (row.get("Phase") or ""))
    return int(m.group()) if m else None


_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.*)")


def sn_all_ids(text):
    """The SN id UNIVERSE: every `SN-###` token anywhere in stakeholder-needs.md
    — a whole-text scrape, so a prose mention counts exactly like a table row
    (registry-machinery-reference §2.1 records the sharp edge: a ratified,
    uncited prose mention caps the bar at DevStg-Below via the coverage rung). `-000`
    excluded. Duplicated from trace.py per the F5 rule; pinned equal by
    test_rule_sync (WI-408) — a divergence here would let the gate and trace's
    itemized listing disagree about which ids the rules run over."""
    return {u for u in re.findall(r"\bSN-\d+\b", text) if not is_example(u)}


def sn_draft_ids(text):
    """The set of Drafted SN ids in a needs registry's `text`, through whichever
    CARRIER wrote it.

    Under TOML draft-ness is a FIELD on the need (`status = "Drafted"`); under the
    legacy markdown it was SECTION-AS-STATE — every `SN-###` appearing under a
    heading containing the word "draft". Both are read; the dispatch is
    `spine_carrier.needs_from_text`, and it is load-bearing rather than tidy: a
    heading scan over a TOML file finds NO headings, reports ZERO drafts, and
    every draft need reads as ratified — which floats the derived gate upward.
    A migration whose failure mode is "the gate rises" is the one shape this
    repo can least afford, so the carrier is sniffed rather than assumed.

    Retiring section-as-state also closes a live sharp edge the 2026-08-10
    sitting hit: a prose MENTION of an id under the draft heading silently
    re-drafted an already-attested need, because the id universe is a whole-text
    scrape while draft-ness was a heading scan. A field cannot be set by
    mentioning the id in a sentence. `-000` placeholders stay excluded.
    Duplicated in derive_gate.py per the F5 rule; pinned equal by
    test_rule_sync."""
    return spine_carrier.draft_ids_from_text(text)


def sn_cited_ids(srs):
    """Every SN id cited by >=1 SR row's `SN-Refs` cell — the coverage set the
    SN-coverage rung reads (WI-401). No filtering here: -000 rows are excluded
    by the caller's row filter, and a Drafted SR's citation is deliberately in the
    set (the raw view matches trace.py's orphan exemption; the ex-draft
    counterfactual re-runs this on the non-draft subset instead). Duplicated in
    trace.py per the F5 rule; pinned equal by test_rule_sync.

    Implements: SR-049, LLR-147"""
    return {x for r in srs for x in refs(r.get("SN-Refs"))}


# --- per-artifact bar rules (docs/archive/specs/derived-gate-model.2026-07-20.md §3) -------------
# THE CEILING (owner ruling OI-30 D2, 2026-08-15). `sr_bar` stops at
# `BAR_TESTS`: `DevStg-Impl` is UNREACHABLE FROM A STATUS CELL until a harness
# driver computes the release bar from test evidence.
#
# WHY IT IS A GUARD RAIL AND NOT A DOWNGRADE. `Verified` used to make two claims
# at once — the text is ratified AND the evidence passed — and `sr_bar` read the
# pair as decomposed+Verified -> DevStg-Impl. D-9 step 5 deleted the pass claim
# from the vocabulary (OI-30 D1 folded `Planned` in beside `Verified`), so
# WITHOUT this ceiling a formerly-`Planned` row with children would satisfy the
# old rule and the derived gate would RISE to DevStg-Impl for rows that never
# passed anything. That is the migration plan's §F5 risk, and this is its named
# mitigation.
#
# WHY IT LOOSENS NOTHING. Every consumer of `DevStg-Impl` was enumerated before
# the ruling — harness strictness selection, the rung-6/7 stage record, the
# release checklist; explicitly NOT scheduling — and every one is
# monotone-stricter in the bar. Withholding the top bar therefore withholds
# ESCALATION and relaxes no check that was running. `check.py --gate
# DevStg-Impl` stays explicitly invocable at any time, so the strict plan is
# never unreachable, only never AUTO-SELECTED from a hand-set cell.
#
# THE OWNER'S FRAMING, recorded as the design intent: the derived gate can only
# be truly computed by RUNNING the test sequence, which is more honest than
# inferring it from a status cell.
#
# HOW IT LEAVES. Delete these three lines and the `_RELEASE_CEILING` flag when
# the harness driver lands; `tests/test_derive_gate.py`'s ceiling pin is
# commented as deliberately deleted at that moment, so removal is an act rather
# than a drift.
_RELEASE_CEILING = BAR_TESTS

# The suffix a HUMAN-FACING render of the bar name carries while the ceiling
# holds, so the ceiling is never read as a regression. ONE HOME: `bar_label`
# below is the only place that composes it, and every human surface calls that
# rather than formatting the name itself. It is deliberately NOT part of
# `BAR_NAMES` or of `docs/gate`'s runnable last line — those are MACHINE values
# that `check.py` and CI match exactly, and annotating them would break every
# consumer to make a note to a reader.
_CEILING_NOTE = "(Release: pending harness driver)"


def bar_label(name):
    """A bar name as a HUMAN reads it: the machine value, plus the ceiling note
    when the value is the one the ceiling holds it at.

    The ONE rendering home (OI-30 D2's mitigation). `traj_status` and any other
    prose surface call this instead of interpolating `name`, so the note cannot
    appear on one surface and not another — the failure mode a second rendering
    path guarantees. Unknown or empty names pass through untouched: a surface
    reading an older `docs/gate` should say what it found, not decorate it."""
    if name == BAR_NAMES[_RELEASE_CEILING]:
        return "{} {}".format(name, _CEILING_NOTE)
    return name


def sr_bar(sr, has_llr, has_tc):
    """The bar an SR row has reached, from its Status + whether it is decomposed.

    CEILINGED AT `BAR_TESTS` since OI-30 D2 — see the block above for why, and
    for how the ceiling is removed when the harness driver lands."""
    if is_drafted(sr):
        return BAR_BELOW
    exempt = llr_exempt(sr)
    decomposed = (exempt or has_llr) and has_tc
    if decomposed:
        return _RELEASE_CEILING
    return BAR_REQS  # a ratified requirement not yet decomposed


def maturity_bar(row):
    """An LLR/TC caps the bar only when its own maturity is DRAFTED (`DevStg-Below`
    — the new-phase signal). Once present, its own Status does NOT independently
    gate the top bar: the SR's `Approved` status drives DevStg-Tests ->
    DevStg-Impl (matching trace.py's --require-verified bar, which checks SRs,
    not LLR/TC status), and the LLR/TC's *existence* is what makes its SR
    decomposed (DevStg-Tests, decided in sr_bar). So a present, non-Drafted LLR/TC
    contributes DevStg-Impl and never caps.

    THIS IS THE ONE SPINE RULE THAT ASKS THE LADDER'S OWN QUESTION ("does this row
    cap its rung?"), so at D-9 step 5 it was re-keyed onto `SPINE_MATURITY`
    through the SAME `_maturity`/`_caps` pair every off-spine tier uses — the
    table edit correction C2 promised, rather than a fourth private copy of the
    predicate.

    BEHAVIOUR IS UNCHANGED BY THE RE-KEY, in both directions. Every non-`Drafted`
    value in the table maps at or above APPROVED and does not cap — that was true
    of the transitional `Modified` and is true of `Founded`, which step 8 armed —
    exactly as the old `is_draft`-only test was.

    **THE UNKNOWN VALUE NOW FAILS CLOSED (2026-08-20, ROUND-SOL MAJOR-6), and
    the migration tolerance it was carrying is kept by NAME instead.** This
    passed `default=APPROVED`, reasoning that an unrecognized spine value is
    already an integrity ERROR on the always-on floor, so holding its rung open
    would punish one fault twice and would let D-9's rename silently LOWER the
    derived gate for a downstream repo whose LLRs still read `Implemented`. The
    first half of that reasoning survives; the second half was doing the work,
    and it did not need a blanket default to do it. A blanket default cannot tell
    `Implemented` from `Approvd`: a one-character typo derived the same finished
    bar as an approval, on the axis the automation dial reads, and `derive_gate`
    runs perfectly well without the integrity checker ever having been invoked.
    So the retired spellings are enumerated (`SPINE_TRANSITIONAL`) and read
    exactly as they always did, while everything else takes `_maturity`'s
    fail-honest DRAFTED — the typo hole closes and the migration tolerance
    stays."""
    return (
        BAR_BELOW
        if _caps(_maturity(row.get("Status"), SPINE_MATURITY_READ))
        else BAR_RELEASE
    )


def is_founded(row):
    """The ladder's top rung (repo-lock D-9): settled AND the artifacts the row
    calls for EXIST. Armed for the spine at D-9 step 8, as it armed for CMP at
    the registry status unification — the word becomes legal, no live cell moves
    to it. What matters HERE is that it reads ABOVE `Approved`: `SPINE_MATURITY`
    maps it to FOUNDED (never caps) and `spine_stage`'s Impl->Release
    discriminator accepts it, so arming a word cannot LOWER the derived gate —
    the rule the step-5 rename ran under. The DISCHARGE is computed per tier
    elsewhere (migration plan C4); this reads the cell, like its two siblings.
    Duplicated from trace.py per F5; pinned equal by test_rule_sync."""
    return (row.get("Status") or "").strip().lower() == "founded"


# `is_planned` WAS DELETED AT D-9 STEP 5 (not re-keyed) with the word it read:
# OI-30 D1 folded `Planned` into `Approved`, so `is_approved` answers for those
# rows and the `planned=` basis counter goes with the predicate. It was step-2
# insurance against a value no predicate recognized, and its own docstring said
# it would be deleted here rather than migrated.
#
# `is_modified` WAS DELETED AT D-9 STEP 7 on the same terms, as its own docstring
# promised. It marked "approved text that has since moved" and survived step 5
# only so the kit never had a commit with NO drift detector; its successor (the
# `docs/archive/last_approved/` comparison) ran alongside it through the signing.
# `modified=N` went with it, for `planned=`'s reason: a count of a value the
# closed enum cannot hold counts integrity errors, not pending rows.


def sn_bar(sn_id, draft_ids, cited_ids):
    """A Drafted SN is `DevStg-Below` — and that is the ONLY rung that fires on a
    draft: it is exempt from the coverage rung below exactly as it is exempt from
    trace.py's orphan rule, so one fact never fires two findings at once. A
    RATIFIED SN must be cited by >=1 SR's `SN-Refs` (WI-401, owner ruling
    2026-08-01): ratified-but-uncovered caps the raw level at `DevStg-Below`,
    because a ratified need no SR answers has not earned `DevStg-Reqs`. This rung
    is the BAR INPUT; the itemized "SN {id} has no SR" listing stays trace.py's
    orphan finding at DevStg-Tests strictness — the same states-here /
    structure-there split the module docstring describes. A covered ratified SN
    has no obligation past `DevStg-Reqs` and never caps the repo (contributes
    `DevStg-Impl` to the min).

    Implements: SR-049, LLR-147"""
    if sn_id in draft_ids:
        return BAR_BELOW
    return BAR_RELEASE if sn_id in cited_ids else BAR_BELOW


# --- SN-029 / OI-21: the SECOND derived axis — the EIGHT-RUNG STAGE LADDER ------
# WHY TWO AXES. The bar answers "how strict is the harness right now" — its
# vocabulary is `DevStg-Reqs|DevStg-Tests|DevStg-Impl` and `check.py` selects
# steps from it. The human ratification level answers a different question: "how
# far up the ladder is a HUMAN still the acceptor". Those are not the same ladder,
# and the retired G-numbering could express neither cleanly: `G2` conflated "LLRs
# and TCs exist" AND doubled as the pull a `Modified` row applies, so there was no
# G that meant "TCs are in process". Forcing one axis to carry both is how a dial
# ends up meaning something subtly different at each of its five reading sites.
#
# THE RULED MODEL (owner, 2026-08-12; the ladder re-ruled 2026-08-13 as OI-21):
# **stages are the rungs of the decomposition — a repo is IN one; bars are the
# subset of rung boundaries a human must certify — you CLEAR one.** The stage is
# state, the bar is an event.
#
# THE VOCABULARY ITSELF MOVED OUT (WI-498 slice 0, plan §5 item 0). The rung
# strings, their order, `STAGE_OF`, `STAGE_DESC` and the `stage_ord` lookup are
# `kitlib.ladder`'s — one home, imported by everyone, so the equality pins that
# used to hold `agent_common`'s restatement in step retire: the drift is now
# UNREPRESENTABLE rather than DETECTED (the WI-448 declared-line precedent,
# `tests/test_rule_sync.py`). The names are RE-EXPORTED below because
# `derive_gate.STAGE_*` is the spelling six modules and the test suite already
# read, and re-pointing every citation is churn this slice does not need.
# The ladder's own design rationale — why requirements precede architecture, why
# the label and not the ordinal is the identifier, why it is not monotonic —
# travelled with it and is NOT restated here.
STAGE_NEEDS = _ladder.STAGE_NEEDS
STAGE_BOUNDARY = _ladder.STAGE_BOUNDARY
STAGE_REQS = _ladder.STAGE_REQS
STAGE_ARCH = _ladder.STAGE_ARCH
STAGE_LLREQS = _ladder.STAGE_LLREQS
STAGE_TESTS = _ladder.STAGE_TESTS
STAGE_IMPL = _ladder.STAGE_IMPL
STAGE_RELEASE = _ladder.STAGE_RELEASE
STAGE_ORDER = _ladder.STAGE_ORDER
STAGE_OF = _ladder.STAGE_OF
STAGE_DESC = _ladder.STAGE_DESC
stage_ord = _ladder.stage_ord


# --- THE MATURITY MAPPING TABLE — ONE HOME (OI-21 question 5b) -----------------
# THE PROBLEM IT SOLVES. The min-fold folded over SN/SR/LLR/TC only, which is why
# rung 1 (Boundary) had no machine-readable state and rung 3's `CMP.State` was
# read by nothing that gates. Folding IF and CMP in is what makes the recursion
# self-reporting — but those two registries carry their OWN maturity vocabularies,
# and the spine carries a third — which, since D-9 migration steps 5/7/8, is
# `Drafted`/`Approved`/`Founded` and therefore SPEAKS THIS TABLE'S OWN WORDS.
#
# So every vocabulary maps onto ONE set of ladder semantics, stated here and
# nowhere else:
#
#   DRAFTED   the row exists but is not settled — it CAPS its rung (work in flight)
#   APPROVED  the row is settled at its tier — it does not cap
#   FOUNDED   the row is settled AND demonstrated — it does not cap
#
# The migration promised this would be a TABLE EDIT rather than a predicate
# rewrite, and step 5 is that edit landing: `SPINE_MATURITY` below is the spine's
# row of this one table, and it is DECLARED rather than inferred — the previous
# revision had every other tier in the table and the spine only in prose.
DRAFTED, APPROVED, FOUNDED = "Drafted", "Approved", "Founded"

# THE SPINE (SR/LLR/TC `Status`) — the row D-9 step 5 added. Keys lower-cased,
# like every other table here (`_maturity` lowercases before the lookup), so this
# is the closed `STATUS_VALUES` vocabulary spelled in the ladder's own terms.
#
# THE TRANSITIONAL `modified` ROW LEFT AT STEP 7, as this comment's previous
# revision said it would; the state it named is now read by comparing the row
# against its `docs/archive/last_approved/` copy, which is not a maturity.
# `founded` JOINED AT STEP 8 under the rule that governed the rename: it maps to
# FOUNDED, which does not cap, so a row at the top rung cannot read as work in
# flight and drop the bar. Its demonstration is computed per tier (migration plan
# C4), never asserted by this table. DevStg-Release still does not follow from a
# `Founded` cell — that driver is the harness's answer, which is why `sr_bar`
# stays ceilinged at `BAR_TESTS` (OI-30 D2).
SPINE_MATURITY = {
    "drafted": DRAFTED,
    "approved": APPROVED,
    "founded": FOUNDED,
}

# THE RETIRED SPELLINGS, NAMED (2026-08-20, ROUND-SOL MAJOR-6). Not live
# vocabulary and never part of `SPINE_MATURITY`: nothing may author these, and
# the closed-enum integrity rule names any cell that does. What naming them buys
# is that `maturity_bar` can tell a MID-MIGRATION registry from a TYPO, which a
# blanket `default=APPROVED` could not — `Approvd` derived the same finished bar
# as `Approved`, on the axis the automation dial reads. Each read is the
# documented one: `modified` left at D-9 step 7 and an amended row was still
# APPROVED; `implemented` is the pre-rename LLR/TC word this tolerance exists
# for; `verified`/`planned` folded INTO `approved` at step 5 (OI-30 D1); `draft`
# is the pre-rename `drafted` and is the one that CAPS, since promoting a draft
# on a spelling is the error this table must not make. Anything outside both
# tables holds its rung open (`_maturity`'s fail-honest default).
SPINE_TRANSITIONAL = {
    "modified": APPROVED,
    "implemented": APPROVED,
    "verified": APPROVED,
    "planned": APPROVED,
    "draft": DRAFTED,
}

# What `maturity_bar` reads: the live ladder plus those retired spellings,
# composed ONCE so "what does this accept?" has one home.
SPINE_MATURITY_READ = dict(SPINE_TRANSITIONAL, **SPINE_MATURITY)

# BOUNDARY CROSSINGS — the depth-0 frame's `[boundary.B-##]` rows in
# `external.toml` (rung 1). `Status` is the tier's ONE maturity field — the name
# it carries since the 2026-08-17 registry status unification, which retired the
# transitional `Approval` spelling this table was first keyed on.
#
# THIS TABLE REPLACED AN `IF_MATURITY` KEYED ON `Stability` AT WI-442, and the
# swap is the whole reason that commit could not be split. `Stability` was the
# sole input to `boundary_incomplete`; deleting the column without re-keying the
# predicate in the same commit would have left every IF row reading an
# unrecognized value, which `_maturity` maps to DRAFTED — rung 1 pinned open
# forever by a column that no longer exists, reporting the right stage for
# entirely the wrong reason.
#
# NOT Founded on `approved`, for the reason the old table gave and which
# survives the re-key unchanged: an approval says the crossing is agreed, it says
# nothing about the crossing having been demonstrated.
# `drafted` (not `draft`) since D-9 step 5b: the off-spine approval vocabulary
# moved with the spine's so ONE word means one thing across every registry —
# `interfaces.toml` and `external.toml` cells, both file headers, and the two
# shipped templates changed in the same commit.
BIF_MATURITY = {
    "drafted": DRAFTED,
    "approved": APPROVED,
}

# CMP rows — the partition (rung 3).
# CMP now speaks the ONE enum (registry status unification, 2026-08-17), and
# that collapses this table to the identity over it. What it used to hold was
# two axes at once: `planned`/`built`/`verified` were maturity spelled in
# regenerated retired spine words, while `has-gap`/`deprecated` were LIFECYCLE
# facts folded onto maturity — exactly the conflation SN's `kind` was. The
# lifecycle half moved to its own `standing` field, which this table does not
# map because it is not a maturity — but ONE of its values still answers a
# rung-3 question, and `CMP_STANDING_CLEARS` below is where it answers it.
#
# CMP KEEPS ITS OWN TABLE rather than sharing `SPINE_MATURITY`, RE-EXAMINED at
# D-9 step 8 rather than inherited: the two are byte-identical as of that step,
# so collapsing them is the obvious move. Declined on the unification plan's own
# §7(c) recommendation — two registries' vocabularies that HAPPEN to coincide,
# not one with two names. They have already diverged in both directions (CMP
# reached `founded` first; the spine carried `modified` and CMP never did), and
# one shared table would make the next per-registry subset (which decision 12
# provides for) a change to the OTHER registry's ladder.
#
# `founded` is REACHABLE HERE and nowhere else off-spine: a demonstrated
# partition is a claim something computes, which is the whole test for whether a
# tier may carry the word.
CMP_MATURITY = {
    # (Keys lower-cased — see `_maturity`.)
    "drafted": DRAFTED,
    "approved": APPROVED,
    "founded": FOUNDED,
}

# CMP `standing` — the LIFECYCLE axis, and the one value on it that rung 3 must
# still read. Restores, on its new home, the protection the pre-split
# `CMP_MATURITY` entry stated verbatim and `6f39b2ed` deleted without citing:
#
#   `has-gap` is an explicit statement that the partition does NOT yet hold —
#   the strongest possible DRAFTED signal, and the one place a lenient mapping
#   would let a known-broken partition report a finished architecture rung.
#
# The split was right — `has-gap` is not a maturity — but it is a direct
# statement ABOUT the partition, which is exactly what rung 3 asks, so it has to
# be read SOMEWHERE. Without this, `Status = "Founded"` + `standing = "has-gap"`
# (a demonstrated partition that also records a gap: precisely the combination
# the new axis was created to make expressible) closes rung 3 (2026-08-17 desk
# round, F1). `deprecated` does NOT hold the rung — a decided state, not work in
# flight, which is the reading the pre-split table also gave it (APPROVED).
#
# Stated as what CLEARS rather than what holds, so the fail-honest direction is
# the default: an unreadable standing holds the rung open, the same choice
# `_maturity` makes and for the same reason (the tier's schema is ADVISORY, so a
# typo really can arrive here). An ABSENT cell is not unreadable — `omit =
# active` is the declared shorthand — so it clears.
CMP_STANDING_CLEARS = frozenset({"active", "deprecated"})


def _standing_holds_rung(value):
    """Does this CMP `standing` cell hold the architecture rung open?

    Not a maturity lookup: `standing` answers a lifecycle question, and only its
    `has-gap` value (plus anything unreadable) bears on whether the partition
    holds. See `CMP_STANDING_CLEARS` for why the polarity is inverted."""
    text = str(value or "").strip().lower()
    if not text:
        return False
    return text not in CMP_STANDING_CLEARS


def _maturity(value, table, default=DRAFTED):
    """A registry cell's ladder semantic through `table`, matched case-insensitively.

    An UNRECOGNIZED value reads DRAFTED — the fail-honest direction — unless the
    caller overrides `default`. The ONE caller that does is `maturity_bar`, and
    its reason is stated there: the spine's `Status` is a closed INTEGRITY enum
    whose unknown values are already an always-on error, so holding the rung open
    for them would punish the same fault twice and would make D-9's rename lower
    the derived gate. Every ADVISORY-schema tier keeps the fail-honest default. These two
    tiers are schema-ADVISORY (WI-443 ruled the enums warn-first, so a typo never
    fails the harness), which means an unknown value genuinely can reach here; the
    choice is between "an unreadable row reports finished" and "an unreadable row
    holds its rung open", and only the second is safe on an axis the automation
    dial reads.

    The case-insensitive match is real, not aspirational: the tables are keyed
    lower-cased below. It used to be a docstring claim only — every key happened
    to be spelled exactly as the registries spelled it, so the claim cost nothing
    and bought nothing. WHAT THE FOLD ACTUALLY BUYS, stated accurately after an
    adversarial round caught the first version overclaiming: it defends against a
    hand-authored `Approved`/`Drafted`, which no other check validates — the enums
    are schema-ADVISORY, so a capitalized cell reaches here and would otherwise
    read DRAFTED. It does NOT fix any live or shipped value; every one of those
    already matched exactly."""
    return table.get((value or "").strip().lower(), default)


def _caps(semantic):
    """True when a ladder semantic means work is still in flight at its rung."""
    return semantic == DRAFTED


def _decomposed_sr_ids(llrs, tcs):
    """`(SR ids some LLR answers, SR ids some TC verifies)` — the decomposition
    index both the stage axis and the gate arithmetic ask for.

    One home because two copies of a join rule is exactly how the two axes would
    drift apart while still agreeing on the day they were written (WI-347: the
    cross-SCRIPT duplication F5 sanctions never licensed intra-file copies)."""
    return (
        {x for r in llrs for x in refs(r.get("SR-Refs"))},
        {x for r in tcs for x in refs(r.get("Verifies"))},
    )


def boundary_incomplete(bifs, have_registry):
    """Rung 1's predicate — is the BOUNDARY INVENTORY still in work?

    READS `external.toml`'s `[boundary.B-##]` ROWS. Until WI-442 it read the IF
    registry's `Stability` column and nothing else, which was the honest best
    available: nothing in the schema typed a crossing as external, so the rung
    could only report whether the INTERNAL seam inventory had settled and call it
    the boundary. Sitting 2 ruled the frame into its own tier (§1R.5, decision 3),
    so the predicate now reads the thing it always claimed to.

    APPLIES-WHEN (OI-14's ruled A6 shape, warn-first): the rung applies only when
    an `external.toml` FILE exists. A project that never declares a boundary is
    NOT held at DevStg-Boundary forever — `have_registry` is False and the rung is
    skipped. That is the whole difference between a rung that ships to every
    adopter and one that ships to the adopters who declared a boundary. The
    applies-when MOVED with the predicate: a repo that carries interfaces.toml and
    no external.toml now skips rung 1 rather than being held by its internal
    seams, which is the correction, not a loosening.

    WARN-HONEST WHEN IT DOES APPLY. A registry that exists but declares NO real
    crossing is honestly incomplete: the file says the project intends to type its
    frame and has not. And any crossing at DRAFTED maturity (`approval = "draft"`)
    is a frame declared and not yet ratified. Both cap the rung.

    APPROVAL, NOT REALIZATION COVERAGE — the two readings of the ruling, resolved
    rather than assumed. 13u's wording gates on BIF *approval*; §1R.5's wording
    ("every declared BIF settled, every BIF realized or explicitly deferred")
    names approval AND a second conjunct. They are different predicates, and this
    is the first: whether each declared crossing carries a realizing IF row is
    DECISION 6, deferred BY RULING to post-schema (sitting-2 §4.0), and gating on
    it here would take a decision nobody has. It is not a hypothetical gap — four
    of the six locked crossings are realized by no IF row today, so the second
    conjunct would hold rung 1 down on work decision 6 has not yet scoped, and it
    would do so under a predicate that reads like ratification. When decision 6
    lands, adding the conjunct is a two-line change HERE, with the coverage rule
    stated in its own docstring.

    NOTE WHAT THIS STILL DOES *NOT* CLAIM. An approved crossing is agreed, not
    demonstrated. Nothing here reports that anything was built."""
    if not have_registry:
        return False
    if not bifs:
        return True
    return any(_caps(_maturity(r.get("Status"), BIF_MATURITY)) for r in bifs)


def arch_incomplete(cmps, have_registry):
    """Rung 3's predicate — is the PARTITION still in work?

    Same applies-when shape as `boundary_incomplete`: no components registry, no
    rung. With one, a partition of nothing is incomplete, and a component at
    DRAFTED maturity (`Status = "Drafted"`) is a scope proposed and not yet
    realized.

    TWO AXES ARE READ, not one. The registry status unification (2026-08-17)
    split CMP's single field into `Status` (maturity) and `standing`
    (lifecycle), and `standing = "has-gap"` is a direct statement that the
    partition does not hold — a rung-3 fact wherever it is spelled. It is read
    through `_standing_holds_rung`, whose comment carries the restored
    rationale; without it a `Founded` row could record a known gap and still
    report a finished rung.

    THIS IS THE RUNG THAT MAKES THE RECURSION SELF-REPORTING. Rungs 2 and 3
    oscillate as the decomposition descends, and the mechanism is exactly this
    predicate reading a newly minted `Drafted` CMP row: identifying a
    sub-component DROPS the reported stage back to Arch with nobody deciding to,
    which is the honest report."""
    if not have_registry:
        return False
    if not cmps:
        return True
    return any(
        _caps(_maturity(r.get("Status"), CMP_MATURITY))
        or _standing_holds_rung(r.get("Standing"))
        for r in cmps
    )


def spine_stage(
    srs,
    llrs,
    tcs,
    sn_ids,
    sn_draft,
    bifs=None,
    cmps=None,
    have_bifs=False,
    have_cmps=False,
    cited_srs=None,
):
    """The rung currently IN WORK — the STATE axis (a repo is *in* a stage), and
    the one a human-ratification level is compared against. Returns a
    `DevStg-<Label>` from STAGE_ORDER.

    Read as the LOWEST unfinished rung — the one work is happening at, and
    therefore the one a human boundary has to be compared against.

      DevStg-Needs      a need is a draft, none is ratified, or a ratified one
                        has no SR answering it
      DevStg-Boundary   ...and the declared boundary inventory is in work
      DevStg-Reqs       ...and a requirement is Drafted
      DevStg-Arch       ...and the declared partition is in work
      DevStg-LLReqs     ...and an LLR is missing or Drafted
      DevStg-Tests      ...and a TC is missing or Drafted
      DevStg-Impl       ...and every SR is decomposed and every TC authored and
                        non-Drafted, but some SR is not yet `Approved` (or above)
      DevStg-Release    nothing in work: every rung is settled and approved

    THE `Modified` ARM OF THE Reqs RUNG RETIRED AT D-9 STEP 7 — no cell records
    "amended after attestation" any more, and the successor (the snapshot
    comparison) is deliberately NOT read here; see the rung itself.

    THE TWO INSERTED RUNGS (OI-21) read from the IF and CMP registries, which
    joined the fold here — see `boundary_incomplete` / `arch_incomplete` for the
    applies-when that keeps them free for a project that adopts neither.

    THE SPINE RUNGS STILL READ PREDICATES (`is_drafted`/`is_approved`/
    `is_founded`) rather than `SPINE_MATURITY`, and that is not an oversight:
    the rungs need distinctions finer than the three-way ladder (which child is
    Drafted, which SR has not been blessed), while the ladder answers only "does
    this cap its rung". `maturity_bar` — the one spine question that IS the
    ladder question — reads the table, so the row is live rather than decorative.

    CAVEAT ON THE Impl->Release DRIVER. DevStg-Impl ends when every SR reads
    `Approved`, which is a registry CELL, not a harness run. The intended signal is
    the harness (green tests at the declared tier and coverage); the cell is
    today's interim proxy for it, and repo-lock D-9's correction owes the swap to a
    later batch. Nothing here should be read as proof the tests passed.

    WHICH RUNG OWNS A MISSING ARTIFACT: the rung the artifact belongs to, not its
    parent. An SR with no LLR yet is DevStg-LLReqs, because what is being written
    is an LLR. Reading it as DevStg-Reqs (the older shape) made the lower rungs
    unreachable during exactly the period they describe — every SR had to be fully
    decomposed before a Drafted child could be seen at all — which left the axis
    unable to express "TCs are human-held but LLRs are not", the distinction the
    axis exists for.

    WHICH RUNG OWNS AN UNBLESSED SR: it is checked LAST, after the children. An
    SR reaches `Approved` only once its LLRs and TCs are green, so while a child
    is still in flight the child's rung is the honest answer. (A two-case rule
    until step 7, which retired the `Modified` case that was checked FIRST.)

    `cited_srs` IS THE SCOPE OF THE NEED-COVERAGE RUNG, and it exists for the
    PER-PHASE call (WI-498 slice 1). The coverage question — "does every ratified
    need have a requirement answering it" — is repo-global: a need answered only
    by phase 1's requirements is answered. Running this function over one phase's
    rows with the default would read every OTHER phase's needs as uncovered and
    report DevStg-Needs for every phase but the first. So a per-phase caller passes
    the repo's whole (settled) SR set here while `srs` stays the phase's own rows.
    Default `None` means "the rows I was given", which is the repo-wide call and
    is byte-for-byte what this function did before the parameter existed.

    Two corners are explicit. A repo with no real SRs at all is DevStg-Needs, NOT
    DevStg-Release — the vacuous-lowest-bar short circuit in `_raw_level` exists
    for the bar's own arithmetic and would read as "everything is finished" here,
    which is precisely backwards. And a RATIFIED-BUT-UNCITED SN is DevStg-Needs,
    applying WI-401's coverage rung on the same subset `_raw_level` uses: a need
    with no requirement answering it is unfinished work at the needs rung."""
    bifs = bifs or []
    cmps = cmps or []
    if any(u in sn_draft for u in sn_ids) or not sn_ids:
        return STAGE_NEEDS
    if not srs:
        return STAGE_NEEDS
    if boundary_incomplete(bifs, have_bifs):
        return STAGE_BOUNDARY
    if any(is_drafted(r) for r in srs):
        return STAGE_REQS
    if any(
        u not in sn_cited_ids(cited_srs if cited_srs is not None else srs)
        for u in sn_ids
    ):
        return STAGE_NEEDS
    # THE `Modified` RUNG RETIRED AT STEP 7 with the word it read (owner ruling
    # 2026-08-17m). NOT re-keyed onto drift: this axis reads CELLS, and reaching
    # into `docs/archive/` would make a pure row computation read the filesystem.
    if arch_incomplete(cmps, have_cmps):
        return STAGE_ARCH
    llr_sr_refs, tc_refs = _decomposed_sr_ids(llrs, tcs)
    if any(
        not llr_exempt(sr) and sr.get("SR-ID") not in llr_sr_refs for sr in srs
    ) or any(is_drafted(r) for r in llrs):
        return STAGE_LLREQS
    if any(sr.get("SR-ID") not in tc_refs for sr in srs) or any(
        is_drafted(r) for r in tcs
    ):
        return STAGE_TESTS
    # THE Tests-vs-Impl DISCRIMINATOR. Falling through both rungs above means
    # every SR is decomposed and every TC is authored and non-Drafted — the test set
    # is written, so "TCs in work" is no longer true. What remains is making them
    # pass, which is DevStg-Impl. (`is_approved` is the interim proxy for that;
    # the intended signal is the harness — see the CAVEAT above.)
    # `is_founded` JOINS THE TEST AT STEP 8 — a correction, not a widening:
    # `Founded` is `Approved` plus a demonstration, so reading only `is_approved`
    # would hold a Founded SR at DevStg-Impl forever.
    if not all(is_approved(r) or is_founded(r) for r in srs):
        return STAGE_IMPL
    return STAGE_RELEASE


# THE STAGE -> BAR CROSSING TABLE IS GONE (WI-498 slice 2, ruled plan §5 item 2).
# `STAGE_BAR` and `stage_to_bar` declared which bar a rung sat under, and their
# own docstring recorded that NOTHING derived the bar from the stage in
# production — it was a reader's reconciliation between two axes. Selection now
# keys on the stage alone, so there are no longer two axes for a reader to
# reconcile: the table answered a question nobody asks any more. The bar itself
# stays computed below, because `docs/gate` is still WRITTEN for the detectors
# that read its committed history (phase-drop, tier signal — slice 4); when
# slice 5 retires the file, the rest of this axis goes with it.


def _raw_level(srs, llrs, tcs, sn_ids, sn_draft):
    """`(raw_level, sr_bars)` over ONE set of spine rows.

    The raw level is the min over every in-scope artifact's bar (SN drafts, SR
    maturity, LLR/TC maturity — including WI-401's SN-coverage rung, whose cited
    set is built from THIS call's `srs`); a set with no real SRs is `DevStg-Reqs`
    (requirements-drafting), never a vacuous `DevStg-Impl` from
    ratified-SN-only. Taken as a function of its rows rather than of `docs` so
    `compute` can ask it the counterfactual question too — the same arithmetic,
    over the non-draft subset (`ex-draft`), which is what tells a mature spine
    held down by drafts apart from an early one (WI-341). The coverage rung rides
    that subset consistently: a citation on a removed Drafted SR leaves with its
    row, so the counterfactual never fabricates coverage a ratified spine does not
    have.
    """
    llr_sr_refs, tc_refs = _decomposed_sr_ids(llrs, tcs)
    cited = sn_cited_ids(srs)
    sr_g = {
        r["SR-ID"]: sr_bar(r, r["SR-ID"] in llr_sr_refs, r["SR-ID"] in tc_refs)
        for r in srs
    }
    if not srs:
        return BAR_REQS, sr_g
    raw = min(
        [sr_g[k] for k in sr_g]
        + [sn_bar(u, sn_draft, cited) for u in sn_ids]
        + [maturity_bar(r) for r in llrs]
        + [maturity_bar(r) for r in tcs]
    )
    return raw, sr_g


def load_spine(docs):
    """Every registry row both derivations read, loaded once through the carrier.

    EXTRACTED FROM `compute` (WI-498 slice 1) so the STAGE derivation
    (`derive_stage.py`) reads the same rows through the same resolution rules
    rather than re-implementing the load. It is a pure read: no filtering beyond
    dropping the `-000` example rows, and the `have_*` applies-when flags travel
    with the rows they qualify, because a caller that separated them would have to
    remember that an ABSENT registry and an EMPTY one mean opposite things at the
    two inserted rungs.

    Returns exactly the keyword arguments `spine_stage` takes."""
    # The three spine tiers read through the CARRIER, which resolves TOML or CSV
    # and hands back rows under today's column names — so both derivations are
    # untouched by the migration. `load_csv` stays for the off-spine registries,
    # which do not move.
    raw_srs = spine_carrier.load(
        docs / "requirements" / "system-requirements.toml", "SR-ID"
    )
    raw_llrs = spine_carrier.load(
        docs / "requirements" / "low-level-requirements.toml", "LLR-ID"
    )
    raw_tcs = spine_carrier.load(docs / "test" / "test-cases.toml", "TC-ID")
    srs = [r for r in raw_srs if r.get("SR-ID") and not is_example(r["SR-ID"])]
    llrs = [r for r in raw_llrs if r.get("LLR-ID") and not is_example(r["LLR-ID"])]
    tcs = [r for r in raw_tcs if r.get("TC-ID") and not is_example(r["TC-ID"])]

    # THE NEEDS FILE RESOLVES THROUGH THE CARRIER, and this is the one place in
    # the kit where a literal suffix would be worst: an existence test on `.toml`
    # alone answers False for a repo still on markdown, `sn_ids` and `sn_draft`
    # both come back EMPTY, and an empty draft set makes every draft need read as
    # ratified — the derived value RISES on a registry the reader simply could not
    # find. Absent must mean absent, never "no drafts".
    sn_md = spine_carrier.resolve(
        docs / "requirements" / "stakeholder-needs.toml", spine_carrier.NEED_CARRIERS
    )
    sn_ids, sn_draft = set(), set()
    if sn_md is not None:
        text = sn_md.read_text(encoding="utf-8-sig", errors="replace")
        sn_ids = sn_all_ids(text)
        sn_draft = sn_draft_ids(text)

    # THE TWO OFF-SPINE REGISTRIES THE LADDER'S INSERTED RUNGS READ (OI-21). Both
    # are resolved through the carrier and both are APPLIES-WHEN: `have_*` is the
    # file's existence, and a project that adopts neither registry simply never
    # sits at DevStg-Boundary or DevStg-Arch. They feed the STAGE axis only —
    # `_raw_level` is untouched, so the runnable bar is computed from exactly the
    # rows it always was.
    ext_path = spine_carrier.resolve(
        docs / "requirements" / "external.toml", spine_carrier.CARRIERS
    )
    cmp_path = spine_carrier.resolve(
        docs / "requirements" / "components.toml", spine_carrier.CARRIERS
    )
    bifs = (
        [
            r
            for r in spine_carrier.load(docs / "requirements" / "external.toml", "B-ID")
            if r.get("B-ID") and not is_example(r["B-ID"])
        ]
        if ext_path is not None
        else []
    )
    cmps = (
        [
            r
            for r in spine_carrier.load(
                docs / "requirements" / "components.toml", "CMP-ID"
            )
            if r.get("CMP-ID") and not is_example(r["CMP-ID"])
        ]
        if cmp_path is not None
        else []
    )
    return {
        "srs": srs,
        "llrs": llrs,
        "tcs": tcs,
        "sn_ids": sn_ids,
        "sn_draft": sn_draft,
        "bifs": bifs,
        "cmps": cmps,
        "have_bifs": ext_path is not None,
        "have_cmps": cmp_path is not None,
    }


def compute(docs):
    """Derive the gate from the spine registries under `docs`. Returns a result
    dict: counts, the raw computed level (may be DevStg-Below), the same level recomputed
    with the drafts removed (`ex_draft`), the per-phase breakdown, and the
    runnable bar name (raw floored to DevStg-Reqs)."""
    spine = load_spine(docs)
    srs, llrs, tcs = spine["srs"], spine["llrs"], spine["tcs"]
    sn_ids, sn_draft = spine["sn_ids"], spine["sn_draft"]

    raw, sr_g = _raw_level(srs, llrs, tcs, sn_ids, sn_draft)

    n_draft = (
        sum(1 for r in srs if is_drafted(r))
        + sum(1 for r in llrs if is_drafted(r))
        + sum(1 for r in tcs if is_drafted(r))
        + len(sn_draft)
    )
    # `modified=` IS GONE AT D-9 STEP 7, deleted with `is_modified` and the word
    # it counted: no cell records a landed-but-unblessed amendment any more, and
    # the successor state is a property of two FILES, uncountable from the rows
    # this function is handed. `check._BASIS_RE` was re-read in the SAME commit
    # and still HONOURS the field when a gate file carries one, so a downstream
    # repo mid-migration keeps its window detector. A `drifted=N` successor is
    # designed (baseline-snapshot design §F4) and NOT built: it needs an import
    # edge from here into `baseline_snapshot`, which imports THIS module.
    #
    # `planned=` IS GONE AT D-9 STEP 5, deleted with `is_planned` and the word
    # itself (OI-30 D1 folded `Planned` into `Approved`). It was step-2 insurance
    # for a value 14 live rows carried while every counter here read past it;
    # once the value is `Approved` the count would be "how many rows are fine",
    # which is not a pending state and does not belong on a pending-state line.
    # `check._BASIS_RE` moved in the SAME commit — see `basis_line`.
    # Ratified SNs no SR answers (WI-401): normally the count behind the coverage
    # rung's DevStg-Below cap, surfaced on the basis line so a computed=DevStg-Below
    # with drafted=0 names its cause. Not always a cap: with zero real SRs the
    # vacuous-lowest-bar branch
    # in _raw_level returns before the rung runs, so the count can be nonzero
    # with nothing capped — the requirements-drafting corner, deliberately
    # visible. Counted over ALL SRs' citations (Drafted included) — the same set
    # trace.py's "SN has no SR" orphan rule reads, so the itemized listing and
    # this count never disagree on one registry state. Drafted SNs are exempt
    # (they ride the draft rung + drafted=N instead — one fact, one finding).
    cited = sn_cited_ids(srs)
    n_uncovered = sum(1 for u in sn_ids if u not in sn_draft and u not in cited)

    # The same arithmetic with the DRAFT rows taken out — "what would the gate be
    # if nothing were pending?" (WI-341). A Drafted row reads DevStg-Below, so it drops the repo's
    # min AND its own phase's, which erases the only evidence a consumer had that
    # this spine had ever climbed: in a single-phase repo the whole per-phase
    # breakdown goes to DevStg-Below and a mature repo reopening is indistinguishable
    # from a project that has never ratified anything (128-REVIEW-A MAJOR 3).
    # Excluding the drafts recovers it WITHOUT history or a stored high-water:
    # the rows the draft did not touch are still standing right here, and if they
    # all read DevStg-Tests/DevStg-Impl then the drafts are the only thing holding it.
    ex_draft, _ = _raw_level(
        [r for r in srs if not is_drafted(r)],
        [r for r in llrs if not is_drafted(r)],
        [r for r in tcs if not is_drafted(r)],
        sn_ids - sn_draft,
        set(),
    )

    per_phase = _per_phase(srs, sr_g, llrs, tcs)

    # Derived current phase: the highest phase number any RATIFIED (non-draft) spine
    # row carries, digit-parsed — the phase analogue of the derived gate (a scope
    # change surfaces as a phase bump). None when nothing is phased yet (a fresh or
    # all-blank downstream registry), so a non-adopter reads `phase=(none)`.
    phase_nums = [phase_num(r) for r in (srs + llrs + tcs) if not is_drafted(r)]
    phase_nums = [p for p in phase_nums if p is not None]
    cur_phase = max(phase_nums) if phase_nums else None

    stage = spine_stage(
        srs,
        llrs,
        tcs,
        sn_ids,
        sn_draft,
        bifs=spine["bifs"],
        cmps=spine["cmps"],
        have_bifs=spine["have_bifs"],
        have_cmps=spine["have_cmps"],
    )
    return {
        "counts": {"SN": len(sn_ids), "SR": len(srs), "LLR": len(llrs), "TC": len(tcs)},
        # SN-029's second axis, derived from the same rows (never from the bar).
        "stage": stage,
        "stage_ord": stage_ord(stage),
        "stage_of": STAGE_OF,
        "drafted": n_draft,
        "uncovered": n_uncovered,
        "raw": raw,
        "ex_draft": ex_draft,
        "per_phase": per_phase,
        "phase": cur_phase,
        # the runnable value (floored to the lowest runnable bar)
        "gate": BAR_NAMES[max(BAR_REQS, raw)],
    }


def _per_phase(srs, sr_g, llrs, tcs):
    """`{phase-label: bar-name}` — the SRs grouped by their optional `Phase` column
    (blank => "(default)"), each phase's bar the **raw** min over its SRs and the
    LLR/TC that decompose/verify them (NOT floored to `DevStg-Reqs`, unlike the
    runnable repo value): a phase carrying a draft reads `DevStg-Below`, so
    check_trajectory's phase-drop detector (WI-093) can see a phase fall below the
    level its own closed phase anchor recorded. The phase archetype + the drop
    warning live in check_trajectory."""
    llr_by_sr = {}
    llr_srs = {}
    for r in llrs:
        for s in refs(r.get("SR-Refs")):
            llr_by_sr.setdefault(s, []).append(maturity_bar(r))
            llr_srs.setdefault(r.get("LLR-ID") or "", []).append(s)
    # A TC that cites only its LLR (a legal shape the orphan rules accept) must
    # still land in its SR's phase bucket, or a Drafted TC in that shape drops the
    # repo's raw min while every per-phase entry stays green — the phase-drop
    # detector then points at nothing. Resolve LLR refs to their SR(s); direct
    # SR refs pass through.
    tc_by_ref = {}
    for r in tcs:
        for ref in refs(r.get("Verifies")):
            for s in llr_srs.get(ref, [ref]):
                tc_by_ref.setdefault(s, []).append(maturity_bar(r))

    phases = {}
    for r in srs:
        label = (r.get("Phase") or "").strip() or "(default)"
        sid = r["SR-ID"]
        bars = [sr_g[sid]] + llr_by_sr.get(sid, []) + tc_by_ref.get(sid, [])
        phases.setdefault(label, []).extend(bars)
    return {
        label: BAR_NAMES[min(gs)] if gs else BAR_NAMES[BAR_REQS]
        for label, gs in sorted(phases.items())
    }


def _git(root, args):
    """`git -C root <args>` stdout on success, else None (git absent / not a repo)."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(root)] + args,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, ValueError):
        return None
    return proc.stdout.strip() if proc.returncode == 0 else None


def basis_line(result):
    """The single, deterministic `# basis:` comment line compared by --check
    (the counts + raw computed level + the drafts-removed level + per-phase
    breakdown — everything that must stay in step with the states, excluding the
    volatile compute date).

    `ex-draft=` (WI-341), `uncovered=` (WI-401) and `stage=` (SN-029) are
    additive: a reader that does not know a field is unaffected, and check.py
    falls back to the older per-phase heuristic when `ex-draft` is absent, so a
    gate file written by an earlier derive_gate keeps working until it is next
    regenerated. Regenerating IS required — `--check` compares this line whole,
    so any new field is a cache-format change a downstream repo passes through
    by rerunning derive_gate once — the ordinary regenerate-a-generated-artifact
    step.

    THE OI-21 LADDER CONVERSION IS FIELD-COMPATIBLE, not value-compatible — the
    same precedent the 2026-08-12 rung insert set, applied deliberately this time.
    Every field keeps its name and position; the VALUES move to the new closed
    vocabularies (`computed=`/`ex-draft=`/`per-phase=` now carry `DevStg-*`,
    `stage=` now carries `DevStg-<Label>`), and two DERIVED companions join it:
    `stage-ord=` and `stage-of=`, so a raw-file reader gets the position without
    the identifier carrying it. `--check` reports the line as stale on the first
    recompute, so the retired vocabulary cannot persist past one regeneration.
    There is deliberately NO COMPAT SHIM: a reader that silently accepted both
    vocabularies is exactly how the retired tags would grow back.

    D-9 STEP 5 RENAMED `drafts=` TO `drafted=` AND DELETED `planned=`, and STEP 7
    DELETED `modified=` — field renames and field REMOVALS on a line whose
    consumers are named below, each done in the same commit as
    `check._BASIS_RE`, the window-detector fixtures and this repo's own
    `docs/gate`, because that is exactly the edit the twelve-commit precedent
    punished.

    THIS LINE HAS A MACHINE CONSUMER AND IT IS NOT `--check`: `check._BASIS_RE`
    parses `drafted=` (and `modified=`, when a file carries one) out of it to
    decide whether an open ratification WINDOW is suppressing the bar — and when
    that detector goes blind, twelve gate steps stop running silently (the
    measured 2026-07-26/27 precedent at `check.py`'s `window_open`). So a field
    may be inserted here only with that regex re-read in the SAME commit;
    `tests/test_derive_gate.py`'s producer-consumer round-trip pin
    (`check._BASIS_RE.search(derive_gate.basis_line(result))`) is what makes a
    future edit that breaks it fail loudly instead of quietly.

    THE STEP-7 REMOVAL WAS NOT SYMMETRIC WITH THE REGEX EDIT, deliberately: this
    producer stopped EMITTING `modified=` (the value cannot exist under the closed
    enum) while `check._BASIS_RE` kept HONOURING it as an optional group, because
    gate files this kit did not produce still carry one. Dropping the consumer
    half too would have disarmed the window detector's one conclusive arm for
    exactly those repos — the failure this docstring exists to prevent.
    """
    c = result["counts"]
    per_phase = ";".join(f"{k}={v}" for k, v in result["per_phase"].items())
    return (
        "# basis: SN={SN} SR={SR} LLR={LLR} TC={TC} drafted={d} "
        "uncovered={u} computed={raw} ex-draft={ed} phase={ph} "
        "per-phase={pp} stage={st} stage-ord={so} stage-of={sof}".format(
            SN=c["SN"],
            SR=c["SR"],
            LLR=c["LLR"],
            TC=c["TC"],
            d=result["drafted"],
            u=result["uncovered"],
            raw=BAR_NAMES[result["raw"]],
            ed=BAR_NAMES[result["ex_draft"]],
            ph=result["phase"] if result["phase"] is not None else "(none)",
            pp=per_phase or "(none)",
            st=result["stage"],
            so=result["stage_ord"],
            sof=result["stage_of"],
        )
    )


HEADER = [
    "# DERIVED BAR — generated by scripts/derive_gate.py (do not hand-edit).",
    "#",
    '# WHAT THIS VALUE IS. NOT "the rung the repo is at": a repo is IN a stage',
    '# and CLEARS a bar (process.md section 4, "The stage ladder"; the model:',
    "# docs/archive/specs/derived-gate-model.2026-07-20.md). The value on the last",
    "# line is the bar that must next be CLEARED — and therefore the STRICTNESS",
    "# SELECTOR check.py runs at. It is COMPUTED, not declared: the MIN over every",
    "# in-scope SN/SR/LLR/TC's own bar, floored to DevStg-Reqs. So the least-mature",
    "# row picks it, and a Drafted row DROPS it (the signal that a new",
    "# phase is due) — which means a mature spine held down by one draft displays",
    "# exactly what a fresh scaffold displays. The `# basis:` line below is what",
    "# tells them apart: `stage=` is the rung actually in work on the eight-rung",
    "# ladder (Needs, Boundary, Reqs, Arch, LLReqs, Tests, Impl, Release — with",
    "# `stage-ord=`/`stage-of=` carrying its DERIVED position), `ex-draft=` is the",
    "# value the same arithmetic gives with the pending rows removed, and",
    "# `computed=` is the raw level before the DevStg-Reqs floor (`DevStg-Below`",
    "# there is the internal below-the-lowest-bar sentinel, not a bar).",
    "#",
    "# HOW IT MOVES. By APPROVING artifacts in a reviewed commit",
    "# (Drafted->Approved — process.md section 4), never by editing this line.",
    "# An APPROVED row whose text is later amended does not move this value at",
    "# all: it is caught by comparing the row against its copy in",
    "# docs/archive/last_approved/, and it surfaces on the re-attest brief.",
    "# Regenerate: python scripts/derive_gate.py",
    "# Freshness is guarded by `--check` (a pre-commit + bar step). check.py / CI",
    "# read the first non-comment line below, exactly as before.",
    "#",
]


def render_cache(result, as_of, date):
    """The full docs/gate file text: static header, the compared `# basis:` line,
    the informational (never-compared) compute stamp, then the runnable gate."""
    lines = list(HEADER)
    lines.append(basis_line(result))
    lines.append("# computed {} (as-of {})".format(date, as_of))
    lines.append(result["gate"])
    return "\n".join(lines) + "\n"


def parse_cache(text):
    """`(gate_value, basis_line)` from a cached docs/gate: the first non-comment
    line, and the `# basis:` comment. Either may be None (a legacy hand-set gate
    file has no basis line — --check then reports it as needing the first compute)."""
    gate, basis = None, None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("# basis:"):
            basis = s
        elif s and not s.startswith("#") and gate is None:
            gate = s
    return gate, basis


# Implements: SR-049, LLR-148
def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    ap.add_argument(
        "--docs", default=None, help="docs directory (default: <root>/docs)"
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="recompute and compare to the cached docs/gate; exit 1 on drift "
        "(the gate value or the basis moved but the cache did not)",
    )
    ap.add_argument(
        "--print",
        dest="print_only",
        action="store_true",
        help="compute and print the derived gate + basis; do not write docs/gate",
    )
    ap.add_argument(
        "--next-phase",
        dest="next_phase",
        action="store_true",
        help="print the next delivery phase number — max(Phase over non-draft "
        "spine rows) + 1, the basis line's phase=N plus one; an unphased spine "
        "is the implicit foundation (1), so it prints 2. Output mode only: "
        "docs/gate is not written",
    )
    args = ap.parse_args()
    root = Path(args.root)
    docs = Path(args.docs) if args.docs else root / "docs"

    result = compute(docs)
    basis = basis_line(result)

    if args.next_phase:
        # The one derived answer to "a confirmed scope change opens a new phase
        # — what number does it take?" (owner ruling 2026-08-01, WI-402: a phase
        # increments on an adjudication-confirmed scope change or a ratified
        # draft-SN batch, NEVER on the raw derived-gate drop — a spurious
        # Modified window must not burn a phase number). Printed bare so the
        # intake mint helper (WI-388) can int() the output. Reuses the basis
        # line's phase=N derivation — an output mode, not a second parse; a
        # Drafted row's phase is not yet scope, so it never bumps the answer.
        cur = result["phase"]
        print((cur if cur is not None else 1) + 1)
        return 0

    if args.print_only:
        print(basis)
        print("derived gate: {}".format(result["gate"]))
        return 0

    gate_path = root / GATE_FILE
    if args.check:
        if not gate_path.exists():
            print(
                "derive_gate: {} is absent — run `python scripts/derive_gate.py` "
                "to generate it".format(GATE_FILE),
                file=sys.stderr,
            )
            return 1
        cached_gate, cached_basis = parse_cache(
            gate_path.read_text(encoding="utf-8", errors="replace")
        )
        # A legacy, hand-set docs/gate has no `# basis:` line (pre-migration). Then
        # --check compares only the VALUE (so the meta + fresh scaffolds stay green
        # until the one-time migration runs derive_gate); a value mismatch is still
        # a hard fail. Once migrated (basis present), the full rot guard applies.
        if cached_basis is None:
            if cached_gate == result["gate"]:
                print(
                    "derive_gate: {} value OK ({}) but not yet in derived form — run "
                    "`python scripts/derive_gate.py` once to migrate.".format(
                        GATE_FILE, result["gate"]
                    ),
                    file=sys.stderr,
                )
                return 0
            print(
                "derive_gate: {} STALE — hand-set {} but the derived gate is {}.\n"
                "  run `python scripts/derive_gate.py` and commit the result.".format(
                    GATE_FILE, cached_gate, result["gate"]
                ),
                file=sys.stderr,
            )
            return 1
        if cached_gate == result["gate"] and cached_basis == basis:
            print("derive_gate: {} up to date ({}).".format(GATE_FILE, result["gate"]))
            return 0
        print(
            "derive_gate: {} STALE — the derived gate moved but the cache did not.\n"
            "  cached: gate={} basis={!r}\n"
            "  now:    gate={} basis={!r}\n"
            "  run `python scripts/derive_gate.py` and commit the result.".format(
                GATE_FILE, cached_gate, cached_basis, result["gate"], basis
            ),
            file=sys.stderr,
        )
        return 1

    as_of = _git(root, ["rev-parse", "--short", "HEAD"]) or "no-git"
    date = (
        _git(root, ["log", "-1", "--format=%cs"]) or datetime.date.today().isoformat()
    )
    gate_path.parent.mkdir(parents=True, exist_ok=True)
    gate_path.write_text(
        render_cache(result, as_of, date), encoding="utf-8", newline="\n"
    )
    print("derive_gate: wrote {} -> {} ({}).".format(GATE_FILE, result["gate"], basis))
    return 0


if __name__ == "__main__":
    sys.exit(main())
