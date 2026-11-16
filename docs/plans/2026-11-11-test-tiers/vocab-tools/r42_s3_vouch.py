"""HANDOFF 4.2, two rows: the requirement field `verification` becomes
`verification_method` (row key `VerificationMethod`), and the method `Attest`
becomes `Vouch`.

Prose that needs a sentence rewritten (the method's definition, LLM-Attest,
"human attestation is the honest floor") is done by hand afterwards.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT, RECORDS  # noqa: E402,F401

SKIP = RECORDS + HAND_ONLY + [
    # reads an adopter's OLD csv headers by design; edited by hand
    "project-trajectory/scripts/migrate_carrier.py",
    "project-trajectory/scripts/migrate_vocabulary.py",
    "tests/test_migrate_carrier.py",
    "tests/test_migrate_vocabulary.py",
]

TOKENS = {
    "ATTESTED_METHODS": "VOUCHED_METHODS",
    "ATTESTED_METHOD": "VOUCHED_METHOD",
    "attested_verified": "vouched_verified",
    "ATTEST_SRS": "VOUCH_SRS",
    "ATTEST_TCS": "VOUCH_TCS",
}

REGEX = [
    # --- the field
    (r'(["\'])Verification\1', r"\1VerificationMethod\1"),
    (r"(?m)^(\s*)verification(\s*=\s*\")", r"\1verification_method\2"),
    (r"`verification = \"", '`verification_method = "'),
    (r",Verification(?=,|\"|\\n|$)", ",VerificationMethod"),
    (r"\| Verification \|", "| VerificationMethod |"),
    (r"`Verification`", "`VerificationMethod`"),
    # --- the method, as a value and in method lists
    (r"\b([Aa])n (\*\*)?`Attest`", r"\1 \2`Vouch`"),
    (r"\b([Aa])n VOUCHED_METHOD\b", r"\1 VOUCHED_METHOD"),
    (r"`Attest`", "`Vouch`"),
    (r'"Attest  "', '"Vouch  "'),
    (r"\(and Verification not in ", "(and VerificationMethod not in "),
    (r'"Attest"', '"Vouch"'),
    (r",Attest,", ",Vouch,"),
    (r"(Analysis\s*/\s*Inspection\s*/\s*)Attest\b", r"\1Vouch"),
    (r"(Inspection\s*/\s*Analysis\s*/\s*)Attest\b", r"\1Vouch"),
    (r"(Demonstration / Inspection / )Attest\b", r"\1Vouch"),
    (r"(Inspection \| )Attest( \| Critique)", r"\1Vouch\2"),
    (r"(\|Manual\|)Attest(\|Critique)", r"\1Vouch\2"),
    (r"\{Analysis, Inspection, Attest\}", "{Analysis, Inspection, Vouch}"),
    (r"\(Test / Attest / Demonstrated / Critique\)", "(Test / Vouch / Demonstrated / Critique)"),
    (r"\bAn Attest (SR|TC|requirement|one)\b", r"A Vouch \1"),
    (r"\ban Attest (SR|TC|requirement|one)\b", r"a Vouch \1"),
    (r"\bnon-Attest\b", "non-Vouch"),
    (r"\bAttest (SRs?|TCs?|rows?)\b", r"Vouch \1"),
    (r"\(unlike Attest\)", "(unlike Vouch)"),
    (r"\bUnlike Attest,", "Unlike Vouch,"),
    (r"\baccept Attest \(", "accept Vouch ("),
    (r"Critique/Attest SR", "Critique/Vouch SR"),
    # --- its report words
    (r"\bverified-attested=", "verified-vouched="),
    (r"\battested-vs-mechanized\b", "vouched-vs-mechanized"),
    (r"\battested-vs-everything-else\b", "vouched-vs-everything-else"),
    (r"mechanized / demonstrated / attested", "mechanized / demonstrated / vouched"),
    (r"mechanized/demonstrated/attested", "mechanized/demonstrated/vouched"),
    (r"Attested \(Attest\)", "Vouched (Vouch)"),
    (r"— attested \(human, §4\)", "— vouched (operator, §4)"),
    (r"\battested-by=", "vouched-by="),
    (r"\battested-on=", "vouched-on="),
]
