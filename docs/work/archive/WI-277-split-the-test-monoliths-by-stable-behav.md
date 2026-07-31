+++
id = "WI-277"
title = "Split the test monoliths by stable behavior boundary (parse/decision/effect/recovery/render) once WI-280's production seams stabilize, with shared fixture modules only where they express a genuine test API"
workstream = "scripts"
needs = ["~WI-280"]
buildtier = "medium"
safety_class = "ordinary"
order = 274
+++

## Deliverable

All four test monoliths split along stable behavior boundaries, in two dependency-ordered halves.

The three independent monoliths (S6-S8): test_trajectory.py 151 tests -> parent 56 + _staged 25 (git effect/recovery) + _arch 45 (decision over architecture inputs) + _specs 25 (decision over spec bodies); test_trace.py 81 -> parent 44 + _rules 21 (pure in-process decision) + _briefs 16 (git effect/recovery); test_agent_loop.py 111 -> parent 56 + _routing 21 + _policy 26, with the genuinely git-dependent worker-endstate block appended to the existing test_agent_loop_worker.py rather than minting a stem.

The anchor (S1-S5), deferred until WI-280 landed the production seams it is organized around: test_gen_trajectory.py 5,359 lines / 163 tests -> a 295-line parent keeping 14 facade/CLI tests, plus seven modules on the traj_* boundaries - _parse 5, _graph 25, _views 37, _panels 31, _render 32, _render_sweeps 12, _status 7. The one shared fixture module the WI sanctions, tests/traj_fixtures.py, holds the 34 names that genuinely express a test API (chiefly _every_emitter_document, moved byte-identical because its docstring encodes an owner ruling, and the seven emitter builders it composes) - membership was MEASURED from the anchor's own reference graph rather than assumed, which refuted the plan's guess that _wcag was single-module. Everything used by exactly one module moved with it; no test module imports another.

Behavior preservation is proven mechanically, not asserted. For the three independent splits an AST comparison (decorator-inclusive, duplicate-aware, re-cut stricter by the reviewer) shows all 405 top-level functions surviving with exactly ONE differing body - a comment repoint - and all 12 @parametrize blocks byte-identical. For the anchor: 282 top-level names before and after across nine files, zero missing, zero extra, zero duplicated, zero bodies changed, 163 test functions equal. Tier membership is the standing guard: every one of the fourteen new stems joined conftest.SLOW_MODULES in the same commit as the module it names, the collect-only total / smoke / slow counts held flat across every slice, and tests/test_smoke_tier.py gained a permanent guard (with a derived half: every tests/test_traj_*.py on disk must map to slow) so a future edit that drops a SLOW_MODULES line fails loudly rather than silently re-joining the commit bar.

One review finding was substantive and fixed by moving code rather than editing a comment: three pure tests had landed under test_agent_loop_worker.py's module-wide git skipif and went 3 passed -> 3 skipped with git off PATH. They moved to the ungated policy module; the reviewer then drove the converse and confirmed the tests that stayed genuinely fail without git, so the gate is earned rather than inherited. The deliberate smoke re-tier that this split first makes possible at module granularity is recorded as a measured option and deliberately NOT taken - mixing it into a behavior-preserving move would make both unreviewable.
