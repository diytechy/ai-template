# The validation gap and the assumption tier

**Status: PROPOSAL. Not a ruling.** It asks for one, because it changes the
frame that [`external.toml`](../requirements/external.toml) declares LOCKED.
The owner has answered most of its questions (§11). Those answers set the
direction the next sitting builds on. They are not the ruling itself, and
`external.toml` is unedited.

**It reverses part of sitting 2.** The direction taken here — the human as
their own entity, the frame drawn around the system in operation — undoes two
premises that several 2026-08-13 rulings rest on. §5.2 lists each one and
what happens to it, so the sitting reverses them deliberately rather than by
drift.

**What it proposes, in one sentence.** The kit records what the system must do
at its own interface and tests that exhaustively; it does not record the
assumptions that carry those interface facts up to the human outcomes its needs
are written about, and therefore cannot test them — so this proposes that those
assumptions become rows, that test cases may verify them, and that the depth-0
frame be redrawn around the system in operation, so that the crossing where an
outcome lands is one the frame actually holds.

**Who this is for.** The owner, as a decision document. It names what would
change and what it would cost before anything is built.

## The model at a glance

```
WHERE          EXT ◄── [B] ◄── IF ◄── SS ◄── LLR ◄── TC       SS = the SR tier, "the specification"
                                │
                                └── DA   assumption; optional, many-to-many with IFs

WHY    Stakeholder ◄── SN ◄── DA        when the SS's IF carries a DA
       Stakeholder ◄── SN ◄── SS        when it does not
```

- **The frame is drawn around the kit in operation** (§5), with the human as
  their own party. That reverses sitting-2 premises 13k and 13n, and the
  rulings built on them (§5.2).
- **An SS is stated over an IF, never a bare bundle.** Where the IF's reading
  does not settle the outcome, a DA on it says why it stands in (§6.2).
- **`[B]` is a bundle**: the IFs to one party in one direction, checked against
  the hand-kept `B` rows first and derivable later (§5.7).
- **Hats are lenses** applied to each piece. They mostly constrain existing
  rows, and they generate a DA's obstacles (§6.5).
- **Tests are owed on three fronts**, S, W and R-through-W, not one (§7).

**The work, in packages** (§10; all wait for the sitting):

| package | what | adopter migration? |
|---|---|---|
| 1. The sitting | reverse §5.2; redraw the frame; add DA rows and the stakeholder list | yes (schema), deferred |
| 2. Write the assumptions | DA rows for the 24 person-facing needs | no |
| 3. SS over IF | SRs cite IFs; the need link moves to the DA where one exists | yes (SR schema), deferred |
| 4. Test assumptions | TCs may verify a DA alone | yes (rule change), deferred |
| 5. Findings | warn-only checks | no |
| 6. Gate | every need reaches a DA or a waiver; opt-in | opt-in |
| 7. Derived boundary | drop the `B` rows, generate the view | yes, decided on its own |
| Hats per piece | the five-outcome record; `speaks_for` | template content |

Decisions and open questions: §11.

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
| SN | 27 | a human outcome for 24 of them — a team, reviewer, reader, owner, stakeholder or person; the other three (SN-006, SN-025, SN-029) are about an agent or an autonomous run |
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
It happens where a person operates the adopted kit, and today's frame puts both
of the needs above out of reach:

- SN-001's team sits inside `EXT-003` (Adopter), reachable only across
  `REL-001` — *"external-to-external, the system NOT a party"*, which *"must
  never grow a realizing IF row."*
- SN-002's reviewer reads the spine through `PROJECT_STATE.html` and the other
  generated surfaces, which ruling 13u declared *"NOT system outputs"* and
  folded into `REL-002`.

**So the crossings where this kit's stakeholder value lands were ruled outside
the frame.** Not by accident — the reasoning behind them is careful and
consistent (§5.2 traces it to one premise). The present frame is a
**delivery** frame, and delivery is not where any effect happens. The
consequence is that there is nowhere for validation to attach, which is why
there are 194 test cases and all 194 of them test the machine. §5 redraws the
frame so that there is.

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

In the kit's tiers: **R is the SN, S is the set of SRs, and W is what this
proposal adds.**

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

Roughly **45 of 167 seams (~27%) face a far side that interprets** — more
assumptions than one per need would suggest. That count prices §7(a).

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

`frame` stays written, per Q3. Once DAs and IFs link to each other (§6.2),
the rows also imply a value. An IF with no DA is coincident. An IF with a DA
is bridged by an assumption, and the crossing is `effect` where that DA's needs
belong to a stakeholder at a different party from the IF — authority, measured
at the session's `IF-134` but landing with the human. A check compares the written
value with the implied one, and a mismatch is a finding. Whether the written
value can eventually be dropped is left for later (Q10).

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
and delivers it.** The normal operating environment is an adopter's repo, and
the system is the kit as it runs there.

`B-05` does not go away, and the 69 SRs stated at it are not re-pointed. The
package still leaves the system. What changes is that its departure stops being
the *only* modelled crossing and stops being the one the stakeholder needs are
read against.

### 5.2 The sitting-2 rulings this reverses

Sitting 2 (2026-08-13) drew the present frame on two premises, both in its own
words:

- **13k** — the human and the loop are one entity: *"who-holds-authority is
  policy and record, never an entity split."*
- **13n** — the delivery frame: *"the system is the act of creating the
  guardrails and template contents … just because it happens to USE them as
  well doesn't mean they are each inputs into the system."*

This proposal reverses both. The human comes out (§5.4), and the system is the
kit in operation (§5.1). The rulings built on those premises follow:

| ruling / row | what it says | rests on | under this direction |
|---|---|---|---|
| **13u** — `B-03` removed | `PROJECT_STATE.html`, `open-items.html`, `docs/status.md` and `docs/gate` are *"not system outputs"* | 13k, 13n — the sitting doc itself says a separate human *"should be a deliberate reversal of 13k"* | **falls.** The human reading the spine is a crossing (§5.4). New id; `B-03` stays spent. |
| **`REL-002`** flow and notes | self-adoption; invoking `agent-resume` is *"NOT an input"*; carries 13u's surfacing | 13n, 13u | **shrinks** to the bare hand-off of the Template into an environment (§5.5) |
| **`REL-003`** (13n), and `IF-041`'s note | model providers *"touch the SESSION, never the system"*; the runner invocation *"crosses no boundary of this system"* | 13n and 13k — the ledger's only argument is *"the loop launching its CLI — the session driving itself"* | **reversed: becomes a crossing.** In operation the kit's own loop invokes the provider. Two parts survive: 13o's merge of primary and reviewer CLIs into one entity, and the backoff obligation on kit content. |
| **Hosted-CI cut** (2026-08-16q, not a sitting-2 ruling): `EXT-004`, `B-06`, `B-07` | *"this template has no design control over an external CI respecting configurations… all it can do is provide a method within the pack"*; `B-04`'s note: *"a hosted runner is an ADOPTER's boundary"* | 13n, the adopter entity, and `REL-002`/`REL-003` as cited precedent — plus **design control, which is independent** | **partly reversed.** Design control survives as the reason SR-151/152 constrain the shipped workflow *file*. It does not keep the runner off the frame: `interoperating` parties are outside the system's control by definition. It may return as a party (new ids: `EXT-006`+, `B-09`+). |
| **13o** — `B-08` removed | `check_vendored` *"would be run by the development environment; it's not an input directly into this design-scope system (its content input arrives via B-01's governed writes …)"* | 13n | **reversed, and the reason was incomplete.** The script compares each vendored file against its *"PINNED upstream raw URL"*, a network fetch that is not a `B-01` write. `IF-036` already calls the upstream *"a live question for the frame's owner"*. Whether it earns an entity is open: the input is opt-in, and this repo vendors nothing. |

The first two rows are certain, because their own text names the premise. The
last three were traced to their full log entries (`docs/log.md:1510-1566`,
`:3953-3984`; sitting-2 plan `:202-209`): `REL-003` and 13o rest only on the
reversed premises, and the hosted-CI cut keeps one independent reason that
does not decide its placement. `tests/test_external_frame.py` also asserts
`B-06`, `B-07` and `EXT-004` are absent (per the 2026-08-16q entry), so any
return is re-pinned under the same ruling.

### 5.3 Two planes, which `class` already separates

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

### 5.4 The human's three edges

The human touches the system three ways, not one:

| edge | what it is | row |
|---|---|---|
| human → **session** → system | **write, mediated**: the human edits a cell, the computer writes it, the hook floor admits it | `B-01`, governed writes in |
| human → **system** | **authority**: rulings, attestations, Status flips | `B-02`, authority in |
| system → **human** | **read**: the spine and the views generated from it — the dashboard, open items, status, gate reports | **new crossing**, out — the old `B-03` content, returned |

**Authority.** `interfaces.toml` singles `B-02` out:

> *"ONE CROSSING IS DELIBERATELY REALIZED BY NOTHING: `B-02` (authority in —
> rulings, attestations and Status flips) **has no port of its own.** Authority
> enters as CONTENT on B-01's write path: a human edits a Status cell and
> commits, and the hook floor admits that write as it admits any other."*

Under §3's test, the system can observe *that a Status cell changed*. It cannot
observe *that a human judged*. Only the proxy is shared.

> **`B-02` is this repo's first `effect` crossing, and its "realized by nothing"
> status is what an effect crossing looks like from inside a design frame.**
> Ports are design-frame objects, and authority is not a design-frame phenomenon.

**Read.** This is where SN-002 lands: the reviewer trusts the chain by reading
it. The system can see that it rendered a view. It cannot see that the reader
understood it, or that the understanding was right. So this crossing is also
`effect`, and it is where the render rig (§8.4) stands in for the reader.

Left inside `EXT-001`, the human gives this repo no `effect` crossing at all,
and the model would be correct and inert here. On the inside, the write and
authority edges land on `CMP-006` *"W1 Registry & conformance"*, and the read
edge on `CMP-009` *"W4 Human & adopter surfaces"*. What is missing is only that
the derived view does not yet connect a depth-0 crossing to the component that
serves it.

### 5.5 The adopter is dropped

`EXT-003` was *"the downstream team + repo"*. The operating frame already splits
that pair: **the team is the human operator**, and **the repo is the operating
environment the frame is drawn in**. Nothing is left for a third row to name.

- **One adoption hand-off remains.** Stripped of 13n and 13u (§5.2), `REL-002`
  is only *the Template is installed into an operating environment* — the
  Transition-stage hand-off (§8.1), in the evolution plane. `REL-001` said the
  same thing about a different repo, and in the operating frame "which repo" is
  not a party. One relationship carries it.
- **The value §1 located across relationships lands on crossings.** SN-001's
  team works through `B-01`, `B-04` and the read crossing; SN-002's reviewer
  reads through the read crossing.
- **`EXT-003` is spent and never re-minted**, following the
  `B-06`/`B-07`/`EXT-004` precedent in `external.toml`.

### 5.6 The proposed frame

The boundary view is **derived**: `gen_trajectory.py` builds the System-context
view from `external.toml` (`context_block(frame_context(root), ...)`, WI-455).
**Editing rows is editing the diagram.**

| row | change | plane |
|---|---|---|
| *new* Human operator | **add**, `operational`; owns `B-02` and the read crossing | operating |
| `EXT-001` Development session | **narrow** to the computer: shell, editor, OS, git client, working copy; owns `B-01`, `B-04` | operating |
| `EXT-005` Model provider | stays; `REL-003` becomes a crossing, prompt out and response in (§5.2); gains an inbound `emulates` | operating |
| hosted CI, vendored-doc upstream | **open**: may return as `interoperating` parties (§5.2); not counted below | operating |
| `EXT-002` Template | unchanged | evolution |
| `EXT-003` Adopter | **dropped** (§5.5) | — |
| *new* Scripted model runner | **add**, `enabling`, `emulates = "EXT-005"` | evolution |
| *new* Scaffold rig | **add**, `enabling`; emulates a fresh operating environment | evolution |
| *new* Render critic | **add**, `enabling`, `emulates` the human operator's reading | evolution |
| *new* read crossing | **add**, out, `frame = "effect"` | — |
| test infrastructure | **not shown** — inherent to defining a system, not a frame element | — |

`EXT-001` is the largest edit. Its description today folds in *"shell, git
client, OS, Python, editors, test runner, LLM runners"*: the human, the
environment, the test infrastructure **and** the model runner in one row.

**Counts.** Entities 4 → **7** (one dropped, one human, three rigs).
Crossings 4 → **6 or 7**: the read crossing, plus the model provider as one
crossing or an out/in pair. Relationships 3 → **1**: only the stripped `REL-002`
hand-off remains. Hosted CI and the vendored-doc upstream would add more if they
return. No SR's
`boundary_refs` is re-pointed, though SRs about the generated surfaces may move
from `B-05` to the read crossing. Next ids from `docs/id-watermark`: `EXT-006`,
`B-09`, `REL-005`. Costs are in §9.3.

### 5.7 The boundary as a derived view

A `B` row is a bundle: the collection of signals that pass between the system
and one party in one direction. Once each IF says which party it attaches to,
the bundles can be derived rather than hand-maintained. Grouping by party and
direction, against the live rows:

| today | party, direction |
|---|---|
| `B-01` governed writes | `EXT-001`, in |
| `B-02` authority | `EXT-001`, in ← **collides with `B-01`** |
| `B-04` verdicts | `EXT-001`, out |
| `B-05` template | `EXT-002`, out |

Today `B-01` and `B-02` would merge. After the redraw (§5.6), `B-02` belongs to
the human operator and `B-01` to the session, and every pair is unique,
including the read crossing. So the derivation reproduces the redrawn frame
exactly. Where two bundles carry different signals to one party in one
direction, an optional `bundle` label on the IF separates them.

The pattern already exists here: `components.derived.toml` is generated from
the rows that carry the obligation (*"do not hand-edit"*).

**What derivation needs:**

- **IFs name a party, not a bundle.** The 44 tie-backs convert mechanically,
  since each `B` has one entity. But 41 IFs name `"external:downstream
  adopter"` as free text, and that is the entity §5.5 drops. Reassigning them to
  the human operator or the operating environment is judgment, row by row.
- **An effect crossing enters through the WHY chain.** Every DA measures
  through an IF (§6.2), but the authority effect lands with the human while its
  IF (`IF-134`) attaches to the session. The human's inbound bundle is derived
  from the DAs whose needs belong to the human and whose IFs sit at another
  party: the crossing is where the effect lands, and nothing measures it there.
- **Some of `B`'s content is not derivable:** the `carries` intent, ruling notes
  such as `B-04`'s honest-limit paragraph, and approval status. The prose and
  status move to the EXT row, one entry per direction.
- **`frame` stays written and is checked against the rows (Q10)**, using the
  implication in §4. If the bundle rows are dropped in step 2, the written value
  moves to the EXT row with the prose.

**Two steps, so the second is a separate decision:**

1. **Keep the `B` rows, add the IF → party links, and check each `B` against
   its derived bundle.** A mismatch is a finding, which also tests whether the
   derivation holds.
2. **Once that check has held, drop the rows and generate the view.** `B` ids
   are cited 87 times in `system-requirements.toml` alone, and also in the
   rulings, the shipped `external.template.toml` and `test_external_frame.py`.
   This step is an adopter migration and a bigger change to the LOCKED frame
   than the redraw itself.

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
   one `holds_when` and one falsifier, citing the seams it covers, is
   PROCESS.md §3's 0→A→B rule applied to W.

### 6.2 Two chains: where it sits, and why it exists

The assumption sits between a bundle and the interfaces that measure it. The
need it serves sits on a separate chain, because a stakeholder need not touch
the system at all.

```
WHERE          EXT ◄── [B] ◄── IF ◄── SS ◄── LLR ◄── TC
                                │
                                └── DA   (optional; many-to-many with IFs)

WHY    Stakeholder ◄── SN ◄── DA        when the SS's IF carries a DA
       Stakeholder ◄── SN ◄── SS        when it does not
```

`SS` is the SR tier: the specification in Jackson's terms (§2). The prefix
stays `SR-` (Q9). `[B]` is the bundle, derived from the rows that attach to it
(§5.7). The input side is drawn; the output side mirrors it.

**The rule behind the WHERE chain.** An SS must be testable, so **it is stated
over a defined interface (an IF), never a bare bundle.** Where the IF's reading
does not settle the outcome, a DA on that IF states why it stands in for it.
This sharpens 13s (sitting-2 §3R), which already allowed a bundle *"as long as
it's broken down or clearly stated in the component details."* The IFs are
that breakdown; the SS now says which piece it is about. The recursion 13s
ruled stays clean: an SS cites IFs that attach to a party, and an LLR cites the
internal seams (124 of the 167 IFs today).

**Every DA measures through at least one IF.** This follows from the formalism:
S is stated over shared phenomena, which is what an IF is, and W connects those
phenomena to the world. An assumption with nothing observable on its near side
has nothing to connect. The one apparent exception was authority, which sitting
2 recorded as *"realized by nothing"*. But its proxy — a changed Status cell —
reaches the system as a commit, through `IF-134`, the hook floor's facing row
(`interface_from_external = "B-01"`). So the authority assumption measures
through `IF-134` like any other.

**Not every IF needs a DA.** A deterministic interface, like `subagent_gate`'s
exit code 0/2, is its own effect: that is `coincident`. Forcing a DA onto it
produces a row with no obstacle worth writing, which fails §6.3's filter. The
absence of a DA asserts coincidence, the same way `interfaces.toml` already
treats an absent tie-back as a statement.

**Why a DA is its own row, not optional fields on an IF.** The two are always
joined, but the join is **many-to-many**, and it carries its own evidence:

1. **One assumption spans many IFs.** *"The far side interprets, so its output
   needs judgement rather than comparison"* covers ~45 seams (§3). As IF fields
   it would be written 45 times: the cells-versus-rows argument of §6.1.
2. **One IF can carry several assumptions.** `IF-134` carries the authority
   assumption *and* the bypass limit `B-04`'s note already records
   (*"a local hook floor is bypassable (git commit --no-verify)"*).
3. **A test of an assumption needs an id that is not the IF's.** Otherwise a TC
   checking the IF's contract and a TC checking its assumption cannot be told
   apart (§6.1).

It is a row *kind*, not a new registry: `[assumption.DA-###]` rows sit in an
existing file, chosen by where their IF sits (§9.2). Most sit at the boundary,
but not all: an interpreting part *inside* the system, such as an embedded
model handing structured output to a script, puts W on an internal seam.

**The stakeholder is not in the WHERE chain.** A need can belong to someone who
never touches the system: SN-038 (*"an adopter can determine why every file
supplied by the kit exists"*) is one, and a legal or regulatory voice is
another. Stakeholders are a small list (Q12); a stakeholder may optionally link
to the EXT party it is, as the human operator does.

**Where the need link comes from — one of two places, never both.** A script
checks each SS:

- **(A) Its IF carries a DA.** The DA names the needs (`sn_refs`), and the SS
  carries none. The SS reaches its needs through the assumption that makes its
  interface mean something.
- **(B) Its IF carries no DA.** The SS names its needs itself, as every SR does
  today.

IFs never carry `sn_refs`. The rule is mechanical, and it keeps the need link
in exactly one place per SS. An SS inherits all the needs its DA names, which
is much finer than going through the party — the human operator will be the
stakeholder for ~24 of the 27 needs, and a link through the party would make
every SS at the human appear to serve all 24 (SN-002's failure mode, built into
the schema). The two edge cases stay strict (Q13): an SS over a DA-carrying IF
that serves a need the DA does not name means the DA is incomplete, so the need
is added to the DA; an SS stated over two IFs of which only one carries a DA
bundles two kinds of interface, so it is split, per 13s's one-shall guideline.

**The wiring this replaces**, for reference:

| row | links today |
|---|---|
| SR (79) | `sn_refs` → SN, `boundary_refs` → B; **no link to any IF** |
| IF (167) | tie-back → B for 44 (39 to `B-05`, 4 to `B-04`, 1 in from `B-01`); 124 internal; none for `B-02` |
| LLR (192) | `sr_refs` → SR, plus `component`, `module`; no link to any IF |
| TC (194) | `verifies` → SR / LLR; 8 also cite an IF |

An SR and its IFs meet only at `B` today, so an SR at `B-05` does not say which
of the 39 interfaces it is about.

**One stated exception.** SR-031, SR-034, SR-035 and SR-114 are the ruled
"package-wide property" class: a property of every delivered capability at
once. They apply to every IF in the Template's bundle, so they stay stated
against the bundle, as an exception named in the rule rather than a gap in it.

The row:

```toml
[assumption.DA-###]
sn_refs      = ["SN-002"]
measured_at  = ["IF-###"]       # required, one or more: the strict check's report, as rendered
assumption   = """A spine the strict check passes with zero orphans is one a
                  reviewer can rely on: each row says something, and the links
                  between rows are the ones a reviewer would draw."""
holds_when   = """Rows are authored under the spine-authoring question list;
                  the reviewer reads the generated views, not raw TOML."""
obstacle     = """Every row resolves and every row says nothing: an
                  orphan-free, semantically vacuous spine."""
falsified_by = "TC-###"         # the signal that would show this is false
status       = "Drafted" | "Approved" | "Falsified"
```

A rig's fidelity row adds `realized_by = "EXT-###"`, naming the rig entity
(§8.2). There is no `bridges_to` and no `boundary_refs`. Where an effect lands
at a different party from the IF — authority is measured at the session's
`IF-134` but lands with the human — the landing party comes from the need's
stakeholder, through the WHY chain.

**The missing-crossing rule.** A need whose stakeholder is an operating party,
with no DA and no SS stated over an IF of that party, is a finding: either the
frame is missing an interface, or the need names the wrong stakeholder.
`REL-001` and the read edge were both found this way, by hand.

Three cells are borrowed, each with a standard behind it:

- **`holds_when` is an ODD.** SAE J3016 / ISO 21448 / UL 4600 call the declared
  region within which a claim is asserted the *operational design domain*.
  Naming it after the established concept brings the **restriction move** with
  it (§7(d)).
- **`obstacle` is van Lamsweerde & Letier's obstacle**: the negation of a goal,
  requirement **or assumption**, refined until it reaches conditions satisfiable
  in the domain. It is a *generator*, not a comment (§7(b)), and hats are what
  drive the generator (§6.5).
- **`falsified_by` is the falsifier.** REAssuRE's monitored **claims** (Welsh,
  Sawyer & Bencomo, ASE 2011) and UL 4600's **Safety Performance Indicators**
  converge on it. The rule both imply is worth adopting outright, as a
  warn-first `trace.py` finding:

  > **An assumption with no declared falsifier is an untested assumption.**

Two more rows the redraw makes available at once:

```toml
[assumption.DA-###]
sn_refs      = ["SN-001"]
measured_at  = ["IF-###"]       # the harness verdict the operator reads
assumption   = """A scaffold whose harness runs green is one an adopting team
                  can actually work in: the profile fits their stack, and the
                  registries they must fill are discoverable without reading
                  the kit's source."""
holds_when   = """The team's stack is one of the shipped profiles, and the team
                  reads ADOPTING.md before first use."""
obstacle     = """A team green-scaffolds, never fills a registry, and operates
                  a spine that resolves and says nothing."""

[assumption.DA-###]
sn_refs      = ["SN-004"]
measured_at  = ["IF-134"]       # the hook floor admitting the commit
assumption   = """A changed Status cell on a human-held rung means a human
                  actually exercised the judgment that Status asserts."""
holds_when   = """The row's rung is at or below the `human_approval_through`
                  dial in docs/process.toml."""
obstacle     = """A Status change on a human-held rung arrives in a commit the
                  unattended loop authored."""
```

The second is what `Attest` and the attested-vs-mechanized split exist to
protect, stated for the first time as something falsifiable. Its `holds_when`
matters here: this repo sets `human_approval_through = "DevStg-Needs"`, so for
SR, LLR and TC rows a Status change *is not* a human act, by policy, and an
unscoped version of this assumption would be false. The obstacle names its own
falsifier: a Status change on a human-held rung in a loop-authored commit.
Whether an existing guard already detects that has not been checked; if one
does, that guard is the falsifier's TC.

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

The same filter covers the trusted layer — the OS, git, the terminal, the
interpreter. Where their failure is implausible there is no row; where it is
plausible and costly, a hat asks how the system responds (§6.5).

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

- **Hardening narrows the DA.** When an interpreting seam is hardened — say,
  schema-constrained output checked by a validator — the checked part moves
  into S, and the DA is rewritten to state only what remains assumed (*"the
  content is right"*, not *"the output parses and is right"*). There is no
  separate field for hardening; the narrower row is the record.

### 6.5 Hats: the lens applied to each piece

Stakeholders and hats do different jobs, and `hats.toml` already says so:

> *"A HAT IS NOT A PERSON AND NOT A STAKEHOLDER ROW. It is a QUESTION that must
> be put to every decomposition it applies to. A domain expert may have no needs
> of their own, yet their perspective constrains someone else's need — that
> constraint is what a hat carries."*

- A **stakeholder** owns an outcome. It is where SNs come from.
- A **hat** owns a failure class (`asks` + `listens_for`). It is where
  constraints come from.

They overlap in one place. Some hats are a stakeholder's voice used as a lens
(FIRST-RUN-ADOPTER, UX-DESIGNER); others are disciplines with no needs of their
own (SECURITY, CROSS-PLATFORM, LEGAL). An optional `speaks_for = <stakeholder>`
on the voice hats records that. It also settles FIRST-RUN-ADOPTER's loose end
(§9.3c): it was anchored to `EXT-003`, a **party**, when it should name a
**stakeholder** — the same conflation §6.2 separates.

**A hat constrains the specification; it does not always create a
requirement.** The data already behaves that way: 77 of the 79 SRs carry
`hat_refs`, and the package-wide property SRs (SR-031/034/035/114) are
hat-shaped constraints stated once for a whole bundle. Applied to the pieces of
the WHERE chain, a hat produces one of five things:

| a hat applied to… | produces |
|---|---|
| any row, and it does not bite | a recorded "not applicable" |
| an IF or SS | a **constraint**: a tightened acceptance clause on the existing SS (`hat_refs`) |
| a whole bundle | a **cross-cutting property**: one SS against the bundle (the package-wide class) |
| a gap nobody stated | a **new SS** — the rare case |
| a DA | an **obstacle**: the hat's `listens_for` is a failure class. UNATTENDED-OPS asking *"what happens when its input is missing, stale, or half-written?"* writes the DA's `obstacle` cell. |

The last row is the strongest fit: §7(b) says obstacles are *generated, not
imagined*, and hats are the generator.

The table is also a schema for a record `hats.toml` says is missing: *"WHAT IS
NOT BUILT YET … the per-decomposition RECORD of which hats were applied and
what each produced."* It is related to the SN-036 coverage record already in
status.md's unfiled follow-ups.

**The one real change:** hats fire today on SN → SR decomposition, keyed on
work-item and need tags. Firing them per DA or IF means those rows need tags,
or the composer runs per bundle.

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
one per need (§3 counts ~45 interpreting seams), so shared rows (§6.1) are what
keep it bounded.

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
what a user experiences. ISO/IEC/IEEE 15288:2023 (3.15) defines an enabling
system as one that *"supports a system-of-interest during its life cycle stages
but does not necessarily contribute directly to its function during
operation"*, and notes that *"each enabling system has a life cycle of its
own."* The stages are concept, development, production, utilization, support
and retirement (detailed in ISO/IEC/IEEE 24748-1:2024). Deployment is served by
the **Transition** technical process (6.4.10, retained in 2023), which installs
the verified system, with its relevant enabling systems, into its operational
environment. The kinds fall out of the stage axis:

| kind | what it enables |
|---|---|
| rig | Development stage — the Verification and Validation processes |
| test infrastructure | Development stage |
| deployment / delivery | the **Transition** process, into Utilization |
| procurement, warehousing | Production and Support stages |

The rows are this proposal's reading, not a list from the standard; the standard
itself gives one example, a production-enabling system.

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
| **does it stand in for something else?** | rigs only | an `emulates` cell and a fidelity DA |

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
  conversion holds. It is a DA alone.
- A **rig** converts it by *performing* the conversion: simulating the effect
  and putting the output against a rubric. It is a DA with `realized_by`.

**A rig plugs into an interface that already exists.** It presents the same
interface as the party it replaces, so the system's side is unchanged; only
what is plugged into the far side changes. That is also why rig evidence counts
toward validation and not only verification: a rubric run there runs on the
interface the user acts through. The registry records it in three places, none
of them new interfaces:

| | recorded as |
|---|---|
| the real party | `[entity.EXT-###]`, operating plane |
| the rig, as a system | `[entity.EXT-###]`, `class = "enabling"`, `emulates = "EXT-###"` — evolution plane |
| the interface both plug into | the **existing** `IF` rows, unchanged |
| its fidelity | a DA with `realized_by` naming the rig entity |

A rig costs one entity row, one cell and one DA. It adds no `IF` and no `B-##`
rows.

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
no DA naming it in `realized_by`** is a virtualized component whose fidelity
nobody has stated: a warn-first `trace.py` finding that fires on the rig's
existence.

### 8.4 The rigs this repo already runs

**The scripted model runner.** `IF-041` is the runner contract: `agent_session`
invokes the agent CLI headless, the prompt on stdin. `FAKE_AGENT`
(`tests/test_agent_loop.py:34`) answers that same contract: it records each
invocation and the model it was handed, then performs the next action from an
`actions.txt` script (`commit` / `done` / `blocked` / `noop`). **It simulates
`EXT-005`'s protocol, not its judgment**, and that is the right split: a model
good enough to stand in for a model is circular. The split belongs in its DA as
the delta (§6.4). `IF-041`'s note says the invocation *"crosses no boundary of
this system"*; that is 13n's reasoning, and the tie-back it lacks arrives with
`REL-003`'s re-examination (§5.2).

**The scaffold rig.** `tests/conftest.py:1-7`: *"The tests exercise the scripts
the way a downstream user would: bootstrap a real scaffold in a temp dir and run
the actual commands."* Materializing the package is `B-05`, ordinary
verification of an output. The *second* half is the rig: running the adopted
toolkit in a synthetic repo and judging that it comes up green, which emulates a
fresh operating environment through the harness's existing interfaces. SN-001's
acceptance is written at exactly that far side.

That rig also settled the old `REL-001` question. The registry's own rule —
*"a relationship ... must never grow a realizing IF row. **Wanting one means
what you have is a boundary crossing**"* (`external.toml:20-22`) — could not
coexist with a rig that had been standing at `REL-001` since before the frame
was drawn. Dropping the adopter (§5.5) resolves it.

**The render critic.** `render-dashboard-critique` screenshots
`PROJECT_STATE.html` across a declared width/theme/tab matrix so a critique
judges pixels, not ~790 KB of markup. The critique contract in
`PROCESS_OPTIONS.md` already makes a perceptual TC name its **artifact recipe**
beside its rubric, and `llm-vision-convergence-loop` requires two consecutive
approvals at one content hash. That is a rig standing in for the human reader
at the read crossing, a declared ODD and a repeatability control, with **no
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
sn_refs       = ["SN-023", "SN-024"]
measured_at   = ["IF-###"]      # the rendered view, on the read crossing
realized_by   = "EXT-###"       # the render critic
assumption    = """A vision model judging the rendered dashboard against the
                   rubric reaches the verdict a human reviewer would."""
holds_when    = """The model is image-capable; the rubric carries its accumulated
                   anchors; the artifact is a static render at a declared
                   width/theme."""
obstacle      = """A model revision shifts judgment silently; or the rubric
                   overfits to anchors accumulated under one model's eye."""
falsified_by  = "TC-###"        # a periodic human Attest sample that disagrees
status        = "Drafted"
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
`sn_refs` on the DA weakens the case for supplementing: the objection *"it no
longer says which requirement it discharges"* does not apply to a row that
names its need directly.

### 9.2 Where the rows live

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

**The savings are not unique to `external.toml`.** Any registry already in
`DECLARED_INPUTS` gets most of them: stakeholder needs, system requirements,
external, components and test cases. `interfaces.toml` is **not** in that list.
So the real choice is which existing file, and that decides **which rung
approves an assumption**, because off-spine approval follows each registry's
rung (`docs/process.toml`, OI-30 D3: `external` → DevStg-Boundary, `interfaces`
and `components` → DevStg-Arch).

**Not every DA sits at the boundary.** The owner's case: an LLM *inside* the
system, handing structured output to a mechanical script. That seam is internal,
yet it carries W — *"the model structures its output so the script can decode
it"* — because the far side interprets (§3's determinism axis). It is not rare
downstream: any bought-in part that interprets (an embedded model, a sensor, a
third-party parser; the kit's `PART` registry already holds such parts) puts W
on an internal seam. In this repo the model is `EXT-005`, outside, and
`REL-003` becomes a crossing (§5.2), so the case does not arise here yet. And
an internal seam is defined at DevStg-Arch, **after** the Boundary rung, so a
DA on it cannot be approved at Boundary: its IF does not exist yet.

**Decided (Q8): the DA's home and rung follow the IF it measures
through.** One row kind, two homes, mirroring 13s's recursion (an SS against a
boundary IF, an LLR against an internal seam):

| the DA measures through… | home | approved at |
|---|---|---|
| an IF attached to a party (boundary) | `external.toml` | DevStg-Boundary |
| an internal seam | `interfaces.toml` | DevStg-Arch, with the seam |

Cost of the second home: `interfaces.toml` is not in `DECLARED_INPUTS`, so the
stage fingerprint would not see those rows until it is added, which is needed
only once a gate reads DAs (step 6). The kit's `structured-output-contract`
skill is the hardening move for exactly this seam (§6.4).

**For boundary DAs: `external.toml`.** The owner has ruled that those DAs are
approved at **DevStg-Boundary**: *approving the boundary and the assumptions that
make that boundary possible are the same act* (a later rename to something like
`DevStg-BoundaryAssumptions` is possible). `external.toml` is the one file
already on that rung and in the stage fingerprint. `interfaces.toml`, the other
natural neighbour since every DA measures through an IF, approves at
DevStg-Arch and is not fingerprinted.

Two consequences to accept with it:

- **Who approves, in this repo.** The dial is `human_approval_through =
  "DevStg-Needs"`, which would let the loop approve assumptions about the world —
  the §8.5 concern. The owner has decided to move it to DevStg-Boundary at the
  sitting (Q14), so
  boundary DAs are human-approved. Internal-seam DAs, at DevStg-Arch, stay under
  ordinary review.
- **The lock's scope.** `external.toml`'s header says *"its rows change only by a
  recorded ruling."* The owner has decided to narrow it (Q15): entity, boundary
  and relationship rows change only by ruling; DA rows follow ordinary
  Boundary-rung approval under the dial.

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
`test_external_frame.py:371`), and the four live rows.

**(b) `[assumption.DA-###]` row kind — 8 mandatory edits**

The four above, plus `OFFSPINE_KEYS` (new `DA-ID`), `OFFSPINE_TABLE`
(`"DA-ID": "assumption"`), a `TOML_REGISTRIES` entry **and** its floor
(`test_dogfood_sync.py:433` asserts `set(floors) == set(TOML_REGISTRIES)`), and
`trace.py:920-928` `_offspine_ids` for the id watermark. The watermark is not
optional: the missing-watermark hole has happened here twice (IF-121/122 and
OI-26). Then behaviour: `trace.py` must resolve the DA's `sn_refs`,
and `measured_at` (required, one or more IFs).

**(d) SS stated over an IF (§6.2) — a schema change that ships**

- The SR schema gains a citation of the IFs it is stated over. It ships to
  adopters, so it needs a resync entry.
- A check enforces the need-link rule: an SS over a DA-carrying IF has no
  `sn_refs`; an SS over an IF with no DA has them.
- All 79 SRs are re-annotated. The 69 at `B-05` each choose among its 39 tie-back
  IFs. 13s anticipated exactly this work: *"it should help to expose if there
  are some other issues in the way this system has been decomposed."*
- IFs gain a party link (§5.7), and no `sn_refs`. The 44 tie-backs convert
  mechanically; the 41 `"external:downstream adopter"` rows need judgment.
- `boundary_refs` on the SR becomes derivable, except for the package-wide
  property exception.

**(e) Dropping the `B` rows (§5.7 step 2) — a separate decision**

The 87 `B` citations in `system-requirements.toml`, the rulings,
`external.template.toml`, `test_external_frame.py` and the context-view
generator all move to the derived bundle. An adopter migration.

**(f) The stakeholder list (Q12) — a new row kind, about the same as (b)**

A stakeholder id prefix, its watermark entry, template example rows, the
dogfood-sync floor, `trace.py` resolution of each SN's stakeholder citation,
and an optional link to an EXT party. It lives in `stakeholder-needs.toml`,
which is already fingerprinted and approves at DevStg-Needs.

**(g) Hats applied per piece (§6.5)**

Firing hats per DA or IF needs tags on those rows, or a composer that runs per
bundle. The five-outcome record is the artifact `hats.toml` says is not built,
and FIRST-RUN-ADOPTER's `speaks_for` needs (f) to exist first.

**(c) The frame redraw (§5.6) — a sitting**

- `tests/test_external_frame.py:87-114` pins *exactly* 4 entities, 4 crossings
  and 3 relationships plus the spent-id gaps, and `:128-146` pins every `status`
  to `Approved`. Its docstring says it **is expected to be edited by a sitting
  and by nothing else**. The redraw re-pins all three counts, adds `EXT-003` to
  the spent ids, and adds `emulates` to the entity schema.
- **The reversed rulings (§5.2) carry prose with them.** `REL-002`'s flow and
  notes, `EXT-005`'s description, `IF-041`'s note and `B-04`'s note each state
  13n's reasoning, and each needs rewriting in the same sitting.
- `tests/test_hats.py:885-900` names `EXT-003 Adopter` as the entity the
  FIRST-RUN-ADOPTER review hat speaks for. WI-453 re-pointed the hat's predicate
  away from the id, so nothing breaks, but the hat needs a new anchor: a
  stakeholder via `speaks_for`, not a party (§6.5).
- `docs/log.md` and the sitting-2 plan cite `EXT-003` and 13u historically. They
  are records and stay as written.

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
Nothing is built before the sitting: typing `frame` on today's four `B` rows was
once a separable first step, but the redraw changes who owns `B-02` and SSs
will cite IFs rather than bundles, so it is folded into step 1.

**Step 1 — the sitting.** Reverse the §5.2 rulings deliberately; land the §5.6
rows (§9.3c) with `frame` on the redrawn bundles (§9.3a); add the DA row kind
to `external.toml` at the DevStg-Boundary rung, narrowing the file's lock to
the frame rows (§9.3b; Q8, Q15); move `human_approval_through` to
DevStg-Boundary (Q14); add the stakeholder list (§9.3f). The internal-seam home
in `interfaces.toml` (Q8) waits until a seam needs it.

**Step 2 — write the assumptions.** DA rows for the 24 person-facing needs, each
measured at the IFs it bridges. They exist today as the unstated gap between
each `need` and its `acceptance`, so this is transcription, not invention.
Warn-only; nothing gates. Expect this step alone to surface real defects.

**Step 3 — state each SS over an IF.** The §9.3d schema change: IFs gain their
party link; each SS cites the IFs it is stated over; the need link moves to
the DA where one exists (§6.2's rule); each `B` row is checked against its
derived bundle (§5.7 step 1). Warn-only.

**Step 4 — let test cases verify an assumption.** Allow `DA-###` as a `Verifies`
target, standing alone (Q5, §9.1), and add the evidence descriptor (§7(e)).
Start with the metamorphic subset (§7(c)), which is nearly free.

**Step 5 — the warn-first findings.** `trace.py` warns on:
- an `Approved` DA with no `falsified_by` (§6.2);
- a rig row with `emulates` and no DA naming it (§8.3);
- a need whose stakeholder is an operating party, with no DA and no SS over an
  IF of that party (§6.2);
- an SS stated over a bare bundle, outside the package-wide exception (§6.2);
- an SS whose need link breaks the one-place rule (§6.2);
- a `Falsified` DA, reported with every IF, SS and TC it reaches (§11, closed item 1);
- a Status change on a human-held rung in a loop-authored commit — the authority DA's falsifier (§6.2).
- a `B` row that differs from its derived bundle, or a written `frame` that
  differs from the implied one (§4, §5.7).

**Step 6 — the gate, if wanted.** The vision promises work built *"test-first
with explicit approval gates so you can trust what ships."* Steps 2–5 only
warn, so without this step DA rows are optional documentation. The gate:
**`DevStg-Tests` requires every need to have at least one DA, or a recorded
waiver stating that its SRs alone deliver it** — the need-level form of
`coincident`. It is keyed on the **need**, because that is where the argument
lives: a gate keyed on SRs at `effect` crossings would check only the handful
at `B-02` and pass SN-001 and SN-002. **The only step that costs an adopter
anything mandatory; opt-in with an applies-when**, per the proportionality
doctrine.

**Step 7 — generate the boundary, if the check has held.** Drop the `B` rows
and derive the view (§5.7 step 2, §9.3e). An adopter migration, decided on its
own.

**Hats per piece (§6.5, §9.3g)** can land any time after step 1's stakeholder
list.

**Adopter migration is deferred, deliberately.** No adopter has taken a spine
update for some time. Once this repo's model is firm, the resync entries are
written against the real gaps rather than planned now (§9.4).

**Not proposed: a new stage rung.** The recursion already oscillates Reqs↔Arch,
and this concept rides existing rungs.

---

## 11. Decisions and open questions

Owner answers, 2026-09-21 and 2026-09-22. `DECIDED` means the next sitting may
build on it; `OPEN` means it may not.

| # | question | standing |
|---|---|---|
| Q1 | Does the human come out of `EXT-001`? | **DECIDED: yes** (§5.4). The answer widened into the enabling-systems thread (§8). |
| Q2 | Does `REL-001` become a crossing? | **DISSOLVED** by dropping the adopter (§5.5): the value it guarded lands on the operator's crossings. My reading of the owner's decision to drop the adopter. |
| Q3 | `frame` vocabulary: two values or three? | **DECIDED: three**, keep `coincident` (§4). Deriving coincidence from topology considered and not adopted. |
| Q4 | How heavy is the evidence descriptor? | **DECIDED: `assumed \| sampled \| monitored`**, CAS as the escalation path (§7(e)). Agreement to the cheap option, not a finding that the heavy one was wrong; revisit first if the descriptor starts carrying weight. |
| Q5 | Does a W-test supplement an SR citation, or may it stand alone? | **DECIDED: stand alone, for DA ids only.** A DA names its needs, so a TC verifying one says what it serves; `coherence.py`'s supplement rule gains a narrow exception, not a general loosening (§9.1). |
| Q6 | Does a rig get its own crossing? | **DECIDED: no.** A rig is an `enabling` entity with `emulates`, plugged into the existing interface, with a fidelity DA (§8.2). |
| Q7 | Does this ship downstream in v1? | **DECIDED in principle: yes**, once the sitting has nailed down the details. Adopter migration and resync documentation are deferred until this repo's model is firm (§10). |
| Q8 | Which existing file holds the DA rows? | **DECIDED: home and rung follow the IF.** Boundary DAs in `external.toml` at DevStg-Boundary; DAs on internal seams, like an embedded LLM feeding a script, in `interfaces.toml` at DevStg-Arch, added when a real seam needs it (§9.2). |
| — | Orientation, the adopter, and the reversed rulings | **DECIDED:** operating frame, two planes, `EXT-003` dropped, 13u reversed (§5). **Traced 2026-09-22:** `REL-003` and 13o reversed; the hosted-CI cut (2026-08-16q) partly reversed — design control survives but does not keep the runner off the frame (§5.2). Whether hosted CI and the vendored-doc upstream return as parties is open. |
| — | Two chains | **Agreed 2026-09-22:** WHERE is `EXT ← [B] ← IF ← SS`, with an optional DA on the IF (many-to-many); every DA measures through at least one IF, authority included (`IF-134`). WHY is `Stakeholder ← SN ← DA`, or `← SS` when its IF carries no DA. An SS is stated over an IF, never a bare bundle, except the package-wide class (§6.2). |
| — | Hats | **Agreed 2026-09-22:** a hat is a lens that constrains, not a stakeholder; five outcomes per piece; `speaks_for` on voice hats (§6.5). |
| Q9 | Rename SR to SS (system specification)? | **DECIDED: prose now, prefix later.** Docs call the tier "the specification" now; the `SR-` prefix stays until a separate, deliberate adopter migration (§6.2). Note: in conventional SRS usage *specification* names the document and its entries are *requirements*, so "system requirement" is the standard entry name. That leaves "prefix never" open as the likely outcome (appendix). |
| Q10 | Derive `frame` from which rows exist, instead of writing it? | **DECIDED: write it, check the derivation.** Q3's explicit word stands; a check compares it with the derivation (no DA = coincident, IF + DA = bridged, DA without IF = effect). Whether to drop the written value is decided later (§5.7). |
| Q11 | Where does an SS's need link come from? | **DECIDED, then refined by the owner:** one place, never both — from the DA when the SS's IF carries one (the SS has no `sn_refs`), otherwise from the SS itself. IFs carry no `sn_refs`. A script checks it (§6.2). |
| Q12 | Where does a stakeholder live? | **DECIDED: a small stakeholder list.** Named rows, likely in `stakeholder-needs.toml`; each SN cites one, hats' `speaks_for` points at one, and a stakeholder may optionally link to an EXT party (§6.2, §6.5). |
| — | DA approval rung | **DECIDED: DevStg-Boundary.** Approving the boundary and the assumptions that make it possible are the same act; a later rename such as `DevStg-BoundaryAssumptions` is possible (§9.2). |
| — | Step 1 | **DECIDED:** folded into the sitting; nothing is built before it (§10). |
| — | Packaging | **DECIDED:** split into packages for the sitting; a model-at-a-glance summary opens the doc. |
| Q13 | Need-link edge cases | **DECIDED: fix the DA or split the SS.** A need the DA does not name is added to the DA; an SS over mixed IFs is split (§6.2). |
| Q14 | Should DA approval be human-held here? | **DECIDED: move `human_approval_through` to `DevStg-Boundary`, at the sitting**, in the same ruling that adds DA rows. SRs and below stay under ordinary review (§9.2). |
| Q15 | Does `external.toml`'s lock cover DA rows? | **DECIDED: narrow the lock.** Entity, boundary and relationship rows change only by ruling; DA rows follow Boundary-rung approval under the dial (§9.2). |
| — | Enabling-system stage vocabulary | **Tentative.** Placed, not settled; the standard wording is now verified (§8.1). |

### Formerly "not captured" — closed or scheduled (owner, 2026-09-23)

1. **Blast radius → a status and a report (step 5).** Example: one DA covers
   every seam where the kit consumes model output (*"the model runner follows
   the runner contract"*, measured at `IF-041` and its neighbours). A provider
   changes its CLI's exit codes; the DA is false, and every SS over those IFs
   loses part of its argument at once. `measured_at` already lists them. Added:
   a `Falsified` DA status, and a derived report — *DA falsified → these IFs →
   these SSs → these TCs no longer prove their need.*
2. **Chained assumptions → closed, no machinery.** An SS emits something that
   crosses another IF with its own DA, so a need's argument is the conjunction
   of every DA on its path: Jackson's flat conjunction is enough. Assumptions
   only surface possible gaps, and depth does not change the response. Item 1's
   report walks the chain anyway.
3. **Graded interpretation → closed by authoring rule (§6.4).** A hardened seam
   moves part of W into S: with schema-constrained output and a validator,
   *"the output parses"* becomes checked, and only *"its content is right"*
   stays assumed. No field records the hardening; the seam gets a narrower DA.
   Testing the remaining content half is a judge-and-rubric job, triggered by
   events such as a model change rather than every run — which the render
   critic's `holds_when` already expresses.
4. **The trusted layer → closed by §6.3 and §6.5.** Everything outside design
   scope that carries our signals (OS, git, terminal, interpreter) is handled
   where a boundary is broken down, in proportion to risk. Implausible failure:
   the obstacle test gives no row. Plausible and costly: a hat such as
   UNATTENDED-OPS or INTEGRITY-RECOVERABILITY asks what happens when the input
   is missing or corrupt, and the answer is an SS (detect and respond) or a DA
   (knowingly assume). Precedent: running with git off PATH exposed a hook
   defect (WI-333, recorded in `conftest.py`).
5. **The authority DA's falsifier → a step-5 finding.** Prevention exists: the
   dispatcher routes attestation and gate work on human-held tiers to *surface*
   rather than execute (`dispatch.py` `_kind_action`). No after-the-fact
   detection was found. Added: *a Status change on a human-held rung, in a
   loop-authored commit, is a finding* — the check that makes the assumption
   testable.

**Standards, verified 2026-09-22.** The 15288:2023 definition (3.15), the stage
names (via 24748-1:2024) and the Transition process (6.4.10) were checked against
the published standards' free previews and SEBoK. The §8.1 table of enabling-system
kinds is this proposal's reading, not a list in the standard. The IEEE 830 /
29148 item is in the appendix.

---

## Appendix — the conventional SRS, mapped

A cross-check against the usual outline of a System Requirements Specification
(SRS): *what* the system must do and how well, without *how* it is built. The
model above covers every element. Nothing here proposes a change.

| SRS element | where it lives in this model |
|---|---|
| Purpose, scope, definitions | the README's `PROJECT-VISION:` tag, each need's Scope, `PROCESS.md` |
| System context | the depth-0 frame (§5), becoming a derived view (§5.7) |
| Major functions | needs and components |
| User characteristics | the stakeholder list (Q12) |
| Constraints | `performance-budgets.csv`, the dependency ledger, `stack.ini`, and hat-produced constraints (§6.5) |
| **Assumptions** | **the DA rows. Empty in the kit today: the gap §1 found.** |
| Functional / non-functional | implicit in how an SS originated: see below |
| Interface requirements | IF rows, which an SS is stated over (§6.2) |
| Exclusions (no design detail) | the SR / LLR split, and SN-033's check that needs name no mechanism |

**Assumptions are a standard section, not an invention of this proposal.** The
conventional outline gives them their own slot, so §1's finding is also a gap
against ordinary practice. IEEE 830-1998's prototype SRS outline carries
*"2.5 Assumptions and dependencies"* under *"Overall description"* (guidance in
clause 5.2.5: the factors whose change *"can affect the requirements"*). Its
successor, ISO/IEC/IEEE 29148 (2011, revised 2018), keeps the item (2018:
9.6.8). Verified 2026-09-22 against a course copy of 830 and IEEE SA's catalog
entry; the 29148 clause number came from an unofficial copy, so cite the
catalog entry rather than the number.

**No functional / non-functional category.** The split is binary and adds
nothing the kit cannot already read. SRs carry an optional `aspect` (a closed,
cross-cutting review grouping — process, trajectory, unattended-loop,
connectivity, perf, portability; filled on 31 of 79, never gated), and the
non-functional kind are what hats produce as constraints (§6.5).

**Lifecycle is an enabling system** (§8.1), not yet exercised by a project.

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
| 12 | ISO/IEC/IEEE 15288:2023 (3.15, 6.4.10); ISO/IEC/IEEE 24748-1:2024 | **enabling system**; the Transition process; life-cycle stages |
| 13 | Cobleigh, Giannakopoulou & Păsăreanu, *Learning Assumptions for Compositional Verification*, TACAS 2003 | an over-strong W is a defect |
| 14 | IEEE 830-1998 (superseded by ISO/IEC/IEEE 29148:2011, rev. 2018) | the SRS outline's "Assumptions and dependencies" section |
