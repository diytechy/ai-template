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
`shall`; a requirement cell names a concrete artifact only where its rationale
records why that artifact must be constrained; a rationale carries its own
reason) and §4 (gates, verification methods). Read the rule there; use
this file to decide whether your row obeys it.

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
  (ii) two SRs naming the same artifact token, and (iii) a direct-LLR fan-out
  over the declared bound (`SR_FANOUT_MAX`, default 7). A bound is deliberately
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
- **The three authoring advisories** (§2d) read as a cheap standing sweep over an
  existing registry: run `scripts/trace.py` and read the artifact, shared-artifact
  and fan-out sections as a worklist of rows to re-adjudicate.
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
