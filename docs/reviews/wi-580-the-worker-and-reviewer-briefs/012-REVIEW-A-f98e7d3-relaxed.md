# WI-580 — REVIEW-A round 012 (relaxed)

Scope: `git diff contract_split...HEAD` less records/generated artifacts. Rows under
review: WI-580 (spec of record `docs/archive/work/complete/WI-580-the-worker-and-reviewer-briefs.md`).

## Worst failure classes this change admits, hunted first

1. **Silent wrong content in a SENT brief** — `assignment_block` labelling a row the walk
   will return to as `built`, so a batch session skips live work. Driven, see below.
2. **Behaviour drift in the walk** — `current_assignment_wi` was rewritten onto the new
   `lane_completion`. Re-derived: `w not in (built - claimed)` ≡ `w not in built or w in
   claimed` — byte-for-byte the old predicate, no semantic move.
3. **Fail-open in the brief** — `claimed_on_branch` collapses `None` to `set()`, so a tree
   git cannot read makes `done == built`. Inherited unchanged from the pre-diff walk and
   unreachable for a checked-out lane branch (`git ls-tree` exits 0 on an absent prefix);
   not raised.
4. **Unfilled/leaked slots in a sent brief** — checked end-to-end, none.

## Instruments (run here, this tip, summaries only)

- `python project-trajectory/scripts/check.py --jobs 0` → `Check summary (stage
  DevStg-Tests, tier all)` — 11 PASS, 3 SKIP (`derived-stage`, `approval-fresh`,
  `verdict-rollup`, all "work branch … §5.2"), `RESULT: PASS`.
- `python project-trajectory/scripts/trace.py --strict-integrity` → `Traceability: SN=27
  SR=76 LLR=191 TC=190 orphans=0 integrity=0 verified-mechanized=72 … budget-findings=0
  component-findings=0 interface-findings=0 paraphrase-advisories=3`.
- Full unfiltered suite `python -m pytest -q -n auto` → `1 failed, 3436 passed, 21 skipped
  in 662.74s (0:11:02)`. The single red is
  `tests/test_derive_stage.py::test_this_repo_s_committed_stage_is_current` — a
  `docs/stage` FINGERPRINT mismatch. Verified it is the §5.2 lane-benign class and not a
  ladder move: the same test PASSES in a detached worktree at `contract_split`, and
  `derive_stage.py --print` on this tip reproduces the recorded rung, `drafted = 9`, and
  every `per-phase` value unchanged — only the content hash moved, because LLR-061's
  `detail` did. `check.py` SKIPs the step on a work branch by design and the trunk lane
  regenerates it. Not raised as a finding.
- `trace.py --approve modified` regenerated to a scratch path and diffed against the
  committed `docs/ratify/CURRENT.md`: **identical**, so the LLR-061 amendment reached the
  surface that approves it.
- `check_complexity.module_sloc(agent_loop.py)` → **2610**, exactly the ratchet baseline.

## Real shipped code paths driven (not probes)

Built an independent batch lane outside the repo (`git init -b wi-777-batch`, two specs in
`docs/work/active/wi-777-batch/`, one `WI: WI-777` trailer commit) and called the shipped
functions against it:

- `lane_completion` → `({'WI-777'}, set())` — trailer present, spec still active, so NOT
  done. `current_assignment_wi` → `WI-777`.
- `assignment_block` → `- The WHOLE assignment (2 rows claimed on this lane …)` with
  `WI-777 [this session's focus] Alpha row — SpecRef: docs/specs/a.md` and `WI-778 [not
  started] Beta row — SpecRef: —`.
- `worker_prompt` single-row → block absent; explicit one-element `assigned` renders the
  same bytes as the default.
- `reviewer_prompt(..., worker=<2-row lane>)` end-to-end → both rows named, and **no**
  `{wis}`/`{verdict}`/`{trunk}`/`{process_doc}`/`{scripts}` left unrendered.
- Scope-widening hazard checked and cleared: a round is scheduled only when
  `all(w in built_now for w in worker["assigned"])` (`agent_loop.py:2837`,
  `agent_loop.py:3611`), so naming every assigned row in the reviewer brief cannot ask a
  reviewer to map Done-when items for rows with no code in the diff.

## Regression tests driven RED on the pre-fix behaviour

Mutated `lane_completion` back to the trailer-alone predicate (`return built, built`):

```
FAILED tests/test_agent_loop_worker.py::test_the_brief_never_calls_an_unclosed_row_built
FAILED tests/test_agent_loop_worker.py::test_the_false_partial_class_turns_only_on_the_close_ritual
2 failed, 41 deselected
```

Both are real regression tests, not tautologies. Source restored; `git status` clean.

## Done-when → coverage

1. one-turn close bar — `test_worker_brief_names_the_one_turn_close_bar_scratch_and_amendments`; the
   rung claim independently confirmed by the check summary above (14 steps at
   DevStg-Tests, not one a test step). COVERED.
2. `{assignment_block}` + opening sentence —
   `test_worker_prompt_single_row_carries_no_assignment_block` +
   `test_worker_batch_prompt_names_every_assigned_row_and_its_state`. COVERED. (The
   "byte-identical to today's" clause is met as default-vs-explicit identity; literal
   identity against the pre-diff render is unachievable because items 1/4/5 change the
   same template — not raised.)
3. `{wis}` + override-without-slot — `test_reviewer_prompt_names_the_rows_under_review`,
   `test_reviewer_prompt_without_an_assignment_says_so`. COVERED.
4. amendment stales the approval brief — asserted on the rendered prompt. COVERED.
5. scratch home in one line — asserted on the rendered prompt. COVERED.
6. CATALOG regenerated — `prompt-catalog PASS`; both template hashes and the 12/5 slot
   lists match. Full suite: above. COVERED.
- WI-559 DW3 false-partial half — `test_the_false_partial_class_turns_only_on_the_close_ritual`,
  driven red. Its round-scheduling half is claimed by WI-579's own Deliverable
  (`docs/archive/work/complete/WI-579-…:52,61`), verified. COVERED.

## Findings

- [MINOR] project-trajectory/prompts/worker.template.md:48 -> the SENT brief body now cites this meta-repo's own records — `WI-540`'s sessions 005/006/007, `WI-538`, and the row id `LLR-206` — which an adopter can never read; confirmed they survive `prompts.load`'s `<!-- -->` strip (`worker_prompt` render contains `WI-540`/`WI-538`/`LLR-206` as True, while the pre-diff body at `contract_split` carried no concrete meta id at all), against CLAUDE.md "Templates must stay copy-ready": "a marker naming one of this repo's own rulings cites a record they can never read" -> move the WI-540/WI-538/LLR-206 forensics up into the stripped operator comment and leave the sent body the rule alone; this ADDS no check — removing the citation from the sent surface is itself the `antidote` skill's "smallest change that makes this fix unnecessary" -> @owner
- [MINOR] project-trajectory/prompts/worker.template.md:48 -> the brief RESTATES the commit bar ("the fast test tier plus its declared wall-time budget (docs/stack.ini), plus the docs staleness check") instead of pointing at its one home, and the restatement is wrong downstream in both directions: `project-trajectory/stack.ini.template` declares `[tiers]` but no wall-time budget section (`[smoke-budget]` and `check_smoke_budget.py` are meta-repo-only, not shipped), and it drops the pre-commit hook floor that PROCESS_OPTIONS "Phase cadence" names as the first of the bar's three parts -> replace the restatement with a pointer to PROCESS_OPTIONS "Phase cadence" / the `session-protocol` skill §3, or mark the budget clause conditional on the repo declaring one; deleting the second copy is the antidote (the same reasoning the row itself applies to the session-protocol clause), so no cross-file check is owed -> @owner
- [MINOR] project-trajectory/skills/session-protocol/SKILL.md:108 (and the byte-identical `.claude/` and `.agents/` copies) -> the diff deletes "before claiming a slice/phase done, at close" but leaves "Run the **full** unfiltered suite (`pytest -q -n auto`) after a broad script change" standing UNCONDITIONALLY, which still orders the run the shipped brief now forbids ("Run the full suite as well only if it demonstrably fits inside one turn; NEVER end a turn waiting on one") — and a broad script change is exactly the WI shape whose suite does not fit (measured here at 11:02 against a 10-minute foreground cap, the WI-540 stall this row exists to close) -> qualify the surviving trigger with the one-turn condition or fold it into the same single home the rest of the cadence went to; a prose deletion, no guard added -> @owner
- [MINOR] project-trajectory/skills/byte-budget-guard/SKILL.md:34 (and both fan-out copies) -> for clarity: "**`AGENTS.template.md` and this file are parked at their caps** (~1% free each)" is now false for this file — the same edit moved its baseline 4,847 -> 4,781 against the 5,000 cap (`wc -c` confirms 4781), i.e. 4.4% free, while the adjacent "~8%" -> "~6%" clause in the very same sentence WAS re-derived -> re-derive the "~1% free each" clause in the same edit, or split the parked claim so only `AGENTS.template.md` carries it -> @owner

VERDICT: APPROVE findings=4
