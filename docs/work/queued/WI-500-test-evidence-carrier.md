+++
id = "WI-500"
title = "The test-evidence carrier: the input that makes DevStg-Release reachable (owed by the ruled stage unification plan)"
specref = "docs/plans/2026-08-21-stage-unification-plan.md"
workstream = "scripts"
sr_refs = ["SR-151", "SR-152"]
needs = []
buildtier = "strong"
safety_class = "spine"
priority = 2
+++

## Context

The ruled plan (§5, sequencing note) names this as its own row: WI-498
made `DevStg-Release` evidence-gated with — deliberately — NO producer, so
the rung is unreachable until a test-evidence carrier exists. This row
builds the carrier: a durable, committed record that the declared test
suite ran and every test case passed, produced by the HARNESS (the OI-30
D2 rule survives: no Status cell, and no hand-written file, may ever be
the source of "the evidence passed").

Design constraints gathered by the program (read the plan + the design
record + the slice-3 fragment section before shaping):
- The evidence sources measured ABSENT today, all four: no TC outcome cell
  (by ruling — stays that way), docs/test reports gitignored,
  coverage.json opt-in and deleted per run, no junit/json-report anywhere.
  The carrier is NEW state, and its trust model is the design's heart:
  what makes a committed evidence file believable (producing command +
  revision binding, the declared-figure/fig: discipline, staleness =
  unreachable again)?
- Once it exists it joins `kitlib/stage.DECLARED_INPUTS` (the one-list
  edit the input design promised) and `spine_stage`'s Release
  discriminator consumes it; the slice-3 structural pin (source contains
  no `return STAGE_RELEASE`) is then retired DELIBERATELY with the
  producer's arrival recorded.
- The evidence claim binds to the TREE it was measured on (the WI-492
  correction-record precedent: value-bound, not space-bound), or Release
  silently rides stale evidence — the failure class the whole unification
  exists to prevent.
- Adopter-facing throughout: RESYNC entry, scaffold verification, and the
  shipped ci lane is the natural producer (a harness driver writing the
  record on a green full run).

**Orphan fold-in (owner-directed 2026-08-22):** this row's build DISCHARGES
the decomposition debt on `SR-151` (hosted CI runs the declared bar per
trigger) and `SR-152` (the hosted CI verdict is the harness's own) — the
two orphaned SRs whose subject IS this carrier and its CI-lane producer.
Mint their LLR/TC rows as part of the design, so the carrier lands traced
rather than rowless.
