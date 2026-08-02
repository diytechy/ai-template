## 2026-08-01 — WI-392: declared figures carry their command and revision (rung 1)

**Summary.** The declared-figure convention plus its presence check, rung 1
only per the drain plan (row 6): a driven figure may opt in by carrying, on
its own line, the marker `fig: cmd="<command>" rev=<revision>` — or
`fig: derived="<how, from which declared figures>"` for a figure computed
from declared ones — and the new `project-trajectory/scripts/check_figures.py`
(opt-in `[step:figures]`, G3 product layer, warn-first, `--strict` gates)
flags a declared figure carrying neither. PRESENCE, never truth: the marker is
opt-in because digit detection drowns in ids/dates/section numbers/byte
budgets (one of the three motivating false figures had no digits at all), so
the check's honest claim is "declared figures carry provenance", never "all
figures do". The convention has one home —
`project-trajectory/PROCESS_OPTIONS.md` "Signed measurements" part 3, carrying
both acceptance bars (the cmd enumerates the population it was computed over,
or names the selection principle; a derived figure is itself declared) — and
every other surface links to it. **Rung 2 (re-derivation) is deliberately NOT
built and is recorded as a declared absence** in the
[enforcement audit](../enforcement-audit.md) signed-measurement row (truth
stays Reviewer; presence is now Harness): recorded commands are an execution
surface needing an allow-list, most figures are legitimately historical, and
some commands are expensive or non-deterministic.

- **Deliverables:** `project-trajectory/scripts/check_figures.py` (the
  presence check); `tests/test_check_figures.py` (13 tests, watched red
  first, the three 2026-08-01 false figures as fixtures — each flags under a
  bare marker); the PROCESS_OPTIONS.md convention text; `docs/stack.ini`
  `[step:figures]` + its re-measure note re-pointed at the check (it used to
  ask a human); the enforcement-audit row split with rung 2 declined;
  `check_doc_refs.py` gains the lifted `authored_lines` walk (IF-087, shared
  with the new check). Registration: SR-136 + LLR-146 + TC-140 (CMP-003),
  IF-086/IF-087, CMP-003 description, bootstrap MAPPING/docstring +
  `tests/test_bootstrap.py` list, the kit README row, dupes census cli class
  86 -> 90 (audit literals re-pinned), `docs/gate` basis regenerated, the
  session-protocol skill's record-the-work bullet linking the convention +
  the byte-budget-guard baseline re-stamp (skill source and both per-agent
  copy trees, byte-identical). WI spec closed to
  `docs/work/complete/WI-392-driven-figures-carry-their-command.md` with
  `specref` cleared (R-F); spec-of-record archived to
  `docs/archive/specs/WI-392.2026-08-01.md` via the `spec_move.py --archive`
  ritual (WI-393's), which redirected the two inbound `docs/log.md` link
  targets itself — the deviation WI-394 recorded by hand is retired.
- **Deviations from spec:** (1) built as a new script rather than the
  check_docs arm the spec left open — a separate seam keeps the honest-claim
  docstring and the opt-in step independent, at the price of the full
  registration, which is filed; (2) the shared GENERATED-block walk was
  lifted into `check_doc_refs.authored_lines` (behavior-preserving, its suite
  green) instead of copied — the check_dupes gate red on the copy, and only
  the F5-sanctioned `_utf8_console`/CLI-preamble boilerplate joined the
  census; (3) `docs/gate` was regenerated on this work branch —
  `tests/test_derive_gate.py`'s dogfood cache check requires the committed
  cache to track the new spine rows (its failure message names the remedy;
  the WI-393 precedent) — while all other generated artifacts stay
  trunk-lane; (4) the enforcement audit's existing signed-measurement row was
  rewritten in place (Reviewer for truth + Harness for presence) rather than
  a second row appended — same rule, one home.
- **Watched, measured on the build commit 83ebd450 (clean tree):** module
  suite 13 passed in 0.46s
  <!-- fig: cmd="python -m pytest -q tests/test_check_figures.py" rev=83ebd450 -->
  (watched RED first: 13 failed in 0.23s on the claim tree with the script
  absent — historical, that tree is gone); smoke tier 607 passed / 6 skipped
  in 9.45s
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=83ebd450 -->
  (membership 613 within the 640 ceiling, no re-stamp); full suite 1835
  passed / 10 skipped in 0:04:43
  <!-- fig: cmd="python -m pytest -q -n auto" rev=83ebd450 -->;
  `check_figures` / `check_doc_refs` / `check_trajectory` all rc=0 under
  `--strict`; `check_dupes` rc=0; `check_docs --stale` stays at the
  pre-existing trunk red of 4 broken links
  <!-- fig: cmd="python project-trajectory/scripts/check_docs.py --root . --stale" rev=83ebd450 -->,
  the same WI-070/WI-173/WI-288 record lines WI-394's close reported, none
  added by this branch. The close commit after those measurements touches
  record surfaces only.
- **Byte deltas:** AGENTS.template.md 9,991 (untouched); PROCESS.md 64,319
  (untouched); PROCESS_OPTIONS.md 166,314 -> 167,884
  <!-- fig: cmd="wc -c project-trajectory/PROCESS_OPTIONS.md" rev=83ebd450 -->
  — a flagged growth of +1,570
  <!-- fig: derived="167,884 minus the 166,314 WI-378 baseline, both wc -c readings" -->
  for the convention text and the enforcement-split paragraph, baseline
  re-stamped in every tracked skill copy in the same commit.
