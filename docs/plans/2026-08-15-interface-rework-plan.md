# The interface rework — a sized plan, for ruling

**An amendment to OI-14 Part B ("what an interface row must say"), which is
already `ruled`.** Not a new program.

**Status: UNRULED, UNEXECUTED.** No registry row has moved.

> **REVISION NOTICE — this document was rewritten 2026-08-15 after an
> adversarial Opus review returned CHANGES-REQUESTED with ten MAJOR findings
> against its first version.** The review is why the owner made it a
> precondition of presenting the plan, and it earned that: the first version's
> headline finding was **factually wrong**, and its central recommendation would
> have taken a clean gating check to 32 hard failures. Both are documented below
> rather than quietly dropped, because the *reason* the first version was wrong
> is itself the most useful thing this exercise produced. The first version's
> conclusions are superseded in full; §1 records what they were and why they
> failed.

**Every count below is measured against the re-tier lane**
(`…/wi451-sr-retier-campaign`, 64 SR rows), **not trunk** (149 SR rows).

---

## 0. The one-paragraph version

**The schema inversion should not proceed, and the measurement that motivated it
does not survive re-derivation.** The proposal's headline — *"74 of 115 seams
are consumed with no declared provider"* — is the direction split restated:
every row is its own seam, `Provides` 41 + `Consumes` 74 = 115, so "uncovered"
is definitionally "is a `Consumes` row." No provider gap of that size exists:
all 41 distinct providing modules author a `Provides` row, and the modules the
proposal named as declaring nothing — `spine_carrier` above all — declare one
explicitly. What *is* wrong with the registry is what the owner actually said
was wrong with it: **it is hard to read.** That is a schema-tier problem, which
is what OI-14 Part B already ruled ("ADDING A SCHEMA TIER, not writing more
prose"), and it is roughly a tenth of the work the inversion would have cost.

---

## 1. The finding that dissolved, and how it survived two documents

The proposal (§1) and the first version of this plan (§0, F1, steps 1 and 5)
both rested on this:

> `spine_carrier` is consumed by 14 modules and **declares no output at all**;
> `trace` and `check_trajectory` by 5 each. The modules most depended upon are
> precisely the ones with no declared outputs.

It is false. `spine_carrier` authors `IF-102`, `direction = "Provides"`, and its
`notes` cell opens `"source - spine_carrier consumes nothing by design"` — it is
not merely declared, it is declared *and* annotated with the honesty marker the
proposal said the model still needed. `trace` authors IF-001,
`check_trajectory` IF-009, `schedule` IF-053, `prompts` IF-097. **All 41
`Provides` rows have 41 distinct authoring modules.**

The error was to compute coverage over `(provider, consumer)` **pairs** and
report it as coverage over **providers**. Since one row is one pair, a pair is
"covered" exactly when a `Provides` row was written for it:

```
seams=115  covered=41  gaps=74        direction: Provides 41, Consumes 74
```

`41 + 74 = 115`. The measurement has one degree of freedom and it is the
`direction` column.

Three process points, because this is the second campaign in a month to lose
counts this way (resume brief §5, *"Measure, do not report intent"*):

- **The number was carried, not re-derived.** The proposal measured it; this
  plan's first version reproduced the pipeline that produced it and read the
  agreement as confirmation. Re-running the same derivation is not verification.
- **A derived quantity that equals an input column is a smell.** "74 of 115"
  should have prompted the check `74 == count(direction == "Consumes")`. It
  takes one line.
- **It was reviewed as a plan, not as a diff, which is the only reason it was
  caught before 115 rows moved.** That is precisely the owner's stated rationale
  for mandating the review at plan stage.

### What the corrected audit does show

Applying the first version's own proposed rule — credit a provider only from a
row it authored — to the lane:

```
provides-credited modules   OLD: 43    NEW: 41
modules losing credit: scripts/plan_coverage, scripts/wi_convert
new "declares no Provides seam" warns: 1   (plan_coverage is marked `sink`)
```

**One warning.** Not 42. The rule change may still be worth making on its
merits, but it is a one-row finding, not a program.

---

## 2. Why the endpoint fields must not be deleted — four blockers, measured

### B1 — Deleting the `Consumes` rows breaks a gating check: 0 → 32 findings

`check_trajectory._declared_seam_pairs` stores each row's endpoints **both
ways** — *"a seam is one declared relationship, whichever side authored the
row"* — and that set is what silences `cross_component_findings`, whose rule is
*"an internal import edge whose endpoints belong to different CMP components
must be covered by a declared IF-### row."*

Simulated on the lane by deleting the 72 non-process `Consumes` rows:

```
TODAY   cross_component_findings = 0
AFTER   cross_component_findings = 32
  - cross-component import scripts/agent_loop (CMP-008) -> scripts/spine_carrier (CMP-006) has no declared IF-### seam
  - cross-component import scripts/check_doc_refs (CMP-007) -> scripts/gen_arch_map (CMP-006/CMP-009) has no declared IF-### seam
  …
```

`component_findings` promotes these to **ERROR under `--strict` at DevBar-Tests
and above** — the bar this campaign is walking back to.

**This inverts the first version's central argument.** It claimed the import
graph made the `Consumes` rows redundant. The relationship is the opposite: the
**import edge is the obligation, and the row is the discharge.** The registry
itself says so — `components.toml` CMP-006's notes record that `gen_arch_map`'s
one straddling import edge *"stays POLICED (**IF-117** covers it)"* — and IF-117
was on the deletion list.

### B2 — 35 of the 74 rows have a non-module endpoint and nowhere to go

Of 74 `Consumes` rows: 39 are module→module, **35 have at least one endpoint
that is not an arch-map module** (a file, a tool, an upstream). For those there
is no import edge to derive from and no provider that could author a row. The
`source`/`sink` marker does not substitute — it marks a *module* as consuming or
providing nothing; it cannot record "`trace` reads `system-requirements.toml`."

### B3 — Derivation from the arch-map is Python-only, in a stack-agnostic kit

`Imports (internal):` is produced by `gen_arch_map.py` from the Python AST. A
model that derives the consumer side from it works for Python adopters and
silently degrades to nothing for everyone else — against the kit's stated
stack-agnostic core and its own retrofit guide.

### B4 — Core's ratified glossary defines an interface as a two-endpoint relation

> **Interface (IF-###)** — a typed connection contract **between Modules**, in
> four views…

That is what `this_project`/`counterpart` encode. The first version quoted the
half of Core's glossary that kills `serves` (the slot rule) and not the half
that supports keeping endpoints. And Core's own `ThisProject` cells read
`gilbert (HAL: joint surface)` — the IF schema has no name/title field, so
**`ThisProject` is the only place the surface is named**; deleting it deletes
the name.

---

## 3. What is actually wrong, measured

The owner's complaint was legibility: an interface row lists `this_project`,
`counterpart`, `direction` and `sr_refs`, *"none of which tell you who is
serving the interface without looking at more details."* That complaint is
correct and these are its causes.

| # | Defect | Size |
|---|---|---|
| D1 | **The IF registry has no schema tier at all.** `trace.py`'s required-field and enum dictionaries carry keys for SR, LLR and TC only — no IF key. Nothing is required, nothing is enum-checked, nothing bounds a cell. (OI-14 Part B, re-verified.) | the whole registry |
| D2 | **Endpoint cells are unvalidated and have rotted.** 24 of 115 `counterpart` cells resolve to nothing. **10 are genuine rot** — 4× `docs/requirements/system-requirements.csv`, plus `agents.csv`, `open-items.csv`, `stakeholder-needs.md`, `performance-budgets.csv`, `subagent-gate`, `coverage.json` — spine files migrated to TOML and never followed. The rest are legitimately external (`downstream adopter` ×8, `git`, `agent CLI`, `upstream docs`, `run.* launchers`) but carry **no marker saying so**, which is why they are indistinguishable from rot. | 10 to fix, 14 to mark |
| D3 | **One cell holds three endpoints.** `IF-097`'s counterpart is `"scripts/agent_loop;scripts/plan_briefs;scripts/plan_runner"` — a list in a scalar field, which is what makes any seam count approximate. | 1 row |
| D4 | **`this_project` drift.** `IF-080` names `scripts/integrate`; the module that declares it in its docstring is `scripts/handback`. 107 of 115 agree, 3 more are hook rows (correct as written), this one is wrong. | 1 cell |
| D5 | **Answering "who serves this" needs three cells read together** (`direction` + `this_project` + `counterpart`) with the meaning of the latter two swapping on the first. This is the owner's complaint, exactly. | schema |
| D6 | **`sr_refs` means two different things by tier** — a design row's parent requirement, and an interface's requirements. One column, two relationships. | naming |

---

## 4. The recommendation

**Add the schema tier OI-14 Part B already ruled; do not invert the schema.**
Nothing below deletes a column, so nothing below can break B1–B4.

| # | Step | Size | Gate |
|---|---|---|---|
| 1 | **Give IF a schema tier in `trace.py`** — required fields, enum-checked `direction`, `approval`, `signal`; bounded `contract`. This is the ruled direction and every other step depends on it. | 1 dict entry + validators; ~40 lines; +2 TC | **RULING** (it is OI-14 Part B's execution) |
| 2 | **Validate endpoints against the tree**, warn-first: an unresolvable `counterpart` or `this_project` that carries no `external` marker is a finding. | ~20 lines; +1 TC | none — new warn-first check |
| 3 | **Fix what step 2 finds** — 10 rotted paths, 14 external endpoints marked, `IF-097` split or its field made a list (D3), `IF-080` corrected (D4). | 25 cells, 1 possible row split | none — cell corrections |
| 4 | **Rename `IF.sr_refs`** to something that does not collide with the design tier's meaning (D6). | 115 cells, mechanical; template + PROCESS §8 + EXAMPLE.md in lockstep | **RULING** (a shipped column name) |
| 5 | **Author the owner cell** (D5) — `owner`, id-typed, holding an `SR-###` **or** a design-tier id (Q1), resolved against either registry, invariant "exactly one owner per interface". Replaces the three-cell read (`direction`+`this_project`+`counterpart`) that is the owner's original complaint. **Revised from "derive it" by Q1** — see §6. | 115 cells to populate (mechanically seeded from `this_project`, then 115 judgement reads); +1 resolver, +2 TC | **RULING** |
| 6 | **Split flow out of `direction`** (Q2) — ownership orientation moves to step 5's cell; what remains is a **flow** property that is genuinely often absent. `traj_views` is its live consumer and keeps reading it. Restate the 74 `Consumes` rows as **coverage declarations**, which is what §2 B1 shows they already are. | 1 column renamed/re-scoped; `traj_views` + its TCs; the 74 rows' meaning stated, cells unchanged | **RULING** |
| 7 | **Interface composition** (Q3) — an IF may name another IF as its destination; add the carriage field, an **acyclicity check** and a depth bound. Prove it on `IF-102` (`spine_carrier`, 14 constituents, the highest-concentration seam in the audit) before generalising. | 1 field + 1 check + 1 TC; 1 worked bundle (15 rows touched) | **RULING** |
| 8 | **Re-base the `interfaces.toml` header off dead SR-091** — it holds `direction`/`counterpart` on the grounds that deleting them would remove *"a ratified requirement's only input"*, naming SR-091. **SR-091 does not exist on the lane**; the census demoted it and its obligation is now the design row *"Hierarchy seam ports."* The constraint holds; the citation is dead. | 1 header block | none — prose |

**Deferred, explicitly:** `SR.provides` / `IF.serves`, dropping the endpoint
fields, and minting provider rows. B1–B4 are the reasons. If the inversion is
revived it must first answer B1 (what covers the 32 cross-component edges) and
B2 (where the 35 non-module facts go).

**Note what the rulings did to the inversion's case.** Q1 and Q2 give the owner
his original complaint's answer — one id-typed cell says who owns it, and
ownership no longer pretends to be flow — **without deleting a column**. The
inversion's stated purpose was legibility; steps 5 and 6 deliver that, and
B1–B4 remain unanswered. The inversion is now not merely blocked but
unmotivated.

### What the rulings did and did not add

Steps 5–7 are new or revised by the 2026-08-15 rulings (§6). Step 5 changed
direction — from *derive the provider* to *author an owner cell* — because Q1
makes the owner polymorphic across tiers and today's `this_project` holds a path
string, not a resolvable id.

**Q4's `views` facet is deliberately NOT a step.** It is ruled for the model;
this repo is pure software, nothing here would populate the column, and a column
no row uses is the failure the `Area` retirement just corrected. Whether it
ships in the **template** ahead of this repo's own registry is a separate call
and is not taken here.

**Sequencing inside the rulings:** step 6 depends on step 5 (flow can only be
split out once ownership has somewhere else to live), and step 7 depends on step
1 (the carriage field needs the schema tier to validate it). Steps 5–7 do not
depend on each other beyond that.

---

## 5. The hardware crosscheck — what Core does and does not support

Read 2026-08-15 from `/Users/diytechy/Documents/Core`.

**Read the limit first.** Core's hardware half is **designed, not exercised**:
`interfaces.csv` has **3 rows, all software HAL surfaces**; `procurement.csv`
holds only the `PART-000` example; `hardware/assemblies/` and `tests/hardware/`
are empty; `electrical/` is a README; no mass budget row exists. Core is
evidence about **reasoning**, tested against this kit by someone who set out to
test hardware fit. It is not evidence that any model survives a populated
hardware registry.

| Question | What Core shows | Strength |
|---|---|---|
| **Interface between two assemblies — one row or two, who owns it?** | Whiteboard 09 §1 names each seam from both sides (BASE "Torso mount plate" ↔ TORSO "Base mount"; ARM-PROX "elbow plate out" ↔ ARM-DIST "Elbow plate"). The `out` suffix appears 3 times in one kinematic chain and not on TORSO's provider-side entries, so **"proximal provides" is an inference from the reader's kinematic model, not a marker in the data.** | **Weak.** Whiteboard prose; zero mechanical rows exist. |
| **A mutual seam with no natural provider?** | Three: the normally-closed **e-stop loop** (named by BASE and PWR, assigned to PWR *by function*); the **backbone pass-through** through TORSO, which neither provides nor consumes; and **HARNESS**, which *"**Is** pure interface: its IF rows are its existence"*, owned by *"Build (integration-owned)"*. | Medium. Core's answer is an **owner/hat**, not a provider role — which is the custodian concept, not a replacement for it. Reifying HARNESS as a module does not close it: TORSO names the same backbone, and HARNESS↔ARM-PROX is itself a mate. |
| **Would dropping the endpoint fields cost Core anything?** | Yes — see B4. Its `Counterpart` cells *are* prose sets (`"all logic nodes"`), which is the proposal's shape hitting the proposal's own wall; but `ThisProject` is the only place its surfaces are named. | Medium-high. |
| **How is HARNESS modelled?** | As a Module that is nothing but its interfaces, with a real rig (continuity + flex-cycle through joint range) and a real budget (conductor count per joint, connector mass). | Medium. |

**The invariant the proposal proposed fails on Core outright.** All three Core
rows carry **three** `SR-Refs` each, so *"every interface is named in exactly one
requirement's `provides`"* would require picking an owner from three co-equal
requirements on 100% of the only physical-adjacent adopter's rows. On the lane
it bites 7 of 41 `Provides` rows (IF-004, IF-005, IF-009, IF-013, IF-014,
IF-015, IF-044).

**One mechanism carries across at zero cost and is already proven:**
`check_perf.py` is metric-agnostic — "grams and N·m budget exactly like
milliseconds."

**And Core's swappability rule cuts against `serves` specifically:** a slot
declares *the interfaces it requires*, and a module fills it iff it satisfies
them. The interface never names its consumers, because naming them would make
every module swap edit the interface row — the churn a narrow waist exists to
prevent.

---

## 6. The four open questions — RULED (owner, in session, 2026-08-15)

All four are ruled. The rulings are recorded verbatim, then what each changes.

### Q1 — Owner: a requirement or a module? **BOTH.**

> *"An interface can serve both. Requirements are just decomposition of needs
> into measurable objectives, and modules are just physical implementations at a
> lower level that do the same thing. Thus, a requirement and a module can
> provide/own an interface."*

**What it settles:** the contradiction the review found — this plan answering
"requirement, because a module is a placement" while handing mutual seams to a
component — was a false dichotomy. Both tiers are decompositions of the same
thing at different levels, so both are legitimate owners.

**What it changes:** the ownership pointer is **polymorphic and id-typed** — one
cell holding an `SR-###` *or* a design-tier id, resolved against either
registry, under one invariant ("exactly one owner"). It does **not** become two
authored fields (`SR.provides` + `LLR.provides`); that would double the authored
surface and re-open which tier signs.

**And it moves this plan's recommendation.** §4 step 5 offered (a) a *derived*
provider view and (b) an *authored* owner cell, and recommended (a). **(a) is no
longer sufficient:** a derived view can only surface what is already encoded,
and `this_project` holds a module **path string**, not a resolvable id — it
cannot express "SR-012 owns this." **Step 5(b) is now the answer**, and §4 is
updated below.

### Q2 — Bidirectional seams: **ownership implies orientation; orientation is not flow.**

> *"A 'provide' from one requirement or module implies directionality, but does
> not mean it is actually directional."*

**This is the ruling with the widest reach, and it dissolves three problems at
once.** It separates two facts the `direction` column currently fuses:

| | What it is | Where it belongs |
|---|---|---|
| **Ownership orientation** | who is answerable for the interface — bookkeeping | implied by the owner cell; never authored twice |
| **Flow directionality** | whether anything actually travels one way | a **property of the interface**, and often absent |

Consequences:

1. **The bidirectional question dissolves.** No "two interfaces, one per
   direction" rule is needed. One row, one owner; whether it is actually
   directional is a separate and possibly empty property.
2. **The physical/mutual case is solved without a special rule** — and better
   than either prior answer. A bolted joint, a mated connector, a thermal path:
   *owner* = whoever is answerable, *flow* = none. The proposal's **custodian**
   and this plan's first version's **reify-as-component** were both workarounds
   for a conflation that Q2 simply removes. No second rule, no new kind, no
   promotion of seams to components.
3. **`direction` is misnamed and mixed-purpose.** `Provides` is doing *ownership*
   work under a flow-sounding name, and `Consumes` — under Q2 — is not an
   ownership claim at all. Which reconciles with §2 B1 rather than threatening
   it: the 74 `Consumes` rows are **coverage declarations** (this cross-component
   edge is intended, and here is the row that discharges it), not ownership
   rows. They stay; what they are called and what they claim gets stated.

Flow direction keeps a live consumer — `traj_views` orients the seam graph from
it — so it is a real field, not a speculative one.

### Q3 — Signal granularity: **one row per contract, AND contracts compose.**

> *"Yes — and I'll note an IF could feasibly have a destination of another IF, so
> 6 IFs could have a destination of a larger IF to carry them in a single
> definable signal. They themselves can be decomposed to an extent."*

**This is new structure, not in any prior version of this plan or the proposal:
an interface may name another interface as its destination.** Six constituent
IFs ride inside one carrier IF.

**What it settles:** granularity stops being a forced choice. You declare the
bundle *and* its constituents, related by a carriage link, and decompose only as
far as is useful.

**It answers HARNESS directly** — Core's loom, *"pure interface: its IF rows are
its existence"*, is one carrier IF; the joint bus, power rails and e-stop loop
it carries are IFs whose destination is that carrier. Core needed no such
concept only because it has written zero physical rows.

**It has an immediate, testable application in this repo.** `IF-102` —
`spine_carrier`, literally named a carrier and consumed by 14 modules, the
highest-concentration seam in the audit — is the natural first bundle, with the
14 consumption seams as constituents. That is the cheapest available test of
whether the concept earns its column.

**It also may bear on §2 B1** — if a carrier row can cover the edges its
constituents cover, one bundle could discharge many cross-component import
edges. *Flagged as worth testing, not claimed.*

**New obligation it creates:** the carriage graph must be **acyclic** and its
depth bounded, or `IF-A carried by IF-B carried by IF-A` is representable. That
is a check, and it belongs in step 1's schema tier.

### Q4 — Does physical get its own kind? **No — a `views` facet.** *(Agreed.)*

Core's ratified vocabulary: one Interface, four views (Mechanical / Electrical /
Network / Software); a slot is filled iff all four are satisfied. Ruled for the
**model**. The **column stays out of this repo's schema for now**, stated
explicitly rather than silently: this repo is pure software, nothing here would
populate it, and a column no row uses is the exact failure the `Area` retirement
just corrected. It lands when a physical adopter needs it — or in the shipped
template ahead of this repo, which is a separate call.

---

## 7. Sequencing

1. **Steps 2, 3 and 8 now** — a warn-first check, 25 cell corrections, one dead
   citation. No column changes, no ruling needed beyond noting them.
2. **Rule the five re-tier findings** (brief §4: H1, H4, H5, M1, M3) and the two
   flagged crossing attributions.
3. **Merge the lane — and the ratification wave is no longer blocked by this
   work.** Brief §4 option **(a)** — merge and ratify now — is viable, and the
   2026-08-15 rulings do **not** re-open it. The reason is specific and worth
   checking rather than trusting: under Q1 the owner cell lives on the **IF
   row**, holding an `SR-###` or a design id. **No SR row gains a field**, so
   nothing in steps 1–8 gives cause to sign the same requirement twice. That was
   the entire argument for holding, and it is gone.
4. **Rule steps 1 and 4–7** — the schema tier, the `sr_refs` rename, the owner
   cell, the flow split, and interface composition. Steps 5–7 are the rulings of
   §6 being executed; step 1 is their precondition.
5. **D-3 stays scoped as it is** (shedding `direction`/`counterpart`) and stays
   **blocked** — B1 and B2 are the blockers, and they are new information for
   it.
6. **Round 2 of the adversarial review last**, on the settled state.

---

## 8. Downstream and template impact

Absent from the first version entirely; it is a template repo, and this is the
part that breaks other people.

- **`tests/test_dogfood_sync.py`** maps `"IF-ID" → (docs/requirements/interfaces.toml,
  registries/interfaces.template.toml, "interface")`. Structural parity between
  this repo's registry and the shipped template is a **hard test** — any schema
  change must land in both in one commit or the suite fails.
- **`project-trajectory/INTERFACES.template.md`** documents the columns and
  ships a rule that dies with them: *"Direction drives ownership. Only the
  `Provides` side may close the owner's final read."*
- **`PROCESS.md` §8** and **`EXAMPLE.md`** carry worked rows in the current
  shape. PROCESS.md is byte-budget-watched — run the `byte-budget-guard` skill
  before and after.
- **`RESYNC_PACK.md`** is the ruled one home for downstream migration entries
  and is structurally tested. Steps 1, 4 and 5 each need an entry.
- **Docstrings.** 42 script files carry `Contracts: IF-###` lines naming 69 of
  the rows any deletion would remove; `interface_findings` warns per dangling
  id. Steps 1–6 as scoped touch none of them — which is another reason to prefer
  this scope.

---

## 9. Risks and rollback

- **Step 1 is the only irreversible-ish step**, and only in the sense that a
  schema tier makes previously-silent rows loud. Land it warn-first, promote to
  strict in a second commit, and the rollback is reverting the promotion.
- **Steps 2–6 are individually revertible** — one check, cell edits, a
  mechanical rename, a prose block. Each should be its own commit.
- **Do not run `gen_arch_map.py` with default args.** It scans a non-existent
  `src/`, emits an empty map behind a warning, and has destroyed 1,413 lines of
  committed content once. Always `--src project-trajectory/scripts`.
- **A green suite is not evidence on §5.** This repo is pure software; the
  suite passes whether or not the model fits hardware.
- **This plan has been reviewed once, adversarially, and materially changed as a
  result.** It has **not** been re-reviewed in its current form. A second round
  against this version is cheap and is recommended before step 1 is ruled.

---

## 10. Authorisation

Nothing here is ruled. Per resume brief §6b what was authorised without a ruling
is: running the audit (done — §1), reading Core (done — §5), and writing this
plan under adversarial review (done — see the revision notice). **Executing any
step requires an explicit ruling**, and `human_ratification_through = 4` does
**not** hold them: it covers attestation-class work only, so build work of this
shape dispatches unasked unless an instruction stops it.

---

## Execution record (2026-08-15)

**Steps 1–8 are EXECUTED.** Landed on trunk (`infra/mechanized-loop`) in five
commits under the owner's 2026-08-15 charge-through instruction: *everything
here is provisional and overturnable at the review sitting*, and no approval or
status cell was moved.

The full record — what landed per step, all 21 judgement owner picks with their
reasons, the external-marker design, the `carried_by` prototype, and the two
cells the plan predicted that turned out **not** to be defects (IF-080 and
IF-097) — is the Decisions-log entry **`2026-08-15e`** in
[`../log.md`](../log.md). Read that, not this section, for the detail.

Three of this document's own measurements did not survive execution and are
corrected there rather than edited out of §3: **D1** overstated the gap (the IF
schema tier largely landed at WI-443; only `Direction` was missing), **D2**'s
tenth rotted cell was a *declared absence* and the checker was wrong rather than
the row, and **D4** was a misreading — `IF-080`'s `this_project` is correct as
written.

**§6's rulings are unchanged.** Nothing in execution reopened Q1–Q4.
