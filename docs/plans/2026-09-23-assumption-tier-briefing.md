# Briefing: the validation gap and the assumption tier

**Derived summary, not a source.** A listening-order digest of
[`2026-09-20-validation-gap-and-the-assumption-tier.md`](2026-09-20-validation-gap-and-the-assumption-tier.md)
as of commit `e7ca23e0` (after review round 4): its open questions, conflicts,
assessed options and recommendations. The plan is authoritative; where the two
differ, the plan wins. Each point names the plan section to dig into. IDs are
kept for lookup and expanded in parentheses; row meanings are quoted from
[`external.toml`](../requirements/external.toml).

## Glossary

**Tiers and terms**

- **SN**: stakeholder need, a human outcome. **SR**: system requirement,
  stated at the kit's interface. **LLR**: low-level (module) requirement.
  **TC**: test case. **IF**: interface row, a seam between components or across
  the boundary.
- **DA**: domain assumption, the new tier this plan proposes. A claim that
  carries an SR's machine-checkable result to the human outcome its SN names.
- **Rig**: a test stand-in that emulates a real party, such as the scripted
  fake model runner `FAKE_AGENT`.
- **Sitting**: a formal owner ruling session. Its rulings are Decisions
  entries in `docs/log.md`; the plan's short ids expand to the log's, so 13k is
  `2026-08-13k` (grep the log for it).
- **Stage arms**: the checks in `derive_stage` that decide whether a registry's
  rows let the derived stage advance.
- **DevStg-Boundary / -Arch / -Release**: rungs of the stage ladder. The
  boundary (context frame) is approved at DevStg-Boundary, interfaces at
  DevStg-Arch, and shipped evidence is recorded at DevStg-Release.
- **LOCKED**: `external.toml`'s rows change only by a sitting ruling.

**The context frame today**

| id | what it is |
|---|---|
| **Sitting 2** | 2026-08-13, *"the boundary, the operational context, and the structural rulings"* ([plan](2026-08-13-sitting-2-boundary-and-context.md)). It drew the present frame. |
| `EXT-001` | Development session: the human or LLM in a terminal, attended or the `agent-resume` loop, *"indistinguishable by rule"*, plus the local machine and working copy |
| `EXT-002` | Template: the delivered package (templates, registries, scripts, hooks, skills, launchers) |
| `EXT-003` | Adopter: *"the downstream team and their repository"* |
| `EXT-005` | Model provider API(s)/CLI(s): the services and runners behind every LLM, builder and reviewers alike |
| `B-01` | Governed writes in: edits admitted only through the git hook floor |
| `B-02` | Authority in: rulings, attestations, Status flips. It has no port of its own; it rides `B-01` as content |
| `B-04` | Guardrail verdicts out: hook-floor accept/reject, `subagent_gate` allow/deny |
| `B-05` | The Template leaving: the packaged deliverable and its scripts' contracts |
| `REL-001` | Template → Adopter: *"full template content provided and adopted into the adopter's repo"* |
| `REL-002` | Self-adoption: this repo's session adopts the kit, runs `agent-resume`, and generates `PROJECT_STATE.html`, `open-items.html`, `docs/status.md` and `docs/stage` for the human to read |
| `REL-003` | The LLM runner surface: rate limits, auth expiry, model retirement; review briefs out, findings in |

Spent ids (removed, never reused): `B-03` (the generated surfaces out, removed
by 13u), `B-06`/`B-07`/`EXT-004` (hosted CI and its crossings, removed
2026-08-16q), `B-08` (the `check_vendored` upstream fetch, removed by 13o).

## Where it stands

- A **proposal, not a ruling**. Most owner questions are answered, but nothing
  is built and `external.toml` is unedited (plan header).
- Four adversarial reviews found 24, 18, 5 and 7 problems. Rounds 1–2 found
  design flaws; rounds 3–4 found implementation-level gaps. **The round-4 fixes
  were not re-reviewed**: read them as the current position, not as verified
  (§12.5).
- **The problem.** Needs (SNs) are written about a person: a team gets a
  working process (SN-001), a reviewer trusts the chain (SN-002). Their
  acceptance checks are written about a machine reading: the scaffold runs
  green, the trace check finds zero orphans. The claim that bridges the two is
  written down nowhere, so nothing tests it. The plan's answer is to make those
  claims **DA rows** that SRs cite and TCs evidence (§1, §2).
- **Why it matters.** 69 of 79 SRs (87%) sit on `B-05` (the Template leaving),
  yet the outcomes the needs describe happen where a person operates the kit.
  The present frame ruled those crossings out (§1).

## 1. Conflicts with earlier rulings (§5.2, §5.5)

**Sitting 2 is reversed at its two premises:**

- **13k**: the human and the loop are one entity. *"Who-holds-authority is
  policy and record, never an entity split."* That is why `EXT-001` (development
  session) holds both.
- **13n**: the delivery frame. *"The system is the act of creating the
  guardrails and template contents"*; the kit using its own tools doesn't make
  them inputs.

**What rested on them:**

- **13u falls.** 13u removed `B-03` and declared `PROJECT_STATE.html`,
  `open-items.html`, `docs/status.md` and `docs/gate` *"not system outputs"*.
  The human reading them becomes a real **read** crossing under a new bundle id.
- **`REL-002` (self-adoption) shrinks** to the Transition hand-off alone: the
  Template installed into an operating environment. Its claims that invoking
  `agent-resume` is *"NOT an input"* and that the generated views are only
  surfaced go.
- **`REL-003` (the LLM runner surface) becomes a bundle.** Model providers were
  said to *"touch the SESSION, never the system"*; now the model runner is a
  crossing of the kit. Two parts survive: 13o's merge of the primary and
  reviewer CLIs into one entity, and the backoff obligation.
- **The hosted-CI cut (2026-08-16q) is partly reversed.** It removed hosted CI
  (`EXT-004`, `B-06`, `B-07`) because *"this template has no design control over
  an external CI"*. Design control still explains why SR-151/152 constrain only
  the shipped workflow file, but it no longer keeps CI off the frame.
- **13o is reversed.** It removed `B-08` because `check_vendored` *"would be run
  by the development environment"*. That reasoning was incomplete: the script
  fetches a pinned upstream URL, which is not a `B-01` governed write.

**Still open:** whether hosted CI returns as a party, and whether the
vendored-doc upstream earns an entity (this repo vendors nothing).

**`EXT-003` (the Adopter) is dropped.** The team becomes the new human-operator
entity, the repo becomes the operating environment, and `REL-001` (Template →
Adopter) merges into the single Transition hand-off. The id is spent.

## 2. Owner answers the reviews reopened (§12.1)

| Q | your answer | now proposed | dig in |
|---|---|---|---|
| Q8 (where DA rows live) | no new registry; put them in `external.toml` | **a dedicated `assumptions.toml`.** The approval ledger (`baseline_snapshot`) is keyed by file, so approving one DA in `external.toml` would re-bless any other drift in the LOCKED frame rows | §10.1 |
| Q11 (where an SR's need link comes from) | move the need link onto the assumption | **the SR keeps `sn_refs` and adds `da_refs`**; a DA's needs are derived from the SRs citing it. One IF serves several arguments: `IF-134` (the hook floor) carries the privacy SRs and the authority DA at once, so inheriting needs through it attaches the wrong ones. The change would also touch 123 refs in 54 files | §6.2 |
| Q3 / Q10 (frame vocabulary; derive or write it) | two or three frame words, written on the bundle | three words: **effect** (the outcome lands here), **coincident** (the SR's own result *is* the outcome), **bridged** (a DA carries it). `coincident` is an explicit waiver with a reason; **no label goes on a bundle**; absence means *unclassified*, never coincidence | §4 |
| Q6 (does a rig get its own crossing?) | no | agreed, and **no entity either**: the frame's `enabling` class means a runtime dependency, so rigs become `[rig]` rows in `assumptions.toml`, each naming the party it `emulates` | §5.3 |
| Q5 (may a test of an assumption stand alone?) | yes | intent kept, through a new TC `assumption_refs` field; `Verifies` (which points only at SR/LLR) is required only when that is absent | §7 |

Q8 and Q11 run directly against what you said and need your explicit
acceptance.

## 3. New questions, each with a recommendation (§12.1)

- **Q16, two frames in one view.** The **kit** frame (the kit in operation in
  a repo) and the **delivery** frame (this repo's build and release, emitting
  the Template through `B-05`). Membership is a `system` cell on each bundle,
  not a property of the party, because the human and the model provider take
  part in both (§5.1).
- **Q19, a `mediates` cell on `EXT-001`** (the narrowed development session,
  now just the machine and working copy), so an outcome landing on a session
  bundle counts as the human's (§5.4).
- **Q20, switch the stage arms on as a separate step.** Otherwise the first
  Drafted DA regresses the derived stage to Boundary by surprise (§10.2c,
  §11 C4).
- **Q22, evidence is a passing result, not the existence of a test.**
  Automated results join `docs/test/evidence`. Sampled and monitored
  observations get their own dated record with an expiry (Q25), kept off the
  approved TC (§7, §10.2l).
- **Q24, sampled evidence can only falsify.** A passing sparse sample proves
  nothing (5-user studies catch 55–99% of known problems). A DA backed only by
  samples clears the gate only with a declared sampling model, a narrowed
  `holds_when` (the conditions under which the claim holds), or a recorded
  `accepted_risk` (§7).
- **Q27, split the gate.** Maturity (DAs Approved and not falsified) is checked
  at DevStg-Boundary; evidence (current passing results) at DevStg-Release,
  after the harness has run. A single early gate would deadlock (§11 C5).
- **Q23, re-attest only approved-content cells.** `coincident`, `form`,
  `sampling` and `max_age` count as content. Link cells (`da_refs`,
  `assumption_refs`, `stakeholder_refs`) are traced pointers like `SN-Refs`, and
  don't re-arm approval (§10.2k).

## 4. Options assessed

**Approval identity (Q21, Q26; §10.1).** `assumptions.toml` holds two tiers
(assumptions and rigs), and `stakeholder-needs.toml` would hold needs and
stakeholders. Approval is keyed by file end to end, so approving one tier would
approve the other.

| option | cost | also fixes | verdict |
|---|---|---|---|
| tier-specific identity: path plus id column, through parsing, refusal, write scope and stamping | a real change to `baseline_snapshot` and its tests | the same hazard across `external.toml`'s three tiers (entities, bundles, relationships), which exists today | **recommended** |
| one tier per file: rigs and stakeholders in their own registries | two more registries | nothing else | simpler fallback |

**Interfaces (§9; Q17, Q18).** Your rule: a requirement's interface must be
defined or clearly assumed.

- Approving boundary IFs at DevStg-Boundary so SRs can cite them was
  **withdrawn**: it approves architecture before the requirements it serves.
- A `realizes` cell on IFs was **rejected**: IF rows deliberately state no
  requirement; the requirement is reached through the IF's owning module.
- Minting IFs to match the count (69 SRs on `B-05` vs 39 `B-05` IFs) was
  **rejected**: new IFs only for genuine seams, such as the dashboard, which
  has no IF row today.
- **Adopted:** allocation at DevStg-Arch. Each boundary IF names the DAs that
  bridge it (`bridged_by`), or carries a `coincident` waiver, or is flagged
  unclassified.

**Vocabulary (§4).**

- machine/world (Jackson & Zave): kept in the rationale only.
- solution/problem domain: draws the wrong cut.
- system-of-interest (ISO 15288): **adopted for the frames**.
- ODD, the operational design domain from automotive safety: **adopted for
  `holds_when`**.
- "design system": means a UI component library.
- control/effect: "control" collides with `B-02` (authority).

## 5. Risks and costs (§10.2, §10.4)

- **Human-held DA approval needs enforcement that doesn't exist.** The
  dispatcher's off-spine approval hold is dormant, so moving the
  `human_approval_through` dial to DevStg-Boundary won't stop an automated path
  on its own (§10.2h).
- **The authority DA's falsifier needs a validated loop provenance trailer** on
  every loop commit, so a Status flip on a human-held rung made by the loop can
  be detected. It doesn't exist yet (§10.2i).
- **Prose headroom:** `AGENTS.template.md` has 20 B left. This concept's prose
  goes in `PROCESS_OPTIONS.md`, `ADOPTING.md` or `EXAMPLE.md` (§10.4).
- **Adopters:** schema changes in C1, C3 and E are mandatory on resync; the
  gate (C5) is opt-in; resync entries are deferred until the model is firm
  (§10.4).
- **Sitting judgment:** classifying the 69 `B-05` SRs into the two frames. SRs
  about the kit in operation move to kit bundles; SRs about the package as a
  package stay on `B-05` (§5.1).

## 6. Recommended path (§11)

1. **C1, the sitting:** reverse the rulings above, redraw the frames, create
   `assumptions.toml` and the stakeholder list with their stage arms **off**.
2. **C2, write the DAs,** each a new Drafted claim. Every SR gets `da_refs` or
   a `coincident` waiver, plus its `form` (interface, assumption or
   package-wide). Warn-only.
3. **C3, evidence:** `assumption_refs` and `sampling` on TCs, starting with
   metamorphic tests (cheap, oracle-free).
4. **C4, activation:** re-attest the changed SRs and TCs, switch the arms on,
   accept the stage regression, approve DAs and rigs as one batch.
5. **C5, the gate,** opt-in.
6. **E, the interface extension,** any time after C4.

**Not proposed:** a new stage rung; deleting `B` rows; moving interfaces to
DevStg-Boundary.

## Decisions waiting on you

1. Accept or reject the five reopened answers (Q3/Q10, Q5, Q6, Q8, Q11).
2. Rule on the new questions (Q16, Q19–Q27).
3. Choose tier-specific approval identity or one tier per file.
4. Decide whether hosted CI and the vendored-doc upstream return to the frame.
