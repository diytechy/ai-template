+++
id = "WI-749"
title = "adjudicate: LLR-116, TC-121 - approved/routed cell(s) amended on merged trunk 2a902b5..6a40d7b (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "medium"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-116", "TC-121", "TC-262", "TC-263", "TC-264", "TC-267"]
+++

## Deliverable

Spine-acts sitting, one act (seq 14): an independent Claude Opus 5.5 adjudicator
ruled all six rows MEANING and re-attested them; no Dispositions.

- **LLR-116 `detail`, TC-121 `method` and `expected`** (WI-722's shrink floor): the
  min-width is now `ceil(natural x 9 / smallest NODE_TYPE_PX token)`, not the 0.62
  ratio; the new text is true of `traj_render._svg_fit_style` and the t7 tests.
- **TC-262, TC-263, TC-264, TC-267 `method`** (`3e0a5f48`, WI-541's live
  recordings): the required evidence moved from documented-shape fixtures to live
  recordings; the golden session files carry no NOT LIVE line.
- **Noted, not returned:** TC-264's unchanged clause says codex's cache write stays
  empty, true of the adapter today though the live line reports it; WI-748 reads
  the field and amends the clause.
- **Act:** `intake.py snapshot --reattests LLR-116,TC-121,TC-262,TC-263,TC-264,TC-267`.
  Taken on the lane at 1875db7c, then retaken by the coordinator on the merged tree
  (trunk had gained WI-746's Drafted rows since the lane was cut):
  `refresh_refusal` returned no refusal for the same arguments, `last_approved/`
  was reset to trunk, and the exact command re-run.
- **Review:** Sonnet 5.5 cross-review SOUND at 1875db7c (two minors noted).
- Verdict: `docs/reviews/wi-749-adjudicate-llr-116-tc-121/001-ADJUDICATE-579cd18.md`.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-116 `Detail`: 'The mechanized core of usability anchor T7 (docs/rubrics/dashboard-usability.md). Every emitted SVG (all three wrappers…' -> 'The mechanized core of usability anchor T7 (docs/rubrics/dashboard-usability.md). Every emitted SVG carries width:100% …'
- TC-121 `Expected`: 'Every emitted svg scales to fit its container; zero svgs keep the pre-fix fixed-width shape; the shrink floor is pinned…' -> 'Every emitted SVG scales to fit its container; zero SVGs keep the pre-fix fixed-width shape. Every emitted node type to…'
- TC-121 `Method`: 'Generate the dashboard and derive EVERY emitted <svg> from the document (not a hand list, so a fourth emitter cannot sk…' -> 'Generate the dashboard and derive EVERY emitted <svg> from the document (not a hand list, so a fourth emitter cannot sk…'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Carried 2026-10-02 by the coordinator (wave 7): TC-262, TC-263, TC-264 and
TC-267's approved `method` cells were amended on trunk outside a lane by
`3e0a5f48` (WI-541's live codex and opencode recordings: each method now says
its fixture is a live recording rather than a documented-shape one), so no merge
minted an adjudication for them. `docs/ratify/CURRENT.md` lists them. Judge them
in this sitting with the same outcomes.
