+++
id = "WI-382"
title = "DESIGN DRAFT (docs/concurrency-v2.md §4) - do not claim until that doc is settled. Amortise the gate bar by composing ALL finished claimed branches onto one candidate and barring ONCE per drain, instead of once per branch. Measured 2026-07-31: the full G3 bar is ~11 minutes, of which tests+coverage is 634 s and all nineteen other steps total ~25 s - so three WIs handled singly cost three bars where grouped they cost one. This is the cheaper half of the owner's grouping requirement: it gets the 3-bars-to-1 win WITHOUT session grouping's failure coupling, because each WI is still built and reviewed independently and only the BAR is shared. Red-bar attribution is the trade: mitigate by falling back to per-branch barring on red, so a red drain still names its culprit. Already listed as one of the three Q2 bar-speed levers."
workstream = "scripts"
specref = "docs/concurrency-v2.md"
buildtier = "medium"
safety_class = "ordinary"
+++
