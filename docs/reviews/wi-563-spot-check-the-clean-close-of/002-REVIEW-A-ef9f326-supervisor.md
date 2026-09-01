# WI-563 REVIEW-A (supervisor-drawn) — spot-check of the WI-552 close

No mechanized round was scheduled for this adjudication lane (the WI-559
defect: scheduling exists after a committing BUILD only, and the exit banner
claimed a round that was never drawn). The supervising session drew this
round through an independent Opus reviewer with a hostile brief, read-only,
at HEAD `ef9f3268` (2026-09-01). The reviewer re-verified every code citation
the Deliverable makes, reproduced the `_SPEC_NEEDS_RE` residual directly,
re-ran the tree-wide multi-line-`needs` scan (empty — the mitigation holds),
ran `check_trajectory.py --strict` (exit 1, one ERROR; non-strict exit 0) and
`git status --short` (clean), and verified the close mechanics (spec in
`complete/`, Deliverable before Context, specref cleared, claim dir empty,
fragment compiled by the station refresh, no stray ids in status.md).

## Findings

- [MAJOR] project-trajectory/scripts/schedule.py:445 -> WI-552 arm 5 added a lazy `import trace` inside `_open_item_states`, creating a cross-component import CMP-008 -> CMP-006 with no declared IF-### seam; `check_trajectory.py --strict` errors on it at HEAD (exit 1), and it is attributable to the work under review — the same command on trunk immediately before the merge (`b6e155d3^1`) is ERROR-free and has no `import trace` in `schedule.py` (introduced by `b2b06898` "WI-552 arms 5+6"). The spot-check concluded arm 5 "Present" and the close "STANDS" without detecting it. This is precisely the class a sample attestation exists to catch, and the row's prescribed exit for it is a successor row -> re-open the spot-check verdict: mint the successor to declare the IF-### seam in `docs/requirements/interfaces.toml` (or retag the membership), and record the strict-ERROR miss against the WI-552 close -> @owner
- [MAJOR] docs/log.md:54768 -> the session's Bar declaration ("The environment here has no pytest toolchain; the spot-check is a read-level attestation") is factually wrong and is the direct cause of the miss above: `check_trajectory.py` needs no pytest and runs clean on `python3` here, the trunk venv exists, `docs/status.md` standingly requires `check_trajectory.py --strict` unfiltered before claiming anything done, and the station's refresh trailer `ef9f3268` attests `bar PASS (11 steps, tier all)` on this tree — so an environment claim excused a check the environment could run and the repo mandates -> re-run the mandated checks and re-state the Bar with real output, or state honestly that no verification command was run and downgrade the verdict's confidence accordingly -> @owner
- [MINOR] docs/log.md:54693 -> the WI-563 log fragment carries no `Deferred open items: ...` declaration in either form, which PROCESS.md §5 and the session-protocol skill require of every fragment and `gen_open_items.py --check` reads at the commit bar; the session in fact ends routing a confirmed-live residual `@owner` with no OI row — the exact shape the rule targets -> add the declaration line (a follow-up fragment or the successor's) -> @owner
- [MINOR] docs/archive/work/complete/WI-563-spot-check-the-clean-close-of.md:32 -> the three carried-forward WI-552 findings (`intake._SPEC_NEEDS_RE` no-DOTALL, dead `intake._OI_ID_RE`, `check_trajectory.validate` docstring vs `known_ois=None` coercion) are named and re-confirmed, and the DOTALL analysis (arm 4's "unrepresentable" narrows to "unrepresentable under the single-line-`needs` invariant") is defensible — but after this close the three findings exist on no queue: no OI row, no successor, and the REVIEW-A rollup is not an owner decision surface -> surface at least the DOTALL residual as an OI row and let the two cosmetic ones ride the same row -> @owner

VERDICT: CHANGES-REQUESTED findings=4
