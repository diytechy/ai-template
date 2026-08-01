+++
id = "WI-385"
title = "Backlog re-evaluation after a re-attest"
workstream = "scripts"
buildtier = "medium"
safety_class = "ordinary"
+++

## Deliverable

RETIRED 2026-07-31, unbuilt — **folded into WI-388** (adjudication). The
behaviour ships; the separate row does not. Reasoning in
`docs/concurrency-v2.md` §A7.

**Original scope, kept as the record.** Warn when a queued WI cites an SR
amended after the WI was filed. A verdict goes stale when the tree moves under
it and the kit mechanizes that (`integrate._verdict_gate`); a WI's *premise*
goes stale when a cited SR is amended under it, and the kit does not check that
at all — `SR-Refs` is only ever tested for existence. If re-attest means scope
changed, every open WI citing an amended SR may be mis-scoped, redundant or
obsolete, and today it will be claimed and built as though nothing happened. It
was to be cheap (`ratify_check` and `_verdict_gate` both already do git-derived
is-X-older-than-Y comparisons), WARN and never gate, firing as the final step
of the dispatcher flow.

**Why retired.** The owner scoped adjudication (WI-388) to include *verifying
whether current work items in queue need adjustment or cancellation* — this
exact judgement, made by the same agent, on the same diff, at the same point in
the flow. A standalone warn would be a second and strictly weaker reader of one
fact: it can only say *re-read this*, where the adjudicator can cancel the row,
re-scope it, or file its replacement. One behaviour, one home.

The stated dependency on WI-380 survives inside WI-388 for the reason it was
written here: until the ratified-vs-traced cell split lands, this fires on every
WI whose cited SR was touched by a `Module`-pointer re-home — which is how a
warn gets switched off.
