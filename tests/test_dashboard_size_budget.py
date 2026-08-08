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
# 1,650,000 -> 1,900,000, WI-340/342 (2026-07-28). 1,658,490 against 1,640,447
# at the parent commit: +18,043 for SEVEN new WI rows (WI-343..WI-349) and three
# long Deliverables, ~2.6 kB/row, which is the SAME per-row cost as before —
# registry growth, not a rendering blow-up. (129-REVIEW-A MAJOR 4 refuted the
# first figures stamped here: they were measured before two more rows were filed
# in the same session, so they were stale by +3,034 bytes and one WI. Measure
# AFTER the last edit, not during.) Note what the old number really was: 1,650,000
# left 9,553 bytes of headroom (0.6%), so it had stopped being the "generous
# ceiling" this file documents and had become an exact freeze that bites on the
# next four rows — the same defect as the smoke ratchet stamped at current+1
# (WI-336). 1,900,000 restores ~15%, matching the 14-21% the earlier stamps kept.
# Size at the commit that carries this stamp: 1,666,554 (129-REVIEW-A's remediation
# added WI-350/WI-351). Both figures are point measurements labelled by commit,
# per the signed-measurement rule — the ceiling is what is normative here.
# 1,900,000 -> 2,185,000, concurrency-v2 drain (2026-08-01). Trunk measured
# 1,899,614 at 4ae2e838 — 386 bytes of headroom, 0.02%. The ceiling had again
# become an exact freeze rather than the generous one this file documents, and
# the stamp above diagnoses that exact failure at 0.6%: any merge at all trips
# it. It was tripped by the first WI of the drain (WI-380 renders +1,270 bytes
# — one archived spec with a Deliverable plus one intake edit), which is
# ordinary per-row cost, not a rendering blow-up. Restamped to ~15% headroom,
# matching the 14-21% every earlier stamp kept.
# Measured AFTER the last edit in this commit, per this file's own 129-REVIEW-A
# lesson: 1,899,614 at the commit carrying the stamp. Reason in the log.
# 2,185,000 -> 2,680,000, mechanized-loop P1 (2026-08-08). The combined spine
# sitting added 82 rows in one commit — 21 SR (SR-137..158), 31 LLR
# (LLR-155..185) and 30 TC (TC-150..179) — every one of which renders a node
# with its detail JSON. MEASURED: 2,159,708 at the parent commit, 2,332,896
# after, so 173,188 bytes for 82 rows = **2,112 bytes/row**, BELOW the ~2.6 kB/row
# every earlier stamp measured for WI rows (a spine row carries no Deliverable).
# Per-row cost unchanged => registry growth, not a rendering blow-up, which is
# exactly the discrimination this sensor exists to make. Restamped to ~15%
# headroom on the post-edit figure, matching the 14-21% every earlier stamp kept
# and avoiding the exact-freeze failure the two stamps above diagnose at 0.6%
# and 0.02%. Measured AFTER the last edit in this commit. Reason in the log.
MAX_BYTES = 2_680_000


def test_dashboard_stays_within_its_size_budget():
    assert DASHBOARD.exists(), "PROJECT_STATE.html is missing from the repo root"
    size = DASHBOARD.stat().st_size
    assert size <= MAX_BYTES, (
        "PROJECT_STATE.html is {:,} bytes, over its {:,}-byte budget. If this is "
        "legitimate registry growth, re-stamp MAX_BYTES with the reason in the "
        "log; if it is an accidental blow-up, fix gen_trajectory.py instead."
    ).format(size, MAX_BYTES)
