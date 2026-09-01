# WI-553 — REVIEW-A rollup

Compiled by the supervising session (2026-09-01) from the round files under
`docs/reviews/wi-553-hold-ban-and-surface-hygiene/`, time-ordered, governing
line last — the loop does not write this file yet (OI-76, WI-558). Both
rounds ran cross-family (heterogeneity held; no relaxation).

### REVIEW-A — Round 1 — session 002 — tip ae02efc

- [MAJOR] docs/requirements/low-level-requirements.toml:606 -> Approved LLR-058 still requires a queued WI carrying `blockref` to read as blocked, but this diff removes `BlockRef` from the registry schema -> revise the row to the terminal-close model -> @owner
- [MAJOR] docs/requirements/low-level-requirements.toml:1430 -> Approved LLR-144 still specifies `schedule`'s queued-plus-`blockref` anti-livelock mechanism after this diff removes it -> revise the LLR -> @owner
- [MAJOR] docs/requirements/low-level-requirements.toml:1981 -> Approved LLR-198 still requires the `blocked_pending` symbol and its blockref-backed owner-action projection, but this diff deletes both -> update the CodeSymbol and Detail -> @owner
- [MAJOR] docs/test/test-cases.toml:1348 -> Approved TC-138 still requires a declared `blockref` to survive a partial close even though the field was removed -> replace the obsolete assertion with the terminal-close model's -> @owner
- [MAJOR] docs/test/test-cases.toml:1864 -> Approved TC-194 still requires a blocked-row pointer projection and all four former facade names, while this diff removes the blocked source and `blocked_pending` -> revise -> @owner

VERDICT: CHANGES-REQUESTED findings=5

### REVIEW-A — Round 2 — session 004 — tip c5cf731

All five round-1 spine-consistency findings addressed; clean approval.
(Full text: `004-REVIEW-A-c5cf731.md`.)

VERDICT: APPROVE findings=0
