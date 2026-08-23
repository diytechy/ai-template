+++
id = "WI-127"
title = "Run-state ask line - NEEDS-HUMAN stop banner headlines the human act"
workstream = "unattended"
needs = ["~WI-115", "~WI-125"]
order = 126
+++

## Deliverable

Owner-directed 2026-07-13 (interrupted-run triage: the console banner promised 'the asks below' but current_state_excerpt caps at 40 lines and this repo's Current State runs ~290 - the Needs <human> items and the WI-123 ask fell past the cap, so the stop said NEEDS-HUMAN without saying WHAT). docs/run-state may now follow the state word with one `ask: <one-line ask>` line: read_ask() scans for the `ask:` prefix and the NEEDS-HUMAN exit headlines it as the banner detail's first line, ABOVE the capped status excerpt; every state reader (read_declared, the hooks, check_trajectory's _first_declared_line) takes only the first declared line, so the extra line is invisible to them - never-breaking, absent line = byte-identical banner. The driver prompt's NEEDS-HUMAN clause now mandates the ask line alongside the existing status.md Needs-<human> requirement, and the loop's own three NEEDS-HUMAN writes (no-routable-model page, review-escalation page, critique-budget page) each write their ask into the file so the parked state stays self-describing after the console scrolls away. PROCESS_OPTIONS 'run-state contract' NEEDS-HUMAN bullet documents the line (the one home); the meta's live docs/run-state gains its real ask (rule WI-123). Tests: fake-agent needs-human action writes the ask line and the exit test asserts the headline; the three page-path tests pin state[0]=NEEDS-HUMAN + state[1]=ask.
