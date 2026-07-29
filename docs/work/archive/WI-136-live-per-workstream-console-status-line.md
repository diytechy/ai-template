+++
id = "WI-136"
title = "Live per-workstream console status line (agent-resume)"
workstream = "unattended"
order = 135
+++

## Deliverable

Off-spine dev-slice (2026-07-14, WI-136;WI-137 batch): the live per-workstream console status line. agent_loop's echo_session_line split into summarize_session_line (the shared stream-json parse) + a thin scrolling echo; new LiveStatus renders ONE in-place line per workstream (CR + \x1b[2K clear + terminal-width truncation), selected by --live-status / a docs/live-status toggle but ONLY when stdout is a TTY with VT on (_stdout_is_tty + _enable_windows_vt, stdlib ctypes on Windows, curses/colorama-free) - a pipe/CI log keeps the append-only scroll (never-breaking); run_session's echo bool generalized to an on_line callback; --no-session-echo still silences both. Off-spine, no SR. Tests: test_summarize_session_line_shapes, test_live_status_rewrites_one_line_in_place, test_live_status_falls_back_to_scroll_on_non_tty.
