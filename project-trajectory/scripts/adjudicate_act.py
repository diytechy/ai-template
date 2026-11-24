#!/usr/bin/env python3
"""adjudicate_act.py — the ACT a committed, recorded verdict still owes, and
the act brief filled from it.

Stack-agnostic, standard-library only (Python 3.11+, Windows/POSIX).

WHY THIS MODULE EXISTS (WI-912). A sitting used to judge and act in one turn:
the brief that asked for the judgement also ordered the `Status` flips and the
anchoring copy. So a sitting held ahead of landing order that followed its
brief took its act out of order. The operator's rulings split the two (revision
31 of the review-churn plan: verdicts move between lanes while acts keep
landing order; revision 32: the act is a later turn of the retained
adjudicator, run fresh where retention lapsed; revision 36: the split reaches
the shipped briefs and the coordinator's entry point). Q1 of
coordinator-2026-10-14 D-003 makes the act turn an adjudicator turn with its
own brief, since OI-45 (b) keeps scripted acceptance retired; Q2 makes a MEANING
row's blessing a typed mark on the verdict, `[MEANING+BLESS]`.

THE CARRIER. The verdict and the binding beside it, as committed at the lane's
HEAD, read through `kitlib.sitting.recorded_at`, the one reader every consumer
of a verdict goes through. After the split that committed verdict is the act
turn's whole authority: the session that wrote it may be gone, and a fresh act
turn takes the same act. The other consumers of the same carrier are
unchanged: the merge slot (`kitlib.sitting.uncovered_refusal` and
`unrecorded_refusal`) still admits an act only when a recorded verdict over
the act's own rows backs it (operator ruling 6, 2026-10-07), and its lane rule
(`held_status.commit_held_acceptance_lines`) admits a held-rung re-acceptance
only when that verdict rules the row CLARITY and its binding records the row's
text. `intake.py snapshot --verdict` still records the verdict an act names,
for audit; no rule requires it.

WHAT THE VERDICT AUTHORIZES. Exactly the rows each recorded part rules to
authorize them, read through `kitlib.sitting.judged_rows`, the one reader the
merge's backing check also reads, so the two cannot disagree. A first-acceptance
part's ACCEPT flips a row, on a released rung only (a dial the operator
tightened after the sitting binds the act it has not yet authorized). An amendment part's CLARITY re-accepts a row, naming the
verdict on a held rung; its MEANING re-accepts only on a released rung and
only with the bless mark. A RETURN row, an unmarked or held MEANING row, a
Done-when part and every brief class but amendment, first-acceptance and
combined owe no act. The dial is read at the act, from the committed tree, and
each rung's arm is `intake.adjudication_action`'s answer (the held-rung
policy's one home, which the judging composer reads too).

OWED, TAKEN OR INCONSISTENT: judged at a revision, never the working tree. A
first acceptance is owed while the row's committed status is below Accepted,
whatever its recorded copy holds (a whole-registry copy carries Drafted rows),
and taken when the row is Accepted and its copy equals its committed text. A
re-accept of an Accepted row is taken when the copy equals the row, and owed
otherwise. A re-accept of a row absent from the committed registries is a
RETIREMENT (the operator's ruling of 2026-10-17, WI-912): owed while its recorded
copy still holds the row, named in `--reaccepts` with the other re-accepts
(the snapshot writer clears a recorded row the live registry no longer holds
only when it is named there), and taken once the copy no longer holds it. On a
held rung a retirement owes no act, read through the same held-rung test as a
held MEANING or APPROVE row: removing a held row is the operator's. Every other
state (an Accepted row without an equal copy at a first acceptance, a first
acceptance of an absent row, a re-accept of a row below Accepted, a row no
compared tier holds) is inconsistent and refuses the whole derivation, naming
the row: it is never counted as taken. "Equal" compares the whole parsed row, Status included,
which is what makes a flip committed without its copy read as inconsistent.

A FLIP WAITS WHILE ITS PARENT STAYS UNACCEPTED (WI-1059). An owed
first-acceptance flip waits when a parent the parent-first rule reads for it
(`kitlib.spine.parent_first_findings`, the commit hook's own question) would
not be accepted after the act: neither accepted at the revision nor flipped by
a flip of the act that does not itself wait, so a flip under a waiting parent
waits too. The rows are read by the hook's own reader
(`landing_rules.parent_first_tiers`), and one of its registries that cannot
be read or does not parse refuses the whole derivation, naming it. A waiting
flip stays OWED: the brief names it, with each parent it waits on, and never
lists it; the later-act derivation reports it marked; a verdict whose every
remaining act waits is refused, naming each; and once each parent is accepted,
the same verdict's act lists it. So the act lists only flips the hook admits,
and a wrong wait leaves a flip owed and reported, never lost. ("Waits", not
"held": held names the rung below.)

A HELD CLARITY ACT IS BOUND TO THE TEXT ITS VERDICT JUDGED. The binding beside
the verdict records the digest of each judged row's accepted text and
adjudicated links (`kitlib.sitting.recorded_identities`; the links since
WI-1069, so a binding written before then refuses a held row carrying one,
and that row is re-sat); a re-accept owed on a held rung is
owed only while the committed row still has that digest
(`acceptance_record.accepted_text_digest`). A binding with no identity, a
malformed one, one that does not name the row, or a different digest refuses
the whole derivation, naming the row and both digests, so the entry point
refuses before it launches an adjudicator. A verdict sat before the identity
existed binds no text and is re-sat. Released rungs and taken acts read no
identity.

ALL OR NOTHING, as `adjudicate_brief`'s rule 2 states: every call returns
`(value, None)` or `(None, reason)`, never a partial act and never a brief
with a hole in it.

Component: CMP-008

Contracts: IF-296 — the seam this module declares (process.md §8; row of record
in docs/requirements/interfaces.toml).

Contract IF-296: the act assembler's call surface, which the coordinator's
entry point consumes.
    `owed_acts(root, verdict, rev="HEAD")` returns `(acts, None)`, where
    `acts` is `{"amendment": {"reaccepts": [ids], "verdict": bool},
    "first-acceptance": {"accepts": {registry: [ids]}}}` in that order, each
    part present only when something is owed there, the amendment part also
    carrying `"retires": [ids]`, the re-accepted ids absent from the committed
    registries, only when one is owed, and the first-acceptance part
    `"waiting": {id: [(parent, status)]}`, the owed flips that wait on an
    unaccepted parent (never in `accepts`, which is empty only when every
    flip waits beside an owed amendment), only when one waits, or
    `(None, reason)` for
    a verdict that is not committed at `rev`, has no binding there, records
    a pending or failed outcome, is not valid against its binding, is of a
    class that owes no act, owes no act, owes no act that can be taken
    because every flip it still owes waits (each named with its parents),
    or judged a row whose committed
    state is inconsistent (named), a parent-first registry that cannot be
    read or does not parse at `rev` (named) while a flip is owed,
    or a held CLARITY row whose accepted text
    differs from the identity the verdict's binding records for it - the
    binding has no identity cell, a malformed one, does not name the row, or
    names another digest (the row, the bound digest and the committed digest
    named); `act_values(root, verdict, wi,
    rev="HEAD")` is the act brief's slot values from it, and
    `compose_act(root, verdict, wi, prompt_templates=None)` the act brief
    filled from them at HEAD, an operator override under `ADJUDICATE-ACT`
    winning, or `(None, reason)`; `left_owed(root, verdict, rev="HEAD")` is
    None when `rev` carries every act the verdict authorizes in full, else
    the acts still owed there, each waiting flip marked `waiting on` its
    parents, or the derivation's refusal, and
    `bound_brief(root, verdict, rev="HEAD")` the brief class a recorded,
    actable verdict's binding records, or None. Reads git, the shipped
    template and the repository's scripts layout (`agent_brief.scripts_dir`)
    only; writes nothing.
"""

from __future__ import annotations

from pathlib import Path

import acceptance_record
import agent_brief
import baseline_snapshot
import intake
import landing_rules
import prompts
from kitlib import authority as kauthority
from kitlib import sitting as ksitting
from kitlib import spine as kspine
from kitlib.git import git_out

# The brief classes whose verdict can authorize an act: the one home of the
# set, which `adjudicate_brief` also reads to decide which retained sessions'
# identity covers the act brief.
ACTABLE = ("amendment", "first-acceptance", ksitting.SITTING)
# A part of the act that nothing is owed for: a state the derivation reports,
# never a default a missing value falls back to.
NONE_OWED = "none owed"
# A judged row's state when its ruling authorizes no act on it: a retirement
# on a held rung.
NO_ACT = "no act"
# The act a re-accept of a row absent from the committed registries is.
RETIRE = "retire"


def _verdict_rel(root, verdict):
    """The verdict's repo-relative POSIX path, or None when an absolute path
    lies outside `root`."""
    path = Path(str(verdict))
    if path.is_absolute():
        try:
            path = path.resolve().relative_to(Path(root).resolve())
        except ValueError:
            return None
    rel = path.as_posix()
    return rel[2:] if rel.startswith("./") else rel


def _unrecorded_reason(root, rev, rel):
    """Why the verdict at `rel` is not recorded at `rev`, read off the files
    `recorded_at` read; only ever asked once that reader returned None.

    Implements: SR-231, SR-232, LLR-338"""
    text = git_out(root, ["show", "{}:{}".format(rev, rel)])
    if text is None:
        return "the verdict {} is not committed at {}".format(rel, rev)
    binding = git_out(root, ["show", "{}:{}".format(rev, ksitting.requested_path(rel))])
    bound = ksitting.read_requested(binding) if binding is not None else None
    if bound is None:
        return "the verdict {} has no binding committed beside it at {}".format(
            rel, rev
        )
    brief, kinds, outcome = bound
    if outcome != "recorded":
        return "the verdict {}'s binding records the outcome {}, not recorded".format(
            rel, outcome
        )
    why = ksitting.parse(text, brief, kinds, rel)[1] or "it does not parse"
    return "the verdict {} is not a valid {} verdict: {}".format(rel, brief, why)


def _recorded_verdict(root, rev, rel):
    """`(brief class, {kind: part})` for a recorded verdict of an actable
    class, or `(None, reason)`.

    Implements: SR-231, SR-232, LLR-338"""
    binding = git_out(root, ["show", "{}:{}".format(rev, ksitting.requested_path(rel))])
    bound = ksitting.read_requested(binding) if binding else None
    if bound and bound[0] not in ACTABLE:
        return None, "a {} verdict owes no act; only {} verdicts do".format(
            bound[0], ", ".join(ACTABLE)
        )
    parsed = ksitting.recorded_at(root, rev, rel)
    if not parsed:
        return None, _unrecorded_reason(root, rev, rel)
    return (bound[0], parsed), None


def _tier(rid):
    """`(registry, id column)` of the compared tier holding row `rid`, read off
    its prefix, or None."""
    for rel, id_col in baseline_snapshot.SNAPSHOT_TIERS:
        if rid.startswith(id_col[: -len("ID")]):
            return rel, id_col
    return None


def _held(dial, rid):
    """Does the dial hold the rung row `rid`'s status cell is accepted into?
    A row no compared tier holds is held, the direction every unknown fails."""
    tier = _tier(rid)
    return kauthority.holds_under(dial, kauthority.rung_for(tier[0])) if tier else True


def _arm(ruling, held):
    """The act one authorized row's ruling owes on its rung: "accept",
    "reaccept" or None. The rung's arm is `intake.adjudication_action`'s
    answer, the held-rung policy's one home, never restated here: "recommend"
    owes no act, "reaccept" is the re-accept a held CLARITY row owes, and
    "flip" is the act itself, a flip for an ACCEPT row and a re-accept for an
    amendment row. A RETURN row, or any ruling that is not an acceptance or an
    amendment ruling, owes none.

    Implements: SR-231, SR-232, LLR-338"""
    if ruling not in ("ACCEPT", "CLARITY", "MEANING"):
        return None
    if intake.adjudication_action(held, ruling) == "recommend":
        return None
    return "accept" if ruling == "ACCEPT" else "reaccept"


def _authorized(parts, dial):
    """`[(act, row id, held)]` every recorded part authorizes, `act` being
    "accept" or "reaccept", amendment first, in verdict order within a kind.
    Which rows a part authorizes is `kitlib.sitting.judged_rows`'s answer (a
    MEANING row only with its bless mark), the reader the merge's backing
    check also reads; each such row's act is `_arm`'s.

    Implements: SR-231, SR-232, LLR-338"""
    judged = ksitting.judged_rows(parts)
    out = []
    for kind in ("amendment", "first-acceptance"):
        if kind not in parts:
            continue
        for rid, ruling in parts[kind][3].items():
            if (kind, rid) not in judged:
                continue
            held = _held(dial, rid)
            act = _arm(ruling, held)
            if act:
                out.append((act, rid, held))
    return out


class _Rows:
    """The committed rows of each registry and of its recorded copy at one
    revision, each registry read once."""

    def __init__(self, root, rev):
        self.root, self.rev, self.cache = root, rev, {}

    def pair(self, rel, id_col):
        key = (rel, id_col)
        if key not in self.cache:
            copy = "{}/{}".format(baseline_snapshot.SNAPSHOT_DIR, rel)
            self.cache[key] = (
                acceptance_record.rows_at(self.root, self.rev, rel, id_col),
                acceptance_record.rows_at(self.root, self.rev, copy, id_col),
            )
        return self.cache[key]


# Whether a row's `Status` claims acceptance (`Accepted` or `Founded`): the pair's
# one home is `kitlib.spine.claims_acceptance`, which the acceptance record's
# acceptance-act readers and the parent-first rule read too.
_claims_acceptance = kspine.claims_acceptance


def _retirement(act, rid, held, recorded):
    """The state of a judged row absent from the committed registries: a
    re-accept is a retirement, owed while the copy still holds the row
    (`recorded`) and taken once it does not, and owes no act on a held rung;
    a first acceptance of an absent row is inconsistent.

    Implements: SR-231, SR-232, LLR-338"""
    if act != "reaccept":
        return None, _odd(rid, "absent", False)
    if held:
        return NO_ACT, None
    return (RETIRE if recorded else "taken"), None


def _state(rows, act, rid, held, bound):
    """`("owed" | RETIRE | "taken" | NO_ACT, None)` for one authorized row,
    or `(None, why)` when its committed state is inconsistent with the act, or
    when an owed held re-accept's text is not the text `bound` (the verdict's
    `(identities, why)`) records.

    Implements: SR-231, SR-232, SR-178, LLR-338, LLR-359"""
    tier = _tier(rid)
    if tier is None:
        return None, "{} is held by no compared tier".format(rid)
    live, copy = rows.pair(*tier)
    row = live.get(rid)
    if row is None:
        return _retirement(act, rid, held, rid in copy)
    accepted, equal = _claims_acceptance(row), copy.get(rid) == row
    if act == "accept" and not accepted:
        return "owed", None
    if accepted and equal:
        return "taken", None
    if accepted and act == "reaccept":
        why = _unbound_text(row, tier, rid, bound) if held else None
        return (None, why) if why else ("owed", None)
    return None, _odd(rid, row.get("Status") or "(empty)", equal)


def _unbound_text(row, tier, rid, bound):
    """Why the held re-accept of row `rid` is not bound to its committed text,
    or None: the verdict's binding (`bound`, `(identities, why)`) records no
    identity, does not name the row, or names another digest than the
    committed row's accepted text and adjudicated links have.

    Implements: SR-178, LLR-359"""
    committed = acceptance_record.accepted_text_digest(tier[0], tier[1], row)
    identities, why = bound
    if identities is None:
        return "{} is held and its verdict binds no text ({}); committed {}".format(
            rid, why, committed
        )
    if rid not in identities:
        return "{} is held and its verdict's binding names no text for it; committed {}".format(
            rid, committed
        )
    if identities[rid] != committed:
        return "{} is held and its judged text (accepted cells and adjudicated links) moved after the verdict: bound {}, committed {}".format(
            rid, identities[rid], committed
        )
    return None


def _odd(rid, status, equal):
    """The inconsistent-row line, naming its status and its copy."""
    return "{} is inconsistent: its committed status is {} and its recorded copy {}".format(
        rid, status, "equals it" if equal else "does not equal it"
    )


def _findings(tiers, accepted):
    """The parent-first rule's findings over `tiers` with every row whose id
    is in `accepted` read as `Accepted`, on an in-memory copy (this module
    writes no registry; OI-30 D3's writer guard exempts the line by name): the
    commit hook's question about the tree an act taking those flips would
    leave.

    Implements: SR-231, LLR-338"""
    after = {
        label: [
            dict(row, Status="Accepted")
            if str(row.get(label + "-ID") or "").strip() in accepted
            else row
            for row in rows
        ]
        for label, rows in tiers.items()
    }
    return kspine.parent_first_findings(after)


def _waiting(tiers, flips):
    """`{flip: [(parent, status)]}`, in `flips`' order, for each owed
    first-acceptance flip that waits: a parent the parent-first rule reads for
    it is neither accepted in `tiers` nor flipped by a flip that does not wait.

    A fixpoint from every flip taken: each pass drops the flips the rule's
    findings name as accepted children, until a pass drops none. Each pass
    that does not stop shrinks a finite set, so it ends; the set it ends on is
    the largest whose flips leave the rule nothing to find, which is why a
    flip under a waiting parent waits too. Each waiting flip is then named
    with every parent it waits on, read with it alone added to that set.

    Implements: SR-231, LLR-338"""
    taken = set(flips)
    while True:
        late = taken & {entry[0] for entry in _findings(tiers, taken)}
        if not late:
            break
        taken -= late
    return {
        rid: [
            (parent, status)
            for child, _status, parent, status in _findings(tiers, taken | {rid})
            if child == rid
        ]
        for rid in flips
        if rid not in taken
    }


def _waits(root, rev, rel, owed):
    """`(waiting, None)` for the `owed` acts of the verdict at `rel` judged at
    the commit `rev` (`_waiting`'s map, empty when no flip is owed), or
    `(None, reason)` when a registry the parent-first rule reads fails there.
    The rows are read by the commit hook's own reader, so the act lists a
    flip only where the hook would judge the same rows.

    Implements: SR-231, LLR-338"""
    flips = [rid for act, rid, _held in owed if act == "accept"]
    if not flips:
        return {}, None
    tiers, failures = landing_rules.parent_first_tiers(root, rev + ":")
    if failures:
        return None, (
            "the verdict {}'s flips cannot be judged against the parent-first "
            "rule at {}: {}".format(rel, rev, "; ".join(failures))
        )
    return _waiting(tiers, flips), None


def _derive(root, verdict, rev):
    """`(rel, authorized, owed, waiting, None)` for the verdict at `verdict`
    judged at the commit `rev`, or `(rel, None, None, None, reason)` when it
    is refused: not recorded there, of a class that owes no act, a judged row
    in a state no act explains, or a parent-first registry that fails to read.
    A waiting flip stays in `owed`; `waiting` names it (`_waits`).

    Implements: SR-231, SR-232, LLR-338"""
    rel = _verdict_rel(root, verdict)
    if not rel:
        refusal = "the verdict {} lies outside {}".format(verdict, root)
        return None, None, None, None, refusal
    found, why = _recorded_verdict(root, rev, rel)
    if found is None:
        return rel, None, None, None, why
    rows, authorized, owed = _Rows(root, rev), [], []
    judged = _authorized(found[1], kauthority.dial_at(root, rev))
    bound = (None, None)
    if any(act == "reaccept" and held for act, _rid, held in judged):
        bound = ksitting.recorded_identities(root, rev, rel)
    for act, rid, held in judged:
        state, why = _state(rows, act, rid, held, bound)
        if state is None:
            refusal = "the verdict {} judged a row {}".format(rel, why)
            return rel, None, None, None, refusal
        if state == NO_ACT:
            continue
        authorized.append((act, rid, held))
        if state in ("owed", RETIRE):
            owed.append((RETIRE if state == RETIRE else act, rid, held))
    waiting, why = _waits(root, rev, rel, owed)
    if why:
        return rel, None, None, None, why
    return rel, authorized, owed, waiting, None


def owed_acts(root, verdict, rev="HEAD"):
    """`(acts, None)`: every act the verdict at `verdict` authorizes that the
    commit `rev` does not yet carry in full, or `(None, reason)` (the module
    docstring's partition and refusals).

    Implements: SR-231, SR-232, LLR-338"""
    rel, authorized, owed, waiting, why = _derive(root, verdict, rev)
    if why:
        return None, why
    if any(act == "accept" for act, _rid, _held in owed) and not _recorded(root, rev):
        return None, (
            "the verdict {} accepts rows, but no acceptance record exists at {}: "
            "the first signing creates it, and that is the operator's".format(rel, rev)
        )
    if not owed:
        return None, "the verdict {} owes no act: {}".format(
            rel,
            "every act it authorizes is taken at {}".format(rev)
            if authorized
            else "it authorizes none",
        )
    if all(rid in waiting for _act, rid, _held in owed):
        return None, (
            "the verdict {} owes no act that can be taken at {}: every flip it "
            "still owes waits on a parent that is not accepted, and a later act "
            "lists each once its parent is accepted: {}".format(
                rel, rev, "; ".join(_waiting_lines(waiting))
            )
        )
    return _grouped(owed, waiting), None


def left_owed(root, verdict, rev="HEAD"):
    """None when the commit `rev` carries in full every act the verdict at
    `verdict` authorizes; else why not: the acts still owed there, named, a
    waiting flip marked with each parent it waits on, or the derivation's
    refusal. What the act turn asks after its call.

    Implements: SR-231, SR-232, LLR-338"""
    _rel, _authorized, owed, waiting, why = _derive(root, verdict, rev)
    if why:
        return why
    if not owed:
        return None
    parts = _grouped(owed, waiting)
    named = []
    if "amendment" in parts:
        named.append("re-accept " + ", ".join(parts["amendment"]["reaccepts"]))
    first = parts.get("first-acceptance", {})
    for rel, ids in sorted(first.get("accepts", {}).items()):
        named.append("flip {} ({})".format(", ".join(ids), rel))
    named += ["flip " + line for line in _waiting_lines(first.get("waiting", {}))]
    return "; ".join(named)


def _waiting_lines(waiting):
    """One line per waiting flip: `<row> (<registry>) waiting on <parent>
    (<status>)[, ...]`, a missing status reading `no status` as the
    parent-first line reads it. The brief, the refusal and the later-act
    report all write a waiting flip this way.

    Implements: SR-231, LLR-338"""
    return [
        "{} ({}) waiting on {}".format(
            rid,
            _tier(rid)[0],
            ", ".join(
                "{} ({})".format(parent, status or "no status")
                for parent, status in parents
            ),
        )
        for rid, parents in waiting.items()
    ]


def bound_brief(root, verdict, rev="HEAD"):
    """The brief class the binding beside an accepted, actable verdict
    records at `rev`, or None: what the act turn's keep is planned by.

    Implements: SR-231, LLR-338"""
    rel = _verdict_rel(root, verdict)
    found = _recorded_verdict(root, rev, rel)[0] if rel else None
    return found[0] if found else None


def _recorded(root, rev):
    """Does the commit `rev` carry the acceptance record's directory?"""
    kind = git_out(
        root, ["cat-file", "-t", "{}:{}".format(rev, baseline_snapshot.SNAPSHOT_DIR)]
    )
    return (kind or "").strip() == "tree"


def _grouped(owed, waiting):
    """The owed rows as `owed_acts`' `acts` mapping, amendment first; a
    flip `waiting` names is in the first-acceptance part's `waiting`, never in
    its `accepts`."""
    acts = {}
    amendment = [entry for entry in owed if entry[0] != "accept"]
    if amendment:
        acts["amendment"] = {
            "reaccepts": [rid for _act, rid, _held in amendment],
            "verdict": any(held for _act, _rid, held in amendment),
        }
        retires = [rid for act, rid, _held in amendment if act == RETIRE]
        if retires:
            acts["amendment"]["retires"] = retires
    flips = [rid for act, rid, _held in owed if act == "accept"]
    if flips:
        acts["first-acceptance"] = _first_acceptance(flips, waiting)
    return acts


def _first_acceptance(flips, waiting):
    """The first-acceptance part over the owed `flips`: `accepts`, the flips
    the act lists by registry (empty only when every flip waits), and
    `waiting`, present only when a flip waits.

    Implements: SR-231, LLR-338"""
    accepts = {}
    for rid in flips:
        if rid not in waiting:
            accepts.setdefault(_tier(rid)[0], []).append(rid)
    part = {"accepts": accepts}
    if waiting:
        part["waiting"] = waiting
    return part


def _amendment_text(part, rel, wi, scripts):
    """The amendment act's rendered rows and command, run from `scripts`."""
    command = "python {}/intake.py snapshot --reaccepts {}".format(
        scripts, ",".join(part["reaccepts"])
    )
    if part["verdict"]:
        command += " --verdict {}".format(rel)
    retires = part.get("retires") or []
    accepted = [rid for rid in part["reaccepts"] if rid not in retires]
    rows = "Re-accept these Accepted rows: {}.\n".format(", ".join(accepted))
    if retires:
        rows = (rows if accepted else "") + (
            "Retire these rows, which the lane deleted from their registries, "
            "from the recorded copy (leave them deleted): {}.\n".format(
                ", ".join(retires)
            )
        )
    return (
        "{}Run, then commit the copy it writes, ending the commit with "
        "`WI: {}`:\n\n    {}".format(rows, wi, command)
    )


def _acceptance_part(part, registries, wi, scripts):
    """The first-acceptance part's rendered text: the listed flips and their
    command (or that no flip can be taken in this act), then each waiting
    flip, named with the parents it waits on and never listed.

    Implements: SR-231, LLR-338"""
    accepts, waiting = part["accepts"], part.get("waiting")
    text = (
        _acceptance_text(accepts, registries, wi, scripts)
        if accepts
        else "No flip can be taken in this act."
    )
    if not waiting:
        return text
    return (
        "{}\n\nNot in this act: each row below is owed a flip under this "
        "verdict, but a parent it cites is not accepted and this act does not "
        "accept it, so the parent-first rule would refuse the flip. Leave its "
        "`Status` at `Drafted` and leave it out of the command; a later act "
        "lists it once each parent it waits on is accepted.\n\n{}".format(
            text, "\n".join("    - " + line for line in _waiting_lines(waiting))
        )
    )


def _acceptance_text(accepts, registries, wi, scripts):
    """The first-acceptance act's rendered rows and command, run from
    `scripts`."""
    rows = ", ".join(
        "{} ({})".format(rid, rel) for rel in sorted(accepts) for rid in accepts[rel]
    )
    return (
        "Flip `Status` from `Drafted` to `Accepted` for exactly these rows: {}.\n"
        "Then run, and commit the flips and the copy together, ending the commit "
        'with `WI: {}`:\n\n    python {}/intake.py snapshot --accepts "{}"'.format(
            rows, wi, scripts, registries
        )
    )


def act_values(root, verdict, wi, rev="HEAD"):
    """`({slot: value}, None)` for the act brief, or `(None, reason)`. Its
    commands and its `scripts` value name the repository's own scripts
    directory (`agent_brief.scripts_dir`, the value the reviewer and worker
    briefs take).

    Implements: SR-231, LLR-338"""
    acts, why = owed_acts(root, verdict, rev)
    if acts is None:
        return None, why
    rel = _verdict_rel(root, verdict)
    wi = str(wi or "").strip()
    if not wi:
        return None, "no work item was named for the act's commit trailer"
    amendment, first = acts.get("amendment"), acts.get("first-acceptance")
    accepts = (first or {}).get("accepts") or {}
    registries = baseline_snapshot.format_accepts(dict.fromkeys(accepts, wi))
    scripts = agent_brief.scripts_dir(root)
    return {
        "verdict": rel,
        "wi": wi,
        "scripts": scripts,
        "amendment_act": _amendment_text(amendment, rel, wi, scripts)
        if amendment
        else NONE_OWED,
        "acceptance_act": _acceptance_part(first, registries, wi, scripts)
        if first
        else NONE_OWED,
        "registries": registries or NONE_OWED,
        "accepts_rows": "\n".join(
            "    - `{}={}` covers {}".format(rel_, wi, ", ".join(ids))
            for rel_, ids in sorted(accepts.items())
        )
        or NONE_OWED,
    }, None


def compose_act(root, verdict, wi, prompt_templates=None):
    """`(act brief, None)` filled IN FULL from the act the verdict still owes
    at HEAD, or `(None, reason)`; an operator override under `ADJUDICATE-ACT`
    wins over the shipped template, and a `PromptError` is a refusal.

    Implements: SR-231, LLR-338"""
    values, why = act_values(root, verdict, wi)
    if values is None:
        return None, why
    key = prompts.ADJUDICATE_ACT
    try:
        base = (prompt_templates or {}).get(key) or prompts.load(key)
        return prompts.fill(key, base, values), None
    except prompts.PromptError as exc:
        return None, str(exc)
