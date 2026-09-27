+++
id = "WI-670"
title = "Count design rows that list a module none of their symbols binds in"
workstream = "requirements"
specref = "docs/requirements/low-level-requirements.toml"
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Context

Drafted by WI-662's builder (its answer to that item's question) and filed at
its integration. A design row's `module` cell is where a reader goes to find
the row's code, but `check_doc_refs.symbol_findings` (LLR-180) reads the cell
as a UNION: a row is anchored when any identifier token binds in any listed
module, so a module that holds none of the row's code passes silently.
Measured at cae40af6 (after `bootstrap.py` was dropped from LLR-235 and
LLR-256): 37 Approved rows list at least one `.py` module in which none of
their identifier tokens binds. Most follow an unruled convention (a module
holding only a composition line, `migrate_carrier.py` for a KEY-map entry,
`gen_trajectory.py` for a CSS-token cell). Separately, a name-only oracle is
fooled by a generic name: LLR-235 and LLR-256 named `main`, which
`bootstrap.py` also defines, so neither would have been reported. LLR-240,
LLR-241, LLR-243, LLR-244 and LLR-258 bind no symbol in any listed module
(approved ahead of their build).

IN SCOPE: first obtain a ruling on what `module` lists (the modules holding
the row's code_symbol entries, or every module the change touched). If the
former, amend LLR-180's detail (union reading kept for the anchor verdict; a
new per-module "unbound module" count added) and build it as an UNTRACED-class
count, listed by `--show-untraced`, never dangling and never the exit code.
Treat a generic token (`main`, and any name every CLI module defines) as not
binding for this count. Burn the live rows down under that ruling as a
separate item. OUT OF SCOPE: any gating arm.

## Done-when

- The ruling on the `module` cell's meaning is recorded.
- LLR-180's amendment is adjudicated, its test case gains one clause per new
  behaviour, and the count reports LLR-235-shaped rows a `main` coincidence
  used to hide.
- The commit bar passes.
