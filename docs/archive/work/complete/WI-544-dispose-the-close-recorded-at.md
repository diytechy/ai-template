+++
id = "WI-544"
title = "dispose: the close recorded at docs/handbacks/WI-484-wi484-concern-refs-component-view.md - cancel / defer / draft a successor / surface an open item (a disposition row never closes early; R3)"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "disposition"
+++

## Deliverable

The close of `WI-484` recorded at
`docs/handbacks/WI-484-wi484-concern-refs-component-view.md` is adjudicated
**PARTIAL — claim upheld; keep/discard split honest (the two in-range commits
are docs-only bookkeeping, nothing shippable either way); one successor
drafted** (the `## Dispositions` block below, `supersedes = "WI-484"`, which
intake mints at this row's merge). The adjudication
(`docs/reviews/wi-544-dispose-the-close-recorded-at/001-ADJUDICATE-a6a6748.md`,
`451e198a`, ANTHROPIC-OPUS) found the lane delivered none of the drafting the
owner's **Delegated for the unattended run** section assigned — it read a
branch spec the delegation had not reached and re-derived the residue as
owner-gated — so the successor's scope is exactly items 3 and 5 of that
section: the `knowledge` value-pass into `docs/requirements/hats.toml`
(re-pointing to existing `docs/knowledge/` packs where one carries the
perspective, drafting only where none does, each marked draft) and the 17
approved-cell `Rationale` attribution deletions, both under ordinary review.
Item 7 (which traced cells are staleness-bearing) is a classification ruling
owed by nobody and is deliberately excluded. This row's own move to
`complete/` is the supervising session's act under the delegated run
(decision 21 of `docs/decisions-for-review-2026-08-31.md`: no machinery
closes an adjudication row).

## Context

The closed spec is `docs/work/partial/WI-484-concern-refs-component-view.md`.

Its per-close report is `docs/handbacks/WI-484-wi484-concern-refs-component-view.md` — READ IT FIRST. The report is the close EVENT's own immutable record: what the lane claims it delivered and did not, the commit range, the keep/discard split, and the review tier it suggests. The lane's claimed outcome is a CLAIM under judgement here, not this row's premise.

Outcomes (R3): cancel / defer / draft a successor / surface an open item. Continuing the work MINTS A SUCCESSOR (drafted in THIS row's `## Dispositions` section, carrying `supersedes`), never a revival of the closed row — a closed row is never re-opened and a scope definition never changes to mean something else. An override moves the byte-identical spec to the corrected terminal folder; the report stays on record as the claim it was. An open item goes to docs/requirements/open-items.toml.

## Dispositions

Transcribed by the supervising session from the adjudication's own draft
(`docs/reviews/wi-544-dispose-the-close-recorded-at/001-ADJUDICATE-a6a6748.md`,
`451e198a`): the adjudicator wrote the block into its verdict file rather than
this section, under a `[disposition]` table header intake refuses as an unknown
key, with a title over the 120-character rule. Cells verbatim; the title
shortened to the rule; nothing else changed.

```toml
title = "WI-484 delegated residue: the hats.toml knowledge value-pass and the 17 approved-cell Rationale attribution deletions"
workstream = "requirements"
buildtier = "medium"
supersedes = "WI-484"
specref = "docs/requirements/open-items.toml#OI-32"
safety_class = "spine"
priority = 2
planmode = "single"
```

Scope of the successor is items **3 and 5 only** of `WI-484`'s "Delegated for
the unattended run" section — the `knowledge` value-pass into
`docs/requirements/hats.toml` (re-pointing to existing `docs/knowledge/` packs
where one carries the perspective, drafting only where none does, each marked
draft) and the 17 approved-cell `Rationale` attribution deletions, both listed
for the owner in a re-attestation fragment. Item 7 (which traced cells are
staleness-bearing) is a classification ruling owed by nobody and is excluded.
