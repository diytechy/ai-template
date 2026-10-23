# WI-850 implementation plan: a spine row is approved only after the rows it hangs from are

Planner: a fresh Claude Opus session. It read the claim copy
`docs/work/active/wi-850/WI-850-child-approved-after-parent.md` in full, its
`specref` (`docs/plans/2026-10-07-wi841-retro/PROPOSAL.md` §7.2 and row P3),
the owner's ruling 4 in `docs/log.d/2026-10-07-wi841-retro-owner-rulings.md`,
and the code, registries, skill and tests the Trust section names, all in the
lane worktree at `ad67e4b3f`.

## The architectural-delta answer

DELTA: within

- **Adds a state?** No. The status vocabulary stays `{Drafted, Approved,
  Founded}`, and the derived stage reads nothing new.
- **Adds a value to a domain?** Yes, three. `check.py`'s built-in step set
  gains `parent-first`. The integrity finding class gains one finding kind.
  `text_then_act.LANE_COMMIT_RIDERS` gains a third rider.
- **Makes an output depend on a new input?** Yes, two. The pre-commit verdict
  and the merge slot's per-commit verdict now depend on the status pairs
  across tiers in a commit and its parents. The `trace.py` integrity floor
  depends on those pairs on disk.
- **Crosses a new boundary?** Yes. `text_then_act` and `check` call a new
  commit judgement owned by `acceptance_record`. That is a new call seam, so
  P2 proposes a new IF row for it.

Each of these is carried by a row of the table: P2 (the IF row), P5 (the
rule), P6 (the finding kind), P7 (the judgement and its contract) and P8 (the
step, the rider and the hook). No refactor outside this item is needed on
today's base. There is one conditional tripwire, recorded under Risks R1 (the
module-size threshold if WI-963 lands first). If it fires, the builder stops
and the coordinator rules on it. The plan does not route around it.

## Settled points

The draft left these open, or they had to be settled before the build.

1. **D5: a labelled derived SR, not SR-178's chain.** No approved row demands
   the parent-first rule:
   - SR-178 reports text that has drifted from its acceptance record. Its
     own rationale keeps it apart from any status movement.
   - SR-157 reports the rules the checkers declare. It does not declare this
     one. A rule added at a declaration site falls inside SR-157's reporting
     scope by default, so SR-157 needs no amendment.
   - SN-002 asks for a chain that is "mechanically verified, not manually
     asserted", and SN-029 asks that each approval be a review against the
     row's evidence. Neither names parent-first order.

   So P2 authors one **derived** SR, labelled as one in its rationale the way
   SR-224's is. It cites SN-002 and SN-029 (both Approved), with
   `boundary_refs` B-02 (status flips, the authority input) and B-09 (the
   reports). Proposed hat: CONSISTENCY. Below it go two LLRs and two TCs (P2
   has the detail).

   No need text is amended, so every row sits on a released rung (the dial
   reads `DevStg-Boundary`) and one combined first-approval sitting judges
   the set (P12).

   SR-178 stays the item's SR, and this plan cites it where its own code and
   wording are touched: P4 (the amendment walk's readers, kept
   behaviour-identical), P9 (its TCs re-run over audited fixtures) and P10
   (the skill's "approved for its current text" half). Whether the minted SR
   joins the item's `sr_refs` is the coordinator's call. If it does, this
   plan is revised to cite the minted id.
2. **The parent set** follows D-002. An SR's parents are its `SN-Refs` that
   resolve to SN rows. An LLR's are its `SR-Refs` that resolve to SR rows. A
   TC's are its `Verifies` ids that resolve to SR or LLR rows. Several kinds
   of id are not judged:
   - an IF, B or DA id;
   - an id no row declares (that is `coherence.py`'s `references unknown`);
   - a `-000` example row, as child or as parent.

   The last one is load-bearing. The shipped
   `registries/low-level-requirements.template.toml` carries `LLR-000`
   `Approved` under `SR-000` `Drafted`, so a rule that judged example rows
   would red every freshly bootstrapped scaffold (SR-010).
3. **Approved** means `kitlib.spine.claims_approval(row)`: `is_approved` or
   `is_founded`. That is the pair `acceptance_record._claims_approval` names
   today. It moves into `kitlib.spine`, and `_claims_approval` becomes a
   binding to it. A missing `Status`, or a word outside the vocabulary, is not
   approved.
4. **One message, two readers.** `kitlib.spine.parent_first_line(entry)`
   formats every entry. Example: `LLR-281 (Approved) is approved under SR-224
   (Drafted), which is not: approve SR-224 in its own approval act, or return
   LLR-281 to Drafted`. The standing finding prefixes `parent-first:`. The
   commit judgement prefixes `commit <sha10>:` or `the index:`. Each line
   carries its own remedy, so `integrate._with_text_then_act_remedy` leaves
   it alone and `integrate.py` needs no code change.
5. **The step name** is `parent-first`, with `check.py --parent-first` as its
   body. It is a `_text_then_act_mode`-shaped mode at `STAGE_NEEDS`, layer
   `process`. It is in `BUILTIN_STEP_NAMES` and not in
   `_TRUNK_FRESHNESS_STEPS`.
6. **No reuse of the status-move readers.** The commit judgement does not
   reuse `staged_status_moves`, `committed_status_moves` or `_spine_rows_at`.
   The first two read the first parent only and answer `[]` when git cannot
   answer. The third takes "cannot be read" and "does not parse" for an
   absent registry. All three degrades are ones the Trust ruling forbids
   here. The judgement reads each carrier through WI-963's
   `acceptance_record._tier_reads`: `kitlib.git.git_show` plus
   `spine_carrier.tier_rows_from_text`, which keeps the two failures apart.
7. **The in-lane skill line** ("approved only after the parent is approved
   for its current text") stays. This check reads status only. "For its
   current text" is the drift report's half: SR-178's amendment walk and the
   re-attestation. P10 names both enforcers.
8. **`trace.llr_status_advisories` (WI-129) retires** in P6. Every case it
   warned of is a Drafted LLR whose citing TCs are all Approved. Each such
   case is now an integrity finding on the edge from TC to LLR. The finding
   is strictly stronger: it gates, and it fires on one approved TC, not only
   on all of them.
9. **D1 recommended path:** adjudicate SR-224 for first approval. LLR-281 and
   TC-291 are already approved and built. SR-224 is a labelled derived SR on
   a released rung, its parent SN-005 is Approved, and approving it costs one
   sitting with no rework. Demoting LLR-281 and TC-291 is the fallback, used
   only if the sitting does not approve.

   A read-only scan of the four live registries at `ad67e4b3f` finds exactly
   that one standing case: LLR-281 and TC-291 under SR-224.

## The plan

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | D1 in its own act: a first-approval sitting of SR-224 (coordinator_adjudicate.py judge, then act). APPROVE: the act turn flips SR-224 to Approved and runs `intake.py snapshot`, in one act commit that changes no other cell. Otherwise: one hand commit returns LLR-281 and TC-291 to Drafted (no copy, since a de-approval is no act). Lands in the lane after the plan's pass record and before any code commit. | D1; SR-224; TC-291 | no interface — a registry act, no code changes | |
| P2 | Terra's intent change set, one commit, every new row Drafted: the labelled derived SR (cites SN-002 and SN-029; B-02 and B-09); LLR-a (the rule's one home and the standing finding: kitlib/spine.py, trace.py; CMP-006); LLR-b (the commit judgement, staged and per-commit, and its wiring: acceptance_record.py, check.py, text_then_act.py, integrate.py, hooks/pre-commit; CMP-008); TC-a (Unit, Smoke, verifies the SR and LLR-a); TC-b (Integration, Full, verifies the SR, LLR-b and the new IF row); the new IF row; and the lane's arms map. No existing row is amended. | D5; SR-157 | Proposed: the commit judgement's call seam, owned by scripts/acceptance_record and requested by scripts/text_then_act and scripts/check — nearest existing IF-196 (the held status, offered by the same owner in staged and per-commit forms to check and integrate); its shape follows IF-303 (a per-commit rider returning refusal lines) | P1 |
| P3 | Tests first, committed alone before any code: the new modules tests/test_parent_first.py (in-process, smoke) and tests/test_parent_first_git.py (real git, added to `tests/conftest.py` SLOW_MODULES with test_parent_first as its in-process pin), plus the replaced cases in tests/test_trace_rules.py. New behaviour is marked `xfail(strict=True, raises=(AssertionError, pytest.fail.Exception))`, with stubs so that each red reaches its own assertion. The tests are listed per step below. | D6 | no interface — test files only | P2 |
| P4 | Behaviour-preserving preparation, two commits. (a) Carry WI-963's `acceptance_record._tier_reads` as its own commit, with `_spine_rows_at` reading through it (skipped if WI-963 has landed first; then rebase). (b) Move the approval pair into `kitlib.spine.claims_approval`; `acceptance_record._claims_approval` binds it. Every existing caller's behaviour is unchanged. | D2; SR-178; TC-153; TC-193 | IF-102; IF-091 | P3 |
| P5 | The rule's one home: `kitlib.spine.parent_first_findings(tiers)` takes `{"SN","SR","LLR","TC": rows}` under the readers' column names and returns one entry `(child, child status, parent, parent status)` for each approved child citing a declared, unapproved parent, over the edges SN-Refs, SR-Refs and Verifies (SR and LLR only), skipping `-000` rows. `parent_first_line(entry)` formats each one. A pure function: no I/O. | D2; D3 | intra-module: a pure predicate in kitlib/spine.py beside is_approved, is_founded and refs, which carry no IF row; its inputs are the rows IF-102's readers already produce | P4 |
| P6 | The standing finding. `trace.integrity_sweep` appends `parent_first_findings(dict(raw, SN=reg.raw_sns))`, formatted, to `findings.integrity`, so `--strict-integrity` and `--strict` exit 1 and the `registry-integrity` step (pre-commit, every bar, CI, the slot's bar) fails on a standing case. Retire `llr_status_advisories`, its `Findings` field, its report section and its `llr-status-advisories=` summary token. Rewrite docs/registry-machinery-reference.md §4.1's advisory paragraph and add a row to docs/enforcement-audit.md. Re-stamp trace.py's ratchet entry downward in the same commit. | D3; D6 | IF-145; IF-042; IF-001; IF-102 | P5 |
| P7 | The commit judgement's one home, in acceptance_record.py. `parent_first_lines(root, bases, head=None)`: read the name list per base with `git diff --name-only --no-renames` (index or `head`) over every carrier of the four registries (`tier_carriers`); no carrier touched in any base means `[]`, and an unreadable diff is a refusal line. Otherwise read every tier on each side through `_tier_reads`. On the commit side, a carrier that cannot be read or does not parse is a refusal line naming the path and the tree. On a parent side, either failure counts every status as moved. An absent registry is no rows. Call `parent_first_findings` on the commit tree and keep each entry whose child or parent status differs from that row's status in any base (an absent row counting as a value). `staged_parent_first_lines(root)`: the index against HEAD (and MERGE_HEAD during a merge); `[]` before the first commit; no squash path. `commit_parent_first_lines(root, rev)`: `_commit_parents` (every parent), with each line naming the commit. Add the `Contracts:` id and its `Contract IF-###:` body to the module header. | D2 | Proposed: the same call seam P2 mints (nearest IF-196); reads through IF-102 (tier_rows_from_text, tier_carriers) | P5 |
| P8 | Wiring. Add `acceptance_record.commit_parent_first_lines` to `text_then_act.LANE_COMMIT_RIDERS` (`lane_commit_walk` and `integrate._each_lane_commit` unchanged). In check.py: the `parent-first` step tuple at `STAGE_NEEDS`, the `BUILTIN_STEP_NAMES` row, `_parent_first_refusal` (off git returns None) and `_parent_first_mode` in `_text_then_act_mode`'s shape, and the `--parent-first` flag; the step stays out of `_TRUNK_FRESHNESS_STEPS`. In hooks/pre-commit: `parent-first` joins the batched `--run-steps` list, with a comment entry beside `text-then-act`'s. Reviewed ratchet bump of check.py, reason recorded. | D2 | IF-040; IF-303; Proposed: the P2 seam (nearest IF-196) | P7 |
| P9 | Fixture audit and regression. Run the full unfiltered suite once. Any fixture that approves a child under a Drafted parent (most likely in the in-lane act, snapshot and approval-record suites) is corrected in the fixture by approving its parent: it is test data, not a rule exception. Then re-run SR-178's TCs and the two sibling riders' TCs over the result. | D6; SR-178; TC-153; TC-269; TC-271; TC-278; TC-331; TC-173; TC-383 | IF-091; IF-196; IF-303 | P6; P8 |
| P10 | D4, the skill. spine-authoring SKILL.md "In every mode" now reads "a TC for every SR and LLR it verifies" (D-002) and names its enforcers: `check.py`'s `parent-first` step at the commit and the merge slot's lane-commit walk, and `trace.py --strict-integrity` for a standing case. references/in-lane.md's "approved for its current text" line names both halves: status by this check, text by the drift report. Sync the dogfooded copy under `.claude/skills/` (skills-sync step); the description is unchanged, so the skills index does not move. | D4; SR-178 | no interface — skill prose | P8 |
| P11 | D8, the RESYNC_PACK entry, anchored `[since <trunk sha>]` at the lane's trunk base and re-anchored after any rebase. What changed: the step, the slot rider, the integrity finding, the retired advisory. What to do: run `trace.py --strict-integrity` after overwriting. For each `parent-first` finding, either approve the parent in its own approval act or return the child to Drafted. Kit-owned files to overwrite: scripts/kitlib/spine.py, scripts/acceptance_record.py, scripts/text_then_act.py, scripts/check.py, scripts/trace.py, hooks/pre-commit, skills/spine-authoring/SKILL.md, skills/spine-authoring/references/in-lane.md. | D8 | no interface — kit prose | P10 |
| P12 | D5's one combined sitting at the checkpoint: reconcile P2's set against the settled code, then one first-approval sitting judges the derived SR, both LLRs and both TCs together. Its act flips them in one commit, which by construction leaves no child under an unapproved parent. | D5 | no interface — a registry act, no code changes | P9; P11 |
| P13 | D7: the gate over the checkpoint tip, one cross-family REVIEW-A (Codex Sol), then landing through the merge slot. The coordinator regenerates the trunk-only artifacts at landing: cli-reference (the new flag), interface-reference (the new Contract body), the component view and PROJECT_STATE.html. | D7 | no interface — review and landing, no code | P12 |

## Tests per step, and what each fails on before its change

Unless marked *characterization*, every test below goes in at P3 as a strict
expected failure and turns green in the step named.

**P4** (in tests/test_parent_first.py):
- `test_the_approval_pair_has_one_home`: asserts
  `getattr(kitlib.spine, "claims_approval", None) is
  acceptance_record._claims_approval`. Fails before because the attribute is
  absent and the assertion compares None.
- *Characterization:* the existing amendment-walk suites (TC-153's evidence)
  run unchanged over `_tier_reads`. Adequacy witness: a `_spine_rows_at`
  that stopped skipping a failed carrier would red
  `test_the_amendment_walk_covers_every_tier_an_approval_act_blesses`.

**P5** (tests/test_parent_first.py, in-process):
- `test_an_approved_child_under_an_unapproved_parent_is_found[SR-SN,
  LLR-SR, TC-SR, TC-LLR]`: each tier pair yields exactly one entry. Fails
  before because the stub returns `[]`.
- `test_founded_counts_as_approved_on_either_side`: a Founded child under a
  Drafted parent is found; a child under a Founded parent is not. Fails
  before (stub).
- `test_an_entry_names_the_child_the_parent_and_both_statuses`: checks
  `parent_first_line`'s text. Fails before (stub).
- `test_a_parent_with_no_status_or_an_unknown_word_is_not_approved`. Fails
  before (stub).
- `test_only_declared_tier_parents_are_judged`: one fixture holds a real
  violation together with an IF id, an undeclared id, a DA id and `-000`
  rows. It asserts the result equals exactly the one real entry, so it fails
  before (stub) and catches over-reporting after.
- *Characterization:* `test_the_shipped_templates_example_rows_raise_no_finding`.
  The shipped registry templates yield no entry. Adequacy witness: a rule
  that does not skip `-000` reports `LLR-000` under `SR-000`.

**P6** (tests/test_trace_rules.py, smoke; the tests at its lines 630–735 are
replaced):
- `test_an_approved_llr_under_a_drafted_sr_reds_strict_integrity`: on the
  `scaffold` fixture, `trace.py --strict-integrity` exits 1 and its output
  names the child, the parent and both statuses. Fails before: exit 0, and
  only the WI-129 advisory prints.
- `test_a_drafted_llr_whose_citing_tcs_are_approved_is_an_integrity_finding`:
  the advisory's old case is now an integrity finding on the edge from TC to
  LLR. Fails before (advisory only).
- `test_the_llr_status_advisory_is_retired`: asserts `not
  hasattr(trace, "llr_status_advisories")` and that the summary carries no
  `llr-status-advisories=` token. Fails before.

**P7** (in-process arms in tests/test_parent_first.py, with git reads
monkeypatched):
- `test_a_commit_side_registry_that_cannot_be_read_or_does_not_parse_is_refused_by_name`.
- `test_a_diff_git_cannot_produce_is_a_refusal_not_a_skip`.
- `test_a_parent_side_that_does_not_parse_counts_every_status_as_moved`.

All three fail before because the stub returns `[]`.

**P7 and P8** (tests/test_parent_first_git.py, real repositories; TC-b's
evidence). Each one drives `check.py --parent-first` or the merge slot, so
before P8 each fails on its exit-code assertion: the flag is unknown, so the
exit is 2, or the lane merges.
- `test_staging_an_approved_child_under_a_drafted_parent_is_refused[four pairs]`:
  exit 1, naming both rows.
- `test_demoting_a_parent_under_an_approved_child_is_refused`.
- `test_a_founded_child_flipped_under_a_drafted_parent_is_refused`.
- `test_an_act_approving_parent_and_child_together_passes` (exit 0).
- `test_a_commit_moving_neither_row_passes_over_a_standing_case`: the standing
  case is trace's to report, not this step's.
- `test_a_commit_touching_no_registry_is_not_read`.
- `test_a_registry_added_with_a_violation_is_refused`.
- `test_a_commit_repairing_an_unparseable_registry_is_judged_on_its_own_rows`:
  a clean repair passes; one that carries a violation is refused.
- `test_a_merge_assembling_a_violation_from_two_sides_is_refused`: staged
  during a merge, against HEAD and MERGE_HEAD.
- `test_a_no_verify_lane_commit_with_a_violation_is_refused_at_the_slot`:
  `integrate` names the commit, and the line carries the rule's own remedy,
  not `TEXT_THEN_ACT_REMEDY`.
- `test_the_first_commit_is_not_judged`.
- `test_a_legacy_csv_carrier_is_judged_like_toml`.

**P8** (tests/test_parent_first.py pins):
- `test_the_rule_rides_the_lane_commit_walk`: the rider's name is in
  `LANE_COMMIT_RIDERS`.
- `test_the_pre_commit_hook_runs_the_parent_first_step`: the hook's
  `--run-steps` list and `BUILTIN_STEP_NAMES` both carry `parent-first`, and
  `_TRUNK_FRESHNESS_STEPS` does not.

Both fail before.

**P9:** no new tests. The full suite's corrected fixtures are the evidence,
together with TC-153, TC-269, TC-271, TC-278 and TC-331 (SR-178's TCs) and
TC-173 and TC-383 (the sibling riders) passing over them.

**P10 and P11:** prose. The `skills-sync` step checks the dogfooded copy, and
`tests/test_check_resync.py` checks the entry's anchor and shape.

## Risks and open points for the coordinator

- **R1, module size.** acceptance_record.py is 916 SLOC on this base, and P4
  plus P7 add about 55, so it stays under the ratchet's 1000-SLOC threshold.
  WI-963's held lane brings it to 977 SLOC on its own. Whichever of the two
  rows lands second therefore crosses the threshold, and
  `test_module_sizes_exactly_match_the_committed_baseline` reads that as a
  new monolith. If this lane is rebased onto a trunk carrying WI-963, the
  builder stops at P7 and the coordinator rules before the build continues.
  The options are a reviewed new baseline entry, or moving the commit
  judgement's home, which would amend the Trust section. The plan takes
  neither path on its own.
- **R2, fixture churn.** P6 and P8 make any test fixture that approves a
  child under a Drafted parent red. P9's audit runs the full suite once to
  find these. Each fix goes in the fixture, never in the rule.
- **R3, in-flight lanes.** Once the rider lands, the slot judges every
  not-yet-landed lane commit. A sitting's act that flips a child without its
  parent is then refused. That is the intended behaviour, but it is worth
  naming in the landing note.

## Surfaced, not in scope

`adjudicate_act._claims_approval` repeats the same approval pair, with an
identical body. `baseline_snapshot._claims_approval` is a deliberately wider
OR that covers the off-spine tiers. Binding the first one to
`kitlib.spine.claims_approval` would be a one-line consolidation, but neither
module is in this item's Trust section. It is a candidate successor row.
