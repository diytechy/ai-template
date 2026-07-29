+++
id = "WI-120"
title = "Cross-provider spawn path - Windows CLI shims fail CreateProcess (opencode WinError 2)"
workstream = "unattended"
needs = ["~WI-109"]
order = 119
+++

## Deliverable

Owner-directed 2026-07-12 (same sitting as the filing): run_session resolves argv[0] via shutil.which on Windows only (against the session env's PATH when a registry row declares one) and hands CreateProcess the resolved absolute path - an explicit .cmd runs fine; a which miss or a .ps1-only resolution falls through unchanged to the existing OSError sentinel, POSIX spawn byte-identical (os.name gate). Root cause (reproduced): npm-style CLIs install .cmd/.ps1 shims with no .exe, shutil.which honors PATHEXT (preflight passes) but CreateProcess resolves bare names only to .exe/.com - so the cross-family REVIEW-A leg (OPENAI rows) died at spawn every round (sessions 002/005) and reviews silently ran same-family. Rejected shell=True (quoting/injection on a prompt-carrying template). Tests: test_cmd_shim_cli_spawns_on_windows (a .cmd-shim-only fake CLI passes preflight, spawns, run ends DONE with no ERROR row; Windows-only, POSIX suite untouched). Live-verified: build_argv+run_session on the registry's exact terra CmdTemplate exits 0 with the model replying - the argv that produced WinError 2 hours earlier; the full OPENAI-written REVIEW-A verdict rides the next agent-resume run.
