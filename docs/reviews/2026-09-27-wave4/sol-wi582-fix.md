<!-- Codex Sol (gpt-5.6-sol, medium) review of WI-582, read-only; prompt gist in ARBITRATION.md. Links re-rooted from the removed worktree. -->

1803458b NOT YET SOUND

- **major** — LLR-210 names seven code symbols, but none carries the required `Implements: SR-220, LLR-210` backlink: `docs/requirements/low-level-requirements.toml:2222`; `project-trajectory/scripts/consolidate.py:170,193,445,526,632,900,1164`. Add the backlink to every named symbol’s docstring.

- **major** — TC-208 still omits IF-177 and IF-178, despite their allow entries explicitly assigning burn-down to TC-208 or WI-604’s successor: `docs/test/test-cases.toml:2114`; `docs/if-tc-coverage-allow:219-220`. Add both IDs to TC-208’s `verifies`, add their owner-side `Contracts:` markers and `Contract IF-###:` bodies, then remove both allow entries.

- **major** — The “only edit”/“scope text unchanged” clauses are under-tested. TC-208 requires the one-line Deliverable to be the absorbed row’s only edit (`docs/test/test-cases.toml:2116`), but its test checks only one retained sentence and frontmatter equality (`tests/test_consolidate.py:758-765`). TC-254 likewise claims unchanged scope (`docs/test/test-cases.toml:2622`), while its end-to-end test checks only one context sentinel (`tests/test_consolidate_close.py:297-300`). Compare the complete original and archived specifications after removing exactly the inserted Deliverable section, so any other byte change fails.