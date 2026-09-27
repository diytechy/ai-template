+++
id = "WI-602"
title = "spot-check the clean close of WI-580 - does the shipped work match what the row asked for? (cancel / defer / draft a successor / surface an open item)"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
+++

## Deliverable

THE SHIPPED WORK MATCHES THE ROW. Every one of WI-580's six Done-when items,
and the three absorbed items it quotes, is answered by code, template text or
a test at this tip. The close stands; one residual is drafted as a successor
below, and it is the residual WI-580's own final review round named and
accepted at APPROVE (round 012, four MINORs), not something new.

RE-DRIVEN, NOT READ. WI-580's commits (`1d8756c3` .. `f98e7d3f`, merged at
`dc36375f`) were diffed against the tip, the two test modules they extend were
run whole, and three mutations were applied to `agent_loop.py` and reverted
(`git status` clean at the end). Baseline `tests/test_agent_loop_worker.py` +
`tests/test_agent_loop_review.py`: **79 passed in 1698.08s** (a loaded shared
box; the modules are in `conftest.SLOW_MODULES`, so this is not the smoke
tier). Mutations, each on a targeted node list:

- `assignment_block`'s state map reduced to the trailer-alone predicate
  (`dict.fromkeys(built, "built")`): `test_the_brief_never_calls_an_unclosed_row_built`
  **red** on the exact line its MUTATION NOTE predicts (`[built]` where
  `[started, not closed]` is owed); the single-row control test stayed green.
- `reviewed_rows_block`'s no-assignment arm returning `""`:
  `test_reviewer_prompt_without_an_assignment_says_so` **red** (the fallback
  sentence absent from a rendered brief). Run result: `2 failed, 1 passed`.
- the one-row gate `len(assigned) < 2` widened to `< 1`:
  `test_worker_prompt_single_row_carries_no_assignment_block` **red** (a
  one-row lane rendered a "WHOLE assignment (1 rows...)" block);
  `test_worker_brief_names_the_one_turn_close_bar_scratch_and_amendments`
  green beside it. Run result: `1 failed, 1 passed`.

ITEM BY ITEM.

1. WI-559 item 1, the one-turn close bar. `worker.template.md` carries the
   "THE CLOSE BAR IS THE COMMIT BAR, and it must fit in ONE turn" bullet, names
   the refresh's `Bar-Green:` trailer, points at `check.py`'s step table as the
   owner of what the bar runs, and names `DevStg-Impl` as where the product
   test step arrives; asserted on the RENDERED prompt by
   `test_worker_brief_names_the_one_turn_close_bar_scratch_and_amendments`
   (green in the baseline). The merge slot's own record corroborates the
   rework's claim: `dc36375f`'s body reads "bar PASS (14 steps, tier all)",
   the fourteen-step, no-product-test bar the Deliverable says `DevStg-Tests`
   selects. Matches.
2. `worker_prompt` takes the whole assignment. `assignment_block(root,
   wi_rows, wi, base, assigned)` renders id + `[state]` + title + SpecRef per
   row and `""` for one row; `worker_prompt` gained `assigned=None` defaulting
   to `[wi]`. Driven end to end through the loop by
   `test_worker_batch_prompt_names_every_assigned_row_and_its_state` (session
   001 sees focus / not started, session 002 sees the first row `built`), and
   the one-row identity by the single-row test (explicit `assigned=[wi]` ==
   default, block empty, "assigned ONE work item" gone). One literal-vs-
   substance note, not a finding: the row says "byte-identical to today's
   except for that sentence", and the render also differs by the close-bar,
   scratch and amendment bullets and the `{scripts}` slot, which are items 1,
   4, 5 and a review rework of this same row. The test pins what the predicate
   meant (the mechanism adds nothing to a one-row lane), and the mutation
   above shows it is live. Matches.
3. `reviewer_prompt` gains `{wis}`. `reviewed_rows_block(worker)` renders
   `  - <id> - <title>` per assigned row, a declared fallback sentence with no
   worker; `reviewer.template.md` places it after "The work item(s) under
   review are:" and states the reading scope "stays the diff itself";
   `CATALOG.md` lists `{wis}` among the REVIEWER slots.
   `test_reviewer_prompt_names_the_rows_under_review` drives it through the
   loop (`WI-201 - Scoped work for WI-201` in the sent brief, three-dot range
   untouched) and the fallback test covers the no-worker and override-without-
   slot cases (`str.replace` no-op, rendered bytes equal). Matches.
4. WI-560 item 2, the amendment clause. The close-ritual bullet reads "if this
   WI minted spine rows OR AMENDED THE TEXT OF AN ALREADY-APPROVED CELL ...
   regenerate the approval brief"; asserted on the rendered prompt by the same
   brief test as item 1. Matches.
5. WI-562 item 2, the scratch home. One bullet, "Scratch belongs OUTSIDE the
   worktree - your own session temp directory. Never `out/` ..."; asserted by
   the same test. Matches.
6. Tests and regeneration. The two-id test and the reviewer-rows test exist
   and pass (above). `gen_prompt_catalog.py --check` at the tip:
   `gen_prompt_catalog: fresh (8 prompts).`, exit 0, and the WORKER row lists
   all twelve slots the template's header now counts (`{assignment_block}`
   and `{scripts}` included). "Full suite green": the close-tip log records
   `3429 passed, 25 skipped, 1 failed in 976.8 s`, the one red being
   `test_derive_stage.py::test_this_repo_s_committed_stage_is_current` on the
   LLR-061 fingerprint, with every derived value byte-identical and
   `docs/stage` a trunk-regenerated artifact a lane may not hand-set. That
   reading is correct and the merge regenerated it; the literal "green" was
   the tree after the merge, not the branch, which the log says plainly.
   Matches, with the caveat stated where it was stated.

The absorbed shared halves. WI-559 item 3's false-partial half is
`test_the_false_partial_class_turns_only_on_the_close_ritual` (green in the
baseline; it drives `lane_completion` and `integrate.finished_branches` on one
scaffold and flips both with the spec move alone); its round-scheduling half
is WI-579's, archived in `docs/archive/work/complete/`. WI-560 item 4's "tests
drive all three" is met for this row's third by the rendered-prompt assertion.
`LLR-061.code_symbol` reads `build_worker_assignment/worker_prompt/assignment_block`
and its `detail` names the two-part predicate, `status = "Approved"`
untouched. The `session-protocol` clause "before claiming a slice/phase done,
at close" is gone from all three copies (`.claude/`, `.agents/`,
`project-trajectory/skills/`; line 109 in each now opens "after a broad script
change").

THE ONE RESIDUAL. Round 012 approved with four MINORs, and three of them
describe kit-shipped prose that is still exactly as the round found it: the
SENT worker brief cites this meta-repo's own records (`prompts.load("WORKER")`
at the tip carries `WI-540`, `WI-538`, `LLR-206` outside the stripped
comment; the REVIEWER body carries none), restates the commit bar as "the fast
test tier plus its declared wall-time budget (docs/stack.ini)" where
`stack.ini.template` ships `[tiers]` and no `[smoke-budget]` section, and the
skill still orders the full suite "after a broad script change"
unconditionally. `CLAUDE.md` makes the copy-ready rule explicit ("a marker
naming one of this repo's own rulings cites a record they can never read"),
and no open item or queued row tracks the three. Drafted as one successor
below: it is one reviewed diff of two kit-owned prose files, the same reason
WI-580 itself was one row.

No source file changed by this WI. Harness: the two test modules above and the
targeted mutation runs; `check_trajectory.py --strict` clean at the close
commit.

## Context

This close was GREEN: the merge slot ran the declared bar on the composed tree and the review rounds judged the work. Nothing is alleged. It is here because `docs/process.toml [attestation] complete_review` is 'sample', and a process that only ever looks at its failures learns nothing about its successes.

Read `docs/archive/work/complete/WI-580-the-worker-and-reviewer-briefs.md` and ask ONE question: does what shipped answer what the row asked for? A finding is a successor row, never a reversal — the close stands.

## Done-when

- The row's `## Deliverable` answers its one question, whether what WI-580
  shipped answers what WI-580's row asked for, item by item, each answer citing
  the code, test or document it was checked against.
- Each finding is drafted as a successor in this spec's `## Dispositions`
  section, with an `open_item` cell where the answer is the owner's; none
  reverses the close.
- With no finding, the Deliverable says the close stands and on what evidence.

## Dispositions

```toml
title = "make the shipped worker brief adopter-true: cite no meta-repo record in the sent body, point the close bar at its one home, and settle the skill's residual full-suite order"
workstream = "process"
buildtier = "small"
specref = "project-trajectory/prompts/worker.template.md"
```

WI-580's final review round (REVIEW-A 012, APPROVE with four MINORs) named
three defects in kit-shipped prose and the row closed with them standing; WI-602
re-verified all three at the tip. (1) The SENT body of `worker.template.md`
(what survives `prompts.load`'s comment strip) cites `WI-540`'s sessions
005/006/007, `WI-538` and `LLR-206` - records of THIS repo that an adopter
copying the kit can never read, against `CLAUDE.md`'s "Templates must stay
copy-ready" rule. (2) The same bullet RESTATES the commit bar ("the fast test
tier plus its declared wall-time budget (docs/stack.ini), plus the docs
staleness check") instead of pointing at its home, and the restatement is false
downstream: `project-trajectory/stack.ini.template` declares `[tiers]` and no
`[smoke-budget]` section, so a scaffold's worker is told to run a budget its
repo does not declare. (3) `project-trajectory/skills/session-protocol/SKILL.md`
line 109 (and the byte-identical `.claude/` and `.agents/` copies) still orders
"Run the **full** unfiltered suite ... after a broad script change"
unconditionally - the one clause WI-580's deletion left, and it contradicts the
brief's "Run the full suite as well only if it demonstrably fits inside one
turn; NEVER end a turn waiting on one".

IN SCOPE - move the measured evidence (the WI-540 stall, the WI-538 stale
brief) into the template's `<!-- -->` header, where the kit already keeps its
own history, leaving the sent body with the rule and its reason in adopter-
neutral words; replace the bar restatement with a pointer to the step table
and `docs/stack.ini`'s `[tiers]` (the two homes that exist in every scaffold);
qualify or delete the skill's "after a broad script change" order so it agrees
with the brief, in all three copies (`tests/test_dogfood_sync.py` polices the
fan-out). Regenerate `prompts/CATALOG.md`; the rendered-prompt assertions in
`tests/test_agent_loop_worker.py` must keep passing or be re-aimed at the new
wording in the same diff.

NOT IN SCOPE - the close-bar doctrine itself (settled by the owner 2026-09-05,
`docs/handoff-2026-09-04.md`), the rung gating of `tests+coverage` in
`check.py`, and the fourth MINOR (the byte-budget-guard "parked at their caps"
sentence), which is this repo's own skill and a one-line fix for whoever next
edits it.
