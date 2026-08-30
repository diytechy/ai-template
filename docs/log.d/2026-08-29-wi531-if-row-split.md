## 2026-08-29 — WI-531: the split — one row, one direction, one kind (OI-67 slice 4)

Deferred open items: none — the decisions this slice took alone are filed for
review in [../decisions-for-review-2026-08-29-slices-4-6.md](../decisions-for-review-2026-08-29-slices-4-6.md),
not as rulings owed.

**Summary.** The interface registry reads one row, one direction, one kind.
Twenty rows were minted (`IF-145`–`IF-164`) from the split worklist the
slice-3 workers' notes produced; two duplicate pairs collapsed (`IF-127` into
`IF-075`, `IF-116` into `IF-101`); three channels and nine far sides were
corrected from the code (counted as the ordinary corrections — the collapses
and the generated-document re-points aside); the three generated-document rows name their reader
class instead of the artifact. **136 rows became 154**, and the reference
reads **73 sources declare 150 seams; 150 carry a stated contract** (from
68 / 132 / 132 at slice 3's close — the four legacy rows are the difference).
Every `Contracts:` marker declares exactly the registry's rows for its file;
the owner-exact check warns on `IF-031` alone, as before.

**First act of the session — the smoke budget re-measured on a quiet box:**
`check_smoke_budget.py --mode enforce` read **23.3 s vs 60 s → within**
(1366 passed, 6 skipped in 22.90 s) at the HEAD slice 3 left, so the 99–118 s
readings the slice-3 close recorded were the busy box, as that close said.
<!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=673d9f3c -->

**How it ran.** Three Opus workers in parallel over disjoint owner-file
batches (the round is recorded whole at
[../reviews/2026-08-29-oi67-slice4/](../reviews/2026-08-29-oi67-slice4/README.md):
brief, worklist, batches, reports, fold and post-fold scripts). Each row
action was a `new` (an id assigned from the watermark, a body to write), an
`edit` (cells to confirm or MEASURE, a body to re-state) or a `delete` (a
collapse, its clauses merged into the surviving body). The workers read the
code before writing every body and measured every far side marked for it;
the fold applied the reports serially, minting each new row directly after
the row it split from, then the coordinator's post-fold edits applied the
findings the workers handed back outside their row sets (`scripts/trunk_step`
joined `IF-010`/`IF-012`/`IF-150` — its `--regen` invokes both generators and
gates on their exit codes; the adopter who runs the trunk step by hand joined
`IF-155`; `IF-001`'s `data` dropped the report medium that is `IF-146`'s).

**What was split, and what was not.** The exit-code halves the harness gates
on (`trace` `IF-145`, `check_perf` `IF-147`, `check_privacy` `IF-148`,
`gen_arch_map` `IF-150`); the argv arms a kit module or a launcher drives
(`subagent_gate`'s stdin `IF-151`, `plan_coverage` `IF-152`, `integrate`
`IF-154`, `trunk_step` `IF-155`, `run_menu` `IF-157`); the media a writer or
reader had no row for (`docs/test/report.md` `IF-146`, `docs/okf/` `IF-149`,
the coverage report `IF-153`, `docs/log.d/` `IF-156`, `docs/test/` `IF-161`,
`docs/agents-enabled` `IF-162`, `docs/status.md` `IF-163`, its generated block
`IF-164`); the write sides of `docs/work/` (`IF-159`) and `docs/reviews/`
(`IF-160`); `run_menu`'s exit code to the launchers (`IF-158`). Alphabets were
confirmed against `main()` and two corrected: `check_privacy --repo` cannot
return 2 (that alphabet is the pre-push arm's, `IF-043`), and `gen_arch_map`
returns 1 under `--strict-backlinks` too. **Not split, by decision:** the
harness's argv into each checker — `check.py`'s step table is the one
requestor of all of them, and a `cli` row per checker would restate the
generated CLI reference some twenty times — recorded as a class rather than
minted; `IF-040`'s two invocations share one exit-code contract;
`IF-056`/`082`/`083`/`084`/`138` and `IF-097`/`099`/`100` stay separate because
each requestor takes a distinct symbol subset (the collapse test the two
collapses passed and these fail).

**Measured, not asserted.** `docs/stage` has five direct readers, not one
(`IF-050`; `dispatch` and `agent_loop` reach it through `agent_common` and are
excluded); `docs/okf/` has a kit reader after all (`traj_parse._okf_nodes`, the
dashboard's Knowledge tab — `IF-149`); `schedule`'s requestors are `census`,
`dispatch` and `intake` with the symbols each takes, and `check_trajectory`
imports none (`IF-053`); `intake`'s callers are three, `agent_loop` included
(`IF-090`); `spine_carrier`'s six undeclared importers joined `IF-102` rather
than minting six carried rows; `docs/process.toml` has fifteen readers counting
the three hooks' pure-sh grep (`IF-037`), `docs/status.md` six (`IF-163`),
`docs/test/test-cases.toml` thirteen (`IF-161`). `IF-164`'s owner is
`scripts/traj_status` — the splice is its code; `gen_trajectory` only
dispatches — and it is the one new module-shaped owner the spine-link advisory
names (no design row names it and it declares no `Implements:` line).

**Citations re-pointed.** `TC-161`'s `verifies` names `IF-075` where it named
`IF-127` (its approved `method` prose still says `IF-127` — an approved cell,
left for the owner). The seam-TC allowlist: `IF-075` (now cited) and `IF-116`
(collapsed) pruned from the seed, **120 → 118**, the pinned set in
`tests/test_trajectory_arch.py` lowered in the same commit; twenty reasoned
entries added for the split rows (the parent's test state carries; each
closes when a TC cites the split kind) plus one **inherited** entry: `IF-144`
had no citing TC and no allow entry since it was minted at OI-64, so
`check_trajectory --strict` was already red on it — a reasoned entry, not a
laundering, recorded here. Four inherited R-F errors closed the same way:
`WI-528`/`529`/`530`/`532` were closed with their `specref` still set, and a
terminal row clears it; `WI-531` closes clean.

**Two small root-cause fixes the split forced.** `trunk_step.fragment_paths`
skips `README.md` by name, because `docs/log.d/` now owns a row and a
directory owner declares in its README — which the fragment grammar would
otherwise refuse (test added). `trace._IF_CONNECTIVE_RE` no longer reads
`--since` as the connective "since": a `cli` row's `Data` cell lists flags,
and a token opening with a hyphen is not a word (test added). And two stale
`docs/agents.csv` mentions in the enable-list's comment header now say
`docs/agents.toml`.

**Surfaced, not done — the next worklist.** `derive_stage --check`'s exit code
to the harness, `schedule.py`'s own CLI (`ready`/`simulate`), `integrate`'s
in-process call surface (`dispatch` and `handback` import it), and the
`docs/test/report.html` / `docs/test/perf-report.md` media carry no row.
`gen_arch_map.py` given both `--cli-doc` and `--contracts-doc` on one
invocation processes only the first (each `_*_doc_exit` calls `sys.exit`) —
the kit's own steps pass them separately, so nothing breaks, but the
invocation silently skips a target. `gen_okf._doc_title_and_summary` skips
only the first line of a leading HTML comment (slice 3's finding, now live for
`docs/status.md` too; slice 6 fixes it).

**Ratchets.** Three modules grew, docstring-only plus one two-line comment,
each re-stamped with the reason: `trace.py` +16 (5882 → 5898),
`gen_arch_map.py` +10 (2183 → 2193), `integrate.py` +7 (2605 → 2612).

**Deviations from spec:** the harness-argv class was not split (recorded
above, with the reason); the four legacy rows stay as slice 3 left them
(`IF-031` and the three `external:` rows are slice 6's); the inherited
`IF-144` and R-F reds were closed here rather than left, because the strict
bar is the claim bar and a red inherited is still a red.

**Byte deltas on budgeted files:** none touched.

**pytest totals:** full suite `python -m pytest -q -n auto`: 3078 passed, 15 skipped, 1 failed in 1863.03s (0:31:03) on a box at 62-76% CPU from other sessions' processes — the one failure was `test_traj_parse`'s pin of this repo's untied `external:` rows (three, now seven: the agent CLI's stdin arm and the three argv arms an external party drives, each stating its reason on the row), widened and re-run green with the frame, external-frame and component suites (43 passed); smoke tier: 1367 passed, 6 skipped (one in-process test joined the tier). **The smoke budget read OVER on this box at close — 132.5 s and 87.9 s against 60 s — and the reading is ENVIRONMENTAL, not this change's:** the same tier read 23.3 s at this session's first act on the quiet box (above), and both OVER readings were taken with 14 other-session `claude`/`codex`/python processes holding the box at 62-76% CPU. One machine, one data point; the budget is not moved, and the quiet re-measure is owed at the next quiet moment. `check_trajectory --strict`: 0 errors; `trace --strict`: interface-findings=0 (the three standing reds — SR-181's orphan pair and LLR-197's citation — predate the program); `check_docs --stale`: 0 broken; every freshness check current.
