# Architecture (one page)

Owned by the **Software Engineer** hat. The **overview** below is hand-written
and must stay within one screen; the **module/function map** is **generated** by
the check harness so it cannot drift (see [process.md §3/§7](process.md)).

## High-level flow

```
<input> ──► <stage 1> ──► <stage 2> ──► <output>
            (module)       (module)
```

_Describe the data flow in a few boxes/arrows. Keep it readable at a glance._

### Program flow (generated)

The ordered steps of the entry/orchestrator function, generated from the code by
`python scripts/gen_arch_map.py --flow <entry>` (wire `--flow` into the harness's
map step). Keep the orchestrator thin so this reads as the high-level flow; the
diagram above carries the control flow this list omits.

<!-- BEGIN GENERATED FLOW -->
_(run `gen_arch_map.py --flow <entry>` to populate — e.g. `--flow run`)_
<!-- END GENERATED FLOW -->

## Module responsibilities

| Module | Responsibility | Key public items |
|---|---|---|
| `path/to/mod_a` | <one line> | |
| `path/to/mod_b` | <one line> | |

Design rules (enforced): shared logic lives in one place (no duplication); pure,
unit-testable cores are separated from I/O / network / GUI shells; functions stay
small; each module has a single clear responsibility.

<!-- BEGIN GENERATED MODULE MAP -->
_(the harness regenerates the code map here from the source AST: per-module
summary, internal dependencies, and public symbols with `Implements:` back-links.
Run `python scripts/gen_arch_map.py`. To also surface it where agents read, add
the same marker pair to `AGENTS.md`/`CLAUDE.md` and pass `--doc` for each — see
process.md "Generated code map".)_
<!-- END GENERATED MODULE MAP -->
