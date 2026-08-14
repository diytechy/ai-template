# The DevStg-Boundary draft — the kit's depth-0 frame, for sitting 2

**Status: DRAFT FOR RULING — with TWO parts already ruled.** §1a carries the
owner's 2026-08-13 ruling on *what defines a boundary* (actor **and** crossing
interface); §1b carries the ruling that *the operational context is part of the
boundary*. Everything else here is proposed, and §4 lists what is still owed —
including the registry shape §1b recommends but does not decide.
Written after sitting 1 ratified
SN-037…SN-040 and ruled decision **2.7(a)** — *an SR may name an artifact only
where that artifact is a **declared boundary crossing***
([sitting-pack §2.7](2026-08-13-sitting-pack.md)) — which queued
[`WI-451`](../../work/active/wi451-sr-retier-campaign/WI-451-sr-boundary-conformance-pass.md). That pass
re-states ~50 SRs *against the boundary*, so the boundary has to exist first.
This document proposes it. Every figure names the command that produced it.

---

## 0. Provenance — where DevStg-Boundary came from, and where boundaries live

**The owner's question:** *"I don't recall how that even appeared, do those
appear in interfaces.toml or was a new registry proposed?"*

**Short answer: `interfaces.toml` is the one home. No new registry was ever
proposed — not in any plan, WI spec, open item or log entry.** (Searched:
`grep -rn "boundary registry\|boundaries.toml\|boundary.toml\|actors.toml\|new
registry" docs/plans docs/requirements docs/log.md docs/work project-trajectory`
— the only hits are two dual-plan assumptions about a WI-registry *column* and
WI-399's scope guard, none about boundaries.) The rung's own predicate reads the
IF registry and nothing else (`derive_gate.boundary_incomplete`, line 574).

*That is the answer to "was one proposed?" as a matter of history — nothing ever
was. It is **not** a claim that none is needed: §1b, written after the
2026-08-13 context ruling, proposes one for external **entities** (never for a
second set of interfaces) and §4 item 5 leaves it open.*

**How the rung appeared, in three steps:**

1. **2026-08-11** — [`2026-08-11-stage-gate-semantics.md`](2026-08-11-stage-gate-semantics.md)
   argued *a gate is a moment, the repo uses it as a state*, and shipped a
   six-rung ladder. **No boundary rung in it** (its header now records it as
   superseded in part). The companion
   [`status-ladder-migration.md`](2026-08-11-status-ladder-migration.md) is D-9's
   `Status` rewrite and is unrelated — it mentions boundaries nowhere.
2. **2026-08-12/13 — OI-14 part A-prime is what minted the rung.** OI-14 asked
   *"whether `DevBar-Reqs` must require a declared system boundary first"*
   (`open-items.toml#OI-14.one_line`), because *"SRs are blessed today against a
   frame nobody declared"* (`OI-14.recommendation`). Ruled **(A6): require the
   declared system boundary, WITH AN APPLIES-WHEN AND WARN-FIRST**
   (`docs/log.md` Decisions, 2026-08-13 batch ruling).
3. **2026-08-13 — OI-21 gave it a rung.** The eight-rung `DevStg-<Label>` ladder
   inserted `DevStg-Boundary` at position 1, between Needs and Reqs; OI-14's
   own row records the consequence: *"naming 'system boundary interfaces' as its
   own stage makes the ORDERING obligation ladder-borne for every project, so
   A5/A6/A7 now decides only the ENFORCEMENT half."* Shipped in **WI-445**
   (`docs/log.md` §2026-08-13c, "the gate vocabulary retires").

**What the rung requires.** `PROCESS.md` §4 line 396: *"the system's frame: what
is outside, what crosses, each crossing typed. HAPPENS ONCE."* The boundary is
the one level that does **not** recurse — every boundary below it is *produced
by* a partition (PROCESS.md §4, "The boundary happens once"). The bar
(`gate-advance/SKILL.md` L128-131): *"If the repo declares an `interfaces`
registry, the boundary inventory is settled — every declared crossing typed,
none left at `Stability = Experimental` — or `DevStg-Boundary` honestly holds the
ladder down."*

**What "typed" does NOT mean today — a correction carried into this draft.**
The rung's enforced predicate, `derive_gate.boundary_incomplete` (L569), reads
**`Stability` only**. It never looks at the `signal` field. So the mechanized
half of "each crossing typed" is today just *"no declared crossing is still
`Experimental`"* — the predicate's own docstring says as much (*"the declared
inventory is settled, or it is not"*). Any reading that treats
`discrete`/`variable` as the rung's typing axis is a claim about intent, not
about what runs. §1a rules what the axis actually is.

**The honest current state — and it is weaker than it sounds.**
`boundary_incomplete`'s own docstring (`derive_gate.py` L586-590) says the quiet
part: *"NOTE WHAT THIS DOES NOT CLAIM. It does not verify that every external
crossing is covered — nothing in the schema types a crossing as external today,
and inventing that field is OI-14 part B's business, not this rung's."* Part B
shipped (WI-443) **without** adding that field: `interfaces.toml`'s fields are
`direction · this_project · counterpart · contract · signal · signal_note ·
sr_refs · version · stability · component · notes` — there is no `external`
flag. So the rung today checks only that the *declared* rows are settled, never
that the frame is complete.

**The five rows holding the rung down** (`Stability = Experimental`, 5 of 113;
`python3 -c` over `tomllib.load(interfaces.toml)['interface']`):

| IF | Gist | Why still Experimental |
|---|---|---|
| **IF-057** | `plan_coverage` reads `interfaces.toml` + SR ids to resolve a dual-plan's per-WI cites | its consumer seam (`agent_loop`) was never declared — "WI-197's to declare" |
| **IF-103** | `migrate_carrier.py` — the one-shot CSV→TOML spine converter | *"Stability is PROVISIONAL on purpose: migration scaffolding with a defined end"* |
| **IF-118** | `gen_open_items` reads the decision registry through `spine_carrier` | minted by the batch-2 carrier sweep, never re-reviewed |
| **IF-119** | `agent_route` reads the model registry through `spine_carrier` | same sweep |
| **IF-120** | `trunk_step` asks the carrier which carrier of a registry is live | same sweep; was `Provisional` until WI-443 |

Note what they are: **four of the five are internal carrier seams, not external
crossings.** The rung that is supposed to certify *the system's frame* is
currently held down by module-to-module plumbing. That is a finding for §4.

**Where the 34-crossing inventory actually lives — and it is not a registry.**
[`2026-08-13-part-a-data-pack.md` §1](2026-08-13-part-a-data-pack.md) (WI-441,
measured at rev `81a142c2`), whose own header says **"analysis input, not a
decision."** §1a lists 15 crossings the registry carries (X-01…X-15), §1b lists
19 it misses (M-01…M-19), §1c declares the set **complete to the author's best
reading** with six stated uncertainties. WI-441's deliverable records the same:
*"the 34-crossing boundary inventory … (19 crossings have no IF row — Part B's
intake)."*

**Reconciliation with the live registry, honestly.** The 15 X-rows all still
exist and still name an external counterpart today — though **four of them do not
survive §1a's actor rule** (X-08/X-12 read internal, X-14/X-15 are mislabelled),
so the honest count of declared *frame* crossings is 11. A filter for
non-repo-path counterparts returns **16** rows — the extra is `IF-019`
(`skills/INDEX.csv`), an internal generated file, not an actor. Of the 19
M-rows, **13 have no IF row at all** (M-01, M-02, M-04, M-05, M-07, M-09, M-11,
M-12, M-13, M-14, M-15, M-17, M-19) and **6 have a partial/adjacent row that
names the file rather than the actor** (M-03/IF-048, M-06/IF-014, M-08/IF-074,
M-10/IF-037, M-16/IF-032, M-18/IF-070). **`docs/architecture.md` carries no
boundary section at all** (`grep -n "boundary\|external\|actor"` returns only
three generated function-summary rows) — which is a live gap against SN-040's
acceptance: *"the record is kept with the architecture, not in session prose."*

---

## 1. The depth-0 frame — what is OUTSIDE, what CROSSES

**The system** = the kit: `project-trajectory/` scripts + hooks + templates,
verified by `tests/`, self-applied to this repo (`docs/architecture.md`, "Shape
of the product").

**How to read the table.** **One row per crossing** — each row is one directed
seam and becomes exactly one `IF-###`, which is the shape `PROCESS.md` §8
already rules ("record each directed seam once"). **Dir** is stated from the
kit's point of view: **IN** = the crossing enters the system (the kit consumes),
**OUT** = it leaves (the kit provides), **IN/OUT** = a genuine two-way surface
that sitting 2 may choose to split into two rows. **IF today** names the live row
if one exists. The **`#`** ids are the data pack's own (`X-` = the registry
already carries it, `M-` = the pack found it missing) so every row here is
traceable back to the WI-441 inventory; **`N-`** marks a crossing this draft adds
*beyond* the pack's 34, which the completeness declaration has to absorb.

Signal typing (`discrete`/`variable`) is deliberately **not** a column here — per
§1a it is a property of the IF row, not of the frame.

| # | Party | Dir | What crosses | IF today | State |
|---|---|---|---|---|---|
| M-01 | **E1** Adopting team / contributor | IN | a contributor runs `dev-setup.{sh,cmd,command}`; toolchain probe result | — | **MISSING** |
| M-03 | **E1** | OUT | the runnable capability list a contributor reads | IF-048 | partial — menu side only |
| M-19 | **E1** | OUT | every script's human-readable report to the terminal/console | — | **MISSING** |
| X-12 | **E1** | OUT | `run_menu.py` → the `run.*` launcher scripts | IF-048 | reads **internal** — counterpart is the kit's own launchers, not the person |
| M-02 | **E2** Human owner | IN | one-command autonomous-run trigger via root `agent-resume.*` | — | **MISSING** |
| N-01 | **E2** | IN | `docs/process.toml` — the policy-dial surface the owner hand-edits | — | **MISSING, and NEW** (not among the pack's 34) |
| M-11 | **E2** | IN | rulings, attestations and `Status` flips into the registries | — | **MISSING** |
| M-10 | **E2** | IN/OUT | `docs/status.md` — the resume-from-text surface the owner also edits | IF-037 | partial — names the *file*, not the owner |
| M-09 | **E2** | OUT | `PROJECT_STATE.html` trajectory dashboard | — | **MISSING** as an owner surface |
| M-08 | **E2** | OUT | `open-items.html` decision-brief / signing surface | IF-074 | partial — names the *file*, not the reader |
| M-12 | **E3** Agent CLI (direct session) — OI-28 seed 1 | IN | instructions / prompt into the repo from a direct session | — | **MISSING** |
| M-13 | **E3** | OUT | artifact edits, admitted only through the git hook floor (`pre-commit`, `pre-push`, `commit-msg`) | — | **MISSING** |
| X-07 | **E3** | OUT | `subagent_gate.py` PreToolUse spawn allow/deny | IF-020 | declared |
| X-11 | **E3** | IN | `agent_session.py` launches the CLI and reads its result | IF-041 | declared |
| M-15 | **E4** Model provider API | IN | rate limit, auth expiry, retired model | — | **MISSING** — and its SN owner (SN-020) was dissolved at OI-18, so **no live need owns it**; SR-026's backoff clause is its only home |
| M-14 | **E5** External reviewer CLI (codex `sol`/`terra`) | IN/OUT | hostile-review brief out, findings in | — | **MISSING** — IF-045 declares model *families*, not the provider |
| X-09 | **E6** git — the mutation floor | IN | `check_privacy.py` reads staged/outgoing content | IF-032 | declared |
| M-16 | **E6** | IN/OUT | commits, merges, pushes, advisory locks, and the hook floor as enforcement | IF-032 | partial — read side only (§1c asks whether this is one crossing or three) |
| M-04 | **E7** GitHub / hosted CI | IN | push · PR · schedule trigger; the OS × Python matrix | — | **MISSING** |
| M-05 | **E7** | OUT | job verdict + step log | — | **MISSING** |
| M-17 | **E8** OS · filesystem · Python ≥3.11 | IN | path semantics, encoding, kernel advisory lock, interpreter presence | — | **MISSING** (SN-011 + SR-034/035/114 depend on it; the pack also cited SN-013, dissolved at OI-18) |
| M-18 | **E9** Test / coverage toolchain | IN | pytest results feeding the tier floors | IF-070 | partial — coverage side only |
| X-13 | **E9** | IN | `check_coverage.py` reads `coverage.json` | IF-070 | declared, but the counterpart is a **file**, not the toolchain |
| X-01 | **E10** Downstream adopted repo | OUT | `check.py` gate/tier harness verdict | IF-013 | declared |
| X-02 | **E10** | OUT | `bootstrap.py` scaffold write + re-sync diff | IF-014 | declared |
| X-03 | **E10** | OUT | `agent_loop.py` unattended coordinator run | IF-015 | declared |
| X-04 | **E10** | OUT | `check_vendored.py` drift verdict | IF-016 | declared |
| X-05 | **E10** | OUT | `gen_cases.py` permutation expansion | IF-017 | declared |
| X-06 | **E10** | OUT | `gen_release_checklist.py` checklist | IF-018 | declared |
| X-10 | **E10** | IN | `check_vendored.py` reads the vendored upstream source | IF-036 | declared |
| M-06 | **E10** | OUT | the MAPPING: templates → the adopting repo's `docs/` tree, + kit-version stamp | IF-014 | partial — coarse; names the adopter, not the tree |
| X-14 | **E10** | OUT | `integrate.py` serialized merge queue | IF-080 | **MISLABELLED** — claims `downstream adopter`, is an internal station seam |
| X-15 | **E10** | OUT | `trunk_step.py` trunk step | IF-081 | **MISLABELLED** — same |
| M-07 | **E11** The shipped template set as product — OI-28 seed 2 | OUT | `*.template.*` + `registries/*` as a traced product artifact class | — | **MISSING** — one SR anchor owed, `test_dogfood_sync` as its verification |
| N-02 | **E12** The kit's own ENABLING system (§1b) — the development environment: human + LLM session + agent CLI, *external, tightly coupled, shares personnel with E2/E3* | IN | template and registry CONTENT authored into the kit outside the mechanization — the inbound half of M-07 | — | **MISSING, and NEW** (OI-28 noted the minting; no crossing was ever declared for it) |
| X-08 | *(unassigned)* | IN | `check_docs.py` reads the doc tree | IF-030 | reads **internal** — counterpart `docs` is an in-repo path, not an actor |

**The tally, and it reconciles to the pack.** 36 rows = the pack's 34
(X-01…X-15 + M-01…M-19) plus **N-01** and **N-02**. Of the pack's 34: **11
declared** cleanly, **6 partial** (a row exists but names a file or module where
the actor belongs), **13 MISSING**, **2 MISLABELLED** (X-14/X-15), and **2 that
read internal** under §1a's actor rule (X-08, X-12). The 13 + 6 split is exactly
the §0 reconciliation, from the other direction. Both **new** rows have no IF row
either, so the honest missing count is **15**.

**Three things the tally says that the party-level view hid.** First, **`N-01` is
a real gap in the completeness declaration**: `docs/process.toml` is the owner's
single policy-dial home — SN-028's whole subject — and the WI-441 inventory has
no crossing for it, so §1c's "complete to my best reading" is now known to be
complete-minus-two. Second, **four of the 15 crossings the registry was credited
with do not survive contact with the actor rule** (X-08, X-12 read internal;
X-14, X-15 are mislabelled), so the honest count of declared *frame* crossings is
**11, not 15**. Third, **`N-02`** — the inbound half of the template artifact
class, which §1b derives.

### 1a. What DEFINES a boundary — ruled by the owner, 2026-08-13

**The ruling.** A boundary is defined by **the actor AND the crossing
interface** — not by the actor alone. The owner's reasoning, recorded because it
is the load-bearing part: naming the interface *technically starts
implementation*, and that is accepted deliberately, because **it is the only way
system requirements end up constrained to defined interfaces**. So the boundary
declaration **encodes the first design decision: how the external parties
interact with the system.** Everything the SR tier is allowed to say about a
port descends from that decision.

This is what makes decision 2.7(a) executable rather than aspirational. "An SR
may name an artifact only where it is a declared boundary crossing" has no
referent unless the crossing names an interface; with the interface declared, an
SR naming `check.py` is *citing the frame*, and an SR naming `trace.py` is
naming something the frame never admitted.

**What this rules OUT as the boundary's typing axis: `signal`.** The
`discrete`/`variable` vocabulary (OI-14 part B, `PROCESS.md` §8) stays a real and
useful property **of an IF row** — it is what makes SN-037's *"incompatible
signal types are mechanical findings"* checkable between two modules. It is not
what types the *frame*, for a measured reason: it is near-constant there. Over
the 113 live rows, **106 are `variable` and 7 are `discrete`**; on a crude
outward cut (a counterpart that is not an in-repo path) it is **15 `variable` to
2 `discrete`**, and **25 rows carry a `signal_note`** — the marker the WI-443
conversion left where it could not type the crossing cleanly. The cause is the
absorbing rule visible on IF-020: any unbounded part makes the whole crossing
`variable`, and almost every boundary crossing carries prose, a diff or file
bytes somewhere inside it. A property that is 94 % one value over the set it is
applied to is not typing that set.

<!-- fig: cmd="python3 - … tomllib.load(interfaces.toml)['interface']; Counter over
r['signal'], split on outward = counterpart NOT startswith
('scripts/','docs/','project-trajectory/scripts','coverage'); signal_note = truthy
count", rev=768b6d3a -->

**The typing the frame needs instead**, and the honest state of each half: the
**actor** (a real external party, never a file path — this is the IF-080/081
mislabel and the six "names the file rather than the actor" partials below), the
**direction** (present), the **contract** (present), and the **class of the
crossing** — a CLI invocation, a process exit status, a file artifact, a VCS
event, a network call, a human-read surface. That last axis is the one that
genuinely discriminates at a frame and **has no field today**. It is adjacent to
the `external` flag `boundary_incomplete` already admits nobody built, which is
what would let the rung check frame *completeness* rather than only settledness.
Whether to mint one, both, or neither is §4's to rule.

**The nuance the owner flagged, recorded for the kit's downstream reach.** This
kit ships stack-agnostic and already carries a physical tier (`PROCESS.md` §8's
purchased/external parts, `PART-###` + `procurement.csv`; `MULTI_REPO.md` §3.3
owner-of-record). For a **mechanical** system the crossings are not signals at
all — they are mounts and mating features, power rails, thermal paths, fluid and
pneumatic connections, forces and torques, plus regulatory and environmental
exposure. The actor-plus-interface rule holds there and arguably holds *harder*
(choosing a connector, a bolt pattern or a voltage rail is unmistakably a design
decision that constrains everything inside). What does **not** travel is
`discrete`/`variable`, which is a software-signal vocabulary: making it the
frame's typing axis would ship a software-only assumption into a mechanical
adopter's boundary. A class axis (medium/quantity: mechanical · electrical ·
thermal · fluid · data) would travel. Not a decision for this repo's own frame —
recorded so the kit-level version of this rule is not written software-first by
default.

**The four rows the actor rule re-reads** are flagged in the table's State column
and are sitting 2's to confirm: `IF-080`/`IF-081` (X-14/X-15) declare
`downstream adopter` but are the unattended station's *internal* serialization
seams, and X-08/X-12 name an in-repo path (`docs`, the kit's own `run.*`
scripts) where an actor belongs. All four were counted toward the registry's 15
"external" rows. **This is the case for making the actor a declared thing rather
than free text:** none of the four is *wrong* in any way a check can currently
see, because `counterpart` is prose — which is the §4 item 3 decision.

**The data pack's six stated uncertainties (§1c) stand and are the ruler's, not
mine:** is `downstream adopter` one actor or three (team / tree / their CI)? is
git one crossing or three (read / write / hooks)? is the terminal an actor at
all? is the skills fan-out into a third-party agent's config namespace its own
crossing? is a `docs/knowledge/` pack an input? and `MULTI_REPO.md`'s cross-repo
rung was deliberately not audited.

### 1b. The operational CONTEXT is part of the boundary — ruled by the owner, 2026-08-13

**The ruling.** Modelling the operational context is **part of defining the
boundary**, not a later exercise. The owner's reasoning: it is one step in
determining **how this system lives in its surroundings**, and that question *"can
sometimes only be well answered while knowing surrounding relationships."* So
`DevStg-Boundary` declares the parties around the system and the relationships
among them, not only the crossings into and out of it.

**Already ruled — do not re-litigate this half (OI-28, 2026-08-13).** The batch
ruling records the same observation in the owner's own earlier words, and ruled
*(a) SEED AT THE BOUNDARY, executed with OI-14's rung-1 work*: the
`*.template.*` files *"are minted primarily through LLM sessions, but they are
OUTCOMES of this system — the reusable baseline other repositories copy is the
product — so they need to tie back to the requirements like any other product
artifact"*, and *"a CLI session is itself an INTERFACE into the system — an LLM
agent outside the mechanization can contribute to and modify artifacts — and that
is true of basically every downstream adopter too."* M-07, M-12 and M-13 in §1
are those seeds; **WI-442** owns landing them.

**The cut is the DESIGN SCOPE, and everything else is external — including the
enabling system** (owner correction, 2026-08-13). The top-level division is not
*actor versus other*; it is **inside the design scope versus outside it**. An
enabling system — the development environment that produces the kit — is *not
part of the system*, even though it is tightly coupled to it. It may not be an
**actor** in the interaction sense at all; it is simply another external entity,
of a different kind. So the taxonomy has two levels: **external** is the
boundary cut, and *operational actor · enabling system · interoperating system*
are kinds of external entity beneath it.

Standard systems engineering carries this as the *system of interest* versus its
**enabling systems** — systems that support it across its lifecycle without being
part of it (the development environment, the build and test system, the training
system). The kit has no such vocabulary today (searched: `PROCESS.md`,
`PROCESS_OPTIONS.md`). Adopting it dissolves what otherwise reads as a paradox:
**`dev-setup` is an OUT contract consumed by two different external entities** —
an adopting contributor *operationally*, and this repo's own development
environment *through self-adoption*. One contract, two crossings, distinguished
by what stands on the far side.

**So the class sits on the ENTITY, and the overlap is a RELATIONSHIP.** An
earlier draft of this section put the class on the *crossing*, reasoning that E2
both ratifies (operational) and authors the shipped templates (enabling). Under
the correction that is the wrong shape: the operational owner and the enabling
development environment are **two distinct external entities that happen to share
personnel**, not one entity wearing two hats. Each entity then carries exactly one
class, which is the simpler schema — and the sharing does not vanish, it becomes
an **external-to-external relationship**, precisely the kind of surrounding
relationship this ruling says the frame must model. Self-adoption is therefore
not an awkward special case in the schema; it is a declared coupling between two
external entities, and the frame can state it.

**The crossing this exposes — `N-02`.** OI-28 observed that templates are minted
through LLM sessions but declared only the OUT half (M-07, the artifact class
leaving). **The inbound authoring flow was never given a crossing**: a human +
LLM session outside the mechanization writes the template and registry content
that the kit then ships. Under this ruling that is a real IN crossing from an
enabling actor, and it is now `N-02` in §1.

**A category error the per-crossing table made visible.** **E11 is not a party** —
"the shipped template set as product" is an *artifact class*. Under the enabling
/ operational split it resolves cleanly into two crossings against real parties:
OUT to the adopting repo (E10), IN from the enabling author (N-02). Sitting 2
should retire E11 as a party and keep it as what it is.

**The registry question — PROPOSED, not ruled.** The owner's initial impression
is an `external.toml` carrying both external agents and external interfaces. The
recommendation here is to **split by entity type, not by internal-versus-external**:

- **An EXTERNAL-ENTITY registry: YES — and the owner's `external.toml` naming is
  better than "actors".** Under the design-scope correction above, the registry
  does not hold *actors*; it holds **external entities**, of which an operational
  actor is one kind and an enabling system another. Naming it for the cut
  (external) rather than for one kind (actor) is what keeps E12 from having to
  pretend to be an actor to get a row. An external entity is a different entity
  type from a directed seam and has **no home in this kit today** — which is the
  §4 item 3 gap. It is precedented rather than exotic: the kit already ships
  off-spine
  registries (`PART`, `ASSET`, `PB`, `REPO`), and `repos.template.csv` already
  models *other repos* as entities with `Type = owned|external|reused`. It is
  also the only place the owner's context requirement can live: **`interfaces.toml`
  structurally cannot hold external-to-external flows**, because every IF row has
  `this_project` on one side by construction. "The author mints a template, the
  kit ships it, the adopter customizes it" is a chain with one link that never
  touches the kit — and that chain is exactly the surrounding relationship the
  ruling says the frame needs.
- **A second INTERFACES registry: NO**, and the argument is the owner's own
  ruling. **D-6** (2026-08-10, `repo-lock.md`): F5's copy-ability *"does not
  cover a shared **vocabulary**, whose divergence is silent content loss."*
  LLR-166's rationale states the failure: *"duplicating a vocabulary fails
  silently — the copy that has not learned a column returns a row missing that
  cell, which every consumer reads as 'the cell is empty'."* An external-interface
  registry parallel to `interfaces.toml` is that duplication exactly — same
  fields, two files, and four consumers (`plan_briefs.IF_SURFACE_COLUMNS`,
  `check_trajectory` connectivity, `trace` integrity, `derive_gate`) that must
  learn both or silently read one. There is a second cost specific to this repo:
  as the partition recurses, crossings **move** between internal and external.
  Under two registries that is a delete-and-mint, and D-4 says ids never re-mean,
  so every reclassification loses its history; under one registry with a
  resolvable counterpart it is an edit.
- **So:** external entities (and the relationships among them) get a new home; every
  directed seam that *touches* the system stays in `interfaces.toml`, with
  `counterpart` becoming a **resolvable reference** — a declared external-entity id or an
  in-repo path. Boundary-ness becomes **derived**, which is what makes
  X-14/X-15's mislabel unrepresentable rather than merely visible.

**Why the registry earns it: the RENDERED VIEW — and why the prose variant is
withdrawn.** An earlier draft of this section offered a cheaper first move —
park the entities and the context as prose in `docs/architecture.md`, mint a
registry later. **That is withdrawn**, on the owner's reasoning and on the file's
own shape. `docs/architecture.md` is **1,594 lines of which ~1,402 (88%) are
GENERATED** — the AST-plus-`IF-###` dependency graph (L41-267) and the
per-symbol module map over ~60 scripts (L276-1450), both written by
`gen_arch_map.py` and freshness-gated by `--check`. Its hand-authored remainder
is ~192 lines: the intro, *Shape of the product*, and *Runtime flows*. So the
file's **structural** content is already a rendering target, and a hand-written
frame would be the one piece of structure in it that nothing generates. There is
a second consequence: `PROJECT_STATE.html`'s **"How (SW architecture)"** tab
already renders that module map (`traj_views.py`: *"The module map from
`docs/architecture.md`"*), so registry data joins an existing pipeline —
registry → generated block → dashboard tab — while prose could only join it by
being parsed.

**The split by KIND, not by cost.** The entities and their interconnections are
enumerable structural data → **registry**, feeding a *generated* context view
emitted beside the dependency graph and rendered in the same tab. The
operational **narrative** is what *Runtime flows* already is — hand-authored,
SR-cited, checked by `check_flows.py` — so the frame is not introducing a new
category but completing one.

**The cost, corrected in both directions.** *Lighter than first stated:* the
entity registry is **off-spine** — the `PART`/`ASSET`/`PB`/`REPO` tier — because
it exists to build the view, not to gate the spine; so entity rows need no SR
back-refs, no gate arithmetic, an advisory schema tier, and a leftover example
row blocks nothing. *Heavier than first stated (owner's note, 2026-08-13):*
**SRs are still expected to resolve back to the boundary interfaces, and that IS
a spine-validation cost.** Measured, so the size is honest:

- **IF → SR already exists and is clean.** `trace.interface_findings` makes an
  IF row with an empty or unknown `sr_refs` a `--strict` finding; **all 113 live
  rows link at least one valid SR**, the eleven declared frame crossings
  included (IF-013 → SR-006/007/008, IF-015 → SR-026/027/028/030, and so on).
- **SR → IF does NOT exist.** No check reads an SR's inputs and outputs and
  asks whether each references a declared interface. That direction is exactly
  **SN-037's ratified acceptance** (*"unresolved references, uncovered crossings
  and incompatible signal types are mechanical findings"*), and it is the real
  spine cost: a new checker, plus **WI-451's re-statement making the ~57
  internal-naming SRs resolvable in the first place**. The registry is the cheap
  half; this is not.

**The light tier for a simpler adopter — a single INPUTS / OUTPUTS pair.**
Recommended as the kit-level default, with one refinement: it must be **the same
schema with two rows**, never a different mechanism, so growing from light to
full is *adding rows* rather than migrating a file. A simple project then gets an
honest one-blob context diagram, and — the part worth keeping — **the derived
check still bites at that tier**: if `counterpart` must resolve to a declared
entity *or* an in-repo path, an internal station seam cannot claim
`downstream adopter` when the only declared entities are INPUTS and OUTPUTS; it
has to name its path. X-14/X-15's defect is caught at the lightest tier the kit
offers.

---

## 2. The boundary set the SRs get written against

**The discriminator, stated as a rule WI-451 can apply mechanically:**

> An artifact may be named in SR text **iff** it is the *this-project* side of an
> IF row whose `counterpart` is an **external party from §1** — i.e. it is a
> **port**. Everything else is an **internal seam**: it belongs to the LLR tier
> (or is re-stated against the IF row that types the seam).

**Depth-0 PORTS — the proposed list.**

- **Harness entry** — `check.py` (IF-013); **scaffold/re-sync** —
  `bootstrap.py` (IF-014, incl. `--agents`/`--sync`).
- **Unattended entry** — `agent_loop.py` (IF-015) + root
  `agent-resume.{cmd,sh,command}` (M-02, no row). **Contributor launchers** —
  `run.*`/`run_menu.py` (IF-048), `dev-setup.{sh,cmd,command}` (M-01, no row).
- **Agent-harness contract** — `subagent_gate.py` PreToolUse (IF-020).
- **The git hook floor** — `pre-commit`, `pre-push`, `commit-msg` (M-13, no row).
  Ports *because they are the only thing standing between E3 and the tree*
  (OI-28: SR-019's rationale is already written as a boundary statement).
- **Adopter-invoked generators** — `gen_cases.py` (IF-017),
  `gen_release_checklist.py` (IF-018), `check_vendored.py` (IF-016).
- **Declared surfaces a human reads or edits** — `docs/process.toml` (the dial
  surface), `docs/status.md`, `docs/gate`, `PROJECT_STATE.html`,
  `open-items.html`, `docs/architecture.md`. **The surface is the port; its
  generator is not.**

**Internal seams — the LLR/architecture tier.** The W1–W4 component boundaries
(`components.toml`: CMP-006 Registry & conformance · CMP-007 Gatekeeper ·
CMP-008 Autonomy · CMP-009 Human & adopter surfaces, all `State = planned`,
provisionally adopted warn-first — sitting-pack §3). Under the recursion these
are *depth-1* boundaries produced by the P5 partition; the ladder is explicit
that a partition **is** the next level's boundary declaration, so they are not
depth-0 frame and SRs must not name their modules.

**Worked examples of each class:**

| SR | Names | Class | Why |
|---|---|---|---|
| SR-006 | `check.py` | **PORT** | IF-013's this-project side; an adopter types this string |
| SR-034 | `scripts/*.py` (as a set) | **PORT-ish** | names the *shipped set*, not a module — a property of E10's crossing |
| SR-026 | `agent_loop.py` | **PORT** | IF-015 |
| SR-137 | `docs/process.toml` | **PORT** | E2's dial surface |
| — | `gen_trajectory.py` (11 SRs) | **INTERNAL** | the *dashboard* is the port; the generator is CMP-009 realization |
| — | `check_trajectory.py` (9 SRs) | **INTERNAL** | a lint inside CMP-007; the adopter invokes `check.py`, never this |
| — | `trace.py` (10 SRs) | **INTERNAL** | same; its verdict reaches the outside only through IF-013 |
| — | `schedule.py` (5 SRs) | **INTERNAL** | CMP-008 frontier machinery, no external counterpart |

**Measurement, and where it differs from the pack.** `75 of 148` SRs name a
`.py` in `requirement` text — the pack's figure reproduces exactly. Splitting
them on the *ten declared-external-port scripts* (`check`, `bootstrap`,
`agent_loop`, `check_vendored`, `gen_cases`, `gen_release_checklist`,
`subagent_gate`, `run_menu`, `integrate`, `trunk_step`) gives **18 SRs naming
only ports** and **57 naming at least one internal module** — not the pack's
~25/~50 estimate. The delta is definitional (the pack's "entry-point-class" was
a looser reading), and it moves the re-statement program *up*, not down. The
per-row census is WI-451 slice 1's job; this figure only sizes it.

<!-- fig: cmd="python3 - <<'EOF' … tomllib over system-requirements.toml, re
r'\b([A-Za-z_][A-Za-z0-9_]*\.py)\b' over requirement text, ports set as listed",
rev=4295dea4 -->

---

## 3. The SR↔SN duplication question

**The owner's concern, verbatim:** *"If a system requirement is defined at the
boundaries of the system, it can't refer to its implementation and it also can
feasibly be 1 SR per SN, and then implementation specific details drop into
LLRs. My main concern is how much duplication might exist between SR and SNs."*

**The quantification** (`tomllib` over `stakeholder-needs.toml` +
`system-requirements.toml`, counting `sn_refs`):

- 27 SNs, 148 SRs, **232 (SR→SN) edges**.
- **19 SNs are covered; 8 are not** — and the uncovered eight are exactly
  SN-033…SN-040, *including all four boundary needs ratified at sitting 1*.
  All 27 rows now read `kind = "core"` (the sitting-1 ratification commit,
  4295dea4), so **SN-037…SN-040 are ratified needs with zero SRs.** They are
  not "young rows waiting for decomposition" — they are the commissioning
  authority for WI-451, and WI-451's output is their first coverage.
- Across the 19 covered: **min 2, median 8, mean 12.2, max 30**.
  **No SN has exactly one SR.** The thinnest are SN-028 (2), SN-011 (3),
  SN-029 (3); the fattest are SN-006 (30), SN-025 (28), SN-002 and SN-010 (24).
- **82 of 148 SRs cite more than one SN** — so the graph is not even a tree,
  let alone 1:1. A 1:1 tier would have to *cut* 84 of the 232 edges.

<!-- fig: cmd="python3 - <<'EOF' … collections.Counter over sn_refs; median via
statistics.median", rev=4295dea4 -->

**Chain 1 — SN-008 → 19 SRs: the SN is one word, the SRs are the mechanism.**
SN-008 is *"a reader can believe a green: gates are honest, and a green never
hides a skipped check, a stub, or an unmet criterion."* Restated at the boundary
it fans out across **different ports**: SR-006 types IF-013's verdict
(`--gate <bar>` runs that bar's steps; a missing tool **fails**, `--lenient`
degrades to SKIP); SR-016 is the stub detector; SR-133 the freshness skip;
SR-093…098 the loop's own honesty. **The SR tier is not duplicating SN-008 —
it is naming which port each promise is measurable at.** One need, many ports:
this is the healthy case and it is the majority.

**Chain 2 — SN-006 → 30 SRs, via SR-026: signal typing and error paths.**
SN-006 says *"an agent can run unattended and resume from repo text alone; such
a run never blocks on a prompt and fails clearly."* SR-026 adds what the port
contract must say: *which* text is authority (claimed assignment + committed
trailer evidence, **not** `docs/status.md`, which SR-059 makes a *generated*
surface), that stdin is closed, that a rate limit **backs off** rather than
fails, that a stall aborts to protect budget. Everything after the semicolon is
**error-path obligation the SN does not carry** — and the acceptance cell
records that the backoff clauses were folded in at the 2026-08-13 dissolution
*because the review round found no SR carried them*. That is the tier earning
its keep in the record.

**Chain 3 — SN-028 → 2 SRs: the honest near-echo.** SN-028's need cell already
names `docs/process.toml`, bare `[section]` headers, the dual-reader pin and the
`--migrate-config` refusal — because its *acceptance* cell does. SR-137 restates
the one-home-plus-refusal rule; SR-138 adds the migration. **Read SN-028's need
sentence against SR-137's requirement sentence and they say the same thing.**
The delta lives entirely in the acceptance cells (SR-137 enumerates *at every
guarded entry point*: the dispatcher's pre-claim preflight, intake's
adjudication arm, the integrator's verdict gate). SN-011 → SR-034/035/114 is the
same shape: SR-035's whole text is *"the process and ID scheme shall be
stack-agnostic"* with acceptance *"the ID scheme is language-neutral"* — an SR
that adds **nothing** over its SN.

**The options where the echo is real:**

1. **Tolerate the echo, the acceptance cell carries the delta.** Cheapest; keeps
   the tiers uniform; but SN-033's ratified rule (*a stakeholder reads the need
   without knowing how the repo is built*) is violated in the other direction —
   SN-028's need cell is echoing *downward* into implementation vocabulary.
2. **Merge** — delete the SR, point LLRs at the SN. Breaks the join
   (`trace.py` walks SN→SR→LLR→TC); refuted on machinery grounds alone.
3. **Split the roles: the SN carries the OUTCOME, the SR carries the PORT
   CONTRACT.** SN-028 becomes *"the owner can find and change every policy dial
   in one home, and a repo declaring a dial twice is refused"* — no filename;
   SR-137 keeps `docs/process.toml`, the line grammar and the refusal points.

**Recommendation: option 3, and note it is already the ratified direction.**
SN-033 (ratified) forbids internal paths in `need` cells; decision 2.7(a)
permits them in SR cells *at declared ports*. `docs/process.toml` is a port
(§2), so SR-137 keeps its name and SN-028 loses it. The two rules compose into
one sentence: **the need names the outcome, the requirement names the port.**
Do **not** target 1:1 — 82 of 148 SRs are genuinely multi-need, and forcing 1:1
would either merge unrelated ports into one row or duplicate one port's contract
across several. The right invariant is *one SR per (need, port)* pair, which the
current 232 edges are already a rough approximation of.

**One flag for the ruler:** SR-035 as written adds nothing to SN-011 and is a
real merge candidate — but it is `Modified`, so touching it costs a re-attest.
Bundle it into WI-451's window rather than opening a second one.

---

## 4. What sitting 2 must rule

1. **Adopt or amend the depth-0 frame (§1)** — the eleven external parties
   E1…E11 and their crossings, including the six stated uncertainties from the
   data pack §1c (is `downstream adopter` one actor or three? is git one
   crossing or three? is the terminal an actor?). Adopting also means adopting
   the **completeness declaration** — the claim that this set is the whole
   frame — which is what the rung actually certifies.
2. **Adopt or amend the port list (§2)** and its discriminator rule. The two
   rows to decide explicitly: **IF-080/IF-081** (`integrate.py`,
   `trunk_step.py`) declare `downstream adopter` but read as internal;
   and whether a **generated surface** is a port while its generator is not.
3. **The frame's typing axis — ruled in principle (§1a), mechanics still open.**
   The actor-plus-interface rule is the owner's ruling and needs no re-decision.
   What it leaves open is whether the registry grows fields to carry it: an
   **`external`** flag (which `boundary_incomplete` already names as missing, and
   which is what would let the rung check completeness rather than settledness),
   a **crossing-class** axis (CLI · exit status · file artifact · VCS event ·
   network · human-read surface), both, or neither — with the frame's typing
   living in `docs/architecture.md` prose instead while `interfaces.toml` carries
   only what it carries today. Cost of minting: an IF schema change with a
   downstream re-sync; cost of not: the rung's completeness half stays
   unmechanized and the frame is settled only by eye. Note also that `signal`
   stays untouched either way — it is an IF-row property, not the frame's.

   **A third shape, proposed here and not yet ruled: declare the ACTORS, derive
   the rest.** Make the external parties a closed set (E1…E11 as declared rows or
   a vocabulary) and let *"is this a boundary crossing?"* be **derived** from
   whether `counterpart` names one of them — instead of a hand-set flag that can
   drift out of step with the contract beside it. It follows from §1a's ruling
   (if the frame is actor **plus** interface, the actor is the half that should
   be declared) and it is strictly stronger on the evidence in §1's table: the
   four re-read rows and the six file-not-actor partials are all cases where
   `counterpart` says something untrue and **nothing can catch it, because the
   field is prose**. Under a declared vocabulary, an internal seam claiming
   `downstream adopter` becomes unrepresentable rather than merely detectable —
   the repo's own governing principle (`status.md`: *prefer a constraint that
   makes a bad state unrepresentable over a check that detects it*). Cost: a
   closed vocabulary every adopter must populate for their own frame, versus a
   boolean they can set per row.
4. **The five Experimental rows.** They hold the rung down today, and four of
   the five (IF-118/119/120 + IF-057) are internal carrier plumbing, not frame.
   Three dispositions: promote to `Stable` (the carrier sweep has converged);
   leave and accept the rung stays down; or rule that **only external-counterpart
   rows should gate rung 1** — which requires the `external` field
   `derive_gate.boundary_incomplete` says nobody has built yet. **IF-103**
   (`migrate_carrier`) is deliberately provisional and should stay Experimental
   until the conversion program ends.
5. **Where the external entities and the context LIVE (§1b's recommendation,
   not ruled).** Three shapes: an **external-entity registry** (the owner's
   `external.toml`, holding operational actors AND enabling systems under one
   cut) plus a resolvable `counterpart` in
   `interfaces.toml` (**recommended** — derived boundary-ness, one home for
   seams, and the entity data feeds a *generated* context view into
   `docs/architecture.md` and the dashboard's existing "How (SW architecture)"
   tab); **the same file also absorbing the external interfaces**, the owner's
   first impression (rejected in §1b on D-6 grounds — a duplicated vocabulary,
   and reclassification becomes delete-and-mint under D-4); or **prose in
   `docs/architecture.md` first, registry later** — offered in an earlier draft
   and now **WITHDRAWN** (§1b: that file's structural content is 88% generated,
   so a hand-written frame would be its lone exception, and prose cannot join the
   render pipeline). **Tier it:** a single **INPUTS / OUTPUTS** entity pair is the
   kit-level light default — same schema, two rows, so growth is additive and the
   derived check still bites. **Cost, both directions:** the entity registry is
   **off-spine** (view-building, no SR back-refs, advisory schema) — but **SRs
   still resolve to the boundary interfaces**, which is real spine cost: IF→SR is
   enforced today and clean at 113/113, while **SR→IF does not exist** and is
   SN-037's ratified obligation, landing on WI-451 plus a new checker.
   Riders on whichever shape wins: retire **E11** as an entity (it is
   an artifact class, §1b), admit **E12** (the enabling development environment —
   external, tightly coupled, sharing personnel with E2/E3), and confirm that the
   operational/enabling class sits on the **entity** with the personnel overlap
   recorded as an external-to-external relationship (§1b, per the owner's
   design-scope correction).
6. **The 15 missing crossings + 6 partial ones.** WI-442 (queued) owns OI-28's
   two seeds; the rest need an owner, including the two this draft added
   (**N-01** `docs/process.toml` as the owner's dial surface, **N-02** the
   inbound template-authoring flow). Ruling scope here decides whether rung 1 can
   honestly close at all — and note the completeness declaration (§1c) is now
   known to be complete-minus-two.
7. **The duplication policy for the re-statement pass** — §3's option 3, or an
   alternative — stated as a rule WI-451 slice 2 can apply per row, plus whether
   SR-035's merge rides that window.
8. **Where the boundary record LIVES once ruled.** SN-040's acceptance requires
   it *"kept with the architecture, not in session prose"*, and
   `docs/architecture.md` has **no boundary section today** — that gap is owed
   under every option. The frame's prose belongs there; the typed crossings
   belong in `interfaces.toml`. **Amended by §1b:** this draft opened at
   "no new registry" — true of *interfaces*, and still recommended — but the
   context ruling means the **parties** may need a home that neither file has,
   which is item 5. So the honest statement is now: **no second interfaces
   registry**; whether an external-entity registry is minted is open.
