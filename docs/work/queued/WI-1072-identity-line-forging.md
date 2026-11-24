+++
id = "WI-1072"
title = "A row's own text cannot add or override a judged-text identity the binding records"
workstream = "process"
specref = "docs/plans/2026-11-21-queue-drill/HANDOFF.md"
sr_refs = ["SR-178"]
needs = ["WI-1070"]
buildtier = "medium"
safety_class = "ordinary"
priority = 3
planmode = "single"
+++

## Context

Filed on trunk on 2026-11-24 by the queue drill's coordinator, from
WI-1070's plan (its decision D12, found by its builder and left out of its
scope).

A sitting's binding records one judged-text identity per row its brief
shows for judgement: the brief's `JUDGED-TEXT: <row id> <digest>` lines,
read by one reader over the whole composed prompt (`adjudicate_brief`,
`requested_identities`: a multi-line match anywhere in the text, later
lines replacing earlier ones for the same id). The held act, the held-claim
exception and the record's kept-row reading each take a row only while the
committed row's identity equals the bound one (LLR-359; WI-1069's
`## Trust`).

The brief prints each judged cell verbatim, and a registry cell may span
lines. So a row whose own text holds a line shaped as an identity line
adds an identity the composer never wrote; where that line comes after the
genuine one (a combined prompt's first-acceptance section follows its
amendment section's identity lines), it replaces the genuine digest of the
row it names. A binding could then record a digest no shown text has, and
a held act could take a row whose text the verdict never judged. Registry
text is written by supported workflows (authoring and the kit's routes),
so this is inside the coverage bound PROCESS.md §6 ("Review threat model")
draws. WI-1070's new context listing collapses each listed cell to one
line and is tested against such a line; the rows' own cells are not.

**Order.** After WI-1070, which changes the same brief and template.

Critiqued 2026-11-24 (Sol and Hydrogen;
`docs/reviews/2026-11-24-scope-critiques/WI-1072.md`): `planmode` is
`single`, and the row carries a `## Trust` section.

## Trust

PROCESS.md §3, "When a guard is owed". The binding beside a verdict decides
whether an act may take a row on a held rung, so what enters it is
authority; this row narrows what enters it, and changes nothing else.

- **Producer.** Unchanged from WI-1069's `## Trust`
  (`docs/archive/work/complete/WI-1069-brief-shows-routed-links.md`): the
  binding is written when a sitting's request is bound, and records one
  judged-text identity per row the composed brief shows for judgement. This
  row adds that only the identity lines the composer itself writes for
  those rows enter it; text a judged cell carries never does.
- **A failed or missing write.** Unchanged: a binding absent, unreadable,
  carrying no identity, not naming the row, or naming another digest than
  the committed row's, fails closed in each consumer. A brief the plan's
  mechanism cannot compose safely is refused at compose, never bound with
  a guess.
- **Consumers.** Unchanged: the held act, the held-claim exception and the
  record's kept-row reading each take a row only while the committed row's
  identity equals the bound one, through the one identity function.

## Done-when

- [ ] The binding records only the identity lines the composer wrote for
      the rows it shows for judgement: a judged cell, in an amendment, a
      first-acceptance or a combined brief, holding a line shaped as an
      identity line neither adds an identity nor replaces one. The plan
      settles the mechanism (where the reader looks, or how a judged cell
      is rendered, or a refusal at compose), from the code.
- [ ] A test per brief kind drives a cell holding such a line naming its
      own row, another shown row and a row not shown, red first.
- [ ] LLR-359 states the rule in contract terms, no code names, if its
      text does not already cover it; any amended row is owed to a sitting.
- [ ] A RESYNC entry if a shipped file changes.
