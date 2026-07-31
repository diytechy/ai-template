+++
id = "WI-377"
title = "Make the integrator's bar step count honest: integrate.py's _run_bar counts every line matching PASS in check.py's output, but under --jobs each step's status line prints TWICE (once by the lane runner, once in the final summary block), so a 20-step G3 bar is recorded as \"bar PASS (40 steps)\" - the figure already sits in log entries and in WI-374's own spec title as if it were 40 units of work. Count only the summary block (split on check.py's `=` banner) or, better, have check.py emit one machine-readable total line the integrator parses - whichever is smaller; add a regression test pinning that a --jobs>1 run and a --jobs 1 run report the SAME step count. Cosmetic in behavior, but the recorded evidence is the thing this kit treats as load-bearing, and a doubled step count is a false measurement in the merge record."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

_run_bar now reports the count of DISTINCT step names among check.py's PASS lines (_passed_steps, a pure helper), which is identical at --jobs 1 and --jobs N - a 20-step bar reports 20. Chosen over the filed banner-split option because it needs no check.py change and cannot silently fall back to double-counting on a banner-format change; the deviation and its reason are recorded in the log fragment. One regression test pins the property the row asked for (the doubled --jobs output shape and the serial shape of the same plan report the same count) plus the malformed-line guard (a name-less PASS line is skipped, FAIL/SKIP never count). Existing log entries that say "40 steps" stand as history of what the tool printed.
