#!/usr/bin/env python3
"""adjudicate_act.py — the ACT a committed, accepted verdict still owes, and
the act brief filled from it.

Stack-agnostic, standard-library only (Python 3.11+, Windows/POSIX).

WHY THIS MODULE EXISTS (WI-912). A sitting used to judge and act in one turn:
the brief that asked for the judgement also ordered the `Status` flips and the
anchoring copy. So a sitting held ahead of landing order that followed its
brief took its act out of order. The owner's rulings split the two (revision
31 of the review-churn plan: verdicts move between lanes while acts keep
landing order; revision 32: the act is a later turn of the retained
adjudicator, run fresh where retention lapsed; revision 36: the split reaches
the shipped briefs and the coordinator's entry point). Q1 of
coordinator-2026-10-14 D-003 makes the act turn an adjudicator turn with its
own brief, since OI-45 (b) keeps scripted approval retired; Q2 makes a MEANING
row's blessing a typed mark on the verdict, `[MEANING+BLESS]`.

THE CARRIER. The verdict and the binding beside it, as committed at the lane's
HEAD, read through `kitlib.sitting.accepted_at`, the one reader every consumer
of a verdict goes through. After the split that committed verdict is the act
turn's whole authority: the session that wrote it may be gone, and a fresh act
turn takes the same act. The other consumers of the same carrier are
unchanged: the merge slot (`kitlib.sitting.uncovered_refusal` and
`unaccepted_refusal`, `acceptance_record.held_reattest_refusal`) still admits
an act only when an accepted verdict over the act's own rows backs it (owner
ruling 6, 2026-10-07), and `intake.py snapshot --verdict` still records the
verdict a held-rung re-attestation names.

WHAT THE VERDICT AUTHORIZES. Exactly the rows each accepted part rules to
authorize them, read through `kitlib.sitting.judged_rows`, the one reader the
merge's backing check also reads, so the two cannot disagree. A first-approval
part's APPROVE flips a row, on a released rung only (a dial the owner
tightened after the sitting binds the act it has not yet authorized). An amendment part's CLARITY re-attests a row, naming the
verdict on a held rung; its MEANING re-attests only on a released rung and
only with the bless mark. A RETURN row, an unmarked or held MEANING row, a
Done-when part and every brief class but amendment, first-approval and
combined owe no act. The dial is read at the act, from the committed tree, and
each rung's arm is `intake.adjudication_action`'s answer (the held-rung
policy's one home, which the judging composer reads too).

OWED, TAKEN OR INCONSISTENT: judged at a revision, never the working tree. A
first approval is owed while the row's committed status is below Approved,
whatever its recorded copy holds (a whole-registry copy carries Drafted rows),
and taken when the row is Approved and its copy equals its committed text. A
re-attest of an Approved row is taken when the copy equals the row, and owed
otherwise. A re-attest of a row absent from the committed registries is a
RETIREMENT (the owner's ruling of 2026-10-17, WI-912): owed while its recorded
copy still holds the row, named in `--reattests` with the other re-attests
(the snapshot writer clears a recorded row the live registry no longer holds
only when it is named there), and taken once the copy no longer holds it. On a
held rung a retirement owes no act, read through the same held-rung test as a
held MEANING or APPROVE row: removing a held row is the owner's. Every other
state (an Approved row without an equal copy at a first approval, a first
approval of an absent row, a re-attest of a row below Approved, a row no
compared tier holds) is inconsistent and refuses the whole derivation, naming
the row: it is never counted as taken. "Equal" compares the whole parsed row, Status included,
which is what makes a flip committed without its copy read as inconsistent.

ALL OR NOTHING, as `adjudicate_brief`'s rule 2 states: every call returns
`(value, None)` or `(None, reason)`, never a partial act and never a brief
with a hole in it.

Contracts: IF-296 — the seam this module declares (process.md §8; row of record
in docs/requirements/interfaces.toml).

Contract IF-296: the act assembler's call surface, which the coordinator's
entry point consumes.
    `owed_acts(root, verdict, rev="HEAD")` returns `(acts, None)`, where
    `acts` is `{"amendment": {"reattests": [ids], "verdict": bool},
    "first-approval": {"approves": {registry: [ids]}}}` in that order, each
    part present only when something is owed there, the amendment part also
    carrying `"retires": [ids]`, the re-attested ids absent from the committed
    registries, only when one is owed, or `(None, reason)` for
    a verdict that is not committed at `rev`, has no binding there, records
    a pending or failed outcome, is not valid against its binding, is of a
    class that owes no act, owes no act, or judged a row whose committed
    state is inconsistent (named); `act_values(root, verdict, wi,
    rev="HEAD")` is the act brief's slot values from it, and
    `compose_act(root, verdict, wi, prompt_templates=None)` the act brief
    filled from them at HEAD, an operator override under `ADJUDICATE-ACT`
    winning, or `(None, reason)`; `left_owed(root, verdict, rev="HEAD")` is
    None when `rev` carries every act the verdict authorizes in full, else
    the acts still owed there or the derivation's refusal, and
    `bound_brief(root, verdict, rev="HEAD")` the brief class an accepted,
    actable verdict's binding records, or None. Reads git and the shipped
    template only; writes nothing.
"""

from __future__ import annotations

from pathlib import Path

import acceptance_record
import baseline_snapshot
import intake
import prompts
from kitlib import authority as kauthority
from kitlib import sitting as ksitting
from kitlib import spine as kspine
from kitlib.git import git_out

# The brief classes whose verdict can authorize an act: the one home of the
# set, which `adjudicate_brief` also reads to decide which retained sessions'
# identity covers the act brief.
ACTABLE = ("amendment", "first-approval", ksitting.SITTING)
# A part of the act that nothing is owed for: a state the derivation reports,
# never a default a missing value falls back to.
NONE_OWED = "none owed"
# A judged row's state when its ruling authorizes no act on it: a retirement
# on a held rung.
NO_ACT = "no act"
# The act a re-attest of a row absent from the committed registries is.
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


def _unaccepted_reason(root, rev, rel):
    """Why the verdict at `rel` is not accepted at `rev`, read off the files
    `accepted_at` read; only ever asked once that reader returned None.

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
    if outcome != "accepted":
        return "the verdict {}'s binding records the outcome {}, not accepted".format(
            rel, outcome
        )
    why = ksitting.parse(text, brief, kinds, rel)[1] or "it does not parse"
    return "the verdict {} is not a valid {} verdict: {}".format(rel, brief, why)


def _accepted(root, rev, rel):
    """`(brief class, {kind: part})` for an accepted verdict of an actable
    class, or `(None, reason)`.

    Implements: SR-231, SR-232, LLR-338"""
    binding = git_out(root, ["show", "{}:{}".format(rev, ksitting.requested_path(rel))])
    bound = ksitting.read_requested(binding) if binding else None
    if bound and bound[0] not in ACTABLE:
        return None, "a {} verdict owes no act; only {} verdicts do".format(
            bound[0], ", ".join(ACTABLE)
        )
    parsed = ksitting.accepted_at(root, rev, rel)
    if not parsed:
        return None, _unaccepted_reason(root, rev, rel)
    return (bound[0], parsed), None


def _tier(rid):
    """`(registry, id column)` of the compared tier holding row `rid`, read off
    its prefix, or None."""
    for rel, id_col in baseline_snapshot.SNAPSHOT_TIERS:
        if rid.startswith(id_col[: -len("ID")]):
            return rel, id_col
    return None


def _held(dial, rid):
    """Does the dial hold the rung row `rid`'s status cell is approved into?
    A row no compared tier holds is held, the direction every unknown fails."""
    tier = _tier(rid)
    return kauthority.holds_under(dial, kauthority.rung_for(tier[0])) if tier else True


def _arm(ruling, held):
    """The act one authorized row's ruling owes on its rung: "approve",
    "reattest" or None. The rung's arm is `intake.adjudication_action`'s
    answer, the held-rung policy's one home, never restated here: "recommend"
    owes no act, "reattest" is the re-attest a held CLARITY row owes, and
    "flip" is the act itself, a flip for an APPROVE row and a re-attest for an
    amendment row. A RETURN row, or any ruling that is not an approval or an
    amendment ruling, owes none.

    Implements: SR-231, SR-232, LLR-338"""
    if ruling not in ("APPROVE", "CLARITY", "MEANING"):
        return None
    if intake.adjudication_action(held, ruling) == "recommend":
        return None
    return "approve" if ruling == "APPROVE" else "reattest"


def _authorized(parts, dial):
    """`[(act, row id, held)]` every accepted part authorizes, `act` being
    "approve" or "reattest", amendment first, in verdict order within a kind.
    Which rows a part authorizes is `kitlib.sitting.judged_rows`'s answer (a
    MEANING row only with its bless mark), the reader the merge's backing
    check also reads; each such row's act is `_arm`'s.

    Implements: SR-231, SR-232, LLR-338"""
    judged = ksitting.judged_rows(parts)
    out = []
    for kind in ("amendment", "first-approval"):
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


# Whether a row's `Status` claims approval (`Approved` or `Founded`): the pair's
# one home is `kitlib.spine.claims_approval`, which the acceptance record's
# approval-act readers and the parent-first rule read too.
_claims_approval = kspine.claims_approval


def _retirement(act, rid, held, recorded):
    """The state of a judged row absent from the committed registries: a
    re-attest is a retirement, owed while the copy still holds the row
    (`recorded`) and taken once it does not, and owes no act on a held rung;
    a first approval of an absent row is inconsistent.

    Implements: SR-231, SR-232, LLR-338"""
    if act != "reattest":
        return None, _odd(rid, "absent", False)
    if held:
        return NO_ACT, None
    return (RETIRE if recorded else "taken"), None


def _state(rows, act, rid, held):
    """`("owed" | RETIRE | "taken" | NO_ACT, None)` for one authorized row,
    or `(None, why)` when its committed state is inconsistent with the act.

    Implements: SR-231, SR-232, LLR-338"""
    tier = _tier(rid)
    if tier is None:
        return None, "{} is held by no compared tier".format(rid)
    live, copy = rows.pair(*tier)
    row = live.get(rid)
    if row is None:
        return _retirement(act, rid, held, rid in copy)
    approved, equal = _claims_approval(row), copy.get(rid) == row
    if act == "approve" and not approved:
        return "owed", None
    if approved and equal:
        return "taken", None
    if approved and act == "reattest":
        return "owed", None
    return None, _odd(rid, row.get("Status") or "(empty)", equal)


def _odd(rid, status, equal):
    """The inconsistent-row line, naming its status and its copy."""
    return "{} is inconsistent: its committed status is {} and its recorded copy {}".format(
        rid, status, "equals it" if equal else "does not equal it"
    )


def _derive(root, verdict, rev):
    """`(rel, authorized, owed, None)` for the verdict at `verdict` judged at
    the commit `rev`, or `(rel, None, None, reason)` when it is refused: not
    accepted there, of a class that owes no act, or a judged row in a state
    no act explains.

    Implements: SR-231, SR-232, LLR-338"""
    rel = _verdict_rel(root, verdict)
    if not rel:
        return None, None, None, "the verdict {} lies outside {}".format(verdict, root)
    found, why = _accepted(root, rev, rel)
    if found is None:
        return rel, None, None, why
    rows, authorized, owed = _Rows(root, rev), [], []
    for act, rid, held in _authorized(found[1], kauthority.dial_at(root, rev)):
        state, why = _state(rows, act, rid, held)
        if state is None:
            return rel, None, None, "the verdict {} judged a row {}".format(rel, why)
        if state == NO_ACT:
            continue
        authorized.append((act, rid, held))
        if state in ("owed", RETIRE):
            owed.append((RETIRE if state == RETIRE else act, rid, held))
    return rel, authorized, owed, None


def owed_acts(root, verdict, rev="HEAD"):
    """`(acts, None)`: every act the verdict at `verdict` authorizes that the
    commit `rev` does not yet carry in full, or `(None, reason)` (the module
    docstring's partition and refusals).

    Implements: SR-231, SR-232, LLR-338"""
    rel, authorized, owed, why = _derive(root, verdict, rev)
    if why:
        return None, why
    if any(act == "approve" for act, _rid, _held in owed) and not _recorded(root, rev):
        return None, (
            "the verdict {} approves rows, but no approval record exists at {}: "
            "the first signing creates it, and that is the owner's".format(rel, rev)
        )
    if not owed:
        return None, "the verdict {} owes no act: {}".format(
            rel,
            "every act it authorizes is taken at {}".format(rev)
            if authorized
            else "it authorizes none",
        )
    return _grouped(owed), None


def left_owed(root, verdict, rev="HEAD"):
    """None when the commit `rev` carries in full every act the verdict at
    `verdict` authorizes; else why not: the acts still owed there, named, or
    the derivation's refusal. What the act turn asks after its call.

    Implements: SR-231, SR-232, LLR-338"""
    _rel, _authorized, owed, why = _derive(root, verdict, rev)
    if why:
        return why
    if not owed:
        return None
    parts = _grouped(owed)
    named = []
    if "amendment" in parts:
        named.append("re-attest " + ", ".join(parts["amendment"]["reattests"]))
    for rel, ids in sorted(parts.get("first-approval", {}).get("approves", {}).items()):
        named.append("flip {} ({})".format(", ".join(ids), rel))
    return "; ".join(named)


def bound_brief(root, verdict, rev="HEAD"):
    """The brief class the binding beside an accepted, actable verdict
    records at `rev`, or None: what the act turn's keep is planned by.

    Implements: SR-231, LLR-338"""
    rel = _verdict_rel(root, verdict)
    found = _accepted(root, rev, rel)[0] if rel else None
    return found[0] if found else None


def _recorded(root, rev):
    """Does the commit `rev` carry the approval record's directory?"""
    kind = git_out(
        root, ["cat-file", "-t", "{}:{}".format(rev, baseline_snapshot.SNAPSHOT_DIR)]
    )
    return (kind or "").strip() == "tree"


def _grouped(owed):
    """The owed rows as `owed_acts`' `acts` mapping, amendment first."""
    acts = {}
    amendment = [entry for entry in owed if entry[0] != "approve"]
    if amendment:
        acts["amendment"] = {
            "reattests": [rid for _act, rid, _held in amendment],
            "verdict": any(held for _act, _rid, held in amendment),
        }
        retires = [rid for act, rid, _held in amendment if act == RETIRE]
        if retires:
            acts["amendment"]["retires"] = retires
    approves = {}
    for act, rid, _held in owed:
        if act == "approve":
            approves.setdefault(_tier(rid)[0], []).append(rid)
    if approves:
        acts["first-approval"] = {"approves": approves}
    return acts


def _amendment_text(part, rel, wi):
    """The amendment act's rendered rows and command."""
    command = "python scripts/intake.py snapshot --reattests {}".format(
        ",".join(part["reattests"])
    )
    if part["verdict"]:
        command += " --verdict {}".format(rel)
    retires = part.get("retires") or []
    approved = [rid for rid in part["reattests"] if rid not in retires]
    rows = "Re-attest these Approved rows: {}.\n".format(", ".join(approved))
    if retires:
        rows = (rows if approved else "") + (
            "Retire these rows, which the lane deleted from their registries, "
            "from the recorded copy (leave them deleted): {}.\n".format(
                ", ".join(retires)
            )
        )
    return (
        "{}Run, then commit the copy it writes, ending the commit with "
        "`WI: {}`:\n\n    {}".format(rows, wi, command)
    )


def _approval_text(approves, registries, wi):
    """The first-approval act's rendered rows and command."""
    rows = ", ".join(
        "{} ({})".format(rid, rel) for rel in sorted(approves) for rid in approves[rel]
    )
    return (
        "Flip `Status` from `Drafted` to `Approved` for exactly these rows: {}.\n"
        "Then run, and commit the flips and the copy together, ending the commit "
        'with `WI: {}`:\n\n    python scripts/intake.py snapshot --approves "{}"'.format(
            rows, wi, registries
        )
    )


def act_values(root, verdict, wi, rev="HEAD"):
    """`({slot: value}, None)` for the act brief, or `(None, reason)`.

    Implements: SR-231, LLR-338"""
    acts, why = owed_acts(root, verdict, rev)
    if acts is None:
        return None, why
    rel = _verdict_rel(root, verdict)
    wi = str(wi or "").strip()
    if not wi:
        return None, "no work item was named for the act's commit trailer"
    amendment = acts.get("amendment")
    approves = (acts.get("first-approval") or {}).get("approves") or {}
    registries = baseline_snapshot.format_approves(dict.fromkeys(approves, wi))
    return {
        "verdict": rel,
        "wi": wi,
        "amendment_act": _amendment_text(amendment, rel, wi)
        if amendment
        else NONE_OWED,
        "approval_act": _approval_text(approves, registries, wi)
        if approves
        else NONE_OWED,
        "registries": registries or NONE_OWED,
        "approves_rows": "\n".join(
            "    - `{}={}` covers {}".format(rel_, wi, ", ".join(ids))
            for rel_, ids in sorted(approves.items())
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
