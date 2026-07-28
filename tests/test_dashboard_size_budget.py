"""PROJECT_STATE.html size budget — repo-review-2026-07-22 L-2 (runaway sensor).

The dashboard is a deliberate single-file offline artifact, but that means every
view change regenerates a megabyte-scale blob whose growth is otherwise
invisible in review (the review measured it drifting 1,145,810 -> 1,148,348
bytes across one remediation pass with nobody noticing). This is a coarse
runaway sensor: it does NOT freeze the exact size (the file legitimately grows as
work items accrue), it fails only if the artifact balloons past a generous
ceiling — the signature of an embedding bug or an accidental duplication, not of
normal WI growth.

When this fails: confirm the growth is legitimate (more WI/registry rows) rather
than an accidental blow-up, then re-stamp MAX_BYTES upward with the reason in the
WI/session log. If the jump is an accident (a doubled embed, an unbounded loop in
the generator), fix the generator instead of bumping the budget.
"""

import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DASHBOARD = REPO_ROOT / "PROJECT_STATE.html"

# Measured 2026-07-22 at 1,155,350 bytes (after registering WI-276..280). The
# ceiling carries ~21% headroom for ordinary registry growth; a jump past it is
# a runaway signal, not routine drift. Re-stamp with a logged reason, never
# silently.
# Re-stamped 2026-07-26 at 1,403,240 measured: legitimate registry growth, not
# an embedding bug — 25 WI rows (289 -> 314) plus the option-(f) decomposition
# (LLR-101..114 / TC-104..119, each Detail stating scope + narrowing, all
# embedded in the dashboard's detail JSON) crossed the 2026-07-22 ceiling.
# ~14% headroom kept. Reason in the log, 2026-07-26.
# 1,600,000 -> 1,650,000, WI-328: the compound-SR split added 15 SR and 12 LLR
# rows, every one of which renders a node. Registry GROWTH, not a rendering
# blow-up — the per-row cost is unchanged, and the check that would catch a real
# blow-up is this one staying tight against the new row count.
# 1,650,000 -> 1,900,000, WI-340/342 (2026-07-28). Measured 1,655,456 against
# 1,640,447 at the parent commit: +15,009 for SIX new WI rows and three long
# Deliverables, ~2.5 kB/row, which is the SAME per-row cost as before — registry
# growth, not a rendering blow-up. Note what the old number really was: 1,650,000
# left 9,553 bytes of headroom (0.6%), so it had stopped being the "generous
# ceiling" this file documents and had become an exact freeze that bites on the
# next four rows — the same defect as the smoke ratchet stamped at current+1
# (WI-336). 1,900,000 restores ~15%, matching the 14-21% the earlier stamps kept.
MAX_BYTES = 1_900_000


def test_dashboard_stays_within_its_size_budget():
    assert DASHBOARD.exists(), "PROJECT_STATE.html is missing from the repo root"
    size = DASHBOARD.stat().st_size
    assert size <= MAX_BYTES, (
        "PROJECT_STATE.html is {:,} bytes, over its {:,}-byte budget. If this is "
        "legitimate registry growth, re-stamp MAX_BYTES with the reason in the "
        "log; if it is an accidental blow-up, fix gen_trajectory.py instead."
    ).format(size, MAX_BYTES)
