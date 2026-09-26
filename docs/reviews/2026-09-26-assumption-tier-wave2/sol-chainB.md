4aec3a2a NOT YET SOUND  
0312d591 NOT YET SOUND

### 4aec3a2a

- **major** — TC-161 remains `tier = "Smoke"` while its amended method explicitly requires real subprocesses, git repositories, and loop sessions (test-cases.toml:1601, test-cases.toml:1602). Its evidence module is consequently excluded from Smoke as slow (conftest.py:253), contrary to D31 and the builder brief. Fix in **4aec3a2a**: amend and adjudicate TC-161’s tier to `Full`; its method cannot honestly be implemented as an in-memory Smoke case.

### 0312d591

- **major** — The “scope that no longer differs” test does not contain a live settled or re-anchored scoped row: it scopes the brief to nonexistent `SR-404` (test_adjudicate_brief.py:857, test_adjudicate_brief.py:864). It therefore proves the “gone from the spine” case, not the named “still exists but no longer differs” clause added to TC-161. Fix in **0312d591**: retain an approved scoped row identical to its snapshot, keep another row drifted outside the scope, and assert the scoped refusal names the settled row.

- **major** — The per-registry anchor test renders a brief containing only an SR row; the TC registry is checked only by calling `stamp` directly (test_adjudicate_brief.py:900, test_adjudicate_brief.py:925, test_adjudicate_brief.py:928). A regression that renders or stamps only the first shown registry would pass, despite TC-161 requiring a stamp for “each registry shown” (test-cases.toml:1601). Fix in **0312d591**: create simultaneous scoped drift in two tiers with differently dated snapshot copies and assert both registry/stamp pairs in the composed baseline. Also add direct coverage for TOML and markdown-era carriers; the implementation includes them at baseline_snapshot.py:424, but the new test exercises only a CSV-backed snapshot.

### CROSS-CHAIN

- **major** — The TC-161 tier defect propagates into 0312d591, which adds further git-backed tests and another method amendment without resolving the Smoke/Full contradiction. The fix belongs first in **4aec3a2a** and requires the final combined TC-161 amendment in **0312d591** to be adjudicated with `tier = "Full"`. No carrier-column, classifier, signature, finding-class, or watermark conflict was found between the two implementation deltas.

Targeted pytest could not start because the read-only environment exposes no writable temporary directory. `check_trajectory.py --strict` exited 0 with existing advisories; `trace.py --strict-integrity` could not complete because it writes `docs/test/report.md`.