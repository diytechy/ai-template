9c7e5b9f NOT YET SOUND

- **blocker** — `docs/archive/last_approved/acts.toml:15`: the act approved nine new rows, but the ledger records only the five frame rows and omits `STK-01..STK-04`. `baseline_snapshot.SNAPSHOT_TIERS` lacks `STK-ID`, contrary to IF-220. Add that tier with regression coverage and rerun the snapshot act so all nine approvals are recorded.

- **major** — `tests/test_dogfood_sync.py:472`: lowering the REL floor from 1 to 0 weakens a ratchet to green the ruled one-row frame; the adjacent claim that this still means “more than the example” is false. Exempt the locked REL tier from this generic growth-floor assertion and rely on the exact-one frame pin.

- **major** — `docs/requirements/external.toml:24`: the extra “TWO SYSTEMS OF INTEREST” header paragraph is neither §1.3’s signed header text nor a disclosed reconciliation. Remove it or obtain and record approval for this added normative prose.

- **major** — `docs/plans/2026-09-25-c1-sitting-package.md:454`: the required sitting-act log fragment is absent. Also, the derived-view requirement at line 457 is unmet: `gen_trajectory.py --check` reports `PROJECT_STATE.html` stale. Add the Decisions/approvals/dial fragment and regenerate the dashboard.

- **minor** — `tests/test_intake.py:291`, `tests/test_intake.py:349`: docstrings still say this repository runs only `DevStg-Needs` held. Make them fixture- or history-specific and point current policy claims to the dial.