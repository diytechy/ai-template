# The validation gap and the assumption tier

**Status: PROPOSAL. Not a ruling.** It asks for one, because it changes the
frame that [`external.toml`](../requirements/external.toml) declares LOCKED.

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
by the system**, which is Jackson's shared-phenomena test:

> A crossing is `design` if the system can detect that it happened.
> It is `effect` if the need names an outcome there that the system cannot see.

This makes the central claim countable rather than rhetorical: **the V&V gap is
the set of phenomena a requirement names that the system cannot observe.** "The
gap grows with complexity" stops being a slogan and becomes something a row can
be measured against.

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
plant the kit depends on and cannot simulate.

So: **two boundary types, one entity class, one new row kind.** Not three
boundaries.

---

## 5. Three test obligations, not one

If the argument is `S ∧ W ⊨ R`, then evidence is owed on three fronts. The kit
currently collects one.

| # | verifies | where evidence sits | cost | cadence |
|---|---|---|---|---|
| **1** | **S** | the design crossing | cheap | every commit — *this is all 194 TCs today* |
| **2** | **W** | the assumption itself | cheap-to-moderate — *free where it is expressible as a metamorphic relation (§6c)* | continuous |
| **3** | **R through W** | the effect crossing, via a translation layer | expensive | sparse, sampled — *and see the limit in §6* |

Obligation **2** is the new idea and the important one. Tests of W are often not
software tests at all — they are measurements of the world, monitors, sampled
observations, or a recorded check that a stated precondition still holds. For
SN-001's assumption, a W-test is *"take a shipped profile, scaffold it, and have
someone who has not read the source reach a first filled registry"* — not cheap,
but enormously cheaper than validating "an adopting team gets a working
process", and it fails in the same direction.

Obligation **3** is validation proper, and it is expensive by nature. The point
of the proposal is **not** to make it cheap. It is to make it *rare and
targeted* by putting obligation 2 underneath it.

---

## 6. Why this is affordable

Three mechanisms, in the order they matter.

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

1. **Does the human come out of `EXT-001`?** `EXT-001`'s own note calls this an
   open follow-on. Under this proposal it is decisive: if the human stays folded
   into "Development session", this repo has **no `effect` crossing at all** and
   every `frame` value is `design` — the model would be correct and inert here
   while still working downstream. Splitting the human out is what makes the kit
   able to dogfood its own validation story. It is also the more invasive
   change.

2. **Does `REL-001` become a crossing?** §1's finding is that the kit's
   stakeholder value lands across a relationship declared not-a-party. Either
   that ruling stands — and the kit accepts that it cannot validate its central
   claim, recorded as such — or `REL-001` is re-framed as an `effect` crossing
   and the frame grows. Both are defensible; drifting between them is not.

3. **`frame` vocabulary: two values or three?** `coincident` costs a word and
   buys an explicit claim. The alternative is two values plus the convention
   that a single row may be cited by both kinds of requirement.

4. **How heavy is the evidence descriptor?** A 0–4 CAS-style ordinal is
   defensible and citable; a three-value `assumed | sampled | monitored` is
   cheaper and probably enough for a kit this size. My recommendation is the
   three-value form, with the CAS cited as where to go if a project needs more.

5. **Does a W-test supplement, or may it stand alone?** (§7.1.) The `IF-###`
   precedent says a TC citing only off-spine ids is an orphan. My reading is
   that an assumption belongs to some requirement's argument and should
   therefore supplement — but a W-test of *"zero orphans ⟹ a reviewer trusts
   it"* does not obviously discharge any single SR, so this needs deciding
   rather than defaulting.

6. **Does any of this ship downstream in v1, or is it dogfooded here first?**
   Given the template/instance sync constraint and the 20 bytes free in
   `AGENTS.template.md`, shipping the schema and holding the enforcement is the
   low-risk path.

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

