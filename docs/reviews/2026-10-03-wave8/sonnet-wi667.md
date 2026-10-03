# Sonnet review — WI-667 (build/wi-667 at 24cd3b91)

Reviewer: Claude Sonnet 5.5 (read-only). Builder: Codex Sol (gpt-6.1-sol). Range
`30ee386b..24cd3b91`.

24cd3b91 SOUND

**MAJOR (follow-up, outside this lane's grant):** the evidence ladder is still shown
and still required. WI-697's brief carries `_Evidence level now: specified_` and
`**Evidenced by.** TC-279` from the shared renderer (`trace.py:4047`, `:4426`), and
the ladder lives on in `assumption_rules.py`, `check_assumption_gate.py`, `trace.py`,
`traj_views.py`, `traj_parse.py` and approved SR rows whose `coincident` cells cite
SN-043's removed sentence. Ruling item 1 drops it; removing it amends Approved
SRs/LLRs and the gate script. The new re-judge template paragraph ("establishes
nothing beyond that sample") mitigates. Recommendation: file a follow-up row.

**MINOR**
1. The plan's supersession note links `../work/queued/WI-667-…`, which rots when
   the row closes. *(Fixed at the landing: cited by id.)*
2. The RESYNC entry omits the prompt-catalogue regeneration the template change
   needs. *(Fixed at the landing.)*
3. SR-033's rationale and `sn_refs` justify only the budgets. *(Fixed at the
   landing: SN-043 added, rationale sentence.)*
4. The composer's held/out-of-scope/Approved/dangling-DA behaviour is correct
   (probed) but untested.
5. The plan's C3/C5 paragraphs were replaced in place; the original is in git.
6. LLR-295 carries both composer arms in one row.

**Verified:** WI-697's brief composes, rendering DA-011's statement, falsifier and
standing, then TC-279. The first-approval composer shows TC-279 awaiting approval
with the right snapshot token. A DevStg-Release dial, an out-of-scope id, an
Approved case and a dangling DA each refuse correctly. `_render_approval_rows` is
shared by both arms. The checklist's old and new output is byte-identical on the
live, empty and phase-filtered docs; a synthetic Approved registry adds only the
`## 7. Assumptions — not falsified` block. Inclusion and omission follow ruling
item 8. The generator only reads. SN-043 is changed minimally, and SN-004 is
correctly left alone. LLR-295/296 and TC-308..310 are true of the code, with
correct back-links.

**Commands:** `pytest -q -n 2 tests/test_assumption_observation_briefs.py
tests/test_release_assumptions.py tests/test_gen_release_checklist.py
tests/test_adjudicate_brief.py`: `78 passed in 26.44s`; `check_trajectory.py
--strict`: clean (764 work items); `gen_prompt_catalog.py --check`: fresh.
