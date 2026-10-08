+++
id = "WI-812"
title = "The spine-authoring flow: an author drafts the change set, the adjudicator judges it"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-spine-authoring"
needs = ["WI-809", "WI-802", "WI-810", "WI-850", "WI-854"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04) as S788-spine-authoring (ch.4 §7, §11; OI-101 Q1).

**Re-scoped 2026-10-07 by the owner's ruling** (docs/log.d/2026-10-07-wi841-retro-owner-rulings.md,
ruling 10): "Terra or another generic author does the first authoring pass; the
adjudicator passes judgement." This replaces the design's "the adjudicator drafts
spine text (or adopts the builder's), the adjudication reviewer edits it, and the
act is the adjudicator's unchanged final pass" (README change 4 and change 14;
OI-101 Q1's drafting half). One authoring model now serves every mode of spine
growth (ruling 3): an author drafts, an independent adjudicator judges. B10's
non-mutating-final-pass exception to the independence rule (D-022) existed only
because the adjudicator drafted; with no drafting judge, it retires. Code
findings still return to the builder (D-017).

In this repository the author role is GPT Terra; the role is declared, not the
model. The in-lane change set the author drafts is the one the `spine-authoring`
skill describes: anchored, closed, judged in one sitting.

## Done-when

- The first authoring pass on in-lane spine text (new rows and amendments) is an
  author session's, never the adjudicator's. The adjudicator judges and takes the
  act, and edits no cell of a row it judges.
- A RETURN goes back to the author with its findings; the author's revision is
  judged again. A fourth return of the same set is refused, and its rows are
  minted unsettled.
- No session judges text it authored: B10's exception (D-022) is retired in
  routing, session reuse and act admission alike.
- A sitting is composed only for a closed set: every row's parent is in the set
  or Approved, each TC cites its LLR and that LLR's SR, and each changed interface
  row has a citing TC. An open set is refused before the sitting, naming the
  missing edge.
- With the two-family pool, the author and the adjudicator each have an eligible
  draw, from different families (ch.2 §3 step 2 as amended by README A1).
- `prompts/adjudicate-amendment.template.md` and
  `prompts/adjudicate-first-approval.template.md` state the split: the judge never
  amends the row it judges, and a RETURN goes to the author.
- The README matrix names no spine row for this row; any it amends or adds passes
  in-lane adjudication.
- The row's test bar: its affected modules' tests (prompts and range rules) plus
  the smoke tier at `-n 2`; no extra bar is named.
- Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
- RESYNC_PACK: an entry anchored at a trunk commit; the shipped adjudicate prompts
  change.
