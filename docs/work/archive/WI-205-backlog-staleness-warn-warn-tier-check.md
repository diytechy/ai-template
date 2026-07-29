+++
id = "WI-205"
title = "Backlog-staleness warn - warn-tier check_trajectory finding (the check_docs --stale idiom on the WI<->spine join): an OPEN WI whose cited SR rows or SpecRef target changed AFTER the WI row was last touched warns for a driven re-look (git-blame row timestamps; silent off-git; deferred rows exempt; any reviewed row touch re-affirms). Closes the backlog-semantic-currency gap: nothing re-evaluates incomplete WIs after spine ratification"
workstream = "scripts"
buildtier = "medium"
order = 204
+++

## Deliverable

WI-205 (2026-07-17): check_trajectory.backlog_staleness_findings + _blame_row_times/_path_commit_time - warn-only at every tier (never joins the exit code, even under --strict; the WI-129 stance): for each open (queued/active/blocked; deferred+done exempt) WI, one git blame --line-porcelain per registry CSV maps row id -> committer time; a cited SR row or SpecRef target (git log -1, memoized per path) STRICTLY NEWER than the WI row's last touch warns for a driven re-look; any reviewed row touch re-affirms. Silent off-git/untracked/uncommitted (no basis -> no warn, never a false one); bounded at <=2 blames + one log per distinct SpecRef path. 7 fixture-git tests (stamped commit dates; both directions + off-git + deferred-exempt + strict-stays-warn). Built by a parallel opus agent, root-reviewed + integrated. Live dogfood: first run flagged WI-204's spec amended after its row was filed - a true positive, triaged in the log.
