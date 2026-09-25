+++
id = "WI-619"
title = "Point builders at the tests the spine links to their module, as an inner loop beside the smoke bar (S5)"
workstream = "scripts"
specref = "docs/plans/2026-09-23-owner-notes-spine-sessions-and-tests.md#22-should-lower-level-tests-run-only-when-sr-level-tests-fail-note-3"
buildtier = "medium"
priority = 3
safety_class = "ordinary"
+++

## Context

Ruled by the owner 2026-09-24 (sister plan S5, §2.2): options (a) and (d),
with a spine-derived map.

Builders are told nothing about which tests to run while iterating. Matching
file names (`tests/test_<module>*.py`) finds a test for 61 of 82 modules, but
only about 11% of the tests that exercise a module. The map derived from the
spine (a module's LLRs, the TCs verifying them, their evidence files) covers
all 82. It is an inner loop only: the smoke bar still runs before every
commit, and test-impact selection stays rejected as the bar
(PROCESS_OPTIONS.md:2037-2041). The 41 tier disagreements are a separate item.

## Done-when

- A command prints, for a module, the test files the spine links to it,
  derived from the registries, with no hand-kept map.
- The builder brief says to run those while iterating, and the smoke bar
  before every commit.
- A test pins the map for a module whose tests do not follow the
  `test_<module>` naming.
