## 2026-07-29 — WI-346: one local spine loader + one capture helper for gen_trajectory

Two extractions inside `project-trajectory/scripts/gen_trajectory.py`, both
charged by the census ([dupes-allow](../dupes-allow)) and both explicitly *not*
the F5 case — F5 buys cross-**script** copy-ability, and every copy here was
inside one file.

- **`_spine(root, skip_example=False)` → `(srs, llrs, tcs)`.** `arch_icicle`,
  `spine_stats` and `_spine_pending` each re-derived the same
  `read_rows(...) if id.startswith(...)` triple; `_spine_pending`'s variant
  also excluded `-000`, so that rule moved *into* the loader as the parameter
  rather than staying at the call site. `arch_icicle`'s TC filter was inlined
  in a `for` header, so that loop was restructured (`for r in tcs:`) rather
  than substituted. The docstring states the contract the copies left implicit:
  **row order is the `--check` byte contract** — no sort, no set, no dict
  round-trip — because the icicle links each row to its first listed parent and
  lays blocks out in arrival order.
- **`_run_captured(argv)`.** The five-keyword `subprocess.run` capture block
  (`capture_output`/`text`/`encoding`/`errors`/`stdin=DEVNULL`) that `_asof`
  and `_git` each spelled out — the same pattern WI-304 extracted in
  `agent_dispatch` rather than sanctioning. It deliberately does **not** catch
  `OSError`; both callers already own the off-git degrade, and swallowing it in
  the helper would hide a failure from a future caller.

**Census 217 → 208**, and the whole emitted census was diffed, not just the two
sections: **nine deletions, zero insertions**, so no `gen_trajectory ==
gen_trajectory` block moved in to replace what left. Eight are the charged
classes (`spine-load-repeat` ×7, `subprocess-capture` ×1); the ninth is a
clique dissolution one class over — `f02bcce4d53d` (check.py ==
gen_trajectory.py, `git-wrapper`) matched check.py's `_git_out` against
gen_trajectory's `_git` **body**, which is now a one-line call, too short to
match. check.py was not touched.

One charged fingerprint **did not dissolve**, and is re-classed rather than
quietly dropped: `29c06640159e` re-emits byte-identically because it was never
the loader. It is the icicle's per-tier node build (`<tier>_ids = {...}` then
the `add()`/primary-parent/`link()` loop, SR arm vs LLR arm), which
`spine-load-repeat` had charged to WI-346 by proximity. The two arms read
different columns, so what removes it is a per-tier column spec — the
view-model half of the graph/render split **WI-280**'s row already names for
this file. New `tier-node-build` class, `debt WI-280`.

**Byte-determinism, checked by hand.** On a claimed work branch the
`trajectory-map`/`status-map` freshness steps skip (§5.2), which hides exactly
the regression this refactor could cause, so both were run directly from the
worktree: `gen_trajectory.py --check` → "project-state dashboard up to date",
`--status --check` → "status snapshot up to date". No generated artifact
committed. Both were run with the registry still in its parent state, which is
the control that matters: after the closing `git mv` flips WI-346 to `done` the
dashboard reports STALE, and re-running the pair with the spec temporarily back
in `active/` reports fresh again — so the staleness is the WI close, which §5.2
hands to the trunk, and not a byte regression from the refactor.

**Ratchets, same commit.** `test_module_size_ratchet` 5256 → **5281** (+25):
the deduplication grew the file, the WI-345 shape again — the code shrank, the
two helpers carry the docstrings the copies did without.
`test_complexity_ratchet` was **not** re-stamped: `arch_icicle` measures 23
before and after. Collapsing three comprehension filters was expected to lower
it, but ruff's mccabe does not count comprehension `for`/`if` clauses, and the
one `for` header that was restructured stayed a `for`. The ratchet asserts an
*exact* match in both directions, so stamping the expected 20 would have redded
it; recorded here instead of silently adjusting a number to match a prediction.

Three unmarked tests in `tests/test_gen_trajectory.py`, over a deliberately
scrambled fixture registry (out-of-id-order rows, a `-000` example, a
non-prefixed row): `_spine` equals the former inline comprehensions
row-for-row *and* in file order; `skip_example=True` drops `-000` from all
three tiers while the default keeps them, proven through to `_spine_pending`;
`_run_captured` states all five keywords (asserted as kwargs, so dropping
`errors="replace"` alone reds) and both callers degrade off-git without
raising.

No perceptual advisory owed: zero `Verification=Critique` rows since the
Phase 2c flip, so no critique ceremony attaches to this WI.
