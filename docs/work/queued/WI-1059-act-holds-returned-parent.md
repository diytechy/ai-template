+++
id = "WI-1059"
title = "A derived act holds back a first-acceptance flip whose parent stays Drafted, instead of listing one the hook refuses"
workstream = "process"
specref = "docs/archive/work/complete/WI-1057-adjudicate-fourth-sitting.md"
sr_refs = ["SR-231"]
needs = []
buildtier = "medium"
planmode = "single"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed on trunk on 2026-11-23 by the queue drill's coordinator, from the
fourth adjudication sitting's act (WI-1057, the specref).

The sitting ruled LLR-406 ACCEPT and returned its parent SR-251. The act
the kit derives from that verdict listed LLR-406's flip from `Drafted` to
`Accepted`. Taken as listed, the commit was refused by the hook's
parent-first step: "LLR-406 (Accepted) is accepted under SR-251 (Drafted),
which is not: accept SR-251 in its own acceptance act, or return LLR-406
to Drafted". The coordinator took the act without LLR-406.

So the act brief told its taker to do something the kit then refuses. A
taker that follows it to the letter fails at the commit. A taker that
improvises has to choose which listed row to leave out, which the brief
forbids ("take nothing that is not listed" says nothing of taking less).
The derivation and the parent-first rule read the same statuses but
disagree.

The fix belongs in the derivation, which already lists only what is still
owed. A first-acceptance flip whose parent would still not be accepted
after the act is held back and named in the brief: owed under the verdict
until the parent is accepted. The parent can be accepted by the same act
or already, and so is not held. Once the parent is accepted, the same
verdict's act lists the flip again. That is today's behaviour: WI-1057's
act lists LLR-406 and nothing else.

**The outcomes, settled at the scope critique** (coordinator, 2026-11-23):
- **A hold chains.** A flip whose parent is itself held is held too, since
  that parent will not be flipped by the act. A test case whose verified
  design row is held waits on that row.
- **Some flips held, some not.** The brief lists the takeable flips and
  names each held row with the parent it waits on.
- **Every owed flip held, and no other act owed.** There is nothing to take
  now. The derivation refuses, as it refuses a verdict owing no act, and
  its reason names each held row and its parent.
- **Completion is unchanged.** A held flip is work the verdict still owes.
  The later-act derivation keeps reporting it, marked held with its parent,
  so a coordinator act turn that leaves one does not read complete, and the
  verdict is not done until a later act takes it. SR-231's completion
  contract needs no amendment.

**Rows this changes.** LLR-338 (Accepted) states the derivation. Its text
gains the hold, and that amendment is owed to a sitting. Runtime Flow 6's
refusal branch names the all-held case. The plan confirms whether LLR-306's
act-report text needs the held marking too.

**Planning** is `single`: the hold reads parent statuses over the SR, LLR
and TC edges, with chains, and the plan settles where the hold is computed
so the brief and the later-act derivation read one answer.

## Trust

This row adds no authority. The derivation already reads each row's
committed status at the revision to tell an owed act from a taken one, and
the hold reads the parents' committed statuses the same way. Those come from
the registries as committed, written by supported routes. An unreadable or
unparseable registry already refuses the whole derivation. The consumers are
the act brief (`project-trajectory/scripts/adjudicate_act.py`), the
coordinator's act turn and its completion report
(`project-trajectory/scripts/coordinator_adjudicate.py`), and the person or
session that takes the act. The ruling they share: a hold only takes a flip
out of the act and never adds one, so a wrong hold leaves a flip owed and
reported, never lost. The commit hook's parent-first step stays the guard
against a flip listed wrongly. (PROCESS.md §3, "When a guard is owed".)

The promise reaches the states supported workflows and the kit's own routes
produce. Hand-edited kit-written state, such as a hand-edited verdict or
binding, is outside it (PROCESS.md §6, "Review threat model").

## Done-when

- [ ] The derived act holds back each first-acceptance flip whose parent
      (a design row's system requirement, a test case's verified rows) is
      neither already accepted nor flipped by the same act. The brief names
      each held row and the parent it waits on, and part 2 lists only rows
      the parent-first rule accepts. A hold chains through a held parent.
- [ ] A test derives an act from a verdict that accepts a child and
      returns its parent. The child is held and named, and the brief's
      flips, once taken, pass the parent-first check. A second test accepts
      the parent in the same act and shows the child listed. A third holds
      a test case under a held design row.
- [ ] A verdict whose only owed acts are held flips is refused, naming each
      held row and its parent. The later-act derivation reports a held flip
      as owed and marked held, never as taken; a test shows both.
- [ ] Once the parent is accepted, the same verdict's act lists the held
      flip; a test shows it.
- [ ] LLR-338's amendment (text only) and any other accepted row text this
      changes are listed in the Deliverable as owed to adjudication, and
      Flow 6 names the all-held refusal. No text it writes names a code
      file, function, symbol or flag.
