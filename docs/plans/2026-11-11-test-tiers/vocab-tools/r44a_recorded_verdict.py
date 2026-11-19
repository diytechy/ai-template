"""HANDOFF 4.4, row 1: a script recorded that the adjudicator's verdict parsed.

"accepted verdict" -> "recorded verdict"; outcome value accepted -> recorded.
Frees "accept" for the one act of 4.2.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import PROTECT, RECORDS  # noqa: E402,F401

SKIP = RECORDS

TOKENS = {
    "accepted_at": "recorded_at",
    "accepted_identities": "recorded_identities",
    "accepted_part": "recorded_part",
    "unaccepted_refusal": "unrecorded_refusal",
    "_unaccepted_reason": "_unrecorded_reason",
}

_V = r"(?:dispute |calls |parsed |, actable )?(?:verdict|sitting)"

REGEX = [
    # the stored value, as text and as a Python argument
    (r"outcome = accepted\b", "outcome = recorded"),
    (r'outcome="accepted"', 'outcome="recorded"'),
    (r"outcome = pending\|accepted\|failed", "outcome = pending|recorded|failed"),
    # the one reader, called through its module
    (r"\b((?:k|_kit)?sitting|SITTING_MOD)\.accepted\(", r"\1.recorded("),
    # prose, with the article that changes
    (r"\b([Aa])n accepted((?:,)? (?:committed, )?" + _V + ")", r"\1 recorded\2"),
    (r"\b([Aa])n ACCEPTED( " + _V + ")", r"\1 RECORDED\2"),
    (r"\b([Aa])n unaccepted( (?:or unreadable |or unruled )?(?:verdict|call|CLARITY))", r"\1n unrecorded\2"),
    (r"\b([Aa]) committed, accepted( verdict)", r"\1 committed, recorded\2"),
    (r"\baccepted( " + _V + ")", r"recorded\1"),
    (r"\bACCEPTED( " + _V + ")", r"RECORDED\1"),
    (r"\bunaccepted( (?:verdict|call))", r"unrecorded\1"),
    (r"\baccepted-verdict\b", "recorded-verdict"),
    (r"\broute-accepted\b", "route-recorded"),
    # test names
    (r"(?<![A-Za-z0-9])an_accepted_((?:dispute_|calls_)?(?:verdict|sitting))", r"a_recorded_\1"),
    (r"(?<![A-Za-z0-9])an_unaccepted_((?:or_unreadable_|or_unruled_)?(?:verdict|CLARITY))", r"an_unrecorded_\1"),
    (r"(?<=_)accepted_((?:dispute_|calls_)?(?:verdict|sitting))", r"recorded_\1"),
    (r"(?<=_)unaccepted_((?:or_unreadable_|or_unruled_)?(?:verdict|CLARITY))", r"unrecorded_\1"),
]
