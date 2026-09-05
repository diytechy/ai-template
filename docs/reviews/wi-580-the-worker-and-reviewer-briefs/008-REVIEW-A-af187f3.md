# REVIEW-A — WI-580 (the worker and reviewer briefs) @ c5ce8659

Scope: `git diff contract_split...HEAD` minus records/generated. Rows under
review: WI-580 (spec of record now at
`docs/archive/work/complete/WI-580-the-worker-and-reviewer-briefs.md`).

## Instruments (run here, this tip)

- `python project-trajectory/scripts/check.py --jobs 0` — `RESULT: PASS`
  (stage DevStg-Tests, tier all; 11 PASS / 3 SKIP — the three work-branch
  freshness stand-downs). `prompt-catalog PASS` is the CATALOG regeneration.
- `python project-trajectory/scripts/trace.py --strict-integrity` —
  `Traceability: SN=27 SR=76 LLR=191 TC=190 orphans=0 integrity=0
  verified-mechanized=72 verified-demonstrated=3 verified-attested=0 drafts=9
  budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=164
  interface-findings=0 paraphrase-advisories=3.`
- `pytest -q -n auto tests/test_agent_loop_worker.py
  tests/test_agent_loop_review.py tests/test_module_size_ratchet.py` —
  `79 passed in 33.27s`; `tests/test_prompts.py
  tests/test_routing_and_prompts.py tests/test_dogfood_sync.py
  tests/test_smoke_tier.py` — `99 passed, 1 skipped in 5.92s`.
- `check_complexity.module_sloc(agent_loop.py)` = **2610**, matching the
  ratchet baseline.

## Driven, not read

Built a real four-row batch lane (git repo, `active/<branch>/` specs, `WI:`
trailers) and called the shipped functions. `assignment_block` rendered
`WI-201 [built]` (trailer + spec moved out), `WI-204 [this session's focus]`,
`WI-207 [not started]`, and `WI-299 [not started] (row missing from the
registry)`; `lane_completion` returned `({'WI-201','WI-204'}, {'WI-201'})`;
`current_assignment_wi` walked to `WI-204`. Mutation check on the regression
test: re-ran the same fixture through the pre-fix trailer-alone predicate and
the unclosed row rendered `[built]`, so
`test_the_brief_never_calls_an_unclosed_row_built`'s `"[built]" not in block`
does fail on pre-fix behaviour. `current_assignment_wi`'s rewrite is
algebraically the old predicate (`w not in built or w in still_open` ≡
`w not in built - still_open`) — verified, not assumed. Checked and CLEARED the
suspicion that `{wis}` names unstarted rows to a reviewer:
`schedule_review_round` returns early unless every assigned row is built, so
the block can only name built rows.

Done-when coverage: 1 / 4 / 5 → `test_worker_brief_names_the_one_turn_close_bar_scratch_and_amendments`;
2 → `test_worker_prompt_single_row_carries_no_assignment_block` +
`test_worker_batch_prompt_names_every_assigned_row_and_its_state`; 3 →
`test_reviewer_prompt_names_the_rows_under_review` +
`test_reviewer_prompt_without_an_assignment_says_so`; 6 → CATALOG covered by
`prompt-catalog PASS`.

## Findings

- [MAJOR] project-trajectory/prompts/worker.template.md:48 -> the close-bar line excuses the worker from the full suite on the claim that "the lane's own refresh runs the full declared bar for you", but the refresh's bar is `check.py --tier all` (integrate.`_run_bar`) and `check.py`'s `format` / `lint` / `tests+coverage` steps are gated at `_kitladder.STAGE_IMPL` (check.py:719-727) while this repo's derived stage is `DevStg-Tests` (docs/stage) — my own `check.py --jobs 0` run at this tip reported 14 steps and NOT ONE of them a test step, so the `Bar-Green:` trailer attests a bar that executed zero tests and, between the smoke commit bar and phase close, nothing runs the suite the worker was just told it need not run -> either state the true condition in the brief (the refresh's bar includes the product test step only from the DevStg-Impl rung; below it the smoke tier at the commit bar is the whole test coverage) or ungate `tests+coverage` from the rung so the sentence becomes true; no guard is being added here, so no unrepresentability clause is owed — the structural fix, if taken, is check.py's step table being the ONE owner of "what the bar runs" so no brief has to describe it -> @owner
- [MAJOR] project-trajectory/skills/session-protocol/SKILL.md:109 (identically .claude/skills/… :109 and .agents/skills/… :109) -> the same commit that removed "before claiming a WI/slice done" from CLAUDE.md left the skill saying "Run the **full** unfiltered suite (`pytest -q -n auto`) before claiming a slice/phase done, at close, and after a broad script change" — and CLAUDE.md's amended bullet points AT THIS SKILL as the authority for "Commit bar vs gate bar", so the delegated home now contradicts the delegator and contradicts the shipped worker brief's "You do NOT owe the full unfiltered suite at close"; the skill even self-contradicts two lines later ("A per-WI slice inside a phase ends at the commit bar") -> delete the "before claiming a slice/phase done, at close" clause from all three copies, leaving PROCESS_OPTIONS.md "Phase cadence" as the single home of the cadence rule — that deletion is itself the antidote (one home, so the contradiction is unrepresentable rather than policed by a cross-file test) -> @owner
- [MINOR] docs/archive/work/complete/WI-580-the-worker-and-reviewer-briefs.md:92 -> the lane amended its own acceptance heading from "item 3 is shared" to "items 2 and 3 were discharged by WI-579; WI-580 absorbs item 1", narrowing this row's Done-when during the row's own build; WI-579's Done-when list never claims WI-559 item 3 (only item 2, at its line 465) — only its Deliverable prose does — and item 3's FIRST half, "tests drive the false-partial class (built-and-verified lane, long suite)", rides with item 1, which is WI-580's; grep finds no test of that class anywhere in `tests/` -> restore the shared wording and either cover the false-partial half or record it as knowingly uncovered against a named successor, rather than reclassifying it as discharged -> @owner
- [MINOR] project-trajectory/skills/byte-budget-guard/SKILL.md:37 -> for clarity: the prose "`CLAUDE.md` holds ~8%" was written against the 7,886-byte baseline (7.2% free) and the same edit moved the baseline to 7,975 (6.2% free), so a byte-accounting doc's one free-space figure is stale by its own change -> restate it as "~6%" (or drop the percentage and let the pinned Baseline column carry it, since `test_capped_doc_baselines_match_the_real_sizes` already pins that number and nothing pins the prose) -> @owner
- [MINOR] project-trajectory/prompts/worker.template.md:33 -> for clarity: the opening sentence still names the literal `scripts/agent_loop.py` while the very same commit routed the close-ritual commands through `{scripts}` precisely because that literal is wrong in this meta-repo, where the path is `project-trajectory/scripts/agent_loop.py` -> use `{scripts}/agent_loop.py` here too, so one composition boundary owns every runtime path the brief prints -> @owner

VERDICT: CHANGES-REQUESTED findings=5
