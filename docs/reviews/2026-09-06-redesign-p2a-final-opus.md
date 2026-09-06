# redesign-p2a-final — adversarial review

Requested route: Opus 5, high; declared CLI stream-json pattern.

Subject SHA256: `8cc2f35f3830833674450f85ec120ecae10b91c5bd0ca3cb86abd538df4e51ea`

Tracked invocation: [session log](../iteration/call_b50de3f2d9234e708bae128a1182a376-20260906-105439.log).

Review uses supplied source with tools disabled. It is an independent
assessment, not a requirement approval or a test execution.

## APPROVE

Verdict rests on the supplied packet only (no tools, no tests run). Each of the four open findings is discharged; I found no new reachable defect.

**1 — ratchet head entry.** Fixed exactly as asked. `"intake.py": 1453,  # +56 (1397 -> 1453 SLOC), 2026-09-06 P2a: … Earlier: +18 (1379 -> 1397 SLOC) …` — current delta leads the inline chain, prior behind `Earlier:`, no detached block. `bootstrap.py: 1663 # +2 (1661 -> 1663 …)` takes the same shape. Arithmetic and prior values both match the `-` lines (1397+56, 1661+2). `P2A-EXECUTION.md`'s "reason beside the value" is now true.

**2 — evidence cites a shipped test.** Bullet 3 names `test_a_cr_only_dependency_edit_refuses_before_any_mint_effect` and describes real CR-only input, not injection. I re-drove all four of its claims against `tests/test_intake.py:862-894`: `minted == []`, refusal text, `dependent.read_bytes() == cr_only.encode()` (old bytes), `local == "keep\n"` (unrelated untracked survives), no `WI-009-*.md` (future WI unwritten). The record matches the code. Bullet 4's multi-group test is the one the closure review quoted assertions from; nothing contradicts it.

**3 — refusal diagnosis.** The message now reads `cannot locate LF/CRLF frontmatter and a unique needs array span; CR-only line endings are unsupported`. It names the newline style, which was the substance of the finding; declining the extra `len(fences) < 2` branch is a fair call once the operator is told the real cause. Settled.

**4 — parser coupling.** The docstring states the invariant, which was one of the two resolutions I offered. I verified the claim rather than taking it: `registry.parse_spec_frontmatter` (`registry.py:308-323`) returns `tomllib.loads(...)` unmodified — no defaults, no normalization — and requires `lines[0] == SPEC_FENCE` exactly, so it accepts no trailing fence whitespace the local `^\+\+\+\r?$` would reject. Both halves of the docstring are accurate today. Per your instruction I am not requiring a second parse or a future-normalizer guard.

**5 — `agent_loop`.** Confirmed from the full body: `current_wi` is bound once at 3960 and read at 3964, 3978, 4002 and 4032 with no rebinding in between (nothing between assigns it). The alias was redundant; dropping it is behavior-preserving. `session_commit_range`'s conditional binds inside the tuple as intended, and `bool(commits)` is equivalent to the old `committed`.

**Withdrawal stands.** No counterexample surfaced; late destructive recovery remains correctly declined.

### Non-blocking, no action required
- The refusal's `and` reads as a conjunction where two disjoint causes are meant ("frontmatter **or** a unique span"). Wording only.
- "The checker reads the numeric dictionary, not a trailing-comment protocol" is not verifiable from this packet (the ratchet's checking code wasn't supplied), but it is now moot — the comment is conformant either way.
- `bootstrap.py`'s new entry carries no not-decomposable/must-be-whole clause of the kind every neighboring entry has. That row is P0a's, outside this subject; noting the shape, not approving the restamp.

This is an independent assessment, not an artifact approval, queue close or cutover; the full suite after source freeze is still owed to the supervising record.
