+++
id = "WI-250"
title = "Process tab working loops rendered as CSS-grid 'racetracks' with no visible flow direction or clear shared junction - redraw as two intersecting SVG hoops, each a directed closed cycle of arrow-wired stage cards meeting at one shared LLM_Agent hub"
workstream = "dashboard"
sr_refs = ["SR-070"]
buildtier = "medium"
safety_class = "ordinary"
order = 247
+++

## Deliverable

_loop_panel rewritten from the grid-racetrack markup to one self-contained SVG (_loop_svg): two overlapping .hoop discs whose lens holds the single .hub (LLM_Agent, rendered once), each loop a directed hub->s1->..->sn->hub cycle wired by outward-bowing .floop edges carrying one floparrow marker apiece (11 edges), stage cards keyed data-node a-*/b-* and linked to their canonical homes, loop names in the top margin clear of the cards. Fixed-geometry trig (math, .1f rounding) keeps --check byte-stable and a data-less repo renders identically; scales to the panel width with no 390px overflow. TC-056 Expected + verification-detail rewritten from racetrack/grid wording to the hoop structure; the process-loop tests re-pointed at the SVG structure; OKF TC-056 regenerated. Verified light+dark + 390px; full suite green.
