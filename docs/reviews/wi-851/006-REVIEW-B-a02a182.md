Reviewed: a02a18284c87ed3fe641e916f547de182a751920

Full-lane review of WI-851 (range 31b8ed941..a02a182), convergence stance. I read no earlier verdict, decision record or lane commit message. Commit history was read only as `--format=%h` hashes and stats.

Verified. I hunted these failure classes first:
- a fail-open path that lands a held approval;
- a fail-open marker arm;
- silent wrong content in the row-text identity, meaning a digest the brief and the rule compute differently.

What I checked and found right:
- **Claim predicate.** `held_status.held_claims`, `_copy_claim` and `_excepted` match Done-when's closed predicate: claims (a) and (b), the exception's five conditions, and the not-judged list.
- **Refresh merges.** A claim counts only when it holds against every parent (`_every_base`). So a refresh merge claims nothing, and a merge resolution that approves a row claims against both parents.
- **Dial.** The slot rider reads `dial_at(root, "HEAD")`. That is trunk at the slot, because `integrate._each_lane_commit` walks `_head(root)..branch` from the trunk checkout, and trunk again at a squash landing.
- **Unreadable state.** A carrier on the head side that cannot be read, or that does not parse, refuses by name. A base side that fails counts every approving row as a claim. `grep_files` tells exit 1 ("no match") apart from a failure.
- **Squash.** The squash path (`check._held_squash_refusal` over `text_then_act.squash_walk`) admits only when the tip contains HEAD and the index holds `HELD_PATHS` byte-equal. Otherwise it judges the index as one commit. Text then act's own squash path is behaviour-preserved.
- **Marker arm.** It is skipped inside a claimed lane (`kitlib.git.claimed_work_branch`, a byte-faithful move of check.py's reader). It judges HEAD and MERGE_HEAD during a merge, so the slot's own merge commit is not double-refused.
- **Row-text identity, compared across readers.** I wrote a probe in my area, `probe/p2.py`. It computes `approved_text_digest` for every live row of the twelve held tiers at HEAD, 1144 rows. Each digest is computed through the rule's reader (`_tier_reads`, via `_side`) and through the brief's reader (`spine_carrier.load`). Result: 0 mismatches. A second probe, `p1.py`, confirmed that off-spine lowercase `status` normalizes to `Status`, so `claims_approval` sees off-spine approvals.
- **Binding.** `record_outcome` carries the identity cell through. `[MEANING+BLESS]`, and a row tagged both ways, read as non-CLARITY (`blessed_rows`, `row_rulings`).

Red-before:
- I exported the pre-implementation tree (62ed6b0ca, the behaviour-preserving move) with the tip's `tests/` laid over it, into my area.
- Nine of the new git tests FAIL there, including the slot tests for:
  - a held SN approved with its copy;
  - loop, coordinator and re-claimed lanes;
  - a held retirement;
  - `[MEANING+BLESS]`;
  - text edited after the verdict;
  - a marked commit inside a lane;
  - both squash cases.
- They fail either by reaching the fixture's undeclared product bar, meaning the lane would have landed, or on the missing digest. At the tip they pass.

Done-when coverage, item by item:
- **Lane predicate, claims (a) and (b), and the not-judged list:** `test_held_status.py` (`test_a_live_flip_into_approval_is_a_claim`, `test_a_copy_entry_move_or_retirement_is_a_claim`, `test_not_judged`, `test_an_unmapped_registry_is_held`), plus the git tests for the slot.
- **Walk (slot rider, squash admitted or not):** `test_the_rule_rides_the_lane_commit_walk`, `test_a_squash_landing_is_judged_by_its_lane_commits`, `test_a_squash_not_admitted_is_judged_as_one_commit`.
- **Unmarked plain trunk commit not judged:** `test_an_unmarked_plain_trunk_commit_approving_a_held_row_passes`.
- **Identity:**
  - brief: `test_the_amendment_brief_states_each_shown_rows_digest`, which covers a chained and an unchained row against the committed digest;
  - reservation: `test_bind_pending_records_the_briefs_identities`;
  - act turn refusing before launch: `test_the_act_turn_refuses_before_launch_when_held_text_moved`;
  - flow 6 text: updated.
- **CLARITY arm retired, `--verdict` optional:** `test_a_held_CLARITY_reattestation_bound_to_the_exact_text_lands[unnamed]`.
- **WI-849's checks unchanged:** the existing `test_snapshot_readers.py` and `test_integrate_admission.py` cases.
- **Marker arm narrowed:**
  - hook: `test_the_same_commit_marked_is_refused_by_the_hook_step`;
  - claim, mint and telemetry writers: `test_each_loop_writer_outside_a_lane_refuses_a_held_approval`;
  - handback: `test_a_handback_commit_outside_a_lane_refuses_a_held_status_move`;
  - marked commit inside a lane: `test_a_marked_commit_inside_a_lane_passes_at_commit_and_is_judged_at_landing`;
  - slot rung retired: `test_the_slot_no_longer_runs_a_loop_lane_held_status_rung`.
- **in-lane.md line and RESYNC entry:** both present. The entry is anchored at the trunk base. It names the retired arm, the narrowed arm, that unmarked trunk approvals are untouched, and that a held verdict sat before the upgrade must be re-sat.
- **Spec test list:** every test it names exists and passes.
- **No item is UNCOVERED.** The "one combined sitting" item could not be checked under this stance: its record lives under `docs/reviews/`, which I did not read.

Two of the tests are source inspections (`inspect.getsource`): `test_the_ledger_clarity_arm_is_retired` and `test_the_slot_no_longer_runs_a_loop_lane_held_status_rung`. Each also has a behavioural counterpart that would fail if the retired arm came back:
- the unnamed-verdict landing;
- `test_an_off_spine_demotion_and_a_born_Drafted_row_land_from_a_loop_lane`.

Rubric results:
- **K2:** the SR-208 cells name no script, command, file or function.
- **K3 (back-links):** every new `Implements:` tag I checked names an LLR whose `module` and `code_symbol` carry it:
  - LLR-246: held_status, git.grep_files, check._held_squash_refusal, agent_policy;
  - LLR-249: committed_status_moves, _spine_status_moves;
  - LLR-359: digest, sitting, brief, act;
  - LLR-141: claimed_work_branch, _implausible_branch_notice;
  - LLR-302: squash_walk.

Coverage-extension notes. These are fail-closed inputs outside the declared set, so they carry no severity:
- The amendment brief renders `JUDGED-TEXT` lines only for the SR, LLR, TC, SN, DA and SUR tiers (`_REGISTRY_OF` and `_UNCHAINED_TIERS`). A held CLARITY re-attestation of an IF, CMP, EXT, B, REL or STK row can therefore never be excepted, and is always refused.
- The second squash of a two-commit hand landing has a tip that does not contain the first squash commit. It is judged as one index commit rather than walked. The bound exception still applies through the index.

Process notes, also carrying no severity:
- `docs/work/active/wi-963/WI-963-sweep-skips-settled-amendments.md:172` still cites the retired `held_reattest_refusal`. That spec is outside this diff, so it is for the coordinator to amend.
- The generated `docs/interface-reference.md` still describes the retired arm. It is trunk-owned and regenerates at landing, so it is not a finding.
- Running `trace.py --strict-integrity`, as the brief requires, rewrote the git-ignored `docs/test/report.md` in the lane worktree. No tracked file changed: `git status` is clean.

The ruled narrowing:
- Off-spine and spine demotions, and below-approval moves, now land from any lane, a loop lane included, where the retired slot rung refused them for loop lanes.
- This is Done-when's stated "Not judged" set, and it is D-003 as the spec drafts it for the owner to confirm or overrule.
- It is not raised as a finding.

Commands:
- `git rev-parse HEAD` -> `a02a18284c87ed3fe641e916f547de182a751920`
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../gate/opus/wi-851 tests/test_held_status.py tests/test_held_status_git.py tests/test_text_then_act.py tests/test_adjudicate_act.py tests/test_adjudicate_brief.py tests/test_coordinator_act.py tests/test_loop_provenance.py` -> `302 passed, 1 skipped in 1030.07s (0:17:10)`. The 1 skip is environment-gated (posix-shell).
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (969 work item(s), 856 done (88%), 34 cancelled, graph acyclic).` (exit 0, WARN advisories only)
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=138 LLR=326 TC=353 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=2.` (exit 0)
- `probe/p1.py`: all 12 held tiers read at HEAD, no failures; off-spine `Status` normalized.
- `probe/p2.py` -> `rows 1144 mismatches 0`: the digest through the rule's reader against the brief's reader.
- Pre-implementation red-before, run on `git archive 62ed6b0ca` with the tip's `tests/` overlaid, in my area: `pytest -n 2 tests/test_held_status_git.py -k "<9 cases>"` -> `9 failed in 26.99s`. The failures are landings that reach the product bar, a lane that is not refused, and the missing `approved_text_digest`.

Findings:

- [MINOR] docs/requirements/system-requirements.toml:1740 -> K3. The lane amends Approved SR-228's `acceptance_criteria` ("when supplied, the recorded act names the verdict"), and Done-when's change set does not grant that. Its list is SR-208, LLR-246, LLR-278, TC-241, TC-278 and IF-196/287/296/129. For clarity, the amended cell still says the act "is refused unless its recorded verdict names that row as CLARITY". Once `--verdict` is optional, that reads as if an unnamed act were refused, yet `test_a_held_CLARITY_reattestation_bound_to_the_exact_text_lands[unnamed]` lands one. -> Record SR-228 in the spec's granted change set, or in a disposition. Reword the cell to "unless an accepted verdict bound to the row's text rules it CLARITY", or else leave the approved cell untouched. -> @owner
- [MINOR] docs/test/test-cases.toml:2847 -> K3/K1. TC-278 verifies LLR-278, and its amended Method and Expected no longer state any held-rung rule except a held retirement. Its evidence still cites held lane-rule tests that exercise `held_status` (LLR-246), not LLR-278:
  - `tests/test_snapshot_readers.py:427` (`test_a_held_rung_is_read_from_trunk_not_from_the_lane`, which calls only `HS.commit_held_approval_lines`);
  - `test_a_held_MEANING_BLESS_reattestation_is_refused`;
  - `test_a_binding_with_no_identity_cell_is_refused`;
  - `test_a_first_draft_under_a_bound_CLARITY_verdict_is_no_exception`;
  - `test_an_absent_or_unreadable_CLARITY_verdict_is_no_exception`;
  - `test_an_unaccepted_or_unruled_CLARITY_binding_is_no_exception`.

  -> Move those ids to TC-241's evidence, where most already appear, so each TC's evidence supports its own Method. -> @owner
- [MINOR] project-trajectory/scripts/acceptance_record.py:988 -> K1 and simplification. `merge_approval_refusal(..., *, trunk)` keeps a required keyword that no rule reads; its own docstring says "`trunk` ... is read by no rule of this function". The one caller's comment at `project-trajectory/scripts/integrate.py:1242`, "`trunk=head`: the act lands under TRUNK's authority ... the merge base can predate a hold trunk has since declared", now describes behaviour that was deleted. -> Drop the keyword from the signature, from the IF-091 contract text, from the integrate.py call and from the five test calls, and delete the stale comment. -> @owner
- [MINOR] project-trajectory/scripts/held_status.py:606 -> PROCESS.md §3, consolidate. The new module repeats logic it already holds:
  - `_own_moves` (606) re-implements `merge_status_moves`' every-parent intersection (188-207);
  - `_commit_bases` (624) repeats `pending_status_moves`' MERGE_HEAD read (219-221);
  - `registry_held` (356) restates the `rung is None or holds_under` test that `held_status_lines` inlines (237-238);
  - `_named` (602) restates `staged_status_moves`' inline path normalization (183);
  - `_REVIEWS` (344) restates `kitlib.sitting.REVIEWS`.

  -> Let `merge_status_moves` take the spine tiers and serve as `_own_moves`. Have `held_status_lines` call `registry_held`, `staged_status_moves` use `_named`, and import `REVIEWS`. -> @owner
- [MINOR] project-trajectory/scripts/held_status.py:317 -> PROCESS.md §3. `HELD_TIERS` is a hand-copied literal of `baseline_snapshot.SNAPSHOT_TIERS`, kept equal only by `test_HELD_TIERS_equals_the_snapshotted_tiers`. The import is unavailable because baseline_snapshot imports check_trajectory, which imports held_status. -> Move the tier table to a lower layer both already import (`spine_carrier`) as its single owner, and import it in both. The pin test then becomes unnecessary. -> @owner
- [MINOR] project-trajectory/scripts/held_status.py:437 -> B1, confirmed by reading.
  - **The gap.** `_bound_clarity` admits a (b) claim on ANY accepted CLARITY binding under `docs/reviews/` in the tree, a historical one from an earlier lane included. WI-849's backing (`kitlib.sitting.uncovered_refusal`) needs only that some binding this branch added (`branch_verdicts`) rules the row CLARITY, whatever text it bound. So the row's own sitting and the matching identity can come from two different verdicts.
  - **The scenario.** A lane sits verdict V on text T2 (CLARITY), reverts the held row byte-exactly to an older text T0 that a past sitting bound, and takes the act by hand through `intake.py snapshot --reattests`. The act then lands, although no sitting in this lane judged T0. The coordinator's act turn refuses it, because it reads V's identity.
  - **Plausibility.** Low: it needs a byte-exact revert plus a hand-taken act.
  - **Fix.** Limit candidates to the bindings the lane added, through the one reader WI-849 already uses (`kitlib.sitting.branch_verdicts(root, "HEAD", rev)`, where HEAD is trunk at the slot and at the squash). This narrows an existing input rather than adding a check.

  -> @owner

VERDICT: APPROVE findings=6
