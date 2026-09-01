## 2026-09-01 — WI-563: spot-check the clean close of WI-552 (sample attestation)

Session claimed `WI-563` on branch `wi-563-spot-check-the-clean-close-of`.
SpecRef `docs/archive/work/complete/WI-552-adjudicator-two-exit-close.md`. This
is a `complete_review = 'sample'` spot-check (`docs/process.toml [attestation]`):
the WI-552 close was GREEN and nothing is alleged; the one question is whether
what shipped answers what the row asked for. A finding is a successor row, never
a reversal — the close stands.

### Method

Read the WI-552 spec (seven Done-when arms, OI-70 as refined by OI-73), its log
fragment, and the REVIEW-A rollup (4 rounds, governing APPROVE findings=2).
Verified each Done-when arm against the merged tree at HEAD, not against the
claim prose.

### Findings

(in progress)
