# The validation gap and the assumption tier

**Status: PROPOSAL. Not a ruling.** It asks for one, because it changes the
frame that [`external.toml`](../requirements/external.toml) declares LOCKED.
The owner has answered most of its questions (§12). Those answers set the
direction the next sitting builds on. They are not the ruling itself, and
`external.toml` is unedited.

**Revised four times after adversarial review (2026-09-23, §12.2–§12.5).**
Four codex Sol reviews (reasoning effort high) found 24, 18, 5 and 7 problems.
The last two judged the draft *"NOT YET SOUND"* on specific points — by then
implementation-level: result carriers, snapshot parsing, stage placement. All
are applied here; the round-4 fixes were not put through a fifth round. Every finding was checked against the code before being
applied. The second review showed the first revision had over-reached — it moved interfaces ahead of
requirements on the stage ladder and recreated a bundle-level scalar — so this
draft splits the proposal in two:

- **the core** (§4–§8): the assumption tier on its own — assumption rows in a
  dedicated registry, cited by the requirements whose argument needs them,
  evidenced by test cases, in a depth-0 view of two frames;
- **an extension** (§9): the owner's rule that a specification's interface must
  be defined or clearly assumed, as an allocation made at the architecture rung,
  where interfaces actually live.

**A fifth Sol review (2026-09-23, §12.7)** checked the owner's decisions of
that day for open points and false premises; its findings are applied, and
the owner questions it raised are Q28–Q30.

Owner answers the reviews overturned are marked **REOPENED** with a proposed
replacement (§12.1), never silently changed.

**What it proposes, in one sentence.** The kit records what the system must do
at its own interface and tests that exhaustively; it does not record the
assumptions that carry those interface facts up to the human outcomes its needs
are written about, and so cannot test them — so this proposes that those
assumptions become rows the requirements cite, that test cases may evidence
them, and that the depth-0 view show the kit in operation beside the system that
delivers it, so that the crossing where an outcome lands is one the frame holds.

**Who this is for.** The owner, as a decision document. A rendered mockup of the
resulting depth-0 view is in [`mockups/`](mockups/depth0-operating-frame.html).

## The model at a glance

```
CORE
  frames      each bundle [B] declares which system it crosses into:
                system = "kit"       the kit in operation — the system-of-interest
                system = "delivery"  this repository's build and release, emitting the Template
  WHY         Stakeholder ◄── SN ◄── SR                   (stakeholder_refs, sn_refs: unchanged direction)
  W           SR ── da_refs ──► DA ── effect_at ──► [B]   the bundle where the outcome lands
              SR ── coincident ──   "its S alone delivers its needs"  (the explicit alternative)
  rigs        RIG ── emulates ──► EXT          a fidelity DA names its rig (realized_by)
  evidence    TC ── verifies ──► SR / LLR      TC ── assumption_refs ──► DA

EXTENSION (at DevStg-Arch, where interfaces live)
  IF ⇢ SR                     the requirement a seam answers, REACHED through its owner (as today)
  IF ── bridged_by ──► DA[]   the assumptions that carry this interface's reading to an outcome
  IF ── coincident ──         else an explicit waiver; else unclassified
```

- **Frames are a property of the bundle**, not of the party (§5.1): one actor
  can take part in both, as the human and the model provider do here.
- **Bundles keep their authored identity; membership is derived** (§5.7).
- **Assumptions get their own registry**, `assumptions.toml`, approved with the
  boundary at DevStg-Boundary, activated deliberately (§6.2, §10).
- **Each SR either cites the assumptions its argument needs or states that its
  S alone delivers its needs** — absence is unknown, never coincidence (§4).
- **Rigs are rows beside the assumptions**, not `enabling` parties: the frame's
  `enabling` means a runtime dependency (§5.3).

**The work, in packages** (§11; all wait for the sitting):

| package | what | adopter cost |
|---|---|---|
| C1. The sitting | reverse §5.2; redraw the frames; create `assumptions.toml` with its arms **off** | schema on resync, deferred |
| C2. Write the assumptions | DA rows, each a new Drafted claim; SR `da_refs` or `coincident` | none (warn-only, arms off) |
| C3. Evidence | TC `assumption_refs` and `sampling` | schema on resync, deferred |
| C4. Activation | turn the stage arms on: a deliberate stage regression and one approval batch | none beyond C1–C3 |
| C5. Gate | every SR's argument bridged or coincident, with Approved, active, evidenced assumptions; opt-in | opt-in |
| E. Extension | interface allocation at DevStg-Arch (§9) | schema on resync, deferred |
| Hats per piece | positive provenance only; `speaks_for` | template content |

Decisions and open questions: §12.

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
the frame** — by careful, consistent reasoning that §5.2 traces to one premise.
The present frame is a **delivery** frame, and delivery is not where any effect
happens.

**Validation is not absent; it is sparse, untyped and stale.** SR-054
(dashboard usability) is rubric-adjudicated, and TC-055 verifies it with a
Critique run by a fresh session over rendered screenshots. TC-036 and
TC-209–211 are Inspections. Five TCs are not automated. But none of that
evidence says which assumption it tests, nothing re-runs it (TC-055 records
*"a one-time judgement that nothing re-fires"*), and nothing asks where the rest
of the gap is. The missing piece is structured assumption provenance and a
refresh policy, not the first human check.

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

The practical consequence: **the cost of iteration scales with the size of the W
gap.** If the only way to learn whether the system delivers R is to run the
whole world, every corner case costs a full validation cycle. If W is written
down, most corner cases can be produced and caught against W instead — cheaply,
continuously — and the expensive R-level probe is reserved for sampling whether
W itself still holds.

---

## 3. Where W comes from — two sources

W attaches wherever seeing the exchange does not settle whether the outcome was
achieved. There are two independent ways that happens:

| axis | question | if "no" |
|---|---|---|
| **observability** | can the system, or something built to watch it, detect that the outcome happened? | the outcome lands where nothing built can see it; W bridges to it |
| **determinism** | does the far side *compute*, or *interpret*? | seeing the exchange does not tell you it was right; W covers the interpretation |

**Observability** is Jackson's shared-phenomena test. **Determinism** is the
oracle problem (Barr et al. 2015): a seam facing a model is fully observable —
the system sees the call, what it sent, and what came back — and none of that
says the answer was right.

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

## 4. The three words — where each lives

The formalism's nouns, "machine" and "world", drift badly outside Jackson. The
proposal keeps three words for the positions a claim can take, and puts each
where it is true:

| word | meaning | lives on | how |
|---|---|---|---|
| **effect** | the outcome a need names lands here | a DA's `effect_at` edge to a bundle | authored, required on every DA |
| **coincident** | the system's reading *is* the outcome; S alone delivers | an SR (core), an IF (extension) | an explicit waiver cell with a reason |
| **bridged** | an assumption carries the reading to the outcome | an SR citing a DA (core); an IF naming a DA (extension) | derived from `da_refs` / `bridged_by` |

**Two rules the reviews forced:**

- **Absence is unknown, never coincidence.** An SR that neither cites a DA nor
  carries a `coincident` waiver is *unclassified* — a warn-first finding. The
  first draft read "no DA" as coincidence, which broke the doctrine that an
  empty cell asserts nothing.
- **No scalar on a bundle.** A bundle holds many interfaces and many arguments;
  it cannot be one of *design* or *effect*. The view shows, per bundle, which
  assumptions land there and how its interfaces are classified — counts and
  edges, not a label. A bundle where nothing lands asserts nothing.

**A rig does not move an outcome.** A rig observes a *model* of the world, not
the world (§8.2). The outcome stays where `effect_at` says; the rig adds a
fidelity assumption and cheaper evidence beside it.

### The candidates, assessed

| candidate | verdict |
|---|---|
| `machine` / `world` (Jackson, Zave) | Citable and exact; kept in the rationale, rejected as the shipped noun. |
| `solution domain` / `problem domain` | The cut is wrong — the problem domain is the whole context, not where the outcome lands. |
| `system-of-interest` / `operational environment` (ISO/IEC/IEEE 15288:2023) | Adopted for the frames (§5.1). It names systems, not positions, so it does not replace the three words. |
| `ODD` (SAE J3016, ISO 21448, UL 4600) | Adopted for the assumption row's `holds_when` (§6.2). |
| `design system` | Unusable: in software it means a UI component library. |
| `control` / `effect` | "Control" collides with control theory and with this repo's `B-02` authority crossing. |

---

## 5. Two frames: the kit in operation, and the system that delivers it

### 5.1 Two systems-of-interest, one view

The owner's direction: the frame used to be oriented toward **the entire package
that developed the product**; it is now oriented toward **the system the user
experiences, as well as the enabling system that develops and delivers it.**

One system-of-interest cannot hold both: in an operating frame the installed
Template *is* the system, so it cannot also be that system's output. So the view
draws two, linked by the hand-off between them:

| frame | system-of-interest | its crossings |
|---|---|---|
| **kit** | the kit, as it runs in a repository (this one included) | writes, verdicts, authority, reading, the model runner |
| **delivery** | this repository's build and release — the kit's enabling system in 15288's sense | the Template leaving (`B-05`) |

**Frame membership is a cell on the bundle**, `system = "kit" | "delivery"`, not
a property of the party. The second review showed why: `class` describes a
party's role, not a frame, and the same actors take part in both frames here —
the human develops the kit and operates it; the model provider builds it and
runs in it. A party appears in the frame of each bundle it has.

**A stated simplification for this repository.** Here, development *is done
through* the kit in operation: the human's source edits reach the repository
through the same hook floor as any governed write (`B-01`). So the delivery
frame's inputs are not drawn a second time; its only crossing is the Template
leaving. For an adopter only the kit frame exists, and the Template arrives
through Transition as their enabling system (`EXT-002`'s own note says so).

**Links between the frames, typed.** Transition — the Template installed into an
operating environment — is the only **lifecycle** hand-off. Other edges also
cross the frames and are drawn as what they are: a rig's `emulates` edge to the
party it stands in for, and an assumption measured in one frame whose outcome
lands in the other.

**Where each SR sits** is derived, not judged: an SR's frame is the frame of the
bundles it cites. An SR whose bundles sit in both frames is a finding, to be
split — SR-139 (`B-02` and `B-05`) is the live example. Re-pointing
`boundary_refs` during the redraw follows the subject: an SR about the kit's
behaviour in operation (a verdict, a loop outcome, what the views show) moves to
a kit bundle — the dashboard SRs SR-052, SR-053, SR-054, SR-168 and SR-169 go to
the read bundle — and an SR about the package as a package (what the scaffold
contains, that a re-sync never clobbers) stays on `B-05`. Classifying all 69 is
sitting work (§10.3).

### 5.2 The sitting-2 rulings this reverses

Sitting 2 (2026-08-13) drew the present frame on two premises, both in its own
words:

- **13k** — the human and the loop are one entity: *"who-holds-authority is
  policy and record, never an entity split."*
- **13n** — the delivery frame: *"the system is the act of creating the
  guardrails and template contents … just because it happens to USE them as
  well doesn't mean they are each inputs into the system."*

This proposal reverses both. The rulings built on those premises follow:

| ruling / row | what it says | rests on | under this direction |
|---|---|---|---|
| **13u** — `B-03` removed | `PROJECT_STATE.html`, `open-items.html`, `docs/status.md` and `docs/gate` are *"not system outputs"* | 13k, 13n — the sitting doc itself says a separate human *"should be a deliberate reversal of 13k"* | **falls.** The human reading the spine is a crossing (§5.4). New id; `B-03` stays spent. |
| **`REL-002`** flow and notes | self-adoption; invoking `agent-resume` is *"NOT an input"*; carries 13u's surfacing | 13n, 13u | **shrinks** to the Transition hand-off (§5.5) |
| **`REL-003`** (13n), and `IF-041`'s note | model providers *"touch the SESSION, never the system"*; the runner invocation *"crosses no boundary of this system"* | 13n and 13k — the ledger's only argument is *"the loop launching its CLI — the session driving itself"* | **reversed: becomes a bundle.** Two parts survive: 13o's merge of primary and reviewer CLIs into one entity, and the backoff obligation on kit content. |
| **Hosted-CI cut** (2026-08-16q, not a sitting-2 ruling): `EXT-004`, `B-06`, `B-07` | *"this template has no design control over an external CI respecting configurations"*; `B-04`'s note: *"a hosted runner is an ADOPTER's boundary"* | 13n, the adopter entity, and `REL-002`/`REL-003` as precedent — plus **design control, which is independent** | **partly reversed.** Design control survives as the reason SR-151/152 constrain the shipped workflow *file*; it does not keep an `interoperating` party off the frame. It may return (new ids). |
| **13o** — `B-08` removed | `check_vendored` *"would be run by the development environment; it's not an input directly into this design-scope system"* | 13n | **reversed, and the reason was incomplete**: the script fetches a *"PINNED upstream raw URL"*, not a `B-01` write. Whether the upstream earns an entity is open (opt-in; this repo vendors nothing). |

The first two rows are certain, because their own text names the premise. The
last three were traced to their full log entries (`docs/log.md:1510-1566`,
`:3953-3984`; sitting-2 plan `:202-209`). `tests/test_external_frame.py` also
asserts `B-06`, `B-07` and `EXT-004` are absent, so any return is re-pinned
under the same ruling.

### 5.3 Rigs are not `enabling` parties

The first revision recorded each rig as an `EXT` row with `class = "enabling"`.
The second review found that misreads the vocabulary: the frame defines
`enabling` as *"something the system depends on to run"* (`external.toml:41-46`)
— a runtime dependency — not 15288's enabling system. A test rig is neither a
party outside the system nor something it runs on.

So rigs become their own rows, beside the assumptions whose fidelity they carry
(`[rig.RIG-##]` in `assumptions.toml`, §6.2): a name, the party it `emulates`,
and a description. The view still draws them — in the delivery frame, with a
dotted edge to the party each emulates — which is what the owner asked for: *"a
component has a maintained virtualized counterpart."* The frame's `class`
vocabulary keeps its meaning, and the entity count does not grow by three.

### 5.4 The human's three edges

| edge | what it is | bundle |
|---|---|---|
| human → **session** → system | **write, mediated**: the human edits a cell, the computer writes it, the hook floor admits it | `B-01`, governed writes in |
| human → **system** | **authority**: rulings, attestations, Status flips | `B-02`, authority in |
| system → **human** | **read**: the spine and the views generated from it | **new bundle**, out — the old `B-03` content, returned |

**Mediation is one cell.** The session carries the human's writes and shows the
human its verdicts, so the narrowed `EXT-001` row gains `mediates = "EXT-006"`.
An outcome landing on a session bundle can then be one the human experiences,
and the reach check (§6.2) can say so without a second copy of every bundle.

**Authority.** `interfaces.toml` singles `B-02` out: *"ONE CROSSING IS
DELIBERATELY REALIZED BY NOTHING: `B-02` … **has no port of its own.** Authority
enters as CONTENT on B-01's write path."* The system can observe *that a Status
cell changed*; it cannot observe *that a human judged*. So the authority
assumption lands on `B-02`, and its SRs (SR-140, SR-178, SR-179, and SR-139 in
part) cite it.

**Read.** This is where SN-002 lands: the reviewer trusts the chain by reading
it, and the system can see only that it rendered a view. **`PROJECT_STATE.html`
itself has no IF row today** — only `gen_trajectory`'s exit code (`IF-011`) —
which the extension (§9) has to fix.

### 5.5 The adopter is dropped

`EXT-003` was *"the downstream team + repo"*. The kit frame already splits that
pair: **the team is the human operator**, and **the repo is the operating
environment**.

- **One hand-off remains.** Stripped of 13n and 13u (§5.2), `REL-002` is only
  *the Template installed into an operating environment* — Transition.
  `REL-001` said the same about a different repo; one relationship carries it.
- **The value §1 located across relationships lands on bundles.** SN-001's team
  works through `B-01`, `B-04` and the read bundle; SN-002's reviewer reads
  through the read bundle.
- **`EXT-003` is spent and never re-minted**, following the
  `B-06`/`B-07`/`EXT-004` precedent.

### 5.6 The proposed frames

| row | change | frame(s) |
|---|---|---|
| *new* Human operator | **add**, `operational` | kit |
| `EXT-001` Development session | **narrow** to the computer and working copy; `mediates = "EXT-006"` | kit |
| `EXT-005` Model provider | stays; `REL-003` becomes a bundle | kit |
| hosted CI | **add**, external party under new ids (Q28; `EXT-004`, `B-06`, `B-07` stay spent) | kit |
| vendored-doc upstream | **not drawn** until a repo vendors something (Q28; `B-08` stays spent) | — |
| `EXT-002` Template | unchanged | delivery |
| `EXT-003` Adopter | **dropped** (§5.5) | — |
| `B-01`, `B-02`, `B-04` | `system = "kit"`; `B-02` re-pointed to the human | kit |
| *new* read bundle, *new* model-runner bundle | **add**, `system = "kit"` | kit |
| `B-05` | `system = "delivery"` | delivery |
| rigs | **not frame rows** — `[rig]` rows in `assumptions.toml` (§5.3) | drawn in delivery |

**Counts.** Entities 4 → **4** (the human added, the adopter dropped). Bundles 4
→ **6** (read, model runner). Relationships 3 → **1** (`REL-001` merged,
`REL-003` promoted). Next ids from `docs/id-watermark`: `EXT-006`, `B-09`.

### 5.7 Bundles: authored identity, derived membership

`B` rows stay as authored identity rows — id, party, direction, `system`,
`carries`, status — because two things need a stable subject to cite: the
package-wide SRs (SR-031, SR-034, SR-035, SR-114) and every assumption's
`effect_at`. Their **membership** is derived from IF tie-backs, as the dashboard
already derives it (`frame_context`'s `realized_by`). The redraw re-points some
tie-backs (the generated surfaces to the read bundle; the runner invocation
gains one) and the 41 IFs whose far side is the dropped adopter, by judgment.

---

## 6. The assumption row (core)

### 6.1 Why rows, not cells

The strongest objection is that translation is everywhere: a person operates a
computer, the computer turns intent into registry cells, and even an `IF` row
facing an LLM assumes a non-deterministic judgment on its input. Two reasons,
either sufficient, for rows anyway:

1. **W needs an id so that W-evidence can be counted separately from
   S-evidence.** Otherwise a TC checking an interface's *contract* and a TC
   checking its *assumption* are indistinguishable, and the three obligations in
   §7 collapse into one counter.
2. **Pervasiveness argues *for* rows.** As a cell, the claim *"the far side
   interprets, so its output needs judgement rather than comparison"* would be
   written ~45 times (§3). One row with one status, one `holds_when` and one
   falsifier, cited where it applies, is PROCESS.md §3's 0→A→B rule applied to W.

### 6.2 How the rows connect

**Requirements keep their links; they gain one.** An SR keeps `sn_refs` and
`boundary_refs` exactly as today. It adds **either** `da_refs` — the
assumptions its argument rests on — **or** a `coincident` waiver stating why
its S alone delivers its needs. An SR with neither is *unclassified* (§4).

The first draft (and the owner's Q11 answer) moved the need link to the
assumption whenever one existed. The data shows why that fails: one interface
serves several arguments. `IF-134`, the hook floor, is where SR-017 and SR-018
(privacy, SN-009), SR-019 and SR-020 (SN-005, SN-009) and SR-137 (SN-028) all
meet — and the authority assumption, serving SN-029, measures there too.
Inheriting needs through it would give the privacy SRs the authority
assumption's need. Removing SR `sn_refs` would also rewrite stage derivation,
the orphan checks, the trace forest and every renderer (123 references across 54
script and test files).

**An assumption's needs are derived** from the SRs citing it, so the link lives
in one place.

**The DA row.** It lives in a dedicated registry, `docs/requirements/assumptions.toml`
(§10.1 says why not `external.toml`), approved at **DevStg-Boundary** — the
owner's ruling: *approving the boundary and the assumptions that make that
boundary possible are the same act*.

```toml
[assumption.DA-###]
effect_at     = ["B-##"]        # required: the bundle(s) where the outcome lands
assumption    = """A spine the strict check passes with zero orphans is one a
                   reviewer can rely on: each row says something, and the links
                   between rows are the ones a reviewer would draw."""
holds_when    = """Rows are authored under the spine-authoring question list;
                   the reviewer reads the generated views, not raw TOML."""
obstacle      = """Every row resolves and every row says nothing: an
                   orphan-free, semantically vacuous spine."""
falsifier     = """A sampled reviewer, reading the views cold, finds a traced
                   row that says nothing the reviewer would rely on."""
status        = "Drafted"       # maturity: Drafted | Approved
standing      = "active"        # validity: active | falsified
accepted_risk = ""              # optional: why it is relied on without evidence
```

Cited by SR-157 (*"spine and work-registry rules red the harness verdict"*), so
its needs derive to SN-002 and SN-025, and it lands on the read bundle.

**`effect_at` is required**, and it is constrained. A stakeholder names a party,
not a bundle — the human has two — so the assumption must say where its outcome
lands. The bundle's party must be the served needs' stakeholder party, or a
party that `mediates` for it (§5.4). The one exception is a **fidelity**
assumption, which names its rig (`realized_by = "RIG-##"`) and lands on the
emulated party's bundle: its claim is about the rig matching the real party, not
about a stakeholder's outcome.

**Maturity and validity are separate fields.** An Approved assumption can later
be falsified, so `status` keeps the shared `Drafted | Approved` vocabulary and
`standing` is a separate closed field — the same separation the kit already made
between lifecycle and maturity on components.

**`falsifier` is a description, not a link.** The TC → DA link lives only on the
TC (`assumption_refs`, §7); the DA's `falsifier` describes the signal. The rule
REAssuRE's monitored claims and UL 4600's Safety Performance Indicators both
imply stays: **an assumption with no declared falsifier is an untested
assumption.**

**The stakeholder link.** Needs gain `stakeholder_refs`, citing rows in a small
stakeholder list kept beside them (`[stakeholder.STK-##]` in
`stakeholder-needs.toml`): a name, optionally the party it is (`party =
"EXT-###"`), and a `status`. The need cites the stakeholder, child to parent, so
the relation has one home. Provenance for a design-constraint need lives on the
need, not on the stakeholder row (the sister plan, §1.3). A need that an
assumption serves must have at least one stakeholder with a `party`, or the
reach check has nothing to check.

**Rig rows** sit in the same registry:

```toml
[rig.RIG-##]
name        = "Scripted model runner"
emulates    = "EXT-005"
description = """FAKE_AGENT: answers the runner contract from a script;
                 reproduces protocol, not judgment."""
status      = "Drafted"
```

**Rig and stakeholder rows carry `status`, and it is wired**, because
`emulates` and `party` are load-bearing: they decide fidelity and reach.

| tier | approved at | in which act | the gate relies on it when |
|---|---|---|---|
| rig | DevStg-Boundary, with the assumptions | the same brief and batch as the DAs (C4) — a fidelity DA and its rig are judged together | a fidelity DA counts only if its rig is Approved |
| stakeholder | DevStg-Needs, with the needs — human-held here | the needs' approval act (C1) | the reach check reads only Approved stakeholder rows |

Each of those files then holds two approvable tiers (assumptions and rigs; needs
and stakeholders), so approval must be tier-specific, not file-wide (§10.1).

**`da_refs`, when present, is non-empty.** An empty list asserts nothing and is
treated as absent.

Three cells are borrowed, each with a standard behind it: **`holds_when`** is an
ODD (SAE J3016 / ISO 21448 / UL 4600), bringing the **restriction move** with it
(§7(d)); **`obstacle`** is van Lamsweerde & Letier's obstacle — a generator, not
a comment, driven by hats (§6.5); **`falsifier`** is REAssuRE's and UL 4600's.

Two more rows the redraw makes available at once:

```toml
[assumption.DA-###]
effect_at    = ["B-02"]         # the authority bundle
assumption   = """A changed Status cell on a human-held rung means a human
                  actually exercised the judgment that Status asserts."""
holds_when   = """The row's rung is at or below the human_approval_through
                  dial in docs/process.toml."""
obstacle     = """A Status change on a human-held rung arrives in a commit the
                  unattended loop authored."""
falsifier    = """A commit carrying the loop's provenance trailer that changes
                  a Status cell on a human-held rung."""

[assumption.DA-###]
effect_at    = ["B-01"]         # governed writes; the session mediates for the human
assumption   = """A write the local hook floor admitted was checked: the floor
                  was not bypassed, or a re-run of the same bar agrees."""
holds_when   = """Commits are not made with --no-verify, or a re-run of the bar
                  away from the session is in place."""
obstacle     = """git commit --no-verify admits an unchecked write, and nothing
                  re-runs the bar."""
```

The first is cited by SR-140, SR-178 and SR-179 (SN-029). It is what `Attest`
and the attested-vs-mechanized split exist to protect, stated for the first time
as something falsifiable — scoped by `holds_when`, because this repo sets
`human_approval_through = "DevStg-Needs"` and for SR, LLR and TC rows a Status
change is not a human act, by policy. Its falsifier needs a **validated loop
provenance trailer**, which does not exist yet: loop worker commits carry `WI:`
trailers, but not on every loop commit and nothing validates them (§10.2). The
second is cited by SR-019 and SR-020 (SN-005, SN-009): the bypass limit `B-04`'s
note already records, now as a row.

**Checks the rows make possible** (warn-first; §11):

- an SR with neither `da_refs` nor a `coincident` waiver — *unclassified*;
- a DA that no SR cites, with no `falsifier`, or with an `effect_at` whose party
  is neither the served stakeholder's party nor a party that mediates for it;
- a rig no fidelity DA names;
- a need whose stakeholder is a kit-frame party, where none of its SRs sits on a
  kit bundle and no assumption it rests on lands on one — the frame is missing a
  bundle, or the need names the wrong stakeholder (`REL-001` and the read edge
  were both found this way, by hand);
- an SR whose bundles sit in both frames (§5.1).

### 6.3 Which assumptions become rows

*"The computer turns the user's keystrokes into registry cells"* is true, is an
assumption, and should obviously not be a row. The stopping rule:

1. **The obstacle test.** An assumption earns a row when you can write a
   **non-silly `obstacle`** for it. *"The keyboard emits characters other than
   those pressed"* fails. *"A team green-scaffolds and operates a spine that
   says nothing"* passes.
2. **The interpretation trigger.** Wherever the far side interprets rather than
   computes (§3), *suspect* an assumption.

The same filter covers the trusted layer — the OS, git, the terminal, the
interpreter: implausible failure, no row; plausible and costly, a hat asks how
the system responds (§6.5). Behind both sits NASA-STD-7009's rule:
**credibility proportional to the risk of the decision the evidence supports.**

**Writing the rows is derivation, not transcription.** The claims are written
down nowhere, and a row such as *"the team reads ADOPTING.md before first use"*
adds a new precondition. Each DA is a newly derived Drafted claim, reviewed
through its own approval brief (§10.2).

### 6.4 Writing a good one

- **An over-strong W is a defect, not safety** (Cobleigh, Giannakopoulou &
  Păsăreanu, TACAS 2003): an assumption broad enough to make the entailment
  trivially true has moved the problem, not solved it.
- **For a rig, state the delta, not the resemblance.** The *"nearly"* in *"the
  same interface (or nearly the same)"* is the fidelity assumption.

| weak — states the resemblance | strong — states the delta |
|---|---|
| *"the contact model grips like the real gripper"* | *"the contact model omits deformation and stick-slip; above ~X N the sim over-reports grip"* |
| *"the fake runner behaves like a model CLI"* | *"the fake runner reproduces argv/stdin, exit codes and commit effects; it reproduces no judgment, so nothing about prompt quality is evidenced here"* |

- **Hardening narrows the DA.** When an interpreting seam is hardened —
  schema-constrained output checked by a validator — the checked part moves into
  S, and the DA is rewritten to state only what remains assumed.

### 6.5 Hats: the lens applied to each piece

Stakeholders and hats do different jobs, and `hats.toml` already says so:
*"A HAT IS NOT A PERSON AND NOT A STAKEHOLDER ROW. It is a QUESTION that must be
put to every decomposition it applies to."* A **stakeholder** owns an outcome;
a **hat** owns a failure class (`asks` + `listens_for`). Some hats are a
stakeholder's voice used as a lens (FIRST-RUN-ADOPTER, UX-DESIGNER); an optional
`speaks_for = "STK-##"` on those records it, and re-anchors FIRST-RUN-ADOPTER,
which was anchored to `EXT-003` — a party, not a stakeholder.

**A hat constrains the specification; it does not always create a
requirement.** Applied to a piece of the chain, a hat that bites produces one of
four things:

| a hat applied to… | produces |
|---|---|
| an SR | a **constraint**: a tightened acceptance clause (`hat_refs`) |
| a whole bundle | a **cross-cutting property**: one SR against the bundle (the package-wide class) |
| a gap nobody stated | a **new SR** — the rare case |
| a DA | an **obstacle**: UNATTENDED-OPS asking *"what happens when its input is missing, stale, or half-written?"* writes the DA's `obstacle` cell |

**Only positive provenance is recorded** — `hat_refs` on the rows a hat changed,
and which hat generated an obstacle — not a "not applicable" record per hat per
row, which would have no consumer. Hats fire today on SN → SR decomposition,
keyed on tags; firing them per DA needs DA tags, or a composer per bundle.

---

## 7. Three test obligations, and why they are affordable

If the argument is `S ∧ W ⊨ R`, evidence is owed on three fronts. The kit
currently collects one systematically.

| # | evidences | where evidence sits | cost | cadence |
|---|---|---|---|---|
| **1** | **S** | a TC that `verifies` an SR or LLR | cheap | every commit — nearly all 194 TCs today |
| **2** | **W** | a TC whose `assumption_refs` names the DA | cheap-to-moderate — *free where it is a metamorphic relation, (c)* | continuous or event-triggered |
| **3** | **R through W** | the bundle where the outcome lands, via a translation or a rig | expensive — *a rig splits the cost rather than removing it (§8.2)* | sparse, sampled — *see the limit below* |

**W-evidence has its own field.** `Verifies` means SR or LLR everywhere — the
trace forest, the SR → LLR → TC matrix, phase grouping (`derive_stage.py:144-151`)
— so assumption evidence gets `assumption_refs`, and `Verifies` becomes required
*unless* `assumption_refs` is present. A TC that only evidences an assumption is
valid on its own (the intent of Q5). It takes its phase from the SRs citing the
assumption, and `assumption_refs` joins stage-change attribution, the acceptance
record's classification, the census and the reports (§10.2).

**Evidence is a result, not a test's existence.** The third review was right
that a TC *specifying* a check is not evidence: PROCESS.md says *"`Approved` says
the row's TEXT is blessed and says nothing about tests passing — whether they
pass is the harness's answer, never a cell's."* So an assumption's evidence
standing is derived from **results**:

| standing | derived when |
|---|---|
| `assumed` | no TC evidences it |
| `specified` | a TC evidences it, but there is no current passing result |
| `monitored` | a current passing result from an automated or monitoring TC |
| `sampled` | a current passing result from a sampled TC — a human probe or a measurement |

**Where results live.** An automated assumption TC joins the existing
tree-bound suite verdict (`docs/test/evidence`). A sampled or monitored
observation cannot be re-run per tree, and putting it on the approved TC would
mix the test's specification with its results and force a re-attestation after
every sample. So observations get **their own result record**, keyed by TC:
outcome, when it was observed, by whom or what, when it expires, and a digest
of the state it judged (the rows and artifacts the check reads). The TC keeps
only its policy — `sampling` and `max_age`, which may not be under seven days
(Q25). **One freshness model:** a record is stale when it passes its expiry,
or when, at a checkpoint, the digest of what the check reads no longer matches
the judged digest (the sister plan's S6 uses the same rule and record). A stale
record makes the standing `specified` again; a failing one is falsification evidence against the
assumption.

**A passing sparse sample does not satisfy the gate by itself.** The limit below
says so — *a passed sparse probe is not evidence that an assumption holds* — so
the gate cannot count it as if it were. An assumption whose only evidence is
`sampled` clears the gate (§11, C5) only with one of: a declared sampling model
and threshold that justifies a positive claim (sample size, acceptance rule); a
`holds_when` narrowed until an automated check covers it; or a recorded
`accepted_risk`. Sparse samples keep their real job: falsification.

**`accepted_risk` reopens on triggers** (Q29): a failed sample, a change to the
text of a need the assumption serves, or a change to the assumption's own text
returns its evidence standing to unproven until the risk is re-accepted or
evidence arrives. There is no clock: a risk does not lapse because time passed.
An assumption-only TC may belong to several phases, as the SRs citing its
assumption may; `derive_stage` already places one TC in several phase groups.

Obligation **2** is the new one. Tests of W are often not software tests at all:
measurements, monitors, sampled observations, or a recorded check that a
precondition still holds. For SN-001's assumption, a W-test is *"take a shipped
profile, scaffold it, and have someone who has not read the source reach a first
filled registry"* — not cheap, but enormously cheaper than validating "an
adopting team gets a working process", and it fails in the same direction.

The mechanisms that make this affordable, in the order they matter:

**(a) The probe count is bounded by the assumptions, not by the input space.**
The same allocation rule is normative in aerospace structures as the
**building-block approach** (FAA AC 20-107B; CMH-17 Vol. 3): *run many cheap
low-level tests to bound variability so that very few expensive high-level tests
can be justified.*

**(b) Corner cases are generated, not imagined.** Each `obstacle` yields at
least one adversarial case: *what if this does not hold?*

**(c) Some W is executable, at ordinary CI cost.** A **metamorphic relation**
(Chen, Cheung & Yiu, 1998) tests a necessary property across executions without
knowing any single correct output. Most useful MRs are statements about the
world (*"adding an unrelated registry row must not change an unrelated row's
status"*), so **writing an MR is writing a testable domain assumption.**

**(d) Narrowing the declared world is a legitimate answer.** SOTIF (ISO 21448)
sanctions two responses to a gap: improve the system, **or restrict the ODD**.
When `S ∧ W ⊨ R` will not close, narrow `holds_when` until it does, and say so.

### The limit on sparse sampling

Sampling the human axis sparsely gives a **high-variance lower bound on
discovery, not a coverage claim.** Faulkner (2003) found random 5-user sets
caught anywhere from **55% to 99%** of known problems; Schmettow (2012) shows
discovery is over-dispersed. So **a passed sparse probe is not evidence that an
assumption holds; only a failed one is evidence that it does not** — and the
same holds for a green run against a rig. If a human-axis assumption is
load-bearing, the honest options are to restrict the ODD or accept a recorded
risk.

---

## 8. Enabling systems and rigs

### 8.1 Enablement, and where verification sits

ISO/IEC/IEEE 15288:2023 (3.15) defines an enabling system as one that
*"supports a system-of-interest during its life cycle stages but does not
necessarily contribute directly to its function during operation"*; *"each
enabling system has a life cycle of its own."* The stages are concept,
development, production, utilization, support and retirement (ISO/IEC/IEEE
24748-1:2024). Deployment is served by the **Transition** process (6.4.10). In
this proposal the delivery frame's system-of-interest *is* the kit's enabling
system (§5.1). Note the vocabulary clash §5.3 resolved: the frame's own
`enabling` class means a runtime dependency, not this.

**Verification sits outside the classification.** Every system needs
verification around it: `tests/` verifies the harness, and CLAUDE.md traces
`tests/` as product. Three independent axes:

| axis | applies to | recorded as |
|---|---|---|
| **is it verified?** | *everything* | ordinary tests |
| **does it discharge a spine requirement?** | whatever a requirement is written about | a TC with `verifies` |
| **does it stand in for something else?** | rigs only | a rig row with `emulates`, and a fidelity DA |

### 8.2 Translation and rig: one construct at two weights

- A **translation** converts an effect into something the system can check by
  *claiming* the conversion holds: a DA alone.
- A **rig** converts it by *performing* the conversion — simulating the effect
  and putting the output against a rubric: a DA with `realized_by`.

**A rig plugs into an interface that already exists.** It presents the same
interface as the party it replaces; only what is plugged into the far side
changes. It costs one rig row and one fidelity DA — no new interface, no bundle,
no entity.

**What a rig buys, and what it does not.** It does not make the real phenomenon
observable, so **the outcome stays where the served assumption's `effect_at`
says**. It makes a *model* of the world observable, and the evidence gets
cheaper:

| the assumption before the rig | the assumption after |
|---|---|
| *"zero orphans ⟹ a reviewer trusts the chain"* | *"a model judging the rendered artifact against rubric R judges as a human would"* |
| *"this current curve ⟹ the apple is gripped"* | *"the contact model grips like the real gripper does"* |

The left column is untestable in principle; the right is a **fidelity**
assumption — bounded, and testable by calibration. The product changes every
commit and the rig changes yearly, so obligation 3 **splits**: cheap and
continuous against the rig, expensive and sparse against the rig's fidelity.

### 8.3 The rigs this repo already runs

| rig | emulates | what it is | fidelity delta |
|---|---|---|---|
| **Scripted model runner** | `EXT-005` | `FAKE_AGENT` (`tests/test_agent_loop.py:34`) answers `IF-041`'s runner contract from an `actions.txt` script | reproduces protocol, not judgment — *a model good enough to stand in for a model is circular* |
| **Scaffold rig** | `EXT-001` | the scaffold fixture (`tests/conftest.py:1-7`): *"bootstrap a real scaffold in a temp dir and run the actual commands"* — the narrowed session is the operating environment | an adopter property the temp dir lacks (existing hooks, CRLF settings, a monorepo layout) |
| **Render critic** | `EXT-006` | `render-dashboard-critique` plus a vision model over declared width/theme/tab renders; two consecutive approvals at one content hash | a model revision shifting judgment silently; a rubric overfit to one model's eye |

The scaffold rig also settled the old `REL-001` question: the registry's rule
that a relationship *"must never grow a realizing IF row. **Wanting one means
what you have is a boundary crossing**"* could not coexist with a rig that had
been standing at `REL-001` since before the frame was drawn.

What nothing does today is treat **the judge** as an assumption:

```toml
[assumption.DA-###]
effect_at    = ["B-##"]         # the read bundle — the emulated party's
realized_by  = "RIG-##"         # the render critic
assumption   = """A vision model judging the rendered dashboard against the
                  rubric reaches the verdict a human reviewer would."""
holds_when   = """An image-capable model; the rubric carries its accumulated
                  anchors; a static render at a declared width and theme."""
obstacle     = """A model revision shifts judgment silently; or the rubric
                  overfits to anchors accumulated under one model's eye."""
falsifier    = """A periodic human Attest sample that disagrees with the
                  critic's verdict."""
```

Cited by SR-052, SR-053 and SR-054 (SN-023, SN-024).

### 8.4 The self-derivation limit

This repo cannot dogfood its own development scripts: executing the scripts
being modified has repeatedly failed to give a usable result. The general rule:

> **A rig derived from the system under test cannot falsify assumptions the two
> share.**

Self-execution is the limit case: the rig *is* the system, and can falsify
nothing. It is also why `FAKE_AGENT` has the right shape: a scripted stand-in
that does not run the real thing shares no assumptions with it.

---

## 9. Extension — interface allocation at DevStg-Arch

The owner's augmentation: *a specification needs to be testable, so its
interface must be either defined or clearly assumed.* The core already carries
the *"clearly assumed"* half (§6.2). This extension carries the *"defined"* half
— without breaking the stage ladder, which the first revision did.

**Why at the architecture rung.** PROCESS.md: *"**Requirements come before
architecture**, because architecture is a response to requirements … An
interface and a requirement say different things — an interface says what
crosses (provider, consumers, contract, type), a requirement says what must be
achieved — so neither derives from the other."* Every IF row is approved at
DevStg-Arch. The first revision moved boundary IFs to DevStg-Boundary so SRs
could cite them; the second review was right that this approves architecture
before the requirements it serves. So the link is made **from the architecture
side, at the architecture rung**:

- **The requirement a seam answers is already derived — keep it that way.**
  `interfaces.toml` rules that an IF row states no requirement: *"the requirement
  this seam answers to is REACHED through the owner — the design rows whose
  `module` names it, or the `Implements:` line in its header — and is not stated
  on the row"*, and a requirement-reference cell is a retired strict finding. The
  third revision proposed a `realizes` cell; the fourth review was right that it
  would reverse that rule and give the relation two homes. So the extension uses
  the derived relation: IF owner → the design rows naming that module → their
  SRs. An IF may reach several SRs that way, which is fine: the relation is
  "answers to", not "is defined by".
- **An IF names the assumptions that bridge its reading** (`bridged_by =
  ["DA-###"]`). The allocation lives on the **IF row**, which is approved at
  DevStg-Arch, so the Arch approval owns both edges. The previous draft put
  `measured_at` on the assumption instead; the third review was right that
  adding it at Arch would mutate a row already approved at Boundary, which is
  either unblessed drift or a re-attestation during Arch. The assumption row
  stays exactly as approved.
- **Each boundary IF is classified**: *bridged* (`bridged_by` non-empty),
  *coincident* (an explicit waiver cell on the IF), or *unclassified* (a
  finding).

**No synthetic interfaces.** 69 SRs sit on `B-05` against 39 `B-05` IFs, and
each real IF carries a contract body beside its code and a contract test
(PROCESS.md:1181-1208). New IF rows are minted only for genuine seams — the
dashboard itself is one (§5.4) — never to match a count. All 167 IF rows are
still Drafted, so their approvals are owed regardless.

**An SR carries an explicit form** — introduced in the core (C2, §10.2k) so it
rides the same re-attestation batch, and used here: an SR reached by no
interface must not look the same as one meant to rest only on an assumption.
`form = "interface" | "assumption" | "package-wide"`, a closed cell; absence is
a finding, not a default.

**What the extension adds to the gate** (§11, C5): every SR of form
`interface` is reached by at least one boundary IF through the derived relation,
and each such IF is `coincident`, or is bridged by an assumption the SR also
cites.

---

## 10. Impact

Surveyed against the code on 2026-09-20 and re-checked against both reviews on
2026-09-23. Anchors are given so the next session can start from them.

### 10.1 Why a dedicated `assumptions.toml`

The owner preferred no new registry, and the first revision put DA rows in
`external.toml`. The second review found, and the code confirms, that this
would silently re-bless unrelated drift in the LOCKED frame rows:
`baseline_snapshot.py` keys its authorization ledger **by file path**
(`:565-583`), and a file with any approval flip suppresses the refusal for every
absorbed change in that file (`:660-667`). Approving one DA inside
`external.toml` would authorize whatever else had drifted in the entity,
boundary and relationship rows. A dedicated file gets its own ledger entry. It
also settles:

- the **one-path-per-id-column** rule of `test_dogfood_sync.TOML_REGISTRIES`
  (`:246-312`) — `DA-ID` and `RIG-ID` get one path each;
- the **approval act**: `acceptance_record.OUTSIDE_THE_APPROVAL_ACT` puts
  `external.toml` outside the approval-act rung by ruling; a new registry joins
  one side deliberately — proposed: inside, with its own approval brief (§10.2),
  since DA approval is a judgment the owner wants human-held;
- the **lock**: `external.toml`'s rows keep changing only by ruling; DA rows
  follow ordinary Boundary-rung approval.

**But a separate file is not enough on its own: approval must be
tier-specific.** The third review found the same coalescing one level down:
`assumptions.toml` holds assumptions *and* rigs, and `stakeholder-needs.toml`
would hold needs *and* stakeholders. The fourth review showed the fix is larger
than re-keying a ledger: the approval identity is a registry path end to end —
`--approves <path>=<ref>` is parsed per path (`baseline_snapshot.py:277-304`),
the refusal compares path names (`:644-675`), authorization selects whole
registries (`:785-854`), and the writer copies the whole file (`:857-890`).

Two ways out, to be chosen at the sitting:

| option | what it takes | also fixes |
|---|---|---|
| **tier-specific approval identity** — path plus id column, through parsing, refusal, write scope and stamping; the whole file is copied only after every other tier in it is shown to have no unapproved drift | a real change to `baseline_snapshot` and its tests | the same hazard in `external.toml`'s three tiers, which exists today |
| **one tier per file** — rigs and stakeholders in their own files | two more registries, each with the new-registry machinery of §10.2b | nothing beyond the new tiers |

**Owner ruling (Q26, 2026-09-23): neither — row-level refusal.** Each row
already carries its own Status, and the snapshot copy is the owner's asserted
definition of the file. What the copy must not do is carry an edit the owner
never saw. Today a refresh is refused only when a file has drifted approved text
and **no** approval in the act (`baseline_snapshot.py:667`); once any row in the
file flips, every drifted row is copied with it. The ruling: an approval act
refuses to refresh a file's snapshot while any **other** row in it has drifted
approved text that the act does not itself approve or re-attest. Each drifted
row must be explicitly in the act. This works for any number of tiers in one
file, so neither option above is needed, and it closes the same gap in
`external.toml` today.

**Internal assumptions** — the owner's case of an LLM *inside* the system
handing structured output to a script — are **design-tier** assumptions: they
pair with design expectations, not requirements, and belong at DevStg-Arch. This
repo has none (its model is `EXT-005`, outside), so the proposal records the
direction — a second id space at the design tier when the first such seam
appears — and builds nothing for it now.

### 10.2 The edit list — core

**(a) The frame redraw — a sitting.** `tests/test_external_frame.py:87-114` pins
the counts and spent ids, and `:128-146` pins every `status`; its docstring says
it **is expected to be edited by a sitting and by nothing else**. New cells:
`system` on bundles, `mediates` on entities. The reversed rulings carry prose:
`REL-002`'s flow and notes, `EXT-005`'s description, `IF-041`'s note, `B-04`'s
note. FIRST-RUN-ADOPTER's `EXT-003` anchor (`tests/test_hats.py:885-900`) moves
to a `speaks_for` stakeholder.

**(b) `assumptions.toml` — a new registry, no new rung.** The 13-edit new-registry
survey included a new ladder rung; this needs none, because its rows join
existing rungs' predicates. What it does need: `DECLARED_INPUTS`
(`kitlib/stage.py:144`), `bootstrap.MAPPING`, the snapshot tiers
(`baseline_snapshot`), `TOML_REGISTRIES` and its floor, the id watermark
(`trace.py:920-928` `_offspine_ids`; the missing-watermark hole has happened
here twice), the carrier maps (`spine_carrier` / `migrate_carrier`, which must
invert and match in length), the schema of record, the template, and resolution
of `effect_at`, `realized_by`, `emulates` and SR `da_refs`.

**(c) Stage arms — present, but off until activation.** Drafted rows are
excluded from the selection stage (`derive_stage.py:183-190`), so a later
draft never lowers it. The exception is a registry that exists with **no**
settled row: the Boundary predicate reads that as a frame declared and not yet
approved (`spine_rules.py:492-496`), and the fold returns Boundary before any
later rung (`spine_rules.py:633-652`). A new `assumptions.toml` is exactly that
registry until its first rows are Approved. The arm therefore ships **off**, and
is switched on in the same commit that approves the first batch (§11, C4), so
no committed tree reads the regression.

**(d) SR cells.** `da_refs` and the `coincident` waiver; `sn_refs` and
`boundary_refs` untouched.

**(e) Evidence on TCs.** `assumption_refs`, `sampling` and `max_age` (validated
against a seven-day floor, Q25); `Verifies` becomes
conditionally required (`trace.py:445-454`, `coherence.py:91-104`); phase
inheritance for assumption-only TCs; `assumption_refs` in stage-change
attribution (`derive_stage.py:288-294`), the acceptance record, the census, the
reports and the approval briefs.

**(f) The stakeholder list.** `[stakeholder.STK-##]` rows and SN
`stakeholder_refs`, with the same registry machinery as (b) on
`stakeholder-needs.toml`, which is already fingerprinted.

**(g) A DA approval brief and act.** `trace.spine_chain` and the approval model
render only SR, LLR and TC (`trace.py:3085-3110`). A human-held assumption
approval needs a brief showing the citing SRs, the derived needs, the landing
bundles, the evidence and the falsifier.

**(h) Enforcement of human-held approval.** The dispatcher's off-spine approval
axis *"DEFAULTS FALSE AND EVERY CALLER IN THIS MODULE PASSES THE DEFAULT"*
(`dispatch.py:337-355`), so moving `human_approval_through` to DevStg-Boundary
(Q14) does not by itself stop an automated path. It needs registry identity
threaded through admission, or a commit-time refusal.

**(i) Loop provenance.** A validated trailer on every loop-created commit,
checked by the commit-msg hook — the prerequisite for the authority assumption's
falsifier.

**(j) Row-level refusal** in `baseline_snapshot`'s refresh check (Q26, §10.1).

**(k) Classifying the new cells, and re-attesting what is approved content.**
The acceptance classifier fails safe: an unclassified column is approved content
(`acceptance_record.py:296-302`). But link cells have a ruled home among the
**traced** cells — `SN-Refs`, `Boundary-Refs` and `Hat-Refs` on SRs, `Verifies`
on TCs — which do not arm a re-attestation (`acceptance_record.py:236-270`). So
each new cell is classified explicitly:

| cell | class | consequence |
|---|---|---|
| SR `da_refs`, SN `stakeholder_refs`, TC `assumption_refs` | **traced** — pointers, like `SN-Refs` and `Verifies` | no re-attestation; a changed `da_refs` routes to adjudication, as a re-pointed `SR-Refs` does |
| SR `coincident` waiver, SR `form`, TC `sampling`, TC `max_age` | **approved** — prose or policy the row now asserts | the rows that gain them are re-attested |

So the batch before activation is the SRs that gain a `coincident` waiver or a
`form`, and the TCs that gain a `sampling` policy — not every row a link touches.
`form` moves from the extension into C2 so it rides the same SR batch rather than
opening a second one. That is still the core's largest human cost, and the
reason C2's writing and C4's activation are separate steps.

**(l) Evidence results.** Automated assumption TCs join the tree-bound evidence
record; sampled and monitored observations get their own result record keyed by
TC (outcome, observed-at, provenance, expiry), with a writer, validation, stale
and failure behaviour, and the gate as its reader (§7).

### 10.3 The edit list — extension

- IF `bridged_by` and the per-IF `coincident` waiver; the derived IF → SR
  relation used as it is today (SR `form` has moved into the core, §10.2k).
- **All 79 SRs mapped to real seams**, with recorded waivers where seams are
  shared and new IF rows only for genuine seams — each with its contract body,
  its contract test and its approval.
- The 41 IFs whose far side is the dropped adopter, re-pointed by judgment.

### 10.4 What will actually hurt

**Prose has almost nowhere to go.**

| file | cap | now | headroom |
|---|---|---|---|
| `AGENTS.template.md` | 10,000 | 9,980 | **20 B** |
| `CLAUDE.md` | 8,500 | 7,975 | 525 B |
| `byte-budget-guard/SKILL.md` | 5,000 | 4,613 | 387 B |

Any edit to a capped file must re-stamp the skill in the same commit
(`test_bootstrap.py:443+`). This concept's prose home is `PROCESS_OPTIONS.md` or
`ADOPTING.md` / `EXAMPLE.md`, **not** `AGENTS.template.md`.

**Mandatory for adopters, on resync:** the schema changes in C1, C3 and E —
template/schema equality is enforced (`test_dogfood_sync.py:339-405`). **Optional
for adopters:** the gate (C5). The resync entries are deferred until this repo's
model is firm.

### 10.5 Adjacent findings

1. **This repo has not recorded Release evidence.** `docs/test/evidence` is the
   sole input to `DevStg-Release`; `record_test_evidence.py` exists to write it.
2. **Per-requirement coverage lives in `trace.py`**, not `plan_coverage.py`.
3. **The SN `priority` vocabulary and the WI `Priority` integer are
   unconnected.**
4. **`Permutations` + `gen_cases.py` is a dormant layer**, pinned unused by
   `test_dogfood_sync.py:515-519`.
5. **The dashboard has no IF row** (§5.4).

---

## 11. Staging

Nothing is built before the sitting. Each step is useful alone, and each later
step assumes only the earlier ones.

**C1 — the sitting.** Reverse the §5.2 rulings deliberately; land the §5.6 rows,
including hosted CI as an external party under new ids (Q28)
(§10.2a); create `assumptions.toml` and the stakeholder list with their stage
arms **off** (§10.2b–c, f); approve the stakeholder rows with the needs, as a
human-held act. If the owner rules the sister plan's S3 with Q12, the
constraint-provenance cell on needs lands here too: the cell, its carrier and
template entries, validation, rendering and dogfood sync.

**C2 — write the assumptions.** DA and rig rows derived from the person-facing
needs — each a new Drafted claim — and, on every SR, `da_refs` or a `coincident`
waiver, and its `form`. **Warn-only, genuinely:** the arms are off, so nothing moves the derived
stage.

**C3 — evidence.** `assumption_refs`, `sampling` and `max_age` on TCs, with the
seven-day floor checked mechanically; result records carrying the judged-state
digest (§7, §10.2e, l). `sampling` and `max_age` are approved content, so the TCs
that gain them join C4's re-attestation batch. Start with the metamorphic subset
(§7(c)). Designed together with the sister plan's S6 runner.

**C4 — activation, in one reviewed commit (Q20).** With the arms still off, the
owner reviews two batches: the **re-attestation batch** for the SRs and TCs whose
approved content C2 and C3 changed (§10.2k), and the **assumptions and rigs**
through their brief (§10.2g). One commit then carries the re-attestations, the
DA and rig approvals and the arm switch, under the moved dial and its
enforcement (§10.2h), with row-level refusal in place (§10.2j). No
committed tree reads a regression. If one did, `check.py` would deselect its
three DevStg-Tests steps (`smoke`, `design-flows`, `trajectory`; this repo's
`smoke` step is declared in `docs/stack.ini`) for the window.

**Findings, from C2 on** — warn-only: the §6.2 checks; a `falsified` assumption,
reported with every SR and TC that cites it; an Approved, active assumption that
is only `assumed` or `specified`; a Status change on a human-held rung in a
commit carrying the loop trailer (once §10.2i exists).

**C5 — the gate — split by rung, so it cannot deadlock.** Opt-in for adopters,
with an applies-when; **enabled in this repository**, which is Q27's condition.
The switch's home is settled with C5's implementation, and turning it on here
is part of C5, not a later option. Passing
results exist only after the harness runs, so evidence cannot gate an early rung.

- **At DevStg-Boundary — maturity only:** for every SR, either its `coincident`
  waiver holds, or each assumption it cites is **Approved** and **active**,
  lands on its stakeholders' party (or a mediating one), and — if a fidelity
  assumption — names an Approved rig.
- **At DevStg-Release — evidence, after the harness:** each of those assumptions
  has a **current passing result** of the right kind (§7: `monitored`, or
  `sampled` with a justified sampling model) or a recorded `accepted_risk`. This
  sits beside the existing Release input, `docs/test/evidence`, which the harness
  writes after a passing run.

With the extension, the Boundary half also runs per reached boundary IF (§9). The
vision promises work built *"test-first with explicit approval gates so you can
trust what ships"*; without this step, the assumption rows are optional
documentation.

**E — the extension**, at any point after C4: interface allocation at
DevStg-Arch (§9, §10.3).

**Hats per piece** can land any time after C1's stakeholder list.

**T — terminology**, any time: one prose pass for the SR wording (Q9) and
LLR → design expectation (the sister plan's S2), with one PROCESS.md glossary
line each. Id prefixes and rung names are unchanged; changing them is a
separate later decision.

**Not proposed:** a new stage rung; deleting the `B` rows; moving interfaces to
DevStg-Boundary.

---

## 12. Decisions and open questions

### 12.1 Decisions

Owner answers, 2026-09-21 to 2026-09-23. `DECIDED` means the next sitting may
build on it; `OPEN` and `REOPENED` mean it may not. A `REOPENED` row carries the
revision this document now proposes, for the owner to accept or reject.

| # | question | standing |
|---|---|---|
| Q1 | Does the human come out of `EXT-001`? | **DECIDED: yes** (§5.4). |
| Q2 | Does `REL-001` become a crossing? | **DISSOLVED** by dropping the adopter (§5.5). |
| Q3 | `frame` vocabulary: two values or three? | **DECIDED 2026-09-23 (owner accepted the revision; reopened by reviews 1, 2).** Three words kept, `coincident` explicit — on the SR in the core, on the IF in the extension. No word on a bundle (§4). |
| Q4 | How heavy is the evidence descriptor? | **DECIDED: `assumed \| sampled \| monitored`** — now homed as TC `sampling`, `assumed` derived (§7). |
| Q5 | May a W-test stand alone? | **DECIDED 2026-09-23 (owner accepted the revision), intent kept.** Yes, through TC `assumption_refs`; `Verifies` conditionally required (§7). |
| Q6 | Does a rig get its own crossing? | **DECIDED 2026-09-23 (owner accepted the revision; reopened by review 2).** Still no crossing — and no entity either: `enabling` means a runtime dependency, so rigs are rows in `assumptions.toml` with `emulates` (§5.3). |
| Q7 | Does this ship downstream in v1? | **DECIDED in principle: yes**; schema migration deferred, gate optional (§10.4). |
| Q8 | Where do assumption rows live? | **DECIDED 2026-09-23 (owner accepted the revision; reopened by reviews 1, 2).** A dedicated `assumptions.toml`: in `external.toml` an assumption approval would re-bless drift in the LOCKED frame rows (§10.1). Internal assumptions: direction recorded, nothing built. |
| Q9 | Rename SR to SS? | **DECIDED: prose now, prefix later** — "prefix never" likely. |
| Q10 | Derive `frame`, or write it? | **DECIDED 2026-09-23 (owner accepted the revision; reopened by reviews 1, 2).** Nothing is written on a bundle; `coincident` is written where it holds; the rest is derived (§4). |
| Q11 | Where does an SR's need link come from? | **DECIDED 2026-09-23 (owner accepted the revision; reopened by review 1).** The SR keeps `sn_refs`; it adds `da_refs`; an assumption's needs are derived (§6.2). |
| Q12 | Where does a stakeholder live? | **DECIDED: a small list** in `stakeholder-needs.toml`, cited by needs (`stakeholder_refs`) (§6.2). |
| Q13 | Need-link edge cases | **DISSOLVED** by Q11's revision. |
| Q14 | Should assumption approval be human-held here? | **DECIDED: move the dial to DevStg-Boundary at the sitting** — with enforcement that does not exist yet (§10.2h). |
| Q15 | Does `external.toml`'s lock cover assumption rows? | **MOOT** under Q8's revision: they live elsewhere. |
| Q16 | Two frames in one view? | **DECIDED 2026-09-23** (owner: *"let's see how it looks"*; raised by reviews 1, 2). Kit and delivery frames; membership a `system` cell on the bundle; Transition the only lifecycle hand-off (§5.1). |
| Q17 | Boundary IFs approved at DevStg-Boundary? | **WITHDRAWN (review 2):** it put architecture before requirements. Interface allocation happens at DevStg-Arch instead (§9). |
| Q18 | One SR per interface — mint the missing IFs? | **DECIDED 2026-09-23** (owner confirmed the revision of reviews 2, 4): no `realizes` cell and no minting to a count — the IF → SR relation stays derived through the owner, as today; new IF rows only for genuine seams (§9). |
| Q19 | `mediates` on the session? | **DECIDED 2026-09-23** (raised by review 2). It only stops the reach check reading the session's crossings as not the human's; it changes no sign-off. Whether an assumption needs a person present is judged at its human-held approval, through `holds_when`; no attendance cell. Revisit if a DA is falsified by an unattended event. One cell lets an outcome on a session bundle count as the human's (§5.4). |
| Q20 | Activate the stage arms as a separate step? | **DECIDED 2026-09-23, amended, reconfirmed** (raised by review 2): the batch is reviewed with the arms off, and its approvals and the arm switch land in ONE commit, so no committed tree reads the regression (§11, C4). The owner first chose this on a miscount of two deselected steps; review 5 corrected it to three (`smoke`, `design-flows`, `trajectory`), and the owner reconfirmed. |
| Q21 | Key snapshot authorization by tier, not by file? | **SUPERSEDED by Q26** (review 5): review 4 showed re-keying the ledger is not enough, because approval identity is a path end to end (§10.1). |
| Q22 | Evidence as a current passing result, not a TC's existence? | **DECIDED 2026-09-23** (raised by review 3). LLM verdicts count only through the rig route (§8.3). Yes — tree-bound for automated assumption TCs, dated with a `max_age` for sampled and monitored ones (§7). |
| Q23 | Re-attest the approved SRs and TCs that C2 and C3 amend, before activation? | **DECIDED 2026-09-23, on condition it is documented**: each new cell's class recorded in `acceptance_record.py`'s classification table and mirrored in `registry-machinery-reference.md` §10 (revised by review 4). Only approved-content cells re-attest; link cells are traced, like `SN-Refs` and `Verifies` (§10.2k). |
| Q24 | How does sampled evidence count? | **DECIDED 2026-09-23** (raised by review 4). As falsification only, unless a declared sampling model justifies a positive claim, `holds_when` is narrowed, or the risk is accepted (§7). |
| Q25 | Where do sampled and monitored results live? | **DECIDED 2026-09-23** (raised by review 4). `max_age` is proposed by the TC's author, approved with the TC, and mechanically floored at 7 days; expiry reverts to `specified`, never `falsified`. In their own result record keyed by TC, not on the approved TC (§7, §10.2l). |
| Q26 | Tier-specific approval identity, or one tier per file? | **DECIDED 2026-09-23: neither — row-level refusal** (raised by review 4): a snapshot refresh refuses while any other row in the file has drifted approved text the act does not approve or re-attest (§10.1). |
| Q27 | Where does the gate sit? | **DECIDED 2026-09-23, on condition it is checked**: this repo enables C5 (raised by review 4). Split: maturity at DevStg-Boundary, evidence at DevStg-Release (§11, C5). |
| — | Orientation, the adopter, the reversed rulings | **DECIDED**; traced 2026-09-22 (§5.2). |
| — | Bundles | **DECIDED 2026-09-23** (owner confirmed the revision): authored identities; membership derived; not deleted (§5.7). |
| — | Hats | **Agreed, narrowed:** four positive outcomes; no "not applicable" record (§6.5). |
| — | Enabling-system stage vocabulary | Now Q30. |
| Q28 | Do hosted CI (spent `EXT-004`, `B-06`, `B-07`) and the vendored-doc upstream (spent `B-08`) return to the frame, under new ids? | **DECIDED 2026-09-23** (raised by review 5): hosted CI is drawn as an external party under new ids — outside design control is what makes it external, not a reason to leave it undrawn; the vendored upstream is not drawn until a repo vendors something (§5.6). |
| Q29 | Does `accepted_risk` carry an expiry or a re-review trigger, or is a recorded risk permanent until someone edits it? | **DECIDED 2026-09-23** (raised by review 5): it reopens on triggers — a failed sample, a change to a served need's text, or a change to the assumption's text; no clock (§7). |
| Q30 | Adopt 15288's enabling-system and 24748-1's stage vocabulary in the kit's prose (§8.1)? | **DECIDED 2026-09-23** (raised by review 5): "enabling system" is adopted for the delivery frame; the six life-cycle stage names are not, since the kit has its own DevStg ladder. |

### 12.2 Review round 1 — codex Sol, reasoning effort high (2026-09-23)

Verdict: *"REJECT AS WRITTEN."* 24 findings; each checked against the code; all
held.

| # | finding (short) | where it landed |
|---|---|---|
| 1 | one system-of-interest cannot both emit the Template and be the installed kit | §5.1 two frames |
| 2 | SRs at Reqs cannot cite IFs approved later at Arch | §9 (round 1's fix was itself wrong; see round 2) |
| 3 | the one-place need link gives wrong needs on multi-assumption IFs | §6.2 |
| 4 | nothing supplies the direction of an effect with no IF | §6.2 `effect_at` required |
| 5 | one `DA-ID` cannot have two homes | §10.1 one dedicated home |
| 6 | a need-level gate passes with unbridged paths | §11 C5, path-level |
| 7 | `Falsified` mixes validity into maturity | §6.2 `standing` |
| 8 | sharing a file does not wire a new tier into predicates or snapshots | §10.2b–c |
| 9 | one SR per interface: 69 SRs vs 39 IFs | §9 (revised in round 2) |
| 10 | deleting `B` rows leaves bundle-wide SRs without a subject | §5.7 |
| 11 | one scalar per bundle cannot aggregate mixed interfaces | §4 |
| 12 | "no DA means coincident" contradicts "absence asserts nothing" | §4 |
| 13 | a rig does not move an effect into design | §4, §8.2 |
| 14 | removing SR `sn_refs` touches 123 references in 54 files | §6.2 |
| 15 | an assumption-only `Verifies` breaks the trace forest | §7 |
| 16 | "no SR re-pointed" contradicted "dashboard SRs may move" | §5.1 |
| 17 | the scaffold rig had no valid `emulates` target | §8.3 |
| 18 | the dispatcher's off-spine approval hold is dormant | §10.2h |
| 19 | "all 194 TCs test the machine" ignored existing Critique and Inspection | §1 |
| 20 | writing assumptions is derivation, not transcription | §6.3 |
| 21 | `falsified_by` plus inbound TC links is two homes | §6.2 |
| 22 | a per-row "not applicable" hat ledger has no consumer | §6.5 |
| 23 | endpoint and tie-back counts were stale | §3 |
| 24 | Release is unrecorded, not unreachable | §10.5 |

### 12.3 Review round 2 — codex Sol, reasoning effort high (2026-09-23)

Verdict: *"REJECT AS WRITTEN. The revision moves the stage-ordering defect into
architecture-before-requirements and leaves the core gate satisfiable by
invalid, untested assumptions."* 18 findings; each checked against the code;
all held (finding 17 in weakened form — loop worker commits do carry `WI:`
trailers, but not validated and not on every loop commit). Round 2 is why the
proposal is now split into a core and an extension.

| # | finding (short) | where it landed |
|---|---|---|
| 1 | boundary IFs at Boundary approve architecture before requirements | §9: allocation at Arch; Q17 withdrawn |
| 2 | a Drafted DA waiting on an Arch IF deadlocks the stage | §9: the claim at Boundary, allocation at Arch |
| 3 | the gate passes on Drafted, falsified or unevidenced assumptions | §11 C5 |
| 4 | `external.toml` snapshots are path-keyed: a DA approval re-blesses frame drift | §10.1 dedicated registry |
| 5 | SR frame placement was judgment; SR-139 spans both frames | §5.1: derived, multi-frame is a finding |
| 6 | `class` is not frame membership; `enabling` means a runtime dependency | §5.1 `system` on bundles; §5.3 rig rows |
| 7 | the mockup's reach check ignored the stakeholder's party | §6.2 constraint on `effect_at`; §5.4 `mediates`; mockup fixed |
| 8 | the bundle scalar was recreated as effect/design | §4: no scalar |
| 9 | Transition is not the only cross-frame link | §5.1: typed links |
| 10 | assumption-only TCs are schema-invalid and lose phase and attribution | §7, §10.2e |
| 11 | the evidence descriptor had no home | §7 TC `sampling` |
| 12 | steps 2–3 were not warn-only: Drafted DAs regress the stage | §10.2c, §11 C4 |
| 13 | minting IFs means contract bodies, tests and approvals, or synthetic seams | §9: real seams, recorded waivers |
| 14 | the need–stakeholder relation had two homes | §6.2 `stakeholder_refs` on the need |
| 15 | the package-wide exception was indistinguishable from omission | §9 SR `form` |
| 16 | no approval brief for an assumption | §10.2g |
| 17 | the falsifier needs a loop provenance marker | §10.2i |
| 18 | adopter cost understated | §10.4 |

### 12.4 Review round 3 — codex Sol, reasoning effort high (2026-09-23)

A convergence round. Verdict: *"NOT YET SOUND — the core still mistakes an
authored test for passing evidence, while the extension and approval model
contain mechanisms that cannot represent or authorize the state they
describe."* It confirmed round 2's findings 1, 4, 5, 7–9, 11–12 and 14–17
resolved, and found five residual problems; each was checked and applied.

| # | finding (short) | where it landed |
|---|---|---|
| 1 | a TC's existence was counted as evidence; only a result is | §7 standing table; §11 C5 (Q22) |
| 2 | a single-valued `realizes` cannot express a shared seam | §9: a list, with a sharing waiver |
| 3 | `measured_at` added at Arch would mutate an approved Boundary row | §9: IF `bridged_by`, owned by the Arch approval |
| 4 | rig and stakeholder rows had no approval, and file-keyed snapshots coalesce tiers | §6.2 `status`; §10.1 tier-keyed ledger (Q21) |
| 5 | C2 and C3 amend approved SRs and TCs, which needs re-attestation | §10.2k; §11 C4 (Q23) |

Non-blocking notes also applied: multi-phase placement for assumption-only TCs
(§7); `da_refs` non-empty (§6.2); a party-bearing stakeholder for every need an
assumption serves (§6.2); and, in the mockup, a per-interface `bridged_by` and a
reach check that no longer takes a Cartesian product.

### 12.5 Review round 4 — codex Sol, reasoning effort high (2026-09-23)

Verdict: *"NOT YET SOUND — the core still lacks a coherent positive-evidence and
approval path, while the extension's allocation authority and full
re-attestation cost remain unresolved."* It confirmed the round-3 corrections
hold — the Arch-owned `bridged_by`, preserved `sn_refs`, re-attestation before
activation — and that the two-frame `system` cell, required `effect_at`,
`bridged_by` and the explicit unclassified state are internally coherent. Seven
findings; each checked against the code and applied. **These fixes were not put
through a fifth round.**

| # | finding (short) | where it landed |
|---|---|---|
| 1 | the gate accepted a passing sparse sample the plan says proves nothing | §7; §11 C5 (Q24) |
| 2 | rig and stakeholder statuses were unwired | §6.2 approval table; §11 C1, C4 |
| 3 | no carrier for sampled or monitored results | §7, §10.2l (Q25) |
| 4 | re-keying the ledger is not enough: approval identity is a path end to end | §10.1 (Q26) |
| 5 | `realizes` reverses the rule that an IF states no requirement | §9: use the derived relation |
| 6 | the re-attestation cost was incomplete — and link cells are traced, not approved | §10.2k (Q23 revised) |
| 7 | an evidence gate at an early rung would deadlock | §11 C5 split by rung (Q27) |

**Where the loop was stopped, and why.** The finding counts ran 24, 18, 5, 7. The
first two rounds found design flaws; the last two found implementation-level
specification gaps — which carrier, which parser, which rung. Those are the
sitting's and the implementation's to settle against real code, and a fifth
round would keep finding the next level of detail. The owner should read the
round-4 fixes as the proposal's current position, not as independently
verified.

### 12.6 Formerly "not captured" — closed or scheduled (owner, 2026-09-23)

1. **Blast radius → a field and a report.** One assumption covers every seam
   where the kit consumes model output (*"the model runner follows the runner
   contract"*). A provider changes its CLI's exit codes; the assumption is false,
   and every SR citing it loses part of its argument at once. With `standing =
   "falsified"`, a derived report lists the SRs and TCs that no longer prove
   their need.
2. **Chained assumptions → closed, no machinery.** A need's argument is the
   conjunction of every assumption on its paths; item 1's report walks the chain.
3. **Graded interpretation → closed by authoring rule (§6.4).**
4. **The trusted layer → closed by §6.3 and §6.5**, in proportion to risk.
5. **The authority assumption's falsifier → a finding, once loop provenance
   exists (§10.2i).** Prevention is partial: the dispatcher surfaces attestation
   and gate work on human-held *spine* tiers, but its off-spine hold is dormant.

**Standards, verified 2026-09-22.** The 15288:2023 definition (3.15), the stage
names (24748-1:2024) and the Transition process (6.4.10) were checked against the
standards' free previews and SEBoK.

### 12.7 Review round 5 — codex Sol, reasoning effort high (2026-09-23)

A decisions check, run after the owner's answers of the same day, across this
plan, the sister plan and the derived briefing. Verdict: *"OPEN POINTS REMAIN —
Q20 rests on false stage-selection facts, while several cross-plan dependencies
and conditional decisions still lack executable resolution paths."* 18 findings
(3 BLOCKER, 11 MAJOR, 4 MINOR), each checked against the code; all held. It
confirmed the day's other factual claims (the selection stage excludes drafts,
the reviewer's Done-when mapping, the test-impact ruling, the separate claim
commit, value-bound evidence, the traced/approved split's home). Those that
touch this plan:

| # | finding (short) | where it landed |
|---|---|---|
| 1 | §10.2c said any Drafted assumption regresses the stage; only a registry with no settled row does | §10.2c |
| 2 | C4 still described a visible regression, contradicting Q20's single commit | §11 C4 |
| 3 | a drop deselects three steps, not two: this repo's `smoke` step (`docs/stack.ini`) starts at DevStg-Tests; 34 steps in all | §11 C4, Q20 (reconfirm) |
| 4 | hosted CI and the vendored-doc upstream had no question | Q28, a C1 prerequisite |
| 5 | S6 and Q25 had no shared freshness model; the record held no judged state | §7 digest; C3 |
| 6 | the sister plan's S3 provenance cell was scheduled nowhere | §11 C1 |
| 7 | Q9's SR prose rename had no package | §11 T |
| 8 | Q25's `max_age` and its floor were missing from C3 | §10.2e, §11 C3 |
| 9 | Q27's condition had no activation step | §11 C5 |
| 10 | `accepted_risk`'s expiry had no question | Q29 |
| 11 | enabling-system vocabulary was "tentative" with no question | Q30 |
| 12 | Q21 still read as a small change, though Q26 superseded it | Q21 |

The sister plan's findings are in its §6.4; the briefing's were fixed there.

---

## Appendix — the conventional SRS, mapped

A cross-check against the usual outline of a System Requirements Specification.
The model covers every element; nothing here proposes a change.

| SRS element | where it lives in this model |
|---|---|
| Purpose, scope, definitions | the README's `PROJECT-VISION:` tag, each need's Scope, `PROCESS.md` |
| System context | the depth-0 view of the two frames (§5) |
| Major functions | needs and components |
| User characteristics | the stakeholder list (Q12) |
| Constraints | `performance-budgets.csv`, the dependency ledger, `stack.ini`, and hat-produced constraints (§6.5) |
| **Assumptions** | **the DA rows. Empty in the kit today: the gap §1 found.** |
| Functional / non-functional | implicit in how an SR originated |
| Interface requirements | IF rows; allocated to SRs at DevStg-Arch (§9) |
| Exclusions (no design detail) | the SR / LLR split, and SN-033's check that needs name no mechanism |

**Assumptions are a standard section.** IEEE 830-1998's prototype SRS outline
carries *"2.5 Assumptions and dependencies"* under *"Overall description"*;
ISO/IEC/IEEE 29148 (2011, revised 2018) keeps the item. Verified 2026-09-22.

**No functional / non-functional category.** SRs carry an optional `aspect`
(filled on 31 of 79, never gated), and the non-functional kind are what hats
produce as constraints.

---

## Appendix — sources

| # | Source | What it supplies |
|---|---|---|
| 1 | Zave & Jackson, *Four Dark Corners of Requirements Engineering*, ACM TOSEM 6(1), 1997 | R / S / W and the entailment `S ∧ W ⊨ R` |
| 2 | van Lamsweerde & Letier, *Handling Obstacles in Goal-Oriented RE*, IEEE TSE 26(10), 2000 | obstacle analysis as the W test-generator |
| 3 | Welsh, Sawyer & Bencomo, *Towards Requirements-Aware Systems* (REAssuRE), ASE 2011 | design-time assumptions as monitored **claims** |
| 4 | ANSI/UL 4600, *Evaluation of Autonomous Products* (Koopman) | Safety Performance Indicators — a falsifier bound to one claim |
| 5 | ISO 21448 (SOTIF) | **ODD restriction** as a sanctioned response |
| 6 | SAE J3016 | the ODD concept and term |
| 7 | NASA-STD-7009B, *Standard for Models and Simulations* | credibility proportional to decision risk |
| 8 | FAA AC 20-107B; CMH-17 Vol. 3 | the building-block pyramid as a **cost-allocation** rule |
| 9 | Chen, Cheung & Yiu, *Metamorphic Testing*, HKUST-CS98-01, 1998 | MRs as oracle-free necessary properties |
| 10 | Barr, Harman, McMinn, Shahbaz & Yoo, *The Oracle Problem in Software Testing*, IEEE TSE 41(5), 2015 | why validation is expensive |
| 11 | Faulkner, *Beyond the five-user assumption*, 2003; Schmettow, CACM 55(4), 2012 | the honest limit on sparse human sampling |
| 12 | ISO/IEC/IEEE 15288:2023 (3.15, 6.4.10); ISO/IEC/IEEE 24748-1:2024 | **enabling system**; the Transition process; life-cycle stages |
| 13 | Cobleigh, Giannakopoulou & Păsăreanu, *Learning Assumptions for Compositional Verification*, TACAS 2003 | an over-strong W is a defect |
| 14 | IEEE 830-1998 (superseded by ISO/IEC/IEEE 29148:2011, rev. 2018) | the SRS outline's "Assumptions and dependencies" section |
