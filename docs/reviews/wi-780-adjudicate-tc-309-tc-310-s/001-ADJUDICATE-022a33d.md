# WI-780 adjudication: TC-309, TC-310 (first approval; reworked by WI-778)

Independent adjudicator: Claude Opus 5.5. I directed none of WI-776 or WI-778.

**What I read.**
- The chains of SR-033 (LLR-033, LLR-296; TC-033, TC-310), SR-146 (LLR-162, LLR-163, LLR-164, LLR-167, LLR-273, LLR-295; TC-157, TC-161, TC-192, TC-271, TC-308, TC-309) and SR-215 (LLR-254, LLR-255, LLR-265, LLR-293, LLR-294, LLR-295; TC-247, TC-248, TC-261, TC-306, TC-307, TC-308, TC-309, TC-311).
- WI-776's verdict, as prior findings that bind nothing here.
- The code: `adjudicate_brief._rejudge_case_text`, `_assumption_case_chain` and `rejudge_values`.
- The evidence: `tests/test_assumption_observation_briefs.py` and `tests/test_release_assumptions.py`. Both modules are smoke tier (neither is in `tests/conftest.py` `SLOW_MODULES`), which matches `Tier = Smoke` on both rows.

**What I ran.**
- The two modules pass: 8 passed.
- Mutation probes, in process on unmodified files: each probe patched the function under test and re-ran the existing test.

- [RETURN] TC-309 -> compose the re-judge brief for a due assumption-only case; assert the assumption id, statement, falsifier and standing and the observation Method appear; an undeclared assumption refuses naming it; a missing Method, Expected or MaxAge each refuses naming that cell; none returns a brief. Expected: the complete brief "composes under the assumption chain" -> the WI-776 gap is closed.
  - The new `Method` and `Expected` entries really drive their refusals. The refusal reason names only the missing cell (`TC-279 has no \`Method\` cell`), so `cell in reason` discriminates.
  - A probe that back-fills a missing Method, or a missing Expected, before validation makes the test fail. So does a probe for MaxAge.
  - But LLR-295 (Approved) states the re-judge brief "shows the observation instruction beneath its assumption chain", and the row's own Expected says the brief composes "under" the chain. Neither the Method nor the evidence asserts that order.
  - A probe that moves the case text ABOVE the chain still PASSES `test_rejudge_shows_assumption_only_case`.

  -> not ready. This is the defect class returned three times before: a verifier that leaves its LLR's stated clause unverified. Here the row's own Method also cannot settle its own Expected. The code is correct (`chain + [text]`), so the fix is the row's text and one assertion.
- [RETURN] TC-310 -> generate release checklists from fixture registries; assert the heading, `ASSUMPTION DA-id` marker, falsifier and observation case id, with an automated case naming the same assumption not listed; include a missing-falsifier Drafted row; omit falsified and Drafted-with-falsifier rows, with no section when all are omitted; no section for an absent registry; "assert the source registry remains byte-identical" -> both WI-776 wording findings are closed: "fixture registries", and "SR-033's inclusion set". `verifies` SR-033;LLR-296;IF-018 is sound, and the inclusion set matches SR-033's acceptance. But the evidence does not assert what the Method says.
  - `generate` compares `read_text()` to the string it wrote. That is decoded text with universal-newline translation, not bytes.
  - A probe where the generator rewrites the registry with LF endings over the CRLF bytes `write_text` produced on Windows still PASSES `test_assumptions_section_and_marker`.
  - A BOM rewrite is caught, but a line-ending rewrite is a write the read-only obligation (LLR-296 "writes no registry") forbids, and "byte-identical" is the row's own word.
  - The automated-case exclusion is proved only through the exact substring `(method: TC-279)`. TC-280 listed anywhere else in the checklist would pass.

  -> not ready: the row states a closed, correct obligation its evidence does not discharge. Test-only fix; the row's text stands.

Routed pointer cells, read and ruled, not counted in rows=N:
- TC-309 `evidence`, the one pointer cell WI-778's range (ae702b75..758519de) changed, is sound.
  - It renames the second node id to `test_rejudge_refuses_an_unresolved_assumption_or_a_missing_cell`. That test exists and drives the four refusals.
  - The first node, `test_rejudge_shows_assumption_only_case`, is unchanged.
- No `verifies` or other pointer cell moved in the range.

**Gates the follow-up must clear.** On the worktree, as a reverted trial, I applied the drafted TC-309 text and the two test changes:
- Both modules: 8 passed.
- All four probes above now fail the tests.
- With TC-309 and TC-310 left Drafted: `trace.py --strict` reports only LLR-292's pre-existing `minimal` finding, and `check_trajectory.py --strict` exits 0.
- With TC-309 and TC-310 flipped: the only new findings are the approval-record ones that the act's snapshot clears. There is no form finding on the new text.

Findings that do not withhold an approval, for the record:
- The briefs still render the assumption evidence ladder ("Evidence level now: specified"). That is WI-771's. Neither row's text depends on it.

Approved: none. Returned: TC-309, TC-310.
The one follow-up for both rows is drafted in `## Dispositions` of `docs/work/queued/WI-780-adjudicate-tc-309-tc-310-s.md`.

OUTCOME: RETURN rows=2
