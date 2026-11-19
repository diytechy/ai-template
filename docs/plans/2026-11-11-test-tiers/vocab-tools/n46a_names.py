"""HANDOFF 10.6: Python names of the passed-checks record, renamed by token (pyname.py).

`attested` held a `PassedChecks` (or the sha carrying one) and becomes
`passed`; the trailer's field and parameter `bar` becomes `checks`;
`integrate.attest` becomes `record_checks`. Each entry is limited to the
lines where the name has that sense: a work item's `bar` key, a bar summary
matched in a test, and the parametrized red/green `bar` of one loop test keep
the word (4.5.2 to 4.5.7, 10.7). Line numbers are those after r46a.
"""

P = "project-trajectory/scripts/"
WHOLE = None

NAMES = [
    (P + "kitlib/verdict.py", {"attested": "passed", "bar": "checks"}, WHOLE),
    # the Review-Verdict trailers at one tree, in `_round_refusal`
    (P + "integrate.py", {"attested": "trailers"}, (1707, 1708)),
    (P + "integrate.py", {"attested": "passed"}, (1709, 99999)),
    (P + "integrate.py", {"bar": "checks", "attest": "record_checks"}, (2800, 99999)),
    (P + "agent_loop.py", {"attested": "passed"}, WHOLE),
    (P + "review_brief.py", {"attested": "passed"}, WHOLE),
    (P + "kitlib/red_mark.py", {"attested": "passed"}, WHOLE),
    ("tests/test_passed_checks.py", {"attested": "passed", "bar": "checks"}, WHOLE),
    ("tests/test_integrate_record_checks.py", {"attested": "passed", "bar": "checks"}, WHOLE),
    ("tests/test_integrate_station.py", {"attested": "passed"}, WHOLE),
    ("tests/test_integrate_station.py", {"bar": "checks"}, (1395, 1415)),
    ("tests/test_review_brief_git.py", {"attested": "passed", "bar": "checks"}, WHOLE),
    ("tests/test_red_mark_lane.py", {"attested": "passed", "bar": "checks"}, WHOLE),
    ("tests/test_agent_loop_review_gate.py", {"attested": "passed", "att": "rec", "attests": "checks_logs"}, WHOLE),
    ("tests/test_agent_loop_review_gate.py", {"bar": "checks"}, (434, 434)),
]
