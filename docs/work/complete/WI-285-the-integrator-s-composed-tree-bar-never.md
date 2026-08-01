+++
id = "WI-285"
title = "The integrator's composed-tree bar never runs - _run_combined_bar reads docs/stack.ini [stack] test but the kit declares its harness under [product] test = {py} -m pytest, a schema mismatch, so every integration (WI-275/279 + all historical) journals 'skipped (no declared test command)' and fail-opens; run the bar the repo actually declares (check.py/[product] with {py} substitution) and stop the declared-but-unread-key silent pass"
workstream = "scripts"
buildtier = "medium"
priority = 1
safety_class = "ordinary"
order = 282
+++

## Deliverable

Integrated from train p0-g3-WI-285-76a8 @ 57deedc: WI-285: fail closed when the composed-tree bar's binary is missing (rework)
