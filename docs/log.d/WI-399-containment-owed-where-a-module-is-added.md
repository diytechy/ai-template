## 2026-08-02 — WI-399: containment is owed where a module is ADDED

**Summary.** `docs/architecture.md` is trunk-owned, so its freshness gate SKIPs
on a claimed work branch (SR-133) and a module a branch adds enters the
arch-map inventory only when the station's refresh regenerates the map — AFTER
the last review round, which made the station the FIRST place the
knowledge⇒component `--strict` red could exist. Twice driven with the identical
two-registry-row remedy, each costing a review round and a station red:
`drive.py` (WI-374 era) and `handback.py` (WI-387, the 2026-08-01 blocking red
whose "tested and refuted" hypothesis was in fact correct — the refuting probe
measured a trunk-vintage map; [handoff-2026-08-01.md](../handoff-2026-08-01.md)
§2/§6); WI-393 dodged the class the same day only by registering `spec_move.py`
defensively at build time. The SAME rule now also fires in the lane's own bar
at the commit that adds the module, keyed off what the lane CAN see with no
regeneration — so the station can never again be the first to know.

**Deliverables.**

- **The early firing point** (`check_trajectory.py`:
  `added_module_findings` + `shipped_modules` + `_arch_scan_profile`, wired as
  the fourth rule of `component_findings`): the shipped-module set is derived
  from the declared arch-map scan root — `docs/stack.ini` `[paths] src` +
  `[arch-map] mode` — and mirrors `gen_arch_map.build_map`'s symbol-mode
  collection exactly: `*.py` under the root (absolute or repo-relative), the
  same dot/`__pycache__` skip, keys relative to the root's parent, and the
  same symbol-emptiness skip (`_would_be_inventoried`; the REVIEW-A rework
  below). Files mode is dormant by parity — a real files-mode map has no
  `### ` module headers, so `arch_inventory` is empty and the whole family is
  off there. The delta
  against the COMMITTED inventory (`arch_inventory`) is joined through the LLR
  `Component` cells exactly as the station rule joins. A delta module with no
  real-CMP membership is the same finding class at the same tier (WARN plain,
  ERROR under `--strict`), with the same pack arming and the same
  `docs/components-check: off` opt-out. A fresh map (every trunk checkout after
  the refresh) makes the delta empty, so the station's own rule — untouched —
  never double-fires and stays the backstop. No new policy, no new registry
  surface: the existing rule, an earlier firing point.
- **Driven, red-then-green** (`tests/test_trajectory_arch.py`, 12 new tests
  after the rework):
  the wi-387 topology reproduced as the class this row closes — a
  stale-but-contained committed map plus an untagged on-disk module REDS the
  lane bar naming the module, while the station rule itself has nothing to say
  (the station-first shape, now impossible); the LLR `Component` tag greens the
  same tree with no regeneration. Pinned around it: no double-report when the
  map is fresh, shared pack arming (dormant without packs), shared opt-out,
  pre-arch-map vacuity, symbols-mode `*.py` scope, files-mode dormancy parity,
  the hidden/`__pycache__` skip, and the differential harness (below). Watched
  red first: 2 failed on the
  pre-implementation tree (`test_added_module_without_component_tag_reds_the_lane_bar`
  plus the since-replaced files-mode test) — historical, that tree is gone.
- **The lane seam, verified live:** on this claimed branch
  `check.py --run-step trajectory` runs the step (PASS, not SKIP) — the
  `trajectory` step was already branch-runnable (not in
  `_TRUNK_FRESHNESS_STEPS`), which is exactly why moving the firing point into
  `component_findings` needed no `check.py` change and leaves `--trunk-lane`
  and the SR-133 freshness skips untouched.

**Deviations and judgments.**

1. **The shipped-module set derives from the declared scan root, not
   `bootstrap.py`'s MAPPING literally.** The spec named both ("bootstrap.py's
   MAPPING and the scripts dir"); MAPPING is kit-only (a downstream repo has no
   `bootstrap.py`), while `[paths] src` is the same declaration `check.py`
   hands `gen_arch_map` — so the delta is exactly what the refresh WOULD
   inventory, in any adopter repo, and every shipped kit module lives under the
   scripts dir either way.
2. **No new LLR/TC rows owed** (the WI-398 precedent): no module was added; the
   rule is an internal of `component_findings`, already registered under
   LLR-049/SR-087, and the new tests land beside that row's existing evidence
   module.
3. **A dupes-census red at the commit bar was answered by REUSE, not
   sanction:** the first cut duplicated the lenient stack.ini read a third
   time, which surfaced three unclassified blocks — including a latent
   `bootstrap.py == check_trajectory.py` pairing. Both in-file copies collapsed
   onto one `_stack_ini_get` (shrinking `_tests_dir`), the cross-script block
   dissolved, and its now-dead sanction was REMOVED: `docs/dupes-allow`
   `declared-file` class re-stamped 13 → 12 blocks, reason in place.
   <!-- fig: cmd="python project-trajectory/scripts/check_dupes.py --src project-trajectory/scripts" rev=278eea0f -->
4. **Size ratchet re-stamped upward, reason in the baseline comment:**
   `check_trajectory.py` 3261 → 3359 (+98), roughly half of it the mechanism
   comment that keeps a successor from "simplifying" the firing point back to
   the station.
   <!-- fig: derived="len(text.splitlines()) at 278eea0f, the ratchet's own metric (tests/test_module_size_ratchet.py)" -->
5. **Pre-existing trunk red surfaced, not fixed inline:** the commit-bar
   `check_docs.py --stale` run reports 4 broken links in three closed specs
   (`docs/work/complete/` WI-070 / WI-173 / WI-288), byte-identical on trunk —
   inherited residue outside this row's scope, left for a trunk-side fix.

**Byte budgets:** none of the budget-watched docs touched (no
`AGENTS.template.md` / `PROCESS.md` / `PROCESS_OPTIONS.md` edits).

**Watched, measured on the build commit 278eea0f:**
`tests/test_trajectory_arch.py` 54 passed in 1.15s
<!-- fig: cmd="python -m pytest -q -n auto tests/test_trajectory_arch.py" rev=278eea0f -->;
smoke tier 615 passed / 6 skipped in 10.42s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=278eea0f -->;
full unfiltered suite 1853 passed / 10 skipped in 282.47s (0:04:42)
<!-- fig: cmd="python -m pytest -q -n auto" rev=278eea0f -->;
`check_trajectory --strict` / `check_doc_refs --strict` / `check_figures
--strict` all rc=0 on this tree (the delta is empty here — the committed map
already carries all 49 shipped modules
<!-- fig: derived="ls project-trajectory/scripts/*.py | wc -l == grep -c '^### `scripts/' docs/architecture.md, both 49 at 278eea0f" -->,
so the kit's own bar is green by construction, not by exemption).

**REVIEW-A rework (2026-08-02, CHANGES-REQUESTED findings=3, one commit).**

1. **(MAJOR) The delta over-collected against the generator it claimed to
   mirror.** `gen_arch_map.build_map` SKIPS symbol-empty modules (bare
   `__init__.py`, comment-only, private-only) from the MODULE MAP, so the
   first cut's every-non-hidden-`*.py` scan redded such a module under
   `--strict` and kept it red after the trunk regen FOREVER (the map never
   absorbs it, the delta never empties) — accidental new policy, the scope
   guard breached. Fixed at the class: `_would_be_inventoried` mirrors the
   generator's emptiness predicate (`summary or imports or contracts or
   rows`; a PARSE ERROR module stays inventoried), with
   `_has_internal_import` mirroring the import-walk arm. The pin is
   DIFFERENTIAL, not synthetic: `regen_map` runs the REAL `gen_arch_map`
   over the fixture tree, and the tests assert the delta empties exactly
   when the regenerated map absorbs the module —
   `test_differential_delta_empties_exactly_when_the_regen_absorbs` (lane
   red → regen absorbs → `ADDED` message gone with the station rule holding
   the same red → tag clears both) and
   `test_symbol_empty_module_reds_neither_side_of_the_regen` (green on BOTH
   sides). Watched red first: the symbol-empty test failed under the build
   commit's code (rc=1 where green was owed), green under the mirror.
2. **(MINOR) The files-mode test pinned an unreachable state** (a synthetic
   symbols-shaped map under a `files` declaration). Replaced by the honest
   claim, driven against a real `--mode files` regeneration:
   `test_files_mode_real_map_keeps_the_whole_family_dormant` — no `### `
   headers, empty inventory, the whole family dormant, parity with the
   station rule (`shipped_modules` now returns empty in files mode by
   design rather than scanning what could never be absorbed).
3. **(NIT) An absolute `[paths] src` was silently remapped repo-relative**
   by the `strip("/")`; it now scans the path it names, as `gen_arch_map`
   treats `--src` — watched red
   (`test_absolute_declared_src_scans_like_the_generator` failed under the
   build commit's code, no red where one was owed) then green.

Bookkeeping: `check_trajectory.py` baseline 3359 → 3428 (reason in the
stamp); the import-walk mirror sanctioned under the F5 `module-path` class
(2 → 3 blocks, drift-guarded by the differential tests — the census note
says so in place).

**Watched after the rework (the tree of the rework commit):**
`tests/test_trajectory_arch.py` 57 passed in 1.28s
<!-- fig: cmd="python -m pytest -q -n auto tests/test_trajectory_arch.py" rev=this-rework-commit -->;
smoke tier 619 passed / 2 skipped in 9.98s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=this-rework-commit -->;
`check_trajectory --strict` / `check_doc_refs --strict` / `check_figures
--strict` all rc=0.
