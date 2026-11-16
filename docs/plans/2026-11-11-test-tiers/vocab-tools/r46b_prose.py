"""HANDOFF 10.6, second rule pass: phrases naming the passed-checks record (S1)
and the failed-checks record (4.5.1), in the files that discuss them.

Run after r46a, n46a (pyname) and h46a. Phrase rules only, each anchored on
a word that fixes the sense: "review attestation" is the record with
`checks=commit`; "refresh attestation" the refresh's; "the attest route" the
command. Bare "attestation" is not touched here, because the same files call
the `Review-Verdict:` trailer an attestation too (h46b-h46c read those by
hand). Every rule is limited to the S1 files listed below.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import HAND_ONLY, PROTECT as _PROTECT, RECORDS  # noqa: E402

S1_FILES = [
    "tests/test_agent_loop_review_gate.py",
    "tests/test_integrate_record_checks.py",
    "tests/test_integrate_station.py",
    "tests/test_passed_checks.py",
    "tests/test_review_brief_git.py",
    "tests/test_red_mark_lane.py",
    "tests/test_red_mark.py",
    "tests/test_dispatch.py",
    "tests/test_hooks_on_routes.py",
    "tests/conftest.py",
    "tests/integrate_fixtures.py",
    "tests/test_traj_panels.py",
    "tests/test_prompts.py",
    "tests/test_check_smoke_budget.py",
    "docs/requirements/low-level-requirements.toml",
    "docs/requirements/interfaces.toml",
    "docs/requirements/system-requirements.toml",
    "docs/test/test-cases.toml",
    "docs/runtime-flows.md",
    "docs/stack.ini",
    "project-trajectory/stack.ini.template",
    "project-trajectory/process.toml.template",
    "*/skills/coordinator-cycle/SKILL.md",
    "*/skills/coordinator-cycle/references/recipes.md",
]

import fnmatch  # noqa: E402
import subprocess  # noqa: E402

# Every tracked file outside S1_FILES is skipped, so the phrases below run as
# plain REGEX over the S1 files only (a SCOPED rule per file and phrase made
# vapply test every glob on every line of the whole tree: too slow to finish).
_TRACKED = subprocess.run(
    ["git", "-C", "C:/Projects/ai-template-wt-vocabulary", "ls-files"],
    capture_output=True, text=True, encoding="utf-8", check=True,
).stdout.splitlines()
_OUTSIDE = [rel for rel in _TRACKED if not any(fnmatch.fnmatch(rel, g) for g in S1_FILES)]

SKIP = RECORDS + HAND_ONLY + _OUTSIDE

_PHRASES = [
    # the record with checks=commit, by its earlier names
    (r"\ba verified green attestation\b", "a verified passed-checks record"),
    (r"\ba green review attestation\b", "a commit record"),
    (r"\bverified review attestations\b", "verified commit records"),
    (r"\b([Vv])erified review attestation\b", r"\1erified commit record"),
    (r"\breview attestation\b", "commit record"),
    (r"\bverified-attestation gate\b", "passed-checks gate"),
    (r"\bVerified-attestation gate\b", "Passed-checks gate"),
    # the refresh's record
    (r"\brefresh attestations\b", "refresh records"),
    (r"\brefresh attestation\b", "refresh record"),
    (r"\brefresh-attestation contract\b", "refresh-record contract"),
    # the trailer named with its label
    (r"\bChecks-Passed:? attestation trailer label\b", "Checks-Passed: trailer label"),
    (r"(`Checks-Passed: \.\.\. checks=commit`) attestation\b", r"\1 record"),
    (r"\b(a|the|A|The) (verified )?Checks-Passed attestation\b", r"\1 \2passed-checks record"),
    (r"(`Checks-Passed:`) attestation\b", r"\1 record"),
    (r"\bTHE BAR ATTESTATION\b", "THE PASSED-CHECKS RECORD"),
    # the values `landing` and `none`
    (r"\bbar landing or no-bar\b", "checks `landing` or `none`"),
    (r"\blanding or no-bar record\b", "`landing` or `none` record"),
    (r"\blanding and no-bar refresh records\b", "`landing` and `none` refresh records"),
    (r"\bwrites landing or no-bar\b", "writes `landing` or `none`"),
    (r"\(or no-bar\)", "(or none)"),
    # the command
    (r"\b([Tt])he attest route\b", r"\1he record-checks route"),
    (r"\b([Oo])n the attest route\b", r"\1n the record-checks route"),
    (r"\bthe attestation route\b", "the record-checks route"),
    (r"\b(the|an) attest step\b", lambda m: ("the" if m[1] == "the" else "a") + " record-checks step"),
    (r"\bthe attest command\b", "the record-checks command"),
    (r"\b([Dd])rive the attest command line\b", r"\1rive the record-checks command line"),
    (r"\ban attest operation\b", "a record-checks operation"),
    (r"\b(next|first) attest commit\b", r"\1 record-checks commit"),
    (r"\ban empty attestation commit\b", "an empty record-checks commit"),
    (r"\bone empty attestation commit\b", "one empty record-checks commit"),
    (r"\bof an attest message\b", "of a record-checks message"),
    (r"\bthe (next|first) attest\b", r"the \1 record-checks run"),
    (r"\bits first attest\b", "its first record-checks run"),
    (r"\ban attest's bar\b", "a record-checks run's bar"),
    (r"\bmoved the attest\b", "moved the record-checks run"),
    (r"\bevery bar, attest and full-suite run\b", "every bar, record-checks and full-suite run"),
    (r"\beach red attest\b", "each failed record-checks run"),
    (r"\brefresh and attest both\b", "refresh and record-checks both"),
    (r"\bthe attest tests\b", "the record-checks tests"),
    (r"\bThe attest fixture\b", "The record-checks fixture"),
    # applied as "this record-checks run runs"; h46b rewords it
    (r"\bthis attest runs\b", "this record-checks run runs"),
    (r"\bthe attest ran\b", "record-checks ran"),
    (r"\battest committed\b", "record-checks committed"),
    (r"\bmarker's attest and refresh arms\b", "marker's record-checks and refresh arms"),
    (r"\bthe attest route\b", "the record-checks route"),
    (r"# --- attest: ", "# --- record-checks: "),
    (r"\bso attest (resolves|names)\b", r"so record-checks \1"),
    # what the record names
    (r"\b([Tt])he attested commit\b", r"\1he recorded commit"),
    (r"\babove an attested commit\b", "above a recorded commit"),
    (r"\babove the attested (one|commit)\b", r"above the recorded \1"),
    (r"\bthe attested tip\b", "the recorded tip"),
    (r"\ban attested tip\b", "a recorded tip"),
    (r"\ban attested one\b", "a recorded one"),
    (r"\blast attested tree\b", "last recorded tree"),
    (r"\bthe attested tree\b", "the recorded tree"),
    (r"\bfrom the attested lane's own declarations\b", "from the lane's own declarations"),
    (r"\bthe attested lane's declarations\b", "the lane's declarations"),
    (r"\battested green\b", "recorded as passed"),
    (r"\b[Uu]nattested\b", lambda m: "Unrecorded" if m[0][0] == "U" else "unrecorded"),
    (r"\bno attested-commit line\b", "no recorded-commit line"),
    (r"\bOne producer writes every attestation\b", "One producer writes every passed-checks record"),
    (r"\bis not an attestation\b", "is not a passed-checks record"),
    (r"\bnot an attestation\b", "not a passed-checks record"),
    # the failed-checks record (4.5.1)
    (r"\b(the|a|one|each|committed) red record\b", r"\1 failed-checks record"),
    (r"\bred records\b", "failed-checks records"),
    (r"\bA red record\b", "A failed-checks record"),
    (r"\bthe red-round count\b", "the failed-round count"),
    # the record's value in prose: `review` -> `commit`
    (r"\blast review record\b", "last commit record"),
    (r"\bno review record\b", "no commit record"),
]

REGEX = _PHRASES

PROTECT = list(_PROTECT) + [
    r"red_rounds_max",
    r"RED_ROUNDS_\w+",
]
