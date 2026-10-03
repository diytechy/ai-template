+++
id = "WI-758"
title = "Separate wires that share a lane at the port fans, and bind 'no two distinct edges share a segment' as a test (TC-055 T8)"
workstream = "scripts"
specref = "project-trajectory/scripts/rendering/traj_graph.py"
sr_refs = ["SR-054"]
needs = []
buildtier = "medium"
safety_class = "spine"
priority = 3
+++

## Context

Filed 2026-10-03 by the coordinator from WI-754's cross-family re-judge of TC-055
(RECORDED fail on T8 only; `docs/reviews/wi-754-re-judge-tc-055-declared-inpu/001-REJUDGE-6e89705b.md`).
T8 failed twice running (WI-713, WI-754). WI-750 removed the crossings WI-713 named,
but its How-view lane change left distinct edges sharing segments:

- **How view, default CMP-006 selection:** CMP-006->CMP-009 (orange) and
  CMP-008->CMP-006 (blue) run on the same x=452 (22 units overlapping) and meet
  end-to-end at (452,71); likewise at (220,71). The hub reads as a chain
  CMP-007 -> CMP-008 -> CMP-009 -> CMP-006. Three same-coloured arrowheads converge
  into CMP-006's in-fan ~17 CSS px apart. Each inter-box gap is ~50 CSS px.
- **When roadmap (1280 px):** 26 pairs of edges sharing no endpoint are drawn over
  each other along a shared lane (the longest 864-872 of 1748 units).

The owner's direction (2026-10-02, WI-747): LLM judgement should not run more than it
must. A judge noted the How-view overlap can be bound as a test. Binding the
clause mechanically means TC-055's T8 stops depending on an LLM for it.

## Done-when

- The router gives each edge its own channel where the geometry allows: no two
  edges that share no endpoint overlap along a segment, and no two edges meet
  end-to-end at a point that is not a shared endpoint, in the How, When and Process
  views as emitted. Where the geometry genuinely cannot separate two edges, the code
  says why and the test names the case.
- A test over the EMITTED SVG paths of every wired view asserts it (segment overlap
  and end-to-end joins between unrelated edges), and would fail at 6e89705b.
- The clause is bound: draft a test-case row (Drafted, for the merge's first
  approval) verifying LLR-120 or a new LLR for lane separation, and amend the
  rubric's T8 text in place to say the lane-separation clause is test-bound (the
  rubric names bound clauses in its header); TC-055 then judges only what remains.
- Every `tests/test_traj_*.py` module and the smoke tier pass; TC-055 is due again at
  the merge and is re-judged cross-family.
