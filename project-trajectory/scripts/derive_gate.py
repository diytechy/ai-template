#!/usr/bin/env python3
"""Derive the active gate from artifact states — the hybrid, cached gate.

Stack-agnostic, standard-library only. This replaces the hand-set `docs/gate`
marker with one *computed* from the spine's own maturity states
(docs/specs/derived-gate-model.md): **the repo is at gate G iff every in-scope
SN/SR/LLR/TC meets G's bar.** SSOT applied to the gate itself — you no longer bump
a line, you ratify artifacts (in a reviewed commit) and the gate follows.

The model is **hybrid**: the computed value is *cached* to `docs/gate` (now a
generated file) with a compute date, so the gate is known on checkout with no
recompute; `--check` recomputes and guards the cache against rot, the same
freshness discipline the kit already runs for the arch-map / OKF / dashboard.
`check.py`'s `resolve_gate()` still reads the first non-comment line of
`docs/gate` — the value is simply derived now, not declared.

Per-artifact gate (docs/specs/derived-gate-model.md §3), on the ladder
G0 < G1 < G2 < G3:
  - **SN** — Draft (under a stakeholder-needs.md heading containing "draft",
    section-as-state §4a) => G0; ratified AND cited by >=1 SR `SN-Refs` => it has
    no obligation past G1, so it never caps the repo (contributes G3 to the min);
    ratified but cited by NO SR (WI-401) => G0 — a ratified-but-unanswered need
    means G1 is not earned. The `uncovered=N` basis count surfaces the cause
    beside `drafts=N`/`modified=N` (a Draft SN is exempt from the coverage rung —
    it already reads G0 via the draft rung, one fact one rung; the itemized
    "SN has no SR" listing stays trace.py's orphan finding at G2 strictness,
    this rung being the gate-input half of that same split).
  - **SR** — Draft (Status) => G0; ratified but not decomposed => G1; decomposed
    (has its required LLR — unless the Verification is LLR-exempt
    Analysis/Inspection/Attest — AND a TC) => G2; decomposed AND Status=Verified
    => G3. A `Modified` SR (post-attestation amendment, WI-316) needs no rule of
    its own: it is decomposed-but-not-Verified, so it reads G2 — the deliberate
    gate pull that makes a pending re-attest visible. The `modified=N` basis
    count surfaces it beside `drafts=N`.
  - **LLR / TC** — Draft => G0 (the new-phase signal). Once present, its Status
    does not independently gate: the SR's Verified status drives G2->G3 (matching
    trace.py's --require-verified, which checks SRs, not LLR/TC status), so a
    present LLR/TC never caps below G3.

Aggregation: the repo gate = **min over all in-scope artifacts** (a phase gate is
the min over that phase's artifacts; the repo gate is the min over phases, which
is the same set — also reported per-phase). A repo with **no** real SRs yet (a
fresh scaffold) is at **G1** (the requirements-drafting start), never a vacuous
G3. A draft artifact is at G0, so introducing draft/reopened content **drops** the
derived gate — the signal that a new phase is due (the `[phase]-[g*]` detector
lives in check_trajectory). The cached runnable value is floored at G1 (check.py's
gate vocabulary is G1..G3); the raw computed level, including a G0 drop, is
recorded in the `# basis:` comment so nothing hides.

This script reads STATES and picks the LEVEL; `trace.py` (run by check.py at that
level) ENFORCES the structure — orphans/decomposition/verified — at the derived
gate. The two compose: a draft is exempt from trace's orphan rule (so it can live
in the live spine) yet sits at G0 here (so it drops the gate). Auditing
correctness is the whole point, so every rule is fixture-tested.

Note: the derived range is G1..G3 (the SN/SR/LLR/TC-derivable gates). G-Release /
G-Final are release milestones beyond the spine and stay separately recorded.

Usage:
    python scripts/derive_gate.py [--root .] [--docs DIR]   # compute + write docs/gate
    python scripts/derive_gate.py --check                    # recompute + guard rot (exit 1 on drift)
    python scripts/derive_gate.py --print                    # compute + print, do not write

Small CSV/heading loaders below are duplicated from trace.py per the kit's
independently-copyable-script convention (the F5 rule) — derive_gate.py stays a
self-contained drop-in, never importing the joined-spine engine.

Contracts: IF-050, IF-051 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
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

# The derived ladder. G0 = pre-ratification (draft); G1..G3 are the runnable gates
# check.py knows. GATE_NAMES maps the internal int back to the marker string.
G0, G1, G2, G3 = 0, 1, 2, 3
GATE_NAMES = {G0: "G0", G1: "G1", G2: "G2", G3: "G3"}

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


def is_draft(row):
    """A row in the pre-ratification `Draft` state (open-vocab Status)."""
    return (row.get("Status") or "").strip().lower() == "draft"


def is_verified(row):
    """The terminal `Verified` state, matched case-insensitively — the SAME rule as
    is_draft (the one Status-casing rule, process.md §4). Duplicated from trace.py
    per the F5 rule; pinned equal by test_rule_sync."""
    return (row.get("Status") or "").strip().lower() == "verified"


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
    uncited prose mention caps the gate at G0 via the coverage rung). `-000`
    excluded. Duplicated from trace.py per the F5 rule; pinned equal by
    test_rule_sync (WI-408) — a divergence here would let the gate and trace's
    itemized listing disagree about which ids the rules run over."""
    return {u for u in re.findall(r"\bSN-\d+\b", text) if not is_example(u)}


def sn_draft_ids(text):
    """The set of Draft SN ids in a needs registry's `text`, through whichever
    CARRIER wrote it.

    Under TOML draft-ness is a FIELD on the need (`kind = "draft"`); under the
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
    by the caller's row filter, and a Draft SR's citation is deliberately in the
    set (the raw view matches trace.py's orphan exemption; the ex-draft
    counterfactual re-runs this on the non-draft subset instead). Duplicated in
    trace.py per the F5 rule; pinned equal by test_rule_sync."""
    return {x for r in srs for x in refs(r.get("SN-Refs"))}


# --- per-artifact gate rules (docs/specs/derived-gate-model.md §3) -------------
def sr_gate(sr, has_llr, has_tc):
    """The gate an SR row has reached, from its Status + whether it is decomposed."""
    if is_draft(sr):
        return G0
    exempt = llr_exempt(sr)
    decomposed = (exempt or has_llr) and has_tc
    verified = is_verified(sr)
    if decomposed and verified:
        return G3
    if decomposed:
        return G2
    return G1  # a ratified requirement not yet decomposed


def maturity_gate(row):
    """An LLR/TC caps the gate only when it is Draft (G0 — the new-phase signal).
    Once present, its own Status does NOT independently gate G3: the SR's Verified
    status drives G2->G3 (matching trace.py's --require-verified bar, which checks
    SRs, not LLR/TC status), and the LLR/TC's *existence* is what makes its SR
    decomposed (G2, decided in sr_gate). So a present LLR/TC contributes G3 and
    never caps — a downstream repo whose LLRs read `Implemented` still reaches G3
    on its SRs, exactly as trace.py's gate does."""
    return G0 if is_draft(row) else G3


def is_modified(row):
    """The post-attestation `Modified` state (WI-316, process.md §7): content
    changed after the last attestation, re-attest owed. NO gate arithmetic of its
    own — a Modified SR is simply not Verified, so sr_gate already derives G2
    (decomposed-unverified); recognized here only for the `modified=N` basis
    count, so the pending state never hides. Duplicated from trace.py per the F5
    no-shared-module rule; pinned equal by test_rule_sync."""
    return (row.get("Status") or "").strip().lower() == "modified"


def sn_gate(sn_id, draft_ids, cited_ids):
    """A Draft SN (section-as-state) is G0 — and that is the ONLY rung that fires
    on a draft: it is exempt from the coverage rung below exactly as it is exempt
    from trace.py's orphan rule, so one fact never fires two findings at once.
    A RATIFIED SN must be cited by >=1 SR's `SN-Refs` (WI-401, owner ruling
    2026-08-01): ratified-but-uncovered caps the raw level at G0, because a
    ratified need no SR answers has not earned G1. This rung is the GATE INPUT;
    the itemized "SN {id} has no SR" listing stays trace.py's orphan finding at
    G2 strictness — the same states-here/structure-there split the module
    docstring describes. A covered ratified SN has no obligation past G1 and
    never caps the repo (contributes G3 to the min)."""
    if sn_id in draft_ids:
        return G0
    return G3 if sn_id in cited_ids else G0


# --- SN-029: the SECOND derived axis --------------------------------------------
# WHY TWO AXES. The gate answers "how strict is the harness right now" — its
# vocabulary is `G1|G2|G3` and `check.py` selects steps from it. The human
# ratification level answers a different question: "how far up the spine is a
# HUMAN still the acceptor". Those are not the same ladder, and G-numbering
# cannot express the second: G2 conflates "LLRs and TCs exist" AND doubles as
# the pull a `Modified` row applies, so there is no G that means "TCs are in
# process". Forcing one axis to carry both is how a dial ends up meaning
# something subtly different at each of its five reading sites.
#
# So `spine_stage` is derived SEPARATELY, on its own 0-4 ladder, and
# `stage_to_gate` is the declared mapping between them — one auditable place
# rather than an arithmetic coincidence. The runnable gate value is untouched;
# the stage rides the `# basis:` line as an appended field.
STAGE_SN, STAGE_SR, STAGE_LLR, STAGE_TC, STAGE_DONE = 0, 1, 2, 3, 4


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


def spine_stage(srs, llrs, tcs, sn_ids, sn_draft):
    """The tier currently IN PROCESS, 0-4 — the axis a human-ratification level
    is compared against.

      0  SNs in process: a need is a draft, none is ratified, or a ratified one
         has no SR answering it
      1  SNs settled, SRs in process: a requirement is Draft, or one is
         `Modified` (amended after attestation, so its RE-ratification is owed)
      2  ...and the LLRs are in process: one is missing or Draft
      3  ...and the TCs are in process: one is missing or Draft
      4  nothing in process: every tier is decomposed and Verified

    Read as the LOWEST unfinished tier — the one work is happening at, and
    therefore the one a human boundary has to be compared against.

    WHICH TIER OWNS A MISSING ARTIFACT: the tier the artifact belongs to, not
    its parent. An SR with no LLR yet puts the spine at stage 2, because what is
    being written is an LLR. Reading it as stage 1 (the older shape) made stages
    2 and 3 unreachable during exactly the period they describe — every SR had
    to be fully decomposed before a Draft child could be seen at all — which
    left the axis unable to express "TCs are human-held but LLRs are not", the
    distinction the axis exists for.

    WHICH TIER OWNS AN UNVERIFIED SR: `Modified` is the SR's own tier and is
    checked FIRST, because it means the requirement's text moved after it was
    attested and a fresh ratification is owed on the SR itself. Any OTHER
    not-yet-Verified SR is checked LAST, after the children: an SR reaches
    Verified only once its LLRs and TCs are green, so while a child is still in
    flight the child's tier is the honest answer.

    Two corners are explicit. A repo with no real SRs at all is stage 0, NOT
    stage 4 — the vacuous-G1 short circuit in `_raw_level` exists for the gate's
    own arithmetic and would read as "everything is finished" here, which is
    precisely backwards. And a RATIFIED-BUT-UNCITED SN is stage 0, applying
    WI-401's coverage rung on the same subset `_raw_level` uses: a need with no
    requirement answering it is unfinished work at the SN tier, and without this
    such a spine read stage 4 while the gate arithmetic put it at G0."""
    if any(u in sn_draft for u in sn_ids) or not sn_ids:
        return STAGE_SN
    if not srs:
        return STAGE_SN
    if any(is_draft(r) for r in srs):
        return STAGE_SR
    if any(u not in sn_cited_ids(srs) for u in sn_ids):
        return STAGE_SN
    if any(is_modified(r) for r in srs):
        return STAGE_SR
    llr_sr_refs, tc_refs = _decomposed_sr_ids(llrs, tcs)
    if any(
        not llr_exempt(sr) and sr.get("SR-ID") not in llr_sr_refs for sr in srs
    ) or any(is_draft(r) for r in llrs):
        return STAGE_LLR
    if any(sr.get("SR-ID") not in tc_refs for sr in srs) or any(
        is_draft(r) for r in tcs
    ):
        return STAGE_TC
    if not all(is_verified(r) for r in srs):
        return STAGE_TC
    return STAGE_DONE


def stage_to_gate(stage):
    """THE DECLARED MAPPING between the two axes — stated once, here, so the
    reconciliation is auditable instead of implied.

    It is deliberately LOSSY in one direction only: several stages map to one
    gate (0 and 1 both read G1, because the harness has the same strictness
    while requirements are being drafted whether or not the needs are settled),
    and no stage maps to a gate the harness does not know. Nothing derives the
    gate FROM the stage in production — `compute` still computes the gate from
    the artifact states exactly as it always did — so this is a reader's
    reconciliation, not a second source of truth."""
    if stage >= STAGE_DONE:
        return "G3"
    if stage >= STAGE_LLR:
        return "G2"
    return "G1"


def _raw_level(srs, llrs, tcs, sn_ids, sn_draft):
    """`(raw_level, sr_gates)` over ONE set of spine rows.

    The raw level is the min over every in-scope artifact's gate (SN drafts, SR
    maturity, LLR/TC maturity — including WI-401's SN-coverage rung, whose cited
    set is built from THIS call's `srs`); a set with no real SRs is G1
    (requirements-drafting), never a vacuous G3 from ratified-SN-only. Taken as
    a function of its rows rather than of `docs` so `compute` can ask it the
    counterfactual question too — the same arithmetic, over the non-draft
    subset (`ex-draft`), which is what tells a mature spine held down by drafts
    apart from an early one (WI-341). The coverage rung rides that subset
    consistently: a citation on a removed Draft SR leaves with its row, so the
    counterfactual never fabricates coverage a ratified spine does not have.
    """
    llr_sr_refs, tc_refs = _decomposed_sr_ids(llrs, tcs)
    cited = sn_cited_ids(srs)
    sr_g = {
        r["SR-ID"]: sr_gate(r, r["SR-ID"] in llr_sr_refs, r["SR-ID"] in tc_refs)
        for r in srs
    }
    if not srs:
        return G1, sr_g
    raw = min(
        [sr_g[k] for k in sr_g]
        + [sn_gate(u, sn_draft, cited) for u in sn_ids]
        + [maturity_gate(r) for r in llrs]
        + [maturity_gate(r) for r in tcs]
    )
    return raw, sr_g


def compute(docs):
    """Derive the gate from the spine registries under `docs`. Returns a result
    dict: counts, the raw computed level (may be G0), the same level recomputed
    with the drafts removed (`ex_draft`), the per-phase breakdown, and the
    runnable gate name (raw floored to G1)."""
    # The three spine tiers read through the CARRIER, which
    # resolves TOML or CSV and hands back rows under today's column names — so
    # the gate derivation below is untouched by the migration. `load_csv` stays
    # for the off-spine registries, which do not move.
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
    # the kit where a literal suffix here would be worst: an existence test on
    # `.toml` alone answers False for a repo still on markdown, `sn_ids` and
    # `sn_draft` both come back EMPTY, and an empty draft set makes every draft
    # need read as ratified — the derived gate RISES on a registry the reader
    # simply could not find. Absent must mean absent, never "no drafts".
    sn_md = spine_carrier.resolve(
        docs / "requirements" / "stakeholder-needs.toml", spine_carrier.NEED_CARRIERS
    )
    sn_ids, sn_draft = set(), set()
    if sn_md is not None:
        text = sn_md.read_text(encoding="utf-8-sig", errors="replace")
        sn_ids = sn_all_ids(text)
        sn_draft = sn_draft_ids(text)

    raw, sr_g = _raw_level(srs, llrs, tcs, sn_ids, sn_draft)

    n_draft = (
        sum(1 for r in srs if is_draft(r))
        + sum(1 for r in llrs if is_draft(r))
        + sum(1 for r in tcs if is_draft(r))
        + len(sn_draft)
    )
    # `Modified` rows (WI-316): landed-but-unblessed amendments awaiting re-attest.
    # Counted across the three registries exactly like drafts (SNs have no Status
    # cell — a changed ratified SN rides its SR chain's Modified) and surfaced on
    # the basis line so the pending state never hides. No gate arithmetic here:
    # a Modified SR already computes G2 via sr_gate's decomposed-unverified rung.
    n_modified = (
        sum(1 for r in srs if is_modified(r))
        + sum(1 for r in llrs if is_modified(r))
        + sum(1 for r in tcs if is_modified(r))
    )
    # Ratified SNs no SR answers (WI-401): normally the count behind the coverage
    # rung's G0 cap, surfaced on the basis line so a computed=G0 with drafts=0
    # names its cause. Not always a cap: with zero real SRs the vacuous-G1 branch
    # in _raw_level returns before the rung runs, so the count can be nonzero
    # with nothing capped — the requirements-drafting corner, deliberately
    # visible. Counted over ALL SRs' citations (Draft included) — the same set
    # trace.py's "SN has no SR" orphan rule reads, so the itemized listing and
    # this count never disagree on one registry state. Draft SNs are exempt
    # (they ride the draft rung + drafts=N instead — one fact, one finding).
    cited = sn_cited_ids(srs)
    n_uncovered = sum(1 for u in sn_ids if u not in sn_draft and u not in cited)

    # The same arithmetic with the DRAFT rows taken out — "what would the gate be
    # if nothing were pending?" (WI-341). A Draft reads G0, so it drops the repo's
    # min AND its own phase's, which erases the only evidence a consumer had that
    # this spine had ever climbed: in a single-phase repo the whole per-phase
    # breakdown goes to G0 and a mature repo reopening becomes indistinguishable
    # from a project that has never ratified anything (128-REVIEW-A MAJOR 3).
    # Excluding the drafts recovers it WITHOUT history or a stored high-water:
    # the rows the draft did not touch are still standing right here, and if they
    # all read G2/G3 then the drafts are the only thing holding the gate down.
    ex_draft, _ = _raw_level(
        [r for r in srs if not is_draft(r)],
        [r for r in llrs if not is_draft(r)],
        [r for r in tcs if not is_draft(r)],
        sn_ids - sn_draft,
        set(),
    )

    per_phase = _per_phase(srs, sr_g, llrs, tcs)

    # Derived current phase: the highest phase number any RATIFIED (non-draft) spine
    # row carries, digit-parsed — the phase analogue of the derived gate (a scope
    # change surfaces as a phase bump). None when nothing is phased yet (a fresh or
    # all-blank downstream registry), so a non-adopter reads `phase=(none)`.
    phase_nums = [phase_num(r) for r in (srs + llrs + tcs) if not is_draft(r)]
    phase_nums = [p for p in phase_nums if p is not None]
    cur_phase = max(phase_nums) if phase_nums else None

    return {
        "counts": {"SN": len(sn_ids), "SR": len(srs), "LLR": len(llrs), "TC": len(tcs)},
        # SN-029's second axis, derived from the same rows (never from the gate).
        "stage": spine_stage(srs, llrs, tcs, sn_ids, sn_draft),
        "drafts": n_draft,
        "modified": n_modified,
        "uncovered": n_uncovered,
        "raw": raw,
        "ex_draft": ex_draft,
        "per_phase": per_phase,
        "phase": cur_phase,
        "gate": GATE_NAMES[max(G1, raw)],  # the runnable value (floored to G1)
    }


def _per_phase(srs, sr_g, llrs, tcs):
    """`{phase-label: gate-name}` — the SRs grouped by their optional `Phase` column
    (blank => "(default)"), each phase's gate the **raw** min over its SRs and the
    LLR/TC that decompose/verify them (NOT floored to G1, unlike the runnable repo
    value): a phase carrying a draft reads `G0`, so check_trajectory's phase-drop
    detector (WI-093) can see a phase fall below its closed `[phase]-[g*]` level.
    The `[phase]-[g*]` archetype + the drop warning live in check_trajectory."""
    llr_by_sr = {}
    llr_srs = {}
    for r in llrs:
        for s in refs(r.get("SR-Refs")):
            llr_by_sr.setdefault(s, []).append(maturity_gate(r))
            llr_srs.setdefault(r.get("LLR-ID") or "", []).append(s)
    # A TC that cites only its LLR (a legal shape the orphan rules accept) must
    # still land in its SR's phase bucket, or a Draft TC in that shape drops the
    # repo's raw min while every per-phase entry stays green — the phase-drop
    # detector then points at nothing. Resolve LLR refs to their SR(s); direct
    # SR refs pass through.
    tc_by_ref = {}
    for r in tcs:
        for ref in refs(r.get("Verifies")):
            for s in llr_srs.get(ref, [ref]):
                tc_by_ref.setdefault(s, []).append(maturity_gate(r))

    phases = {}
    for r in srs:
        label = (r.get("Phase") or "").strip() or "(default)"
        sid = r["SR-ID"]
        gates = [sr_g[sid]] + llr_by_sr.get(sid, []) + tc_by_ref.get(sid, [])
        phases.setdefault(label, []).extend(gates)
    return {
        label: GATE_NAMES[min(gs)] if gs else GATE_NAMES[G1]
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

    `ex-draft=` (WI-341) and `uncovered=` (WI-401) are additive: a reader that
    does not know a field is unaffected, and check.py falls back to the older
    per-phase heuristic when `ex-draft` is absent, so a gate file written by an
    earlier derive_gate keeps working until it is next regenerated. Regenerating
    IS required — `--check` compares this line whole, so any new field is a
    cache-format change a downstream repo passes through by rerunning
    derive_gate once — the ordinary regenerate-a-generated-artifact step.
    """
    c = result["counts"]
    per_phase = ";".join(f"{k}={v}" for k, v in result["per_phase"].items())
    return (
        "# basis: SN={SN} SR={SR} LLR={LLR} TC={TC} drafts={d} modified={m} "
        "uncovered={u} computed={raw} ex-draft={ed} phase={ph} per-phase={pp} "
        "stage={st}".format(
            SN=c["SN"],
            SR=c["SR"],
            LLR=c["LLR"],
            TC=c["TC"],
            d=result["drafts"],
            m=result["modified"],
            u=result["uncovered"],
            raw=GATE_NAMES[result["raw"]],
            ed=GATE_NAMES[result["ex_draft"]],
            ph=result["phase"] if result["phase"] is not None else "(none)",
            pp=per_phase or "(none)",
            st=result["stage"],
        )
    )


HEADER = [
    "# DERIVED GATE — generated by scripts/derive_gate.py (do not hand-edit).",
    "#",
    "# The active gate is COMPUTED from artifact states, not declared",
    "# (docs/specs/derived-gate-model.md): the repo is at gate G iff every in-scope",
    "# SN/SR/LLR/TC meets G's bar. You advance it by RATIFYING artifacts in a",
    "# reviewed commit (Draft->Planned, or moving an SN out of a draft section;",
    "# a Modified row re-attests the same way, Modified->Verified — process.md",
    "# section 7), not by editing this line. Regenerate: python scripts/derive_gate.py",
    "# Freshness is guarded by `--check` (a pre-commit + gate step). check.py / CI",
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
        # Draft row's phase is not yet scope, so it never bumps the answer.
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
