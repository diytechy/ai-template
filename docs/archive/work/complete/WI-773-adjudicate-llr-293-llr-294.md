+++
id = "WI-773"
title = "adjudicate: LLR-293, LLR-294, TC-306, TC-311 - spine row(s) authored Drafted on merged trunk 00467fc..1ffd8c5 await a FIRST APPROVAL; read the whole chain, then approve (flip + snapshot) or return with findings"
workstream = "process"
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "first-approval"
adjudicates = ["LLR-293", "LLR-294", "TC-306", "TC-311", "TC-307", "TC-279"]
+++

## Deliverable

Spine-acts batch O (act seq 22): LLR-293, LLR-294, TC-307, TC-311 and TC-279
approved; TC-306 returned (LLR-293's refusals untested). One combined successor is
drafted in `## Dispositions` below. It covers TC-306, TC-309, LLR-296 and TC-310,
with the observation-case filter routed through IF-200's seam, TC-055's
`expected` and SR-215's rationale. Sonnet 5.5 cross-review: NOT YET SOUND at
1d0c7bf2 on the draft (an undeclared cross-component import; TC-055), never on
the act; answered at 83c2f292. The coordinator confirmed on a scratch copy that
the IF-200 requestor edit clears `check_trajectory --strict` (exit 0 with it,
the ERROR without it).

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
one first-approval sitting can judge them together. The same lane also carries
two amendments of Approved rows: TC-055 and SR-215 (see the 2026-10-03 addendum
to WI-772's verdict). WI-769's spec points here and carries no draft of its
own.

```toml
title = "Verify the cadence and assumption-brief refusals, list only observation cases as an assumption's method, and correct SR-215's floor rationale and TC-055's stale cadence"
workstream = "process"
buildtier = "medium"
safety_class = "spine"
sr_refs = ["SR-215", "SR-033", "SR-054"]
priority = 2
```

Each cell below is replaced whole with the text given. Write it byte-exact
apart from TOML escaping.

Revised 2026-10-03, before any build, after the Sonnet cross-review of
1d0c7bf2. The first draft's code change failed the cross-component seam rule,
and it missed TC-055's stale Expected and SR-215's overclaimed Rationale. The
sections below supersede that draft.

**Prohibitions.** The registry edits allowed are exactly these, and no other
cell of any row changes:
- the Drafted rows: LLR-296 `detail`; TC-306 `method` and `expected`;
  TC-309 `method`, `expected` and `evidence`; TC-310 `verifies` and `method`;
- the Approved rows: SR-215 `rationale` and TC-055 `expected`;
- the Drafted interface row IF-200: `requestors` alone.

LLR-293, LLR-295, TC-033, TC-247, TC-307, TC-308, TC-311 and TC-279 stay
byte-identical.

Further limits:
- Do not flip any Status. Amended rows stay `Approved`; the Drafted rows stay
  `Drafted`. The approvals and re-attestations are the adjudications'.
- Production code changes in exactly one place: in
  `project-trajectory/scripts/gen_release_checklist.py`, one
  `import assumption_rules` beside the module's other script-sibling imports,
  and the observation-case filter in `assumption_checklist_lines`.
- Do not copy `is_observation_tc`'s logic anywhere.
- Every other code edit is a test.
- Do not touch the evidence-ladder rendering, `Evidenced by.` or
  `_Evidence level now_`. That is WI-771's.
- Under ruling R2, SR-215's new Rationale names no script, command, file or
  function.

**Landing.** The merge mints two adjudications:
- `staged_drafted_rows` mints a first-approval adjudication over LLR-296,
  TC-306, TC-309 and TC-310. Each gets a text change, so nothing needs carrying.
- `staged_spine_amendments` mints an amendment adjudication for SR-215 and
  TC-055, both Approved and amended.
- IF-200 is an interface row and Drafted, so its requestor edit mints nothing
  and drifts no approved copy.

The first-approval act copies the test-case registry, and that copy is refused
while TC-055 has drifted and is unattested. So hold one combined sitting with
one act, as this sitting did. The alternative is that the amendment act lands
first, and the coordinator adds a `needs` edge from the first-approval row to
it after the mint.

**TC-306 (rework, Drafted).** LLR-293 (Approved) states two clauses no case
verifies.
- `method` -> `Drive committed file, component, release and stage-gate triggers and an undeclared input-change case. Assert due and not-due, floor blocking and threshold crossing, a raised floor and a lower attempted override, a zero policy floor disabling the default, bookkeeping exclusion, first judgement and expiry bypass, revision-bound reads and a fresh record resetting the floor. Construct the cadence directly with a malformed policy floor, an unknown trigger and a git that cannot read history, and assert each raises ValueError.`
- `expected` -> `A declared trigger fires only after the closed-WI floor; with no declared trigger, a change to declared inputs fires subject to the same floor; absence and expiry bypass both; a zero policy floor disables the default; a malformed floor, an unknown trigger or unreadable history raises ValueError rather than reading as not due.`
- Tests, in `tests/test_rejudge.py` (Full tier, matching `Tier = Full`):
  - `test_a_zero_policy_floor_disables_the_default`. Use a `files:src/*`
    trigger, a case floor of 0 and a committed policy of
    `observation_min_work_items = 0`, then commit a change to `src/a.txt` with
    no closed work. Assert the case is due.
  - `test_cadence_refuses_what_it_cannot_read`. Build the repository with
    `root, sha = cadence_repo(tmp_path)`. The real `since` is the commit that
    added the records, `since = _git(root, "rev-parse", "HEAD~1")`: the
    `judged` commit, which `cadence_repo` commits under its `cadence policy`
    commit. The snapshot is a separate directory, `snap = tmp_path / "snap"`,
    holding only `docs/process.toml`. `Cadence(root, revision, snapshot,
    checkpoint, git)` reads the policy from `snapshot` on disk and history
    through `git`. Assert `ValueError` in three cases:
    1. `snap/docs/process.toml` reads
       `[checks]\nobservation_min_work_items = "ten"\n`, and
       `observation_cadence.Cadence(root, sha, snap, "merge", rejudge._run_git)`
       raises at construction.
    2. The same file reads `[checks]\nobservation_min_work_items = 0\n`, so the
       floor is met: `eligible` checks the floor before the trigger, and a
       floor not met returns False first. Then
       `observation_cadence.Cadence(root, sha, snap, "merge", rejudge._run_git).eligible({"Trigger": "nightly"}, since, "merge")`
       raises.
    3. With the same zero-floor file, a `git` that returns
       `types.SimpleNamespace(returncode=1, stdout=b"")` for every call, and
       `observation_cadence.Cadence(root, sha, snap, "merge", git).eligible({"Trigger": ""}, since, "merge")`
       raises. History is read before the floor is applied.

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
  `assumption_rules.is_observation_tc(tc)` is true. That function is the one
  definition of an observation case. Add `import assumption_rules` beside the
  module's other script-sibling imports, and change nothing else in the
  generator. Its output on this repo's live registries must stay
  byte-identical, because TC-279, the only case carrying `Assumption-Refs`, is
  an observation case.
- The seam (option (a): one predicate, one home). The import makes a new
  cross-component edge: `scripts/gen_release_checklist` (CMP-008/CMP-009) to
  `scripts/assumption_rules` (CMP-006/CMP-007). Without a declared seam,
  `trajectory_arch.cross_component_findings` reports it, and
  `check_trajectory --strict` errors. `is_observation_tc` already rides IF-200
  (owner `scripts/assumption_rules`; its `data` cell names it). So in
  `docs/requirements/interfaces.toml`, IF-200's `requestors` becomes:
  `["scripts/trace", "scripts/rejudge", "scripts/record_observation", "scripts/observation_cadence", "scripts/gen_release_checklist"]`.
  IF-200's other cells stay byte-identical, and so does every other IF row.
  A requestor carries no `Contracts:` line (rejudge, a current requestor, has
  none), so no module header changes.
- Landing consequence of the IF-200 edit: IF-200 is Drafted, so the edit drifts
  no approved copy and mints no adjudication. The generated views that render
  seams must be regenerated by whoever owns them on trunk; a work branch
  commits no generated artifact. Confirm the seam rule with
  `python project-trajectory/scripts/check_trajectory.py --strict`. It must
  print no `cross-component import ... gen_release_checklist ... assumption_rules`
  finding.

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

**SR-215 (amend; Approved).** The Rationale says the floor lets an accepted
judgement outlive changes to what it judged "for at most the configured number
of closed work items". That bound holds only for the no-trigger input-change
case. A `release` or `stage-gate` trigger, or a `files:` or `component:`
trigger that a change does not match, lets a judgement outlive more, bounded
only by expiry.
- `rationale` -> `Judgements cost time and model calls and vary across sessions. Written pass criteria fixed before the first judgement make the pass reviewable. The closed-work floor and the declared trigger are cost limits the owner directed (the PERFORMANCE lens): no change makes an accepted judgement due again within the configured number of closed work items of its latest record, and a declared trigger narrows which changes make it due at all, so a judgement can stand on changes it never judged until a qualifying change meets the floor or its result expires. First judgement and expiry keep missing or old evidence from standing indefinitely.`

**TC-055 (amend; Approved).** Its Expected still states the old cadence: "the
verdict recorded in Evidence is re-judged at a merge or release checkpoint when
no result of it is on record, when a declared input changes, or when the record
passes its declared max_age". Its Trigger is now `component:CMP-009` with a
floor of 10, so an input change no longer makes it due. The replacement
changes only that sentence, and states the cadence through the case's own
Trigger and floor cells rather than restating their values.
- `expected` -> `APPROVE citing numbered anchors. The rubric is the single home of the live-vs-retired anchor set: its header states the live set, and each retired anchor carries its retirement and binding in place. A verdict cites only anchors the rubric lists live, never a retired one; a clause a test now holds is verified through the LLR/TC chain the registry records, not by a verdict. Standing limit, so this row is never read as live coverage: the verdict recorded in Evidence is re-judged when no result of it is on record or when the record passes its declared max_age, and otherwise only when its declared trigger fires after its closed-work floor, never on every commit. This row's assurance is therefore as old as its latest recorded verdict, and a clause needing assurance newer than that is one to bind to a test rather than to re-judge here.`

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
remain. Then `check_trajectory.py --strict`, which must not report the
`gen_release_checklist` -> `assumption_rules` cross-component edge. Paste the
real output.
