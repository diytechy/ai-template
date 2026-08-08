"""Gate authority after the dial moved (Thread 32 -> decision D-4/§1.4).

Who accepts a gate advance used to be the one-word `docs/gate-policy` value,
scaffolded into every repo and settable with `bootstrap.py --gate-policy`. The
P13 cutover replaced the enum with the numeric
`attestation.human_ratification_through`, and P14 deleted the file, its
template and the flag. The three tests that drove the scaffolded file and its
deviation register went with the feature.

What SURVIVES here is the part that was never about the file: the de-dup
tripwire. Gate authority is asserted once in process.md §4 and *referenced*
everywhere else, and a future edit must not re-scatter the claim across the
kit's prose. It is the one test in this module that can still fail for a
reason worth knowing about.
"""

import re

from conftest import KIT, SCRIPTS, run_py


def test_no_scaffold_lays_down_the_retired_gate_policy_file(scaffold):
    # The successor is `attestation.human_ratification_through`, whose SCHEMA
    # default 3 is exactly what the retired template's `attended` converted to
    # — so a default scaffold's behaviour is unchanged, and the kit now ships
    # that default ONCE. (Before P14 it shipped twice, and
    # tests/test_config_cutover.py had to pin the pair equal.)
    assert not (scaffold / "docs" / "gate-policy").exists()
    assert not (scaffold / "docs" / "gate-policy.md").exists()
    assert not (KIT / "gate-policy.template").exists()


def test_the_retired_scaffold_flag_is_gone(tmp_path):
    # Driven, not grepped: argparse must REFUSE it. A flag that parsed and did
    # nothing would leave an adopter believing they had declared an authority.
    proc = run_py(
        [
            SCRIPTS / "bootstrap.py",
            "--dest",
            tmp_path / "repo",
            "--gate-policy",
            "autonomous",
        ],
        cwd=tmp_path,
    )
    assert proc.returncode != 0
    assert "--gate-policy" in (proc.stderr + proc.stdout)


# The gate-authority claim, in the variants the kit's prose has historically
# used. "human ratification/decision" (the §6 decision-surfacing dial) is a
# different fact and deliberately not matched.
_AUTHORITY_CLAIM = re.compile(
    r"human\s+approval|human\s+approves|pausing\s+for\s+your\s+approval",
    re.IGNORECASE,
)


def test_gate_authority_stated_at_most_once_per_shipped_file():
    # The de-dup tripwire (field report R4): gate authority is asserted once in
    # process.md §4 and *referenced* everywhere else. Each shipped prose file
    # may carry at most one occurrence (its single reference); a second one
    # means the claim is being restated again.
    offenders = {}
    for path in sorted(KIT.rglob("*")):
        if not path.is_file():
            continue
        if not (path.suffix == ".md" or ".template" in path.name):
            continue
        if "scripts" in path.parts:
            continue
        hits = _AUTHORITY_CLAIM.findall(path.read_text(encoding="utf-8"))
        if len(hits) > 1:
            offenders[str(path.relative_to(KIT))] = len(hits)
    assert not offenders, (
        "gate authority restated (must be stated once in process.md §4 and "
        "referenced at most once per file): {}".format(offenders)
    )
