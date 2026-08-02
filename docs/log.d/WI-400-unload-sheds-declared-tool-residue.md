## 2026-08-02 — WI-400: the unload sheds declared tool-residue, keeps refusing on evidence

**Summary.** §5.6's unload reads dirt with `git status --porcelain
--ignored=matching` — correctly, since the 2026-07-26 lesson's sole-copy files
are the ignored kind — but `_shed_residue` sheds only what the REFRESH'S OWN
bar added, so a lane whose worker ever ran the suite arrived at the merge slot
permanently dirty. Measured in the 2026-08-01 drain: five of five lane merges
(WI-395/394/393/392/398/399's stations) exited 1 at unload over the IDENTICAL
six ignored paths — `.pytest_cache/`, `.ruff_cache/`, `__pycache__/`,
`docs/test/report.md`, `project-trajectory/scripts/__pycache__/`,
`tests/__pycache__/` — pure tool caches plus the gitignored generated trace
report, and every worktree was removed by hand.
<!-- fig: derived="the 2026-08-01 drain record: backlog-plan-2026-08-01.md row 9 + handoff-2026-08-01.md §6, this WI's spec evidence" -->
The distinction is now representable: `_unload_branch` sheds the DECLARED
tool-residue set, then judges again on what is actually left — and anything
outside the declaration still refuses exactly as before, naming it.

**Deliverables.**

- **The declared residue set and its shed** (`integrate.py`:
  `_RESIDUE_DIR_NAMES` = {`.pytest_cache`, `.ruff_cache`, `__pycache__`} +
  `_RESIDUE_FILES` = {`docs/test/report.md`}, consumed by
  `_is_declared_residue` + `_shed_declared_residue`/`_sweep_residue_dirs`): a
  short enumerated list co-located with the unload — not a glob-configuration
  surface, not a dial. The shed is locked twice: a path must be git-IGNORED
  (`ignored_files`; an untracked-but-trackable file is a surprise, and a
  surprise is evidence) AND match the declaration; nothing is deleted when git
  cannot enumerate (the `_worktree_dirt` fail direction, kept closed); the
  directory sweep rmdirs only now-EMPTY directories inside declared cache
  trees, so a cache dir still holding an undeclared file survives to be
  reported as the dirt it is. The refusal message for a genuine remainder is
  byte-identical to before.
- **The orphan read, untouched:** an ignored `out/run-logs/` session stream,
  a local `.env`, one untracked file — all still refuse, named. The repo-root
  `out/` (home of WI-398's `refresh-refused-<branch>.log`, outside any lane
  worktree) is never reached: the shed operates only under the holding
  worktree's own path.
- **The inside-the-lane invocation made safe** (the second driven fact from
  the same day, the WI-397 close): `git worktree remove` run from INSIDE the
  lane fails "Permission denied" AFTER half-unregistering the worktree — or,
  where it succeeds, strands the process in a deleted cwd (the Linux/macOS
  shape the new test caught live). `_unload_branch` now steps out of the lane
  (`os.chdir(root)`) before asking for the removal, guarded on the resolved
  cwd actually being inside the lane.
- **Driven, red-then-green** (`tests/test_integrate.py`, 5 new tests, module
  106 → 111 test functions): the drain's holding set reproduced verbatim as
  `MEASURED_RESIDUE` — a lane dirty with exactly those six paths unloads clean
  through the integrator's own arm with no `--force` anywhere; the same lane
  plus ONE undeclared file refuses, names `orphan.txt`, and the note no longer
  mentions the shed caches; the ignored stream + root-`out/` boundary; the
  declared-set predicate as data; and the inside-the-lane unload. Watched red
  first: 4 failed on the pre-implementation tree, the shed test failing on the
  exact drain refusal ("DIRTY (6 uncommitted or ignored path(s))") and the
  inside-invocation test on `FileNotFoundError: os.getcwd` — historical, that
  tree is gone.

**Deviations and judgments.**

1. **No new LLR/TC rows owed** (Class B, the WI-398/WI-399 precedent): no
   module was added; the shed and the cwd guard are internals of the §5.6
   unload inside `integrate_one`'s flow, registered under LLR-140/SR-132, and
   the new tests land beside that row's existing evidence module
   (`tests/test_integrate.py`, TC-132).
2. **`docs/test/report.html` deliberately NOT declared:** `trace.py --html` <!-- path-ok: a generated, gitignored output named to record its EXCLUSION from the declared set; it exists in no tracked tree by design -->
   can generate it, but the bar does not run `--html` and no drain lane showed
   it. The declaration stays exactly the measured set; widening is a one-line
   reviewed edit if it is ever measured.
3. **Complexity ratchet answered by extraction, not a bump:** the first cut of
   `_shed_declared_residue` hit C901 11; the directory sweep split out as
   `_sweep_residue_dirs` (the `_drop_abandoned`/`_merge_refusal` precedent),
   both halves under the ceiling, baseline untouched.
4. **Size ratchet re-stamped upward, reason in the baseline comment:**
   `integrate.py` 1977 → 2079 (+102), roughly half of it the docstrings and
   comments that keep the shed narrow.
   <!-- fig: derived="len(text.splitlines()) at b9faefd3, the ratchet's own metric (tests/test_module_size_ratchet.py)" -->
5. **Pre-existing trunk red, unchanged:** the commit-bar `check_docs.py
   --stale` run reports the same 4 broken links in three closed specs
   (`docs/work/complete/` WI-070 / WI-173 / WI-288) that WI-399's session
   recorded — byte-identical on trunk, inherited, outside this row's scope.

**Byte budgets:** none of the budget-watched docs touched (no
`AGENTS.template.md` / `PROCESS.md` / `PROCESS_OPTIONS.md` edits).

**Watched, measured on the build commit b9faefd3:**
`tests/test_integrate.py` 113 passed in 20.34s
<!-- fig: cmd="python -m pytest -q -n auto tests/test_integrate.py" rev=b9faefd3 -->
smoke tier 615 passed, 6 skipped in 10.40s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=b9faefd3 -->
