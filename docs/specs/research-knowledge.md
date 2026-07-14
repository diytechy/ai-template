# Design spec — Research track + durable knowledge layer

**Status: DRAFT — pending owner ratification (OI-9).** Branch:
`derived-gate-model`. Registered as **WI-138** (owner intake 2026-07-13 items
5+6 — [the intake brief](owner-intake-2026-07-13.md#research-knowledge)).
This doc is the spec-of-record; implementation WIs are filed from §8 **on
ratification**, not before.

## 1. The problem

Two owner items, one design gap:

- **Item 5 (TRIP research emphasis).** TRIP's plan/implement/release, multi-LLM
  review, and ARCHI.md-style memory are already covered here (PLAN/BUILD +
  gates; REVIEW-A/B cross-family; the generated `architecture.md` + OKF bundle).
  The genuine gap: a **first-class research task** — investigation at a defined
  compute level, producing *documented findings, not code* — with a
  grounded-second-opinion step. Today such work has no WI shape: it either
  squats inside a dev WI's context (lost at session end) or lands as an
  archive-bound note.
- **Item 6 (durable module specs / "where are the knowledge kits").**
  Research findings and durable per-module expectations have **no hand-owned
  home**: `docs/okf/` is generated-only (never a parallel source of truth),
  per-WI `docs/specs/` archive at close by design, and `log.md` is append-only
  evidence. Using any of them as module memory duplicates analysis across WI
  iterations — the owner's exact concern.

## 2. Prior art — the repo already names the answer

Don't invent a parallel system; the pieces exist and only lack kit support:

- **`docs/knowledge/<label>.md` is the resolved knowledge home** (Thread 52
  iter 6, archived in `docs/archive/AXES_AND_WORKSTREAMS.md` §4): reusable
  agent knowledge = a *skill*; **project-specific domain knowledge = a
  labelled pack**, many-to-many with components. Ratified then; never built.
- **The CMP registry already references it.** A `CMP-###` row's `Knowledge`
  cell holds `;`-joined refs (skill names, `docs/knowledge/` labels, URLs) and
  its optional `DetailDoc` names a per-component doc
  (process-options.md "Component layer") — the durable *module* hooks exist;
  nothing checks or scaffolds what they point at.
- **OKF's iron constraint** — a generated export, never authored — rules it
  out as the hand-owned home (its `--check` byte-compares against a
  regeneration).
- **The §6 tiering doctrine + `BuildTier` pin** already carry "who runs it";
  the reviewer dial (`docs/review-policy`) already carries "who checks it".

## 3. The model

One layer, two faces: **knowledge packs** (the durable store) and the
**research track** (the WI shape that fills them).

### 3a. Knowledge packs — `docs/knowledge/<label>.md`, made real

- **One topic per file; the filename is the label** the CMP `Knowledge` cell
  (and any prose) references. Hand-owned, reviewed like any doc.
- **A pack holds only what no registry can** — findings with their evidence,
  decision rationale, vendor/tool quirks, failed approaches (so they aren't
  re-tried), external references *with retrieval dates*. It **never restates**
  an SR/LLR/TC/IF row or the generated architecture map — it links ids
  (§3 anti-duplication, applied to prose).
- **Promotion rule (the spine stays authoritative).** A finding that hardens
  into a rule, constraint, or requirement is **promoted** via the §5
  change-intake flow (new/changed SN→SR→LLR rows); the pack keeps the *why*
  and the trail, the spine keeps the *what*. A pack is advisory context —
  it never gates.
- **A durable module spec = the CMP row + its refs.** Per-component
  expectations live where the component's identity already lives: the
  `CMP-###` row (`State`, `Knowledge`, `DetailDoc`), not a new
  `docs/specs/components/` tree — `docs/specs/` keeps its archive-at-close
  semantics.
- **Integrity, warn-first.** `trace.py` (which already validates CMP
  membership joins) learns to resolve `docs/knowledge/`-shaped `Knowledge`
  refs to real files — a missing pack is a **warning**, never a gate failure
  (skill names and URLs in the same cell are not checkable and stay
  unchecked). `check_docs.py` covers pack link/staleness hygiene for free once
  the packs are in the doc graph (a scaffolded `docs/knowledge/README.md`
  indexes them, so packs aren't orphans).

### 3b. The research track — a WI shape, not new machinery

- **A research WI is an ordinary `WI-###` row** (`Workstream=research`): its
  Done-when is a set of **named questions answered**; its Deliverable is a
  knowledge pack (durable findings) and/or a spec input — **never code**. It
  rides the existing loop (next-wi, BuildTier pin, review dial) with **zero
  coordinator changes**: no new run-phase, no new session type.
- **Defined compute level.** The row's `BuildTier` *is* TRIP's "defined
  compute level". Default **medium** (the owner's instinct: mid-tier agents),
  pinned per row; **strong** where the findings will shape a design the owner
  ratifies. The effortmining caution (process-options.md "Per-phase effort")
  is the boundary: a low tier *fabricates*, so the tier floor is medium, and
  the guard below is mandatory at every tier.
- **Grounded second opinion.** A research WI's review round (the existing
  `review-policy` dial; cross-family recommended, as for REVIEW-A/B) uses a
  **grounding charter**: verify the load-bearing claims — sources exist and
  say what's claimed, dates recorded, repo-facts checked against the repo —
  rather than reviewing a diff. Findings route per §5. Where a web tool is
  unavailable the reviewer says so and downgrades the claim to "ungrounded",
  never silently passes it.
- **When research runs — both entry points, both optional** (proportionality:
  an opt-in track, never a mandatory gate step):
  - **at PLAN / spec time** — a PLAN or design session files a research WI
    when a spec rests on a load-bearing unknown, sequencing it as a
    predecessor of the WIs that need the answer;
  - **at intake** — change-intake triage routes an inbound item to research
    first when the *question* is clearer than the requirement.

## 4. What the kit ships (surface changes)

1. **`docs/knowledge/README.md`** — scaffolded (bootstrap `MAPPING` +
   `test_bootstrap` lists): the pack contract (§3a) in one page + a pack
   index table.
2. **`trace.py`** — the warn-first `Knowledge`-ref resolution (§3a); fixtures.
3. **Process text** — a new `PROCESS_OPTIONS.md` opt-in section ("Research
   track & knowledge packs", *applies-when*: findings outlive the session that
   produced them / a spec rests on an unknown), cross-linked from the
   Component-layer section; **PROCESS.md gets at most a one-line pointer**
   (§7 "repo text is the durable memory layer" is the natural anchor —
   byte-budget-guard applies).
4. **Dogfood** — seed the meta-repo's own `docs/knowledge/` (first candidates:
   the agent-routing research now archive-bound in
   `docs/archive/AGENT_ROUTING_RESEARCH.md`; the effortmining findings) and
   reference them from the kit's CMP rows.

## 5. Rejected alternatives

- **`docs/specs/components/` chunks** — forks `docs/specs/`' archive-at-close
  semantics; the CMP `DetailDoc`/`Knowledge` hooks already exist.
- **An authored dir inside `docs/okf/`** — violates OKF's
  generated-never-authored constraint. (OKF may later *export* packs alongside
  registry pages — deferred, §8.)
- **A knowledge registry (CSV)** — Thread 52's ruling stands: labelled docs
  referenced by label; promote to a registry only if reuse forces it.
- **A new coordinator phase (`RESEARCH`)** — needless machinery; a WI row +
  BuildTier already expresses it.

## 6. Open decisions (ratify at OI-9)

1. **The home** — §3a as specced (`docs/knowledge/` + CMP hooks). *Rec: yes.*
2. **Tier default** — research WIs default `BuildTier=medium`, strong where
   design-shaping. *Rec: yes, with the grounding guard mandatory.*
3. **Where the ref check lives** — `trace.py` (registry data, warn-first) vs
   `check_docs.py`. *Rec: `trace.py` — it already owns CMP reference joins.*
4. **OKF export of packs** — now or deferred. *Rec: defer; revisit when a
   downstream consumes OKF.*

## 7. Risks

- **A second prose surface competing with the spine.** Mitigation: the §3a
  pack contract + promotion rule; Reviewer B's process/trace charter gains
  "a pack restating a registry fact is a finding".
- **Knowledge rot.** Mitigation: retrieval dates in packs, `check_docs
  --stale` coverage, warn-first ref check; packs are advisory, so rot never
  falsely gates.
- **Research WIs producing unactionable essays.** Mitigation: Done-when =
  named questions; the grounding review; WI-sized scope like any row.

## 8. WI breakdown (filed on ratification)

1. **Knowledge home** — `docs/knowledge/README.md` template + bootstrap wiring
   + scaffold tests (§4.1).
2. **Ref integrity** — `trace.py` warn-first `Knowledge` resolution + fixtures
   (§4.2).
3. **Process text** — PROCESS_OPTIONS section + Component-layer cross-link +
   PROCESS.md pointer + reviewer-charter line (§4.3, §7).
4. **Dogfood** — seed the meta packs + CMP `Knowledge` refs (§4.4).
5. *(deferred)* OKF pack export (§6.4).

## 9. Done-when (the campaign)

- [ ] This design ratified by the owner (OI-9).
- [ ] A fresh scaffold ships `docs/knowledge/README.md`; the kit's own
      `docs/knowledge/` holds ≥2 seeded packs referenced from CMP rows.
- [ ] `trace.py` warns (never fails) on a `Knowledge` ref naming a missing
      pack; fixture-tested both ways.
- [ ] The research-track section is in `PROCESS_OPTIONS.md` with its
      applies-when; PROCESS.md stays within its byte budget.
- [ ] A first research WI has run end-to-end: questions in the row, a pack as
      the deliverable, a grounded second-opinion review recorded.
