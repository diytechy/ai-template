"""What a REVIEW session may change (S9, "verify, don't isolate"): the pure half.

Nothing on a commit reliably names its role, so the check keys on the record the
coordinator writes for every session - its phase and its exact commit range
(`# phase:`, `# commits: before..after`). For a REVIEW session that range may
change exactly one path: its own verdict file, the round file named for the
session's (train, ordinal) and the phase its log declares. The loop asks this
right after the session and the merge slot asks it again from the committed
logs; both ask `kitlib.verdict.scope_offenders`, so they cannot disagree.

In-memory only - the git-driven halves are in tests/test_verdict_record.py
(the merge ladder) and tests/test_agent_loop_review.py (the loop).
"""

import sys

from conftest import SCRIPTS

if str(SCRIPTS) not in sys.path:  # the kit's script-sibling import idiom
    sys.path.insert(0, str(SCRIPTS))

from kitlib import verdict as kv  # noqa: E402

OWN = "docs/reviews/t1/004-REVIEW-A-abc1234.md"
BEFORE = "a" * 40
AFTER = "b" * 40


def test_a_clean_review_changes_only_its_own_verdict():
    assert kv.scope_offenders([OWN], "t1", 4, "REVIEW-A") == []
    relaxed = "docs/reviews/t1/004-REVIEW-A-abc1234-relaxed.md"
    assert kv.scope_offenders([relaxed], "t1", 4, "REVIEW-A") == [], (
        "the recorded heterogeneity tag is part of the session's own name"
    )
    assert kv.scope_offenders([], "t1", 4, "REVIEW-A") == [], (
        "a session that committed nothing changed nothing"
    )


def test_anything_beside_the_verdict_is_named():
    changed = [
        OWN,
        "src/widget.py",
        "docs/log.d/WI-201-widget.md",
        # Record paths are not exempt: a round file for ANOTHER phase, ordinal or
        # train is a verdict this session had no business writing.
        "docs/reviews/t1/004-REVIEW-B-abc1234.md",
        "docs/reviews/t1/005-REVIEW-A-abc1234.md",
        "docs/reviews/t2/004-REVIEW-A-abc1234.md",
        "docs/reviews/t1/scoreboard.txt",
    ]
    assert kv.scope_offenders(changed, "t1", 4, "REVIEW-A") == sorted(changed[1:])


def test_the_recorded_range_parses_from_the_session_log_header():
    blob = "# phase: REVIEW-A\n# commits: {}..{}\n# tokens: 1+2\n".format(BEFORE, AFTER)
    assert kv.session_range(blob) == (BEFORE, AFTER)
    assert kv.parse_range("{}..{}".format(BEFORE, AFTER)) == (BEFORE, AFTER)
    # A session that committed nothing records an EMPTY range, and the loop's
    # placeholders for an unborn or unreadable head are not a range either.
    assert kv.session_range("# phase: REVIEW-A\n# commits: \n") is None
    assert kv.session_range("# phase: REVIEW-A\n") is None
    assert kv.parse_range("(root)..{}".format(AFTER)) is None
    assert kv.parse_range("{}..?".format(BEFORE)) is None
    assert kv.parse_range("") is None
