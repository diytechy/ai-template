+++
id = "WI-1067"
title = "WI-1066's verdict answered: SR-207 fronts its event and states its retirement rule; TC-560 drives two more faults"
workstream = "process"
specref = "docs/reviews/wi-1066-adjudicate-seventh-sitting/001-ADJUDICATE-123cd20.md"
sr_refs = ["SR-207", "SR-157"]
needs = []
buildtier = "medium"
planmode = "none"
safety_class = "ordinary"
priority = 2
+++

## Context

Filed on trunk on 2026-11-23 by the queue drill's coordinator, to answer
the seventh automated adjudication sitting's verdict (WI-1066, Gemini Neon,
the specref). Its two `### Dispositions` drafts name this row's scope; the
two are one row because both are small and text-led, and neither waits on
the other.

**SR-207 (MEANING, not blessed; still `Accepted`, owed at its recorded
text).** WI-1060 rewrote it from "refuse the act while an unnamed row has
drifted" to "leave every unnamed drifted row at its recorded text". The
sitting asks two things:
1. Its requirement fronts its event condition in the EARS event form
   ("When the kit takes an acceptance act, it shall leave ..."), rather
   than burying ", in an acceptance act," after "shall leave".
2. Its acceptance criteria state the retirement rule the requirement
   already names: an unnamed recorded accepted row that live no longer
   carries stays in the recorded copy and is named owed, and an act naming
   that row retires it from the recorded copy.

The coordinator adds one item from reading the row: its rationale's list of
"adjudicated links" (a requirement's needs and boundary crossings, a design
row's requirements, a test case's verified rows) predates WI-1024, which
routes a requirement's or design row's `constrains` link to adjudication
too (LLR-420; `record_rows.ROUTED_TRACED_CELLS`). The list names that link
as well, so the row stays true to the code. The builder confirms from the
code that the record keeps a row whose `constrains` link alone changed, and
says so; if it does not, the builder stops and reports.

SR-207 is the acceptance act's rule, and WI-1060's record says its
amendment is shown to the operator; this row's rewrite is shown with it.

Critiqued 2026-11-23 (`docs/reviews/2026-11-23-scope-critiques/WI-1067.md`):
the `constrains` check is a Done-when item of its own.

**TC-560 (RETURN; still `Drafted`).** It verifies LLR-480 but leaves two
of its fault branches undriven, in its method, expected and tests:
1. A design row whose parent cell names an example row (an id ending
   `-000`, which is not a live design row).
2. A design row whose parent chain reaches a cycle (a row below the cycle,
   not on it), reported naming the row where its chain breaks.
Each runs at both `Drafted` and `Accepted` and through both the orphan
pass and the strict check, as TC-560's other faults do. If a test shows
the code does not do what LLR-480 says for either, the builder stops and
reports; LLR-480 was accepted by this sitting and is not amended here.

## Done-when

- [ ] SR-207's requirement opens with its event condition; its acceptance
      criteria state the retirement rule (kept and named owed while
      unnamed, retired when named), each clause driven by a test its test
      cases name; its rationale's adjudicated links include the
      `constrains` link. The amendment is text only; SR-207 stays
      `Accepted`, owed to the next sitting.
- [ ] The Deliverable reports, from the code and a test, that an act keeps
      a row whose `constrains` link alone changed (LEFT OWED, in `kept`)
      until an act names it; if it does not, the builder stops and reports
      before amending SR-207's rationale.
- [ ] TC-560's method, expected and tests drive both missing faults at
      both statuses, red first where a test is new; TC-560 stays
      `Drafted`, owed to the next sitting.
- [ ] Each row it touches keeps the three row rules (no code names,
      inherited ones included; one obligation with every clause tested; a
      child within its parent).
