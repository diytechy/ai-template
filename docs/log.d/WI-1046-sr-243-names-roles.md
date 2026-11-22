## 2026-11-21 — WI-1046: SR-243 names the author, critic and REVIEW-A calls, not Sol or Terra

Deferred open items: none. The row changes text only and takes no operator
decision; it needed no decisions record.

Built on the maintenance branch `maint/wi-1046` from `660805e62`, with the
commit hooks on. The record is in the row's Deliverable
(`../archive/work/complete/WI-1046-sr-243-names-roles.md`).

- **SR-243** (Accepted, text only; `e8969307a`): its requirement now ends
  "provide the sole launch route for author, critic and REVIEW-A calls", and
  its acceptance criteria name "the coordinator-call route as the only
  launch path for author, critic and REVIEW-A calls", TC-385's words after
  WI-1044, where both named "Sol or Terra". Its status and every other cell
  are unchanged.
- **Pins:** none; no test quoted either old phrase.
- **Tests:** the 36 modules reading the live requirement registry, TC-385's
  chain or the generated views, and the whole-tree tests:
  `1150 passed, 3 skipped, 18 warnings in 984.28s (0:16:24)`.
  `run_menu.py smoke`: `3714 passed, 3 skipped, 18 warnings in 288.04s (0:04:48)`,
  with a CPU budget WARN only. `trace.py --strict`:
  `orphans=0 integrity=0`; `check_trajectory.py --strict`: clean.
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
- **Byte deltas:** no budgeted or watched file was touched.
  `system-requirements.toml` +50.
- **Acts owed:** SR-243's drift, for automated adjudication (its chain in
  `docs/ratify/CURRENT.md`, "Waiting for automated adjudication").
- **Review:** round 1, OpenAI Sol (low) and Gemini Hydrogen (low, the
  Antigravity CLI): both `VERDICT: APPROVE findings=0`.
