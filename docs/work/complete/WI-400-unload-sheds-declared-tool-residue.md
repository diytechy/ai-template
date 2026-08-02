+++
id = "WI-400"
title = "THE UNLOAD MUST DISTINGUISH DECLARED TOOL-RESIDUE FROM EVIDENCE - today every worker-built lane ends 'UNLOAD INCOMPLETE', forever. MECHANISM: integrate's unload reads dirt with git status --porcelain --ignored=matching, so a __pycache__/ or .pytest_cache/ counts among 'files that may exist nowhere else', while _shed_residue sheds only what the REFRESH'S OWN bar added (its docstring says so) - so any lane whose worker ever ran the suite arrives at the merge slot permanently dirty, and the refusal fires on every merge with nothing anyone did wrong. MEASURED (2026-08-01, handoff-2026-08-01.md §6): all four session lanes were removed by PLAIN git worktree remove, no --force and no manual cleanup, because git's own cleanliness test ignores ignored files - the integrator refuses an unload git itself performs safely, on every lane, always. THE ORPHAN CHECK IT PROTECTS IS REAL and must not be loosened (the 2026-07-26 lesson: a deleted worktree held two session logs that existed nowhere else) - so make the DISTINCTION representable instead: shed the small DECLARED tool-residue set (the caches and generated outputs the bar itself creates - the same names every lane showed: .pytest_cache, .ruff_cache, __pycache__ trees, the generated test report), then treat ANY remainder as potential evidence and keep refusing, naming it. A SECOND DRIVEN FACT FROM THE SAME DAY, same surface: git worktree remove run from INSIDE the lane fails 'Permission denied' AFTER half-unregistering the worktree, leaving an empty directory (the WI-397 close) - so the unload arm must run from outside the lane's directory, a one-line constraint on the caller. DONE-WHEN, driven end-to-end: a lane dirtied only by cache/generated residue unloads clean through integrate's own arm with no --force anywhere; a lane holding ONE untracked real file still refuses and names the file; and the inside-the-lane invocation is made safe or unrepresentable. SCOPE GUARD: the declared-residue set is a short enumerated list co-located with what the bar already generates - not a glob-configuration surface, and not a new dial."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

**Built 2026-08-02 (commit b9faefd3).** The §5.6 unload now distinguishes
declared tool-residue from evidence. `integrate.py`'s `_unload_branch` sheds a
DECLARED residue set before judging dirtiness — `_RESIDUE_DIR_NAMES`
(`.pytest_cache`, `.ruff_cache`, `__pycache__`) plus `_RESIDUE_FILES`
(`docs/test/report.md`), the exact names every lane of the 2026-08-01 drain
was held by — via `_is_declared_residue` +
`_shed_declared_residue`/`_sweep_residue_dirs`: a short enumerated list
co-located with the unload, not a glob-configuration surface and not a dial.
The shed is locked twice (a path must be git-IGNORED via `ignored_files` AND
match the declaration — an untracked-but-trackable file is a surprise, and a
surprise is evidence), deletes nothing when git cannot enumerate, and rmdirs
only now-EMPTY directories inside declared cache trees. The orphan read is
NOT loosened: any remainder — an ignored `out/run-logs/` session stream, one
untracked real file — still refuses with the byte-identical honest message,
naming it, and the repo-root `out/` (WI-398's refresh-refused logs, outside
any lane) is never reached. The second driven fact is closed too:
`_unload_branch` steps out of the lane (`os.chdir(root)`, guarded on the
resolved cwd) before `git worktree remove`, so the inside-the-lane invocation
that half-unregistered the WI-397 worktree is now safe.

Done-when, driven end-to-end in `tests/test_integrate.py` (5 new tests, 4
watched red on the pre-implementation tree — the shed test failing on the
drain's verbatim refusal, "DIRTY (6 uncommitted or ignored path(s))"): a lane
dirtied with exactly the measured six-path residue set unloads clean through
the integrator's own arm with no `--force` anywhere; the same lane plus ONE
untracked file refuses and names it (and no longer names the shed caches);
the ignored-stream and root-`out/` boundaries hold; the inside-the-lane
unload leaves the process standing in a directory that exists. Scope guard
held: no new policy surface; `docs/test/report.html` deliberately left
undeclared (the 2026-08-01 drain lanes ran plain `trace.py`, which writes
only the markdown report, so the measured set never showed the html one —
widen only if measured). **Record correction 2026-08-02 (WI-407, REVIEW-A
finding 2):** the parenthetical above originally read "the bar never
generates it" — FALSE, corrected in place: `check.py` passes `--html` to its
trace step at G2/G3 (check.py:449-455, in the bar since 2026-06-28), so the
declared bar writes the html report in whatever lane it runs in; what was
true is only the narrower drain fact now stated. The exclusion DECISION
stood on the honest scope guard regardless (enumerate the measured set,
widen only on measurement) — and on 2026-08-02 the wi-402 lane was measured
holding the file at unload, so WI-407 declared it into `_RESIDUE_FILES`
under the same double-lock, with a test; the absence ledger
(`docs/declared-absences`) now carries the path beside the markdown
report's row. Class B
registration judgment: internals of the LLR-140/SR-132 unload, no new rows
owed; size ratchet re-stamped 1977 → 2079 with reason in the baseline
comment. Totals on the build commit, 2026-08-02:
`tests/test_integrate.py` 113 passed in 20.34s, smoke tier 615 passed / 6
skipped in 10.40s.
<!-- fig: cmd="python -m pytest -q -n auto tests/test_integrate.py" rev=b9faefd3 -->
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=b9faefd3 -->
Session record: the log fragment `docs/log.d/` (compiled into `docs/log.md`
at merge).
