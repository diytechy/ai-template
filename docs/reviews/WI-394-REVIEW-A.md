# WI-394 — REVIEW-A (2026-08-01)

Verdict: APPROVE (round 2 — round 1 was CHANGES-REQUESTED; both findings
remedied by rework commit `3976bb5d` and re-verified below)

Reviewed independently against the spec (`docs/work/complete/WI-394-a-verified-spine-row-can-cite-evidenc.md`),
the R2 ruling (`docs/backlog-plan-2026-08-01.md`, option (c): FILE half only,
`::node` ruled prose, warn-first), and the archived spec-of-record
(`docs/archive/specs/WI-394.2026-08-01.md`). Diff = three commits
(`e1f83167` build, `35c0cdb6` triage, `d21bb6a4` close) on
`wi-394-a-verified-spine-row-can-cite-evidenc` vs `ConcurrencyTrainRewrite`.
`docs/log.d/` was not read; the checker's mechanical output over it is cited
below, which convicts without reading.

## Findings

1. **MAJOR — the branch at HEAD is RED at the very `--strict` step this WI
   arms, and the close commit's pasted green is false at the commit that
   pasted it.** The close commit `d21bb6a4` files
   `docs/log.d/WI-394-a-verified-spine-row-can-cite-evidenc.md`, whose line 57
   backtick-quotes two doc-relative link targets that do not resolve at repo
   root. Run in the worktree at HEAD:

   ```
   check_doc_refs: WARN - docs/log.d/WI-394-a-verified-spine-row-can-cite-evidenc.md:57: `specs/WI-394.md` does not exist in the repo
   check_doc_refs: WARN - docs/log.d/WI-394-a-verified-spine-row-can-cite-evidenc.md:57: `archive/specs/WI-394.2026-08-01.md` does not exist in the repo
   check_doc_refs: 2 dangling reference(s) · 849 untraced (explained: declared absent, kit-relative, or a record surface) — --show-untraced to list.
   ```
   rc=1 under `--strict`. `[step:doc-refs]` is wired `gates = G3` in
   `docs/stack.ini` (`command = {py} project-trajectory/scripts/check_doc_refs.py --root . --strict`),
   and this repo is at G3, so the branch delivers a red G3 harness step.
   `docs/log.d/` is deliberately NOT a record prefix — the tool's own comment:
   "a fragment is judged strictly while its author can still edit it" — so
   this is the check working as designed, on this branch's own close commit.
   Yet the Deliverable states "`check_doc_refs --root . --strict` rc=0 with 0
   dangling" and the close commit message states "check_doc_refs --root .
   --strict rc=0 (0 dangling)". Both were true at the triage commit
   (`35c0cdb6` tree measured: `OK - no dangling ... rc=0`) and are FALSE at
   `d21bb6a4` — the same commit that pasted them invalidated them. That
   violates the "paste the real output; never report a green you didn't
   produce" bar (the green was produced, then un-produced in the same
   commit). Remedy is small and honest: mark the fragment's two quoted
   targets `path-ok` with a reason (the shipped idiom the archived spec
   already uses seven times), or quote resolvable repo-relative paths — then
   re-run the step and re-paste. Not a sanction: the quotation is genuinely a
   record of the relink, and once compiled into `docs/log.md` it would be
   record-surface untraced anyway; the red is real only while the fragment
   sits in `docs/log.d/`, which is exactly the state being merged.

2. **MINOR — the Deliverable's module-suite total does not reproduce.** It
   claims "module suite 39 passed"; the module suite is
   `tests/test_check_doc_refs.py` and running it gives:

   ```
   27 passed in 1.04s
   ```
   (27 = 20 trunk tests + 7 new; no natural pairing reproduces 39 —
   `+ test_dual_plan_round.py` = 34, `+ test_check_dupes.py` = 45.) The close
   commit's smoke figure (582 passed / 2 skipped) also differs from the
   Deliverable's (578 passed / 6 skipped). Nothing here convicts the code —
   the tests that exist pass — but a verification paragraph exists to be
   reproduced, and two of its three numbers can't be. Restate the actual
   commands with their actual totals when fixing finding 1.

## Tried to break it — and failed (verified clean)

- **TC-076 repoints are verbatim-true.** All three node names exist as
  `def test_...` in `tests/test_dual_plan_round.py` (lines 173, 259, 308) and
  in no other test file; commit `31ad569d` shows the same three defs moved
  from `test_agent_loop_dualplan.py` when the dispatcher died ("the seven
  native --dual-plan flag-path tests + fixture ... from
  test_agent_loop_dualplan"). Ran them:
  `3 passed, 4 deselected in 0.66s`.
- **TC-091's removal is honest.** The removed node's module
  (`tests/test_agent_loop_dispatch.py`) was deleted with the dispatcher whose
  e2e behavior it exercised; the four surviving `test_schedule.py` nodes
  cover the row's Expected — reason codes (`unclassified:missing`,
  `unclassified:unknown-value:bogus`,
  `unclassified:declared-ordinary-vs-structural-spine`,
  `unclassified:planmode-dual-vs-declared-*`) and disjoint-valid-rows-stay
  (`ready_ids(wis) == ["WI-003"]`). The Method's stray "checkpoint" is a
  RATIFIED-cell residue the spec explicitly leaves to WI-390 — pre-existing,
  correctly out of scope.
- **Fail-open hunt failed to find fail-open.** In a scratch copy: an invented
  TC Evidence (`tests/this_file_has_never_existed.py::test_entirely_invented`)
  and an invented LLR Module were both convicted by row id + column and
  gated (`strict-rc=1`, `warnfirst-rc=0` — the ruled warn-first shape). A
  `path-ok` marker exempts ONLY its own line (a dangling ref on the next
  line was convicted); the registry tier has no `path-ok` escape at all
  (planting the literal string inside the Evidence cell still convicted).
  The census claim reproduces exactly: new checker on the pristine trunk
  tree = `13 dangling reference(s)` (3×TC-076, 1×TC-091, LLR-096, LLR-132,
  4 spec-markdown, 3 `docs/test/report.md`); triage-commit tree = rc=0.
  The invented files were never created on the branch.
- **The LIFECYCLE declaration is honest narrowing, not a mothballed red.**
  Trunk's OWN checker on a pristine trunk tree (git archive, no gitignored
  files): `3 dangling reference(s)` — `README.md:154`, `README.md:187`,
  `docs/work/complete/WI-396-...md:3`, all naming `docs/test/report.md`,
  rc=1 — so the red pre-dates this branch and had been masked locally by a
  gitignored generated copy on disk. The file genuinely is trace.py's
  on-demand output (`.gitignore` line 12, "Generated reports"); the
  declaration classifies with its reason and stays visible in the untraced
  count rather than suppressing.
- **The log.md deviation is acceptable.** `git diff --word-diff` shows
  exactly two changes, both link TARGETS
  (`(specs/WI-394.md)` → `(archive/specs/WI-394.2026-08-01.md)`) with the
  link text untouched; the close commit records the deviation with its
  reason (the WI-288 relink convention applied by hand, its machinery dead
  since `31ad569d`).
- **Mechanical closes.** R-F: `specref = "docs/specs/WI-394.md"` present
  pre-close, absent in the complete spec's frontmatter; the spec-of-record
  archived to `docs/archive/specs/WI-394.2026-08-01.md` (git R091).
  R-A: Deliverable filled and — census, repoints, absence line, audit row —
  true to the diff (the verification totals are finding 2). The docs/work
  delta touches only WI-394's own files. `check_trajectory --root . --strict`
  rc=0 ("clean (400 work item(s), 372 done (93%), 17 cancelled, graph
  acyclic)"). `ruff format --check .`: "148 files already formatted";
  `ruff check` on the two changed Python files: "All checks passed!".
  `docs/enforcement-audit.md` gains the Harness row with the `::node`
  selector recorded as an accepted Prose gap — matching the ruling.

The build and triage are sound — I attacked the checker, the repoints, and
the lifecycle call and none of them broke. What failed at round 1 was the
close: the branch shipped red at the exact strict step it built, under a
pasted green. (Round 1 verdict as issued: CHANGES-REQUESTED findings=2.)

## Round 2 (2026-08-01) — the remedy, judged on its own

One rework commit, `3976bb5d`, touching exactly two files (the log fragment
and the complete spec's Deliverable) — docs-only, no code or registry rows,
so everything round 1 verified clean above stands untouched. Every corrected
claim re-measured by me at the rework HEAD:

1. **Finding 1 (MAJOR) — remedied.** The fragment's redirect quotation now
   names the AFTER-target as the docs-rooted live path
   `docs/archive/specs/WI-394.2026-08-01.md` (resolves — the archived spec
   exists) and quotes the BEFORE-target `docs/specs/WI-394.md` on a line
   carrying a reasoned `path-ok` marker ("the redirect's BEFORE-target,
   quoted as record — the spec moved at this very close, so the old path
   resolves nowhere by construction"). That is the shipped idiom with the
   reason it asks for, not a sanction: the BEFORE-target is dead by
   construction and quoting it IS the record. Re-run at the rework HEAD:

   ```
   check_doc_refs: OK - no dangling path or sym: references · 854 untraced (explained: declared absent, kit-relative, or a record surface) — --show-untraced to list.
   doc-refs-strict-rc=0
   ```
   The honesty half is also fixed: the Deliverable no longer pastes an
   undated green — it states rc=0 at the triage commit, **rc=1 at the close
   commit itself** ("2 dangling in the new log fragment's own redirect
   quotation — REVIEW-A finding 1"), rc=0 at the rework HEAD. All three legs
   match what I measured independently: triage tree rc=0 (round 1), close
   HEAD rc=1 with those exact 2 findings (round 1), rework HEAD rc=0 (now).

2. **Finding 2 (MINOR) — remedied.** Totals restated as dated measurements,
   and every at-rework-HEAD claim reproduces under my own runs:

   ```
   tests/test_check_doc_refs.py            27 passed in 0.87s
   tests/test_dupes_census_audit.py        12 passed in 0.48s
   both modules in one run                 39 passed in 1.33s
   smoke tier (-q -n auto -m smoke)        582 passed, 2 skipped in 9.08s
   check_trajectory --root . --strict      rc=0  "clean (400 work item(s), 372 done (93%), 17 cancelled, graph acyclic)"
   ```
   The combined 39 confirms the old number's origin exactly as the rework
   commit states (the two modules' one combined run); the full-suite figure
   (1802 passed / 10 skipped) is now explicitly dated to the pre-close tree,
   which a two-markdown-file rework does not invalidate.

Nothing new introduced: `git show 3976bb5d --stat` = the fragment + the
complete spec only; the census, registry rows, and checker code are
byte-identical to what round 1 attacked; and the strict step this WI armed
is green at the delivered HEAD. Both findings closed.

VERDICT: APPROVE findings=2
