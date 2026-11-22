+++
id = "WI-1044"
title = "The author's prompt template and TC-385 name roles, not models; recipes §5's carriage-return escapes restored"
workstream = "docs"
sr_refs = []
needs = []
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 4
planmode = "none"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1044`, cut from `refactor_again` at
`1b22c9355`, with the commit hooks on. The specref (WI-1037's archived spec)
is cleared at close, as a terminal row's is.

- `f9aa0914f`: the template, the pins, TC-385's two cells, recipes §5's
  escapes in the source and its two refreshed copies, and the regenerated
  views.
- The close-out commit after it: this Deliverable, the move to `complete/`
  and the log fragment.

**The template.** `scripts/coordinator/terra-spine-prompt.template.md` names
the roles: "You are the SPINE AUTHOR for one work item", "At a checkpoint
turn, the builder has built the code, tests and docs in this lane", "An
independent adjudicator will judge your rows later". It read "GPT Terra,
gpt-5.6-terra", "a Claude Opus builder" and "An independent Claude Opus
adjudicator". It holds no observation tied to one model, so none needed a
label. Its file name stays (the spec), as does its `--basetemp` path
`@LANE_SLUG@-terra`, a launch path recipes §5 also names ("the lane's
`<lane>-terra` basetemp").

**The pins.** `tests/test_prompts.py::test_the_terra_brief_has_an_intent_form_before_build_round_1`
asserts "At a checkpoint turn, the builder has built the code, tests and
docs in this lane". WI-1037's role pin,
`test_the_cycle_names_each_role_never_the_model_that_fills_it`, now reads
the template beside the skill's three copies and the coordinator tools'
README: a model name only directly after "observed with", and no model id.
That extension is the pin that makes the first Done-when item hold
(accepted by the coordinator). Both ride the module's file-level tag; no
row is minted. Red on the prior template (the role pin found 7 sites),
green after.

**TC-385** (Accepted; text only). Its method now ends "retirement of direct
author, critic and REVIEW-A launch recipes" (was "direct Sol and Terra
launch recipes"), and its expected reads "names the coordinator-call route
as the only launch path for author, critic and REVIEW-A calls" (was "the
only Sol or Terra launch path"). The roles are the skill's own phrase
("Every author, critic and REVIEW-A call runs through
`scripts/coordinator/codex_call.py`"), the set those two routes serve
today. Its status, its evidence and its tests' names are unchanged.

**Recipes §5.** The CR-count bullet's three escapes read `\r` again: count
`\r`, `count(b"\r")` and `grep -c $'\r'`. `b0e16fe0f` wrote a raw CR byte
there, since normalized to a newline. Edited in the source; the
`.claude/skills/` and `.agents/skills/` copies were refreshed with
`bootstrap.py --dest . --sync`. The bytes were checked: the three copies are
sha256-equal, hold no CR byte, each escape is the two characters backslash
and `r`, and no newline is left between backticks.
`gen_skills_index.py --check-agents`: "OK - 22 per-agent skill copy(ies)
match source"; `--skills project-trajectory/skills --check`: "OK - 33
skill(s), index fresh".

**Tests.**

- Red first, on the prior template with the test edits only:
  `2 failed, 93 deselected in 1.14s`; green after:
  `2 passed, 93 deselected in 0.63s`.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider tests/test_prompts.py -k 'names_each_role or intent_form_before_build_round_1'" rev="1b22c9355 with the test edits only, then f9aa0914f (its tree before the commit)" -->
- The modules reading the template, the skill, its copies or the live
  test-case registry, and the whole-tree tests: `test_prompts`,
  `test_overnight_legs`, `test_skills_sync`, `test_skills_index`,
  `test_skill_materialization`, `test_bootstrap`, `test_dogfood_sync`,
  `test_generated_freshness_wiring`, `test_module_size_ratchet`,
  `test_pre_commit_hook`, `test_adoption_record`,
  `test_disposition_adoption`, `test_import_layers`,
  `test_decision_record`, `test_adjudicate_brief`, `test_spine_rules`,
  `test_cell_classes`, `test_rule_sync`, `test_evidence_join`,
  `test_baseline_snapshot`, `test_check_test_first`, `test_trace`,
  `test_spine_carrier`: `1011 passed, 2 skipped, 18 warnings in 572.87s (0:09:32)`.
  `trace.py --tests-for` links no spine module to the template or the skill.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider -n auto <the 23 modules listed>" rev="f9aa0914f (its tree before the commit)" -->
- The commit checks, `run_menu.py smoke`:
  `1 failed, 3713 passed, 3 skipped, 18 warnings in 338.56s (0:05:38)`.
  The one failure is trunk's, not this branch's:
  `test_stage_ladder.py::test_this_repo_is_clean_at_the_ERROR_severity`,
  `check_vocab --strict` on a retired tag at lines 46 and 100 of WI-1024's
  queued spec, which trunk's `1b15d07fb` wrote (the file is byte-identical
  to this branch's base) and trunk fixed at `dd8f79e6c`; the branch picks
  the fix up at the merge. Its budget line reads CPU 922.3 s against 540, a
  WARN only.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="f9aa0914f (its tree before the commit)" -->
- `trace.py --root . --strict`: `orphans=0 integrity=0`.
  `check_trajectory.py --strict`: clean. `scripts/check_resync.py`: "OK, no
  shipped path changed". Ruff check and format on the test module: clean.
  The build commit passed the hook (29 steps, all PASS).

**Byte deltas** (none budgeted or watched; the byte-budget-guard's list is
unchanged): the template 5,767 -> 5,718 (-49); `references/recipes.md`
110,525 -> 110,528 (+3, in each of the three copies);
`docs/test/test-cases.toml` 676,393 -> 676,432 (+39);
`tests/test_prompts.py` 68,846 -> 69,018 (+172).

**Acts owed:** TC-385's drift, for automated adjudication. Its method and
expected cells changed under an unchanged `Accepted` status; the hook
reports the amendment, and `docs/ratify/CURRENT.md` lists its chain
(SR-243) under "Waiting for automated adjudication". This branch takes no
act.

**Found, not changed (outside the spec's files):**

- SR-243 (Accepted) still names "the sole Sol or Terra launch route" in its
  requirement and "the only Sol or Terra launch path" in its acceptance
  criteria. Filed on trunk as WI-1046, which needs this row for TC-385's
  wording.

**Review** (the coordinator, 2026-11-21; queue-drill HANDOFF §4 step 4).
Round 1 over `1b22c9355..2cb001733`, the generated views and this spec's
copies withheld from the diff and the spec at the tip given whole: OpenAI
Sol (`gpt-6.1-sol`, low, via `codex exec`) read the whole diff, and Gemini
Hydrogen (`gemini-4-hydrogen-low`, via the Antigravity CLI) read the prose
and registry part by file reference. Sol: `VERDICT: APPROVE findings=0`.
Hydrogen: `VERDICT: APPROVE findings=0`. No findings, so no fix and no
further round.

## Context

Filed on trunk on 2026-11-21 from WI-1037's close-out, which found three
things outside its files (its Deliverable, "Found, not changed"; its
decision D-003).

- `scripts/coordinator/terra-spine-prompt.template.md` still names models
  ("GPT Terra", "a Claude Opus builder", "Claude Opus adjudicator") where it
  means roles, and `tests/test_prompts.py` pins one of those phrases. The
  operator's rule behind WI-1037: which model fills a role is a setting.
- TC-385 (Accepted) names Sol and Terra in its method and expected cells.
  WI-1037 left it, since amending it owes an act a text-only row did not
  take.
- In `coordinator-cycle` recipes §5, the bullet about counting carriage
  returns has lost its `\r` escapes in three places: a raw newline sits
  between the backticks. The defect predates WI-1037.

The three ride one row because each is a small text fix the same review
reads; none changes behaviour. The template's file name stays (renaming it
is a launch-path change outside this row).

## Done-when

- [x] The template names the roles (the author, the builder, the
      adjudicator); an observation tied to one model keeps its evidence,
      labelled "observed with <model>"; its pin in `tests/test_prompts.py`
      follows.
- [x] TC-385's method and expected cells name the roles (text only, its
      status unchanged); the Deliverable lists its drift for automated
      adjudication.
- [x] Recipes §5's three escapes read `\r` again, in all three byte-equal
      copies of the skill (regenerated, not hand-edited).
