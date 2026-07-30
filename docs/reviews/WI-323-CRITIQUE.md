# WI-323-CRITIQUE — periodic advisory render critique of the corridor-lane change

**Date:** 2026-07-29 · **Instrument:** [dashboard-usability.md](../rubrics/dashboard-usability.md)
(live anchors T2/T4/T5/T8; this critique judges T8's second clause) · **Mode:**
same-family with the implementer (documented degraded-legal mode — the critic
was told to compensate by grading the residue list adversarially, and did:
two of its five items were refuted as understated, one as misattributed).
Advisory post-RULING-5: this verdict gates nothing; it is evidence.
**Evidence:** the `scripts/dashboard-shots/shots/{,before/,compare/}` PNG
matrix (gitignored, machine-local); all measurements are device pixels from
the 2x-DPR shots, sampled with a stdlib PNG decoder — rendered pixels, never
source.

## VERDICT: IMPROVED (T8 second clause), with two localized regressions filed

The 121-CRITIQUE MAJOR — long coincident horizontal corridors — is measurably
gone. Stroke-compositing proof (a single wire renders rgb(123,137,156) on
white; two strokes on the same pixels composite darker), interior wire ink at
1680px light:

| | BEFORE | AFTER |
|---|---|---|
| single-stroke px | 7,644 | 19,426 |
| overlap (darker) px | 6,454 | 1,092 |
| overlap share | 45.8% | 5.3% |

BEFORE's two full-width "lanes" at crop y=367/y=488 sampled darker than a
single stroke — two edges drawn exactly on top of each other. AFTER, every
lane samples clean single-stroke ink; the tightest long-haul pair moved from
6.5 to 10 CSS px; per-column distinct strokes rose 4.53 → 7.55 with the
adjacent-pair population moving from the fused 8–16 dev band (299 pairs) to
the resolvable 16–24 band (528). Dark theme reads at least as well; no lane
crosses a node box (the T8 objective floor's "in open space" clause used
correctly); the ~2x taller wire envelope grew into gutters and margins and
does not hurt scanability, including at 390px.

## Where attribution still fails (ranked follow-ups, both FILED)

1. **Port fans — WORSE at two sites, one newly created** (→ **WI-366**).
   Right of the `unphased` block: two edges at 2.5–3 CSS px pitch for ~55 CSS
   px of descent (BEFORE: 3.5–5.5 px and diverging). Right of block 1: a NEW
   25 CSS px stretch where two edges render as one line (the second edge was
   routed there to reach the new y=346 lane). The implementer's residue list
   called the fans "unaddressed"; the pixels show them measurably worse.
   Also: the How-SW emitter's new lanes sit at 8 CSS px pitch against the
   roadmap's 10 (and a pre-existing 4.5 px SW pair) — the stated 10–14 px
   floor is not the floor.
2. **Canvas-clip stubs — pre-existing, now dominant** (→ **WI-367**). Hard
   ink boundaries at x=22/x=1406: every wrap-around lane ends flat at a clip
   plane and its continuation re-enters ~5 CSS px away — a line that stops at
   nothing and a curve that starts from nothing. Identical structure in
   BEFORE (the WI-257 stubs); WI-323's spreading pushed ~30% more edge ink
   against it. Misattributed as WI-323 residue by the implementer; it is its
   own item.

## Not verifiable from pixels

Which lane maps to which edge pair (inferred from compositing, not the
emitter — the critic did not read gen_trajectory.py); hover/focus
interaction (static shots); whether the x=22 boundary is viewBox clip or
routing margin; the Process/What/arch tabs (no BEFORE shots exist for them —
Process renders HTML chevrons, not routed SVG, so T8 does not bite there).
