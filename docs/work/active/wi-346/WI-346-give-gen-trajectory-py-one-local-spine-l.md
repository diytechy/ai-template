+++
id = "WI-346"
title = "Give gen_trajectory.py one local spine loader and one capture helper (docs/dupes-allow: spine-load-repeat 8, subprocess-capture 1 = 9 sanctioned blocks). Three functions each re-derive the SR/LLR/TC row filters from ct.read_rows. This is explicitly NOT the F5 case - F5 buys cross-SCRIPT copy-ability and a shared _kitcommon.py was rejected 2026-07-12, but every copy here is inside one file, so a module-local _spine(root) costs nothing and removes eight census blocks. The five-keyword subprocess.run capture block is the same pattern WI-304 extracted in agent_dispatch as _run_captured rather than sanctioning it. Distinct from WI-280, which owns this file's graph/render split, not its loaders. Triaged under WI-340."
workstream = "scripts"
needs = ["WI-340"]
specref = "docs/reviews/128-REVIEW-A.md"
buildtier = "medium"
priority = 0
safety_class = "ordinary"
order = 343
+++
