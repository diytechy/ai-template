Reviewed: 6e2ad9f7fd0f8d71ea94bfe83463b7b7cc966168

Verified. I checked the whole lane, e474f51dd..6e2ad9f7, against the WI-911 spec, its specref (review-churn README, owner rulings through revision 37), PROCESS.md, the registries it cites and `docs/rubrics/kit-change-review.md`. The failure classes I hunted first, worst first:
(a) Fail-open at the rework coverage gate: SUCCESSOR resolving an exclusion without an accepted, corresponding verdict.
(b) Fail-open at the plan cap: SUCCESSOR letting a pass record through.
(c) The dispute parser accepting an unknown or reasonless ruling.
(d) A convergence marking that is misplaced or silent: narrow plus convergence, or a wrong value.
(e) Silent loss of review coverage through the widened reading-scope pathspec.

(a) to (d) hold when driven through the real code.
- `ruling_problem` keeps DISMISS as its default. Only `resolution_findings` passes `RESOLVING`. The plan cap's two callers (`plan_gate.py:433` and `review_brief._ruled_findings` at `review_brief.py:905`) stay DISMISS-only. A pending SUCCESSOR, a SUCCESSOR of another finding, and another round's finding under the same id are each refused.
- `kitlib/dispute._one_ruling` gives SUCCESSOR the same reason rule as FIX. It still refuses `successor` and `SUCCESSORS`.
- `review_brief.py review` behaves as specified:
  - `--stance convergence` adds exactly one line, which I diffed against the ordinary render.
  - With no `--stance`, the brief renders byte-identical to an ordinary render.
  - `--scope narrow --stance convergence` exits 2 and writes no brief.
  - `--stance Convergence` is refused by argparse with exit 2.
- `critique` renders the five registry lines from the one `_REGISTRIES` table.
- The new pathspec really filters on this Windows git. `docs/decisions` and `docs/plans/*/critique-*` are gone from the diff, and `plan.md` stays in it.

Other checks that came out right:
- The three skill copies are byte-identical (`diff -r`).
- The byte-budget stamps match `wc -c` (4,434 and 96,933).
- IF-290's new requestors match real imports (`plan_gate._dispute` and `review_brief.kdispute`).
- TC-334's move to Full matches `test_dispute` in `SLOW_MODULES` at the base.
- The RESYNC entry is anchored at a trunk commit and lists every shipped file (K4).
- The baseline manifest exists at e474f51dd.
- `pass.toml` (b06c462f8) precedes the first build commit (59487bbcf).

Red-before: I exported e474f51dd with `git archive` into my scratch area, overlaid the lane's eight changed test files, and ran the new tests. 21 failed and 89 passed. The two new tests that pass on the old tree pin unchanged behaviour by design: the tag-count filing pin, and the planner-input structural move.

Done-when map:
- (1) Deliverables in their targets, skill free of narrow and single-reviewer text: covered by reading. A grep finds only "There are no narrow rounds".
- (2) Skill sync: covered by `diff -r`.
- (3) Critique registries: covered by test_the_scope_critique_names_the_registries_beside_the_spec.
- (3) Stance: covered by test_a_convergence_round_renders_the_one_fixed_stance_line, test_an_absent_stance_renders_the_ordinary_round and test_a_narrow_round_refuses_the_convergence_stance.
- (3) SUCCESSOR parse: covered by test_a_successor_ruling_is_accepted_and_parsed and test_an_unknown_ruling_is_refused_naming_the_four_rulings.
- (3) SUCCESSOR at the coverage gate: covered by test_a_successor_ruling_citing_its_verdict_passes, test_a_successor_ruling_of_another_finding_refuses, and test_a_cited_ruling_that_does_not_dismiss_refuses (its pending case).
- All of the tests named in (3) are red before the change.
- (3) Trace rows sat at the checkpoint: UNCOVERED, as expected. The checkpoint has not run, and the rows are Drafted.
- (4) RESYNC entry: covered, and test_resync_pack is green.
- (5) Plan gate before the build: covered by the commit order.
- (6) Baseline manifest on trunk: covered.
- (7) Bar on the landing tip:
  - smoke tier: UNCOVERED here, because these round facts forbid running it;
  - `check_trajectory --strict`: clean;
  - `trace.py --strict`: no finding beyond LLR-292's.

Interface counterparts:
- IF-288 (changed side: `review --stance`): retained, rightly. Its data cell names subcommands, not flags.
- IF-289 (changed side: the stance refusals): retained. Its "2 refused" already covers them.
- IF-290 (changed side: the SUCCESSOR ruling value): retained. Its data cell names the functions, not the ruling set; the requestors are corrected.

Side effect: `trace.py` regenerated the gitignored `docs/test/report.md` in the worktree. No tracked file changed (`git status` is clean).

Commands:
- `git rev-parse HEAD` -> 6e2ad9f7fd0f8d71ea94bfe83463b7b7cc966168
- the brief's pytest selection (15 files, `-n 2`, the literal `--basetemp`) -> `518 passed, 18 warnings in 316.78s (0:05:16)`
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (919 work item(s), 800 done (87%), 30 cancelled, graph acyclic).` (rc 0)
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=303 TC=317 orphans=0 integrity=0 ... form-findings=1 paraphrase-advisories=3.` (rc 0)
- `python project-trajectory/scripts/trace.py --strict` -> the only FINDING is `LLR LLR-292 Detail uses 'minimal'` (rc 1; the Done-when exempts LLR-292)
- the lane's new tests run against the e474f51dd tree, in my scratch -> `21 failed, 89 passed in 9.29s`
- `review_brief.py review` with `--stance convergence`, then without `--stance`, then `--scope narrow --stance convergence`, then `--stance Convergence` -> rc 0 / 0 / 2 / 2; `diff` shows exactly the one stance line
- `review_brief.py critique --wi WI-911 --rubric docs/rubrics/scope-critique.md` -> rc 0, the five registry lines rendered
- `git diff --stat e474f51dd...6e2ad9f7 -- <the new pathspec>` -> no decisions or critique file; `docs/plans/WI-911/plan.md` and `pass.toml` remain

Findings:

- [MAJOR] project-trajectory/prompts/reviewer.template.md:66 -> The exclusion of `docs/decisions` and `docs/plans/*/critique-*` is written into the one shared reading-scope pathspec, not into the convergence round that needed it. Every review now loses the delegated-decisions record, including ordinary rounds and the unattended loop's shipped reviewer in adopters' repositories. That contradicts the doctrine the kit ships: project-trajectory/PROCESS_OPTIONS.md:1298 says "a reviewer's dissent, may promote a call (silent to recorded, recorded to an exit)"; project-trajectory/decisions.template.toml describes `decided` as "one sentence a stranger can check against the diff". Scenario, reachable in normal use: a loop lane under `decision_recording = "record"` commits `docs/decisions/<branch>.toml` with a call the route table sends to the exits. The loop's reviewer brief now hides the record, so no reviewer can dissent on it. Neither the spec's deliverables nor its Done-when asks to narrow the ordinary reading scope. -> Keep the ordinary pathspec as it was at e474f51dd. Carry the two extra excludes only in the convergence round, for example by making review_brief.py's `_CONVERGENCE_ROUND` line state the full replacement reading-scope command. Then the convergence brief's own command still hides earlier findings by construction (review 003 F1's remedy kept), and ordinary and loop rounds keep the record. Add a test that an ordinary render's command still includes `docs/decisions`, and add a RESYNC line. (No guard is added: this narrows a scope back to its owner, the stance.) -> @owner
- [MINOR] project-trajectory/skills/coordinator-cycle/references/recipes.md:196 -> The closure-check recipe still runs `trace.py --strict-integrity`. SKILL.md:176 now says ruling 6 runs `trace.py --strict` "at the closure check and at the landing check" (deliverable 1). A coordinator following the recipe misses the form findings `--strict` reports. -> Change the closure check to `"$PY" "$SCRIPTS/trace.py" --strict`, keeping `--strict-integrity` where the recipes need integrity only. -> @owner
- [MINOR] docs/rubrics/kit-change-review.md:23 -> (K2) This round's rubric still says a file name "belongs in acceptance as current-carrier evidence". This lane rewrote that same sentence in scripts/coordinator/terra-spine-prompt.template.md:13 (deliverable 6) and in project-trajectory/prompts/spine-questions.md §3 under ruling 5: "SN and SR rows name no file in any cell, acceptance included". Every lane review rendered with `--rubric docs/rubrics/kit-change-review.md` gets the opposite rule from the one the spine author now gets, which is a sibling site of deliverable 6's correction. -> Rewrite K2 to ruling 5's voice: no implementation carrier in any SN or SR cell, acceptance included; current-carrier evidence lives in the verifying TC rows. -> @owner
- [MINOR] project-trajectory/skills/coordinator-cycle/references/recipes.md:634 -> The deleted "Reviews in the trial shape, by hand until WI-911 renders them" bullet also carried the plan critique's interim rule: append `critique-addendum.md` (severity by reachability) under a plan preface. The latest handoff's "How to run reviews now" still relies on it. WI-911 renders severity only into reviewer.template.md, and neither the critique template nor docs/rubrics/plan-decomposition.md states it. So after landing, the next lane's plan critique runs with no severity rule and nothing tells the coordinator to add one. -> Keep one recipe line in §1 "Single plan", step 3: append the severity-by-reachability rule to a plan critique brief until a row renders it. Or state the rule in docs/rubrics/plan-decomposition.md's verdict section, as scope-critique.md's now does for confirming rounds. -> @owner
- [MINOR] project-trajectory/prompts/reviewer.template.md:69 -> The convergence paragraph names only "docs/reviews/ or docs/decisions/" as the records to avoid. The lane's own commit subjects carry earlier findings to any reviewer who runs `git log`, which the brief invites: it asks the reviewer to confirm HEAD and to find each fix's pre-fix code. Examples: 36f18cbfc "full-lane review round 1, filed: one MAJOR (003, Opus)" and 6e2ad9f7f "... excludes every record of earlier findings (003 F1)". The recipes themselves have commit subjects cite round files. -> Add "or lane commit messages, which cite earlier rounds" to the stance's exclusion. Have the convergence reviewer locate pre-fix code from the diff (`git log -p` over test files, not subjects). Commit history is readable by construction, so an instruction (or a subject convention that names no finding) is the only lever; it cannot be made unrepresentable within this diff. -> @owner
- [MINOR] docs/requirements/system-requirements.toml:1840 -> (K1, for clarity) In SR-236 and in LLR-069's detail (docs/requirements/low-level-requirements.toml:672), the approved "resolves a finding only when an accepted dismissal ruled that same finding" is followed by an appended "An accepted SUCCESSOR ... also resolves", so the "only when" clause reads false. In SR-234's requirement and acceptance (system-requirements.toml:1810 and 1812), "the declared ruling set ... excludes fail-open, data-loss, and Done-when-gap findings" and "a convergence-class finding does not receive SUCCESSOR" read as a verdict-acceptance rule. No parser can enforce that, since the findings file carries no class. TC-332 pins only the template text. -> At the checkpoint, Terra rewords these cells: SR-236 and LLR-069: the resolving set is DISMISS or SUCCESSOR; SR-234: the SUCCESSOR bound is a direction to the sitting, not an acceptance check. (The approved bytes stay until the sitting rules the amendment.) -> @owner

VERDICT: CHANGES-REQUESTED findings=6
