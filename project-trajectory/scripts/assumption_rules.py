"""THE ASSUMPTION TIER'S RULES — pure joins over the assumptions registry.

The sibling of `frame_rules.py`, and built the same way: every rule here is a
JOIN ACROSS ROWS, it reads no file, and `trace.analyze` composes it and stays
its only caller. `trace.py` is held to an exact size ratchet, so the tier's
rules land here and `trace.py` grows by the composition lines alone (spine map
D21).

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

WHERE THE TIER APPLIES. An assumption's outcome lands on a boundary crossing,
so with no declared crossing there is nothing to land on and the whole tier is
silent (SR-191's applies-when). And the requirement-side reports ask nothing of
a project that has not adopted the tier: until the registry holds a real
assumption row, no requirement is asked for a citation or a form. Every
adopter is scaffolded the blank form, so the file existing is not adoption.

Rows are the carrier's column-keyed dicts (`DA-ID`, `EffectAt`, `SUR-ID`,
`Emulates`, `SR-ID`, `DA-Refs`, `EXT-ID`, `B-ID`, `Entity`), exactly as
`trace.load_registries` hands them over; a list cell arrives `;`-joined. Every
function returns plain finding strings, and no function writes to a row it is
handed.

Stdlib only. A plain sibling of `scripts/`, not a `kitlib` module, for the
reason `coherence.py` records: these are the checker's rules, and the
scaffolder has no business importing them.

Contracts: IF-190 — the seam this module declares (process.md §8; row of record
in docs/requirements/interfaces.toml).

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
"""

try:
    from kitlib.spine import FORM_VALUES, STATUS_VALUES, is_example, refs
except ImportError:  # pragma: no cover - in-process fallback
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kitlib.spine import FORM_VALUES, STATUS_VALUES, is_example, refs

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
