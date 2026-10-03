+++
id = "WI-766"
title = "adjudicate: LLR-254, SR-215, TC-024, TC-036, TC-055, TC-209, TC-210, TC-211, TC-247, TC-248 - approved/routed cell(s) amended on merged trunk 122816d..1f1dc64 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-215"]
specref = "docs/requirements/system-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-254", "SR-215", "TC-024", "TC-036", "TC-055", "TC-209", "TC-210", "TC-211", "TC-247", "TC-248"]
+++

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-215 `AcceptanceCriteria`: 'At a work-item merge and at release preparation, each observation test case has its declared inputs hashed; one whose d…' -> 'Every observation case references a numbered rubric written before its first judgement; existing omissions warn. No res…'
- SR-215 `Rationale`: 'A judgment made by inspection, critique or observation holds only for the state it looked at, and nothing re-fires it o…' -> 'Judgements cost time and model calls and vary across sessions. A fixed rubric makes the pass criterion reviewable; a cl…'
- SR-215 `Requirement`: 'When a work item merges or a release is prepared, the delivered harness shall file one re-judge work item for each obse…' -> 'When a work item merges, a release is prepared or a stage gate is checked, the delivered harness shall file one re-judg…'
- LLR-254 `Detail`: 'A pure sibling of consolidate.py that intake imports. observation_test_cases(root, rev) reads the observation cases at …' -> 'A sibling of consolidate.py imported by intake. observation_test_cases(root, rev) reads observation cases at a revision…'
- TC-024 `Verifies`: 'SR-024;LLR-024' -> 'SR-024;LLR-024;IF-270'
- TC-036 `MinWorkItems`: '' -> '10'
- TC-036 `Rubric`: '' -> 'docs/rubrics/resync-inspection.md'
- TC-036 `Trigger`: '' -> 'files:project-trajectory/ADOPTING.md;project-trajectory/skills/downstream-resync/*'
- TC-055 `MinWorkItems`: '' -> '10'
- TC-055 `Rubric`: '' -> 'docs/rubrics/dashboard-usability.md'
- TC-055 `Trigger`: '' -> 'component:CMP-009'
- TC-209 `MinWorkItems`: '' -> '10'
- TC-209 `Rubric`: '' -> 'docs/rubrics/critique-provenance.md'
- TC-209 `Trigger`: '' -> 'release'
- TC-210 `MinWorkItems`: '' -> '10'
- TC-210 `Rubric`: '' -> 'docs/rubrics/counterpart-review.md'
- TC-210 `Trigger`: '' -> 'release'
- TC-211 `MinWorkItems`: '' -> '10'
- TC-211 `Rubric`: '' -> 'docs/rubrics/decomposition-proportionality.md'
- TC-211 `Trigger`: '' -> 'release'
- TC-247 `Expected`: "Satisfies SR-215's acceptance: a changed, expired or unjudged observation case gets exactly one open re-judge item nami…" -> 'Satisfies SR-215 acceptance: missing or expired evidence is due; other judgements obey their trigger and floor, and eac…'
- TC-247 `Method`: 'checkpoint_drafts driven on a real git repository. An observation case whose declared input changed since its latest re…' -> 'checkpoint_drafts driven on a real git repository. No result and expiry are due independently of the floor. Changed inp…'
- TC-248 `Method`: "Driven through intake on a real git repository. A merged work item whose merge changes an observation case's declared i…" -> 'Driven through intake on a real git repository. A merged work item satisfying an observation case’s trigger and closed-…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-254 [project-trajectory/scripts/rejudge.py :: observation_test_cases/checkpoint_for/checkpoint_drafts/_open_rejudge/due_cases/BRIEF/CHECKPOINTS] tests: - — The checkpoint re-judge decision
- LLR-255 [project-trajectory/scripts/intake.py;project-trajectory/scripts/gen_release_checklist.py :: intake_after_merge/mint_rejudge/_cmd_rejudge/_rejudge_checklist_line] tests: - — The merge and release checkpoints file the re-judge items
- LLR-265 [project-trajectory/scripts/intake.py :: merged_outcomes/_merged_shape_refusal/_cmd_sweep] tests: - — The merge-slot intake re-run for a merge made outside the s…
- LLR-293 [project-trajectory/scripts/observation_cadence.py :: Cadence] tests: - — The observation cadence policy
- LLR-294 [project-trajectory/scripts/observation_cadence.py :: observation_rubric_findings] tests: - — The observation rubric-reference advisory
- TC-247 -> tests/test_rejudge.py

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-018 scripts/gen_release_checklist -> external:downstream adopter: file docs/release-checklist.md — one `- [ ] <ID> — <what to confirm> (refs)` item per human-verified row
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-034 docs/requirements/ -> scripts/gen_release_checklist;external:downstream adopter: file None
- IF-050 scripts/derive_stage -> scripts/check;scripts/agent_common;scripts/check_trajectory;scripts/traj_parse;scripts/intake: file docs/stage — key = value fields plus a sha256 fingerprint of the declared inputs
- IF-053 scripts/schedule <- scripts/census;scripts/dispatch;scripts/intake: call load_wis · _load, frontier, kind_of · SAFETY_CLASSES — the symbols census, dispatch and intake take; no write…
- IF-090 scripts/intake <- scripts/integrate;scripts/dispatch;scripts/agent_loop: call intake_after_merge (integrate) · mint_gap_rows (dispatch) · context_block (agent_loop, advisory)

## Dispositions

Verdict: `docs/reviews/wi-766-adjudicate-llr-254-sr-215-t/001-ADJUDICATE-30ee386.md`,
MEANING on all nine rows; its 2026-10-03 addendum corrects the bless list. The
rows blessed as written are TC-036, TC-055, TC-209, TC-210 and TC-211. SR-215,
LLR-254, TC-247 and TC-248 return. WI-767 returned LLR-293, LLR-294, TC-306
and TC-307
(`docs/reviews/wi-767-adjudicate-llr-293-llr-294/001-ADJUDICATE-30ee386.md`).
One lane carries every returned row. Two lanes would couple through the
snapshot: a registry copy is refused while any approved row in it has drifted.

```toml
title = "Rework the SR-215 cadence rows WI-766 and WI-767 returned, and prompt the stage-gate re-judge at the gate"
workstream = "process"
buildtier = "medium"
safety_class = "spine"
sr_refs = ["SR-215"]
priority = 2
```

Each cell below is replaced whole with the text given. Write it byte-exact
apart from TOML escaping.

**Prohibitions.**
- Change no other cell of these rows, and no cell of any other approved row.
  TC-036, TC-055, TC-209, TC-210, TC-211, LLR-265 and TC-261 stay
  byte-identical.
- Under ruling R2, no SR-215 cell names a script, command, file or function.
- Do not flip any Status. Amended rows stay `Approved`; reworked rows stay
  `Drafted`. The approvals are the adjudications' to give.
- Change no production code. The only code edits allowed are the test
  assertions the TC-247 bullet names.
- Do not touch TC-279. It waits for WI-667.

**Landing.** The merge mints an amendment adjudication for SR-215, LLR-254,
LLR-255, TC-247 and TC-248, and a first-approval adjudication for LLR-293,
LLR-294, TC-306, TC-307 and the new TC. The coordinator carries TC-036,
TC-055, TC-209, TC-210 and TC-211 into the amendment adjudication's
`adjudicates` list (as in wave 6, carrying held approvals) and checks that they
render. That lets one sitting re-anchor the whole test-case registry.

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
- `detail`: replace only the sentence `` mint_rejudge(root, rev, checkpoint) files them through _mint, and `intake.py rejudge --checkpoint release` is the release-preparation entry. `` with `` mint_rejudge(root, rev, checkpoint) files them through _mint; `intake.py rejudge --checkpoint release` is the release-preparation entry and `intake.py rejudge --checkpoint stage-gate` the stage-gate-preparation entry, and the command refuses a merge checkpoint, which only the merge slot runs. `` Every other sentence of the cell stays byte-exact.

**TC-247 (amend).**
- `method` -> `checkpoint_drafts driven on a real git repository. No result and expiry are due independently of the floor. Changed inputs with no trigger are due only once the configured closed-WI floor is met. File, component, release and stage-gate triggers are due only when they fire and the floor is met; a case may raise but cannot lower the default floor. A draft names the case, its reason, its rubric and the changed input or the fired trigger, and its title carries the case id and the inputs-digest prefix. An open typed re-judge item suppresses a second; a closed archived item with the same title does not. Policy and inputs are read at the given revision: uncommitted changes affect neither. Committed links are excluded, including self-links and platforms checking them out as text. No model runs.`
- No test today asserts that a draft's context names the rubric, or the fired trigger for a triggered case. Add those assertions to `tests/test_rejudge.py`, and change nothing else in it.

**TC-248 (amend).**
- `method` -> `Driven through intake on a real git repository. A merged work item satisfying an observation case's trigger and closed-WI floor mints one re-judge item; another merge while it is open mints none. Release preparation mints for expired or release-triggered due cases, and the generated release checklist carries one required item naming the release re-judge command and the count of cases due at the release checkpoint. The stage-gate command files one item for a stage-gate-triggered case past its floor, none at merge and none while one is open, and the command refuses a merge checkpoint. Minting follows the mint checks and preserves unrelated uncommitted edits.`
- `expected` -> `Satisfies SR-215's acceptance at every checkpoint: a work-item merge, release preparation and stage-gate preparation each file one re-judge item per due case and never a second while one is open.`
- The stage-gate clause is
  `tests/test_rejudge.py::test_stage_gate_trigger_is_filed_through_the_cli_not_at_merge`,
  and the merge refusal is
  `tests/test_rejudge.py::test_the_cli_refuses_a_manual_merge_checkpoint`.
  Both modules are already in its Evidence cell.

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
- `method` = `Run the trajectory check with --strict on a tree holding no work items and a real observation case with no rubric reference.`
- `expected` = `The check exits 0 and prints one warning naming the case and the missing rubric; strict mode never promotes it to a failure.`
- `evidence` = `tests/test_rejudge.py::test_trajectory_rubric_warning_survives_strict_and_no_work_items`
- `phase` = `6`, `status` = `"Drafted"`

**The gate prompt (shipped skill).** In
`project-trajectory/skills/gate-advance/SKILL.md`, insert this paragraph
directly after the paragraph beginning "Run the checks with
`scripts/check.py`":

> **File the stage-gate re-judges before you sign (required).** At the commit
> you are about to sign, run `python scripts/intake.py rejudge --checkpoint
> stage-gate`. It files one re-judge item for each observation case whose
> declared `stage-gate` trigger is due past its closed-work floor, and none
> while one is open (PROCESS.md "Observation judgement"). Paste its output into
> the `docs/log.md` audit entry beside the check output.

Then regenerate the dogfooded copies under `.claude/skills/gate-advance/` and
`.agents/skills/gate-advance/` (`gen_skills_index.py --check-agents` must
pass). Add a RESYNC_PACK.md entry for the shipped skill change. Nothing else
in the skill changes.
