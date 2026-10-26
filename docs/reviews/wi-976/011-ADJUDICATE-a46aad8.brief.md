You are an INDEPENDENT adjudicator holding ONE sitting for a lane checkpoint. It composes several judgements, each in its own section below. Each section is a complete brief for its kind: answer each one exactly as its section asks, with its own machine line. The sitting ends at its committed verdict: the acts its sections authorize are a later act turn taken from that verdict.

Write ONE verdict file at docs/reviews/wi-976/011-ADJUDICATE-a46aad8.md, with one heading per section, spelled exactly `## <kind>` (for this sitting: amendment;first-approval). Under each heading write that section's verdict lines and its machine line, and nothing for another kind. A section that asks for a `## Dispositions` draft takes it under its own heading.

End the file with exactly one machine line naming every section you judged:

    SITTING: JUDGED kinds=amendment;first-approval

Each section below says to commit its verdict file: commit this ONE file once, after every section is written, ending that commit with the trailer `WI: WI-976`, and stop there.

=== SECTION `## amendment` ===

You are an INDEPENDENT adjudicator launched by the unattended coordinator, wearing a DIFFERENT hat from whoever made this change. You are judging ONE question about an approved requirement row whose normative text moved after it was attested.

THE QUESTION, and it is the only one you answer:

    Did this amendment change the requirement's MEANING, or only its CLARITY?

CLARITY means: a reader who acted correctly on the OLD text would still act correctly on the NEW one. Wording, ordering, a typo, a term made consistent with the rest of the registry, a rationale expanded to say why — the obligation is identical.

MEANING means: some behaviour, limit, actor, scope or acceptance condition is different. A threshold moved. A case was added or removed. An actor changed. A "should" became a "must". If a correct implementation of the old text could FAIL the new text — or pass it while doing something the old text forbade — that is meaning, however small the diff looks.

Judge the CELLS BELOW and nothing else. You have no access to the session that made the change, and you must not go looking: an amendment's author is not a witness to their own intent.

--- ACCEPTED ANCHOR ---
docs/archive/last_approved — the approved text as a human last blessed it, each registry's copy as last written:
  - docs/requirements/system-requirements.toml: copied 2026-10-23 (commit afb57ae33)
  - docs/requirements/low-level-requirements.toml: copied 2026-10-25 (commit e592e5eee)
  - docs/test/test-cases.toml: copied 2026-10-25 (commit e592e5eee)
  - docs/requirements/stakeholder-needs.toml: copied 2026-10-04 (commit e33298c0e)
This is the text BEFORE the change below; it is not the change under judgement, and it could only have been written by copying a live registry in an approval commit.
--- AMENDED CELLS (before/after, per row) ---
- SR SR-161 (chain of SR-161)
  - AcceptanceCriteria
    - before: A decomposition round writes the perspective record beside its artifacts; a declared perspective applicable to the decomposition and absent from the record is reported; the record distinguishes not-applicable from considered-with-no-finding; the independent adequacy review reads the record rather than the authoring transcript.
    - after: For one completed decomposition round, the applicable perspectives resolve from the declared hats roster, the decomposition brief presents each applicable perspective's question, and the sitting's review record names an outcome for every one; the independent adequacy review reads that record.
  - Coincident
    - before: The need asks for each decomposition examined from every declared perspective; the machine-readable record of each perspective's decision, and the finding when an applicable one is missing, is that outcome, and whether the resulting requirements are adequate is left to independent review, as the need states.
    - after: The need asks that each decomposition round is reviewed against every applicable declared perspective; the sitting's review record naming each perspective's outcome is that outcome, and whether the resulting requirements are adequate is left to independent review, as the need states.
  - Rationale
    - before: Realizes SN-036 — a decomposition produced from one perspective can look complete while omitting security, operations or first-use failures, and the omission is invisible unless the record names what was considered. SN-036 had no citing SR. The declared-perspective inventory is the ruled hats roster; the record proves coverage and provenance while adequacy stays with the independent review, exactly as the need partitions it.
    - after: A decomposition produced from one perspective can look complete while omitting security, operations or first-use failures. The hats roster and the planning briefs already supply the applicable questions, and the sitting's review record preserves their outcomes; a separate machine-readable coverage record and checker would duplicate that review without improving its adequacy judgment. Hat-Refs remain the row-level provenance for perspectives that raised a requirement. This applies the owner ruling of 2026-09-06, re-affirmed 2026-10-13.
  - Requirement
    - before: The delivered planning content shall leave, with every decomposition it produces, a machine-readable record of the declared review perspectives — each perspective's applicability decision and the requirements or explicit no-finding it produced — such that an applicable declared perspective missing from the record is a reportable finding.
    - after: When a decomposition round is reviewed, the delivered planning content shall provide every applicable declared perspective's question in the decomposition brief and require the sitting's review record to name the outcome for each perspective.
  - Title
    - before: Decompositions carry a perspective record
    - after: Each decomposition round is reviewed against its applicable perspectives
  - Verification
    - before: Test
    - after: Inspection
- LLR LLR-183 (chain of SR-161)
  - Detail
    - before: The machine-readable half of the perspective record, sited on the row rather than beside it. spine_carrier declares hat_refs (column Hat-Refs) as an OPTIONAL key on the SR and LLR tiers, a typed array of hat roster NAMES; the roster name is the id space, and the C-###-style clause numbering that appears in eight rationale cells is prose that resolves against nothing. Absence is NOT RECORDED and never no-perspective-applied, which is why no rule anywhere requires the cell to be present. trace.load_hat_names reads the roster's table keys only - hats.py stays the sole validator of roster CONTENT, and this reader answers the one question that module answers for nobody else, is this name declared - degrading to the empty set for an absent or unparseable file so the whole rule goes vacuous rather than reporting every row as dangling. trace.hat_findings splits severity the way the boundary rule does: a name the roster does not declare is a finding in the --strict failure set under its own class label, while coverage and the roster's own unattributed hats are single advisory summary lines that never gate. trace.effective_hats derives a design row's effective set as its own refs unioned with its SR parents', so the LLR cell holds only what its own decomposition raised and a dangling parent contributes nothing rather than raising. check_trajectory classifies Hat-Refs TRACED at both tiers, which is what keeps the cell off the re-attest window and out of the snapshot drift basis. NOT DISCHARGED, stated in the debt-stating pattern this tier uses rather than left to be discovered: the parent asks for a record that distinguishes NOT-APPLICABLE from CONSIDERED-WITH-NO-FINDING, and this cell expresses neither - both are facts about a decomposition, while this cell is a fact about a row. Applicability is separately DERIVABLE from the roster's own predicates, so storing it here would store a derived fact and let it go stale; the no-finding half is a per-decomposition artifact, built under LLR-297.
    - after: The row-level provenance part of perspective review, sited on the row rather than beside it. spine_carrier declares hat_refs (column Hat-Refs) as an OPTIONAL key on the SR and LLR tiers, a typed array of hat roster NAMES; the roster name is the id space, and the C-###-style clause numbering that appears in eight rationale cells is prose that resolves against nothing. Absence is NOT RECORDED and never no-perspective-applied, which is why no rule anywhere requires the cell to be present. trace.load_hat_names reads the roster's table keys only - hats.py stays the sole validator of roster CONTENT, and this reader answers the one question that module answers for nobody else, is this name declared - degrading to the empty set for an absent or unparseable file so the whole rule goes vacuous rather than reporting every row as dangling. trace.hat_findings splits severity the way the boundary rule does: a name the roster does not declare is a finding in the --strict failure set under its own class label, while coverage and the roster's own unattributed hats are single advisory summary lines that never gate. trace.effective_hats derives a design row's effective set as its own refs unioned with its SR parents', so the LLR cell holds only what its own decomposition raised and a dangling parent contributes nothing rather than raising. check_trajectory classifies Hat-Refs TRACED at both tiers, which is what keeps the cell off the re-attest window and out of the snapshot drift basis. Per-decomposition coverage is discharged by the existing review path: applicability derives from the roster's predicates, the decomposition brief presents every applicable hat's question, and the sitting's review record names each outcome. Hat-Refs retain their narrower role of identifying the hats that raised a row; storing applicability or no-finding outcomes in this cell would duplicate review facts and let them go stale.
- TC TC-178 (chain of SR-161)
  - Expected
    - before: Satisfies the acceptance folded into LLR-183 (parent SR-161)
    - after: Satisfies LLR-183's Hat-Refs provenance, name-resolution, severity and effective-set mechanics; SR-161's perspective-review acceptance is inspected by TC-211.
- SR SR-165 (chain of SR-165)
  - Rationale
    - before: Realizes SN-040 — a free-form partition leaves no record of the alternatives weighed, so the next reviser cannot tell load-bearing boundaries from accidents; the record is what lets the choice be re-examined. SN-040 had no citing SR, even as the P5 partition work performed exactly this record. Reproducibility is stated as a recomputation from the record's own declared inputs, not as a reviewer re-running a model session, because only the former can fail — the SR-161 form applied to the partition instead of the perspective set. B-05 alone: the human ruling is an element the record must carry, not an observable the system states at the authority input, which is SR-139's and SR-140's ground.
    - after: Realizes SN-040 — a free-form partition leaves no record of the alternatives weighed, so the next reviser cannot tell load-bearing boundaries from accidents; the record is what lets the choice be re-examined. SN-040 had no citing SR, even as the P5 partition work performed exactly this record. Reproducibility is stated as a recomputation from the record's own declared inputs, not as a reviewer re-running a model session, because only the former can fail. B-05 alone: the human ruling is an element the record must carry, not an observable the system states at the authority input, which is SR-139's and SR-140's ground.
- TC TC-211 (chain of SR-186)
  - Expected
    - before: A child within a required tier with no independent decision or verification purpose is an Inspection finding; otherwise the review records that independent value and why further splitting stops.
    - after: The actual review record names every applicable perspective's outcome, each child within a required tier has an independent decision or verification purpose, and the record explains why further splitting stops; any omitted outcome or purposeless child is an Inspection finding.
  - Inputs
    - before: docs/test/inspection-procedures.md;SR-186;docs/ai-template-redesign-2026-09-05-codex/DECOMPOSITION-AMENDMENTS.md;docs/ai-template-redesign-2026-09-05-codex/DECOMPOSITION-AMENDMENTS.perspectives.toml
    - after: docs/test/inspection-procedures.md;SR-161;SR-186;docs/requirements/hats.toml;docs/reviews/wi-976/011-ADJUDICATE-a46aad8.brief.md;docs/reviews/wi-976/011-ADJUDICATE-a46aad8.md
  - Method
    - before: Follow the decomposition proportionality inspection in docs/test/inspection-procedures.md#decomposition-proportionality-inspection; inspect the complete chain and an extra paraphrasing child.
    - after: Follow the decomposition proportionality inspection in docs/test/inspection-procedures.md#decomposition-proportionality-inspection; inspect one actual completed decomposition review record, its complete chain, and an extra paraphrasing child.
- SN SN-036
  - Acceptance
    - before: Each decomposition has a machine-readable record of the declared perspectives, the applicability decision for each perspective, and the requirements or explicit no-finding result produced from it. A check reports any applicable declared perspective missing from that record. The record proves coverage and provenance; an independent review judges whether the resulting requirements are adequate.
    - after: Each decomposition round is reviewed against every applicable declared perspective, and the review record names each perspective and its outcome. The record demonstrates coverage and provenance; an independent review judges whether the resulting requirements are adequate.
--- JUDGED TEXT (the identity of each row's approved text shown above) ---
JUDGED-TEXT: SN-036 sha256:64145cce5e7dc3c9
JUDGED-TEXT: SR-161 sha256:43f1bab901f97732
JUDGED-TEXT: LLR-183 sha256:cbbf28889806ffb8
JUDGED-TEXT: TC-178 sha256:64436fe6d9e3230e
JUDGED-TEXT: SR-165 sha256:ecffc231d34d29bd
JUDGED-TEXT: TC-211 sha256:2d784feadd0ebac4
--- END ---

Method:
- Read the BEFORE text and write down, for yourself, the concrete obligation it imposes — what a builder must do, what a test must check.
- Read the AFTER text and do the same, independently.
- Compare the two obligations, not the two paragraphs. Diff noise is not the subject; the obligation is.
- When the two obligations differ AT ALL, the answer is `meaning`. Fail toward `meaning`: a wrongly-kept attestation is a silent false claim that a human blessed this text, and that is the failure this rung exists to prevent. A wrongly-owed re-attest costs one sitting.
- If the diff is mixed — one cell clarified, another moved the obligation — the answer for the ROW is `meaning`, and you say which cell carried it.

Whether a `MEANING` row's new text is one you would bless — or recommend to the owner — is judged by the questions for its tier, the same ones a first approval puts. A `CLARITY` verdict owes them nothing new: the obligation is the one already blessed.

## 0. Every row — read the chain, not the row

- For each row, state to yourself the obligation it imposes: what a builder
  must do, what a test must check. A row you cannot restate as an obligation is
  not ready.
- Read UPWARD. Does the parent it points at actually call for this? A
  decomposition row that answers a requirement nobody made is scope, not
  detail.
- Read SIDEWAYS. Do the siblings together cover what the parent asks, without
  overlapping into each other's decisions? One decision per row.
- Read DOWNWARD. Do the test cases that claim to verify this row verify what it
  actually says — and does anything it says go unverified?
- Read the wording as a closed obligation: a "should" that means "must", a
  threshold with no units, an actor left unnamed, an acceptance condition
  nobody could observe. Each is a finding that sends the row back, not a note.
- **Name only what the row's tier may name.** No row's text names an
  implementation carrier (a code file, function or symbol). A shipped boundary
  artifact (a registry, template, config file or launcher) may be named at the
  LLR and TC tiers only; SN and SR rows name no file in any cell, acceptance and
  rationale included. An approved cell keeps its approved text verbatim, names
  included, until it is amended through its authority, and an amendment adds no
  name the rule forbids.

## 1. At SN intake — answer these before the need is approved

A defect admitted here becomes a whole subtree of need-less requirements later.
Questions:

- **(a) Does this need carry the TAGS that reach its governing perspective?**
  Hats fire on declared fields; an undeclared field satisfies no condition.
  Use `python scripts/hats.py applicable --tag <tag> ...` and a check of the
  actual brief to verify the intended questions reach this need. The audit's
  strict finding detects unknown predicate tags, not adequacy of decomposition.
- **(b) Is every load-bearing clause in the NORMATIVE text?** A safety or bound
  or authority clause living in the `why`/rationale cell is not derivable: a
  deriving team reads the need and the acceptance, produces nothing for that
  clause, and the SR that *does* carry it reads need-less forever. Ask of each
  clause: **if a stranger derived only from `need` + `acceptance`, would this
  obligation appear?** If not, move it up into the normative text.
- **(c) Is the quality bar written down, or is it in someone's head?** "A reader
  can see progress" is not "the view is legible, uniform and operable". If a
  perceptual or quality obligation is wanted, **the need that wants it has to
  exist**; otherwise the requirements built on it are underivable from every
  declared input, and no amount of downstream rigour will rescue them.
- **(d) Would a blind reader recover the intended obligations from the text
  alone?** The honest test of a need. Where the answer is no, the defect is in
  the need — file it as a needs defect, not as an SR problem.
- **(e) Does the acceptance intent name an INSTRUMENT?** The no-concrete-artifact
  rule reaches this tier too (owner directive 2026-08-18, extending it from SR up
  to SN), and it bites hardest here: the SN `acceptance` cell is where a need
  quietly becomes a sentence about a file. "`trace.py --strict` reports zero
  orphans" fixes a *stakeholder outcome* to one script — it cannot survive the
  script being re-carried, and the stakeholder it exists for cannot validate a
  claim about a file they have never opened. Write the observable **condition**
  ("the strict traceability check reports zero orphans") and let the carrier be
  named where carriers belong: no SN cell names a file, `why` included (§0's
  naming rule), so a carrier the need seems to require is named at the LLR or
  TC tier, or cited by a registry **id**. A **declared vocabulary** token (a dial
  name, a status word, a flag) is NOT waivable naming and needs no token, because
  it is not a carrier. A **provenance** citation is not a carrier either — and it
  does not belong in the cell at all (§6).

## 2. At SR derivation — per row

- **(a) One decision per row; one home per method** (`docs/process.md` §3). A row
  that decides both *which artifact* carries a capability and *what it does* is a
  tiering defect, not a style choice. Two rows sharing one interface identity is
  the same defect seen from the other side.
- **(b) Voice.** SN and SR alike state the delivered capability or the artifact
  **class** ("the delivered harness", "the launchers at the repository root") —
  one rule, two tiers, since the 2026-08-18 directive. The concrete
  name belongs one tier down — LLR `Module`, TC `Evidence` — and never in an SR
  cell, acceptance included (§0's naming rule); where acceptance genuinely needs
  an anchor, it cites a registry **id**. Acceptance criteria carry the **observable condition and its
  threshold** (Volere's *fit criterion*: an objective measure of the
  requirement's meaning) — *what would be observed and where the pass/fail line
  falls*, while *where and how* it is observed is the TC's.
- **(b2) Pick the EARS pattern from the OBLIGATION, then write the row.** The
  question is not "which keyword sounds right" but *what makes this requirement
  apply*: always (ubiquitous) · a discrete event starts it (`When`) · it holds
  for the duration of a state (`While`) · the trigger is a fault or misuse
  (`If … then`) · it applies only where an optional feature or declaration is
  present (`Where`). Three traps, all seen here:
  - **The buried condition.** `shall, during an unattended run, refuse…` states
    the same condition where no reader and no tool looks for it. Front it.
  - **A near-miss keyword.** "Before X…", "For work declared…", "During…" are
    conditions outside the pattern; `trace.py` warns on the opening, and the
    fix is to name which of the four it actually is (a *Before* is almost
    always a `When`; a *For <declared kind of work>* is almost always a
    `Where`).
  - **A condition that is really a response qualifier.** "fail that gate when a
    required tool is missing" belongs after the `shall` — it says *what the
    response is*, not *when the row applies*. Fronting it would change the
    obligation. This is why the checker warns rather than gates: only you can
    tell those two apart.
- **(b3) Does a joint-delivery row still state behaviour at a BOUNDARY?** Read
  every requirement named in `Delivered-With` and the assumptions each sibling
  cites directly. Check that their obligations and premises align around the
  shared need; never import one sibling's assumptions into another. Then apply
  the tier test: a row whose own output crosses a boundary is a real SR even
  when siblings complete the need with it, while a row whose output crosses no
  boundary and is consumed only by a sibling is a design decision and belongs
  at LLR. The shared-need checker is a detector; alignment and tier remain the
  adjudicator's judgement.
- **(c) If the obligation arrived through a lens rather than the need's text,
  RECORD the lens.** This is DO-178C's **derived requirement** class: content
  beyond what the parent demands, legitimate *because* it is (i) recorded as
  derived in a cell something reads, (ii) carrying a rationale that argues the
  deriving lens — the hat, the design
  constraint, the implementation fact — and (iii) fed back upward so the
  need owner sees it. Name the deriving hat in **`Hat-Refs`** (roster names; the
  cell IS the row's perspective record, and a name the roster does not declare is a
  finding) and argue it in `Rationale`. A prose label alone is not the record: it
  resolves against nothing, so nothing can tell a retired hat from a live one.
  **Never silently trace a derived row to a
  parent whose text does not demand it**: that is the single most common way a
  spine acquires structure nobody asked for and nobody can audit.
  - A row derivable **only** through a hat that ships switched OFF must say so.
    An obligation whose only lens is unreachable is a roster finding, not a
    licence — the label makes it reviewable; it does not make the row wanted.
- **(c2) Fill `Hat-Refs` as you mint the row, by the `listens_for` test — and
  leave it EMPTY when nothing passes.** (c) is the strongest case for the cell,
  not the whole population: a row can be attributable to a perspective without
  having been *derived* through one. The one test, stated so a later reader can
  falsify a cell rather than re-argue it: **attribute a hat only where THAT
  hat's own `listens_for` names a failure THIS row prevents.** The reading it
  displaces is "which lens could be held up to this row" — under that one a
  roster whose hats are mostly `always` puts every name in every cell and the
  column discriminates nothing. So read the failure classes instead of
  recalling them: `python scripts/hats.py list` prints each hat's `asks` and
  the `listens_for` it exists to catch, and `hats.py applicable --tag <tag> …`
  narrows to the ones a given context must face.
  - **An empty cell is an answer, and often the right one** — it reads *not
    recorded*, never *no perspective applied*, so it claims nothing. Two shapes
    earn it after you have looked: a row that names a hat in order to **refuse**
    it as a basis (the refusal is `Rationale`'s job — writing the name into
    `Hat-Refs` would assert the opposite), and a row whose attribution's
    **subject is gone**, where re-pointing the cell at a deleted mechanism is
    exactly the staleness the cell exists to make mechanical.
  - **Calibrate against the row's own argument.** One name is the common case.
    If a cell is heading for three, check whether the row really states three
    failures or whether the extras are stated by sibling rows — the hat belongs
    with the row that carries the obligation, not with every row nearby.
  - **Coverage is warn-only forever, in both directions**, and neither advisory
    is a quota: rows attributable to no declared perspective can be honest, and
    a hat attributable to no row is evidence about the ROSTER — a charter this
    project files no work in — not a hole to fill by attributing it somewhere.
  - **Which tiers carry it:** `SR` and `LLR` only. `SN` states the need a hat is
    a lens *on*, and `TC` records how a claim is checked; neither is a place an
    obligation is attributed, and neither schema declares the key.
- **(c3) In a decomposition round, the review record names each applicable
  hat's outcome.** `Hat-Refs` cannot say that a perspective was weighed and
  found nothing, and no file beside the decomposition says it either. A round
  that adds an SR under a need, or amends an approved need, carries each
  applicable hat's question in its brief, and the sitting's verdict, the
  review record, names every one of them once: the rows it raised, by their
  `Hat-Refs`, or no finding with the reason. A missing outcome is a finding
  for the review, never a coverage gate, and no check counts the outcomes.
  Whether each outcome is adequate is your judgement as adjudicator.
- **(d) The advisories are detectors, not caps.** `scripts/trace.py` warns —
  never gates — on (i) an SR `Requirement` naming a concrete `.py` artifact,
  (ii) two SRs naming the same artifact token, (iii) an SN `acceptance` naming a
  concrete artifact (a wider vocabulary than the SR arm's — scripts, configs,
  generated pages — because the need tier's instruments are mostly not scripts;
  `.md` is deliberately excluded, since a document named in a cell is usually a
  citation), (iv) a direct-LLR fan-out over the declared bound (`SR_FANOUT_MAX`,
  default 7), (v) an opening that states a condition outside the four EARS
  keywords, and (vi) an absolute in a need, requirement or design cell whose
  domain names nothing from a closed list (below). There is no shared-artifact
  census at SN: two needs may honestly
  describe outcomes one file happens to serve without either deciding anything
  about it. A bound is deliberately
  not a cap: a hard cap invites merging two LLRs into one to slip under it,
  hiding the defect the number exists to surface. Clearing one is a **recorded
  per-row re-stamp** — the waiver token in the tier's reason cell (`Rationale`
  at SR, `why` at SN) for an approved cell's kept name (§0), never for a new
  one, the
  `fan-out re-stamp: <reason>` phrase for fan-out — and the reason must be one a
  later reader can **argue with**. "Accepted" is not a reason.
- **(d2) Is every absolute's domain really closed?** An absolute ("never",
  "always", "every", "any", a clause-opening "no") is a promise every child keeps
  under every condition. The advisory is silent when the words after it name a
  registry, an id or a declared set, and that silence is lexical: ask whether the
  named domain is one the system controls and someone actually declares, and
  whether an unnamed one ("every commit", "each session") is closed anyway. Over
  the open world or open time ("in every repo", "never silently") it is a premise
  that can be sampled, not tested: bound it, or carry it as an assumption row. In
  a need, a prohibited MECHANISM ("never from prose") is a design decision; move
  it down a tier. Only then waive, as `recorded waiver: <reason>` in the reason
  cell. Test cases are out: they state a method, not an obligation.
- **Also ask:** does this row state a *package-wide property* (right-sizing,
  proportionality, one-definition-of-passing, refusal legibility)? Those are the
  rows a per-capability decomposition systematically misses — they end up as
  secondary clauses in nine rows and the subject of none.

## 3. At LLR and TC

- **An LLR states its contract in words that survive a refactor.** Its text
  states the observable obligation: the inputs it takes, the outcome it
  produces and where it refuses, so a refactor that keeps the behaviour keeps
  the row true. It names no implementation carrier (a code file, function or
  symbol), and §0's naming rule says which tiers may name a shipped boundary
  artifact. Do not launder a concrete name upward
  into the SR to keep the LLR abstract. The traced `module` and `code_symbol`
  cells are trace homes, not row text: they stay filled and binding while the
  schema requires them (`trace.py --strict-schema` requires both;
  `check_doc_refs --strict` binds the symbol), so never return a row for
  keeping them. No `shall` in an LLR — the SR states the obligation, the child
  decomposes it.
- **A child adds detail.** If the LLR would merely re-word its parent, link
  instead. `trace.py`'s paraphrase advisory is lexical and warns forever; the
  judgement stays yours.
- **Replace an unsuitable design through the normal amendment route.** If the
  parent outcome remains sound but the LLR's mechanism causes the problem,
  compare the old/new design, retained parent clauses and behavioral regressions,
  affected trace/evidence/work references, and the code that becomes removable.
  Amend the LLR and its mechanism-specific verification together; an Approved
  LLR does not require keeping an obsolete shim. Preserve unchanged parent
  approval, re-attest changed child content through the applicable authority,
  and let the derived stage expose incomplete evidence. A changed stakeholder
  outcome, justified SR constraint or active WI scope returns to its own intake
  and approval path; it cannot be hidden as a design-only replacement.
- **An LLR's `Hat-Refs` holds only what its OWN decomposition raised — never a
  copy of its parent's.** The row's EFFECTIVE set is derived (own refs unioned
  with its `SR-Refs` parents'), so an own ref is earned only where the design
  row bears a hat **no parent carries**: a platform quirk in the mechanism, a
  keyboard path, an atomicity the requirement never states. Everything else is
  the copy-down the derivation exists to prevent — it turns re-ruling one SR
  into a sweep over its children, and the copies are what go stale. The `§2(c2)`
  test (a hat only where its own `listens_for` names a failure this row
  prevents) decides the rest: most design rows correctly carry nothing, because their
  parent already says why they exist.
- **Acceptance criteria hold the observable condition + threshold.** True of
  every cell that states acceptance, SN `acceptance` included — the tier changes
  what the condition is *about*, never that it must be a condition. Artifact
  identity lives at the trace homes: the LLR `Module` cell, the TC `Evidence`
  cell, `Implements:` back-links, registry ids. Trace media are explicitly open
  — code-comment back-links are a legitimate trace carrier, not a lesser one.
  **An artifact the TC already lists has no second home in the AC**: the second
  copy is the one that goes stale, and it goes stale silently because nothing
  joins the two cells.
- **State acceptance as the CONDITION, never as the instrument** — at SN
  acceptance-intent as much as here, and at SN it is enforced by an advisory
  (§2(d) iii). "A CRITIQUE
  session returns APPROVE against `<rubric>`" names a machine; "each clause of
  the requirement is bound to a child whose TC names the test holding it, and
  that binding set is closed over the clauses" names a condition. The second
  survives the instrument being replaced — which it will be, every time a
  subjective clause is mechanized. For a decomposed row the honest AC is
  usually *the chain, passing, closed over the clauses*.
- **Descend only where a mechanized check earns its keep** (`docs/process.md`
  §3, "over-aggressive traceability is a failure mode in its own right"). Where
  the honest floor is a human's judgement, name the verification `Attest` rather
  than inflate a subjective call into a false `Test`.
- **Record the stopping boundary in the existing scoped review.** For every
  retained child, state the independent decision or verification purpose it adds;
  when further splitting would only paraphrase or duplicate, record why the
  decomposition stops there. Keep the `SN→SR→LLR→TC` tiers required by the
  selected verification method and real verification links intact; this is a
  review judgment, not a row-count quota or a new schema.
- **Coverage by children is earned, not assumed** (the kit repository's ruling
  of record: `OI-72`). An LLR may be satisfied by its parent's coverage. An SR
  may be satisfied by its children only when the children span the SR's full
  dimensional space and are not interdependent; otherwise the honest states are
  a recorded orphan or a direct TC. No validator settles this, and none is
  likely to be efficient: it rests on the author's and the reviewer's reading.

--- PERSPECTIVES (the declared hats this decomposition round must face) ---
_(this sitting's perspectives follow its last section, once for the whole sitting.)_
--- END ---

Write your verdict to the `## amendment` section of docs/reviews/wi-976/011-ADJUDICATE-a46aad8.md. One line per amended row, in the log.md block format:

    - [MEANING|MEANING+BLESS|CLARITY] <row-id> <cell> -> the obligation before -> the obligation after -> why they are (not) the same

`[MEANING+BLESS]` is a MEANING row whose new text you would bless; `[MEANING]` is one you would not. Mark a row one way only: a row tagged both ways reads as MEANING and is not blessed.

Then exactly one machine line:

    VERDICT: MEANING|CLARITY rows=N

`CLARITY` only when EVERY row you were shown is clarity. Commit that verdict file (an adjudication is a recorded verdict — its one home), ending that commit with the trailer `WI: WI-976` — the coordinator learns a judgement is recorded from that trailer and from nothing else, so a verdict committed without it leaves this row open.

Your verdict is this turn's whole output: stop once it is committed. Every row you judged still reads as approved text that drifted from its anchor until an act re-anchors it, and that act is a later act turn taken from your committed verdict, so each row line says what the act needs:

- A `CLARITY` row keeps its attestation: the owner's signature still describes it. The later act turn re-anchors it so the record stops drifting. Where the dial still HOLDS the rung for a human, your verdict is bound to the text shown above (its JUDGED TEXT identities), so an edit to that text after your verdict refuses the act; that act names your verdict, so the act ledger records it and the owner's surface lists it for audit; the merge refuses a held-rung re-attestation your verdict does not rule CLARITY.
- A `MEANING` row's attestation is now a false claim, and it owes a fresh one. Where the rung is RELEASED, mark each row whose new text you would bless `[MEANING+BLESS]`: the later act turn re-attests exactly those. If a row's new text is NOT one you would bless, mark it `[MEANING]` and draft the corrective work in a `## Dispositions` section of this row's own spec, which intake mints at this row's merge. Where the dial HOLDS the rung, stop at the verdict and recommend the row to the owner: the row surfaces on the owner's approval brief and the signature is theirs.
- Never approve a first draft on a held rung. A held rung's `Drafted` row is the owner's alone.

A MEANING row on a held rung refuses the copy and holds the CLARITY rows that share its registry until the owner signs; say so in your verdict, so the coordinator puts them in the same sitting as the MEANING row.

THE DIAL FOR THIS ROW: the LLR/SR/TC tier(s) sit on a rung the declared gate authority has RELEASED, so a CLARITY row is re-attested by the later act turn, and so is a MEANING row you mark `[MEANING+BLESS]`; a row you mark plain `[MEANING]` is not re-anchored.

THE DIAL FOR THIS ROW: the SN tier(s) sit on a rung the declared gate authority still HOLDS for a human. A CLARITY verdict on them is re-attested by the later act turn as a judgement act, naming this verdict; the act ledger records the verdict and the owner's surface lists the act for audit. The verdict is bound to the text shown here (its JUDGED-TEXT identities), so an edit to that text after this verdict refuses the act. A MEANING verdict on them stops at your verdict and the signature is the owner's — recommend it to the owner and do not re-anchor it.

Do not edit any registry CELL either way. Amending the text is the authoring lane's act, approving it is yours, and rewriting a row you are judging is neither — a row whose findings need answering is RETURNED through `## Dispositions`, never fixed in place by its judge.

=== SECTION `## first-approval` ===

You are an INDEPENDENT adjudicator launched by the unattended coordinator, wearing a DIFFERENT hat from whoever authored these rows. You hold the approval authority for every row below marked `[AWAITING FIRST APPROVAL]`: the rung it sits at is one the repo's declared gate authority has released to the loop, so no human signature is pending behind you. What you approve is approved.

A row marked `[AWAITING FIRST APPROVAL - HELD FOR THE OWNER, NOT YOURS TO FLIP]` is shown because it is part of a chain you must read — never because it is yours. Its rung is one the dial still holds for a human. Read it as evidence, weigh it in your verdict on the rows that ARE yours, and leave it out of the act: it reaches the owner through the approval brief, and a flip of it is the one act this whole arm exists to keep out of a session's hands.

A row marked `[AWAITING FIRST APPROVAL - OUTSIDE THIS ACT'S SCOPE, ANOTHER ADJUDICATION'S ROW; SHOWN AS CHAIN EVIDENCE ONLY]` is also shown for the chain and is also not yours — for a different reason, and the difference matters. Nothing is pending on a human for it: it was handed to a DIFFERENT adjudication by a different merge, which will rule on it as you rule on yours. Read it as evidence and do not rule on it. The act may reach only the rows this sitting's `Adjudicates` scope names; the merge refuses a flip outside that scope by name, and the row's own adjudication will judge it.

THE QUESTION, and it is the only one you answer:

    Is each of these rows ready to be APPROVED as it stands — or does it go back with findings?

`Approved` blesses the row's TEXT and nothing else. It does NOT claim any test passed; whether they pass is the harness's answer, never a cell's.

--- ROWS AWAITING A FIRST APPROVAL, WITH THEIR CHAINS ---
- chain of SR-161 — Each decomposition round is reviewed against its applicable perspectives
  - SR SR-161 [approved]
    - AcceptanceCriteria: For one completed decomposition round, the applicable perspectives resolve from the declared hats roster, the decomposition brief presents each applicable perspective's question, and the sitting's review record names an outcome for every one; the independent adequacy review reads that record.
    - Boundary-Refs: B-05
    - Coincident: The need asks that each decomposition round is reviewed against every applicable declared perspective; the sitting's review record naming each perspective's outcome is that outcome, and whether the resulting requirements are adequate is left to independent review, as the need states.
    - Hat-Refs: TEST-ENGINEER
    - Phase: 5
    - Priority: S
    - Rationale: A decomposition produced from one perspective can look complete while omitting security, operations or first-use failures. The hats roster and the planning briefs already supply the applicable questions, and the sitting's review record preserves their outcomes; a separate machine-readable coverage record and checker would duplicate that review without improving its adequacy judgment. Hat-Refs remain the row-level provenance for perspectives that raised a requirement. This applies the owner ruling of 2026-09-06, re-affirmed 2026-10-13.
    - Requirement: When a decomposition round is reviewed, the delivered planning content shall provide every applicable declared perspective's question in the decomposition brief and require the sitting's review record to name the outcome for each perspective.
    - SN-Refs: SN-036
    - SR-ID: SR-161
    - Status: Approved
    - Title: Each decomposition round is reviewed against its applicable perspectives
    - Verification: Inspection
  - LLR LLR-183 [approved]
    - CodeSymbol: load_hat_names/hat_findings/effective_hats
    - Component: CMP-006
    - Detail: The row-level provenance part of perspective review, sited on the row rather than beside it. spine_carrier declares hat_refs (column Hat-Refs) as an OPTIONAL key on the SR and LLR tiers, a typed array of hat roster NAMES; the roster name is the id space, and the C-###-style clause numbering that appears in eight rationale cells is prose that resolves against nothing. Absence is NOT RECORDED and never no-perspective-applied, which is why no rule anywhere requires the cell to be present. trace.load_hat_names reads the roster's table keys only - hats.py stays the sole validator of roster CONTENT, and this reader answers the one question that module answers for nobody else, is this name declared - degrading to the empty set for an absent or unparseable file so the whole rule goes vacuous rather than reporting every row as dangling. trace.hat_findings splits severity the way the boundary rule does: a name the roster does not declare is a finding in the --strict failure set under its own class label, while coverage and the roster's own unattributed hats are single advisory summary lines that never gate. trace.effective_hats derives a design row's effective set as its own refs unioned with its SR parents', so the LLR cell holds only what its own decomposition raised and a dangling parent contributes nothing rather than raising. check_trajectory classifies Hat-Refs TRACED at both tiers, which is what keeps the cell off the re-attest window and out of the snapshot drift basis. Per-decomposition coverage is discharged by the existing review path: applicability derives from the roster's predicates, the decomposition brief presents every applicable hat's question, and the sitting's review record names each outcome. Hat-Refs retain their narrower role of identifying the hats that raised a row; storing applicability or no-finding outcomes in this cell would duplicate review facts and let them go stale.
    - Hat-Refs: MAINTAINER;TEST-ENGINEER
    - LLR-ID: LLR-183
    - Module: project-trajectory/scripts/spine_carrier.py;project-trajectory/scripts/trace.py;project-trajectory/scripts/check_trajectory.py
    - Phase: 5
    - Rationale: A prose label is not a record. The convention this replaces asked an author to name the deriving perspective inside a rationale sentence, which reads correctly to a human and resolves against nothing: no check could tell a live perspective from one deleted a month earlier, and a census was the only instrument that ever found a stale one. Making the attribution a cell whose values resolve against the declared roster converts the whole class from unfalsifiable to mechanical, at the cost of one existence check. The severity split is what makes it adoptable rather than merely correct - the cell is empty on nearly every row the day it exists, so a presence rule would red an entire spine at once and be switched off within a day, while a resolution rule reds only rows that cite something untrue and can therefore be armed immediately. Deriving the effective set instead of copying parents down is the same argument one tier up: a copy turns re-ruling a single requirement into a sweep across every child it has, which is precisely the hand-maintenance a resolvable cell exists to escape.
    - SR-Refs: SR-161
    - Status: Approved
    - TestRefs: (see TC-178)
    - Title: The perspective record as a resolvable cell: Hat-Refs, its integrity rule and the derived effective set
  - LLR LLR-202 [approved]
    - CodeSymbol: staged_hat_refs_findings/traced_cells
    - Component: CMP-006
    - Detail: LLR-183 resolves the perspective record and derives its effective set; staged_hat_refs_findings(root) checks whether that record stayed TRUE. As a Hat-Refs arm of the amend-without-flip guard rather than a new mechanism, it reuses the amendment set staged_spine_amendments already computes and reports each row whose approved half is non-empty while Hat-Refs is absent from its traced half. THE COMPARISON IS BY CELL CLASS: a line-based comparison cannot distinguish an approved-cell amendment from an informative-cell edit that re-dates the row, so this arm keys off split_changed_cells' A5.1 split and stays silent on a traced-only edit - the perspective backfill's own shape. Scope is STRUCTURAL, not an allowlist: traced_cells, extracted from spine_cell_class, answers whether a registry declares the column at all, so the test-case tier is silent because it carries no such cell and a third registry that gains one is guarded with no edit here. Its baseline is the guard's own - HEAD versus the index over rows reading the same approved-text Status on both sides - which leaves two honest vacuities: a row minted in the same commit has nothing to compare, and a row below approval has blessed nothing to amend behind a human's back. Warn-first and never an exit code, printed only under --staged. NOT DISCHARGED: the warn fires once, at the commit that earns it, where a last_approved snapshot would make the finding STAND until answered; that baseline was declined on the timing argument this row exists to serve, and promoting the arm to a drift-tier finding is the next rung if the warn is measured to be ignored.
    - Hat-Refs: MAINTAINER
    - LLR-ID: LLR-202
    - Module: project-trajectory/scripts/acceptance_record.py
    - Phase: 5
    - Rationale: The component and knowledge views are DERIVED, and a derived view is only as true as the rows it derives from: freshness compares an artifact to its regeneration and never asks whether the source was right, so a generated page can be perfectly fresh and confidently wrong. That is the one obligation generation cannot discharge, and the measured instance is a design row that published a deleted symbol for five weeks and was caught by a census rather than by a check. Building it as an arm of an existing guard rather than as its own rule is what keeps the two from disagreeing about what an amendment IS - the same amendment set, the same cell classes, one home. Warn-first because the judgement it asks for is a re-read, not a refusal: whether a moved obligation changes which lenses bear is exactly the call a checker cannot make, and a rule that guessed it would be silenced.
    - SR-Refs: SR-161
    - Status: Approved
    - TestRefs: TC-198
    - Title: Staged Hat-Refs amendment guard
  - LLR LLR-360 [AWAITING FIRST APPROVAL]
    - CodeSymbol: sitting_hat_block/round_hat_block/round_questions/fill_hat_slot/sitting_tail/hat_surface_for_work_item/NOT_A_ROUND/HAT_SLOT/HAT_PARENTS/_roster_refusal/compose/combined_values
    - Component: CMP-008
    - Detail: A sitting brief for a decomposition round carries every declared perspective question applicable to that round and asks the verdict to name one outcome for each perspective. The verdict's per-perspective outcome lines are neither row-ruling lines nor machine lines, so a verdict carrying them parses to the same rulings and judged rows as one without them. A decomposition round judges a system requirement awaiting first approval or an approved stakeholder need whose text is amended; another judged set carries no perspective question. The applicable set combines each amended need with each need named by a system requirement the sitting judges, including an amended system requirement, widens each need by the authoring work item's declared tags, and evaluates each need alone. Questions fill the perspective slot only when the sitting template declares it; a template without that slot composes unchanged. A sitting composed from several judgement kinds carries the questions once. Outside a decomposition round the roster is not read. An absent roster yields its no-perspective line, while an unreadable existing roster refuses a round's composition only when its template declares the perspective slot, and names the roster.
    - LLR-ID: LLR-360
    - Module: project-trajectory/scripts/plan_briefs.py;project-trajectory/scripts/adjudicate_brief.py;project-trajectory/prompts/adjudicate-first-approval.template.md;project-trajectory/prompts/adjudicate-amendment.template.md
    - Phase: 5
    - Rationale: A decomposition review needs the applicable questions in the same brief and verdict that record its judgement. Treating each parent need independently prevents tags from one sibling widening another, while an optional slot preserves briefs that do not conduct a decomposition review.
    - SR-Refs: SR-161
    - Status: Drafted
    - TestRefs: TC-399
    - Title: Perspective questions in a decomposition-round sitting
  - TC TC-178 [approved]
    - Automated: Yes
    - Evidence: tests/test_trace_hats.py::test_an_undeclared_hat_name_is_a_finding; tests/test_trace_hats_driven.py::test_an_undeclared_hat_reds_a_real_run_under_strict; tests/test_trace_hats.py::test_the_rule_is_vacuous_without_a_roster; tests/test_trace_hats.py::test_an_unparseable_roster_is_vacuous_not_loud; tests/test_trace_hats.py::test_coverage_is_one_advisory_and_never_a_finding; tests/test_trace_hats.py::test_effective_hats_unions_the_parents; tests/test_trace_hats.py::test_a_parent_re_ruling_moves_the_child_with_no_child_cell_edited; tests/test_trace_hats.py::test_a_dangling_parent_contributes_nothing_rather_than_raising; tests/test_trace_hats.py::test_the_roster_path_matches_the_hats_module; tests/test_trace_hats.py::test_the_design_tier_is_checked_too_and_names_its_own_id; tests/test_trace_hats.py::test_an_absent_roster_file_reads_as_no_names; tests/test_trace_hats.py::test_a_hat_no_row_is_attributable_to_is_reported
    - Expected: Satisfies LLR-183's Hat-Refs provenance, name-resolution, severity and effective-set mechanics; SR-161's perspective-review acceptance is inspected by TC-211.
    - Level: Unit
    - Method: Four halves, one per claim the row makes. RESOLUTION: build a spine whose SR and LLR rows carry a Hat-Refs naming a hat the roster declares and one naming a hat it does not, and assert the second is reported and joins the --strict failure set under its own class while the first is silent. VACUITY: delete the roster and assert the same tree reports nothing at all, then leave a roster that will not parse and assert the same - absence is opt-out for the layer, and a rule that reddened every row on a malformed roster would punish the wrong file. COVERAGE NEVER GATES: assert a tree whose rows carry no Hat-Refs at all exits zero under --strict and reports exactly one coverage advisory. THE DERIVED SET: assert effective_hats returns the union of a row's own refs with its SR parents', that a parent's change moves the child's answer with no child cell edited, and that a dangling SR-Refs contributes nothing rather than raising. Plus the anti-drift pin the second reader needs: assert trace's roster path equals hats.ROSTER_REL, since a test may import both modules where the shipped code may not.
    - Phase: 5
    - Status: Approved
    - TC-ID: TC-178
    - Tier: Full
    - Verifies: SR-161;LLR-183
  - TC TC-198 [approved]
    - Automated: Yes
    - Evidence: tests/test_trajectory_staged.py::test_amending_approved_cells_without_moving_hat_refs_warns; tests/test_trajectory_staged.py::test_hat_refs_arm_is_silent_when_only_traced_cells_move; tests/test_trajectory_staged.py::test_hat_refs_arm_is_silent_when_the_cell_moves_with_the_amendment; tests/test_trajectory_staged.py::test_hat_refs_arm_is_vacuous_where_a_row_has_no_baseline; tests/test_trajectory_staged.py::test_hat_refs_arm_is_silent_on_a_tier_that_carries_no_such_column
    - Expected: Satisfies the acceptance folded into LLR-202 (parent SR-161)
    - Level: Unit
    - Method: Drive the arm over a real two-commit git repository whose HEAD holds an Approved SR-001 (and, for the tier case, an Approved LLR-001 and TC-001), with the change STAGED rather than committed - the hook's own question. FIRES: the requirement cell amended while Hat-Refs stands raises one finding naming the row and the moved cells, with the amendment arm firing alongside it so the second arm is proven an addition rather than a re-spelling. SILENT ON TRACED-ONLY MOVEMENT: writing the Hat-Refs cell itself - the perspective backfill's own edit - raises nothing, and neither does an SN-Refs re-point. SILENT WHEN DISCHARGED: substance and Hat-Refs moving together raises nothing here while the amendment arm still fires. VACUOUS WHERE THERE IS NO BASELINE, both shapes: a row minted in the staged commit, and a row amended below approval on both sides. STRUCTURALLY SILENT ON A TIER WITH NO SUCH COLUMN: an LLR and a TC amended in the same commit yield exactly one finding, the LLR's, so the scoping cannot pass by the arm being silent everywhere.
    - Phase: 5
    - Status: Approved
    - TC-ID: TC-198
    - Tier: Full
    - Verifies: SR-161;LLR-202
  - TC TC-211 [approved]
    - Automated: No
    - Evidence: docs/test/inspection-procedures.md#decomposition-proportionality-inspection-result
    - Expected: The actual review record names every applicable perspective's outcome, each child within a required tier has an independent decision or verification purpose, and the record explains why further splitting stops; any omitted outcome or purposeless child is an Inspection finding.
    - Inputs: docs/test/inspection-procedures.md;SR-161;SR-186;docs/requirements/hats.toml;docs/reviews/wi-976/011-ADJUDICATE-a46aad8.brief.md;docs/reviews/wi-976/011-ADJUDICATE-a46aad8.md
    - Level: Inspection
    - MaxAge: 90
    - Method: Follow the decomposition proportionality inspection in docs/test/inspection-procedures.md#decomposition-proportionality-inspection; inspect one actual completed decomposition review record, its complete chain, and an extra paraphrasing child.
    - MinWorkItems: 10
    - Phase: 5
    - Rubric: docs/rubrics/decomposition-proportionality.md
    - Status: Approved
    - TC-ID: TC-211
    - Tier: Release
    - Trigger: release
    - Verifies: SR-161;SR-186
  - TC TC-399 [AWAITING FIRST APPROVAL]
    - Automated: Yes
    - Evidence: tests/test_plan_briefs.py::test_a_sitting_with_no_first_approval_sr_and_no_amended_need_says_it_is_no_decomposition_round; tests/test_plan_briefs.py::test_outside_a_round_the_roster_is_not_read; tests/test_plan_briefs.py::test_an_amended_need_is_a_parent_the_work_items_refs_do_not_reach; tests/test_plan_briefs.py::test_a_judged_sr_reaches_hats_through_the_need_it_names; tests/test_plan_briefs.py::test_the_work_items_tags_widen_each_need_and_sibling_needs_never_merge; tests/test_plan_briefs.py::test_an_absent_roster_yields_the_opt_out_line_in_a_round; tests/test_plan_briefs.py::test_a_malformed_roster_refuses_a_round_naming_the_roster; tests/test_plan_briefs.py::test_the_round_block_asks_one_outcome_line_per_hat_in_a_non_ruling_form; tests/test_adjudicate_brief.py::test_a_first_approval_of_a_drafted_sr_carries_the_hat_block; tests/test_adjudicate_brief.py::test_a_first_approval_of_llr_and_tc_rows_only_says_no_decomposition_round; tests/test_adjudicate_brief.py::test_an_amendment_of_an_approved_need_carries_the_hat_block; tests/test_adjudicate_brief.py::test_an_amendment_of_an_sr_only_says_no_decomposition_round; tests/test_adjudicate_brief.py::test_an_amendment_round_reaches_the_need_of_every_sr_it_judges; tests/test_adjudicate_brief.py::test_a_combined_round_reaches_the_need_of_an_sr_another_section_amends; tests/test_adjudicate_brief.py::test_an_override_without_the_hats_slot_composes_unchanged; tests/test_adjudicate_brief.py::test_a_combined_sitting_carries_the_hat_questions_once_over_the_union; tests/test_adjudicate_brief.py::test_a_combined_sitting_that_is_no_round_states_it_once; tests/test_adjudicate_brief.py::test_a_malformed_roster_refuses_a_round_sitting_by_name; tests/test_adjudicate_brief.py::test_no_other_brief_declares_the_hats_slot; tests/test_adjudicate_brief.py::test_hat_outcome_lines_change_no_ruling
    - Expected: Satisfies LLR-360 (parent SR-161): a decomposition-round sitting presents each applicable perspective question and requires one outcome, while another sitting has no perspective question; optional-slot, combined-sitting, absent-roster, unreadable-roster, and verdict-parsing outcomes remain as stated.
    - Level: Unit
    - Method: Exercise each state of the hat block: a non-round neither reads the roster nor asks a perspective question; a first-approved system requirement or amended approved need makes the round, and every judged system requirement's need and every amended need is a parent; work-item tags widen one need without merging siblings; an absent roster supplies the no-perspective line; an unreadable roster refuses and names it; each applicable perspective receives one non-ruling outcome line; declared template slots receive the block while undeclared slots compose unchanged; a combined sitting carries one union block; and those outcome lines do not alter parsed row rulings or judged rows.
    - Phase: 5
    - Status: Drafted
    - TC-ID: TC-399
    - Tier: Full
    - Verifies: SR-161;LLR-360
--- WHAT THE APPROVAL RECORD CURRENTLY ANCHORS ---
docs/archive/last_approved, each registry this act copies as last written:
  - docs/requirements/low-level-requirements.toml: copied 2026-10-25 (commit e592e5eee)
  - docs/test/test-cases.toml: copied 2026-10-25 (commit e592e5eee)
Approving these rows moves it for the registries the act flips rows in and for no others (WI-571), so an off-spine census computed against it survives the act.
--- END ---

Method — put to each row the questions for its tier, reading the CHAIN, not the row:

## 0. Every row — read the chain, not the row

- For each row, state to yourself the obligation it imposes: what a builder
  must do, what a test must check. A row you cannot restate as an obligation is
  not ready.
- Read UPWARD. Does the parent it points at actually call for this? A
  decomposition row that answers a requirement nobody made is scope, not
  detail.
- Read SIDEWAYS. Do the siblings together cover what the parent asks, without
  overlapping into each other's decisions? One decision per row.
- Read DOWNWARD. Do the test cases that claim to verify this row verify what it
  actually says — and does anything it says go unverified?
- Read the wording as a closed obligation: a "should" that means "must", a
  threshold with no units, an actor left unnamed, an acceptance condition
  nobody could observe. Each is a finding that sends the row back, not a note.
- **Name only what the row's tier may name.** No row's text names an
  implementation carrier (a code file, function or symbol). A shipped boundary
  artifact (a registry, template, config file or launcher) may be named at the
  LLR and TC tiers only; SN and SR rows name no file in any cell, acceptance and
  rationale included. An approved cell keeps its approved text verbatim, names
  included, until it is amended through its authority, and an amendment adds no
  name the rule forbids.

## 3. At LLR and TC

- **An LLR states its contract in words that survive a refactor.** Its text
  states the observable obligation: the inputs it takes, the outcome it
  produces and where it refuses, so a refactor that keeps the behaviour keeps
  the row true. It names no implementation carrier (a code file, function or
  symbol), and §0's naming rule says which tiers may name a shipped boundary
  artifact. Do not launder a concrete name upward
  into the SR to keep the LLR abstract. The traced `module` and `code_symbol`
  cells are trace homes, not row text: they stay filled and binding while the
  schema requires them (`trace.py --strict-schema` requires both;
  `check_doc_refs --strict` binds the symbol), so never return a row for
  keeping them. No `shall` in an LLR — the SR states the obligation, the child
  decomposes it.
- **A child adds detail.** If the LLR would merely re-word its parent, link
  instead. `trace.py`'s paraphrase advisory is lexical and warns forever; the
  judgement stays yours.
- **Replace an unsuitable design through the normal amendment route.** If the
  parent outcome remains sound but the LLR's mechanism causes the problem,
  compare the old/new design, retained parent clauses and behavioral regressions,
  affected trace/evidence/work references, and the code that becomes removable.
  Amend the LLR and its mechanism-specific verification together; an Approved
  LLR does not require keeping an obsolete shim. Preserve unchanged parent
  approval, re-attest changed child content through the applicable authority,
  and let the derived stage expose incomplete evidence. A changed stakeholder
  outcome, justified SR constraint or active WI scope returns to its own intake
  and approval path; it cannot be hidden as a design-only replacement.
- **An LLR's `Hat-Refs` holds only what its OWN decomposition raised — never a
  copy of its parent's.** The row's EFFECTIVE set is derived (own refs unioned
  with its `SR-Refs` parents'), so an own ref is earned only where the design
  row bears a hat **no parent carries**: a platform quirk in the mechanism, a
  keyboard path, an atomicity the requirement never states. Everything else is
  the copy-down the derivation exists to prevent — it turns re-ruling one SR
  into a sweep over its children, and the copies are what go stale. The `§2(c2)`
  test (a hat only where its own `listens_for` names a failure this row
  prevents) decides the rest: most design rows correctly carry nothing, because their
  parent already says why they exist.
- **Acceptance criteria hold the observable condition + threshold.** True of
  every cell that states acceptance, SN `acceptance` included — the tier changes
  what the condition is *about*, never that it must be a condition. Artifact
  identity lives at the trace homes: the LLR `Module` cell, the TC `Evidence`
  cell, `Implements:` back-links, registry ids. Trace media are explicitly open
  — code-comment back-links are a legitimate trace carrier, not a lesser one.
  **An artifact the TC already lists has no second home in the AC**: the second
  copy is the one that goes stale, and it goes stale silently because nothing
  joins the two cells.
- **State acceptance as the CONDITION, never as the instrument** — at SN
  acceptance-intent as much as here, and at SN it is enforced by an advisory
  (§2(d) iii). "A CRITIQUE
  session returns APPROVE against `<rubric>`" names a machine; "each clause of
  the requirement is bound to a child whose TC names the test holding it, and
  that binding set is closed over the clauses" names a condition. The second
  survives the instrument being replaced — which it will be, every time a
  subjective clause is mechanized. For a decomposed row the honest AC is
  usually *the chain, passing, closed over the clauses*.
- **Descend only where a mechanized check earns its keep** (`docs/process.md`
  §3, "over-aggressive traceability is a failure mode in its own right"). Where
  the honest floor is a human's judgement, name the verification `Attest` rather
  than inflate a subjective call into a false `Test`.
- **Record the stopping boundary in the existing scoped review.** For every
  retained child, state the independent decision or verification purpose it adds;
  when further splitting would only paraphrase or duplicate, record why the
  decomposition stops there. Keep the `SN→SR→LLR→TC` tiers required by the
  selected verification method and real verification links intact; this is a
  review judgment, not a row-count quota or a new schema.
- **Coverage by children is earned, not assumed** (the kit repository's ruling
  of record: `OI-72`). An LLR may be satisfied by its parent's coverage. An SR
  may be satisfied by its children only when the children span the SR's full
  dimensional space and are not interdependent; otherwise the honest states are
  a recorded orphan or a direct TC. No validator settles this, and none is
  likely to be efficient: it rests on the author's and the reviewer's reading.

Fail toward `RETURN`. An approval is a standing claim that a competent reader blessed this text; a wrongly-returned row costs one more lane, and a wrongly-approved one is a false claim the record then carries forward.

Your verdict is this turn's whole output. You change no registry cell and take no snapshot: the act your verdict authorizes, flipping each row you APPROVE and anchoring its copy, is a later act turn taken from your committed verdict, so a row line here is exactly what that act reads.

If the answer is RETURN, change NO registry cell. Draft the follow-up work in a `## Dispositions` section of this row's own spec — one fenced ```toml block per draft — and intake mints it at this row's merge. Do not file the row yourself; a lane that mints an id is refused at the merge slot.

A MIXED batch is normal: approve the rows that are ready, return the rest, and say which is which. The verdict label answers for the BATCH.

--- PERSPECTIVES (the declared hats this decomposition round must face) ---
_(this sitting's perspectives follow its last section, once for the whole sitting.)_
--- END ---

Write your verdict to the `## first-approval` section of docs/reviews/wi-976/011-ADJUDICATE-a46aad8.md. One line per row, in the log.md block format:

    - [APPROVE|RETURN] <row-id> -> the obligation it imposes -> what its chain shows -> why it is (not) ready

Then exactly one machine line:

    OUTCOME: APPROVE|RETURN rows=N

`APPROVE` only when EVERY row you were shown is approved. Only a row marked `[AWAITING FIRST APPROVAL]` may be ruled `APPROVE`. Commit the verdict file (an adjudication is a recorded verdict — its one home), ending that commit with the trailer `WI: WI-976` — the coordinator learns a judgement is recorded from that trailer and from nothing else, so a verdict committed without it leaves this row open.

Then stop. The sitting ends at that committed verdict: the later act turn flips each row you ruled `APPROVE` and takes its copy, and a row you RETURNED stays `Drafted`, with its `## Dispositions` follow-up already part of the verdict.

=== THIS SITTING'S PERSPECTIVES ===

- **SECURITY** — What secret, credential, or irreversible action does this touch — and which requirement says who may reach it?
  - listens for: A decomposition that spends a secret, or takes an action nothing can undo, with no requirement naming the authority for it.
  - knowledge: docs/knowledge/security-review.md
- **FIRST-RUN-ADOPTER** — Can a new or upgrading adopter complete this using the shipped guidance while preserving project-owned content, policy meaning, accepted evidence and unfinished work?
  - listens for: A requirement satisfiable only with undocumented project knowledge, or an upgrade that breaks supported callers, changes preserved content's meaning, loses accepted evidence or strands unfinished work.
  - knowledge: docs/knowledge/instruction-file-adherence.md
- **MAINTAINER** — Can a reader two years from now tell why this exists, and what would break if they deleted it?
  - listens for: A requirement whose reason lives only in the session that wrote it, leaving the next reviser unable to tell load-bearing from accident.
  - knowledge: docs/knowledge/instruction-file-adherence.md, docs/knowledge/traceability-enforcement.md
- **TEST-ENGINEER** — Which test, analysis, critique or attestation detects a violation, how is its ability to detect it demonstrated, and what does that evidence leave unverified?
  - listens for: An obligation with no suitable verification, or evidence that passes without examining the claimed behavior or hides its limits.
  - knowledge: docs/knowledge/traceability-enforcement.md
- **UX-DESIGNER** — Who reads this surface, what decision are they making on it, and does the layout put that first?
  - listens for: A surface that renders every fact it has instead of the one the reader came for.
  - knowledge: docs/knowledge/rendered-surface-review.md
- **UX-ENGINEER** — Does this hold up at the real widths, themes and content volumes — and what does it do when the data is empty, huge, or malformed?
  - listens for: A view verified only by reading its generator, never by looking at it rendered.
  - knowledge: docs/knowledge/rendered-surface-review.md
- **ACCESSIBILITY** — Can someone using a keyboard, a screen reader, or a low-vision setting complete this — and is that stated as a requirement rather than hoped for?
  - listens for: A surface whose acceptance names only how it looks to a sighted mouse user.
  - knowledge: docs/knowledge/rendered-surface-review.md
- **PERFORMANCE** — Does this need a measurable bound on speed, size, provider usage or operator time? If yes, what is the budget, under which conditions is it measured, and what happens when it is exceeded?
  - listens for: A material resource or operating-cost risk left unassessed, a budget with no measurement behind it, or incomparable or unavailable measurements reported as a reliable total.
  - knowledge: docs/knowledge/prompt-image-token-efficiency.md, docs/knowledge/parallel-scheduling.md
- **CONSISTENCY** — Where else does this fact, state or action appear, and do the related requirements, interfaces, policy readers and user surfaces agree in meaning, vocabulary and interaction?
  - listens for: Related contracts or readers disagreeing after a one-sided change, a rule stated differently by template and instance, or one meaning given conflicting words, visual treatments or interaction behavior.
  - knowledge: docs/knowledge/rendered-surface-review.md
- **INTEGRITY-RECOVERABILITY** — If this is interrupted mid-write — a kill, a crash, a lane that dies holding it — what does the next reader find, and what gets the system back to a state it can name?
  - listens for: A durable artifact updated in place with no all-or-nothing guarantee; a claim or reservation nothing can reclaim once its holder is gone; a recovery path written only for the unattended run when the same corruption is reachable attended.
  - knowledge: docs/knowledge/crash-atomicity-recovery.md
- **PRODUCT-FITNESS** — Who asked for this, which stated need does it still serve, and would the person who asked recognise this as the outcome they wanted?
  - listens for: A decomposition faithfully hardening the wrong thing: an obligation no stakeholder can be named for, a need whose subject has moved while its text stayed, work justified by the machinery it continues rather than by an outcome anyone wants.

Name every hat listed above in your verdict, once each, on its own line beside your row lines and under no heading of its own:

    - HAT <NAME> -> <the rows it raised, by their Hat-Refs, or no finding> -> <why>

An outcome line rules no row and is no machine line. A listed hat with no outcome line is a finding for the review of this verdict, never a check.

Write these outcome lines once for the whole sitting, under the last section's `## <kind>` heading.

## Arms map (a coordinator-supplied input: a read-only sub-agent mapped each LLR arm and SR-161 acceptance clause to the TC clause and the test that verify it; three lane gaps it found were closed before this sitting, the rest are listed as found)

# Arms map — WI-976 spine sitting (SN-036 / SR-161 / SR-165 / LLR-183 / LLR-360 / TC-178 / TC-211 / TC-399)

Read from worktree `C:/Projects/ai-template.wt/wi-976` at HEAD 5fbe747b3 (lane base aa36a5b6e).
Test bodies read with `ast`. Test files abbreviated: `th` = tests/test_trace_hats.py, `thd` =
tests/test_trace_hats_driven.py, `pb` = tests/test_plan_briefs.py, `ab` = tests/test_adjudicate_brief.py.
Status: **E** = exercised by a test in the TC's evidence; **P** = partly exercised; **—** = not exercised by evidence.

Context checks:
- SR-165 vs lane base: only `rationale` moved (the dangling "the SR-161 form applied to the partition..." clause is gone). Meaning unchanged. No arm drawn, and no TC in the set cites it.
- SN-036 acceptance ↔ SR-161: they coincide (the record names each perspective's outcome; an independent review judges adequacy).
- TCs citing the set's rows: TC-178 (SR-161, LLR-183), TC-211 (SR-161, SR-186), TC-399 (SR-161, LLR-360), and TC-198 (SR-161, LLR-202), which is outside the set.
- All 9 TC-178 and 21 TC-399 evidence nodes exist as top-level `def`s. TC-211's evidence anchor `#decomposition-proportionality-inspection-result` exists.

## LLR-183 (cited only by TC-178)

| # | Arm (detail clause) | TC-178 clause stating it | Evidence test(s) exercising it | St |
|---|---|---|---|---|
| A1 | spine_carrier declares `hat_refs` (Hat-Refs) as an OPTIONAL key on SR+LLR, a typed array of roster NAMES | RESOLUTION ("SR and LLR rows carry a Hat-Refs") only implies it. Optional/typed is not stated | none asserts the carrier declaration or array typing. Unit tests feed dicts, `thd` appends a CSV column | — |
| A2 | Roster name is the id space. C-### prose resolves nowhere | RESOLUTION (implicitly) | th::test_an_undeclared_hat_name_is_a_finding (a name outside the roster is a finding) | P |
| A3 | Absence = NOT RECORDED; no rule requires the cell | COVERAGE NEVER GATES | th::test_coverage_is_one_advisory_and_never_a_finding (findings == [], "NOT RECORDED" in line) | E |
| A4 | load_hat_names reads table keys only; hats.py stays the sole CONTENT validator | "anti-drift pin ... trace's roster path equals hats.ROSTER_REL" (path only) | th::test_the_roster_path_matches_the_hats_module (path equality only; "keys only" not exercised) | P |
| A5 | Degrades to the empty set for an ABSENT or UNPARSEABLE file, so the rule goes vacuous | VACUITY ("delete the roster", "a roster that will not parse") | th::test_an_unparseable_roster_is_vacuous_not_loud (load_hat_names → empty). th::test_the_rule_is_vacuous_without_a_roster passes `set()` straight to hat_findings and never reads an absent FILE | P |
| A6 | An undeclared name is a finding in the --strict failure set under its own class label (both tiers) | RESOLUTION | th::test_an_undeclared_hat_name_is_a_finding (SR only; declared SR-001 silent). thd::test_an_undeclared_hat_reds_a_real_run_under_strict (exit 1, "FINDING (hat)", SR CSV only). No evidenced LLR-tier case | P |
| A7 | Coverage = one advisory summary line, never gates | COVERAGE NEVER GATES | th::test_coverage_is_one_advisory_and_never_a_finding | E |
| A8 | The roster's own unattributed hats = one advisory line, never gates | not stated | none in evidence (th::test_a_hat_no_row_is_attributable_to_is_reported exists, unlisted) | — |
| A9 | effective_hats = own refs ∪ SR parents' | THE DERIVED SET | th::test_effective_hats_unions_the_parents | E |
| A10 | The LLR cell holds only its own (no copy-down) | "a parent's change moves the child's answer with no child cell edited" | th::test_a_parent_re_ruling_moves_the_child_with_no_child_cell_edited | E |
| A11 | A dangling parent contributes nothing rather than raising | THE DERIVED SET | th::test_a_dangling_parent_contributes_nothing_rather_than_raising | E |
| A12 | check_trajectory classifies Hat-Refs TRACED at both tiers (off re-attest window, out of snapshot drift basis) | not stated | none in TC-178 evidence. The class map is `acceptance_record.SPINE_TRACED_CELLS`, re-exported by check_trajectory. TC-198's test_trajectory_staged tests touch it only indirectly (LLR-202, outside the set) | — |
| A13 | Per-decomposition coverage goes through the existing review path (roster predicates → brief questions → record outcomes) | expected: "SR-161's perspective-review acceptance is inspected by TC-211" (a hand-off, and TC-211 does not cite LLR-183) | none under TC-178. Brief side under TC-399 (see LLR-360), record side under TC-211 | — |
| A14 | Hat-Refs keep the narrower "raised a row" role; applicability/no-finding outcomes are NOT stored in the cell | not stated | none (a prohibition in rationale voice) | — |

TC-178 method clauses that no LLR-183 sentence states: the roster-path equality pin (A4 states only "sole validator"), and COVERAGE's "a tree whose rows carry no Hat-Refs at all ... reports exactly one coverage advisory", which contradicts the code (see gap 3b).

## LLR-360 (cited only by TC-399)

| # | Arm (detail clause) | TC-399 clause stating it | Evidence test(s) exercising it | St |
|---|---|---|---|---|
| B1 | A round's brief carries every applicable perspective question | expected "presents each applicable perspective question". Method "first-approved SR or amended approved need makes the round" | pb::test_the_round_block_asks_one_outcome_line_per_hat_in_a_non_ruling_form. ab::test_a_first_approval_of_a_drafted_sr_carries_the_hat_block. ab::test_an_amendment_of_an_approved_need_carries_the_hat_block | E |
| B2 | ...and asks the verdict to name one outcome for each perspective | expected "requires one outcome". Method "each applicable perspective receives one non-ruling outcome line" | pb::test_the_round_block_asks_one_outcome_line_per_hat_in_a_non_ruling_form (asserts a `- HAT` form exists and is non-ruling, but not the "every hat, once each" wording). ab first-approval/amendment tests assert `- HAT ` present | P |
| B3 | Round = an SR awaiting first approval, or an approved SN whose text is amended | method "a first-approved system requirement or amended approved need makes the round" | ab::test_a_first_approval_of_a_drafted_sr_carries_the_hat_block. ab::test_an_amendment_of_an_approved_need_carries_the_hat_block | E |
| B4 | Any other judged set carries no perspective question | expected "another sitting has no perspective question". Method "a non-round ... nor asks a perspective question" | pb::test_a_sitting_with_no_first_approval_sr_and_no_amended_need_says_it_is_no_decomposition_round. ab::test_a_first_approval_of_llr_and_tc_rows_only_says_no_decomposition_round. ab::test_an_amendment_of_an_sr_only_says_no_decomposition_round. ab::test_a_combined_sitting_that_is_no_round_states_it_once | E |
| B5 | Applicable set = each amended need ∪ each need named by a judged SR (amended SRs included) | method "every judged system requirement's need and every amended need is a parent" | pb::test_an_amended_need_is_a_parent_the_work_items_refs_do_not_reach. pb::test_a_judged_sr_reaches_hats_through_the_need_it_names. ab::test_an_amendment_round_reaches_the_need_of_every_sr_it_judges. ab::test_a_combined_round_reaches_the_need_of_an_sr_another_section_amends | E |
| B6 | Each need is widened by the authoring WI's declared tags | method "work-item tags widen one need" | pb::test_the_work_items_tags_widen_each_need_and_sibling_needs_never_merge | E |
| B7 | Each need is evaluated alone | method "without merging siblings" | same test (`"both question?" not in apart`) | E |
| B8 | Questions fill the slot only when the template declares it | method "declared template slots receive the block". Expected "optional-slot" | ab::test_a_first_approval_of_a_drafted_sr_carries_the_hat_block (shipped slot filled). ab::test_no_other_brief_declares_the_hats_slot (only the two spine templates declare it) | E |
| B9 | A template without the slot composes unchanged | method "undeclared slots compose unchanged" | ab::test_an_override_without_the_hats_slot_composes_unchanged | E |
| B10 | A multi-kind sitting carries the questions once | method "a combined sitting carries one union block". Expected "combined-sitting" | ab::test_a_combined_sitting_carries_the_hat_questions_once_over_the_union. ab::test_a_combined_round_reaches_the_need_of_an_sr_another_section_amends. ab::test_a_combined_sitting_that_is_no_round_states_it_once | E |
| B11 | Absent roster → the no-perspective line | method "an absent roster supplies the no-perspective line". Expected "absent-roster" | pb::test_an_absent_roster_yields_the_opt_out_line_in_a_round (plan_briefs level only) | E |
| B12 | An unreadable existing roster refuses composition and names the roster | method "an unreadable roster refuses and names it". Expected "unreadable-roster" | pb::test_a_malformed_roster_refuses_a_round_naming_the_roster. ab::test_a_malformed_roster_refuses_a_round_sitting_by_name. ab::test_an_override_without_the_hats_slot_composes_unchanged (shipped half) | E |

TC-399 clauses/evidence beyond LLR-360: "a non-round neither reads the roster" (pb::test_outside_a_round_the_roster_is_not_read); "outcome lines do not alter parsed row rulings or judged rows" / expected "verdict-parsing outcomes" (ab::test_hat_outcome_lines_change_no_ruling); ab::test_the_spine_authors_hats_value_puts_the_sittings_questions, which exercises scripts/coordinator/mkprompt.py + terra-spine-prompt.template.md. That is repo-local tooling, and neither LLR-360's module cell nor its detail names it.

## SR-161 acceptance clauses

| # | Clause | TC-211 (Inspection) method/expected | TC-399 / TC-178 | St |
|---|---|---|---|---|
| C1 | For one completed decomposition round, applicable perspectives resolve from the declared hats roster | method "inspect one actual completed decomposition review record" plus the linked procedure ("Resolve the applicable hats"). Inputs list hats.toml. Not in TC-211's own cells | TC-399 B5–B7 (unit) | P |
| C2 | The decomposition brief presents each applicable perspective's question | only in the linked procedure ("confirm that the brief presents every applicable hat's question"). Inputs list the 011 brief. Not in TC-211's method/expected cells | TC-399 expected "presents each applicable perspective question" (B1) | P |
| C3 | The sitting's review record names an outcome for every one | expected "The actual review record names every applicable perspective's outcome ... any omitted outcome ... is an Inspection finding" | TC-399 asks for it in the brief (B2) | E |
| C4 | The independent adequacy review reads that record | not stated (procedure silent too) | not stated | — |

TC-211 expected's other clauses (each child has an independent decision/verification purpose; the record explains why splitting stops; a purposeless child is a finding) are SR-186's, which TC-211 also verifies. SR-186 is outside this set.

## GAPS

**(1) Arms no evidence test exercises**
- a. LLR-183 A1: no evidenced test asserts that spine_carrier declares `hat_refs` OPTIONAL on SR+LLR as a typed array of names.
- b. LLR-183 A6 at the LLR tier: TC-178's method says "SR and LLR rows", but both evidenced resolution tests use SR rows only. th::test_the_design_tier_is_checked_too_and_names_its_own_id exists but is not in the evidence.
- c. LLR-183 A5 absent-FILE half: the evidenced vacuity test passes `set()` to hat_findings and never reads an absent roster file. th::test_an_absent_roster_file_reads_as_no_names exists but is unlisted.
- d. LLR-183 A8 (the unattributed-hats advisory): no evidenced test. th::test_a_hat_no_row_is_attributable_to_is_reported exists but is not in any TC's evidence.
- e. LLR-183 A12 (Hat-Refs classified TRACED; off the re-attest window and the drift basis): no TC-178 test. It is touched only indirectly by TC-198's staged-arm tests (LLR-202, outside the set). The class map also lives in `acceptance_record.SPINE_TRACED_CELLS`, while LLR-183's detail and module cell credit check_trajectory, which only re-exports it.
- f. LLR-183 A4 "table keys only": only the path-equality pin is evidenced. Nothing shows a roster with sound keys and content hats.py rejects still yielding names.
- g. LLR-183 A13/A14 (discharged via the review path; nothing stored in the cell): no TC-178 test. A14 is a rationale-voice prohibition, not testable as written.
- h. LLR-360 B2 (weak): the evidence asserts that a non-ruling `- HAT` form exists, not that the instruction asks for every listed hat once each.

**(2) Arms no citing TC clause states**
- a. LLR-183 A1 (optional, typed array), A8 (unattributed advisory), A12 (TRACED classification), A14 (nothing stored in the cell): TC-178 states none of them.
- b. LLR-183 A13: TC-178 hands it to TC-211, but TC-211 does not cite LLR-183. So no TC citing LLR-183 states the review-path discharge.
- c. SR-161 C4 ("the independent adequacy review reads that record"): no citing TC states it (TC-178, TC-211, TC-399, nor the inspection procedure).
- d. SR-161 C1/C2 in TC-211: neither TC-211 cell states them. They live only in the procedure the method delegates to. C2 is stated by TC-399's expected.

**(3) TC clauses no LLR/SR sentence in the set states**
- a. TC-399 expected "verdict-parsing outcomes remain as stated", plus method "non-ruling outcome line ... do not alter parsed row rulings or judged rows": no sentence in LLR-360 or SR-161 states that outcome lines leave verdict parsing unchanged.
- b. TC-178 method COVERAGE: "a tree whose rows carry no Hat-Refs at all exits zero under --strict and reports exactly one coverage advisory" contradicts the code. th::test_a_spine_that_uses_the_cell_nowhere_gets_NO_advisories pins ZERO advisories for exactly that tree. The evidenced th::test_coverage_is_one_advisory_and_never_a_finding uses a tree with one filled cell, and it is unit-level, with no --strict run. LLR-183 states neither the gate-on-use behaviour nor "exactly one".
- c. TC-399 method "a non-round neither reads the roster" has no LLR-360 sentence. LLR-360's "an unreadable existing roster refuses composition" reads unscoped, but pb::test_outside_a_round_the_roster_is_not_read and the slotless override show a malformed roster does NOT refuse outside a round or without a declared slot.
- d. TC-178 method's roster-path equality pin: LLR-183 states only "hats.py stays the sole validator". The pin is arguably the test-side consequence.
- e. (Not a real gap.) TC-211 expected's child-purpose and stopping clauses are stated by SR-186, which TC-211 verifies but which is outside this set.
- f. TC-399 evidence ab::test_the_spine_authors_hats_value_puts_the_sittings_questions pins the coordinator author prompt (scripts/coordinator/mkprompt.py, terra-spine-prompt.template.md). No LLR-360 arm or TC-399 clause states it.

**(4) Evidence nodes that do not exist**
- All 30 named test nodes (TC-178 ×9, TC-399 ×21) and TC-211's evidence anchor exist.
- TC-211 `inputs` names `docs/reviews/wi-976/011-ADJUDICATE-a46aad8.brief.md` and `docs/reviews/wi-976/011-ADJUDICATE-a46aad8.md`. Neither exists: the lane's reviews stop at 010, and a46aad8 is the telemetry commit "session WI-976 verdict accepted". This reads as a forward reference to the pending sitting. It must resolve once that sitting is filed, or the inspection inputs dangle.
- TC-211's anchored result is a PASS from 2026-10-03, taken "under the procedure as it then read". The procedure has since changed, so the inspection is owed again.
- Cosmetic: TC-399's evidence has no space after `;` between `...puts_the_sittings_questions` and `tests/test_adjudicate_brief.py::test_an_override...`.

**(5) LLR test_refs vs citing TCs**
- None. LLR-183 test_refs "(see TC-178)" matches its only citing TC (TC-178). LLR-360 test_refs "TC-399" matches its only citing TC (TC-399, Drafted like LLR-360).
