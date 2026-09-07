# 2026-09-07 — current-turn impact census authoring

This is a design-only authoring record, not an approval. It resolves the cycle
created when the candidate-wide tracked-ID census asks the `## Approval`
payload to name blobs of judgment, review and invocation records that are first
created while producing that same candidate.

The exact clarification excludes only paths that both satisfy
`kitlib.verdict.is_record_path(path)` and are proven by Git to have been first
created after `turn.base`. Those files are current-turn decision evidence.
Every record path already present at the base remains a censused historical ID
use, preserving all prior evidence and references. The separate selected-spec
`proposal_spec_blob` rule remains unchanged because the queued spec is not a
record path.

No live requirement or test cell needed amendment: the governing cells require
complete impact coverage and candidate binding without prescribing that a
decision must recursively inventory the evidence it creates. No runtime,
snapshot, Status, approval payload, queued WI, or earlier review artifact was
changed.

The prior independently reviewed design had SHA-256
`4ebfdbfeed1be800a8dcfbb3cf05bad615ee58b94fca3b7b7cbcc4ceab586751cc42`.
Independent judgment must review the exact new design hash reported with this
artifact before implementation relies on this clarification.
