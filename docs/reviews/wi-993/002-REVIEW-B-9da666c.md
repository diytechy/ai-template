Reviewed: 9da666cbf8200e0e93c8efdddecc5c26c741cbf8

Verified. Independent REVIEW-B of the full lane, read from the three-dot diff, the spec and `docs/specs/WI-993.md`. Failure classes hunted first: (1) silent wrong content, an item whose act is wrong or a row carried out of the amendment row with nothing holding it; (2) fail-open, a mint on an unaccepted, released or settled row; (3) data loss, forced rows lost at a landing.

The mint's closed set holds. I drove the real `intake_after_merge` and found no state that mints wrongly on a pending, failed, invalid, unbound, CLARITY, released or copy-equal row. Six mutations of the arm each turned tests red, so the tests are witnesses: any-MEANING reader (1 red), no copy comparison (2), no dial (3), stage-read dial (3), carried rows kept on the amendment row (7), reversed verdict order (2). The carried filter has one caller, `intake_after_merge`, so sweep and merge slot share it. A verdict or copy git cannot read fails safe or refuses by name.

The single-row command runs: the minted `intake.py snapshot --approves ... --reattests SR-001 --verdict ...` exited 0 in a real repo. `--verdict` on an unblessed MEANING row is safe on trunk, because `unaccepted_refusal` judges only acts a merge adds.

The claimed citer holds. A full `check_trajectory.py --strict` on a repo with an item only a claimed row cites exits 0 ("clean (1 work item(s)..."), and the row reads `blocked:open-item-pending:OI-5`. Spec claims checked by running: a `- [x]` tick leaves `kitlib.done_when.items` equal, and `ruling_sync_lines` returns `[]` for a ruling that ticks a claim copy. `_CITER_STATUSES` is the one home and every queue reader goes through `open_item_queue`. No reader of a claim and no detector was added (call 7).

Done-when map:
- PROCESS.md states the ruling once, and step 3 points at it: inspected at `project-trajectory/PROCESS.md` §5 and the skill. A grep of the narrower rule leaves only history and generated views (`docs/interface-reference.md` is declared `[generated]`).
- Keep the claim at a planned step, with OI-70's text sites amended: inspected, all sites carry the exception.
- OI-126, a held-rung approval is never such a step: inspected, one stale site remains (finding 3).
- Sitting verdict writes the item: tests/test_intake_held_act.py, 20 cases; "the command" is covered only as a string, and that gap is finding 1.
- Owner queue counts claimed rows: test_a_claimed_citer_counts_beside_a_queued_one, test_an_item_only_a_claimed_row_cites_is_no_error, test_a_claimed_citer_is_a_card_and_on_the_blocked_list, test_a_draft_or_deferred_citer_still_reads_uncited.
- Routine push files no item, and an act's item closes by ruling or delegated decision: text, inspected.
- No detector: inspected, none built.
- RESYNC one entry: present, one remedy wrong (finding 2).
- Review bar A+B: this verdict is the B half.

Requirement and interface relationships, each changed side with its counterpart and my decision:
- IF-073 (data, notes, v2) with LLR-299, LLR-118, TC-314, TC-123 and the open-items headers: carried, wording agrees with the code.
- IF-073 with LLR-288: retained, it reads any row's `needs` and a claimed row already reads blocked (observed).
- IF-073 with SR-148 and SR-049: retained, neither says "queued".
- IF-074 with LLR-118: carried.
- LLR-153 with SR-174 and SR-228: retained. SR-228 limits an adjudicated re-attest to CLARITY, and the arm takes no act, so it does not contradict; SR-174's mint is the writer's existing home.
- LLR-153 with TC-147: carried.
- LLR-364 with LLR-153: carried, the same "owner row carries" clause on both sides.
- IF-091 with `unanchored_rows` and LLR-153: carried, `code_symbol` and `module` list it, so K3 holds.
- IF-224 requestor added, with its notes: retained, intake is in CMP-008 beside agent_common, so no new crossing.
- The new row text was swept against the existing registries: no SN or SR cell changed (K2), no Status moved, and the only contradiction is the K1 point in finding 1. No decomposition here, so no child-purpose record is owed.

Commands:
- `git rev-parse HEAD` -> 9da666cbf8200e0e93c8efdddecc5c26c741cbf8
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../s1B/wi-993 tests/test_intake_held_act.py tests/test_intake.py tests/test_acceptance_record.py tests/test_open_item_queue.py tests/test_open_item_readiness.py tests/test_gen_open_items.py tests/test_traj_status.py` -> 239 passed in 201.05s (0:03:21)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> check_trajectory: clean (998 work item(s), 886 done (89%), 34 cancelled, graph acyclic).
- Probes outside the lane, `s1B/probe/test_probe.py` and `test_probe2.py`, driving `intake_after_merge` and the `intake.py snapshot` CLI on real repositories -> P1 exit 0; P2 both commands exit 1; Q1 exit 1, widened exit 0; P3 second mint refused; P4 minted with the amendment row empty.
- `s1B/probe/test_mut.py` under six `MUT` values -> 1, 2, 3, 3, 7 and 2 failed, as listed above.
- `git status --short` in the lane -> empty.

- [MAJOR] project-trajectory/scripts/intake.py:913 -> K1, B1: the command an item publishes is refused whenever another row of the same registry is unanchored, which is the normal state once two owner acts wait, because `baseline_snapshot.refresh_refusal` copies a whole registry and refuses any drifted row the act does not name. Driven: the state tests/test_intake_held_act.py:368 builds (two verdicts, SR-001 and SR-002, one registry) mints OI-1 and OI-2, and each item's command exits 1 ("would ABSORB approved text ... SR-00x"), so neither order completes; the same holds across two landings with the owner not yet acted (Q1). The refusal's remedy, naming both rows beside the item's `--verdict`, exits 0 but records lane A's verdict in the act ledger for SR-002, a row that verdict never ruled, and the owner page audits that list. So the Done-when's "the command" and LLR-153's "the act's command" are untrue for these rows, and no test runs the command -> have the mint file one owner row and item per landing per registry rather than per verdict, and state in option (a) that the act is per registry: name every other drifted row of that registry and drop `--verdict` when the act spans verdicts (the flag is optional and holds one path), amending LLR-153 and TC-147 to match; extend the two-verdict test to run each minted command through `intake.py snapshot` -> @owner
- [MINOR] project-trajectory/RESYNC_PACK.md:10573 -> B1: the stated remedy for a non-TOML registry, "file the item by hand and run `intake.py sweep` over the range", does not clear the refusal. Driven (P3): after hand-filing an item and a citing queued row, the replay refuses again with the same text, since the draft dedups only on an exact title that neither the refusal nor the entry names (Q2), and until then that range's amendment and disposition rows stay unminted too. tests/test_intake_held_act.py:418 stops at the first refusal. Reach is a repository still on the CSV carrier, which this pack already migrates -> change the remedy to converting with `migrate_carrier.py` and then sweeping, and say the same in the `_mint_open_item` refusal for this arm -> @owner
- [MINOR] project-trajectory/skills/coordinator-cycle/SKILL.md:430 -> B1: "Stop that row for an owner signature on a new need" still tells the coordinator to stop a lane for a held-rung approval, two lines after pointing at PROCESS.md §5, which now says a held-rung approval is never a stop and the lane lands its text (OI-126 Q2; Done-when "The text sites say so"), and against the amended spine-authoring row saying held first drafts land. The same text sits in the `.agents` and `.claude` copies -> reword to a stop only for what §5 still keeps in the lane, or point the sentence at §5 -> @owner
- [MINOR] project-trajectory/scripts/intake.py:923 -> B1: the arm does not read the verdict's bound text. Driven (P4): a row edited after an accepted MEANING verdict, with no re-sit, still mints an item saying that verdict ruled the row, and the row leaves the amendment row, so nothing re-sits text no sitting saw, though PROCESS.md:679 binds a verdict to the text it judged and real bindings carry `rows = <id>=sha256:...`. The owner still reads the live row before acting, hence MINOR -> leave a row whose text differs from `kitlib.sitting.accepted_identities` on the amendment row, as the spec's table does for an unsettled row, and amend that table's first line; this stays a read rather than an unrepresentable state because the verdict and the row are separate files written at separate times, and a held MEANING row has no act to refuse the edit at the commit -> @owner

VERDICT: CHANGES-REQUESTED findings=4
