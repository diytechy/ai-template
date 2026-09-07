## 2026-09-06 — Package PC: the agreed cuts are unconditional

**Decision (owner).** The deletions both redesign plans agreed on
independently — one WI per lane with batch admission retired, the legacy tail
(CSV converter, retired-vocabulary arms, out-of-window resync entries), and
the P0b hygiene (complexity-baseline re-key for `rendering/`, the uncalled
`check_changed.py`) — are no longer parked inside the conditional P3–P8 set.
They form package **PC** in the codex plan's IMPLEMENTATION.md, sequenced at
the first commit after the Short control window closes and run regardless of
the window's outcome. The window itself still measures the frozen
configuration, batches included; nothing is cut before it closes.

Not moved: SN-027's parallel lanes, the eight-module minimal kit and rendering
reduction beyond P9R stay owner-ruled candidates needing their own SN-tier
dispositions.

Recorded in IMPLEMENTATION.md (§2 graph + PC package), the README
recommendation, and handoff item 3. No registry, queue, pause or policy change.

Deferred open items: none.
