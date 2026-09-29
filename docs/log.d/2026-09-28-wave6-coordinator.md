## 2026-09-28 — The sixth coordinator session: owner rulings, WI-721 and WI-720, Sol builders under Sonnet review

Resumed from [the wave-5 handoff](../handoff-2026-09-28-wave5-coordinator.md).
The owner first ruled OI-95 to OI-97
([2026-09-28-owner-rulings-oi95-oi96.md](2026-09-28-owner-rulings-oi95-oi96.md),
[2026-09-28-owner-ruling-oi97.md](2026-09-28-owner-ruling-oi97.md)). Reviews
for this session are in [../reviews/2026-09-28-wave6/](../reviews/2026-09-28-wave6/).

### The builder launch, tested

The handoff's roles make Codex Sol the builder, launched through `codex
exec`. The first launch was refused by the coordinator's permission
classifier ("Create Unsafe Agents"). The owner allowed a temporary
`Bash(codex exec *)` rule in `.claude/settings.local.json`, to be removed
when the queue drains, and the launch then ran.

Both builders built and tested in their worktrees, but neither could
commit. Codex's `workspace-write` sandbox keeps `.git` read-only, and
`--add-dir` naming the primary `.git` did not change that (`Permission
denied` on `.git/worktrees/wi-NNN/index.lock`). The coordinator commits
each builder's change on its lane branch, and the commit says so. The
sandbox was not widened.

The `sonnet` alias resolves to Sonnet 5 here, the newest Sonnet available,
not the 5.5 the handoff names.

### WI-720 lands: SR-222's and SR-227's chains restated as standing prose

- **Build:** one Sol build, committed as 9a7c063d.
- **Review:** one Sonnet round, SOUND
  ([sonnet-wi720.md](../reviews/2026-09-28-wave6/sonnet-wi720.md)). Its one
  minor finding (SR-227's rationale also lost the cache comparison) is
  accepted as still true.
- **What landed:** thirteen registry cells on nine Drafted rows, the IF-245
  docstring sentence, and TC-268's evidence pinned to the skip line.
- **Next:** the sweep mints the rows' first approval.
- **Trunk before this squash:** 4dd6827d.
- **Bar:** smoke `1890 passed, 3 skipped`. Its seconds read 64.7 s and
  65.4 s, over the 60 s budget. A control at the parent commit 4dd6827d,
  in a throwaway worktree, read 91.1 s, so the box was loaded (desktop
  apps, a game) and this cells-only lane is not a regression; the budget is
  not re-stamped. check_trajectory --strict, trace --strict-integrity,
  gen_open_items, gen_trajectory, derive_stage and check_docs are clean.

### WI-725 lands: the spot check of WI-720's close, CONFIRMED

An independent Opus spot-checker judged WI-720's close at bbe00d8a:
CONFIRMED
([record](../reviews/wi-725-spot-check-the-clean-close-of/001-SPOTCHECK-bbe00d8a.md)).

- **Folded into WI-724's Context:** three observations on the rows WI-724
  adjudicates, plus a docstring note. These are LLR-266's remaining history
  phrases and a false "already carried" claim, TC-264's Method overclaiming
  the pinned revision, and SR-222's "where the runner reports one".
- **Corrected:** the cell count in WI-720's Deliverable and above.
- **Not filed:** no new row.
- **Bar:** smoke `1890 passed, 3 skipped`. Its seconds read 329.0 s, with
  WI-723's builder and a Sonnet confirmation running tests beside it. That
  is contention, not this documentation-only lane. The spine and doc checks
  are clean.

### WI-723 lands: the joint-delivery class (OI-97 (a))

- **Build and review:** one Sol build and one Sol fix round, with two
  Sonnet rounds.
  - [Round 1](../reviews/2026-09-28-wave6/sonnet-wi723-r1.md): NOT YET
    SOUND. SR-024's sibling was not argued from its rationale.
    `assumption_rules.py` had reached exactly 1000 SLOC by cutting the
    explanations out of its advisory text, and it computed undeclared ids
    in two places.
  - [Round 2](../reviews/2026-09-28-wave6/sonnet-wi723-r2.md): SOUND at
    35444157. The builder accepted every finding, so no arbitration.
- **What landed:** `delivered_with` and the joint class, with SR-193's chain
  amended in place.
  - Seven rows are joint: SR-015, SR-033, SR-111, SR-174, SR-177, SR-223 and
    SR-225.
  - SR-024 and SR-129 stay unclassified, because no rationale sentence
    carries a sibling.
  - The ratchet is re-stamped at 1028 with its reason.
- **Owed:** the amendments and the nine rows' re-opened attestations go to
  the next spine-acts batch.
- **Trunk before this squash:** e86cae4f.
- **Bar:** smoke `1898 passed, 3 skipped` (eight new tests). Its seconds
  read 136.5 s against 60 s, with WI-721's full unfiltered suite running
  `-n auto` on the same box, so this is contention and not re-stamped.
  check_trajectory --strict, trace --strict-integrity, gen_open_items,
  gen_trajectory, derive_stage, check_docs, and the live approval brief
  (`trace.py --approve modified`) are current.

### WI-721 lands: the slow-tier reds cleared, and the full unfiltered suite green

- **Build and review:** one Sol build and one Sol fix round, with two
  Sonnet rounds.
  - [Round 1](../reviews/2026-09-28-wave6/sonnet-wi721-r1.md): SOUND, with
    one major. Approved LLR-286 still said "TOML registry", narrower than
    the fixed reader.
  - The fix round amended that one cell in place under the coordinator's
    grant, listed the new test in TC-299's evidence, and aligned IF-102's
    docstring.
  - [Round 2](../reviews/2026-09-28-wave6/sonnet-wi721-r2.md): SOUND at
    d7c43118.
- **What landed:** `retire.live_ids` reads through `spine_carrier`, so the
  three trace goldens pass with no golden regenerated. The skills-index test
  pins STALE again.
- **The full unfiltered suite:** `4816 passed, 15 skipped, 18 warnings in
  4998.50s (1:23:18)`, run with `--durations=30`.
  - It ran on e86cae4f plus this lane, in a throwaway worktree, with the
    WI-723 builder and reviewers sharing the box.
  - The durations are pasted in WI-721's Deliverable.
  - Two tests dominate the critical path:
    `test_traj_graph.py::test_meta_knowledge_and_when_wires_avoid_unrelated_boxes`
    at 1160.6 s, and its fallback-graph sibling at 392.7 s.
  - Both route over graphs built from the live registries, and the router
    has not changed since 2026-09-06. So the jump from about 10 minutes
    follows the spine's growth.
  - Alone, on a mostly quiet box, the first takes **790.5 s** of call time
    (`1 passed in 965.37s`). No parallelism can finish the suite faster.
  - Filed as **WI-727**: profile the router, fix the cost or bound the test
    at a real scale, and re-measure.
- **Owed:** LLR-286's amendment goes to the next spine-acts batch.
- **Trunk before this squash:** 5124c932. The full-suite run did not
  include WI-723, which landed first; the next phase-close run covers both.
- **Bar:** smoke `1898 passed, 3 skipped`, 54.6 s against 60 s, within
  budget on a quiet box. check_trajectory --strict, trace
  --strict-integrity, gen_open_items, gen_trajectory, derive_stage,
  check_docs and the live approval brief are current.

### Spine-acts batch G (WI-724, WI-726, WI-728): eight SRs re-attested, nine rows returned, the LLR and TC anchoring held

- **The sitting:** one independent Opus adjudicator, which directed none of
  the amendments, sat once over three kit-composed briefs and took one act
  (seq 9). Every routed pointer cell was ruled. A flip showed no
  requirement-form finding.
- **Re-attested and anchored:** SR-015, SR-033, SR-111, SR-174, SR-177,
  SR-193, SR-223 and SR-225. These are the seven `delivered_with` rows and
  SR-193, each judged against OI-97.
- **Returned:**
  - SR-222 ("where the runner reports one");
  - SR-227 (its shall has no mint case or held-session case);
  - LLR-266 (history, and a false "already carried");
  - LLR-268 (the provider name's source is decomposed nowhere);
  - TC-264 (the revision is asserted for claude only);
  - LLR-223 and TC-220. `assumption_rules._classify` classifies a row whose
    only sibling shares no need as `joint`, contrary to SR-193. That is a
    defect WI-723 landed and its two review rounds missed.
- **Held:** LLR-267, LLR-269, LLR-270 and TC-262 are approved in the verdict
  but still Drafted. LLR-222, TC-222 and LLR-286 are blessed but not
  anchored. The snapshot refuses the LLR and TC registries while the returned
  LLR-223 and TC-220 drift, which is the brief's own stop case. Both the
  adjudicator and the cross-review confirmed it with
  `baseline_snapshot.refresh_refusal`.
- **Follow-up:** one consolidated Dispositions draft in WI-724. The sweep at
  this merge mints it, carrying the owed first approvals and
  re-attestations.
- **Cross-review:** Sonnet found the act SOUND, with one minor
  ([sonnet-batch-g.md](../reviews/2026-09-28-wave6/sonnet-batch-g.md)). It
  reproduced every return against the code.
- **Trunk before this squash:** f1733daa.
- **Bar:** smoke `1898 passed, 3 skipped`. Its seconds read 63.0 s
  against 60 s, with WI-545's builder and a Sonnet review running tests
  beside it. That is contention on a lane that changes only records, and
  the budget is not re-stamped. check_trajectory --strict, trace
  --strict-integrity, gen_open_items, gen_trajectory, derive_stage,
  check_docs and the live approval brief are current.

### WI-729 lands: batch G's returns answered

- **Build and review:** one Sol build, and one Sonnet round, SOUND with no
  findings ([sonnet-wi729.md](../reviews/2026-09-28-wave6/sonnet-wi729.md)).
- **What landed:** eleven items across SR-222, SR-227, LLR-266, LLR-268,
  TC-264, LLR-223 and TC-220, plus the three optional rationale and title
  items. Among them is the classifier fix: joint needs a sibling that shares
  a need.
- **Next:** the sweep mints the adjudication. The coordinator adds the
  batch-G carry-over to it: first approvals LLR-267, LLR-269, LLR-270 and
  TC-262, and re-attestations LLR-222, TC-222 and LLR-286.
- **Trunk before this squash:** a20b496a.
- **Bar:** smoke `1899 passed, 3 skipped`, 49.2 s against 60 s, within
  budget. check_trajectory --strict, trace --strict-integrity,
  gen_open_items, gen_trajectory, derive_stage, check_docs and the live
  approval brief are current.

### WI-727 lands: the router's hit test pre-filters by bounds, and the slowest test drops from 980 s to about 40 s

- **Build and review:** one Sol build and one fix round, with two Sonnet
  rounds.
  - Round 1 found the pre-check unsound in floating point, by fuzzing: a
    rectangle touching a wire's box could be skipped one ULP past it. The
    output was byte-identical on today's data, so the defect was latent.
  - The fix round added a documented half-grid margin, the counterexample,
    and a seeded oracle test.
  - Round 2: SOUND at 427fbaf4, with a 520,000-case fuzz clean and
    independent byte-identical renders.
- **Accepted minors:** the margin is empirical, and one boundary test is not
  a float guard.
- **Owed:** the slowest-30 re-measure, taken at the phase-close full run.
- **Trunk before this squash:** 3e8a87d2.
- **Bar:** smoke `1899 passed, 3 skipped`, unchanged, because
  `test_traj_graph` is in the slow tier. Its seconds read 77.4 s against
  60 s, with WI-545's fix builder and the batch-H adjudicator running tests
  beside it. That is contention, not this lane, and the budget is not
  re-stamped. The spine and doc checks are clean.

### Spine-acts batch H (WI-730, WI-731): TC-262 approved, TC-220 and TC-222 re-attested; the SR and LLR anchoring held again

- **The sitting:** one fresh independent Opus adjudicator, one act (seq 10).
  It judged the batch-G carry-over afresh.
- **Anchored:**
  - TC-262 is approved;
  - TC-220 and TC-222 are re-attested.
- **Approved but not flipped:** LLR-267, LLR-269 and LLR-270.
- **Blessed but not anchored:** SR-193, LLR-222 and LLR-286.
- **Not blessed:**
  - SR-177: WI-729's optional rationale rewrite states an obligation wider
    than its acceptance;
  - LLR-223: its contradiction sentence is wider than SR-193, TC-220 and the
    code.

  Each holds a whole registry.
- **Returned:**
  - SR-222, LLR-268 and TC-264: a codex routed to a third-party provider is
    recorded as `openai`;
  - SR-227: its "declared bound" is a code default, and its reason goes only
    to stderr;
  - LLR-266: its absolute over adopter templates.
- **Follow-up:** one consolidated draft in WI-731. The sweep mints it.
- **Cross-review:** Sonnet found the act SOUND, with no findings, and
  reproduced every return
  ([sonnet-batch-h.md](../reviews/2026-09-28-wave6/sonnet-batch-h.md)).
- **A pattern, noted for the owner:**
  - This is the second sitting in a row where one unblessed row held back a
    whole registry's anchoring. Both blockers are single clauses in cells
    the previous lane rewrote, and one came from an optional item.
  - For the lanes that answer returns, the coordinator now asks the builder
    to answer the blocking rows first and to take no optional item that
    touches an approved cell.
- **Trunk before this squash:** b689eada.
- **Bar:** smoke `1899 passed, 3 skipped`. Its seconds read 85.3 s against
  60 s, with a Sonnet confirmation running the agent-loop test modules
  beside it. That is contention on a lane that changes only records, and the
  budget is not re-stamped. The spine and doc checks and the live approval
  brief are current.

### WI-732 lands: batch H's returns answered; the first arbitration of the new roles

- **Build and review:** one Sol build and one Sonnet round, NOT YET SOUND
  on one major.
  - The review held that the new DA-016 and DA-017 belong at B-10, the
    model-runner crossing. The builder had chosen B-09.
  - An independent Opus arbiter ruled for the builder
    ([ARBITRATION.md](../reviews/2026-09-28-wave6/ARBITRATION.md),
    ruling 1). An outcome lands at the stakeholder's crossing (SR-195), and
    the kit's reach check penalises B-10 here.
  - With the only finding overruled, the lane lands as built.
- **What landed:** SR-177's and LLR-223's blocking cells now say exactly
  what their rows hold, which the review probed. Also:
  - SR-222 and LLR-268: the runner's default provider, reconfiguration not
    detected;
  - SR-227: a bounded wait, stating why;
  - LLR-266: its absolute dropped;
  - SR-222 and SR-227 bridged through DA-016 and DA-017.
- **Kit gap recorded, not filed** (from the arbitration): SR-195 and
  SR-212's Boundary arm collide for any future `form = "interface"` SR at a
  crossing with no stakeholder party (B-10, B-11). It is latent, since no
  SR declares a Form, and belongs to the assumption tier's C3/C4 design.
- **Owed:** the adjudication this merge mints also takes the carry-over.
- **Trunk before this squash:** 69902bc9.
- **Bar:** smoke `1900 passed, 3 skipped` (one new test). Its seconds read
  116.4 s against 60 s, with the full unfiltered suite (`-n auto`) and a
  Sonnet confirmation running beside it. That is contention, and the budget
  is not re-stamped. The spine and doc checks and the live approval brief
  are current.

### WI-735 lands: the spot check of WI-732's close, CONFIRMED

An independent Opus spot-checker found every item met
([record](../reviews/wi-735-spot-check-the-clean-close-of/001-SPOTCHECK-03debc71.md)).

- **Its four observations** fall on cells under batch I's adjudication:
  - SR-222's acceptance wording;
  - the provider pairs appearing at the SR tier;
  - LLR-223's silence on failed rows;
  - SR-177's "stated build gap" acceptance clause.

  They were sent to the sitting adjudicator as chain evidence, rather than
  filed.
- **Not filed:** no new row.
- **Bar:** smoke `1900 passed, 3 skipped`, taking 162.8 s with the full
  unfiltered suite and the batch-I adjudicator running beside it. The
  seconds are contention on a records-only lane and not budget evidence.
  The spine and doc checks are clean.

### Spine-acts batch I (WI-733, WI-734): the LLR registry unblocked; LLR-266 to LLR-270 approved, six rows re-attested

- **The sitting:** a third independent Opus adjudicator, one act (seq 11).
  WI-735's spot-check observations reached it as chain evidence.
- **Approved and anchored:** LLR-266 to LLR-270.
- **Re-attested:**
  - SR-177 and SR-193 (CLARITY);
  - LLR-222, LLR-223, LLR-286 and TC-267 (MEANING).

  Three registries were copied. This clears the whole batch G and H
  carry-over.
- **Drafts:** down from 11 to 6.
- **Returned, with an exact narrow draft:**
  - SR-222 and TC-264: bound the usage record to the runners the loop reads;
    the shipped gemini route is not one;
  - SR-227: its `shall` must carry the keep-warm and whole-write clauses its
    acceptance obliges.
- **Recorded, not filed:** WI-735's observations 3 and 4.
- **Cross-review:** Sonnet found the act SOUND, with no findings
  ([sonnet-batch-i.md](../reviews/2026-09-28-wave6/sonnet-batch-i.md)).
- **Trunk before this squash:** 5c71129f.
- **Bar:** smoke `1900 passed, 3 skipped` (100.3 s, with the full
  unfiltered suite running beside it; a records-only lane). check_trajectory
  --strict, trace --strict-integrity (drafts=6), gen_open_items,
  gen_trajectory, derive_stage, check_docs and the live approval brief are
  current.

### The second full unfiltered suite: one red from WI-545, and WI-727's re-measure

- **The run:** trunk 69902bc9 plus build/wi-545 at 7de50658, in a
  throwaway worktree, under load from the batch-I adjudicator, the
  WI-735 spot-checker and two Sonnet reviews. The command was
  `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt python -m pytest -q
  -n auto -p no:cacheprovider --durations=30`:

```
179.35s call     tests/test_prereq_toolchain.py::test_a_gate_closed_run_announces_itself_at_both_ends
124.60s call     tests/test_dispatch.py::test_a_needs_human_worker_hands_back_and_the_run_keeps_going
103.70s call     tests/test_dispatch.py::test_the_dispatcher_mints_the_consolidation_row_for_an_overlapping_queue
85.62s call     tests/test_traj_graph.py::test_meta_knowledge_and_when_wires_avoid_unrelated_boxes
58.16s call     tests/test_traj_graph.py::test_t8_no_wire_passes_through_an_unrelated_node_box
55.53s call     tests/test_integrate_station.py::test_claim_build_and_integrate_end_to_end
53.66s call     tests/test_traj_graph.py::test_fallback_dag_and_sw_graph_wires_avoid_unrelated_boxes
53.06s call     tests/test_old_kit_resync.py::test_node_adopter_upgrade_preserves_populated_owner_content
52.66s call     tests/test_dispatch.py::test_a_red_handback_is_reverted_to_a_bar_inert_artefact_and_merges
49.10s call     tests/test_check_perf.py::test_harness_runs_perf_at_g3
48.03s call     tests/test_check_privacy.py::test_meta_repo_tree_passes_the_secrets_floor
46.56s call     tests/test_dispatch.py::test_drive_end_to_end_claims_builds_merges_and_drains
45.56s call     tests/test_integrate_unload.py::test_the_queue_exits_nonzero_when_a_merged_branch_stays_held
43.93s call     tests/test_trajectory.py::test_deep_acyclic_chain_validates_without_recursionerror
40.62s call     tests/test_verdict_record.py::test_a_record_commit_stacked_on_a_refresh_does_not_bury_the_peel
40.60s call     tests/test_integrate_unload.py::test_the_queue_gcs_a_clean_worker_worktree_end_to_end
40.04s call     tests/test_dispatch.py::test_drive_stops_on_a_red_refresh_bar
39.30s call     tests/test_traj_panels.py::test_meta_spine_renders_the_knowledge_graph_at_real_scale
38.48s call     tests/test_traj_graph.py::test_deep_chain_renders_without_recursionerror
37.09s call     tests/test_dispatch.py::test_residue_settled_at_barrier_open_is_counted_in_the_drained_banner
36.61s call     tests/test_dispatch.py::test_empty_frontier_rung_one_mints_gap_rows_then_drives_them
33.58s call     tests/test_dispatch.py::test_the_spine_batch_admits_first_and_together
33.39s call     tests/test_integrate_admission.py::test_a_lane_that_moves_a_held_status_is_refused_at_the_merge_slot
33.02s call     tests/test_trajectory.py::test_deep_cycle_reported_cleanly_not_recursionerror
31.39s call     tests/test_check_harness.py::test_smoke_tier_runs_only_smoke_and_skips_coverage_gate
30.01s call     tests/test_traj_status.py::test_core_collection_runs_without_the_rendering_package
29.79s call     tests/test_agent_loop_review.py::test_escalation_tiers_up_after_swap
29.35s call     tests/test_pre_commit_hook.py::test_hook_privacy_author_guard
28.17s call     tests/test_check_harness.py::test_unmarked_test_runs_in_full_tier
28.09s call     tests/test_bootstrap.py::test_domain_skills_require_matching_explicit_opt_in
FAILED tests/test_mapping_purpose_cli.py::test_cli_mapping_purpose_gates_when_real_shipped_row_is_removed
1 failed, 4836 passed, 15 skipped, 18 warnings in 3951.89s (1:05:51)
```

- **The one failure** is WI-545's:
  `test_mapping_purpose_cli::test_cli_mapping_purpose_gates_when_real_shipped_row_is_removed`.
  - The test rebinds `bootstrap.MAPPING`, which after the split is an
    alias of `kitlib/bootstrap_manifest.MAPPING`, so the rebinding no
    longer reaches the check.
  - This is a class both path-keyed sweeps missed: rebinding a moved symbol
    through its old module.
  - WI-545's fix round 3 fixes it and sweeps for the class.
- **The wall time** is 1:05:51 under load, against 1:23:18 at WI-721's run
  and 1:51:23 at the wave-5 close.
- **WI-727's re-measure:**
  `test_meta_knowledge_and_when_wires_avoid_unrelated_boxes` now takes
  85.6 s under full load, against 1160.6 s at WI-721's run. The critical
  path is now `test_prereq_toolchain`'s nested-pytest case at 179 s,
  which takes 10 s alone, so that is load.

### WI-736 lands: batch I's exact returns applied

- **Build and review:** one Sol build and one Sonnet round, SOUND. The
  replacements were verified verbatim by a programmatic diff.
  - One minor was accepted as recorded: the fixture's `session_id` fills
    the conversation id, a column the draft does not cover
    ([sonnet-wi736.md](../reviews/2026-09-28-wave6/sonnet-wi736.md)).
- **What landed:**
  - SR-222 bounded to claude, codex and opencode, with any other runner
    recorded empty;
  - SR-227's `shall` carrying its keep-warm and whole-write clauses;
  - TC-264 covering the gemini case.
- **Next:** the sweep mints the three rows' first approval.
- **Trunk before this squash:** a0445a80.
- **Bar:** smoke `1901 passed, 3 skipped` (one new test). Its seconds read
  72.8 s against 60 s, with WI-545's fix builder running tests beside it.
  That is contention, and the budget is not re-stamped. The spine and doc
  checks and the live approval brief are current.

### WI-738 lands: the spot check of WI-736's close, CONFIRMED

An independent Opus spot-checker verified the three replacements
programmatically, and probed the plain adapter over gemini results
([record](../reviews/wi-738-spot-check-the-clean-close-of/001-SPOTCHECK-5b75c39a.md)).

- **Its observations** went to batch J's sitting adjudicator as chain
  evidence:
  - SR-227's "one bounded turn" is true only on the claude adapter;
  - "by one writer" against the lock-free tombstone;
  - the conversation id of an unread runner;
  - `adapter_for`'s prefix match.
- **Not filed:** no new row.
- **Bar:** smoke `1901 passed, 3 skipped` (78.8 s, with an adjudicator and
  a reviewer running beside it; a records-only lane). The spine and doc
  checks are clean.

### WI-545 lands: the decomposition debt paid, by pure moves into four deep modules

- **The moves:**
  - `agent_brief`, `agent_policy` and `trajectory_arch` are extracted from
    `agent_loop`, `agent_common` and `check_trajectory`, and
    `kitlib/bootstrap_manifest` from `bootstrap`;
  - each move is AST byte-identical, with the old modules re-exporting;
  - two test monoliths are split, and four size baselines lowered.
- **Build and review:** one Sol build and three fix rounds, with four
  Sonnet rounds. Each round found something the split had silently
  narrowed or broken:
  - the complexity keys;
  - path-keyed content scans, including SR-175's egress sweep, which read
    re-export stubs;
  - a test rebinding `bootstrap.MAPPING` through the alias. The full
    unfiltered suite found this one; no reviewer's module list reached it.
- **Lesson** (the handoff's, again): a move keeps behaviour but breaks every
  consumer that addresses the code by where it used to live, whether by
  file path, module key or rebinding. Only the full suite covers all of
  them. It ran before this landing, and runs again at the phase close.
- **At the merge:** the generated `docs/id-watermark` conflicted (IF and DA
  both raised) and was regenerated with `--bump-ids`. Integrity is 0, and
  the traced-cell moves leave batch I's anchored LLR snapshot clean.
- **Trunk before this squash:** 205d02cf.
- **Bar:**
  - smoke `1902 passed, 3 skipped`, 51.2 s against 60 s, within budget;
  - check_trajectory --strict, trace --strict-integrity, gen_open_items,
    gen_trajectory, derive_stage and the live approval brief are current;
  - check_docs was 0 broken after one historical link to WI-545's old queued
    path (`docs/ai-template-redesign-2026-09-05-codex/BACKLOG-MIGRATION.md`)
    was repointed to the archive.
