+++
id = "WI-642"
title = "Approve the phase-6 chains SN-041..SN-044, SR-187..SR-219, LLR-211..LLR-258, TC-212..TC-251 as one act"
workstream = "requirements"
specref = "docs/plans/2026-09-25-assumption-tier-spine-map.md#6-assumptions-and-critical-decisions"
sr_refs = ["SR-187", "SR-188", "SR-189", "SR-190", "SR-191", "SR-192", "SR-193", "SR-194"]
needs = ["WI-641", "WI-601", "WI-603"]
buildtier = "strong"
safety_class = "spine"
priority = 2
+++

## Context

The chains were derived and reviewed in text while the owner was away (codex Sol per iteration; the owner's Fable stand-in approved each tier). The act was deferred because refreshing the requirements and design-row records would carry twenty drifted approved rows with it: seventeen rationale edits WI-547 already ruled CLARITY, which this act re-anchors on that recorded verdict; SR-162 (WI-641); and LLR-061 and LLR-167 (WI-601, WI-603). The needs are the owner's rung: their flip is the stand-in's act unless the owner has returned and signs it. Taking the three adjudications and this act as one sitting keeps the requirement-text window open once rather than three times. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- WI-641, WI-601 and WI-603 are closed, and no approved row in the requirement, design-row or test-case registries is drifted except the seventeen WI-547 re-anchors.
- The approval brief for phase 6 is generated with `trace.py --approve 6`, read, and minted as a dated brief.
- Every row in the chains flips to Approved in one commit with the acceptance record refreshed, and the derived stage stays DevStg-Tests.
- The log records who approved: the owner, or the stand-in with the owner's re-attestation owed, and `[checks] test_first_since` is set to this commit.
