## 2026-08-29 — OI-67 filed: the interface row shape is questioned, and the cell pass is held

Deferred open items: **OI-67** — filed by this sitting and pending: the shape of
an interface row, and which of its cells go.

**Summary.** Owner-directed, no WI. Reading the registry after the contract
header landed, the owner asked what the `contract` cell is still for, what
`req_refs` does when the owner already names a requirement, and whether the
row should not simply be *what the information plugs into, who it serves, and
what the data is* — **one row, one direction, one kind of information**. The
two-way rows, in the owner's reading, are where the churn has come from.

**Measured before filing, every number in the row:**

- `provider` is absent on 106 of 136 rows and stated on 30 — 21 modules, 3
  directories, 3 files, 3 `external:` parties. Its readers: the component
  graph, the cross-component import rule, the arch map, the planning briefs.
- `req_refs` has one mechanical reader (the back-link check). On **88 rows** it
  adds nothing the owner does not already derive; **48** add a requirement,
  hand-written and verified by nothing.
- `contract` is the only place the payload is described, and it is fed verbatim
  to the LLM planning briefs. `signal` reads `variable` on 127 rows.
- **Direction, every row read (an Opus pass, not a regex):** 87 one-way, **14
  two-way**, **35 one-way-but-several-kinds**, 0 unclear. The registry is 136
  rows today, 157 if only the two-way rows split, 213 if every bundled kind
  gets its own row.
- **31 rows are provided by something that is not a Python module** — 24 files
  (nearly all hand-edited), 4 directories, 3 external parties — and the header
  scanner reads `*.py` only. That is the gap between the owner's shape and the
  mechanism WI-527 built.

**Options filed:** (a) the owner's shape — three cells go, `owner` widened to
name a file or directory, `signal` replaced by a typed `data` cell, the module
header the only home, two-way rows split; (b) the same but the schema stays a
structured cell; (c) drop `req_refs` only; (d) finish the 71-row cell pass as
ruled at OI-66. Recommendation **(a)**, sequenced so nothing is removed before
its replacement exists. **The 71-row cell pass is HELD** until this is ruled:
it is authoring against a shape the owner has questioned.

**Also this sitting — the registry header brought back to true.** Six stale
claims in `interfaces.toml`'s field guide were corrected, one of which stated
the opposite of live behaviour: the "dial of 4 … every cell is the owner's to
flip" paragraph, when `human_approves(docs, "interfaces")` answers **False** at
this repo's `DevStg-Needs` dial (the same claim corrected in `external.toml`,
`agent_common.py`'s predicate docstring and its module comment). The others:
"nothing lints `rationale`" (WI-523 widened `IF_REASON_CELLS`), placement
"still open" (ruled and built — the paragraph now describes the header, the
reference and the 2-of-136 debt), and three drifted counts (provider survivors
29 → 30, `rationale` 37 → 38, multi-ref rows 21 → 25, the last also in
`trace.py`). `IF-144`'s cell was trimmed to its crossing statement — it had
been stating the whole protocol twice, in the cell and in `check.py`'s header,
the duplication the header exists to remove. And WI-527's insertion into the
shipped `interfaces.template.toml` had split a sentence in half; the
paragraph is re-seated whole. Checks: `check.py` PASS; smoke tier 1363 passed,
6 skipped, 22.6 s against the 60 s budget.

**Deliverables.** `OI-67` filed; `docs/id-watermark` bumped `OI 66 → 67`;
`docs/open-items.html` regenerated; `docs/status.md` re-pointed — the decision
surface is no longer empty and the cell pass is held behind the row.
**Deviations from spec:** none.

**Byte deltas on budgeted files:** none touched.
