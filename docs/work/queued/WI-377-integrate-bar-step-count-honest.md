+++
id = "WI-377"
title = "Make the integrator's bar step count honest: integrate.py's _run_bar counts every line matching PASS in check.py's output, but under --jobs each step's status line prints TWICE (once by the lane runner, once in the final summary block), so a 20-step G3 bar is recorded as \"bar PASS (40 steps)\" - the figure already sits in log entries and in WI-374's own spec title as if it were 40 units of work. Count only the summary block (split on check.py's `=` banner) or, better, have check.py emit one machine-readable total line the integrator parses - whichever is smaller; add a regression test pinning that a --jobs>1 run and a --jobs 1 run report the SAME step count. Cosmetic in behavior, but the recorded evidence is the thing this kit treats as load-bearing, and a doubled step count is a false measurement in the merge record."
workstream = "scripts"
specref = "docs/concurrency-restructure.md"
buildtier = "quick"
safety_class = "ordinary"
+++
