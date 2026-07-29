+++
id = "WI-261"
title = "L-32 ruled intended, clarity WI (owner 2026-07-21, repo-review-2026-07-21 L-32): both shipped defaults STAY - privacy-check off (the documented fail-open exception) and the active 12:00-19:00 UTC weekday blackout. Deltas: (1) make the intent unmissable - template/doc wording states plainly that blackout is weekday-only (already implemented, agent_common.blackout_wake skips Sat/Sun) and is honored by the agent-resume -> agent_loop path; (2) stronger terminal feedback when a session pauses for blackout - replace the single one-line print (agent_loop.py ~2275) with a prominent banner naming the policy file (docs/blackout), the window, weekday-only scope, and the resume time, plus a periodic countdown heartbeat so a walk-away launch is visibly waiting rather than hung. No behavior change to the window semantics themselves"
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
order = 258
+++

## Deliverable

Blackout pause feedback (agent_common.py + agent_loop.py, L-32 clarity WI): the single one-line pause print is replaced by a prominent multi-line banner (naming docs/blackout, the HH:MM-HH:MM UTC window, the weekday-only Mon-Fri scope, and the resume time) plus a periodic countdown heartbeat (BLACKOUT_HEARTBEAT_SEC=300) via pure/injectable helpers blackout_banner/blackout_countdown_line/blackout_wait, so a walk-away launch is visibly WAITING not hung; the weekday-only intent is made unmissable in the module docstring. NO change to the window semantics (sum-of-sleeps==wake; weekday/disabled/malformed preserved - reviewer drove 84 combos). Adversarial REVIEW-A APPROVE f=0.
