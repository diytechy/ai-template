# WI-554 — REVIEW-A rollup

Compiled by the supervising session (2026-09-01) from the round files under
`docs/reviews/wi-554-approval-brief-defects/`, time-ordered, governing line
last. One mechanized round exists (scheduled by the loop after the committing
BUILD, review-policy 1, cross-family draw); the verdict gate requires this
per-WI rollup and nothing in the kit writes it yet (the verdict-carrier
repair is queued), so it is compiled by hand.

### Supervisor note — NOT a round, does not govern

Recorded so the merge carries it. An independent read of the lane diff
against the WI's Done-when arms (a read-only Opus pass drawn by the
supervisor, not a recorded round) agrees: both `trace.py --approve modified`
renderer defects (a Drafted row's cells captioned "approved — re-attestation
owed"; a changed cell truncated at the 1500-char limit) are fixed in both the
markdown and the `open-items.html` halves, with end-to-end subprocess tests
that fail on the pre-change paths; the C901 pressure was answered by
decomposition rather than a baseline bump; product code touches exactly two
functions plus a mechanical `_chain_row` split; the "approved, then demoted"
gap is banked with a pointer, which the arm permits. Three record-layer
convention misses no instrument reds: the fragment declares no `Deferred
open items:` line although this row genuinely defers one; its driven figures
(suite totals, ratchet deltas) carry no `fig:` provenance markers; and the
`trace.py` module-size re-stamp header reads `+8 (6005 -> 6031)` where the
parenthetical is +26 (the body explains the split; the header line is
self-contradictory). None alters the round's verdict; they are carried to
the session record.

Also carried by this rollup's commit: the in-slot refresh was REFUSED on the
`approval-fresh` step because this very lane changed the brief renderer, so
the committed `docs/ratify/CURRENT.md` was stale against its own output.
Resolved as the check prescribes — regenerated on the branch with
`trace.py --approve modified --out docs/ratify/CURRENT.md`, never
hand-merged. The regenerated brief is a rendering change only (the same six
MEANING rows, now shown whole and correctly captioned); no registry cell
moved.

### REVIEW-A — Round 2 — OPENAI-TERRA (medium, `-c model_reasoning_effort=medium`) — tip 280ad20

The reviewer's committed final message: 88 focused tests passed; the full
harness `RESULT: PASS`; both regressions reproduce on the pre-fix tree and
are corrected post-fix. Zero findings recorded.
(Full text: `002-REVIEW-A-280ad20.md` — the machine line only. Advisory
scoreboard: `scoreboard.txt`, margin 0, tripwires none.)

VERDICT: APPROVE findings=0
