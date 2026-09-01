# WI-563 — REVIEW-A rollup

Compiled by the supervising session (2026-09-01) from the round files under
`docs/reviews/wi-563-spot-check-the-clean-close-of/`, time-ordered, governing
line last. The loop scheduled NO round for this adjudication lane (the WI-559
defect — scheduling exists after a committing BUILD only; the session-001
exit banner's "review round approved" claim was false). Both rounds were
drawn by the supervising session through an independent Opus reviewer with a
hostile brief, and are recorded as `002-…-supervisor.md` /
`003-…-supervisor.md`.

### REVIEW-A — Round 2 — supervisor-drawn — tip ef9f326

The spot-check's mechanics were clean but its verdict rested on a false
no-toolchain claim; the reviewer ran the mandated checks and found a live
`--strict` ERROR the spot-check missed — WI-552 arm 5's lazy `import trace`
in `schedule.py` creating an undeclared CMP-008 → CMP-006 crossing,
attributed by control to commit `b2b06898` (pre-merge trunk strict-clean).
Four findings (2 MAJOR, 2 MINOR): re-open the verdict and mint the successor;
restate the Bar with real output; add the missing deferral declaration; give
the three carried-forward WI-552 findings a queue carrier.
(Full text: `002-REVIEW-A-ef9f326-supervisor.md`.)

VERDICT: CHANGES-REQUESTED findings=4

### REVIEW-A — Round 3 — supervisor-drawn — tip 26c18f8

All four remedies verified discharged: verdict corrected to "stands WITH
FINDINGS — successor owed"; real Bar output that reproduces; the deferral
declaration parses file-level; and both disposition drafts proven to mint at
merge intake (draft 1 the seam successor, draft 2 the OI carrying the DOTALL
residual + two cosmetic leftovers). Two MINORs recorded: a stale 1152/1153
doc-count figure, and the kit gap that a pending `open_item` cell is
invisible to the fragment-declaration surface.
(Full text: `003-REVIEW-A-26c18f8-supervisor.md`.)

VERDICT: APPROVE findings=2
