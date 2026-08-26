## 2026-08-25 — OI-64 (c): the shipped checkers measured against one contract — protocol honoured, vocabulary not

Deferred open items: **OI-64** — still `pending` and deliberately so. This
sitting ran the measurement its option (c) asks for; the measure-vs-state
choice was always the ruling, not the measurement, and (a) vs (b) vs (d) is
untouched by it except that the numbers now exist.

**Summary.** Owner-directed sitting, no WI minted. OI-64's option (c) run in
full over the delivered harness and filed at
[../plans/2026-08-25-oi64-checker-uniformity.md](../plans/2026-08-25-oi64-checker-uniformity.md).
**Nothing was edited** — no checker, no registry cell, no severity, the WI-516
discipline applied to code instead of contract cells. The row's brief and the
working surface now carry the headline; the row stays `pending`.

### THE NUMBERS

Method: an AST census of every finding-emission site across the 14 shipped
checkers plus the two rule libraries feeding `trace`, **every extracted site
read** and classified (the rules and both exception sets are enumerated by site
in the record, so the counts are auditable without re-running anything); then
every checker driven twice, once on an EMPTY root and once on this repo.

| axis | reading |
|---|---|
| emission sites | **430** — 177 artifact/data builders, 40 renderers, 55 summary lines, **158 per-finding sites** |
| names a location | **141 / 158 = 89.2%**; 11 population-level (no at-fault row exists), 6 thin |
| advisory never gates | **unanimous**; the phrase "never the exit code" / "never gating" appears **25 times** across 7 modules |
| absent optional input | **12 of 14** exit 0 AND name the absence; `check_flows` fails by design, `trace` reports a true integrity finding |
| severity words | **12 label tokens for 4 dispositions** |
| escalation | **6 flag spellings**, 4 checkers with none, 2 per-row mechanisms |

<!-- fig: cmd="python project-trajectory/scripts/<checker>.py --root .  # driven on an empty root and on this repo" rev=fc8a0edc -->

**The answer in one line: the PROTOCOL is honoured; the VOCABULARY is not.**
Stated as the clauses a row would carry, (a) mints **three green and one red** —
location (with a population-level carve-out), advisory-never-gates and vacuity
are already honoured across the harness; a closed severity vocabulary is red on
every checker at once, and red only in spelling, since no behaviour would have
to change to satisfy it.

**The precedent the measurement turned up, and it is the corpus's own:** the
five declared allow-file readers share ONE parse-honesty protocol (first
unreadable declaring line, with the count and the grammar, at `file:lineno`)
while each picks its own SEVERITY and says why in its own docstring — `trace`'s
integrity-class *"because the always-on floor is the only pipe that runs at
every gate"*, `check_trajectory`'s kernel-allow riding `components_check`
instead. One protocol, per-row disposition, already working in five places.
That is the shape OI-64's recommendation argues for, demonstrated rather than
asserted.

**Two things the drive found that no row would catch today**, recorded and not
acted on: `check_privacy` exits **2** in a non-git directory where `check_docs`
prints *"staleness check skipped"* and continues — one class of environment
absence resolved three ways; and `trace` WRITES `docs/test/report.md` into the
tree as a side effect of a plain check invocation.

**What is deliberately not settled:** where the row would live. The owner's
direction puts the mint target at the INTERFACE tier, and `OI-63`'s placement
re-ask has not yet said where interface contracts live. The record does not
prejudge that sequencing.

**Deliverables.** The measurement record (new); OI-64's `decision` and
`recommendation` carrying the result and marking (c) discharged;
`docs/open-items.html` regenerated; `docs/status.md` re-pointed on the remap
row. **Deviations from spec:** none — no WI was in scope, and the sitting's
whole instruction was to run the measurement.

**Byte deltas on budgeted files:** none touched.
