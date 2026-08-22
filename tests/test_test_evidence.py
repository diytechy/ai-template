"""WI-500 — the test-evidence carrier: the record, its VALUE binding, its one
producer, and the Release rung it makes derivable.

The property under test throughout is the trust model, not the file format. A
committed claim that the declared suite passed is believable only if (a) nothing
but the harness can write it, (b) it is bound to the tree it was measured on so
it cannot outlive that tree, and (c) going stale is LOUD — the rung becomes
underivable AND the freshness check reds — rather than a quiet ride. Each of the
three has its own arm below, and the staleness arm is driven from both
directions (a spine edit and a source edit), because either alone would leave the
other invisible.
"""

import hashlib
import sys

import pytest

from conftest import SCRIPTS, load_script

sys.path.insert(0, str(SCRIPTS))

from kitlib import evidence as kitevidence  # noqa: E402
from kitlib import ladder as kitladder  # noqa: E402
from kitlib import stage as kitstage  # noqa: E402

RULES = load_script("spine_rules")
DERIVE = load_script("derive_stage")
PRODUCER = load_script("record_test_evidence")

pytestmark = pytest.mark.smoke


# --- fixtures -----------------------------------------------------------------
def _repo(tmp_path, *, src="src", tests="tests"):
    """A minimal tree with a declared source surface: `docs/stack.ini` naming two
    paths, one file in each, and no spine registries (their ABSENCE is a legal
    fingerprint value — `input_paths` says so)."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "stack.ini").write_text(
        "[paths]\nsrc = {}\ntests = {}\n".format(src, tests), encoding="utf-8"
    )
    (tmp_path / src).mkdir(parents=True, exist_ok=True)
    (tmp_path / src / "app.py").write_text("VALUE = 1\n", encoding="utf-8")
    (tmp_path / tests).mkdir(parents=True, exist_ok=True)
    (tmp_path / tests / "test_app.py").write_text("def test_x():\n    pass\n", "utf-8")
    return tmp_path


def _record(root, **over):
    rec = {
        "outcome": kitevidence.PASS,
        "tier": "full",
        "command": "python scripts/check.py --tier full",
        "revision": "abc1234",
        "binding": kitstage.evidence_binding(root, memo=None),
    }
    rec.update(over)
    return rec


def _write(root, **over):
    path = root / kitevidence.EVIDENCE_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        kitevidence.render(_record(root, **over), "2026-08-22"),
        encoding="utf-8",
        newline="\n",
    )
    return path


# --- the record ---------------------------------------------------------------
def test_the_record_round_trips_through_its_own_parser(tmp_path):
    root = _repo(tmp_path)
    _write(root)
    parsed = kitevidence.read(root)
    assert parsed["outcome"] == kitevidence.PASS
    assert parsed["tier"] == "full"
    assert parsed["binding"] == kitstage.evidence_binding(root, memo=None)


def test_a_file_that_is_not_a_record_reads_as_ABSENT_and_never_raises(tmp_path):
    """The deliberate divergence from `stage.parse`, which RAISES on a bad value.
    This file is a CLAIM; every way it can be wrong has the same right answer —
    the claim does not hold — and a crashed reader would be worse than a doubted
    one."""
    root = _repo(tmp_path)
    path = root / kitevidence.EVIDENCE_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# nothing declared here\n", encoding="utf-8")
    assert kitevidence.read(root) is None
    assert kitstage.evidence_verdict(root, memo=None)[0] is False


# --- the verdict --------------------------------------------------------------
def test_no_record_means_the_claim_does_not_hold(tmp_path):
    holds, reason = kitstage.evidence_verdict(_repo(tmp_path), memo=None)
    assert holds is False
    assert kitevidence.EVIDENCE_FILE in reason


def test_a_matching_record_HOLDS(tmp_path):
    root = _repo(tmp_path)
    _write(root)
    holds, reason = kitstage.evidence_verdict(root, memo=None)
    assert holds is True, reason


def test_a_SMOKE_tier_record_is_refused_by_the_READER(tmp_path):
    """Two refusals for one rule. The producer refuses to WRITE a partial tier;
    this is the second half — the reader refuses to BELIEVE one — because the file
    is committed state and a consumer must not have to trust its writer."""
    root = _repo(tmp_path)
    _write(root, tier="smoke")
    holds, reason = kitstage.evidence_verdict(root, memo=None)
    assert holds is False
    assert "whole-suite" in reason


def test_an_outcome_other_than_pass_is_refused(tmp_path):
    root = _repo(tmp_path)
    _write(root, outcome="fail")
    assert kitstage.evidence_verdict(root, memo=None)[0] is False


@pytest.mark.parametrize(
    "edit",
    [
        pytest.param(
            lambda r: (r / "src" / "app.py").write_text("VALUE = 2\n"), id="src"
        ),
        pytest.param(
            lambda r: (r / "tests" / "test_app.py").write_text("def test_y(): pass\n"),
            id="tests",
        ),
        pytest.param(
            lambda r: (r / "src" / "new.py").write_text("X = 0\n"), id="new-source-file"
        ),
        pytest.param(
            lambda r: (r / "docs" / "stack.ini").write_text(
                "[paths]\nsrc = src\ntests = tests\n[product]\ntest = pytest -k nothing\n"
            ),
            id="the-declared-bar-itself",
        ),
        pytest.param(
            lambda r: (
                (r / "docs" / "test").mkdir(exist_ok=True)
                or (r / "docs" / "test" / "test-cases.toml").write_text(
                    '[test.TC-001]\nverifies = ["SR-001"]\n'
                )
            ),
            id="a-new-test-case",
        ),
    ],
)
def test_the_claim_is_bound_to_the_TREE_it_was_measured_on(tmp_path, edit):
    """The WI-492 precedent, applied: value-bound, never space-bound. A record
    that survived any of these edits would be a green measured on a tree that no
    longer exists — the exact failure the stage unification exists to prevent."""
    root = _repo(tmp_path)
    _write(root)
    assert kitstage.evidence_verdict(root, memo=None)[0] is True
    edit(root)
    holds, reason = kitstage.evidence_verdict(root, memo=None)
    assert holds is False
    assert "STALE" in reason


def test_build_residue_is_NOT_part_of_the_binding(tmp_path):
    """A `__pycache__` entry changes on every interpreter run, so folding it would
    make every record stale the moment anything imported the tree."""
    root = _repo(tmp_path)
    _write(root)
    cache = root / "src" / "__pycache__"
    cache.mkdir()
    (cache / "app.cpython-311.pyc").write_bytes(b"\x00\x01")
    assert kitstage.evidence_verdict(root, memo=None)[0] is True


def test_a_WIDE_declared_surface_still_binds(tmp_path):
    """`src = .` is legal and a single-package project may well write it. The
    record must be excluded from its own fold, or no value could satisfy the
    binding and the rung would be unreachable for exactly the simplest layouts."""
    root = tmp_path
    (root / "docs").mkdir()
    (root / "docs" / "stack.ini").write_text("[paths]\nsrc = .\ntests = .\n", "utf-8")
    (root / "app.py").write_text("VALUE = 1\n", encoding="utf-8")
    _write(root)
    holds, reason = kitstage.evidence_verdict(root, memo=None)
    assert holds is True, reason
    (root / "app.py").write_text("VALUE = 2\n", encoding="utf-8")
    assert kitstage.evidence_verdict(root, memo=None)[0] is False


def test_an_UNDECLARED_source_surface_binds_to_nothing_and_is_refused(tmp_path):
    """A binding over an empty surface would be a digest of nothing: it would
    match forever. The producer refuses by name rather than writing one."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "stack.ini").write_text("[product]\ntest = pytest\n", "utf-8")
    assert kitevidence.source_paths(tmp_path) == []
    assert PRODUCER._refuse_without_a_surface(tmp_path)


# --- the loudness: staleness reaches the freshness check ----------------------
def test_the_STAGE_fingerprint_moves_with_the_SOURCE_only_while_a_record_exists(
    tmp_path,
):
    """THE HOLE THIS CLOSES, driven in both directions. If the stage fingerprint
    covered only the evidence file's BYTES, a source edit would leave it matching
    — so `read_stage` would return the RECORDED `DevStg-Release` without ever
    asking whether the evidence still held, and `derive_stage --check` would call
    the committed file fresh. With no record, the source is not folded at all, so
    an adopter below the rung pays nothing."""
    root = _repo(tmp_path)
    before = kitstage.fingerprint(root, memo=None)
    (root / "src" / "app.py").write_text("VALUE = 99\n", encoding="utf-8")
    assert kitstage.fingerprint(root, memo=None) == before, (
        "a repo with no evidence record must not fingerprint its source tree"
    )
    _write(root)
    with_record = kitstage.fingerprint(root, memo=None)
    assert with_record != before
    (root / "src" / "app.py").write_text("VALUE = 100\n", encoding="utf-8")
    assert kitstage.fingerprint(root, memo=None) != with_record, (
        "with a record present a source edit MUST move the stage fingerprint, or "
        "a stale Release rides the recorded cache unchecked"
    )


def test_the_evidence_file_is_a_declared_stage_input(tmp_path):
    declared = [d for d, _s in kitstage.DECLARED_INPUTS]
    assert kitevidence.EVIDENCE_FILE in declared


def test_the_binding_does_not_fold_the_record_itself(tmp_path):
    """It cannot: a record would have to contain its own digest. Editing an
    unrelated field of the file must therefore leave the binding computable and
    unchanged — what catches a doctored file is the field check, not the fold."""
    root = _repo(tmp_path)
    binding = kitstage.evidence_binding(root, memo=None)
    _write(root, revision="deadbee")
    assert kitstage.evidence_binding(root, memo=None) == binding


# --- the rung -----------------------------------------------------------------
SR = {
    "SR-ID": "SR-001",
    "Status": "Founded",
    "Verification": "Test",
    "SN-Refs": "SN-001",
    "Phase": "1",
}
LLR = {"LLR-ID": "LLR-001", "SR-Refs": "SR-001", "Status": "Founded", "Phase": "1"}
TC = {"TC-ID": "TC-001", "Verifies": "SR-001", "Status": "Founded", "Phase": "1"}


def _stage(evidence_passed):
    return RULES.spine_stage(
        [dict(SR)],
        [dict(LLR)],
        [dict(TC)],
        sn_ids={"SN-001"},
        sn_draft=set(),
        evidence_passed=evidence_passed,
    )


def test_a_settled_spine_reaches_RELEASE_only_with_the_evidence_verdict():
    assert _stage(False) == kitladder.STAGE_IMPL
    assert _stage(True) == kitladder.STAGE_RELEASE


def test_the_evidence_argument_cannot_lift_an_UNSETTLED_spine():
    """Evidence is the LAST condition, not an override. A repo whose test cases
    are still Drafted does not reach Release because a suite went green — the
    green was measured over a spine that is still being written."""
    drafted = RULES.spine_stage(
        [dict(SR)],
        [dict(LLR)],
        [dict(TC, Status="Drafted")],
        sn_ids={"SN-001"},
        sn_draft=set(),
        evidence_passed=True,
    )
    assert drafted == kitladder.STAGE_TESTS


def test_the_derivation_reaches_RELEASE_end_to_end(tmp_path, monkeypatch):
    """The whole chain in one place: a holding record -> `evidence_passed` ->
    `spine_stage` -> the recorded `stage =` field."""
    root = _repo(tmp_path)
    monkeypatch.setattr(
        DERIVE.spine_rules,
        "load_spine",
        lambda docs: {
            "srs": [dict(SR)],
            "llrs": [dict(LLR)],
            "tcs": [dict(TC)],
            "sn_ids": {"SN-001"},
            "sn_draft": set(),
            "bifs": [],
            "cmps": [],
            "have_bifs": False,
            "have_cmps": False,
        },
    )
    assert DERIVE.derive(root)["stage"] == kitladder.STAGE_IMPL
    _write(root)
    assert DERIVE.derive(root)["stage"] == kitladder.STAGE_RELEASE
    (root / "src" / "app.py").write_text("VALUE = 3\n", encoding="utf-8")
    assert DERIVE.derive(root)["stage"] == kitladder.STAGE_IMPL, (
        "a source edit after the run must drop the rung back — evidence goes "
        "stale, it is never silently ridden"
    )


# --- the producer -------------------------------------------------------------
def _fake_harness(exit_code):
    return lambda root, tier: [
        sys.executable,
        "-c",
        "raise SystemExit({})".format(exit_code),
    ]


def test_a_GREEN_run_writes_a_record_that_HOLDS(tmp_path, monkeypatch):
    root = _repo(tmp_path)
    monkeypatch.setattr(PRODUCER, "harness_command", _fake_harness(0))
    assert PRODUCER.main(["--root", str(root), "--tier", "full"]) == 0
    assert kitstage.evidence_verdict(root, memo=None)[0] is True


def test_a_RED_run_writes_NOTHING(tmp_path, monkeypatch):
    """There is no `outcome = fail` state and no flag that records without
    running: a red run leaves the committed state exactly as it was (OI-30 D2 —
    only the harness's own exit may be the source of the claim)."""
    root = _repo(tmp_path)
    monkeypatch.setattr(PRODUCER, "harness_command", _fake_harness(1))
    assert PRODUCER.main(["--root", str(root), "--tier", "full"]) == 1
    assert not (root / kitevidence.EVIDENCE_FILE).exists()


def test_a_RED_run_does_not_overwrite_an_existing_record(tmp_path, monkeypatch):
    root = _repo(tmp_path)
    monkeypatch.setattr(PRODUCER, "harness_command", _fake_harness(0))
    PRODUCER.main(["--root", str(root), "--tier", "full"])
    before = (root / kitevidence.EVIDENCE_FILE).read_bytes()
    monkeypatch.setattr(PRODUCER, "harness_command", _fake_harness(2))
    assert PRODUCER.main(["--root", str(root), "--tier", "full"]) == 1
    assert (root / kitevidence.EVIDENCE_FILE).read_bytes() == before


def test_the_writer_refuses_a_PARTIAL_tier(tmp_path, monkeypatch):
    root = _repo(tmp_path)
    monkeypatch.setattr(PRODUCER, "harness_command", _fake_harness(0))
    assert PRODUCER.main(["--root", str(root), "--tier", "smoke"]) == 2
    assert not (root / kitevidence.EVIDENCE_FILE).exists()


def test_dry_run_runs_nothing_and_writes_nothing(tmp_path, monkeypatch):
    root = _repo(tmp_path)
    marker = tmp_path / "the-harness-ran"
    monkeypatch.setattr(
        PRODUCER,
        "harness_command",
        lambda r, t: [
            sys.executable,
            "-c",
            "open({!r}, 'w').close()".format(str(marker)),
        ],
    )
    assert PRODUCER.main(["--root", str(root), "--dry-run"]) == 0
    assert not marker.exists(), "--dry-run invoked the harness"
    assert not (root / kitevidence.EVIDENCE_FILE).exists()


def test_check_reports_the_verdict_and_exits_nonzero_when_it_does_not_hold(
    tmp_path, monkeypatch
):
    root = _repo(tmp_path)
    assert PRODUCER.main(["--root", str(root), "--check"]) == 1
    _write(root)
    assert PRODUCER.main(["--root", str(root), "--check"]) == 0
    (root / "src" / "app.py").write_text("VALUE = 7\n", encoding="utf-8")
    assert PRODUCER.main(["--root", str(root), "--check"]) == 1


def test_the_producer_names_the_documented_harness_entry_point():
    """SR-151/SR-152's one-definition-of-passing rule reaches the driver too: it
    invokes `check.py` at a declared tier, never a test command of its own."""
    argv = PRODUCER.harness_command(".", "full")
    assert argv[1].endswith("check.py")
    assert argv[2:] == ["--tier", "full"]
    assert "pytest" not in " ".join(str(a) for a in argv)


def test_the_binding_written_is_the_one_the_reader_recomputes(tmp_path, monkeypatch):
    """The producer and the verdict must fold identically — a mismatch here would
    make every freshly written record read stale."""
    root = _repo(tmp_path)
    monkeypatch.setattr(PRODUCER, "harness_command", _fake_harness(0))
    PRODUCER.main(["--root", str(root), "--tier", "full"])
    written = kitevidence.read(root)["binding"]
    assert written == kitstage.evidence_binding(root, memo=None)
    assert written.startswith("sha256:")
    assert written != hashlib.sha256(b"").hexdigest()


def test_the_shipped_harness_the_driver_names_actually_exists():
    """Not a unit-test artifact: the shipped driver spawns the kit's own
    `check.py`, so a rename of the harness reddens here rather than at an
    adopter's first attempt to earn the rung."""
    assert PRODUCER.harness_path().is_file()
