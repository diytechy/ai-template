"""HANDOFF 4.5.2: Python names that hold the work-item key, renamed by token
(pyname.py). Each entry is limited to the lines where `bar` is the key: the
same files also use `bar` for a check tier (`integrate_fixtures.refused`) and
for running checks, which a later concept renames. Line numbers are those
after r47a.
"""

P = "project-trajectory/scripts/"

NAMES = [
    # intake._draft_refusal: the declared stage of a drafted row
    (P + "intake.py", {"bar": "stage"}, (1868, 1869)),
    # integrate._lane_checks_directives: the stages the claimed rows declare
    (P + "integrate.py", {"bars": "stages"}, (2068, 2094)),
    # integrate._run_bar's parameter: the stage it hands check.py --stage
    # (applied second, from /d/v47/n47a2.py, after h47a rewrote its docstring)
    (P + "integrate.py", {"gate": "stage"}, (1874, 1910)),
    # the spec fixtures' keyword, and the callers that pass it
    ("tests/integrate_fixtures.py", {"bar": "checks_stage"}, (140, 180)),
    ("tests/test_dispatch.py", {"bar": "checks_stage"}, (145, 170)),
    ("tests/test_dispatch.py", {"bar": "checks_stage"}, (890, 1000)),
    ("tests/test_integrate_station.py", {"bar": "checks_stage"}, (495, 530)),
]
