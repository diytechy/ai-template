+++
id = "WI-216"
title = "Deliver session prompts via stdin so a large prompt survives the Windows codex.CMD 8191 cmd.exe cap"
workstream = "unattended"
sr_refs = ["SR-026"]
buildtier = "strong"
order = 213
+++

## Deliverable

WI-216 (2026-07-17): the robust code fix for the codex 8191 defect gilbert hit (owner chose the stdin approach over gilbert's machine-local exe-path hack). build_argv now returns (argv, stdin_input): a CmdTemplate with {prompt} rides the command line (claude, unchanged); a template with NO {prompt} routes the prompt to the child's STDIN. run_session writes stdin_input from a DAEMON thread then closes - the fixed prompt + EOF preserves the SN-016 no-wedge invariant, and threading it means a non-draining child cannot block proc.wait's timeout. This keeps the command line short enough to survive the Windows npm codex.CMD 8191-char cmd.exe cap that silently killed brief-sized prompts-in-argv (short auth probes passed, masking it). Adopted: this repo's OPENAI-SOL/TERRA/LUNA rows + agents.template.csv's codex example drop {prompt} (codex reads stdin per its own help); claude keeps {prompt}. All 6 build_argv callsites updated (interactive path pipes via subprocess.run input=; the 3 dummy-prompt probes unpack). tests/test_session_stdin.py (5, incl. a 20,044-char prompt through stdin - gilbert's proven failing size). Spine: LLR-026 amended (+build_argv/run_session symbols + the stdin path), TC-026 extended; no new SR (robustness under SR-026/SN-016). Sits on WI-215 (same OpenAI cross-family-path thread).
