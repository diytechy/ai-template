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

The going-forward semantic for what surrounds the system is **entity**. The
noun lives on the registry table (`[entity.EXT-###]`), so the class values
carry none: **`operational` · `enabling` · `interoperating`**. Applied to this
document's live surfaces (owner-confirmed 2026-08-13): the §1 table's column
header is renamed **Party → Entity**, the §2 discriminator rule now reads
*"external entity from §1"*, and decisions 1/3 speak entity. Quoted rulings
and the archived draft analysis (the §1 stub points at it) keep their original words
("actor", "parties") as provenance — read them as *operational entity* /
*entities*. Everything written from here on — kit-facing schema, process
prose, the `external.toml` field vocabulary — uses entity vocabulary. ("Entity" is also
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

## 1. The drafted frame — ARCHIVED

The original 36-row crossing table and the carried draft analysis (§1a what
defines a boundary; §1b the operational context) were superseded as the live
frame by the 2026-08-13k reframe and moved, with the other ruled decision
material, to
[`../archive/plans/2026-08-13-sitting-2-superseded-material.md`](../archive/plans/2026-08-13-sitting-2-superseded-material.md)
(owner cleanup direction, 2026-08-13m). **The live frame is §1R below.** The
two owner rulings the draft carried stay summarized at §0.2 and recorded in
[`../log.md`](../log.md) Decisions 2026-08-13e/f.

## 1R. The depth-0 frame, v2 — the system creates the template (2026-08-13n)

**Status: CONFIRMED — the five §1R.7 confirmations RULED 2026-08-13o**, with
three amendments applied below: the external reviewer CLI merged into the
provider entity (*"a model CLI is just a model CLI, whether primary or
secondary"*), B-08 removed (`check_vendored` is run by the development
environment, not an input into this design-scope system), and the residual
skills-fan-out / `docs/knowledge/` uncertainties folded into B-05 — they are
template content, available from the package whether an adopter uses them or
not. The v1 tables (31 BIFs
over 8 entities, RULED-then-amended) are archived in
[`../archive/plans/2026-08-13-sitting-2-superseded-material.md`](../archive/plans/2026-08-13-sitting-2-superseded-material.md);
their old ids appear in the *absorbs* columns so nothing is lost.

**The governing principle (owner, verbatim-close):** *the system is the act of
creating the guardrails and template contents; the system provides the methods
of acting on repositories autonomously — including itself — but just because
it happens to USE them as well doesn't mean they are each inputs into the
system.* The **Template** is its own entity — the thing actually delivered, a
separate package — which provides its full content to adopters **and feeds
back into this same project's development session**. Activating autonomous
builds from that adopted content (`agent-resume`) is **NOT an input into this
system**: it is an input into this repository's *development session*, exactly
as it would be for any other adopter — and once running, the loop *"is not
differentiable from a human user, an LLM in CLI, or that script launching LLM
runners."* Likewise `dev-setup` is only template content that is provided.

### 1R.1 The entities (v2 — five; ids re-proposed, v1 numbering superseded)

| id | Entity | Class | Description |
|---|---|---|---|
| **EXT-001** | **Development session** | `operational` | Human or LLM in a terminal — attended or the `agent-resume` loop, indistinguishable by rule — **plus the user's local development environment and the working copy in its hands** (shell, git client, OS, Python, editors, test runner, LLM runners). ⚠ *Interpretation to confirm:* "includes the repository contents" is read as *the session holds the checkout*; the SYSTEM owns the governed state those edits become once admitted through the hook floor. |
| **EXT-002** | **Template** | `deliverable` ⚠ | **The delivered package** — every `*.template.*`, the registries, scripts, hooks, skills, launchers (`dev-setup.*`, `agent-resume.*`, `run.*`) — as a separate package. ⚠ `deliverable` is a proposed ADDITION to the class vocabulary (operational/enabling/interoperating do not fit an output package); confirm or rename. From an adopter's frame this package is their *enabling system*. |
| **EXT-003** | **Adopter** | `operational` | The downstream team + repo. Receives the Template (REL-001), never the repository. |
| **EXT-004** | **Hosted CI** | `interoperating` | Remote validation: triggers + OS×Python matrix in, job verdicts out. |
| **EXT-005** | **Model provider API(s) / CLI(s)** | `interoperating` | The model services and command-line runners behind any LLM in the session — the primary builder AND the adversarial reviewers (codex `sol`/`terra`) alike: *"a model CLI is just a model CLI, whether primary or secondary"* (owner merge, 2026-08-13o). They touch the SESSION, never the system (REL-003). |

**Dissolved as entities** (absorbed into EXT-001's local environment per the
owner's ruling): git (v1 EXT-005), OS · filesystem · Python (v1 EXT-007), the
test/coverage toolchain (v1 EXT-008). Their obligations survive as
**requirements on Template content** (portability, hook behavior, tier floors)
and as the mechanics of the B-01/B-04 crossings — not as frame entities.

### 1R.2 The system's boundary crossings (v2 — **six**; B-08 removed 13o, **B-03 removed 13u**)

| BIF | Dir | What crosses | Absorbs (v1 / draft ids) |
|---|---|---|---|
| **B-01** | IN | **Governed writes**: artifact, registry and config edits admitted **only through the git hook floor** (privacy, format, gate checks) — the one write path from the session into the system's governed state | BIF-004/N-01, BIF-006/M-13, BIF-007-in/M-10, BIF-025/X-09 (the guardrail's read is this crossing's mechanism), the write half of BIF-026/M-16 |
| **B-02** | IN | **Authority**: rulings, attestations, `Status` flips — the distinguished input the process advances on | BIF-005/M-11 |
| **B-04** | OUT | **Guardrail verdicts during a session**: hook-floor accept/reject, `subagent_gate` PreToolUse allow/deny | BIF-012/X-07, the verdict halves of BIF-006/BIF-026 |
| **B-05** | OUT | **THE TEMPLATE — the packaged deliverable** to EXT-002. The delivered scripts' contracts (`check.py`, `bootstrap.py` + MAPPING, `agent_loop.py`, `check_vendored.py`, `gen_cases.py`, `gen_release_checklist.py`, the hooks, the launchers) are **IF definitions tied `interface_to_external = "B-05"`** — content of the package, not separate system crossings | BIF-014/M-07, BIF-015/M-06, BIF-016…021/X-01…X-06, and BIF-001/M-01 + BIF-002/M-02 as CONTENT (their invocation is the session's, per 13n) |
| **B-06** | IN | Hosted CI trigger: push · PR · schedule; the OS × Python matrix | BIF-027/M-04 |
| **B-07** | OUT | Hosted CI job verdict + step log | BIF-028/M-05 |

### 1R.3 The relationships (external-to-external; the system is not a party)

| REL | From → To | Flow |
|---|---|---|
| **REL-001** | Template → Adopter | full content provided; adopted into their repo (their scaffold, their loop, their hooks) |
| **REL-002** | Template → Development session | **self-adoption**: this repo's session adopts the same content and activates autonomous builds from it (`agent-resume`) — the 13n NOT-an-input ruling lives here. **Absorbed 13u:** the session then *runs* that adopted toolkit to produce `PROJECT_STATE.html`, `open-items.html`, `docs/status.md`, `docs/gate` and the console reports, and surfaces them to the human reading from that session. **Those outputs are NOT system outputs** — the system delivered the generators (B-05 content); the workflow that runs them is adopted, exactly as an adopter's would be |
| **REL-003** | Development session ↔ Model provider API(s)/CLI(s) | the LLM runner surface, primary and adversarial alike: rate limit, auth expiry, model retirement (old M-15) and hostile-review briefs out / findings in (old M-14) — the backoff obligation reads as a requirement on delivered loop content, exercised session-side |

### 1R.4 The reclassification ledger — every v1 row dispositioned

**Stay system crossings (folded):** v1 BIF-004/005/006/007-in/025/026 →
B-01/B-02 (+ verdict halves → B-04); BIF-012 → B-04; BIF-027/028 → B-06/B-07.
**Move to REL-002 (13u):** BIF-007-out/M-10, BIF-008/M-03, BIF-009/M-19,
BIF-010/M-09, BIF-011/M-08 — the former B-03 set.
**Become Template content (IF definitions under B-05):** BIF-014, BIF-015,
BIF-016…021 — *strictly outputs*; plus BIF-001 (`dev-setup`) and BIF-002
(`agent-resume`), **explicitly ruled NOT inputs**.
**Become relationships:** BIF-023/M-15 and BIF-024/M-14 → REL-003 (merged
2026-08-13o); the adoption and self-adoption flows → REL-001/REL-002.
**Dissolve into the session entity:** BIF-003/M-12 (prompts into a session —
between the human and their runner, inside EXT-001); BIF-013/X-11 (the loop
launching its CLI — the session driving itself; the provider behind it is
REL-003); and BIF-022/X-10 (`check_vendored` is **run by the development
environment** — its content input arrives through B-01's governed writes, and
the tool itself ships as B-05 content; ruled 2026-08-13o).
**Dissolve with their absorbed entities:** BIF-029/M-17 (OS · filesystem ·
Python), BIF-030/M-18 (pytest results) and BIF-031/X-13 (`coverage.json`) —
their obligations survive as **requirements on Template content** (portability;
the tier floors) and as B-01/B-03/B-04 mechanics, not as crossings.
**Count check:** 8 stay (→ B-01/B-02/B-04/B-06/B-07) + 10 become Template
content (→ B-05) + **5 move to REL-002 (the former B-03)** + 2 become
relationships (→ REL-003) + 3 dissolve into the session + 3 dissolve with their
entities = **31**; none dropped silently.

### 1R.5 The registry shape around them (decisions 3/4/5 as ruled)

**`external.toml` holds three kinds of row** — the owner's decision-3/4 ruling
inverts the earlier split: the boundary interfaces live WITH the entities, so
**system requirements form around the boundary interfaces**, and the concrete
IF rows tie into them:

```toml
[entity.EXT-001]
name = "Development session"
class = "operational"            # operational | enabling | interoperating | deliverable
description = "Human or LLM terminal session, attended or the agent-resume loop."

[relationship.REL-001]           # external-to-external only; no interface vocabulary
from = "EXT-001"
to   = "EXT-002"
kind = "hands-off"
flow = "…"

[boundary.BIF-014]               # a frame-level crossing; SRs form around these
entity = "EXT-002"               # must resolve to a declared entity
direction = "out"                # in | out | inout, the system's point of view
carries = "the template artifact class: *.template.* + registries/*"
```

**`interfaces.toml` slims to interface DEFINITIONS** (the owner's decision-4
direction): an IF row states what the interface concretely *is* — its actual
definition — and sheds the complexity it carries today (`direction`,
`counterpart`, the argued contracts). An IF carries a directional tie-back field **only** when it realizes a
boundary interface — **`interface_from_external = "BIF-###"`** for an IN
crossing, **`interface_to_external = "BIF-###"`** for an OUT crossing, both
for an in/out crossing (owner naming, 2026-08-13m; supersedes the earlier
provider/consumer field names); otherwise provider/consumer are **implied by the
requirements**: **an LLR lists its requirements around PROVIDING that
interface** (and possibly where it is consumed — consumption may stay implied
at design). This is also where the owner's decomposition point lands: **an LLR
may be the provider of information that ends up external** — decomposition
breaks the system into manageable pieces that still serve the necessary
output — and the BIF tier is what lets an SR state the boundary obligation
while the LLR states which piece provides it, without the two fighting over
one row.

**What this re-keys.** `derive_gate.boundary_incomplete` stops reading IF
`Stability` and gates rung 1 on **the boundary-interface set**: every declared
BIF settled, every BIF realized (or explicitly deferred). IF `stability` is
owner-questioned (*"is it even a useful attribute, if the intent is just to
flag a draft item?"*) and is expected to retire with the slimming — which
**dissolves decision 4's five-Experimental-rows question and the IF-103
tension entirely**: internal definitions no longer gate the frame rung, and
the resync helper's stability is its own affair.

### 1R.6 How an SR is written against a bundle crossing — validation shapes (owner + review, 2026-08-13)

Each crossing is a bundle of implementation-specific interfaces; **the SR
states an observable AT the crossing, and the tier below pins the bundle's
members.** Two shapes:

- **Artifact-shaped crossings — the observable is a standing thing.**
  **B-03:** the validation/status surfaces are *generated and fresh*; LLRs
  name the exact files and expectations; the `--check` freshness steps are the
  mechanical verification. **B-05:** the package *exists, is complete, and is
  consumable downstream*; the manifest is already pinned (`bootstrap.py`
  MAPPING + `test_bootstrap` file lists + `test_dogfood_sync`). **B-06/B-07:**
  the job files are *present and declare the same bar the local moments run*
  (`tests/test_ci_tier_declaration.py` against the declared moment→tier
  table).
- **Event-shaped crossings — the observable is a VERDICT to a constructed
  stimulus** (B-04, and B-01/B-02's admission side). SR form: *"when a session
  attempts ⟨class of act⟩, the system shall ⟨admit/refuse⟩, observably ⟨exit
  code / named reason / logged decision⟩."* TCs construct the act and assert
  the verdict — the pattern the suite already uses: stage a crafted secret →
  pre-commit refuses with the finding named; drive `subagent_gate` with an
  allowed and a denied spawn → allow/deny verdicts + the record in
  `out/subagent-gate.log`; malformed `commit-msg` input → refusal.

**The honest limit to write INTO the B-04 SR:** a local hook floor is
bypassable (`git commit --no-verify`), so *"no unchecked write enters governed
state"* is only validatable as a **pair** — B-04's verdict at the moment of
the act plus B-06/B-07's hosted re-run of the same bar as backstop (the
declared CI mirror). Stating the pairing keeps the green honest. This
subsection is the SR-writing guidance for WI-451 slice 2's re-statement.

### 1R.7 Completeness + the confirmations this section owes

**CONFIRMED 2026-08-13o — the frame is LOCKED.** The five confirmations, as
ruled: **(1)** the session/working-copy interpretation stands (the session
holds the checkout; the system owns the governed state admitted through the
hook floor). **(2)** `deliverable` accepted as the Template's class — noting
`class` is read by nothing mechanically today and is planned only for the
generated context view and the advisory schema tier; nothing gates on it.
**(3)** B-08 removed: `check_vendored` is run by the development environment —
not an input into this design-scope system. **(4)** the git / OS / toolchain
entity dissolutions stand (compactness). **(5)** the skills fan-out and
`docs/knowledge/` packs fold into **B-05**: they are template content,
available from the package whether an adopter uses them or not.

**The declared frame: 5 entities · 6 boundary crossings · 3 relationships**
*(7 → 6 at 13u, when B-03 was ruled not a system output).*
The one deliberate exclusion: `MULTI_REPO.md`'s cross-repo rung stays
unaudited. **Decision 1 is CLOSED.**

## 2. The port set and the discriminator — what WI-451 executes against

*Carried in full from the boundary draft §2, now archived.*

**The discriminator, stated as a rule WI-451 can apply mechanically:**

> An artifact may be named in SR text **iff** it is the *this-project* side of an
> IF row whose `counterpart` is an **external entity from §1** — i.e. it is a
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

**Chain 3 — SN-028 → 2 SRs: the near-echo that MEASURES CLEAN.** *(Re-measured
2026-08-13p; the draft's reading of this chain was wrong and is corrected
here.)* The draft claimed *"read SN-028's need sentence against SR-137's
requirement sentence and they say the same thing."* They do not. The live cells:

> **SN-028 `need`:** "The repo owner can find and change every policy dial in
> **one home** — a **single hand-edited, machine-read file** — and a repo that
> declares the same dial twice is REFUSED rather than resolved by precedence."

> **SR-137 `requirement`:** "The kit shall read every process policy dial from
> a single `docs/process.toml`, and shall REFUSE — never resolve by precedence
> — a repo in which any dial is declared both there and in its legacy one-word
> file. The file's line shape shall be a checked contract: one `key = value`
> per line under a bare `[section]` header, no dotted keys, no inline tables,
> no multi-line strings."

They overlap on **one clause** (one home + refuse-not-precedence — the outcome
restated at its crossing, which is legitimate). SR-137 then adds the filename,
the legacy-file specificity and the **entire line-shape contract**, none of
which is in the need. SR-138 adds the migration. **And SN-028's need cell does
NOT name `docs/process.toml`** — the prose batch already removed it; the
filename lives in the *acceptance* cell, which ratified SN-033 explicitly
exempts. So option 3's worked example on this row **is already executed**. SN-011 → SR-034/035/114 is the
same shape: SR-035's whole text is *"the process and ID scheme shall be
stack-agnostic"* with acceptance *"the ID scheme is language-neutral"* — an SR
that adds **nothing** over its SN. *(Live, for the record, the cell reads with
its sentence capitalization: "The process and ID scheme shall be
stack-agnostic." — no obligation differs.)*

**The options where the echo is real:**

1. **Tolerate the echo, the acceptance cell carries the delta.** Cheapest; keeps
   the tiers uniform. *(The draft argued this violates SN-033 by echoing
   downward — **measured false**: zero of 27 need cells carry an internal path
   or implementation identifier. See the measurement below.)*
2. **Merge** — delete the SR, point LLRs at the SN. Breaks the join
   (`trace.py` walks SN→SR→LLR→TC); refuted on machinery grounds alone.
3. **Split the roles: the SN carries the OUTCOME, the SR carries the PORT
   CONTRACT.** SN-028 becomes *"the owner can find and change every policy dial
   in one home, and a repo declaring a dial twice is refused"* — no filename;
   SR-137 keeps `docs/process.toml`, the line grammar and the refusal points.

**Recommendation: option 3 — and the SN side is ALREADY DONE.** SN-033
(ratified) forbids internal paths in `need` cells; decision 2.7(a) permits them
in SR cells at declared crossings. The two compose into one sentence: **the need
names the outcome, the requirement names the crossing.** Do **not** target 1:1
— 82 of 148 SRs are genuinely multi-need, and forcing 1:1 would either merge
unrelated crossings into one row or duplicate one crossing's contract across
several.

**The invariant, re-keyed to the §1R v2 frame:** *one SR per **(need,
crossing-or-delivered-property)*** — because under v2 an SR attaches either to
a system crossing (**B-01…B-07**) or to a **property of the delivered package**
(**B-05** content). The old wording said "(need, port)", which had no home for
the large class of SRs describing what the template's own scripts must do in an
adopter's hands. The current 232 edges are already a rough approximation.

**The measurement that settles the SN side** *(2026-08-13p)*: **0 of 27 `need`
cells** contain an internal path or implementation identifier — the prose batch
cleaned them all. **16 of 27 `acceptance` cells** do, and ratified SN-033's own
acceptance scopes the rule to exempt exactly those: *"The rule applies
specifically to each SN `need` cell, not to engineering requirements or
acceptance evidence."* So option 3 costs **zero SN edits** and opens **no SN
re-attest window**; what remains of decision 7 is purely an **SR-side rule** for
slice 2.

<!-- fig: cmd="python3 - tomllib over stakeholder-needs.toml; regex for
[\w./-]+\.(py|toml|md|csv|html|ini|yml|sh|cmd) and docs//scripts/ paths over
need vs acceptance cells", rev=e32fd9a0 -->

**Worked examples for slice 2, from the live registry:**

| | Example | Verdict |
|---|---|---|
| **Healthy fan-out** | SN-011 → **SR-034** (AST import scan; the ledger row's required fields; a shipped-tier dependency needs a recorded owner ruling) and **SR-114** (the CI matrix spans, plus a reasoned exclusion of the macOS+3.11 cell as redundant coverage) | **KEEP** — the need cannot carry these; each names a distinct observable |
| **True echo** | **SR-035** — requirement *"The process and ID scheme shall be stack-agnostic."*, acceptance *"The ID scheme is language-neutral."* | **MERGE or RE-STATE** — no crossing, no mechanism, no measurable criterion; the acceptance restates the requirement. Not attachable under v2 either: stack-agnosticism is a **B-05 delivered property**, so a re-statement needs a real observable (e.g. the shipped registries and ID scheme carry no language-specific token; a non-Python adopter's scaffold passes `trace.py`) |
| **Looks like an echo, is not** | SN-028 → **SR-137 / SR-138** (chain 3 above) | **KEEP** — one clause overlaps; the line-shape contract, the legacy-file rule and the guarded entry points are the SR's own |
| **Thin but grounded** | SR-072 (`gen_trajectory.py` byte-determinism), SR-022 (`check_vendored.py` drift), SR-086 (`trace.py` accepts `Critique`) | **NOT duplication** — these are short *and* grounded; they belong to the 57-row **re-statement** class, not this decision. Keep the two classes apart in slice 2 |

**One flag for the ruler — CORRECTED.** SR-035 as written adds nothing to SN-011
and is a real merge candidate. The draft said it "is `Modified`, so touching it
costs a re-attest"; **that is false — SR-035 is live at `Verified`.** The advice
survives with a better reason: **touching a `Verified` row flips it `Modified`
and opens a re-attest window either way**, so bundle it into WI-451's window
rather than opening a second one. (Correction ledger #2.)

---

## 3R. The requirement FORM rule — RULED 2026-08-13s

**The ruling, in the owner's words:**

> **A single "shall" statement is permitted, and must be applied to interfaces
> going to the respective component level. An "interface" can still be a bundle
> as long as it's broken down or clearly stated in the component details.**

Three consequences, stated so a builder can apply them per row:

1. **One `shall` per requirement row — mandatory, at every tier.** This settles
   the pack's §2.1 form question affirmatively (decision 9): the answer is
   neither *waive* nor *split-these-six-now*, it is **the rule holds and is
   applied as rows are re-tiered.**
2. **The shall's subject is an interface at that row's own component level.**
   The rule is *recursive*, which is what lets one sentence govern the whole
   spine: an **SR** states a shall against a **boundary interface** (§1R.2's
   B-01…B-07); an **LLR** states a shall against a **component-level
   interface** (the depth-1 partition's seams). A row whose shall names
   something below its own level is mis-tiered — which is exactly the finding
   the re-tier will surface, row by row.
3. **A bundle is a legitimate interface, IF it is broken down below.** An
   interface may bundle others provided the decomposition *"is broken down or
   clearly stated in the component details."*

**This resolves the B-05 mega-node risk** flagged at decision 9. B-05 (the
Template) is the largest bundle in the frame, and a single shall against it is
**legitimate under this rule** — the obligation to discriminate moves to the
component details, where the delivered capabilities (harness verdict, scaffold
and MAPPING, unattended loop, generators, hook floor) are broken out. The
bundle does not have to be pre-split at the SR tier to be honest; it has to be
*decomposed somewhere and stated*.

**The owner's acceptance of the cost, recorded because it governs how the
re-tier is judged:** *"a decomposition will result in significant retiering,
and I'm accepting that because most of it should just be shifting items around,
but the repo should follow its own definition, and it should help to expose if
there are some other issues in the way this system has been decomposed."* So
the re-tier is **not** a defect-remediation program: it is the repo applying
its own rule, and the *findings it exposes* are a deliverable of it, not a
failure of it.

---

## 4. THE DECISIONS

Twelve. Items 1–8 are the boundary draft's §4, updated; items 9–12 are the
pack's tabled and deferred calls plus one rescued design question.

### 4.0 STATE OF PLAY — **ALL TWELVE DECISIONS ARE RULED** (as of 2026-08-13u)

Sitting 2's decision surface is **complete**. Nothing on this list awaits you;
what remains is execution, then sitting 3.

| # | Ruled | The call |
|---|---|---|
| **1** | 13k · 13l · 13o | frame locked — **5 entities · 6 crossings · 3 relationships** |
| **2** | 13m · **13u** | IF-080/081 internal **confirmed**; **B-03 removed** — the status/validation surfaces are not system outputs, they are adopted-toolkit outputs, folded into REL-002 |
| **3** | 13l | the inversion: boundary interfaces live in `external.toml`; SRs form around them; IF rows tie back directionally |
| **4** | **13u** | **`Stability` retires — IF rows follow the approval schema**; the five `Experimental` rows become ordinary approve-or-fix work |
| **5** | 13i · 13l | `external.toml` minted: entities · relationships · boundary interfaces |
| **6** | 13l (deferred **by ruling**) | re-lands mechanically post-schema as *BIF rows with no realizing IF* |
| **7** | 13q · 13s · **13u** | rule text ruled; **SR-035 deferred into the re-tier** (a real obligation lacking an observable, not a duplicate); **SN-033's checker filed as a placeholder WI** |
| **8** | 13q · **13u** | **`docs/architecture.md` DIES** — architecture renders in `PROJECT_STATE.html` from the registries; ten scripts and `check_flows.py`'s input are the execution shape |
| **9** | 13q · 13s | dissolves into the re-tier; §3R's form rule governs |
| **10** | 13s | **DEFER** P5 ratification until after the re-tier; warn-first stands; WI-448 proceeds on provisional tags |
| **11** | 13q · 13r · **13u** | roster determined at `DevStg-Boundary`; `FIRST-RUN-ADOPTER` kept + fixed; seven hats added (five off by default); **proposed text accepted** |
| **12** | **13u** | **one shared status vocabulary across every registry**, per-registry subsets allowed, **change detection deferred** |

**What is NOT decided, deliberately** — three items that re-land as execution
reaches them: decision 6's crossing ownership (post-schema); the **human-agent
entity** follow-on from decision 2 (recommendation: keep the human inside
EXT-001 per 13k, and say so deliberately if you reverse it); and
**`check_flows.py`'s Runtime-flows obligation** when `architecture.md` goes
(decision 8 — move the flows or retire the check, but do not let a deletion
silently retire it).

**Two unowned mechanizations sit across these** and belong to whichever
execution row takes the schema: the **SR→IF checker** (SN-037's ratified
acceptance, §5.4) and **SN-033's need-cell checker** (decision 7's rider) —
each a stated obligation with no enforcer. Each is
self-contained: the question, the context you need, what each option costs, and
the recommendation where one is on record. **Where no recommendation exists, it
says so.**

### Decision 1 — Adopt or amend the depth-0 frame (§1)

**RULED 2026-08-13l (entities adopted, rebuild delivered), then AMENDED
2026-08-13n:** the **Template** joined as its own entity (the delivered
package), the session absorbed the local development environment (git, OS,
toolchain dissolve as entities), and the ruled principle — *using what the
system creates does not make each used tool an input* — reclassified the v1
rows: `dev-setup`/`agent-resume` invocation are NOT inputs, the delivered
contracts are Template content under one deliverable crossing, and the
provider/reviewer flows are session relationships. **The live frame is §1R
v2, CONFIRMED and LOCKED 2026-08-13o** (5 entities · 7 crossings · 3
relationships; the five §1R.7 confirmations all ruled). **Decision 1 is
CLOSED.**

**The reframe in one paragraph (RULED 2026-08-13k; long form archived).** The
repository IS the system; the template is NOT the system but what it DELIVERS
— adopters adopt the template, never the repository, and the template files
are all of the system's adopter-facing outputs. A human or LLM terminal
session (including the `agent-resume` loop) is ONE external entity; the
tooling is internal, and self-adoption is the system validating what it
builds with the structure it delivers. Implementation closure accepted
deliberately. The twelve drafted entities became §1R.1's eight; E12 and N-02
dissolved; who-holds-authority is policy and record, never an entity split.
Full ruling: [`../log.md`](../log.md) Decisions 2026-08-13k; the long-form
block and the original decision text:
[the archive](../archive/plans/2026-08-13-sitting-2-superseded-material.md).

### Decision 2 — Adopt or amend the port list and its discriminator (self-contained)

**What this decision is.** Sitting 1 ruled 2.7(a): *an SR may name an artifact
only where that artifact is a declared boundary crossing.* For that rule to be
executable, there must be a declared list of which artifacts those are — the
**ports**. A port is the **system-side surface of a boundary interface**
(§1R.2): the thing an external entity actually types, invokes, reads or edits.
Everything else is an **internal seam** — it belongs to the LLR tier, and an SR
naming it is naming implementation. This decision adopts (or amends) that list
and the rule, which is what unblocks WI-451's re-statement of the 57
internal-naming SRs.

**The discriminator rule, in full** (restated from §2 so nothing else need be
opened): *an artifact may be named in SR text iff it is the system-side surface
of a boundary interface whose entity is one of §1R.1's eight — i.e. it is a
port. Everything else re-states against the interface that types its seam, or
demotes to the LLR tier.*

**CONFIRMED 2026-08-13m (owner): ports get concrete IF rows too.** The BIF row
states the frame-level crossing; the realizing **IF row** in `interfaces.toml`
states the concrete interface definition, tied back through the directional
field: **`interface_from_external = "BIF-###"`** for an IN crossing,
**`interface_to_external = "BIF-###"`** for an OUT crossing (both for in/out).
The concrete IF-side list is deliberately undecidable until decision 1's table
is locked — under v2 it falls out of B-05's content list and B-01…B-04's
mechanics at execution.

*(Note on ids: the port list below cites v1 `BIF-###` ids; under §1R v2 the
delivered script ports tie `interface_to_external = "B-05"` — they are
Template content — and the session-facing surfaces are the system sides of
B-01…B-04. **The port SET is unchanged**, so the 18/57 census and WI-451's
sizing do not move; re-key the references when the v2 table is confirmed.)*

**The port list being adopted** (each is the system side of a §1R.2 row):
`check.py` (BIF-016) · `bootstrap.py` incl. `--agents`/`--sync` (BIF-015/017) ·
`agent_loop.py` + root `agent-resume.*` (BIF-018, BIF-002) · `run.*`/`run_menu`
(BIF-008) · `dev-setup.*` (BIF-001) · `subagent_gate.py` (BIF-012) · the git
hook floor `pre-commit`/`pre-push`/`commit-msg` (BIF-006/026) ·
`check_vendored.py` (BIF-019/022) · `gen_cases.py` (BIF-020) ·
`gen_release_checklist.py` (BIF-021) · and the declared surfaces a session
reads or edits: `docs/process.toml` (BIF-004), `docs/status.md` (BIF-007),
`docs/gate`, `PROJECT_STATE.html` (BIF-010), `open-items.html` (BIF-011),
`docs/architecture.md`. Measured on the live registry: **18 SRs name only
these; 57 name at least one internal module** — the re-statement program's
size.

**Two rows to decide explicitly:**

**RULED 2026-08-13u.** (1) **IF-080 / IF-081 fall internal — CONFIRMED.**
(2) The generated-surface question produced a **deeper correction, and the
owner took it**: those surfaces are **not outputs of this system at all.**

> **B-03 is REMOVED as a boundary crossing.** The system generates *the
> toolkit* that produces those outputs. `docs/status.md`, `docs/gate`,
> `PROJECT_STATE.html` and `open-items.html` are **derivatives of the workflow
> adopted from the template kit runner itself** — generator scripts that ship
> in the Template (B-05) and come back into the development session through
> self-adoption. So the surfacing folds into **REL-002**: the session runs the
> adopted toolkit, produces those outputs, and shows them to the human reading
> from that session.

This is the §1R principle applied one level further than v2 had carried it —
*using what the system creates is not a system crossing* — and it makes the
frame smaller again: **6 crossings, not 7.** It also retires the
"is a generated surface a port?" question rather than answering it: neither the
surface nor its generator is a system port; both are delivered content.

**⚠ One follow-on to confirm.** The ruling names *"a human agent … an external
user seeing that from the development session"*. If that human is a **distinct
entity**, the surfacing becomes a declared entity-to-entity relationship and the
frame gains a sixth entity. **Recommendation: keep the human inside EXT-001 and
fold the surfacing into REL-002 (as applied above)** — because 13k ruled
explicitly that human-vs-loop *"survives as policy and record, never as an
entity split"*, and splitting a Human entity out to receive B-03's old content
would re-open exactly that. If you want the human declared anyway, say so and
the split is mechanical — but it should be a deliberate reversal of 13k, not a
side effect of this ruling.

**The original two calls, for the record:**

1. **IF-080 / IF-081** — `integrate.py`'s serialized merge queue and
   `trunk_step.py`'s trunk step. Their rows *claim* `counterpart = "downstream
   adopter"`, but both are the unattended station's **internal** serialization
   machinery — no adopter ever invokes them; the adopter's copy runs inside
   *their* repo's loop, reached through the delivered template (BIF-014), not
   through a direct crossing. Under §1R they have **no BIF** and fall internal.
   Confirming that here is what licenses WI-451 to demote the SRs naming them.
2. **Is a generated surface a port while its generator is not?** §2's answer,
   to confirm: **yes** — the session reads `PROJECT_STATE.html` (BIF-010), so
   the *surface* is the port; `gen_trajectory.py` is CMP-009 realization an SR
   must not name. Same for `open-items.html` vs `gen_open_items.py`.

**Costs.** *Adopt:* WI-451 slice 2 unblocks against a stated rule; 57 SRs enter
the re-statement program. *Amend the list:* each addition or removal moves rows
between the 18 and the 57 — re-run the census before re-sizing. *Reject the
discriminator:* 2.7(a) has no executable form and WI-451 stalls indefinitely.

### Decision 3 — The frame's typing axis: mechanics (principle already ruled)

**RULED 2026-08-13l: the boundary interfaces live IN `external.toml`, beside
the entities.** The owner's shape: *"entities.toml [= the approved
`external.toml`] defining both the entities and their to/from interfaces; IF
entries reserved [for the concrete definitions, tying to a boundary interface
only when they realize one]."* So the frame is typed by **`[boundary.BIF-###]`
rows** (entity + direction + what crosses — §1R.3's schema), **system
requirements form around the boundary interfaces**, and real IF rows tie into
them via the directional tie-back fields (`interface_from_external` /
`interface_to_external = "BIF-###"`, 2026-08-13m naming). This **settles
the `external`-flag question**: no hand-set flag — boundary-ness is a
first-class row, and an internal seam claiming an adopter counterpart becomes
unrepresentable, which is what the "declare the entities, derive the rest"
shape below argued for. The crossing-class axis (CLI · exit status · file
artifact · …) remains unminted; propose deferring it until a check needs it.
**Supersedes in part 2026-08-13i's first clarification** ("every
system-touching crossing stays an IF row"): the *frame-level* crossing is now
a BIF row in `external.toml`; the *concrete definition* stays an IF row. D-6's
duplicated-vocabulary hazard is answered by **reference, not duplication** —
the two registries hold different kinds, linked by resolvable id, so
divergence is a checkable dangling ref rather than silent drift.

*The original question (the `external`-flag / crossing-class mechanics) and
the "declare the entities, derive the rest" proposal that anticipated this
ruling are archived at [`../archive/plans/2026-08-13-sitting-2-superseded-material.md`](../archive/plans/2026-08-13-sitting-2-superseded-material.md).*

### Decision 4 — The five `Experimental` rows, and the IF-103 tension

**RULED 2026-08-13u: `Stability` RETIRES — IF rows follow the APPROVAL schema
(draft vs approved), like every other tier.** *"I would actually like to follow
the approval schema (draft vs approved). Perhaps I misunderstand."* — no
misunderstanding; the two were different axes and you are choosing the right
one. **`Stability`** (`Experimental`/`Provisional`/`Stable`) is a *contract-
maturity* claim: how much the interface is expected to move. **Approval** is
*has this row been ratified*. The five `Experimental` rows show why the
distinction collapsed in practice — four were carrier plumbing that was simply
**never re-reviewed**, i.e. *unapproved*, wearing a maturity word. So the axis
that was doing the real work was approval all along.

**Consequences, and it closes two decisions at once:**

- `interfaces.toml` gains the **same approval element as SN/SR/LLR/TC** (the
  one closed vocabulary D-9 lands) and **`stability` is deleted, not
  duplicated** — this is decision 12's `interfaces` gap closed, on the same
  ruling.
- **`external.toml`'s entity / boundary / relationship rows carry it from their
  first commit** — the frame's own rows become ratifiable, which is what
  decision 12 asked for.
- `derive_gate.boundary_incomplete` re-keys onto **boundary-interface
  completeness** as already ruled, now reading an *approval* state rather than
  `Stability`: rung 1 clears when every declared boundary interface is
  approved.
- The five rows' content findings (IF-057's undeclared consumer seam; the three
  never-re-reviewed carrier seams) become ordinary **approve-or-fix** work —
  no longer a special class.

The earlier direction, which this supersedes:

**RULED DIRECTION 2026-08-13l — the question largely DISSOLVES.** Two owner
points recorded: (1) **`stability` is questioned as an attribute at all** —
*"is it even useful here, if the intent is just to switch/flag a draft item?"*
— and is expected to retire with the IF slimming (§1R.3); (2) **an LLR may be
the provider of information that ends up external** — that is what
decomposition is *for* (small manageable pieces still serving the necessary
output) — and the tension that creates with the boundary is resolved by the
BIF tier: **the SR states the boundary obligation against the BIF; the LLR
states which piece provides the realizing interface** (the directional tie-back field on the IF row when boundary-tied —
`interface_to_external` for a delivered output; implied in the requirement
otherwise).
Consequence: `boundary_incomplete` re-keys from IF `Stability` onto
**boundary-interface completeness** (every BIF settled and realized-or-
deferred), so the five `Experimental` rows stop gating rung 1 — they are
internal definitions — and **the IF-103/WI-452 tension disappears**: the
resync helper's maturity is its own affair, not the frame's. What survives of
this decision for the sitting: confirm the re-key, and dispose of the five
rows' *content* findings (IF-057's undeclared consumer seam; the three
never-re-reviewed carrier seams) as ordinary registry hygiene rather than
frame business.

*The five-row `Experimental` table, the three original dispositions and the
IF-103/WI-452 tension write-up (dissolved by the re-key above) are archived at
[`../archive/plans/2026-08-13-sitting-2-superseded-material.md`](../archive/plans/2026-08-13-sitting-2-superseded-material.md).*

### Decision 5 — Where the external entities and the CONTEXT live

**RULED IN SESSION, 2026-08-13 (owner): shape 1 APPROVED — `external.toml` is
minted; RE-CONFIRMED 2026-08-13l** with one amendment: per decision 3's
inversion, `external.toml` also carries the **`[boundary.BIF-###]`** rows
(§1R.3), so it holds entities + relationships + boundary interfaces. (The
owner's later message says "entities.toml" — the ruled name stays
**`external.toml`** per this decision; recorded so the wobble is not read as a
rename.) The 13i clarifications as amended:

- ~~Every system-touching crossing stays an IF row~~ — **SUPERSEDED 2026-08-13l
  (decision 3):** the *frame-level* crossing is a `BIF` row in `external.toml`;
  `interfaces.toml` keeps the *concrete interface definitions*, tying to a BIF
  via `interface_from_external`/`interface_to_external` only when
  boundary-realizing.
  Boundary-ness is a first-class row, not a derivation from `counterpart`.
- **External-to-external relationships are laid out as a relationship
  sub-table** — one directed row per relationship (`from` / `to` = resolvable
  entity ids, a `kind`, and `flow` prose), mirroring §8's record-each-seam-once
  shape so the context view renders entities as nodes and IF + REL rows as
  edges with one renderer. Per-entity link lists were passed over (two-sided
  declarations drift; one row cannot). A relationship row deliberately carries
  NO interface vocabulary (`contract`/`signal`/`stability`) — growing those
  fields would rebuild the second registry D-6 rejects. Symmetric kinds
  (e.g. `shares-personnel`) read as unordered.

*The original three-shapes question, the INPUTS/OUTPUTS tiering, the costs
and the riders are archived at [`../archive/plans/2026-08-13-sitting-2-superseded-material.md`](../archive/plans/2026-08-13-sitting-2-superseded-material.md).
The riders themselves are executed or absorbed: E11 retired (artifact class),
E12 dissolved by the 13k reframe, and the class sits on the entity in §1R.1's
schema.*

### Decision 6 — The 15 missing crossings + 6 partial ones: who owns them

**BLOCKED — ruled unanswerable as posed (owner, 2026-08-13l):** *"Can't answer
this until the external interfaces are redesigned around the agreed-upon
external entities."* Under the §1R rebuild the question re-lands in the new
shape: mint the 31 `BIF` rows (§1R.2), then the "missing" set becomes **BIF
rows with no realizing IF reference** and the "partial" set becomes **IF rows
whose definition must slim and tie back** — both mechanical lists once the
schema executes. Ownership assignment waits for that execution (the WI-442
re-scope is the natural first vehicle, §5.2).

*The original missing/partial counts and their context are archived at
[`../archive/plans/2026-08-13-sitting-2-superseded-material.md`](../archive/plans/2026-08-13-sitting-2-superseded-material.md).*

### Decision 7 — The duplication policy for the re-statement pass

**RULED 2026-08-13q — and the owner is right that it was effectively already
decided.** 2.7(a) (an SR may name an artifact only at a declared crossing), the
13l inversion (SRs form around the boundary interfaces) and §1R.6 (validation
shapes) had already settled it; this decision only owed the *sentence*. The
canonical rule, in the owner's words, which is **fuller than option 3** because
it carries the input→outcome relation rather than only the naming:

> **The requirement names the interface, and the expectations to generate that
> interface outcome according to its available inputs.**

That is the rule WI-451 applies per row. The two riders below still need
ordering. The original question, for the record:

**The question.** §3's option 3 — *the need names the outcome, the requirement
names the crossing* — or an alternative, **stated as a rule WI-451 slice 2 can
apply per row**, plus whether SR-035's disposition rides that window.

**Context.** WI-451's spec contains **no duplication rule at all**, and slice 2
cannot run without one. It matters more now, not less: the §1R v2 frame is
expected to drive **significant SR churn**, and this rule is what keeps that
churn from re-introducing echoes while it re-states.

**⚠ RE-MEASURED 2026-08-13p — two of this decision's stated costs were false**
(§3 carries the evidence and the worked examples):

- **The SN side is already clean.** *0 of 27 `need` cells* carry an internal
  path or implementation identifier. The "SN-028 echoes downward against
  SN-033" cost line was wrong — its need cell says *"a single hand-edited,
  machine-read file"*, with the filename in the **acceptance** cell, which
  ratified SN-033 explicitly exempts (*"not to engineering requirements or
  acceptance evidence"*).
- **Option 3 therefore costs ZERO SN edits** and opens **no SN re-attest
  window** — not "a small number of edits inside a ratified registry" as
  previously stated. Option 3's own worked example (strip SN-028's filename)
  **was already executed by the prose batch.**

**Costs, corrected.** *Option 1 (tolerate):* zero work, but no rule exists when
slice 2 re-states ~57 rows, so echoes re-enter unchallenged. *Option 2
(merge):* still refuted on machinery grounds — it breaks the SN→SR→LLR→TC join
`trace.py` walks. *Option 3 (split the roles):* zero SN edits; the cost is
**per-row judgement inside slice 2's existing window**, which the WI-444
token-verification bar already governs.

**Recommendation on record:** option 3, with the invariant re-keyed to the v2
frame — ***one SR per (need, crossing-or-delivered-property)***, an SR
attaching either to a system crossing (B-01…B-07) or to a property of the
delivered package (B-05). Do **not** target 1:1 (82 of 148 SRs are genuinely
multi-need).

**Two riders to order with it:**

1. **SR-035's disposition — DEFERRED to the re-tier (ruled 2026-08-13u).**
   The owner: *"ironically SR-035 is truly a requirement, but I'm not sure of
   the best way it can be tested — let's consider this during the SR
   re-tiering."* That is the right call and it sharpens the row's status: it is
   **not** a duplication case to merge away, it is a **genuine obligation with
   no known observable** — which is precisely the class §1R.6 exists to
   resolve, and precisely what the re-tier is for. Carry it into WI-451 as a
   named row rather than a general instruction. *(A candidate observable to
   test against when it comes up: the shipped registries and ID scheme carry no
   language-specific token, and a non-Python adopter's scaffold passes
   `trace.py` — a B-05 delivered property, testable by scaffolding.)*
2. **SN-033's checker — AGREED as a PLACEHOLDER (ruled 2026-08-13u).** Its
   ratified acceptance commissions *"a declared check [that] reports the row
   and phrase when a need cell contains an internal path, implementation-only
   identifier or process citation"* with a reviewed exception list. It does not
   exist, and it would report **zero findings today** — which is exactly why it
   should land now: it **locks the clean state in** before the re-tier churn.
   **On "not sure of the best way to do that" — the shape the kit already
   has:** a stdlib `check_need_form.py` in the `check_*` lint family, run from
   `check.py`'s step table **warn-first** (the DEFAULTED tier), scanning each
   `need` cell for path-like and identifier-like tokens against a declared
   exception list for names that are themselves user-facing interfaces. It
   ships with its exception list empty and its finding count at zero, so the
   *first* row that dirties the tier is the one that reports. Filed as its own
   WI rather than carried as prose.

### Decision 8 — Where the boundary record LIVES once ruled

**RULED 2026-08-13u — going further than 13q: `docs/architecture.md` DIES.**
*"architecture.md can die, instead the available tables should produce full
architecture in the ProjectState.html, much of that exists already today."*
Correct on the last point — `traj_views.py` already renders a **"How (SW
architecture)"** tab. So the target is: **registries → the dashboard**, with no
markdown way-station.

**This answers the 13q open question by dissolving it:** there is no
"narrative remainder stays authored" if the file itself is gone. What was owed
becomes a disposition for each of the file's ~192 hand-authored lines.

**⚠ The execution shape, measured — this is a real program, not a delete.**
**Ten scripts touch `docs/architecture.md`** (`gen_arch_map`, `traj_parse`,
`gen_trajectory`, `check_trajectory`, `check.py`, `check_doc_refs`,
`check_flows`, `traj_status`, `trunk_step`, `bootstrap`), and the current data
path is **registries → `gen_arch_map` → `architecture.md` → `traj_parse` → the
dashboard tab**. Retiring the file means re-pointing that chain to
**registries → dashboard** directly. Two specific consequences to rule with it:

- **`check_flows.py` loses its input.** It reads the *"Runtime flows"* section
  from this file and enforces that every flow diagram cites an SR/LLR id. Those
  flows are **narrative and SR-cited — not registry-derivable** — so they need
  a disposition: move them into the dashboard as authored-and-checked content
  (the check follows them), or retire the obligation deliberately. **Do not let
  the file's deletion silently retire a check.**
- **`bootstrap.py`'s MAPPING and the scaffold surface change**, which is a
  downstream-visible change for adopters (a re-sync entry), and the standing
  lesson applies: *a scaffold-surface change is only verified by bootstrapping
  a scaffold.*

The earlier, narrower ruling this supersedes:

**RULED 2026-08-13q: the hand-authored architecture structure RETIRES — the
architecture becomes a DERIVED FACT.** The owner's reasoning: with the boundary
interfaces defined and tied to system requirements, and recursion allowed over
LLRs and interfaces, the structure is computable rather than authored. So the
boundary record is **generated** from `external.toml` (entities · boundary
interfaces · relationships) + `interfaces.toml` + the LLR/component recursion,
emitted into `docs/architecture.md` beside the existing generated blocks and
rendered in the dashboard's "How (SW architecture)" tab.

**This SATISFIES SN-040 rather than straining it.** Its ratified acceptance
asks that the record be *"kept with the architecture, not in session prose"* —
a generated architecture view is the strongest possible form of that: it cannot
drift, and `--check` freshness makes staleness a red. It also completes the
direction the file already had: **~1,402 of its 1,594 lines (88 %) are already
generated.**

**⚠ One boundary on "the entire structure" to confirm.** The file's ~192
hand-authored lines are not all structural. **Runtime flows** are *narrative
sequences*, SR-cited and checked by `check_flows.py` — an ordering of events
with a rationale, which no registry derives. The honest split (the same
by-KIND cut §1b drew): **structure derives** (entities, boundary interfaces,
relationships, module graph, component map — all registry-backed), **narrative
stays authored-and-checked** (Runtime flows, "Shape of the product"). Confirm
that reading, or rule the narrative out too and say what replaces
`check_flows.py`'s obligation.

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

**RULED 2026-08-13q: neither SPLIT nor WAIVE — the question dissolves into a
RE-TIER.** The owner: *"SRs must now scope only to their boundary interfaces,
which right now is much smaller, such that the current composition of SRs will
likely drop to LLRs."* Four of the six form-finding rows name internal modules
(SR-042 `gen_okf.py`, SR-050 `gen_trajectory.py`, SR-057 `schedule.py`, and
SR-130's serial trunk step — `trunk_step`, internal by construction under
decision 2), so they are **re-tier candidates, not split candidates**. Splitting
them would mint SR ids into rows about to leave the SR tier — precisely the
churn the 2026-08-13d tabling was avoiding. **The form rule applies to whatever
lands after the re-tier**, at whichever tier each obligation ends up.

**⚠ THE SCOPE ESCALATION THIS CREATES — the sitting should size it
deliberately.** WI-451 was scoped as *"re-state ~57 internal-naming SRs."* Under
this ruling it becomes **re-tier the SR registry against 7 crossings**. Order of
magnitude: 148 SRs today; a tier scoped to 7 crossings plausibly sustains a few
dozen, so **~100 rows may demote to LLR**. That is a different program, and it
carries two structural problems worth ruling before it runs:

1. **Every demoted SR needs a parent.** The join is SN→SR→LLR→TC; an LLR hangs
   off an SR. So each demoted row must find a surviving boundary SR to parent
   under — and the demotion also mints ~100 LLR ids, re-points their TC links,
   and re-homes `sn_refs` (LLRs do not carry them; the parent SR does).
2. **B-05 risks becoming a mega-node.** Because the Template is the deliverable
   and nearly every script ships inside it, most demoted rows parent under the
   *one* deliverable crossing — one node with ~100 descendants discriminates
   nothing. **The natural mitigation, and it brings the port list back in a
   legitimate form:** B-05's SRs decompose by **delivered capability** (the
   harness-verdict contract, the scaffold/MAPPING contract, the unattended-loop
   contract, the generators' contracts, the hook-floor contract), each a real
   obligation of the package with its own observable per §1R.6. Those are the
   old ports — no longer crossings, now *properties of the deliverable*.

**RESOLVED 2026-08-13s by the form rule (§3R).** The rule is *one shall per
row, against an interface at that row's own component level; a bundle is
legitimate if broken down in the component details.* So: the six rows are not
split now — **the rule is applied as rows are re-tiered**, and B-05's
bundle-ness is no longer a problem to design around (§3R). **Deferred to the
re-tier:** the per-row execution. **Still owed at this sitting:** nothing on
form; the census (WI-451 slice 1) sizes the program, and **no row count should
be committed before it runs.**

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

**Answering the owner's question — yes: this decision IS the architecture
decomposition**, at depth 1. P5 groups the ~55 shipped modules into four
components (CMP-006…009); under the OI-21 ladder a partition *is* the next
level's boundary declaration, so this is the rung below §1R's frame.

**⚠ Its sequencing is now in question (2026-08-13q).** Decision 8 makes the
architecture a *derived* fact — which does **not** retire this decision, because
the component assignment is a *chosen* input to that derivation, not an output
of it. But decision 9's re-tier changes what the partition is partitioning:
**~100 rows demoting from SR to LLR arrive needing `Component` values**, and
`LLR.Component` is exactly the cell P5 assigns. Ratifying the partition before
the re-tier means re-tagging afterwards anyway.

**So the real call is sequencing, and it is cheap either way** — `LLR.Component`
is a traced cell, so adopting or overturning opens **no re-attest window**
(pack §3's "cheapest decision in the pack" finding still holds).

**RECOMMENDATION, ruled 2026-08-13s (the owner deferred to it): DEFER
ratification — keep P5 provisionally adopted, warn-first, and do not touch it
until the re-tier lands.** Three reasons:

1. **The re-tier changes the input.** ~100 rows demoting SR→LLR arrive needing
   `Component` values. Ratifying a partition over the pre-demotion row set, then
   re-tagging, ratifies a picture that no longer exists.
2. **It costs nothing to wait.** The tags are already applied (149
   `LLR.Component` + 54 IF cells re-pointed; advisories 15 → 0). Warn-first
   means the machinery already behaves as if adopted; ratification only removes
   the "provisional" label.
3. **It does not block the thing you actually care about.** Your stated goal for
   the decomposition is *not duplicating behavior* — and pack §3's own
   constraint finding says the duplication is in the **copies**, not the
   boundaries: *one-home-per-behaviour is unsatisfiable by ANY partition of
   today's tree; the 12 behaviours live as 39 (behaviour, home) pairs across 16
   modules.* **WI-448 (the common-module program) is what deletes the copies**,
   and it can proceed against the provisional tags — it needs to know which home
   OWNS each behaviour, which the tagging already tells it. Deferring
   ratification does not defer the anti-duplication work.

**The one caveat to carry:** pack §3 says the partition and the common-module
program *"must land together"* — read precisely, that means the partition must
not be **ratified as final** while the copies still exist, because the straddle
numbers it was chosen on still move. Deferring is therefore the *consistent*
reading of that finding, not a violation of it. **Re-ratify after WI-448 and
the re-tier, on re-derived numbers.**

The full ranking, the four components as minted, and the accept-vs-overturn
costs follow below unchanged.

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

**RULED 2026-08-13r: THE ROSTER IS DETERMINED AT `DevStg-Boundary`.** Hats are
settled at the boundary rung — with the entities, not after them — which is why
this decision belongs to *this* sitting rather than drifting into execution.
The reason it coheres: a hat is a **question put on behalf of a concern**, and
the frame is where the concerns are enumerated. Downstream the same rule
applies — an adopter determines their roster at their own `DevStg-Boundary`.

**The coherence check this enables — does every declared entity have a voice?**
Mapped against §1R.1's locked frame:

| Entity / concern | Hat speaking for it |
|---|---|
| **EXT-003 Adopter** | `FIRST-RUN-ADOPTER` *(see the open question below)* |
| **EXT-001 session, as the unattended loop** | `UNATTENDED-OPS` |
| **EXT-001's local environment** (the dissolved OS/toolchain entities) | `CROSS-PLATFORM` |
| **EXT-001 session, reading B-03's surfaces** | `UX-DESIGNER` · `UX-ENGINEER` *(new)* |
| **EXT-001 session, as future maintainer** | `MAINTAINER` |
| cross-cutting (no single entity) | `SECURITY` · `TEST-ENGINEER` |

Every operational entity has a voice, and every hat traces to a concern the
frame names. That is the test a roster determined at this rung should pass.

**RULED 2026-08-13q: ADD a UX designer hat and a UX engineer hat** — *"for the
output html specifically is where they will play"* (`PROJECT_STATE.html`,
`open-items.html`).

**Answering the scope question: the roster is BOTH — it ships.**
`project-trajectory/registries/hats.template.toml` exists and `bootstrap.py`
scaffolds it to `docs/requirements/hats.toml`, so the six hats are a **starting
roster delivered to adopters** (B-05 content) *and* this repo's own live
instance. Under the kit's VALUES-vs-STRUCTURE rule the two may legitimately
diverge in *content* while the schema stays identical.

**Recommendation on the split:** add both hats to **this repo's** roster
unconditionally — the dashboard is a real, owner-facing UX surface with a
critique skill already pointed at it. For the **shipped** roster, add them too
but gate them, since not every adopter has a UI: an `applies_when` on a
rendering/UI tag keeps them **silent rather than falsely universal**, exactly
how `FIRST-RUN-ADOPTER` and `CROSS-PLATFORM` are already gated. Proposed rows
(owner text to confirm — a roster chosen by an agent and left unread is the
ceremony SN-036 exists to prevent):

- **`UX-DESIGNER`** — `applies_when = 'tags contains "render" or tags contains "ui"'`
  · *asks:* "Who reads this surface, what decision are they making on it, and does the layout put that first?"
  · *listens_for:* "A surface that renders every fact it has instead of the one the reader came for."
- **`UX-ENGINEER`** — `applies_when = 'tags contains "render" or tags contains "ui"'`
  · *asks:* "Does this hold up at the real widths, themes and content volumes — and what does it do when the data is empty, huge, or malformed?"
  · *listens_for:* "A view verified only by reading its generator, never by looking at it rendered."

Note the second is the standing lesson the `render-dashboard-critique` skill
exists for — *a concurrency diagram reads correct in source and wrong on
screen.*

**⚠ OPEN QUESTION (owner, 2026-08-13r): is `FIRST-RUN-ADOPTER` still necessary
if the template ships conventions and examples — and does it still apply to
this repo?** My assessment, for you to rule against:

- **On "it wouldn't apply to this repo any more":** under the locked frame it
  applies *more*, not less. The hat does not ask *"is this repo a first-run
  adopter?"* — it asks *"when we author this, could a stranger holding only the
  shipped package use it?"* That is a question about **B-05, the deliverable**,
  and this repo is the one authoring B-05. `EXT-003 Adopter` is a declared
  entity in the frame; cutting its hat would leave a declared entity with **no
  voice in review**, breaking the coherence check above.
- **On "the shipped conventions and examples already cover it":** they are the
  *answer*, not the *check*. Shipping examples does not stop a new requirement
  assuming knowledge that lives only in this repo's history — and the kit has a
  worked instance: `bootstrap.py`'s MAPPING omitted `schedule.py`, so **every
  fresh scaffold raised `ModuleNotFoundError` while this repo stayed green**,
  because the kit's own `scripts/` dir holds every file and this repo could not
  see what an adopter would. The standing lesson from it — *a scaffold-surface
  change is only verified by bootstrapping a scaffold* — is exactly this hat's
  failure class.
- **The half of the concern that SHOULD leave the roster.** Under §1R.6 the
  mechanizable half is now B-05's own contract: *the package exists, is
  complete and is consumable downstream*, verified by bootstrapping a real
  scaffold (`test_bootstrap`, `test_dogfood_sync`, the MAPPING-coverage guard
  that lesson produced). Moving it there is strictly stronger than a review
  prompt — the repo's governing principle, *prefer a constraint that makes a
  bad state unrepresentable over a check that detects it*. What **cannot**
  mechanize is the authoring-time half: *an undocumented convention, a step
  whose prerequisite is never stated.* No test sees that.

**Recommendation: KEEP it, and fix it rather than cut it.** Its `applies_when`
is *already broken* — it keys on a `scope` field SN rows do not carry
(SN-039's job), so its three `scope ==` clauses are **silent today**, not true.
Re-point it at the deliverable (a `tags contains "templates"`-style predicate
that actually fires) and let B-05's SRs carry the mechanizable half. **Cut it
only if** you judge the authoring-time half adequately covered by
`MAINTAINER` — a defensible call, but it should be made deliberately, and
`MAINTAINER` asks a different question (*why does this exist?* vs *can a
stranger use it?*).

**RULED 2026-08-13s: `FIRST-RUN-ADOPTER` is KEPT** (fix its predicate, per the
assessment above), and **aspect hats are ADDED for safety, legal and the other
common aspects — OFF BY DEFAULT.**

**How "off by default" works, and it needs NO schema change.** `hats.py`'s
`REQUIRED_KEYS` are exactly `applies_when · asks · listens_for` and it
**refuses any unknown key**, so there is no `enabled = false` to add without
changing a shipped script, its template and its tests. But the grammar already
provides the mechanism, deliberately: *"A FIELD THE COMPOSER DID NOT DECLARE
SATISFIES NO CONDITION … a hat keyed on a fact this project does not yet record
stays silent rather than firing on every decomposition."* So an aspect hat keyed
on **its own tag** ships silent and switches on the moment a project tags work
with it — opt-in by tagging, no dead code, no new field.

**⚠ Distinguish this silence from a defect, in the roster itself.** These hats
are silent **by design** (they wait for a tag). `FIRST-RUN-ADOPTER` is silent
**by accident** (it keys on a `scope` field SN rows do not carry). A future
reader must not have to guess which is which — say it in the roster's header
comment.

**ACCEPTED 2026-08-13u** — *"recommendations and proposals look sufficient."*
The rows below and the `FIRST-RUN-ADOPTER` predicate fix are the text
**WI-453** executes; the template-vs-this-repo split follows the recommendation
(UX pair unconditional here, render/ui-gated in the shipped starting roster).

**The rows (all five aspect hats ship OFF):**

- **`SAFETY`** — `applies_when = 'tags contains "safety"'`
  · *asks:* "How can this harm a person, property or the environment if it behaves incorrectly, and what requirement bounds that harm?"
  · *listens_for:* "A hazardous outcome with no requirement naming its bound, or a mitigation asserted with nothing verifying it."
- **`LEGAL`** — `applies_when = 'tags contains "legal"'`
  · *asks:* "What licence, contract or regulation constrains this, and does the decomposition record which obligation each part discharges?"
  · *listens_for:* "An obligation assumed to be someone else's, or a dependency whose licence terms nothing states."
- **`DATA-PROTECTION`** — `applies_when = 'tags contains "personal-data"'`
  · *asks:* "What personal data does this touch, on what basis, for how long, and who can reach it?"
  · *listens_for:* "Personal data crossing a boundary with no stated basis, retention limit or access rule."
- **`ACCESSIBILITY`** — `applies_when = 'tags contains "a11y"'`
  · *asks:* "Can someone using a keyboard, a screen reader, or a low-vision setting complete this — and is that stated as a requirement rather than hoped for?"
  · *listens_for:* "A surface whose acceptance names only how it looks to a sighted mouse user."
- **`PERFORMANCE`** — `applies_when = 'tags contains "perf"'`
  · *asks:* "What is the declared budget here, measured on what, and what happens when it is exceeded?"
  · *listens_for:* "A speed or size claim with no declared budget, or a budget with no measurement behind it."

*(`PERFORMANCE` pairs with the kit's existing NFR/perf layer and
`performance-budgets.template.csv`; `ACCESSIBILITY` pairs with the two UX hats
above — together they are the aspect set most likely to be switched on by an
adopter with a UI.)*

The existing six hats and the two honest limits follow below.

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

**RULED 2026-08-13q: the sign-off MECHANISM is unchanged** — *"anything above
the human approval rating is performed automatically, anything below pauses and
waits for approval."* That is `human_ratification_through` (the ordinal that
replaced the `attended`/`single-ratify`/`autonomous` enum) working as designed;
this decision does not re-open it.

**The owner's consequence, and it is the real finding:** *"all content generated
at each rung needs to have a designated element that can define if it's approved
or not, and that may have some missing pieces currently."* **Measured — there
are exactly two gaps, and the second is about to be created:**

| Registry | Approval element | Verdict |
|---|---|---|
| stakeholder-needs | `kind` | present *(a TYPE field doing double duty as maturity — the D-9 ladder's to fix)* |
| system-requirements · low-level-requirements · test-cases | `status` | present |
| open-items | `status` | present |
| components | `state` | present |
| work items | the **directory** is the status | present (by construction) |
| **hats** | **NONE** | ⚠ **GAP** — a roster row cannot be approved-or-not today |
| **interfaces** | `stability` | ⚠ **GAP IN THE MAKING** — decision 4's direction retires it, and nothing replaces it |
| **`external.toml`** (entities · boundary interfaces · relationships) | *does not exist yet* | ⚠ **DESIGN IT IN** — the frame's own rows must carry an approval element from the first commit, or the boundary is un-ratifiable |

**RULED 2026-08-13u: ONE shared status designation across every registry —
with per-registry SUBSETS, and change detection DEFERRED.** The owner: *"I
don't see another alternative in order to track these … Ideally they all hold
the same status designation, it's just that 'Founded' may not be applicable to
every registry"*, and *"for now don't worry about change detection like exists
on the requirement rows — that can be deferred down the line."* So:

- **One vocabulary, defined once** — the D-9 ladder's words (`Drafted` →
  `Approved` → `Founded`), so a reader learns one set for the whole repo and no
  registry invents a private synonym. This is why decision 12 and the D-9
  migration (sitting 3 §3) are **one program, not two**: the invariant is what
  D-9's vocabulary is *for*.
- **A registry may declare a SUBSET.** `Founded` — the rung that means
  *discharged by evidence below* — has no meaning where nothing hangs beneath a
  row, so an off-spine registry may legitimately use only `Drafted`/`Approved`.
  The subset is **declared per registry**, not left to inference, so a missing
  third value reads as *not applicable* rather than *not reached*.
- **Change detection is DEFERRED and that is a real simplification.** The
  spine's `Modified` state and its re-attest window stay a **spine-tier**
  mechanism; off-spine rows get approval **without** drift tracking for now.
  Nothing is being given up permanently — it is a later increment, and D-9's
  own hard coupling (drift-as-derived needs D-1's `TextHash` anchor, sitting 3
  §3.2) is exactly why deferring it here is the *consistent* call rather than a
  shortcut.

**How the three measured gaps close under this:** `interfaces.toml` takes the
shared vocabulary as `stability` retires (decision 4, same ruling);
**`external.toml` carries it from its first commit**, so entities, boundary
interfaces and relationships are ratifiable from day one; and the **hats roster
either takes it or is declared not rung-generated content** — it is owner text,
not derived, which is a defensible exemption *if stated* (WI-453 carries the
call).

The question as originally posed:

**What to rule:** that **every registry row a rung generates carries an approval
element** as a schema invariant, and how the three gaps close — the `external.toml`
schema mints one from day one (cheapest: the same closed `Status` vocabulary
D-9 lands, so there is one word across every tier); `interfaces.toml` gains that
same element as `stability` retires rather than after; and the hats roster either
gains one or is explicitly declared *not* rung-generated content (defensible —
it is owner text, not derived — but say so deliberately rather than by
omission). **This is the same class as the two unowned checkers** (SR→IF,
SN-033's need-cell check): a stated obligation with no mechanism, and the
cheapest moment to fix it is before the schema exists.

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

**⚠ AMENDED BY THE 2026-08-13k REFRAME (decision 1).** Under the owner's
re-drawn frame the third bullet **simplifies**: E12 and **N-02 are dissolved**
— authoring is the SESSION entity's ordinary hook-floor crossing, i.e. exactly
M-12/M-13 — so clause (b)'s SR anchors **M-07 alone** (the ONE deliverable
crossing to the ADOPTER), and the "inbound half" WI-442 never contemplated
turns out not to exist as a separate crossing. Clause (a)'s "boundary-actor
declaration" lands as the **SESSION entity row** in `external.toml` (decision
5) plus the M-12/M-13 IF rows. The rest of the order stands.

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
| [`2026-08-13-sitting-2-superseded-material.md`](../archive/plans/2026-08-13-sitting-2-superseded-material.md) | This brief's own ruled/superseded material, moved out 2026-08-13m to keep the live surface clean: the drafted §1 frame + §1a/§1b analysis, the 13k reframe long-form, and decisions 1/3/4/5/6's original questions. Rulings live in the log's Decisions; nothing in it is an instruction. |
