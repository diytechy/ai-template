Reviewed: 6d852f18e53122292f09b91a3cac0e57384728cb

Verified. Full-lane review, convergence stance, of 1b4d9d7af...6d852f18e (the lane's merge base is the current trunk 1b4d9d7af), against WI-929's spec and the kit-change-review rubric (K1-K4, B1). Worst failure classes this change admits, hunted in order: (1) fail-open at the merge gate or filing boundary, where a review VERDICT line with a repeated count is read as a verdict; (2) silent wrong content, where an adjudication line with a repeated field reads one copy; (3) a stale consumer that still unpacks a three-tuple or expects the old reason.
- (1) I drove the shipped `kitlib/sitting.review_line` at the base and at the tip, both loaded from real module copies. At the tip, `findings=7 findings=0`, `findings=0 findings=0`, `findings=0 findings=` and `findings= findings=0` are all refused with "is not exactly `VERDICT: <APPROVE|CHANGES-REQUESTED> findings=<digits>`". Lowercase keywords, trailing tokens and second VERDICT lines are refused as before. `VERDICT: APPROVE findings=0` is still accepted. No path fails open: the exact-form comparison at sitting.py:395 rebuilds a one-count canonical line, so a repeated count can never equal it.
- (2) At the tip, `_one_line` reads `VERDICT: MEANING rows=7 rows=0`, `OUTCOME: APPROVE rows=7 rows=0`, `DONE-WHEN: CLARITY changes=7 digest=7 changes=0` and `SITTING: JUDGED kinds=7 kinds=0` as their last copy. At the base each was refused "more than once". This is exactly the residue the spec states, which the owner ruled at filing (D-017; D-011 and the audit grade it contrived). It is dismissed under PROCESS.md §6 "Review threat model", and the residue is recorded in LLR-310's rationale and the RESYNC entry.
- (3) Every caller of `_machine_line`, `_incomplete` and `_machine_lines` is inside sitting.py: `_machine_lines`, `review_line`, `_one_line` and `line_refusal`. All are consistent with the two-tuple. Nothing else in the repo imports them. No other test asserts the repeated-field refusal (searched for `WI-870`, "more than once" and repeated `field=` pairs). The `score_reviews.parse_verdict` docstring still truthfully lists a "repeated" count as refused.
- Red-before. I ran the three named tests in an exported tip tree with the base `sitting.py` swapped in. `test_a_filed_coordinator_review_appears_in_the_rollup` FAILS ("Actual message: 'the review is not filed: it says `VERDICT: APPROVE` with findings more than once'"). `test_the_gate_reads_a_malformed_verdict_line_as_no_verdict` and `test_an_unusable_verdict_is_refused_and_says_which_way` pass (1 failed, 9 passed). With the tip `sitting.py` all 10 pass.
- Spine (K1-K3). The only registry lines that changed are LLR-310 detail/rationale and TC-327 method/expected. Their text matches Deliverable 4 and stays true of the code. No Status changed. TC-083 is byte-unchanged. The live LLR-310, TC-327 and TC-083 rows equal their `docs/archive/last_approved` snapshots. Act seq 128 re-attests exactly LLR-310 and TC-327. No SN or SR cell is touched, and SR-232 names no repeated-field refusal. The `Implements:` tags are unchanged. I did not read the checkpoint sitting's verdict, because the convergence stance excludes docs/decisions. The merge slot's verdict-backing check is the authority there.
- Contract (K3). The IF-287 sentence is gone from the sitting.py docstring and from docs/interface-reference.md, and the generated paragraph matches the edited docstring. The `review_line` docstring drops "named once" as Deliverable 2 asks.
- Shipping (K4). The RESYNC_PACK.md entry is present and accurate, with no migration. It is anchored `[since cd6ba3160]`, which is a trunk commit and an ancestor of 1b4d9d7af. Landing obligation, not a lane finding: cd6ba3160 is 7 bookkeeping commits behind the lane's current base. The coordinator-cycle recipe re-anchors the entry at the landing's parent, and it must do so here.
- Done-when coverage:
  - (a) No repeated-field branch, two-value `_machine_line`, no `repeated` argument: covered by inspection at sitting.py:312-345 and by the probe.
  - (b) The successors case is deleted and the review_brief expectation is "is not exactly": covered by test_adjudicate_brief.py:1543-1559 and test_review_brief.py:468, red-before confirmed.
  - (c) The gate test is unchanged and passes at the base and the tip: covered.
  - (d) LLR-310 and TC-327 are amended and TC-083 is unchanged: covered by the registry diff, the snapshot equality and act 128. The sitting itself is judged elsewhere.
  - (e) IF-287 sentence removed and reference regenerated: covered.
  - (f) RESYNC entry: covered.
  - (g) The commit bar: I did not run the smoke tier, per the round facts. `check_trajectory.py --strict` exits 0.
- Module-size ratchet: `test_module_sizes_exactly_match_the_committed_baseline` and `test_the_census_sees_inside_packages` pass on the tip tree.
- Cosmetic, below a finding: sitting.py:374, a docstring line of 93 characters, is wider than its neighbours. No lint enforces this.
- Side effect: my `trace.py --strict-integrity` run rewrote the gitignored `docs/test/report.md` in the lane worktree. That file is untracked output and leaves the lane's tree and diff unchanged.

Commands:
- `git rev-parse HEAD` -> 6d852f18e53122292f09b91a3cac0e57384728cb
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../opus/wi-929 tests/test_review_brief.py tests/test_score_reviews.py tests/test_adjudicate_brief.py` -> `140 passed in 62.84s`, exit 0. The first attempt hit INTERNALERROR because the basetemp parent did not exist. After I created the opus directory, it re-ran clean.
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (940 work item(s), 819 done (87%), 30 cancelled, graph acyclic).`, exit 0 (WARN-only advisories)
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=304 TC=318 orphans=0 integrity=0 ... interface-findings=0 ...`, exit 0
- Probe of `review_line` and `_one_line` at the base and at the tip (opus/probe.py): the outputs are as stated above.
- Red-before, three tests on an exported tree with the base sitting.py -> `1 failed, 9 passed`. With the tip sitting.py -> `10 passed`.
- `pytest tests/test_module_size_ratchet.py -k "exactly_match or census_sees"` on the tip tree -> `2 passed`
- Snapshot equality of the LLR-310, TC-327 and TC-083 live rows against the archive (tomllib) -> True, True, True. All three are Approved.

VERDICT: APPROVE findings=0
