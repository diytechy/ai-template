# SN-036 decomposition review brief

Scope: the SN-036 owner amendment, SR-161/LLR-183 and the H2/H3/H5 chain
(SR-184–186, TC-209–211). Review the owner-authorized change in the supplied
source; do not approve artifact statuses or infer inspection results.

Hat questions below are produced by `plan_briefs.hat_surface_for_work_item`
with this exact declared work context and each referenced SR’s parent needs:

```json
{
  "Workstream": "process",
  "SafetyClass": "spine",
  "SR-Refs": "SR-161;SR-184;SR-185;SR-186"
}
```

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

Record a reasoned outcome for every applicable hat, and identify the independent
purpose of each child and why further splitting stops. Use the existing
[change-review rubric](../rubrics/change-review-records.md), challenge it against
SN-012/SN-024/SN-036/SN-037 intent, and cite its revision and numbered anchors.
Missing outcomes are review findings, never a new coverage gate.
