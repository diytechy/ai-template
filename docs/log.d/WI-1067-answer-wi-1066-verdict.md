## 2026-11-23 — WI-1067: WI-1066's verdict answered: SR-207 fronts its event and states its retirement rule; TC-560 drives two more faults

Built on `maint/wi-1067`, cut from `refactor_again` at `d62f3c74b`, planning
`none`. The spec's Deliverable holds the per-item record, the mutations and
the acts owed.

- **SR-207** (text only, still `Accepted`): its requirement opens "When the
  kit takes an acceptance act, it shall leave ..."; its acceptance criteria
  gain the retirement rule (an unnamed recorded accepted row live no longer
  carries stays in the copy, named owed, until an act naming it retires it),
  driven by TC-240's existing removed-row test; its rationale's adjudicated
  links name a requirement's or design row's constrains link.
- **The constrains link, confirmed.** The record keeps a row whose constrains
  link alone moved: the code routes that cell for both tiers, and a new
  TC-240 test drives it through the snapshot command (LEFT OWED, listed in
  `kept`, recorded from live once an act names it).
- **TC-560** (still `Drafted`): its method, expected and tests drive LLR-480's
  two missing faults, a parent cell naming an example row and a row below a
  cycle, at both statuses through the orphan pass and the strict check. The
  code already did both; each new test was shown to bite under a temporary
  mutation, none committed.
- **Rows.** SR-207 amended (owed to the next sitting with WI-1060's
  amendment); TC-560 rewritten (owed a first acceptance). No id minted, no
  status moved, no kit file changed.
- **Left for the coordinator:** LLR-245's list of routed cells does not name
  the constrains cell, which the code routes and SR-207 now names; not
  amended here.
- **Deviations from spec:** none.
- **Byte deltas on budgeted files:** none touched.
- **Tests:** the seven touched and ratchet modules `317 passed, 1 skipped in
  79.30s (0:01:19)`; `trace.py --strict` and `check_trajectory.py --strict`
  exit 0; `run_menu.py smoke` `3882 passed, 3 skipped, 18 warnings in
  138.61s (0:02:18)`, exit 0 (CPU 720.6 s over the 540 s budget, reported
  only).

<!-- fig: cmd="python -m pytest -q -n auto tests/test_requirement_tree.py tests/test_baseline_snapshot.py tests/test_record_rows.py tests/test_import_layers.py tests/test_module_size_ratchet.py tests/test_complexity_ratchet.py tests/test_dogfood_sync.py; python project-trajectory/scripts/run_menu.py smoke" rev="maint/wi-1067 at 5cf590b93 and its close-out tree" -->
- Deferred open items: none — SR-207's amendment and TC-560's first
  acceptance go to the next sitting as owed acts, and LLR-245's gap is the
  coordinator's to route.
