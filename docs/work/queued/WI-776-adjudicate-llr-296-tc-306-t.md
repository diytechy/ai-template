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
(LLR-296, TC-306 and TC-310 approved; TC-309 returned). One lane carries the
one returned row.

```toml
title = "Verify the re-judge brief's Method and Expected refusals for an assumption-only case"
workstream = "process"
buildtier = "quick"
safety_class = "spine"
sr_refs = ["SR-146", "SR-215"]
priority = 2
```

LLR-295 (Approved) states "Re-judge validates Method, Expected and MaxAge".
TC-309, the verifier of that re-judge arm, drives only the MaxAge refusal; no
test drives a missing Method or a missing Expected. The code already refuses
both, naming the cell (confirmed on a scratch copy at d297e17d), so this lane
changes a test and TC-309's text only.

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

**Prohibitions.**
- The only registry edits are TC-309's `method`, `expected` and `evidence`.
  Every other cell of every row stays byte-identical. That includes LLR-295,
  TC-308, LLR-296, TC-306, TC-310, and TC-309's own other cells.
- Do not flip any Status. TC-309 stays `Drafted`; its approval is the
  adjudication its merge mints.
- No production code changes. `project-trajectory/scripts/adjudicate_brief.py`
  stays byte-identical.
- Do not touch the evidence-ladder rendering; that is WI-771's.
- No RESYNC entry: nothing shipped to an adopter changes.

**Landing.** TC-309 is Drafted, so its merge mints a first-approval
adjudication over TC-309 alone. The test-case registry's approved copy is not
affected by this lane. A work branch commits no generated artifact; the
generated views that name the old test (`docs/ratify/CURRENT.md`,
`docs/open-items.html`) are regenerated trunk-side.

**Bar.** The commit bar, plus
`pytest -q -p no:cacheprovider tests/test_assumption_observation_briefs.py`
(3 passed on the scratch copy), plus `trace.py --strict`: only LLR-292's
pre-existing `minimal` finding may remain. Paste the real output.
