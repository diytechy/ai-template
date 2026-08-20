+++
id = "WI-483"
title = "Successor decomposition program: break the seven-module import cycle behind typed read models, split the largest engines by policy/effect boundary, and re-point the size-ratchet's debt owner (repo review 2026-08-19 H-02, H-05, M-02, M-06)"
specref = "docs/archive/repo-review-2026-08-19.md"
workstream = "process"
sr_refs = []
needs = ["~WI-448"]
buildtier = "strong"
safety_class = "spine"
priority = 2
+++

## Context

The review's architecture cluster, one program. The facts, verified or
already on record:

- **H-02 — the cycle.** The AST import graph (deferred imports included) holds
  one strongly connected component: `dispatch <-> handback <-> integrate <->
  intake`, plus `dispatch -> gen_trajectory -> traj_panels -> integrate` and
  `dispatch -> lane -> intake`. `handback.py`'s "never the reverse" prose is
  already false (`integrate.py:2186` — the sentence is WI-477's to fix, the
  structure is this program's). IF-088 documents dispatch's use of private
  presentation functions rather than removing it; `gen_open_items.py` imports
  the large facade for a state query.
- **H-05 — the scale, and the dead owner.** Seven scripts over 2,000 lines
  (trace 4,438 / check_trajectory 4,058 / agent_loop 3,162 / bootstrap 2,859 /
  agent_common 2,608 / integrate 2,541 / check 2,096); worst functions
  `trace.analyze` (514 lines, complexity 50), `check.steps` (494),
  `agent_loop.main` (402/27); `LoopContext` and `Registries`/`Findings` are
  empty classes populated as mutable attribute bags. The size ratchet's
  commentary directs active debt to WI-280 — CLOSED, and scoped to the
  dashboard + `bootstrap.main` only. FIRST SLICE of this program: re-point the
  ratchet's debt-owner comment here, so the baseline has a live owner again.
- **M-02 — the topology.** 59 modules, no package, 33 sibling `sys.path.insert`
  sites, private names as cross-module APIs. Direction: a stdlib-only package
  copied downstream as a unit, package-relative imports, thin direct CLI
  wrappers preserved — the MAPPING/bootstrap half is exactly WI-448's landing
  zone, hence the soft edge: WI-448's themed consolidation lands first and
  this program builds on its shape, never beside it.
- **M-06 rides along** — when a subsystem is decomposed, split its test
  monolith by stable behavior in the same slice (test_integrate 3,495 lines /
  test_trace 1,826 / test_agent_loop 1,567 / test_trajectory_arch 1,412);
  no standalone test-split slices.

Program shape (the review's, adopted as the starting plan): (1) characterize
import directions and behavior; (2) extract dependency-neutral typed modules
for work outcomes, terminal-state enums, registry-gap parsing, pending-action
queries; (3) views depend only on read models; (4) `dispatch` becomes the
top-level composer with `integrate`/`handback`/`intake`/`lane` one-way below;
(5) split `trace.analyze`, `check.steps`, and the loop state by policy/effect
boundary — typed immutable config + explicit mutable runtime state; (6)
install an SCC/layer test that includes FUNCTION-BODY imports so deferred
imports cannot hide regressions. The house exemplars to imitate are already in
the tree (review P-04): `plan_round.py`, `spine_carrier.py`, `traj_graph.py` —
pure decisions, explicit data, effects at the edge. Explicitly NOT: growing a
generic `common.py` (the review's own warning to WI-448).

Collision square: `gen_arch_map`/MAPPING/module moves are contested by
WI-455 (lane), WI-390 (clause 2), and WI-448 — read all three before opening
any slice; module moves re-point LLR `module` cells and IF endpoints, which is
why this row is `safety_class = "spine"` despite being a scripts program.
