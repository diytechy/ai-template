+++
id = "WI-523"
title = "Widen the IF reason-cell lint to `rationale`, and stop the WI-id detector being defeated by a shift key (OI-65 ruled (iv))"
specref = ""
workstream = "conformance"
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Two one-line changes and the three real findings the second one exposed.

`trace.py`'s `IF_REASON_CELLS` is now `("Notes", "SignalNote", "Rationale")`, so
the citation-frame arm reads the cell WI-522 took from 1 row to 37 in a single
pass and which, until now, nothing read at all. `trace_text.py`'s
`_WI_TOKEN_RE` carries `re.IGNORECASE`; the token shape is unchanged, so this
only stops the case of two letters deciding whether provenance is seen.

**Driven, not estimated, and the numbers held.** The widened arm reports
**0 findings** across the 37 live `rationale` cells — the prediction made before
the ruling. The case fix reported exactly **3**: `wI-280` in the `notes` of
`IF-082`, `IF-083` and `IF-084`, invisible to three prior rounds of this arm.
All three were fixed rather than silenced, by dropping the provenance frame the
finding asks to drop; each cell's standing reason stood alone without it, so
nothing was lost. `trace.py`'s IF advisory count is **43 before, 43 after** —
the case fix surfaced three and the same act cleared them.

Two tests in `tests/test_trace_rules.py`:
`test_the_if_rationale_cell_is_swept_too_since_wi523` (a citation frame in
`Rationale` is reported; the cell doing its job — arguing, connectives, length —
stays silent; placeholder rows and token-scoped exceptions behave as they do for
`Notes`) and `test_a_work_item_citation_is_found_whatever_its_capitalisation`
(all four spellings match; `SWI-280` and a bare `WI-` still do not).

## Context

`OI-65` part 3, ruled (iv) on 2026-08-28. The cleanup that filled `rationale`
moved content into the one cell in the registry with no arm on it, and the
detector meant to catch provenance in the neighbouring cell had been defeated by
a typo's capitalisation since WI-280.

## Done when

- [x] `rationale` is in `IF_REASON_CELLS` and the arm reads it.
- [x] `_WI_TOKEN_RE` matches case-insensitively without widening the token shape.
- [x] Tests cover both arms.
- [x] The three real hits fixed, not silenced.
- [x] Commit bar green.
