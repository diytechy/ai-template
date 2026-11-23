## 2026-11-23 — WI-1059: a derived act's flip waits while its parent stays unaccepted: named with its parents, owed, never listed

Deferred open items: none. The row changes the act derivation, one public
name in the acceptance record's parent-first judgement, spine text, a runtime
flow, the act template's notes, the coordinator-cycle recipe and two test
modules; every choice it made is stated by a spine row or by the plan the
coordinator approved, so it needed no decisions record.

Built on the maintenance branch `maint/wi-1059` from `8db60ba58`, with the
commit hooks on, under the plan `docs/plans/WI-1059/plan.md` (`50d4d3fbe`)
and the coordinator's go-ahead, which approved it as written. The record is
in the row's Deliverable
(`../archive/work/complete/WI-1059-act-holds-returned-parent.md`).

- **The wait:** an owed first-acceptance flip whose parent (as the
  parent-first rule reads parents) the act leaves unaccepted now waits. The
  act derivation computes it once, as a fixpoint over the rule's own
  whole-spine predicate, over the rows the hook's own reader returns
  (`acceptance_record._tree_tiers` made public as `parent_first_tiers`, the
  rename alone). The brief lists the takeable flips and names each waiting
  one under `Not in this act` with every parent it waits on; a flip under a
  waiting parent waits too. A verdict whose every remaining act waits is
  refused before launch, naming each; the act turn's owed-after line marks a
  waiting flip (`waiting on SR-251 (Drafted)`) and exits 1; once the parent's
  own act lands, the same verdict's act lists the flip. A parent registry
  that does not parse refuses the derivation, naming it.
- **Vocabulary:** the spec's "held" is "waits" everywhere this row wrote,
  since "held" already names the held rung in the same texts.
- **The live case:** WI-1057's verdict is now refused, naming LLR-406 as
  waiting on SR-251 (Drafted), instead of listing a flip the hook refuses.
- **Rows:** LLR-338 `detail` and TC-368 `method` and `expected` amended,
  text only, owed to the next sitting; IF-296 and IF-308 `data` rewritten
  (Drafted). Flow 6 names the all-waiting refusal. SR-231 and LLR-306 are
  unchanged (the coordinator confirmed). No ids minted.
- **Also:** the act template's notes (its instruction text, slots and
  catalogue digest unchanged; a retained adjudicator drains once), the
  coordinator-cycle recipe in its three copies, and a RESYNC entry.
- **The writer guard:** OI-30 D3's lexical writer guard
  (`test_acceptance_level`) flagged the derivation's in-memory copy of a
  flipped row (`dict(row, Status="Accepted")`); no registry is written. A
  first answer named the status as a constant (`624c2abd0`), which blinded
  the guard; on the coordinator's correction the literal is back and the
  guard carries one exemption by name, reviewed: its file and exact line,
  with the reason, so the same line anywhere else still fails. A new test
  pins that narrowness.
- **Tests:** nine new tests (T1 to T8 in `test_adjudicate_act`, T9 in
  `test_coordinator_act`), all TC-368. Eight failed on the unchanged code;
  T2, and T6's second half, were shown failing under a mutation. The 55
  affected modules: `2292 passed, 1 skipped in 1792.42s (0:29:52)`.
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
  `trace.py --strict` and `check_trajectory.py --strict` exit 0;
  `run_menu.py smoke` passed (the Deliverable quotes it).
