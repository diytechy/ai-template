# WI-399 REVIEW-A — independent, hunt-to-break (branch wi-399-… @ fe0cd1a8 vs ConcurrencyTrainRewrite)

Method: line-diffed `shipped_modules`/`_arch_scan_profile` against `gen_arch_map`'s
collectors, then DROVE divergence with a differential harness (mirror set vs a real
`gen_arch_map` run parsed back through `arch_inventory`/`_norm_module`, 12+11 tree
shapes); drove the false-red end-to-end through `check_trajectory --strict` including
a post-regeneration re-check; ran the 9 new tests + the 54-test module + smoke; did
the wiring-removal mutation check in a scratch copy; verified the amend by reflog and
content; re-ran the strict checks, dupes census, figures, and ruff.

1. [MAJOR] project-trajectory/scripts/check_trajectory.py:1208 (`shipped_modules`) vs
   project-trajectory/scripts/gen_arch_map.py:456-457 -> the mirror is NOT the
   generator's inventory: `build_map` drops any module with no docstring summary, no
   internal imports, no contracts and no public symbols — `if not (summary or imports
   or contracts or rows): continue  # skip empty modules (e.g. bare __init__.py)` —
   while the mirror collects every non-hidden `*.py`. Such a module sits in the delta
   FOREVER: the trunk refresh never inventories it, so "the delta against the COMMITTED
   `arch_inventory` is exactly the modules the refresh WOULD add — no more"
   (docstring + Deliverable) and "A fresh map (delta empty — every trunk checkout
   after the refresh) is vacuous" (`added_module_findings` docstring) are both false
   for this class, and the finding text "not yet in the committed arch-map" promises a
   convergence that never comes. Driven end-to-end: a pack-armed tree with a real
   generated, fully-contained map + a new `scripts/pkg/{__init__.py,mod.py}` with
   `mod` duly tagged reds `--strict` rc=1 naming `scripts/pkg`, and after re-running
   `gen_arch_map` the SAME red persists (regenerated map contains no `scripts/pkg`
   header). Differential harness: bare `__init__.py`, comment-only module, and
   private-only module (`_helper` only) all produce mirror-only keys; every geometric
   case (nested packages with real `__init__`, deep subdirs, spaces, unicode, parent
   keying for a nested scan root, `src = .`, trailing slash, dot-/`__pycache__` skips,
   non-.py in symbols mode) is consistent. Effect: the first downstream repo that adds
   a Python package gets a permanent G2+ ERROR clearable only by an LLR `Component`
   row for a module the arch map will never list — a containment demand the station
   rule never makes, i.e. new policy in effect, which the row's own SCOPE GUARD
   forbids. The 9 new tests never see it because `write_arch` commits a SYNTHETIC map
   and every fixture module is `"# m\n"` — a body the real generator would itself
   skip. -> make the mirror honor the generator's emptiness rule (skip files that
   would yield no `###` section — or make `build_map` inventory every scanned file),
   and pin the equivalence with at least one test whose committed map comes from a
   real `gen_arch_map` run, not `write_arch`. -> @builder

2. [MINOR] tests/test_trajectory_arch.py:604 (`test_added_module_delta_follows_files_mode`)
   + Deliverable "symbols/files-mode scope … pinned" -> pins an unreachable state: a
   real `--mode files` map is a table (`| Source file | Summary |`,
   gen_arch_map.py:436-438) with NO ``### `name``` headers, so `arch_inventory` parses
   it to an EMPTY inventory and the shared arming `if not (packs and
   view["inventory"])` keeps `added_module_findings` (and the whole
   `component_findings` family) dormant on every real files-mode repo — verified by
   harness (files-mode run -> inventory ∅ -> rule silent). The test reds only because
   `write_arch(_arch_n(1))` hand-writes a headered map the files-mode generator cannot
   emit. No new hole (the station rule is equally dormant there — parity holds), but
   the test certifies files-mode behavior that cannot occur and the Deliverable claim
   overstates. -> re-scope the test to what it actually pins (the mode dial's effect
   on the scan pattern) or drive it off real generator output; soften the claim. -> @builder

3. [NIT] project-trajectory/scripts/check_trajectory.py:1217 ->
   `src.strip().strip("/")` remaps an ABSOLUTE POSIX `[paths] src` (`/abs/src` ->
   repo-relative `abs/src`, usually absent -> silent dormancy) where `gen_arch_map`
   would scan the absolute dir; a leading-slash typo diverges the other way. Unusual
   declaration, warn-tier rule, note only. -> @builder

Held under attack (no finding): fail-open geometry — a module outside the declared
scan root (tests/ helper, repo-root script) is invisible to the mirror AND to the
regenerated inventory, so no policy fires at either end (no new hole, no orphaned
promise); no-double-fire is structural (`added = shipped - inventory` is disjoint
from `uncontained ⊆ inventory` — the same module can never appear in both messages)
and driven (fresh-map case reds KN_MSG only; e2e drives showed one message ever), with
the one carve-out already covered by finding 1. The MAPPING->declared-scan-root
deviation is sound (MAPPING is kit-only; `[paths] src` is exactly what check.py hands
`gen_arch_map`, single `--src`, and exists in every adopter repo). Mutation check:
removing `out.extend(added_module_findings(...))` in a scratch copy fails exactly the
two red-driving tests, the WI-387 topology test failing for the stated reason (ADDED
message absent from stderr, station message absent — the lane red is genuinely this
wiring's). Amend verified: reflog shows the amend 21 s after the original close
(2026-08-02 00:26:34 -> 00:26:55, pre-review), content = the Deliverable body + the
`specref` line removal (the disclosed stale-staged blob) — honest, R-F cleared.
Scope hygiene: dupes-allow c6270a4626d4 removal is touched-surface cleanup (the
`_stack_ini_get` collapse dissolved the sanctioned block; `check_dupes: OK - no
duplicate blocks in 49 file(s)` proves the census consistent), 13->12 re-stamped with
a dated reason; `_tests_dir` refactor is behavior-identical (empty/missing/broken all
-> "tests"). Opt-out preserved (absent `docs/components-check` = warn-first; `off`
silences — both pinned by passing tests). Mechanical re-runs on this box:
`tests/test_trajectory_arch.py` 54 passed in 1.12s; smoke 619 passed / 2 skipped in
9.86s (Deliverable stamped 615/6 — same 621 total, environment-variant skips);
`check_trajectory --strict` rc=0 (the kit's own tree does not trip the new rule),
`check_doc_refs --strict` rc=0, `check_figures --strict` OK — 21 declared figure(s);
size ratchet 3359 == `wc -l` 3359 with a reasoned stamp; docs/work delta is
WI-399-only; ruff lint + format clean on the touched files.

VERDICT: CHANGES-REQUESTED findings=3
