+++
id = "WI-137"
title = "Session telemetry commit hygiene + WI-keyed log labels"
workstream = "unattended"
order = 136
+++

## Deliverable

Off-spine dev-slice (2026-07-14, WI-136;WI-137 batch): telemetry commit hygiene + WI-keyed labels. New commit_telemetry commits the coordinator's OWN bookkeeping (the iteration log + regenerated index; the review scoreboard at its own write) in a dedicated best-effort telemetry: commit the moment it is written - never riding the next session's work commit or dangling (the session-021 defect-shape); a hook veto or nothing-staged leaves the files in the tree exactly as before (never-breaking). The WI a session claims is captured from docs/next-wi at session START (before a closing BUILD rewrites it) into a # wi: log-header line + a new WI index column. PROCESS_OPTIONS 'Unattended operation' paragraph updated (+484 B flagged, baseline 134965->135449 re-stamped across all 3 byte-budget-guard skill copies). Tests: test_telemetry_commits_itself_not_riding_the_next_commit, test_telemetry_commit_is_best_effort_when_the_hook_vetoes, test_wi_label_recorded_in_log_header_and_index.
