# Sonnet review — WI-752 (build/wi-752 at d0c11f8e)

Reviewer: Claude Sonnet 5.5 (read-only). Builder: Codex Sol (gpt-6.1-sol, low). Range `56362374..d0c11f8e`.

d0c11f8e SOUND

**BLOCKER:** none. **MAJOR:** none. **MINOR:** none.

- TC-302 `method` matches the adjudicator's replacement byte for byte; `evidence` is the old value plus `; tests/test_open_item_readiness.py::test_only_queued_rows_are_held_and_a_drained_frontier_still_lists_gates`; `status` stays Drafted; other cells untouched.
- The added assert (`tests/test_open_item_readiness.py:83`, after `path.unlink()`) is the drafted line and calls the checker with the registry deleted (`spine_carrier.load` of a missing file).
- The added evidence test moves WI-688 to `docs/archive/work/complete` while the registry names it and asserts no finding, fed from `read_spec_rows`, which reads the archive sibling (`kitlib/registry.py:419`).
- Scope: only the two TC-302 cells and the one assert (plus regenerated artifacts).

**Commands:** `pytest -q -n 2 -p no:cacheprovider tests/test_open_item_readiness.py`: `8 passed in 0.73s`.
