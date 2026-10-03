+++
id = "WI-770"
title = "Rework the SR-215 cadence rows WI-766 and WI-767 returned, and prompt the stage-gate re-judge at the gate"
workstream = "process"
sr_refs = ["SR-215"]
specref = ""
buildtier = "medium"
priority = 2
safety_class = "spine"
+++

## Deliverable

WI-766's adjudicator draft applied byte-exact (19 replacement cells checked
mechanically):

- SR-215 now states the no-result rule the right way round, names no script, and
  drops the rubric clause that tripped trace's CRITIQUE-instrument advisory.
- LLR-254 and LLR-255 amended; LLR-255 carries the release and stage-gate command
  entries and the gate-advance clause.
- TC-247 and TC-248 amended, with TC-247's naming assertions and TC-248's doc-pin
  evidence.
- LLR-293, LLR-294 and TC-306 reworked (Drafted); TC-311 added (Drafted).
- The shipped gate-advance skill gains a required pre-sign step,
  `python scripts/intake.py rejudge --checkpoint stage-gate`, pinned by
  `tests/test_skills_index.py::test_gate_advance_names_the_stage_gate_rejudge_step`.
- RESYNC entry re-anchored at the landing's parent.
- No production code changed, and no Status flipped.

Sonnet 5.5: SOUND at 719dcaeb.

## Context

Drafted by WI-766 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

Each cell below is replaced whole with the text given. Write it byte-exact
apart from TOML escaping.

**Prohibitions.**
- Change no other cell of these rows, and no cell of any other approved row.
  TC-036, TC-055, TC-209, TC-210, TC-211, LLR-265 and TC-261 stay
  byte-identical.
- Under ruling R2, no SR-215 cell names a script, command, file or function.
- Do not flip any Status. Amended rows stay `Approved`; reworked rows stay
  `Drafted`. The approvals are the adjudications' to give.
- Change no production code. The only code edits allowed are these three:
  the TC-247 assertions, a `Rubric` column in the `cadence_repo` helper of
  `tests/test_rejudge.py` (the one sanctioned helper change), and the new
  gate-advance doc-pin test in `tests/test_skills_index.py`.
- Do not touch TC-279. It waits for WI-667.

**Landing.** The merge mints two adjudications:
- an amendment adjudication for SR-215, LLR-254, LLR-255, TC-247 and TC-248;
- a first-approval adjudication for LLR-293, LLR-294, TC-306 and the new TC.

Two rows ride in on neither mint, so the coordinator adds them:
- It carries TC-036, TC-055, TC-209, TC-210 and TC-211 into the amendment
  adjudication's `adjudicates` list (as in wave 6, carrying held approvals) and
  checks that they render.
- It carries TC-307 into the first-approval adjudication's `adjudicates` list.
  TC-307 gets no text change, so `staged_drafted_rows` never mints it, and
  `first_approval_values` renders `adjudicates` ∩ the live Drafted rows.
- TC-279 stays out until WI-667 lands.

The two adjudications must not act out of order. A first-approval copy of the
LLR or TC registry is refused while LLR-254, LLR-255 or the drifted TC rows are
unattested. Preferred: one sitting with one combined act, batch-M style. The
first-approval flips and the amendment re-attestations go in one commit, under
one `intake.py snapshot --approves "..." --reattests ...`, with both trailers.
If they sit separately instead, the amendment adjudication's act lands first,
and the coordinator adds a `needs` edge from the first-approval row to it after
the mint.

**SR-215 (amend).** `trace.py` currently flags it because its Rationale and
AcceptanceCriteria use the word "rubric" while Verification is Test. The
replacement text below contains no "rubric", so the finding clears. Confirm
that `trace.py --strict` no longer prints the "SR SR-215 ... names a CRITIQUE
instrument" advisory.
- `title` -> `At a checkpoint, an unjudged, expired or triggered observation test is queued once for re-judging`
- `requirement` -> `When a work item merges, a release is prepared or a stage gate is checked, the delivered harness shall file one re-judge work item per due observation case: one with no result, one whose result expired, or one whose declared trigger fires after its work-item floor; with no declared trigger, a change to its declared inputs makes it due, subject to that floor. It keeps at most one open item per case, and reports each observation case that cites no written pass criteria as a warning.`
- `rationale` -> `Judgements cost time and model calls and vary across sessions. Written pass criteria fixed before the first judgement make the pass reviewable. The closed-work floor is a cost limit the owner directed (the PERFORMANCE lens): it lets an accepted judgement outlive changes to what it judged for at most the configured number of closed work items, while first judgement and expiry keep missing or old evidence from standing indefinitely.`
- `acceptance_criteria` -> `A case with no result is due at once, and a case whose result expired is due at once; neither waits for the floor. Otherwise a declared trigger (matching changed files, a change to a module tagged with the named component, release preparation, or a stage-gate check) makes a case due only once the configured number of closed work items has passed since its latest record was committed; a case may raise that number but not lower it. With no trigger, a change to its declared inputs makes it due, subject to the same floor; with neither a trigger nor inputs, only absence and expiry make it due. Inputs and policy are read at the checkpoint revision. An open re-judge item suppresses a second, and the decision runs no model. An observation case that cites no written pass criteria is reported as a warning, never a failure, including under strict checking.`
- `coincident` -> `The needs ask that an accepted observation not stand on a state it never judged, and that it be judged against written criteria. Filing one re-judge item for each case that is unjudged, expired or triggered past its floor, and warning on a case that cites no criteria, is that outcome within the cost bound the floor sets. The judging itself is the re-judge item's own.`
- `hat_refs` stays `["TEST-ENGINEER", "PERFORMANCE"]`. PERFORMANCE already records the cost lens the floor derives from, and the new Rationale argues it.

**LLR-254 (amend).**
- `detail` -> `A sibling of consolidate.py imported by intake. observation_test_cases(root, rev) reads observation cases at a revision. checkpoint_for(root, rev, tc) returns the case's Trigger when it names the release or stage-gate checkpoint, else merge. due_cases(root, rev, now, checkpoint) reads committed inputs and records and uses the cadence decision to apply the configured closed-WI floor and declared trigger. A case with no record is due at once, and an expired record is due at once; neither waits for the floor. Without a trigger, a changed input digest is due subject to the floor; without inputs, only absence and expiry make a case due. checkpoint_drafts drafts each due case once, suppressing an open item by its typed Brief and Adjudicates cells, never by title. A draft names the case, the reason, the rubric and the changed inputs or the fired trigger, and its title carries the case id and the inputs-digest prefix. Committed links are excluded by the observation writer's own link predicate. No model runs.`

**LLR-255 (amend; its module is intake.py).**
- `title` -> `The merge, release and stage-gate checkpoints file the re-judge items`
- `detail` -> `` intake_after_merge adds rejudge.checkpoint_drafts(root, after, "merge") to its drafts inside the held merge slot, so the check runs once per merged work item. mint_rejudge(root, rev, checkpoint) files them through _mint; `intake.py rejudge --checkpoint release` is the release-preparation entry and `intake.py rejudge --checkpoint stage-gate` the stage-gate-preparation entry, and the command refuses a merge checkpoint, which only the merge slot runs. Release and stage-gate preparation are a person's acts, so each is prompted where that person works. The release checklist, a view that may not import intake, carries a required item from _rejudge_checklist_line naming the release command and the count of observation cases due at the release checkpoint, read through rejudge's pure decision. The shipped gate-advance skill names the stage-gate command as a required step before a rung is signed. The minted row's brief and verdict entries are added where its kind requires them. Filing goes through the mint path's staging, which has to stage and restore only what it wrote before this runs in a checkout holding uncommitted edits. ``
- This replaces the whole cell. Against today's cell, the changes are:
  - the stage-gate entry and the merge refusal;
  - "naming that command" becomes "naming the release command";
  - the count is "due at the release checkpoint", which is what
    `gen_release_checklist` passes;
  - the gate-advance clause.
  Everything else is today's text.
- `module` and `code_symbol` stay unchanged. Do NOT add the skill file to
  Module. No LLR's Module names a `.md` file today, and Module/CodeSymbol are
  resolved against code by check_trajectory's cross-check. The doc-pin test
  under TC-248 anchors the skill clause. The consequence: a `component:CMP-008`
  trigger does not fire on an edit to the skill.

**TC-247 (amend).**
- `method` -> `checkpoint_drafts driven on a real git repository. No result and expiry are due independently of the floor. Changed inputs with no trigger are due only once the configured closed-WI floor is met. File, component, release and stage-gate triggers are due only when they fire and the floor is met; a case may raise but cannot lower the default floor. A draft names the case, its reason, its rubric and the changed input or the fired trigger, and its title carries the case id and the inputs-digest prefix. An open typed re-judge item suppresses a second; a closed archived item with the same title does not. Policy and inputs are read at the given revision: uncommitted changes affect neither. Committed links are excluded, including self-links and platforms checking them out as text. No model runs.`
- No test today asserts that a draft's context names the rubric, or the fired trigger for a triggered case. No `cadence_repo` case carries a `Rubric` (the brief prints "(not declared)"). Add a `Rubric` column for TC-002 in the `cadence_repo` helper, then add the two assertions to `tests/test_rejudge.py`. Change nothing else in it.

**TC-248 (amend).**
- `method` -> `Driven through intake on a real git repository. A merged work item satisfying an observation case's trigger and closed-WI floor mints one re-judge item; another merge while it is open mints none. The release command mints for an expired case and not twice while its item is open; at the release checkpoint a release-triggered case is drafted only once its floor is met. The generated release checklist carries one required item naming the release re-judge command and the count of cases due at the release checkpoint. The stage-gate command files one item for a stage-gate-triggered case past its floor, none at merge and none while one is open, and the command refuses a merge checkpoint. The shipped gate-advance skill names the stage-gate command as a required step before a rung is signed. Minting follows the mint checks and preserves unrelated uncommitted edits.`
- `expected` -> `Satisfies SR-215's acceptance at every checkpoint: a work-item merge, release preparation and stage-gate preparation each file one re-judge item per due case and never a second while one is open.`
- `evidence` -> `tests/test_rejudge.py; tests/test_intake.py; tests/test_skills_index.py::test_gate_advance_names_the_stage_gate_rejudge_step`
- Where each clause lives:
  - Release minting: `tests/test_rejudge.py::test_the_release_subcommand_mints_for_an_expired_result_once`.
  - Release-triggered drafting past the floor: `tests/test_rejudge.py::test_trigger_waits_for_closed_work_floor` (its `release` case).
  - The checklist item: `tests/test_rejudge.py::test_the_release_checklist_carries_the_required_rejudge_item`.
  - The stage-gate command: `tests/test_rejudge.py::test_stage_gate_trigger_is_filed_through_the_cli_not_at_merge`.
  - The merge refusal: `tests/test_rejudge.py::test_the_cli_refuses_a_manual_merge_checkpoint`.
  - The skill step: the new `tests/test_skills_index.py::test_gate_advance_names_the_stage_gate_rejudge_step`. It reads `project-trajectory/skills/gate-advance/SKILL.md`'s body (below the frontmatter) and asserts it contains the literal `python scripts/intake.py rejudge --checkpoint stage-gate` and the word "required".

**LLR-293 (rework, Drafted).**
- `detail` -> `Cadence reads the process policy at the committed checkpoint and counts distinct terminal archived WI IDs added since the commit that added the latest observation record. eligible applies the greater of default and case floors, then file globs, component-tagged LLR modules and interface owners, release or stage-gate triggers. An omitted trigger leaves input-digest comparison to rejudge. History is cached per result commit; malformed policy, an unknown trigger and unreadable history raise ValueError. Zero explicitly disables the default floor.`
- This drops both intake CLI sentences; LLR-255 now carries the entries.

**LLR-294 (rework, Drafted).** It rests on SR-215's new acceptance clause, "An
observation case that cites no written pass criteria is reported as a warning,
never a failure, including under strict checking". If that clause is reworded,
keep it meaning the same, or this row loses its parent.
- `detail` -> `observation_rubric_findings returns one warning for each real observation case omitting Rubric, naming the case. Automated and example cases are excluded. check_trajectory prints the warnings before its no-WI return and never promotes them under strict.`
- This drops "Creation requires the numbered rubric first". That rule's one home is PROCESS.md "Observation judgement", which keeps it.

**TC-306 (rework, Drafted).**
- `expected` -> `A declared trigger fires only after the closed-WI floor; with no declared trigger, a change to declared inputs fires subject to the same floor; absence and expiry bypass both.`

**TC-307 (Drafted).** No text change. It verifies the function half, and the
new case below verifies the check_trajectory half. `test_rejudge.py` is
outside the smoke tier, so citing it here would contradict `Tier = Smoke`.

**New TC (Drafted), next id from the watermark.**
- `verifies` = `["SR-215", "LLR-294", "IF-269"]`
- `level` = `"Integration"`, `tier` = `"Full"`, `automated` = `"Yes"`
- `method` = `Run the trajectory check with --strict on a tree holding no work items and real observation cases with no rubric reference.`
- `expected` = `The check exits 0 and prints a warning naming a case and its missing rubric; strict mode never promotes these warnings to a failure.`
- `evidence` = `tests/test_rejudge.py::test_trajectory_rubric_warning_survives_strict_and_no_work_items`
- `phase` = `6`, `status` = `"Drafted"`

**The gate prompt (shipped skill).** In
`project-trajectory/skills/gate-advance/SKILL.md`, insert this paragraph
directly after the paragraph beginning "Run the checks with
`scripts/check.py`":

> **File the stage-gate re-judges before you sign (required).** At the commit
> you are about to sign, run
> `python scripts/intake.py rejudge --checkpoint stage-gate`
> (keep the command on one line; the doc-pin matches it literally).
> It files one re-judge item for each observation case whose
> declared `stage-gate` trigger is due past its closed-work floor, and none
> while one is open (PROCESS.md "Observation judgement"). Paste its output into
> the `docs/log.md` audit entry beside the check output.

(The parenthesis about one line is an instruction to you; do not insert it into
the skill.)

Then refresh the byte copies under `.claude/skills/gate-advance/` and
`.agents/skills/gate-advance/` with
`python project-trajectory/scripts/bootstrap.py --dest . --sync` (`--dest` is
required). Confirm with
`python project-trajectory/scripts/gen_skills_index.py --check-agents`, which
only checks. Add a NEW RESYNC_PACK.md entry anchored
`[since <trunk HEAD at build>]` for the shipped skill step. Do not extend the
WI-747 entry anchored `[since 122816da]`: an adopter already synced past that
anchor would never see an extension. Nothing else in the skill changes.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-254 [project-trajectory/scripts/rejudge.py :: observation_test_cases/checkpoint_for/checkpoint_drafts/_open_rejudge/due_cases/BRIEF/CHECKPOINTS] tests: - — The checkpoint re-judge decision
- LLR-255 [project-trajectory/scripts/intake.py;project-trajectory/scripts/gen_release_checklist.py :: intake_after_merge/mint_rejudge/_cmd_rejudge/_rejudge_checklist_line] tests: - — The merge and release checkpoints file the re-judge items
- LLR-265 [project-trajectory/scripts/intake.py :: merged_outcomes/_merged_shape_refusal/_cmd_sweep] tests: - — The merge-slot intake re-run for a merge made outside the s…
- LLR-293 [project-trajectory/scripts/observation_cadence.py :: Cadence] tests: - — The observation cadence policy
- LLR-294 [project-trajectory/scripts/observation_cadence.py :: observation_rubric_findings] tests: - — The observation rubric-reference advisory
- LLR-295 [project-trajectory/scripts/adjudicate_brief.py :: _assumption_case_chain/_render_assumption_cases/_rejudge_case_text] tests: TC-308;TC-309 — Assumption-only observation cases in adjudicator briefs

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-018 scripts/gen_release_checklist -> external:downstream adopter: file docs/release-checklist.md — human-verified rows use `- [ ] <ID> — <what to confirm> (refs)`; assumption confi…
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-034 docs/requirements/ -> scripts/gen_release_checklist;external:downstream adopter: file None
- IF-050 scripts/derive_stage -> scripts/check;scripts/agent_common;scripts/check_trajectory;scripts/traj_parse;scripts/intake: file docs/stage — key = value fields plus a sha256 fingerprint of the declared inputs
- IF-053 scripts/schedule <- scripts/census;scripts/dispatch;scripts/intake: call load_wis · _load, frontier, kind_of · SAFETY_CLASSES — the symbols census, dispatch and intake take; no write…
- IF-075 scripts/trace <- scripts/gen_open_items;scripts/adjudicate_brief: call reattest_model entries: chain rows, changed cells, baseline rev and date, and each spine registry's own copy …
