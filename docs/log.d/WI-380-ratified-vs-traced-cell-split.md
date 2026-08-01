## 2026-08-01 — WI-380: ratified vs traced cells in the amendment detector

**One line:** the post-attestation amend-without-flip warn compared every
column except `Status`, so an LLR `Module` pointer following code that moved
armed the re-attest window exactly as if requirement prose had changed; it now
compares only the **ratified** cells of the §A5.1 split
([`../concurrency-v2.md`](../concurrency-v2.md) §A5.1, owner ruling
2026-07-31), and the traced half is handed on as structured data instead of
being thrown away.

**Deliverables** (all in
[`../../project-trajectory/scripts/check_trajectory.py`](../../project-trajectory/scripts/check_trajectory.py)):

- `SPINE_TRACED_CELLS` + `SPINE_RATIFIED_CELLS` — the ruled table, both halves
  declared per registry, and `spine_cell_class(csv_path, column)` as the single
  place either is consulted.
- `staged_spine_amendments(root)` — the scan, now returning one record per
  amended `Verified` row: `{"registry", "id", "ratified": {cell: (before,
  after)}, "traced": {...}}`. `staged_spine_findings` becomes a thin formatter
  over it that reports the **ratified** half only.
- Five tests in
  [`../../tests/test_trajectory_staged.py`](../../tests/test_trajectory_staged.py)
  (see *Tests* below), and the ratchet moves in
  `tests/test_complexity_ratchet.py` + `tests/test_module_size_ratchet.py`.

**The design call — allowlist WITH a fail-safe residual, not an allowlist
alone.** Both halves of the split are declared, and a column in **neither**
falls to **ratified**. The row's own framing is what decides this: the
detector's two failure modes are not symmetric. A spurious window is a window
somebody sees — it costs an owner sitting and four review rounds (WI-280), in
the open, and gets filed. A missed window is seen by nobody, and being seen is
the entire function of the `Modified` marker. So the residual must fall toward
noise. A pure allowlist gets that backwards: a column added to a registry after
the ruling was written would be silently un-ratified, converting exactly the
spurious window this row removes into a missed one.

That leaves the residual's own hazard — it is silent by construction, so a new
column could ride it unnoticed forever. `test_spine_cell_split_classifies_every_shipped_column`
closes it: every column of this repo's live registries **and** of the blank
forms the kit ships must appear in one half or be the id/`Status` key, and the
halves must not overlap. Adding a column to a spine registry now fails **at the
ruling**, in the suite, rather than quietly changing what counts as attested.

**Adjudication is not in this row.** §A5.1 routes a changed `SN-Refs`/`Verifies`
to adjudication (WI-388), which does not exist yet. This row's job was to stop
those cells arming the window and to leave the change *recoverable*, so the
structured return is the seam: a traced-only edit produces a record with an
empty `ratified` half and the cell's before/after in `traced` — which is
precisely the material §A5.2 says the derived Deliverable body is built from.
No minting, no `safety_class`, no dial added here.

**Tests** (all in `tests/test_trajectory_staged.py`, the module that owns this
warn's tests; it is a `SLOW_MODULES` module, so these run at close and in CI,
not in the smoke bar — the existing tiering, not a new choice):

- `test_staged_spine_traced_cells_do_not_arm_the_reattest_warn` — every traced
  cell of all three registries moves at once (the literal WI-280 shape) with
  every ratified cell and every `Status` untouched → silent.
- `test_staged_spine_ratified_child_cells_still_arm_the_reattest_warn` — the
  complement, so the narrowing cannot be mistaken for a disabling.
- `test_staged_spine_unknown_column_falls_to_ratified` — the fail-safe.
- `test_spine_cell_split_classifies_every_shipped_column` — the coverage guard
  described above.
- `test_staged_spine_amendments_expose_the_traced_half_for_adjudication` — the
  WI-388 seam, asserted on the structured return in-process.

**Mutation-proved, both directions, both reds observed:** reverting
`spine_cell_class` to the pre-WI-380 "everything but `Status` is ratified" reds
the traced-cell test and the seam test (`2 failed, 7 passed`); flipping the
residual to allowlist-only (`ratified` iff explicitly listed) reds the
unknown-column test with an empty stderr — the missed window, made visible.

**Deviation from the spec, deliberate and narrow.** LLR `SR-Refs` and SR
`SupersededBy` are columns of the live registries that §A5.1's table does not
name. They are listed in the **ratified** half — today's behaviour kept, *not*
narrowed past what the owner ruled — because narrowing an unruled cell is
exactly the missed-window risk this row exists to remove. That LLR `SR-Refs` is
the same shape of pointer as the ruled-traced `SN-Refs`/`Verifies` is a real
question; it belongs to WI-388, and the comment at the table says so.

**Ratchets.** Complexity **re-keyed, not bumped**: the classification loop was
extracted as `_split_changed_cells`, so the scan (now
`staged_spine_amendments`) holds at its former **20** and
`staged_spine_findings` drops under the limit and has its entry deleted — the
decomposition escape the ratchet prefers, taken instead of the +3 bump the
inline form measured. Module size `check_trajectory.py` **3098 → 3191 (+93)**,
a reviewed bump with the reason at the entry: most of it is the two declared
tables plus the comment recording why the residual falls to ratified. The rule
stays beside its only consumer for the WI-349 reason — a sibling module would
separate the rule from the single scan it governs.

**Budgeted files:** none touched (`AGENTS.template.md`, `PROCESS.md`,
`PROCESS_OPTIONS.md` all unchanged — 0 bytes). No spine amendment, no new
module. [`../architecture.md`](../architecture.md)'s generated module map was
regenerated for the two new public symbols (a 3-line diff, confined to the
`check_trajectory` block).

**Bars.**

- Smoke (per-commit): `pytest -q -n auto -m smoke` → **1 failed, 552 passed,
  4 skipped in 16.79s**. The one red is the standing work-branch conditional,
  `tests/test_check_lane.py::test_this_repo_is_not_a_work_branch` (it asserts
  the kit's own checkout carries no `docs/work/active/<branch>/` claim, which
  is false by construction inside a claimed worktree).
- Full (close): `pytest -q -n auto` → **2 failed, 1712 passed, 8 skipped in
  414.15s**. Both reds are pre-existing and neither is this row's:
  - `tests/test_check_lane.py::test_this_repo_is_not_a_work_branch` — the
    standing work-branch conditional, as above.
  - `tests/test_check_docs.py::test_meta_repo_has_zero_unexplained_orphans` —
    **not orphans at all**: it asserts `check_docs --strict-orphans` exits 0,
    and the non-zero exit comes from two BROKEN LINKS in
    [`../concurrency-v2.md`](../concurrency-v2.md) (`:10` and `:979`, both
    `work/deferred/`). That directory is empty since the concurrency-v2 rows
    moved to `queued/`, and git does not track empty directories, so it is
    absent from every checkout. Proved pre-existing by running the test's exact
    command against a `git archive` of trunk `54312cfa`: the identical two
    FAILs, exit 1. Trunk therefore fails its own full bar today — filed as a
    finding, not fixed here (`concurrency-v2.md` is not this row's file, and
    the deletion-vs-`.gitkeep` call is the design's).
- `ruff check .` → *All checks passed!*; `ruff format --check .` → *146 files
  already formatted*. Both were run (a past WI shipped seven F401s by checking
  only `format`).
- `check_trajectory.py --root . --strict` (unfiltered) → *clean (388 work
  item(s), 363 done (94%), 16 retired, graph acyclic)*, exit 0. The eight
  connectivity/IF WARNs it prints are the pre-existing drift WI-390's spec
  already itemises.
- `check_docs.py --root . --ignore docs/test/report.md --ignore "docs/work/*"
  --stale` → the same two pre-existing broken links, and otherwise clean
  (`0 orphan(s)`; this fragment matched `docs/orphans-allow`, 106 → 107).
