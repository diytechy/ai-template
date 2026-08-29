<!--
Contracts: IF-025, IF-026 — the interface seams this directory declares
(process.md §8; rows of record in the adopting repo's interfaces registry).

Contract IF-025: the declared source root read as the AST-INVENTORY surface.
    Every `*.py` beneath it offers, from its own syntax tree, a module summary,
    its public symbols with their signatures, the in-tree modules it imports and
    the seam ids its `Contracts:` marker declares — the material for the symbol
    map and the internal-import diagram. A file that cannot be decoded fails the
    generating pass loudly and is dropped from the advisory readers rather than
    silently mis-reported; a module contributing no summary, import, contract or
    symbol is skipped instead of rendered empty.
Contract IF-026: the same root read as the STUB-DETECTION surface, by an
    independent walk. Each `*.py` offers its public functions and methods, and
    one whose body after an optional docstring does nothing at all is listed.
    Warn-first: found stubs exit zero, and only the strict flag makes them fail,
    so a legitimately tiny function is never mistaken for an unfinished one.
-->

# `scripts/` — the kit's checkers, generators and coordinator

Stdlib-only Python 3.11+, cross-platform, each script runnable on its own and
wired into a gate through the declared toolchain. `check.py` is the harness that
runs a gate's steps; `trace.py` joins the requirement spine; the `check_*`
scripts are the individual gates and the `gen_*` scripts the generators of the
committed derived artifacts. `kitlib/` holds the shipped shared helpers a script
imports rather than copies, and `spine_carrier.py` is the registry reader every
spine consumer joins through. This directory is also the declared source root
the AST inventory and the stub detector walk, so a module's own docstring — its
summary, its `Implements:` lines and its `Contracts:` marker — is the source of
what the generated code map and interface reference say about it.
