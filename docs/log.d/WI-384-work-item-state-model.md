## 2026-08-01 — WI-384: state is the folder — `archive/` splits, `disposition` is deleted

The work-item status vocabulary becomes
`draft | queued | active | deferred | cancelled | complete`, and the directory
stops being *most* of the statement and becomes the whole of it. Spec of record:
[`concurrency-v2.md`](../concurrency-v2.md) Workstream B (§B1–§B3), ruled
2026-07-31. Off-spine: `SN=25 SR=135 LLR=126 TC=123` unchanged, no spine row
moved, no `Contracts:` seam changed.

**The deletion is the deliverable.** `archive/` held BOTH terminal states, so it
needed a `disposition = "retired"` frontmatter key to tell them apart, plus
`parse_spec_status()`'s cross-check to keep folder and attribute honest, plus two
raise paths (unknown disposition; a retirement filed outside `archive/`) and
their tests. One folder too few bought an attribute, a validator, two error paths
and their guards. Splitting the folder into `complete/` and `cancelled/` deleted
all of it — [`concurrency-v2.md`](../concurrency-v2.md) §0's principle applied to
the example that produced it. Gone: the key; the cross-check in all three F5
reader copies; both raise paths; `wi_convert`'s `status_from_location`
disposition arm and its `RETIRED`/`ARCHIVE` constants; and the four tests that
only proved that validator (two named tests plus the `unknown-disposition` entry
in the malformed-spec table, which drove two parametrized cases). Nothing was
kept just in case: `parse_spec_status(relpath)` no longer takes the frontmatter
*at all*, so a stale `disposition` key merged in from an older branch is inert
data that cannot contradict the location. `status_dir` and `status_from_location`
are now inverses of one table, so the mapping is a bijection with no second fact
to keep honest.

**Two vocabulary changes, both load-bearing.** `retired` → `cancelled`: not
cosmetic, since `retired` can be read as *finished and put out to pasture* and
the two rows this design retires (WI-382, WI-385) are exactly the case that
would be misread — subsumed work that never shipped. And `draft/` is new, a
DECLARED status directory rather than a scratch folder, for the ruled reason
(§B3): `read_spec_rows` walks `<status>/WI-*.md` and skips anything under an
undeclared directory, so drafts parked outside the declared set are invisible to
`max(id) + 1`, to the duplicate-id guard and to the dashboard, and the next mint
reissues a held id. `draft` is never-ready in the scheduler exactly like
`deferred` and differs only in what it says.

**Readers repointed (the row's stated cost, measured).** `SPEC_STATUS_DIRS` is
triplicated verbatim across `agent_common.py`, `check_trajectory.py` and
`schedule.py` — the F5 rule, with `tests/test_wi_loader_sync.py` pinning the
three byte-equal — plus `wi_convert.py`'s write-side table. Beyond those four:
`agent_common.TERMINAL_STATUSES` + the worker's terminal-assignment refusal;
`schedule.py`'s `_TERMINAL_DISPOSITION`, `_waiting_reasons` dead-edge code and
the new `_NEVER_READY` arm; `check_trajectory.py`'s `OPEN_STATUSES` /
`TERMINAL_STATUSES` / `KNOWN_STATUSES`, R-A, R-F, the R-D forward-only rule,
`dead_dependency_findings` and the clean summary; `traj_render.py`'s
`STATUS_FILL` / `STATUS_BUCKET` / `STATUS_GLYPH`; `gen_trajectory.py`'s
`--cancelled` token, legend and hero clause; `traj_panels.py`'s next-work open
set; `bootstrap.py`'s `GITKEEP_DIRS`; and close-ritual prose in `integrate.py` /
`check.py`. Prose uses of "retired" meaning *removed* were deliberately left
alone — the word is load-bearing in this repo's history.

**Migration, mechanical and verified.** 378 specs left `docs/work/archive/` by
`git mv` — 16 to `cancelled/` (every row carrying `disposition = "retired"`) and
362 to `complete/` — with the now-meaningless `disposition` line stripped from
the 16. The staleness clock was then re-derived over all 362 migrated
`complete/` specs (`_path_commit_time(..., row_history=True)`, i.e.
`git log --follow --diff-filter=AM`): **0 unresolvable**, and sampled rows still
answer their PRE-migration dates (2026-07-29 for the Phase 2c cohort, 2026-07-31
for WI-374) rather than today. The rename re-dated nothing, including the 16 that
were renamed *and* edited in one commit — git scores those `R<similarity>`, which
`--diff-filter=AM` drops (the WI-362 behaviour, working in our favour here).

**Deviations from spec, both deliberate.**

1. **`docs/log.md` was touched, and a work branch is not supposed to touch it.**
   Four LINK TARGETS in it named specs this row moved and would have gone
   dangling, reddening the composed-tree `check_docs` bar. Only the targets were
   retargeted `work/archive/…` → `work/complete/…`; link text and every prose
   mention of the old path stay, because a record surface records what was true.
   This is precisely what WI-288's archival relinker did automatically until it
   died with `agent_dispatch.py` at Phase 5; with the machinery gone the choice
   was a manual four-line retarget or a knowingly red bar.
2. **The "specs-of-record mirror the terminal folders" half of §B2 was NOT
   built,** and needs its own row. Relocating `docs/archive/specs/` into
   `complete/` + `cancelled/` subfolders means rewriting 154 inbound links, 109
   of them inside `docs/log.md` — the surface a work branch may not edit — and
   the relinker that would have done it mechanically is the same one that died at
   Phase 5. A partial move would leave three homes and answer
   "shipped or cancelled?" for none of them, which is worse than either end
   state. Everything else in the row is complete.

**Two measured baselines re-stamped, reasons in place.** `docs/dupes-allow`:
three fingerprints moved when the F5 reader block changed in all three copies at
once (`506ee17be858`→`221f967454e5`, `a73be88000c3`→`e781cf6ec0e8`, and
`6b98b4c1e7c5`→`a986f553a391` for the `plan_briefs == schedule` pair, whose edit
was to `schedule.py`'s module docstring, not the shared block). The class did not
grow — the block SHRANK by the deleted validator. Module linecounts:
`check_trajectory` 3098→3116, `bootstrap` 2232→2241, `agent_common` 1720→1728,
`check` 1523→1524 — all vocabulary plus the comments recording why `draft/` must
be declared.

**Tests: the deletions took their tests with them; four guards added.** New:
`test_each_terminal_state_is_its_own_directory` and
`test_a_leftover_disposition_key_is_inert_not_authoritative` (the deleted
attribute stays deleted); `test_draft_is_never_ready_exactly_like_deferred` +
`test_draft_is_never_ready_and_keeps_its_own_reason_code` (so a later edit
folding `draft` into `deferred` reds rather than quietly losing the distinction);
`test_a_drafted_id_is_visible_to_the_registry_and_so_reserved`, which asserts
BOTH halves of the ruling — the declared folder is seen by the readers and by the
duplicate-id guard, and the same spec in an undeclared folder reads as an empty
registry; `test_the_retired_archive_directory_is_now_refused_by_name`, which is
the composed-tree hazard (a sibling branch closing into the directory this row
deletes) pinned as a LOUD named error rather than a silent skip; plus
`test_a_draft_wi_is_open_and_valid` / `…_with_a_filled_deliverable_fails_ra` and
the draft/cancelled dashboard-bucket guards. All construct their own tree rather
than inheriting this repo's registry.

One test was narrowed with a recorded reason:
`test_a3_js_detail_maps_mirror_the_declared_palettes` now skips the `shipped`
document (WI-372's truth-times rule). The committed `PROJECT_STATE.html` was
written by an older renderer against an older palette, so a vocabulary RENAME
reds through the stale copy while the emitter under test is clean — the exact
mis-triage that helper's docstring warns about. No replacement fixture is owed:
every fresh document emits both colour maps and the per-document `seen >= 2`
floor keeps it non-vacuous.

**Scaffold surface — verified by BOOTSTRAPPING A SCAFFOLD** (the WI-280 lesson,
because nothing in-repo can catch a MAPPING/scaffold omission).
`bootstrap.py --dest <tmp>` created all six status directories; a queued spec
plus a draft spec read `ready` and `excluded:draft`; `integrate.py claim --wi
WI-001 --branch wi-001-probe` cut the branch and moved the spec into
`active/<branch>/`; the close moved it to `complete/` and
`check_trajectory --strict` read `clean (2 work item(s), 1 done (50%))`. A stray
`archive/` spec dropped into the same scaffold exits 1 with
`'archive' is not a status directory (the spec form knows only active,
cancelled, complete, deferred, draft, queued)`.

**Reconciliation note for the integrator.** This branch DELETES
`docs/work/archive/`. `wi-380` and `wi-386` were cut before it and will each
close by moving their spec into that directory, so a composed tree may hold
stray `docs/work/archive/*.md`. That is handled in code, not by luck: the
readers refuse an undeclared status directory by name and `check_trajectory`
exits 1, so it cannot merge silently. **The fix is to `git mv` any late arrival
into `docs/work/complete/`** (or `cancelled/` if it was retired), which is the
same rule ADOPTING.md now states for downstream repos.

**Bars.** Full suite `1712 passed, 12 skipped, 1 failed` (7:11 wall, `-n auto`);
the one failure is the standing work-branch expectation
`tests/test_check_lane.py::test_this_repo_is_not_a_work_branch`, which asserts
this checkout is NOT a claimed work branch and therefore fails on every work
branch by construction. Smoke `557 passed, 4 skipped, 1 failed` (same one).
`ruff check .` clean; `ruff format --check .` clean (146 files).
`check_docs --stale` exit 0 — note it exited **1 at branch start**, on two
pre-existing broken links to `work/deferred/` in `concurrency-v2.md` (the
directory did not exist in this repo); materializing the declared status
directories as `.gitkeep`s, which this row owed anyway, fixed them.
`check_trajectory --strict` exit 0: `388 work item(s), 363 done (94%),
16 cancelled, graph acyclic` (warnings pre-existing and unchanged).

**Byte deltas on budgeted files.** `AGENTS.template.md` 9,991 → 9,991 (unchanged;
the 10,000-byte budget keeps its 9 bytes of headroom). `PROCESS_OPTIONS.md`
163,157 → 163,834 (+677: the lifecycle sentence, the registry paragraph,
`Status ∈ {…}`, R-A and R-F); `PROCESS.md` unchanged.
