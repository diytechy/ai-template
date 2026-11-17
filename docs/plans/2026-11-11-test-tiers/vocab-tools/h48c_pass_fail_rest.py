"""HANDOFF 4.5.6, by line (hline.py), after h48b_pass_fail.py: the last lines
the inventory still showed in the pass/fail sense.

Kept: EXTERNAL_SKILLS.md 49 (an external plugin's own GREEN/YELLOW/RED flags),
test_complexity_ratchet.py 225 (a ratchet history note).
"""

LINES = [
    ("project-trajectory/README.md", 107, "is its ruled red arm,", "is its ruled failure arm,"),
    ("project-trajectory/prompts/worker.template.md", 62, "turns the drain red)", "makes the drain fail)"),
    ("tests/golden/worker-prompt-one-row.txt", 18, "turns the drain red)", "makes the drain fail)"),
    ("project-trajectory/skills/autonomous-gate-operations/SKILL.md", 22, "Keep honest-red visible:", "Keep honest failures visible:"),
    ("docs/stack.ini", 1376, "a lint red stops the checks", "a lint failure stops the checks"),
    ("scripts/check_iterate.py", 802, '"green" if worst == 0 else "RED"', '"passed" if worst == 0 else "FAILED"'),
    ("tests/test_rule_sync.py", 10, "green or false failure at a gate", "pass or false failure at a gate"),
]
