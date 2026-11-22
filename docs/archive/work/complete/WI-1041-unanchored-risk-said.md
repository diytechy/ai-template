+++
id = "WI-1041"
title = "An accepted risk no acceptance act names is reported as unanchored, rather than anchored to a commit found in history"
workstream = "process"
sr_refs = ["SR-202"]
needs = []
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 3
planmode = "none"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1041`, cut from `refactor_again` at
`ca7039691`, with the commit hooks on. The specref (the history-reader audit
note) is cleared at close, as a terminal row's is.

- `7440bc961`: the reader's change, LLR-239's amended text, the test, the
  RESYNC entry and the regenerated views.
- The close-out commit after it: this Deliverable, the move to `complete/`,
  the audit note's site 2 marked resolved, and the log fragment.

**The reader** (`baseline_snapshot.risk_acceptance_act`). When no act ledger
entry names the assumption, as accepted or re-accepted, it returns
`(None, reason)`, the shape it already used for the other no-anchor cases.
The reason reads "no acceptance act names DA-###, so its accepted risk is
unanchored; accept it in an acceptance act that names DA-###". It reads no
history of the live registry. `_risk_first_written`, the walk, had no other
caller in the scripts or the tests, so it is deleted. The order of the other
outcomes is unchanged: a malformed ledger and a shallow clone's window are
still reported first, and acts naming the row with no risk recorded keep
their own reason. The IF-217 contract body in the module docstring (and so
the generated `docs/interface-reference.md`) and the function's docstring
say so. IF-217's registry row is unchanged: its `data` and `notes` never
stated the fallback.

**Callers.** Each was checked, and none needed a change:

- `risk_acceptance_view` returns `{"act": None, "reason": ...}` for any
  no-anchor outcome.
- `record_observation.evidence_inputs`, IF-217's one registered requestor,
  passes the view on as `views`.
- `assumption_rules.accepted_risk_state` reads a view with no act as
  `RISK_UNPROVEN`, "no act accepting assumption DA-###'s risk was found:
  <reason>". Two readers carry that reason: `accepted_risk_advisories`,
  through `trace.py`'s observation evidence where the frame declares a
  crossing, and the `assumption-evidence` step of `check_assumption_gate`,
  through `release_gate_findings`.
- What these callers now show: an accepted risk no act names reads unproven,
  not covered. A falsified assumption under one fails the release gate where
  the gate is on, and is advised where it is off. The RESYNC entry's "What to
  do" names the act that clears it.

**Noted, not changed.** Both readers word every unproven risk as one that
"has reopened" (`accepted_risk_advisories`, `release_gate_findings`). That
reads oddly for a risk no act ever accepted. The same wording already
covered the shallow-clone and malformed-ledger cases, and the reason that
follows it now says "unanchored". Rewording those two readers is outside
this row.

**LLR-239** (`Accepted`, under SR-202), text only, status unchanged. The
sentence "Only where no act names the row does it fall back to the first
commit at which accepted_risk took its current value." is replaced by
"Where no act names the row, nobody accepted the risk and there is no
anchor: it walks no history of the live registry for a commit to stand in
for the act, and reports the risk unanchored, with a reason naming the
assumption and telling the operator to accept the risk in an acceptance
act, and the risk reads unproven with that reason." The next sentence's
"at that commit and now" reads "at the act's commit and now". The hook
gave two warnings on the row, both expected: the Detail drift (the act owed
below), and Hat-Refs unchanged. The row has no Hat-Refs, and the amendment
narrows its behaviour without bringing in a new perspective, so it is left
as it is.

**Test cases.** No test case row states the fallback. TC-234, the case
`tests/test_accepted_risk.py` implements, is unchanged, so no test case
drifts. No id was minted: LLR-408 to LLR-409 and TC-480 to TC-483 are
unused, and the watermark has nothing to move.

**Tests.**

- New: `test_a_risk_no_act_names_is_unanchored_and_no_history_is_walked` in
  `tests/test_accepted_risk.py`. A repository commits DA-001 with its
  accepted risk, then makes a seed act that names the accepted needs and
  requirements but not the drafted DA-001. On the base it failed with
  `AssertionError: no acceptance act names DA-001, so its risk is bound to
  5e30de89afcd, the first commit at which it took its current value`. Now it
  passes. The reader returns no anchor, and its reason names DA-001, says
  "unanchored" and says "accept it in an acceptance act". A spy on the
  module's git reader sees no `log` or `rev-list` call naming the
  assumptions registry. The state reads unproven, with that reason.
- `tests/test_accepted_risk.py`: `15 passed in 16.87s`.
  <!-- fig: cmd="python -m pytest -q -n auto tests/test_accepted_risk.py" rev="7440bc961 (its tree before the commit)" -->
- The 24 test modules importing `baseline_snapshot` (`test_acceptance_record`,
  `test_accepted_risk`, `test_adjudicate_act`, `test_adjudicate_brief`,
  `test_assumption_gate`, `test_baseline_drift`, `test_baseline_snapshot`,
  `test_cell_classes`, `test_coordinator_act`, `test_gen_open_items`,
  `test_gen_trajectory_pending`, `test_held_status`, `test_held_status_git`,
  `test_intake`, `test_intake_held_act`, `test_intake_settled`,
  `test_integrate_admission`, `test_module_size_ratchet`,
  `test_open_items_assumptions`, `test_rule_sync`, `test_snapshot_readers`,
  `test_text_then_act`, `test_trace_briefs`, `test_traj_views`), plus
  `test_spine_carrier`, which `trace.py --tests-for` also lists:
  `1075 passed in 1225.30s (0:20:25)`. Other builders were loading the
  machine.
  <!-- fig: cmd="python -m pytest -q -n auto <the 25 modules listed>" rev="7440bc961 (its tree before the commit, before LLR-239's last rewording, which changed registry text only)" -->
- The whole-tree modules, `test_module_size_ratchet`, `test_import_layers`
  and `test_dogfood_sync`: `55 passed, 1 skipped in 11.03s`.
  `baseline_snapshot.py` is under the ratchet's threshold and has no
  baseline to re-stamp.
  <!-- fig: cmd="python -m pytest -q -n auto tests/test_module_size_ratchet.py tests/test_import_layers.py tests/test_dogfood_sync.py" rev="7440bc961 (its tree before the commit)" -->
- The RESYNC pack's readers, `test_resync_pack`, `test_check_resync`,
  `test_kit_path_invariant`, `test_generated_newlines`,
  `test_held_rung_doctrine`, `test_status_vocabulary_contract`,
  `test_old_kit_resync` and `test_derive_stage`:
  `102 passed in 61.50s (0:01:01)`.
  <!-- fig: cmd="python -m pytest -q -n auto <the 8 modules listed>" rev="7440bc961 (its tree before the commit)" -->
- The commit checks, `run_menu.py smoke`:
  `3714 passed, 3 skipped, 18 warnings in 391.95s (0:06:31)`. Its budget
  line reads CPU 866.8 s against 540. That is a WARN only and is not charged
  to the lane.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="7440bc961 (its tree before the commit)" -->
- `trace.py --root . --strict`: exit 0, `orphans=0 integrity=0`.
  `check_trajectory.py --strict`: clean. `check_resync.py`: OK, one shipped
  path, its entry anchored at `ca7039691`. Ruff check and format: clean. The
  commit passed the hook.

**Byte deltas:** `RESYNC_PACK.md` 737,613 -> 738,909 bytes (+1,296,
unbudgeted). The entry is "An accepted risk no acceptance act names reads
unanchored, not bound to a commit found in history [since ca7039691]", and
the kit-owned file it names is `scripts/baseline_snapshot.py`. No budgeted
or watched file was touched.
<!-- fig: cmd="git show ca7039691:project-trajectory/RESYNC_PACK.md | wc -c; wc -c < project-trajectory/RESYNC_PACK.md" rev="7440bc961" -->

**Decisions record:** none. LLR-239's amended text states the choice.

**Acts owed, for automated adjudication** (the operator-acceptance dial
releases them):

- LLR-239's drift: a re-acceptance of its amended Detail, naming it in the
  act's `--reaccepts`. The acceptance brief lists SR-202's chain as waiting
  for automated adjudication.
- No test case drifts.

**For the merge.** WI-1040 (`maint/wi-1040`) changes `acceptance_stamp` in
the same module. This branch does not touch that function. Both branches
append a RESYNC entry at the end of §4 and regenerate the same views.

**Review** (the coordinator, 2026-11-21; queue-drill HANDOFF §4 step 4).
Round 1 over `ca7039691..598839305`, the generated views and this spec's
copies withheld and the spec at the tip given whole: OpenAI Sol
(`gpt-6.1-sol`, low, via `codex exec`) read the whole diff, and Gemini
Hydrogen (`gemini-4-hydrogen-low`, via the Antigravity CLI) the prose part
by file reference. The brief asked both to judge, by name, whether the new
outcome stays within SR-202's acceptance criteria ("An assumption with a
recorded accepted risk is read as covered by that risk"). Hydrogen judged
that it does: read as recorded by an acceptance act, a risk no act names
has no recorded acceptance to be covered by. No assumption in this
repository records an accepted risk, so the change moves no reading here.
Sol: `VERDICT: APPROVE findings=0`. Hydrogen: `VERDICT: APPROVE
findings=0`. No findings, so no further round.

## Context

Filed on trunk on 2026-11-21 from WI-1036's history-reader audit, class (c)
site 2 (`docs/reviews/2026-11-history-readers/README.md`).

An assumption's accepted risk is bound to the acceptance act that accepted
it. When no act names the assumption, the reader falls back to walking the
live registry's history to the first commit at which `accepted_risk` held
its current value, and anchors the risk there. That recomputes a decision
nobody recorded (PROCESS.md §3; the review-churn plan's item 2). The audit
marks it borderline: in that case no record exists, so the fix is to stop
deriving an anchor and say so; the function's own message already tells the
reader to accept the risk in an act.

LLR-239 (Accepted, under SR-202) states the fallback, so this row amends its
text, which drifts for automated adjudication (queue-drill HANDOFF §3.3 N4).

## Done-when

- [x] With no act naming the assumption, the reader reports the risk as
      unanchored, naming the assumption and telling the operator to accept
      it in an act; it walks no history. The promise covers supported
      workflows and the ledger and registry as the kit writes them; a hand
      edit of either is outside it.
- [x] LLR-239's text says so (text only; its status is unchanged), and a
      test that fails on today's code shows the new outcome.
- [x] The Deliverable lists LLR-239's drift as the act owed; the audit
      note's site 2 is marked resolved by this row.
