"""Three test names in the recorded-verdict sense the phrase rules did not reach."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import PROTECT, RECORDS  # noqa: E402,F401

SKIP = RECORDS

TOKENS = {
    "test_at_the_cap_an_accepted_dismissal_of_every_blocking_finding_passes": "test_at_the_cap_a_recorded_dismissal_of_every_blocking_finding_passes",
    "test_at_the_cap_anything_but_an_accepted_dismissal_is_refused": "test_at_the_cap_anything_but_a_recorded_dismissal_is_refused",
    "test_an_act_omitting_its_verdict_is_still_tied_to_an_accepted_one": "test_an_act_omitting_its_verdict_is_still_tied_to_a_recorded_one",
}
