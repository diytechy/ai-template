+++
id = "WI-894"
title = "dispose: the close recorded at docs/handbacks/WI-828-wi-828.md - cancel / defer / draft a successor / surface an open item (a disposition row never closes early; R3)"
workstream = "process"
specref = ""
buildtier = "quick"
safety_class = "adjudication"
brief = "disposition"
+++

## Deliverable

Closed by hand 2026-10-10, as the disposition verdict directs (`docs/reviews/wi-894/001-ADJUDICATE-3cd530b.md`): OUTCOME PARTIAL, no successor drafted. WI-828's partial close is confirmed (none of its Done-when delivered; keep and discard both empty). Its ask continues in two rows filed by hand before this row was minted (decision D-015): WI-892 carries the shared lane-commit walk, and WI-893 the hand-merge path behind the owner's OI-113. Drafting a successor here would have minted a duplicate of WI-893. The verdict's lineage finding is answered on trunk: WI-893 gains `supersedes = "WI-828"`. The mechanical close refuses a disposition with no draft, so this row closes by hand (the missing arm, adopting an existing successor, is filed as its own row), and the sitting's brief was not composed because the composer refuses the report's empty range (filed as its own row; coordinator decision D-022).

## Context

The closed spec is `docs/work/partial/WI-828-hand-merge-walks-its-commits.md`.

Its per-close report is `docs/handbacks/WI-828-wi-828.md` — READ IT FIRST. The report is the close EVENT's own immutable record: what the lane claims it delivered and did not, the commit range, the keep/discard split, and the review tier it suggests. The lane's claimed outcome is a CLAIM under judgement here, not this row's premise.

Outcomes (R3): cancel / defer / draft a successor / surface an open item. Continuing the work MINTS A SUCCESSOR (drafted in THIS row's `## Dispositions` section, carrying `supersedes`), never a revival of the closed row — a closed row is never re-opened and a scope definition never changes to mean something else. An override moves the byte-identical spec to the corrected terminal folder; the report stays on record as the claim it was. An open item goes to docs/requirements/open-items.toml.
