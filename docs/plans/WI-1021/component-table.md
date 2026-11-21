# WI-1021: one component per file, proposed for the operator's ruling

Proposed on branch `maint/wi-1021`, cut from `refactor_again` at
`1aa6c439a`. The operator's rule (queue-drill HANDOFF §3.3 N3): a file is
ascribed to one component; a file on the shared-kernel surface
(`docs/kernel-modules-allow`) is owned by CMP-006; a configuration file has
one owner and other components read it through a `file` interface; a
near-even split, and a file doing two components' work, is flagged for
filing, never split here. The lane builds on these picks; each flagged file
keeps the ruled header and gets its own queued row on trunk.

## For the ruling first

**Near-even** (the leading component holds less than two thirds of the
file's component tags), each with its pick:

| File | Tags | Pick | Note |
|---|---|---|---|
| `scripts/acceptance_record.py` | CMP-006 8, CMP-008 5, CMP-007 1 | CMP-006 | also flagged below as two components' work |
| `scripts/check.py` | CMP-007 9, CMP-008 4, CMP-006 1 | CMP-007 | |
| `scripts/gen_open_items.py` | CMP-009 2, CMP-006 1, CMP-008 1 | CMP-009 | |
| `scripts/census.py` | CMP-006 1, CMP-008 1 | CMP-008 | |
| `scripts/check_doc_refs.py` | CMP-006 1, CMP-007 1 | CMP-007 | also flagged below as two components' work |
| `scripts/held_status.py` | CMP-006 1, CMP-008 1 | CMP-006 | |
| `scripts/id_carrier.py` | CMP-006 1, CMP-008 1 | CMP-006 | |
| `scripts/kitlib/authority.py` | CMP-006 1, CMP-008 1 | CMP-006 | |

**Two components' work** (evidence about the partition, OI-14; a queued
row each if the operator agrees):

- `scripts/acceptance_record.py`. Its declared boundary is one job:
  comparing two git trees cell by cell to say whether accepted text moved
  (LLR-158, LLR-178, LLR-202, LLR-220, LLR-222, LLR-225, LLR-302). Beside
  it sit rules the coordinator's landing runs on top of that comparison:
  the ruling-to-citer sync (`ruling_sync_lines`, LLR-298), the parent-first
  commit judgement (LLR-358), the intake mint's acceptance arms (LLR-153,
  LLR-364) and the held re-acceptance's text identity (LLR-359), all tagged
  CMP-008, and the merge-time re-acceptance refusal (LLR-278, tagged
  CMP-006). A row would weigh moving the CMP-008 rules to a CMP-008 module
  that reads the record through an interface.
- `scripts/check_doc_refs.py`. A prose lint (paths and `sym:` references,
  LLR-038, the gatekeeper's) beside the realization-symbol binding oracle
  that discharges a design row (LLR-180, the spine's). WI-1023 retires
  SR-180's chain and with it the oracle's spine role, so the row may be
  unneeded; the operator's call.

**Picks against the tag majority:**

- `hooks/pre-commit`: CMP-008 2 (LLR-358, LLR-363), CMP-007 1 (LLR-019);
  pick CMP-007. The component registry's CMP-007 row names the shipped
  pre-commit and pre-push hooks, and the hook's own interface row (IF-134)
  carries CMP-007. LLR-358 and LLR-363 are lane rules the hook runs as
  steps; they are placed through their interfaces later (WI-1024).
- `scripts/kitlib/config.py` (CMP-007 4, CMP-006 3, CMP-008 2) and
  `scripts/kitlib/git.py` (CMP-008 7, CMP-006 2, CMP-007 1): CMP-006 by the
  kernel rule. Both are on `docs/kernel-modules-allow`.

**Outside the header scope:** `scripts/dev-setup.sh` and
`scripts/dev-setup.ps1` (this repository's own copies of the dev-setup
templates) are not under `[paths] src` and are not file owners, so they owe
no header. Their pick, CMP-009, is recorded for when they enter scope; the
lane writes no header in them.

## The 34 files

Counts are LLR rows tagging the file to each component, read from
`docs/requirements/low-level-requirements.toml` at `1aa6c439a`: each row's
`module` cell names the file and its `component` cell names the component.
"Majority" means the pick is the leading component.

| # | File | Tags (LLR rows) | Pick | Reason |
|---|---|---|---|---|
| 1 | `hooks/pre-commit` | CMP-008 2 (358, 363); CMP-007 1 (019) | CMP-007 | against the majority, above |
| 2 | `scripts/acceptance_record.py` | CMP-006 8 (158, 178, 202, 220, 222, 225, 278, 302); CMP-008 5 (153, 298, 358, 359, 364); CMP-007 1 (257) | CMP-006 | near-even; majority; the two-tree comparison is the spine's acceptance conformance; flagged as two components' work |
| 3 | `scripts/adjudicate_brief.py` | CMP-008 8; CMP-006 1 (273) | CMP-008 | majority |
| 4 | `scripts/amendment_brief.py` | CMP-008 2 (167, 359); CMP-006 1 (273) | CMP-008 | majority; a brief the coordinator renders, like `adjudicate_brief` |
| 5 | `scripts/assumption_rules.py` | CMP-006 14; CMP-007 3 (242, 243, 244) | CMP-006 | majority |
| 6 | `scripts/bootstrap.py` | CMP-009 7; CMP-008 1 (339) | CMP-009 | majority |
| 7 | `scripts/census.py` | CMP-006 1 (231); CMP-008 1 (188) | CMP-008 | near-even. LLR-188 states the module's job: the registry-gap census as a read model below every module that reads it, and its readers (`dispatch`, `intake`, `adjudicate_brief`) are CMP-008's. LLR-231 is one count it reports, placed through its interface later |
| 8 | `scripts/check.py` | CMP-007 9; CMP-008 4 (246, 298, 358, 363); CMP-006 1 (302) | CMP-007 | near-even; majority; the gate runner CMP-007's row names. The CMP-008 rows are lane rules it runs as steps |
| 9 | `scripts/check_doc_refs.py` | CMP-006 1 (180); CMP-007 1 (038) | CMP-007 | near-even. A lint a gate run consumes; flagged as two components' work |
| 10 | `scripts/check_trajectory.py` | CMP-006 9; CMP-008 1 (299) | CMP-006 | majority |
| 11 | `scripts/coordinator_adjudicate.py` | CMP-008 3; CMP-009 1 (321) | CMP-008 | majority |
| 12 | `scripts/coordinator_guard.py` | CMP-008 3; CMP-009 1 (322) | CMP-008 | majority |
| 13 | `scripts/dev-setup.ps1` | CMP-009 3; CMP-008 1 (336) | CMP-009 | majority; outside the header scope |
| 14 | `scripts/dev-setup.sh` | CMP-009 2; CMP-008 1 (336) | CMP-009 | majority; outside the header scope |
| 15 | `scripts/dev-setup.template.ps1` | CMP-009 4; CMP-008 1 (336) | CMP-009 | majority |
| 16 | `scripts/dev-setup.template.sh` | CMP-009 5; CMP-008 1 (336) | CMP-009 | majority |
| 17 | `scripts/gen_arch_map.py` | CMP-006 6; CMP-009 1 (080) | CMP-006 | majority |
| 18 | `scripts/gen_open_items.py` | CMP-009 2 (118, 370); CMP-006 1 (271); CMP-008 1 (283) | CMP-009 | near-even; plurality; it generates the operator's decision surface, one of the generated views CMP-009 holds |
| 19 | `scripts/gen_release_checklist.py` | CMP-009 2; CMP-008 1 (255) | CMP-009 | majority |
| 20 | `scripts/hats.py` | CMP-008 2 (168, 360); CMP-006 1 (251) | CMP-008 | majority; its readers are the planning briefs |
| 21 | `scripts/held_status.py` | CMP-006 1 (249); CMP-008 1 (246) | CMP-006 | near-even. Split out of `acceptance_record.py` to keep that module under its size ratchet and reads its two-tree walk, so it goes with it |
| 22 | `scripts/id_carrier.py` | CMP-006 1 (362); CMP-008 1 (363) | CMP-006 | near-even. LLR-362 states the module's job, the one carrier spine ids are reserved from; its importers are `trace` and `retire` (CMP-006). LLR-363 is the landing's use of it |
| 23 | `scripts/intake.py` | CMP-008 10; CMP-006 1 (245) | CMP-008 | majority |
| 24 | `scripts/integrate.py` | CMP-008 17; CMP-006 1 (302) | CMP-008 | majority |
| 25 | `scripts/kitlib/authority.py` | CMP-006 1 (249); CMP-008 1 (246) | CMP-006 | near-even. Reuse: the one comparison of a status rung against the acceptance dial, read by `check_trajectory` and `held_status` (CMP-006), `check` (CMP-007), and `agent_policy`, `agent_common`, `integrate` and `adjudicate_act` (CMP-008) through IF-195, whose `component` cell already reads CMP-006 |
| 26 | `scripts/kitlib/bootstrap_manifest.py` | CMP-009 2; CMP-006 1 (218) | CMP-009 | majority |
| 27 | `scripts/kitlib/config.py` | CMP-007 4; CMP-006 3; CMP-008 2 | CMP-006 | kernel rule (against the plurality) |
| 28 | `scripts/kitlib/git.py` | CMP-008 7; CMP-006 2; CMP-007 1 | CMP-006 | kernel rule (against the majority) |
| 29 | `scripts/kitlib/registry.py` | CMP-006 4; CMP-008 3 | CMP-006 | kernel rule; also the plurality |
| 30 | `scripts/kitlib/spine.py` | CMP-006 18; CMP-008 3; CMP-009 1 | CMP-006 | kernel rule; majority |
| 31 | `scripts/kitlib/verdict.py` | CMP-008 7; CMP-006 1 (278) | CMP-008 | majority; off the kernel surface, as CMP-006's row records |
| 32 | `scripts/pending.py` | CMP-009 3; CMP-008 1 (283) | CMP-009 | majority |
| 33 | `scripts/text_then_act.py` | CMP-008 4; CMP-006 1 (302) | CMP-008 | majority |
| 34 | `scripts/trace.py` | CMP-006 25; CMP-008 1 (363) | CMP-006 | majority |

Paths are relative to `project-trajectory/`, except rows 13 and 14, which
are the repository's own `scripts/`.

## The crossings the picks make

Every import edge between two of the picked files was a multi-membership
advisory or an internal edge before. Under the picks, three edges cross a
component boundary with no covering interface row, and the lane covers
each (plan, "No new silence"):

| Edge | Cover |
|---|---|
| `acceptance_record` (CMP-006) -> `kitlib/done_when` (CMP-008): the digest width `_DIGEST_CHARS` | new `Drafted` call row IF-326 |
| `agent_policy` (CMP-008) -> `kitlib/authority` (CMP-006): the rung tables, `rung_for`, `dial_from_config`, `dial_at`, `holds_under` | `agent_policy` added to IF-195's requestors (a `Drafted` row whose `data` already names those symbols) |
| `id_carrier` (CMP-006) -> `kitlib/provenance` (CMP-008): `with_loop_trailer` | `id_carrier` added to IF-194's requestors (a `Drafted` row whose `data` already names it) |

`census` picked CMP-006 would add two more (`adjudicate_brief` -> `census`,
`census` -> `agent_common`); `kitlib/authority` picked CMP-008 would move
`agent_policy`'s crossing to `held_status` -> `kitlib/authority`;
`acceptance_record` picked CMP-008 would remove the first row. Measured with
the lane's simulation of the rule over the live import graph at
`1aa6c439a`.

## In-scope files no LLR names (the lane's picks)

Not part of the 34, but each owes a header and has no tag to read, so the
lane picks one. The operator may rule these too.

| File | Pick | Reason |
|---|---|---|
| `scripts/agent-resume.template.{cmd,command,sh}` | CMP-009 | launchers a person runs; the LLR naming this repository's `agent-resume.sh` tags CMP-009 |
| `scripts/onboard.template.{cmd,command}` | CMP-009 | siblings of `onboard.template.sh` (CMP-009) |
| `scripts/setup.{ps1,sh}` | CMP-009 | a person's one-shot setup; CMP-009 holds the onboarding templates |
| `scripts/check.{ps1,sh}` | CMP-007 | thin launchers for `check.py` |
| `scripts/gen_arch_map.reference.ps1` | CMP-006 | a PowerShell port of `gen_arch_map.py`, the same job in another language |
| `hooks/pre-push` | CMP-007 | CMP-007's row names it; IF-135 carries CMP-007 |
| `docs/requirements/interfaces.toml` | CMP-006 | a registry: CMP-006 holds the registries (their templates' design rows tag CMP-006); IF-057 carries CMP-006 |
| `docs/requirements/open-items.toml` | CMP-006 | a registry, as above |
| `docs/requirements/performance-budgets.csv` | CMP-006 | a registry, as above |
| `docs/process.toml` | CMP-008 | configuration: its readers (IF-037, IF-038) are mostly CMP-008's (`agent_common`, `agent_loop`, `dispatch`), and it declares the loop's policies |
| `docs/agents.toml` | CMP-008 | configuration read by `agent_route` |
| `docs/agents-enabled` | CMP-008 | configuration read by `agent_route` and `dispatch` |
| `docs/stack.ini` | CMP-007 | configuration: its readers split three ways (IF-022 `check`, IF-049 `run_menu`, IF-068 `agent_loop`); `check.py` loads and validates the profile (LLR-007, LLR-008) |
| `docs/coverage-floors` | CMP-007 | configuration read by `check_coverage` |
| `docs/declared-absences` | CMP-007 | configuration read by `check_doc_refs` and `trace` (IF-072); its stated job is the scaffold-omission check the gate runs |
| `docs/status.md` | CMP-008 | the working surface the loop resumes from; most of its readers (IF-163) are CMP-008's |
| `docs/runtime-flows.md` | CMP-009 | an authored view; two of its three readers (IF-029: `gen_okf`, `traj_parse`) are CMP-009's |

## Every other in-scope file

Each is tagged to one component only, and takes it. Paths are relative to
`project-trajectory/scripts/`.

**CMP-006** (26): `absolute_terms.py`, `arch_components.py`,
`arch_inputs.py`, `arch_interfaces.py`, `arch_seams.py`, `arch_tags.py`,
`baseline_snapshot.py`, `coherence.py`, `derive_stage.py`,
`frame_rules.py`, `kitlib/__init__.py`, `kitlib/evidence.py`,
`kitlib/ladder.py`, `kitlib/observation.py`, `kitlib/secret_classes.py`,
`kitlib/stage.py`, `migrate_carrier.py`, `migrate_vocabulary.py`,
`plan_coverage.py`, `record_observation.py`, `retire.py`,
`spine_carrier.py`, `spine_rules.py`, `trace_text.py`, `trajectory_arch.py`,
`wi_convert.py`.

**CMP-007** (18): `check_assumption_gate.py`, `check_complexity.py`,
`check_coverage.py`, `check_docs.py`, `check_dupes_census.py`,
`check_figures.py`, `check_flows.py`, `check_need_form.py`,
`check_perf.py`, `check_privacy.py`, `check_readability.py`,
`check_stubs.py`, `check_test_first.py`, `check_vendored.py`,
`check_vocab.py`, `flag_axis.py`, `record_test_evidence.py`,
`subagent_gate.py`.

**CMP-008** (45): `adjudicate_act.py`, `adoption_record.py`,
`agent_brief.py`, `agent_common.py`, `agent_loop.py`, `agent_policy.py`,
`agent_route.py`, `agent_session.py`, `bookkeeping.py`, `consolidate.py`,
`dispatch.py`, `handback.py`, `kitlib/adoption.py`,
`kitlib/commit_hooks.py`, `kitlib/decisions.py`, `kitlib/dispute.py`,
`kitlib/done_when.py`, `kitlib/expected_failure.py`, `kitlib/plan_pass.py`,
`kitlib/provenance.py`, `kitlib/shell_line.py`, `kitlib/sitting.py`,
`kitlib/station.py`, `kitlib/winjob.py`, `lane.py`,
`migrate_decisions.py`, `observation_cadence.py`, `plan_artifacts.py`,
`plan_briefs.py`, `plan_coverage_step.py`, `plan_gate.py`, `plan_round.py`,
`plan_runner.py`, `prompts.py`, `rejudge.py`, `review_brief.py`,
`review_set.py`, `schedule.py`, `score_reviews.py`, `session_adapters.py`,
`session_keep.py`, `session_service.py`, `spec_move.py`, `trunk_step.py`,
`usage_ingest.py`.

**CMP-009** (24): `dev-setup.template.cmd`, `dev-setup.template.command`,
`gen_cases.py`, `gen_components.py`, `gen_okf.py`, `gen_prompt_catalog.py`,
`gen_skills_index.py`, `gen_trajectory.py`, `gen_verdict_rollup.py`,
`kitlib/guard_hooks.py`, `onboard.template.sh`, `rendering/__init__.py`,
`rendering/traj_context.py`, `rendering/traj_graph.py`,
`rendering/traj_panels.py`, `rendering/traj_render.py`,
`rendering/traj_views.py`, `run.template.cmd`, `run.template.command`,
`run.template.sh`, `run_menu.py`, `traj_display.py`, `traj_parse.py`,
`traj_status.py`.

167 files in all: 136 Python modules and 18 other files under `[paths] src`
(`README.md` excluded), and 13 file owners outside it.
<!-- fig: derived="the counts are the lane's census of [paths] src and arch_interfaces._owner_files at 1aa6c439a, recorded in the plan" -->
