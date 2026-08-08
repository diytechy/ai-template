"""Gate authority as declared policy (Thread 32, process.md §4).

Who accepts a gate advance is a one-word `docs/gate-policy` value, stated
canonically in process.md §4 and referenced (never restated) everywhere else;
a non-default level ships with a repo-local deviation register. The tripwire
test keeps the de-duplication honest: a future edit must not re-scatter the
gate-authority claim across the kit's prose.
"""

import re

from conftest import KIT, SCRIPTS, process_key, run_py


def _level(root):
    """The declared gate authority — SN-028 moved it out of the one-word
    docs/gate-policy file into `docs/process.toml [attestation] gate_policy`."""
    return process_key(root, "attestation", "gate_policy")


def test_scaffold_gate_policy_defaults_attended(scaffold):
    # The scaffolded authority is `attended` — today's behavior, so existing
    # adopters and default scaffolds see zero change; no register is laid down.
    assert _level(scaffold) == "attended"
    assert not (scaffold / "docs" / "gate-policy.md").exists(), (
        "the deviation register is for non-default levels only"
    )
    assert not (scaffold / "docs" / "gate-policy").exists(), (
        "SN-028: a fresh scaffold gets ONE policy home, never both — shipping "
        "the legacy file too would hand every new repo the mixed-config refusal"
    )


def _bootstrap(tmp_path, *extra):
    dest = tmp_path / "repo"
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", dest, *extra], cwd=tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return dest


def test_gate_policy_autonomous_scaffolds_register(tmp_path):
    dest = _bootstrap(tmp_path, "--gate-policy", "autonomous")
    policy = dest / "docs" / "process.toml"
    assert _level(dest) == "autonomous"
    assert policy.read_text(encoding="utf-8").startswith("#"), "header kept"
    register = (dest / "docs" / "gate-policy.md").read_text(encoding="utf-8")
    assert "`autonomous`" in register
    assert "LLM-GATE" in register  # the verdict mechanism is pre-filled
    # The fixed points nothing overrides ship with every register.
    for point in (
        "G-Final is the human's",
        "No un-run greens",
        "The harness is still the bar",
        "never re-decided by an agent",
    ):
        assert point in register, "missing fixed point: " + point


def test_gate_policy_single_ratify_scaffolds_register(tmp_path):
    dest = _bootstrap(tmp_path, "--gate-policy", "single-ratify")
    assert _level(dest) == "single-ratify"
    register = (dest / "docs" / "gate-policy.md").read_text(encoding="utf-8")
    assert "G2 close" in register  # the fixed ratification point (Q5)
    assert "Blocked register" in register  # MEDIUM/HIGH routing (Q6 Hybrid)
    assert "G-Final is the human's" in register


def test_gate_policy_explicit_attended_matches_default(tmp_path):
    dest = _bootstrap(tmp_path, "--gate-policy", "attended")
    assert _level(dest) == "attended"
    assert not (dest / "docs" / "gate-policy.md").exists()


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
