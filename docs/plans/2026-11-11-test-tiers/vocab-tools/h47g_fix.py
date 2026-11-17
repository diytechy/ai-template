LINES = [
    ("tests/test_agent_loop_review_gate.py", 449, '@pytest.mark.parametrize("bar", ["green", "red"])', '@pytest.mark.parametrize("outcome", ["passed", "failed"])'),
    ("tests/test_agent_loop_review_gate.py", 450, "(tmp_path, checks):", "(tmp_path, outcome):"),
    ("tests/test_agent_loop_review_gate.py", 457, 'red=(bar == "red")', 'red=(outcome == "failed")'),
    ("tests/test_agent_loop_review_gate.py", 458, 'if bar == "red":', 'if outcome == "failed":'),
    ("tests/test_agent_loop_review_gate.py", 465, 'if bar == "green":', 'if outcome == "passed":'),
]
