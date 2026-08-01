+++
id = "WI-345"
title = "Extract agent_loop.py's verdict plumbing (docs/dupes-allow: verdict-plumbing 3, exe-presence 1 = 4 sanctioned blocks). The managed-session verdict path - mkdir the parent, unlink a pre-planted file, then read-and-parse it - is duplicated between the review arm and the critique arm, and the comment explaining WHY the pre-plant unlink exists (repo-review 2026-07-21 M-22) sits in only one of them, so the other reads as a stray unlink. The build_argv -> shutil.which-or-exists launcher probe repeats at two sites. The two arms stay separate; only the plumbing moves. Triaged under WI-340."
workstream = "scripts"
needs = ["WI-340"]
buildtier = "medium"
priority = 0
safety_class = "ordinary"
order = 342
+++

## Deliverable

Extracted agent_loop's verdict plumbing into three named helpers, none sanctioned: fresh_verdict_path (mkdir + clear a pre-planted file, carrying the repo-review 2026-07-21 M-22 reason that previously existed in the review arm ONLY, leaving the critique arm's unlink reading as a stray line), read_verdict (exists -> read -> parse_verdict, identical in both arms) and launcher_exe (build_argv -> argv[0] -> which-or-exists, the 'is this model's CLI installed' preflight probe at two sites). The review and critique arms stay separate as the row required — only the plumbing moved; what each does about an unparseable VERDICT line is untouched. Census 196 -> 190: the 4 charged blocks plus 2 cross-script module-path blocks dissolved as a side effect (agent_loop's mkdir/exists/unlink copy stopped matching agent_common's), proven a removal not a re-stamp. route_session complexity 13 -> 11, re-stamped downward; agent_loop.py 3042 -> 3072.
