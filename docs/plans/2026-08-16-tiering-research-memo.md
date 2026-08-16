# Research memo — where concrete names belong, and the from-scratch re-derivation option

**For the owner, ahead of the WI-464 sitting.** Two web-research passes
(2026-08-16) on the questions raised after re-tier v2: (1) what published
practice says about artifact names across requirement → acceptance →
verification, (2) whether a blind from-scratch breakdown reconciled against
the legacy spine is recognized practice. Sources cited inline; the three
paywalled primaries (ISO 29148, INCOSE GtWR, DO-178C) were triangulated
through secondaries and are marked as such in the underlying reports.

## 1. The naming boundary — what the standards actually say

- **Every body surveyed uses a three-way split**, one tier finer than ours:
  the **statement** (solution-free, contractual) → **attributes** (rationale,
  verification method/level/owner — INCOSE's A01–A49, NASA Table 4.2-2) →
  **trace/verification records** (which artifact, which test, which result —
  DO-178C §11.21 "Trace Data" as a standalone controlled item; MIL-STD-961E
  Section 3 vs Section 4; NASA Table D-1's verification matrix). The
  "which file implements this" fact is **trace data, categorically** — not
  requirement text and not acceptance criteria.
- **No source bans concrete names.** All use a *justified-exception* form:
  INCOSE R31 "unless there is rationale for constraining the design"; 29148
  "avoids **unnecessary** constraints"; NASA "if the requirement states a
  method of implementation, the rationale should state why"; 961E "beyond
  those needed to ensure interchangeability". The gate is **recorded
  justification** (our 13v shape), never prohibition. Swartout–Balzer (1982)
  and Nuseibeh's Twin Peaks say clean separation is unattainable in
  principle — a rule that routes and justifies leakage beats one that
  forbids it.
- **Testability without naming the artifact:** Volere's *fit criterion* —
  "an objective measure of the requirement's meaning" — and NASA's
  matrix-side *verification success criteria* both make a row testable by
  stating the **observable condition and threshold**, while the binding of
  observation point to concrete artifact lives in the verification
  matrix/trace record. Acceptance criteria state *what would be observed and
  the pass/fail line*; the TC/trace tier states *where and how*.
- **The interface answer is the strongest precedent for us:** settled ICD
  practice is that a requirement may name the other side AND **cite the
  interface definition by identifier** — the "shall" points at an ICD row;
  the ICD carries the concrete substance in "will/is" voice, no shalls. The
  generalizable pattern: **a requirement may name a registry entry by id,
  because the id is stable while its contents are rewritable.** That is a
  cleaner formulation of "current carrier" than filenames in acceptance
  cells.
- **Named rule classes the kit lacks** (candidates, each a sitting/WI call):
  design-constraint **typing** (a constraint-class SR is legitimately
  different in kind, not a defect — 29148/INCOSE A40); **derived
  requirements** (DO-178C's sanctioned class for implementation-born content,
  with a feedback obligation); Wiegers' marking rule (design detail labeled
  *true constraint* vs *solution suggestion*); full verification-method
  separation (we have the `verification` field; the current-carrier
  filenames are the unseparated residue).

**Implication for the acceptance-criteria tension:** the S3/S5
"Read off the current carrier, as the current set: …" clauses are a halfway
house. The literature's home for them is one tier down — the LLR `module`
cell, TC `evidence`, and the IF registry, all of which **already exist** —
or, where acceptance genuinely needs an anchor, a **registry id** rather
than a filename. That would leave acceptance cells holding observable
conditions and thresholds only. (Deliberately NOT executed — a sitting
ruling; it would touch every S3-reworded row once more.)

## 2. From-scratch breakdown, then reconcile — is it a thing?

- **Not one named practice, but a well-supported composite**: DO-178C's
  reverse-engineering path for legacy/COTS legitimizes re-deriving
  life-cycle data for an existing system; INCOSE has a published procedure
  for "functional decomposition in the absence of formal requirements"
  (Brimhall et al., IS2016); IV&V and Porter/Votta/Basili's N-fold
  inspection supply the empirical case that an **independent second view
  reconciled against the first finds defects neither finds alone**.
- **The three documented pitfalls and their guards:**
  1. *Implementation-mirroring* — the fresh set re-describes the code.
     Guard: **blind derivation** — the deriving team reads ONLY the
     stakeholder needs + the depth-0 boundary frame, never the current
     SR/LLR/TC registries or the scripts (Parnas & Clements: a requirement
     must hold "for all acceptable products").
  2. *Second-system overreach* — the redo balloons past current need.
     Guard: cap derivation to the current mission/boundary statement.
  3. *Rationale loss* — the diff discards why legacy rows exist. Guard: the
     repo's own standing rule — original rationale read before any
     deletion/demotion.
- **Minimal protocol** (fits the kit's agent machinery): (a) blind
  derivation — independent fresh sessions derive a breakdown from
  `stakeholder-needs.toml` + the boundary frame alone, ideally two teams
  with different decomposition axes (diversity is what makes the comparison
  strong — Knight/Leveson showed nominally-independent same-method teams
  correlate their errors); (b) a **mechanical alignment map** — fresh
  function ↔ legacy SR/LLR ↔ existing TC/code, three buckets: matched /
  orphaned-in-legacy / orphaned-in-fresh; (c) **adjudication** — each orphan
  a finding for the owner, routed as WIs, never silently merged. The
  output is a *validation instrument* for the current spine, not a
  replacement: the diff tells the sitting which rows the accreted set
  distorted, which it carries that no need demands, and which needs have no
  carrier.

## 3. Recommendation (provisional, the owner's call)

Run the blind re-derivation as a **pre-sitting validation exercise**, not a
registry rewrite: two independent agent teams, needs+boundary only, produce
capability breakdowns; a third pass builds the alignment map against the
settled v2 layer; the orphan lists land on the sitting desk beside the
brief. The v2 reform is not wasted either way — the reconciliation needs a
one-decision-tiered target to diff against, and the adjudication then
decides keep/replace per row with evidence instead of wholesale. The
acceptance-cell question (filenames → trace tier or registry-id anchors)
should ride the same sitting as one ruling, since it would re-touch the
S3 rows once.
