## 2026-11-23 — WI-1069: a moved routed link selects its row, the amendment brief shows it, the identity covers it

Built on `maint/wi-1069` (cut from `refactor_again` at `d62f3c74b`) under the
plan `docs/plans/WI-1069/plan.md`, which the coordinator approved on
2026-11-23 before any build, with D1 to D12 as proposed. The spec's
Deliverable holds the per-item record, the approval and the acts owed.

- **What changed.** The acceptance model lists the chain of an accepted row
  whose routed traced cell (`SN-Refs`, `Boundary-Refs`, `Constrains`,
  `SR-Refs`, `Verifies`) moved from its recorded copy, even with no accepted
  cell moved; drift stays the accepted half, and an unjudged trace cell
  selects nothing. The acceptance brief and `open-items.html` label a changed
  row's cells from one grouping: accepted (re-acceptance owed), adjudicated
  link (goes to a sitting), other trace cell (owes no act). The amendment
  brief shows each moved link marked `(link)`, a link-only row included,
  names each scoped row it does not show, and asks of a link whether the
  row's text states what it now points at; the verdict's row grammar is
  unchanged. The judged-text identity covers the routed links, so a link
  moved after a verdict refuses a held act, a held claim and the held-MEANING
  operator row; a binding written before it fails closed for a row carrying a
  link.
- **On this repository.** The model now lists SR-017, SR-022 and SR-024
  (LLR-017, LLR-022, LLR-024 owe only their `Constrains` link); the brief
  over WI-1068's 26 `amendment:` tokens shows 26 rows (23 before), 21 with a
  `Constrains` link. No bound identity sits on a held tier, so no live
  consumer reads differently.
- **Rows.** Amended, text only, owed to a sitting: SR-178, LLR-167, LLR-359,
  TC-161, TC-398. Minted `Drafted`: LLR-484, TC-571. Off-spine `Drafted`
  notes: IF-075, IF-129.
- **Deviations from the plan:** the link tests in a new in-process module
  and the held-claim test in `tests/test_adjudicate_act.py`; the
  held-MEANING case a parameter of an existing TC-147 test (TC-147's evidence
  unchanged); three row wordings corrected against their tests; forced by
  checks, a helper split for the cognitive limit, a paid-down complexity row
  deleted, `trace.py`'s SLOC baseline 3847 -> 3861, the smoke `max-tests`
  3890 -> 4060, the acceptance-brief golden and the LF-site pin moved. The
  Deliverable holds each, with its reason.
- **Byte deltas on budgeted files:** none (no budgeted file touched).
- **Tests:** red first `27 failed, 8 passed in 53.62s`; the 86 importer and
  named modules `3 failed, 3134 passed, 2 skipped, 18 warnings in 3165.81s`
  (the three fixed and rerun, `6 passed in 10.95s`); `run_menu.py smoke`
  `3902 passed, 3 skipped, 18 warnings in 232.54s`, exit 0 (CPU 842.0 s over
  the 540 s budget, reported only); `trace.py --strict` and
  `check_trajectory.py --strict` exit 0. The unfiltered suite is the
  coordinator's, before the merge.

<!-- fig: cmd="python -m pytest -q -n auto -p no:cacheprovider --basetemp <scratch> <the 86 modules>; python project-trajectory/scripts/run_menu.py smoke" rev="maint/wi-1069 at 144f9d8ef (module run) and 5f3907bb7 (smoke), 2026-11-23" -->
- Deferred open items: none — the operator owes no decision from this row;
  every amended and minted row goes to the next sitting as an owed act.
- Review round 1: Hydrogen APPROVE; Sol (code and docs halves) one MAJOR,
  adopted (the RESYNC entry now says to take and land held CLARITY acts
  before upgrading, and how a leftover row is re-sat), and one MINOR,
  adopted (LLR-484 states that a lone accepted group stays unlabelled;
  TC-571's expected names it). The builder's smoke re-stamp and new module
  confirmed.
