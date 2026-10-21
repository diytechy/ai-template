Reviewed: c033a989063844f621fac36c58e3208c5b756765

Verified. `git rev-parse HEAD` in the lane printed the reviewed commit. Failure classes I looked for, worst first: fail-open, meaning a brief rendered over a tip with no matching verified `review` record, or a walk that steps past a commit changing work; silent wrong content, meaning a digest the producer and consumer compute differently; and a refusal that hides its cause. I read the full-lane diff (kitlib/verdict.py `read_bar_attestation`/`_identity_step`/`review_attestation`/`_review_record_answer`, review_brief.py `_review_bar_refusal` and its call before `render_review`, the IF-288/IF-289 contract docstrings, the three byte-identical skill copies, SR-241/LLR-341/TC-371/TC-372, IF-175, RESYNC_PACK) against the WI-957 spec. The gate fails closed everywhere I checked. `_identity_step` is the code `governing_rev` already ran, now extracted, and `governing_rev` keeps its behaviour, so the two walks share one step (§3 consolidation is met). A git read that answers None ends the walk with a refusal. The first verified record decides, and another bar or another digest refuses. The walk never peels a refresh commit and never runs the bar. `tests_digest` is the one digest home and normalises order, `./` and backslashes, which I confirmed through the producer-consumer test.

I drove the real path on the lane itself: `kverdict.review_attestation('.', c033a98, <the round's four tests>)` returned `('c033a98…', None)`, a verified `bar=review` record over the tip's own tree and parent. Red-before: I extracted the tip into the scratch directory, put back the base (638524428) review_brief.py, kitlib/verdict.py and both skill texts, and ran the four named modules: 14 failed, 132 passed. Every new or changed WI-957 test failed (all of TC-371's cases, TC-372's pin, and the two in-process CLI tests whose stub targets the new symbol).

Mutation probe on the tip's code in scratch: I dropped the cause text from the no-step refusal and the "not a `review` one" half from the other-bar refusal. Only the three cause-asserting parametrised cases failed, so 14 passed. The tests below that should have caught these mutations are findings 1 and 2.

Done-when map:
- no attestation: `test_a_tip_with_no_attestation_refuses_naming_the_attest_command` (cause not pinned, finding 1).
- another tree / another parent / older grammar: `test_an_attestation_that_does_not_name_the_tip_refuses_naming_the_cause[*]`.
- landing: `test_a_landing_attestation_refuses_naming_both_bars` (the review half not pinned, finding 2).
- other digest: `test_a_review_attestation_for_other_tests_refuses_naming_both_digests`.
- matching record renders: `test_a_matching_review_attestation_renders_and_names_it`, plus `test_the_review_render_accepts_what_attest_writes` through the real attest producer.
- record-only commits above: `test_record_only_commits_above_the_attested_one_render`.
- work commit above: `test_a_work_commit_above_the_attested_one_refuses[src/app.py, docs/decisions/...]`.
- skill/recipes text: `test_the_cycle_reviews_only_an_attested_tip` (it passes, all three copies are byte-identical, and no copy keeps "`git log -1` moved").
- landing-tip lints: check_trajectory --strict is clean and trace integrity=0. The smoke commit bar was not run, as this round's facts direct.

Relationship decisions:
- IF-175 (owner kitlib/verdict) gains requestor scripts/review_brief and the review-walk datum. The counterpart, review_brief's `kverdict` call, carries it. review_brief already imported kverdict at base, so this also repairs an omitted requestor.
- IF-288/IF-289: the contract body (docstring) states the refusal and its exit 2. The data cells are unchanged, which is justified: the argument surface and the exit-code set did not change. The external:coordinator counterpart is updated through SKILL §3 and recipes §1/§4/§6.
- SN-004/SN-008 are retained unchanged under the labelled derived SR-241.
- LLR-341 is the one coordinator child, with TC-371 (behaviour) and TC-372 (cycle text). Splitting it further would add no independent decision, since WI-958 takes the loop's LLR under the same SR.

Sweep of the new rows against SR-235, SR-156 and LLR-207: no contradictions. SR-241 names no carrier (K2), and the Implements tags match LLR-341's module and code_symbol (K3).

Notes, not findings:
- The verification logic LLR-207 (Approved) describes now lives in `read_bar_attestation`, tagged only to LLR-341. `bar_attestation` stays the LLR-207 symbol as its projection, so K3 holds, but a later edit to the grammar check traces to LLR-341 alone.
- A refresh tip whose non-record identity equals the attested commit beneath it is refused as another bar. This fails closed and is by design.
- Trunk's WI-968 (attest cannot find .venv in a linked lane worktree) is not in this lane's `needs`. Landing this gate before it would make every lane's review render refuse. The lane's decisions record holds the lane for it, but the spec of record does not, and the spec is outside this diff.

Commands:
- `git rev-parse HEAD` -> c033a989063844f621fac36c58e3208c5b756765
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../l8-r957-b/wi-957 tests/test_integrate_attest.py tests/test_prompts.py tests/test_review_brief.py tests/test_review_brief_git.py` -> 146 passed in 70.86s
- `python project-trajectory/scripts/check_trajectory.py --strict` -> check_trajectory: clean (964 work item(s), 847 done (88%), 33 cancelled, graph acyclic).
- `python project-trajectory/scripts/trace.py --strict-integrity` -> Traceability: SN=31 SR=133 LLR=308 TC=329 orphans=0 integrity=0 ... interface-findings=0 ac-advisories=1 paraphrase-advisories=2.
- red-before (scratch copy of the tip, base review_brief.py/verdict.py/skill texts, the same four modules) -> 14 failed, 132 passed in 69.10s
- mutation probe (scratch copy of the tip, refusal causes stripped, tests/test_review_brief_git.py) -> 3 failed, 14 passed in 29.22s
- `kverdict.review_attestation` / `read_bar_attestation` on the lane tip -> (c033a98..., None) / BarAttestation(bar='review', tests=9015297d...)

- [MINOR] tests/test_review_brief_git.py:288 -> The no-attestation case, and the work-commit-above cases at tests/test_review_brief_git.py:397, assert only the sha and the attest command, never the cause. A render whose refusal reads just "<sha>" passed both under mutation. This is a gap in the Done-when "each message names the cause" for the absent case (K1/B1). -> Assert the cause text in both tests, e.g. `"no verified attestation" in err` and `"non-record" in err` (for the absent case, also the zero-label-lines cause). -> @owner
- [MINOR] tests/test_review_brief_git.py:345 -> The "names both bars" assertion is vacuous. After stripping `review_brief` and `--bar review`, the refusal's fixed prefix "carries no review bar attestation" still holds "review". A cause naming only `landing` passed under mutation, so TC-371's "another-bar refusals name both compared values" is not pinned (K1/B1). -> Assert on the cause clause itself, e.g. `"`landing` attestation, not a `review` one" in err`, or strip the fixed prefix before testing for "review". -> @owner
- [MINOR] docs/requirements/system-requirements.toml:1911 -> For clarity: SR-241's requirement and acceptance (line 1913) say "only review-record changes separate it". The code and LLR-341 step through any record-only commit, telemetry fragments under docs/log.d and empty commits included, so read literally a log-fragment commit would force a new bar (K1). -> Say "only record changes (review rounds, session telemetry, iteration records) or no changes separate it", matching LLR-341's "non-record identities remain equal". -> @owner

VERDICT: APPROVE findings=3
