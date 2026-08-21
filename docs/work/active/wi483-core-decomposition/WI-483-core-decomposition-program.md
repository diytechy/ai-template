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

### SLICE 1 LANDED 2026-08-20 — the first cycle edge, and the guard

**The census, re-derived rather than inherited.** The review's SCC reproduces
exactly: 7 modules, 12 intra-cycle edges, and 4 of the 12 exist only inside
function bodies. The characterization step (program shape item 1) is done and it
is now a TEST rather than a paragraph — `tests/test_import_layers.py` builds the
graph, including function-body imports, on every commit.

**The edge broken, and why this one first.** `traj_panels` — a render leaf that
writes nothing — imported the 2,541-line merge coordinator for exactly TWO
constants. That is the review's "the dashboard can drag mutation coordinators
into read-only rendering", literally and in one import line. The lane-close
terminal-outcome vocabulary moved to `project-trajectory/scripts/kitlib/station.py`
as a typed read model (`Outcome`, a `str` enum; `OUTCOME_DIRS`, immutable;
`outcome_of`, the "exactly one declared directory, or none" DECISION lifted out
of `integrate.branch_outcomes`, whose git-tree read stays where the effect
belongs). `integrate` re-exports the former names, so no caller moved.

**Cutting one edge dropped TWO modules from the cycle: 7 -> 5.** `traj_panels`'
only route into the component was that import, and `gen_trajectory`'s only route
in was through `traj_panels`. The remaining SCC is the lifecycle core proper —
`dispatch`, `handback`, `intake`, `integrate`, `lane` — and it is baselined in
the ratchet, which may only tighten.

**TOPOLOGY DECISION (recorded here because the row is `safety_class = spine`).**
The read model landed in `kitlib/` — the `station` theme slot WI-448 named and
deliberately left uncreated, handing it to this row — under a NEW `LLR-182` with
a SINGLE `CMP-008` tag, NOT appended to `LLR-181`'s module list. Appending would
have been one line cheaper and was rejected: `LLR-181` carries the four-way
usage tag `OI-48` is open about, and a four-way tag SUPPRESSES the
cross-component seam rule on the module's edges — so the view-to-service seam
would have stopped being policed at the exact moment it was fixed, and the slice
would have spent an unruled owner question to tidy its own diff. A single tag is
also true here in a way it is not for the shared kernel: the station flow's
modules are all CMP-008. `IF-093` is therefore RE-POINTED (counterpart
`scripts/kitlib/station`, owner `LLR-182`) and stays a policed CMP-009 to
CMP-008 seam. This gives `OI-48` a worked data point — per-theme ownership is
available where a theme has an owner — but does NOT pre-empt it.

**STILL OWED BY THIS ROW — the reason it is not closed:**

1. **The five-module lifecycle SCC**, the hard half. Its three back edges
   (`intake` to `dispatch`, `integrate` to `handback`, `integrate` to `intake`)
   are all deferred function-body imports carrying real lifecycle behaviour, not
   constants — program shape items 2 and 4 (extract lifecycle result types, make
   `dispatch` the outer composer). Nothing here was attempted this slice.
2. **`IF-088` and `gen_open_items`** — `dispatch._pending_cards` still calls the
   private presentation functions `_blocked_pending`/`_spine_pending`, and
   `gen_open_items` still imports the large facade for a state query. Both are
   documented bad edges rather than broken ones; neither is inside the SCC, so
   neither was on this slice's critical path.
3. **The engine splits (program shape item 5)** — `trace.analyze` (514 lines,
   complexity 50), `check.steps` (494), `agent_loop.main` (402/27), and the
   `LoopContext` / `Registries` / `Findings` attribute bags. Untouched. Note the
   standing trap when they are: ruff's C901 counts a nested def into its
   enclosing function, so a helper extracted INWARD raises the number the
   extraction was meant to lower — decompose outward.
4. **M-06's test-monolith splits**, which ride along with each subsystem
   decomposed. `test_traj_panels` and `test_integrate` were both touched here but
   neither needed splitting for this edge, and a standalone split slice is
   explicitly out of scope.

**Deferred to the owner: nothing new.** `OI-48` is engaged by this row's
topology decision but is NOT widened by it — the slice was deliberately built so
that the ruling stays free either way.
