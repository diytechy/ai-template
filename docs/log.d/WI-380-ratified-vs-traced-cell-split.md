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
- `staged_spine_amendments(root, base="HEAD", head=None)` — the scan, now
  returning one record per amended `Verified` row: `{"registry", "id",
  "ratified": {cell: (before, after)}, "traced": {...}}`, over a rev pair
  `_spine_revs` resolves. `staged_spine_findings` becomes a thin formatter over
  it that reports the **ratified** half only.
- Six tests in
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

## REVIEW-A round 1 — CHANGES-REQUESTED, findings=3, all three driven and all
three real

The reviewer re-drove every measurement in the first draft of this entry and all
of them held, so none of the below is a correction of a claim — they are three
gaps. Each was reproduced here before and after the fix.

**[MAJOR] the shipped module docstring still promised the closed window.**
`check_trajectory.py:67` read "a staged diff changing **content cells** of a
`Verified` spine row" — the exact phrase [`../concurrency-v2.md`](../concurrency-v2.md)
§A5 quotes as the defect. The *function* docstring 2,575 lines below had been
rewritten; this one had not. It is the one place stating what the warn watches
without opening the function, and the file ships downstream through
`downstream-resync`, so the false contract would have reached every adopter.
That is this row's own hazard pointed inward: a successor trusting it believes a
moved `Module` pointer still arms the marker — the missed window nobody sees.
Rewritten to the ratified/traced split, citing the ruling and naming
`staged_spine_amendments` as the traced half's home.

**[MINOR] the seam's record was consumable; its scan was not callable at the
trigger.** Driven on a synthetic repo: an `SN-Refs` re-point **staged** gives
`[{'ratified': {}, 'traced': {'SN-Refs': ('SN-001', 'SN-009')}, …}]`, but
`git commit` the identical change and the same call gives `[]` — the scan was
index-vs-HEAD while §A5.2 and `log.md`'s Decisions both put the trigger on a
trunk **commit**. WI-388's dispatcher runs *after* the commit lands and would
have got nothing. Took the reviewer's option (a), the cheaper and more honest
one, because it stayed small: `_spine_revs(root, base, head)` resolves the pair
of trees, `head=None` keeps the index default, and
`staged_spine_amendments(root, "HEAD~1", "HEAD")` now answers the post-commit
question. Re-driven on the same repo: default `[]`, rev range returns the
record. `staged_spine_findings` deliberately keeps its `(root)` signature — the
warn is the hook's question and should not grow a knob. The mechanism WI-388
owns (minting, id allocation, the two gate-policy arms) is untouched. The
docstring's over-claim was narrowed in the same pass: a traced-only record is
**not** automatically the WI-388 case — only the `SN-Refs`/`Verifies` subset is;
a `Module`-only edit is silent, traced, nothing owed.

**[MINOR] the `SR-Refs`/`SupersededBy` hand-off was fiction.** The classification
was right and stated where a maintainer of this code meets it, but the sentence
disposing of it ("it is WI-388's to put") pointed nowhere: driven, `grep -n
"SR-Refs\|SupersededBy" docs/work/queued/WI-388-*.md` returned **0 hits**, and
`concurrency-v2.md` carried no `SupersededBy` at all. A question asserted as
delegated but living only in this row's code comment dies with it. Both cells
are now written into WI-388's spec as intake — named, with the fail-safe
reasoning and the ruling asked for explicitly (confirm ratified with a reason,
or move `SR-Refs` to traced beside its two siblings) — plus one line pointing at
the delivered seam so that row's builder meets the rev pair at the claim. Same
grep now returns **3 × `SR-Refs` + 2 × `SupersededBy`**; the registry still
parses (`check_trajectory --strict` clean). Adding to a queued row's scope is
intake, not scope creep, and it is recorded here because the reviewer asked that
it be.

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
- `test_staged_spine_amendments_read_a_commit_range_not_only_the_index`
  (REVIEW-A round 1) — drives both sides of a real commit: the index default
  correctly goes quiet, the rev range answers, and a second commit proves the
  *ratified* half survives the same trip (a rev range is the same rules read
  against two commits, not a second weaker scan).

**Mutation-proved, three directions, every red observed** (all figures under
`pytest -q tests/test_trajectory_staged.py -k "spine or cell_split"`, re-driven
at `dcddef0a`):

- **M1** — `spine_cell_class` reverted to the pre-WI-380 "everything but
  `Status` is ratified": **`3 failed, 7 passed, 23 deselected`**, reding
  `…traced_cells_do_not_arm_the_reattest_warn`,
  `…expose_the_traced_half_for_adjudication` and
  `…read_a_commit_range_not_only_the_index`.
- **M2** — the residual flipped to allowlist-only (`ratified` iff explicitly
  listed): reds `…unknown_column_falls_to_ratified` on an empty stderr — the
  missed window, made visible.
- **M3** — `_spine_revs` re-inlined index-only: reds
  `…read_a_commit_range_not_only_the_index` on `[] ==
  [('docs/requirements/system-requirements.csv', 'SR-001')]`.

> **Record correction (REVIEW-A round 2, the one MINOR).** M1 was first recorded
> as `2 failed, 7 passed`, which was true when it was measured and went stale in
> the very commit that added M3's test: the commit-range test also asserts the
> traced half, so it reds under M1 too. The pass count coincidentally stayed at
> 7 while selection went 9 → 10, which is exactly why the stale line still read
> plausible — a reminder that a ledger figure is only evidence at the revision
> it was driven on. Re-driven here rather than copied from the verdict. The
> substance is unharmed: the revert reds **more**, never fewer.

**Deviation from the spec, deliberate and narrow.** LLR `SR-Refs` and SR
`SupersededBy` are columns of the live registries that §A5.1's table does not
name. They are listed in the **ratified** half — today's behaviour kept, *not*
narrowed past what the owner ruled — because narrowing an unruled cell is
exactly the missed-window risk this row exists to remove. That LLR `SR-Refs` is
the same shape of pointer as the ruled-traced `SN-Refs`/`Verifies` is a real
question; it belongs to WI-388, and the comment at the table says so.

**Ratchets.** Complexity **re-keyed, not bumped, twice over**: the classification
loop was extracted as `_split_changed_cells`, so the scan (now
`staged_spine_amendments`) holds at its former **20** and
`staged_spine_findings` drops under the limit and has its entry deleted — the
decomposition escape the ratchet prefers, taken instead of the +3 bump the
inline form measured (the reviewer re-inlined it and measured exactly 23). The
round-1 `_spine_revs` extraction then absorbed the rev-pair branch and the scan
**still measures 20**. Module size `check_trajectory.py` **3098 → 3191 (+93)**
at build and **3191 → 3230 (+39)** at the round-1 fix — both reviewed bumps with
their reasons at the entry; the first is the two declared tables plus the
comment recording why the residual falls to ratified, the second is the rev
plumbing and the docstring truth-telling the review demanded. The rule stays
beside its only consumer for the WI-349 reason — a sibling module would separate
the rule from the single scan it governs.

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
- Full (after the REVIEW-A round-1 fixes): `pytest -q -n auto` → **2 failed,
  1713 passed, 8 skipped in 469.13s** (1712 → 1713 is the new commit-range
  test; at close before the review it read `2 failed, 1712 passed, 8 skipped in
  414.15s`). Both reds are pre-existing and neither is this row's:
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
    FAILs, exit 1. Trunk therefore failed its own full bar — filed as a
    finding, not fixed here (`concurrency-v2.md` is not this row's file, and
    the deletion-vs-`.gitkeep` call is the design's). **Since fixed on trunk**
    at `22e66e51`; this branch is behind that commit and the integrator merges
    it, so the red stands here until then.
- `ruff check .` → *All checks passed!*; `ruff format --check .` → *146 files
  already formatted*. Both were run (a past WI shipped seven F401s by checking
  only `format`).
- `check_trajectory.py --root . --strict` (unfiltered) → *clean (388 work
  item(s), 363 done (94%), 16 retired, graph acyclic)*, exit 0. The eight
  connectivity/IF WARNs it prints are the pre-existing drift WI-390's spec
  already itemises.
- `check_docs.py --root . --ignore docs/test/report.md --ignore "docs/work/*"
  --stale` → the same two pre-existing broken links, and otherwise clean
  (`0 orphan(s)`; this fragment and then the round-1 verdict file each matched
  `docs/orphans-allow`, 106 → 107 → 108).
- `gen_arch_map.py --check --strict-parse` → *code map up to date* (it reported
  STALE after the signature change and was regenerated; the diff is one line).
