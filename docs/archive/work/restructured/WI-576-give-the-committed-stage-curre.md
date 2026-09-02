+++
id = "WI-576"
title = "Give the committed-stage currency test the work-branch exemption its derive_stage --check twin already has"
workstream = "process"
specref = "docs/archive/work/complete/WI-574-spot-check-the-clean-close-of.md"
buildtier = "quick"
priority = 3
safety_class = "ordinary"
+++

## Deliverable

Restructured into WI-582.

## Context

Drafted by WI-574 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

`tests/test_derive_stage.py:528` (`test_this_repo_s_committed_stage_is_current`)
asserts `recorded["fingerprint"] == kitstage.fingerprint(ROOT, memo=None)` with
no work-branch exemption, while the commit-bar step that makes the same claim
(`derive_stage.py --check`, run through `check.py`) SKIPs on a work branch
because generated freshness is the trunk lane's (concurrency-restructure §5.2).
The mismatch was near-unreachable until WI-572 made lane-side amendment of a
settled `Approved` spine row the normal path; each such amendment moves the
`docs/stage` input digest, so a routine lane now meets a red that the trunk lane
clears one merge later. IN SCOPE: give the test the same branch-awareness its
twin has — reuse whatever `check.py` already consults to decide "work branch"
rather than adding a second notion of it, and pin the exemption with a test so
the skip cannot silently swallow a genuinely stale trunk `docs/stage`. Show the
test green on a work branch that amends a settled spine row, and still RED on
trunk with a stale `docs/stage`; the second half is the point — an exemption that
also disarms trunk would trade a false red for a missed one. EXPLICITLY NOT IN
SCOPE: any change to `derive_stage.py`'s own derivation, or to which artifacts
the work-branch skip covers.
