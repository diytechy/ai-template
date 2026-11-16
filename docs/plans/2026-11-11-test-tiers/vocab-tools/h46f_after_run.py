"""HANDOFF 10.6, what the first test run found: the merge slot's refusal now
names the record's set as `checks=commit`, and the test asked for the word
"review" (the earlier value). It asks for the new value.
"""

EDITS = [
    ("tests/test_integrate_record_checks.py",
     "    # A build round's record of green is not the landing checks: the slot refuses\n"
     "    # it and names the bar it found and the one it needs.\n",
     "    # A build round's passed-checks record is not the landing checks: the slot\n"
     "    # refuses it and names the set it found and the one it needs.\n"),
    ("tests/test_integrate_record_checks.py",
     '    assert not ready and "review" in why and "landing" in why, why\n',
     '    assert not ready and "checks=commit" in why and "landing" in why, why\n'),
]
