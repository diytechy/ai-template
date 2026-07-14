# Open items — owner decision briefs

The **single owner-review surface**: one section per pending decision, with the
context needed to rule — what's being decided, blast radius, options with
pros/cons, and the driver's recommendation. [status.md](status.md) carries only
the one-line form of each; the DAG rows live in
[work-items.csv](requirements/work-items.csv). **A section lives here only
while the decision is pending** — the ruling appends to [log.md](log.md)'s
Decisions log and the section is deleted. (Format:
[specs/open-items-surface.md](specs/open-items-surface.md).)

_The 2026-07-13 sitting ruled OI-1 (G3 re-attestation — ratified), OI-2
(single-ratify enablement — accepted), OI-5 (WI-098 — thin) and OI-6 (WI-103 —
budget + index). The 2026-07-14 sitting ratified OI-8 (the `[v3]-[g2]`
dashboard-ux batch) and OI-9 (the research-knowledge design spec, as revised) —
records in the log's Decisions. OI-3 (corrected against git), OI-4, and OI-7
remain open._

---

## OI-3 — Push / sync decision

- **Decision:** whether to push the pending local commits on
  `derived-gate-model` (and, separately and later, whether/when to integrate
  the branch into `main`).
- **Git-checked facts (2026-07-13; re-verify at read time — an open-item claim
  about git state must come from git, not memory):**
  - remote `origin` exists (`github.com:diytechy/ai-template`);
  - `derived-gate-model` tracks `origin/derived-gate-model`, **ahead 9** at
    check (10 with the ratification commit that lands this brief) —
    verify: `git fetch --prune && git branch -vv`;
  - `MultiRepoSupport` is **in sync** with its remote;
  - `main` is 340 commits behind this branch
    (`git rev-list --count main..derived-gate-model`) — the eventual
    integration question, **not** part of the routine push.
  - _(The earlier "local-only, ~48 commits" claim was stale and wrong —
    corrected at the 2026-07-13 sitting.)_
- **Blast radius:** durability of ~10 commits of ratification + campaign work
  (one disk holds them until pushed). The branch is already public-remote
  tracked, so pushing adds no new exposure.
- **Options:** authorize the push (`push-policy` = `human`: you push, or
  explicitly authorize the agent once) · hold.
- **Recommendation:** push — the branch is already tracked upstream; the
  unpushed commits are pure durability risk. The `main` integration is a
  separate, later sitting.

## OI-10 — Review-034 findings against WI-141 / SR-051 (drill render)

- **Decision:** how to disposition the two `@owner`-routed findings the
  session-034 REVIEW-A ([reviews/034-REVIEW-A.md](reviews/034-REVIEW-A.md),
  gpt-5.6-terra, CHANGES-REQUESTED) raised against the landed WI-141 render —
  neither is auto-fixable, both touch ratified SR-051 territory.
- **The findings (verified against the code, 2026-07-14):**
  - **[MAJOR] phase not surfaced in leaf WI blocks.** `gen_trajectory.py`
    `wi_block()` puts the delivery Phase in neither the block label/sub nor the
    hover title. When the phase tier does **not** fire (≤3 phases) but the
    workstream tier does (>3 workstreams), a viewer descends into a mixed-phase
    workstream and the per-WI Phase — which SR-051 says the When view "surfaces
    each work item delivery Phase" — is no longer visible. Real but edge-case
    (the common path carries phase in the breadcrumb of the descended layer).
  - **[MINOR] threshold wording inconsistency.** LLR-052 says component blocks
    explode only above `TOP_VIEW_MAX` (10) while SR-051 requires the component
    tier above 3 and the renderer drills even at 2 — the intended ≤3 threshold
    should be stated consistently across SR-051 / LLR-052 / TC-052.
- **Blast radius:** cosmetic/traceability only — no wrong data renders; the gap
  is a missing annotation on one edge-case path plus a doc-wording mismatch.
  Both are exactly the "graphic breakdowns will need iteration" the OI-1
  ratification anticipated (amendments as future WIs, not blockers).
- **Options:** (a) fold both into the already-queued **WI-143** (SR-056
  decomposition render polish) — add phase to the leaf `wi_block` hover/text +
  reconcile the SR-051/LLR-052/TC-052 threshold wording, since WI-143 already
  reopens this renderer · (b) file a dedicated fix WI · (c) accept-as-is (the
  common path surfaces phase; deem the edge case out of SR-051's intent).
- **Recommendation:** (a) — WI-143 is the render-polish slice touching this same
  code; folding the phase-annotation fix and the doc-wording reconcile into it
  is the smallest change and keeps WI-141's ratified Verified status intact
  (making code match the SR, not reopening the phase). No new WI needed.

## OI-4 — WI-097: LICENSE decision

- **Decision:** which license, and whether the kit is headed public (the
  deep-review-b H3 finding; WI row: [work-items.csv](requirements/work-items.csv)).
- **Blast radius:** the legal terms of every downstream adoption — the kit's
  whole model is copy-in, so the license travels with every scaffold.
- **Options:** **MIT** (max adoption, simplest copy-in story) · **Apache-2.0**
  (adds an explicit patent grant; slightly heavier notice obligations) · **stay
  private / no license** (default all-rights-reserved; blocks outside use).
- **Recommendation:** none recorded — this needs the owner's public/private
  intent first.

## OI-7 — WI-123: review-cadence dial

- **Decision:** campaign-close 2× adversarial review instead of per-slice
  (owner-raised 2026-07-12; spec: [specs/WI-123.md](specs/WI-123.md)).
- **Blast radius:** the unattended loop's defect-catch latency — per-slice
  reviews are the escalation sensor the medium-BUILD relax leans on.
- **Options:** adopt campaign-close cadence now · keep per-slice · wait for
  evidence.
- **Recommendation (recorded):** rule only after ≥ 2 campaigns of medium-BUILD
  evidence.
