# Adjudication: WI-869 at 04858f3

## amendment

- [MEANING] TC-325 Tier -> the evidence must run in the Smoke tier, inside the per-commit bar (`-m smoke`, 60 s budget), so every commit re-checks the Done-when hold points -> the evidence must run in the Full tier, at slice/phase close and in CI, but not inside the per-commit bar -> not the same: the cell sets when the acceptance condition is checked. A smoke-tier implementation of the old cell fails the new one, and a Full-tier one fails the old one. The evidence, method and expected cells are unchanged; only the Tier cell moves the obligation.
- [MEANING] TC-326 Tier -> the evidence must run in the Smoke tier, so every commit re-checks the verdict-release arms -> the evidence must run in the Full tier, at slice/phase close and in CI -> not the same: the check moves from the per-commit cadence to the phase-close cadence. Only the Tier cell carries the change.
- [MEANING] TC-327 Tier -> the evidence must run in the Smoke tier, so every commit re-checks the done-when brief and combined-sitting grammar (SR-156, SR-232) -> the evidence must run in the Full tier, at slice/phase close and in CI -> not the same: the check moves from the per-commit cadence to the phase-close cadence. Only the Tier cell carries the change.
- [MEANING] TC-328 Tier -> the evidence must run in the Smoke tier, so every commit re-checks the four LLR-262 merge-mint arms -> the evidence must run in the Full tier, at slice/phase close and in CI -> not the same: the check moves from the per-commit cadence to the phase-close cadence. Only the Tier cell carries the change.

VERDICT: MEANING rows=4

Blessing (the TC rung is RELEASED, so the re-attestation is mine): I would bless all four, and I re-attest them in their own act commit.
- The new cells are accurate. All four rows take their evidence wholly from `tests/test_done_when_blessing.py`, which 86ee0ca1 added to `tests/conftest.py` `SLOW_MODULES`. A Smoke cell would now be a false claim about where the evidence runs.
- No assertion is lost. The method, expected and evidence cells are unchanged, and every case still runs at slice/phase close and in CI.
- The parent requirements keep a per-commit pin. SR-156 keeps TC-259 (Smoke). SR-154 keeps TC-084 and TC-259 (Smoke). SR-232's family pins are the ones named in the conftest comment (`test_approval_level`, `test_consolidate`).
- The 60 s budget is held rather than moved, which is the per-commit rule in CLAUDE.md.

SITTING: JUDGED kinds=amendment
