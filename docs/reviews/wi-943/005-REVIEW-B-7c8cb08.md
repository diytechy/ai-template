Reviewed: 7c8cb0802e175544c6b2286fbca59b0ccd949acd

**Verified.** Full-lane review in the convergence stance, against the WI-943 spec
(docs/work/active/wi-943/WI-943-merge-floor-meaning-bless.md) and the rubric
docs/rubrics/kit-change-review.md. I did not read the specref target
(docs/decisions/wi-912.toml), because the convergence stance excludes everything
under docs/decisions/. The D-008 content the spec quotes was enough. The failure
classes I hunted first were these. (1) Fail-open: a plain or ambiguous MEANING
re-attestation still admitted at the merge slot, through either reader. (2)
Fail-closed regression: a blessed or CLARITY row, or a first-approval APPROVE
row, newly refused, or the act derivation's output changed. (3) Silent wrong
content: the refusal remedy, the spine rows or the RESYNC text misstating the
rule.

On (1): `judged_rows` (project-trajectory/scripts/kitlib/sitting.py:612) now
admits an amendment MEANING row only when `blessed_rows(part[2])` holds it.
`part[2]` is that kind's own section body in a combined verdict and the whole
text in a single-kind verdict (`accepted`, sitting.py:568). A row tagged two
ways reads MEANING in `row_rulings` and is excluded from `blessed_rows`, so it
authorizes nothing, whichever order its lines come in. The reader has exactly
three callers: `_named_line` (to `unaccepted_refusal`), `uncovered_refusal`
(sitting.py:721, to `backed_act_refusal`) and `adjudicate_act._authorized`.
`merge_approval_refusal` reaches both merge checks for scoped and unscoped lanes
(acceptance_record.py:968-972).

On (2): `_authorized` filters on `judged_rows` and then applies `_arm(ruling,
held)`. The result matches the old `_arm(ruling, held, blessed)` for every
(held, ruling, mark) combination. The held-rung CLARITY-only rule is unchanged.
The derivation tests pass with their expectations unchanged.

On (3): the amended text of LLR-310, LLR-278, LLR-338 and TC-278 matches the
spec's deliverable 4 word for word and holds against the code (K1). No SN or SR
cell changed (K2). No Status flipped. TC-368 changed only in its Evidence cell,
which is a traced, silent cell per `acceptance_record.SPINE_TRACED_CELLS`. The
`Implements:` tags name LLRs whose code_symbol lists the function (K3). The
sweep of the touched rows against SR-228, SR-232, LLR-158 and TC-368 found no
contradiction.

Red-before: I extracted a copy of the reviewed tree with `git archive`, put
`kitlib/sitting.py`, `adjudicate_act.py` and `acceptance_record.py` back to
their versions at b120c472, and ran the new and pin tests there. Every new
refusal test fails on the pre-fix code: the plain-MEANING tests (scoped and
unscoped), both two-ways cases, the named-verdict plain-MEANING test and the
combined-whole test all return None, that is, admitted. So do the one-reader
test, the `judged_rows` unit test and the reshaped arm test. The pins pass on
the pre-fix code: the MEANING+BLESS merges (single, named and combined) and
every `held_rung` test. This confirms the fixtures' verdicts are accepted, so
the post-fix refusals come from the bless rule and not from an invalid verdict.

Other checks:
- Only kitlib/verdict.py and kitlib/sitting.py contain `blessed_rows`.
- The coordinator-cycle and byte-budget-guard skill copies are byte-identical
  across project-trajectory/, .claude/ and .agents/.
- PROCESS_OPTIONS.md is 199,426 bytes at the base and 199,496 at the tip
  (+70), as the byte-budget-guard table records.
- The IF-287 sentence in docs/interface-reference.md matches the module
  docstring.

Done-when map:
- Plain MEANING refused at the merge, scoped and unscoped, naming the row and
  the mark: test_a_released_plain_MEANING_reattestation_is_refused_naming_the_row_and_the_mark[scoped|unscoped]
  (red before).
- Row tagged two ways: test_a_released_row_tagged_two_ways_is_refused[bless-and-clarity|bless-and-meaning]
  (red before).
- Combined act refused whole: test_a_combined_act_carrying_a_plain_MEANING_reattestation_is_refused_whole
  (red before).
- Named verdict: test_a_named_verdict_ruling_the_row_plain_MEANING_is_refused_naming_the_verdict
  (red before).
- Pins: test_a_released_MEANING_BLESS_reattestation_merges[*],
  test_a_named_verdict_blessing_the_row_merges,
  test_a_combined_act_with_a_blessed_reattestation_merges and test_a_held_rung_*
  (green before and after).
- One home: test_the_bless_mark_has_one_reader_shared_by_the_merge_and_the_act,
  confirmed by grep (red before). The arm test's bless half moved to
  `_authorized` over verdict text.
- Text, the spine and the RESYNC entry: present. Inspected above.
- The checkpoint sitting's judgement of the spine rows: the lane carries
  docs/reviews/wi-943/003-ADJUDICATE-f01e04c.md. I did not read it (excluded),
  so I did not check its content.
- Landing-tip commit bar (smoke tier): not run, as the round facts instruct.
  check_trajectory --strict and trace --strict-integrity are clean at this tip.

Coverage-extension note (not a finding): the named-verdict route over a row
tagged two ways is untested at integration level. It fails closed: `_named_line`
reads the same `judged_rows`, which the unit test
test_judged_rows_admits_an_amendment_MEANING_row_only_with_its_bless_mark pins
for SR-004 and SR-005.

**Commands**
- `git rev-parse HEAD` (wi-943 worktree): 7c8cb0802e175544c6b2286fbca59b0ccd949acd
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../wi943-gate-opus/wi-943 tests/test_adjudicate_act.py tests/test_integrate_admission.py tests/test_snapshot_readers.py`: `172 passed in 652.11s (0:10:52)`. The shell tool's 600 s cap moved it to the background; it was not re-run.
- `python project-trajectory/scripts/check_trajectory.py --strict`: `check_trajectory: clean (942 work item(s), 826 done (88%), 30 cancelled, graph acyclic).` exit 0
- `python project-trajectory/scripts/trace.py --strict-integrity`: `Traceability: SN=31 SR=131 LLR=304 TC=318 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=3.` exit 0. It rewrote the gitignored docs/test/report.md, and `git status --porcelain` stays empty.
- Pre-fix probe, from a `git archive` copy under .../wi943-gate-opus/prefix with the three scripts at b120c472: `pytest ... -k "plain_MEANING or MEANING_BLESS or tagged_two_ways or blessing_the_row or blessed_reattestation or judged_rows_admits or one_reader_shared or act_arm_follows or held_rung"`: `9 failed, 19 passed`. The failures are exactly the new refusal, one-home, unit and arm tests; the passes are the pins and held-rung tests.
- `grep -rln blessed_rows project-trajectory/scripts`: kitlib/sitting.py and kitlib/verdict.py (plus their .pyc files)

**Findings**
- [MINOR] project-trajectory/scripts/adjudicate_act.py:22 -> the module docstring still says "The other consumers of the same carrier are unchanged: the merge slot (`kitlib.sitting.uncovered_refusal` and `unaccepted_refusal`, ...)". This lane changes exactly those consumers: they now read the bless mark through `judged_rows`, which this module also reads. The sentence makes a reader think the merge slot and the act assembler still decide authorization separately -> reword it to say the merge slot reads the same `judged_rows` this module reads (it is restated correctly at line 31), and drop "unchanged" for the merge checks; for clarity -> @owner
- [MINOR] docs/test/test-cases.toml:2830 -> TC-278's added Method sentence says a row "tag[ged] MEANING+BLESS and another way, is refused naming the row, through the backing check and through a named verdict alike". The Evidence lists only test_a_released_row_tagged_two_ways_is_refused, which names no verdict (`_amendment_act` with `verdict=None`), so the named-verdict half of that claim has no integration evidence (K1) -> add a named-verdict case to the two-ways test, with `_amendment_act(..., verdict=<two-way text>)` asserting "does not authorize SR-001", or narrow the sentence so "through a named verdict alike" covers only the plain-MEANING case -> @owner

VERDICT: APPROVE findings=2
