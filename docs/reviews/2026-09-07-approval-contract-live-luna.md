# 2026-09-07 — approval repair live-cell judgment

## Reviewed bytes and scope

I verified the frozen design proposal before reviewing the live authoring:

`docs/ai-template-redesign-2026-09-05-codex/APPROVAL-REPAIR-CONTRACT.md`

SHA-256: `b5295cec53caa2078aa1ade53d9322022052637a05b9ac6775aa9f4813757105`

The live authoring record is
`docs/reviews/2026-09-07-approval-contract-spine-authoring.md`. Its declared
worktree blobs are `low-level-requirements.toml`
`389f025681849fe080bd4bf8ba4d97e89a5fbb48` and `test-cases.toml`
`bf1765cc6404c7451becdae7ea8e9bf5268e5eb3`. I compared the complete chains,
not only the changed cells: each named LLR's SR parent, its cited test rows,
and the cited IF seams. Status, CodeSymbol, references, rationale, tier and
all unlisted cells remain unchanged in the authored bytes.

This is a live semantic judgment only. It does not approve WI-605, WI-601 or
WI-603, does not approve a Status cell, and does not authorize a snapshot,
runtime implementation or publication commit.

## Row dispositions

The amendments are meaning changes because they add the primary-turn,
projection, restart, scope-binding and carrier obligations that were absent
from the prior text. The following records whether each amended live row is
safe to accept as authored after its full chain is considered.

| Changed cell | Parent and cited evidence | Disposition | Reason |
|---|---|---|---|
| LLR-140 Detail | SR-156; existing TC-132 | APPROVE semantic text | The primary in-process adjudication and pending-turn precedence complete the stated serial integrator seam and preserve ordinary claim/merge/audit behavior. |
| LLR-152 Detail | SR-148; TC-146 | RETURN | The no-bar primary projection is bounded correctly, but the publication contract does not resolve the whole-file snapshot deadlock described below. |
| LLR-153 Detail | SR-174; TC-147, IF-091 | RETURN | The `UNJUDGED` refusal and atomic pending behavior are stated, yet no legal path remains for later scoped judgments when the first equivalent publication is held by an unjudged cell in the same snapshot file. |
| LLR-154 Detail | SR-174; TC-148, IF-090 | RETURN | Holding the station through judgment and publication is correct, but it also holds the only writer needed to reach the pending scopes that the snapshot gate requires. |
| LLR-158 Detail | SR-178; TC-153 | RETURN | The shared comparison basis and whole-file mirror are preserved, but the exact snapshot/absorption rule produces the deadlock rather than a bounded held-snapshot outcome. |
| LLR-167 Detail | SR-146, SR-144, SR-148; TC-161, IF-124, IF-075 | APPROVE semantic text | The brief remains typed, strict and independently bound to the primary turn, candidate and scope; its snapshot difference remains evidence rather than approval. |
| LLR-207 Detail | SR-156; TC-205, IF-175 | APPROVE semantic text | Independent candidate derivation, exact close transformation, absorption coverage and author/committer binding preserve the carrier’s refusal direction. |
| TC-146 Method | SR-148/LLR-152 | RETURN | Its new primary/no-bar assertions cannot be complete while the snapshot deadlock remains unresolved. |
| TC-147 Method | SR-174/LLR-153/IF-091 | RETURN | Its atomic mint/publication and restart assertions need an explicit held-snapshot or predecessor-judgment path. |
| TC-148 Method | SR-174/LLR-154/IF-090 | RETURN | Its exclusive-slot and pending-resume assertions do not provide progress for the unjudged same-file scopes. |
| TC-153 Method | SR-178/LLR-158 | RETURN | The whole seven-registry copy and `UNJUDGED` cases need a legal staged outcome that does not strand the exclusive turn. |
| TC-161 Method | LLR-167; IF-124, IF-075 | APPROVE semantic text | The brief and primary-engine binding assertions match the amended LLR, subject to the publication blocker above. |
| TC-205 Method | SR-156/LLR-207/IF-175 | APPROVE semantic text | The identity, carrier, close, review and refusal assertions match the amended carrier contract, subject to the publication blocker above. |

## Material blocker

The whole-file snapshot rule in LLR-158 interacts with the primary-turn rules
in LLR-152, LLR-153 and LLR-154 as follows:

1. A first `equivalent` decision must publish the named byte-identical
   snapshot file, while the snapshot file contains pending scopes for WI-601,
   WI-603 and WI-605.
2. The projection must refuse an `UNJUDGED` absorbed cell, as LLR-153 and the
   carrier contract require.
3. The pending primary turn holds the exclusive station writer before and
   through publication, so the later scoped turns cannot run to supply those
   judgments.

This is a progress deadlock in the exact live contract, not a demand for a
new workflow or a cryptographic property. The minimum repair must state how a
semantic decision records the snapshot as held/none and later consumes the
exact prior judgments without treating that hold as approval, while preserving
the single writer and the no-duplicate scope rules. Until that disposition is
explicit, the affected live cells and their test claims are RETURNED.

## Verdict

`RETURN — live amendments are not ready for positive publication or runtime implementation until the whole-file snapshot pending-scope deadlock has an explicit bounded disposition.`

No disputed WI-605 cell, snapshot, Status cell or runtime file was changed by
this judgment.
