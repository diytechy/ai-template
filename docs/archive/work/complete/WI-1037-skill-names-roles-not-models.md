+++
id = "WI-1037"
title = "The coordinator-cycle skill names each role, never the model that fills it, which is a setting"
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

Built on the maintenance branch `maint/wi-1037`, cut from `refactor_again` at
`1aa6c439a`, with the commit hooks on. The specref (the queue-drill hand-off,
§3.3 N5) is cleared at close, as a terminal row's is.

- `97f2246dd`: the skill, its recipes and the coordinator tools' README name
  roles; the two copies refreshed; the pins; the decisions record; the
  regenerated views.
- The close-out commit after it: this Deliverable, the move to `complete/`
  and the log fragment.

**The Roles table** names each role (Build: the builder; Spine author: the
author; Code review, REVIEW-A and REVIEW-B: a code reviewer; Scope and plan
critique: the critic; Adjudication: the adjudicator) and states no model or
effort. A list under it says where each is set: a role's route is the
enabled roster row it resolves to (`ROLE_ROUTES` in `codex_call.py`, read
against `docs/agents.toml` and `docs/agents-enabled`; the adjudicator's
default entry in `coordinator_adjudicate.py`; `--route` names another), the
row gives the model and a `codex_call.py` call's effort is its `--effort`;
the builder's model and effort are `.claude/agents/kit-builder.md`'s, and
the REVIEW-B stand-in's are the operator's ruling, coordinator-2026-10-16
D-008.

**The text.** Every "Terra", "Sol", "Opus", "Claude", "Gemini" or "Luna"
that stood for a role names the role, in `SKILL.md`, `references/recipes.md`
and `scripts/coordinator/README.md`. The recipe headings "A Codex call (Sol
or Terra)", "Terra, first turn", "Terra, resumed" and §5's "brief Terra with
these" name the role, and `SKILL.md`'s citations follow. "Codex" stays where
it names the CLI (the `codex` CLI on `PATH`, its sandbox, its shell, the
quoted 400 error), and `codex_call.py`, `terra-spine-prompt.template.md` and
the role ids are unchanged. A gotcha seen with one model keeps its evidence
and reads "observed with <model>" beside its existing date or decision
(the basetemp lock, CRLF and cp1252 writes, compressed cells, reworded
accepted phrases, the dropped `code_symbol`, the plan-file filing, the
capacity failure, the not-offered model). Where a role has no roster row:
the planner's launch passes the builder definition's `model` (today's value,
so no launch changes); the not-offered substitution's route and effort point
at coordinator-2026-10-10 D-017; TC-055's judge command takes `<model>` and
`<effort>`, with WI-920's run kept as an observation. The calls are in
`docs/decisions/maint-wi-1037.toml` (D-001 to D-003).

**The copies.** `.claude/skills/` and `.agents/skills/` were refreshed with
`bootstrap.py --dest . --sync`; `gen_skills_index.py --check-agents`: "OK -
22 per-agent skill copy(ies) match source"; `--check`: "OK - 33 skill(s),
index fresh".

**Tests.** A new pin,
`tests/test_prompts.py::test_the_cycle_names_each_role_never_the_model_that_fills_it`:
in all three copies and the README, a model name only directly after
"observed with", no model id, no effort word in the Roles table's rows, and
the table's section names `ROLE_ROUTES`, `docs/agents.toml`,
`docs/agents-enabled`, `--route`, the builder's definition and D-008. It
rides the module's file-level tag (TC-157); no row is minted. Red on the
prior text (290 sites), green after. Four existing pins follow the new
wording, their names unchanged: the blackout pin (TC-385) asserts "a
`codex_call.py` call is refused before launch"; the intent-order pin, the
reservation pin and the HATS pin key on "the spine author" and "The author,
first turn".
<!-- fig: derived="290 is the new pin's finding count on the prior text: its assertion printed one site and 'Left contains 289 more items'" -->

- Red first: the new pin and the two reworded pins on the prior text,
  `3 failed, 92 deselected in 0.48s`.
  <!-- fig: cmd="python -m pytest -q tests/test_prompts.py -k 'names_each_role or sol_and_terra_calls_are_refused or tc_rows_and_tests_before'" rev="1aa6c439a with the test edits only" -->
- The modules reading the skill and its copies, and the whole-tree tests:
  `test_prompts`, `test_overnight_legs`, `test_skills_sync`,
  `test_skills_index`, `test_skill_materialization`, `test_bootstrap`,
  `test_dogfood_sync`, `test_generated_freshness_wiring`,
  `test_module_size_ratchet`, `test_pre_commit_hook`,
  `test_adoption_record`, `test_disposition_adoption`, `test_import_layers`,
  `test_decision_record`: `522 passed, 1 skipped in 109.79s (0:01:49)`.
  <!-- fig: cmd="python -m pytest -q -n auto <the 14 modules listed>" rev="97f2246dd (its tree before the commit, less the regenerated views)" -->
- The commit checks, `run_menu.py smoke`:
  `3699 passed, 3 skipped, 18 warnings in 355.60s (0:05:55)`. Its budget
  line reads CPU 983.6 s against 540, a WARN only (WI-1039's re-tier), not
  charged to the lane.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="97f2246dd (its tree before the commit)" -->
- `trace.py --root . --strict`: `orphans=0 integrity=0`.
  `check_trajectory.py --strict`: clean. `check_resync.py`: "OK, no shipped
  path changed". Ruff check and format on the test module: clean. The
  commit passed the hook.

**Byte deltas** (none budgeted or watched; the byte-budget-guard's list is
unchanged): `coordinator-cycle/SKILL.md` 35,516 -> 36,411 (+895),
`references/recipes.md` 109,358 -> 110,387 (+1,029),
`scripts/coordinator/README.md` 5,345 -> 5,536 (+191).

**Acts owed:** none. No spine row changed. TC-385 (Accepted) still names
Sol and Terra in its method and expected cells; its text is left as
accepted (D-003), for the coordinator to file if wanted.

**Review round 1 (2026-11-21):** Argon (prose) APPROVE; Sol one MINOR,
adopted: seven observations had lost their model labels (the stand-in
trial, the background-pytest and stray-file incidents, the delayed
critiques, the stopped and resumed author turns, the week-long reset), now
restored as "observed with <model>" beside their evidence; its request for a
test pinning the labels was declined by the coordinator (it would pin
prose).

**Found, not changed (outside the spec's files):**

- `scripts/coordinator/terra-spine-prompt.template.md` names models ("GPT
  Terra, gpt-5.6-terra", "a Claude Opus builder", "An independent Claude
  Opus adjudicator"), and `tests/test_prompts.py` pins one of those phrases.
- `references/recipes.md` §5's CR-count bullet has lost its `\r` escapes
  (the text reads a backtick, a newline, a backtick, where `\r` belongs, in
  three places). It predates this row and was left byte for byte.

## Context

Filed on trunk on 2026-11-21 at the operator's direction (queue-drill
hand-off §3.3 N5). The operator: "The targeting LLM to run prose through and
spine authoring would just be configurable, I wouldn't expect a skill to be
touched."

Which model fills a coordinator role is a setting. `codex_call.py` resolves
each role to an enabled roster row (today `ROLE_ROUTES` maps `REVIEW-A` and
`CRITIQUE` to `OPENAI-SOL` and `AUTHOR` to `OPENAI-TERRA`, with `--route`
as the override). The models themselves are declared in `docs/agents.toml`.
WI-1033 moves the role defaults into `process.toml`. The skill text,
however, names the model where it means the role:

| File | "Terra" | "Sol" | Other model names |
|---|---|---|---|
| `skills/coordinator-cycle/SKILL.md` | 8 | 7 | 7 |
| `skills/coordinator-cycle/references/recipes.md` | 36 | 12 | 2 |
| `scripts/coordinator/README.md` | 4 | 2 | 0 |

The Roles table also states models and efforts that have since drifted: it
says Sol at medium, where this drill runs Sol at low. No other shipped
skill, prompt, `PROCESS.md`, `PROCESS_OPTIONS.md` or `AGENTS.template.md`
names these models. The skill is `scope: this-repo` and is copied
byte-equal into `.claude/skills/` and `.agents/skills/` (the skills-sync
check). It is not one of the byte-budget-guard's watched documents.

Settled here:

- **Roles in the text:** "the author" (the `AUTHOR` role), "the critic"
  (`CRITIQUE`), "the code reviewer" (`REVIEW-A`, `REVIEW-B`) and "the
  adjudicator". The Roles table names each role and says its model is the
  route the role resolves to, never a model or effort.
- **Observations stay, labelled.** A gotcha seen with one model (CRLF and
  cp1252 writes, the basetemp lock, compressed cells, reworded accepted
  phrases) keeps its evidence and says which model showed it and when, so
  it is checked again if the route changes.
- **No behaviour change.** File names such as
  `terra-spine-prompt.template.md`, the role ids and `codex_call.py` stay as
  they are. Renaming them is not this row's scope.

## Done-when

- [x] The coordinator-cycle skill and `scripts/coordinator/README.md` name
      roles, not models, except in labelled observations. The Roles table
      points at the route setting.
- [x] The three copies of the skill are byte-equal, and the skills index
      and skills-sync checks pass.
