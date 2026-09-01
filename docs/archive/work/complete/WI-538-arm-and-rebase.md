+++
id = "WI-538"
title = "Arm the complexity sensor here at the ruled scope, and re-base the module-size ratchet to SLOC (OI-68 phase 2, 1c)"
specref = ""
workstream = "process"
sr_refs = []
needs = ["WI-537", "~WI-521"]
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Executed OI-68 phase 2 at the ruled shape **1c / 2a / 3a / 4a** — arm + re-base,
never arm + retire. Both sensors stay armed on different axes; nothing was deleted
and no pointer moved.

1. **Armed (3a).** New `[step:complexity]` in `docs/stack.ini`
   (`command = {py} project-trajectory/scripts/check_complexity.py --root . --mode
   enforce`, `layer = product`, `from-stage = DevStg-Impl`) — the exact-equality
   compare against `docs/complexity-baseline` in both directions, nonzero on
   either. Minted no spine row: `SR-183` already carries both postures ("gated only
   where a repo opts in"), and the opt-in is the step's presence here.
   `check_complexity.py`'s module docstring updated from "report-only as shipped" to
   "report-only where shipped, armed here". Shipped default stays report-only
   (that's phase 3, a separate WI).

2. **Scoped (2a).** `check_complexity.DEFAULT_INCLUDE` widened to census `tests/`
   as well as `project-trajectory/scripts/`; `docs/complexity-baseline` re-stamped
   to seed the 20 `tests/` functions over threshold 15 (census now 200 rows: 180
   scripts + 20 tests). This closes WI-521 §3's sensor gap on the complexity axis;
   WI-521 amended in place to record that, and to state honestly what is still
   unwatched (test-tree *size* growth — no function crossing cognitive 15 — is
   watched by neither armed sensor).

3. **Re-based (1c).** `tests/test_module_size_ratchet.py` re-based from raw
   physical lines to **SLOC** via the shared `check_complexity.module_sloc`
   (factored out of `sloc`/`_sloc` so the size ratchet and the complexity sensor
   read one definition of a source line). `THRESHOLD` 1500 → **1000 SLOC**; the
   `BASELINE` dict fully re-stamped to SLOC values (trace 6005→3364, agent_loop
   4100→2519, check_trajectory 4653→2223, bootstrap 3166→1571, integrate
   2655→1265, agent_common 2690→1262, gen_arch_map 2230→1262, check 2466→1163,
   intake 1990→1081 — exactly the same 9 modules, per the 900–1000 clean-gap
   derivation on record). Per-entry raw-line history kept verbatim (a dated record
   rewritten to numbers that never existed on its date would falsify it).
   `traj_context.py`'s stale "1,500-line threshold" docstring generalised.
   `docs/enforcement-audit.md` "Right-size" row updated from Reviewer-only to
   Reviewer + Harness (this repo, partial).

**Not done, deliberately:** retired no sensor (ruled out by 1c); shipped nothing
downstream (bootstrap MAPPING, template step, PROCESS_OPTIONS layer,
deep-module-design skill — all phase 3); minted no spine row and touched no
registry, so no approval-brief regen. OI-68 was already `ruled` at the sitting, so
no `open-items.toml` edit.

**Verification.** `check_complexity.py --root . --mode enforce` → `OK - 200 row(s)
over 15, unchanged from baseline`, exit 0. Full unfiltered suite green (see the log
fragment for the paste).

## Context

**What this row does.** Phase 2 of the OI-68 complexity-sensor program, at the
shape the owner RULED on 2026-08-30 — **1c / 2a / 3a / 4a** (the record is
`docs/requirements/open-items.toml` `[open_item.OI-68]`, `status = "ruled"`). The
driver recommended 1a (retire the line ratchet); the owner ruled **1c** — BOTH
sensors stay armed, they measure different axes (module SIZE and function
COMPLEXITY), and the module-size ratchet is RE-BASED from raw physical lines to
SLOC. So this phase is **arm + re-base**, never arm + retire: nothing is deleted,
no pointer is moved. The plan's phase-2 draft
(`docs/plans/2026-08-29-complexity-sensor-plan.md#phase-2--arm-it-here-and-retire-whichever-sensor-the-ruling-retired`)
predates the ruling and is written for 1a; the ruling governs where they differ.

**Three acts, one direction.**

1. **Arm (Q3 → 3a).** Add `[step:complexity]` to `docs/stack.ini`
   (`layer = product`, `from-stage = DevStg-Impl`) running
   `check_complexity.py --root . --mode enforce` — the exact-equality compare in
   both directions, nonzero on either. Growth fails ("simplify, or take a reviewed
   baseline bump whose reason lands in the log"); improvement fails ("re-stamp
   downward in the same commit"). No inline suppression pragma — the central
   baseline is the one escape hatch. Arming mints NO new spine row: `SR-183`
   already carries both postures in one contract ("gated only where a repo opts
   in"), and the opt-in IS the step's presence here. Report-only stays the shipped
   default; shipping downstream is phase 3, a separate WI.

2. **Scope (Q2 → 2a).** The sensor censuses `tests/` as well as
   `project-trajectory/scripts/` — widened in `check_complexity.DEFAULT_INCLUDE`,
   the single home of this repo's census surface — and `docs/complexity-baseline`
   is re-stamped to seed the `tests/` functions over threshold. The line ratchet
   stays scripts-only, per the ruling. This closes WI-521's §3 sensor gap on the
   right axis instead of by extending the disputed line axis to a second tree.

3. **Re-base (Q1 → 1c).** `tests/test_module_size_ratchet.py` re-bases from raw
   physical lines to **SLOC** (non-blank, non-comment, non-docstring) — the
   definition held once beside the sensor (`check_complexity.module_sloc`) and
   IMPORTED by the ratchet, so both sensors share one definition of a source line.
   `THRESHOLD` re-bases 1500 → **1000 SLOC**; the `BASELINE` dict is fully
   re-stamped to SLOC values with the derivation on record. Nothing deleted: the
   test file, its `docs/stack.ini` `[generated]` `linecounts` row, its
   `tests/test_generated_freshness_wiring.py` `OTHERWISE_ENFORCED` entry, and
   WI-521's debt-owner pointer all stay. WI-521's §3 is amended to record what the
   ruling answered (the sensor gap is now closed; the line ratchet keeps its
   distinct module-SIZE job on the code axis).

**Threshold derivation.** The 9 modules the raw-1500 ratchet baselined score
1081–3364 SLOC (`intake.py` smallest at 1081); the largest non-member is
`traj_panels.py` at 891 SLOC. A SLOC threshold in 900–1000 preserves exactly those
9 — a clean 190-line gap — so 1000 re-stamps the current watch set onto the code
axis, deleting no entry and admitting none. That is the "full re-stamp with the
derivation on record" the ruling names.

**Q4 → 4a** is already satisfied by the shipped sensor (match = one increment,
comprehension `if` takes the nesting increment, threshold 15); nothing here
re-opens it.

**Not in scope.** Retiring any sensor (ruled out by 1c). Shipping downstream (the
`bootstrap.MAPPING` row, the commented template step, the `PROCESS_OPTIONS.md`
layer, the `deep-module-design` skill — all phase 3). The relative-churn sensor.
