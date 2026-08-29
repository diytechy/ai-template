## 2026-08-29 — WI-529: the contract header reaches every owner (OI-67 slice 2)

Deferred open items: none.

**Summary.** A registry, a config file or a git hook now declares its seams
and states their contracts exactly as a module does — through a `Contracts:`
marker and `Contract IF-###:` bodies in its leading comment header — and the
reverse check names the OWNER that fails to declare, not merely an id nobody
declares. The two git hooks (`IF-134`, `IF-135`) declare and state their
contracts, closing the "extensionless files a `*.py` scan cannot see" gap the
OI-66 build recorded.

**One grammar, two carriers.** `gen_arch_map.header_lines` reads the leading
comment block of a non-Python file with its markers stripped — `#` lines at the
top of a TOML/INI/CSV/shell/extensionless file (a `#!` shebang skipped; the
block ends at the first non-comment line), or the first `<!-- … -->` block of
a Markdown file — and `file_contracts` runs the SAME marker and body grammar
over those lines that a module docstring gets: `_contract_bodies` is the body
walk extracted from `module_contract_bodies` (now a two-line wrapper), and
`_grammar_findings_over` the lossy-marker report extracted from
`contracts_grammar_findings`, so the four refusals and the two lossy forms hold
for a header exactly as for a docstring. A header is the FIRST thing in its
file or it is not a header.

**Which files.** `owner_files` reads the registry: every row whose owner
resolves to a file in the tree (or to a directory with a `README.md`) and is
neither a `.py` module nor an `external:` party. The reference lists them under
the path the registry spells, beside the modules; the summary line counts
"sources" now. `--contracts-doc` finds the registry through the `--interfaces`
flag the diagram already takes.

**Owner-exact.** `check_trajectory._owner_exact_findings`: a row owned by a
module in the inventory warns unless THAT module's marker declares it (every
inventory module is judged — an owner that declares nothing at all was the
plainest miss, and the first cut, which judged only declaring modules, let it
through until the new test caught it); a row owned by a file warns unless that
file's header declares it; an `external:` owner is skipped; a directory with no
README or an owner the tree cannot resolve falls back to the id-global read.
The marker-grammar honesty arm covers the file headers too. **67 rows warn on
this tree today** — the markers sit on the modules that read a medium rather
than on the medium, and the module-owned rows' markers are scattered — and that
count is slice 3's worklist, warn-first as every rule in this pipe.

**Ratchets.** `gen_arch_map.py` +134 (2010 → 2144) and `check_trajectory.py`
+78 (4366 → 4444), both reviewed bumps with the reason on the stamp: one
grammar, one parser, one home. C901: `module_contract_bodies`' entry re-keyed
onto `_contract_bodies`, the walk it moved into unchanged.

**Gates.** Commit bar and the full suite, both green; totals at the foot.

**Deviations from spec:** none.

**Byte deltas on budgeted files:** none touched.

**pytest totals:** FILLED-AT-CLOSE
