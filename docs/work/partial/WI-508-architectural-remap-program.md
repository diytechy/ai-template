+++
id = "WI-508"
title = "The architectural remapping program: blind minimal-map re-derivation, divergences filed as consolidation WIs"
specref = ""
workstream = "process"
sr_refs = ["SR-163"]
needs = ["WI-448", "WI-483", "WI-507"]
buildtier = "strong"
safety_class = "spine"
priority = 2
+++

## Deliverable

OI-58's (c) half executed: the architecture was blind-re-derived from the
requirements alone, diffed against the live map, and every divergence adjudicated
— consolidations filed as their own rows rather than merged in place. Six slices,
2026-08-25 → 2026-08-30.

- **`SR-163` decomposed (slice 1).** Four rows minted: `LLR-203`/`TC-199` (the
  shipped-file inventory `bootstrap.py::MAPPING` and its declared exclusions) and
  `LLR-204`/`TC-200` (the purpose-reference grammar
  `gen_arch_map.py::backlink_ids`/`scan_backlinks`/`read_backlink_min` and its
  warn-to-gate dial). Each LLR names a delivered, tested mechanism and states its
  undischarged half on-row (the file→requirement join, and the direction/universe
  gaps). The two **LLRs are `Approved`**; the two **TCs are `Drafted`** — slice 6
  blessed all four, but REVIEW-A found the TCs over-claimed `SR-163` (they verify
  only the delivered LLR arms, not the parent's full join and universe), so the
  rework reverted `TC-199`/`TC-200` to `Drafted`, and the round-013 rework
  removed `SR-163` from both rows' `verifies` (they now cite only `LLR-203` /
  `LLR-204`): the cited tests exercise the delivered inventory/grammar/policy
  arms only, and a TC naming the SR made the coverage matrix read `SR-163` as
  tested whatever its `Status`. `SR-163`'s requirement is approved; its full
  verification remains honestly owed and **unscheduled**, and it is back on
  the orphan list as `SR-163 has no test (TC)` — the true state. No active or
  queued WI owns the complete file→requirement join and shipped-universe
  acceptance criteria; in particular, `WI-519`/`WI-520`/`WI-521` carry distinct
  consolidation findings, have empty `sr_refs`, and do not carry `SR-163`,
  `LLR-203`, or `LLR-204`.
- **The blind derivation ran on two axes (slice 2).** Brief written and recorded
  before either agent ran; two agents (A worked backward from boundary outputs, B
  clustered obligations by shared signal) each partitioned all 75 SRs from a
  five-file input set. 97.2% pair agreement; both independently invented the same
  zero-SR finding/severity/exit-composition module no requirement states — a
  requirement gap, not a layout defect. The method finding (strip the harness
  context, not only the input set) is recorded for future runs.
- **The alignment survey completed (slices 3–5).** All eighteen dispersion
  families adjudicated against the live map read as the registry defines it — one
  consolidate, twelve keep-with-reason, the rest routed — with the shared-stage
  test (*calls, not lines*) dissolving most apparent dispersion.
- **Three consolidation WIs filed, none merged in place:** `WI-519` (the
  allow-file parse-honesty arm carried to three readers), `WI-520` (the credential
  class vocabulary — a PEM block refused at the hook but passing unredacted into a
  transcript), and `WI-521` (the decomposition-debt owner). The module-size
  ratchet's dead-owner pointer moved to `WI-521` at slice 5, so this close
  re-points nothing.
- **`OI-64` raised and discharged.** The zero-SR module both teams derived was
  routed to the owner as a requirement gap; ruled (b) and executed 2026-08-28.
- **Closed (slice 6, delegated unattended run), then reworked on REVIEW-A.**
  Slice 6 adjudicated the four `Drafted` slice-1 rows off the re-attestation
  surface (the 7 cited node ids ran, 7 passed) and blessed all four
  `Drafted → Approved` under the loop-held dial; the row moved to
  `docs/archive/work/complete/`. REVIEW-A (`003`) then returned CHANGES-REQUESTED:
  approving `TC-199`/`TC-200` as `SR-163` evidence falsely marked the full mapping
  obligation verified. The rework reverted the two TCs to `Drafted` (live and
  snapshot) and fixed a dead `OI-64` link — see
  `docs/log.d/2026-08-30-wi508-rework-review-a-changes-requested.md`. The census
  instrument's structural-duplication blind spot and the test-tree sensor gap are
  recorded, deliberately not filed.

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
[../../../log.d/2026-08-25-wi508-slice1-sr163-decomposition.md](../../log.md#2026-08-25--wi-508-slice-1-the-row-re-validated-the-lane-claimed-and--decomposed).

### SLICE 2 LANDED 2026-08-25 — the blind derivation ran, on two axes

**The brief was written and recorded BEFORE either agent ran**, so the question
cannot be re-written to fit the answer:
[../../../plans/2026-08-25-blind-minimal-map-brief.md](../../plans/2026-08-25-blind-minimal-map-brief.md).
Two agents derived the minimal module map from a **five-file input set** — the
purpose statement, the needs, the requirements, the depth-0 frame and the hat
roster — with the design tier, the component and interface registries, the
process masters and the source tree all held out, each for a stated reason. Two
axes, per the precedent that two teams on the SAME axis mostly agree and tell
you little: **A worked backwards from the declared boundary outputs**, **B
clustered obligations by shared signal and failure mode**.

Returns, verbatim and durable:
[a](../../plans/2026-08-25-blind-derivation-a-outputs.md) (24 modules) ·
[b](../../plans/2026-08-25-blind-derivation-b-obligations.md) (23 modules) ·
the record, the measured agreement and the disclosures:
[../../../plans/2026-08-25-blind-minimal-map-derivation.md](../../plans/2026-08-25-blind-minimal-map-derivation.md).

**Agreement, measured rather than eyeballed.** Both returned complete forward
assignments (75 SRs, no id twice), so the two maps are comparable as partitions:
**97.2%** pair agreement over 2,775 SR pairs, and a best one-to-one module
correspondence placing **63 of 75 (84%)** identically across 22 matched module
pairs. Twelve SRs are placed differently — those are the places the requirements
underdetermine the boundary, and they are listed in the record as INPUTS to the
adjudication rather than as findings against either map.

**The convergence the arithmetic cannot see, and the program's biggest result so
far.** Team A's `F5` and Team B's `M03` own **zero SRs each** and are the same
module: one home for the shape of a finding, its severity class, strict-mode
escalation, vacuity, and how findings compose into an exit code. Two opposite
axes independently invented it, and independently found that **no requirement
states it** while eleven-to-thirteen rows each restate a fragment — with
`SR-158`'s own acceptance conceding the hole in the corpus's own words. That is
a missing requirement, not a layout defect, and it must NOT be filed as module
work.

**`SR-163` split the two teams on exactly the seam slice 1 wrote.** A assigned it
to the spine-join checks, B to the package manifest — which is `LLR-204` against
`LLR-203`. Two agents that could not see the registry cut along the same line the
decomposition did.

**THE BLINDNESS WAS NOT TOTAL, and both teams disclosed it unprompted.** Neither
read one byte of this repository and both confined every read to the pack by
absolute path — but the harness injected this repository's own instruction file
(and for B a memory index) into their context BEFORE the brief, naming
directories and several script filenames. Both checked their module names against
that material, neither reproduced a filename as a module name, and both recorded
declining the obvious shortcut of using the boundary registry's script
enumeration as the module list. **The method finding: a future run must strip the
harness context, not only the input set.** It belongs to this program, not to
either team.

**STILL OWED BY THIS ROW.** Slices 3 and 4, unchanged: the alignment pass (the
only role permitted to read both sides, three buckets, every divergence
adjudicated with the legacy side's own rationale read FIRST), then filing the
consolidations that earn a row. The record's §6 carries two instructions for the
alignment pass — weight a live divergence by whether A and B agreed there, and
keep the requirement-level findings out of the module-work pile.

**Deferred to the owner: nothing new.** The derivation commissions no act; it is
one half of a diff. Record:
[../../../log.d/2026-08-25-wi508-slice2-blind-derivation.md](../../log.md#2026-08-25--wi-508-slice-2-the-blind-derivation-runs-on-two-axes-and-both-teams-disclose-the-same-breach).

### SLICES 3 AND 4 LANDED 2026-08-25 — the alignment, one WI filed, one question to the owner

Full record:
[../../../plans/2026-08-25-remap-alignment.md](../../plans/2026-08-25-remap-alignment.md).

**The live side was read the way the registry defines it** — an LLR row's
`module` cell joined through its `sr_refs` — so `SR` → `{modules}` is a join
that already exists and no judgement enters until the numbers are down. **75
SRs, 186 LLRs, 83 distinct modules named, and ZERO scripts named by no `Module`
cell.** Three-way pair agreement over the 71 SRs comparable on all three sides:
**A↔live 94.6%, B↔live 94.8%, A↔B 97.0%**.

**The fact that governs every disposition below: the live map is ~3.5× finer
than either derived map** (83 named modules against 24 and 23). A derived module
is a responsibility cluster; a live module is a file; several files realize one
cluster with no duplication provided they call a shared stage. So the question
is never "do these live in one file" but **"does each home re-implement the
behaviour, or do they all call one home for it?"** — *calls, not lines*, applied
as a test rather than quoted.

**THE TWELVE DISPOSITIONS: 10 keep-with-recorded-reason, 2 keep-with-the-reason-
absent, 0 consolidate, 0 requirement gap.** That is not a shrug — the twelve are
exactly the set where the two blind maps DISAGREED, so a live choice cannot be
convicted against a derived answer that does not exist. Two of them refute a
derived map's prediction by measurement: `SR-173` (B predicted the regeneration
order would be duplicated if the seam owned it — it is stated in exactly one
place, with its reason on `LLR-142`) and `SR-174` (B predicted non-reuse would
live away from the mark that proves it — `intake.next_wi_id` CALLS
`trace.read_watermark` and deliberately does not catch its refusal). Two more,
`SR-043` and `SR-024`, sit at the alternative the deriving team had already
named and rejected in its own honesty section. The two thin ones (`LLR-024`,
`LLR-033`) carry a defensible module and no `Rationale`; both rows are
`Approved`, so writing one is an amendment over an attestation and **the
owner's act, not a worker's** — banked, not fixed.

**THE CONSOLIDATION EVIDENCE IS WHERE A AND B AGREED** (47 dispersion pairs),
and the shared-stage test dissolved most of it:
- **Declaration reading — REFUTED.** 38 modules import the shared
  `kitlib.config` stage and only `config.py` defines a declared-line reader. The
  largest apparent dispersion is one home with 38 callers.
- **Measured-value-versus-baseline — REFUSED, and the refusal matters.** Merging
  `check_perf`'s gating engine with the duplication census would put the
  disposition behind one interface and leave an owner ruling (`D-7`, which tore
  down a gated duplication step) one refactor from being undone.
- **Derived-copy freshness — REFUTED.** Team A predicted the largest saving in
  its map; each `--check` is `render() != read()` reusing the generator's own
  renderer, so what a shared module absorbs is lines, not calls.
- **Declared exception lists — UPHELD, and the rationale SHAPED it.** Five files,
  five parsers, five recorded and genuinely different grammars — a blanket merge
  would flatten five arguments. What the reading surfaced is narrower and is a
  live defect the repo diagnosed in its own words: the parse-honesty arm
  (a malformed declaring line is REPORTED, not swallowed) exists on two readers,
  is argued in `read_provenance_allow`'s docstring, was adopted by
  `_parse_kernel_allow` by explicit reference, and is **missing from three**.

**FILED (slice 4): `WI-519`** — carry the parse-honesty arm to the three, each
keeping its own grammar and fail-safe direction. `medium` / `ordinary`, no
`needs`: `WI-448` and `WI-483` are both closed-archived, so there is no parent
lane to feed and the row does not wait on this program.

**DECLINED, each with its reason on the record:** the two refuted families above;
the 48 FUSION pairs (A and B agree apart, live fuses — clustered on `agent_loop`
14, `check_trajectory` 13, `agent_common` 10, `bootstrap` 5), which restate the
module-size ratchet's existing debt from the requirements side and are recorded
as corroboration rather than filed as a rival program; and the census
blind-spot finding below.

**A FINDING ABOUT THE INSTRUMENT, recorded and deliberately NOT filed.** The
standing duplication census reads **0 / 0 / 0** on this tree while this pass
confirmed a real repeated behaviour. No fault in the census: it hashes function
BODIES, so it measures textual duplication, and every family here is structural
— the same behaviour written differently. That is the blind derivation's
measurable value over the standing instrument. It is not a WI because the remedy
is not obvious and the census's own header routes changes through the owner on
`D-7`'s strength, where an over-eager duplication gate was torn down after 93%
of its findings proved to be accepted idioms.

**TO THE OWNER: `OI-64`** — the zero-SR module both teams derived is a
REQUIREMENT gap, not a layout defect. The finding/severity/strict-escalation/
vacuity/exit-composition contract is restated in 11–13 rows and stated by none,
with `SR-158` declaring itself unsatisfied for want of a declaration surface no
row owns. Four options, recommendation (c) then (a) — measure whether the
shipped checkers honour ONE contract before minting a row that might land red.
**No module work was filed against it**, and the row says so, so a later reader
cannot mistake it for a deferred refactor.

**STILL OWED AFTER SLICE 4** (all discharged by slice 5 below): the remaining
dispersion families; routing the 48 fusion pairs; the module-size ratchet's debt
pointer; M-06's four test monoliths. `OI-64` awaits a ruling.

### SLICE 5 LANDED 2026-08-25 — the survey is complete and the inherited debt has a live owner

Record: [../../../plans/2026-08-25-remap-alignment.md](../../plans/2026-08-25-remap-alignment.md)
§§8–10.

**ALL EIGHTEEN dispersion families now carry a disposition** (four in slice 3,
fourteen here) — **one consolidate, one partly upheld by a row already filed,
twelve keep.** Each KEEP states whether it rests on a mechanical shared-stage
test or on a read rationale, because conflating the two is how a survey starts
sounding more certain than it is. Three keeps rest on a read: the **launchers**
split is recorded in `SR-160`'s own text and the shared piece would have to
become a shell library the kit deliberately does not ship; the two **converters**
are one-shot tools whose migrations have already run, so a shared verifier would
have no future caller; the **scaffold/manifest** cluster's shared signal already
has exactly one home.

**ONE MORE ROW EARNED, and it is the one both derivations predicted from the
requirements alone.** `WI-520` — the credential class vocabulary. Two pattern
sets compiled independently, and driven against five samples **four disagree in
both directions**. The first inverts the protection: a PEM private-key block is
refused at the commit hook and passes **unredacted into a committed transcript**,
so the durable artifact is less protected than the ephemeral one — exactly the
hazard `SR-176` exists to prevent. The original rationale was read first and it
NARROWED the proposal: `redact_secrets` is documented as "deliberately imperfect
— unknown token shapes pass through", that decision stands, and the row asks for
one home for the class vocabulary rather than for exhaustive redaction.

**THE INHERITED DEBT NOW HAS AN OWNER THAT OUTLIVES THIS ROW.** `WI-521` is
filed and **the module-size ratchet's pointer moved to it** — six live pointers
across `tests/test_module_size_ratchet.py` and `tests/test_import_layers.py`;
the three surviving mentions of this row are the docstring's history of the
hand-off and are deliberately kept. It moved NOW rather than at this row's close
on two grounds recorded in the ratchet itself: a close-time re-point is a promise
where a filed row is a fact, and this row was never scoped to that axis anyway —
it is a CONSOLIDATION program while the ratchet measures SIZE, which is
decomposition. **This row's close now has nothing to re-point**, which is the
dead-owner defect made unreachable rather than deferred a third time.

**M-06's four test monoliths land on `WI-521`, explicitly unbound from the
ride-along rule.** That rule was `WI-483`'s own scope decision, it was honoured
across all seven of its slices and delivered nothing, and this program filed no
decomposition for it to ride — a rider with no vehicle. A successor row is free
to scope itself differently, which is why this is not an owner question. The
test-tree sensor gap rides with them, carried but NOT executed: extending a
census whose own axis is under an unruled owner question would double whatever
is wrong with it.

**The 48 fusion pairs are routed, not re-derived.** They are attached to `WI-521`
as the requirements-side evidence the size debt never had — which modules a
reader must hold too much in mind to read, reached independently of line counts.

### WHAT REMAINS ON THIS ROW IS OWNER-OWED, AND ONLY THAT

The program has no agent-executable work left. Precisely:

1. **`OI-64` awaits the owner's ruling** — whether the finding/severity/exit
   contract becomes a requirement. No module work may be filed against it until
   then, and the row says so itself.
2. **Four `Drafted` spine rows await blessing** (`LLR-203`/`TC-199`,
   `LLR-204`/`TC-200`), rendered in `docs/ratify/CURRENT.md`. No session may
   flip them.

Everything else this program produced is either landed or filed as its own
claimable row (`WI-519`, `WI-520`, `WI-521`). **The row stays ACTIVE and is
deliberately neither closed nor parked**: closing it would strand `OI-64`'s
ruling with no row to return to, and there is no pause file. When `OI-64` is
ruled and the four rows are blessed, the close is a bookkeeping act — and it
needs to re-point nothing.

### DELEGATED FOR THE UNATTENDED RUN (owner, 2026-08-30)

Item 1 is discharged: `OI-64` was ruled (b) and executed on 2026-08-28
(`docs/log.d/2026-08-28-owner-rulings-oi64-oi65.md`). Item 2 is not the
owner's act under the declared dial — `docs/process.toml` holds only the
`DevStg-Needs` rung human-held, so LLR/TC approval proceeds under ordinary
review: the lane that resumes this row approves the four `Drafted` rows through
the ordinary adjudication flow (the re-attestation brief is the surface, the
snapshot diff the record), closes the row as the bookkeeping act above, and
lists the flip in its fragment for the owner's later review. The owner is away
and has delegated this in session; the lane's branch ref was re-cut at trunk
HEAD on 2026-08-30 so the dispatcher resumes it as a parked lane.

Record:
[../../../log.d/2026-08-25-wi508-slice5-families-and-debt-routing.md](../../log.md#2026-08-25--wi-508-slice-5-the-dispersion-survey-completes-one-more-row-is-earned-and-the-inherited-debt-gets-an-owner-that-outlives-this-program).

### SLICE 6 LANDED 2026-08-30 — the four rows blessed, the row closed

The delegated close ran. `OI-64` was already discharged (ruled (b), executed
2026-08-28); the remaining owed act was the four `Drafted` rows this program
authored in slice 1. Under the declared dial only the `DevStg-Needs` rung is
human-held, so `LLR-203`/`LLR-204`/`TC-199`/`TC-200` are loop-held and a recorded
LLM verdict carries approval authority.

**Adjudicated then flipped.** Read the four rows off the re-attestation surface,
ran the 7 test node ids `TC-199`/`TC-200` cite (**7 passed**), and confirmed the
two LLRs name delivered, tested mechanisms while stating their undischarged halves
on-row. `Status` **`Drafted` → `Approved`** on all four — exactly four pairs, no
other cell moved — anchored by `intake.py snapshot` in the same act.

**Off-spine re-seed, disclosed.** The wholesale snapshot re-baselined the off-spine
registries to their already-merged state; the authority gate blocked on one
loop-held cell — `components.toml` `CMP-006` `Notes`, WI-520's merged
`secret_classes.py`/`LLR-205` kitlib listing — so the copy was named with
`--approves`. `LLR-205`/`TC-201` (WI-520's) were left `Drafted`, correctly still
owing.

**Closed.** Nothing agent-executable remained; the ratchet pointer already lives on
`WI-521` (slice 5), so the close re-points nothing. The spec moves to
`docs/work/complete/`. Record:
[../../../log.d/2026-08-30-wi508-slice6-spine-approval-and-close.md](../../log.md#2026-08-30--wi-508-slice-6-the-four-spine-rows-blessed-the-row-closed).
