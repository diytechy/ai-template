## 2026-11-23 — WI-1027: design rows decompose under one parent row, and every walk from a requirement to its design rows walks the tree

Deferred open items: none. The one design call no spine row states, the
`Parent` cell's class in the acceptance record's cell split (accepted), is
recorded in `docs/decisions/maint-wi-1027.toml` D-001 at the coordinator's
ruling; the parent-first rule's extension to the parent link is a follow-up
row the coordinator files on trunk.

Built on the maintenance branch `maint/wi-1027` from `bba30552f`, with the
commit hooks on, under the plan `docs/plans/WI-1027/plan.md` (`578416476`)
and the coordinator's go-ahead, which approved it with rulings on D1 to D15.
The record is in the row's Deliverable
(`../archive/work/complete/WI-1027-parent-llr-link.md`).

- **The cell:** an optional `parent` on a design row names one other design
  row; a child carries no `sr_refs`, and its SRs are read up its chain. The
  orphan pass reports a top-level row naming no SR, a child naming SRs, a
  parent cell naming no live design row or several, each row on a cycle and
  each row whose chain breaks; `--strict-schema` asks `SR-Refs` of a
  top-level row only. The cell is accepted text: a re-parent is an amendment.
- **The walk:** `kitlib.spine.llr_tree` answers both directions once and
  never follows a cycle; every reader that relates an SR to its design rows
  takes it (the review test set, the orphan and triangle rules, the stage's
  phase grouping, the acceptance and adjudication briefs, the context block,
  the report's views, the component view, the architecture arm's reach, the
  test-first order and five more). Blast radius is WI-1024's to put on it.
- **A parent's discharge:** LLR-408's rule already discharges a design row
  only by a case naming it, so a parent needs its own integration TC; the
  finding on a parent past Drafted says its children's cases do not
  discharge it.
- **The dashboard:** the spine view draws a child inside its parent, one
  design column per tree depth; this repository, with no child, renders as
  before.
- **Docs:** PROCESS.md §4 states decomposition (b) once (+537 bytes on the
  watched file, re-stamped); the spine-authoring and gate-advance skills and
  `spine-questions.md` point at it; the registry machinery reference and a
  RESYNC entry follow.
- **Rows:** LLR-480, LLR-481, LLR-482 and TC-560 to TC-567 (Drafted);
  LLR-367, LLR-244 and LLR-257 amended in `detail`, text only. LLR-001,
  LLR-201, LLR-186 and LLR-197 stay as they are, the Deliverable quoting each
  clause and why it holds.
- **Ratchets:** `trace.py` +46 SLOC (3784 -> 3830), a reviewed bump whose
  reason is in its entry: the walk's readers and the outward decomposition the
  cognitive-complexity census asked for; `check_trajectory.py` and `intake.py`
  down by one; no complexity baseline rose.
- **Tests:** every new case was run red against its unchanged reader first.
  The 181-module rule-5 set: `1 failed, 6052 passed, 19 skipped, 18 warnings in 6199.58s (1:43:19)`, the one failure a race with this lane's own spec move during the run; the module alone on the settled tree, `67 passed in 2.07s`.
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
  `trace.py --strict` and `check_trajectory.py --strict` exit 0;
  `run_menu.py smoke` passed (the Deliverable quotes it).
