# Independent judgment — approval contract schema and launch timing

Decision: **APPROVE**

Reviewed proposal:

- `docs/ai-template-redesign-2026-09-05-codex/APPROVAL-REPAIR-CONTRACT.md`
- SHA-256: `b2c434dda6ae490fbbf137c1e8052faf408c9bede7ddb156d539902909ae5793`
- Authoring record: `docs/reviews/2026-09-07-approval-contract-schema-launch-authoring.md`

The corrected `[[decision]]` carrier explicitly binds `registry`, and its
before/after maps identify the registry blobs containing each cell. The
`[[absorption]].cells` shape now matches the typed nested before/after blob
maps used by the implementation. These are representational corrections and
preserve the reviewed decision classes, scope, census coverage, evidence
binding, and publication limits.

The WI-605 migration clarification preserves the same queued WI and holder
transfer. It correctly defers creation of `turn.toml` until the supported
dispatcher first admits the frozen, pause-removed primary at a clean launch
base. Binding `turn.base` to that actual launch commit prevents a stale or
pre-migration base while adding no new workflow or approval authority.

Unchanged limits verified: no live spine cell, snapshot, approval decision,
registry status, or disputed WI-605 judgment is approved by this record. The
judgment covers only the schema representation and launch-base clarification.
