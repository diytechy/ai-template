# Rubric — Spec/plan interface hygiene (WI-191)

**Adjudicates:** the reviewer/critique-tier gap the mechanical check cannot close
([enforcement-audit.md](../enforcement-audit.md) finding 4) — whether a
spec-of-record's `## Interfaces` section (or a proposed decomposition's per-WI
`IF-###` citations) honestly **reuses** the declared seam registry instead of
near-duplicating it.
**Used by:** a plan/spec CRITIQUE session — the WI-191 reviewer-tier check, and
**WI-190's** dual-plan protocol imports **B1** as its seam-duplication anchor.
`check_trajectory` verifies that citations *resolve* — and, since WI-442
retired the rationale arm with its arming input, nothing else. So this rubric
carries the whole load below that line: does the citation carry a rationale at
all, is it *true*, and is the new seam *actually* new?

The verdict is `VERDICT: APPROVE|CHANGES-REQUESTED findings=N`, each finding
citing an anchor id (`B1`…). Judge the seams as a first-time reader of
[`interfaces.toml`](../requirements/interfaces.toml), not the spec's author.

## Anchors

**B1 — Near-duplicate seam.** A `Proposed` seam proposes a near-duplicate of an
existing `IF-###` instead of **consuming or amending** it. *Bad:* a new
`Provides` row whose contract restates an existing seam with a renamed endpoint;
a citation whose "nearest existing IF" is one the proposed contract in fact
duplicates. *Good:* the spec cites the existing IF and consumes it, or files a
one-line amendment, and mints a new row only when no existing seam spans the
surface (the search genuinely came up empty).

**B2 — Dishonest or absent rationale.** A `Proposed` citation's rationale does
not truly name the **nearest** existing seam, or hand-waves "no existing seam"
without evidence of a search. *Good:* it names a concrete `IF-###` and states
the specific reason it falls short — wrong direction, wrong counterpart,
incompatible contract.

**B3 — Speculative seam.** A seam is proposed before a second consumer exists —
the §8 failure mode (interfaces defined early get bypassed and re-invented). A
spec that could act within one module, or through an existing seam, but mints a
new one anyway. *Good:* intra-module work states the escape and cites nothing; a
seam is minted only when a real second consumer is in hand.
