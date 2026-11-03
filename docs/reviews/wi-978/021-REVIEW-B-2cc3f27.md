Reviewed: 2cc3f279ae8d6c8a0da6d14bb1c3c63b455fc400

## Verified

Convergence stance, full-lane range 2f4ebb2a5..2cc3f279a, read against the WI-978 spec (S3 tables, Trust consumers, Done-when), PROCESS.md §4/§6, and the rubric docs/rubrics/kit-change-review.md (K1-K3, B1). I read no earlier verdict, no decision record and no lane commit message. I found the pre-fix code through `git log --format=%h` and `git archive <fix>^`.

Failure classes I hunted first: (1) fail-open at landing, where an unreserved, stale-base or another lane's id lands; (2) collision, where two reservations get overlapping ranges; (3) data loss, where a record or mark is dropped by a writer, a fold, a merge or a rebase; (4) the hand-raise floor turning red on routes the kit itself drives.

- Real flows, driven by me in a scratch repository with the shipped CLIs (probe/e2e.py):
  - Lane A reserved SR=2 and lane B reserved TC=1,SR=1. They got disjoint ranges (SR 6-7, SR 8-8, TC 4-4).
  - Both lane commits passed `--strict-integrity`.
  - A's hand squash ran the `reserved-ids` step. It refused the lagging staged watermark, naming the B records and the `--fold-ids` remedy. After the fold it passed.
  - B's merge of trunk conflicted on the watermark. `--fold-ids` resolved it, and the floor stayed at 0.
  - B's squash passed. The trunk floor stayed clean, and trunk's watermark holds all three records with SR=8.
  - A stale lane C that authored A's SR-006 failed closed at the squash step.
- This lane's own landing: `trace.landing_id_refusal(HEAD, merge-base, ["WI-978"])` returns None, and `landing_fold_lag(HEAD)` returns []. The carrier holds LLR 362-363 and TC 401-402 for WI-978. The same call keyed on WI-963 refuses all four ids by name.
- Every fix confirmed red on its pre-fix code. I exported each fix commit's tests over its parent's scripts and ran them:
  - 7fd6f6c56: 3 of 4 new cases fail pre-fix. The fourth is an adequacy witness meant to pass.
  - 88c51caf4: 5 of 5 fail pre-fix.
  - ff21d5c24: 5 of 6 fail pre-fix. The sixth is a renamed, pre-existing lag case.
  - 76b8189ff: 2 of 2 fail pre-fix.
  - d3cfb73d6 and 7a21763d3 change no behaviour and have no tests. For 90faabf05 (the prompt text), I checked the corrected text at scripts/coordinator/terra-spine-prompt.template.md:14-17. mkprompt refuses an unfilled @RESERVED@.
- K3 (Implements tags): I mechanically checked every added or changed function in the six touched scripts (probe/k3.py). Each `Implements:` LLR's `module` names its file, and each `code_symbol` names its function. The checker reported no gaps.
- K2: the amended SR-174 names no implementation carrier. The LLR and TC rows name only the watermark artifact and test evidence.
- Shipped and dogfooded copies of coordinator-cycle and byte-budget-guard are byte-identical (`diff -r` across the three copies).
- The act ledger, baseline_snapshot.py and their tests are untouched in the range.

Done-when coverage map:
- Spine rows: SR-174, LLR-362/363, TC-158/401/402 and IF-101 are present. check_trajectory is clean.
- Reserve verb table: test_id_carrier.py COUNT_REFUSALS, WI_REFUSALS and CLI_REFUSALS, plus the usage-error case.
- CAS and first use: test_id_carrier_git first_reservation and lost_race (both moved and first-use).
- Disjoint sequential, stale-base and post-correction ranges: three test_id_carrier_git cases.
- Fold on a clean and on a conflicted file: the fold units and test_fold_ids_on_a_conflicted_watermark.
- Hand-raise, record append-only, bump/correct keep records, no correction misread: eleven new test_id_watermark cases.
- Landing table on both callers: test_id_landing REFUSED x {slot, squash}, plus the unreadable-claim, code-only, stale-base and retired cases.
- Landing and refresh fold: slot_folds, hand_squash_folds, drain and refresh_conflict.
- Act ledger untouched: no diff.
- PROCESS.md §4 text: present at project-trajectory/PROCESS.md:681, beside the CLARITY paragraph. The byte-budget row was restamped (+457).
- spine-questions §0 citation, Terra prompt and recipes §4/SKILL §4: present, and pinned in test_prompts.py.
- RESYNC entry: present. It goes further than the spec: it discloses that a lane-less repository's `git merge --squash` of an unclaimed branch that adds registry ids is now refused. That is a forced change, but it is stated.
- Generated pages: cli-reference and interface-reference are trunk-owned `[generated]` views, regenerated at landing. CATALOG.md was regenerated in the lane.
- Strict lints: clean (Commands below).

Requirement and interface counterparts:
- SR-174, the changed side. Counterparts are SN-025 and SN-027, newly cited (parallel lanes, a fit). Its users are LLR-153, LLR-154, TC-147, TC-148 and TC-158. Decision: retain them. They read the work-item half, which still holds. TC-147/148's "Satisfies SR-174 AcceptanceCriteria" wording now over-claims (finding 2).
- IF-101, the changed side (data, requestors). Owner trace.py exports reserve_ids, fold_watermark, landing_id_refusal and landing_fold_lag. The requestors integrate.py and check.py call them. Decision: carry the change, confirmed in code. Counterpart TC-158 still cites a mint clause IF-101 no longer states (finding 3).
- IF-224, the changed side (data, notes). trace.py's deferred `agent_common.trunk_name`/`parse_wi_id` imports are in check_work_item and _trunk_name. Decision: carry the change, confirmed.
- Decomposition of SR-174 into the new children:
  - LLR-362 is the allocation authority: carrier, record, fold and hand-raise.
  - LLR-363 is the landing admission plus the landing and refresh fold.
  - They are independent decisions: one decides who may hold a number, the other whether a landing may bring one. Each has its own TC (TC-401, TC-402).
  - Splitting the fold out of LLR-362 would add no independent value, because the fold is the record's only copier and shares its grammar.
  - Splitting the squash caller from the slot would add none either, because the spec requires one check with two callers.

Coverage-extension note (no severity): when the hand squash runs `git write-tree` over an unresolved registry conflict, the `reserved-ids` step fails closed with "the staged squash's tree cannot be written". I observed this with lane C.

## Commands

- `git rev-parse HEAD` (worktree) -> 2cc3f279ae8d6c8a0da6d14bb1c3c63b455fc400
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../gate2-B/wi-978 <the 17 declared modules>` -> `762 passed, 20 skipped in 1848.02s (0:30:48)`. 19 skips are posix-shell environment-gated.
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (986 work item(s), 872 done (88%), 34 cancelled, graph acyclic).` exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity`, run on a `git clone -s` of the reviewed commit in scratch, because the run rewrites docs/test/report.md and must not touch the worktree -> exit 0, `Traceability: SN=31 SR=138 LLR=329 TC=356 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=2.`
- `python project-trajectory/scripts/trace.py --strict` (same clone) -> exit 0, same summary line
- probe/own_landing.py (this lane's landing check and fold lag, in the worktree, read-only) -> `refusal: None`, `lag: []`
- probe/e2e.py (two lanes plus a stale lane through the real --reserve-ids, --fold-ids and check.py reserved-ids step) -> outcomes as stated above
- Pre-fix regression runs on `git archive` exports (pre-7fd6f6c56, pre-88c51caf4, pre-ff21d5c24, pre-76b8189ff) -> `3 failed, 58 passed`; `5 failed, 56 passed`; `5 failed, 1 passed`; `2 failed`
- probe/k3.py (Implements tag vs LLR module/code_symbol, every added or changed function) -> no output (clean)
- `id_carrier.landing_lines(set(), [], ['WI-401'], [('SR',900,999,'WI-401')], [], True, 'x')` -> `[]` (finding 1)

## Findings

- [MINOR] project-trajectory/scripts/id_carrier.py:492 -> `landing_lines` returns before its landing-only-record check when the landing adds no id. A code-only landing whose watermark carries a record neither the carrier nor the parent holds therefore passes, observed: `landing_lines(set(), ..., landing_records=[('SR',900,999,'WI-401')], ...) == []`. That record then sits on trunk as a committed, append-only record that justifies a hand-raised mark. The spec's landing table (row 6) and LLR-363 list that refusal without an "ids added" qualifier. The path is reachable only through a hand-written record, which S3 places outside the promise, so it is MINOR (anchor K1) -> run the record check ahead of the `if not added` early return, or state in LLR-363 that a code-only landing's records are not judged -> @owner. The landing is the trust boundary that admits lane content, so this is validation at its one owning boundary and no unrepresentable-clause is owed.
- [MINOR] docs/test/test-cases.toml:1463 -> for clarity: TC-147 (and TC-148 at :1474) still says "Satisfies SR-174 AcceptanceCriteria via the LLR-153/LLR-154 detail contract". The amended SR-174 acceptance now adds three reservation clauses that these TCs do not exercise; TC-158/401/402 do. Read literally, the cell over-claims. The kept-id cross-reference that PROCESS.md §4 "Keep or mint" requires should have caught this wording (anchor K1) -> reword both cells to "Satisfies SR-174's work-item clauses via ..." -> @owner
- [MINOR] docs/test/test-cases.toml:1582 -> for clarity: TC-158's method still says "Covers the mint seam IF-101 declares: next_wi_id counts from the mark". The amended IF-101 data (docs/requirements/interfaces.toml:1388) dropped "a mint counts from max(mark, live) + 1", so the TC cites a clause its interface no longer declares. The counting rule now lives only in LLR-153's detail (anchor K1) -> keep the counting clause in IF-101's data beside the new calls, or point TC-158's method at LLR-153 -> @owner
- [MINOR] project-trajectory/scripts/trace.py:1301 -> `_reserved_highs` repeats, line for line, the per-space highest-`high` loop that `id_carrier.carried` already runs (project-trajectory/scripts/id_carrier.py:234-236). Two homes for "the highest number a record reserves per space" can drift between the hand-raise floor and the fold (PROCESS.md §3 "Consolidate, don't duplicate"; anchor K1) -> expose one `reserved_highs(records)` in id_carrier and call it from both -> @owner
- [MINOR] project-trajectory/scripts/integrate.py:2708 -> `_fold_watermark_conflict` and `_fold_carrier_in` (:2732) each run `trace.fold_watermark(wt)` and then `git add -- WATERMARK`, each with its own failure mapping. The fold-and-stage step therefore has two copies in one module (PROCESS.md §3) -> extract one `_fold_and_stage(wt)` returning a refusal or None, and have both callers map it -> @owner
- [MINOR] project-trajectory/scripts/id_carrier.py:368 -> "the watermark text at a revision" is read in four spellings: the inline `git show <trunk>:docs/id-watermark` here, `carrier_text` (:298, None on absence), `_watermark_at` (:515, "" on absence), and trace.py's inline show in `_baseline_texts` (project-trajectory/scripts/trace.py:1405). integrate.py:262 also re-declares the path that `id_carrier.WATERMARK` owns. Each copy chooses its own absent-file value (PROCESS.md §3) -> keep one `watermark_at(root, rev)` in id_carrier with a single absence contract, call it from the other three sites, and have integrate read `trace.WATERMARK` / `id_carrier.WATERMARK` -> @owner

VERDICT: APPROVE findings=6
