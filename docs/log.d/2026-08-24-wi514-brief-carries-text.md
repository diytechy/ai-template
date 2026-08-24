## 2026-08-24 — `WI-514` puts the anchor SR's own reviewable text on both approval surfaces

Owner-directed, in-session, reviewing `SR-177`'s entry on `docs/open-items.html`,
verbatim: *"if I open open-items.html, and look at SR-177, I don't see the
actual requirement text in that document to be able to review."*

**The finding.** `trace.reattest_model` (widened yesterday by `WI-513` to ask
the `Drafted` question of every chain row, not just the SR) already selects
the right SET of owing rows and already renders most of their text: a
`Drafted` LLR/TC's full cells (`_full_row_bullets` /
`gen_open_items._chain_row`'s non-diff branch) and a drifted cell's
before/after (`_cell_diff_lines` / the HTML word-diff) both render
un-hidden. What neither renderer ever rendered is the ANCHOR SR's own text
when the SR row itself carries no diff and is not `Drafted` — exactly
`SR-177`'s shape: `Approved`, undrifted, its whole amendment living in
`Drafted` children `LLR-196`/`TC-191`. In that shape `reattest_model` never
appends the SR to `entry["rows"]` at all (the `if cells or drafted:` gate in
`reattest_model`), so:

- the markdown brief's `## SR-177 — …` section skipped straight to its chain
  rows, no `### SR SR-177` block at all;
- the HTML card's ONLY copy of the SR's `Requirement`/`Rationale` sat inside
  `_context_block`'s `.ctx` div — `display:none` until the "Collapse
  unchanged text" toolbar checkbox (checked by default) is cleared.

Present in the bytes, invisible on load. Exactly the owner's report.

**The render design, in three sentences.** A new `trace.truncate_cell`
(1,500-char threshold, explicit `"… [N more chars — read the registry row]"`
marker, never silent) is the one shared truncation both renderers import
rather than re-deriving. `trace._anchor_lines` (markdown) and
`gen_open_items._anchor_block` (HTML) render the anchor SR's own
`Requirement`/`Rationale` UNCONDITIONALLY — for every entry, right after the
`## SR-ID — Title` heading in the brief and, in the HTML, in a plain
`<div class="anchor">` sitting BEFORE the collapsible `.ctx` div rather than
inside it, so it is on the page with no interaction; `_context_block`'s
existing "rest of the SR" block is told to skip `Requirement`/`Rationale`
(`_ANCHOR_CELLS`) so the two never render twice. The same `truncate_cell` was
threaded through the two places that already rendered full cell text
(`_full_row_bullets`, `gen_open_items._chain_row`'s full-cell branch) so a
long `Detail`/`Method` degrades the same explicit way rather than only the
new anchor block getting the protection.

**Not done, deliberately:** no row's `Status` was flipped and nothing was
approved — the corrected surface is what the owner reviews from, same
discipline `WI-513` held.

### `SR-177`, before and after (the acceptance evidence)

**Before** (both surfaces, prior to this WI): `docs/open-items.html`'s
`SR-177` card opened with only the pill and the id — the `Requirement`/
`Rationale` text existed in the HTML but only inside `.ctx`
(`display:none` by default); `docs/ratify/CURRENT.md`'s `## SR-177 — …`
section had no SR block at all, jumping straight to `### LLR LLR-196` and
`### TC TC-191`.

**After**, `docs/ratify/CURRENT.md` (regenerated, `trace.py --approve
modified`):

```
## SR-177 — Fan-out utilisation reported from the run's own telemetry

> **Requirement.** The delivered loop content shall report, per run, the
utilisation of the fan-out it commissions — the lanes configured, the lanes
actually occupied, and the work integrated per unit of wall time — derived
from the run's own recorded telemetry, reported and never gated, with no
declared improvement target.

> **Rationale.** Hat-derived (hat.PERFORMANCE, C-PRF-1 — clause text in
docs/plans/2026-08-16-blind-derivation-c-hats.md): […] this report's first
run would have printed lanes=1. […] there is… [175 more chars — read the
registry row]


### LLR LLR-196 — Drafted, never approved
[…as before: Title/Module/CodeSymbol/Detail/Rationale/Status…]

### TC TC-191 — Drafted, never approved
[…as before: Verifies/Level/Method/Tier/Expected/Automated/Evidence/Status…]
```

`docs/open-items.html`'s `SR-177-attest` card now opens `<h3>… SR-177 …
approval owed</h3><div class="anchor">` with the Requirement paragraph and
the (truncated) Rationale paragraph immediately following — before the
`class="ctx"` div, so visible with the toolbar checkbox in its default
(checked) state.
<!-- fig: cmd="python project-trajectory/scripts/gen_open_items.py --root ." rev=435423fa -->

### Gates

- `python -m pytest -q -n auto -m smoke` → **1323 passed, 5 skipped in
  19.08s**; `check_smoke_budget.py --mode enforce` re-ran it standalone at
  **24.47s / 24.9s vs 60s budget → within**.
- `check_docs.py --root . --stale` → 1056 docs, 1377 links, **0 broken**
  (pre-existing "possibly stale" hints only, none touched here).
- `check_trajectory.py --root . --strict` → clean of new findings (the
  pre-existing WARN set is unchanged by this WI's diff).
- `trace.py --root . --strict-integrity` → integrity 0.
- `python -m pytest -q -n auto --basetemp=D:\pytest-tmp-brieftext` →
  **3013 passed, 14 skipped in 1064.80s (0:17:44)**.
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=435423fa -->
<!-- fig: cmd="python -m pytest -q -n auto --basetemp=D:\pytest-tmp-brieftext" rev=435423fa -->

Two ratchets re-stamped, both reviewed bumps: `tests/test_module_size_ratchet.py`
(`trace.py` 5621 → 5678, +57 — `truncate_cell`, `_anchor_lines`, and the
`truncate_cell` calls threaded through `_full_row_bullets`/`_cell_diff_lines`)
and `tests/test_generated_newlines.py`'s pinned LF-write site in
`gen_open_items.py` (1183 → 1234 — `_anchor_block` and the `tr.truncate_cell`
calls threaded through `_context_block`/`_chain_row`, all above the pinned
site). `docs/id-watermark` re-stamped via `trace.py --bump-ids` (`WI 513 ->
514`).

Deferred open items: none — this WI answers the owner's report in full; no
new question was raised. The owner's approval act over the ten owing SRs
remains pending, as it was before this WI — a queued owner act, not an open
item this session owes.
