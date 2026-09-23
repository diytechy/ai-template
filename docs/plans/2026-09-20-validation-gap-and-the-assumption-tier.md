# The validation gap and the assumption tier

**Status: PROPOSAL. Not a ruling.** It asks for one, because it changes the
frame that [`external.toml`](../requirements/external.toml) declares LOCKED.
The owner has answered most of its questions (§11). Those answers set the
direction the next sitting builds on. They are not the ruling itself, and
`external.toml` is unedited.

**Revised after an adversarial review (2026-09-23, §11.2).** A codex Sol review
(reasoning effort high) rejected the previous draft as written: its central
joins could not be computed from the declared data. Every finding was checked
against the code before being applied. The revision keeps the direction and
changes the mechanics. Six owner answers are **reopened** with a proposed
replacement rather than silently changed: Q3, Q5, Q8, Q10, Q11 and Q13 (§11).

**It reverses part of sitting 2.** The direction taken here — the human as
their own entity, the frame drawn around the system in operation — undoes two
premises that several 2026-08-13 rulings rest on. §5.2 lists each one and
what happens to it, so the sitting reverses them deliberately rather than by
drift.

**What it proposes, in one sentence.** The kit records what the system must do
at its own interface and tests that exhaustively; it does not record the
assumptions that carry those interface facts up to the human outcomes its needs
are written about, and so cannot test them — so this proposes that those
assumptions become rows the requirements cite, that test cases may evidence
them, and that the depth-0 view show the system in operation beside the system
that delivers it, so that the crossing where an outcome lands is one the frame
actually holds.

**Who this is for.** The owner, as a decision document. It names what would
change and what it would cost before anything is built. A rendered mockup of
the resulting depth-0 view is in [`mockups/`](mockups/depth0-operating-frame.html).

## The model at a glance

```
OPERATING FRAME   system-of-interest: the kit, as it runs in a repository
                  EXT (party) ◄── [B] ◄── IF ◄── SR ◄── LLR ◄── TC ── verifies
                                        ▲        │
                                        │        └─ da_refs ─► DA ── effect_at ─► [B] where the outcome lands
                                        └──────── measured_at ──┘

DELIVERY FRAME    system-of-interest: this repository, building and releasing the kit
                  Template ◄── B-05 ◄── IF ◄── SR …          rigs (enabling) ── emulates ─► operating parties
                  Template ── Transition hand-off ─► the operating environment

WHY               Stakeholder ◄── SN ◄── SR   (sn_refs, unchanged)     a DA's needs = its citing SRs' needs
EVIDENCE          TC ── verifies ─► SR / LLR          TC ── assumption_refs ─► DA
```

- **Two frames in one view** (§5.1). The kit in operation is the
  system-of-interest; this repository's build-and-release is its enabling
  system and emits the Template. A row's `class` decides its frame.
- **Bundles keep their authored identity; membership is derived** from IF
  tie-backs, as the dashboard already does (§5.7).
- **An SR defines one interface, or rests only on an assumption** — never a
  bare bundle, except the package-wide class (§6.2).
- **An assumption is its own row**, cited by the SRs whose argument needs it,
  measured through the IFs whose reading it interprets, and naming the bundle
  where the outcome lands (§6.2).
- **Every boundary interface is classified**: bridged by a DA, or explicitly
  `coincident`. Absence is unknown, not coincidence (§4).
- **Hats are lenses** that constrain existing rows and generate obstacles (§6.5).
- **Tests are owed on three fronts**, S, W and R-through-W (§7).

**The work, in packages** (§10; all wait for the sitting):

| package | what | adopter migration? |
|---|---|---|
| 1. The sitting | reverse §5.2; redraw the frames; DA row kind; stakeholder list; boundary IFs approved at Boundary | yes (schema), deferred |
| 2. Write the assumptions | DA rows derived from the person-facing needs, each a new Drafted claim | no |
| 3. SRs define IFs | each SR names the IF it defines (minting the missing ones) and the DAs it rests on | yes (SR schema), deferred |
| 4. Evidence for assumptions | TCs cite DAs through their own field | yes (TC schema), deferred |
| 5. Findings | warn-only checks | no |
| 6. Gate | every path bridged or coincident; opt-in | opt-in |
| Hats per piece | positive provenance only; `speaks_for` | template content |

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
| TC | 194 | 189 automated, 5 not |
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
**delivery** frame, and delivery is not where any effect happens.

**Validation is not absent; it is sparse, untyped and stale.** SR-054
(dashboard usability) is rubric-adjudicated, and TC-055 verifies it with a
Critique run by a fresh session over rendered screenshots. TC-036 and
TC-209–211 are Inspections. Five TCs are not automated. But none of that
evidence says which assumption it tests, nothing re-runs it (TC-055 records
*"a one-time judgement that nothing re-fires"*), and nothing asks where the
rest of the gap is. The missing piece is structured assumption provenance and
a refresh policy, not the first human check. §5 redraws the frame so the
assumptions have a place to attach.

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
| **observability** | can the system, or something built to watch it, detect that the outcome happened? | the outcome lands where nothing built can see it; W bridges to it |
| **determinism** | does the far side *compute*, or *interpret*? | seeing the exchange does not tell you it was right; W covers the interpretation |

**Observability** is Jackson's shared-phenomena test. **Determinism** is the
oracle problem (Barr et al. 2015). A seam facing a model is fully observable:
the system sees the call, what it sent, and what came back. None of that says
the answer was right, because the far side interpreted rather than computed.

The set of phenomena a requirement names that the system cannot observe is
therefore a countable **lower bound** on the V&V gap, not the whole of it.

It is also not a small corner. Of the 167 IF rows, 52 name an external endpoint:

```
41 rows  external:downstream adopter   the adopting team — interprets
 4 rows  external:agent CLI            the model runner — interprets
 3 rows  external:git                  computes
 3 rows  external:run.* launchers      computes
 1 row   external:upstream docs        computes
```

About **45 rows face a far side that interprets**. Separately, 43 IF rows tie
back to a boundary bundle (44 tie-back references, because `IF-134` ties to two)
and 124 are internal seams.

---

## 4. Classifying crossings — design, effect, coincident

The formalism's own nouns, "machine" and "world", are precise inside Jackson and
drift badly outside it. So the proposal names **crossings**, since crossings
are what the registry holds, with three words:

- **`design`** — the system can observe and act here. **Verification** lands
  here.
- **`effect`** — where the outcome a need names actually occurs, frequently not
  observable by the system. **Validation** lands here.
- **`coincident`** — the reading *is* the outcome: design and effect are the
  same thing at this point.

**Where each word lives (revised, §11.2).** The previous draft put one written
`frame` value on each boundary bundle. The review showed a bundle cannot carry
one scalar: `B-05` alone has 39 interfaces, some coincident, some bridged by an
assumption, some not yet classified. So the words move to where they are true:

| word | lives on | how |
|---|---|---|
| `coincident` | a boundary **IF** | an explicit waiver cell, `coincident = "<why the reading is the outcome>"`. A CLI whose parsed token is the token the user typed is coincident; saying so costs one line and is reviewable. |
| bridged (`design` with an assumption) | a boundary **IF** | derived: some DA lists the IF in `measured_at` |
| `effect` | a **bundle** | derived: some DA names the bundle in `effect_at` |
| `design` | a **bundle** | derived: no DA lands there |

**Absence is unknown, not coincidence.** A boundary IF with neither a waiver
nor a DA is *unclassified* — a warn-first finding, never an implied
`coincident`. This keeps the doctrine that an empty cell asserts nothing, which
the previous draft broke by reading "no DA" as coincidence.

**A rig does not move an outcome.** The previous draft said building a rig
could move a crossing from `effect` to `design`. It cannot: a rig observes a
*model* of the world, not the world (§8.2). The outcome stays where `effect_at`
says; the rig adds a fidelity assumption and proxy evidence beside it.

### The candidates, assessed

| candidate | verdict |
|---|---|
| `machine` / `world` (Jackson, Zave) | Citable and exact. Keep in the rationale; reject as the shipped noun: "machine" reads as hardware, and "world" drifts into "deployment environment". |
| `solution domain` / `problem domain` | Established, but the cut is wrong — the problem domain is the whole problem context, not the place the outcome lands. |
| `system-of-interest` / `operational environment` (ISO/IEC/IEEE 15288:2023) | The strongest *established* pair, and normative. Adopted for the frames (§5.1). It names **systems**, not crossings, so it does not replace the three words. |
| `ODD` — operational design domain (SAE J3016, ISO 21448, UL 4600) | **Adopt, for a different cell**: the assumption row's `holds_when` (§6.2). |
| `design system` / experience | **Unusable.** In software, "design system" means a UI component library. |
| `design boundary` / `experience boundary` | No collision, weak currency. "Experience" is human-centric, wrong for a kit that also ships to physical projects. |
| `control` / `effect` | "Control" collides with control theory *and* with this repo's own `B-02` authority crossing. |

---

## 5. Two frames: the kit in operation, and the system that delivers it

### 5.1 The orientation, and why it needs two frames

The owner's direction: the frame used to be oriented toward **the entire package
that developed the product**. It is now oriented toward **the system the user
experiences, as well as the enabling system that develops and delivers it.**

The previous draft tried to hold both in one system-of-interest, and the review
showed why that is incoherent: in an operating frame the installed Template *is*
the system, so it cannot also be that system's output at `B-05`. The fix is to
draw two systems-of-interest in one view, linked by the hand-off between them:

| frame | system-of-interest | parties and outputs |
|---|---|---|
| **operating** | the kit, as it runs in a repository (this one included) | the human operator, the development session, the model provider |
| **delivery** | this repository's build-and-release — the kit's enabling system (15288) | the Template it emits at `B-05`; the rigs it verifies the kit with |

A row's `class` already says which frame it belongs to: `operational` and
`interoperating` parties are in the operating frame; `deliverable` and
`enabling` rows are in the delivery frame. The frames are linked by the
**Transition hand-off**: the Template installed into an operating environment.

**Where each SR sits follows from its subject:**

- An SR about the kit's **behaviour in operation** — a check's verdict, the
  loop's outcomes, what the generated views show — belongs on an operating
  bundle. The dashboard SRs (SR-052, SR-053, SR-054, SR-168, SR-169) move from
  `B-05` to the read crossing, for example.
- An SR about the **package as a package** — what the scaffold contains, that a
  re-sync never clobbers, that the manifest materializes where it says — stays
  on `B-05`.

The previous draft said both that the 69 `B-05` SRs are not re-pointed and
that the dashboard SRs may move; the review was right that those contradict.
They are re-pointed, by the rule above. Classifying all 69 is sitting work,
priced in §9.3.

For an adopter only the operating frame is theirs: the Template arrives through
Transition, as their enabling system (`EXT-002`'s own note says so). This
repository has both frames because it builds the kit *and* runs it.

### 5.2 The sitting-2 rulings this reverses

Sitting 2 (2026-08-13) drew the present frame on two premises, both in its own
words:

- **13k** — the human and the loop are one entity: *"who-holds-authority is
  policy and record, never an entity split."*
- **13n** — the delivery frame: *"the system is the act of creating the
  guardrails and template contents … just because it happens to USE them as
  well doesn't mean they are each inputs into the system."*

This proposal reverses both: the human comes out (§5.4), and the kit in
operation becomes a system-of-interest (§5.1). The rulings built on those
premises follow:

| ruling / row | what it says | rests on | under this direction |
|---|---|---|---|
| **13u** — `B-03` removed | `PROJECT_STATE.html`, `open-items.html`, `docs/status.md` and `docs/gate` are *"not system outputs"* | 13k, 13n — the sitting doc itself says a separate human *"should be a deliberate reversal of 13k"* | **falls.** The human reading the spine is a crossing (§5.4). New id; `B-03` stays spent. |
| **`REL-002`** flow and notes | self-adoption; invoking `agent-resume` is *"NOT an input"*; carries 13u's surfacing | 13n, 13u | **shrinks** to the Transition hand-off linking the two frames (§5.5) |
| **`REL-003`** (13n), and `IF-041`'s note | model providers *"touch the SESSION, never the system"*; the runner invocation *"crosses no boundary of this system"* | 13n and 13k — the ledger's only argument is *"the loop launching its CLI — the session driving itself"* | **reversed: becomes a crossing.** In operation the kit's own loop invokes the provider. Two parts survive: 13o's merge of primary and reviewer CLIs into one entity, and the backoff obligation on kit content. |
| **Hosted-CI cut** (2026-08-16q, not a sitting-2 ruling): `EXT-004`, `B-06`, `B-07` | *"this template has no design control over an external CI respecting configurations… all it can do is provide a method within the pack"*; `B-04`'s note: *"a hosted runner is an ADOPTER's boundary"* | 13n, the adopter entity, and `REL-002`/`REL-003` as cited precedent — plus **design control, which is independent** | **partly reversed.** Design control survives as the reason SR-151/152 constrain the shipped workflow *file*. It does not keep the runner off the frame: `interoperating` parties are outside the system's control by definition. It may return as a party (new ids). |
| **13o** — `B-08` removed | `check_vendored` *"would be run by the development environment; it's not an input directly into this design-scope system (its content input arrives via B-01's governed writes …)"* | 13n | **reversed, and the reason was incomplete.** The script compares each vendored file against its *"PINNED upstream raw URL"*, a network fetch that is not a `B-01` write. `IF-036` already calls the upstream *"a live question for the frame's owner"*. Whether it earns an entity is open: the input is opt-in, and this repo vendors nothing. |

The first two rows are certain, because their own text names the premise. The
last three were traced to their full log entries (`docs/log.md:1510-1566`,
`:3953-3984`; sitting-2 plan `:202-209`). `tests/test_external_frame.py` also
asserts `B-06`, `B-07` and `EXT-004` are absent, so any return is re-pinned
under the same ruling.

### 5.3 The enabling system is frame-relative

`EXT-002` (Template) is `deliverable` — an *output*, not a party — and its note
records that the class was *"an ADDITION to the class vocabulary"* because the
outward-facing three did not fit. The delivery frame has simply been
half-populated. The same note records the relativity the two frames rely on:
*"From an adopter's frame this package is their enabling system."*

An enabling system is normally something the developing organization **owns**;
that is what the class is for in 15288. So an in-tree rig is an `EXT` row with
`class = "enabling"`: being built here does not keep it off the frame.

### 5.4 The human's three edges

| edge | what it is | bundle |
|---|---|---|
| human → **session** → system | **write, mediated**: the human edits a cell, the computer writes it, the hook floor admits it | `B-01`, governed writes in |
| human → **system** | **authority**: rulings, attestations, Status flips | `B-02`, authority in |
| system → **human** | **read**: the spine and the views generated from it — the dashboard, open items, status, gate reports | **new bundle**, out — the old `B-03` content, returned |

**Authority.** `interfaces.toml` singles `B-02` out:

> *"ONE CROSSING IS DELIBERATELY REALIZED BY NOTHING: `B-02` (authority in —
> rulings, attestations and Status flips) **has no port of its own.** Authority
> enters as CONTENT on B-01's write path: a human edits a Status cell and
> commits, and the hook floor admits that write as it admits any other."*

The system can observe *that a Status cell changed*. It cannot observe *that a
human judged*. Only the proxy is shared: it arrives as a commit through
`IF-134`, the hook floor's facing row. So `B-02` is an **effect** bundle with no
IF of its own, and the authority assumption measures through `IF-134` and names
`B-02` in `effect_at` (§6.2). Its SRs (SR-140, SR-178, SR-179, and SR-139 in
part) serve SN-029.

**Read.** This is where SN-002 lands: the reviewer trusts the chain by reading
it. The system can see that it rendered a view. It cannot see that the reader
understood it. So the read bundle is also an effect bundle, and it is where the
render critic (§8.4) stands in for the reader. **`PROJECT_STATE.html` itself has
no IF row today** — only `gen_trajectory`'s exit code (`IF-011`) — so the read
bundle needs one minted.

On the inside, the write and authority edges land on `CMP-006` *"W1 Registry &
conformance"*, and the read edge on `CMP-009` *"W4 Human & adopter surfaces"*.

### 5.5 The adopter is dropped

`EXT-003` was *"the downstream team + repo"*. The operating frame already splits
that pair: **the team is the human operator**, and **the repo is the operating
environment the frame is drawn in**.

- **One hand-off remains.** Stripped of 13n and 13u (§5.2), `REL-002` is only
  *the Template installed into an operating environment* — the Transition
  hand-off that links the delivery frame to the operating frame. `REL-001` said
  the same thing about a different repo; one relationship carries it.
- **The value §1 located across relationships lands on bundles.** SN-001's team
  works through `B-01`, `B-04` and the read bundle; SN-002's reviewer reads
  through the read bundle.
- **`EXT-003` is spent and never re-minted**, following the
  `B-06`/`B-07`/`EXT-004` precedent in `external.toml`.

### 5.6 The proposed frames

The boundary view is **generated**: `gen_trajectory.py` builds it from
`external.toml` (`context_block(frame_context(root), ...)`, WI-455). Editing rows
is editing the diagram.

| row | change | frame |
|---|---|---|
| *new* Human operator | **add**, `operational`; owns `B-02` and the read bundle | operating |
| `EXT-001` Development session | **narrow** to the computer: shell, editor, OS, git client, working copy; owns `B-01`, `B-04` | operating |
| `EXT-005` Model provider | stays; `REL-003` becomes a bundle, prompt out and response in (§5.2) | operating |
| hosted CI, vendored-doc upstream | **open**: may return as `interoperating` parties (§5.2) | operating |
| `EXT-002` Template | unchanged; emitted at `B-05` by the delivery system | delivery |
| `EXT-003` Adopter | **dropped** (§5.5) | — |
| *new* Scripted model runner | **add**, `enabling`, `emulates = "EXT-005"` | delivery |
| *new* Scaffold rig | **add**, `enabling`, `emulates = "EXT-001"` — the narrowed session *is* the operating environment: computer plus working copy | delivery |
| *new* Render critic | **add**, `enabling`, `emulates = "EXT-006"` — it stands in for the human reader | delivery |
| *new* read bundle | **add**, out, to the human operator | operating |
| test infrastructure | **not shown** — inherent to defining a system, not a frame element | — |

`EXT-001` is the largest edit. Its description today folds in *"shell, git
client, OS, Python, editors, test runner, LLM runners"*: the human, the
environment, the test infrastructure **and** the model runner in one row.

**Counts.** Entities 4 → **7** (one dropped, one human, three rigs). Bundles 4 →
**6**: the read bundle and the model-provider bundle are new. Relationships 3 →
**1**: only the Transition hand-off remains (`REL-001` merged, `REL-003`
promoted). Hosted CI and the vendored-doc upstream add more if they return. Next
ids from `docs/id-watermark`: `EXT-006`, `B-09`, `REL-005`.

### 5.7 Bundles: authored identity, derived membership

A `B` row is a bundle: the signals that pass between the system and one party
in one direction. The previous draft proposed deriving the bundles themselves
from IF → party links and eventually deleting the `B` rows. The review found
two reasons that cannot work, both verified:

- **Nothing supplies a stable id.** The package-wide SRs (SR-031, SR-034,
  SR-035, SR-114) and every assumption's `effect_at` need a bundle to cite. A
  grouping key can change silently and rename their subject.
- **Nothing supplies direction for an effect with no IF.** The authority effect
  lands with the human, who has two bundles; a stakeholder names a party, not a
  bundle.

So **the `B` rows stay as authored identity rows** — id, party, direction,
`carries`, status — and only their **membership is derived**, from the IF
tie-backs that already exist (`interface_to_external` /
`interface_from_external`). The dashboard already derives membership this way
(`frame_context`'s `realized_by`). What the redraw changes is which bundle some
tie-backs point at (the generated surfaces move to the read bundle; the runner
invocation gains one), plus the 41 IFs whose far side is the dropped adopter,
which need re-pointing by judgment.

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
   S-evidence.** If a W-test cites the interface instead, a TC checking the
   interface's *contract* and a TC checking its *assumption* become
   indistinguishable, and the three obligations in §7 collapse into one counter.
2. **Pervasiveness argues *for* rows.** As a cell, the claim *"the far side
   interprets, so its output needs judgement rather than comparison"* would be
   written ~45 times (§3). The copies would drift, each would need its own
   falsifier, and none could be narrowed in one place. One row with one status,
   one `holds_when` and one falsifier, measured through the seams it covers, is
   PROCESS.md §3's 0→A→B rule applied to W.

### 6.2 How the rows connect

```
WHERE      EXT ◄── [B] ◄── IF ◄── SR ◄── LLR ◄── TC
                            ▲       │
                            │       └── da_refs ──► DA ── effect_at ──► [B]
                            └────── measured_at ────┘

WHY        Stakeholder ◄── SN ◄── SR          (a DA's needs = the needs of the SRs citing it)
EVIDENCE   TC ── assumption_refs ──► DA
```

**An SR defines one interface, or rests only on an assumption.** The owner's
rule: a specification must be testable, so its interface must be *defined, or
clearly assumed*. The house rule sharpens "defined": *"a single interface or
method is fully defined by exactly one requirement"* (PROCESS.md, one decision
per row). So each SR takes one of three forms:

| form | cites | example |
|---|---|---|
| **defines an interface** | `defines = "IF-###"` (one, and no other SR defines it), plus `da_refs` if that IF is bridged | the hook floor admitting or refusing a commit defines `IF-134` |
| **rests only on an assumption** | `da_refs`, no `defines` — nothing on the system's side carries the outcome | SR-140 (*"each acceptance is recorded by a copy riding its own approval commit"*) rests on the authority assumption |
| **package-wide property** | `boundary_refs` to the bundle — the ruled exception | SR-031, SR-034, SR-035, SR-114 |

This sharpens 13s (sitting-2 §3R), which allowed a bundle *"as long as it's
broken down or clearly stated in the component details."* The IFs are that
breakdown; the SR now says which piece it defines. The recursion 13s ruled stays
clean: an SR defines a boundary IF, and an LLR states the internal seams.

**The SR keeps its `sn_refs`.** The previous draft (and the owner's Q11 answer)
moved the need link to the DA whenever the SR's IF carried one. The review
showed, and the data confirms, that this fails: one IF carries several
assumptions serving different needs. `IF-134` is the hook floor; the SRs over it
are SR-017 and SR-018 (privacy, SN-009), SR-019 and SR-020 (SN-005 and SN-009)
and SR-137 (SN-028). Inheriting the needs of the DAs on `IF-134` would give the
privacy SRs the authority assumption's need and drop their own. Removing SR
`sn_refs` would also rewrite stage derivation, orphan checks, the trace forest
and every renderer (123 references across 54 script and test files). So:

- the SR's `sn_refs` stay exactly as they are;
- the SR gains `da_refs`, naming the assumptions its own argument rests on;
- a DA carries **no** `sn_refs`: its needs are derived from the SRs citing it,
  which keeps the link in one place.

**Every DA measures through at least one IF, and names where its outcome
lands.** S is stated over shared phenomena, which is what an IF is, and W
connects those phenomena to the world. The authority assumption, which sitting 2
recorded as *"realized by nothing"*, still measures through `IF-134`: a Status
change arrives as a commit. But the outcome lands with the human, on `B-02`,
which no IF measures. A stakeholder names a party, not a bundle, and the human
has two. So `effect_at` is **required**: the bundle(s) where the outcome the
assumption bridges to lands.

**Why a DA is its own row, not fields on an IF.** The two are always joined,
but the join is **many-to-many** and carries its own evidence:

1. **One assumption spans many IFs** — the interpreting-far-side claim covers
   ~45 seams.
2. **One IF carries several assumptions** — `IF-134` carries the authority
   assumption *and* the bypass limit `B-04`'s note records (*"a local hook floor
   is bypassable (git commit --no-verify)"*).
3. **A test of an assumption needs an id that is not the IF's.**

**The stakeholder is not in the WHERE chain.** A need can belong to someone who
never touches the system: SN-038 (*"an adopter can determine why every file
supplied by the kit exists"*) is one, and a legal or regulatory voice is
another. Stakeholders are a small list (Q12); a stakeholder may optionally name
the EXT party it is, as the human operator does.

**The wiring this changes**, for reference:

| row | links today | links after |
|---|---|---|
| SR (79) | `sn_refs` → SN, `boundary_refs` → B; **no link to any IF** | `sn_refs` unchanged; `defines` → one IF, or none; `da_refs` → DA; `boundary_refs` only for the package-wide class |
| IF (167) | tie-back → B on 43 rows; 124 internal | tie-backs re-pointed by the redraw; boundary IFs gain `coincident` where it applies |
| DA | — | `measured_at` → IF, `effect_at` → B, `realized_by` → rig |
| TC (194) | `verifies` → SR / LLR; 8 also cite an IF | `verifies` unchanged; `assumption_refs` → DA |

The row:

```toml
[assumption.DA-###]
measured_at  = ["IF-013", "IF-###"]  # the harness verdict; the dashboard (a proposed IF row)
effect_at    = ["B-09"]              # the read bundle: where the reviewer's trust lands
assumption   = """A spine the strict check passes with zero orphans is one a
                  reviewer can rely on: each row says something, and the links
                  between rows are the ones a reviewer would draw."""
holds_when   = """Rows are authored under the spine-authoring question list;
                  the reviewer reads the generated views, not raw TOML."""
obstacle     = """Every row resolves and every row says nothing: an
                  orphan-free, semantically vacuous spine."""
falsifier    = """A sampled reviewer, reading the views cold, finds a traced
                  row that says nothing the reviewer would rely on."""
status       = "Drafted"                 # maturity: Drafted | Approved
standing     = "active"                  # validity: active | falsified
```

Cited by SR-157 (*"spine and work-registry rules red the harness verdict"*),
so its needs derive to SN-002 and SN-025.

**Maturity and validity are separate fields.** The previous draft added
`Falsified` to `status`. The review was right that it mixes two axes: an
Approved assumption can later be falsified, and the kit already separated
lifecycle from maturity on components for exactly this reason. `status` keeps
the shared `Drafted | Approved` vocabulary; `standing` is a separate closed
field.

**`falsifier` is a description, not a link.** The previous draft had
`falsified_by = "TC-###"` on the DA *and* TCs citing the DA — the same
association twice. Now the TC → DA link lives only on the TC
(`assumption_refs`), and the DA's `falsifier` cell describes the signal in
prose. The rule both lines of research imply stays: **an assumption with no
declared falsifier is an untested assumption.**

Three cells are borrowed, each with a standard behind it:

- **`holds_when` is an ODD** (SAE J3016 / ISO 21448 / UL 4600): the declared
  region in which the claim is asserted. It brings the **restriction move** with
  it (§7(d)).
- **`obstacle` is van Lamsweerde & Letier's obstacle**: the negation of an
  assumption, refined until it reaches conditions satisfiable in the domain. A
  *generator*, not a comment (§7(b)); hats drive it (§6.5).
- **`falsifier` is the falsifier** of REAssuRE's monitored claims (Welsh, Sawyer
  & Bencomo, ASE 2011) and UL 4600's Safety Performance Indicators.

Two more rows the redraw makes available at once:

```toml
[assumption.DA-###]
measured_at  = ["IF-134"]       # the hook floor admitting the commit
effect_at    = ["B-02"]         # the authority bundle, which no IF measures
assumption   = """A changed Status cell on a human-held rung means a human
                  actually exercised the judgment that Status asserts."""
holds_when   = """The row's rung is at or below the human_approval_through
                  dial in docs/process.toml."""
obstacle     = """A Status change on a human-held rung arrives in a commit the
                  unattended loop authored."""
falsifier    = """A commit authored by the loop that changes a Status cell on
                  a human-held rung."""

[assumption.DA-###]
measured_at  = ["IF-134", "IF-135"]
effect_at    = ["B-01"]
assumption   = """A write the local hook floor admitted was checked: the floor
                  was not bypassed, or a re-run of the same bar agrees."""
holds_when   = """Commits are not made with --no-verify, or a re-run of the bar
                  away from the session is in place."""
obstacle     = """git commit --no-verify admits an unchecked write, and nothing
                  re-runs the bar."""
```

The first is cited by SR-140, SR-178 and SR-179 (SN-029). It is what `Attest` and
the attested-vs-mechanized split exist to protect, stated for the first time as
something falsifiable. Its `holds_when` matters here: this repo sets
`human_approval_through = "DevStg-Needs"`, so for SR, LLR and TC rows a Status
change *is not* a human act, by policy, and an unscoped version would be false.
The second is cited by SR-019 and SR-020 (SN-005, SN-009): the bypass limit
`B-04`'s note already records, now as a row.

**Checks the rows make possible** (all warn-first, step 5):

- a boundary IF that is neither bridged nor `coincident` — *unclassified*;
- an SR that defines a bridged IF but cites none of the DAs measured there;
- a DA that no SR cites, or that names no `falsifier`;
- a need whose stakeholder is an operating party, where no SR of the need
  defines an IF on that party's bundles and no DA it rests on lands there — the
  frame is missing an interface, or the need names the wrong stakeholder
  (`REL-001` and the read edge were both found this way, by hand).

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

**Writing the rows is derivation, not transcription.** The previous draft
called step 2 transcription. The review was right: the claims are written down
nowhere, and a row such as *"the team reads ADOPTING.md before first use"* adds
a new precondition. Each DA is a newly derived Drafted claim that needs the same
review as any other row.

### 6.4 Writing a good one

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
on the voice hats records that, and re-anchors FIRST-RUN-ADOPTER, which was
anchored to `EXT-003` — a **party** — when it should name a **stakeholder**.

**A hat constrains the specification; it does not always create a
requirement.** 77 of the 79 SRs already carry `hat_refs`, and the package-wide
SRs are hat-shaped constraints stated once for a whole bundle. Applied to a
piece of the WHERE chain, a hat that bites produces one of four things:

| a hat applied to… | produces |
|---|---|
| an IF or SR | a **constraint**: a tightened acceptance clause on the existing SR (`hat_refs`) |
| a whole bundle | a **cross-cutting property**: one SR against the bundle (the package-wide class) |
| a gap nobody stated | a **new SR** — the rare case |
| a DA | an **obstacle**: UNATTENDED-OPS asking *"what happens when its input is missing, stale, or half-written?"* writes the DA's `obstacle` cell |

**Only positive provenance is recorded.** The previous draft also recorded a
"not applicable" outcome for every hat on every piece. The review was right that
16 hats over hundreds of rows would produce thousands of negative records with
no machine use. What the kit keeps is what already has a consumer: `hat_refs` on
the rows a hat changed, and which hat generated an obstacle.

**The one real change:** hats fire today on SN → SR decomposition, keyed on
work-item and need tags. Firing them per DA or IF means those rows need tags,
or the composer runs per bundle.

---

## 7. Three test obligations, and why they are affordable

If the argument is `S ∧ W ⊨ R`, evidence is owed on three fronts. The kit
currently collects one systematically.

| # | evidences | where evidence sits | cost | cadence |
|---|---|---|---|---|
| **1** | **S** | a TC that `verifies` an SR or LLR | cheap | every commit — nearly all 194 TCs today |
| **2** | **W** | a TC whose `assumption_refs` names the DA | cheap-to-moderate — *free where it is a metamorphic relation, (c)* | continuous or event-triggered |
| **3** | **R through W** | the effect bundle, via a translation or a rig | expensive — *a rig splits the cost rather than removing it (§8.2)* | sparse, sampled — *see the limit below* |

**W-evidence has its own field.** The previous draft let a TC name a DA in
`Verifies` and called that a narrow `coherence.py` exception. The review showed
it is not narrow: `Verifies` means SR or LLR throughout the trace forest and
the SR → LLR → TC matrix, which would label a DA-only TC *"verifying nothing
valid"*. A separate `assumption_refs` field leaves `Verifies` meaning what it
means everywhere, and a TC that only evidences an assumption is valid on its own
(the intent of Q5).

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
input space. That is why W has to be rows, not prose; shared rows (§6.1) keep
the number bounded.

The same allocation rule is normative in aerospace structures as the
**building-block approach**: FAA AC 20-107B requires tests "at the coupon,
element, details, and subcomponent levels", and CMH-17 Vol. 3 states the
reasoning — **run many cheap low-level tests to bound variability so that very
few expensive high-level tests can be justified.** Many cheap W-tests buy the
right to run few R-probes.

**(b) Corner cases are generated, not imagined.** Each `obstacle` mechanically
yields at least one adversarial case: *what if this does not hold?*

**(c) Some W is executable, at ordinary CI cost.** A **metamorphic relation**
(Chen, Cheung & Yiu, 1998) is a necessary property across *multiple*
executions, which tests without knowing any single correct output — the
standard answer to the oracle problem. Most useful MRs are statements about the
world (*"adding an unrelated registry row must not change an unrelated row's
status"*), so **writing an MR is writing a testable domain assumption.** Try it
first for any new W row.

**(d) Narrowing the declared world is a legitimate answer.** SOTIF (ISO 21448)
sanctions two responses to a gap: improve the system, **or restrict the ODD**.
When `S ∧ W ⊨ R` will not close, narrow `holds_when` until it does, and say so.
*"The team's stack is one of the shipped profiles"* is exactly such a
restriction.

**(e) Evidence declares how close to validation it sits.** The `Verification`
vocabulary (`trace.py:526`) names the **method**; nothing names the **distance
from the effect**. The descriptor is `assumed | sampled | monitored` (Q4), with
NASA-STD-7009B's Credibility Assessment Scale as the escalation path.

### The limit on sparse sampling

Sampling the human axis sparsely gives a **high-variance lower bound on
discovery, not a coverage claim.** Faulkner (2003) resampled from 60 users and
found random 5-user sets caught anywhere from **55% to 99%** of known problems;
n=10 lifted the floor to 80%, n=20 to 95%. Schmettow (2012) shows discovery is
over-dispersed.

So sparse R-level probes are worth running and their *findings* are real, but
**a passed sparse probe is not evidence that a W row holds; only a failed one is
evidence that it does not.** The same holds for a green run against a rig. If a
human-axis assumption is load-bearing, the honest options are to restrict the
ODD or accept a recorded risk, not to claim a model covers it.

---

## 8. Enabling systems and rigs

### 8.1 Enablement, and where verification sits

ISO/IEC/IEEE 15288:2023 (3.15) defines an enabling system as one that
*"supports a system-of-interest during its life cycle stages but does not
necessarily contribute directly to its function during operation"*, and notes
that *"each enabling system has a life cycle of its own."* The stages are
concept, development, production, utilization, support and retirement (detailed
in ISO/IEC/IEEE 24748-1:2024). Deployment is served by the **Transition**
technical process (6.4.10, retained in 2023), which installs the verified
system, with its relevant enabling systems, into its operational environment.

| kind | what it enables |
|---|---|
| rig | Development stage — the Verification and Validation processes |
| test infrastructure | Development stage |
| deployment / delivery | the **Transition** process, into Utilization |
| procurement, warehousing | Production and Support stages |

The rows are this proposal's reading, not a list from the standard; the standard
itself gives one example, a production-enabling system. Stage does not decide
which things carry test cases, so it is a taxonomy, not a gate.

**Verification sits outside this classification.** Every enabling system needs
verification around it, not only the product: `tests/` verifies the harness, and
CLAUDE.md traces `tests/` as product. Three independent axes:

| axis | applies to | recorded as |
|---|---|---|
| **is it verified?** | *everything* | ordinary tests |
| **does it discharge a spine requirement?** | whatever a requirement is written about | a TC with `verifies` |
| **does it stand in for something else?** | rigs only | an `emulates` cell and a fidelity DA |

The split is **frame-relative**. This kit's product *is* test infrastructure, so
what would be supporting enablement elsewhere is shipped product here.

### 8.2 Translation and rig: one construct at two weights

- A **translation** converts an effect into something the system can check by
  *claiming* the conversion holds. It is a DA alone.
- A **rig** converts it by *performing* the conversion: simulating the effect
  and putting the output against a rubric. It is a DA with `realized_by`.

**A rig plugs into an interface that already exists.** It presents the same
interface as the party it replaces, so the system's side is unchanged; only
what is plugged into the far side changes.

| | recorded as |
|---|---|
| the real party | `[entity.EXT-###]`, operating frame |
| the rig, as a system | `[entity.EXT-###]`, `class = "enabling"`, `emulates = "EXT-###"` — delivery frame |
| the interface both plug into | the **existing** `IF` rows, unchanged |
| its fidelity | a DA with `realized_by` naming the rig entity |

A rig costs one entity row, one cell and one DA.

**What a rig buys, and what it does not.** It does not make the real phenomenon
observable, so **the outcome stays where `effect_at` says**. It makes a *model*
of the world observable, and W is **replaced** for the cheap, continuous part of
the evidence:

| the assumption before the rig | the assumption after |
|---|---|
| *"zero orphans ⟹ a reviewer trusts the chain"* | *"a model judging the rendered artifact against rubric R judges as a human would"* |
| *"this current curve ⟹ the apple is gripped"* | *"the contact model grips like the real gripper does"* |

The left column is untestable in principle. The right is a **fidelity**
assumption: bounded, stated, and testable by calibration. The product changes
every commit and the rig changes yearly, so obligation 3 **splits**: cheap and
continuous against the rig, expensive and sparse against the rig's fidelity.

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

From that cell the view draws the rig in the delivery frame with a dotted edge
to `EXT-005`, and can mark `EXT-005` as *"has a maintained virtualized
counterpart"* by reading the inverse. **A rig row with `emulates` and no DA
naming it in `realized_by`** is a virtualized component whose fidelity nobody
has stated: a warn-first finding.

### 8.4 The rigs this repo already runs

**The scripted model runner.** `IF-041` is the runner contract: `agent_session`
invokes the agent CLI headless, the prompt on stdin. `FAKE_AGENT`
(`tests/test_agent_loop.py:34`) answers that same contract from an `actions.txt`
script (`commit` / `done` / `blocked` / `noop`). **It simulates `EXT-005`'s
protocol, not its judgment**, and that is the right split: a model good enough
to stand in for a model is circular.

**The scaffold rig.** `tests/conftest.py:1-7`: *"The tests exercise the scripts
the way a downstream user would: bootstrap a real scaffold in a temp dir and run
the actual commands."* It emulates `EXT-001` — the narrowed session is the
computer plus the working copy, which is the operating environment. That rig
also settled the old `REL-001` question: the registry's rule that a relationship
*"must never grow a realizing IF row. **Wanting one means what you have is a
boundary crossing**"* (`external.toml:20-22`) could not coexist with a rig that
had been standing at `REL-001` since before the frame was drawn.

**The render critic.** `render-dashboard-critique` screenshots
`PROJECT_STATE.html` across a declared width/theme/tab matrix so a critique
judges pixels, not markup; the critique contract makes a perceptual TC name its
**artifact recipe** beside its rubric; `llm-vision-convergence-loop` requires
two consecutive approvals at one content hash. That is a rig standing in for the
human reader, a declared ODD and a repeatability control, with **no assumption
row behind any of them.** The TC pins the rubric, not the pixels, so a redesign
re-runs the judgment instead of invalidating the case.

What nothing does today is treat **the judge** as an assumption:

```toml
[assumption.DA-###]
measured_at  = ["IF-###"]       # the dashboard (a proposed IF row, §5.4)
effect_at    = ["B-09"]         # the read bundle
realized_by  = "EXT-###"        # the render critic
assumption   = """A vision model judging the rendered dashboard against the
                  rubric reaches the verdict a human reviewer would."""
holds_when   = """An image-capable model; the rubric carries its accumulated
                  anchors; a static render at a declared width and theme."""
obstacle     = """A model revision shifts judgment silently; or the rubric
                  overfits to anchors accumulated under one model's eye."""
falsifier    = """A periodic human Attest sample that disagrees with the
                  critic's verdict."""
```

Cited by SR-052, SR-053 and SR-054 (SN-023, SN-024). It does not claim a model
covers the human axis; it states the claim, bounds it, and names the sample
that would refute it.

### 8.5 The self-derivation limit

This repo cannot dogfood its own development scripts: executing the scripts
being modified has repeatedly failed to give a usable result. The general rule:

> **A rig derived from the system under test cannot falsify assumptions the two
> share.**

Self-execution is the limit case: the rig *is* the system, the shared set is
total, and it can falsify nothing. It is also why `FAKE_AGENT` has the right
shape: a scripted stand-in that does not run the real thing shares no
assumptions with it.

---

## 9. Impact

Surveyed against the code on 2026-09-20 and re-checked against the review on
2026-09-23. Anchors are given so the next session can start from them.

### 9.1 Evidence for assumptions: a TC field, not a new `Verifies` target

`Verifies` already accepts `IF-###` as a *supplement* to a spine citation
(`coherence.py:73-108`), but a DA-only TC would still be misclassified by
`trace.py`, which indexes only SR and LLR targets (`:3118-3121`, `:3164-3168`)
and labels any other TC *"verifying nothing valid"*. So assumption evidence
gets its own field, `assumption_refs`, and the consumers that need to learn it
are named rather than assumed away:

- `coherence.py`'s TC rule: a TC must verify an SR or LLR **or** evidence a DA;
- the trace forest and the SR → LLR → TC matrix, which should show DA evidence
  beside, not inside, the S evidence;
- the TC schema of record, its template, `spine_carrier` / `migrate_carrier`
  maps, and the dogfood census.

### 9.2 Where the rows live — one home, and what it does not give for free

**One home: `external.toml`.** The previous draft (and Q8's answer) gave DAs two
homes, `external.toml` for boundary DAs and `interfaces.toml` for internal-seam
DAs. The review showed that breaks the registry machinery:
`test_dogfood_sync.TOML_REGISTRIES` maps each id column to exactly one live and
template path (`:246-312`), so one `DA-ID` key cannot represent two files.

The owner's concern behind the second home is kept by a **readiness rule**
instead: *a DA cannot be Approved until every IF in its `measured_at` is
Approved.* An internal seam is approved at DevStg-Arch, so a DA measured there
simply waits, Drafted, until its seam exists. The owner's case — an LLM *inside*
the system handing structured output to a script — is exactly that: W on an
internal seam, because the far side interprets. It is not rare downstream (any
bought-in interpreting part: an embedded model, a sensor, a third-party parser;
the kit's `PART` registry already holds such parts), but in this repo the model
is `EXT-005`, outside, so the case does not arise here yet.

**What sharing the file does not give for free** (the previous draft claimed
more than it delivers):

- `boundary_incomplete` (`spine_rules.py:453-496`) and `derive_stage.py:178-190`
  read only `B-ID` rows, so a Drafted DA would hold no rung until a DA arm is
  added to the Boundary predicate.
- `baseline_snapshot.py:209-222,511-517` enumerates EXT, B and REL but no DA
  tier, so Approved DAs get no drift comparison until the tier is added.
- The file *does* give: the stage fingerprint (`kitlib/stage.py:144`), scaffold
  mapping, and an id-column-keyed dogfood census that already holds three tiers
  on one path.

**The lock is narrowed** (Q15): entity, boundary and relationship rows change
only by a recorded ruling; DA rows follow ordinary Boundary-rung approval under
the dial.

**Moving the dial is not yet enforcement** (Q14). The dispatcher's off-spine
approval axis, `approval_held`, *"DEFAULTS FALSE AND EVERY CALLER IN THIS MODULE
PASSES THE DEFAULT"* (`dispatch.py:337-355`), because no work-item kind carries
a registry identity. What bites today is `tests/test_approval_level.py`, which
pins that no shipped loop module writes an `approval` cell. So moving
`human_approval_through` to DevStg-Boundary does not stop an automated path
editing a DA's status until either registry identity is threaded through
admission or a commit-time refusal exists (§9.3h).

### 9.3 The edit list

**(a) Classify boundary IFs.** A `coincident` waiver cell on the IF schema
(`kitlib/spine.py` IF tuple, `interfaces.template.toml`, the carrier maps — the
maps must invert and match in length, `test_rule_sync.py:700-712`), then the
warn-first *unclassified* finding.

**(b) The DA row kind — 8 schema edits, plus wiring.** `OFFSPINE_KEYS`
(`DA-ID`), `OFFSPINE_TABLE` (`"DA-ID": "assumption"`), the schema tuple, the
template, both carrier maps, a `TOML_REGISTRIES` entry **and** its floor
(`test_dogfood_sync.py:433`), and `trace.py:920-928` `_offspine_ids` for the id
watermark (the missing-watermark hole has happened here twice: IF-121/122 and
OI-26). Then the wiring §9.2 lists: a DA arm in the Boundary predicate, a
snapshot tier, the readiness rule, and resolution of `measured_at`,
`effect_at` and `realized_by`.

**(c) The frame redraw — a sitting.**
- `tests/test_external_frame.py:87-114` pins *exactly* 4 entities, 4 crossings
  and 3 relationships plus the spent-id gaps, and `:128-146` pins every
  `status`. Its docstring says it **is expected to be edited by a sitting and by
  nothing else**. The redraw re-pins all three counts, adds `EXT-003`, `REL-001`
  and `REL-003` to the spent ids, and adds `emulates` to the entity schema.
- The reversed rulings (§5.2) carry prose with them: `REL-002`'s flow and notes,
  `EXT-005`'s description, `IF-041`'s note and `B-04`'s note.
- `tests/test_hats.py:885-900` names `EXT-003 Adopter` as FIRST-RUN-ADOPTER's
  entity; the hat needs a `speaks_for` stakeholder instead (§6.5).
- `docs/log.md` and the sitting-2 plan cite `EXT-003` and 13u historically. They
  are records and stay as written.

**(d) SRs define IFs — the largest item.**
- The SR schema gains `defines` (one IF) and `da_refs`; `sn_refs` is untouched,
  and `boundary_refs` remains only for the package-wide class. A schema change
  that ships, so it needs a resync entry.
- **All 79 SRs are re-classified by frame (§5.1) and paired with the IF each
  defines.** The house rule is one SR per interface. 69 SRs sit on `B-05` today
  against 39 `B-05` IFs, and some of those IFs move to operating bundles, so
  roughly **25–30 IF rows have to be minted** — including the dashboard's own,
  which does not exist (§5.4). 13s anticipated this: *"it should help to expose
  if there are some other issues in the way this system has been decomposed."*
- The 41 IFs whose far side is `"external:downstream adopter"` are re-pointed by
  judgment.

**(e) Boundary IFs approved at DevStg-Boundary.** An SR at DevStg-Reqs cannot
cite an interface that is only approved later at DevStg-Arch
(`kitlib/ladder.py:70-80,119-125`; `agent_common.APPROVAL_RUNGS` maps the whole
`interfaces` registry to DevStg-Arch). The IFs with a tie-back are frame content
and move to the Boundary rung; internal seams stay at Arch. That makes the
interfaces registry's approval rung per row, not per registry: `APPROVAL_RUNGS`,
`human_approves`, and the Boundary predicate change with it.

**(f) The stakeholder list (Q12) — a new row kind, about the same as (b).** A
stakeholder id prefix, its watermark entry, template example rows, the
dogfood-sync floor, `trace.py` resolution of each SN's stakeholder citation, and
an optional link to an EXT party. It lives in `stakeholder-needs.toml`, which is
already fingerprinted and approves at DevStg-Needs.

**(g) Assumption evidence on TCs** — `assumption_refs` and its consumers (§9.1).

**(h) Enforcing human-held DA approval** — thread registry identity through
admission and pass `human_approves(...)`, or add a commit-time refusal (§9.2).

**(i) Hats per piece** — tags on DA and IF rows or a per-bundle composer; the
record is positive provenance only (§6.5); `speaks_for` needs (f) first.

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
be `PROCESS_OPTIONS.md` or `ADOPTING.md` / `EXAMPLE.md`, **not**
`AGENTS.template.md`.

**The SR re-classification is the real cost.** Items (d) and (e) touch every
SR and the interfaces registry's approval model. Everything else is a new row
kind on existing machinery.

**Adopters need a resync entry.** `RESYNC_PACK.md` §3 takes a `[since <sha>]`
entry, format-enforced by `test_resync_pack.py:117/210/252`.

### 9.5 Adjacent findings

Not part of this proposal; recorded because the survey found them.

1. **This repo has not recorded Release evidence.** `docs/test/evidence` is the
   sole input to `DevStg-Release` (`spine_rules.py:583-592`), and
   `record_test_evidence.py` exists to write it; the rung is reachable once the
   recorder is run successfully and committed.
2. **Per-requirement coverage lives in `trace.py`, not `plan_coverage.py`** —
   the `SR → LLR → TC` matrix at `trace.py:5194-5207`.
3. **The SN `priority` vocabulary (`M`/`S`/`C`) and the WI `Priority` integer
   are unconnected.** Nothing maps a Must-need onto queue order.
4. **`Permutations` + `gen_cases.py` is a dormant layer, not a live hook.**
   `test_dogfood_sync.py:515-519` *asserts it stays unused* as a probe.
5. **The dashboard has no IF row** (§5.4): SN-023's own surface is realized by
   nothing but `gen_trajectory`'s exit code.

---

## 10. Staging

Each step is useful alone, and each later step assumes only the earlier ones.
Nothing is built before the sitting.

**Step 1 — the sitting.** Reverse the §5.2 rulings deliberately; land the §5.6
rows in the two frames (§9.3c); add the DA row kind with its wiring (§9.3b) and
the `coincident` waiver (§9.3a); move boundary IFs to the Boundary rung (§9.3e);
narrow the lock (Q15); move `human_approval_through` to DevStg-Boundary (Q14) and
land the enforcement it needs (§9.3h); add the stakeholder list (§9.3f).

**Step 2 — write the assumptions.** DA rows derived from the 24 person-facing
needs — each a new Drafted claim, reviewed like any other row (§6.3). Warn-only;
nothing gates. Expect this step alone to surface real defects.

**Step 3 — SRs define IFs.** The §9.3d re-classification: each SR moves to its
frame, names the IF it defines (minting the missing ones) and the DAs it rests
on; each boundary IF is bridged or `coincident`. Warn-only.

**Step 4 — evidence for assumptions.** `assumption_refs` on TCs (§9.1) and the
evidence descriptor (§7(e)). Start with the metamorphic subset (§7(c)), which is
nearly free.

**Step 5 — the warn-first findings.** `trace.py` warns on:
- an unclassified boundary IF (§4);
- an SR over a bridged IF that cites none of its DAs, or an SR that defines no
  IF, cites no DA and is not package-wide (§6.2);
- a DA no SR cites, with no `falsifier`, or measured at an IF not yet Approved
  while it is itself Approved (§6.2, §9.2);
- a rig with `emulates` and no fidelity DA (§8.3);
- a need whose stakeholder party is reached by none of its SRs or DAs (§6.2);
- a `falsified` DA, reported with every IF, SR and TC it reaches (§11.3, item 1);
- a Status change on a human-held rung in a loop-authored commit — the authority
  DA's falsifier (§6.2).

**Step 6 — the gate, if wanted.** The vision promises work built *"test-first
with explicit approval gates so you can trust what ships."* Steps 2–5 only warn.
The gate is **path-level**, which the review showed a need-level gate is not:
one DA on one path would have cleared a need while its other paths stayed
unbridged. So `DevStg-Tests` requires, for every SR that defines a boundary IF,
that the IF is `coincident` or the SR cites a DA measured there. **The only step
that costs an adopter anything mandatory; opt-in with an applies-when**, per the
proportionality doctrine.

**Hats per piece (§6.5, §9.3i)** can land any time after step 1's stakeholder
list.

**Adopter migration is deferred, deliberately.** No adopter has taken a spine
update for some time. Once this repo's model is firm, the resync entries are
written against the real gaps rather than planned now (§9.4).

**Not proposed: a new stage rung**, and **no longer proposed: deleting the `B`
rows** (§5.7).

---

## 11. Decisions and open questions

### 11.1 Decisions

Owner answers, 2026-09-21 to 2026-09-23. `DECIDED` means the next sitting may
build on it; `OPEN` and `REOPENED` mean it may not. A `REOPENED` row carries the
revision this document now proposes, for the owner to accept or reject.

| # | question | standing |
|---|---|---|
| Q1 | Does the human come out of `EXT-001`? | **DECIDED: yes** (§5.4). |
| Q2 | Does `REL-001` become a crossing? | **DISSOLVED** by dropping the adopter (§5.5). |
| Q3 | `frame` vocabulary: two values or three? | **REOPENED (review 11).** Three words kept, and `coincident` stays explicit — but on the IF, as a waiver cell. `design` and `effect` become derived properties of a bundle, because a bundle cannot carry one scalar (§4). |
| Q4 | How heavy is the evidence descriptor? | **DECIDED: `assumed \| sampled \| monitored`**, CAS as the escalation path (§7(e)). |
| Q5 | May a W-test stand alone? | **REOPENED (review 15, 21), intent kept.** Yes, through a separate TC field `assumption_refs`, not through `Verifies`, whose meaning stays SR/LLR everywhere (§7, §9.1). |
| Q6 | Does a rig get its own crossing? | **DECIDED: no.** A rig is an `enabling` entity with `emulates`, plugged into the existing interface, with a fidelity DA (§8.2). |
| Q7 | Does this ship downstream in v1? | **DECIDED in principle: yes**, once the sitting has nailed down the details; migration deferred (§10). |
| Q8 | Where do DA rows live? | **REOPENED (review 5).** One home, `external.toml`, plus a readiness rule: a DA cannot be Approved before the IFs it measures. Two homes break the one-path-per-id registry map (§9.2). |
| Q9 | Rename SR to SS? | **DECIDED: prose now, prefix later** — and "prefix never" is the likely outcome, since in SRS usage the entries are *requirements* (appendix). |
| Q10 | Derive `frame`, or write it? | **REOPENED (review 11, 12).** The written bundle column goes away: with `coincident` explicit on IFs and `effect_at` required on DAs, every value is determined by authored rows, and a second written copy would be a second home (§4). |
| Q11 | Where does an SR's need link come from? | **REOPENED (review 3, 14).** The SR keeps `sn_refs`; it adds `da_refs`; a DA's needs are derived from its citing SRs. The one-place rule failed on multi-assumption IFs such as `IF-134` (§6.2). |
| Q12 | Where does a stakeholder live? | **DECIDED: a small stakeholder list** in `stakeholder-needs.toml` (§6.2, §9.3f). |
| Q13 | Need-link edge cases | **REOPENED (review 3)** — dissolved by Q11's revision: with `sn_refs` kept on the SR there is nothing to add to a DA or split. |
| Q14 | Should DA approval be human-held here? | **DECIDED: move the dial to DevStg-Boundary at the sitting** — with the enforcement it needs, which does not exist yet (§9.2, §9.3h). |
| Q15 | Does `external.toml`'s lock cover DA rows? | **DECIDED: narrow the lock** to entity, boundary and relationship rows (§9.2). |
| Q16 | Two frames in one view? | **NEW (review 1, 16).** Operating and delivery frames, each with its own system-of-interest, membership from `class`, linked by the Transition hand-off; SRs placed by subject, so dashboard SRs and other operating-behaviour SRs leave `B-05` (§5.1). |
| Q17 | Boundary IFs approved at DevStg-Boundary? | **NEW (review 2).** Needed so an SR at Reqs never cites an interface approved later; makes the interfaces registry's rung per row (§9.3e). |
| Q18 | One SR per interface — mint the missing IFs? | **NEW (review 9).** The house rule says a single interface is defined by exactly one requirement, so ~25–30 IF rows are minted rather than the rule reversed (§9.3d). |
| — | Orientation, the adopter, and the reversed rulings | **DECIDED:** operating frame, `EXT-003` dropped, 13u reversed. **Traced 2026-09-22:** `REL-003` and 13o reversed; the hosted-CI cut partly reversed (§5.2). |
| — | Bundles | **REVISED (review 4, 10):** `B` rows stay as authored identities; only membership is derived. The "drop the rows" step is withdrawn (§5.7). |
| — | Hats | **Agreed 2026-09-22, narrowed (review 22):** four positive outcomes; no "not applicable" record (§6.5). |
| — | DA approval rung | **DECIDED: DevStg-Boundary**, subject to the readiness rule (§9.2). |
| — | Packaging | **DECIDED:** split into packages for the sitting. |
| — | Enabling-system stage vocabulary | **Tentative**; standard wording verified (§8.1). |

### 11.2 Review round 1 — codex Sol, reasoning effort high (2026-09-23)

Verdict: *"REJECT AS WRITTEN — the proposal's central joins, stage ordering,
frame derivation, and approval wiring are not implementable from the declared
data."* 24 findings. Each was checked against the code before being applied;
all 24 held, and each was applied in the section named.

| # | finding (short) | applied in |
|---|---|---|
| 1 | one system-of-interest cannot both emit the Template and be the installed kit | §5.1 two frames (Q16) |
| 2 | SRs at Reqs cannot cite IFs approved later at Arch | §9.3e (Q17) |
| 3 | one-place need link gives wrong needs on multi-DA IFs | §6.2 (Q11, Q13) |
| 4 | nothing supplies the direction of an effect with no IF | §6.2 `effect_at` required; §5.7 |
| 5 | one `DA-ID` cannot have two homes | §9.2 (Q8) |
| 6 | a need-level gate can pass with unbridged paths | §10 step 6, path-level |
| 7 | `Falsified` mixes validity into maturity | §6.2 `standing` |
| 8 | sharing `external.toml` does not wire a DA tier into predicates or snapshots | §9.2, §9.3b |
| 9 | one SR per interface: 69 SRs vs 39 IFs | §9.3d (Q18) |
| 10 | deleting `B` rows leaves bundle-wide SRs without a subject | §5.7 |
| 11 | one scalar `frame` per bundle cannot aggregate mixed IFs | §4 (Q3, Q10) |
| 12 | "no DA means coincident" contradicts "absence asserts nothing" | §4 |
| 13 | a rig does not move an effect into design | §4, §8.2 |
| 14 | removing SR `sn_refs` touches 123 references in 54 files | §6.2 |
| 15 | a DA-only `Verifies` breaks the trace forest and matrix | §7, §9.1 (Q5) |
| 16 | "no SR re-pointed" contradicts "dashboard SRs may move" | §5.1 |
| 17 | the scaffold rig had no valid `emulates` target | §5.6, §8.4: `EXT-001` |
| 18 | the dispatcher's off-spine approval hold is dormant | §9.2, §9.3h, §11.3 item 5 |
| 19 | "all 194 TCs test the machine" ignores existing Critique and Inspection | §1 |
| 20 | writing DAs is derivation, not transcription | §6.3 |
| 21 | `falsified_by` plus inbound TC links is two homes | §6.2 `falsifier` prose |
| 22 | a per-row "not applicable" hat ledger has no consumer | §6.5 |
| 23 | endpoint and tie-back counts were stale | §3 |
| 24 | Release is unrecorded, not unreachable | §9.5 |

### 11.3 Formerly "not captured" — closed or scheduled (owner, 2026-09-23)

1. **Blast radius → a field and a report (step 5).** Example: one DA covers
   every seam where the kit consumes model output (*"the model runner follows
   the runner contract"*, measured at `IF-041` and its neighbours). A provider
   changes its CLI's exit codes; the DA is false, and every SR over those IFs
   loses part of its argument at once. With `standing = "falsified"`, a derived
   report lists the IFs, SRs and TCs that no longer prove their need.
2. **Chained assumptions → closed, no machinery.** A need's argument is the
   conjunction of every DA on its paths: Jackson's flat conjunction is enough,
   and item 1's report walks the chain anyway.
3. **Graded interpretation → closed by authoring rule (§6.4).** Hardening moves
   part of W into S, and the DA is rewritten narrower. Testing the remaining
   content half is an event-triggered judge-and-rubric job.
4. **The trusted layer → closed by §6.3 and §6.5**, in proportion to risk.
   Precedent: running with git off PATH exposed a hook defect (WI-333, recorded
   in `conftest.py`).
5. **The authority DA's falsifier → a step-5 finding.** Prevention is partial:
   the dispatcher surfaces attestation and gate work on human-held *spine*
   tiers, but its off-spine approval hold is dormant (§9.2). Detection does not
   exist. Added: *a Status change on a human-held rung, in a loop-authored
   commit, is a finding*.

**Standards, verified 2026-09-22.** The 15288:2023 definition (3.15), the stage
names (via 24748-1:2024) and the Transition process (6.4.10) were checked against
the published standards' free previews and SEBoK. The §8.1 table of
enabling-system kinds is this proposal's reading, not a list in the standard.

---

## Appendix — the conventional SRS, mapped

A cross-check against the usual outline of a System Requirements Specification
(SRS): *what* the system must do and how well, without *how* it is built. The
model above covers every element. Nothing here proposes a change.

| SRS element | where it lives in this model |
|---|---|
| Purpose, scope, definitions | the README's `PROJECT-VISION:` tag, each need's Scope, `PROCESS.md` |
| System context | the depth-0 view of the two frames (§5) |
| Major functions | needs and components |
| User characteristics | the stakeholder list (Q12) |
| Constraints | `performance-budgets.csv`, the dependency ledger, `stack.ini`, and hat-produced constraints (§6.5) |
| **Assumptions** | **the DA rows. Empty in the kit today: the gap §1 found.** |
| Functional / non-functional | implicit in how an SR originated: see below |
| Interface requirements | IF rows, each defined by one SR (§6.2) |
| Exclusions (no design detail) | the SR / LLR split, and SN-033's check that needs name no mechanism |

**Assumptions are a standard section, not an invention of this proposal.**
IEEE 830-1998's prototype SRS outline carries *"2.5 Assumptions and
dependencies"* under *"Overall description"* (guidance in clause 5.2.5: the
factors whose change *"can affect the requirements"*). Its successor, ISO/IEC/IEEE
29148 (2011, revised 2018), keeps the item (2018: 9.6.8). Verified 2026-09-22
against a course copy of 830 and IEEE SA's catalog entry; the 29148 clause number
came from an unofficial copy, so cite the catalog entry rather than the number.

**No functional / non-functional category.** The split is binary and adds
nothing the kit cannot already read. SRs carry an optional `aspect` (a closed,
cross-cutting review grouping, filled on 31 of 79, never gated), and the
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
