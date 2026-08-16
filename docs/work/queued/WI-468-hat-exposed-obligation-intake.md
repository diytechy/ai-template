+++
id = "WI-468"
title = "Hat-exposed obligation intake — propose SN/SR intake for the four obligation candidates the hat-aware blind re-derivation exposed (WI-467 team C, docs/plans/2026-08-16-derivation-alignment.md §4.3), each carried by NEITHER the A/B breakdowns nor the legacy registries: C-DPR-3 (repository content briefed to an external model runner carries commit authorship — names, addresses, timestamps — and no need states a basis, a boundary or an exclusion for that crossing, though the frame already draws it at REL-003); C-DPR-2 (the privacy FINDING RECORD is the one artifact guaranteed to contain the personal data it reports, and nothing bounds its retention or names who may reach it); C-PRF-1 (SN-027 justifies itself entirely in throughput, commissions the system's most complex machinery, and declares no measurement of the improvement — unfalsifiable as written); C-ACC-2 (SN-008's 'a reader can believe a green' names the system's most important signal by its COLOUR, and if colour is the only channel the signal does not exist for a substantial class of readers, nor in a monochrome terminal or a printed record). THIS ROW PROPOSES INTAKE AND MINTS NOTHING: the disposition of each candidate — a new need, an amendment to an existing one, a labelled derived requirement, or refused — is the owner's ruling at the sitting, and the session's deliverable is the option set with its evidence, not a registry row."
specref = "docs/plans/2026-08-16-derivation-alignment.md"
workstream = "requirements"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "spine"
priority = 3
+++

## Context

Filed 2026-08-16 out of the option-(b) application of WI-467's
recommendations. The four rows are the ones team C's hat-aware run exposed
that no earlier derivation reached: A and B worked from needs and from the
frame, and neither axis carries a disciplinary lens, so an obligation that
only a domain charter demands was invisible to both. Two of the four
(C-DPR-3, C-PRF-1) the alignment map classes as **needs defects** — the kit
does the thing, or is about to, and no need says so; two (C-DPR-2, C-ACC-2)
as **new derived-obligation candidates**, which under DO-178C are legitimate
only once the deriving lens is named and a reviewer can accept or reject the
lens rather than the conclusion alone.

Two of the four charters that derived them (DATA-PROTECTION, ACCESSIBILITY,
PERFORMANCE) were unreachable at need level until the same pass gave SN rows
a `tags` field — finding R-2, the largest roster defect the exercise found.
That fix is what makes these four reviewable at all; it is not itself
evidence that any of them should be minted.

### What the session is to produce (scope, not the closed Deliverable)

One intake proposal per candidate, each stating: the C-row id and the charter
that derived it, which existing need (if any) it amends versus what a new need
would have to say, the observable a requirement could be held to, and the
honest case for REFUSING it. Four candidates, one line of subject each:

- **C-DPR-3 · provider egress of commit authorship** (hat.DATA-PROTECTION,
  with hat.SECURITY's C-SEC-5 and hat.LEGAL's C-LEG-3 arriving at the same
  boundary control from two other directions) — a declared basis and exclusion
  rule for repository content, authorship metadata included, crossing to an
  external model runner.
- **C-DPR-2 · finding-record retention bound** (hat.DATA-PROTECTION) — a
  retention limit and an access rule on any persisted personal-data finding
  record, the control's own output being the durable copy of what it caught.
- **C-PRF-1 · SN-027 throughput budget** (hat.PERFORMANCE) — a declared
  improvement target measured against the serial semantic on a declared
  workload, repeatable, with a miss reported rather than silently accepted.
- **C-ACC-2 · colour-only signal** (hat.ACCESSIBILITY) — no verdict, gate
  outcome or status conveyed by colour alone, on any surface that carries one,
  console and rendered alike.

Explicitly OUT of scope, so the boundary is not re-argued in session: minting
or editing any SN row; dispositioning the §2.2 legacy orphans (WI-467's
option-(b) pass labelled those and stops there); and ruling the three
provisional hat charters added to `docs/requirements/hats.toml` at the same
pass — all three are the owner's, at the sitting.
