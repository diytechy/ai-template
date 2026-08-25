+++
id = "WI-508"
title = "The architectural remapping program: blind minimal-map re-derivation, divergences filed as consolidation WIs"
specref = "docs/requirements/open-items.toml#OI-58"
workstream = "process"
sr_refs = ["SR-163"]
needs = ["WI-448", "WI-483", "WI-507"]
buildtier = "strong"
safety_class = "spine"
priority = 2
+++

## Context

Executes OI-58's (c) half — minted NOW at the owner's explicit
instruction so it is not lost to history, sequenced (needs) behind the
wi448/wi483 consolidation lanes and the WI-507 doctrine so the remap
reads settled ground and inherits the measured baseline.

The shape, grounded in the repo's proven method (the WI-467 blind
re-derivation precedent): an agent re-derives the MINIMAL module map from
the requirements alone — blind to the live layout — with the objective
the owner stated: serve the declared outputs while minimizing internal
signal overlap and duplicated behavior (calls, not lines). The live map
diffs against it; each divergence is adjudicated (consolidate / keep with
reason) and filed as consolidation WIs feeding the wi448/wi483 lanes.
The research grounding recorded on OI-58's row (minimum-description-
length, deep-modules, the repo's own one-home findings) is the derivation
brief's framing. Multi-session program lane; slices end green at the
commit bar; spine-touching consolidations follow the ordinary approval
machinery under the declared dial.

**Orphan fold-in (owner-directed 2026-08-22):** the remap IS `SR-163`'s
verification exercise (every shipped file maps to a stakeholder outcome)
— decompose that SR into its LLR/TC as the program's slice 1 framing act,
so the blind derivation has the requirement it is checking traced before
it runs.

### RE-VALIDATED against the amended SpecRef and the amended `SR-163`

The checker carried two staleness warnings on this row. Both were READ
before the lane opened rather than cleared by the touch, and the row
STANDS with its scope unchanged:

- **`SR-163` (cited).** Amended exactly once since this row was last
  touched, and the whole amendment is the addition of
  `hat_refs = ["MAINTAINER"]` in the perspective backfill. The normative
  `requirement`, the `rationale` and the `acceptance_criteria` cells are
  byte-identical to the text this row was minted against, so the
  obligation the program verifies has not moved. The added lens SHARPENS
  the derivation brief rather than redirecting it: `MAINTAINER` asks
  *"can a reader two years from now tell why this exists, and what would
  break if they deleted it?"*, which is the remap's own question asked of
  a module instead of a row.
- **`docs/requirements/open-items.toml` (the SpecRef).** `OI-58`'s own
  row has not changed since it was ruled — that commit PRECEDES this
  row's last touch, so the warning is file-level. What changed in the
  file is the arrival of `OI-60`, `OI-61`, `OI-62` and `OI-63`. All four
  were read for retasking and none touches this program's scope; they
  belong to the interface-registry lane. **`OI-63` is explicitly NOT this
  row's to execute** — it is the interface `contract` relocation question
  and is pending the owner's ruling.

### Inherited debt, taken on at the WI-483 close

Both items ride along with whatever this program decomposes; neither is a
standalone slice, and neither is discharged by the framing act.

1. **The module-size ratchet's debt owner.** `tests/test_module_size_
   ratchet.py` names this row in its module docstring, its BASELINE
   header and its failure message, and `tests/test_import_layers.py`
   carries two more pointers. The pointer must not rot again: closing
   this row while it is named there recreates the H-05 defect the WI-483
   lane opened by fixing.
2. **M-06's four test monoliths, re-measured at that close:**
   `tests/test_integrate.py` **3,520**, `tests/test_trace.py` **2,099**,
   `tests/test_trajectory_arch.py` **1,927**, `tests/test_agent_loop.py`
   **1,640**. The standing rule is unchanged — a split RIDES ALONG with a
   subsystem decomposition and a standalone split slice is out of scope.
   The WI-483 close also banked the reason nothing noticed them growing
   5–36%: the size ratchet censuses `SCRIPTS` only, so **no armed sensor
   watches the test tree**. Whether the census should extend there is a
   real question for this program, not a drive-by.

### Slice plan

1. **Framing (LANDED).** Re-validate the row against the amended
   requirement, claim it, and decompose `SR-163` into its LLR/TC so the
   requirement the remap checks is traced before the derivation runs.
2. **The blind derivation.** Write the brief, run it against a strictly
   bounded input set (requirements + the depth-0 frame + the hat roster —
   never the design tier, the component or interface registries, or the
   source tree), and record brief and return durably.
3. **The alignment pass.** The only role permitted to read both sides:
   build the map — matched / present-only-in-live / present-only-in-
   derived — with each divergence adjudicated, never silently merged.
4. **File the consolidations.** One WI per adjudicated divergence that
   earns one, feeding the existing lanes rather than minting a rival
   program.

### SLICE 1 LANDED 2026-08-25 — the framing act: `SR-163` is decomposed

**Four rows minted, all `Drafted`, and the pair discipline is WI-510's:
name the real delivered mechanism, and state plainly what does not
exist.** `SR-163` leaves the orphan list (orphans **4 → 2**; only
`SR-181` remains, owned elsewhere) with `integrity=0` unchanged.

- **`LLR-203`** — *the shipped-file inventory and its declared
  exclusions, carrying no purpose reference.* Module
  `project-trajectory/scripts/bootstrap.py`, symbol `MAPPING`,
  `CMP-009`. Two of the parent's four finding classes are ALREADY
  delivered and driven: the scaffold-coverage walk reports a declared
  destination this repository neither carries, serves in place, nor
  declares as an absence, and reports a declared absence that has since
  materialized; the package-completeness check asks a REAL scaffold
  whether the copied helper package is the kit's module set, naming a
  missing or stale row as the cause; and the sibling-import closure
  catches a shipped script importing a file the inventory omits.
  `docs/declared-absences` is the recorded-exclusions carrier.
  **NOT DISCHARGED, on the row:** a `MAPPING` row is a source/destination
  pair plus a comment, so **no cell joins an inventoried file to a
  requirement id**; every delivered arm walks the DESTINATIONS the
  inventory declares rather than the shipped tree, so a kit file the
  inventory omits altogether is outside all of them; and the installer's
  own exclusion — the one that is load-bearing for the distribution model
  — is prose at its module rather than a row anyone can enumerate.
- **`TC-199`** — Integration / Full, verifying `SR-163` + `LLR-203`.
  Evidence is 5 EXISTING node ids across `tests/test_dogfood_sync.py`
  (the walk, its stale-entry honesty half, and the bite proof that
  removing one declared entry makes its destination reappear) and
  `tests/test_bootstrap.py` (package completeness and sibling-import
  closure, both asked of a real bootstrapped scaffold).
- **`LLR-204`** — *the purpose-reference grammar and its declared
  warn-to-gate dial, running the other direction.* Module
  `project-trajectory/scripts/gen_arch_map.py`, symbols
  `backlink_ids/scan_backlinks/read_backlink_min`, `CMP-006`. The
  `Implements:` grammar is the ONE definition of a purpose declaration in
  the source surface, and the declared threshold delivers exactly the
  warning-to-gating shape the parent's fourth clause asks for — warn at
  exit zero, gate only on the strict arm the harness appends from the
  tests rung on. **NOT DISCHARGED, two independent ways:** DIRECTION —
  the report asks whether each design row is NAMED by a source
  declaration, the parent asks the inverse, and a full reading here is
  compatible with a tree in which no file declares anything; UNIVERSE —
  the scanned roots are the declared source paths, so the grammar never
  sees a template, registry seed, launcher, workflow or process document,
  which is the greater part of the inventory.
- **`TC-200`** — Integration / Full, verifying `SR-163` + `LLR-204`.
  Evidence is 2 EXISTING node ids in `tests/test_gen_arch_map.py`: the
  grammar driven on the shared function both the map column and the
  coverage percentage read, and the warn-then-gate exit contract driven
  through the real command line on a real scaffold.

**What this buys the derivation, which is the point of doing it first.**
The blind agent is asked for the minimal set of modules that serves the
declared outputs. `SR-163` is the requirement that says every shipped
file must be traceable to a stakeholder outcome — so the derivation's
output IS the evidence for that row, and its two LLRs now say exactly
which half of the join exists (the grammar and the policy) and which
half does not (the direction and the universe). The remap is therefore
not a free-standing opinion about layout: it is the missing side of a
join the registry already half-carries.

**Deliberately NOT done here.** No purpose-coverage checker was built and
no module or symbol was invented to cite — the parent's tier discipline
is that a cited symbol must exist to be read, and the honest state is
that the mechanism is unbuilt. Neither `SR-163` nor any other `Approved`
cell was rewritten; the four rows are authored, not amended, so no
approval act is claimed and none was needed.

**Watermarks** `LLR` 202 → 204, `TC` 198 → 200, via `trace.py
--bump-ids`. Record:
[../../../log.d/2026-08-25-wi508-slice1-sr163-decomposition.md](../../../log.d/2026-08-25-wi508-slice1-sr163-decomposition.md).
