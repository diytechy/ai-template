# WI-579 — REVIEW-A rollup (legacy carrier, the last hand-compiled one)

Compiled by the supervising session (2026-09-03) from the round files under
`docs/reviews/wi-579-the-verdict-carrier-and-the-ad/`, time-ordered, governing
line last. This is the file WI-579 itself retires: the merge slot that judged
this lane ran TRUNK's gate (the pre-WI-579 one, which reads only this legacy
rollup), so the row that replaces the carrier is carried over the seam by the
carrier it replaces, once. After this merge the gate computes over the round
files and `docs/reviews/rollup/<train>.md` is generated.

Eleven rounds, every one drawn by the loop (cross-family Terra where the
OpenAI provider had budget, Opus with heterogeneity relaxed where it did not;
recorded per round): 002 CHANGES-REQUESTED (3), 007 (4, relaxed), 012 (2,
relaxed), 015 (5, relaxed), 019 (1), 022 (2), 025 (3), 030 (4, relaxed),
033 (4, relaxed), 036 (1), 039 APPROVE (0). Each round's findings were
reworked on the lane before the next draw; the record of what each found and
what changed is the round files and `docs/log.d/WI-579-verdict-carrier-and-adjudication-review.md`.

Governing: `039-REVIEW-A-92c7a72.md` — `VERDICT: APPROVE findings=0`,
cross-family (gpt-5.6-terra), on the tree at `92c7a725`; the refresh onto
trunk `319f374a` that followed is the station's own commit and moves no
work tree.

VERDICT: APPROVE findings=0
