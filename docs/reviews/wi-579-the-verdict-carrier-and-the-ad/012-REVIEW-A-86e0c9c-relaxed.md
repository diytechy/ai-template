# WI-579 — REVIEW-A round 012 (reviewed `86e0c9c`, relaxed)

Scope: `git diff contract_split...HEAD` excluding session telemetry, verdict
records and generated artifacts. Requirement surface read: the archived spec
`docs/archive/work/complete/WI-579-the-verdict-carrier-and-the-ad.md` (Done-when,
including the quoted WI-558/559/560 items), `LLR-140`, `LLR-207`, `LLR-208`,
`IF-046`, `IF-047`, `IF-175`, `TC-205`, `TC-206`, `docs/process.toml
[attestation]`, `docs/stack.ini`, `RESYNC_PACK.md`, `docs/enforcement-audit.md`
and `PROCESS_OPTIONS.md` "The LLM-gate verdict protocol".

## Instruments (run here, once each)

- `python project-trajectory/scripts/check.py --jobs 0` → `RESULT: PASS`
  (`verdict-rollup` SKIPs with its `_TRUNK_FRESHNESS_STEPS` siblings: "work
  branch 'wi-579-the-verdict-carrier-and-the-ad' — generated freshness is the
  trunk lane's").
- `python project-trajectory/scripts/trace.py --strict-integrity` →
  `Traceability: SN=27 SR=76 LLR=190 TC=189 orphans=2 integrity=0
  verified-mechanized=72 ... interface-findings=0 provenance-findings=1
  paraphrase-advisories=3. Report -> docs/test/report.md`.
- `python -m pytest -q -n auto -m smoke` → `1504 passed, 8 skipped in 27.31s`;
  `python scripts/check_smoke_budget.py --mode enforce` → `smoke wall-clock
  budget: 28.9s vs 60s budget -> within` (1512 collected against the re-stamped
  `max-tests = 1560` — the re-stamp's own figures reproduce on this box).
- `python -m pytest -q tests/test_verdict_record.py tests/test_integrate_admission.py
  tests/test_check_lane.py` → `104 passed in 27.91s`.

## What was driven, not read

- **The live branch, through the shipped readers.** `governing_rev` →
  `86e0c9c4` (it walks past the `2bd072a3` telemetry tip, so the finding-5 peel
  works in production); `logged_rounds` finds rounds 002 and 007 through the
  session-log join; both name superseded trees, so `round_entries` is correctly
  empty and no stale APPROVE governs.
- **The trailer writer, replayed on real history.** `format_branch_trailer` at
  `8b14670b` emits `Review-Verdict: CHANGES-REQUESTED rounds=1 tree=454f8fae…`,
  and `tree_identity('01fe742') == tree_identity('8b14670b')` — the writer and
  the gate agree on the round-007 evidence. (No trailer is on `abe8e00b`
  itself; that commit was made by a loop process started before the writer
  landed, not by a defect in it.)
- **The regression test's pre-fix behaviour.** With `kv.governing_rev` bound
  back to `kv.work_tip`,
  `test_a_record_commit_stacked_on_a_refresh_does_not_bury_the_peel` FAILS
  (`tests/test_verdict_record.py:505`) — the finding-5 test is a real
  regression test, not a restatement.
- **A hand-built git history for the peel**, `refresh` commit + coordinator
  commit, run through `refresh_attestation` / `_record_only` /
  `governing_rev` / `governing_identity` (see finding 1).

Done-when coverage: WI-558 DW1 → `logged_rounds` +
`test_an_implementer_authored_file_in_the_review_path_is_not_a_round`; DW2 →
`branch_trailers` / `_round_refusal` + the four trailer tests; DW3 →
`gen_verdict_rollup.py`, `docs/stack.ini [generated]`, `check.py verdict-rollup`
in the hook floor and `_TRUNK_FRESHNESS_STEPS`, `trunk_step.py --regen`, TC-206;
DW4 → `_legacy_rollup_refusal` + `RESYNC_PACK.md` (two entries) +
`test_the_legacy_rollup_path_warns_while_it_clears`; DW5/WI-560 DW1/WI-559 DW2 →
`test_the_review_owed_derivation_and_the_gate_share_one_definition`,
`test_the_dial_decides_when_an_adjudication_owes_a_round`,
`test_the_done_banner_states_the_rounds_it_actually_drew`. Dial, template row,
enforcement-audit rows and RESYNC_PACK entry all present. Nothing UNCOVERED.

## Findings

- [MAJOR] `project-trajectory/scripts/kitlib/verdict.py:386` -> `_record_only` answers False for any commit git reports no paths for, so `governing_rev` STOPS its walk at a zero-path commit — and `agent_common.commit_telemetry` (line 2535, this diff) newly creates exactly that shape, committing `--allow-empty` whenever a `Review-Verdict:` trailer must land on unchanged bookkeeping. Driven on a real history: a genuine `Bar-Green` refresh commit with one EMPTY trailer telemetry commit stacked on it gives `_record_only -> False`, `governing_rev != work_tip`, and `governing_identity != identity at the work tip`, while the identical case with a NON-empty record commit peels correctly — i.e. the finding-5 defect (an honest APPROVE parked at a supervisor stop because a coordinator record commit buried the refresh) survives for the empty variant, and `commit_telemetry`'s own docstring asserts the opposite ("an empty commit changes no tree, so it cannot disturb the very identity the trailer names"). `test_a_record_commit_stacked_on_a_refresh_does_not_bury_the_peel` uses a non-empty record commit and does not reach it. This asks for no new guard and CAN be made unrepresentable, which is the change to make (the `antidote` skill's "smallest change that makes this fix unnecessary"): make `governing_rev` walk through any commit whose non-record fold EQUALS its first parent's — that is definitionally "a commit that cannot invalidate a verdict", it is already computable from `tree_identity`, and it deletes the path-classification code path along with its empty-commit and merge-commit special cases rather than adding a case to it; then correct the `commit_telemetry` docstring's claim and cover the empty carrier beside the non-empty one in TC-205 -> @owner
- [MINOR] `project-trajectory/PROCESS_OPTIONS.md:566` -> for clarity: the bolded normative sentence "**The consequence for a lane is unchanged: every commit after an APPROVE buys another round**" is unqualified, and is false under the rule stated seven lines above it in the same paragraph — a commit touching only `docs/reviews/`, `docs/log.d/` or `docs/iteration/` does NOT buy another round, which is the entire point of `RECORD_PREFIXES` and the WI-547 double-identical-round class this row exists to close. An adopter (or a lane) reading the bolded claim gets the pre-OI-76 rule from the very passage that retires it. Qualify it to "every commit that changes the non-record tree" -> @owner

VERDICT: CHANGES-REQUESTED findings=2
