+++
id = "WI-1059"
title = "A derived act holds back a first-acceptance flip whose parent stays Drafted, instead of listing one the hook refuses"
workstream = "process"
specref = "docs/archive/work/complete/WI-1057-adjudicate-fourth-sitting.md"
sr_refs = ["SR-231"]
needs = []
buildtier = "medium"
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

## Done-when

- [ ] The derived act holds back each first-acceptance flip whose parent
      (a design row's system requirement, a test case's verified rows) is
      neither already accepted nor flipped by the same act. The brief names
      each held row and the parent it waits on, and part 2 lists only rows
      the parent-first rule accepts.
- [ ] A test derives an act from a verdict that accepts a child and
      returns its parent. The child is held and named, and the brief's
      flips, once taken, pass the parent-first check. A second test accepts
      the parent in the same act and shows the child listed.
- [ ] Once the parent is accepted, the same verdict's act lists the held
      flip; a test shows it.
- [ ] Any accepted row text this changes is listed as owed to adjudication.
      No text it writes names a code file, function, symbol or flag.
