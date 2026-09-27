ab3f110e NOT YET SOUND

- **blocker** `project-trajectory/scripts/intake.py:2610` — The refused test row is `Drafted`, so `--reattests LLR-001` is the wrong remedy; it is not an amended `Approved` row. Distinguish statuses: direct `Drafted` rows to a reviewed `Status` approval plus snapshot, and reserve `--reattests <id>` for drifted approved rows.

- **blocker** `project-trajectory/scripts/acceptance_record.py:1140` — `_mirror_repair` interpolates the live carrier path into `--approves`. For CSV carriers, e.g. `docs/requirements/system-requirements.csv`, `resolve_registry()` accepts only the canonical TOML path/name or carrierless stem, so the prescribed command refuses. Normalize to the canonical registry token and test by executing the command for both carrier formats.

- **blocker** `project-trajectory/scripts/trace.py:4166`, `project-trajectory/scripts/gen_open_items.py:810` — The census now names three triggers, but “when its own Status moves” is too broad. The implementation copies only on a transition into approval or a new row arriving approved; de-approval does not authorize copying. Say “moves into approval (or arrives approved).”

- **minor** `tests/test_intake.py:1845`, `tests/test_baseline_snapshot.py:1569`, `tests/test_trace_briefs.py:944`, `tests/test_gen_open_items.py:853` — Tests still pin substrings rather than validity and currently enshrine the false statements above. Execute the suggested repairs and behaviorally exercise all three census triggers plus a non-triggering de-approval.