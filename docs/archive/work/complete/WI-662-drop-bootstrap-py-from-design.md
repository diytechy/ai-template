+++
id = "WI-662"
title = "Drop bootstrap.py from design rows whose code_symbol names nothing in it"
workstream = "requirements"
specref = ""
buildtier = "quick"
safety_class = "ordinary"
priority = 5
+++

## Deliverable

`project-trajectory/scripts/bootstrap.py` is dropped from the `module` cell of
the two design rows whose `code_symbol` names nothing in it: LLR-235
(record_observation) and LLR-256 (check_readability). These are traced cells,
so no re-attestation follows. LLR-203 and LLR-218 (`MAPPING`) and LLR-009,
LLR-010, LLR-011, LLR-121 and LLR-156 keep it, since each has a symbol that
binds there. The check the spec asked about, a warning on a listed module no
symbol binds in, is worth building only as a counted advisory, and only after
a ruling on what `module` means. The binding rule reads the cell as a union
(LLR-180's approved detail), 37 rows would fire on arrival, and a name-only
oracle is fooled by `main`. It is filed as **WI-670**. Sol: SOUND.

## Context

Several design rows list `project-trajectory/scripts/bootstrap.py` in
`Module` because the change registered a new script in `bootstrap.MAPPING`,
while their `code_symbol` names nothing that lives in `bootstrap.py`
(LLR-235 and LLR-256 at b14d1808; LLR-218 names `MAPPING`, and LLR-203 is the
`MAPPING` row itself, so recheck those two). A `Module` cell is where a
reader goes to find the row's code; a module holding none of it sends them
to the wrong place.

IN SCOPE: for each design row, keep `bootstrap.py` in `Module` only where a
`code_symbol` binds in it. These are traced cells, so no re-attestation
follows. Consider whether `check_trajectory`'s symbol binding should warn on
a listed module no symbol binds in; if so, draft that as its own item.

## Done-when

- Every design row listing `bootstrap.py` has a `code_symbol` that binds
  there, and `trace.py --strict-integrity` passes.
- The commit bar passes.
