> **ARCHIVE** — design history as of 2026-08-16; not current guidance.

# The interface model — PROPOSAL, NOT RULED

**Status: a scratchboard.** Nothing here is decided, nothing here has been
executed, and no registry row has moved because of it. Raised by the owner
2026-08-15 while reading `interfaces.toml` and finding it hard to read. Written
down so the reasoning survives the conversation.

**The complaint that started it, in the owner's words:** an interface row lists
`this_project`, `counterpart`, `direction` and `sr_refs`, *"none of which tell
you who is serving the interface without looking at more details."*

---

## 1. The measured finding that motivates it

Run before any proposal, read-only, against the live registry:

- `direction` is not `in`/`out` — it is **`Provides` (41) / `Consumes` (74)**.
  The registry is already provider/consumer shaped.
- Grouping rows into (provider, consumer) seams: **115 distinct seams, and
  zero with more than one provider.** The "no more than one provider" half of
  the proposed invariant is already clean.
- **74 of 115 seams are consumed with no declared provider.** Splitting by
  what sits on the far end:

| Far end of the consumed thing | Count | Reading |
|---|---|---|
| A file or doc (`docs/stack.ini`, a registry file) | 32 | Legitimate. A file cannot declare that it provides; this needs a source/sink concept. |
| **A script that never declares it provides anything** | **42** | The real gap. |

Concentration matters more than the total: **`spine_carrier` is consumed by 14
modules and declares no output at all**; `trace` and `check_trajectory` are
consumed by 5 each. The modules most depended upon are precisely the ones with
no declared outputs.
<!-- fig: derived="grouping docs/requirements/interfaces.toml rows by (this_project, counterpart) normalised to (provider, consumer); Provides rows give the provider set, Consumes rows the consumer set; the gap is the set difference" -->

**This audit is not only diagnostics — it is the migration's work list.** Under
the proposed model those 74 rows stop being rows and become entries in a
`serves` list; but 42 of them have no provider row to fold into, so those must
be minted first.

## 2. The proposed model

Three rules:

1. An **interface** declares only what it is and where it goes: its contract,
   its signal, and `serves = [...]` — the consumers, each either a design block
   or a boundary crossing (`B-05`). Nothing about endpoints.
2. A **system requirement** declares `provides = [IF-...]` — the interfaces it
   is answerable for. This **replaces** `IF.sr_refs`; it does not join it. (The
   author's first reaction — that this duplicates the link — was wrong: it is a
   move, not an addition.)
3. Provider identity and direction are **derived, never authored**: the
   providing modules are the requirement's low-level rows' modules, and flow is
   "from the provider toward everything in `serves`".

**The invariant:** every interface is named in exactly one requirement's
`provides` — no more (ambiguous ownership), no less (an output nobody is
answerable for). Every id in `serves` resolves. An interface nobody serves is a
dead row.

**What this deletes:** `this_project`, `counterpart`, `direction` (115 cells
each) and `interface_from_external`/`interface_to_external` (8) — a boundary
crossing simply becomes another entry in `serves`. Four authored fields become
two; roughly 460 hand-maintained cells become about 180.

**A second win, unremarked at the time:** `SR-Refs` currently names *two
different relationships* depending on tier — a low-level row's parent
requirement, and an interface's requirements. Renaming the interface side stops
one column meaning two things, which is a real part of why the file reads badly.

## 3. Physical interfaces — the owner's challenge, and why it is not an edge case

The owner's question: interfaces between **physical** components. *"The physical
orientation still needs to be oriented and owned from some parent."*

**That instinct matches the ruled method exactly.** The component partition was
ruled to be N2/DSM decomposition *literally rather than by analogy*
(`docs/knowledge/system-decomposition-methods.md`). In an N2 chart, direction is
encoded by **position in the matrix** — feed-forward above the diagonal,
feedback below — and the matrix belongs to the **containing block**. So
"orientation owned from a parent" is not an accommodation for physical
interfaces; it is the N2 convention, and it is what the repo already committed
to.

**Where provider/consumer breaks down.** Information flows have a natural
provider. A mated connector, a bolted joint or a thermal path is a *mutual
constraint*: both sides are real design obligations and neither "provides" the
other. Classic practice gives such an interface a **custodian** — the common
parent that owns the control document — while each side carries derived
requirements against it.

**The proposed reconciliation, and it is the owner's own suggestion applied**
(*"the elements could just change semantics, because there would be different
rules involved"*): generalise the field from **provider** to **owner**.

- For an information flow, the owner is the provider. The rule is
  provides → serves, exactly as §2 states.
- For a physical/mutual interface, the owner is the **common parent
  component**, and both sides declare against it. Same field, same "exactly one
  owner" check; the rule for *who qualifies* differs by interface kind.

This keeps one invariant and one mechanical check across both, which is the
property worth protecting.

**Two facts the knowledge doc already records, and they cut both ways:**

- Physical components are explicitly listed as a **non-structural constraint**
  that "can override a lower-cost cut for reasons outside the matrix" — so the
  method already concedes the matrix does not capture everything physical.
- **Signal granularity** — whether "one signal" is a whole interface row or one
  field within it — is called "a modeling choice made before the matrix exists,
  not something the algorithm derives." That choice is unmade, and it decides
  how many rows this model produces.

## 4. THE EVIDENCE THAT SHOULD BE READ BEFORE ANY OF THIS IS RULED

`open-items.toml` OI-14 records that **Core (the Gilbert/Adamah robot) is a real
MIXED software-plus-physical adopter of this kit** — stamped `767487c`
2026-07-06, at `DevBar-Release`, 37 SN / 31 SR / 63 LLR / 70 TC — and that it
carries a **283-line whiteboard titled "AI-Template Fit and Hardware
Traceability", written expressly to test whether this kit fits hardware**, plus
a ratified glossary.

The open item's own words: *"It is the strongest evidence available for part A
and it should be read before the partition is ruled."*

**It has not been read into this question.** Designing a physical-interface
model from first principles while a hardware adopter's own fit assessment sits
unread would be inventing an answer that already exists in evidence form. This
is the single highest-value input available and it costs a read.

## 5. Relationship to what is already ruled

This is **not a new program**. OI-14 is `ruled`, and its **Part B is literally
"what an interface row must say"** — so this proposal is an *amendment to a
ruled item*, not a fresh design, and it must be raised as one.

- **D-3** already owns shedding `direction`/`counterpart` across the 115 rows
  with roughly 85 consumption-shaped re-authorings, and sits unexecuted on the
  architecture-retirement lane. This proposal does that *and* inverts the
  requirement link. **Re-scope D-3 to be this** rather than run two programs
  against the same 115 rows on two lanes.
- **A coupling that must not be missed:** D-3 sheds `direction`, but the §1
  audit *depends* on `direction` to know which end provides. If that field goes
  before the provider concept lands, the check loses its input. They have to be
  designed together.
- OI-14 also records that `cross_component_findings` is **deliberately vacuous**
  for any endpoint carrying no component tag — **46 of 113 rows** — so
  `component-findings=0` honestly means "no findings among the 67 classifiable
  rows". That coverage gap is the same shape as the 74 above and should be
  resolved by the same act.

## 6. Sequencing, and the reason for it

1. **Now, zero risk:** produce the full 74-row audit table, each row classified
   file-source / script-source-needing-a-provider / covered. Read-only, touches
   no lane, and it is the input the schema change needs anyway.
2. **Read the hardware adopter's whiteboard** (§4) before ruling the physical
   semantics.
3. **Mint the missing provider rows** the audit names — 42 of them — because the
   inversion has nowhere to put those consumers otherwise.
4. **Then** invert the schema, folded into D-3, and **after the current
   re-tier lane merges**: it rewrites the same requirement rows the ratification
   wave is about to sign, and signing rows about to gain a `provides` field
   means signing twice.

**Severity when it lands: warn-first, with the count visible.** There is a
measured finding on record that one-home-per-behaviour is unsatisfiable against
the current tree — 12 duplicated behaviours across 39 (behaviour, home) pairs in
16 modules — and a separate program owns deleting those copies. A gating check
would be red on day one against a backlog it does not own.

## 7. Open questions this proposal does NOT answer

1. Is the owner of an interface a **requirement** or a **module**? Written here
   as the requirement (which makes ownership unforgeable), but 32 of the gaps
   are *files* answerable to no requirement — those need the source/sink concept.
2. **Bidirectional seams.** Recommendation: two interfaces, one per direction.
   Today zero rows claim bidirectionality, so nothing is lost by disallowing it,
   and allowing it reintroduces the ambiguity the model exists to remove. The
   owner flagged this as possibly infeasible for complex interfaces — unresolved.
3. **Signal granularity** (§3) — one row per contract, or per field/flag/exit
   code? Unmade, and it decides the row count.
4. Does the physical/mutual case get its own **interface kind**, or is it a
   convention on the existing rows?
