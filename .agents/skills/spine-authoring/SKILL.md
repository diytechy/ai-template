---
name: spine-authoring
description: Use when breaking down or developing the SN → SR → LLR → TC spine — the adjudicator's question list per tier: what a need must carry before it is approved, what belongs at SR versus LLR versus the trace tier, when an obligation is a labelled derived requirement, and which instruments catch a distorted breakdown.
stacks: [python, node, powershell, go, rust, any]
domains: [any]
phases: [dev, gate]
tags: [requirements, decomposition, tiering, derivation, hats, derived-requirements, acceptance-criteria]
scope: kit
---

# Spine authoring (breaking down SN → SR → LLR → TC)

You are the **adjudicator**: the one deciding what a row says and which tier it
says it at. Every mechanized check on the spine is a *detector* — it reports a
smell after the fact. The tiering itself is a judgement, and this is the question
list to put to a row **before** it lands.

**Authoring is not approving** (owner ruling 2026-09-01; `docs/process.md` §4).
A worker lane writes its rows `Drafted` and may amend any cell of any row,
approved ones included. It never flips a `Status` to `Approved`/`Founded`, never
writes a row already claiming one, and never writes `docs/archive/last_approved/`
— that act is an adjudication session's, on the serial trunk side, after reading
the row's whole chain, and a lane's merge is refused by name if its delta
performs it. So use the question list to make a row *ready*; the answer to "is
it approved" comes from elsewhere.

**Authority, not restated here:** `docs/process.md` §3 (one fact one home;
decompose don't paraphrase; one decision per row, one home per method; one
`shall`; the eight quality characteristics and the EARS statement pattern; a
need or requirement cell names a concrete artifact only where its reason cell
records why that artifact must be constrained; a rationale carries its own
reason and no citation frame) and §4
(gates, verification methods). Read the rule there; use this file to decide
whether your row obeys it.

## The frame: solution-freedom is tier-relative

The rule that stops most arguments: **keep the SR independent of filenames.**
Record where a capability currently lives in the trace fields that already
exist for it — the LLR `Module` cell, the TC `Evidence` cell, the `Implements:`
back-links in code, or a registry id (an interface row, a component row) — not
in requirement text and not in acceptance criteria. A registry **id** is a safe
anchor where a filename is not: the id is stable while its contents are
rewritable.

And no published body *bans* concrete names — every one gates them on **recorded
justification** (INCOSE R31 "unless there is rationale for constraining the
design"; ISO 29148's "*unnecessary* constraints"; NASA's "if the requirement
states a method of implementation, the rationale should state why"). DO-178C puts
low-level requirements in the Design Description beside the architecture and
defines them as directly implementable — **naming design elements at LLR tier is
the expected shape, not an exception**. So: SR = delivered-capability voice,
LLR = solution-specific by design, and the artifact's identity belongs in the
trace fields listed above. Route and justify leakage; a rule that forbids it
just gets bent silently.

## At adoption or a material project change

Review the project's own vision, stakeholders, domain, operating environment
and changed assurance obligations before relying on its existing hats or spine.
Apply this at initial adoption and to the affected scope of an upgrade or
project change. A tooling-only upgrade may record "no semantic impact" with
its reason in the resync commit; routine commits do not require a whole-spine
rederivation.

Use the ordinary scoped change/review record for the following decisions:

1. **Reassess hats against purpose.** Keep, refine, combine, condition or propose
   retirement by each hat's question and failure class. Add a hat only when an
   important distinct question has no suitable owner. A seed roster, a preserved
   custom file or zero attributed rows does not establish relevance. When
   changing or removing a hat, review its inbound Hat-Refs and preserve valid
   obligations.
2. **Check the real brief.** Inspect applicability on representative need/WI
   contexts, including missing context and not-applicable cases. `hats.py audit`
   is a worksheet; confirm that the actual decomposition receives every relevant
   question. The roster lives in `docs/requirements/hats.toml`; the audit shows
   the SN × conditional-hat matrix, needs reaching no conditional hat and each
   hat's reach count. Repair unreachable predicates or missing declared tags through the
   ordinary authoring/review route, without inferring context from arbitrary prose.
3. **Revisit needs, then affected SRs.** A missing stakeholder outcome warrants
   a new-SN proposal with purpose and observable acceptance intent. An existing
   sound need with a missing perspective-derived constraint warrants an SR
   amendment instead. Use a fresh derivation before comparing implementation-led
   legacy text where independence matters; read legacy rationales before declaring
   an obligation unsupported. A sound requirement violated by code needs a fix,
   not another need.
4. **Reconcile and review the affected chain.** Identify changed LLRs, TCs,
   interfaces, evidence and queued/active work. Keep IDs where meaning remains;
   preserve previous approvals as history and submit the scoped amendments under
   the current authority. Rejected proposals leave authoritative content intact.
   Do not automatically re-seed snapshots, cancel work or copy the kit's own
   objectives, hats or needs into another product.

Syntax checks prove reference integrity and preservation; independent judgment
assesses relevance and adequacy. Optional prose objective anchors explain
purpose without adding a registry tier, approval stage or completion percentage.

## 1. At SN intake — answer these before the need is approved

A defect admitted here becomes a whole subtree of need-less requirements later.
Questions:

- **(a) Does this need carry the TAGS that reach its governing perspective?**
  Hats fire on declared fields; an undeclared field satisfies no condition.
  Use `python scripts/hats.py applicable --tag <tag> ...` and the actual brief
  check above to verify the intended questions reach this need. The audit's
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
  named where carriers belong. **Where a concrete name is genuinely unavoidable,
  the waiver goes in `why`** — the SN tier's reason cell, since the need schema
  carries no `Rationale` — as the same `recorded waiver: <reason>` marker the SR valve uses, with a
  reason a later reader can argue with. A **declared vocabulary** token (a dial
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
  name belongs one tier down — LLR `Module`, TC `Evidence` — or, where acceptance
  genuinely needs an anchor, as **rewritable current-carrier evidence** or a
  registry **id**. Acceptance criteria carry the **observable condition and its
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
- **(c) If the obligation arrived through a lens rather than the need's text,
  RECORD the lens.** This is DO-178C's **derived requirement** class: content
  beyond what the parent demands, legitimate *because* it is (i) recorded as
  derived in a cell something reads, (ii) carrying a rationale that argues the
  deriving lens — the hat, the design
  constraint, the implementation fact — and (iii) fed back upward so the
  need owner sees it. Name the deriving hat in **`Hat-Refs`** (roster names; the
  cell IS the perspective record, and a name the roster does not declare is a
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
- **(d) The advisories are detectors, not caps.** `scripts/trace.py` warns —
  never gates — on (i) an SR `Requirement` naming a concrete `.py` artifact,
  (ii) two SRs naming the same artifact token, (iii) an SN `acceptance` naming a
  concrete artifact (a wider vocabulary than the SR arm's — scripts, configs,
  generated pages — because the need tier's instruments are mostly not scripts;
  `.md` is deliberately excluded, since a document named in a cell is usually a
  citation), (iv) a direct-LLR fan-out over the declared bound (`SR_FANOUT_MAX`,
  default 7), and (v) an opening that states a condition outside the four EARS
  keywords. There is no shared-artifact census at SN: two needs may honestly
  describe outcomes one file happens to serve without either deciding anything
  about it. A bound is deliberately
  not a cap: a hard cap invites merging two LLRs into one to slip under it,
  hiding the defect the number exists to surface. Clearing one is a **recorded
  per-row re-stamp** — the waiver token in the tier's reason cell for a named
  artifact (`Rationale` at SR, `why` at SN), the
  `fan-out re-stamp: <reason>` phrase for fan-out — and the reason must be one a
  later reader can **argue with**. "Accepted" is not a reason.
- **Also ask:** does this row state a *package-wide property* (right-sizing,
  proportionality, one-definition-of-passing, refusal legibility)? Those are the
  rows a per-capability decomposition systematically misses — they end up as
  secondary clauses in nine rows and the subject of none.

## 3. At LLR and TC

- **LLRs name modules and symbols by design.** That is the tier's job; do not
  launder a concrete name upward into the SR to "keep the LLR abstract", and do
  not strip it out of the LLR to satisfy a rule that bites one tier up. No
  `shall` in an LLR — the SR states the obligation, the child decomposes it.
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
  test decides the rest: most design rows correctly carry nothing, because their
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

## 4. Validation instruments

- **Blind re-derivation.** The strongest instrument, and it is a *validation
  exercise, not a rewrite*: independent sessions derive a breakdown from the
  stakeholder needs + the boundary frame + **the hats roster** (the roster is a
  derivation input — a lens that is not in the blind input set cannot produce its
  obligations), never reading the current SR/LLR/TC rows or the code. A separate
  alignment pass — the only role permitted to read both sides — builds a map with
  three buckets: **matched / orphaned-in-legacy / orphaned-in-fresh**. Every
  orphan is **adjudicated** as a finding, never silently merged or deleted; the
  legacy row's own rationale is read *first*. Two teams with **different
  decomposition axes** beat two teams with the same one. Classify each
  legacy orphan: **(i)** implementation-born (a derived-requirement candidate —
  label it), **(ii)** a genuine need the blind teams missed because the *need*
  understates it (a needs defect, not an SR defect), **(iii)** true accretion.
- **The authoring advisories** (§2d) read as a cheap standing sweep over an
  existing registry: run `scripts/trace.py` and read the artifact,
  shared-artifact, fan-out and EARS sections as a worklist of rows to
  re-adjudicate. The
  **verification-coherence** section joins the same sweep: it names a row whose
  prose claims an instrument its `Verification` field contradicts.
- **The method-flip sweep — do this by hand, no checker covers it whole.** When
  a row's `Verification` changes, EVERY prose cell it owns is suspect, not just
  the one you came for. A row mechanized out of `Critique` typically leaves the
  claim in three places: the AC (the instrument), the rationale (the argument
  that the instrument was *necessary* — often phrased as "a mechanized
  verification would assert a green nothing checks", which the row's own passing
  tests then refute), and the retired instrument's own header. Sweep the row,
  its children, and anything citing the retired instrument, in the same commit
  as the flip.
- **The approve brief.** `scripts/trace.py --approve <scope>` renders the batch's
  SN→SR→LLR→TC hierarchy with prose for the acceptor to read, and
  `--approve modified` renders the per-cell before/after re-attestation brief.
  Link the brief; never hand-copy rows into it. (Running the bar itself: the
  `gate-advance` skill. Orphans, integrity and schema findings:
  `registry-hygiene`.)

## 5. Known failure modes

One line each, each one seen in a real spine:

- **Implementation-mirroring** — the "fresh" breakdown re-describes the code
  rather than the need. Guard: blind derivation; a requirement must hold for all
  acceptable products, not just the built one.
- **False constraints** — solutions masquerading as constraints (Volere §3a's
  own name for it). Guard: every constraint carries a rationale *and* a fit
  criterion, both challengeable.
- **The why-cell trap** — a need's load-bearing half (safety, bounds, authority)
  lives only in its `why` cell, so the SR realizing it reads need-less and looks
  like accretion. The defect is in the need. (Seen: a subagent-spawn bound whose
  need stated only *resumable*, with the *safe* half in `why`.)
- **The untagged need / blind hat** — the governing perspective evaluates tags
  the need does not carry, so the hat that most obviously governs it is
  guaranteed not to see it. (Seen: the data-protection, accessibility and
  performance lenses unable to read the very needs they govern.)
- **The buried condition** — the row's condition sits after the `shall` ("shall,
  during an unattended run, refuse…") or opens on a near-miss keyword ("Before
  X…", "For declared…"). Every reader who scans openings to learn *when a row
  applies* misses it, and so does every tool. Guard: the EARS advisory catches
  the opening; the buried-in-the-middle case is yours to catch, because a
  qualifier that describes the RESPONSE legitimately lives there.
- **Colour-only signals** — an obligation naming the system's most important
  signal by its **colour** ("a reader can believe a green") does not exist for a
  substantial class of readers; state the channel, not the hue.
- **Switched-off hats orphaning obligations silently** — a row derivable only
  through an OFF hat looks like accretion to every later reader. It must say so
  in its rationale (§2c).
- **Underivable-from-any-input rows** — when needs-only, frame-only *and*
  hat-aware derivations all fail to produce a row, the missing thing is a need or
  a hat charter. Say which; do not quietly keep the subtree. (Seen: a
  cross-view-uniformity requirement with eight LLRs and eight TCs behind it and
  no declared input demanding it.)
- **Package-wide properties with no home** — an obligation cited as a secondary
  clause in many rows and as the subject of none is uncovered, however many
  citations it has.
- **Acceptance rot after a method flip** — a row states one verification method
  in its `Verification` field and a different one in its prose. Every strict
  gate passes at rc=0 while the row instructs a reader to obtain a verdict its
  own method cannot produce. (Seen: two rows mechanized out of `Critique`, whose
  acceptance went on demanding an APPROVE verdict from rubrics whose own headers
  by then read RETIRED — three weeks and several reviews before it surfaced,
  because nothing compared the two cells.)
- **A citation that outlives its instrument** — retire-don't-delete is right for
  the instrument and wrong for the rows citing it. Retiring a rubric without
  sweeping its citers converts every one of them into an undischargeable
  criterion.
- **The unwired marker** — a state field nobody reads. Adding it is not the same
  as wiring it, and a marker with no consumer is the original gap with a better
  name. Ask, at the moment you add it: which checker, gate or brief changes
  behaviour because of this cell? If the answer is none, say so in the row.
- **A rule that names only some of its tiers** — and the tier quietly left out
  is usually `SN`, the one a stakeholder actually reads. Seen twice: the
  artifact-voice rule shipped governing `SR` alone and the provenance rule
  governing `SR`/`LLR`/`TC`, and each had to be extended to the need tier
  afterwards. Guard: writing or amending a spine rule, enumerate all four tiers
  and say why each one is in or out.
- **A row amended without its own re-attest** — a row's `Status` answers for
  its OWN cells (`docs/process.md` §4; owner ruling 2026-08-17): re-read the
  row whose text changed, and only that row — a child LLR/TC amendment never
  touches its parent SR. There is no marker to set (`Modified` retired
  2026-08-20); EVERY post-approval amendment is the snapshot-drift arm's find
  (`docs/archive/last_approved/`), never the parent signature's, and the
  chain-completeness claim belongs to the derived `Founded` state (D-9).
  The amendment is yours to make; the RE-COPY is the approval act and belongs
  to the trunk-side adjudication (the ruling above), which takes it in the same
  commit as its own ruling on the amendment.

## 6. Cell hygiene — a registry holds living truth

Tiering decides *which row* says a thing. These decide *what a cell may hold at
all*, and they cut across every tier. Each is cheap to violate and expensive to
find later, because the mechanized detectors mostly read PROSE and these
failures hide in FIELDS.

- **A cell states what is true now — never when it changed.** Provenance has
  homes that cannot drift: git, the log's decisions, the archive. A field
  recording an amendment date is the same defect the stand-alone rule forbids in
  prose, and it survives only because the checker reads text, not schema. If you
  are about to add `amended`, `updated`, `since` or a version stamp to a
  registry row, the fact already exists somewhere better.
- **The reason cell is not a changelog.** `Rationale` (`why` at `SN`) is the one
  cell whose whole job is argument, which is why every citation drifts into it —
  and it is covered by the rule above, on all four spine tiers. It states **what
  breaks without the row** and **which alternative lost**, and carries no citation
  frame: no work-item id, no ruling, sitting, review-round or open-item reference,
  no decision id, no `AMENDED`/`REWORDED`/`MINTED` verb, no date stamp. Those
  belong in the log, which can hold the full account and cannot rot into the
  specification.
- **When you strip a frame, keep the reason.** The failure mode is deleting
  `AMENDED 2026-03-04 (round 2, finding F7): the cell claimed a speedup nothing
  measures` in one stroke — frame *and* argument — leaving a bare assertion.
  Restate the durable half as standing prose ("this states a structural property,
  not a throughput claim: no instrument here measures speedup") and send the rest
  to the log. If deleting the frame leaves nothing, the cell was a changelog and
  the log already holds it; delete the whole block. `scripts/trace.py` reports
  what is left as a **worklist**, warn-first — a row whose frame is the only
  record of an unresolved question gets a reviewed entry in the detector's
  allow file rather than a silent deletion.
- **One vocabulary per axis, across every tier.** If three tiers say `Drafted`
  and the fourth says something else for the same state, a reader must learn a
  different field per tier and every cross-tier query grows a special case.
  Reach for the vocabulary that exists before minting a parallel one — a new
  marker for a state the spine already names is a synonym, not a feature.
- **Do not declare what the row already derives.** If a field's value is a
  function of the other cells — a type implied by which fields are present, an
  owner implied by a link — it is a second source that can disagree with the
  first. A redundant cell can be deleted; a *disagreeing* one cannot, and you
  will not know which you have until it disagrees.
- **One question per field.** A field answering two unrelated questions (a
  maturity state and a row type in one `kind`) cannot be queried for either
  without knowing the other, and neither half can change vocabulary
  independently.
- **Prefer the smallest closed vocabulary that stays honest.** Enum values are
  cheap to add and near-impossible to remove once rows carry them; a value whose
  meaning overlaps an existing one will be applied inconsistently from the day
  it lands.
