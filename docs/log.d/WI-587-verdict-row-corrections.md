## 2026-09-03 — WI-587: the verdict row says what the module does, and two stated guards grow detectors

Continuing `docs/reviews/wi-586-adjudicate-llr-207-llr-208/009-ADJUDICATE-082b9e1.md`,
`OUTCOME: RETURN rows=4`, over the `LLR-207` / `TC-205` half of that return. The
other half (`LLR-208` / `TC-206`) is WI-588's and is not touched here. Nothing in
`kitlib/verdict.py`'s behaviour changes: the return is about text that
contradicts the module and guards no fixture drives.

IN FLIGHT — the seven findings of the spec's `## Context`, in its order.

1. `LLR-207.detail`, `governing_identity`: "for HEAD or an explicit revision" →
   the branch tip, and the branch argument is a branch NAME.
2. `LLR-207.detail`, `governing_rev`: "until it can peel" is not the termination
   condition — the peel re-seats and continues; the walk ends at the first
   commit whose identity differs from its parent's.
3. A regression for the multi-log ambiguity rule (`len(ph) == 1`).
4. A regression for `branch_trailers`' carrier verification.
5. `TC-205.evidence`: reach `work_tip` / `refresh_attestation`'s refusal arms.
6. `TC-205.method`: the identity fixture's second assertion drops an entry
   rather than changing a spec.
7. `CMP-006`'s "the one package module NOT owned here" note, which this row's
   own `component = "CMP-008"` cell falsifies.

NOT ON THIS LANE — the approval. `LLR-207` and `TC-205` stay `Drafted`; no
`docs/archive/last_approved/` write, no `intake.py snapshot`.
