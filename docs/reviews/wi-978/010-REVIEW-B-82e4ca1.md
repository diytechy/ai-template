Reviewed: 82e4ca1a73bc48382f04522c3f71a3ac811048ad

Full-lane review of WI-978 (range c6e982882e81b7369bd4ca323ad1e06ebe93b108..82e4ca1a73bc48382f04522c3f71a3ac811048ad), convergence stance, rubric docs/rubrics/kit-change-review.md. I read no earlier verdict, plan critique or lane commit message. I took each fix's pre-fix code from the per-path history by short hash alone.

Verified. Before hunting I named the failure classes this change could admit, worst first: (1) fail-open landing, where a registry id lands without its own work item's reservation; (2) data loss, where a writer, merge or fold drops a reservation record or lowers a mark; (3) overlapping ranges, from a lost or ignored compare-and-swap; (4) a fold that writes wrong marks; (5) the refresh resolving a non-watermark conflict by itself. I hunted them in that order.

- The CAS. `write_carrier` moves the ref with `update-ref <ref> <new> <old>`, with an empty old on first use, and refuses LOST_RACE when the ref moved. Each range starts at max(carrier mark, trunk committed mark)+1 (`plan_reservation`).
- The fold. It takes each space's maximum and unions the records. The carrier contributes only its records and the marks they justify (`carried`).
- Every watermark writer carries the records: `bump_watermark`, `correct_watermark`, bootstrap's line-preserving `raise_watermark`, and the intake and plan_artifacts mints through bump. The committed-record check is a union over HEAD, MERGE_HEAD and every parent.
- The hand-raise rule admits a rise only up to the highest well-formed record in the commit's own file.
- Every carrier-space reader (`_csv_ids`, `SPINE_FILES`, `_offspine_ids`, `_sn_ids`) reads under docs/requirements or docs/test. So `ids_at`, which writes out only LANDING_DIRS, misses no carrier-space id.
- The merge-slot rung reads the lane's delta over `_lane_base`. The squash step reads both the staged tree over HEAD and the lane tip over its merge base. Both read retirement records at every tree judged, and both fail closed on an unreadable tree, a SystemExit from the sweep, or an unreadable merge base.
- `_fold_watermark_conflict` acts only when the watermark is the sole conflict left. Any other conflict still refuses, and the merge is undone.
- `_record_act`, the act ledger and the latch are untouched (baseline_snapshot.py is not in the diff).
- SR-174 names no code (K2). It stays Approved with text the spec grants. IF-101 is Drafted.
- Text deliverables: the recipes, SKILL §4 and the Terra prompt match the Done-when, in both copies (test_dogfood_sync green). mkprompt refuses an unfilled `@RESERVED@`. PROCESS.md §4 states keep-or-mint once, directly after the CLARITY/MEANING paragraph, and spine-questions §0 cites it in one line.

Requirement/interface record. Changed side: SR-174, amended and kept. Its counterparts and my decision on each:
- IF-101: carried. Its requestors gain integrate and check, and its data names the reserve, fold, landing and lag calls and the record grammar.
- TC-158: carried. It gains the record rules, and every test it names exists and passes.
- LLR-153, LLR-154, TC-147 and TC-148, and the SR-170/SR-173 rationales: retained. Each reads only the work-item half, and the amendment leaves that half unchanged ("Work items are minted on the integration branch alone").

Decomposition: SR-174 gains two children, each with its own decision.
- LLR-362 is the allocation authority (carrier, record grammar, writers carrying records). Its purpose is verified by TC-401 and TC-158.
- LLR-363 is admission at the landing (the reserved-only rule and landing the fold). Its purpose is verified by TC-402.
- Splitting the fold out further would add no independent decision. Both children consume the one fold, and it is verified through both.

Done-when coverage map:
- Spine rows: present, and both strict lints are clean. The checkpoint sitting's verdict was not read (convergence stance), so I did not verify it.
- Reserve verb admits and refuses: test_id_carrier.py test_the_counts_*, test_the_work_item_*, and test_each_reserve_refusal_writes_nothing (CLI, nothing written).
- First use and the CAS lost race with two worktrees: test_id_carrier_git.py test_first_reservation_seeds_the_carrier_from_trunk and test_a_lost_race_refuses_with_nothing_written[moved, first-use].
- Sequential and stale-base ranges are disjoint, and a reservation after a ruled correction starts above it: test_sequential_reservations_are_disjoint, test_stale_base_reservations_are_disjoint and test_a_reservation_after_a_ruled_correction_starts_above_it. They fail on trunk's code, where the verb does not exist.
- Fold on clean and conflicted files: test_the_fold_*, test_fold_ids_on_a_conflicted_watermark.
- Hand-raise rule, record history, writers keep records, no misreading as a correction: the TC-158 tests in test_id_watermark.py.
- Every landing row on both callers: test_id_landing.py test_the_slot_refuses_each_unreserved_landing[5], test_the_hand_squash_refuses_each_unreserved_landing[5], the unreadable-claim, retired-in-own-record and another-lane's-number cases, and the code-only cases.
- Landing folds the carrier, and a refresh conflict is resolved by the fold: test_the_slot_folds_a_carrier_moved_after_the_lanes_refresh, test_a_hand_squash_folds_a_carrier_moved_after_the_lanes_fold, test_a_refresh_conflicting_only_on_the_watermark_is_resolved_by_the_fold and test_the_dispatchers_drain_refreshes_a_lane_whose_watermark_lags_the_carrier.
- Act machinery unchanged: no diff.
- Text items: present. RESYNC: one entry, present.
- "This row's own ids are reserved through its verb": a landing-time act, not yet taken. No `refs/heads/id-carrier` exists, and the watermark holds no record. It is self-enforcing, because the landing check refuses ids added with no carrier.
- Generated pages: trunk-generated.

Red-before, confirmed through each fix's regression tests run on its pre-fix tree:
- 47933d624^: the hand squash refuses another lane's number after that lane landed; the slot and the squash each refuse a retired id re-authored inside the lane's own reservation; the drain refreshes a lane whose watermark lags the carrier; the retired-in-own-record row. 5 failed.
- ea084509f^: the slot lands a code-only lane after trunk deletes an id the lane was based on; the claim-folder reader. 2 failed.
- e5ecf9d7c^: the export-ignore cases on both the sweep and the slot; the carrier contributes only its records; a lane behind trunk commits through the floor; a registry conflict beside the watermark refuses. 5 failed.

The trace.py ratchet bump (3741 -> 3852) is reasoned per step, and the bulk of the new logic lives in id_carrier.py. I judged it acceptable against S5.

Coverage-extension note (no severity): `trace.py --fold-ids` run while a registry is still conflicted stops on the sweep's own exit instead of a Refused line. It fails closed, and the station path never reaches it, because the fold runs only when the watermark is the sole conflict.

Commands:
- `git rev-parse HEAD` -> 82e4ca1a73bc48382f04522c3f71a3ac811048ad
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r4-978-B/wi-978 tests/test_id_watermark.py ... tests/test_dispatch.py` (the brief's 17 modules) -> `758 passed, 20 skipped in 1658.93s (0:27:38)`. 19 of the skips are gated on posix-shell.
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (986 work item(s), 872 done (88%), 34 cancelled, graph acyclic).` exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=138 LLR=329 TC=356 orphans=0 integrity=0 ...` exit 0
- `python -m pytest -q -n 2 tests/test_pre_commit_hook.py`, with C:\Program Files\Git\bin on PATH to satisfy the posix-shell gate -> `31 passed in 114.23s`
- Red-before, run on a `git archive` export of 47933d624^ with 47933d624's tests: `5 failed, 2 passed`. The 5 failures are the regression tests above; the 2 passes are pre-existing matches of the -k filter.
- Red-before, run on an export of ea084509f^ with ea084509f's tests: `2 failed`.
- Red-before, run on an export of e5ecf9d7c^ with e5ecf9d7c's tests: `5 failed, 1 passed`.
- `python r4-978-B/probe_forged.py r4-978-B/probe1` (drives trace.landing_id_refusal, watermark_findings and reserve_ids on a real repository and linked worktree) -> `row-1 landing check: None`; `integrity findings at that commit: []`; `carrier records: ['# reservation: SR 3-3 (WI-001)', '# reservation: TC 4-4 (WI-001)']`; `landing check for re-added SR-003: None`.

- [MINOR] project-trajectory/scripts/id_carrier.py:486 -> two pieces combine here. First, `landing_lines` returns early when no id is added, so landing-table row 6 (a record that neither the carrier nor the parent holds) is never judged on a code-only landing. Second, `reserve` (id_carrier.py:372) folds trunk's records into the carrier. A record line that no reservation wrote, landed on a code-only lane, therefore becomes carrier authority at the next reservation. The probe drove the chain: a lane re-added the freed SR-003, and the landing check returned None. The spec's S3 places a hand edit of a reservation line outside the promise, hence MINOR. The spec's table also leaves row 1 vs row 6 precedence ambiguous (K1). -> have `reserve` take records from the carrier tip only, never from trunk's watermark (trunk's marks still floor the range). This deletes the path by which a tree's record becomes allocation authority, so the bad state becomes unrepresentable and no new guard is needed. Alternatively, judge row 6 before the no-ids early return. -> @owner
- [MINOR] project-trajectory/RESYNC_PACK.md:10281 -> the entry discloses a forced change for "a repository without lanes": a `git merge --squash` of an unclaimed branch whose staged tree adds registry ids is refused. The spec's Done-when for the RESYNC item says "a trunk-only repository is unaffected". The code follows the spec's landing table (row 5, unreadable claim, refuses), so the spec contradicts itself and the RESYNC entry honestly reports the wider effect. -> the owner rules which one stands, and the Done-when/S3 text is amended to match. The RESYNC wording already describes the built behavior. -> @owner
- [MINOR] docs/test/test-cases.toml:1608 -> TC-402's evidence cites eight tests. None of them drives a refusal, yet its Expected promises that each unreserved, other-work-item, reused, carrierless, unreadable-claim and landing-only-record case refuses. The tests that discharge those cases exist and pass but are not cited (test_the_slot_refuses_each_unreserved_landing, test_the_hand_squash_refuses_each_unreserved_landing, the *_unreadable_claim and *_retired_id_* cases). (K1) -> add them to TC-402's evidence, or cite tests/test_id_landing.py whole, as TC-401 does for test_id_carrier.py. -> @owner
- [MINOR] project-trajectory/scripts/id_carrier.py:483 -> several functions implement LLR-363's landing rule but carry `Implements: SR-174, LLR-362`: `landing_lines`, `landing_refusal`, `_read_landing`, `_added_ids`, `_outside_lines`, `_retired_lines`, `ids_at` and `rev_fold_lag`. LLR-362's code_symbol (low-level-requirements.toml:3749) also lists `landing_lines`. LLR-363's module (low-level-requirements.toml:3760) omits id_carrier.py, so the landing judgement's code does not trace to the landing LLR (K3). -> add id_carrier.py to LLR-363's module. Retag those functions LLR-363 and move `landing_lines` and `landing_refusal` into LLR-363's code_symbol. -> @owner
- [MINOR] docs/requirements/system-requirements.toml:995 -> for clarity: SR-174's title still reads "Work-item identity is allocated once and never re-issued". The amended requirement now covers every identity the content mints, including the registry identities lanes reserve. The rationale also gains SN-027 in sn_refs without stating how the row contributes to it; it still argues only SN-025 (K1). -> widen the title to the row's scope (e.g. "Identity is allocated once and never re-issued") and add one rationale sentence on the SN-027 contribution. Both go through the row's authority at the next sitting. -> @owner
- [MINOR] project-trajectory/scripts/kitlib/git.py:427 -> `write_blobs` materializes a revision's paths into a scratch directory blob by blob, built so that no export attribute can hide a registry. rejudge.py:282 `_extract` does the same in intent through `git archive`, which keeps the exposure write_blobs was built to avoid. The lane's history shows a consolidation onto a shared extractor that was later reverted (PROCESS.md §3, consolidate, don't duplicate). -> file a consolidation row on trunk that routes rejudge's snapshot through `write_blobs` (returning the links it skips). It is outside this diff's scope, so this is a separate finding, not an inline fix. -> @owner

VERDICT: APPROVE findings=6
