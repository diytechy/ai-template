# WI-566 — REVIEW-A rollup

Compiled by the supervising session (2026-09-01) from the round files under
`docs/reviews/wi-566-adjudicate-llr-058-llr-144/`, time-ordered, governing
line last. No mechanized round exists for adjudication lanes (the WI-559
defect); both rounds were drawn by the supervising session through an
independent Opus reviewer and recorded as `002-…-supervisor.md` plus this
round-3 summary.

### REVIEW-A — Round 2 — supervisor-drawn — tip 61ad8b8

The six in-scope rows (LLR-058, LLR-144, LLR-198, TC-138, TC-147, TC-194)
all correctly ruled MEANING, no under-call; but the verdict census was
inflated to rows=23 by seventeen SR rows WI-547 had already adjudicated and
closed, and six MEANING rows closed with NO `## Dispositions` while the
machine-inserted Deliverable promised minting successors. Two kit findings
recorded for future rows: the amendment-brief arm has no refusal invariant
(handback.py:519), and WI-553's new hold-ban detector correctly reds the
stranded wi508 claim on trunk (WI-555's business).
(Full text: `002-REVIEW-A-61ad8b8-supervisor.md`.)

VERDICT: CHANGES-REQUESTED findings=5

### REVIEW-A — Round 3 — supervisor-drawn — tip 80405032

Rework verified claim by claim: the verdict file re-issued in place ends in
the single governing `VERDICT: MEANING rows=6` (edit-in-place proven right —
`verdict_refusal` is per-session, `re.search` takes the first line, no
immutability convention covers docs/reviews/); the spec's false
successors-mint sentence replaced with true reasoning, and the omitted
`## Dispositions` proven correct (`parse_dispositions` REFUSES a prose-only
section — the kit has no shape for "MEANING, no successor owed", a sharpened
kit gap); the re-attestation brief renders 6/6 in-scope rows; the fragment
declares file-level `Deferred open items: none`; markdown-only commit,
figures provenanced. Two MINORs: a stale internal pointer to the absent
Dispositions section, and a mis-quoted `check_figures --strict` exit code in
the commit message (substance right, code wrong).
(Full text: round 3 as returned; both MINORs non-gating.)

VERDICT: APPROVE findings=2
