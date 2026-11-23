+++
id = "WI-1052"
title = "An unproven risk no act ever accepted is reported as never accepted, not as reopened"
workstream = "process"
sr_refs = ["SR-202"]
needs = []
specref = ""
buildtier = "medium"
safety_class = "ordinary"
priority = 4
planmode = "none"
+++

## Deliverable

Built on the maintenance branch `maint/wi-1052`, cut from `refactor_again` at
`3c33b3783`, with the commit hooks on. No status moved and no act was taken.
Two ids were minted from the brief's range, TC-500 and TC-501, and the
watermark raised (`trace.py --bump-ids`, TC 484 -> 501). The specref
(WI-1041's archived spec) is cleared at close, as a terminal row's is. No
decisions record was needed: LLR-239's and LLR-243's amended text and
IF-217's contract state the choices.

- `e6e6d3dfb`: the reader's and the reports' change, the two tests' modules,
  LLR-239's and LLR-243's amended Detail, TC-500 and TC-501, IF-217's
  `data`, the reference page's sentence, the RESYNC entry, the watermark,
  the regenerated evidence and the regenerated views. The hook passed.
- The commit after it: the close-out, this Deliverable, the move to
  `complete/` and the log fragment.
- The commit after that: review round 1's finding answered, LLR-239's and
  LLR-243's Details restated without code names, and the regenerated views.

**How the three cases are told apart.** The Done-when asked for the wording
to follow what the reading already returns. It returned the state and one
reason, and for a risk with no anchoring act that reason was the act reader's
own text, so "no act in the readable record accepted it" and "the record
could not be read" differed only in prose. The act reader is the one place
that knows which branch it took, so it says so: with no anchor,
`risk_acceptance_view` carries one more key, `unaccepted`, true only when the
whole history and every act ledger on it were read and no act there accepted
the risk (no act names the row, or the acts naming it recorded no risk), and
false for a shallow clone's window, a malformed ledger or no git.
`risk_acceptance_act` keeps its `(commit, reason)` contract; its body moved
to a private `_risk_anchor` that also returns the flag. The reading itself
keeps its shape, `(state, reasons)`, and its state (`RISK_UNPROVEN` in all
three cases, as LLR-239 and SR-202 say); its one reason for a risk with no
act is now led by `no acceptance act accepted assumption X's risk:` where the
record read whole holds no act, and keeps its old lead, `no act accepting
assumption X's risk was found:`, where it could not be read whole. Both
reports read the case from that lead through one helper, `_unproven_case`,
so the release gate, which receives only the reading, words it exactly as
the advisory does.

**The wordings** (Done-when 1).

| case | advisory | release gate (after "it is falsified ..., and") |
|---|---|---|
| an act accepted it; a later change or failing record undid it | "accepted risk has reopened, and it reads unproven until the risk is accepted again in a reviewed acceptance: <triggers>" (unchanged) | "its accepted risk has reopened, so it covers nothing until the risk is accepted again: <triggers>" (was "has reopened: <triggers>") |
| no act in the record read whole accepted it | "accepted risk was never accepted in an acceptance act, and it reads unproven until an act accepts it: <the reader's reason>" | "its accepted risk was never accepted in an acceptance act, so it covers nothing until an act accepts it: <the reader's reason>" |
| the record could not be read whole | "accepted risk reads unproven: <the reading's reason>" | "its accepted risk reads unproven: <the reading's reason>" |

The reader's reason says how to accept the risk ("accept it in an acceptance
act that names DA-###", or "accepting one is re-accepting the row in an
act"); the reading's reason in the third case is kept whole, so it names the
shallow clone, the malformed ledger or the unread history and claims
neither. No reading changes: each case reads unproven as before, and a
falsified assumption under any of them fails the gate where it is on. The
promise is bounded as the Done-when bounds it: the record and registries as
the kit writes them.

**Tests** (Done-when 2), red first.

- TC-501, `test_the_release_gate_words_an_unproven_risk_by_why_it_reads_unproven`
  in `tests/test_assumption_rules.py` (smoke tier): the release rule over a
  falsified, relied-on assumption whose risk is read by the accepted-risk
  rule from four readings, an act whose copy of the assumption text differs,
  a record read whole holding no act, a shallow clone's unread record, and no
  view. On the base it failed: the reopened line lacked "accepted again".
- TC-500, three tests in `tests/test_accepted_risk.py` (real git, slow
  module): the advisory composed from the act reader's view of five
  histories. `..._has_reopened` (an act, then the assumption's text amended)
  passed on the base, since that wording is unchanged; it pins it.
  `..._was_never_accepted` (an act naming other rows only; an act accepting
  the row with no risk, the risk written after) and
  `..._claims_neither_where_the_record_cannot_be_read_whole` (a one-commit
  shallow clone; a ledger renumbered by hand) failed on the base with
  `KeyError: 'unaccepted'`.
- After the change all four pass, in the module run below.

**Rows checked against the new wording** (Done-when 3).

- **LLR-239** (Accepted, Detail only, so it drifts): one sentence appended.
  It said "any difference ... is an advisory naming the trigger" and
  nothing of how the advisory words the other two cases, so the advisory's
  new wording had no row stating it. Appended: "The advisory words an
  unproven risk by why it reads unproven: for a risk an act accepted and a
  later difference or failing record undid, it says the risk has reopened
  and reads unproven until accepted again; for a risk no act accepted, the
  history and the act records on it read whole, whether no act names the row
  or none that does recorded a risk, it says the assumption's risk was never
  accepted and reads unproven until an act accepts it; and where they could
  not be read whole, as in a shallow clone or with a malformed act record,
  it states the reason and says neither that the risk reopened nor that the
  assumption's risk was never accepted." Within SR-202: no reading changes,
  and the reopened case keeps SR-202's "until the risk is accepted again".
  After review round 1 the Detail names no code either (see below).
- **LLR-243** (Accepted, Detail only, so it drifts): "either that it
  records no accepted risk or the triggers that reopened its risk" said
  every uncovered risk is named by its reopening triggers, which the new
  gate wording contradicts for the other two cases. It now reads "either
  that it records no accepted risk or why its accepted risk does not cover
  it: that the risk has reopened, naming the triggers, and covers nothing
  until it is accepted again; that the assumption's risk was never accepted,
  and covers nothing until an act accepts it; or, where no act accepting it
  could be read, the reading's reason alone, saying neither." Within
  SR-206, whose acceptance criteria already ask the failure to name "why it
  is not covered". After review round 1 the Detail names no code either.
- **Review round 1's finding** (Sol MAJOR, adopted by the coordinator): the
  two amended Details still carried code names inherited from their
  accepted text. Each is rewritten in contract terms, clause for clause,
  with its meaning unchanged and no clause added or dropped; both rows are
  re-accepted at the sitting anyway, so this costs no extra act. LLR-239:
  "risk_acceptance_act(root, da_id) is the latest commit" now reads "An
  assumption's acceptance anchor is the latest commit"; "it walks no
  history" reads "the anchor's reader walks no history"; and
  "accepted_risk_state compares" reads "The accepted-risk reading
  compares". LLR-243: "release_gate_findings(das, srs, risks) fails" reads
  "The release gate fails"; "covered by accepted_risk_state" reads "covered
  by the accepted-risk reading"; and "check.py gains a built-in step
  `assumption-evidence` at the DevStg-Release threshold" reads "The harness
  gains a built-in step at the DevStg-Release threshold". The registry
  column `accepted_risk` and the stage token stay. Sol's second MAJOR
  (IF-217's `data` cell naming the call and its keys) was dismissed: an
  interface row's data cell states the call contract by design, and IF-217
  is Drafted and off-spine.
- Checked, unchanged: **SR-202** (its reopening is the act-accepted case,
  worded as before); **SR-206** ("why it is not covered"); **TC-234**
  ("A shallow clone missing the acceptance act reads unproven with the
  reason stated" still holds); **TC-238** (its reopened cases still fail
  naming the trigger; its phrase "the checker's reopened-risk advisory"
  names the advisory by its reopened case and is not contradicted).
- **IF-217** (Drafted): its `data` cell lists the view's no-anchor keys,
  `unaccepted` among them. **IF-216** and **IF-217**'s contract bodies in
  the code (and so `docs/interface-reference.md`) say the same.
- `docs/registry-machinery-reference.md`'s sentence on the advisory now
  names the three cases.

**New rows** (Drafted, each one obligation, each clause driven by a test its
evidence names): **TC-500** (`verifies` SR-202, LLR-239; Integration,
Full): the advisory's wording in the five histories. **TC-501**
(`verifies` SR-206, LLR-243; Unit, Smoke): the release failure's wording
under the four readings. Their Method and Expected name no code file,
function, flag or test.

**Test runs.**

- The 46 test modules: every module importing `assumption_rules` or
  `baseline_snapshot`, those `trace.py --tests-for` lists for both, the
  modules holding the tests tagged TC-500 and TC-501 (`test_accepted_risk`,
  `test_assumption_rules`) and TC-234's and TC-238's (`test_assumption_gate`
  besides), the whole-tree `test_import_layers`, `test_module_size_ratchet`
  and `test_dogfood_sync`, and the RESYNC pack's and the reference page's
  readers (`test_resync_pack`, `test_check_resync`,
  `test_kit_path_invariant`, `test_generated_newlines`,
  `test_held_rung_doctrine`, `test_status_vocabulary_contract`,
  `test_old_kit_resync`, `test_derive_stage`, `test_rule_sync`):
  `1702 passed, 2 skipped in 2462.25s (0:41:02)`. Other builders were
  loading the machine.
  <!-- fig: cmd="python -m pytest -q -p no:cacheprovider -n auto --basetemp D:/review-tmp/2026-11-22-wi1052/mods <the 46 modules listed>" rev="e6e6d3dfb (its tree before the commit)" -->
- `trace.py --root . --strict`: exit 0, `orphans=0 integrity=0`. LLR-239
  and LLR-243 carry no new absolute-term advisory (each keeps the one it
  had: "Time is never read", "each accepted risk's acceptance act").
  <!-- fig: cmd="python project-trajectory/scripts/trace.py --root . --strict" rev="e6e6d3dfb (with the close-out's tree, before its commit)" -->
- `check_trajectory.py --root . --strict`, exit 0:
  `check_trajectory: clean (1053 work item(s), 922 done (88%), 37 cancelled, graph acyclic).`
  <!-- fig: cmd="python project-trajectory/scripts/check_trajectory.py --root . --strict" rev="e6e6d3dfb (with the close-out's tree, before its commit)" -->
- `check_docs.py --root .` after the move: `0 broken`. `check_resync.py`:
  OK, two shipped paths, the entry anchored at `3c33b3783`. Ruff check and
  format: clean. The build commit passed the hook, 29 steps PASS, with the
  expected warnings: LLR-239's and LLR-243's Detail drift (the acts owed
  below) and Hat-Refs unchanged (neither row has Hat-Refs, and neither
  amendment brings in a new perspective, so both are left as they are).
- The commit checks, `run_menu.py smoke`, exit 0:
  `3725 passed, 3 skipped, 18 warnings in 253.68s (0:04:13)`. Its budget
  line reads CPU 817.4 s against 540, a WARN only and not charged to the
  lane; wall 254.7 s against 600.
  <!-- fig: cmd="python project-trajectory/scripts/run_menu.py smoke" rev="e6e6d3dfb (with the close-out's tree, before its commit)" -->

**Byte deltas** (none budgeted or watched):
`project-trajectory/RESYNC_PACK.md` 752,486 -> 754,066 (+1,580, unbudgeted);
`docs/requirements/low-level-requirements.toml` 560,663 -> 561,592 (+929);
`docs/test/test-cases.toml` 693,595 -> 696,278 (+2,683);
`docs/registry-machinery-reference.md` 70,885 -> 70,986 (+101).
<!-- fig: cmd="git show 3c33b3783:<file> | wc -c; wc -c < <file>" rev="e6e6d3dfb" -->

**Acts owed, for automated adjudication.**

- LLR-239's amendment (Detail; an `Accepted` row, drifting): a
  re-acceptance naming it in the act's `--reaccepts`.
- LLR-243's amendment (Detail; an `Accepted` row, drifting): the same.
- The first acceptance of TC-500 (verifying LLR-239) and TC-501 (verifying
  LLR-243), both `Drafted`.
- No routed traced change to an `Accepted` row.

## Context

Filed on trunk on 2026-11-22 by the queue drill's coordinator, from
WI-1041's build (noted in the queue-drill hand-off, not filed until now).
WI-1041 made a risk that no acceptance act names read unanchored, so it
reads unproven. Two messages then word every unproven risk the same way:
the advisory in `assumption_rules.py` ("assumption {}'s accepted risk has
reopened, and it reads unproven until the risk is accepted again", line
1509) and the release gate's line ("its accepted risk has reopened", line
1759). "Reopened" and "accepted again" are true for a risk an act accepted
and a later change undid; for a risk no act ever accepted they tell the
reader something that never happened.

## Done-when

- [x] The advisory and the release gate word an unproven risk by what the
      reading `accepted_risk_state` already returns, in three cases: a risk
      an act accepted and a later change or failed sample undid reads
      "reopened" and "accepted again"; a risk no act in the readable
      acceptance record names reads as never accepted, with how to accept
      it; and a risk whose acceptance history cannot be read (an unreadable
      ledger, history the clone lacks) keeps the reading's own reason and
      claims neither. The promise is bounded to the record and registries as
      the kit writes them.
- [x] Tests pin each of the three wordings at both sites.
- [x] Any row whose accepted text words this message (LLR-239 first) is
      checked against the new wording; an amendment it needs is text only
      and listed as owed to adjudication.
