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

**Authority, not restated here:** `docs/process.md` §3 (one fact one home;
decompose don't paraphrase; one decision per row, one home per method; one
`shall`; the eight quality characteristics and the EARS statement pattern; a
requirement cell names a concrete artifact only where its rationale records why
that artifact must be constrained; a rationale carries its own reason) and §4
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

## 1. At SN intake — answer these before the need is approved

A defect admitted here becomes a whole subtree of need-less requirements later.
Four questions:

- **(a) Does this need carry the TAGS that reach its governing perspective?**
  Hats (`docs/requirements/hats.toml`) fire on an `applies_when` predicate over
  declared fields — and *an undeclared field satisfies no condition*. A need with
  no tags is invisible to the hat that most obviously governs it. Ask: **which
  hats should derive from this need, and do its declared tags reach them?** Check
  it, don't assume it — `python scripts/hats.py audit` is the intake sweep: it
  prints the whole SN × conditional-hat matrix in one pass, plus the needs waking
  no conditional hat, each hat's reach count, and the one mechanical finding (a
  tag token no predicate anywhere can evaluate — `--strict` fails on that class
  alone). The matrix is your **worksheet**, not a verdict: every blank row and
  zero-reach hat is a question you answer per row. For a single row in isolation,
  `python scripts/hats.py applicable --tag <tag> ...` prints
  the hats that decomposition must face. If the governing hat is not in that list,
  fix the tags (or the hat's predicate) *now* — a lens that cannot see the need
  will never produce the obligations that need implies.
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

## 2. At SR derivation — per row

- **(a) One decision per row; one home per method** (`docs/process.md` §3). A row
  that decides both *which artifact* carries a capability and *what it does* is a
  tiering defect, not a style choice. Two rows sharing one interface identity is
  the same defect seen from the other side.
- **(b) Voice.** SR states the delivered capability or the artifact **class**
  ("the delivered harness", "the launchers at the repository root"). The concrete
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
  LABEL it derived.** This is DO-178C's **derived requirement** class: content
  beyond what the parent demands, legitimate *because* it is (i) labelled as
  derived, (ii) carrying a rationale that names the deriving lens — the hat, the
  design constraint, the implementation fact — and (iii) fed back upward so the
  need owner sees it. Name the deriving hat in `Rationale` and record it in the
  decomposition's perspective record. **Never silently trace a derived row to a
  parent whose text does not demand it**: that is the single most common way a
  spine acquires structure nobody asked for and nobody can audit.
  - A row derivable **only** through a hat that ships switched OFF must say so.
    An obligation whose only lens is unreachable is a roster finding, not a
    licence — the label makes it reviewable; it does not make the row wanted.
- **(d) The advisories are detectors, not caps.** `scripts/trace.py` warns —
  never gates — on (i) an SR `Requirement` naming a concrete `.py` artifact,
  (ii) two SRs naming the same artifact token, (iii) a direct-LLR fan-out
  over the declared bound (`SR_FANOUT_MAX`, default 7), and (iv) an opening
  that states a condition outside the four EARS keywords. A bound is deliberately
  not a cap: a hard cap invites merging two LLRs into one to slip under it,
  hiding the defect the number exists to surface. Clearing one is a **recorded
  per-row re-stamp** — the waiver token in `Rationale` for a named artifact, the
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
- **Acceptance criteria hold the observable condition + threshold.** Artifact
  identity lives at the trace homes: the LLR `Module` cell, the TC `Evidence`
  cell, `Implements:` back-links, registry ids. Trace media are explicitly open
  — code-comment back-links are a legitimate trace carrier, not a lesser one.
  **An artifact the TC already lists has no second home in the AC**: the second
  copy is the one that goes stale, and it goes stale silently because nothing
  joins the two cells.
- **State acceptance as the CONDITION, never as the instrument.** "A CRITIQUE
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
- **The ratify brief.** `scripts/trace.py --ratify <scope>` renders the batch's
  SN→SR→LLR→TC hierarchy with prose for the acceptor to read, and
  `--ratify modified` renders the per-cell before/after re-attestation brief.
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
- **A row amended without its own flip** — a row's `Status` answers for its
  OWN cells (`docs/process.md` §4; owner ruling 2026-08-17): flip the row whose
  text changed, and only that row — a child LLR/TC amendment never flips its
  parent SR, and a `Modified` child under an `Approved` SR is a legitimate
  state. The chain-completeness claim belongs to the derived `Founded` state
  (D-9), and an UNMARKED amendment is the snapshot-drift arm's find
  (`docs/archive/last_approved/`), never the parent signature's. Amend and
  flip in the same commit.

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
