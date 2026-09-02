### REVIEW-A — WI-571 — Round 004 — 2026-09-01

- [MAJOR] project-trajectory/scripts/baseline_snapshot.py:728 -> `_authorised_registries` treats every Status difference as an approving flip, so an `Approved`→`Drafted` change in one SR authorises a registry-wide copy that absorbs an unrelated approved SR amendment; the driven tmp-tree flow wrote `system-requirements.toml` and reported `amendment_absorbed=True` -> authorise only an actual approval transition (Drafted→Approved, plus a new approved row), and add the two-row de-approval-plus-amendment regression -> @owner; per the `antidote` structural test, keep that transition meaning in the single owning maturity/approval predicate rather than adding a later compensating guard.
VERDICT: CHANGES-REQUESTED findings=1
