Reviewed: cbf029136e053cb9144e00ad79943f4c232b4f41

Verified. `git rev-parse HEAD` in the lane printed cbf029136e053cb9144e00ad79943f4c232b4f41. I read the spec (docs/work/active/wi-912/WI-912-verdict-act-split.md) and the full diff in scope. I ran the real derivation (`adjudicate_act.owed_acts` / `left_owed` / `act_values`) and the real snapshot writer (`baseline_snapshot.copy_live`) over git fixtures I built in my scratch folder. These are right:
- The judging briefs (first-approval, amendment, combined, and the composer's released and held-reattest arms) no longer order a flip, a snapshot or a re-attestation, and each points to the later act turn.
- `adjudicate_act` reads the verdict and its binding only through `kitlib.sitting.accepted_at` at a revision, never from the working tree. It refuses absent, unbound, pending, failed, malformed and non-actable verdicts, and judged rows in an inconsistent state, all or nothing.
- APPROVE acts are skipped on held rungs. CLARITY acts carry `--verdict` when a held row is listed. MEANING is re-attested only with `[MEANING+BLESS]` on a released rung. The `[MEANING+BLESS]` tag cannot prefix-match `[MEANING]`.
- Combined acts are ordered amendment first. A whole-registry copy holding a Drafted row reads as owed, and a flip committed without its copy is refused as inconsistent.
- `coordinator_adjudicate.py act`:
  - checks lane, route and clean tree (untracked files included) before it composes anything;
  - reserves no verdict path and writes no binding;
  - plans its keep by the bound class;
  - appends `loop_provenance_note()` to every launched prompt through one `_launched`;
  - exits 0 only when the call succeeded, `left_owed` is None, and nothing changed under docs/reviews/, committed or not.
- The act brief joins the retained identity of the actable classes (`_add_act_template`).
- Skill copies (.claude/.agents) are byte-identical to the kit source. PROCESS_OPTIONS.md grew from 199,296 to 199,426 bytes (+130), as stamped.
- The RESYNC entry is anchored `[since ace24c85c]` and states the loop gap. Implements tags match LLR-338, LLR-306, LLR-305 and LLR-310's module and code_symbol (K3).
- SR-231's amendment names no carrier (K2).

Done-when mapping:
- "no judging brief orders an act" -> test_adjudicate_brief.py::test_no_judging_brief_orders_an_act.
- The WI-572 pin is removed; its successor is test_coordinator_act.py::test_the_act_turn_reports_success_only_when_no_listed_act_is_left.
- Each Trust input refusal -> test_the_act_command_refuses_each_trust_input_before_launch and test_each_unaccepted_or_unreadable_verdict_is_refused_naming_why.
- Retained and fresh turns taking the same act -> test_a_retained_and_a_fresh_act_turn_take_the_same_act_from_one_verdict.
- Combined order -> test_a_combined_act_commits_its_amendment_act_before_its_first_approval_act, plus the assembler twin.
- Mixed `--approves` -> test_a_mixed_first_approval_verdict_approves_only_its_approved_rows_registries.
- Unmarked MEANING -> test_a_MEANING_row_without_the_bless_mark_is_left_unacted.
- Stops short, or writes under reviews -> test_the_act_turn_reports_success_only_when_no_listed_act_is_left and test_an_act_turn_that_writes_under_docs_reviews_does_not_succeed.
- Interrupted between flip and snapshot -> test_an_act_interrupted_between_flip_and_snapshot_is_refused_dirty_then_rerun_in_full.
- Interrupted combined act -> test_a_combined_act_interrupted_between_commits_reruns_with_only_its_first_approval_act.
- Flip without its copy -> test_a_flip_committed_without_its_copy_is_refused_naming_the_row.
- Drafted row in a whole-registry copy -> test_a_Drafted_row_present_unchanged_in_a_whole_registry_copy_is_owed.
- Loop marker, with and without -> test_under_the_loop_marker_every_launched_prompt_ends_with_the_loop_session_line and test_without_the_marker_no_prompt_carries_the_line, parametrized over every brief class plus act.
- Catalogue check -> test_the_catalogue_on_disk_is_FRESH (passes).

Every new test targets a module, command or tag that does not exist at ace24c85c, so each one fails on the pre-change code; the old ROW_RULINGS had no `[MEANING+BLESS]` tag. The checkpoint-sitting and landing-bar items are process facts at landing, outside this diff. Per the brief I read no decision record, so I did not verify them.

Commands:
- `git rev-parse HEAD` -> cbf029136e053cb9144e00ad79943f4c232b4f41
- `python lowprio.py python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r1/opus/wi-912 tests/test_adjudicate_act.py tests/test_coordinator_act.py tests/test_adjudicate_brief.py tests/test_coordinator_adjudicate.py tests/test_routing_and_prompts.py tests/test_done_when_blessing.py tests/test_assumption_observation_briefs.py tests/test_prompts.py` -> `387 passed in 280.00s (0:04:40)` (0 env-gated skips)
- `python lowprio.py python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (936 work item(s), 817 done (87%), 30 cancelled, graph acyclic).` (exit 0)
- `python lowprio.py python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=304 TC=318 orphans=0 integrity=0 ... interface-findings=0 ...` (exit 0; worktree left clean)
- probe .../r1/opus/probe/probe_retired.py:
  - case 1, the verdict rules a deleted TC-001 CLARITY: `owed_acts` -> `(None, '... judged a row TC-001 is inconsistent: its committed status is absent and its recorded copy does not equal it')`. The pre-change route, `copy_live(reattests={LLR-001, TC-001})`, gives OK.
  - case 2, the verdict omits TC-001: the act lists only LLR-001.
- probe .../r1/opus/probe/probe_retired2.py: TC-001 is deleted and TC-002 is drafted and ruled APPROVE. The act lists TC-002, and its own `--approves` snapshot gives `REFUSED ... docs/test/test-cases.toml TC-001: removed from the live registry`.
- probe .../r1/opus/probe/probe_bless.py: the verdict has `[MEANING] SR-001` and `[CLARITY] LLR-001`, and the act re-attests both. `left_owed` -> None, so `act` would exit 0. The merge floor's `judged_rows` -> `[('amendment','LLR-001'), ('amendment','SR-001')]`.

Findings:

- [MAJOR] project-trajectory/scripts/adjudicate_act.py:237 -> When a lane retires (deletes) an approved row, the act turn has no way to take its act. The retired row is still in the anchored copy, so the snapshot reads it as REMOVED drift, which "is cleared only by naming it in `--reattests`" (baseline_snapshot.copy_live's gate). The coordinator-cycle skill says to "Carry retired rows into scope explicitly" (project-trajectory/skills/coordinator-cycle/SKILL.md:288), and the pre-change recipe named retired rows in `--reattests`. Now `_state` reads a ruled row that is absent at HEAD as inconsistent and refuses the whole derivation (exit 2), and recipes.md:427 writes that refusal down as the rule. If the verdict leaves the row out, every later copy of that registry is refused, including this act's own first approval in the same registry (probe_retired2). Both branches block a supported workflow (retire.py plus its successor row) from landing through the only sanctioned act route. The pre-change judging session completed it (probe_retired case 1, old route). -> Extend the S3 "Re-runs" partition and `_state`: a re-attest of a ruled row absent at HEAD whose recorded copy still holds it is owed (a retirement), and taken once the copy no longer holds it. Render it in `--reattests`, add the matching spec/LLR-338/TC-368 wording, and add a test that retires an approved row under a CLARITY verdict and lands the act (with a sibling first approval in the same registry). This widens the partition rather than adding a guard, so no unrepresentable clause is owed -> @owner

- [MINOR] project-trajectory/scripts/coordinator_adjudicate.py:445 -> The bless mark (Q2) is honored only by the act session's obedience. `_act_report` asks only whether the listed acts are taken (`left_owed`), not whether the call took anything else. The merge floor's `kitlib.sitting.judged_rows` (`_AUTHORIZING["amendment"] = ("MEANING", "CLARITY")`) admits a re-attestation of an unblessed `[MEANING]` row. So an act turn that widens `--reattests` to that row reports `act: complete`, and the merge admits it (probe_bless), which re-anchors text the verdict refused to bless. Only an act session that disobeys its brief reaches this, hence MINOR. -> Make the single owning boundary read the mark: have the merge floor's `judged_rows` authorize an amendment re-attestation only for CLARITY or for a `blessed_rows` MEANING row, which makes an act-turn post-check unnecessary. If that is out of this lane's scope, `_act_report` can instead compare the rows acted between `before` and HEAD (the approval delta's acted set) with `_authorized` and fail on any extra. That would be a compensating check, because the boundary that should own the mark (the merge floor) does not read it -> @owner

- [MINOR] docs/test/test-cases.toml:3555 -> TC-368's Expected and LLR-338's Detail (docs/requirements/low-level-requirements.toml:3466) both claim that "an approval without an approval record refuses" and that "an unmatched tier refuses ... naming the row". No test in the evidence list reaches either branch: every fixture seeds the record (`copy_live(seed=True)`), and the inconsistent-row case uses LLR-404, which has a tier. So adjudicate_act.py:289-293 (`_recorded`) and :233-234 (`_tier` None) are unpinned, and so is the `_verdict_rel` outside-root refusal (:264-265). A deleted branch would stay green. -> Add three cases to tests/test_adjudicate_act.py (an unseeded repo with an APPROVE owed, a ruled row id with no compared tier's prefix, and an absolute verdict path outside the root) and add them to TC-368's evidence -> @owner

- [MINOR] docs/requirements/system-requirements.toml:1724 -> For clarity (K1). SR-231's amended requirement still opens with "read success only from a verdict that its own call wrote within that call's deadline". That sentence applies to the whole entry point, but the act command reads success from the acts at the lane head, and its call writes no verdict. Read literally, the new second sentence contradicts the first. The rationale also still argues only the fresh-verdict obligation, nothing about the act. -> Scope the first sentence to the judging turn (for example "...read a judgement's success only from a verdict that its own call wrote...") and add one rationale sentence on why the act is authorized only by an accepted committed verdict -> @owner

Coverage-extension note (no severity): the act derivation does not filter APPROVE rows by the sitting's `Adjudicates` scope. An out-of-scope APPROVE line would be listed, then refused at the merge by `reattest_scope_refusal` / `first_approval_scope`, so the change fails closed on it.

VERDICT: CHANGES-REQUESTED findings=4
