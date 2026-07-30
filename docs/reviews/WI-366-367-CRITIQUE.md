# WI-366-367-CRITIQUE — periodic advisory render critique of the port-fan + viewBox changes

**Date:** 2026-07-30 · **Instrument:**
[dashboard-usability.md](../rubrics/dashboard-usability.md) (this critique
judges T8's two open residues: the WI-323 port-fan finding and the
canvas-clip stubs) · **Mode:** same-family with both implementers
(documented degraded-legal mode — compensated, as the WI-323 critique did,
by grading every recorded residue adversarially rather than accepting the
implementers' accounts). Advisory post-RULING-5: this verdict gates
nothing; it is evidence. **Evidence:** the full
`scripts/dashboard-shots/shots/` matrix (gitignored, machine-local,
regenerated at trunk `1858f78`) plus 4 Playwright-clipped close-ups of the
named sites at 1680px/2x (scratchpad, ephemeral). Both builders' and both
reviewers' pixel measurements were made independently earlier the same day
and agreed with each other; this critique READ the rendered pixels rather
than re-measuring them a third time, and says so.

## VERDICT: BOTH RESIDUES CLEARED AS FILED — no new finding worth a WI

1. **Port fans (WI-366's clause) — reads as fans.** Right of the
   `unphased` block's out-port: five strands leave the port and are
   individually attributable within a short run — white space between
   every adjacent pair, no composite-dark fused band, in both themes. Right
   of block 1's out-port: the formerly-fused pair is three visibly separate
   strands curving to distinct lanes. The x-staggered departure rises are
   what makes the fan legible — strands part at the port, not far from it.
2. **Canvas-clip stubs (WI-367's clause) — gone.** At both former clip
   planes every wrap-around lane draws its full U-turn: the long
   horizontals now END in a visible turn that connects to a port, in light
   and dark, on the roadmap AND the How-SW root (whose right-edge orphan
   stubs merged into their strands). "A line that stops at nothing" no
   longer describes any lane on either routed tab.
3. **No collateral damage seen.** No lane crosses a node box; 390px is
   unchanged (scroll cue present, no page-level horizontal overflow; the
   mid-page sticky header in the full shot is the documented capture
   artifact, confirmed against the fold shot); the −1.2%/−2.2% fit-scale
   cost of the wider boxes is imperceptible at reading distance, though
   the How-SW labels remain the smallest text on the page (recorded
   residue, panel-layout territory — the WI-367 record's finding 3).

## Residues that remain open, adversarially re-read (none new, none hidden)

- The `unphased` port's tightest adjacent pairs clear 8 CSS px at ~15.6–19
  px out rather than within 15 (recorded in WI-366's Deliverable; visible
  in the crop as a slightly later part-point on two strands — it does NOT
  read as fusion).
- Block 1's flagship pair sits at ~7.9 CSS px rendered after WI-367's
  1.23% scale-down (a recorded letter-miss of WI-366's CSS-px clause,
  judged marginal in WI-367-REVIEW-A finding 1; the crop reads as two
  clean strands).
- One `unphased` INPUT-fan pair never reaches 8 px within its window
  (WI-366's recorded residue; not visually prominent).
- The full two-phase route-then-refan pass remains the deferred design if
  the letter of "8 px within 15 px" is ever promoted from advisory to
  bound — nothing seen today argues for building it.

## Not verifiable from this session's pixels

Hover/focus interaction (static shots); the Process/What/Knowledge tabs
(HTML, not routed SVG — T8 does not bite); comparative BEFORE shots (the
changes merged this session; the BEFORE evidence lives in the WI-366/367
records and their independent review reproductions, not in a parallel
shot set).
