# WI-783 adjudication: TC-309, TC-310 (first approval; tests tightened by WI-781)

Independent adjudicator: Claude Opus 5.5. I directed none of WI-776, WI-778, WI-780 or WI-781. Earlier verdicts (WI-776 and WI-780) were read as findings that bind nothing here.

**What I read.**
- Every row in the three chains:
  - SR-033: LLR-033, LLR-296; TC-033, TC-310.
  - SR-146: LLR-162, LLR-163, LLR-164, LLR-167, LLR-273, LLR-295; TC-157, TC-161, TC-192, TC-271, TC-308, TC-309.
  - SR-215: LLR-254, LLR-255, LLR-265, LLR-293, LLR-294, LLR-295; TC-247, TC-248, TC-261, TC-306, TC-307, TC-308, TC-309, TC-311.
- The owner's ruling of 2026-10-02, items 3 and 8: the composer arm for an assumption-only case, and the release checklist's differentiable assumptions section.
- IF-115 and IF-018.
- The code: `adjudicate_brief._rejudge_case_text`, `_assumption_case_chain`, `rejudge_values` and `REJUDGE_CELLS`, and `gen_release_checklist.assumption_checklist_lines`.
- The evidence: `tests/test_assumption_observation_briefs.py` and `tests/test_release_assumptions.py`. Neither module is in `tests/conftest.py` `SLOW_MODULES`, which matches `Tier = Smoke` on both rows.

**What I ran.**
- The two modules: 8 passed.
- Mutation probes, each applied to the code, run against the two modules, and reverted:
  - P1: the re-judge brief joins the case text ABOVE the chain (`[text] + chain`). This FAILS `test_rejudge_shows_assumption_only_case`. WI-780's order finding is closed.
  - P2: `Expected` is dropped from `REJUDGE_CELLS`. This FAILS the refusal test.
  - P3: the undeclared-assumption refusal is disabled. This FAILS the refusal test.
  - P4: the checklist lists automated cases too. This FAILS `test_assumptions_section_and_marker`, on `"TC-280" not in text`. WI-780's exclusion finding is closed.
  - P5: the generator rewrites the assumptions registry with CRLF turned to LF. This FAILS every registry-backed test through the `read_bytes()` comparison. WI-780's byte-identity finding is closed.

- [APPROVE] TC-309 -> compose the re-judge brief for a due assumption-only case with no `Verifies`; assert that the assumption's id, statement, falsifier and standing appear above the case line and its Method; assert that an undeclared assumption refuses naming it, and that a missing Method, Expected or MaxAge refuses naming that cell, with no brief returned -> the chain shows the following:
  - LLR-295 (Approved; parents SR-146 and SR-215) states that re-judge "validates Method, Expected and MaxAge and shows the observation instruction beneath its assumption chain", and that "an unresolved assumption refuses composition". TC-309 is the re-judge half of LLR-295. TC-308 covers the first-approval half. Each obligation sits in one row.
  - IF-115 is the `compose` call, which returns the text or the reason. The test drives `compose` and asserts both arms.
  - The Method states exactly what the evidence asserts, and P1–P3 show that each assertion bites.
  -> ready. The obligation is closed and observable, and the Expected is settled by its own Method.
- [APPROVE] TC-310 -> generate release checklists from fixture registries, and assert:
  - the assumptions heading, the `ASSUMPTION DA-id` marker, the falsifier and the observation case id;
  - that an automated case naming the same assumption is not listed;
  - that a missing-falsifier Drafted row is listed;
  - that falsified rows and Drafted-with-falsifier rows are omitted, with no section when all are omitted;
  - that an absent registry gives no section;
  - that the assumptions registry stays byte-identical.

  -> the chain shows the following:
  - SR-033's acceptance asks for exactly this inclusion set, with a differentiable marker, absent-tolerance and no change to standing.
  - LLR-296 decomposes it into `assumption_checklist_lines`.
  - IF-018 declares the `- [ ] ASSUMPTION <DA-ID> — <falsifier question> (method: <TC IDs>)` line shape that the test pins.
  - TC-033 covers SR-033's budget half. The two cases do not overlap.
  - P4 and P5 show the exclusion and byte-identity assertions now bite.
  -> ready. The obligation is closed, and its evidence discharges what the Method says.

**Routed pointer cells, read, not counted in rows=N.** TC-309 `evidence` names two tests that exist and are the ones described above. TC-310 `verifies` (SR-033;LLR-296;IF-018) is sound.

**The act is deferred, not withheld.** This verdict approves both rows. The test-case registry's first-approval copy is refused while any approved TC row has drifted unattested. WI-782's drift includes TC-227, TC-233, TC-234, TC-235, TC-238 and TC-251. WI-782 returned LLR-243 and TC-238 for an in-lane fix (owner direction S11, 2026-10-03). So the flips of TC-309 and TC-310 and the `--approves "docs/test/test-cases.toml=WI-783"` snapshot happen in the one combined act, after I re-judge that fix. No `## Dispositions` row is drafted.

**Findings that do not withhold an approval, for the record.**
- SR-033 and LLR-296 say "once", and LLR-296 says "one item per row". No fixture holds a row that qualifies twice: an active Approved row with no falsifier. The single loop over rows makes the property structural, so the gap is low risk. A later tightening could add that row and assert its marker appears once.
- When no observation case names a row, the checklist line says `(method: none declared)`. SR-033 says the case ids appear "if present". The output reads as a stated absence, not an omission.
- IF-115 `notes` is stale. It still says `amendment` is "deliberately absent" from `ROUTED`, but the amendment brief is routed now.

Approved: TC-309, TC-310. Returned: none.

OUTCOME: APPROVE rows=2
