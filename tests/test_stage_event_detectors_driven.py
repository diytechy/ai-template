"""The two EVENT detectors, re-keyed to the stage axis — the DRIVEN half
(WI-498 slice 4).

Everything the decisions in `test_stage_event_detectors.py` rest on that cannot
be stated in a fixture: the claim that three rungs are repo-global is a claim
about `spine_stage` and is driven on a real bootstrapped scaffold, and the tier
signal's whole subject is a delta between two committed git trees.

FILED IN `conftest.SLOW_MODULES` by the declared criterion — every test here
either takes the `scaffold` fixture (a full bootstrap) or builds and commits a
real git repo, the same class as `test_derive_stage` and `test_phase_rule`. The
split is by COST, not by importance: WI-497's two demanded regressions and the
end-to-end proof that `tier_signal`'s `strong` arm can now fire are here, and
they run at slice/phase close and in CI.
"""

import subprocess

import sys

from conftest import (
    SCRIPTS,
    load_script,
    make_minimal_project,
    pin_autocrlf,
    skip_without_env_gates,
)

# `kitlib` is a PACKAGE UNDER scripts/, which nothing puts on `sys.path` until
# the first `load_script` call — so a module-level `from kitlib import ...` in a
# test file resolves only when some earlier-collected module happens to have
# called it first. That held by accident until an xdist worker collected this
# module first (WI-498 slice 4). Stated explicitly here rather than inherited.
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from kitlib import ladder, stage as kitstage  # noqa: E402

DS = load_script("derive_stage")
INTAKE = load_script("intake")


# --- THE REPO-GLOBAL RUNGS, DRIVEN --------------------------------------------
def test_the_repo_global_rungs_are_the_ones_a_PER_PHASE_call_cannot_own(scaffold):
    """`REPO_GLOBAL_RUNGS` is a claim about `spine_stage`, so it is driven against
    `spine_stage` rather than asserted.

    The mechanism: a Drafted component makes `arch_incomplete` fire, and the
    component registry is repo-wide, so EVERY phase reports `DevStg-Arch` at once
    — including a phase whose own spine is fully decomposed and TC'd. That
    identical-across-phases signature is what "unattributable" means, and it is
    what the abstention refuses to blame on any one phase."""
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    srs_h = (
        "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,"
        "Priority,Verification,Status,Phase\n"
    )
    llrs_h = "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status,Phase\n"
    tcs_h = (
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,"
        "Status,Phase\n"
    )
    srs = "".join(
        '{},T,SN-001,"r","why","ac",,M,Test,Approved,{}\n'.format(sid, phase)
        for sid, phase in (("SR-001", "1"), ("SR-002", "2"))
    )
    llrs = "".join(
        '{},{},Adder,src/demo,add,"d",(see TC),Approved,{}\n'.format(lid, sid, phase)
        for lid, sid, phase in (
            ("LLR-001", "SR-001", "1"),
            ("LLR-002", "SR-002", "2"),
        )
    )
    tcs = "".join(
        '{},{},Unit,m,Smoke,"a=1","e",Yes,tests/t.py::t,Approved,{}\n'.format(
            tid, sid, phase
        )
        for tid, sid, phase in (("TC-001", "SR-001", "1"), ("TC-002", "SR-002", "2"))
    )
    (req / "system-requirements.csv").write_text(srs_h + srs, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(llrs_h + llrs, encoding="utf-8")
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(
        tcs_h + tcs, encoding="utf-8"
    )
    for name in ("external", "components"):
        for suffix in (".toml", ".csv"):
            path = req / (name + suffix)
            if path.exists():
                path.unlink()

    frame_free = DS.derive(scaffold)
    assert set(frame_free["per-phase-live"].values()) == {ladder.STAGE_IMPL}

    # ...now ONE drafted component row, which is a repo-wide fact.
    (req / "components.csv").write_text(
        "CMP-ID,Name,Responsibility,Owner,Status,Standing\n"
        'CMP-001,Core,"does things",team,Drafted,\n',
        encoding="utf-8",
    )
    drafted_frame = DS.derive(scaffold)
    per_phase = drafted_frame["per-phase-live"]
    assert set(per_phase.values()) == {ladder.STAGE_ARCH}, per_phase
    assert len(per_phase) == 2  # every phase at once — the unattributable shape
    assert ladder.STAGE_ARCH in kitstage.REPO_GLOBAL_RUNGS


def test_rung_3s_self_reporting_recursion_IS_visible_on_the_live_reading(scaffold):
    """Slice 3's banked tension, discharged in the detector's own terms.

    `arch_incomplete`'s docstring calls the recursion "the mechanism the whole
    eight-rung design rests on": minting a Drafted component for a newly
    identified sub-component drops the reported stage with nobody deciding to.
    Slice 1's draft exclusion made that FALSE of the effective stage, and slice 3
    banked the tension.

    It is not a contradiction once detection and selection are separated. The
    settled fold still ignores the Drafted component — SELECTION must not
    collapse on a draft — while the LIVE fold still sees it, and the LIVE fold is
    what the detector reads. The signal survives where events are detected; it is
    the headline that stopped moving, which is what slice 1 intended."""
    make_minimal_project(scaffold)
    req = scaffold / "docs" / "requirements"
    # The BOUNDARY rung sits below Arch and a scaffold ships a blank
    # `external.toml`, so the frame's lower rung would mask the one under test
    # (slice 2's banked finding). Declaring no boundary is a legal adopter shape
    # and the rungs' applies-when serves it explicitly.
    for suffix in (".toml", ".csv"):
        (req / ("external" + suffix)).unlink(missing_ok=True)
    # ONE carrier only: `spine_carrier.resolve` REFUSES both homes at once, and
    # the scaffold ships the `.toml` side.
    (req / "components.toml").unlink(missing_ok=True)
    (req / "components.csv").write_text(
        "CMP-ID,Name,Responsibility,Owner,Status,Standing\n"
        'CMP-001,Core,"does things",team,Founded,\n',
        encoding="utf-8",
    )
    settled_before = DS.derive(scaffold)["per-phase"]
    live_before = DS.derive(scaffold)["per-phase-live"]

    (req / "components.csv").write_text(
        "CMP-ID,Name,Responsibility,Owner,Status,Standing\n"
        'CMP-001,Core,"does things",team,Founded,\n'
        'CMP-002,NewlyIdentified,"a sub-component just seen",team,Drafted,\n',
        encoding="utf-8",
    )
    settled_after = DS.derive(scaffold)["per-phase"]
    live_after = DS.derive(scaffold)["per-phase-live"]

    # The settled reading is unmoved: a draft may not collapse selection.
    assert settled_after == settled_before
    # The live reading DID move, and to the Arch rung: the recursion reported
    # itself, with nobody deciding to.
    assert ladder.STAGE_ARCH not in live_before.values(), live_before
    assert set(live_after.values()) == {ladder.STAGE_ARCH}, live_after


# --- THE TIER SIGNAL (WI-497 folds here) --------------------------------------
# Each git test gates itself through `_repo`'s `skip_without_env_gates`, rather
# than a module-level `pytestmark`: half of this module needs no git at all and
# must keep running on a box without it.
def _git(root, *args):
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout


def _repo(root):
    skip_without_env_gates("git")
    root.mkdir(parents=True, exist_ok=True)
    _git(root, "init", "-q")
    pin_autocrlf(root)
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _git(root, "config", "commit.gpgsign", "false")
    _git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    (root / "docs").mkdir(exist_ok=True)
    return root


def _commit(root, message):
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", message)
    return _git(root, "rev-parse", "HEAD").strip()


def _write_stage_value(root, stage, header_suffix=""):
    record = {
        "stage": stage,
        "stage-ord": kitstage.order(stage),
        "stage-of": ladder.STAGE_OF,
        "floored": False,
        "settled-stage": stage,
        "live-stage": stage,
        "phase": 1,
        "per-phase": {"1": stage},
        "per-phase-live": {"1": stage},
        "drafted": 0,
        "fingerprint": "sha256:" + "0" * 64,
    }
    text = kitstage.render(record, "abc1234", "2026-08-21") + header_suffix
    (root / "docs" / "stage").write_text(text, encoding="utf-8", newline="\n")


def test_the_tier_signal_SEES_a_value_change_whose_header_is_unchanged(tmp_path):
    """WI-497's first demanded regression, on the new carrier.

    The defect it pins: `_gate_moved` took `splitlines()[0]` of `docs/gate` —
    the static do-not-hand-edit header, byte-identical at every revision of the
    derived era — so a real value move produced False. Here the header is
    IDENTICAL across the two revisions by construction (one renderer wrote both)
    and only the value differs, which is exactly the shape that used to read
    False."""
    root = _repo(tmp_path)
    _write_stage_value(root, ladder.STAGE_ARCH)
    before = _commit(root, "one")
    header_before = (
        (root / "docs" / "stage").read_text(encoding="utf-8").splitlines()[0]
    )
    _write_stage_value(root, ladder.STAGE_IMPL)
    after = _commit(root, "two")
    header_after = (root / "docs" / "stage").read_text(encoding="utf-8").splitlines()[0]

    assert header_before == header_after  # the line the retired reader compared
    assert INTAKE._stage_moved(root, before, after) is True


def test_the_tier_signal_IGNORES_a_header_only_change(tmp_path):
    """WI-497's second demanded regression: the inverse. A comment-only edit —
    the as-of stamp, a reworded header line — is not a stage move, and a reader
    that keyed on the whole file rather than the FIELD would call it one."""
    root = _repo(tmp_path)
    _write_stage_value(root, ladder.STAGE_ARCH)
    before = _commit(root, "one")
    _write_stage_value(root, ladder.STAGE_ARCH, header_suffix="# a later note\n")
    after = _commit(root, "two")
    assert (root / "docs" / "stage").read_text(encoding="utf-8").count("later note")
    assert INTAKE._stage_moved(root, before, after) is False


def test_an_unreadable_side_answers_False_rather_than_reporting_a_move(tmp_path):
    """The retired contract SAID "unreadable answers False" and did not do it: a
    None on one side compared unequal to a value on the other and reported a
    move. It matters at exactly one commit in every adopting repo — the kit
    upgrade that first writes `docs/stage` — where the before side has no file
    and a spurious `strong` row would be minted for a change nobody made."""
    root = _repo(tmp_path)
    (root / "seed.txt").write_text("x\n", encoding="utf-8")
    before = _commit(root, "no stage file yet")
    _write_stage_value(root, ladder.STAGE_IMPL)
    after = _commit(root, "the kit upgrade that adds docs/stage")
    assert INTAKE._stage_moved(root, before, after) is False


def test_a_stage_file_carrying_an_unknown_rung_answers_False(tmp_path):
    root = _repo(tmp_path)
    _write_stage_value(root, ladder.STAGE_ARCH)
    before = _commit(root, "one")
    # The retired tag below is the INPUT being proven rejected, not a use of it.
    retired = "stage = G3\n"  # check_vocab: allow
    (root / "docs" / "stage").write_text(retired, encoding="utf-8", newline="\n")
    after = _commit(root, "a retired vocabulary")
    assert INTAKE._stage_moved(root, before, after) is False


def test_tier_signals_STRONG_ARM_CAN_ACTUALLY_FIRE_end_to_end(tmp_path):
    """THE PROOF THIS SLICE OWES, and the reason the fix alone is not enough.

    `tier_signal`'s `strong` arm has been unreachable through the stage-delta
    input for the whole derived era — not wrong, DEAD. A unit test of
    `_stage_moved` proves the input; it does not prove the row. So this drives
    `intake._amendment_drafts` over a real two-commit repo whose merged delta
    both amends an approved spine cell (the mint's trigger) and moves the recorded
    stage (the signal), and asserts the minted row's `buildtier`.

    The counterfactual is the same repo with the stage value held still: the row
    still mints, at `medium`. One row touched, so `rows_touched > 3` cannot be
    what carried it — the stage delta is the only difference between the two."""
    root = _repo(tmp_path)
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    sr_header = (
        "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
        "Permutations,Priority,Verification,Status\n"
    )

    def write_sr(text):
        (req / "system-requirements.csv").write_text(
            sr_header
            + 'SR-001,Adder,SN-001,"{}","why","ac",,C,Test,Approved\n'.format(text),
            encoding="utf-8",
            newline="\n",
        )

    write_sr("the original text")
    _write_stage_value(root, ladder.STAGE_ARCH)
    before = _commit(root, "attested baseline")

    write_sr("the AMENDED text")
    _write_stage_value(root, ladder.STAGE_IMPL)
    after = _commit(root, "the merged branch's delta")

    drafts = INTAKE._amendment_drafts(root, before, after)
    assert len(drafts) == 1, drafts
    assert drafts[0]["buildtier"] == "strong"

    # The counterfactual: identical amendment, stage held still -> medium.
    root2 = _repo(tmp_path / "still")
    req2 = root2 / "docs" / "requirements"
    req2.mkdir(parents=True, exist_ok=True)

    def write_sr2(text):
        (req2 / "system-requirements.csv").write_text(
            sr_header
            + 'SR-001,Adder,SN-001,"{}","why","ac",,C,Test,Approved\n'.format(text),
            encoding="utf-8",
            newline="\n",
        )

    write_sr2("the original text")
    _write_stage_value(root2, ladder.STAGE_ARCH)
    before2 = _commit(root2, "attested baseline")
    write_sr2("the AMENDED text")
    _write_stage_value(root2, ladder.STAGE_ARCH)
    after2 = _commit(root2, "the merged branch's delta")

    drafts2 = INTAKE._amendment_drafts(root2, before2, after2)
    assert len(drafts2) == 1, drafts2
    assert drafts2[0]["buildtier"] == "medium"
