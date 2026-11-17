"""HANDOFF 10.7 item 1: Python names for a run of checks, renamed by token
(pyname.py), because the same spelling is prose elsewhere or names the
retired bar axis (`spine_rules.bar_label`, "BARS" in history comments), and a
local `bar` in `agent_common` is a rule of `=` that stays.

- traj_panels' panel 3: `bars` (the cadence's rows) -> `cadence`, and the
  passed-checks label `bar_label` -> `record_label`;
- test_check_smoke_budget: the two routes the commit checks run by, `BARS`
  -> `ROUTES` (values `commit`/`review` -> `by-hand`/`record-checks`, h47g),
  `bar` -> `route`, `_bar_budget_argv` -> `_route_budget_argv`;
- integrate_fixtures.refused: its third parameter is the check tier;
- test_integrate_station: the matched `checks PASS` summary;
- test_held_status_git: the refusal's text when no check suite is declared.
"""

NAMES = [
    ("project-trajectory/scripts/rendering/traj_panels.py", {"bars": "cadence", "bar_label": "record_label"}, None),
    ("tests/test_check_smoke_budget.py", {"BARS": "ROUTES", "bar": "route", "_bar_budget_argv": "_route_budget_argv"}, None),
    ("tests/integrate_fixtures.py", {"bar": "tier"}, (270, 290)),
    ("tests/test_integrate_station.py", {"bar": "summary"}, (1118, 1132)),
    ("tests/test_held_status_git.py", {"BAR": "UNDECLARED"}, None),
]
