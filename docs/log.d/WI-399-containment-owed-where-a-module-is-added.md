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
  `[arch-map] mode`, the exact inventory `gen_arch_map` reads (`*.py` in
  symbols mode, every non-hidden source file in files mode, the same
  dot/`__pycache__` skip, keys relative to the root's parent) — and the delta
  against the COMMITTED inventory (`arch_inventory`) is joined through the LLR
  `Component` cells exactly as the station rule joins. A delta module with no
  real-CMP membership is the same finding class at the same tier (WARN plain,
  ERROR under `--strict`), with the same pack arming and the same
  `docs/components-check: off` opt-out. A fresh map (every trunk checkout after
  the refresh) makes the delta empty, so the station's own rule — untouched —
  never double-fires and stays the backstop. No new policy, no new registry
  surface: the existing rule, an earlier firing point.
- **Driven, red-then-green** (`tests/test_trajectory_arch.py`, 9 new tests):
  the wi-387 topology reproduced as the class this row closes — a
  stale-but-contained committed map plus an untagged on-disk module REDS the
  lane bar naming the module, while the station rule itself has nothing to say
  (the station-first shape, now impossible); the LLR `Component` tag greens the
  same tree with no regeneration. Pinned around it: no double-report when the
  map is fresh, shared pack arming (dormant without packs), shared opt-out,
  pre-arch-map vacuity, symbols-mode `*.py` scope, files-mode breadth, and the
  hidden/`__pycache__` skip. Watched red first: 2 failed on the
  pre-implementation tree (`test_added_module_without_component_tag_reds_the_lane_bar`,
  `test_added_module_delta_follows_files_mode`) — historical, that tree is
  gone; all 9 green under the fix.
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
