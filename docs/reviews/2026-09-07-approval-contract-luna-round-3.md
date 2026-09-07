# 2026-09-07 — approval repair contract independent review, round 3

## Reviewed artifact and scope

Verified the frozen proposal before reading it:

`docs/ai-template-redesign-2026-09-05-codex/APPROVAL-REPAIR-CONTRACT.md`

SHA-256:
`b5295cec53caa2078aa1ade53d9322022052637a05b9ac6775aa9f4813757105`

This is a design judgment on the frozen contract. It does not approve any
WI-605 requirement cell, snapshot, runtime change, or live registry edit. The
prior two whole-chain reviews remain immutable evidence; this round checked
their blockers against the corrected bytes and re-read the proposed surgical
amendments, their parents, cited interfaces/tests, the live rows, and the
`docs/archive/last_approved/` rows.

## Disposition of prior blockers

All previously identified material design blockers are resolved:

- The pending record now binds the initial proposal through
  `proposal_spec_blob`, while explicitly allowing only `## Approval` and
  `## Dispositions` to grow. The final non-record candidate is computed by Git
  and bound by the existing review evidence, removing the self-referential
  candidate problem.
- The `## Approval` payload binds `proposal`, turn/base, row decisions,
  before/after identities, absorption rows/cells, and a typed `impact` census.
  Exact set equality over every `(id,path)` pair closes the prior incomplete
  stable-ID impact disposition. `meaning` requires completed impact evidence;
  `equivalent` preserves existing implementation judgments.
- The projection allowlist is closed over reviewed Approval bytes, in-scope
  cells, named byte-identical snapshots, the queued-to-terminal move, parsed
  successors, watermark, and declared generated paths. Whole-file absorption
  is bounded by per-file changed Approved-cell coverage, Drafted riders, and
  `UNJUDGED` refusal.
- The exact close transformation is now specified as the existing `spec_move`
  operation: terminal move, `specref` clearing, fixed Deliverable insertion,
  and link rebasing only. The verifier derives these bytes independently.
- Restart and holder behavior is explicit: a pending turn resumes before queue
  selection, blocks every other primary writer, and has a single atomic commit
  boundary. The dedicated WI-605 migration preserves its branch/evidence,
  moves exactly one spec back to queued, creates one pending record, and treats
  prior rounds and snapshot proposals as evidence rather than approval.
- The author/committer split, logged reviewer/route binding, human-act
  requirement, and false-attribution refusals preserve SR-140/LLR-173/TC-167
  under the repository's stated accident, drift, and misbinding threat model.
  No extra cryptographic mechanism is required by this review.

## Surgical amendment judgment

The following proposed changes preserve their omitted live clauses and parent
intent, subject to the implementation and tests explicitly required by the
contract:

| Rows | Judgment | Basis |
|---|---|---|
| `LLR-140`, `LLR-152`, `LLR-153`, `LLR-154` | APPROVE design | The branchless primary turn remains under the existing exclusive station lock; ordinary claim/merge/audit/bar paths remain stated as preserved. Stage-only projection, no-bar allowlist, idempotent minting, refusal, and restart behavior are bounded rather than a second general workflow. |
| `LLR-158` | APPROVE design | Every WI branch refuses Status/ledger/snapshot effects, while the held primary projection is the sole positive writer. The shared comparison basis and registry partition remain intact. |
| `LLR-167` | APPROVE design | The same brief engine receives primary root, WI, turn, base, candidate, scope and lock binding. The existing live drift is explicitly combined with the WI-603 question rather than silently replaced. |
| `LLR-207` | APPROVE design | Existing identity folds, ordinary refresh peel, phase and trailer rules remain. The primary publication carrier independently derives the exact projection and close transformation, checks every resulting byte, and refuses stale, widened, cross-WI, partial, or unreviewed effects. |
| `TC-146`, `TC-147`, `TC-148`, `TC-153`, `TC-161`, `TC-205` | APPROVE design | The added cases exercise no-worktree ownership, atomic projection, seven-registry absorption, restart, identity binding, author/committer provenance, and all listed refusal paths without changing ordinary cases. |

`SR-140`, `LLR-173`, and `TC-167` remain preserved in meaning. The proposal
does not authorize implementation to amend them; it requires independent
implementation tests for the stated author/committer and mirror properties.

## Runtime boundary and limits

The contract is implementable as a scoped exclusive primary authoring and
publication design. Missing functions, parser wiring, lock plumbing, and test
code are implementation work, not design blockers here. Implementation must
honor the exact payload and set-equality rules; a passing test that omits an
impact pair, absorption cell, generated-path allowlist entry, or close byte
does not discharge this judgment.

The proposal remains authoring-only. This review does not approve the disputed
WI-605 cells, does not accept its preserved snapshot proposals, and does not
authorize a snapshot or Status publication.

## Verdict

`APPROVE — design contract accepted for independent implementation and review.`

This approval is limited to the frozen proposal's design meaning and surgical
amendment scope. It is not approval of any live spine text, WI-605 judgment,
runtime implementation, generated artifact, or control-window launch.
