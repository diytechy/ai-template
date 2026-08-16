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
  DO-178C §11.21 "Trace Data" as a standalone controlled item; NASA
  Table D-1's verification matrix). The "which file implements this" fact is
  **trace data, categorically** — not requirement text and not acceptance
  criteria. *(MIL-STD-961E's Section-3/Section-4 requirements-vs-verification
  split is widely referenced and almost certainly real, but its primary text
  could not be fetched — every mirror 403'd — so it is a LEAD here, not a
  citation; no 961E quote in this memo is verified.)*
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

## 1b. Late-arriving primary-adjacent evidence (the DO-178C deep pass)

- **The split is deliberate, not incidental:** the FAA's DO-178B→C
  Differences Tool records that DO-178C **deleted** the traceability bullet
  points from the requirements/design/code content sections and consolidated
  them into dedicated homes (§5.5 process, §6.5 verification trace, §11.21
  Trace Data as a new life-cycle data item, bi-directional). The standard's
  authors refactored "which artifact carries this" OUT of requirement
  content on purpose.
- **The trace medium is explicitly open** (CAST-15 App. A / DO-248B FAQ
  #71): a matrix is not required, and *"embedded features such as code
  comments"* are sanctioned for fine-grained correlation — which
  incidentally blesses the kit's `Implements:` docstring back-links as a
  legitimate trace carrier.
- **Solution-freedom is level-relative, structurally:** LLRs are outputs of
  the *design* process, live in the Design Description (§11.10) **beside**
  the architecture and component descriptions, and are defined as
  "directly implementable without further information" — naming concrete
  design elements at LLR tier is the standard's expected shape, not an
  exception. (Careful cite: this follows from §11.10's contents and the
  glossary, not from CAST-15, which never enumerates artifacts; and no
  numbered DO-178C objective says "HLRs shall be implementation-
  independent" — that lives in guidance, not the Annex A tables.)
- **Derived requirements** are defined by *content* (behavior beyond the
  parent), carry a mandatory rationale, and are passed upward to the system
  process — the complete published shape for the class the kit lacks.

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

## 2b. The sharpest late findings on the naming rule itself

- **Zave & Jackson 1997 ("Four Dark Corners of RE")** formalize the
  testability/solution-freedom paradox and dissolve it: a requirement R is
  stated in environment vocabulary; a specification S is stated at the
  *shared, observable phenomena*; domain knowledge K relates them
  (S, K ⊨ R). **Naming the observation point fixes subject matter, not
  solution** — it legitimately narrows design space while creating the
  basis for verification. That is the principled answer to "testable but
  not implementation-naming".
- **Volere §3a names our failure mode: "false constraints — solutions
  masquerading as constraints."** Its defence is that every constraint must
  carry a rationale AND a fit criterion, both challengeable. Volere's own
  examples DO name technology, legitimated exactly that way.
- **R2's absolute form ("never name a concrete artifact") is stricter than
  every standard surveyed.** INCOSE R31, 29148, NASA all gate on recorded
  rationale ("unless there is rationale for constraining the design") and
  INCOSE concedes that at the lowest level statements are *"entirely
  specific to the selected solution."* The published resolution is:
  (a) declare the tier the rule bites at (SR = HLR voice, LLR =
  solution-specific by design), (b) rationale-gate the exceptions (the 13v
  shape), (c) move volatile artifact identity to trace data.

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
