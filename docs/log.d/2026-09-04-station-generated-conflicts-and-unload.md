## 2026-09-04 — The station settles [generated] conflicts, and build residue stops refusing the unload

Two defects measured three times each during that day's queue drain, both in
`integrate.py`, both fixed where the machinery already had the declaration it
needed. Neither changes what a lane owns; each removes a hand-resolution the
supervisor performed identically every time.

### 1. A refresh conflict confined to declared generated artifacts

Three lane refreshes refused with "merging trunk … in CONFLICTS" where the ONLY
conflicted paths were artifacts BOTH sides had regenerated — `PROJECT_STATE.html`
and `docs/ratify/CURRENT.md` — and the supervisor resolved each identically:
take the trunk side, re-run the trunk step. There is no content question in that
conflict, because `_run_trunk_step` regenerates every one of those files from
source seconds later, over whichever side sits in the tree.

`refresh` now lists the conflicted paths (`git diff --name-only --diff-filter=U`)
and takes the TRUNK side of every one that is DECLARED in `docs/stack.ini`
`[generated]`, then falls through into the trunk step exactly as a clean merge
does. The declaration is READ, never restated: `_generated_table` parses the
section into `{path: kind}` (a `"/"`-terminated row is a prefix, a marker pair
keeps only its kind) and `_generated_paths` — the RULING-6 audit's reader — is
now two lines over it, so there is still one parser in this module.

Two locks hold it narrow. A path must be in the §5.2 trunk-only set, which a
lane may not commit at all; and its kind must not be hand-stamped. **The one
kind held back is `linecounts` — `tests/test_module_size_ratchet.py`, this very
change's other subject.** Its rows are measured-and-classified data re-stamped
BY HAND with a reason: no command re-derives them, both sides of a conflict
carry a reviewed reason, and taking trunk's would silently drop the lane's. Any
path git will not resolve that way (a delete/modify conflict has no "their
version") stays in the remainder. A remainder — a product-code conflict — still
refuses with the same message the lane has always seen, plus the list of
generated paths that were settled first, so the remainder is not read as the
whole conflict; the undo throws the resolutions away with the rest. A merge that
failed with NO conflicted path at all (a refused merge) resolves nothing and
therefore continues nothing.
Tests: `test_a_conflict_only_on_declared_generated_paths_refreshes_green`,
`test_a_product_file_conflict_still_refuses_and_names_what_was_resolved`,
`test_a_hand_stamped_linecounts_conflict_still_refuses`,
`test_the_generated_table_reads_kinds_and_prefixes_not_a_second_copy`.

### 2. An ignored `.venv/` is not evidence

Three merged lanes ended `UNLOAD INCOMPLETE … DIRTY (1 uncommitted or ignored
path(s))` where the one path was the lane's own `.venv/`, the run exited 1 with
`INCOMPLETE - 1 merged branch(es) NOT unloaded` after every merge, and each
worktree came off by hand with `git worktree remove --force`.

This is the third measured shape of the same lesson, after the 2026-08-01 tool
caches and the 2026-08-30 loop streams, and it takes the same short enumerated
answer rather than a glob: `.venv/`, `__pycache__/`, `.pytest_cache/`,
`.ruff_cache/` and `.coverage*` are BUILD RESIDUE — rebuilt from a manifest,
sole-copy evidence never — and never count as dirt. Everything else keeps the
caveat verbatim, an ignored `out/run-logs/` stream included, because a worktree
can hold files that exist nowhere else.

Where the earlier residue is SHED, this is merely not counted: `git worktree
remove` deletes an ignored path with the lane (measured — an ignored path does
not refuse the removal), so walking a five-thousand-file virtualenv to unlink it
first would buy nothing. The exception is a `.venv` that is a SYMLINK into a
shared virtualenv, the shape this Mac's lanes carry: the shed unlinks the LINK
under `os.path.islink` and never walks through it, because what it points at
lives outside the lane and is not ours to delete. The double lock is unchanged —
git must report the path as IGNORED and the name must be declared — and the
synthetic line `_worktree_dirt` returns when git cannot answer at all is prose,
not a path, so it still reads as dirt.
Tests: `test_a_merged_lane_holding_only_its_own_venv_unloads`,
`test_a_stray_ignored_file_beside_the_venv_still_refuses`,
`test_a_symlinked_venv_unloads_without_following_the_link`,
`test_the_build_residue_allowlist_is_short_and_named`.

**The module-size ratchet is re-stamped, `integrate.py` 1361 → 1426 SLOC.** The
reason is recorded at the baseline row: the kit's scripts may not import one
another, so a helper for a station behaviour has no home short of `kitlib`, and
roughly half the delta is the recorded WHY — which kind is held back and why a
symlinked `.venv` is never followed — that a successor would otherwise
re-litigate. The extractions were compacted before the stamp was taken, and six
of the lines are a DECOMPOSITION rather than the feature: the merge arm moved
out to `_merge_trunk_in` because the conflict handling took `refresh` C901
10 → 11, so the complexity ratchet is untouched by this change.

Deferred open items: none — both defects are closed at their root with tests,
and neither fix leaves a follow-on: the auto-resolve reads a declaration that
already exists and the allowlist is enumerated, so a new generated artifact or a
new cache name is covered (or deliberately not) by the same one row it is
declared in.
