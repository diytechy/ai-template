+++
id = "WI-750"
title = "Fit the system-context crossing captions to their lane, and minimise avoidable wire crossings (TC-055 T4, T8)"
workstream = "scripts"
specref = ""
sr_refs = ["SR-054"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

TC-055's T4 and T8 findings from WI-713, answered:

- **T4:** each System-context crossing caption is fitted to the measured gap
  between the party column and the system box from the token-derived estimate
  (`_BSUB_CH`, 0.667 em: 33 characters, 231 of the lane's 234 units), painted after
  the boxes, and ends in a visible ellipsis when cut; relationship labels sit clear
  of their curves. Tested over the emitted SVG.
- **T8:** the Process station's merged/partial exits swapped; the How view orders
  nested lanes and same-row ports geometrically with staggered turns; the When
  roadmap's detour trunk clears the "1+5" and "4" output fans. Each tested over
  emitted geometry. Stopped, documented and pinned: the When roadmap's cyclic
  return-route and perimeter crossings, which need joint routing beyond this row
  (`traj_render.py`); TC-055's next re-judge decides whether a successor is needed.
- **Also:** `tests/test_traj_graph.py`'s frame-padding pin read the pre-WI-722 0.62
  floor and was red on trunk since 6a40d7b2; it now reads the token-derived floor.
- No row and no golden fixture changed.
- **Review:** Sonnet 5.5 SOUND at 9884f643, two minors
  (`docs/reviews/2026-10-02-wave7/sonnet-wi750.md`).

## Context

Filed 2026-10-02 by the coordinator from WI-713's cross-family re-judge of TC-055
(RECORDED fail; `docs/reviews/wi-713-re-judge-tc-055-declared-inpu/001-REJUDGE-cafa07ab.md`).
Three independent Claude Opus judges, one per width, on native-resolution tiles.

**T4 (fails at 390, 1280 and 1680 px, both themes).** In the How tab's
System-context (depth-0) diagram each crossing's `carries` caption is wider than
its wire lane and is drawn before the boxes, so the external-party cards cover its
start and the system box covers its end ("…packaged deliverable. The delivere").
The caption is cut by character count (`rendering/traj_context.py`, `carrymax = 54`)
and centred in the 246-unit gap between the party column (x 364) and the system box
(x 610). It uses `--nsub`, which WI-722 raised from 8.5 to 10.5 px, so the 54-char
cut sized for the old scale no longer fits: the likely cause. At 1680 px the dotted
REL-002 curve also runs through its own label.

**T8 (MAJOR at 1680 px, MINOR at 1280 px).** Avoidable crossings:
- the Process station cycle: the curves from "Lane build" to "merged" and to
  "partial" cross just below their shared source (swap the exit points);
- the How top view: the lane order is reversed in both colour families, so the
  descending verticals cut the sibling lane before converging into CMP-006's input
  fan;
- the When roadmap: a vertical routing trunk runs about 7 CSS px from the output
  ports of "1+5" and "4", crossing the stubs at the fans; perimeter-routed wires
  cross every lane.

## Done-when

- The context captions are fitted to the measured lane gap from the emitted type
  token (the WI-722 pattern: a token-derived per-character estimate pinned to a
  band), drawn so no box covers them, and end in a visible ellipsis when cut; the
  REL-002 label sits clear of its own curve. A test reads the emitted SVG and
  asserts every caption fits between the boxes at natural size.
- The three T8 crossings are removed or justified (a crossing the layout cannot
  avoid is named in a comment and the test), each with a test over the emitted
  geometry where the router decides it.
- The slow traj tests and the smoke tier pass; TC-055 is then due again at the
  merge (its declared inputs change) and is re-judged cross-family on native tiles.
- Not in scope: the non-anchor observations in the verdict (they are the owner's
  to file if wanted).
