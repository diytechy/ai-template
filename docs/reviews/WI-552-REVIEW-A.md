# WI-552 — REVIEW-A rollup

Compiled by the supervising session (2026-09-01) from the round files under
`docs/reviews/wi-552-adjudicator-two-exit-close/`, time-ordered, governing
line last — the loop does not write this file yet (OI-76, WI-558). Every
round of this lane ran with heterogeneity **relaxed and recorded** (the
cross-family providers were down; independent Opus fallback — the `-relaxed`
suffix on each round file, scoreboard alongside). Round 2 (007) APPROVEd;
the close commits that followed it re-opened the clock, and round 3 (009)
caught a genuinely red module-size-ratchet baseline at that head, re-stamped
before round 4.

### REVIEW-A — Round 1 — session 005 — tip 4ccabb2 — relaxed

- [MAJOR] project-trajectory/scripts/intake.py:1150 (and handback.py:516) -> the refusal invariant gates on `brief == "disposition"`, but a CANCELLED original close mints a brief-LESS adjudication row, so neither the close-side nor merge-side guard refuses a cancelled close that queues no successor -> extend the invariant to the cancelled arm -> @owner
- [MINOR] project-trajectory/scripts/schedule.py:678 -> `_waiting_reasons` emits the dead-edge reason only for `cancelled` predecessors though `partial` is equally terminal -> emit `waiting:hard-pred-partial` too -> @owner
- [MINOR] project-trajectory/scripts/schedule.py:434 -> the `_OI_PENDING` comment contradicts the fail-closed code beside it -> fix the comment -> @owner

VERDICT: CHANGES-REQUESTED findings=3

### REVIEW-A — Round 2 — session 007 — tip 9286104 — relaxed

All three round-1 findings fixed and re-driven (cancelled-brief-less refusal, `waiting:hard-pred-partial`, comment); Done-when 1–7 each mapped to a covering test plus a driven path, none uncovered; `check.py --jobs 0` RESULT: PASS, 194 targeted tests passed.

- [MINOR] project-trajectory/scripts/intake.py:1364 -> `_SPEC_NEEDS_RE` is single-line (no DOTALL) while `parse_spec_frontmatter` accepts a multi-line `needs` list — the rewrite can miss a multi-line edge -> @owner
- [MINOR] project-trajectory/scripts/intake.py:305 -> `_OI_ID_RE` defined but never referenced (dead code) -> @owner

VERDICT: APPROVE findings=2

### REVIEW-A — Round 3 — session 009 — tip b797022 (HEAD f1a7e6b8) — relaxed

- [BLOCKER] tests/test_module_size_ratchet.py:1929 -> the committed `intake.py` baseline is 1179 SLOC but the module measures 1177, so `test_module_sizes_exactly_match_the_committed_baseline` FAILS — verified red under `-m smoke` on the clean HEAD; the per-commit bar is red and the Deliverable's "smoke tier green" claim is stale at this head -> re-stamp the baseline deliberately -> @owner

VERDICT: CHANGES-REQUESTED findings=1

### REVIEW-A — Round 4 — session 016 — tip 3bb8bb1 — relaxed

Module-size ratchet green after the deliberate re-stamp (197 targeted tests
passed); the seven Done-when arms re-driven directly — typed OI edges
fail-closed (`pending`/absent → not satisfied), the cancelled-brief-less
refusal regression genuine, inbound hard edges re-point while soft edges are
left alone, all caller sites thread `oi_status`, byte budgets match on disk.
(Full account: `016-REVIEW-A-3bb8bb1-relaxed.md`.)

- [MINOR] project-trajectory/scripts/check_trajectory.py:812 -> `validate`'s docstring says a non-adopter's OI edge (`known_ois=None`) is left to the scheduler, but the code coerces `None -> frozenset()` so every OI edge errors -> align docstring or behavior -> @owner
- [MINOR] project-trajectory/scripts/intake.py:304 -> `_OI_ID_RE` still defined and never referenced -> delete the dead constant -> @owner

VERDICT: APPROVE findings=2
