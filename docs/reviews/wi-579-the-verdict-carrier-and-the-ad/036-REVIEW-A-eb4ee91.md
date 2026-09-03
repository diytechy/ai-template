### REVIEW-A — WI-579 — Round 036 — 2026-09-03
Verdict: CHANGES-REQUESTED
Findings:
- [MINOR] project-trajectory/scripts/gen_verdict_rollup.py:162 -> `_extra` only scans direct children, so a stale nested `docs/reviews/rollup/nested/stale.md` survives both `--check` and regeneration (the shipped flow reports `fresh (0 review scope(s))` then leaves it) despite the generator and LLR-208 claiming ownership of the directory -> make the owned-output scan and prune recursive, and add the nested-output regression -> @owner; per the antidote skill, this is a single owning generator boundary, so recursive ownership can make the stale state unrepresentable rather than adding a compensating guard.
VERDICT: CHANGES-REQUESTED findings=1
