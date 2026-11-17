"""HANDOFF 4.5.6 and 10.7 item 1: parametrize ids the rules left half-moved
(no evidence cell cites an id), by line (hline.py)."""

LINES = [
    ("tests/test_integrate_record_checks.py", 146, 'ids=["red-checks", "red-named-test"]', 'ids=["failing-checks", "failing-named-test"]'),
    ("tests/test_test_evidence.py", 154, 'id="the-declared-checks-itself"', 'id="the-declared-checks-themselves"'),
]
