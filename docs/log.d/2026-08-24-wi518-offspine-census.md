## 2026-08-24 — WI-518: the off-spine census closes the disclosure hole the OI-62 sitting's adversarial round found

Deferred open items: none.

**The gap** (found by the 2026-08-24 OI-62-sitting adversarial round, its
MAJOR-2:
[2026-08-24-oi62-rule-and-spine-approval.md](2026-08-24-oi62-rule-and-spine-approval.md)).
`intake.py snapshot` copies all seven `SNAPSHOTTED` registries wholesale —
the off-spine tiers (`interfaces.toml`, `external.toml`, `components.toml`)
included — but `trace.py --approve modified` renders one section per SR: the
spine chains only. An off-spine registry changed since the last re-seed
therefore entered the signed baseline with no owner-visible before/after at
all. This is a disclosure surface fix, not a new gate: it changes nothing
`owes()` tests, and the off-spine tiers keep their own approval machinery
(one `status` cell per row, the OI-30 D3 rung map).

**The fix** (`project-trajectory/scripts/trace.py`,
`project-trajectory/scripts/gen_open_items.py`). `trace.offspine_census_rows`
— the data half, the `reattest_model`/`reattest_lines` shape — walks the
three off-spine FILES (`external.toml` carrying three id-keyed tables:
`EXT-ID`, `B-ID`, `REL-ID`) and counts rows changed/added/removed against the
snapshot by plain whole-row equality (`_offspine_row_diff`; not the spine's
approved/traced cell split, since this is a count for a signer's attention,
not a cell-level attestation surface). `_offspine_ruling_pointer` reads the
`WI-###`/`OI-###` tokens out of the subjects of commits that touched the file
since the snapshot was written (the same house pattern `agent_loop.py`'s
`build_scope_wis` uses), or names `"none cited"` when git cannot say or names
nothing. `trace.offspine_census_lines` is the markdown renderer over those
rows, wired into `reattest_lines` right after the two derived stamp lines —
before the per-SR sections — so it reaches the reader whether or not the
spine window is open (the exact shape the finding measured: the spine window
had just closed while the IF reshape sat unreported).
`gen_open_items._offspine_census_block` is the HTML renderer over the same
`offspine_census_rows`, wired into `render`'s header, right after the
Baseline line. **A no-change off-spine tier renders NOTHING on either
surface** — no heading, no list item — so a clean re-seed costs the reader
nothing extra to read past, matching the spine's own silence for an unchanged
chain row.

**Driven by tests, RED first** (`tests/test_trace_briefs.py`,
`tests/test_gen_open_items.py`): a fixture carrying this repo's own seven
real registries (`test_baseline_snapshot.py`'s `_tree` pattern, since the
failure mode is about a whole-file snapshot copy and a real IF row, which a
hand-rolled two-row fixture would not honestly exercise) is snapshotted, then
one `IF-001` cell is amended. The regenerated markdown brief and the
regenerated HTML view both name `docs/requirements/interfaces.toml` with `1
changed, 0 added, 0 removed`, and both stay silent for the untouched
`external.toml`/`components.toml` tiers. A second test per surface confirms
total silence — no `Off-spine census` heading, no `offspine-note` paragraph —
when nothing off-spine changed. The first assertion run against the
unmodified trace.py/gen_open_items.py failed exactly as expected (the census
did not exist yet); confirmed green after the implementation landed.

**Ratchets re-stamped, reasons recorded at each site** (deliberate bumps, not
drive-bys): `tests/test_module_size_ratchet.py` `trace.py` 5678 -> 5817 (+139,
the census machinery); `tests/test_complexity_ratchet.py`
`("trace.py", "reattest_lines")` 11 -> 12 (+1, the `if census:` splice branch);
`tests/test_generated_newlines.py`'s pinned non-literal-newline site in
`gen_open_items.py` 1234 -> 1266 (the new `_offspine_census_block` function
and its `{offspine}` format slot, both above the pinned site).

`docs/open-items.html` was regenerated and is byte-identical to what was
already committed — no off-spine tier has drifted from the live snapshot
right now, so the new census section renders nothing on the live repo.

### Gates

- `python project-trajectory/scripts/check_trajectory.py --root . --strict`
  → clean, exit 0, no new finding naming WI-518; the pre-existing
  `WI-484`/`WI-508`/`WI-516` pair-warns are unchanged.
- `python project-trajectory/scripts/check_docs.py --root . --stale` → OK,
  1071 doc(s), 1393 intra-repo link(s), 0 broken (the `--stale` hints are the
  same pre-existing set unrelated to this change).
- `python project-trajectory/scripts/gen_open_items.py --root . --check` →
  `open-items view up to date` (the pre-existing OI-41 deferral-arm warns are
  unchanged, and never move this step's exit code by the ruling).
- Targeted: `pytest -q tests/test_trace_briefs.py tests/test_gen_open_items.py
  tests/test_baseline_snapshot.py tests/test_complexity_ratchet.py
  tests/test_module_size_ratchet.py tests/test_generated_newlines.py` → **124
  passed in 169.28s**.
- **Smoke tier is OVER BUDGET ON THIS BOX, measured both with and without
  this change — a pre-existing, one-machine condition, not a regression from
  WI-518.** `pytest -q -n auto -m smoke` → **1327 passed, 5 skipped in
  124.11s** (this change); re-measured at HEAD via `git stash` on the same
  box → **1325 passed, 5 skipped in 131.64s**. Both breach the 60s
  `[smoke-budget]` ceiling by roughly the same margin; this machine was
  concurrently running unrelated heavy work from a different project's
  `agent_loop.py` sessions during both measurements, consistent with the
  "one machine is one data point" doctrine rather than anything this WI's
  diff touches. Not re-stamped: the budget is a real ceiling this box
  currently cannot meet under load, and re-stamping it to fit a loaded box
  would be sanctioning the check, not measuring it. Flagged here rather than
  silently claimed green.
- Full unfiltered suite, run in two foreground batches split at the
  smoke/slow tier boundary (verified against `--collect-only`'s 1332
  smoke-selected / 1701 not-smoke-selected / 3033 total): `pytest -q -n auto
  -m smoke` → **1327 passed, 5 skipped in 124.11s**; `pytest -q -n auto -m
  "not smoke"` → **1692 passed, 9 skipped in 2286.98s (0:38:06)** — the
  second batch exceeded the tool's 600s foreground ceiling and was carried by
  the harness's background-notification cycle rather than a `--timeout`
  workaround; both batches together account for all 3033 collected tests, 0
  failed. `tests/test_pre_commit_hook.py`'s known collection-order-dependent
  case (documented pre-existing at HEAD) did not fire in either batch.
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=760d1aa8 -->
<!-- fig: cmd="python -m pytest -q -n auto -m \"not smoke\"" rev=760d1aa8 -->
