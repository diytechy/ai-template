# Briefing: the validation gap and the assumption tier

**Derived summary, not a source.** A listening-order digest of
[`2026-09-20-validation-gap-and-the-assumption-tier.md`](2026-09-20-validation-gap-and-the-assumption-tier.md)
after review round 5 and the owner's answers of 2026-09-23: its open
questions, conflicts, assessed options and recommendations. Decision states are
copied from the plan's §12.1. The plan is authoritative; where the two
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

**Owner accepted all five revisions, 2026-09-23** — recorded as DECIDED in the
plan's §12.1, including Q8 and Q11, which reverse the original answers.

## 3. New questions, as choices (§12.1)

Each one is set out as a question with its alternatives, what each alternative
costs, the plan's recommendation, and your response (2026-09-23). Items marked
**pending** are waiting on the answer given with them.

### Q16. How many frames does the depth-0 view draw?

| option | consequence |
|---|---|
| A. One delivery frame (today) | The crossings where a person gets value (reading the dashboard, operating the loop) stay outside the frame, so no assumption can land on them. This is the gap itself. |
| B. One operating frame only | There, the installed Template *is* the system, so it can't also be the system's output: `B-05` (the Template leaving) has nowhere to sit (review 1, finding 1). |
| **C. Two frames, kit and delivery (recommended)** | The kit in operation sits beside this repo's build and release. Each bundle carries a `system` cell, and a party can appear in both frames. Cost: the frame redraw, and sorting the 69 `B-05` SRs by subject (§5.1). |

**You:** agreed; see how it looks. **Decided.**

### Q19. How does an outcome that lands on the session count as the human's?

The narrowed `EXT-001` (development session) is just the computer and the
working copy, and the human becomes a separate entity. But the human never
touches the repo directly. Their edits travel through `B-01` (governed writes)
and the verdicts come back through `B-04` (hook-floor accept/reject), and the
party of both bundles is the *session*, not the human. The plan's reach check
requires an assumption to land on a bundle whose party is the stakeholder's
own party.

**Example.** A privacy need (SN-009) is a human outcome: *my private data never
lands in the repo.* The hook floor rejecting a commit is observable at `B-04`.
The assumption that carries that rejection to the human is something like
*"when the floor rejects a write, the person sees the reason and does not route
around it"*. That assumption lands on `B-04`, which is the session's bundle.
Without a link, the reach check says "this assumption lands on the computer,
not on the person the need is about" and flags it, even though the terminal is
exactly where the person experiences the rejection.

| option | consequence |
|---|---|
| A. No link | Every assumption about what a person experiences through their terminal fails the reach check, or has to be forced onto `B-02` (authority) or the read bundle, where it doesn't happen. |
| B. Make the human the party of `B-01` and `B-04` | Erases the distinction the redraw exists for: the machine writes and returns verdicts, and the person is behind it. |
| C. A second, human-facing copy of each session bundle | Twice the bundles for one path, with nothing to tell the copies apart (§5.4). |
| **D. One `mediates = "EXT-006"` cell on `EXT-001` (recommended)** | The reach check accepts a session bundle for a human need. Scope: only the session mediates, and only for the human operator. The risk is that it accepts *any* session bundle, so the assumption's own text still has to say how the person is reached. |

**Clarification: no LLM is involved.** After the narrowing, `EXT-001` is only
the computer and the working copy; the model provider is its own entity
(`EXT-005`). With `mediates` set, the outcome *does* count as reaching you, and
that is the recommendation. The question is only whether to add the cell. It
is needed because the reach check is a mechanical rule that compares party ids:
without the cell it sees "session ≠ human" and flags the assumption.

**The cell's real limit: it can't tell whether you were there.** During an
unattended overnight `agent-resume` run, the hook floor rejects a loop write at
`B-04` and no one is at the terminal. The assumption "the person sees the
rejection" still passes the reach check, because the check proves the
assumption points at the right place, not that a person was present. So that
assumption's `holds_when` has to say "while a person is attending the session".

**What `mediates` is and isn't.** It isn't sign-off: who must approve an
assumption is Q14's dial, and your approval is required. It only fixes a false
alarm in the automatic reach check, which otherwise reads your terminal's
crossings as "the computer's, not the person's".

**Residual, accepted knowingly.** The check can't tell whether a person was
present. An assumption that holds only while someone is attending passes it
anyway, so that judgment rests on your sign-off: its `holds_when` must say so.
An attendance cell with an advisory list was considered and dropped as
machinery your sign-off already covers. **Revisit if** an assumption is ever
falsified because an event happened unattended.

**You:** add `mediates`; no attendance cell or advisory; "no harm in seeing
where this leads". **Decided.**

### Q20. When do the new checks start moving the project stage?

"The checks" are the stage arms: the rules in `derive_stage` that stop the
derived stage at a rung while any row it depends on is Drafted
(`spine_rules.py:643-652`). The proposal adds two:

- a Drafted **assumption or rig** holds the stage at DevStg-Boundary;
- a Drafted **stakeholder** row holds it at DevStg-Needs.

This repo is at DevStg-Tests (`docs/stage`), so the first Drafted assumption
would drop it three rungs.

| option | consequence |
|---|---|
| A. On from the first row | Writing the first draft assumption drops the stage from Tests to Boundary without warning, and every later draft keeps it there until the batch is approved. |
| B. Never on | Assumptions never gate anything. They stay documentation, which is the state the plan exists to end. |
| C. Off until a deliberate activation step (the plan) | Rows are written warn-only (C2, C3). Activation (C4) re-attests the affected SRs and TCs, switches the arms on, states the regression in advance, and approves the assumptions and rigs as one batch. |
| D. Put the assumption arm at DevStg-Arch | The drop is smaller (Tests to Arch), but requirements would be approved before the assumptions they rest on, which reverses your ruling that the boundary and its assumptions are approved together. The review batch is the same size. |
| **E. Off, then approve and activate in the same commit (proposed 2026-09-23)** | The batch is reviewed while the arms are still off. Its approvals and the arm switch land in one reviewed commit, so no commit ever reads below DevStg-Tests. |

**What a drop does and doesn't do.**

- **DevStg-Tests is rung 5 of 0–7.** It means requirements and module
  requirements are settled and the test set is in work. Impl and Release sit
  above it.
- **A drop un-approves nothing.** The stage is derived as a minimum over the
  rows, so it jumps straight back once the batch is approved.
- **The review effort is the batch, whichever rung you pick:** the assumptions
  and rigs, the SRs that gain a `coincident` waiver or a `form`, and the TCs
  that gain a `sampling` policy. Nothing already approved is re-reviewed.
- **A visible drop switches off three checks, for the length of the window.**
  `check.py` selects its steps "at or above" the current stage
  (`check.py:1324`), and a Boundary reading is floored to DevStg-Reqs for
  selection. With this repo's own profile (`docs/stack.ini`) loaded,
  `check.py` has 34 steps:
  - 12 start at DevStg-Needs and keep running at any stage.
  - 3 start at DevStg-Tests: `smoke` (this repo's per-commit regression bar,
    declared in `docs/stack.ini`), `design-flows` and `trajectory`. **These
    are the ones a drop from Tests would switch off.**
  - 19 start at DevStg-Impl. They aren't selected at Tests today either, so a
    drop changes nothing for them.

  An earlier version of this briefing said two of 28, having counted without
  the repo's profile; review round 5 caught it.
- **Ordinary drafts can't cause a drop.** The selection stage is derived over
  settled rows only; drafts are excluded (WI-498, `check.py` `resolve_plan`).
  The drop happens in one case: a brand-new registry that exists but has no
  approved row yet, which the boundary rung reads as "the frame is declared and
  not yet approved" (`spine_rules.boundary_incomplete`). Option E never creates
  that state in a committed tree.

**You:** asked which checks (above); preferred a smaller drop. Chose E, "we'll
see how it goes". **Decided**, on the two-check count. With `smoke` included
the case for E is stronger, but **please reconfirm**.

### Q22 + Q25. What counts as evidence for an assumption, and where does it live?

| option | consequence |
|---|---|
| A. A test case existing counts (the first draft) | Contradicts PROCESS.md: `Approved` blesses a row's text, never that its tests pass. |
| B. Results written on the test-case row | Mixes the test's specification with its results, and every new sample re-arms a re-attestation of an approved row. |
| **C. Results only, in result records (recommended)** | Automated results join `docs/test/evidence`. Sampled and monitored observations get their own record, keyed by TC: outcome, observed-at, by whom or what, and expiry. |

**Expiry, as proposed.**

- **Automated results have no clock.** The existing evidence record is bound
  *by value* to the content it ran on (the spine registries plus the product
  and test trees). It goes stale the moment any of that changes
  (`kitlib/evidence.py:21-33`). Automated assumption tests inherit this.
- **Sampled and monitored results carry a `max_age`.** It's a policy cell on
  each TC, set per test and approved with it. Its only fixed value is your
  7-day floor: a human probe of the adopter experience might be good for a
  release cycle, a CI monitor for a week. The record also stores a digest of
  what it judged, so a check is due again when that changes or `max_age`
  passes, whichever is first; the sister plan's S6 uses the same rule. Past `max_age`, the assumption's evidence reverts to
  *specified*. A failing result counts as falsification evidence.

**Your condition: produced mechanically, outside an LLM.** Automated and
monitored results are written by a script that ran the check, so they meet the
condition. Two cases don't:

- a **human sample** is produced by a person. Recording it (an `Attest`) is
  mechanical; producing it isn't.
- the **render critic** (a vision model judging the dashboard, §8.3) *is* an
  LLM producing a verdict. The plan admits it only through a rig row plus a
  fidelity assumption that a periodic human sample can falsify.

That leaves one sub-choice open:

- (i) accept the plan's rig route for LLM verdicts;
- (ii) exclude LLM-produced results from evidence entirely, so the render
  critic evidences nothing;
- (iii) allow LLM verdicts only as falsifiers, like sparse samples.

**You:** option (i), the rig route, with a default expiry. Whoever writes the
test (usually the LLM) proposes its `max_age`, and it's approved with the TC.
There's a mechanical floor of **7 days**: a shorter `max_age` is refused. An
expiry only reverts the evidence to *specified*; it never falsifies. So a badly
tuned value costs a re-sample, not a wrong verdict, and values can be retuned
after the first expiries. **Decided.**

### Q24. How does a sparse human sample count?

Random 5-user studies catch anywhere from 55% to 99% of known problems
(Faulkner 2003), so a clean small sample says little. A failure says a lot.

| option | consequence |
|---|---|
| A. A passing sample counts as positive evidence | The gate can be passed by luck, and the high variance stays hidden. |
| B. Human-axis assumptions never gate | Honest but hollow: 24 of the 27 needs are human outcomes, so most of the tier would stay documentation. |
| **C. Samples can only falsify; three routes to clear the gate (recommended)** | A declared sampling model with an acceptance rule; a `holds_when` narrowed until an automated check covers it; or a recorded `accepted_risk`. |

**A worked example (SN-001, an adopting team gets a working process).**

- **The assumption:** "A team that scaffolds the kit and follows
  `ADOPTING.md` reaches its first filled, approved registry row without reading
  the kit's source."
- **The sample:** three people try it, and all three succeed. That doesn't
  show the assumption holds. Even if one team in four would fail, three
  successes in a row happen 42% of the time (0.75³).
- **If one of the three fails,** that is real evidence: the assumption is false
  as stated. The DA is marked `falsified`, and the report lists every SR and TC
  that leaned on it.
- **So what clears the gate?** One of three honest positions:
  1. **A sampling model:** "30 fresh attempts, at most 1 failure", which
     supports a claim of roughly 90%+. Too costly for people.
  2. **Narrow the claim:** `holds_when` becomes "the team runs the scaffold's
     quickstart unchanged". The scaffold rig then runs that quickstart in CI on
     every commit, which is automated evidence. The price is that the claim now
     says nothing about teams that deviate.
  3. **Accept the risk:** `accepted_risk = "No adopter population to sample
     yet; revisit at the first external adopter or any failed sample."` You
     sign it when you approve the DA.
- **Likely in practice:** 2 and 3 together. Automate the part that can be
  automated, and knowingly accept the rest.

The gate doesn't demand proof. It demands that each assumption states which of
those positions it takes.

**What a closer look is likely to turn up.**

1. **`accepted_risk` is the weakest link as specified.** It's an optional
   free-text cell with no expiry and no review date. Your signature on it comes
   only through the assumption's own approval (human-held under Q14). Most rows
   will probably take this route, so it may want an expiry or a re-review
   trigger, for example reopening whenever a sample fails or the need's text
   changes.
2. **Narrowing `holds_when` can hollow out the claim.** This is the mirror of
   the plan's rule that an over-strong assumption is a defect: an operating
   domain so narrow that no real use falls inside it. A reviewer has to ask
   whether the narrowed claim still serves the need.
3. **A real sampling model is heavy** for human probes. It fits measurements
   and rigs better. In practice the sampling-model route is for machines, and
   the other two routes are for people.

**You:** agreed; it's a trade-off between risk and a tenable path. **Decided.**

### Q27. Where does the assumption gate sit?

| option | consequence |
|---|---|
| A. One gate at DevStg-Boundary, for maturity and evidence | Deadlocks: passing results exist only after the harness runs, many rungs later. |
| B. One gate at DevStg-Release | Drafted or falsified assumptions pass through every earlier rung unchecked. |
| **C. Split (recommended)** | Maturity is checked at DevStg-Boundary: Approved, not falsified, landing on the right party, and a fidelity assumption naming an Approved rig. Evidence is checked at DevStg-Release. |

**Your condition: it's checked.** The gate (C5) is **opt-in**, with an
applies-when. So "checked" means this repo enables it, and then `derive_stage`
enforces both halves on every commit bar. Until C5 is on, both halves are
warn-only.

**You:** okay if checked. **Decided, on condition that this repo enables C5.**

### Q23. Which new cells force re-approval when they change?

| option | consequence |
|---|---|
| A. All new cells are approved content (the fail-safe default) | Every row a link touches re-arms a re-attestation. This is the 148-row noise `Boundary-Refs` was classified out of. |
| B. All new cells are traced | Policy cells like `sampling`, `max_age` and the `coincident` waiver would change without your sign-off. |
| **C. Split (recommended)** | Pointers (`da_refs`, `assumption_refs`, `stakeholder_refs`) are traced, and a changed `da_refs` routes to adjudication, as `SR-Refs` does. Prose and policy (`coincident`, `form`, `sampling`, `max_age`) are approved content. |

**Your condition: documented, and where does documentation end?** It ends at
one home and one mirror:

- **The home** is the classification table in `acceptance_record.py`
  (`SPINE_TRACED_CELLS` / `SPINE_APPROVED_CELLS`). Every existing cell's ruling
  already carries its reason inline there.
- **The mirror** is `docs/registry-machinery-reference.md` §10 ("the
  traced-vs-approved cell split").

The new cells get one line each in both places, in the same change. Nothing in
the AGENTS or PROCESS prose restates it.

**You:** okay if documented. **Decided, on condition that both entries are
written.**

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
- **Proposed** (Q18 is REVISED, awaiting your confirmation): allocation at
  DevStg-Arch. Each boundary IF names the DAs that
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

1. **C1, the sitting:** rule Q28 first (hosted CI, vendored upstream); reverse
   the rulings above, redraw the frames, create `assumptions.toml` and the
   stakeholder list with their stage arms **off**; land the sister plan's S3
   provenance cell if it is ruled with Q12.
2. **C2, write the DAs,** each a new Drafted claim. Every SR gets `da_refs` or
   a `coincident` waiver, plus its `form` (interface, assumption or
   package-wide). Warn-only.
3. **C3, evidence:** `assumption_refs`, `sampling` and `max_age` (7-day floor)
   on TCs, and result records with a judged-state digest, starting with
   metamorphic tests (cheap, oracle-free). Designed with the sister plan's S6.
4. **C4, activation, in one commit:** review the re-attestation batch and the
   DAs and rigs while the arms are off; then one commit carries the
   re-attestations, the approvals and the arm switch. No committed regression.
5. **C5, the gate:** opt-in for adopters, **enabled here** (your Q27 condition).
6. **E, the interface extension,** any time after C4.
7. **T, terminology,** any time: the SR prose wording (Q9) and LLR → design
   expectation (sister S2).

**Not proposed:** a new stage rung; deleting `B` rows; moving interfaces to
DevStg-Boundary.

## Decisions waiting on you

Regenerated from the plan's §12.1 after review round 5:

1. **Q20, reconfirm:** a visible drop would switch off three checks, including
   `smoke`, not two. Option E avoids the drop entirely.
2. **Q26:** tier-specific approval identity (recommended) or one tier per file.
   Q21 is superseded by it.
3. **Q28:** do hosted CI and the vendored-doc upstream return to the frame? A
   prerequisite of the C1 redraw.
4. **Q29:** does `accepted_risk` expire or reopen on a trigger, or stay until
   edited?
5. **Q30:** adopt the standards' enabling-system and stage vocabulary (low
   stakes).
6. **Confirm the plan's revisions** marked REVISED: Q18 (no interface minting,
   the relation stays derived) and the bundle rows (kept as named rows,
   membership derived).
