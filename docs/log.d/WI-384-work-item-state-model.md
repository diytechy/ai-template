## 2026-08-01 — WI-384: state is the folder — `archive/` splits, `disposition` is deleted

The work item's state is now its DIRECTORY and only its directory. Two
vocabularies, and they are not the same list — REVIEW-A round 1 caught this
record surface conflating them. Six **directories**:
`draft/ queued/ active/ deferred/ cancelled/ complete/`. Seven **statuses**:
`draft, queued, active, done, deferred, blocked, cancelled` — `complete/` maps
to the status `done` (the word every consumer already speaks, deliberately not
renamed by this row), and `blocked` has no directory at all, being derived from
`queued/` plus a `blockref`. `complete` is never a Status value. Spec of
record:
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
DECLARED status directory rather than a scratch folder. `draft` is never-ready
in the scheduler exactly like `deferred` and differs only in what it says.

**The ruled rationale for declaring `draft/` was checked at REVIEW-A round 1 and
is PARTLY FALSE — the conclusion stands, the reason has to be restated, and
[WI-390](../concurrency-v2.md)'s prose sweep should inherit the correction
rather than the error.** [`concurrency-v2.md`](../concurrency-v2.md) §B3 calls
id reservation "the strongest argument", on the premise that a draft in an
undeclared folder is *"invisible to `max(id) + 1`"* so the next mint would
reissue its id. Driven on two temp trees, and it is not so: the shipped mint is
`plan_artifacts._existing_wi_nums` -> `wi_convert.spec_paths`, an **unfiltered**
`rglob("WI-*.md")` that never consults `SPEC_STATUS_DIRS` and only regex-matches
the FILENAME. `docs/work/draft/WI-042-held.md` and the same spec at an
undeclared `docs/work/thinking/WI-042-held.md` both yield `[42]` and both mint
`WI-043`. Identical. The mint is safe either way.

What IS true — and what the branch's own guard actually asserts — is the other
half: everything downstream of `read_spec_rows` goes blind, because that reader
DOES filter. In the same drive, the declared folder returns `['WI-042']` and the
undeclared one returns `[]`, so the validator's duplicate-id integrity finding
and the dashboard never see the held id at all. So the accurate statement is:
**the declaration is what makes the reservation CHECKED rather than incidental**
— today an undeclared folder holds its id only by the accident that one writer
happens to scan unfiltered, and nothing would report a collision if that
accident stopped being true. That strengthens the ruling rather than weakening
it, and it is now the wording at all ten transcription sites (the three F5
copies, `bootstrap.py`, `ADOPTING.md`, `PROCESS_OPTIONS.md`, `README.md`, the
`WI-000` template + its dogfooded copy, and both this row's test docstrings).
`concurrency-v2.md` itself is a RULED design doc and is left for the owner —
this fragment is the correction's home.

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
   built.** It is now filed as **WI-391** in `docs/work/queued/`. Re-measured at
   REVIEW-A round 1, because the first figure here ("109 in log.md") was
   unreproducible by any counting method and is superseded: a reference of the
   form `archive/specs/<name>.md` occurs **154 times repo-wide** across 30 files
   (`*.md`/`*.py`/`*.csv`/`*.html`), of which **101 are markdown link TARGETS** —
   the quantity a relocation actually has to rewrite. `docs/log.md` alone holds
   **119 occurrences on 101 lines, 92 of them link targets** over 61 unique
   targets, and 111 files sit in `docs/archive/specs/`. That bulk lands in the
   one surface a work branch may not edit, and WI-288's relinker — which did
   this mechanically — died with `agent_dispatch.py` at Phase 5, so rebuilding
   it is WI-391's probable predecessor. A partial move would leave three homes
   and answer "shipped or cancelled?" for none of them, so the row is
   all-or-nothing by construction. Everything else in WI-384 is complete, and
   the reviewer judged the split legitimate rather than a dropped half: unlike
   the registry, `docs/archive/specs/` carries no state attribute, so mirroring
   it deletes no machinery and makes nothing unrepresentable — it is navigation.

**Two measured baselines re-stamped, reasons in place.** `docs/dupes-allow`:
three fingerprints moved when the F5 reader block changed in all three copies at
once (`506ee17be858`→`221f967454e5`, `a73be88000c3`→`e781cf6ec0e8`, and
`6b98b4c1e7c5`→`a986f553a391` for the `plan_briefs == schedule` pair). The third
entry's recorded reason was WRONG and is corrected: I had blamed
`schedule.py`'s module docstring; isolating the change on an otherwise-base tree
shows the ~38-token block OPENS at the module constant, and renaming
`_RETIRED = "retired"` to `_NEVER_READY = ("deferred", "draft")` *alone*
reproduces `a986f553a391` exactly. The edit is inside the matched block. The
class did not grow — the two `agent_common` blocks SHRANK (968→918 and 970→920
tokens) by the deleted validator, and the census is 164 blocks at base and 164
at HEAD, same three pairs. Module linecounts:
`bootstrap` 2232→2243, `agent_common` 1720→1731, `check` 1523→1524, and
`check_trajectory` 3098→3119 on this branch, re-measured to **3251** at the
merge (see the reconciliation above) — all vocabulary plus the comments
recording why `draft/` must be declared, the last +3/+2/+3 of it being round 1's
corrected rationale (pure comment lines, zero code tokens; round 2 re-measured
this by the round-1 method and confirmed +0 code tokens on all three, with an
AST-with-docstrings-stripped comparison identical base→tip for all four
scripts). Two of the four modules got SMALLER in code mass while their baselines
rose (`check_trajectory` −38 significant tokens, `agent_common` −43), so these
are registration, not greening.

**Two more corrections at REVIEW-A round 2, both re-driven first.** (a) WI-391
pointed its future builder at `_spec_of_record`, which exists nowhere in the
kit; the archived glob lives in `_own_spec` (`check_trajectory.py:1770`, glob at
:1791, two call sites). Since that row is the only record the §B2 remainder is
owed, both of its code pointers now carry file:line and resolve. (b) The
corrected `draft/` clause was right in the F5 comments, which scope it to an
undeclared directory *under* `docs/work/`, and over-general in the one
adopter-facing copy, which said "an improvised folder". Driven on a fresh
scaffold with one spec in three places:
`docs/work/draft/` and `docs/work/thinking/` both give `_existing_wi_nums=[0,42]`
-> next mint `WI-043`, while `docs/drafts/` gives `[0]` -> next mint `WI-001`,
which really would reissue the held id. And the validator inverts: the
undeclared directory under `docs/work/` exits 1 naming it, while the folder
outside reads `clean (no work items …)` and exits 0. ADOPTING.md now states
BOTH cases, because together they are the strongest form of the ruling rather
than a retreat from it — there is nowhere else safe to put a draft: inside
`docs/work/` the registry reads empty but the harness is loud; outside it the
id collision is real and the harness is silent, which is the worse failure.

**ADOPTING.md's migration recipe cited the wrong flag** and is corrected
(REVIEW-A round 1): it named `git log --follow` as the staleness clock, but the
shipped reader is `--follow --diff-filter=AM` and needs BOTH. Driven on this
very migration — for `docs/work/complete/WI-374-…` the pair answers
`2026-07-31 02:17` (its true pre-migration date) while `--follow` alone answers
`2026-08-01 00:56`, the rename commit, and `--diff-filter=AM` alone answers the
same wrong thing. This one ships to adopters, so the wrong flag would have
taught every migrating repo to check the trap with an instrument that cannot
see it.

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

**The reconciliation this row predicted, and then paid.** The fragment said it
before it happened: this branch DELETES `docs/work/archive/`, `wi-380` and
`wi-386` were cut before it and close by moving their spec into that directory,
so a composed tree would hold stray `docs/work/archive/*.md` — handled in code
rather than by luck, because the readers refuse an undeclared status directory
by name and `check_trajectory` exits 1. WI-380 merged to trunk first and the
merge queue refused this branch with exactly that conflict, plus one more.
Both were resolved here, on the worker's side, after REVIEW-A round 2:

- **`docs/work/archive/WI-380-…` (file location).** Git's own rename detection
  proposed the answer the note states, and it is the answer taken: the spec sits
  at `docs/work/complete/`, byte-identical to trunk's archived copy (sha256
  `3cbe6dcbc0622b20` either side), `docs/work/archive/` is in neither the tree
  nor the index, and `check_trajectory --strict` reads clean — the
  undeclared-directory error staying SILENT is what confirms the directory is
  gone rather than merely emptied.
- **`tests/test_module_size_ratchet.py` (content).** WI-380 re-stamped
  `check_trajectory.py` to 3230 and this row to 3119, both from the same base
  3098 on parallel branches. Resolved by RE-MEASURING the merged file with the
  census's own metric (`len(text.splitlines())`) rather than picking a side:
  **3251**, which is exactly `3098 + 132 (WI-380) + 21 (WI-384)`. The two
  changes are disjoint, so the arithmetic checks the resolution instead of
  merely agreeing with it, and both reason chains are preserved verbatim at the
  entry — neither WI's record was dropped to make the number fit.

Trunk's generated artifacts (`PROJECT_STATE.html`, `docs/gate`,
`docs/status.md`, `docs/architecture.md`) came in through the merge and were NOT
regenerated here — `git diff ConcurrencyTrainRewrite` over all four is empty —
and `docs/log.md` still differs from trunk by exactly the four link targets
round 1 accepted, and nothing else.

**Worth naming, because it is the cost this program is removing:** none of the
above is a defect in either branch. Two lanes each did the right thing from the
same base and the conflict surfaced at the queue, where it is most expensive.
Under WI-386's station protocol the lane refreshes onto trunk and bars there, so
this would have been resolved once, on the builder's side, before the queue ever
saw it. This branch is the last one that pays it.

**Bars (final, on the merged tree).** Full suite `1718 passed, 12 skipped,
1 failed` (6:18 wall, `-n auto`; 1712 before the merge — the +6 are WI-380's
tests arriving with it);
the one failure is the standing work-branch expectation
`tests/test_check_lane.py::test_this_repo_is_not_a_work_branch`, which asserts
this checkout is NOT a claimed work branch and therefore fails on every work
branch by construction. Smoke `557 passed, 4 skipped, 1 failed` (same one).
`ruff check .` clean; `ruff format --check .` clean (146 files).
`check_docs --stale` exit 0: `338 doc(s), 964 intra-repo link(s), 0 broken` —
note it exited **1 at branch start**, on two pre-existing broken links to
`work/deferred/` in `concurrency-v2.md` (the directory did not exist in this
repo); materializing the declared status directories as `.gitkeep`s, which this
row owed anyway, fixed them, and trunk independently retargeted the same links.
`check_trajectory --strict` exit 0: `389 work item(s), 364 done (94%),
16 cancelled, graph acyclic` (389 counts WI-391, the remainder row this branch
files; 364 counts WI-380 arriving through the merge; warnings pre-existing and
unchanged).

**Byte deltas on budgeted files.** `AGENTS.template.md` 9,991 → 9,991 (unchanged;
the 10,000-byte budget keeps its 9 bytes of headroom). `PROCESS_OPTIONS.md`
163,157 → 163,834 (+677: the lifecycle sentence, the registry paragraph,
`Status ∈ {…}`, R-A and R-F); `PROCESS.md` unchanged.
