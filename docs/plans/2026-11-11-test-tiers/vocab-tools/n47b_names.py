"""HANDOFF 4.5.4: Python names renamed by token (pyname.py), after the
`git mv`s and r47b. Strings keep their words: `"red_rounds_max"` is the
retired key's spelling, `"review"` and `"red_mark"` inside `_moved(...)` are
the retired `[bars]` keys, and the cause keys that name the fields as strings
move by hand (h47d.py).

- `CommitCheckSettings` fields `review` -> `commit_checks`, `red_mark` ->
  `marker`; the locals and parameters holding one, `bars` -> `settings`.
- `kconfig.red_rounds_max()` -> `commit_check_failure_cap()`; the loop
  context's field `red_rounds_max` -> `failure_cap`, its local `red_max` ->
  `cap`.
"""

P = "project-trajectory/scripts/"
WHOLE = None
SETTINGS = {"review": "commit_checks", "red_mark": "marker", "bars": "settings"}

NAMES = [
    (P + "kitlib/expected_failure.py", SETTINGS, WHOLE),
    (P + "integrate.py", {"bars": "settings"}, (3010, 3025)),
    (P + "integrate.py", {"bars": "settings", "review": "commit_checks"}, (3149, 3164)),  # 3161-3164 applied second (/d/v47/n47b2.py)
    ("tests/test_expected_failure.py", SETTINGS, WHOLE),
    # the cap's reader
    (P + "kitlib/config.py", {"red_rounds_max": "commit_check_failure_cap"}, WHOLE),
    (P + "dispatch.py", {"red_rounds_max": "commit_check_failure_cap"}, WHOLE),
    ("tests/test_commit_check_failure_cap.py", {"red_rounds_max": "commit_check_failure_cap"}, WHOLE),
    # the loop's context field and the one call of the reader
    (P + "agent_loop.py", {"red_rounds_max": "commit_check_failure_cap", "red_max": "cap"}, (3803, 3803)),
    (P + "agent_loop.py", {"red_rounds_max": "failure_cap", "red_max": "cap"}, (1, 3404)),
    # failure_cap_check: its local `red` holds the failed rounds' count
    (P + "agent_loop.py", {"red_rounds_max": "failure_cap", "red": "failed"}, (3405, 3432)),
    (P + "agent_loop.py", {"red_rounds_max": "failure_cap", "red_max": "cap"}, (3433, 3802)),
    (P + "agent_loop.py", {"red_rounds_max": "failure_cap", "red_max": "cap"}, (3804, 99999)),
]
