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
MAX_BYTES = 1_400_000


def test_dashboard_stays_within_its_size_budget():
    assert DASHBOARD.exists(), "PROJECT_STATE.html is missing from the repo root"
    size = DASHBOARD.stat().st_size
    assert size <= MAX_BYTES, (
        "PROJECT_STATE.html is {:,} bytes, over its {:,}-byte budget. If this is "
        "legitimate registry growth, re-stamp MAX_BYTES with the reason in the "
        "log; if it is an accidental blow-up, fix gen_trajectory.py instead."
    ).format(size, MAX_BYTES)
