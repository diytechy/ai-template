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
- **LLR-245** (text only, still `Accepted`), on the coordinator's ruling of
  2026-11-23: its list of routed trace cells gains `Constrains` on a
  requirement and on a design row, so it says what the code does and what
  SR-207's amended rationale says. TC-240's new constrains test drives it.
- **Rows.** SR-207 and LLR-245 amended (owed to the next sitting, SR-207
  with WI-1060's amendment); TC-560 rewritten (owed a first acceptance). No
  id minted, no status moved, no kit file changed.
- **Deviations from spec:** LLR-245's amendment, outside the spec's
  Done-when, added on the coordinator's ruling.
- **Byte deltas on budgeted files:** none touched.
- **Tests:** the seven touched and ratchet modules `317 passed, 1 skipped in
  79.30s (0:01:19)`; `trace.py --strict` and `check_trajectory.py --strict`
  exit 0; `run_menu.py smoke` `3882 passed, 3 skipped, 18 warnings in
  138.61s (0:02:18)`, exit 0 (CPU 720.6 s over the 540 s budget, reported
  only). After LLR-245's amendment: the three touched modules `261 passed in
  83.71s (0:01:23)`; `trace.py --strict` and `check_trajectory.py --strict`
  exit 0.

<!-- fig: cmd="python -m pytest -q -n auto tests/test_requirement_tree.py tests/test_baseline_snapshot.py tests/test_record_rows.py tests/test_import_layers.py tests/test_module_size_ratchet.py tests/test_complexity_ratchet.py tests/test_dogfood_sync.py; python project-trajectory/scripts/run_menu.py smoke; the first three modules again after LLR-245's amendment" rev="maint/wi-1067 at 5cf590b93, its close-out tree, and 8b3f62154 plus LLR-245's amendment" -->
- Deferred open items: none — SR-207's and LLR-245's amendments and TC-560's
  first acceptance go to the next sitting as owed acts.
- Review round 1: Sol and Hydrogen APPROVE, no findings.
