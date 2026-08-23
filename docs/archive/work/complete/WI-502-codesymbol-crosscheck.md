+++
id = "WI-502"
title = "Mechanize the Implements-tag vs CodeSymbol cross-check, warn-first (OI-53 ruled (d) follow-up, 2026-08-22)"
specref = ""
workstream = "scripts"
sr_refs = []
needs = ["WI-501"]
buildtier = "quick"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Executed OI-53's ruled (d) half: the 2026-08-21 closing review's manual
method — resolve every `Implements:` tag's ENCLOSING def/class via AST and
compare it against the row's `CodeSymbol`/`Module` cells by containment — is
now `check_trajectory.codesymbol_crosscheck_findings`, a new warn-first
finding class run every commit.

**Grammar-sharing decision.** The AST symbol-resolution grammar lives in
`gen_arch_map.py` (WI-486's one home for `Implements:` parsing), sharing
`backlink_ids` with the existing reverse-coverage scan rather than
re-deriving it: `_scope_index`/`_top_level_targets`/`enclosing_symbol`/
`declaration_sites`/`implements_report` are the new surface, and
`check_trajectory` consumes only the last of those (`implements_report`) —
the same `scan_inventory` idiom `arch_inventory` already uses, so this is a
second CONSUMER of the shared walk, not a second walk. `check_trajectory`
owns the registry-comparison half only: `codesymbol_crosscheck_findings` +
`_codesymbol_site_finding` (the per-site containment/mismatch/unresolvable
rule, split out to keep the walk's own C901 complexity from absorbing the
rule's) + `_codesymbol_candidates` (the `/`/`;`/` + ` symbol-list splitter,
widened past a bare `/` once the live registry showed all three joins in
real cells).

**Containment, both directions.** A tag inside `RoutingState.note_session`
satisfies a cell naming `RoutingState` (class-as-prefix, the WI's own
example) OR a cell naming bare `note_session` (method-as-suffix, the
convention most live `CodeSymbol` cells actually use — the rendered map's
own `methods` row lists them unqualified too). A tag at true module scope
satisfies an empty (module-only) cell. A comment sitting directly above a
module-level constant or `def` (no containing AST node) resolves to that
statement's bound name via a small forward-association window (<=4 lines,
matching `implements()`'s own docstring lookback) rather than reading as
bare module scope — without it, the crosscheck could not see the very common
"comment above a `CONSTANT = ...` assignment" tagging shape and would
mis-flag roughly 40 real, correct rows as module-scope mismatches (measured
during this session: the first live run misread 48 sites before this and the
`+`/`;` splitter widening; the honest post-widening count is below).

**Two finding shapes**, named in the message and distinguished so a reader
(and the regression tests) can tell "the cell names a different REAL symbol"
(**mismatch**) from "the cell names nothing resolvable at all — a
function-local variable, or a gone symbol" (**unresolvable**, so a
non-machine-checkable cell reports rather than silently reading as a match —
the false-quiet shape `docs/enforcement-audit.md` item 5 already names for
the neighboring `Contracts:` grammar, which this rule does not inherit).

WARN-FIRST FOREVER by the ruling: no allowlist, no `--strict` promotion —
folded into `check_trajectory`'s existing never-promoted warn loop beside
`interface_findings`/`cross_component_advisories`/
`if_tc_allow_hygiene_findings`.

**Initial finding count over the live tree, post-WI-501 baseline: 9**
mismatches/unresolvables across LLR-077, LLR-111, LLR-117, LLR-155, LLR-156,
LLR-159 (twice), LLR-188, LLR-195 — residual drift WI-501's repair did not
reach (a different population: WI-501 fixed the dozen the 2026-08-21 review
read by hand; this mechanization scans the WHOLE live tree, catching the
`LLR-159` Module cell still naming `dispatch.py` after the WI-483 slice-2
move to `census.py`, plus several bare-function-name/multi-symbol cells this
review's manual pass never reached). Reported honestly, not fixed here — a
worker amending an Approved cell mid-WI is the precedent OI-53 itself turned
on.
<!-- fig: cmd="python -c \"import sys; sys.path.insert(0,'project-trajectory/scripts'); import check_trajectory as ct; from pathlib import Path; print(len(ct.codesymbol_crosscheck_findings(Path('.'))))\"" rev=13818fe6-dirty -->

**Regression tests** (`tests/test_trajectory_arch.py`, in-process — no
subprocess, per the WI's ask): `test_codesymbol_crosscheck_reports_a_planted_mismatch`,
`test_codesymbol_crosscheck_containment_case_is_silent`,
`test_codesymbol_crosscheck_function_local_name_is_unresolvable`,
`test_codesymbol_crosscheck_vacuous_in_files_mode`.

**Deviations from spec:** none in shape; the forward-association window and
the widened `/`/`;`/` + ` splitter were not named in the spec but were
necessary to keep the check honest — a naive `/`-only, AST-scope-only
reading misfired on ~40 real, correctly-tagged module-level constants before
they were added (measured live, see above), which would have been exactly
the "invents links" defect `backlink_ids`' own docstring warns against, one
tier up.

Deferred open items: none — the honest residual count is recorded above, not
deferred; OI-53 is now fully executed (WI-501 + WI-502) and its `wi_refs`
updated in the same commit.
