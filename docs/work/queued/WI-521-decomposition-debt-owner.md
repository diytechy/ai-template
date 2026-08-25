+++
id = "WI-521"
title = "The decomposition debt owner: four wide modules, M-06's four test monoliths, and no sensor watching the test tree"
specref = "docs/plans/2026-08-25-remap-alignment.md"
workstream = "process"
sr_refs = []
needs = []
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Context

**This row is the module-size ratchet's named DEBT OWNER.** The pointer in
`tests/test_module_size_ratchet.py` moved here from `WI-508` in the same commit
that filed this row, and the reason is the ratchet's own rule, applied one step
further than it has been before.

### Why the pointer moved rather than waiting for `WI-508` to close

The ratchet's docstring records the chain: it directed active debt to `WI-280`
for months after that item closed — "a ratchet whose commentary names a closed
item tells the next author that the debt is somebody's when it is nobody's,
which is the one thing a growth sensor must not do" — so `WI-483` took ownership
on its first day, and handed it to `WI-508` at its close.

Two things make a third hand-off at close the wrong mechanism:

1. **A close-time re-point is a promise; a filed row is a fact.** It has been
   honoured once, deliberately and with the defect named. Relying on it a second
   time makes the sensor's honesty depend on a future session remembering.
2. **`WI-508` was never the right owner for this AXIS, and the ratchet says so
   about its predecessor in the same words.** The docstring notes `WI-483`
   "CLOSED having paid down the axis it was scoped for ... which is precisely
   NOT this file's axis". The same is true here: `WI-508` is a **consolidation**
   program — minimize duplicated behaviour — while this ratchet measures module
   **size**, which is decomposition. `WI-508` inherited the pointer for being the
   live architectural program, not for being scoped to the axis.

So the pointer now names a row scoped to the axis it measures, and **`WI-508`'s
eventual close has nothing to re-point.** That is the dead-owner defect made
unreachable rather than deferred again.

**THIS ROW IS A STANDING DEBT OWNER, NOT A ONE-SITTING TASK.** Do not claim it
expecting to finish it. It is claimable for one scoped slice at a time, and it
is closed only when the debt below is paid or re-homed — and if it is ever
closed, **the ratchet pointer must move in the same commit**, which is the rule
it inherited.

### What it owns — 1: the four wide modules, corroborated from the requirements side

`WI-508`'s blind derivation produced evidence this debt has never had. Two agents
derived a minimal module map from the requirements alone, and where **both**
agreed two obligations belong in *different* modules while the live tree fuses
them, the fusion clusters hard:

| live module | obligation pairs both derivations put APART |
| --- | --- |
| `agent_loop` | 14 |
| `check_trajectory` | 13 |
| `agent_common` | 10 |
| `bootstrap` | 5 |
| `trace`, `check_privacy` | 2 each |
| `check`, `check_doc_refs` | 1 each |

fig: derived="pairs (x,y) of SRs where derivation A and derivation B each place x and y in different modules while the live SR->module join puts them in the same one; the live join reads LLR `module` cells through `sr_refs`"

These are the same four modules the ratchet has baselined as its largest, reached
by a completely independent route — from what the requirements say belongs
apart, not from line counts. **That agreement is the row's strongest asset**: a
size ratchet alone can be answered with "it is big because it does a lot"; this
says which obligations a reader has to hold at once to read it.

**It is NOT a mandate to split all four.** `WI-483` measured `check.steps` and
deliberately LEFT it on four recorded grounds, and that decision stands. Any
slice here re-measures first and may reach the same answer.

### What it owns — 2: M-06's four test monoliths, which now ride nothing

Re-measured at the `WI-483` close: `tests/test_integrate.py` **3,520**,
`tests/test_trace.py` **2,099**, `tests/test_trajectory_arch.py` **1,927**,
`tests/test_agent_loop.py` **1,640**.

`WI-483`'s item 4 ruled that a test split **rides along** with a subsystem
decomposition and that a standalone split slice was out of scope. That rule was
honoured for all seven of its slices and it delivered nothing: every slice
checked its touched tests and none needed a split. `WI-508` then filed no
subsystem decomposition at all, so there was no vehicle to ride.

**This row inherits them, and is explicitly NOT bound by that rule.** The
ride-along constraint was `WI-483`'s own scope decision, not a standing ruling,
and it has now failed to deliver across two programs — which is the evidence
that a rider with no vehicle is a rider that never moves. A standalone split is
in scope here. It should still be taken by stable behaviour boundary rather than
by line count, and a slice that decomposes a subsystem should still take its
tests with it.

### What it owns — 3: the sensor gap, and the unruled question under it

`tests/test_module_size_ratchet.py` censuses `SCRIPTS` only, so **no armed
sensor watches the test tree** — which is why three of the four monoliths grew
5–36% between the 2026-08-19 review and the `WI-483` close with nothing saying
so.

**Do not just extend the census.** That file's own docstring banks an unruled
owner question — whether the line-count axis survives at all, given the owner's
`OI-16` correction that "the monolith risk was always about FUNCTION size and
complexity, not file length" and the worked counterexample where a structurally
simpler `bootstrap.py` was made to demand a reviewed bump. Extending a disputed
axis to a second tree doubles whatever is wrong with it. The honest sequence is
to raise the axis question with the measurement this row can now supply, and
extend only what survives the answer.

### Standing constraints

- Every slice ends green at the commit bar; a baseline is re-stamped only
  deliberately, with the reason in the log, and **never to clear a finding**.
- Moving lines into a new module is the intended escape hatch: the new module
  stays under `THRESHOLD` or earns its own reviewed baseline, and the shrunk one
  re-stamps downward in the same commit.
- If this row closes, **move the ratchet pointer in the same commit.**
