## 2026-11-01 — WI-987: the open-items page lists the stakeholder needs and stakeholders owing an act

Deferred open items: none — the one finding left open, the approval brief
clipping a first-approval need's long cell, is a successor row for the
coordinator to file, not an owner decision.

Section 2 of `docs/open-items.html` now reads `baseline_snapshot.needs_owing`
beside `trace.reattest_model`, so a drifted or unapproved need or stakeholder
gets a card: a drifted one with its moved cells before and after, a
first-approval one with every cell whole and unclipped. The empty message is
printed only when neither an SR chain nor a need owes, and names both checks;
the header counts the needs that owe and its drifted count includes them.

- The SR cards and the need cards share two new cell helpers
  (`_cell_diff_html`, `_full_cells_html`); the SR rendering stayed
  byte-identical, checked by rendering trunk's page with both versions.
- The regenerated page shows SN-028 (DRIFTED: Acceptance, Why) and SN-036
  (DRIFTED: Acceptance), the same two rows `needs_owing` reports on the lane.
- `gen_open_items.py` is at 983 SLOC (`check_complexity.module_sloc`), from
  933, under the module-size threshold of 1000.

Left for a successor: the Markdown approval brief (`trace.need_brief_lines`)
still clips a first-approval need's cell past 1,500 characters, where the page
now shows it whole. Both name the same rows as owing.
