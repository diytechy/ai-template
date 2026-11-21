# Queue drill hand-off (2026-11-21)

For the coordinator session that works the queue next, and for the operator.
Read this file first; it is the resume point. The longer history is
`docs/plans/2026-11-11-test-tiers/HANDOFF.md` §12.6, and nothing there needs
reading before starting.

**The job:** take each drillable work item through scope critique, build,
review and merge into `refactor_again`, running items in parallel worktrees
where they do not collide. Reviews: code by OpenAI Sol at low effort; prose
and documentation by Sol at low effort **and** Gemini Argon at low effort
(operator, 2026-11-21).

## 1. State at hand-off

- Trunk `refactor_again`, tree clean. It is ahead of the remote; pushing is
  the operator's (`push = "operator"`).
- Since the last unfiltered suite (2026-11-20 on `979e128c5`, one failure,
  fixed in `28ad912db`): acceptance acts 184 and 185, the assumption gate on
  (`[checks] assumption_gate = true`; its four steps report no finding), and
  work-item filings. `tests/test_rule_sync.py` and its neighbours passed after
  the gate flip (327 passed), but the whole suite has not run since. Run it
  once before wave A as the baseline (§7).
- The operator still owes, outside this drill: the OI-79 remote-ref delete
  and the push.

## 2. The queue

| Item | What | Wave | Notes |
|---|---|---|---|
| WI-1013 | A delegated run records only calls no spine row states, and none about conducting the run | A | Docs, the decisions template, the session instruction; RESYNC entry |
| WI-1014 | The README's registry map and the dashboard's lifecycle panel show today's tiers and ladder | A | `README.md`, `rendering/traj_panels.py`, dashboard golden files |
| WI-1017 | The guidance says an LLR yields to a sustainable design | A | Starts with an evidence check of recent lanes; then PROCESS.md §5, skills, prompts |
| WI-1015 | The code is held to its interface and LLR rows | B | Waits on the operator's variant-F call (§3); amends LLR-067 |
| WI-1016 | A repository can switch off the implementation layer | C | After WI-1015 (same checks); reverses SR-186, so its amendment is drafted for the operator |

Not drillable: WI-827 (the operator's signature on SN-029's amendment),
WI-998 (waits for a decomposition round to supply its sample), WI-1012 (waits
on HomeHub's adoption), and the five Blocked rows the open items hold
(`docs/status.md` "Blocked").

**Why the waves.** Wave A's three items touch different files (WI-1013 the
decisions doctrine and session instruction, WI-1014 the README and the
dashboard renderer, WI-1017 PROCESS.md §5, the spine-authoring skill and the
reviewer and critique prompts); their only shared file is likely
`project-trajectory/RESYNC_PACK.md`, which merges by keeping both entries.
WI-1015 and WI-1016 both rework `trace.py`, the architecture checks and the
interface registry, so they run one after the other.

## 3. Stop and ask the operator

- **Variant F, before WI-1015 builds.** The review-churn plan's pointer rules
  (`docs/plans/2026-10-11-review-churn/pointer-rules.md`; page
  https://claude.ai/artifact/VYzwf3J1WYcFJpvZCjRdt5) are ruled in full and
  not built: LLRs lose `module`, `code_symbol` and their component cell, an
  interface's owner becomes a component id, code files declare `Component:`.
  Several WI-1015 checks would hold cells F retires. Put the choice to the
  operator with WI-1015's critique in hand: (a) file the review-churn phase-3
  rows and build F first, then WI-1015 and WI-1016 on it; or (b) build
  WI-1015 narrowed to what F keeps, and WI-1016 on today's shape.
- **Any acceptance.** New rows are `Drafted`; an amended `Accepted` row keeps
  its status and shows as drift. Never flip a status to `Accepted`, never run
  `intake.py snapshot`. At the end, list what owes an act (`docs/open-items.html`
  §2) for the operator. An amendment's text is committed before its act
  (the `text-then-act` hook check).
- **A finding that would reverse an operator ruling.** Rulings are in each
  spec's Context ("operator, 2026-11-2x"), HANDOFF §12.2 of the test-tiers
  plan, and the review-churn plan.
- **Anything irreversible or outward:** a push, deleting a ref, a release.

## 4. One work item, start to finish

Run the commands from the repository root with
`.venv/Scripts/python.exe` (the system Python is 3.8; the kit needs 3.11).
`<scratch>` is the session's scratchpad.

1. **Scope critique, on trunk, before any build.** Render the brief:
   `review_brief.py critique --wi WI-NNNN --rubric docs/rubrics/scope-critique.md --scratch <scratch> --out <scratch>/crit-NNNN.txt`.
   A scope critique judges prose, so both reviewers read it (§6). Save both
   verdicts, as returned, in `docs/reviews/2026-11-2X-scope-critiques/WI-NNNN.md`
   (the pattern of `docs/reviews/2026-11-19-scope-critiques/`). Apply the
   findings to the spec on trunk: settle open choices, add `planmode`, split
   where the critique shows independent deliverables (a split mints its new
   WI id on trunk; `trace.py --bump-ids`). Commit with hooks. Once a wave's
   critiques are all in, update §2's waves and §8's id ranges for any split
   rows on trunk before launching a builder.
2. **Build, in a worktree.**
   `git worktree add D:/ai-template-wt-wiNNNN -b maint/wi-NNNN refactor_again`.
   Worktrees go on D:, never under `C:\Projects` (VS Code's file watcher
   storms on bulk writes there), and never while a suite runs. The builder is
   a fresh sub-agent given §5's rules, the spec path, its id ranges (§8) and
   the worktree path. With `planmode = "single"` it writes
   `docs/plans/WI-NNNN/plan.md` first.
3. **Close out on the branch, before the review,** so the review reads the
   closing prose too. The spec gets its `## Deliverable`, moves with
   `spec_move.py --root . docs/work/queued/WI-NNNN-<slug>.md docs/archive/work/complete/WI-NNNN-<slug>.md`,
   and the log fragment `docs/log.d/WI-NNNN-<slug>.md` opens with `## `.
4. **Review the branch** (the coordinator, never the builder). Render:
   `review_brief.py review --wi WI-NNNN --base <merge-base> --sha <tip> --scope full --scratch <scratch> --rubric docs/rubrics/kit-change-review.md --out <scratch>/rev-NNNN.txt`.
   Code changes (scripts, tests) go to Sol. Prose and documentation changes
   (docs, skills, prompts, templates, registry text, RESYNC entries) go to Sol
   and Argon. A branch with both: Sol reads the whole diff, Argon the prose
   part. Fix findings on the branch, then record the reviewers, findings and
   fixes in the Deliverable and the log fragment. That record needs no
   further review; any other change made after the review gets a narrow
   re-review (`--scope narrow --findings <round file>`) before the merge.
5. **Merge** (§7), one branch at a time, never while the suite runs.
6. **After each wave:** the unfiltered suite, fixes for anything red, a
   progress line in §10, and the merged worktrees removed
   (`git worktree remove D:/ai-template-wt-wiNNNN`, `git branch -d maint/wi-NNNN`).

## 5. Builder rules (paste into each builder's brief)

1. Work only in your worktree, on `maint/wi-NNNN`. Never touch trunk or
   another worktree. Never push. Commit with hooks on; never `--no-verify`.
2. Read your spec and its `specref`, `CLAUDE.md` and the `session-protocol`
   skill. Build test-first: a failing test, then the code.
3. Mint ids only from the ranges in your brief, then run `trace.py --bump-ids`
   on your branch so no live id sits above its mark. Never use `--reserve-ids`.
   Need an id outside your ranges: stop and ask.
4. New spine rows are `Drafted`. Amending an `Accepted` row changes its text
   only. Never flip a status to `Accepted`, never run `intake.py snapshot`.
5. Run every test module that imports a module you changed (grep the
   importers; `trace.py --tests-for <module>` lists the spine-linked ones),
   not just the tests you edited, plus the whole-tree tests your change can
   reach (`test_import_layers`, `test_module_size_ratchet`, `test_dogfood_sync`).
   Quote the real summary lines.
6. Before a commit that changes what a generated view reads, run
   `trunk_step.py --root . --regen` so the hook's freshness steps pass.
7. A work-item title stays under 120 characters; a spec filename stem under 38.
8. Write scripts and multi-line files with the Write tool; Bash heredocs
   mangle tabs and CRLF.
9. If `$PYTEST_DEBUG_TEMPROOT` is set in your shell, run pytest under
   `env -u PYTEST_DEBUG_TEMPROOT`.
10. Never read `OPERATOR_SCRATCHPAD.md`.
11. Record a design call in `docs/decisions/maint-wi-NNNN.toml`
    (`project-trajectory/decisions.template.toml`) only when no spine row
    states what you chose and it is not about conducting the run: a reading
    of scope, or a design choice no LLR or interface states (the operator's
    rule behind WI-1013). Most branches need few or none.
12. Stop and report, rather than guess, when a call is the operator's, when
    the spec leaves something unsettled, or when a red is outside your scope.
13. End with: your commits, the tests you ran and their summaries, and
    anything left.

## 6. Reviewers

- **Sol (code, and prose alongside Argon):** from `<scratch>`, not the repo:
  `codex exec -c model_reasoning_effort=low --model gpt-6.1-sol --skip-git-repo-check -o <scratch>/sol-NNNN.md - < <scratch>/rev-NNNN.txt`.
  Several Sol runs may go at once.
- **Argon (prose):** from `<scratch>`:
  `timeout 900 opencode run -m opencode-go/gemini-4-argon --variant low -- "$(cat <scratch>/part.txt)"`.
  Put the text inline, under 32 KB (split a longer diff into parts). Never
  attach with `-f`: it has stalled for 20 minutes. One opencode run at a
  time: two at once fail with "database is locked". **If Argon times out,
  skip it** (operator, 2026-11-21): it stalled twice on this hand-off's own
  review, inline, at 13 KB. Note in the review record that Sol reviewed
  alone; do not retry it in a loop.
- Tell each reviewer to answer from the brief and diff, and to cap its tool
  calls; a reviewer handed the whole repository reads for half an hour.

## 7. Merging and the suite

1. On trunk with a clean tree: `git merge --no-ff --no-commit maint/wi-NNNN`.
2. Conflicts: in a registry, rows with distinct new ids are all kept; an
   existing row both sides edited is reconciled cell by cell, keeping its
   status, and two edits that disagree in meaning go to the operator.
   `docs/id-watermark` takes theirs, then `trace.py --bump-ids`. A generated
   file (`PROJECT_STATE.html`, `docs/open-items.html`, `docs/status.md`'s
   generated block, `docs/stage`, `docs/ratify/CURRENT.md`,
   `docs/interface-reference.md`, `docs/cli-reference.md`,
   `docs/requirements/components.derived.toml`) takes trunk's.
3. Whether or not anything conflicted, run `trunk_step.py --root . --regen`,
   then commit with hooks: `Merge maint/wi-NNNN: <what it delivers> (WI-NNNN)`.
4. Then regenerate once more, since the views stamp the merge commit, and
   commit `regen: the generated views over the WI-NNNN merge` if anything
   moved. The same holds after any act commit.
5. A commit runs the hook's 29 steps and takes 2 to 3 minutes. One past 10
   minutes is stalled: look for a process waiting on input.
6. The unfiltered suite:
   `env -u PYTEST_DEBUG_TEMPROOT .venv/Scripts/python.exe -m pytest -q -n auto`,
   35 to 60 minutes, on a clean trunk. Run it in the background. Until it
   finishes, make no trunk commit, merge or regeneration and create no
   worktree; builders already in their D: worktrees keep working. Record the
   commit it ran on and its summary line in §10. Fix or triage every failure
   before the next wave starts; the baseline run's failures are fixed before
   wave A.

## 8. Ids for wave A

Marks at hand-off: SR 247, LLR 388, TC 448, IF 322, DA 28, SUR 4, CMP 9,
WI 1017. Each wave-A branch mints only from its own ranges:

| Branch | LLR | TC | IF |
|---|---|---|---|
| WI-1013 | 389–392 | 449–454 | 323–324 |
| WI-1014 | 393–395 | 455–459 | 325–326 |
| WI-1017 | 396–398 | 460–463 | 327–328 |

No SR, DA or SUR is expected in wave A; a builder that needs one stops and
asks. Waves B and C run alone, so each mints from trunk's marks at its start.

## 9. Gotchas

- `docs/status.md`'s hand-written prose must name no retired stage tag and no
  work-item id a later claim needs (`integrate._status_prose_refusal`); point
  at files instead.
- An accepted row's amendment lands in a commit before its act, never in the
  same one (`text-then-act`).
- After an act commit or a merge commit, regenerate before the next commit.
- `check_trajectory` warns, harmlessly, that a CMP-008 knowledge pack is never
  cited by a new spec; it warns hard on a title over 120 characters.
- A sub-agent's list of tests can miss whole-tree tests; check them yourself
  before merging.
- Claims through the kit's lanes refuse without a coordinator lease; this
  drill uses maintenance branches merged by hand, as the last three batches did.

## 10. Progress log

Append one line per step taken: the item, what happened, the commit.

- 2026-11-21: hand-off written; queue as in §2. Reviewed by Sol (low): five
  findings, all applied (regenerate on every merge, close out before the
  review, reconcile shared rows cell by cell, waves and ids for split rows,
  trunk frozen while the suite runs). Argon timed out twice and was skipped.
