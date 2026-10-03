+++
id = "WI-776"
title = "adjudicate: LLR-296, TC-306, TC-309, TC-310 - spine row(s) authored Drafted on merged trunk f2bc66c..ba68016 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-296", "TC-306", "TC-309", "TC-310"]
+++

## Context

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-296 amended in `docs/requirements/low-level-requirements.toml` (Detail)
- TC-306 amended in `docs/test/test-cases.toml` (Expected, Method)
- TC-309 amended in `docs/test/test-cases.toml` (Evidence, Expected, Method)
- TC-310 amended in `docs/test/test-cases.toml` (Method, Verifies)

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.

## Dispositions

Verdict: `docs/reviews/wi-776-adjudicate-llr-296-tc-306-t/001-ADJUDICATE-bcf10fa.md`
(LLR-296 and TC-306 approved; TC-309 and TC-310 returned). One lane carries
both returned rows: both are Drafted rows in the test-case registry, and one
first-approval sitting can judge them together.

```toml
title = "Verify the re-judge brief's Method and Expected refusals; close TC-310 and SR-215 wording"
workstream = "process"
buildtier = "quick"
safety_class = "spine"
sr_refs = ["SR-146", "SR-215", "SR-033"]
priority = 2
```

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
