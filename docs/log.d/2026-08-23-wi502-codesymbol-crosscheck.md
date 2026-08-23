## 2026-08-23 — WI-502: mechanize the Implements-tag vs CodeSymbol crosscheck

Executed OI-53's ruled (d) half (docs/log.d/2026-08-22-oi53-54-rule.md): the
2026-08-21 closing review's manual method — resolve every `Implements:` tag's
enclosing def/class and compare it against its LLR row's `CodeSymbol`/
`Module` cells by containment — is now a standing warn-first finding class,
`check_trajectory.codesymbol_crosscheck_findings`, run on every commit.

**Grammar-sharing decision.** The AST resolution lives in `gen_arch_map.py`
(WI-486's one home for `Implements:` parsing), as a new consumer of
`backlink_ids` alongside the existing reverse-coverage scan:
`_scope_index`/`_top_level_targets`/`enclosing_symbol`/`declaration_sites`/
`implements_report` are the additions, and `check_trajectory` imports only
`implements_report` — the same `scan_inventory` idiom `arch_inventory`
already uses to share the walk rather than re-deriving it. `check_trajectory`
owns the registry-comparison half: `codesymbol_crosscheck_findings` (the
walk), `_codesymbol_site_finding` (the per-site containment/mismatch/
unresolvable rule, split into its own function so the walk's own C901
complexity stayed the irreducible part) and `_codesymbol_candidates` (a
`/`/`;`/` + ` splitter — widened past a bare `/` once the live registry
showed all three joins used as the same "and also" separator in real cells,
sometimes in one cell).

**What "containment" turned out to need, measured against the live tree.**
The WI's own example (a tag inside `RoutingState.note_session` satisfies a
cell naming `RoutingState`) is one direction; most live cells actually name
the bare method (`stall_verdict`, no class qualifier — the rendered map's own
`methods` row lists them unqualified too), so containment reads both
directions of the dotted path. A first pass that resolved enclosing symbols
by AST-scope containment alone misread 48 real, correctly-tagged sites as
findings — nearly all of them a comment sitting directly above a
module-level constant (`# Implements: ...` then `TIER_FILL = {...}` on the
next line), a shape outside any def/class node's own line range. Fixing that
(a small forward-association window, <=4 lines, matching `implements()`'s
own docstring lookback) plus the wider candidate splitter brought the count
to 9 — the honest residual. Adding the splitter and forward-association was
not named in the spec but was necessary: without them the check would have
been exactly the "invents links" defect `backlink_ids`'s own docstring warns
against, one tier up (false NOISE instead of `backlink_ids`'s false LINKS).

**Two finding shapes**, named in the message: **mismatch** (the cell names a
real def/class/constant elsewhere in the scanned surface, just not the one
containing this tag) and **unresolvable** (no candidate in the cell resolves
to anything real — a function-local variable, a CLI flag list, or a symbol
that is simply gone). Distinguishing them keeps this rule from inheriting the
false-quiet shape `docs/enforcement-audit.md` item 5 already names for the
neighboring `Contracts:` grammar: a cell that cannot be verified reports as
such rather than silently reading as a match.

WARN-FIRST FOREVER (no allowlist, no `--strict` promotion) — folded into
`check_trajectory`'s existing never-promoted warn loop beside
`interface_findings`/`cross_component_advisories`/
`if_tc_allow_hygiene_findings`. Verified live: `check_trajectory.py --root .
--strict` exits 0 with the 9 new WARN lines present.

**Initial finding count over the live tree, post-WI-501 baseline: 9** —
LLR-077, LLR-111, LLR-117, LLR-155, LLR-156, LLR-159 (twice), LLR-188,
LLR-195. A different population than WI-501's dozen: this scans the whole
live tree rather than the 2026-08-21 review's by-hand read, and catches (for
example) LLR-159's `Module` cell still naming `dispatch.py` after the
WI-483 slice-2 move of the census to `census.py`. Reported honestly, not
repaired here — a worker amending an Approved cell mid-WI is the precedent
OI-53 itself turned on; `open-items.toml` OI-53 gains `wi_refs = ["WI-501",
"WI-502"]` in this commit, now that both halves of the ruling are executed.
<!-- fig: cmd="python -c \"import sys; sys.path.insert(0,'project-trajectory/scripts'); import check_trajectory as ct; from pathlib import Path; print(len(ct.codesymbol_crosscheck_findings(Path('.'))))\"" rev=13818fe6-dirty -->

**Regression tests** (`tests/test_trajectory_arch.py`, in-process — no
subprocess, per the WI's ask): `test_codesymbol_crosscheck_reports_a_planted_mismatch`
(a planted mismatch warns), `test_codesymbol_crosscheck_containment_case_is_silent`
(the containment case is silent), `test_codesymbol_crosscheck_function_local_name_is_unresolvable`
(a function-local cell name reports unresolvable, not matched), and
`test_codesymbol_crosscheck_vacuous_in_files_mode` (files-mode has no parser
to ask).

**Ratchets.** `codesymbol_crosscheck_findings` measures C901 13 (the walk
itself, over `MAX_COMPLEXITY = 10`; the actual rule is split into
`_codesymbol_site_finding`, well under it) —
`tests/test_complexity_ratchet.py` `BASELINE` gains
`("check_trajectory.py", "codesymbol_crosscheck_findings"): 13`.
`check_trajectory.py` grew 4645 -> 4789 lines (+144);
`tests/test_module_size_ratchet.py` `BASELINE` re-stamped with the reason
inline. `gen_arch_map.py` (1467 lines) stays below the 1500-line tracked
threshold.

**Gates.** `python -m pytest -q -n auto -m smoke` — 1265 passed, 5 skipped,
17.6s-21.5s across runs. `python scripts/check_smoke_budget.py --mode
enforce`: ~21.9s vs 60s budget — within. `python
project-trajectory/scripts/check_docs.py --root . --stale`: exit 0 (only
pre-existing archive-link staleness hints, none touching this change).
`python project-trajectory/scripts/check_trajectory.py --root . --strict`:
exit 0, the 9 new crosscheck WARN lines present alongside the pre-existing
warn population. Full suite:
`python -m pytest -q -n auto --basetemp=D:\pytest-tmp-w502` — **2903 passed,
14 skipped, 1082.62s (0:18:02)**
<!-- fig: cmd="python -m pytest -q -n auto --basetemp=D:\pytest-tmp-w502" rev=13818fe6-dirty -->
(sh.exe on PATH via Git Bash for the environment-gate test).

**Deviations from spec:** none in shape (new finding class, shared grammar,
warn-first-forever, three named regression cases, live count recorded) — the
forward-association window and the widened candidate splitter were needed
beyond the spec's literal text to keep the check from misreporting real,
correctly-tagged rows, per the measurement above.

Deferred open items: none — the residual 9-count is recorded honestly above,
not deferred, and OI-53 is now fully executed.
