+++
id = "WI-1069"
title = "A sitting is shown each routed link change: the acceptance model and amendment brief carry it, link-only rows too"
workstream = "process"
specref = "docs/plans/WI-1024/plan.md"
sr_refs = ["SR-146", "SR-178"]
needs = []
buildtier = "medium"
planmode = "single"
safety_class = "ordinary"
priority = 2
+++

## Context

Filed on trunk on 2026-11-23 by the queue drill's coordinator, while
preparing WI-1024's sitting A (WI-1068). A routed traced cell (a
requirement's needs and boundary crossings, a design row's requirements, a
test case's verified rows and, since WI-1024, a requirement's or design
row's `constrains` link) is classed traced because it carries no prose, and
routed because whether the move changed what the row claims is a sitting's
judgement (`acceptance_record.SPINE_TRACED_CELLS`' comments; WI-1024's
plan, the specref: "Silent, the whole population would land unjudged").
The record keeps such a row at its recorded copy until an act names it
(WI-1060). But no sitting is shown the change:

- **The amendment brief renders accepted cells only**
  (`amendment_brief._scoped_chain_rows` keeps `c[0] in accepted`). Its
  docstring says traced cells are excluded because the classification
  "already answers" them, which predates routing: it is true of a silent
  traced cell, not a routed one. So sitting A would judge LLR-010's
  amended `detail` without being shown that the row now constrains IF-014,
  and blessing it would copy the link into the record unjudged.
- **A row whose only change is a routed link is in no surface.** The
  acceptance model (`trace.reaccept_model`) does not select LLR-017,
  LLR-022 or LLR-024, whose only change is a `constrains` link: they are
  absent from `docs/ratify/CURRENT.md`, `open-items.html` and the brief,
  while the snapshot prints them LEFT OWED and the act ledger lists them
  `kept`. A combined brief naming them as `amendment:` tokens drops them
  silently. Two answers to "what is owed" disagree.

Measured on trunk at `3f887ec5d`: 21 routed `constrains` changes owed by
WI-1024's slice 1, three of them on link-only rows; the model carries
LLR-010's `Constrains` triple but marks only `Detail` accepted.

Critiqued 2026-11-23 (Sol and Hydrogen;
`docs/reviews/2026-11-23-scope-critiques/WI-1069.md`): a `## Trust` section,
the deliverables kept together with the reason, and a coverage bound.

## Done-when

- [ ] The acceptance model selects a row whose routed traced cell differs
      from its recorded copy, even when no accepted cell moved, and the
      operator surfaces built on it (the acceptance brief, `open-items.html`)
      list it as owed, naming the link that moved. A silent traced cell
      still selects nothing.
- [ ] The amendment brief shows, for each row in its scope, every routed
      link that moved (before and after, by the cell's contract name)
      beside its accepted cells, and a row whose only change is a routed
      link is shown, not dropped; the question it asks of a link is the
      one the routing exists for (does the row's text state what it now
      points at?). The verdict's row grammar is unchanged.
- [ ] The binding's judged-text identity covers what the brief showed, so
      a link changed after the verdict is not taken under it (`## Trust`
      below); the plan says how, from the code.
- [ ] A brief scope naming a row with nothing to judge, accepted or routed,
      still refuses by name; a combined brief no longer drops a scoped
      row silently.
- [ ] Coverage bound: the promises reach registries, records and bindings
      as supported workflows and the kit's own routes write them;
      hand-edited kit-written state (a record copy, a ledger, a binding) is
      outside them (PROCESS.md §6, "Review threat model").
- [ ] Tests, red first, over a fixture with an accepted-text-only row, a
      routed-link-only row and a row with both, through the model, the
      operator surfaces and the amendment brief; the rows the change
      re-cuts (SR-146's and SR-178's design rows that say accepted cells
      only, LLR-167 and any the plan finds) are amended in text and owed
      to a sitting; a RESYNC entry.

## Trust

PROCESS.md §3, "When a guard is owed". Done-when 3 widens what a verdict's
binding identifies, and the binding decides whether an act may take a row
on a held rung, so the file's authority is stated here.

- **Producer.** The binding beside a verdict (`<verdict>.requested`),
  written when a sitting's request is bound (`adjudicate_brief.bind_pending`,
  `coordinator_adjudicate.bind_requested`), records one judged-text
  identity per row the composed brief shows (the brief's `JUDGED-TEXT:`
  lines, read back by `kitlib.sitting.recorded_identities`). Today an
  identity digests a row's accepted cells; this row extends it to the
  routed links the brief shows.
- **A failed or missing write.** A binding absent, unreadable, carrying no
  identity, not naming the row, or naming another digest than the
  committed row's: each consumer fails closed, as today. The held act's
  derivation refuses naming the row and both digests; the held-status
  exception reads the claim as not excepted; the record's kept-row reading
  does not count the row as settled.
- **Consumers, by path, and their shared ruling.** `adjudicate_act.py`
  (`_unbound_text`, the held re-accept), `held_status.py` (`_excepted`, a
  held CLARITY re-acceptance claim) and `acceptance_record.py` (the ruled
  rows a held verdict keeps). Each takes a row under a verdict only while
  the committed row's identity equals the bound one; one identity function
  serves all three, so a link changed after the verdict reads as changed
  text in every one. Released rungs and taken acts read no identity, as
  today.

## Scope answers

- **Kept together.** The model and surface change and the brief and
  binding change are one row on purpose: the brief reads the model, the
  binding digests what the brief shows, and one fixture (accepted-only,
  link-only, both) drives all three; landed apart, the first would list
  link-only rows that no brief could show.
- **Not in scope:** what a verdict on a routed link authorizes (the act
  already records a named row whole from live); the first-acceptance brief
  (a `Drafted` row shows every cell already).
- **Order.** WI-1068 (sitting A) waits on this row: its 21 routed links are
  the case that found it.
