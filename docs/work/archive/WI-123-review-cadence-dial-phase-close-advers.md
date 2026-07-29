+++
id = "WI-123"
title = "Review cadence dial - phase-close adversarial rounds (owner proposal)"
workstream = "unattended"
needs = ["~WI-107", "~WI-121"]
safety_class = "high-risk"
disposition = "retired"
order = 122
+++

## Deliverable

RETIRED 2026-07-27, owner-ruled (OI-7, Decisions log): -previous evidence shows a per slice review is advantageous and not to deviate.- The proposal was to replace the per-slice adversarial review with two rounds at phase close, with the passing suite as cover in between; it was evidence-gated at filing (>= 2 phases of medium-BUILD evidence). The evidence accumulated and argues against relaxing: per-slice review refuted the headline claim of WI-297 and found the severe defect it existed to fix, caught real defects on WI-313 and WI-316, and across 124/125/126-REVIEW-A caught what a green suite structurally cannot - text left behind by a removal, scope added by a rewrite, and eight fluent-but-false claims two of which would have entered the record under a signature. A builder writes its own tests, so a green suite cannot police a vacuous TC or an overstated claim. Retired rather than left deferred: the question is settled, not waiting. Reopening needs new evidence, not a re-read of this one.
