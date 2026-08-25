"""`kitlib.secret_classes` — the credential class vocabulary (WI-520).

Filed by the WI-508 alignment pass (`docs/plans/2026-08-25-remap-alignment.md`
§8, `F4`/`M17`): the hook scanner's enforcement floor (`check_privacy.py`) and
the session-transcript redactor (`agent_common.redact_secrets`) compiled their
credential patterns independently, and driven against five samples, four
disagreed IN BOTH DIRECTIONS — the one that mattered, a PEM private-key block
refused at the commit hook but passed unredacted into a committed transcript.

This module is the regression guard for the fix: it drives BOTH sides against
a shared sample set (Done-when #4) and pins two things that must never regress
independently of each other:

  1. **The five-sample table the alignment pass measured** now reads the way
     `SECRET_CLASSES`' per-class decision says it should (PEM: catch/catch;
     the three deliberate threshold asymmetries: miss/catch).
  2. **Nothing caught before WI-520 is caught less after it.** `_PRE_SCAN` /
     `_PRE_REDACT` below are FROZEN witnesses of the literals each module
     compiled before this row — independent of `kitlib.secret_classes`, so a
     future edit to the shared table cannot silently rewrite the ground truth
     it is being checked against.

Asserting that one list "contains" the other is deliberately NOT done: the
redactor's threshold is allowed to stay looser than the floor's (recorded in
`SECRET_CLASSES`'s own comments), so the pin here is per-class coverage against
the table's declared decision, not blanket equality between the two sides.
"""

import re
from pathlib import Path

import pytest

from conftest import load_script
from kitlib import secret_classes

CHECK_PRIVACY = load_script("check_privacy")
AGENT_COMMON = load_script("agent_common")


def _scanner_catches(text):
    """Whether check_privacy's Scanner (secrets floor, privacy layer off)
    flags `text` on any class. `root` is unused on this path (Scanner returns
    before touching it when `privacy_on=False`)."""
    scanner = CHECK_PRIVACY.Scanner(Path("."), secrets_on=True, privacy_on=False)
    return any(scanner.scan_line(text))


def _redactor_catches(text):
    """Whether agent_common.redact_secrets replaces anything in `text`."""
    _, hits = AGENT_COMMON.redact_secrets(text)
    return hits > 0


# --- 1. The alignment pass's own driven table, re-measured after the fix ----
#
# (label, sample text, scanner catches?, redactor catches?) — row 1 is the
# fix: PEM flips from (catch, MISS) to (catch, catch). Rows 2-5 are unchanged,
# deliberate asymmetries (SECRET_CLASSES' own per-class comments say why).

DRIVEN_SAMPLES = (
    (
        "PEM private key block",
        "-----BEGIN RSA PRIVATE KEY-----",  # privacy-ok: sample, not a key
        True,
        True,
    ),
    ("Bearer <30 chars>", "Bearer " + "a" * 30, False, True),
    ("ghp_ + 36 chars", "ghp_" + "a" * 36, True, True),
    ("ghp_ + 24 chars", "ghp_" + "a" * 24, False, True),
    ("sk- + 22 chars", "sk-" + "a" * 22, False, True),
)


@pytest.mark.parametrize(
    "label,text,scan_expected,redact_expected",
    DRIVEN_SAMPLES,
    ids=[s[0] for s in DRIVEN_SAMPLES],
)
def test_wi508_driven_table_matches_the_recorded_decision(
    label, text, scan_expected, redact_expected
):
    assert _scanner_catches(text) == scan_expected, label
    assert _redactor_catches(text) == redact_expected, label


# --- 2. Every declared class actually reaches the side that claims it -------
#
# The mechanical version of Done-when #1 ("both the scanner and the redactor
# read [the table]"): a class whose `scan_pattern`/`redact_pattern` drifted
# out of `TOKEN_RES`/`_SECRET_RES` (a hand-copy instead of a derivation) would
# fail here even though the table itself still looks right.

POSITIVE_SAMPLE_BY_CLASS = {
    "private key header": "-----BEGIN RSA PRIVATE KEY-----",  # privacy-ok: documented example of the pattern class, not a key
    "github token": "ghp_" + "a" * 36,
    "github fine-grained token": "github_pat_" + "a" * 22,
    "slack token": "xoxb-" + "1" * 10,
    "aws access key id": "AKIA" + "A" * 16,
    "api secret key": "sk-" + "a" * 24,
    "generic bearer token": "Bearer " + "a" * 25,
}


def test_every_class_has_a_driven_sample():
    """A canary against a class quietly dropping off the fixture below."""
    assert POSITIVE_SAMPLE_BY_CLASS.keys() == {
        cls.name for cls in secret_classes.SECRET_CLASSES
    }


@pytest.mark.parametrize("cls", secret_classes.SECRET_CLASSES, ids=lambda c: c.name)
def test_each_side_catches_the_class_it_claims(cls):
    sample = POSITIVE_SAMPLE_BY_CLASS[cls.name]
    if cls.scan_pattern is not None:
        assert _scanner_catches(sample), (
            "{!r} declares a scan_pattern but check_privacy's Scanner does "
            "not catch its own sample -- TOKEN_RES/KEY_RE has drifted from "
            "the shared table".format(cls.name)
        )
    if cls.redact_pattern is not None:
        assert _redactor_catches(sample), (
            "{!r} declares a redact_pattern but agent_common.redact_secrets "
            "does not catch its own sample -- _SECRET_RES has drifted from "
            "the shared table".format(cls.name)
        )


# --- 3. Nothing caught before WI-520 is caught less after it ----------------
#
# FROZEN witnesses: the exact literals each module compiled before this row
# (git history, pre-WI-520). Compared by BEHAVIOR over a probe set, not by
# string equality — the slack-token class changed its character-class member
# ORDER (`xox[baprs]-` -> `xox[abprs]-`), which is a no-op on what it matches,
# and a literal-text pin would wrongly flag that as a regression.

_PRE_SCAN = {
    "private key header": r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----",
    "github token": r"ghp_[A-Za-z0-9]{36}",
    "github fine-grained token": r"github_pat_[A-Za-z0-9_]{22,}",
    "slack token": r"xox[abprs]-[A-Za-z0-9-]{10,}",
    "aws access key id": r"(?<![A-Z0-9])AKIA[0-9A-Z]{16}(?![A-Z0-9])",
    "api secret key": r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{24,}(?![A-Za-z0-9_-])",
}

_PRE_REDACT = {
    "api secret key": r"sk-[A-Za-z0-9_-]{20,}",
    "github token": r"ghp_[A-Za-z0-9]{20,}",
    "github fine-grained token": r"github_pat_[A-Za-z0-9_]{20,}",
    "aws access key id": r"AKIA[0-9A-Z]{16}",
    "generic bearer token": r"(?i)\bBearer\s+[A-Za-z0-9._\-]{25,}",
    "slack token": r"xox[baprs]-[A-Za-z0-9-]{10,}",
    # "private key header" is deliberately ABSENT: it had no redact pattern
    # before WI-520 -- that omission is this row's whole subject, not a fact
    # this dict may pretend was always true.
}

# Threshold-straddling probes per class: at/above/below the tighter (scan)
# and looser (redact) cutoffs, plus a boundary case for the two classes whose
# floor pattern is word-bounded. Every probe is driven through BOTH the frozen
# old pattern and the live one; the assertion is that they agree, not that
# either produces a specific verdict, so the same table serves both sides.
_PROBES = {
    "private key header": [
        "-----BEGIN RSA PRIVATE KEY-----",  # privacy-ok: documented example of the pattern class, not a key
        "-----BEGIN CERTIFICATE-----",
        "no key here",
    ],
    "github token": [
        "ghp_" + "a" * 36,
        "ghp_" + "a" * 24,
        "ghp_" + "a" * 20,
        "ghp_" + "a" * 19,
        "not a token",
    ],
    "github fine-grained token": [
        "github_pat_" + "a" * 22,
        "github_pat_" + "a" * 20,
        "github_pat_" + "a" * 19,
    ],
    "slack token": [
        "xoxa-" + "1" * 10,
        "xoxb-" + "1" * 10,
        "xoxp-" + "1" * 10,
        "xoxr-" + "1" * 10,
        "xoxs-" + "1" * 10,
        "xoxc-" + "1" * 10,  # not a real prefix -- must reject on both sides
        "xox-" + "1" * 10,
    ],
    "aws access key id": [
        "AKIA" + "A" * 16,
        "xAKIA" + "A" * 16 + "y",  # embedded in a longer alnum run
        "AKIA" + "A" * 15,
    ],
    "api secret key": [
        "sk-" + "a" * 24,
        "sk-" + "a" * 20,
        "sk-" + "a" * 19,
        "xsk-" + "a" * 24 + "y",
    ],
    "generic bearer token": [
        "Bearer " + "a" * 25,
        "bearer " + "a" * 25,
        "Bearer " + "a" * 24,
        "Bearer" + "a" * 25,
    ],
}


@pytest.mark.parametrize("name", sorted(_PROBES), ids=sorted(_PROBES))
def test_pre_wi520_scan_behavior_is_preserved(name):
    old_source = _PRE_SCAN.get(name)
    if old_source is None:
        pytest.skip("{} had no pre-WI-520 scan pattern".format(name))
    old_rx = re.compile(old_source)
    new_rx = secret_classes.SECRET_CLASSES_BY_NAME[name].scan_pattern
    assert new_rx is not None, "{}: lost its scan pattern".format(name)
    for probe in _PROBES[name]:
        assert bool(old_rx.search(probe)) == bool(new_rx.search(probe)), (
            name,
            probe,
        )


@pytest.mark.parametrize("name", sorted(_PROBES), ids=sorted(_PROBES))
def test_pre_wi520_redact_behavior_is_preserved_or_is_the_declared_addition(name):
    old_source = _PRE_REDACT.get(name)
    new_rx = secret_classes.SECRET_CLASSES_BY_NAME[name].redact_pattern
    if old_source is None:
        if name == "private key header":
            assert new_rx is not None, (
                "the row's own stated minimum (PEM reaches the redactor) did not land"
            )
        else:
            assert new_rx is None, (
                "{}: gained a redact pattern with no pre-WI-520 record and "
                "no Done-when item authorizing a new addition".format(name)
            )
        return
    old_rx = re.compile(old_source)
    assert new_rx is not None, "{}: lost its redact pattern".format(name)
    for probe in _PROBES[name]:
        assert bool(old_rx.search(probe)) == bool(new_rx.search(probe)), (
            name,
            probe,
        )
