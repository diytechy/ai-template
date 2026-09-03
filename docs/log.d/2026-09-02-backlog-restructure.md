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

**Full suite at the round-1 fix tip `503b2b53`** (real tail):

```
FAILED tests/test_gen_trajectory.py::test_cancelled_wi_renders_its_own_bucket
1 failed, 3304 passed, 20 skipped in 615.53s (0:10:15)
```

The one red is round 1's own regression: the dashboard legend rewrite dropped
the phrase `cancelled — won't build` that WI-267's test pins. Fixed in round 2.

### Review round 2 — Sol (6 findings) and Opus (8 findings) over `891a5b24..503b2b53`; no BLOCKER; fix commit `dc3c9e68`

Both reviewers first re-verified every round-1 fix — the R-F carve-out
matrix, the eight rows' byte identity, all eleven verbatim blocks, the
frontier, the 11 → 4 pair count re-derived from a clean worktree at
`891a5b24`, the ratchet stamps, the byte budgets — and reported them
reproduced. Then, what the fixes had opened:

- *A successor re-pointed to itself* (both, MAJOR). Round 1's
  `_replace_inbound_edges` excluded the minted successor from its sibling set
  and ran the direct-replacement arm before any exclusion, so a successor
  whose own `needs` named the absorbed row ended up waiting on itself — a
  strand no validator reports. Reachable by WI-583's QUEUE-WITH-EDGE arm.
- *The accumulate arm guessed* (both). It appended a later successor to any
  open row that named an earlier one, which cannot tell a rewritten dependent
  from a row naming that successor on purpose, and printed a re-point message
  for an edge that never existed. `dc3c9e68` replaces the heuristic with what
  Sol named: the mint knows every draft, so `_apply_supersedes` runs ONCE
  after all drafts are on disk, inverts absorbed → successor set, and each
  dependent's absorbed tokens are replaced by the whole set in one write. A
  row is a non-dependent by its own `supersedes` cell, never by the shape of
  its `needs`. Tests: three successors + one dependent (union, message names
  all three); a successor naming the absorbed row is untouched; an unrelated
  row naming successor 1 gains nothing; overlapping sets dedupe.
- *Lineage cycles passed* (Sol MAJOR, Opus MINOR): a restructured row naming
  itself, a duplicated successor, a successor that is itself restructured.
  `_restructured_successor_refusal` now asks five ordered questions (self,
  duplicate, exists, not itself restructured, mutual); the mint refuses a
  draft superseding an already-restructured row at the authoring boundary.
- *Four rows moved off the armed complexity ratchet unstamped* (Opus MAJOR):
  `schedule._waiting_reasons`, `intake._mint`, `intake._replace_inbound_edges`
  (twice, once DOWN — the re-stamp round 1 owed), `check_trajectory.load_wis`.
  Three repaired by extraction, the fourth re-stamped down;
  `check_complexity --mode enforce` exits 0 ("200 row(s) over 15, unchanged
  from baseline").
- *Authoring grammar* (both, MINOR): a hand-authored `supersedes =
  "WI-558;WI-559"` was accepted because the registry-cell reader was reused;
  a string is now exactly one id, several is a TOML list, and the `;` split
  reads the cell only. The `supersedes_ids` docstring argued for one
  separator class while the regex had two; now one.
- *The legend regression* above; `docs/enforcement-audit.md` rows for the new
  R-A error class and the R-F carve-out; PROCESS_OPTIONS "(surrounding
  whitespace ignored)" (+111 bytes, watched).
- *Records* (Opus MINOR): plan §2.4 step 6's replaced criterion is restated
  AS a replacement with the reason; plan §5 records the rule round 2 stated —
  amend a description freely and inline, move an acceptance criterion only
  with the reason in the criterion. Both reviewers judged round 1's declined
  finding (plan amendments) correctly declined.

Ratchets in `dc3c9e68` (reasons in the baseline entries):
`check_trajectory.py` 2310 → 2327, `intake.py` 1305 → 1343; smoke
collection 1477 against the 1480 ceiling.

**Full suite at `dc3c9e68` + this record** (real tail):

```
3309 passed, 20 skipped in 611.56s (0:10:11)
```
