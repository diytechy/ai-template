Reviewed: 4dc0f7e292f3429c966f1f2c2c67bc213074000f

**Verified.** This was a full-lane review in the convergence stance. I read no earlier verdict, decision record or lane commit message, and read pre-fix code only from the base tree and from per-hash patches.

I hunted three worst cases first: a claim or assignment that fails open, a close that loses data, and a peel that lets a close skip review. Each one is closed.

- **Claim.** `integrate.claim` runs `_claim_input_refusal` first, which calls the shared `ac.parse_wi_id`. That refusal comes before the hooks rung, the coordinator guard, the dispatch lock and any move, commit, branch or worktree.
- **Worker.** `agent_loop --wi` is read by presence (`is_drive_launch`, `preflight`). So `--wi ""` refuses by name instead of starting a drive launch that claims.
- **Resume.** A parked branch whose trunk claim holds two or more specs stops the run before `_pre_admit`. `_stop_run` freezes admission while lanes are live, and the run loop honours `state["fatal"]`.
- **Closes.** `_the_one_claimed_spec` refuses a claim of zero specs, or of two or more, before `_lane`, before any report and before any residue commit.
- **Peel.** `_closed_wi_ids` accepts exactly one deletion. `mechanical_close_subject` and `claim_subject` take a `str` only. The history readers (`claim_base`, `loop_claimed`, `provenance.loop_writer_commit`) still read the joined historical subject.

I ran the real shipped code on the pre-fix code. I took a `git archive` of 41dfbb17e and overlaid the lane's new test files on it. Every refusal test fails there, for the right reason:

- the empty claim and the multi-item claim each assert `0 == 1`: the claim committed;
- the parked two-spec lane relaunched the worker with both ids;
- the `--wi ""` launch printed "claiming WI-401";
- both two-spec closes returned `['WI-401', 'WI-402']`;
- the two-row close under the joined subject peeled to the judged commit;
- the list assignment exited 0 instead of 2.

**Done-when coverage**
- Admission: covered by `test_lanes_back_in_the_station_the_first_spine_row_admits_alone`, `test_no_kind_maps_to_a_batch_arm` and `test_spine_rows_admit_one_per_exclusive_turn`.
- Claim: covered by `test_a_multi_item_claim_refuses_before_any_state_change` and `test_an_empty_claim_refuses_before_the_lock`.
- Resume: covered by `test_a_parked_lane_claimed_with_two_specs_stops_the_run`.
- Worker: covered by `test_the_worker_refuses_any_assignment_but_one_id`, `test_a_list_assignment_exits_preflight_before_a_provider_launches`, `test_the_wi_help_names_one_work_item` and `test_an_explicit_empty_assignment_is_refused_not_driven`.
- Prompt: covered by the slot test and the golden one-row render.
- Close: covered by the two two-spec refusal tests and `test_a_partial_close_restores_the_single_report_after_move_refusal`.
- Peel: covered by the two two-row no-peel tests and the writer-to-attestor test.
- Claim subject and history readers: covered by `test_the_claim_subject_composes_one_id_only` and `test_a_historical_joined_claim_still_reads_as_a_claim`.
- Other readers: covered by `test_a_lane_whose_one_row_is_ordinary_runs_the_bar`.
- Text: checked by reading. The PROCESS_OPTIONS paragraph is gone. The byte stamps are measured right: PROCESS_OPTIONS 199,839 -> 199,478 (-361), and the skill 4,523 -> 4,559, with all three copies identical. The README rows, script headers, runtime-flows and concurrency-v2 notes are updated.
- RESYNC: the entry is present, and the 81cac0e1 and f4ca1bd5 entries carry supersede notes.
- Spine rows: amended, with the gaps listed in the findings below.
- Checkpoint sitting: not checked, because its record is under the excluded docs/decisions.
- `docs/cli-reference.md`: still shows the `'WI-201;WI-204'` help on the lane tip. It is a trunk-owned `[generated]` region, so its regeneration is owed at landing (a note, not a finding).

**Consolidation.** `parse_wi_id` is now the one home of the one-id rule for both the claim and the worker. `_stop_run` replaces two copies of the freeze-or-exit block. I found no new repeated stage.

**Coverage-extension notes (no severity).**
- A hand-made `active/<b>/WI-x.md` with no id makes `_admit_parked` raise on `(wi_id,) = wi_ids`. That fails closed, outside the §6 threat model.
- On a hand-made multi-spec claim, `_lane_bar_directives` takes `bars[0]` rather than the strictest bar. That is outside the promise the spec bounds.

**Disclosure.** My one `trace.py --strict-integrity` run rewrote the git-ignored `docs/test/report.md` in the lane worktree. No tracked file changed: `git status` is clean.

**Commands**
- `git rev-parse HEAD` (lane worktree) -> `4dc0f7e292f3429c966f1f2c2c67bc213074000f`
- The brief's 17-module pytest command, run in the foreground by my sub-agent. Relayed result: `755 passed, 2 skipped in 1210.57s` (the 2 skips are the posix-shell gate).
- `python project-trajectory/scripts/check_trajectory.py --strict`, run by the same sub-agent. Relayed result: exit 0, warnings only.
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=138 LLR=326 TC=353 orphans=0 integrity=0 verified-mechanized=131 ...`, exit 0.
- Base-tree red-before run (41dfbb17e archive with the head test files): `15 failed, 6 passed`. The 6 passes are the preserved-behaviour pins (the historical-reader test, the restore test, the three valid-value worker cases and the one-id-subject two-row close, which the base subject check also refuses). All the new refusal tests fail.
- `python project-trajectory/scripts/trace.py --docs <base registries> --tests-for kitlib/verdict.py` (and `integrate.py`), against `--docs docs` at head. At head both drop `tests/test_bar_attestation.py`.

**Findings**

- [MAJOR] docs/test/test-cases.toml:2103 -> **TC-205's evidence cell shrank from 87 entries to 4.** The spec grants only a traced edit that follows the code. Yet 86 still-existing tests are gone from the cell, and with them every citation of three files: `tests/test_bar_attestation.py`, `tests/test_integrate_station.py` and `tests/test_integrate_admission.py`. `tests/test_bar_attestation.py` is now cited by no TC at all. The real reader proves the loss: `trace.py --tests-for kitlib/verdict.py` and `--tests-for integrate.py` listed `tests/test_bar_attestation.py` at base and no longer do. So a builder iterating on the Bar-Green grammar's home is no longer pointed at its tests. TC-205's own method still says those suites are "cited beside this module" and in "the cited set", so the row now contradicts itself (K1, K3). TC-156 (docs/test/test-cases.toml:1564) likewise dropped five still-existing adoption-test node ids. -> Restore the base evidence of both cells, and change only what the code changed: drop `test_a_two_row_batch_close_peels_under_one_canonical_order` and add the new tests. -> @owner convergence-class: yes
- [MINOR] docs/test/test-cases.toml:1450 -> **TC-146's method was rewritten whole.** The spec allows it to change "in their single-WI parts only ... the rest of the cell waits for item 5's migration". The rewrite also drops concrete pins: "pinned by name", "bar = DevStg-Tests reaches check.py as --gate DevStg-Tests (asserted off the recording stub's own argv)" and "(fail toward the bar)". An approved row has changed beyond its grant (K3). -> Restore the base method and replace only "a mixed batch bars as usual" with "a lane whose one row is any other kind bars as usual". -> @owner
- [MINOR] docs/requirements/system-requirements.toml:641 -> **SR-148's rationale was not ported.** The spec's target meaning asks for the `contract_split` sentence: admission cardinality here and executable-claim cardinality in SR-156 bound one single-WI contract at two boundaries. Without it, the rationale's "stated here and nowhere else" now overlaps SR-156's new "every executable lane claim names exactly one work item" (for clarity). -> Append CS's sentence to the rationale: "The uniqueness claim concerns selection precedence; the admission cardinality here and executable-claim cardinality in SR-156 constrain different boundaries of the same single-WI contract." -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:1504 -> **LLR-150 keeps the old tree-signal wording.** It still says "the tree signal (specs moved out of active/<branch>/)". The spec's target meaning is "the one assigned spec leaving the claim directory", and CS reads "the assigned spec" (for clarity). -> Replace it with "the one assigned spec moved out of active/<branch>/". -> @owner
- [MINOR] project-trajectory/scripts/dispatch.py:1059 -> **Three new Implements tags do not match their LLR rows (K3).**
  - `_stop_run` cites LLR-143, whose `code_symbol` is `run` alone. The lane listed `_stop_run` under LLR-150 instead.
  - `_buildable_wi` (project-trajectory/scripts/agent_loop.py:1366) cites LLR-061, but is not in LLR-061's `code_symbol`.
  - `_the_one_claimed_spec` (project-trajectory/scripts/handback.py:370) cites LLR-144, but is not in LLR-144's `code_symbol`. It also serves `close_adjudication`, which is LLR-312's.

  This leaves the Done-when "traced cells follow the code" short. -> Make each tag and its row agree: either retag `_stop_run` to LLR-150 or add it to LLR-143, and add `_buildable_wi` to LLR-061 and `_the_one_claimed_spec` to LLR-144's `code_symbol`. -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:1499 -> **Two replaced clauses read poorly (for clarity).**
  - LLR-149's new detail repeats the keep-nondependent rule inside one cell ("a human-held attestation/gate row SURFACES even under keep_nondependent ..." and again "a human-held attestation or gate row surfaces even under keep-nondependent ..."), and keeps the retired word "attended".
  - LLR-151's replaced clause starts a sentence in lower case ("... dispatch_lock_held=True. a claim commit moves one queued spec").

  -> Drop the duplicated sentence in LLR-149 and capitalise "A claim commit" in LLR-151. -> @owner

VERDICT: CHANGES-REQUESTED findings=6
