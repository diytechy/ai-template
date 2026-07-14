# Open items — owner decision briefs

The **single owner-review surface**: one section per pending decision, with the
context needed to rule — what's being decided, blast radius, options with
pros/cons, and the driver's recommendation. [status.md](status.md) carries only
the one-line form of each; the DAG rows live in
[work-items.csv](requirements/work-items.csv). **A section lives here only
while the decision is pending** — the ruling appends to [log.md](log.md)'s
Decisions log and the section is deleted. (Format:
[specs/open-items-surface.md](specs/open-items-surface.md).)

Items OI-1…OI-3 bundle into **one ratification sitting**; OI-4…OI-7 are
independent rulings the same sitting can absorb.

---

## OI-1 — Attest the SR-049 spine cut + the v2 batch (→ G3)

- **Decision:** accept (attest) the spine as it now stands: the derived-gate
  campaign added **SR-049** (gate computed from artifact states) to the
  ratified spine, and phase v2 (SR-050 process view, SR-051 tiered drill-downs)
  was ratified `Planned` by the G1 LLM-gate review, decomposed by the
  `[v2]-[g2]` batch, and Verified by the two dev slices. The mechanized bar is
  met (derived gate reads uniform G3; 46 Test · 2 Analysis · 1 Inspection · 0
  Attest); the owner's attested sign-off is the outstanding half.
- **Blast radius:** the spine's trust claim. G3 asserts owner-accepted scope;
  until attested, that claim rides mechanics alone — every downstream consumer
  of the "kit traces itself" story inherits the gap.
- **Included provisional rulings to accept or amend** (implemented as ruled;
  verdicts + rationale in [log.md](log.md)): the tiered-drill-down slice's four
  calls (tier composition Phase ⊃ Workstream ⊃ WI; grouping-primary phase
  encoding + per-phase accent; in-place expand, no zoom; the >3
  start-collapsed rule with `TOP_VIEW_MAX = 10`) and the process view's
  generated-first render mode.
- **Options:** attest as-is · amend a provisional ruling (re-opens the slice
  that implemented it) · reject a slice (reverts its spine rows).
- **Recommendation:** review the provisional verdicts in the log, attest at
  one sitting (`gate-advance` skill, Attest row) — the mechanized evidence is
  green and re-runnable.

## OI-2 — Review the single-ratify enablement commit

- **Decision:** accept the `docs/gate-policy` move `attended` → `single-ratify`
  (one human attest per phase batch). By the policy file's own rule the landing
  commit *is* the reviewed commit the owner accepts; until reviewed,
  [gate-policy.md](gate-policy.md) stands DRAFT.
- **Blast radius:** governance only — WHO makes a ratifying commit for every
  future phase batch. It does not change what the derived gate computes.
- **Options:** accept (unattended loop continues under one-attest-per-batch) ·
  revert to `attended` (every ratification needs a live human in the loop).
- **Recommendation:** accept if the OI-1 sitting felt right — that sitting *is*
  the cadence this policy institutionalizes.

## OI-3 — Push decision

- **Decision:** whether/where to push. `MultiRepoSupport` is local-only (~48
  commits); branch `derived-gate-model` adds the derived-gate campaign + the
  open-items-surface campaign on top.
- **Blast radius:** durability (one disk holds the only copy) vs. exposure
  (pushing to a public remote publishes — and no license is chosen yet, OI-4).
- **Options:** push to a **private** remote now (durability, no exposure) ·
  stay local until OI-4 rules public intent · push public after OI-4.
- **Recommendation:** private remote now; the public question is OI-4's and
  doesn't block backup.

## OI-4 — WI-097: LICENSE decision

- **Decision:** which license, and whether the kit is headed public (the
  deep-review-b H3 finding; WI row: [work-items.csv](requirements/work-items.csv)).
- **Blast radius:** the legal terms of every downstream adoption — the kit's
  whole model is copy-in, so the license travels with every scaffold.
- **Options:** **MIT** (max adoption, simplest copy-in story) · **Apache-2.0**
  (adds an explicit patent grant; slightly heavier notice obligations) · **stay
  private / no license** (default all-rights-reserved; blocks outside use).
- **Recommendation:** none recorded — this needs the owner's public/private
  intent first; it's the gating input OI-3's public option also waits on.

## OI-5 — WI-098: history-provenance comments in the kit masters

- **Decision:** keep, thin, or strip the `(REVIEW_*/THREAD_*)` provenance
  comments in the kit **masters** (the strip-at-scaffold precedent shipped
  2026-07-13, so downstream readers already inherit none — this is now purely
  about the masters' own readability).
- **Blast radius:** kit-source readability vs. design archaeology; could absorb
  the design-doc citations (`AGENT_ROLES`/`IMPROVEMENT_PLAN`) the
  scaffold-strip left in scope.
- **Options:** keep (archaeology intact) · thin to log/archive pointers ·
  strip entirely.
- **Recommendation (driver):** thin — the scaffold-strip precedent showed the
  citations aren't load-bearing for readers, and the archive holds the history.

## OI-6 — WI-103: PROCESS_OPTIONS byte budget + applies-when index

- **Decision:** give PROCESS_OPTIONS.md a byte budget + an applies-when index
  table (deep-review M5); any further doc *split* is an owner-taste call.
- **Blast radius:** shipped-doc structure churn; §-numbering stability
  (`§N` cross-refs pervade the kit).
- **Options:** budget only · budget + index table · full split (taste).
- **Recommendation (driver):** budget + index; defer the split until the file
  actually fights its budget.

## OI-7 — WI-123: review-cadence dial

- **Decision:** campaign-close 2× adversarial review instead of per-slice
  (owner-raised 2026-07-12; spec: [specs/WI-123.md](specs/WI-123.md)).
- **Blast radius:** the unattended loop's defect-catch latency — per-slice
  reviews are the escalation sensor the medium-BUILD relax leans on.
- **Options:** adopt campaign-close cadence now · keep per-slice · wait for
  evidence.
- **Recommendation (recorded):** rule only after ≥ 2 campaigns of medium-BUILD
  evidence.
