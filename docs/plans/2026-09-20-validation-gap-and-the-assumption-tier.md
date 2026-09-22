# The validation gap and the assumption tier

**Status: PROPOSAL. Not a ruling.** It asks for one, because it changes the
frame that [`external.toml`](../requirements/external.toml) declares LOCKED.

**Owner answers to §9 recorded 2026-09-21** — five answered (one in principle),
two open or deferred after a second pass the same day. Q1's answer opened the
enablement/verification thread in §10, which in turn resolved Q6 as posed and
**retired §6(f)'s separate treatment of the rig** in favour of one row kind at
two weights (§10.2). Recording an answer is not the ruling; §§1–8 are unchanged
by any of it.

**What it proposes, in one sentence.** The kit records what the system must do
at its own interface and tests that exhaustively; it does not record the
assumptions that carry those interface facts up to the human outcomes its needs
are written about, and therefore cannot test them — so this proposes that those
assumptions become rows, that test cases may verify them, and that the boundary
registry distinguish the crossing the system can observe from the crossing where
the outcome actually lands.

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
It happens at `EXT-003` (Adopter) — and `EXT-003` is reachable only across
`REL-001`, which the registry defines as *"external-to-external, the system NOT
a party"* and which *"must never grow a realizing IF row."*

**So the crossing where this kit's stakeholder value lands was ruled outside the
frame.** Not by accident — the reasoning in `REL-002`'s and `B-04`'s notes is
careful and defensible on its own terms. But the consequence is that there is
nowhere for validation to attach, which is why there are 194 test cases and all
194 of them test the machine.

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

## 3. Naming

The owner's reservation about "the machine" and "the world" is well founded.
They are precise inside Jackson's formalism and drift badly outside it —
"machine" reads as *hardware* to hardware people, and "world" slides to
"environment" and then to "deployment environment" within about two documents.

**Recommendation: keep R / S / W as the cited formalism, and do not ship
"machine" and "world" as the everyday nouns.** Name the *crossings* instead,
since crossings are what the registry actually holds.

### The candidates, assessed

| candidate | verdict |
|---|---|
| `machine` / `world` (Jackson, Zave) | Citable and exact. Keep in the rationale; reject as the shipped noun for the reason above. |
| `solution domain` / `problem domain` | Established, but the cut is wrong — the problem domain is the whole problem context, not the place the outcome lands. |
| `system-of-interest` / `operational environment` (ISO/IEC/IEEE 15288:2023) | The strongest *established* pair, and normative. But both name **systems**, and what we are typing here is a **crossing** — the operational environment is where the system *sits*, not where the outcome *lands*. Keep 15288 as the citation for the system-level split and for the enabling system (§4.3); it does not type a boundary row. |
| `ODD` — operational design domain (SAE J3016, ISO 21448, UL 4600) | **Adopt, for a different cell.** This is the current, standard-backed term for *the declared region of the environment within which the system's behaviour is claimed to hold* — which is exactly what the assumption row's `holds_when` cell is. See §4.2. |
| **`design system` / experience** | **Unusable.** In software, "design system" means a UI component library (Material, Carbon, Polaris, Fluent). This kit ships to software teams; the collision is immediate and total. The instinct behind it is right, and is preserved below. |
| `design boundary` / `experience boundary` | No collision, self-explanatory, weak currency. "Experience" is human-centric, which is wrong for a kit that also ships to physical projects (`CMP.category = "physical"` exists today). |
| `control` / `effect` | Both real usage ("span of control", "span of effect"). "Control" collides with control theory *and* with this repo's own `B-02` "Authority" crossing. |

### Recommended

A closed vocabulary on the boundary row:

```toml
frame = "design" | "effect" | "coincident"
```

- **`design`** — the system can observe and act here. Instrumentable.
  **Verification** lands here.
- **`effect`** — where the outcome the need names actually occurs. Frequently
  *not* observable by the system. **Validation** lands here.
- **`coincident`** — the two are the same crossing at this point, stated
  deliberately.

Three reasons this is the right shape:

1. It keeps the owner's **"design"** for the side you have authority over — and
   the repo already reasons in exactly that word: `B-04`'s note rules a crossing
   out because *"this system holds no **design authority** over whether an
   external runner honours the workflow it is handed."*
2. **`effect`** generalizes past humans — peer systems, physical outcomes,
   downstream repos — where "experience" does not.
3. **`coincident`** makes the collapse case a *stated claim* rather than an
   omission, which is this kit's standing doctrine that an empty cell should
   assert nothing. A CLI where the token the user types is the token the parser
   reads genuinely is coincident; saying so costs one word and is reviewable.

### The criterion that separates them

Not authority alone — you *do* hold design authority over the pixels, and none
at all over whether the user understood them. The criterion is **observability
by the system and whatever has been built to watch it**, which is Jackson's
shared-phenomena test:

> A crossing is `design` if the system, or a rig built to observe it, can
> detect that it happened. It is `effect` if the need names an outcome there
> that nothing built can see.

This makes the central claim countable rather than rhetorical: **the V&V gap is
the set of phenomena a requirement names that the system cannot observe.** "The
gap grows with complexity" stops being a slogan and becomes something a row can
be measured against.

> **Bounded 2026-09-21 (§11.1).** Read that as *a lower bound* on the gap, not
> the whole of it. Observability is one of **two** sources of W: a seam whose
> far side **interprets** rather than computes — an LLM, an adopting team — is
> fully observable and still carries W, because seeing the exchange does not
> tell you the answer was right. `frame` classifies the first source only.

**`frame` records a position, not a property.** Observability is not intrinsic
to a crossing; it is a function of what has been built to watch it, so a row can
**move** from `effect` to `design` when someone builds the rig. That is a
feature rather than a wobble — it makes the column a measure of instrumentation
coverage instead of a permanent verdict, and makes *"we moved a crossing into
the design frame"* a reportable result. §6(f) is the mechanism, and its
price: moving a row does not delete that row's assumption, it **replaces** it
with a fidelity assumption that has to be written as one.

---

## 4. What changes in the frame

### 4.1 One column on boundary rows

```toml
[boundary.B-05]
entity = "EXT-002"
direction = "out"
frame = "design"          # NEW — closed vocabulary, see §3
carries = """..."""
status = "Approved"
```

**Five edits.** Because all 79 SRs already carry `boundary_refs`, typing the
five `B-##` rows classifies every system requirement in the repo *for free* —
no SR is touched. That is the single strongest argument for putting the
discriminator here rather than on the requirement.

### 4.2 A fourth row kind: the assumption

`external.toml` already holds three row kinds *"because they are one
statement."* A domain assumption is a fourth statement about the same frame: it
is approved by the same authority, it changes only by ruling, and it belongs
beside the crossings it bridges. **Putting it here avoids a new registry file
and a new stage predicate entirely** — the conservative option, and the one the
file's own logic asks for.

> **Re-argued 2026-09-21 (§11.4).** That is a reason for putting the rows in
> *this file*; it is not a reason for them being rows at all, which the owner
> challenged directly. The load-bearing answer is narrower: **W needs an id so
> that W-evidence can be counted separately from S-evidence.** `Verifies` takes
> ids, so an assumption stated as a *cell* on a boundary row cannot be cited by
> a TC — and §5's three obligations collapse into one counter the moment they
> share an id. §11.3 also drops `bridges_from` in favour of the seam citing the
> assumption, which removes a duplicated edge.

```toml
[assumption.DA-001]
bridges_from = "B-05"          # the design crossing — where S is observable
bridges_to   = "EXT-003"       # the effect side — where R lands
assumption   = """A scaffold whose harness runs green is one an adopting team
                  can actually work in: the profile fits their stack, and the
                  registries they must fill are discoverable without reading
                  the kit's source."""
holds_when   = """The adopter's stack is one of the shipped profiles, and the
                  adopter reads ADOPTING.md before first use."""
obstacle     = """A team green-scaffolds, never fills a registry, and operates
                  a spine that resolves and says nothing."""
falsified_by = "TC-###"        # the signal that would show this is false
status       = "Drafted" | "Approved"
```

Three of those cells are borrowed rather than invented, and each has a standard
behind it:

- **`holds_when` is an ODD.** SAE J3016 / ISO 21448 / UL 4600 call the declared
  region within which a claim is asserted the *operational design domain*. This
  is the same object: the bounded slice of the world in which the assumption is
  claimed to hold. Naming it after the established concept means the
  **restriction move** comes with it — see §6(d).
- **`obstacle` is van Lamsweerde & Letier's obstacle** (*Handling Obstacles in
  Goal-Oriented Requirements Engineering*, IEEE TSE 26(10):978–1005, 2000).
  Formally: the negation of a goal, requirement **or assumption**, refined until
  it reaches conditions satisfiable in the domain. It is a *generator*, not a
  comment — see §6(b).
- **`falsified_by` is the falsifier.** Two independent lines converged on this:
  the monitored **"claims"** of REAssuRE (Welsh, Sawyer & Bencomo, ASE 2011),
  where a design-time assumption is attached to a goal and falsification
  propagates; and UL 4600's **Safety Performance Indicators**, defined as a
  metric with a threshold that *conditions a specific claim* in a safety case.
  The rule both imply is checkable and worth adopting outright:

  > **An assumption with no declared falsifier is an untested assumption.**

  That is a `trace.py` finding, in the kit's existing warn-first idiom.

One further borrowing, stated as a caution rather than a cell. In
assume-guarantee reasoning the environment assumption can be *synthesized* as
the weakest condition under which `S ⊨ R` (Cobleigh, Giannakopoulou &
Păsăreanu, TACAS 2003). The transferable consequence is that **an
over-strong W is a defect, not safety** — an assumption written broadly enough
to make the entailment trivially true has moved the problem rather than solved
it. Worth stating in the authoring guidance; not worth mechanizing.

### 4.3 The plant gets its existing, empty home

The third thing the owner named — *virtualizing the user's behaviour* — **is not
a boundary.** It is a system. ISO/IEC 15288 already names it: an **enabling
system**, one that supports a life-cycle stage of the system of interest without
being part of the delivered solution. Test rigs, simulators, plant models.

And the slot already exists: `entity.class` is a closed vocabulary of
`operational | enabling | interoperating | deliverable`, and **`enabling` has
zero rows in this repo.** The declared vocabulary anticipated this and nothing
ever filled it — while `EXT-005` ("Model provider API(s) / CLI(s)") is exactly a
plant the kit depends on.

One correction to make before that row is written: **EXT-005's protocol is
already simulated; its judgment is not.** `FAKE_AGENT`
(`tests/test_agent_loop.py:34`) is a scripted stand-in runner — it records each
invocation and the model it was handed, then performs the next action from an
`actions.txt` script (`commit` / `done` / `blocked` / `noop`) in the repo it was
launched in. That is what makes the loop tests deterministic, and it is the half
worth faking. The judgment half should stay un-simulated: a model good enough to
stand in for a model is circular. The split is worth stating on the row.

So: **two boundary types, one entity class, one new row kind.** Not three
boundaries. (What fills the `enabling` class, and what it costs, is §6(f).)

---

## 5. Three test obligations, not one

If the argument is `S ∧ W ⊨ R`, then evidence is owed on three fronts. The kit
currently collects one.

| # | verifies | where evidence sits | cost | cadence |
|---|---|---|---|---|
| **1** | **S** | the design crossing | cheap | every commit — *this is all 194 TCs today* |
| **2** | **W** | the assumption itself | cheap-to-moderate — *free where it is expressible as a metamorphic relation (§6c)* | continuous |
| **3** | **R through W** | the effect crossing, via a translation layer | expensive — *unless a rig moves the crossing (§6f), which splits the cost rather than removing it* | sparse, sampled — *and see the limit in §6* |

Obligation **2** is the new idea and the important one. Tests of W are often not
software tests at all — they are measurements of the world, monitors, sampled
observations, or a recorded check that a stated precondition still holds. For
SN-001's assumption, a W-test is *"take a shipped profile, scaffold it, and have
someone who has not read the source reach a first filled registry"* — not cheap,
but enormously cheaper than validating "an adopting team gets a working
process", and it fails in the same direction.

Obligation **3** is validation proper, and it is expensive by nature. The point
of the proposal is **not** to make it cheap. It is to make it *rare and
targeted* by putting obligation 2 underneath it — and, where a rig can be built,
to change **what the expensive probe is aimed at** (§6f).

---

## 6. Why this is affordable

The mechanisms, in the order they matter.

**(a) The probe count is bounded by the assumptions, not by the input space.**
Validation gets unaffordable when you try to sample R directly, because R lives
over the world and the world is large. Sampling W instead bounds the work by the
number of assumptions you wrote down. Twelve assumptions means roughly twelve
validation probes — not `2^n` over an input space. This is the whole
affordability argument and it is why W has to be *rows*, not prose.

The same allocation rule is normative in aerospace structures, where it is
called the **building-block approach** or validation pyramid: FAA AC 20-107B
requires tests "at the coupon, element, details, and subcomponent levels", and
CMH-17 Vol. 3 states the reasoning plainly — **run many cheap low-level tests to
bound variability so that very few expensive high-level tests can be
justified.** The pyramid is a cost argument, not a thoroughness argument. The
same logic transfers: many cheap W-tests are what buy the right to run few
R-probes.

**(b) Corner cases are generated, not imagined.** This is what the `obstacle`
cell is for. An obstacle is a negated domain assumption — van Lamsweerde's
obstacle analysis in goal-oriented RE is exactly this construction. Each W row
mechanically yields at least one adversarial case: *what if this does not hold?*
That answers the owner's requirement to "get as close to the validation layer as
possible in order to produce and catch corner cases" — the corner cases come out
of the assumption set by construction, rather than out of someone's imagination
at 4pm.

**(c) Some W is executable, at ordinary CI cost.** The cheapest surprise in the
survey. A **metamorphic relation** (Chen, Cheung & Yiu, 1998; surveys in IEEE
TSE 2016 and ACM CSUR 2018) is a necessary property across *multiple*
executions, which lets you test without knowing any single correct output —
the standard answer to the oracle problem (Barr et al., *The Oracle Problem in
Software Testing: A Survey*, IEEE TSE 41(5), 2015), and the reason the
technique is used at world boundaries with no oracle at all (*Metamorphic
Testing of Driverless Cars*, CACM 61(3), 2018).

The observation that matters here: **most useful metamorphic relations are
statements about the world, not about the machine** — *"reordering irrelevant
inputs must not change the verdict"*, *"adding an unrelated registry row must
not change an unrelated row's status"*. So writing an MR **is** writing a
testable domain assumption. Where a W row can be expressed as an MR, it costs
CI time and carries validation-flavoured semantics. That is the best price in
the whole proposal, and it should be the first thing tried for any new W row.

**(d) Narrowing the declared world is a legitimate answer.** This is the move
the kit currently has no name for, and it comes from SOTIF (ISO 21448), whose
whole method partitions scenarios into *known/unknown × safe/unsafe* and treats
**Area 3, "unknown unsafe", as the thing to shrink**. Its two sanctioned
responses to a gap are: improve the system, **or restrict the ODD**.

In our terms: when `S ∧ W ⊨ R` will not close, you may narrow `holds_when`
until it does — and then say so. That converts an unbounded validation
obligation into a bounded one plus an honest exclusion. It is neither "test
more" nor "build more", and it is the response most likely to be right for a
small team. SN-001's assumption is a live candidate: *"the adopter's stack is
one of the shipped profiles"* is an ODD restriction that makes a hopeless claim
tractable.

**(e) Evidence declares how close to validation it sits.** The owner's
observation — *"I'm not sure all the attributes / descriptors are available for
that distinction in the interface registry today"* — is correct. They are not.
The `Verification` vocabulary (`Test | Demonstration | Manual | Analysis |
Inspection | Attest | Critique` — `trace.py:526`) names the **method**; nothing
names the **distance from the effect boundary**. They are orthogonal, so a
descriptor can be added without disturbing the existing vocabulary.

The established instrument is **NASA-STD-7009B's Credibility Assessment
Scale** — eight near-orthogonal factors (verification, validation, input
pedigree, results uncertainty, results robustness, use history, M&S management,
people qualifications), each scored **0–4**, with the standard's own rule that
required credibility is **proportional to the risk of the decision the evidence
supports**. Level 4 validation is defined as agreement with the real system
across the full operational range *in its real environment* — i.e. the scale's
top rung is full validation and every lower rung is a declared distance from it.

Eight factors is far too heavy for this kit. The transferable part is the
*shape*: a small ordinal, and a rule that the required level is set by
consequence rather than by ambition. §7 proposes the minimal version.

**(f) The boundary can be moved: a rig manufactures a design crossing.**
Everything above takes the design/effect split as given. It is not given — it is
the current position of the instrumentation (§3), and instrumentation has become
far cheaper to build than the test-design conventions around it assume. This is
the mechanism that changes what the other five are worth.

The move: **add an enabling system (§4.3) that renders the effect observable,
and the crossing it manufactures is `design` by construction** — it was built to
be watched. Two instances, one from each end of the span this kit already claims
(`CMP.category = "physical"` exists today):

- A UI requirement's effect is *"the panel reads clearly."* Nothing at the API
  boundary sees that, so the TC stops at the DOM. Render the pixels and hand
  them to a vision model against a rubric, and a judgment of legibility becomes
  an observable event. **What made this impossible before was not that the
  effect was unobservable — it is that nothing rendered it.** Suites stop short
  of the pixels because they were designed when no judge existed downstream of
  them, and the convention outlived the constraint.
- A manipulation requirement's effect is *"the apple is gripped."* Software
  alone commands a current curve. A simulated arm with a contact model and a
  simulated apple makes *grasp succeeded* an observable event — and variance in
  mass, friction and pose can be injected far more cheaply than the
  corresponding real-world scenarios can be staged.

**What it buys, and what it does not.** It does not make the real phenomenon
observable. It manufactures a crossing against a *model* of the world and makes
**that** observable. So W does not disappear; it is **replaced**:

| the assumption before the rig | the assumption after |
|---|---|
| *"zero orphans ⟹ a reviewer trusts the chain"* | *"a model judging the rendered artifact against rubric R judges as a human would"* |
| *"this current curve ⟹ the apple is gripped"* | *"the contact model grips like the real gripper does"* |

That exchange is the whole point, and it is strongly favourable. The left column
is untestable in principle. The right column is a **fidelity** assumption —
bounded, stated, and testable by calibration against reality. The rate is good
because of *what changes how often*: the product changes every commit, the rig
changes yearly. So obligation 3 (§5) **splits** rather than shrinking — cheap
and continuous against the rig, expensive and sparse against the rig's fidelity.
The same small number of expensive probes, now aimed at the stable thing.

That is (a)'s pyramid with its rungs named: **the rig is the element level, and
the fidelity check is what buys the right to run few R-probes.**

**It needs no vocabulary beyond §4.2 and §4.3.** What is left over is one
`[assumption.DA-###]` whose `bridges_from` is the rig's crossing, `bridges_to`
the real effect, `holds_when` the rig's ODD, and `falsified_by` the calibration
probe. No fourth `frame` value, no new row kind.

> **Superseded in part, 2026-09-21 (§10.2/§10.4).** This paragraph originally
> made the rig an `enabling` *entity* with `B-##` crossings of its own. That is
> wrong for an in-tree rig, which is not outside the boundary: a rig we build is
> an `IF` row realizing an **existing** crossing, named from the `DA` row's
> optional `realized_by`. Only an *external* enabling system — a hosted
> simulator, a CI service — is an `EXT` row. The rest of (f) stands.

**The credibility caveat is (e)'s, unchanged.** A verdict inherits the
credibility of the rig that produced it — which is exactly why NASA-STD-7009's
CAS scores *input pedigree* and *results robustness* as factors separate from
validation. And the limit below stands without amendment: **a green run against
a rig is not evidence the fidelity assumption holds; only a red one is evidence
that it does not.**

### What this repo already built, and the row it is missing

The mechanism is live here and unrecorded. `render-dashboard-critique`
screenshots `PROJECT_STATE.html` across a declared width/theme/tab matrix so
that a critique judges pixels instead of ~790 KB of markup; the critique
contract in `PROCESS_OPTIONS.md` already obliges a perceptual TC to name its
**artifact recipe** beside its rubric; `llm-vision-convergence-loop` requires
two consecutive approvals at one content hash. That is a rig, a declared ODD and
a repeatability control — with **no assumption row behind any of them.**

It also answers the re-evaluation worry directly: *a rendered panel changes
easily, so what happens to its test case?* **The TC does not pin the pixels; it
pins the rubric — and the contract already rules that the rubric derives from
the SN/SR intent and never from the TC.** The anchor therefore sits *above* the
artifact: a redesign re-runs the judgment instead of invalidating the case,
`G#`/`B#` anchors accumulate as new failure modes are found, and the lax-TC
ratchet fires if a CHANGES-REQUESTED round closes with no change to the TC
prose, the test logic, or the rubric. The artifact is allowed to churn because
the bar is not stored in it.

What nothing does today is treat **the judge itself** as an assumption. No
check notices when a model revision silently shifts what the critic approves.
That row could be written immediately, and it is the most dogfoodable one in the
proposal:

```toml
[assumption.DA-002]
bridges_from = "B-##"        # the render rig's crossing - pixels, observable
bridges_to   = "EXT-003"
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

Note what that row does **not** claim. It does not assert that a model covers
the human axis — the caution below rules that out and still does. It states the
claim, bounds it, and names the sample that would refute it, which is the only
honest form available for a human-axis assumption.

### The honest limit on sparse sampling

One correction the survey forced, and it should be recorded before anyone plans
around the cheap end of this.

Sampling the human axis sparsely gives a **high-variance lower bound on
discovery, not a coverage claim.** Nielsen's "five users" rule is
popular practice, not established evidence: Faulkner (*Beyond the five-user
assumption*, Behavior Research Methods 35(3):379–383, 2003) resampled from 60
users and found that random 5-user sets caught anywhere from **55% to 99%** of
known problems — n=10 lifted the floor to 80%, n=20 to 95%. Schmettow (CACM
55(4), 2012) shows problem discovery is over-dispersed, which breaks the
homogeneous model Nielsen's curve assumes.

So: sparse R-level probes are worth running, and their *findings* are real. But
**a passed sparse probe is not evidence that a W row holds** — only a failed one
is evidence that it does not. Any rule the kit writes must say that, or it will
manufacture exactly the false confidence the proposal exists to remove. The
weight has to sit on obligations (b), (c) and (d); (a) buys targeting, not
assurance.

There is also no standard for the credibility of a *human* model comparable to
NASA-STD-7009 for physics models. If a human-axis assumption is load-bearing,
the honest options are to restrict the ODD around it or to accept a recorded
risk — not to claim a model covers it.

---

## 7. Impact

Surveyed against the code, not estimated. Anchors are given so the next session
can start from them.

### 7.1 The one precedent that makes this cheap

**A TC may already verify an off-spine id.** `Verifies` accepts `SR` / `LLR`
**and `IF-###`** — the rule is in `coherence.py:73-108`, and its constraint is
that a seam citation **supplements** a spine citation: *"a TC naming only seam
ids no longer says which requirement it discharges."* There is even a
migration allowlist for the coverage arm (`docs/if-tc-coverage-allow`, 118
seeded entries) and an `if_tc_coverage_findings` check that warns, then errors
under `--strict` at DevStg-Tests+.

So step 3 of the staging is not a new mechanism — it is a second tenant in an
existing one, with a working precedent for both the citation rule and the
staged rollout. **Open question it forces:** does a W-test *supplement* an SR
citation, like a seam does, or may it stand alone? A test of "zero orphans ⟹ a
reviewer trusts it" does not obviously discharge any single SR. My reading is
that it should supplement — the assumption belongs to a requirement's argument —
but this needs a ruling, not a default.

### 7.2 Why the assumption rows belong in `external.toml` — costed

The survey priced both options. A **new registry file** requires **13 mandatory
edits** including a new `kitlib/ladder.py` rung, a new `spine_rules` predicate,
a `DECLARED_INPUTS` entry, a `bootstrap.MAPPING` entry, an `_offspine_ids`
watermark, and a `test_dogfood_sync` floor — with the ladder change described as
*"the largest single ripple"* (it reaches `check.py` stage selection, every
`from-stage` in `stack.ini`, `check_vocab.py`, the `gate-advance` skill and
three test modules).

Putting the rows in `external.toml` **skips five of those outright**, because
the file is already carried:

- `kitlib/stage.py:144` — `external.toml` is already a `DECLARED_INPUTS` entry,
  so the stage fingerprint covers the new rows **for free**. (The survey flags
  the opposite case as a real hazard: an undeclared registry means
  `derive_stage --check` stays green over a changed file.)
- `bootstrap.MAPPING` already scaffolds it.
- `baseline_snapshot` already lists it in `SNAPSHOTTED` / `SNAPSHOT_TIERS`.
- No new ladder rung, no new `spine_rules` predicate.
- `test_dogfood_sync.TOML_REGISTRIES` is keyed by **ID column, not path**
  (`:246-252`, precisely because `external.toml` already carries three tiers on
  one path) — so a fourth tier is the shape that census was built for.

**This is the decisive argument for §4.2**, and it was not obvious before the
survey.

### 7.3 The actual edit list

**(a) `frame` column on boundary rows — 4 mandatory edits**

| # | File | What |
|---|---|---|
| 1 | `kitlib/spine.py:651` | add the key to the `B-ID` tuple (schema of record) |
| 2 | `registries/external.template.toml` | add the key to `[boundary.B-000]` |
| 3 | `spine_carrier.py` `OFFSPINE_COLUMN` | key → `Frame` |
| 4 | `migrate_carrier.py` `KEY` | the exact inverse — `test_rule_sync.py:700-712` asserts both maps invert **and match in length** |

Then behavior: `trace.py:526+` `ENUM_FIELDS` for the closed vocabulary (note the
`B` tier's enums ride the **advisory** pipe, so a bad value warns and never
fails — `test_external_frame.py:371`), and the five live rows.

**(b) `[assumption.DA-###]` row kind — 8 mandatory edits**

The four above, plus `OFFSPINE_KEYS` (new `DA-ID` entry), `OFFSPINE_TABLE`
(`"DA-ID": "assumption"`), a `TOML_REGISTRIES` entry **and** a matching floor
(`test_dogfood_sync.py:433` asserts `set(floors) == set(TOML_REGISTRIES)` — a
registry joined with no floor fails immediately), and `trace.py:920-928`
`_offspine_ids` for the id watermark. That last one is not optional: the survey
notes the missing-watermark hole has really happened twice here (IF-121/122 and
OI-26).

### 7.4 What will actually hurt

Three constraints worth knowing before committing to scope.

**The frame is pinned by test, not just by prose.**
`tests/test_external_frame.py:87-114` asserts *exactly* 4 entities, 4 crossings
and 3 relationships plus the spent-id gaps; `:128-146` pins every `status` to
`Approved`. Adding a column is fine. **Adding rows changes that test and needs
a sitting** — which is correct, and is the ruling this document asks for.

**Prose has almost nowhere to go.** The byte budget is tighter than expected:

| file | cap | now | headroom |
|---|---|---|---|
| `AGENTS.template.md` | 10,000 | 9,980 | **20 B** |
| `CLAUDE.md` | 8,500 | 7,975 | 525 B |
| `byte-budget-guard/SKILL.md` | 5,000 | 4,613 | 387 B |
| `PROCESS.md` | *watched* | 88,990 | — |
| `PROCESS_OPTIONS.md` | *watched* | 189,535 | — |

And `test_bootstrap.py:443+` parses the skill's own budget table and asserts
each baseline equals the real file size — **so any edit to a capped file must
re-stamp the skill in the same commit, and that re-stamp has 387 bytes to fit
in.** Practical consequence: this concept's prose home must be
`PROCESS_OPTIONS.md` (watched, an expansion home) or `ADOPTING.md`/`EXAMPLE.md`
(explicitly unbudgeted), **not** `AGENTS.template.md`, which has 20 bytes free.

**Adopters need a resync entry.** `RESYNC_PACK.md` §3 takes a `[since <sha>]`
entry, format-enforced by `test_resync_pack.py:117/210/252`.

### 7.5 A correction to something I said earlier

I suggested that `Permutations` + `gen_cases.py` was the cheapest hook for
dimensional reasoning. The survey shows that is weaker than I implied:

- **No live SR row uses `Permutations`** — and `test_dogfood_sync.py:515-519`
  *actively asserts it stays unused*, because it is the deliberate probe for
  the template-drop direction of the three-leg drift rule. Filling it on a live
  row **breaks that test** until a different probe key is chosen.
- **`gen_cases.py` has no downstream consumer.** It writes to stdout only
  (*"nothing is written: the output is text for a human or a registry to take
  up"*), is not a `stack.ini` step, and no script imports it. The repo's own
  census calls it *"opt-in permutation grammar, unused layer"*.

So the machinery exists and is genuinely well built — greedy all-pairs,
boundary corners, four output formats — but it is a **dormant layer, not a live
hook.** Using it is a decision to activate something, with a test to re-point
first. That does not kill the idea; it re-prices it.

### 7.6 Adjacent gaps the survey turned up

Not part of this proposal — recorded because they were found.

1. **`docs/test/evidence` does not exist in this repo.** It is the sole input to
   `DevStg-Release` (`spine_rules.py:583-592`), so this repo can never derive
   its top rung. Not a defect at stage Tests, but worth knowing.
2. **Per-requirement coverage lives in `trace.py`, not `plan_coverage.py`** —
   the `SR → LLR → TC` matrix at `trace.py:5194-5207`. `plan_coverage.py` is
   the dual-plan pre-pass and is unrelated, despite the name.
3. **The SN `priority` vocabulary (`M`/`S`/`C`) and the WI `Priority` integer
   are unconnected.** Nothing maps a Must-need onto queue order. This is the
   prioritization gap from earlier in the session, and it is a small, separable
   fix.

---

## 8. Staging

The proposal is deliberately separable. Each step is useful alone, and each
later step assumes only the earlier ones.

**Step 1 — type the crossings.** Add `frame` to the boundary schema; set it on
the five `B-##` rows and the template's example rows. **Four mandatory edits
(§7.3a); no new row kind, no new predicate, no requirement touched, no test
re-pinned.** *Outcome: every SR in the repo is classified design/effect for
free, and the question "which of our requirements can we actually observe?"
becomes answerable.* This step alone is worth doing even if everything below is
rejected.

**Step 2 — record the assumptions that already exist, unenforced.** Add the
`[assumption.DA-###]` row kind (**eight mandatory edits, §7.3b**). Write the W
rows for the 16 SNs — they exist today as the unstated gap between each `need`
and its `acceptance`, so this is transcription, not invention. Warn-only.
Nothing gates. **This is the step that needs the ruling**, because adding rows
re-pins `tests/test_external_frame.py`. *Outcome: the argument becomes visible
and arguable. Expect this step alone to surface real defects.*

**Step 3 — let test cases verify an assumption.** Allow `DA-###` as a `Verifies`
target — following the `IF-###` precedent already in `coherence.py`, and
settling the supplement question in §7.1 first — and add the evidence
descriptor from §6(e). Start with the metamorphic subset (§6(c)) because it is
nearly free. *Outcome: the first W evidence exists.*

**Step 4 — the falsifier rule.** `trace.py` warns on an `Approved` assumption
with no `falsified_by`. Warn-first, per house idiom. *Outcome: an assumption
cannot quietly be decoration.*

**Step 5 — the gate, if wanted.** `DevStg-Tests` requires every `effect`-framed
SR to reach an assumption, or carry a recorded waiver. **This is the only step
that costs an adopter anything mandatory, and it should be opt-in with an
applies-when**, per the proportionality doctrine.

**Not proposed: a new stage rung.** The recursion already oscillates
Reqs↔Arch; adding a sixth predicate would make the ladder harder to read for a
concept that rides existing rungs perfectly well.

---

## 9. Open questions for the owner

Answers recorded inline, dated, with their standing marked. `ANSWERED` means
the owner has decided and the next sitting may build on it; `DEFERRED` and
`OPEN` mean it may not.

1. **Does the human come out of `EXT-001`?** `EXT-001`'s own note calls this an
   open follow-on. Under this proposal it is decisive: if the human stays folded
   into "Development session", this repo has **no `effect` crossing at all** and
   every `frame` value is `design` — the model would be correct and inert here
   while still working downstream. Splitting the human out is what makes the kit
   able to dogfood its own validation story. It is also the more invasive
   change.

   > **Owner, 2026-09-21 — ANSWERED: yes, and wider than asked.** The human
   > comes out. The owner also re-opens the *system breakdown* around it: every
   > design has **auxiliaries** — a test rig, the test infrastructure itself,
   > the deployment/delivery path — which are under design control, are not
   > shipped with the product, and do not trace to an effect, yet carry implied
   > requirements and tightly-coupled interfaces. Developed in **§10**; the
   > owner will return to it in more detail.

2. **Does `REL-001` become a crossing?** §1's finding is that the kit's
   stakeholder value lands across a relationship declared not-a-party. Either
   that ruling stands — and the kit accepts that it cannot validate its central
   claim, recorded as such — or `REL-001` is re-framed as an `effect` crossing
   and the frame grows. Both are defensible; drifting between them is not.

   > **Owner, 2026-09-21 — DEFERRED, dependent on Q1.** Expected to fall out of
   > the re-drawn breakdown rather than to be decided on its own.
   >
   > **Evidence added the same day (§10.4.2), still deferred.** The registry's
   > own rule — *"wanting [a realizing IF row] means what you have is a boundary
   > crossing"* — makes this checkable rather than a matter of preference, and
   > the check returns *crossing* for both relationships: `FAKE_AGENT` rigs
   > `REL-003`, and the `scaffold` fixture has been rigging `REL-001` since
   > before the frame was drawn. The decision stays the owner's; what is gone is
   > the option of settling it by taste.

3. **`frame` vocabulary: two values or three?** `coincident` costs a word and
   buys an explicit claim. The alternative is two values plus the convention
   that a single row may be cited by both kinds of requirement.

   > **Owner, 2026-09-21 — ANSWERED: three values; keep `coincident`.** Noting
   > that ordinary software crossings will reach for it often. One idea
   > recorded but **not adopted**: coincidence might be *derivable from
   > topology* — a `B-##` running straight from an external entity into the
   > design is coincident, whereas a crossing reached only through a
   > translating layer is not. The owner pushed that to its end (*"does the
   > `B-` interface need to exist at all?"*) and landed on keeping the explicit
   > row: **differentiating is worth the word.** Consistent with the standing
   > doctrine that an empty cell asserts nothing — a derived value would assert
   > something nobody wrote.

4. **How heavy is the evidence descriptor?** A 0–4 CAS-style ordinal is
   defensible and citable; a three-value `assumed | sampled | monitored` is
   cheaper and probably enough for a kit this size. My recommendation is the
   three-value form, with the CAS cited as where to go if a project needs more.

   > **Owner, 2026-09-21 — ANSWERED: take the recommendation.** The three-value
   > `assumed | sampled | monitored` descriptor, CAS cited as the escalation
   > path. Recorded honestly: the owner notes the impact is hard to appreciate
   > from here, so this is agreement to the cheap option, **not** a finding that
   > the heavy one was wrong. If the descriptor starts carrying weight, this is
   > the answer to revisit first.

5. **Does a W-test supplement, or may it stand alone?** (§7.1.) The `IF-###`
   precedent says a TC citing only off-spine ids is an orphan. My reading is
   that an assumption belongs to some requirement's argument and should
   therefore supplement — but a W-test of *"zero orphans ⟹ a reviewer trusts
   it"* does not obviously discharge any single SR, so this needs deciding
   rather than defaulting.

   > **Owner, 2026-09-21 — OPEN, leaning stand-alone.** Against my reading
   > above. Consequence if it holds: the `IF-###` precedent does **not**
   > transfer, and `coherence.py`'s supplement rule needs a deliberate
   > exception rather than a second tenant — which un-does most of §7.1's
   > "this is cheap because the mechanism exists" argument. That cost is not
   > yet surveyed.

6. **Does a rig's crossing get a `B-##` row, or stay out of the frame?**
   (§6(f).) Giving the render rig a boundary row puts an *enabling* system into
   a registry that has so far held only the system's own crossings — and
   `test_external_frame.py:87-114` pins the crossing count, so this is a
   sitting either way. The alternative is to leave the rig unregistered and let
   the assumption row carry the whole bridge: cheaper, but it forfeits the
   "which crossings are instrumented" count that §3's mutable-`frame` reading
   exists to buy.

   > **Owner, 2026-09-21 — OPEN; the same question as Q1.** Stated by the
   > owner as: *how do we differentiate the deliverable system the user
   > experiences from the components that exist to maintain and deploy it?*
   > **Second pass, same day — answered as posed: neither.** A rig built by
   > this team is in-tree, so it is an `IF` row realizing an existing crossing
   > plus a `DA` row carrying its fidelity — it adds no `B-##` row and does not
   > re-pin the crossing count. See §10.4. The *classification* question behind
   > it is resolved in §10.3; what remains open is the `EXT-001` re-draw.

7. **Does any of this ship downstream in v1, or is it dogfooded here first?**
   Given the template/instance sync constraint and the 20 bytes free in
   `AGENTS.template.md`, shipping the schema and holding the enforcement is the
   low-risk path.

   > **Owner, 2026-09-21 — ANSWERED in principle: yes, it ships.** Conditional
   > on the details being nailed down first — which §10 and Q5 currently block.

---

## 10. Enablement, verification, and the auxiliary systems (OPEN)

Recorded 2026-09-21 from the owner's answers to Q1 and Q6, then extended the
same day. **Still a sketch, not a proposal** — but the second pass resolved more
than the first, and two of its findings are checkable against the code today.

### 10.1 The chain

The owner's frame, in one line:

```
effect  <->  translation | rig  <->  boundary interface  <->  design
```

- A **translation** converts an effect into a design boundary and **is an
  assumption**. It enables validation by *claiming* the conversion holds.
- A **rig** converts an effect into a design boundary and **is a system**. It
  enables validation by *performing* the conversion — simulating the effect and
  putting the output against a rubric — on a more complex basis than an
  assumption can carry.

Both are enabling components; neither is shipped. Other supporting systems
(deployment, procurement, the test plumbing) sit alongside them, also under
design control and also absent from what a user experiences. The owner's
position is that those need no further typing here, and that is right: this
section only has to be correct about the ones that **bridge to an effect**.

### 10.2 Translation and rig are one construct at two weights

This is the simplification the second pass bought, and it **retires the separate
treatment §6(f) gave the rig**.

A translation and a rig do the same job in the same place, and differ only in
whether the bridge is *asserted* or *built*. So they are one row kind — §4.2's
`[assumption.DA-###]` — with an optional cell naming the system when one exists:

```toml
[assumption.DA-002]
bridges_from = "B-##"
bridges_to   = "EXT-003"
realized_by  = "IF-###"    # OPTIONAL. Present = rig. Absent = translation.
```

The idiom is already in the file next door. `interfaces.toml` carries
`interface_from_external` / `interface_to_external` naming the `B-##` a row
realizes, and states the rule this cell should copy — *"a row with neither key
is an internal seam, and that ABSENCE is the statement."* A `DA` row with no
`realized_by` is a pure claim and says so by omission.

**Cost: one optional key on a row kind §4.2 already proposes.** It adds nothing
to §7.3(b)'s eight edits.

### 10.3 The discriminator is a fidelity claim — and the owner's naming is better

The first pass cut *"a rig may carry TCs, plumbing may not"* on the grounds that
a rig makes a falsifiable fidelity claim and plumbing makes none. The owner's
naming for that cut — **enablement versus verification** — is better and should
be the shipped wording.

One correction to how it is drawn: these are **not siblings**. Deployment, test
infrastructure and rigs are all *enabling* in 15288's sense. **Verification is a
role some enabling systems play**, identified by whether the system stands
underneath a fidelity claim. Which gives the cheapest possible typing:

> **A rig is an enabling system named in some `DA` row's `realized_by`.
> Everything else under design control and not shipped is supporting
> enablement.**

No new column and no new vocabulary — the classification is **derived** from the
assumption set. The trade to note: a derived classification cannot be queried
before the `DA` rows exist, so *"list our rigs"* is unanswerable at Step 1 and
answerable at Step 3. Acceptable, and the same shape as `B-02` being reported
unrealized today — a deliberate state, visible rather than hidden.

### 10.4 Where a rig stands — the party/crossing distinction

**Correction to the first pass, from the owner: a rig *does* connect to the
external interface.** That is the whole point of one. A rig is virtualizing the
external party, so it presents the interface that party presents; a rubric run
at that boundary is a rubric run on the interface **the user acts through and
sees effects from**, which is exactly why rig evidence is validation-flavoured
rather than merely more verification. The first pass said "a rig is an `IF` row,
not an `EXT` row" in a way that read as pushing the rig *away* from the
boundary. It does not.

What makes both statements true is a distinction the registry already draws:

> **A rig is not a *party*. It occupies a *crossing*.**

`external.toml` separates the two on purpose — `[entity.EXT-###]` is *"who is
outside"*, `[boundary.B-##]` is *"what crosses, from the SYSTEM's point of
view"*. The rig does not become the external entity (we built it; claiming
otherwise would misstate design authority). It stands **in that entity's
position at the crossing** — and the mechanism for "an in-tree row standing at
an external crossing" already exists and is named:
`interface_from_external` / `interface_to_external`. So an `IF` row with a
tie-back **is** the rig connected to the `EXT` interface. The earlier table's
*therefore* column obscured that; the rows themselves were right.

| | is the external party? | stands at the crossing? | recorded as |
|---|---|---|---|
| the real entity | yes | yes | `[entity.EXT-###]` |
| a **rig** we build | no — we hold design authority over it | **yes** | an `IF` row tying back to that `B-##` |
| a **translation** | no | no — it is a claim, not a port | a `DA` row alone |

**Q6's answer is unchanged by the correction:** rigs add no `B-##` rows and do
not re-pin `test_external_frame.py`'s count, because they realize crossings that
already exist rather than manufacturing new ones. An *external* enabling system —
a hosted simulator, a CI service — would still be an `EXT` row in the empty
`enabling` class.

### 10.4.1 The "nearly" is the fidelity assumption

The owner's own hedge is the most useful sentence in this thread: a rig stands
at *"the same interface (or nearly the same)"* — and wonders whether that
**nearly** is why it cannot simply *be* the external row.

It is, and the consequence is a rule this proposal was missing:

> **The delta between the rig's interface and the real party's interface IS the
> fidelity assumption. A `DA` row should state the delta, not the resemblance.**

If a rig presented *exactly* the external interface it would be
indistinguishable from the real party, there would be no gap, and the `DA` row
would be vacuous. The gap is therefore not a defect of the rig — it is the rig's
**content as evidence**, and the thing the assumption row exists to hold.

This also supplies the positive construction §4.2 lacked. That section warns,
via Cobleigh, that an over-strong `W` is a defect, but says nothing about how to
write a good one. The delta framing says how:

| weak — states the resemblance | strong — states the delta |
|---|---|
| *"the contact model grips like the real gripper"* | *"the contact model omits deformation and stick-slip; above ~X N the sim over-reports grip"* |
| *"the fake runner behaves like a model CLI"* | *"the fake runner reproduces argv/stdin, exit codes and commit effects; it reproduces no judgment, so nothing about prompt quality is evidenced here"* |

The right-hand column is falsifiable, bounds its own ODD, and tells a reader
what the rig does **not** cover — which is the cell `obstacle` and
`falsified_by` then hang off naturally.

### 10.4.2 Applying the rig test to Q2

The first pass flagged that `FAKE_AGENT` stands in for `EXT-005` across
**`REL-003`** — a *relationship*, not a crossing — so an `IF` row pointed at it
would have nothing to realize. With the correction above, that is no longer a
loose end. **It is a decision procedure, and it is the registry's own:**

> *"A relationship carries NO interface vocabulary, deliberately: it is not a
> crossing and must never grow a realizing IF row. **Wanting one means what you
> have is a boundary crossing.**"* — `external.toml:20-22`

A rig realizes a crossing. So **building a rig at a relationship is precisely
the "wanting one" that rule names**, and the rule's own answer is that the
relationship was a crossing. That converts Q2 from a matter of taste into
something checkable: *is there a rig standing there?*

Run the check and both relationships answer:

- **`REL-003`** (session → model provider) — `FAKE_AGENT` stands there today.
- **`REL-001`** (Template → Adopter), the one Q2 actually asks about — **a rig
  stands there too, and has all along.** `tests/conftest.py:1-7` states the
  design outright: *"The tests exercise the scripts the way a downstream user
  would: bootstrap a real scaffold in a temp dir and run the actual commands."*
  The `scaffold` fixture materializes the delivered package and then **plays the
  adopter**, running the adopted toolkit in a synthetic repo —
  `test_bootstrap` (full scaffold bootstraps), `test_old_kit_resync` (scaffold
  at an old kit commit, sync forward), and the scaffold-driven gate modules.
  That is a virtualized `EXT-003`.

Worth splitting carefully, because overclaiming here would be easy. Materializing
the package is **`B-05`** — ordinary verification of an output that genuinely
leaves the system. It is the *second* half that is the rig: running the harness
as an adopter would and judging that it comes up green. And SN-001's acceptance
is already written at that far side — *"produces a scaffold whose harness runs
green out of the box"* — so the need's own acceptance reaches across `REL-001`
even though the frame says the system is not a party to it.

**This does not decide Q2**, which is the owner's and is deferred pending Q1.
What it does is remove the option of deciding it by preference: the frame
declares relationships un-realizable, the suite has been realizing this one since
before the frame was drawn, and one of those two has to move.

### 10.5 The self-derivation limit

The owner's finding, recorded: **this repo cannot dogfood its own development
scripts.** It has been tried repeatedly; executing the same scripts that are
being modified does not yield a usable result.

Worth generalizing, because the reason is what this section is about:

> **A rig derived from the system under test cannot falsify assumptions the two
> share.**

Self-execution is that failure at its limit — the rig *is* the system, the
shared-assumption set is total, and so the rig can falsify nothing. That is why
it never works, and it turns the owner's experience into a rule that applies to
every rig rather than to this one situation. It is also the standing argument
for why `FAKE_AGENT` is the right shape: a **scripted stand-in that does not run
the real thing** shares no assumptions with what it replaces. The owner's remark
that a rig *"might be derived by the system itself"* names the risk axis
exactly — derivation is cheap, and it buys correlated blind spots.

**Scope, stated so it is not over-read.** The finding is about **self-execution
of scripts under modification**. It is *not* a retraction of Q1's rationale,
which was about the kit being able to state and test its own validation story —
a different claim, still standing. And CLAUDE.md's existing self-application
boundary (*"no product launch"*) is the same instinct already written down; this
extends it rather than contradicting it.

### 10.6 The boundary diagram is derived — so the redraw is a row change

The owner asks for the boundary diagram to change. The useful fact: **there is
no diagram to edit.** `gen_trajectory.py` derives the System-context view from
`external.toml` into the How-SW tab (`context_block(frame_context(root), ...)`,
WI-455) — *"the depth-0 frame: who is outside, what crosses, and the
external-to-external flows the system is not a party to."* **Editing rows is
editing the diagram**, and there is no second artifact to keep in sync.

The target the owner described, as a sketch for the sitting to rule on:

| row | change | why |
|---|---|---|
| `EXT-001` Development session | **narrow** — keep the environment and working copy, drop the human | Q1, answered yes |
| *new* Human operator | **add**, `operational` | gives this repo its first `effect` crossing (§9 Q1) |
| `EXT-005` Model provider | keep external; make its **rigged** status legible | the owner: *"the LLM agent, while external, is rigged in this setting"* |
| `EXT-002` Template | unchanged | already the delivery auxiliary, already typed (§10.7) |
| `EXT-003` Adopter | unchanged | the effect side |
| test infrastructure | **not shown** | the owner: inherent to defining a system, not a frame element |
| rigs | **not entities** | in-tree, so `IF` + `DA` rows (§10.4) |

The open piece is how *"rigged"* renders. `EXT-005` stays one external entity
either way; what changes is that a `DA` row now names the rig standing in for
it, and the derived view would have to read that to show it. **Whether
`context_block` learns to draw the rigged relation is a dashboard question and
should not hold up the frame decision** — the rows are true before the view can
render them.

### 10.7 Where this still collides with the frame as it stands

1. **`EXT-001` already bundles three of the four kinds.** Its description folds
   in *"shell, git client, OS, Python, editors, test runner, LLM runners"* — the
   human, the dev environment, the test infrastructure **and** the model runner
   in one row. Q1's *yes* pulls the human out; §10.6 pulls the frame further.
   Still the largest single edit in this thread, and it re-pins
   `test_external_frame.py`.

2. **~~`enabling` is one word for three things~~ — RESOLVED by §10.3.** It stays
   one class; verification is a *role*, derived from `realized_by`. No
   subdivision needed.

3. **The delivery auxiliary already exists, typed from the other end.**
   `EXT-002` (Template) *is* the packaging/delivery auxiliary, and its note
   already records the frame-relativity this thread keeps reaching for: *"From
   an adopter's frame this package is their enabling system."* Any taxonomy that
   lands must **absorb** that row, not add a second beside it.

### 10.8 The degenerate case this repo is

**This kit's product *is* test infrastructure.** CLAUDE.md declares the traced
product to be `project-trajectory/scripts` **and `tests/`** — so the thing
§10.3's rule would class as supporting enablement is, here, shipped product that
must carry TCs.

My reading of the resolution, offered rather than assumed: the split is
**frame-relative, exactly as `EXT-002`'s note already says.** Auxiliary is a
role a system plays with respect to a declared system-of-interest, not an
intrinsic property — and this repo's system-of-interest is the kit, for which
the harness is deliverable content. §10.5 is the same relativity seen from the
operational side: the scripts are product when they are the thing being built,
and cannot simultaneously be the rig that tests that build.

### What this does not change

Nothing in §§1–8. This thread is about *which entities exist, how they are
classed, and where the bridge is recorded*; the `S ∧ W ⊨ R` argument, the
`frame` column and the assumption row are indifferent to its answer. **§8's step
1 in particular stays executable today** — typing the five existing `B-##` rows
does not wait on any of this.

---

## 11. Are assumptions a tier, or a cell? (owner challenge, 2026-09-21)

The owner's challenge, stated fairly, because it is the strongest one made
against §4.2 so far:

> *A user is always working* through *something that translates — a person
> operates a computer, the computer turns their intent into cells in the spine
> registries, the tooling acts on those. So the translation is not a special
> case, it is everywhere. And it is ultimately boundaries and relationships that*
> *"make an assumption about how another system will interpret complex
> information." Even an `IF` row facing an LLM assumes a non-deterministic
> judgment on its input. So why a separate row kind — why not just expand the
> boundary definition with what it assumes about an ambiguous far side?*

The challenge is right about the diagnosis and, I will argue, backwards on the
remedy — but the diagnosis forces a correction to §3 that matters more than the
remedy does.

### 11.1 The correction: W has two sources, not one

§3 derives the entire V&V gap from **observability** — *"the set of phenomena a
requirement names that the system cannot observe."* That is incomplete, and the
owner's LLM example is the counter-example that shows it:

**An `IF` row facing a model is fully observable and still unverifiable.** The
system can see the call happen, see what it sent, and see what came back. Every
phenomenon is shared. And none of that says the answer was *right*, because the
far side **interpreted** rather than computed.

So there are two independent properties, and the doc has been running them
together:

| axis | question | if "no" |
|---|---|---|
| **observability** (§3) | can the system detect that the crossing happened? | the crossing is `effect`; W bridges to it |
| **determinism** | does the far side *compute*, or *interpret*? | seeing the crossing does not tell you it was right; W covers the interpretation |

Observability asks *can I see it*. Determinism asks *does seeing it tell me it
is correct*. They are orthogonal, and **W attaches to either.** This is exactly
the oracle problem that §6(c) already cites (Barr et al. 2015) — the doc quoted
it as a reason validation is expensive and never connected it to the frame. It
belongs in the frame: a seam with no oracle carries W whether or not it sits at
the boundary.

**Consequence for §3:** the `frame` column stays correct and stays worth adding,
but it no longer classifies every source of W. A crossing can be `design`,
`coincident`, and still assumption-laden. The countable claim in §3 should be
read as *a* lower bound on the gap, not the whole of it.

### 11.2 The pervasiveness is real, and it is priced

Counted, not estimated. `interfaces.toml` holds **167 rows**, and the external
parties they name are:

```
41  external:downstream     the adopting team - interprets
 5  external:               (unqualified)
 4  external:git            computes
 4  external:agent          the model runner - interprets
 3  external:run            computes
 1  external:upstream
```

So the interpreting far sides are roughly **45 of 167 rows, ~27%** — not
universal, as the owner's "always" would suggest, but far more than the ~16
effect-side assumptions §6(a)'s affordability argument was sized against. The
challenge is therefore materially correct: **assumptions are not confined to
effect crossings, and §6(a)'s "twelve assumptions, twelve probes" was priced too
cheaply.**

### 11.3 Why pervasiveness argues *for* rows, not cells

Here is where I think the remedy inverts. If the assumption were a cell on the
boundary or `IF` row, then the claim *"the far side interprets rather than
computes, so its output requires judgement rather than comparison"* would be
written **45 times**. Those 45 copies would drift, would each need their own
falsifier, and could not be narrowed in one place when the ODD is restricted
(§6d).

That is precisely the situation this repo's own doctrine addresses:

> *"Where two or more existing outputs already overlap, restructure so each
> behavior has exactly one home — never an original plus a near-copy."*
> — PROCESS.md §3, the 0→A→B rule

**A pervasive assumption is the strongest possible argument for giving it an
id.** One row, one status, one `holds_when` to narrow, one `falsified_by` — and
45 seams citing it. Stated as cells it is 45 near-copies of one claim; stated as
a row it has one home. The owner's observation that assumptions are everywhere
is the reason they cannot be cells.

**This does flip the citation direction, and that fixes a duplication the owner
was right to sense.** §4.2's `bridges_from` / `bridges_to` re-declares an edge
the `B` and `IF` rows already declare. Better: the **seam cites the
assumption**, exactly as an SR cites `boundary_refs` today —

```toml
[boundary.B-05]
frame       = "design"
rests_on    = ["DA-001"]      # NEW - the assumptions this crossing's claims need
```

— leaving the `DA` row to carry only what the seam does not already know: the
effect side it reaches, the ODD, the obstacle, the falsifier. `bridges_from`
becomes derivable and should be dropped. **This is a real simplification of
§4.2 and it came out of the challenge.**

### 11.4 The second reason, which is decisive on its own

Even if an assumption were attached to exactly one seam and never shared, it
would still need an id — because **§8 step 3 requires a test case to cite it,
and `Verifies` takes ids, not cells.**

If a W-test cites the boundary instead, then a TC verifying the crossing's
*contract* and a TC verifying the crossing's *assumption* become
indistinguishable. §5's three obligations collapse back into one counter, and
§1's finding — *194 test cases and all 194 of them test the machine* — becomes
unsayable. The whole document exists to make that split countable. **W needs an
id so that W-evidence can be counted separately from S-evidence.** That is a
better justification for the row kind than the one §4.2 gives ("a fourth
statement about the same frame"), and §4.2 should be re-argued on it.

### 11.5 Which assumptions become rows — the filter the doc lacked

The owner's keyboard example exposes a genuine hole. *The computer translates
the user's intent into cells in the registries* is true, is an assumption, and
obviously should not be a row. The doc had no rule for stopping. Two, proposed:

1. **The obstacle test — primary, and self-checking.** An assumption earns a row
   when you can write a **non-silly `obstacle`** for it (§6b). If the negation is
   not a failure mode anyone would plan against, there is no row. *"The keyboard
   emits characters other than those pressed"* fails. *"A team green-scaffolds,
   never fills a registry, and operates a spine that says nothing"* passes. This
   uses a cell §4.2 already proposes and needs no new machinery.
2. **The interpretation trigger — where to go looking.** Wherever the far side
   interprets rather than computes (§11.1), *suspect* an assumption. A detector
   for where to search, never a rule that every such seam yields a row.

Behind both sits NASA-STD-7009's rule, already cited at §6(e): **credibility
proportional to the risk of the decision the evidence supports.** The keyboard
assumption carries no decision risk. The scaffold assumption carries all of
SN-001's.

### 11.6 What is still not captured

The owner says pieces are missing, and that is correct — these are the ones I
can name, recorded so the next pass does not mistake this section for closure.

1. **Blast radius is unmodelled.** If 41 seams cite one assumption and it is
   falsified, 41 seams are affected at once. Nothing in the proposal expresses
   that, and a shared `DA` row makes the coupling invisible in exactly the way a
   shared dependency does.
2. **Chained assumptions.** If a crossing rests on `DA-001` and `DA-001` itself
   rests on another assumption, does `W` compose? Jackson's formalism takes `W`
   as a flat conjunction and says nothing about depth. The owner's
   user→device→registry→tooling chain is precisely a chain, so this is not
   hypothetical.
3. **Interpretation is graded, and the frame treats it as binary.** A seam using
   constrained decoding against a JSON schema is far more deterministic than a
   free-prose critique — the kit ships `structured-output-contract` as a skill
   *specifically* to move a seam along that axis. The frame should be able to
   record that a seam was **hardened**, and today it cannot. This is the most
   actionable of the three.
4. **Where the translating equipment itself belongs.** §10.1 types a rig as a
   system that performs the conversion, but the owner's point is that
   *non-rig* equipment performs it too, all the time, and is simply trusted.
   That trusted layer has no home in the frame and probably needs none — but
   "probably needs none" is not yet an argument.

---

## Appendix — sources

Load-bearing citations, so a later reader can check the argument rather than
take it.

| # | Source | What it supplies |
|---|---|---|
| 1 | Zave & Jackson, *Four Dark Corners of Requirements Engineering*, ACM TOSEM 6(1), 1997 | R / S / W and the entailment `S ∧ W ⊨ R` |
| 2 | van Lamsweerde & Letier, *Handling Obstacles in Goal-Oriented RE*, IEEE TSE 26(10), 2000 | obstacle analysis as the W test-generator |
| 3 | Welsh, Sawyer & Bencomo, *Towards Requirements-Aware Systems* (REAssuRE), ASE 2011 | design-time assumptions as monitored **claims** |
| 4 | ANSI/UL 4600, *Evaluation of Autonomous Products* (Koopman) | Safety Performance Indicators — a falsifier bound to one claim; the *pitfall* item type |
| 5 | ISO 21448 (SOTIF) | known/unknown × safe/unsafe; **ODD restriction** as a sanctioned response |
| 6 | SAE J3016 | the ODD concept and term |
| 7 | NASA-STD-7009B, *Standard for Models and Simulations* | Credibility Assessment Scale; credibility proportional to decision risk |
| 8 | FAA AC 20-107B; CMH-17 Vol. 3 | the building-block pyramid as a **cost-allocation** rule |
| 9 | Chen, Cheung & Yiu, *Metamorphic Testing*, HKUST-CS98-01, 1998 | MRs as oracle-free necessary properties |
| 10 | Barr, Harman, McMinn, Shahbaz & Yoo, *The Oracle Problem in Software Testing*, IEEE TSE 41(5), 2015 | why validation is expensive: no oracle at the world boundary |
| 11 | Faulkner, *Beyond the five-user assumption*, Behav. Res. Methods 35(3), 2003; Schmettow, CACM 55(4), 2012 | the honest limit on sparse human sampling |
| 12 | ISO/IEC/IEEE 15288:2023 | system-of-interest / **enabling system** / operational environment |
| 13 | Cobleigh, Giannakopoulou & Păsăreanu, *Learning Assumptions for Compositional Verification*, TACAS 2003 | an over-strong W is a defect |

