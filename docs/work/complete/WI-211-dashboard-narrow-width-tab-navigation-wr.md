+++
id = "WI-211"
title = "Dashboard narrow-width tab navigation wraps instead of clipping off-screen"
workstream = "dashboard"
sr_refs = ["SR-052", "SR-054"]
needs = ["WI-189"]
buildtier = "quick"
order = 210
+++

## Deliverable

The shared dashboard nav.tabs style now wraps at narrow widths, keeping every labeled tab visible and operable at 390 px; the declared light/dark render matrix was regenerated and visually checked.
