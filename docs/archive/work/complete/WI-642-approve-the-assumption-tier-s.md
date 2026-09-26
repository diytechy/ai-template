+++
id = "WI-642"
title = "Approve the phase-6 chains SN-041..SN-044, SR-187..SR-219, LLR-211..LLR-258, TC-212..TC-251 as one act"
workstream = "requirements"
specref = ""
sr_refs = ["SR-187", "SR-188", "SR-189", "SR-190", "SR-191", "SR-192", "SR-193", "SR-194"]
needs = ["WI-641", "WI-601", "WI-603"]
buildtier = "strong"
safety_class = "spine"
priority = 2
+++

## Deliverable

The act is the commit that closes this row: every row of the phase-6 chains
flips `Drafted` to `Approved` together, 124 in all (SN-041..SN-044,
SR-187..SR-219, LLR-211..LLR-258 without the deleted LLR-253, TC-212..TC-251),
`status` only, with the acceptance record refreshed in the same commit.

- **Gating adjudications:** WI-641 (SR-162 CLARITY), WI-601 and WI-603 (LLR-061
  and LLR-167 MEANING, re-anchored at f537fc53) closed at 71844466. Going in, the
  only drifted approved rows were the seventeen WI-547 rows and SR-162, all
  ruled CLARITY. This act re-anchors them.
- **Brief:** `docs/ratify/2026-09-25-phase6-assumption-tier.md`, minted from the
  fresh `CURRENT.md` at the act's parent. The stand-in read the `trace.py
  --approve 6` rendering, byte-identical at that parent.
- **Record:** `intake.py snapshot`, with the design-row and test-case records
  authorised by their Status moves. The requirements and needs records are named
  with `--approves` (the tool refuses drifted approved text a flip does not
  cover, and has no needs tier). Each record equals live after the copy. The
  moved cells on existing rows are the 124 flips and the 18 CLARITY-ruled SR
  rationales; SR-183..SR-186 and TC-208..TC-211 ride along Drafted.
- **Stage:** the headline stays DevStg-Tests; phase 6 reads DevStg-Impl.
- **Who approved:** SN-041..SN-044 were signed by the owner's **stand-in**, a
  Fable agent (`SITTING: APPROVE`), as the owner directed, and the owner's
  re-attestation is owed: D6/D20 (SN-042's narrowed acceptance) first, then D2
  (SN-043, SN-044 new) and D5 (SN-041's first sentence answered by a later
  assumption row). The SR, LLR and TC tiers are released rungs, approved on the
  per-tier Sol reviews and stand-in approvals, confirmed at the sitting.
- **README:** the four approved needs gained their inventory bullets, marked
  commissioned rather than shipped (`check_docs` requires a bullet per approved
  Must/Should need).

**Deviation: `[checks] test_first_since` is not set here.** A commit cannot
name itself, and SR-217 judges requirements "approved after" the start, so the
right value is the act's parent, `f537fc531dd37b372259ba84f8836a290d1efddb`.
The key cannot be declared yet, though: `tests/test_rule_sync.py` holds this
repo's `[checks]` keys equal to the shipped template's, and the template gains
the key only with WI-640, which builds its reader. The value is recorded in
WI-640's spec, which sets it when it ships the key.

Review: codex Sol (medium) on the staged act, NOT YET SOUND with 2 blockers
(close this row in the act; README bullets) and 1 minor (the snapshot stamp's
refs), all applied. The smoke tier caught the `[checks]` structure rule above,
which Sol had judged acceptable; the test wins, so the key waits for WI-640.

## Context

The chains were derived and reviewed in text while the owner was away (codex Sol per iteration; the owner's Fable stand-in approved each tier). The act was deferred because refreshing the requirements and design-row records would carry twenty drifted approved rows with it: seventeen rationale edits WI-547 already ruled CLARITY, which this act re-anchors on that recorded verdict; SR-162 (WI-641); and LLR-061 and LLR-167 (WI-601, WI-603). The needs are the owner's rung: their flip is the stand-in's act unless the owner has returned and signs it. Taking the three adjudications and this act as one sitting keeps the requirement-text window open once rather than three times. Derivation and decisions: `docs/plans/2026-09-25-assumption-tier-spine-map.md`.

## Done-when

- WI-641, WI-601 and WI-603 are closed, and no approved row in the requirement, design-row or test-case registries is drifted except the seventeen WI-547 re-anchors.
- The approval brief for phase 6 is generated with `trace.py --approve 6`, read, and minted as a dated brief.
- Every row in the chains flips to Approved in one commit with the acceptance record refreshed, and the derived stage stays DevStg-Tests.
- The log records who approved: the owner, or the stand-in with the owner's re-attestation owed, and `[checks] test_first_since` is set to this commit.
