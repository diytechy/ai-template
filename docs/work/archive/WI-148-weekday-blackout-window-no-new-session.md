+++
id = "WI-148"
title = "Weekday blackout window - no new sessions inside configured UTC hours"
workstream = "unattended"
needs = ["WI-023", "WI-024", "~WI-147", "WI-145"]
order = 147
+++

## Deliverable

agent_loop.py honors docs/blackout (parse_blackout + blackout_wake helpers, top-of-loop boundary check): a HH:MM-HH:MM UTC Mon-Fri half-open window starts no new session - the loop waits it out and resumes automatically (a single walk-away launch survives the blackout). start==end / absent / malformed = disabled (byte-identical); wraps past midnight. blackout.template scaffolds the 12:00-19:00 default (bootstrap SCAFFOLD + test_scaffold_contains + a default-value test). PROCESS_OPTIONS unattended section documents it (+742 B, baseline re-stamped 136,841). 5 tests (parse edges, boundary minutes, disable/weekend, wrap, present-but-inactive end-to-end).
