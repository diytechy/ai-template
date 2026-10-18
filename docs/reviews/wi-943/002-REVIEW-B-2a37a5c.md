Reviewed: 2a37a5c0486fc070b922df5cf9e84827e386e985

**Verified.** The worst failure class this change admits is fail-open: an unblessed MEANING re-attestation admitted at the merge slot, or the act derivation and the merge disagreeing about what a verdict authorizes. A secondary class is a regression that refuses a legitimately backed act (CLARITY, APPROVE, or a held-rung CLARITY act). I hunted both and found neither.
- `kitlib.sitting.judged_rows` now admits an amendment MEANING row only when `kitlib.verdict.blessed_rows` returns it. That reader drops a row also tagged `[MEANING]` or `[CLARITY]`. Its two callers both read it: `uncovered_refusal`, unioned over `branch_verdicts`, and `_named_line`/`unaccepted_refusal`.
- `adjudicate_act._authorized` filters through the same set, and `_arm` lost its `blessed` argument. Grep finds `blessed_rows` only in `kitlib/verdict.py` and `kitlib/sitting.py`. No other module restates `("MEANING", "CLARITY")` as authorizing.
- I wrote an in-process probe (scratch `probe.py`) that feeds the real `accepted()` parser a combined sitting. The amendment section holds plain MEANING, MEANING+BLESS, CLARITY, a double-spaced bless tag and a misspelt `[MEANING + BLESS]` tag; the first-approval section holds APPROVE and RETURN. `judged_rows` returned only SR-002 (blessed), SR-003 (CLARITY) and the APPROVE rows. Both malformed tags authorized nothing (fail closed). `_authorized` on a released rung listed the same rows, and on a held rung only the CLARITY row. So the derivation's output is unchanged and agrees with the floor.
- **Red before the fix.** I took the tip's tree (git archive into scratch) and swapped in the base `b120c472` copies of `sitting.py`, `adjudicate_act.py` and `acceptance_record.py`. All 9 new or changed tests failed: the merge-slot cases returned `None` (admitted), and `_arm()` raised a TypeError for its missing `blessed` argument. The 35 pins and held-rung tests in the selection passed on the old code. On the tip, both modules pass in full.
- **Spine and text.** The LLR-310, LLR-278, LLR-338 and TC-278 cells carry the spec's quoted amendments exactly. Status is unchanged and the parent SRs are untouched (K3). The `Implements:` tags match their LLR modules and code_symbols. TC-278's evidence names all seven new snapshot-reader tests, and TC-368's evidence names the two new act tests. IF-287's sentence matches `docs/interface-reference.md`.
- **Byte-watched files.** `PROCESS_OPTIONS.md` grew by exactly 70 bytes (199,426 → 199,496), as the byte-budget-guard re-stamp records. That skill is 4,509 bytes, matching its own stamp.
- **Copies.** The three byte-budget-guard copies are byte-identical, and so are the three recipes copies.
- **RESYNC entry** is present and anchored at the lane base.
- **Sweep.** SR-228 (held: CLARITY only) and SR-232 (preserve each kind's decision grammar) agree with the narrowed rule. PROCESS.md §5's held-rung text and PROCESS_OPTIONS' table row (a meaning row re-attested only when the verdict blesses it) agree too. Nothing contradicts.

**Done-when coverage map.**
- Plain MEANING refused, scoped and unscoped: `test_a_released_plain_MEANING_reattestation_is_refused_naming_the_row_and_the_mark[scoped|unscoped]`. Red before.
- A row tagged two ways is refused: `test_a_released_row_tagged_two_ways_is_refused[bless-and-clarity|bless-and-meaning]`. Red before.
- A combined act is refused whole: `test_a_combined_act_carrying_a_plain_MEANING_reattestation_is_refused_whole`. Red before.
- A named verdict is refused: `test_a_named_verdict_ruling_the_row_plain_MEANING_is_refused_naming_the_verdict`. Red before, and it was admitted (`None`).
- Pins: `test_a_released_MEANING_BLESS_reattestation_merges`, `test_a_named_verdict_blessing_the_row_merges`, `test_a_combined_act_with_a_blessed_reattestation_merges`, and `test_a_held_rung_*`. All pass before and after.
- One home: `test_the_bless_mark_has_one_reader_shared_by_the_merge_and_the_act` and `test_judged_rows_admits_an_amendment_MEANING_row_only_with_its_bless_mark`. Red before. The arm test's bless half moved to a verdict-text case through `_authorized`, and the bless and derivation tests are unchanged.
- The text and `RESYNC_PACK.md`: confirmed by inspection, as above.
- The spine: the text is in place. The checkpoint sitting's judgement is not on this tip. That is expected at a counted round, which precedes the checkpoint (coordinator-cycle §3), so it is not a finding.
- The landing-tip commit bar: not run, by the round facts.

**Note, not a finding.** `uncovered_refusal` unions authorization across every accepted verdict in the branch. So an earlier verdict's `[MEANING+BLESS]` still backs a row that a later re-sit rules plain `[MEANING]`, when the act names no verdict. That is a pre-existing property, and this range does not widen it.

**Commands**
- `git rev-parse HEAD` -> `2a37a5c0486fc070b922df5cf9e84827e386e985`
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../wi943-r1-opus/wi-943 tests/test_adjudicate_act.py tests/test_snapshot_readers.py` -> `100 passed in 247.36s (0:04:07)` (0 environment-gated skips)
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (942 work item(s), 826 done (88%), 30 cancelled, graph acyclic).`
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=131 LLR=304 TC=318 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=3.`
- Pre-fix red check (scratch tree, base copies of the 3 scripts), the same two modules with `-k "MEANING or bless or two_ways or plain or arm or judged_rows or combined or named_verdict or held_rung"` -> `9 failed, 35 passed in 111.85s`. The 9 are exactly the new or changed tests.
- `python -I probe.py` (scratch) -> the judged and authorized sets quoted above.

- [MINOR] project-trajectory/scripts/kitlib/sitting.py:727 -> Two message defects. (1) The row line still says "SR-001 (amendment) is judged by no accepted verdict". For the case this change adds, that is untrue: the row IS judged, plain MEANING, but unblessed. The spec's deliverable 1 says the lines read "authorized by no accepted verdict". (2) `_BLESS_REMEDY` is appended unconditionally, here (sitting.py:730) and in `unaccepted_refusal` (sitting.py:668). So a refusal over a first-approval row alone, or over a verdict that is simply not accepted, tells the operator to "re-sit that row" for a MEANING bless mark that is not involved (rubric K1/B1, confirmed by reading `tests/test_integrate_admission.py:569`'s first-approval refusal path). -> Word the line "is authorized by no accepted verdict" and update the one wording assertion at tests/test_integrate_admission.py:569. Append `_BLESS_REMEDY` only when an unauthorized row's kind is `amendment`. This is message wording, not a guard, so no unrepresentability clause is owed. -> @owner
- [MINOR] docs/test/test-cases.toml:2830 -> For clarity (K1). TC-278's Method keeps "a named verdict must itself be accepted and judge each row its act re-attests", and its Expected (docs/test/test-cases.toml:2832) keeps "a named verdict judges each row it re-attests". The amended LLR-278 now reads "must also authorize every row its act re-attests in the same way". A plain-MEANING named verdict does "judge" the row, so the general sentence understates the new rule, which only the added Method sentence states. -> At the checkpoint sitting, amend both phrases to "authorize ... in the same way", matching LLR-278. -> @owner

VERDICT: APPROVE findings=2
