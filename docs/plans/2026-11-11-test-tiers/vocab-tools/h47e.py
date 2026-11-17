"""HANDOFF 4.5.4, the prose that names the commit-check failure cap and the
module by their earlier words ("red cap", "red-round maximum", `red_mark`),
after r47b, n47b and h47d. The interface row's exit-code label follows the
constant renamed in 10.6 (`EXIT_CHECK_FAILURE_CAP`); no script prints it.
"""

P = "project-trajectory/scripts/"
AL = P + "agent_loop.py"
TC = "docs/test/test-cases.toml"

EDITS = [
    (
        AL,
        "    Returns `schedule_review_round`'s exit code, the red cap's after a red\n"
        "    (`failure_cap_check`), or None.",
        "    Returns `schedule_review_round`'s exit code, the failure cap's after a\n"
        "    refused build (`failure_cap_check`), or None.",
    ),
    (
        AL,
        "    is recorded as any red is. Returns the red cap's exit code after a red\n"
        "    (`failure_cap_check`), else None: the session is routed next.",
        "    is recorded as any failure is. Returns the failure cap's exit code after a\n"
        "    failure (`failure_cap_check`), else None: the session is routed next.",
    ),
    (
        AL,
        "    stop. A lane already at its red cap ends before any session.\"\"\"",
        "    stop. A lane already at its failure cap ends before any session.\"\"\"",
    ),
    (
        P + "kitlib/bootstrap_manifest.py",
        "    # WI-996 added `red_mark`: the declared strict expected-failure mark, its",
        "    # WI-996 added `expected_failure`: the declared strict expected-failure mark, its",
    ),
    (
        "tests/test_dispatch.py",
        "    with the red cap's exit code, specs still in active/.\"\"\"",
        "    with the failure cap's exit code, specs still in active/.\"\"\"",
    ),
    (
        "tests/test_dispatch.py",
        "    # TC-381. The red cap is a decided worker outcome:",
        "    # TC-381. The failure cap is a decided worker outcome:",
    ),
    (
        "tests/conftest.py",
        "        # WI-958: the review gate and the red-round cap, each case a real",
        "        # WI-958: the review gate and the commit-check failure cap, each case a real",
    ),
    (
        "tests/test_prompts.py",
        "def test_coordinator_cycle_states_the_red_round_cap_citing_the_key():",
        "def test_coordinator_cycle_states_the_failure_cap_citing_the_key():",
    ),
    (
        "tests/test_prompts.py",
        "    # each failed record-checks run as a red round and, at the declared key, closes the lane",
        "    # each failed record-checks run as a failed round and, at the declared key, closes the lane",
    ),
    (
        "docs/requirements/interfaces.toml",
        "9 REVIEW-OWED · 11 RESTART · 12 RED-CAP",
        "9 REVIEW-OWED · 11 RESTART · 12 CHECK-FAILURE-CAP",
    ),
    (
        "docs/requirements/low-level-requirements.toml",
        "The declared red-round maximum reads as a positive integer,",
        "The declared commit-check failure cap reads as a positive integer,",
    ),
    (
        TC,
        "Run red rounds across a process resume and through a commit record, asserting "
        "that the persisted count continues across the resume and resets after green.",
        "Run failed rounds across a process resume and through a commit record, asserting "
        "that the persisted count continues across the resume and resets once the checks pass.",
    ),
    (
        TC,
        "Reach the red-round maximum during a run and resume a lane already at that maximum,",
        "Reach the commit-check failure cap during a run and resume a lane already at that cap,",
    ),
    (
        TC,
        "Read absent and invalid red-round settings,",
        "Read absent and invalid failure-cap settings,",
    ),
]
