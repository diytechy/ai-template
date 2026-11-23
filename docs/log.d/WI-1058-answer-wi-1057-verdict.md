## 2026-11-23 — WI-1058: WI-1057's verdict answered: SR-251's trigger fronted, and TC-483 covers LLR-406's key insertion and sorted append

Deferred open items: none. The row changes spine text, one test module and
the regenerated evidence and views; every choice it made is stated by a
spine row, so it needed no decisions record.

Built on the maintenance branch `maint/wi-1058` from `8db60ba58`, with the
commit hooks on and planning `none`. The record is in the row's Deliverable
([WI-1058](../archive/work/complete/WI-1058-answer-wi-1057-verdict.md)).

- **SR-251:** its requirement opens "When requested, the delivered harness
  shall rewrite ...", one `shall` with nothing between it and its verb. Two
  absolutes are bounded by naming their domain ("every other part of the
  cell", "anything else in the registry"); the row has no absolute-term
  advisory left.
- **TC-483:** two new tests drive the regeneration command. A case with no
  evidence key, set mid-registry among comments, current cases and a prose
  line that reads as an evidence key, gains its key, and taking that one line
  back out gives the registry's bytes as written. Three missing declared
  tests, defined out of sorted order, are appended after the part the cell
  names, joined by `; `, in sorted order. The method and expected name both;
  "the command names the cases it changed" moves to the scenario whose test
  asserts it, and "the command exits 0", which neither parent states, is
  cut. Evidence regenerated from the tags.
- **Bite:** both tests passed on the code as it stood, so each was shown red
  under a temporary mutation of `arch_tags.py`, never committed: a blank line
  after the inserted key, multi-line strings untracked, the appended nodes
  reverse-sorted, and the join without its space. The second and third are
  caught by no other test.
- **LLR-406:** text unchanged; its flip stays owed under WI-1057's verdict.
- **Tests:** the trace-cells, import-layer, size-ratchet and dogfood-sync
  modules: `75 passed, 1 skipped in 11.68s`. `trace.py --strict`:
  `orphans=0 integrity=0`; `check_trajectory.py --strict`: clean.
  `run_menu.py smoke`: `3751 passed, 3 skipped, 18 warnings in 120.43s
  (0:02:00)`, with a CPU budget WARN only.
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
- **Byte deltas:** no budgeted or watched file was touched.
  `system-requirements.toml` +31, `test-cases.toml` +821,
  `test_llr_trace_cells.py` +2,633.
- **Owed to the next sitting:** the first acceptances of SR-251 and TC-483.
- **Review:** Sol (low) over the whole diff and Hydrogen (low) over the
  prose: both `VERDICT: APPROVE findings=0`; no change after the review.
