+++
id = "WI-778"
title = "Verify the re-judge brief's Method and Expected refusals; close TC-310 and SR-215 wording"
workstream = "process"
sr_refs = ["SR-146", "SR-215", "SR-033"]
specref = ""
buildtier = "quick"
priority = 2
safety_class = "spine"
+++

## Deliverable

WI-776's adjudicator draft applied, with arbitration ruling B's SR-215 sentence:

- **TC-309:** its method, expected and evidence state and test the missing
  Method and Expected refusals. The renamed test
  `..._or_a_missing_cell` gains two tuple entries; this closes a coverage gap,
  since the code already refused both.
- **TC-310:** "fixture registries" and "SR-033's inclusion set".
- **SR-215:** the rationale sentence now names the checkpoint triggers.
- No production code changed.

Codex Luna (high) found one MAJOR: the lane committed regenerated views. The
coordinator refuted it, because the hook requires the regeneration and the
landing regenerates on trunk (`docs/reviews/2026-10-03-wave8/luna-wi778.md`).
Every authored change was verified as specified.

## Context

Drafted by WI-776 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

LLR-295 (Approved) states "Re-judge validates Method, Expected and MaxAge".
TC-309, the verifier of that re-judge arm, drives only the MaxAge refusal; no
test drives a missing Method or a missing Expected. The code already refuses
both, naming the cell (confirmed on a scratch copy at d297e17d), so for
TC-309 this lane changes a test and the row's text only.

TC-310's tests are complete; its text is not. Flipped, its Method trips
`trace.py --strict` ("TC TC-310 Method uses 'minimal' - no test can settle
it"), and its Expected names "the ruled inclusion set" where SR-033's
acceptance states that set. Two wording fixes, no test change.

Each cell below is replaced whole with the text given. Write it byte-exact
apart from TOML escaping.

**TC-309 (rework, Drafted).**
- `method` -> `Compose the re-judge template for a due assumption-only case with no Verifies; assert its assumption id, statement, falsifier and standing and the observation Method appear. The same case citing an assumption the registry does not declare refuses composition naming that assumption, and the same case with no Method, no Expected or no MaxAge refuses naming that cell; none returns a brief.`
- `expected` -> `The complete re-judge brief composes under the assumption chain, and an undeclared assumption or a missing Method, Expected or MaxAge refuses with its reason.`
- `evidence` -> `tests/test_assumption_observation_briefs.py::test_rejudge_shows_assumption_only_case; tests/test_assumption_observation_briefs.py::test_rejudge_refuses_an_unresolved_assumption_or_a_missing_cell`

**The test (smoke tier, matching `Tier = Smoke`).** In
`tests/test_assumption_observation_briefs.py`:
- Rename `test_rejudge_refuses_an_unresolved_assumption_or_a_missing_lifetime`
  to `test_rejudge_refuses_an_unresolved_assumption_or_a_missing_cell`.
- In its `for row, cell in (...)` tuple, between the `DA-099` entry and the
  `MaxAge` entry, add two entries of the same shape as the `MaxAge` one:
  `({key: value for key, value in case.items() if key != "Method"}, "Method")`
  and
  `({key: value for key, value in case.items() if key != "Expected"}, "Expected")`.
- Change nothing else in the module. The loop's existing assertions (`text is
  None`, the cell named in `reason`) cover the new entries.

**TC-310 (rework, Drafted).** Two cells, each replaced whole:
- `method` -> `Generate release checklists from fixture registries: assert the assumptions heading and ASSUMPTION DA-id marker, falsifier and observation case id, and that an automated case naming the same assumption is not listed; include a missing-falsifier Drafted row; omit falsified and Drafted rows with falsifiers, and emit no section when every row is omitted; tolerate an absent registry without a section; assert the source registry remains byte-identical.`
- `expected` -> `Assumption confirmations are differentiable, absent-tolerant and read-only, with SR-033's inclusion set.`
- The only change in `method` is "minimal registries" becoming "fixture
  registries"; the only change in `expected` is "the ruled inclusion set"
  becoming "SR-033's inclusion set". `tests/test_release_assumptions.py` does
  not change.

**SR-215 (amend, Approved; added 2026-10-03 by arbitration ruling B).** Replace
ONLY the `rationale` cell's sentence that begins "The closed-work floor and the
declared trigger are cost limits" with this sentence, byte-exact; every other
sentence of the cell stays as it is:

`The closed-work floor and the declared trigger are cost limits the owner directed (the PERFORMANCE lens): no change or checkpoint makes an accepted judgement due again within the configured number of closed work items of its latest record, and a declared trigger replaces input changes with the change or checkpoint it names, so a judgement can stand on changes it never judged until a qualifying change or checkpoint meets the floor or its result expires.`

**Prohibitions.**
- The only registry edits are TC-309's `method`, `expected` and `evidence`,
  TC-310's `method` and `expected`, and the one sentence of SR-215's
  `rationale` given above. Every other cell of every row stays
  byte-identical. That includes LLR-295, TC-308, LLR-296, TC-306, TC-033,
  TC-310's `verifies`, and both rows' other cells.
- Do not flip any Status. TC-309 and TC-310 stay `Drafted`; their approval is
  the adjudication their merge mints.
- No production code changes. `project-trajectory/scripts/adjudicate_brief.py`
  stays byte-identical.
- Do not touch the evidence-ladder rendering; that is WI-771's.
- No RESYNC entry: nothing shipped to an adopter changes.

**Landing.** TC-309 and TC-310 are Drafted, so the merge mints one
first-approval adjudication over the two; SR-215 is Approved and amended, so the
merge also mints an amendment adjudication for it. SR-215 stays drifted until
that sitting acts, which blocks any act copying the system-requirements registry.
WI-771 amends rows in all three registries, so the coordinator sits these with
WI-771's adjudications in one combined act. A work branch commits no generated artifact; the
generated views that name the old test (`docs/ratify/CURRENT.md`,
`docs/open-items.html`) are regenerated trunk-side.

**Bar.** The commit bar, plus
`pytest -q -p no:cacheprovider tests/test_assumption_observation_briefs.py`
(3 passed on the scratch copy), plus `trace.py --strict`: only LLR-292's
pre-existing `minimal` finding may remain. On the scratch copy with both rows'
new text and TC-309 and TC-310 flipped as a trial, that held. Paste the real
output.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-033 [project-trajectory/scripts/gen_release_checklist.py :: main] tests: (see TC-033) — Release checklist generator
- LLR-162 [project-trajectory/scripts/prompts.py :: load/fill/strict_check/digest/catalog_rows/preflight] tests: TC-157 — Prompts as loaded files, catalogued and fingerprinted
- LLR-163 [project-trajectory/scripts/agent_session.py :: split_cmd/build_argv] tests: TC-157 — Argv arrays, and the adjudicator as a routed phase
- LLR-164 [project-trajectory/scripts/gen_prompt_catalog.py :: render/main] tests: TC-192 — The generated prompt catalogue and its freshness gate
- LLR-167 [project-trajectory/scripts/adjudicate_brief.py :: compose/disposition_values/red_tc_values/consolidate_values/amendment_values/first_approval_values] tests: TC-161 — The adjudicator briefs' evidence, and the refusal that keep…
- LLR-254 [project-trajectory/scripts/rejudge.py :: observation_test_cases/checkpoint_for/checkpoint_drafts/_open_rejudge/due_cases/BRIEF/CHECKPOINTS] tests: - — The checkpoint re-judge decision

### Knowledge packs the touched components declare (read before building)
- CMP-006 W1 Registry & conformance: registry-hygiene
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency
- CMP-009 W4 Human & adopter surfaces: downstream-resync

### Interface seams via the touched modules
- IF-018 scripts/gen_release_checklist -> external:downstream adopter: file docs/release-checklist.md — human-verified rows use `- [ ] <ID> — <what to confirm> (refs)`; assumption confi…
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-034 docs/requirements/ -> scripts/gen_release_checklist;external:downstream adopter: file None
- IF-041 external:agent CLI <- scripts/agent_session: cli headless invocation; the prompt on stdin
- IF-050 scripts/derive_stage -> scripts/check;scripts/agent_common;scripts/check_trajectory;scripts/traj_parse;scripts/intake: file docs/stage — key = value fields plus a sha256 fingerprint of the declared inputs
- IF-053 scripts/schedule <- scripts/census;scripts/dispatch;scripts/intake: call load_wis · _load, frontier, kind_of · SAFETY_CLASSES — the symbols census, dispatch and intake take; no write…
