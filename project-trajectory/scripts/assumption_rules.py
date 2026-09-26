"""THE ASSUMPTION TIER'S RULES — pure joins over the assumptions registry.

The sibling of `frame_rules.py`, and built the same way: every rule here is a
JOIN ACROSS ROWS, it reads no file, and `trace.analyze` composes it and stays
the only caller of its rules. `trace.py` is held to an exact size ratchet, so
the tier's rules land here and `trace.py` grows by the composition lines alone
(spine map D21). Two other readers take one derivation from here and no rule:
the stage derivation and the red-TC census read `da_citing_srs`, because an
assumption's citing requirements are what place and count its evidence.

What the tier records. A requirement states what the system does at its own
boundary and a stakeholder need what a person experiences; between them sits a
claim about the world, and a false one makes a fully verified system deliver
nothing. `docs/requirements/assumptions.toml` holds each such claim as a row of
its own (`[assumption.DA-###]`, SR-191): where its outcome lands, what it
assumes, when it holds, the obstacle under which it fails, its maturity and its
validity. Beside it sit the stand-ins that answer for an outside party in tests
(`[surrogate.SUR-###]`, SR-192); a stand-in is evidence only as far as it
matches the party it replaces, so an assumption naming it in `RealizedBy`
states that match, and lands on a crossing of a party it emulates.

Each requirement then cites the assumptions its argument relies on
(`DA-Refs`), or records in `Coincident` why its own specification alone
delivers its needs (SR-193), and declares its `Form` (SR-194). An assumption no
requirement cites, or with no falsifying signal, is reported (SR-196). The need
link stays on the requirement: an assumption's needs are derived from the
requirements citing it (`da_citing_srs`), and nothing records them on the
assumption.

EVIDENCE FOR AN ASSUMPTION IS A TEST CASE (SR-197): its `Assumption-Refs` name
the assumptions it evidences, in place of or beside what its `Verifies` names.
And many such tests are OBSERVATIONS (a person reading a render, a measurement
across an adopter's first week) that the harness cannot rerun. A test case
recorded as not automated declares the inputs its judgment reads, how many days
its result holds, and, evidencing an assumption, how it samples (SR-198), so a
changed input or an expired lifetime can make the result stale without anyone
re-judging it. Those declarations are judged here too; they apply to every
observation case, with or without a frame.

WHERE THE TIER APPLIES. An assumption's outcome lands on a boundary crossing,
so with no declared crossing there is nothing to land on and the whole tier is
silent (SR-191's applies-when). And the requirement-side reports ask nothing of
a project that has not adopted the tier: until the registry holds a real
assumption row, no requirement is asked for a citation or a form. Every
adopter is scaffolded the blank form, so the file existing is not adoption.
The two rules at the end of this module stand apart (IF-208) and wait for
neither: each boundary interface is asked whether assumptions bridge it or its
reading is the outcome (SR-211), and each assumption's obstacle perspectives
are resolved against the hats roster (SR-214), because neither requirement
states such a condition, and a pointer into nothing is wrong wherever it is
written.

Rows are the carrier's column-keyed dicts (`DA-ID`, `EffectAt`, `SUR-ID`,
`Emulates`, `SR-ID`, `DA-Refs`, `EXT-ID`, `B-ID`, `Entity`), exactly as
`trace.load_registries` hands them over; a list cell arrives `;`-joined. Every
function returns plain finding strings, and no function writes to a row it is
handed.

Stdlib only. A plain sibling of `scripts/`, not a `kitlib` module, for the
reason `coherence.py` records: these are the checker's rules, and the
scaffolder has no business importing them.

Contracts: IF-190, IF-200, IF-201, IF-208 — the seams this module declares
(process.md §8; rows of record in docs/requirements/interfaces.toml).

Contract IF-190: the assumption tier's rule surface `trace.py` imports. Rows in,
    findings out, and nothing else: no I/O, no git, no filesystem, no argv.
    `assumption_tier_findings(srs, das, surs, exts, bifs)` is the tier as the
    checker composes it and returns `(frame, integrity, advisories)`: the
    frame list joins the frame class and `trace.py --strict`'s exit code, the
    integrity list joins the always-on `--strict-integrity` floor, and the
    advisories ride the warn pipe and never join a failure set. It returns
    three empty lists when `bifs` declares no crossing, and asks no requirement
    for a form until `das` holds a real assumption row. The rules it composes
    are public and callable alone: `assumption_row_findings(das, bifs)` returns
    failures, `surrogate_findings(surs, das, exts, bifs)`,
    `sr_classification_advisories(srs, das)` and `sr_form_findings(srs)`
    return `(failures, advisories)`, and `uncited_assumption_advisories(das,
    srs)` and `no_falsifier_advisories(das)` return advisories. Two data reads
    ride the same seam: `da_citing_srs(srs)` maps each cited assumption id to
    the requirement ids citing it, and `classify_srs(srs, das)` maps each
    requirement id to one of `SR_CLASSES`. A row whose id ends `-000` is the
    template's example and is never judged.
    Two reach reports ride the same seam as advisories, composed by the checker
    beside the tier: `assumption_reach_advisories(das, srs, needs, stks, exts,
    bifs, surs)`, silent when `bifs` declares no crossing, and
    `need_frame_gap_advisories(needs, stks, srs, bifs, das)`, silent with no
    operation crossing or no agreed stakeholder. `needs` are
    `spine_carrier.load_needs`' rows. `reaching_parties(needs, stks, exts)` is
    their data read: each need id mapped to the set of entities a crossing
    must belong to in order to reach it.

Contract IF-200: the observation test declaration's rules `trace.py` imports.
    Rows in, findings out, with no I/O. `observation_tc_findings(tcs)` returns
    `(failures, advisories)`: the failures join the always-on
    `--strict-integrity` floor and the advisories ride the warn pipe, each
    naming its row. It applies whatever the frame declares. Two reads ride the
    same seam: `is_observation_tc(tc)`, true when the `Automated` cell reads
    No, and `sampling_model_declared(tc)`, true only for a sampled case whose
    sample size and acceptance rule are both valid. A `-000` row is never
    judged.
Contract IF-201: the one derivation of an assumption's citing requirements,
    `da_citing_srs(srs) -> {assumption id: [requirement ids]}` in row order,
    read by the stage derivation and the red-TC census. Pure over requirement
    rows in the carrier's column names; a `-000` row contributes nothing, and a
    requirement citing no assumption appears nowhere in the map.

Contract IF-208: the tier's two pointer rules that land in OTHER classes, which
    `trace.py` imports beside the tier entry point and composes itself. Rows in,
    findings out, on the same terms as IF-190. `interface_bridge_findings(ifs,
    das)` returns `(failures, advisories)` over boundary interfaces alone
    (a from- or to-external tie-back): the failures, a `BridgedBy` entry naming
    an undeclared assumption, join the interface class and `--strict`'s exit
    code; the advisories, a boundary interface with neither `BridgedBy` nor
    `Coincident`, ride the warn pipe. `obstacle_hat_findings(das, hat_names)`
    returns failures, each an `ObstacleHats` entry the roster names in
    `hat_names` do not hold, joining the dangling-hat class; an empty
    `hat_names` means no roster, so every named perspective fails. Neither
    waits for a declared crossing or a real assumption row.
"""

import re

try:
    from kitlib.spine import (
        FORM_VALUES,
        MAX_AGE_FLOOR_DAYS,
        SAMPLING_VALUES,
        STATUS_VALUES,
        is_example,
        refs,
    )
    from kitlib.spine import is_approved, is_founded
except ImportError:  # pragma: no cover - in-process fallback
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kitlib.spine import (
        FORM_VALUES,
        MAX_AGE_FLOOR_DAYS,
        SAMPLING_VALUES,
        STATUS_VALUES,
        is_example,
        refs,
    )
    from kitlib.spine import is_approved, is_founded

# THE ASSUMPTION ROW'S REQUIRED CELLS (SR-191), in the carrier's column names.
# `Falsifier` is deliberately absent: an assumption is often written before the
# signal that could show it false exists, so a missing one is reported by
# `no_falsifier_advisories` rather than failed here. `AcceptedRisk`,
# `RealizedBy` and `ObstacleHats` are optional by their own requirements.
# Implements: SR-191, LLR-219
DA_REQUIRED = ("EffectAt", "Assumption", "HoldsWhen", "Obstacle", "Status", "Standing")

# An assumption's VALIDITY, separate from its maturity: an approved assumption
# can later be shown false, and `Status` cannot say so without un-approving it.
# Implements: SR-191, LLR-219
STANDING_VALUES = ("active", "falsified")

# THE SURROGATE ROW'S REQUIRED CELLS (SR-192), in the carrier's column names.
# `Emulates` is a list, and an empty one counts as missing: a stand-in that
# answers for nobody is not a stand-in.
# Implements: SR-192, LLR-221
SUR_REQUIRED = ("Name", "Emulates", "Description", "Status")

# How a requirement relates to the assumptions under it (SR-193). `bridged`: it
# cites declared assumptions; `coincident`: its waiver says its own
# specification delivers its needs; `unclassified`: neither; `both`: a citation
# and a waiver at once, which contradict each other.
SR_CLASSES = ("bridged", "coincident", "unclassified", "both")

# AN OBSERVATION CASE'S DECLARATION CELLS (SR-198), in the carrier's column
# names: the cells an automated case has no use for, since the harness reruns
# it and nothing it produces goes stale by age.
OBSERVATION_CELLS = ("Inputs", "MaxAge", "Sampling", "SampleSize", "AcceptanceRule")

# A whole number of days or samples, written in digits: `7.5`, `seven` and `-3`
# are not. The carrier hands an integer cell over as its text.
_WHOLE = re.compile(r"[0-9]+")


def _cell(row, column):
    """One cell, stripped; `""` when the row does not carry it."""
    return (row.get(column) or "").strip()


def _real(rows, id_col):
    """`(id, row)` for each row that is not the template's `-000` example."""
    for row in rows:
        rid = _cell(row, id_col)
        if rid and not is_example(rid):
            yield rid, row


def _adopted(das):
    """Whether the registry holds a real assumption row: the one sign a project
    has adopted the tier, since every scaffold receives the blank form."""
    return next(_real(das, "DA-ID"), None) is not None


def _missing(row, required):
    """The required columns this row leaves empty, in the stated order. A list
    cell counts as empty when it names nothing, whitespace included."""
    return [c for c in required if not refs(row.get(c))]


def _assumption_row(did, row, crossings):
    """One assumption's own failures: each empty required cell, a status or a
    standing outside its vocabulary, a landing crossing the frame does not
    declare."""
    out = [
        "assumption {} has no {} — an assumption states where its outcome lands, "
        "what it assumes, when it holds, the obstacle under which it fails, its "
        "maturity and its validity".format(did, column)
        for column in _missing(row, DA_REQUIRED)
    ]
    status, standing = _cell(row, "Status"), _cell(row, "Standing")
    if status and status not in STATUS_VALUES:
        out.append(
            "assumption {} Status={!r} is outside the spine's closed vocabulary "
            "({})".format(did, status, " | ".join(sorted(STATUS_VALUES)))
        )
    if standing and standing not in STANDING_VALUES:
        out.append(
            "assumption {} Standing={!r} is outside its closed vocabulary ({})".format(
                did, standing, " | ".join(STANDING_VALUES)
            )
        )
    out += [
        "assumption {} EffectAt names {}, which is not a crossing the frame "
        "declares".format(did, bid)
        for bid in refs(row.get("EffectAt"))
        if bid not in crossings
    ]
    return out


def assumption_row_findings(das, bifs):
    """SR-191's row rule, as failures naming the row and the cell.

    An assumption missing a `DA_REQUIRED` cell, carrying a `Status` outside the
    spine's closed vocabulary or a `Standing` outside `STANDING_VALUES`, or
    landing (`EffectAt`) on a crossing the frame does not declare, fails. The
    caller joins these to the frame class, which fails wherever the frame check
    runs rather than only under `--strict-schema` (the Impl rung alone).

    VACUOUS when the frame declares no crossing, since an assumption's outcome
    has nowhere to land, and for the template's `-000` example rows.

    Implements: SR-191, LLR-219
    """
    if not bifs:
        return []
    crossings = {r["B-ID"] for r in bifs}
    return [
        f
        for did, row in _real(das, "DA-ID")
        for f in _assumption_row(did, row, crossings)
    ]


def _surrogate_row(sid, row, entities):
    """One surrogate's own failures: each empty required cell, a status outside
    the vocabulary, an emulated party that is not a declared entity."""
    out = [
        "surrogate {} has no {} — a surrogate names itself, the outside parties "
        "it answers for, what it is and its maturity".format(sid, column)
        for column in _missing(row, SUR_REQUIRED)
    ]
    status = _cell(row, "Status")
    if status and status not in STATUS_VALUES:
        out.append(
            "surrogate {} Status={!r} is outside the spine's closed vocabulary "
            "({})".format(sid, status, " | ".join(sorted(STATUS_VALUES)))
        )
    out += [
        "surrogate {} Emulates names {}, which is not an entity the frame "
        "declares — only an outside party (EXT-###) is emulated, never a "
        "component or an interface".format(sid, party)
        for party in refs(row.get("Emulates"))
        if party not in entities
    ]
    return out


def _fidelity(did, row, surrogates, landing):
    """One fidelity assumption's failures: it names exactly one declared
    surrogate, and lands on a crossing of a party that surrogate emulates."""
    named = refs(row.get("RealizedBy"))
    if len(named) > 1:
        return [
            "assumption {} RealizedBy names {} surrogates ({}) — a fidelity "
            "assumption states the match of exactly one".format(
                did, len(named), ", ".join(named)
            )
        ]
    (sid,) = named
    if sid not in surrogates:
        return [
            "assumption {} RealizedBy names {}, which is not a declared "
            "surrogate".format(did, sid)
        ]
    emulated = set(refs(surrogates[sid].get("Emulates")))
    parties = {landing.get(bid) for bid in refs(row.get("EffectAt"))}
    if parties & emulated:
        return []
    return [
        "assumption {} lands on no crossing of a party its surrogate {} emulates "
        "({}) — a stand-in's fidelity is a claim about the party it answers "
        "for".format(did, sid, ", ".join(sorted(emulated)) or "none")
    ]


def surrogate_findings(surs, das, exts, bifs):
    """SR-192's surrogate rules, as `(failures, advisories)`.

    FAILURES: a surrogate missing a `SUR_REQUIRED` cell (an empty `Emulates`
    list included), carrying a status outside the spine's closed vocabulary, or
    emulating anything but a declared entity (`exts`) — a component or an
    interface id does not resolve there, since only an outside party is
    emulated. And each FIDELITY assumption — one naming a surrogate in
    `RealizedBy` — must name exactly one declared surrogate and land (`EffectAt`)
    on a crossing (`bifs`) whose entity that surrogate emulates.

    ADVISORIES: a surrogate no assumption names, one line each. A stand-in
    whose fidelity nothing states is unexamined evidence, not a wrong row.

    Implements: SR-192, LLR-221
    """
    entities = {r["EXT-ID"] for r in exts}
    landing = {r["B-ID"]: _cell(r, "Entity") for r in bifs}
    surrogates = dict(_real(surs, "SUR-ID"))
    failures = [
        f for sid, row in surrogates.items() for f in _surrogate_row(sid, row, entities)
    ]
    named = set()
    for did, row in _real(das, "DA-ID"):
        if refs(row.get("RealizedBy")):
            named.update(refs(row.get("RealizedBy")))
            failures += _fidelity(did, row, surrogates, landing)
    advisories = [
        "surrogate {} is named by no assumption's RealizedBy — nothing states how "
        "faithfully it stands in for {}".format(
            sid, _cell(row, "Emulates") or "its parties"
        )
        for sid, row in surrogates.items()
        if sid not in named
    ]
    return failures, advisories


def da_citing_srs(srs):
    """`{assumption id: [requirement ids]}`: each assumption a requirement's
    `DA-Refs` cites, and the requirements citing it, in row order.

    THE ONE DERIVATION of an assumption's citing requirements. Its served needs
    are read from here, through those requirements' `SN-Refs`, and nothing
    records needs on the assumption: each requirement keeps its own need link,
    because one seam serves several arguments, and needs inherited through a
    shared assumption would hand a requirement the needs of every other
    requirement that merely relies on the same claim.

    Implements: SR-193, LLR-223
    """
    out = {}
    for sid, row in _real(srs, "SR-ID"):
        for did in refs(row.get("DA-Refs")):
            citing = out.setdefault(did, [])
            if sid not in citing:
                citing.append(sid)
    return out


def _classify(row, declared):
    """`(class, undeclared)` for one requirement: its `SR_CLASSES` member, or
    None when a citation names an assumption the registry does not declare."""
    cited = refs(row.get("DA-Refs"))
    waiver = _cell(row, "Coincident")
    undeclared = [did for did in cited if did not in declared]
    if undeclared:
        return None, undeclared
    if cited and waiver:
        return "both", []
    if cited:
        return "bridged", []
    return ("coincident" if waiver else "unclassified"), []


def classify_srs(srs, das):
    """`{requirement id: class}` over `SR_CLASSES`: how each requirement relates
    to the assumptions under it. A requirement citing an undeclared assumption
    is left out, because `sr_classification_advisories` fails it instead. An
    empty or whitespace-only `DA-Refs` counts as no citation.

    `{}` when the registry holds no real assumption: the tier is not adopted.
    The data read beside `sr_classification_advisories`, which reports from the
    same per-row classification (`_classify`).
    """
    if not _adopted(das):
        return {}
    declared = dict(_real(das, "DA-ID"))
    out = {}
    for sid, row in _real(srs, "SR-ID"):
        cls, _undeclared = _classify(row, declared)
        if cls:
            out[sid] = cls
    return out


def sr_classification_advisories(srs, das):
    """SR-193's classification, as `(failures, advisories)`.

    A requirement citing declared assumptions is bridged and one carrying a
    `Coincident` waiver is coincident; neither is reported. One with neither is
    an advisory naming it unclassified, and one carrying both is an advisory
    naming it: reported rather than failed, so the classification stays a
    worklist until a gate relies on it. A citation naming an undeclared
    assumption is a FAILURE naming the requirement; the caller joins it to the
    frame class beside the tier's other reference rules. The requirement's
    `SN-Refs` are never read or changed here.

    VACUOUS until the registry holds a real assumption row.

    Implements: SR-193, LLR-223
    """
    if not _adopted(das):
        return [], []
    declared = dict(_real(das, "DA-ID"))
    failures, advisories = [], []
    for sid, row in _real(srs, "SR-ID"):
        cls, undeclared = _classify(row, declared)
        failures += [
            "SR {} DA-Refs names {}, which is not a declared assumption".format(
                sid, did
            )
            for did in undeclared
        ]
        if cls == "unclassified":
            advisories.append(
                "SR {} is unclassified: it cites no assumption in DA-Refs and records "
                "no Coincident waiver saying why its own specification delivers its "
                "needs".format(sid)
            )
        elif cls == "both":
            advisories.append(
                "SR {} cites assumptions in DA-Refs AND records a Coincident waiver — "
                "the two contradict each other; keep the one that is true".format(sid)
            )
    return failures, advisories


def sr_form_findings(srs):
    """SR-194's form rule, as `(failures, advisories)`, over every requirement
    it is handed.

    A `Form` outside `FORM_VALUES` is a FAILURE naming the row; the caller
    joins it to the always-on integrity class. A requirement declaring no form
    is an ADVISORY naming it: the omission stays visible without failing, where
    a default would hide a missing interface behind a legitimate exception.

    Whether the question is asked at all is the composer's: the tier asks no
    requirement for a form until the registry holds a real assumption row, so
    a project that never adopts the tier is never asked
    (`assumption_tier_findings`).

    Implements: SR-194, LLR-224
    """
    failures, advisories = [], []
    allowed = " | ".join(FORM_VALUES)
    for sid, row in _real(srs, "SR-ID"):
        form = _cell(row, "Form")
        if not form:
            advisories.append(
                "SR {} declares no Form ({}) — say whether it is met at an "
                "interface, rests on an assumption or is a property of the whole "
                "system".format(sid, allowed)
            )
        elif form not in FORM_VALUES:
            failures.append(
                "SR {} Form={!r} is not one of the three forms ({})".format(
                    sid, form, allowed
                )
            )
    return failures, advisories


def uncited_assumption_advisories(das, srs):
    """SR-196, the first half: one advisory per assumption no requirement's
    `DA-Refs` cites. Drafted and approved rows are read alike, since an
    assumption is often written before the requirement that will cite it.

    Implements: SR-196, LLR-228
    """
    cited = da_citing_srs(srs)
    return [
        "assumption {} is cited by no requirement's DA-Refs — no argument relies "
        "on it yet".format(did)
        for did, _row in _real(das, "DA-ID")
        if did not in cited
    ]


def no_falsifier_advisories(das):
    """SR-196, the second half: one advisory per assumption declaring no
    `Falsifier`, the observable signal that would show it false. Drafted and
    approved rows are read alike.

    Implements: SR-196, LLR-228
    """
    return [
        "assumption {} declares no Falsifier — no falsifying signal says which "
        "observation would show it false, so it cannot be tested".format(did)
        for did, row in _real(das, "DA-ID")
        if not _cell(row, "Falsifier")
    ]


def assumption_tier_findings(srs, das, surs, exts, bifs):
    """The whole tier as `trace.analyze` composes it: `(frame, integrity,
    advisories)`, each list bound for its own class.

    FRAME: the assumption rows' own failures and a requirement's citation of an
    undeclared assumption, the tier's reference rules beside the frame's own.
    INTEGRITY, the always-on floor: every surrogate failure and a form outside
    the three. ADVISORIES, the warn pipe: an unnamed surrogate, an unclassified
    or doubly classified requirement, a requirement with no form, an uncited
    assumption and one with no falsifier.

    Three empty lists when the frame declares no crossing: an assumption's
    outcome has nowhere to land, so the tier does not apply (SR-191). And no
    requirement is asked for a form until the registry holds a real assumption
    row (SR-194): every project is scaffolded the blank form, so the file
    existing is not adoption.
    """
    if not bifs:
        return [], [], []
    sur_failures, sur_advisories = surrogate_findings(surs, das, exts, bifs)
    cls_failures, cls_advisories = sr_classification_advisories(srs, das)
    form_failures, form_advisories = (
        sr_form_findings(srs) if _adopted(das) else ([], [])
    )
    frame = assumption_row_findings(das, bifs) + cls_failures
    advisories = (
        sur_advisories
        + cls_advisories
        + form_advisories
        + uncited_assumption_advisories(das, srs)
        + no_falsifier_advisories(das)
    )
    return frame, sur_failures + form_failures, advisories


# --- reach: where an assumption lands, and where a need met in operation does --
# A crossing REACHES a need when it belongs to the party of one of the need's
# agreed stakeholders, or to a party the frame records as mediating for that
# party (`Mediates` on an entity, judged by `frame_rules.mediation_findings`).
# Two reports read that relation. The reach check (SR-195) holds each cited
# assumption to the needs it serves, need by need, so an assumption shared by
# two needs cannot reach one and silently miss the other. The need-frame gap
# (SR-188) asks the frame itself whether a need whose stakeholder is a party in
# operation has anything answering it at an operation crossing. Both ride the
# warn pipe: each names a gap in an argument, not a malformed row.

# The system in use, the member of `kitlib.spine.SYSTEM_VALUES` a need met in
# operation lands in (the other is the system that builds and delivers it).
_OPERATION = "operation"


def _agreed_parties(stks):
    """`{stakeholder id: party}` for each agreed stakeholder declaring a party:
    `Approved`, or `Founded`, which reads above it on the one ladder. A
    stakeholder still in draft has not been agreed as anyone's, so its party is
    never read."""
    return {
        sid: _cell(row, "Party")
        for sid, row in _real(stks, "STK-ID")
        if _cell(row, "Party") and (is_approved(row) or is_founded(row))
    }


def reaching_parties(needs, stks, exts):
    """`{need id: set of entity ids}`: the parties a crossing must belong to in
    order to reach each need.

    A need's parties are those of its agreed stakeholders (`stakeholder_refs`),
    plus every entity whose `Mediates` names one of them: a development session
    reaches its operator because it carries the operator's writes in and shows
    them the system's verdicts. Mediation is one step, never a chain. A need
    whose agreed stakeholders declare no party maps to an empty set, which is
    how the reach check tells an unreachable need from an undeclared one.
    `needs` are `spine_carrier.load_needs`' rows, lower-case keys and the id
    under `id`.

    Implements: SR-195, LLR-227
    """
    agreed = _agreed_parties(stks)
    mediators = {}
    for eid, row in _real(exts, "EXT-ID"):
        target = _cell(row, "Mediates")
        if target and target != eid:
            mediators.setdefault(target, set()).add(eid)
    out = {}
    for nid, need in _real(needs, "id"):
        direct = {agreed[s] for s in refs(need.get("stakeholder_refs")) if s in agreed}
        out[nid] = direct.union(*(mediators.get(p, set()) for p in direct))
    return out


def _served_needs(srs, declared):
    """`{assumption id: [need ids]}`: each cited assumption's served needs, read
    through `da_citing_srs` and the citing requirements' `SN-Refs`, in order and
    once each. A need `declared` does not hold is left out: a dangling `SN-Refs`
    is the orphan rules' finding, and it has no stakeholders to reach."""
    sn_of = {sid: refs(row.get("SN-Refs")) for sid, row in _real(srs, "SR-ID")}
    out = {}
    for did, citing in da_citing_srs(srs).items():
        served = out.setdefault(did, [])
        for nid in (n for sid in citing for n in sn_of[sid]):
            if nid in declared and nid not in served:
                served.append(nid)
    return out


def _emulated(row, surrogates):
    """`(judged, parties)`: whether the reach check judges this assumption, and
    the parties a fidelity assumption is judged against.

    An assumption naming no surrogate is judged against its needs' parties
    (`(True, None)`). A fidelity assumption whose `RealizedBy` resolves to
    exactly one declared surrogate is judged against the parties that surrogate
    emulates. One naming an undeclared surrogate, or several, is NOT judged
    (`(False, None)`): that reference is `surrogate_findings`' failure, and
    with no resolved stand-in there is no emulated party to judge against, so
    a reach report on top would only restate the broken reference."""
    named = refs(row.get("RealizedBy"))
    if not named:
        return True, None
    if len(named) != 1 or named[0] not in surrogates:
        return False, None
    return True, set(refs(surrogates[named[0]].get("Emulates")))


def _unreached_needs(did, landing, entity_of, reach, fidelity):
    """One line per served need no landing crossing reaches; a need with no
    party at all is named unreachable, since no landing could reach it."""
    whose = (
        "a party its surrogate emulates"
        if fidelity
        else "a party of the need's approved stakeholders or one mediating for it"
    )
    out = []
    for nid, parties in reach.items():
        if not parties and not fidelity:
            out.append(
                "assumption {} serves need {}, which is unreachable: no approved "
                "stakeholder of it declares a party a crossing could belong "
                "to".format(did, nid)
            )
        elif not any(entity_of[bid] in parties for bid in landing):
            out.append(
                "assumption {} serves need {}, but none of its landing crossings "
                "belongs to {}".format(did, nid, whose)
            )
    return out


def _idle_landings(did, landing, entity_of, reach, fidelity):
    """One line per landing crossing that reaches none of the served needs."""
    what = (
        "belongs to no party its surrogate emulates"
        if fidelity
        else "reaches none of the needs it serves ({})".format(", ".join(reach))
    )
    return [
        "assumption {} lands on {} ({}), which {}".format(
            did, bid, entity_of[bid] or "no entity", what
        )
        for bid in landing
        if not any(entity_of[bid] in parties for parties in reach.values())
    ]


def assumption_reach_advisories(das, srs, needs, stks, exts, bifs, surs):
    """SR-195's reach check, need by need, as advisories.

    For each assumption at least one requirement cites, its SERVED NEEDS are
    derived through `da_citing_srs` and the citing requirements' `SN-Refs`, and
    never read from the assumption. Every (served need, landing crossing) pair
    is evaluated against `reaching_parties`: a served need no landing crossing
    reaches is one advisory naming the assumption and the need, and a landing
    crossing reaching none of the served needs is one naming the assumption and
    the crossing. A served need none of whose approved stakeholders declares a
    party is named unreachable.

    A FIDELITY assumption, one naming a surrogate in `RealizedBy`, is judged
    against the parties its surrogate emulates instead of the needs' parties:
    its claim is that a stand-in matches an outside party, not that a
    stakeholder's outcome lands. An uncited assumption is not judged here
    (`uncited_assumption_advisories` reports it), nor is a fidelity assumption
    whose `RealizedBy` does not resolve to exactly one declared surrogate
    (`surrogate_findings` fails it), and a landing on an undeclared crossing is
    left to `assumption_row_findings`, which fails it.
    Silent when the frame declares no crossing (SR-191's applies-when).

    Implements: SR-195, LLR-227
    """
    if not bifs:
        return []
    entity_of = {r["B-ID"]: _cell(r, "Entity") for r in bifs}
    parties = reaching_parties(needs, stks, exts)
    served_by = _served_needs(srs, parties)
    surrogates = dict(_real(surs, "SUR-ID"))
    out = []
    for did, row in _real(das, "DA-ID"):
        served = served_by.get(did)
        judged, emulated = _emulated(row, surrogates)
        if not served or not judged:
            continue
        landing = [bid for bid in refs(row.get("EffectAt")) if bid in entity_of]
        fidelity = emulated is not None
        reach = {nid: emulated if fidelity else parties[nid] for nid in served}
        out += _unreached_needs(did, landing, entity_of, reach, fidelity)
        out += _idle_landings(did, landing, entity_of, reach, fidelity)
    return out


def _answering_srs(srs):
    """`{need id: [requirement rows]}`: the requirements naming each need in
    their `SN-Refs`, in row order."""
    out = {}
    for _sid, row in _real(srs, "SR-ID"):
        for nid in refs(row.get("SN-Refs")):
            out.setdefault(nid, []).append(row)
    return out


def _reaches_operation(rows, operation, lands):
    """Whether any of these requirements names an operation crossing in its
    `Boundary-Refs`, or cites in `DA-Refs` an assumption landing on one."""
    for row in rows:
        if operation & set(refs(row.get("Boundary-Refs"))):
            return True
        if any(operation & lands.get(did, set()) for did in refs(row.get("DA-Refs"))):
            return True
    return False


def need_frame_gap_advisories(needs, stks, srs, bifs, das):
    """SR-188's need-frame gap, as advisories: one per need met in operation
    that nothing answering it reaches an operation crossing for.

    A need is IN SCOPE when the party of one of its approved stakeholders is
    itself the entity of an operation crossing. A party that only mediates for
    such an entity does not bring the need into scope: the rule reads the
    stakeholder's own party, as SR-188 states it. An in-scope need is reported,
    once, naming it and those stakeholders, when none of the requirements
    naming it in `SN-Refs` names an operation crossing in `Boundary-Refs` and
    none of the assumptions they cite in `DA-Refs` lands on one. That is the
    one place the gap shows: a need about what a person experiences while the
    system runs, answered only at the crossings of the system that builds and
    delivers it, still passes every reference check. A need no requirement
    names meets the condition as written and is reported too: nothing answers
    it at an operation crossing either.

    Only approved stakeholders are read (`Approved`, or `Founded` above it).
    VACUOUS with no frame, no stakeholder list or no crossing declaring the
    operation system.

    Implements: SR-188, LLR-214
    """
    operation = {
        r["B-ID"]: _cell(r, "Entity") for r in bifs if _cell(r, "System") == _OPERATION
    }
    agreed = _agreed_parties(stks)
    if not operation or not agreed:
        return []
    crossings, in_operation = set(operation), set(operation.values())
    lands = {did: set(refs(row.get("EffectAt"))) for did, row in _real(das, "DA-ID")}
    answering = _answering_srs(srs)
    out = []
    for nid, need in _real(needs, "id"):
        owners = [
            s
            for s in refs(need.get("stakeholder_refs"))
            if agreed.get(s) in in_operation
        ]
        if owners and not _reaches_operation(answering.get(nid, []), crossings, lands):
            out.append(
                "need {} is met in operation by {}, but none of its requirements "
                "names an operation crossing and none of the assumptions they cite "
                "lands on one — the frame has no crossing where this outcome "
                "lands".format(
                    nid, ", ".join("{} ({})".format(s, agreed[s]) for s in owners)
                )
            )
    return out


def is_observation_tc(tc):
    """Whether a test case is an OBSERVATION: a judgment the harness cannot
    rerun, recorded as such by its `Automated` cell reading No.

    THE ONE MARKER, and deliberately not the `Level` or the requirement's
    `Verification`: those cells disagree across rows (a manual inspection is
    filed at more than one level), while every case the harness cannot rerun
    says so in `Automated`. So manual and demonstration cases are observations
    too, and declare how long their results hold.

    Implements: SR-198, LLR-233
    """
    return _cell(tc, "Automated").lower() == "no"


def _whole_at_least(value, floor):
    """Whether a cell reads as a whole number of at least `floor`."""
    return bool(_WHOLE.fullmatch(value)) and int(value) >= floor


def _present(row, column):
    """Whether a cell holds anything, whitespace included.

    THE CARRIER RULE: an absent key IS an empty cell (`kitlib.spine`). The TOML
    carrier refuses an explicit `""` at load and the migration drops empty
    cells, so an empty cell here is an absent one, on every carrier alike;
    reading key presence instead would make a legacy carrier's empty column
    declare the optional sampling model on every row. A whitespace-only cell
    was written and says nothing, so it is present, and the rule reading it
    judges it blank."""
    return (row.get(column) or "") != ""


def _model_failures(tid, row):
    """The sampling model's failures for one case: each malformed cell, and
    one of the two cells without the other."""
    out = []
    size, rule = _cell(row, "SampleSize"), _cell(row, "AcceptanceRule")
    if _present(row, "SampleSize") and not _whole_at_least(size, 1):
        out.append(
            "TC {} SampleSize={!r} is not a whole number of at least 1 — a "
            "sampling model's size counts the samples judged".format(tid, size)
        )
    if _present(row, "AcceptanceRule") and not rule:
        out.append(
            "TC {} AcceptanceRule is empty — a sampling model states what a "
            "passing sample is".format(tid)
        )
    if _present(row, "SampleSize") != _present(row, "AcceptanceRule"):
        has, lacks = ("SampleSize", "AcceptanceRule")
        if not _present(row, "SampleSize"):
            has, lacks = lacks, has
        out.append(
            "TC {} declares {} without {} — a sampling model is both cells or "
            "neither".format(tid, has, lacks)
        )
    return out


def _declaration_failures(tid, row):
    """One case's malformed declaration cells: a lifetime that is not a whole
    number of days at the floor, a policy outside the pair, and the model."""
    out = []
    max_age, sampling = _cell(row, "MaxAge"), _cell(row, "Sampling")
    if max_age and not _whole_at_least(max_age, MAX_AGE_FLOOR_DAYS):
        out.append(
            "TC {} MaxAge={!r} is not a whole number of days of at least {} — "
            "a judgment is not demanded more often than it can honestly be "
            "taken".format(tid, max_age, MAX_AGE_FLOOR_DAYS)
        )
    if sampling and sampling not in SAMPLING_VALUES:
        out.append(
            "TC {} Sampling={!r} is outside its closed vocabulary ({})".format(
                tid, sampling, " | ".join(SAMPLING_VALUES)
            )
        )
    return out + _model_failures(tid, row)


def _omissions(tid, row):
    """One observation case's omitted declarations, one advisory each."""
    wanted = [("Inputs", "the inputs its judgment reads"), ("MaxAge", "its lifetime")]
    if refs(row.get("Assumption-Refs")):
        wanted.append(("Sampling", "its sampling policy, sampled | monitored"))
    return [
        "TC {} is an observation test case declaring no {} ({}) — declare it "
        "so its result can go stale".format(tid, column, what)
        for column, what in wanted
        if not refs(row.get(column))
    ]


def observation_tc_findings(tcs):
    """SR-198's declaration rules, as `(failures, advisories)`, each naming the
    row.

    ADVISORIES: an observation case (`is_observation_tc`) omitting `Inputs`,
    `MaxAge`, or, when it cites assumptions, `Sampling`, one line per omission.
    Reported rather than refused, so observation cases written before these
    cells existed keep passing. And an AUTOMATED case carrying any
    `OBSERVATION_CELLS` cell, one line per cell: the harness reruns it, so the
    declaration says nothing about it.

    FAILURES, bound for the always-on integrity floor: a `MaxAge` that is not a
    whole number of days of at least `MAX_AGE_FLOOR_DAYS`, a `Sampling` outside
    `SAMPLING_VALUES`, a `SampleSize` that is not a whole number of at least
    one, an `AcceptanceRule` of whitespace alone, and one of those two model
    cells without the other, on an observation case. An empty cell is an
    absent one (the carrier rule, `_present`). An automated case's
    stray cell is the advisory above and nothing more: its values declare
    nothing, so judging them would fail a row for a cell it should not carry.

    Whether a sampling model is adequate for its claim is judged when the case
    is approved, never here. The template's `-000` row is never judged.

    Implements: SR-198, LLR-233
    """
    failures, advisories = [], []
    for tid, row in _real(tcs, "TC-ID"):
        if is_observation_tc(row):
            failures += _declaration_failures(tid, row)
            advisories += _omissions(tid, row)
            continue
        advisories += [
            "TC {} is automated but declares {} — only an observation test case "
            "declares what it reads, how long its result holds and how it "
            "samples".format(tid, column)
            for column in OBSERVATION_CELLS
            if _present(row, column)
        ]
    return failures, advisories


def sampling_model_declared(tc):
    """Whether a case declares a usable SAMPLING MODEL: it is `sampled`, and its
    sample size (a whole number of at least one) and its acceptance rule (not
    empty) are both valid. A sampled result supports a positive claim only under
    a stated model; a monitored case, or a sampled one with neither cell, has
    declared none.

    Implements: SR-198, LLR-233
    """
    return (
        _cell(tc, "Sampling") == "sampled"
        and _whole_at_least(_cell(tc, "SampleSize"), 1)
        and bool(_cell(tc, "AcceptanceRule"))
    )


def _crossings(row):
    """The boundary crossings an interface row realizes: its from- and
    to-external tie-backs. Empty for an internal seam."""
    return refs(row.get("InterfaceFromExternal")) + refs(row.get("InterfaceToExternal"))


def interface_bridge_findings(ifs, das):
    """SR-211's interface rule, as `(failures, advisories)`.

    Reads only BOUNDARY interfaces, those with a from- or to-external tie-back:
    an internal seam realizes no crossing, so no outcome hangs on its reading.
    A boundary interface naming declared assumptions in `BridgedBy` is bridged,
    and one recording in `Coincident` why its reading is the outcome is
    coincident; neither is reported.

    FAILURES: a `BridgedBy` entry naming an assumption the registry does not
    declare, naming the interface and the id; the caller joins it to the
    interface class, which fails `--strict`. ADVISORIES: a boundary interface
    with neither cell, one line naming it, on the warn pipe.

    No requirement reference is read or asked for: the requirement a seam
    answers stays derived through its owner, and stating it on the row would
    give that relation a second home.

    Implements: SR-211, LLR-250
    """
    declared = dict(_real(das, "DA-ID"))
    failures, advisories = [], []
    for iid, row in _real(ifs, "IF-ID"):
        crossings = _crossings(row)
        if not crossings:
            continue
        bridging = refs(row.get("BridgedBy"))
        failures += [
            "IF {} BridgedBy names {}, which is not a declared assumption".format(
                iid, did
            )
            for did in bridging
            if did not in declared
        ]
        if not bridging and not _cell(row, "Coincident"):
            advisories.append(
                "IF {} realizes boundary crossing {} but names no assumption in "
                "BridgedBy carrying its reading to an outcome, and records no "
                "Coincident waiver saying why its reading is the outcome".format(
                    iid, ", ".join(crossings)
                )
            )
    return failures, advisories


def obstacle_hat_findings(das, hat_names):
    """SR-214's provenance rule: each perspective an assumption's
    `ObstacleHats` names is a declared hat, as failures naming the assumption
    and the name. The caller joins them to the dangling-hat class, which fails
    `--strict`.

    `hat_names` is the roster's names as the checker read them, or an empty
    set when the project has no roster; every named perspective is then
    undeclared, since a cell pointing into a roster that does not exist points
    at nothing. An empty cell is valid and produces nothing: it reads as NOT
    RECORDED, never as "no perspective applied". The cell is kept apart from
    `Hat-Refs`, which records attribution, because this one records which
    perspective's question raised the obstacle.

    Implements: SR-214, LLR-252
    """
    return [
        "assumption {} ObstacleHats names {}, which is not a perspective the "
        "hats roster declares".format(did, name)
        for did, row in _real(das, "DA-ID")
        for name in refs(row.get("ObstacleHats"))
        if name not in hat_names
    ]
