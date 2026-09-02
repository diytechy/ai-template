## 2026-09-02 — the backlog restructure: WI-579..583 minted, eight rows archived as restructured, the frontier re-sequenced, two adversarial rounds applied

Executed out of band (owner direction, this date) per
`docs/plans/2026-09-02-backlog-restructure-and-consolidation.md` §2.4 steps
3–7, on top of the vocabulary commits `038a16a7` (the `restructured` terminal
state) and `36395b54` (list-valued `supersedes`) recorded in
`2026-09-02-restructured-vocabulary.md`.

**Step 3 — the mint (`1c0fb2d6`).** Five drafts through `intake._mint`, the
same path every mechanical mint takes: ids from the watermark (WI-579..583;
mark bumped to `WI = 583` by `trace.bump_watermark` in the same commit),
Context written with the registry joins, `supersedes` lists applied. The
absorbed rows' Done-when blocks are quoted under their old ids in each
successor's Context.

**Step 4 — the moves (`c16182cb`).** WI-558, 559, 560, 561, 562, 564, 565,
576 moved `queued/ -> docs/archive/work/restructured/` with `spec_move.py`
(links redirected) and a one-line `## Deliverable` naming the successor(s)
placed before `## Context`. No open row hard-depended on an absorbed id, so
`_replace_inbound_edges` had nothing to re-point.

**Step 5 — the kept rows.** `WI-551` `needs = ["WI-579", "WI-580"]`,
`priority = 7`; `WI-541` `priority = 7`; `WI-545` `needs = ["WI-579",
"WI-580", "WI-581", "WI-551", "WI-583"]`, `priority = 1`.

**Full suite at `c16182cb`** (`python -m pytest -q -n auto`, real tail):

```
3300 passed, 20 skipped in 582.93s (0:09:42)
```

### Review round 1 — OpenAI Sol (codex, medium; 8 findings) and Opus (15 findings), one hostile brief; no BLOCKER

**What the first execution got wrong, and the fix commit for each.**

- *The specref remedy was backwards* (Opus MAJOR). The strict check errored
  R-F on all eight rows, and step 4 cleared `specref` and amended the plan to
  say so. The R-F `partial` carve-out's own reason — the successor's
  `supersedes` lineage is worth nothing if the thread it continues has been
  cut — applies to an absorbed row word for word. `8fa0f0f3` extends the
  carve-out (`_SPECREF_MAY_STAY = ("partial", "restructured")`); this commit
  restores the eight rows' original `specref`, so each archived row is again
  byte-identical to its `891a5b24` text plus the one Deliverable line
  (verified by `diff` against `git show 891a5b24:…` for all eight). Plan §1.5
  corrected.
- *Quote fidelity* (both reviewers). Two `[...]` elisions of WI-559's item 3,
  WI-560's item 4 ("Tests drive all three") dropped from every successor, and
  a "From WI-565 (verbatim)" block that was a rewrite. `3edb7e85` quotes all
  of them in full with headings that say what they hold; the OI-77 ruling is
  noted outside the quote.
- *Deliverable grammar* (Sol MAJOR). Three multi-successor Deliverables
  carried parentheticals and nothing checked the form. `3edb7e85` sets one
  grammar (`Restructured into WI-a, WI-b.`); `8fa0f0f3` adds
  `check_trajectory._restructured_lineage_findings` — the line must match
  `^Restructured into WI-\d{3,}(, WI-\d{3,})*\.$` and every named successor's
  `Supersedes` must name the row back (ERROR under `--strict`, R-A class).
- *Many-to-many `supersedes`* (Sol MAJOR). One absorbed row split across
  three successors re-pointed a dependent to the first successor only.
  `8fa0f0f3`: a later successor over the same absorbed set is appended to any
  open row already naming an earlier one, so a dependent accumulates the
  union; and `supersedes_ids` now reads the `;`-joined cell `_draft_row`
  writes (Opus MINOR).
- *The frontier order* (both). Declaring `WI-582` `spine` put it at rank 0,
  and a READY spine row stops all admission until it runs — so it would have
  run before `WI-579`, the owner's first priority. `3edb7e85` gives `WI-582`
  `needs = ["WI-579", "WI-580"]`; plan §2.3 and §2.4 step 6 corrected.
- *Readers still missed* (both): `traj_panels`'s closed set (done/cancelled
  only — `partial` was already missing), the dashboard legend (`⇥`, and the
  pre-existing undocumented `◐`), `PROCESS_OPTIONS.md`'s five vocabulary
  sentences, two docstrings in `kitlib/registry.py` and one MAPPING comment
  in `bootstrap.py`, the `test_bootstrap` scaffold folder list, and
  `test_integrate_admission` reaching none of the changed code — all in
  `8fa0f0f3`. `RESYNC_PACK.md` gains the missing `36395b54` entry (the two new
  mint refusals an adopter can hit).
- *Log honesty* (both). The first fragment said the shared-spec warnings
  "fell from eight pairs to two"; the rule strips `#anchors`, so the base was
  **11** pairs (559/560/561/562 → 6, 564/565, 576/577, 556/557/558 → 3) and
  the result is **4** (556/557, 556/579, 557/579, 580/581), each a group that
  IS one ruling by design. The scheduler excerpt had columns trimmed; the
  unabridged output is below. `docs/stack.ini`'s smoke stamp claimed a
  measurement at clean `891a5b24` that was taken dirty — `0c245f2b`
  re-measures at `8fa0f0f3` (1476 collected, ceiling 1480).
- *Not applied*: Sol's MINOR that amending the plan after execution is out of
  scope. The plan is the plan of record and carries its corrections dated and
  inline (plan §5); silently leaving it asserting an order the machinery does
  not produce is the worse record.

**Ratchets in `8fa0f0f3`** (reasons stamped in the baseline entries):
`check_trajectory.py` 2275 → 2310 (the lineage findings arm and the
carve-out, after compacting message templates), `intake.py` 1286 → 1305 (the
two extractions `_open_specs` / `_repointed_needs` that keep
`_replace_inbound_edges` under C901).

### Verification at this commit, real output

`.venv/bin/python project-trajectory/scripts/schedule.py ready --explain`,
open rows only, unabridged:

```
WI-582     waiting   exclusive    rank=0 P4   down=0   path=0   waiting:hard-preds-not-done:WI-579,WI-580
WI-578     ready     exclusive    rank=1 P0   down=0   path=0   exclusive:adjudication;ready
WI-579     ready     parallel     rank=6 P9   down=5   path=2   parallel:ordinary;ready
WI-580     ready     parallel     rank=6 P8   down=4   path=2   parallel:ordinary;ready
WI-551     waiting   parallel     rank=6 P7   down=2   path=1   waiting:hard-preds-not-done:WI-579,WI-580
WI-541     waiting   parallel     rank=6 P7   down=0   path=0   waiting:hard-preds-not-done:WI-551
WI-581     ready     parallel     rank=6 P6   down=1   path=1   parallel:ordinary;ready
WI-570     ready     parallel     rank=6 P5   down=2   path=2   parallel:ordinary;ready
WI-583     waiting   parallel     rank=6 P5   down=1   path=1   waiting:hard-preds-not-done:WI-579,WI-570
WI-577     waiting   parallel     rank=6 P4   down=0   path=0   waiting:open-item-pending:OI-82
WI-557     ready     parallel     rank=6 P3   down=0   path=0   parallel:ordinary;ready
WI-536     ready     parallel     rank=6 P2   down=0   path=0   parallel:ordinary;ready
WI-539     ready     parallel     rank=6 P2   down=0   path=0   parallel:ordinary;ready
WI-556     ready     parallel     rank=6 P2   down=0   path=0   parallel:ordinary;ready
WI-545     waiting   parallel     rank=6 P1   down=0   path=0   waiting:hard-preds-not-done:WI-579,WI-580,WI-581,WI-551,WI-583
```

`WI-578` is the first READY row; `WI-545` is no longer ready (the §2.1
contradiction); `WI-582` classifies `spine` and waits on 579+580.

`check_trajectory.py --strict`: ONE error, pre-existing and now owned by
`WI-582` — `cross-component import scripts/schedule (CMP-008) -> scripts/trace
(CMP-006) has no declared IF-### seam`. Shared-spec pairs: the four named
above. `trace.py --strict-integrity`: integrity=0, orphans=2 (unchanged).
`docs/status.md` regenerated; zero absorbed ids remain in it.

The full unfiltered suite at the round-1 fix tip is recorded in the follow-up
entry below once it has run.
