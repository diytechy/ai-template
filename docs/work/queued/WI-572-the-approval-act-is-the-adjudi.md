+++
id = "WI-572"
title = "The approval act is the adjudicator's, on trunk: lanes author Drafted rows, a first-approval adjudication flips and snapshots them"
workstream = "process"
needs = ["WI-571"]
specref = "docs/plans/2026-09-01-approval-act-adjudicator-only.md"
buildtier = "strong"
priority = 5
safety_class = "ordinary"
+++

## Context

Filed 2026-09-01 (evening supervised session) from the owner's ruling made in session (docs/log.d/2026-09-01-owner-ruling-approval-act.md, compiled): approval acts on spine rows - the Status flip and the anchoring snapshot - are the adjudicator's alone, on the serial trunk side, for whole-chain context and for concurrency. A lane's merge is refused on any flip, born-Approved row or snapshot write; a first-approval adjudication arm is minted at merge with the whole chain in its brief and flips + snapshots on trunk; the amendment arm's stale mechanical-tool line is replaced by the true aftermath; the doctrine is stated once. Serialized behind the copy-scope row (both touch intake.py and baseline_snapshot.py). Read the plan's section 2 before widening.
