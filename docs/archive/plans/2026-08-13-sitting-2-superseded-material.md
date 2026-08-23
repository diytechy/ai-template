> **ARCHIVE** — design history as of 2026-08-23; not current guidance.

# Sitting 2 — superseded & ruled material (archived 2026-08-13)

Moved out of
[`../../plans/2026-08-13-sitting-2-boundary-and-context.md`](../../plans/2026-08-13-sitting-2-boundary-and-context.md)
at the owner's direction (*"archive anything that has been ruled on to keep
this document clean"*, 2026-08-13m) once the 13k/13l rulings superseded it as
live decision surface. The rulings are in [`../../log.md`](../../log.md)
Decisions (2026-08-13e/f/k/l/m); the live frame is the brief's §1R. Nothing
here is an instruction.

## The drafted §1 frame and its analysis (superseded by §1R)

## 1. The depth-0 frame — what is OUTSIDE, what CROSSES

> **SUPERSEDED AS THE LIVE FRAME — kept as provenance.** The owner's
> 2026-08-13k reframe re-drew the system boundary (the repository is the
> system; the template is the deliverable) and decision 1 ruled its entities
> adopted. **The live frame is §1R below**, which re-attributes every row of
> this table and accounts for each one. Read this section for the original
> derivation and the carried draft analysis (§1a/§1b), not for the frame.

*Carried verbatim from the boundary draft §1, now archived at
[`../archive/plans/2026-08-13-devstg-boundary-draft.md`](2026-08-13-devstg-boundary-draft.md).*

**The system** = the kit: `project-trajectory/` scripts + hooks + templates,
verified by `tests/`, self-applied to this repo
([`../architecture.md`](../../runtime-flows.md), "Shape of the product").

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

| # | Entity | Dir | What crosses | IF today | State |
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

### 1a. What DEFINES a boundary — RULED 2026-08-13e

**What is ruled, and needs no re-decision:**

- A boundary is defined by **the actor AND the crossing interface** — not by the
  actor alone. Your reasoning is the load-bearing half and is recorded as ruled:
  naming the interface *technically starts implementation*, and that is accepted
  deliberately, **because it is the only way system requirements end up
  constrained to defined interfaces**. So the boundary declaration **encodes the
  first design decision: how the external parties interact with the system.**
- This is what makes decision 2.7(a) executable rather than aspirational. With
  the interface declared, an SR naming `check.py` is *citing the frame*; an SR
  naming `trace.py` is naming something the frame never admitted.
- **Ruled OUT as the frame's typing axis: `signal`.** The `discrete`/`variable`
  vocabulary stays a real and useful property **of an IF row** — it is what makes
  SN-037's *"incompatible signal types are mechanical findings"* checkable
  between two modules. It is not what types the *frame*, for a measured reason:
  over the 113 live rows, **106 are `variable` and 7 are `discrete`**; on a crude
  outward cut it is **15 `variable` to 2 `discrete`**, and **25 rows carry a
  `signal_note`** — the marker the WI-443 conversion left where it could not type
  the crossing cleanly. The cause is the absorbing rule visible on IF-020: any
  unbounded part makes the whole crossing `variable`. **A property that is 94 %
  one value over the set it is applied to is not typing that set.**

<!-- fig: cmd="python3 - … tomllib.load(interfaces.toml)['interface']; Counter over
r['signal'], split on outward = counterpart NOT startswith
('scripts/','docs/','project-trajectory/scripts','coverage'); signal_note = truthy
count", rev=768b6d3a -->

- **The correction that rode the ruling:** the rung's enforced predicate,
  `derive_gate.boundary_incomplete`, reads **`Stability` only** and never looks at
  `signal`. So "each crossing typed", *as mechanized today*, means only *"no
  declared crossing is still `Experimental`"*. An earlier session statement to
  the contrary was wrong.
- **Flagged for the kit's stack-agnostic reach, and NOT decided:** for a
  mechanical system the crossings are mounts and mating features, power rails,
  thermal paths, fluid and pneumatic connections, forces and torques, plus
  regulatory and environmental exposure. The actor-plus-interface rule travels
  there and arguably holds *harder*. What does **not** travel is
  `discrete`/`variable`, a software-signal vocabulary; a class axis (mechanical ·
  electrical · thermal · fluid · data) would. Recorded so the kit-level version of
  this rule is not written software-first by default.

**What stays OPEN — the field mechanics.** The ruling settles the *principle*,
not whether the registry grows fields to carry it. The typing the frame needs is
the **actor** (a real external party, never a file path), the **direction**
(present), the **contract** (present), and the **class of the crossing** — CLI
invocation, process exit status, file artifact, VCS event, network call,
human-read surface. That last axis genuinely discriminates at a frame and **has
no field today**. It is adjacent to the `external` flag `boundary_incomplete`
already admits nobody built. **Whether to mint one, both, or neither is decision
3 below.**

**The four rows the actor rule re-reads** are flagged in the table's State column
and are this sitting's to confirm: `IF-080`/`IF-081` (X-14/X-15) declare
`downstream adopter` but are the unattended station's *internal* serialization
seams, and X-08/X-12 name an in-repo path where an actor belongs. All four were
counted toward the registry's 15 "external" rows. **This is the case for making
the actor a declared thing rather than free text:** none of the four is *wrong* in
any way a check can currently see, because `counterpart` is prose.

**The data pack's six stated uncertainties (§1c) stand and are yours, not the
analyst's:** is `downstream adopter` one actor or three (team / tree / their CI)?
is git one crossing or three (read / write / hooks)? is the terminal an actor at
all? is the skills fan-out into a third-party agent's config namespace its own
crossing? is a `docs/knowledge/` pack an input? and `MULTI_REPO.md`'s cross-repo
rung was deliberately not audited.

**Three of those six carried a JUSTIFICATION the draft compressed away.** Rescued
verbatim from the data pack §1c
([`../archive/plans/2026-08-13-part-a-data-pack.md`](2026-08-13-part-a-data-pack.md)),
because each is the reason the analyst decided as they did and you are overruling
a reason, not a coin-flip:

> 3. **M-19 (terminal)** may be judged below the boundary — an output medium
>    rather than an actor. I included it because it is the only crossing that
>    explains a 32-copy behaviour.
> 4. **Skills fan-out** (`project-trajectory/skills` → `.claude/skills/` via
>    `bootstrap.py --agents`) crosses into an *agent harness's* config namespace.
>    IF-035 and IF-019 cover the index; the materialization into a third-party
>    agent's directory layout is arguably its own crossing. I did not add it.
> 5. **`docs/knowledge/` packs** arm the containment rule (§3e) from *presence*.
>    Whether a knowledge pack is an input crossing or an internal artifact is
>    undecided here.

**How the missing rows were proved missing** — the absence-verification method,
also rescued from the data pack §1b, because "MISSING" is a claim that needs
evidence and this is the only place it exists:

> Verified absent by literal search of `docs/requirements/interfaces.csv`:
> `dev-setup` → 0 hits, `workflow`/`codex`/`OpenAI`/`onboard` → 1 hit
> (`IF-064`, an unrelated `agent_session` row), `agent-resume` → 1 hit
> (`IF-068`, the `[agent-loop]` ini section, not the launcher),
> `PROJECT_STATE` → 1 hit (`IF-011`, the staleness contract to `check.py`, not
> the owner-facing surface).

<!-- fig: cmd="grep -icF '<token>' docs/requirements/interfaces.csv", rev=81a142c2 -->

### 1b. The operational CONTEXT is part of the boundary — RULED 2026-08-13f

**What is ruled:**

- **Modelling the operational context is part of defining the boundary**, not a
  later exercise. It is one step in determining **how this system lives in its
  surroundings**, and that question *"can sometimes only be well answered while
  knowing surrounding relationships."* So `DevStg-Boundary` declares the parties
  around the system and the relationships **among them**, not only the crossings
  into and out of it.
- **The cut is the DESIGN SCOPE, and everything else is external — including the
  enabling system.** The top-level division is not *actor versus other*; it is
  **inside the design scope versus outside it**. An enabling system — the
  development environment that produces the kit — is *not part of the system*
  even though tightly coupled to it, and it may not be an **actor** in the
  interaction sense at all. So the taxonomy has two levels: **external** is the
  boundary cut, and *operational actor · enabling system · interoperating system*
  are kinds of external entity beneath it. This is standard SE vocabulary the kit
  does not carry today (searched: `PROCESS.md`, `PROCESS_OPTIONS.md`), and
  adopting it dissolves the `dev-setup` paradox: **one OUT contract consumed by
  two different external entities** — an adopting contributor *operationally*,
  and this repo's own development environment *through self-adoption*.
- **The class sits on the ENTITY; the overlap is a RELATIONSHIP.** An earlier
  draft put the class on the *crossing* (E2 both ratifies and authors). Under the
  correction that is the wrong shape: the operational owner and the enabling
  development environment are **two distinct external entities that happen to
  share personnel**. Each entity carries exactly one class — the simpler schema —
  and the sharing becomes an **external-to-external relationship**, precisely the
  kind of surrounding relationship the ruling says the frame must model.
  Self-adoption stops being a schema special case.
- **`N-02` exists.** OI-28 declared only the OUT half (M-07, the artifact class
  leaving). The inbound authoring flow — a human + LLM session outside the
  mechanization writing the template and registry content the kit ships — was
  never given a crossing. It is now `N-02`.
- **E11 is a category error.** "The shipped template set as product" is an
  *artifact class*, not a party. Under the enabling/operational split it resolves
  into two crossings against real parties: **OUT to the adopting repo (E10)** and
  **IN from the enabling author (E12, `N-02`)**. Retire E11 as a party; keep it as
  what it is.

**The registry recommendation — PROPOSED, NOT RULED.** Your initial impression
was an `external.toml` carrying both external agents and external interfaces. The
recommendation is to **split by entity type, not by internal-versus-external**:

- **An EXTERNAL-ENTITY registry: YES — and your `external.toml` naming is better
  than "actors".** Under the design-scope correction the file holds external
  **entities**, of which an operational actor is one kind and an enabling system
  another; naming it for the cut keeps E12 from having to pretend to be an actor
  to get a row. It is precedented off-spine (`PART`, `ASSET`, `PB`, `REPO` — the
  last already models other repos as entities with `Type = owned|external|reused`)
  and it is the only place the context requirement can live, because
  **`interfaces.toml` structurally cannot hold external-to-external flows**: every
  IF row has `this_project` on one side by construction. "The author mints a
  template, the kit ships it, the adopter customizes it" is a chain with one link
  that never touches the kit.
- **A second INTERFACES registry: NO**, on your own **D-6** ruling (a duplicated
  **vocabulary** diverges silently) — LLR-166's rationale states the failure
  mode — plus **D-4** (ids never re-mean, so a crossing moving between internal
  and external becomes delete-and-mint rather than an edit, losing its history).
  Four consumers (`plan_briefs.IF_SURFACE_COLUMNS`, `check_trajectory`
  connectivity, `trace` integrity, `derive_gate`) would have to learn both files
  or silently read one.
- **So:** external entities (and the relationships among them) get a new home;
  every directed seam that *touches* the system stays in `interfaces.toml`, with
  `counterpart` becoming a **resolvable reference** — a declared external-entity
  id or an in-repo path. Boundary-ness becomes **derived**, which makes
  X-14/X-15's mislabel *unrepresentable* rather than merely visible.

**Why the registry earns it: the RENDERED VIEW — and why the prose variant is
WITHDRAWN.** An earlier draft offered a cheaper first move: park the entities and
the context as prose in `docs/architecture.md`, mint a registry later. **That is
withdrawn.** `docs/architecture.md` is **1,594 lines of which ~1,402 (88 %) are
GENERATED** — the AST-plus-`IF-###` dependency graph and the per-symbol module map
over ~60 scripts, both written by `gen_arch_map.py` and freshness-gated by
`--check`. Its hand-authored remainder is ~192 lines: the intro, *Shape of the
product*, and *Runtime flows*. So the file's **structural** content is already a
rendering target, and a hand-written frame would be the one piece of structure in
it that nothing generates. Second: `PROJECT_STATE.html`'s **"How (SW
architecture)"** tab already renders that module map, so registry data joins an
existing pipeline — registry → generated block → dashboard tab — while prose could
only join it by being parsed. **The split is by KIND, not by cost:** enumerable
structural data → registry → generated context view; the operational *narrative*
stays what *Runtime flows* already is (hand-authored, SR-cited, checked by
`check_flows.py`).

**The light tier for a simpler adopter — a single INPUTS / OUTPUTS pair.**
Recommended as the kit-level default, with one refinement: it must be **the same
schema with two rows**, never a different mechanism, so growing from light to
full is *adding rows* rather than migrating a file. And the part worth keeping:
**the derived check still bites at that tier** — if `counterpart` must resolve to
a declared entity *or* an in-repo path, an internal station seam cannot claim
`downstream adopter` when the only declared entities are INPUTS and OUTPUTS; it
has to name its path. X-14/X-15's defect is caught at the lightest tier the kit
offers.

**The cost, corrected in both directions.** *Lighter than first stated:* the
entity registry is **off-spine** — the `PART`/`ASSET`/`PB`/`REPO` tier — because it
exists to build the view, not to gate the spine; entity rows need no SR
back-refs, no gate arithmetic, an advisory schema tier, and a leftover example row
blocks nothing. *Heavier than first stated (your note, 2026-08-13):* **SRs are
still expected to resolve back to the boundary interfaces, and that IS a
spine-validation cost.** Measured:

- **IF → SR already exists and is clean.** `trace.interface_findings` makes an
  IF row with an empty or unknown `sr_refs` a `--strict` finding; **all 113 live
  rows link at least one valid SR**, the eleven declared frame crossings
  included (IF-013 → SR-006/007/008, IF-015 → SR-026/027/028/030, and so on).
- **SR → IF does NOT exist.** No check reads an SR's inputs and outputs and
  asks whether each references a declared interface. That direction is exactly
  **SN-037's ratified acceptance** (*"unresolved references, uncovered crossings
  and incompatible signal types are mechanical findings"*), and it is the real
  spine cost: a new checker, plus **WI-451's re-statement making the 57
  internal-naming SRs resolvable in the first place**. The registry is the cheap
  half; this is not.

---


## Decision 1 — the 13k reframe long-form and the original question

**The reframe that produced the entities — RULED IN SESSION, 2026-08-13k.** The drafted frame
does not match the owner's concept of where the system boundary sits, and the
owner re-drew it (the staged sequence exists precisely to catch this before the
SR re-statement runs). The ruling, in the owner's terms:

> **This repository IS the system. The template is NOT the system — it is what
> the system delivers.** Other repositories do not adopt this repository; they
> adopt the template it provides. The template files are the system's
> adopter-facing outputs — all of them. A **human or LLM session in a terminal
> — including the loop agent `agent-resume` launches — is ONE external
> entity**, which touches both the spine and the test scripts. The test
> scripts act on the spine content to validate it and feed back
> `open-items.html` and `PROJECT_STATE.html` to that session — outputs of the
> same scripts that are also packaged into the template. **The template is
> what the system delivers through development by the human/LLM entity, and
> it is validated by the same structure it builds.** The implementation
> closure this implies is accepted deliberately (the same grounds as the §1a
> ruling): the deliverable is known to be a template — a set of files and
> test scripts — and a different solution space would need a boundary
> incompatible with the entire structure that exists. Bounding the problem
> this way is the method.

**What the reframe does to the drafted entity roster — twelve become eight:**

| New entity | Class | Absorbs from the draft |
|---|---|---|
| **SESSION** — the development session: human or LLM in a terminal, attended or the unattended loop | `operational` | E2 (owner) + E3 (agent CLI) + E12 (enabling environment, **dissolved**) + E1's this-repo contributor rows (M-01/M-03/M-19). **N-02 dissolves** — authoring is the session's ordinary IN crossing through the hook floor (M-12/M-13). N-01, M-02, M-08…M-11 re-attribute here. |
| **ADOPTER** — the downstream team + their repo, receiving the template | `operational` | E1-downstream + E10. **M-07 stays the ONE deliverable crossing** (the template artifact class OUT; `test_dogfood_sync` its verification). |
| **MODEL PROVIDER** | `interoperating` | E4, unchanged (M-15) |
| **EXTERNAL REVIEWER CLI** | `interoperating` | E5, unchanged (M-14) |
| **GIT** | `interoperating` | E6, unchanged (X-09, M-16) |
| **HOSTED CI** | `interoperating` | E7, unchanged (M-04, M-05) |
| **OS · FILESYSTEM · PYTHON** | `interoperating` | E8, unchanged (M-17) |
| **TEST / COVERAGE TOOLCHAIN** | `interoperating` | E9, unchanged (M-18, X-13) |

**Recorded with the ruling, so it is not lost:** (a) at this repo's depth 0
**no entity is class `enabling`** — developing the template IS this
repository's operation; the class stays in the `external.toml` schema and
lands downstream, where **the delivered template is precisely an enabling
system from the ADOPTER's frame**. (b) Merging human and LLM into one SESSION
entity means the frame no longer expresses **who holds authority** — that
distinction survives as **policy and record** (`human_ratification_through`,
the log's Sittings table, decision 12's Human-column constraint), never as an
entity split; do not re-split the entity to get it back. (c) The owner's
"tooling acts as external entities" reads formally as: the tooling stays
**internal**, and self-adoption is the system consuming its own outputs
through internal seams — which is what lets rung 1 gate on genuinely external
crossings only (decision 4's direction). (d) The §2 port list and the 2.7(a)
discriminator survive unchanged — the ten port scripts are the template's
entry points plus the session's surfaces, so the 18/57 census and WI-451 do
not move. (e) The §1 table's 36 crossings survive as crossings; what changes
is their **entity attribution** per the Absorbs column above. **The sitting's
remaining act on this decision: confirm the re-derived table** (crossings
re-attributed to the eight entities, X-08/X-12/X-14/X-15 falling internal as
already flagged) **and the completeness declaration over it.**

The original question and context, for the record:

**The question.** Do the 36 crossings in §1's table, against the twelve external
entities E1…E12, constitute the kit's declared frame?

**Context.** Adopting also means adopting the **completeness declaration** — the
claim that this set is the whole frame — which is what the rung actually
certifies. The declaration is now known to be **complete-minus-two** (N-01, N-02
were added after it). Six uncertainties from the data pack §1c are yours to
settle (§1a above, with the three rescued justifications): is `downstream
adopter` one actor or three? is git one crossing or three? is the terminal an
actor at all? is the skills fan-out its own crossing? is a `docs/knowledge/` pack
an input? and `MULTI_REPO.md`'s cross-repo rung was deliberately not audited.

**Costs.** *Adopt:* the frame becomes the referent WI-451 slice 1 censuses
against — today that referent exists only in an analysis-input plan doc, which is
why slice 1 cannot honestly run without this. *Amend:* cheap now, and the only
moment it is cheap; every row added later re-opens the declaration. *Defer:* rung
1 cannot honestly close, and `DevStg-Boundary` holds the ladder down.

**Recommendation on record:** none for the six uncertainties — the draft states
explicitly they *"stand and are the ruler's, not mine."*


## Decision 3 — original question + the "declare the entities" proposal

The original question and the shape that anticipated this ruling, for the
record:

**The question.** §1a's actor-plus-interface rule is ruled and needs no
re-decision. What it leaves open is **whether the registry grows fields to carry
it**: an **`external`** flag (which `boundary_incomplete` already names as
missing, and which is what would let the rung check *completeness* rather than
*settledness*), a **crossing-class** axis (CLI · exit status · file artifact ·
VCS event · network · human-read surface), **both**, or **neither** — with the
frame's typing living in `docs/architecture.md` prose instead while
`interfaces.toml` carries only what it carries today.

**Costs.** *Mint:* an IF schema change with a downstream re-sync. *Do not mint:*
the rung's completeness half stays unmechanized and the frame is settled only by
eye. Note `signal` stays untouched either way — it is an IF-row property, not the
frame's.

**A third shape, proposed and not yet ruled: declare the ENTITIES, derive the
rest** *(drafted as "declare the actors" — §0.2b's vocabulary ruling renames
it)*. Make the external entities a closed set (E1…E12 as declared rows or a
vocabulary) and let *"is this a boundary crossing?"* be **derived** from whether
`counterpart` names one of them — instead of a hand-set flag that can drift out of
step with the contract beside it. It follows from §1a's ruling (if the frame is
entity **plus** interface, the entity is the half that should be declared) and it
is strictly stronger on the evidence in §1's table: the four re-read rows and the
six file-not-entity partials are all cases where `counterpart` says something
untrue and **nothing can catch it, because the field is prose**. Under a declared
vocabulary, an internal seam claiming `downstream adopter` becomes
*unrepresentable* rather than merely detectable — the repo's own governing
principle (`status.md`: *prefer a constraint that makes a bad state
unrepresentable over a check that detects it*). **Cost:** a closed vocabulary
every adopter must populate for their own frame, versus a boolean they can set
per row. **Note this shape is the same mechanism decision 5's `counterpart`-as-
resolvable-reference needs** — ruling one largely rules the other.


## Decision 4 — the five Experimental rows and the (dissolved) IF-103 tension

The original question and dispositions, for the record:

**The question.** Five of 113 IF rows carry `Stability = Experimental` and they
are what `derive_gate.boundary_incomplete` reads — they hold rung 1 down today.

| IF | Gist | Why still Experimental |
|---|---|---|
| **IF-057** | `plan_coverage` reads `interfaces.toml` + SR ids to resolve a dual-plan's per-WI cites | its consumer seam (`agent_loop`) was never declared — "WI-197's to declare" |
| **IF-103** | `migrate_carrier.py` — the CSV→TOML spine converter | *"Stability is PROVISIONAL on purpose: migration scaffolding with a defined end"* |
| **IF-118** | `gen_open_items` reads the decision registry through `spine_carrier` | minted by the batch-2 carrier sweep, never re-reviewed |
| **IF-119** | `agent_route` reads the model registry through `spine_carrier` | same sweep |
| **IF-120** | `trunk_step` asks the carrier which carrier of a registry is live | same sweep; was `Provisional` until WI-443 |

**The finding underneath.** **Four of the five are internal carrier seams, not
external crossings.** The rung that is supposed to certify *the system's frame* is
currently held down by module-to-module plumbing.

**Three dispositions:** promote to `Stable` (the carrier sweep has converged);
leave them and accept the rung stays down; or rule that **only
external-counterpart rows should gate rung 1** — which requires the `external`
field `boundary_incomplete` says nobody has built (decision 3).

**⚠ THE WI-452 TENSION — this is new and must be reconciled here.** The boundary
draft's §4 item 4 said IF-103 *"is deliberately provisional and should stay
Experimental until the conversion program ends."* But the ruled 2.3 rider says
the converter is **RESURFACED as the downstream-resync helper rather than spent
history** — a live row with a forward obligation. **A live helper's program does
not end.** So "until the conversion program ends" has **no terminus**, and IF-103
would hold `DevStg-Boundary` down indefinitely. The two cannot both stand. The
options, and none is on record as recommended:

- **Re-scope IF-103's stability semantics** — it stops being "provisional
  migration scaffolding" and becomes a stable adopter-facing conversion helper,
  promoted to `Stable`. Cost: the row's own `notes` cell states the provisional
  intent verbatim and must be re-written; it is a declared IF row, so this is a
  registry edit, not a spine re-attest.
- **Keep it `Experimental` and rule that only external-counterpart rows gate rung
  1** — which folds this into decision 3's `external` flag and makes IF-103's
  status irrelevant to the rung. Cost: the flag must be built first.
- **Keep it `Experimental` and accept rung 1 stays down.** Cost: `DevStg-Boundary`
  never clears, which makes the whole ladder a display that cannot move.


## Decision 5 — original three shapes, tiering, costs, riders

The riders (E11 retire, E12 admit, class-on-entity) and the `counterpart`
mechanics field-work remain with decision 3 and the execution rows. The
original question, for the record:

**The question.** §1b recommends but does not rule. Three shapes:

1. **An external-entity registry** (your `external.toml`, holding operational
   actors AND enabling systems under one cut) **plus a resolvable `counterpart`**
   in `interfaces.toml` — **RECOMMENDED**: derived boundary-ness, one home for
   seams, and the entity data feeds a *generated* context view into
   `docs/architecture.md` and the dashboard's existing "How (SW architecture)"
   tab.
2. **The same file also absorbing the external interfaces** — your first
   impression. **Rejected in §1b** on D-6 grounds (a duplicated vocabulary
   diverges silently; four consumers must learn both files) and D-4 (ids never
   re-mean, so reclassification becomes delete-and-mint).
3. **Prose in `docs/architecture.md` first, registry later** — offered in an
   earlier draft and now **WITHDRAWN** (§1b: that file's structural content is
   88 % generated, so a hand-written frame would be its lone exception, and prose
   cannot join the render pipeline).

**Tier it:** a single **INPUTS / OUTPUTS** entity pair is the kit-level light
default — same schema, two rows, so growth is additive and the derived check
still bites.

**Cost, both directions.** The entity registry is **off-spine** (view-building,
no SR back-refs, advisory schema) — but **SRs still resolve to the boundary
interfaces**, which is real spine cost: **IF→SR is enforced today and clean at
113/113**, while **SR→IF does not exist** and is SN-037's ratified obligation,
landing on WI-451 plus a new checker that nobody currently owns (§5.4).

**Riders on whichever shape wins:** retire **E11** as an entity (it is an artifact
class, §1b); admit **E12** (the enabling development environment — external,
tightly coupled, sharing personnel with E2/E3); and confirm that the
operational/enabling class sits on the **ENTITY**, with the personnel overlap
recorded as an external-to-external relationship.


## Decision 6 — original missing/partial counts

The original count, for the record:

**The question.** 13 of the pack's 34 have no IF row at all, plus both new rows
(N-01, N-02) — an honest missing count of **15** — and 6 more have a partial row
that names a file or module where the actor belongs.

**Context.** WI-442 (queued) owns OI-28's two seeds (M-07, M-12/M-13). The rest
have no owner, **including the two this draft added**: **N-01** (`docs/process.toml`
as the owner's dial surface) and **N-02** (the inbound template-authoring flow).

**Cost.** Ruling scope here decides whether rung 1 can honestly close at all. A
frame declared complete with 15 undeclared crossings is the failure OI-14 named:
*"SRs are blessed today against a frame nobody declared."*

## §1R v1 — the eight-entity / 31-BIF rebuild (superseded by v2 at the 2026-08-13n rulings)

## 1R. The REBUILT depth-0 frame — the adopted entities (RULED 2026-08-13l)

**This is the live frame** (the drafted §1 is archived — see the §1 stub above).
Decision 1 is ruled: *"Adopt the entities as currently described. Please rebuild
the boundary draft given these entities."* This is that rebuild — the 2026-08-13k
reframe's eight entities, the drafted crossings re-attributed to them, and the
registry shape decisions 3/4/5 settled around them. The sitting's confirmation
target is this section's tables and the completeness declaration at its end.

### 1R.1 The entities

| id (proposed) | Entity | Class | Description |
|---|---|---|---|
| **EXT-001** | **Development session** | `operational` | Human or LLM in a terminal — attended, or the unattended loop `agent-resume` launches. ONE entity: it touches both the spine and the test scripts. Who holds authority (human vs loop) is policy and record (`human_ratification_through`, the Sittings table), never an entity split. |
| **EXT-002** | **Adopter** | `operational` | The downstream team + their repository. Adopts **the template, never this repository**. |
| **EXT-003** | **Model provider API** | `interoperating` | Rate limits, auth expiry, model retirement behind any LLM session. |
| **EXT-004** | **External reviewer CLI** | `interoperating` | codex `sol`/`terra` — hostile-review briefs out, findings in. |
| **EXT-005** | **git** | `interoperating` | The mutation floor: commits, merges, pushes, advisory locks, the hook floor as enforcement. |
| **EXT-006** | **Hosted CI** | `interoperating` | GitHub Actions: push/PR/schedule triggers, the OS × Python matrix, job verdicts. |
| **EXT-007** | **OS · filesystem · Python ≥3.11** | `interoperating` | Path semantics, encoding, kernel advisory locks, interpreter presence. |
| **EXT-008** | **Test / coverage toolchain** | `interoperating` | pytest + coverage feeding the tier floors. |

No entity is class `enabling` at this depth — developing the template IS this
repository's operation; the delivered template is the enabling system in the
ADOPTER's own frame (2026-08-13k rider a).

### 1R.2 The boundary interfaces — 31 rows, re-attributed

One row per directed frame-level crossing; **`#` keeps the drafted-inventory id** (the archived table / data pack) so
every row traces to the WI-441 inventory. Dir is the system's point of view.
Proposed `BIF-###` ids mint at execution, in table order.

**EXT-001 Development session (13):**

| BIF | # | Dir | What crosses | IF today |
|---|---|---|---|---|
| BIF-001 | M-01 | IN | `dev-setup.{sh,cmd,command}` invocation; toolchain probe result back | — |
| BIF-002 | M-02 | IN | one-command autonomous-run trigger via root `agent-resume.*` | — |
| BIF-003 | M-12 | IN | instructions / prompt into a direct session | — |
| BIF-004 | N-01 | IN | `docs/process.toml` — the policy-dial surface the session hand-edits | — |
| BIF-005 | M-11 | IN | rulings, attestations and `Status` flips into the registries | — |
| BIF-006 | M-13 | IN* | artifact edits, admitted only through the git hook floor (*§1 listed OUT; re-read: the edits enter the system, the hook verdict is the return half*) | — |
| BIF-007 | M-10 | IN/OUT | `docs/status.md` — the resume-from-text surface the session also edits | IF-037 partial |
| BIF-008 | M-03 | OUT | the runnable capability list (`run_menu`) | IF-048 partial |
| BIF-009 | M-19 | OUT | every script's human-readable report to the terminal | — |
| BIF-010 | M-09 | OUT | `PROJECT_STATE.html` — validation feedback rendered to the session | — |
| BIF-011 | M-08 | OUT | `open-items.html` — decision-brief / signing surface | IF-074 partial |
| BIF-012 | X-07 | OUT | `subagent_gate.py` PreToolUse spawn allow/deny | IF-020 |
| BIF-013 | X-11 | IN/OUT | `agent_session.py` launches the session's CLI and reads its result | IF-041 |

**EXT-002 Adopter (9):**

| BIF | # | Dir | What crosses | IF today |
|---|---|---|---|---|
| BIF-014 | M-07 | OUT | **THE DELIVERABLE: the template artifact class** — `*.template.*` + `registries/*` (`test_dogfood_sync` its verification) | — |
| BIF-015 | M-06 | OUT | the MAPPING: templates → the adopter's `docs/` tree, + kit-version stamp | IF-014 partial |
| BIF-016 | X-01 | OUT | `check.py` gate/tier harness verdict | IF-013 |
| BIF-017 | X-02 | OUT | `bootstrap.py` scaffold write + re-sync diff | IF-014 |
| BIF-018 | X-03 | OUT | `agent_loop.py` unattended coordinator run | IF-015 |
| BIF-019 | X-04 | OUT | `check_vendored.py` drift verdict | IF-016 |
| BIF-020 | X-05 | OUT | `gen_cases.py` permutation expansion | IF-017 |
| BIF-021 | X-06 | OUT | `gen_release_checklist.py` checklist | IF-018 |
| BIF-022 | X-10 | IN | `check_vendored.py` reads the vendored upstream source | IF-036 |

*(BIF-016…021 are the delivered template's runtime contracts — the promises the
system's SRs form around, exercised in the adopter's hands. They are the reason
"the template is the deliverable" does not reduce the frame to one row.)*

**EXT-003…EXT-008 (9):**

| BIF | # | Entity | Dir | What crosses | IF today |
|---|---|---|---|---|---|
| BIF-023 | M-15 | EXT-003 | IN | rate limit, auth expiry, retired model (SR-026's backoff clause its only spine home) | — |
| BIF-024 | M-14 | EXT-004 | IN/OUT | hostile-review brief out, findings in | — |
| BIF-025 | X-09 | EXT-005 | IN | `check_privacy.py` reads staged/outgoing content | IF-032 |
| BIF-026 | M-16 | EXT-005 | IN/OUT | commits, merges, pushes, advisory locks, the hook floor as enforcement | IF-032 partial |
| BIF-027 | M-04 | EXT-006 | IN | push · PR · schedule trigger; the OS × Python matrix | — |
| BIF-028 | M-05 | EXT-006 | OUT | job verdict + step log | — |
| BIF-029 | M-17 | EXT-007 | IN | path semantics, encoding, kernel advisory lock, interpreter presence | — |
| BIF-030 | M-18 | EXT-008 | IN | pytest results feeding the tier floors | IF-070 partial |
| BIF-031 | X-13 | EXT-008 | IN | `check_coverage.py` reads `coverage.json` | IF-070 |

**Reconciliation.** 36 drafted rows − **N-02** (dissolved: authoring = BIF-003/006)
− **X-08, X-12, X-14, X-15** (internal under the entity rule, as the draft
already flagged) = **31 boundary interfaces**. Every §1 crossing is accounted for; none
was dropped silently.


### 1R.4 The completeness declaration (the sitting confirms this)

**Claim:** the 8 entities of §1R.1 and the 31 boundary interfaces of §1R.2 are
the WHOLE depth-0 frame of this repository-as-system. Complete to this
rebuild's best reading, with the residual uncertainties inherited from the data
pack §1c (the two the reframe resolved — one adopter, terminal-as-medium — are
closed): **is git one crossing or three** (BIF-025/026 split read/write/hooks)?
**is the skills fan-out into a third-party agent's config namespace its own
crossing?** **is a `docs/knowledge/` pack an input?** and `MULTI_REPO.md`'s
cross-repo rung stays deliberately unaudited.

## §5 Downhill impacts on the queued WIs (superseded 2026-08-13w — applied into the WI specs; parts predate the final frame)

## 5. Downhill impacts on the queued work items

Five specs sit in [`../work/queued/`](../../work/queued/), all dependency-ready
(every `needs` edge resolves to a complete WI). Each carries text this sitting's
rulings make stale. **Re-scope them in the ruling; do not let a builder discover
the staleness mid-slice.**

### 5.1 WI-390 — concurrency-v2 program close

[`../work/queued/WI-390-concurrency-v2-program-close.md`](../work/complete/WI-390-concurrency-v2-program-close.md)
· `safety_class = "spine"` · `buildtier = medium` · **no `priority` key** (worth
ruling if it is meant to sort last).

**What the spec says, and what changed:**

- **Stale status claims.** Its `## Context` (WI-414 re-scope) states
  *"`SR-055` — still requires 'two circular working loops' … still `Verified`."*
  **SR-055 is `Modified`; so is SR-050.** SR-093/124/131/132/133 are still
  `Verified`; LLR-051/056 and TC-051/056 still `Verified`. (Correction ledger #3.)
- **Its central premise now collides with two other windows.** The spec's own
  point is *"per §A4 all spine WIs admit together as ONE re-attest window and ONE
  owner sitting."* **Three windows now compete:** sitting 1's deliberately
  re-opened 2.4-sweep `Modified` window, WI-451's 57-SR re-statement window, and
  WI-390's own batch.
- **IF-080/IF-081 change meaning.** WI-390 treats them as connectivity drift
  (*"IF-055, IF-080 and IF-081 are in the registry with no script declaring
  them"*); §1 flags them **MISLABELLED**. Under a resolvable `counterpart`
  (decision 3/5) the mislabel becomes *unrepresentable*, which changes what
  "closing the drift" even means.
- **An unassigned prose home.** WI-390 owns the `PROCESS_OPTIONS.md` /
  `AGENTS.template.md` prose pass. The §1a actor-plus-interface rule and the
  "enabling system" vocabulary have **no process-doc home today** (searched:
  `PROCESS.md`, `PROCESS_OPTIONS.md`). Whether WI-390's pass absorbs them is
  unassigned.

**What this sitting should order.** Rule the **window sequencing** explicitly:
does WI-390's spine amendment ride WI-451's window, ride the 2.4-sweep window, or
open its own? Re-point its stale status list to "re-measure at claim, do not
quote". Say whether the boundary vocabulary lands in WI-390's prose pass or its
own row.

### 5.2 WI-442 — OI-28 seeds landed on the spine

[`../work/queued/WI-442-oi-28-seeds-landed-on-the-spine.md`](../work/complete/WI-442-oi-28-seeds-landed-on-the-spine.md)
· priority 2 · spine · `needs = ["WI-441"]` (complete) · `sr_refs = []`.
**This is the highest-impact staleness in the queue.**

- **Its vehicle has sailed.** The title says the two accidental "agent CLI" IF
  rows are regularized *"during part B's schema pass"*. **Part B is WI-443 and is
  COMPLETE.** The two rows are **IF-020** and **IF-041** (both declared under E3
  in §1). The clause needs a new home. (Correction ledger #4.)
- **E11's retirement doubles its SR clause.** Clause (b) — "one SR declaring the
  shipped template set a traced product artifact class" — now anchors **TWO
  crossings**: **OUT M-07** to the adopting repo (E10) and **IN N-02** from the
  enabling author (E12). WI-442's scope never contemplated an inbound crossing.
- **§1a raises the bar on clause (a).** An actor declaration *alone* is
  insufficient — a boundary is actor **AND** crossing interface. E3's **M-12** (IN,
  prompt into the repo) and **M-13** (OUT, edits through the hook floor) both lack
  IF rows, so clause (a) grows to **at least two typed IF rows**.
- **It is a coverage-relief vehicle and does not know it.** SN-037…SN-040 are
  ratified with zero `sr_refs` (`uncovered=8`). WI-442's SR could cite **SN-040**;
  neither WI-442 nor WI-451 declares which SN it covers.
- **Its home moves with decision 5.** If `external.toml` is minted, clause (a)'s
  declaration lands as an **entity row**, not an IF row. WI-442 assumes
  `interfaces.toml` is the only home.

**What this sitting should order.** Re-home the part-B clause; grow clause (a) to
typed IF rows for M-12 and M-13; state that clause (b) covers both M-07 and N-02;
declare the SN it covers; and re-point its registry home per decision 5.

**⚠ AMENDED BY THE 2026-08-13k REFRAME (decision 1).** Under the owner's
re-drawn frame the third bullet **simplifies**: E12 and **N-02 are dissolved**
— authoring is the SESSION entity's ordinary hook-floor crossing, i.e. exactly
M-12/M-13 — so clause (b)'s SR anchors **M-07 alone** (the ONE deliverable
crossing to the ADOPTER), and the "inbound half" WI-442 never contemplated
turns out not to exist as a separate crossing. Clause (a)'s "boundary-actor
declaration" lands as the **SESSION entity row** in `external.toml` (decision
5) plus the M-12/M-13 IF rows. The rest of the order stands.

### 5.3 WI-448 — common-module inversion program (OI-16 / D-8)

[`../work/queued/WI-448-common-module-inversion.md`](../../work/active/wi448-common-module/WI-448-common-module-inversion.md)
· priority 3 · `buildtier = strong` · spine · `needs = ["WI-441", "~WI-447"]`
(both complete).

- **Its basis is provisional.** The spec says *"Sequenced after OI-14 part A
  (component ownership turns import doctrine into a lookup)."* Part A shipped —
  but **P5 is only provisionally adopted warn-first** (CMP-006…009 all
  `state = planned`; decision 10 is unruled). If you overturn P5, **P3 is the named
  fallback** and the lookup basis changes. The pack's "overturn costs nothing
  else" costing **did not account for WI-448 consuming the component tags as
  doctrine.**
- **The must-land-together coupling is stated in the pack, not in the spec.**
  Decision 10's constraint finding says *"P2's measurement is the proof the two
  must land together"* — extraction without deletion makes every number worse.
  WI-448's spec says only *"sequenced after"*. **Reconcile:** "sequenced after" and
  "must land together" are different obligations.
- **MAPPING is a declared boundary crossing.** The spec's whole downstream risk
  surface is *"the module joins MAPPING (the single line that is the whole
  downstream risk surface, and the line the repo has got wrong once)"*. MAPPING is
  now **M-06 (IF-014, partial)** — a crossing to E10. Whether adding a module to a
  declared crossing obliges an **IF-row update** is unruled.

**What this sitting should order.** Rule decision 10 first (it gates this row's
premise); state whether WI-448 and the partition land together or merely in
order; and rule whether a MAPPING addition is an IF-row edit.

### 5.4 WI-451 — SR-tier boundary conformance pass

[`../work/queued/WI-451-sr-boundary-conformance-pass.md`](../work/partial/WI-451-sr-boundary-conformance-pass.md)
· priority 2 · `buildtier = strong` · spine · `needs = []`. **The central row this
sitting unblocks — and its central numbers are superseded.**

- **The split is 18/57, not ~25/~50.** Its title's estimate is wrong in the
  direction that **moves the program up**. Restate it. (Correction ledger #1, §2.)
- **The gate is restated.** Its guard says *"Do not begin slice 2 without the
  sitting's ruling"* — but **2.7(a) IS already ruled**. What remains gated is the
  **boundary-inventory agreement** (decisions 1 + 2), not the discriminator. Say so,
  or a builder reads the guard as unsatisfied forever.
- **Slice 1 has no referent yet.** The census is *"against the boundary
  inventory"*, and no authoritative artifact holds one — the 34-crossing inventory
  lives only in an analysis-input plan doc whose own header says *"analysis input,
  not a decision."* **Adopting the frame at this sitting creates the referent.**
- **The SR→IF checker is an UNOWNED deliverable.** IF→SR is enforced today and
  clean at 113/113; **SR→IF does not exist**, and it is SN-037's ratified
  acceptance. WI-451 names the mechanization but **assigns no build**. Either give
  it to WI-451 explicitly or mint a row.
- **It needs the duplication rule as an input.** Decision 7's rule is applied
  **per row** in slice 2, and WI-451's spec contains no duplication rule at all.
- **It is the coverage-relief vehicle.** WI-451's output is SN-033…SN-040's first
  coverage; its spec says nothing about SN coverage. `uncovered=8` bites at
  `trace.py --strict` from **DevBar-Tests** on.
- **Its "internal seam" definition is pinned to unruled tags.** It reads internal
  against CMP-006…009 (P5), which decision 10 has not ratified.
- **Area→aspect rides here or nowhere.** The conversion is *"queued for the next
  SR-registry touch"* — **WI-451 slice 2 IS that touch**, and WI-451 never mentions
  `Area`. Decide whether it rides.

### 5.5 WI-452 — LLR-165 resync-helper resurface

[`../work/queued/WI-452-llr-165-resync-helper.md`](../work/complete/WI-452-llr-165-resync-helper.md)
· priority 3 · medium · `safety_class = ordinary` · workstream `docs` ·
`sr_refs = ["SR-147"]` — the only queued row carrying an SR ref.

- **Part (1) is real work, not a verification no-op — measured.**
  `project-trajectory/RESYNC_PACK.md` **HAS** the pointer (8 mentions of
  `migrate_carrier.py`, with runnable commands). **`ADOPTING.md` §6 has ZERO
  mentions. `project-trajectory/skills/downstream-resync/SKILL.md` has ZERO.** Two
  of the three named surfaces are empty.
- **The TC-159 lift gap.** Pack §2.3 lifted SR-147 / LLR-165 / **TC-160** — never
  **TC-159**, which is the TC that actually verifies LLR-165. Live: TC-159 `Draft`
  (verifies SR-147 + LLR-165); LLR-165 `Planned` with `test_refs = TC-159`. WI-452
  part (2) says *"confirm … that TC-159/TC-160 still exercise the path"* — it will
  walk straight into a `Draft` row. **Lift it or re-point it deliberately**
  (sitting 3 §2). (Correction ledger #8.)
- **The IF-103 tension.** Decision 4 above. WI-452's ruled thesis (the converter
  has a forward obligation) contradicts the draft's "Experimental until the
  conversion program ends."
- **A possible fourth surface.** If `external.toml` is minted (decision 5), the
  resync pack gains an entry and **WI-452 part (1)'s surface list grows**.

---

