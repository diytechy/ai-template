+++
id = "WI-453"
title = "Execute the DevStg-Boundary hats roster (sitting-2 decision 11, owner-ruled 2026-08-13q/r/s): the roster is settled AT the boundary rung, and three things are owed. (1) FIX FIRST-RUN-ADOPTER's predicate — it keys on a `scope` field SN rows do not carry (SN-039's job), so its three `scope ==` clauses are silent by DEFECT, not true; the hat is KEPT (it is the declared Adopter entity's only voice in review, and the schedule.py MAPPING omission is its worked failure class), so re-point it at a predicate that actually fires. (2) ADD seven hats: UX-DESIGNER and UX-ENGINEER (the surfaces the session reads under REL-002 — PROJECT_STATE.html, open-items.html; B-03 was REMOVED as a crossing at 13u, so these are adopted-toolkit outputs the session consumes, not system outputs — the hats' warrant is the reader, not a crossing) which apply here unconditionally, plus SAFETY, LEGAL, DATA-PROTECTION, ACCESSIBILITY and PERFORMANCE which ship OFF BY DEFAULT. Mechanism: hats.py REFUSES unknown keys (REQUIRED_KEYS is exactly applies_when/asks/listens_for), so there is no `enabled` field to add without changing a shipped script + its template + its tests — instead use the grammar's own ruled behaviour ('a field the composer did not declare satisfies no condition') and key each aspect hat on its own tag, so it ships silent and switches on when a project tags work with it. (3) STATE THE DISTINCTION in the roster header: these aspect hats are silent BY DESIGN (awaiting a tag) while FIRST-RUN-ADOPTER was silent BY DEFECT — a reader cannot tell them apart otherwise. Scope note: the roster SHIPS (registries/hats.template.toml scaffolds to docs/requirements/hats.toml), so decide the template-vs-this-repo split deliberately per the kit's VALUES-may-diverge/STRUCTURE-must-not rule — recommended: UX hats unconditional in this repo, render/ui-gated in the shipped starting roster. Proposed row text for all seven is in the sitting-2 brief, decision 11, and is OWNER TEXT TO CONFIRM before it lands (a roster chosen by an agent and left unread is the ceremony SN-036 exists to prevent). Verify with hats.py's own refusal paths (missing key, unevaluable condition) and the dogfood-sync pin over the template copy."
specref = ""
workstream = "process"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

The Decision 11 roster (rulings 2026-08-13q/r/s, accepted 13u) executed, all
three owed things, in `docs/requirements/hats.toml` + the shipped
`project-trajectory/registries/hats.template.toml`:

1. **FIRST-RUN-ADOPTER fixed, kept.** Old predicate
   `'scope == "template" or scope == "both" or tags contains "templates"'` →
   new `'tags contains "scripts" or tags contains "templates" or tags
   contains "process"'` — keyed on the deliverable's real tags (the kit's
   product is its shipped scripts, templates and process docs), same row in
   both copies. Driven over every real work-item context: 453 rows
   <!-- fig: cmd=".venv/bin/python -m pytest -q tests/test_hats.py -k old_first_run_adopter" rev=ceb6d5d0 (the census the test derives: docs/work/**/*.md front matter -> hats.context_from_work_item) -->;
   the old predicate's `scope ==` clauses fire on 0 of them and the whole old
   predicate on exactly 1 (WI-131, 2026-07-13, a workstream label no later
   row uses) <!-- fig: derived="the same census, old predicate evaluated per row" -->;
   the new predicate fires on 224
   <!-- fig: derived="the same census, new predicate evaluated per row" -->.
   **Census refinement over the ruling's "silent":** the `templates` tag
   clause had fired once in history — effectively voiceless, not literally;
   the test (`test_the_old_first_run_adopter_predicate_was_defective_and_the_new_one_fires`)
   states the measured truth.
2. **Seven hats added, owner row text verbatim from Decision 11** (13u ruled
   "the rows below and the FIRST-RUN-ADOPTER predicate fix are the text
   WI-453 executes" — no owner-text-pending remainder): UX-DESIGNER +
   UX-ENGINEER, `always` in this repo's instance (the REL-002 reader of
   PROJECT_STATE.html / open-items.html), `render`/`ui`-gated in the shipped
   template — the accepted VALUES-diverge split, STRUCTURE identical
   (`test_the_ux_pair_is_unconditional_here_and_render_gated_in_the_template`
   also pins asks/listens_for byte-identical across copies); SAFETY, LEGAL,
   DATA-PROTECTION, ACCESSIBILITY, PERFORMANCE each keyed on its own tag
   (`safety`/`legal`/`personal-data`/`a11y`/`perf`) — OFF by the grammar's
   undeclared-field rule, no `enabled` key, no schema change, proven silent
   on all 453 real rows and live under their tags
   (`test_aspect_hats_ship_silent_by_design_and_switch_on_by_tag`).
3. **The two kinds of silence stated in both roster headers**: aspect hats
   silent BY DESIGN (awaiting a tag) vs FIRST-RUN-ADOPTER's old silence BY
   DEFECT (keyed on a field no context declares) — plus the values-diverge
   note on the UX pair in the instance header, and the template header now
   tells adopters to make every silent hat silent on purpose.

Refusal paths (missing key, unevaluable condition, unknown key, malformed
TOML, falsey table) were already driven in `tests/test_hats.py`; the
template/instance structure pin and the thirteen-hat template census pin
updated in place. Prose counts updated: `project-trajectory/README.md`,
`bootstrap.py` MAPPING comment, `test_bootstrap.py` scaffold-list comment.
