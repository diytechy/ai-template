Reviewed: 9f35d60eaaaafffd440465bc6d94b836fd036a99

Verified: The checkout's HEAD is 9f35d60eaaaafffd440465bc6d94b836fd036a99. I read the whole reading-scope diff (code, prompts, PROCESS.md, rubrics, skills, registries, RESYNC entry) and the spec with its specref's "Owner rulings, 2026-10-11" section. I did not read docs/reviews, docs/decisions, plan critiques or commit messages. The failure classes I hunted first were these:
(a) fail-open: a SUCCESSOR clearing an F# exclusion without an accepted verdict for that same finding, or reaching the plan cap;
(b) silent wrong content: a convergence marking leaking into ordinary or loop briefs, or the convergence scope dropping work files;
(c) grammar drift: SUCCESSOR accepted with a malformed reason, or an unknown ruling accepted.

None of these holds:
- `kitlib/dispute.parse` refuses a reasonless SUCCESSOR, a lowercase `successor` and `SUCCESSORS`, and names FIX|SUCCESSOR|DISMISS|ESCALATE.
- `plan_coverage.resolution_findings` passes only `RESOLVING` (DISMISS, SUCCESSOR) on the rework path. `ruling_problem` keeps its DISMISS-only default for the filing step's `_ruled_findings`, and `plan_gate._dismissals` still compares against "DISMISS" alone. So SUCCESSOR never writes a plan-cap pass record, and an unaccepted, mismatched or other-round SUCCESSOR leaves the finding open.
- No other script consumes the ruling set (grep over the scripts for DISMISS/ESCALATE).

I drove the real CLI on this lane: `review_brief.py review --scope full --stance convergence` wrote one brief (exit 0). The `- STANCE: CONVERGENCE.` line sits directly after the FULL-LANE range line. Running the brief's own reading-scope command with `--name-only` lists no `docs/decisions` or `critique-*` path but keeps `docs/plans/WI-911/plan.md` and `pass.toml`.

Done-when map:
- Deliverables are in their targets, each citing its ruling. The skill no longer describes narrow rounds or a single reviewer (only "There are no narrow rounds" matches): covered by inspection and test_prompts' skill clause test.
- The skill copies in `.claude/skills/` and `.agents/skills/` are byte-identical to the kit source (`cmp`).
- critique names the registries: `test_the_scope_critique_names_the_registries_beside_the_spec`.
- The convergence line: `test_a_convergence_round_renders_the_one_fixed_stance_line`.
- An absent stance renders the ordinary round: `test_an_absent_stance_renders_the_ordinary_round`.
- Narrow plus convergence refuses: `test_a_narrow_round_refuses_the_convergence_stance`.
- SUCCESSOR parse, and other unknown rulings still refused: `test_a_successor_ruling_is_accepted_and_parsed`, `test_an_unknown_ruling_is_refused_naming_the_four_rulings`.
- The coverage gate excludes SUCCESSOR only with an accepted cite: `test_a_successor_ruling_citing_its_verdict_passes`, `test_a_successor_ruling_of_another_finding_refuses`, `test_a_cited_ruling_that_does_not_dismiss_refuses`.
- The trace rows were sat: acts 117/118 re-attest SR-233/234/236, LLR-069/311/313/314 and TC-069/332/333/334, and the live SR/LLR/TC registries equal `docs/archive/last_approved` byte for byte.
- RESYNC: one entry naming every shipped file, nothing forced. Its `[since e474f51dd]` sits before the current base, and recipes §3 re-anchors it at the landing's parent.
- Plan gate: WI-913 (b803dd019) is an ancestor of the base, and `docs/plans/WI-911/pass.toml` exists.
- The baseline manifest is committed at the trunk base.
- `trace.py --strict`: the only finding is LLR-292's.

Pre-fix red: I exported the base tree `c0dfd18` into my scratch, overlaid the HEAD test files, and ran all 15 tests this diff adds for its new behaviour against the pre-change code. All 15 FAILED there. Examples: "the ruling is not one of FIX|DISMISS|ESCALATE", "Round.__init__() got an unexpected keyword argument 'stance'", "AssertionError: ('docs/requirements/components.toml', [])", and the reading-scope git test.

Commands:
- `git rev-parse HEAD` -> 9f35d60eaaaafffd440465bc6d94b836fd036a99
- the brief's pytest command (15 files, `-n 2`, the literal basetemp, under lowprio.py) -> `525 passed, 18 warnings in 1757.70s (0:29:17)`, exit 0
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (922 work item(s), 802 done (87%), 30 cancelled, graph acyclic).` exit 0
- `python project-trajectory/scripts/trace.py --strict` -> exit 1 on one finding, `FINDING (requirement form): LLR LLR-292 Detail uses 'minimal'` (the Done-when's allowed exception). Final line: `SN=31 SR=131 LLR=303 TC=317 orphans=0 integrity=0 ... form-findings=1 ...`. It rewrote the gitignored `docs/test/report.md`; `git status` stays clean.
- the 15 new tests on the base tree with HEAD tests overlaid (basetemp `.../gate/C/pre-bt`) -> 15 failed, 0 passed
- `review_brief.py review ... --scope full --stance convergence --out <scratch>/probe-brief.md` -> exit 0. I ran its reading-scope command with `--name-only`: 0 decisions/critique paths, while plan.md and pass.toml are kept.

- [MINOR] docs/requirements/low-level-requirements.toml:3322 -> LLR-314's detail still says parse "accepts only one FIX, DISMISS, or ESCALATE ruling", and then its appended sentence says "SUCCESSOR is a fourth ruling". The row contradicts itself on the closed ruling set (K1, for clarity) -> at the next amendment through its authority, word the set once as FIX, SUCCESSOR, DISMISS or ESCALATE -> @owner
- [MINOR] docs/requirements/system-requirements.toml:1841 -> SR-236's rationale still reads "a disputed finding remains open unless its accepted dismissal decided that very finding". The amended requirement and acceptance now also resolve a finding on an accepted successor ruling (K1, for clarity) -> carry "or successor ruling" into the rationale sentence -> @owner
- [MINOR] docs/rubrics/kit-change-review.md:23 -> K2, "as review-churn ruling 5 refines it", bans an implementation carrier only in SN and SR cells. Ruling 5 and spine-questions.md §0 ban it in every requirement row, LLR included. So a reviewer applying K2 would pass a new LLR detail that names a function (K2, for clarity) -> say "No SN, SR or LLR row's text names an implementation carrier" and keep the boundary-artifact allowance for LLR/TC -> @owner
- [MINOR] project-trajectory/prompts/spine-questions.md:48 -> §0's new rule says "No row's text names an implementation carrier (a code file, function or symbol)". It does not say whether a TC's method may name test functions, and this lane's own TC-332 amendment (docs/test/test-cases.toml:3370) adds two test function names to the method cell. A sitting could return or pass such rows inconsistently (K2, for clarity) -> state whether test functions in TC method and evidence cells are outside the carrier ban until item 5 generates the evidence column -> @owner
- [MINOR] project-trajectory/scripts/review_brief.py:174 -> the convergence reading scope leaves out `docs/decisions` and plan critiques but keeps `docs/plans/<WI>/plan.md`. A revised plan answers the first plan critique by finding id (`docs/plans/WI-911/plan.md:12`: "The first critique's one finding, F1, is covered"), so a convergence reviewer still reads a summary of an earlier verdict. This is not fail-open, data loss or a Done-when gap: the Done-when names only the stance line -> decide whether the in-lane plan is reviewer input under ruling 4 ("never the builder's coverage plan"). If it is not, add it to `_CONVERGENCE_EXCLUDES`, the one declared set; this adds no new check -> @owner
- [MINOR] project-trajectory/skills/byte-budget-guard/SKILL.md:48 -> the PROCESS.md row re-stamps 97,946 against the prior 96,606 stamp but records the change as "+1,013 WI-911: §6 ...". The lane's delta is +1,340 (`wc -c` at c0dfd18 and HEAD), and the uncounted ~327 bytes are the §3 "Record a decision where it is made" bullet that deliverable 4 asked to be byte-checked (no rubric anchor) -> record +1,340 and name both the §3 and §6 additions -> @owner

VERDICT: APPROVE findings=6
