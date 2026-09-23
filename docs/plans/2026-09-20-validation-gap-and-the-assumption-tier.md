# The validation gap and the assumption tier

**Status: PROPOSAL. Not a ruling.** It asks for one, because it changes the
frame that [`external.toml`](../requirements/external.toml) declares LOCKED.
The owner has answered most of its questions (§11). Those answers set the
direction the next sitting builds on. They are not the ruling itself, and
`external.toml` is unedited.

**What it proposes, in one sentence.** The kit records what the system must do
at its own interface and tests that exhaustively; it does not record the
assumptions that carry those interface facts up to the human outcomes its needs
are written about, and therefore cannot test them — so this proposes that those
assumptions become rows, that test cases may verify them, and that the depth-0
frame be redrawn around the system in operation, so that the crossing where an
outcome lands is one the frame actually holds.

**Who this is for.** The owner, as a decision document. It names what would
change and what it would cost before anything is built.

---

## 1. The gap, in this repo's own rows

Two needs, quoted whole. Read the `need` cell against the `acceptance` cell.

**SN-001**

> `need` — *"An adopting team can add this process to a new or existing
> repository and get a working gated, requirement-traced process, without
> hand-building the tooling."*
>
> `acceptance` — *"A single scaffolding action against a destination repository
> produces a scaffold whose harness runs green out of the box; a re-sync onto an
> existing repo never clobbers the repo's own files."*

**SN-002**

> `need` — *"A reviewer can trust the chain from need to requirement to design
> to test because it is **mechanically verified**, not manually asserted."*
>
> `acceptance` — *"The strict traceability check reports **zero orphans** across
> the joined `SN→SR→LLR→TC` spine; a malformed/duplicate id fails at any stage."*

In both rows the need is stated about a **person** and the acceptance is stated
about a **machine reading**. Between them sits a claim:

- *a green scaffold* ⟹ *that team has a working process*
- *zero orphans* ⟹ *a reviewer trusts the chain*

Those claims are load-bearing, contestable, and **written down nowhere**. The
second one is plainly falsifiable: a spine can be orphan-free and semantically
vacuous. Every row can resolve while every row says nothing. That is not a
hypothetical failure mode — it is the exact worry that opened this review
(*"most of the tooling technically works, but I want to make sure the process
works"*), and the reason it is hard to answer is that the repo has no artifact
in which the question can even be posed.

**The shape of it, counted:**

| tier | rows | stated about |
|---|---|---|
| SN | 16 | a human outcome — 15 of 16 say "can trust", "can believe", "can navigate", "can recognize", "an adopting team can add" |
| SR | 79 | the package and its interfaces |
| LLR | 192 | modules |
| TC | 194 | the package and its interfaces |
| **assumptions bridging SN and SR** | **0** | — |

All 79 SRs carry `boundary_refs`, and the distribution is stark:

```
69  B-05           THE TEMPLATE — the packaged deliverable
 5  B-01, B-04     governed writes in / guardrail verdicts out
 3  B-02           authority in
 1  B-04
 1  B-02, B-05
```

**87% of this repo's system requirements are stated at one crossing: the moment
the package leaves.** But nothing the package *does* for anyone happens there.
It happens where a person operates the adopted kit. In today's frame that person
sits inside `EXT-003` (Adopter), which can only be reached across `REL-001`. The
registry defines that relationship as *"external-to-external, the system NOT a
party"*, and says it *"must never grow a realizing IF row."*

**So the crossing where this kit's stakeholder value lands was ruled outside the
frame.** Not by accident — the reasoning in `REL-002`'s and `B-04`'s notes is
careful and defensible on its own terms. The present frame is a **delivery**
frame, and delivery is not where any effect happens. The consequence is that
there is nowhere for validation to attach, which is why there are 194 test cases
and all 194 of them test the machine. §5 redraws the frame so that there is.

---

## 2. Why this is not a documentation gap

The formal statement is Jackson and Zave's, and it is worth stating exactly
because it tells you how many things you are obliged to test.

- **R**, the requirement, is stated over **world phenomena** — including
  phenomena the system cannot observe ("a reviewer trusts it").
- **S**, the specification, is stated **only over shared phenomena** — those
  visible at the system's own interface ("zero orphans").
- **W**, the domain assumptions, bridge the two.

The obligation is the entailment:

```
S  ∧  W  ⊨  R
```

**Testing only S tests one term of three.** W is not a soft artifact or a
rationale; it is a premise the argument depends on, and a false W makes a
perfectly verified S deliver nothing. The kit currently verifies S to a high
standard, states R honestly at the need tier, and leaves W entirely implicit.

The practical consequence is the one that motivated this proposal: **the cost of
iteration scales with the size of the W gap.** If the only way to learn whether
the system delivers R is to run the whole world, every corner case costs a full
validation cycle. If W is written down, most corner cases can be produced and
caught against W instead — cheaply, continuously — and the expensive R-level
probe is reserved for sampling whether W itself still holds.

---

## 3. Where W comes from — two sources

W attaches wherever seeing the exchange does not settle whether the outcome was
achieved. There are two independent ways that happens:

| axis | question | if "no" |
|---|---|---|
| **observability** | can the system, or something built to watch it, detect that the crossing happened? | the crossing is `effect`; W bridges to it |
| **determinism** | does the far side *compute*, or *interpret*? | seeing the crossing does not tell you it was right; W covers the interpretation |

**Observability** is Jackson's shared-phenomena test, and it is what the `frame`
column (§4) records:

> A crossing is `design` if the system, or a rig built to observe it, can
> detect that it happened. It is `effect` if the need names an outcome there
> that nothing built can see.

**Determinism** is the oracle problem (Barr et al. 2015). A seam facing a model
is fully observable: the system sees the call, what it sent, and what came
back. None of that says the answer was right, because the far side interpreted
rather than computed. So a crossing can be `design` and still carry W.

The set of phenomena a requirement names that the system cannot observe is
therefore a countable **lower bound** on the V&V gap, not the whole of it.

It is also not a small corner. `interfaces.toml` holds 167 rows, and the
external parties they name are:

```
41  external:downstream     the adopting team - interprets
 5  external:               (unqualified)
 4  external:git            computes
 4  external:agent          the model runner - interprets
 3  external:run            computes
 1  external:upstream
```

Roughly **45 of 167 seams (~27%) face a far side that interprets.** Not
universal, but far more than the ~16 need-level assumptions alone would suggest.
That count prices §7(a).

---

## 4. Naming — the `frame` column

The formalism's own nouns, "machine" and "world", are precise inside Jackson and
drift badly outside it. "Machine" reads as *hardware* to hardware people, and
"world" slides to "environment" and then to "deployment environment" within
about two documents.

**Keep R / S / W as the cited formalism, and name the *crossings* instead**,
since crossings are what the registry holds. A closed vocabulary on the boundary
row:

```toml
frame = "design" | "effect" | "coincident"
```

- **`design`** — the system can observe and act here. Instrumentable.
  **Verification** lands here.
- **`effect`** — where the outcome the need names actually occurs. Frequently
  *not* observable by the system. **Validation** lands here.
- **`coincident`** — the two are the same crossing at this point, stated
  deliberately.

Why this shape:

1. It keeps **"design"** for the side the system has authority over, and the
   repo already reasons in exactly that word: `B-04`'s note rules a crossing out
   because *"this system holds no **design authority** over whether an external
   runner honours the workflow it is handed."*
2. **`effect`** generalizes past humans — peer systems, physical outcomes,
   downstream repos — where "experience" does not.
3. **`coincident`** makes the collapse case a *stated claim* rather than an
   omission, which is this kit's standing doctrine that an empty cell should
   assert nothing. A CLI where the token the user types is the token the parser
   reads genuinely is coincident; saying so costs one word and is reviewable.
   Ordinary software crossings will reach for it often, and that is fine.

Coincidence could in principle be *derived from topology*: a crossing running
straight from an external entity into the design would be coincident. That is
not adopted. A derived value would assert something nobody wrote, and
differentiating is worth the word.

**`frame` records a position, not a property.** Observability depends on what
has been built to watch a crossing, so a row can **move** from `effect` to
`design` when someone builds a rig (§8). That makes the column a measure of
instrumentation coverage instead of a permanent verdict, and makes *"we moved a
crossing into the design frame"* a reportable result. The price: moving a row
does not delete its assumption, it **replaces** it with a fidelity assumption
that has to be written down.

### The candidates, assessed

| candidate | verdict |
|---|---|
| `machine` / `world` (Jackson, Zave) | Citable and exact. Keep in the rationale; reject as the shipped noun for the reason above. |
| `solution domain` / `problem domain` | Established, but the cut is wrong — the problem domain is the whole problem context, not the place the outcome lands. |
| `system-of-interest` / `operational environment` (ISO/IEC/IEEE 15288:2023) | The strongest *established* pair, and normative. But both name **systems**, and what is typed here is a **crossing**. Keep 15288 as the citation for the system-level split and for the enabling system (§8). |
| `ODD` — operational design domain (SAE J3016, ISO 21448, UL 4600) | **Adopt, for a different cell**: the assumption row's `holds_when` (§6). |
| `design system` / experience | **Unusable.** In software, "design system" means a UI component library (Material, Carbon, Polaris, Fluent). The instinct behind it survives as `design` / `effect`. |
| `design boundary` / `experience boundary` | No collision, weak currency. "Experience" is human-centric, which is wrong for a kit that also ships to physical projects (`CMP.category = "physical"` exists today). |
| `control` / `effect` | Both real usage. "Control" collides with control theory *and* with this repo's own `B-02` authority crossing. |

---

## 5. The frame, redrawn as the operating frame

### 5.1 The orientation

The frame used to be oriented toward the system as **the entire package that
developed the product**. That is still partly true. It is now oriented toward
**the system the user experiences, as well as the enabling system that develops
and delivers it.** The normal operating environment is an adopter's repo.

The change does less damage than "redraw the depth-0 frame" suggests. **`B-05`
does not go away, and the 69 SRs stated at it are not re-pointed.** The package
still leaves the system. What changes is that its departure stops being the
*only* modelled crossing and stops being the one the stakeholder needs are read
against.

### 5.2 Two planes, which `class` already separates

| plane | classes | holds |
|---|---|---|
| **operating** — what the user experiences | `operational`, `interoperating` | the human operator, the session, the real model provider |
| **evolution** — ours, not experienced | `deliverable`, `enabling` | the Template, the rigs, the delivery path |

The frame has never been purely "who is outside". `EXT-002` (Template) is
`deliverable`, an *output* rather than a party, and its note records that the
class was *"an ADDITION to the class vocabulary"* because the outward-facing
three did not fit. The evolution plane has simply been half-populated. Its note
also records the relativity this proposal relies on: *"From an adopter's frame
this package is their enabling system."*

An enabling system is normally something the developing organization **owns**.
That is what the class is for in 15288. So an in-tree rig is an `EXT` row with
`class = "enabling"`: being built here does not keep it off the frame.

### 5.3 The human's two edges

The human interacts with **the development session** (really just a computer)
*and* with the system. Both edges already exist in the frame:

| edge | what it is | existing row |
|---|---|---|
| human → **session** → system | the mediated path: the human edits a cell, the computer writes it, the hook floor admits it | `B-01`, governed writes in |
| human → **system** | the direct path: the human's *judgment* — rulings, attestations, Status flips | `B-02`, authority in |

`B-02` is the crossing `interfaces.toml` singles out:

> *"ONE CROSSING IS DELIBERATELY REALIZED BY NOTHING: `B-02` (authority in —
> rulings, attestations and Status flips) **has no port of its own.** Authority
> enters as CONTENT on B-01's write path: a human edits a Status cell and
> commits, and the hook floor admits that write as it admits any other."*

Under §3's test, the system can observe *that a Status cell changed*. It cannot
observe *that a human judged*. Only the proxy is shared.

> **`B-02` is this repo's first `effect` crossing, and its "realized by nothing"
> status is what an effect crossing looks like from inside a design frame.**
> Ports are design-frame objects, and authority is not a design-frame phenomenon.

Its first assumption row is one the gate machinery already depends on:

```toml
assumption = """A changed Status cell means a human actually exercised the
                judgment that Status asserts."""
```

That is what `Attest` and the attested-vs-mechanized split exist to protect,
stated for the first time as something falsifiable. It is also why the human has
to come out of `EXT-001`: left folded in, this repo would have no `effect`
crossing at all, and the model would be correct and inert here.

On the inside, the two edges land on components that already exist: `CMP-006`
*"W1 Registry & conformance"* (write, via the session) and `CMP-009` *"W4 Human
& adopter surfaces"* (read, directly). What is missing is only that the derived
view does not yet connect a depth-0 crossing to the component that serves it.

### 5.4 The adopter is dropped

`EXT-003` was *"the downstream team + repo"*. The operating frame already splits
that pair: **the team is the human operator**, and **the repo is the operating
environment the frame is drawn in**. Nothing is left for a third row to name.

- **`REL-001` collapses into `REL-002`.** `REL-002` (Template → `EXT-001`) is
  already the adoption edge, drawn from the operating side. Its flow reads
  *"this repository's own session adopts the same delivered content"*, and its
  note says the workflow is adopted *"exactly as an adopter's would be."* With
  the adopter gone, `REL-001` would state the same hand-off twice.
- **The value §1 located across `REL-001` now lands on `B-01` and `B-02`**, the
  human operator's own crossings, which are crossings of the system.
- **`EXT-003` is spent and never re-minted**, following the
  `B-06`/`B-07`/`EXT-004` precedent in `external.toml`.

### 5.5 The proposed frame

The boundary view is **derived**: `gen_trajectory.py` builds the System-context
view from `external.toml` (`context_block(frame_context(root), ...)`, WI-455).
**Editing rows is editing the diagram.** There is no second artifact to keep in
sync.

| row | change | plane |
|---|---|---|
| *new* Human operator | **add**, `operational`; owns `B-02` (`frame = "effect"`) | operating |
| `EXT-001` Development session | **narrow** to the computer: shell, editor, OS, git client, working copy; owns `B-01` | operating |
| `EXT-005` Model provider | unchanged; gains an inbound `emulates` from its rig | operating |
| `EXT-002` Template | unchanged | evolution |
| `EXT-003` Adopter | **dropped** (§5.4) | — |
| *new* Scripted model runner | **add**, `enabling`, `emulates = "EXT-005"` | evolution |
| *new* Scaffold rig | **add**, `enabling`; emulates a fresh operating environment, not a party | evolution |
| test infrastructure | **not shown** — inherent to defining a system, not a frame element | — |

`EXT-001` is the largest edit. Its description today folds in *"shell, git
client, OS, Python, editors, test runner, LLM runners"*: the human, the
environment, the test infrastructure **and** the model runner in one row.

**Count changes:** entities 4 → 6, relationships 3 → 2, crossings unchanged, and
`B-02` gains an owner. No SR's `boundary_refs` is re-pointed. Costs are in §9.3.

---

## 6. The assumption row

### 6.1 Why rows, not cells

The strongest objection is that translation is everywhere. A person operates a
computer, the computer turns intent into registry cells, and even an `IF` row
facing an LLM assumes a non-deterministic judgment on its input. So why not
widen the boundary definition to say what it assumes about an ambiguous far
side?

Two reasons, either sufficient:

1. **W needs an id so that W-evidence can be counted separately from
   S-evidence.** `Verifies` takes ids, not cells. If a W-test cites the boundary
   instead, a TC checking the crossing's *contract* and a TC checking its
   *assumption* become indistinguishable. The three obligations in §7 collapse
   into one counter, and §1's finding (*194 test cases, all of them testing the
   machine*) can no longer be stated.
2. **Pervasiveness argues *for* rows.** As a cell, the claim *"the far side
   interprets, so its output needs judgement rather than comparison"* would be
   written ~45 times (§3). The copies would drift, each would need its own
   falsifier, and none could be narrowed in one place. One row with one status,
   one `holds_when` and one falsifier, cited by 45 seams, is PROCESS.md §3's
   0→A→B rule applied to W.

### 6.2 The row, and where it lives

A fourth row kind in `external.toml`, beside the three it describes:

```toml
[assumption.DA-###]
bridges_to   = "EXT-###"       # the effect side — where R lands (Human operator)
realized_by  = "IF-###"        # OPTIONAL. Present = a rig performs the bridge.
                               #           Absent  = a translation, a pure claim.
assumption   = """A scaffold whose harness runs green is one an adopting team
                  can actually work in: the profile fits their stack, and the
                  registries they must fill are discoverable without reading
                  the kit's source."""
holds_when   = """The team's stack is one of the shipped profiles, and the team
                  reads ADOPTING.md before first use."""
obstacle     = """A team green-scaffolds, never fills a registry, and operates
                  a spine that resolves and says nothing."""
falsified_by = "TC-###"        # the signal that would show this is false
status       = "Drafted" | "Approved"
```

The **seam cites the assumption**, the way an SR cites `boundary_refs`:

```toml
[boundary.B-05]
frame    = "design"
rests_on = ["DA-001"]          # the assumptions this crossing's claims need
```

So the `DA` row does not re-declare an edge the `B` and `IF` rows already hold.
It carries only what the seam does not know: the effect side, the ODD, the
obstacle and the falsifier.

`realized_by` copies an idiom already in `interfaces.toml`: a row with neither
`interface_from_external` nor `interface_to_external` *"is an internal seam,
and that ABSENCE is the statement."* A `DA` row with no `realized_by` is a pure
claim, and says so by omission.

Three cells are borrowed, each with a standard behind it:

- **`holds_when` is an ODD.** SAE J3016 / ISO 21448 / UL 4600 call the declared
  region within which a claim is asserted the *operational design domain*.
  Naming it after the established concept brings the **restriction move** with
  it (§7(d)).
- **`obstacle` is van Lamsweerde & Letier's obstacle**: the negation of a goal,
  requirement **or assumption**, refined until it reaches conditions satisfiable
  in the domain. It is a *generator*, not a comment (§7(b)).
- **`falsified_by` is the falsifier.** REAssuRE's monitored **claims** (Welsh,
  Sawyer & Bencomo, ASE 2011) and UL 4600's **Safety Performance Indicators**
  converge on it. The rule both imply is worth adopting outright, as a
  warn-first `trace.py` finding:

  > **An assumption with no declared falsifier is an untested assumption.**

**Why `external.toml` and not a new file** (costed in §9.2): the file already
holds three row kinds *"because they are one statement"*. An assumption is a
fourth statement about the same frame, approved by the same authority and
changed only by ruling. Putting it there skips a new registry file and a new
stage predicate entirely.

### 6.3 Which assumptions become rows

*"The computer turns the user's keystrokes into registry cells"* is true, is an
assumption, and should obviously not be a row. The stopping rule:

1. **The obstacle test.** An assumption earns a row when you can write a
   **non-silly `obstacle`** for it. If the negation is not a failure mode anyone
   would plan against, there is no row. *"The keyboard emits characters other
   than those pressed"* fails. *"A team green-scaffolds and operates a spine that
   says nothing"* passes.
2. **The interpretation trigger.** Wherever the far side interprets rather than
   computes (§3), *suspect* an assumption. This says where to look; it does not
   mean every such seam yields a row.

Behind both sits NASA-STD-7009's rule: **credibility proportional to the risk of
the decision the evidence supports.** The keyboard assumption carries no decision
risk. The scaffold assumption carries all of SN-001's.

### 6.4 Writing a good one

Two rules, one from each side:

- **An over-strong W is a defect, not safety.** In assume-guarantee reasoning
  the environment assumption can be *synthesized* as the weakest condition under
  which `S ⊨ R` (Cobleigh, Giannakopoulou & Păsăreanu, TACAS 2003). An
  assumption written broadly enough to make the entailment trivially true has
  moved the problem, not solved it. Authoring guidance, not a mechanism.
- **For a rig, state the delta, not the resemblance.** A rig stands at *"the
  same interface (or nearly the same)"* as the party it replaces. The *nearly*
  is the fidelity assumption. If the rig matched exactly, the row would be
  vacuous.

| weak — states the resemblance | strong — states the delta |
|---|---|
| *"the contact model grips like the real gripper"* | *"the contact model omits deformation and stick-slip; above ~X N the sim over-reports grip"* |
| *"the fake runner behaves like a model CLI"* | *"the fake runner reproduces argv/stdin, exit codes and commit effects; it reproduces no judgment, so nothing about prompt quality is evidenced here"* |

The right-hand column is falsifiable, bounds its own ODD, and tells a reader what
the rig does **not** cover. `obstacle` and `falsified_by` hang off it naturally.

---

## 7. Three test obligations, and why they are affordable

If the argument is `S ∧ W ⊨ R`, evidence is owed on three fronts. The kit
currently collects one.

| # | verifies | where evidence sits | cost | cadence |
|---|---|---|---|---|
| **1** | **S** | the design crossing | cheap | every commit — *this is all 194 TCs today* |
| **2** | **W** | the assumption itself | cheap-to-moderate — *free where it is a metamorphic relation, (c)* | continuous |
| **3** | **R through W** | the effect crossing, via a translation or a rig | expensive — *a rig splits the cost rather than removing it (§8.2)* | sparse, sampled — *see the limit below* |

Obligation **2** is the new one and the important one. Tests of W are often not
software tests at all: they are measurements, monitors, sampled observations, or
a recorded check that a stated precondition still holds. For SN-001's
assumption, a W-test is *"take a shipped profile, scaffold it, and have someone
who has not read the source reach a first filled registry"*. It is not cheap,
but it is enormously cheaper than validating "an adopting team gets a working
process", and it fails in the same direction.

Obligation **3** is validation proper, and expensive by nature. The point is not
to make it cheap but to make it *rare and targeted* by putting obligation 2
underneath it.

The mechanisms that make this affordable, in the order they matter:

**(a) The probe count is bounded by the assumptions, not by the input space.**
Sampling R directly is unaffordable because R lives over the world. Sampling W
bounds the work by the number of assumptions written down, not `2^n` over an
input space. That is why W has to be rows, not prose. The number is larger than
the ~16 need-level assumptions (§3 counts ~45 interpreting seams), so shared
rows (§6.1) are what keep it bounded.

The same allocation rule is normative in aerospace structures as the
**building-block approach**: FAA AC 20-107B requires tests "at the coupon,
element, details, and subcomponent levels", and CMH-17 Vol. 3 states the
reasoning — **run many cheap low-level tests to bound variability so that very
few expensive high-level tests can be justified.** It is a cost argument, not a
thoroughness argument. Many cheap W-tests buy the right to run few R-probes.

**(b) Corner cases are generated, not imagined.** Each `obstacle` mechanically
yields at least one adversarial case: *what if this does not hold?* The corner
cases come out of the assumption set by construction.

**(c) Some W is executable, at ordinary CI cost.** A **metamorphic relation**
(Chen, Cheung & Yiu, 1998) is a necessary property across *multiple*
executions, which tests without knowing any single correct output. It is the
standard answer to the oracle problem, and it is used at world boundaries with
no oracle at all (*Metamorphic Testing of Driverless Cars*, CACM 61(3), 2018).
Most useful MRs are statements about the world — *"adding an unrelated registry
row must not change an unrelated row's status"* — so **writing an MR is writing
a testable domain assumption.** Try it first for any new W row.

**(d) Narrowing the declared world is a legitimate answer.** SOTIF (ISO 21448)
treats *"unknown unsafe"* as the area to shrink, and sanctions two responses to
a gap: improve the system, **or restrict the ODD**. When `S ∧ W ⊨ R` will not
close, narrow `holds_when` until it does, and say so. That turns an unbounded
obligation into a bounded one plus an honest exclusion, and it is likely the
right response for a small team. *"The team's stack is one of the shipped
profiles"* is exactly such a restriction.

**(e) Evidence declares how close to validation it sits.** The `Verification`
vocabulary (`Test | Demonstration | Manual | Analysis | Inspection | Attest |
Critique`, `trace.py:526`) names the **method**. Nothing names the **distance
from the effect boundary**, and the two are orthogonal. The descriptor is the
three-value `assumed | sampled | monitored`. The escalation path, if a project
needs more, is NASA-STD-7009B's Credibility Assessment Scale: eight factors
scored 0–4, with required credibility **proportional to the risk of the decision
the evidence supports**.

### The limit on sparse sampling

Sampling the human axis sparsely gives a **high-variance lower bound on
discovery, not a coverage claim.** Nielsen's "five users" is practice, not
evidence: Faulkner (2003) resampled from 60 users and found random 5-user sets
caught anywhere from **55% to 99%** of known problems; n=10 lifted the floor to
80%, n=20 to 95%. Schmettow (2012) shows discovery is over-dispersed.

So sparse R-level probes are worth running and their *findings* are real, but
**a passed sparse probe is not evidence that a W row holds; only a failed one is
evidence that it does not.** The same holds for a green run against a rig. Any
rule the kit writes must say so, or it manufactures the false confidence this
proposal exists to remove. The weight sits on (b), (c) and (d); (a) buys
targeting, not assurance.

There is no standard for the credibility of a *human* model comparable to
NASA-STD-7009 for physics models. If a human-axis assumption is load-bearing, the
honest options are to restrict the ODD or accept a recorded risk, not to claim a
model covers it.

---

## 8. Enabling systems and rigs

### 8.1 Enablement, and where verification sits

Every design has **enabling systems**: under design control, not shipped, not
what a user experiences. In 15288 an enabling system supports the
system-of-interest during one or more **life-cycle stages**, and deployment is
the enabling system for the **Transition** process (installing into the
operational environment). The kinds fall out of the stage axis:

| kind | stage it enables |
|---|---|
| rig | Development — Verification/Validation specifically |
| test infrastructure | Development |
| deployment / delivery | **Transition** |
| procurement, warehousing | Production, Support |

Stage does not decide which things carry test cases, so it is a taxonomy, not a
gate. Keep `enabling` as the class, and take *Transition* if a standard word is
wanted for deployment.

**Verification sits outside this classification, not inside it.** Every
enabling system needs verification around it, not only the product. This repo
is the proof: `tests/` verifies the harness, and CLAUDE.md traces `tests/` as
product. Three independent axes:

| axis | applies to | recorded as |
|---|---|---|
| **is it verified?** | *everything*, product and every enabling system alike | ordinary tests |
| **does it discharge a spine requirement?** | whatever a requirement is written about | a TC with `Verifies` |
| **does it stand in for something else?** | rigs only | an `emulates` cell and a `DA` row's fidelity claim |

Only the third makes a rig a rig. Everything gets tested; not everything earns a
row in the traced spine.

The split is **frame-relative**. This kit's product *is* test infrastructure, so
what would be supporting enablement elsewhere is shipped product here. Auxiliary
is a role relative to a declared system-of-interest, not an intrinsic property,
which is what `EXT-002`'s note already says.

### 8.2 Translation and rig: one construct at two weights

```
effect  <->  translation | rig  <->  boundary interface  <->  design
```

- A **translation** converts an effect into a design boundary by *claiming* the
  conversion holds. It is a `DA` row alone.
- A **rig** converts it by *performing* the conversion: simulating the effect
  and putting the output against a rubric. It is a `DA` row with `realized_by`.

A rig **is not the external party. It stands at that party's crossing.** It
presents the interface the party presents, so a rubric run there is a rubric run
on the interface the user acts through, which is why rig evidence counts toward
validation and not only verification. The registry already has every piece:

| | recorded as |
|---|---|
| the real party | `[entity.EXT-###]`, operating plane |
| the rig, as a system | `[entity.EXT-###]`, `class = "enabling"`, `emulates = "EXT-###"` — evolution plane |
| the rig at the crossing | an `IF` row with `interface_from_external` / `interface_to_external` tying back to the existing `B-##` |
| its fidelity | a `DA` row with `realized_by` naming that `IF` row |

Rigs realize crossings that already exist, so they add entity rows but **no
`B-##` rows**.

**What a rig buys.** It does not make the real phenomenon observable. It makes
a *model* of the world observable, so W is **replaced**, not removed:

| the assumption before the rig | the assumption after |
|---|---|
| *"zero orphans ⟹ a reviewer trusts the chain"* | *"a model judging the rendered artifact against rubric R judges as a human would"* |
| *"this current curve ⟹ the apple is gripped"* | *"the contact model grips like the real gripper does"* |

The left column is untestable in principle. The right is a **fidelity**
assumption: bounded, stated, and testable by calibration. The exchange rate is
good because the product changes every commit and the rig changes yearly.
Obligation 3 **splits**: cheap and continuous against the rig, expensive and
sparse against the rig's fidelity. In the building-block terms of §7(a), the rig
is the element level.

Two instances, one from each end of the span the kit claims:

- A UI requirement's effect is *"the panel reads clearly."* Render the pixels
  and hand them to a vision model against a rubric, and legibility becomes an
  observable event. Suites stop at the DOM because they were designed when no
  judge existed downstream of the pixels, and the convention outlived the
  constraint.
- A manipulation requirement's effect is *"the apple is gripped."* A simulated
  arm with a contact model makes *grasp succeeded* observable, and variance in
  mass, friction and pose can be injected far more cheaply than it can be staged.

### 8.3 The emulation edge

The relation between a rig and what it stands in for is an identity claim
between two entities, not a crossing. So it is **one cell on the rig's row**:

```toml
[entity.EXT-###]
name     = "Scripted model runner (rig)"
class    = "enabling"
emulates = "EXT-005"
status   = "Approved"
```

From that cell the derived view can draw the rig in the evolution plane, dotted
or tinted, with a dotted edge to `EXT-005`. It can also mark `EXT-005` as
*"has a maintained virtualized counterpart"* by reading the inverse, with no
second cell. Whether `context_block` learns to draw this is a dashboard question
and does not hold up the frame decision: the rows are true before the view can
render them.

`emulates` also anchors the fidelity assumption. **A rig row with `emulates` and
no `DA` row** is a virtualized component whose fidelity nobody has stated: a
warn-first `trace.py` finding that fires on the rig's existence.

### 8.4 The rigs this repo already runs

**The scripted model runner.** `FAKE_AGENT` (`tests/test_agent_loop.py:34`)
records each invocation and the model it was handed, then performs the next
action from an `actions.txt` script (`commit` / `done` / `blocked` / `noop`).
**It simulates `EXT-005`'s protocol, not its judgment**, and that is the right
split: a model good enough to stand in for a model is circular. The split
belongs in its `DA` row as the delta (§6.4).

**The scaffold rig.** `tests/conftest.py:1-7`: *"The tests exercise the scripts
the way a downstream user would: bootstrap a real scaffold in a temp dir and run
the actual commands."* Materializing the package is `B-05`, ordinary
verification of an output. The *second* half is the rig: running the adopted
toolkit in a synthetic repo and judging that it comes up green, which emulates a
fresh operating environment. SN-001's acceptance is written at exactly that far
side.

This was the evidence that decided the old `REL-001` question. The registry's
own rule — *"a relationship ... must never grow a realizing IF row. **Wanting one
means what you have is a boundary crossing**"* (`external.toml:20-22`) — and a
rig that had been standing at `REL-001` since before the frame was drawn could
not both hold. Dropping the adopter (§5.4) resolves it: the scaffold rig
emulates the operating environment, which is an entity, not a relationship.

**The render rig.** `render-dashboard-critique` screenshots `PROJECT_STATE.html`
across a declared width/theme/tab matrix so a critique judges pixels, not ~790 KB
of markup. The critique contract in `PROCESS_OPTIONS.md` already makes a
perceptual TC name its **artifact recipe** beside its rubric, and
`llm-vision-convergence-loop` requires two consecutive approvals at one content
hash. That is a rig, a declared ODD and a repeatability control, with **no
assumption row behind any of them.**

It also answers *"a rendered panel changes easily, so what happens to its test
case?"* **The TC pins the rubric, not the pixels**, and the contract rules that
the rubric derives from the SN/SR intent, never from the TC. A redesign re-runs
the judgment instead of invalidating the case, and the lax-TC ratchet fires if a
CHANGES-REQUESTED round closes with no change to TC prose, test logic, or
rubric.

What nothing does today is treat **the judge** as an assumption. No check
notices when a model revision silently shifts what the critic approves. The most
dogfoodable row in the proposal:

```toml
[assumption.DA-###]
bridges_to   = "EXT-###"     # Human operator
realized_by  = "IF-###"      # the render rig at its crossing
assumption   = """A vision model judging the rendered dashboard against the
                  rubric reaches the verdict a human reviewer would."""
holds_when   = """The model is image-capable; the rubric carries its accumulated
                  anchors; the artifact is a static render at a declared
                  width/theme."""
obstacle     = """A model revision shifts judgment silently; or the rubric
                  overfits to anchors accumulated under one model's eye."""
falsified_by = "TC-###"      # a periodic human Attest sample that disagrees
status       = "Drafted"
```

It does not claim a model covers the human axis (§7's limit rules that out). It
states the claim, bounds it, and names the sample that would refute it.

### 8.5 The self-derivation limit

This repo cannot dogfood its own development scripts: executing the scripts
being modified has repeatedly failed to give a usable result. The general rule:

> **A rig derived from the system under test cannot falsify assumptions the two
> share.**

Self-execution is the limit case: the rig *is* the system, the shared set is
total, and it can falsify nothing. It is also why `FAKE_AGENT` has the right
shape: a scripted stand-in that does not run the real thing shares no
assumptions with it. A rig *"derived by the system itself"* is cheap and buys
correlated blind spots. This extends CLAUDE.md's existing self-application
boundary (*"no product launch"*) rather than contradicting it.

---

## 9. Impact

Surveyed against the code on 2026-09-20, not estimated. Anchors are given so
the next session can start from them.

### 9.1 The precedent for letting a TC verify an assumption

**A TC may already verify an off-spine id.** `Verifies` accepts `SR` / `LLR`
**and `IF-###`** (`coherence.py:73-108`), on the constraint that a seam citation
**supplements** a spine citation: *"a TC naming only seam ids no longer says
which requirement it discharges."* There is a migration allowlist
(`docs/if-tc-coverage-allow`, 118 entries) and an `if_tc_coverage_findings`
check that warns, then errors under `--strict` at DevStg-Tests+.

If a W-test supplements, `DA-###` is a second tenant in that mechanism. If it
may stand alone (Q5, §11), the precedent does **not** transfer, and the
supplement rule needs a deliberate exception. That cost is not yet surveyed.

### 9.2 Why the rows belong in `external.toml`

A **new registry file** costs **13 mandatory edits**, including a new
`kitlib/ladder.py` rung, a `spine_rules` predicate, a `DECLARED_INPUTS` entry, a
`bootstrap.MAPPING` entry, an `_offspine_ids` watermark and a
`test_dogfood_sync` floor. The ladder rung is *"the largest single ripple"*: it
reaches `check.py` stage selection, every `from-stage` in `stack.ini`,
`check_vocab.py`, the `gate-advance` skill and three test modules.

`external.toml` **skips five of those outright**:

- `kitlib/stage.py:144` already lists it in `DECLARED_INPUTS`, so the stage
  fingerprint covers new rows for free. (The opposite case is a real hazard: an
  undeclared registry leaves `derive_stage --check` green over a changed file.)
- `bootstrap.MAPPING` already scaffolds it.
- `baseline_snapshot` already lists it in `SNAPSHOTTED` / `SNAPSHOT_TIERS`.
- No new ladder rung, no new `spine_rules` predicate.
- `test_dogfood_sync.TOML_REGISTRIES` is keyed by **ID column, not path**
  (`:246-252`), because `external.toml` already carries three tiers on one path.

### 9.3 The edit list

**(a) `frame` column on boundary rows — 4 mandatory edits**

| # | File | What |
|---|---|---|
| 1 | `kitlib/spine.py:651` | add the key to the `B-ID` tuple (schema of record) |
| 2 | `registries/external.template.toml` | add the key to `[boundary.B-000]` |
| 3 | `spine_carrier.py` `OFFSPINE_COLUMN` | key → `Frame` |
| 4 | `migrate_carrier.py` `KEY` | the exact inverse — `test_rule_sync.py:700-712` asserts both maps invert **and match in length** |

Then behaviour: `trace.py:526+` `ENUM_FIELDS` for the closed vocabulary (the `B`
tier's enums ride the **advisory** pipe, so a bad value warns and never fails —
`test_external_frame.py:371`), and the five live rows. `rests_on` follows the
same four-edit path.

**(b) `[assumption.DA-###]` row kind — 8 mandatory edits**

The four above, plus `OFFSPINE_KEYS` (new `DA-ID`), `OFFSPINE_TABLE`
(`"DA-ID": "assumption"`), a `TOML_REGISTRIES` entry **and** its floor
(`test_dogfood_sync.py:433` asserts `set(floors) == set(TOML_REGISTRIES)`), and
`trace.py:920-928` `_offspine_ids` for the id watermark. The watermark is not
optional: the missing-watermark hole has happened here twice (IF-121/122 and
OI-26). `realized_by` is one optional key and adds nothing to the count.

**(c) The frame redraw (§5.5) — a sitting**

- `tests/test_external_frame.py:87-114` pins *exactly* 4 entities, 4 crossings
  and 3 relationships plus the spent-id gaps, and `:128-146` pins every `status`
  to `Approved`. Its docstring says it **is expected to be edited by a sitting
  and by nothing else**. The redraw moves entities 4 → 6 and relationships
  3 → 2, adds `EXT-003` to the spent ids, and adds `emulates` to the entity
  schema. Crossings stay at 4.
- `tests/test_hats.py:885-900` names `EXT-003 Adopter` as the entity the
  FIRST-RUN-ADOPTER review hat speaks for. WI-453 re-pointed the hat's predicate
  away from the id, so nothing breaks, but the hat loses its entity and needs a
  new anchor, plausibly the human operator on first run.
- `docs/log.md` and the sitting-2 plan cite `EXT-003` historically. They are
  records and stay as written.

### 9.4 What will actually hurt

**Prose has almost nowhere to go.**

| file | cap | now | headroom |
|---|---|---|---|
| `AGENTS.template.md` | 10,000 | 9,980 | **20 B** |
| `CLAUDE.md` | 8,500 | 7,975 | 525 B |
| `byte-budget-guard/SKILL.md` | 5,000 | 4,613 | 387 B |
| `PROCESS.md` | *watched* | 88,990 | — |
| `PROCESS_OPTIONS.md` | *watched* | 189,535 | — |

`test_bootstrap.py:443+` parses the skill's budget table and asserts each
baseline equals the real file size, **so any edit to a capped file must re-stamp
the skill in the same commit, within 387 bytes.** This concept's prose home must
be `PROCESS_OPTIONS.md` (watched, an expansion home) or `ADOPTING.md` /
`EXAMPLE.md` (unbudgeted), **not** `AGENTS.template.md`.

**Adopters need a resync entry.** `RESYNC_PACK.md` §3 takes a `[since <sha>]`
entry, format-enforced by `test_resync_pack.py:117/210/252`.

### 9.5 Adjacent findings

Not part of this proposal; recorded because the survey found them.

1. **`docs/test/evidence` does not exist in this repo.** It is the sole input to
   `DevStg-Release` (`spine_rules.py:583-592`), so this repo can never derive
   its top rung.
2. **Per-requirement coverage lives in `trace.py`, not `plan_coverage.py`** —
   the `SR → LLR → TC` matrix at `trace.py:5194-5207`. `plan_coverage.py` is the
   dual-plan pre-pass, despite the name.
3. **The SN `priority` vocabulary (`M`/`S`/`C`) and the WI `Priority` integer
   are unconnected.** Nothing maps a Must-need onto queue order. Small and
   separable.
4. **`Permutations` + `gen_cases.py` is a dormant layer, not a live hook** for
   dimensional reasoning. No live SR uses `Permutations`, and
   `test_dogfood_sync.py:515-519` *asserts it stays unused* as the probe for the
   template-drop direction of the drift rule. `gen_cases.py` writes to stdout
   only and has no consumer. Using it means activating it and re-pointing that
   probe first.

---

## 10. Staging

Each step is useful alone, and each later step assumes only the earlier ones.

**Step 1 — type the crossings.** Add `frame` to the boundary schema; set it on
the five `B-##` rows and the template's example rows. **Four edits (§9.3a); no
new row kind, no predicate, no requirement touched, no test re-pinned.** Every
SR is classified for free, and *"which of our requirements can we actually
observe?"* becomes answerable. Executable today, independent of everything
below.

**Step 2 — redraw the frame and record the assumptions.** The sitting: the
§5.5 rows (§9.3c), plus the `[assumption.DA-###]` row kind (§9.3b) and
`rests_on`. Write the W rows for the 16 SNs and for `B-02`. They exist today as
the unstated gap between each `need` and its `acceptance`, so this is
transcription, not invention. Warn-only; nothing gates. Expect this step alone to
surface real defects.

**Step 3 — let test cases verify an assumption.** Allow `DA-###` as a `Verifies`
target (settle Q5 first, §9.1) and add the evidence descriptor (§7(e)). Start
with the metamorphic subset (§7(c)), which is nearly free.

**Step 4 — the warn-first findings.** `trace.py` warns on an `Approved`
assumption with no `falsified_by`, and on a rig row with `emulates` and no `DA`
row (§8.3).

**Step 5 — the gate, if wanted.** `DevStg-Tests` requires every `effect`-framed
SR to reach an assumption, or carry a recorded waiver. **The only step that costs
an adopter anything mandatory; opt-in with an applies-when**, per the
proportionality doctrine.

**Not proposed: a new stage rung.** The recursion already oscillates Reqs↔Arch,
and this concept rides existing rungs.

---

## 11. Decisions and open questions

Owner answers, 2026-09-21 and 2026-09-22. `DECIDED` means the next sitting may
build on it; `OPEN` means it may not.

| # | question | standing |
|---|---|---|
| Q1 | Does the human come out of `EXT-001`? | **DECIDED: yes** (§5.3). The answer widened into the enabling-systems thread (§8). |
| Q2 | Does `REL-001` become a crossing? | **DISSOLVED** by dropping the adopter (§5.4): the value it guarded lands on `B-01`/`B-02`. My reading of the owner's decision to drop the adopter. |
| Q3 | `frame` vocabulary: two values or three? | **DECIDED: three**, keep `coincident` (§4). Deriving coincidence from topology considered and not adopted. |
| Q4 | How heavy is the evidence descriptor? | **DECIDED: `assumed \| sampled \| monitored`**, CAS as the escalation path (§7(e)). Agreement to the cheap option, not a finding that the heavy one was wrong; revisit first if the descriptor starts carrying weight. |
| Q5 | Does a W-test supplement an SR citation, or may it stand alone? | **OPEN, leaning stand-alone.** If so, the `IF-###` precedent does not transfer (§9.1), and that cost is unsurveyed. |
| Q6 | Does a rig's crossing get a `B-##` row? | **DECIDED: no.** A rig is an `enabling` entity with `emulates`, an `IF` row at the existing crossing, and a `DA` row (§8.2). |
| Q7 | Does this ship downstream in v1? | **DECIDED in principle: yes**, once Q5 and the sitting have nailed down the details. |
| — | The frame's orientation and the adopter | **DECIDED:** operating frame, two planes; `EXT-003` dropped (§5). |
| — | Enabling-system stage vocabulary | **Tentative.** Placed, not settled (§8.1). |

### Still not captured

Recorded so this section is not mistaken for closure.

1. **Blast radius.** If 41 seams cite one assumption and it is falsified, 41
   seams are affected at once. A shared `DA` row makes that coupling invisible,
   the way a shared dependency does.
2. **Chained assumptions.** The user → device → registry → tooling chain is a
   chain of assumptions. Jackson takes `W` as a flat conjunction and says nothing
   about depth.
3. **Interpretation is graded; the frame treats it as binary.** Constrained
   decoding against a JSON schema is far more deterministic than free-prose
   critique, and the kit ships `structured-output-contract` specifically to move
   a seam along that axis. The frame cannot record that a seam was **hardened**.
   The most actionable of the four.
4. **The trusted translating layer.** Non-rig equipment performs translation all
   the time and is simply trusted. It probably needs no home in the frame, but
   "probably" is not yet an argument.

**Verify before ruling.** The 15288 definition of an enabling system, its stage
list and the Transition process name are given from knowledge, not from the text.
Check them against the 2023 edition before citing any of it in a ruling.

---

## Appendix — sources

Load-bearing citations, so a later reader can check the argument rather than
take it.

| # | Source | What it supplies |
|---|---|---|
| 1 | Zave & Jackson, *Four Dark Corners of Requirements Engineering*, ACM TOSEM 6(1), 1997 | R / S / W and the entailment `S ∧ W ⊨ R` |
| 2 | van Lamsweerde & Letier, *Handling Obstacles in Goal-Oriented RE*, IEEE TSE 26(10), 2000 | obstacle analysis as the W test-generator |
| 3 | Welsh, Sawyer & Bencomo, *Towards Requirements-Aware Systems* (REAssuRE), ASE 2011 | design-time assumptions as monitored **claims** |
| 4 | ANSI/UL 4600, *Evaluation of Autonomous Products* (Koopman) | Safety Performance Indicators — a falsifier bound to one claim |
| 5 | ISO 21448 (SOTIF) | known/unknown × safe/unsafe; **ODD restriction** as a sanctioned response |
| 6 | SAE J3016 | the ODD concept and term |
| 7 | NASA-STD-7009B, *Standard for Models and Simulations* | Credibility Assessment Scale; credibility proportional to decision risk |
| 8 | FAA AC 20-107B; CMH-17 Vol. 3 | the building-block pyramid as a **cost-allocation** rule |
| 9 | Chen, Cheung & Yiu, *Metamorphic Testing*, HKUST-CS98-01, 1998 | MRs as oracle-free necessary properties |
| 10 | Barr, Harman, McMinn, Shahbaz & Yoo, *The Oracle Problem in Software Testing*, IEEE TSE 41(5), 2015 | why validation is expensive: no oracle at the world boundary |
| 11 | Faulkner, *Beyond the five-user assumption*, Behav. Res. Methods 35(3), 2003; Schmettow, CACM 55(4), 2012 | the honest limit on sparse human sampling |
| 12 | ISO/IEC/IEEE 15288:2023 | system-of-interest / **enabling system** / operational environment |
| 13 | Cobleigh, Giannakopoulou & Păsăreanu, *Learning Assumptions for Compositional Verification*, TACAS 2003 | an over-strong W is a defect |
