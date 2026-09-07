# Owner-only relink review — 2026-09-07

Decision: **APPROVE** the bounded privacy fix and regression test.

Reviewed bytes:

- `project-trajectory/scripts/spec_move.py`
  - SHA-256: `5be2aa86f487e14b318ad52f12b8ffa2c0b98aaa75dc4f70a1c3fa5544cf9868`
- `tests/test_spec_move.py`
  - SHA-256: `1b13e08e713d6e9495417b30440fde6a0672625cacb9e5b88681fb0e37b8aaeb`

`_relink_inbound_links` checks the repository-relative path against the shared
`ac.OWNER_ONLY_PATHS` set before opening, rewriting, or adding the file to its
`touched` result. The guard is inside the traversal and leaves ordinary
Markdown relinking unchanged.

The synthetic test creates a temporary path using the shared owner-only path
name, monkeypatches `Path.open` to fail if that path is read, runs the complete
move ritual, and verifies the file's bytes and staged path remain unchanged.
The targeted regression passed: **1 passed, 19 deselected**. I did not open
`OWNER_SCRATCHPAD.md`.

This review covers only the traversal privacy boundary and its regression
evidence. It grants no registry, snapshot, or work-item approval.
