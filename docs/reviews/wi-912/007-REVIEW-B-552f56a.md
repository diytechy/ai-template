Reviewed: 552f56a3ae204203d8e151814bc5aefe35366789

**Verified.** Full-lane review, convergence stance, of 702ce8511..552f56a3 over the brief's pathspec. The worst failure classes this change admits are: (1) fail-open, where the act turn reports `act: complete` while a listed act is untaken, or takes an act the verdict did not authorize (an unblessed MEANING row, a held row, a RETURN row, a registry with no approved row); (2) silent wrong content, a wrong `--approves`/`--reattests`/`--verdict` argument; (3) data loss, a retirement that drops a held row from the recorded copy. I hunted those first, through the real code paths.

- **What the assembler authorizes.** `adjudicate_act._arm` reads `intake.adjudication_action`. Held APPROVE, held MEANING, unblessed MEANING and RETURN rows owe no act, and the per-rung pin test confirms this. `_grouped` keys `--approves` by the approved rows' registries only. `--verdict` is set when any listed re-attest is held, and the merge's `held_reattest_refusal` judges only the held rows.
- **Retirement through the real `intake.py snapshot` CLI** (probes under my scratch directory, not the in-process writer the tests use):
  - On a released rung, a retirement-only act (`--reattests TC-001`) clears the copy, and `left_owed` then reads None.
  - On a held rung, a retirement plus a held CLARITY row in the same registry: the assembler lists only the CLARITY row, and the real snapshot REFUSES (rc 1) because the removal is unattested. The copy keeps TC-001, so there is no data loss and no fail-open; `left_owed` keeps reporting the re-attest as owed.
- **The act turn.** `coordinator_adjudicate.act` refuses before launch for every input in the Trust section (exit 2, nothing launched, HEAD and the tree untouched). It exits 0 only when `call_succeeded` holds, `left_owed` is None at HEAD, and nothing under `docs/reviews/` changed (committed or uncommitted). The loop note is appended in exactly one place, `_launched`, which both commands go through; `adjudicate` previously launched `prompt=prompt`.
- **Pre-fix runs.**
  - Lane patch f937df747 (retirement): I loaded the module as it stood at ef63a1d42 and ran the three retirement tests against it. All three FAIL ("TC-001 is inconsistent: its committed status is absent"); they pass at the tip.
  - Patch 0f10b36ce is a refactor with the same behaviour. 552f56a3a only retags.
  - Every other Done-when test targets a module or command that does not exist before the change (`adjudicate_act`, `act`), or text the old templates carried (`intake.py snapshot`, "BY YOU"), so each fails on the pre-change code.
- **Done-when coverage.**

  | Done-when item | Covered by |
  |---|---|
  | No judging brief orders an act | `test_no_judging_brief_orders_an_act` (4 cases) |
  | WI-572 pin successor | `test_the_act_turn_reports_success_only_when_no_listed_act_is_left` |
  | Trust refusals | `test_the_act_command_refuses_each_trust_input_before_launch` (12 cases) and `test_each_unaccepted_or_unreadable_verdict_is_refused_naming_why` |
  | Retained and fresh turns take the same act | `test_a_retained_and_a_fresh_act_turn_take_the_same_act_from_one_verdict` |
  | Combined order | `test_a_combined_act_commits_its_amendment_act_before_its_first_approval_act` and `test_a_combined_verdict_lists_the_amendment_act_before_the_first_approval_act` |
  | Mixed first approval | `test_a_mixed_first_approval_verdict_approves_only_its_approved_rows_registries` |
  | Unblessed MEANING | `test_a_MEANING_row_without_the_bless_mark_is_left_unacted` |
  | Stop-short / reviews write | `test_the_act_turn_reports_success_only_when_no_listed_act_is_left` and `test_an_act_turn_that_writes_under_docs_reviews_does_not_succeed` |
  | Flip/snapshot interruption | `test_an_act_interrupted_between_flip_and_snapshot_is_refused_dirty_then_rerun_in_full` |
  | Combined interruption | `test_a_combined_act_interrupted_between_commits_reruns_with_only_its_first_approval_act` |
  | Flip without copy | `test_a_flip_committed_without_its_copy_is_refused_naming_the_row` |
  | Drafted row in a whole-registry copy | `test_a_Drafted_row_present_unchanged_in_a_whole_registry_copy_is_owed` |
  | Loop marker on / off | `test_under_the_loop_marker_every_launched_prompt_ends_with_the_loop_session_line` and `test_without_the_marker_no_prompt_carries_the_line` (every class plus `act`) |
  | Skill sync | `diff -q` of the kit source against `.claude/skills` and `.agents/skills`: identical |
  | Catalogue | `gen_prompt_catalog.py --check`: fresh |
  | byte-budget-guard | `PROCESS_OPTIONS.md` 199,296 -> 199,426 = +130, matching the restamped row |
  | RESYNC entry, with the loop gap stated | present |
  | Checkpoint sat in the new shape | act ledger seq 126 (re-attests) then seq 127 (approves LLR-338, TC-368) in separate commits. The coordinator's decision record lives under `docs/decisions/`, which is outside my reading scope: unverified here |
  | Landing bar (smoke tier, `trace.py --strict`) | not run, by round instruction; it is the landing tip's |

- **Requirement/interface relationships** (my semantic decisions):
  - SR-231 amended, with counterparts LLR-306, IF-283, IF-284 and IF-285. The change is carried: each now states the `act` command, its exits 0/1/2/7 and its readings, and the reservation clause is scoped to the judging turn on both sides.
  - LLR-306 adds SR-209, with counterparts IF-260 (requestor `coordinator_adjudicate` added) and TC-321 (now verifies SR-209). Carried.
  - LLR-338 is new under SR-231 and SR-232, with counterpart IF-296 (new, Drafted, as IF rows stay under OI-112), verified by TC-368. Carried.
  - The IF-090, IF-113, IF-124, IF-175, IF-195, IF-196 and IF-287 requestor additions match the new module's imports (`intake.adjudication_action`, `prompts`, `baseline_snapshot`, `kitlib.verdict`, `kauthority`, `acceptance_record.rows_at`, `ksitting`). Carried.
  - LLR-310 gains the bless reader, its counterpart IF-175 data gains "blessed rows", and TC-368 is added to its test_refs. Carried.
  - LLR-305 gains `_add_act_template`, counterpart TC-322. Carried.
  - LLR-167, TC-161 and TC-308 lose the `--approves` slot. Carried, except for one stale clause (finding 1).
- **Decomposition.** LLR-338 is the one retained child. It is a single derivation (verdict plus committed tree to owed acts), and splitting the owed/taken partition from brief filling would only re-split one all-or-nothing derivation, which adds no independent decision.
- **Rubric.** K2 holds: no SR cell names a script or command. K3 holds: every new `Implements:` tag names an LLR whose module is that file and whose code_symbol lists the function. K4 holds: the RESYNC entry is anchored at trunk commit ace24c85c (the landing re-anchors it at its parent, per recipes §3).

**Coverage-extension notes** (inputs outside the declared set that the change fails closed on):
- A verdict that rules APPROVE on a row the first-approval brief marked out of scope would be flipped by the act turn, and the merge slot then refuses that flip by name.
- On a held rung, a retirement or an unblessed MEANING row sharing a registry with a listed CLARITY row makes the real snapshot refuse. The act turn exits 1 with the act still owed.

**Commands**
- `git rev-parse HEAD` -> 552f56a3ae204203d8e151814bc5aefe35366789
- `lowprio.py python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../gate/opus/wi-912 tests/test_adjudicate_act.py tests/test_coordinator_act.py tests/test_adjudicate_brief.py tests/test_coordinator_adjudicate.py tests/test_routing_and_prompts.py tests/test_done_when_blessing.py tests/test_assumption_observation_briefs.py tests/test_prompts.py` -> `395 passed in 296.18s (0:04:56)`. The first attempt hit an INTERNALERROR because the basetemp's parent directory did not yet exist; I created it and re-ran.
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (937 work item(s), 817 done (87%), 30 cancelled, graph acyclic).`
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=304 TC=318 orphans=0 integrity=0 ... interfaces=245 interface-findings=0 ...`. The worktree stayed clean.
- `python project-trajectory/scripts/gen_prompt_catalog.py --check` -> `gen_prompt_catalog: fresh (14 prompts).`
- probe1.py: retirement-only act through the real `intake.py snapshot --reattests` -> rc 0, then `left_owed` None.
- probe2.py: the three retirement tests against adjudicate_act.py at ef63a1d42 -> 3 FAIL, while the absent-row first-approval guard PASSes.
- probe3.py: held versus released retirement beside a CLARITY row in one registry, through the real CLI. Held: rc 1, the copy keeps TC-001, and the re-attest stays owed. Released: rc 0, nothing owed.

- [MINOR] docs/requirements/low-level-requirements.toml:1708 -> for clarity (K1): LLR-167's detail still says "`_judged_tiers` derives first-approval tiers from its `--approves` registry walk", while the sentence this lane appended says a first-approval brief "derives neither an approval-registry token nor its per-token row map"; one cell now reads as both deriving and not deriving the `--approves` set -> reword the clause to "from the registries of the rows the brief marks as this session's" -> @owner
- [MINOR] project-trajectory/scripts/adjudicate_brief.py:993 -> for clarity (K1): the comments in the modified first-approval assembler still describe the retired slot. At :993-998 they say "`{registries}` is fixed at composition time ... a mixed batch has to be able to DROP a token". At :953 and :1241 they speak of "the caller's `--approves` set" and "its `--approves` walk". This diff removed that slot (the docstring at :1142-1146 says so), so the comments describe behaviour the module no longer has -> rewrite them as the registry walk that feeds `_judged_tiers` only -> @owner
- [MINOR] project-trajectory/scripts/intake.py:899 -> K1: `_first_approval_context`, the minted first-approval adjudication row's Context, still orders the act inside the judging session ("APPROVE (move the rows' `Status` to `Approved` and take the anchoring snapshot ... in ONE reviewed commit on this lane) ... The approval act is YOURS"). `_amendment_context` at :783-787 likewise tells the judge to name rows "in the act's `--reattests`". So a sitting that reads its own row's spec is still told to act in-turn, contrary to the split this lane ships. Acting out of landing order is the defect the WI exists to close. The merge slot does not enforce landing order, so nothing downstream catches it, but the brief the session is handed says otherwise, hence MINOR -> reword both contexts to say the verdict authorizes a later act turn (`coordinator_adjudicate.py act`) and stop at the verdict -> @owner
- [MINOR] project-trajectory/RESYNC_PACK.md:8635 -> K4: the entry's "Kit-owned files — overwrite" list omits `prompts/CATALOG.md` (regenerate). This diff changes the catalogue: the new `ADJUDICATE-ACT` row, three new digests, and the first-approval slot set. Downstream, check.py's `prompt-catalog` step (`gen_prompt_catalog.py --check`) runs at every stage, and earlier entries (:7837, :8471) list the catalogue for exactly this reason. An adopter applying this entry as written turns that step red -> add "`prompts/CATALOG.md` (regenerate)" to the list -> @owner
- [MINOR] docs/work/active/wi-912/WI-912-verdict-act-split.md:273 -> the spec acknowledges a reachable residue: a retirement whose registry carries no other act in the branch. The act turn reports `act: complete` for it, and then the merge slot refuses it. The spec says this is "left to a follow-up row", and recipes §3 repeats that, but no `## Dispositions` draft or minted row carries it within the reading scope, so the known gap has no tracked home -> draft the follow-up in this spec's `## Dispositions` section so intake mints it at this merge -> @owner

VERDICT: APPROVE findings=5
