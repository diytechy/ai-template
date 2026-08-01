+++
id = "WI-384"
title = "RULED 2026-07-31 (docs/concurrency-v2.md workstream B) - the design is ruled into log.md's Decisions, so this row is CLAIMABLE. Replace the work-item state vocabulary so STATE IS THE FOLDER, with no attribute duplicating it. Before: queued|active|deferred|archive plus a `disposition` frontmatter key. After: draft|queued|active|deferred|cancelled|complete. The `disposition` key exists for exactly one reason - archive/ holds two terminal states and the folder cannot express which - so it needs an attribute AND parse_spec_status()'s cross-check to keep the two honest, with two raise paths (unknown disposition, retirement filed outside archive/) and their tests. Splitting archive/ into complete/ and cancelled/ DELETES the attribute, the validator, both raise paths and the tests: the inconsistent state stops being checked-for and becomes unrepresentable. This is the cleanest test of the design's governing principle. Two vocabulary fixes ride along: `retired` is ambiguous (it can read as finished-and-put-out-to-pasture) and becomes `cancelled`, which cannot; and `draft/` gives thinking-in-progress an honest home - today there is none, so a design still under discussion sits in deferred/, which reads as A DECISION (we decided not to do this now) rather than as THE ABSENCE OF ONE (still being figured out). THESE VERY ROWS ARE THE WORKED EXAMPLE: while the concurrency-v2 design was open they sat in deferred/ for want of a draft/, and they moved to queued/ the moment it was ruled - so the mis-filing ended, but only because the thinking finished, and the next design to open has the same nowhere to sit until this row lands. draft is never-ready in the scheduler, exactly like deferred, and differs only in what it SAYS. Specs-of-record mirror the terminal folders instead of one docs/archive/specs/, so a spec's location answers shipped-or-cancelled without opening it. THE draft/ QUESTION IS RULED (2026-07-31) AND THE DECIDING REASON IS ID RESERVATION, not somewhere to think. Note first that there is NOTHING TO KEEP IN SYNC: the spec frontmatter carries no status key at all - Status is synthesised from the directory at read time - so folder/frontmatter divergence is ALREADY unrepresentable, and disposition is the single one-key exception this row deletes. But read_spec_rows walks <status>/WI-*.md, parse_spec_status RAISES on a directory not in SPEC_STATUS_DIRS, and read_spec_rows then SKIPS that file - so parking drafts in an UNDECLARED folder makes them invisible to max(id)+1, to the duplicate-id guard and to the dashboard, and the next mint would hand out an id a draft already holds. WI-388's mechanical adjudication minting is exactly such a mint, running with nobody watching, so declaring draft/ is what makes an id reservation real. RETIRED AND CANCELLED ARE ONE STATE, ONE RENAME APART - state this plainly because it is live the moment anything retires before this row lands. Today's shipped vocabulary has exactly ONE won't-build terminal, spelled disposition = retired and living in archive/; cancelled/ is that same state after this row renames it and gives it a folder. So anything retired BEFORE this lands correctly writes retired (the only spelling the readers, the scheduler's _TERMINAL_DISPOSITION and check_trajectory's R-A/R-F rungs accept), anything retired AFTER writes nothing at all because the folder is the whole statement, and the migration is mechanical and already in scope here. WI-382 and WI-385 (retired 2026-07-31, subsumed by WI-386 and folded into WI-388) are simply two of its INPUTS - and a useful pair, since both carry a real reason and so prove the migration preserves the RECORD rather than just the state. The rename is not cosmetic: retired can be read as finished-and-put-out-to-pasture, cancelled cannot, and those two rows are exactly the case that would be misread - subsumed work that never shipped. COST, stated honestly: SPEC_STATUS_DIRS is triplicated across the three F5 readers (agent_common 3, check_trajectory 4, schedule 3 references) plus wi_convert.py, the scheduler's terminal-state logic and tests; the driver must treat draft as never-ready; existing archive/ rows migrate by disposition; downstream repos owe a migration step. Independent of the concurrency workstream, so it can proceed in parallel. RE-AFFIRMED 2026-07-31 against the concurrency-v2 §A9.1 addition (the program-close row WI-390): that section adds a NEW row's scope - the spine amendment, connectivity, prose and stamps that no single builder can own - and changes nothing in this row's own scope, so this row stands as written."
workstream = "process"
buildtier = "medium"
safety_class = "ordinary"
+++

## Deliverable

Work-item state IS the folder, with no attribute duplicating it: the directory
is now the WHOLE statement rather than most of it. Two vocabularies, and they
are not the same list. Six **directories** —
`draft/ queued/ active/ deferred/ cancelled/ complete/`. Seven **statuses** —
`draft, queued, active, done, deferred, blocked, cancelled`, where `complete/`
maps to the status `done` (the word every consumer already speaks; renaming it
was out of scope and deliberately not done) and `blocked` has no directory at
all, being derived from `queued/` plus a `blockref`. `complete` is never a
Status value.

**What was DELETED** (the point of the row, not a side effect): the
`disposition` frontmatter key; `parse_spec_status()`'s attribute/folder
cross-check in all three F5 reader copies; both of its raise paths (unknown
disposition, retirement filed outside `archive/`); `wi_convert`'s
`status_from_location` disposition arm and its `RETIRED`/`ARCHIVE` constants;
and the four tests that only proved that validator
(`test_retirement_is_archive_plus_a_disposition`,
`test_a_retired_spec_outside_archive_is_refused`, and the `unknown-disposition`
entry in the malformed-spec table, which drove two parametrized cases). Nothing
was kept "just in case": `parse_spec_status(relpath)` no longer takes the
frontmatter at all, so a stale `disposition` key on a spec merged from an older
branch is inert data that CANNOT contradict the location — proven by
`test_a_leftover_disposition_key_is_inert_not_authoritative`. `status_dir` and
`status_from_location` are now inverses of one table (`STATUS_DIRS` /
`DIR_STATUSES`), so the mapping is a bijection and there is no second fact to
keep honest.

**Readers repointed** — the row's stated cost, measured: `SPEC_STATUS_DIRS` is
triplicated verbatim across `agent_common.py`, `check_trajectory.py` and
`schedule.py` (the F5 rule; `tests/test_wi_loader_sync.py` pins the three
byte-equal), plus `wi_convert.py`'s write-side table. Beyond the four:
`agent_common.TERMINAL_STATUSES` + the worker's terminal-assignment refusal;
`schedule.py`'s `_TERMINAL_DISPOSITION`, `_waiting_reasons` dead-edge code and
the new `_NEVER_READY` arm; `check_trajectory.py`'s `OPEN_STATUSES` /
`TERMINAL_STATUSES` / `KNOWN_STATUSES`, R-A, R-F, the R-D forward-only rule,
`dead_dependency_findings` and the clean-summary count; `traj_render.py`'s
`STATUS_FILL` / `STATUS_BUCKET` / `STATUS_GLYPH`; `gen_trajectory.py`'s
`--cancelled` CSS token, legend and hero clause; `traj_panels.py`'s next-work
open-set test; `bootstrap.py`'s `GITKEEP_DIRS`; and the close-ritual prose in
`integrate.py` / `check.py`.

**`retired` -> `cancelled`** everywhere the WI *status* is meant (prose uses of
"retired" meaning *removed* were left alone — the word is load-bearing in this
repo's history). **`draft/`** is a declared status directory, never-ready in the
scheduler exactly like `deferred` and carrying its own disposition + reason code
so the two stay distinguishable in `--explain`.

**The ruled rationale for the declaration was CHECKED at REVIEW-A round 1 and is
partly false; the conclusion stands and the reason is restated at all ten
transcription sites.** §B3 called id reservation "the strongest argument" on the
premise that a draft in an undeclared folder is invisible to `max(id) + 1`.
Driven on two temp trees: it is not. The shipped mint
(`plan_artifacts._existing_wi_nums` -> `wi_convert.spec_paths`) is an unfiltered
`rglob("WI-*.md")` that never consults `SPEC_STATUS_DIRS` and matches on the
FILENAME, so a spec at draft/WI-042-held.md and one at an undeclared
thinking/WI-042-held.md
both mint `WI-043` — identical. What DOES go blind is everything downstream of
`read_spec_rows`, which filters: the same drive returns `['WI-042']` for the
declared folder and `[]` for the undeclared one, so the validator's duplicate-id
integrity finding and the dashboard never see the held id. The accurate reason:
**declaring the folder makes the reservation CHECKED rather than incidental** —
an undeclared folder holds its id today only by the accident that one writer
scans unfiltered. That is what the counterfactual asserts rather than assumes
(`test_a_drafted_id_is_visible_to_the_registry_and_so_reserved`), and it is now
the wording in the three F5 copies, `bootstrap.py`, `ADOPTING.md`,
`PROCESS_OPTIONS.md`, `README.md`, the `WI-000` template + its dogfooded copy
and both test docstrings. `concurrency-v2.md` is a ruled design doc and is left
to the owner; the correction's home is this row's log fragment, so WI-390's
prose sweep inherits it rather than the error. Deliberately NOT done: filtering
`spec_paths` by `SPEC_STATUS_DIRS` to make the original sentence true — that
would make drafts in an undeclared folder invisible to the mint too, i.e. build
the hazard the clause imagined.

**Migration, mechanical and verified:** 378 specs left `docs/work/archive/` by
`git mv` — 16 to `cancelled/` (every row carrying `disposition = "retired"`,
including WI-382 and WI-385, the two this design retired) and 362 to
`complete/`, with the `disposition` line stripped from the 16. The
backlog-staleness clock (`git log --follow --diff-filter=AM`) was re-derived
over all 362 migrated `complete/` specs afterwards: 0 unresolvable, and every
sampled row still answers its PRE-migration date, so the rename re-dated
nothing. Four link TARGETS in `docs/log.md` naming moved specs were retargeted
(text and prose mentions untouched); `docs/dupes-allow` and the module linecount
baseline were re-stamped with reasons in place.

**Scaffold surface, verified by bootstrapping a scaffold** (the WI-280 lesson):
`bootstrap.py --dest <tmp>` created all six status directories, a queued spec
plus a draft spec read as `ready` and `excluded:draft`, `integrate.py claim`
cut the branch and moved the spec into `active/<branch>/`, the close moved it to
`complete/` and `check_trajectory --strict` read `1 done (50%)` clean. A stray
`archive/` spec — the composed-tree hazard while sibling branches close into the
directory this row deletes — exits 1 naming the file and listing the six
declared directories, which is the reconciliation instruction.

**That hazard then arrived, and was resolved as written.** WI-380 merged to
trunk first, closing into `docs/work/archive/`, and the queue refused this
branch on exactly that conflict. Its spec now sits in `docs/work/complete/`,
byte-identical to trunk's copy, with `docs/work/archive/` gone from tree and
index — confirmed by the undeclared-directory error staying SILENT. The second
conflict was the size ratchet, where WI-380 and this row re-stamped
`check_trajectory.py` from the same base on parallel branches; resolved by
re-measuring the merged file (3251 = 3098 + 132 + 21) rather than picking a
side, with both reason chains preserved.

**Not done, and now filed as WI-391:** the "specs-of-record mirror the terminal
folders" half of §B2. Re-measured at REVIEW-A round 1 (the first figure, "109 in
log.md", was unreproducible and is superseded): a reference of the form
`archive/specs/<name>.md` occurs **154 times repo-wide** across 30 files, of
which **101 are markdown link TARGETS** — the quantity a relocation rewrites;
`docs/log.md` alone holds **119 occurrences on 101 lines, 92 of them link
targets** over 61 unique targets, across 111 archived spec files. That bulk
lands in the one surface a work branch may not edit, and the WI-288 relinker
that once did this mechanically died with `agent_dispatch.py` at Phase 5 —
rebuilding it is WI-391's probable predecessor. A partial move would leave three
homes and answer "shipped or cancelled?" for none of them, so the row is
all-or-nothing. The split is a legitimate remainder rather than a dropped half:
unlike the registry, `docs/archive/specs/` carries no state attribute, so
mirroring it deletes no machinery and makes nothing unrepresentable — §B2 frames
it as answering the question *without opening the file*, which is navigation.

**A gap in the row's own scope-of-consequences, found by the composed-tree bar
(REVIEW-A round 3) and recorded as a miss.** `check_doc_refs.py --strict` is not
in the per-commit bar, so three green rounds did not see that this rename left
dangling path references in prose — 15 on the branch, 8 on the composed tree.
A state-model change retires a PATH, and paths live in prose; the row's
checklist covered the scaffold surface, the readers and the migration, and never
asked which prose now names what it retired. Fixed in three classes, judged
apart rather than blanket-suppressed: `docs/work/archive/` DECLARED in
`docs/declared-absences` on the `work-items.csv` precedent (a registry home
retired by a migration) and deliberately unmarked by `LIFECYCLE:`, so the
materialize-guard stays armed against the very state the loaders refuse;
WI-391's two prospective destinations declared, where that guard is the feature
(when the row lands, the entries must go); and the driven-probe fixture paths
DE-BACKTICKED rather than declared, because they are experiment parameters in a
temp scaffold and no "absent by design" or "history" reason would have been
true of them. Deliberately NOT done: adding the terminal directories to
`check_doc_refs.RECORD_PREFIXES`. I built that, measured it inert (identical
`no dangling · 860 untraced` without it), and reverted — a record prefix widens
a blind spot, and strictness here is what forced `docs/work/archive/` to earn a
declaration with a reason and a guard instead of being silently swallowed. The
full reasoning, the asymmetry that would make it safe if a real case ever
arrives, and a filed seam about `docs/log.d/` are in the log fragment.
