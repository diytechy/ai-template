# Sitting 2 — the boundary, the operational context, and the structural rulings

**Status: DRAFT FOR RULING.** Assembled 2026-08-13 from the two carriers that
preceded it — the sitting pack
([`../archive/plans/2026-08-13-sitting-pack.md`](../archive/plans/2026-08-13-sitting-pack.md))
and the DevStg-Boundary draft
([`../archive/plans/2026-08-13-devstg-boundary-draft.md`](../archive/plans/2026-08-13-devstg-boundary-draft.md))
— after **sitting 1** ruled pack §2.2–2.7 ([`../log.md`](../log.md) Decisions
**2026-08-13d**) and you then ruled the two boundary halves in session
(**2026-08-13e**, what defines a boundary; **2026-08-13f**, the operational
context). Both carriers move to `../archive/plans/` with this document; every
pointer below already names them at their archive path so nothing dangles.

**The two-sitting split, and why.** Sitting 1 deliberately closed the *needs*
foundation and left the SR tier open, because the boundary ruling reshapes it.
What is left divides cleanly into a **frame-and-structure** sitting and a
**verification** sitting, and they cannot be run in one pass because the second's
subject is the *output* of the first:

- **THIS sitting (2) rules the frame and the structure.** The depth-0 boundary,
  the port list and its discriminator, where the external entities and the
  context live, the tabled one-obligation-per-row call, the P5 partition, the
  hats roster, and the sequencing of three colliding re-attest windows. It rules;
  it does not sign a spine.
- **Sitting 3 verifies the adapted spine** —
  [`2026-08-13-sitting-3-spine-verification.md`](2026-08-13-sitting-3-spine-verification.md),
  the sibling file in this directory. It runs *after* this sitting's rulings are
  executed, and its subject is whether the re-stated system requirements are
  functional and the windows close honestly.

**This document IS the decision surface.**
[`../requirements/open-items.toml`](../requirements/open-items.toml) holds exactly
one `pending` row and it is the `OI-000` example placeholder — 19 of 20 rows are
ruled. Nothing mechanized projects this sitting onto `open-items.html`. So unless
you want new OI rows minted first, the durable record of what you rule here is
**an entry appended to [`../log.md`](../log.md)'s `## Decisions log`**, and this
file is the brief you rule from.

---

## 0. Already ruled — do not re-litigate

### 0.1 The sitting-pack decisions, dispositioned

| Pack item | Outcome | Where it is recorded |
|---|---|---|
| **§2.1** six one-obligation-per-row form findings | **TABLED to this sitting** — splitting mints ids into SR text the retier may shuffle, so it waits for the boundary re-statement | `../log.md` 2026-08-13d; carried below as **decision 9** |
| **§2.2** SR-082 drain-dial confirm | **YES** — "the separate drain dial" IS `keep_nondependent`; the §E.1 replacement applied verbatim | `../log.md` 2026-08-13d |
| **§2.3** three Draft lifts (SR-147 / LLR-165 / TC-160) | **YES, with a rider** — LLR-165's converter RESURFACED as the downstream-resync helper rather than spent history; WI-452 minted | `../log.md` 2026-08-13d |
| **§2.4** rationale-citation keep-or-sweep | **SWEEP**, overriding the pack's *keep* recommendation — the 29 SR rationale cells shed the retired SN-013…SN-022 tokens, each parenthetical's content kept as "the dissolved edge expectation that …"; the SR-021/SR-026 in-cell fold annotations stay verbatim. Swept rows flip/stay `Modified` — **a deliberately re-opened window, this sitting's to close** | `../log.md` 2026-08-13d |
| **§2.5** WI-419 chain-flip scoping | **CONFIRMED** — narrow scoping stands, the wide precedent is not extended | `../log.md` 2026-08-13d |
| **§2.6** four `gate policy` stale-text verdicts | **YES** — four cells re-worded onto the declared ratification level + `session_hold`; SR-085 and SR-108 flip `Modified`, SR-125 re-titled only | `../log.md` 2026-08-13d |
| **§2.7** SR-implementation-naming discriminator | **(a) RULED** — an SR may name an artifact only where it is a DECLARED BOUNDARY CROSSING. **Its EXECUTION is gated on this sitting**: the boundary must be agreed before the pass runs, so WI-451 slice 2 stays held | `../log.md` 2026-08-13d |
| **§3** P5 partition acceptance · **§4** hats roster | **NOT ruled** — explicitly deferred to this sitting, "which the owner expects to carry significant SR churn and possible retiering" | `../log.md` 2026-08-13d; carried below as **decisions 10 and 11** |

### 0.2 The two boundary rulings

- **2026-08-13e — a boundary is the actor AND the crossing interface.** Naming
  the interface *technically starts implementation*, and that is accepted
  deliberately, **because it is the only way system requirements end up
  constrained to defined interfaces**. **Ruled OUT as the frame's typing axis:
  `signal`.** Full summary and the measured basis: §1a below.
- **2026-08-13f — the operational CONTEXT is part of the boundary definition.**
  `DevStg-Boundary` declares the parties around the system and the relationships
  **among them**, not only the crossings into and out of it. The cut is the
  DESIGN SCOPE; the class sits on the ENTITY; E11 is a category error; N-02 is a
  real new crossing; the external-entity registry is **recommended and NOT
  RULED**. Full summary: §1b below.

### 0.2b Vocabulary — RULED 2026-08-13j (owner): the noun is ENTITY, never "actor"

The going-forward semantic for the parties around the system is **entity**. The
noun lives on the registry table (`[entity.EXT-###]`), so the class values
carry none: **`operational` · `enabling` · `interoperating`**. Sections of this
document carried verbatim from the archived draft (§1, §1a, §1b) and quoted
rulings keep their original words as provenance — read **"actor"** there as
*operational entity*, and the §1 table's **"Party"** column header as *entity*.
Everything written from here on — kit-facing schema, process prose, the
`external.toml` field vocabulary — uses entity vocabulary. ("Entity" is also
the standard context-diagram term — *external entity* — and coheres with the
IF registry's `counterpart` field; "stakeholder" was passed over because it
already names the SN tier's subject.)

### 0.3 CORRECTION LEDGER — eight cross-document corrections this document carries

Every one of these is a place where a still-live artifact states something that
measurement has since falsified. They are corrected *here* rather than silently;
where a conclusion survives its broken reason, that is said too.

| # | Stale claim, and where it lives | Verified fact (2026-08-13) |
|---|---|---|
| 1 | **WI-451's title**: "~25 plausibly naming the boundary port itself … ~50 naming internal modules" | **SUPERSEDED: 18 SRs name only ports, 57 name at least one internal module** (draft §2, carried at §2 below). The delta is definitional and moves the program **up**. |
| 2 | **Boundary draft §3's flag**: "SR-035 … it is `Modified`, so touching it costs a re-attest" | **SR-035 is live at `Verified`.** The *bundling* conclusion survives — touching a `Verified` row **flips it `Modified` and opens a window either way** — but the stated reason is false. |
| 3 | **WI-390's body** (`## Context`, WI-414 re-scope): "SR-055 — still requires 'two circular working loops' … still `Verified`" | **SR-055 is `Modified`. So is SR-050.** SR-093/124/131/132/133 are still `Verified`; LLR-051/056 and TC-051/056 still `Verified`. Do not re-quote WI-390's list without re-measuring. |
| 4 | **WI-442's title**: "regularize the two accidental 'agent CLI' IF rows … **during part B's schema pass**" | **Part B is WI-443 and is COMPLETE.** The sub-clause's vehicle has sailed; the two rows are **IF-020** and **IF-041**. It needs re-homing (§5.2). |
| 5 | **Pack §5's basis block** (`drafts=51 modified=64 uncovered=0 phase=4 stage=DevStg-Needs stage-ord=0`) | Superseded by the live [`../gate`](../gate) — the current basis is quoted verbatim at §0.4. |
| 6 | **Boundary draft §0**: "No new registry was ever proposed" | True **as history** — nothing ever was. Amended by the draft's own §1b and §4 item 5: **whether an external-entity registry is minted is now open** (decision 5). |
| 7 | **Boundary draft §4 item 4**: IF-103 "should stay Experimental until the conversion program ends" | **Direct tension with the ruled 2.3 rider**, which makes `migrate_carrier.py` a **live resync helper** — so the conversion program has **no terminus**, and IF-103 would hold `DevStg-Boundary` down indefinitely. This sitting must reconcile (decision 4). |
| 8 | **Pack §2.3**: lifted SR-147 / LLR-165 / **TC-160** | It never lifted **TC-159** — the TC that actually verifies LLR-165. Live: **TC-159 `Draft`** (verifies SR-147 + LLR-165); TC-160 `Planned` (verifies SR-147 + LLR-166); LLR-165 `Planned` with `test_refs = TC-159`; LLR-166 `Draft`. **The 2.3 execution left the chain internally inconsistent** — owed at sitting 3 §2. |

### 0.4 The current basis line — verbatim from [`../gate`](../gate)

```
# basis: SN=27 SR=148 LLR=151 TC=148 drafts=27 modified=51 uncovered=8 computed=DevBar-Below ex-draft=DevBar-Below phase=5 per-phase=1=DevBar-Tests;2=DevBar-Tests;3=DevBar-Tests;4=DevBar-Below;5=DevBar-Below stage=DevStg-Boundary stage-ord=1 stage-of=8
# computed 2026-08-13 (as-of 94408245)
DevBar-Reqs
```

Read it honestly: the value is the bar that must next be **CLEARED**, the MIN
over every in-scope row's own bar floored to `DevBar-Reqs`. `drafts=27` is
LLR 14 + TC 13; `modified=51` is SR 30 + LLR 14 + TC 7; both reconcile exactly.
`uncovered=8` is new since sitting 1 and is exactly SN-033…SN-040 — ratified
needs with zero SR children. The stage is `DevStg-Boundary`, rung 1 of 8, which
is what this sitting exists to clear.

---

## 1. The depth-0 frame — what is OUTSIDE, what CROSSES

*Carried verbatim from the boundary draft §1, now archived at
[`../archive/plans/2026-08-13-devstg-boundary-draft.md`](../archive/plans/2026-08-13-devstg-boundary-draft.md).*

**The system** = the kit: `project-trajectory/` scripts + hooks + templates,
verified by `tests/`, self-applied to this repo
([`../architecture.md`](../architecture.md), "Shape of the product").

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
([`../archive/plans/2026-08-13-part-a-data-pack.md`](../archive/plans/2026-08-13-part-a-data-pack.md)),
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

## 2. The port set and the discriminator — what WI-451 executes against

*Carried in full from the boundary draft §2, now archived.*

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
provisionally adopted warn-first — decision 10). Under the recursion these
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

*Carried in full from the boundary draft §3, now archived — with correction 2
applied inline.*

**Your concern, verbatim:** *"If a system requirement is defined at the
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
that adds **nothing** over its SN. *(Live, for the record, the cell reads with
its sentence capitalization: "The process and ID scheme shall be
stack-agnostic." — no obligation differs.)*

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

**One flag for the ruler — CORRECTED.** SR-035 as written adds nothing to SN-011
and is a real merge candidate. The draft said it "is `Modified`, so touching it
costs a re-attest"; **that is false — SR-035 is live at `Verified`.** The advice
survives with a better reason: **touching a `Verified` row flips it `Modified`
and opens a re-attest window either way**, so bundle it into WI-451's window
rather than opening a second one. (Correction ledger #2.)

---

## 4. THE DECISIONS

Twelve. Items 1–8 are the boundary draft's §4, updated; items 9–12 are the
pack's tabled and deferred calls plus one rescued design question. Each is
self-contained: the question, the context you need, what each option costs, and
the recommendation where one is on record. **Where no recommendation exists, it
says so.**

### Decision 1 — Adopt or amend the depth-0 frame (§1)

**The question.** Do the 36 crossings in §1's table, against the twelve external
parties E1…E12, constitute the kit's declared frame?

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

### Decision 2 — Adopt or amend the port list (§2) and its discriminator

**The question.** Is §2's discriminator rule the one WI-451 applies, and is §2's
port list the depth-0 set?

**Two rows to decide explicitly.** **IF-080 / IF-081** (`integrate.py`,
`trunk_step.py`) declare `downstream adopter` but read as the unattended
station's internal serialization seams. And: **is a generated surface a port
while its generator is not?** (§2 says yes: *"The surface is the port; its
generator is not."*)

**Costs.** *Adopt:* WI-451 slice 2 unblocks against a stated rule; 57 SRs enter a
re-statement program. *Amend the list:* each addition or removal moves rows
between the 18 and the 57. *Reject the discriminator:* decision 2.7(a) has no
executable form and WI-451 stalls indefinitely.

### Decision 3 — The frame's typing axis: mechanics (principle already ruled)

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

### Decision 4 — The five `Experimental` rows, and the IF-103 tension

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

### Decision 5 — Where the external entities and the CONTEXT live

**RULED IN SESSION, 2026-08-13 (owner): shape 1 APPROVED — `external.toml` is
minted** as the off-spine home for external entities and the relationships
among them; no second interfaces registry. Two clarifications recorded with
the approval (log Decisions 2026-08-13i):

- **Every system-touching crossing stays an IF row** — the owner's read,
  confirmed: information flowing from/to an external entity to/from the system
  is and remains `interfaces.toml`'s to describe, IN and OUT. `external.toml`
  holds only entities and the external-to-external flows the IF registry
  structurally cannot express (`this_project` is always one side of an IF row).
  Boundary-ness derives from `counterpart` resolving to a declared entity.
- **External-to-external relationships are laid out as a relationship
  sub-table** — one directed row per relationship (`from` / `to` = resolvable
  entity ids, a `kind`, and `flow` prose), mirroring §8's record-each-seam-once
  shape so the context view renders entities as nodes and IF + REL rows as
  edges with one renderer. Per-entity link lists were passed over (two-sided
  declarations drift; one row cannot). A relationship row deliberately carries
  NO interface vocabulary (`contract`/`signal`/`stability`) — growing those
  fields would rebuild the second registry D-6 rejects. Symmetric kinds
  (e.g. `shares-personnel`) read as unordered.

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

### Decision 6 — The 15 missing crossings + 6 partial ones: who owns them

**The question.** 13 of the pack's 34 have no IF row at all, plus both new rows
(N-01, N-02) — an honest missing count of **15** — and 6 more have a partial row
that names a file or module where the actor belongs.

**Context.** WI-442 (queued) owns OI-28's two seeds (M-07, M-12/M-13). The rest
have no owner, **including the two this draft added**: **N-01** (`docs/process.toml`
as the owner's dial surface) and **N-02** (the inbound template-authoring flow).

**Cost.** Ruling scope here decides whether rung 1 can honestly close at all. A
frame declared complete with 15 undeclared crossings is the failure OI-14 named:
*"SRs are blessed today against a frame nobody declared."*

### Decision 7 — The duplication policy for the re-statement pass

**The question.** §3's option 3 (*the need names the outcome, the requirement
names the port*), or an alternative — **stated as a rule WI-451 slice 2 can apply
per row** — plus whether SR-035's merge rides that window.

**Context.** WI-451's spec contains **no duplication rule at all**. Slice 2
cannot run without this; it is not optional colour.

**Costs.** *Option 1 (tolerate the echo):* zero work; SN-028's `need` cell keeps
echoing downward into implementation vocabulary, against SN-033's ratified rule.
*Option 2 (merge):* refuted on machinery grounds — it breaks the SN→SR→LLR→TC
join `trace.py` walks. *Option 3 (split the roles):* each near-echo SN loses its
filename and its SR keeps it — a small number of SN edits inside a **ratified**
registry, so they open a re-attest window and must ride sitting 3's. Plus
SR-035's merge, if you order it (§3's flag).

**Recommendation on record:** option 3, noted as *already the ratified direction*
(SN-033 forbids internal paths in `need` cells; 2.7(a) permits them in SR cells
at declared ports). Do **not** target 1:1.

### Decision 8 — Where the boundary record LIVES once ruled

**The question.** SN-040's ratified acceptance requires the record *"kept with the
architecture, not in session prose."* **`docs/architecture.md` has NO boundary
section today** — measured: `grep -n "boundary\|external\|actor"` returns only
three generated function-summary rows. **That gap is owed under every option.**

**The shape.** The frame's prose belongs in `docs/architecture.md`; the typed
crossings belong in `interfaces.toml`. **Amended by §1b:** the honest statement is
now **no second interfaces registry** (still recommended); whether an
external-entity registry is minted is decision 5.

**Cost of not ruling it:** SN-040 is a ratified need with zero coverage and a
live, measurable gap against its own acceptance text.

---

### Decision 9 — The six one-obligation-per-row form findings (pack §2.1, TABLED)

*Carried in full from the sitting pack §2.1, now archived. It was tabled to this
sitting because splitting mints ids into SR text the retier may shuffle.*

**The question.** The prose batch's legibility method converts participial
chains into separate `It shall …` sentences. That is exactly what makes these
rows readable — and exactly what the kit's own one-obligation-per-row rule
flags. `trace.py` reported `form-findings=6` after the batch; the same command
at the pre-batch baseline reported none. **All six are rows the batch rewrote.**
*(ledger part 1 — [`../archive/plans/2026-08-13-wi444-batch-application.md`](../archive/plans/2026-08-13-wi444-batch-application.md))*

**The blast radius, precisely.** Form findings join the exit code only under
`trace.py --strict`, which `check.py` runs at the traceability step from the
**DevBar-Tests** bar on. At today's `DevBar-Reqs` nothing blocks — but this
sitting exists to move the bar back up, and these six will fail there.

The six rows, trimmed to their shall-clauses (verbatim from the live registry):

- **SR-040** *Per-phase routing and review dial* — **3 shalls**
  > "The unattended coordinator **shall select** the agent command template per in-process session phase (…) via AGENT_CMD_MAP/--cmd-map, falling back to the single AGENT_CMD.
  > It **shall surface** the declared reviewer dial (docs/process.toml [policies] review_rounds, default 1; …) at run start without enforcing it.
  > It **shall warn** (never block) when a lane resume surface exceeds the declared size threshold."
- **SR-042** *OKF knowledge-bundle export* — **2 shalls**
  > "gen_okf.py **shall export** the spine registries AND the key process docs as a generated Open Knowledge Format bundle under docs/okf: …
  > The bundle **shall be deterministic** (no clocks), with --check failing on any stale, missing or extra bundle file; …"
- **SR-050** *Process reference view* — **2 shalls**
  > "gen_trajectory.py **shall render** a Process reference tab in PROJECT_STATE.html beside the existing views, presenting how the project is built as three linked panels: …
  > The tab **shall be data-derived** where a canonical source exists (…); self-contained and byte-deterministic; a data-less repo renders byte-identically; --check freshness unchanged."
- **SR-057** *WI-DAG frontier scheduling* — **3 shalls**
  > "A stdlib schedule.py library/CLI **shall derive** the dependency-ready frontier from the tracked WI registry plus the active claims - never from prose.
  > It **shall exclude** blocked (queued + blockref), deferred, claimed, protected-conflicting and exclusive-conflicting WIs.
  > It **shall expose** ready --explain, ready --format json and simulate --jobs N."
- **SR-130** *Serial trunk step compiles log fragments…* — **2 shalls**
  > "A serial trunk step **shall compile** docs/log.d/ work-branch log fragments into docs/log.md in merge order derived from git history.
  > It **shall validate** every fragment before any write, rebase relative links to the log's home, delete compiled fragments, fail loudly at the first error, and never commit."
- **SR-131** *Tracked pause drains claiming to a merged stop* — **2 shalls**
  > "A tracked docs/work/pause file (TOML: reason, since) **shall pause claiming** — everything in flight finishes and integrates.
  > It **shall be read** via pause_reason as the ONE pause home (…), failing closed on malformation."

**The choice: SPLIT or WAIVE.** Splitting mints new SR ids and changes the
decomposition — **that is your act, not an agent's** (an agent minting ids to
silence its own lint is the failure mode the rule exists to catch). Waiving
means recording a reason on each row and accepting the finding standing at the
tests bar.

- **Yes (split)** costs: 8 new SR ids, their LLR/TC re-pointing, and 6 rows'
  chains re-attested. Buys: the rule holds, and the tests bar passes clean.
- **No (waive)** costs: six standing findings the harness will report at every
  tests-bar run forever, plus a documented exception the next reader must
  re-litigate. Buys: zero rework now.

**No recommendation is on the record for this one** — the ruling that authorised
the batch explicitly left it to the sitting. Note only that SR-130 and SR-131
already carry the rule in their own rationale cells (*"…is SR-134's obligation
(one row, one obligation)"*), so those two rows are self-aware exceptions.

**⚠ RESCUED INPUT the pack did not carry** — from the prose rewrite's §G
("Recorded as too low-confidence to propose"), item 8, now archived at
[`../archive/plans/2026-08-10-sn-sr-prose-rewrite.md`](../archive/plans/2026-08-10-sn-sr-prose-rewrite.md):

> 8. **Splitting SR-050 and SR-055 into separate requirements** — worth
>    considering, deliberately not drafted: it mints ids, changes the
>    decomposition, and may be pre-empted by §D item 6.

**Why it matters here:** SR-050 is one of the six form-finding rows, and this is
prior evidence that the *same* split was considered and consciously withheld for
the *same* reason (id minting + possible pre-emption). It does not change the
options; it tells you the question has been at this door before and the answer
each time was "not by an agent, and not before the thing that might pre-empt it."

### Decision 10 — The P5 partition (pack §3): accept or overturn

*Carried in full from the sitting pack §3, now archived, with three rescued
caveats and four pointers appended.*

Ruled at OI-14 (options A3 + A6), executed as WI-441 and **provisionally adopted
warn-first**: safe, because `LLR.Component` is a *traced* cell, so adopting it
opened **no re-attest window**.

**The ranking**

| Rank | Candidate | Cut / Straddle | Why it places here |
|---|---|---|---|
| **1 — ADOPTED** | **P5 narrow-waist** (4 components) | **31 / 7 of 12 (best)** | Best on the PRIMARY constraint: lowest behaviour straddle, and the only candidate that single-homes B3 (`value_to_cell`), B4 (gate policy), B9 (carrier vocabulary), B12 (`_norm_module`). Best boundary count (**4**) at a cut statistically tied with the best. **Zero new interface rows owed.** Same 8-module rework as the runner-up. Closest to the Core adopter's ratified answer — the strongest external evidence OI-14 names. |
| 2 — runner-up | P3 actor-boundary (5) | **30 (best)** / 10 | Lowest raw cut, 1 new IF row — but its components are AUDIENCE distinctions, and Parnas asks what CHANGES together; a dashboard and a decision brief may not. **If you overturn P5, reach for this.** |
| 3 | P4 functional (9) | 48 / 9 | Most faithful to the pure method, second-best straddle — but **15 interface rows that do not exist today** must be written before its checks are honest, and its F7 work-flow cluster at 22 crossings says that grouping is not one component. Right shape for a later depth-1 recursion, not depth 0. |
| 4 | P1 minimal-change (today's 5) | 33 / 10 | The honest floor: zero modules move, and it deletes the fail-open. But it ratifies the accident A1 was refuted for. Its value was making every other candidate justify its rework. |
| 5 | P2 shared-kernel (6) | 48 / **11 (worst)** | The measured **TRAP**, ranked last on purpose: extracting shared services without deleting the duplicated copies makes everything worse (cut 33→48, straddle 10→11, a 31-crossing hub K). Kept in the record because it is the move a reader reaches for first. |

**What P5 is — the four components, as minted**

| id | name | mission (live `components.toml`) |
|---|---|---|
| **CMP-006** | W1 Registry & conformance | the spine and everything that decides whether it holds — `spine_carrier`, `trace`, `trace_text`, `derive_gate`, `check_trajectory`, `plan_coverage`, `migrate_carrier`, `wi_convert`, `gen_arch_map` (9) |
| **CMP-007** | W2 Gatekeeper | every verdict a hook, CI job or gate run consumes — `check`, `check_privacy`, `subagent_gate` + the 8 `check_*` lints, and the shipped hooks (11) |
| **CMP-008** | W3 Autonomy | the unattended coordinator end to end — the 5 `agent_*`, the 5 `plan_*`, `adjudicate_brief`, `dispatch`, `handback`, `intake`, `integrate`, `lane`, `prompts`, `schedule`, `score_reviews`, `spec_move`, `trunk_step` (20) |
| **CMP-009** | W4 Human & adopter surfaces | everything a person or an adopting repo reads or runs — `bootstrap`, `run_menu`, the 7 `gen_*`, the 6 `traj_*` (15) |

Per-component interface load: **W1 26 · W3 17 · W4 14 · W2 5** (only W2 meets
the ≤6 narrow-waist target). **W1 is deliberately coarse** — under the OI-21
ladder architecture RECURSES, and W1 is the first candidate for a depth-1
partition at the scheduled re-score; P4's F1/F2 split is the natural seed.

**The 8-module rework, executed**

`check`, `check_privacy`, `gen_arch_map`, `migrate_carrier`, `prompts`,
`run_menu`, `subagent_gate`, `wi_convert` re-homed; the 5 multi-tagged modules
(`bootstrap`, `agent_common`, `agent_session`, `derive_gate`, `handback`) each
narrowed to ONE component. **CMP-006…009 minted, CMP-001…005 retired** under D-4
(ids never re-meaning). **149 `LLR.Component` + 54 IF `Component` cells
re-pointed; advisories 15 → 0, exactly as predicted.** All 31 cross-component
seams already have an IF row — **zero new rows** for the internal cut.

**The constraint finding underneath it**

**One-home-per-behaviour is unsatisfiable by ANY partition of today's tree:**
the 12 duplicated behaviours live as **39 (behaviour, home) pairs across 16
modules**, so the *copies* — not the boundaries — are the violation. The
partition adopts the owning home; the D-8 common-module program (WI-448) is what
DELETES the copies. P2's measurement is the proof the two must land together.

**`SR.Area` → aspect — the verdict to ratify**

Neither pure option survived measurement: **25 of 31** `Area` values are a
component by another name (derivable → redundant), and the **6 spanning values
carry 65 of 147 SRs** and are **ASPECTS** — cross-cutting concerns a partition
structurally cannot express. So "derive from Component" deletes information and
"retire outright" deletes the only grouping of SR-137…146. The provisional
verdict:

- `Area` as a 31-value free-text authored column **retires**;
- the six spanning values become a **closed aspect vocabulary**: `process`,
  `trajectory`, `unattended-loop`, `connectivity`, `perf`, `portability` — an
  aspect is a REVIEW grouping, not an ownership claim (cleanly compatible with
  the OI-19 hats axis);
- the 25 derivable values are dropped at conversion;
- **Portability's homelessness is not a defect** — its 3 SRs are depth-0
  system-level obligations discharged by every module, and under the OI-21
  ladder the system IS the depth-0 component.

**Not yet executed** — it is queued for the next SR-registry touch. **And
WI-451 slice 2 IS that touch** (§5.4), so this sitting should say whether
Area→aspect rides that window.

**What accepting vs overturning costs**

Four things to accept or overturn: (1) P5 as the depth-0 partition; (2) the
CMP-006…009 mint and CMP-001…005 retirement; (3) the Area→aspect conversion;
(4) the boundary inventory (34 crossings, its completeness declaration, and the
two OI-28 seeds inside it).

- **Accept** costs: nothing further; the warn-first state becomes the ruled one.
- **Overturn** costs: **a mechanical re-tag and a re-derive of generated
  surfaces — and nothing else.** `LLR.Component` is a traced cell, so no
  re-attest window opens either way. This is the cheapest decision in the pack.

#### Three caveats the pack did not carry — rescued, and they qualify the numbers above

**(a) The volatility limitation** — data pack Appendix B item 4, verbatim:

> 4. **Volatility.** Every metric here is coupling. The Parnas criterion — which
>    modules will *change* together — is not measured and cannot be; the pack's
>    own source knowledge pack says so, and it is the criterion that most often
>    decides whether a partition survives.

That is the honest limit on the whole ranking: every figure above is a *coupling*
number, and the criterion that usually decides survival was never measured.

**(b) The behaviour-vs-policy question — "the ruler should say which one binds."**
Every straddle number in the ranking is **conditional on an unruled reading**.
From the data pack §0, verbatim:

> That collapse collides head-on with the standing **F5 ruling** (owner,
> 2026-07-12; reaffirmed 2026-08-10 as repo-lock D-7, executed WI-426), which
> *requires* each kit script to stay stdlib-only and independently copy-able and
> which **rejected a shared `_kitcommon.py`**. F5's own live statement
> (`tests/test_rule_sync.py` module docstring) draws the line the ruler needs:
>
> > duplicated **PLUMBING** is accepted UNBOUNDED — no census, no allowlist, no
> > count. […] duplicated **POLICY** requires a BEHAVIOURAL PIN IN THIS FILE.
>
> So OI-14's "one home per behaviour" and F5's "duplicate plumbing freely" are
> **both live owner rulings that contradict each other on exactly these twelve
> behaviours**, unless "behaviour" is read as "policy". §4 therefore reports the
> straddle count under both readings, and the ruler should say which one binds.
> This is the single largest input to the ranking and it is prior to any
> partition choice.

And Appendix B item 2, verbatim: *"**Whether "behaviour" means "policy".** F5 vs
OI-14 (§0). Every straddle number changes depending on the answer."*

**⚠ Note the recency argument already on record**, from the shortlist ruling
([`../archive/plans/2026-08-13-part-a-shortlist-ruling.md`](../archive/plans/2026-08-13-part-a-shortlist-ruling.md)),
which the pack never carried:

> The pack flagged an apparent contradiction with the D-7-era F5 ruling
> ("duplicated plumbing accepted unbounded; shared `_kitcommon` rejected"):
> resolved by recency — D-8 (2026-08-12, step 2 inverted 2026-08-13) supersedes
> that acceptance, and P2's measurement is the proof the two must land together
> (extraction without deletion makes every number worse).

So the analysis *did* resolve it by recency; what has never happened is you
saying so. **If you accept the recency resolution, say it in the ruling** — it is
the single largest input to the ranking and it currently rests on an analyst's
inference.

**(c) The vacuous-zero corrections Part B inherits** — from the same
shortlist ruling, verbatim:

> - The containment rule does **NOT** cover the 45 IF rows
>   `cross_component_findings` is vacuous for — their untagged endpoints are
>   data files, external actors and directories, never arch-map modules, so
>   **they are policed by nothing today**. The OI-14 brief's hope that
>   containment covered them is refuted; the Part B schema tier is where that
>   coverage lands.
> - Two figures in the OI-14 brief did not reproduce and are corrected by the
>   pack: `LLR.Module` distinct values 59 (brief said 70), vacuous IF rows 45/68
>   (brief said 46/67). Every load-bearing figure (149 LLRs, 5 multi-tags,
>   97/64/17/33 edge accounting) reproduced exactly.

Part B (WI-443) has shipped; **whether it absorbed the 45-row coverage gap is not
recorded anywhere.** Worth one verification line in this sitting's ruling.

#### Pointers — the execution inputs, deliberately NOT copied here

A **decision** is carried in full; a large **execution-input table** is pointed
at. These live in
[`../archive/plans/2026-08-13-part-a-data-pack.md`](../archive/plans/2026-08-13-part-a-data-pack.md)
and do not need re-deriving:

- **P3's module assignment — the overturn fallback** — its §5 (P1–P4 assignments).
  The ranking says *"If you overturn P5, reach for this"*; P3's actual component
  membership exists **only** there.
- **The Area→CMP 31-row execution table** — its §6. Which 25 values drop, which
  SRs each carries. This is the input the conversion runs from.
- **The 12-behaviour census with per-behaviour homes, the exclusion list, and the
  unpinned B11** — its §4. The exclusion list (`_utf8_console`'s 32 homes,
  excluded as declared F5 boilerplate serving M-19) is what keeps the straddle
  counts honest. **B11 is still unpinned:** `derive_gate.load_csv` and
  `trace.load_csv` pass `errors="replace"`; `gen_release_checklist.load_csv` does
  not — so a non-UTF-8 byte in a registry is tolerated by two homes and raises in
  the third (verified: zero `load_csv` hits in `test_rule_sync.py`).
- **The Fn-01…Fn-20 functional decomposition with SN/SR feeds** — its §2. The
  OI-14 ruled sequence's second rung; the re-score loop is still scheduled.
  **Fn-20 (Portability) has no home** and Fn-02/Fn-12 (SN-037/SN-040) have no
  module of their own.
- **The three derivation scripts, verbatim** — its Appendix A. The reproducibility
  chain for figures still being ratified, including the exact `_norm_module`
  replication and the candidate scorer.

### Decision 11 — The hats roster (pack §4): accept, edit or cut

*Carried in full from the sitting pack §4, now archived.*

Lives at [`../requirements/hats.toml`](../requirements/hats.toml); read by
`project-trajectory/scripts/hats.py`. Ruled at OI-19 option (a): ship the
six-hat starting roster, **injection first, record second**. A hat is **not a
person and not a stakeholder row** — it is a QUESTION put to every decomposition
it applies to. Three keys are required per hat (`hats.py` refuses a row missing
any); a hat that names no failure class is refused as ceremony. **Absence is
opt-out, malformed is a refusal.**

**Your job here: review the six, cut what does not earn its place, add what is
missing, and rewrite any `applies_when` that does not match how this repo
actually files work.** A roster chosen by an agent and left unread is exactly
the ceremony SN-036 was admitted to prevent.

All six, verbatim:

**`SECURITY`** — `applies_when = "always"`
- *asks:* "What secret, credential, or irreversible action does this touch — and which requirement says who may reach it?"
- *listens_for:* "A decomposition that spends a secret, or takes an action nothing can undo, with no requirement naming the authority for it."

**`FIRST-RUN-ADOPTER`** — `applies_when = 'scope == "template" or scope == "both" or tags contains "templates"'`
- *asks:* "Does this hold for a stranger with only the shipped README and examples — no context from this project, no one to ask?"
- *listens_for:* "A requirement only satisfiable by someone who already knows this project: an undocumented convention, an example that does not run as shipped, a step whose prerequisite is never stated."

**`UNATTENDED-OPS`** — `applies_when = 'tags contains "unattended" or tags contains "loop"'`
- *asks:* "What does this look like at 3am with no human — what happens when its input is missing, stale, or half-written?"
- *listens_for:* "A failure that pages nobody: a silent degrade, a partial write left behind, an unbounded retry, a green that is green because nothing looked."

**`CROSS-PLATFORM`** — `applies_when = 'tags contains "scripts" or tags contains "launcher" or tags contains "shell"'`
- *asks:* "Which of Windows, macOS and Linux breaks this — path separators, line endings, console encoding, shell quoting, case sensitivity?"
- *listens_for:* "A rule that is true only on the author's platform and shipped as if it were universal."

**`MAINTAINER`** — `applies_when = "always"`
- *asks:* "Can a reader two years from now tell why this exists, and what would break if they deleted it?"
- *listens_for:* "A requirement whose reason lives only in the session that wrote it, leaving the next reviser unable to tell load-bearing from accident."

**`TEST-ENGINEER`** — `applies_when = "always"`
- *asks:* "What mechanical check fails if this is quietly violated — and can that check be shown to fail when it should?"
- *listens_for:* "An obligation with no enforcer, or an enforcer that passes because it never actually looks at the thing it claims to check."

**Two honest limits.** (1) The composer today declares `tags` (a work item's
Workstream + SafetyClass) and does **not** declare `scope`, because SN rows do
not yet carry a scope field — that is SN-039's job, so the three `scope ==`
clauses in `FIRST-RUN-ADOPTER` are honestly **silent**, not quietly true.
(2) SN-036 also requires a per-decomposition **record** of which hats were
applied and what each produced. Only injection shipped; **nothing gates on a hat
today.**

**Rescued from the SN intake, which dates limit (1)** —
[`../archive/plans/2026-08-12-sn-intake.md`](../archive/plans/2026-08-12-sn-intake.md),
its E1 tail: the `SN.Scope` schema field is **deferred into the step-7 schema
batch** (*"Waits for step 7: the `Scope` schema field, the edge columns'
retirement"*; repo-lock §8.6 item 3). Measured: there is **no `scope` key in
`stakeholder-needs.toml`**. So FIRST-RUN-ADOPTER's three `scope ==` clauses stay
silent **until the step-7 batch runs** — that is the date, not "someday". If you
want the hat live sooner, the schema batch has to move, not the hat.

**Costs.** *Accept as shipped:* nothing further; the roster becomes the ruled one
and `hats.py` keeps injecting it. *Edit or cut:* one TOML file, off-spine, no
re-attest window — the cheapest edit in this sitting. *Add a hat:* the same,
plus the D-7 bar (a hat naming no failure class is refused as ceremony). *Do not
review:* the roster stands unread, which is precisely the ceremony SN-036 was
admitted to prevent — and SN-036's *record* half still has no enforcer either
way.

### Decision 12 — The gate sign-off mechanization (OI-21 execution question 3)

**The question.** OI-21 ruled *sittings stay their own axis* — fewer sittings than
boundaries, each naming the rung range it certifies. What was never ruled is
**how a sign-off is composed and recorded** now that there are eight rungs rather
than three gates. This is the still-open half of OI-21's execution question 3.

**Rescued design, verbatim from the stage-gate-semantics §6** —
[`../archive/plans/2026-08-11-stage-gate-semantics.md`](../archive/plans/2026-08-11-stage-gate-semantics.md).
These three observations exist on **no live surface**:

> - **No gate has ever been driven at its own boundary.** `log.md`'s Gate
>   Sign-offs table records G1, G2 **and** G3 all `MET 2026-07-07` — the day
>   Thread 47 self-adoption started and the spine was first authored. They were
>   stamped at adoption, not certified at a boundary.

> - **WI-424's adjudicator seam is the natural carrier.** It already provides a
>   declared discriminator, evidence assembly that *refuses* rather than
>   half-fills, a typed verdict validated before a session may close, and
>   fail-closed routing for a declared-but-uncomposable brief. A gate sign-off is
>   that shape — a named role, a declared bar, assembled evidence, a typed
>   verdict. A fifth template, or one parameterized by hat, reuses all of it.

> - **The Gate Sign-offs table already distinguishes hat from human** (four role
>   columns plus a separate `Human` column). Any mechanization must fill the role
>   columns and leave `Human` reachable only by a human, or the record loses the
>   ability to answer "which gates did a person actually look at?"

**Why it belongs in THIS sitting.** The 2026-08-13 `DevStg-Needs` row is the
first sign-off ever driven at a real boundary — the first bullet's claim has just
stopped being universally true, and the mechanism that made it true (a human
reading a brief and ruling) is exactly what the second bullet proposes to
formalize. Ruling the shape now, while the practice is one row old, is cheaper
than retro-fitting it.

**Costs.** *Mechanize on the adjudicator seam:* one more brief template, plus the
`Human`-column constraint enforced. Note `## Gate Sign-offs` is a **code-pinned
heading** (`trunk_step.RESERVED_HEADINGS`, asserted by a bootstrap test) and
`LOG.template.md` ships downstream, so a rename is a code change. *Leave it
prose:* sittings stay a human convention with no enforcer — which is honest, and
is what the enforcement audit would record as a Prose-tier rule.

**No recommendation is on the record** beyond OI-21's already-ruled
"sittings stay their own axis."

---

## 5. Downhill impacts on the queued work items

Five specs sit in [`../work/queued/`](../work/queued/), all dependency-ready
(every `needs` edge resolves to a complete WI). Each carries text this sitting's
rulings make stale. **Re-scope them in the ruling; do not let a builder discover
the staleness mid-slice.**

### 5.1 WI-390 — concurrency-v2 program close

[`../work/queued/WI-390-concurrency-v2-program-close.md`](../work/queued/WI-390-concurrency-v2-program-close.md)
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

[`../work/queued/WI-442-oi-28-seeds-landed-on-the-spine.md`](../work/queued/WI-442-oi-28-seeds-landed-on-the-spine.md)
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

### 5.3 WI-448 — common-module inversion program (OI-16 / D-8)

[`../work/queued/WI-448-common-module-inversion-program.md`](../work/queued/WI-448-common-module-inversion-program.md)
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

[`../work/queued/WI-451-sr-boundary-conformance-pass.md`](../work/queued/WI-451-sr-boundary-conformance-pass.md)
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

[`../work/queued/WI-452-llr-165-resync-helper-resurface.md`](../work/queued/WI-452-llr-165-resync-helper-resurface.md)
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

## 6. Housekeeping ledger — ruled-but-unexecuted, and homeless

Fifteen small items rescued from the plan docs being archived. Each names its
source at the archive path, and a proposed disposition: **needs a ruling** ·
**rides an existing window** · **pointer-only**. None is large; several are the
kind that silently cost a re-attest window if executed alone.

### 1. SN-007's ruled clause strike — **EXECUTED 2026-08-13, owner ruling in session** (superseding the ride-sitting-3 disposition)

*Source:
[`../archive/plans/2026-08-10-sn-sr-prose-rewrite.md`](../archive/plans/2026-08-10-sn-sr-prose-rewrite.md)
§B item 2, verbatim:*

> **OWNER RULED, 2026-08-11: strike the clause.** *"I'm fine with removing
> the prose … which doesn't have coverage today. That's not really
> sustainable anyways."* So the fix is a **deletion, not a new SR** — the
> need stops claiming per-change coverage. Note what this makes true, which
> is the argument for it: **SN-007's own acceptance cell already states the
> sustainable version** (*"The suite bootstraps a temp scaffold and runs
> every script; `pytest -q` green is required before each change lands"*) —
> a gate on the *suite* at each change, never a per-change coverage proof.
> The Need cell was over-claiming against its own acceptance, so striking
> the clause makes the row self-consistent rather than weakening it. Lands
> with the prose batch at the sitting (a lone edit to a ratified need would
> open a re-attest window outside the batched one — §F).

**Measured NOT EXECUTED.** `docs/requirements/stakeholder-needs.toml` SN-007
`need` still reads *"…a change to a script is covered by a test exercised
end-to-end against a real scaffold."* The prose batch it was ruled to ride has
been and gone.

**Why this is the sharpest item in the ledger.** Sitting 1 **ratified the SN
registry** (all 27 rows `kind = "core"`, zero draft). So the strike now does
exactly what its own ruling said to avoid: *a lone edit to a ratified need opens
a re-attest window outside the batched one.* **Disposition: schedule it INSIDE
sitting 3's window — never as a lone edit.** It is a one-cell deletion; the cost
is entirely in *when* it lands.

**EXECUTED — OWNER RULING IN SESSION, 2026-08-13.** Reviewing the post-strike
remainder (*"…its own changes stay traceable and tested"*), the owner flagged
that **"changes … tested" still reads as delta-testing** — as if something
tests the A→B change itself — which nothing does: the suite tests the *state
after* each change (the scaffold bootstrap), while "traceable" genuinely does
attach to changes (change-intake, the WI registry, the log). The owner then
ruled the fix lands **NOW, before this sitting runs** — *"SNs are the first
stage, so it should be changed before sitting 2 attempts to build boundary
conditions that are built up on SNs"* — superseding both the plain strike and
the ride-sitting-3 disposition. The `need` cell now reads:

> "The people maintaining this kit hold it to its own standard: it stays
> traceable and tested through every change."

A state claim at every landing, not a per-change coverage or delta-testing
claim; the `acceptance` cell (unchanged) carries the mechanism at its own
altitude. **Blast radius, measured at execution:** the struck clause was the
*undecomposed* one — zero SR descendants — and the four `Verified` SRs citing
SN-007 (SR-010, SR-011, SR-036, SR-111) realize the surviving half, so no
child's grounding moves and nothing flips. (The SN tier carries no `status`
field; its maturity is `kind`, unchanged at `core`. The owner authored and
ratified the wording in session, so no token-comparison transcription bar
applies — there is no source text being transcribed.) The ruling is in
[`../log.md`](../log.md)'s Decisions.

### 2. §E.5 — migration history inside the `Requirement` cell — **NEEDS A RULING**

*Source: prose-rewrite §E.5, verbatim:*

> Six rows carry **migration history inside the `Requirement` cell** ("the retired
> X, deleted by SR-Y, is not an input"; "the legacy Z half retired with the
> dispatcher at Phase 5"). A requirement cell states an obligation; *why it used to
> be different* is rationale.
>
> **Offered as its own ruling, not folded into the formatting pass** — because
> moving text between cells changes which cell a re-attest reads, which is not a
> formatting change.

**Still live, verified:** SR-040's *"the retired docs/run-phase file, deleted by
SR-059, is not an input"*; SR-131's *"(the legacy untracked docs/pause half
retired with the dispatcher at Phase 5)"*; SR-059's own trailing parenthetical
(item 7 below). **Disposition: needs a ruling of its own** — and note it interacts
with decision 9, since SR-040 and SR-131 are both form-finding rows.

### 3. SN-008's acceptance cites its own child — **NEEDS A RULING** (small)

*Source: prose-rewrite §B, SN-008: "the acceptance cell cites **SR-006** — a need
citing its own child. Recommend deleting the token in either form; the join
already carries the link."* Live: SN-008 acceptance reads *"…the
explicitly-requested `--lenient` local mode is the one sanctioned degrade to SKIP
(SR-006)…"* **Precedent exists** — see item 14, where the same class of deletion
was applied to SN-014 and SN-021 as the plan's own choice.

### 4. SN-027's acceptance carries design provenance — **NEEDS A RULING** (small)

*Source: prose-rewrite, SN-027: "the acceptance cell's trailing `"Spec of record:
docs/archive/specs/… + docs/concurrency-restructure.md"` is design provenance in
an acceptance cell; move to **SR-132**'s rationale."* Live and unmoved.

### 5. SR-060's dead-file prohibition — **NEEDS A RULING** (small)

*Source: prose-rewrite, verbatim:*

> **Note:** the `never docs/next-wi` clause names a file SR-059 deletes. It stays
> meaningful as a prohibition, but the sitting may prefer to strike it once SR-059
> lands. **Flagged, not changed.**

Live: SR-060's requirement reads *"…and any rework finding (never docs/status.md
or docs/next-wi)."* SR-059 is `Verified` and its migration is what deletes the
file. **SR-060 is `Verified`, so a strike opens a window** — bundle it.

### 6. §G item 3 — `interfaces.toml` still declares the `docs/subagent-gate` counterpart — **NEEDS A RULING**

*Source: prose-rewrite §G, verbatim: "**Whether `docs/subagent-gate` (SR-043) is
stale** — no reader found in `project-trajectory/scripts/`; the gate is hook-side
and was not traced to a reader. SR-043 is dropped from the batch on this ground."*

**Live, measured:** LLR-040 now names `process.toml [checks] subagent_gate`, but
**IF-038 still declares `counterpart = "docs/subagent-gate"`** with a contract
reading *"reads the docs/subagent-gate policy (off|ask|deny) via the shared
declared-line parse…"*. The question was dropped for the SR; **it is still open
for the IF row**, and an IF row is exactly what this sitting is about.

### 7. §G item 4 — SR-059's ungrammatical trailing parenthetical — **NEEDS A RULING**

*Source: prose-rewrite §G item 4: "**What SR-059's trailing parenthetical was
meant to say** — it is ungrammatical as committed. Repairing it means deciding its
meaning."* **The live broken text, verbatim:**

> "(The generated docs/run-state surface this row once paired with retired with the
> dispatcher at Phase 5 - the stop banner and exit codes carry the outcome.)"

SR-059 is `Verified`; repairing it opens a window, so bundle it. (It is also an
instance of item 2's pattern.)

### 8. §G item 7 — SR-025 title/requirement mismatch — **NEEDS A RULING**

*Source: prose-rewrite §G item 7: "SR-025's title reads *"Skills index + checked
per-agent fan-out"* while the requirement covers only index regeneration.
Resolving it means deciding whether an obligation exists."* **Live and
unchanged:** SR-025's requirement is *"gen_skills_index.py shall regenerate
skills/INDEX.csv from each SKILL.md applicability frontmatter."* — no fan-out
clause. SR-025 is already `Modified`, so this rides the open window at no extra
cost.

### 9. §D artifact 2 — the unfinished `"(Note this )"` — **NEEDS YOUR TEXT**

*Source: prose-rewrite §D, verbatim:*

> 2. **One item ends in an unfinished `"(Note this )"`.** The record does not say
>    which item. **The owner must supply the completion.** Not reconstructed.

Zero hits anywhere else in the repo. **This is the one ledger item nobody can
progress without you** — an agent reconstructing it would be inventing intent.

### 10. §C's kit-level consequence — the lifecycle framing as an SR authoring checklist — **NEEDS A RULING**

*Source: prose-rewrite §C, verbatim:*

> **Kit-level consequence:** this table ships to every adopter. **Recommended
> shape:** keep the lifecycle framing (Provision / Startup / Runtime) in the
> template as an **authoring checklist for SRs**, not as a second table of needs —
> preserving what the tier taught while removing the level error.

The edge tier itself is gone (OI-18 dissolution). What the tier *taught* has no
home. This is a **template change**, so it touches what ships downstream.

### 11. §E.2's thirteen dropped rows — **POINTER-ONLY** (a future formatting pass)

*Source: prose-rewrite §E.2, verbatim: "Per correction 3, these are removed rather
than presented as outlines. **Reason for all thirteen: exact replacement text was
not produced in this pass, and an outline is not ratifiable.** They remain on the
measured list for a future pass."*

The thirteen ids, which exist **only** in that document:

`SR-129` · `SR-031` · `SR-136` · `SR-147`¹ · `SR-053` · `SR-054` · `SR-052` ·
`SR-056` · `SR-043`² · `SR-144` · `SR-139` · `SR-142` · `SR-145`

> ¹ SR-147 leaves the *legibility* batch but stays in §E.3 as a **carrier
> correction**. ² SR-043 is additionally unresolved on fact — see §G.

### 12. The SN intake's two standing residues — **POINTER-ONLY / lesson**

*Source:
[`../archive/plans/2026-08-12-sn-intake.md`](../archive/plans/2026-08-12-sn-intake.md).*

**E2 — a standing do-not-mint, verbatim:**

> The reviewer also confirmed **no needs may be minted from repo-lock §8.6
> items 5–7** (prompt-carrier format, common modules, guardrail delivery) —
> those were questions, since answered as analyses, not stakeholder intent.

**E3 — the SN-029 spatial-metaphor diagnosis, verbatim** (the fix is in the
registry; the *diagnosis* is nowhere):

> one residual CONFIRMED — the SN-029 amendment's "below the reserved tier" reads
> backwards in level-number order while reading correctly in abstraction order
> (the two rounds tripped on it in opposite directions, the tell that the
> spatial metaphor itself was the defect); fixed as "on every tier released to
> automation".

That last clause is a reusable lesson about *spatial metaphors in tier
vocabulary* — worth carrying into the D-9 ladder decision (sitting 3 §3), which
is a tier-vocabulary rewrite.

### 13. The README's `Status=Modified` line — **RIDES the D-9 step-7 sweep list**

*Source:
[`../archive/plans/2026-08-11-stage-gate-semantics.md`](../archive/plans/2026-08-11-stage-gate-semantics.md)
§8, verbatim:*

> **Also stale and unrelated to the ruling:** the README's *"a `Status=Modified`
> row … derives G2 until the sitting blesses it"* goes false the moment D-9
> migrates, since `Modified` leaves the vocabulary. It belongs on step 7's sweep
> list.

**D-9 has NOT migrated** — so this is a *pending* sweep item, not a done one, and
it is **not** in repo-lock's checklist. It attaches to sitting 3 §3.

### 14. WI-444's three application residues — **POINTER-ONLY**

*Source:
[`../archive/plans/2026-08-13-wi444-batch-application.md`](../archive/plans/2026-08-13-wi444-batch-application.md).*

- **H1, two transcription flags:** SN-014's proposed cell dropped a trailing
  `(SN-008)` and SN-021's dropped `(SN-010)` — *"the plan's choice, not drift —
  applied as written. Note it is the same class of edit the plan holds back as a
  recommendation on SN-008."* Plus SN-015's quote-glyph delta (single quotes,
  applied verbatim). **This is the live precedent for ledger item 3.**
- **H3, four accounting slips** (recorded as plan slips, **no words removed in
  any**): SR-049 (plan `+2`, measured `+0` words plus three list numerals),
  SR-042 (plan `+2`, measured `+4`), and SR-110 and SR-059 measured `+0` against
  claimed `+3`/`+1`.
- **H2, the pointer that matters:** the full before/after is retained in
  `docs/ratify/2026-08-13-wi444.md` — but the **pre-edit `sha256` cell hashes**
  are **only** in the archived ledger. They are the sole proof of pre-edit cell
  state independent of git.

### 15. The `LLR.Module` 70-vs-59 warning — **POINTER-ONLY**

*Source: data pack §3b, verbatim: "**Do not carry 70 forward without re-deriving
it.**"* OI-14's decision cell states **70** distinct `LLR.Module` values; the pack
reproduces **59** at `81a142c2` and could not reproduce 70 by any reading. Both
this and the 46-vs-45 vacuous-row count are declared as discrepancies rather than
silently reconciled (Appendix B item 5).

### 16. Two registry strays from sitting 1's own surfaced-not-fixed list — **RIDE THE NEXT REGISTRY TOUCH**

*Source: [`../log.md`](../log.md) 2026-08-13d, "Surfaced, not fixed."* Beyond the
items already carried above (the TC-159 chain gap → sitting 3 §2.2; IF-080/081 →
decision 2; SR-035 → §3; M-15/M-17's dissolved SN owners → the §1 table), two
small strays remain that no decision above owns:

- **IF-064's `contract` cell still cites SN-016 inline** — a dissolved edge need,
  outside the ruled 29-cell sweep scope (that sweep was SR `rationale` cells
  only). Same treatment as the sweep: drop the dead id, keep the content.
- **The SN registry's comment block still declares the now-empty Edge-case
  section** — the OI-18 dissolution deleted the rows and left the header prose.

Both are mechanical, neither opens a re-attest window (a comment block and an IF
cell are not traced spine text) — batch them onto whichever registry touch runs
first rather than minting anything.

---

## 7. Where the depth lives — the archive map

Everything below is archived at `../archive/plans/` (moved with this document's
commit; indexed by [its README](../archive/plans/README.md)). One line each on
**what it still uniquely holds**, so nothing is re-derived by accident. (The two
mechanical prerequisites — a `docs/archive/plans/*` glob in `docs/orphans-allow`
and the `tests/test_ratification_level.py` docstring repoint — were executed
with the move.)

| Archived file | What it uniquely holds |
|---|---|
| [`2026-08-13-sitting-pack.md`](../archive/plans/2026-08-13-sitting-pack.md) | **§1 and §1a-ii in full** — the 12 previously-laundered rows, what round 1 was caught doing on each, and the before(`81a142c2`)→after cell quotes for every one, plus the five TRANSFORMED SN→SR carrier chains. Sitting 1 signed against it; it is the attestation evidence and is not reproduced here. |
| [`2026-08-13-devstg-boundary-draft.md`](../archive/plans/2026-08-13-devstg-boundary-draft.md) | **§0's provenance** — how `DevStg-Boundary` appeared in three steps, the `boundary_incomplete` docstring quotes, and the five-Experimental-row table's original framing. §1–§4 are carried above. |
| [`2026-08-10-sn-sr-prose-rewrite.md`](../archive/plans/2026-08-10-sn-sr-prose-rewrite.md) | The **per-row rewrite tables** for 29 SNs + 17 SRs with word deltas, the round-1 adversarial review record, §E.1's exact replacement texts, §E.3's stale-verdict table, and §G's eleven low-confidence items in full. Ledger items 1–11 are lifted from it; the rest is spent. |
| [`2026-08-11-stage-gate-semantics.md`](../archive/plans/2026-08-11-stage-gate-semantics.md) | §3's "in-process" reasoning and §4's measured `stage_to_gate` mapping — **cited from a live test docstring** (`tests/test_ratification_level.py:352`). §6's four observations are carried at decision 12 and ledger item 13. |
| [`2026-08-11-status-ladder-migration.md`](../archive/plans/2026-08-11-status-ladder-migration.md) | **⚠ STILL LIVE — its program is sitting 3's decision.** The only checklist for D-9: §1's 470-row per-tier migration table, §2's predicate map, §3's SN `kind` split with its nine readers, §4's four traps by `file:line`, §5's ordered 7-step plan, §6's three declared unknowns. **Its figures are stale** — measured 2026-08-11 at `bc6315d9`, *pre-dissolution* — so the SHAPE is the plan and every number must be re-derived before executing. |
| [`2026-08-12-sn-intake.md`](../archive/plans/2026-08-12-sn-intake.md) | The SN-033…SN-040 intake record: the adversarial dispositions table, the launcher-tier dispute, and the ten-row edge-dissolution map with its two judgment calls. Ledger item 12 is its live tail. |
| [`2026-08-13-part-a-data-pack.md`](../archive/plans/2026-08-13-part-a-data-pack.md) | The measured inputs behind decision 10: §1's 34-crossing inventory with the per-crossing `Character` column (dropped from §1 above deliberately — signal typing is an IF-row property), §2's Fn-01…Fn-20, §3e's classification of the 45 vacuous IF rows, §4's 12-behaviour census + exclusions, §5's P1–P4 module assignments (**P3 = the overturn fallback**), §6's 31-row Area→CMP table, and **Appendix A's three derivation scripts verbatim**. Its own header: *"analysis input, not a decision."* |
| [`2026-08-13-part-a-shortlist-ruling.md`](../archive/plans/2026-08-13-part-a-shortlist-ruling.md) | Superseded by decision 10 **except** the F5→D-8 recency resolution and the two vacuous-zero corrections, both carried above. |
| [`2026-08-13-wi444-batch-application.md`](../archive/plans/2026-08-13-wi444-batch-application.md) | The per-row before/after ledger with **pre-edit `sha256` cell hashes** — the only proof of pre-edit cell state independent of git (ledger item 14) — plus the verification-run figures at application and the one stated reconstruction. |
| [`2026-08-10-carrier-cutover.patch`](../archive/plans/2026-08-10-carrier-cutover.patch) | **Zero decision content.** 777 KB of spent diff, reachable from git history; `status.md` already calls it *"spent history, not an instruction."* |
| [`DP-001-dual-plan-loop-wiring/`](../archive/plans/DP-001-dual-plan-loop-wiring/) | A **closed** dual-plan round (verdict in `../log.md`; WI-194…199 filed and complete). Keep the directory intact — its files cross-link relatively. Its `verdict.md`/`goal.md` cite the retired `docs/gate-policy` / `gate-policy: autonomous`, harmless as history but worth one line in the archive README row. |
