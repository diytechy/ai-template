+++
id = "WI-305"
title = "Dashboard has no next-work surface (119-CRITIQUE T1) - dashboard-usability.md's core reading task 2 (find the next work) has no path: with 0 active items nothing is marked you-are-here, the Process tab's resume-loop panel is a static method diagram carrying no data, and the only route to a queued item is When -> double-click a phase -> double-click a workstream -> scan for a queued node - the anchor's own bad case, expanding nested blocks to locate something. Fix: surface the ready/queued work items derived from the DAG (schedule.py's frontier, already computed for IF-071) on the landing view or within one tab switch, named, with their blocking predecessor. Re-affirmed 2026-07-26 against the amended SR-054 (the T1/T3 ruling retires T3 and rewords T1; T1 stays a LIVE critique anchor, so this defect is unaffected). WI-315 - the T1 binding - is gated behind this row: binding the anchor while its defect is open would be the lax classification the option-(f) ruling forbids."
workstream = "dashboard"
sr_refs = ["SR-054"]
buildtier = "medium"
safety_class = "ordinary"
order = 302
+++

## Deliverable

Delivered 2026-07-26 by dispatcher train 3-g2-WI-305-6f47, hand-folded onto the dev branch (the train could not integrate: it delivers SR-054 Verification=Critique, so a CRITIQUE APPROVE was required, but a whole-document critique also judges T2/T4/T5/T7 - anchors this train never touched; verdict at 54cf50f was CHANGES-REQUESTED findings=4, none of them WI-305's). The landing hero gains a NEXT WORK surface naming the scheduler's dependency-ready frontier (the same frontier IF-071 projects into status.md): ready WIs first, then waiting WIs each annotated with the blocking predecessor. INDEPENDENTLY VERIFIED by the train's own critique task exercise - 'next work: 0 tab switches / 0 clicks (NEXT WORK on the landing view)', the first time T1's core reading task has passed since 119-CRITIQUE. Verdict record preserved at docs/reviews/3-g2-WI-305-6f47/002-CRITIQUE-54cf50f.md.
