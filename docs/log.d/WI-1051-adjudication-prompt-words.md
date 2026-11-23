## 2026-11-22 — WI-1051: the act brief names the repository's own scripts directory, and the first-acceptance brief asks for ACCEPT

Deferred open items: none. The row changes two prompt templates, the act
assembler and four test modules, and takes no operator decision; it needed
no decisions record.

Built on the maintenance branch `maint/wi-1051` from `3c33b3783`, with the
commit hooks on. The record is in the row's Deliverable
(`../archive/work/complete/WI-1051-adjudication-prompt-words.md`).

- **The act's scripts directory:** the act template takes the `{scripts}`
  value the reviewer and worker briefs take, in its instructions and in the
  commands the act assembler renders, so an act taken here runs
  `project-trajectory/scripts/intake.py` and one taken in a scaffold
  `scripts/intake.py`. A new TC-368 test composes the act in both layouts.
  The coordinator-act stub finds a command by its script, and the act
  brief's pinned slot set gains `scripts`.
- **ACCEPT, not APPROVE:** the first-acceptance brief now asks for `ACCEPT`
  where it said `APPROVE`. A new test in `tests/test_prompts.py` (TC-157's
  module) reads every machine-line word each of ten briefs asks for against
  the grammar its verdict is parsed with; it was red on the first-acceptance
  brief alone.
- **Catalogue:** `prompts/CATALOG.md` regenerated (both digests; `{scripts}`
  in the act's slots).
- **Re-sync:** a `RESYNC_PACK.md` §4 entry anchored at `3c33b3783` for the
  three shipped files, which the smoke checks' re-sync step asked for.
- **Tests:** the sixteen modules importing the act assembler, holding the
  touched cases' tests, reading the two templates or the catalogue, and the
  three whole-tree tests: `584 passed, 1 skipped in 1641.19s (0:27:21)`
  (a loaded box); the re-sync pack's five readers: `55 passed in 10.93s`.
  `trace.py --strict`: `orphans=0 integrity=0`; `check_trajectory.py
  --strict`: clean. `run_menu.py smoke`: `3737 passed, 3 skipped, 18 warnings in 293.37s (0:04:53)`,
  with a CPU budget WARN only.
  <!-- fig: derived="the totals are those the Deliverable's Tests list declares, each with its command and revision" -->
- **Byte deltas:** no budgeted or watched file was touched.
- **Acts owed:** none. No row text was written or amended; TC-368's
  regenerated `evidence` routes nothing.
- **Downstream:** an operator override of `ADJUDICATE-ACT` must now declare
  `{scripts}`, or the strict fill refuses it naming the slot.
- **Left open:** LLR-338's accepted Detail still says "APPROVE" for a first
  acceptance; amending it is outside this row.
