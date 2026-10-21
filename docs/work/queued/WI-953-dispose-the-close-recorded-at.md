+++
id = "WI-953"
title = "dispose: the close recorded at docs/handbacks/WI-902-wi-902.md - cancel / defer / draft a successor / surface an open item (a disposition row never closes early; R3)"
workstream = "process"
specref = "docs/work/partial/WI-902-disposition-adopts-existing-successor.md"
buildtier = "medium"
safety_class = "adjudication"
brief = "disposition"
+++

## Context

The closed spec is `docs/work/partial/WI-902-disposition-adopts-existing-successor.md`.

Its per-close report is `docs/handbacks/WI-902-wi-902.md` — READ IT FIRST. The report is the close EVENT's own immutable record: what the lane claims it delivered and did not, the commit range, the keep/discard split, and the review tier it suggests. The lane's claimed outcome is a CLAIM under judgement here, not this row's premise.

Outcomes (R3): cancel / defer / draft a successor / surface an open item. Continuing the work MINTS A SUCCESSOR (drafted in THIS row's `## Dispositions` section, carrying `supersedes`), never a revival of the closed row — a closed row is never re-opened and a scope definition never changes to mean something else. An override moves the byte-identical spec to the corrected terminal folder; the report stays on record as the claim it was. An open item goes to docs/requirements/open-items.toml.

## Owner route

Owner ruling in session (2026-10-20; coordinator-2026-10-20 D-008), on wi-902 D-011: the plan-cap FIX of sitting `docs/reviews/wi-902/016-ADJUDICATE-7ffa12c.md` (F1) is taken by a THIRD plan revision that carries the sitting's ruling (record admission admits the close's exact inbound relinks through `spec_move.exact_relink`; the record/request, parent-tree and close-shape validation and the peel unchanged; the real-close regression added), then ONE confirming critique in convergence stance over that revision, then the build. This sitting therefore drafts the successor (carrying `supersedes = "WI-902"`) on that route; it does not choose another. The partial lane's records (the plan, its revision, both critiques, the findings file and the verdict) are the successor's inputs.
