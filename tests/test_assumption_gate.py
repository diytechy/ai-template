"""The assumption gate's check steps, driven through `check.py --run-step`
(TC-237, TC-238, TC-239).

With `[checks] assumption_gate` on in `docs/process.toml`, the argument behind
each requirement is gated at the rung where it can first be judged honestly:
at DevStg-Boundary its maturity (`assumption-gate`, SR-205) and each
interface-form requirement's crossings (`crossing-allocation`, SR-212's
Boundary arm), at DevStg-Arch the boundary interfaces reaching it
(`interface-allocation`, SR-212's Arch arm), and at DevStg-Release each
relied-on assumption's standing (`assumption-evidence`, SR-206). With the
setting absent or off the same findings print as advisories and every step
passes. The derived stage
never reads any of it.

Registered in `tests/conftest.py`'s `SLOW_MODULES`: every case runs the
harness of a bootstrapped scaffold as a subprocess (one bootstrap per module,
copied per case), and the release half commits an approval act to a real git
repository. The pure rules live in `assumption_rules.py`.
"""

import datetime
import inspect
import shutil
import subprocess

import pytest

from conftest import SCRIPTS, load_script, pin_autocrlf, run_py

CHECK = load_script("check")
SNAP = load_script("baseline_snapshot")
WRITER = load_script("record_observation")
SPINE_RULES = load_script("spine_rules")
import kitlib.ladder as LADDER  # noqa: E402  (scripts/ is on the path by now)
import kitlib.observation as OBS  # noqa: E402

NEEDS_REL = "docs/requirements/stakeholder-needs.toml"
SR_REL = "docs/requirements/system-requirements.toml"
LLR_REL = "docs/requirements/low-level-requirements.toml"
IF_REL = "docs/requirements/interfaces.toml"
DA_REL = "docs/requirements/assumptions.toml"
FRAME_REL = "docs/requirements/external.toml"
TC_REL = "docs/test/test-cases.toml"
POLICY_REL = "docs/process.toml"


# --- the project ---------------------------------------------------------------

NEEDS = """
[need.SN-001]
need = "An operator can tell what the system did with their request."
why = "A silent system is indistinguishable from a broken one."
priority = "M"
acceptance = "The operator names the outcome from what the system shows."
stakeholder_refs = ["STK-001"]
status = "Approved"

[stakeholder.STK-001]
name = "Operator"
description = "Runs the system and owns what it shows."
party = "EXT-001"
status = "Approved"
"""

FRAME = """
[entity.EXT-001]
name = "Operator"
class = "operational"
description = "The person running the system."
status = "Approved"

[entity.EXT-002]
name = "Archive"
class = "operational"
description = "A store the system writes to."
status = "Approved"

[boundary.B-01]
entity = "EXT-001"
direction = "out"
carries = "the outcome shown to the operator"
system = "operation"
status = "Approved"

[boundary.B-02]
entity = "EXT-002"
direction = "out"
carries = "the record kept"
system = "operation"
status = "Approved"

[boundary.B-03]
entity = "EXT-001"
direction = "in"
carries = "the operator's request"
system = "operation"
status = "Approved"
"""


def _assumption(did, *, status="Approved", standing="active", lands="B-01", **cells):
    extra = "".join('{} = "{}"\n'.format(k, v) for k, v in cells.items())
    return (
        "\n[assumption.{}]\n"
        'effect_at = ["{}"]\n'
        'assumption = "The operator reads what the system shows."\n'
        'holds_when = "The screen is in view."\n'
        'obstacle = "The operator looks away."\n'
        'falsifier = "A request repeated after its outcome was shown."\n'
        'status = "{}"\n'
        'standing = "{}"\n'
        "{}"
    ).format(did, lands, status, standing, extra)


def _requirement(sid, *, da=(), coincident=None, form=None, boundary=("B-01",)):
    lines = [
        "\n[requirement.{}]".format(sid),
        'title = "Requirement {}"'.format(sid),
        'sn_refs = ["SN-001"]',
        "boundary_refs = [{}]".format(", ".join('"{}"'.format(b) for b in boundary)),
        'requirement = "The system shall show the outcome."',
        'status = "Approved"',
    ]
    if da:
        lines.append("da_refs = [{}]".format(", ".join('"{}"'.format(d) for d in da)))
    if coincident:
        lines.append('coincident = "{}"'.format(coincident))
    if form:
        lines.append('form = "{}"'.format(form))
    return "\n".join(lines) + "\n"


def _write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.lstrip("\n"), encoding="utf-8", newline="\n")
    return path


def _policy(root, gate):
    """`[checks] assumption_gate` as given; None leaves the key out."""
    body = "[checks]\n"
    if gate is not None:
        body += "assumption_gate = {}\n".format("true" if gate else "false")
    _write(root, POLICY_REL, body)


@pytest.fixture(scope="module")
def bootstrapped(tmp_path_factory):
    """One scaffold bootstrapped from the kit, the documented quick-start."""
    dest = tmp_path_factory.mktemp("gate-scaffold")
    proc = run_py([SCRIPTS / "bootstrap.py", "--dest", dest], cwd=dest)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return dest


@pytest.fixture
def scaffold(bootstrapped, tmp_path):
    """A fresh copy of the module's scaffold for one case."""
    root = tmp_path / "project"
    shutil.copytree(bootstrapped, root)
    return root


def _project(root, files, gate, drop=()):
    """The scaffold with `files` written over its blank forms, the registries
    named in `drop` removed, and the gate's setting as given."""
    for rel, text in files.items():
        _write(root, rel, text)
    for rel in drop:
        (root / rel).unlink()
    _policy(root, gate)
    return root


def _step(root, name):
    """Run one of the scaffold's built-in steps the way the hook and a person
    do."""
    return run_py(["scripts/check.py", "--run-step", name], cwd=root)


def _findings(proc, kind, *needles):
    """The step's own finding lines of `kind` (FAIL or ADVISORY) naming every
    one of `needles`."""
    marker = "{}: ".format(kind)
    return [
        line.strip()
        for line in proc.stdout.splitlines()
        if line.strip().startswith(marker) and all(n in line for n in needles)
    ]


def _listing(root):
    proc = run_py(["scripts/check.py", "--stage", "all", "--list"], cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _listed_at(listing, name, stage):
    return [
        line
        for line in listing.splitlines()
        if line.strip().startswith("- {} ".format(name))
        and "[>={}]".format(stage) in line
    ]


# --- TC-237: the boundary half (SR-205) ----------------------------------------

BOUNDARY_SRS = (
    _requirement("SR-001", coincident="Showing the outcome is the outcome.")
    + _requirement("SR-002", da=["DA-001"])
    + _requirement("SR-003")
    + _requirement("SR-004", da=["DA-002"])
    + _requirement("SR-005", da=["DA-003"])
    + _requirement("SR-006", da=["DA-004"])
    + _requirement("SR-007", da=["DA-005"])
    + _requirement("SR-008", da=["DA-006"])
)

BOUNDARY_DAS = (
    _assumption("DA-001")
    + _assumption("DA-002", status="Drafted")
    + _assumption("DA-003", standing="falsified")
    + _assumption("DA-004", lands="B-02")
    + _assumption("DA-005", realized_by="SUR-001")
    + _assumption("DA-006", realized_by="SUR-002")
    + """
[surrogate.SUR-001]
name = "Scripted operator, drafted"
emulates = ["EXT-001"]
description = "A driver reading the screen."
status = "Drafted"

[surrogate.SUR-002]
name = "Scripted operator, approved"
emulates = ["EXT-001"]
description = "A driver reading the screen."
status = "Approved"
"""
)

BOUNDARY = {
    NEEDS_REL: NEEDS,
    FRAME_REL: FRAME,
    SR_REL: BOUNDARY_SRS,
    DA_REL: BOUNDARY_DAS,
}

# Each failing requirement, with what its finding must name.
BOUNDARY_FAILURES = {
    "SR-003": ("cites no assumption",),
    "SR-004": ("DA-002", "not approved"),
    "SR-005": ("DA-003", "not active"),
    "SR-006": ("DA-004", "does not reach"),
    "SR-007": ("DA-005", "SUR-001", "not approved"),
}


def test_with_no_frame_the_boundary_step_reports_nothing(scaffold):
    files = {k: v for k, v in BOUNDARY.items() if k != FRAME_REL}
    root = _project(scaffold, files, gate=True, drop=[FRAME_REL])
    proc = _step(root, "assumption-gate")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _findings(proc, "FAIL") == _findings(proc, "ADVISORY") == []
    assert "assumption-gate" in proc.stdout


@pytest.mark.parametrize("gate", [None, False], ids=["absent", "off"])
def test_with_the_gate_absent_or_off_each_condition_is_an_advisory(scaffold, gate):
    root = _project(scaffold, BOUNDARY, gate=gate)
    proc = _step(root, "assumption-gate")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _findings(proc, "FAIL") == []
    for sid, needles in BOUNDARY_FAILURES.items():
        assert len(_findings(proc, "ADVISORY", sid, *needles)) == 1, (sid, proc.stdout)


def test_with_the_gate_on_each_unmet_condition_fails_naming_it(scaffold):
    root = _project(scaffold, BOUNDARY, gate=True)
    proc = _step(root, "assumption-gate")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    failed = _findings(proc, "FAIL")
    for sid, needles in BOUNDARY_FAILURES.items():
        assert len(_findings(proc, "FAIL", sid, *needles)) == 1, (sid, proc.stdout)
    # A coincident requirement, one citing only approved, active, reaching
    # assumptions, and one whose fidelity assumption's surrogate is approved,
    # all pass: nothing names them.
    for sid in ("SR-001", "SR-002", "SR-008"):
        assert not [line for line in failed if sid in line], (sid, failed)
    assert len(failed) == len(BOUNDARY_FAILURES), failed


def test_a_frame_with_no_assumptions_registry_fails_every_non_coincident_requirement(
    scaffold,
):
    files = {k: v for k, v in BOUNDARY.items() if k != DA_REL}
    root = _project(scaffold, files, gate=True, drop=[DA_REL])
    proc = _step(root, "assumption-gate")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    failing = {
        sid
        for sid in (f"SR-00{i}" for i in range(1, 9))
        if _findings(proc, "FAIL", sid)
    }
    assert failing == {f"SR-00{i}" for i in range(2, 9)}, proc.stdout


def test_the_boundary_step_lists_at_the_boundary_rung_and_is_built_in(scaffold):
    root = _project(scaffold, BOUNDARY, gate=True)
    listing = _listing(root)
    for name in ("assumption-gate", "crossing-allocation"):
        assert len(_listed_at(listing, name, LADDER.STAGE_BOUNDARY)) == 1, listing
        assert name in CHECK.BUILTIN_STEP_NAMES


def test_the_derived_stage_is_identical_with_the_gate_on_and_off(scaffold):
    root = _project(scaffold, BOUNDARY, gate=False)
    derived = run_py(["scripts/derive_stage.py", "--root", root], cwd=root)
    assert derived.returncode == 0, derived.stdout + derived.stderr
    off = (root / "docs" / "stage").read_bytes()
    _policy(root, True)
    check = run_py(["scripts/derive_stage.py", "--root", root, "--check"], cwd=root)
    assert check.returncode == 0, check.stdout + check.stderr
    again = run_py(["scripts/derive_stage.py", "--root", root], cwd=root)
    assert again.returncode == 0, again.stdout + again.stderr
    assert (root / "docs" / "stage").read_bytes() == off


# --- TC-239: the interface-form requirement, both arms (SR-212) ------------------
# THE ARCH ARM: an interface-form requirement is reached through the modules
# its design rows name by each boundary interface owned there. SR-001 is
# reached by a coincident interface, SR-002 by one bridged by an assumption it
# cites; SR-003 only by one bridged by another assumption; SR-004 by none;
# SR-005 by one valid and one invalid interface. SR-006 and SR-007 are of the
# other two forms, and are never judged.

ARCH_SRS = (
    _requirement("SR-001", form="interface")
    + _requirement("SR-002", form="interface", da=["DA-001"])
    + _requirement("SR-003", form="interface", da=["DA-001"])
    + _requirement("SR-004", form="interface", da=["DA-001"])
    + _requirement("SR-005", form="interface", da=["DA-001"])
    + _requirement("SR-006", form="assumption", da=["DA-001"])
    + _requirement("SR-007", form="cross-cutting")
)


def _design(lid, module, sid):
    return (
        "\n[design.{}]\n"
        'sr_refs = ["{}"]\n'
        'title = "Design {}"\n'
        'module = "{}"\n'
        'code_symbol = "run"\n'
        'detail = "How {} is built."\n'
        'status = "Approved"\n'
    ).format(lid, sid, lid, module, sid)


ARCH_LLRS = (
    _design("LLR-001", "scripts/alpha.py", "SR-001")
    + _design("LLR-002", "scripts/beta.py", "SR-002")
    + _design("LLR-003", "scripts/gamma.py", "SR-003")
    + _design("LLR-004", "scripts/epsilon.py", "SR-004")
    + _design("LLR-005", "scripts/delta.py", "SR-005")
    + _design("LLR-006", "scripts/zeta.py", "SR-006")
    + _design("LLR-007", "scripts/eta.py", "SR-007")
)


def _interface(iid, owner, *, bridged=(), coincident=None):
    lines = [
        "\n[interface.{}]".format(iid),
        'owner = "{}"'.format(owner),
        'consumers = ["external:operator"]',
        'channel = "stdout"',
        'data = "the outcome"',
        'version = "v1"',
        'status = "Approved"',
        'interface_to_external = ["B-01"]',
    ]
    if bridged:
        lines.append(
            "bridged_by = [{}]".format(", ".join('"{}"'.format(d) for d in bridged))
        )
    if coincident:
        lines.append('coincident = "{}"'.format(coincident))
    return "\n".join(lines) + "\n"


ARCH_IFS = (
    _interface("IF-001", "scripts/alpha", coincident="The line shown is the outcome.")
    + _interface("IF-002", "scripts/beta", bridged=["DA-001"])
    + _interface("IF-003", "scripts/gamma", bridged=["DA-009"])
    + _interface("IF-004", "scripts/delta", bridged=["DA-001"])
    + _interface("IF-005", "scripts/delta", bridged=["DA-009"])
    # An internal seam realizes no crossing and reaches nothing.
    + '\n[interface.IF-006]\nowner = "scripts/epsilon"\nconsumers = '
    '["scripts/alpha"]\nchannel = "call"\ndata = "x"\nversion = "v1"\n'
    'status = "Approved"\n'
)

ARCH = {
    NEEDS_REL: NEEDS,
    FRAME_REL: FRAME,
    SR_REL: ARCH_SRS,
    LLR_REL: ARCH_LLRS,
    IF_REL: ARCH_IFS,
    DA_REL: _assumption("DA-001") + _assumption("DA-009"),
}

ARCH_FAILURES = {
    "SR-003": ("IF-003",),
    "SR-004": ("no boundary interface reaches it",),
    "SR-005": ("IF-005",),
}

# THE BOUNDARY ARM: the same form judged against the frame's crossings, the
# level-0 interfaces approved with the frame. SR-011 is recorded coincident;
# SR-012 cites an assumption landing on its crossing; SR-013 cites one landing
# elsewhere; SR-014 names two crossings and is bridged on one; SR-015 cites
# nothing. SR-016 is of assumption form, and SR-017 names a crossing the frame
# does not declare, which the frame's own rule fails, not this one.

CROSSING_SRS = (
    _requirement("SR-011", form="interface", coincident="The outcome shown is it.")
    + _requirement("SR-012", form="interface", da=["DA-001"])
    + _requirement("SR-013", form="interface", da=["DA-002"])
    + _requirement("SR-014", form="interface", da=["DA-001"], boundary=("B-01", "B-03"))
    + _requirement("SR-015", form="interface")
    + _requirement("SR-016", form="assumption")
    + _requirement("SR-017", form="interface", boundary=("B-09",))
)

CROSSING = {
    NEEDS_REL: NEEDS,
    FRAME_REL: FRAME,
    SR_REL: CROSSING_SRS,
    DA_REL: _assumption("DA-001") + _assumption("DA-002", lands="B-02"),
}

CROSSING_FAILURES = {
    "SR-013": ("B-01",),
    "SR-014": ("B-03",),
    "SR-015": ("B-01",),
}


def _judged(proc, kind, failures, others):
    """Each expected requirement named once with its needles, and nothing
    else named."""
    lines = _findings(proc, kind)
    for sid, needles in failures.items():
        assert len(_findings(proc, kind, sid, *needles)) == 1, (sid, proc.stdout)
    for sid in others:
        assert not [line for line in lines if "SR {} ".format(sid) in line], (
            sid,
            lines,
        )
    assert len(lines) == len(failures), lines


def test_the_arch_arm_fails_each_unreached_or_unbridged_requirement(scaffold):
    root = _project(scaffold, ARCH, gate=True)
    proc = _step(root, "interface-allocation")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    _judged(proc, "FAIL", ARCH_FAILURES, ("SR-001", "SR-002", "SR-006", "SR-007"))
    # The valid interface reaching SR-005 is not named: only the invalid one.
    assert not _findings(proc, "FAIL", "SR-005", "IF-004")


def test_the_arch_arm_is_advisory_with_the_gate_off(scaffold):
    root = _project(scaffold, ARCH, gate=False)
    proc = _step(root, "interface-allocation")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _findings(proc, "FAIL") == []
    _judged(proc, "ADVISORY", ARCH_FAILURES, ("SR-001", "SR-002", "SR-006", "SR-007"))


def test_the_boundary_arm_fails_each_crossing_neither_coincident_nor_bridged(scaffold):
    root = _project(scaffold, CROSSING, gate=True)
    proc = _step(root, "crossing-allocation")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    _judged(
        proc,
        "FAIL",
        CROSSING_FAILURES,
        ("SR-011", "SR-012", "SR-016", "SR-017"),
    )
    # SR-014's bridged crossing is not named: only the unbridged one.
    assert not _findings(proc, "FAIL", "SR-014", "B-01")


def test_the_boundary_arm_is_advisory_with_the_gate_off(scaffold):
    root = _project(scaffold, CROSSING, gate=None)
    proc = _step(root, "crossing-allocation")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _findings(proc, "FAIL") == []
    _judged(
        proc,
        "ADVISORY",
        CROSSING_FAILURES,
        ("SR-011", "SR-012", "SR-016", "SR-017"),
    )


def test_the_arms_list_at_their_rungs_and_the_stage_fold_takes_no_interface(
    scaffold,
):
    root = _project(scaffold, ARCH, gate=True)
    listing = _listing(root)
    assert len(_listed_at(listing, "interface-allocation", LADDER.STAGE_ARCH)) == 1
    assert len(_listed_at(listing, "crossing-allocation", LADDER.STAGE_BOUNDARY)) == 1
    assert {"interface-allocation", "crossing-allocation"} <= CHECK.BUILTIN_STEP_NAMES
    params = inspect.signature(SPINE_RULES.spine_stage).parameters
    assert not [p for p in params if "if" in p.split("_") or "interface" in p], params


# --- TC-238: the release half (SR-206) -----------------------------------------
# An assumption carries no evidence level (owner ruling 2026-10-02), so release
# asks no assumption for a passing result: it reads standing. Each assumption is
# cited by one requirement. DA-001 is active with no result at all, and DA-002
# active beside a failing observation that no person has acted on: both pass,
# since only a person or an adjudication sets standing. DA-003 is falsified with
# no accepted risk; DA-004 falsified under a risk accepted in the act that
# still stands; DA-005 falsified under a risk reopened by an edit to its text
# after that act; DA-006 falsified under a risk reopened by a failing sample
# recorded after it.

RELEASE_DAS = (
    _assumption("DA-001")
    + _assumption("DA-002")
    + _assumption("DA-003", standing="falsified")
    + _assumption("DA-004", standing="falsified", accepted_risk="Ship it anyway.")
    + _assumption("DA-005", standing="falsified", accepted_risk="Ship it anyway.")
    + _assumption("DA-006", standing="falsified", accepted_risk="Ship it anyway.")
)

RELEASE_SRS = "".join(
    _requirement("SR-00{}".format(i), da=["DA-00{}".format(i)]) for i in range(1, 7)
)


def _case(tid, did, sampling):
    return (
        "\n[test.{}]\n"
        'assumption_refs = ["{}"]\n'
        'level = "System"\n'
        'method = "An operator is watched reading the outcome."\n'
        'tier = "Release"\n'
        'expected = "The outcome is read."\n'
        'automated = "No"\n'
        'evidence = "docs/notes.md"\n'
        'status = "Approved"\n'
        'inputs = ["docs/notes.md"]\n'
        "max_age = 30\n"
        'sampling = "{}"\n'
    ).format(tid, did, sampling)


RELEASE_TCS = _case("TC-002", "DA-002", "sampled") + _case(
    "TC-006", "DA-006", "sampled"
)

RELEASE = {
    NEEDS_REL: NEEDS,
    FRAME_REL: FRAME,
    SR_REL: RELEASE_SRS,
    DA_REL: RELEASE_DAS,
    TC_REL: RELEASE_TCS,
    "docs/notes.md": "What the operator is shown.\n",
}

RELEASE_FAILURES = {
    "DA-003": ("falsified", "no accepted risk"),
    "DA-005": ("falsified", "reopened"),
    "DA-006": ("falsified", "reopened", "failed after the act"),
}


def _git(root, *args):
    proc = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, encoding="utf-8"
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip()


def _utc(moment):
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def _observe(root, tid, outcome="pass"):
    """A current record for `tid`, judging its inputs as they stand."""
    observed = datetime.datetime.now(datetime.timezone.utc).replace(
        microsecond=0
    ) - datetime.timedelta(hours=1)
    record = {
        "tc": tid,
        "outcome": outcome,
        "observed_at": _utc(observed),
        "provenance": "an operator watched at work",
        "expires": _utc(observed + datetime.timedelta(days=20)),
        "judged": WRITER.inputs_digest(root, ["docs/notes.md"]),
    }
    folder = root / OBS.OBSERVATIONS_DIR
    folder.mkdir(parents=True, exist_ok=True)
    OBS.write_atomic(
        folder / OBS.record_name(tid, record["observed_at"]), OBS.render(record)
    )


def _release_repo(scaffold, gate):
    """The release project in a git repository: the assumptions approved, with
    their accepted risks, in one act; then DA-005's text edited after it, and
    failing samples recorded against DA-002 and DA-006."""
    root = _project(scaffold, RELEASE, gate=gate)
    _git(root, "init", "-q")
    pin_autocrlf(root)
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "the project")
    SNAP.copy_live(root, seed=True)
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "approve the assumptions and their accepted risks")
    da = root / DA_REL
    text = da.read_text(encoding="utf-8")
    marker = "[assumption.DA-005]\n"
    head, tail = text.split(marker)
    da.write_text(
        head
        + marker
        + tail.replace(
            'holds_when = "The screen is in view."',
            'holds_when = "The screen is in view and lit."',
            1,
        ),
        encoding="utf-8",
        newline="\n",
    )
    for tid in ("TC-002", "TC-006"):
        _observe(root, tid, outcome="fail")
    return root


def test_the_release_step_fails_each_falsified_assumption_no_standing_risk_covers(
    scaffold,
):
    root = _release_repo(scaffold, gate=True)
    proc = _step(root, "assumption-evidence")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    lines = _findings(proc, "FAIL")
    for did, needles in RELEASE_FAILURES.items():
        assert len(_findings(proc, "FAIL", did, *needles)) == 1, (did, proc.stdout)
    for did in ("DA-001", "DA-002", "DA-004"):
        assert not [line for line in lines if "assumption {},".format(did) in line], (
            did,
            lines,
        )
    assert len(lines) == len(RELEASE_FAILURES), lines


def test_the_release_step_is_advisory_with_the_gate_off(scaffold):
    root = _release_repo(scaffold, gate=False)
    proc = _step(root, "assumption-evidence")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert _findings(proc, "FAIL") == []
    for did, needles in RELEASE_FAILURES.items():
        assert len(_findings(proc, "ADVISORY", did, *needles)) == 1, (did, proc.stdout)


def test_the_release_step_lists_at_the_release_rung_and_the_producer_pin_holds(
    scaffold,
):
    root = _project(scaffold, RELEASE, gate=True)
    listing = _listing(root)
    assert len(_listed_at(listing, "assumption-evidence", LADDER.STAGE_RELEASE)) == 1
    assert "assumption-evidence" in CHECK.BUILTIN_STEP_NAMES
    # The stage's single release producer, the harness evidence verdict, is
    # untouched: the approval-level pin on it still holds.
    import test_approval_level as approval_level

    approval_level.test_the_RELEASE_rung_has_EXACTLY_ONE_PRODUCER_and_it_is_the_EVIDENCE_VERDICT()


def test_the_release_step_judges_a_project_that_declares_no_frame(scaffold):
    """SR-206 has no frame exemption: with no crossing declared, a falsified
    relied-on assumption with no accepted risk still fails, and an active one
    with no result at all still passes."""
    files = {
        NEEDS_REL: NEEDS,
        SR_REL: _requirement("SR-001", da=["DA-001"])
        + _requirement("SR-002", da=["DA-002"]),
        DA_REL: _assumption("DA-001") + _assumption("DA-002", standing="falsified"),
        "docs/notes.md": "What the operator is shown.\n",
    }
    root = _project(scaffold, files, gate=True, drop=[FRAME_REL])
    proc = _step(root, "assumption-evidence")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    lines = _findings(proc, "FAIL")
    assert len(_findings(proc, "FAIL", "DA-002", "falsified")) == 1, lines
    assert not [line for line in lines if "assumption DA-001," in line], lines
    assert len(lines) == 1, lines
