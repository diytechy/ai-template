# Briefing: the validation gap and the assumption tier

**Derived summary, not a source.** A listening-order digest of
[`2026-09-20-validation-gap-and-the-assumption-tier.md`](2026-09-20-validation-gap-and-the-assumption-tier.md)
as of commit `e7ca23e0` (after review round 4): its open questions, conflicts,
assessed options and recommendations. The plan is authoritative; where the two
differ, the plan wins. Each point names the plan section to dig into.

## Where it stands

- A **proposal, not a ruling**. Most owner questions are answered, nothing is
  built, and `external.toml` is unedited (plan header).
- Four adversarial reviews: 24, 18, 5 and 7 findings. Rounds 1–2 found design
  flaws; rounds 3–4 found implementation-level gaps. **The round-4 fixes were
  not re-reviewed** — read them as the current position, not as verified
  (§12.5).
- **The problem.** Needs are written about a person (a team gets a working
  process; a reviewer trusts the chain); acceptance is written about a machine
  reading (green scaffold; zero orphans). The bridging claim is written down
  nowhere, so it cannot be tested. The answer: make those claims **domain
  assumption (DA) rows** that SRs cite and TCs evidence (§1, §2).

## 1. Conflicts with earlier rulings (§5.2, §5.5)

- **Sitting 2 is reversed.** 13k (the human and the loop are one entity) and
  13n (the delivery frame) are overturned. What rested on them:
  - **13u falls** — the dashboard and status surfaces become a real *read*
    crossing (new bundle id; `B-03` stays spent).
  - **`REL-002` shrinks** to the Transition hand-off alone.
  - **`REL-003` becomes a bundle** — the model provider is no longer outside.
  - **Hosted-CI cut, partly reversed** — design control still explains why only
    the workflow file is constrained, but no longer keeps CI off the frame.
  - **13o reversed** — its reasoning was incomplete.
- **Still open:** whether hosted CI returns as a party; whether the
  vendored-doc upstream earns an entity.
- **The adopter (`EXT-003`) is dropped**: the team becomes the human operator,
  the repo the operating environment; the id is spent, never re-minted.

## 2. Owner answers the reviews reopened (§12.1)

| Q | your answer | now proposed | dig in |
|---|---|---|---|
| Q8 | no new registry; DA rows in `external.toml` | **dedicated `assumptions.toml`** — file-keyed approval would re-bless drift in the LOCKED frame rows | §10.1 |
| Q11 | move the need link onto the assumption | **SR keeps `sn_refs`, adds `da_refs`**; a DA's needs are derived. One IF serves several arguments (`IF-134`), and removal touches 123 refs in 54 files | §6.2 |
| Q3 / Q10 | frame vocabulary / derive or write it | three words (effect, coincident, bridged); `coincident` an explicit waiver; **no label on a bundle**; absence = *unclassified*, never coincidence | §4 |
| Q6 | rigs get no crossing | agreed, and **no entity either** — `enabling` means a runtime dependency; rigs are `[rig]` rows with `emulates` | §5.3 |
| Q5 | a W-test may stand alone | intent kept, via TC `assumption_refs`; `Verifies` required only when that is absent | §7 |

Q8 and Q11 run directly against what you said and need your explicit
acceptance.

## 3. New questions, each with a recommendation (§12.1)

- **Q16 — two frames in one view:** the kit in operation, and the delivery
  system; membership is a `system` cell on the bundle, not the party (§5.1).
- **Q19 — `mediates` on the session**, so an outcome there counts as the
  human's (§5.4).
- **Q20 — activate the stage arms as a separate step**, or writing the first
  Drafted DA regresses the derived stage by surprise (§10.2c, §11 C4).
- **Q22 — evidence is a result, not a TC's existence.** Automated results join
  `docs/test/evidence`; sampled/monitored observations get their own dated
  record with expiry (Q25), off the approved TC (§7, §10.2l).
- **Q24 — sampled evidence falsifies only.** A passing sparse sample proves
  nothing; a sampled-only DA clears the gate only with a declared sampling
  model, a narrowed `holds_when`, or a recorded `accepted_risk` (§7).
- **Q27 — split the gate:** maturity at DevStg-Boundary, evidence at
  DevStg-Release, so it cannot deadlock (§11 C5).
- **Q23 — re-attest only approved-content cells** (`coincident`, `form`,
  `sampling`, `max_age`); link cells are traced (§10.2k).

## 4. Options assessed

**Approval identity (Q21 / Q26, §10.1)**

| option | cost | also fixes | verdict |
|---|---|---|---|
| tier-specific identity (path + id column through parsing, refusal, write scope, stamping) | real change to `baseline_snapshot` | the same hazard in `external.toml` today | **recommended** |
| one tier per file (rigs, stakeholders in their own registries) | two more registries | nothing else | simpler fallback |

**Interfaces (§9; Q17, Q18)**

- Boundary IFs approved at DevStg-Boundary — **withdrawn**: architecture before
  requirements.
- A `realizes` cell on IFs — **rejected**: IF rows state no requirement; the
  relation is reached through the owner module.
- Minting IFs to match the count (69 SRs on `B-05` vs 39 IFs) — **rejected**:
  new IFs only for genuine seams.
- **Adopted:** allocation at DevStg-Arch; IFs name their bridging DAs
  (`bridged_by`) or carry a `coincident` waiver.

**Vocabulary (§4)** — machine/world: rationale only; solution/problem domain:
wrong cut; system-of-interest (ISO 15288): **adopted for frames**; ODD:
**adopted for `holds_when`**; "design system": means a UI library;
control/effect: collides with the authority crossing.

## 5. Risks and costs (§10.2, §10.4)

- Human-held DA approval needs **enforcement that does not exist** — the
  dispatcher's off-spine hold is dormant (§10.2h).
- The authority DA's falsifier needs a **validated loop provenance trailer**,
  which does not exist (§10.2i).
- **Prose headroom:** `AGENTS.template.md` has 20 B left; this concept's prose
  goes in `PROCESS_OPTIONS.md` / `ADOPTING.md` / `EXAMPLE.md` (§10.4).
- **Adopters:** schema changes in C1, C3 and E are mandatory on resync; the
  gate (C5) is opt-in; resync entries deferred (§10.4).
- Classifying the 69 `B-05` SRs into frames is sitting judgment (§5.1).

## 6. Recommended path (§11)

1. **C1 — sitting:** reverse the rulings, redraw the frames, create the new
   registries with arms **off**.
2. **C2 — write the DAs**, warn-only.
3. **C3 — evidence**, starting with the metamorphic subset.
4. **C4 — activation:** re-attest, switch arms on, accept the regression,
   approve DAs and rigs as one batch.
5. **C5 — gate**, opt-in.
6. **E — extension** any time after C4.

**Not proposed:** a new stage rung; deleting `B` rows; moving interfaces to
DevStg-Boundary.

## Decisions waiting on you

1. Accept or reject the five reopened answers (Q3/Q10, Q5, Q6, Q8, Q11).
2. Rule on the new questions (Q16, Q19–Q27).
3. Tier-specific approval identity vs one tier per file.
4. Whether hosted CI and the vendored-doc upstream return to the frame.
