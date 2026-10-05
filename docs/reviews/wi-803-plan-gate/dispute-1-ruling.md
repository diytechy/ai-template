RULING: (a)

# WI-803 dispute 1: does an unexplained DUAL clause gap fail the plan gate?

Adjudicator: independent Claude Opus (authored none of WI-803), under OI-103 Q3.
Lane `wi-803` at `4dca7543`. Dispute: Codex 6.1 Sol's review r1, MAJOR 2
(`project-trajectory/scripts/plan_coverage.py:644`) against the builder's
`docs/decisions/wi-803.toml` D-001.

## The ruling

§4.5 applies to DUAL plans. An unexplained DUAL `C#` gap is a finding (exit 1).
"Existing DUAL fixtures stay byte-identical" is compatible with that. It binds
the existing DUAL fixture inputs and the `--out` report they produce, and under
(a) both stay byte-identical. It does not bind the exit status. This does not
need the owner. The approved note settles it, and the owner's checkpoint ruling
(README A1-A4) does not touch it.

## Why the design text requires it

1. **The clause rule names both runs.** `docs/plans/2026-10-04-wi788-design/3-planning-tiering.md:228-236`:
   - the **Clauses** bullet lists SINGLE's `D#`/`F#` clauses and then DUAL's
     `C#` clauses (`:232`);
   - the next bullet, "**Coverage is a finding.** A clause is either covered by
     a row, or named under `Excludes:` ... An unexplained gap fails the gate"
     (`:233-234`), has no run qualifier. "A clause" refers to both kinds just
     defined.
2. **The rule's own example is a DUAL round.** `3-planning-tiering.md:235-236`:
   "Gilbert DP-001's plan declared exclusions with reasons, and the arbiter
   accepted them (§3.2). The grammar makes that mechanical." DP-001 was a
   dual-plan round. Reading the rule as SINGLE-only would leave its only
   example outside its scope.
3. **Selection is gated.** Decision 3 (`3-planning-tiering.md:20-22`): "A plan
   the gate fails cannot be selected or built from." §4.4 (`:212`): in a DUAL
   round "the adopted plan must also pass the gate (§4.5)". If a DUAL gap never
   fails, then for clause coverage a DUAL plan can never fail the gate, and
   both sentences say nothing.
4. **"For `DUAL`: today's pairwise coverage diff, unchanged" (`:241`) is about
   the SR/TC diff only.** It sits under the **SR/TC diff** bullet (`:238-241`),
   paired with "For `SINGLE`: every `sr_refs` entry ...". It says DUAL gets no
   SR/TC diff and keeps its pairwise diff. It is not an exemption from the
   clause rule two bullets earlier.
5. **The row says the same.** `docs/work/active/wi-803/WI-803-checkable-plan-gate.md:16-19`
   (Context): "a `DUAL` plan's are its goal's `C#` clauses. A clause is
   covered by a row or named under `Excludes: <clause> — <reason>`; an
   unexplained gap fails."
6. **The checkpoint ruling is silent here.** README "The owner's checkpoint
   ruling (2026-10-04)" (`docs/plans/2026-10-04-wi788-design/README.md:326-`):
   - A1 is routing, A2 is pacing, A3 is the disagreement page's third agent,
     A4 is D-016;
   - none of them touches coverage, `Excludes:` or the gate;
   - the README's readiness table points "What the arbiter checks against" at
     "the plan gate, ch.3 §4.5".

## Why the Done-when does not override it

The Done-when line is "Existing DUAL fixtures stay byte-identical"
(`WI-803-checkable-plan-gate.md:28`; the same words in the ch.3 §6 sketch,
`3-planning-tiering.md:408`). D-001 reads it as "DUAL exit codes and stdout stay
as before". That reading is not required, and it makes the line contradict the
same author's §4.5, decision 3 and §4.4. The reading that fits all of them:

- **The fixtures are the inputs.** These goal and plan files stay unedited:
  - `GOAL`, `PLAN_A`, `PLAN_B` in `tests/test_plan_coverage.py:14-37`;
  - `GOAL`, `PLAN_A`, `PLAN_B_GOOD`, `PLAN_B_BAD` in `tests/test_plan_coverage_step.py:17-44`;
  - the recorded planner outputs in `tests/test_dual_plan_round.py:36-70`.
- **Their report is the payload a brief embeds.** The `--out` report (IF-153)
  stays byte-identical over those inputs.

**Verified under (a).** I applied the one-line change to a scratch copy of the
lane (`gap_findings` run for every plan, the SR/TC diff still SINGLE-only) and
ran it on the `tests/test_plan_coverage.py` DUAL fixture:

- the `--out` file matched `DUAL_REPORT` (`tests/test_plan_coverage.py:322-344`)
  byte for byte (`cmp` clean);
- the run exited 1;
- stdout gained exactly these four lines after the report:

```
plan_coverage: FAIL - plan-A.md: C3 is neither covered by a row nor excluded with a reason: 'the verdict file records ports.'
plan_coverage: FAIL - plan-A.md: C4 is neither covered by a row nor excluded with a reason: 'budgets bound every session.'
plan_coverage: FAIL - plan-B.md: C2 is neither covered by a row nor excluded with a reason: 'briefs are redacted by construction.'
plan_coverage: FAIL - plan-B.md: C4 is neither covered by a row nor excluded with a reason: 'budgets bound every session.'
```

The report stays the same because `format_report` writes the `--out` file
without the FAIL/OK/note lines (`plan_coverage.py:84-91`, `:692-695`).

**What changes for the existing fixtures:** their exit status and the FAIL
lines on stdout. That is the finding §4.5 introduces, not a fixture byte.
`PLAN_A`'s prose note "C3, C4 excluded: out of scope for the pilot."
(`tests/test_plan_coverage.py:29-30`) is the free-form exclusion that the
`Excludes:` grammar exists to replace. Leaving it as non-grammar input is the
right negative case.

## D-001's other arguments

- **"S788-plan-kinds can flip this one call."** That is a misattribution.
  - What the gate reports is this row's scope. ch.3 §6 `:408` gives S788-plan-gate
    "the `Excludes:` grammar"; README `:217` gives it LLR-069 and IF-060.
  - S788-plan-kinds (WI-804) consumes the verdict ("the adopted plan must also
    pass the gate"). It does not define the verdict.
  - Deferring the rule leaves WI-804 to change a contract this row just
    shipped and specified the other way.
- **"Compatibility for the dual-plan round."** Not needed.
  - The round already handles exit 1, through its one-repair-then-PAGE path:
    `plan_coverage_step.py:111-113` maps exit 1 to `findings`, and
    `plan_round.py:229-240` sends the implicated plan to its one repair and
    PAGEs if the finding persists.
  - `plan_runner._repair_critique` (`plan_runner.py:208-228`) gives each plan
    only its own FAIL lines, which will now include its gap lines.
  - No round code changes. In the scratch run, `tests/test_dual_plan_round.py`
    passed unchanged: both recorded plans cover C1 and C2 (`:36-37`, `:69-70`).

**The one real exposure is the planner prompt.** `project-trajectory/prompts/dual-plan-planner.template.md:71-73`
tells a drafter to declare each exclusion as a free-form `## Notes` line. Under
(a), a plan written exactly as the kit's prompt asks fails the gate. On the
still-live `--dual-plan` hand path (`agent_loop.py:994`), that sends an honest
exclusion to repair and, if the drafter guesses the format wrong, to a PAGE.
The kit must not ship a gate that its own prompt fails by construction ("templates
must stay copy-ready"). So the prompt sentence moves with the gate (instruction 3).

**Scratch-run totals** (patched copy, affected modules plus the round modules):
9 failed, 58 passed.
- All 9 failures are the DUAL tests listed below that expect exit 0 over gapped
  fixtures.
- `tests/test_dual_plan_round.py`, `tests/test_plan_round.py`,
  `tests/test_trunk_step_plan.py` and `tests/test_dual_plan_routing.py` were
  green.

## Instructions for the builder

### 1. Code: `project-trajectory/scripts/plan_coverage.py`

- **`_check_one` (`:643-647`).** Run `gap_findings` for every plan, outside the
  `if gate["item_srs"] is not None:` branch. Keep `spine_diff` and
  `diff_findings` inside that branch (SINGLE-only, per §4.5's SR/TC bullet).
- **`gap_findings` docstring (`:416-417`).** Drop "SINGLE:". The gate applies
  to every run's clauses.
- **Module docstring:**
  - `:11-12`: a DUAL uncovered clause is now a finding unless excluded;
  - `:55-57`: move "a clause neither covered nor excluded" out of "SINGLE
    only:" into the general findings list. Leave the SR and TC items under
    SINGLE only;
  - IF-060 contract text `:72-75`: replace "In a DUAL run uncovered clauses
    are never a finding ..." with "In either run an unexplained clause gap is
    a finding, so a plan cannot narrow its goal or item silently; a rival plan
    that is honestly incomplete says so with an `Excludes:` line".
- **`project-trajectory/scripts/plan_coverage_step.py:11`.** Change "`1`
  reference/structure findings" to say that findings include unexplained clause
  gaps. The adapter's code does not change.

### 2. Tests

Leave the existing fixture constants and `DUAL_REPORT` byte-identical. Add
gated variants beside them; do not edit the originals.

**`tests/test_plan_coverage.py`**
- Add these constants:
  - `PLAN_A_GATED = PLAN_A + "\nExcludes: C3; C4 — out of scope for the pilot.\n"`
  - `PLAN_B_GATED = PLAN_B + "\nExcludes: C2; C4 — another plan's scope.\n"`
- Switch to the gated pair (the tests' purpose is unrelated to gaps):
  - `test_two_plans_green_with_coverage_diff`;
  - `test_out_writes_the_report_file`;
  - `test_absent_registries_degrade_to_notes_not_findings`;
  - `test_multi_covered_clause_is_reported_not_failed`: derive its plan from
    `PLAN_A_GATED`.
- `test_the_dual_report_is_byte_identical_to_the_pre_gate_report`:
  - keep the `--out` bytes assertion against `DUAL_REPORT`;
  - assert `returncode == 1`;
  - assert stdout equals `DUAL_REPORT + "\n"` plus the four FAIL lines quoted
    above (in that order, newline-terminated);
  - rename it to say both things, e.g.
    `test_dual_report_bytes_unchanged_and_unexplained_dual_gaps_fail`.
  - It also pins that a prose "excluded:" note is not an exclusion.
- New test, e.g. `test_a_dual_gap_excluded_with_a_reason_passes`: the gated
  pair exits 0, and the report shows `- excluded: C3 - out of scope for the
  pilot.` (the DP-001 case).
- New test, e.g. `test_a_dual_gap_fails_naming_only_its_plan`: `PLAN_A_GATED`
  plus the ungated `PLAN_B` exits 1, and every gap FAIL line names `plan-B.md`.

**`tests/test_plan_coverage_step.py`**
- Add these constants:
  - `PLAN_A_GATED = PLAN_A + "\nExcludes: C3; C4 — out of scope for the pilot.\n"`
  - `PLAN_B_GOOD_GATED = PLAN_B_GOOD + "\nExcludes: C2; C4 — another plan's scope.\n"`
  - `PLAN_B_BAD_GATED`: built from `PLAN_B_GOOD_GATED` with the existing
    `C3` to `C9` replace.
- Give `write_case` a `plan_a=PLAN_A_GATED` parameter.
- Use the gated B variants in:
  - `test_clean_pass_advances_the_round`;
  - `test_findings_bounce_then_repair_then_clean_advances`: the repaired
    write is `PLAN_B_GOOD_GATED`;
  - `test_findings_repeat_after_repair_pages`;
  - `test_implicated_parsing_names_only_the_faulting_plan`;
  - `test_report_payload_is_captured`.
- Expected: `implicated == ["B"]` still holds. Plan B is implicated by both its
  C9 cite and its C3 gap; plan A is clean.
- New test: an unexcluded gap in plan A alone bounces only A
  (`implicated == ["A"]`, repair offered for `{"A"}`). This pins how the round
  reads a DUAL gap.

**`tests/test_dual_plan_round.py`** stays unchanged and must stay green.

### 3. Planner prompt: `project-trajectory/prompts/dual-plan-planner.template.md:71-73`

Replace the free-form exclusion instruction with the grammar, for example:

> for every goal clause you deliberately do **not** cover, one line `Excludes:
> C# — <why>` (a declared non-goal, never silence; an unexplained gap fails the
> coverage gate).

Change nothing else in the prompt. Select mode and the `Tier` column stay
WI-804's. The coordinator trims `Excludes:` from WI-804's Done-when line
(`docs/work/queued/WI-804-plan-kinds-through-ask.md:36-37`) when it lands this.
Run `tests/test_plan_briefs.py` and `tests/test_hats.py`. They compose this
template, and the edit adds no slot.

### 4. Decisions record: `docs/decisions/wi-803.toml`

Rewrite D-001 to record the call that remains delegated after this ruling:

- **decided:** "Existing DUAL fixtures stay byte-identical" binds the DUAL
  fixture inputs and their `--out` report, not their exit status.
- **why_not_escalated:** settled by the independent adjudicator's dispute-1
  ruling (`docs/reviews/wi-803-plan-gate/dispute-1-ruling.md`, OI-103 Q3).

Keep it in `high_risk`. Leave `review` empty for the owner.

### 5. RESYNC entry: `project-trajectory/RESYNC_PACK.md` (the WI-803 entry)

Replace "A dual run (`--goal`) is otherwise unchanged: its `C#` gaps stay
report payload ..." and the "No migration ..." sentence with an honest
migration note. This is a downstream-visible behaviour change:

- In a dual run, an uncovered `C#` with no `Excludes:` line now exits 1.
- The `--out` report bytes are unchanged; stdout gains the FAIL lines.
- In a round, this sends the implicated plan to its one repair, then PAGEs if
  the finding persists.
- **What to do:** re-sync `prompts/dual-plan-planner.template.md`, and teach
  the `Excludes:` line in any planner override passed with `--prompt-map`.
  Free-form "excluded" notes no longer count.

### 6. Spine (re-amend; route to the spine author, adjudicated on the one path, per the row's Done-when)

The amended cells currently encode D-001:

- **LLR-069 `detail`** (`docs/requirements/low-level-requirements.toml:672`):
  replace "A single run treats uncovered Done-when or finding clauses and
  missing SR/TC coverage as findings; a dual run retains uncovered clauses as
  report payload" with "Either run treats an unexplained clause gap as a
  finding; a single run also treats missing SR/TC coverage as findings".
- **TC-069** (`docs/test/test-cases.toml:741-`):
  - `expected`: "an unexplained SINGLE Done-when or finding gap" becomes "an
    unexplained clause gap in either run (SINGLE Done-when or finding, DUAL
    goal clause)". Keep "DUAL report bytes remain unchanged".
  - `evidence`: add the renamed byte-identity test and the two new DUAL tests.
- **IF-060 `data`** (`docs/requirements/interfaces.toml:537-`): "1 findings,
  including SINGLE gaps or SR/TC misses" becomes "1 findings, including
  unexplained clause gaps or SINGLE SR/TC misses".
- **SR-155:** no SR cell changes (R2).

### 7. Bar

The row's test bar, unchanged:

- `tests/test_plan_coverage.py`, `tests/test_plan_coverage_step.py`,
  `tests/test_dual_plan_round.py`, `tests/test_plan_briefs.py`,
  `tests/test_hats.py`, `tests/test_complexity_ratchet.py`;
- the smoke tier at `-n 2` with `scripts/check_smoke_budget.py --mode enforce`.

Paste the real output.

Out of scope for this ruling: Sol's MAJOR 1 (an item SR excluded instead of
cited) and the MINOR on `docs/stack.ini:846`. Settle those on their own.
