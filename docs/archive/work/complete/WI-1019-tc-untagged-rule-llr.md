+++
id = "WI-1019"
title = "An LLR states WI-1001's rule that an accepted automated test case no test tag names is a finding"
workstream = "process"
sr_refs = ["SR-157"]
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 3
planmode = "none"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1019`, cut from `refactor_again` at
`d849667f1`, with the commit hooks on. The specref (WI-1017's archived spec)
is cleared at close, as a terminal row's is.

- `43795aa29`: LLR-395, the code tag, the RESYNC entry, this spec's
  build-time change (Context and Done-when) and the regenerated views.
- The close-out commit after it: this Deliverable, the move to `complete/`
  and the log fragment.

**LLR-395** (`Drafted`, under SR-157): "An accepted or founded automated test
case that no test file declares is a finding". Its detail is in contract
voice and names no code. It states:

- which cases owe a declaration: a loaded row, `Accepted` or `Founded`, whose
  automated cell, stripped and case-folded, reads yes;
- which owe none: a placeholder row, a `Drafted` case, and an automated cell
  that is absent, blank or another word. A `Drafted` case's Evidence parts
  stay held by the separate equality rule;
- the finding for an owed case that no valid declaration under the declared
  tests root names, whatever its Evidence cell holds;
- a misplaced or malformed declaration declares nothing;
- the unreadable-file exclusion, alone or beside a readable part;
- one declaration clears both this finding and the part's;
- declarations are read, not outcomes;
- vacuity (no tests root, no test-case registry) and the parse stop;
- severity: a warning without strict checking, an error with it, and strict
  from `DevStg-Impl`, so a new project warns below it;
- its bound.

Its cells follow LLR-366: `module` `project-trajectory/scripts/arch_tags.py`,
`code_symbol` `tc_tag_findings/_undeclared_case_findings`, `component`
CMP-006, `phase` 6, `test_refs` "TC-428; TC-429". `trace.py` gives it no
absolute-term, paraphrase or citation-frame advisory. `trace.py --bump-ids`
moved the watermark from LLR 394 to 395. TC-457 and TC-458 are unused.

**Changed at the build** (Context, "Changed at the build"). As first
specified, `trace.py --strict` exited 1 with two parent-first findings
("TC-428 (Accepted) is accepted under LLR-395 (Drafted), which is not",
and the same for TC-429). The hook's `parent-first` step judges the staged
tree the same way. The coordinator ruled that TC-428 and TC-429 stay
unchanged here, and their re-point is WI-1038's. No status moved.

**The code tag.** The `Implements:` line of the function that applies the rule
reads `SR-157, LLR-395`. The commit checks' RESYNC check refuses a shipped
change with no entry, and the first smoke run stopped there. So
`RESYNC_PACK.md` gains "The undeclared-case rule's code tag names the design
row stating it [since d849667f1]": nothing is forced, and the kit-owned file is
`scripts/arch_tags.py`. The pack is unbudgeted: 733,993 -> 734,651 bytes.

**Tests.** The change is registry text and a docstring, so there is no
behaviour to drive red first. TC-428 and TC-429's tests are unchanged.

- The modules reading what changed: `test_trajectory_arch`,
  `test_trajectory`, `test_trajectory_phase`, `test_changed_selection`,
  `test_complexity_ratchet`, `test_components_registry`,
  `test_module_size_ratchet`, `test_policy_one_home`, `test_smoke_tier`,
  `test_stack_profile`, `test_stage_event_detectors`, `test_import_layers`,
  `test_dogfood_sync`, the eight `test_trace*` modules, `test_id_watermark`,
  `test_id_watermark_driven` and `test_spine_rules`:
  `886 passed, 2 skipped in 193.93s (0:03:13)`.
  <!-- fig: cmd="python -m pytest -q -n auto <the 24 modules listed>" rev="43795aa29 (its tree before the commit, less the RESYNC entry)" -->
- The RESYNC pack's readers: `test_resync_pack`, `test_check_resync`,
  `test_kit_path_invariant`, `test_generated_newlines`,
  `test_held_rung_doctrine`, `test_status_vocabulary_contract`,
  `test_old_kit_resync`, `test_derive_stage`: `102 passed in 58.75s`.
  <!-- fig: cmd="python -m pytest -q -n auto <the 8 modules listed>" rev="43795aa29 (its tree before the commit)" -->
- `test_bootstrap.py -k "byte_caps or size_budget or baselines"`:
  `3 passed, 71 deselected in 0.37s`.
  <!-- fig: cmd="python -m pytest -q tests/test_bootstrap.py -k 'byte_caps or size_budget or baselines'" rev="43795aa29 (its tree before the commit, less the RESYNC entry)" -->
- The commit checks, `run_menu.py smoke`:
  `3698 passed, 3 skipped, 18 warnings in 350.93s (0:05:50)`. Its budget
  line reads CPU 1014.6 s against 540; that is a WARN only and is not
  charged to the lane.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="43795aa29 (its tree before the commit)" -->
- `trace.py --root . --strict`: exit 0, `orphans=0 integrity=0`.
  `check_trajectory.py --strict`: clean. Ruff check and format: clean. The
  commit passed the hook.

**Decisions record:** none. LLR-395 and the coordinator's ruling state every
choice.

**Nearest existing homes:** LLR-366, whose amendment the scope critique
declined; the tag joins the function's existing `Implements:` line.

**Acts owed, for automated adjudication** (the operator-acceptance dial
releases them):

- LLR-395's first acceptance. The acceptance brief lists SR-157's chain as
  waiting for automated adjudication.
- The re-point of TC-428 and TC-429 (`verifies` naming LLR-395 in place of
  SR-157, IF-263 kept) and its drift on those accepted rows. Both belong to
  WI-1038, after that acceptance.

**Review (2026-11-21, round 1, over `d849667f1..9fe88b282`):** the
coordinator's hand-built brief (the kit-change rubric, the spec at the tip,
the diff with the generated views excluded). OpenAI Sol (low) read the whole
diff and the code at the tip: APPROVE, no findings. Gemini Argon (low) read
the same brief by file reference, with the implementing functions and the
rows it names copied in: APPROVE, no findings. Nothing to fix.

## Context

Filed on trunk at WI-1017's landing (2026-11-21), from the evidence sample
in its Deliverable ("Causes outside the guidance", row 2; case B10).

WI-1001 built the rule that an accepted automated TC no test tag names is a
finding. No LLR states it: TC-428 and TC-429 verify SR-157 directly. Its
builder stopped at the accepted row, since whether LLR-366 is amended or a
new LLR is minted was the operator's call, and nothing filed the gap.

**Settled at the scope critique (2026-11-21,
`docs/reviews/2026-11-21-scope-critiques/WI-1019.md`): a new row.** WI-1001's
rule says which test cases owe a declaration at all; LLR-366 says a case's
evidence parts equal its declarations, Drafted cases included. Two contracts,
so two rows, and LLR-366 stays as accepted. The new row is LLR-395, minted
`Drafted` under SR-157. Its text is in contract voice and names no code: the
review-churn plan's item 5 refuses code names in requirement text, and
variant F's text check (WI-1021 to WI-1030) will hold it to that. Its
`module` and `code_symbol` cells are filled, since today's schema requires
them until variant F removes them.

**The acts it leaves.** LLR-395 is `Drafted`, and TC-428 and TC-429
(`Accepted`) drift when their `verifies` cell changes. The operator-acceptance
dial releases these rungs to automated adjudication (queue-drill HANDOFF §3.1
Q5, §3.3 N4), so the lane ends at the registry edits and lists what is owed;
no status moves and no hold sits inside the lane.

**Changed at the build (2026-11-21).** The parent-first rule (SR-245 and
LLR-357 at the trace, SR-246 and LLR-358 at the commit) refuses an `Accepted`
TC verifying a `Drafted` LLR: re-pointing TC-428 and TC-429 at a new `Drafted`
LLR-395 fails `trace.py --strict`, and the commit hook refuses it. So this row
mints LLR-395 and links it from the code tag, and TC-428 and TC-429 move to
verify it after LLR-395's first acceptance, under WI-1038 (filed on trunk by
the coordinator). The re-point's drift is WI-1038's.

## Done-when

- [x] LLR-395 (`Drafted`, under SR-157) states WI-1001's rule as built: which
      live test cases owe a test-file declaration, the inputs that make the
      check vacuous or stop it, and its severity by rung and by strict
      checking, all as TC-428 and TC-429 expect. Its text names no code.
- [x] LLR-395's `test_refs` name TC-428 and TC-429, whose rows are unchanged
      here; their re-point to verify LLR-395 is WI-1038's, after LLR-395's
      first acceptance. `trace.py --strict` stays clean.
- [x] The function implementing the rule names LLR-395 in its `Implements:`
      tag, SR-157 kept.
- [x] The Deliverable lists the act owed: LLR-395's first acceptance, for
      automated adjudication; the re-point's drift is WI-1038's.
