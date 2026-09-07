"""Real-Git checks for the implementation/spine-authoring merge boundary."""

import subprocess

from conftest import load_script


integrate = load_script("integrate")


def _git(root, *args):
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _repo(root, safety="ordinary"):
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.name", "Boundary Test")
    _git(root, "config", "user.email", "boundary@example.com")
    req = root / "docs" / "requirements"
    test = root / "docs" / "test"
    active = root / "docs" / "work" / "active" / "wi-001"
    req.mkdir(parents=True)
    test.mkdir(parents=True)
    active.mkdir(parents=True)
    (req / "system-requirements.toml").write_text(
        '[requirement.SR-001]\ntitle = "Capability"\n'
        'requirement = "The product shall work."\nstatus = "Drafted"\n'
    )
    (req / "low-level-requirements.toml").write_text(
        '[design.LLR-001]\nsr_refs = ["SR-001"]\ntitle = "Design"\n'
        'module = "src/old.py"\ncode_symbol = "old"\n'
        'detail = "Implement the capability."\ntest_refs = "TC-001"\n'
        'status = "Drafted"\n'
    )
    (test / "test-cases.toml").write_text(
        '[test.TC-001]\nverifies = ["SR-001", "LLR-001"]\n'
        'method = "Exercise the capability."\nexpected = "It works."\n'
        'evidence = "tests/test_old.py"\nstatus = "Drafted"\n'
    )
    (active / "WI-001-boundary.md").write_text(
        f'+++\nid = "WI-001"\ntitle = "Boundary"\nsafety_class = "{safety}"\n+++\n'
    )
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "seed")
    _git(root, "branch", "wi-001")
    return root


def _commit_branch(root, changes):
    _git(root, "checkout", "-q", "wi-001")
    for rel, old, new in changes:
        path = root / rel
        path.write_text(path.read_text().replace(old, new))
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "worker change")
    _git(root, "checkout", "-q", "main")


def test_ordinary_implementation_returns_governing_sr_change_as_handback(tmp_path):
    root = _repo(tmp_path)
    _commit_branch(
        root,
        [("docs/requirements/system-requirements.toml", "shall work", "shall persist")],
    )

    refusal = integrate._approval_act_refusal(root, "wi-001")

    assert "SafetyClass=spine" in refusal
    assert "SR-001 (Requirement)" in refusal
    assert "handback" in refusal


def test_exclusive_spine_authoring_may_propose_the_same_change(tmp_path):
    root = _repo(tmp_path, safety="spine")
    _commit_branch(
        root,
        [("docs/requirements/system-requirements.toml", "shall work", "shall persist")],
    )

    assert integrate._approval_act_refusal(root, "wi-001") is None


def test_ordinary_implementation_may_repoint_declared_evidence_bindings(tmp_path):
    root = _repo(tmp_path)
    _commit_branch(
        root,
        [
            (
                "docs/requirements/low-level-requirements.toml",
                'code_symbol = "old"',
                'code_symbol = "new"',
            ),
            (
                "docs/requirements/low-level-requirements.toml",
                'test_refs = "TC-001"',
                'test_refs = "TC-001, TC-002"',
            ),
            (
                "docs/test/test-cases.toml",
                'evidence = "tests/test_old.py"',
                'evidence = "tests/test_new.py"',
            ),
        ],
    )

    assert integrate._approval_act_refusal(root, "wi-001") is None


def test_trace_classification_does_not_exempt_governing_llr_or_tc_cells(tmp_path):
    root = _repo(tmp_path)
    _commit_branch(
        root,
        [
            (
                "docs/requirements/low-level-requirements.toml",
                "Implement the capability",
                "Cache the capability",
            ),
            (
                "docs/test/test-cases.toml",
                "Exercise the capability",
                "Inspect the capability",
            ),
        ],
    )

    refusal = integrate._approval_act_refusal(root, "wi-001")
    assert "LLR-001 (Detail)" in refusal
    assert "TC-001 (Method)" in refusal
