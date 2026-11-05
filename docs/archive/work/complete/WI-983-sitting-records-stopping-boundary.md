+++
id = "WI-983"
title = "A decomposition round's sitting brief names a stopping-boundary line, so the verdict states why each retained chain stops"
workstream = "process"
sr_refs = ["SR-186", "SR-161"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 5
planmode = "single"
+++

## Deliverable

A decomposition round's sitting brief now asks the verdict for one named
stopping-boundary line per retained chain, beside the hat outcome lines,
stating why further splitting would only paraphrase or duplicate. A round with
no roster or no applicable hat still carries it, a sitting that is no round
carries none, and a combined sitting carries it once and says which section
takes its lines. The line rules no row and no check reads it. Both shipped
sitting templates are pinned by test. LLR-360 and TC-399 state it and cite
SR-186, re-attested at act seq 173. WI-998, the re-inspection row, was filed
before this claim and stays off the queue until a sample exists.

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

**Deliverables and order (S1).** Two deliverables, and they cannot stay one
row. The brief change, its test and the RESYNC entry land first, in this
row. The TC-211 re-inspection follows in a second row, filed on trunk
before this row's claim, because it cannot finish in this lane. This lane's
own sitting is no round: its spine change amends design and test rows, and
no SR is Drafted today. A round elsewhere composes from trunk, which gets
the line only when this lane lands. Kept whole, the row could not close
and no record could carry the line while it waited.

**The re-inspection row, WI-998.** It `needs` this row and stays off the queue
table until a sample exists. Its sample is the first round composed after
this row's landing whose brief is committed beside its verdict. In order:
amend TC-211's `inputs` to name that brief and verdict, through the
existing amendment route (the cell is approved, and the observation writer
never writes the registry); a fresh session that wrote none of the sample
inspects it; the result goes in the procedure's result section; the
observation writer records it last. The writer digests the declared inputs
as they stand and the procedure file is one of them, so a record written
earlier would anchor to the old sample or go stale at once. TC-211's fail
stands as the observation of record until then.

**Which briefs carry the line (S3).** The set is the composer's existing
round classification, with no new classifier: a sitting that judges an SR
awaiting its first approval or an amended approved need, on either
composing route, alone or combined. A combined sitting carries it once, in
the perspectives part after its last section. A round with no roster or no
applicable hat still carries it, because SR-186's stopping decision rests
on no hat, so the line cannot live only in the hat outcome instruction,
which that case omits. The default: every other sitting, an SR amended
alone included, keeps its existing behaviour; a template that declares no
perspective slot composes unchanged; a roster that cannot be read still
refuses. The promise reaches the briefs the kit's routes compose (PROCESS.md
§6, "Review threat model"). The line asks and nothing checks: a missing
reason is a finding for the review of the verdict.

**Architectural delta (S5).** No new mode class, no new boundary and no new
authority. The one change in CMP-008's brief and review boundary is added
content: the round's block gains the named line, and the verdict gains a
stopping reason per retained chain. Like a hat outcome line, that reason
is neither a row ruling nor a machine line, so a verdict parses to the
same rulings with or without it.

## Done-when

- [x] A decomposition round's sitting brief carries a named
      stopping-boundary line beside the hat outcome lines, asking the
      verdict to state, for each retained chain, why further splitting
      would only paraphrase or duplicate, for the set "Which briefs carry
      the line" closes.
- [x] A test pins that the shipped sitting templates carry it.
- [x] WI-998, the re-inspection row, is filed on trunk before this row is claimed,
      and carries the steps and order "The re-inspection row" states.
- [x] One RESYNC entry; the commit bar is green, and both strict lints
      are clean on the landing tip.

## Critique dispositions

Round 1 (fresh Sol, 2026-11-04): CHANGES-REQUESTED, two MAJORs and two
MINORs.

- **S1, adopted.** The Context now reads "The brief change, its test and
  the RESYNC entry land first, in this row", and answers the one-row
  question: "Two deliverables, and they cannot stay one row". The title
  and the third Done-when bullet follow, and the bullet reads "filed on
  trunk before this row is claimed".
- **S3, adopted.** "Which briefs carry the line" reads "The set is the
  composer's existing round classification, with no new classifier", its
  default reads "every other sitting, an SR amended alone included, keeps
  its existing behaviour", and its bound reads "The promise reaches the
  briefs the kit's routes compose". No refusal is added.
- **S4, adopted.** The frontmatter reads `planmode = "single"`: the row
  promises behaviour over the round classification.
- **S5, adopted.** The delta reads "No new mode class, no new boundary and
  no new authority". The input change is carried into the re-inspection
  row, whose order reads "amend TC-211's `inputs` to name that brief and
  verdict", ahead of "the observation writer records it last".
