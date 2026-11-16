"""HANDOFF 4.2/4.3: the dial and its table.

`[attestation]` -> `[authority]`; `human_approval_through` ->
`operator_accepts_through`; the constant `LEGACY_ATTESTATION_KEY` ->
`LEGACY_DIAL_KEY`, which kitlib.authority already defines and agent_policy
re-exported under the other name.

The readers of still-older spellings (the 0-4 ordinal, the key
`human_ratification_through`, the gate-policy enum) keep reading them, now
inside the renamed table. They leave the core in D11's change.

"attestation" is also a work-item safety class (schedule.py, dispatch.py).
That is the act's concept and is not touched here: every rule below names the
table by its context.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT, RECORDS  # noqa: E402,F401

SKIP = RECORDS + HAND_ONLY + [
    "project-trajectory/scripts/migrate_vocabulary.py",
    "tests/test_migrate_vocabulary.py",
]

TOKENS = {
    "human_approval_through": "operator_accepts_through",
    "LEGACY_ATTESTATION_KEY": "LEGACY_DIAL_KEY",
}

_KEYS = (
    "operator_accepts_through|keep_nondependent|final_review|complete_review|"
    "complete_sample_rate|adjudication_review|decision_recording|gate_policy"
)

REGEX = [
    (r"\[attestation\]", "[authority]"),
    (r"_unconfirmed_form\(text, \x22attestation\x22", '_unconfirmed_form(text, "authority"'),
    (r"\b([Aa]) (`?operator_accepts_through)", r"\1n \2"),
    # the table as a Python string, always beside one of its keys or a reader
    (r'"attestation", "(?=' + _KEYS + r')', '"authority", "'),
    (r'"attestation", (key|old)\b', r'"authority", \1'),
    (r'\.get\("attestation"\)', '.get("authority")'),
    (r'\["attestation"\]', '["authority"]'),
    (r'\{"attestation": ', '{"authority": '),
    (r"dict\(data, attestation=", "dict(data, authority="),
    (r'_refusal\("attestation", old, _unconfirmed_form\(text, "attestation", True\)\)',
     '_refusal("authority", old, _unconfirmed_form(text, "authority", True))'),
    (r"'attestation = \{\{", "'authority = {{"),
    (r"\battestation = process_toml\(tmp_path\)", "authority = process_toml(tmp_path)"),
    (r"assert attestation == \{old:", "assert authority == {old:"),
    # the dial's name in prose
    (r"\bhuman-approval dial\b", "operator-acceptance dial"),
    (r"\bhuman-approval DIAL\b", "operator-acceptance DIAL"),
    (r"\b([Aa]) human-approval (dial|level|hold|rung)\b", r"\1n operator-acceptance \2"),
    (r"\bhuman-approval level\b", "operator-acceptance level"),
    (r"\bhuman-approval hold\b", "operator-acceptance hold"),
    (r"\bhuman-approval rung\b", "operator-acceptance rung"),
]
