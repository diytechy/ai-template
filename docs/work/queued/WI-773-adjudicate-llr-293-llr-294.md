+++
id = "WI-773"
title = "adjudicate: LLR-293, LLR-294, TC-306, TC-311 - spine row(s) authored Drafted on merged trunk 00467fc..1ffd8c5 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-293", "LLR-294", "TC-306", "TC-311", "TC-307", "TC-279"]
+++

## Context

Carried in by the coordinator 2026-10-03: TC-307 (returned by WI-767 for its parent's gap, given no text change by WI-770, so no mint routes it), and TC-279 (an assumption-only observation case WI-767's composer could not render; WI-667 added the arm).

Derived from `staged_drafted_rows` on the merged commit (§A5.2).
These spine rows are BELOW approval and no act has blessed them.
Each line: registry row / what the lane did.

- LLR-293 amended in `docs/requirements/low-level-requirements.toml` (Detail)
- LLR-294 amended in `docs/requirements/low-level-requirements.toml` (Detail)
- TC-306 amended in `docs/test/test-cases.toml` (Expected)
- TC-311 authored in `docs/test/test-cases.toml`

Outcomes (owner ruling 2026-09-01): read each row's WHOLE CHAIN — the
parent SR, the sibling LLRs, the test cases — and either APPROVE (move
the rows' `Status` to `Approved` and take the anchoring snapshot,
`python scripts/intake.py snapshot --approves "<REGISTRY>=<this row>"`,
in ONE reviewed commit on this lane) or RETURN with findings, drafting
the follow-up in a `## Dispositions` section of THIS spec — intake mints
it at this row's merge (drafts-not-mints, R1). The approval act is
YOURS: a work lane's merge is refused if it performs one.

## Dispositions

Verdicts: `docs/reviews/wi-773-adjudicate-llr-293-llr-294/001-ADJUDICATE-2256e4e.md`
(TC-306 returned; LLR-293, LLR-294, TC-307, TC-311 and TC-279 approved) and
`docs/reviews/wi-769-adjudicate-llr-295-llr-296/001-ADJUDICATE-2256e4e.md`
(LLR-296, TC-309 and TC-310 returned; LLR-295 and TC-308 approved). One lane
carries every returned row: all four are Drafted rows in two registries, and
one first-approval sitting can judge them together. WI-769's spec points here
and carries no draft of its own.

```toml
title = "Verify the cadence refusals and the assumption-brief refusals, and list only observation cases in the release checklist's assumptions section"
workstream = "process"
buildtier = "medium"
safety_class = "spine"
sr_refs = ["SR-215", "SR-033"]
priority = 2
```

Each cell below is replaced whole with the text given. Write it byte-exact
apart from TOML escaping.

**Prohibitions.**
- Change no other cell of these four rows, and no cell of any Approved row.
  In particular LLR-293, LLR-295, TC-033, TC-247, TC-307, TC-308, TC-311 and
  TC-279 stay byte-identical.
- Do not flip any Status. LLR-296, TC-306, TC-309 and TC-310 stay `Drafted`.
  Their approval is the next first-approval adjudication's.
- Production code changes in exactly one place: the observation-case filter in
  `gen_release_checklist.assumption_checklist_lines`, with the import it needs.
  Every other edit is a test.
- Do not touch the evidence-ladder rendering, `Evidenced by.` or
  `_Evidence level now_`. That is WI-771's.
- Under ruling R2, no SR cell changes.

**Landing.** Each of the four rows gets a text change, so the merge's
`staged_drafted_rows` mints one first-approval adjudication over LLR-296,
TC-306, TC-309 and TC-310, and no carry is needed. No Approved row changes, so
no amendment adjudication is minted.

**TC-306 (rework, Drafted).** LLR-293 (Approved) states two clauses no case
verifies.
- `method` -> `Drive committed file, component, release and stage-gate triggers and an undeclared input-change case. Assert due and not-due, floor blocking and threshold crossing, a raised floor and a lower attempted override, a zero policy floor disabling the default, bookkeeping exclusion, first judgement and expiry bypass, revision-bound reads and a fresh record resetting the floor. Construct the cadence directly with a malformed policy floor, an unknown trigger and a git that cannot read history, and assert each raises ValueError.`
- `expected` -> `A declared trigger fires only after the closed-WI floor; with no declared trigger, a change to declared inputs fires subject to the same floor; absence and expiry bypass both; a zero policy floor disables the default; a malformed floor, an unknown trigger or unreadable history raises ValueError rather than reading as not due.`
- Tests, in `tests/test_rejudge.py` (Full tier, matching `Tier = Full`):
  - `test_a_zero_policy_floor_disables_the_default`. Use a `files:src/*`
    trigger, a case floor of 0 and a committed policy of
    `observation_min_work_items = 0`, then commit a change to `src/a.txt` with
    no closed work. Assert the case is due.
  - `test_cadence_refuses_what_it_cannot_read`. Construct
    `observation_cadence.Cadence` and assert `ValueError` for three inputs:
    a policy `observation_min_work_items = "ten"` (at construction); a row
    whose `Trigger` is `nightly`, at `eligible`, under a policy floor of 0
    (`eligible` checks the floor before the trigger, so a floor not met
    returns False first); and a `git` callable returning a nonzero
    `returncode`, at `eligible`.

**TC-309 (rework, Drafted).** LLR-295 (Approved) states two refusals no case
verifies.
- `method` -> `Compose the re-judge template for a due assumption-only case with no Verifies; assert its assumption id, statement, falsifier and standing and the observation Method appear. The same case citing an assumption the registry does not declare refuses composition naming that assumption, and the same case with no MaxAge refuses naming that cell; neither returns a brief.`
- `expected` -> `The complete re-judge brief composes under the assumption chain, and an undeclared assumption or a missing MaxAge refuses with its reason.`
- `evidence` -> `tests/test_assumption_observation_briefs.py::test_rejudge_shows_assumption_only_case; tests/test_assumption_observation_briefs.py::test_rejudge_refuses_an_unresolved_assumption_or_a_missing_lifetime`
- Test, in `tests/test_assumption_observation_briefs.py` (smoke tier, matching
  `Tier = Smoke`): `test_rejudge_refuses_an_unresolved_assumption_or_a_missing_lifetime`.
  Monkeypatch as in `test_rejudge_shows_assumption_only_case`. For a case
  whose `assumption_refs` is `["DA-099"]`, `compose` returns `(None, reason)`
  with `DA-099` in the reason. For the TC-279 case with `max_age` removed, it
  returns `(None, reason)` with `MaxAge` in the reason.

**LLR-296 (rework, Drafted).** SR-033 (blessed this sitting) lists "the
observation case ids naming it". This row, and the code, list every test case.
- `detail` -> `Read real DA rows through spine_carrier; emit a separate assumptions section with one ASSUMPTION DA-id item per active Approved row or row with no falsifier, including its falsifier or missing notice and the ids of the observation cases naming it in Assumption-Refs. Missing registries and empty selections emit no section. Checklist generation writes no registry; checking a box asserts only not falsified, and a person sets standing. Existing sections and phase selection remain intact through named readers and section renderers.`
- The only change against today's cell: "TC ids naming it in Assumption-Refs"
  becomes "the ids of the observation cases naming it in Assumption-Refs".
- Code: in `assumption_checklist_lines`, list a case as a method only when
  `assumption_rules.is_observation_tc(tc)` is true; that function is the one
  definition of an observation case. Import `assumption_rules` the way the
  module imports its other script siblings. Change nothing else in the
  generator. Its output on this repo's live registries must stay
  byte-identical: TC-279, the only case carrying `Assumption-Refs`, is an
  observation case.

**TC-310 (rework, Drafted).**
- `verifies` -> `["SR-033", "LLR-296", "IF-018"]`. SR-033's new assumptions
  clause gets a direct verifier beside TC-033's budget half.
- `method` -> `Generate release checklists from minimal registries: assert the assumptions heading and ASSUMPTION DA-id marker, falsifier and observation case id, and that an automated case naming the same assumption is not listed; include a missing-falsifier Drafted row; omit falsified and Drafted rows with falsifiers, and emit no section when every row is omitted; tolerate an absent registry without a section; assert the source registry remains byte-identical.`
- Tests, in `tests/test_release_assumptions.py`:
  - In the `generate` helper's test registry, TC-279 becomes
    `automated = "No"`. Add a second case, `TC-280`, with
    `assumption_refs = ["DA-011"]` and `automated = "Yes"`.
  - `test_assumptions_section_and_marker` keeps its exact-line assertion
    ending `(method: TC-279)`, which now also proves TC-280 is not listed.
  - `test_ineligible_assumptions_omitted` also asserts `"## 7. Assumptions"`
    is not in the text.

**TC-247 (Approved; test only, no cell change).** Its Method says policy is
read at the revision and uncommitted changes do not affect it. No test asserts
that for the policy file. Add `test_an_uncommitted_policy_change_moves_nothing`
to `tests/test_rejudge.py`. Use `cadence_repo` with a `files:src/*` trigger
(committed floor 2), and commit a change to `src/a.txt` with no closed work.
Then write `observation_min_work_items = 0` to `docs/process.toml` without
committing, and assert the case is not due at that commit.

**RESYNC.** Add a NEW `RESYNC_PACK.md` entry anchored
`[since <trunk HEAD at build>]`. It says the release checklist's assumptions
section now lists only observation cases (`Automated = No`) as an assumption's
method, and that an adopter whose automated test cases carry `Assumption-Refs`
will see them drop from that list. Do not extend WI-667's entry.

**Bar.** The commit bar, plus
`pytest -q -p no:cacheprovider tests/test_rejudge.py tests/test_assumption_observation_briefs.py tests/test_release_assumptions.py tests/test_gen_release_checklist.py`,
plus `trace.py --strict`: only LLR-292's pre-existing `minimal` finding may
remain. Paste the real output.
