## 2026-09-01 — the owner rules OI-77: (a), the intake write-back reads the value the parser already parsed

The owner read the hand-filled card (`6032ce69`) in the evening sitting and
ruled **(a)**: `intake._replace_inbound_edges` re-points a dependent's hard
`needs` edge from the parsed TOML value (or, minimally, the existing pattern
under `re.DOTALL`), so the WI-541 strand class becomes unrepresentable
regardless of how a spec's `needs` list is laid out. The recommendation's
guard stands with the ruling: the rewrite stays surgical — only the `needs`
value moves, the rest of the spec byte-identical — with a dependent carrying
a multi-line `needs` as the acceptance test. The two cosmetic WI-552
leftovers (the dead `intake._OI_ID_RE`; the `check_trajectory.validate`
docstring against the `known_ois=None` coercion) ride the same row.

Clarified for the record, because the owner asked: the `needs` in this ruling
is a work-item spec's **`needs` frontmatter cell** — its hard-predecessor
edges in the WI graph (`WI-###` and `OI-###` tokens) — not a stakeholder need
(`SN-###`). No stakeholder-needs row is touched by any option.

The ruling unparks the row that carries it (its `needs` names this open item),
so the scheduler reads it ready on the next resume.

Deferred open items: none — this entry records a ruling, it raises none.
