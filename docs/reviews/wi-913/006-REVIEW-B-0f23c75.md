Reviewed: 0f23c755bd548ea23093af53cdf5539b8f420725

Verified. This is a full-lane review of WI-913 (`aac06695e...0f23c755b`, 36 files, excluding the brief's paths). I checked it against `docs/work/active/wi-913/WI-913-plan-gate.md`, its specref (review-churn README items 9 and 12, entry point 2 at README.md:825), PROCESS.md section 5 and section 6's threat model, and `docs/rubrics/kit-change-review.md`. `git rev-parse HEAD` printed the reviewed commit.

I hunted the worst failure classes first:
1. Fail-open: build output accepted in a `single` lane without a binding record, at the hook, at the squash path or at the slot.
2. Silent wrong binding: a pass record pairing current digests with a critique of other inputs.
3. A record written on a non-approving critique, or past the cap.

I read all of `plan_gate.py`, `kitlib/plan_pass.py`, the `review_brief.py` plan additions and the `check.py`, `integrate.py`, `plan_coverage.py` and `kitlib/git.py` changes. I also read the tests and the helpers they rely on (`agent_common.default_base`, `kitlib.done_when.claim_copy/spec_at/digest`, `text_then_act.lane_commit_walk`, `handback.close_partial`, `integrate.refresh`).

What I found right:
- One predicate, `commit_lines`, is asked at the hook, the squash walk and the slot (`_merge_refusal` now chains `plan_gate.landing_refusal`).
- `_own_changes` intersects across parents, so a merge is judged by what neither parent carried.
- A record committed together with build output is refused, because the build arm reads the parents' record.
- The planmode set is closed and read from the claim copy at the claim base. Non-string values hold by name.
- `render` round-trips through `parse`.
- A third critique is unrepresentable: `_CRITIQUE_RE` is capped and filing refuses past the cap.
- `beyond` and a missing delta are refused at render, at filing and at pass.
- The cap requires an accepted DISMISS of every BLOCKER and MAJOR finding, numbered by position among all findings.

I drove the real code on fixture lanes (a probe under this scratch directory, which imports the worktree's `plan_gate`, `review_brief` and `spec_move`):
- (a) A critique approved the plan, then a Done-when item was reworded and committed. `review_brief.write_pass` refused: "the critique reviewed other plan bytes or another Done-when than the record binds".
- (b) A `single` lane closed partial through `spec_move.move_spec` plus its report, and that close passed. A refresh-style merge of trunk carrying a regenerated `PROJECT_STATE.html` and a compiled `docs/log.md` was then held at the hook ("build output (PROJECT_STATE.html, docs/log.md) before a pass record binds its plan") and refused by `landing_refusal` (finding 1).
- (c) `git commit --amend` of the pass-record commit adding `src/app.py` passed the hook, which is the hook's usual blind spot. `landing_refusal` caught it ("build output (src/app.py) before a pass record binds its plan"), so the landing backstop holds.

Spine sweep:
- LLR-337's detail matches the code.
- IF-295 matches `plan_gate.main`.
- The SR-154, LLR-313 and TC-333 amendments are the ones the spec grants.
- The LLR-302 and LLR-069 module and code_symbol edits are the back-links K3 needs for `squash_commits` and `_tree_text`/`_tree_tomls`.
- Each new function's `Implements:` tag names an LLR whose module and code_symbol carry it.
- The RESYNC entry is anchored `[since aac06695e]` (K4).
- The skill copies are byte-identical across `project-trajectory/`, `.claude/` and `.agents/`, and so are `WI-000.template.md` and its example copy (cmp).

Done-when map:
- Gate arms, `tests/test_plan_gate.py`:
  - hook, landing and slot: 140, 156, 178
  - plan and Done-when edits, and a tick: 233, 255
  - absent, unreadable, malformed and other-row or other-digest records: 269, 293
  - pass-record commit against its parent: 313, 337, 355
  - homes and a close: 390, 396
  - rebase and merge: 414, 425
  - planmode edit and another lane's claim copy: 441, 450
  - the closed set: 199, 470
  - trunk and a lane with no `single` row: 483
- Strict render: `test_plan_pass.py` 177/188/200 and `test_plan_filing.py` 306.
- Filing refusals: `test_plan_filing.py` 63, 81, 98, 109, 118, 127, 203, 225, 248. The "another Done-when digest" arm is UNCOVERED by a test, though the code implements it (finding 2).
- Template, catalogue, delta words and no skill: `test_plan_pass.py` 149, 164, 207, 215. The words match README.md:825 exactly.
- Skill and template sync: `test_dogfood_sync.py`.
- RESYNC: present. It forces no migration and says that an out-of-set planmode is now held.
- Bar: `check_trajectory --strict` is clean, and `trace.py` has no finding beyond LLR-292's. I did not run the smoke tier, per the brief.

Red-before: every gate test drives a module that does not exist at `aac06695e`.

Commands (worktree C:/Projects/ai-template.wt/wi-913, GIT_CEILING_DIRECTORIES set as the brief states):
- `git rev-parse HEAD` -> 0f23c755bd548ea23093af53cdf5539b8f420725
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-14-coord/wi-913/r2/C/wi-913 tests/test_plan_gate.py tests/test_plan_filing.py tests/test_plan_pass.py tests/test_plan_coverage.py tests/test_plan_coverage_step.py tests/test_review_brief.py tests/test_review_brief_git.py tests/test_text_then_act.py tests/test_prompts.py tests/test_dogfood_sync.py tests/test_integrate.py` -> 329 passed, 1 skipped in 191.45s
- `python project-trajectory/scripts/check_trajectory.py --strict` -> check_trajectory: clean (913 work item(s), 798 done (87%), 30 cancelled, graph acyclic). exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity` -> Traceability: SN=31 SR=131 LLR=303 TC=317 orphans=0 integrity=0 ... form-findings=1 (LLR-292 'minimal', pre-existing and allowed by the Done-when). exit 0
- `python probe/probe.py <dir> dw|refresh|amend` (scratch probes, outputs quoted above)

- [MINOR] project-trajectory/scripts/plan_gate.py:86 -> [B1] The closed pre-record path set misses two lane writers the kit itself prescribes, so a `single` lane that never passes cannot land through the slot. The first is the section A2 station refresh. Its `--no-ff` merge of trunk carries `trunk_step.py`'s regenerated views and the compiled `docs/log.md`, which differ from both parents. The second is a `docs/log.d/<WI>-<slug>.md` fragment, PROCESS.md section 5's home for a work branch's evidence. The scenario is reachable through the gate's own exits: a `DELTA: beyond` plan, a FIX or ESCALATE at the cap, or a finding-less second change request each "closes the lane partial". `close_partial` then says "the branch then merges like any other", but the refresh commit is "refused by its own floor" (the hook's plan-gate step) and `landing_refusal` refuses the slot. The probe reproduced both. The hold tells the operator to "plan first", which is the wrong remedy for a closed lane. It fails closed by name, so it is a coverage-extension note. -> Admit the refresh merge's declared `[generated]` paths and the compiled `log.md`, plus `docs/log.d/` fragments, as record homes, or exempt a lane whose claimed rows have all left `active/<branch>/` through a close. Add a fixture test that refreshes a partial-closed `single` lane. Extending an allow-set adds no guard, so no unrepresentable clause is owed. -> @owner
- [MINOR] tests/test_plan_gate.py:355 -> [B1] The Done-when names two arms: a pass form or pass-record commit whose cited critique reviewed "other plan bytes or another Done-when digest than HEAD's", and "A test covers each". Only the plan-bytes arm is tested. A critique approving the plan under one Done-when, followed by a reworded Done-when and a pass form, is refused by `_reviewed_problems` (probe (a)), but no test pins it. A regression that compared only the plan bytes would pass the suite. -> Add the Done-when-digest case at the pass form (`write_pass` refuses) and at the hook (a forged record with the current digests, whose `reviewed` commit holds the old Done-when). Add it to TC-367's evidence. This is a test, not a guard, so no unrepresentable clause is owed. -> @owner
- [MINOR] project-trajectory/skills/coordinator-cycle/SKILL.md:105 -> [K1] Step 5 tells the coordinator to write an adopted recommendation that changes what the row promises "into its Done-when ... in the lane", after the pass record. Such an edit (not a tick) moves the Done-when digest, so the record no longer binds. Before the pass, `_reviewed_problems` refuses for the same reason (probe (a)). Either way it costs a fresh critique, and after the second critique none is filable (`_critique_round_to_open`, `_CRITIQUE_RE`). The scenario is reachable in normal use: a second critique approves with a MINOR that sharpens a Done-when item, the coordinator adopts it as step 5 says, and the lane is stuck until the owner acts. Recipes 'An edited plan or Done-when unbinds the record' says it in general, but step 5 sends the coordinator straight into it. -> In step 5, say that a Done-when adoption must precede the critique round meant to pass, so it consumes that round. At the second critique, the adoption goes to the Trust section or to the owner. This is skill text, so no unrepresentable clause is owed. -> @owner
- [MINOR] docs/requirements/interfaces.toml:2606 -> [K1; for clarity] IF-288's `data` lists `plan-file (--critique --sha | --pass [--dispute])` but omits the third mode, `plan-file --dispute-findings PATH --positions FILE`. IF-289's `data` (line 2617) likewise names "review, critique or pass record filed" without the dispute findings file. Both modes are in Contract IF-288/IF-289 at project-trajectory/scripts/review_brief.py:85 and :98. -> Add the `--dispute-findings --positions` mode to IF-288's data, and "dispute findings file" to IF-289's 0-arm, matching the docstring contract. -> @owner
- [MINOR] docs/requirements/system-requirements.toml:713 -> [K1; for clarity] SR-154's appended acceptance requires that the plan "declares an in-scope architectural delta". Read literally, that demands a delta, while the code passes `DELTA: none` as well as `within` (`plan_pass.PASSING_DELTAS`) and the spec's Q8 lists `none` as an answer. -> Reword to "declares an architectural delta of none, or one carried within its scope". -> @owner

VERDICT: APPROVE findings=5
