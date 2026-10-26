+++
id = "WI-983"
title = "A decomposition round's sitting brief names a stopping-boundary line, so the verdict states why each retained chain stops, and TC-211 is re-inspected on the first record that carries it"
workstream = "process"
sr_refs = ["SR-186", "SR-161"]
specref = "docs/reviews/wi-976/021-ADJUDICATE-095bb79.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Context

Filed by hand by headless leg 23 (2026-10-26) at WI-976's landing, from
the SUCCESSOR ruling of WI-976's dispute sitting 021
(`docs/reviews/wi-976/021-ADJUDICATE-095bb79.md`, F1, accepted).

What is true: TC-211's re-judge (`docs/reviews/wi-976/019-REJUDGE-28a0309.md`)
recorded a fail (`docs/test/observations/TC-211.2026-10-26T071924Z.toml`):
the sample verdict, WI-976's sitting 016, names every applicable hat's
outcome but records no reason why further splitting of the retained chain
stops, though its brief asks for one (SR-186's stopping-boundary
criterion; the proportionality rubric's R2). The sitting found the
omission systemic: four whole-set verdicts in that lane left it out,
because the verdict's stated form (one line per row, the machine line,
one line per hat) has no place for a chain's stopping reason.

The ruling, verbatim: "give a decomposition round's sitting brief a named
stopping-boundary line, beside the hat outcome lines, that asks the
verdict to state for each retained chain why further splitting would only
paraphrase or duplicate, test that the shipped templates carry it, and
re-inspect TC-211 against the first completed round whose record carries
it, recording the observation".

The change touches the shipped sitting templates and the composer's round
block, so every adopter's briefs: it owes a RESYNC entry. Its scope
critique runs before its claim (the `coordinator-cycle` skill, section 1).

## Done-when

- [ ] A decomposition round's sitting brief carries a named
      stopping-boundary line beside the hat outcome lines, asking the
      verdict to state, for each retained chain, why further splitting
      would only paraphrase or duplicate.
- [ ] A test pins that the shipped sitting templates carry it.
- [ ] TC-211 is re-inspected, by a fresh session that wrote none of the
      sample, against the first completed round whose record carries the
      line, and its result is recorded through the observation writer
      and in the procedure's result section.
- [ ] One RESYNC entry; the commit bar is green, and both strict lints
      are clean on the landing tip.
