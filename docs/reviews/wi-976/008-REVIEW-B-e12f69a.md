Reviewed: e12f69aa14f0d0823c248a849c29a3bdb5d1db07

Verified. This was a full-lane review in the convergence stance, of WI-976 against its spec (docs/work/active/wi-976/WI-976-retire-perspective-sidecar.md) and the kit-change rubric (K1-K3, B1). `git rev-parse HEAD` printed the reviewed commit. Failure classes I hunted first: (1) silent wrong content, where a sitting brief carries the wrong hat set (siblings merged, parents missed, questions on a non-round) or a hat line changes a ruling; (2) fail-open, where a malformed roster composes a round's brief; (3) dangling live surfaces after the retirement.

What I drove through the real code (`adjudicate_brief.compose` on this lane's own spine, with scripts in the scratch folder, no bytecode written):
- An amendment sitting of SN-036 carries the hat block and its `- HAT` outcome form.
- First-approval of LLR-360 and TC-399, and amendment of SR-161 alone, each state NOT_A_ROUND once.
- A combined sitting `amendment:SN-036;SR-161;LLR-183` + `first-approval:LLR-360;TC-399` puts the pointer line in each section's slot, then one `=== THIS SITTING'S PERSPECTIVES ===` part after the last section, carrying each question once.

Convergence fix confirmation. I exported the pre-fix tree at 9eeff7a2f (from `git log -p --format=%h`) into scratch and overlaid the tip's test files. These fail there and pass at the tip:
- test_an_amendment_round_reaches_the_need_of_every_sr_it_judges
- test_a_combined_round_reaches_the_need_of_an_sr_another_section_amends
- test_the_spine_authors_hats_value_puts_the_sittings_questions
- test_mkprompt_asks_only_the_hats_of_the_needs_the_turn_names
- test_mkprompt_refuses_a_hats_value_naming_no_need (all 4 params)
- test_the_cycle_names_the_hats_slot_at_dispatch (all 3 copies)

The e12f69aa1 recipe fix is confirmed by the corrected text at all three recipe copies: "each need an SR it amends names", byte-identical across copies.

Done-when coverage:
- Ruling fragment before row text: commit 36fc6d6f7, the fragment, precedes the rows commit 4fc5d55f4.
- Spine rows, read against the spec's proposed text:
  - SN-036 acceptance matches verbatim.
  - SR-161's title, requirement, acceptance and coincident match, and verification is Inspection.
  - LLR-183 has the opening and closing clauses.
  - TC-178's expected is split.
  - TC-211 verifies SR-161 and SR-186, and its inputs name no sidecar.
- LLR-297 and TC-312 are removed, with docs/log.d/retired/LLR-297.md and TC-312.md added.
- LLR-360 and TC-399 are added; all 21 TC-399 evidence functions exist.
- IF-133 drops `load`; hats.py now uses only load_needs, resolve, stem, folded and NEED_CARRIERS.
- inspection-procedures: the missing-perspective-outcome input is added and the 2026-09-06 result is kept as history; the rubric's R1 and B1 are rewritten.
- The record code and tests/test_hats_record.py are gone. The sidecar and its pointer paragraph are gone. A grep of the live surfaces for the sidecar or the record command finds nothing; the "perspective record" hits that remain mean Hat-Refs. The PROCESS.md §1 sentence, spine-questions (c3), both roster headers and the three recipe copies are updated.
- SAFETY is out of the live roster (15 hats), the template keeps it (16), and the name pins are split.
- Hat-block states: each is covered by TC-399's tests, and I confirmed them by driving the code above.
- mkprompt's HATS: covered by test_prompts.
- The RESYNC entry supersedes the 9233772b entry. CATALOG digests are refreshed. The byte-budget row matches: `wc -c` gives 97,962 now against 98,185 at the base.

Not yet reached at this tip, because they are the lane's later steps rather than this diff:
- TC-211's sample (the lane's checkpoint sitting, its brief committed). TC-211's `inputs` do not yet name that record and its brief, so the checkpoint reconcile must add them.
- The fresh-session re-judge.
- The owner's SN-036 act, and no landing before it.
- The retirements' "at the sitting".
- The commit bar, which the round facts say not to run.

Coverage-extension note (fails closed, no severity): `plan_briefs._roster_refusal` wraps every HatsError, including an unknown SR or SN id behind a judged row, as "cannot be composed from docs/requirements/hats.toml". The refusal holds the sitting correctly but names the roster for a need-registry fault.

Commands:
- `git rev-parse HEAD` -> e12f69aa14f0d0823c248a849c29a3bdb5d1db07
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r3b/wi-976 tests/test_plan_briefs.py tests/test_adjudicate_brief.py tests/test_prompts.py tests/test_hats.py tests/test_dogfood_sync.py` -> 347 passed, 1 skipped in 46.21s
- `python project-trajectory/scripts/check_trajectory.py --strict` -> check_trajectory: clean (973 work item(s), 863 done (89%), 34 cancelled, graph acyclic).
- `python project-trajectory/scripts/trace.py --strict-integrity` -> Traceability: SN=31 SR=138 LLR=326 TC=353 orphans=0 integrity=0 verified-mechanized=131 verified-demonstrated=7 verified-attested=0 drafts=2 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=255 interface-findings=0 ac-advisories=1 paraphrase-advisories=2. This rewrote the git-ignored docs/test/report.md; `git status` is still clean.
- pre-fix tree at 9eeff7a2f with the tip's tests, `pytest ... -k "hat or mkprompt or HATS or cycle_names"` -> 9 failed, 37 passed; `-k "reaches_the_need or round or sitting or override"` on test_adjudicate_brief -> 3 failed, 6 passed (the failures are the fix tests listed above)
- r3b/probe1.py (compose over this lane: combined, amendment SN-036, first-approval LLR-360;TC-399, amendment SR-161) -> HAT block 1, 1, 0, 0; NOT_A_ROUND 0, 0, 1, 1
- r3b/probe2.py (amendment SN-036: an authoring row with Workstream "scripts" against a merge-minted row with "process"/"adjudication") -> lost on the minted route: ['CROSS-PLATFORM', 'DATA-PROTECTION']

- [MAJOR] project-trajectory/scripts/plan_briefs.py:434 -> (K1) `round_questions` widens each need by the tags of the row handed to `compose`. On the merge-mint route (`agent_loop.py:406` composing a row minted by `intake.py:829`/`:933`), that row is the minted adjudication row, whose Workstream is always "process" and SafetyClass "adjudication". The decomposing work item's tags never reach the sitting brief. Driven on this lane, probe2 shows an amendment of SN-036 dropping CROSS-PLATFORM and DATA-PROTECTION from the minted sitting that the in-lane sitting (compose_lane, the lane's own work-item row) carries. No check counts the outcomes, so the omission is silent, against the Done-when's "widened by the work item's tags ... the rule the dual-plan planner already uses" and LLR-360's "widens each need by the work item's declared tags" -> carry the authoring work item's Workstream/SafetyClass onto the first-approval and amendment rows at mint (intake's two draft builders already run with the merged lane's work item in hand), or have the composer resolve the authoring work item, and add a TC-399 case that composes a minted-shape row; if that scope is refused, state in LLR-360 and the RESYNC entry that a trunk-minted sitting is widened by no work-item tags, and stop it being widened by the adjudication row's own -> @owner convergence-class: yes
- [MINOR] docs/requirements/system-requirements.toml:812 -> (K2, for clarity) SR-161's new rationale says "The hats roster and plan briefs already supply the applicable questions". "plan briefs" reads as the `plan_briefs` module, an implementation carrier, in an SR cell, where PROCESS.md §1 says "the planning briefs" -> reword to the artifact class ("the hats roster and the planning briefs"), or drop the clause, at the checkpoint sitting that judges SR-161 -> @owner

VERDICT: CHANGES-REQUESTED findings=2
