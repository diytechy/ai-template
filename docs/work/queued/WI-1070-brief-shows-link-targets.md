+++
id = "WI-1070"
title = "The amendment brief shows a linked row's own text and the row each moved link names, so a sitting can judge the link"
workstream = "process"
specref = "docs/reviews/wi-1068-adjudicate-eighth-sitting/001-ADJUDICATE-fbd50be.md"
sr_refs = ["SR-146", "SR-178"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Filed on trunk on 2026-11-24 by the queue drill's coordinator, to answer
the eighth automated adjudication sitting's verdict (WI-1068, sitting A,
Gemini Neon; the specref), its first `## amendment` disposition.

WI-1069 made the amendment brief show each moved routed link (before and
after, marked `(link)`) and a row whose only change is a link, and its
template asks of a link the question its routing exists for: "does the
row's text state what the link now points at?". The sitting could not
answer it. For each of the 21 rows gaining a `constrains` link it ruled
MEANING, not blessed, saying the brief supplies neither the interface the
link names nor, for a link-only row (LLR-017, LLR-022, LLR-024), the row's
own text. The coordinator confirmed it from the composed brief: the
amendment section lists moved cells only, so LLR-017 reads in full
"Constrains (link): before (empty), after IF-032". The same gap is why the
sitting did not bless LLR-167 (the brief's contract asks a question it does
not equip the judge to answer) and TC-161 (it verifies that contract).

All 21 rows, LLR-167 and TC-161 stay `Accepted` at their recorded text,
owed (the act `WI: WI-1068` left them owed). F-4's slices 2 to 4 add many
more `constrains` links; every one meets the same gap at its sitting
unless this row lands first.

## Done-when

- [ ] For each row in an amendment brief's scope with a moved routed link,
      the brief shows the row's current accepted text (every accepted cell,
      not only the moved ones), so a link-only row is judged against its own
      text.
- [ ] For each id a moved routed link names, before or after, the brief
      shows that row's identifying text (its title and the cell that states
      what it is: an interface's contract, a requirement's requirement, a
      design row's detail, a need's statement, a crossing's description), as
      context, not as text under judgement; an id that names no live row is
      shown as such. The plan settles, from the code, which cell each tier
      shows and the bound on its size.
- [ ] The binding's judged-text identity is unchanged in what it covers (a
      row's accepted cells and its routed links), or the plan argues a
      change under the `## Trust` section WI-1069 wrote; the brief says
      which shown text is context and not under the identity.
- [ ] LLR-167 and TC-161 state and verify the new contract (text only, no
      code names); any other row the plan finds saying the brief shows moved
      cells only is amended in text. Every amended row is owed to a sitting.
- [ ] Tests, red first, over a link-only row and a row with both, through
      the amendment brief and the combined brief; a RESYNC entry if a
      shipped file or template changes.
- [ ] The Deliverable measures the brief over WI-1068's 54 tokens before
      and after (characters), so the next sitting's split is known.

## Scope answers

- **Not in scope:** re-sitting the 21 rows (a sitting row filed when this
  lands, with WI-1071's rows); the first-acceptance brief, which already
  shows each row whole with its chain.
- **Order.** Lands before the sitting that re-judges WI-1068's link rows,
  and before any sitting judging F-4's later slices' links.
