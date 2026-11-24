+++
id = "WI-1064"
title = "The parent-first rule reads a child design row's authored parent link, as it reads a design row's requirements"
workstream = "process"
specref = "docs/archive/work/complete/WI-1027-parent-llr-link.md"
sr_refs = ["SR-245", "SR-246"]
needs = ["WI-1027"]
buildtier = "medium"
planmode = "single"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed on trunk on 2026-11-23 by the queue drill's coordinator, from
WI-1027's plan (F-7, the specref), its second decision. F-7 adds an
authored `parent` link: a child design row names one parent design row and
carries no requirement link of its own. The parent-first rule (SR-245,
SR-246, LLR-357, LLR-358) states a closed list of edges: a requirement's
needs, a design row's requirements, a test case's verified rows. A child
design row's parent is not among them. So once F-7 lands, a child can be
accepted under a parent design row that stays `Drafted`, and neither the
standing integrity finding nor the commit hook's parent-first step reports
it. F-7 keeps that closed list unchanged on purpose, since its rows and
test case state the list. This row extends it.

The derived act's waiting flips (WI-1059) read the parent-first rule's own
findings, so they follow the new edge with no change of their own.

Critiqued 2026-11-23 (Sol and Hydrogen;
`docs/reviews/2026-11-23-scope-critiques/WI-1064.md`): `planmode` is
`single`, since the edge reaches three admission routes, and the edge holds
at each of them.

## Done-when

- [ ] The parent-first rule treats a child design row's parent link as a
      declared parent edge: an accepted child under a parent design row
      that does not claim acceptance is one parent-first finding, with the
      same wording and remedy as the existing edges, at every route that
      judges the existing edges: the standing integrity check, the commit
      hook's staged check, and a supported lane commit's admission (the
      interface carrying the parent-first findings to a lane, IF-308). The
      new edge inherits the existing edges' classification, exclusions and
      status-movement conditions unchanged.
- [ ] Coverage bound: the promise reaches registries as supported
      workflows and the kit's own routes write them; hand-edited kit-written
      state is outside it (PROCESS.md §6, "Review threat model").
- [ ] A test shows each: the standing finding, the staged refusal, the
      lane commit's refusal, a simultaneous parent-and-child acceptance
      passing, and a derived act naming such a child as waiting.
- [ ] SR-245's, SR-246's, LLR-357's and LLR-358's amendments (text only, no
      code names) and their test cases' are listed in the Deliverable as
      owed to adjudication.
