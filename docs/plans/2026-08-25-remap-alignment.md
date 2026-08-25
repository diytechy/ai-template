# The alignment pass — derived map against live layout (WI-508 slice 3)

_The only role permitted to read both sides. Inputs: the two blind returns
([a](2026-08-25-blind-derivation-a-outputs.md),
[b](2026-08-25-blind-derivation-b-obligations.md)) and their
[record](2026-08-25-blind-minimal-map-derivation.md), against the live layout as
the registry itself defines it. **Every divergence is adjudicated; none is
silently merged or deleted, and no legacy home is called an accretion without
its own recorded rationale read first** (owner's standing directive)._

## 1. How the live side was read

An LLR row's `module` cell is the traced home of a design decision and its
`sr_refs` say which obligation it decomposes, so **SR → {modules} is a join the
registry already carries**. No judgement enters until the numbers are down.

| | value |
| --- | --- |
| SR rows | 75 |
| LLR rows | 186 |
| distinct modules named in `Module` cells | **83** |
| source tree | 67 top-level scripts + 9 package modules = **76** |
| scripts named by NO `Module` cell | **0** |
| components | 4 |

fig: derived="for each SR, the distinct module stems named by the `module` cells of the LLR rows whose `sr_refs` cite it, over docs/requirements/low-level-requirements.toml; the source-tree counts are the `.py` files under the declared `[paths] src` and its `kitlib/` package"

**The live map is roughly 3.5× finer than either derived map** (83 named modules
against 24 and 23). That is the single most important thing to hold before
reading anything below, because it makes most raw disagreement meaningless: a
derived module is a *responsibility cluster*, a live module is a *file*, and
several files can realize one cluster **without duplicating a thing** provided
they call a shared stage. The objective is *calls, not lines*. So the
adjudication question is never "do these live in one file" but:

> **does each live home re-implement the behaviour, or do they all call one
> home for it?**

**Four SRs have no live module, and three of them legitimately.** `SR-034`
(Analysis), `SR-036` (Inspection) and `SR-114` (Analysis) carry a verification
method that exempts them from LLR decomposition — the absence is the declared
method, not a hole, and it is the same package-wide-property class both blind
teams gave a module (A's `P3`, B's `M18`) and the boundary registry's own note
calls a "sixth capability". `SR-181` is the last orphan and is owned elsewhere.

## 2. Three-way agreement

Over the 71 SRs comparable on all three sides (2,485 pairs):

| comparison | pair agreement |
| --- | --- |
| A vs LIVE | **94.6%** |
| B vs LIVE | **94.8%** |
| A vs B | 97.0% |

fig: derived="pairwise co-membership over all 2485 unordered pairs of the 71 SRs present in all three partitions; the live partition assigns each SR the module its own LLR rows name most often"

Both derived maps sit closer to each other than either sits to the live layout,
by about the same margin — which is what an axis-diverse pair should do, and it
means neither map is measurably a better description of the live tree than the
other. **Neither is a verdict on the live tree**: at 3.5× the grain, a live
partition CANNOT score 100% against a coarser one.

The two directions of disagreement carry different information, and only one of
them is about duplication:

- **DISPERSION — 47 pairs.** A and B agree two SRs belong together; live splits
  them. *Candidate* duplication: one behaviour, many homes.
- **FUSION — 48 pairs.** A and B agree two SRs belong apart; live puts them in
  one module. Wide modules, and they cluster hard:

| live module | fused pairs |
| --- | --- |
| `agent_loop` | 14 |
| `check_trajectory` | 13 |
| `agent_common` | 10 |
| `bootstrap` | 5 |
| `trace`, `check_privacy` | 2 each |
| `check`, `check_doc_refs` | 1 each |

**The fusion set is not new work — it is the module-size ratchet's existing debt
seen from the requirements side**, and the four heads of it are the four largest
modules in the tree. It is recorded here as independent corroboration, not filed
as a rival program.

## 3. The twelve dispositions

These are the SRs where **A and B disagreed** — by the record's own reasoning,
the *weak-evidence* set: places where the requirements underdetermine the
boundary. The adjudication question for a weak-evidence divergence is therefore
not "is live wrong" (there is no derived answer to be wrong against) but
**"is live's choice defensible, and is its reason recorded where the next
reviser will find it?"**

| # | SR | A | B | LIVE | bucket |
| --- | --- | --- | --- | --- | --- |
| 1 | `SR-006` | step planner | harness bar | `check.py` + the three step scripts | KEEP — recorded |
| 2 | `SR-015` | measurement | spine rules | `trace.py` | KEEP — recorded |
| 3 | `SR-019` | enforcement floor | content guard | `hooks/pre-commit` (+ the shared probe) | KEEP — recorded |
| 4 | `SR-020` | enforcement floor | content guard | `hooks/pre-push` (+ the shared probe) | KEEP — recorded |
| 5 | `SR-024` | coverage & provenance | registry carrier | `gen_cases.py` | KEEP — **reason not on the row** |
| 6 | `SR-033` | measurement | state view | `gen_release_checklist.py` | KEEP — **reason not on the row** |
| 7 | `SR-043` | enforcement floor | run supervision | `subagent_gate.py` | KEEP — recorded |
| 8 | `SR-111` | history facts | package manifest | `bootstrap.py` | KEEP — recorded |
| 9 | `SR-113` | scaffold & re-sync | content guard | `dev-setup.template.sh` | KEEP — recorded |
| 10 | `SR-163` | spine rule checks | package manifest | `bootstrap.py` **and** `gen_arch_map.py` | KEEP — recorded |
| 11 | `SR-173` | lane & seam | derivation integrity | `trunk_step.py` | KEEP — recorded, prediction REFUTED |
| 12 | `SR-174` | lane & seam | registry carrier | `intake.py` (+ `integrate.py`) | KEEP — recorded, prediction REFUTED |

**Ten keep with a recorded reason, two keep with the reason absent from the row,
zero consolidations, zero requirement gaps.** That result is not a shrug and it
is worth stating plainly: the twelve are exactly the set where the two blind maps
could not agree, so a live choice cannot be convicted against a derived answer
that does not exist. The consolidation evidence is in §4, where A and B *did*
agree.

Where the disposition needed more than a reading, it got one:

- **`SR-019`/`SR-020` (#3, #4).** Both derived maps wanted ONE module; live has
  two hook files. But `LLR-021` — the interpreter probe — is cited by **both**
  SRs, so the shared stage the merge was arguing for already exists and is
  traced. The derived "one module" is realized as one declared shared symbol
  with two callers. Both teams independently flagged this probe as duplicated
  *by explicit ruling*; the registry shows the duplication they predicted is a
  single row.
- **`SR-043` (#7)** and **`SR-024` (#5).** In both cases the live home is the
  alternative the deriving team **named and rejected in its own honesty
  section** — B offered "a spawn-gate module of its own", A offered "a
  standalone case generator". Live took the option each team had already
  written down as reasonable. B additionally argued (its `S-dec 5`) against A's
  grouping on fail-safe direction: the spawn gate fails OPEN while every other
  guard fails closed, and fusing them would force the direction to become a
  caller-visible parameter. Live agrees with B.
- **`SR-173` (#11) — B's prediction refuted by measurement.** B assigned the
  regeneration order to the artifact graph rather than the seam, arguing that
  putting it in the seam "duplicates the graph". Measured: the dependency order
  is stated in exactly one place, `trunk_step.regen`, with `LLR-142`'s rationale
  recording its reason (*"derive_stage runs before the dashboard/status regens
  because docs/stage is their input, not their output"*). Nothing else declares
  an order. **There is no second copy to remove.**
- **`SR-174` (#12) — B's prediction refuted by reading the code.** B argued the
  id space belongs with the carrier or "non-reuse would live away from the mark
  that proves it". Measured: `intake.next_wi_id` **calls** `trace.read_watermark`
  and deliberately does not catch its refusal (*"a mint with no record of what
  has been allocated is the one operation that must not proceed on a guess"*).
  The mark's rules live with the carrier; only the allocation lives at the seam.
  One stage, one caller — the split B feared is not there.
- **`SR-006` (#1).** Live is A's reading (a planner that calls checks). The
  reason is not only recorded but recently re-argued: `check.steps` was
  re-measured at 649 lines / complexity 8 and deliberately LEFT, on four stated
  grounds. Nothing here reopens that.
- **`SR-163` (#10).** The two teams split on the inventory against the join —
  and the live registry, authored one day earlier by this program's own slice 1,
  carries **both**, as `LLR-203` (the inventory) and `LLR-204` (the join and its
  declared policy). Two agents that could not see the registry cut along the
  line the decomposition had just drawn.

### The two thin ones, and why they are banked rather than fixed

`LLR-024` (permutation expander) and `LLR-033` (release checklist generator)
each carry a defensible module choice and **no `rationale` cell**. That is the
`MAINTAINER` failure class exactly — *"a requirement whose reason lives only in
the session that wrote it, leaving the next reviser unable to tell load-bearing
from accident"* — and `MAINTAINER` is the lens the perspective backfill put on
this program's own parent row.

**They are NOT fixed here, and the reason is a rule, not reticence:** both rows
are `Approved`, and adding a `rationale` to an `Approved` row is an amendment
that overrides an attestation. That is the owner's act, not a worker's. Banked
as a finding.

## 4. The consolidation evidence — where A and B AGREED and live splits

Forty-seven pairs, and the test applied to each family is the one §1 states:
**is there a shared stage, or is the behaviour re-implemented?** Answering that
mechanically dissolved most of them.

### REFUTED — the shared stage already exists

- **Declaration reading** (`SR-007`, `SR-031`, `SR-137`, `SR-138`; A's `F1`,
  B's `M01`; live splits across `check`, `check_privacy`, `agent_common`,
  `bootstrap`). **38 modules import the shared `kitlib.config` stage, and
  `config.py` is the only module that defines a declared-line reader.** The
  derived maps' single declaration module is not missing — it is built, and the
  live dispersion is four obligations stated at four call sites that all call
  one home. This is the largest dispersion cluster and it is *calls, not lines*
  already satisfied.

fig: derived="count of modules under the declared src root importing kitlib.config, against the count of modules defining a declared-line reader function"

- **Measured-value-versus-baseline** (`SR-167`, `SR-177`, `SR-182`; A's `M1`,
  B's `M07`; live: `check_perf`, `agent_common`, `check_dupes_census`).
  **REFUSED, and the refusal is the interesting one.** The three are not one
  pipeline in the tree: `check_perf.evaluate` is a per-row budget / tolerance /
  gate / tier engine; `check_coverage.evaluate` is a four-line floor compare;
  `check_dupes_census` compares a triple against a stamped baseline and is
  **WARN-FIRST FOREVER by owner ruling** — its own header says the gated
  predecessor was torn down (D-7) and that teeth may not be added without
  bringing the case to the owner. Merging a gating engine with a never-gating
  census puts the disposition behind one interface, which is precisely the
  wide-interface-over-thin-implementation the deep-module rule forbids — and it
  would put an owner ruling one refactor away from being undone.

- **Derived-copy freshness** (`SR-022`, `SR-070`, `SR-112`; A's `D1`, B's `M08`;
  live: nine `--check` implementations). Team A predicted this would be "the
  single largest total-behaviour reduction in the map". **It is not, and the
  reason is visible only from the tree:** each `--check` is `render() != read()`
  reusing the generator's OWN renderer — three or four lines, not a stage. What
  a shared module would absorb is *lines*, and the one subtle part (line-ending
  normalisation, argued at length after two live defects) is already stated
  where it is needed. A derivation from requirements alone cannot see that the
  comparison is trivial once the renderer exists; this is the alignment pass
  doing its job in the direction that protects the live tree.

### UPHELD — a real repeated behaviour, and the original rationale SHAPED the proposal

**Declared exception lists.** Five declared exception files
(`docs/declared-absences`, `docs/if-tc-coverage-allow`,
`docs/kernel-modules-allow`, `docs/orphans-allow`, `docs/provenance-allow`) with
five separate parsers across four modules. Both blind maps put carve-out markers
and exception lists inside the ownerless finding-contract module (A's `F5`, B's
`M03`).

Reading the original rationale first is what stopped this from being filed as
"merge five parsers", which would have been **wrong**. Each parser differs in a
way its own docstring argues:

- `if-tc-coverage-allow` carries a `# seed-count:` migration baseline whose
  entries share one header reason;
- `kernel-modules-allow` requires a per-entry reason and says so **by contrast
  with** the seed-count file — "OI-48's reuse provision is a deliberate recorded
  act every time, never a bare-baseline default";
- `provenance-allow` requires an open-item id as the **first token** of the
  reason, a ruled required field;
- `declared-absences` accepts two separators and a `LIFECYCLE:` marker for paths
  whose presence is a legal state;
- `need-form-allow` keeps a token set and discards the reason.

Those are five recorded decisions and a blanket extraction would flatten them.

**What the reading DID surface is narrower, and it is a live defect the repo has
already diagnosed in writing.** Two of the five return `(entries, unparsed)` and
report a malformed *declaring* line as a finding. Three drop it silently. And
`provenance-allow`'s own docstring records why the silent version is wrong:

> "the other half of 'declares nothing' is that it also COUNTS as nothing, and
> the arms that reason about how many exceptions stand were reading that silence
> as an empty surface."

That correction was made for `provenance-allow`, adopted by `kernel-modules-allow`
("the same parse-honesty shape"), and **never carried to the other three**. It
is one behaviour, argued once, applied twice, missing three times.

→ Filed as **`WI-519`**. Not a merge: the parse-honesty ARM, extended to the
three files that lack it, each keeping its own grammar and its own fail-safe
direction.

## 5. A finding about the INSTRUMENT, and why it is not a WI

The standing duplication census reads **0 groups / 0 redundant copies / 0
redundant lines** on this tree — while this pass identified three families of
repeated behaviour and confirmed one as a live defect.

fig: cmd="python project-trajectory/scripts/check_dupes_census.py --root ." rev=64e9bf2a

There is no contradiction and no fault in the census: it hashes function
**bodies**, so it measures *textual* duplication. Every family here is
*structural* — the same behaviour written differently in three to five places —
which body-hashing cannot see by construction. **That is the blind derivation's
measurable value over the standing instrument**, and it is worth knowing before
anyone reads a zero census as "no duplication".

**Deliberately NOT filed as a WI.** The remedy is not obvious, structural
duplication detection is expensive and noisy, and the census's own header routes
changes to it through the owner on the strength of `D-7` — where an over-eager
duplication gate was torn down after 93% of its findings proved to be accepted
idioms. Proposing a mechanism here would be design-by-speculation on a surface
the owner has already burned once. Recorded, not built.

## 6. The requirement gap

The one bucket-3 finding of this pass is **not** among the twelve and is not a
layout question at all: both teams derived a module owning **zero requirements**
— the finding / severity / strict-escalation / vacuity / exit-composition
contract that 11 to 13 rows each restate and no row states.

Filed for the owner as **`OI-64`**, because it asks for a requirement to exist
(or for a ruling that it should not), which is not a worker's call. It is
explicitly NOT filed as a consolidation WI: building a shared finding module
before the obligation is stated would install a mechanism ahead of its
requirement, which is the inversion this kit exists to prevent.

## 7. What the first pass did not do — and what §§8–10 then did

The first pass (2026-08-25, slices 3–4) left three items open, and all three are
now discharged below: the remaining dispersion families are adjudicated (§8), the
fusion set is routed to a filed owner (§9), and M-06's monoliths have a landing
(§9). What still stands from that list: this pass **moved no module and no spine
cell**. It did move six debt pointers in two test files, which is §9's whole
subject and is recorded there.

---

## 8. The remaining dispersion families, adjudicated

**Eighteen dispersion families exist**, grouped by the (A-module, B-module) pair
both derivations agreed on. Four were adjudicated in §4; the fourteen below
complete the set.

fig: derived="pairs (x,y) where A and B each co-locate x and y while the live SR->module join separates them, grouped by the (A,B) module pair; the live join reads LLR `module` cells through `sr_refs`"

The test is §1's, unchanged: **is there a shared stage, or is the behaviour
re-implemented?** Where the answer came from an import edge or a missing second
implementation, the disposition says so — a KEEP grounded mechanically is not
the same claim as a KEEP grounded in a read rationale, and conflating them is
how a survey starts sounding more certain than it is.

| family (A/B) | SRs | live modules | disposition |
| --- | --- | --- | --- |
| `P1`/`M15` scaffold + manifest | 009, 010, 011, 032, 166 | `bootstrap`, `onboard.template.sh`, `kitlib/__init__` | KEEP — shared signal has one home |
| `U1`/`M20` run lifecycle | 026, 027, 028, 171, 172 | `agent_common`, `agent_loop` | KEEP — `agent_loop` imports `agent_common` |
| **`F4`/`M17` sensitive content** | **017, 018, 176** | **`check_privacy`, `agent_common`** | **CONSOLIDATE → `WI-520`** |
| `U3`/`M21` dispatch + brief | 040, 146, 175 | `adjudicate_brief`, `agent_loop`, `plan_briefs` | KEEP — mechanical |
| `G2`/`M12` presentation vocabulary | 052, 053, 054 | `traj_render`, `gen_trajectory` | KEEP — shared stage exists |
| `A2`/`M06` acceptance record | 140, 178, 179 | `baseline_snapshot`, `check_trajectory` | KEEP — mechanical |
| `U5`/`M23` lane + seam | 144, 156, 170 | `handback`, `integrate`, `trunk_step` | KEEP — recorded, recently re-argued |
| `V5`/`M11` authored prose | 149, 150, 158 | `check_vocab`, `check_need_form`, `check_doc_refs` | PARTLY UPHELD — the carve-out arm is `WI-519`'s |
| `V3`/`M04` spine rules | 157, 164, 180 | `trace`, `check_trajectory`, `check_doc_refs` | KEEP — recorded, recently re-argued |
| `P2`/`M16` launchers | 046, 160 | `run_menu`, `agent-resume.sh` | KEEP — the split is recorded and argued |
| `A1`/`M05` stage + approval | 049, 139 | `spine_rules`, `agent_common` | KEEP — shared stage exists |
| `F2`/`M02` converters | 129, 147 | `wi_convert`, `migrate_carrier` | KEEP — both migrations are spent |
| `V2`/`M14` hosted bar | 151, 152 | `check.yml`, `kitlib/evidence.py` | KEEP — recorded, built deliberately |
| `V4`/`M09` frame checks | 159, 162 | `check_trajectory`, `trace` | KEEP — `trace` imports `check_trajectory` |

**Where the KEEP is grounded in a read rather than an import edge:**

- **Launchers** (`P2`/`M16`). Both maps wanted one entry-point module and quoted
  `SR-046`'s "the platform launchers delegate to the one selector rather than
  carrying commands of their own". But `SR-160`'s own text records the split as
  deliberate — it "spans two audiences … and parts along that line" — and the
  piece that IS shared, the interpreter probe, would have to become a **shell
  library** to be shared between a hook and a launcher. The kit ships no such
  thing, deliberately: a hook must work standing on nothing but the repository.
  The recorded reason still holds.
- **Converters** (`F2`/`M02`). Both maps merged them to remove "a second
  cell-exact round-trip verifier". Both verifiers exist — and **both migrations
  have already run**: the spine is TOML and the work registry is spec files.
  These are one-shot tools retained as the proof that the conversion was
  lossless, which is their stated purpose ("the converter is proven by a
  round-trip before the CSV is demoted"). A shared verifier would be built for
  no future caller.
- **Scaffold + manifest** (`P1`/`M15`). The shared signal both maps clustered on
  is the inventory, and the inventory has exactly one home (`bootstrap.MAPPING`).
  The other two live modules are different artifact kinds — a shipped shell
  template and a package `__init__` — not second manifest walkers.

### The one that earned a row, and it is the one both teams predicted

**`F4`/`M17` — the credential class vocabulary.** Both derivations merged the
scanner and the redactor and both cited `SR-176`'s own rationale as evidence the
duplicated class list had *already* diverged. Measured, it is worse than the
requirement records. Two pattern sets are compiled independently —
`check_privacy.KEY_RE` + `TOKEN_RES` (the hook floor) and
`agent_common._SECRET_RES` (`redact_secrets`, applied before a transcript is
committed) — and driven against five samples, **four disagree, in both
directions**:

| sample | hook scanner | transcript redactor |
| --- | --- | --- |
| PEM private key block | catch | **MISS** |
| `Bearer <30 chars>` | **MISS** | catch |
| `ghp_` + 36 chars | catch | catch |
| `ghp_` + 24 chars | **MISS** | catch |
| `sk-` + 22 chars | **MISS** | catch |

fig: cmd="load check_privacy and agent_common by path, then evaluate KEY_RE + TOKEN_RES against _SECRET_RES over the five samples in the table" rev=754870db

**The first row inverts the protection**: a PEM private-key block is refused at
the commit hook and passes **unredacted into a committed transcript**, so the
durable artifact is less protected than the ephemeral one — the exact hazard
`SR-176` exists to prevent, with a different subject.

**The original rationale was read first and it narrowed the proposal.**
`redact_secrets` is documented as "deliberately imperfect — unknown token shapes
pass through", and that decision STANDS: `WI-520` does not make redaction
exhaustive. What the docstring does not license is the measured gap — a PEM key
is not an unknown shape, it is a compiled pattern in a sibling module. The row
asks for one home for the class vocabulary and a per-class decision on each
side, not for one behaviour.

---

## 9. The fusion set and M-06 — routed to a filed owner, not left to a promise

The 48 fusion pairs (§2) are the module-size ratchet's existing debt seen from
the requirements side. They needed an owner that outlives this program, and so
did M-06's four test monoliths, which had been riding a vehicle that never
arrived.

**`WI-521` is filed and the ratchet's pointer MOVED TO IT** — six live pointers
across `tests/test_module_size_ratchet.py` (the module docstring, the
decomposition instruction, the sensor paragraph, the `BASELINE` header comment,
the growth failure message) and `tests/test_import_layers.py` (the deferred-import
window, the cycle ratchet). The three surviving `WI-508` mentions are the
docstring's history of the hand-off and are deliberately kept.

**Why it moved now rather than at `WI-508`'s close**, recorded in the ratchet's
own docstring because that is where its rule lives:

1. **A close-time re-point is a promise; a filed row is a fact.** It has been
   honoured exactly once, deliberately, with the defect named — and relying on
   it again makes the sensor's honesty depend on a session remembering.
2. **`WI-508` was never scoped to this axis, and the ratchet says the same
   about its predecessor in the same words.** `WI-508` is a CONSOLIDATION
   program; this ratchet measures SIZE, which is decomposition. It held the
   pointer for being the live architectural program, not for matching the axis.

**`WI-508`'s eventual close now has nothing to re-point.** That is the dead-owner
defect made unreachable rather than deferred a third time.

**M-06 lands on `WI-521`, explicitly unbound from the ride-along rule.**
`WI-483`'s item 4 held that a test split rides along with a subsystem
decomposition and that a standalone split was out of scope — honoured across all
seven of its slices, and it delivered nothing, because no slice needed one.
`WI-508` then filed no decomposition at all. A rule that has failed to deliver
across two programs is a rider with no vehicle, so `WI-521` states that a
standalone split is in scope for it. That rule was `WI-483`'s own scope decision,
not a standing ruling, which is what makes this a successor row's call rather
than the owner's.

**The sensor gap is carried, NOT executed.** No armed sensor watches the test
tree, which is why three of the four monoliths grew 5–36% unnoticed. Extending
the census is deliberately not proposed: that file banks an unruled owner
question about whether the line-count axis survives at all, and extending a
disputed axis to a second tree doubles whatever is wrong with it.

---

## 10. What remains, after this pass

- **Not adjudicated, and named as such:** nothing in the dispersion set. All 18
  families now carry a disposition.
- **Owner-owed:** `OI-64`'s ruling, and the four `Drafted` spine rows on the
  approval surface.
- **Filed and executable by a worker:** `WI-519` (the carve-out parse-honesty
  arm), `WI-520` (the credential class vocabulary), `WI-521` (the standing
  decomposition debt).
- **Still true and unchanged:** this pass moved no module and no spine cell.
